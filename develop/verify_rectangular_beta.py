#!/usr/bin/env python3
"""Exact, standard-library regression checks for the uniform beta_2 proof.
These finite tests are not a substitute for the written universal proof.
Run: python3 verify_rectangular_beta.py [--output verification.json]
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def g(n: int) -> int:
    return n - 2 * (n // 3)

def target(m: int, n: int) -> int:
    a = ((m+1)//2)*((2*n+2)//3)+(m//2)*(n//3)
    b = ((n+1)//2)*((2*m+2)//3)+(n//2)*(m//3)
    return max(a,b)

def horizontal_neighbors(mask: int, width: int) -> int:
    return mask & ((mask << 1) | (mask >> 1)) & ((1<<width)-1)

def valid_rows(width: int) -> list[int]:
    return [x for x in range(1<<width) if not (x & (x<<1) & (x<<2))]

def verify_path_expansion(limit: int) -> dict:
    checked = exceptions = 0
    for n in range(1,limit+1):
        full=(1<<n)-1
        odd=sum(1<<j for j in range(0,n,2))
        for p in range(1<<n):
            if p & (p<<1):
                continue
            nb=((p<<1)|(p>>1))&full
            deficit=p.bit_count()-nb.bit_count()
            exceptional=(n%2==1 and p==odd)
            require(deficit==1 if exceptional else deficit<=0,
                    f'path expansion: n={n}, mask={p}')
            checked+=1
            exceptions+=exceptional
    return {'maximum_path_order':limit,'independent_sets_checked':checked,
            'exceptional_sets':exceptions}

def verify_ladder(limit: int) -> dict:
    checked=equalities=0
    for n in range(1,limit+1):
        rows=valid_rows(n)
        odd=sum(1<<j for j in range(0,n,2))
        for p in rows:
            hp=horizontal_neighbors(p,n)
            for q in rows:
                if hp&q or horizontal_neighbors(q,n)&p:
                    continue
                weight=p.bit_count()+q.bit_count()
                require(weight<=n+n%2, f'ladder bound n={n}')
                if n%2 and weight==n+1:
                    require(p==q==odd, f'ladder rigidity n={n}')
                    equalities+=1
                checked+=1
    return {'maximum_width':limit,'valid_ladder_sets_checked':checked,
            'odd_width_extremizers':equalities}

def verify_profile(max_length: int, max_positive: int, min_negative: int) -> dict:
    checked=0
    for upper in range(1,max_positive+1,2):
        values=list(range(min_negative,upper+1,2))
        # State (last entry, length of positive suffix), retaining best sum.
        states={(v,int(v>0)):v for v in values}
        for m in range(1,max_length+1):
            optimum=max(states.values())
            bound=g(m) if m%2==0 else max(g(m),upper)
            require(optimum==bound,
                    f'profile m={m}, A={upper}: {optimum} != {bound}')
            checked+=1
            nxt={}
            for (last,run),score in states.items():
                for v in values:
                    if last+v>0 and not last==v==1:
                        continue
                    newrun=run+1 if v>0 else 0
                    if newrun>=3:
                        continue
                    key=(v,newrun)
                    nxt[key]=max(nxt.get(key,-10**9),score+v)
            states=nxt
    return {'maximum_length':max_length,'positive_upper_bounds':list(range(1,max_positive+1,2)),
            'minimum_test_entry':min_negative,'exact_profile_optimizations':checked}

def grid_optima(width: int, max_rows: int) -> list[int]:
    rows=valid_rows(width)
    h={p:horizontal_neighbors(p,width) for p in rows}
    compatible={p:[q for q in rows if not(h[p]&q or h[q]&p)] for p in rows}
    states={(0,0):0}
    values=[]
    for length in range(1,max_rows+1):
        nxt={}
        for (p,saturated),score in states.items():
            for q in compatible[p]:
                if q&saturated:
                    continue
                key=(q,h[q]|(p&q))
                nxt[key]=max(nxt.get(key,-1),score+q.bit_count())
        states=nxt
        optimum=max(states.values())
        require(optimum==target(length,width),f'grid {length}x{width}: {optimum}')
        values.append(optimum)
    return values

def verify_constructions(limit: int) -> dict:
    count=0
    for m in range(1,limit+1):
        for n in range(1,limit+1):
            def make(a:int,b:int) -> set[tuple[int,int]]:
                return {(i,j) for i in range(a) for j in range(b)
                        if (i%2==0 and j%3!=2) or (i%2==1 and j%3==2)}
            s=make(m,n)
            t={(j,i) for i,j in make(n,m)}
            for selected in (s,t):
                require(all(sum((i+di,j+dj) in selected for di,dj in
                                ((1,0),(-1,0),(0,1),(0,-1)))<=1
                            for i,j in selected),f'construction {m}x{n}')
            require(max(len(s),len(t))==target(m,n),'construction count')
            require(2*target(m,n)-m*n==max((m%2)*g(n),(n%2)*g(m)),
                    'algebraic normalization')
            count+=1
    return {'maximum_side':limit,'rectangles_checked':count,'constructions_per_rectangle':2}

def verify_boundary_controls() -> dict:
    T={1,3,6,9,12};M=[(0,4),(7,11),(13,14)];B={2,5,8,10,15}
    def neighbors(v:int) -> set[int]:
        r,c=divmod(v,4)
        return {i*4+j for i,j in ((r-1,c),(r+1,c),(r,c-1),(r,c+1))
                if 0<=i<4 and 0<=j<4}
    ends={v for edge in M for v in edge}
    A=T|ends
    require(len(ends)==2*len(M) and not T&ends,'matching disjointness')
    require(set(range(16))-A==B,'boundary partition')
    require(all(v in neighbors(u)for u,v in M),'matching edge support')
    require(all(len(neighbors(v)&A)<=1 for v in T),'pair feasibility')
    image=set().union(*(neighbors(v)for v in T))&B
    require(len(image)==4<len(T),'Hall counterexample')
    require(len(T)+len(M)==target(4,4),'counterexample preserves objective bound')
    require(target(101,103)==5219 and target(100,103)==5167,'symbolic examples')
    return {'grid':[4,4],'T':sorted(T),'M':M,'B':sorted(B),'N_B_T':sorted(image),
            'scope':'Covering-matching mechanism fails; numerical bound is attained.'}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('verification.json'))
    args=parser.parse_args()
    start=perf_counter()
    out={'scope':'Exact finite regression checks; universal theorem rests on written proof; no Lean verification.'}
    out['path_expansion']=verify_path_expansion(20)
    out['ladder_rigidity']=verify_ladder(10)
    out['odd_profile']=verify_profile(32,19,-39)
    out['constructions']=verify_constructions(40)
    out['boundary_control']=verify_boundary_controls()
    out['grid_beta_optima']={str(w):grid_optima(w,30) for w in range(1,9)}
    out['grid_beta_instance_count']=240
    out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out['elapsed_seconds']=round(perf_counter()-start,3)
    out['result']='ALL_CHECKS_PASSED'
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='grid_beta_optima'},indent=2))

if __name__=='__main__':
    main()
