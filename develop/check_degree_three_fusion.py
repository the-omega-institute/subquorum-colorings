"""Check the original receiver ledger for arbitrary degree-three physical fusions."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_two_leg_corner_obstruction import saturated_endpoint_donors
from degree_three_fusion import corner_join, four_way, occupied_bands, occupied_band_certificate
from rotor_networks import affine, chain, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, modules, require_frozen=True, allow_degree_four=False):
    direct_check(*current)
    network = combine(modules)
    assert network['selected'] == current[2]
    assert network['matching'] == current[3]
    endpoints = network['endpoints']
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    degrees = occupied_degrees(current)
    assert set(degrees.values()) <= ({3,4} if allow_degree_four else {3})
    for module in modules:
        old_occupied = module['endpoints'] | module['selected']
        assert all(len(set(neighbors(point)) & old_occupied) == 3 for point in module['endpoints'])
        assert all(len(set(neighbors(point)) & old_occupied) == 1 and
                   len(set(neighbors(point)) & module['endpoints']) == 1 for point in module['selected'])
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    contacts = {tuple(sorted((point, other))) for point in endpoints
                for other in set(neighbors(point)) & endpoints if owners[point] != owners[other]}
    contact_degree = Counter()
    missing_supports = []
    nonleaf_contacts = 0
    for first, second in contacts:
        first_module, second_module = modules[owners[first]], modules[owners[second]]
        for endpoint, foreign, module in ((first,second,first_module),(second,first,second_module)):
            if foreign not in module['selected']:
                assert degrees[endpoint] == 4
                missing_supports.append((endpoint,foreign))
        contact_degree.update((first, second))
        nonleaf_contacts += int(len(set(neighbors(first)) & first_module['endpoints']) > 1 or
                                len(set(neighbors(second)) & second_module['endpoints']) > 1)
    intratile = sum(tuple(coordinate//2 for coordinate in first) ==
                    tuple(coordinate//2 for coordinate in second) for first, second in contacts)
    assert len({endpoint for endpoint,foreign in missing_supports}) == len(missing_supports)
    assert {endpoint for endpoint,foreign in missing_supports} == {
        endpoint for endpoint,degree in degrees.items() if degree == 4}
    inside_defect = sum(tuple(coordinate//2 for coordinate in first) ==
                        tuple(coordinate//2 for coordinate in second)
                        for first,second in missing_supports)
    receiver = network['receiver']
    new_aligned_faces = 0
    local_cycles = 0
    tile_multiplicity = Counter()
    for tile in receiver:
        cells = vertices_of({tile})
        represented = {owners[point] for point in cells & endpoints}
        tile_multiplicity[len(represented)] += 1
        cross_edges = sum(first in cells and second in cells for first, second in contacts)
        rank = cross_edges-len(represented)+1
        assert rank in (0, 1)
        if rank:
            assert cells <= endpoints and len(represented) > 1
            if not allow_degree_four:
                assert len(represented) == 4
                assert all(len(cells & module['endpoints']) <= 1 for module in modules)
        if cells <= endpoints and len(represented) > 1:
            assert rank == 1
            new_aligned_faces += 1
        local_cycles += rank
    overlaps = sum(len(module['receiver']) for module in modules)-len(receiver)
    assert local_cycles == new_aligned_faces
    assert overlaps == intratile-new_aligned_faces
    assert len(network['receiver_selected']) == sum(len(module['receiver_selected'])
                                                  for module in modules)-2*intratile+inside_defect
    isolated_charge = sum(module['charge'] for module in modules)
    assert network['charge'] == isolated_charge-2*new_aligned_faces+inside_defect
    ledger = verify_terminal(current)
    assert sum(record['charge_twice'] for record in ledger['receivers']) == 2*network['charge']
    actual_donors = saturated_endpoint_donors(current)
    actual = {(tuple(donor['selected']), tuple(donor['anchor']), tuple(donor['guard']))
              for donor in actual_donors}
    chosen = []
    marked_witnesses = []
    positive = 0
    marked = 0
    for module in modules:
        if module['charge'] <= 0:
            continue
        positive += 1
        assert module['charge'] == 1
        selected, anchor, opposite, guard = module['guard']
        guardians = (set(neighbors(anchor)) & module['endpoints']) | {guard}
        assert len(guardians) == 3
        if any(degrees[endpoint] == 4 for endpoint in guardians):
            marked += 1
            witness = min(endpoint for endpoint in guardians if degrees[endpoint] == 4)
            foreign = next(foreign for endpoint,foreign in missing_supports if endpoint == witness)
            assert tuple(coordinate//2 for coordinate in witness) != tuple(
                coordinate//2 for coordinate in foreign)
            marked_witnesses.append(witness)
            continue
        assert selected in current[2]
        assert (selected, anchor, guard) in actual
        chosen.append(tuple(coordinate//2 for coordinate in selected))
    assert len(chosen) == len(set(chosen))
    assert len(chosen) == positive-marked
    assert len(set(marked_witnesses)) == marked
    degree_four = sum(degree == 4 for degree in degrees.values())
    assert inside_defect+marked <= degree_four
    assert len(chosen) <= ledger['empty_deficit']
    negative_mass = positive-isolated_charge
    strict_credit = negative_mass+2*new_aligned_faces-inside_defect-marked
    assert current[0]*current[1]//2-ledger['objective'] >= strict_credit
    if strict_credit >= 0:
        assert ledger['objective'] <= current[0]*current[1]//2
    frozen, layers = frozen_certificate(current)
    if require_frozen:
        assert frozen == endpoints
    return dict(endpoints=len(endpoints), selected=len(current[2]), matching_edges=len(current[3]),
                receiver_tiles=len(receiver), receiver_selected=len(network['receiver_selected']),
                isolated_charge=isolated_charge, actual_charge=network['charge'],
                new_aligned_faces=new_aligned_faces, contact_edges=len(contacts),
                intratile_contacts=intratile, maximum_contacts_per_endpoint=max(contact_degree.values(),default=0),
                nonleaf_contact_edges=nonleaf_contacts,
                degree_four_endpoints=sum(degree == 4 for degree in degrees.values()),
                intratile_degree_four_defect=inside_defect,
                marked_positive_modules=marked, negative_module_mass=negative_mass,
                certified_slack_lower_bound=strict_credit,
                tile_multiplicity=dict(tile_multiplicity), chosen_distinct_unit_donors=len(chosen),
                all_guard_donor_tiles=len({tuple(donor['tile']) for donor in actual_donors}),
                endpoint_components=len(endpoint_components(current)), frozen_endpoints=len(frozen),
                freezing_layers=len(layers), objective=ledger['objective'],
                half_area=current[0]*current[1]//2)


def phase_images(modules):
    for symmetry in itertools.product((False,True),repeat=3):
        oriented = [transform_module(module,symmetry) for module in modules]
        occupied = set.union(*(module['endpoints'] | module['selected'] for module in oriented))
        low_row = min(point[0] for point in occupied)
        low_column = min(point[1] for point in occupied)
        for row_phase,column_phase in itertools.product(range(2),repeat=2):
            offset = 2*(-low_row//2+1)+row_phase,2*(-low_column//2+1)+column_phase
            moved = [transform_module(module,(False,False,False),offset) for module in oriented]
            network = combine(moved)
            points = network['endpoints'] | network['selected']
            rows = 2*(max(point[0] for point in points)//2+1)
            columns = 2*(max(point[1] for point in points)//2+1)
            image = rows,columns,network['selected'],network['matching']
            yield symmetry,(row_phase,column_phase),offset,image,moved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    junctions = []
    images = []
    for width in (8, 10, 14, 20, 40, 80):
        current, modules = four_way(width)
        report = inspect(current, modules)
        assert report['endpoints'] == 8*width+24
        assert report['selected'] == 32
        assert report['receiver_tiles'] == 2*width+17
        assert report['receiver_selected'] == 24
        assert report['actual_charge'] == 2
        assert report['isolated_charge'] == 4
        assert report['new_aligned_faces'] == 1
        assert report['maximum_contacts_per_endpoint'] == 2
        assert report['chosen_distinct_unit_donors'] == 4
        junctions.append(dict(width=width, **report))
        for symmetry,phase,offset,image,moved in phase_images(modules):
            record = inspect(image,moved)
            central = {affine((width+row,width+column),symmetry,offset)
                       for row,column in itertools.product((0,1),repeat=2)}
            expected_new_face = int(len({tuple(coordinate//2 for coordinate in point)
                                         for point in central}) == 1)
            assert record['new_aligned_faces'] == expected_new_face
            images.append(dict(width=width,symmetry=symmetry,phase=phase,**record))
    corners = []
    for width in (6, 8, 14, 40):
        current, modules = corner_join(width)
        record = inspect(current, modules)
        assert record['nonleaf_contact_edges'] == 1
        assert record['new_aligned_faces'] == 0
        assert record['actual_charge'] == 2-width
        corners.append(dict(width=width, **record))
    previous = []
    for length in (1,2,3,4,8):
        current, modules = chain(length)
        record = inspect(current, modules)
        assert record['new_aligned_faces'] == 0 and record['actual_charge'] == length+1
        previous.append(dict(stars=length, **record))
    bands = []
    band_images = []
    for width in (6,8,10,14,20,40):
        current,modules = occupied_bands(width)
        record = inspect(current,modules,allow_degree_four=True)
        assert record['degree_four_endpoints'] == 4
        assert record['intratile_degree_four_defect'] == 4
        assert record['new_aligned_faces'] == 2
        assert record['marked_positive_modules'] == 0
        assert record['actual_charge'] == 2-width
        assert record['negative_module_mass'] == width-1
        assert record['certified_slack_lower_bound'] == width-1
        mates = {endpoint:partner for edge in current[3]
                 for endpoint,partner in (edge,edge[::-1])}
        earlier = set()
        for endpoint,first,second in occupied_band_certificate(width):
            assert endpoint not in earlier and first != second
            assert {first,second} <= set(neighbors(endpoint))
            assert mates[endpoint] not in {first,second}
            assert all(point in current[2] or mates.get(point) in earlier for point in (first,second))
            earlier.add(endpoint)
        assert earlier == set(mates)
        record['ordered_certificate_endpoints'] = len(earlier)
        bands.append(dict(width=width,**record))
        for symmetry,phase,offset,image,moved in phase_images(modules):
            checked = inspect(image,moved,allow_degree_four=True)
            assert checked['degree_four_endpoints'] == 4
            assert checked['intratile_degree_four_defect'] == 2*checked['new_aligned_faces']
            band_images.append(dict(width=width,symmetry=symmetry,phase=phase,**checked))
    witness, _ = four_way(8)
    output = dict(status='PASS', four_way_junctions=junctions,
                  symmetry_phase_images=images, nonleaf_corner_joins=corners,
                  previous_branched_chains=previous,
                  controlled_degree_four_bands=bands,
                  degree_four_band_phase_images=band_images,
                  scope='Finite controls for the separate general physical fusion proof. '
                        'No predefined ports or single-use-port hypothesis; exact original '
                        'receiver charge subtracts two per new aligned mixed-module P face '
                        'and adds the exact intratile new-neighbor defect at degree-four endpoints. '
                        'General geometric proof and no-reuse argument are not inferred from samples.',
                  four_way_witness=dict(shape=witness[:2],selected=sorted(witness[2]),matching=witness[3]))
    arguments.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',four_way_widths=len(junctions),
                          all_phase_symmetry_images=len(images),nonleaf_corner_joins=len(corners),
                          previous_chains=len(previous),degree_four_band_widths=len(bands),
                          degree_four_phase_images=len(band_images),base_junction=junctions[0])))


if __name__ == '__main__':
    main()
