"""Phase01 critical return roles, exact physical packing and a sharp family."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_closed_neutral_receivers import closed_contacts
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_critical_closed_owner_counterexample import modules as six_sources
from check_exact_event_reserve import inspect_exact
from check_full_neutral_receivers import add, scale
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from check_passive_corner_transfers import inspect_transfers
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


LEFT_SUPPORT = {
    (0, 1), (2, 1), (3, 6), (4, 1), (4, 7), (5, 10),
    (6, 1), (6, 7), (8, 1), (8, 7), (9, 8), (10, 1),
    (10, 6), (11, 8), (12, 1), (13, 2), (13, 4), (16, 4),
    (17, 2), (18, 3), (18, 5), (18, 7),
}


def family(width):
    assert width >= 20 and width % 2 == 0
    specifications = [
        ((width, 12, 12), (False, False, False), (0, 1)),
        ((10, 4, 4), (True, False, False), (1, 3)),
        ((10, 4, 4), (True, True, False), (1, width)),
        ((6, 4, 4), (True, True, False), (11, 7)),
        ((6, 4, 4), (True, False, False), (11, width-4)),
        ((width-12, 6, 6), (False, False, False), (2, 7)),
        ((width-14, 4, 4), (False, True, False), (8, 8)),
    ]
    return [transform_module(source(*dimensions), symmetry, offset)
            for dimensions, symmetry, offset in specifications]


def row_table(width):
    records = [
        ((0, 1, 2), ((2, width+1),)),
        ((3, 7, 8), ((2, 4), (8, width-5), (width-1, width+1))),
        ((4, 5, 6), ((2, 4), (8, 9), (width-6, width-5), (width-1, width+1))),
        ((9, 10), ((2, 4), (width-1, width+1))),
        ((11, 12), ((2, 7), (width-4, width+1))),
        ((13, 14, 15, 16), ((6, 7), (width-4, width-3))),
        ((17,), ((3, 7), (width-4, width))),
    ]
    return {(row, column) for rows, intervals in records for row in rows
            for lower, upper in intervals for column in range(lower, upper+1)}


def bar_corners(module):
    result = set()
    for point in module['endpoints']:
        own = set(neighbors(point)) & module['endpoints']
        if len(own) == 2:
            first, second = own
            if sum((value-base)*(other-base)
                   for value, other, base in zip(first, second, point)) == 0:
                result.add(point)
    assert len(result) == 2
    return result


def owner_roles():
    counts = Counter()
    for dimensions in itertools.product((6, 8, 14, 30), (4, 6, 12), (4, 10)):
        base = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            for anchor in base['endpoints']:
                offset = tuple(-value for value in affine(anchor, symmetry))
                module = transform_module(base, symmetry, offset)
                if phase_of(module) != '01':
                    continue
                counts['phase01_anchored_images'] += 1
                if module['endpoints'] & {(-1, 0), (0, -1)}:
                    continue
                assert anchor in ((0, 1), (0, dimensions[0]))
                assert (0, 0) in bar_corners(module)
                assert vertices_of({(0, 0)}) <= module['endpoints']
                counts['two_foreign_blocker_survivors'] += 1
    return dict(counts)


def inspect(current, originals):
    rows, columns, selected, matching = current
    network = combine(originals)
    endpoints = network['endpoints']
    assert len(endpoints) == 2*len(matching) == sum(len(module['endpoints']) for module in originals)
    assert not selected & endpoints and selected == network['selected']
    assert all(0 <= row < rows and 0 <= column < columns for row, column in endpoints | selected)
    assert all(second in neighbors(first) for first, second in matching)
    assert all(len(set(neighbors(point)) & (endpoints | selected)) <= 1 for point in selected)
    phases = [phase_of(module) for module in originals]
    owner_at = {point: owner for owner, module in enumerate(originals) for point in module['endpoints']}
    data, closed, contacts, _, _ = closed_contacts(originals)
    regular, critical = [], []
    counts = Counter()
    for key, target in contacts.items():
        if phases[key[0]] != '01' or phases[target[0]] != '01':
            continue
        port = data[key[0]]['ports'][key[1]]
        if port['blank'] not in endpoints:
            continue
        first, second = port['inward'], port['exterior']
        point = add(add(port['point'], first), second)
        regular.append((key[0], point, (first, second)))
        counts['first_contacts'] += 1
        counts['closed01_contacts'] += key[0] in closed
        incoming = owner_at[point]
        if phases[incoming] != '11':
            continue
        width = positive_dimensions(originals[incoming])[0]
        height = max(sum((value-base)*direction for value, base, direction
                         in zip(site, port['point'], first)) for site in originals[key[0]]['endpoints'])
        if height >= width+4:
            forced = add(point, scale(first, width))
            regular.append((key[0], forced, (first, second)))
            counts['long_seconds'] += 1
            continue
        assert height == width+2
        root = add(point, scale(first, width-1))
        opposite = [site for site in originals[incoming]['endpoints']
                    if sum((value-base)*direction for value, base, direction
                           in zip(site, root, first)) == 0]
        far_height = max(sum((value-base)*direction for value, base, direction
                             in zip(site, root, second)) for site in opposite)
        assert far_height >= 4 and far_height % 2 == 0
        forced = add(root, scale(second, far_height+1))
        assert forced in originals[incoming]['selected'] & endpoints
        assert add(forced, first) in originals[key[0]]['endpoints']
        assert add(forced, scale(second, -1)) in originals[incoming]['endpoints']
        critical.append((key[0], incoming, forced, owner_at[forced]))
        counts['critical_seconds'] += 1

    assert len({record[2] for record in critical}) == len(critical)
    regular_tiles, additional = set(), set()
    nonfull = 0
    for owner, point, frame in regular:
        receiver = tile_of(point)
        assert receiver not in regular_tiles
        regular_tiles.add(receiver)
        cells = vertices_of({receiver})
        pair = {add(point, scale(frame[1], -1)), add(point, add(frame[0], scale(frame[1], -1)))}
        assert cells & originals[owner]['endpoints'] == pair
        extra = (cells & endpoints)-pair
        assert len(extra) in (1, 2) and point in extra and not additional & extra
        nonfull += len(extra) == 1
        additional.update(extra)

    returns, full_bar_tiles, bar_positions = Counter(), set(), set()
    for _, _, point, owner in critical:
        assert tile_of(point) not in regular_tiles
        assert point not in additional
        if phases[owner] != '01':
            counts['other_phase_critical_owners'] += 1
            continue
        assert point in bar_corners(originals[owner])
        receiver = tile_of(point)
        cells = vertices_of({receiver})
        assert cells <= originals[owner]['endpoints']
        assert receiver not in regular_tiles | full_bar_tiles
        assert not cells & (additional | bar_positions)
        full_bar_tiles.add(receiver)
        bar_positions.update(cells)
        returns[owner] += 1
        counts['phase01_bar_returns'] += 1
        counts['closed_phase01_bar_returns'] += owner in closed
    assert all(amount <= 2 for amount in returns.values())
    counts['owners_with_two_bar_returns'] = sum(amount == 2 for amount in returns.values())
    assert len(bar_positions) == 4*counts['phase01_bar_returns']
    assert len(additional | bar_positions)+nonfull == 2*len(regular)+4*counts['phase01_bar_returns']
    exact = inspect_exact(current, originals)
    passive = inspect_transfers(current, originals)['counted']
    assert passive+nonfull <= 2*exact['activated_positive']+exact['boundary_cost']
    assert len(additional | bar_positions)+2*exact['activated_positive']+exact['boundary_cost'] >= (
        2*len(regular)+4*counts['phase01_bar_returns']+passive)
    counts.update(regular_receivers=len(regular), regular_additional_points=len(additional),
                  bar_endpoint_positions=len(bar_positions), joint_positions=len(additional | bar_positions))
    return dict(counts=dict(counts), reserve=exact['event_reserve'], boundary=exact['boundary_cost'],
                retained_supports=len(selected), matching_edges=len(matching),
                objective=len(selected)+len(matching), half_area=rows*columns//2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    records = []
    widths = list(range(20, 42, 2))+[60, 100]
    controls = [('preceding_six_source', six_sources())]
    for width in widths:
        originals = family(width)
        network = combine(originals)
        assert network['endpoints'] == row_table(width)
        assert network['selected'] == LEFT_SUPPORT | {(row, width+3-column) for row, column in LEFT_SUPPORT}
        assert len(network['matching']) == 3*width+37
        fixed = inspect((20, width+4, network['selected'], network['matching']), originals)
        assert fixed['counts']['phase01_bar_returns'] == fixed['counts']['closed_phase01_bar_returns'] == 2
        assert fixed['counts']['owners_with_two_bar_returns'] == 1
        assert fixed['counts']['joint_positions'] == 12
        assert fixed['retained_supports'] == 44 and fixed['reserve'] == width-7
        assert fixed['boundary'] == 2*width-18
        assert fixed['half_area']-fixed['objective'] == 7*width-41
        records.append(dict(width=width, fixed=fixed))
        controls.append(('sharp_family_'+str(width), originals))
    for name, originals in controls:
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose
                      else (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset) for module in originals])
            record = inspect(current, moved)
            totals.update(record['counts'])
            totals['complete_feasible_images'] += 1
    for key in ('long_seconds', 'other_phase_critical_owners', 'closed01_contacts'):
        totals.setdefault(key, 0)
    result = dict(status='PASS', original_role_controls=owner_roles(), family_controls=records,
                  complete_controls=dict(totals), complete_AA_coverage=0,
                  scope='General role and packing claims have written proofs and scoped Lean. '
                        'The unbounded sharp family is proved by explicit source/row tables; '
                        'these13widths and112signed-isometry images are controls. '
                        'Full bar endpoints are not new H or reserve payments. '
                        'Other-phase critical, long-second and closed01-contact coverage is zero here; full target OPEN.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', original_role_controls=result['original_role_controls'],
                          complete_controls=dict(totals), family_widths=widths)))


if __name__ == '__main__':
    main()
