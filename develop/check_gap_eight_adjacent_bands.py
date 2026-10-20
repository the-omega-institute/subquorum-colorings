"""Coordinate controls for the conditional gap-eight east-terminal branch."""

from collections import Counter
import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def source(dimensions, symmetry, offset):
    endpoints, supports, matching = independent_source(dimensions, symmetry, offset)
    assert len(endpoints) == 2*len(matching)
    assert {point for edge in matching for point in edge} == endpoints
    assert not endpoints & supports
    return endpoints, supports


def east_role_controls():
    counts = Counter()
    for height, width, far, breadth, leg, other, upward in itertools.product(
            (12, 18, 26), (8, 18, 26), (4, 8), (6, 10, 16),
            (4, 6, 8, 12), (4, 8), (False, True)):
        cross, _ = source((width, height, far), (True, True, False), (1, height+2))
        offset = (4 if upward else 2, height-4+leg)
        east, _ = source((breadth, leg, other), (True, True, upward), offset)
        point = (3, height-4)
        assert point in east
        assert set(neighbors(point)) & east == {(3, height-3)}
        counts['anchored_east_terminal_roles'] += 1
        if not cross & east:
            assert leg == 4 and not upward
            assert breadth <= width-2
            counts['surviving_incident_four_downward_roles'] += 1
    assert counts['surviving_incident_four_downward_roles'] > 0
    return dict(counts)


def band_controls():
    counts = Counter()
    examples = {}
    for height, width, far, breadth, other in itertools.product(
            (12, 18, 26), (8, 12, 18, 26), (4, 6, 8, 12, 20),
            (6, 8, 10, 16, 24), (4, 6, 8, 12, 20)):
        cross, cross_support = source(
            (width, height, far), (True, True, False), (1, height+2))
        east, east_support = source(
            (breadth, 4, other), (True, True, False), (2, height))
        if cross & east:
            continue
        assert breadth <= width-2
        endpoints = cross | east
        cap = (breadth+3, height)
        assert cap in east_support
        assert {(breadth+2, height), (breadth+3, height+1)} <= endpoints
        if breadth <= width-4:
            branch = 'unsaturated_bar_end_exit'
            point, supports = cap, east_support
        else:
            assert breadth == width-2 and cap in cross
            if far >= other+4:
                branch = 'saturated_east_far_exit'
                point, supports = (width, height-other-1), east_support
            elif far <= other:
                branch = 'saturated_cross_far_exit'
                point, supports = (width+1, height+1-far), cross_support
            else:
                assert far == other+2
                branch = 'saturated_matched_return_PARTIAL'
                point, supports = None, None
                east_terminal = (width, height-other)
                cross_terminal = (width+1, height-other)
                assert east_terminal in east
                assert cross_terminal in cross & east_support
                forced_pair = ((width, height-other-1), (width+1, height+1-far))
                assert forced_pair[0] in east_support
                assert forced_pair[1] in cross_support
                for support in forced_pair:
                    assert support in cross_support | east_support
                    assert support not in endpoints
                    assert len(set(neighbors(support)) & endpoints) == 1
                occupied = endpoints | set(forced_pair)
                for consumed in itertools.product((False, True), repeat=2):
                    feasible = all(consumed[index] or
                                   len(set(neighbors(support)) & occupied) == 1
                                   for index, support in enumerate(forced_pair))
                    assert feasible == all(consumed)
        if point is not None:
            assert point in supports and point not in endpoints
            assert len(set(neighbors(point)) & endpoints) >= 2
        counts[branch] += 1
        examples.setdefault(branch, dict(height=height, cross_width=width,
                                        cross_far=far, east_width=breadth, east_far=other))
    assert len(counts) == 4
    return dict(counts=dict(counts), examples=examples)


if __name__ == '__main__':
    print(json.dumps(dict(
        status='PASS', east_roles=east_role_controls(), bands=band_controls(),
        scope='Finite endpoint/support/matching controls for the direct written propagation lemma. '
              'PARTIAL configurations only; no complete extension, new reserve, activation injection, '
              'Lean verification or universal allocation conclusion.'), indent=2))
