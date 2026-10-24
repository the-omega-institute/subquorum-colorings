"""Complete connected positive-demand sources obstruct pointwise cut payments."""

from collections import Counter
import json

from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_exact_event_reserve import inspect_exact
from check_minus_one_joint_compensation import contained
from check_source_retention_closure import cut_modules, hull, implications, marked_counts
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def connected(endpoints):
    reached = {min(endpoints)}
    pending = list(reached)
    while pending:
        fresh = (set(neighbors(pending.pop())) & endpoints)-reached
        reached.update(fresh)
        pending.extend(fresh)
    return reached == endpoints


def selected_formula(length):
    return ({(row, -1) for row in range(-length-2, 3, 2)} | {(3, 0)} |
            {(3, 2), (3, 4), (8, 3), (8, 5), (8, 7), (7, 2), (6, 4)} |
            {(2, 9), (-length-7, 5), (-length-7, 7), (-length-7, 9),
             (-length-6, 4), (-length-5, 6)} |
            {(row, column) for row in range(-length+1, -2, 2) for column in (2, 5)})


def inspect(length):
    assert length >= 4 and length % 2 == 0
    first = cut_modules(length, 8)
    fixed = [transform_module(module, (False, False, True), (18, 16))
             for module in cut_modules(4, 8)]
    modules = first+fixed
    network = combine(modules)
    endpoints, selected = network['endpoints'], network['selected']
    occupied = endpoints | selected
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert len(endpoints) == 2*len(network['matching']) == 6*length+176
    assert all(sum(abs(first_point[index]-second_point[index]) for index in (0, 1)) == 1
               for first_point, second_point in network['matching'])
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in selected)
    assert all(len(set(neighbors(point)) & occupied) >= 3 for point in endpoints)
    assert connected(endpoints)
    assert combine(first)['selected'] == selected_formula(length)
    assert selected == ((selected_formula(length)-{(8, 7)}) |
                        {(row+18, 16-column) for row, column in selected_formula(4)}-
                        {(7, 7)})
    assert len(selected) == 3*length//2+34
    assert [phase_of(module) for module in modules] == ['01', '01', '01', '10',
                                                       '00', '11', '11', '11']
    assert [module['charge'] for module in modules] == [-1, -1, -1, -5, 1, -5, -11, -5]
    census = Counter((len(vertices_of({tile}) & endpoints),
                      len(vertices_of({tile}) & selected)) for tile in network['receiver'])
    assert census == Counter({(4, 0): 3*length//2+25, (2, 1): 15, (2, 0): 14,
                              (3, 0): 5, (1, 1): 2, (1, 2): 1})
    current, moved = contained(modules)
    report = inspect_exact(current, moved)
    assert (report['positive'], report['marked'], report['activated_positive'],
            report['unused_u_triples'], report['unpaired_rotor_activation'],
            report['boundary_cost'], report['event_reserve'], report['exact_joint_margin']) == (
                1, 2, 1, 5, 0, 30, 18, 17)
    assert marked_counts(modules, range(8)) == {4: (True, True)}
    for point in [(14, 15), (16, 15), (14, 10), (16, 10)]:
        assert point in modules[7]['endpoints']
    kept = frozenset(range(1, 8))
    persistent = set.union(*(modules[index]['endpoints'] for index in kept))
    support = set.union(*(modules[index]['selected'] for index in kept))
    restored = support & (endpoints-persistent)
    visible = support-endpoints
    assert connected(persistent)
    assert marked_counts(modules, kept) == {4: (True, True)}
    expected_restored = {(row, column) for row in range(-length, 1, 2)
                         for column in (0, 7)} | {
                             (-length-1, 1), (-length-1, 6), (1, 0), (2, 0)}
    assert restored == expected_restored and len(restored) == length+6
    assert all(not set(neighbors(point)) & restored for point in visible)
    forced = {point for point in restored if len(set(neighbors(point)) & persistent) >= 2}
    assert forced == {(row, 7) for row in range(-length, 1, 2)}
    remaining = restored-forced
    edges = {tuple(sorted((point, other))) for point in remaining
             for other in set(neighbors(point)) & remaining}
    assert edges == {((0, 0), (1, 0)), ((1, 0), (2, 0))}
    omitted = forced | {(1, 0)}
    relaxed = (support-persistent)-omitted
    assert all(len(set(neighbors(point)) & (persistent | relaxed)) == 1 for point in relaxed)
    assert len(omitted) == length//2+2
    degree_excess = sum(len(set(neighbors(point)) & persistent)-1+
                        len(set(neighbors(point)) & restored) for point in restored)
    assert degree_excess == length//2+6
    clauses, occurrences = implications(modules)
    assert (2, 3, 0) in clauses and hull(clauses, kept) == frozenset(range(8))
    positive_block = frozenset(range(4, 8))
    assert hull(clauses, positive_block) == positive_block
    assert all((first_owner < 4 and second_owner < 4 and consumer < 4) or
               (first_owner >= 4 and second_owner >= 4 and consumer >= 4)
               for first_owner, second_owner, consumer in clauses)
    assert all(-length-8 <= row <= 27 and -2 <= column <= 17 for row, column in occupied)
    slack = (length+36)*10-len(network['matching'])-len(selected)
    assert slack == 11*length//2+238
    return dict(length=length, original_owners=8, endpoints=len(endpoints),
                matching=len(network['matching']), selected=len(selected),
                full_endpoint_connected=True, retained_endpoint_connected=True,
                positive=1, marked=2, activation=1, unused_u=5, rotor=0,
                boundary=30, reserve=18, allocation_margin=17, ambient_slack=slack,
                retained_endpoints=len(persistent), restored_supports=len(restored),
                forced_omissions=len(forced), minimum_omissions=len(omitted),
                degree_excess=degree_excess, refutes_pointwise_pool_payment=len(omitted) > 36,
                closure_of_cut=list(range(1, 9)), distinct_horn_rules=len(clauses),
                raw_conflict_occurrences=occurrences,
                positive_block_is_separately_closed=True)


def main():
    controls = [inspect(length) for length in (4, 6, 8, 10, 20, 40, 68, 70, 100, 200)]
    witness = next(row for row in controls if row['length'] == 70)
    assert witness['minimum_omissions'] == 37 and witness['ambient_slack'] == 623
    print(json.dumps(dict(status='PASS', witness=witness, controls=controls,
                         scope='Complete original-source and occupied-degree reconstruction, '
                         'independent exact reserve census, actual positive marks, full and '
                         'retained endpoint connectivity, and attaining minimum relaxed '
                         'omission certificate. General parameter proof is written separately. '
                         'This refutes pointwise source-cut payment even with positive demand '
                         'and connectivity, not full allocation, grid equality, or a theorem '
                         'restricted to demand-generated least marked hulls.'), indent=2))


if __name__ == '__main__':
    main()
