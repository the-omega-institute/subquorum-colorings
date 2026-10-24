"""A safe BP-to-TP closure gives sharp physical beta Hall deficiencies.

General proofs are in BETA_CLOSING_AND_SHARP_MIXED_DEFECT.md. This checker
retains old interval identities and verifies actual simultaneous mixed repair.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_boundary_sealed_gap_obstruction import stack
from check_compensation_flow_normal_form import solve
from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_support_tree_reroot import A,B,model_at
from check_interior_support_tree_caps import capped
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_tree_external_witness_bound import physical

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def closed(d):
    current,layers=capped(d)
    site=(2,12); tip=(3,12)
    assert site not in current[2] | endpoints_of(current)
    assert set(neighbors(site)) & (current[2] | endpoints_of(current))=={tip}
    return (*current[:2],current[2]|{site},current[3]),layers


def check(current,bands,move,d,extra,totals):
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,rep,model,betas,_=model_at(current,bands)
    assert (rep['alpha'],rep['beta'],rep['paid'],rep['defect'])==(2,0,1,1)
    assert not betas
    u=50+8*d+6*extra
    assert rep['spare']==u and rep['margin']==u-1
    assert len(model['incidence'])==u+1
    assert len(current[2])==34+4*d and len(current[3])==25
    alpha_ids={frozenset(pair):a for a,pair in enumerate(model['alphas'])}
    a,b=alpha_ids[frozenset(map(move,A))],alpha_ids[frozenset(map(move,B))]
    owned={j:users for j,users in model['incidence'].items() if users}
    assert len(owned)==1
    j=next(iter(owned));assert owned[j]=={a,b}
    for bp in (move((8,7)),move((8,13))):
        assert data[0][bp]=='BP'
    details=[]
    for link,exit,port in [(((5,10),(5,11)),(3,12),(1,10)),
                           (((8,8),(8,9)),(8,10),(4,11))]:
        link=tuple(map(move,link));exit=move(exit)
        assert link in data[2]
        # Identify resources by their physical cells, including carried bands.
        desired=set(map(move,((2*port[0],port[1]),(2*port[0]+1,port[1]))))
        locations={frozenset(col):(bi,ci) for bi,band in enumerate(bands) for ci,col in enumerate(band)}
        bi,ci=locations[frozenset(desired)]
        k=meta['owner'][bi,ci]
        assert k!=j and k in data[3][exit] and k not in meta['boundary']
        # The original source tree has no ownership of k; the mixed transfer
        # grows its support. The interval itself is old, not newly generated.
        assert not model['incidence'][k]
        _,_,after,after_model,_,_=model_at(current,bands,[link])
        assert (after['alpha'],after['beta'],after['paid'],after['defect'],after['spare'],after['margin'])==(
            2,0,2,0,u-1,u-1)
        new=next(i for i,pair in enumerate(after_model['alphas']) if exit in pair)
        other=next(i for i in range(2) if i!=new)
        assert new in after_model['incidence'][k] and other in after_model['incidence'][j]
        details.append(dict(link=link,exit=exit,original_interval=k))
    full=solve(*data)
    assert (full['value'],full['cost'],full['deficit'])==(2,1,0)
    token=physical(current,bands,totals)
    assert (token['trees'],token['mu'],token['joint_defect'],token['distinct_mixed_witnesses'],
            token['distinct_mark_witnesses'],token['zero_witness_bound'])==(1,0,1,2,0,1)
    totals['sharp_physical_beta_hall_boards']+=1
    return dict(d=d,extra_columns=extra,shape=current[:2],alpha=2,beta=0,
                trees=1,mu=0,beta_hall_defect=1,distinct_mixed_witnesses=2,
                interval=j,unused=u,margin=u-1,minimum_full_links=1,repairs=details)


def stacks(d,q,totals,unclosed=0):
    base,layers=closed(d)
    current=stack(base,q+unclosed)
    if unclosed:
        remove={(2+12*i,12) for i in range(q,q+unclosed)}
        current=(*current[:2],current[2]-remove,current[3])
    bands=whole_bands(current)
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,rep,model,betas,_=model_at(current,bands)
    assert (rep['alpha'],rep['beta'],rep['defect'])==(2*(q+unclosed),unclosed,q+unclosed)
    token=physical(current,bands,totals)
    assert token['mu']==unclosed and token['joint_defect']==q
    assert token['distinct_mixed_witnesses']==2*(q+unclosed) and token['distinct_mark_witnesses']==0
    links=[];payments={};ids={frozenset(pair):a for a,pair in enumerate(model['alphas'])}
    for i in range(q+unclosed):
        move=lambda v:(v[0]+12*i,v[1])
        links.append((move((5,10)),move((5,11))))
        a,b=ids[frozenset(map(move,A))],ids[frozenset(map(move,B))]
        j=next(j for j,users in model['incidence'].items() if users=={a,b})
        payments[frozenset(map(move,A))]=j
        if i<q:
            payments[frozenset((move((3,12)),move((8,14))))]=meta['owner'][1+6*i,10]
    _,_,after,after_model,_,_=model_at(current,bands,links)
    assert (after['alpha'],after['beta'],after['paid'],after['defect'])==(2*q+unclosed,0,2*q+unclosed,0)
    surviving={frozenset(pair):a for a,pair in enumerate(after_model['alphas'])}
    assert len(set(payments.values()))==len(payments)
    assert all(surviving[pair] in after_model['incidence'][j] for pair,j in payments.items())
    full=solve(*data)
    assert (full['value'],full['cost'],full['deficit'])==(2*(q+unclosed),q+unclosed,0)
    expected=(49+8*d)*q+(50+8*d)*unclosed
    assert rep['margin']==after['margin']==expected
    totals['sharp_defect_stack_controls']+=1
    totals['positive_beta_and_hall_defect_controls']+=unclosed>0
    return dict(d=d,closed=q,unclosed=unclosed,trees=q+unclosed,beta=unclosed,
                mu=unclosed,joint_defect=q,full_links=q+unclosed,margin=expected)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();records=[]
    for d in range(1,17):
        current,layers=closed(d)
        check_rank_certificate(current,layers)
        # The BP closure preserves the entire BB--TT forest, not just its size.
        before=model_at(capped(d)[0],whole_bands(current))
        after=model_at(current,whole_bands(current))
        assert before[1]['intervals']==after[1]['intervals']
        assert before[1]['boundary']==after[1]['boundary']
        assert before[3]['incidence']==after[3]['incidence']
        for extra in (0,2,8,24):
            wider=(current[0],current[1]+extra,current[2],current[3])
            records.append(check(wider,whole_bands(wider),lambda v:v,d,extra,totals))
    current,layers=closed(1)
    for symmetry in itertools.product((False,True),repeat=3):
        shape,selected,matching=transformed(*current,*symmetry)
        move=image_map(*current[:2],symmetry)
        image=(*shape,selected,matching)
        bands=[[tuple(map(move,col)) for col in band] for band in whole_bands(current)]
        check_rank_certificate(image,[list(map(move,layer)) for layer in layers])
        records.append(check(image,bands,move,1,0,totals))
    copies=[stacks(d,q,totals) for d in (1,3) for q in range(1,13)]
    copies += [stacks(1,q,totals,s) for q,s in itertools.product((1,2,4),(1,2,3))]
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),boards=records,stacks=copies,
        scope='Written all-d/all-q feasible frozen construction has actual whole-support beta Hall '
              'defect q, sharp two-mixed-witness bound in closed stacks, stable right padding. '
              'Full mixed compensation needs exactly one link per copy and uses distinct ORIGINAL '
              'intervals. Positive-beta controls have betas confined to their own unclosed components. '
              'No target inequality counterexample or forced shared-beta competition is claimed.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
