"""Independent output-rank/parity audit, not an algorithmic complexity proof.

The general argument is in docs/MIXED_RESOURCE_DUAL_PARITY.md. Only stdlib;
Edmonds--Karp rank oracle is separate from the existing min-cost fork flow
and primitive-pack DP. All three are compared, including original sources.
"""
import argparse
from collections import Counter, deque
import itertools
import json
from pathlib import Path
import random

from check_capacity_two_gate_bundles import physical
from check_canonical_band_coarsening import forests
from check_compensation_flow_normal_form import owner_data
from check_degree_changing_bent_completions import compile_model
from check_destructive_exchange_choice import constrained_optimum
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_P_free_pivot_interface import regions
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical, optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def subsets(items):
    items = list(items)
    return [frozenset(x for i, x in enumerate(items) if mask >> i & 1)
            for mask in range(1 << len(items))]


def network(data):
    kinds, pairs, links, support, resources = data
    own, A, B, M = owner_data(kinds, pairs)
    arcs = []
    def add(u, v, c):
        arcs.append((u, v, c))
    exit = lambda o: ('a', o) if o in A else ('out', o) if o in M else ('b', o)
    for a in sorted(A):
        add(('s',), exit(a), 1)
    for m in sorted(M):
        add(('in', m), exit(m), 1)
    for b in sorted(B):
        for tip in pairs[b]:
            add(('tip', tip), exit(b), 1)
        add(exit(b), ('output', ('beta', b)), len(A) + 1)
    for p, q in sorted(set(links)):
        assert kinds[p] == 'TP' and kinds[q] == 'BP'
        if own[p] != own[q]:
            add(exit(own[p]), ('tip', q) if own[q] in B else ('in', own[q]), len(A) + 1)
    for o, W in support.items():
        for j in sorted(W):
            add(exit(o), ('output', ('interval', j)), len(A) + 1)
    ground = {('interval', j) for j in resources} | {('beta', b) for b in B}
    for e in sorted(ground):
        add(('output', e), ('t',), 1)
    return arcs, ground


def rank(arcs, allowed):
    """Maximum flow with exactly the specified output-sink arcs enabled."""
    ids = {}; adj = []; edges = []
    def node(x):
        if x not in ids:
            ids[x] = len(ids); adj.append([])
        return ids[x]
    s = node(('s',)); t = node(('t',))
    for u, v, c in arcs:
        if v == ('t',) and u[1] not in allowed:
            continue
        a, b = node(u), node(v); i = len(edges)
        adj[a].append(i); adj[b].append(i + 1)
        edges.extend([[a, b, c], [b, a, 0]])
    value = 0
    while True:
        parent = {s: None}; todo = deque([s])
        while todo and t not in parent:
            u = todo.popleft()
            for i in adj[u]:
                _, v, cap = edges[i]
                if cap and v not in parent:
                    parent[v] = i; todo.append(v)
        if t not in parent:
            return value
        v = t
        while v != s:
            i = parent[v]; edges[i][2] -= 1; edges[i ^ 1][2] += 1
            v = edges[i][0]
        value += 1


def audit_all_cuts(data, groups, counts):
    arcs, U = network(data); r = rank(arcs, U)
    nodes = {v for u,w,c in arcs for v in (u,w)} - {('s',),('t',)}
    assert len(nodes) <= 12
    cuts = []
    for subset in subsets(sorted(nodes)):
        Z = set(subset) | {('s',)}
        capacity = sum(c for u,v,c in arcs if u in Z and v not in Z)
        I = {u[1][1] for u,v,c in arcs if v == ('t',) and
             u in Z and u[1][0] == 'interval'}
        assert capacity >= r
        cuts.append((capacity,I))
    for closed in subsets(range(len(groups))):
        X = set().union(set(), *(set(groups[i]) for i in closed))
        after = rank(arcs,U-{('interval',j) for j in X})
        assert after == min(c-len(X & I) for c,I in cuts)
        assert (after == r) == all(len(X & I) <= c-r for c,I in cuts)
        counts['all_cut_deletion_ledger_checks'] += len(cuts)


def state(data, groups, selected):
    closed = set().union(set(), *(set(g) for i, g in enumerate(groups) if i not in selected))
    return (*data[:3], {o: W - closed for o, W in data[3].items()}, data[4])


def verify(data, groups, weights, counts, axioms=False):
    assert all(1 <= len(g) <= 2 for g in groups)
    assert sum(map(len, groups)) == len(set().union(set(), *map(set, groups)))
    assert all(isinstance(w, int) and w >= 0 for w in weights)
    arcs, ground = network(data)
    pairs = [frozenset([('interval', j) for j in g] +
                       ([('dummy', i)] if len(g) == 1 else [])) for i, g in enumerate(groups)]
    U = ground | set().union(set(), *pairs)
    r = rank(arcs, U); rank_cache = {}
    def rk(S):
        S = frozenset(S)
        if S not in rank_cache:
            rank_cache[S] = rank(arcs, S)
        return rank_cache[S]
    def dual(S):
        return len(S) - r + rk(U - S)
    if axioms:
        allsets = subsets(sorted(U)); independent = [S for S in allsets if rk(S) == len(S)]
        for S in allsets:
            assert 0 <= rk(S) <= len(S)
            for e in U - S:
                assert rk(S) <= rk(S | {e}) <= rk(S) + 1
                for f in U - S - {e}:
                    assert rk(S | {e}) + rk(S | {f}) >= rk(S) + rk(S | {e, f})
                    counts['rank_local_submodular_checks'] += 1
            assert (dual(S) == len(S)) == (rk(U - S) == r)
        for S in independent:
            for T in independent:
                if len(S) < len(T):
                    assert any(rk(S | {e}) == len(S) + 1 for e in T - S)
                    counts['independent_exchange_checks'] += 1
        counts['complete_ground_set_axiom_audits'] += 1
    J = set(range(len(groups))); candidates = []; parity = []
    _, A, _, mixed = owner_data(*data[:2])
    old = state(data, groups, set())
    feasible_old = [P for P in subsets(sorted(A)) if constrained_optimum(old, P) is not None]
    for selected in subsets(sorted(J)):
        d = state(data, groups, selected); f = fork_flow(*d); p = optimize(*d)
        assert (f['value'], f['cost']) == (p['value'], p['cost'])
        fee = sum(weights[j] for j in selected)
        candidates.append((f['value'], fee, selected))
        closed = J - selected
        X = set().union(set(), *(pairs[j] for j in closed))
        assert rk(U - X) == f['value']
        if dual(X) == len(X):
            parity.append((sum(weights[j] for j in closed), closed))
        counts['rank_vs_full_flow_vs_primitive_states'] += 1
        counts['states_with_beta_forks'] += any(p['kind']=='fork' for p in f['certificates'])
        counts['states_using_mixed_relays'] += any(set(p['owners']) & mixed for p in f['certificates'])
        counts['states_with_routing_deficit'] += f['value'] < len(A)
    best = max(candidates, key=lambda x: (x[0], -x[1]))
    saving, closed = max(parity, key=lambda x: x[0])
    assert best[:2] == (r, sum(weights) - saving)
    chosen = J - closed
    for P in feasible_old:
        protected = constrained_optimum(state(data, groups, chosen), P)
        assert protected is not None and protected[0] == r
        # The SAME fee-optimal state retains every old feasible source set.
        counts['same_optimum_fee_old_source_set_checks'] += 1
        counts['nonempty_old_source_set_checks'] += bool(P)
    counts['weighted_dual_parity_comparisons'] += 1
    return dict(value=r, minimum_fee=best[1], closed=sorted(closed),
                ground_elements=len(U), resource_rank=r)


def physical_audit(counts):
    cur, bits, ranks, gates = physical()
    bits[4, 12] = bits[4, 44] = True
    gates += [(4, 12), (4, 44)]
    P = {v for e in cur[3] for v in e}
    direct_check(*cur)
    assert len(check_rank_certificate(cur, ranks)) == 140
    assert frozen_certificate(cur)[0] == P
    assert all(not {(r+i, c+j) for i, j in itertools.product(range(2), repeat=2)} & P for r, c in gates)
    records = []; rows = []
    for mask in range(32):
        changed = dict(bits)
        for i, tile in enumerate(gates):
            changed[tile] = not bool(mask >> i & 1)
        regs = regions(cur, changed); data, components, _ = compile_model(cur, regs); fs = forests(cur, regs)
        cells = {fs[j][1] for j in data[4]}
        support = {o: {fs[j][1] for j in W} for o, W in data[3].items()}
        own, A, B, M = owner_data(*data[:2])
        aL, aR, bL, bR, zL, zR = [own[x] for x in [(3,12),(3,45),(5,17),(5,40),(5,15),(5,42)]]
        assert (len(A), len(B), len(M)) == (4,4,10) and A == {aL,aR,bL,bR}
        assert zL in M and zR in M
        external = {(p,q) for p,q in data[2] if own[p] != own[q]}
        assert {(p,q) for p,q in external if own[p] in A | {zL,zR}} == {((5,17),(5,16)),((5,40),(5,41))}
        assert not support[bL] and not support[bR]
        f = fork_flow(*data); p = optimize(*data)
        assert (f['value'], f['cost']) == (p['value'], p['cost'])
        selected = {i for i in range(5) if mask >> i & 1}
        direct = 2 if 0 in selected or {1,2} <= selected else int(bool(selected & {1,2}))
        assert (f['value'], f['cost']) == (direct + int(3 in selected) + int(4 in selected),
                                             int(3 in selected) + int(4 in selected))
        records.append((data, components, cells, support))
        rows.append(dict(mask=mask, selected=sorted(selected), value=f['value'], links=f['cost']))
    base = records[0]; full = records[-1]; lost=[]; new=[]
    for i in range(5):
        rec = records[1 << i]
        lost.append(base[2] - rec[2]); new.append(rec[2] - base[2])
        assert len(lost[i]) == len(new[i]) == (2 if i == 0 else 1)
        assert all(not any(c in W for W in base[3].values()) for c in lost[i])
    assert sum(map(len,lost)) == len(set().union(*lost)) == 6
    assert sum(map(len,new)) == len(set().union(*new)) == 6
    target = [{aL,aR},{aL},{aR},{zL},{zR}]
    assert all(not base[3][o] for o in (aL,aR,zL,zR))
    for mask, (data, components, cells, support) in enumerate(records):
        chosen = {i for i in range(5) if mask >> i & 1}
        assert data[:2] == base[0][:2] and set(data[2]) == set(base[0][2])
        assert [x['body'] for x in components] == [x['body'] for x in base[1]]
        assert len(cells) == 228 == 16*58//2-166-70
        assert cells == (base[2] - set().union(set(), *(lost[i] for i in chosen))) | set().union(set(), *(new[i] for i in chosen))
        for o in support:
            expected = base[3][o] | set().union(set(), *(new[i] for i in chosen if o in target[i]))
            assert support[o] == expected
        counts['physical_all_subset_exact_adapters'] += 1
    # Label the active cells once; inactive unsupported cells are identified
    # through the proved disjoint replacement adapter, never extra inventory.
    labels = {c:j for j,c in enumerate(sorted(full[2], key=lambda c: sorted(c)))}
    data = (*full[0][:3], {o:{labels[c] for c in W} for o,W in full[3].items()}, set(labels.values()))
    groups = [[labels[c] for c in sorted(S, key=lambda c:sorted(c))] for S in new]
    costs = []
    for weights in [(1,1,1,1,1),(3,2,2,4,5),(5,1,1,0,0),(0,0,0,2,3)]:
        result = verify(data, groups, weights, counts)
        expected = max(((row['value'], sum(weights[i] for i in row['selected'])) for row in rows), key=lambda x:(x[0],-x[1]))
        assert (result['value'], result['minimum_fee']) == expected
        costs.append(dict(weights=weights, **result))
    counts['physical_strict_freeze_events'] += 140
    return dict(shape=[16,58], T=166, matching=70, frozen_endpoints=140,
                alpha=4,beta=4,mixed=10,raw_inventory=228,
                group_capacities=[2,1,1,1,1],gates=gates,states=rows,cost_profiles=costs)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); counts=Counter(); controls={}
    # Reachability would allow two assignments through one mixed owner.
    kinds,pairs,_=canonical('AAM')
    data=(kinds,pairs,[(0,4),(2,4)],{0:set(),1:set(),2:{0,1}},{0,1})
    assert rank(*network(data)) == 1
    controls['shared_mixed_gate']=verify(data,[[0,1]],[3],counts,True)
    audit_all_cuts(data,[[0,1]],counts)
    assert controls['shared_mixed_gate']['value'] == 1
    kinds,pairs,_=canonical('AAB')
    for name,links,expected in [('same_beta_BP',[(0,4),(2,4)],1),('distinct_beta_BPs',[(0,4),(2,5)],2)]:
        data=(kinds,pairs,links,{0:set(),1:set(),2:{0}},{0})
        controls[name]=verify(data,[[0]],[2],counts,True)
        audit_all_cuts(data,[[0]],counts)
        assert controls[name]['value'] == expected
    # An independent output set is not necessarily a normalized pack's
    # identical output set: two beta intervals can become beta + one interval.
    data=(kinds,pairs,[(0,4),(2,5)],{0:set(),1:set(),2:{0,1}},{0,1})
    arcs,U=network(data)
    assert rank(arcs,{('interval',0),('interval',1)})==2
    controls['beta_output_identity_normalization']=verify(data,[[0,1]],[3],counts,True)
    assert all(p['kind']=='fork' and p['value']==2 for p in fork_flow(*data)['certificates'])
    audit_all_cuts(data,[[0,1]],counts)
    # Feasible closed groups are NOT themselves a matroid: {0} cannot
    # augment toward {1,2}, although both are feasible closed sets.
    kinds,pairs,_=canonical('AA')
    data=(kinds,pairs,[],{0:{0,2},1:{1,3}},{0,1,2,3})
    arcs,U=network(data); gs=[{0,1},{2},{3}]
    feasible=lambda T:rank(arcs,U-{('interval',j) for i in T for j in gs[i]})==2
    assert feasible({0}) and feasible({1,2}) and not feasible({0,1}) and not feasible({0,2})
    controls['closed_group_exchange_failure']=verify(data,gs,[3,2,2],counts,True)
    audit_all_cuts(data,gs,counts)
    assert controls['closed_group_exchange_failure']['minimum_fee']==3
    counts['closed_group_greedy_obstructions']+=1
    rng=random.Random(20261026)
    for index in range(100):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible)
        links=possible[:rng.randrange(min(9,len(possible))+1)]
        resources=set(range(rng.randrange(1,5)))
        support={o:{j for j in resources if rng.randrange(2)} for o in range(len(pairs))}
        remaining=sorted(resources);groups=[]
        while remaining:
            size=rng.randrange(1,min(2,len(remaining))+1)
            groups.append(remaining[:size]);remaining=remaining[size:]
        # Some original units remain free/unpaired.
        if index%3==0:groups.pop()
        weights=[rng.randrange(5) for _ in groups]
        verify((kinds,pairs,links,support,resources),groups,weights,counts,axioms=index<35)
        counts['random_mixed_beta_models']+=1
    physical_result=physical_audit(counts)
    report=dict(status='PASS',counts=dict(counts),controls=controls,physical=physical_result,
        scope='Independent output-rank maxflow, existing full mincost fork flow, independent primitive DP; exhaustive small-ground rank/exchange/dual deletion checks and fee-optimal old-source retention; full 32-state physical adapter.',
        limits='Finite checks validate the written general proof, not replace it. No general polynomial oracle-parity algorithm, no global minimum-link tertiary objective, no universal 5/6 improvement, no end-to-end Lean claim.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['counts'],indent=2));print('PASS: mixed resource dual parity')

if __name__=='__main__':
    main()
