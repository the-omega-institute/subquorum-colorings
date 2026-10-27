"""Independent full-N checks for complete routing and both unbounded families."""
from itertools import product
from pathlib import Path
import json
import random
from monochromatic_completion_flow import solve_completion_flow
from zero_defect_long_relay import long_extension_obstacle, free_hh_relay_obstacle
from zero_fee_extension import zero_fee_extension
from check_strip_tree_compensation import partial_matchings
from check_general_square_ports import all_matchings, physical_state, edge, grid, mates
from check_mixed_terminal_compensation import neighbours
from strip_tree_compensation import physical_state_linear
from joint_frontier_compensation import solve_frontier

if not __debug__: raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def evaluate(h,w,m,t,weights,full,frontier=True):
    result=solve_completion_flow(h,w,m,t,weights)
    board=grid(h,w);state=physical_state(board,m,result['auxiliary'],t)
    assert state['data']['counts'][0]==0
    assert sum(weights[e] for e in state['paid'])==result['TH_fee']
    assert sum(weights[e] for p in state['data']['paths'] for e in p['M'])==result['all_terminal_cost']
    assert len(result['auxiliary'])==h*w//2
    potentials=result['potential']
    assert all(c+potentials[u]-potentials[v]>=0 for u,v,cap,c in result['residual_arcs'] if cap)
    all_costs=[];fees=[]
    for n in full:
        s=physical_state(board,m,n,t)
        assert s['data']['counts'][0]==0
        all_costs.append(sum(weights[e] for p in s['data']['paths'] for e in p['M']))
        fees.append(sum(weights[e] for e in s['paid']))
    assert min(all_costs)==result['all_terminal_cost']
    assert min(fees)<=result['TH_fee']<=result['all_terminal_cost']
    if result['TH_exactness_certified']:
        assert min(fees)==result['TH_fee']==result['all_terminal_cost']
    if frontier:
        r=solve_frontier(h,w,m,t,weights)
        assert (r['minimum_TT'],r['TH_cost'])==(0,min(fees))
    return dict(exact=result['TH_exactness_certified'],upper_gap=result['all_terminal_cost']-min(fees),
                evaluations=len(full),same_colour_hole_with_P_neighbour=any(
                 neighbours(v)&set(mates(board,m)) for v in board-set(mates(board,m))-t
                 if sum(v)%2==result['source_colour']))


def exhaustive():
    rows=[]
    for h,w in [(1,2),(1,4),(1,6),(2,2),(2,3),(3,2),(2,4)]:
        board=grid(h,w);full=[set(n) for n in all_matchings(board)]
        models=evaluations=exact=gap=zero_reachable=0
        for m0 in partial_matchings(board):
            m=set(m0);p={v for e in m for v in e};q=board-p
            selections={frozenset()}
            for colour in (0,1):
                sites=sorted(v for v in q if sum(v)%2==colour)
                for bits in product((False,True),repeat=len(sites)):
                    selections.add(frozenset(v for v,bit in zip(sites,bits) if bit))
            for t0 in sorted(selections,key=lambda x: (len(x),sorted(x))):
                t=set(t0);weights={e:(7*sum(e[0])+3*sum(e[1]))%9 for e in m}
                if models%31==0:weights={e:10**400+3+i for i,e in enumerate(sorted(m))}
                if models%29==0:weights={e:0 for e in m}
                r=evaluate(h,w,m,t,weights,full)
                models+=1;evaluations+=r['evaluations'];exact+=r['exact'];gap+=r['upper_gap']>0
                zero_reachable+=r['exact'] and r['same_colour_hole_with_P_neighbour']
        row=dict(height=h,width=w,all_one_colour_models=models,full_N_evaluations=evaluations,
                 exactness_condition_models=exact,strict_all_terminal_overestimates=gap,
                 zero_weight_HH_reachability_models=zero_reachable,frontier_checks=models)
        rows.append(row);print(json.dumps(row),flush=True)
    return rows


def larger_controls():
    rng=random.Random(10272743);rows=[]
    for h,w,count in [(4,4,24),(4,6,24),(6,4,24),(6,6,4)]:
        board=grid(h,w);full=[set(n) for n in all_matchings(board)]
        edges=sorted({edge(v,z) for v in board for z in neighbours(v)&board})
        evaluations=exact=gaps=0
        for i in range(count):
            rng.shuffle(edges);m=set();p=set()
            for e in edges:
                if not set(e)&p and rng.random()<.4:m.add(e);p.update(e)
            colour=i%2;t={v for v in sorted(board-p) if sum(v)%2==colour and (i%3==0 or rng.random()<.6)}
            weights={e:rng.randrange(12) for e in sorted(m)}
            if i==0:weights={e:10**400+5 for e in m}
            r=evaluate(h,w,m,t,weights,full)
            evaluations+=r['evaluations'];exact+=r['exact'];gaps+=r['upper_gap']>0
        rows.append(dict(height=h,width=w,models=count,full_N_evaluations=evaluations,
                         exactness_condition_models=exact,strict_all_terminal_overestimates=gaps,frontier_checks=count))
    return rows


def families():
    rows=[];flow_checks=[]
    for k in range(1,41):
        f=long_extension_obstacle(k);board=f['board'];p=f['P'];t=f['T'];holes=f['H']
        occupied=p|t
        assert all(len(neighbours(v)&occupied)<=1 for v in t)
        assert {v for e in f['M'] for v in e}==p
        assert len(f['M'])==8*k*k+4*k and len(t)==12*k+7 and len(holes)==12*k+9
        assert len(f['M'])+len(t)==len(board)//2-1
        assert {v for v in holes if sum(v)%2}=={f['white_hole']}
        assert not neighbours(f['white_hole'])&p and neighbours(f['centre'])<=p
        assert min(sum(abs(a-b) for a,b in zip(v,f['centre'])) for v in t)==2*k+1
        mates(board,f['direct']);assert len(f['direct'])==len(t)
        assert all((a in t and b in holes) or (b in t and a in holes) for a,b in f['direct'])
        hood={v for u in f['hall_black'] for v in neighbours(u)&board if v not in t}
        assert hood==f['hall_white'] and len(f['hall_black'])-len(hood)==1
        mates(board,set(f['M'])|f['direct'])
        s=physical_state_linear(board,f['M'],f['auxiliary'],t)
        assert s['data']['counts'][0]==0 and s['data']['counts'][1]==1
        assert s['paid']==f['paid'] and len(s['paid'])==k
        alternative={edge((a[1],a[0]),(b[1],b[0])) for a,b in f['M']}
        mates(board,alternative);assert alternative!=f['M']
        fixed={edge((r,c),(r,c+1)) for r in range(f['side']) for c in range(0,f['side'],2)}
        alt=physical_state_linear(board,alternative,fixed,t)
        assert alt['data']['counts'][0]==0 and len(alt['paid'])>=k
        # The second family has a free long HH, and all selected payments direct.
        free=free_hh_relay_obstacle(k)
        fs=physical_state_linear(free['board'],free['M'],free['auxiliary'],free['T'])
        assert not fs['paid'] and fs['data']['counts'][0]==0
        assert sum(len(path['M']) for path in fs['data']['paths'])==k
        assert all(not path['M'] for path in fs['data']['paths'] if path['kind']=='TH')
        rows.append(dict(k=k,side=f['side'],J=len(f['M'])+len(t),d=0,delta_0=1,
                         exact_unit_TH_fee=k,one_HH_path_direct=True,rematching_lower_control=True,
                         free_HH_comparison_side=free['side'],free_HH_all_terminal_optimum=k,free_HH_true_TH_optimum=0))
        if k<=8:
            z=zero_fee_extension(f['side'],f['side'],f['M'],t);assert z['defect']==1
            r=solve_completion_flow(f['side'],f['side'],f['M'],t)
            assert r['TH_exactness_certified'] and r['all_terminal_cost']==r['TH_fee']==k
            zf=zero_fee_extension(free['side'],free['side'],free['M'],free['T']);assert zf['defect']==0
            rf=solve_completion_flow(free['side'],free['side'],free['M'],free['T'])
            assert not rf['TH_exactness_certified'] and rf['all_terminal_cost']==k
            # A candidate returned by the overestimating optimizer need not
            # itself minimize TH fee; only the explicit free-HH witness does.
            weights={e:0 for e in free['M']}
            rz=solve_completion_flow(free['side'],free['side'],free['M'],free['T'],weights)
            assert rz['TH_exactness_certified'] and rz['TH_fee']==rz['all_terminal_cost']==0
            flow_checks.append(dict(k=k,sharp_flow_cost=r['all_terminal_cost'],free_HH_flow_cost=rf['all_terminal_cost'],
                                    exactness_with_zero_reachable_weights=True,whole_board_defects=[z['defect'],zf['defect']]))
    return dict(all_k_coordinate_controls=rows,complete_flow_controls=flow_checks)


def rejection_controls():
    cases=[(0,2,set(),set(),None),(3,3,set(),set(),None),(2,2,set(),{(0,0),(0,1)},None),
           (2,2,set(),{(4,0)},None),(2,2,{edge((0,0),(0,1))},set(),{}),
           (2,2,{edge((0,0),(0,1))},set(),{edge((0,0),(0,1)):-1})]
    for args in cases:
        try:solve_completion_flow(*args)
        except ValueError:pass
        else:raise AssertionError('Invalid input accepted')
    return len(cases)


def main():
    ex=exhaustive();large=larger_controls();fam=families()
    out=dict(status='PASS',exhaustive=ex,larger_controls=large,families=fam,
             rejected_invalid_inputs=rejection_controls(),
             exhaustive_models=sum(x['all_one_colour_models'] for x in ex),
             full_N_evaluations=sum(x['full_N_evaluations'] for x in ex+large),
             frontier_checks=sum(x['frontier_checks'] for x in ex+large),
             family_flow_checks=3*len(fam['complete_flow_controls']),
             scope='All M and all monochromatic T on seven small boards; independent full-N objectives and exact frontier; larger seeded models, exact residual potentials, zero and 401-digit weights. Forty parameters of both families; complete flows and whole-board defects for k<=8.',
             proof_scope='General physical flow adapter, sufficient exactness condition, all-k d=0/delta0=1 fee k with every-rematching lower bound, and all-k free-HH overcharge are written proofs. No new general flow algorithm, numerical coefficient, or Lean claim.')
    (ROOT/'output/monochromatic-completion-flow.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','exhaustive_models','full_N_evaluations','frontier_checks','family_flow_checks']}),flush=True)


if __name__=='__main__':main()
