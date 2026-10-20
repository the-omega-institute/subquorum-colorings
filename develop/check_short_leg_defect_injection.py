"""Physical single-use witnesses and the remaining connected D2 patterns."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import inspect_slots, tile_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_multiple_positive_saturation import inspect_sources
from check_occupied_gate_activation import positive_dimensions
from degree_four_overcount import opposed_modules
from dual_guard_compensation import paired_guards
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inverse_affine(point, symmetry, offset):
    row, column = point[0]-offset[0], point[1]-offset[1]
    transpose, flip_row, flip_column = symmetry
    if transpose:
        row, column = column, row
    return (-row if flip_row else row, -column if flip_column else column)


def defect_tiles(modules, endpoints):
    result = {}
    represented = set.union(*(module['receiver'] for module in modules))
    for tile in represented:
        cells = vertices_of({tile})
        owners = [module for module in modules if module['endpoints'] & cells]
        profiles = [(len(module['endpoints'] & cells), len(module['selected'] & cells))
                    for module in owners]
        size = len(cells & endpoints)
        if size == 1 and profiles == [(1, 1)]:
            result[tile] = 'L1'
        elif size == 2 and profiles == [(2, 0)]:
            result[tile] = 'L2bar'
        elif size == 2 and profiles == [(1, 1), (1, 1)]:
            if all((cells & endpoints)-module['endpoints'] <= module['selected']
                   for module in owners):
                result[tile] = 'L2mutual'
        elif size == 3 and len(owners) > 1:
            result[tile] = 'L3'
    return result


def inspect_witnesses(current, modules):
    report = inspect_sources(current, modules)
    slots = inspect_slots(current, modules)
    endpoints = combine(modules)['endpoints']
    owners = {point: index for index, module in enumerate(modules)
              for point in module['endpoints']}
    marked = {tuple(item['tile']): item for item in slots['marked_assignments']}
    blank_tiles = {tile for tile, item in marked.items() if item['kind'] == 'blank_gate'}
    all_defects = defect_tiles(modules, endpoints)
    assert len(all_defects) == sum(report[key] for key in
                            ('lone_irregular', 'sole_irregular_pair',
                             'mutual_non_event', 'mixed_three'))
    pool = {tile: kind for tile, kind in all_defects.items() if kind in ('L2bar', 'L3')}
    assert len(pool) == report['sole_irregular_pair']+report['mixed_three']
    assert blank_tiles <= pool.keys()
    activated_pool = set()
    witnesses = []
    forced_tiles = set()
    for index, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        activated = []
        for tile in module['receiver']:
            cells = vertices_of({tile})
            supports = cells & module['selected']
            if len(cells & module['endpoints']) == 1 and len(supports) == 2:
                if supports & endpoints:
                    activated.append(tile)
                    activated_pool.add((index, tile))
        width, left, right, symmetry, offset = positive_dimensions(module)
        exceptional = width != 6 and (width >= 12 or max(left, right) >= 8)
        side_marks = [marked[tile_of(guard[0])] for guard in paired_guards(module)
                      if tile_of(guard[0]) in marked]
        if exceptional or len(side_marks) != 2:
            continue
        if activated:
            witnesses.append(dict(source=index, kind='A', tile=min(activated)))
            continue
        blank = [tuple(item['tile']) for item in side_marks if item['kind'] == 'blank_gate']
        if blank:
            witnesses.append(dict(source=index, kind='blank', tile=min(blank)))
            continue
        assert width in (8, 10) and left in (4, 6) and right in (4, 6)
        candidates = []
        for reflected, height in ((False, left), (True, right)):
            def normalized(point):
                row, column = affine(point, symmetry, offset)
                return row, width+1-column if reflected else column

            def original(point):
                row, column = point
                return inverse_affine((row, width+1-column if reflected else column),
                                      symmetry, offset)

            gate = original((2, 2))
            incoming_index = owners[gate]
            incoming = modules[incoming_index]
            body = {normalized(point) for point in incoming['endpoints']}
            if set(neighbors((2, 2))) & body != {(3, 2)}:
                continue
            if not {(row, column) for row in (5, 6) for column in range(2, 8)} <= body:
                continue
            assert height == 6
            cells = {original(point) for point in itertools.product((6, 7), (2, 3))}
            tiles = {tile_of(point) for point in cells}
            assert len(tiles) == 1
            tile = next(iter(tiles))
            pair = {original((6, 2)), original((6, 3))}
            assert cells & incoming['endpoints'] == pair
            assert not cells & incoming['selected']
            assert not cells & (module['endpoints'] | module['selected'])
            assert original((7, 2)) not in endpoints | current[2]
            assert pool[tile] in ('L2bar', 'L3')
            corner, partner = original((6, 2)), original((6, 3))
            assert len(set(neighbors(corner)) & incoming['endpoints']) == 2
            assert len(set(neighbors(partner)) & incoming['endpoints']) == 3
            candidates.append((tile, incoming_index, corner, original((6, 1))))
        assert candidates, ('Missing forced longitudinal witness', index, report)
        tile, incoming_index, corner, positive_anchor = min(candidates)
        assert positive_anchor in module['endpoints']
        assert tile not in forced_tiles and tile not in blank_tiles
        forced_tiles.add(tile)
        witnesses.append(dict(source=index, kind='forced_pair', tile=tile,
                              pair_owner=incoming_index, corner=corner,
                              positive_anchor=positive_anchor))
    assert len(activated_pool) == report['activated_positive']
    resources = [('A', item['source'], item['tile']) if item['kind'] == 'A'
                 else ('tile', item['tile']) for item in witnesses]
    assert len(set(resources)) == len(resources)
    assert all((item['source'], item['tile']) in activated_pool if item['kind'] == 'A'
               else item['tile'] in pool for item in witnesses)
    double_count = len(witnesses)
    assert double_count == sum(not item['exceptional'] and item['marked'] == 2
                               for item in report['dimensions'])
    activation = report['activated_positive']
    discarded = (report['unused_u_triples']+report['unpaired_rotor_activation']+
                 report['lone_irregular']+report['sole_irregular_pair']+
                 2*report['mutual_non_event'])
    assert double_count <= activation+len(pool)
    assert double_count+discarded <= 2*report['event_reserve']
    assert report['double_marked_sources']+discarded <= (
        2*report['event_reserve']+report['exceptional_sources'])
    return dict(nonexceptional_double=double_count, activation=activation,
                unweighted_defect_tiles=len(pool), discarded_defects=discarded,
                defect=2*report['event_reserve'], witnesses=witnesses)


def local_controls():
    donor = ((3, 2), (3, 1), (2, 3), (1, 3))
    negative = {(-1, 0), (-1, 1), (0, 0), (0, 1), (0, 2)}
    positive = {(0, -1)}
    records = []
    for symmetry in itertools.product((False, True), repeat=3):
        moved = [affine(point, symmetry) for point in donor]
        lower = tuple(min(point[axis] for point in moved[:1]+[affine((2, 2), symmetry),
                      affine((3, 3), symmetry), moved[2]]) for axis in (0, 1))
        chosen, anchor, opposite, guard = [tuple(value-minimum for value, minimum in
                                                zip(point, lower)) for point in moved]
        inward = chosen[0]-anchor[0], chosen[1]-anchor[1]
        gate = opposite[0]-inward[0], opposite[1]-inward[1]
        reason = ('selected_blank' if chosen == (1, 0) else
                  'negative_anchor' if anchor in negative else
                  'positive_anchor' if anchor in positive else
                  'occupied_gate' if gate in negative else
                  'positive_protector' if guard in positive else None)
        assert reason is not None
        records.append(dict(symmetry=symmetry, chosen=chosen, anchor=anchor,
                            gate=gate, guard=guard, exclusion=reason))
    original_corners = 0
    for width, left, right in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8)):
        incoming = transform_module(source(width, left, right),
                                    (False, True, False), (left+2, 1))
        pair = {(left+2, 2), (left+2, 3)}
        assert len(set(neighbors((left+2, 2))) & incoming['endpoints']) == 2
        assert len(set(neighbors((left+2, 3))) & incoming['endpoints']) == 3
        assert pair <= incoming['endpoints']
        original_corners += 1
    names = ('A', 'U0', 'Z0', 'L1', 'L2bar', 'L2mutual', 'L3')
    patterns = []
    for values in itertools.product(range(3), repeat=7):
        activation, unused, rotor, lone, bar, mutual_pairs, mixed = values
        if activation+unused+rotor+lone+2*bar+2*mutual_pairs+mixed != 2:
            continue
        allowed = 2 <= activation+bar+mixed
        assert allowed == (unused == rotor == lone == bar == mutual_pairs == 0)
        patterns.append(dict(counts=dict(zip(names, values)), survives_injection=allowed))
    assert len(patterns) == 17 and sum(item['survives_injection'] for item in patterns) == 3
    return dict(donor_orientations=records, original_corner_controls=original_corners,
                weighted_D2_patterns=patterns)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    local = local_controls()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_witnesses(current, moved)))
    for amount in (2, 4, 8):
        modules = [transform_module(module, (False, False, False), (0, 20*index))
                   for index in range(amount) for module in opposed_modules(6+2*(index % 2), 4)]
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose else
                      (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset)
                                        for module in modules])
            report = inspect_witnesses(current, moved)
            assert len(report['witnesses']) == amount
            assert all(item['kind'] == 'forced_pair' for item in report['witnesses'])
            physical.append(dict(fixture='separated_forced_%d' % amount,
                                 symmetry=symmetry, **report))
    summary = dict(physical_images=len(physical),
                   witness_kinds=dict(Counter(item['kind'] for record in physical
                                              for item in record['witnesses'])),
                   multi_witness_images=sum(len(record['witnesses']) >= 2 for record in physical),
                   excluded_D2_patterns=14, surviving_D2_patterns=3)
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary,
        local=local, physical=physical,
        scope='Finite actual-source witness reconstruction, all eight local donor orientations, original corner roles and D2 arithmetic controls. Universal injection/ownership and cross-type disjointness are written proofs. Remaining three connected patterns are neither realized nor excluded by these controls.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
