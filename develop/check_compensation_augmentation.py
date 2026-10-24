"""Check support-preserving augmentation from arbitrary route packings."""

import argparse
from collections import Counter, defaultdict, deque
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import (
    abstract, blocked_sources, exhaustive, owner_data, solve,
)
from check_one_sided_interval_allocation import chain_family
from check_terminal_cancellation_and_stranded_demand import (
    all_link_matchings, cancel_pairs, extended_ports, terminal_data,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


class Network:
    def __init__(self, kinds, pairs, links, access, resources):
        self.kinds, self.pairs = kinds, pairs
        self.access, self.resources = access, resources
        owners, self.alphas, self.betas, mixed = owner_data(kinds, pairs)
        self.source, self.sink = ('source',), ('sink',)
        self.edges, self.adjacency, self.by_tag = [], defaultdict(list), {}
        for owner in sorted(self.alphas):
            self.add(self.source, ('alpha', owner), 1, ('source', owner))
        for owner in sorted(mixed):
            self.add(('in', owner), ('out', owner), 1, ('mixed', owner))
        for owner in sorted(self.betas):
            self.add(('beta', owner), self.sink, 1, ('beta', owner))
        for resource in sorted(resources):
            self.add(('interval', resource), self.sink, 1, ('interval', resource))
        for first, second in sorted(set(links)):
            assert kinds[first] == 'TP' and kinds[second] == 'BP'
            if owners[first] == owners[second]:
                continue
            tail = ('alpha', owners[first]) if owners[first] in self.alphas else ('out', owners[first])
            head = ('beta', owners[second]) if owners[second] in self.betas else ('in', owners[second])
            self.add(tail, head, len(self.alphas)+1, ('link', first, second))
        for point in sorted(access):
            assert kinds[point] == 'TP' and set(access[point]) <= resources
            tail = ('alpha', owners[point]) if owners[point] in self.alphas else ('out', owners[point])
            for resource in sorted(access[point]):
                self.add(tail, ('interval', resource), len(self.alphas)+1,
                         ('access', point, resource))

    def add(self, tail, head, capacity, tag):
        index = len(self.edges)
        assert tag not in self.by_tag
        self.by_tag[tag] = index
        self.edges.append((tail, head, capacity, tag))
        self.adjacency[tail].append((index, 1, head))
        self.adjacency[head].append((index, -1, tail))

    def supports(self, flow):
        sources, resources = set(), set()
        for amount, (_, _, _, tag) in zip(flow, self.edges):
            if amount and tag[0] == 'source':
                sources.add(tag[1])
            if amount and tag[0] in ('beta', 'interval'):
                resources.add(tag)
        return sources, resources

    def feasible(self, flow):
        balance = Counter()
        for amount, (tail, head, capacity, _) in zip(flow, self.edges):
            assert isinstance(amount, int) and 0 <= amount <= capacity
            balance[tail] -= amount
            balance[head] += amount
        assert all(value == 0 for node, value in balance.items()
                   if node not in (self.source, self.sink))
        sources, resources = self.supports(flow)
        assert -balance[self.source] == balance[self.sink] == len(sources) == len(resources)

    def paths(self, flow=None, start=None):
        start = self.source if start is None else start

        def visit(node, seen, route):
            if node == self.sink:
                yield route
                return
            for index, direction, other in self.adjacency[node]:
                if direction != 1 or other in seen or (flow is not None and not flow[index]):
                    continue
                yield from visit(other, seen | {other}, route+[index])

        return visit(start, {start}, [])

    def all_packings(self):
        choices = defaultdict(list)
        for route in self.paths():
            choices[self.edges[route[0]][3][1]].append(route)
        sources = sorted(self.alphas)

        def extend(position, flow):
            if position == len(sources):
                yield flow
                return
            yield from extend(position+1, flow)
            for route in choices[sources[position]]:
                if all(flow[index] < self.edges[index][2] for index in route):
                    following = flow.copy()
                    for index in route:
                        following[index] += 1
                    yield from extend(position+1, following)

        return extend(0, [0]*len(self.edges))

    def normalize(self, flow):
        remaining, normalized, routes = flow.copy(), [0]*len(flow), []
        while True:
            route = next(self.paths(remaining), None)
            if route is None:
                break
            for index in route:
                remaining[index] -= 1
                normalized[index] += 1
            routes.append([self.edges[index][3] for index in route])
        assert self.supports(flow) == self.supports(normalized)
        self.feasible(normalized)
        return normalized, routes

    def certificate(self, flow):
        normalized, routes = self.normalize(flow)
        selected = [tuple(tag[1:]) for route in routes for tag in route if tag[0] == 'link']
        terminals = [point for edge in selected for point in edge]
        assert len(terminals) == len(set(terminals))
        payments = [tuple(tag[1:]) for route in routes for tag in route if tag[0] == 'access']
        assert len({resource for _, resource in payments}) == len(payments)
        reduced, inventory, _ = cancel_pairs(self.kinds, self.pairs, selected, Counter())
        alphas = [pair for pair in reduced if all(self.kinds[point] == 'TP' for point in pair)]
        paid = set()
        for point, resource in payments:
            assert resource in self.access[point]
            owner = next(index for index, pair in enumerate(alphas) if point in pair)
            assert owner not in paid
            paid.add(owner)
        assert len(self.betas)-inventory['BP', 'BP']+len(payments) == len(routes)
        return normalized, routes

    def augment(self, initial, optimum, totals):
        flow, routes = self.certificate(initial)
        initial_sources, initial_resources = self.supports(flow)
        reverse = Counter()
        while True:
            parent, pending = {self.source: None}, deque([self.source])
            while pending and self.sink not in parent:
                node = pending.popleft()
                for index, direction, other in self.adjacency[node]:
                    capacity = self.edges[index][2]
                    available = flow[index] < capacity if direction == 1 else flow[index] > 0
                    if available and other not in parent:
                        parent[other] = (node, index, direction)
                        pending.append(other)
            if self.sink not in parent:
                cut = sum(capacity for tail, head, capacity, _ in self.edges
                          if tail in parent and head not in parent)
                assert cut == len(routes) == optimum
                break
            old_sources, old_resources = self.supports(flow)
            cursor, seen = self.sink, {self.sink}
            while cursor != self.source:
                previous, index, direction = parent[cursor]
                assert previous not in seen
                seen.add(previous)
                if direction == -1:
                    category = self.edges[index][3][0]
                    assert category not in ('source', 'beta', 'interval')
                    reverse[category] += 1
                flow[index] += direction
                cursor = previous
            self.feasible(flow)
            flow, routes = self.certificate(flow)
            new_sources, new_resources = self.supports(flow)
            assert old_sources < new_sources and old_resources < new_resources
            assert len(new_sources-old_sources) == len(new_resources-old_resources) == 1
            totals['verified_augmentations'] += 1
        final_sources, final_resources = self.supports(flow)
        assert initial_sources <= final_sources and initial_resources <= final_resources
        totals['initial_packings'] += 1
        totals.update({'reverse_'+category+'_steps': amount for category, amount in reverse.items()})
        return dict(value=len(routes), routes=routes, reverse=dict(reverse))


def abstract_controls(totals):
    for types in [('alpha', 'alpha', 'mixed'), ('alpha', 'alpha', 'beta')]:
        kinds, pairs, candidates = abstract(types)
        candidates = [edge for edge in candidates if edge not in pairs and edge[::-1] not in pairs]
        tips = [point for point in kinds if kinds[point] == 'TP']
        for link_mask in range(1 << len(candidates)):
            links = [edge for index, edge in enumerate(candidates) if link_mask >> index & 1]
            for access_mask in range(1 << len(tips)):
                access = {point: {0} if access_mask >> index & 1 else set()
                          for index, point in enumerate(tips)}
                network = Network(kinds, pairs, links, access, {0})
                best, _ = exhaustive(kinds, pairs, links, access, totals)
                for flow in network.all_packings():
                    network.augment(flow, best, totals)
                totals['exhaustive_models'] += 1
    generator = random.Random(20261023)
    for _ in range(160):
        types = ('alpha', 'alpha')+tuple(generator.choice(('alpha', 'beta', 'mixed'))
                                         for _ in range(generator.randrange(1, 5)))
        kinds, pairs, candidates = abstract(types)
        links = [edge for edge in candidates if generator.random() < 0.25]
        resources = set(range(generator.randrange(1, 4)))
        access = {point: {resource for resource in resources if generator.random() < 0.35}
                  for point in kinds if kinds[point] == 'TP'}
        network = Network(kinds, pairs, links, access, resources)
        optimum = solve(kinds, pairs, links, access, resources)['value']
        paths = list(network.paths())
        for _ in range(8):
            generator.shuffle(paths)
            flow = [0]*len(network.edges)
            for route in paths:
                if generator.random() < 0.5 and all(flow[index] < network.edges[index][2] for index in route):
                    for index in route:
                        flow[index] += 1
            network.augment(flow, optimum, totals)
        totals['random_models'] += 1


def replacement_control(totals):
    kinds, pairs, _ = abstract(('alpha', 'alpha', 'mixed'))
    links, access = [(0, 4), (2, 4)], {5: {0}, 1: {1}}
    network = Network(kinds, pairs, links, access, {0, 1})
    initial = [0]*len(network.edges)
    for tag in [('source', 0), ('link', 0, 4), ('mixed', 2), ('access', 5, 0), ('interval', 0)]:
        initial[network.by_tag[tag]] = 1
    result = network.augment(initial, 2, totals)
    assert result['reverse']['link'] == 1
    final_links = {tuple(tag[1:]) for route in result['routes'] for tag in route if tag[0] == 'link'}
    assert final_links == {(2, 4)}
    fixed_index = network.by_tag['link', 0, 4]
    assert max(len(network.supports(flow)[0]) for flow in network.all_packings()
               if flow[fixed_index]) == 1
    totals['fixed_selected_link_obstructions'] += 1
    return result


def cost_control(totals):
    kinds, pairs, _ = abstract(('alpha', 'mixed'))
    links, access = [(0, 2)], {3: {0}, 1: {1}}
    network = Network(kinds, pairs, links, access, {0, 1})
    costs = []
    for flow in network.all_packings():
        sources, resources = network.supports(flow)
        if len(sources) == 1 and ('interval', 0) in resources:
            costs.append(sum(amount for amount, edge in zip(flow, network.edges)
                             if edge[3][0] == 'link'))
    assert costs and min(costs) == 1
    free = solve(kinds, pairs, links, access, {0, 1})
    assert free['value'] == 1 and free['cost'] == 0
    totals['unrestricted_cost_incompatible_with_old_support'] += 1


def finite_frontier(kinds, pairs, links, access, shared, count, totals):
    old_owner = {resource: index for index, resource in enumerate(shared)}
    attained = set()
    for selected in all_link_matchings(links):
        reduced, inventory, _ = cancel_pairs(kinds, pairs, selected, Counter())
        alphas = [pair for pair in reduced if all(kinds[point] == 'TP' for point in pair)]
        assert len(alphas) == count and inventory['BP', 'BP'] == 0
        assert all(all(8*index+3 <= point[1] <= 8*index+7 for point in pair)
                   for index, pair in enumerate(alphas))
        incidence = [set().union(*(access[point] for point in pair)) for pair in alphas]

        def assign(position, used, changes):
            if position == count:
                attained.add((len(selected), changes))
                totals['independent_full_interval_allocations'] += 1
                return
            for resource in incidence[position]-used:
                changed = resource in old_owner and old_owner[resource] != position
                assign(position+1, used | {resource}, changes+changed)

        assign(0, set(), 0)
        totals['independent_arbitrary_chain_link_matchings'] += 1
    frontier = {pair for pair in attained if not any(
        other != pair and other[0] <= pair[0] and other[1] <= pair[1] for other in attained)}
    expected = {(1, 1)} if count == 2 else {(1, count-1), (2, 1)}
    assert frontier == expected
    totals['exhaustive_physical_pareto_frontiers'] += 1
    return sorted(frontier)


def circulation_control(totals):
    kinds, pairs, _ = abstract(('alpha', 'mixed', 'mixed'))
    network = Network(kinds, pairs, [(3, 4), (5, 2)], {0: {0}}, {0})
    flow = [0]*len(network.edges)
    tags = [('source', 0), ('access', 0, 0), ('interval', 0),
            ('mixed', 1), ('link', 3, 4), ('mixed', 2), ('link', 5, 2)]
    for tag in tags:
        flow[network.by_tag[tag]] = 1
    network.feasible(flow)
    normalized, routes = network.certificate(flow)
    assert network.supports(normalized) == network.supports(flow)
    assert len(routes) == 1
    assert sum(flow)-sum(normalized) == 4
    assert all(normalized[network.by_tag[tag]] == 0 for tag in tags[3:])
    totals['nonzero_circulation_cleanup_fixtures'] += 1
    totals['circulation_arc_units_discarded'] += 4


def physical_controls(totals):
    examples = []
    for width, count in itertools.product((6, 8, 12), range(2, 25)):
        current, bands, fixed = chain_family(width, count)
        _, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
        extended = extended_ports(current, bands, labels, intervals, owners, kinds, ports, Counter())
        reduced, _, _ = cancel_pairs(kinds, pairs, fixed, Counter())
        kinds = {point: kinds[point] for pair in reduced for point in pair}
        marked = {owners[band, column] for band in range(len(bands))
                  for column in (0, len(bands[band])-1)}
        resources = set(range(len(intervals)))-marked
        access = {point: {owners[port] for port in extended[point]} & resources
                  for point in kinds if kinds[point] == 'TP'}
        links = [(first, second) for first in kinds for second in kinds
                 if kinds[first] == 'TP' and kinds[second] == 'BP'
                 and first[0] == second[0] and abs(first[1]-second[1]) == 1]
        root_link = ((width+4, 5), (width+4, 6))
        assert root_link in links
        _, alpha_owners, _, _ = owner_data(kinds, reduced)
        assert len(alpha_owners) == count
        assert all(all(8*index+3 <= point[1] <= 8*index+7 for point in reduced[owner])
                   for index, owner in enumerate(sorted(alpha_owners)))
        last_owner = max(alpha_owners)
        last_shared = owners[0 if (count-2) % 2 == 0 else len(bands)-1, 9+8*(count-2)]
        assert last_owner not in blocked_sources(kinds, reduced, links, access, resources, set())
        assert last_owner in blocked_sources(kinds, reduced, links, access, resources,
                                             {('interval', last_shared)})
        totals['unrestricted_last_resource_separator_certificates'] += 1
        if width == 6 and count <= 3:
            shared = [owners[0 if index % 2 == 0 else len(bands)-1, 9+8*index]
                      for index in range(count-1)]
            frontier = finite_frontier(kinds, reduced, links, access, shared, count, totals)
            examples.append(dict(width=width, count=count, exact_enumerated_frontier=frontier))
        for mode, permitted in [('all_links', links), ('root_link_only', [root_link])]:
            network = Network(kinds, reduced, permitted, access, resources)
            alpha_owners = sorted(network.alphas)
            initial = [0]*len(network.edges)
            for index in range(count-1):
                resource = owners[0 if index % 2 == 0 else len(bands)-1, 9+8*index]
                owner = alpha_owners[index]
                point = next(point for point in reduced[owner] if resource in access[point])
                for tag in [('source', owner), ('access', point, resource), ('interval', resource)]:
                    initial[network.by_tag[tag]] = 1
            result = network.augment(initial, count, totals)
            if mode == 'root_link_only':
                assert result['reverse']['access'] == count-1
                assert sum(tag[0] == 'link' for route in result['routes'] for tag in route) == 1
            totals['physical_last_root_augmentations'] += 1
            if (width, count) in ((6, 2), (8, 3), (12, 24)):
                examples.append(dict(width=width, count=count, mode=mode,
                                     reversed_old_accesses=result['reverse'].get('access', 0),
                                     final_value=result['value']))
        totals['physical_last_root_chains'] += 1
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    abstract_controls(totals)
    replacement = replacement_control(totals)
    cost_control(totals)
    circulation_control(totals)
    examples = physical_controls(totals)
    record = dict(status='PASS', totals=dict(totals), reverse_link_example=replacement,
                  physical_examples=examples, scope='Finite validation of arbitrary-initial-packing '
                  'augmentation, nested paid-source/resource supports, actual terminal matching '
                  'and single resource use. General theorem is written; no universal grid budget claim.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
