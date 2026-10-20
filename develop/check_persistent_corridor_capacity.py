"""Reconstruct permanent corridor receipts and legal lower-strip losses."""

from collections import Counter
import itertools
import json

from check_closed_extension_reserve import signature
from check_five_endpoint_cap import SYMMETRIES
from check_feasible_core_separator import contact_graph, components
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_pair_transfer_protected_defects import (
    inverse_of, original, physical_case, protected_fixtures,
)
from check_periodic_slab_compression import decode, defects
from check_source_retention_closure import feasible, hull, implications, marked_counts
from check_rotor_transfer_path_endings import side_frame
from dual_guard_compensation import paired_guards
from rotor_networks import combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def family(width, height, filling=False):
    modules = [original((width+4, height+8, height+8)),
               original((width+2, 4, 4), offset=(2, 1)),
               original((width+2, height, height),
                        (False, True, False), (height+7, 1)),
               original((width, height, height), offset=(5, 2))]
    if filling:
        assert width >= 8 and height >= 6
        modules.append(original((width-2, height-2, height-2), offset=(7, 3)))
    return modules


def tile_of(cells):
    key = tuple(value//2 for value in next(iter(cells)))
    assert cells == vertices_of({key})
    return key


def original_matches(module, dimensions, symmetry, offset):
    if dimensions[0] < 6 or min(dimensions[1:]) < 4 or any(value % 2 for value in dimensions):
        return False
    expected = original(dimensions, symmetry, offset)
    return all(module[field] == expected[field] for field in ['endpoints', 'selected'])


def local_module(module, inverse):
    return dict(module, endpoints={inverse(point) for point in module['endpoints']},
                selected={inverse(point) for point in module['selected']})


def frames(module, translation):
    if module['guard'] is None:
        return
    (width, near, far), move = decode(module)
    row_shift, column_shift = translation
    for reflected in (False, True):
        def chart(point, reflected=reflected):
            row, column = point[0]-row_shift, point[1]-column_shift
            return move((row, width+1-column if reflected else column))
        cells = {chart(point) for point in vertices_of({(0, 0)})}
        key = tuple(value//2 for value in next(iter(cells)))
        if cells == vertices_of({key}):
            yield (width, far if reflected else near, near if reflected else far), chart


def certificates(modules):
    caps = set()
    upper = set()
    lower = set()
    upper_owners = {}
    claim_labels = set()
    for bar_owner, bar in enumerate(modules):
        for (width, near, far), move in frames(bar, (2, 1)):
            inverse = inverse_of(move)
            for strip_owner, strip in enumerate(modules):
                if strip_owner == bar_owner or strip['guard'] is None:
                    continue
                current = local_module(strip, inverse)
                points = current['endpoints']
                strip_width = max(column for _, column in points)-2
                strip_near = max(row for row, column in points if column == 3)-5 if any(
                    column == 3 for _, column in points) else 0
                strip_far = max(row for row, column in points if column == strip_width+2)-5
                if not original_matches(current, (strip_width, strip_near, strip_far),
                                        (False, False, False), (5, 2)):
                    continue
                assert strip_width <= width-2
                if strip_width < width-4:
                    continue
                cap = tile_of({move(point) for point in vertices_of({(2, 1)})})
                pairs = {tile_of({move(point) for point in vertices_of({(2, column//2)})})
                         for column in range(4, strip_width+2, 2)}
                assert len(pairs) == strip_width//2-1
                assert (bar_owner, strip_owner, cap) not in claim_labels
                claim_labels.add((bar_owner, strip_owner, cap))
                caps.add(cap)
                upper.update(pairs)
                if strip_owner in upper_owners:
                    assert upper_owners[strip_owner] == pairs
                upper_owners[strip_owner] = pairs
        for (width, near, far), move in frames(bar, (3, 2)):
            if near != 4:
                continue
            inverse = inverse_of(move)
            for return_owner, returning in enumerate(modules):
                if return_owner == bar_owner or returning['guard'] is None:
                    continue
                current = local_module(returning, inverse)
                points = current['endpoints']
                return_width = max(column for _, column in points)-1
                if not any(column == 2 for _, column in points):
                    continue
                return_near = 9-min(row for row, column in points if column == 2)
                return_far = 9-min(row for row, column in points if column == return_width+1)
                if not original_matches(current, (return_width, return_near, return_far),
                                        (False, True, False), (9, 1)):
                    continue
                last = min(width+2, return_width+1)
                lower.update(tile_of({move(point) for point in vertices_of({(2, column//2)})})
                             for column in range(4, last-1, 2))
    assert len(claim_labels) == len(caps)
    assert len(caps) <= 2*len(upper_owners) <= len(upper)
    assert not caps & upper and not caps & lower and not upper & lower
    return caps, upper, lower, upper_owners


def check_receipts(modules):
    whole = frozenset(range(len(modules)))
    assert feasible(modules, whole)
    endpoints = {point for module in modules for point in module['endpoints']}
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    caps, upper, lower, strip_owners = certificates(modules)
    values, boundary, reserve = defects(modules)
    for tile in caps:
        cells = vertices_of({tile})
        profiles = sorted((len(cells & module['endpoints']), len(cells & module['selected']))
                          for module in modules if cells & module['endpoints'])
        assert len(cells & endpoints) == 3 and profiles == [(1, 1), (2, 1)]
        assert boundary[tile] == 1
    for tile in upper | lower:
        cells = vertices_of({tile})
        profiles = [(len(cells & module['endpoints']), len(cells & module['selected']))
                    for module in modules if cells & module['endpoints']]
        assert len(cells & endpoints) == 2 and profiles == [(2, 0)]
        assert boundary[tile] == 2
    _, activations, prior = physical_case(modules, whole, with_labels=True)
    prior_tiles = {receipt[-1] for receipt in prior}
    assert not prior_tiles & (caps | upper | lower)
    certified = caps | upper | lower
    for module in modules:
        for point in module['endpoints']:
            if tuple(value//2 for value in point) in certified:
                assert len(set(neighbors(point)) & module['endpoints']) > 1
        if module['charge'] == 1:
            assert all(tuple(value//2 for value in gate) not in certified
                       for gate, _, _, _ in paired_guards(module))
    assert 2*reserve >= len(activations)+len(prior)+len(caps)+2*len(upper | lower)
    owners = {point: owner for owner, module in enumerate(modules) for point in module['endpoints']}
    claims = set()
    transferred = marked = 0
    for producer, sides in marked_counts(modules, whole).items():
        for side, is_marked in enumerate(sides):
            if not is_marked:
                continue
            marked += 1
            _, move = side_frame(modules[producer], side)
            consumer = modules[owners[move((3, 2))]]
            if consumer['charge'] == 1 or consumer['guard'] is None:
                transferred += 1
                continue
            current = local_module(consumer, inverse_of(move))
            points = current['endpoints']
            width = max(column for _, column in points)-1
            if not any(column == 2 for _, column in points):
                continue
            near = max(row for row, column in points if column == 2)-2
            far = max(row for row, column in points if column == width+1)-2
            if not original_matches(current, (width, near, far),
                                    (False, False, False), (2, 1)):
                continue
            cap = tile_of({move(point) for point in vertices_of({(2, 1)})})
            if cap in caps:
                assert cap not in claims
                claims.add(cap)
    uncovered = marked-transferred-len(claims)
    positive = sum(module['charge'] == 1 for module in modules)
    assert transferred <= len(activations) and uncovered >= 0 and marked <= 2*positive
    allocation_floor = len(upper | lower)+(len(prior)-uncovered+1)//2
    assert positive+reserve-marked >= allocation_floor
    covered = uncovered <= 2*len(upper | lower)+len(prior)+1
    if covered:
        assert positive+reserve-marked >= 0
    return dict(caps=len(caps), upper_pairs=len(upper), lower_pairs=len(lower),
                distinct_upper_owners=len(strip_owners), m8=len(prior),
                activated=values[0], reserve=reserve,
                certified_negative_gates=len(claims), uncovered_negative_gates=uncovered,
                coverage_criterion_passes=int(covered))


def complete_profile(modules, width, height, stage):
    whole = frozenset(range(len(modules)))
    network = combine(modules)
    endpoints, selected = network['endpoints'], network['selected']
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert len(network['matching'])*2 == len(endpoints)
    assert all(len(set(neighbors(point)) & (endpoints | selected)) == 1 for point in selected)
    assert all(len(set(neighbors(point)) & (endpoints | selected)) >= 3 for point in endpoints)
    seen = {next(iter(endpoints))}
    pending = list(seen)
    while pending:
        for point in set(neighbors(pending.pop())) & endpoints-seen:
            seen.add(point)
            pending.append(point)
    assert seen == endpoints
    outer = {(row, column) for row in range(0, height+9, 2) for column in (0, width+5)}
    outer |= {(height+9, 1), (height+9, width+4)}
    if stage == 'I':
        inner = {(5, 3), (5, width+2)}
        inner |= {(row, column) for row in range(8, height+5, 2) for column in (3, width+2)}
        expected_endpoints = 6*width+4*height+34
        expected_selected = 2*height+12
        expected_reserve = 2
    elif stage == 'J':
        inner = {(row, column) for row in range(8, height+5, 2) for column in (4, width+1)}
        expected_endpoints = 8*width+6*height+32
        expected_selected = 2*height+10
        expected_reserve = width-1
    else:
        inner = {(row, column) for row in range(10, height+5, 2) for column in (5, width)}
        expected_endpoints = 10*width+8*height+22
        expected_selected = 2*height+8
        expected_reserve = width-2
    assert selected == outer | inner
    assert (len(endpoints), len(selected)) == (expected_endpoints, expected_selected)
    values, boundary, reserve = defects(modules)
    assert reserve == expected_reserve and values == (0, 2 if stage == 'K' else 0, 0)
    expected_boundary = ({(3, 1): 2, (3, (width+2)//2): 2} if stage == 'I' else
                         {(2, 1): 1, (2, (width+2)//2): 1})
    if stage != 'I':
        for column in range(4, width+2, 2):
            expected_boundary[(2, column//2)] = 2
        lower_row = 3 if stage == 'J' else 4
        first = 4 if stage == 'J' else 6
        last = width+2 if stage == 'J' else width
        for column in range(first, last, 2):
            expected_boundary[(lower_row, column//2)] = 2
    assert boundary == expected_boundary, (stage, width, height, boundary, expected_boundary)
    marks = marked_counts(modules, whole)
    assert marks == {0: (True, True)}
    clauses, _ = implications(modules)
    assert hull(clauses, {0, 1}) == frozenset({0, 1, 2})
    return dict(stage=stage, width=width, height=height, endpoints=len(endpoints),
                matching=len(network['matching']), selected=len(selected),
                reserve=reserve, margin=reserve-1)


def physical_controls():
    totals = Counter()
    examples = []
    for width, height in itertools.product((6, 8, 14, 22), (4, 6, 12)):
        base = family(width, height)
        stages = [('I', base[:3]), ('J', base)]
        if width >= 8 and height >= 6:
            stages.append(('K', family(width, height, True)))
        for stage, modules in stages:
            examples.append(complete_profile(modules, width, height, stage))
            for symmetry in SYMMETRIES:
                for phase in itertools.product((0, 1), repeat=2):
                    moved = [transform_module(module, symmetry, phase) for module in modules]
                    counts = check_receipts(moved)
                    totals.update(counts)
                    totals['images'] += 1
                    if stage == 'J' and counts['caps']:
                        assert counts['caps'] == 2 and counts['distinct_upper_owners'] == 1
                        assert counts['upper_pairs'] == width//2-1
                        assert counts['lower_pairs'] == (width//2-1 if height == 4 else 0)
                        totals['double_corner_single_strip_controls'] += 1
        if width >= 8 and height >= 6:
            filled = family(width, height, True)
            assert signature(filled, frozenset(range(5)))['reserve']-signature(
                base, frozenset(range(4)))['reserve'] == -1
            full = {point for module in filled for point in module['endpoints']}
            for column in range(4, width+2, 2):
                assert vertices_of({(3, column//2)}) <= full
    for _, modules in protected_fixtures()[:2]:
        moved_family = family(8, 4)
        combined = modules+[transform_module(module, (False, False, False), (100, 100))
                            for module in moved_family]
        counts = check_receipts(combined)
        assert counts['m8'] == 1 and counts['caps'] == 2 and counts['lower_pairs'] == 3
        totals['mixed_m8_corridor_receipt_controls'] += 1
    return dict(totals=totals, complete_parametric_examples=examples)


def corridor_role_controls():
    totals = Counter()
    candidates = []
    for dimensions in itertools.product((6, 8, 14), (4, 6, 10), (4, 6, 10)):
        for symmetry in SYMMETRIES:
            module = original(dimensions, symmetry)
            for terminal in module['endpoints']:
                own = set(neighbors(terminal)) & module['endpoints']
                if own == {(terminal[0], terminal[1]+1)}:
                    candidates.append(transform_module(module, (False, False, False),
                                                       (4-terminal[0], 3-terminal[1])))
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry)
        for terminal in module['endpoints']:
            if set(neighbors(terminal)) & module['endpoints'] == {(terminal[0], terminal[1]+1)}:
                candidates.append(transform_module(module, (False, False, False),
                                                   (4-terminal[0], 3-terminal[1])))
    for width, strip_width in itertools.product((8, 10, 14, 20), (6, 8, 12, 18)):
        bar = original((width, 8, 10), offset=(2, 1))
        strip = original((strip_width, 8, 10), offset=(5, 2))
        if bar['endpoints'] & strip['endpoints']:
            continue
        assert strip_width <= width-2
        occupied = bar['endpoints'] | strip['endpoints']
        for module in candidates:
            if module['endpoints'] & occupied:
                continue
            assert module['guard'] is not None
            points = module['endpoints']
            height = max(column for _, column in points)-3
            stem_width = max(row for row, _ in points)-3
            far = height+3-min(column for row, column in points if row == stem_width+3)
            expected = original((stem_width, height, far), (True, True, False), (3, height+3))
            assert all(module[field] == expected[field] for field in ['endpoints', 'selected'])
            assert strip_width+2 <= height <= width-4
            assert {(4, column) for column in range(3, strip_width+3)} <= points
            totals['endpoint_disjoint_possible_entries'] += 1
        totals['bar_pairs'] += 1
    totals['anchored_terminal_or_tip_candidates'] = len(candidates)
    return totals


def aggregate_controls():
    totals = Counter()
    full = family(8, 6, True)
    for symmetry in SYMMETRIES:
        for phase in itertools.product((0, 1), repeat=2):
            modules = [transform_module(module, symmetry, phase) for module in full]
            graph = contact_graph(modules)
            for mask in range(1 << len(modules)):
                core = frozenset(index for index in range(len(modules)) if mask >> index & 1)
                if not feasible(modules, core):
                    continue
                if not core:
                    continue
                old_modules = [modules[index] for index in sorted(core)]
                old_caps, old_upper, old_lower, _ = certificates(old_modules)
                _, old_activated, old_prior = physical_case(old_modules,
                    frozenset(range(len(old_modules))), with_labels=True)
                old_reserve = signature(modules, core)['reserve']
                parts = components(graph, frozenset(range(len(modules)))-core)
                deltas = [signature(modules, core | part)['reserve']-old_reserve for part in parts]
                loss = sum(max(0, -delta) for delta in deltas)
                floor = (len(old_upper)+len(old_lower)+
                         (len(old_activated)+len(old_prior)+len(old_caps)+1)//2)
                minimum = old_reserve
                for subset in range(1 << len(parts)):
                    retained = core | frozenset().union(*(part for index, part in enumerate(parts)
                                                         if subset >> index & 1))
                    assert feasible(modules, retained)
                    chosen = [modules[index] for index in sorted(retained)]
                    caps, upper, lower, _ = certificates(chosen)
                    assert old_caps <= caps and old_upper <= upper and old_lower <= lower
                    reserve = signature(modules, retained)['reserve']
                    assert reserve >= floor
                    minimum = min(minimum, reserve)
                    totals['legal_component_subunions'] += 1
                assert minimum == old_reserve-loss
                assert loss <= old_reserve-floor
                totals['legal_nonempty_cores'] += 1
                totals['losing_cores_with_corridor_receipts'] += bool(loss and old_caps)
    combined = family(8, 6)+[transform_module(module, (False, False, False), (100, 100))
                             for module in family(8, 6)]
    additions = [family(8, 6, True)[-1], transform_module(
        family(8, 6, True)[-1], (False, False, False), (100, 100))]
    modules = combined+additions
    core = frozenset(range(len(combined)))
    graph = contact_graph(modules)
    parts = components(graph, frozenset(range(len(modules)))-core)
    assert len(parts) == 2
    base = check_receipts(combined)
    assert (base['caps'], base['upper_pairs'], base['distinct_upper_owners']) == (4, 6, 2)
    assert signature(modules, core)['reserve'] == 14
    for subset in range(1 << len(parts)):
        retained = core | frozenset().union(*(part for index, part in enumerate(parts)
                                             if subset >> index & 1))
        assert feasible(modules, retained)
        assert signature(modules, retained)['reserve'] == 14-subset.bit_count()
        check_receipts([modules[index] for index in sorted(retained)])
    totals['two_simultaneous_loss_certificate'] = 1
    totals['simultaneous_loss'] = 2
    totals['simultaneous_persistent_floor'] = 8
    return totals


def main():
    result = dict(status='PASS', physical=physical_controls(),
                  partial_role_controls=corridor_role_controls(),
                  aggregate=aggregate_controls(),
                  scope='Exact original support and matching reconstruction, actual aligned '
                        'tile certificates, double-corner strip deduplication and m8 '
                        'cross-class controls. Partial entry patterns are not complete '
                        'realizations. Finite checks supplement the general written '
                        'corridor/nonreuse proof; no full allocation or grid theorem.')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
