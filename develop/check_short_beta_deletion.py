"""Solver-free actual frozen-board obstruction to reverse pocket completion.

The four-point closed dependency core excludes EVERY strict freezing order,
not just the output of one peeling run. General stacking and ledger proofs
are in SHORT_BETA_DELETION_AND_FREEZING_OBSTRUCTION.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_forced_pocket_guards_and_cycle_elimination import inspect_geometry,blocks
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import whole_support_data,ordinary_flow,optimize,evaluate

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')

FIXTURE=Path(__file__).parent/'fixtures/frozen_short_beta_deletion.json'


def base():
    j=json.loads(FIXTURE.read_text())
    return (*j['shape'],set(map(tuple,j['selected'])),
            [tuple(map(tuple,e)) for e in j['matching']]),j


def closed_core(current,core):
    mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    if not core or not core<=set(mate):return False
    return all(sum(w in current[2] or (w in mate and mate[w] not in core)
        for w in set(neighbors(p))-{mate[p]})<=1 for p in core)


def identities(data,meta):
    return {(meta['intervals'][j]['band'],meta['intervals'][j]['first'],meta['intervals'][j]['last'])
            for j in data[4]}


def family(q,deleted,padding=0):
    cur,j=base();assert q>=1 and set(deleted)<=set(range(q)) and padding>=0 and padding%2==0
    move=lambda v,i:(v[0]+16*i,v[1])
    current=(16*q,14+padding,{move(v,i) for i in range(q) for v in cur[2]},
        [tuple(move(v,i) for v in e) for i in range(q) for e in cur[3]])
    targets={frozenset(move(tuple(v),i) for v in j['target']) for i in deleted}
    after=(*current[:3],[e for e in current[3] if frozenset(e) not in targets])
    layers=[[move(tuple(w['endpoint']),i) for i in range(q) for w in layer]
            for layer in j['freezing_layers']]
    cores=[{move(tuple(v),i) for v in j['closed_core']} for i in sorted(deleted)]
    return current,after,layers,cores


def check_pair(current,after,bands,layers,cores,q,deleted,totals,independent=False,unsupported=True):
    direct_check(*current);direct_check(*after)
    check_rank_certificate(current,layers)
    data,motifs=inspect_geometry(current,bands,totals)
    if unsupported:assert all(not data[3][a] for m in motifs for a in m['ends'])
    assert sorted((len(a),len(b)) for a,b in blocks(data,motifs))==[(2,2)]*q
    new,meta,_=whole_support_data(after,bands)
    old,oldmeta,_=whole_support_data(current,bands)
    assert data==old
    count=len(deleted)
    assert len(new[4])==len(old[4])+2*count
    assert identities(old,oldmeta)<=identities(new,meta)
    originalP={v for e in current[3] for v in e};remaining={v for e in after[3] for v in e}
    assert len(originalP)==90*q and len(remaining)==90*q-2*count
    frozen,after_layers=frozen_certificate(after)
    assert len(remaining-frozen)==40*count
    mate={v:w for e in after[3] for v,w in (e,e[::-1])}
    rank={tuple(w['endpoint']):i for i,l in enumerate(after_layers) for w in l}
    assert set(rank)==frozen
    for p in frozen:
        kept={w for w in neighbors(p) if w!=mate[p] and
              (w in after[2] or (w in mate and mate[w] in rank and rank[mate[w]]<rank[p]))}
        assert len(kept)>=2
        totals['partial_rank_events_checked']+=1
    if count:assert closed_core(after,remaining-frozen)
    assert len(cores)==count and all(closed_core(after,c) for c in cores)
    assert not cores or closed_core(after,set().union(*cores))
    assert all(not c&frozen for c in cores)
    for solver in (ordinary_flow,fork_flow):
        before_result,after_result=solver(*old),solver(*new)
        assert before_result['value']==2*q
        if unsupported:assert before_result['cost']==2*q
        else:assert 0<=before_result['cost']<=2*q
        assert (after_result['value'],after_result['cost'])==(2*q,2*(q-count))
        for model,result in ((old,before_result),(new,after_result)):
            assert evaluate(*model[:2],result['links'],*model[3:])['value']==2*q
            assert len(result['links'])==result['cost']
            totals['actual_link_pack_checks']+=1
        totals['original_after_value_cost_comparisons']+=1
    if independent:
        for model in (old,new):
            result=optimize(*model)
            flow=fork_flow(*model)
            assert (result['value'],result['cost'])==(flow['value'],flow['cost'])
            totals['independent_primitive_pack_comparisons']+=1
    totals['deletion_pairs']+=1
    totals['closed_core_certificates']+=len(cores)
    totals['destroyed_frozen_endpoints']+=40*count
    return dict(copies=q,deleted=sorted(deleted),unfrozen_after=40*count,
                value=2*q,cost_before=2*q,cost_after=2*(q-count))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();records=[]
    for q in range(1,13):
        masks=range(1<<q) if q<=4 else [0]+[(1<<n)-1 for n in range(1,q+1)]
        for mask in masks:
            deleted={i for i in range(q) if mask>>i&1}
            current,after,layers,cores=family(q,deleted)
            records.append(check_pair(current,after,whole_bands(current),layers,cores,q,deleted,totals,q<=2))
    for padding in range(2,34,2):
        current,after,layers,cores=family(1,{0},padding)
        check_pair(current,after,whole_bands(current),layers,cores,1,{0},totals,True,unsupported=False)
        totals['padding_controls']+=1
    current,after,layers,cores=family(1,{0})
    for sym in itertools.product((False,True),repeat=3):
        move=image_map(*current[:2],sym)
        shape,T,M=transformed(*current,*sym);shape2,T2,M2=transformed(*after,*sym)
        bands=[[tuple(map(move,c)) for c in band] for band in whole_bands(current)]
        check_pair((*shape,T,M),(*shape2,T2,M2),bands,[list(map(move,l)) for l in layers],
                   [{move(v) for v in c} for c in cores],1,{0},totals,True)
        totals['carried_band_isometries']+=1
    core=cores[0]
    for n in range(1,len(core)):
        for subset in itertools.combinations(core,n):
            assert not closed_core(after,set(subset))
            totals['proper_core_subsets_checked']+=1
    j=json.loads(FIXTURE.read_text());old,meta,_=whole_support_data(current,whole_bands(current))
    new,newmeta,_=whole_support_data(after,whole_bands(after))
    assert len(old[4])==30 and len(new[4])==32
    assert identities(new,newmeta)-identities(old,meta)=={(4,5,5),(4,6,6)}
    assert len(current[2])==18 and len(current[3])==45
    assert 16*14//2-18-45-16==33
    # The same obstruction also occurs with a complete recognized tree.
    loop=frozenset({(8,8),(8,9)});target=frozenset(map(tuple,j['target']))
    tree=(*current[:3],[e for e in current[3] if frozenset(e)!=loop])
    tree_frozen,tree_layers=frozen_certificate(tree)
    assert len(tree_frozen)==88
    check_rank_certificate(tree,[[tuple(w['endpoint']) for w in l] for l in tree_layers])
    tree_data,tree_motifs=inspect_geometry(tree,whole_bands(tree),totals)
    assert [(len(a),len(b)) for a,b in blocks(tree_data,tree_motifs)]==[(2,1)]
    both=(*tree[:3],[e for e in tree[3] if frozenset(e)!=target]);direct_check(*both)
    assert closed_core(both,core)
    assert len({v for e in both[3] for v in e}-frozen_certificate(both)[0])==39
    for cur,expected in [(tree,(2,1)),(both,(2,0))]:
        model,_,_=whole_support_data(cur,whole_bands(cur))
        for solver in (ordinary_flow,fork_flow,optimize):
            result=solver(*model)
            assert (result['value'],result['cost'])==expected
            totals['recognized_tree_variant_optimizations']+=1
    control=json.loads(FIXTURE.with_name('frozen_short_beta_deletion_supported.json').read_text())
    simple=(*control['shape'],set(map(tuple,control['selected'])),
            [tuple(map(tuple,e)) for e in control['matching']])
    direct_check(*simple)
    check_rank_certificate(simple,[[tuple(w['endpoint']) for w in l] for l in control['freezing_layers']])
    target=frozenset(map(tuple,control['target']))
    cut=(*simple[:3],[e for e in simple[3] if frozenset(e)!=target]);direct_check(*cut)
    mate={v:w for e in cut[3] for v,w in (e,e[::-1])};tip=(8,4)
    assert {w for w in neighbors(tip) if w!=mate[tip] and w in simple[2]|set(mate)}=={(9,4)}
    assert len(set(mate)-frozen_certificate(cut)[0])==25
    totals['supported_degree_two_control']=1
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),physical=records,
        base=dict(shape=[16,14],selected_count=18,matching_edges=45,frozen_endpoints=90,
                  alpha=2,beta=5,available_intervals=30,target=j['target'],closed_core=j['closed_core'],
                  unfrozen_after=40,scalar_margin_before=33,scalar_margin_after=34,
                  newly_created_intervals=[[4,5,5],[4,6,6]]),
        recognized_tree_variant=dict(first_delete_loop=[[8,8],[8,9]],original_frozen=88,
            graph_vertices=2,graph_edges=1,unfrozen_after_target_deletion=39,
            cost_before=1,cost_after=0,original_tree_freezing_layers=tree_layers),
        scope='Reverse short-beta deletion need not preserve freezing, even with forced PP guards and both alpha owners having empty whole support. Four-point actual closed core excludes every strict certificate. Algebraic cyclic-block elimination and the target inequality remain valid; finite checks do not replace the written all-q proof.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
