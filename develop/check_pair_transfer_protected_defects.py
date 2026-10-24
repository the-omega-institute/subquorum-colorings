"""Check actual positive transfers and the permanent pair-attachment receipts."""

from collections import Counter
import itertools
import json

from check_component_receivers import vertices_of
from check_closed_extension_reserve import signature
from check_connected_marked_hull_obstruction import modules_at
from check_demand_hull_reserve_obstruction import independent_source
from check_demand_hull_reserve_obstruction import report as independent_report
from check_exact_event_reserve import fixtures
from check_five_endpoint_cap import SYMMETRIES
from check_feasible_core_separator import contact_graph, components
from check_marked_side_gate_consumption import retained_families
from check_minus_one_tip_obstructions import source
from check_periodic_slab_compression import canonical_demand_hull, decode
from check_source_retention_closure import feasible, implications, marked_counts
from dual_guard_compensation import paired_guards
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def original(parameters, symmetry=(False, False, False), offset=(0, 0)):
    module = transform_module(source(*parameters), symmetry, offset)
    endpoints, supports, matching = independent_source(parameters, symmetry, offset)
    assert endpoints == module['endpoints'] and supports == module['selected']
    assert matching == {tuple(sorted(edge)) for edge in module['matching']}
    return module


def inverse_of(move):
    origin = move((0, 0))
    axes = [tuple(value-start for value, start in zip(move(point), origin))
            for point in [(1, 0), (0, 1)]]
    return lambda point: tuple(sum((value-start)*step for value, start, step in
                                   zip(point, origin, axis)) for axis in axes)


def recipient_frame(module, gate):
    (width, left, right), move = decode(module)
    local = inverse_of(move)(gate)
    if local == (0, 1):
        return (width, left, right), move
    assert local == (0, width), local
    return (width, right, left), lambda point: move((point[0], width+1-point[1]))


def rectangle_points(bounds):
    lower, upper, first, last = bounds
    inside = {(row, column) for row in range(lower+1, upper)
              for column in range(first+1, last)}
    boundary = {(row, column) for row in range(lower, upper+1)
                for column in range(first, last+1)
                if row in (lower, upper) or column in (first, last)}
    return inside, boundary


def same_original(first, second):
    return all(first[field] == second[field] for field in ['endpoints', 'selected'])


def consumer_case(base_width, cross_width, cross_far, consumer):
    endpoints = consumer['endpoints']
    width = max(column for _, column in endpoints)-1
    far = max(row for row, column in endpoints if column == width+1)-2
    if width >= 6 and far >= 4 and width % 2 == far % 2 == 0:
        expected = original((width, 4, far), offset=(2, 1))
        if same_original(consumer, expected):
            assert width+1 < base_width
            assert width+1 != cross_width-1
            if width+1 < cross_width-1:
                assert far == 4
                return 'I-short', None, (6, width), (3, 7, 1, width+1)
            assert cross_far == 4
            return 'I-cross', 1, (6, cross_width-2), (3, 7, 1, cross_width-1)
    far = 6-min(row for row, column in endpoints if column == width+1)
    if width >= 6 and far >= 4 and width % 2 == far % 2 == 0:
        expected = original((width, 4, far), (False, True, False), (6, 1))
        if same_original(consumer, expected):
            return 'II', 2, (4, 3), (1, 5, 2, min(base_width, width+1))
    width = max(row for row, _ in endpoints)-2
    near = max(column for _, column in endpoints)-2
    far = near+2-min(column for row, column in endpoints if row == width+2)
    assert width >= 6 and min(near, far) >= 4
    expected = original((width, near, far), (True, True, False), (2, near+2))
    assert same_original(consumer, expected)
    assert cross_width <= near <= base_width-4 and cross_far == 4
    return 'III', 1, (6, cross_width-2), (3, 7, 1, cross_width-1)


def inspect_receipt(base, cross, consumer, check_other_owners=()):
    width, near, far = decode(base)[0]
    assert near == 6 and base['charge'] == 1
    cross_width = max(column for _, column in cross['endpoints'])+1
    cross_far = 8-min(row for row, column in cross['endpoints'] if column == cross_width-1)
    assert same_original(cross, original((cross_width, 8, cross_far),
                                        (False, True, False), (8, -1)))
    modules = [base, cross, consumer]
    endpoints = set().union(*(module['endpoints'] for module in modules))
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    kind, cap_owner, missing, bounds = consumer_case(width, cross_width, cross_far, consumer)
    inside, boundary = rectangle_points(bounds)
    assert bounds[1]-bounds[0] == 4 and boundary <= endpoints
    assert missing in inside and missing not in endpoints
    tile = (missing[0]//2, missing[1]//2)
    cells = vertices_of({tile})
    assert len(cells & endpoints) == 3
    split = sorted(len(cells & module['endpoints']) for module in modules
                   if cells & module['endpoints'])
    assert split == ([1, 2] if cap_owner is None else [3])
    if cap_owner is not None:
        assert len(cells & modules[cap_owner]['endpoints']) == 3
    for other in check_other_owners:
        assert not other['endpoints'] & inside
    return kind, cap_owner, tile, missing, bounds


def local_controls():
    thin = receipts = 0
    cases = Counter()
    for width, other, cross_width, cross_far in itertools.product(
            (6, 8, 12, 20), (4, 6, 10), (6, 8, 12, 20), (4, 6, 10)):
        for near, height in [(4, 6), (6, 8)]:
            base = original((width, near, other))
            cross = original((cross_width, height, cross_far),
                             (False, True, False), (height, -1))
            if base['endpoints'] & cross['endpoints']:
                continue
            if height == 6:
                inside, boundary = rectangle_points((1, 5, 1, min(width, cross_width-1)))
                endpoints = base['endpoints'] | cross['endpoints']
                assert boundary <= endpoints and (3, 2) in inside and (3, 2) not in endpoints
                thin += 1
                continue
            for consumer_width, far in itertools.product((6, 8, 12, 20), (4, 6, 10)):
                choices = [original((consumer_width, 4, far), offset=(2, 1)),
                           original((consumer_width, 4, far), (False, True, False), (6, 1))]
                choices += [original((consumer_width, incident, far),
                                     (True, True, False), (2, incident+2))
                            for incident in (6, 8, 12, 20)]
                for consumer in choices:
                    modules = [base, cross, consumer]
                    endpoints = set().union(*(module['endpoints'] for module in modules))
                    if len(endpoints) != sum(len(module['endpoints']) for module in modules):
                        continue
                    kind, _, _, _, _ = inspect_receipt(base, cross, consumer)
                    cases[kind] += 1
                    receipts += 1
    return dict(thin_enclosures=thin, protected_receipt_geometries=receipts,
                receipt_types=dict(cases),
                scope='Independent complete-source/matching reconstructions. Endpoint-disjoint '
                      'partial patterns verify every boundary, missing corner and original '
                      'owner split. No complete fusion or realizability is inferred from them.')


def protected_fixtures():
    common = [original((14, 12, 4), (True, False, False), (-2, -2)),
              original((8, 6, 6)),
              original((10, 8, 8), (False, True, False), (8, -1))]
    cap = original((6, 4, 4), (False, True, False), (4, 9))
    short = common+[original((6, 4, 4), offset=(2, 1)), cap]
    inverted = common+[original((6, 4, 4), (False, True, False), (6, 1)), cap]
    separated = short+[transform_module(module, (False, False, False), (50, 50))
                       for module in inverted]
    losing = short+[transform_module(module, (False, False, False), (120, 80))
                    for module in modules_at(70)]
    return [('complete_m8_mixed', short), ('complete_m8_cap', inverted),
            ('two_complete_m8_receipts', separated), ('protected_m8_with_loss', losing)]


def owner_role_controls():
    prepared = []
    for dimensions in itertools.product((6, 8, 14), (4, 6, 8, 12), (4, 6, 8, 12)):
        for symmetry in SYMMETRIES:
            oriented = original(dimensions, symmetry)
            for point in oriented['endpoints']:
                offset = (3-point[0], 2-point[1])
                module = transform_module(oriented, (False, False, False), offset)
                if module['endpoints'] & {(1, 2), (3, 1), (7, 2)}:
                    continue
                prepared.append(module)
    counts = Counter()
    images = 0
    for width, far, cross_width, cross_far in itertools.product(
            (6, 8, 14, 20), (4, 6), (6, 8, 14), (4, 6)):
        base = original((width, 6, far))
        cross = original((cross_width, 8, cross_far), (False, True, False), (8, -1))
        if base['endpoints'] & cross['endpoints']:
            continue
        fixed = base['endpoints'] | cross['endpoints']
        for candidate in prepared:
            if candidate['endpoints'] & fixed:
                continue
            kind, _, _, _ = consumer_case(width, cross_width, cross_far, candidate)
            assert candidate['charge'] < 0
            counts[kind] += 1
        images += 1
    cross_collisions = 0
    for width in (6, 8, 14, 40):
        transformed = {(row-2, width+1-column) for row in [3]
                       for column in range(2, width)}
        assert (1, 3) in transformed
        cross_collisions += 1
    return dict(parameter_images=images, all_anchored_u_role_controls=dict(counts),
                cross_cap_collision_controls=cross_collisions,
                scope='Finite original-role controls of the general three-form classification; '
                      'all eight isometries and every endpoint role, no translation cutoff '
                      'within the explicitly bounded parameter library. Not an unbounded proof.')


def physical_case(modules, retained, with_labels=False):
    owners = {point: owner for owner in retained for point in modules[owner]['endpoints']}
    activations = {(owner, tile) for owner in retained if modules[owner]['charge'] == 1
                   for tile in modules[owner]['receiver']
                   if len(vertices_of({tile}) & modules[owner]['endpoints']) == 1 and
                   len(vertices_of({tile}) & modules[owner]['selected']) == 2 and
                   bool(vertices_of({tile}) & modules[owner]['selected'] & owners.keys())}
    assignments = set()
    receipts = set()
    counts = Counter({key: 0 for key in ['singleton_transfers', 'pair_transfers',
                     'permanently_unmarked_pair_recipients', 'm8_attachment_patterns',
                     'marked_m8_receipts_I-short', 'marked_m8_receipts_II',
                     'marked_m8_receipts_I-cross', 'marked_m8_receipts_III']})
    for producer, sides in marked_counts(modules, retained).items():
        for marked, (gate, _, _, _) in zip(sides, paired_guards(modules[producer])):
            if not marked:
                continue
            consumer_owner = owners[gate]
            consumer = modules[consumer_owner]
            if consumer['charge'] != 1:
                continue
            tile = tuple(value//2 for value in gate)
            profile = len(vertices_of({tile}) & consumer['endpoints'])
            if profile == 1:
                target = (consumer_owner, tile)
                counts['singleton_transfers'] += 1
            else:
                assert profile == 2
                (width, near, far), move = recipient_frame(consumer, gate)
                inverse = inverse_of(move)
                terminal = move((near, 1))
                target = (consumer_owner, tuple(value//2 for value in terminal))
                cross_owner = owners[move((0, 0))]
                cross = modules[cross_owner]
                local_endpoints = {inverse(point) for point in cross['endpoints']}
                height = max(row for row, column in local_endpoints if column == 0)
                cross_width = max(column for _, column in local_endpoints)+1
                cross_far = height-min(row for row, column in local_endpoints
                                       if column == cross_width-1)
                expected = original((cross_width, height, cross_far),
                                    (False, True, False), (height, -1))
                assert local_endpoints == expected['endpoints']
                assert {inverse(point) for point in cross['selected']} == expected['selected']
                assert height >= near+2 and move((near, 0)) in cross['endpoints']
                counts['pair_transfers'] += 1
                receiving_gate = move((3, 2))
                if height == 6:
                    assert near == 4 and receiving_gate not in owners
                    counts['permanently_unmarked_pair_recipients'] += 1
                if near == 6 and height == 8:
                    counts['m8_attachment_patterns'] += 1
                    if receiving_gate in owners:
                        current_owner = owners[receiving_gate]
                        current = modules[current_owner]
                        local_consumer = dict(current,
                            endpoints={inverse(point) for point in current['endpoints']},
                            selected={inverse(point) for point in current['selected']})
                        others = [dict(module, endpoints={inverse(point) for point in module['endpoints']})
                                  for owner, module in enumerate(modules) if owner in retained and
                                  owner not in {consumer_owner, cross_owner, current_owner}]
                        kind, cap_owner, receipt_tile, _, _ = inspect_receipt(
                            original((width, near, far)), expected, local_consumer, others)
                        physical_tile = {move(point) for point in vertices_of({receipt_tile})}
                        tile_key = tuple(value//2 for value in next(iter(physical_tile)))
                        assert physical_tile == vertices_of({tile_key})
                        owner_key = (cross_owner if cap_owner == 1 else current_owner)
                        receipt = ('mixed', tile_key) if cap_owner is None else ('cap', owner_key, tile_key)
                        assert receipt not in receipts
                        receipts.add(receipt)
                        counts['marked_m8_receipts_'+kind] += 1
            assert target in activations and target not in assignments
            assignments.add(target)
    assert len(assignments) <= len(activations)
    return (counts, activations, receipts) if with_labels else counts


def physical_controls():
    images = restrictions = 0
    counts = Counter()
    extensions = protected_extensions = losing_protected = strict_floors = 0
    chosen_fixtures = fixtures()+[('connected_hull6', modules_at(6)),
                                 ('connected_hull24', modules_at(24))]+protected_fixtures()
    for _, original_modules in chosen_fixtures:
        clauses, _ = implications(original_modules)
        families = retained_families(original_modules, clauses)
        for symmetry in SYMMETRIES:
            for phase in itertools.product((0, 1), repeat=2):
                modules = [transform_module(module, symmetry, phase) for module in original_modules]
                for retained in families:
                    assert feasible(modules, retained)
                    counts.update(physical_case(modules, retained))
                    restrictions += 1
                core = canonical_demand_hull(modules, clauses)
                _, activated, receipts = physical_case(modules, core, with_labels=True)
                old = signature(modules, core)['reserve']
                graph = contact_graph(modules)
                parts = components(graph, frozenset(range(len(modules)))-core)
                deltas = [signature(modules, core | part)['reserve']-old for part in parts]
                loss = sum(max(0, -delta) for delta in deltas)
                minimum = None
                for mask in range(1 << len(parts)):
                    retained = core | frozenset().union(*(part for index, part in enumerate(parts)
                                                         if mask >> index & 1))
                    assert feasible(modules, retained)
                    _, current_activated, current_receipts = physical_case(modules, retained, True)
                    assert activated <= current_activated and receipts <= current_receipts
                    reserve = signature(modules, retained)['reserve']
                    assert 2*reserve >= len(activated)+len(receipts)
                    minimum = reserve if minimum is None else min(minimum, reserve)
                    extensions += 1
                    protected_extensions += bool(receipts)
                assert minimum == old-loss
                assert 2*loss <= 2*old-len(activated)-len(receipts)
                losing_protected += int(bool(receipts) and loss > 0)
                strict_floors += int((len(activated)+len(receipts)+1)//2 >
                                    (len(activated)+1)//2)
                images += 1
    return dict(images=images, complete_legal_restrictions=restrictions,
                actual_transfers=dict(counts),
                canonical_component_subextensions=extensions,
                subextensions_with_protected_receipts=protected_extensions,
                losing_canonical_hulls_with_protected_receipts=losing_protected,
                canonical_hulls_with_stronger_integer_floor=strict_floors,
                scope='Actual full-feasibility restrictions, original positive gate consumers, '
                      'singleton/pair activation targets and cross-type injectivity. All32 '
                      'phase/isometry images. Subsets exhaustive through9owners; deterministic '
                      'Horn-hull samples above9. Zero counts explicitly retain uncovered channels.')


def complete_certificates():
    result = []
    for name, modules in protected_fixtures()[:2]:
        whole = frozenset(range(len(modules)))
        assert feasible(modules, whole)
        current = independent_report(modules, whole)
        counts = physical_case(modules, whole)
        assert sum(value for key, value in counts.items() if key.startswith('marked_m8_receipts_')) == 1
        assert (current['positive'], current['marked'], current['event_reserve'],
                current['activated_positive'], current['exact_joint_margin']) == (2, 3, 13, 2, 12)
        result.append(dict(name=name, original_sources=5,
                           independent_physical_report=current,
                           actual_transfers=dict(counts),
                           old_persistent_reserve_floor=1,
                           new_persistent_reserve_floor=2))
    return result


def main():
    print(json.dumps(dict(status='PASS', local=local_controls(), owner_roles=owner_role_controls(),
                         physical=physical_controls(), complete_certificates=complete_certificates(),
                         scope='Finite controls supplement general catalogue, connected-source '
                         'enclosure, receipt-injection and permanent-loss proofs. No bounded '
                         'enumeration proves the general allocation or grid equality.'), indent=2))


if __name__ == '__main__':
    main()
