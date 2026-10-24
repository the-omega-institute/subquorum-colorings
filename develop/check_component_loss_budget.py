"""Check aggregate loss on physical complete-source component extensions."""

import itertools
import json

from check_closed_extension_reserve import signature
from check_component_receivers import vertices_of
from check_connected_marked_hull_obstruction import modules_at
from check_exact_event_reserve import fixtures, inspect_exact
from check_feasible_core_separator import contact_graph, components
from check_marked_side_gate_consumption import retained_families
from check_minus_one_joint_compensation import contained
from check_source_retention_closure import feasible, implications, marked_counts
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(modules, families):
    whole = frozenset(range(len(modules)))
    graph = contact_graph(modules)
    cache = {}

    def data(retained):
        if retained not in cache:
            assert feasible(modules, retained)
            endpoints = {point for owner in retained for point in modules[owner]['endpoints']}
            activation = sum(
                len(vertices_of({tile}) & modules[owner]['endpoints']) == 1 and
                len(vertices_of({tile}) & modules[owner]['selected']) == 2 and
                bool(vertices_of({tile}) & modules[owner]['selected'] & endpoints)
                for owner in retained if modules[owner]['charge'] == 1
                for tile in modules[owner]['receiver'])
            marks = marked_counts(modules, retained)
            marked = {(owner, side) for owner, sides in marks.items()
                      for side, present in enumerate(sides) if present}
            current = signature(modules, retained)
            current.update(activation=activation, positive=len(marks), marked=marked,
                           margin=len(marks)+current['reserve']-len(marked))
            assert 2*current['reserve'] >= activation
            cache[retained] = current
        return cache[retained]

    checked = subunions = multiple_loss = strict_loss = preserving = 0
    witness = None
    single_owner_witness = None
    full = data(whole)
    for core in families:
        parts = components(graph, whole-core)
        shared = data(core)
        branches = [data(core | part) for part in parts]
        deltas = [branch['reserve']-shared['reserve'] for branch in branches]
        losses = sum(max(0, -change) for change in deltas)
        minimum_set = core | frozenset().union(
            *(part for part, change in zip(parts, deltas) if change < 0))
        minimum = data(minimum_set)
        assert minimum['reserve'] == shared['reserve']-losses
        assert minimum['activation'] >= shared['activation']
        assert 2*losses <= 2*shared['reserve']-shared['activation']
        assert losses <= shared['reserve']-(shared['activation']+1)//2
        actual_minimum = full['reserve']
        demand_preserved = shared['positive'] == full['positive'] and shared['marked'] == full['marked']
        for mask in range(1 << len(parts)):
            chosen = [index for index in range(len(parts)) if mask >> index & 1]
            retained = core | frozenset().union(*(parts[index] for index in chosen))
            current = data(retained)
            for field in ['reserve', 'positive', 'margin']:
                assert current[field] == shared[field]+sum(
                    branches[index][field]-shared[field] for index in chosen)
            assert current['marked'] == shared['marked'] | set().union(
                *(branches[index]['marked']-shared['marked'] for index in chosen))
            new_marks = [branches[index]['marked']-shared['marked'] for index in chosen]
            assert sum(map(len, new_marks)) == len(current['marked']-shared['marked'])
            assert current['events'] == shared['events'] | set().union(
                *(branches[index]['events']-shared['events'] for index in chosen))
            assert sum(len(branches[index]['events']-shared['events']) for index in chosen) == len(
                current['events']-shared['events'])
            assert current['full'] == shared['full'] | set().union(
                *(branches[index]['full']-shared['full'] for index in chosen))
            assert sum(len(branches[index]['full']-shared['full']) for index in chosen) == len(
                current['full']-shared['full'])
            assert current['activation'] >= shared['activation']
            actual_minimum = min(actual_minimum, current['reserve'])
            if demand_preserved:
                assert current['positive'] == full['positive'] and current['marked'] == full['marked']
                assert current['margin'] >= shared['margin']-losses
            subunions += 1
        assert actual_minimum == minimum['reserve']
        if demand_preserved:
            assert minimum['margin'] == shared['margin']-losses
            assert (minimum['margin'] >= 0) == (losses <= shared['margin'])
            preserving += 1
        losing = sum(change < 0 for change in deltas)
        if losing >= 2:
            multiple_loss += 1
            if len(core) == 1:
                single_owner_witness = dict(core_owners_1based=sorted(owner+1 for owner in core),
                                            reserve_deltas=deltas, aggregate_loss=losses,
                                            core_reserve=shared['reserve'],
                                            minimizing_reserve=minimum['reserve'])
            if witness is None or losses > witness['aggregate_loss']:
                witness = dict(core_owners_1based=sorted(owner+1 for owner in core),
                               branch_owners_1based=[sorted(owner+1 for owner in part) for part in parts],
                               reserve_deltas=deltas, aggregate_loss=losses,
                               core_reserve=shared['reserve'], core_activation=shared['activation'],
                               minimizing_reserve=minimum['reserve'], demand_preserving=demand_preserved)
                if minimum_set:
                    current, moved = contained([modules[owner] for owner in sorted(minimum_set)])
                    independent = inspect_exact(current, moved)
                    assert independent['event_reserve'] == minimum['reserve']
                    assert independent['activated_positive'] == minimum['activation']
        strict_loss += int(losses > 0)
        checked += 1
    return dict(legal_core_extensions=checked, all_component_subunions=subunions,
                extensions_with_multiple_losing_groups=multiple_loss,
                extensions_with_strict_loss=strict_loss,
                demand_preserving_extensions=preserving, witness=witness,
                single_owner_witness=single_owner_witness)


def main():
    records = []
    for name, original in fixtures()+[('connected_hull24', modules_at(24)),
                                      ('connected_hull70', modules_at(70))]:
        clauses, _ = implications(original)
        families = retained_families(original, clauses)
        images = []
        for symmetry in itertools.product((False, True), repeat=3):
            for phase in itertools.product((0, 1), repeat=2):
                moved = [transform_module(module, symmetry, phase) for module in original]
                images.append(inspect(moved, families))
        keys = ['legal_core_extensions', 'all_component_subunions',
                'extensions_with_multiple_losing_groups', 'extensions_with_strict_loss',
                'demand_preserving_extensions']
        records.append(dict(fixture=name, owners=len(original), images=len(images),
                            **{key: sum(image[key] for image in images) for key in keys},
                            first_image_witness=images[0]['witness'],
                            first_image_single_owner_witness=images[0]['single_owner_witness']))
    print(json.dumps(dict(status='PASS', fixtures=records,
                         images=sum(row['images'] for row in records),
                         **{key: sum(row[key] for row in records) for key in keys},
                         scope='All component subunions for each tested legal core, actual '
                         'support feasibility, reserve/events/full tiles/marks, activation '
                         'persistence and aggregate minimum. Core subsets exhaustive through '
                         'nine owners; deterministic Horn-hull samples above nine. All32 '
                         'phase/isometry images per fixture. Finite controls supplement the '
                         'general proof; no full allocation or grid equality claim.'), indent=2))


if __name__ == '__main__':
    main()
