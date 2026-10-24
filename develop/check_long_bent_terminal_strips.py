"""Control remote strip payment and geometric exclusion of overlapping claims."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_saturated_bent_bands import long_bent


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def terminal_strip(width, depth):
    return {(row, column) for row in (2*depth+4, 2*depth+5)
            for column in range(4, width+2)}


def selected_degree_ok(previous, current, following):
    return all(((current >> (1-row)) & 1)+((previous >> row) & 1)+
               ((following >> row) & 1) <= 1
               for row in range(2) if current >> row & 1)


def strip_optimum(columns):
    states = {(0, 0): 0}
    for index in range(columns):
        following_states = {}
        for (previous, current), value in states.items():
            for following in ((0,) if index in (0, columns-1) else range(4)):
                if selected_degree_ok(previous, current, following):
                    key = current, following
                    following_states[key] = max(following_states.get(key, -1),
                                                value+following.bit_count())
        states = following_states
    return max(value for (previous, current), value in states.items()
               if selected_degree_ok(previous, current, 0))


def oriented(points, turns, mirror):
    result = {(row, 1-column if mirror else column) for row, column in points}
    for _ in range(turns):
        result = {(column, 1-row) for row, column in result}
    return result


def controls():
    records = []
    for width in range(8, 41, 2):
        assert strip_optimum(width-2) == width-4
        for depth in (1, 2, 5, 16):
            filled, _ = long_bent(width, depth)
            strip = terminal_strip(width, depth)
            assert not strip & endpoint_data(filled)[0]
            assert len(strip) == 2*(width-2)
            assert len(filled[2] & strip) <= width-4
            sparse, _ = long_bent(width, depth, saturate=False)
            selected = sparse[2] | {(row, column+3)
                                    for row in (2*depth+4, 2*depth+5)
                                    for column in range(3, width-2, 2)}
            sharp = (*sparse[:2], selected, sparse[3])
            direct_check(*sharp)
            assert frozen_certificate(sharp)[0] == endpoint_data(sharp)[0]
            receiver = verify_terminal(sharp)['receivers'][0]
            assert receiver['charge_twice'] == 2
            count = len(selected & strip)
            assert count == width-4
            deficit = width-2-count
            assert deficit == 2
            records.append(dict(width=width, depth=depth, strip_selected=count,
                                strip_deficit=deficit, source_charge=1,
                                compensated_charge=-1))
    first, _ = long_bent(8, 2)
    first_endpoints = endpoint_data(first)[0]
    first_strip = terminal_strip(8, 2)
    first_neighbors = {(row+vertical, column+horizontal)
                       for row, column in first_endpoints
                       for vertical, horizontal in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    overlaps = parallel = perpendicular = 0
    for width, depth, turns, mirror in itertools.product((8, 10, 16), (1, 2, 5),
                                                         range(4), (False, True)):
        second, _ = long_bent(width, depth)
        endpoints = oriented(endpoint_data(second)[0], turns, mirror)
        strip = oriented(terminal_strip(width, depth), turns, mirror)
        first_tiles = {(row//2, column//2) for row, column in first_strip}
        second_tiles = {(row//2, column//2) for row, column in strip}
        offsets = {(2*(first_row-second_row), 2*(first_column-second_column))
                   for first_row, first_column in first_tiles
                   for second_row, second_column in second_tiles}
        for vertical, horizontal in offsets:
            moved_endpoints = {(row+vertical, column+horizontal) for row, column in endpoints}
            moved_strip = {(row+vertical, column+horizontal) for row, column in strip}
            assert moved_strip & first_strip
            overlaps += 1
            parallel += turns % 2 == 0
            perpendicular += turns % 2 == 1
            violates_clear_strip = bool(first_endpoints & moved_strip or
                                        moved_endpoints & first_strip)
            joins_components = bool(moved_endpoints & (first_endpoints | first_neighbors))
            assert violates_clear_strip or joins_components, (width, depth, turns, mirror,
                                                              vertical, horizontal)
    fixture, _ = long_bent(10, 2, saturate=False)
    tip = 6
    move = lambda vertex: (vertex[0]+2, vertex[1]+3)
    points = [(tip-1, 3), (tip, 3), (tip+1, 3), (tip+2, 3)]
    supports = {(tip-2, 3), (tip+3, 3), (tip-1, 4), (tip, 2),
                (tip+1, 4), (tip+2, 2)}
    matching = fixture[3]+[(move(points[0]), move(points[1])),
                           (move(points[2]), move(points[3]))]
    fixture = (*fixture[:2], fixture[2] | {move(point) for point in supports}, matching)
    assert direct_check(*fixture) == 37
    checked = verify_terminal(fixture)
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0, 2]
    assert frozen_certificate(fixture)[0] == endpoint_data(fixture)[0]
    crossing = endpoint_data(fixture)[0] & terminal_strip(10, 2)
    assert len(crossing) == 2
    source, _ = long_bent(8, 2, saturate=False)
    source_selected = source[2] | {(row, column+3)
                                   for row in (8, 9) for column in (3, 5)}
    mixed_selected, mixed_matching, mixed_strips = set(), [], []
    for turns, (base_row, base_column) in enumerate(((0, 0), (0, 40), (40, 0), (40, 40))):
        points = oriented(source_selected | endpoint_data(source)[0], turns, False)
        vertical = base_row-2*(min(row for row, column in points)//2)
        horizontal = base_column-2*(min(column for row, column in points)//2)
        moved = lambda values: {(row+vertical, column+horizontal)
                                 for row, column in oriented(values, turns, False)}
        mixed_selected.update(moved(source_selected))
        mixed_matching.extend(tuple(next(iter(moved({endpoint}))) for endpoint in edge)
                              for edge in source[3])
        mixed_strips.append(moved(terminal_strip(8, 2)))
    mixed = 80, 80, mixed_selected, mixed_matching
    mixed_checked = verify_terminal(mixed)
    assert len(mixed_checked['receivers']) == 4
    assert all(receiver['charge_twice'] == 2 for receiver in mixed_checked['receivers'])
    assert frozen_certificate(mixed)[0] == endpoint_data(mixed)[0]
    assert all(not first & second for first, second in itertools.combinations(mixed_strips, 2))
    assert all(not strip & endpoint_data(mixed)[0] for strip in mixed_strips)
    assert all(len(strip)//2-len(strip & mixed_selected) == 2 for strip in mixed_strips)
    return dict(status='ALL_CHECKS_PASSED', sharp_family_cases=len(records),
                strip_dynamic_program_widths=17, overlapping_placement_cases=overlaps,
                parallel_overlap_cases=parallel, perpendicular_overlap_cases=perpendicular,
                endpoint_free_hypothesis_not_automatic=dict(
                    shape=fixture[:2], selected=sorted(fixture[2]), matching=fixture[3],
                    objective=37, strip_endpoints=sorted(crossing), fully_frozen=True),
                mixed_direction_fixture=dict(sources=4, strip_deficit=8,
                                             source_charge=4, compensated_charge=-4,
                                             objective=mixed_checked['objective'],
                                             area=mixed_checked['area']),
                family=records,
                scope='Finite controls of the independent general written strip theorem. '
                      'All tile-aligned translations causing overlap are checked for the '
                      'listed shapes/orientations, without treating their finite set as a proof. '
                      'No universal endpoint-free-strip or grid equality claim.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('family', 'endpoint_free_hypothesis_not_automatic')}))


if __name__ == '__main__':
    main()
