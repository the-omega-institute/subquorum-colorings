#!/usr/bin/env python3
"""Enumerate bounded simple LL paths with capacity-one internal tiles.

The existing patch builder supplies physical corners and forced saturated
attachments. A reported witness is a full finite rectangle after blank padding,
not an abstract residual multigraph. Exhaustion applies only to this path class.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from grid_three_step_patterns import (
    CORNERS, Conflict, Patch, add, point, tile_of, corner_of,
)
from verify_grid_short_path_compensation import graph, feasible, residual

DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))


def partial_check(patch):
    for vertex, state in patch.states.items():
        if state == 'T' and sum(
            patch.states.get(add(vertex, d), 'B') != 'B' for d in DIRECTIONS
        ) > 1:
            raise Conflict('T_degree')


def rectangle(patch):
    tiles = [tile_of(p) for p in patch.states]
    lo = tuple(min(t[i] for t in tiles) for i in (0, 1))
    hi = tuple(max(t[i] for t in tiles) for i in (0, 1))
    m, n = (2 * (hi[i] - lo[i] + 1) for i in (0, 1))
    index = lambda p: (p[0] - 2*lo[0])*n + p[1] - 2*lo[1]
    T = sum(1 << index(v) for v, s in patch.states.items() if s == 'T')
    M = tuple(sorted((min(index(u), index(v)), max(index(u), index(v)))
                     for u, v in patch.mate.items() if u < v))
    assert feasible(graph(m, n)[0], T, M)
    g = residual(m, n, T, M)
    return dict(m=m, n=n, T=[v for v in range(m*n) if T >> v & 1],
                M=M, q=T.bit_count()+len(M)-m*n//2,
                internal_matching_edges=sum(g['h']))


def search(length, allow_internal):
    counts = dict(partial_candidates=0, completed_patches=0)
    witnesses = []
    canonical_witnesses = set()
    kinds = ['T0', 'T1', 'S0', 'S1'] + (['H'] if allow_internal else [])

    def extend(patch, entry, depth, route, types):
        tile, ec = tile_of(entry), corner_of(entry)
        if tile in patch.roles:
            return
        # All capacity-one two-port shapes have adjacent residual corners.
        for xc in CORNERS:
            if sum(abs(ec[i]-xc[i]) for i in (0, 1)) != 1:
                continue
            endpoint = point(tile, xc)
            for direction in DIRECTIONS:
                nxt = add(endpoint, direction)
                nt = tile_of(nxt)
                if nt == tile or nt in patch.roles:
                    continue
                for kind in kinds:
                    counts['partial_candidates'] += 1
                    p = copy.deepcopy(patch)
                    try:
                        p.central(tile, (ec, xc), kind)
                        partial_check(p)
                        if depth == length-1:
                            for leafkind in range(3):
                                final = copy.deepcopy(p)
                                try:
                                    final.leaf(endpoint, direction, leafkind)
                                    final.finish()
                                except Conflict:
                                    continue
                                counts['completed_patches'] += 1
                                canonical_witnesses.add(canonical(rectangle(final)))
                                if len(witnesses) < 3:
                                    witnesses.append(dict(route=route+[tile, nt],
                                        types=types+[kind, 'leaf'+str(leafkind)],
                                        rectangle=rectangle(final)))
                        else:
                            p.edge(endpoint, nxt)
                            partial_check(p)
                            extend(p, nxt, depth+1, route+[tile], types+[kind])
                    except Conflict:
                        continue

    for leafkind in range(3):
        p = Patch()
        p.leaf((0, 2), (0, -1), leafkind)
        extend(p, (0, 2), 1, [(0, 0)], ['leaf'+str(leafkind)])
    return dict(length=length, allow_internal=allow_internal,
                counts=counts, witnesses=witnesses,
                canonical_witnesses=sorted(canonical_witnesses),
                scope='Simple tile paths; every internal capacity is one; fixed first edge up to lattice symmetries.')


def canonical(record):
    m, n = record['m'], record['n']
    candidates = []
    for transpose in (False, True):
        for fi in (False, True):
            for fj in (False, True):
                a, b = (n, m) if transpose else (m, n)
                def transform(v):
                    i, j = divmod(v, n)
                    i = m-1-i if fi else i
                    j = n-1-j if fj else j
                    return j*b+i if transpose else i*b+j
                T = sorted(transform(v) for v in record['T'])
                M = sorted(sorted((transform(u), transform(v))) for u, v in record['M'])
                candidates.append(json.dumps([a,b,T,M], separators=(',', ':')))
    return hashlib.sha256(min(candidates).encode()).hexdigest()


def classification_control():
    from grid_three_step_patterns import classification
    expected = set()
    for example in classification()['all_examples']:
        p = Patch()
        p.states = {tuple(v):s for v,s in example['states']}
        for u,v in example['edges']:
            p.mate[tuple(u)] = tuple(v)
            p.mate[tuple(v)] = tuple(u)
        expected.add(canonical(rectangle(p)))
    actual = search(3, True)
    assert set(actual['canonical_witnesses']) == expected
    return dict(status='MATCHES_EARLIER_CLASSIFICATION',
                canonical_configurations=len(expected), enumerated=actual['counts']['completed_patches'],
                scope='Different enumeration orders; shared patch builder. Not an independent proof of the all-length question.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', type=int, required=True)
    parser.add_argument('--allow-internal', action='store_true')
    parser.add_argument('--through', type=int)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 2 <= args.length <= 8:
        parser.error('length must be between 2 and 8')
    last = args.through if args.through is not None else args.length
    if not args.length <= last <= 8:
        parser.error('through must be between length and 8')
    records = [search(length, args.allow_internal) for length in range(args.length, last+1)]
    result = records[0] if len(records) == 1 else dict(records=records)
    result['classification_control'] = classification_control()
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps([{k:v for k,v in record.items() if k != 'witnesses'} for record in records]), flush=True)
