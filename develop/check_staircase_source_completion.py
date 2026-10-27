"""Independent distances, source capacities and physical completion controls.

Finite checks test the implementation; the arbitrary-size result is proved in
docs/STAIRCASE_HH_BUDGET_EXACTNESS.md.
"""
from collections import Counter
from pathlib import Path
import json
import random

from staircase_source_completion import staircase_family,solve_staircase,expose_staircase_white
from check_mixed_terminal_compensation import all_matchings,edge,mates,neighbours,selected_feasible
from check_unbounded_hole_relay import family as isolated_core
from check_general_square_ports import physical_state
from check_corner_relay_shortest_path import flip_rematching
from monochromatic_completion_flow import solve_completion_flow
from terminal_source_budget import terminal_source_budget

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def forward_core_distances(f,m,weights):
    """Separate forward Bellman-Ford, with no production relay search calls."""
    result=[]
    for p,h in zip(f['parts'],f['centres']):
        targets={v for u in p for v in neighbours(u)&f['T']}
        allowed=p|targets|{h};arcs=[]
        for a,b in sorted(m):
            if a not in p:continue
            black,white=(a,b) if sum(a)%2==0 else (b,a)
            arcs.append((black,white,weights[edge(a,b)]))
        for a in sorted(v for v in allowed if sum(v)%2):
            arcs.extend((a,b,0) for b in sorted(neighbours(a)&allowed) if edge(a,b) not in m)
        dist={v:0 for v in targets}
        for _ in range(len(allowed)-1):
            changed=False
            for a,b,c in arcs:
                if a in dist and (b not in dist or dist[b]>dist[a]+c):
                    dist[b]=dist[a]+c;changed=True
            if not changed:break
        assert h in dist
        result.append(dist[h])
    return result


def generic_budget(f,m,weights):
    board=f['board'];p=set(mates(board,m));q=board-p;directed={v:[] for v in board};cost={}
    for a,b in sorted(m):
        black,white=(a,b) if sum(a)%2==0 else (b,a)
        directed[black].append(white);cost[black,white]=weights[edge(a,b)]
    for a in sorted(v for v in board if sum(v)%2):
        directed[a].extend(b for b in sorted(neighbours(a)&board) if edge(a,b) not in m)
    return terminal_source_budget(board,directed,f['T'],f['white_holes'],{v for v in q if sum(v)%2==0},cost)


def brute_discount(budget):
    reach=budget['reachable_discount_pairs'];holes=sorted(reach);ell=budget['terminal_lower_weights']
    def visit(i,used):
        if i==len(holes):return 0
        return max([visit(i+1,used)]+[ell[b]+visit(i+1,used|{b}) for b in reach[holes[i]]-used])
    return visit(0,set())


def check_geometry(f):
    scales=f['scales'];r=len(scales);s=sum(scales);half=f['height']*f['width']//2
    assert half==8*s*s+4*s*(r+1)+2*r
    assert len(f['M'])==8*sum(k*k for k in scales)+4*s
    assert len(f['T'])==half-len(f['M'])-(r-1)
    assert len(f['H'])==half-len(f['M'])+(r-1)
    assert len(f['M'])+len(f['T'])==half-(r-1)
    assert selected_feasible(f['P'],f['T'])
    assert {v for v in f['board']-f['P'] if sum(v)%2 and len(neighbours(v)&f['P'])>1}==f['white_holes']
    assert len(f['ordered_white_holes'])==r-1


def check_physical(result,independent=True):
    f=result['family'];m=result['M'];weights=result['weights']
    state=physical_state(f['board'],m,result['auxiliary'],f['T']) if independent else result['state']
    assert state['data']['counts'][0]==0
    assert state['data']['counts'][1]==len(f['white_holes'])
    assert state['paid']==result['TH_relay']['actual']
    assert sum(weights[e] for e in state['paid'])==result['minimum_TH_fee']==min(result['rho'])
    all_used=set();sources=set();all_cost=0
    for path in state['data']['paths']:
        assert not all_used&path['M'];all_used|=path['M']
        all_cost+=sum(weights[e] for e in path['M'])
        if path['kind']=='HH':
            white=next(v for v in (path['vertices'][0],path['vertices'][-1]) if sum(v)%2)
            assert white not in sources;sources.add(white)
    assert sources==f['white_holes']
    assert len({h for h,i in result['HH_assignment']})==len({i for h,i in result['HH_assignment']})==len(sources)
    return all_cost-result['minimum_TH_fee']


def outer_controls():
    rows=[]
    cases=[(1,),(2,),(1,1),(1,1,1),(2,1,3),(3,2,1),(1,2,1,1),(1,1,1,1,1),(1,3,1),(3,1,2,1)]
    for scales in cases:
        f=staircase_family(scales);check_geometry(f)
        region=f['board']-f['P']-set(f['centres'])-f['white_holes']
        white=sorted(v for v in region if sum(v)%2)
        for target in white:
            matching,path=expose_staircase_white(f,target)
            assert set(mates(region,matching))==region-{target}
            assert len(path)==len(set(path)) and len(path)%2==1
        rows.append(dict(scales=scales,outer_vertices=len(region),all_white_deletions=len(white)))
    return rows


def exhaustive_single_core_slices():
    """All 196 matchings in EACH of three positions, others canonical.

    This is deliberately not described as all 196**3 joint rematchings.
    """
    raw=[set(m) for m in all_matchings(isolated_core(1)['P'])];assert len(raw)==196
    f=staircase_family((1,1,1));hist=Counter();count=0
    for varied,(row,col) in enumerate(f['origins']):
        fixed={e for e in f['M'] if e[0] not in f['parts'][varied]}
        for local in raw:
            move=lambda v:(v[0]+row,v[1]+col)
            m=fixed|{edge(move(a),move(b)) for a,b in local};weights={e:1 for e in m}
            result=solve_staircase(f['scales'],m,weights)
            reference=forward_core_distances(f,m,weights)
            assert result['rho']==reference;check_physical(result)
            hist[tuple(reference)]+=1;count+=1
        print('single-core exhaustive slice',varied,count,flush=True)
    return dict(core_matchings=196,positions=3,models=count,
                rho_histogram=[dict(rho=key,count=value) for key,value in sorted(hist.items())],
                scope='All 196 rematchings at each of three positions separately; other cores fixed canonical. Not all joint triples.')


def transpose_cores(f,m):
    origins={v:origin for p,origin in zip(f['parts'],f['origins']) for v in p}
    def move(v):
        r,c=origins[v];return (r+v[1]-c,c+v[0]-r)
    return {edge(move(a),move(b)) for a,b in m}


def weighted_controls():
    rng=random.Random(27102745);rows=[]
    cases=[(1,),(1,1),(1,1,1),(2,1,3),(3,2,1),(1,2,1,1),(1,1,1,1,1)]
    for scales in cases:
        f=staircase_family(scales);r=len(scales)
        owner={v:i for i,p in enumerate(f['parts']) for v in p}
        for variant in range(4+r):
            m=flip_rematching(f['M'],f['P'],rng,120*(variant+1))
            if variant%2:m=transpose_cores(f,m)
            weights={e:rng.randrange(23) for e in sorted(m)}
            forced=None
            if variant==0:weights={e:1 for e in m}
            elif variant==1:weights={e:0 for e in m}
            elif variant==2:weights={e:10**400+7*j for j,e in enumerate(sorted(m))}
            elif variant>=4:
                forced=variant-4;weights={e:1 if owner[e[0]]==forced else 10**6 for e in m}
            result=solve_staircase(scales,m,weights);reference=forward_core_distances(f,m,weights)
            assert result['rho']==reference
            budget=generic_budget(f,m,weights)
            assert [budget['terminal_lower_weights'][h] for h in f['centres']]==reference
            assert budget['lower_bound']==result['minimum_TH_fee']==min(reference)
            assert budget['max_discount']==brute_discount(budget)==sum(reference)-min(reference)
            assert not budget['unreachable_from_T']
            phi=budget['potential'];assert all(c+phi[a]-phi[b]>=0 for a,b,cap,c in budget['residual_arcs'] if cap)
            hh_cost=check_physical(result)
            if forced is not None:assert result['paid_core']==forced
            rows.append(dict(scales=scales,variant=variant,changed_M=m!=f['M'],rho=reference,
                             exact_TH_fee=result['minimum_TH_fee'],budget_lower=budget['lower_bound'],
                             paid_core=result['paid_core'],forced_paid_core=forced,HH_actual_expense=hh_cost,
                             HH_assignment=result['HH_assignment']))
    return rows


def canonical_controls():
    rows=[]
    for scales in [(1,),(1,1),(1,1,1),(2,1,3),(1,2,1,1),(1,1,1,1,1)]:
        f=staircase_family(scales);check_geometry(f);s=solve_staircase(scales)
        assert s['rho']==list(scales) and s['minimum_TH_fee']==min(scales)
        c=physical_state(f['board'],f['M'],f['canonical_C_auxiliary'],f['T'])
        c_cost=sum(len(path['M']) for path in c['data']['paths'])
        assert c_cost==len(c['paid'])==sum(scales)
        row=dict(scales=scales,TH_optimum=min(scales),canonical_C=sum(scales),flow_checked=False)
        if sum(scales)<=4:
            flow=solve_completion_flow(f['height'],f['width'],f['M'],f['T'])
            assert flow['all_terminal_cost']==flow['TH_fee']==sum(scales)
            phi=flow['potential'];assert all(cost+phi[a]-phi[b]>=0 for a,b,cap,cost in flow['residual_arcs'] if cap)
            row['flow_checked']=True
        rows.append(row)
    return rows


def large_controls():
    rows=[]
    for scales in [(1,)*20,(8,1,4,2,6),(32,1,1),(2,)*16]:
        result=solve_staircase(scales);f=result['family'];check_geometry(f)
        assert result['rho']==list(scales) and result['minimum_TH_fee']==min(scales)
        check_physical(result,independent=False)
        rows.append(dict(scales=scales,height=f['height'],width=f['width'],TH_optimum=min(scales)))
    return rows


def main():
    outer=outer_controls();slices=exhaustive_single_core_slices();weighted=weighted_controls()
    canonical=canonical_controls();large=large_controls()
    out=dict(status='PASS',outer=outer,single_core_exhaustive_slices=slices,weighted=weighted,canonical=canonical,large=large,
             all_white_outer_deletion_checks=sum(r['all_white_deletions'] for r in outer),
             weighted_rematching_models=len(weighted),changed_weighted_matchings=sum(r['changed_M'] for r in weighted),
             independent_generic_budget_and_brute_discount_comparisons=len(weighted),
             forced_paid_core_models=sum(r['forced_paid_core'] is not None for r in weighted),
             scope='All white outer deletions on ten footprints; all single-core rematching slices at three positions; forward Bellman-Ford core distances; independent old physical decomposition; generic HH budget, brute discount matching, residual potentials; zero and 401-digit weights; forced left, right and interior paid cores; canonical C witnesses and small full min-cost flows; four large chains.',
             proof_scope='Arbitrary r, scales, rematchings and nonnegative-real weights follow from the written relay, outer deletion and capacity-one completion proofs. Finite checks validate implementations. No new Lean or universal 5/6 claim.')
    (ROOT/'output/staircase-source-exact-completion.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','all_white_outer_deletion_checks','weighted_rematching_models','changed_weighted_matchings','independent_generic_budget_and_brute_discount_comparisons','forced_paid_core_models']}),flush=True)


if __name__=='__main__':main()
