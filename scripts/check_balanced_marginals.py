"""Independent local auxiliary-support controls for balanced witness marginals."""
from fractions import Fraction
from pathlib import Path
import json


def check(h, cyclic):
    assert not cyclic or h % 2 == 0
    q = {}
    for i in range(h if cyclic else h-1):
        a, b = 2*i+1, 2*((i+1) % h)
        q[a], q[b] = b, a
    marginals = {x: Fraction(0) for x in range(2*h)}
    expected_size = Fraction(0); cases = 0
    for side in (0, 1):
        indices = [i for i in range(h) if i % 2 == side]
        k = len(indices)
        if cyclic:
            supports = [{indices[(start+2*j) % k] for j in range(k//2)} for start in range(k)]
        else:
            supports = [set(indices[parity::2]) for parity in (0, 1)]
        for J in supports:
            assert all(not ({i, (i+2) % h} <= J) for i in J) if cyclic else all(i+2 not in J for i in J)
            probability = Fraction(1, 2*len(supports))
            chosen = {x for i in J for x in (2*i, 2*i+1)}
            expected_X = {x: Fraction(int(x in chosen)) for x in range(2*h)}
            for i in range(h):
                if i % 2 == side: continue
                pair = {2*i, 2*i+1}
                available = {x for x in pair if q.get(x) not in chosen}
                assert available
                # At a path endpoint use the matched witness when available.
                # An isolated helper and an unblocked cycle pair use a fair choice.
                inside = available & set(q)
                if not cyclic and len(pair & set(q)) == 1 and inside:
                    distribution = {next(iter(inside)): Fraction(1)}
                else:
                    distribution = {x: Fraction(1, len(available)) for x in available}
                for x, p in distribution.items(): expected_X[x] += p
            for x, p in expected_X.items(): marginals[x] += probability*p
            # Owner side has2*number of same-colour helpers; all helpers exceptJ.
            size = 2*len(indices)+h-len(J)+sum(expected_X.values())
            expected_size += probability*size
            cases += 1
    odd = cyclic and (h//2) % 2 == 1
    assert max(marginals.values()) <= Fraction(1, 2)
    assert expected_size == Fraction(11*h, 4)-Fraction(int(odd), 2)
    return {'helpers': h, 'cyclic': cyclic, 'support_cases': cases,
            'max_witness_marginal': str(max(marginals.values())),
            'expected_size': str(expected_size)}


rows = [check(h, False) for h in range(1, 65)]
rows += [check(h, True) for h in range(2, 65, 2)]
report = {'status': 'PASS', 'models': len(rows),
          'support_cases': sum(x['support_cases'] for x in rows), 'rows': rows,
          'scope': '96 local auxiliary path/cycle shapes,1312physical-side/support cases through64helpers; exact witness marginals and mean cardinalities, including quotientloops/parallelcases and endpoints. General proof is separate; no all-template or large-optimum claim.'}
(Path(__file__).resolve().parents[1]/'output/balanced-marginals-check.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: v for k, v in report.items() if k != 'rows'}))
