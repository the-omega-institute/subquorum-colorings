"""Solver-free checks of the all-length interior PP cap construction.

General proofs, including all-length feasibility and freezing, are in
docs/INTERIOR_SUPPORT_TREE_CAPS_AND_EXTERNAL_WITNESSES.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_boundary_sealed_gap_obstruction import stack
from check_compensation_flow_normal_form import solve
from check_even_bridge_support_completion import endpoints_of
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_support_tree_reroot import A, B, fixture, model_at
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_tree_beta_compensation import verify
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def capped(d):
    assert isinstance(d, int) and d >= 1
    base, layers = fixture()
    c = 17+2*d
    tail = {(r if col % 2 else r+1, col)
            for r in (6, 8) for col in range(17, c)}
    anchors = {(5,c), (6,c+1), (8,c+1), (10,c)}
    current = (12, c+3, base[2] | tail | anchors,
               base[3]+[((6,c),(7,c)), ((8,c),(9,c))])
    return current, layers+[[(6,c),(9,c)], [(7,c),(8,c)]]


def check(current, bands, move, d, extra, totals):
    direct_check(*current)
    assert frozen_certificate(current)[0] == endpoints_of(current)
    data, meta, rep, model, betas, witness = model_at(current, bands)
    ids = {frozenset(pair): a for a, pair in enumerate(model['alphas'])}
    a, b = ids[frozenset(map(move,A))], ids[frozenset(map(move,B))]
    owned = {j: users for j, users in model['incidence'].items() if users}
    assert len(owned) == 1
    j = next(iter(owned))
    assert owned[j] == {a,b} and list(betas.values()) == [{b}]
    expected = 50+8*d+6*extra
    assert (rep['alpha'],rep['beta'],rep['paid'],rep['defect'],rep['spare'],rep['margin']) == (
        2,1,1,1,expected,expected)
    assert len(model['incidence']) == expected+1
    assert len(meta['intervals']) == expected+13 and len(meta['boundary']) == 12
    assert len(current[2]) == 33+4*d and len(current[3]) == 25
    assert sum(p['kind'] == ['cycle'] for p in meta['original']['components']) == 5
    result = verify(2, model['incidence'], betas, totals, {b:j}, exhaustive=True)
    assert result['paid'] == 2 and result['mu'] == result['changes'] == 1
    assert result['intervals'] == {a:j}
    assert verify(2,model['incidence'],betas,totals,{a:j})['changes'] == 0
    link = witness[b,result['betas'][b]]
    assert link == (move((5,10)),move((5,11)))
    _,_,after,after_model,_,_ = model_at(current,bands,[link])
    assert (after['alpha'],after['beta'],after['paid'],after['defect'],after['spare']) == (
        1,0,1,0,expected)
    surviving = next(i for i,pair in enumerate(after_model['alphas']) if set(pair)==set(map(move,A)))
    assert surviving in after_model['incidence'][j]
    mixed_link = (move((8,8)),move((8,9)))
    assert mixed_link in data[2]
    _,_,other,other_model,_,_ = model_at(current,bands,[mixed_link])
    new_a = next(i for i,pair in enumerate(other_model['alphas'])
                 if set(pair)=={move((5,8)),move((8,10))})
    new_b = next(i for i,pair in enumerate(other_model['alphas']) if set(pair)==set(map(move,B)))
    choices = {r for r,users in other_model['incidence'].items() if new_a in users and r!=j}
    assert new_b in other_model['incidence'][j] and choices
    assert choices <= data[3][move((8,10))]
    assert (other['alpha'],other['beta'],other['paid'],other['defect'],other['spare']) == (
        2,1,2,0,expected-1)
    full = solve(*data)
    assert (full['value'],full['cost'],full['deficit']) == (2,1,0)
    # Each old B exit stops at the interior PP cap, with NO BB along it.
    # Carried bands may reverse their column order, so check physical cells.
    selected, endpoints = current[2], endpoints_of(current)
    for r in (6,8):
        for col in range(15,17+2*d):
            cells = set(map(move,((r,col),(r+1,col))))
            assert len(cells & selected)==1 and not cells & endpoints
        assert set(map(move,((r,17+2*d),(r+1,17+2*d)))) <= endpoints
    totals['interior_cap_physical_controls'] += 1
    totals['stable_right_padding_controls'] += extra > 0
    return dict(d=d,extra_columns=extra,shape=current[:2],selected=len(selected),
                matching=len(current[3]),intervals=len(model['incidence']),
                alpha=2,beta=1,tree_defect=1,shared_interval=j,margin=expected,
                direct_links=1,old_assignment_changes=1,mixed_links=1,
                mixed_additional_intervals=sorted(choices))


def check_stack(d,q,totals):
    base,_ = capped(d)
    current = stack(base,q)
    direct_check(*current)
    assert frozen_certificate(current)[0] == endpoints_of(current)
    data,_,rep,model,betas,witness = model_at(current,whole_bands(current))
    ids = {frozenset(pair):a for a,pair in enumerate(model['alphas'])}
    baseline = {}
    for i in range(q):
        move = lambda v:(v[0]+12*i,v[1])
        a,b = ids[frozenset(map(move,A))],ids[frozenset(map(move,B))]
        units = [j for j,users in model['incidence'].items() if users=={a,b}]
        assert len(units)==1
        baseline[b]=units[0]
    result = verify(2*q,model['incidence'],betas,totals,baseline)
    expected = (50+8*d)*q
    assert (rep['alpha'],rep['beta'],rep['defect'],rep['spare'],rep['margin']) == (
        2*q,q,q,expected,expected)
    assert len(model['incidence'])==(51+8*d)*q
    assert result['paid']==2*q and result['t']==result['mu']==result['changes']==q
    links = [witness[a,b] for a,b in result['betas'].items()]
    _,_,after,after_model,_,_ = model_at(current,whole_bands(current),links)
    assert (after['alpha'],after['beta'],after['paid'],after['defect'],after['spare']) == (
        q,0,q,0,expected)
    assert len({v for link in links for v in link})==2*q
    surviving={frozenset(pair):a for a,pair in enumerate(after_model['alphas'])}
    assert all(surviving[frozenset(model['alphas'][a])] in after_model['incidence'][j]
               for a,j in result['intervals'].items())
    totals['interior_cap_stack_controls']+=1
    return dict(d=d,copies=q,deficient_trees=q,beta_matching=q,changes=q,margin=expected)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    totals=Counter(); controls=[]
    for d in range(1,17):
        base,layers=capped(d)
        check_rank_certificate(base,layers)
        controls.append(check(base,whole_bands(base),lambda v:v,d,0,totals))
        for extra in (2,4,12,32):
            wider=(base[0],base[1]+extra,base[2],base[3])
            controls.append(check(wider,whole_bands(wider),lambda v:v,d,extra,totals))
    images=[]
    for d in (1,4):
        base,layers=capped(d)
        for symmetry in itertools.product((False,True),repeat=3):
            shape,selected,matching=transformed(*base,*symmetry)
            current=(*shape,selected,matching)
            move=image_map(*base[:2],symmetry)
            bands=[[tuple(map(move,col)) for col in band] for band in whole_bands(base)]
            check_rank_certificate(current,[list(map(move,layer)) for layer in layers])
            check(current,bands,move,d,0,totals)
            images.append(dict(d=d,symmetry=symmetry))
    stacks=[check_stack(d,q,totals) for d in (1,2,4) for q in range(1,13)]
    receipt=dict(status='PASS',totals=dict(totals),controls=controls,images=images,stacks=stacks,
        scope='Written all-d/all-q frozen interior cap and right-padding proof; finite controls '
              'and independent allocation checks here. Genuine interval-only deficient tree; '
              'direct beta repair exists, so this is NOT a beta Hall failure or grid-bound counterexample.')
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':
    main()
