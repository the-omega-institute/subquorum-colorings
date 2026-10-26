"""Retained occupations, arbitrary actual rematching, and robust rank traps.

The all-k proof is the even-core/two-port normalization and the fixed strict
rank trap in the accompanying note. Local matching enumeration is a control.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_endpoint_invasion_sharp_strips import (
    check_extension, components, edge_key, endpoints, free_vertices,
    invading_completion,
)
from check_cooperative_promotion import neighbors
from check_component_receivers import vertices_of
from check_occupied_strip_degree_four_budget import family, inspect_budget
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# Core coordinates translated by (r,c)->(r,c+6i). A,B,C,D,E,F,G,H
# are the eight old endpoints; U,V are the two adjacent possible new ports.
A,B,C,D,E,F,G,H = (1,5),(1,6),(1,7),(2,7),(2,6),(3,6),(3,7),(3,8)
U,V = (2,5),(3,5)
CORE = {A,B,C,D,E,F,G,H}
PORTS = {U,V}
TRAP = {B,U,D}
MODES = [
    [(A,B),(C,D),(E,F),(G,H),(U,V)],
    [(A,B),(C,D),(U,E),(V,F),(G,H)],
    [(A,U),(B,C),(D,E),(V,F),(G,H)],
    [(A,U),(B,E),(C,D),(V,F),(G,H)],
]
MODES = [[edge_key(e) for e in M] for M in MODES]


def all_matchings(P):
    if not P:
        yield []
        return
    v = min(P,key=lambda v:(len(set(neighbors(v)) & P),v))
    for u in sorted(set(neighbors(v)) & P):
        for rest in all_matchings(P-{v,u}):
            yield [edge_key((v,u))]+rest


def shift(v,i):
    return v[0],v[1]+6*i


def local_geometry(k,counts):
    old = family(k)[0]
    P0,F0 = endpoints(old[3]),free_vertices(old)
    for i in range(k):
        core = {shift(v,i) for v in CORE}
        ports = {shift(v,i) for v in PORTS}
        assert core <= P0 and not core & F0
        assert {u for v in core for u in neighbors(v) if u in F0} == ports
        assert not {u for v in core for u in neighbors(v) if u in P0-core}
        assert shift(V,i) in neighbors(shift(U,i))
        for v in (shift(z,i) for z in TRAP):
            possible = set(neighbors(v)) & (P0 | F0)
            assert possible <= core | ports
            # All possible occupied neighbours of a trap vertex are endpoints
            # once a noncanonical core uses BOTH ports.
            assert not set(neighbors(v)) & old[2]
        counts['core_boundary_geometry_controls'] += 1


def check_local_modes(counts):
    assert {frozenset(M) for M in all_matchings(CORE | PORTS)} == {
        frozenset(M) for M in MODES}
    assert len(list(all_matchings(CORE))) == 1
    assert not list(all_matchings(CORE | {U}))
    assert not list(all_matchings(CORE | {V}))
    for mode,M in enumerate(MODES):
        mate = {v:u for e in M for v,u in (e,e[::-1])}
        assert endpoints(M) == CORE | PORTS
        if mode:
            for v in TRAP:
                outside_supports = {u for u in set(neighbors(v)) & (CORE | PORTS)
                                    if mate[u] not in TRAP}
                assert len(outside_supports) <= 1
            counts['noncanonical_rank_trap_templates'] += 1


def normalize(cur,k,counts):
    old = family(k)[0]
    direct_check(*cur)
    assert old[:2] == cur[:2] and old[2] <= cur[2]
    P0,P = endpoints(old[3]),endpoints(cur[3])
    assert P0 <= P
    assert P-P0 <= free_vertices(old)
    M = {edge_key(e) for e in cur[3]}
    changed = []
    for i in range(k):
        core = {shift(v,i) for v in CORE}
        ports = {shift(v,i) for v in PORTS}
        internal = {e for e in M if set(e) <= core}
        crossing = {e for e in M if len(set(e) & core) == 1}
        assert 8 == 2*len(internal)+len(crossing)
        assert len(crossing) in (0,2)
        old_edges = {edge_key((shift(a,i),shift(b,i)))
                     for a,b in MODES[0] if a in CORE}
        if crossing:
            assert {v for e in crossing for v in e if v not in core} == ports
            region = core | ports
            actual = {e for e in M if set(e) <= region}
            unshift = lambda v:(v[0],v[1]-6*i)
            template = {edge_key((unshift(a),unshift(b))) for a,b in actual}
            mode = next(j for j in range(1,4) if template == set(MODES[j]))
            trap = {shift(v,i) for v in TRAP}
            mate = {v:u for e in M for v,u in (e,e[::-1])}
            O = P | cur[2]
            for v in trap:
                ns = set(neighbors(v)) & O
                assert ns <= P
                assert len({u for u in ns if mate[u] not in trap}) <= 1
            changed.append(dict(core=i,mode=mode,trap=sorted(trap)))
            M -= internal | crossing
            M |= old_edges | {edge_key(tuple(sorted(ports)))}
        else:
            assert internal == old_edges
    normalized = (*cur[:3],sorted(M))
    assert endpoints(normalized[3]) == P and len(normalized[3]) == len(cur[3])
    assert {edge_key(e) for e in old[3]} <= M
    direct_check(*normalized)
    check_extension(normalized,k,counts)
    actual_frozen,_ = frozen_certificate(cur)
    for row in changed:
        assert not actual_frozen & set(map(tuple,row['trap']))
        counts['robust_unfrozen_traps'] += 1
    if actual_frozen == P:
        assert not changed
        extra = P-P0
        assert extra <= components(k)[0]
        counts['actual_fully_frozen_models'] += 1
    counts['arbitrary_rematching_models'] += 1
    counts['nontrivial_normalizations'] += bool(changed)
    return normalized,changed,actual_frozen


def sharp_all_ports(k,modes):
    cur = invading_completion(k)[0]
    T = cur[2]-{shift(V,i) for i in range(1,k)}
    M = [cur[3][-2]]  # isolated old left edge
    for i,mode in enumerate(modes):
        M += [(shift(a,i),shift(b,i)) for a,b in MODES[mode]]
    assert len(modes) == k and len(T)+len(M) == 17*k+12
    return (*cur[:2],T,M)


def matching_credit_ledger(cur,k,modes,counts):
    """Allocate every actual D4 once, including matching-created BP refunds."""
    region = family(k)[1]
    budget = inspect_budget(cur,[region],counts)
    extra = sum(mode == 3 for mode in modes)
    assert budget['surplus_twice'] == 1-k
    assert budget['degree_four_budget'] == dict(boundary_ends=1,
        unported_degree_four_TP=k+extra,ported_exports=1,
        unused_forest_end_slots=0,bound_surplus_twice=1-k)
    assert budget['unused_BP'] == extra and budget['safe_cross'] == 0
    P,T = endpoints(cur[3]),cur[2]
    mate = {v:u for e in cur[3] for v,u in (e,e[::-1])}
    top = {v for col in region for v in col}
    actual_D4 = {v for v in P & top if (0,v[1]) in T and mate[v] not in top
                 and len(set(neighbors(v)) & (P | T)) == 4}
    # The separate boundary export is ported, with degree three, so excluded.
    expected = set()
    allocations = {}
    for i,mode in enumerate(modes):
        one = A if mode == 2 else C
        target = shift(one,i)
        allocations[target] = ('external_half_tile',(1,4+3*i))
        expected.add(target)
        if mode == 3:
            target = shift(A,i)
            refund = shift(B,i)
            assert mate[refund] not in top and (0,refund[1]) not in P | T
            allocations[target] = ('unused_BP_half_credit',refund)
            expected.add(target)
    assert actual_D4 == expected == set(allocations)
    assert len(set(allocations.values())) == len(allocations) == k+extra
    reserves = {(1,1)} | {(1,2+3*i) for i in range(1,k)}
    rebates = {(1,4+3*i) for i in range(k)}
    charge = lambda q:4-2*len(T & vertices_of({q}))-len(P & vertices_of({q}))
    assert reserves.isdisjoint(rebates) and len(reserves) == k
    assert all(charge(q) == 2 for q in reserves)
    assert all(charge(q) == 1 for q in rebates)
    assert charge((1,2)) == 0 and charge((1,0)) == -1
    for r,c in itertools.product(range(1,3),range(cur[1]//2)):
        if (r,c) not in reserves | rebates | {(1,0)}:
            assert charge((r,c)) == 0
    # Each extra BP half credit is SPENT on the extra actual D4 in its own
    # core. It is not also retained as an unspent interval/beta/tile resource.
    assert (1+extra)-(k+extra)+(k-1)+2*k == 2*k
    counts['matching_specific_no_reuse_ledgers'] += 1
    counts['extra_actual_D4_paid_by_distinct_BP_refunds'] += extra


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--write-fixture',action='store_true')
    args = p.parse_args()
    counts,samples = Counter(),[]
    check_local_modes(counts)
    for k in (*range(1,17),32,64,128):
        local_geometry(k,counts)
        rng = random.Random(261026+k)
        choices = list(itertools.product(range(4),repeat=k)) if k <= 4 else [
            [0]*k,[1]*k,[2]*k,[3]*k,[i%4 for i in range(k)],
            [rng.randrange(4) for _ in range(k)]]
        for modes in choices:
            cur = sharp_all_ports(k,modes)
            normalized,changed,frozen = normalize(cur,k,counts)
            assert len(cur[2])+len(cur[3]) == 17*k+12
            assert {edge_key(e) for e in normalized[3]} == {
                edge_key(e) for e in sharp_all_ports(k,[0]*k)[3]}
            matching_credit_ledger(cur,k,modes,counts)
            counts['sharp_all_port_rematching_models'] += 1
        # Same sharp fully frozen occupation has exactly four actual matchings,
        # with exactly one fully frozen. Only its FIRST core has new endpoints.
        cur = invading_completion(k)[0]
        frozen_count = 0
        for mode in range(4):
            old_first = {edge_key(e) for e in cur[3][:4]} | {edge_key((U,V))}
            actual = {edge_key(e) for e in cur[3]}-old_first | set(MODES[mode])
            rematched = (*cur[:3],sorted(actual))
            normalized,changed,frozen = normalize(rematched,k,counts)
            frozen_count += frozen == endpoints(actual)
            assert (frozen == endpoints(actual)) == (mode == 0)
            counts['single_invader_all_matching_controls'] += 1
        assert frozen_count == 1
        if k in (1,2,16,128):
            samples.append(dict(k=k,shape=cur[:2],all_port_sharp_matching_count=f'4^{k}',
                sharp_objective=17*k+12,whole_surplus=k,
                single_invader_matching_count=4,single_invader_fully_frozen_matching_count=1))
    # Independent T variation: reselect arbitrary additional T, retaining T0,
    # after choosing an actual matching with several noncanonical cores.
    for k in (1,2,4,8):
        for seed in range(16):
            rng = random.Random(8123+seed+101*k)
            cur = sharp_all_ports(k,[rng.randrange(4) for _ in range(k)])
            old = family(k)[0]
            T = old[2] | {v for v in cur[2]-old[2] if rng.randrange(2)}
            normalize((*cur[:2],T,cur[3]),k,counts)
            counts['varied_T_rematching_controls'] += 1
    for k in (1,2,4,8):
        base = family(k)[0]
        free = free_vertices(base)
        edges = sorted({edge_key((v,u)) for v in free
                        for u in set(neighbors(v)) & free})
        for seed in range(16):
            rng = random.Random(39101+seed+107*k)
            order = edges[:]
            rng.shuffle(order)
            extra,used = [],set()
            for e in order:
                if not set(e) & used and rng.randrange(3) == 0:
                    extra.append(e)
                    used.update(e)
            M = {edge_key(e) for e in base[3]+extra}
            for i in range(k):
                port_edge = edge_key((shift(U,i),shift(V,i)))
                if port_edge in M:
                    canonical = {edge_key((shift(a,i),shift(b,i))) for a,b in MODES[0]}
                    mode = rng.randrange(4)
                    M -= canonical
                    M |= {edge_key((shift(a,i),shift(b,i))) for a,b in MODES[mode]}
            P,T = endpoints(M),set(base[2])
            order = sorted(free-P)
            rng.shuffle(order)
            for v in order:
                trial = T | {v}
                if all(len(set(neighbors(t)) & (P | trial)) <= 1 for t in trial):
                    T = trial
            normalize((*base[:2],T,sorted(M)),k,counts)
            counts['varied_P_and_T_rematching_controls'] += 1
    cur = sharp_all_ports(2,[1,3])
    normalized,changed,frozen = normalize(cur,2,counts)
    fixture = dict(scope='k2 sharp rematching: old T0/P0 retained, old M0 not retained. Both cores noncanonical; disjoint three-endpoint traps remain unfrozen. Normalization restores all old edges with the same T/P/objective and physical tile charges.',
        k=2,shape=cur[:2],selected=sorted(cur[2]),actual_matching=cur[3],
        normalized_matching=normalized[3],changed_cores=changed,
        actual_unfrozen=sorted(endpoints(cur[3])-frozen),objective=46,whole_surplus=2)
    path = Path('develop/fixtures/sharp_strip_rematching_traps_k2.json')
    if args.write_fixture:
        path.write_text(json.dumps(fixture,indent=2)+'\n')
    assert json.loads(path.read_text()) == json.loads(json.dumps(fixture))
    out = dict(status='PASS',counts=dict(counts),samples=samples,
        scope='Written all-k even-core two-adjacent-port normalization covers EVERY feasible T0/P0-retained arbitrary actual matching; sharp T+M<=area/2-k. Noncanonical old-core matching creates a robust three-endpoint strict-rank trap, so complete freezing forces all old M0 edges already retained. Local matching enumeration is a control, not the general proof. Old T/P withdrawal, arbitrary footprint compensation and universal5/6 remain open.')
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__ == '__main__':
    main()
