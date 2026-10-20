"""Owner-role and height-order controls for the four-stem compensation proof."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_minus_one_tip_obstructions import source
from check_support_chain_compensation import incoming_chain
from check_width_eight_u_cap_obstruction import rotor_owners
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    first = {(1, column) for column in range(1, 7)}
    first |= {(row, column) for row in range(2, 7) for column in (2, 5)}
    second = first | {(row, 3) for row in range(2, 7)}
    assert rotor_owners((2, 3), first) == []
    assert rotor_owners((2, 4), second) == []
    counts = Counter()
    parameters = list(itertools.product((6, 8, 12), (4, 6, 10), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    for width, left_height, right_height in parameters:
        module = source(width, left_height, right_height)
        for symmetry in itertools.product((False, True), repeat=3):
            body = {affine(point, symmetry) for point in module['endpoints']}
            for endpoint in module['endpoints']:
                anchor = affine(endpoint, symmetry)
                for name, target, blockers in [('first', (2, 3), first), ('second', (2, 4), second)]:
                    counts[name+'_role_tests'] += 1
                    offset = target[0]-anchor[0], target[1]-anchor[1]
                    endpoints = {(point[0]+offset[0], point[1]+offset[1]) for point in body}
                    if endpoints & blockers:
                        continue
                    assert endpoint in ((left_height, 1), (right_height, width))
                    predecessor = affine((endpoint[0]-1, endpoint[1]), symmetry, offset)
                    assert predecessor == (target[0]+1, target[1])
                    counts[name+'_downward_tips'] += 1
    order_cases = 0
    for right, second_height, first_height, outer in itertools.product(range(4, 22, 2), repeat=4):
        if right+2 <= second_height and second_height+2 <= first_height and first_height+2 <= outer:
            assert right+6 <= outer
            for short in range(4, right+1, 2):
                long = outer+4
                assert short+10 <= long
                assert not long <= short+8
                order_cases += 1
    pool_cases = 0
    for single, paid, chain in itertools.product(range(17), repeat=3):
        if paid <= single and single-paid <= chain:
            assert single <= paid+chain
            assert -((single-paid-chain)//2) >= 0
            pool_cases += 1
    modules = [source(6, 14, 4),
               transform_module(source(12, 10, 4), (False, True, False), (12, 1)),
               transform_module(source(6, 4, 4), (False, True, False), (6, 4)),
               transform_module(source(10, 8, 4), (False, True, False), (10, 2)),
               transform_module(source(8, 6, 4), (False, True, False), (8, 3))]
    network = combine(modules)
    endpoints = network['endpoints']
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert incoming_chain(1, (2, 2), modules, endpoints) is None
    assert incoming_chain(4, (2, 4), modules, endpoints) is None
    assert (2, 4) in modules[2]['selected']
    assert {(2, 3), (2, 5)} <= endpoints
    assert {(2, 3), (2, 4)} <= modules[3]['endpoints'] | modules[4]['endpoints']
    bad_supports = sorted(point for point in network['selected']
                          if len(set(neighbors(point)) & (endpoints | network['selected'])) > 1)
    assert bad_supports
    result = dict(status='PASS', parameter_controls=len(parameters),
                  rotor_tables=dict(first_owners=[], second_owners=[], exact_roles_per_table=16),
                  source_role_controls=dict(counts), ordered_height_cases=order_cases,
                  shared_pool_cases=pool_cases,
                  partial_staircase=dict(positive_dimensions=[6, 14, 4],
                      outer_heights=[10, 4], intermediate_heights=[8, 6],
                      incoming_widths_left_to_right=[12, 10, 8, 6],
                      left_and_inner_phase11_chains_full=True,
                      disjoint_original_endpoints=len(endpoints),
                      complete_feasible=False, remaining_infeasible_supports=bad_supports,
                      scope='Partial source geometry attains h-k=6 and positive gap10; its retained supports are infeasible. Not a complete allocation example or counterexample.'),
                  new_complete_physical_fixture_coverage=0,
                  scope='Exact rotor role tables, representative U dimension/isometry controls, finite height/pool arithmetic and an explicitly incomplete partial staircase. General source-role and support proofs are written; arbitrary mixed allocation remains open.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', controls=dict(counts), height_cases=order_cases,
                          pool_cases=pool_cases, partial_bad_supports=len(bad_supports))))


if __name__ == '__main__':
    main()
