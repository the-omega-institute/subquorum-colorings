"""Physical controls for frozen adjacent rails and their exact receiver cost."""

import argparse
import itertools
import json
from pathlib import Path

from check_bipartite_promotion import verify as verify_orientations
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed
from check_stepped_patch_isolation import embedded


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def sharp_word(length):
    return {0, length-1} | set(range(2, length-2, 2))


def rail_elbow(width, height, rails, sharp_corner=True):
    root = elbow(width, height)
    relative = lambda point: (point[0]-4, point[1]-5)
    selected = {relative(point) for point in root[2]}
    matching = [tuple(relative(point) for point in edge) for edge in root[3]]
    root_endpoints = {point for edge in matching for point in edge}
    if sharp_corner:
        selected.add((2, 2))
    previous_end = -2
    for start, length, top in rails:
        assert start >= 0 and length >= 4 and length % 2 == 0
        assert start+length <= width and start >= previous_end+2
        assert {0, length-1} <= top <= set(range(length))
        assert not any(index+1 in top for index in top)
        previous_end = start+length-1
        selected.update((-2, start+index) for index in top)
        matching.extend(((-1, column), (-1, column+1))
                        for column in range(start, start+length, 2))
    current, move = embedded(selected, matching)
    root_core = {move(point) for point in root_endpoints}
    root_selected = {move(relative(point)) for point in root[2]}
    donor = {move(point) for point in itertools.product((2, 3), (1, 2))}
    loss = sum(length//2-len(top) for _, length, top in rails)
    misaligned = sum(start % 2 == 0 for start, _, _ in rails)
    return current, dict(root=root_core, root_selected=root_selected, donor=donor,
                         loss=loss, misaligned=misaligned, move=move)


def inspect(width, height, rails, symmetries=False):
    current, certificate = rail_elbow(width, height, rails)
    endpoints = endpoint_data(current)[0]
    checked = verify_terminal(current)
    assert endpoint_components(current) == [endpoints]
    assert frozen_certificate(current)[0] == endpoints
    assert min(occupied_degrees(current).values()) >= 3
    expected_charge = 1-certificate['loss']-2*certificate['misaligned']
    assert checked['receivers'][0]['charge_twice'] == 2*expected_charge
    donor = certificate['donor']
    assert not donor & endpoints and len(donor & current[2]) == 1
    mates = {point: other for edge in current[3] for point, other in (edge, edge[::-1])}
    kept = current[2] | certificate['root']
    used_tiles = {(row//2, column//2) for row, column in certificate['root']}
    rail_records = []
    for start, length, top in rails:
        added = {certificate['move']((-1, column)) for column in range(start, start+length)}
        tiles = {(row//2, column//2) for row, column in added}
        assert len(tiles) == length//2+int(start % 2 == 0)
        assert not tiles & used_tiles
        used_tiles |= tiles
        cells = vertices_of(tiles)
        expected_top = {certificate['move']((-2, start+index)) for index in top}
        assert cells & current[2] == expected_top
        assert cells & endpoints == added
        for order in (range(start, start+length, 2), range(start+length-1, start, -2)):
            for column in order:
                point = certificate['move']((-1, column))
                assert len(set(neighbors(point)) & kept) >= 2
                assert mates[point] not in set(neighbors(point)) & kept
                kept.add(mates[point])
        cost = len(top)-length//2-2*int(start % 2 == 0)
        assert len(current[2] & cells)+len(added)//2-2*len(tiles) == cost
        assert cost <= -2*int(start % 2 == 0)
        rail_records.append(dict(start=start, length=length, top_selected=len(top),
                                 receiver_tiles=len(tiles), charge=cost))
    assert endpoints <= kept
    images = 0
    if symmetries:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            image = *shape, selected, matching
            assert direct_check(*image) == checked['objective']
            assert frozen_certificate(image)[0] == endpoint_data(image)[0]
            assert verify_terminal(image)['receivers'][0]['charge_twice'] == 2*expected_charge
            images += 1
    return dict(width=width, height=height, rails=rail_records, charge=expected_charge,
                root_endpoints=len(certificate['root']), endpoints=len(endpoints),
                receiver_tiles=len(used_tiles), loss=certificate['loss'],
                misaligned_rails=certificate['misaligned'], symmetry_images=images)


def word_controls():
    records = []
    for length in range(4, 15, 2):
        for bits in itertools.product((False, True), repeat=length-2):
            word = {0, length-1} | {index+1 for index, chosen in enumerate(bits) if chosen}
            if any(index+1 in word for index in word):
                continue
            for start in (0, 1):
                width = length+2
                records.append(inspect(width, 4, [(start, length, word)]))
    return records


def packing_controls():
    records = []
    for sizes in ((1, 1), (1, 2, 1), (1, 1, 1, 1)):
        selected, matching, donors = set(), [], []
        expected_loss = expected_misaligned = 0
        shape = 0, 0
        for index, parity in enumerate(sizes):
            start = parity % 2
            word = sharp_word(4) if index % 2 == 0 else {0, 5}
            length = 4 if index % 2 == 0 else 6
            current, certificate = rail_elbow(10, 4, [(start, length, word)])
            shift = lambda point: (point[0], point[1]+32*index)
            selected.update(shift(point) for point in current[2])
            matching.extend(tuple(shift(point) for point in edge) for edge in current[3])
            donors.append({shift(point) for point in certificate['donor']})
            expected_loss += certificate['loss']
            expected_misaligned += certificate['misaligned']
            shape = max(shape[0], current[0]), max(shape[1], current[1]+32*index)
        packed = *shape, selected, matching
        checked = verify_terminal(packed)
        assert len(checked['receivers']) == len(sizes)
        assert sum(len(donor) for donor in donors) == len(set.union(*donors))
        deficit = checked['area']//2-checked['objective']
        residual = checked['empty_deficit']-len(sizes)
        assert residual >= 0
        assert deficit == residual+expected_loss+2*expected_misaligned
        records.append(dict(components=len(sizes), loss=expected_loss,
                            misaligned_rails=expected_misaligned, deficit=deficit,
                            remaining_physical_deficit=residual))
    return records


def nonterminal_exterior_controls():
    records = []
    for length, start in itertools.product((4, 6, 8, 16, 32, 64), (0, 1)):
        current, certificate = rail_elbow(length+2, 4, [(start, length, sharp_word(length))])
        receiver = {(row//2, column//2) for row, column in endpoint_data(current)[0]}
        changed = *current[:3], current[3]+[((0, 0), (0, 1))]
        assert direct_check(*changed) == direct_check(*current)+1
        assert min(occupied_degrees(changed).values()) == 1
        assert certificate['root'] <= frozen_certificate(changed)[0]
        graph, _ = graph_record(*changed)
        charge_twice = sum(graph['deg'][row*(changed[1]//2)+column]
                           - 2*graph['r'][row*(changed[1]//2)+column]
                           for row, column in receiver
                           if graph['t'][row*(changed[1]//2)+column] < 2)
        raw = 2*len(changed[2] & vertices_of(receiver))
        raw += len(endpoint_data(changed)[0] & vertices_of(receiver))-4*len(receiver)
        assert charge_twice == raw == 2*(1-2*int(start % 2 == 0))
        records.append(dict(length=length, start=start, ambient_single_terminal=False,
                            receiver_charge_twice=charge_twice))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    words = word_controls()
    large = []
    for length, height in itertools.product((4, 8, 16, 32, 64, 128), (4, 8, 16)):
        for start in (0, 1):
            large.append(inspect(length+2, height, [(start, length, sharp_word(length))], True))
    multiple = []
    for count in (2, 3, 4, 8):
        rails = [(5*index, 4, sharp_word(4)) for index in range(count)]
        multiple.append(inspect(2*((5*count+3)//2), 4, rails, True))
    current, certificate = rail_elbow(6, 4, [(1, 4, {0, 3})])
    occupied = current[2] | endpoint_data(current)[0]
    exhaustive = verify_orientations(current[2], current[3],
        {point: set(neighbors(point)) & occupied for point in occupied},
        {point: sum(point) % 2 for point in occupied})
    assert exhaustive['oriented_choices'] == 3**11 and exhaustive['feasible_choices'] == 1
    report = dict(status='ALL_CHECKS_PASSED', selection_word_cases=len(words), words=words,
                  large_parameter_cases=len(large), large_parameters=large,
                  multiple_rail_cases=len(multiple), multiple_rails=multiple,
                  symmetry_images=sum(record['symmetry_images'] for record in large+multiple),
                  packs=packing_controls(), nonterminal_exteriors=nonterminal_exterior_controls(),
                  positive_isolation_obstacle=dict(
                      shape=current[:2], selected=sorted(current[2]), matching=current[3],
                      prescribed_root=sorted(certificate['root']), donor=sorted(certificate['donor']),
                      charge=1, **exhaustive),
                  scope='Finite controls for the independent all-length written freezing and charge '
                        'proof. Isolation rule fails, grid target not refuted. Complete enlarged '
                        'component required for charge calculation, not for freezing.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key in ('status', 'selection_word_cases', 'large_parameter_cases',
                                 'multiple_rail_cases', 'symmetry_images')}))


if __name__ == '__main__':
    main()
