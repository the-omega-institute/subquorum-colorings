"""Check whole-beta and interval allocations in fully frozen occupied bands."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_native_guard_compensation import force_matching
from check_one_sided_interval_allocation import allocate, independent_maximum
from check_residual_corridors import direct_check, transformed
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, extended_ports, terminal_data,
)
from degree_three_fusion import occupied_bands


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def control(current, totals):
    direct_check(*current)
    force_matching(current, totals)
    bands = whole_bands(current)
    original, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
    extended = extended_ports(current, bands, labels, intervals, owners, kinds, ports, Counter())
    alphas = sorted(pair for pair in pairs if all(kinds[point] == 'TP' for point in pair))
    betas = sorted(pair for pair in pairs if all(kinds[point] == 'BP' for point in pair))
    marked = {owners[band, column] for band in range(len(bands))
              for column in (0, len(bands[band])-1)}
    incidence = {('interval', resource): set() for resource in range(len(intervals))
                 if resource not in marked}
    for demand, pair in enumerate(alphas):
        for point in pair:
            for port in extended[point]:
                if owners[port] not in marked:
                    incidence['interval', owners[port]].add(demand)
    witnesses = {}
    for resource, beta in enumerate(betas):
        candidates = {}
        for demand, alpha in enumerate(alphas):
            choices = [(first, second) for first in alpha for second in beta
                       if first[0] == second[0] and abs(first[1]-second[1]) == 1]
            if choices:
                candidates[demand] = min(choices)
        retained = sorted(candidates)[:2]
        incidence['beta', resource] = set(retained)
        witnesses.update({(demand, resource): candidates[demand] for demand in retained})
        totals['candidate_beta_owner_incidences'] += len(retained)
        totals['beta_lists_requiring_owner_truncation'] += len(candidates) > 2
    allocation = allocate(len(alphas), incidence)
    assert len(allocation['assignment']) == independent_maximum(len(alphas), incidence)
    chosen = [witnesses[demand, resource[1]]
              for demand, resource in allocation['assignment'].items() if resource[0] == 'beta']
    reduced, inventory, _ = cancel_pairs(kinds, pairs, chosen, Counter())
    assert inventory['TP', 'TP'] == len(alphas)-len(chosen)
    assert inventory['BP', 'BP'] == len(betas)-len(chosen)
    reduced_pairs = {frozenset(pair) for pair in reduced}
    for demand, resource in allocation['assignment'].items():
        if resource[0] == 'interval':
            assert frozenset(alphas[demand]) in reduced_pairs
            assert any(owners[port] == resource[1] for point in alphas[demand] for port in extended[point])
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*(
        len(allocation['spare_resources'])-len(allocation['deficient']))
    totals['frozen_beta_adapter_models'] += 1
    totals['nonempty_beta_link_allocations'] += bool(chosen)
    totals['whole_beta_owners_consumed'] += len(chosen)
    totals['interval_demands_preserved'] += sum(resource[0] == 'interval'
                                              for resource in allocation['assignment'].values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    for width in range(6, 25, 2):
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*occupied_bands(width)[0], *symmetry)
            for row_shift, column_shift in itertools.product((2, 3), repeat=2):
                move = lambda point: (point[0]+row_shift, point[1]+column_shift)
                current = (2*((shape[0]+7)//2), 2*((shape[1]+7)//2),
                           {move(point) for point in selected},
                           [tuple(map(move, edge)) for edge in matching])
                control(current, totals)
    assert totals['nonempty_beta_link_allocations'] > 0
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals),
        scope='Actual fully frozen occupied-band controls with whole original beta resources. '
              'Conditional beta incidence selection is explicit; the general proof is written.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
