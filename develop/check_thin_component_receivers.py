"""Check arbitrary-tail capped receivers and the thin-component normalization bound."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate, normalize
from check_residual_corridors import direct_check, transformed
from check_single_square_parity import single_square
from verify_grid_five_sixths import bits, pairs


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def optional_sites(width):
    north = range(1, width-2) if width % 2 else range(1, width-1)
    south = range(2, width-1) if width % 2 else range(2, width-2)
    return {(-1, column) for column in north} | {(2, column) for column in south}


def optional_patterns(width, exhaustive):
    sites = sorted(optional_sites(width))
    if exhaustive:
        for mask in range(1 << len(sites)):
            selected = {vertex for index, vertex in enumerate(sites) if mask >> index & 1}
            if all(not (set(neighbors(vertex)) & selected) for vertex in selected):
                yield selected
        return
    yield set()
    for parity in (0, 1):
        yield {vertex for vertex in sites if vertex[1] % 2 == parity}
    yield {vertex for vertex in sites if vertex[1] % 2 == (0 if vertex[0] == -1 else 1)}


def capped(width, left_tail, right_tail, vertical, horizontal, optional):
    assert width >= 3 and left_tail % 2 == right_tail % 2 == 1
    right_row = width % 2
    outside = lambda row: -1 if row == 0 else 2
    selected = {(2, 0), (outside(1-right_row), width-1), (0, -left_tail-1),
                (right_row, width+right_tail)} | optional
    selected |= {(-1 if index % 2 else 1, -index) for index in range(1, left_tail+1)}
    selected |= {(outside(right_row) if index % 2 else 1-right_row, width+index-1)
                 for index in range(1, right_tail+1)}
    matching = [((0, -1), (0, 0))]
    matching += [((index % 2, index-1), (index % 2, index)) for index in range(1, width+1)]
    matching += [((0, -index), (0, -index-1)) for index in range(2, left_tail, 2)]
    matching += [((right_row, width+index-1), (right_row, width+index))
                 for index in range(2, right_tail, 2)]
    column_shift = 2*((left_tail+3)//2)+horizontal
    move = lambda vertex: (vertex[0]+2+vertical, vertex[1]+column_shift)
    selected = {move(vertex) for vertex in selected}
    matching = [tuple(move(vertex) for vertex in edge) for edge in matching]
    columns = 2*((max(vertex[1] for vertex in selected)+3)//2)
    return 8, columns, selected, matching


def expected_counts(width, left_tail, right_tail, vertical, horizontal, optional):
    extra = (left_tail+right_tail-2)//2
    endpoints = 2*width+left_tail+right_tail
    if vertical == 0:
        tiles = width//2+2 if horizontal == 0 else (width+1)//2+1
        selected = 2*tiles-width-2
        charge = -1
    else:
        tiles = width+2
        selected = 5 if width % 2 else 6-2*horizontal
        selected += len(optional)
        charge = selected-width-3
    return tiles+extra, selected+extra, endpoints, 2*charge


def check_family_case(width, left_tail, right_tail, vertical, horizontal, optional):
    assert len(optional) <= width-3
    current = capped(width, left_tail, right_tail, vertical, horizontal, optional)
    checked = verify_terminal(current)
    assert len(checked['receivers']) == 1
    receiver = checked['receivers'][0]
    expected = expected_counts(width, left_tail, right_tail, vertical, horizontal, optional)
    actual = tuple(receiver[key] for key in ('tiles', 'selected', 'endpoints', 'charge_twice'))
    assert actual == expected, (width, left_tail, right_tail, vertical, horizontal, optional, actual, expected)
    assert receiver['charge_twice'] <= 0
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    cells = vertices_of({(row//2, column//2) for row, column in endpoints})
    assert all(set(neighbors(vertex)) & endpoints for vertex in current[2] & cells)
    column_shift = 2*((left_tail+3)//2)+horizontal
    optional_candidates = {(row+2+vertical, column+column_shift) for row, column in optional_sites(width)}
    for vertex in cells-current[2]-endpoints-optional_candidates:
        assert len(set(neighbors(vertex)) & endpoints) >= 2 or any(
            support in current[2] and set(neighbors(support)) & endpoints
            for support in neighbors(vertex))
    return current, receiver


def family_controls():
    cases = images = extensions = 0
    rows = []
    tails = [(1, 1), (1, 3), (3, 1), (3, 5), (7, 3), (17, 21)]
    for width in range(3, 25):
        patterns = list(optional_patterns(width, exhaustive=width <= 8))
        for optional in patterns:
            for vertical, horizontal in itertools.product((0, 1), repeat=2):
                for left_tail, right_tail in tails:
                    current, receiver = check_family_case(
                        width, left_tail, right_tail, vertical, horizontal, optional)
                    if (left_tail, right_tail) == (1, 1):
                        for extended_left, extended_right in ((3, 1), (1, 3)):
                            _, following = check_family_case(
                                width, extended_left, extended_right, vertical, horizontal, optional)
                            assert [following[key]-receiver[key] for key in
                                    ('tiles', 'selected', 'endpoints', 'charge_twice')] == [1, 1, 2, 0]
                            extensions += 1
                    if width in (3, 4, 9, 24) and (left_tail, right_tail) == (3, 5):
                        for symmetry in itertools.product((False, True), repeat=3):
                            shape, chosen, matching = transformed(*current, *symmetry)
                            image = (*shape, chosen, matching)
                            assert verify_terminal(image)['receivers'][0]['charge_twice'] == receiver['charge_twice']
                            assert frozen_certificate(image)[0] == endpoint_data(image)[0]
                            images += 1
                    cases += 1
        rows.append(dict(width=width, optional_patterns=len(patterns), tail_choices=len(tails)))
        print(json.dumps(rows[-1]), flush=True)
    return rows, cases, images, extensions


def is_thin(component):
    return max(row for row, _ in component)-min(row for row, _ in component) <= 1 or max(
        column for _, column in component)-min(column for _, column in component) <= 1


def exhaustive_controls():
    records = []
    for rows, columns in ((2, 2), (2, 4), (2, 6), (3, 4)):
        examined = qualifying = moves = residual_caps = 0
        for selected_mask, _, matching in pairs(rows, columns):
            current = (rows+rows % 2, columns,
                       {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns)) for first, second in matching])
            examined += 1
            if not all(is_thin(component) for component in endpoint_components(current)):
                continue
            ending, operations = normalize(current)
            assert all(is_thin(component) for component in endpoint_components(ending))
            assert frozen_certificate(ending)[0] == endpoint_data(ending)[0]
            checked = verify_terminal(ending)
            assert all(receiver['charge_twice'] <= 0 for receiver in checked['receivers'])
            assert direct_check(*current) == checked['objective'] <= checked['area']//2
            assert checked['area']-2*checked['objective'] == -sum(
                receiver['charge_twice'] for receiver in checked['receivers'])+2*checked['empty_deficit']
            qualifying += 1
            moves += len(operations)
            residual_caps += sum(not receiver['straight'] for receiver in checked['receivers'])
        records.append(dict(source_shape=[rows, columns], examined=examined, qualifying=qualifying,
                            normalization_bundles=moves, residual_capped_components=residual_caps))
        print(json.dumps(records[-1]), flush=True)
    return records


def neutral_control():
    optional = {(-1, 1)}
    current, receiver = check_family_case(4, 1, 1, 1, 0, optional)
    assert receiver['charge_twice'] == 0
    endpoints = endpoint_data(current)[0]
    assert len(endpoint_data(current)[2]) == 3
    return dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                endpoint_squares=3, frozen_endpoints=len(endpoints), receiver=receiver,
                refutes='Every frozen thin square-bearing component has receiver charge at most minus one.',
                global_coefficient_one_refuted=False)


def combined_control():
    pieces = [capped(6, 3, 5, 1, 0, {(-1, 1), (-1, 3), (2, 2)}),
              capped(5, 3, 1, 0, 1, set())]
    source = capped(7, 5, 3, 1, 1, {(-1, 1), (-1, 3), (2, 2), (2, 4)})
    shape, selected, matching = transformed(*source, True, False, False)
    pieces.append((*shape, selected, matching))
    branch, _ = single_square((1, 2, 1, 2), [(0, 1)])
    pieces.append(branch)
    pieces.append((4, 4, set(), [((1, 1), (2, 1)), ((1, 2), (2, 2))]))
    selected = set()
    matching = []
    offset = 0
    columns = max(piece[1] for piece in pieces)+4
    for rows, _, chosen, edges in pieces:
        move = lambda vertex: (vertex[0]+offset, vertex[1]+2)
        selected.update(move(vertex) for vertex in chosen)
        matching.extend(tuple(move(vertex) for vertex in edge) for edge in edges)
        offset += rows+4
    current = offset, columns, selected, matching
    initial_components = endpoint_components(current)
    squares = endpoint_data(current)[2]
    assert len(initial_components) == len(pieces)
    assert any(not is_thin(component) for component in initial_components)
    assert all(is_thin(component) or sum(origin in component for origin in squares) <= 1
               for component in initial_components)
    ending, operations = normalize(current)
    assert operations
    checked = verify_terminal(ending)
    assert all(receiver['charge_twice'] <= 0 for receiver in checked['receivers'])
    assert any(receiver['charge_twice'] == 0 and not receiver['straight'] for receiver in checked['receivers'])
    assert direct_check(*current) == checked['objective'] <= checked['area']//2
    assert checked['area']-2*checked['objective'] == -sum(
        receiver['charge_twice'] for receiver in checked['receivers'])+2*checked['empty_deficit']
    return dict(initial_shape=current[:2], selected=sorted(selected), matching=matching,
                initial_components=len(initial_components), normalization_bundles=len(operations), **checked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    family, cases, images, extensions = family_controls()
    report = dict(status='ALL_CHECKS_PASSED', family_cases=cases, symmetry_images=images,
                  tail_extension_checks=extensions, family=family,
                  exhaustive=exhaustive_controls(), neutral_multisquare=neutral_control(),
                  mixed_components=combined_control(),
                  scope='Controls for the written arbitrary thin-component classification, all-phase capped receiver formulas, frozen converse and normalization bound. Enumeration does not replace general proofs; no universal grid bound claimed.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('family', 'neutral_multisquare', 'mixed_components')}))


if __name__ == '__main__':
    main()
