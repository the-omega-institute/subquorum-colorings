"""Check low-congestion route covers, switching, and physical two-exit reserves."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data, solve
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_physical_joint_selection_parity_holes import family
from check_terminal_cancellation_and_stranded_demand import extended_ports, terminal_data


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def route_records(kinds, pairs, links, access):
    owners, sources, betas, mixed = owner_data(kinds, pairs)
    adjacency = defaultdict(list)
    for first, second in links:
        if owners[first] != owners[second]:
            adjacency[owners[first]].append((owners[second], (first, second)))
    exits = defaultdict(list)
    for point, resources in access.items():
        exits[owners[point]].extend((resource, point) for resource in resources)
    records = defaultdict(list)

    def visit(source, owner, visited, gates, arcs, cost):
        if owner in betas:
            resource = ('beta', owner)
            records[source].append(dict(source=source, units=frozenset(gates+[resource]),
                                        resource=resource, arcs=arcs+[('sink', resource)], cost=cost))
            return
        for interval, point in exits[owner]:
            resource = ('interval', interval)
            records[source].append(dict(source=source, units=frozenset(gates+[resource]),
                                        resource=resource,
                                        arcs=arcs+[('access', point, interval), ('sink', resource)], cost=cost))
        for target, edge in adjacency[owner]:
            if target in visited:
                continue
            assert target in mixed or target in betas
            unit = [('mixed', target)] if target in mixed else []
            visit(source, target, visited | {target}, gates+unit,
                  arcs+[('link', *edge)]+unit, cost+1)

    for source in sorted(sources):
        visit(source, source, {source}, [], [('source', source)], 0)
    return {source: records[source] for source in sorted(sources)}


def packings(routes):
    sources = list(routes)

    def extend(position, used, chosen):
        if position == len(sources):
            yield tuple(chosen)
            return
        yield from extend(position+1, used, chosen)
        for route in routes[sources[position]]:
            if not used & route['units']:
                yield from extend(position+1, used | route['units'], chosen+[route])

    yield from extend(0, frozenset(), [])


def counts(routes):
    units, arcs = Counter(), Counter()
    for route in routes:
        units.update(route['units'])
        arcs.update(route['arcs'])
    return units, arcs


def layer_decomposition(candidates, remaining, multiplicity, memo):
    if multiplicity == 0:
        return []
    key = multiplicity, frozenset(remaining.items())
    if key in memo:
        return None
    for packing in candidates:
        _, used = counts(packing)
        if all(amount <= remaining[arc] for arc, amount in used.items()):
            following = remaining-used
            suffix = layer_decomposition(candidates, following, multiplicity-1, memo)
            if suffix is not None:
                return [packing]+suffix
    memo.add(key)
    return None


def check_cover(routes, certificates, multiplicity, all_packings, optimum, totals):
    source_count = len(routes)
    assert Counter(route['source'] for route in certificates) == Counter({source: multiplicity for source in routes})
    loads, union_arcs = counts(certificates)
    excess = sum(max(0, amount-multiplicity) for amount in loads.values())
    assert multiplicity*(source_count-optimum['value']) <= excess
    totals['route_covers'] += 1
    if excess:
        totals['overloaded_cover_bounds'] += 1
        return
    full = [packing for packing in all_packings if len(packing) == source_count]
    assert optimum['value'] == source_count and full
    saturated = {unit for unit, amount in loads.items() if unit[0] != 'mixed' and amount == multiplicity}
    preserving = [packing for packing in full if saturated <= {route['resource'] for route in packing}]
    total_cost = sum(route['cost'] for route in certificates)
    assert preserving and multiplicity*min(sum(route['cost'] for route in packing) for packing in preserving) <= total_cost
    totals['complete_low_congestion_covers'] += 1
    totals['reserved_resource_cost_controls'] += 1
    if len(preserving) <= 64 and len(union_arcs) <= 24:
        layers = layer_decomposition(preserving, union_arcs, multiplicity, set())
        assert layers is not None and len(layers) == multiplicity
        _, combined = counts(route for packing in layers for route in packing)
        assert all(amount <= union_arcs[arc] for arc, amount in combined.items())
        assert sum(route['cost'] for packing in layers for route in packing) <= total_cost
        totals['complete_layer_decompositions'] += 1


def synthetic(source_count, mixed_count, beta_count, interval_count, generator):
    kinds, pairs = {}, []
    for owner in range(source_count+mixed_count+beta_count):
        pair = (2*owner, 2*owner+1)
        pairs.append(pair)
        kinds[pair[0]] = 'TP' if owner < source_count else 'BP'
        kinds[pair[1]] = 'BP' if owner >= source_count+mixed_count else 'TP'
    exits = {owner: 2*owner if owner < source_count else 2*owner+1
             for owner in range(source_count+mixed_count)}
    links = [(point, 2*target) for owner, point in exits.items()
             for target in range(source_count, len(pairs))
             if owner != target and generator.randrange(3) == 0]
    access = {point: {resource for resource in range(interval_count) if generator.randrange(3) == 0}
              for point in exits.values()}
    return kinds, pairs, links, access, set(range(interval_count))


def abstract_controls(totals):
    generator = random.Random(231039)
    for model in range(180):
        data = synthetic(1+model % 3, model % 3, (model//3) % 2, 1+(model//6) % 3, generator)
        routes = route_records(*data[:4])
        if any(not choices for choices in routes.values()):
            continue
        alternatives = list(packings(routes))
        optimum = solve(*data)
        maximum = max(map(len, alternatives))
        minimum_cost = min(sum(route['cost'] for route in packing) for packing in alternatives if len(packing) == maximum)
        assert (maximum, minimum_cost) == (optimum['value'], optimum['cost'])
        totals['independently_enumerated_networks'] += 1
        totals['independent_route_packings'] += len(alternatives)
        for multiplicity in (2, 3):
            for _ in range(18):
                certificates = [generator.choice(choices) for choices in routes.values() for _ in range(multiplicity)]
                check_cover(routes, certificates, multiplicity, alternatives, optimum, totals)


def switching_example(totals):
    kinds = {point: 'TP' if point < 4 or point % 2 else 'BP' for point in range(12)}
    pairs = [(point, point+1) for point in range(0, 12, 2)]
    links = [(0, 4), (0, 8), (2, 4), (2, 6), (5, 6), (5, 8), (7, 10), (9, 10)]
    access = {7: {0}, 11: {0, 1}, 9: {1}}
    routes = route_records(kinds, pairs, links, access)
    specifications = [(0, {2, 3}, 0), (0, {4, 5}, 0), (1, {2, 4}, 1), (1, {3, 5}, 1)]
    certificates = []
    for source, gates, resource in specifications:
        candidates = [route for route in routes[source]
                      if {unit[1] for unit in route['units'] if unit[0] == 'mixed'} == gates
                      and route['resource'] == ('interval', resource)]
        assert len(candidates) == 1
        certificates.append(candidates[0])
    assert all(first['units'] & second['units'] for first in certificates[:2] for second in certificates[2:])
    optimum = solve(kinds, pairs, links, access, {0, 1})
    check_cover(routes, certificates, 2, list(packings(routes)), optimum, totals)
    assert optimum['value'] == 2 and optimum['cost'] == 2
    totals['fixed_route_choice_obstructions_with_switching_repair'] += 1


def sharp_excess(totals):
    for source_count in range(2, 9):
        for multiplicity in (2, 3, 4):
            gate = source_count
            kinds = {point: 'TP' for point in range(2*source_count)}
            kinds.update({2*gate: 'BP', 2*gate+1: 'TP'})
            pairs = [(point, point+1) for point in range(0, 2*source_count+2, 2)]
            links = [(2*source, 2*gate) for source in range(source_count)]
            access = {2*gate+1: set(range(multiplicity*source_count))}
            routes = route_records(kinds, pairs, links, access)
            certificates = [next(route for route in routes[source]
                                 if route['resource'] == ('interval', multiplicity*source+choice))
                            for source in range(source_count) for choice in range(multiplicity)]
            optimum = solve(kinds, pairs, links, access, access[2*gate+1])
            loads, _ = counts(certificates)
            excess = sum(max(0, amount-multiplicity) for amount in loads.values())
            assert excess == multiplicity*(source_count-1) and optimum['value'] == 1
            totals['sharp_overload_families'] += 1


def physical_controls(totals):
    for width, depth, copies in itertools.product((6, 8, 12), (2, 3, 5), (1, 2)):
        current, _, _ = family(width, depth, copies)
        bands = whole_bands(current)
        _, labels, intervals, interval_owner, kinds, pairs, direct_ports = terminal_data(current, bands)
        access_columns = extended_ports(current, bands, labels, intervals, interval_owner, kinds, direct_ports, Counter())
        boundary = {index for index, interval in enumerate(intervals)
                    if interval['first'] == 0 or interval['last'] == current[1]-1}
        resources = set(range(len(intervals)))-boundary
        access = {point: {interval_owner[column] for column in choices}-boundary
                  for point, choices in access_columns.items()}
        links = [(first, second) for first in kinds if kinds[first] == 'TP'
                 for second in kinds if kinds[second] == 'BP' and first[0] == second[0]
                 and abs(first[1]-second[1]) == 1]
        routes = route_records(kinds, pairs, links, access)
        assert len(routes) == 2*copies and all(len(choices) == 2 for choices in routes.values())
        certificates = [route for choices in routes.values() for route in choices]
        loads, _ = counts(certificates)
        assert all(amount == 1 for amount in loads.values())
        assert all(route['cost'] == 2 and len(route['units']) == 3 for route in certificates)
        optimum = solve(kinds, pairs, links, access, resources)
        assert optimum['value'] == 2*copies and optimum['cost'] == 4*copies
        units = sorted(loads)
        failures = [frozenset(), *(frozenset([unit]) for unit in units)]
        if copies == 1:
            failures.extend(map(frozenset, itertools.combinations(units, 2)))
        for removed in failures:
            surviving = {source: [route for route in choices if not route['units'] & removed]
                         for source, choices in routes.items()}
            blocked = sum(not choices for choices in surviving.values())
            assert 2*blocked <= len(removed)
            modified_links = [(first, second) for first, second in links
                              if ('mixed', next(owner for owner, pair in enumerate(pairs) if second in pair)) not in removed]
            modified_access = {point: {unit for unit in choices if ('interval', unit) not in removed}
                               for point, choices in access.items()}
            result = solve(kinds, pairs, modified_links, modified_access,
                           {unit for unit in resources if ('interval', unit) not in removed})
            assert result['value'] == len(routes)-blocked and result['cost'] == 2*result['value']
            totals['physical_unit_reservation_controls'] += 1
        totals['physical_two_exit_families'] += 1
        totals['different_physical_route_units'] += len(units)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    abstract_controls(totals)
    switching_example(totals)
    sharp_excess(totals)
    physical_controls(totals)
    report = dict(status='PASS', totals=dict(totals),
                  scope='Independent finite route-packing enumeration versus min-cost flow; '
                        'two/three-fold low-congestion covers, prescribed saturated-resource preservation, '
                        'layer decomposition, sharp overload and fixed-route-choice obstruction; '
                        'real-grid two-exit routes and unavailable mixed/interval units. '
                        'General proofs and integral-flow decomposition are written, not inferred '
                        'from enumeration. No universal geometric route-cover existence or full flow Lean claim.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
