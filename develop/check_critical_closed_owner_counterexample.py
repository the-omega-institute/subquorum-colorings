"""Complete six-source obstruction to critical closed-owner exclusion."""

import argparse
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_closed_neutral_receivers import closed_contacts
from check_component_receivers import vertices_of
from check_exact_event_reserve import inspect_exact
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_neutral_support_injection import inspect_joint
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SPECIFICATIONS = [
    ((26, 12, 4), (False, False, False), (0, 1)),
    ((10, 4, 4), (True, False, False), (1, 3)),
    ((6, 4, 4), (True, True, False), (11, 7)),
    ((6, 4, 4), (False, True, False), (8, 8)),
    ((8, 6, 6), (False, False, False), (2, 7)),
    ((10, 4, 4), (True, True, False), (1, 20)),
]


def neighbors(point):
    row, column = point
    return {(row-1, column), (row+1, column),
            (row, column-1), (row, column+1)}


def canonical(parameters):
    width, left, right = parameters
    matching = [((0, 1+2*index), (0, 2+2*index)) for index in range(width//2)]
    matching += [((1, 2+2*index), (1, 3+2*index)) for index in range(width//2-1)]
    matching += [((1+2*index, 1), (2+2*index, 1)) for index in range(left//2)]
    matching += [((1+2*index, width), (2+2*index, width))
                 for index in range(right//2)]
    supports = {(0, 0), (0, width+1), (left+1, 1), (right+1, width)}
    supports.update((row, 0 if row % 2 == 0 else 2) for row in range(2, left+1))
    supports.update((row, width+1 if row % 2 == 0 else width-1)
                    for row in range(2, right+1))
    return matching, supports


def modules():
    result = []
    for parameters, symmetry, offset in SPECIFICATIONS:
        module = transform_module(source(*parameters), symmetry, offset)
        matching, supports = canonical(parameters)
        expected_edges = {frozenset(affine(point, symmetry, offset) for point in edge)
                          for edge in matching}
        assert expected_edges == {frozenset(edge) for edge in module['matching']}
        assert module['selected'] == {affine(point, symmetry, offset) for point in supports}
        result.append(module)
    return result


def verify(current, originals, move=lambda point: point):
    rows, columns, selected, matching = current
    endpoints = [point for edge in matching for point in edge]
    assert len(endpoints) == len(set(endpoints)) == 180
    endpoints = set(endpoints)
    assert len(matching) == 90 and len(selected) == 38
    assert not selected & endpoints
    assert all(0 <= row < rows and 0 <= column < columns
               for row, column in endpoints | selected)
    assert all(second in neighbors(first) for first, second in matching)
    assert all(len(neighbors(point) & (endpoints | selected)) <= 1 for point in selected)
    original_supports = set.union(*(module['selected'] for module in originals))
    assert selected == original_supports-endpoints
    assert [phase_of(module) for module in originals] == ['01', '11', '01', '10', '01', '11']
    assert [module['charge'] for module in originals] == [-1, -9, -1, -5, -1, -9]

    def profile(origin):
        cells = vertices_of({tile_of(move(origin))})
        return len(cells & endpoints), len(cells & selected)

    assert profile((12, 2)) == (2, 1)
    assert move((12, 2)) in originals[0]['endpoints']
    assert move((12, 3)) in originals[2]['endpoints']
    assert move((11, 3)) in originals[0]['selected'] & originals[2]['selected']
    assert move((11, 3)) in originals[1]['endpoints']
    assert profile((10, 2)) == (4, 0)
    assert move((2, 8)) in originals[1]['selected'] & originals[4]['endpoints']
    assert move((1, 8)) in originals[0]['endpoints']
    assert profile((2, 8)) == (4, 0)
    assert vertices_of({tile_of(move((2, 8)))}) <= originals[4]['endpoints']

    data, closed, contacts, edges, components = closed_contacts(originals)
    assert closed == {3, 4} and components == 1 and not edges
    assert data[4]['phase'] == '01' and data[3]['phase'] == '10'
    assert {port['point'] for port in data[4]['ports']} == {move((8, 8)), move((8, 15))}
    assert {port['point'] for port in data[3]['ports']} == {move((8, 9)), move((8, 14))}
    assert all(contacts[contacts[owner, index]] == (owner, index)
               for owner in closed for index in (0, 1))
    assert all(contacts[owner, index][0] == 7-owner
               for owner in closed for index in (0, 1))
    assert profile((8, 8)) == profile((8, 14)) == (2, 1)
    critical = move((2, 8))
    assert critical not in {port['point'] for port in data[4]['ports']}
    assert critical in set.union(*(originals[owner]['endpoints'] for owner in closed
                                  if data[owner]['phase'] == '01'))
    exact = inspect_exact(current, originals)
    assert exact == dict(positive=0, marked=0, activated_positive=0,
                         unused_u_triples=4, unpaired_rotor_activation=0,
                         lone_irregular=2, sole_irregular_pair=15,
                         mutual_non_event=0, mixed_three=0, boundary_cost=32,
                         event_reserve=18, exact_joint_margin=18)
    joint = inspect_joint(current, originals)
    return dict(shape=[rows, columns], matching_edges=len(matching), endpoints=len(endpoints),
                retained_supports=len(selected), objective=len(matching)+len(selected),
                half_area=rows*columns//2, slack=rows*columns//2-len(matching)-len(selected),
                phases=[phase_of(module) for module in originals],
                source_charges=[module['charge'] for module in originals],
                closed_owners=sorted(closed), closed_components=components,
                critical_point=critical, exact_census=exact, joint_control=joint)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    originals = modules()
    network = combine(originals)
    fixed = verify((20, 30, network['selected'], network['matching']), originals)
    images = []
    for symmetry in itertools.product((False, True), repeat=3):
        transpose, flip_row, flip_column = symmetry
        parity = ((int(flip_column), int(flip_row)) if transpose
                  else (int(flip_row), int(flip_column)))
        transformed = [transform_module(module, symmetry, parity) for module in originals]
        current, transformed = contained(transformed)
        anchor = next(iter(originals[0]['endpoints']))
        moved_anchor = next(point for point in transformed[0]['endpoints']
                            if point == min(transformed[0]['endpoints']))
        raw_min = min(affine(point, symmetry, parity) for point in originals[0]['endpoints'])
        shift = tuple(value-other for value, other in zip(moved_anchor, raw_min))
        total_offset = tuple(value+other for value, other in zip(parity, shift))
        move = lambda point: affine(point, symmetry, total_offset)
        assert move(anchor) in transformed[0]['endpoints']
        record = verify(current, transformed, move)
        record.update(symmetry=symmetry, offset=total_offset)
        images.append(record)
    result = dict(status='PASS', specifications=SPECIFICATIONS, fixed=fixed,
                  partition_preserving_images=images,
                  refuted_rule='Every critical second point avoids all closed phase01 original owners.',
                  target_inequality_refuted=False,
                  scope='One complete six-source critical witness and its eight partition-preserving images. '
                        'Not AA, no closed01-closed01 contact, no long-second event. '
                        'Does not establish overlap with the other extra corner of a first/long receiver.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], fixed=fixed, images=len(images))))


if __name__ == '__main__':
    main()
