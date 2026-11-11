"""Independent literal-star reconstruction of the height-three certificate.

This script does not import the C++ generator or its activity predicate.
It builds stars as literal three-vertex edge patterns, reconstructs both
complete vectors from the empty prefix, and checks every saved entry.
"""
from itertools import combinations
import json
from pathlib import Path
import hashlib

if not __debug__:
    raise RuntimeError('Verification requires assertions; run without -O.')

ROOT = Path(__file__).resolve().parents[1]


def grid(height, length):
    # Column-major labels agree with the public ternary serialization only.
    g = [set() for _ in range(height * length)]
    for c in range(length):
        for r in range(height):
            v = c * height + r
            for d, s in ((c - 1, r), (c + 1, r), (c, r - 1), (c, r + 1)):
                if 0 <= d < length and 0 <= s < height:
                    g[v].add(d * height + s)
    return g


def literal_stars(g, vertex):
    pairs = []
    for a, b in combinations((v for v in range(len(g)) if v != vertex), 2):
        if ((a in g[vertex]) + (b in g[vertex]) + (b in g[a])) >= 2:
            pairs.append((1 << a) | (1 << b))
    return pairs


def failure_tables(height):
    g = grid(height, 5)
    centre = list(range(2 * height, 3 * height))
    stars = [literal_stars(g, x) for x in centre]
    formed = [sum(1 << i for i, pairs in enumerate(stars)
                  if any(mask & s == s for s in pairs))
              for mask in range(1 << len(g))]
    kernel = []
    for mask in range(1 << len(g)):
        witness = 0
        valid = True
        for i, x in enumerate(centre):
            if mask >> x & 1:
                if not (formed[mask ^ (1 << x)] >> i & 1):
                    witness |= 1 << x
            else:
                if not (formed[mask] >> i & 1):
                    valid = False
                    break
                for v in range(len(g)):
                    if mask >> v & 1 and not (formed[mask ^ (1 << v)] >> i & 1):
                        witness |= 1 << v
        kernel.append(witness if valid else None)
    return kernel


def step(state, new_column, height, kernel, actual_centre):
    selected, marked = state
    window = selected | (new_column << (4 * height))
    added = kernel[window] if actual_centre else 0
    if added is None:
        return None
    flags = marked | added
    oldest = (1 << height) - 1
    if (window & oldest) != (flags & oldest):
        return None
    return window >> height, flags >> height


def closes(state, height, kernel, length):
    # Four absent columns flush all actual vertices. Their centres are
    # processed only when the global column index is in the original board.
    for extra in range(4):
        centre = length + extra - 2
        state = step(state, 0, height, kernel, 0 <= centre < length)
        if state is None:
            return False
    return state == (0, 0)


def encode(state, vertices):
    selected, marked = state
    code, power = 0, 1
    assert marked & ~selected == 0
    for v in range(vertices):
        code += ((selected >> v & 1) + (marked >> v & 1)) * power
        power *= 3
    return code


def prefix_vectors(height, limit, kernel):
    table = {(0, 0): 0}
    values, saved = [], {}
    for length in range(1, limit + 1):
        new = {}
        for state, score in table.items():
            for column in range(1 << height):
                target = step(state, column, height, kernel, length >= 3)
                if target is not None:
                    new[target] = max(new.get(target, -1), score + column.bit_count())
        table = new
        values.append(max(score for state, score in table.items()
                          if closes(state, height, kernel, length)))
        if length in (12, 15):
            saved[length] = {encode(state, 4 * height): score
                             for state, score in table.items()}
    return values, saved


def literal_board_control(height, length, kernel):
    g = grid(height, length)
    stars = [literal_stars(g, x) for x in range(len(g))]
    forms = []
    best, minimal_count = -1, 0
    for mask in range(1 << len(g)):
        formed = all(mask >> x & 1 or any(mask & s == s for s in pairs)
                     for x, pairs in enumerate(stars))
        forms.append(formed)
        minimal = formed and all(not forms[mask ^ (1 << v)]
                                 for v in range(len(g)) if mask >> v & 1)
        state = (0, 0)
        for c in range(length):
            state = step(state, mask >> (c * height) & ((1 << height) - 1),
                         height, kernel, c >= 2)
            if state is None:
                break
        accepted = state is not None and closes(state, height, kernel, length)
        assert minimal == accepted, (height, length, mask)
        if minimal:
            minimal_count += 1
            best = max(best, mask.bit_count())
    return {'height': height, 'length': length, 'subsets': 1 << len(g),
            'minimal_sets': minimal_count, 'SF': best}


def read_certificate(length):
    path = ROOT / f'output/grid-star-h3-v{length}.tsv'
    rows = [tuple(map(int, line.split())) for line in path.read_text().splitlines()]
    assert rows == sorted(rows)
    assert len({state for state, _ in rows}) == len(rows)
    assert all(0 <= state < 3**12 for state, _ in rows)
    return dict(rows)


def main():
    controls = []
    three_kernel = None
    for height, bound in ((1, 10), (2, 6), (3, 5)):
        kernel = failure_tables(height)
        if height == 3:
            three_kernel = kernel
        for length in range(1, bound + 1):
            controls.append(literal_board_control(height, length, kernel))
    values, saved = prefix_vectors(3, 15, three_kernel)
    expected = [5 * (n // 3) + 2 * (n % 3) for n in range(1, 16)]
    assert values == expected
    for length in (12, 15):
        assert saved[length] == read_certificate(length)
    assert saved[12].keys() == saved[15].keys()
    assert all(saved[15][state] == score + 5 for state, score in saved[12].items())
    generator = json.loads((ROOT / 'output/grid-star-transfer-h3.json').read_text())
    assert generator['optima'] == values and generator['translation_checked']
    report = {
        'status': 'PASS', 'literal_star_kernel_patterns': 2**5 + 2**10 + 2**15,
        'literal_board_controls': controls,
        'literal_board_subsets': sum(c['subsets'] for c in controls),
        'per_subset_transfer_acceptance_comparisons': sum(c['subsets'] for c in controls),
        'reconstructed_prefix_lengths': 15, 'optima': values,
        'full_state_domain': 3**12, 'reachable_certificate_states': len(saved[12]),
        'start': 12, 'period': 3, 'increment': 5,
        'complete_vectors_rebuilt_from_empty': True,
        'new_Lean': False,
        'certificate_sha256': {
            f'grid-star-h3-v{n}.tsv': hashlib.sha256(
                (ROOT / f'output/grid-star-h3-v{n}.tsv').read_bytes()).hexdigest()
            for n in (12, 15)}}
    (ROOT / 'output/grid-star-transfer-check.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
