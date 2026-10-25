"""Canonical same-N bands, resource bijection, and sharp cut/deletion frontier.

General proofs are in docs/CANONICAL_BAND_COARSENING_AND_REPAIR.md.
Enumeration checks the physical adapters, rather than proving the theorem.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_crossing_matching_ports import rectangle
from check_degree_changing_bent_completions import compile_model, add_selections
from check_forced_mates_and_adjacent_maxima import configuration
from check_frozen_inventory_frontier import inventory_schedule
from check_frozen_selection_frontier import cover, seals
from check_mixed_terminal_defect import port_graph, mixed_regions
from check_opposed_direction_interfaces import fast_rank_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize, primitive_certificates

if not __debug__:
    raise RuntimeError('Assertions required; no -O.')


def tile_directions(R, C, regions):
    directions = {}
    for region in regions:
        r0, r1, c0, c1 = region['bounds']
        assert all(x % 2 == 0 for x in (r0, r1, c0, c1))
        for r in range(r0, r1, 2):
            for c in range(c0, c1, 2):
                assert (r, c) not in directions
                directions[r, c] = region['vertical']
    assert set(directions) == set(itertools.product(range(0, R, 2), range(0, C, 2)))
    return directions


def canonical_bands(R, C, regions):
    """Maximal H tile-row runs and maximal V tile-column runs."""
    direction = tile_directions(R, C, regions)
    result = []
    for r in range(0, R, 2):
        c = 0
        while c < C:
            if direction[r, c]:
                c += 2
                continue
            start = c
            while c < C and not direction[r, c]:
                c += 2
            result.append(rectangle(r, r+2, start, c))
    for c in range(0, C, 2):
        r = 0
        while r < R:
            if not direction[r, c]:
                r += 2
                continue
            start = r
            while r < R and direction[r, c]:
                r += 2
            result.append(rectangle(start, r, c, c+2, True))
    assert tile_directions(R, C, result) == direction
    return result


def tile_refinement(R, C, regions):
    direction = tile_directions(R, C, regions)
    return [rectangle(r, r+2, c, c+2, d) for (r, c), d in sorted(direction.items())]


def forests(cur, regions):
    """Extract all forest cells including the balanced zero components."""
    P = {v for e in cur[3] for v in e}
    T = cur[2]
    result = {}
    bands = [band for region in regions for band in region['bands']]
    for b, band in enumerate(bands):
        word = [tuple(sorted('P' if v in P else 'T' if v in T else 'B' for v in pair))
                for pair in band]
        unseen = {i for i, label in enumerate(word) if label in (('B', 'B'), ('T', 'T'))}
        while unseen:
            first = min(unseen)
            body = {first}
            todo = [first]
            unseen.remove(first)
            while todo:
                i = todo.pop()
                for j in (i-1, i+1):
                    if j in unseen and (word[i] == ('T', 'T') or word[j] == ('T', 'T')):
                        unseen.remove(j)
                        body.add(j)
                        todo.append(j)
            cells = frozenset(v for i in body for v in band[i])
            cap = sum(1 if word[i] == ('B', 'B') else -1 for i in body)
            assert cap in (0, 1)
            result[b, min(body), max(body)] = (cap, cells)
    return result


def restriction(data, pool):
    return (*data[:3], {a: W & pool for a, W in data[3].items()}, pool)


def check_coarsening(cur, fine, totals, independent=False, withdrawal=False, port=False):
    direct_check(*cur)
    coarse = canonical_bands(*cur[:2], fine)
    fd, fc, fN = compile_model(cur, fine)
    cd, cc, cN = compile_model(cur, coarse)
    assert fN == cN
    # Global ownership is intrinsic to M and N, not to the band cuts.
    assert [(x['body'], x['ends']) for x in fc] == [(x['body'], x['ends']) for x in cc]
    assert fd[:2] == cd[:2] and set(fd[2]) <= set(cd[2])
    ff, cf = forests(cur, fine), forests(cur, coarse)
    assert {j for j, (cap, _) in ff.items() if cap} == fd[4]
    assert {j for j, (cap, _) in cf.items() if cap} == cd[4]
    at = {v: j for j, (_, cells) in cf.items() for v in cells}
    children = {j: [] for j in cf}
    rho = {}
    for j, (cap, cells) in ff.items():
        parent = {at[v] for v in cells}
        assert len(parent) == 1
        p = parent.pop()
        assert cells <= cf[p][1]
        children[p].append(j)
        if cap:
            assert cf[p][0] == 1
            rho[j] = p
    for j, (cap, cells) in cf.items():
        assert frozenset().union(*(ff[ch][1] for ch in children[j])) == cells
        assert sum(ff[ch][0] for ch in children[j]) == cap
        assert sum(ff[ch][0] == 1 for ch in children[j]) == cap
    assert set(rho) == fd[4] and set(rho.values()) == cd[4]
    assert len(rho) == len(set(rho.values()))
    assert all({rho[j] for j in W} <= cd[3][a] for a, W in fd[3].items())
    totals['positive_resource_bijection_checks'] += len(rho)
    pools = [set(fd[4])]
    if withdrawal:
        Q = sorted(fd[4])
        rng = random.Random(len(Q)+len(fine)*103)
        pools += [set(), {j for j in Q if rng.randrange(2)}]
        if len(Q) <= 5:
            pools += [{j for i, j in enumerate(Q) if mask >> i & 1} for mask in range(1 << len(Q))]
    for pool in pools:
        newpool = {rho[j] for j in pool}
        fdata, cdata = restriction(fd, pool), restriction(cd, newpool)
        f, c = fork_flow(*fdata), fork_flow(*cdata)
        assert c['value'] >= f['value']
        if c['value'] == f['value']:
            assert c['cost'] <= f['cost']
        # Every individual old primitive embeds with the same owner/source,
        # beta-entry, links, and cost, not just with a scalar flow inequality.
        if independent:
            primitives = primitive_certificates(*fdata)
            coarse_primitives = primitive_certificates(*cdata)
            for old in primitives:
                lifted = dict(old)
                if lifted['interval'] is not None:
                    lifted['interval'] = rho[lifted['interval']]
                assert lifted in coarse_primitives
            totals['individual_primitive_embeddings'] += len(primitives)
            zf, zc = optimize(*fdata), optimize(*cdata)
            assert (zf['value'], zf['cost']) == (f['value'], f['cost'])
            assert (zc['value'], zc['cost']) == (c['value'], c['cost'])
            totals['independent_primitive_optima_pairs'] += 1
        totals['complete_pool_or_joint_withdrawal_comparisons'] += 1
    if port:
        fr, _ = port_graph(cur, fine)
        cr, _ = port_graph(cur, coarse)
        for field in ('alpha', 'beta', 'mixed', 'raw', 'slack', 'd4', 'seam', 'cross_direction_M'):
            assert fr[field] == cr[field]
        assert cr['boundary'] <= fr['boundary'] and cr['port_deficit'] <= fr['port_deficit']
        totals['terminal_tax_monotonicity_checks'] += 1
    totals['general_coarsening_models'] += 1
    return dict(fine_regions=len(fine), canonical_regions=len(coarse), raw=len(fd[4]),
                old_value=fork_flow(*fd)['value'], new_value=fork_flow(*cd)['value'])


def vertical_segments(R, C, removed):
    """A removed cut is (even row coordinate, even column-pair coordinate)."""
    assert removed <= set(itertools.product(range(2, R, 2), range(0, C, 2)))
    result = []
    for c in range(0, C, 2):
        cuts = [0]+[r for r in range(2, R, 2) if (r, c) not in removed]+[R]
        result += [rectangle(a, b, c, c+2, True) for a, b in zip(cuts, cuts[1:])]
    return result


def family_profile(w, k, cur, removed, totals, independent=False):
    R, C, T, M = cur
    direct_check(*cur)
    assert seals(w, k) <= T
    regions = vertical_segments(R, C, removed)
    data, closed, N = compile_model(cur, regions)
    own, A, B, X = owner_data(*data[:2])
    assert A == {own[1, 10*i+3] for i in range(k)}
    loss = cover(w, k, cur)
    hit, h = [], []
    for i in range(k):
        c = 10*i
        a = own[1, c+3]
        assert set(data[1][a]) == {(1, c+3), (w, c+3)}
        assert not any(own[p] == a and own[q] != a for p, q in data[2])
        opened = bool({(2, c+2), (w, c+2)} & removed)
        caps = loss[0, c+4]+loss[w, c+4]
        hit.append(opened)
        h.append(caps)
        assert bool(data[3][a]) == (opened or caps > 0)
        assert all({o for o, W in data[3].items() if j in W} == {a} for j in data[3][a])
    f = fork_flow(*data)
    expected = sum(opened or caps > 0 for opened, caps in zip(hit, h))
    assert (f['value'], f['deficit'], f['cost']) == (expected, k-expected, 0)
    ell = sum(loss.values())
    q = sum(hit)
    assert ell+f['deficit']+q >= k
    assert q <= len(removed)
    canonical, _, sameN = compile_model(cur, canonical_bands(R, C, regions))
    assert sameN == N
    full = fork_flow(*canonical)
    assert (full['value'], full['deficit'], full['cost']) == (k, 0, 0)
    if independent:
        z = optimize(*data)
        assert (z['value'], z['cost']) == (f['value'], f['cost'])
        totals['family_independent_primitive_optima'] += 1
    totals['arbitrary_T_and_cut_profiles'] += 1
    return dict(w=w, k=k, size=len(T), ell=ell, joins=len(removed), hit_modules=q,
                central_cap_losses=h, value=f['value'], deficit=f['deficit'], links=f['cost'])


def random_board(R, C, rng):
    sites = list(itertools.product(range(R), range(C)))
    rng.shuffle(sites)
    P, M = set(), []
    for r, c in sites:
        if (r, c) in P or rng.random() < .5:
            continue
        near = [(a, b) for a, b in ((r+1, c), (r, c+1)) if a < R and b < C and (a, b) not in P]
        if near:
            v = rng.choice(near)
            M.append(((r, c), v))
            P |= {(r, c), v}
    return add_selections((R, C, set(), M), rng)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    totals, rng, records = Counter(), random.Random(2026102617), []
    from check_adjacent_band_boundary_repair import copies
    from check_degree_changing_bent_completions import family as bent
    from rotor_networks import chain
    from degree_three_fusion import four_way, corner_join
    boards = [configuration(8, 1), bent(8), copies(1), chain(1)[0], four_way(8)[0], corner_join(8)[0]]
    for bi, cur in enumerate(boards):
        R, C = cur[:2]
        partitions = [[rectangle(0, R, 0, C, v)] for v in (False, True)]
        if bi == 0:
            partitions.append(mixed_regions(8, 1))
        r, c = R//4*2, C//4*2
        boxes = [(0, r, 0, c), (0, r, c, C), (r, R, 0, c), (r, R, c, C)]
        partitions += [[rectangle(*box, bool(mask >> j & 1)) for j, box in enumerate(boxes)] for mask in range(16)]
        for repeat in range(4):
            partitions.append([rectangle(r, r+2, c, c+2, bool(rng.randrange(2)))
                               for r in range(0, R, 2) for c in range(0, C, 2)])
        for pi, regions in enumerate(partitions):
            for fine in (regions, tile_refinement(R, C, regions)):
                rec = check_coarsening(cur, fine, totals, independent=bi == 0 and pi < 3,
                                      withdrawal=pi < 3, port=True)
                if bi == 0:
                    records.append(dict(board=bi, partition=pi, **rec))
    # No freezing/terminal-degree assumptions in the coarsening theorem.
    for repeat in range(80):
        R, C = rng.choice((4, 6)), rng.choice((4, 6))
        cur = random_board(R, C, rng)
        regions = [rectangle(r, r+2, c, c+2, bool(rng.randrange(2)))
                   for r in range(0, R, 2) for c in range(0, C, 2)]
        check_coarsening(cur, regions, totals, independent=True, withdrawal=repeat < 8)
        totals['unfrozen_random_geometry_controls'] += 1
    sharp = []
    fixture = None
    for w, k in itertools.product((8, 10, 14, 32, 64), (1, 2, 3, 7)):
        base = configuration(w, k)
        R, C = base[:2]
        # Exact joint quotas: at most s axial cut removals, final deficit<=d.
        for s, d in itertools.product(range(k+1), repeat=2):
            q = min(s, k-d)
            deleted = {(0, 10*i+5) for i in range(q, k-d)}
            removed = {(2, 10*i+2) for i in range(q)}
            cur = (R, C, base[2]-deleted, base[3])
            z = family_profile(w, k, cur, removed, totals, independent=w == 8 and k <= 2)
            assert z['size'] == (7*k+2)*(w//2)+3*k+2-max(0, k-d-s)
            assert z['deficit'] == d
            ranks = fast_rank_certificate(cur, inventory_schedule(w, k))
            totals['strict_freezing_events'] += len(ranks)
            totals['sharp_frozen_joint_quota_attainers'] += 1
            if w == 8:
                sharp.append(dict(switch_budget=s, deficit_threshold=d, **z))
            if (w, k, s, d) == (8, 2, 1, 1):
                fixture = dict(shape=cur[:2], selected=sorted(cur[2]), matching=cur[3],
                               removed_cuts=sorted(removed), freezing_layers=inventory_schedule(w, k), expected=z)
        # Full T*, arbitrary joins: exhaust all effective upper/lower choices
        # on small k and mix in irrelevant cuts elsewhere.
        gates = [(r, 10*i+2) for i in range(k) for r in (2, w)]
        masks = range(1 << len(gates)) if k <= 3 else [0, 1, (1 << len(gates))-1]
        for mask in masks:
            removed = {gate for i, gate in enumerate(gates) if mask >> i & 1}
            removed |= {(r, c) for r in range(2, R, 2) for c in range(0, C, 2)
                        if (r, c) not in gates and rng.random() < .08}
            z = family_profile(w, k, base, removed, totals)
            assert z['value'] == z['hit_modules']
            totals['maximum_T_arbitrary_cut_profiles'] += 1
        for repeat in range(10):
            bare = (R, C, seals(w, k), base[3])
            cur = add_selections(bare, rng)
            if repeat % 2:
                cur = (R, C, {v for v in sorted(cur[2]) if v in seals(w, k) or rng.randrange(2)}, base[3])
            removed = {(r, c) for r in range(2, R, 2) for c in range(0, C, 2) if rng.random() < .3}
            family_profile(w, k, cur, removed, totals, independent=k == 1 and repeat < 2)
            totals['T_rebuilt_from_only_leaf_seals'] += 1
    path = Path(__file__).parent/'fixtures/canonical_band_coarsening_w8_k2.json'
    path.write_text(json.dumps(fixture, indent=2)+'\n')
    saved = json.loads(path.read_text())
    cur = (*saved['shape'], set(map(tuple, saved['selected'])), [tuple(map(tuple, e)) for e in saved['matching']])
    assert family_profile(8, 2, cur, set(map(tuple, saved['removed_cuts'])), totals, True) == saved['expected']
    fast_rank_certificate(cur, [[tuple(v) for v in layer] for layer in saved['freezing_layers']])
    args.output.write_text(json.dumps(dict(status='PASS', counts=dict(totals), general_records=records,
        sharp_quota_records=sharp,
        theorem='For every feasible T,M and aligned even-rectangle HV partition, canonical maximal H tile-row/V tile-column bands retain N and every global owner, give a bijection of positive original forests, embed all old supports and links, and dominate full payment for every jointly transported original pool and prescribed old source set. No new slack unit. Terminal d4,s,eHV unchanged; b and port deficit nonincreasing when terminal degrees>=3.',
        family='All even W>=8,k>=1; arbitrary sealed final T and vertical band cuts: source i is payable iff at least one of its upper/lower guard cuts is removed or either central cap loses its selection. Every source support is private and no source has terminal exits. V=count(payable), minlinks0; ell+D+number_hit_modules>=k. Frozen optimum with at most s cut removals and D<=d is tau-max(0,k-d-s). T* has value0 on 2x2 tiles and valuek on canonical bands with same N,raw2k,d4=s=eHV0.',
        limits=['Coarsening is proved for the existing within-band support/link model; arbitrary extra cross-band links are not assumed absent in a larger model.',
                'General coordinate/forest adapters have written proofs and executable checks; formal scope is separate.',
                'The orientation mosaic is still to be optimized; no universal5/6 improvement.']), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(totals)), indent=2))


if __name__ == '__main__':
    main()
