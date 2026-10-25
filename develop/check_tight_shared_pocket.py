"""Solver-free full-pool cost obstruction for a shared guarded pocket.

All-size proofs and scope: SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md.
Optional Z3 discovery is not imported. Assertions must be enabled.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_normal_form import whole_support_data, ordinary_flow, optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')
FIXTURE=Path(__file__).parent/'fixtures/frozen_shared_pocket_tight.json'


def fixture(q=1,filled=frozenset(),padding=0):
    assert q>=1 and set(filled)<=set(range(q)) and padding>=0 and padding%2==0
    j=json.loads(FIXTURE.read_text())
    moves=[lambda v,i=i:(v[0]+16*i,v[1]) for i in range(q)]
    current=(16*q,14+padding,{f(tuple(v)) for f in moves for v in j['selected']},
        [tuple(f(tuple(v)) for v in e) for f in moves for e in j['matching']]+
        [((8+16*i,5),(8+16*i,6)) for i in sorted(filled)])
    layers=[[f(tuple(w['endpoint'])) for f in moves for w in layer] for layer in j['freezing_layers']]
    if filled:
        layers.append([(8+16*i,c) for i in sorted(filled) for c in (5,6)])
    return current,layers


def check(current,bands,q,filled,move,totals,padding=0):
    direct_check(*current)
    endpoints={v for e in current[3] for v in e}
    assert frozen_certificate(current)[0]==endpoints
    data,meta,_=whole_support_data(current,bands)
    independent_kinds,components=independent_strands(current,bands)
    assert independent_kinds==data[0]
    independent_pairs={tips for tips,_ in components if tips}
    assert independent_pairs=={frozenset(pair) for pair in data[1]}
    totals['independent_strand_reconstructions']+=1
    added={frozenset(move((8+16*i,c)) for c in (5,6)) for i in filled}
    old_current=(*current[:3],[edge for edge in current[3] if frozenset(edge) not in added])
    old,old_meta,_=whole_support_data(old_current,bands)
    identities=lambda d,m:{(m['intervals'][j]['band'],m['intervals'][j]['first'],
        m['intervals'][j]['last']) for j in d[4]}
    lost={(4+8*i,c,c) for i in filled for c in (5,6)}
    assert identities(old,old_meta)-lost==identities(data,meta)
    totals['exact_original_interval_deletion_checks']+=1
    owner,aa,bb,mm=owner_data(*data[:2])
    assert (len(current[2]),len(endpoints))==(27*q,72*q+2*len(filled))
    assert (len(aa),len(bb),len(mm))==(2*q,3*q+len(filled),5*q)
    if padding==0:
        assert len(data[4])==32*q-2*len(filled)
        assert len(data[4])+len(bb)-len(aa)==33*q-len(filled)
    paid=set();beta_used=set();interval_used=set()
    for i in range(q):
        f=lambda p:move((p[0]+16*i,p[1]))
        a,b=owner[f((8,4))],owner[f((8,7))]
        assert a!=b and {a,b}<=aa
        assert set(data[1][a])=={f((3,2)),f((8,4))}
        assert set(data[1][b])=={f((3,5)),f((8,7))}
        paid|={a,b}
        if i in filled:
            assert not data[3][a] and not data[3][b]
            old,new=owner[f((3,3))],owner[f((8,6))]
            assert old!=new and {old,new}<=bb
            assert not data[3][new]
            assert {edge[0] for edge in data[2] if edge[1] in data[1][new]}=={
                f((8,4)),f((8,7))}
            assert (f((3,2)),f((3,3))) in data[2]
            assert (f((8,7)),f((8,6))) in data[2]
            assert not beta_used&{old,new}
            beta_used|={old,new}
        else:
            units={meta['owner'][4+8*i,c] for c in (5,6)}
            assert len(units)==2 and units<=data[4]
            assert data[3][a]==data[3][b]==units
            assert not interval_used&units
            interval_used|=units
    assert paid==aa
    # A filled-copy source has no zero-link interval payment. Paying all
    # such distinct sources costs at least one outgoing link EACH, even
    # inside a fork. The two explicitly distinct beta stems attain this.
    for solver in (ordinary_flow,fork_flow):
        answer=solver(*data)
        assert (answer['value'],answer['cost'])==(2*q,2*len(filled))
        totals['full_pool_value_cost_comparisons']+=1
    if q<=2:
        answer=optimize(*data)
        assert (answer['value'],answer['cost'])==(2*q,2*len(filled))
        totals['independent_primitive_packs']+=1
    totals['fully_frozen_boards']+=1
    return dict(copies=q,filled=sorted(filled),payment=2*q,minimum_links=2*len(filled),
        available_intervals=len(data[4]),margin=len(data[4])+len(bb)-len(aa))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();totals=Counter();records=[]
    for q in range(1,13):
        masks=range(1<<q) if q<=6 else [0]+[(1<<s)-1 for s in range(1,q+1)]
        for mask in masks:
            filled={i for i in range(q) if mask>>i&1}
            cur,layers=fixture(q,filled);check_rank_certificate(cur,layers)
            records.append(check(cur,whole_bands(cur),q,filled,lambda v:v,totals))
    for padding,plug in itertools.product((2,4,10,24),(False,True)):
        filled={0} if plug else set();cur,layers=fixture(1,filled,padding)
        check_rank_certificate(cur,layers)
        records.append(check(cur,whole_bands(cur),1,filled,lambda v:v,totals,padding))
        totals['right_padding_controls']+=1
    for sym,plug in itertools.product(itertools.product((False,True),repeat=3),(False,True)):
        filled={0} if plug else set();cur,layers=fixture(1,filled)
        move=image_map(*cur[:2],sym);shape,T,M=transformed(*cur,*sym)
        image=(*shape,T,M)
        bands=[[tuple(map(move,col)) for col in band] for band in whole_bands(cur)]
        check_rank_certificate(image,[[move(v) for v in layer] for layer in layers])
        check(image,bands,1,filled,move,totals)
        totals['carried_band_isometries']+=1
    report=dict(status='PASS',totals=dict(totals),controls=records,
        scope='Actual frozen full-pool minimum-link cost rises from0to2 after shared-pocket '
        'completion. Full payment remains2. All-q copied/subset family has cost2|S|. '
        'Counterexample to cost-nonincreasing completion, not to universal compensation or5/6.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
