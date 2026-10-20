"""Transported-frame and conditional all-route occurrence-ledger controls."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cap_continuation_budget import phase_of
from check_minus_one_tip_obstructions import source
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def geometry_controls():
    counts = Counter()
    cardinal = ((-1, 0), (0, 1), (1, 0), (0, -1))
    frames = [(active, outward) for active in cardinal for outward in cardinal
              if sum(first*second for first, second in zip(active, outward)) == 0]
    for width, height, far, incident, owner_width, owner_far in itertools.product(
            (6, 8, 18), (8, 12, 20, 40), (4, 8), (4, 6, 10, 20), (6, 10), (4, 12)):
        if incident > height-4:
            continue
        root = transform_module(source(width, far, height),
                                (False, True, False), (height, -width))
        owner = transform_module(source(owner_width, owner_far, incident),
                                 (False, False, False), (1, -owner_width-1))
        if root['endpoints'] & owner['endpoints']:
            counts['overlapping_original_pairs'] += 1
            continue
        assert phase_of(root) == '10' and phase_of(owner) == '11'
        cap = {(2, -2), (2, -1), (3, -2), (3, -1)}
        assert owner['endpoints'] & cap == cap-{(3, -2)}
        terminal = incident+1, -1
        candidate = incident+2, -1
        assert terminal in owner['endpoints'] and candidate in owner['selected']
        opposite = tuple(value+1 if value % 2 == 0 else value-1 for value in candidate)
        displacement = tuple(other-value for value, other in zip(candidate, opposite))
        assert displacement == (1, -1)
        admissible = [(active, outward) for active, outward in frames if outward == (1, 0)
                      and tuple(-first+second for first, second in zip(active, outward)) == displacement]
        assert admissible == [((0, 1), (1, 0))]
        active_endpoint = candidate[0], candidate[1]+1
        assert active_endpoint == (incident+2, 0)
        assert active_endpoint in root['endpoints']
        counts['phase10_wall_blocks_required_phase01_endpoint'] += 1
    assert counts['phase10_wall_blocks_required_phase01_endpoint'] > 0
    return dict(counts=counts, cardinal_frames=len(frames), complete_critical_U10_events=0,
                scope='Endpoint-disjoint G/V pairs and exact transported-frame controls only; '
                      'no complete critical A/B/C/D event realization.')


def ledger_controls():
    counts = Counter()
    parameters = itertools.product(range(4), range(3), range(3), range(3), range(3),
                                   range(3), range(3))
    for phase11, route_b_cap, route_d_cap, interior_b, interior_d, route_c, negative_sources in parameters:
        available = 2*phase11-route_b_cap-route_d_cap
        if available < 0:
            continue
        for route_a in range(available+1):
            unselected = available-route_a
            route_b = route_b_cap+interior_b
            route_d = route_d_cap+interior_d
            all_routes = route_a+route_b+route_c+route_d
            old_reservations, activation_slack, rotor, boundary, unused = 1, 1, 0, 1, 1
            original = 2*(phase11-negative_sources)+old_reservations+2*route_c+interior_d+interior_b
            rewritten = all_routes+route_c-2*negative_sources+old_reservations+unselected
            assert original == rewritten
            twice_reserve = original+activation_slack+rotor+boundary+unused
            assert twice_reserve == rewritten+activation_slack+rotor+boundary+unused
            assert rewritten+rotor+boundary <= twice_reserve
            counts['conditional_all_route_identities'] += 1
            if unselected:
                counts['positive_cap_complement'] += 1
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = dict(status='PASS', geometry=geometry_controls(), ledgers=ledger_controls(),
                  scope='Finite source/frame and conditional arithmetic controls supplement the written '
                        'all-parameter nonreuse proof and Lean primitives; no global allocation or grid equality.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
