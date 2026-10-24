"""Probe compensation routes on bent, capacity-two and branched frozen grids."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import physical
from check_elbow_sources import elbow
from check_exchange_terminal_nonunique import fixture, graft, matching_orders
from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
from check_promotion_cores import degree_four_patch, frozen_certificate, tight_diamond
from check_residual_corridors import direct_check, transformed
from degree_three_fusion import occupied_bands
from rotor_networks import chain, combine, rotor, star_modules, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def pad_image(current, symmetry, offset):
    shape, selected, matching = transformed(*current, *symmetry)
    move = lambda point: (point[0]+offset[0], point[1]+offset[1])
    return (2*((shape[0]+7)//2), 2*((shape[1]+7)//2),
            {move(point) for point in selected}, [tuple(map(move, edge)) for edge in matching])


def control(name, current, symmetry, offset, totals, records):
    current = pad_image(current, symmetry, offset)
    direct_check(*current)
    endpoints = {point for edge in current[3] for point in edge}
    if frozen_certificate(current)[0] != endpoints:
        totals['not_fully_frozen_excluded_'+name] += 1
        return
    result = physical(current, whole_bands(current), [], totals)
    totals['fully_frozen_frontier_models'] += 1
    totals['nonempty_compensation_models'] += result['value'] > 0
    totals['deficient_models'] += result['deficit'] > 0
    records.append(dict(family=name, symmetry=list(symmetry), offset=list(offset),
                        alpha=result['value']+result['deficit'], routed=result['value'],
                        deficit=result['deficit'], minimum_link_cost=result['cost'],
                        cut=result['cut'], blocked=result['blocked']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, records = Counter(), []
    base = fixture()
    fixtures = [('bent_nonunique_'+str(index), (*base[:3], list(record['matching'])))
                for index, record in enumerate(matching_orders())]
    fixtures += [('graft', graft(6, 4)), ('degree_four_control', degree_four_patch()),
                 ('diamond', tight_diamond()[0]), ('elbow', elbow(6, 4)),
                 ('occupied', occupied_bands(6)[0])]
    fixtures += [(name, stack(6, 4, [name])) for name in ('missing', 'collision', 'cycle')]
    module = rotor()
    fixtures.append(('capacity_two_rotor', (6, 6, module['selected'], module['matching'])))
    for width in (6, 10, 20):
        modules = [transform_module(module, (False, False, False), (width-2, width-2))
                   for module in star_modules(width)]
        network = combine(modules)
        fixtures.append(('branched_star_'+str(width),
                         (2*width+2, 2*width+2, network['selected'], network['matching'])))
    for (name, current), symmetry, offset in itertools.product(
            fixtures, itertools.product((False, True), repeat=3),
            itertools.product((2, 3), repeat=2)):
        control(name, current, symmetry, offset, totals, records)
    print(json.dumps(dict(stage='fixtures', totals=dict(totals)), sort_keys=True), flush=True)
    for amount, offset in itertools.product((1, 2, 4, 8), itertools.product((2, 3), repeat=2)):
        current, modules = chain(amount)
        control('branched_chain_'+str(amount), current, (False, False, False), offset, totals, records)
    assert totals['fully_frozen_frontier_models'] > 0
    assert totals['not_fully_frozen_excluded_degree_four_control'] == 32
    families = []
    for name in sorted({record['family'] for record in records}):
        images = [record for record in records if record['family'] == name]
        outcomes = Counter((record['alpha'], record['routed'], record['deficit'],
                            record['minimum_link_cost']) for record in images)
        families.append(dict(family=name, images=len(images),
                             nonempty=sum(record['alpha'] > 0 for record in images),
                             outcomes=[dict(alpha=key[0], routed=key[1], deficit=key[2],
                                            minimum_link_cost=key[3], count=value)
                                       for key, value in sorted(outcomes.items())]))
    record = dict(status='PASS', totals=dict(totals), families=families,
                  deficient_examples=[record for record in records if record['deficit']],
                  scope='Finite discovery with full feasibility/freezing checks and explicit '
                  'flow/cut certificates. Includes both actual matchings of the bent fixture, '
                  'capacity-two rotors, occupied bands and connected branched networks. '
                  'No universal geometric cut inequality is inferred from this finite sample.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
