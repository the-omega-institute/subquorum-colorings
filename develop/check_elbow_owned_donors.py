"""Local label checks and geometric controls for capped-corner owned donors."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import neighbors
from check_elbow_sources import elbow, sharp_flanks
from check_orthogonal_source_mouths import feasible
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def local_controls():
    valid = 0
    fixed = {(-1, 0): 2, (-1, 1): 2, (0, -1): 2, (1, -1): 1}
    corners = ((0, 0), (0, 1), (1, 0), (1, 1))
    outside = ((0, 2), (1, 2), (2, 0), (2, 1))
    for labels in itertools.product(range(3), repeat=8):
        state = dict(fixed)
        state.update(zip(corners+outside, labels))
        if state[0, 0] == 2 or state[0, 1] == 2:
            continue
        checked = corners+((1, -1),)
        if any(state.get(point) == 1 and sum(state.get(near, 0) != 0
                                            for near in neighbors(point)) > 1 for point in checked):
            continue
        if state[1, 1] == 2 and sum(state.get(near, 0) != 0
                                    for near in neighbors((1, 1))) < 3:
            continue
        assert all(state[point] != 2 for point in corners)
        assert sum(state[point] == 1 for point in corners) <= 1
        valid += 1
    return dict(all_local_labelings=3**8, valid_local_models=valid)


def oriented_template(width, height, symmetry, sharp=False):
    current = elbow(width, height, sharp_flanks(width) if sharp else ())
    transpose, flip_row, flip_column = symmetry

    def move(point):
        row, column = point[0]-6, point[1]-6
        row = 1-row if flip_row else row
        column = 1-column if flip_column else column
        return (column, row) if transpose else (row, column)

    return dict(endpoints={move(point) for point in endpoint_data(current)[0]},
                selected={move(point) for point in current[2]},
                matching=[tuple(move(point) for point in edge) for edge in current[3]])


def overlap_reason(first, second):
    if first['endpoints'] & second['endpoints']:
        return 'same_component_shared_endpoint'
    if any(set(neighbors(point)) & second['endpoints'] for point in first['endpoints']):
        return 'same_component_adjacent_endpoints'
    endpoints = first['endpoints'] | second['endpoints']
    selected = first['selected'] | second['selected']
    if endpoints & selected:
        return 'endpoint_selected_conflict'
    if any(len(set(neighbors(point)) & (endpoints | selected)) > 1 for point in selected):
        return 'selected_support_has_two_occupied_neighbors'
    raise AssertionError('Distinct feasible complete elbows would share one owned tile.')


def bundle(templates):
    selected, matching, owned = set(), [], []
    for index, source in enumerate(templates):
        move = lambda point: (point[0]+32, point[1]+32+64*index)
        selected.update(move(point) for point in source['selected'])
        matching.extend(tuple(move(point) for point in edge) for edge in source['matching'])
        owned.append({move(point) for point in itertools.product((0, 1), repeat=2)})
    current = 64, 64*len(templates), selected, matching
    assert feasible(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    checked = verify_terminal(current)
    assert len(endpoint_components(current)) == len(templates)
    assert [receiver['charge_twice'] for receiver in checked['receivers']] == [2]*len(templates)
    assert len(set.union(*owned)) == 4*len(owned)
    deficits = []
    for cells in owned:
        assert not cells & endpoints
        deficit = 2-len(cells & selected)
        assert deficit >= 1
        deficits.append(deficit)
    assert checked['area']//2-checked['objective'] == checked['empty_deficit']-len(templates)
    assert checked['empty_deficit'] >= sum(deficits) >= len(templates)
    return dict(components=len(templates), owned_deficits=deficits,
                total_physical_deficit=checked['empty_deficit'],
                half_area_deficit=checked['area']//2-checked['objective'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    symmetries = list(itertools.product((False, True), repeat=3))
    templates = [oriented_template(width, height, symmetry)
                 for width, height, symmetry in itertools.product((6, 8, 12), (4, 8), symmetries)]
    rejected = Counter(overlap_reason(first, second)
                       for first, second in itertools.product(templates, repeat=2))
    records = []
    for width, height, symmetry, sharp in itertools.product((6, 8, 12), (4, 8), symmetries,
                                                          (False, True)):
        source = oriented_template(width, height, symmetry, sharp)
        record = bundle([source])
        assert record['owned_deficits'] == [1 if sharp else 2]
        records.append(dict(width=width, height=height, symmetry=symmetry, sharp=sharp, **record))
    multiple = [bundle([oriented_template(8, 6, symmetries[index], sharp=True)
                        for index in range(count)]) for count in (2, 4, 8)]
    report = dict(status='ALL_CHECKS_PASSED', local_controls=local_controls(),
                  individual_oriented_cases=len(records), shared_tile_pair_attempts=sum(rejected.values()),
                  shared_tile_rejection_reasons=dict(rejected), multi_component_controls=multiple,
                  records=records,
                  scope='Finite local-label and geometric controls; the arbitrary-component witness '
                        'criterion and injectivity have a separate written proof. No universal grid claim.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}))


if __name__ == '__main__':
    main()
