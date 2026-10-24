"""Check exact interval allocation with at most two demand owners per resource."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_arbitrary_depth_cap_relays import relay_family, shortest_access
from check_even_bridge_support_completion import endpoints_of
from check_native_guard_compensation import force_matching
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, direct_family, extended_ports, inspect_extended, terminal_data,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def allocate(demand_count, incidence):
    demands = set(range(demand_count))
    assert all(owners <= demands and len(owners) <= 2 for owners in incidence.values())
    adjacency = defaultdict(list)
    for resource, owners in incidence.items():
        if len(owners) == 2:
            first, second = sorted(owners)
            adjacency[first].append((second, resource))
            adjacency[second].append((first, resource))

    def spanning(root, excluded=None):
        reached, pending, parents = {root}, [root], {}
        while pending:
            vertex = pending.pop()
            for other, resource in adjacency[vertex]:
                if resource != excluded and other not in reached:
                    reached.add(other)
                    pending.append(other)
                    parents[other] = resource
        return reached, parents

    remaining, assignment, deficient = set(demands), {}, []
    while remaining:
        reached, parents = spanning(min(remaining))
        remaining -= reached
        resources = {resource for resource, owners in incidence.items() if owners & reached}
        extra = sorted(resources-set(parents.values()))
        if extra:
            chosen = extra[0]
            root = min(incidence[chosen])
            reached_again, parents = spanning(root, chosen)
            assert reached_again == reached
            assignment[root] = chosen
        else:
            assert len(resources) == len(reached)-1
            assert all(len(incidence[resource]) == 2 for resource in resources)
            deficient.append(dict(demands=sorted(reached), resources=sorted(resources)))
        assignment.update(parents)
    assert all(demand in incidence[resource] for demand, resource in assignment.items())
    assert len(set(assignment.values())) == len(assignment)
    assert len(assignment) == demand_count-len(deficient)
    return dict(assignment=assignment, deficient=deficient,
                spare_resources=sorted(set(incidence)-set(assignment.values())))


def independent_maximum(demand_count, incidence):
    neighbours = {demand: [resource for resource, owners in incidence.items() if demand in owners]
                  for demand in range(demand_count)}
    resource_owner = {}

    def augment(demand, seen):
        for resource in neighbours[demand]:
            if resource in seen:
                continue
            seen.add(resource)
            previous = resource_owner.get(resource)
            if previous is None or augment(previous, seen):
                resource_owner[resource] = demand
                return True
        return False

    for demand in range(demand_count):
        augment(demand, set())
    return len(resource_owner)


def grid_allocation(current, bands, links):
    original, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
    extended = extended_ports(current, bands, labels, intervals, owners, kinds, ports, Counter())
    reduced, inventory, _ = cancel_pairs(kinds, pairs, links, Counter())
    alphas = sorted(pair for pair in reduced if all(kinds[point] == 'TP' for point in pair))
    marked = {owners[band, 0] for band in range(len(bands))}
    marked |= {owners[band, len(columns)-1] for band, columns in enumerate(bands)
               if len(columns) % 2 == 0 and labels[band][-1] == ('B', 'B')}
    assert len(marked) == original['boundary_budget']
    incidence = {resource: set() for resource in range(len(intervals)) if resource not in marked}
    for demand, pair in enumerate(alphas):
        for point in pair:
            for port in extended[point]:
                resource = owners[port]
                if resource in incidence:
                    incidence[resource].add(demand)
    allocation = allocate(len(alphas), incidence)
    assert len(allocation['assignment']) == independent_maximum(len(alphas), incidence)
    defect, reserves = len(allocation['deficient']), len(allocation['spare_resources'])
    beta = inventory['BP', 'BP']
    margin = reserves+beta-defect
    assert 2*margin == original['surplus_twice']-2*original['boundary_budget']
    return dict(alpha=len(alphas), beta=beta, defect=defect, reserves=reserves,
                assigned=len(allocation['assignment']), margin=margin,
                incident_resources=Counter(map(len, incidence.values())),
                allocation=allocation), (original, kinds, pairs, extended, marked, owners)


def chain_family(width, count):
    assert width >= 6 and width % 2 == 0 and count >= 2
    selected, matching, links = set(), [], []
    last_row = width+4
    for index in range(count):
        base = direct_family(width, 4)
        move = lambda point: (point[0], point[1]+8*index)
        selected |= {move(point) for point in base[2]}
        matching.extend(tuple(map(move, edge)) for edge in base[3])
        states = {5: 'middle', last_row: 'middle'}
        if index:
            states[5 if (index-1) % 2 == 0 else last_row] = 'left'
        if index+1 < count:
            states[5 if index % 2 == 0 else last_row] = 'right'
        for row, state in states.items():
            if state != 'left':
                links.append((move((row, 3)), move((row, 4))))
            if state == 'right':
                links.append((move((row, 5)), move((row, 6))))
    current = width+12, 8*count+12, selected, matching
    bands = [[((row, column), (row+1, column)) for column in range(8*count+2)]
             for row in range(4, width+5, 2)]
    return current, bands, links


def chain_control(width, count, totals):
    current, bands, links = chain_family(width, count)
    direct_check(*current)
    force_matching(current, totals)
    cells = {point for band in bands for column in band for point in column}
    assert current[2] | endpoints_of(current) <= cells
    assert len(current[2]) == 13*count and len(current[3]) == (width+4)*count
    uncancelled, _ = grid_allocation(current, bands, [])
    assert uncancelled['assigned'] == count and uncancelled['defect'] == 0
    before, _ = grid_allocation(current, bands, links)
    assert len(links) == 2*count
    assert before['alpha'] == count and before['beta'] == 0
    assert before['defect'] == 1 and before['assigned'] == count-1
    assert before['incident_resources'][2] == count-1 and before['incident_resources'][1] == 0
    witness = before['allocation']['deficient'][0]
    assert len(witness['demands']) == count and len(witness['resources']) == count-1
    additional = ((width+4, 5), (width+4, 6))
    after, _ = grid_allocation(current, bands, links+[additional])
    assert after['defect'] == 0 and after['assigned'] == count
    assert after['incident_resources'][2] == count-1 and after['incident_resources'][1] == 1
    assert before['margin'] == after['margin'] == (3*width-9)*count
    old_connector = inspect_extended(current, bands, links, Counter())
    new_connector = inspect_extended(current, bands, links+[additional], Counter())
    assert old_connector['omitted'] == 2 and new_connector['omitted'] == 1
    assert old_connector.get('h2', 0) == new_connector.get('h2', 0) == 0
    totals['frozen_chain_families'] += 1
    totals['chain_demands_paid_after_one_link'] += count
    return dict(width=width, count=count, margin=after['margin'],
                before=dict(assigned=before['assigned'], deficit=before['defect']),
                after=dict(assigned=after['assigned'], deficit=after['defect']),
                omitted_two_sided_connectors_after=new_connector['omitted'])


def relay_control(depth, totals):
    current, bands, move = relay_family(8, 4, depth, depth)
    original, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
    extended = extended_ports(current, bands, labels, intervals, owners, kinds, ports, Counter())
    marked = {owners[band, column] for band in range(len(bands))
              for column in (0, len(bands[band])-1)}
    unmarked_ports = {point: [port for port in choices if owners[port] not in marked]
                      for point, choices in extended.items()}
    choices = [(first, second) for first in kinds for second in kinds
               if kinds[first] == 'TP' and kinds[second] == 'BP' and first[0] == second[0]
               and abs(first[1]-second[1]) == 1]
    assert min(shortest_access(row, move((row, 3)), kinds, pairs, choices, unmarked_ports)
               for row in (5, 12)) == depth
    left = [(move((5, 5-2*index)), move((5, 4-2*index))) for index in range(1, depth+1)]
    right = lambda row: [(move((row, 3)), move((row, 4))), (move((row, 5)), move((row, 6)))]
    one_sided, _ = grid_allocation(current, bands, left)
    assert one_sided['assigned'] == 1 and one_sided['defect'] == 0
    assert inspect_extended(current, bands, left, Counter())['omitted'] == 1
    both_right = inspect_extended(current, bands, right(5)+right(12), Counter())
    assert both_right['omitted'] == 0 and both_right['h2'] == 1
    two_sided = inspect_extended(current, bands, left+right(12), Counter())
    assert two_sided['omitted'] == two_sided.get('h2', 0) == 0
    totals['fixed_height_payment_distance_controls'] += 1
    return dict(depth=depth, dimensions=[10, 2*depth+10], minimum_two_end_access=4,
                minimum_one_interval_assignment=depth,
                minimum_two_end_collision_free_compensation=depth+2)


def physical_cycle_control(width, totals):
    current, bands, _ = chain_family(width, 2)
    links = [((row, column), (row, column+1))
             for row in (5, width+4) for column in (3, 5)]
    allocation, _ = grid_allocation(current, bands, links)
    assert allocation['alpha'] == allocation['assigned'] == 2
    assert allocation['defect'] == 0
    assert allocation['incident_resources'][2] == 2
    assert allocation['incident_resources'][1] == 0
    connector = inspect_extended(current, bands, links, Counter())
    assert connector['cycles'] == 1 and connector['omitted'] == connector.get('h2', 0) == 0
    assert connector['h0'] == allocation['margin'] == 2*(3*width-9)
    totals['physical_parallel_cycle_controls'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for incidence, expected in (
            ({('beta', 0): {0, 1}}, 1),
            ({('beta', 0): {0, 1}, ('interval', 0): {0}}, 2),
            ({('beta', 0): {0, 1}, ('interval', 0): {0, 1}}, 2)):
        result = allocate(2, incidence)
        assert len(result['assignment']) == expected
        assert len(set(result['assignment'].values())) == expected
        totals['labelled_whole_beta_interval_controls'] += 1
    for demand_count in range(5):
        options = [set()]+[{demand} for demand in range(demand_count)]
        options += [set(pair) for pair in itertools.combinations(range(demand_count), 2)]
        for resource_count in range(5):
            for owners in itertools.product(options, repeat=resource_count):
                incidence = dict(enumerate(owners))
                result = allocate(demand_count, incidence)
                assert len(result['assignment']) == independent_maximum(demand_count, incidence)
                totals['exhaustive_abstract_incidence_models'] += 1
    for width, count in itertools.product((6, 8, 10, 16), range(2, 25)):
        record = chain_control(width, count, totals)
        if (width, count) in ((6, 2), (8, 3), (16, 24)):
            examples.append(record)
    relay_examples = [relay_control(depth, totals) for depth in (3, 4, 8, 16, 32, 64)]
    for width in range(6, 27, 2):
        physical_cycle_control(width, totals)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals),
        chain_examples=examples, relay_examples=relay_examples,
        scope='Finite controls support the written resource-degree-two allocation proof. '
              'No universal grid bound or general route-existence theorem is claimed.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
