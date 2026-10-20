"""Original-occurrence controls for cap fills and paired continuations."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures, inspect_exact
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from check_regular_tile_compensation import profile_counts
from check_short_leg_defect_injection import inverse_affine
from rotor_networks import affine, combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def phase_of(module):
    if len(module['endpoints']) == 8:
        return 'rotor'
    if module['charge'] == 1:
        return '00'
    if module['charge'] == -1:
        return '01'
    assert module['charge'] <= -5
    return '11' if profile_counts(module)[3, 0] else '10'


def inspect_occurrences(modules):
    endpoints = set.union(*(module['endpoints'] for module in modules))
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    owner_of = {point: owner for owner, module in enumerate(modules)
                for point in module['endpoints']}
    phases = [phase_of(module) for module in modules]
    census = Counter(phases)
    pool = set()
    activated = set()
    negative_caps = set()
    positive_caps = set()
    cap_tiles = set()
    pair_reserved = set()
    unfilled = 0
    for owner, module in enumerate(modules):
        for tile in module['receiver']:
            cells = vertices_of({tile})
            own = cells & module['endpoints']
            if len(own) == 1 and phases[owner] in ('01', '10'):
                pool.update(own)
            if phases[owner] == '00' and len(own) == 1:
                assert len(cells & module['selected']) == 2
                if cells & module['selected'] & endpoints:
                    activated.add(next(iter(own)))
            if len(own) != 3 or phases[owner] == 'rotor':
                continue
            assert phases[owner] == '11' and tile not in cap_tiles
            cap_tiles.add(tile)
            if not cells <= endpoints:
                unfilled += 1
                continue
            point = next(iter(cells-own))
            foreign = owner_of[point]
            assert foreign != owner
            assert cells & modules[foreign]['endpoints'] == {point}
            assert phases[foreign] in ('00', '01', '10')
            slots = positive_caps if phases[foreign] == '00' else negative_caps
            assert point not in slots
            slots.add(point)
    paired = []
    indirect = []
    continuation_points = []
    indirect_points = []
    parent_pairs = {}
    for point in pool:
        cells = vertices_of({tile_of(point)})
        pair_owners = [owner for owner, module in enumerate(modules)
                       if len(cells & module['endpoints']) == 2 and
                       not cells & module['selected']]
        assert len(pair_owners) <= 1
        if pair_owners:
            assert pair_owners[0] != owner_of[point]
            pair_reserved.add(point)
    for parent, module in enumerate(modules):
        if phases[parent] != '10':
            continue
        width, _, _, symmetry, offset = positive_dimensions(module)
        original = lambda point: inverse_affine(point, symmetry, offset)
        outer = [original((2, 2)), original((2, width-1))]
        if not all(point in endpoints for point in outer):
            continue
        intermediate = owner_of[outer[0]]
        if owner_of[outer[1]] != intermediate or phases[intermediate] != '01':
            continue
        foreign = modules[intermediate]
        tips = {point for point in foreign['endpoints']
                if sum(neighbor in foreign['endpoints'] for neighbor in (
                    (point[0]-1, point[1]), (point[0]+1, point[1]),
                    (point[0], point[1]-1), (point[0], point[1]+1))) == 1}
        assert set(outer) == tips
        reference_points = {affine(point, symmetry, offset) for point in foreign['endpoints']}
        height = max(point[0] for point in reference_points)-2
        expected = transform_module(source(width-2, height, height),
                                    (False, True, False), (height+2, 1))
        assert reference_points == expected['endpoints']
        assert {affine(point, symmetry, offset) for point in foreign['selected']} == expected['selected']
        paired.append((parent, intermediate))
        continuation_points.extend(outer)
        for point in outer:
            cells = vertices_of({tile_of(point)})
            pair = cells & module['endpoints']
            assert len(pair) == 2 and not cells & module['selected']
            assert point not in parent_pairs
            parent_pairs[point] = (parent, tile_of(point), pair)
        inner = [original((2, 3)), original((2, width-2))]
        if not all(point in endpoints for point in inner):
            continue
        child = owner_of[inner[0]]
        if owner_of[inner[1]] != child or phases[child] != '10':
            continue
        child_width, _, _, child_symmetry, child_offset = positive_dimensions(modules[child])
        corners = {inverse_affine(point, child_symmetry, child_offset)
                   for point in ((0, 1), (0, child_width))}
        assert set(inner) == corners and child_width == width-4
        indirect.append((parent, child))
        indirect_points.extend(inner)
        for point in inner:
            cells = vertices_of({tile_of(point)})
            pair = cells & module['endpoints']
            assert len(pair) == 2 and not cells & module['selected']
            assert point not in parent_pairs
            parent_pairs[point] = (parent, tile_of(point), pair)
    assert len(pool) == 2*(census['01']+census['10'])
    assert len(cap_tiles) == 2*census['11']
    assert len(negative_caps)+len(positive_caps)+unfilled == 2*census['11']
    assert positive_caps <= activated
    assert negative_caps <= pool
    assert set(continuation_points) <= pool and set(indirect_points) <= pool
    assert set(continuation_points) | set(indirect_points) <= pair_reserved
    assert not negative_caps & pair_reserved
    assert len(negative_caps)+len(pair_reserved) <= len(pool)
    used = list(negative_caps)+continuation_points+indirect_points
    assert len(used) == len(set(used))
    assert len(used) <= len(pool)
    assert 2*census['11']+2*len(paired)+2*len(indirect) <= (
        2*census['10']+2*census['01']+len(positive_caps)+unfilled)
    assert 2*census['11']+len(pair_reserved) <= (
        2*census['10']+2*census['01']+len(positive_caps)+unfilled)
    return dict(phase01=census['01'], phase10=census['10'], phase11=census['11'],
                unfilled=unfilled, activation=len(activated),
                negative_cap_fillers=len(negative_caps), positive_cap_fillers=len(positive_caps),
                paired=len(paired), indirect=len(indirect), pool=len(pool),
                pair_reserved=len(pair_reserved), used_occurrences=len(used))


def role_controls():
    counts = Counter()
    core = {(row, column) for row in (0, 1) for column in range(1, 7)}
    core |= {(row, 1) for row in range(2, 5)}
    for mirror in (False, True):
        base = transform_module(rotor(), (False, False, mirror))
        for anchor in base['endpoints']:
            offset = 2-anchor[0], 2-anchor[1]
            moved = transform_module(base, (False, False, False), offset)
            assert moved['endpoints'] & core
            counts['exact_rotor_roles'] += 1
    parameters = list(itertools.product((6, 8, 14), (4, 8, 16), (4, 6, 12)))
    parameters += [(40, 100, 4)]
    for dimensions in parameters:
        base = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            points = {affine(point, symmetry) for point in base['endpoints']}
            for row, column in points:
                counts['U_endpoint_roles'] += 1
                if {(row-1, column), (row, column-1)} <= points and (
                        row-1, column-1) not in points:
                    assert (row, column-2) in points
                    counts['triple_arm_roles'] += 1
    for short, incident, width, far in itertools.product((4, 6, 12), (4, 8, 16),
                                                       (6, 10, 20), (4, 8, 18)):
        if incident < short:
            continue
        incoming = transform_module(source(width, incident, far),
                                    (False, True, False), (incident+2, 4))
        assert (short+1, 5) in incoming['endpoints']
        assert (short, 7) not in incoming['endpoints']
        counts['AA_incoming_stem_coordinates'] += 1
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    roles = role_controls()
    physical = []
    cap_fixture = paired_fixture = None
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            report = inspect_occurrences(moved)
            exact = inspect_exact(current, moved)
            assert report['activation'] == exact['activated_positive']
            assert report['unfilled'] == exact['unused_u_triples']
            assert report['phase11']+report['paired']+report['indirect'] <= (
                report['phase10']+report['phase01']+exact['event_reserve'])
            retained = (2*(report['phase11']-report['phase10']-report['phase01'])+
                        report['pair_reserved']+report['activation']-
                        report['positive_cap_fillers']+exact['unpaired_rotor_activation']+
                        exact['boundary_cost'])
            assert retained <= 2*exact['event_reserve']
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 reserve=exact['event_reserve'], **report))
            if report['negative_cap_fillers'] and cap_fixture is None:
                cap_fixture = moved
            if report['paired'] and paired_fixture is None:
                paired_fixture = moved
    assert cap_fixture is not None and paired_fixture is not None
    separated = cap_fixture+[transform_module(module, (False, False, False), (0, 1000))
                             for module in paired_fixture]
    current, moved = contained(separated)
    report = inspect_occurrences(moved)
    exact = inspect_exact(current, moved)
    assert report['negative_cap_fillers'] and report['paired']
    assert report['phase11']+report['paired']+report['indirect'] <= (
        report['phase10']+report['phase01']+exact['event_reserve'])
    physical.append(dict(fixture='separated_caps_and_paired_tips',
                         reserve=exact['event_reserve'], **report))
    partial = []
    for width, height in ((10, 6), (12, 8), (16, 12)):
        parent = transform_module(source(width, 4, 4), (False, False, False), (1, 0))
        intermediate = transform_module(source(width-2, height, height),
                                        (False, True, False), (height+3, 1))
        child = transform_module(source(width-4, 4, 4), (False, False, False), (3, 2))
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            shift = ((int(flip_column), int(flip_row)) if transpose else
                     (int(flip_row), int(flip_column)))
            modules = [transform_module(module, symmetry, shift)
                       for module in (parent, intermediate, child)]
            report = inspect_occurrences(modules)
            assert report['paired'] == report['indirect'] == 1
            network = combine(modules)
            occupied = network['endpoints'] | network['selected']
            bad = [point for point in network['selected'] if sum(neighbor in occupied
                for neighbor in ((point[0]-1, point[1]), (point[0]+1, point[1]),
                                 (point[0], point[1]-1), (point[0], point[1]+1))) > 1]
            assert bad
            partial.append(dict(width=width, height=height, symmetry=symmetry,
                                endpoint_disjoint=True, complete_feasible=False,
                                infeasible_retained_supports=len(bad), **report))
    summary = dict(physical_images=len(physical),
                   filled_U_caps=sum(row['negative_cap_fillers']+row['positive_cap_fillers']
                                     for row in physical),
                   positive_cap_fillers=sum(row['positive_cap_fillers'] for row in physical),
                   negative_cap_fillers=sum(row['negative_cap_fillers'] for row in physical),
                   physical_paired_motifs=sum(row['paired'] for row in physical),
                   physical_indirect_motifs=sum(row['indirect'] for row in physical),
                   physical_images_with_caps_and_paired=sum(
                       row['paired'] > 0 and row['negative_cap_fillers']+
                       row['positive_cap_fillers'] > 0 for row in physical),
                   original_pair_reserved_occurrences=sum(row['pair_reserved'] for row in physical),
                   images_stronger_than_paired_motif_count=sum(row['pair_reserved'] >
                       2*row['paired']+2*row['indirect'] for row in physical),
                   nonvacuous_partial_motif_images=len(partial), new_complete_AA_fixture_coverage=0)
    result = dict(status='PASS', summary=summary, role_controls=dict(roles), physical=physical,
                  partial_motifs=partial,
                  scope='Original phase singleton catalogue, exact rotor orbit barrier, cap and typed paired-continuation token injection. Complete feasible fixture counts are separate from endpoint-disjoint infeasible motif controls. Universal nonreuse and reserve implications have written proofs; scoped Lean checks are separate. No global closure or grid theorem.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=summary, role_controls=dict(roles))))


if __name__ == '__main__':
    main()
