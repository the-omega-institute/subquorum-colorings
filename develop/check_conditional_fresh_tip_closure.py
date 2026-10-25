"""Conditional fresh-TP guards extend the retained occupation certificate.

General proof: docs/CONDITIONAL_FRESH_TIP_CLOSURE.md. Finite checks are
corroboration, not a proof of universal compensation or a 5/6 improvement.
"""
import argparse
from collections import Counter, deque
import json
from pathlib import Path
import random

from check_guarded_promotion_closure import load_model, base_copies, square_switches, inspect as old_inspect
from check_endpoint_extension_replacement import FLEX, static_certificate
from check_cooperative_promotion import neighbors
from check_merger_completion_reserves import feasible, frozen, whole_bands, whole_support_data, owner_data
from check_partial_tip_compensation import lift
from check_reserve_boundary_split import clipped
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import ordinary_flow, optimize
from check_whole_support_fork_flow import fork_flow
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_protected_shared_columns import family as long_columns, join

if not __debug__: raise RuntimeError('Run without -O.')

PROTECTED=[((1,14),(1,13)),((1,18),(1,19)),
 ((8,22),(8,21)),((9,22),(9,21)),((10,1),(10,2)),((10,22),(10,21)),
 ((11,1),(11,2)),((11,22),(11,21)),((12,22),(12,21)),((13,22),(13,21)),
 ((14,22),(14,21)),((15,22),(15,21)),((16,10),(16,11)),((16,22),(16,21)),
 ((17,8),(17,7)),((17,10),(17,11)),((17,22),(17,21)),((18,22),(18,21)),
 ((19,9),(19,8)),((19,22),(19,21)),((20,22),(20,21)),
 ((21,13),(21,12)),((21,14),(21,13)),((21,22),(21,21)),
 ((24,13),(24,12)),((24,14),(24,13)),((24,15),(24,14))]


def endpoints(cur): return {v for e in cur[3] for v in e}
def partner(v): return (v[0]^1,v[1])
def shift(v,i): return (v[0],v[1]+24*i)


def audit(base):
    P=endpoints(base);O=P|base[2];old,_=static_certificate(base)
    assert len(PROTECTED)==len({v for v,w in PROTECTED})==len({w for v,w in PROTECTED})==27
    records=[]
    for v,w in PROTECTED:
        t=partner(v);q=partner(w);z=(w[0],2*w[1]-v[1]);cells={z,partner(z)}
        assert v not in O and t not in O and not set(neighbors(t))&O
        assert not set(neighbors(v))&base[2]
        assert w not in O and w in neighbors(v)
        blockers=sorted(set(neighbors(w))&O);assert blockers
        assert set(blockers).isdisjoint({v,q})
        direct=sorted(cells&P)
        exterior=[(x,a) for x in sorted(cells) for a in sorted(set(neighbors(x))&O-cells)]
        assert direct or exterior
        assert w not in {u for _,u in FLEX}
        assert (w[0]//2,w[1]) not in {(u[0]//2,u[1]) for _,u in FLEX}
        assert w not in {target[1] for target in old} and w!=(3,13)
        assert 0<w[1]<23
        records.append(dict(source=v,target=w,selection=t,blank_partner=q,
            selection_blocker=blockers[0],outer_column=z,
            nonTT_old_endpoint=direct[0] if direct else None,
            nonTT_external_guard=exterior[0] if not direct else None))
    for v,w in PROTECTED:
        for x,y in PROTECTED:
            if (w[0]//2,w[1])==(y[0]//2,y[1]):
                assert v==x or v==partner(x)
    return records


def augment_with_selection(cur,start):
    """Actual augmenting path; allows a newly added unsaturated selection.
    Occupation is unchanged on old P, so check the two new endpoints only.
    """
    T=cur[2];P=endpoints(cur);O=T|P
    assert start not in O
    if any(len(set(neighbors(t))&(O|{start}))>1 for t in T): return None
    mate={v:w for e in cur[3] for v,w in (e,e[::-1])}
    todo=deque([(start,[],[],{start})]);seen={start}
    while todo:
        v,added,removed,used=todo.popleft()
        for w in sorted(neighbors(v)):
            if not (0<=w[0]<cur[0] and 0<w[1]<cur[1]) or w in used or w in T: continue
            if w not in P:
                if any(w in neighbors(t) and set(neighbors(t))&(O|{start}) for t in T): continue
                drop={frozenset(e) for e in removed}
                trial=(*cur[:3],[e for e in cur[3] if frozenset(e) not in drop]+added+[(v,w)])
                if feasible(trial): return trial
            else:
                z=mate[w]
                if z in used or z in seen: continue
                seen.add(z);todo.append((z,added+[(v,w)],removed+[(w,z)],used|{w,z}))
    return None


def activate(cur,v):
    P=endpoints(cur);t=partner(v)
    if v in cur[2] or t in P: return None
    trial=(*cur[:2],cur[2]|{t},cur[3])
    if v in P: return trial if feasible(trial) else None
    return augment_with_selection(trial,v)


def inspect(base,initial,cur,n,totals,independent=False):
    P=endpoints(cur);P0=endpoints(initial)
    assert initial[2]<=cur[2] and P0<=P and feasible(cur)
    d,meta,_=whole_support_data(cur,whole_bands(cur));old,_=static_certificate(base)
    tips={v for v,k in d[0].items() if k=='TP'}
    assignment={};pool=set();h=p=g=q=0
    for i in range(n):
        for target,v in old.items(): assignment['bp',shift(target[1],i)]=shift(v,i)
        local_flexible=[]
        for v,w in FLEX:
            local_flexible.append((shift(v,i),shift(w,i)))
            h+=shift(w,i) in P
        t,v,w,b=map(lambda x:shift(x,i),[(2,14),(3,14),(3,13),(2,13)])
        if t in cur[2]:
            assert b not in cur[2]|P and d[0][w]=='BP'
            assignment['bp',w]=v;p+=1
        for v,w in PROTECTED:
            v,w=shift(v,i),shift(w,i)
            if v in tips:
                assert v not in P0
                local_flexible.append((v,w));g+=1;q+=w in P
        for v,w in local_flexible:
            assert v in tips and w not in cur[2] and partner(w) not in cur[2]|P
            if w in P:
                assert d[0][w]=='BP' and (v,w) in d[2]
                target=('bp',w)
                assert target not in assignment;assignment[target]=v
            else:
                unit=meta['owner'][w[0]//2,w[1]]
                assert meta['intervals'][unit]==dict(band=w[0]//2,first=w[1],last=w[1])
                assert unit in d[4] and unit not in pool
                pool.add(unit);assignment['interval',unit,0]=v
    covered=set(assignment.values());fresh=tips-P0
    protected={shift(v,i) for i in range(n) for v,w in PROTECTED}&fresh
    holes=fresh-protected
    assert g==len(protected) and len(covered)==len(assignment)==23*n+p+g
    assert tips-covered==holes
    assert len(pool)==5*n-h+g-q
    C=[(v,t[1]) for t,v in assignment.items() if t[0]=='bp']
    assert len(C)==18*n+h+p+q
    _,inventory,records=cancel_pairs(*d[:2],C,Counter())
    final_alphas=[r for r in records if not r['cycle'] and r['alpha']==r['beta']+1]
    k=sum(set(r['ends'])<=holes for r in final_alphas)
    paid=len(final_alphas)-k;r=len(pool);e=len(holes)
    assert 2*k<=e and paid<=min(r,(r+e)//2)
    assert len(fresh)+p<=len(cur[2]-initial[2])
    assert 2*k<=len(cur[2]-initial[2])-p-g
    dd=clipped(d,pool);certificate=lift(dd,assignment)
    assert certificate['holes']==e and certificate['certified_deficit']==k
    ordinary=ordinary_flow(*dd);full=fork_flow(*dd)
    assert full['deficit']<=ordinary['deficit']<=k
    if e<=1: assert k==ordinary['deficit']==full['deficit']==0
    if independent:
        for forks in (False,True):
            primitive=optimize(*dd,allow_forks=forks);expected=full if forks else ordinary
            assert (primitive['value'],primitive['cost'])==(expected['value'],expected['cost'])
            totals['independent_primitive_comparisons']+=1
    is_frozen=frozen(cur)
    totals['models']+=1;totals['frozen' if is_frozen else 'feasible_nonfrozen']+=1
    totals['protected_fresh_active_models']+=g>0
    totals['protected_new_BP_models']+=q>0
    totals['coarse_budget_strict_improvement_models']+=e//2<len(fresh)//2
    totals['all_fresh_protected_models']+=bool(g) and e==0
    totals['max_simultaneous_protected_fresh']=max(totals['max_simultaneous_protected_fresh'],g)
    return dict(copies=n,protected_fresh=g,protected_BP_targets=q,unprotected_fresh=e,
        all_fresh=len(fresh),promotions=p,old_filled_targets=h,certificate_links=len(C),
        assigned_units=r,exact_strategy_loss=k,ordinary_deficit=ordinary['deficit'],
        ordinary_cost=ordinary['cost'],frozen=is_frozen,endpoints=len(P),selected=len(cur[2]))


def frozen_caps(base,n):
    initial=base_copies(base,n)
    record=json.loads(Path('develop/fixtures/conditional_fresh_tip_frozen_caps.json').read_text())
    new_t={shift(tuple(v),i) for i in range(n) for v in record['new_selected']}
    new_m=[tuple(shift(tuple(v),i) for v in edge) for i in range(n) for edge in record['new_matching']]
    cur=(*initial[:2],initial[2]|new_t,initial[3]+new_m)
    layers=[[w['endpoint'] for w in layer] for layer in frozen_certificate(initial)[1]]
    layers.append([v for edge in new_m for v in edge])
    check_rank_certificate(cur,layers)
    return initial,cur


def supplement(base,totals,named):
    for n in range(1,9):
        initial,cur=frozen_caps(base,n)
        info=inspect(base,initial,cur,n,totals,independent=n<=2)
        assert info['frozen'] and info['protected_fresh']==2*n and info['promotions']==n
        assert info['protected_BP_targets']==info['unprotected_fresh']==info['ordinary_deficit']==0
        assert info['certificate_links']==21*n and info['assigned_units']==5*n
        totals['frozen_caps_independent_rank_checks']+=1
        named['frozen_caps_'+str(n)]=info
    # Protected closure and genuinely unprotected fresh alphas coexist.
    for n in (1,2,3):
        initial,core=frozen_caps(base,n)
        for m in (1,2,4):
            cur=join(core,long_columns(m,2)[0])
            info=inspect(base,initial,cur,n,totals,independent=n==1 and m==1)
            assert info['frozen'] and info['unprotected_fresh']==2*m
            assert info['exact_strategy_loss']==info['ordinary_deficit']==m
            data,_,_=whole_support_data(cur,whole_bands(cur))
            assert ordinary_flow(*data)['deficit']==0
            totals['mixed_protected_unprotected_frozen_controls']+=1
            named['unprotected_'+str((n,m))]=info
    j=json.loads(Path('develop/fixtures/conditional_fresh_tip_old_pool_loss_nonfrozen.json').read_text())
    cur=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
    before=old_inspect(base,base,cur,1,Counter(),independent=True,full_pool=True)
    after=inspect(base,base,cur,1,totals,independent=True)
    assert not before['frozen'] and not after['frozen']
    assert before['ordinary_deficit']==before['exact_certificate_loss']==1
    assert after['ordinary_deficit']==after['exact_strategy_loss']==after['unprotected_fresh']==0
    assert after['protected_fresh']==11 and after['protected_BP_targets']==5
    named['actual_old_pool_loss_repaired']=dict(before=before,after=after)
    totals['actual_old_pool_loss_repaired_controls']+=1


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    base,*_=load_model();audit_records=audit(base);totals=Counter();named={};rng=random.Random(2026102509)
    for n in range(1,7):
        initial=base_copies(base,n)
        inspect(base,initial,initial,n,totals,n<=2)
        for v,w in PROTECTED:
            for i in ([0] if n==1 else [0,n-1]):
                cur=activate(initial,shift(v,i))
                if cur is None:
                    totals['single_activation_no_augmenting_completion']+=1;continue
                info=inspect(base,initial,cur,n,totals,independent=n==1)
                if n==1:named[str(v)]=info
                for v2,w2 in PROTECTED:
                    # Test actual occupation of the chosen target after activation.
                    if v2!=v:continue
                    w2=shift(w2,i)
                    if w2 not in endpoints(cur)|cur[2]:
                        occupied=augment_with_selection(cur,w2)
                        if occupied is not None:
                            inspect(base,initial,occupied,n,totals,independent=n==1)
                            totals['target_occupation_controls']+=1
                if n<=2:
                    for sq,rematched in list(square_switches(cur))[:3]:
                        inspect(base,initial,rematched,n,totals)
                        totals['actual_rematching_controls']+=1
        print(json.dumps(dict(progress_copy_count=n,models=totals['models'])),flush=True)
        for run in range(8):
            cur=initial;options=[shift(v,i) for i in range(n) for v,w in PROTECTED];rng.shuffle(options)
            accepted=0
            for v in options:
                trial=activate(cur,v)
                if trial is None:continue
                cur=trial;accepted+=1
                info=inspect(base,initial,cur,n,totals,independent=n<=2 and accepted==2 and run<2)
            named['many_'+str((n,run))]=info
            totals['simultaneous_activation_runs']+=1
    # Explicit all-frozen two-protected-end fixture, when construction permits.
    cur=base
    for v in [(19,9),(24,15)]:
        cur=activate(cur,v);assert cur is not None
    named['two_fresh_caps']=inspect(base,base,cur,1,totals,True)
    ff,layers=frozen_certificate(cur)
    if len(ff)==len(endpoints(cur)):
        check_rank_certificate(cur,[[w['endpoint'] for w in layer] for layer in layers])
        totals['two_cap_independent_rank_checks']+=1
    # Saved frozen 310P geometry from previous turn: one fresh protected TP.
    j=json.loads(Path('develop/fixtures/guarded_promotion_fresh_tip_frozen.json').read_text())
    cur=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
    named['existing_frozen_310P']=inspect(base,base,cur,1,totals,True)
    supplement(base,totals,named)
    report=dict(status='PASS',counts=dict(totals),local_witness_audit=audit_records,named=named,
      scope='Written arbitrary-extension theorem; 27 conditional fresh-tip sites per actual base copy, distinct BP targets and distinct available original units; arbitrary T/P additions and rematching; only unprotected fresh tips count as holes. Universal compensation and 5/6 remain open.')
    a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals),two_caps=named['two_fresh_caps'])))

if __name__=='__main__':main()
