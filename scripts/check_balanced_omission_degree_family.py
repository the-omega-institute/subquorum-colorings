#!/usr/bin/env python3
"""Physical checks of the balanced-omission sharpness family.
The exact dissociation cap is proved by cases, not solved here numerically.
"""
from itertools import combinations
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
import witness_interface_optimizer as opt
from check_sharp_minimum_two_degree import diss,literal
if not __debug__:raise RuntimeError('Assertions are required.')


def base(t,p):
    if type(t)is not int or type(p)is not int or t<2 or p<max(t,5)or 3*p%t:
        raise ValueError('Integer t>=2,p>=max(t,5),t dividing 3p required.')
    old,S=opt.graph(p,p,opt.degree_adjacency(p));n=12*p+2*t
    g=[set()for _ in range(n)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for a in range(12*p):
        for b in old[a]:
            if a<b<12*p:edge(a,b)
    A=tuple(range(12*p,12*p+t));B=tuple(range(12*p+t,n))
    for first,own,other in((0,A,B),(p,B,A)):
        for j in range(p):
            c=6*(first+j)
            for u in range(t):
                edge(own[u],c+3)
                if u!=3*j%t:edge(own[u],c+1)
                if u!=(3*j+1)%t:edge(own[u],c+2)
                if u!=(3*j+2)%t:edge(other[u],c)
    Q={6*j+a for j in range(2*p)for a in((0,1,3)if j<p else(1,2,4,5))}
    return g,S,Q


def lift(t,p,k):
    if type(k)is not int or k<1:raise ValueError('Positive integer k required.')
    old,S0,Q0=base(t,p);n=len(old);g=[set()for _ in range(n*k)]
    for j in range(k):
        for a in range(n):
            for b in old[a]:
                if a<b and(a,b)!=(5,6*p+5):g[n*j+a].add(n*j+b);g[n*j+b].add(n*j+a)
        a,b=n*j+5,n*((j+1)%k)+6*p+5;g[a].add(b);g[b].add(a)
    return g,{n*j+x for j in range(k)for x in S0},{n*j+x for j in range(k)for x in Q0}


def physical(t,p,k,delete_port=False):
    n0=12*p+2*t;g,S,Q=lift(t,p,k);delta=t+1;Delta=(4*t-3)*p//t
    if delete_port:
        assert k==1;g[5].remove(6*p+5);g[6*p+5].remove(5)
    assert len(g)==n0*k and len(S)==8*p*k and len(Q)==7*p*k
    expected_min=t if delete_port and p==t else delta
    assert min(map(len,g))==expected_min and max(map(len,g))==Delta and diss(g,Q)
    assert all(len(g[a])==p-(1 if delete_port else 0)+1 for a in(5,6*p+5))
    if not delete_port:
        assert {b for b in g[5]if b//n0!=0}==({n0+6*p+5}if k>1 else set())
    col={0:0};todo=[0]
    while todo:
        a=todo.pop();assert a not in g[a]
        for b in g[a]:
            assert a in g[b]
            if b not in col:col[b]=1-col[a];todo.append(b)
            assert col[b]!=col[a]
    assert len(col)==len(g)
    for x in set(range(len(g)))-S:assert literal(g,S,x)
    for x in S:
        copy,v=divmod(x,n0);j,kind=divmod(v,6)
        failure=n0*copy+6*j+{0:4,1:4,2:5,3:3}[kind]
        assert not literal(g,S,failure,x)
    for omitted in range(len(g)):
        root=next(x for x in range(len(g))if x!=omitted);seen={root};todo=[root]
        while todo:
            for b in g[todo.pop()]:
                if b!=omitted and b not in seen:seen.add(b);todo.append(b)
        assert len(seen)==len(g)-1
    pair_coverage=single_y=no_y=triple_coverage=0
    for copy in range(k):
        o=copy*n0;A=set(range(o+12*p,o+12*p+t));B=set(range(o+12*p+t,o+n0))
        assert all(len(g[a])==Delta for a in A|B)
        assert all(g[a]<=S for a in A|B)
        for first,own,other in((0,A,B),(p,B,A)):
            I={o+6*(first+j)+3 for j in range(p)}
            leaves={o+6*(first+j)+a for j in range(p)for a in(1,2)}
            oppositeC={o+6*((p-first)+j)for j in range(p)}
            ys={o+6*(first+j)+2 for j in range(p)}
            for a in own:
                assert I<=g[a]
                if g[a]&ys:single_y+=1
                else:
                    assert {o+6*(first+j)+1 for j in range(p)}<=g[a]
                    no_y+=1
                assert len(g[a]&leaves)>=p
            for a,b in combinations(sorted(own),2):
                assert I|leaves|oppositeC <= g[a]|g[b]
                pair_coverage+=1
            for triple in combinations(sorted(own),3):
                assert all(sum(v in g[a]for a in triple)>=2 for v in I|leaves|oppositeC)
                triple_coverage+=1
            for j in range(p):
                x,y=o+6*(first+j)+1,o+6*(first+j)+2
                assert len(own-g[x])==len(own-g[y])==1 and own-g[x]!=own-g[y]
        for j in range(p):
            L=[o+6*j+a for a in(4,5)];R=[o+6*(p+(j+1)%p)+a for a in(4,5)]
            assert all(b in g[a]for a in L for b in R)
    case_checks=0
    for qA in range(t+1):
        for qB in range(t+1):
            m=qA+qB
            if m==0:bound=7*p
            elif m==1:bound=7*p # no-y subcase also has 6p+2<=7p
            elif m<=3:bound=6*p+2+m
            elif qA==qB==2:bound=2*p+8
            elif not qA or not qB:bound=6*p+m
            else:bound=4*p+1+m
            assert bound<=7*p
            case_checks+=1
    assert 6*p+2<=7*p
    assert Delta*len(g)==(12*Delta+8*delta-14)*(len(S)-len(Q))
    return {'t':t,'p':p,'k':k,'safe_edge_deleted':delete_port,'order':len(g),
            'selected':len(S),'attaining_set_size':len(Q),'minimum_degree':min(map(len,g)),'completed_graph_minimum_degree':delta,
            'maximum_degree':Delta,'literal_deletion_failures':len(S),
            'single_vertex_deletion_checks':len(g),'same_side_pair_coverage_checks':pair_coverage,
            'single_connector_y_checks':single_y,'single_connector_no_y_checks':no_y,
            'same_side_triple_coverage_checks':triple_coverage,'case_capacity_checks':case_checks,
            'boundary_piece_below_target_minimum':delete_port and p==t,
            'beta_cap_source':'Analytical cases; no exhaustive large-graph solve.'}


def main():
    invalid=0
    for t,p in((1,6),(2,4),(6,4),(5,6),(True,6),(3,False),(3,6.0)):
        try:base(t,p)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid domain accepted.')
    for k in(0,-1,True,1.5):
        try:lift(3,6,k)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid lift accepted.')
    params=((3,5),(5,5),(2,6),(3,6),(3,7),(3,8),(3,9),(4,8),(5,10),
            (6,6),(6,8),(6,10),(7,7),(8,8),(9,9),(9,12),(12,12),(12,16))
    models=[physical(t,p,k)for t,p in params for k in(1,2)]
    models +=[physical(t,p,1,True)for t,p in params]
    models +=[physical(t,p,3)for t,p in((3,5),(5,5),(3,7),(6,6),(9,12))]
    # Whole finite parameter window: arithmetic/omission balance only.
    arithmetic=0
    for t in range(2,41):
        for p in range(max(t,5),121):
            if 3*p%t:continue
            counts=[sum((3*j+a)%t==u for j in range(p)for a in range(3))for u in range(t)]
            assert counts==[3*p//t]*t
            Delta=(4*t-3)*p//t
            assert Delta*(12*p+2*t)==(12*Delta+8*(t+1)-14)*p
            assert Delta>=t+1 and p+1>=t+1
            arithmetic+=1
    report={'status':'PASS','models':models,'invalid_domains_rejected':invalid,
            'arithmetic_parameters':arithmetic,
            'scope':'Physical construction, literal stars/deletions, bipartition, '
                    'attaining set, slots, connector pairs/triples, single-no-y case, '
                    'all vertex deletions and sharpness arithmetic. At p=t the '
                    'deleted piece has minimum t, while completed lifts have t+1. '
                    'The infinite-parameter exact beta cap uses the written proof; '
                    'no exhaustive large-graph dissociation optimization is claimed.'}
    out=ROOT/'output/balanced-omission-degree-check.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(models),
                      'arithmetic_parameters':arithmetic,
                      **{name:sum(x[name]for x in models)for name in(
                         'literal_deletion_failures','single_vertex_deletion_checks',
                         'single_connector_no_y_checks','same_side_pair_coverage_checks',
                         'same_side_triple_coverage_checks','case_capacity_checks')},
                      'boundary_deleted_pieces':sum(x['boundary_piece_below_target_minimum']for x in models)},sort_keys=True))


if __name__=='__main__':main()
