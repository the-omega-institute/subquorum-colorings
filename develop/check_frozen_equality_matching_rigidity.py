"""Solver-free controls of the written all-length matching-rigidity proof.

The all-length proof is in docs/FROZEN_EQUALITY_MATCHING_RIGIDITY.md. This
verifier independently checks actual freezing times and local trap geometry;
finite discovery or optimization is never used as a substitute for that proof.
"""
if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')
import argparse
from collections import Counter, deque
import itertools
import json
from pathlib import Path

from check_boundary_withdrawal_compensation import domain, pocket_bound, random_model, left_gain_model
from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import edge_key, endpoints
from check_frozen_half_area_attainers import frozen_family
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_selection_withdrawal_sharp_strips import attaining


def first_times(cur):
    """Independent event-queue replay, with each kept site activated once."""
    T, M = cur[2:]
    mate = {v:u for edge in M for v,u in (edge,edge[::-1])}
    counts = {v:len(set(neighbors(v)) & T) for v in mate}
    times = {v:1 for v,n in counts.items() if n>=2}
    todo = deque(sorted(times))
    while todo:
        x=todo.popleft()
        for v in neighbors(mate[x]):
            if v not in mate or v in times:
                continue
            counts[v]+=1
            if counts[v]>=2:
                times[v]=times[x]+1
                todo.append(v)
    return times


def trap_check(cur,S):
    T,M=cur[2:];mate={v:u for e in M for v,u in (e,e[::-1])}
    assert S and S<=set(mate)
    for v in S:
        supports={u for u in neighbors(v) if u in T or u in mate and mate[u] not in S}
        assert len(supports)<=1,(v,supports)
    assert S.isdisjoint(first_times(cur))


def local_traps(counts):
    # All injections from the three black core vertices into their possible
    # white mates, including EF as the only fourth port.
    A,B,C,D,E,F,U,V,G=(1,5),(1,6),(1,7),(2,7),(2,6),(3,6),(2,5),(3,5),(3,7)
    for ab,cd,ee in itertools.product([B,U],[B,D],[B,D,U,F]):
        if len({ab,cd,ee})<3:
            continue
        if ee==F:
            continue
        M=[(A,ab),(C,cd),(E,ee)]
        mate={v:u for edge in M for v,u in (edge,edge[::-1])}
        S={B,U,D}
        assert S<=set(mate)
        for v in S:
            support={u for u in set(neighbors(v))&({A,C,E,V,G}) if u not in mate or mate[u] not in S}
            assert len(support)<=1
        counts['noncanonical_EF_injection_traps']+=1
    assert counts['noncanonical_EF_injection_traps']==3
    a,u,v,z=(3,3),(3,4),(4,3),(4,4)
    for m in [2,3,8]:
        cur=frozen_family(m)
        for extra in [[(a,u),(v,z)],[(a,v),(u,z)]]:
            trial=(*cur[:2],cur[2]-{a,z},cur[3]+extra)
            direct_check(*trial)
            assert len(trial[2])+len(trial[3])==18*m+30
            trap_check(trial,{a,z})
            counts['actual_extra_square_traps']+=1


def check_time_propagation(m,cur,tau,counts):
    mate={v:u for e in cur[3] for v,u in (e,e[::-1])}
    for j in range(m+1):
        s=6*j;B=(1,s+6);D=(2,s+7);F=(3,s+6);H=(3,s+8);U=(2,s+5);k=(4,s+6)
        assert tau[D]>tau[F] and tau[D]>tau[H]
        assert tau[B]>tau[D] and tau[B]>tau[F]
        assert tau[U]>tau[B] and tau[U]>tau[F]
        assert tau[H]<tau[F] and tau[mate[k]]<tau[F]<tau[U]
        counts['canonical_core_actual_time_controls']+=1
    for j in range(m,0,-1):
        s=6*j;ZR=(4,s+5);U=(2,s+5);X=(4,s+4);L=(4,s+3);b=(3,s+4)
        Y=(4,s+2);W=(4,s+1);H=(3,s+2);F=(3,s);k=(4,s);Z=(4,s-1)
        assert mate[X]==L and mate[Y]==W and mate[k]==Z
        assert tau[L]<tau[ZR]<tau[U]<tau[b]
        assert tau[W]<tau[L] and tau[W]<tau[H]<tau[F]
        assert tau[Z]<tau[W]
        counts['backward_block_actual_time_controls']+=1


def token_ledger(m,cur):
    h,w,T,M=cur;P=endpoints(M);plus=set();minus=set();strip=0
    for r in (0,2,4):
        for c in range(0,w,2):
            tile={(r+i,c+j) for i in (0,1) for j in (0,1)}
            charge=4-2*len(T&tile)-len(P&tile)
            if r==0:
                strip+=charge
                continue
            plus.update(((r,c),i) for i in range(max(charge,0)))
            minus.update(((r,c),i) for i in range(max(-charge,0)))
    assert strip==-m
    delta=int(set(map(edge_key,frozen_family(m)[3]))-set(map(edge_key,M))!=set())
    assert len(plus)>=len(minus)+m+2*delta
    ordered=sorted(plus);paid=ordered[:len(minus)+m];reserve=ordered[len(minus)+m:]
    assert len(paid)==len(set(paid)) and set(paid).isdisjoint(reserve)
    return len(reserve)


def alternating_cycle_controls(m,counts):
    cur=frozen_family(m);M=set(map(edge_key,cur[3]));P=endpoints(M)
    mate={v:u for e in M for v,u in (e,e[::-1])};cycles=set()
    def walk(path):
        v=path[-1]
        for b in set(neighbors(v))&P-{mate[v]}:
            w=mate[b]
            if w==path[0] and len(path)>=2:
                cycles.add(tuple(path))
            elif w>path[0] and w not in path and len(path)<7:
                walk(path+[w])
    for v in sorted(x for x in P if sum(x)%2):
        walk([v])
    for cy in cycles:
        old={edge_key((v,mate[v])) for v in cy}
        new={edge_key((cy[i],mate[cy[(i+1)%len(cy)]])) for i in range(len(cy))}
        trial=(*cur[:3],sorted((M-old)|new))
        direct_check(*trial)
        assert endpoints(trial[3])==P and set(first_times(trial))!=P
        counts['nonfrozen_short_alternating_cycle_controls']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--max-m',type=int,default=24);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();local_traps(counts);records=[]
    for m in sorted(set(range(2,args.max_m+1))|{64,100}):
        cur=frozen_family(m);Mstar=set(map(edge_key,cur[3]));direct_check(*cur)
        tau=first_times(cur);assert set(tau)==endpoints(cur[3])
        check_time_propagation(m,cur,tau,counts)
        alt=(*cur[:2],(cur[2]-{(4,2),(5,1)})|{(5,0),(5,2)},cur[3])
        direct_check(*alt);assert cur[2]!=alt[2] and len(cur[2])==len(alt[2])
        assert all(set(neighbors(v))&cur[2]==set(neighbors(v))&alt[2] for v in endpoints(cur[3]))
        assert first_times(alt)==tau
        counts['nonunique_selection_all_length_controls']+=1
        assert token_ledger(m,cur)==token_ledger(m,alt)==0
        base=attaining(m+1,set(range(m)));direct_check(*base)
        tb=first_times(base);assert set(tb)==endpoints(base[3])
        missing=Mstar-set(map(edge_key,base[3]));expected={edge_key(((2,5),(3,5))),edge_key(((3,6*m+9),(4,6*m+9)))}|{edge_key(((4,5+2*l),(4,6+2*l))) for l in range(3*m+2)}
        assert missing==expected and len(missing)==3*m+4
        assert len(base[2])+len(base[3])==18*m+29
        assert token_ledger(m,base)==2
        counts['sharp_nonadditive_frozen_lengths']+=1
        counts['original_token_allocations']+=4
        c=6*m+9;n=3*m+2
        Tg=(cur[2]-{(2,c)})|{(3,5),(3,c)}|{(4,6+2*l) for l in range(n)}
        Mg=sorted(Mstar-expected);explicit_g=(*cur[:2],Tg,Mg)
        direct_check(*explicit_g)
        assert len(Tg)==12*m+24 and len(Mg)==6*m+5
        assert first_times(explicit_g)==tb and token_ledger(m,explicit_g)==2
        counts['explicit_all_g_frozen_lengths']+=1
        for current,times in [(cur,tau),(alt,tau),(base,tb),(explicit_g,tb)]:
            assert all(len(set(neighbors(v))&(current[2]|endpoints(current[3])))>=3 for v in times)
            counts['fully_frozen_boards']+=1
            if m in [2,3,8]:
                f,layers=frozen_certificate(current)
                assert f==set(times) and {tuple(rec['endpoint']):i+1 for i,layer in enumerate(layers) for rec in layer}==times
                counts['independent_synchronous_replays']+=1
        records.append(dict(m=m,matching=len(Mstar),frozen_layers=max(tau.values()),nonadditive_missing_edges=len(missing),nonadditive_margin=1))
    for m in [2,3,8]:
        alternating_cycle_controls(m,counts)
        for symmetry in itertools.product([False,True],repeat=3):
            cur=frozen_family(m);shape,T,M=transformed(*cur,*symmetry);trial=(*shape,T,M)
            direct_check(*trial);assert set(first_times(trial))==endpoints(M)
            counts['isometry_controls']+=1
    for m in [2,3,4]:
        for current in [left_gain_model(m)]+[random_model(m,seed) for seed in range(40)]:
            direct_check(*current);L=pocket_bound(current[2],endpoints(current[3]),current[3],counts)
            assert L<=9+int((2,5) in current[2]|endpoints(current[3]))
            counts['actual_pocket_port_controls']+=1
    out=dict(status='PASS',theorem='Every completely frozen half-area equality board in the stated P0/R permissions has exactly Mstar. Binary missing-edge reserve is sharp; additive reserve per missing edge is false for all lengths.',proof='Written weighted-certificate port inequality, three-endpoint EF trap, actual-mate time induction and two-endpoint extra-pocket trap; finite checks only validate instances.',scope='No universal 5/6 result. Coordinate graph adapter is written and executable, not end-to-end Lean.',counts=dict(counts),records=records)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'}))

if __name__=='__main__':main()
