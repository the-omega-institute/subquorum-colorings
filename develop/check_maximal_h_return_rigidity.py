"""Check maximal-return H rigidity stencils against original source catalogues."""

import itertools
import json

from check_component_receivers import vertices_of
from check_long_horizontal_corner_channel import specifications
from check_pair_transfer_protected_defects import original, rectangle_points
from check_persistent_corridor_capacity import certificates
from check_source_retention_closure import feasible


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rigidity_controls():
    patterns = forced_stencils = matched_pairs = 0
    for incident, width, far in itertools.product(
            (6, 8, 12, 20, 38), (6, 8, 12, 22), (4, 6, 12, 28)):
        returning = original((6, incident, incident-2),
                             (False, True, False), (incident+3, 1))
        for near in range(4, incident, 2):
            corner = original((width, near, far), offset=(3, 2))
            endpoints = returning['endpoints'] | corner['endpoints']
            assert len(endpoints) == len(returning['endpoints'])+len(corner['endpoints'])
            inside, boundary = rectangle_points((4, incident+2, 2, 7))
            assert boundary <= endpoints
            assert not {point for point in inside if point[1] == 6} & endpoints
            reflected = {(row, 9-column) for row, column in inside & endpoints}
            assert not {point for point in reflected if point[1] == 3}
            if near < incident-2:
                forced = (near+4, 3)
                assert forced in inside & corner['selected']
                assert forced not in endpoints
                assert {(near+3, 3), (near+4, 2)} <= endpoints
                forced_stencils += 1
            else:
                channel, boundary = rectangle_points((4, incident+2, 3, 7))
                assert boundary <= endpoints and not channel & endpoints
                tile = vertices_of({(2, 2)})
                assert tile & endpoints == {(4, 4), (4, 5)}
                assert not tile & corner['selected']
                matched_pairs += 1
            patterns += 1
    return dict(two_owner_patterns=patterns, impossible_short_near_stencils=forced_stencils,
                matched_permanent_pair_profiles=matched_pairs)


def complete_controls():
    checked = 0
    for stretch in (0, 2, 6, 18, 60):
        modules = [original(*specification) for specification in specifications(stretch)]
        assert feasible(modules, frozenset(range(len(modules))))
        _, _, lower, _ = certificates(modules)
        assert (2, 2) in lower
        checked += 1
    return checked


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', rigidity=rigidity_controls(),
                         complete_unbounded_family_instances=complete_controls(),
                         scope='Original endpoint/support coordinate controls and existing complete '
                               'family instances; no bounded search is used as a nonextension proof. '
                               'Arbitrary-extension rigidity follows from the written reflected '
                               'four-column barrier and original-support forcing.'), indent=2))
