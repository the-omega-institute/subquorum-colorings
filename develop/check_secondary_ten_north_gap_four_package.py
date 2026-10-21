"""Independent original-source controls for the narrow north package theorem."""

import itertools
import json
from collections import Counter

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_first_consumer import prescribed
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def fixed_sources(bottom, width, far, other):
    return prescribed(bottom, width+4, far)+[
        independent_source((width, 4, other), (False, False, False), (bottom-9, 6))]


def consumer(bottom, width, breadth, incident, far, right, second=False):
    column = width+7+int(second)
    return independent_source((breadth, incident, far), (False, True, not right),
                              (bottom-9+incident, column-1 if right else column+1))


def classify(record, point):
    assert set(neighbors(point)) & record[0] == {(point[0]+1, point[1])}
    incident = max(row for row, column in record[0])-point[0]
    low = min(column for row, column in record[0])
    high = max(column for row, column in record[0])
    right = low == point[1]
    assert right or high == point[1]
    breadth = high-low+1
    opposite = high if right else low
    far = point[0]+incident-min(row for row, column in record[0] if column == opposite)
    expected = independent_source((breadth, incident, far), (False, True, not right),
                                  (point[0]+incident, point[1]-1 if right else point[1]+1))
    assert record == expected
    return right, breadth, incident, far


def role_controls():
    library, rotors = axial_library({(1, 0), (0, 1)})
    patterns = surviving = excluded_rotors = 0
    forms = Counter()
    negative_examples = []
    for bottom, width, far, other in itertools.product(
            (-24, 40), (8, 10, 20, 50), (4, 6, 10), (4, 6, 12)):
        fixed = fixed_sources(bottom, width, far, other)
        blocked = set.union(*(record[0] for record in fixed))
        point = bottom-9, width+7
        assert point in fixed[2][1] and point not in blocked
        assert {(bottom-10, width+7), (bottom-9, width+6)} <= set(neighbors(point)) & blocked
        local = {(row-point[0], column-point[1]) for row, column in blocked}
        for relative in library:
            if relative[0] & local:
                continue
            record = shift(relative, point)
            right, breadth, incident, leg = classify(record, point)
            assert incident >= (far if right else other+2)
            assert charge(record) == (1 if right else -1)
            forms['right_positive' if right else 'left_negative'] += 1
            surviving += 1
            if not right and len(negative_examples) < 12:
                negative_examples.append((bottom, width, far, other, fixed, record, incident))
        for relative in rotors:
            assert relative[0] & local
            excluded_rotors += 1
        patterns += 1
    second_survivors = second_rotors = 0
    second_forms = Counter()
    for bottom, width, far, other, fixed, first, first_incident in negative_examples:
        blocked = set.union(*(record[0] for record in fixed+[first]))
        point = bottom-9, width+8
        assert point in first[1] and point not in blocked
        assert {(point[0]-1, point[1]), (point[0], point[1]-1),
                (point[0], point[1]+1)} <= set(neighbors(point)) & blocked
        local = {(row-point[0], column-point[1]) for row, column in blocked}
        for relative in library:
            if relative[0] & local:
                continue
            record = shift(relative, point)
            right, breadth, incident, leg = classify(record, point)
            assert incident >= (far if right else first_incident+2)
            assert charge(record) == (-1 if right else 1)
            second_forms['right_negative' if right else 'left_positive'] += 1
            second_survivors += 1
        for relative in rotors:
            assert relative[0] & local
            second_rotors += 1
    assert set(forms) == {'right_positive', 'left_negative'}
    assert set(second_forms) == {'right_negative', 'left_positive'}
    return dict(first_patterns=patterns, first_U_roles=surviving, first_forms=dict(forms),
                first_rotor_exclusions=excluded_rotors, second_patterns=len(negative_examples),
                second_U_roles=second_survivors, second_forms=dict(second_forms),
                second_rotor_exclusions=second_rotors, U_dimensions_bounded_by=18,
                every_bounded_endpoint_role_included=True)


def package_controls():
    patterns = 0
    for bottom, width, far, other, extra, breadth, leg in itertools.product(
            (-24, 40), (8, 10, 20, 50, 200), (4, 10, 40), (4, 12, 50),
            (0, 2, 10), (6, 10, 50), (4, 12, 80)):
        incident = far+extra
        fixed = fixed_sources(bottom, width, far, other)
        outward = consumer(bottom, width, breadth, incident, leg, True)
        assert all(not first[0] & second[0]
                   for first, second in itertools.combinations(fixed+[outward], 2))
        point = bottom-9, width+7
        assert point in outward[0]
        assert {(bottom-10, width+7), (bottom-9, width+6)} <= outward[1]
        assert charge(outward) == 1
        base = inventory(fixed[:2])
        before = inventory(fixed)
        after = inventory(fixed+[outward])
        overlap = min(incident, other)//2
        assert after['mass'] == before['mass']
        assert len(after['full'])-len(before['full']) == 1+overlap
        assert len(after['events'])-len(before['events']) == 1+2*overlap
        assert after['raw_reserve']-before['raw_reserve'] == 1
        assert before['raw_reserve']-base['raw_reserve'] == -2
        assert after['raw_reserve']+1 == base['raw_reserve']
        patterns += 1
    return dict(parameter_patterns=patterns, widths=[8, 10, 20, 50, 200],
                independent_leg_max=80, exact_N_plus_Rraw_package_change=0)


def cavity_controls():
    library, rotors = axial_library({(-1, 0), (1, 0)})
    patterns = surviving = rotor_exclusions = empty = tight = 0
    phases = Counter()
    for bottom, width, far, extra, breadth, leg in itertools.product(
            (-24, 40), (8, 12, 50), (4, 10), (0, 2, 4, 6, 10), (6, 8, 12), (4, 10)):
        incident = far+extra
        fixed = fixed_sources(bottom, width, far, 6)
        outward = consumer(bottom, width, breadth, incident, leg, True)
        fixed.append(outward)
        point = bottom-8, width+8
        blocked = set.union(*(record[0] for record in fixed))
        assert point in fixed[1][1] & outward[1] and point not in blocked
        assert {(point[0], point[1]-1), (point[0], point[1]+1)} <= set(neighbors(point)) & blocked
        local = {(row-point[0], column-point[1]) for row, column in blocked}
        local_count = 0
        for relative in library:
            if relative[0] & local:
                continue
            record = shift(relative, point)
            bar = max(row for row, column in record[0])
            near = bar-min(row for row, column in record[0] if column == point[1])
            span = max(column for row, column in record[0])-(width+7)
            other = bar-min(row for row, column in record[0] if column == width+7+span)
            expected = independent_source((span, near, other), (False, True, False), (bar, width+7))
            assert record == expected
            assert bottom-9+far <= bar <= bottom-9+incident-2
            assert bar-(bottom-9)-1 <= near <= bar-(bottom-9)
            assert incident >= far+2
            assert charge(record) == (-1 if bar % 2 else 1-span)
            assert bar-near == (bottom-9 if bar % 2 else bottom-8)
            if extra == 2:
                assert bar == bottom-9+far and near == far
                assert span <= breadth-2 and breadth >= 8
                tight += 1
            phases['minus_one' if bar % 2 else 'negative_width'] += 1
            surviving += 1
            local_count += 1
        for relative in rotors:
            assert relative[0] & local
            rotor_exclusions += 1
        if extra == 0:
            assert local_count == 0
            empty += 1
        patterns += 1
    assert set(phases) == {'minus_one', 'negative_width'} and tight
    return dict(patterns=patterns, surviving_U_roles=surviving, phases=dict(phases),
                rotor_exclusions=rotor_exclusions, equal_incident_noncompletion_patterns=empty,
                tight_negative_consumer_controls=tight, U_dimensions_bounded_by=18,
                all_endpoint_anchors_included=True)


def obstruction_control():
    fixed = fixed_sources(40, 12, 4, 6)
    outward = consumer(40, 12, 6, 4, 4, True)
    external = independent_source((6, 4, 4), (True, False, False), (32, 13))
    all_sources = fixed+[outward, external]
    assert all(not first[0] & second[0] for first, second in itertools.combinations(all_sources, 2))
    base = inventory(fixed[:2]+[external])
    after = inventory(all_sources)
    internal = inventory(fixed+[outward])
    internal_base = inventory(fixed[:2])
    internal_new = internal['full']-internal_base['full']
    assert internal_new <= after['full']-base['full']
    extra_full = (after['full']-base['full'])-internal_new
    external_events = {event for event in after['events'] if
                       (event[0] in (2, 3) and event[2] in external[0]) or
                       (event[0] == 4 and event[2] in fixed[2][0] | outward[0])}
    assert len(extra_full) == 2 and len(external_events) == 7
    assert 1+after['raw_reserve']-base['raw_reserve'] == -3
    assert not {(row//2, column//2) for row, column in outward[0]} & {
        (row//2, column//2) for row, column in external[0]}
    missing = 32, 20
    endpoints = set.union(*(record[0] for record in all_sources))
    assert missing in fixed[1][1] & outward[1] and missing not in endpoints
    assert (32, 21) in fixed[1][0] and (32, 19) in outward[0]
    assert {(32, 21), (32, 19)} <= set(neighbors(missing)) & endpoints
    return dict(endpoint_disjoint_sources=5, bottom=40, width=12,
                D=[16, 10, 4], L=[12, 4, 6], outward=[6, 4, 4],
                outward_frame='(35-r,18+c)', external=[6, 4, 4],
                external_frame='(32+c,13+r)', repaired_support=[31, 19],
                positive_terminal_supports=[[30, 19], [31, 18]],
                extra_full_tile_indices=sorted(extra_full),
                extra_full_tile_lower_coordinates=sorted((2*row, 2*column) for row, column in extra_full),
                external_directed_events=len(external_events),
                external_events=[dict(owner='W' if event[0] == 4 else 'L' if event[0] == 2 else 'C_R',
                                      endpoint=event[1], target=event[2])
                                 for event in sorted(external_events)],
                external_signed_term=-3, delta_N_plus_Rraw=-3,
                next_missing_forced_original_support=missing,
                complete_family=False, refutes_full_allocation=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', roles=role_controls(), package=package_controls(),
                         cavity=cavity_controls(), obstruction=obstruction_control(),
                         scope='Finite independent controls of a separately written general '
                         'consumer dichotomy, exact neutral raw-potential package, and '
                         'subsequent negative cavity consumer/window. The '
                         'external-sign obstruction is partial, not complete-model or '
                         'allocation refutation. No global target credit is claimed.'), indent=2))
