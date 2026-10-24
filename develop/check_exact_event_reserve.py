"""Exact geometric reserve and saturation controls for complete source fusions."""

import argparse
from collections import Counter
import json
from pathlib import Path

import check_activated_singleton_budget as previous
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from singleton_negative_defects import inspect_local, packings, profiles


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def local_controls():
    catalogue = profiles()
    result = []
    for packing in packings(catalogue):
        report = inspect_local(catalogue, packing)
        if report is None:
            continue
        current = [catalogue[index] for index in packing]
        endpoints = set(report['endpoints'])
        kinds = [(len(profile['endpoints']), len(profile['selected'])) for profile in current]
        activated = sum(kind == (1, 2) and bool(profile['selected'] & endpoints)
                        for kind, profile in zip(kinds, current))
        forwarding = int(len(endpoints) == 4 and activated == 1 and
                         any(kind[0] == 3 for kind in kinds))
        remainder = report['irregular_slots']+report['exceptional_three']-2*(
            report['irregular']-report['correction'])
        lone = int(len(endpoints) == 1 and kinds == [(1, 1)])
        bar = int(len(endpoints) == 2 and kinds == [(2, 0)])
        mutual = int(len(endpoints) == 2 and kinds == [(1, 1), (1, 1)] and
                     report['irregular'] == 0)
        mixed = int(len(endpoints) == 3 and len(current) > 1)
        cost = lone+2*bar+2*mutual+mixed
        assert remainder+forwarding-activated == cost
        result.append(dict(endpoints=len(endpoints), owners=len(current), lone=lone, bar=bar,
                           mutual=mutual, mixed=mixed, boundary_cost=cost))
    return result


def inspect_exact(current, modules):
    report = previous.inspect_budget(current, modules)
    endpoints = set.union(*(module['endpoints'] for module in modules))
    represented = set.union(*(module['receiver'] for module in modules))
    lone = bar = mutual = mixed = 0
    for tile in represented:
        cells = vertices_of({tile})
        originals = [module for module in modules if tile in module['receiver']]
        kinds = [(len(cells & module['endpoints']), len(cells & module['selected']))
                 for module in originals]
        size = len(cells & endpoints)
        lone += int(size == 1 and kinds == [(1, 1)])
        bar += int(size == 2 and kinds == [(2, 0)])
        if size == 2 and kinds == [(1, 1), (1, 1)]:
            events = sum(len((set(neighbors(point)) & cells & endpoints)-
                             module['endpoints']-module['selected'])
                         for module in originals for point in cells & module['endpoints'])
            assert events in (0, 1)
            mutual += int(events == 0)
        mixed += int(size == 3 and len(originals) > 1)
    unused_u = unpaired_rotor = 0
    for module in modules:
        if len(module['endpoints']) == 8:
            for triple, (singleton, _) in previous.rotor_pairs(module).items():
                support = vertices_of({singleton}) & module['selected']
                unpaired_rotor += int(bool(support & endpoints) and
                                      not vertices_of({triple}) <= endpoints)
        else:
            for tile in module['receiver']:
                cells = vertices_of({tile})
                if len(cells & module['endpoints']) == 3:
                    assert module['charge'] <= -5
                    unused_u += int(not cells <= endpoints)
    assert report['activated'] == report['positive_activated']+report['rotor_activated']
    assert unused_u == 2*report['diagonal_u']-report['exceptional_u']-report['forwarding_u']
    assert unpaired_rotor == report['rotor_activated']-report['exceptional_r']-report['forwarding_r']
    boundary = lone+2*bar+2*mutual+mixed
    assert boundary == (report['remainder']+report['forwarding_u']+report['forwarding_r']-
                        report['activated'])
    total = report['positive_activated']+unused_u+unpaired_rotor+boundary
    assert total == 2*report['event_reserve'] and total % 2 == 0
    joint_margin = report['positive']+report['event_reserve']-report['marked']
    assert (joint_margin >= 0) == (2*report['marked'] <= 2*report['positive']+total)
    assert (joint_margin < 0) == (total <= 2*report['marked']-2*report['positive']-2)
    if report['positive'] == 1 and total > 0:
        assert joint_margin >= 0
    if report['positive'] == 1 and joint_margin < 0:
        assert report['marked'] == 2 and total == 0
    assert (report['event_reserve'] == 0) == (total == 0)
    if report['event_reserve'] == 0:
        assert report['blank_marks'] == 0
        assert not any([report['positive_activated'], unused_u, unpaired_rotor,
                        lone, bar, mutual, mixed])
    return dict(positive=report['positive'], marked=report['marked'],
                activated_positive=report['positive_activated'], unused_u_triples=unused_u,
                unpaired_rotor_activation=unpaired_rotor, lone_irregular=lone,
                sole_irregular_pair=bar, mutual_non_event=mutual, mixed_three=mixed,
                boundary_cost=boundary, event_reserve=report['event_reserve'],
                exact_joint_margin=joint_margin)


def fixtures():
    result = [('marked_gate', previous.marked_gate_modules()), ('two_tips', previous.two_tip_modules()),
              ('overloaded', previous.overloaded_tile_modules()), ('zero_credit', previous.family()),
              ('rotor', [previous.rotor()])]
    result += [('four_way_%d' % width, previous.four_way_modules(width)) for width in (8, 14)]
    result += [('star_%d' % width, previous.star_modules(width)) for width in (6, 14)]
    result += [('chain_%d' % amount, previous.chain_modules(amount)) for amount in (1, 2, 3)]
    for width in (6, 8, 14, 40):
        result.append(('opposed_%d' % width, previous.opposed_bands(width, 4)[1]))
        result.append(('occupied_%d' % width, previous.occupied_bands(width)[1]))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    local = local_controls()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in previous.phase_images(modules):
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_exact(current, moved)))
    distribution = Counter((record['endpoints'], record['boundary_cost']) for record in local)
    summary = dict(local_states=len(local), physical_images=len(physical),
                   local_cost_distribution=[dict(endpoints=key[0], cost=key[1], count=value)
                                            for key, value in sorted(distribution.items())],
                   zero_reserve_images=sum(record['event_reserve'] == 0 for record in physical),
                   zero_reserve_fixtures=dict(Counter(record['fixture'] for record in physical
                                                     if record['event_reserve'] == 0)),
                   zero_reserve_marked_images=sum(record['event_reserve'] == 0 and record['marked'] > 0
                                                 for record in physical))
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary, local=local,
        physical=physical, scope='Complete local profile census and independent physical geometric counts. The all-parameter exact reserve identity and saturation proof are written, with separately scoped Lean checks. No inference that zero reserve globally excludes negative sources or that general occupied gates satisfy joint allocation.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
