"""Independent finite controls for straight chambers and their matching exits."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_bent_cap_compensation import bent_cap
from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import capacity_cross, endpoint_data, straight_comb
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed
from check_two_row_terminal_shapes import matchings


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def corners(face):
    return {(face[0]+row, face[1]+column)
            for row, column in itertools.product((0, 1), repeat=2)}


def components(vertices):
    remaining = set(vertices)
    result = []
    while remaining:
        pending = [min(remaining)]
        found = set(pending)
        remaining -= found
        while pending:
            following = set(neighbors(pending.pop())) & remaining
            remaining -= following
            found |= following
            pending.extend(following)
        result.append(found)
    return result


def check_strips(faces):
    strips = components(faces)
    used = set()
    for strip in strips:
        rows = {point[0] for point in strip}
        columns = {point[1] for point in strip}
        assert len(rows) == 1 or len(columns) == 1
        assert len(strip) == len(rows)*len(columns)
        cells = set().union(*(corners(face) for face in strip))
        assert not used & cells
        used |= cells
    return strips


def geometric_controls():
    board = list(itertools.product(range(4), repeat=2))
    valid = junctions = residual_strips = 0
    for mask in range(1 << len(board)):
        endpoints = {point for index, point in enumerate(board) if mask >> index & 1}
        faces = {point for point in endpoints if corners(point) <= endpoints}
        degree_four = {point for point in endpoints if set(neighbors(point)) <= endpoints}
        marked = {face for face in faces if corners(face) & degree_four}
        assert len(marked) <= 4*len(degree_four)
        strips = check_strips(faces-marked)
        residual_strips += len(strips)
        for original in components(faces):
            surviving = components(original-marked)
            assert len(surviving) <= 1+3*len(original & marked)
        if degree_four:
            junctions += 1
        else:
            valid += 1
            check_strips(faces)
    return dict(masks=1 << len(board), masks_without_degree_four=valid,
                masks_with_degree_four=junctions, surviving_strip_instances=residual_strips)


def ladder_count(width, exits):
    blocked = {column: sum(1 << row for row in (0, 1) if (row, column) in exits)
               for column in range(width)}
    states = {0: 1}
    for column in range(width):
        following = Counter()
        for incoming, weight in states.items():
            if incoming & blocked[column]:
                continue

            def fill(occupied, outgoing):
                if occupied == 3:
                    following[outgoing] += weight
                    return
                row = next(index for index in (0, 1) if not occupied >> index & 1)
                if occupied == 0:
                    fill(3, outgoing)
                if column+1 < width:
                    fill(occupied | (1 << row), outgoing | (1 << row))

            fill(incoming | blocked[column], 0)
        states = following
    return states.get(0, 0)


def matching_controls():
    fibonacci = [0, 1]
    for _ in range(130):
        fibonacci.append(sum(fibonacci[-2:]))
    cases = brute = unique = 0
    for width in range(2, 129):
        vertices = set(itertools.product((0, 1), range(width)))
        outer = sorted(set(itertools.product((0, 1), (0, width-1))))
        for bits in itertools.product((False, True), repeat=4):
            exits = {point for point, chosen in zip(outer, bits) if chosen}
            actual = ladder_count(width, exits)
            if len(exits) % 2:
                expected = 0
            elif not exits:
                expected = fibonacci[width+1]
            elif len(exits) == 4:
                expected = fibonacci[width-1]
            elif len({point[1] for point in exits}) == 1:
                expected = fibonacci[width]
            else:
                expected = int(len({sum(point) % 2 for point in exits}) == 2)
            assert actual == expected, (width, exits, actual, expected)
            if width <= 8:
                assert actual == sum(1 for _ in matchings(vertices-exits))
                brute += 1
            if actual == 1:
                unique += 1
                if width >= 4:
                    assert len(exits) == 2 and len({point[1] for point in exits}) == 2
            cases += 1
    return dict(widths=[2, 128], exit_subsets=cases, independently_enumerated=brute,
                unique_internal_matching_cases=unique)


def inspect(current):
    endpoints, adjacency, faces = endpoint_data(current)
    assert set(occupied_degrees(current).values()) == {3}
    assert frozen_certificate(current)[0] == endpoints
    assert all(len(adjacent) <= 3 for adjacent in adjacency.values())
    strips = check_strips(faces)
    used = set().union(*(set().union(*(corners(face) for face in strip))
                         for strip in strips)) if strips else set()
    for path in components(endpoints-used):
        assert len({point[0] for point in path}) == 1 or len({point[1] for point in path}) == 1
        contacts = [(point, other) for point in path for other in adjacency[point] & used]
        assert len(contacts) <= 2
        for point in path:
            adjacent = adjacency[point]
            assert len(adjacent) <= 2
            if len(adjacent) == 2:
                assert len({other[0] for other in adjacent}) == 1 or len({other[1] for other in adjacent}) == 1
    records = []
    for strip in strips:
        cells = set().union(*(corners(face) for face in strip))
        rows = sorted({point[0] for point in cells})
        columns = sorted({point[1] for point in cells})
        outer = set(itertools.product((rows[0], rows[-1]), (columns[0], columns[-1])))
        for point in cells-outer:
            assert adjacency[point] <= cells
        exiting = {point for edge in current[3] for point, mate in (edge, edge[::-1])
                   if point in cells and mate not in cells}
        assert exiting <= outer and len(exiting) in (2, 4)
        horizontal = len(rows) == 2
        width = len(columns) if horizontal else len(rows)
        normalized = {(point[0]-rows[0], point[1]-columns[0]) if horizontal else
                      (point[1]-columns[0], point[0]-rows[0]) for point in exiting}
        assert ladder_count(width, normalized) == 1
        assert len({point[0] for point in cells}) == 2 or len({point[1] for point in cells}) == 2
        records.append(dict(width=width, exits=len(exiting)))
    checked = verify_terminal(current)
    return dict(endpoint_components=len(endpoint_components(current)), chambers=records,
                charge_twice=[record['charge_twice'] for record in checked['receivers']])


def fixture_controls():
    fixtures = []
    for size in range(1, 33):
        fixtures.extend([straight_comb(size), bent_cap(2*size+2), capacity_cross(size)[0]])
    reports = []
    for current in fixtures:
        reports.append(inspect(current))
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            inspect((*shape, selected, matching))
    return dict(base_fixtures=len(fixtures), symmetry_images=8*len(fixtures), examples=reports[:9])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='PASS', geometric_masks=geometric_controls(),
                  matching_exits=matching_controls(), physical_fixtures=fixture_controls(),
                  scope='Finite controls for the all-size written geometry and exit classification; '
                        'not a proof of the whole-receiver charge ceiling or grid inequality.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'physical_fixtures'}))
    print(json.dumps({key: value for key, value in report['physical_fixtures'].items() if key != 'examples'}))


if __name__ == '__main__':
    main()
