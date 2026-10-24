"""Local capacities and complete-source controls for singleton-flow cancellation."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import boundary, inspect_slots, tile_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_minus_one_joint_compensation import marked_gate_modules
from check_minus_one_tip_obstructions import overloaded_tile_modules, two_tip_modules
from check_regular_tile_compensation import inspect
from check_zero_credit_tip_family import family
from degree_four_overcount import opposed_bands
from degree_three_fusion import four_way_modules, occupied_bands
from rotor_networks import chain_modules, rotor, star_modules, transform_module
from singleton_negative_defects import inspect_local, packings, profiles


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def local_controls():
    catalogue = profiles()
    checked = []
    blank_gate_cases = 0
    for packing in packings(catalogue):
        report = inspect_local(catalogue, packing)
        if report is None:
            continue
        current = [catalogue[index] for index in packing]
        endpoints = set(report['endpoints'])
        activated = sum(len(profile['endpoints']) == 1 and len(profile['selected']) == 2
                        and bool(profile['selected'] & endpoints) for profile in current)
        forwarding = int(len(endpoints) == 4 and activated == 1 and
                         any(len(profile['endpoints']) == 3 for profile in current))
        remainder = report['irregular_slots']+report['exceptional_three']-2*(
            report['irregular']-report['correction'])
        assert activated <= remainder+forwarding
        blank_gate = 0 not in endpoints | set(report['selected']) and any(
            profile['negative'] and profile['endpoints'] in ({1, 3}, {2, 3}) and
            len(profile['selected']) <= 1 and profile['selected'] <= endpoints
            for profile in current)
        if blank_gate:
            blank_gate_cases += 1
            assert activated == forwarding == 0 and remainder >= 1
        checked.append(dict(activated=activated, forwarding=forwarding,
                            remainder=remainder, endpoint_count=len(endpoints)))
    assert blank_gate_cases > 0
    return checked, blank_gate_cases


def rotor_pairs(module):
    singletons = {}
    triples = {}
    for tile in module['receiver']:
        cells = vertices_of({tile})
        profile = len(cells & module['endpoints']), len(cells & module['selected'])
        if profile == (1, 2):
            singletons[tile] = cells & module['endpoints']
        elif profile == (3, 0):
            triples[tile] = next(iter(cells-module['endpoints']))
    if not triples:
        return {}
    assert len(singletons) == len(triples) == 2
    result = {}
    for triple, missing in triples.items():
        candidates = [(singleton, support) for singleton, endpoints in singletons.items()
                      for support in module['selected'] & set(neighbors(missing))
                      if support in vertices_of({singleton}) and
                      endpoints <= set(neighbors(support))]
        assert len(candidates) == 1
        result[triple] = candidates[0]
    assert len({singleton for singleton, _ in result.values()}) == 2
    return result


def inspect_budget(current, modules):
    physical = inspect(current, modules, require_frozen=False)
    slots = inspect_slots(current, modules)
    endpoints = set.union(*(module['endpoints'] for module in modules))
    regular = Counter()
    irregular = Counter()
    for module in modules:
        original = module['endpoints'] | module['selected']
        candidates = boundary(module)[2]
        for point in module['endpoints']:
            for other in (set(neighbors(point)) & endpoints)-original:
                if tile_of(point) == tile_of(other):
                    (irregular if point in candidates else regular)[tile_of(point)] += 1
    represented = set.union(*(module['receiver'] for module in modules))
    blank_marks = {tuple(record['tile']) for record in slots['marked_assignments']
                   if record['kind'] == 'blank_gate'}
    assert len(blank_marks) == sum(record['kind'] == 'blank_gate'
                                 for record in slots['marked_assignments'])
    activated = set()
    remainder_sum = exceptional_u = exceptional_r = forwarding_u = forwarding_r = 0
    diagonal = sum(module['charge'] <= -5 and any(
        len(vertices_of({tile}) & module['endpoints']) == 3 for tile in module['receiver'])
        for module in modules)
    for tile in represented:
        cells = vertices_of({tile})
        originals = [(index, cells & module['endpoints'], cells & module['selected'])
                     for index, module in enumerate(modules) if tile in module['receiver']]
        local_activated = {(index, tile) for index, own, support in originals
                           if len(own) == 1 and len(support) == 2 and support & endpoints}
        activated |= local_activated
        triple = [index for index, own, _ in originals if len(own) == 3]
        irregular_singleton = any(len(own) == len(support) == 1
                                 for _, own, support in originals)
        exceptional = int(cells <= endpoints and bool(triple) and irregular_singleton)
        forwarding = int(cells <= endpoints and bool(triple) and bool(local_activated))
        assert not (exceptional and forwarding)
        if exceptional or forwarding:
            assert len(triple) == 1
            owner = modules[triple[0]]
            is_rotor = len(owner['endpoints']) == 8
            if is_rotor:
                assert owner['charge'] == 0
                exceptional_r += exceptional
                forwarding_r += forwarding
            else:
                assert owner['charge'] <= -5
                exceptional_u += exceptional
                forwarding_u += forwarding
        new_full = cells <= endpoints and not any(cells <= own for _, own, _ in originals)
        credit = 2*int(new_full)-regular[tile]
        local_slots = sum(len(cells & boundary(modules[index])[2])
                          for index, _, _ in originals)
        remainder = local_slots+exceptional-2*(irregular[tile]-credit)
        assert remainder >= 0
        if tile in blank_marks:
            assert not local_activated and not forwarding and not cells <= endpoints
            assert remainder >= 1
        assert len(local_activated)+int(tile in blank_marks) <= remainder+forwarding
        remainder_sum += remainder
    rotor_activated = {(index, tile) for index, tile in activated
                       if len(modules[index]['endpoints']) == 8}
    positive_activated = {(index, tile) for index, tile in activated
                          if modules[index]['charge'] == 1}
    assert rotor_activated.isdisjoint(positive_activated)
    bridge_targets = set()
    filled_triples = 0
    for index, module in enumerate(modules):
        if len(module['endpoints']) != 8:
            if module['charge'] == 1:
                assert sum(len(vertices_of({tile}) & module['endpoints']) == 1
                           for tile in module['receiver']) == 2
            continue
        for triple, (singleton, support) in rotor_pairs(module).items():
            if vertices_of({triple}) <= endpoints:
                assert support in endpoints and (index, singleton) in rotor_activated
                assert (index, singleton) not in bridge_targets
                bridge_targets.add((index, singleton))
                filled_triples += 1
    assert filled_triples == exceptional_r+forwarding_r
    assert exceptional_r+forwarding_r <= len(rotor_activated)
    assert exceptional_r+forwarding_r+len(positive_activated) <= len(activated)
    assert exceptional_u+forwarding_u <= 2*diagonal
    assert len(activated)+len(blank_marks) <= remainder_sum+forwarding_u+forwarding_r
    margin = 2*diagonal+remainder_sum-exceptional_u-exceptional_r
    assert len(positive_activated)+len(blank_marks) <= margin
    reserve = slots['negative_mass']+physical['residual_square_credit']-slots['irregular_events']
    assert 2*reserve == margin and reserve >= 0
    assert 2*reserve >= len(positive_activated)+len(blank_marks)
    return dict(positive=slots['positive'], marked=slots['marked_sides'],
                positive_activated=len(positive_activated), blank_marks=len(blank_marks),
                activated=len(activated), rotor_activated=len(rotor_activated),
                exceptional_u=exceptional_u, exceptional_r=exceptional_r,
                forwarding_u=forwarding_u, forwarding_r=forwarding_r,
                diagonal_u=diagonal, remainder=remainder_sum, event_reserve=reserve,
                guaranteed_slack=slots['positive']-slots['marked_sides']+
                                 (len(positive_activated)+len(blank_marks)+1)//2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    local, blank_gate_cases = local_controls()
    rotor_images = 0
    for symmetry in itertools.product((False, True), repeat=3):
        for phase in itertools.product(range(2), repeat=2):
            rotor_pairs(transform_module(rotor(), symmetry, phase))
            rotor_images += 1
    fixtures = [('marked_gate', marked_gate_modules()), ('two_tips', two_tip_modules()),
                ('overloaded', overloaded_tile_modules()), ('zero_credit', family()), ('rotor', [rotor()])]
    fixtures += [('four_way_%d' % width, four_way_modules(width)) for width in (8, 14)]
    fixtures += [('star_%d' % width, star_modules(width)) for width in (6, 14)]
    fixtures += [('chain_%d' % amount, chain_modules(amount)) for amount in (1, 2, 3)]
    for width in (6, 8, 14, 40):
        fixtures.append(('opposed_%d' % width, opposed_bands(width, 4)[1]))
        fixtures.append(('occupied_%d' % width, occupied_bands(width)[1]))
    controls = []
    for name, modules in fixtures:
        for symmetry, phase, _, current, moved in phase_images(modules):
            controls.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_budget(current, moved)))
    summary = dict(local_packings=len(local), local_blank_gate_cases=blank_gate_cases,
                   rotor_images=rotor_images,
                   physical_images=len(controls),
                   positive_activation_images=sum(record['positive_activated'] > 0 for record in controls),
                   blank_gate_images=sum(record['blank_marks'] > 0 for record in controls),
                   exceptional_rotor_images=sum(record['exceptional_r'] > 0 for record in controls),
                   forwarding_rotor_images=sum(record['forwarding_r'] > 0 for record in controls))
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary, local=local,
        physical=controls, scope='Local catalogue and complete physical controls. The arbitrary finite fusion proof uses written source normalization, local classification, rotor pairing and cancellation; finite controls alone do not prove it. The unrestricted occupied-gate allocation and grid equality remain open.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
