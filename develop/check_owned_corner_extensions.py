"""Controls for three donor rules, distinct capacities and mixed-component ownership."""

import argparse
import itertools
import json
from pathlib import Path

from check_bent_cap_compensation import bent_cap
from check_charge_two_frozen_receiver import fixture as charge_two_fixture
from check_component_receivers import endpoint_components, verify_terminal
from check_corner_free_frozen_receiver import fixture as corner_free_fixture
from check_elbow_sources import elbow
from check_guarded_stepped_arms import stepped, transform
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from owned_corner_witnesses import physical_donors


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def stepped_case(parameter):
    source = transform(stepped(parameter), (False, False, False))
    margin = 2*parameter+12
    move = lambda point: (point[0]+margin, point[1]+margin)
    return (2*margin+4, 2*margin+4, {move(point) for point in source['selected']},
            [tuple(move(point) for point in edge) for edge in source['matching']])


def separated(sources):
    selected, matching = set(), []
    column_offset = 4
    for current in sources:
        move = lambda point: (point[0]+4, point[1]+column_offset)
        selected.update(move(point) for point in current[2])
        matching.extend(tuple(move(point) for point in edge) for edge in current[3])
        column_offset += current[1]+4
    return max(current[0] for current in sources)+8, column_offset+4, selected, matching


def inspect(current):
    direct_check(*current)
    endpoints = {point for edge in current[3] for point in edge}
    assert frozen_certificate(current)[0] == endpoints
    ledger = verify_terminal(current)
    records = physical_donors(current, include_endpoint_guard=True)
    assert len(records) == len({tuple(record['tile']) for record in records})
    owned = {index: sum(record['deficit'] for record in records if record['owner'] == index)
             for index in range(len(endpoint_components(current)))}
    for index, receiver in enumerate(ledger['receivers']):
        assert 2*owned[index] >= receiver['charge_twice']
    assert sum(owned.values()) <= ledger['empty_deficit']
    return dict(components=len(ledger['receivers']), donor_tiles=len(records),
                owned_capacity=sum(owned.values()),
                receiver_charge_twice=[record['charge_twice'] for record in ledger['receivers']])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    sources = [('corner_free', corner_free_fixture()[0]), ('charge_two', charge_two_fixture()[0]),
               ('bent', bent_cap(4)), ('elbow', elbow(6, 4))]
    sources += [('stepped_%d' % parameter, stepped_case(parameter)) for parameter in (1, 2, 4)]
    cases = []
    for name, current in sources:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            cases.append(dict(name=name, symmetry=symmetry, **inspect((*shape, selected, matching))))
    mixed = []
    for number in (2, 3, len(sources)):
        current = separated([source for _, source in sources[:number]])
        record = inspect(current)
        assert record['components'] == number
        mixed.append(record)
    report = dict(status='PASS', physical_symmetry_cases=len(cases),
                  mixed_component_controls=mixed, records=cases,
                  scope='Finite physical controls for the written same-component endpoint-guard '
                        'lemma and compatibility with capped and selected-guarded ownership. '
                        'No universal coverage theorem is inferred.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}))


if __name__ == '__main__':
    main()
