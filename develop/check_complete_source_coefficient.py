"""Constructor-size and integer-budget controls for complete-source coefficients."""

import argparse
import itertools
import json
from pathlib import Path

from check_two_leg_corner_obstruction import two_leg_case


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    constructor_cases = 0
    exceptional_cases = 0
    minimum_size = None
    minimum_exceptional_size = None
    for width, left_height, right_height in itertools.product(range(6, 32, 2), range(4, 32, 2), range(4, 32, 2)):
        current, _ = two_leg_case(width, left_height, right_height)
        matching = current[3]
        endpoints = [point for edge in matching for point in edge]
        size = len(matching)
        assert len(set(endpoints)) == 2*size
        assert size == width+(left_height+right_height)//2-1
        assert size >= 9
        minimum_size = size if minimum_size is None else min(minimum_size, size)
        exceptional = width != 6 and (width >= 12 or max(left_height, right_height) >= 8)
        if exceptional:
            assert size >= 13
            minimum_exceptional_size = size if minimum_exceptional_size is None else min(minimum_exceptional_size, size)
            exceptional_cases += 1
        constructor_cases += 1
    universal_cases = 0
    nonexceptional_cases = 0
    for exceptional, single, unmarked in itertools.product(range(33), repeat=3):
        matching = 13*exceptional+9*single
        margin = unmarked-exceptional-single//2
        assert 13*(exceptional+single//2) <= matching
        assert 13*margin+matching >= 0
        universal_cases += 1
        if exceptional == 0:
            assert 18*margin+matching >= 0
            nonexceptional_cases += 1
    result = dict(status='PASS', constructor_cases=constructor_cases,
                  exceptional_constructor_cases=exceptional_cases,
                  minimum_matching_size=minimum_size,
                  minimum_exceptional_matching_size=minimum_exceptional_size,
                  universal_budget_cases=universal_cases,
                  nonexceptional_budget_cases=nonexceptional_cases,
                  scope='Finite constructor cardinality and arithmetic-budget controls, not new physical-fusion coverage or a substitute for the general written proof.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
