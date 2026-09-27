"""Enumerate every matching and every allowed T on small grids, independently."""
import csv
import json
from pathlib import Path


def brute_omega(height, width):
    count = height * width
    neighbors = [0] * count
    for r in range(height):
        for c in range(width):
            v = r * width + c
            for a, b in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if 0 <= a < height and 0 <= b < width:
                    neighbors[v] |= 1 << (a * width + b)
    best = 0
    matchings = 0

    def visit(unprocessed, endpoints, size):
        nonlocal best, matchings
        if not unprocessed:
            matchings += 1
            available = ((1 << count) - 1) ^ endpoints
            selected = available
            while True:
                occupied = endpoints | selected
                if all(not (selected >> v & 1) or
                       (neighbors[v] & occupied).bit_count() <= 1
                       for v in range(count)):
                    best = max(best, size + selected.bit_count())
                if not selected:
                    break
                selected = (selected - 1) & available
            return
        v_bit = unprocessed & -unprocessed
        v = v_bit.bit_length() - 1
        rest = unprocessed ^ v_bit
        visit(rest, endpoints, size)
        partners = neighbors[v] & rest
        while partners:
            u_bit = partners & -partners
            partners ^= u_bit
            visit(rest ^ u_bit, endpoints | v_bit | u_bit, size + 1)

    visit((1 << count) - 1, 0, 0)
    return best, matchings


def main():
    results = []
    for m, n in [(1, 1), (1, 5), (2, 2), (2, 3), (2, 5), (3, 3), (3, 4)]:
        value, count = brute_omega(m, n)
        rows = {int(r['length']): r for r in csv.DictReader(
            (Path('results') / f'omega-w{m}.csv').open())}
        assert value == int(rows[n]['omega'])
        results.append(dict(width=m, length=n, omega=value,
                            matchings_enumerated=count, agrees=True))
    Path('results/small-exhaustive-check.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
