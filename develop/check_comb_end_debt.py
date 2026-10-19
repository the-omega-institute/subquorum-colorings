"""Exact physical mouth debt controls with complete perpendicular comb ends."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_long_bent_terminal_strips import terminal_strip
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_saturated_bent_bands import long_bent
from check_transverse_comb_mouths import crossing_family, optimize_strip


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


KINDS = {'through': (1, 2), 'end_upper': (3, 0), 'start_lower': (-1, 4),
         'start_upper': (0, 3), 'end_lower': (2, 1), 'within': (0, 1)}


def contact_family(width, depth, contacts):
    baseline, _ = long_bent(width, depth, saturate=False)
    selected, matching, rows = set(baseline[2]), list(baseline[3]), baseline[0]
    for center, phase, kind in contacts:
        upper, lower = KINDS[kind]
        current, _ = crossing_family(width, depth, [center], [phase], upper, lower)
        selected.update(current[2])
        matching.extend(current[3][len(baseline[3]):])
        rows = max(rows, current[0])
    current = rows, baseline[1], selected, matching
    direct_check(*current)
    return current, terminal_strip(width, depth)


def mouth_record(current, strip):
    endpoints = endpoint_data(current)[0]
    rows = sorted({row for row, column in strip})
    columns = sorted({column for row, column in strip})
    assert len(rows) == 2
    assert all((row, column) not in endpoints | current[2]
               for row in rows for column in (columns[0], columns[-1]))
    tiles = {(row//2, column//2) for row, column in strip}
    paired = {(row//2, column//2) for row, column in strip & endpoints}
    sparse, saturated, full = set(), set(), set()
    for tile in paired:
        cells = vertices_of({tile})
        counts = len(cells & current[2]), len(cells & endpoints)
        assert counts in ((1, 2), (1, 1), (2, 1)), counts
        if counts == (1, 2):
            full.add(tile)
        elif counts == (1, 1):
            sparse.add(tile)
        else:
            saturated.add(tile)
    shifted_partial = 0
    for column in columns[1:-1:2]:
        square = {(row, current_column) for row in rows
                  for current_column in (column, column+1)}
        selected_count, endpoint_count = len(square & current[2]), len(square & endpoints)
        assert endpoint_count in (0, 1, 2)
        if endpoint_count == 2:
            assert len({current_column for row, current_column in square & endpoints}) == 1
        shifted_partial += endpoint_count == 1
        assert 2*selected_count+endpoint_count <= 4+int(endpoint_count == 1)
    assert shifted_partial == len(sparse)+len(saturated)
    selected_total = len(strip & current[2])
    endpoint_total = len(strip & endpoints)
    assert endpoint_total == 2*len(full)+len(sparse)+len(saturated)
    slack_twice = 4*(len(tiles)-1)+len(sparse)+len(saturated)-2*selected_total-endpoint_total
    assert slack_twice >= 0 and slack_twice % 2 == 0
    deficit = sum(2-len(vertices_of({tile}) & current[2]) for tile in tiles-paired)
    assert deficit == 2-len(sparse)+slack_twice//2
    assert deficit >= 2-len(sparse)
    return dict(sparse_ends=len(sparse), saturated_ends=len(saturated), full_columns=len(full),
                shifted_slack=slack_twice//2, no_endpoint_deficit=deficit,
                sparse_tiles=sorted(sparse))


def sparse_owners(current, claimed):
    owners = set()
    for index, component in enumerate(endpoint_components(current)):
        if not (len({row for row, column in component}) == 1 or
                len({column for row, column in component}) == 1):
            continue
        tiles = {(row//2, column//2) for row, column in component}
        sparse = {tile for tile in tiles if len(vertices_of({tile}) & component) == 1 and
                  len(vertices_of({tile}) & current[2]) == 1}
        assert len(sparse) <= 1
        if sparse & claimed:
            owners.add(index)
    assert len(owners) == len(claimed)
    return len(owners)


def controls():
    records, images = [], 0
    names = tuple(KINDS)
    for count in range(1, 7):
        kinds = list(itertools.product(names, repeat=count)) if count <= 2 else [
            tuple(kind for index in range(count)) for kind in names]+[
            tuple(names[(index+offset) % len(names)] for index in range(count))
            for offset in range(len(names))]
        phases = list(itertools.product((-1, 1), repeat=count)) if count <= 2 else [
            tuple(1 for index in range(count)), tuple(-1 for index in range(count)),
            tuple((-1)**index for index in range(count)), tuple(-(-1)**index for index in range(count))]
        for depth, types, sides in itertools.product((3, 6), kinds, phases):
            contacts = [(5+4*index, side, kind) for index, (side, kind) in enumerate(zip(sides, types))]
            current, strip = contact_family(4*count+10, depth, contacts)
            sharp = optimize_strip(current, strip)
            checked = verify_terminal(sharp)
            assert frozen_certificate(sharp)[0] == endpoint_data(sharp)[0]
            assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*count+[2]
            record = mouth_record(sharp, strip)
            assert sparse_owners(sharp, set(map(tuple, record['sparse_tiles']))) == record['sparse_ends']
            records.append(dict(contacts=contacts, width=4*count+10, depth=depth, **record))
            if count in (1, 3, 6) and depth == 3 and types == kinds[0] and sides == phases[0]:
                for flip_vertical, flip_horizontal in itertools.product((False, True), repeat=2):
                    shape, selected, matching = transformed(*sharp, False, flip_vertical, flip_horizontal)
                    _, moved_strip, _ = transformed(*sharp[:2], strip, [], False, flip_vertical, flip_horizontal)
                    assert mouth_record((*shape, selected, matching), moved_strip)['no_endpoint_deficit'] == record['no_endpoint_deficit']
                    images += 1
    first, _ = long_bent(14, 2, saturate=False)
    _, other_selected, other_matching = transformed(*first, False, True, True)
    move = lambda vertex: (vertex[0]+12, vertex[1]-2)
    selected = first[2] | {move(point) for point in other_selected}
    matching = first[3]+[tuple(move(point) for point in edge) for edge in other_matching]
    selected |= {(8, 8), (15, 8)} | {(row, 7 if row % 2 else 9) for row in range(9, 15)}
    matching += [((row, 8), (row+1, 8)) for row in range(9, 15, 2)]
    shared = 32, 22, selected, matching
    first_strip = terminal_strip(14, 2)
    _, other_strip, _ = transformed(*first[:2], first_strip, [], False, True, True)
    second_strip = {move(point) for point in other_strip}
    for strip in (first_strip, second_strip):
        shared = optimize_strip(shared, strip)
    checked = verify_terminal(shared)
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0, 2, 2]
    assert frozen_certificate(shared)[0] == endpoint_data(shared)[0]
    mouths = [mouth_record(shared, strip) for strip in (first_strip, second_strip)]
    assert [mouth['sparse_ends'] for mouth in mouths] == [1, 0]
    assert [mouth['shifted_slack'] for mouth in mouths] == [0, 1]
    assert [mouth['no_endpoint_deficit'] for mouth in mouths] == [1, 3]
    claimed = {tuple(tile) for mouth in mouths for tile in mouth['sparse_tiles']}
    assert sparse_owners(shared, claimed) == 1
    shared_record = dict(shape=shared[:2], selected=sorted(shared[2]), matching=shared[3],
                         sources=2, complete_bridge_combs=1, total_sparse_debt=1,
                         mouth_payments=[mouth['no_endpoint_deficit'] for mouth in mouths],
                         compensated_charge=2-sum(mouth['no_endpoint_deficit'] for mouth in mouths),
                         objective=checked['objective'], mouths=mouths)
    return dict(status='ALL_CHECKS_PASSED', optimized_cases=len(records), symmetry_images=images,
                contact_kinds=names, family=records, shared_end_owner_fixture=shared_record,
                scope='Finite controls of a separate general debt/slack proof. All extra mouth selections '
                      'are optimized for the fixed contacts. Sparse ends have unique complete-comb owners; '
                      'no automatic exterior debt payment or universal grid theorem is inferred.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('family', 'shared_end_owner_fixture')}))


if __name__ == '__main__':
    main()
