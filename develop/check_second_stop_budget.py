"""Exact nonfull-pair catalogue and original support ownership controls."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_minus_one_tip_obstructions import source
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    pairs = ((0, 1), (0, 2), (1, 3), (2, 3))
    counts = Counter()
    for labels in itertools.product((None, 0, 1), repeat=4):
        if None not in labels:
            continue
        counts['nonfull_original_owner_labelings'] += 1
        for first, second in itertools.product(pairs, repeat=2):
            first_owner = labels[first[0]]
            second_owner = labels[second[0]]
            if first_owner is None or second_owner is None:
                continue
            if labels[first[1]] != first_owner or labels[second[1]] != second_owner:
                continue
            assert first_owner == second_owner
            counts['two_original_pair_occurrences'] += 1
    for width, active, far in itertools.product((6, 14, 30), range(4, 34, 2), (4, 10)):
        parent = transform_module(source(width, active, far), (False, False, False),
                                  (2-active, -1))
        assert phase_of(parent) == '01'
        for tile in parent['receiver']:
            cells = vertices_of({tile})
            endpoints = cells & parent['endpoints']
            if len(endpoints) != 2:
                continue
            supports = cells & parent['selected']
            assert len(supports) == 1
            assert sum(abs(first-second) for first, second in zip(*sorted(endpoints))) == 1
            counts['original_phase01_regular_pair_supports'] += 1
        for child_width in range(6, active-3, 2):
            point = (1-child_width, 1)
            cells = vertices_of({tile_of(point)})
            assert cells & parent['selected'] == {point}
            assert cells & parent['endpoints'] == {(point[0]-1, 0), (point[0], 0)}
            for missing in cells-{point}-(cells & parent['endpoints']):
                assert sum(abs(first-second) for first, second in zip(point, missing)) == 1
                assert any(sum(abs(first-second) for first, second in zip(anchor, missing)) == 1
                           for anchor in cells & parent['endpoints'])
            counts['second_receiver_exact_original_2P1T_stencils'] += 1
    result = dict(status='PASS', counts=dict(counts), complete_feasible_second_stop_coverage=0,
                  scope='Exact four-corner nonfull owner catalogue and independently reconstructed '
                  'phase01 original regular pair/support geometry. Second-receiver stencils '
                  'are partial; no claimed complete feasible second-stop, AA or full-grid coverage. '
                  'Shared H budget uses the general written pair packing and original-support uniqueness proof.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(counts), complete_feasible_second_stop_coverage=0)))


if __name__ == '__main__':
    main()
