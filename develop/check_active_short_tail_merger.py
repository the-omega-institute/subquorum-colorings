"""Solver-free checks of an active frozen short-tail merger and escape lemma.

The optional discovery script is separate; this verifier imports no SAT solver.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_beta_support_fork import restrict
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_short_mixed_chains import chains,contract_flow,fixture_cases
from check_whole_support_fork_normal_form import whole_support_data,optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Assertions required; run without -O.')


def load():
    r=json.loads((Path(__file__).parent/'fixtures/frozen_active_short_tail_merger.json').read_text())
    return r,(*r['shape'],set(map(tuple,r['selected'])),[tuple(map(tuple,e)) for e in r['matching']])


def escape_scan(current,totals):
    data,_,_=whole_support_data(current,whole_bands(current));kinds=data[0]
    mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    _,layers=frozen_certificate(current);rank={tuple(w['endpoint']):i for i,layer in enumerate(layers) for w in layer}
    assert len(rank)==len(mate)
    occupied=current[2]|set(mate);chosen={};records=[]
    retained=lambda v,w:w in current[2] or w in mate and rank[mate[w]]<rank[v]
    for v in kinds:
        r,c=v;side=-1 if r%2==0 else 1
        if kinds[v]!='BP':continue
        if not all(kinds.get((r,c+s))=='TP' and mate.get((r,c+s))==(r,c+2*s) for s in (-1,1)):continue
        vp=(r+side,c);assert mate[v]==vp
        tails=[(r,c-1),(r,c+1)];bps=[mate[t] for t in tails]
        assert all(rank[b]<rank[v] for b in bps)
        for s,b in zip((-1,1),bps):
            assert retained(b,(r,c+3*s)) and retained(b,(r+side,c+2*s))
        available=[]
        for s in (-1,1):
            z=(r+side,c+s);d=(r+side,c+2*s)
            if retained(vp,z):
                assert z in mate and d in mate
                assert rank[mate[z]]<rank[vp]
                assert rank[mate[d]]<rank[(r,c+2*s)]<rank[v]
                assert mate[z] in (d,(r+2*side,c+s))
                available.append(z)
        assert available
        z=min(available);assert z not in chosen;chosen[z]=v
        records.append(dict(center=v,retained_escapes=available,chosen=z))
    totals['geometric_scans']+=1;totals['short_tail_forks']+=len(records);totals['injective_retained_escapes']+=len(chosen)
    return records


def inspect(current,bands,move,layers,totals,independent=False):
    direct_check(*current);check_rank_certificate(current,layers)
    d,meta,_=whole_support_data(current,bands);owner,aa,bb,mm=owner_data(*d[:2])
    key={v:owner[move(v)] for v in [(5,6),(5,7),(5,9),(5,11),(5,12)]}
    sources={key[5,6],key[5,12]};short={key[5,7],key[5,11]};gate=key[5,9]
    assert len(sources)==len(short)==2 and len(sources|short|{gate})==5
    assert sources<=aa and short|{gate}<=mm
    js={meta['owner'][5,10],meta['owner'][5,12]};assert len(js)==2 and js<=d[4]
    assert js<=d[3][gate] and all(not d[3][a]&js for a in sources|short)
    restricted=restrict(d,sources|short|{gate},js)
    ro,ra,rb,rm=owner_data(*restricted[:2]);ng=ro[move((5,9))]
    assert ra=={ro[move((5,6))],ro[move((5,12))]} and not rb
    assert {a for a,us in restricted[3].items() if us}=={ng}
    edges={(u,v) for u,v in restricted[2] if ro[u]!=ro[v]}
    expected={tuple(map(move,e)) for e in [((5,6),(5,7)),((5,8),(5,9)),((5,12),(5,11)),((5,10),(5,9))]}
    assert edges==expected
    correct=fork_flow(*restricted);full=fork_flow(*d)
    assert (correct['value'],correct['cost'])==(1,2)
    assert len(aa)==2 and (full['value'],full['cost'])==(2,0)
    bypasses=[meta['owner'][2,c] for c in (5,13)]
    assert len(set(bypasses))==2 and set(bypasses)<=d[4]
    assert all(j in d[3][key[v]] for v,j in zip(((5,6),(5,12)),bypasses))
    assert all(meta['intervals'][j]==dict(band=2,first=c,last=c) for j,c in zip(bypasses,(5,13)))
    for source in sources:
        single=restrict(d,{source}|short|{gate},js);one=fork_flow(*single)
        assert (one['value'],one['cost'])==(1,2)
    rows,tp,bp,internal=chains(current,bands,restricted)
    assert sorted(map(len,rows))==[1,1]
    reduced=contract_flow(restricted,rows,tp,bp,internal)
    assert reduced['contracted_mixed']==3 and (reduced['value'],reduced['cost'])==(1,2)
    # Every retained restricted owner is alpha reachable; pruning removes none.
    reached=set(ra)
    while True:
        new=reached|{ro[v] for u,v in edges if ro[u] in reached}
        if new==reached:break
        reached=new
    assert reached==set(range(5))
    z,zp=move((6,8)),move((7,8));mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    assert mate[z]==zp and mate[zp]==z
    rank={v:i for i,layer in enumerate(layers) for v in layer}
    assert rank[zp]<rank[move((6,9))]
    assert all(move(v) in mate for v in [(6,7),(7,7),(6,9),(7,9)])
    if independent:
        for data in (restricted,d):
            a=optimize(*data);b=fork_flow(*data);assert (a['value'],a['cost'])==(b['value'],b['cost'])
            totals['independent_primitive_packs']+=1
    totals['physical_cases']+=1;totals['restricted_exact_mergers']+=1;totals['sealed_retained_escape_cycles']+=1
    return dict(restricted_value=1,restricted_minimum_links=2,individual_values=[1,1],
        projection_reachability_value=2,full_value=2,full_minimum_links=0,
        alpha_reachable_owners=5,pruned_owners=0,short_chain_lengths=[1,1],
        original_resources=[meta['intervals'][j] for j in sorted(js)],actual_paying_links=correct['links'],
        shared_gate_tip=move((5,9)),sealed_cycle=[z,zp])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();totals=Counter()
    r,base=load();layers=[[tuple(v) for v in layer] for layer in r['freezing_layers']]
    named=inspect(base,whole_bands(base),lambda v:v,layers,totals,True)
    for sym in itertools.product((False,True),repeat=3):
        shape,t,m=transformed(*base,*sym);move=image_map(*base[:2],sym)
        bands=[[tuple(move(v) for v in col) for col in cols] for cols in whole_bands(base)]
        inspect((*shape,t,m),bands,move,[[move(v) for v in row] for row in layers],totals,True)
    copy_records=[]
    for q,pad in itertools.product(range(1,9),(0,2,10)):
        move=lambda v,i:(v[0]+14*i,v[1])
        cur=(14*q,18+pad,{move(v,i) for i in range(q) for v in base[2]},
             [tuple(move(v,i) for v in e) for i in range(q) for e in base[3]])
        direct_check(*cur);cl=[[move(v,i) for i in range(q) for v in row] for row in layers];check_rank_certificate(cur,cl)
        d,meta,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*d[:2]);keep={o[move(v,i)] for i in range(q) for v in [(5,6),(5,7),(5,9),(5,11),(5,12)]}
        js={meta['owner'][5+7*i,c] for i in range(q) for c in (10,12)};rd=restrict(d,keep,js)
        full=fork_flow(*d);limited=fork_flow(*rd)
        assert len(aa)==2*q and (full['value'],full['cost'])==(2*q,0)
        assert (limited['value'],limited['cost'])==(q,2*q)
        if q<=2:
            x=optimize(*rd);assert (x['value'],x['cost'])==(q,2*q);totals['independent_primitive_packs']+=1
        escape_scan(cur,totals);totals['separated_copy_models']+=1
        copy_records.append(dict(q=q,padding=pad,restricted_value=q,restricted_cost=2*q,full_value=2*q,full_cost=0))
    for cur,_,_ in fixture_cases():escape_scan(cur,totals)
    escape_scan(base,totals)
    result=dict(status='PASS',totals=dict(totals),base=named,copies=copy_records,
        oracle=dict(status='FAILED_NO_REVIEW',task_id='03b95177-eec4-40c3-af54-bbe4f2d5f91b',reason='model_unavailable@selecting_model'),
        scope='Actual alpha-entered short-tail common-BP merger survives reachable pruning and short-chain contraction; separate reachability payments cannot add. Injective retained escape P sites need not be resource units. Restricted-pool obstruction only; full original compensation2q remains. General proofs written separately; no inference from finite enumeration.')
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
