"""Independent finite controls for all-gap upward rigidity and target transfer."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_first_consumer import prescribed
from check_secondary_ten_terminal_rigidity import ROTOR_A, ROTOR_B
from check_secondary_ten_tight_transfer import square_depth_controls


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def relative_endpoints(endpoints, point):
    return {(row-point[0], column-point[1]) for row, column in endpoints}


def obstruction_controls():
    horizontal, horizontal_rotors = axial_library({(0, -1), (0, 1)})
    northwest, northwest_rotors = axial_library({(-1, 0), (0, -1)})
    top_sites = first_sites = first_U_roles = first_rotor_roles = 0
    north_A = north_B = west_boundary = right_boundary = 0
    for bottom, width, gap in itertools.product((24, 60), (6, 8, 10, 14, 20, 50), (2, 4, 8, 20)):
        incident = width+gap
        secondary = prescribed(bottom, width, 4)[1]
        east = independent_source((20, incident, 4), (True, True, True), (bottom-4, incident+7))
        assert not secondary[0] & east[0]
        blocked = secondary[0] | east[0]
        for column in range(7, width+5):
            point = bottom-9, column
            local = relative_endpoints(blocked, point)
            assert point not in blocked
            assert (bottom-10, column) in secondary[0]
            assert (bottom-9, 6) in secondary[0] and (bottom-9, width+5) in secondary[0]
            assert all(record[0] & local for record in horizontal+horizontal_rotors)
            if column == width+4:
                assert (bottom-9, column+1) in secondary[0]
                right_boundary += 1
            top_sites += 1
        for terminal in range(8, width+6):
            point = bottom-6, terminal-1
            local = relative_endpoints(blocked | {(bottom-6, terminal)}, point)
            assert (bottom-5, terminal-1) in east[0]
            assert point not in blocked
            for record in northwest:
                assert record[0] & local
                first_U_roles += 1
            for relative in northwest_rotors:
                if relative[0] & local:
                    if terminal == 8 and (-2, -1) in relative[0]:
                        assert (bottom-8, 6) in secondary[0]
                        west_boundary += 1
                    continue
                record = shift(relative, point)
                if relative[0] == ROTOR_A:
                    assert terminal <= width+4
                    top_column = terminal
                    north_A += 1
                else:
                    assert relative[0] == ROTOR_B and terminal >= 9
                    top_column = terminal-2
                    north_B += 1
                top = bottom-9, top_column
                anchor = bottom-8, top_column
                assert 7 <= top_column <= width+4
                assert top in record[1] and top not in record[0] | blocked
                assert set(neighbors(top)) & record[0] == {anchor}
                assert (bottom-10, top_column) in secondary[0]
                first_rotor_roles += 1
            first_sites += 1
    assert all((north_A, north_B, west_boundary, right_boundary))
    return dict(top_sites=top_sites, first_support_sites=first_sites,
                bounded_first_U_roles_excluded=first_U_roles,
                surviving_north_rotor_roles_forcing_forbidden_support=first_rotor_roles,
                north_A=north_A, north_B=north_B,
                left_boundary_D_blockers=west_boundary,
                right_boundary_D_blockers=right_boundary,
                original_U_dimensions_max=18,
                H_not_used_for_local_obstruction=True)


def successor_controls():
    shortened = rigid = even_bar = disjoint = excluded = 0
    for bottom, width, gap, breadth, far, span, other in itertools.product(
            (40,), (6, 10, 18), (2, 4, 8), (12, 20), (4, 10), (6, 8, 12), (4, 8)):
        incident = width+gap
        fixed = prescribed(bottom, width, 4)
        east = independent_source((breadth, incident, far),
                                  (True, True, True), (bottom-4, incident+7))
        fixed.append(east)
        if any(first[0] & second[0] for first, second in itertools.combinations(fixed, 2)):
            continue
        for bar in range(width+7, incident+6):
            for near in range(4, bar-6, 2):
                if near < bar-width-5:
                    continue
                successor = independent_source((span, near, other),
                                               (True, True, True), (bottom-5, bar))
                if any(successor[0] & record[0] for record in fixed):
                    excluded += 1
                    continue
                terminal = bar-near
                disjoint += 1
                assert 7 <= terminal <= width+5
                if terminal == 7:
                    assert bar % 2 == 1 and width <= near <= incident-2
                    assert charge(successor) == 1
                    assert (bottom-6, 7) in successor[0]
                    assert {(bottom-6, 6), (bottom-5, 7)} <= successor[1]
                    assert (bottom-6, 6) in fixed[1][0] and (bottom-5, 7) in east[0]
                    rigid += 1
                else:
                    assert terminal >= 8
                    point = bottom-6, terminal-1
                    assert point in successor[1]
                    assert point not in successor[0] | set.union(*(record[0] for record in fixed))
                    assert set(neighbors(point)) & successor[0] == {(bottom-6, terminal)}
                    assert (bottom-5, terminal-1) in east[0]
                    shortened += 1
                    even_bar += bar % 2 == 0
    assert all((rigid, shortened, even_bar))
    return dict(disjoint_partial_successor_stencils=disjoint,
                excluded_endpoint_intersections=excluded,
                rigid_positive_stencils=rigid, forced_short_terminal_stencils=shortened,
                forced_even_bar_stencils=even_bar,
                complete_actual_marked_chain_realization=False)


def frame_controls():
    compositions = witnesses = 0
    for bottom, near, row, column in itertools.product((-20, 30, 100), (6, 10, 18, 40), range(4), range(1, 7)):
        target = bottom-5-column, near+7-row
        old_S = near+3-row, 3-column
        old_P = column+2, row+2
        old_E = column+2, near+3-row
        old_companion_S = near+3-row, column+2
        assert (bottom-8+old_S[1], old_S[0]+4) == target
        assert (bottom-3-old_P[0], near+9-old_P[1]) == target
        assert (bottom-3-old_E[0], old_E[1]+4) == target
        assert (bottom-3-old_companion_S[1], old_companion_S[0]+4) == target
        compositions += 4
        producer = independent_source((near+4, 4, 4), (False, False, False), (0, 0))
        assert {(0, near+3), (1, near+2)} <= producer[0]
        assert (bottom-3, near+9-(near+3)) == (bottom-3, 6)
        assert (bottom-4, near+9-(near+2)) == (bottom-4, 7)
        witnesses += 1
    return dict(arbitrary_incident_frame_compositions=compositions,
                old_P_mandatory_endpoint_pairs=witnesses)


def ledger_controls():
    parity = ledgers = 0
    for baseline, added in itertools.product(range(-40, 41), range(21)):
        gain = (baseline+added+1)//2-(baseline+1)//2
        assert gain in (added//2, (added+1)//2)
        assert (baseline+added+3)//2-(baseline+added+1)//2 == 1
        parity += 1
    for unmarked, upper, pairs, m8, resolved, residual, old, extra, added, caps in itertools.product(
            range(2), range(2), range(2), range(2), range(2), range(5), range(2), range(2), range(3), range(2)):
        if added > residual:
            continue
        total = old+caps+resolved+residual
        positive = unmarked+(total+1)//2
        reserve = (old+extra+added+m8+caps+2*pairs+2*upper+1)//2
        bound = unmarked+upper+pairs+(m8-resolved-residual+extra+added+1)//2
        assert positive+reserve-total >= bound
        if resolved+residual <= 2*unmarked+2*upper+2*pairs+m8+extra+added+1:
            assert positive+reserve-total >= 0
        ledgers += 1
    return dict(parity_controls=parity, same_inventory_bound_controls=ledgers)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', obstruction=obstruction_controls(),
                         successors=successor_controls(), frames=frame_controls(),
                         intrinsic_depth=square_depth_controls(), ledger=ledger_controls(),
                         scope='Finite validation of separately written all-gap support proof and '
                         'actual-label compensation. Local obstruction uses Q/D/E only; H belongs '
                         'to the global actual-chain dependency. No complete realizability, '
                         'unrestricted allocation or grid equality is inferred.'), indent=2))
