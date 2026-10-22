"""Direct canonical-side mark controls for the complete width-six core."""

import itertools
import json
from collections import Counter

from check_activated_singleton_budget import phase_images
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_exact_event_reserve import fixtures
from check_incident_eight_north_transfer import charge, shift
from check_localized_exterior_tile_budget import (
    cells_of, complete_certificate, old_family, spanning, tile_of)
from check_minus_one_joint_compensation import marked_gate_modules
from check_terminal_exterior_classification import cap, is_complete
from dual_guard_compensation import paired_guards


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def canonical_sides(record):
    if charge(record) != 1:
        return []
    result = []
    for chosen in record[1]:
        anchors = set(neighbors(chosen)) & record[0]
        assert len(anchors) == 1
        anchor = next(iter(anchors))
        inward = tuple(chosen[axis]-anchor[axis] for axis in (0, 1))
        cells = cells_of(tile_of(chosen))
        if cells & record[0] or cells & record[1] != {chosen}:
            continue
        for along in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if sum(inward[axis]*along[axis] for axis in (0, 1)):
                continue
            gate = tuple(chosen[axis]-along[axis] for axis in (0, 1))
            far = tuple(chosen[axis]+inward[axis] for axis in (0, 1))
            opposite = tuple(gate[axis]+inward[axis] for axis in (0, 1))
            guard = tuple(chosen[axis]-2*along[axis]+inward[axis] for axis in (0, 1))
            if {chosen, gate, far, opposite} != cells or guard not in record[0]:
                continue
            protectors = {tuple(anchor[axis]+sign*along[axis] for axis in (0, 1))
                          for sign in (-1, 1)} | {guard}
            if not protectors <= record[0]:
                continue
            missing = {}
            for point in protectors:
                targets = set(neighbors(point))-record[0]-record[1]
                assert len(targets) == 1
                missing[point] = next(iter(targets))
            result.append(dict(chosen=chosen, protectors=protectors, missing=missing))
    assert len(result) == 2
    assert len({tile_of(side['chosen']) for side in result}) == 2
    return result


def actual_marks(records):
    endpoints = set.union(*(record[0] for record in records))
    original_supports = set.union(*(record[1] for record in records))
    occupied = endpoints | original_supports
    result = {}
    for index, record in enumerate(records):
        if charge(record) != 1:
            continue
        marks = []
        for side in canonical_sides(record):
            affected = {point for point in side['protectors']
                        if len(set(neighbors(point)) & occupied) == 4}
            missing_endpoints = {point for point, target in side['missing'].items()
                                 if target in endpoints}
            missing_occupied = {point for point, target in side['missing'].items()
                                if target in occupied}
            assert affected == missing_endpoints == missing_occupied
            marks.append(bool(affected))
        result[index] = sum(marks)
    return result


def records_of(modules):
    return [(module['endpoints'], module['selected'],
             {tuple(sorted(edge)) for edge in module['matching']}) for module in modules]


def source_controls():
    count = 0
    for dimensions, symmetry, offset in itertools.product(
            ((6, 4, 4), (6, 4, 10), (8, 6, 10), (20, 4, 4), (100, 40, 6)),
            itertools.product((False, True), repeat=3), itertools.product(range(2), repeat=2)):
        record = independent_source(dimensions, symmetry, offset)
        if charge(record) == 1:
            assert len(canonical_sides(record)) == 2
            count += 1
    return count


def physical_controls():
    count = marked_one = marked_two = 0
    for _, modules in fixtures():
        for _, _, _, _, moved in phase_images(modules):
            records = records_of(moved)
            complete_certificate(records)
            marks = actual_marks(records)
            occupied = set.union(*(record[0] | record[1] for record in records))
            for index, marked in marks.items():
                standard = []
                standard_tiles = set()
                for chosen, anchor, _, guard in paired_guards(moved[index]):
                    protectors = (set(neighbors(anchor)) & records[index][0]) | {guard}
                    standard.append(any(len(set(neighbors(point)) & occupied) == 4
                                        for point in protectors))
                    standard_tiles.add(tile_of(chosen))
                assert marked == sum(standard)
                assert standard_tiles == {tile_of(side['chosen'])
                                          for side in canonical_sides(records[index])}
                marked_one += marked == 1
                marked_two += marked == 2
            count += 1
    return dict(complete_physical_images=count, singly_marked_positive_occurrences=marked_one,
                doubly_marked_positive_occurrences=marked_two)


def double_mark_block():
    full = records_of(marked_gate_modules())
    assert is_complete(full)
    assert actual_marks(full) == {0: 2}
    return full


def family_controls():
    full = double_mark_block()
    checked = qualifying = previous_condition_excluded = coarse_mark_condition_excluded = 0
    witness = None
    for gaps in range(4):
        rows = tuple(2+10*index for index in range(gaps+1))
        last = rows[-1]+4
        for modes, doubles, unmarked in itertools.product(
                itertools.product((False, True), repeat=gaps), (0, 1, 4, 5, 7), (0, 2)):
            old = old_family(6, rows, last+10, last+14)
            chambers = [spanning(6, upper, lower, downward)
                        for upper, lower, downward in zip(rows, rows[1:], modes)]
            exterior = [cap(6, 4, rows[-1])]
            for index in range(doubles):
                exterior += [shift(record, (100+80*index, 100)) for record in full]
            exterior += [independent_source((20+2*index, 4, 10),
                                             (False, False, False), (100+40*index, 1000))
                         for index in range(unmarked)]
            records = old+chambers+exterior
            _, potential, _, _ = complete_certificate(records)
            marks = actual_marks(records)
            for index in range(1, gaps+1):
                assert marks[index] == 0
            for index, downward in enumerate(modes):
                if not downward:
                    assert marks[len(old)+index] == 0
            last_marks = marks[gaps+1]
            assert last_marks == 0
            start = len(old)+len(chambers)
            exterior_counts = Counter(marked for index, marked in marks.items() if index >= start)
            assert exterior_counts == Counter({0: 1+unmarked, 2: doubles})
            positive_out = sum(exterior_counts.values())
            total_marks = sum(marks.values())
            assert total_marks == last_marks+exterior_counts[1]+2*exterior_counts[2]
            downward = sum(modes)
            assert potential >= 4*gaps+2*downward+2+positive_out
            actual_mark_bound = (4*gaps+2*downward+2-last_marks
                                 +exterior_counts[0]-exterior_counts[2])
            assert potential-total_marks >= actual_mark_bound
            condition = exterior_counts[2] <= exterior_counts[0]+4*gaps+2*downward
            if condition:
                assert actual_mark_bound >= 0
                qualifying += 1
                previous_condition_excluded += positive_out > 4*downward
                coarse_mark_condition_excluded += total_marks > len(marks)
            if condition and total_marks > len(marks) and witness is None:
                witness = dict(gaps=gaps, downward=downward, positive_out=positive_out,
                    unmarked_exterior=exterior_counts[0], singly_marked_exterior=exterior_counts[1],
                    doubly_marked_exterior=exterior_counts[2], last_old_marks=last_marks,
                    total_positive=len(marks), total_actual_marks=total_marks,
                    Phi=potential, certified_marked_slack=actual_mark_bound,
                    exact_source_ledger_margin=potential-total_marks)
            checked += 1
    assert previous_condition_excluded > 0 and coarse_mark_condition_excluded > 0
    return dict(whole_complete_width_six_families=checked,
        sufficient_actual_mark_excess_controls=qualifying,
        qualifying_beyond_previous_Pout_le_4d=previous_condition_excluded,
        qualifying_beyond_coarse_G_le_N=coarse_mark_condition_excluded,
        singly_marked_exterior_in_these_families=0, witness=witness)


def main():
    source_images = source_controls()
    physical = physical_controls()
    families = family_controls()
    print(json.dumps(dict(status='PASS', source_side_reconstructions=source_images,
        **physical, **families,
        scope='Direct actual dual-guard mark counts and complete immutable-source controls '
              'for a written general unmarked-core theorem. Source-to-grid ledger remains '
              'an explicit dependency. Neither finite enumeration nor these controls '
              'prove arbitrary grid decomposition or unrestricted coefficient one.'), indent=2))


if __name__ == '__main__':
    main()
