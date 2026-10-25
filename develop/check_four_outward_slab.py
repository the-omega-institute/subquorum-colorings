"""Explicit all-length frozen obstruction; no discovery solver is required.

See FOUR_OUTWARD_SLAB_AND_ONE_UNIT_OBSTRUCTION.md for the general proof.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_cooperative_promotion import neighbors
from check_crossing_matching_ports import rectangle, strand_parts, compile_partition
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed
from check_whole_support_fork_normal_form import brute

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def slab(h):
    assert h >= 1
    selected = {(r, c) for r in range(2*h+4)
                for c in ((1, 6) if r % 2 == 0 else (0, 7))}
    selected |= {(2*h+3, 2), (2*h+3, 5)}
    matching = [((0, 2), (0, 3)), ((0, 4), (0, 5)),
                ((1, 3), (1, 4)), ((2, 3), (2, 4))]
    matching += [((1, c), (2, c)) for c in (2, 5)]
    matching += [((r, c), (r+1, c)) for r in range(3, 2*h, 2)
                 for c in range(2, 6)]
    matching += [((2*h+1, 3), (2*h+1, 4))]
    matching += [((2*h+1, c), (2*h+2, c)) for c in (2, 5)]
    return 2*h+4, 8, selected, matching


def freezing_schedule(h):
    """The nine written waves, not a recomputed peeling certificate."""
    result = []
    def pair(row, columns):
        result.append([(row, c) for c in columns])
    for row in range(2*h+2, 1, -2):
        pair(row, (2, 5))
    pair(0, (2, 5))
    pair(1, (3, 4))
    pair(0, (3, 4))
    pair(1, (2, 5))
    pair(2, (3, 4))
    for row in range(3, 2*h, 2):
        pair(row, (3, 4))
    pair(2*h+1, (3, 4))
    for row in range(2*h, 3, -2):
        pair(row, (3, 4))
    for row in range(3, 2*h+2, 2):
        pair(row, (2, 5))
    return result


def inspect(cur, totals):
    R, C, T, M = cur
    objective = direct_check(*cur)
    P = {v for e in M for v in e}
    mate = {v: w for e in M for v, w in (e, e[::-1])}
    frozen, layers = frozen_certificate(cur)
    assert frozen == P
    totals['peeling_freezing_events'] += len(check_rank_certificate(
        cur, [[w['endpoint'] for w in layer] for layer in layers]))
    ledger = verify_terminal(cur)
    assert len(ledger['receivers']) == 1
    assert ledger['receivers'][0]['charge_twice'] == -2
    assert ledger['empty_deficit'] == 0 and R*C//2-objective == 1
    graph, _ = graph_record(*cur)
    q = [0 if t == 2 else d-2*r
         for t, d, r in zip(graph['t'], graph['deg'], graph['r'])]
    assert Counter(q) == Counter({0: R*C//4-2, -1: 2})
    assert sum(max(0, -x) for x in q) == 2
    centers = []
    for r, c in itertools.product(range(0, R, 2), range(0, C, 2)):
        cells = {(a, b) for a in (r, r+1) for b in (c, c+1)}
        if cells <= P and all(mate[v] not in cells for v in cells):
            i = r//2*(C//2)+c//2
            assert (graph['t'][i], graph['h'][i], graph['s'][i],
                    graph['r'][i], graph['deg'][i]) == (0, 0, 0, 2, 4)
            centers.append((r//2, c//2))
    totals['physical_models'] += 1
    totals['four_outward_centers'] += len(centers)
    return dict(shape=(R, C), selected=len(T), endpoints=len(P), matching=len(M),
                objective=objective, margin=1, negative_charge_twice=2,
                centers=centers, receiver=ledger['receivers'][0])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals = Counter()
    records = []
    for h in [*range(1, 33), 48, 64, 128]:
        cur = slab(h)
        checked = inspect(cur, totals)
        assert checked['endpoints'] == 8*h+10
        assert checked['selected'] == 4*h+10 and checked['matching'] == 4*h+5
        assert checked['objective'] == 8*h+15
        assert set(checked['centers']) == set(itertools.product(range(1, h+1), (1, 2)))
        schedule = freezing_schedule(h)
        totals['written_schedule_events'] += len(check_rank_certificate(cur, schedule))
        reg = rectangle(0, cur[0], 0, cur[1])
        P = {v for e in cur[3] for v in e}
        parts, _ = strand_parts(P, cur[2], cur[3], reg['bands'])
        assert Counter(x['kind'] for x in parts) == Counter({'TT': 1, 'cycle': 1})
        alpha = next(x for x in parts if x['kind'] == 'TT')
        cycle = next(x for x in parts if x['kind'] == 'cycle')
        assert len(alpha['body']) == 4*h+10 and len(cycle['body']) == 4*h
        assert cycle['body'] == set(itertools.product(range(2, 2*h+2), (3, 4)))
        for b in range(1, h+1):
            assert {(2*b, 2), (2*b+1, 2), (2*b, 5), (2*b+1, 5)} <= alpha['body']
        record, data = compile_partition(cur, [reg])
        expected, count = brute(*data)
        assert expected == (record['value'], record['cost']) == (1, 0)
        assert record['alpha'] == 1 and record['beta'] == 0 and record['raw'] == 2
        assert not data[2] and data[4] == {(h+1, 3, 3), (h+1, 4, 4)}
        assert list(data[3].values()) == [data[4]]
        totals['independent_full_pool_comparisons'] += 1
        totals['independent_terminal_matchings'] += count
        records.append(dict(h=h, **checked, pp_m_alpha_vertices=4*h+10,
                            pp_m_cycle_vertices=4*h, original_units=sorted(data[4]), payment=1))
    for h in (1, 2, 3, 8, 32):
        cur = slab(h)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, T, M = transformed(*cur, *symmetry)
            checked = inspect((*shape, T, M), totals)
            assert len(checked['centers']) == 2*h
            totals['symmetry_images'] += 1
    # Independent enumeration uses every omitted/first/second edge state.
    # The repository helper caps at eight edges; this nine-edge case uses
    # the same physical feasibility criterion directly, without peeling.
    cur = slab(1)
    occupied = cur[2] | {v for e in cur[3] for v in e}
    feasible = 0
    for states in itertools.product((0, 1, 2), repeat=len(cur[3])):
        bundle = [e if state == 1 else e[::-1]
                  for state, e in zip(states, cur[3]) if state]
        if not bundle:
            continue
        remaining = occupied-{w for _, w in bundle}
        feasible += all(sum(w in remaining for w in neighbors(v)) <= 1 for v, _ in bundle)
        totals['independent_nonempty_oriented_bundles'] += 1
    assert feasible == 0 and totals['independent_nonempty_oriented_bundles'] == 3**9-1
    smallest = slab(1)
    fixture = dict(h=1, shape=smallest[:2], selected=sorted(smallest[2]), matching=smallest[3],
                   frozen_schedule=freezing_schedule(1),
                   labels=[''.join('T' if (r, c) in smallest[2] else 'P' if (r, c) in
                       {v for e in smallest[3] for v in e} else '.' for c in range(8))
                       for r in range(6)])
    fixture_path = Path(__file__).parent/'fixtures/four_outward_one_unit_slab.json'
    assert json.loads(fixture_path.read_text()) == json.loads(json.dumps(fixture))
    report = dict(status='PASS', totals=dict(totals), family=records,
        refuted='Without unique-square hypothesis, even one aligned four-outward fully frozen square need not have two units of negative physical charge anywhere on the board; per-center independent credits also fail without bound.',
        proved='All h>=1 written construction and freezing proof; exactly 2h capacity-two centers, one repeated alpha and one PP/M cycle, two half-donor tiles and one-unit total margin.',
        scope='General construction/proof is written. Finite geometry/flow and all oriented bundle controls verify explicit instances; universal 5/6 improvement remains open. No email or manuscript changes.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **totals)))


if __name__ == '__main__':
    main()
