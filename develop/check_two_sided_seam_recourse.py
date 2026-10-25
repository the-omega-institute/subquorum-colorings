"""Two-sided seam selection budgets, full-pool ranks/costs and unbounded recourse.

General proofs: docs/TWO_SIDED_SEAM_BUDGET_AND_UNBOUNDED_RECOURSE.md.
Enumeration corroborates geometry and algorithms; it does not prove all sizes.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path

from check_forced_mates_and_adjacent_maxima import configuration, uniform_freezing, forced_order, verify_forced_mates, upper_certificate
from check_selection_maximum_singleton import compile_even_width
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import evaluate
from check_interface_reserve_reoptimization import constrained_primitive
from check_full_pool_interface_profile import closure
from check_residual_corridors import direct_check
from check_promotion_cores import frozen_certificate

if not __debug__: raise RuntimeError('Assertions required; do not use -O.')


@lru_cache(None)
def base_compiled(w,k):
    return compile_even_width(configuration(w,k))[0]


def model(w,k,upper,lower):
    base=configuration(w,k)
    removed={(0,10*i+1) for i in upper}|{(w+1,10*i+1) for i in lower}
    assert removed<=base[2]
    return (*base[:2],base[2]-removed,base[3])


def components(k,upper,lower):
    present=upper|lower;start=0;out=[]
    for i in range(1,k+1):
        if i==k or i not in present:
            doubles=sorted(j for j in upper&lower if start<j<i)
            out.append((start,i-1,doubles));start=i
    return out


def prescription(k,upper,lower):
    """Explicit maximum-value minimum-link allocation on the seam multigraph."""
    assignment={};cost=0;unpaid=[]
    for left,right,doubles in components(k,upper,lower):
        if not doubles:
            unpaid.append(left)
            for a in range(left+1,right+1):
                assignment[a]=(a,0 if a in lower else 1);cost+=1
        else:
            p=doubles[0]
            for a in range(left,right+1):
                edge=a+1 if a<p else a
                side=1 if a==p-1 else (0 if edge in lower else 1)
                assignment[a]=(edge,side);cost+=2 if a<p else 1
    assert len(set(assignment.values()))==len(assignment)
    return assignment,cost,unpaid


def route(w,a,edge,side):
    row=1 if side else w;c=10*a
    if edge==a:return [((row,c+5),(row,c+4))]
    assert edge==a+1
    return [((row,c+5),(row,c+6)),((row,c+7),(row,c+8))]


def inspect(w,k,upper,lower,totals,fixture=False):
    cur=model(w,k,upper,lower);P={v for e in cur[3] for v in e}
    direct_check(*cur);ranks,layers=uniform_freezing(w,k,cur)
    assert frozen_certificate(cur)[0]==P
    if fixture:leaf=verify_forced_mates(cur,forced_order(w,k))
    m=len(upper)+len(lower);t=(7*k+2)*(w//2)+3*k+2
    assert len(cur[2])==t-m
    d,meta=compile_even_width(cur);own,A,B,X=owner_data(*d[:2]);Q=d[4]
    old=base_compiled(w,k)
    assert d[:3]==old[:3]
    assert (len(A),len(B),len(X),len(Q),meta['slack'])==(k,0,7*k,3*k+m,2*k+m)
    units={(i,side):(0 if side else w//2,10*i+1,10*i+1)
           for side,edges in [(0,lower),(1,upper)] for i in edges}
    assert Q==old[4]|set(units.values()) and old[4].isdisjoint(units.values())
    roots=[];tables=[]
    for a in range(k):
        c=10*a
        ids={name:own[(r,c+col)] for name,r,col in [('A',1,5),('U0',1,3),('U1',1,6),('U2',1,8),('L0',w,3),('L1',w,6),('L2',w,8)]}
        roots.append(ids['A']);tables.append(ids)
        seen,edges=closure(d,{ids['A']});assert seen==set(ids.values())
        exits={'A':{'U0','U1','L0','L1'},'U1':{'U2'},'L1':{'L2'}}
        supports={name:({units[i,side]} if (i,side) in units else set())
            for name,i,side in [('U0',a,1),('U2',a+1,1),('L0',a,0),('L2',a+1,0)]}
        for name,o in ids.items():
            assert edges[o]=={ids[x] for x in exits.get(name,set())}
            assert d[3][o]==supports.get(name,set())
        totals['seven_owner_closures']+=1
    assert set(roots)==A and set(units.values())<=Q
    reachable,_=closure(d,A)
    assert set().union(set(),*(d[3][o] for o in reachable))==set(units.values())
    for (i,side),j in units.items():
        names=('U2','U0') if side else ('L2','L0')
        assert {o for o,js in d[3].items() if j in js}=={tables[i-1][names[0]],tables[i][names[1]]}
    comps=components(k,upper,lower);cyclic=sum(bool(ds) for _,_,ds in comps)
    doubles=len(upper&lower);deficit=len(comps)-cyclic;value=k-deficit
    mincost=value+sum(ds[0]-left for left,_,ds in comps if ds)
    allocation,cost,unpaid=prescription(k,upper,lower)
    assert len(allocation)==value and cost==mincost and len(unpaid)==deficit
    links=[];cert=[]
    for a,(edge,side) in sorted(allocation.items()):
        path=route(w,a,edge,side);j=units[edge,side]
        assert all(link in d[2] for link in path)
        assert j in d[3][own[path[-1][1]]]
        links+=path;cert.append(dict(source=a,owner=roots[a],unit=j,links=path))
    assert len({v for link in links for v in link})==2*len(links)
    assert evaluate(*d[:2],links,*d[3:])['value']==value
    f=fork_flow(*d);assert (f['value'],f['cost'],f['deficit'])==(value,mincost,deficit)
    assert meta['slack']+deficit==3*k+doubles-cyclic
    if w==8 and k<=4:
        assert constrained_primitive(d,set())==(value,mincost)
        totals['independent_primitive_profiles']+=1
    if lower==set(range(1,k)) and len(upper)==1:
        p=next(iter(upper));assert (value,mincost,m)==(k,k+p,k)
        # Every old source 1,...,p-1 is forced onto its RIGHT seam in any
        # full payment. Our witness keeps all other previously paid units.
        changes=sum(allocation[a]!=(a,0) for a in range(1,k))
        assert changes==p-1
        assert all(allocation[a][0]==a+1 for a in range(p))
        assert cost-(k-1)==p+1
        if k<=8:
            # Independent enumeration of ALL full incident assignments,
            # including the alternative allocation of the new upper unit.
            full=[]
            def enumerate_all(a,used,current):
                if a==k:
                    changed=sum(current[b]!=(b,0) for b in range(1,k))
                    links=sum(1 if edge==b else 2 for b,(edge,side) in current.items())
                    full.append((changed,links));return
                for unit in units:
                    if unit[0] in (a,a+1) and unit not in used:
                        enumerate_all(a+1,used|{unit},{**current,a:unit})
            enumerate_all(0,set(),{})
            assert len(full)==2 and min(x for x,_ in full)==p-1
            assert {links for _,links in full}=={k+p}
            totals['independent_all_full_assignment_recourse_enumerations']+=1
        totals['single_repair_exact_cost_and_old_assignment_recourse']+=1
    if fixture:
        payload=dict(W=w,k=k,upper_open=sorted(upper),lower_open=sorted(lower),shape=cur[:2],
            selected=sorted(cur[2]),matching=cur[3],freezing_layers=layers,
            unique_matching_leaf_certificate=leaf,pairs=d[1],roots=roots,
            owner_links=sorted({(own[u],own[v]) for u,v in d[2] if own[u]!=own[v]}),
            reachable=sorted(reachable),resources=sorted(Q),support=[(o,sorted(js)) for o,js in d[3].items()],
            new_units=sorted(units.values()),payments=cert,paid=value,min_links=mincost,
            true_fixed_P_maximum=t,constrained_maximum=t-m,slack=meta['slack'],
            old_value=k-1,old_min_links=k-1,old_assignment_changes=next(iter(upper))-1)
        (Path(__file__).parent/'fixtures/two_sided_seam_recourse.json').write_text(json.dumps(payload,indent=2)+'\n')
    totals['physical_frozen_boards']+=1;totals['freezing_events']+=len(ranks)
    return dict(W=w,k=k,upper=sorted(upper),lower=sorted(lower),selected=len(cur[2]),
                maximum=t,loss=m,value=value,cost=mincost,deficit=deficit,
                components=len(comps),cyclic_components=cyclic,double_seams=doubles,slack=meta['slack'])


def local_budget(w,k,totals):
    base=configuration(w,k);P={v for e in base[3] for v in e}
    cert=upper_certificate(w,k,base)
    assert cert['upper_bound']==(7*k+2)*(w//2)+3*k+2
    patches=[{(r+x,2+10*a+y) for x in range(4) for y in (0,1)} for r,a in itertools.product((0,w-2),range(k))]
    seen=set()
    for i,side in itertools.product(range(1,k),(0,1)):
        row=0 if side else w;tile={(r,c) for r in (row,row+1) for c in (10*i,10*i+1)}
        assert not seen&tile and all(not tile&p for p in patches);seen|=tile
        upper=(1 if side else w,10*i);lower=(0 if side else w+1,10*i)
        fixed=(upper[0],10*i-1)
        assert fixed in P and upper not in P and lower not in P
        # Open right column leaves only the two vertically adjacent left
        # cells. The one facing P cannot be selected with the other.
        assert sum(abs(a-b) for a,b in zip(upper,lower))==1
        assert sum(abs(a-b) for a,b in zip(upper,fixed))==1
        totals['disjoint_top_bottom_seam_tile_certificates']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[]
    for w in (8,10):
        for k in range(1,6):
            local_budget(w,k,totals)
            for states in itertools.product(range(4),repeat=k-1):
                up={i for i,s in enumerate(states,1) if s&1};lo={i for i,s in enumerate(states,1) if s&2}
                records.append(inspect(w,k,up,lo,totals,fixture=(w,k,up,lo)==(8,4,{3},{1,2,3})))
    for w,k in itertools.product((12,20,40,64),(3,8,16)):
        local_budget(w,k,totals);all_edges=set(range(1,k))
        for up,lo in [(all_edges,all_edges),({1},all_edges),({k-1},all_edges),
                       (set(range(1,k,2)),set(range(2,k,2)))]:
            records.append(inspect(w,k,up,lo,totals))
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='All top/bottom seam subsets on frozen explicit attainers; exact constrained maximum has written same-cover proof. Full original-pool reachable support, value/min-links and concrete disjoint payment witnesses; single-resource unbounded recourse.',
        limits=['Finite checks corroborate all-parameter written proofs.',
                'Endpoint family has vertical full compensation; no universal5over6 improvement.',
                'Recourse is original-unit assignment changes relative to the specified old optimum, not every possible notion of edit distance.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
