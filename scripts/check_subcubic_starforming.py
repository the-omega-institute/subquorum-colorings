"""Independent controls for the general subcubic gap proof."""

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess

from check_starforming_gap import connected, forms, literal_condition, local_condition


BASE_MASKS = [2048, 896, 3584, 1344, 1152, 2176, 8, 50, 10, 6, 28, 37]
CORE = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
SELECTED = {0, 1, 4, 5, 6, 7, 8, 9}
WITNESSES = {0: 0, 1: 2, 4: 10, 5: 11, 6: 6, 7: 10, 8: 3, 9: 2}
PORT_WITNESSES = {
    (False, False): {2, 3, 4, 5, 8, 9},
    (False, True): {1, 4, 5, 6, 8, 10, 11},
    (True, False): {0, 2, 3, 4, 5, 8, 9},
    (True, True): {0, 1, 2, 4, 5, 6, 8},
}


def base():
    return [{vertex for vertex in range(12) if mask >> vertex & 1}
            for mask in BASE_MASKS]


def dissociation(adjacency, selected):
    return all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)


def base_controls():
    adjacency = base()
    subsets = [{vertex for vertex in range(12) if mask >> vertex & 1}
               for mask in range(4096)]
    for selected in subsets:
        for outside in set(range(12)) - selected:
            assert literal_condition(adjacency, selected, outside) == local_condition(
                adjacency, selected, outside)
    forming = [selected for selected in subsets if forms(adjacency, selected)]
    minimal = [selected for selected in forming
               if not any(proper < selected for proper in forming)]
    assert max(map(len, minimal)) == 8
    assert Counter(map(len, minimal)) == {6: 61, 7: 52, 8: 1}
    assert SELECTED in minimal
    for deleted, outside in WITNESSES.items():
        assert not local_condition(adjacency, SELECTED - {deleted}, outside)
    for deleted, unique in [(1, 2), (7, 10)]:
        reduced = SELECTED - {deleted}
        assert [outside for outside in range(12)
                if outside not in reduced and not local_condition(adjacency, reduced, outside)] == [unique]
    exchanged = (SELECTED - {1, 7}) | {2, 10}
    assert len(exchanged) == 8 and not dissociation(adjacency, exchanged)
    assert all(second in adjacency[first] for first, second in [(9, 2), (2, 10), (10, 4)])
    dissociation_sets = [selected for selected in subsets if dissociation(adjacency, selected)]
    assert max(map(len, dissociation_sets)) == 7
    port_states = []
    for state, witness in PORT_WITNESSES.items():
        exact = max(len(selected) for selected in dissociation_sets
                    if (0 in selected, 6 in selected) == state)
        assert exact == len(witness) == 6 + any(state)
        assert dissociation(adjacency, witness)
        assert (0 in witness, 6 in witness) == state
        assert all(not adjacency[port] & witness for port in {0, 6} & witness)
        port_states.append(dict(state=list(state), maximum=exact, witness=sorted(witness)))
    cycle = [1, 9, 2, 11, 5, 7, 4, 10, 3, 8]
    assert set(cycle) == set(CORE)
    assert all(cycle[(position + 1) % 10] in adjacency[vertex]
               for position, vertex in enumerate(cycle))
    return dict(order=12, beta_2=7, SF_2=8,
                minimal_set_counts=dict(Counter(map(len, minimal))),
                all_subsets_literal_predicate_and_all_proper_minimality_checked=True,
                forced_adjacent_certificates=[2, 10], failed_exchange_path=[9, 2, 10, 4],
                port_states=port_states)


def cycle_graph(copies):
    if copies < 2 or copies % 2:
        raise ValueError('Use an even number of copies, at least two.')
    adjacency = [set() for vertex in range(11 * copies)]
    images = []
    for block in range(copies):
        image = {vertex: 10 * block + position for position, vertex in enumerate(CORE)}
        image[0] = 10 * copies + (block - 1) % copies
        image[6] = 10 * copies + block
        images.append(image)
        for vertex, neighbors in enumerate(base()):
            for neighbor in neighbors:
                adjacency[image[vertex]].add(image[neighbor])
    return adjacency, images


def cycle_controls(copies):
    adjacency, images = cycle_graph(copies)
    selected = {image[vertex] for image in images for vertex in SELECTED}
    assert len(adjacency) == 11 * copies
    assert len(selected) == 7 * copies
    assert sum(map(len, adjacency)) == 28 * copies
    assert min(map(len, adjacency)) == 2 and max(map(len, adjacency)) == 3
    assert connected(adjacency)
    assert all(connected(adjacency, vertex) for vertex in range(len(adjacency)))
    colors = {}
    for block, image in enumerate(images):
        for local, vertex in image.items():
            color = (local >= 6) ^ (block % 2)
            assert vertex not in colors or colors[vertex] == color
            colors[vertex] = color
    assert all(colors[vertex] != colors[neighbor]
               for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
    assert sum(colors.values()) == 11 * copies // 2
    matching = []
    for block, image in enumerate(images):
        edges = [(0, 11), (6, 3), (1, 8), (7, 5), (2, 9), (10, 4)] if block % 2 == 0 else [
            (1, 9), (2, 11), (5, 7), (4, 10), (3, 8)]
        matching.extend((image[first], image[second]) for first, second in edges)
    assert len(matching) == 11 * copies // 2
    assert sorted(vertex for edge in matching for vertex in edge) == list(range(11 * copies))
    assert all(second in adjacency[first] for first, second in matching)
    assert forms(adjacency, selected)
    assert Counter(len(adjacency[vertex] & selected) for vertex in selected) == {
        0: copies, 1: 4 * copies, 3: 2 * copies}
    for image in images:
        for deleted, outside in WITNESSES.items():
            assert not local_condition(adjacency, selected - {image[deleted]}, image[outside])
    ports = {10 * copies + block for block in range(copies) if block % 2 == 0}
    attaining = set()
    for image in images:
        state = (image[0] in ports, image[6] in ports)
        attaining.update(image[vertex] for vertex in PORT_WITNESSES[state])
    assert len(attaining) == 13 * copies // 2
    assert dissociation(adjacency, attaining)
    paths = [[images[0][vertex] for vertex in path] for path in [
        [1, 7], [1, 9, 2], [1, 8, 3], [10, 4, 7],
        [10, 2], [10, 3], [11, 5, 7], [11, 2]]]
    external = [images[0][3]]
    for block in range(1, copies):
        external.append(10 * copies + block - 1)
        external.extend(images[block][vertex] for vertex in [11, 2, 10, 3])
    external.extend([10 * copies + copies - 1, images[0][11]])
    paths.append(list(reversed(external)))
    first_part = {images[0][vertex] for vertex in [1, 10, 11]}
    second_part = {images[0][vertex] for vertex in [7, 2, 3]}
    assert {(path[0], path[-1]) for path in paths} == {
        (first, second) for first in first_part for second in second_part}
    interiors = set()
    for path in paths:
        assert len(path) == len(set(path))
        assert not set(path[1:-1]) & (first_part | second_part | interiors)
        assert all(second in adjacency[first] for first, second in zip(path, path[1:]))
        interiors.update(path[1:-1])
    for port_mask in range(1 << min(copies, 12)) if copies <= 12 else []:
        chosen = {block for block in range(copies) if port_mask >> block & 1}
        touched = {block for block in range(copies)
                   if block in chosen or (block - 1) % copies in chosen}
        assert len(touched) - len(chosen) <= copies // 2
    return dict(copies=copies, order=11 * copies, edges=14 * copies,
                perfect_matching_size=len(matching), independence_number=11 * copies // 2,
                nonplanarity_K33_subdivision_checked=True,
                beta_attaining_size=len(attaining), minimal_star_set_size=len(selected),
                gap_lower_bound=copies // 2, two_connected=True, bipartite=True,
                minimum_degree=2, maximum_degree=3)


def degree_two_controls(order):
    adjacency = [{(vertex - 1) % order, (vertex + 1) % order}
                 for vertex in range(order)]
    subsets = [{vertex for vertex in range(order) if mask >> vertex & 1}
               for mask in range(1 << order)]
    beta = max(len(selected) for selected in subsets if dissociation(adjacency, selected))
    star = max(len(selected) for selected in subsets if forms(adjacency, selected)
               and all(not forms(adjacency, selected - {deleted}) for deleted in selected))
    assert beta == star == 2 * order // 3
    return dict(order=order, beta_2=beta, SF_2=star)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--exhaustive-binary', type=Path)
    arguments = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED', base=base_controls(),
                  cycles=[cycle_controls(copies) for copies in range(2, 33, 2)],
                  degree_two_cycles=[degree_two_controls(order) for order in range(3, 13)],
                  scope='Finite controls only. All-size claims have general written proofs; SF cycle values are lower bounds.')
    if arguments.exhaustive_binary:
        result = subprocess.run([str(arguments.exhaustive_binary.resolve()), '--two-block-cycle'],
                                check=True, text=True, capture_output=True)
        exhaustive = json.loads(result.stdout)
        adjacency, images = cycle_graph(2)
        assert exhaustive['adjacency'] == [sum(1 << vertex for vertex in neighbors)
                                           for neighbors in adjacency]
        assert exhaustive['beta'] == 13 and exhaustive['SF'] == 14
        beta_set = {vertex for vertex in range(22) if exhaustive['beta_mask'] >> vertex & 1}
        star_set = {vertex for vertex in range(22) if exhaustive['star_mask'] >> vertex & 1}
        assert len(beta_set) == 13 and dissociation(adjacency, beta_set)
        assert len(star_set) == 14 and forms(adjacency, star_set)
        assert all(not forms(adjacency, star_set - {deleted}) for deleted in star_set)
        report['two_block_exhaustive'] = dict(exhaustive, subset_count=1 << 22,
                                               implementation='C++20 independent full-subset enumeration')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], base=report['base'], cycles=len(report['cycles']))))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
