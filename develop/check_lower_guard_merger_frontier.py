"""Two guard types: exact joint frontier and a robust freezing obstruction.

All-k proof uses disjoint free slots, a universal 13-site certificate and
an equality obstruction in a seven-site component. Enumeration is a check.
"""
import argparse
from collections import Counter,deque
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import endpoints,edge_key,free_vertices,POCKET
from check_occupied_strip_degree_four_budget import family
from check_frozen_strip_completion_reserves import completion
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_selection_withdrawal_sharp_strips import attaining,guard,tree_cells
from check_withdrawal_rematching_joint_bound import (
    pocket_certificate,tree_occupation_certificate,global_physical_tokens,
)

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# Sorted translated coordinates: d,u,g,b,v,h,e,a,L,z,l,s,r.
JOINT=[(2,0),(2,2),(3,0),(3,1),(3,2),(4,-1),(4,0),
       (4,1),(5,-2),(5,-1),(5,0),(5,1),(5,2)]
LOWER=[(4,-1),(4,1),(5,-2),(5,-1),(5,0),(5,1),(5,2)]
# label, weight, centre, neighbour1, neighbour2; integer certificate 3F<=50.
JOINT_ANCHORS=[(3,2,0),(3,4,1),(2,5,6),(1,5,9)]
JOINT_WEDGES=[(3,3,2,4),(2,6,5,10),(2,7,3,6),(1,7,3,11),
              (1,9,5,8),(2,9,8,10),(2,10,9,11),(3,11,7,12)]


def lower_guard(i):
    return 4,8+6*i


def cells(pattern,i):
    return [(r,c+9+6*i) for r,c in pattern]


def actual_components(F):
    pending=set(F);out=[]
    while pending:
        stack=[min(pending)];C=set()
        while stack:
            v=stack.pop()
            if v not in pending:continue
            pending.remove(v);C.add(v);stack.extend(set(neighbors(v))&pending)
        out.append(C)
    return out


def joint_certificate(T,P,counts):
    O=T|P;t=lambda j:int(j in T);o=lambda j:int(j in O)
    assert not T&P and T|P<=set(range(13))
    assert t(1)==0 and t(6)<=o(6) and t(10)<=o(10)
    terms=[weight*(t(v)+o(u)) for weight,v,u in JOINT_ANCHORS]
    assert all(value<=weight for value,(weight,_,_) in zip(terms,JOINT_ANCHORS))
    for weight,v,a,b in JOINT_WEDGES:
        value=t(v)+o(a)+o(b);assert value<=2
        terms.append(weight*value)
    lhs=sum(terms)+3*(t(0)+t(8)+t(12))+3*t(1)
    charge=2*len(T)+len(P)
    # Include the two nonnegative selection-subset slacks explicitly.
    assert lhs+t(6)+t(10)==3*charge+o(6)+o(10)
    assert 3*charge<=lhs<=50
    assert charge<=16
    counts['joint_thirteen_site_certificates']+=1


def lower_coloring_certificate(T,P,counts):
    # h,a,L,z,l,s,r.
    O=T|P;t=lambda j:int(j in T);o=lambda j:int(j in O)
    values=[t(0)+o(3),t(3)+o(0)+o(2),t(5)+o(1)+o(6),
            t(1),t(6),t(2),t(4),o(4),o(5)]
    assert all(x<=b for x,b in zip(values,[1,2,2,1,1,1,1,1,1]))
    assert sum(values)==2*len(T)+len(P)<=11
    if 2*len(T)+len(P)==11:
        assert {1,4,6}<=T and 5 in P
        counts['lower_unmatchable_equality_patterns']+=1
    counts['lower_seven_site_occupation_certificates']+=1


def local_controls(pattern,oldcounts,certificate,counts,label):
    n=len(pattern)
    adj=[sum(1<<j for j,u in enumerate(pattern) if u in neighbors(v)) for v in pattern]
    count=best=0
    for tm in range(1<<n):
        ti=[i for i in range(n) if tm>>i&1]
        if any(oldcounts.get(i,0)+(adj[i]&tm).bit_count()>1 for i in ti):continue
        forbidden=tm;clauses=[]
        for i in ti:
            if oldcounts.get(i,0)+(adj[i]&tm).bit_count()==1:forbidden|=adj[i]
            else:clauses.append(adj[i])
        allowed=((1<<n)-1)&~forbidden
        pm=allowed
        while True:
            if all((pm&mask).bit_count()<=1 for mask in clauses):
                T=set(ti);P={i for i in range(n) if pm>>i&1}
                certificate(T,P,counts);count+=1
                best=max(best,2*len(T)+len(P))
            if not pm:break
            pm=(pm-1)&allowed
    counts[label+'_independent_occupations']=count
    counts[label+'_maximum_charge_twice']=best
    assert best==({'joint':16,'lower':11}[label])


def check_extension(cur,k,G,H,counts,sharp=False,frozen=False):
    old=family(k)[0];P0=endpoints(old[3]);P=endpoints(cur[3]);T=cur[2]
    assert G|H<=set(range(k-1))
    R=old[2]-{guard(i) for i in G}-{lower_guard(i) for i in H}
    assert R<=T and P0<=P and cur[:2]==old[:2]
    direct_check(*cur)
    F=free_vertices((*old[:2],R,old[3]));newT=T-R;newP=P-P0
    assert newT|newP<=F
    expected=[set(POCKET)];bounds=[19]
    pocket_certificate(newT,newP,cur[3],P0,counts)
    for i in range(k-1):
        c=9+6*i
        gate={(2,c+2),(3,c+2)}
        star={(4,c+1),(5,c),(5,c+1),(5,c+2)}
        iso={(5,c-2)}
        if i in G and i in H:
            C=set(cells(JOINT,i));expected.append(C);bounds.append(16)
            index={v:j for j,v in enumerate(cells(JOINT,i))}
            joint_certificate({index[v] for v in newT&C},{index[v] for v in newP&C},counts)
            assert {j:len(set(neighbors(v))&P0) for v,j in index.items() if set(neighbors(v))&P0}=={1:2,2:1,4:1,5:1}
        elif i in G:
            C=set(tree_cells(i));expected += [C,iso];bounds += [12,2]
            index={v:j for j,v in enumerate(tree_cells(i))}
            tree_occupation_certificate({index[v] for v in newT&C},{index[v] for v in newP&C},counts)
        elif i in H:
            C=set(cells(LOWER,i));expected += [gate,C];bounds += [2,10]
            index={v:j for j,v in enumerate(cells(LOWER,i))}
            lower_coloring_certificate({index[v] for v in newT&C},{index[v] for v in newP&C},counts)
            # At charge11 the centre has all three possible mates selected.
            assert set(neighbors((5,c+1)))&(F|P0)==star-{(5,c+1)}
            charge=2*len(newT&C)+len(newP&C)
            if charge==11:
                assert (5,c+1) in newP and star-{(5,c+1)}<=newT
                raise AssertionError('Actual matching cannot cover the isolated centre.')
            assert charge<=10
        else:
            expected += [gate,star,iso];bounds += [2,6,2]
    expected += [{(5,6*k+1)},{(5,6*k+3)}];bounds += [2,2]
    assert {frozenset(C) for C in actual_components(F)}=={frozenset(C) for C in expected}
    assert sum(map(len,expected))==len(F)
    for C,bound in zip(expected,bounds):
        assert 2*len(newT&C)+len(newP&C)<=bound
    assert sum(bounds)==10*k+13+4*len(G)+2*len(H)
    total=len(T)+len(cur[3]);extra=2*len(newT)+len(newP)
    assert 2*total+2*len(G)+2*len(H)==24*k+12+extra
    assert 2*total<=2*(17*k+12+len(G))+1
    assert total<=17*k+12+len(G)
    if sharp:assert total==17*k+12+len(G)
    global_physical_tokens(cur,k,G,counts)
    f,_=frozen_certificate(cur)
    if frozen:assert f==P
    # Geometry of the robust guard implication g in T -> h in T.
    for i in range(k-1):
        g,h=guard(i),lower_guard(i);c=g[1];oldH=(3,c-1)
        if g in T:
            assert set(neighbors(h))&(T|P)<={(3,c-1),(5,c-1)}
            assert set(neighbors(oldH))&(T|P)<={(3,c-2),g,h}
            if h in P:assert h not in f
            if h not in T|P:assert oldH not in f
            if f==P:assert h in T
            counts['robust_guard_implication_controls']+=1
    counts['board_models']+=1
    counts['actual_lower_guard_withdrawals']+=sum(lower_guard(i) not in T for i in H)
    counts['old_edge_rematching_models']+=not {edge_key(e) for e in old[3]}<={edge_key(e) for e in cur[3]}


def sharp_unfrozen_lower(k,H):
    cur=completion(k)[0];T=set(cur[2]);M=list(cur[3])
    for i in H:
        h=lower_guard(i);T.remove(h);M.append((h,(5,h[1])))
    return (*cur[:2],T,M)


def explicit_lower_patch_ranks(cur,k,H,counts):
    P,T=endpoints(cur[3]),cur[2]
    mate={v:u for edge in cur[3] for v,u in (edge,edge[::-1])}
    ranks={};records=[]
    # The old witness coordinates still work: a withdrawn lower selection is
    # now an endpoint whose mate z was frozen at rank zero.
    template={(1,5):0,(1,7):0,(3,8):1,(2,6):1,
              (3,7):2,(3,6):2,(2,7):3,(1,6):4}
    for v,_,a,b in family(k)[2]:
        if v[1]==1:rank=0
        else:
            i=next(i for i in range(k) if (v[0],v[1]-6*i) in template)
            rank=template[v[0],v[1]-6*i]
        ranks[v]=rank;records.append((v,rank,a,b))
    for i in H:
        c=9+6*i;z=(5,c-1)
        ranks[z]=0;records.append((z,0,(5,c-2),(5,c)))
    assert set(ranks)==P-{lower_guard(i) for i in H}
    for v,rank,a,b in records:
        assert a!=b and {a,b}<=set(neighbors(v))
        assert all(w in T or w in P and mate[w] in ranks and ranks[mate[w]]<rank for w in (a,b))
        counts['explicit_partial_freezing_rank_events']+=1


def random_model(k,G,H,seed):
    rng=random.Random(seed);old=family(k)[0]
    R=old[2]-{guard(i) for i in G}-{lower_guard(i) for i in H}
    P0=endpoints(old[3]);F=free_vertices((*old[:2],R,old[3]));possible=P0|F
    mate={v:u for e in old[3] for v,u in (e,e[::-1])}
    starts=sorted(F);rng.shuffle(starts)
    for start in starts[:rng.randrange(len(starts)+1)]:
        if start in mate:continue
        parent={start:None};queue=deque([start]);end=None
        while queue and end is None:
            v=queue.popleft();choices=sorted(set(neighbors(v))&possible);rng.shuffle(choices)
            for u in choices:
                if mate.get(v)==u or u in parent:continue
                parent[u]=v
                if u not in mate:end=u;break
                w=mate[u]
                if w not in parent:parent[w]=u;queue.append(w)
        if end is None:continue
        path=[end]
        while parent[path[-1]] is not None:path.append(parent[path[-1]])
        path.reverse();assert len(path)%2==0
        for v in path:mate.pop(v,None)
        for a,b in zip(path[::2],path[1::2]):mate[a]=b;mate[b]=a
    M=sorted({edge_key((v,u)) for v,u in mate.items()});T=set(R)
    candidates=sorted(F-set(mate));rng.shuffle(candidates)
    for v in candidates:
        if rng.randrange(5)==0:continue
        trial=T|{v};O=trial|set(mate)
        if all(len(set(neighbors(t))&O)<=1 for t in trial):T=trial
    return (*old[:2],T,M)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();counts=Counter()
    local_controls(JOINT,{1:2,2:1,4:1,5:1},joint_certificate,counts,'joint')
    local_controls(LOWER,{0:1},lower_coloring_certificate,counts,'lower')
    for k in list(range(2,13))+[16,32,64,128]:
        states=(itertools.product(range(4),repeat=k-1) if k<=4 else
                [[(i+s)%4 for i in range(k-1)] for s in range(4)]+[[3]*(k-1),[0]*(k-1)])
        for state in states:
            G={i for i,s in enumerate(state) if s&1};H={i for i,s in enumerate(state) if s&2}
            check_extension(attaining(k,G),k,G,H,counts,sharp=True,frozen=True)
            counts['sharp_frozen_two_guard_attainers']+=1
        for offset in range(3):
            H={i for i in range(k-1) if (i+offset)%3!=0}
            cur=sharp_unfrozen_lower(k,H)
            check_extension(cur,k,set(),H,counts,sharp=True)
            P=endpoints(cur[3]);f,_=frozen_certificate(cur)
            assert P-f=={lower_guard(i) for i in H}
            explicit_lower_patch_ranks(cur,k,H,counts)
            counts['exact_lower_withdrawal_unfrozen_trap_families']+=1
        if k<=32:
            for seed in range(32):
                rng=random.Random(2131*k+seed)
                G={i for i in range(k-1) if rng.randrange(2)}
                H={i for i in range(k-1) if rng.randrange(2)}
                check_extension(random_model(k,G,H,1251*k+seed),k,G,H,counts)
    assert counts['actual_lower_guard_withdrawals']>0 and counts['old_edge_rematching_models']>0
    report=dict(status='PASS',counts=dict(counts),
        scope='Written all-k sharp maximum17k+12+|G| with arbitrary old-edge rematching and all P0 retained, allowing arbitrary subsets of upper guards g_i and lower guards h_i withdrawn. Lower withdrawal permission costs no extra objective. Four local states have capacities5,7,6,8; joint13-site occupation certificate3F<=50 givesF<=16; lower7-site certificateF<=11 has an unmatchable equality, henceF<=10 under actual matching. General strict-freezing implication g_i in T => h_i in T; explicit sharp lower-withdrawal family has exactly the withdrawn h_i unfrozen. Original-tile signed compensation remains valid, with no token reused. No universal5/6 improvement; other T/P withdrawals and interacting slots remain open.')
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
