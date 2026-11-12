#!/usr/bin/env python3
"""Independent small-block/exact graph and rational fixed-extraction controls."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from fractions import Fraction
import argparse, hashlib, json, random, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from sharp_all_helper import physical, odd_path_ledger
from all_helper_optimization import solve
from owner_matching_certificate import lift_certificate
from subcubic_partial_template import decompose
if not __debug__: raise RuntimeError('Assertions must be enabled')
counts = Counter(); digest = hashlib.sha256()


def diss(g, D): return all(len(g[v]&D) <= 1 for v in D)


def literal_beta(g):
    best = 0
    for mask in range(1 << len(g)):
        D = {v for v in range(len(g)) if mask >> v & 1}
        if diss(g, D): best = max(best, len(D))
        counts['literal_small_graph_subsets'] += 1
    return best


def bipartite_beta(g, left):
    """Enumerate one side; independently proved private-neighbour identity."""
    right = sorted(set(range(len(g)))-set(left))
    loc = {v:i for i, v in enumerate(left)}
    adj = [sum(1 << loc[v] for v in g[u]) for u in right]
    assert all(not (g[v]&set(left)) for v in left)
    assert all(not (g[u]&set(right)) for u in right)
    best, best_D = -1, None
    for mask in range(1 << len(left)):
        zero, private = [], {}
        for u, ns in zip(right, adj):
            selected = ns & mask
            if not selected: zero.append(u)
            elif selected.bit_count() == 1: private[selected] = u
        D = {v for j, v in enumerate(left) if mask >> j & 1}
        D.update(zero); D.update(private.values())
        assert diss(g, D)
        if len(D) > best: best, best_D = len(D), sorted(D)
        counts['one_part_subsets'] += 1
    return best, best_D


def forms(g, S):
    """Literal noninduced K1,2 membership, independent of degree shortcut."""
    return all(any(x in {c,a,b} and len({c,a,b}&S) == 2
                   for c in {x}|g[x] for a,b in combinations(g[c], 2))
               for x in set(range(len(g)))-S)


def ledger_controls(g, S, beta, colour):
    w = decompose(g,S)
    D,rec = lift_certificate(g,S,w,beta,colour)
    if D is None: return
    assert diss(g,D)
    o = rec['template']['prepared']['odd_paths']; bp = rec['bprime']
    values = {Fraction(k,4) for k in range(5)}
    values.add(Fraction(o,2*bp) if bp else Fraction(1))
    for gamma in sorted(values):
        if o < 2*gamma*bp: continue
        r = odd_path_ledger(len(g),w['a'],len(w['triples']),len(w['pairs']),
            len(w['R']),w['b'],w['b3'],len(S),beta,rec['L'],o,gamma)
        assert r['gap_upper'] >= len(S)-beta
        digest.update(json.dumps(r,sort_keys=True).encode())
        counts['physical_odd_path_ledger_checks'] += 1
    counts['physical_extractions'] += 1
    counts['positive_odd_path_extractions'] += bool(o)


def main():
    model = json.loads((ROOT/'develop/fixtures/sharp-all-helper-thirty.json').read_text())
    g, colour = physical(model); n = len(g); b = model['b']
    assert n == 30 and sum(map(len,g))//2 == 42
    assert min(map(len,g)) == 2 and max(map(len,g)) == 3
    seen = {0}; todo = [0]
    while todo:
        for u in g[todo.pop()]-seen: seen.add(u); todo.append(u)
    assert len(seen) == n
    assert sum(c == 0 for c in colour) == 15
    expected_edges = {frozenset(e) for order in model['owner_cycles']
                      for e in zip(order, order[1:]+order[:1])}
    assert expected_edges == set(map(frozenset, model['B']))
    D = set(range(b)) | {b+v for v in model['all_helper_witnesses']} | {
        3*b+v for v in model['all_helper_owners']}
    assert len(D) == 16 and diss(g, D)
    assert len(model['unrestricted_witness']) == 17 and diss(g, set(model['unrestricted_witness']))
    assert solve(b, model['P'], model['Q'], model['B'])['beta_I'] == 16
    # Independent literal choices: all A-independent witness sets and all
    # dissociating owner sets. No matching reduction is used for this maximum.
    V = set(range(2*b)); owner_adj = [set() for _ in V]
    for a,c in model['B']: owner_adj[a].add(c); owner_adj[c].add(a)
    independent = []
    for mask in range(1 << (2*b)):
        if all(not (mask >> a & 1 and mask >> c & 1) for a,c in model['P']+model['Q']):
            independent.append(mask)
    forced = 0
    for mask in range(1 << (2*b)):
        S = {v for v in V if mask >> v & 1}
        if not diss(owner_adj, S): continue
        for T in independent:
            if mask & T: continue
            forced = max(forced, b+mask.bit_count()+T.bit_count())
            counts['literal_owner_witness_choices'] += 1
    assert forced == 16 and len(independent) == 343
    # Complete maximal cost<=1 obstruction: 3 charged locations, 4 singleton
    # complements in it, and 2 opposite-pair complements in each other square.
    for charged in range(3):
        others = [j for j in range(3) if j != charged]
        for singleton, phases in product(range(4), product((0,1), repeat=2)):
            S = {4*charged+singleton}
            for j,p in zip(others, phases): S.update((4*j+p, 4*j+p+2))
            bad = [v for v in S if len(owner_adj[v]&S) >= 2]
            assert bad
            counts['analytic_maximal_cost_one_cases'] += 1
    # Literal ten-vertex checks support the general written three-block proof.
    for j in range(3):
        block = [2*j,2*j+1]+list(range(6+4*j,10+4*j))+list(range(18+4*j,22+4*j))
        best = 0; maxima = 0
        for mask in range(1 << 10):
            D = {v for k,v in enumerate(block) if mask >> k & 1}
            counts['literal_ten_vertex_subsets'] += 1
            if not diss(g,D): continue
            best = max(best, len(D))
            if j < 2 and len(D) == 6:
                pairs = [(18+4*j,20+4*j),(19+4*j,21+4*j)]
                assert any({a,c} <= D for a,c in pairs); maxima += 1
            if j == 2:
                owners = D & set(range(26,30))
                assert len(owners) > 2 or len(D) <= 6
                assert owners or len(D) <= 4
        assert best == (6 if j < 2 else 7)
        if j < 2: assert maxima == 11
    for side in (0,1):
        exact, witness = bipartite_beta(g, [v for v in range(n) if colour[v] == side])
        assert exact == 17
        digest.update(json.dumps([side,exact,witness],sort_keys=True).encode())
    canonical = set(range(6)) | set(range(18,30))
    assert forms(g,canonical) and all(not forms(g,canonical-{v}) for v in canonical)
    counts['literal_canonical_deletions'] += len(canonical)
    # Nonempty extracted templates, including genuine odd-path surplus.
    for b0 in (4,6):
        n0 = 2*b0
        P = [(v,v+1) for v in range(0,n0,2)]
        col = [(v//2)%2 for v in range(n0)]
        Q = [(v,(v+1)%n0) for v in range(1,n0,2)]
        order = [v for pair in zip([v for v in range(n0) if col[v]==0],
                                  [v for v in range(n0) if col[v]==1]) for v in pair]
        for cut in range(5):
            B = [(order[j],order[j+1]) for j in range(n0-1-cut)]
            h,c = physical(dict(b=b0,P=P,Q=Q,B=B,index_colours=col))
            S = set(range(b0)) | set(range(3*b0,5*b0))
            assert forms(h,S) and all(not forms(h,S-{v}) for v in S)
            beta,_ = bipartite_beta(h,[v for v in range(len(h)) if c[v]==0])
            ledger_controls(h,S,beta,dict(enumerate(c)))
            counts['nonempty_template_graphs'] += 1
    # Every binary bipartite graph with both sides<=3; n<=6. Literal beta
    # validates the independently implemented one-part optimization formula.
    for left_size in range(4):
        for right_size in range(4):
            n0 = left_size+right_size
            es = list(product(range(left_size),range(left_size,n0)))
            for mask in range(1 << len(es)):
                h = [set() for _ in range(n0)]
                for k,(a,c) in enumerate(es):
                    if mask >> k & 1: h[a].add(c); h[c].add(a)
                beta = literal_beta(h)
                assert bipartite_beta(h,list(range(left_size)))[0] == beta
                # All minimal forming sets are independently literal; this
                # supplies actual graph/witness-extraction ledger controls.
                for M in range(1 << n0):
                    S = {v for v in range(n0) if M >> v & 1}
                    if not forms(h,S) or any(forms(h,S-{v}) for v in S): continue
                    ledger_controls(h,S,beta,{v:int(v>=left_size) for v in range(n0)})
                counts['small_bipartite_graphs'] += 1
    # Seeded exact rational identities, with all extraction algebra enforced.
    rng = random.Random(121126)
    for _ in range(3000):
        # Generate from the two ledgers; this numerical control is separate
        # from the actual physical extractions above, not a realization claim.
        gamma = Fraction(rng.randrange(101),100)
        bp = rng.randrange(25); b3 = rng.randrange(6); b = bp+b3
        o = 2*rng.randrange(bp+1)
        if o < 2*gamma*bp: continue
        minimum = rng.randrange(10); tau = rng.randrange(10)
        if (b+minimum-tau) % 2: continue
        d = (b+minimum-tau)//2
        al,pi = ((rng.randrange(10),0) if rng.randrange(2) else (0,rng.randrange(10)))
        a,p = minimum+al,minimum+pi
        e,r,q = b3+rng.randrange(10),rng.randrange(10),rng.randrange(10)
        Z = 5*minimum+3*(al+pi)+3*e+5*b3+tau-d
        if Z < Fraction(o,2) or (Z+8*bp) % 3: continue
        L = r+a+b-bp+p
        beta = L+(Z+8*bp)//3
        S_size = beta+d
        u = a+2*b+e
        n0 = S_size+p+u+q
        rec = odd_path_ledger(n0,a,p,u,r+a+b,b,b3,S_size,beta,L,o,gamma)
        digest.update(json.dumps(rec,sort_keys=True).encode())
        counts['rational_ledger_controls'] += 1
    assert counts['analytic_maximal_cost_one_cases'] == 48
    assert counts['positive_odd_path_extractions'] > 0
    parser = argparse.ArgumentParser(); parser.add_argument('--output',type=Path,
        default=ROOT/'output/sharp-all-helper-check.json'); args = parser.parse_args()
    report = {'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),
        'sharp_block':{'order':30,'edges':42,'beta_I':16,'beta_2':17,
                       'all_helper_forcing_loss':1,'canonical_minimal_forming_size':18},
        'scope':'General written exact block proof and additive all-r forcing loss; independent finite exact optima. Odd-path coefficient is conditional on an actual K4-free extraction and its odd-path ratio. General all-helper8b/3 and universal subcubic sharp coefficient remain open. No SF optimum is asserted here.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__': main()
