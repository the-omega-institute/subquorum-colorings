"""Solver-free two-dead fork and exact support-shadow relay compensation.

General hypotheses/proof: TWO_SIDED_DEAD_ESCAPES_AND_SHADOW_RELAY.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import brute, whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O: assertions required.')

FIXTURE = Path(__file__).parent/'fixtures/frozen_two_dead_mixed_escapes.json'
ALPHA = (((5, 13), (10, 11)), ((5, 15), (7, 20)))
GATE = ((5, 14), (10, 14))
DEAD = (((5, 12), (5, 11)), ((5, 16), (5, 17)))


def fixture(q=1):
    j = json.loads(FIXTURE.read_text())
    move = lambda v, i: (v[0]+14*i, v[1])
    cur = (14*q, 28, {move(v, i) for i in range(q) for v in j['selected']},
           [tuple(move(v, i) for v in e) for i in range(q) for e in j['matching']])
    layers = [[move(v, i) for i in range(q) for v in layer] for layer in j['freezing_layers']]
    return cur, layers


def formula(Q, L, R, X, S, T, private_cost=1, shadow_cost=1, tail_cost=5):
    """Exact two-source relay class, under the hypotheses of Theorem 2."""
    assert S <= L
    assert all(not a & b for a, b in itertools.combinations((L, R, X, T), 2))
    l, r, x, s, t = [len(Q & p) for p in (L, R, X, S, T)]
    double = []
    for available, cost in ((l and r, 0), (l and x, private_cost),
                            (s and l >= 2, shadow_cost), (l and t, tail_cost),
                            (r and t, tail_cost), (x and t, private_cost+tail_cost)):
        if available:
            double.append(cost)
    if double:
        return 2, min(double)
    single = []
    for available, cost in ((l or r, 0), (x, private_cost),
                            (s, shadow_cost), (t, tail_cost)):
        if available:
            single.append(cost)
    return (1, min(single)) if single else (0, 0)


def inspect(cur, bands, layers, move=lambda v: v):
    direct_check(*cur)
    rank = check_rank_certificate(cur, layers)
    endpoints = {v for e in cur[3] for v in e}
    assert frozen_certificate(cur)[0] == endpoints
    d, meta, _ = whole_support_data(cur, bands)
    k0, components = independent_strands(cur, bands)
    kinds, pairs, links, W, I = d
    assert kinds == k0
    assert {frozenset(p) for p in pairs} == {tips for tips, body in components if tips}
    owner, A, B, M = owner_data(kinds, pairs)
    a, b = [owner[move(p[0])] for p in ALPHA]
    g = owner[move(GATE[0])]
    assert A == {a, b} and not B and len(M) == 10
    assert len(endpoints) == 56 and len(cur[2]) == 26
    for pair in (*ALPHA, GATE, *DEAD):
        assert frozenset(map(move, pair)) in {frozenset(p) for p in pairs}
    mate = {v: w for e in cur[3] for v, w in (e, e[::-1])}
    for c in (13, 14, 15):
        assert mate[move((5, c))] == move((6, c))
    for pair in DEAD:
        bp, tp = map(move, pair)
        o = owner[bp]
        assert o in M and kinds[bp] == 'BP' and kinds[tp] == 'TP'
        assert mate[bp] == tp and not W[o]
        assert next(body for tips, body in components if tips == frozenset((bp, tp))) == {bp, tp}
        assert not meta['all_ports'][bp] and not meta['all_ports'][tp]
        assert [(u, v) for u, v in links if u == tp] == [(tp, bp)]
    # All reachable nonself arcs, including the original other-tip bypass.
    expected = [((5,13),(5,12)), ((5,13),(5,14)),
                ((5,15),(5,14)), ((5,15),(5,16)),
                ((7,20),(7,21)), ((10,14),(10,15)),
                ((10,16),(10,17)), ((10,18),(10,19)), ((10,20),(10,21))]
    assert {(u,v) for u,v in links if owner[u] != owner[v]} == {
        tuple(map(move, e)) for e in expected}
    # Four distinct pools; S is a subset of L, not a second copy of its units.
    L, R = W[a], W[b]
    S = W[g]
    X = W[owner[move((7,21))]]
    T = W[owner[move((10,21))]]
    assert list(map(len, (L, R, X, S, T))) == [20, 3, 3, 2, 3]
    assert S <= L and all(not p & q for p,q in itertools.combinations((L,R,X,T),2))
    assert not any(W[owner[move((10,c))]] for c in (15,17,19))
    full = fork_flow(*d)
    assert (full['value'], full['cost']) == (2, 0)
    return d, (L,R,X,S,T), dict(endpoints=56, selected=26, alpha=2, beta=0, mixed=10,
        dead_forced_escapes=2, rank_witnesses=len(rank),
        full_value=2, full_cost=0,
        pools={name:[meta['intervals'][i] for i in sorted(pool)]
               for name,pool in zip(('L','R','X','S','T'), (L,R,X,S,T))})


def restrict(d, Q):
    return (*d[:3], {o:w & Q for o,w in d[3].items()}, Q)


def independent_relay_packing(Q, pools, costs):
    """Enumerate actual named units and one shared gate, separately from formula."""
    L,R,X,S,T = pools
    p,h,z = costs
    paths = [([(j,0,False) for j in Q & L] + [(j,h,True) for j in Q & S] + [(j,z,True) for j in Q & T]),
             ([(j,0,False) for j in Q & R] + [(j,p,False) for j in Q & X] +
              [(j,h,True) for j in Q & S] + [(j,z,True) for j in Q & T])]
    best=(0,0)
    for u,v in itertools.product([None]+paths[0], [None]+paths[1]):
        chosen=[path for path in (u,v) if path is not None]
        if len({path[0] for path in chosen}) != len(chosen):continue
        if sum(path[2] for path in chosen)>1:continue
        candidate=(len(chosen),sum(path[1] for path in chosen))
        if (candidate[0],-candidate[1])>(best[0],-best[1]):best=candidate
    return best


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    c,layers=fixture(); bands=whole_bands(c)
    d,pools,base=inspect(c,bands,layers)
    L,R,X,S,T=pools
    totals=Counter(); examples=[]
    # All 3^5 threshold patterns: S, L\S, R, X, T selected 0,1,2 each.
    # The proof, not these representatives, covers all subsets and identities.
    partitions=(S,L-S,R,X,T)
    for counts in itertools.product(range(3),repeat=5):
        Q=set().union(*(set(sorted(p)[:n]) for p,n in zip(partitions,counts)))
        expected=formula(Q,*pools)
        actual=fork_flow(*restrict(d,Q))
        assert (actual['value'],actual['cost']) == expected
        assert independent_relay_packing(Q,pools,(1,1,5)) == expected
        totals['physical_threshold_patterns']+=1
    rng=random.Random(20261025072)
    for _ in range(120):
        Q={j for j in d[4] if rng.random()<rng.choice((.02,.1,.5,.9))}
        actual=fork_flow(*restrict(d,Q)); expected=formula(Q,*pools)
        assert (actual['value'],actual['cost']) == expected
        totals['physical_random_full_pool_subsets']+=1
    # Physical terminal matchings cover all original owners, not a trimmed rule.
    controls=[set(d[4]),set(),set(T),set(S),{min(S),min(R)},
              {min(L-S),min(S)}, {min(T),min(X)}]
    for Q in controls:
        exact,n=brute(*restrict(d,Q)); assert exact==formula(Q,*pools)
        totals['independent_physical_terminal_models']+=1
        totals['independent_physical_terminal_matchings']+=n
        examples.append(dict(Q=sorted(Q),value=exact[0],cost=exact[1]))
    # General relay lemma: variable original set sizes and nonnegative costs.
    for _ in range(300):
        sizes=[rng.randrange(5) for i in range(4)]; cursor=0; groups=[]
        for n in sizes:groups.append(set(range(cursor,cursor+n)));cursor+=n
        LL,RR,XX,TT=groups; SS={j for j in LL if rng.random()<.5}
        Q={j for j in range(cursor) if rng.random()<.65}; costs=tuple(rng.randrange(7) for i in range(3))
        expected=formula(Q,LL,RR,XX,SS,TT,*costs)
        assert independent_relay_packing(Q,(LL,RR,XX,SS,TT),costs)==expected
        totals['abstract_variable_cost_relay_models']+=1
    images=[]
    for sym in itertools.product((False,True),repeat=3):
        shape,selected,matching=transformed(*c,*sym);move=image_map(*c[:2],sym)
        bs=[[tuple(map(move,e)) for e in band] for band in bands]
        ls=[list(map(move,layer)) for layer in layers]
        di,pi,ri=inspect((*shape,selected,matching),bs,ls,move)
        assert fork_flow(*restrict(di,pi[4]))['value']==1
        images.append(dict(symmetry=sym,value=ri['full_value'],cost=ri['full_cost']))
    stacks=[]
    for q in (2,3,5):
        cur,ls=fixture(q);direct_check(*cur);check_rank_certificate(cur,ls)
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        di,mi,_=whole_support_data(cur,whole_bands(cur));oi,Ai,Bi,Mi=owner_data(*di[:2])
        assert (len(Ai),len(Bi),len(Mi))==(2*q,0,10*q)
        full=fork_flow(*di);assert (full['value'],full['cost'])==(2*q,0)
        # Tail-only: >=2 distinct original units per copy still allow just one
        # payment, because every source-to-unit route uses its one G gate.
        Q=set().union(*(di[3][oi[10+14*i,21]] for i in range(q)))
        tail=fork_flow(*restrict(di,Q));assert (tail['value'],tail['cost'])==(q,5*q)
        stacks.append(dict(q=q,full_value=2*q,full_cost=0,tail_only_value=q,tail_only_cost=5*q))
    report=dict(status='PASS',base=base,counts=dict(totals),examples=examples,images=images,stacks=stacks,
        scope='Explicit beta-free frozen two-dead escape; exact all-original-pool-subset relay formula has a separate written proof. Tail-only deficits are declared resource exclusions; complete original pool pays all. No universal5/6 improvement. Lean scope recorded separately.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**dict(totals),full_value=2,full_cost=0,tail_only_value=1,tail_only_cost=5)))


if __name__=='__main__':main()
