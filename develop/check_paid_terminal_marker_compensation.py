"""Check payment transport through marked open relays without resource reuse."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory, matchings
from check_mixed_relay_orientation import forest_budget, model
from check_terminal_cancellation_and_stranded_demand import components


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def marked_model(sources, sizes, kinds, paid_ends, cycle_sizes):
    vertices, actual, auxiliary, chosen, free, colours, cycles = model(sources, sizes, cycle_sizes)
    markers = {}
    for index, (size, kind, paid_end) in enumerate(zip(sizes, kinds, paid_ends)):
        path = [('m', index, position) for position in range(2*size+2)]
        free[path[0]] = 'BP' if kind == 'beta' else 'TP'
        free[path[-1]] = 'TP' if kind == 'alpha' else 'BP'
        defect = (0 if paid_end == 0 else 2*size) if kind == 'alpha' else 0 if kind == 'beta' else -1
        current = -1 if kind == 'beta' else 1
        colours[path[0]] = current
        for position in range(len(path)-1):
            if position != defect:
                current = -current
            colours[path[position+1]] = current
        if kind == 'alpha':
            edge = frozenset((path[defect], path[defect+1]))
            markers[edge] = (path[0] if paid_end == 0 else path[-1], index)
    assert all(colours[point] == (1 if kind == 'TP' else -1) for point, kind in free.items())
    assert {frozenset(edge) for edge in actual if colours[edge[0]] == colours[edge[1]] == 1} == set(markers)
    assert all(colours[first]+colours[second] == 0 for first, second in auxiliary)
    return (vertices, actual, auxiliary, chosen, free, colours, cycles), markers


def verify(data, markers, relay_kinds, replacement, totals):
    vertices, actual, auxiliary, chosen, free, colours, cycles = data
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices-set(free)
    records = components(vertices, actual+replacement)
    physical = chosen | free
    counts = inventory(records, physical)
    paid, unused_betas = relay_kinds.count('alpha'), relay_kinds.count('beta')
    used_units, error_witnesses, unpaid = set(), set(), 0
    for record in records:
        if not record['ends'] or not all(physical[point] == 'TP' for point in record['ends']):
            continue
        local_markers = [edge for edge in markers if edge <= record['vertices']]
        if local_markers:
            paid_point, unit = markers[local_markers[0]]
            assert paid_point in record['ends'] and paid_point in free and free[paid_point] == 'TP'
            assert unit not in used_units
            used_units.add(unit)
        else:
            unpaid += 1
            local_errors = [frozenset(edge) for edge in replacement
                            if set(edge) <= record['vertices']
                            and colours[edge[0]] == colours[edge[1]] == -1]
            assert local_errors and local_errors[0] not in error_witnesses
            error_witnesses.add(local_errors[0])
    assert counts['alpha'] == len(used_units)+unpaid
    assert used_units <= {unit for _, unit in markers.values()}
    minimum = len(replacement)
    for flips in itertools.product((-1, 1), repeat=len(cycles)):
        signs = dict(colours)
        for cycle, flip in zip(cycles, flips):
            signs.update({point: colours[point]*flip for point in cycle})
        negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
        positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
        assert positive == negative
        assert counts['alpha'] <= paid+negative and counts['beta'] <= unused_betas+negative
        assert unpaid <= negative
        for record in records:
            local = record['vertices']
            new_ends = [point for edge in replacement if edge[0] in local for point in edge]
            old_ends = [point for edge in actual if edge[0] in local for point in edge]
            assert Counter(new_ends+list(local & set(free))) == Counter(old_ends+list(local & set(chosen)))
            boundary = sum(-1 if physical[point] == 'TP' else 1 for point in record['ends'])
            assert sum(signs[point] for point in new_ends)-sum(signs[point] for point in old_ends) == boundary
        if negative == 0:
            assert unpaid == 0 and len(used_units) == counts['alpha']
            cancelled = paid-counts['alpha']
            assert 0 <= cancelled <= min(paid, unused_betas)
            assert counts['beta'] == unused_betas-cancelled
            assert counts['mixed'] == relay_kinds.count('mixed')+len(chosen)//2+2*cancelled
            totals['coherent_payment_transport_certificates'] += 1
        minimum = min(minimum, negative)
        totals['signed_marker_controls'] += 1
    errors, rank = forest_budget(replacement, colours, cycles, {'alpha': unpaid})
    assert (errors == 0) == (minimum == 0)
    if rank <= 1:
        assert unpaid == 0
        totals['low_rank_all_final_alphas_paid'] += 1
    tails = {(('T' if point[0] == 't' else 'P'), point[1], 0): kind for point, kind in chosen.items()}
    full_actual = actual+[(point, (('T' if point[0] == 't' else 'P'), point[1], 0)) for point in chosen]
    full_vertices = vertices | set(tails)
    original = inventory(components(full_vertices, full_actual+auxiliary), physical | tails)
    sources = len(chosen)//2
    assert (original['alpha'], original['beta'], original['mixed']) == (
        sources+paid, sources+unused_betas, relay_kinds.count('mixed'))
    assert inventory(components(full_vertices, full_actual+replacement), free | tails) == counts
    totals['general_paid_marker_replacements'] += 1
    totals['final_alpha_payments_transported'] += len(used_units)
    totals['unpaid_alpha_distinct_error_witnesses'] += unpaid


def misplaced_marker_control():
    data, markers = marked_model(1, (1,), ('alpha',), (1,), ())
    vertices, actual, auxiliary, chosen, free, colours, cycles = data
    source, donor = ('t', 0, 0), ('p', 0, 0)
    first, second = ('m', 0, 1), ('m', 0, 2)
    paid_point = ('m', 0, 0)
    replacement = [(source, second), (first, donor)]
    assert all(colours[first]+colours[second] == 0 for first, second in replacement)
    records = components(vertices, actual+replacement)
    physical = chosen | free
    alpha = next(record for record in records if record['ends']
                 and all(physical[point] == 'TP' for point in record['ends']))
    assert paid_point not in alpha['vertices']
    assert any(edge <= alpha['vertices'] for edge in markers)
    return dict(status='CHECKED', actual_endpoints=len(vertices)+len(chosen),
                coherent_for_wrong_marker=True, original_paid_endpoint_leaves_final_alpha=True,
                failure='Moving the sign defect away from the actual paid terminal does not transport its access certificate.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    for sources in (1, 2):
        for relay_count in (1, 2):
            for sizes in itertools.product(range(2), repeat=relay_count):
                for kinds in itertools.product(('alpha', 'beta', 'mixed'), repeat=relay_count):
                    choices = [(0, 1) if kind == 'alpha' else (0,) for kind in kinds]
                    for paid_ends in itertools.product(*choices):
                        for cycle_pairs in range(2):
                            if sources+sum(sizes)+cycle_pairs > 5:
                                continue
                            data, markers = marked_model(sources, sizes, kinds, paid_ends,
                                                         () if cycle_pairs == 0 else (cycle_pairs,))
                            vertices, _, _, _, free, _, _ = data
                            domain = vertices-set(free)
                            for replacement in matchings(sorted(domain)):
                                if 2*len(replacement) == len(domain):
                                    verify(data, markers, kinds, replacement, totals)
    record = dict(status='PASS', totals=dict(totals), misplaced_marker=misplaced_marker_control(),
                  scope='All complete N replacements with 1..2 selected alpha/beta pairs; '
                  '1..2 internal alpha/beta/mixed relays, 0..1 PP pair per relay, both paid '
                  'end choices, 0..1 cycle pair, at most ten N-covered vertices. '
                  'All cycle flips, incidence counts, full tails, actual marker identities, '
                  'endpoint-based old-unit transport, distinct error edges and parity rank. '
                  'No physical interval access or grid embedding is asserted by this abstract checker.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
