"""Check compensation normal forms, resource cuts and minimum link costs."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_arbitrary_depth_cap_relays import relay_family
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_native_guard_compensation import force_matching
from check_one_sided_interval_allocation import (
    allocate, chain_family, grid_allocation, independent_maximum,
)
from check_residual_corridors import direct_check, transformed
from check_shared_donor_collision_after_mixed_relays import collision_family
from check_terminal_cancellation_and_stranded_demand import (
    all_link_matchings, cancel_pairs, direct_family, extended_ports, terminal_data,
)
from degree_three_fusion import occupied_bands


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def owner_data(kinds, pairs):
    assert len(kinds) == 2*len(pairs)
    owners = {point: index for index, pair in enumerate(pairs) for point in pair}
    assert len(owners) == len(kinds) and set(owners) == set(kinds)
    types = {index: tuple(sorted(kinds[point] for point in pair))
             for index, pair in enumerate(pairs)}
    alphas = {index for index, kind in types.items() if kind == ('TP', 'TP')}
    betas = {index for index, kind in types.items() if kind == ('BP', 'BP')}
    mixed = set(types)-alphas-betas
    return owners, alphas, betas, mixed


def solve(kinds, pairs, links, access, resources):
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    assert all(kinds[first] == 'TP' and kinds[second] == 'BP' for first, second in links)
    assert all(set(choices) <= resources for choices in access.values())
    source, sink = ('source',), ('sink',)
    edges, adjacency = [], defaultdict(list)

    def add(first, second, capacity, cost=0, tag=None):
        position = len(edges)
        edges.extend([dict(first=first, second=second, residual=capacity,
                           initial=capacity, cost=cost, tag=tag),
                      dict(first=second, second=first, residual=0,
                           initial=0, cost=-cost, tag=None)])
        adjacency[first].append(position)
        adjacency[second].append(position+1)

    exit_node = lambda owner: ('alpha', owner) if owner in alphas else ('out', owner)
    entry_node = lambda owner: ('beta', owner) if owner in betas else ('in', owner)
    for owner in sorted(alphas):
        add(source, exit_node(owner), 1, tag=('source', owner))
    for owner in sorted(mixed):
        add(('in', owner), ('out', owner), 1, tag=('mixed', owner))
    for owner in sorted(betas):
        add(entry_node(owner), sink, 1, tag=('beta', owner))
    for resource in sorted(resources):
        add(('interval', resource), sink, 1, tag=('interval', resource))
    large = len(alphas)+1
    for first, second in sorted(set(links)):
        if owners[first] != owners[second]:
            add(exit_node(owners[first]), entry_node(owners[second]), large,
                cost=1, tag=('link', first, second))
    for point in sorted(kinds):
        if kinds[point] == 'TP':
            for resource in sorted(access.get(point, set())):
                add(exit_node(owners[point]), ('interval', resource), large,
                    tag=('access', point, resource))
    nodes = set(adjacency) | {source, sink}
    value, cost = 0, 0
    while True:
        distance, parent = {source: 0}, {}
        for _ in range(len(nodes)-1):
            changed = False
            for position, edge in enumerate(edges):
                first, second = edge['first'], edge['second']
                if edge['residual'] and first in distance:
                    proposal = distance[first]+edge['cost']
                    if second not in distance or proposal < distance[second]:
                        distance[second], parent[second] = proposal, position
                        changed = True
            if not changed:
                break
        if sink not in distance:
            break
        cursor, used = sink, set()
        while cursor != source:
            assert cursor not in used
            used.add(cursor)
            position = parent[cursor]
            edges[position]['residual'] -= 1
            edges[position ^ 1]['residual'] += 1
            cursor = edges[position]['first']
        value += 1
        cost += distance[sink]
    reachable, pending = {source}, [source]
    while pending:
        vertex = pending.pop()
        for position in adjacency[vertex]:
            edge = edges[position]
            if edge['residual'] and edge['second'] not in reachable:
                reachable.add(edge['second'])
                pending.append(edge['second'])
    assert sink not in reachable
    assert value == sum(edge['initial'] for edge in edges[::2]
                        if edge['first'] in reachable and edge['second'] not in reachable)
    removed = {('mixed', owner) for owner in mixed
               if ('in', owner) in reachable and ('out', owner) not in reachable}
    removed |= {('beta', owner) for owner in betas if ('beta', owner) in reachable}
    removed |= {('interval', resource) for resource in resources
                if ('interval', resource) in reachable}
    blocked = blocked_sources(kinds, pairs, links, access, resources, removed)
    assert len(blocked)-len(removed) == len(alphas)-value
    remaining = {position: edge['initial']-edge['residual']
                 for position, edge in enumerate(edges) if position % 2 == 0}
    selected, payments, routes = [], [], []
    for position in adjacency[source]:
        if position % 2 or not remaining[position]:
            continue
        cursor, route, visited = source, [], set()
        while cursor != sink:
            assert cursor not in visited
            visited.add(cursor)
            candidate = next(index for index in adjacency[cursor]
                             if index % 2 == 0 and remaining[index] > 0)
            edge = edges[candidate]
            remaining[candidate] -= 1
            if edge['tag']:
                route.append(edge['tag'])
                if edge['tag'][0] == 'link':
                    selected.append(tuple(edge['tag'][1:]))
                if edge['tag'][0] == 'access':
                    payments.append(tuple(edge['tag'][1:]))
            cursor = edge['second']
        routes.append(route)
    assert all(amount == 0 for amount in remaining.values())
    assert len(routes) == value and len(selected) == cost
    reduced, inventory, _ = cancel_pairs(kinds, list(pairs), selected, Counter())
    final_alpha = [pair for pair in reduced if all(kinds[point] == 'TP' for point in pair)]
    assigned = set()
    for point, resource in payments:
        assert resource in access[point]
        owner = next(index for index, pair in enumerate(final_alpha) if point in pair)
        assert owner not in assigned
        assigned.add(owner)
    assert len({resource for point, resource in payments}) == len(payments)
    assert len(betas)-inventory['BP', 'BP']+len(payments) == value
    return dict(value=value, cost=cost, links=selected, payments=payments,
                routes=routes, cut=sorted(removed), blocked=sorted(blocked),
                deficit=len(alphas)-value)


def blocked_sources(kinds, pairs, links, access, resources, removed):
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    adjacency = defaultdict(set)
    for first, second in links:
        if owners[first] != owners[second]:
            adjacency[owners[first]].add(owners[second])
    forbidden = {owner for category, owner in removed if category in ('mixed', 'beta')}
    surviving = resources-{resource for category, resource in removed if category == 'interval'}
    exits = {owners[point] for point in kinds if kinds[point] == 'TP'
             and access.get(point, set()) & surviving}
    targets = exits | (betas-forbidden)
    blocked = set()
    for alpha in alphas:
        reached, pending = {alpha}, [alpha]
        while pending:
            owner = pending.pop()
            for other in adjacency[owner]-forbidden-reached:
                reached.add(other)
                pending.append(other)
        if not reached & targets:
            blocked.add(alpha)
    return blocked


def exhaustive(kinds, pairs, links, access, totals):
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    best, minimum = -1, None
    for selected in all_link_matchings(links):
        adjacency = defaultdict(set)
        used = {point for edge in selected for point in edge}
        for first, second in list(pairs)+selected:
            adjacency[first].add(second)
            adjacency[second].add(first)
        remaining, alpha_neighbours, final_beta = set(kinds), [], 0
        while remaining:
            reached, pending = {min(remaining)}, [min(remaining)]
            while pending:
                point = pending.pop()
                for other in adjacency[point]-reached:
                    reached.add(other)
                    pending.append(other)
            remaining -= reached
            tips = reached-used
            assert len(tips) in (0, 2)
            if tips and all(kinds[point] == 'BP' for point in tips):
                final_beta += 1
            if tips and all(kinds[point] == 'TP' for point in tips):
                alpha_neighbours.append(set().union(*(access.get(point, set()) for point in tips)))
        incidence = defaultdict(set)
        for demand, choices in enumerate(alpha_neighbours):
            for resource in choices:
                incidence[resource].add(demand)
        value = len(betas)-final_beta+independent_maximum(len(alpha_neighbours), incidence)
        if value > best or (value == best and len(selected) < minimum):
            best, minimum = value, len(selected)
        totals['independent_terminal_matchings'] += 1
    return best, minimum


def check(kinds, pairs, links, access, resources, totals, enumerate_links=True, enumerate_cuts=False):
    result = solve(kinds, pairs, links, access, resources)
    if enumerate_links:
        assert (result['value'], result['cost']) == exhaustive(kinds, pairs, links, access, totals)
        totals['exhaustive_normal_form_models'] += 1
    if enumerate_cuts:
        owners, alphas, betas, mixed = owner_data(kinds, pairs)
        options = [('mixed', owner) for owner in mixed]+[('beta', owner) for owner in betas]
        options += [('interval', resource) for resource in resources]
        maximum = 0
        for count in range(len(options)+1):
            for subset in itertools.combinations(options, count):
                removed = set(subset)
                blocked = blocked_sources(kinds, pairs, links, access, resources, removed)
                maximum = max(maximum, len(blocked)-len(removed))
                totals['independent_separator_subsets'] += 1
        assert maximum == result['deficit']
        totals['exhaustive_cut_models'] += 1
    totals['flow_models'] += 1
    totals['witness_routes'] += result['value']
    return result


def abstract(types):
    pairs = [(2*index, 2*index+1) for index in range(len(types))]
    kinds = {}
    for pair, kind in zip(pairs, types):
        kinds[pair[0]], kinds[pair[1]] = dict(alpha=('TP', 'TP'), beta=('BP', 'BP'),
                                             mixed=('BP', 'TP'))[kind]
    links = [(first, second) for first in kinds for second in kinds
             if kinds[first] == 'TP' and kinds[second] == 'BP']
    return kinds, pairs, links


def abstract_controls(totals):
    for count in range(1, 4):
        for types in itertools.combinations_with_replacement(('alpha', 'beta', 'mixed'), count):
            if 'alpha' not in types:
                continue
            kinds, pairs, candidates = abstract(types)
            tips = [point for point in kinds if kinds[point] == 'TP']
            for link_mask in range(1 << len(candidates)):
                links = [edge for index, edge in enumerate(candidates) if link_mask >> index & 1]
                for access_mask in range(1 << len(tips)):
                    access = {point: {0} if access_mask >> index & 1 else set()
                              for index, point in enumerate(tips)}
                    check(kinds, pairs, links, access, {0}, totals)
    generator = random.Random(20261023)
    for index in range(400):
        types = ('alpha',)+tuple(generator.choice(('alpha', 'beta', 'mixed'))
                                for _ in range(generator.randrange(1, 5)))
        kinds, pairs, candidates = abstract(types)
        links = [edge for edge in candidates if generator.random() < 0.3]
        resources = set(range(generator.randrange(4)))
        access = {point: {resource for resource in resources if generator.random() < 0.4}
                  for point in kinds if kinds[point] == 'TP'}
        check(kinds, pairs, links, access, resources, totals, enumerate_cuts=True)
    kinds, pairs, candidates = abstract(('alpha', 'alpha', 'mixed'))
    links = [(0, 4), (2, 4)]
    result = check(kinds, pairs, links, {5: {0, 1}}, {0, 1}, totals, enumerate_cuts=True)
    assert result['value'] == 1 and result['cut'] == [('mixed', 2)]
    assert result['blocked'] == [0, 1]
    assert not blocked_sources(kinds, pairs, links, {5: {0, 1}}, {0, 1}, set())
    bottleneck = result
    kinds, pairs, candidates = abstract(('alpha',)*4+('beta',))
    result = check(kinds, pairs, [(point, 8) for point in (0, 2, 4, 6)], {}, set(),
                   totals, enumerate_cuts=True)
    assert result['value'] == 1 and result['cost'] == 1
    return dict(shared_mixed_bottleneck=bottleneck, four_owner_beta=result)


def physical(current, bands, fixed, totals, enumerate_links=False, protected=False):
    original, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
    extended = extended_ports(current, bands, labels, intervals, owners, kinds, ports, Counter())
    reduced, inventory, _ = cancel_pairs(kinds, pairs, fixed, Counter())
    kinds = {point: kinds[point] for pair in reduced for point in pair}
    marked = {owners[band, 0] for band in range(len(bands))}
    marked |= {owners[band, len(columns)-1] for band, columns in enumerate(bands)
               if len(columns) % 2 == 0 and labels[band][-1] == ('B', 'B')}
    assert len(marked) == original['boundary_budget']
    resources = set(range(len(intervals)))-marked
    access = {point: {owners[port] for port in extended[point]} & resources
              for point in kinds if kinds[point] == 'TP'}
    if protected:
        alpha_pairs = [pair for pair in reduced if all(kinds[point] == 'TP' for point in pair)]
        incidence = {resource: {index for index, pair in enumerate(alpha_pairs)
                                if any(resource in access[point] for point in pair)}
                     for resource in resources}
        assignment = allocate(len(alpha_pairs), incidence)['assignment']
        excluded = {point for index in assignment for point in alpha_pairs[index]}
        reduced = [pair for pair in reduced if not set(pair) & excluded]
        kinds = {point: kind for point, kind in kinds.items() if point not in excluded}
        resources -= set(assignment.values())
        access = {point: choices & resources for point, choices in access.items() if point in kinds}
        totals['protected_paid_alpha_owners'] += len(assignment)
    links = [(first, second) for first in kinds for second in kinds
             if kinds[first] == 'TP' and kinds[second] == 'BP'
             and first[0] == second[0] and abs(first[1]-second[1]) == 1]
    result = check(kinds, reduced, links, access, resources, totals,
                   enumerate_links=enumerate_links)
    if not protected:
        unused = len(resources)+inventory['BP', 'BP']-result['value']
        assert original['surplus_twice']-2*original['boundary_budget'] == 2*(unused-result['deficit'])
    totals['physical_flow_models'] += 1
    return result


def physical_controls(totals):
    examples = []
    for width in (8, 12):
        for depth in (1, 2, 3, 8, 32, 64):
            current, bands, _ = relay_family(width, 4, depth, depth)
            direct_check(*current)
            force_matching(current, totals)
            result = physical(current, bands, [], totals, enumerate_links=depth <= 2)
            assert result['value'] == 1 and result['cost'] == depth
            examples.append(dict(family='relay', width=width, depth=depth,
                                 value=result['value'], cost=result['cost']))
    for width, count in itertools.product((6, 8, 12), (2, 3, 8, 24)):
        current, bands, fixed = chain_family(width, count)
        direct_check(*current)
        force_matching(current, totals)
        result = physical(current, bands, fixed, totals)
        assert result['value'] == count and result['cost'] == 1
        core = physical(current, bands, fixed, totals, protected=True)
        assert core['value'] == 1 and core['cost'] == 1
        examples.append(dict(family='shared_chain', width=width, count=count,
                             value=result['value'], cost=result['cost'], protected_cost=core['cost']))
    for width in (8, 12, 24):
        current, bands = collision_family(width)
        direct_check(*current)
        force_matching(current, totals)
        initial = [((5, 5), (5, 6))]
        left, right = ((5, 7), (5, 8)), ((5, 15), (5, 14))
        for name, extra in [('initial', []), ('left', [left]), ('right', [right]), ('both', [left, right])]:
            result = physical(current, bands, initial+extra, totals, enumerate_links=True)
            assert result['value'] == 2
            assert result['cost'] == (2 if name == 'initial' else 1)
            lower = [((width+4, 5), (width+4, 4)), ((width+4, 15), (width+4, 14))]
            repaired, _ = grid_allocation(current, bands, initial+extra+lower)
            assert repaired['assigned'] == 2 and repaired['defect'] == 0
            totals['explicit_lower_collision_repairs'] += 1
            if name == 'both':
                core = physical(current, bands, initial+extra, totals, protected=True)
                assert core['value'] == core['cost'] == 1
            examples.append(dict(family='donor_collision', width=width, state=name,
                                 value=result['value'], cost=result['cost']))
    for width, symmetry in itertools.product((6, 8, 12, 16), itertools.product((False, True), repeat=3)):
        current = transformed(*occupied_bands(width)[0], *symmetry)
        shape, selected, matching = current
        move = lambda point: (point[0]+2, point[1]+2)
        current = (2*((shape[0]+7)//2), 2*((shape[1]+7)//2),
                   {move(point) for point in selected}, [tuple(map(move, edge)) for edge in matching])
        direct_check(*current)
        force_matching(current, totals)
        result = physical(current, whole_bands(current), [], totals, enumerate_links=True)
        totals['occupied_band_flow_adapters'] += 1
        totals['occupied_band_nonempty_compensation'] += result['value'] > 0
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    abstract_examples = abstract_controls(totals)
    print(json.dumps(dict(stage='abstract', totals=dict(totals)), sort_keys=True), flush=True)
    examples = physical_controls(totals)
    record = dict(status='PASS', totals=dict(totals), abstract_examples=abstract_examples,
                  physical_examples=examples, scope='Independent terminal-matching and separator '
                  'enumeration checks the written exact compensation-flow normal form and minimum '
                  'link cost. General proofs remain written; no universal grid routing assertion.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
