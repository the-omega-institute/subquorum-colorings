"""Finite gate controls and conditional arithmetic, without a geometric theorem claim."""

from collections import Counter
import itertools
import json

from check_low_cost_exceptional_doubles import compensated
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import gate_roles
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def role_controls(parameters, candidates):
    width, left, right = parameters
    producer = source(*parameters)
    forbidden = {(left+1, 2), (right+1, width-1)}
    libraries = []
    for reflected in (False, True):
        library = {}
        for candidate in candidates:
            incoming = (transform_module(candidate['module'], (False, False, True), (0, width+1))
                        if reflected else candidate['module'])
            if producer['endpoints'] & incoming['endpoints']:
                continue
            if forbidden & (incoming['endpoints'] | incoming['selected']):
                continue
            library[frozenset(incoming['endpoints'])] = candidate, incoming
        libraries.append(list(library.values()))
    outcomes = Counter()
    for first, first_owner in libraries[0]:
        for second, second_owner in libraries[1]:
            if first_owner['endpoints'] == second_owner['endpoints']:
                assert parameters == (8, 6, 8)
                expected = {(6-row, column+1) for row, column in source(6, 4, 4)['endpoints']}
                assert first_owner['endpoints'] == expected
                tile = {(row, column) for row in (6, 7) for column in (2, 3)}
                assert tile & first_owner['endpoints'] == {(6, 2), (6, 3)}
                assert not tile & first_owner['selected']
                assert not tile & (producer['endpoints'] | producer['selected'])
                assert (7, 2) in forbidden
                outcomes['common_inverted_owner'] += 1
            elif first_owner['endpoints'] & second_owner['endpoints']:
                outcomes['distinct_owner_collision'] += 1
            else:
                assert parameters == (8, 4, 10)
                assert first['phase'] == second['phase'] == '11'
                assert first['role'] == second['role'] == 'F'
                assert first['height'] == 4 and first['parameters'][0] == 6
                assert first['predecessor'] == (0, 1)
                assert second['height'] == 8 and second['predecessor'] == (1, 0)
                assert second_owner['charge'] < 0
                outcomes['long_negative_terminal_height_eight'] += 1
    return dict(parameters=parameters, left_roles=len(libraries[0]),
                right_roles=len(libraries[1]), outcomes=dict(outcomes),
                complete_physical_realization_claimed=False)


def dimension_controls():
    checked = 0
    new_shapes = set()
    for width, left, right in itertools.product(range(6, 32, 2),
                                               range(4, 32, 2), range(4, 32, 2)):
        matching = width+(left+right)//2-1
        if not compensated(width, left, right) and matching <= 14:
            assert matching == 14 and width == 8 and (left, right) in {
                (6, 8), (8, 6), (4, 10), (10, 4)}
            new_shapes.add((width, left, right))
        for left_long, right_long in itertools.product((0, 1), repeat=2):
            if left_long and left < 8 or right_long and right < 8:
                continue
            assert matching >= 9+2*(left_long+right_long)
        checked += 1
    assert len(new_shapes) == 4
    return dict(dimensions=checked, remaining_cost_fourteen_shapes=sorted(new_shapes))


def conditional_arithmetic_controls():
    checked = negative = 0
    for zero, single, twice, middle, remaining in itertools.product(range(4), repeat=5):
        for credit in range(middle+1):
            for unmarked, one_mark in itertools.product(range(3), repeat=2):
                positive = unmarked+one_mark+zero+single+twice+middle+remaining
                marked = one_mark+2*(zero+single+twice+middle+remaining)
                reserve_minimum = (2*zero+single+2*twice+middle-credit+1)//2
                for reserve in range(reserve_minimum, reserve_minimum+3):
                    margin = positive+reserve-marked
                    assert 2*(-margin) <= 2*remaining+single+middle+credit
                    budget = 36*positive+20*middle+24*remaining+9*marked+8*credit
                    matching = (budget+3)//4
                    assert 39*margin+2*matching >= 0
                    checked += 1
                    negative += margin < 0
    assert negative > 0
    return dict(conditional_budgets=checked, negative_margin_budgets=negative,
                geometric_hypotheses_assumed=True)


def main():
    dimensions, candidates = gate_roles()
    print(json.dumps(dict(status='PASS_CONDITIONAL_REDUCTION_ONLY',
                          incoming_dimensions=len(dimensions), anchored_roles=len(candidates),
                          roles=[role_controls(parameters, candidates)
                                 for parameters in ((8, 6, 8), (8, 4, 10))],
                          sizes=dimension_controls(), arithmetic=conditional_arithmetic_controls(),
                          scope='Finite role masks do not prove arbitrary-dimension geometry or shared-pool injections. The 37/39 bound remains conditional.'), indent=2))


if __name__ == '__main__':
    main()
