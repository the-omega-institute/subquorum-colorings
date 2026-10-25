"""Actual frozen four-source/four-mixed-gate cycle and exact resource budgets.

All-size claims have proofs in FROZEN_MIXED_GATE_CYCLES_AND_OCCUPIED_CHAMBERS.md.
Finite checks corroborate, not replace, those proofs.
"""
import argparse,itertools,json,random
from collections import Counter
from pathlib import Path
from check_occupied_cycle_chambers import actual,scaffold
from check_merger_completion_reserves import feasible,frozen,owner_data,whole_bands,whole_support_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_beta_support_fork import restrict
from check_reserve_boundary_split import clipped
from check_joint_gate_resource_cuts import tree_count,matching_rank
from check_whole_support_fork_normal_form import optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Run without -O.')

FIXTURE=Path(__file__).parent/'fixtures/frozen_all_mixed_gate_cycle.json'

def load_model():
    r=json.loads(FIXTURE.read_text());cur=actual(r)
    assert feasible(cur) and frozen(cur)
    check_rank_certificate(cur,[[tuple(v) for v in layer] for layer in r['freezing_layers']])
    d,meta,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*d[:2])
    T,M,roots,blank=scaffold(24,5,18)
    canon=lambda es:{tuple(sorted(e)) for e in es}
    assert T<=cur[2] and canon(M)<=canon(cur[3])
    assert not blank & (cur[2]|{v for e in cur[3] for v in e})
    gates=[o[v] for v in roots];top,right,bottom,left=[o[v] for v in [(5,6),(5,19),(24,6),(5,4)]]
    assert aa=={top,right,bottom,left} and len(set(gates))==4 and set(gates)<=mm
    entries=[((5,6),(5,5)),((5,19),(5,18)),((24,17),(24,18)),((24,4),(24,5))]
    allentries=entries+[((5,4),(5,5)),((5,17),(5,18)),((24,19),(24,18)),((24,6),(24,5))]
    assert all(e in d[2] for e in allentries)
    group={g:d[3][g] for g in gates}
    pool=set().union(*group.values())-set().union(*(d[3][a] for a in aa))
    assert len(pool)==16
    local=restrict(d,aa|set(gates),pool);lo,la,lb,lm=owner_data(*local[:2])
    assert not lb and len(la)==len(lm)==4
    edges={(u,v) for u,v in local[2] if lo[u]!=lo[v]}
    assert edges==set(allentries)
    assert all(not local[3][a] for a in la)
    gates_local={lo[v] for v in roots}
    incidence={j:{g for g in gates_local if j in local[3][g]} for j in pool}
    assert all(1<=len(gs)<=2 for gs in incidence.values())
    # Source-private cost classes and simultaneous beta fallback paths.
    WL,WB=d[3][left],d[3][bottom];WG=d[3][gates[2]]|d[3][gates[3]]
    assert list(map(len,(WL,WB,WG)))==[11,6,11]
    assert not (WL&WB or WL&WG or WB&WG)
    assert not d[3][top] and not d[3][right]
    beta_paths=[[(5,17),(5,16)],[(5,19),(5,20)],[(5,4),(5,3)],[(18,15),(18,16)]]
    for u,v in beta_paths: assert (u,v) in d[2] and o[v] in bb
    assert len({o[v] for u,v in beta_paths})==4
    assert o[18,15]==gates[2]
    source_first={a:{o[v] for u,v in d[2] if o[u]==a and o[v]!=a} for a in aa}
    assert source_first[bottom]=={gates[2],gates[3]}
    return cur,d,meta,local,gates_local,incidence,(WL,WB,WG),pool


def full_prediction(classes,A):
    WL,WB,WG=classes
    ell=0 if A&WL else 1
    b=0 if A&WB else 1 if A&WG else 2
    return 4,2+ell+b


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    cur,d,meta,local,gates,incidence,classes,pool=load_model();totals=Counter();rng=random.Random(2026102505)
    # Every unit identity and pair; random larger subsets and all five
    # resource-graph incidence classes, with multiplicity zero/one/two.
    edgeclasses={}
    for j,gs in incidence.items():edgeclasses.setdefault(tuple(sorted(gs)),set()).add(j)
    assert sorted(map(len,edgeclasses.values()))==[2,2,2,3,7]
    choices=[]
    for key,units in sorted(edgeclasses.items()):
        u=sorted(units);choices.append([set(),{u[0]},set(u[:2])] if len(key)==2 else [set(),{u[0]}])
    pools=[set().union(set(),*xs) for xs in itertools.product(*choices)]
    pools += [set(s) for n in (0,1,2) for s in itertools.combinations(sorted(pool),n)]
    pools += [{j for j in pool if rng.randrange(2)} for _ in range(128)]
    for A in pools:
        t=tree_count(gates,set(A),incidence);rank=matching_rank(gates,{g:{j for j in A if g in incidence[j]} for g in gates})
        assert rank==4-t
        data=clipped(local,A);z=fork_flow(*data);b=optimize(*data)
        assert (z['value'],z['cost'])==(b['value'],b['cost'])==(rank,rank)
        totals['local_actual_resource_models']+=1;totals['independent_local_packs']+=1
    # All original singleton/pair identities; keep EVERY original owner/link/beta.
    full_pools=[d[4]]+[set(s) for n in (0,1,2) for s in itertools.combinations(sorted(d[4]),n)]
    full_pools += [{j for j in d[4] if rng.randrange(2)} for _ in range(128)]
    for i,A in enumerate(full_pools):
        z=fork_flow(*clipped(d,A));expected=full_prediction(classes,A)
        assert (z['value'],z['cost'])==expected
        if i<80 or i>=len(full_pools)-32:
            for forks in (False,True):
                b=optimize(*clipped(d,A),allow_forks=forks)
                assert (b['value'],b['cost'])==expected;totals['independent_complete_packs']+=1
        totals['complete_original_availability_models']+=1
    identity=lambda b,c:meta['owner'][b,c]
    tree={identity(5,10),identity(7,13),identity(9,13)}
    repairs=[identity(5,12),identity(7,15),identity(9,14),identity(6,15),identity(9,8)]
    assert len(tree)==3 and len(set(repairs))==5 and not tree&set(repairs)
    for flags in itertools.product((False,True),repeat=5):
        A=tree|{j for j,f in zip(repairs,flags) if f}
        z=fork_flow(*clipped(local,A));expected=3+any(flags)
        assert (z['value'],z['cost'])==(expected,expected)
        totals['overlapping_original_unit_repairs']+=1
    named={}
    for label,A in [('empty',set()),('tree3',tree),('tree_plus_parallel',tree|{repairs[0]}),('all',d[4])]:
        full=fork_flow(*clipped(d,A));small=fork_flow(*clipped(local,A&pool))
        named[label]=dict(full_value=full['value'],full_cost=full['cost'],local_value=small['value'],local_cost=small['cost'])
    # Literal separated grid copies, with even blank buffers. The proof
    # covers all n/availability; these check source and interval identity shifts.
    root_points=[(5,5),(5,18),(24,18),(24,5)]
    base_ids=[(5,10),(7,13),(9,13)]
    repair_ids=[(5,12),(7,15),(9,14),(6,15),(9,8)]
    for n in (2,3):
        for mode in range(4):
            T=set();M=[];wanted=set();repaired=0;gatepoints=[]
            for i in range(n):
                shift=32*i+2;move=lambda v:(v[0]+shift,v[1])
                T|={move(v) for v in cur[2]};M += [tuple(move(v) for v in e) for e in cur[3]]
                flags=[False]*5 if mode==0 else [True]*5 if mode==1 else [i%2==0]*5 if mode==2 else [bool(rng.randrange(2)) for _ in range(5)]
                repaired+=any(flags)
                wanted|={(16*i+1+b,c,c) for b,c in base_ids}
                wanted|={(16*i+1+b,c,c) for (b,c),flag in zip(repair_ids,flags) if flag}
                gatepoints += [move(v) for v in root_points]
            joined=(32*n,24,T,M);assert feasible(joined) and frozen(joined)
            data,info,_=whole_support_data(joined,whole_bands(joined));own,alphas,_,_=owner_data(*data[:2])
            A={j for j in data[4] if (info['intervals'][j]['band'],info['intervals'][j]['first'],info['intervals'][j]['last']) in wanted}
            gateowners={own[v] for v in gatepoints};small=restrict(data,alphas|gateowners,A)
            lf=fork_flow(*small);ff=fork_flow(*clipped(data,A))
            assert (lf['value'],lf['cost'])==(3*n+repaired,3*n+repaired)
            assert (ff['value'],ff['cost'])==(4*n,4*n)
            totals['separated_frozen_copy_models']+=1
    record=dict(status='PASS',shape=cur[:2],selected=len(cur[2]),endpoints=2*len(cur[3]),totals=dict(totals),named=named,
        support_class_sizes=list(map(len,edgeclasses.values())),all_original_classes=list(map(len,classes)),
        scope='Actual four-alpha/four-distinct-mixed-gate even cycle completely frozen. All-subset local resource-graph tree rank and complete original V4/cost2+ell+b have general written proofs. Local owner restriction is explicit; full model always retains all original owners/betas. Abstract five-source joint obstruction is NOT physically realized;5/6 open.')
    args.output.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))

if __name__=='__main__':main()
