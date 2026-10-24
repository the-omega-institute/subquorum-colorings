"""Exact full-original controls for arbitrary left consumers across old blocks."""

import itertools
import json
from collections import Counter

from check_secondary_ten_arbitrary_t_consumers import expected_local, north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def frontier(sites, index, breadth, depth, far):
    origin, east, offset = sites[index]
    column = offset+1-breadth
    terminal = origin-4-depth+far
    contact = next((other for other in range(index+1, len(sites))
                    if column >= sites[other][2]-3), None)
    if contact is None:
        return True, 'outside', 0, None
    other_origin, other_east, other_offset = sites[contact]
    assert other_offset-3 <= column <= sites[contact-1][2]-5
    if column == other_offset-3:
        return terminal <= other_origin, 'X', int(terminal >= other_origin-2), contact
    if column == other_offset-1:
        return terminal <= other_origin-6, 'Z_west', 0, contact
    assert other_offset+1 <= column
    return terminal <= other_origin-10, 'P', 0, contact


def check_chain(origin, offset, widths, depths, indices=None):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, 10)
    blocked = set.union(*(record[0] for record in fixed))
    before = inventory(fixed)
    before_phi = phi_from(fixed, before)
    count = len(widths)
    controls = surviving = exact_sets = 0
    minimum = None
    phases = Counter()
    activations = Counter()
    indices = range(count) if indices is None else indices
    for index in indices:
        current_origin, east, current_offset = sites[index]
        breadths = {6, 8, 12, current_offset-sites[-1][2]+6}
        for later in range(index+1, count):
            later_origin, later_east, later_offset = sites[later]
            breadths |= {current_offset-later_offset+step for step in (-6, -2, 0, 2, 4, 6)}
        breadths = sorted(breadth for breadth in breadths if breadth >= 6)
        for breadth, depth in itertools.product(breadths, (4, 8, 80)):
            fars = {4, 8, 100}
            for later in range(index+1, count):
                fars |= {sites[later][0]-current_origin+4+depth+step
                         for step in (-12, -10, -8, -6, -4, -2, 0, 2, 4)}
            for far in sorted(far for far in fars if far >= 4):
                candidate = north_U(current_origin, current_offset, breadth, depth, far, True)
                allowed, phase, delta, contact = frontier(sites, index, breadth, depth, far)
                assert allowed == (not bool(candidate[0] & blocked)), (
                    index, breadth, depth, far, phase, contact,
                    sorted(candidate[0] & blocked)[:8], sites)
                controls += 1
                if not allowed:
                    continue
                after = inventory(fixed+[candidate])
                near_full, near_events = expected_local(current_origin, current_offset,
                    widths[index], breadth, depth, far, True, 9*count+1+index, len(fixed))
                extra_full = set()
                extra_events = set()
                if delta:
                    other_origin, other_east, other_offset = sites[contact]
                    terminal = current_origin-4-depth+far
                    overlap = (terminal-other_origin+2)//2
                    assert overlap in (0, 1)
                    old_owner = 11*count+1+contact
                    new_owner = len(fixed)
                    if overlap:
                        extra_full.add(((other_origin-1)//2, (other_offset-4)//2))
                        extra_events.add((new_owner, (other_origin-1, other_offset-3),
                                          (other_origin-1, other_offset-4)))
                    extra_events |= {(old_owner, (other_origin-2+2*step, other_offset-4),
                                      (other_origin-2+2*step, other_offset-3))
                                     for step in range(overlap+1)}
                    assert breadth == current_offset-other_offset+4 >= 28
                    activations[overlap] += 1
                assert not near_full & extra_full and not near_events & extra_events
                assert after['full']-before['full'] == near_full | extra_full
                assert after['events']-before['events'] == near_events | extra_events
                assert before['full'] <= after['full'] and before['events'] <= after['events']
                gain = phi_from(fixed+[candidate], after)-before_phi
                assert gain == breadth-1-delta >= 5
                assert (gain == 5) == (breadth == 6)
                surviving += 1
                exact_sets += 1
                minimum = gain if minimum is None else min(minimum, gain)
                phases[phase] += 1
    return dict(blocks=count, collision_classification_controls=controls,
                surviving=surviving, exact_set_controls=exact_sets, minimum_gain=minimum,
                legal_phases=dict(phases), X_activation_cases=dict(activations))


def main():
    cases = [check_chain(origin, offset, [12+2*(index % 3) for index in range(count)],
                         [24+2*(index % 4) for index in range(count)])
             for origin, offset, count in ((31, 0, 1), (31, 0, 2), (-33, -100, 4), (31, 200, 7))]
    cases.append(check_chain(31, 0, [12]*24, [24]*24, (0, 12, 23)))
    print(json.dumps(dict(status='PASS', cases=cases,
        scope='Full ORIGINAL source collision and exact physical tile/directed event SET '
              'controls for a written all-parameter ONE-consumer theorem. '
              'No simultaneous arbitrary-consumer, complete-extension or global bound claim.'), indent=2))


if __name__ == '__main__':
    main()
