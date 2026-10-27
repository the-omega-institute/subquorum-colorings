"""Independent exposure controls and exact coordinate/Hall certificates."""
from itertools import permutations
from pathlib import Path
import json
import random

from exposable_source_completion import surplus_exposure,expose_matching,solve_exposable_sources
from branched_source_obstruction import branched_family,weighted_obstruction
from check_staircase_source_completion import forward_core_distances,generic_budget,brute_discount
from staircase_source_completion import staircase_family,solve_staircase
from check_corner_relay_shortest_path import flip_rematching
from check_isolated_hole_detours import maximum_adjacent_matching
from check_general_square_ports import physical_state
from check_mixed_terminal_compensation import edge,mates,neighbours
from shared_source_exact_completion import _shortest_relay

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def abstract_graph_controls():
    graphs=saturated=flips=0
    for n in range(4):
        left={('L',i) for i in range(n)};right={('R',i) for i in range(n+1)}
        pairs=[(a,b) for a in sorted(left) for b in sorted(right)]
        for mask in range(1<<len(pairs)):
            adj={a:set() for a in left}
            for i,(a,b) in enumerate(pairs):
                if mask>>i&1:adj[a].add(b)
            brute=set()
            for images in permutations(sorted(right),n):
                if all(b in adj[a] for a,b in zip(sorted(left),images)):brute|=right-set(images)
            result=surplus_exposure(left,right,adj);graphs+=1
            assert (result is None)==(not brute)
            if result is not None:
                saturated+=1;assert result['exposable']==brute
                for target in brute:
                    exposed=expose_matching(result,target)
                    assert set(exposed.values())==right-{target};flips+=1
    return dict(all_bipartite_graphs=graphs,saturating_graphs=saturated,exposure_flips=flips,
                scope='Every graph with left size 0,1,2,3 and right size one greater; independent permutation enumeration of all left-saturating matchings.')


def rescore(f,result,weights):
    if result['auxiliary'] is None:return None
    state=physical_state(f['board'],result['M'],result['auxiliary'],f['T'])
    assert sum(weights[e] for e in state['paid'])==result['normal_form_optimum']
    assert state['paid']==result['TH_relay']['actual']
    used=set();sources=set()
    for path in state['data']['paths']:
        assert not used&path['M'];used|=path['M']
        if path['kind']=='HH':
            z=next(v for v in (path['vertices'][0],path['vertices'][-1]) if sum(v)%2)
            assert z not in sources;sources.add(z)
    assert sources==result['white_holes'] and state['data']['counts'][0]==0
    return state


def exterior_and_unit_certificate():
    f=branched_family(True);s=solve_exposable_sources(f['board'],f['M'],f['T'],f['parts'],f['centres'])
    outer=s['outer'];black=outer['left'];exposable=set()
    for t in sorted(f['T']):
        value=maximum_adjacent_matching(f['T']-{t},black)
        if value==len(black):exposable.add(t)
        else:assert value==len(black)-1
    assert exposable==outer['exposable']==f['T']-f['white_chamber']
    assert len(f['M'])==60 and len(f['T'])==98 and len(exposable)==78
    assert len(f['black_chamber'])==len(f['white_chamber'])==20
    assert set().union(*(neighbours(b)&f['T'] for b in f['black_chamber']))==f['white_chamber']
    mm=mates(f['board'],f['M']);one_edge=[]
    for part,h in zip(f['parts'],f['centres']):
        assert neighbours(h)<=part
        one_edge.append(set().union(*(neighbours(mm[w])&f['T'] for w in neighbours(h))))
    assert one_edge==[{f['cheap_source']},set(),set(),set(),set()]
    assert s['rho']==[1,2,2,2,2] and s['sigma']==[2]*5
    assert s['source_budget']==1 and s['normal_form_optimum']==2
    assert s['strict_positive_hypotheses'] and s['budget_attainment_decided'] and not s['budget_attained']
    assert s['eligible_roots']==set(range(5))
    assert forward_core_distances(f,f['M'],{e:1 for e in f['M']})==s['rho']
    restricted=dict(f,T=exposable);assert forward_core_distances(restricted,f['M'],{e:1 for e in f['M']})==s['sigma']
    budget=generic_budget(f,f['M'],{e:1 for e in f['M']});assert budget['lower_bound']==1
    assert budget['max_discount']==brute_discount(budget)==8
    rescore(f,s,{e:1 for e in f['M']})
    relays=[_shortest_relay(h,p,{v for u in p for v in neighbours(u)&f['T']},mm,{e:1 for e in f['M']})['path'] for p,h in zip(f['parts'],f['centres'])]
    certificate=dict(board=[18,18],origins=f['origins'],centres=f['centres'],white_holes=sorted(f['white_holes']),
                     black_Hall_set=sorted(f['black_chamber']),white_Hall_neighbours=sorted(f['white_chamber']),
                     unit_actual_matching=sorted(f['M']),unit_attaining_auxiliary=sorted(s['auxiliary']),
                     unit_shortest_core_relays=relays,unit_one_actual_edge_sources=[sorted(x) for x in one_edge],
                     unit_TH_relay=s['TH_relay']['path'],unit_HH_assignment=sorted(s['HH_assignment'].items()),
                     unit_rho=s['rho'],unit_sigma=s['sigma'],unit_source_budget=1,unit_true_optimum=2,
                     unit_lower_proof='At most four HH centres; one-edge TH can only be centre0 from t* in the tight Hall chamber. All other terminal paths would be direct and cannot match 20 black vertices to 19 available white neighbours.',
                     outer_base_matching=sorted(outer['matching'].items()),outer_exposed=outer['exposed'],
                     all_exposable_white_ports=sorted(exposable))
    return certificate,dict(all_white_deletion_independent_matchings=len(f['T']),exposable_whites=len(exposable),
                            nonexposable_whites=len(f['white_chamber']),black_Hall_set_size=20,
                            unit_source_budget=1,unit_true_optimum=2)


def weighted_gap_controls(certificate):
    rows=[]
    for k in [2,3,7,100,10**6,10**400+17]:
        f=weighted_obstruction(k);s=solve_exposable_sources(f['board'],f['M'],f['T'],f['parts'],f['centres'],f['weights'])
        assert s['rho']==[1,k,k,k,k] and s['sigma']==[k]*5
        assert s['source_budget']==1 and s['normal_form_optimum']==k
        assert s['strict_positive_hypotheses'] and s['budget_attainment_decided'] and not s['budget_attained']
        mm=mates(f['board'],f['M']);b,w=(6,8),(7,8)
        assert mm[b]==w and neighbours(b)&f['T']=={f['cheap_source']}
        assert neighbours(w)&(f['board']-f['P'])=={f['centres'][0]}
        assert s['TH_relay']['path']==[(8,5),(8,6),(8,7),(8,8)]
        state=rescore(f,s,f['weights']);assert sum(f['weights'][e] for e in state['paid'])==k
        budget=generic_budget(f,f['M'],f['weights']);assert budget['lower_bound']==1
        rows.append(dict(K=k,source_budget=1,true_TH_optimum=k,normal_form_optimum=k,
                         proof='If f<K, only the one cheap edge can be paid. Its centre relay consumes t* in F and all W are HH centre sources; the Hall chamber then forbids direct completion. Explicit full N attains K.'))
    certificate.update(canonical_actual_matching=sorted(f['M']),cheap_edge=f['cheap_edge'],cheap_source=f['cheap_source'],
                       weighted_attaining_auxiliary=sorted(s['auxiliary']),weighted_TH_relay=s['TH_relay']['path'],
                       weighted_HH_assignment=sorted(s['HH_assignment'].items()),
                       weighted_symbolic_cost='1 on cheap_edge, K on every other M edge, integer K>=2',
                       weighted_exact_formula='source_budget=1; true_TH_optimum=K for every integer K>=2')
    return rows


def rematching_controls():
    rng=random.Random(27102799);rows=[];f=branched_family()
    for variant in range(48):
        m=flip_rematching(f['M'],f['P'],rng,80*(variant+1))
        weights={e:rng.randrange(12) for e in sorted(m)}
        if variant%8==0:weights={e:1 for e in m}
        elif variant%8==1:weights={e:0 for e in m}
        elif variant%8==2:weights={e:10**400+3*j for j,e in enumerate(sorted(m))}
        elif variant%8==3:weights={e:rng.randrange(1,12) for e in sorted(m)}
        s=solve_exposable_sources(f['board'],m,f['T'],f['parts'],f['centres'],weights)
        assert s['rho']==forward_core_distances(f,m,weights)
        assert s['sigma']==forward_core_distances(dict(f,T=s['outer']['exposable']),m,weights)
        budget=generic_budget(f,m,weights)
        assert budget['lower_bound']==s['source_budget'] and budget['max_discount']==brute_discount(budget)
        assert [budget['terminal_lower_weights'][h] for h in f['centres']]==s['rho']
        phi=budget['potential'];assert all(c+phi[a]-phi[b]>=0 for a,b,cap,c in budget['residual_arcs'] if cap)
        rescore(f,s,weights)
        assert s['source_budget']<=s['normal_form_optimum']
        if s['budget_attained']:assert s['budget_attainment_decided']
        elif s['strict_positive_hypotheses']:assert s['budget_attainment_decided']
        rows.append(dict(variant=variant,changed_M=m!=f['M'],rho=s['rho'],sigma=s['sigma'],
                         source_budget=s['source_budget'],normal_form_upper=s['normal_form_optimum'],
                         exact_TH_certified=s['budget_attained'],strict_budget_nonattainment=(s['strict_positive_hypotheses'] and not s['budget_attained']),
                         scope='Upper is the exact one-paid-centre/direct-exterior normal form. It is not asserted to be the global optimum unless lower=upper.'))
    return rows


def staircase_controls():
    rows=[];rng=random.Random(27102800)
    for scales in [(1,),(1,1),(1,1,1),(2,1,3),(1,2,1,1),(1,)*6]:
        f=staircase_family(scales)
        for variant in range(4):
            m=flip_rematching(f['M'],f['P'],rng,120*(variant+1));weights={e:rng.randrange(16) for e in sorted(m)}
            if variant==0:weights={e:1 for e in m}
            elif variant==1:weights={e:0 for e in m}
            a=solve_exposable_sources(f['board'],m,f['T'],f['parts'],f['centres'],weights)
            b=solve_staircase(scales,m,weights)
            assert a['rho']==a['sigma']==b['rho']
            assert a['source_budget']==a['normal_form_optimum']==b['minimum_TH_fee']
            assert a['outer']['exposable']==f['T'] and a['eligible_roots']==set(range(len(scales)))
            rescore(f,a,weights);rows.append(dict(scales=scales,variant=variant,exact_TH_fee=b['minimum_TH_fee']))
    return rows


def main():
    graphs=abstract_graph_controls();certificate,outer=exterior_and_unit_certificate()
    weighted=weighted_gap_controls(certificate);rematched=rematching_controls();staircase=staircase_controls()
    out=dict(status='PASS',abstract_graphs=graphs,branched_unit_obstruction=outer,weighted_gap=weighted,
             rematched_controls=rematched,staircase_controls=staircase,
             rematched_models=len(rematched),changed_actual_matchings=sum(r['changed_M'] for r in rematched),
             certified_exact_rematched_models=sum(r['exact_TH_certified'] for r in rematched),
             strict_budget_nonattainment_models=sum(r['strict_budget_nonattainment'] for r in rematched),
             staircase_specialization_comparisons=len(staircase),
             proof_scope='General two-exposure normal-form theorem and positive-weight budget-attainment iff are written proofs. Explicit finite Hall and matching certificates prove the fixed unit example; an all-integer-K argument proves the weighted unbounded gap on one footprint. Enumeration discovers/tests witnesses, not arbitrary-size claims. No Lean or universal 5/6 claim.')
    (ROOT/'output/branched-source-coordinate-certificates.json').write_text(json.dumps(certificate,indent=2)+'\n')
    (ROOT/'output/exposable-source-completion.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','rematched_models','changed_actual_matchings','certified_exact_rematched_models','strict_budget_nonattainment_models','staircase_specialization_comparisons']}),flush=True)
    print(json.dumps(graphs),flush=True);print(json.dumps(outer),flush=True)


if __name__=='__main__':main()
