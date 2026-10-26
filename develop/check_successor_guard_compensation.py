"""Sharp G/F compensation with successor ownership; stdlib proof checks.

The universal weighted identities and all-k coordinate proof are in the note.
Enumeration checks them independently; it is not the proof of the theorem.
"""
import argparse
from collections import Counter, deque
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import endpoints, edge_key, free_vertices, POCKET
from check_frozen_strip_completion_reserves import completion
from check_lower_guard_merger_frontier import actual_components
from check_occupied_strip_degree_four_budget import family
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_selection_withdrawal_sharp_strips import attaining, guard, tree_cells
from check_withdrawal_rematching_joint_bound import (
    global_physical_tokens, pocket_certificate, tree_occupation_certificate,
)

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# Relative to c_i=9+6i. New withdrawal is f_{i+1}=(4,c_i+3).
ONLY_F = [(2,2),(3,2),(4,1),(4,2),(4,3),
          (5,0),(5,1),(5,2),(5,3),(5,4)]
JOINT_GF = [(2,0),(2,2),(3,0),(3,1),(3,2),(4,1),(4,2),
            (4,3),(5,0),(5,1),(5,2),(5,3),(5,4)]
GF_ANCHORS = [(3,2,0),(3,4,1),(2,7,6),(1,7,11)]
GF_WEDGES = [(1,3,2,4),(2,3,2,5),(2,5,3,6),(1,5,3,9),
             (2,6,4,10),(1,9,5,8),(2,9,8,10),(2,10,9,11),
             (3,11,7,12)]


def successor_guard(i):
    return 4,12+6*i


def translated(pattern, i):
    return [(r,c+9+6*i) for r,c in pattern]


def gf_certificate(T,P,counts):
    O=T|P; t=lambda j:int(j in T); o=lambda j:int(j in O)
    assert not T&P and T|P<=set(range(13))
    terms=[]
    for w,v,u in GF_ANCHORS:
        value=t(v)+o(u); assert value<=1; terms.append(w*value)
    for w,v,a,b in GF_WEDGES:
        value=t(v)+o(a)+o(b); assert value<=2; terms.append(w*value)
    assert t(1)==0
    lhs=sum(terms)+3*(t(0)+t(8)+t(12))+3*t(1)
    charge=2*len(T)+len(P)
    assert lhs+t(6)+t(10)==3*charge+o(6)+o(10)
    assert 3*charge<=lhs<=50 and charge<=16
    counts['gf_thirteen_site_certificates']+=1


def f_certificate(T,P,counts):
    # u,v,a,x,f,l,s,r,z,R.
    O=T|P; t=lambda j:int(j in T); o=lambda j:int(j in O)
    assert not T&P and T|P<=set(range(10))
    values=[t(0),o(1),t(1)+o(0),t(3)+o(2)+o(7),t(4)+o(8),
            t(5),t(6)+o(2)+o(5),t(7)+o(3)+o(6),
            t(8)+o(4)+o(9),t(9)]
    bounds=[0,1,1,2,1,1,2,2,2,1]
    assert all(a<=b for a,b in zip(values,bounds))
    charge=2*len(T)+len(P); lhs=sum(values)
    assert lhs+t(2)==charge+o(2)
    assert charge<=lhs<=13
    if charge==13:
        # Uses the other genuine feasibility constraints as well as tightness.
        assert t(6)+o(5)+o(7)<=2
        assert t(2)+o(3)+o(6)<=2
        assert t(4)+o(3)<=1
        assert t(7)+o(3)+o(8)<=2
        assert {2,5,7}<=T and 6 in P
        counts['f_unmatchable_equality_patterns']+=1
    counts['f_ten_site_certificates']+=1


def coefficient_controls(counts):
    # Verify the identities symbolically, not merely on 0/1 occupations.
    for n,which in [(13,'gf'),(10,'f')]:
        t=[Counter({('t',i):1}) for i in range(n)]
        o=[Counter({('o',i):1}) for i in range(n)]
        lhs=Counter()
        def add(weight,*terms):
            for term in terms:
                for key,value in term.items(): lhs[key]+=weight*value
        if which=='gf':
            for w,v,u in GF_ANCHORS:add(w,t[v],o[u])
            for w,v,a,b in GF_WEDGES:add(w,t[v],o[a],o[b])
            for i in (0,1,8,12):add(3,t[i])
            add(1,t[6],t[10]); rhs=Counter({('t',i):3 for i in range(n)})
            rhs.update({('o',i):3 for i in range(n)});rhs[('o',6)]+=1;rhs[('o',10)]+=1
            assert sum(w for w,_,_ in GF_ANCHORS)+2*sum(w for w,_,_,_ in GF_WEDGES)+9==50
        else:
            for i in range(n):add(1,t[i])
            for i in range(n):add(1,o[i])
            add(1,o[2]);rhs=lhs.copy();lhs=Counter()
            for terms in [(t[0],),(o[1],),(t[1],o[0]),(t[3],o[2],o[7]),
                          (t[4],o[8]),(t[5],),(t[6],o[2],o[5]),
                          (t[7],o[3],o[6]),(t[8],o[4],o[9]),(t[9],),(t[2],)]:add(1,*terms)
        assert lhs==rhs
        counts['universal_coefficient_identities']+=1


def successor_partition(k,G,F):
    blocks=[set(POCKET)];bounds=[19]
    for i in range(k-1):
        c=9+6*i; gate={(2,c+2),(3,c+2)}
        star={(4,c+1),(5,c),(5,c+1),(5,c+2)}; iso={(5,c+4)}
        if i in G and i in F:
            blocks.append(set(translated(JOINT_GF,i)));bounds.append(16)
        elif i in F:
            blocks.append(set(translated(ONLY_F,i)));bounds.append(12)
        elif i in G:
            blocks += [set(tree_cells(i)),iso];bounds += [12,2]
        else:
            blocks += [gate,star,iso];bounds += [2,6,2]
    blocks += [{(5,7)},{(5,6*k+3)}];bounds += [2,2]
    return blocks,bounds


def geometry(k,G,F,counts):
    old=family(k)[0];P0=endpoints(old[3])
    R=old[2]-{guard(i) for i in G}-{successor_guard(i) for i in F}
    assert G|F<=set(range(k-1)) and len(R)==8*k+5-len(G)-len(F)
    free=free_vertices((*old[:2],R,old[3]));blocks,bounds=successor_partition(k,G,F)
    assert len(free)==7*k+10+3*len(G)+3*len(F)
    owner={v:j for j,C in enumerate(blocks) for v in C}
    assert len(owner)==sum(map(len,blocks))==len(free) and set(owner)==free
    assert all(owner[v]==owner[u] for v in free for u in set(neighbors(v))&free)
    assert {frozenset(C) for C in actual_components(free)}=={frozenset(C) for C in blocks}
    for i in F:
        pattern=JOINT_GF if i in G else ONLY_F
        oldcounts={1:2,2:1,4:1,7:1} if i in G else {0:2,1:1,4:1}
        assert {j:len(set(neighbors(v))&P0) for j,v in enumerate(translated(pattern,i))
                if set(neighbors(v))&P0}==oldcounts
        centre=(5,10+6*i)
        assert set(neighbors(centre))&(free|P0)=={(4,10+6*i),(5,9+6*i),(5,11+6*i)}
    assert sum(bounds)==10*k+13+4*len(G)+2*len(F)
    # Pocket boundary and absence of interactions with old unanchored T.
    assert {v for v in POCKET if set(neighbors(v))&P0}=={(2,5),(3,5)}
    assert all(not set(neighbors(v))&free for v in R if not set(neighbors(v))&P0)
    counts['successor_geometry_partitions']+=1
    return R,P0,free,blocks,bounds


def check_extension(cur,k,G,F,counts,sharp=False,frozen=False):
    R,P0,free,blocks,bounds=geometry(k,G,F,counts)
    P=endpoints(cur[3]);T=cur[2]
    assert R<=T and P0<=P;direct_check(*cur)
    newT,newP=T-R,P-P0;assert newT|newP<=free
    pocket_certificate(newT,newP,cur[3],P0,counts)
    for i in range(k-1):
        if i in F:
            pattern=JOINT_GF if i in G else ONLY_F
            index={v:j for j,v in enumerate(translated(pattern,i))}
            lt={index[v] for v in newT if v in index};lp={index[v] for v in newP if v in index}
            (gf_certificate if i in G else f_certificate)(lt,lp,counts)
            if i not in G:
                # Charge13 forces a P centre with its entire mate set selected.
                assert 2*len(lt)+len(lp)<=12
        elif i in G:
            index={v:j for j,v in enumerate(tree_cells(i))}
            tree_occupation_certificate({index[v] for v in newT if v in index},
                                        {index[v] for v in newP if v in index},counts)
    for C,b in zip(blocks,bounds):assert 2*len(newT&C)+len(newP&C)<=b
    total=len(T)+len(cur[3]);extra=2*len(newT)+len(newP)
    assert 2*total+2*len(G)+2*len(F)==24*k+12+extra
    assert total<=17*k+12+len(G)
    global_physical_tokens(cur,k,G,counts)
    if sharp:assert total==17*k+12+len(G)
    if frozen:assert frozen_certificate(cur)[0]==P
    old=family(k)[0]
    counts['actual_old_edge_rematching_models']+=not {edge_key(e) for e in old[3]}<={edge_key(e) for e in cur[3]}
    counts['actual_successor_guard_deletions']+=sum(successor_guard(i) not in T for i in F)
    counts['board_models']+=1


def random_model(k,G,F,seed):
    rng=random.Random(seed);old=family(k)[0]
    R=old[2]-{guard(i) for i in G}-{successor_guard(i) for i in F}
    free=free_vertices((*old[:2],R,old[3]));possible=endpoints(old[3])|free
    mate={v:u for e in old[3] for v,u in (e,e[::-1])}
    starts=sorted(free);rng.shuffle(starts)
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
    candidates=sorted(free-set(mate));rng.shuffle(candidates)
    for v in candidates:
        if rng.randrange(5)==0:continue
        trial=T|{v};O=trial|set(mate)
        if all(len(set(neighbors(t))&O)<=1 for t in trial):T=trial
    return (*old[:2],T,M)


def sharp_f_patch(k,F):
    cur=completion(k)[0];T=set(cur[2]);M=list(cur[3])
    for i in F:
        f=successor_guard(i);T.remove(f);M.append((f,(5,f[1])))
    return (*cur[:2],T,M)


def partial_patch_ranks(cur,k,F,counts):
    P=endpoints(cur[3]);mate={v:u for e in cur[3] for v,u in (e,e[::-1])}
    records=list(family(k)[2])
    for i in F:
        c=successor_guard(i)[1]
        records.append(((5,c),0,(5,c-1),(5,c+1)))
    ranks={v:rank for v,rank,_,_ in records}
    assert set(ranks)==P-{successor_guard(i) for i in F}
    for v,rank,a,b in records:
        assert a!=b and {a,b}<=set(neighbors(v))
        assert all(w in cur[2] or w in P and mate[w] in ranks and ranks[mate[w]]<rank
                   for w in (a,b))
        counts['explicit_partial_rank_events']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();counts=Counter();coefficient_controls(counts)
    # Independent bitmask occupation enumerator; no optimization package.
    for pattern,oldcounts,cert,name,maximum in [
        (ONLY_F,{0:2,1:1,4:1},f_certificate,'f',13),
        (JOINT_GF,{1:2,2:1,4:1,7:1},gf_certificate,'gf',16)]:
        n=len(pattern);adj=[sum(1<<j for j,u in enumerate(pattern) if u in neighbors(v)) for v in pattern]
        best=-1
        for tm in range(1<<n):
            ti={i for i in range(n) if tm>>i&1}
            if any(oldcounts.get(i,0)+(adj[i]&tm).bit_count()>1 for i in ti):continue
            forbidden=tm;clauses=[]
            for i in ti:
                if oldcounts.get(i,0)+(adj[i]&tm).bit_count()==1:forbidden|=adj[i]
                else:clauses.append(adj[i])
            allowed=((1<<n)-1)&~forbidden;pm=allowed
            while True:
                if all((pm&mask).bit_count()<=1 for mask in clauses):
                    pi={i for i in range(n) if pm>>i&1};cert(ti,pi,counts)
                    counts[name+'_independent_occupations']+=1;best=max(best,2*len(ti)+len(pi))
                if not pm:break
                pm=(pm-1)&allowed
        assert best==maximum;counts[name+'_maximum_doubled_charge']=best
    for k in list(range(2,13))+[16,32,64,128]:
        states=(itertools.product(range(4),repeat=k-1) if k<=4 else
                [[(i+s)%4 for i in range(k-1)] for s in range(4)]+[[3]*(k-1),[0]*(k-1)])
        for state in states:
            G={i for i,s in enumerate(state) if s&1};F={i for i,s in enumerate(state) if s&2}
            check_extension(attaining(k,G),k,G,F,counts,sharp=True,frozen=True)
            counts['sharp_frozen_permission_attainers']+=1
        for offset in range(3):
            F={i for i in range(k-1) if (i+offset)%3!=0};cur=sharp_f_patch(k,F)
            check_extension(cur,k,set(),F,counts,sharp=True)
            assert endpoints(cur[3])-frozen_certificate(cur)[0]=={successor_guard(i) for i in F}
            partial_patch_ranks(cur,k,F,counts)
            counts['sharp_actual_f_deletion_controls']+=1
        if k<=32:
            for seed in range(24):
                rng=random.Random(2903*k+seed)
                G={i for i in range(k-1) if rng.randrange(2)}
                F={i for i in range(k-1) if rng.randrange(2)}
                check_extension(random_model(k,G,F,4073*k+seed),k,G,F,counts)
    assert counts['actual_successor_guard_deletions'] and counts['actual_old_edge_rematching_models']
    report=dict(status='PASS',counts=dict(counts),
        scope='General written sharp G/F permissions theorem with all h retained, P0 retained, arbitrary actual rematching: maximum17k+12+|G| independent of F. Successor isolate ownership is injective; local capacities5/7/6/8; universal13-site3Q<=50 and ten-siteQ<=13 equality has unmatched centre, henceQ<=12. Sharp frozen permission attainers retain F; all-k actual-F-deletion patches reach sharp bound with exactly those f endpoints unfrozen, with explicit partial strict ranks. Original physical tile half-tokens allocated once. Full G/H/F connected-chain inequality and universal5/6 remain open.')
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
