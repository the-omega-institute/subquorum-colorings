"""Independent bounded controls for tight upward terminal rigidity."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, shift
from check_secondary_ten_first_consumer import prescribed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


ROTOR_A = {(-3, -1), (-2, -1), (-2, 0), (-2, 1),
           (-1, -2), (-1, -1), (-1, 0), (0, 0)}
ROTOR_B = {(-3, 1), (-2, -1), (-2, 0), (-2, 1),
           (-1, 0), (-1, 1), (-1, 2), (0, 0)}


def top_controls():
    library, rotors = axial_library({(0, -1), (0, 1)})
    patterns = 0
    for bottom, width in itertools.product((24, 40), (6, 8, 12, 20, 50)):
        fixed = prescribed(bottom, width, 4)
        fixed.append(independent_source((12, width+2, 4),
                                        (True, True, True), (bottom-4, width+9)))
        assert all(not first[0] & second[0] for first, second in itertools.combinations(fixed, 2))
        blocked = fixed[1][0] | fixed[2][0]
        for column in range(7, width+4):
            point = bottom-9, column
            assert point not in blocked and (bottom-10, column) in fixed[1][0]
            for record in library+rotors:
                assert shift(record, point)[0] & blocked
            patterns += 1
    return dict(top_row_sites=patterns, surviving_U_roles=0, surviving_rotor_roles=0,
                widths=[6, 8, 12, 20, 50], all_horizontal_straight_interiors_included=True)


def rigidity_controls():
    library, rotors = axial_library({(-1, 0), (0, -1)})
    patterns = excluded = forced_rotors = 0
    kinds = dict(RA=0, RB=0)
    for bottom, width, breadth, span, other in itertools.product(
            (24, 40), (6, 8, 12), (10, 14), (8, 12), (4, 8)):
        if span > breadth-2:
            continue
        for near in range(4, width, 2):
            fixed = prescribed(bottom, width, 4)
            fixed.append(independent_source((breadth, width+2, 4),
                                            (True, True, True), (bottom-4, width+9)))
            fixed.append(independent_source((span, near, other),
                                            (True, True, True), (bottom-5, width+7)))
            if any(first[0] & second[0] for first, second in itertools.combinations(fixed, 2)):
                excluded += 1
                continue
            terminal = width+7-near
            assert terminal % 2 == 1 and 9 <= terminal <= width+3
            point = bottom-6, terminal-1
            blocked = set.union(*(record[0] for record in fixed))
            assert point in fixed[3][1] and point not in blocked
            assert (bottom-6, terminal) in fixed[3][0]
            assert (bottom-5, terminal-1) in fixed[2][0]
            for record in library:
                assert shift(record, point)[0] & blocked
            for relative in rotors:
                record = shift(relative, point)
                if record[0] & blocked:
                    continue
                if relative[0] == ROTOR_A:
                    column = terminal
                    kinds['RA'] += 1
                else:
                    assert relative[0] == ROTOR_B
                    column = terminal-2
                    kinds['RB'] += 1
                top = bottom-9, column
                anchor = bottom-8, column
                assert 7 <= column <= width+3
                assert top in record[1] and top not in blocked | record[0]
                assert set(neighbors(top)) & record[0] == {anchor}
                assert (bottom-10, column) in fixed[1][0]
                assert top[0] == bottom-9
                forced_rotors += 1
            patterns += 1
    assert patterns and all(kinds.values())
    terminal_controls = 0
    for bottom, width in itertools.product((24, 40), (6, 8, 12, 20, 50)):
        fixed = prescribed(bottom, width, 4)
        upward = independent_source((12, width+2, 4), (True, True, True), (bottom-4, width+9))
        successor = independent_source((8, width, 4), (True, True, True), (bottom-5, width+7))
        assert (bottom-6, 7) in successor[0]
        assert {(bottom-6, 6), (bottom-5, 7)} <= successor[1]
        assert (bottom-6, 6) in fixed[1][0] and (bottom-5, 7) in upward[0]
        terminal_controls += 1
    return dict(disjoint_short_leg_patterns=patterns, excluded_fixed_intersections=excluded,
                surviving_U_roles_at_first_site=0, forced_north_rotor_patterns=forced_rotors,
                rotor_types=kinds, each_rotor_forces_a_forbidden_original_top_support=True,
                rigid_terminal_support_controls=terminal_controls)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', top=top_controls(), rigidity=rigidity_controls(),
        scope='Finite controls for a written arbitrary-dimension two-stage support proof. '
              'No complete realization, joint target nonreuse or global ledger increment claimed.'), indent=2))
