"""Finite endpoint-box search for exchange-terminal nonunique matchings."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_promotion_cores import frozen_certificate
from check_rematching_receiver_flux import perfect_matchings


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def search(rows, columns):
    points = list(itertools.product(range(1, rows+1), range(1, columns+1)))
    counts = Counter()
    for mask in range(1 << len(points)):
        if mask.bit_count() < 4 or mask.bit_count() % 2:
            continue
        endpoints = {point for index, point in enumerate(points) if mask >> index & 1}
        if 2*sum(sum(point) % 2 == 0 for point in endpoints) != len(endpoints):
            continue
        supports = sorted({near for point in endpoints for near in neighbors(point)
                           if near not in endpoints
                           and len(set(neighbors(near)) & endpoints) == 1})
        if any(len(set(neighbors(point)) & (endpoints | set(supports))) < 3
               for point in endpoints):
            continue
        counts['potential_endpoint_masks'] += 1
        matchings = list(perfect_matchings(endpoints))
        if len(matchings) < 2:
            continue
        counts['nonunique_endpoint_masks'] += 1
        support_indices = {point: index for index, point in enumerate(supports)}
        conflict = [sum(1 << support_indices[near] for near in neighbors(point)
                        if near in support_indices) for point in supports]
        terminal = [(3-len(set(neighbors(point)) & endpoints),
                     sum(1 << support_indices[near] for near in neighbors(point)
                         if near in support_indices)) for point in endpoints]
        for selection_mask in range(1 << len(supports)):
            if any(selection_mask >> index & 1 and selection_mask & adjacent
                   for index, adjacent in enumerate(conflict)):
                continue
            if any((selection_mask & available).bit_count() < needed
                   for needed, available in terminal):
                continue
            counts['single_terminal_support_models'] += 1
            selected = {point for index, point in enumerate(supports)
                        if selection_mask >> index & 1}
            all_frozen = True
            for matching in matchings:
                current = rows+2, columns+2, selected, list(matching)
                frozen, _ = frozen_certificate(current)
                counts['tested_matchings'] += 1
                if frozen != endpoints:
                    all_frozen = False
                    break
                counts['fully_frozen_matchings'] += 1
            if all_frozen:
                return dict(status='FOUND', shape=[rows+2, columns+2],
                            endpoint_box=[rows, columns], selected=sorted(selected),
                            matching=matchings[0], total_matchings=len(matchings),
                            counts=dict(counts))
    return dict(status='NO_COUNTEREXAMPLE_IN_DOMAIN', endpoint_box=[rows, columns],
                counts=dict(counts),
                scope='All endpoint subsets of the specified interior box and all feasible '
                      'endpoint-adjacent selections in a one-site blank padding, with occupied '
                      'endpoint degree at least3 and nonunique induced perfect matching. '
                      'Selections with no endpoint neighbor are irrelevant to bundles and are '
                      'omitted. Finite search only, not a general uniqueness theorem.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=4)
    parser.add_argument('--columns', type=int, default=4)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = search(arguments.rows, arguments.columns)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
