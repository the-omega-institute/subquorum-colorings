"""Solver-free local completion and full-pool private-resource elimination.

All assertions concern original matching-retaining extensions. Finite checks
corroborate the general guarded-gap classification and elimination proof.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_active_short_tail_merger import load
from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors
from check_frozen_beta_support_fork import restrict
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_whole_support_fork_normal_form import whole_support_data,optimize
from check_whole_support_fork_flow import fork_flow
from check_frozen_tip_slot_obstruction import fixture as residual_fixture

if not __debug__:raise RuntimeError('Run without -O.')

EDGES=[((4,3),(5,3)),((5,3),(5,4)),((5,4),(5,5))]
STATES=[('empty',(),False),('selection',(),True),('cycle',(0,),False),
        ('inner_beta',(1,),False),('outer_beta',(2,),False),('cycle_beta',(0,2),False)]


def complete(base,state):
    _,es,selected=state
    return (*base[:2],base[2]|({(5,4)} if selected else set()),base[3]+[EDGES[i] for i in es])


def frozen(current):return len(frozen_certificate(current)[0])==2*len(current[3])


def inspect(current,bands,centers,totals,move=lambda v:v,independent=False):
    direct_check(*current);assert frozen(current)
    d,meta,_=whole_support_data(current,bands);o,aa,bb,mm=owner_data(*d[:2]);mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    deleted=set();units=set();filled=0;chosen=[]
    for offset in centers:
        mv=lambda v:move((v[0]+offset,v[1]));band=2+offset//2
        left,right=o[mv((5,6))],o[mv((5,12))]
        assert left in aa and right in aa and left!=right
        assert all(mv(v) not in mate and mv(v) not in current[2] for v in [(4,4),(4,5),(4,13),(5,13),(5,14)])
        assert mv((4,14)) in current[2]
        rj=meta['owner'][band,13]
        assert rj in d[4] and meta['intervals'][rj]==dict(band=band,first=13,last=13)
        assert {a for a,js in d[3].items() if rj in js}=={right}
        assert mate[mv((4,2))]==mv((5,2))
        deleted|={left,right};units.add(rj)
        if mv((5,5)) in mate:
            assert mate[mv((5,5))]==mv((5,4))
            assert mate[mv((4,3))]==mv((5,3))
            beta=o[mv((5,5))];assert beta in bb and not d[3][beta]
            incoming={(u,v) for u,v in d[2] if o[v]==beta}
            assert incoming=={(mv((5,6)),mv((5,5)))}
            assert not d[3][left], 'Fixed-rectangle filled-cap alpha has no available whole support.'
            deleted.add(beta);filled+=1;chosen.append(dict(kind='beta',tip=mv((5,5))))
        else:
            lj=meta['owner'][band,5]
            assert lj in d[4] and meta['intervals'][lj]==dict(band=band,first=5,last=5)
            assert {a for a,js in d[3].items() if lj in js}=={left}
            units.add(lj);chosen.append(dict(kind='interval',identity=meta['intervals'][lj]))
    keep=set(range(len(d[1])))-deleted;res=restrict(d,keep,d[4]-units)
    full=fork_flow(*d);remainder=fork_flow(*res)
    assert full['value']==2*len(centers)+remainder['value']
    assert full['cost']==filled+remainder['cost']
    if independent:
        for data in (d,res):
            x=optimize(*data);y=fork_flow(*data);assert (x['value'],x['cost'])==(y['value'],y['cost'])
            totals['independent_primitive_packs']+=1
    totals['frozen_completion_models']+=1;totals['settled_old_alphas']+=2*len(centers)
    totals['exclusive_beta_payments']+=filled;totals['private_interval_payments']+=2*len(centers)-filled
    totals['exact_value_and_cost_eliminations']+=1
    totals['nonempty_residual_alpha_cases']+=bool(owner_data(*res[:2])[1])
    totals['positive_residual_payment_cases']+=remainder['value']>0
    totals['positive_residual_cost_cases']+=remainder['cost']>0
    return dict(filled_caps=filled,full_value=full['value'],full_cost=full['cost'],residual_value=remainder['value'],residual_cost=remainder['cost'],settled_alphas=2*len(centers),left_units=chosen)


def additions(current):
    P={v for e in current[3] for v in e};blanks={(r,c) for r in range(current[0]) for c in range(current[1])}-P-current[2]
    for v in sorted(blanks):yield ('T',v),(*current[:2],current[2]|{v},current[3])
    for v in sorted(blanks):
        for w in sorted(set(neighbors(v))&blanks):
            if v<w:yield ('M',(v,w)),(*current[:2],current[2],current[3]+[(v,w)])


def feasible(current):
    occupied=current[2]|{v for e in current[3] for v in e}
    if any(c==0 for r,c in occupied):return False
    if any({(r,current[1]-1),(r+1,current[1]-1)}<=occupied for r in range(0,current[0],2)):return False
    try:direct_check(*current);return True
    except AssertionError:return False


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();totals=Counter();r,base=load();named={};good=[]
    for state in STATES:
        cur=complete(base,state);direct_check(*cur);ff,layers=frozen_certificate(cur)
        is_good=len(ff)==2*len(cur[3]);assert is_good==(state[0] not in ('inner_beta','outer_beta'))
        if is_good:
            good.append((state,cur));named[state[0]]=inspect(cur,whole_bands(cur),[0],totals,independent=True)
        else:
            v=(5,4);mate={x:y for e in cur[3] for x,y in (e,e[::-1])}
            assert len(set(neighbors(v))&(cur[2]|set(mate))-{mate[v]})==1
            totals['degree_two_nonfreezing_controls']+=1
    # All local label/matching states: four mutable sites with only these edges.
    # 0=blank,1=selected,2=endpoint; frozen exclusion is checked by geometry above.
    states=Counter()
    for flags in itertools.product(range(3),repeat=4):
        u,v,w,x=[(4,3),(5,3),(5,4),(5,5)];ts={p for p,f in zip((u,v,w,x),flags) if f==1}
        ps={p for p,f in zip((u,v,w,x),flags) if f==2}
        for mask in range(8):
            es=[e for i,e in enumerate(EDGES) if mask>>i&1]
            if len({p for e in es for p in e})!=2*len(es) or {p for e in es for p in e}!=ps:continue
            cur=(*base[:2],base[2]|ts,base[3]+es)
            if feasible(cur):states[str((tuple(i for i in range(3) if mask>>i&1),tuple(sorted(ts))))]+=1
    assert len(states)==6 and sum(states.values())==6;totals['exhaustive_local_feasible_states']=6
    for state,cur in good:
        for sym in itertools.product((False,True),repeat=3):
            shape,t,m=transformed(*cur,*sym);move=image_map(*cur[:2],sym)
            bands=[[tuple(move(v) for v in col) for col in cols] for cols in whole_bands(cur)]
            inspect((*shape,t,m),bands,[0],totals,move,True)
        # Every single T or matching-edge addition on the fixed rectangle.
        for tag,ext in additions(cur):
            totals['single_addition_candidates']+=1
            if not feasible(ext):continue
            totals['single_addition_feasible']+=1
            if not frozen(ext):continue
            inspect(ext,whole_bands(ext),[0],totals)
            totals['single_addition_frozen']+=1
    # All four frozen local choices in up to four copies. Nonempty residual
    # controls below add a separate verified occupied patch.
    for q in range(1,5):
        for choices in itertools.product(range(4),repeat=q):
            copy_cur=[good[i][1] for i in choices];move=lambda v,i:(v[0]+14*i,v[1])
            cur=(14*q,18,{move(v,i) for i,c in enumerate(copy_cur) for v in c[2]},
                 [tuple(move(v,i) for v in e) for i,c in enumerate(copy_cur) for e in c[3]])
            record=inspect(cur,whole_bands(cur),[14*i for i in range(q)],totals,independent=q<=2)
            assert record['filled_caps']==sum(good[i][0][0]=='cycle_beta' for i in choices)
            totals['copy_local_choice_models']+=1
    # A separate residual research fixture has exact value/cost h/h. This
    # exercises elimination while an outside compensation problem remains.
    for state,cur in good:
        for h in (1,2,3):
            outside=residual_fixture(h,2);move=lambda v:(v[0]+14,v[1])
            joined=(14+outside[0],18,cur[2]|{move(v) for v in outside[2]},
                    cur[3]+[tuple(move(v) for v in e) for e in outside[3]])
            record=inspect(joined,whole_bands(joined),[0],totals,independent=True)
            assert (record['residual_value'],record['residual_cost'])==(h,h)
            totals['nontrivial_residual_controls']+=1
    # Greedy multi-addition samples; inspect every accepted frozen prefix.
    rng=random.Random(20261025)
    for state,initial in good:
        for run in range(12):
            cur=initial
            for depth in range(6):
                candidates=list(additions(cur));rng.shuffle(candidates);accepted=False
                for tag,ext in candidates:
                    if feasible(ext) and frozen(ext):cur=ext;accepted=True;break
                if not accepted:break
                inspect(cur,whole_bands(cur),[0],totals,independent=run==0 and depth==5)
                totals['multi_addition_frozen_prefixes']+=1
    a.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),local_models=named,
        scope='General six-state guarded-cap classification, four frozen states, private interval or exclusive empty-body beta, and fixed admissible packet rectangle arbitrary monotone feasible completely frozen extension elimination with standard boundary marks and no arbitrary reservations V=2q+Vres,c=filledCaps+cres. Finite checks corroborate written proof, not substitute. Universal compensation and5/6 remain open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
