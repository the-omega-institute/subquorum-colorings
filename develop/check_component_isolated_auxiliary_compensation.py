"""Check component-isolated auxiliary toggles and a shared-beta collision."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_terminal_cancellation_and_stranded_demand import components, terminal_data
from check_zero_capacity_gap_beta_compensation import barrier_family


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def matchings(vertices):
    if not vertices:
        yield []
        return
    first, *remaining = vertices
    yield from matchings(remaining)
    for index, second in enumerate(remaining):
        rest = remaining[:index]+remaining[index+1:]
        for following in matchings(rest):
            yield [(first, second)]+following


def inventory(records, kinds):
    return Counter('cycle' if not record['ends'] else
                   'alpha' if all(kinds[point] == 'TP' for point in record['ends']) else
                   'beta' if all(kinds[point] == 'BP' for point in record['ends']) else
                   'mixed' for record in records)


def support_of(path, records):
    points = set(path)
    return frozenset(index for index, record in enumerate(records)
                     if points & record['vertices'])


def toggle(auxiliary, paths):
    removed, added = set(), []
    for path in paths:
        removed.update(frozenset(edge) for edge in zip(path[1::2], path[2::2]))
        added.extend(zip(path[::2], path[1::2]))
    assert removed <= {frozenset(edge) for edge in auxiliary}
    following = [edge for edge in auxiliary if frozenset(edge) not in removed]+added
    covered = [point for edge in following for point in edge]
    assert len(covered) == len(set(covered))
    assert {point for edge in auxiliary for point in edge} <= set(covered)
    return following


def check_family(vertices, actual, auxiliary, kinds, paths):
    before = components(vertices, actual+auxiliary)
    supports = [support_of(path, before) for path in paths]
    assert all(not first & second for first, second in itertools.combinations(supports, 2))
    for path, support in zip(paths, supports):
        assert len(path) == len(set(path)) and len(path) % 2 == 0
        assert kinds[path[0]] == 'TP' and kinds[path[-1]] == 'BP'
        assert all(point not in kinds for point in path[1:-1])
        local = inventory([before[index] for index in support], kinds)
        assert local['alpha'] == local['beta'] == 1 and local['mixed'] == 0
    following = toggle(auxiliary, paths)
    covered = {point for edge in following for point in edge}
    free = {point: kinds[point] for point in vertices-covered}
    assert len(free) == len(kinds)-2*len(paths)
    after = components(vertices, actual+following)
    old_counts, new_counts = inventory(before, kinds), inventory(after, free)
    assert new_counts['alpha'] == old_counts['alpha']-len(paths)
    assert new_counts['beta'] == old_counts['beta']-len(paths)
    assert new_counts['mixed'] == old_counts['mixed']+len(paths)
    touched = set().union(*supports)
    for index, record in enumerate(before):
        if index not in touched:
            assert any(all(record[key] == other[key] for key in ('vertices', 'ends', 'cycle'))
                       for other in after)


def augmenting_paths(vertices, auxiliary, kinds):
    partner = {first: second for edge in auxiliary
               for first, second in (edge, edge[::-1])}

    def extend(path):
        for point in vertices-set(path):
            if kinds.get(point) == 'BP':
                yield path+[point]
            elif point in partner and partner[point] not in path:
                yield from extend(path+[point, partner[point]])

    for source in kinds:
        if kinds[source] == 'TP':
            yield from extend([source])


def abstract_controls(totals):
    for size in (2, 4, 6, 8):
        vertices = set(range(size))
        actual = [(point, point+1) for point in range(0, size, 2)]
        for auxiliary in matchings(list(range(size))):
            free = sorted(vertices-{point for edge in auxiliary for point in edge})
            before = components(vertices, actual+auxiliary)
            for signs in itertools.product(('TP', 'BP'), repeat=len(free)):
                kinds = dict(zip(free, signs))
                eligible = []
                for path in augmenting_paths(vertices, auxiliary, kinds):
                    support = support_of(path, before)
                    local = inventory([before[index] for index in support], kinds)
                    if local['alpha'] == local['beta'] == 1 and local['mixed'] == 0:
                        check_family(vertices, actual, auxiliary, kinds, [path])
                        eligible.append((path, support))
                        totals['isolated_abstract_paths'] += 1
                for (first, first_support), (second, second_support) in itertools.combinations(eligible, 2):
                    if not first_support & second_support:
                        check_family(vertices, actual, auxiliary, kinds, [first, second])
                        totals['simultaneous_disjoint_support_pairs'] += 1
                totals['signed_abstract_models'] += 1


def physical_controls(totals):
    for width, depth in itertools.product((6, 8, 12, 20), range(1, 25)):
        current, bands, _, _, shift = barrier_family(width, depth, True)
        _, _, _, _, kinds, _, _ = terminal_data(current, bands)
        vertices = {point for edge in current[3] for point in edge}
        auxiliary = [tuple(column) for columns in bands for column in columns
                     if set(column) <= vertices]
        outer = 2-2*depth+shift
        path = [(5, 3+shift), (4, outer), (5, outer),
                (5, outer-1), (4, outer-1), (4, outer-2)]
        check_family(vertices, current[3], auxiliary, kinds, [path])
        totals['reflected_physical_support_controls'] += 1


def collision_control(totals):
    vertices = set(range(6))
    actual = [(0, 1), (2, 3), (4, 5)]
    kinds = {point: 'TP' if point < 4 else 'BP' for point in vertices}
    paths = [[0, 4], [2, 5]]
    assert not set(paths[0]) & set(paths[1])
    following = toggle([], paths)
    before = components(vertices, actual)
    assert support_of(paths[0], before) & support_of(paths[1], before)
    free = {point: kinds[point] for point in (1, 3)}
    after = inventory(components(vertices, actual+following), free)
    assert after['alpha'] == 1 and after['beta'] == after['mixed'] == 0
    totals['vertex_disjoint_shared_beta_obstruction'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    collision_control(totals)
    abstract_controls(totals)
    physical_controls(totals)
    record = dict(status='PASS', totals=dict(totals),
                  scope='Abstract complete permitted-edge relation on at most eight endpoints; '
                  'fixed actual perfect matching up to vertex relabelling; all partial auxiliary '
                  'matchings, all free-end signs, simple qualifying augmenting paths and '
                  'disjoint-support pairs. Also 96 reflected physical support controls. '
                  'Finite checks support the general written conditional theorem; '
                  'no universal geometric existence, new Lean proof or Oracle acceptance.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record, sort_keys=True))


if __name__ == '__main__':
    main()
