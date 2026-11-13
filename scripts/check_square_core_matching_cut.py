#!/usr/bin/env python3
"""Independent physical scoring, exact small optima and extraction ledgers."""
from pathlib import Path
from itertools import product
from collections import Counter
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'develop'),str(ROOT/'scripts')]
from square_core_matching_cut import matching_cut_certificate,template_certificate,lift_certificate
from subcubic_square_core import template_certificate as old_template
from subcubic_partial_template import decompose
from all_helper_optimization import solve as all_helper
from check_square_core_template import model,diss,minimal,exact,literal_beta,matchings
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();features=Counter();digest=hashlib.sha256();rng=random.Random(38721113)


def clean(x):
    if isinstance(x,dict):return {str(k):clean(v) for k,v in sorted(x.items(),key=lambda z:str(z[0]))}
    if isinstance(x,set):return sorted(x)
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x


def record(x):digest.update(json.dumps(clean(x),sort_keys=True).encode()+b'\n')


def pair_dict(pairs):return {v:u for a,b in pairs for v,u in ((a,b),(b,a))}


def partial_matchings(vertices):
    if not vertices:yield [];return
    a=vertices[0]
    yield from partial_matchings(vertices[1:])
    for b in vertices[1:]:
        for tail in partial_matchings([v for v in vertices[1:] if v!=b]):yield [(a,b)]+tail


def inspect_cut(t,P,Q,R,colour,brute=False):
    Y,rec=matching_cut_certificate(P,Q,R,colour);J=rec['auxiliary']
    # Rebuild adjacency directly from all matching resources, not supplier data.
    assert J=={v:{d[v] for d in (P,Q,R) if v in d} for v in colour}
    assert len(Y)>=(3*t+1)//2 and all(not J[v]&Y for v in Y)
    for a in rec['alternatives']:
        assert len(a['first'])==t and a['first'].isdisjoint(a['second'])
        assert a['forbidden']=={Q[v] for v in a['first'] if v in Q}
        assert len(a['available'])>=t and 2*len(a['second'])>=len(a['available'])
    if brute:
        V=sorted(J);edges={(a,b) for a in J for b in J[a] if a<b}
        alpha=max(mask.bit_count() for mask in range(1<<len(V)) if all(not(mask>>a&1 and mask>>b&1) for a,b in edges))
        assert alpha>=len(Y);counts['literal_auxiliary_optima']+=1
    features['odd_square_count']+=t%2
    features['duplicate_P_R']+=bool(set(P)&set(R) and any(P[v]==R[v] for v in P))
    features['partial_P']+=len(P)<4*t;features['partial_Q']+=len(Q)<4*t
    counts['matching_cut_models']+=1;record([P,Q,R,colour,Y,rec]);return Y


# Complete abstract matching-cut class for t=0,1,2 with canonical fixed R.
# Within each side R can always be relabelled to this fixed perfect matching.
for t in range(3):
    left=list(range(2*t));right=list(range(2*t,4*t));col={v:int(v>=2*t) for v in left+right}
    R=pair_dict([(v,v+1) for v in range(0,4*t,2)])
    for p0 in partial_matchings(left):
        for p1 in partial_matchings(right):
            for q in matchings(left,right):inspect_cut(t,pair_dict(p0+p1),pair_dict(q),R,col,brute=True)
for t in (3,4,7,16,63,128):
    for trial in range(12):
        sides=[list(range(2*t)),list(range(2*t,4*t))];R=[];P=[]
        for side in sides:
            rng.shuffle(side);R+=list(zip(side[::2],side[1::2]));rng.shuffle(side)
            P += [(a,b) for a,b in zip(side[::2],side[1::2]) if trial%3==0 or rng.randrange(3)]
        Q=[(a,b) for a,b in zip(*sides) if trial%4==0 or rng.randrange(3)]
        inspect_cut(t,pair_dict(P),pair_dict(Q),pair_dict(R),{v:int(v>=2*t) for v in range(4*t)},brute=t==3)


def inspect(m,ex=False,literal=False):
    g=m['g'];b=len(m['I']);D,rec=template_certificate(m);t=rec['square_count']
    assert all(len(ns)<=3 and all(v!=u and v in g[u] and m['graph_colour'][v]!=m['graph_colour'][u] for u in ns) for v,ns in enumerate(g))
    assert m['I']<=D and diss(g,D) and minimal(g,m['I']|m['C'])
    assert len(D)>=3*b-t//2>=(11*b+3)//4
    assert len(rec['chosen'])>=(3*t+1)//2 and len(rec['deleted'])==2*t
    assert rec['structural_surplus_W']==b-2*t+2*(t%2)>=0
    old,oldrec=old_template(m)
    features['strict_guarantee_improvement']+=rec['guarantee']>oldrec['guarantee']
    features['strict_actual_certificate_improvement']+=len(D)>len(old)
    features['nonsquare_owners']+=4*t<len(m['C'])
    features['nonempty_square_core']+=t>0
    if ex:
        beta=exact(g);assert beta>=len(D)
        if literal:assert beta==literal_beta(g);counts['literal_physical_optima']+=1
        counts['exact_physical_optima']+=1
        try:lifted,lift=lift_certificate(g,m['I']|m['C'],m['graph_colour'],decompose(g,m['I']|m['C']),beta)
        except ValueError:counts['canonical_extraction_nonapplicable']+=1
        else:
            assert diss(g,lifted) and sum(lift['nonnegative_terms'])==7*len(g)-72*(3*b-beta)
            counts['canonical_extraction_lifts']+=1
    counts['physical_templates']+=1;record([m,D,rec]);return rec


# All prescribed physical partial templates b<=3, r=0..b (labelled controls).
for b in range(4):
    for r in range(b+1):
        base=model(b,r,[],[]);ca=sorted(v for v in base['C'] if not base['graph_colour'][v]);cb=sorted(base['C']-set(ca));xa=sorted(v for v in base['X'] if not base['graph_colour'][v]);xb=sorted(base['X']-set(xa));E=list(product(ca,cb))
        for mask in range(1<<len(E)):
            core=[e for j,e in enumerate(E) if mask>>j&1]
            if any(sum(v in e for e in core)>2 for v in base['C']):continue
            try:template_certificate(model(b,r,core,[]))
            except ValueError:continue
            for Q in matchings(xa,xb):inspect(model(b,r,core,Q),ex=True,literal=b<=2)
for b,number in ((4,40),(5,30),(6,20),(8,15),(16,15),(40,8),(128,3),(512,1)):
    for trial in range(number):
        r=b//2 if trial%3 else rng.randrange(b+1);base=model(b,r,[],[])
        ca=sorted(v for v in base['C'] if not base['graph_colour'][v]);cb=sorted(base['C']-set(ca));xa=sorted(v for v in base['X'] if not base['graph_colour'][v]);xb=sorted(base['X']-set(xa))
        for z in (ca,cb,xa,xb):rng.shuffle(z)
        t=min(len(ca),len(cb))//2
        if trial%2:t=rng.randrange(t+1)
        core=[(a,c) for k in range(t) for a in ca[2*k:2*k+2] for c in cb[2*k:2*k+2]]+[(a,c) for a,c in zip(ca[2*t:],cb[2*t:]) if rng.randrange(2)]
        Q=[(a,c) for a,c in zip(xa,xb) if trial%4==0 or rng.randrange(3)]
        inspect(model(b,r,core,Q),ex=b<=6)


# Independently solve the all-helper matching optimization on fixed controls.
fixtures={}
for name in ('square-core-matching-cut-sharp','square-core-strict-thirty'):
    x=json.loads((ROOT/f'develop/fixtures/{name}.json').read_text());m=model(**{k:x[k] for k in ('b','r','core','interface')});rec=inspect(m,ex=True);b=x['b'];P=[(2*i,2*i+1) for i in range(b)];Q=[(a-b,c-b) for a,c in x['interface']];B=[(a-3*b,c-3*b) for a,c in x['core']]
    assert all_helper(b,P,Q,B)['beta_I']==x['all_helper_beta']==exact(m['g'])==len(template_certificate(m)[0])==x['unrestricted_beta']
    fixtures[name]=m;counts['independent_all_helper_exact_fixture_optima']+=1
sharp=fixtures['square-core-matching-cut-sharp'];P=[(2*i,2*i+1) for i in range(4)];x=json.loads((ROOT/'develop/fixtures/square-core-matching-cut-sharp.json').read_text());Q=[(a-4,b-4) for a,b in x['interface']];B=[(a-12,b-12) for a,b in x['core']]
A={v:set() for v in range(8)}
for a,b in P+Q:A[a].add(b);A[b].add(a)
owner_squares=[{a-12 for a in sq} for sq in __import__('subcubic_square_core').square_components(sharp)]
for mask in range(256):
    U={v for v in range(8) if mask>>v&1}
    permitted=all(sum(u in U for u in square)>=2 for square in owner_squares)
    if permitted:
        assert len(U)>=4 and any(A[v]&U for v in U);counts['sharp_block_permitted_omissions_checked']+=1
# alpha(J)=3, direct subset check, without importing independence algorithm.
J=template_certificate(sharp)[1]['auxiliary'];V=sorted(J)
assert max(mask.bit_count() for mask in range(256) if all(not(mask>>i&1 and mask>>j&1) for i,a in enumerate(V) for j,b in enumerate(V) if b in J[a]))==3


def disjoint(models):
    out=dict(g=[],I=set(),C=set(),X=set(),owner={},graph_colour={})
    for m in models:
        off=len(out['g']);out['g'] += [{v+off for v in row} for row in m['g']]
        for k in ('I','C','X'):out[k]|={v+off for v in m[k]}
        out['owner'].update({x+off:c+off for x,c in m['owner'].items()});out['graph_colour'].update({v+off:c for v,c in m['graph_colour'].items()})
    return out
single=model(2,1,list(product((6,7),(8,9))),[]);squarefree=model(1,1,[],[])
for t in range(9):
    for extra in range(4):
        models=[sharp]*(t//2)+[single]*(t%2)+[squarefree]*extra;m=disjoint(models);rec=inspect(m,ex=len(m['I'])<=6)
        assert rec['square_count']==t and len(template_certificate(m)[0])==3*len(m['I'])-t//2
        counts['sharp_refined_disjoint_family_controls']+=1
# Label and physical-colour invariance controls on the fixed sharp graph.
for trial in range(12):
    order=list(range(20));rng.shuffle(order)
    m=dict(g=[set() for _ in order],I={order[v] for v in sharp['I']},X={order[v] for v in sharp['X']},C={order[v] for v in sharp['C']},owner={order[x]:order[c] for x,c in sharp['owner'].items()},graph_colour={order[v]:c^(trial%2) for v,c in sharp['graph_colour'].items()})
    for v,row in enumerate(sharp['g']):m['g'][order[v]]={order[u] for u in row}
    inspect(m,ex=True);counts['physical_relabel_colour_flip_controls']+=1
# Every minimal S in complete small labelled bipartite graph controls.
for n in range(7):
    for a in range(n//2+1):
        E=list(product(range(a),range(a,n)))
        for mask in range(1<<len(E)):
            g=[set() for _ in range(n)]
            for j,(v,u) in enumerate(E):
                if mask>>j&1:g[v].add(u);g[u].add(v)
            if max(map(len,g),default=0)>3:continue
            beta=literal_beta(g);col={v:int(v>=a) for v in range(n)}
            for bits in range(1<<n):
                S={v for v in range(n) if bits>>v&1}
                if not minimal(g,S):continue
                try:D,lift=lift_certificate(g,S,col,decompose(g,S),beta)
                except ValueError:counts['nonapplicable_minimal_selections']+=1;continue
                assert diss(g,D) and sum(lift['nonnegative_terms'])==7*n-72*(len(S)-beta)
                counts['all_minimal_selection_lifts']+=1
            counts['small_bipartite_graphs']+=1
for n in range(1,7):
    for trial in range(8):
        a=n//2;tail=[set() for _ in range(n)]
        for v,u in product(range(a),range(a,n)):
            if len(tail[v])<3 and len(tail[u])<3 and rng.randrange(2):tail[v].add(u);tail[u].add(v)
        for bits in range(1<<n):
            T={v for v in range(n) if bits>>v&1}
            if not minimal(tail,T):continue
            g=[set(z) for z in single['g']]+[{v+10 for v in z} for z in tail];S=single['I']|single['C']|{v+10 for v in T};col=dict(single['graph_colour']);col.update({v+10:int(v>=a) for v in range(n)})
            w=decompose(g,S);D,lift=lift_certificate(g,S,col,w,exact(g))
            assert diss(g,D) and lift['bprime']==2 and lift['retained']
            features['retained_triple_leaf_with_square']+=bool(w['triples']);counts['nonempty_template_exterior_lifts']+=1
# Formal zero-slack rays check the coefficient algebra, NOT graph realizability.
for scale in (0,1,2,7,10**40):
    m,d,b,n=2*scale,7*scale,12*scale,72*scale;assert 7*n-72*d==0 and 2*d==7*m and m+b==2*d;counts['formal_zero_slack_ledger_rays']+=1
bad=model(2,1,[(6,8),(7,8)],[])
try:template_certificate(bad)
except ValueError:counts['rejected_nonapplicable_P3_core']+=1
else:raise AssertionError('P3 accepted')
assert features['strict_actual_certificate_improvement'] and features['strict_guarantee_improvement'] and features['retained_triple_leaf_with_square']
report=dict(status='PASS',counts=dict(sorted(counts.items())),features=dict(sorted(features.items())),deterministic_sha256=digest.hexdigest(),scope='All-size matching-cut proof; sharp ALL-HELPER square-core template11b/4 and refined3b-floor(t/2). Conditional fixed-actual-extraction7n/72 graph-gap bound, no unrestricted or sharp gap claim. Complete prescribed small labelled controls; larger seeds finite tests only. No Lean execution.')
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/square-core-matching-cut-check.json');a=p.parse_args();a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
