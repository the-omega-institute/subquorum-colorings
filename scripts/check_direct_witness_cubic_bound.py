#!/usr/bin/env python3
"""Literal exchange controls and exact cubic/signed identities.
Requires the two preceding public standalone checkers as utility modules.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import check_selected_star_general_budget as old
import check_full_degree_capacity as cut

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def identity(v):
    c,q,s,a,b2,b3,mu,m,z0,u=v
    n,(J,T,R,D,F,B)=cut.values(v,3,3)
    Tp=T-q
    assert J+R+Tp==2*c-b3-mu
    assert F+3*B==m+c+s
    assert n==2*J+2*R+4*Tp+5*B+2*F+2*(s+q+b3+mu+z0)
    return n,J,Tp,R,F,B


def audit(g,S,beta,count):
    col=old.colors(g)
    C,L,I=old.structure(g,S)
    d=len(S)-beta
    for v,W,U,P,H in cut.allocations(g,S):
        c,q,s,a,b2,b3,mu,m,z0,u=v
        n,J,Tp,R,F,B=identity(v)
        assert n==len(g) and B==2*len(S)-n
        sets=[]
        for side in (0,1):
            chosen_W={w for w in W if col[w]==side}
            helpers={i for i in I if g[i]&chosen_W}
            D=((S-C)|chosen_W)-helpers
            assert old.diss(g,D) and len(D)<=beta
            sets.append(D)
        assert sum(map(len,sets))==2*len(S)+s+q-(a+b2+b3)
        assert J>=0 and min(Tp,R,B)>=2*d
        assert 4*beta-2*len(S)-n >= m+z0-u+s+(b3+mu)/2
        # Integer-scaled check avoids relying on floating arithmetic.
        assert 2*(4*beta-2*len(S)-n)>=2*(m+z0-u+s)+b3+mu
        assert 4*beta>=2*len(S)+n-u
        if max(map(len,g),default=0)<=3:
            eps_S=sum(3-len(g[x])for x in S)
            eps_U=sum(3-len(g[x])for x in U)
            Fhat=F+eps_S-eps_U
            actual=c+s+2*q-H+sum(len(g[x]&U)for x in U)+sum(len(g[x]&W)for x in U)
            assert Fhat==actual>=0
            assert 22*d<=n+2*eps_S-2*eps_U
            assert d<=(n+2*eps_S-2*eps_U)//22
            count['subcubic_boundary_allocations']+=1
            count['negative_boundary_differences']+=eps_S<eps_U
        if g and min(map(len,g))==max(map(len,g))==3:
            assert F>=0 and 22*d<=n
            count['cubic_allocations']+=1
        count['allocations']+=1
        count['actual_exchange_sets']+=2
        count['direct_only_allocations']+=q>0
        count['positive_gap_allocations']+=d>0
        count['witness_conflict_allocations']+=any(g[w]&W for w in W)
        count['strict_improvements_over_leaf_only']+=q>0


def graphs():
    for a,b in product(range(1,4),repeat=2):
        possible=list(product(range(a),range(a,a+b)))
        for mask in range(1<<len(possible)):
            yield 'all_parts_1_through_3',old.graph(a+b,[e for i,e in enumerate(possible)if mask>>i&1])
    yield from cut.models()


def graph_controls():
    count=Counter();ranges={}
    for label,g in graphs():
        col=old.colors(g)
        beta,subsets=old.one_part_beta(g,col)
        assert beta==old.beta_literal(g)
        if len(g)<=6:assert beta==old.beta_full_subsets(g)
        formed=cut.literals(g)
        row=Counter()
        for mask,ok in enumerate(formed):
            row['selected_subsets']+=1
            if not ok or any(formed[mask^(1<<v)] for v in range(len(g))if mask>>v&1):continue
            S={v for v in range(len(g))if mask>>v&1}
            if old.structure(g,S)is None:continue
            row['eligible_minimal_selections']+=1
            audit(g,S,beta,row)
        row['graph_inputs']+=1;row['one_part_subsets']+=subsets
        count.update(row);ranges.setdefault(label,Counter()).update(row)
    return {'totals':dict(sorted(count.items())),
            'ranges':{k:dict(sorted(v.items()))for k,v in sorted(ranges.items())},
            'scope':'All labelled fixed-part graphs with each part1..3; previous explicitly labelled regular/nonregular finite models. Inputs, not necessarily distinct adjacency lists.'}


def padding(a,b,t):
    g,S=old.gap_family(a,b);col=old.colors(g);n=len(g)
    A={v for v in range(n)if col[v]==0};B=set(range(n))-A
    X=set(range(n,n+t));Y=set(range(n+t,n+2*t))
    edges=[(u,v)for u in range(n)for v in g[u]if u<v]
    edges+=list(product(X,B|Y))+list(product(A,Y))
    return old.graph(n+2*t,edges),S


def targets():
    models=[('direct_parallel',old.fixture([(0,0),(0,0),(1,0),(1,0)],dense=True)),
            ('direct_large_helper',old.fixture([(0,0)]*3+[(1,0)]*3,dense=True)),
            ('mixed_clean_direct',old.fixture([(0,None),(0,0),(1,0),(1,1)],dense=True)),
            ('surplus_and_extras',old.fixture([(0,None),(0,0),(0,0),(1,None),(1,0)],True,True)),
            ('multiple_witness_choices',old.multiple_options()),
            ('shared_helper_centres',old.shared_two_centres()),
            ('sharp_universal_selected_star',old.gap_family(2,2)),
            ('padding_correction_tight',padding(2,2,2)),
            ('oracle22_counterexample',padding(1,2,2))]
    rows=[]
    for name,(g,S)in models:
        assert old.minimal(g,S)and old.structure(g,S)is not None
        beta,subsets=old.one_part_beta(g,old.colors(g))
        if len(g)<=24:assert beta==old.beta_literal(g)
        count=Counter();audit(g,S,beta,count)
        rows.append({'name':name,'order':len(g),'selected':len(S),'beta':beta,
                     'one_part_subsets':subsets,'checks':dict(sorted(count.items()))})
        if name=='padding_correction_tight':
            assert 4*beta-2*len(S)-len(g)==-4
    # Positive d and direct-only centres in one actual selection.
    direct=old.fixture([(0,0),(0,1),(1,0),(1,1)],dense=True)
    g,S=old.disjoint(old.gap_family(3,3),direct)
    direct_beta,subsets=old.one_part_beta(direct[0],old.colors(direct[0]))
    beta=21+direct_beta
    assert old.minimal(g,S)and len(S)>beta
    count=Counter();audit(g,S,beta,count)
    assert count['direct_only_allocations']and count['positive_gap_allocations']
    rows.append({'name':'positive_gap_with_direct_centres','order':len(g),'selected':len(S),'beta':beta,
                 'beta_method':'accepted beta(G_(3,3))=21 plus independent one-part optimum on the other disjoint component',
                 'component_one_part_subsets':subsets,'checks':dict(sorted(count.items()))})
    return rows


def arithmetic():
    for i in range(10):
        v=[0]*10;v[i]=1;identity(v)
    for exponent in (64,401,1024):identity([(j+1)*(10**exponent+7)for j in range(10)])
    v=[2,0,0,2,0,0,0,4,0,6]
    assert identity(v)==(22,0,2,2,0,2)
    return {'basis_identity_checks':10,'large_integer_checks':3,
            'numerical_relaxation_point':[v,22],
            'graph_sharpness_claim':False}


def main():
    report={'status':'PASS','graph_controls':graph_controls(),'targeted':targets(),
            'arithmetic':arithmetic(),'scope':'Finite literal controls; the complete general proof supplies all-graph conclusions.'}
    path=Path(__file__).resolve().parents[1]/'output/direct-witness-cubic-check.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','totals':report['graph_controls']['totals'],'targeted_models':len(report['targeted'])},sort_keys=True))


if __name__=='__main__':main()
