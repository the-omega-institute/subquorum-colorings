"""Joint withdrawal and arbitrary old-edge rematching: checks of a general proof.

The proof uses an occupation-only tree certificate and ONE pocket half-slack;
enumeration validates local identities and never substitutes for that proof.
"""
import argparse
from collections import Counter, deque
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import (
    POCKET, EDGES, WEDGES, coefficients, edge_key, endpoints, free_vertices,
)
from check_occupied_strip_degree_four_budget import family
from check_promotion_cores import frozen_certificate
from check_endpoint_rematching_normalization import sharp_all_ports
from check_residual_corridors import direct_check
from check_selection_withdrawal_sharp_strips import (
    TREE, TREE_EDGES, OLD_P_COUNTS, attaining, free_components, guard,
    rematching_obstruction, tree_cells, physical_payment,
)

if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')


def tree_occupation_certificate(T, P, counts):
    assert not T & P and T | P <= set(range(9))
    O = T | P
    t = lambda i: int(i in T)
    o = lambda i: int(i in O)
    assert t(3) == 0
    values = [t(1)+o(0), t(4)+o(3),
              t(2)+o(1)+o(4), t(5)+o(2)+o(6),
              t(6)+o(7)+o(8), t(0), t(7), t(8), o(5)]
    assert all(a <= b for a, b in zip(values, [1,1,2,2,2,1,1,1,1]))
    assert sum(values) == 2*len(T)+len(P) <= 12
    counts['occupation_tree_certificates'] += 1


def all_tree_controls(counts):
    adj = [{b if a == i else a for a,b in TREE_EDGES if i in (a,b)}
           for i in range(9)]
    maxima = []
    for state in itertools.product(range(3), repeat=9):
        T = {i for i,s in enumerate(state) if s == 1}
        P = {i for i,s in enumerate(state) if s == 2}
        if any(OLD_P_COUNTS.get(i,0)+len(adj[i] & (T|P)) > 1 for i in T):
            continue
        tree_occupation_certificate(T,P,counts)
        counts['independent_tree_occupations'] += 1
        if 2*len(T)+len(P) == 12:
            maxima.append(dict(T=sorted(T), P=sorted(P)))
    assert len(maxima) == 4
    counts['tree_maximum_occupation_patterns'] = len(maxima)


def pocket_certificate(T, P, M, P0, counts):
    pocket = set(POCKET)
    localT, localP = T & pocket, P & pocket
    internal = {edge_key(e) for e in M if set(e) <= pocket}
    cross = {edge_key(e) for e in M if len(set(e) & pocket) == 1}
    outside = {v for e in cross for v in e if v not in pocket}
    assert outside <= P0
    ports = {v for e in cross for v in e if v in pocket}
    U,V = (2,5),(3,5)
    assert ports <= {U,V}
    xU,xV = int(U in ports),int(V in ports)
    assert len(localP) == 2*len(internal)+xU+xV
    O = localT | localP
    assert U not in localT
    lhs = 3*int((2,3) in localT)+3*int(U in localT)
    for weight,v,a,b in WEDGES:
        value = int(v in localT)+int(a in O)+int(b in O)
        assert value <= 2
        lhs += weight*value
    _,mc = coefficients()
    costly = sum(mc[e] == 5 for e in internal)
    local_integer = len(localT)+len(internal)+xV
    assert lhs == 3*local_integer+2*costly <= 29
    assert local_integer <= 9
    charge_twice = 2*len(localT)+len(localP)
    assert charge_twice == 2*local_integer+xU-xV <= 18+xU-xV <= 19
    counts['pocket_matching_boundary_certificates'] += 1
    counts['pocket_upper_only_crossings'] += xU and not xV
    return charge_twice


def all_pocket_controls(counts):
    """Enumerate all internal matchings, boundary flags and feasible local T.

    Outside names merely identify occupied old endpoints and their matching
    partners. Their global extendability is deliberately not assumed.
    """
    base = family(2)[0]
    P0 = endpoints(base[3])
    candidates = EDGES+[((2,5),(1,5)),((3,5),(3,6))]
    matchings = []
    def visit(j,M,used):
        if j == len(candidates):
            matchings.append(tuple(M)); return
        visit(j+1,M,used)
        a,b = candidates[j]
        if not {a,b} & used:
            visit(j+1,M+[(a,b)],used|{a,b})
    visit(0,[],set())
    local = set(POCKET)
    best = -1
    boundary_best = {}
    for M in matchings:
        P = endpoints(M)
        remaining = sorted(local-P)
        for bits in range(1 << len(remaining)):
            T = {v for i,v in enumerate(remaining) if bits >> i & 1}
            O = T | P | P0
            if any(len(set(neighbors(t)) & O) > 1 for t in T):
                continue
            value = pocket_certificate(T,P,M,P0,counts)
            best = max(best,value)
            ports = {v for e in M if len(set(e) & local) == 1 for v in e if v in local}
            key = str((int((2,5) in ports),int((3,5) in ports)))
            boundary_best[key] = max(boundary_best.get(key,-1),value)
            counts['independent_pocket_partial_matching_models'] += 1
    assert best == 18
    assert boundary_best == {'(0, 0)':18,'(0, 1)':17,'(1, 0)':17,'(1, 1)':18}
    counts['enumerated_pocket_charge_twice_maximum'] = best
    counts['written_pocket_certificate_upper_bound'] = 19
    print('Independent pocket boundary maxima:',boundary_best,flush=True)


def global_physical_tokens(cur,k,J,counts):
    """Pay exterior debts AND net strip debt from actual positive tile tokens.

    This is a global charge assignment, not a direction-restricted route or
    an assertion that residual half units lie in whole-unit original tiles.
    """
    T,P = cur[2],endpoints(cur[3])
    charges = {}
    for a,b in itertools.product(range(3),range(cur[1]//2)):
        tile = {(2*a+i,2*b+j) for i,j in itertools.product(range(2),repeat=2)}
        charges[a,b] = 4-2*len(T & tile)-len(P & tile)
    assert sum(c for (a,b),c in charges.items() if a == 0) == 1-k
    outside = {tile:c for tile,c in charges.items() if tile[0] != 0}
    positive = [(tile,j) for tile,c in sorted(outside.items()) if c > 0 for j in range(c)]
    negative = [('outside',tile,j) for tile,c in sorted(outside.items()) if c < 0 for j in range(-c)]
    demands = negative+[('net_strip',j) for j in range(k-1)]
    assert sum(outside.values()) == len(positive)-len(negative) >= 3*k-1-2*len(J)
    assert len(positive) >= len(demands)+2*(k-len(J))
    allocation = dict(zip(demands,positive))
    assert len(allocation) == len(demands) and len(set(allocation.values())) == len(demands)
    remaining = positive[len(demands):]
    assert not set(remaining) & set(allocation.values())
    assert len(remaining) >= 2*(k-len(J))
    assert len(remaining) == 2*(cur[0]*cur[1]//2-len(T)-len(cur[3]))
    counts['global_actual_tile_token_allocations'] += 1
    counts['actual_exterior_negative_tokens_paid'] += len(negative)
    counts['net_strip_half_demands_paid_once'] += k-1
    counts['unspent_actual_exterior_half_tokens'] += len(remaining)


def check_extension(cur,k,J,counts,require_frozen=False):
    old = family(k)[0]
    P0 = endpoints(old[3])
    retainedT = old[2]-{guard(i) for i in J}
    assert J <= set(range(k-1))
    assert cur[:2] == old[:2] and retainedT <= cur[2]
    P,T,M = endpoints(cur[3]),cur[2],cur[3]
    assert P0 <= P
    direct_check(*cur)
    F = free_vertices((*old[:2],retainedT,old[3]))
    components,_ = free_components(k,J)
    assert set().union(*components) == F
    assert sum(map(len,components)) == len(F) == 7*k+10+3*len(J)
    owner = {v:j for j,C in enumerate(components) for v in C}
    assert all(owner[v] == owner[u] for v in F for u in set(neighbors(v)) & F)
    assert T-retainedT | (P-P0) <= F
    # Verify ALL boundary possibilities, independently of the actual matching.
    pocket = set(POCKET)
    possible = {v for v in pocket if set(neighbors(v)) & P0}
    assert possible == {(2,5),(3,5)}
    assert all(not set(neighbors(v)) & F for v in retainedT if not set(neighbors(v)) & P0)
    newT,newP = T-retainedT,P-P0
    local_bounds = []
    pocket_value = pocket_certificate(newT,newP,M,P0,counts)
    local_bounds.append(19)
    assert pocket_value <= 19
    for j,C in enumerate(components[1:],1):
        localT,localP = newT & C,newP & C
        boundary = {u for v in C for u in set(neighbors(v)) & P0}
        if len(C) == 9:
            i = next(i for i in J if C == set(tree_cells(i)))
            cells = tree_cells(i)
            index = {v:a for a,v in enumerate(cells)}
            assert {v:len(set(neighbors(v)) & P0) for v in C} == {
                v:OLD_P_COUNTS.get(index[v],0) for v in C}
            tree_occupation_certificate({index[v] for v in localT},
                                        {index[v] for v in localP},counts)
            bound = 12
        elif len(C) == 2:
            u,v = sorted(C)
            assert u[0] == 2 and v[0] == 3
            assert len(set(neighbors(u)) & P0) == 2
            assert len(set(neighbors(v)) & P0) == 1
            assert u not in localT
            assert int(v in localT)+int(u in localT|localP) <= 1
            bound = 2
        elif len(C) == 4:
            assert not boundary
            internal = [e for e in M if set(e) <= C]
            assert endpoints(internal) == localP
            assert len(internal) <= 1
            if internal:
                assert len(localT) <= 2
            else:
                assert len(localT) <= 3
            bound = 6
        else:
            assert len(C) == 1 and not boundary
            assert not localP
            bound = 2
        assert 2*len(localT)+len(localP) <= bound
        local_bounds.append(bound)
    q = len(J)
    assert sum(local_bounds) == 10*k+13+4*q
    extra_twice = 2*len(newT)+len(newP)
    assert extra_twice <= sum(local_bounds)
    total = len(T)+len(M)
    assert 2*total == 2*(12*k+6-q)+extra_twice
    assert 2*total <= 2*(17*k+12+q)+1
    assert total <= 17*k+12+q
    assert cur[0]*cur[1]//2-total >= k-q
    global_physical_tokens(cur,k,J,counts)
    old_edges = {edge_key(e) for e in old[3]}
    counts['models_not_retaining_old_edges'] += not old_edges <= {edge_key(e) for e in M}
    counts['arbitrary_rematching_withdrawal_models'] += 1
    if require_frozen:
        assert frozen_certificate(cur)[0] == P
        counts['fully_frozen_joint_models'] += 1


def random_extension(k,J,seed):
    """Augment on the true allowed grid, keeping P0 covered at every step."""
    rng = random.Random(seed)
    old = family(k)[0]
    retainedT = old[2]-{guard(i) for i in J}
    P0 = endpoints(old[3])
    F = free_vertices((*old[:2],retainedT,old[3]))
    possible = F | P0
    mate = {v:u for e in old[3] for v,u in (e,e[::-1])}
    starts = sorted(F); rng.shuffle(starts)
    for start in starts[:rng.randrange(len(starts)+1)]:
        if start in mate:
            continue
        parent = {start:None}; queue = deque([start]); end = None
        while queue and end is None:
            v = queue.popleft()
            choices = sorted(set(neighbors(v)) & possible); rng.shuffle(choices)
            for u in choices:
                if mate.get(v) == u or u in parent:
                    continue
                parent[u] = v
                if u not in mate:
                    end = u; break
                w = mate[u]
                if w not in parent:
                    parent[w] = u; queue.append(w)
        if end is None:
            continue
        path = [end]
        while parent[path[-1]] is not None:
            path.append(parent[path[-1]])
        path.reverse()
        assert len(path)%2 == 0 and len(set(path)) == len(path)
        for v in path:
            mate.pop(v,None)
        for a,b in zip(path[::2],path[1::2]):
            mate[a]=b;mate[b]=a
        assert P0 <= set(mate)
    M = sorted({edge_key((v,u)) for v,u in mate.items()})
    T = set(retainedT); candidates = sorted(F-set(mate)); rng.shuffle(candidates)
    for v in candidates:
        if rng.randrange(5) == 0:
            continue
        trial = T | {v}; O = trial | set(mate)
        if all(len(set(neighbors(t)) & O) <= 1 for t in trial):
            T = trial
    return (*old[:2],T,M)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();counts=Counter();samples=[]
    all_tree_controls(counts)
    all_pocket_controls(counts)
    for k in list(range(2,13))+[16,32,64,128]:
        sets = ([{i for i in range(k-1) if mask >> i & 1} for mask in range(1<<(k-1))]
                if k <= 6 else [set(),{0},{k-2},set(range(k-1)),set(range(0,k-1,2))])
        for J in sets:
            cur = attaining(k,J)
            check_extension(cur,k,J,counts,require_frozen=True)
            physical_payment(cur,k,J,counts)
            assert len(cur[2])+len(cur[3]) == 17*k+12+len(J)
            counts['sharp_frozen_all_subset_attainers'] += 1
        obstacle = rematching_obstruction(k)
        check_extension(obstacle,k,{0},counts,require_frozen=True)
        newP = endpoints(obstacle[3])-endpoints(family(k)[0][3])
        assert (3,9) in newP and not set(neighbors((3,9))) & newP
        counts['frozen_no_normalization_controls'] += 1
        if k <= 32:
            for seed in range(24):
                rng = random.Random(4500+seed+101*k)
                J = {i for i in range(k-1) if rng.randrange(2)}
                check_extension(random_extension(k,J,seed+1000*k),k,J,counts)
            modes = (itertools.product(range(4),repeat=k) if k <= 4 else
                     [[(i+offset)%4 for i in range(k)] for offset in range(4)])
            for modeset in modes:
                cur = sharp_all_ports(k,list(modeset))
                J = {i for i in range(k-1) if i%2 == 0}
                cur = (*cur[:2],cur[2]-{guard(i) for i in J},cur[3])
                check_extension(cur,k,J,counts)
                counts['explicit_joint_withdrawal_and_rematching_controls'] += 1
        samples.append(dict(k=k,q=k-1,sharp_objective=18*k+11,
                            half_area=18*k+12,whole_surplus=1))
    assert counts['models_not_retaining_old_edges'] > 100
    assert counts['pocket_upper_only_crossings'] > 0
    report=dict(status='PASS',counts=dict(counts),samples=samples,
        scope='Written all-k exact maximum17k+12+q after any q specified interior guard withdrawals; retain T0 except these guards and P0, allow arbitrary actual old-edge rematching and arbitrary added endpoints/selections. No freezing needed for upper bound; every J has a fully frozen sharp attainer. Occupation-only tree capacity6 and one boundary-aware pocket half-slack, removed by ONE global integer rounding. No old-M normalization assumption. For every arbitrary actual rematching, actual positive original-tile half tokens injectively cover all exterior negative charge plus net strip deficit and leave at least2(k-q) unspent half tokens. This global allocation has no locality/direction restriction; individual D4 routing and whole-unit original-tile reserves for arbitrary rematching are not claimed. The prior successor physical payment applies to the explicit sharp attainers. Universal5/6, other T/P deletions and general mixed-direction geometric cut remain open.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__=='__main__':
    main()
