"""Actual-source separator restrictions and the shared-reserve correction."""

import json

from check_closed_extension_reserve import signature
from check_connected_source_cut_obstruction import connected
from check_cooperative_promotion import neighbors
from check_exact_event_reserve import fixtures
from check_degree_three_fusion import phase_images
from check_source_retention_closure import cut_modules, feasible, marked_counts
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def graph(modules):
    owner = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    assert len(owner) == sum(len(module['endpoints']) for module in modules)
    return {index: {owner[other] for point in module['endpoints']
                    for other in neighbors(point) if other in owner and owner[other] != index}
            for index, module in enumerate(modules)}


def branches(adjacency, separator):
    remaining = set(adjacency)-{separator}
    result = []
    while remaining:
        reached = {min(remaining)}
        pending = list(reached)
        remaining.difference_update(reached)
        while pending:
            fresh = adjacency[pending.pop()] & remaining
            reached.update(fresh)
            remaining.difference_update(fresh)
            pending.extend(fresh)
        result.append(frozenset(reached))
    return result


def inspect_split(modules, separator, left, right):
    full = frozenset(range(len(modules)))
    assert left & right == {separator} and left | right == full
    assert feasible(modules, left) and feasible(modules, right)
    first, second, total = [signature(modules, retained) for retained in (left, right, full)]
    assert first['events'].isdisjoint(second['events'])
    assert first['events'] | second['events'] == total['events']
    assert first['full'].isdisjoint(second['full'])
    assert first['full'] | second['full'] == total['full']
    shared_mass = max(0, -modules[separator]['charge'])
    assert total['reserve'] == first['reserve']+second['reserve']-shared_mass
    marks = [marked_counts(modules, retained) for retained in (left, right, full)]
    duplicates = 0
    positive_separator = int(modules[separator]['charge'] == 1)
    for owner, sides in marks[2].items():
        if owner != separator:
            actual = marks[0] if owner in left else marks[1]
            assert actual[owner] == sides
        else:
            assert sides == tuple(first_side or second_side for first_side, second_side
                                  in zip(marks[0][owner], marks[1][owner]))
            duplicates = sum(first_side and second_side for first_side, second_side
                             in zip(marks[0][owner], marks[1][owner]))
    marked = [sum(sum(sides) for sides in item.values()) for item in marks]
    positive = [sum(modules[index]['charge'] == 1 for index in retained)
                for retained in (left, right, full)]
    assert positive[2] == positive[0]+positive[1]-positive_separator
    assert marked[2] == marked[0]+marked[1]-duplicates
    margins = [positive[index]+data['reserve']-marked[index]
               for index, data in enumerate((first, second, total))]
    assert margins[2] == margins[0]+margins[1]-positive_separator-shared_mass+duplicates
    return dict(separator_charge=modules[separator]['charge'], duplicate_marked_sides=duplicates,
                shared_mass=shared_mass, reserves=[first['reserve'], second['reserve'], total['reserve']],
                margins=margins)


def inspect_family(name, modules):
    adjacency = graph(modules)
    checked = 0
    corrections = set()
    for separator in range(len(modules)):
        parts = branches(adjacency, separator)
        if len(parts) < 2:
            continue
        masks = range(1, 1 << (len(parts)-1)) if len(parts) <= 8 else [1 << index for index in range(len(parts)-1)]
        for mask in masks:
            left = frozenset({separator}).union(*(part for index, part in enumerate(parts) if mask >> index & 1))
            right = (frozenset(range(len(modules)))-left) | {separator}
            report = inspect_split(modules, separator, left, right)
            corrections.add((report['separator_charge'], report['duplicate_marked_sides']))
            checked += 1
    return dict(fixture=name, owners=len(modules), legal_separator_splits=checked,
                correction_types=sorted(corrections))


def connected_witness():
    modules = cut_modules(10, 8)+[transform_module(module, (False, False, True), (18, 16))
                                for module in cut_modules(4, 8)]
    adjacency = graph(modules)
    parts = branches(adjacency, 1)
    assert set(parts) == {frozenset((0, 2, 3)), frozenset((4, 5, 6, 7))}
    left = frozenset((0, 1, 2, 3))
    right = frozenset((1, 4, 5, 6, 7))
    assert connected(combine(modules)['endpoints'])
    report = inspect_split(modules, 1, left, right)
    assert report['reserves'] == [3, 16, 18]
    assert report['shared_mass'] == 1
    return dict(separator='V2', left_owners=[1, 2, 3, 4], right_owners=[2, 5, 6, 7, 8], **report)


def main():
    controls = [dict(symmetry=symmetry, phase=phase, **inspect_family(name, moved))
                for name, modules in fixtures()
                for symmetry, phase, _, _, moved in phase_images(modules)]
    print(json.dumps(dict(status='PASS', controls=controls,
                         legal_separator_splits=sum(row['legal_separator_splits'] for row in controls),
                         connected_witness=connected_witness(),
                         scope='Actual complete-source restrictions, source contact separation, '
                         'exact directed-event/mixed-full-tile disjoint partitions, reserve and '
                         'actual mark valuation. Finite controls do not prove the general '
                         'separator theorem or unrestricted allocation. Partitions exhaustive '
                         'through eight branches, singleton branch samples thereafter.'), indent=2))


if __name__ == '__main__':
    main()
