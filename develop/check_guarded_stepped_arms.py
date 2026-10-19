"""Physical controls for guarded donors, stepped arms and mixed ownership."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal, vertices_of
from check_cooperative_promotion import neighbors
from check_elbow_owned_donors import oriented_template, overlap_reason
from check_orthogonal_source_mouths import feasible
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from search_corner_coverage import witnesses


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def stepped(k):
    assert k >= 1
    bottom = 2*k+4
    matching = [((0, 0), (0, 1)), ((0, 2), (0, 3)), ((1, 0), (1, 1)),
                ((1, 2), (2, 2)), ((1, 3), (2, 3)), ((2, 0), (2, 1)),
                ((2, 4), (2, 5)), ((3, 1), (3, 2)), ((3, 3), (3, 4)),
                ((3, 0), (4, 0)), ((3, 5), (4, 5))]
    for row in range(4, bottom, 2):
        matching.extend([((row, 1), (row+1, 1)), ((row, 2), (row+1, 2)),
                         ((row+1, 0), (row+2, 0)), ((row+1, 5), (row+2, 5))])
    matching.append(((bottom, 1), (bottom, 2)))
    selected = {(-1, 1), (0, -1), (0, 4), (2, -1), (2, 6), (bottom, 3),
                (bottom+1, 0), (bottom+1, 2), (bottom+1, 5)}
    selected |= {(row, column) for row in range(4, bottom+1, 2) for column in (-1, 6)}
    selected |= {(row, 4) for row in range(5, bottom, 2)}
    endpoints = {(row, column) for row in (0, 1) for column in range(4)}
    endpoints |= {(row, column) for row in (2, 3) for column in range(6)}
    endpoints |= {(row, column) for row in range(4, bottom+1) for column in (0, 1, 2, 5)}
    assert {point for edge in matching for point in edge} == endpoints
    order = [(bottom, column) for column in (0, 2, 5)]
    order += [(row, column) for row in range(bottom-2, 3, -2) for column in (0, 5)]
    order += [(2, 0), (2, 5)]
    order += [(row, 1) for row in range(bottom-1, 4, -2)]
    order += [(3, 1), (2, 2), (3, 4), (1, 1), (2, 3), (0, 0), (0, 3),
              (0, 1), (0, 2), (1, 2), (1, 3), (3, 2), (2, 1), (3, 3),
              (1, 0), (2, 4), (3, 0), (3, 5)]
    order += [(row, 2) for row in range(4, bottom, 2)]
    order += [point for row in range(4, bottom, 2) for point in ((row, 1), (row+1, 0))]
    order += [(bottom, 1)]
    order += [(row, 2) for row in range(bottom-1, 4, -2)]
    order += [(row, 5) for row in range(5, bottom, 2)]
    assert len(order) == len(set(order)) == len(endpoints)
    mates = {point: mate for edge in matching for point, mate in (edge, edge[::-1])}
    frozen = set()
    for point in order:
        retained = selected | {mates[previous] for previous in frozen}
        assert len(set(neighbors(point)) & retained) >= 2, (k, point)
        frozen.add(point)
    assert frozen == endpoints
    return dict(endpoints=endpoints, selected=selected, matching=matching, bottom=bottom)


def transform(source, symmetry):
    transpose, flip_row, flip_column = symmetry

    def move(point):
        row, column = point[0]-source['bottom'], point[1]-3
        row = 1-row if flip_row else row
        column = 1-column if flip_column else column
        return (column, row) if transpose else (row, column)

    return dict(endpoints={move(point) for point in source['endpoints']},
                selected={move(point) for point in source['selected']},
                matching=[tuple(move(point) for point in edge) for edge in source['matching']])


def inspect(k, symmetry):
    source = transform(stepped(k), symmetry)
    margin = 2*k+12
    move = lambda point: (point[0]+margin, point[1]+margin)
    current = (2*margin+4, 2*margin+4, {move(point) for point in source['selected']},
               [tuple(move(point) for point in edge) for edge in source['matching']])
    endpoints = endpoint_data(current)[0]
    assert feasible(current)
    assert frozen_certificate(current)[0] == endpoints
    checked = verify_terminal(current)
    assert len(checked['receivers']) == 1
    receiver = checked['receivers'][0]
    assert (receiver['endpoints'], receiver['tiles'], receiver['selected'],
            receiver['charge_twice']) == (8*k+24, 3*k+10, 2*k+9, 2)
    assert not witnesses(*current[:2], current[2], endpoints)
    donor = {(margin+row, margin+column) for row, column in itertools.product((0, 1), repeat=2)}
    assert len(donor & current[2]) == 1 and not donor & endpoints
    receiver_cells = vertices_of({(row//2, column//2) for row, column in endpoints})
    for point in receiver_cells-endpoints-current[2]:
        adjacent = set(neighbors(point))
        assert len(adjacent & endpoints) >= 2 or any(
            set(neighbors(support)) & endpoints for support in adjacent & current[2])
    return dict(k=k, symmetry=symmetry, **receiver, owned_deficit=1)


def local_guard_controls():
    valid = 0
    fixed = {(0, 0): 1, (0, -1): 2, (1, 2): 1, (0, 2): 2}
    variable = ((-1, 0), (0, 1), (1, 0), (1, 1), (2, 2), (1, 3))
    for labels in itertools.product(range(3), repeat=len(variable)):
        state = dict(fixed)
        state.update(zip(variable, labels))
        if any(sum(state.get(point, 0) != 0 for point in neighbors(support)) > 1
               for support in ((0, 0), (1, 2))):
            continue
        assert all(state[point] == 0 for point in ((0, 1), (1, 0), (1, 1)))
        valid += 1
    return dict(local_models=3**len(variable), valid_models=valid)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    symmetries = list(itertools.product((False, True), repeat=3))
    lengths = list(range(1, 17))+[24, 32, 64]
    records = [inspect(k, symmetry) for k, symmetry in itertools.product(lengths, symmetries)]
    new = [transform(stepped(k), symmetry) for k, symmetry in itertools.product((1, 2, 5), symmetries)]
    old = [oriented_template(width, height, symmetry) for width, height, symmetry in
           itertools.product((6, 8), (4, 8), symmetries)]
    same_type = Counter(overlap_reason(first, second) for first, second in itertools.product(new, repeat=2))
    cross_type = Counter(overlap_reason(first, second) for first, second in itertools.product(new, old))
    report = dict(status='ALL_CHECKS_PASSED', local=local_guard_controls(),
                  lengths=lengths, oriented_cases=len(records), records=records,
                  new_new_shared_tile_attempts=sum(same_type.values()),
                  new_new_reasons=dict(same_type), old_new_shared_tile_attempts=sum(cross_type.values()),
                  old_new_reasons=dict(cross_type),
                  scope='Finite physical controls for the written all-k freezing/count proof and '
                        'general guarded/old mixed ownership. No universal grid conclusion.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}))


if __name__ == '__main__':
    main()
