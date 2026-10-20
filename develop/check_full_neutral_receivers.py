"""Full receiver injection: exact frames, original geometry and complete controls."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_closed_neutral_receivers import closed_contacts
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures, inspect_exact
from check_minus_one_tip_obstructions import source
from check_neutral_phase10_descent import family
from check_occupied_gate_activation import positive_dimensions
from check_passive_corner_transfers import inspect_transfers
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def add(first, second):
    return tuple(value+other for value, other in zip(first, second))


def scale(point, amount):
    return tuple(amount*value for value in point)


def tile(frame, point):
    first, second = frame
    return {point, add(point, first), add(point, scale(second, -1)),
            add(point, add(first, scale(second, -1)))}


def stencil(frame, point, kind, extended=True):
    first, second = frame
    steps = (-1, 0, 1, 2) if extended else (-1, 0, 1)
    result = {add(point, add(scale(first, step), scale(second, -1))): first
              for step in steps}
    result.update({add(point, add(scale(first, -1), scale(second, step))):
                   second if kind == 'first' else None for step in (0, 1)})
    return result


def compatible(first, second):
    return all(first[point] == second[point] for point in first.keys() & second.keys())


def exact_frames():
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    frames = [(first, second) for first, second in itertools.product(directions, repeat=2)
              if sum(value*other for value, other in zip(first, second)) == 0]
    counts = Counter()
    for first_kind, second_kind in itertools.product(('first', 'long'), repeat=2):
        prefix = first_kind+'_'+second_kind
        for first_frame, second_frame in itertools.product(frames, repeat=2):
            cells = tile(first_frame, (0, 0))
            for point in cells:
                if tile(second_frame, point) != cells:
                    continue
                counts[prefix+'_same_tile_cases'] += 1
                old = compatible(stencil(first_frame, (0, 0), first_kind, False),
                                 stencil(second_frame, point, second_kind, False))
                current = compatible(stencil(first_frame, (0, 0), first_kind),
                                     stencil(second_frame, point, second_kind))
                counts['three_run_distinct_point_survivors'] += old and point != (0, 0)
                counts[prefix+'_four_run_survivors'] += current
                assert not current or point == (0, 0)
                assert current == (point == (0, 0) and first_frame == second_frame
                                   and first_kind == second_kind)
    assert counts['three_run_distinct_point_survivors'] == 32
    return dict(counts)


def original_geometry():
    counts = Counter()
    blockers = {(1, 0), (2, 1), (0, 0), (2, 2)}
    for width, left, right in itertools.product((6, 8, 14), (4, 6, 10), (4, 8)):
        base = source(width, left, right)
        for symmetry in itertools.product((False, True), repeat=3):
            for anchor in base['endpoints']:
                root = affine(anchor, symmetry)
                module = transform_module(base, symmetry, (1-root[0], 1-root[1]))
                if phase_of(module) != '01':
                    continue
                counts['phase01_original_owner_images'] += 1
                if blockers & module['endpoints']:
                    continue
                assert anchor in ((left, 1), (right, width))
                counts['phase01_forced_owner_terminal_survivors'] += 1
        parent = transform_module(base, (False, False, False), (2-left, -1))
        for distance in range(0, left-2, 2):
            point = (1-distance, 1)
            cells = vertices_of({tile_of(point)})
            assert cells & parent['endpoints'] == {(point[0]-1, 0), (point[0], 0)}
            assert cells & parent['selected'] == {point}
            assert {(point[0]+step, 0) for step in (-2, -1, 0, 1)} <= parent['endpoints']
            counts['first_or_long_four_run_original_profiles'] += 1
    return dict(counts)


def inspect_complete(current, modules):
    exact = inspect_exact(current, modules)
    transfers = inspect_transfers(current, modules)
    endpoints = combine(modules)['endpoints']
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    owner_at = {point: owner for owner, module in enumerate(modules)
                for point in module['endpoints']}
    phases = [phase_of(module) for module in modules]
    data, closed, contacts, _, _ = closed_contacts(modules)
    closed01 = {point for owner in closed if phases[owner] == '01'
                for point in modules[owner]['endpoints']}
    tags = {point: record['ports'][0]['inward'] for owner, record in data.items()
            if record['phase'] == '01' for point in modules[owner]['endpoints']}
    events = []
    counts = Counter()
    for key, target in contacts.items():
        if phases[key[0]] != phases[target[0]] or phases[key[0]] != '01':
            continue
        port = data[key[0]]['ports'][key[1]]
        if port['blank'] not in endpoints:
            continue
        frame = port['inward'], port['exterior']
        forced = add(add(port['point'], frame[0]), frame[1])
        assert forced in endpoints
        events.append((key[0], forced, frame, 'first'))
        counts['first_contacts'] += 1
        counts['closed_first_contacts'] += key[0] in closed
        if phases[owner_at[forced]] != '11':
            continue
        counts['phase11_first_owners'] += 1
        incoming_width = positive_dimensions(modules[owner_at[forced]])[0]
        second = add(forced, scale(frame[0], incoming_width))
        if second in modules[key[0]]['endpoints']:
            counts['critical_phase11_exits'] += 1
            continue
        assert second in endpoints
        assert second in modules[key[0]]['selected'] & modules[owner_at[forced]]['selected']
        events.append((key[0], second, frame, 'long'))
        counts['long_second_receivers'] += 1
    occupied_tiles, positions = set(), set()
    nonfull = 0
    for owner, point, frame, kind in events:
        expected = stencil(frame, point, kind)
        assert all(tags.get(site) == value for site, value in expected.items())
        receiver = tile_of(point)
        cells = vertices_of({receiver})
        assert cells == tile(frame, point)
        assert receiver not in occupied_tiles
        occupied_tiles.add(receiver)
        pair = {add(point, scale(frame[1], -1)),
                add(point, add(frame[0], scale(frame[1], -1)))}
        assert cells & modules[owner]['endpoints'] == pair
        assert cells & modules[owner]['selected'] == {point}
        additional = (cells & endpoints)-pair
        assert point in additional and len(additional) in (1, 2)
        assert not additional & positions and not additional & closed01
        positions.update(additional)
        nonfull += len(additional) == 1
        counts['full_receivers'] += len(additional) == 2
    assert len(positions)+nonfull == 2*len(events)
    assert transfers['counted']+nonfull <= 2*exact['activated_positive']+exact['boundary_cost']
    counts.update(receivers=len(events), nonfull_receivers=nonfull,
                  distinct_additional_endpoints=len(positions))
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    summary = Counter()
    control_fixtures = list(fixtures())
    control_fixtures += [('phase10_full_family_'+str((incoming, gap)),
                          family(incoming+gap, incoming))
                         for incoming, gap in itertools.product((6, 8, 12, 20), (4, 6, 10))]
    for _, modules in control_fixtures:
        for _, _, _, current, moved in phase_images(modules):
            summary.update(inspect_complete(current, moved))
            summary['complete_feasible_images'] += 1
    assert summary['full_receivers'] > 0
    for name in ('phase11_first_owners', 'long_second_receivers', 'critical_phase11_exits',
                 'closed_first_contacts'):
        summary.setdefault(name, 0)
    result = dict(status='PASS', exact_frame_controls=exact_frames(),
                  original_geometry=original_geometry(), complete_controls=dict(summary),
                  complete_AA_coverage=0,
                  scope='General four-endpoint and two-complementary-pair proof, with scoped Lean. '
                  'Complete controls include actual full first receivers, but ZERO long/critical '
                  'phase11 or closed01 contacts; those coverage counts are reported explicitly. '
                  'No fresh reserve payment or complete grid/coefficient-one theorem.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
