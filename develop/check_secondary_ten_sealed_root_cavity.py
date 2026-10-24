"""Full-original controls for sealed root cavities and complete-prefix compensation."""

from collections import deque
import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_secondary_ten_root_fourth_consumer import originals
from check_secondary_ten_root_sharp_staircase import check_case, sharp_dimensions
from check_secondary_ten_root_support_staircase import horizontal
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def connected(points):
    start = next(iter(points))
    reached, queue = {start}, deque([start])
    while queue:
        point = queue.popleft()
        for adjacent in set(neighbors(point)) & points-reached:
            reached.add(adjacent)
            queue.append(adjacent)
    return reached == points


def projection_controls():
    original_count = rotor_count = 0
    for breadth, near, far, symmetry in itertools.product(
            (6, 14, 100), (4, 8, 100), (4, 10, 100),
            itertools.product((False, True), repeat=3)):
        points = independent_source((breadth, near, far), symmetry, (31, -100))[0]
        assert connected(points)
        assert max(column for row, column in points)-min(column for row, column in points)+1 >= 5
        original_count += 1
    for symmetry in itertools.product((False, True), repeat=3):
        points = transform_module(rotor(), symmetry, (31, -100))['endpoints']
        assert connected(points)
        assert max(column for row, column in points)-min(column for row, column in points)+1 == 4
        rotor_count += 1
    return dict(full_U_orientation_controls=original_count, rotor_orientation_controls=rotor_count)


def cavity_case(origin, offset, widths, depths, breadth, reduction,
                root_breadth=6, receiver_far=4):
    old_width, width, depth = widths[0], widths[1], depths[0]
    dimensions = sharp_dimensions(old_width, width, depth, breadth)
    dimensions[3][1] -= reduction
    dimensions[3][2] -= reduction
    result = check_case(origin, offset, widths, depths, breadth, 6, dimensions,
                        receiver_far, root_breadth, root_breadth+2)
    fixed, additions, sites = originals(origin, offset, widths, depths, root_breadth,
                                        root_breadth+2, receiver_far, breadth, 6)
    stairs = [horizontal(origin, offset, old_width, index, *parameters)
              for index, parameters in enumerate(dimensions)]
    occupied = set.union(*(source[0] for source in fixed+additions+stairs))
    near_column = offset-width-12
    right_column = offset+old_width+12-dimensions[3][1]
    top, bottom = origin-12, origin+depth-15
    rectangle = {(row, column) for row in range(top, bottom+1)
                 for column in range(near_column+1, right_column)}
    left_wall = {(row, near_column) for row in range(top, bottom+1)}
    right_wall = {(row, right_column) for row in range(top, bottom+1)}
    upper_wall = {(top-1, column) for column in range(near_column+1, right_column)}
    lower_wall = {(bottom+1, column) for column in range(near_column+1, right_column)}
    assert left_wall | upper_wall <= additions[0][0]
    assert right_wall <= stairs[3][0]
    assert lower_wall <= fixed[9*len(widths)+2][0]
    assert not rectangle & occupied
    boundary = set.union(*(set(neighbors(point))-rectangle for point in rectangle))
    assert boundary == left_wall | right_wall | upper_wall | lower_wall
    assert boundary <= occupied
    point = bottom, near_column+1
    assert point in rectangle & additions[0][1]
    assert point not in occupied
    assert {(bottom, near_column), (bottom+1, near_column+1)} <= set(neighbors(point)) & occupied
    reached, queue = {point}, deque([point])
    while queue:
        current = queue.popleft()
        for adjacent in set(neighbors(current))-occupied-reached:
            reached.add(adjacent)
            queue.append(adjacent)
            assert adjacent in rectangle
    assert reached == rectangle
    free_width = right_column-near_column-1
    assert free_width == old_width+width+23-dimensions[3][1] == reduction+1
    assert len(rectangle) == (depth-2)*free_width
    result.update(cavity_width=free_width, cavity_size=len(rectangle), mandatory_site=point,
                  narrow_cavity_excludes_complete_extension=free_width <= 3)
    if reduction <= 2:
        assert dimensions[3][1] >= old_width+width+20
    else:
        assert dimensions[3][1] <= old_width+width+18
        assert result['joint_gain'] >= breadth//2+7 >= 10
    assert result['joint_gain'] == breadth//2+3+reduction
    return result


def case_budget(result, origin, widths, depths, breadth, dimensions):
    old_width, width, depth = widths[0], widths[1], depths[0]
    bottom = origin+depth-15
    first_bottom = origin-11+dimensions[1][0] == bottom
    third_bottom = origin-13+dimensions[3][0] == bottom
    if third_bottom and dimensions[3][1] > old_width+width+18:
        return 'excluded_narrow_cavity'
    if third_bottom:
        assert result['joint_gain'] >= old_width+width+breadth//2+25-dimensions[3][1]
        branch = 'third_bottom'
    elif first_bottom:
        assert result['staircase_pair_receipt'] == result['old_A_events'] == 0
        assert dimensions[1][1]+8 <= dimensions[3][1]
        assert result['bottom_far_total_length'] <= dimensions[1][1]-old_width-12
        assert result['joint_gain'] >= breadth//2+9 >= 12
        branch = 'first_bottom'
    else:
        assert result['bottom_far_intervals'] == 0
        assert result['far_budget'] >= -3
        assert result['joint_gain'] >= width//2+breadth//2+8
        branch = 'no_bottom'
    assert result['joint_gain'] >= breadth//2+7 >= 10
    return branch


def cavity_controls():
    cases = []
    for origin, offset, old_width, width, depth, reduction in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80), (0, 2, 4)):
        for breadth in sorted({6, width-reduction}):
            count = 2 if len(cases) % 2 else 5
            cases.append(cavity_case(origin, offset, [old_width, width]+[12]*(count-2),
                                     [depth]+[24]*(count-1), breadth, reduction,
                                     root_breadth=40, receiver_far=2000))
    return cases


def width_three_boundary_control():
    dimensions = sharp_dimensions(12, 12, 24, 12)
    dimensions[3][1] -= 2
    dimensions[3][2] -= 2
    second = horizontal(31, 0, 12, 2, *dimensions[2])
    third = horizontal(31, 0, 12, 3, *dimensions[3])
    collision = (20, -20)
    assert dimensions[2][1] == dimensions[3][1] == 44
    assert collision in second[0] & third[0]
    return dict(excluded_unrestricted_boundary='L=v', collision=collision,
                admissible_width_three_range='6<=L<=v-2')


if __name__ == '__main__':
    projections = projection_controls()
    cavities = cavity_controls()
    first_dimensions = [[6, 44, 4], [20, 46, 22], [6, 52, 4], [8, 54, 4]]
    first = check_case(31, 0, [12, 20], [24, 24], 6, 4, first_dimensions)
    assert case_budget(first, 31, [12, 20], [24, 24], 6, first_dimensions) == 'first_bottom'
    no_dimensions = [[6, 34, 4], [8, 36, 6], [10, 38, 4], [12, 46, 16]]
    no_bottom = check_case(31, 0, [12, 12], [24, 24], 6, 8, no_dimensions)
    assert case_budget(no_bottom, 31, [12, 12], [24, 24], 6, no_dimensions) == 'no_bottom'
    width_five = cavity_case(31, 0, [12, 12], [24, 24], 6, 4)
    assert case_budget(width_five, 31, [12, 12], [24, 24], 6, width_five['dimensions']) == 'third_bottom'
    long_control = cavity_case(-33, 200, [12]*24, [24]*24, 6, 0,
                               root_breadth=40, receiver_far=2000)
    print(json.dumps(dict(status='PASS', projection_controls=projections,
        exact_cavity_controls=len(cavities),
        width_three_boundary=width_three_boundary_control(),
        excluded_width_one=sum(case['cavity_width'] == 1 for case in cavities),
        excluded_width_three=sum(case['cavity_width'] == 3 for case in cavities),
        width_five_controls=sum(case['cavity_width'] == 5 for case in cavities),
        first_bottom_control=first, no_bottom_control=no_bottom,
        width_five_control=width_five, long_chain_control=long_control,
        scope='Exact wall, support, component and inherited receipt controls for a separate '
              'general proof. Width1/3 cavities exclude complete extensions, not merely '
              'a proposed consumer rule. Width5 and the conditional >=10 ledger do not '
              'assert complete extendibility or global allocation.'), indent=2))
