"""Physical controls for the charge-minus-one joint witness budget."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_regular_tile_compensation import inspect as inspect_regular
from check_two_leg_corner_obstruction import two_leg_case
from degree_three_fusion import four_way
from dual_guard_compensation import paired_guards
from rotor_networks import chain, combine, labeled_module, rotor, transform_module, two_leg_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def tile_of(point):
    return tuple(coordinate//2 for coordinate in point)


def normalized_core(symmetry):
    transpose, flip_row, flip_column = symmetry
    core = {(1, column) for column in range(1, 5)} | {
        (row, 1) for row in range(2, 5)}
    result = set()
    for row, column in core:
        row, column = row-2, column-2
        row = 1-row if flip_row else row
        column = 1-column if flip_column else column
        result.add((column, row) if transpose else (row, column))
    return result


def packing_controls():
    cores = [normalized_core(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    ring = set(itertools.product(range(-1, 3), repeat=2))-set(itertools.product(range(2), repeat=2))
    assert len(ring) == 12 and all(len(core) == 7 and core <= ring for core in cores)
    witnesses = []
    for first, second in itertools.product(range(8), repeat=2):
        common = cores[first] & cores[second]
        assert len(common) >= 2
        witnesses.append(dict(first=first, second=second, common_endpoint=min(common)))
    return witnesses


def minus_one_boundary(module):
    assert module['charge'] == -1
    endpoints = module['endpoints']
    occupied = endpoints | module['selected']
    corners = set()
    tips = {point for point in endpoints if len(set(neighbors(point)) & endpoints) == 1}
    failures = set()
    for point in endpoints:
        cells = vertices_of({tile_of(point)})
        if not (set(neighbors(point))-cells) & endpoints:
            corners.add(point)
        for blank in (set(neighbors(point)) & cells)-occupied:
            other = next(iter((set(neighbors(point)) & cells)-{blank}))
            continuation = tuple(2*value-original for value, original in zip(point, other))
            assert continuation in endpoints
            if other not in endpoints or continuation not in endpoints:
                failures.add(point)
    assert len(corners) == len(tips) == 2 and not corners & tips
    assert failures == tips
    for point in corners:
        assert vertices_of({tile_of(point)}) <= endpoints
    for point in tips:
        cells = vertices_of({tile_of(point)})
        assert cells & endpoints == {point} and len(cells & module['selected']) == 1
    return corners, tips


def inspect(current, modules):
    result = inspect_regular(current, modules, require_frozen=False)
    endpoints = {point for module in modules for point in module['endpoints']}
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    degrees = occupied_degrees(current)
    corners = set()
    tips = set()
    minus_one = 0
    negative_rotors = 0
    for module in modules:
        if module['charge'] == -1:
            current_corners, current_tips = minus_one_boundary(module)
            corners |= current_corners
            tips |= current_tips
            minus_one += 1
        elif module['charge'] == -2:
            negative_rotors += 1
        else:
            assert module['charge'] in (0, 1)
    irregular_tips = set()
    for point in tips:
        module = modules[owners[point]]
        missing = set(neighbors(point))-(module['endpoints'] | module['selected'])
        assert len(missing) == 1
        other = next(iter(missing))
        assert tile_of(point) == tile_of(other)
        if other in endpoints:
            irregular_tips.add(point)
    donor_tiles = set()
    charged = set()
    records = []
    for module in modules:
        if module['charge'] != 1:
            continue
        for chosen, anchor, opposite, guard in paired_guards(module):
            tile = tile_of(chosen)
            assert tile not in donor_tiles
            donor_tiles.add(tile)
            protectors = (set(neighbors(anchor)) & module['endpoints']) | {guard}
            if not any(degrees[point] == 4 for point in protectors):
                continue
            inward = tuple(first-second for first, second in zip(chosen, anchor))
            gate = tuple(first-second for first, second in zip(opposite, inward))
            assert gate in endpoints and gate in corners
            witness = gate
            kind = 'bar_corner'
            assert vertices_of({tile}) <= modules[owners[witness]]['endpoints']
            assert tile_of(witness) == tile and witness not in charged
            charged.add(witness)
            records.append(dict(tile=tile, witness=witness, kind=kind))
    assert len(charged) == result['marked_sides']
    assert len(charged) <= 2*minus_one
    assert not charged & irregular_tips
    assert charged | irregular_tips <= corners | tips
    assert len(corners | tips) == 4*minus_one
    assert len(charged)+len(irregular_tips) <= 4*minus_one
    assert result['irregular_source_events']-len(irregular_tips) <= 4*negative_rotors
    assert result['irregular_source_events']+len(charged) <= 4*minus_one+4*negative_rotors
    credit = result['positive_modules']-3*minus_one-2*negative_rotors+result['residual_square_credit']
    assert credit <= result['two_guard_credit'] <= result['half_area']-result['objective']
    return dict(positive=result['positive_modules'], minus_one=minus_one,
                negative_rotors=negative_rotors, marked_sides=len(charged),
                irregular_tip_events=len(irregular_tips),
                irregular_events=result['irregular_source_events'],
                regular_events=result['regular_source_events'],
                square_credit=result['residual_square_credit'],
                joint_tax_bound=4*minus_one+4*negative_rotors,
                guaranteed_slack=credit, finer_slack=result['two_guard_credit'],
                actual_slack=result['half_area']-result['objective'],
                original_donor_tiles=len(donor_tiles), marked_assignments=records)


def contained(modules):
    occupied = {point for module in modules for point in module['endpoints'] | module['selected']}
    offset = tuple(-2*(min(point[axis] for point in occupied)//2) for axis in (0, 1))
    modules = [transform_module(module, (False, False, False), offset) for module in modules]
    network = combine(modules)
    occupied = network['endpoints'] | network['selected']
    shape = tuple(2*(max(point[axis] for point in occupied)//2+1) for axis in (0, 1))
    return (*shape, network['selected'], network['matching']), modules


def marked_gate_modules():
    modules = [transform_module(two_leg_module(14, 4), (False, False, False), (6, 6))]
    for flip_row, offset in [(False, (8, 7)), (False, (8, 13)),
                             (True, (15, 1)), (True, (15, 19)),
                             (True, (17, 7)), (True, (17, 13))]:
        modules.append(transform_module(two_leg_module(6, 4), (False, flip_row, False), offset))
    return modules


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    boundary = []
    specs = list(itertools.product((6, 8, 14), (4, 6, 12), (4, 8, 20)))+[(40, 4, 100)]
    for width, left, right in specs:
        current, _ = two_leg_case(width, left, right)
        base = labeled_module(current[2], current[3], (), ((3, 2), (3, 1), (2, 3), (1, 3)))
        base = transform_module(base, (False, False, False), (0, 1))
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = (int(flip_column), int(flip_row)) if transpose else (int(flip_row), int(flip_column))
            module = transform_module(base, symmetry, offset)
            corners, tips = minus_one_boundary(module)
            boundary.append(dict(parameters=[width, left, right], symmetry=symmetry,
                                 bar_corners=sorted(corners), tips=sorted(tips)))
    records = []
    base = two_leg_module(6, 4)
    for amount in (1, 2, 3, 4, 8, 16, 32):
        modules = [transform_module(base, (False, bool(index % 2), False),
                                    (9 if index % 2 else 0, 5*index)) for index in range(amount)]
        current, modules = contained(modules)
        records.append(dict(kind='mixed_zigzag', amount=amount, **inspect(current, modules)))
    for amount in (1, 2, 3, 4, 8):
        current, modules = chain(amount)
        records.append(dict(kind='rotor_star_chain', amount=amount, **inspect(current, modules)))
    for amount in (1, 2, 4, 8, 32):
        modules = [transform_module(rotor(), (False, False, False), (2*index, 2*index+1))
                   for index in range(amount)]
        current, modules = contained(modules)
        records.append(dict(kind='degree_four_zero_rotor_chain', amount=amount,
                            **inspect(current, modules)))
    for width in (8, 14, 40):
        current, modules = four_way(width)
        records.append(dict(kind='nonhereditary_four_way', width=width, **inspect(current, modules)))
    current, modules = contained(marked_gate_modules())
    marked = inspect(current, modules)
    assert current[:2] == (12, 28)
    assert (marked['positive'], marked['minus_one'], marked['marked_sides']) == (1, 6, 2)
    assert marked['finer_slack'] == 5 and marked['actual_slack'] == 69
    records.append(dict(kind='actual_two_donor_gate_intrusion', **marked))
    arguments.output.write_text(json.dumps(dict(status='PASS', core_overlap=packing_controls(),
        negative_boundary_images=boundary, physical=records,
        summary=dict(core_pairs=64, boundary_images=len(boundary), physical_fusions=len(records),
                     marked_controls=sum(record['marked_sides'] > 0 for record in records),
                     irregular_tip_controls=sum(record['irregular_tip_events'] > 0 for record in records)),
        scope='Controls for a general written corner/tip injection proof. An explicit feasible seven-module example loses both positive donors but satisfies the finer target budget. No universal residual payment or sharpness of coefficient three is inferred.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS', boundary_images=len(boundary), physical_fusions=len(records),
                          marked_controls=sum(record['marked_sides'] > 0 for record in records))))


if __name__ == '__main__':
    main()
