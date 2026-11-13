#!/usr/bin/env python3
"""Exact finite-state certificate for four-row representative pairs.

Labels are B (unused), T (selected), and P (a matching endpoint).  A
matching endpoint is either matched to the previous or next column or is
paired vertically inside its column.  The transfer checks the occupied
neighbour condition for T vertices when their right neighbour becomes known.

The script also runs an independent literal matching/subset enumeration on
the first three boards.  It proves the two translation identities used by
the accompanying note for the unrestricted and boundary-constrained
transfers.
"""

from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path


HEIGHT = 4
B, T, P = range(3)


def occupied_mask(labels: tuple[int, ...]) -> int:
    return sum((label != B) << row for row, label in enumerate(labels))


def vertical_edges(
    labels: tuple[int, ...], left_match: int, right_match: int
) -> int | None:
    """Return the forced vertical matching size, or None if impossible."""

    remaining = [
        row
        for row, label in enumerate(labels)
        if label == P
        and not (left_match >> row & 1)
        and not (right_match >> row & 1)
    ]
    used: set[int] = set()
    edges = 0
    for row in remaining:
        if row in used:
            continue
        if row + 1 in remaining and row + 1 not in used:
            used.update((row, row + 1))
            edges += 1
        else:
            return None
    return edges


def base_counts(
    labels: tuple[int, ...], left_occupied: int,
    left_match: int, right_match: int
) -> tuple[int, ...] | None:
    if vertical_edges(labels, left_match, right_match) is None:
        return None
    if any(
        ((left_match >> row) & 1) and labels[row] != P
        for row in range(HEIGHT)
    ):
        return None
    if any(
        ((right_match >> row) & 1) and labels[row] != P
        for row in range(HEIGHT)
    ):
        return None
    if left_match & right_match:
        return None

    occupied = occupied_mask(labels)
    counts = [0] * HEIGHT
    for row, label in enumerate(labels):
        if label != T:
            continue
        counts[row] = (
            (row > 0 and bool(occupied >> (row - 1) & 1))
            + (row + 1 < HEIGHT and bool(occupied >> (row + 1) & 1))
            + bool(left_occupied >> row & 1)
        )
        if counts[row] > 1:
            return None
    return tuple(counts)


State = tuple[tuple[int, ...], int, int, int, int]


def allowed_column(kind: str, column: int, labels: tuple[int, ...]) -> bool:
    if kind == "free":
        return True
    if kind == "bottom-even-empty":
        return column % 2 == 1 or labels[HEIGHT - 1] == B
    raise ValueError(kind)


def transfer(kind: str, columns: int) -> tuple[int, dict[State, int], list[int]]:
    """Run the exact transfer and return the terminal optimum and vectors."""

    dp: dict[State, int] = {}
    for labels in product(range(3), repeat=HEIGHT):
        if not allowed_column(kind, 0, labels):
            continue
        for right_match in range(1 << HEIGHT):
            if base_counts(labels, 0, 0, right_match) is None:
                continue
            occupied = occupied_mask(labels)
            score = labels.count(T) + vertical_edges(labels, 0, right_match)
            state: State = (labels, occupied, 0, 0, right_match)
            dp[state] = max(dp.get(state, -10**9), score)

    state_counts = [len(dp)]
    for column in range(1, columns):
        nxt: dict[State, int] = {}
        for (
            previous, previous_occupied, previous_left_occupied,
            previous_left, previous_right
        ), score in dp.items():
            previous_base = base_counts(
                previous, previous_left_occupied, previous_left, previous_right
            )
            if previous_base is None:
                raise AssertionError("invalid retained state")
            for labels in product(range(3), repeat=HEIGHT):
                if not allowed_column(kind, column, labels):
                    continue
                left_match = previous_right
                occupied = occupied_mask(labels)
                if any(
                    ((left_match >> row) & 1) and labels[row] != P
                    for row in range(HEIGHT)
                ):
                    continue
                if any(
                    previous[row] == T
                    and previous_base[row] + bool(occupied >> row & 1) > 1
                    for row in range(HEIGHT)
                ):
                    continue
                for right_match in range(1 << HEIGHT):
                    if base_counts(
                        labels, previous_occupied, left_match, right_match
                    ) is None:
                        continue
                    next_state: State = (
                        labels, occupied, previous_occupied,
                        left_match, right_match
                    )
                    value = (
                        score
                        + labels.count(T)
                        + vertical_edges(labels, left_match, right_match)
                        + left_match.bit_count()
                    )
                    if value > nxt.get(next_state, -10**9):
                        nxt[next_state] = value
        dp = nxt
        state_counts.append(len(dp))

    optimum = max(
        score for (
            labels, occupied, left_occupied, left_match, right_match
        ), score in dp.items()
        if right_match == 0
    )
    return optimum, dp, state_counts


def transfer_vectors(kind: str, first: int, second: int) -> dict[str, object]:
    first_optimum, first_vector, first_counts = transfer(kind, first)
    second_optimum, second_vector, second_counts = transfer(kind, second)
    if set(first_vector) != set(second_vector):
        raise AssertionError(f"support changed for {kind}")
    increment = second_optimum - first_optimum
    if any(second_vector[state] != score + increment for state, score in first_vector.items()):
        raise AssertionError(f"vector translation failed for {kind}")
    return {
        "kind": kind,
        "first_length": first,
        "second_length": second,
        "translation_increment": increment,
        "first_optimum": first_optimum,
        "second_optimum": second_optimum,
        "first_states": len(first_vector),
        "second_states": len(second_vector),
        "first_state_counts": first_counts,
        "second_state_counts": second_counts,
        "support_translates": True,
    }


def grid(h: int, width: int) -> tuple[list[int], list[tuple[int, int]]]:
    vertices = h * width
    adjacency = [0] * vertices
    edges: list[tuple[int, int]] = []

    def add(a: int, b: int) -> None:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
        edges.append((a, b))

    for column in range(width):
        for row in range(h - 1):
            add(column * h + row, column * h + row + 1)
        if column + 1 < width:
            for row in range(h):
                add(column * h + row, (column + 1) * h + row)
    return adjacency, edges


def matching_masks(edges: list[tuple[int, int]]) -> list[int]:
    masks: list[int] = []

    def visit(index: int, used: int) -> None:
        if index == len(edges):
            masks.append(used)
            return
        visit(index + 1, used)
        a, b = edges[index]
        bits = (1 << a) | (1 << b)
        if not used & bits:
            visit(index + 1, used | bits)

    visit(0, 0)
    return masks


def literal_optimum(width: int, boundary: bool) -> int:
    adjacency, edges = grid(HEIGHT, width)
    all_vertices = (1 << (HEIGHT * width)) - 1
    optimum = -1
    for endpoints in matching_masks(edges):
        for selected in range(all_vertices + 1):
            if selected & endpoints:
                continue
            if boundary and any(
                selected & (1 << (column * HEIGHT + HEIGHT - 1))
                or endpoints & (1 << (column * HEIGHT + HEIGHT - 1))
                for column in range(0, width, 2)
            ):
                continue
            occupied = selected | endpoints
            if any(
                selected >> vertex & 1
                and (adjacency[vertex] & occupied).bit_count() > 1
                for vertex in range(HEIGHT * width)
            ):
                continue
            optimum = max(optimum, selected.bit_count() + endpoints.bit_count() // 2)
    return optimum


def main() -> None:
    # The period-two boundary restriction requires a two-column operator.
    # Certify both parity classes: 4 -> 6 seeds the even widths and
    # 5 -> 7 seeds the odd widths. Complete vector translation, rather than
    # only terminal optima, is what makes the max-plus induction valid.
    unrestricted_even = transfer_vectors("free", 4, 6)
    unrestricted_odd = transfer_vectors("free", 5, 7)
    boundary_even = transfer_vectors("bottom-even-empty", 4, 6)
    boundary_odd = transfer_vectors("bottom-even-empty", 5, 7)
    for certificate in (
        unrestricted_even, unrestricted_odd, boundary_even, boundary_odd
    ):
        assert certificate["translation_increment"] == 4
    assert unrestricted_even["first_optimum"] == 8
    assert unrestricted_odd["first_optimum"] == 11
    assert boundary_even["first_optimum"] == 8
    assert boundary_odd["first_optimum"] == 10

    literal = []
    for width in range(1, 4):
        free = literal_optimum(width, False)
        constrained = literal_optimum(width, True)
        dp_free = transfer("free", width)[0]
        dp_constrained = transfer("bottom-even-empty", width)[0]
        assert (free, constrained) == (dp_free, dp_constrained)
        literal.append({
            "width": width,
            "literal_free": free,
            "literal_boundary": constrained,
            "transfer_free": dp_free,
            "transfer_boundary": dp_constrained,
        })

    report = {
        "status": "PASS",
        "scope": (
            "Exact representative-pair transfer for P4 square Pn and the "
            "bottom-even-empty boundary condition; literal controls through width 3."
        ),
        "unrestricted_even": unrestricted_even,
        "unrestricted_odd": unrestricted_odd,
        "boundary_even": boundary_even,
        "boundary_odd": boundary_odd,
        "literal_controls": literal,
        "translation_period": 2,
        "unrestricted_formula": "2*n + (n mod 2)",
        "boundary_formula": "2*n",
        "new_Lean": False,
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "output/grid-height-four-representative-check.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    report["report_sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
