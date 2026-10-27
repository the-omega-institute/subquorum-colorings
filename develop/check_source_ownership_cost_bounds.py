"""Independent full-N identities, frontier comparisons, HH discount capacities."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import random
from source_ownership_cost_bounds import source_ownership_bounds
from two_source_chambers import two_source_chambers
from shared_hole_chambers import shared_hole_chambers
from monochromatic_completion_flow import solve_completion_flow
from strip_tree_compensation import physical_state_linear
from check_strip_tree_compensation import partial_matchings
from check_general_square_ports import all_matchings, physical_state, edge, grid, mates
from check_mixed_terminal_compensation import neighbours
from joint_frontier_compensation import solve_frontier

if not __debug__: raise RuntimeError('Assertions required')
ROOT=Path(__file__).resolve().parents[1]


def brute_discount(budget):
    ell=budget['terminal_lower_weights'];rows=list(budget['reachable_discount_pairs'].values())
    sites=sorted({b for row in rows for b in row});bits={b:1<<i for i,b in enumerate(sites)}
    @lru_cache(None)
    def solve(i,used):
        if i==len(rows):return 0
        best=solve(i+1,used)
        for b in rows[i]:
            if not used&bits[b]:best=max(best,ell[b]+solve(i+1,used|bits[b]))
        return best
    return solve(0,0)


def evaluate(h,w,m,t,weights,full):
    r=source_ownership_bounds(h,w,m,t,weights);board=grid(h,w)
    assert brute_discount(r['source_budget'])==r['source_budget']['max_discount']
    for flow in [r['lower_flow'],r['upper_flow'],r['source_budget']]:
        phi=flow['potential']
        assert all(c+phi[u]-phi[v]>=0 for u,v,cap,c in flow['residual_arcs'] if cap)
    assert r['ambiguous']|r['exclusive_T']|r['exclusive_H']|r['unreachable']==m
    assert sum(map(len,[r['ambiguous'],r['exclusive_T'],r['exclusive_H'],r['unreachable']]))==len(m)
    fees=[];lows=[];highs=[];ell=r['source_budget']['terminal_lower_weights']
    for n in full:
        s=physical_state(board,m,n,t);assert s['data']['counts'][0]==0
        path_actual=set().union(set(),*(p['M'] for p in s['data']['paths']))
        fee=sum(weights[e] for e in s['paid']);fees.append(fee)
        low=sum(weights[e] for e in path_actual&r['exclusive_T']);lows.append(low)
        high=sum(weights[e] for e in path_actual&(r['exclusive_T']|r['ambiguous']));highs.append(high)
        assert fee-low==sum(weights[e] for e in s['paid']&r['ambiguous'])
        assert high-fee==sum(weights[e] for e in (path_actual-s['paid'])&r['ambiguous'])
        hh_saving=0;used_holes=set();used_black=set()
        for path in s['data']['paths']:
            vs=path['vertices'];white,black=(vs[0],vs[-1]) if sum(vs[0])%2==r['source_colour'] else (vs[-1],vs[0])
            assert black in ell and black not in used_black;used_black.add(black)
            if path['kind']=='TH':assert sum(weights[e] for e in path['M'])>=ell[black]
            else:
                assert white not in used_holes;used_holes.add(white);hh_saving+=ell[black]
        assert hh_saving<=r['source_budget']['max_discount']
        assert r['source_budget']['lower_bound']<=fee
    optimum=min(fees)
    assert min(lows)==r['lower_bound'] and min(highs)==r['static_upper_bound']
    assert r['combined_lower_bound']<=optimum<=r['TH_fee']<=r['static_upper_bound']
    actual=physical_state(board,m,r['auxiliary'],t)
    assert sum(weights[e] for e in actual['paid'])==r['TH_fee']
    if r['exactness_certified']:assert r['TH_fee']==optimum
    frontier=solve_frontier(h,w,m,t,weights)
    assert (frontier['minimum_TT'],frontier['TH_cost'])==(0,optimum)
    return dict(evaluations=len(full),separated=r['source_separated'],
                certified=r['exactness_certified'],ambiguity_weight=r['ambiguity_weight'],
                static_width=r['static_upper_bound']-r['lower_bound'],
                combined_width=r['TH_fee']-r['combined_lower_bound'],
                budget_improves=r['source_budget']['lower_bound']>r['lower_bound'],
                positive_optimum=optimum>0,
                feasible=all(len(neighbours(v)&({x for e in m for x in e}|t))<=1 for v in t))


def enumerate_models():
    out=[];total_index=0
    for h,w in [(1,2),(1,4),(1,6),(2,2),(2,3),(3,2),(2,4)]:
        board=grid(h,w);full=[set(n) for n in all_matchings(board)];rows=[]
        for mm in partial_matchings(board):
            m=set(mm);q=board-{v for e in m for v in e};selections={frozenset()}
            for colour in (0,1):
                sites=sorted(v for v in q if sum(v)%2==colour)
                for bits in product((0,1),repeat=len(sites)):
                    selections.add(frozenset(v for v,on in zip(sites,bits) if on))
            for tt in sorted(selections,key=lambda x:(len(x),sorted(x))):
                weights={e:(11*sum(e[0])+3*sum(e[1])+total_index)%7 for e in m}
                if total_index%23==0:weights={e:0 for e in m}
                if total_index%31==0:weights={e:10**400+i for i,e in enumerate(sorted(m))}
                rows.append(evaluate(h,w,m,set(tt),weights,full));total_index+=1
        out.append(summarize(h,w,rows));print(json.dumps(out[-1]),flush=True)
    return out


def summarize(h,w,rows):
    return dict(height=h,width=w,models=len(rows),full_N_evaluations=sum(x['evaluations'] for x in rows),
                source_separated=sum(x['separated'] for x in rows),certified_optima=sum(x['certified'] for x in rows),
                positive_optima=sum(x['positive_optimum'] for x in rows),feasible_selections=sum(x['feasible'] for x in rows),
                budget_strictly_improves_static_lower=sum(x['budget_improves'] for x in rows),
                unresolved_certificate_intervals=sum(x['combined_width']>0 for x in rows),
                tight_positive_static_width=sum(x['static_width']==x['ambiguity_weight']>0 for x in rows))


def larger_models():
    rng=random.Random(271019);out=[]
    for h,w,count in [(3,4,80),(4,4,48),(4,6,16),(6,4,16)]:
        board=grid(h,w);full=[set(n) for n in all_matchings(board)]
        edges=sorted({edge(a,b) for a in board for b in neighbours(a)&board});rows=[]
        for i in range(count):
            rng.shuffle(edges);m=set();p=set()
            for e in edges:
                if not set(e)&p and rng.random()<.55:m.add(e);p.update(e)
            colour=i%2;sites=sorted(v for v in board-p if sum(v)%2==colour)
            t={v for v in sites if i%7==0 or rng.random()<.7}
            weights={e:rng.randrange(7) for e in m}
            if i==0:weights={e:10**400+7 for e in m}
            if i==1:weights={e:0 for e in m}
            rows.append(evaluate(h,w,m,t,weights,full))
        out.append(summarize(h,w,rows));print(json.dumps(out[-1]),flush=True)
    return out


def sharp_controls():
    m={edge((1,1),(1,2)),edge((1,3),(2,3)),edge((2,0),(2,1))};t={(0,1),(1,0)}
    full=[set(n) for n in all_matchings(grid(3,4))];rows=[]
    for scale in [0,1,17,10**400+3]:
        weights={e:scale for e in m};r=source_ownership_bounds(3,4,m,t,weights)
        evaluate(3,4,m,t,weights,full)
        assert r['ambiguous']=={edge((1,3),(2,3))}
        assert (r['lower_bound'],r['static_upper_bound'],r['TH_fee'])==(0,scale,0)
        rows.append(dict(scale=scale,L=0,U=scale,exact_fee=0,width_equals_ambiguity_weight=True))
    return rows


def family_controls():
    separated=[];shared=[];weighted=[]
    for k in range(1,25):
        a=two_source_chambers(k);s=physical_state_linear(a['board'],a['M'],a['auxiliary'],a['T'])
        assert s['paid']==a['TH_paid'] and len(s['paid'])==k
        assert sum(len(p['M']) for p in s['data']['paths'] if p['kind']=='HH')==k
        occupied={v for e in a['M'] for v in e}|a['T']
        assert all(len(neighbours(v)&occupied)<=1 for v in a['T'])
        separated.append(dict(k=k,height=a['height'],width=a['width'],explicit_TH=k,explicit_HH=k))
        b=shared_hole_chambers(k);occupied=b['P']|b['T']
        assert all(len(neighbours(v)&occupied)<=1 for v in b['T'])
        assert len(b['M'])==16*k*k+8*k and len(b['T'])==16*k*k+16*k+3
        assert len(b['H'])==16*k*k+16*k+5
        assert len(b['M'])+len(b['T'])==len(b['board'])//2-1
        assert {v for v in b['H'] if sum(v)%2}=={b['white_hole']}
        assert all(neighbours(v)<=b['P'] for v in b['centres'])
        assert all(min(sum(abs(x-y) for x,y in zip(v,z)) for z in b['T'])==2*k+1 for v in b['centres'])
        assert all(sum(abs(x-y) for x,y in zip(v,b['white_hole']))==4*k+1 for v in b['centres'])
        lo=physical_state_linear(b['board'],b['M'],b['true_TH_auxiliary'],b['T'])
        hi=physical_state_linear(b['board'],b['M'],b['all_terminal_auxiliary'],b['T'])
        assert lo['paid']==b['true_TH_paid'] and len(lo['paid'])==k
        assert sum(len(p['M']) for p in lo['data']['paths'] if p['kind']=='HH')==2*k
        assert len(hi['paid'])==2*k and not any(p['M'] for p in hi['data']['paths'] if p['kind']=='HH')
        assert len(b['corner_relay'])-1==4*k+1
        shared.append(dict(k=k,height=b['height'],width=b['width'],J=len(b['M'])+len(b['T']),
                           explicit_TH_optimum=k,explicit_all_terminal_optimum=2*k,
                           positive_HH_fee_at_TH_optimum=2*k))
        if k<=6:
            r=source_ownership_bounds(a['height'],a['width'],a['M'],a['T'])
            old=solve_completion_flow(a['height'],a['width'],a['M'],a['T'])
            assert r['source_separated'] and r['TH_fee']==r['lower_bound']==r['static_upper_bound']==k
            assert not old['TH_exactness_certified'] and old['all_terminal_cost']==2*k
            rb=source_ownership_bounds(b['height'],b['width'],b['M'],b['T'])
            cb=solve_completion_flow(b['height'],b['width'],b['M'],b['T'])
            assert rb['source_budget']['lower_bound']==k
            assert cb['all_terminal_cost']==cb['TH_fee']==2*k
            # Nonnegative reweightings and rematchings preserve the source
            # budget lower bound; an explicit complete N remains an upper witness.
            for variant in range(3):
                m=b['M']
                if variant==2:
                    n=4*k+2;move=lambda v:(v[0]+4*k,v[1]+n)
                    core=__import__('check_unbounded_hole_relay').family(k)
                    transpose={edge((x[1],x[0]),(y[1],y[0])) for x,y in core['M']}
                    m=transpose|{edge(move(x),move(y)) for x,y in transpose}
                weights={e:(0 if variant==0 else (10**400+3 if variant==1 else 1)) for e in m}
                rr=source_ownership_bounds(b['height'],b['width'],m,b['T'],weights)
                witness=physical_state_linear(b['board'],m,b['true_TH_auxiliary'],b['T'])
                fee=sum(weights[e] for e in witness['paid'])
                assert rr['combined_lower_bound']<=fee
                if variant==1:assert rr['source_budget']['lower_bound']==k*(10**400+3)
                weighted.append(dict(k=k,variant=variant,lower=rr['combined_lower_bound'],explicit_upper=fee))
    return dict(separated_coordinate_controls=separated,shared_coordinate_controls=shared,
                weighted_rematching_controls=weighted,optimized_parameters=6)


def main():
    ex=enumerate_models();large=larger_models();sharp=sharp_controls();families=family_controls()
    out=dict(status='PASS',exhaustive=ex,larger=large,sharp_width_controls=sharp,families=families,
             exhaustive_models=sum(x['models'] for x in ex),
             seeded_models=sum(x['models'] for x in large),
             full_N_evaluations=sum(x['full_N_evaluations'] for x in ex+large)+4*len(list(all_matchings(grid(3,4)))),
             exact_frontier_comparisons=sum(x['models'] for x in ex+large)+4,
             brute_discount_comparisons=sum(x['models'] for x in ex+large)+4,
             scope='Pointwise static-cost identities and weighted source-budget lower bounds on independent full N, exact frontier and brute discount matching; both colours, empty T, zero/401-digit weights; two all-k families with 24 coordinate controls and flows for k<=6; 18 weighted/rematching controls.',
             proof_scope='General source-ownership identities, separated exactness and capacity-one HH discount lower bound are written proofs. Feasible all-k shared-source family has exact TH k and EVERY all-terminal minimizer TH 2k. Finite controls do not replace proofs. No Lean, generic-algorithm novelty or universal numerical improvement claimed.')
    (ROOT/'output/source-ownership-cost-bounds.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','exhaustive_models','seeded_models','full_N_evaluations','exact_frontier_comparisons','brute_discount_comparisons']}),flush=True)


if __name__=='__main__':main()
