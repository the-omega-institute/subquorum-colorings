"""Independent finite controls of the written sharp open-block proof."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_cubic_triple_ports import triple_core
from check_long_core_words import PATTERNS
from check_regular_starforming import masks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    adjacency = triple_core()
    for first, second in [(0, 5), (12, 17)]:
        adjacency[first].remove(second)
        adjacency[second].remove(first)
    reflection = [group * 6 + 5 - index for group in range(3) for index in range(6)]
    reflection += [19, 18]
    assert all({reflection[neighbor] for neighbor in adjacency[vertex]} ==
               adjacency[reflection[vertex]] for vertex in range(20))
    neighborhoods = masks(adjacency)
    pair_masks = [3 << (12 + 2 * index) for index in range(3)]
    groups = [[vertex] for vertex in range(12)] + [[12, 13], [14, 15], [16, 17], [18], [19]]
    group_masks = [sum(1 << vertex for vertex in group) for group in groups]
    counts = Counter()
    maxima = {hub: 0 for hub in range(3)}
    exceptional = []
    for configuration in range(1 << 17):
        selection = sum(group_masks[index] for index in range(17) if configuration >> index & 1)
        chosen = [vertex for vertex in range(20) if selection >> vertex & 1]
        if any((neighborhoods[vertex] & selection).bit_count() > 1 for vertex in chosen):
            continue
        counts['normalized_dissociation_sets'] += 1
        hubs = (selection >> 18 & 1) + (selection >> 19 & 1)
        score = len(chosen) + sum(not selection & pair for pair in pair_masks)
        maxima[hubs] = max(maxima[hubs], score)
        count_selected_hubs = int(18 in chosen) + int(19 in chosen)
        assert hubs == count_selected_hubs
        cells = [sum(selection >> vertex & 1 for vertex in [2 * index, 2 * index + 1,
                                                           6 + 2 * index, 7 + 2 * index]) +
                 int(selection & pair_masks[index] == pair_masks[index]) for index in range(3)]
        assert max(cells) <= 3 and score == 3 + sum(cells) + hubs
        selected = set(chosen)
        assert score <= 12 + int(selected == PATTERNS['A'])
        if score == 13:
            exceptional.append(chosen)
            assert cells == [3, 2, 3] and hubs == 2
            assert all(len(adjacency[vertex] & selected) == 1 for vertex in [0, 5])
    assert exceptional == [sorted(PATTERNS['A'])]
    assert maxima == {0: 12, 1: 12, 2: 13}
    report = dict(status='ALL_CHECKS_PASSED', scope='Independent finite controls, not a premise of the all-k proof. Normalized pairs have equal selection bits, reducing the open block to seventeen binary choices. Every valid local dissociation set obeys the cell and sharp block inequalities; only A scores13 and its H boundaries are saturated. Reflection is checked as an exact graph automorphism.',
                  normalized_configurations=1 << 17, totals=dict(counts),
                  maxima_by_selected_hubs=maxima, exceptional_sets=exceptional,
                  reflection=reflection)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
