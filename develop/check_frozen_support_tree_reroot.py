"""Solver-free verification of a frozen nonsingleton support tree and rerooting.

The SAT search discovers coordinates only. General stacking and exact-interface
arguments are in FROZEN_SUPPORT_TREE_AND_FORCED_REROOT.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_boundary_sealed_gap_obstruction import support_allocation, stack
from check_bt_corridor_ports import compile_model
from check_compensation_flow_normal_form import solve
from check_even_bridge_support_completion import endpoints_of
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_tree_beta_compensation import physical_control, verify
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed

if not __debug__:
    raise RuntimeError('Run without -O; validation requires assertions.')

FIXTURE=Path(__file__).parent/'fixtures/frozen_support_tree_reroot.json'
A=((5,8),(8,8))
B=((5,10),(8,14))
BETA=((3,12),(5,11))


def fixture():
    record=json.loads(FIXTURE.read_text())
    current=(*record['shape'],set(map(tuple,record['selected'])),
             [tuple(map(tuple,e)) for e in record['matching']])
    layers=[[tuple(v['endpoint']) for v in layer] for layer in record['freezing_layers']]
    return current,layers


def model_at(current,bands,fixed=()):
    data,meta=compile_model(current,bands,Counter())
    report,model=support_allocation(current,bands,data,meta,list(fixed),Counter(),return_model=True)
    kinds=data[0]
    betas=[pair for pair in model['reduced'] if all(kinds[v]=='BP' for v in pair)]
    aa={v:a for a,pair in enumerate(model['alphas']) for v in pair}
    bb={v:b for b,pair in enumerate(betas) for v in pair}
    incidence={b:set() for b in range(len(betas))}
    witness={}
    for tp,bp in data[2]:
        if tp in aa and bp in bb:
            a,b=aa[tp],bb[bp]
            incidence[b].add(a);witness[a,b]=(tp,bp)
    return data,meta,report,model,incidence,witness


def check(current,bands,move,totals):
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,report,model,betas,witness=model_at(current,bands)
    alpha_ids={frozenset(pair):a for a,pair in enumerate(model['alphas'])}
    a,b=alpha_ids[frozenset(map(move,A))],alpha_ids[frozenset(map(move,B))]
    assert (report['alpha'],report['beta'],report['paid'],report['defect'],report['margin'])==(2,1,1,1,44)
    owned={j:users for j,users in model['incidence'].items() if users}
    assert len(owned)==1
    j=next(iter(owned))
    assert owned[j]=={a,b} and list(betas.values())==[{b}]
    assert frozenset(map(move,BETA)) in map(frozenset,model['reduced'])
    baseline={b:j}
    result=verify(2,model['incidence'],betas,totals,baseline,exhaustive=True)
    assert result['changes']==result['mu']==1 and result['paid']==2
    assert result['intervals']=={a:j} and set(result['betas'])=={b}
    reverse=verify(2,model['incidence'],betas,totals,{a:j},exhaustive=True)
    assert reverse['changes']==0
    link=witness[b,result['betas'][b]]
    assert link==(move((5,10)),move((5,11)))
    _,_,after,after_model,_,_=model_at(current,bands,[link])
    new_a=next(i for i,pair in enumerate(after_model['alphas']) if set(pair)==set(map(move,A)))
    assert new_a in after_model['incidence'][j]
    assert (after['alpha'],after['beta'],after['paid'],after['defect'],after['margin'])==(1,0,1,0,44)
    # A wider one-link repair keeps the old B -> J payment, uses a NEW interval,
    # and leaves the beta unused. It is outside the direct beta-only theorem.
    mixed_link=(move((8,8)),move((8,9)))
    assert mixed_link in data[2]
    _,_,other,other_model,_,_=model_at(current,bands,[mixed_link])
    new_a=next(i for i,pair in enumerate(other_model['alphas'])
               if set(pair)=={move((5,8)),move((8,10))})
    new_b=next(i for i,pair in enumerate(other_model['alphas']) if set(pair)==set(map(move,B)))
    available=[r for r,users in other_model['incidence'].items() if new_a in users and r!=j]
    assert new_b in other_model['incidence'][j] and available
    new_interval=available[0]
    assert new_interval in data[3][move((8,10))]
    assert (other['alpha'],other['beta'],other['paid'],other['defect'],other['margin'])==(2,1,2,0,44)
    assert other['spare']==43 and after['spare']==44
    full=solve(*data)
    assert (full['value'],full['cost'],full['deficit'])==(2,1,0)
    totals['physical_forced_reroot_images']+=1
    totals['physical_mixed_alternative_images']+=1
    return dict(alpha=2,beta=1,interval_only_paid=1,deficient_tree_size=2,
        original_interval=j,baseline_owner=b,unpaid_root=a,
        direct_beta_neighbours={str(beta):sorted(users) for beta,users in betas.items()},
        joint_paid=2,minimum_beta_links=1,minimum_old_assignment_changes=1,
        beta_link=link,mixed_alternative_link=mixed_link,
        mixed_alternative_interval=new_interval,mixed_alternative_beta_consumption=0,
        full_terminal_minimum_links=1,margin=44)


def check_stack(base,count,totals):
    current=stack(base,count)
    bands=whole_bands(current)
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,report,model,betas,witness=model_at(current,bands)
    aa={frozenset(pair):a for a,pair in enumerate(model['alphas'])}
    baseline={}
    for index in range(count):
        move=lambda v:(v[0]+index*base[0],v[1])
        a,b=aa[frozenset(map(move,A))],aa[frozenset(map(move,B))]
        units=[j for j,users in model['incidence'].items() if users=={a,b}]
        assert len(units)==1
        baseline[b]=units[0]
    result=verify(2*count,model['incidence'],betas,totals,baseline)
    assert (report['alpha'],report['beta'],report['defect'],report['spare'],report['margin'])==(
        2*count,count,count,44*count,44*count)
    assert len(model['incidence'])==45*count
    assert result['t']==result['mu']==result['changes']==count
    assert result['paid']==2*count
    links=[witness[a,b] for a,b in result['betas'].items()]
    _,_,after,after_model,_,_=model_at(current,bands,links)
    assert (after['alpha'],after['beta'],after['paid'],after['defect'],after['margin'])==(
        count,0,count,0,44*count)
    assert len({v for link in links for v in link})==2*count
    surviving={frozenset(pair):a for a,pair in enumerate(after_model['alphas'])}
    for a,j in result['intervals'].items():
        assert surviving[frozenset(model['alphas'][a])] in after_model['incidence'][j]
    totals['separated_stack_controls']+=1
    totals['stack_forced_old_assignment_changes']+=count
    return dict(copies=count,alpha=2*count,beta=count,trees=count,tree_size=2,
                old_changes=count,extra_beta_links=count,margin=44*count)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    base,layers=fixture()
    witnesses=check_rank_certificate(base,layers)
    totals=Counter()
    result=check(base,whole_bands(base),lambda v:v,totals)
    images=[]
    for symmetry in itertools.product((False,True),repeat=3):
        shape,selected,matching=transformed(*base,*symmetry)
        move=image_map(*base[:2],symmetry)
        bands=[[tuple(map(move,column)) for column in band] for band in whole_bands(base)]
        check_rank_certificate((*shape,selected,matching),[list(map(move,layer)) for layer in layers])
        check((*shape,selected,matching),bands,move,totals)
        images.append(list(symmetry))
    stacks=[check_stack(base,count,totals) for count in range(1,17)]
    padding=[]
    for half_extra in range(1,17):
        wider=(base[0],base[1]+2*half_extra,base[2],base[3])
        data,meta,rep,model,betas,witness=model_at(wider,whole_bands(wider))
        assert frozen_certificate(wider)[0]==endpoints_of(wider)
        assert rep['alpha']==2 and rep['beta']==1 and rep['paid']==2 and rep['defect']==0
        assert rep['spare']==43+12*half_extra and rep['margin']==44+12*half_extra
        assert len(model['incidence'])==45+12*half_extra
        assert solve(*data)['cost']==0
        totals['right_padding_releases_defect_controls']+=1
        padding.append(dict(extra_columns=2*half_extra,intervals=len(model['incidence']),
                            deficit=0,minimum_links=0,margin=rep['margin']))
    # This independently exercises every C0 in the fixed physical skeleton.
    physical_control(base,whole_bands(base),totals,exhaustive=True)
    assert totals['frozen_fixed_c0_lift_checks']==1980
    assert totals['physical_nonsingleton_deficient_trees']==504
    assert totals['physical_positive_reroot_controls']>0
    searches=[]
    for filename in ['support-tree-search-12x18.json','support-tree-reroot-search-12x18.json',
                     'support-tree-competition-search-12x18.json','support-tree-competition-search-14x20.json']:
        raw=json.loads((Path('output')/filename).read_text())
        searches.append(dict(file=filename,shape=raw['shape'],status=raw['status'],
                             seconds=raw['seconds'],reason=raw['reason']))
    output=dict(status='PASS',totals=dict(totals),base=result,images=images,stacks=stacks,
        right_padding=padding,
        independent_strict_rank_witnesses=witnesses,search_receipts=searches,
        scope='Actual frozen nonsingleton whole-support deficient tree; direct-interface forced '
              'reroot relative to a specified maximum interval baseline. Wider mixed-route repair '
              'keeps that assignment by adding a new interval. All-q disjoint stacking is a written '
              'proof; general Hall expansion and grid bounds remain open. No matching uniqueness claim.')
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':
    main()
