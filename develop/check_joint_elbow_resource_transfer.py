"""Simultaneous local elbow adapter, complete pools and nonadditive withdrawals."""
import argparse
from collections import Counter
import json
from pathlib import Path

from check_canonical_band_coarsening import canonical_bands, tile_directions, forests
from check_crossing_matching_ports import rectangle
from check_degree_changing_bent_completions import compile_model
from check_compensation_flow_normal_form import owner_data
from check_forced_mates_and_adjacent_maxima import configuration
from check_local_elbow_resource_transfer import adapter, omit
from check_mixed_terminal_defect import mixed_regions
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize, canonical

if not __debug__:
    raise RuntimeError('Assertions required; no -O.')


def joint(cur, regions, patches, totals, independent=False):
    R, C = cur[:2]
    regions = canonical_bands(R, C, regions)
    data, closed, _ = compile_model(cur, regions)
    bits = tile_directions(R, C, regions)
    oldforests = forests(cur, regions)
    oldcells = {j: oldforests[j][1] for j in data[4]}
    lost, targets, witnesses, affected = set(), set(), set(), set()
    allbands = [b for reg in regions for b in reg['bands']]
    for r, c in patches:
        ans = adapter(cur, regions, r, c)
        assert ans['target'] not in targets and not lost & ans['lost']
        targets.add(ans['target'])
        lost |= ans['lost']
        witnesses |= ans['lost_users']
        for x in (r, r+2):
            ids = [i for i, band in enumerate(allbands)
                   if ((x, c), (x+1, c)) in band]
            assert len(ids) == 1 and ids[0] not in affected
            affected.add(ids[0])
    flipped = {(x, c) for r, c in patches for x in (r, r+2)}
    for r, c in patches:
        assert not {(x, c) for x in (r-2, r+4) if 0 <= x < R} & flipped
    for tile in flipped:
        bits[tile] = True
    after = canonical_bands(R, C, [rectangle(r, r+2, c, c+2, b) for (r, c), b in bits.items()])
    new, nclosed, _ = compile_model(cur, after)
    assert data[:2] == new[:2] and set(data[2]) == set(new[2])
    assert [x['body'] for x in closed] == [x['body'] for x in nclosed]
    nf = forests(cur, after)
    newcells = {j: nf[j][1] for j in new[4]}
    assert {z for j, z in oldcells.items() if j not in lost} <= set(newcells.values())
    created = {j for j, z in newcells.items() if z not in set(oldcells.values())}
    assert len(created) == len(lost)
    supported_targets = set()
    for j in created:
        users = {o for o, W in new[3].items() if j in W}
        assert len(users) == 1 and users <= targets
        supported_targets |= users
    assert supported_targets == targets
    for o in data[3]:
        if o not in targets:
            assert {oldcells[j] for j in data[3][o]-lost} == {newcells[j] for j in new[3][o]}
    minus, rest = omit(data, targets), omit(data, targets, data[4]-lost)
    old, pm, pr, newflow = map(lambda d: fork_flow(*d), (data, minus, rest, new))
    rloss = pm['value']-pr['value']
    assert 0 <= rloss <= len(witnesses-targets) <= len(targets)
    assert (newflow['value'], newflow['cost']) == (len(targets)+pr['value'], pr['cost'])
    if old['value'] == pm['value']:
        assert newflow['value'] == old['value']+len(targets)-rloss
        assert newflow['value'] >= old['value']
        totals['joint_old_maximum_leaves_all_targets_unpaid'] += 1
    if independent:
        for d, flow in ((data, old), (minus, pm), (rest, pr), (new, newflow)):
            z = optimize(*d)
            assert (z['value'], z['cost']) == (flow['value'], flow['cost'])
            totals['independent_joint_primitive_optima'] += 1
    totals['physical_joint_models'] += 1
    totals['physical_joint_lost_units'] += len(lost)
    totals['physical_joint_distinct_targets'] += len(targets)
    return dict(patches=patches, targets=len(targets), old_value=old['value'],
                minus_value=pm['value'], residual_value=pr['value'], joint_rank_loss=rloss,
                new_value=newflow['value'], links=newflow['cost'])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    totals, records = Counter(), []
    for w, k in ((8, 1), (8, 2), (8, 3), (14, 3), (32, 5), (64, 7)):
        base = configuration(w, k)
        for mask in range(1, 1 << min(k, 3)):
            patches = [(0, 10*i+2) for i in range(k) if mask >> i & 1]
            for deleted in (set(), {(0, 10*i+5) for i in range(k) if i % 2 == 0}):
                cur = (*base[:2], base[2]-deleted, base[3])
                records.append(dict(w=w, k=k, **joint(cur, mixed_regions(w, k), patches, totals, w == 8)))
    # Completely specified abstract incidence counterexample to adding
    # single-withdrawal gains. It is not a claimed physical embedding.
    kinds, pairs, links = canonical('AAA')
    old = (kinds, pairs, [], {0: {0, 1}, 1: set(), 2: set()}, {0, 1})
    def withdrew(Q):
        d = (*old[:3], {o: W-Q for o, W in old[3].items()}, old[4]-Q)
        return fork_flow(*d)['value']
    assert withdrew(set()) == withdrew({0}) == withdrew({1}) == 1
    assert withdrew({0, 1}) == 0
    new = (kinds, pairs, [], {0: set(), 1: {2}, 2: {3}}, {2, 3})
    assert fork_flow(*new)['value'] == optimize(*new)['value'] == 2
    totals['abstract_nonadditive_joint_withdrawal_controls'] += 1
    args.output.write_text(json.dumps(dict(status='PASS', counts=dict(totals), records=records,
        abstract_control='Old b supports u1,u2; targets a1,a2 unpaid. Each individual withdrawal rank loss0, joint loss1. Replace ui with a private ai resource: oldV1,newV2,gain1. Abstract incidence only, not a physical or frozen-grid counterexample.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(totals)), indent=2))


if __name__ == '__main__':
    main()
