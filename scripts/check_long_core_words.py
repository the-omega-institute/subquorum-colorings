"""Literal controls for the general cyclic A/B omission obstruction."""

import argparse
from itertools import product
import json
from pathlib import Path

from check_cubic_padding_rings import core, edge
from check_cubic_starforming import EIGHT, SELECTED, SEVEN, base, dissociation, star_masks
from check_regular_starforming import bipartition
from check_starforming_gap import connected, forms


PATTERNS = {
    'A': {0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 18, 19},
    'B': {1, 4, 6, 7, 8, 9, 10, 11, 14, 15},
}


def translate(copies, block, local):
    if local < 18:
        group, index = divmod(local, 6)
        return 6 * copies * group + 6 * block + index
    return 18 * copies + 2 * block + local - 18


def word_control(word):
    copies = len(word)
    assert all(word[index] != 'A' or word[(index + 1) % copies] != 'A'
               for index in range(copies))
    adjacency = core(copies)
    pairs = [(12 * copies + 2 * index, 12 * copies + 2 * index + 1)
             for index in range(3 * copies)]
    for first, second in pairs:
        adjacency[first].remove(second)
        adjacency[second].remove(first)
    selected = {translate(copies, block, local)
                for block, kind in enumerate(word) for local in PATTERNS[kind]}
    omitted = [index for index, pair in enumerate(pairs) if not set(pair) & selected]
    count_a = word.count('A')
    assert len(selected) == 10 * copies + 2 * count_a
    assert len(omitted) == 2 * copies - count_a
    assert len(selected) + len(omitted) == 12 * copies + count_a
    assert dissociation(adjacency, selected)
    for block in range(copies):
        successor = (block + 1) % copies
        for group in [0, 2]:
            first = 6 * copies * group + 6 * block + 5
            second = 6 * copies * group + 6 * successor
            assert second in adjacency[first]
            assert not {first, second} <= selected
    return adjacency, pairs, selected, omitted


def full_control(copies):
    word = 'AB' * (copies // 2) + ('B' if copies % 2 else '')
    adjacency, pairs, witness, omitted = word_control(word)
    core_witness = sorted(witness)
    selected = set(range(12 * copies))
    omitted_set = set(omitted)
    for index, (first, second) in enumerate(pairs):
        offset = len(adjacency)
        block = base()
        block[0].remove(8)
        block[8].remove(0)
        adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in block)
        edge(adjacency, offset, second)
        edge(adjacency, offset + 8, first)
        witness |= {offset + vertex for vertex in (EIGHT if index in omitted_set else SEVEN)}
        selected |= {offset + vertex for vertex in SELECTED}
    count_a = copies // 2
    assert len(adjacency) == 62 * copies
    assert len(witness) == 33 * copies + count_a
    assert len(selected) == 36 * copies
    assert sum(not adjacency[vertex] & selected for vertex in selected) == 6 * copies
    assert dissociation(adjacency, witness)
    assert all(len(neighbors) == 3 and vertex not in neighbors and
               all(vertex in adjacency[neighbor] for neighbor in neighbors)
               for vertex, neighbors in enumerate(adjacency))
    assert bipartition(adjacency) is not None and connected(adjacency)
    stars = star_masks(adjacency)
    containing = [[] for vertex in adjacency]
    for star in stars:
        vertices = [vertex for vertex in range(len(adjacency)) if star >> vertex & 1]
        assert len(vertices) == 3
        for vertex in vertices:
            containing[vertex].append(star)

    def literal_forms(selection):
        chosen_mask = sum(1 << vertex for vertex in selection)
        for outside in set(range(len(adjacency))) - selection:
            available = chosen_mask | (1 << outside)
            if not any(star & available == star for star in containing[outside]):
                return False
        return True

    assert literal_forms(selected) and forms(adjacency, selected)
    assert all(not literal_forms(selected - {deleted}) for deleted in selected)
    slack_lower = 3 * len(adjacency) + 2 * len(witness) - 7 * len(selected)
    assert slack_lower == 2 * count_a
    gap_numerator_upper = 3 * len(adjacency) - 5 * len(witness)
    assert gap_numerator_upper == 21 * copies - 5 * count_a
    return dict(k=copies, word=word, order=len(adjacency),
                core_dissociation_witness=core_witness, omitted_pairs=omitted,
                core_score=len(core_witness) + len(omitted),
                full_dissociation_witness_size=len(witness),
                minimal_forming_selection_size=len(selected), selected_isolates=6 * copies,
                selected_deletion_checks=len(selected), slack_lower=slack_lower,
                seven_times_gap_upper=gap_numerator_upper,
                exact_beta_claimed=False, exact_SF_claimed=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    words_checked = 0
    for copies in range(1, 9):
        for letters in product('AB', repeat=copies):
            word = ''.join(letters)
            if any(word[index] == word[(index + 1) % copies] == 'A'
                   for index in range(copies)):
                continue
            word_control(word)
            words_checked += 1
    instances = [full_control(copies) for copies in range(1, 17)]
    obstacle = instances[1]
    assert obstacle['core_score'] == 25 and obstacle['omitted_pairs'] == [1, 3, 5]
    assert obstacle['core_dissociation_witness'] == [
        0, 1, 4, 5, 7, 10, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25,
        28, 29, 32, 33, 36, 37]
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='Finite literal controls of the written all-k word and attachment proofs. No optimization and no exact beta or SF claim. Literal non-induced stars include each newly outside deleted vertex; upward closure makes single deletion failures sufficient for inclusion-minimality.',
                  cyclic_words_checked=words_checked, full_instances=instances,
                  selected_deletion_checks=sum(record['selected_deletion_checks'] for record in instances))
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in
                      ['status', 'cyclic_words_checked', 'selected_deletion_checks']}))


if __name__ == '__main__':
    main()
