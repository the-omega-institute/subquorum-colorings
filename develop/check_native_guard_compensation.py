"""Check native-guard donor lifting and terminal virtual-guard obstructions."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_even_bridge_support_completion import bridge_cuts, completed, endpoints_of, tiles_of
from check_exchange_terminal_nonunique import graft
from check_matching_block_tile_ledger import small_models
from check_promotion_cores import frozen_certificate
from check_rematching_receiver_flux import canonical
from check_residual_corridors import direct_check, transformed
from search_corner_coverage import corner_patterns, witnesses


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def charge(current):
    endpoints = endpoints_of(current)
    return len(endpoints)//2+sum(len(current[2] & vertices_of({tile}))-2 for tile in tiles_of(endpoints))


def pieces(current):
    result = []
    for component in endpoint_components(current):
        cuts = {tuple(sorted((first, second)))
                for first, second, left, _ in bridge_cuts(component) if len(left) % 2 == 0}
        remaining = set(component)
        while remaining:
            pending = [min(remaining)]
            reached = set(pending)
            while pending:
                point = pending.pop()
                for other in set(neighbors(point)) & component:
                    if other in reached or tuple(sorted((point, other))) in cuts:
                        continue
                    reached.add(other)
                    pending.append(other)
            remaining -= reached
            supports = {other for point in reached for other in set(neighbors(point)) & (component-reached)}
            result.append(completed(current, reached, supports))
    return result


def inspect_native(current, totals):
    objective = direct_check(*current)
    assert min(occupied_degrees(current).values()) >= 3
    endpoints = endpoints_of(current)
    completed_pieces = pieces(current)
    assert sum(charge(piece) for piece in completed_pieces) == charge(current)
    owners = {}
    criterion = True
    positive = 0
    for index, piece in enumerate(completed_pieces):
        local_endpoints = endpoints_of(piece)
        native_tiles = set()
        for witness in witnesses(*current[:2], piece[2], local_endpoints):
            required, support, excluded = list(corner_patterns(*witness['square']))[witness['orientation']]
            assert set(required) <= local_endpoints and not set(excluded) & local_endpoints
            if support not in current[2]:
                totals['virtual_witnesses'] += 1
                continue
            tile = tuple(value//2 for value in witness['square'])
            cells = vertices_of({tile})
            assert not cells & endpoints
            assert len(cells & current[2]) <= 1
            assert tile not in owners or owners[tile] == index
            owners[tile] = index
            native_tiles.add(tile)
            totals['native_witnesses'] += 1
        if charge(piece) > 0:
            positive += 1
            criterion &= charge(piece) <= 1 and bool(native_tiles)
    empty = set(itertools.product(range(current[0]//2), range(current[1]//2)))-tiles_of(endpoints)
    deficit = sum(2-len(current[2] & vertices_of({tile})) for tile in empty)
    assert deficit >= 0
    margin = current[0]*current[1]//2-objective
    assert margin == deficit-sum(charge(piece) for piece in completed_pieces)
    if criterion:
        assert margin >= 0
        totals['compensation_criterion_models'] += 1
        if positive:
            totals['nonvacuous_compensation_models'] += 1
    totals['native_input_models'] += 1
    totals['completed_pieces_checked'] += len(completed_pieces)
    return dict(criterion=criterion, positive_pieces=positive, original_deficit=deficit,
                original_margin=margin, completed_charges=[charge(piece) for piece in completed_pieces])


def virtual_guard_pair(outer_width, outer_height, inner_width, inner_height):
    assert inner_width >= 6 and inner_height >= 4 and outer_width >= inner_width+6 and outer_height >= 4
    assert all(parameter % 2 == 0 for parameter in (outer_width, outer_height, inner_width, inner_height))
    outer = elbow(outer_width, outer_height)
    inner = elbow(inner_width, inner_height)
    move = lambda point: (point[0]+3, point[1])
    outer_endpoints = endpoints_of(outer)
    inner_matching = [tuple(move(point) for point in edge) for edge in inner[3]]
    inner_endpoints = {point for edge in inner_matching for point in edge}
    inner_selected = {move(point) for point in inner[2]}-{(7, 4)} | {(6, 5)}
    selected = (outer[2] | inner_selected)-(outer_endpoints | inner_endpoints)
    current = max(outer_height+8, inner_height+10), outer_width+12, selected, outer[3]+inner_matching
    return current, outer_endpoints, inner_endpoints


def force_matching(current, totals):
    remaining = endpoints_of(current)
    forced = []
    while remaining:
        leaves = [point for point in remaining if len(set(neighbors(point)) & remaining) == 1]
        assert leaves
        leaf = min(leaves)
        mate = next(iter(set(neighbors(leaf)) & remaining))
        forced.append((leaf, mate))
        remaining -= {leaf, mate}
    assert canonical(forced) == canonical(current[3])
    assert frozen_certificate(current)[0] == endpoints_of(current)
    totals['independent_forced_matching_edges'] += len(forced)
    totals['unique_frozen_pairs'] += 1


def check_forcing_template(width, height, pair, offset, totals):
    order = [((2, 0), (1, 0))]
    order += [((column % 2, column), (column % 2, column+1)) for column in range(width-1)]
    order += [((1, width-1), (2, width-1))]
    order += [((row, width-2 if row % 2 == 0 else width-1),
               (row+1, width-2 if row % 2 == 0 else width-1)) for row in range(2, height)]
    move = lambda point: (point[0]+offset[0], point[1]+offset[1])
    order = [(move(leaf), move(mate)) for leaf, mate in order]
    remaining = endpoints_of(pair)
    for leaf, mate in order:
        assert set(neighbors(leaf)) & remaining == {mate}
        remaining -= {leaf, mate}
    assert not remaining and canonical(order) == canonical(pair[3])
    totals['explicit_forcing_template_edges'] += len(order)


def inspect_obstruction(parameters, totals):
    outer_width, outer_height, inner_width, inner_height = parameters
    current, outer_endpoints, inner_endpoints = virtual_guard_pair(*parameters)
    assert direct_check(*current) == outer_width+inner_width+2*outer_height+2*inner_height+4
    assert not outer_endpoints & inner_endpoints
    contacts = {(point, other) for point in outer_endpoints for other in set(neighbors(point)) & inner_endpoints}
    assert contacts == {((6, 5), (7, 5))}
    cuts = [(first, second) for first, second, side, _ in bridge_cuts(outer_endpoints | inner_endpoints)
            if len(side) % 2 == 0]
    assert cuts == [((6, 5), (7, 5))]
    outer = completed(current, outer_endpoints, {(7, 5)})
    inner = completed(current, inner_endpoints, {(6, 5)})
    check_forcing_template(outer_width, outer_height, outer, (4, 5), totals)
    check_forcing_template(inner_width, inner_height, inner, (7, 5), totals)
    assert charge(outer) == 1 and charge(inner) == 1-inner_width
    assert charge(current) == 2-inner_width
    assert len(tiles_of(inner_endpoints)) == inner_width+inner_height
    assert len(inner[2] & vertices_of(tiles_of(inner_endpoints))) == inner_height+2
    for pair in (current, outer, inner):
        force_matching(pair, totals)
    donor = vertices_of({(3, 3)})
    assert not donor & outer_endpoints and not donor & outer[2]
    assert donor & inner_endpoints == {(7, 6), (7, 7)}
    record = inspect_native(current, totals)
    assert record['original_margin'] == record['original_deficit']+inner_width-2
    assert record['original_margin'] >= 4
    assert not record['criterion']
    totals['obstruction_parameters'] += 1
    return current, record


def separated_elbows():
    selected, matching = set(), []
    for width, height, vertical, horizontal in ((6, 4, 0, 0), (8, 6, 0, 30), (10, 4, 24, 12)):
        base = elbow(width, height)
        move = lambda point: (point[0]+vertical, point[1]+horizontal)
        selected |= {move(point) for point in base[2]}
        matching += [tuple(move(point) for point in edge) for edge in base[3]]
    return 40, 54, selected, matching


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    totals = Counter()
    for current in small_models(3, 4):
        inspect_native(current, totals)
    assert totals['native_input_models'] == 1086
    controls = [elbow(6, 4), elbow(12, 8), graft(6, 4), graft(10, 8), separated_elbows()]
    for current in controls:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            result = inspect_native((*shape, selected, matching), totals)
            assert result['criterion'] and result['positive_pieces'] >= 1
    assert inspect_native(separated_elbows(), totals)['positive_pieces'] == 3
    example = None
    for inner_width in range(6, 17, 2):
        for inner_height in range(4, 13, 2):
            for gap, outer_height in itertools.product((6, 10), (4, 8, 12)):
                current, record = inspect_obstruction((inner_width+gap, outer_height, inner_width, inner_height), totals)
                if (inner_width, inner_height, gap, outer_height) == (6, 4, 6, 8):
                    example = dict(parameters=[12, 8, 6, 4], selected=sorted(current[2]),
                                   matching=current[3], shape=list(current[:2]), record=record)
                if inner_width in (6, 16) and inner_height in (4, 12) and gap == 6 and outer_height == 8:
                    for symmetry in itertools.product((False, True), repeat=3):
                        shape, selected, matching = transformed(*current, *symmetry)
                        image = *shape, selected, matching
                        direct_check(*image)
                        force_matching(image, totals)
                        image_record = inspect_native(image, totals)
                        assert image_record['completed_charges'] == record['completed_charges'] or \
                            sorted(image_record['completed_charges']) == sorted(record['completed_charges'])
                        totals['obstruction_symmetries'] += 1
    assert totals['obstruction_parameters'] == 180 and totals['obstruction_symmetries'] == 32
    report = dict(status='PASS', controls=dict(totals), reference_obstruction=example,
                  scope='Finite coordinate validation of the general written native-guard compensation '
                        'and all-parameter exchange-terminal virtual-guard donor-transport obstruction. '
                        'Leaf forcing establishes uniqueness of each tested matching; enumeration '
                        'does not replace the parameter-independent proofs or solve the global target.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'reference_obstruction'}, indent=2))


if __name__ == '__main__':
    main()
