"""Two-state recognition and physical compiler for uniform zero-capacity pivots.

The all-state proof is docs/UNIFORM_ZERO_CAPACITY_OPENINGS.md. Exhaustive
subsets below independently validate recognition, the support compiler, and
joint fees against primitive packing. The optimizer itself uses two snapshots
and one min-cost fork flow, not subset enumeration.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random
from unittest.mock import patch
import check_protected_linear_corridors as corridor_impl

from check_canonical_band_coarsening import forests, tile_refinement, random_board
from check_compensation_flow_normal_form import owner_data
from check_degree_changing_bent_completions import compile_model
from check_P_free_pivot_interface import regions, family as loss_family
from check_protected_linear_corridors import apply, corridor_flow, frozen_board, subsets
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize
from check_frozen_coordinated_pivots import family as gain_family

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def tile_cells(tile):
    r,c=tile
    return {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}


def snapshot(cur,bits):
    regs=regions(cur,bits);data,closed,_=compile_model(cur,regs)
    fine=forests(cur,tile_refinement(*cur[:2],regs));coarse=forests(cur,regs)
    anchors=sorted(tuple(sorted(cc)) for cap,cc in fine.values() if cap)
    ids={a:i for i,a in enumerate(anchors)}
    at={v:ids[a] for a in anchors for v in a};mapping={};shapes={}
    for j,(cap,cc) in coarse.items():
        if cap:
            children={at[v] for v in cc if v in at}
            assert len(children)==1
            uid=children.pop();mapping[j]=uid;shapes[uid]=cc
    assert len(mapping)==len(anchors)==len(set(mapping.values()))
    normalized=(*data[:3],{o:{mapping[j] for j in W} for o,W in data[3].items()},set(ids.values()))
    axes={i:bits[min(r for r,c in a)//2*2,min(c for r,c in a)//2*2] for i,a in enumerate(anchors)}
    return dict(data=normalized,closed=closed,regs=regs,anchors=anchors,axes=axes,
                mapping=mapping,shapes=shapes)


def compile_openings(cur,bits,gates):
    """Recognize using just the two extreme states; compile if lossless."""
    assert len(gates)==len(set(gates))
    P={v for e in cur[3] for v in e}
    for g in gates:
        assert bits[g] and not tile_cells(g)&P and len(tile_cells(g)&cur[2])==2
    fullbits=dict(bits)
    for g in gates:fullbits[g]=False
    old=snapshot(cur,bits);full=snapshot(cur,fullbits)
    assert old['anchors']==full['anchors'] and old['axes']==full['axes']
    assert old['data'][:2]==full['data'][:2] and set(old['data'][2])==set(full['data'][2])
    assert [(x['body'],x['ends']) for x in old['closed']]==[(x['body'],x['ends']) for x in full['closed']]
    losses=[(o,j) for o,W in old['data'][3].items() for j in W-full['data'][3][o]]
    assert all(old['axes'][j] for o,j in losses)
    result=dict(accepted=not losses,old=old,full=full,losses=losses)
    if losses:return result
    body_owner={v:o for o,x in enumerate(full['closed']) for v in x['body']}
    corridors=[];b=0;placed=[];resources=[]
    for region in full['regs']:
        for band in region['bands']:
            if not region['vertical']:
                row=min(r for r,c in band[0]);startcol=min(c for r,c in band[0])
                def boundary(i):
                    if not 0<=i<len(band):return None
                    owners={body_owner[v] for v in band[i] if v in body_owner}
                    assert len(owners)<=1
                    return next(iter(owners),None)
                i=0
                while i<len(band):
                    if set(band[i])&P:i+=1;continue
                    first=i
                    while i<len(band) and not set(band[i])&P:i+=1
                    after=i
                    units=[uid for j,uid in full['mapping'].items() if j[0]==b and first<=j[1]<=j[2]<after]
                    units.sort(key=lambda u:min(c for r,c in full['anchors'][u]))
                    gg=[]
                    for gi,(r,c) in enumerate(gates):
                        if r==row and startcol+first<=c and c+1<startcol+after:
                            slot=sum(min(y for x,y in full['anchors'][u])<c for u in units)
                            gg.append((gi,slot));placed.append(gi)
                    if units or gg:
                        corridors.append(dict(left=boundary(first-1),right=boundary(after),units=units,gates=gg))
                        resources+=units
            b+=1
    horizontal={u for u,v in full['axes'].items() if not v}
    assert set(resources)==horizontal and len(resources)==len(horizontal)
    assert set(placed)==set(range(len(gates))) and len(placed)==len(gates)
    base=(*old['data'][:3],{o:W-horizontal for o,W in old['data'][3].items()},old['data'][4])
    assert apply(base,corridors,set())[3]==old['data'][3]
    assert apply(base,corridors,set(range(len(gates))))[3]==full['data'][3]
    result.update(base=base,corridors=corridors,horizontal=horizontal)
    return result


def solve_openings(cur,bits,gates,weights,required=frozenset()):
    """Polynomial solving API: two physical states and one costed flow.

    Primitive-pack and gate-subset enumeration belong only to the audit.
    Rejection returns exact original-owner/anchor loss witnesses.
    """
    direct_check(*cur)
    assert set(weights)==set(range(len(gates)))
    assert all(isinstance(w,int) and w>=0 for w in weights.values())
    compiled=compile_openings(cur,bits,gates)
    if not compiled['accepted']:
        return dict(accepted=False,losses=[dict(owner=o,anchor=compiled['old']['anchors'][j])
                                          for o,j in compiled['losses']])
    result=corridor_flow(compiled['base'],compiled['corridors'],weights,required,independent=False)
    return dict(accepted=True,**result,opened_tiles=[gates[i] for i in result['opened']])


def audit(cur,bits,gates,counts,exhaustive=True):
    direct_check(*cur);compiled=compile_openings(cur,bits,gates);n=len(gates);allgates=set(range(n))
    chosen=subsets(range(n)) if exhaustive else [frozenset(),frozenset(allgates),
        *[frozenset({i}) for i in allgates],*[frozenset(allgates-{i}) for i in allgates]]
    records={};changed_shapes=0;old=compiled['old'];H={u for u,v in old['axes'].items() if not v};V=old['data'][4]-H
    for F in chosen:
        changed=dict(bits)
        for i in F:changed[gates[i]]=False
        s=snapshot(cur,changed);data=s['data']
        assert s['anchors']==old['anchors'] and s['axes']==old['axes']
        assert data[:2]==old['data'][:2] and set(data[2])==set(old['data'][2])
        assert [(x['body'],x['ends']) for x in s['closed']]==[(x['body'],x['ends']) for x in old['closed']]
        for o,W in data[3].items():
            assert old['data'][3][o]&H<=W&H<=compiled['full']['data'][3][o]&H
            assert compiled['full']['data'][3][o]&V<=W&V<=old['data'][3][o]&V
        f=fork_flow(*data);p=optimize(*data)
        assert (f['value'],f['cost'])==(p['value'],p['cost'])
        records[F]=dict(data=data,value=f['value'],links=f['cost'])
        if compiled['accepted']:
            proxy=apply(compiled['base'],compiled['corridors'],F)
            assert proxy[3]==data[3] and proxy[4]==data[4]
            counts['complete_physical_support_compiler_states']+=1
        counts['physical_primitive_optimum_comparisons']+=1
        counts['states_with_changed_positive_forest_cells']+=s['shapes']!=old['shapes']
        changed_shapes+=s['shapes']!=old['shapes']
    if exhaustive:
        monotone=True
        for F,a in records.items():
            for i in allgates-F:
                W=records[F|{i}]['data'][3]
                good=all(S<=W[o] for o,S in a['data'][3].items())
                monotone=monotone and good
                for o,S in a['data'][3].items():
                    assert S&H<=W[o]&H and W[o]&V<=S&V
                counts['all_lattice_edge_support_checks']+=1
        assert compiled['accepted']==monotone
        counts['two_state_iff_all_subset_monotonicity_audits']+=1
    if compiled['accepted']:
        weights={i:(i%4)+1 for i in allgates}
        result=solve_openings(cur,bits,gates,weights)
        assert result['accepted']
        if exhaustive:
            expected=max(((r['value'],sum(weights[i] for i in F),r['links']) for F,r in records.items()),key=lambda t:(t[0],-t[1],-t[2]))
            assert (result['value'],result['fee'],result['links'])==expected
            counts['compiler_flow_vs_all_physical_gate_choices']+=1
        changed=dict(bits)
        for i in result['opened']:changed[gates[i]]=False
        physical=snapshot(cur,changed)['data'];p=optimize(*physical)
        assert (p['value'],p['cost'])==(result['value'],result['links'])
        counts['reconstructed_physical_operation_optima']+=1
        counts['accepted_two_state_audits']+=1
    else:
        result=None;counts['rejected_two_state_audits']+=1
    counts['boards']+=1
    return dict(accepted=compiled['accepted'],shape=list(cur[:2]),T=len(cur[2]),matching=len(cur[3]),
        raw=len(old['data'][4]),gates=gates,states=len(records),losses=len(compiled['losses']),
        corridor_count=len(compiled.get('corridors',[])),result=result,
        changed_forest_cell_states=changed_shapes,
        state_payments=[dict(opened=sorted(F),value=r['value'],links=r['links']) for F,r in records.items()] if n<=5 else None,
        old_value=records[frozenset()]['value'],full_value=records[frozenset(allgates)]['value'])


def balanced_frozen():
    cur,bits,ranks,left,right,q=frozen_board(2,2)
    R,C,T,M=cur;newC=C+8
    T=T|{(2,C+4),(2,C+5)};cur=(R,newC,T,M)
    bb={(r,c):bits.get((r,c),False) for r in range(0,R,2) for c in range(0,newC,2)}
    for r in (0,2,4):bb[r,C+4]=True
    return cur,bb,ranks,left+right+[(2,C+4)]


def scalar_guard_trap():
    cur,bits,ranks=loss_family(0);R,C,T,M=cur
    left=(C,R,{(c,r) for r,c in T},[tuple((c,r) for r,c in e) for e in M])
    lb={(c,r):not v for (r,c),v in bits.items()};lr=[[(c,r) for r,c in layer] for layer in ranks]
    right,rb,rr,_=gain_family(1);shift=lambda p:(p[0],p[1]+18)
    cur=(28,48,left[2]|set(map(shift,right[2])),left[3]+[tuple(map(shift,e)) for e in right[3]])
    bb={(r,c):False for r in range(0,28,2) for c in range(0,48,2)}
    bb.update(lb);bb.update({(r,c+18):v for (r,c),v in rb.items()})
    for r in range(0,28,2):bb[r,16]=True
    ranks=[a+[shift(v) for v in b] for a,b in zip(lr,rr)]
    return cur,bb,ranks,[(16,2),(2,34)]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();counts=Counter();examples={};rng=random.Random(2026102603)
    for l,r in [(1,1),(2,3),(3,3),(7,1),(16,17)]:
        for one in (False,True):
            cur,bits,ranks,left,right,q=frozen_board(l,r,one)
            assert len(check_rank_certificate(cur,ranks))==140 and len(frozen_certificate(cur)[0])==140
            counts['strict_freeze_events']+=140
            row=audit(cur,bits,left+right,counts,exhaustive=l+r<=8)
            assert row['accepted'];examples[f'frozen_{l}_{r}_one{int(one)}']=row
    cur,bits,ranks,gates=balanced_frozen()
    assert len(check_rank_certificate(cur,ranks))==140 and len(frozen_certificate(cur)[0])==140
    counts['strict_freeze_events']+=140
    row=audit(cur,bits,gates,counts)
    assert row['accepted'] and row['changed_forest_cell_states']>0
    examples['frozen_balanced_TT_gate']=row
    cur,bits,ranks,gates=scalar_guard_trap()
    assert len(check_rank_certificate(cur,ranks))==140 and len(frozen_certificate(cur)[0])==140
    counts['strict_freeze_events']+=140
    row=audit(cur,bits,gates,counts)
    assert not row['accepted'] and [r['value'] for r in row['state_payments']]==[3,2,4,3]
    assert row['old_value']==row['full_value'] and row['losses']==10
    examples['frozen_scalar_guard_trap']=row
    counts['scalar_payment_guard_counterexamples']+=1
    # Fully frozen V->H support-loss family: same formal gate hypotheses,
    # rejected precisely by the final support inclusion test.
    cur,bits,ranks=loss_family(0);R,C,T,M=cur
    cur=(C,R,{(c,r) for r,c in T},[tuple((c,r) for r,c in e) for e in M])
    bits={(c,r):not v for (r,c),v in bits.items()};gates=[(16,2)]
    ranks=[[(c,r) for r,c in layer] for layer in ranks]
    assert len(check_rank_certificate(cur,ranks))==70 and len(frozen_certificate(cur)[0])==70
    counts['strict_freeze_events']+=70
    row=audit(cur,bits,gates,counts)
    assert not row['accepted'] and (row['old_value'],row['full_value'],row['losses'])==(2,1,10)
    examples['frozen_loss_rejection']=row
    # The callable solver must not invoke the exponential independent
    # primitive or operation-subset checks used by this audit.
    with patch.object(corridor_impl,'constrained_optimum',side_effect=RuntimeError('enumeration in solver')), \
         patch.object(corridor_impl,'subsets',side_effect=RuntimeError('subset enumeration in solver')):
        c,b,_,g=balanced_frozen()
        solved=solve_openings(c,b,g,{i:(i%4)+1 for i in range(len(g))})
        assert solved['accepted'] and (solved['value'],solved['fee'],solved['links'])==(4,10,2)
        c,b,_,g=scalar_guard_trap()
        rejected=solve_openings(c,b,g,dict.fromkeys(range(len(g)),1))
        assert not rejected['accepted'] and len(rejected['losses'])==10
    counts['solver_API_without_enumeration_checks']+=2
    for index in range(180):
        R,C=rng.choice([(4,6),(6,6),(6,8)])
        cur=random_board(R,C,rng)
        cur=(R,C,{v for v in cur[2] if rng.random()<.8},[e for e in cur[3] if rng.random()<.6])
        P={v for e in cur[3] for v in e}
        candidates=[(r,c) for r in range(0,R,2) for c in range(0,C,2)
                    if not tile_cells((r,c))&P and len(tile_cells((r,c))&cur[2])==2]
        if not candidates:continue
        rng.shuffle(candidates);gates=candidates[:rng.randrange(1,min(5,len(candidates))+1)]
        bits={(r,c):bool(rng.randrange(2)) for r in range(0,R,2) for c in range(0,C,2)}
        for g in gates:bits[g]=True
        audit(cur,bits,gates,counts)
        counts['random_feasible_boards']+=1
        counts['non_BT_zero_capacity_gate_occurrences']+=sum(cur[2]&tile_cells(g) not in
            ({g,(g[0]+1,g[1]+1)},{(g[0],g[1]+1),(g[0]+1,g[1])}) for g in gates)
    report=dict(status='PASS',counts=dict(counts),examples=examples,
        scope='Common positive fine-anchor resource IDs; two-state iff all-subset support monotonicity on enumerated uniform V-to-H capacity-zero physical families; exact compiler and joint fee/link flow; actual frozen accepted balanced gate and rejected loss controls.',
        limits='Enumeration validates general written proofs. Uniform target direction, P-free zero-capacity gates and canonical bands required. Rejection means support-only contract fails, not numerical inequality failure or impossibility of destructive repair. No universal 5/6 or arbitrary mixed-target orientation theorem.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(counts),indent=2));print('PASS: uniform zero-capacity opening compiler')


if __name__=='__main__':main()
