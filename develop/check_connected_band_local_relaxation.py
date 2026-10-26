"""An exact rational barrier to a specified local-certificate strategy.

This is a fractional occupation witness, not a feasible integer matching.
No solver is used. Infinite-period and finite-boundary inequalities are exact.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import endpoints,free_vertices
from check_lower_guard_merger_frontier import actual_components,guard,lower_guard,JOINT,LOWER
from check_occupied_strip_degree_four_budget import family
from check_successor_guard_compensation import JOINT_GF,ONLY_F,successor_guard
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

PERIOD_DATA=[
    ((2,3),'1','1'),((2,5),'0','1'),
    ((3,3),'0','7/12'),((3,4),'2/3','1'),((3,5),'0','3/4'),
    ((4,0),'1/3','1/2'),((4,1),'1/2','2/3'),((4,2),'1/3','1/2'),
    ((4,3),'23/36','2/3'),((4,4),'1/3','1/3'),((4,5),'7/12','2/3'),
    ((5,0),'2/3','2/3'),((5,1),'1/2','1/2'),((5,2),'2/3','2/3'),
    ((5,3),'1/2','2/3'),((5,4),'2/3','2/3'),((5,5),'1/2','2/3'),
]
PERIOD={v:(Q(t),Q(o)) for v,t,o in PERIOD_DATA}
WINDOWS=[('gh13',JOINT,16),('h7',LOWER,10),
         ('gf13',JOINT_GF,16),('f10',ONLY_F,12)]


def reduced(v):return v[0],v[1]%6


def old_count(v):
    r,c=reduced(v)
    if (r,c)==(2,5):return 2
    return int((r==3 and c in (3,5)) or (r==4 and c in (0,1,2)))


def connected_cells(m):
    assert m>=2
    return ({(2,c+6*j) for j in range(m) for c in (9,11)} |
            {(3,c+6*j) for j in range(m) for c in (9,10,11)} |
            {(4,c) for c in range(8,6*m+5)} |
            {(5,c) for c in range(7,6*m+6)})


def vertex_inequalities(v,ns,c,counts):
    t,o=PERIOD[reduced(v)];nt=lambda u:PERIOD[reduced(u)][1]
    assert 0<=t<=o<=1;counts['bound_and_subset_checks']+=1
    if c>=2:assert t==0;counts['forbidden_selection_checks']+=1
    if c>=1:
        for u in ns:
            assert t+nt(u)<=1;counts['anchored_pair_checks']+=1
    # Also check all ordinary wedges, including vertices with old anchors.
    for a,b in itertools.combinations(sorted(ns),2):
        assert t+nt(a)+nt(b)<=2;counts['wedge_checks']+=1
    assert (len(ns)+c-1)*t+sum(map(nt,ns))<=len(ns)
    counts['full_selected_degree_checks']+=1
    if v[0]==5:
        assert sum(sum(PERIOD[reduced(u)]) for u in set(ns)|{v})<=6
        counts['bottom_closed_star_cuts']+=1


def period_controls(counts):
    domain=set(PERIOD)
    for v in sorted(domain):
        ns={reduced(u) for u in neighbors(v)}&domain
        vertex_inequalities(v,ns,old_count(v),counts)
    for name,pattern,b in WINDOWS:
        value=sum(sum(PERIOD[r,(c+9)%6]) for r,c in pattern)
        assert value<=b;counts['period_window_'+name]+=1
    assert sum(sum(v) for v in PERIOD.values())==Q(349,18)


def boundary_controls(counts):
    # The only surviving sites whose free-neighbour sets differ from the
    # doubly infinite 6-period graph. Right sites are represented at m=2;
    # adding6 preserves all data, so this verifies every m>=2 boundary.
    m=2;C=connected_cells(m);changed=[];slacks={}
    for v in sorted(C):
        infinite={reduced(u) for u in neighbors(v)}&set(PERIOD)
        actual=set(neighbors(v))&C
        if {reduced(u) for u in actual}!=infinite:
            changed.append(v);vertex_inequalities(v,actual,old_count(v),counts)
            t=PERIOD[reduced(v)][0]
            slack=len(actual)-(len(actual)+old_count(v)-1)*t-sum(PERIOD[reduced(u)][1] for u in actual)
            slacks[str(v)]=str(slack)
    assert changed==[(3,17),(4,8),(4,16),(5,7),(5,17)]
    assert slacks=={'(3, 17)':'0','(4, 8)':'0','(4, 16)':'0','(5, 7)':'1/3','(5, 17)':'1/3'}
    # Relative to m complete periods the finite region omits these four
    # phase sites, each once. All others are counted exactly m times.
    omitted=[(4,0),(4,1),(4,5),(5,0)]
    missing=sum(sum(PERIOD[v]) for v in omitted)
    assert missing==Q(55,12)
    return slacks


def finite_control(m,counts):
    k=m+1;old=family(k)[0];P0=endpoints(old[3]);C=connected_cells(m)
    R=old[2]-{guard(i) for i in range(m)}-{lower_guard(i) for i in range(m)}
    R-={(4,6+6*i) for i in range(1,m)}
    free=free_vertices((*old[:2],R,old[3]))
    actual=next(S for S in actual_components(free) if guard(0) in S)
    assert actual==C and len(C)==17*m-4
    assert len(free-C)==17  # fixed15-site pocket and two isolates
    for v in sorted(C):
        c=len(set(neighbors(v))&P0);assert c==old_count(v)
        vertex_inequalities(v,set(neighbors(v))&C,c,counts)
    for name,pat,b in WINDOWS:
        for i in range(-2,m+2):
            S={(r,c+9+6*i) for r,c in pat}
            if S<=C:
                assert sum(sum(PERIOD[reduced(v)]) for v in S)<=b
                counts['finite_window_'+name]+=1
    value=sum(sum(PERIOD[reduced(v)]) for v in C)
    assert value==Q(698*m-165,36)
    gap=value-(18*m-2);assert gap==Q(50*m-93,36)>0
    counts['finite_connected_chain_controls']+=1
    return dict(m=m,sites=len(C),fractional_charge=str(value),candidate_cut=18*m-2,gap=str(gap))


def integer_counterexample(counts):
    root=Path(__file__).resolve().parents[1]
    data=json.loads((root/'develop/fixtures/connected_component_cut_counterexample_k3.json').read_text())
    T={tuple(v) for v in data['T']};M=[tuple(tuple(v) for v in e) for e in data['M']]
    P=endpoints(M);old=family(3)[0];P0=endpoints(old[3]);C=connected_cells(2)
    R=old[2]-{guard(i) for i in [0,1]}-{lower_guard(i) for i in [0,1]}-{successor_guard(0)}
    assert data['shape']==[6,22] and data['G']==data['H']==[0,1] and data['F']==[0]
    assert {tuple(v) for v in data['retained_T']}==R<=T and P0<=P
    direct_check(6,22,T,M)
    free=free_vertices((6,22,R,old[3]));assert T-R|P-P0<=free
    assert C==next(S for S in actual_components(free) if guard(0) in S)
    assert C=={tuple(v) for v in data['connected_free_region']}
    assert len(T&C)==14 and len(P&C)==7 and 2*len(T&C)+len(P&C)==35
    assert data['connected_charge_twice']==35>data['candidate_component_cut']==34
    assert len(T)==38 and len(M)==17 and data['whole_objective']==55<data['whole_candidate_bound']==65
    f,_=frozen_certificate((6,22,T,M))
    assert f=={tuple(v) for v in data['frozen_endpoints']} and P-f=={tuple(v) for v in data['unfrozen_endpoints']}
    assert len(f)==23 and len(P)==34 and (2,5) not in f
    assert (4,8) in T  # Permission restored, not a forced-deletion example.
    # The actual integer point satisfies the entire stated local system too.
    t=lambda v:int(v in T);o=lambda v:int(v in T|P)
    for v in C:
        ns=set(neighbors(v))&C;c=len(set(neighbors(v))&P0)
        if c>=2:assert t(v)==0
        if c>=1:assert all(t(v)+o(u)<=1 for u in ns)
        assert all(t(v)+o(a)+o(b)<=2 for a,b in itertools.combinations(ns,2))
        assert (len(ns)+c-1)*t(v)+sum(o(u) for u in ns)<=len(ns)
        if v[0]==5:assert sum(t(u)+o(u) for u in ns|{v})<=6
    for name,pat,b in WINDOWS:
        for i in range(-2,4):
            S={(r,c+9+6*i) for r,c in pat}
            if S<=C:assert sum(t(v)+o(v) for v in S)<=b
    counts['actual_integer_component_cut_counterexamples']+=1
    return dict(shape=[6,22],component_charge=35,component_candidate_cut=34,
                selected=38,edges=17,whole_objective=55,whole_candidate_bound=65,
                frozen_endpoints=23,total_endpoints=34,
                scope='Actual feasible arbitrary-rematching permissions example; restores h0. Not completely frozen; not a whole-board bound counterexample.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();counts=Counter();period_controls(counts);boundary=boundary_controls(counts)
    samples=[finite_control(m,counts) for m in [*range(2,17),32,64,128]]
    actual=integer_counterexample(counts)
    out=dict(status='PASS',counts=dict(counts),period=[dict(site=v,t=t,o=o) for v,t,o in PERIOD_DATA],
        boundary_full_degree_slack=boundary,period_charge='349/18',omitted_phase_charge='55/12',
        finite_charge='(698m-165)/36',candidate_cut='18m-2',strict_gap='(50m-93)/36>0 for every m>=2',
        samples=samples,actual_integer_obstacle=actual,
        scope='Exact rational witness for the stated fractional local occupation relaxation on every connected17m-4-site G/H/F chain. Satisfies bounds, selection subset, old-P forbiddance, every anchor, every ordinary wedge, full selected-degree inequalities, all bottom closed-star6 cuts and all fully contained module-translates of gh13<=16,h7<=10,gf13<=16,f10<=12. Real relaxation cannot imply Q<=18m-2 or any fixed-boundary correction with bulk slope18; elementary local mate coverage already excludes this rational point. Separately an actual feasible6x22 matching givesQ(C2)=35>34 under the permissions/retainedP0/arbitrary-rematching hypotheses, refuting the isolated component cut. It restores h0, has23of34 endpoints frozen and whole objective55<65; completely frozen component cut, whole-board G/H/F frontier and universal5/6 remain open.')
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(counts),samples=samples[:2],boundary=boundary),indent=2))


if __name__=='__main__':main()
