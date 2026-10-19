"""Discover frozen components outside the thin-or-one-square covered class."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_two_row_terminal_shapes import connected, matchings, support_sets


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--columns', type=int, default=3)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    vertices = list(itertools.product(range(3), range(arguments.columns)))
    shapes = supports = cases = frozen = phase_checks = 0
    maximum_charge_twice = None
    examples = []
    for mask in range(1 << len(vertices)):
        endpoints = {vertex for index, vertex in enumerate(vertices) if mask >> index & 1}
        if not endpoints or len(endpoints) % 2:
            continue
        if any(min(vertex[coordinate] for vertex in endpoints) != 0 for coordinate in (0, 1)):
            continue
        if max(row for row, _ in endpoints) != 2 or max(column for _, column in endpoints) < 2:
            continue
        if not connected(endpoints):
            continue
        squares = {vertex for vertex in endpoints if
                   {(vertex[0]+first, vertex[1]+second)
                    for first, second in itertools.product((0, 1), repeat=2)} <= endpoints}
        if len(squares) <= 1:
            continue
        actual_matchings = list(matchings(endpoints))
        if not actual_matchings:
            continue
        shapes += 1
        for selected in support_sets(endpoints):
            supports += 1
            for matching in actual_matchings:
                move = lambda vertex: (vertex[0]+2, vertex[1]+2)
                current = 8, 2*((arguments.columns+6)//2), {move(vertex) for vertex in selected}, [
                    tuple(move(vertex) for vertex in edge) for edge in matching]
                direct_check(*current)
                cases += 1
                if frozen_certificate(current)[0] != endpoint_data(current)[0]:
                    continue
                frozen += 1
                for vertical, horizontal in itertools.product((0, 1), repeat=2):
                    shifted = lambda vertex: (vertex[0]+vertical, vertex[1]+horizontal)
                    image = current[0]+2, current[1]+2, {shifted(vertex) for vertex in current[2]}, [
                        tuple(shifted(vertex) for vertex in edge) for edge in current[3]]
                    checked = verify_terminal(image)
                    assert len(checked['receivers']) == 1
                    charge = checked['receivers'][0]['charge_twice']
                    if maximum_charge_twice is None or charge > maximum_charge_twice:
                        maximum_charge_twice = charge
                        examples = [dict(shape=image[:2], selected=sorted(image[2]), matching=image[3],
                                         endpoint_squares=len(squares), receiver=checked['receivers'][0])]
                    phase_checks += 1
    report = dict(status='ENUMERATION_COMPLETED', endpoint_box=[3, arguments.columns],
                  connected_matched_uncovered_shapes=shapes, terminal_support_patterns=supports,
                  single_terminal_configurations=cases, bundle_terminal_configurations=frozen,
                  phase_checks=phase_checks, maximum_receiver_charge_twice=maximum_charge_twice,
                  maximum_examples=examples,
                  scope='Finite discovery outside the proved thin-or-one-square class. No general geometric theorem or universal coefficient-one conclusion follows from this search.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
