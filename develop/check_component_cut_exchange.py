"""Controls for the written all-even-height cut obstruction and square exchange.

The loops below validate explicit coordinates, not universal grid feasibility.
Actual physical edges, rather than endpoints, are the resource identities.
"""
from collections import Counter
import json
from pathlib import Path

from check_turning_edge_ownership import adapter, canonical, verify_owner
from check_two_row_signed_compensation import charges

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def board(h):
    assert h >= 6 and h % 2 == 0
    t = {(0, 1), (1, 0), (0, 3), (h-2, 0), (h-1, 1), (h-1, 3)}
    holes = {(0, 0), (0, 2), (2, 0), (h-3, 0), (h-1, 0), (h-1, 2)}
    edges = [((1, 1), (1, 2)), ((h-2, 1), (h-2, 2))]
    edges += [((r, 3), (r+1, 3)) for r in range(1, h-2, 2)]
    edges += [((r, c), (r+1, c)) for r in range(2, h-3, 2) for c in (1, 2)]
    edges += [((r, 0), (r+1, 0)) for r in range(3, h-4, 2)]
    return t, holes, [canonical(*e) for e in edges]


def alternating_groups(original, witness, sigma):
    """Check a disjoint resource partition, with one consistent charge map."""
    old, new = set(original), set(witness)
    assert {u for e in old for u in e} == {u for e in new for u in e} == set(sigma)
    common = old & new
    assert all(sigma[u]+sigma[v] <= 0 for u, v in common)
    assert all(sigma[u]+sigma[v] <= 0 for u, v in new)
    remaining = old ^ new
    adjacent = {}
    for u, v in remaining:
        adjacent.setdefault(u, set()).add(v)
        adjacent.setdefault(v, set()).add(u)
    assert all(len(vs) == 2 for vs in adjacent.values())
    paid = set(common)
    cycles = 0
    while remaining:
        component = set()
        seed = min(remaining)[0]
        seen = {seed}; pending = [seed]
        while pending:
            u = pending.pop()
            for v in adjacent[u]:
                component.add(canonical(u, v))
                if v not in seen:
                    seen.add(v); pending.append(v)
        old_group, new_group = component & old, component & new
        assert len(old_group) == len(new_group) >= 2
        assert not paid & old_group
        old_sum = sum(sigma[u]+sigma[v] for u, v in old_group)
        new_sum = sum(sigma[u]+sigma[v] for u, v in new_group)
        assert old_sum == new_sum <= 0
        positive = sum(max(0, sigma[u]+sigma[v]) for u, v in old_group)
        negative = sum(max(0, -sigma[u]-sigma[v]) for u, v in old_group)
        assert positive <= negative
        paid.update(old_group); remaining -= component; cycles += 1
    assert paid == old
    return cycles


def all_matchings(vertices):
    if not vertices:
        yield []
        return
    u = min(vertices)
    for v in sorted(vertices-{u}):
        if abs(u[0]-v[0])+abs(u[1]-v[1]) == 1:
            for tail in all_matchings(vertices-{u, v}):
                yield [canonical(u, v)]+tail


def check(h):
    t, holes, edges = board(h)
    data = adapter(h, 4, t, edges)
    assert data['holes'] == holes
    assert len(t) == len(holes) == 6 and len(edges) == 2*h-6
    assert len(t)+len(edges) == 2*h
    k = h//2
    source_trace = [(0, 0)]+[(i, 1) for i in range(k)]+[(k-1, 0)]
    cut = set(source_trace)
    assert len(cut) == k+2
    incident = set().union(*(set(data['incident'][b]) for b in cut))
    assert all((data['tile'](u) in cut) == (data['tile'](v) in cut) for u, v in edges)
    cut_demand = sum(data['demand'][b] for b in cut)
    assert cut_demand == h and len(incident) == h-1
    outside = set(data['demand'])-cut
    assert sum(data['demand'][b] for b in outside) == h-6
    assert len(set(range(len(edges)))-incident) == h-5
    # The previous horizontal signed ledger locates precisely the same reserve.
    sigma = {}; q = {}
    for b in data['demand']:
        r, c = 2*b[0], 2*b[1]
        word = {(i, j): 1 if (r+i, c+j) in t else
                2 if (r+i, c+j) in data['occupied'] else 0
                for i in range(2) for j in range(2)}
        q[b], local, _ = charges(word)
        assert sum(local.values())-q[b] == 0
        sigma.update({(r+i, c+j): s for (i, j), s in local.items()})
    assert sum(q[b] for b in cut) == 2 and sum(q[b] for b in outside) == -2
    source_edge_charges = [sigma[u]+sigma[v] for i, (u, v) in enumerate(edges) if i in incident]
    reserve_edge_charges = [sigma[u]+sigma[v] for i, (u, v) in enumerate(edges) if i not in incident]
    assert sum(source_edge_charges) == 2 and min(source_edge_charges) >= 0
    assert sum(reserve_edge_charges) == -2 and max(reserve_edge_charges) <= 0
    # Partial ownership: all demands covered except one missing unit at B.
    a, b = (1, 0), (1, 1)
    removed = {canonical((2, 1), (3, 1)), canonical((2, 2), (3, 2))}
    added = {canonical((2, 1), (2, 2)), canonical((3, 1), (3, 2))}
    old_index = {e: i for i, e in enumerate(edges)}
    reserve = old_index[canonical((2, 1), (3, 1))]
    baseline = {e: z for z, es in data['loops'].items() for e in es if e != reserve}
    mid = source_trace.index(b)
    for i, (v, w) in enumerate(zip(source_trace, source_trace[1:])):
        es = data['between'][frozenset([v, w])]
        assert len(es) == 1
        baseline[es[0]] = v if i < mid else w
    for i in range(1, k-2):
        es = data['between'][frozenset([(i, 0), (i+1, 0)])]
        assert len(es) == 1
        baseline[es[0]] = (i, 0)
    counts = Counter(baseline.values())
    assert len(baseline) == len(edges)-1
    assert all(counts[z] == d-(z == b) for z, d in data['demand'].items())
    assert reserve not in baseline
    # This partial certificate is not passed off as a full certificate.
    assert all(e in data['incident'][z] for e, z in baseline.items())
    switched = [e for e in edges if e not in removed]+sorted(added)
    new_data = adapter(h, 4, t, switched)
    assert len(switched) == len(edges) and new_data['occupied'] == data['occupied']
    assert new_data['demand'] == data['demand']
    physical_owner = {edges[i]: z for i, z in baseline.items() if edges[i] not in removed}
    physical_owner.update({e: b for e in added})
    new_owner = {i: physical_owner[e] for i, e in enumerate(switched)}
    assert verify_owner(new_data, switched, new_owner) == dict(
        used_edges=len(edges), unused_edges=0, exact_tile_demands=True)
    # Read the repaired charges back on the ORIGINAL matching: one exceptional
    # old edge is +2 and its paired old square edge is -2, each used once.
    sigma_new = {}
    for i, (u, v) in enumerate(switched):
        owner_tile = new_owner[i]
        positive = u if new_data['tile'](u) == owner_tile else v
        sigma_new[u], sigma_new[v] = (1, -1) if positive == u else (-1, 1)
    original_charge = {e: sigma_new[e[0]]+sigma_new[e[1]] for e in edges}
    assert original_charge[canonical((2, 1), (3, 1))] == -2
    assert original_charge[canonical((2, 2), (3, 2))] == 2
    assert sum(original_charge[e] for e in removed) == 0
    assert all(c == 0 for e, c in original_charge.items() if e not in removed)
    assert all(q[z] <= sum(c for u, c in sigma_new.items() if data['tile'](u) == z)
               for z in data['demand'])
    assert sum(original_charge.values()) == 0
    assert alternating_groups(edges, switched, sigma_new) == 1
    # Additional finite controls cover ALL matchings on these two endpoint sets,
    # rather than repeating only one four-edge symmetric difference.
    matching_controls = 0; max_cycles = 0
    if h in (6, 8):
        for other in all_matchings(set(sigma_new)):
            adapter(h, 4, t, other)
            max_cycles = max(max_cycles, alternating_groups(other, switched, sigma_new))
            matching_controls += 1
        assert matching_controls > 1
    # Every surviving old physical resource keeps its former owner.
    assert all(physical_owner[edges[i]] == z for i, z in baseline.items()
               if edges[i] not in removed)
    return dict(height=h, width=4, J=2*h, cut_tiles=len(cut),
                cut_demand=cut_demand, distinct_cut_resources=len(incident),
                Hall_deficiency=1, cut_signed_excess=2, outside_signed_payment=-2,
                square_flip_removes=len(removed), square_flip_adds=len(added),
                full_ownership_after_flip=True,
                ownership_after_flip_retains_original_matching=False,
                original_M_grouped_charge_certificate=True,
                exceptional_original_edge_charges=[-2, 2],
                endpoint_set_and_matching_size_preserved=True,
                additional_all_matching_controls=matching_controls,
                max_alternating_cycles_in_controls=max_cycles)


def main():
    records = [check(h) for h in range(6, 105, 2)]
    result = dict(status='PASS', controls=len(records), smallest=records[0], largest=records[-1],
                  all_matching_controls=sum(r['additional_all_matching_controls'] for r in records),
                  all_matching_control_heights=[r for r in records if r['additional_all_matching_controls']],
                  scope='Coordinates, exact failed physical-resource Hall cut, signed ledger, explicit ownership after a single alternating square flip, paired -2/+2 accounting on the original matching, and 77 all-matching disjoint-cycle controls at heights 6 and 8. Written proof covers every even h>=6.',
                  refuted='Universal ownership feasibility for a fixed actual matching, even with unlimited intratile rerouting.',
                  not_refuted='Half-area numerical target. It holds with equality in this family.',
                  not_proved='Universal existence of a suitable rematching on arbitrary grids.')
    (ROOT/'output/component-cut-square-exchange.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
