"""Physical slot payments and exact role controls for two width-six gates."""

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
from check_occupied_gate_activation import gate_roles, positive_dimensions
from check_regular_tile_compensation import profile_counts
from check_saturated_gate_geometry import tip_forbidden
from check_short_leg_defect_injection import defect_tiles, inverse_affine
from check_unactivated_double_compensation import both_forced_tiles
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def normalized_maps(module, reflected=False):
    width, left, right, symmetry, offset = positive_dimensions(module)

    def reference(point):
        row, column = affine(point, symmetry, offset)
        return row, width+1-column if reflected else column

    def original(point):
        row, column = point
        return inverse_affine((row, width+1-column if reflected else column), symmetry, offset)

    return (width, right if reflected else left, left if reflected else right,
            reference, original)


def tight_witness(module, modules, endpoints, selected, owners, reflected):
    width, height, _, reference, original = normalized_maps(module, reflected)
    gate = original((2, 2))
    if gate not in endpoints:
        return None
    incoming_index = owners[gate]
    incoming = modules[incoming_index]
    body = {reference(point) for point in incoming['endpoints']}
    if set(neighbors((2, 2))) & body != {(3, 2)}:
        return None
    incident = max(row for row, column in body if column == 2)-2
    if incident != height-2 or not profile_counts(incoming)[3, 0]:
        return None
    cells = {original(point) for point in itertools.product((height, height+1), (2, 3))}
    pair = {original((height, 2)), original((height, 3))}
    assert cells & incoming['endpoints'] == pair
    assert not cells & incoming['selected']
    assert not cells & (module['endpoints'] | module['selected'])
    assert original((height+1, 2)) not in endpoints | selected
    corner, partner = original((height, 2)), original((height, 3))
    assert len(set(neighbors(corner)) & incoming['endpoints']) == 2
    assert len(set(neighbors(partner)) & incoming['endpoints']) == 3
    tiles = {tile_of(point) for point in cells}
    assert len(tiles) == 1
    return dict(tile=next(iter(tiles)), incoming=incoming_index, height=height,
                incident=incident, positive_width=width)


def inspect_payment(current, modules):
    report = inspect_sources(current, modules)
    marks = {tuple(record['tile']): record for record in inspect_slots(current, modules)[
        'marked_assignments']}
    endpoints = combine(modules)['endpoints']
    owners = {point: index for index, module in enumerate(modules)
              for point in module['endpoints']}
    defects = defect_tiles(modules, endpoints)
    blank = {tile for tile, record in marks.items() if record['kind'] == 'blank_gate'}
    assert all(defects[tile] == 'L2bar' for tile in blank)
    actual_slots = {(tile, slot) for tile, kind in defects.items()
                    for slot in range(2 if kind in ('L2bar', 'L2mutual') else 1)}
    assert len(actual_slots) == report['boundary_cost']
    census = Counter()
    selected_slots = []
    paid_witnesses = []
    all_tight = []
    positive_parameters = []
    interleavings = []
    for index, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        width, left, right, _, _ = positive_dimensions(module)
        positive_parameters.append((width, left, right))
        side_marks = []
        activated = []
        tight = []
        for reflected in (False, True):
            _, height, _, reference, original = normalized_maps(module, reflected)
            tile = tile_of(original((3, 2)))
            mark = marks.get(tile)
            side_marks.append(mark)
            terminal = vertices_of({tile_of(original((height, 1)))})
            supports = terminal & module['selected']
            assert len(supports) == 2
            active = bool(supports & endpoints)
            activated.append(active)
            witness = None if active or mark is None else tight_witness(
                module, modules, endpoints, current[2], owners, reflected)
            tight.append(witness)
            if witness is not None:
                assert defects[witness['tile']] in ('L2bar', 'L3')
                assert witness['tile'] not in blank
                all_tight.append(dict(source=index, reflected=reflected, **witness))
            if width == 6 and mark is not None:
                assert mark['kind'] == 'gate'
        if width == 6 and all(side_marks):
            assert all(mark['kind'] == 'gate' for mark in side_marks)
            for reflected, active in zip((False, True), activated):
                if active:
                    continue
                _, long_height, short_height, reference, original = normalized_maps(
                    module, reflected)
                incoming_index = owners[original((2, 2))]
                opposite_index = owners[original((2, 5))]
                assert incoming_index != opposite_index
                incoming = {reference(point) for point in modules[incoming_index]['endpoints']}
                opposite = {reference(point) for point in modules[opposite_index]['endpoints']}
                incident = max(row for row, column in incoming if column == 2)-2
                other_incident = max(row for row, column in opposite if column == 5)-2
                assert short_height <= other_incident <= incident-2 <= long_height-4
                assert profile_counts(modules[incoming_index])[3, 0]
                assert not profile_counts(modules[opposite_index])[3, 0]
                if long_height-short_height <= 4:
                    assert long_height == short_height+4 and incident == long_height-2
                interleavings.append(dict(source=index, long=long_height, short=short_height,
                                          incident=incident, opposite=other_incident))
        if not all(side_marks):
            continue
        exceptional = width != 6 and (width >= 12 or max(left, right) >= 8)
        if exceptional:
            census['exceptional'] += 1
            continue
        activation_count = sum(activated)
        census[activation_count] += 1
        source_blank = sorted(tuple(mark['tile']) for mark in side_marks
                              if mark['kind'] == 'blank_gate')
        if activation_count == 0:
            if source_blank:
                selected_slots.extend((source_blank[0], slot) for slot in range(2))
            else:
                selected_slots.extend((tile, 0) for tile in both_forced_tiles(
                    module, modules, endpoints))
        elif activation_count == 1:
            if source_blank:
                selected_slots.append((source_blank[0], 0))
                census['paid'] += 1
                paid_witnesses.append(dict(source=index, kind='blank', tile=source_blank[0]))
            elif any(tight):
                witness = next(member for member in tight if member is not None)
                selected_slots.append((witness['tile'], 0))
                census['paid'] += 1
                paid_witnesses.append(dict(source=index, kind='tight', **witness))
    assert len(set(selected_slots)) == len(selected_slots)
    assert set(selected_slots) <= actual_slots
    zero_count, single, twice = (census[index] for index in range(3))
    paid, exceptional = census['paid'], census['exceptional']
    assert len(selected_slots) == 2*zero_count+paid
    assert paid <= single
    lower = report['unmarked_sources']-exceptional-(single-paid)//2
    assert report['exact_joint_margin'] >= lower
    covered = all(width == 6 and abs(left-right) <= 4
                  for width, left, right in positive_parameters)
    if covered:
        assert zero_count == 0 and single == paid and exceptional == 0
        assert report['exact_joint_margin'] >= report['unmarked_sources']
    return dict(positive=report['positive'], zero_double=zero_count, single_double=single,
                twice_double=twice, paid_single=paid, exceptional_double=exceptional,
                selected_slots=len(selected_slots), boundary=report['boundary_cost'],
                tight_marked_sides=len(all_tight), covered_width_six=covered,
                unmarked=report['unmarked_sources'], margin=report['exact_joint_margin'],
                margin_bound=lower, tight_witnesses=all_tight,
                paid_witnesses=paid_witnesses, interleavings=interleavings)


def role_controls():
    _, candidates = gate_roles()
    counts = Counter()
    examples = []
    for long_height, short_height in itertools.product((4, 6, 8, 10, 12, 14), repeat=2):
        positive = source(6, long_height, short_height)
        left_roles = [candidate for candidate in candidates
                      if not candidate['module']['endpoints'] & positive['endpoints']
                      and not tip_forbidden(candidate['module'], long_height)]
        right_roles = [(candidate, transform_module(candidate['module'],
                       (False, False, True), (0, 7))) for candidate in candidates]
        right_roles = [(candidate, module) for candidate, module in right_roles
                       if not module['endpoints'] & positive['endpoints']
                       and not tip_forbidden(module, long_height)]
        for incoming in left_roles:
            assert incoming['phase'] == '11' and incoming['predecessor'] == (1, 0)
            for opposite, moved in right_roles:
                if incoming['module']['endpoints'] & moved['endpoints']:
                    continue
                incident, other_incident = incoming['height'], opposite['height']
                assert opposite['phase'] == '10'
                assert short_height <= other_incident <= incident-2 <= long_height-4
                counts['interleaving_pairs'] += 1
                if long_height-short_height <= 4:
                    assert long_height == short_height+4
                    assert incident == long_height-2 and other_incident == short_height
                    counts['height_gap_four_pairs'] += 1
                    if not examples:
                        examples.append(dict(long=long_height, short=short_height,
                            left_parameters=incoming['parameters'], right_parameters=opposite[
                                'parameters'], scope='Endpoint/support role pair; not a complete fusion.'))
    positive = source(6, 4, 4)
    cells = vertices_of({(1, 1)})
    for width, near_height, far_height in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8)):
        base = source(width, near_height, far_height)
        for corner in ((0, 1), (0, width)):
            for symmetry, target in itertools.product(itertools.product((False, True), repeat=3),
                                                       ((3, 2), (2, 3))):
                oriented = affine(corner, symmetry)
                offset = tuple(value-original for value, original in zip(target, oriented))
                moved = transform_module(base, symmetry, offset)
                if moved['endpoints'] & cells != {target, (3, 3)}:
                    continue
                if (2, 2) in moved['endpoints'] | moved['selected']:
                    continue
                assert moved['endpoints'] & positive['endpoints']
                counts['blank_corner_overlaps'] += 1
        incoming = transform_module(base, (False, True, False), (near_height+2, 1))
        corner = near_height+2, 2
        partner = near_height+2, 3
        cells = vertices_of({tile_of(corner)})
        assert cells & incoming['endpoints'] == {corner, partner}
        assert not cells & incoming['selected']
        assert len(set(neighbors(corner)) & incoming['endpoints']) == 2
        assert len(set(neighbors(partner)) & incoming['endpoints']) == 3
        counts['general_height_corner_profiles'] += 1
        cells = vertices_of({(1, 1)})
    assert counts['height_gap_four_pairs'] and counts['blank_corner_overlaps']
    return dict(counts=counts, examples=examples,
                scope='Finite exact role/profile controls, not complete feasible source fusions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    roles = role_controls()
    images = []
    base_fixtures = list(fixtures())
    for height in (6, 8, 10, 14):
        modules = [source(6, height, height-2), transform_module(source(6, height-2, height),
                   (False, True, False), (height, 1))]
        base_fixtures.append(('one_mark_tight_%d' % height, modules))
    for name, modules in base_fixtures:
        for symmetry, phase, _, current, moved in phase_images(modules):
            images.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                               **inspect_payment(current, moved)))
    for amount in (2, 4, 8):
        modules = [transform_module(module, (False, False, False), (0, 20*index))
                   for index in range(amount) for module in [source(6, 8, 6),
                   transform_module(source(6, 6, 8), (False, True, False), (8, 1))]]
        current, moved = contained(modules)
        images.append(dict(fixture='separated_tight_%d' % amount,
                           **inspect_payment(current, moved)))
    summary = dict(physical_images=len(images),
                   tight_marked_occurrences=sum(image['tight_marked_sides'] for image in images),
                   paid_single_double_occurrences=sum(image['paid_single'] for image in images),
                   width_six_interleaving_occurrences=sum(len(image['interleavings']) for image in images),
                   covered_width_six_images=sum(image['covered_width_six'] and image['positive'] > 0
                                               for image in images),
                   multi_tight_images=sum(image['tight_marked_sides'] > 1 for image in images))
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary, roles=roles,
        physical=images,
        scope='Finite physical labelled-slot and complete one-mark tight-gate controls. Paid-single-double and interleaving fixture coverage is reported explicitly; role pairs are incomplete. General width-six/height-gap and common-pool proofs remain written; unrestricted joint/grid theorem OPEN.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary, role_counts=roles['counts'])))


if __name__ == '__main__':
    main()
