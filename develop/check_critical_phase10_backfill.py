"""Critical U10 backfill geometry and exact receiver orientation controls."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_critical_closed_owner_counterexample import modules as six_sources
from check_critical_owner_profiles import anchored_images, event_families
from check_critical_owner_profiles import family, fixtures, normalized
from check_critical_owner_profiles import phase_eleven_terminal_fixture
from check_full_neutral_receivers import add, scale, tile
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from rotor_networks import combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
FRAMES = [(first, second) for first, second in itertools.product(DIRECTIONS, repeat=2)
          if sum(value*other for value, other in zip(first, second)) == 0]
BACK = {(0, -2), (0, -1), (1, -2), (1, -1)}
KNOWN = {(-1, -1): (-1, 0), (-1, 0): (-1, 0), (-1, 1): (-1, 0),
         (0, -2): None, (0, -1): None, (0, 0): None, (1, 0): None, (2, 0): None}


def critical_tile(root, frame):
    return {add(root, add(scale(frame[0], row), scale(frame[1], column)))
            for row, column in itertools.product((0, -1), (0, 1))}


def back_tile(root, frame):
    return {add(root, add(scale(frame[0], row), scale(frame[1], column)))
            for row, column in itertools.product((0, -1), (-1, -2))}


def critical_tags(root, frame):
    result = {add(root, add(frame[0], scale(frame[1], step))): frame[0]
              for step in (-1, 0, 1)}
    result.update({add(root, scale(frame[1], step)): None for step in (-1, -2)})
    return result


def orientation_controls():
    counts = Counter()
    critical = set()
    for root, frame in itertools.product(sorted(BACK), FRAMES):
        counts['ordinary_frame_point_cases'] += 1
        if tile(frame, root) == BACK:
            counts['ordinary_same_tile_cases'] += 1
            active = {add(root, add(scale(frame[0], step), scale(frame[1], -1))): frame[0]
                      for step in (-1, 0, 1, 2)}
            assert any(KNOWN[point] != tag for point, tag in active.items() if point in KNOWN)
        if critical_tile(root, frame) == BACK:
            counts['critical_same_tile_cases'] += 1
            tags = critical_tags(root, frame)
            if all(KNOWN[point] == tag for point, tag in tags.items() if point in KNOWN):
                critical.add((root, frame))
    assert critical == {((0, -2), ((-1, 0), (0, 1))),
                        ((0, -2), ((0, -1), (1, 0))),
                        ((0, -1), ((-1, 0), (0, -1))),
                        ((1, -2), ((1, 0), (0, 1))),
                        ((1, -2), ((0, -1), (-1, 0)))}
    candidates = set()
    roots = ((0, 0), (1, 0), (0, -3), (1, -3),
             (-1, -2), (-1, -1), (2, -2), (2, -1))
    for root, frame in itertools.product(roots, FRAMES):
        counts['backfill_frame_root_cases'] += 1
        if back_tile(root, frame) != BACK:
            continue
        counts['backfill_same_tile_cases'] += 1
        companion = {add(root, scale(frame[1], step)) for step in (-1, -2)}
        if not companion & {(0, -2), (0, -1)}:
            candidates.add((root, frame))
    assert candidates == {((1, 0), ((1, 0), (0, 1))),
                          ((1, -3), ((1, 0), (0, -1)))}
    return dict(counts=counts, critical_candidates=sorted(critical),
                distinct_companion_backfill_candidates=sorted(candidates))


def source_geometry_controls():
    counts = Counter()
    for dimensions in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8, 20)):
        width, left, right = dimensions
        base = source(*dimensions)
        for anchor, module in anchored_images(base):
            counts['anchored_U_images'] += 1
            own = module['endpoints']
            if own & {(-1, 0), (0, -1)}:
                continue
            counts['two_blocker_U_roles'] += 1
            assert {(1, 0), (2, 0)} <= own or {(0, 1), (0, 2)} <= own
        southern = [transform_module(base, (False, True, True), (left, 1)),
                    transform_module(base, (False, True, False), (right, -width))]
        for module in southern:
            counts['phase10_south_terminal_roles'] += 1
            assert phase_of(module) == '10'
            assert {(0, 0), (1, 0), (2, 0)} <= module['endpoints']
            assert not {(1, -1), (1, -2), (1, 1)} & module['endpoints']
            assert (1, -1) in module['selected']
        companions = [transform_module(base, (True, False, False), (-1, -left-1)),
                      transform_module(base, (True, False, True), (width, -right-1))]
        for module in companions:
            counts['phase11_companion_terminal_roles'] += 1
            assert phase_of(module) == '11'
            assert module['endpoints'] & BACK == {(0, -1), (0, -2)}
            assert module['selected'] & BACK == {(1, -2)}
            assert (0, -3) in module['endpoints']
    rotor_images = {frozenset(module['endpoints']) for _, module in anchored_images(rotor())}
    assert len(rotor_images) == 16
    for own in rotor_images:
        if own & {(-1, 0), (0, -1)}:
            continue
        counts['two_blocker_rotor_roles'] += 1
        assert {(1, 0), (2, 0)} <= own or {(0, 1), (0, 2)} <= own
    return dict(counts)


def complete_controls():
    controls = fixtures()+[('critical_six', six_sources()),
                           ('critical_phase11_terminal', phase_eleven_terminal_fixture())]
    controls += [('critical_family_'+str(width), family(width)) for width in (20, 22, 26, 40, 100)]
    counts = Counter(critical_phase10_events=0)
    for _, modules in controls:
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose
                      else (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset) for module in modules])
            network = combine(moved)
            endpoints = network['endpoints']
            assert len(endpoints) == sum(len(module['endpoints']) for module in moved)
            assert all(len(set(neighbors(point)) & (endpoints | network['selected'])) <= 1
                       for point in network['selected'])
            regular, critical, _, phases = event_families(moved)
            ordinary_tiles = {tile_of(point) for _, point, _ in regular}
            critical_tiles = {tile_of(point) for _, point, _, _ in critical}
            backfills = set()
            counts['complete_feasible_images'] += 1
            counts['critical_events'] += len(critical)
            for _, point, frame, owner in critical:
                if phases[owner] != '10':
                    continue
                counts['critical_phase10_events'] += 1
                cells = back_tile(point, frame)
                assert cells <= endpoints
                receiver = tile_of(next(iter(cells)))
                assert cells == vertices_of({receiver})
                assert receiver not in ordinary_tiles | critical_tiles | backfills
                backfills.add(receiver)
                companion = next(module for module in moved
                                 if add(point, scale(frame[1], -1)) in module['endpoints'])
                assert phase_of(companion) == '11'
                assert {normalized(site, point, frame) for site in cells & companion['endpoints']} == {
                    (0, -1), (0, -2)}
                assert not cells & moved[owner]['endpoints']
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = dict(status='PASS', orientation_controls=orientation_controls(),
                  source_geometry_controls=source_geometry_controls(),
                  complete_controls=complete_controls(),
                  scope='General backfill/receiver separation and original-owner arguments are written '
                        'and normalized primitives formalized. Fixed direction/rotor catalogue is exhaustive; '
                        'U dimension samples are controls only. Complete phase10 critical coverage must be '
                        'read from the recorded count and is not inferred from local roles. '
                        'No backfill sharpness, fresh reserve, full allocation or grid equality claim.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
