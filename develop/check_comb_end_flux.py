"""Controls for two-tiling flux and complete-comb end-contact cancellation."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_comb_end_debt import KINDS, contact_family, mouth_record, sparse_owners
from check_component_receivers import verify_terminal
from check_long_bent_terminal_strips import terminal_strip
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed
from check_saturated_bent_bands import long_bent
from check_transverse_comb_mouths import optimize_strip


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def flux_record(current, strip):
    if len({row for row, column in strip}) != 2:
        assert len({column for row, column in strip}) == 2
        shape, selected, matching = transformed(*current, True, False, False)
        _, moved_strip, _ = transformed(*current[:2], strip, [], True, False, False)
        return flux_record((*shape, selected, matching), moved_strip)
    physical = mouth_record(current, strip)
    endpoints = endpoint_data(current)[0]
    rows = sorted({row for row, column in strip})
    columns = sorted({column for row, column in strip})
    shifted_sparse = shifted_saturated = shifted_full = shifted_deficit = 0
    for column in columns[1:-1:2]:
        square = {(row, current_column) for row in rows
                  for current_column in (column, column+1)}
        selected_count, endpoint_count = len(square & current[2]), len(square & endpoints)
        if endpoint_count:
            assert (endpoint_count, selected_count) in ((2, 1), (1, 1), (1, 2))
            shifted_full += endpoint_count == 2
            shifted_sparse += (endpoint_count, selected_count) == (1, 1)
            shifted_saturated += (endpoint_count, selected_count) == (1, 2)
        else:
            assert selected_count <= 2
            shifted_deficit += 2-selected_count
    assert shifted_full == physical['full_columns']
    assert shifted_sparse == physical['saturated_ends']
    assert shifted_saturated == physical['sparse_ends']
    assert physical['shifted_slack'] == physical['saturated_ends']+shifted_deficit
    assert physical['no_endpoint_deficit'] == (
        2-physical['sparse_ends']+physical['saturated_ends']+shifted_deficit)
    return dict(**physical, shifted_no_endpoint_deficit=shifted_deficit)


def bridge_family(count, phases, extension):
    first, _ = long_bent(4*count+10, 2, saturate=False)
    _, other_selected, other_matching = transformed(*first, False, True, True)
    move = lambda vertex: (vertex[0]+12+extension, vertex[1]-2)
    selected = first[2] | {move(point) for point in other_selected}
    matching = first[3]+[tuple(move(point) for point in edge) for edge in other_matching]
    for index, phase in enumerate(phases):
        center = 8+4*index
        selected |= {(8, center), (15+extension, center)}
        selected |= {(row, center+phase*(1 if row % 2 else -1))
                     for row in range(9, 15+extension)}
        matching += [((row, center), (row+1, center))
                     for row in range(9, 15+extension, 2)]
    current = 32+extension, first[1], selected, matching
    first_strip = terminal_strip(4*count+10, 2)
    _, other_strip, _ = transformed(*first[:2], first_strip, [], False, True, True)
    strips = first_strip, {move(point) for point in other_strip}
    for strip in strips:
        current = optimize_strip(current, strip)
    checked = verify_terminal(current)
    assert frozen_certificate(current)[0] == endpoint_data(current)[0]
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*count+[2, 2]
    assert not strips[0] & strips[1]
    mouths = [flux_record(current, strip) for strip in strips]
    assert sum(mouth['sparse_ends'] for mouth in mouths) == count
    assert sum(mouth['saturated_ends'] for mouth in mouths) == count
    claimed = {tuple(tile) for mouth in mouths for tile in mouth['sparse_tiles']}
    assert sparse_owners(current, claimed) == count
    payment = sum(mouth['no_endpoint_deficit'] for mouth in mouths)
    shifted = sum(mouth['shifted_no_endpoint_deficit'] for mouth in mouths)
    assert payment == 4+shifted
    assert payment-2 >= 2
    return current, strips, dict(sources=2, internal_contacts=count, outward_contacts=0,
        inward_contacts=0, phases=phases, extension=extension, mouths=mouths,
        physical_payment=payment, shifted_deficit=shifted,
        source_minus_payment=2-payment, old_sparse_count_criterion_holds=count <= 2)


def controls():
    types = tuple(KINDS)
    histogram = Counter()
    family_cases = symmetry_images = 0
    for count in range(1, 7):
        kinds = list(itertools.product(types, repeat=count)) if count <= 2 else [
            tuple(kind for index in range(count)) for kind in types]+[
            tuple(types[(index+offset) % len(types)] for index in range(count))
            for offset in range(len(types))]
        phases = list(itertools.product((-1, 1), repeat=count)) if count <= 2 else [
            tuple(1 for index in range(count)), tuple(-1 for index in range(count)),
            tuple((-1)**index for index in range(count)), tuple(-(-1)**index for index in range(count))]
        for depth, kinds_record, sides in itertools.product((3, 6), kinds, phases):
            contacts = [(5+4*index, side, kind)
                        for index, (side, kind) in enumerate(zip(sides, kinds_record))]
            current, strip = contact_family(4*count+10, depth, contacts)
            optimized = optimize_strip(current, strip)
            checked = verify_terminal(optimized)
            assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*count+[2]
            assert frozen_certificate(optimized)[0] == endpoint_data(optimized)[0]
            record = flux_record(optimized, strip)
            histogram[(record['sparse_ends'], record['saturated_ends'],
                       record['shifted_no_endpoint_deficit'])] += 1
            family_cases += 1
    bridges, witness = [], None
    for count in range(1, 9):
        patterns = list(itertools.product((-1, 1), repeat=count)) if count <= 4 else [
            tuple(1 for index in range(count)), tuple(-1 for index in range(count)),
            tuple((-1)**index for index in range(count)), tuple(-(-1)**index for index in range(count))]
        for extension, phases in itertools.product((0, 4, 10), patterns):
            current, strips, record = bridge_family(count, phases, extension)
            bridges.append(record)
            if count == 3 and extension == 0 and phases == patterns[0]:
                witness = dict(shape=current[:2], selected=sorted(current[2]),
                               matching=current[3], strips=[sorted(strip) for strip in strips], **record)
            if count in (1, 4, 8) and extension == 4 and phases == patterns[0]:
                for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
                    shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
                    image = (*shape, selected, matching)
                    moved = [transformed(*current[:2], strip, [], transpose, vertical, horizontal)[1]
                             for strip in strips]
                    records = [flux_record(image, strip) for strip in moved]
                    assert sum(item['no_endpoint_deficit'] for item in records) == record['physical_payment']
                    symmetry_images += 1
    assert witness is not None and not witness['old_sparse_count_criterion_holds']
    current, strips, _ = bridge_family(3, (-1, -1, -1), 0)
    transposed_shape, other_selected, other_matching = transformed(*current, True, False, False)
    move = lambda vertex: (vertex[0], vertex[1]+current[1]+4)
    selected = current[2] | {move(point) for point in other_selected}
    matching = current[3]+[tuple(move(point) for point in edge) for edge in other_matching]
    mixed = max(current[0], transposed_shape[0]), current[1]+4+transposed_shape[1], selected, matching
    other_strips = [{move(point) for point in transformed(*current[:2], strip, [], True, False, False)[1]}
                    for strip in strips]
    mixed_mouths = [flux_record(mixed, strip) for strip in (*strips, *other_strips)]
    mixed_checked = verify_terminal(mixed)
    assert frozen_certificate(mixed)[0] == endpoint_data(mixed)[0]
    assert sorted(receiver['charge_twice'] for receiver in mixed_checked['receivers']) == [0]*6+[2]*4
    assert sum(mouth['sparse_ends'] for mouth in mixed_mouths) == 6
    assert sum(mouth['saturated_ends'] for mouth in mixed_mouths) == 6
    mixed_payment = sum(mouth['no_endpoint_deficit'] for mouth in mixed_mouths)
    assert mixed_payment == 12
    mixed_record = dict(sources=4, internal_contacts=6, sparse_ends=6, saturated_ends=6,
                        physical_payment=mixed_payment, source_minus_payment=4-mixed_payment,
                        mouths=mixed_mouths, old_sparse_count_criterion_holds=False)
    return dict(status='ALL_CHECKS_PASSED', optimized_contact_cases=family_cases,
        optimized_bridge_cases=len(bridges), bridge_symmetry_images=symmetry_images,
        flux_histogram=[dict(sparse=sparse, saturated=saturated, shifted_deficit=shifted,
            cases=number) for (sparse, saturated, shifted), number in sorted(histogram.items())],
        bridge_family=bridges, beyond_previous_criterion_witness=witness,
        mixed_orientation_closed_network=mixed_record,
        scope='Finite controls of a general written type-swap, exact two-tiling identity and '
              'closed end-contact network theorem. Shifted deficits are auxiliary counts, '
              'not additional physical donors. No automatic unmatched exterior compensation '
              'or universal grid theorem is inferred.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('flux_histogram', 'bridge_family', 'beyond_previous_criterion_witness',
                                     'mixed_orientation_closed_network')}))


if __name__ == '__main__':
    main()
