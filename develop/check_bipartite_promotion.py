"""Independent exhaustive controls for complete bipartite promotion freezing."""

import argparse
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def subsets(vertices):
    ordered = tuple(sorted(vertices))
    for size in range(len(ordered)+1):
        for chosen in itertools.combinations(ordered, size):
            yield frozenset(chosen)


def matching_choices(edges):
    for chosen in subsets(edges):
        if len({vertex for edge in chosen for vertex in edge}) == 2*len(chosen):
            yield tuple(sorted(chosen))


def feasible(selected, matching, adjacency, promoted):
    mates = {vertex: partner for first, second in matching
             for vertex, partner in ((first, second), (second, first))}
    if not promoted <= mates.keys() or any(mates[vertex] in promoted for vertex in promoted):
        return False
    occupied = selected | mates.keys()
    kept = occupied-{mates[vertex] for vertex in promoted}
    return all(len(adjacency[vertex] & kept) <= 1 for vertex in selected | promoted)


def freezing(selected, matching, adjacency):
    mates = {vertex: partner for first, second in matching
             for vertex, partner in ((first, second), (second, first))}
    frozen = set()
    layers = []
    while True:
        retained = selected | {mates[vertex] for vertex in frozen}
        added = {vertex for vertex in mates if vertex not in frozen
                 and len(adjacency[vertex] & retained) >= 2}
        if not added:
            return frozen, layers
        layers.append(sorted(added))
        frozen.update(added)


def color_core(selected, matching, adjacency, colors, color):
    mates = {vertex: partner for first, second in matching
             for vertex, partner in ((first, second), (second, first))}
    original = selected | mates.keys()
    remaining = {vertex for vertex in mates if colors[vertex] == color}
    while True:
        removed_mates = {mates[vertex] for vertex in remaining}
        bad = {vertex for vertex in remaining
               if len(adjacency[vertex] & (original-removed_mates)) > 1}
        if not bad:
            return remaining
        remaining -= bad


def verify(selected, matching, adjacency, colors, exhaustive=True):
    mates = {vertex: partner for first, second in matching
             for vertex, partner in ((first, second), (second, first))}
    endpoints = set(mates)
    original = selected | endpoints
    assert selected.isdisjoint(endpoints)
    assert all(len(adjacency[vertex] & original) <= 1 for vertex in selected)
    assert all(colors[first] != colors[second] for first, second in matching)
    assert all(colors[vertex] != colors[neighbor]
               for vertex in original for neighbor in adjacency[vertex] & original)
    frozen, layers = freezing(selected, matching, adjacency)
    available = [{vertex for vertex in endpoints-frozen if colors[vertex] == color}
                 for color in (0, 1)]
    for color, chosen in enumerate(available):
        assert feasible(selected, matching, adjacency, chosen)
        assert chosen == color_core(selected, matching, adjacency, colors, color)
    examined = valid = 0
    universal_promotable = set()
    if exhaustive:
        for states in itertools.product((0, 1, 2), repeat=len(matching)):
            promoted = {edge[state-1] for edge, state in zip(matching, states) if state}
            actual = feasible(selected, matching, adjacency, promoted)
            restricted = [{vertex for vertex in promoted if colors[vertex] == color}
                          for color in (0, 1)]
            assert actual == all(feasible(selected, matching, adjacency, part)
                                 for part in restricted)
            examined += 1
            if actual:
                valid += 1
                universal_promotable.update(promoted)
                assert not promoted & frozen
                assert all(part <= allowed for part, allowed in zip(restricted, available))
        assert universal_promotable == endpoints-frozen
        assert (valid == 1) == (frozen == endpoints)
    return dict(all_orientations_enumerated=exhaustive,
                oriented_choices=examined if exhaustive else None,
                feasible_choices=valid if exhaustive else None,
                frozen=len(frozen), layers=len(layers),
                terminal=frozen == endpoints, available=[len(part) for part in available])


def exhaustive_bipartite():
    left = set(range(3))
    right = set(range(3, 6))
    vertices = left | right
    possible = tuple(itertools.product(sorted(left), sorted(right)))
    colors = {vertex: int(vertex in right) for vertex in vertices}
    totals = dict(graphs=0, graph_matching_pairs=0, feasible_configurations=0,
                  oriented_choices=0, feasible_choices=0, terminal_configurations=0,
                  maximum_freeze_layers=0)
    for edges in subsets(possible):
        adjacency = {vertex: set() for vertex in vertices}
        for first, second in edges:
            adjacency[first].add(second)
            adjacency[second].add(first)
        totals['graphs'] += 1
        for matching in matching_choices(edges):
            totals['graph_matching_pairs'] += 1
            endpoints = {vertex for edge in matching for vertex in edge}
            for selected in subsets(vertices-endpoints):
                if any(len(adjacency[vertex] & (selected | endpoints)) > 1 for vertex in selected):
                    continue
                checked = verify(selected, matching, adjacency, colors)
                totals['feasible_configurations'] += 1
                totals['oriented_choices'] += checked['oriented_choices']
                totals['feasible_choices'] += checked['feasible_choices']
                totals['terminal_configurations'] += checked['terminal']
                totals['maximum_freeze_layers'] = max(totals['maximum_freeze_layers'],
                                                       checked['layers'])
    assert totals['graphs'] == 512 and totals['graph_matching_pairs'] == 5504
    return totals


def physical_controls():
    from check_cooperative_promotion import neighbors
    from check_mixed_color_ladders import mixed_ladder
    from check_promotion_cores import anchored_diamonds, degree_four_patch, tight_diamond
    from check_single_square_parity import neutral_obstacle

    neutral = neutral_obstacle()
    fixtures = [anchored_diamonds(1)[0], anchored_diamonds(2)[0], degree_four_patch(),
                tight_diamond()[0], (*neutral['shape'], set(neutral['selected']), neutral['matching'])]
    fixtures.extend(mixed_ladder(left, right)[0] for left, right in ((1, 1), (1, 2), (2, 1)))
    records = []
    for current in fixtures:
        selected, matching = current[2:]
        occupied = selected | {vertex for edge in matching for vertex in edge}
        adjacency = {vertex: set(neighbors(vertex)) & occupied for vertex in occupied}
        colors = {vertex: sum(vertex) % 2 for vertex in occupied}
        checked = verify(selected, matching, adjacency, colors, exhaustive=len(matching) <= 8)
        records.append(dict(shape=current[:2], matching_edges=len(matching), **checked))
    return records


def nonbipartite_obstacle():
    vertices = set(range(6))
    adjacency = {vertex: vertices-{vertex} for vertex in vertices}
    matching = ((0, 1), (2, 3), (4, 5))
    frozen, layers = freezing(set(), matching, adjacency)
    assert not frozen and not layers
    examined = nonempty_feasible = 0
    for states in itertools.product((0, 1, 2), repeat=3):
        if not any(states):
            continue
        promoted = {edge[state-1] for edge, state in zip(matching, states) if state}
        examined += 1
        nonempty_feasible += feasible(set(), matching, adjacency, promoted)
    assert examined == 26 and nonempty_feasible == 0
    return dict(graph='K6', matching=matching, selected=[], frozen=[],
                nonempty_oriented_bundles=examined, feasible_nonempty_bundles=nonempty_feasible,
                conclusion='Bipartiteness is essential: empty freeze closure need not imply a promotion in a general graph.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED', exhaustive=exhaustive_bipartite(),
                  physical=physical_controls(), nonbipartite_obstacle=nonbipartite_obstacle(),
                  scope='All bipartite graphs with labeled parts of size three, every matching and feasible selected subset; all oriented bundles including empty. Graph-level general proof is independent of these finite checks.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
