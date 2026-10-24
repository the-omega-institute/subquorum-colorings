"""Original-source controls for the mandatory E-owner footprint and depth gap."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rotor_forms(target):
    forms = set()
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        record = module['endpoints'], module['selected'], {
            tuple(sorted(edge)) for edge in module['matching']}
        for endpoint in record[0]:
            if set(neighbors(endpoint)) & record[0] != {(endpoint[0]-1, endpoint[1])}:
                continue
            moved = shift(record, (target[0]-endpoint[0], target[1]-endpoint[1]))
            forms.add(tuple(sorted(moved[0])))
    assert len(forms) == 2
    return [set(form) for form in forms]


def main():
    old_controls = rotor_controls = shallow_controls = footprint_controls = phase_charge_controls = 0
    right_decisions = geometrically_legal = excluded_geometric = 0
    branch_obstructions = 0
    examples = []
    for origin, offset, root_breadth in itertools.product((-33, 31), (-100, 200), (6, 40)):
        widths, depths = [12, 14, 50, 16, 20], [24, 80, 26, 100, 24]
        fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
        blocked = set.union(*(record[0] for record in fixed))
        all_sites = []
        for index, (anchor, east, lateral) in enumerate(sites):
            column = lateral+widths[index]+13
            target = anchor-1, column
            footprint = {(row, column) for row in range(anchor-9, anchor)}
            assert target in bases[index][4][1] and target not in blocked
            assert {(anchor-1, column-1), (anchor, column), (anchor-1, column+1)} <= blocked
            assert not footprint & blocked
            assert {(row, column-1) for row in range(anchor-8, anchor+3)} <= blocked
            east_start = anchor-6 if index == 0 else anchor-depths[index-1]
            assert {(row, column+1) for row in range(east_start, anchor+1)} <= blocked
            all_sites += [target, (anchor-4, lateral)]
            old_controls += 1
            for form in rotor_forms(target):
                assert form & {(anchor-2, column-1), (anchor-2, column+1)}
                assert form & blocked
                rotor_controls += 1
            for breadth, incident, far, left in itertools.product(
                    (6, 14, 80), (4, 6, 8, 10, 24, 82, 102), (4, 10, 80), (False, True)):
                candidate = north_U(anchor+3, column, breadth, incident, far, left)
                assert target in candidate[0]
                half_legs = (incident+far)//2
                endpoint_tiles = {(row//2, lateral//2) for row, lateral in candidate[0]}
                inside_supports = {point for point in candidate[1]
                                   if (point[0]//2, point[1]//2) in endpoint_tiles}
                assert len(candidate[2]) == breadth+half_legs-1
                assert len(endpoint_tiles) == breadth//2+half_legs+int(not left)
                assert len(inside_supports) == half_legs+4*int(not left)
                assert charge(candidate) == (-1 if left else 1)
                phase_charge_controls += 1
                if incident >= 8:
                    assert footprint <= candidate[0]
                    footprint_controls += 1
                if left and incident <= 8:
                    assert (anchor-incident, column-1) in candidate[0] & blocked
                    shallow_controls += 1
                if not left and incident <= (6 if index == 0 else depths[index-1]):
                    assert (anchor-incident, column+1) in candidate[0] & blocked
                    shallow_controls += 1
            if index+1 == len(sites):
                continue
            current, unused, current_offset = sites[index+1]
            breadth = widths[index]+widths[index+1]+26
            for incident in range(4, depths[index]+22, 2):
                for far in (4, 6, 8, 10, 20, 40):
                    parent = north_U(current, current_offset, breadth, incident, far, False)
                    necessary = incident <= depths[index]-12 or incident-far >= depths[index]
                    if not parent[0] & blocked:
                        geometrically_legal += 1
                        assert target not in parent[0]
                        if not necessary:
                            assert parent[0] & footprint
                            excluded_geometric += 1
                    right_decisions += 1
            for raised, far in itertools.product((0, 2), (4, 6, 8, 10, 12, 24)):
                parent = north_U(current, current_offset, breadth, depths[index]+raised, far, False)
                assert (anchor-8, column) in parent[0] & footprint
                assert target not in parent[0] or parent[0] & blocked
                branch_obstructions += 1
            if origin == 31 and offset == 200 and root_breadth == 6:
                examples.append(dict(block=index, mandatory_support=target,
                    footprint=sorted(footprint), east_wall_start=east_start))
        assert len(set(all_sites)) == 2*len(sites)
        assert {sum(point) % 2 for point in all_sites} == {1}
    print(json.dumps(dict(status='PASS', old_original_geometry_controls=old_controls,
        rotor_collision_controls=rotor_controls, shallow_U_collision_controls=shallow_controls,
        full_original_physical_phase_charge_controls=phase_charge_controls,
        mandatory_nine_endpoint_controls=footprint_controls,
        arbitrary_depth_far_decisions=right_decisions,
        geometrically_legal_candidates=geometrically_legal,
        newly_excluded_geometric_candidates=excluded_geometric,
        prior_band_branch_obstructions=branch_obstructions, examples=examples,
        scope='Original support/endpoint/matching-role controls for an all-parameter written '
              'mandatory footprint proof. Both earlier right-band families have no complete '
              'extension. No sufficiency or global net compensation inferred from owner mass.'), indent=2))


if __name__ == '__main__':
    main()
