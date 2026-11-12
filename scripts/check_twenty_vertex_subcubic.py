#!/usr/bin/env python3
"""Independent literal controls for the robust twenty-vertex construction."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import random
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
from twenty_vertex_subcubic import block,cyclic_family
if not __debug__:raise RuntimeError('Run with assertions enabled')
COUNTS=Counter()
DIGEST=hashlib.sha256()


def add(g,a,b):g[a].add(b);g[b].add(a)


def independent_block():
    # Independent specification, not parsed from the generator fixture.
    g=[set() for _ in range(20)]
    cycle=[0,4,11,3,10,7,1,6,8,2,9,5]
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):add(g,a,b)
    for x in range(5,12):add(g,x,x+8)
    for left,right in (((12,13),(16,19)),((14,15),(17,18))):
        for a in left:
            for b in right:add(g,a,b)
    return g


def diss(g,D):return all(len(g[v]&D)<=1 for v in D)


def literal_forms(g,S):
    # Enumerate the physical two-leaf stars, without the local predicate.
    return all(any(x in {c,a,b} and len({c,a,b}&S)==2
                   for c in {x}|g[x] for a,b in combinations(g[c],2))
               for x in set(range(len(g)))-S)


def exact(g):
    adj=[sum(1<<u for u in ns) for ns in g]
    @lru_cache(None)
    def go(mask):
        if not mask:return 0
        v=max((i for i in range(len(g)) if mask>>i&1),key=lambda i:(adj[i]&mask).bit_count())
        ns=adj[v]&mask
        if not ns:return mask.bit_count()
        closed=ns|(1<<v)
        ans=max(go(mask&~(1<<v)),1+go(mask&~closed))
        while ns:
            bit=ns&-ns;ns-=bit
            ans=max(ans,2+go(mask&~(closed|adj[bit.bit_length()-1])))
        return ans
    return go((1<<len(g))-1)


def literal_subsets(g):
    # Every subset, using its unique smaller subset: no optimisation search.
    adj=[sum(1<<u for u in ns) for ns in g]
    valid=bytearray(1<<len(g));valid[0]=1
    profile={str((a,b)):-1 for a in range(3) for b in range(3)}
    best=0;number=0
    for mask in range(1<<len(g)):
        if mask:
            bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit
            ns=adj[v]&rest
            valid[mask]=bool(valid[rest] and ns.bit_count()<=1 and
                (not ns or not(adj[ns.bit_length()-1]&rest)))
        if not valid[mask]:continue
        number+=1;size=mask.bit_count();best=max(best,size)
        states=tuple(0 if not(mask>>p&1) else 1+bool(adj[p]&mask) for p in (4,12))
        profile[str(states)]=max(profile[str(states)],size)
    COUNTS['literal_subsets_checked']+=1<<len(g)
    return {'beta':best,'valid_subsets':number,'port_profiles':profile}


def connected(g,deleted=None):
    available=set(range(len(g)))-({deleted} if deleted is not None else set())
    if not available:return True
    seen={next(iter(available))};todo=list(seen)
    while todo:
        for u in g[todo.pop()]:
            if u in available and u not in seen:seen.add(u);todo.append(u)
    return seen==available


def canonical_check(g,S,col,D,r):
    n=len(g)
    assert n==20*r and sum(map(len,g))==56*r
    assert Counter(map(len,g))=={2:4*r,3:16*r}
    assert Counter(col)=={0:10*r,1:10*r}
    assert all(v!=u and v in g[u] and col[v]!=col[u] for v,ns in enumerate(g) for u in ns)
    assert len(D)==11*r and diss(g,D)
    I={20*i+j for i in range(r) for j in range(4)}
    C={20*i+j for i in range(r) for j in range(12,20)}
    assert S==I|C and len(S)==12*r
    assert all(not g[i]&S for i in I)
    ownership={}
    for x in set(range(n))-S:
        assert len(g[x]&S)==2 and len(g[x]&I)==1 and len(g[x]&C)==1
        owner=next(iter(g[x]&C));assert owner not in ownership;ownership[owner]=x
    assert set(ownership)==C
    # Explicit uncovered vertex for every selected deletion.
    for v in S:
        x=v if v in I else ownership[v]
        ns=g[x]&(S-{v})
        assert not ns if v in I else len(ns)==1 and not(g[next(iter(ns))]&(S-{v}))
    COUNTS['deletion_failure_certificates']+=len(S)
    if r<=4:
        assert literal_forms(g,S)
        assert all(not literal_forms(g,S-{v}) for v in S)
        COUNTS['literal_family_minimal_sets']+=1
    if r<=16:
        assert connected(g) and all(connected(g,v) for v in range(n))
        COUNTS['vertex_deletion_connectivity_checks']+=n
    DIGEST.update(json.dumps([r,sorted(S),sorted(D)],separators=(',',':')).encode()+b'\n')
    COUNTS['cyclic_family_certificates']+=1


def main():
    f,S,col,D=block();ref=independent_block()
    assert f==ref and len(D)==11 and not D&{4,12} and diss(f,D)
    fixture=json.loads((ROOT/'develop/fixtures/twenty-vertex-subcubic-core.json').read_text())
    ham=fixture['hamilton_cycle_after_deletion']
    assert sorted(ham)==list(range(20)) and all(b in f[a] for a,b in zip(ham,ham[1:]+ham[:1]))
    c=fixture['helper_witness_cycle'];C=set(range(12,20))
    periodic=[]
    for cycle_selection in combinations(c,8):
        T=set(cycle_selection)
        if not diss(f,T):continue
        available={v for v in C if not f[v]&T}
        core_beta=exact([{sorted(available).index(u) for u in f[v]&available} for v in sorted(available)])
        assert core_beta<=3
        periodic.append({'selected_cycle':sorted(T),'available_core':sorted(available),'core_beta':core_beta})
    assert len(periodic)==3
    COUNTS['cycle_eight_set_candidates']=len(list(combinations(c,8)))
    COUNTS['cycle_eight_set_survivors']=3
    full=[set(ns) for ns in f];add(full,4,12)
    profiles={'F':literal_subsets(f),'H':literal_subsets(full)}
    assert profiles['F']['beta']==profiles['H']['beta']==11
    assert exact(f)==exact(full)==11
    assert literal_forms(full,S) and all(not literal_forms(full,S-{v}) for v in S)
    # In F all nine states occur. Restoring the port edge forces both selected
    # ports to be internally paired, ruling out three states in H.
    assert all(x>=0 for x in profiles['F']['port_profiles'].values())
    assert sum(x>=0 for x in profiles['H']['port_profiles'].values())==6
    for r in list(range(1,17))+[32,64,128,256]:
        m=cyclic_family(r)
        canonical_check(m['g'],m['selected'],m['colour'],m['dissociation'],r)
        COUNTS['family_vertices_checked']+=len(m['g'])
    rng=random.Random(20112026)
    # Exact unrestricted attachment optima, including nonbipartite exteriors.
    for n in range(7):
        for k in range(8):
            tail=[set() for _ in range(n)]
            for a,b in combinations(range(n),2):
                if rng.randrange(2):add(tail,a,b)
            g=[set(ns) for ns in f]+[{20+u for u in ns} for ns in tail]
            for p in (4,12):
                for v in range(n):
                    if rng.randrange(2):add(g,p,20+v)
            if k%2:add(g,4,12)
            assert exact(g)==11+exact(tail)
            COUNTS['exact_arbitrary_attachment_optima']+=1
            COUNTS['nonbipartite_exteriors']+=any(b in tail[a] and c in tail[a] and c in tail[b]
                for a,b,c in combinations(range(n),3))
    # Large arbitrary interfaces: use explicit port-avoiding optima, not a claim
    # that an unrestricted solver ran on these larger instances.
    for r in (2,3,5,9,32):
        for k in range(4):
            g=[{20*i+u for u in ns} for i in range(r) for ns in f]
            ports=[20*i+p for i in range(r) for p in (4,12)]
            for a,b in combinations(ports,2):
                if rng.randrange(4)==0:add(g,a,b)
            chosen={20*i+v for i in range(r) for v in D}
            assert diss(g,chosen) and len(chosen)==11*r
            COUNTS['arbitrary_multiport_certificates']+=1
    for bad in (0,-1,1.5,True):
        try:cyclic_family(bad)
        except ValueError:COUNTS['invalid_inputs_rejected']+=1
        else:raise AssertionError(bad)
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/twenty-vertex-subcubic-check.json')
    args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    report={'schema_version':1,'counts':dict(sorted(COUNTS.items())),
            'literal_block_enumeration':profiles,'cycle_cases':periodic,
            'deterministic_certificate_sha256':DIGEST.hexdigest(),
            'scope':{'general_proofs':'Note proves beta(F)=11, arbitrary port composition, and all-r topology/minimality/gap.',
                     'exact_optima':'Two literal2^20 block enumerations and56 one-block/exterior exact recursion comparisons.',
                     'larger_models':'Actual dissociation and minimal-set certificates; no large exact SF optimisation.',
                     'open':'Exact SF(G_r) for generalr, sharp subcubic coefficient, general8b/3 template and arbitrary grid equality.',
                     'no_Lean_or_submission':True}}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(args.output),'counts':report['counts']}))

if __name__=='__main__':main()
