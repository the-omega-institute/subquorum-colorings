#!/usr/bin/env python3
"""Actual fixed-boundary matching certificates and independent finite controls."""
from pathlib import Path
from functools import lru_cache
from collections import Counter
from itertools import product
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'develop'),str(ROOT/'scripts')]
from balanced_boundary_matching_cut import certificate
from all_helper_optimization import score
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();features=Counter();digest=hashlib.sha256();rng=random.Random(44821113)


def aux(lengths):
    P=[];Q=[];col={};off=0
    for n in lengths:
        assert n>=4 and n%4==0
        P += [(off+j,off+j+1) for j in range(0,n,2)]
        Q += [(off+j,off+(j+1)%n) for j in range(1,n,2)]
        col.update({off+j:(j//2)%2 for j in range(n)});off+=n
    return P,Q,col


def placement(k,h,lengths):
    P,Q,col=aux(lengths);assert len(col)==4*(k+h)
    sides=[[v for v in col if col[v]==c] for c in (0,1)]
    for side in sides:rng.shuffle(side)
    C=[[sides[0][2*j],sides[1][2*j],sides[0][2*j+1],sides[1][2*j+1]] for j in range(k)]
    F=sorted(set(col)-{v for K in C for v in K});return P,Q,col,C,F


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


def independent_physical(P,Q,C,col,rec,U):
    # Rebuild the temporary all-helper graph on 10(k+h) vertices, without
    # importing a physical template builder or trusting returned adjacencies.
    V=sorted(col);idx={v:j for j,v in enumerate(V)};b=len(V)//2
    assert len(P)==b
    graph=[set() for _ in range(5*b)]
    def add(a,c):graph[a].add(c);graph[c].add(a)
    for i,(a,c) in enumerate(P):add(i,b+idx[a]);add(i,b+idx[c])
    for v in V:add(b+idx[v],3*b+idx[v])
    for a,c in Q:add(b+idx[a],b+idx[c])
    for K in list(C)+rec['artificial_squares']:
        for j,v in enumerate(K):add(3*b+idx[v],3*b+idx[K[(j+1)%4]])
    Z=rec['base_omissions'];Y=rec['independent']
    D=set(range(b))|{3*b+idx[v] for v in set(V)-Z}|{b+idx[v] for v in Y}
    assert all(len(graph[v]&D)<=1 for v in D)
    assert len(D)>=3*b-(len(C)+rec['h'])//2
    counts['independent_base_physical_scores']+=1


def inspect(P,Q,col,C,F0,literal=False,physical=False):
    U,rec=certificate(P,Q,C,col,F0);V=set(col);F=V-{v for K in C for v in K};k=len(C);h=len(F)//4;f=len(F0)
    assert rec['k']==k and rec['h']==h and U&F==set(F0)
    assert all(len(U&set(K))==2 for K in C) and len(U)==2*k+f
    Y,Z=rec['independent'],rec['base_omissions']
    R=[e for row in rec['free_opposite_pairs'] for e in row]+[(K[j],K[j+2]) for K in C for j in (0,1)]
    assert all(not set(e)<=Y for e in P+Q+R) and Y<=Z and len(Y)>=(3*(k+h)+1)//2
    assert len(Z&set(F0))>=(f+1)//2
    if rec['forced'] is not None:assert rec['forced'] in Y
    M=rec['matching'];assert len({v for e in M for v in e})==2*len(M)
    edges={frozenset(e) for e in P+Q};assert all(set(e)<=U and frozenset(e) in edges for e in M)
    if literal:
        assert literal_cost(P,Q,U)==len(M)
        assert literal_cost(P,Q,Z)==len(rec['base_matching']);counts['literal_matching_comparisons']+=2
    if physical:independent_physical(P,Q,C,col,rec,U)
    assert rec['deficiency']==len(U)-2*len(M)>=max(0,2*k-2*((k+h)//2))+f%2
    assert len(M)<=(k+h)//2+f//2
    features['both_side_counts_odd']+=all(a%2 for a in rec['side_membership_counts'])
    features['exactly_one_side_count_odd']+=sum(a%2 for a in rec['side_membership_counts'])==1
    features['forced_vertex']+=rec['forced'] is not None
    features['negative_raw_bound']+=rec['raw_guarantee']<0
    features['nontrivial_positive_even_part']+=rec['guarantee']-f%2>0
    features['eight_boundary_vertices']+=h==2
    counts['fixed_boundary_controls']+=1
    digest.update(json.dumps([P,Q,C,sorted(F0),rec['side_membership_counts'],rec['forced'],sorted(Y),sorted(Z),sorted(U),rec['deficiency'],rec['guarantee']],sort_keys=True).encode()+b'\n')
    return rec


# Every fixed boundary subset for each stated seeded placement, h<=2.
for h in range(3):
    for k in range(9):
        n=4*(k+h);choices=[[]] if n==0 else [[n],[4]*(k+h)]
        if n>=16:choices.append([16]+[4]*((n-16)//4))
        for lengths in choices:
            for trial in range(3 if h==2 else 2):
                P,Q,col,C,F=placement(k,h,lengths)
                for mask in range(1<<len(F)):
                    F0={v for j,v in enumerate(F) if mask>>j&1}
                    inspect(P,Q,col,C,F0,literal=k+h<=8,physical=mask in (0,1,(1<<len(F))-1))
                counts['complete_boundary_placements_h'+str(h)]+=1
# One whole 12-vertex boundary hypercube, all4096 exact subsets.
P,Q,col,C,F=placement(3,3,[16,4,4])
for mask in range(1<<12):inspect(P,Q,col,C,{v for j,v in enumerate(F) if mask>>j&1},literal=True,physical=mask%127==0)
counts['complete_boundary_placements_h3']+=1
# All side-cardinality pairs for these larger geometries; one seeded support
# for each pair, not all supports. Includes empty/all, odd and asymmetric cases.
for k,h in ((0,3),(3,4),(7,5),(31,8),(63,16),(128,32)):
    P,Q,col,C,F=placement(k,h,[16]+[4]*(k+h-4) if k+h>=4 else [4]*(k+h))
    sides=[[v for v in F if col[v]==c] for c in (0,1)]
    values=range(2*h+1) if h<=8 else sorted({0,1,2,h-1,h,h+1,2*h-2,2*h-1,2*h})
    for a,b in product(values,repeat=2):
        F0=set(rng.sample(sides[0],a)+rng.sample(sides[1],b))
        inspect(P,Q,col,C,F0,literal=k+h<=12,physical=True);counts['sampled_side_cardinality_pairs']+=1
# Relabel the physical region and reverse its physical colours.
for trial in range(16):
    P,Q,col,C,F=placement(5,2,[16,4,4,4]);V=list(col);perm=V[:];rng.shuffle(perm);mapping=dict(zip(V,perm))
    rel=lambda e:[mapping[v] for v in e]
    PP=[tuple(rel(e)) for e in P];QQ=[tuple(rel(e)) for e in Q];cc={mapping[v]:c^(trial%2) for v,c in col.items()};CC=[rel(K) for K in C];F0={mapping[v] for v in F if rng.randrange(2)}
    inspect(PP,QQ,cc,CC,F0,literal=True,physical=True);counts['relabel_colour_flip_controls']+=1
assert features['both_side_counts_odd'] and features['exactly_one_side_count_odd'] and features['negative_raw_bound'] and features['nontrivial_positive_even_part']
report=dict(status='PASS',counts=dict(sorted(counts.items())),features=dict(sorted(features.items())),deterministic_sha256=digest.hexdigest(),scope='All-size written matching-cut theorem for k actual C4 owners and4h balanced boundary vertices, every prescribed F0. Complete boundary subsets per stated seeded placement throughh3, not complete physical placements or nonisomorphicclassification; larger side-cardinality pairs one seeded support each. Independent literal matching and base actual10(k+h)vertexphysicalscoring. No fullC16/mixedcyclic/physicalgrid theorem or overlappingregionaladdition claim.')
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/balanced-boundary-matching-cut-check.json');a=p.parse_args();a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
