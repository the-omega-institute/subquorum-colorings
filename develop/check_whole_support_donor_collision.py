"""Actual frozen cross-component donor collision in WHOLE-path support.

The all-even-height construction and rank induction are proved in
WHOLE_SUPPORT_DONOR_COLLISION_AND_FROZEN_PP_SEALS.md. No SAT solver is used.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import solve
from check_even_bridge_support_completion import endpoints_of
from check_frozen_support_tree_reroot import model_at
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_mixed_support_component_merges import verify
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_shared_donor_collision_after_mixed_relays import collision_family

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def sealed(width):
    assert width>=8 and width%2==0
    current,bands=collision_family(width)
    cap=[((r,c),(r+1,c)) for r in range(8,width+1,2) for c in (4,14)]
    return (*current[:3],current[3]+cap),bands


def residual_solve(data,model):
    free={v for pair in model['reduced'] for v in pair}
    return solve({v:k for v,k in data[0].items() if v in free},model['reduced'],
                 [link for link in data[2] if set(link)<=free],
                 {v:s for v,s in data[3].items() if v in free},data[4])


def stable_incidence(model,lower_tips):
    stable={}
    for a,pair in enumerate(model['alphas']):
        labels={lower_tips[v] for v in pair if v in lower_tips}
        assert len(labels)==1
        stable[a]=next(iter(labels))
    assert len(stable)==len(lower_tips)
    return {j:{stable[a] for a in users} for j,users in model['incidence'].items()}


def check(current,bands,move,width,padding,totals):
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    first=[tuple(map(move,((5,5),(5,6))))]
    left=tuple(map(move,((5,7),(5,8))))
    right=tuple(map(move,((5,15),(5,14))))
    alternate=tuple(map(move,((width+4,15),(width+4,14))))
    lower={move((width+4,5)):0,move((width+4,15)):1}
    states={};models={};records=[]
    expected_i=7*width-22+(width+2)*padding
    shared_unit=None
    for name,extra in [('none',[]),('left',[left]),('right',[right]),('both',[left,right])]:
        data,meta,rep,model,betas,_=model_at(current,bands,first+extra)
        assert (rep['alpha'],rep['beta'])==(2,0) and not betas
        incidence=stable_incidence(model,lower)
        assert len(incidence)==expected_i
        assert rep['margin']==expected_i-2
        owned={j:users for j,users in incidence.items() if users}
        if name=='none':
            assert rep['paid']==0 and rep['defect']==2 and not owned
        else:
            assert (rep['paid'],rep['defect'],rep['spare'])==(1,1,expected_i-1)
            assert len(owned)==1
            j=next(iter(owned))
            if shared_unit is None:shared_unit=j
            assert j==shared_unit
            assert owned[j]==({'left':{0},'right':{1},'both':{0,1}}[name])
        states[name]=incidence;models[name]=model
        records.append(dict(state=name,paid=rep['paid'],defect=rep['defect'],
                            owned=[dict(interval=j,owners=sorted(o)) for j,o in owned.items()]))
    for old,new in [('none','left'),('none','right'),('none','both'),('left','both'),('right','both')]:
        result=verify(2,states[old],states[new],totals)
        assert result['gain']==(0 if old in ('left','right') else 1)
        if old=='none' and new=='both':
            assert result['clusters']==[dict(old_components=2,old_deficient=2,old_unused=1,
                activated_loose=1,post_defect=1,payment_gain=1,owners=[0,1])]
    # All original alpha supports are already unpaid before C0 as well.
    data,meta,raw,raw_model,_,_=model_at(current,bands)
    assert len(current[2])==34 and len(current[3])==3*width+10
    assert (meta['original']['alpha'],meta['original']['beta'],meta['original']['gamma'])==(2,0,14)
    assert sum(c['kind']==['cycle'] for c in meta['original']['components'])==2*width-4
    assert len(meta['intervals'])==8*width-20+(width+2)*padding
    assert len(meta['boundary'])==width+2
    legal_links={frozenset(link) for link in data[2]}
    assert all(frozenset(link) in legal_links for link in first+[left,right,alternate])
    assert raw['paid']==0 and raw['defect']==2
    # A different lower mixed exit supplies an ORIGINAL distinct unit.
    repaired=first+[left,right,alternate]
    _,_,after,after_model,_,_=model_at(current,bands,repaired)
    assert (after['alpha'],after['beta'],after['paid'],after['defect'],after['spare'])==(
        2,0,2,0,expected_i-2)
    assert after['margin']==expected_i-2
    free_after={v for p in after_model['alphas'] for v in p}
    exit=move((width+4,13))
    assert exit in free_after
    other_ids={j for j,u in after_model['incidence'].items() if u and j!=shared_unit}
    assert other_ids and data[3][exit] & other_ids
    for state,cost in [('none',2),('both',1)]:
        solved=residual_solve(data,models[state])
        assert (solved['value'],solved['deficit'],solved['cost'])==(2,0,cost)
    optimal_extra=[left,alternate]
    _,_,optimal,_,_,_=model_at(current,bands,first+optimal_extra)
    assert optimal['paid']==2 and optimal['defect']==0
    totals['actual_whole_support_collision_boards']+=1
    totals['actual_whole_support_collision_transitions']+=5
    return dict(width=width,right_padding_half=padding,shape=current[:2],
                original_intervals=expected_i,margin=expected_i-2,shared_interval=shared_unit,
                states=records,extra_repair=alternate,repair_original_units=sorted(data[3][exit]&other_ids),
                optimum_extra_links_from_C0=2,minimum_further_links_after_collision=1)


def stacked(width,q):
    current,_=sealed(width);selected=set();matching=[]
    for i in range(q):
        move=lambda v:(v[0]-4+i*(width+4),v[1])
        selected|={move(v) for v in current[2]}
        matching += [tuple(map(move,e)) for e in current[3]]
    return q*(width+2)+2*(q-1),22,selected,matching


def check_stack(width,q,totals):
    current=stacked(width,q);bands=whole_bands(current)
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    first=[];both=[];repair=[];lower={}
    for i in range(q):
        move=lambda v:(v[0]-4+i*(width+4),v[1])
        first.append(tuple(map(move,((5,5),(5,6)))))
        both.extend(tuple(map(move,e)) for e in [((5,7),(5,8)),((5,15),(5,14))])
        repair.append(tuple(map(move,((width+4,15),(width+4,14)))))
        lower[move((width+4,5))]=2*i;lower[move((width+4,15))]=2*i+1
    data,meta,old,old_model,_,_=model_at(current,bands,first)
    legal_links={frozenset(link) for link in data[2]}
    assert all(frozenset(link) in legal_links for link in first+both+repair)
    _,_,new,new_model,_,_=model_at(current,bands,first+both)
    expected=q*(7*width-22)+20*(q-1)
    assert (old['alpha'],old['beta'],old['paid'],old['defect'],old['spare'])==(2*q,0,0,2*q,expected)
    assert (new['paid'],new['defect'],new['spare'])==(q,q,expected-q)
    assert old['margin']==new['margin']==expected-2*q
    result=verify(2*q,stable_incidence(old_model,lower),stable_incidence(new_model,lower),totals)
    assert result['gain']==q and len(result['clusters'])==q
    assert all(row['old_deficient']==2 and row['old_unused']==1 for row in result['clusters'])
    _,_,after,after_model,_,_=model_at(current,bands,first+both+repair)
    assert (after['paid'],after['defect'],after['spare'])==(2*q,0,expected-2*q)
    solved=residual_solve(data,new_model)
    assert (solved['value'],solved['cost'],solved['deficit'])==(2*q,q,0)
    totals['actual_whole_support_collision_stacks']+=1
    totals['stack_colliding_clusters']+=q
    return dict(width=width,copies=q,initial_defect=2*q,simultaneous_gain=q,
                residual_defect=q,distinct_collision_units=q,extra_repair_links=q,
                margin=expected-2*q)


def write_fixture(path):
    current,bands=sealed(8)
    _,layers=frozen_certificate(current)
    path.write_text(json.dumps(dict(shape=current[:2],selected=sorted(current[2]),matching=current[3],
        freezing_layers=[[dict(endpoint=e['endpoint'],kept_neighbors=e['kept_neighbors']) for e in layer]
                         for layer in layers],packet_rows=[4,13],packet_columns=[0,21]),indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--write-fixture',type=Path)
    args=parser.parse_args();totals=Counter();records=[]
    for width in range(8,41,2):
        current,bands=sealed(width)
        for padding in (0,1,3,8):
            columns=22+2*padding
            wider=(current[0],max(current[1],columns),current[2],current[3])
            extended=[[((r,c),(r+1,c)) for c in range(columns)] for r in range(4,width+5,2)]
            records.append(check(wider,extended,lambda v:v,width,padding,totals))
    for width in (8,14):
        current,bands=sealed(width)
        for symmetry in itertools.product((False,True),repeat=3):
            shape,t,m=transformed(*current,*symmetry);move=image_map(*current[:2],symmetry)
            carried=[[tuple(map(move,col)) for col in band] for band in bands]
            records.append(check((*shape,t,m),carried,move,width,0,totals))
    stacks=[check_stack(width,q,totals) for width in (8,12) for q in range(1,13)]
    if args.write_fixture:write_fixture(args.write_fixture)
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),boards=records,stacks=stacks,
        scope='Actual frozen all-even-height PP-seal family: whole-support d2S1 collision; '
              'two separately successful disjoint mixed continuations share one original interval. '
              'Arbitrary stacks and blank right padding; alternative mixed exit repairs with '
              'distinct original resources. Written all-parameter proof; no target counterexample '
              'or matching uniqueness claim.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
