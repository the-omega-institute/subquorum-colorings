#!/usr/bin/env python3
"""Coordinate and abstract controls for exact exterior-component port budgets."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_cross_component_compensation import witness_record
from check_mixed_band_boundary_obstacle import capacity_two, closure_control, configuration, general_region_ledger, regions
from check_neutral_attachment_normalization import eligible
from check_residual_corridors import direct_check, graph_record, transformed
from verify_grid_short_path_compensation import pairs


def component_budgets(current, exterior):
    graph, _ = graph_record(*current)
    assert all(graph['t'][tile] < 2 for tile in exterior)
    pending = set(exterior)
    records = []
    while pending:
        start = min(pending)
        pending.remove(start)
        tiles = {start}
        queue = [start]
        while queue:
            tile = queue.pop()
            for neighbor, _ in graph['neighbors'][tile]:
                if neighbor in pending:
                    pending.remove(neighbor)
                    tiles.add(neighbor)
                    queue.append(neighbor)
        internal = sum(first in tiles and second in tiles for first, second in graph['E'])
        crossing = [(first, second) if first in tiles else (second, first)
                    for first, second in graph['E'] if (first in tiles) != (second in tiles)]
        ports = len(crossing)
        zero = sum(graph['r'][tile] == 0 for tile in tiles)
        two = sum(graph['r'][tile] == 2 for tile in tiles)
        rank = internal-len(tiles)+1
        assert rank >= 0
        balance = 1+two-zero-rank
        charge_twice = sum(graph['deg'][tile]-2*graph['r'][tile] for tile in tiles)
        assert charge_twice == ports-2*balance
        vertices = {divmod(vertex, current[1]) for tile in tiles for vertex in graph['vertices'][tile]}
        assert general_region_ledger(current, vertices)['charge_twice'] == charge_twice
        shortfall = ports-balance
        assert ports+charge_twice == 2*shortfall
        assert (shortfall <= 0) == (-charge_twice >= ports)
        records.append(dict(tiles=sorted(tiles), internal_edges=internal, ports=ports,
                            port_edges=crossing, capacity_zero=zero, capacity_two=two,
                            cycle_rank=rank, balance=balance, charge_twice=charge_twice,
                            signed_shortfall=shortfall))
    return records


def tile_set(current, vertices):
    return {row//2*(current[1]//2)+column//2 for row, column in vertices}


def bent_receiver(length, variation='two_ports'):
    if length < 2:
        raise ValueError('Require length at least two.')
    matching = [((1, 2), (2, 2))]
    matching.extend(((3, 2*column), (3, 2*column+1)) for column in range(1, length))
    matching.extend(((2, 2*column+1), (2, 2*column+2)) for column in range(1, length))
    matching.extend((((2, 2*length+1), (3, 2*length+1)),
                     ((3, 2*length), (4, 2*length)),
                     ((5, 2*length), (5, 2*length+1)),
                     ((4, 2*length+1), (4, 2*length+2))))
    if variation == 'capacity_two':
        matching.remove(((3, 2), (3, 3)))
    elif variation == 'one_port':
        matching.remove(((4, 2*length+1), (4, 2*length+2)))
    elif variation != 'two_ports':
        raise ValueError('Unknown variation.')
    current = 8, 2*length+4, set(), matching
    vertices = {(row, column) for row in (2, 3) for column in range(2, 2*length+2)}
    vertices.update((row, column) for row in (4, 5) for column in (2*length, 2*length+1))
    return current, vertices


def cyclic_receiver(repaired=False):
    matching = [((2, 3), (2, 4)), ((3, 3), (3, 4)),
                ((2, 5), (3, 5)), ((2, 1), (2, 2)), ((3, 1), (3, 2))]
    if repaired:
        matching.remove(((2, 5), (3, 5)))
    return (6, 8, set(), matching), {(row, column) for row in (2, 3) for column in range(2, 6)}


def abstract_controls():
    controls = 0
    for size in range(1, 4):
        pairs_list = list(itertools.combinations(range(size), 2))
        for multiplicities in itertools.product(range(3), repeat=len(pairs_list)):
            edges = [edge for edge, count in zip(pairs_list, multiplicities) for _ in range(count)]
            reached = {0}
            while True:
                extended = reached | {endpoint for edge in edges if reached.intersection(edge) for endpoint in edge}
                if extended == reached:
                    break
                reached = extended
            if len(reached) != size:
                continue
            degrees = [sum(vertex in edge for edge in edges) for vertex in range(size)]
            for capacities in itertools.product(range(3), repeat=size):
                for ports in itertools.product(range(3), repeat=size):
                    if any(degree+port > (2*capacity if capacity else 1)
                           for degree, port, capacity in zip(degrees, ports, capacities)):
                        continue
                    total_ports = sum(ports)
                    charge_twice = sum(degree+port-2*capacity
                                       for degree, port, capacity in zip(degrees, ports, capacities))
                    rank = len(edges)-size+1
                    balance = 1+capacities.count(2)-capacities.count(0)-rank
                    assert charge_twice == total_ports-2*balance
                    assert (total_ports <= balance) == (charge_twice <= -total_ports)
                    controls += 1
    return controls


def exhaustive_controls():
    records = []
    for rows, columns in ((2, 2), (2, 4), (4, 2), (2, 6), (6, 2)):
        count = subsets = components = 0
        for mask, matching in pairs(rows, columns):
            selected = {divmod(vertex, columns) for vertex in range(rows*columns) if mask >> vertex & 1}
            current = rows, columns, selected, [tuple(divmod(vertex, columns) for vertex in edge)
                                                for edge in matching]
            graph, _ = graph_record(*current)
            deficient = [tile for tile in range(graph['N']) if graph['t'][tile] < 2]
            for subset in range(1, 1 << len(deficient)):
                exterior = {tile for index, tile in enumerate(deficient) if subset >> index & 1}
                records_for_subset = component_budgets(current, exterior)
                assert sum(record['charge_twice'] for record in records_for_subset) == sum(
                    graph['deg'][tile]-2*graph['r'][tile] for tile in exterior)
                components += len(records_for_subset)
                subsets += 1
            count += 1
        records.append(dict(shape=[rows, columns], feasible_pairs=count,
                            deficient_subsets=subsets, component_checks=components))
    return records


def family_control(modules, flipped):
    current = configuration(modules)
    if flipped:
        current = capacity_two(current)
    patch_regions = regions(current)
    patch = set().union(*(patch_regions[name] for name in ('source', 'parent', 'child')))
    patch_tiles = tile_set(current, patch)
    graph, _ = graph_record(*current)
    exterior = {tile for tile in range(graph['N']) if graph['t'][tile] < 2 and tile not in patch_tiles}
    components = component_budgets(current, exterior)
    incident = [record for record in components if record['ports']]
    remainder = [record for record in components if not record['ports']]
    closure_edges = {frozenset(edge) for edge in current[3]
                     if {edge[0][0], edge[1][0]} == {5, 6} and edge[0][1] in range(2, current[1]-2)}
    residual_crossings = {frozenset(endpoints) for edge, endpoints in zip(graph['E'], graph['ends'])
                          if (edge[0] in patch_tiles) != (edge[1] in patch_tiles)}
    coordinate_crossings = {frozenset(first*current[1]+second for first, second in edge) for edge in closure_edges}
    assert coordinate_crossings == residual_crossings and len(residual_crossings) == modules
    assert len(incident) == modules
    assert all(record['ports'] == record['balance'] == 1 and record['charge_twice'] == -1
               and record['signed_shortfall'] == 0 for record in incident)
    assert all(record['charge_twice'] == 0 for record in remainder)
    bound = sum(record['signed_shortfall'] for record in incident)+sum(
        record['charge_twice'] for record in remainder)/2
    assert bound == direct_check(*current)-current[0]*current[1]//2 == 0
    assert general_region_ledger(current, patch_regions['child'])['charge_twice']+general_region_ledger(
        current, patch_regions['bottom'])['charge_twice'] == -2
    return dict(modules=modules, capacity_two_source=flipped,
                paid_ports=modules, outside_components=len(components), bound=0)


def envelope_controls():
    records = []
    expected = {'residual': (1, 0, 0, 1, 0),
                'saturated_export': (0, 0, 1, 0, 0),
                'saturated_attachment': (0, 1, 0, 0, -2)}
    for role in expected:
        original = configuration(1)
        selected = set(original[2])
        matching = list(original[3])
        if role == 'residual':
            matching.append(((7, 8), (8, 8)))
        elif role == 'saturated_export':
            matching.append(((7, 0), (8, 0)))
        else:
            selected.remove((7, 9))
            selected.update(((8, 9), (9, 8)))
            matching.append(((7, 8), (8, 8)))
        current = 10, original[1], selected, matching
        direct_check(*current)
        window = {(row, column) for row in range(8) for column in range(current[1])}
        outside = {(row, column) for row in (8, 9) for column in range(current[1])}
        record = closure_control(current, window, outside)
        assert tuple(record[key] for key in ('residual', 'saturated_attachments', 'saturated_exports',
                                             'charge_twice_before', 'charge_twice_after')) == expected[role]
        slab = 8, current[1], selected & window, [edge for edge in matching if all(vertex in window for vertex in edge)]
        assert direct_check(*slab) <= slab[0]*slab[1]//2
        assert record['charge_twice_before'] <= record['residual']+2*record['saturated_attachments']
        witness = witness_record('Eight-row envelope boundary role: '+role, current)
        witness['envelope'] = record
        records.append(witness)
    current = configuration(1)
    padded = 10, current[1], current[2], current[3]
    assert direct_check(*padded) == 4*current[1]
    assert general_region_ledger(padded, {(row, column) for row in range(10)
                                         for column in range(current[1])})['charge_twice'] == -2*current[1]
    return dict(boundary_role_witnesses=records, ten_row_padding_charge_twice=-2*current[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-length', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_length < 2:
        parser.error('--max-length must be at least two')
    controls = []
    witnesses = []
    for length in range(2, args.max_length+1):
        for variation, expected in (('two_ports', (2, 0, 0, 1)),
                                    ('capacity_two', (2, 1, -2, 0)),
                                    ('one_port', (1, 0, -1, 0))):
            original, region = bent_receiver(length, variation)
            for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*original, transpose, flip_rows, flip_columns)
                current = (*shape, selected, matching)
                moved_region = transformed(*original[:2], region, [], transpose, flip_rows, flip_columns)[1]
                direct_check(*current)
                assert not eligible(current)
                record, = component_budgets(current, tile_set(current, moved_region))
                assert (record['ports'], record['capacity_two'], record['charge_twice'],
                        record['signed_shortfall']) == expected
                assert len(record['tiles']) == length+1 and record['cycle_rank'] == record['capacity_zero'] == 0
                controls.append(dict(length=length, variation=variation,
                                     symmetry=[transpose, flip_rows, flip_columns], **record))
            if length == 2:
                witness = witness_record('Bent receiver: '+variation, original)
                witness['exterior'] = component_budgets(original, tile_set(original, region))
                witnesses.append(witness)
    cycle_controls = []
    for repaired in (False, True):
        original, region = cyclic_receiver(repaired)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, *symmetry)
            current = (*shape, selected, matching)
            moved_region = transformed(*original[:2], region, [], *symmetry)[1]
            direct_check(*current)
            assert not eligible(current)
            record, = component_budgets(current, tile_set(current, moved_region))
            assert (record['ports'], record['cycle_rank'], record['capacity_two'],
                    record['charge_twice'], record['signed_shortfall']) == (2, 1, 1+int(repaired),
                                                                          -2*int(repaired), 1-int(repaired))
            cycle_controls.append(dict(repaired=repaired, symmetry=symmetry, **record))
        witness = witness_record('Parallel-cycle receiver'+(' repaired' if repaired else ''), original)
        witness['exterior'] = component_budgets(original, tile_set(original, region))
        witnesses.append(witness)
    abstract_count = abstract_controls()
    exhaustive = exhaustive_controls()
    family = [family_control(modules, flipped) for modules in range(1, 41) for flipped in (False, True)]
    envelopes = envelope_controls()
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/EXTERIOR_COMPONENT_BUDGETS.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_mixed_band_boundary_obstacle.py', 'check_residual_corridors.py',
        'check_cross_component_compensation.py', 'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', length_range=[2, args.max_length],
                  bent_symmetry_controls=len(controls), cycle_symmetry_controls=len(cycle_controls),
                  abstract_multigraph_controls=abstract_count, exhaustive=exhaustive,
                  family_controls=family, envelope_controls=envelopes,
                  witnesses=witnesses, bent_controls=controls, cycle_controls=cycle_controls,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite validation of written all-size graph identities and feasible constructions. Abstract models do not certify grid realizability. Global compensation is conditional on the explicit patch and exterior-balance hypotheses; no universal grid or new Lean theorem.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'length_range', 'bent_symmetry_controls',
                                                'cycle_symmetry_controls', 'abstract_multigraph_controls', 'exhaustive')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
