"""FULL original-pool mixed interface obstruction and exact isolated repairs.

No external solver. All-size proofs: FULL_POOL_INTERFACE_SINGLETON_AND_REPAIR_PROFILE.md.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_crossing_matching_ports import rectangle, compile_partition
from check_interface_reserve_reoptimization import constrained_primitive, subsets
from check_frozen_beta_support_fork import restrict
from check_selection_maximum_singleton import cropped, reduced_serial_certificate
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import evaluate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__: raise RuntimeError('Assertions required; no -O.')


def family(w,q,repairs):
    assert w>=8 and w%2==0 and q>=1 and set(repairs)<=set(range(q))
    base=cropped(w);T=set();M=[];regions=[]
    for i in range(q):
        d=i*(w+4);move=lambda v:(v[0]+d,v[1])
        T|={move(v) for v in base[2] if i not in repairs or v!=(0,1)}
        M += [tuple(map(move,e)) for e in base[3]]
        regions += [rectangle(d,d+w+2,0,14),rectangle(d,d+w+2,14,22,True)]
        if i+1<q: regions.append(rectangle(d+w+2,d+w+4,0,22))
    return (q*(w+4)-2,22,T,M),regions


def closure(data,roots):
    owner,_,_,_=owner_data(*data[:2]);edges=defaultdict(set)
    for u,v in data[2]:
        if owner[u]!=owner[v]: edges[owner[u]].add(owner[v])
    seen=set(roots);todo=list(roots)
    while todo:
        u=todo.pop()
        for v in edges[u]-seen: seen.add(v);todo.append(v)
    return seen,edges


def full_pool_check(w,q,repairs,totals,fixture=False):
    s=len(repairs);cur,regions=family(w,q,repairs);R,C,T,M=cur
    direct_check(*cur);P={v for e in M for v in e};frozen,layers=frozen_certificate(cur)
    assert frozen==P and len(P)==q*(6*w+20)
    # Replay the uniform, non-search-generated serial certificate inside
    # each individual copy, preserving every translated mate and seed.
    base=cropped(w)
    for i in range(q):
        local=(*base[:2],base[2]-({(0,1)} if i in repairs else set()),base[3])
        schedule=reduced_serial_certificate(w,local)
        totals['serial_freezing_events']+=sum(map(len,schedule))
    record,data=compile_partition(cur,regions)
    own,A,B,X=owner_data(*data[:2]);Q=data[4]
    assert (len(T),len(M))==(41*q-s,q*(3*w+10))
    assert (len(A),len(B),len(X),len(Q))==(2*q,q*(w//2-2),8*q,q*(15*w//2-3)+s-22)
    assert record['slack']==q*(8*w-7)+s-22>0
    assert len(record['crossing_edges'])==2*q
    assert record['local_inventory']['CC']==q and record['interface']=={'TT':q}
    assert (record['local_closed_value'],record['local_closed_deficit'],record['local_closed_cost'])==(q,0,2*q-s)
    assert (record['value'],record['cost'],record['deficit'])==(q+s,s,q-s)
    old=set();interface=set();units=set();repair_units=set();copy_roots=[];offset=0;tables=[]
    upper=[];lower=[]
    for i in range(q):
        d=i*(w+4);move=lambda v:(v[0]+d,v[1])
        pair=lambda x,y:tuple(map(move,(x,y)))
        ids={
            'A':own[move((1,5))], 'I':own[move((1,13))],
            'U0':own[move((1,3))], 'U1':own[move((1,6))], 'U2':own[move((1,8))],
            'L0':own[move((w,3))], 'L1':own[move((w,6))], 'L2':own[move((w,8))]}
        expected_pairs={'A':pair((1,5),(w,5)),'I':pair((1,13),(w,13)),
            'U0':pair((1,3),(1,4)),'U1':pair((1,6),(1,7)),'U2':pair((1,8),(1,9)),
            'L0':pair((w,3),(w,4)),'L1':pair((w,6),(w,7)),'L2':pair((w,8),(w,9))}
        assert all(set(data[1][ids[k]])==set(p) for k,p in expected_pairs.items())
        j=(offset+w//2,11,11);l=(offset,1,1);units.add(j)
        if i in repairs: repair_units.add(l)
        old.add(ids['A']);interface.add(ids['I']);copy_roots.append((ids['A'],ids['I']))
        reached,edges=closure(data,{ids['A'],ids['I']})
        assert reached==set(ids.values()) and not reached&B
        expected_exits={'A':{'U0','U1','L0','L1'},'U1':{'U2'},'L1':{'L2'}}
        expected_support={'I':{j},'L2':{j},'U0':({l} if i in repairs else set())}
        for name,o in ids.items():
            assert edges[o]=={ids[k] for k in expected_exits.get(name,set())}
            assert data[3][o]==expected_support.get(name,set())
        assert {o for o,js in data[3].items() if j in js}=={ids['I'],ids['L2']}
        assert sum(data[3][o]=={j} for o in reached)==2
        # The singleton class has exactly one unit, even though there are
        # many other actual original units in the complete pool.
        assert {x for x in Q if {o for o,js in data[3].items() if x in js}=={ids['I'],ids['L2']}}=={j}
        upper.append(pair((1,5),(1,4)))
        lower += [pair((w,5),(w,6)),pair((w,7),(w,8))]
        tables.append(dict(copy=i,offset=d,owners=ids,shared=j,private=l if i in repairs else None))
        totals['exact_closed_reachable_owner_tables']+=1
        offset+=len(regions[3*i]['bands'])+len(regions[3*i+1]['bands'])
        if i+1<q:offset+=1
    assert len(units)==q and len(units|repair_units)==q+s
    assert old|interface==A and not old&interface
    all_seen,_=closure(data,A)
    assert set().union(set(),*(data[3][o] for o in all_seen))==units|repair_units
    assert not all_seen&B and len(all_seen)==8*q
    assert set(lower)<=set(data[2]) and set(upper)<=set(data[2])
    local=restrict(data,set(range(len(data[1])))-interface,Q)
    f=fork_flow(*local);assert (f['value'],f['cost'])==(q,2*q-s)
    direct=fork_flow(*restrict(data,interface,Q));assert (direct['value'],direct['cost'])==(q,0)
    # A maximum preserving every old alpha cannot pay any unrepaired I.
    # Remove just those source-only owners; every remaining alpha must be
    # paid at value q+s. This yields the protected optimum and exact cost.
    forbidden={copy_roots[i][1] for i in range(q) if i not in repairs}
    kept=sorted(set(range(len(data[1])))-forbidden)
    protected=restrict(data,set(kept),Q);pf=fork_flow(*protected)
    paid={o for c in pf['certificates'] for o in c['owners']} & owner_data(*protected[:2])[1]
    assert {kept.index(o) for o in old}<=paid
    assert (pf['value'],pf['cost'])==(q+s,2*q-s)
    # Explicit prescribed realization, retaining all old identities and
    # assigning each j/l at most once, independent of solver tie-breaking.
    witness=[e for i in range(q) for e in ([upper[i]] if i in repairs else lower[2*i:2*i+2])]
    assert len(witness)==2*q-s and len({v for e in witness for v in e})==2*len(witness)
    assert evaluate(*data[:2],witness,*data[3:])['value']==q+s
    assigned=[(copy_roots[i][0],tables[i]['private'] if i in repairs else tables[i]['shared']) for i in range(q)]
    assigned += [(copy_roots[i][1],tables[i]['shared']) for i in repairs]
    assert len(assigned)==q+s and len({a for a,j in assigned})==q+s
    assert len({j for a,j in assigned})==q+s and all(j in Q for a,j in assigned)
    if q<=5:
        maxima=[]
        unrepair={tables[i]['shared'] for i in range(q) if i not in repairs}
        for J in subsets(units):
            F=Q-J
            oldv=fork_flow(*restrict(data,set(range(len(data[1])))-interface,F))['value']
            hv=fork_flow(*restrict(data,interface,F))['value']
            deficit=q-oldv+q-hv-len(J)
            assert oldv==q-len(J&unrepair) and hv==q-len(J)
            assert deficit==len(J&unrepair)
            joint=fork_flow(*(*data[:3],{o:js&F for o,js in data[3].items()},F))
            assert joint['value']==q+s-len(J) # each removed j loses one globally
            if deficit==q-s:maxima.append(J)
            totals['full_pool_shared_withdrawals']+=1
        assert len(maxima)==2**s and set.intersection(*maxima)==unrepair
    if q<=2 and w<=10:
        assert constrained_primitive(data,set())==(q+s,s)
        assert constrained_primitive(data,old)==(q+s,2*q-s)
        totals['independent_primitive_profiles']+=2
    if fixture:
        out=dict(shape=cur[:2],selected_points=sorted(T),matching_edges=M,
            freezing_layers=[[x['endpoint'] for x in layer] for layer in layers],
            regions=[dict(bounds=r['bounds'],vertical=r['vertical']) for r in regions],
            kinds=sorted(data[0].items()),pairs=data[1],links=data[2],
            resources=sorted(Q),support=[(o,sorted(js)) for o,js in data[3].items()],
            old=sorted(old),interface=sorted(interface),tables=tables,
            closure=sorted(all_seen),owner_links=sorted({(own[u],own[v]) for u,v in data[2] if own[u]!=own[v]}),
            value=q+s,unrestricted_minimum_links=s,protected_minimum_links=2*q-s,
            local_value=q,interface_standalone=q,deficit=q-s,numerical_slack=record['slack'],
            availability='FULL original pool, including every boundary and zero-owner unit; no reservation.')
        (Path(__file__).parent/'fixtures/full_pool_interface_singleton.json').write_text(json.dumps(out,indent=2)+'\n')
    totals['fully_frozen_full_pool_boards']+=1;totals['actual_frozen_endpoints']+=len(P)
    totals['distinct_repaired_copies']+=s;totals['protected_source_identities']+=q
    totals['full_pool_deficit']+=q-s
    return dict(W=w,q=q,repairs=sorted(repairs),original_units=len(Q),closed_local_value=q,
        standalone_interface_value=q,joint_and_full_value=q+s,interface_gain=s,deficit=q-s,
        unrestricted_minimum_links=s,protected_minimum_links=2*q-s,numerical_slack=record['slack'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[]
    for w in (8,10):
        for q in range(1,5):
            for H in subsets(range(q)):
                records.append(full_pool_check(w,q,H,totals,fixture=(w,q,H)==(8,1,set())))
    for w,q in itertools.product((12,20,40,64),(1,3,5)):
        for H in {frozenset(),frozenset(range(q)),frozenset(range(0,q,2))}:
            records.append(full_pool_check(w,q,set(H),totals))
    report=dict(status='PASS',totals=dict(totals),records=records,
        proof='docs/FULL_POOL_INTERFACE_SINGLETON_AND_REPAIR_PROFILE.md',
        scope='Complete original pools, actual M-crossing mixed partitions, arbitrary-route eight-owner closure excluding every beta/other interval, exact all-subset repair value and protected/unrestricted costs; uniform all-W/q/H arguments are written, finite checks corroborate.',
        limits=['Same underlying sealed-board family as the prior full-pool singleton note; new actual-crossing positive-local-payment interface specialization and repair/cost profile.',
                'Not a numerical grid counterexample, not a global P/T extremum or failure for arbitrary alternative partitions; universal5over6 open.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
