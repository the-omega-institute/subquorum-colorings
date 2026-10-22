"""Independent controls for arbitrary tile cuts with terminal and rotor flux."""

import itertools
import json
from collections import Counter

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_gap_axial_compensation import transform
from check_exact_event_reserve import fixtures
from check_activated_singleton_budget import phase_images
from check_incident_eight_north_transfer import charge, shift
from check_localized_exterior_tile_budget import (
    cells_of, complete_certificate, old_family, spanning, tile_inventory, tile_of)
from check_six_row_rotor_exclusion import normalized
from check_terminal_exterior_classification import cap


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def positive_terminal_occurrences(record):
    if charge(record) != 1:
        return []
    terminals = [point for point in record[0]
                 if len(set(neighbors(point)) & record[0]) == 1]
    assert len(terminals) == 2
    result = []
    for point in terminals:
        tile = tile_of(point)
        assert cells_of(tile) & record[0] == {point}
        assert len(cells_of(tile) & record[1]) == 2
        result.append((point, tile))
    assert len({tile for _, tile in result}) == 2
    return result


def partition(universe, kind):
    if kind == 'rows':
        key = lambda tile: tile[0] % 3
    elif kind == 'columns':
        key = lambda tile: tile[1] % 3
    elif kind == 'checkerboard':
        key = lambda tile: (tile[0]+tile[1]) % 2
    elif kind == 'singleton':
        return [{tile} for tile in sorted(universe)]
    else:
        raise ValueError(kind)
    labels = {key(tile) for tile in universe}
    return [{tile for tile in universe if key(tile) == label} for label in sorted(labels)]


def inspect(records, old_indices, data, potential, negative_u, rotor_pairs):
    old_indices = set(old_indices)
    old = [record for index, record in enumerate(records) if index in old_indices]
    baseline, old_potential = tile_inventory(old) if old else ({}, 0)
    assert set(baseline) <= set(data)
    owners = {point: index for index, record in enumerate(records) for point in record[0]}
    new_positive = [index for index, record in enumerate(records)
                    if index not in old_indices and charge(record) == 1]
    anchors = Counter(tile_of(min(records[index][0])) for index in new_positive)
    tokens = Counter(tile for index in new_positive
                     for _, tile in positive_terminal_occurrences(records[index]))
    assert sum(tokens.values()) == 2*len(new_positive)
    old_negative = {tile for tile in negative_u
                    if owners[next(iter(data[tile]['endpoints']))] in old_indices}
    eligible = set()
    for index in old_indices:
        for point, tile in positive_terminal_occurrences(records[index]):
            if baseline[tile]['endpoints'] == {point}:
                eligible.add(tile)
    assert old_negative <= eligible
    mates = set(rotor_pairs.values())
    assert len(mates) == len(rotor_pairs)
    assert not (old_negative & (set(rotor_pairs) | mates))
    residual = {}
    for tile, item in data.items():
        value = (item['doubled_weight']+tokens[tile]+int(tile in old_negative)
                 +int(tile in rotor_pairs)-int(tile in mates))
        assert value >= 0
        residual[tile] = value
        if tile in negative_u-old_negative:
            assert tokens[tile] == 1 and value == 0
        if tile in old_negative or tile in rotor_pairs:
            assert tokens[tile] == 0 and value == 0
    cuts = split_sources = crossing_arcs = closed_marginals = half_integral = 0
    for kind in ('rows', 'columns', 'checkerboard', 'singleton'):
        regions = partition(set(data), kind)
        assert set().union(*regions) == set(data)
        assert sum(map(len, regions)) == len(data)
        total_increment = total_incoming = total_outgoing = 0
        for region in regions:
            positive = sum(amount for tile, amount in anchors.items() if tile in region)
            old_weight = sum(item['doubled_weight'] for tile, item in baseline.items()
                             if tile in region)
            increment = 2*positive+sum(data[tile]['doubled_weight']
                        -(baseline[tile]['doubled_weight'] if tile in baseline else 0)
                        +tokens[tile] for tile in region)
            incoming = sum(tile not in region and mate in region
                           for tile, mate in rotor_pairs.items())
            outgoing = sum(tile in region and mate not in region
                           for tile, mate in rotor_pairs.items())
            actual_old = len(old_negative & region)
            bound_old = len(eligible & region)
            remaining = sum(residual[tile] for tile in region)
            assert increment == (2*positive-old_weight-actual_old
                                  +incoming-outgoing+remaining)
            assert increment >= 2*positive-old_weight-bound_old+incoming-outgoing
            additions = [record for index, record in enumerate(records)
                         if index not in old_indices]
            crossing = [record for record in additions
                        if {tile_of(point) for point in record[0]} & region
                        and not {tile_of(point) for point in record[0]} <= region]
            if crossing:
                split_sources += len(crossing)
            else:
                selected = [record for record in additions
                            if {tile_of(point) for point in record[0]} <= region]
                restricted = old+selected
                restricted_potential = tile_inventory(restricted)[1] if restricted else 0
                assert increment == 2*(restricted_potential-old_potential)
                closed_marginals += 1
            half_integral += increment % 2 != 0
            crossing_arcs += incoming
            total_increment += increment
            total_incoming += incoming
            total_outgoing += outgoing
            cuts += 1
        assert total_incoming == total_outgoing
        assert total_increment == 2*(potential-old_potential)
    return dict(cuts=cuts, split_added_source_occurrences=split_sources,
                crossing_rotor_arc_occurrences=crossing_arcs,
                footprint_closed_marginal_checks=closed_marginals,
                half_integral_regional_increments=half_integral)


def cases():
    for dimensions, symmetry, phase in itertools.product(
            ((6, 4, 4), (8, 4, 10)), itertools.product((False, True), repeat=3),
            itertools.product(range(2), repeat=2)):
        yield [independent_source(dimensions, symmetry, phase)]
    for reflected, row, column in itertools.product((False, True), range(2), range(2)):
        yield [shift(normalized(reflected), (row, column))]
    for _, modules in fixtures():
        for _, _, _, _, moved in phase_images(modules):
            yield [(module['endpoints'], module['selected'],
                    {tuple(sorted(edge)) for edge in module['matching']}) for module in moved]
    for width, gaps, downward, short_wall in itertools.product(
            (6, 12), (0, 1, 3), (False, True), (False, True)):
        rows = tuple(2+10*index for index in range(gaps+1))
        last = rows[-1]+4
        old = old_family(width, rows, last if short_wall else last+6, last+6)
        added = [spanning(width, upper, lower, downward)
                 for upper, lower in zip(rows, rows[1:])]
        added.append(cap(width, 4, rows[-1]))
        if short_wall:
            outer = independent_source((8, 10, 6), (False, False, False), (0, 0))
            added.append(transform(outer, lambda point: (last+7-point[0], point[1]-8)))
        yield old+added


def diagnostics():
    rotor = shift(normalized(False), (1, 0))
    data, potential, _, pairs = complete_certificate([rotor])
    assert potential == 0 and pairs[(0, 0)] == (1, 0)
    assert data[(0, 0)]['doubled_weight'] == -1
    assert data[(1, 0)]['doubled_weight'] == 1
    weights = sorted(item['doubled_weight'] for item in data.values())
    assert weights == [-1, -1, 1, 1]
    assert sum(weights) == 0
    separate_ceilings = sum((weight+1)//2 for weight in weights)
    assert separate_ceilings == 2
    source = independent_source((6, 4, 4), (False, False, False), (0, 0))
    data, potential, _, _ = complete_certificate([source])
    terminal = positive_terminal_occurrences(source)[0][1]
    assert tile_of(min(source[0])) != terminal
    assert data[terminal]['doubled_weight'] == -1 and potential == 1
    return dict(old_rotor_negative_cut=dict(doubled_increment=0, old_doubled_beta=-1,
                    outgoing=1, incoming=0, repaired_rhs=0, omitted_flux_rhs=1),
                added_positive_U_terminal_cut=dict(doubled_increment=0, anchor_count=0,
                    doubled_beta=-1, terminal_credits=1, whole_Phi=1),
                separate_rounding_counterexample=dict(old_empty=True, whole_Phi=0,
                    doubled_regional_increments=weights, exact_total=0,
                    sum_of_individual_ceilings=separate_ceilings))


def main():
    totals = Counter()
    for records in cases():
        data, potential, negative_u, pairs = complete_certificate(records)
        selections = {(), tuple(range(len(records))), tuple(range(0, len(records), 2))}
        for old_indices in sorted(selections):
            totals.update(inspect(records, old_indices, data, potential, negative_u, pairs))
            totals['old_inventory_choices'] += 1
        totals['complete_inventories'] += 1
    assert totals['split_added_source_occurrences'] > 0
    assert totals['crossing_rotor_arc_occurrences'] > 0
    assert totals['half_integral_regional_increments'] > 0
    print(json.dumps(dict(status='PASS', **totals, diagnostics=diagnostics(),
        scope='Finite controls of a written arbitrary-cut conservation proof. '
              'Checks direct immutable inventory identity, physical new-terminal allocation, '
              'injective actual rotor pairs, exact signed boundary terms, old-eligible debit '
              'and partition sums, including cuts through sources. Does not prove general '
              'grid decomposition, sharp exterior5, or marked-side coverage.'), indent=2))


if __name__ == '__main__':
    main()
