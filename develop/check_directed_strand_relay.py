#!/usr/bin/env python3
"""Abstract endpoint controls for the ordered donor relay theorem."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

from check_strand_switches import strand_graph


def add_edge(adjacency, first, second):
    adjacency[first].add(second)
    adjacency[second].add(first)


def join_arm(adjacency, first, second, subdivision, unique):
    cursor = first
    for position in range(subdivision):
        vertex = (unique, position)
        add_edge(adjacency, cursor, vertex)
        cursor = vertex
    add_edge(adjacency, cursor, second)


def control(word, debt, subdivision):
    junctions = [tuple((index, corner) for corner in range(4)) for index in range(len(word)+1)]
    adjacency = collections.defaultdict(set)
    labels = {}
    serial = 1000
    ends = []
    for strand_index, kind in enumerate(('SS', *word, debt)):
        visits = []
        if strand_index > 0:
            visits.append(junctions[strand_index-1][2:])
        if strand_index <= len(word):
            visits.append(junctions[strand_index][:2])
        first_end, second_end = (serial, 0), (serial, 1)
        serial += 1
        labels[first_end], labels[second_end] = kind
        ends.append((first_end, second_end))
        cursor = first_end
        for first, second in visits:
            join_arm(adjacency, cursor, first, subdivision, serial)
            serial += 1
            add_edge(adjacency, first, second)
            cursor = second
        join_arm(adjacency, cursor, second_end, subdivision, serial)
        serial += 1
    strands, cycles = strand_graph(adjacency, labels)
    initial = collections.Counter(strand['kind'] for strand in strands)
    assert not cycles and initial == collections.Counter(('SS', *word, debt))
    intermediate = []
    for index, corners in enumerate(junctions):
        for first, second in ((corners[0], corners[1]), (corners[2], corners[3])):
            adjacency[first].remove(second)
            adjacency[second].remove(first)
        add_edge(adjacency, corners[0], corners[3])
        add_edge(adjacency, corners[1], corners[2])
        strands, cycles = strand_graph(adjacency, labels)
        counts = collections.Counter(strand['kind'] for strand in strands)
        assert not cycles
        if index < len(word):
            assert counts == initial
            donor, = [strand for strand in strands if strand['kind'] == 'SS']
            assert set(junctions[index+1][:2]) <= donor['vertices']
        else:
            expected = initial.copy()
            expected['SS'] -= 1
            expected[debt] -= 1
            expected['LS'] += debt.count('L')
            expected['PS'] += debt.count('P')
            assert +counts == +expected
        intermediate.append(dict(counts))
    return dict(word=list(word), debt=debt, subdivision=subdivision,
                switches=len(junctions), initial=dict(initial), final=intermediate[-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    checked = 0
    for length in range(7):
        for word in itertools.product(('LS', 'PS'), repeat=length):
            for debt, subdivision in itertools.product(('LL', 'LP', 'PP'), (0, 2, 6)):
                control(word, debt, subdivision)
                checked += 1
    long_controls = [control(tuple('LS' if index % 2 else 'PS' for index in range(length)), debt, 2)
                     for length in range(7, 41) for debt in ('LL', 'LP', 'PP')]
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/DIRECTED_STRAND_RELAY.md', Path(__file__).with_name('check_strand_switches.py')]
    report = dict(status='ALL_CHECKS_PASSED', exhaustive_neutral_word_controls=checked,
                  word_length_range=[0,6], arm_subdivisions=[0,2,6], long_controls=long_controls,
                  long_length_range=[7,40],
                  sha256={str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                  scope='Abstract strand topology controls; no claim all words realize physical feasible grids. General geometric theorem has explicit directed junction assumptions.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','exhaustive_neutral_word_controls','word_length_range','long_length_range')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
