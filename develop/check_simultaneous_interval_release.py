"""Exact joint release ledger and frozen eleven/two-unit obstructions.

General proofs: SIMULTANEOUS_INTERVAL_RELEASE_AND_PHYSICAL_CIRCUITS.md.
Resource deletion reserves identities; it does not edit the physical grid.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_compensation_flow_geometry_frontier import pad_image
from check_even_bridge_support_completion import endpoints_of
from check_frozen_beta_support_fork import fixture, stacked, restrict, A, C, B
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical, whole_support_data, optimize, ordinary_flow

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def delete(data, removed):
    removed=set(removed)
    return (*data[:3], {o:w-removed for o,w in data[3].items()}, data[4]-removed)


def subsets(values):
    values=sorted(values)
    for bits in range(1<<len(values)):
        yield frozenset(v for i,v in enumerate(values) if bits>>i&1)


def fixed_paid_model(data):
    answer=fork_flow(*data)
    _,alphas,betas,mixed=owner_data(*data[:2])
    paid=set().union(*(set(c['owners'])&alphas for c in answer['certificates'])) if answer['certificates'] else set()
    assert len(paid)==answer['value']
    fixed=restrict(data,paid|betas|mixed,data[4])
    assert fork_flow(*fixed)['value']==len(paid)
    return fixed,len(paid)


def abstract_checks(totals):
    rng=random.Random(20261031)
    examples=[]
    for index in range(320):
        kinds,pairs,possible=canonical('AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,6))))
        rng.shuffle(possible)
        resources=set(range(rng.randrange(6)))
        support={o:set() for o in range(len(pairs))}
        for j in resources:
            for o in rng.sample(range(len(pairs)),rng.randrange(min(2,len(pairs))+1)):
                support[o].add(j)
        original=(kinds,pairs,possible[:rng.randrange(min(13,len(possible))+1)],support,resources)
        fixed,p=fixed_paid_model(original)
        totals['initially_deficient_models']+=fork_flow(*original)['deficit']>0
        values={}
        for H in subsets(resources):
            f=fork_flow(*delete(fixed,H))
            values[H]=f['value']
            if index<40:
                other=optimize(*delete(fixed,H))
                assert (other['value'],other['cost'])==(f['value'],f['cost'])
                totals['abstract_independent_packing_comparisons']+=1
            totals['abstract_deleted_flow_models']+=1
        safe={H for H,v in values.items() if v==p}
        largest=fork_flow(*fixed,maximal_cut=True)
        far=resources-set(largest['source_side_intervals'])
        for j in resources:
            assert (frozenset({j}) in safe)==(j in far)
            totals['canonical_single_release_checks']+=1
        for F in subsets(resources):
            expected=len(F)-p+values[F]
            actual=max(len(H) for H in safe if H<=F)
            assert actual==expected
            totals['exact_release_rank_comparisons']+=1
        circuits=[H for H,v in values.items() if v<p and all(H-{h} in safe for h in H)]
        for H in circuits:
            assert values[H]==p-1
            assert len(H)-p+values[H]==len(H)-1
            totals['minimal_release_obstructions']+=1
        if circuits and len(examples)<4:
            examples.append(dict(model=index,paid_sources=p,minimal_obstructions=[sorted(H) for H in circuits]))
        totals['abstract_fixed_paid_systems']+=1
    return examples


def sectors(data, move=lambda x:x):
    owner,alphas,betas,mixed=owner_data(*data[:2])
    a,c,b=(owner[move(pair[0])] for pair in (A,C,B))
    d=owner[move((7,12))];e=owner[move((7,11))];x=owner[move((12,10))]
    assert alphas>={a,c,d} and betas>={b,e} and x in mixed
    group=[data[3][o] for o in (a,c,b)]
    assert list(map(len,group))==[5,2,4]
    assert sum(map(len,group))==len(set().union(*group))
    assert not data[3][d] and not data[3][x] and len(data[3][e])==5
    return group,(a,c,d,b,e,x)


def physical_base(totals):
    current,_=fixture()
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,_=whole_support_data(current,whole_bands(current))
    group,owners=sectors(data);aw,cw,bw=group;F=set().union(*group)
    a,c,d,b,e,x=owners
    owner=owner_data(*data[:2])[0]
    links={(owner[u],owner[v]) for u,v in data[2] if owner[u]!=owner[v]}
    assert links=={(a,b),(c,b),(d,e),(d,x)}
    coords={o:{(meta['intervals'][j]['band'],meta['intervals'][j]['first']) for j in w}
            for o,w in zip(('A','C','B'),group)}
    assert coords=={'A':{(1,3),(1,4),(1,5),(1,6),(2,4)},
                   'C':{(6,3),(6,4)},'B':{(4,7),(4,8),(4,9),(4,10)}}
    outcomes=Counter();safe=0;min_cost_safe=0;answers={}
    for H in subsets(F):
        na,nc,nb=(len(w-H) for w in group)
        z=int(na+nc+nb==0)
        expected=(3-z,1+int(na==0)+int(nc==0)-z)
        reduced=delete(data,H);flow=fork_flow(*reduced);other=optimize(*reduced)
        assert (flow['value'],flow['cost'])==expected==(other['value'],other['cost'])
        assert flow['value']==3 or H==F
        safe+=flow['value']==3
        min_cost_safe+=(flow['value'],flow['cost'])==(3,1)
        outcomes[expected]+=1
        answers[H]=expected
        totals['physical_base_deletion_models']+=1
        totals['physical_independent_packing_comparisons']+=1
    assert safe==2047
    assert min_cost_safe==(2**5-1)*(2**2-1)*2**4
    # Independent subset dynamic programming computes the largest safe
    # subreservation of every K, from all previously optimized H outcomes.
    release={};cost_release={}
    for K in sorted(answers,key=lambda s:(len(s),sorted(s))):
        release[K]=len(K) if answers[K][0]==3 else -1
        cost_release[K]=len(K) if answers[K]==(3,1) else -1
        for j in K:
            release[K]=max(release[K],release[K-{j}])
            cost_release[K]=max(cost_release[K],cost_release[K-{j}])
        assert release[K]==min(len(K),10)
        assert cost_release[K]==min(len(K&aw),4)+min(len(K&cw),1)+len(K&bw)
        totals['physical_all_candidate_value_and_cost_rank_checks']+=1
    selected=[]
    for H in [set(),{min(cw)},{max(cw)},cw,F]:
        f=fork_flow(*delete(data,H),maximal_cut=True)
        selected.append(dict(deleted=sorted(H),value=f['value'],minimum_links=f['cost'],certificates=f['certificates']))
    # Explicit original capacity-13 cut: source, A,C,B bodies, both B tips,
    # and eleven interval nodes. All other nodes, including D, are outside.
    # The exact owner-link and support checks above certify no large arc crosses.
    cut_capacity=1+1+len(F)  # source->D, whole B, the F interval sinks
    assert cut_capacity==13 and cut_capacity-len(F)==2
    return dict(shape=list(current[:2]),selected=len(current[2]),actual_endpoints=len(endpoints_of(current)),
        original_intervals=len(data[4]),candidate_intervals=sorted(F),
        coordinates={o:sorted(w) for o,w in coords.items()},
        release_capacity=10,release_capacity_at_original_minimum_links=9,
        minimally_nonreleasable_set_size=11,original_cut_capacity=cut_capacity,
        all_proper_deletions_feasible=safe,original_cost_preserving_deletions=min_cost_safe,
        outcomes=[dict(value=v,minimum_links=c,count=n) for (v,c),n in sorted(outcomes.items())],
        selected_deletions=selected)


def physical_stacks(totals):
    records=[];rng=random.Random(20261101)
    for q in range(1,17):
        current=stacked(q)
        direct_check(*current)
        assert frozen_certificate(current)[0]==endpoints_of(current)
        data,_,_=whole_support_data(current,whole_bands(current))
        groups=[sectors(data,lambda v,i=i:(v[0]+16*i,v[1]))[0] for i in range(q)]
        assert len(set().union(*(set().union(*gs) for gs in groups)))==11*q
        for pattern in ('none','all_C','all_F','all_A_C','one_A_left','one_B_left','random'):
            H=set()
            for aw,cw,bw in groups:
                F=aw|cw|bw
                if pattern=='all_C':H|=cw
                if pattern=='all_F':H|=F
                if pattern=='all_A_C':H|=aw|cw
                if pattern=='one_A_left':H|=F-{min(aw)}
                if pattern=='one_B_left':H|=F-{min(bw)}
                if pattern=='random':H|={j for j in F if rng.randrange(2)}
            z=sum(not (aw|cw|bw)-H for aw,cw,bw in groups)
            a0=sum(not aw-H for aw,cw,bw in groups)
            c0=sum(not cw-H for aw,cw,bw in groups)
            expected=(3*q-z,q+a0+c0-z)
            f=fork_flow(*delete(data,H))
            assert (f['value'],f['cost'])==expected
            totals['physical_stack_deletion_models']+=1
            if q<=3:
                other=optimize(*delete(data,H))
                assert (other['value'],other['cost'])==expected
                totals['stack_independent_packing_comparisons']+=1
            records.append(dict(copies=q,pattern=pattern,removed_intervals=len(H),value=f['value'],minimum_links=f['cost']))
    return records


def phases(totals):
    current,_=fixture();outcomes=Counter()
    for sym,offset in itertools.product(itertools.product((False,True),repeat=3),itertools.product((2,3),repeat=2)):
        image=pad_image(current,sym,offset)
        direct_check(*image)
        assert frozen_certificate(image)[0]==endpoints_of(image)
        data,_,_=whole_support_data(image,whole_bands(image))
        f=fork_flow(*data);ordinary=ordinary_flow(*data)
        assert f['deficit']==0
        assert (f['value'],f['cost'])==(ordinary['value'],ordinary['cost'])
        totals['reselected_band_phase_models']+=1
        outcomes[(sym[0],offset[0]%2,f['value'],f['cost'])]+=1
    return [dict(transposed=t,row_offset_parity=p,value=v,minimum_links=c,count=n)
            for (t,p,v,c),n in sorted(outcomes.items())]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter()
    abstract=abstract_checks(totals)
    base=physical_base(totals)
    print(json.dumps(dict(stage='abstract_and_base',totals=dict(totals))),flush=True)
    stacks=physical_stacks(totals);phase=phases(totals)
    report=dict(status='PASS',totals=dict(totals),abstract_obstruction_examples=abstract,
        physical_base=base,physical_stacks=stacks,reselected_band_phases=phase,
        scope='Written exact simultaneous-release formula retaining prescribed paid sources; '
              'all 2048 reservations of the physical eleven-unit sector independently optimized; '
              'arbitrary-copy formula has a separation proof, finite stack checks are controls; '
              'two C units obstruct simultaneous release at unchanged minimum link cost only. '
              'Resource reservations do not edit the physical grid or its scalar ledger. '
              'No unrestricted full-compensation or target-inequality counterexample claimed.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))),flush=True)


if __name__=='__main__':main()
