#!/usr/bin/env python3
"""Exact ledger and actual graph controls for the degree-dependent bound."""
import importlib.util
import json
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('original_general',ROOT/'scripts/check_selected_star_general_budget.py')
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
checks=0
for c,q,s,b2,b3,mu in product(range(5),repeat=6):
    if q>c or mu>b2:continue
    B0,C0,D0=c+2*q-b2-2*b3,c-q+b2+b3-mu,q+s+2*mu-2*b2
    if D0<0:continue
    for a in range(9):
        if a+2*b2+3*b3>c+s+2*q:continue
        t=a+b2+b3
        for d in range(1,1+min(B0//2,C0//2,(t-s)//2)):
            for r in range(7):
                n=5*c+2*s+q+t+r
                eta=n-12*d
                assert 4*eta>=9*s+b3+7*mu+4*r
                assert 6*eta>=q+13*s+10*mu+6*r
                for delta in range(2,6):
                    for maximum in range(delta,15):
                        if (delta-1)*a>maximum*r:continue
                        L=max(7*(delta-1),maximum)
                        assert d<=L*n//(12*L+2*(delta-1))
                        checks+=1
# Actual nonempty minimum-degree-two graph with selected-star positive gap.
g,s=original.gap_family(3,3)
n=len(g);edges=[(u,v) for u in range(n) for v in g[u] if u<v]
for i in range(3):edges.append((n,6*i+3))
for i in range(3,6):edges.append((n+1,6*i+3))
g=original.graph(n+2,edges)
assert min(map(len,g))>=2 and original.minimal(g,s)
col=original.colors(g);beta,subsets=original.one_part_beta(g,col)
d=len(s)-beta;maximum=max(map(len,g));M=max(7,maximum)
assert d>0 and d<=M*len(g)//(12*M+2)
report={'status':'PASS','finite_ledger_controls':checks,'graph_control':{'order':len(g),'selected_size':len(s),'beta':beta,'deficit':d,'minimum_degree':min(map(len,g)),'maximum_degree':maximum,'one_part_subsets':subsets,'bound':M*len(g)//(12*M+2)},'scope':'Necessary ledger controls and one actual graph. General proof is in docs/SELECTED_STAR_MINIMUM_DEGREE_BOUND.md.'}
(ROOT/'output/selected-star-degree-budget-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
