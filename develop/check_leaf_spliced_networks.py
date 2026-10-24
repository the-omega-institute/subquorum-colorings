"""Physical controls for the written all-length leaf-splice compensation proof."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_corner_extensions import separated
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_two_leg_corner_obstruction import saturated_endpoint_donors, two_leg_case
from local_quota_strip_allocation import local_quota_allocation
from sealed_strip_allocation import maximal_strips


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def module_record(selected, matching):
    endpoints = {point for edge in matching for point in edge}
    receiver = {tuple(coordinate//2 for coordinate in point) for point in endpoints}
    chosen = selected & vertices_of(receiver)
    return dict(endpoints=endpoints, receiver=receiver, selected=selected,
                matching=matching, receiver_selected=chosen,
                charge=len(chosen)+len(matching)-2*len(receiver))


def zigzag(amount):
    base, _ = two_leg_case(6, 4, 4)
    modules = []
    for index in range(amount):
        move = lambda point: (9-point[0] if index % 2 else point[0], point[1]+5*index)
        modules.append(module_record({move(point) for point in base[2]},
                                     [tuple(move(point) for point in edge) for edge in base[3]]))
    endpoints = set.union(*(module['endpoints'] for module in modules))
    selected = set.union(*(module['selected'] for module in modules))-endpoints
    matching = [edge for module in modules for edge in module['matching']]
    columns = 5*amount+3+(amount % 2 == 0)
    return (10, columns, selected, matching), modules


def inspect(current, modules):
    objective = direct_check(*current)
    endpoints = {point for edge in current[3] for point in edge}
    assert sum(len(module['endpoints']) for module in modules) == len(endpoints)
    assert len(endpoint_components(current)) == 1
    assert set(occupied_degrees(current).values()) == {3}
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    contacts = {tuple(sorted((point, other))) for point in endpoints
                for other in set(neighbors(point)) & endpoints if owners[point] != owners[other]}
    module_edges = Counter(tuple(sorted((owners[first], owners[second])))
                           for first, second in contacts)
    assert set(module_edges.values()) <= {1}
    assert set(module_edges) == {(index, index+1) for index in range(len(modules)-1)}
    intratile = sum(tuple(coordinate//2 for coordinate in first) ==
                    tuple(coordinate//2 for coordinate in second) for first, second in contacts)
    receiver = set.union(*(module['receiver'] for module in modules))
    selected_in = len(vertices_of(receiver) & current[2])
    assert len(receiver) == sum(len(module['receiver']) for module in modules)-intratile
    assert selected_in == sum(len(module['receiver_selected']) for module in modules)-2*intratile
    ledger = verify_terminal(current)
    charge = sum(module['charge'] for module in modules)
    assert ledger['receivers'][0]['charge_twice'] == 2*charge
    assert charge <= len(modules) % 2
    assert all(modules[index]['charge']+modules[index+1]['charge'] <= 0
               for index in range(len(modules)-1))
    for tile in receiver:
        cells = vertices_of({tile})
        assert all(set(neighbors(chosen)) & cells & endpoints for chosen in cells & current[2])
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    donors = saturated_endpoint_donors(current)
    if charge > 0:
        assert donors and all(donor['deficit'] == 1 and donor['owner'] == 0 for donor in donors)
    assert 2*len(donors) >= ledger['receivers'][0]['charge_twice']
    assert objective <= current[0]*current[1]//2
    return dict(modules=len(modules), endpoints=len(endpoints), selected=len(current[2]),
                matching_edges=len(current[3]), intratile_splices=intratile,
                intertile_splices=len(contacts)-intratile, charge=charge,
                isolated_charges=[module['charge'] for module in modules],
                receiver_tiles=len(receiver), receiver_selected=selected_in,
                objective=objective, half_area=current[0]*current[1]//2,
                frozen_endpoints=len(frozen), freezing_layers=len(layers),
                distinct_unit_donors=len(donors))


def phase_controls():
    cases = 0
    for width, left, right in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8)):
        base, _ = two_leg_case(width, left, right)
        half_sum = (left+right)//2
        for row_phase, column_phase in itertools.product(range(2), repeat=2):
            move = lambda point: (point[0]+row_phase, point[1]+column_phase)
            current = base[0]+2, base[1]+2, {move(point) for point in base[2]}, [
                tuple(move(point) for point in edge) for edge in base[3]]
            receiver = verify_terminal(current)['receivers'][0]
            expected_tiles = ((width//2+half_sum+1, width//2+half_sum),
                              (width+half_sum, width+half_sum-2))[row_phase][column_phase]
            expected_selected = ((half_sum+4, half_sum),
                                 (half_sum+2, half_sum-2))[row_phase][column_phase]
            expected_charge = (1 if column_phase == 0 else -1) if row_phase == 0 else 1-width
            assert receiver['tiles'] == expected_tiles
            assert receiver['selected'] == expected_selected
            assert receiver['charge_twice'] == 2*expected_charge
            if expected_charge > 0:
                endpoints = {point for edge in current[3] for point in edge}
                for point in endpoints:
                    if len(set(neighbors(point)) & endpoints) == 1:
                        cells = vertices_of({tuple(coordinate//2 for coordinate in point)})
                        assert len(cells & current[2]) == 2
                        assert len(cells & endpoints) == 1
            cases += 1
    return cases


def locality_controls():
    tested = 0
    valid = 0
    for labels in itertools.product(range(3), repeat=4):
        adjacent = {index: {index ^ 1, index ^ 2} for index in range(4)}
        for exterior in itertools.product(range(3), repeat=4):
            tested += 1
            degrees = {index: exterior[index]+sum(labels[other] != 0 for other in adjacent[index])
                       for index in range(4)}
            if any(labels[index] == 1 and degrees[index] > 1 or
                   labels[index] == 2 and degrees[index] < 3 for index in range(4)):
                continue
            valid += 1
            if 2 in labels:
                assert all(any(labels[other] == 2 for other in adjacent[index])
                           for index in range(4) if labels[index] == 1)
    return dict(cases=tested, feasible_terminal=valid)


def reservation_controls():
    physical = separated([zigzag(1)[0] for _ in range(7)])
    ledger = verify_terminal(physical)
    charge = sum(receiver['charge_twice'] for receiver in ledger['receivers'])//2
    assert charge == 7
    chosen = {}
    for donor in saturated_endpoint_donors(physical):
        chosen.setdefault(donor['owner'], tuple(donor['tile']))
    assert len(chosen) == len(set(chosen.values())) == 7
    tiles = list(chosen.values())
    checked = 0
    first_five = 0
    matching_controls = 0
    for mask in range(1 << len(tiles)):
        reserved = {tile: 1 for index, tile in enumerate(tiles) if mask >> index & 1}
        records, _, residual = maximal_strips(physical, reserved)
        remaining = set(tiles)-set(reserved)
        residual_charge = charge-len(reserved)
        assert len(remaining) >= residual_charge
        assert all(residual[tile] == 1 for tile in remaining)
        if residual_charge <= 5:
            assert sum(capacity > 0 for capacity in residual.values()) >= residual_charge
            first_five += 1
            if mask == 3:
                allocated = local_quota_allocation(records, residual)
                assert allocated['credits'] >= residual_charge == 5
                matching_controls += 1
        checked += 1
    return dict(physical_reservation_subsets=checked, residual_charge_at_most_five=first_five,
                original_charge=charge, positive_networks=7, exact_q5_matching_controls=matching_controls,
                note='Reservations consume genuine donor units; nonzero-B q5 cases included. '
                     'General arbitrary-slot proof is the distinct-unit deletion argument.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    phase_cases = phase_controls()
    locality = locality_controls()
    reservations = reservation_controls()
    lengths = list(range(1, 17))+[24, 33, 64]
    records = []
    images = 0
    phase_splices = 0
    for amount in lengths:
        current, modules = zigzag(amount)
        record = inspect(current, modules)
        assert record['charge'] == amount % 2
        assert record['endpoints'] == 18*amount
        assert record['selected'] == 8*amount+2
        assert record['matching_edges'] == 9*amount
        assert record['intratile_splices'] == amount-1
        for row_phase, column_phase in itertools.product(range(2), repeat=2):
            move = lambda point: (point[0]+row_phase, point[1]+column_phase)
            phased = current[0]+2, current[1]+2, {move(point) for point in current[2]}, [
                tuple(move(point) for point in edge) for edge in current[3]]
            phased_modules = [module_record({move(point) for point in module['selected']}, [
                tuple(move(point) for point in edge) for edge in module['matching']])
                for module in modules]
            phased_record = inspect(phased, phased_modules)
            assert phased_record['intratile_splices'] == (0 if row_phase else amount-1)
            phase_splices += 1
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            physical = *shape, selected, matching
            direct_check(*physical)
            assert verify_terminal(physical)['receivers'][0]['charge_twice'] == 2*(amount % 2)
            assert frozen_certificate(physical)[0] == {point for edge in matching for point in edge}
            if amount % 2:
                assert saturated_endpoint_donors(physical)
            images += 1
        records.append(record)
    combined = separated([zigzag(amount)[0] for amount in (1, 3, 5, 4)])
    ledger = verify_terminal(combined)
    assert len(ledger['receivers']) == 4
    donors = saturated_endpoint_donors(combined)
    assigned = {}
    for donor in donors:
        tile = tuple(donor['tile'])
        assert assigned.setdefault(tile, donor['owner']) == donor['owner']
    capacities = Counter(assigned.values())
    assert all(2*capacities[owner] >= receiver['charge_twice']
               for owner, receiver in enumerate(ledger['receivers']))
    base, modules = zigzag(3)
    report = dict(status='PASS', phase_cases=phase_cases, path_lengths=lengths,
                  symmetry_images=images, phase_splice_cases=phase_splices,
                  receiver_locality_controls=locality, separated_network_components=4,
                  reservation_controls=reservations,
                  separated_positive_components=3,
                  scope='Finite controls for the separate all-length geometric proof; '
                        'phase counts, actual matching, exact corrected splice ledger, '
                        'all-endpoint freezing and distinct physical unit donors. '
                        'No universal grid coverage or unrestricted coefficient improvement.',
                  paths=records,
                  sharp_three_module_example=dict(shape=base[:2], selected=sorted(base[2]),
                      matching=base[3], checked=inspect(base, modules)))
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ['paths', 'sharp_three_module_example']}))


if __name__ == '__main__':
    main()
