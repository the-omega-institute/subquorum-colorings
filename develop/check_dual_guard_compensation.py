"""Physical controls for the two-guard compensation theorem and witness disjointness."""

import argparse
import itertools
import json
from pathlib import Path

from check_degree_three_fusion import phase_images
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import occupied_degrees
from check_promotion_cores import frozen_certificate
from degree_four_overcount import opposed_bands
from degree_three_fusion import corner_join, four_way, occupied_bands
from dual_guard_compensation import inspect as inspect_dual, paired_guards
from rotor_networks import chain, combine, star_modules, transform_module, two_leg_module
from discover_fusion_compensation_obstructions import raw_budget, supported_modules


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, modules):
    result = inspect_dual(current, modules)
    raw = raw_budget(modules)
    for raw_key, physical_key in [('negative_mass', 'negative_module_mass'),
                                  ('degree_four', 'degree_four_endpoints'),
                                  ('squares', 'new_aligned_faces'),
                                  ('inside', 'intratile_degree_four_defect'),
                                  ('marked', 'marked_positive_modules'),
                                  ('fine_credit', 'certified_slack_lower_bound')]:
        assert raw[raw_key] == result[physical_key]
    return result


def external_charge_control():
    covered = [transform_module(two_leg_module(6, 4), (False, False, False), offset)
               for offset in [(0, 0), (0, 12)]]
    external = combine([transform_module(module, (False, False, False), (16, 16))
                        for module in star_modules(6)])
    modules = covered+[external]
    network = combine(modules)
    current = (32, 32, network['selected'], network['matching'])
    assert [module['charge'] for module in modules] == [1, 1, 2]
    assert len(endpoint_components(current)) == 3
    assert set(occupied_degrees(current).values()) == {3}
    assert frozen_certificate(current)[0] == network['endpoints']
    ledger = verify_terminal(current)
    assert sum(receiver['charge_twice'] for receiver in ledger['receivers']) == 8
    donated = []
    demands = ['covered0_own_charge', 'external_charge_unit0',
               'covered1_own_charge', 'external_charge_unit1']
    for module in covered:
        for selected, anchor, opposite, guard in paired_guards(module):
            tile = tuple(coordinate//2 for coordinate in selected)
            cells = vertices_of({tile})
            assert not cells & network['endpoints'] and cells & current[2] == {selected}
            donated.append(dict(tile=tile, selected=selected, demand=demands[len(donated)], capacity=1))
    assert len({tuple(record['tile']) for record in donated}) == 4
    assert ledger['empty_deficit'] >= len(donated) == 4
    assert ledger['objective'] <= current[0]*current[1]//2
    return dict(status='PASS', endpoint_components=3, original_charges=[1, 1, 2],
                covered_positive_modules=2, external_charge=2,
                four_distinct_unit_assignments=donated, physical=ledger,
                scope='Global closed-receiver counting only; no receiver-labelled adjacency or flow claim. No donor of the external charge-two component is used.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    images = []
    for spec, module in supported_modules():
        if spec['kind'] != 'two_leg':
            continue
        current = (max(spec['left'], spec['right'])+2, spec['width']+2,
                   module['selected'], module['matching'])
        record = inspect(current, [module])
        assert record['two_guard_unit_donors'] == 2
        assert record['two_guard_credit'] == 1
        records.append(dict(kind='asymmetric_single', parameters=spec, **record))
    for width in (8, 10, 14, 20):
        current, modules = four_way(width)
        record = inspect(current, modules)
        assert record['two_guard_unit_donors'] == 8
        assert record['two_guard_credit'] == 6
        assert record['improvement'] == 4
        records.append(dict(kind='four_way', width=width, **record))
    for width in (6, 8, 14, 40):
        current, modules = occupied_bands(width)
        record = inspect(current, modules)
        assert record['marked_sides'] == 0
        assert record['two_guard_unit_donors'] == 2
        assert record['two_guard_credit'] == width
        records.append(dict(kind='occupied_bands', width=width, **record))
        current, modules = corner_join(width)
        records.append(dict(kind='corner_join', width=width, **inspect(current, modules)))
        modules = [transform_module(module, (False, False, False), (width+2, width+2))
                   for module in star_modules(width)]
        network = combine(modules)
        rows = 2*(max(point[0] for point in network['endpoints'] | network['selected'])//2+1)
        columns = 2*(max(point[1] for point in network['endpoints'] | network['selected'])//2+1)
        record = inspect((rows, columns, network['selected'], network['matching']), modules)
        assert record['two_guard_unit_donors'] == 8
        assert record['two_guard_credit'] == 6
        records.append(dict(kind='rotor_star', width=width, **record))
    for width, height in itertools.product((6, 8, 14), (4, 8, 20)):
        current, modules = opposed_bands(width, height)
        record = inspect(current, modules)
        assert record['marked_sides'] == 2
        assert record['two_guard_credit'] == width-2
        records.append(dict(kind='opposed_bands', width=width, height=height, **record))
        for symmetry, phase, offset, current_image, moved in phase_images(modules):
            images.append(dict(kind='opposed_bands', width=width, height=height,
                               symmetry=symmetry, phase=phase, **inspect(current_image, moved)))
    for amount in (1, 2, 3, 4, 8):
        current, modules = chain(amount)
        record = inspect(current, modules)
        assert record['two_guard_unit_donors'] == 8*amount
        assert record['two_guard_credit'] == 7*amount-1
        records.append(dict(kind='rotor_chain', amount=amount, **record))
    result = dict(status='PASS', controls=records, images=images, external_charge_control=external_charge_control(),
                  scope='Independent physical donor/witness checks; general injection and budget theorem has a separate written proof.',
                  summary=dict(controls=len(records), images=len(images),
                               strict_improvements=sum(record['improvement'] > 0 for record in records),
                               image_strict_improvements=sum(record['improvement'] > 0 for record in images)))
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
