"""Physical and cut controls for capacity-aware overlapping strip claims."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_adaptive_strip_compensation import certificate, maximum_strip_certificate
from check_coalesced_mouths import assemble, move_source
from check_component_receivers import vertices_of
from check_mixed_source_contacts import add_parallel, source_with_chamber
from check_orthogonal_source_mouths import fill_greedily, strips_of
from check_owned_donors import endpoint_data
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def capacity_path(width=64):
    assert width >= 64 and width % 2 == 0
    sources = []
    for index in range(4):
        tip = 40 if index < 3 else 44
        depth = (tip-4-4*index)//2
        sources.append(move_source(source_with_chamber(width-8*index, depth),
                       lambda point, index=index: (point[0]+4*index, point[1]+4*index)))
    for index in range(3):
        sources.append(move_source(source_with_chamber(38-8*index, 8-2*index),
                       lambda point, index=index: (point[1]+18+4*index, point[0]+20+4*index)))
    sources.append(move_source(source_with_chamber(10, 4),
                   lambda point: (point[1]+30, point[0]+32)))
    current = assemble(70, width+10, sources)
    for start, finish, column in ((37, 40, 18), (37, 44, 50)):
        selected = set(current[2]) | {(start-1, column), (finish+1, column)}
        selected.update((row, column+(1 if (row-finish) % 2 else -1))
                        for row in range(start, finish+1))
        matching = current[3]+[((row, column), (row+1, column))
                               for row in range(start, finish, 2)]
        current = *current[:2], selected, matching
    current = add_parallel(current, 48, 41, 8, 1)
    current = add_parallel(current, 38, 45, 2, 1)
    return current, sources


def capacity_forest(count):
    baseline, originals = capacity_path()
    selected, matching, sources = set(), [], []
    for index in range(count):
        transpose = bool(index % 2)
        _, moved_selected, moved_matching = transformed(*baseline, transpose, False, False)
        move = lambda point, index=index: (point[0]+2, point[1]+2+80*index)
        selected.update(move(point) for point in moved_selected)
        matching.extend(tuple(move(point) for point in edge) for edge in moved_matching)
        sources.extend(move_source(source, lambda point, move=move, transpose=transpose:
                       move((point[1], point[0]) if transpose else point)) for source in originals)
    return (80, 80*count, selected, matching), sources


def capped_certificate(current, sources, required_selected):
    old = certificate(current, sources)
    strips = strips_of(sources)
    weights = old['weights']
    horizontal = [strip['horizontal'] for strip in strips]
    endpoints = endpoint_data(current)[0]
    assert required_selected <= current[2]
    edges, coarse, retained = [], [], []
    for first, second in itertools.product(range(len(strips)), repeat=2):
        if not horizontal[first] or horizontal[second]:
            continue
        shared = strips[first]['tiles'] & strips[second]['tiles']
        if not shared:
            continue
        assert len(shared) == 1
        edges.append((first, second))
        coarse.append(2*sum(not vertices_of({tile}) & endpoints for tile in shared))
        retained.append(sum(2-len(vertices_of({tile}) & required_selected)
                            for tile in shared if not vertices_of({tile}) & endpoints))
    reports = {}
    for name, capacities in (('capacity_two', coarse), ('retained_support', retained)):
        value, chosen, shared_flow = maximum_strip_certificate(weights, horizontal, edges, capacities)
        if len(strips) <= 16:
            exhaustive = max(sum(weight for index, weight in enumerate(weights) if mask >> index & 1)-
                             sum(capacity for (first, second), capacity in zip(edges, capacities)
                                 if mask >> first & 1 and mask >> second & 1)
                             for mask in range(1 << len(strips)))
            assert exhaustive == value
        multiplicity = Counter(tile for index in chosen for tile in strips[index]['tiles']
                               if not vertices_of({tile}) & endpoints)
        original_payment = sum(2-len(vertices_of({tile}) & current[2]) for tile in multiplicity)
        repeated_payment = sum(2-len(vertices_of({tile}) & current[2])
                               for tile, count in multiplicity.items() if count == 2)
        penalty = sum(capacity for (first, second), capacity in zip(edges, capacities)
                      if first in chosen and second in chosen)
        assert repeated_payment <= penalty
        actual_claims = sum(count*(2-len(vertices_of({tile}) & current[2]))
                            for tile, count in multiplicity.items())
        assert original_payment == actual_claims-repeated_payment
        assert value <= actual_claims-penalty <= original_payment <= old['physical']['physical_union_payment']
        assert old['physical']['half_area_deficit'] >= value-len(sources)+old['physical']['outside_remainder']
        reports[name] = dict(value=value, selected_strips=sorted(chosen), capacities=capacities,
                             edges=edges, shared_flow=shared_flow, deducted_capacity=penalty,
                             actual_repeated_payment=repeated_payment, actual_union_payment=original_payment)
    return dict(exclusive=old, capacity_certificates=reports)


def symmetry_controls(current, sources, expected):
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        def move(point):
            row, column = point
            row = current[0]-1-row if vertical else row
            column = current[1]-1-column if horizontal else column
            return (column, row) if transpose else (row, column)
        record = capped_certificate((*shape, selected, matching),
                                    [move_source(source, move) for source in sources], selected)
        assert tuple(record['capacity_certificates'][name]['value']
                     for name in ('capacity_two', 'retained_support')) == expected
    return 8


def controls():
    records, images = [], 0
    witness = None
    for width in (*range(64, 85, 2), 100, 160):
        current, sources = capacity_path(width)
        for seed in (None, 0, 7):
            filled = current if seed is None else fill_greedily(current, sources, seed)
            record = capped_certificate(filled, sources, current[2])
            assert record['exclusive']['weighted_comb_flux'] == -4
            assert record['exclusive']['independent_weight'] == 6 < 8
            assert record['capacity_certificates']['capacity_two']['value'] == 8
            assert record['capacity_certificates']['retained_support']['value'] == 9
            if seed is None:
                assert not record['exclusive']['old_crossing_criterion']
                assert record['exclusive']['physical']['effective_crossing_loss'] == 5
            records.append(dict(kind='all_width_capacity_path', width=width, seed=seed, result=record))
        if width in (64, 100):
            images += symmetry_controls(current, sources, (8, 9))
        if width == 64:
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                           result=capped_certificate(current, sources, current[2]))
    for count in (1, 2, 3, 4, 6, 8):
        current, sources = capacity_forest(count)
        record = capped_certificate(current, sources, current[2])
        assert record['exclusive']['weighted_comb_flux'] == -4*count
        assert record['exclusive']['independent_weight'] == 6*count
        assert record['capacity_certificates']['capacity_two']['value'] == 8*count
        assert record['capacity_certificates']['retained_support']['value'] == 9*count
        records.append(dict(kind='all_count_capacity_forest', count=count, result=record))
        if count == 2:
            images += symmetry_controls(current, sources, (16, 18))
    abstract = 0
    edges = list(itertools.product(range(2), range(2, 4)))
    for weights in ([5, 1, 5, 1], [0, 2, 1, 3], [2, 2, 2, 2]):
        for capacities in itertools.product(range(3), repeat=4):
            value, _, _ = maximum_strip_certificate(weights, [True, True, False, False], edges, capacities)
            exhaustive = max(sum(weight for index, weight in enumerate(weights) if mask >> index & 1)-
                             sum(capacity for (first, second), capacity in zip(edges, capacities)
                                 if mask >> first & 1 and mask >> second & 1)
                             for mask in range(16))
            assert value == exhaustive
            abstract += 1
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), symmetry_images=images,
                abstract_capped_graph_controls=abstract, records=records, smallest_witness=witness,
                scope='Controls of a general capacity-aware strip inequality and classical capacitated '
                      'cut optimization. General all-even-width and all-count constructions have written '
                      'proofs. Shared physical donors are deducted, not spent twice. Exclusive weight '
                      'and old crossing criteria fail in the explicit baseline, while capped certificates '
                      'prove coefficient one. No universal negative-flux or full geometric Lean claim.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in
                      ('status', 'physical_cases', 'symmetry_images', 'abstract_capped_graph_controls')}))


if __name__ == '__main__':
    main()
