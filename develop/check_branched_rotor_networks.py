"""Independent physical controls for the written branched-network theorems."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_two_leg_corner_obstruction import saturated_endpoint_donors
from rotor_networks import chain, combine, rotor, star_modules, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, modules):
    objective = direct_check(*current)
    endpoints = {point for edge in current[3] for point in edge}
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert len(endpoint_components(current)) == 1
    assert set(occupied_degrees(current).values()) == {3}
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    contacts = {tuple(sorted((point, other))) for point in endpoints
                for other in set(neighbors(point)) & endpoints if owners[point] != owners[other]}
    used_ports = Counter()
    for first, second in contacts:
        first_module, second_module = modules[owners[first]], modules[owners[second]]
        assert first in first_module['ports'] and second in second_module['ports']
        assert first in second_module['selected'] and second in first_module['selected']
        used_ports.update((first, second))
    assert set(used_ports.values()) <= {1}
    consumed = set.union(*(module['selected'] for module in modules)) & endpoints
    assert consumed == set(used_ports)
    assert len(contacts) == len(modules)-1
    intratile = sum(tuple(coordinate//2 for coordinate in first) ==
                    tuple(coordinate//2 for coordinate in second) for first, second in contacts)
    receiver = set.union(*(module['receiver'] for module in modules))
    selected_in = len(vertices_of(receiver) & current[2])
    assert len(receiver) == sum(len(module['receiver']) for module in modules)-intratile
    assert selected_in == sum(len(module['receiver_selected']) for module in modules)-2*intratile
    ledger = verify_terminal(current)
    charge = ledger['receivers'][0]['charge_twice']//2
    assert charge == sum(module['charge'] for module in modules)
    donors = saturated_endpoint_donors(current)
    actual = {(tuple(donor['selected']), tuple(donor['anchor']), tuple(donor['guard']))
              for donor in donors}
    chosen_tiles = []
    for module in modules:
        if module['charge'] <= 0:
            continue
        assert module['charge'] == 1 and module['guard'] is not None
        chosen, anchor, opposite, guard = module['guard']
        assert (chosen, anchor, guard) in actual
        tile = tuple(coordinate//2 for coordinate in chosen)
        assert opposite == tuple(4*coordinate+1-value for coordinate, value in zip(tile, chosen))
        assert vertices_of({tile}) & current[2] == {chosen}
        chosen_tiles.append(tile)
    assert len(chosen_tiles) == len(set(chosen_tiles))
    assert charge <= len(chosen_tiles) <= ledger['empty_deficit']
    assert objective <= current[0]*current[1]//2
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    return dict(endpoints=len(endpoints), selected=len(current[2]), matching_edges=len(current[3]),
                receiver_tiles=len(receiver), receiver_selected=selected_in,
                charge=charge, primitive_modules=len(modules), splices=len(contacts),
                intratile_splices=intratile, intertile_splices=len(contacts)-intratile,
                chosen_distinct_unit_donors=len(chosen_tiles),
                all_distinct_unit_donors=len({tuple(donor['tile']) for donor in donors}),
                endpoint_free_deficit=ledger['empty_deficit'], objective=objective,
                half_area=current[0]*current[1]//2, frozen_endpoints=len(frozen),
                freezing_layers=len(layers))


def rotor_controls():
    records = []
    for row, column in itertools.product(range(2), repeat=2):
        module = transform_module(rotor(), (False, False, False), (row, column))
        current = 8, 8, module['selected'], module['matching']
        direct_check(*current)
        assert set(occupied_degrees(current).values()) == {3}
        assert frozen_certificate(current)[0] == module['endpoints']
        assert len(module['receiver_selected']) == 4
        assert len(module['receiver']) == (5 if (row, column) == (0, 0) else 4)
        assert module['charge'] == (-2 if (row, column) == (0, 0) else 0)
        records.append(dict(phase=[row, column], tiles=len(module['receiver']),
                            receiver_selected=4, charge=module['charge']))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    phases = rotor_controls()
    stars = []
    for width in (6, 8, 10, 14, 20, 40):
        modules = [transform_module(module, (False, False, False), (width-2, width-2))
                   for module in star_modules(width)]
        network = combine(modules)
        current = 2*width+2, 2*width+2, network['selected'], network['matching']
        record = inspect(current, modules)
        assert record['endpoints'] == 8*width+32
        assert record['selected'] == 40
        assert record['receiver_tiles'] == 2*width+21
        assert record['receiver_selected'] == 28
        assert record['charge'] == 2
        stars.append(dict(width=width, **record))
    lengths = list(range(1, 17))+[24, 32, 64]
    chains = []
    images = 0
    for amount in lengths:
        current, modules = chain(amount)
        record = inspect(current, modules)
        expected = dict(endpoints=178*amount-34, selected=46*amount-6,
                        matching_edges=89*amount-17, receiver_tiles=58*amount-9,
                        receiver_selected=28*amount, charge=amount+1,
                        primitive_modules=6*amount-1, splices=6*amount-2,
                        intratile_splices=6*amount-2, intertile_splices=0,
                        chosen_distinct_unit_donors=4*amount,
                        all_distinct_unit_donors=8*amount,
                        endpoint_free_deficit=466*amount-126,
                        objective=135*amount-23, half_area=600*amount-150)
        assert all(record[key] == value for key, value in expected.items())
        chains.append(dict(stars=amount, **record))
        if amount <= 4:
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                image = *shape, selected, matching
                direct_check(*image)
                assert set(occupied_degrees(image).values()) == {3}
                assert verify_terminal(image)['receivers'][0]['charge_twice'] == 2*(amount+1)
                assert frozen_certificate(image)[0] == {point for edge in matching for point in edge}
                images += 1
    witness, _ = chain(4)
    report = dict(status='PASS', rotor_phases=phases, stars=stars, chain_lengths=lengths,
                  chains=chains, tile_preserving_symmetry_images=images,
                  scope='Finite controls for separate all-length written proofs: original corrected '
                        'charge, physical feasibility, actual matching and module splice tree, '
                        'complete mixed-bundle freezing, distinct donors within one receiver. '
                        'Unbounded receiver charge refutes a charge ceiling, not compensation '
                        'or the unrestricted grid conjecture.',
                  charge_five_witness=dict(shape=witness[:2], selected=sorted(witness[2]),
                                           matching=witness[3]))
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', rotor_phases=len(phases), star_widths=len(stars),
                          chain_lengths=lengths, symmetry_images=images,
                          maximum_charge=chains[-1]['charge'], charge_five=chains[3])))


if __name__ == '__main__':
    main()
