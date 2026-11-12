#!/usr/bin/env python3
"""Literal physical controls for the square-core construction and its lift."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from subcubic_square_core import template_certificate, lift_certificate, independent_certificate
from subcubic_partial_template import decompose

if not __debug__:
    raise RuntimeError('Run with assertions enabled')
COUNTS, FEATURES = Counter(), Counter()
DIGEST = hashlib.sha256()


def diss(g, D):
    return all(len(g[v] & D) <= 1 for v in D)


def forms(g, S):
    # Enumerate actual two-leaf stars, including an outside vertex as centre or leaf.
    for x in set(range(len(g)))-S:
        if not any(x in {c,a,b} and len({c,a,b} & S) == 2
                   for c in {x} | g[x] for a,b in combinations(g[c],2)):
            return False
    return True


def minimal(g, S):
    return forms(g,S) and all(not forms(g,S-{v}) for v in S)


def exact(g):
    adj = [sum(1<<u for u in row) for row in g]
    @lru_cache(None)
    def solve(mask):
        if not mask: return 0
        v = max((j for j in range(len(g)) if mask>>j&1), key=lambda j:(adj[j]&mask).bit_count())
        ns = adj[v]&mask
        if not ns: return mask.bit_count()
        closed = ns | (1<<v)
        result = max(solve(mask & ~(1<<v)),1+solve(mask & ~closed))
        while ns:
            bit = ns & -ns; ns -= bit
            result = max(result,2+solve(mask & ~(closed|adj[bit.bit_length()-1])))
        return result
    return solve((1<<len(g))-1)


def literal_beta(g):
    return max((mask.bit_count() for mask in range(1<<len(g))
                if diss(g,{v for v in range(len(g)) if mask>>v&1})),default=0)


def model(b, r, core, interface):
    I, X, C = set(range(b)),set(range(b,3*b)),set(range(3*b,5*b))
    g = [set() for _ in range(5*b)]
    colour = {i:int(i>=r) for i in I}
    owner = {}
    for i in I:
        for j in range(2):
            x,c = b+2*i+j,3*b+2*i+j
            colour[x],colour[c],owner[x] = 1-colour[i],colour[i],c
            for v,u in ((i,x),(x,c)):
                g[v].add(u);g[u].add(v)
    for v,u in core+interface:
        g[v].add(u);g[u].add(v)
    return dict(g=g,I=I,X=X,C=C,owner=owner,graph_colour=colour)


def matchings(a,b):
    if not a:
        yield [];return
    yield from matchings(a[1:],b)
    for v in b:
        for tail in matchings(a[1:],[u for u in b if u!=v]):
            yield [(a[0],v)]+tail


def check(m, optimize=True, literal=False):
    g = m['g'];S = m['I']|m['C'];b=len(m['I'])
    assert all(len(ns)<=3 and all(v!=u and v in g[u] and m['graph_colour'][v]!=m['graph_colour'][u]
                                 for u in ns) for v,ns in enumerate(g))
    D,data = template_certificate(m)
    assert diss(g,D) and minimal(g,S)
    t = data['square_count']
    assert len(D)>=3*b-(2*t)//3 >= (8*b+2)//3
    J,Y = data['auxiliary'],data['chosen']
    assert all(not J[v]&Y for v in Y)
    assert all(J[v]&Y for v in set(J)-Y)
    assert all(sum(J[x]&Y=={v} for x in set(J)-Y)<=1 for v in Y)
    if optimize:
        beta=exact(g)
        assert beta>=len(D)
        if literal:
            assert literal_beta(g)==beta
            COUNTS['literal_template_optima']+=1
        try:
            lifted,rec=lift_certificate(g,S,m['graph_colour'],decompose(g,S),beta)
        except ValueError:
            COUNTS['canonical_extraction_nonapplicable']+=1
        else:
            assert diss(g,lifted) and 51*(len(S)-beta)<=5*len(g)
            assert rec['Z']>=rec['template']['structural_surplus']
            COUNTS['canonical_extraction_lifts']+=1
            FEATURES['canonical_lift_nonempty_template']+=bool(rec['bprime'])
        COUNTS['exact_template_optima']+=1
    COUNTS['templates']+=1
    COUNTS['local_exchanges']+=len(data['independent']['exchanges'])
    FEATURES['nonempty_square_core']+=t>0
    FEATURES['nonsquare_owner']+=4*t<len(m['C'])
    FEATURES['partial_Q']+=any(not g[x]&m['X'] for x in m['X'])
    FEATURES['unbalanced_template']+=len({v for v in m['graph_colour'] if not m['graph_colour'][v]})*2!=len(g)
    FEATURES['P_R_duplicate']+=any(m['owner'][v] in m['C'] and
        any(g[i]&m['X']=={v,u} for i in m['I']) for v in J for u in J[v]
        if m['graph_colour'][v]==m['graph_colour'][u]
        and len(g[m['owner'][v]] & g[m['owner'][u]] & m['C'])==2)
    DIGEST.update(json.dumps([len(g),sorted(D),sorted(Y),t],sort_keys=True).encode()+b'\n')
    return data


def main():
    for b in range(4):
        for r in range(b+1):
            m=model(b,r,[],[])
            ca=[v for v in m['C'] if not m['graph_colour'][v]];cb=sorted(m['C']-set(ca))
            xa=[v for v in m['X'] if not m['graph_colour'][v]];xb=sorted(m['X']-set(xa))
            es=list(product(ca,cb))
            for bits in range(1<<len(es)):
                core=[edge for j,edge in enumerate(es) if bits>>j&1]
                if any(sum(v in edge for edge in core)>2 for v in m['C']):continue
                candidate=model(b,r,core,[])
                try:template_certificate(candidate)
                except ValueError:continue
                for Q in matchings(xa,xb):check(model(b,r,core,Q),literal=b<=2)
    rng=random.Random(32861112)
    for b,number in ((4,70),(5,50),(6,15),(8,5),(16,20),(64,8),(256,3),(512,1)):
        for j in range(number):
            r=b//2 if j%3 else rng.randrange(b+1)
            base=model(b,r,[],[])
            ca=[v for v in base['C'] if not base['graph_colour'][v]];cb=sorted(base['C']-set(ca))
            rng.shuffle(ca);rng.shuffle(cb)
            t=min(len(ca),len(cb))//2
            if j%2:t=rng.randrange(t+1)
            core=[]
            for k in range(t):core += list(product(ca[2*k:2*k+2],cb[2*k:2*k+2]))
            core += [(a,c) for a,c in zip(ca[2*t:],cb[2*t:]) if rng.randrange(2)]
            xa=[v for v in base['X'] if not base['graph_colour'][v]];xb=sorted(base['X']-set(xa))
            rng.shuffle(xa);rng.shuffle(xb)
            Q=[(a,c) for a,c in zip(xa,xb) if j%4==0 or rng.randrange(3)]
            check(model(b,r,core,Q),optimize=b<=6)
    # All labelled bipartite graphs in these fixed bipartitions, with ALL minimal S.
    for n in range(7):
        for a in range(n//2+1):
            es=list(product(range(a),range(a,n)))
            for bits in range(1<<len(es)):
                g=[set() for _ in range(n)]
                for j,(v,u) in enumerate(es):
                    if bits>>j&1:g[v].add(u);g[u].add(v)
                if max(map(len,g),default=0)>3:continue
                beta=literal_beta(g);colour={v:int(v>=a) for v in range(n)}
                assert beta==exact(g)
                for mask in range(1<<n):
                    S={v for v in range(n) if mask>>v&1}
                    if not minimal(g,S):continue
                    w=decompose(g,S)
                    try:D,data=lift_certificate(g,S,colour,w,beta)
                    except ValueError:
                        COUNTS['nonapplicable_minimal_selections']+=1;continue
                    assert diss(g,D) and sum(data['nonnegative_terms'])==5*n-51*(len(S)-beta)
                    COUNTS['lifted_minimal_selections']+=1
                    FEATURES['lift_nonempty_template']+=bool(w['I0'])
                    FEATURES['lift_nonempty_retained']+=bool(data['retained'])
                COUNTS['small_graphs']+=1
    # Nonempty square extraction with simultaneously retained outside resources.
    square=model(2,1,[(a,b) for a in (6,7) for b in (8,9)],[])
    seedg=square['g'];seedS=square['I']|square['C']
    joined=0
    for n in range(1,7):
        for j in range(8):
            a=n//2;es=list(product(range(a),range(a,n)))
            tail=[set() for _ in range(n)]
            for v,u in es:
                if len(tail[v])<3 and len(tail[u])<3 and rng.randrange(2):
                    tail[v].add(u);tail[u].add(v)
            for mask in range(1<<n):
                T={v for v in range(n) if mask>>v&1}
                if not minimal(tail,T):continue
                g=[set(row) for row in seedg]+[{10+u for u in row} for row in tail]
                S=seedS|{10+v for v in T}
                colour=dict(square['graph_colour'],**{})
                colour.update({10+v:int(v>=a) for v in range(n)})
                w=decompose(g,S);beta=exact(g)
                D,data=lift_certificate(g,S,colour,w,beta)
                assert data['bprime']==2 and data['template']['square_count']==1 and diss(g,D)
                assert data['retained'] and all(not g[v]&data['inner'] for v in data['retained'])
                COUNTS['nonempty_template_exterior_lifts']+=1
                FEATURES['retained_triple_leaf_with_square']+=bool(w['triples'])
                joined+=1
    # General independent-set subroutine, including odd cycles and actual exchanges.
    for n in range(4,13):
        for j in range(30):
            h={v:set() for v in range(n)};pairs=list(combinations(range(n),2));rng.shuffle(pairs)
            for a,b in pairs:
                if len(h[a])<3 and len(h[b])<3 and not h[a]&h[b] and rng.randrange(2):
                    h[a].add(b);h[b].add(a)
            D,rec=independent_certificate(h)
            assert 3*len(D)>=n and all(not h[v]&D for v in D)
            COUNTS['independent_subroutine_graphs']+=1
            COUNTS['subroutine_exchanges']+=len(rec['exchanges'])
    for edges in ([(0,1),(1,2),(2,0)],list(combinations(range(5),2))):
        h={v:set() for edge in edges for v in edge}
        for a,b in edges:h[a].add(b);h[b].add(a)
        try:independent_certificate(h)
        except ValueError:COUNTS['rejected_bad_auxiliary_graphs']+=1
        else:raise AssertionError('Bad auxiliary accepted')
    bad=model(2,1,[(6,8),(7,8)],[])
    try:template_certificate(bad)
    except ValueError:COUNTS['rejected_nonapplicable_core']+=1
    else:raise AssertionError('P3 core accepted')
    report=dict(status='PASS',counts=dict(sorted(COUNTS.items())),features=dict(sorted(FEATURES.items())),
                digest=DIGEST.hexdigest(),scope='All-size written construction and fixed-extraction ledger. All valid prescribed partial templates b<=3, r=0..b; independent exact optima on these and seeded b4..6. Literal subset optimum additionally b<=2. Seeded larger models check actual sets/minimality/structural bound, not exact beta. All minimal selections in the stated small graph controls are tested, and nonapplicable extractions are counted separately. No unrestricted8b/3 claim.')
    (ROOT/'output').mkdir(exist_ok=True)
    (ROOT/'output/square-core-check.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
