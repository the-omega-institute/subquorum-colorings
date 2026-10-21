"""Full-original controls for the two-direction cavity and depth-eight exclusion."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import shift
from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain
from check_secondary_ten_batch_terminal_budget import key
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def guards(width):
    return ({(-1, column) for column in range(width+1)} |
            {(4, column) for column in range(width)} |
            {(0, width)} | {(row, -1) for row in range(3)})


def aligned_U_roles():
    roles = {}
    for dimensions in itertools.product((6, 14, 50), (4, 8, 100), (4, 8, 100)):
        for symmetry in itertools.product((False, True), repeat=3):
            source = independent_source(dimensions, symmetry, (0, 0))
            for anchor in source[0]:
                adjacent = {(row-anchor[0], column-anchor[1])
                            for row, column in set(neighbors(anchor)) & source[0]}
                if adjacent <= {(0, 1), (1, 0)}:
                    moved = shift(source, (-anchor[0], -anchor[1]))
                    roles[key(moved)] = moved
    return list(roles.values())


def U_controls():
    roles = aligned_U_roles()
    counts = dict(south_terminal_or_corner=0, east_crosses_wall=0,
                  east_upper_bar=0, east_lower_bar=0)
    for width, source in itertools.product((24, 62, 500), roles):
        adjacent = set(neighbors((0, 0))) & source[0]
        assert adjacent in ({(0, 1)}, {(1, 0)}, {(0, 1), (1, 0)})
        if (1, 0) in adjacent:
            witness, phase = (4, 0), 'south_terminal_or_corner'
        else:
            incident = max(column for row, column in source[0] if row == 0)
            assert incident >= 4
            if incident >= width:
                witness, phase = (0, width), 'east_crosses_wall'
            elif (-1, incident) in source[0]:
                witness, phase = (-1, incident), 'east_upper_bar'
            else:
                witness, phase = (4, incident), 'east_lower_bar'
        assert witness in source[0] & guards(width)
        counts[phase] += 1
    assert all(counts.values())
    return dict(aligned_full_original_U_roles=len(roles),
                explicit_collision_controls=len(roles)*3, phases=counts)


def rotor_controls():
    roles = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        source = module['endpoints'], module['selected'], {
            tuple(sorted(edge)) for edge in module['matching']}
        for anchor in source[0]:
            adjacent = {(row-anchor[0], column-anchor[1])
                        for row, column in set(neighbors(anchor)) & source[0]}
            if adjacent <= {(0, 1), (1, 0)}:
                moved = shift(source, (-anchor[0], -anchor[1]))
                roles[key(moved)] = moved
    assert len(roles) == 4
    controls = 0
    for width, source in itertools.product((24, 62, 500), roles.values()):
        assert source[0] & {(2, -1), (1, -1), (-1, 1), (-1, 2)} & guards(width)
        controls += 1
    return dict(exhaustive_fixed_rotor_roles=len(roles), collision_controls=controls)


def retained_controls():
    cases = guard_sites = 0
    for origin, offset, old_width, width, depth, count in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80), (2, 7)):
        widths = [old_width, width]+[12]*(count-2)
        depths = [depth]+[24]*(count-1)
        fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, 40)
        current_origin, unused, current_offset = sites[1]
        column = offset+old_width+13
        parent = north_U(current_origin, current_offset, old_width+width+26, depth+4, 4, False)
        receiver = north_U(origin+3, column, 42, 8, 2000, False)
        for breadth, far in itertools.product((6, width+12), (4, depth-4)):
            consumer = north_U(origin, offset, breadth, 8, far, True)
            records = fixed+[parent, receiver, consumer]
            endpoints = set.union(*(source[0] for source in records))
            assert len(endpoints) == sum(len(source[0]) for source in records)
            point = origin-12, offset+1
            assert point in consumer[1] and point not in endpoints
            assert (point[0]-1, point[1]) in parent[0]
            assert (point[0], point[1]-1) in consumer[0]
            assert set(neighbors(point))-endpoints == {
                (point[0]+1, point[1]), (point[0], point[1]+1)}
            guard = {(point[0]+row, point[1]+column)
                     for row, column in guards(old_width+12)}
            assert guard <= parent[0] | consumer[0] | repairs[0][0]
            cases += 1
            guard_sites += len(guard)
    return dict(endpoint_disjoint_inventories=cases,
                missing_original_support_and_two_foreign_neighbors=cases,
                retained_guard_endpoint_memberships=guard_sites)


def reflected_receiver_controls():
    cases = guard_sites = 0
    phases = dict(incident_six=0, tight_incident_four=0)
    for origin, offset, old_width, width, depth, count in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80), (2, 7)):
        widths = [old_width, width]+[12]*(count-2)
        depths = [depth]+[24]*(count-1)
        fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, 40)
        current_origin, unused, current_offset = sites[1]
        column = offset+old_width+13
        parent = north_U(current_origin, current_offset, old_width+width+26, depth+4, 4, False)
        receiver = north_U(origin+3, column, 42, 8, 2000, False)
        for incident, breadth in ((6, 6), (6, width+12), (4, width+12)):
            for far in (4, depth+incident-12):
                consumer = north_U(origin, offset, breadth, incident, far, True)
                records = fixed+[parent, receiver, consumer]
                endpoints = set.union(*(source[0] for source in records))
                assert len(endpoints) == sum(len(source[0]) for source in records)
                point = origin-9, column-1
                assert point in receiver[1] and point not in endpoints
                assert (point[0], point[1]+1) in receiver[0]
                assert (point[0]+1, point[1]) in repairs[0][0]
                assert set(neighbors(point))-endpoints == {
                    (point[0]-1, point[1]), (point[0], point[1]-1)}
                cavity_width = old_width+12 if incident == 6 else old_width+width+24
                guard = {(point[0]-row, point[1]-column)
                         for row, column in guards(cavity_width)}
                assert guard <= parent[0] | receiver[0] | consumer[0] | repairs[0][0]
                phases['incident_six' if incident == 6 else 'tight_incident_four'] += 1
                cases += 1
                guard_sites += len(guard)
    return dict(endpoint_disjoint_prefixes=cases, phases=phases,
                absent_receiver_support_and_two_foreign_neighbors=cases,
                reflected_guard_endpoint_memberships=guard_sites)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', U_roles=U_controls(), rotors=rotor_controls(),
        retained=retained_controls(), reflected_receiver=reflected_receiver_controls(),
        scope='Controls of a separate all-parameter cavity proof. The U cases use arbitrary '
              'dimensions in the written proof; their finite sample is not catalogue '
              'exhaustion. The rotor table is finite and exhausts its fixed isometries. '
              'No complete extension or global bound is constructed.'), indent=2))
