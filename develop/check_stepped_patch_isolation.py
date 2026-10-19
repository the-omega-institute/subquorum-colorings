"""Controls for intrinsic stepped-patch closure and one-port isolation."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, single_normalize, verify_terminal, vertices_of
from check_cooperative_promotion import apply_bundle, neighbors, occupied_degrees
from check_guarded_stepped_arms import stepped
from check_orthogonal_source_mouths import feasible
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def certificate(k):
    source = stepped(k)
    endpoints, selected = source['endpoints'], source['selected']
    blanks = set()
    for support in selected:
        anchors = set(neighbors(support)) & endpoints
        assert len(anchors) == 1
        blanks.update(set(neighbors(support))-anchors)
    boundary = set().union(*(set(neighbors(point)) for point in endpoints))-endpoints-selected
    unresolved = boundary-blanks
    expected = {(-1, 3), (1, 5), (4, 3)}
    expected |= {(row, 3) for row in range(6, source['bottom'], 2)}
    assert unresolved == expected
    port = (-1, 3)
    for point in unresolved:
        available = set(neighbors(point))-blanks
        if point == port:
            assert available == {(-2, 3), (0, 3)}
        else:
            assert available <= endpoints
    return dict(k=k, unresolved_boundary=len(unresolved), unique_port=port,
                possible_port_neighbors=[(-2, 3), (0, 3)])


def embedded(selected, matching):
    occupied = selected | {point for edge in matching for point in edge}
    top = min(point[0] for point in occupied)-4
    left = min(point[1] for point in occupied)-4
    row_offset = -top+(-top % 2)
    column_offset = -left+((1+left) % 2)
    move = lambda point: (point[0]+row_offset, point[1]+column_offset)
    bottom = max(point[0] for point in occupied)+row_offset+5
    right = max(point[1] for point in occupied)+column_offset+5
    current = (bottom+bottom % 2, right+right % 2, {move(point) for point in selected},
               [tuple(move(point) for point in edge) for edge in matching])
    return current, move


def attached(k, length):
    source = stepped(k)
    selected = set(source['selected'])
    selected.update((-index, 4 if index % 2 == 0 else 2)
                    for index in range(2, 2*length+1))
    selected.add((-2*length-1, 3))
    matching = source['matching']+[((-index, 3), (-index-1, 3))
                                   for index in range(1, 2*length, 2)]
    current, move = embedded(selected, matching)
    assert feasible(current)
    core = {move(point) for point in source['endpoints']}
    port, mate = move((-1, 3)), move((-2, 3))
    assert len(endpoint_components(current)) == 1
    assert occupied_degrees(current)[port] == 2
    assert core <= frozen_certificate(current)[0]
    objective = direct_check(*current)
    isolated = apply_bundle(current, [(port, mate)])
    assert core in endpoint_components(isolated)
    assert core <= frozen_certificate(isolated)[0]
    assert direct_check(*isolated) == objective
    normalized, moves = single_normalize(isolated)
    assert core in endpoint_components(normalized)
    assert verify_terminal(normalized)['receivers'][0]['charge_twice'] == 2
    images = 0
    for symmetry in itertools.product((False, True), repeat=3):
        shape, image_selected, image_matching = transformed(*current, *symmetry)
        image = *shape, image_selected, image_matching
        assert feasible(image)
        candidates = [point for point, degree in occupied_degrees(image).items() if degree <= 2]
        assert len(candidates) == 1
        first = candidates[0]
        second = next(other for edge in image[3] for point, other in (edge, edge[::-1]) if point == first)
        changed = apply_bundle(image, [(first, second)])
        assert direct_check(*changed) == objective
        assert len(endpoint_components(changed)) == 1+int(length > 1)
        images += 1
    return dict(k=k, attached_matching_edges=length, isolation_moves=1,
                later_single_moves=moves, objective=objective, symmetry_images=images)


def paired(k, other_k):
    first, second = stepped(k), stepped(other_k)
    reflect = lambda point: (-3-point[0], 6-point[1])
    selected = first['selected'] | {reflect(point) for point in second['selected']}
    matching = first['matching']+[tuple(reflect(point) for point in edge)
                                  for edge in second['matching']]
    matching.append(((-1, 3), (-2, 3)))
    current, move = embedded(selected, matching)
    first_core = {move(point) for point in first['endpoints']}
    second_core = {move(reflect(point)) for point in second['endpoints']}
    first_port, second_port = move((-1, 3)), move((-2, 3))
    assert feasible(current) and not first_core & second_core
    assert len(endpoint_components(current)) == 1
    assert first_core | second_core <= frozen_certificate(current)[0]
    assert occupied_degrees(current)[first_port] == occupied_degrees(current)[second_port] == 2
    objective = direct_check(*current)
    initial_endpoints = endpoint_data(current)[0]
    initial_tiles = {(row//2, column//2) for row, column in initial_endpoints}
    initial_charge = len(vertices_of(initial_tiles) & current[2])+len(initial_endpoints)//2-2*len(initial_tiles)
    assert initial_charge == -other_k
    for promote, remove in ((first_port, second_port), (second_port, first_port)):
        isolated = apply_bundle(current, [(promote, remove)])
        assert endpoint_data(isolated)[0] == first_core | second_core
        assert set(map(frozenset, endpoint_components(isolated))) == {
            frozenset(first_core), frozenset(second_core)}
        assert sorted(record['charge_twice'] for record in verify_terminal(isolated)['receivers']) == [-2*other_k, 2]
        assert frozen_certificate(isolated)[0] == first_core | second_core
        assert direct_check(*isolated) == objective
    return dict(k=k, other_k=other_k, initial_component_count=1,
                final_component_count=2, isolation_moves=1, valid_orientations=2,
                initial_raw_receiver_charge=initial_charge,
                isolated_receiver_charges=[1, -other_k], exposed_donor_deficit=1,
                alignment='The second patch has the translated negative-charge phase.')


def positive_pair(k, other_k, length):
    assert length >= 2
    first, second = stepped(k), stepped(other_k)
    reflect = lambda point: (-2*length-1-point[0], point[1])
    selected = first['selected'] | {reflect(point) for point in second['selected']}
    matching = first['matching']+[tuple(reflect(point) for point in edge)
                                  for edge in second['matching']]
    matching += [((-index, 3), (-index-1, 3)) for index in range(1, 2*length, 2)]
    current, move = embedded(selected, matching)
    cores = [{move(point) for point in first['endpoints']},
             {move(reflect(point)) for point in second['endpoints']}]
    assert feasible(current) and len(endpoint_components(current)) == 1
    initial_endpoints = endpoint_data(current)[0]
    initial_tiles = {(row//2, column//2) for row, column in initial_endpoints}
    raw = len(vertices_of(initial_tiles) & current[2])+len(initial_endpoints)//2-2*len(initial_tiles)
    assert raw == 2-length
    objective = direct_check(*current)
    isolated = current
    moves = 0
    for port in (move((-1, 3)), move((-2*length, 3))):
        if port not in endpoint_data(isolated)[0]:
            continue
        mate = next(other for edge in isolated[3] for point, other in (edge, edge[::-1]) if point == port)
        isolated = apply_bundle(isolated, [(port, mate)])
        moves += 1
    assert all(core in endpoint_components(isolated) for core in cores)
    ending, subsequent = single_normalize(isolated)
    checked = verify_terminal(ending)
    assert sorted(record['charge_twice'] for record in checked['receivers']) == [2, 2]
    assert endpoint_data(ending)[0] == set.union(*cores)
    assert checked['area']//2-objective == checked['empty_deficit']-2
    assert direct_check(*ending) == objective
    return dict(k=k, other_k=other_k, connecting_matching_edges=length,
                initial_raw_receiver_charge=raw, isolation_moves=moves,
                later_single_moves=subsequent, final_positive_receivers=2,
                no_endpoint_deficit=checked['empty_deficit'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    boundaries = [certificate(k) for k in (*range(1, 33), 64, 128)]
    attachments = [attached(k, length) for k, length in itertools.product(
        (1, 2, 5, 16), (1, 2, 5, 16))]
    pairs = [paired(k, other_k) for k, other_k in itertools.product((1, 2, 5, 16), repeat=2)]
    positive_pairs = [positive_pair(k, other_k, length) for k, other_k, length in
                      itertools.product((1, 2, 5, 16), (1, 2, 5, 16), (2, 3, 8))]
    report = dict(status='ALL_CHECKS_PASSED', boundary_cases=len(boundaries), boundaries=boundaries,
                  attachment_cases=len(attachments), attachments=attachments,
                  attachment_symmetry_images=sum(record['symmetry_images'] for record in attachments),
                  paired_port_cases=len(pairs), paired_ports=pairs,
                  positive_pair_cases=len(positive_pairs), positive_pairs=positive_pairs,
                  scope='Finite controls of the independent all-k boundary proof and general one-port '
                        'isolation argument. Complete component recognition, simultaneous family safety '
                        'and global adapters remain written proofs. No universal receiver ceiling claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items()
                      if key not in ('boundaries', 'attachments', 'paired_ports', 'positive_pairs')}))


if __name__ == '__main__':
    main()
