#!/usr/bin/env python3
"""Small all-graph controls of the global 2-star certificate bound."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask -= bit


def adjacency_masks(order, edges):
    adjacency = [0]*order
    for first, second in edges:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    return adjacency


def in_path(adjacency, subset, outside):
    neighbors = adjacency[outside] & subset
    return neighbors.bit_count() >= 2 or any(adjacency[neighbor] & subset
                                           for neighbor in vertices(neighbors))


def star_forming(adjacency, subset):
    outside = ((1 << len(adjacency))-1) ^ subset
    return all(in_path(adjacency, subset, vertex) for vertex in vertices(outside))


def parameters(adjacency):
    order = len(adjacency)
    independent = []
    minimal = []
    for subset in range(1 << order):
        if all((adjacency[vertex] & subset).bit_count() <= 1 for vertex in vertices(subset)):
            independent.append(subset)
        if star_forming(adjacency, subset) and all(
                not star_forming(adjacency, subset ^ (1 << vertex)) for vertex in vertices(subset)):
            minimal.append(subset)
    return max(map(int.bit_count, independent)), max(map(int.bit_count, minimal)), minimal


def check_graph(adjacency):
    dissociation, star_number, minimal_sets = parameters(adjacency)
    order = len(adjacency)
    high_degree_sets = 0
    for subset in minimal_sets:
        high = [vertex for vertex in vertices(subset)
                if (adjacency[vertex] & subset).bit_count() >= 2]
        if high:
            high_degree_sets += 1
        outside = ((1 << order)-1) ^ subset
        used = set()
        for essential in high:
            certificates = {vertex for vertex in vertices(outside)
                            if not in_path(adjacency, subset ^ (1 << essential), vertex)}
            assert certificates and not certificates & used
            used.update(certificates)
        assert len(high) <= outside.bit_count()
        assert 2*subset.bit_count() <= order+dissociation
    assert star_number <= (order+dissociation)//2
    return len(minimal_sets), high_degree_sets


def grid_controls():
    reports = []
    for rows, columns in itertools.product(range(1, 5), repeat=2):
        order = rows*columns
        edges = []
        for row, column in itertools.product(range(rows), range(columns)):
            vertex = row*columns+column
            if row+1 < rows:
                edges.append((vertex, vertex+columns))
            if column+1 < columns:
                edges.append((vertex, vertex+1))
        adjacency = adjacency_masks(order, edges)
        closed = [neighbors | (1 << vertex) for vertex, neighbors in enumerate(adjacency)]
        dissociation = domination = 0
        for subset in range(1 << order):
            size = subset.bit_count()
            if size > dissociation and all((adjacency[vertex] & subset).bit_count() <= 1
                                           for vertex in vertices(subset)):
                dissociation = size
            if size <= domination:
                continue
            witnesses = 0
            for neighborhood in closed:
                intersection = neighborhood & subset
                if not intersection:
                    break
                if not intersection & (intersection-1):
                    witnesses |= intersection
            else:
                if witnesses == subset:
                    domination = size
        formula = max(((rows+1)//2)*((2*columns+2)//3)+(rows//2)*(columns//3),
                      ((columns+1)//2)*((2*rows+2)//3)+(columns//2)*(rows//3))
        delta = max((rows % 2)*(columns-2*(columns//3)),
                    (columns % 2)*(rows-2*(rows//3)))
        assert domination == (order+1)//2 and dissociation == formula
        assert 2*(dissociation-domination) == delta-(order % 2)
        assert (dissociation == domination) == (
            rows % 2 == columns % 2 == 0 or rows in (1, 3) and columns in (1, 3))
        reports.append(dict(rows=rows, columns=columns, beta_2=dissociation,
                            Gamma=domination, gap=dissociation-domination))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    reports = []
    for order in range(1, 6):
        possible = list(itertools.combinations(range(order), 2))
        total_sets = high_sets = 0
        for edge_mask in range(1 << len(possible)):
            edges = [edge for index, edge in enumerate(possible) if edge_mask >> index & 1]
            minimal_sets, high_degree_sets = check_graph(adjacency_masks(order, edges))
            total_sets += minimal_sets
            high_sets += high_degree_sets
        reports.append(dict(order=order, graphs=1 << len(possible),
                            minimal_sets=total_sets, sets_with_high_degree_vertices=high_sets))
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)]
    dissociation, star_number, minimal_sets = parameters(adjacency_masks(6, edges))
    assert dissociation == star_number == 4
    assert (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) in minimal_sets
    check_graph(adjacency_masks(6, edges))
    root = Path(__file__).resolve().parents[1]
    grids = grid_controls()
    sources = [Path(__file__), root/'docs/STAR_FORMING_CERTIFICATES.md',
               root/'docs/GRID_PARAMETER_BRIDGES.md']
    report = dict(status='ALL_CHECKS_PASSED', all_graph_controls=reports,
                  labelled_graphs=sum(item['graphs'] for item in reports),
                  grid_controls=grids,
                  double_star=dict(order=6, edges=edges, beta_2=dissociation, SF_2=star_number,
                                   minimal_star_forming_sets=[list(vertices(subset)) for subset in minimal_sets]),
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls of the all-graph written proof. No bipartite equality proof or grid upper comparison is claimed.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'double_star'}, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
