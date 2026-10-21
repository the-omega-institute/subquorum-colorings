"""Full-original controls for the internal predecessor barrier and depth gap."""

import itertools
import json

from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    guards = roles = left_survivors = eleven = decisions = excluded = first_deep = 0
    examples = []
    for origin, offset, count, root_breadth in itertools.product(
            (-33, 31), (-100, 0, 200), (3, 6), (6, 40)):
        widths = [12+2*((3*index) % 7) for index in range(count)]
        depths = [24+2*((11*index) % 29) for index in range(count)]
        fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
        blocked = set.union(*(record[0] for record in fixed))
        assert len(blocked) == sum(len(record[0]) for record in fixed)
        for index in range(1, count):
            anchor, unused, lateral = sites[index]
            previous_anchor, unused, previous_lateral = sites[index-1]
            previous_depth = depths[index-1]
            column = lateral+widths[index]+13
            target = anchor-1, column
            predecessor = fixed[11*count+index]
            guard = {(row, column) for row in range(anchor-previous_depth+4, anchor-previous_depth+9)}
            footprint = {(row, column) for row in range(anchor-11, anchor)}
            assert anchor == previous_anchor+previous_depth-6
            assert column == previous_lateral+1
            assert guard == {(row, column) for row in range(previous_anchor-2, previous_anchor+3)}
            assert guard <= predecessor[0]
            assert target in bases[index][4][1] and target not in blocked
            assert not footprint & blocked
            guards += 1
            incident_values = sorted(set(range(4, previous_depth+8, 2)) | {100, 200})
            for breadth, incident, far, left in itertools.product(
                    (6, widths[index]+14, 100), incident_values, (4, 10, 80), (False, True)):
                candidate = north_U(anchor+3, column, breadth, incident, far, left)
                assert target in candidate[0]
                assert candidate[2]
                assert charge(candidate) == (-1 if left else 1)
                if incident >= previous_depth-8:
                    assert (anchor-previous_depth+8, column) in candidate[0] & predecessor[0]
                if not left and incident <= previous_depth:
                    assert (anchor-incident, column+1) in candidate[0] & blocked
                if not candidate[0] & blocked:
                    assert left and 10 <= incident <= previous_depth-10
                    assert footprint <= candidate[0]
                    left_survivors += 1
                if left and incident >= 10:
                    assert footprint <= candidate[0]
                    eleven += 1
                roles += 1
            if index+1 == count:
                continue
            next_anchor, unused, next_lateral = sites[index+1]
            breadth = widths[index]+widths[index+1]+26
            depth = depths[index]
            forbidden = footprint | {(anchor, column)}
            for incident, far in itertools.product(range(4, depth+30, 2), (4, 6, 8, 10, 20, 80)):
                parent = north_U(next_anchor, next_lateral, breadth, incident, far, False)
                interval = {(row, column) for row in range(anchor+depth-10-incident,
                                                          anchor+depth-10-incident+far+1)}
                assert interval <= parent[0]
                necessary = incident <= depth-12 or incident-far >= depth+2
                assert (not bool(interval & forbidden)) == necessary
                if not parent[0] & blocked:
                    assert target not in parent[0]
                    if not necessary:
                        assert footprint & parent[0]
                        excluded += 1
                decisions += 1
            parent = north_U(next_anchor, next_lateral, breadth, depth+4, 4, False)
            assert not parent[0] & blocked
            assert target not in parent[0]
            assert (anchor-10, column) in parent[0] & footprint
            first_deep += 1
            if origin == 31 and offset == 0 and root_breadth == 6 and count == 3:
                examples.append(dict(index=index, target=target,
                    predecessor_guard=sorted(guard), mandatory_footprint=sorted(footprint),
                    parent_dimensions=[breadth, depth+4, 4],
                    old_endpoint_collisions=0, forced_shared_endpoint=[anchor-10, column]))
    fixed, unused, unused, sites = old_chain(31, 0, [12, 12, 12], [24, 24, 24], 6)
    blocked = set.union(*(record[0] for record in fixed))
    next_anchor, unused, next_lateral = sites[2]
    parent = north_U(next_anchor, next_lateral, 50, 28, 4, False)
    assert not parent[0] & blocked and (39, 1) in parent[0]
    assert sites[1] == (49, 2, -24)
    print(json.dumps(dict(status='PASS', predecessor_guards=guards,
        full_original_U_role_controls=roles, old_disjoint_left_survivors=left_survivors,
        eleven_endpoint_controls=eleven, internal_depth_gap_decisions=decisions,
        old_disjoint_candidates_excluded_by_footprint=excluded,
        old_disjoint_first_deep_obstructions=first_deep,
        canonical_uniform_example=dict(target=[48, 1], parent_dimensions=[50, 28, 4],
            parent_chart_origin=[35, -49], old_endpoint_collisions=0, forced_shared_endpoint=[39, 1]),
        examples=examples,
        scope='Necessary conditions and an explicit nonextendibility obstruction in the '
              'complete full-U/rotor model; finite controls do not replace general proofs '
              'or establish complete extensions or a global bound.'), indent=2))


if __name__ == '__main__':
    main()
