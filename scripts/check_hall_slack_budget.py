"""Endpoint controls for arbitrary overlapping Hall regions and q>=1."""
from itertools import permutations
import json
from pathlib import Path
import random


def check():
    rng = random.Random(921111)
    counts = dict(graphs=0, saturating_graphs=0, potential_choices=0,
                  terminal_bijections=0, region_identities=0)
    for b in range(1, 4):
        for q in range(1, 4):
            t = b+q
            masks = range(1 << (b*t)) if b == 1 or (b == 2 and q == 1) else sorted(
                {rng.randrange(1 << (b*t)) for _ in range(16)} |
                {sum(1 << (j*t+j) for j in range(b))})
            for mask in masks:
                counts['graphs'] += 1
                ns = [{i for i in range(t) if mask >> (j*t+i) & 1} for j in range(b)]
                if not any(all(m[j] in ns[j] for j in range(b)) for m in permutations(range(t), b)):
                    continue
                counts['saturating_graphs'] += 1
                regions = []
                for dm in range(1, 1 << b):
                    d = {j for j in range(b) if dm >> j & 1}
                    f = set().union(*(ns[j] for j in d))
                    assert len(f) >= len(d)
                    regions.append((d, f))
                choices = [[(j, 1)] for j in range(len(regions))]
                choices.extend([[(a, 1), (c, 2)] for a in range(len(regions))
                                for c in range(a+1, len(regions))])
                choices.append([(j, 1+j % 3) for j in range(len(regions))])
                for choice in choices:
                    pb = [sum(w for j, w in choice if v in regions[j][0]) for v in range(b)]
                    pt = [sum(w for j, w in choice if v in regions[j][1]) for v in range(t)]
                    mu = max(pb)
                    slack = sum(w*(len(regions[j][1])-len(regions[j][0])) for j, w in choice)
                    assert sum(pt)-sum(pb) == slack
                    assert all(pt[v] >= pb[j] for j in range(b) for v in ns[j])
                    counts['potential_choices'] += 1
                    for r in ([q, q+1, q+2] if b+q <= 4 else [q, q+1]):
                        nb = b+r
                        # All bijections at order<=6; seeded permutations above that.
                        if nb <= 6:
                            assignments = permutations(range(nb))
                        else:
                            assignments = [rng.sample(range(nb), nb) for _ in range(48)]
                        for pi in assignments:
                            k = sum(v >= b for v in pi[:t])
                            hh = [v for v in pi[t:] if v < b]
                            assert k >= q and len(hh) == k-q
                            a = l = compensation = root = nontrivial = 0
                            for v, dest in enumerate(pi[:t]):
                                p = pb[dest] if dest < b else 0
                                a += max(0, pt[v]-p)
                                l += max(0, p-pt[v])
                                compensation += p > pt[v]
                                nontrivial += dest >= b or v not in ns[dest]
                                if dest >= b:
                                    root += pt[v]
                                if p > pt[v]:
                                    assert dest < b and v not in ns[dest]
                            assert a-l == slack+sum(pb[v] for v in hh)
                            assert slack <= a-l <= slack+(k-q)*mu
                            extra = max(0, (a-slack-(k-q)*mu+mu-1)//mu)
                            assert compensation >= extra
                            assert nontrivial >= k+extra
                            assert a >= root
                            counts['terminal_bijections'] += 1
                            counts['region_identities'] += len(choice)
    return dict(status='PASS', **counts,
                scope='Arbitrary terminal bijections; q>=1 and non-tight, overlapping or nested neighbourhoods. No geometric realizability is inferred.')


if __name__ == '__main__':
    report = check()
    Path('output/hall-slack-budget-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
