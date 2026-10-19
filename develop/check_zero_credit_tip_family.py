"""Independent checks of the three-module zero-credit tip family."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_minus_one_joint_compensation import contained, inspect
from check_minus_one_tip_obstructions import source
from check_promotion_cores import frozen_certificate
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def family(vertical_width=6, horizontal_width=6, long_height=10,
           short_height=4, horizontal_long=12, horizontal_short=4):
    parameters = (vertical_width, horizontal_width, long_height,
                  short_height, horizontal_long, horizontal_short)
    assert all(value % 2 == 0 for value in parameters)
    assert min(vertical_width, horizontal_width) >= 6
    assert min(short_height, horizontal_short) >= 4
    assert long_height >= max(short_height+4, horizontal_width+4)
    assert horizontal_long >= vertical_width+horizontal_short+2
    vertical = source(vertical_width, long_height, short_height)
    horizontal = source(horizontal_width, horizontal_long, horizontal_short)
    return [transform_module(vertical, (False, False, False), (-long_height, -1)),
            transform_module(horizontal, (True, True, False), (-1, horizontal_long+1)),
            transform_module(horizontal, (True, True, True), (0, horizontal_long+1))]


def verify_uniform_schedule(current, parameters):
    vertical_width, horizontal_width, long_height, short_height, horizontal_long, horizontal_short = parameters
    mates = {endpoint: partner for edge in current[3]
             for endpoint, partner in (edge, edge[::-1])}
    frozen = set()

    def force(point):
        assert point in mates and point not in frozen
        kept = current[2] | {mates[endpoint] for endpoint in frozen}
        witnesses = set(neighbors(point)) & kept
        assert len(witnesses) >= 2, (parameters, point, witnesses)
        frozen.add(point)

    def first_wave(width, long_leg, short_leg):
        return ([(row, width) for row in range(short_leg, 1, -2)] +
                [(0, width)] +
                [((width-column) % 2, column) for column in range(width-1, 0, -1)] +
                [(row, 1) for row in range(3, long_leg, 2)])

    def return_wave(width, long_leg, short_leg):
        return ([(row, 1) for row in range(long_leg-2, 1, -2)] + [(0, 1)] +
                [(1 if column % 2 == 0 else 0, column) for column in range(2, width)] +
                [(row, width) for row in range(1, short_leg, 2)])

    def vertical(point):
        row, column = point
        return row, column+1

    def horizontal(point, lower):
        row, column = point
        return (long_height-column if lower else long_height+column-1,
                horizontal_long+3-row)

    for lower in (False, True):
        for point in first_wave(horizontal_width, horizontal_long, horizontal_short):
            force(horizontal(point, lower))
    vertical_wave = ([(row, 1) for row in range(long_height, 1, -2)] +
                     [(row, vertical_width) for row in range(short_height, 1, -2)] +
                     [(0, 1)] +
                     [(1 if column % 2 == 0 else 0, column) for column in range(2, vertical_width)] +
                     [(0, vertical_width)] +
                     [((vertical_width-column) % 2, column) for column in range(vertical_width-1, 1, -1)] +
                     [(row, 1) for row in range(1, long_height-1, 2)] +
                     [(row, vertical_width) for row in range(1, short_height, 2)])
    for point in vertical_wave:
        force(vertical(point))
    force((long_height-1, 2))
    force((long_height-1, 3))
    force((long_height, 3))
    for lower in (True, False):
        for point in return_wave(horizontal_width, horizontal_long, horizontal_short):
            force(horizontal(point, lower))
    assert frozen == set(mates)
    return len(frozen)


def check(parameters):
    vertical_width, horizontal_width, long_height, short_height, horizontal_long, horizontal_short = parameters
    current, modules = contained(family(*parameters))
    network = combine(modules)
    report = inspect(current, modules)
    assert [module['charge'] for module in modules] == [-1, -1, -1]
    assert (report['positive'], report['minus_one'], report['negative_rotors'],
            report['marked_sides']) == (0, 3, 0, 0)
    assert (report['regular_events'], report['irregular_events'],
            report['square_credit'], report['finer_slack']) == (0, 1, 0, 2)
    expected_matching = (vertical_width+2*horizontal_width+
                         (long_height+short_height)//2+horizontal_long+horizontal_short-3)
    expected_selected = long_height+short_height+horizontal_long+2*horizontal_short+1
    assert len(current[3]) == expected_matching and len(current[2]) == expected_selected
    assert len(network['endpoints']) == 2*expected_matching and network['charge'] == -2
    degree_four = sum(value == 4 for value in occupied_degrees(current).values())
    assert degree_four == horizontal_long+1
    assert current[:2] == (long_height+horizontal_width+2, horizontal_long+4)
    endpoint_owners = {point: owner for owner, module in enumerate(modules)
                       for point in module['endpoints']}
    mixed = []
    for tile in sorted(network['receiver']):
        cells = vertices_of({tile})
        represented = {endpoint_owners[point] for point in cells & network['endpoints']}
        if len(represented) > 1:
            assert not cells <= network['endpoints']
            mixed.append(dict(tile=tile, endpoints=sorted(cells & network['endpoints']),
                              selected=sorted(cells & network['selected'])))
    assert len(mixed) == 2
    tip = long_height, 2
    target = long_height, 3
    assert tip in modules[0]['endpoints'] and target in modules[1]['endpoints']
    assert target not in modules[0]['selected'] and target in neighbors(tip)
    assert tip[0]//2 == target[0]//2 and tip[1]//2 == target[1]//2
    assert not vertices_of({(tip[0]//2, 1)}) <= network['endpoints']
    frozen, layers = frozen_certificate(current)
    assert frozen == network['endpoints']
    assert verify_uniform_schedule(current, parameters) == len(frozen)
    assert len(endpoint_components(current)) == 1
    return dict(parameters=parameters, shape=current[:2], endpoints=len(network['endpoints']),
                matching=len(current[3]), selected=len(current[2]),
                final_receiver_charge=network['charge'], receiver_tiles=len(network['receiver']),
                receiver_selections=len(network['receiver_selected']),
                mixed_tiles=mixed, frozen_endpoints=len(frozen), frozen_layers=len(layers),
                degree_four_endpoints=degree_four,
                tip=tip, target=target, **report)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    for vertical_width, horizontal_width, short_height, horizontal_short, extra_vertical, extra_horizontal in itertools.product(
            (6, 8, 14), (6, 8, 12), (4, 6), (4, 8), (0, 4), (0, 4)):
        long_height = max(short_height+4, horizontal_width+4)+extra_vertical
        horizontal_long = vertical_width+horizontal_short+2+extra_horizontal
        checked = check((vertical_width, horizontal_width, long_height,
                         short_height, horizontal_long, horizontal_short))
        records.append({key: checked[key] for key in
                        ('parameters', 'shape', 'endpoints', 'matching', 'selected',
                         'frozen_endpoints', 'irregular_events', 'square_credit', 'finer_slack')})
    reference = check((6, 6, 10, 4, 12, 4))
    assert (reference['endpoints'], reference['matching'], reference['selected'],
            reference['actual_slack'], reference['frozen_endpoints']) == (76, 38, 35, 71, 76)
    images = []
    current, modules = contained(family())
    for symmetry in itertools.product((False, True), repeat=3):
        transpose, flip_row, flip_column = symmetry
        phase = ((int(flip_column), int(flip_row)) if transpose else
                 (int(flip_row), int(flip_column)))
        moved = [transform_module(module, symmetry, phase) for module in modules]
        image, moved = contained(moved)
        report = inspect(image, moved)
        assert (report['irregular_events'], report['regular_events'],
                report['square_credit'], report['finer_slack']) == (1, 0, 0, 2)
        assert frozen_certificate(image)[0] == combine(moved)['endpoints']
        images.append(dict(symmetry=symmetry, status='PASS'))
    repeated = []
    for amount in (1, 2, 3, 4, 8, 16):
        copies = [transform_module(module, (False, False, False), (0, 16*index))
                  for index in range(amount) for module in modules]
        repeated_network = combine(copies)
        repeated_current = (18, 16*amount, repeated_network['selected'], repeated_network['matching'])
        report = inspect(repeated_current, copies)
        assert (report['irregular_events'], report['regular_events'], report['square_credit'],
                report['finer_slack'], report['actual_slack']) == (amount, 0, 0, 2*amount, 71*amount)
        assert frozen_certificate(repeated_current)[0] == repeated_network['endpoints']
        repeated.append(dict(copies=amount, irregular=amount, credit=0, finer_slack=2*amount,
                             actual_slack=71*amount, frozen_endpoints=76*amount))
    result = dict(status='PASS', reference=reference, family_controls=records,
                  symmetry_images=images, separated_copy_controls=repeated,
                  scope='Controls for the written all-parameter three-U family. Every control is fully frozen. The reference refutes K_minus_one<=C even for fully frozen fusions: K_minus_one1,C0,J0, finer slack2 and actual slack71. Finite controls do not replace the general proof; Oracle suggested the reference construction, which is independently rebuilt here.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', family_controls=len(records), symmetry_images=len(images),
                          separated_copy_controls=len(repeated), reference_counts=[76, 38, 35],
                          fully_frozen=True)))


if __name__ == '__main__':
    main()
