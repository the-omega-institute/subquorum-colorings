#!/usr/bin/env python3
"""Literal matching checks of every fixed boundary subset in each placement."""
from pathlib import Path
from itertools import combinations,product
from functools import lru_cache
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from fixed_boundary_matching_cut import four_boundary,forced_independent
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();features=Counter();digest=hashlib.sha256();rng=random.Random(445872)


def aux(lengths):
    P=[];Q=[];colour={};off=0
    for n in lengths:
        assert n>=4 and n%4==0
        P += [(off+j,off+j+1) for j in range(0,n,2)]
        Q += [(off+j,off+(j+1)%n) for j in range(1,n,2)]
        colour.update({off+j:(j//2)%2 for j in range(n)});off+=n
    return P,Q,colour


def literal_cost(P,Q,U):
    V=sorted(U);idx={v:j for j,v in enumerate(V)};adj=[0]*len(V)
    for a,b in P+Q:
        if a in idx and b in idx:adj[idx[a]]|=1<<idx[b];adj[idx[b]]|=1<<idx[a]
    @lru_cache(None)
    def solve(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;best=solve(rest);ns=adj[v]&rest
        while ns:
            u=ns&-ns;ns-=u;best=max(best,1+solve(rest^u))
        return best
    return solve((1<<len(V))-1)


def inspect(P,Q,colour,C):
    F=sorted(set(colour)-{v for K in C for v in K});k=len(C)
    for bits in range(16):
        F0={v for j,v in enumerate(F) if bits>>j&1};U,rec=four_boundary(P,Q,C,colour,F0)
        assert U&set(F)==F0 and all(len(U&set(K))==2 for K in C)
        M=rec['matching'];assert len({v for e in M for v in e})==2*len(M) and all(set(e)<=U and (e in P+Q or tuple(reversed(e)) in P+Q) for e in M)
        if k<=12:
            cost=literal_cost(P,Q,U);assert cost==len(M);counts['literal_matching_comparisons']+=1
        assert len(U)-2*len(M)==rec['deficiency']>=2*(k//2)+len(F0)%2
        features['forced_vertex']+=rec['forced'] is not None
        features['strict_improvement_over_previous_four_boundary_guarantee']+=k in (3,4) and rec['guarantee']>(3 if len(F0)%2 else 2)
        counts['boundary_size_'+str(len(F0))]+=1;counts['fixed_boundary_controls']+=1
        digest.update(json.dumps([P,Q,C,sorted(F0),sorted(U),rec['deficiency'],rec['guarantee']],sort_keys=True).encode()+b'\n')
    counts['physical_placements']+=1
# Complete placements of one owner square and four free vertices for each A.
for lengths in ([8],[4,4]):
    P,Q,col=aux(lengths);sides=[[v for v in col if col[v]==c] for c in (0,1)]
    for a in combinations(sides[0],2):
        for b in combinations(sides[1],2):inspect(P,Q,col,[[a[0],b[0],a[1],b[1]]]);counts['complete_one_square_placements']+=1
# All fixed subsets for seeded placements, including k=0 and odd/even large k.
for k in (0,2,3,4,5,6,7,8,12,31,63):
    n=4*(k+1)
    choices=[[n],[4]*(k+1)]
    if n>=16:choices.append([16]+[4]*((n-16)//4))
    for lengths in choices:
        P,Q,col=aux(lengths)
        for trial in range(10 if k<=12 else 3):
            sides=[[v for v in col if col[v]==c] for c in (0,1)]
            for side in sides:rng.shuffle(side)
            C=[[sides[0][2*j],sides[1][2*j],sides[0][2*j+1],sides[1][2*j+1]] for j in range(k)]
            inspect(P,Q,col,C)
            if lengths[0]==16:counts['unique_C16_placements']+=1
# Force every possible vertex in all three matchings for each fixed physical J.
for k in range(1,7):
    P,Q,col=aux([4*k]);sides=[[v for v in col if col[v]==c] for c in (0,1)]
    for side in sides:rng.shuffle(side)
    R=[(side[j],side[j+1]) for side in sides for j in range(0,len(side),2)]
    tod=lambda E:{v:u for a,b in E for v,u in ((a,b),(b,a))}
    for z in col:
        Y,rec=forced_independent(tod(P),tod(Q),tod(R),col,z)
        assert z in Y and len(Y)>=(3*k+1)//2 and all(not {a,b}<=Y for a,b in P+Q+R);counts['every_forced_vertex_controls']+=1
assert features['strict_improvement_over_previous_four_boundary_guarantee'] and counts['unique_C16_placements']
report=dict(status='PASS',counts=dict(sorted(counts.items())),features=dict(sorted(features.items())),deterministic_sha256=digest.hexdigest(),scope='All-k written fixed-four-boundary theorem delta>=2floor(k/2)+boundaryparity. Complete one-square placements for C8 and2C4, all16boundarysubsets perplacement; seeded larger placements finite controls, not proof. Does not prove full uniqueC16/multiplelongcycle or physicalgrid theorems.')
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/fixed-boundary-matching-cut-check.json');a=p.parse_args();a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
