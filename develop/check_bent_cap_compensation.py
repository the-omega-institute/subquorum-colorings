"""Check positive frozen bent receivers and their canonical sparse payment tile."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate, normalize
from check_residual_corridors import direct_check, graph_record, transformed
from check_thin_component_receivers import combined_control


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def bent_cap(width):
    assert width >= 4 and width % 2 == 0
    matching = [((0, column), (0, column+1)) for column in range(0, width, 2)]
    matching += [((1, column), (1, column+1)) for column in range(1, width-1, 2)]
    matching += [((1, column), (2, column)) for column in (0, width-1)]
    selected = {(0, -1), (0, width), (2, -1), (2, width), (3, 0), (3, width-1)}
    move = lambda vertex: (vertex[0]+2, vertex[1]+3)
    return 8, width+8, {move(vertex) for vertex in selected}, [
        tuple(move(vertex) for vertex in edge) for edge in matching]


def charge_twice(graph, columns, tile):
    position = tile[0]*(columns//2)+tile[1]
    return 0 if graph['t'][position] == 2 else graph['deg'][position]-2*graph['r'][position]


def verify(width):
    current = bent_cap(width)
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    assert len(endpoints) == 2*width+2 and len(endpoint_data(current)[2]) == width-1
    receiver = checked['receivers'][0]
    assert (receiver['tiles'], receiver['selected'], receiver['endpoints'], receiver['charge_twice']) == (
        width//2+3, 6, 2*width+2, 2)
    donor = (2, 2)
    tiles = {(row//2, column//2) for row, column in endpoints}
    assert donor not in tiles
    graph, _ = graph_record(*current)
    baseline_charge = charge_twice(graph, current[1], donor)
    assert baseline_charge == -4
    modifications = [dict(kind='baseline', donor_charge_twice=baseline_charge)]
    if width >= 6:
        optional = (*current[:2], current[2] | {(5, 5)}, current[3])
        direct_check(*optional)
        graph, _ = graph_record(*optional)
        assert charge_twice(graph, optional[1], donor) == -2
        assert verify_terminal(optional)['receivers'][0]['charge_twice'] == 2
        modifications.append(dict(kind='sharp_selected_exterior', donor_charge_twice=-2))
        attached = (*current[:2], current[2], current[3]+[((5, 5), (6, 5))])
        direct_check(*attached)
        graph, _ = graph_record(*attached)
        assert charge_twice(graph, attached[1], donor) == -3
        modifications.append(dict(kind='other_component_endpoint_in_donor', donor_charge_twice=-3))
        ending, operations = normalize(attached)
        assert operations and endpoints <= endpoint_data(ending)[0]
        assert not {(4, 4), (4, 5), (5, 4), (5, 5)} & endpoint_data(ending)[0]
        assert verify_terminal(ending)['receivers'][0]['charge_twice'] == 2
    return dict(width=width, endpoint_squares=width-1, receiver=receiver,
                canonical_donor=list(donor), external_controls=modifications)


def donor_orientation_controls():
    endpoints = {(row, column) for row in (-2, -1) for column in (-1, 0, 1, 2)} | {(0, -1)}
    selected = {(-2, -2), (0, -2), (1, -1)}
    records = []
    for mirror, turns in itertools.product((False, True), range(4)):
        def rotate(vertex):
            row, column = vertex
            if mirror:
                column = 1-column
            for _ in range(turns):
                row, column = column, 1-row
            return row, column
        other_endpoints = {rotate(vertex) for vertex in endpoints}
        other_selected = {rotate(vertex) for vertex in selected}
        shared = endpoints & other_endpoints
        if shared:
            records.append(dict(mirror=mirror, turns=turns, shared_endpoint=min(shared)))
            continue
        witnesses = []
        for vertex in selected | other_selected:
            row, column = vertex
            adjacent = {(row-1, column), (row+1, column), (row, column-1), (row, column+1)}
            neighbors = sorted(adjacent & (endpoints | other_endpoints))
            if len(neighbors) >= 2:
                witnesses.append(dict(selected=vertex, endpoint_neighbors=neighbors[:2]))
        assert witnesses
        records.append(dict(mirror=mirror, turns=turns, infeasibility=witnesses[0]))
    return records


def mixed_payment_control():
    pieces = []
    for index, symmetry in enumerate(itertools.product((False, True), repeat=3)):
        source = bent_cap(4+2*index)
        shape, selected, matching = transformed(*source, *symmetry)
        _, marker, _ = transformed(source[0], source[1], {(4, 4), (4, 5), (5, 4), (5, 5)}, [], *symmetry)
        donor = {(row//2, column//2) for row, column in marker}
        assert len(donor) == 1
        pieces.append(((*shape, selected, matching), next(iter(donor))))
    baseline = combined_control()
    pieces.append(((*baseline['initial_shape'], set(map(tuple, baseline['selected'])),
                    [tuple(map(tuple, edge)) for edge in baseline['matching']]), None))
    selected = set()
    matching = []
    donors = set()
    fixed_endpoints = set()
    offset = 0
    columns = max(piece[0][1] for piece in pieces)+4
    for current, donor in pieces:
        move = lambda vertex: (vertex[0]+offset, vertex[1]+2)
        selected.update(move(vertex) for vertex in current[2])
        matching.extend(tuple(move(vertex) for vertex in edge) for edge in current[3])
        if donor is not None:
            donors.add((donor[0]+offset//2, donor[1]+1))
            fixed_endpoints.update(move(vertex) for vertex in endpoint_data(current)[0])
        offset += current[0]+4
    current = offset, columns, selected, matching
    ending, operations = normalize(current)
    endpoints = endpoint_data(ending)[0]
    assert fixed_endpoints <= endpoints
    graph, _ = graph_record(*ending)
    checked = verify_terminal(ending)
    assert len(donors) == 8
    assert sum(receiver['charge_twice'] > 0 for receiver in checked['receivers']) == 8
    assert all(receiver['charge_twice'] <= 0 or receiver['charge_twice'] == 2
               for receiver in checked['receivers'])
    for tile in donors:
        cells = {(2*tile[0]+row, 2*tile[1]+column) for row, column in itertools.product((0, 1), repeat=2)}
        assert not cells & endpoints
        assert len(cells & ending[2]) <= 1
    donor_deficit = sum(1-graph['t'][row*(columns//2)+column] for row, column in donors)
    other_empty_deficit = checked['empty_deficit']-sum(
        2-graph['t'][row*(columns//2)+column] for row, column in donors)
    receiver_deficit_twice = -sum(receiver['charge_twice'] for receiver in checked['receivers']
                                  if receiver['charge_twice'] <= 0)
    assert checked['area']-2*checked['objective'] == (
        receiver_deficit_twice+2*donor_deficit+2*other_empty_deficit)
    assert direct_check(*current) == checked['objective'] <= checked['area']//2-1
    return dict(initial_shape=current[:2], selected=sorted(selected), matching=matching,
                positive_sources=8, distinct_no_endpoint_donors=sorted(donors),
                normalization_bundles=len(operations), donor_deficit=donor_deficit,
                other_empty_deficit=other_empty_deficit, receiver_deficit_twice=receiver_deficit_twice,
                **checked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = [verify(width) for width in range(4, 65, 2)]
    smallest = bent_cap(4)
    report = dict(status='ALL_CHECKS_PASSED', even_widths=len(records),
                  exterior_controls=sum(len(record['external_controls']) for record in records),
                  family=records,
                  donor_orientation_checks=donor_orientation_controls(),
                  mixed_payment=mixed_payment_control(),
                  smallest=dict(shape=smallest[:2], selected=sorted(smallest[2]), matching=smallest[3]),
                  refuted_rule='Every complete bundle-terminal endpoint component has nonpositive whole-receiver charge.',
                  proved_local_payment='The positive receiver has charge one; its canonical sparse tile has original charge at most minus one in every feasible completion retaining the component and forced supports.',
                  proved_terminal_payment='In globally terminal completions canonical donors have no endpoints and are distinct across all eight source orientations; mixed thin/one-square/prescribed-bent sources satisfy coefficient one without reused tiles.',
                  unresolved='Arbitrary bent shapes and complete coverage of every possible positive receiver remain open; no universal grid coefficient-one bound follows.',
                  global_coefficient_one_refuted=False)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('family', 'smallest', 'mixed_payment', 'donor_orientation_checks')}))


if __name__ == '__main__':
    main()
