"""Solver-free frozen beta-body fork and exact reserved-resource gain.

FROZEN_BETA_SUPPORT_FORK_AND_RESERVED_RESOURCE_GAIN.md gives the base argument,
all-copy proof and exact distinction from unrestricted compensation.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_even_bridge_support_completion import endpoints_of
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_support_tree_reroot import model_at
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_whole_support_fork_normal_form import (
    whole_support_data,ordinary_flow,optimize_by_forks,brute,contract,
)

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')

FIXTURE=Path(__file__).parent/'fixtures/frozen_beta_support_fork.json'
FORK=[((5,5),(5,6)),((12,5),(12,6))]
A=((3,2),(5,5));C=((12,2),(12,5));B=((5,6),(12,6))


def fixture():
    j=json.loads(FIXTURE.read_text())
    current=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
    layers=[[tuple(e['endpoint']) for e in layer] for layer in j['freezing_layers']]
    return current,layers


def restrict(data,selected_owners,resources):
    kinds,pairs,links,support,_=data
    owners,_,_,_=owner_data(kinds,pairs)
    kept=[pair for o,pair in enumerate(pairs) if o in selected_owners]
    free={v for pair in kept for v in pair}
    return ({v:kinds[v] for v in free},kept,[e for e in links if set(e)<=free],
        {i:support[owners[pair[0]]]&resources for i,pair in enumerate(kept)},set(resources))


def check(current,bands,move,padding,totals):
    direct_check(*current);assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,witness=whole_support_data(current,bands)
    owners,alphas,betas,mixed=owner_data(*data[:2])
    a,c,b=owners[move(A[0])],owners[move(C[0])],owners[move(B[0])]
    assert a!=c and a in alphas and c in alphas and b in betas
    assert set(data[1][a])==set(map(move,A))
    assert set(data[1][c])==set(map(move,C))
    assert set(data[1][b])==set(map(move,B))
    j=meta['owner'][4,7]
    assert meta['intervals'][j]==dict(band=4,first=7,last=7)
    assert j in data[4] and {o for o,w in data[3].items() if j in w}=={b}
    assert witness[b,j]==(4,6)
    assert len(current[2])==21 and len(current[3])==33
    assert (len(alphas),len(betas),len(mixed))==(3,2,1)
    assert sum(r['kind']==['cycle'] for r in meta['original']['components'])==8
    assert len(data[4])==43+16*padding
    assert len(meta['intervals'])==59+16*padding and len(meta['boundary'])==16
    # The physical board is retained: only permitted sources/resources/owners
    # in this certificate interface are restricted, not the occupied grid.
    reserved=restrict(data,{a,c,b}|mixed,{j})
    ordinary=ordinary_flow(*reserved);full=optimize_by_forks(*reserved)
    assert (ordinary['value'],ordinary['cost'])==(1,1)
    assert (full['value'],full['cost'])==(2,2) and len(full['forks'])==1
    expected,count=brute(*reserved)
    assert expected==(2,2)
    totals['reserved_terminal_matchings']+=count
    fork=list(map(lambda e:tuple(map(move,e)),FORK))
    assert all(e in data[2] for e in fork)
    _,_,after,model,_,_=model_at(current,bands,fork)
    assert (after['alpha'],after['beta'])==(2,1)
    merged=next(o for o,pair in enumerate(model['alphas']) if set(pair)==set(map(move,((3,2),(12,2)))))
    assert model['incidence'][j]=={merged}
    # Prepaying the first beta link makes its whole support a mixed gate;
    # the second arm is now an ordinary interval stem in the contracted model.
    virtual=contract(reserved,[fork[0]])
    assert len(owner_data(*virtual[:2])[2])==0
    continuation=ordinary_flow(*virtual)
    assert (continuation['value'],continuation['cost'])==(1,1)
    unrestricted=optimize_by_forks(*data);old=ordinary_flow(*data)
    assert (unrestricted['value'],unrestricted['cost'])==(3,0 if padding else 1)
    assert (old['value'],old['cost'])==(unrestricted['value'],unrestricted['cost'])
    if not padding:
        expected,count=brute(*data)
        assert expected==(3,1);totals['unrestricted_terminal_matchings']+=count
    totals['frozen_physical_controls']+=1
    totals['strict_reserved_resource_gains']+=1
    totals['actual_fork_occurrences']+=1
    return dict(shape=current[:2],right_padding_half=padding,intervals=len(data[4]),
        margin=len(data[4])+len(betas)-len(alphas),beta_body_unit=j,
        reserved_ordinary_value=1,reserved_fork_value=2,reserved_fork_links=fork,
        full_value=unrestricted['value'],full_min_links=unrestricted['cost'],
        full_ordinary_value=old['value'],full_ordinary_min_links=old['cost'])


def stacked(q):
    base,_=fixture();selected=set();matching=[]
    for i in range(q):
        move=lambda v:(v[0]+16*i,v[1])
        selected|={move(v) for v in base[2]}
        matching += [tuple(map(move,e)) for e in base[3]]
    return 16*q,14,selected,matching


def check_stack(q,totals):
    current=stacked(q);bands=whole_bands(current)
    direct_check(*current);assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,witness=whole_support_data(current,bands)
    owners,alphas,betas,mixed=owner_data(*data[:2]);selected=set(mixed);units=set();links=[]
    for i in range(q):
        move=lambda v:(v[0]+16*i,v[1])
        a,c,b=owners[move(A[0])],owners[move(C[0])],owners[move(B[0])]
        selected|={a,c,b};j=meta['owner'][4+8*i,7];units.add(j)
        assert {o for o,choices in data[3].items() if j in choices}=={b}
        links += [tuple(map(move,e)) for e in FORK]
    assert len(units)==q and len({v for e in links for v in e})==4*q
    assert (len(alphas),len(betas),len(mixed),len(data[4]))==(3*q,2*q,q,43*q)
    reserved=restrict(data,selected,units)
    ordinary=ordinary_flow(*reserved)
    assert (ordinary['value'],ordinary['cost'])==(q,q)
    if q<=6:
        full=optimize_by_forks(*reserved)
        assert (full['value'],full['cost'])==(2*q,2*q)
        totals['small_stack_fork_optimizer_controls']+=1
    _,_,after,model,_,_=model_at(current,bands,links)
    assert (after['alpha'],after['beta'])==(2*q,q)
    paid={}
    for i in range(q):
        move=lambda v:(v[0]+16*i,v[1])
        a=next(o for o,pair in enumerate(model['alphas']) if set(pair)==set(map(move,((3,2),(12,2)))))
        j=meta['owner'][4+8*i,7]
        assert model['incidence'][j]=={a};paid[a]=j
    assert len(paid)==len(set(paid.values()))==q
    # Whole-board gap incidence has no cross-copy edges, hence ordinary
    # full-pool optima add; this explicit solver confirms the all-q proof.
    full=ordinary_flow(*data)
    assert (full['value'],full['cost'])==(3*q,q)
    assert len(data[4])+len(betas)-len(alphas)==42*q
    totals['frozen_stacks']+=1;totals['stack_actual_forks']+=q
    return dict(copies=q,selected=21*q,matching=33*q,alpha=3*q,beta=2*q,mixed=q,
        available_units=43*q,margin=42*q,reserved_ordinary=q,reserved_fork=2*q,
        reserved_fork_links=2*q,full_value=3*q,full_min_links=q)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();base,layers=fixture()
    rank_witnesses=check_rank_certificate(base,layers)
    controls=[]
    for symmetry in itertools.product((False,True),repeat=3):
        shape,t,m=transformed(*base,*symmetry);move=image_map(*base[:2],symmetry)
        bands=[[tuple(map(move,c)) for c in band] for band in whole_bands(base)]
        check_rank_certificate((*shape,t,m),[list(map(move,layer)) for layer in layers])
        controls.append(check((*shape,t,m),bands,move,0,totals))
    for p in range(1,13):
        wider=(16,14+2*p,base[2],base[3])
        controls.append(check(wider,whole_bands(wider),lambda v:v,p,totals))
    stacks=[check_stack(q,totals) for q in range(1,17)]
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),controls=controls,
        stacks=stacks,strict_rank_witnesses=rank_witnesses,
        scope='Actual fully frozen66-endpoint beta fork, with one whole beta plus one '
              'distinct original interval. Strict reserved-source/resource gain2vs1; '
              'unrestricted whole-support optimum unchanged3with1link, blank padding '
              'releases a marked exit and lowers unrestricted cost to0. '
              'All-q physical stack proof written; finite controls do not prove a universal bound.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
