"""Physical controls for an unbounded degree-three obstruction to three-rule coverage."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_owned_corner_extensions import separated, stepped_case
from check_charge_two_frozen_receiver import fixture as charge_two_fixture
from check_corner_free_frozen_receiver import fixture as corner_free_fixture
from check_three_rule_obstruction import fixture as three_rule_fixture
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed
from owned_corner_witnesses import physical_donors


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def two_leg_case(width, left_height, right_height):
    assert width >= 6 and width % 2 == 0
    assert min(left_height, right_height) >= 4
    assert left_height % 2 == right_height % 2 == 0
    selected = set()
    matching = [((0, column), (0, column+1)) for column in range(1, width, 2)]
    matching += [((1, column), (1, column+1)) for column in range(2, width-1, 2)]
    certificate = []
    for column, exterior, interior, height in (
            (1, 0, 2, left_height), (width, width+1, width-1, right_height)):
        selected.add((0, exterior))
        selected.add((height+1, column))
        selected.update((row, exterior if row % 2 == 0 else interior)
                        for row in range(2, height+1))
        matching += [((row, column), (row+1, column)) for row in range(1, height, 2)]
        for row in range(height, 1, -2):
            certificate.append(((row, column), (row, exterior), (row+1, column)))
    certificate.append(((0, 1), (0, 0), (1, 1)))
    for column in range(2, width):
        row = 1 if column % 2 == 0 else 0
        certificate.append(((row, column), (1-row, column), (row, column-1)))
    certificate.append(((0, width), (0, width+1), (1, width)))
    for column in range(width-1, 1, -1):
        row = (width-column) % 2
        certificate.append(((row, column), (1-row, column), (row, column+1)))
    for column, interior, height in ((1, 2, left_height), (width, width-1, right_height)):
        certificate.append(((1, column), (0, column), (1, interior)))
        for row in range(3, height, 2):
            certificate.append(((row, column), (row, interior), (row-1, column)))
    return (max(left_height, right_height)+2, width+2, selected, matching), certificate


def saturated_endpoint_donors(current):
    rows, columns, selected, _ = current
    components = endpoint_components(current)
    owner = {point: index for index, component in enumerate(components) for point in component}
    endpoints = set(owner)
    degrees = occupied_degrees(current)
    result = []
    for tile in itertools.product(range(rows//2), range(columns//2)):
        cells = vertices_of({tile})
        for chosen in sorted(cells & selected):
            anchors = (set(neighbors(chosen))-cells) & endpoints
            opposite = tuple(4*coordinate+1-value for coordinate, value in zip(tile, chosen))
            guards = (set(neighbors(opposite))-cells) & endpoints
            for anchor, guard in itertools.product(sorted(anchors), sorted(guards)):
                if owner[anchor] != owner[guard] or degrees[guard] != 3:
                    continue
                if len(set(neighbors(guard)) & endpoints) != 3:
                    continue
                assert not cells & endpoints and len(cells & selected) == 1
                result.append(dict(tile=tile, selected=chosen, anchor=anchor, guard=guard,
                                   owner=owner[anchor], deficit=1))
    return result


def inspect(current, certificate=None):
    endpoints = endpoint_data(current)[0]
    assert endpoint_components(current) == [endpoints]
    assert set(occupied_degrees(current).values()) == {3}
    assert all(len(set(neighbors(point)) & endpoints) == 1 for point in current[2])
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    if certificate is not None:
        mates = {point: partner for edge in current[3] for point, partner in (edge, edge[::-1])}
        earlier = set()
        for vertex, first, second in certificate:
            assert vertex in endpoints-earlier and first != second
            assert {first, second} <= set(neighbors(vertex))
            assert mates[vertex] not in {first, second}
            assert all(point in current[2] or point in mates and mates[point] in earlier
                       for point in (first, second))
            earlier.add(vertex)
        assert earlier == endpoints
    ledger = verify_terminal(current)
    assert ledger['receivers'][0]['charge_twice'] == 2
    assert physical_donors(current, include_endpoint_guard=True) == []
    donors = saturated_endpoint_donors(current)
    assert len(donors) == len({tuple(record['tile']) for record in donors}) == 2
    return dict(endpoints=len(endpoints), selected=len(current[2]), matching_edges=len(current[3]),
                receiver=ledger['receivers'][0], no_endpoint_deficit=ledger['empty_deficit'],
                objective=ledger['objective'], area=ledger['area'],
                freezing_layer_sizes=[len(layer) for layer in layers],
                three_rule_capacity=0, saturated_endpoint_donors=donors)


def mixed_ownership_control(current):
    ledger = verify_terminal(current)
    records = physical_donors(current, include_endpoint_guard=True)
    records += saturated_endpoint_donors(current)
    assigned = {}
    for record in records:
        tile = tuple(record['tile'])
        if tile in assigned:
            assert assigned[tile] == (record['owner'], record['deficit'])
        assigned[tile] = record['owner'], record['deficit']
    capacities = [sum(deficit for owner, deficit in assigned.values() if owner == index)
                  for index in range(len(ledger['receivers']))]
    assert all(2*capacity >= receiver['charge_twice']
               for capacity, receiver in zip(capacities, ledger['receivers']))
    assert sum(capacities) <= ledger['empty_deficit']
    return dict(components=len(capacities), descriptions=len(records),
                distinct_physical_tiles=len(assigned), owned_capacities=capacities)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = list(itertools.product((6, 8, 10, 14), (4, 6, 10), (4, 8, 12)))
    parameters += [(40, 40, 4), (40, 4, 40), (64, 40, 40)]
    records = []
    symmetry_checks = 0
    for width, left_height, right_height in parameters:
        current, certificate = two_leg_case(width, left_height, right_height)
        checked = inspect(current, certificate)
        half_sum = (left_height+right_height)//2
        assert checked['endpoints'] == 2*(width+half_sum-1)
        assert checked['selected'] == 2*half_sum+2
        assert checked['matching_edges'] == width+half_sum-1
        assert checked['receiver']['tiles'] == width//2+1+half_sum
        assert checked['receiver']['selected'] == half_sum+4
        assert checked['objective'] == width+3*half_sum+1
        for padding in (0, 2):
            move = lambda point: (point[0]+padding, point[1]+padding)
            padded = (current[0]+2*padding, current[1]+2*padding,
                      {move(point) for point in current[2]},
                      [tuple(move(point) for point in edge) for edge in current[3]])
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*padded, *symmetry)
                inspect((*shape, selected, matching))
                symmetry_checks += 1
        records.append(dict(width=width, left_height=left_height, right_height=right_height,
                            **checked))
    mixed_sources = [two_leg_case(6, 4, 4)[0], charge_two_fixture()[0],
                     corner_free_fixture()[0], stepped_case(1)]
    mixed_controls = []
    for number in (2, 3, 4):
        current = separated(mixed_sources[:number])
        checked = mixed_ownership_control(current)
        assert checked['components'] == number
        mixed_controls.append(checked)
    fixture = json.loads(Path(__file__).with_name('two_leg_degree_three_obstruction.json').read_text())
    base, certificate = two_leg_case(6, 4, 4)
    assert fixture['shape'] == list(base[:2])
    assert {tuple(point) for point in fixture['selected']} == base[2]
    assert fixture['matching'] == json.loads(json.dumps(base[3]))
    assert fixture['freezing_certificate'] == json.loads(json.dumps(certificate))
    previous_obstruction = three_rule_fixture()[0]
    assert physical_donors(previous_obstruction, include_endpoint_guard=True) == []
    assert saturated_endpoint_donors(previous_obstruction) == []
    report = dict(status='PASS', parameter_cases=len(records), symmetry_checks=symmetry_checks,
                  mixed_ownership_controls=mixed_controls,
                  previous_22_endpoint_four_rule_capacity=0,
                  scope='Physical controls for the written all-even-parameter two-leg theorem. '
                        'Exact degree three, complete ordered mixed-bundle exclusion certificates, '
                        'original corrected charge one, zero capacity for all three old rules, '
                        'and two distinct saturated-endpoint unit donors. Finite controls do not '
                        'replace the general proof. The previous 22-endpoint example also defeats '
                        'the fourth rule in general; four-rule degree-three coverage remains open.',
                  cases=records)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'cases'}))


if __name__ == '__main__':
    main()
