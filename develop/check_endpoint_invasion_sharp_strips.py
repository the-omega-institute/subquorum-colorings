"""Endpoint additions to the sharp negative strip: written weighted proof is primary.

No optimization package is required. Coordinates and resource identities are
checked independently of the local integer certificate. Do not run with -O.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_component_receivers import vertices_of
from check_frozen_strip_completion_reserves import completion
from check_occupied_strip_degree_four_budget import family, check_ranks, inspect_budget
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

POCKET = [(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,2),(4,3),
          (4,4),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]
EDGES = sorted({tuple(sorted((v,u))) for v in POCKET
                for u in set(neighbors(v)) & set(POCKET)})
# (weight, centre, first neighbour, second neighbour).
WEDGES = [(2,(3,4),(3,3),(3,5)),(1,(3,4),(3,5),(4,4)),
          (2,(4,2),(4,3),(5,2)),(1,(4,3),(3,3),(4,4)),
          (3,(5,0),(4,0),(5,1)),(1,(5,2),(4,2),(5,3)),
          (1,(5,4),(4,4),(5,5)),(2,(5,4),(5,3),(5,5))]


def endpoints(M):
    return {v for e in M for v in e}


def edge_key(e):
    return tuple(sorted(e))


def components(k):
    assert k >= 1
    gates = [{(2,5+6*i),(3,5+6*i)} for i in range(1,k)]
    stars = [{(5,4+6*i),(4,4+6*i),(5,3+6*i),(5,5+6*i)}
             for i in range(1,k)]
    isolated = [{(5,7+6*i)} for i in range(k)] + [{(5,6*k+3)}]
    return [set(POCKET)] + gates + stars + isolated


def free_vertices(cur):
    h,w,T,M = cur
    P = endpoints(M)
    anchored = {t for t in T if set(neighbors(t)) & P}
    board = set(itertools.product(range(h),range(w)))
    return {v for v in board-T-P if not set(neighbors(v)) & anchored}


def coefficients():
    tc = Counter({(2,3):3,(2,5):3})
    pc = Counter()
    for weight,v,a,b in WEDGES:
        assert a != b and a in neighbors(v) and b in neighbors(v)
        tc[v] += weight
        for u in (a,b):
            tc[u] += weight
            pc[u] += weight
    mc = {e:pc[e[0]]+pc[e[1]] for e in EDGES}
    assert set(tc) == set(POCKET) and set(tc.values()) == {3}
    assert len(EDGES) == 17 and set(mc.values()) == {3,5}
    assert 2*sum(z[0] for z in WEDGES)+3 == 29
    return tc,mc


def pocket_bound(newT,newM,counts):
    M = [edge_key(e) for e in newM if set(e) <= set(POCKET)]
    T = newT & set(POCKET)
    P = endpoints(M)
    O = T | P
    assert (2,5) not in T
    lhs = 3*int((2,3) in T)+3*int((2,5) in T)
    for weight,v,a,b in WEDGES:
        value = int(v in T)+int(a in O)+int(b in O)
        assert value <= 2
        lhs += weight*value
    _,mc = coefficients()
    q = len(T)+len(M)
    costly = sum(mc[e] == 5 for e in M)
    assert lhs == 3*q+2*costly <= 29
    assert q <= 9
    counts['weighted_pocket_certificates'] += 1


def check_extension(cur,k,counts):
    old,region,ranks,_ = family(k)
    assert cur[:2] == old[:2] and old[2] <= cur[2]
    oldM = {edge_key(e) for e in old[3]}
    assert oldM <= {edge_key(e) for e in cur[3]}
    direct_check(*cur)
    # Replay the old certificate on its own retained matching; the helper
    # deliberately requires its rank domain to equal ALL supplied endpoints.
    check_ranks((*cur[:3],old[3]),ranks)
    newT = cur[2]-old[2]
    newM = [e for e in cur[3] if edge_key(e) not in oldM]
    F = free_vertices(old)
    assert newT | endpoints(newM) <= F
    C = components(k)
    owner = {v:i for i,c in enumerate(C) for v in c}
    assert len(owner) == sum(map(len,C)) == 7*k+10
    assert set(owner) == F
    assert all(owner[v] == owner[u] for v in F for u in set(neighbors(v)) & F)
    assert all(not set(neighbors(t)) & F for t in old[2]
               if not set(neighbors(t)) & endpoints(old[3]))
    assert all(owner[e[0]] == owner[e[1]] for e in newM)
    pocket_bound(newT,newM,counts)
    caps = [9]+[1]*(k-1)+[3]*(k-1)+[1]*(k+1)
    for c,cap in zip(C,caps):
        localM = [e for e in newM if set(e) <= c]
        assert len(newT & c)+len(localM) <= cap
    assert sum(caps) == 5*k+6
    assert len(cur[2])+len(cur[3]) <= 17*k+12
    assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3]) >= k
    frozen,layers = frozen_certificate(cur)
    P = endpoints(cur[3])
    assert endpoints(old[3]) <= frozen
    if frozen == P:
        assert endpoints(newM) <= set(POCKET) and len(newM) <= 7
        counts['fully_frozen_extension_models'] += 1
    counts['extension_models'] += 1
    return frozen,layers


def invading_completion(k):
    cur,region,ranks,_ = completion(k)
    removed = {(3,3),(3,5),(4,0),(4,4),(5,3)}
    added = {(3,4),(4,3),(5,1),(5,4)}
    assert removed <= cur[2] and not added & cur[2]
    T = (cur[2]-removed) | added
    M = cur[3]+[((2,5),(3,5))]
    return (*cur[:2],T,M),region,ranks


def inspect(k,counts):
    old = family(k)[0]
    C = components(k)
    assert set().union(*C) == free_vertices(old)
    assert len(set().union(*C)) == sum(map(len,C)) == 7*k+10
    cur,region,_ = invading_completion(k)
    frozen,layers = check_extension(cur,k,counts)
    assert frozen == endpoints(cur[3])
    assert len(cur[2]) == 13*k+10 and len(cur[3]) == 4*k+2
    assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3]) == k
    budget = inspect_budget(cur,[region],counts)
    assert budget['surplus_twice'] == 1-k
    T,P = cur[2],endpoints(cur[3])
    charge = lambda q:4-2*len(T & vertices_of({q}))-len(P & vertices_of({q}))
    # The spent first reserve is neutral. The replacement is a DIFFERENT tile.
    assert charge((1,2)) == 0 and charge((1,1)) == 2
    reserves = {(1,1)} | {(1,2+3*i) for i in range(1,k)}
    rebates = {(1,4+3*i) for i in range(k)}
    assert reserves.isdisjoint(rebates) and len(reserves) == len(rebates) == k
    assert all(charge(q) == 2 for q in reserves)
    assert all(charge(q) == 1 for q in rebates)
    assert charge((1,0)) == -1
    for r,c in itertools.product(range(3),range(cur[1]//2)):
        if r == 0 or (r,c) in reserves | rebates | {(1,0)}:
            continue
        assert charge((r,c)) == 0
    assert sum(charge((r,c)) for r,c in itertools.product(range(3),range(cur[1]//2))) == 2*k
    counts['sharp_frozen_invading_models'] += 1
    counts['new_endpoint_freezing_events'] += 2
    counts['distinct_relocated_unit_reserves'] += k
    return cur,region,layers,dict(k=k,shape=cur[:2],selected=len(T),matching=len(cur[3]),
        whole_surplus=k,strip_surplus_twice=1-k,free_vertices=7*k+10,
        free_components=len(C),pocket_bound=9,added_matching=[((2,5),(3,5))],
        consumed_original_reserve=(1,2),replacement_unit_reserve=(1,1),
        distinct_full_unit_reserves=sorted(reserves),distinct_half_rebates=sorted(rebates))


def random_controls(counts):
    for k in (1,2,4,8):
        base = family(k)[0]
        F = free_vertices(base)
        E = sorted({edge_key((v,u)) for v in F for u in set(neighbors(v)) & F})
        for seed in range(24):
            rng = random.Random(261000+73*k+seed)
            newM,used = [],set()
            order = E[:]
            rng.shuffle(order)
            for e in order:
                if not set(e) & used and rng.randrange(3) == 0:
                    newM.append(e)
                    used.update(e)
            T = set(base[2])
            P = endpoints(base[3]) | used
            order = sorted(F-used)
            rng.shuffle(order)
            for v in order:
                trial = T | {v}
                if all(len(set(neighbors(t)) & (trial | P)) <= 1 for t in trial):
                    T = trial
            check_extension((*base[:2],T,base[3]+newM),k,counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--write-fixture',action='store_true')
    args = parser.parse_args()
    tc,mc = coefficients()
    counts,samples = Counter(),[]
    random_controls(counts)
    for k in (*range(1,17),32,64,128):
        cur,region,layers,report = inspect(k,counts)
        check_extension(completion(k)[0],k,counts)
        if k in (1,2,4,16,128):
            if k > 4:
                for key in ('distinct_full_unit_reserves','distinct_half_rebates'):
                    ids = report.pop(key)
                    report[key+'_count'] = len(ids)
                    report[key+'_sample'] = ids[:2]+ids[-2:]
            samples.append(report)
        if k in (1,2,4):
            for sym in itertools.product((False,True),repeat=3):
                shape,T,M = transformed(*cur,*sym)
                image = (*shape,T,M)
                direct_check(*image)
                f,_ = frozen_certificate(image)
                assert f == endpoints(M)
                assert shape[0]*shape[1]//2-len(T)-len(M) == k
                counts['isometry_controls'] += 1
    cur,region,layers,report = inspect(2,counts)
    fixture = dict(scope='Sharp k2 retained endpoint invasion: old matching retained; one new fully frozen edge consumes Q(1,2), distinct Q(1,1) replaces its full-unit reserve. 36T/10M, margin2, strip surplus -1/2.',
        k=2,shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],region=region,
        freezing_layers=layers,report=report)
    path = Path('develop/fixtures/frozen_strip_endpoint_invasion_k2.json')
    if args.write_fixture:
        path.write_text(json.dumps(fixture,indent=2)+'\n')
    assert json.loads(path.read_text()) == json.loads(json.dumps(fixture))
    out = dict(status='PASS',counts=dict(counts),samples=samples,
        certificate=dict(selected_coefficients=[tc[v] for v in POCKET],
            matching_coefficients=[mc[e] for e in EDGES],weighted_rhs=29,
            conclusion='3*(newT_in_pocket+newM_in_pocket)+2*costly_edges<=29; integer score<=9'),
        scope='Written all-k theorem: every feasible retained-T0 retained-M0 extension, arbitrary new matching endpoints, has T+M<=17k+12 and whole surplus>=k. Independent components and explicit weighted pocket certificate, not enumeration. Sharp all-k frozen invading example relocates a consumed physical reserve to a different original tile. All fully frozen new edges lie in a fixed 15-vertex pocket. Does not cover withdrawal/rematching of old M or T, arbitrary footprints, or universal 5/6.')
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__ == '__main__':
    main()
