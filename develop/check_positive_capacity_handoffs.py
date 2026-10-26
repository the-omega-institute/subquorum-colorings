"""Linear-snapshot recognition for uniform P-free pivots of all capacities.

General proof: docs/POSITIVE_CAPACITY_HANDOFFS.md. Recognition and compilation
never enumerate gate subsets; exhaustive audits are deliberately separate.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_canonical_band_coarsening import forests, tile_refinement, random_board
from check_degree_changing_bent_completions import compile_model
from check_P_free_pivot_interface import regions
from check_uniform_zero_capacity_openings import tile_cells
from check_protected_linear_corridors import subsets, frozen_board
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize
from check_residual_corridors import direct_check
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_capacity_two_gate_bundles import physical as bundle_fixture
from check_fully_frozen_elbow_withdrawal import configuration_one
from unittest.mock import patch

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def snapshot(cur, bits, gates, opened=frozenset()):
    changed=dict(bits)
    for i in opened:changed[gates[i]]=False
    regs=regions(cur,changed);data,closed,_=compile_model(cur,regs)
    fine=forests(cur,tile_refinement(*cur[:2],regs));coarse=forests(cur,regs)
    positive=[cc for cap,cc in fine.values() if cap]
    where={v:i for i,g in enumerate(gates) for v in tile_cells(g)}
    local={i:sorted((cc for cc in positive if next(iter(cc)) in where and
                     where[next(iter(cc))]==i),key=lambda cc:sorted(cc)) for i in range(len(gates))}
    anchors={('gate',i,k):cc for i,children in local.items() for k,cc in enumerate(children)}
    anchors.update({('fixed',tuple(sorted(cc))):cc for cc in positive if next(iter(cc)) not in where})
    assert len(anchors)==len(positive)
    at={v:uid for uid,cc in anchors.items() for v in cc};mapping={}
    for j,(cap,cc) in coarse.items():
        if cap:
            children={at[v] for v in cc if v in at}
            assert len(children)==1
            mapping[j]=children.pop()
    assert len(mapping)==len(anchors)==len(set(mapping.values()))
    norm=(*data[:3],{o:{mapping[j] for j in W} for o,W in data[3].items()},set(anchors))
    support={j:{o for o,W in norm[3].items() if j in W} for j in anchors}
    for i,children in local.items():
        assert len(children)==2-len(tile_cells(gates[i])&cur[2])
        assert all(support['gate',i,k]==support['gate',i,0] for k in range(len(children)))
    axes={uid:changed[min(r for r,c in cc)//2*2,min(c for r,c in cc)//2*2]
          for uid,cc in anchors.items()}
    return dict(data=norm,closed=closed,regs=regs,anchors=anchors,mapping=mapping,
                axes=axes,support=support)


def recognize(cur,bits,gates):
    """At most 2+2p snapshots, where p counts positive-capacity gates.

    Every failure is a concrete owner/resource incidence and ordered pair of
    physical states. No optimizer or primitive-pack enumeration is called.
    """
    direct_check(*cur)
    assert len(set(gates))==len(gates)
    P={v for e in cur[3] for v in e};G=frozenset(range(len(gates)))
    for g in gates:assert bits[g] and not tile_cells(g)&P
    cache={}
    def get(F):
        F=frozenset(F)
        if F not in cache:cache[F]=snapshot(cur,bits,gates,F)
        return cache[F]
    old=get(set());full=get(G);losses=[]
    def guard(kind,units,F):
        s=get(F)
        for j in units:
            for o in sorted(old['support'][j]-s['support'][j]):
                losses.append(dict(kind=kind,owner=o,resource=j,from_opened=[],to_opened=sorted(F)))
    guard('fixed_vertical', [j for j in old['support'] if j[0]=='fixed' and old['axes'][j]], G)
    for i,g in enumerate(gates):
        units=[j for j in old['support'] if j[0]=='gate' and j[1]==i]
        if units:
            guard('closed_phase',units,G-{i})
            guard('handoff',units,{i})
    return dict(accepted=not losses,losses=losses,old=old,full=full,snapshots=len(cache))


def compile_handoffs(cur,bits,gates):
    """Exact conditional-support compiler on passing inputs; no cost claim.

    Incidences are the union of old (unconditional) support and H-gap paths
    labelled by prerequisite sets of actual gate IDs. Shared fees stay shared.
    """
    result=recognize(cur,bits,gates)
    if not result['accepted']:return result
    full=result['full'];P={v for e in cur[3] for v in e}
    body_owner={v:o for o,x in enumerate(full['closed']) for v in x['body']}
    paths=[];b=0;placed=[];units_seen=[];gaps=[]
    for region in full['regs']:
        for band in region['bands']:
            if not region['vertical']:
                row=min(r for r,c in band[0]);start=min(c for r,c in band[0])
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
                    after=i;L,R=boundary(first-1),boundary(after)
                    units=[uid for j,uid in full['mapping'].items() if j[0]==b and first<=j[1]<=j[2]<after]
                    gg=[gi for gi,(r,c) in enumerate(gates) if r==row and start+first<=c and c+1<start+after]
                    placed+=gg;units_seen+=units
                    if units or gg:gaps.append(dict(left=L,right=R,units=units,gates=gg))
                    for uid in units:
                        c=min(c for r,c in full['anchors'][uid])
                        for o,req in ((L,{gi for gi in gg if gates[gi][1]<=c}),
                                      (R,{gi for gi in gg if gates[gi][1]+1>=c})):
                            if o is not None:paths.append((o,uid,frozenset(req)))
            b+=1
    assert set(placed)==set(range(len(gates))) and len(placed)==len(gates)
    H={j for j in full['data'][4] if not full['axes'][j]}
    assert set(units_seen)==H and len(units_seen)==len(H)
    result.update(paths=paths,gaps=gaps)
    return result


def compiled_support(compiled,opened):
    W={o:set(S) for o,S in compiled['old']['data'][3].items()}
    for o,j,req in compiled['paths']:
        if req<=opened:W[o].add(j)
    return W


def endpoint_trap(one=False,n=2):
    """All-length feasible family; NOT a freezing or numerical control."""
    assert n>=2
    T={(5,1)}|({(4,2*n)} if one else set())
    M=[((4,1),(3,1)),((3,0),(2,0)),((2,1),(2,2))]
    M += [((2,c),(2,c+1)) for c in range(3,2*n,2)]
    M += [((2,2*n+1),(3,2*n+1))]
    M += [((3,c),(3,c-1)) for c in range(4,2*n+1,2)]
    cur=(8,2*n+4,T,M)
    bits={(r,c):False for r in range(0,8,2) for c in range(0,2*n+4,2)}
    gates=[(4,2*i) for i in range(1,n+1)]
    for g in [(2,2*i) for i in range(n+1)]+gates:bits[g]=True
    return cur,bits,gates


def audit(cur,bits,gates,counts,primitive=True):
    c=compile_handoffs(cur,bits,gates);G=frozenset(range(len(gates)));records={}
    for F in subsets(G):
        s=snapshot(cur,bits,gates,F);old=c['old']
        assert s['data'][4]==old['data'][4] and s['data'][:2]==old['data'][:2]
        assert set(s['data'][2])==set(old['data'][2])
        assert [(x['body'],x['ends']) for x in s['closed']]==[(x['body'],x['ends']) for x in old['closed']]
        if c['accepted']:
            assert compiled_support(c,F)==s['data'][3]
            counts['exact_compiled_support_states']+=1
        if primitive:
            f=fork_flow(*s['data']);p=optimize(*s['data'])
            assert (f['value'],f['cost'])==(p['value'],p['cost'])
            counts['independent_primitive_optima']+=1
        records[F]=s
        counts['physical_states']+=1
    monotone=True
    for F,s in records.items():
        for i in G-F:
            t=records[F|{i}]
            for j,S in s['support'].items():
                T=t['support'][j]
                if j[0]=='gate' and j[1]==i:continue
                if s['axes'][j]:assert T<=S
                else:assert S<=T
                counts['phase_incidence_checks']+=1
            monotone &= all(S<=t['support'][j] for j,S in s['support'].items())
            counts['all_lattice_edges']+=1
        counts['capacity_two_twin_support_states']+=sum(
            2-len(tile_cells(g)&cur[2])==2 for g in gates)
    assert monotone==c['accepted']
    assert c['snapshots']<=2+2*sum(2-len(tile_cells(g)&cur[2])>0 for g in gates)
    for loss in c['losses']:
        assert loss['owner'] in records[frozenset(loss['from_opened'])]['support'][loss['resource']]
        assert loss['owner'] not in records[frozenset(loss['to_opened'])]['support'][loss['resource']]
        counts['physical_rejection_witnesses']+=1
        counts['rejection_'+loss['kind']]+=1
    counts['recognition_iff_all_subset_audits']+=1
    counts['accepted' if c['accepted'] else 'rejected']+=1
    for g in gates:counts['gate_capacity_'+str(2-len(tile_cells(g)&cur[2]))]+=1
    return dict(accepted=c['accepted'],shape=list(cur[:2]),T=len(cur[2]),matching=len(cur[3]),
                gates=gates,snapshots=c['snapshots'],states=len(records),losses=c['losses'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();counts=Counter();rows=[];rng=random.Random(2026102639)
    for R,C in ((4,4),(4,8),(6,6),(8,10)):
        for _ in range(12):
            cur=random_board(R,C,rng);P={v for e in cur[3] for v in e}
            bits={(r,c):bool(rng.randrange(2)) for r in range(0,R,2) for c in range(0,C,2)}
            candidates=[g for g in bits if not tile_cells(g)&P]
            rng.shuffle(candidates);gates=candidates[:min(5,len(candidates))]
            for g in gates:bits[g]=True
            rows.append(audit(cur,bits,gates,counts))
    # Hereditary thinning leaves feasible sparse inputs with many actual
    # capacity-one/two gates, nonempty legacy support and rejected handoffs.
    for _ in range(64):
        raw=random_board(8,8,rng)
        cur=(*raw[:2],{v for v in raw[2] if rng.random()<.35},[e for e in raw[3] if rng.random()<.3])
        P={v for e in cur[3] for v in e}
        bits={(r,c):bool(rng.randrange(2)) for r in range(0,8,2) for c in range(0,8,2)}
        candidates=[g for g in bits if not tile_cells(g)&P]
        rng.shuffle(candidates);gates=candidates[:4]
        for g in gates:bits[g]=True
        rows.append(audit(cur,bits,gates,counts))
    cur,bits,ranks,left,right,q=frozen_board(2,2)
    # All positive P-free tiles in the long corridor join the operation set.
    P={v for e in cur[3] for v in e}
    extra=[g for g in bits if not tile_cells(g)&P and 2-len(tile_cells(g)&cur[2])>0]
    for chosen in (extra[:2],extra[-2:]):
        bb=dict(bits)
        for g in chosen:bb[g]=True
        rows.append(audit(cur,bb,left+right+chosen,counts))
        counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
        assert frozen_certificate(cur)[0]==P
    # Fully frozen positive gates: two shared central outputs and two
    # capacity-one alternative outlets; all eight states retain mixed/beta.
    cur,bits,ranks,gates=bundle_fixture()
    rows.append(audit(cur,bits,gates,counts))
    counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
    assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
    frozen_positive=dict(shape=list(cur[:2]),T=len(cur[2]),matching=len(cur[3]),
        gates=gates,capacities=[2-len(tile_cells(g)&cur[2]) for g in gates],
        states=[dict(opened=sorted(F),value=(f:=fork_flow(*snapshot(cur,bits,gates,F)['data']))['value'],links=f['cost'])
                for F in subsets(range(len(gates)))])
    for one,n in itertools.product((False,True),(2,3,5)):
        cur,bits,gates=endpoint_trap(one,n)
        row=audit(cur,bits,gates,counts);c=recognize(cur,bits,gates)
        assert not c['accepted'] and all(S<=c['full']['support'][j] for j,S in c['old']['support'].items())
        assert len(c['losses'])==2*(n-1)-int(one) and all(x['kind']=='handoff' for x in c['losses'])
        for F in subsets(range(n)):
            s=snapshot(cur,bits,gates,F)
            for j,S in s['support'].items():
                if j[0]=='gate':
                    i=j[1]
                    assert S==({0} if i not in F or set(range(i+1))<=F else set())
                    counts['all_length_family_exact_local_supports']+=1
            f=fork_flow(*s['data']);assert f['value']==f['cost']==0
        counts['physical_endpoint_inclusion_traps']+=1
        row['control']='full original endpoint inclusion passes, singleton handoff fails; feasible, not fully frozen'
        rows.append(row)
        # An actual nonempty legacy-support handoff, in contrast to the trap.
        rows.append(audit(cur,bits,gates[:1],counts))
    # Failure on a fixed V anchor, now in the all-capacities recognizer.
    cur,bits,ranks=configuration_one();g=(10,16)
    rows.append(audit(cur,bits,[g],counts))
    counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
    def forbidden(*a,**kw):raise AssertionError('recognizer/compiler must not enumerate or optimize')
    cur,bits,gates=endpoint_trap()
    with patch(__name__+'.subsets',forbidden),patch(__name__+'.fork_flow',forbidden),patch(__name__+'.optimize',forbidden):
        assert not compile_handoffs(cur,bits,gates)['accepted']
        assert compile_handoffs(cur,bits,gates[:1])['accepted']
    counts['enumeration_and_optimizer_disabled_API_checks']+=2
    result=dict(status='PASS',scope='General written theorem plus finite independent checks; no universal 5/6 or general shared-fee optimizer claim.',counts=dict(counts),
                frozen_positive_fixture=frozen_positive,boards=rows)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(counts,sort_keys=True))


if __name__=='__main__':main()
