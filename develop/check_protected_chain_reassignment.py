"""Check arbitrary protected roots and unavoidable interval reassignment."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import physical
from check_native_guard_compensation import force_matching
from check_one_sided_interval_allocation import allocate, chain_family
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, extended_ports, terminal_data,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def control(width, count, totals):
    current, bands, fixed = chain_family(width, count)
    direct_check(*current)
    force_matching(current, totals)
    original, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
    access = extended_ports(current, bands, labels, intervals, owners, kinds, ports, Counter())
    reduced, inventory, _ = cancel_pairs(kinds, pairs, fixed, Counter())
    alphas = [pair for pair in reduced if all(kinds[point] == 'TP' for point in pair)]
    assert len(alphas) == count and inventory['BP', 'BP'] == 0
    assert all(all(8*index+3 <= point[1] <= 8*index+7 for point in pair)
               for index, pair in enumerate(alphas))
    shared = [owners[0 if index % 2 == 0 else len(bands)-1, 9+8*index]
              for index in range(count-1)]
    marked = {owners[band, column] for band in range(len(bands))
              for column in (0, len(bands[band])-1)}
    resources = set(range(len(intervals)))-marked
    root_costs = []
    for root in range(count):
        assignment = {index if index < root else index+1: resource
                      for index, resource in enumerate(shared)}
        result = physical(current, bands, fixed, totals, protected=True,
                          protected_assignment=assignment)
        assert len(result['protected_assignment']) == count-1
        if root == count-1:
            assert result['value'] == 0 and result['deficit'] == 1
            assert result['cut'] == [] and len(result['blocked']) == 1
            root_costs.append(None)
        else:
            expected = 1 if root == 0 else 2
            assert result['value'] == 1 and result['cost'] == expected
            root_costs.append(expected)
        totals['externally_specified_protected_roots'] += 1
    free_kinds = {point: kinds[point] for pair in reduced for point in pair}
    choices = [(first, second) for first in free_kinds for second in free_kinds
               if kinds[first] == 'TP' and kinds[second] == 'BP'
               and first[0] == second[0] and abs(first[1]-second[1]) == 1]
    full_extensions = []
    for link in choices:
        final, final_inventory, _ = cancel_pairs(kinds, pairs, fixed+[link], Counter())
        final_alphas = [pair for pair in final if all(kinds[point] == 'TP' for point in pair)]
        assert len(final_alphas) == count and final_inventory['BP', 'BP'] == 0
        assert all(all(8*index+3 <= point[1] <= 8*index+7 for point in pair)
                   for index, pair in enumerate(final_alphas))
        incidence = {resource: {index for index, pair in enumerate(final_alphas)
                                if any(any(owners[port] == resource for port in access[point])
                                       for point in pair)} for resource in resources}
        allocation = allocate(count, incidence)
        totals['all_single_additional_link_controls'] += 1
        if len(allocation['assignment']) == count:
            full_extensions.append(link)
            root_resource = owners[len(bands)-1, 9]
            expected = {0: root_resource}
            expected.update({index+1: resource for index, resource in enumerate(shared)})
            assert allocation['assignment'] == expected
            assert all(allocation['assignment'][index] != shared[index]
                       for index in range(count-1))
            totals['old_interval_assignments_forced_to_change'] += count-1
    assert full_extensions == [((width+4, 5), (width+4, 6))]
    if count >= 3:
        pivot = count-2
        protected = {index: shared[index] for index in range(pivot)}
        result = physical(current, bands, fixed, totals, protected=True,
                          protected_assignment=protected)
        assert result['value'] == 2 and result['cost'] == 2
        row = 5 if (pivot-1) % 2 == 0 else width+4
        extra = [((row, 8*pivot+3), (row, 8*pivot+4)),
                 ((row, 8*pivot+5), (row, 8*pivot+6))]
        final, _, _ = cancel_pairs(kinds, pairs, fixed+extra, Counter())
        final_alphas = [pair for pair in final if all(kinds[point] == 'TP' for point in pair)]
        band = 0 if row == 5 else len(bands)-1
        new_resource = owners[band, 9+8*pivot]
        assert new_resource in resources and new_resource not in shared
        assignment = dict(protected)
        assignment[pivot] = new_resource
        assignment[pivot+1] = shared[pivot]
        assert len(assignment) == count and len(set(assignment.values())) == count
        for demand, resource in assignment.items():
            assert any(any(owners[port] == resource for port in access[point])
                       for point in final_alphas[demand])
        totals['two_link_one_reassignment_controls'] += 1
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*(3*width-9)*count > 0
    totals['fully_frozen_shared_chain_families'] += 1
    return dict(width=width, count=count, protected_root_full_repair_costs=root_costs,
                unique_one_link_full_extension=full_extensions[0],
                old_assignments_changed_at_one_link_optimum=count-1,
                two_link_repair_changes_one_assignment=count >= 3,
                margin=(3*width-9)*count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for width, count in itertools.product((6, 8, 12), range(2, 25)):
        record = control(width, count, totals)
        if (width, count) in ((6, 2), (8, 3), (12, 24)):
            examples.append(record)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals),
        examples=examples, scope='Finite controls for the written arbitrary-length protected-root '
        'classification and unbounded old-allocation reassignment at the one-link optimum. '
        'Targets remain positive; no counterexample to the grid inequality is asserted.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
