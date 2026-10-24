"""Check the unchanged-endpoint source bridge obstruction and search controls."""

import argparse
import itertools
import json
from pathlib import Path

from check_elbow_sources import elbow
from check_orthogonal_source_mouths import feasible
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_two_leg_corner_obstruction import two_leg_case
from rotor_networks import affine, rotor


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SYMMETRIES = tuple(itertools.product((False, True), repeat=3))


def source_templates(maximum):
    templates = [('rotor', rotor()['endpoints'])]
    for width in range(6, maximum+1, 2):
        current, _ = two_leg_case(width, 4, 4)
        templates.append((f'U({width},4,4)', endpoint_data(current)[0]))
    return [(name, {affine(point, symmetry) for point in endpoints})
            for name, endpoints in templates for symmetry in SYMMETRIES]


def contained_source(endpoints, templates):
    for name, source in templates:
        source_anchor = min(source)
        for target_anchor in sorted(endpoints):
            offset = tuple(target-source for target, source in zip(target_anchor, source_anchor))
            if all((row+offset[0], column+offset[1]) in endpoints for row, column in source):
                return name, offset
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--maximum', type=int, default=20)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.maximum >= 6 and args.maximum % 2 == 0
    templates = source_templates(args.maximum)
    positive_controls = 0
    for name, source in templates:
        for phase in itertools.product((0, 1), repeat=2):
            shifted = {(row+13+phase[0], column+17+phase[1]) for row, column in source}
            assert contained_source(shifted, [(name, source)]) is not None
            positive_controls += 1
    bases = images = square_controls = 0
    for width in range(6, args.maximum+1, 2):
        for height in range(4, args.maximum+1, 2):
            current = elbow(width, height)
            assert feasible(current)
            endpoints = endpoint_data(current)[0]
            frozen, _ = frozen_certificate(current)
            assert frozen == endpoints
            relative = {(row-4, column-5) for row, column in endpoints}
            for row, column in relative:
                square = {(row+row_offset, column+column_offset)
                          for row_offset, column_offset in itertools.product((0, 1), repeat=2)}
                if square <= relative:
                    assert row == 0 or column == width-2
                    square_controls += 1
            for symmetry in SYMMETRIES:
                for phase in itertools.product((0, 1), repeat=2):
                    image = {affine(point, symmetry, phase) for point in relative}
                    assert contained_source(image, templates) is None
                    images += 1
            bases += 1
    result = dict(status='PASS', maximum=args.maximum, base_elbows=bases,
                  endpoint_images=images, full_square_controls=square_controls,
                  oriented_source_templates=len(templates), positive_search_controls=positive_controls,
                  contained_sources=0,
                  scope='Finite discovery and regression controls; the all-parameter theorem is written separately.',
                  reduction='Any permitted U(width,left,right) contains U(width,4,4) in its endpoint set; the source bar fits in a host bounding-box side.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
