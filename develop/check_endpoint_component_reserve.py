"""Physical component restrictions, additive defects and integer reserves."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_component_receivers import endpoint_components
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures
from check_minus_one_joint_compensation import contained
from check_multiple_positive_saturation import inspect_sources
from degree_four_overcount import opposed_modules
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


ADDITIVE_KEYS = ('positive', 'marked', 'activated_positive', 'unused_u_triples',
                 'unpaired_rotor_activation', 'lone_irregular', 'sole_irregular_pair',
                 'mutual_non_event', 'mixed_three', 'boundary_cost', 'event_reserve',
                 'exact_joint_margin', 'unmarked_sources', 'single_marked_sources',
                 'double_marked_sources', 'exceptional_sources', 'nonexceptional_double_sources')


def connected(points):
    remaining = set(points)
    pending = [remaining.pop()]
    while pending:
        added = set(neighbors(pending.pop())) & remaining
        remaining.difference_update(added)
        pending.extend(added)
    return not remaining


def inspect_components(current, modules):
    total = inspect_sources(current, modules)
    total['nonexceptional_double_sources'] = sum(
        dimensions['marked'] == 2 and not dimensions['exceptional']
        for dimensions in total['dimensions'])
    components = endpoint_components(current)
    component_of = {point: index for index, component in enumerate(components)
                    for point in component}
    endpoints = set(component_of)
    source_groups = [[] for _ in components]
    selected_components = {}
    for module in modules:
        assert connected(module['endpoints'])
        source_components = {component_of[point] for point in module['endpoints']}
        assert len(source_components) == 1
        index = next(iter(source_components))
        source_groups[index].append(module)
        original = module['endpoints'] | module['selected']
        assert all(len(set(neighbors(point)) & original) == 3
                   for point in module['endpoints'])
        for support in module['selected']:
            anchors = set(neighbors(support)) & module['endpoints']
            assert len(anchors) == 1
            assert len(set(neighbors(support)) & original) == 1
            if support in endpoints:
                assert component_of[support] == index
            else:
                selected_components.setdefault(support, set()).add(index)
    assert all(len(indices) == 1 for indices in selected_components.values())
    assert set(selected_components) == current[2]
    endpoint_tiles = {}
    for point in endpoints:
        endpoint_tiles.setdefault(tile_of(point), set()).add(component_of[point])
    assert all(len(indices) == 1 for indices in endpoint_tiles.values())
    restricted = []
    qualifying = 0
    for index, members in enumerate(source_groups):
        network = combine(members)
        assert network['endpoints'] == components[index]
        expected_selected = {point for point, indices in selected_components.items()
                             if index in indices}
        assert network['selected'] == expected_selected
        local = inspect_sources((*current[:2], network['selected'], network['matching']), members)
        local['nonexceptional_double_sources'] = sum(
            dimensions['marked'] == 2 and not dimensions['exceptional']
            for dimensions in local['dimensions'])
        reserve = local['event_reserve']
        double = local['double_marked_sources']
        exceptional = local['exceptional_sources']
        is_qualifying = local['nonexceptional_double_sources'] > 0
        assert not double > exceptional or is_qualifying
        if reserve == 0:
            assert local['nonexceptional_double_sources'] == 0
        assert reserve >= is_qualifying
        assert local['exact_joint_margin'] == local['unmarked_sources']+reserve-double
        if local['exact_joint_margin'] < 0 and exceptional == 0:
            assert reserve >= 1 and double >= local['unmarked_sources']+reserve+1
        qualifying += is_qualifying
        restricted.append(dict(index=index, source_count=len(members),
                               endpoint_count=len(components[index]), qualifies=is_qualifying,
                               **{key: local[key] for key in ADDITIVE_KEYS}))
    for key in ADDITIVE_KEYS:
        assert sum(component[key] for component in restricted) == total[key], key
    assert total['event_reserve'] >= qualifying
    bound = total['unmarked_sources']-total['double_marked_sources']+qualifying
    assert total['exact_joint_margin'] >= bound
    criterion = total['double_marked_sources']-total['unmarked_sources'] <= qualifying
    if criterion:
        assert total['exact_joint_margin'] >= 0
    if total['exceptional_sources'] == 0 and all(
            component['double_marked_sources'] <= 1 for component in restricted):
        assert criterion and total['exact_joint_margin'] >= 0
    return dict(component_count=len(restricted), qualifying_components=qualifying,
                global_reserve=total['event_reserve'], global_margin=total['exact_joint_margin'],
                unmarked_sources=total['unmarked_sources'],
                double_marked_sources=total['double_marked_sources'],
                exceptional_sources=total['exceptional_sources'],
                new_margin_bound=bound, sufficient_criterion=criterion,
                components=restricted)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            records.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                **inspect_components(current, moved)))
    for amount in (2, 4, 8):
        modules = [transform_module(module, (False, False, False), (0, 20*index))
                   for index in range(amount) for module in opposed_modules(6, 4)]
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose else
                      (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset)
                                       for module in modules])
            report = inspect_components(current, moved)
            assert report['component_count'] == report['qualifying_components'] == amount
            assert report['global_reserve'] == 5*amount
            assert report['double_marked_sources'] == amount
            assert report['new_margin_bound'] == 0 and report['global_margin'] == 4*amount
            records.append(dict(fixture='separated_opposed_%d' % amount,
                                symmetry=symmetry, **report))
    summary = dict(physical_images=len(records),
                   restricted_components=sum(record['component_count'] for record in records),
                   multiple_qualifying_images=sum(record['qualifying_components'] >= 2
                                                  for record in records),
                   positive_reserve_images=sum(record['global_reserve'] > 0 for record in records),
                   sufficient_criterion_images=sum(record['sufficient_criterion'] for record in records),
                   component_count_distribution=dict(Counter(record['component_count']
                                                              for record in records)))
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary,
        records=records,
        scope='Finite complete physical restrictions with original anchor/degree/whole-source checks and exact additive mark/reserve/defect censuses. Separated marked chambers exercise several qualifying components at positive reserve. No realization or exclusion of a connected two-double-mark R1 obstruction; universal restriction and tile connectivity are written proofs.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
