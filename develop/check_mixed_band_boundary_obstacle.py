#!/usr/bin/env python3
"""Check the unbounded mixed-band boundary obstruction and closure identity."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_cross_component_compensation import escaping_band, witness_record
from check_neutral_attachment_normalization import eligible
from check_residual_corridors import corridor, direct_check, graph_record, transformed
from verify_grid_short_path_compensation import check_geometry, pairs


def general_region_ledger(current, region):
    rows, columns, selected, matching = current
    residual_graph, _ = graph_record(*current)
    tile_of = lambda vertex: vertex[0]//2*(columns//2)+vertex[1]//2
    tiles = {tile_of(vertex) for vertex in region}
    assert len(region) == 4*len(tiles)
    occupied = selected | {vertex for edge in matching for vertex in edge}
    outgoing = incoming = 0
    for first, second in matching:
        if (first in region) == (second in region):
            continue
        inside, outside = (first, second) if first in region else (second, first)
        outgoing += residual_graph['t'][tile_of(inside)] < 2 and residual_graph['t'][tile_of(outside)] == 2
        incoming += residual_graph['t'][tile_of(inside)] == 2 and residual_graph['t'][tile_of(outside)] < 2
    selected_count = len(region & selected)
    blank_count = len(region-occupied)
    charge_twice = sum(residual_graph['deg'][tile]-2*residual_graph['r'][tile] for tile in tiles)
    assert charge_twice == selected_count-blank_count+outgoing-incoming
    return dict(tiles=sorted(tiles), selected=selected_count, blanks=blank_count,
                outgoing_saturated_attachments=outgoing, incoming_saturated_attachments=incoming,
                charge_twice=charge_twice)


def configuration(branches):
    if branches < 1:
        raise ValueError('Require at least one module.')
    width = 3*branches+5
    columns = 2*width+4
    source = ['TP/BP']+['PP/PP']*width+['PT/PB']
    parent = ['TP/BT', 'PP/BP', 'PP/PP']+['PP/BT']*(3*branches)+[
        'PP/BP', 'PP/PP', 'PP/PB', 'PT/TB']
    child = ['TB/BT', 'TP/BT', 'PP/BT']+[
        state for _ in range(branches) for state in ('TB/BT', 'TB/PP', 'TB/PT')]+[
        'TP/BT', 'PP/BB', 'PT/TB', 'BT/TB']
    bottom = ['TB/BT']*(width+2)
    for module in range(branches):
        bottom[4+3*module] = 'PB/BT'
    bottom[-3:] = ['BT/TB']*3
    tile_rows = [source, parent, child, bottom]
    assert all(len(row) == width+2 for row in tile_rows)
    selected = set()
    expected_endpoints = set()
    for tile_row, states in enumerate(tile_rows):
        for tile_column, state in enumerate(states):
            for corner, letter in enumerate(state.replace('/', '')):
                vertex = 2*tile_row+corner//2, 2*tile_column+corner % 2
                if letter == 'T':
                    selected.add(vertex)
                if letter == 'P':
                    expected_endpoints.add(vertex)
    _, _, _, matching = corridor(width)
    for tile_column in range(1, width+1):
        matching.append(((2, 2*tile_column), (2, 2*tile_column+1)))
    for tile_column in (1, width-2):
        matching.append(((3, 2*tile_column+1), (4, 2*tile_column+1)))
    matching.append(((3, 2*width), (4, 2*width)))
    matching.extend((((3, 4), (4, 4)), ((3, 5), (4, 5)),
                     ((3, 2*(width-1)), (3, 2*(width-1)+1)),
                     ((4, 2*(width-1)), (4, 2*(width-1)+1))))
    for module in range(branches):
        leaf_column = 4+3*module
        matching.extend((((5, 2*leaf_column), (6, 2*leaf_column)),
                         ((5, 2*leaf_column+1), (5, 2*(leaf_column+1)))))
    assert {vertex for edge in matching for vertex in edge} == expected_endpoints
    return 8, columns, selected, matching


def regions(current):
    columns = current[1]
    return dict(source={(row, column) for row in (0, 1) for column in range(columns)},
                parent={(row, column) for row in (2, 3) for column in range(2, columns-2)},
                child={(row, column) for row in (4, 5) for column in range(2, columns-2)},
                bottom={(row, column) for row in (6, 7) for column in range(columns)})


def capacity_two(current):
    removed = {frozenset(((row, 6), (row, 7))) for row in (1, 2)}
    matching = [edge for edge in current[3] if frozenset(edge) not in removed]
    assert len(matching) == len(current[3])-2
    matching.extend((((1, 6), (2, 6)), ((1, 7), (2, 7))))
    changed = (*current[:3], matching)
    before, _ = graph_record(*current)
    after, _ = graph_record(*changed)
    assert [degree-2*capacity for degree, capacity in zip(before['deg'], before['r'])] == [
        degree-2*capacity for degree, capacity in zip(after['deg'], after['r'])]
    assert after['r'][3] == 2 and after['deg'][3] == 4
    return changed


def closure_control(current, child, bottom):
    residual_graph, _ = graph_record(*current)
    columns = current[1]
    tile_of = lambda vertex: vertex[0]//2*(columns//2)+vertex[1]//2
    removed = []
    residual = attachments = saturated_exports = 0
    for first, second in current[3]:
        if first in child and second in bottom:
            inside, outside = first, second
        elif second in child and first in bottom:
            inside, outside = second, first
        else:
            continue
        removed.append((first, second))
        if residual_graph['t'][tile_of(inside)] == 2:
            saturated_exports += 1
        elif residual_graph['t'][tile_of(outside)] == 2:
            attachments += 1
        else:
            residual += 1
    changed = (*current[:3], [edge for edge in current[3] if edge not in removed])
    assert direct_check(*current)-direct_check(*changed) == len(removed)
    before = general_region_ledger(current, child)
    after = general_region_ledger(changed, child)
    assert before['charge_twice']-after['charge_twice'] == residual+2*attachments
    return dict(residual=residual, saturated_attachments=attachments,
                saturated_exports=saturated_exports,
                charge_twice_before=before['charge_twice'], charge_twice_after=after['charge_twice'])


def small_ledger_controls():
    counts = []
    roles = set()
    for rows, columns in ((2, 2), (2, 4), (4, 2)):
        accepted = 0
        region_checks = 0
        for selected_mask, matching_indices in pairs(rows, columns):
            selected = {divmod(vertex, columns) for vertex in range(rows*columns)
                        if selected_mask >> vertex & 1}
            matching = [(divmod(first, columns), divmod(second, columns))
                        for first, second in matching_indices]
            current = rows, columns, selected, matching
            direct_check(*current)
            tiles = [{(row, column) for row in range(2*tile_row, 2*tile_row+2)
                      for column in range(2*tile_column, 2*tile_column+2)}
                     for tile_row in range(rows//2) for tile_column in range(columns//2)]
            for mask in range(1, 1 << len(tiles)):
                region = set().union(*(tile for index, tile in enumerate(tiles) if mask >> index & 1))
                general_region_ledger(current, region)
                outside = {(row, column) for row in range(rows) for column in range(columns)}-region
                closure = closure_control(current, region, outside)
                for role in ('residual', 'saturated_attachments', 'saturated_exports'):
                    if closure[role]:
                        roles.add(role)
                region_checks += 1
            accepted += 1
        counts.append(dict(shape=[rows, columns], feasible_pairs=accepted, regions=region_checks))
    assert roles == {'residual', 'saturated_attachments', 'saturated_exports'}
    current = escaping_band(3)
    inside = {(row, column) for row in (2, 3) for column in range(2, current[1]-2)}
    outside = {(row, column) for row in (4, 5) for column in range(current[1])}
    attachments = closure_control(current, inside, outside)
    receivers = closure_control(current, outside, inside)
    assert attachments['saturated_attachments'] == receivers['saturated_exports'] == 2
    assert receivers['charge_twice_before'] == receivers['charge_twice_after']
    shared = 4, 2, {(3, 1)}, [((1, 0), (2, 0)), ((1, 1), (2, 1))]
    direct_check(*shared)
    shared_graph, _ = graph_record(*shared)
    assert shared_graph['r'][1] == 1 and shared_graph['deg'][1] == 2
    receiver = {(row, column) for row in (2, 3) for column in range(2)}
    assert general_region_ledger(shared, receiver)['charge_twice'] == 0
    return dict(exhaustive=counts, attachment_control=attachments,
                saturated_export_control=receivers,
                shared_receiver=witness_record('Two residual ports, zero receiver budget', shared))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-modules', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_modules < 1:
        parser.error('--max-modules must be positive')
    records = []
    witnesses = []
    ledger_controls = small_ledger_controls()
    for branches, flipped in itertools.product(range(1, args.max_modules+1), (False, True)):
        original = configuration(branches)
        if flipped:
            original = capacity_two(original)
        original_regions = regions(original)
        for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, transpose, flip_rows, flip_columns)
            current = (*shape, selected, matching)
            moved_regions = {name: transformed(*original[:2], region, [],
                                               transpose, flip_rows, flip_columns)[1]
                             for name, region in original_regions.items()}
            assert direct_check(*current) == current[0]*current[1]//2
            assert len(selected) == 13*branches+31 and len(matching) == 11*branches+25
            assert not eligible(current)
            graph, components = graph_record(*current)
            assert not check_geometry(graph)
            assert sorted(component['excess'] for component in components) == [-1]+[0]*(4*branches+5-int(flipped))+[1]
            charges = {name: general_region_ledger(current, region)
                       for name, region in moved_regions.items()}
            assert [charges[name]['charge_twice'] for name in ('source', 'parent', 'child', 'bottom')] == [
                2, 0, branches-2, -branches]
            assert charges['child']['outgoing_saturated_attachments'] == 0
            assert charges['child']['incoming_saturated_attachments'] == 3
            source_component = next(component for component in components if component['excess'] == 1)
            assert set(charges['source']['tiles']) <= set(source_component['tiles'])
            assert len(source_component['tiles']) == len(charges['source']['tiles'])+int(flipped)
            assert source_component['edges'] == 3*branches+6+2*int(flipped)
            assert source_component['capacity'] == 3*branches+5+2*int(flipped)
            closure = closure_control(current, moved_regions['child'], moved_regions['bottom'])
            assert closure == dict(residual=branches, saturated_attachments=0,
                                   saturated_exports=0, charge_twice_before=branches-2,
                                   charge_twice_after=-2)
            records.append(dict(modules=branches, capacity_two_flip=flipped,
                                symmetry=[transpose, flip_rows, flip_columns],
                                shape=shape, objective=direct_check(*current),
                                regional_charge_twice={name: ledger['charge_twice']
                                                      for name, ledger in charges.items()},
                                closure=closure, max_capacity=max(graph['r'])))
        if branches in (1, 2, 3):
            record = witness_record(str(branches)+' mixed boundary modules'+
                                    (' with capacity-two flip' if flipped else ''), original)
            assert record['routing']['a'] == record['routing']['b'] == 1
            assert record['routing']['c'] == branches and record['routing']['f2'] == 0
            record['regions'] = {name: general_region_ledger(original, region)
                                 for name, region in original_regions.items()}
            witnesses.append(record)
        top_six = (6, original[1], {vertex for vertex in original[2] if vertex[0] < 6},
                   [edge for edge in original[3] if all(vertex[0] < 6 for vertex in edge)])
        assert direct_check(*top_six) == 3*original[1]
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/MIXED_BAND_BOUNDARY_DEBT.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_neutral_attachment_normalization.py', 'check_cross_component_compensation.py',
        'check_residual_corridors.py', 'verify_grid_five_sixths.py',
        'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', module_range=[1, args.max_modules],
                  symmetry_controls=len(records), witnesses=witnesses, controls=records,
                  ledger_controls=ledger_controls,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Controls for the written all-size equality family, general ledger and boundary-closure lemma. The lemma uses the established all-length width-six Omega theorem, not a finite search. No unrestricted grid or new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], module_range=report['module_range'],
                          symmetry_controls=len(records), witness_shapes=[
                              [record['rows'], record['columns']] for record in witnesses])))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
