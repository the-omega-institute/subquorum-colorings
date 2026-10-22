"""Check physical coverage parity holes and the sharp half-progress barrier."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory
from check_full_domain_marker_compensation import full_signs
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_port_selection_matching import build_graph, edge_set, lift
from check_mixed_relay_orientation import forest_budget
from check_native_guard_compensation import force_matching
from check_port_choice_rematching_cost import candidate_graph
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, components, direct_family, extended_ports, terminal_data,
    uniform_certificates,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def pair_packet(width, depth, beta):
    assert width >= 6 and width % 2 == 0 and depth >= 2
    offset = 2*depth+4
    selected, actual, endpoints = set(), [], set()
    base = direct_family(width, 4)
    for index, reflected in enumerate((True, False)):
        def move(point):
            return point[0]+int(beta), (10-point[1] if reflected else point[1])+index*offset

        selected.update(map(move, base[2]))
        actual.extend(tuple(map(move, edge)) for edge in base[3])
        endpoints.update(move(point) for edge in base[3] for point in edge)
    corridors = [(6, 7), (width+5, width+4)] if beta else [(5, 4), (width+4, width+5)]
    for occupied_row, opposite in corridors:
        for column in range(8, offset+3):
            selected.add((occupied_row if column % 2 == 0 else opposite, column))
    if beta:
        route = [(6, offset+5), (6, offset+4), (7, offset+4),
                 (7, offset+3), (6, offset+3), (6, 7), (7, 7),
                 (7, 6), (6, 6), (6, 5)]
    else:
        route = [(5, 7), (5, offset+3)]
    return selected, actual, endpoints, route


def family(width, depth, copies):
    assert copies >= 1
    spacing = width+16
    selected, actual, blocks, routes = set(), [], [], []
    for index in range(2*copies):
        current_selected, current_actual, endpoints, route = pair_packet(width, depth, index % 2 == 1)

        def move(point):
            return point[0]+index*spacing, point[1]

        selected.update(map(move, current_selected))
        actual.extend(tuple(map(move, edge)) for edge in current_actual)
        blocks.append(set(map(move, endpoints)))
        routes.append(list(map(move, route)))
    return (2*copies*spacing, 2*depth+20, selected, actual), blocks, routes


def component_sizes(vertices, edges):
    adjacency = {point: set() for point in vertices}
    for first, second in map(tuple, edges):
        adjacency[first].add(second)
        adjacency[second].add(first)
    remaining, sizes = set(vertices), []
    while remaining:
        root = next(iter(remaining))
        reached, pending = {root}, [root]
        while pending:
            added = adjacency[pending.pop()]-reached
            reached.update(added)
            pending.extend(added)
        sizes.append(len(reached))
        remaining -= reached
    return sizes


def check(width, depth, copies, totals):
    current, blocks, routes = family(width, depth, copies)
    direct_check(*current)
    assert len(current[2]) == copies*(8*depth+40)
    assert len(current[3]) == 4*copies*(width+4)
    force_matching(current, totals)
    uniform_certificates(direct_family(width, 4), width, 4, totals)
    vertices = set().union(*blocks)
    bands = whole_bands(current)
    original, labels, intervals, interval_owner, kinds, pairs, direct_ports = terminal_data(current, bands)
    assert (original['alpha'], original['beta'], original['gamma']) == (2*copies, 2*copies, 12*copies)
    unmarked_intervals = len(intervals)-original['boundary_budget']
    assert unmarked_intervals == copies*((2*depth+14)*width+24*depth+232)
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*unmarked_intervals > 0
    sources = [pair for pair in pairs if all(kinds[point] == 'TP' for point in pair)]
    resources = [pair for pair in pairs if all(kinds[point] == 'BP' for point in pair)]
    relays = [pair for pair in pairs if {kinds[point] for point in pair} == {'TP', 'BP'}]
    internal = vertices-set(kinds)
    auxiliary = [tuple(column) for band in bands for column in band if set(column) <= internal]
    old = edge_set(auxiliary)
    candidates, portals, _ = candidate_graph(current, bands, labels, vertices)
    assert edge_set(current[3]+auxiliary) <= candidates
    assert len(portals) == 10*copies
    owner = {point: index for index, block in enumerate(blocks) for point in block}
    assert all(owner[first] == owner[second] for first, second in map(tuple, candidates))
    assert all(len(block) % 2 == 0 for block in blocks)
    for index, block in enumerate(blocks):
        local_sources = [pair for pair in sources if set(pair) <= block]
        local_resources = [pair for pair in resources if set(pair) <= block]
        assert (len(local_sources), len(local_resources)) == ((0, 2) if index % 2 else (2, 0))
        assert all(not set(pair) & block or set(pair) <= block for pair in relays)
    access = extended_ports(current, bands, labels, intervals, interval_owner,
                            kinds, direct_ports, totals)
    cancellations, payment_endpoints = [], []
    offset = 2*depth+4
    for index in range(copies):
        row = 5+2*index*(width+16)
        cancellations.extend([((row, 7), (row, 6)), ((row, 5), (row, 4)),
                              ((row, offset+3), (row, offset+4)),
                              ((row, offset+5), (row, offset+6))])
        payment_endpoints.extend([((row, 3), (row//2, 1)),
                                  ((row, offset+7), (row//2, offset+9))])
    reduced, after_cancel, _ = cancel_pairs(kinds, pairs, cancellations, totals)
    assert len(cancellations) == 4*copies
    assert edge_set(cancellations) <= candidates
    units = set()
    paid = set()
    for endpoint, column in payment_endpoints:
        assert column in access[endpoint]
        unit = interval_owner[column]
        assert unit not in units and intervals[unit]['first'] > 0
        assert intervals[unit]['last'] < current[1]-1
        units.add(unit)
        final_alpha = next(pair for pair in reduced if endpoint in pair)
        assert all(kinds[point] == 'TP' for point in final_alpha)
        assert frozenset(final_alpha) not in paid
        paid.add(frozenset(final_alpha))
    assert len(units) == len(paid) == after_cancel['TP', 'TP'] == 2*copies
    assert after_cancel['BP', 'BP'] == 2*copies
    assert after_cancel['BP', 'TP'] == 8*copies
    totals['complete_distinct_interval_repairs'] += 1
    totals['different_original_interval_payments'] += len(units)
    for selected in range(1, 2*copies, 2):
        graph_vertices, graph_edges = build_graph(internal, sources, resources, relays, candidates, selected)
        sizes = component_sizes(graph_vertices, graph_edges)
        assert sum(size % 2 for size in sizes) >= 2
        totals['odd_selector_empty_cut_tutte_witnesses'] += 1
    for active in range(copies+1):
        used_routes = routes[:2*active]
        added = [edge for route in used_routes for edge in zip(route[::2], route[1::2])]
        removed = edge_set(edge for route in used_routes for edge in zip(route[1:-1:2], route[2:-1:2]))
        assert removed <= old and edge_set(added) <= candidates-old
        following = [edge for edge in auxiliary if frozenset(edge) not in removed]+added
        covered = [point for edge in following for point in edge]
        assert len(covered) == len(set(covered))
        chosen = set(covered)-internal
        assert len(chosen) == 4*active and not chosen & {point for pair in relays for point in pair}
        lifted = lift(internal, sources, resources, relays, candidates, 2*active, following)
        assert len(lifted) > 0
        payments = {min(pair): index for index, pair in enumerate(sources) if not set(pair) & chosen}
        colours, cycles, _ = full_signs(vertices, current[3], auxiliary, kinds, chosen, payments)
        errors, rank = forest_budget(following, colours, cycles, {'alpha': 0})
        assert errors == rank == 2*active
        signs = dict(colours)
        for index in range(active):
            row = 6+(2*index+1)*(width+16)
            for column in (7, 2*depth+7):
                cycle = next(cycle for cycle in cycles if (row, column) in cycle)
                assert cycle == {(row, column), (row+1, column)}
                if signs[row, column] != 1:
                    signs.update({point: -signs[point] for point in cycle})
        negative = sum(signs[first] == signs[second] == -1 for first, second in following)
        positive = sum(signs[first] == signs[second] == 1 for first, second in following)
        assert negative == positive == active
        for block in blocks:
            selected_sources = sum(len(set(pair) & chosen) for pair in sources if set(pair) <= block)
            selected_resources = sum(len(set(pair) & chosen) for pair in resources if set(pair) <= block)
            local_negative = sum(first in block and signs[first] == signs[second] == -1
                                 for first, second in following)
            local_positive = sum(first in block and signs[first] == signs[second] == 1
                                 for first, second in following)
            assert selected_sources-selected_resources == 2*(local_negative-local_positive)
            totals['explicit_signed_block_identities'] += 1
        final = inventory(components(vertices, current[3]+following),
                          {point: kind for point, kind in kinds.items() if point not in chosen})
        assert (final['alpha'], final['beta'], final['mixed']) == (2*copies-active, 2*copies-active, 12*copies)
        assert len(edge_set(following)-old) == 6*active and len(old-edge_set(following)) == 4*active
        totals['explicit_even_cardinality_witnesses'] += 1
        totals['selector_lifts'] += 1
        totals['exact_forest_sign_witnesses'] += 1
    totals['physical_frozen_unique_families'] += 1
    totals['independent_even_vertex_blocks'] += len(blocks)
    totals['portal_edges_checked'] += len(portals)
    return dict(width=width, depth=depth, copies=copies,
                original=dict(alpha=2*copies, beta=2*copies, mixed=12*copies),
                feasible_r=list(range(0, 2*copies+1, 2)),
                packet_margin=unmarked_intervals,
                proof_scope='All infeasible odd r and lower bounds for arbitrary replacements, '
                            'including any complete mixed-pair activation, follow from the written '
                            'even-block and endpoint-inventory proof, not finite enumeration.')


def abstract_parity_controls(totals):
    for copies in range(1, 8):
        feasible = set()
        for source_flags in itertools.product(range(3), repeat=copies):
            if any(count % 2 for count in source_flags):
                continue
            for resource_flags in itertools.product(range(3), repeat=copies):
                if any(count % 2 for count in resource_flags):
                    continue
                if sum(source_flags) == sum(resource_flags):
                    feasible.add(sum(source_flags))
                    totals['block_selection_controls'] += 1
        assert feasible == set(range(0, 2*copies+1, 2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    abstract_parity_controls(totals)
    for width, depth, copies in itertools.product((6, 8, 12, 20), (2, 3, 6), (1, 2, 3)):
        result = check(width, depth, copies, totals)
        if len(examples) < 4 or (width, depth, copies) == (20, 6, 3):
            examples.append(result)
    report = dict(status='PASS', totals=dict(totals), examples=examples,
                  scope='Real feasible frozen uniquely matched rectangular-grid packets with '
                        'all endpoint grid edges and every all-BT gap edge; explicit even-r '
                        'coverage witnesses, selector lifts, actual odd-r empty-set Tutte witnesses, '
                        'explicit signed block identities and positive packet ledgers; complete '
                        'repairs by distinct old interval units through two mixed relays per source. '
                        'General parity exclusion, half-progress lower bound '
                        'and arbitrary mixed activation are written proofs. No general grid '
                        'inequality counterexample and no new Lean validation.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
