#!/usr/bin/env python3
"""Literal graph/exchange controls for the free-unused-vertex theorem.
Standard library only. General conclusions are proved in the companion note.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import check_selected_star_general_budget as old
import check_full_degree_capacity as cut

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def audit(g, S, beta, count):
    col=old.colors(g); C,L,I=old.structure(g,S); L=set(L)
    d=len(S)-beta; minimum=min(map(len,g)); maximum=max(map(len,g))
    for v,W,U,P,unused in cut.allocations(g,S):
        c,q,s,a,b2,b3,mu,m,z0,u=v
        h={i:len(g[i]&W)for i in I}
        touched={i for i in I if h[i]}; untouched=I-touched
        Z={x for x in U if g[x]&S<=C|touched}; free=len(Z)
        assert U-Z=={x for x in U if g[x]&(L|P|untouched)}
        sets=[]
        for side in (0,1):
            chosen={w for w in W if col[w]==side}
            helpers={i for i in I if g[i]&chosen}
            D=((S-C)|chosen)-helpers
            extra={x for x in Z if col[x]==side}
            assert all(not(g[x]&D)for x in extra)
            assert old.diss(g,D|extra)and len(D|extra)<=beta
            sets.append(D|extra)
        t=a+b2+b3; Tp=t-s-q
        J=c+s+2*q-t-b2-2*b3; R=c-q+b2+b3-mu
        D=q+s+2*mu-2*b2; H=b3+mu
        assert sum(map(len,sets))==2*len(S)+s+q-t+free
        assert J>=0 and D>=0 and R>=2*d and Tp-free>=2*d
        assert 2*len(g)==5*J+5*R+7*Tp+5*H+6*s+4*q+2*(m+z0+u)
        eta=len(g)-12*d
        assert 2*eta>=2*u+7*free+5*H+6*s+4*q+2*(m+z0)
        assert 4*d<=2*(a+H-free)-(s+q)
        single={i for i in I if h[i]==1}
        edges={(i,x)for i in single for x in g[i]&U}
        assert all(len(g[i]&U)>=minimum-1 for i in single)
        assert len(edges)==sum(len(g[x]&single)for x in U)
        assert all(len(g[x]&single)<=maximum-1 for x in U-Z)
        assert len(edges)<=(maximum-1)*u+free
        for lower in range(2,minimum+1):
            for upper in range(maximum,maximum+3):
                A=upper-1; B=lower-1
                assert B*a<=A*u+free
                assert 4*B*d<=2*A*u+2*B*H-B*(s+q)-2*(lower-2)*free
                remainder=(7*A+2*lower-4)*free+(5*A-2*B)*H
                remainder+=(6*A+B)*s+(4*A+B)*q+2*A*(m+z0)
                assert 2*A*eta-4*B*d>=remainder>=0
                assert d<=A*len(g)//(12*A+2*B)
                if lower>=3 and d>0:assert (12*A+2*B)*d<A*len(g)
                count['degree_parameter_checks']+=1
        count['allocations']+=1; count['actual_enlarged_exchanges']+=2
        count['free_vertices_checked']+=free
        count['nonfree_vertices_checked']+=u-free
        count['h1_isolate_cut_edges']+=len(edges)
        count['with_free_vertices']+=bool(free)
        count['with_nonfree_vertices']+=u>free
        count['both_free_and_nonfree']+=0<free<u
        count['positive_gap_allocations']+=d>0
        count['direct_only_allocations']+=q>0
        count['isolate_helper_ge3_allocations']+=b3>0
        count['selected_edge_allocations']+=m>0
        count['untouched_isolate_allocations']+=z0>0


def small_graphs():
    for a,b in list(product(range(1,4),repeat=2))+[(3,4)]:
        possible=list(product(range(a),range(a,a+b)))
        for mask in range(1<<len(possible)):
            g=old.graph(a+b,[e for i,e in enumerate(possible)if mask>>i&1])
            if min(map(len,g))>=2:yield 'all_minimum2_parts_'+str(a)+'_'+str(b),g
    yield from cut.models()
    for h,w in [(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4)]:
        es=[]
        for r,c in product(range(h),range(w)):
            if r+1<h:es.append((r*w+c,(r+1)*w+c))
            if c+1<w:es.append((r*w+c,r*w+c+1))
        yield 'rectangle_'+str(h)+'_'+str(w),old.graph(h*w,es)


def controls():
    totals=Counter(); ranges={}
    for label,g in small_graphs():
        beta,subsets=old.one_part_beta(g,old.colors(g))
        assert beta==old.beta_literal(g)
        if len(g)<=7:assert beta==old.beta_full_subsets(g)
        formed=cut.literals(g); row=Counter()
        for mask,ok in enumerate(formed):
            row['selected_subsets']+=1
            if not ok or any(formed[mask^(1<<x)]for x in range(len(g))if mask>>x&1):continue
            S={x for x in range(len(g))if mask>>x&1}
            if old.structure(g,S)is None:continue
            row['eligible_minimal_selections']+=1; audit(g,S,beta,row)
        row['graph_inputs']+=1; row['one_part_subsets']+=subsets
        totals.update(row);ranges.setdefault(label,Counter()).update(row)
    return {'totals':dict(sorted(totals.items())),
            'ranges':{k:dict(sorted(v.items()))for k,v in sorted(ranges.items())},
            'scope':'All fixed-part labelled minimum-degree-at-least-2 graphs with parts1..3 and(3,4); explicitly labelled earlier regular/seeded models; seven stated rectangles. Inputs may repeat adjacency lists.'}


def pad(a,b,t):
    g,S=old.gap_family(a,b);col=old.colors(g);n=len(g)
    A={x for x in range(n)if col[x]==0}; B=set(range(n))-A
    X=set(range(n,n+t));Y=set(range(n+t,n+2*t))
    es=[(u,v)for u in range(n)for v in g[u]if u<v]
    return old.graph(n+2*t,es+list(product(X,B|Y))+list(product(A,Y))),S


def targets():
    g,S=old.gap_family(3,3);n=len(g)
    es=[(u,v)for u in range(n)for v in g[u]if u<v]
    es+=[(n,6*j+3)for j in range(3)]+[(n+1,6*j+3)for j in range(3,6)]
    models=[('minimum2_order38',(old.graph(n+2,es),S)),
            ('universal_padding_order26',pad(2,2,1)),
            ('padding_minimum3',pad(2,2,2)),
            ('multiple_witness_choices',old.multiple_options()),
            ('direct_large_helper',old.fixture([(0,0)]*3+[(1,0)]*3,dense=True)),
            ('shared_helper_centres',old.shared_two_centres()),
            ('surplus_edges_untouched',old.fixture([(0,None),(0,0),(0,0),(1,None),(1,0)],True,True))]
    base,T=old.gap_family(2,2);es=[(u,v)for u in range(24)for v in base[u]if u<v]
    for extra in (False,True):
        more=[(24,3),(24,9),(25,15),(25,21)]
        if extra:more +=[(24,2),(25,14)]
        models.append(('minimum2_order26_'+str(extra),(old.graph(26,es+more),T)))
    rows=[]
    for name,(g,S)in models:
        assert old.minimal(g,S)and old.structure(g,S)is not None
        beta,subsets=old.one_part_beta(g,old.colors(g))
        if len(g)<=24:assert beta==old.beta_literal(g)
        row=Counter(); audit(g,S,beta,row)
        rows.append({'name':name,'order':len(g),'selected':len(S),'beta':beta,
                     'minimum_degree':min(map(len,g)),'maximum_degree':max(map(len,g)),
                     'one_part_subsets':subsets,'checks':dict(sorted(row.items()))})
    return rows


def arithmetic():
    def identity(v):
        c,q,s,a,b2,b3,mu,m,z0,u=v; t=a+b2+b3
        J=c+s+2*q-t-b2-2*b3; R=c-q+b2+b3-mu; Tp=t-s-q
        n=5*c+2*s+q+t+m+z0+u
        assert 2*n==5*J+5*R+7*Tp+5*(b3+mu)+6*s+4*q+2*(m+z0+u)
    for j in range(10):
        v=[0]*10;v[j]=1;identity(v)
    for exponent in (64,401,1024):identity([(j+1)*(10**exponent+7)for j in range(10)])
    return {'basis_identity_checks':10,'large_integer_checks':3,'graph_sharpness_claim':False}


def main():
    report={'status':'PASS','graph_controls':controls(),'targeted':targets(),'arithmetic':arithmetic(),
            'scope':'Actual enlarged exchange sets and physical edge capacities. Complete general proof supplies all-graph bound. Finite controls do not establish sharpness.'}
    out=Path(__file__).resolve().parents[1]/'output/free-unused-degree-refinement-check.json'
    out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','totals':report['graph_controls']['totals'],'targeted_models':len(report['targeted'])},sort_keys=True))


if __name__=='__main__':main()
