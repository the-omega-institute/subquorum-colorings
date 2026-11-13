"""Independent finite checks for the two-C10 owner completion lemma.

The general argument is written in docs/TWO_C10_LOCAL_COMPLETION.md. This
module keeps the finite contact classification and the physical controls
independent of the C20 candidate implementation.
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for i in range(1, len(vertices)):
        second = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def cyclic_equal_edges(bits, offset):
    return sum(
        bits[offset + i] == bits[offset + (i + 1) % 5] for i in range(5)
    )


def contact_solutions(contact):
    return tuple(
        bits
        for bits in itertools.product((0, 1), repeat=10)
        if all(bits[a] != bits[b] for a, b in contact)
    )


@dataclass(frozen=True)
class ContactClass:
    cross_edges: int
    solutions: tuple
    both_cycles_good: bool
    owner0_bad_solution: bool
    owner1_bad_solution: bool


def classify_contact(contact):
    cross = sum((a < 5) != (b < 5) for a, b in contact)
    solutions = contact_solutions(contact)
    scores = {
        (cyclic_equal_edges(bits, 0), cyclic_equal_edges(bits, 5))
        for bits in solutions
    }
    good = any(a <= 1 and b <= 1 for a, b in scores)
    return ContactClass(
        cross_edges=cross,
        solutions=solutions,
        both_cycles_good=good,
        owner0_bad_solution=any(a == 3 and b <= 1 for a, b in scores),
        owner1_bad_solution=any(a <= 1 and b == 3 for a, b in scores),
    )


def legal_owner_mask(mask, length=10):
    """Every three consecutive owner vertices contain an omission."""
    return all(
        ((mask >> i) & 1)
        or ((mask >> ((i + 1) % length)) & 1)
        or ((mask >> ((i + 2) % length)) & 1)
        for i in range(length)
    )


def repair_cost(mask, length=10):
    missing = ((1 << length) - 1) ^ mask
    best = length + 1
    sub = missing
    while True:
        final_mask = mask | sub
        if (
            legal_owner_mask(final_mask, length)
            and sum((final_mask >> i) & 1 for i in range(0, length, 2)) <= 4
            and sum((final_mask >> i) & 1 for i in range(1, length, 2)) <= 4
        ):
            best = min(best, sub.bit_count())
        if sub == 0:
            return best
        sub = (sub - 1) & missing


def four_phase_repair_certificate(contact0, contact1):
    """Find four complementary phase states with average repair at most one."""
    solutions0 = contact_solutions(contact0)
    solutions1 = contact_solutions(contact1)
    for bits0 in solutions0:
        for bits1 in solutions1:
            costs = []
            for phase0 in (0, 1):
                for phase1 in (0, 1):
                    owner0 = sum(
                        (bits0[i] ^ phase0) << (2 * i) for i in range(5)
                    )
                    owner0 |= sum(
                        (bits1[i] ^ phase1) << (2 * i + 1) for i in range(5)
                    )
                    owner1 = sum(
                        (bits0[5 + i] ^ phase0) << (2 * i)
                        for i in range(5)
                    )
                    owner1 |= sum(
                        (bits1[5 + i] ^ phase1) << (2 * i + 1)
                        for i in range(5)
                    )
                    costs.append(repair_cost(owner0) + repair_cost(owner1))
            if sum(costs) <= 4:
                return {
                    "costs": costs,
                    "average": sum(costs) / 4,
                    "bits0": bits0,
                    "bits1": bits1,
                }
    return None


def bipartition(vertex_count, edges):
    graph = [[] for _ in range(vertex_count)]
    for left, right in edges:
        graph[left].append(right)
        graph[right].append(left)
    colour = [None] * vertex_count
    for start in range(vertex_count):
        if colour[start] is not None:
            continue
        colour[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in graph[vertex]:
                if colour[neighbour] is None:
                    colour[neighbour] = 1 - colour[vertex]
                    stack.append(neighbour)
                elif colour[neighbour] == colour[vertex]:
                    return None
    return colour


def matching_number(vertex_count, edges, selected, colour):
    selected = set(selected)
    adjacency = {v: [] for v in selected if colour[v] == 0}
    for left, right in edges:
        if left not in selected or right not in selected:
            continue
        if colour[left] == 0:
            adjacency[left].append(right)
        else:
            adjacency[right].append(left)
    mate = {}

    def augment(vertex, seen):
        for neighbour in adjacency[vertex]:
            if neighbour in seen:
                continue
            seen.add(neighbour)
            if neighbour not in mate or augment(mate[neighbour], seen):
                mate[neighbour] = vertex
                return 1
        return 0

    return sum(augment(vertex, set()) for vertex in adjacency)


def random_matching(vertices, rng):
    vertices = list(vertices)
    rng.shuffle(vertices)
    return [(vertices[i], vertices[i + 1]) for i in range(0, len(vertices), 2)]


def minimum_owner_sets(cycle):
    size = (len(cycle) + 2) // 3
    return tuple(
        frozenset(choice)
        for choice in itertools.combinations(cycle, size)
        if legal_owner_mask(
            sum(1 << cycle.index(vertex) for vertex in choice), len(cycle)
        )
    )


def physical_sample(k, seed, models):
    """Run finite controls for B=2C10 plus k owner squares."""
    rng = random.Random(seed)
    n = 20 + 4 * k
    cycles = [list(range(10)), list(range(10, 20))]
    cycles += [list(range(20 + 4 * i, 24 + 4 * i)) for i in range(k)]
    options = [minimum_owner_sets(cycle) for cycle in cycles]
    physical_colour = [
        index % 2 for cycle in cycles for index in range(len(cycle))
    ]
    target = (k + 7) // 2
    accepted = 0
    skipped_nonbipartite = 0
    observed = []

    for _ in range(models):
        P = []
        for bit in (0, 1):
            P.extend(
                random_matching(
                    [v for v, colour in enumerate(physical_colour) if colour == bit],
                    rng,
                )
            )
        left = [v for v, colour in enumerate(physical_colour) if colour == 0]
        right = [v for v, colour in enumerate(physical_colour) if colour == 1]
        rng.shuffle(left)
        rng.shuffle(right)
        q_size = rng.randrange(0, len(left) + 1)
        Q = list(zip(left[:q_size], right[:q_size]))
        edges = P + Q
        colour = bipartition(n, edges)
        if colour is None:
            skipped_nonbipartite += 1
            continue

        minimum = n
        for choices in itertools.product(*options):
            selected = set().union(*choices)
            minimum = min(
                minimum, matching_number(n, edges, selected, colour)
            )
        if minimum > target:
            raise AssertionError(
                f"local bound failed for k={k}: {minimum}>{target}"
            )
        accepted += 1
        observed.append(minimum)

    return {
        "k": k,
        "models_requested": models,
        "bipartite_models": accepted,
        "skipped_nonbipartite": skipped_nonbipartite,
        "target": target,
        "maximum_observed_minimum": max(observed, default=None),
        "minimum_observed_minimum": min(observed, default=None),
    }
