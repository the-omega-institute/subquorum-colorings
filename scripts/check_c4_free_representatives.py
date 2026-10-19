"""Independent finite controls for the general C4-free pair-packing proof."""

import argparse
from collections import deque
from functools import lru_cache
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def projective_plane(prime):
    representatives = []
    for vector in product(range(prime), repeat=3):
        first = next((entry for entry in vector if entry), None)
        if first == 1:
            representatives.append(vector)
    size = len(representatives)
    assert size == prime * prime + prime + 1
    adjacency = [set() for vertex in range(2 * size)]
    for point, vector in enumerate(representatives):
        for line, normal in enumerate(representatives):
            if sum(first * second for first, second in zip(vector, normal)) % prime == 0:
                adjacency[point].add(size + line)
                adjacency[size + line].add(point)
    return adjacency, set(range(size)), set(range(size, 2 * size))


def mobius_kantor():
    adjacency = [set() for vertex in range(16)]
    for index in range(8):
        for first, second in ((index, (index + 1) % 8),
                              (index, 8 + index),
                              (8 + index, 8 + (index + 3) % 8)):
            adjacency[first].add(second)
            adjacency[second].add(first)
    colors = {0: 0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in colors:
                colors[neighbor] = 1 - colors[vertex]
                queue.append(neighbor)
            assert colors[neighbor] != colors[vertex]
    return adjacency, {vertex for vertex in colors if colors[vertex] == 0}, {
        vertex for vertex in colors if colors[vertex] == 1}


def structural_control(adjacency, left, right, degree):
    assert left.isdisjoint(right) and left | right == set(range(len(adjacency)))
    assert len(left) == len(right)
    assert all(len(neighbors) == degree for neighbors in adjacency)
    assert all(vertex not in neighbors for vertex, neighbors in enumerate(adjacency))
    assert all(vertex in adjacency[neighbor] and ((vertex in left) != (neighbor in left))
               for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
    checked = 0
    for side in (left, right):
        for first, second in combinations(sorted(side), 2):
            assert len(adjacency[first] & adjacency[second]) <= 1
            checked += 1
    return checked


def subset_pair_controls(adjacency, side, other, degree):
    ordered = sorted(side)
    count = 0
    for mask in range(1 << len(ordered)):
        unused = {vertex for index, vertex in enumerate(ordered) if mask >> index & 1}
        neighbors = [len(adjacency[vertex] & unused) for vertex in other]
        eligible = [number for number in neighbors if number >= degree - 1]
        assert comb(degree - 1, 2) * len(eligible) <= comb(len(unused), 2)
        assert sum(comb(number, 2) for number in eligible) <= comb(len(unused), 2)
        count += 1
    return count


def exact_representatives(adjacency):
    order = len(adjacency)
    neighbors = [sum(1 << vertex for vertex in entries) for entries in adjacency]
    impossible = order + 1

    @lru_cache(maxsize=None)
    def cover(available, required):
        if not required:
            return 0
        vertex = (required & -required).bit_length() - 1
        options = neighbors[vertex] & available
        best = impossible
        while options:
            neighbor_bit = options & -options
            options -= neighbor_bit
            removed = (1 << vertex) | neighbor_bit
            best = min(best, 1 + cover(available & ~removed, required & ~removed))
        return best

    optimum = 0
    witness = None
    beta = 0
    for occupied in range(1 << order):
        required = sum(1 << vertex for vertex in range(order)
                       if occupied >> vertex & 1 and
                       (neighbors[vertex] & occupied).bit_count() >= 2)
        if not required:
            beta = max(beta, occupied.bit_count())
        matching_size = cover(occupied, required)
        objective = occupied.bit_count() - matching_size
        if objective > optimum:
            optimum = objective
            available = occupied
            pending = required
            matching = []
            while pending:
                vertex = (pending & -pending).bit_length() - 1
                options = neighbors[vertex] & available
                for neighbor in range(order):
                    if not options >> neighbor & 1:
                        continue
                    removed = (1 << vertex) | (1 << neighbor)
                    if 1 + cover(available & ~removed, pending & ~removed) == cover(available, pending):
                        matching.append([vertex, neighbor])
                        available &= ~removed
                        pending &= ~removed
                        break
                else:
                    raise AssertionError('Missing matching reconstruction')
            singletons = [vertex for vertex in range(order) if available >> vertex & 1]
            endpoints = [vertex for edge in matching for vertex in edge]
            assert len(endpoints) == len(set(endpoints))
            assert not set(endpoints) & set(singletons)
            assert all(second in adjacency[first] for first, second in matching)
            assert all((neighbors[vertex] & occupied).bit_count() <= 1 for vertex in singletons)
            assert len(singletons) + len(matching) == optimum
            witness = dict(singletons=singletons, matching=matching)
    return dict(order=order, occupied_sets=1 << order, beta=beta, omega=optimum,
                witness=witness, cover_states=cover.cache_info().currsize)


def heawood_star_control(adjacency):
    neighbors = [sum(1 << vertex for vertex in entries) for entries in adjacency]

    def forms(selected):
        for vertex, adjacent in enumerate(neighbors):
            if selected >> vertex & 1:
                continue
            selected_neighbors = adjacent & selected
            if selected_neighbors.bit_count() >= 2:
                continue
            if any(selected_neighbors >> center & 1 and neighbors[center] & selected
                   for center in range(len(adjacency))):
                continue
            return False
        return True

    forming = [forms(mask) for mask in range(1 << len(adjacency))]
    minimal = [mask for mask, valid in enumerate(forming) if valid and
               all(not forming[mask ^ (1 << vertex)] for vertex in range(len(adjacency))
                   if mask >> vertex & 1)]
    maximum = max(mask.bit_count() for mask in minimal)
    assert maximum == 8
    witness = next(mask for mask in minimal if mask.bit_count() == maximum)
    return dict(sf=maximum, subsets=len(forming),
                selected=[vertex for vertex in range(len(adjacency)) if witness >> vertex & 1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    planes = []
    for prime in (2, 3, 5, 7):
        adjacency, left, right = projective_plane(prime)
        pairs = structural_control(adjacency, left, right, prime + 1)
        assert all(len(adjacency[first] & adjacency[second]) == 1
                   for side in (left, right) for first, second in combinations(side, 2))
        subsets = 0
        if prime <= 3:
            subsets += subset_pair_controls(adjacency, left, right, prime + 1)
            subsets += subset_pair_controls(adjacency, right, left, prime + 1)
        size = len(left)
        assert size <= 2 * prime * (prime - 1) + 4
        record = dict(q=prime, part_size=size, degree=prime + 1,
                      common_neighbor_pairs=pairs, exhaustive_unused_subsets=subsets)
        if prime == 2:
            record['exact_parameters'] = exact_representatives(adjacency)
            record['exact_star_forming'] = heawood_star_control(adjacency)
            assert record['exact_parameters']['omega'] == record['exact_parameters']['beta'] == size
        planes.append(record)
    adjacency, left, right = mobius_kantor()
    structural_control(adjacency, left, right, 3)
    exact = exact_representatives(adjacency)
    assert exact['omega'] == exact['beta'] == len(left) == 8
    arithmetic_cases = 0
    for capacity in range(1, 41):
        for unused in range(100):
            for excess in range(1, 11):
                if capacity * (unused + excess) <= unused * (unused - 1):
                    assert unused >= capacity + 2
                arithmetic_cases += 1
    receipt = dict(status='ALL_CHECKS_PASSED', planes=planes, mobius_kantor=exact,
                   arithmetic_cases=arithmetic_cases,
                   scope='Finite controls only. Exact Omega exhausts occupied sets and minimizes internal matching size covering every occupied vertex of induced degree at least two; unmatched vertices are T. General pair-packing and all-projective-plane theorems have written proofs, not enumeration premises.')
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
