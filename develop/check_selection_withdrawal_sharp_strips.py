"""Exact guarded-selection withdrawal frontier and physical successor payment.

The proof is the disjoint free-graph decomposition and universal weighted
nine-vertex tree certificate. Finite enumeration is only a local control.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_component_receivers import vertices_of
from check_endpoint_invasion_sharp_strips import (
    components, edge_key, endpoints, free_vertices, pocket_bound,
)
from check_frozen_strip_completion_reserves import completion
from check_occupied_strip_degree_four_budget import family, inspect_budget, check_ranks
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# d,g,b,u,v,a,s,l,r, relative to the withdrawn guard's column c.
TREE = [(2,0),(3,0),(3,1),(2,2),(3,2),(4,1),(5,1),(5,0),(5,2)]
TREE_EDGES = [(0,1),(1,2),(2,4),(2,5),(3,4),(5,6),(6,7),(6,8)]
WEDGES = [(2,1,4),(2,4,5),(5,2,6),(6,7,8)]
OLD_P_COUNTS = {1:1,3:2,4:1}
PATTERN_A = ({0,5,7,8},{(1,2),(3,4)})
PATTERN_B = ({0,7,8},{(1,2),(3,4),(5,6)})


def guard(i):
    return 3,9+6*i


def tree_cells(i):
    c = guard(i)[1]
    return [(r,c+s) for r,s in TREE]


def free_components(k,withdrawn):
    original = components(k)
    out,caps = [original[0]],[9]
    for j in range(1,k):
        if j-1 in withdrawn:
            out.append(set(tree_cells(j-1)))
            caps.append(6)
        else:
            out += [original[j],original[k-1+j]]
            caps += [1,3]
    out += original[2*k-1:]
    caps += [1]*(k+1)
    assert len(out) == len(caps)
    return out,caps


def tree_certificate(tset,M,counts):
    P = {v for e in M for v in e}
    O = tset | P
    assert 3 not in tset
    assert int(1 in tset)+int(0 in O) <= 1
    values = [int(v in tset)+int(a in O)+int(b in O) for v,a,b in WEDGES]
    assert all(x <= 2 for x in values)
    lhs = (int(1 in tset)+int(0 in O)+sum(values)+
           int(0 in tset)+int(7 in tset)+int(8 in tset)+2*int(3 in tset))
    q = len(tset)+len(M)
    assert lhs == 2*q+int(2 in tset)+int((2,4) in M) <= 12
    assert q <= 6
    if q == 6:
        assert 2 not in tset and (2,4) not in M
        assert {0,7,8} <= tset
        assert (tset,M) in (PATTERN_A,PATTERN_B)
    counts['universal_tree_certificate_controls'] += 1


def local_controls(counts):
    best = []
    for mask in range(1 << len(TREE_EDGES)):
        M = {e for j,e in enumerate(TREE_EDGES) if (mask >> j) & 1}
        P = {v for e in M for v in e}
        if len(P) != 2*len(M):
            continue
        remaining = sorted(set(range(9))-P)
        for bits in range(1 << len(remaining)):
            T = {v for j,v in enumerate(remaining) if (bits >> j) & 1}
            O = T | P
            if any(OLD_P_COUNTS.get(v,0)+sum(u in O for u in range(9)
                   if tuple(sorted((u,v))) in TREE_EDGES) > 1 for v in T):
                continue
            tree_certificate(T,M,counts)
            counts['independent_local_models'] += 1
            if len(T)+len(M) == 6:
                best.append((T,M))
    assert len(best) == 2 and all(x in best for x in (PATTERN_A,PATTERN_B))


def check_extension(cur,k,withdrawn,counts):
    old = family(k)[0]
    R = {guard(i) for i in withdrawn}
    assert withdrawn <= set(range(k-1))
    assert old[2]-R <= cur[2] and cur[:2] == old[:2]
    oldM = {edge_key(e) for e in old[3]}
    assert oldM <= {edge_key(e) for e in cur[3]}
    direct_check(*cur)
    base = (*old[:2],old[2]-R,old[3])
    free = free_vertices(base)
    blocks,caps = free_components(k,withdrawn)
    assert set().union(*blocks) == free
    assert sum(map(len,blocks)) == len(free) == 7*k+10+3*len(withdrawn)
    owner = {v:i for i,c in enumerate(blocks) for v in c}
    assert all(owner[v] == owner[u] for v in free for u in set(neighbors(v)) & free)
    newT = cur[2]-base[2]
    newM = [edge_key(e) for e in cur[3] if edge_key(e) not in oldM]
    assert newT | endpoints(newM) <= free
    assert all(owner[a] == owner[b] for a,b in newM)
    pocket_bound(newT,newM,counts)
    for cells,cap in zip(blocks,caps):
        assert len(newT & cells)+sum(set(e) <= cells for e in newM) <= cap
    frozen,layers = frozen_certificate(cur)
    for i in withdrawn:
        cells = tree_cells(i)
        index = {v:j for j,v in enumerate(cells)}
        T = {index[v] for v in newT & set(cells)}
        M = {tuple(sorted((index[a],index[b]))) for a,b in newM
             if {a,b} <= set(cells)}
        tree_certificate(T,M,counts)
        if frozen == endpoints(cur[3]) and len(T)+len(M) == 6:
            assert (T,M) == PATTERN_A
    assert sum(caps) == 5*k+6+2*len(withdrawn)
    upper = 17*k+12+len(withdrawn)
    assert len(cur[2])+len(cur[3]) <= upper
    counts['retained_matching_extension_models'] += 1
    return frozen,layers


def attaining(k,withdrawn):
    cur = completion(k)[0]
    T,M = set(cur[2]),list(cur[3])
    for i in withdrawn:
        c = guard(i)[1]
        T -= {(3,c),(3,c+2)}
        T.add((2,c))
        M += [((3,c),(3,c+1)),((2,c+2),(3,c+2))]
    return (*cur[:2],T,M)


def rematching_obstruction(k):
    """One withdrawn guard defeats old-edge-preserving normalization, all k>=2."""
    assert k >= 2
    cur = completion(k)[0]
    T = (cur[2]-{(2,3),(3,5),(3,9),(3,11),(4,10)}) | {(2,9),(3,10)}
    removed = {edge_key(e) for e in [((1,5),(1,6)),((1,7),(2,7)),((3,7),(3,8))]}
    added = [((1,5),(2,5)),((1,6),(1,7)),((2,7),(3,7)),
             ((3,4),(3,5)),((3,8),(3,9))]
    M = sorted(({edge_key(e) for e in cur[3]}-removed) | {edge_key(e) for e in added})
    return (*cur[:2],T,M)


def check_rematching_obstruction(k,counts):
    cur = rematching_obstruction(k)
    old = family(k)[0]
    direct_check(*cur)
    assert old[2]-cur[2] == {(3,9)}
    P0,P = endpoints(old[3]),endpoints(cur[3])
    assert P0 <= P
    assert P-P0 == {(2,5),(3,4),(3,5),(3,9)}
    assert not set(neighbors((3,9))) & (P-P0)
    assert not {edge_key(e) for e in old[3]} <= {edge_key(e) for e in cur[3]}
    frozen,layers = frozen_certificate(cur)
    assert frozen == P
    # Independent explicit certificate, uniform in k; unaffected old cores keep
    # their original records, and this first component has ranks at most five.
    first_old = {(1,5),(1,6),(1,7),(2,7),(2,6),(3,6),(3,7),(3,8)}
    records = [r for r in family(k)[2] if r[0] not in first_old]
    records += [
        ((1,5),0,(0,5),(1,4)),((1,7),0,(0,7),(1,8)),
        ((3,4),0,(3,3),(4,4)),((3,9),0,(2,9),(3,10)),
        ((2,6),1,(1,6),(2,5)),((3,6),1,(4,6),(3,5)),
        ((3,5),2,(2,5),(3,6)),((3,7),2,(3,6),(3,8)),
        ((2,5),2,(2,6),(3,5)),((1,6),3,(1,5),(2,6)),
        ((2,7),4,(1,7),(2,6)),((3,8),5,(4,8),(3,7)),
    ]
    check_ranks(cur,records)
    assert len(cur[2])+len(cur[3]) == 17*k+11
    assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3]) == k+1
    counts['fully_frozen_normalization_obstruction_models'] += 1
    counts['obstruction_explicit_strict_rank_events'] += len(records)
    return cur,layers


def physical_payment(cur,k,withdrawn,counts):
    region = family(k)[1]
    report = inspect_budget(cur,[region],counts)
    assert report['surplus_twice'] == 1-k
    assert report['degree_four_budget'] == dict(boundary_ends=1,
        unported_degree_four_TP=k,ported_exports=1,
        unused_forest_end_slots=0,bound_surplus_twice=1-k)
    assert report['unused_BP'] == report['safe_cross'] == 0
    P,T = endpoints(cur[3]),cur[2]
    Q = lambda j:(1,2+3*j)
    rebate = lambda i:(1,4+3*i)
    charge = lambda q:4-2*len(T & vertices_of({q}))-len(P & vertices_of({q}))
    recipients = {(1,7+6*i) for i in range(k)}
    payments = {(1,7+6*i):(Q(i+1) if i in withdrawn else rebate(i)) for i in range(k)}
    assert set(payments) == recipients and len(set(payments.values())) == k
    assert all(charge(q) == 1 for q in payments.values())
    spent_reserves = {Q(i+1) for i in withdrawn}
    remaining = {Q(j) for j in range(k)}-spent_reserves
    assert not remaining & set(payments.values()) and len(remaining) == k-len(withdrawn)
    assert all(charge(q) == 2 for q in remaining)
    assert all(charge(rebate(i)) == 0 for i in withdrawn)
    assert charge((1,0)) == -1
    for r,c in itertools.product(range(1,3),range(cur[1]//2)):
        q = (r,c)
        if q in remaining or q in payments.values() or q == (1,0):
            continue
        assert charge(q) == 0
    assert cur[0]*cur[1]//2-len(T)-len(cur[3]) == k-len(withdrawn)
    counts['actual_no_reuse_payment_maps'] += 1
    counts['successor_reserves_converted_and_spent_once'] += len(withdrawn)
    counts['distinct_unspent_full_units'] += len(remaining)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--write-fixture',action='store_true')
    args = p.parse_args()
    counts,samples = Counter(),[]
    local_controls(counts)
    for k in (*range(2,17),32,64,128):
        check_rematching_obstruction(k,counts)
        candidates = [set(c) for size in range(k)
                      for c in itertools.combinations(range(k-1),size)] if k <= 6 else [
            set(),set(range(k-1)),set(range(0,k-1,2)),set(range(1,k-1,2)),{0},{k-2}]
        for withdrawn in candidates:
            cur = attaining(k,withdrawn)
            frozen,layers = check_extension(cur,k,withdrawn,counts)
            assert frozen == endpoints(cur[3])
            assert len(cur[2]) == 13*k+11-len(withdrawn)
            assert len(cur[3]) == 4*k+1+2*len(withdrawn)
            assert family(k)[0][2]-cur[2] == {guard(i) for i in withdrawn}
            physical_payment(cur,k,withdrawn,counts)
            counts['sharp_fully_frozen_joint_withdrawal_models'] += 1
        if k in (2,4,16,128):
            cur = attaining(k,set(range(k-1)))
            samples.append(dict(k=k,withdrawn_guards=k-1,selected=len(cur[2]),
                matching=len(cur[3]),objective=len(cur[2])+len(cur[3]),
                whole_surplus=1,strip_surplus_twice=1-k))
    # Arbitrary matching additions and selected completions in the enlarged free graph.
    for k in (2,3,4,8):
        for seed in range(16):
            rng = random.Random(29101+seed+107*k)
            withdrawn = {i for i in range(k-1) if rng.randrange(2)}
            old = family(k)[0]
            base = (*old[:2],old[2]-{guard(i) for i in withdrawn},old[3])
            free = free_vertices(base)
            edges = sorted({edge_key((v,u)) for v in free
                            for u in set(neighbors(v)) & free})
            rng.shuffle(edges)
            extra,used = [],set()
            for e in edges:
                if not set(e) & used and rng.randrange(3) == 0:
                    extra.append(e)
                    used.update(e)
            P,T = endpoints(old[3]) | used,set(base[2])
            order = sorted(free-used)
            rng.shuffle(order)
            for v in order:
                trial = T | {v}
                if all(len(set(neighbors(t)) & (P | trial)) <= 1 for t in trial):
                    T = trial
            check_extension((*old[:2],T,old[3]+extra),k,withdrawn,counts)
            counts['arbitrary_joint_completion_controls'] += 1
    cur = attaining(2,{0})
    frozen,layers = check_extension(cur,2,{0},counts)
    fixture = dict(scope='One old interior T guard withdrawn, old M retained. Two new edges and one net T loss give objective47 instead of46; all22 endpoints freeze. Regional surplus stays -1/2, whole surplus drops2->1. Lost old half rebate is replaced by successor old reserve, converted to half credit and spent once.',
        k=2,withdrawn_guards=[(3,9)],shape=cur[:2],selected=sorted(cur[2]),
        matching=cur[3],freezing_layers=layers,objective=47,whole_surplus=1,
        lost_rebate_tile=(1,4),successor_reserve_converted_and_spent=(1,5),
        remaining_full_unit_reserve=(1,2))
    path = Path('develop/fixtures/one_guard_withdrawal_frozen_gain_k2.json')
    if args.write_fixture:
        path.write_text(json.dumps(fixture,indent=2)+'\n')
    assert json.loads(path.read_text()) == json.loads(json.dumps(fixture))
    obstacle,layers = check_rematching_obstruction(2,counts)
    other = dict(scope='All-k extension with one old guard withdrawn: fully frozen actual rematching changes old edges. Old endpoints retained; the four new endpoints include isolated (3,9) in their induced graph, so NO matching on the same P can contain all M0. Refutes old-edge normalization/freezing rigidity after withdrawal, not the half-area inequality; whole margin is k+1.',
        k=2,shape=obstacle[:2],selected=sorted(obstacle[2]),matching=obstacle[3],
        freezing_layers=layers,new_endpoints=sorted(endpoints(obstacle[3])-endpoints(family(2)[0][3])),
        isolated_new_endpoint=(3,9),objective=45,whole_surplus=3)
    path = Path('develop/fixtures/one_guard_frozen_rematching_no_normalization_k2.json')
    if args.write_fixture:
        path.write_text(json.dumps(other,indent=2)+'\n')
    assert json.loads(path.read_text()) == json.loads(json.dumps(other))
    out = dict(status='PASS',counts=dict(counts),samples=samples,
        scope='Written all-k exact maximum17k+12+q with retained M0 and T0 except any q interior guard sites; arbitrary extra T and matching edges, no freeze required for upper bound. Explicit all-subset attaining family fully frozen. Nine-vertex tree bound6 and equality classification proved generally by weighted feasibility certificate; physical D4 payment injectively reroutes lost half rebates through successor old reserves, leaving exactly k-q full units. Does not prove the same upper bound for simultaneous arbitrary rematching of old M or arbitrary T/P withdrawals, nor universal5/6.')
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__ == '__main__':
    main()
