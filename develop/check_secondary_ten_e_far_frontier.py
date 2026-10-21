"""Exact old-chain collisions and receipt sets for arbitrary internal E far legs."""

import itertools
import json
from collections import Counter

from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def frontier(sites, index, column, terminal):
    contact = next((later for later in range(index+1, len(sites))
                    if column >= sites[later][2]-4), None)
    if contact is None:
        return True, 'outside', 0, None
    anchor, unused, lateral = sites[contact]
    assert lateral-4 <= column <= sites[contact-1][2]-6
    if column == lateral-4:
        return terminal <= anchor-3, 'X', 0, contact
    if column == lateral-2:
        return terminal <= anchor-3, 'Z', int(terminal == anchor-3), contact
    if column == lateral:
        return terminal <= anchor-5, 'P_far', 2*int(terminal in (anchor-7, anchor-5)), contact
    assert column >= lateral+2
    return terminal <= anchor-9, 'P_bar', int(terminal == anchor-9), contact


def receipts(sites, index, count, column, terminal, phase, deduction, contact, new_owner):
    anchor, unused, lateral = sites[index]
    near_column = sites[index-1][2]+1
    near_owner = 9*count+1+index
    full = {((anchor-7+2*step)//2, (near_column-1)//2) for step in range(4)}
    events = {(owner, source, target) for row in range(anchor-7, anchor, 2)
              for owner, source, target in (
                  (new_owner, (row, near_column), (row, near_column-1)),
                  (near_owner, (row, near_column-1), (row, near_column)))}
    if not deduction:
        return full, events
    other_anchor, unused, unused = sites[contact]
    if phase == 'Z':
        other_owner = 10*count+1+contact
        full.add((terminal//2, column//2))
        events |= {(new_owner, (terminal, column), (terminal, column+1)),
                   (other_owner, (terminal, column+1), (terminal, column)),
                   (other_owner, (terminal+1, column), (terminal, column))}
    elif phase == 'P_far':
        other_owner = 9*count+1+contact
        overlap = (terminal-other_anchor+7)//2
        assert overlap in (0, 1)
        if overlap:
            full.add(((other_anchor-7)//2, column//2))
        events |= {(owner, source, target)
                   for row in range(other_anchor-7, terminal+1, 2)
                   for owner, source, target in (
                       (new_owner, (row, column), (row, column+1)),
                       (other_owner, (row, column+1), (row, column)))}
    else:
        assert phase == 'P_bar'
        events.add((9*count+1+contact, (terminal+1, column), (terminal, column)))
    return full, events


def check_chain(origin, offset, widths, depths, indices=None):
    fixed, unused, unused, sites = old_chain(origin, offset, widths, depths, 6)
    blocked = set.union(*(record[0] for record in fixed))
    before = inventory(fixed)
    controls = surviving = 0
    phases = Counter()
    minimum = None
    indices = range(1, len(widths)) if indices is None else indices
    for index in indices:
        anchor, unused, lateral = sites[index]
        near_column = lateral+widths[index]+13
        fars = {4, 6, 8, 20, 80, 200, 2000}
        far_columns = {lateral-6, lateral-8, sites[-1][2]-20}
        for later in range(index+1, len(widths)):
            fars |= {sites[later][0]-anchor+step for step in range(-2, 16, 2)}
            far_columns |= {sites[later][2]+step for step in range(-8, 12, 2)}
        for column, far in itertools.product(sorted(far_columns), sorted(fars)):
            breadth = near_column+1-column
            if breadth < widths[index]+20 or far < 4:
                continue
            candidate = north_U(anchor+3, near_column, breadth, 10, far, True)
            terminal = anchor-11+far
            allowed, phase, deduction, contact = frontier(sites, index, column, terminal)
            assert allowed == (not bool(candidate[0] & blocked))
            controls += 1
            if not allowed:
                continue
            after = inventory(fixed+[candidate])
            full, events = receipts(sites, index, len(widths), column, terminal,
                                    phase, deduction, contact, len(fixed))
            assert after['full']-before['full'] == full
            assert after['events']-before['events'] == events
            assert before['full'] <= after['full'] and before['events'] <= after['events']
            assert after['mass']-before['mass'] == 1
            gain = phi_from(fixed+[candidate], after)-phi_from(fixed, before)
            assert gain == 1-deduction >= -1
            minimum = gain if minimum is None else min(minimum, gain)
            surviving += 1
            phases[f'{phase}:deduction{deduction}'] += 1
    return dict(blocks=len(widths), collision_controls=controls,
                exact_full_and_event_set_controls=surviving, minimum_gain=minimum,
                phases=dict(sorted(phases.items())))


def sharp_witness():
    fixed, unused, unused, sites = old_chain(31, 0, [12]*3, [24]*3, 6)
    receiver = north_U(52, 1, 50, 10, 22, True)
    before, after = inventory(fixed), inventory(fixed+[receiver])
    gain = phi_from(fixed+[receiver], after)-phi_from(fixed, before)
    assert gain == -1
    return dict(origin=31, offset=0, widths=[12]*3, depths=[24]*3,
                index=1, receiver_dimensions=[50, 10, 22],
                receiver_chart_origin=[38, 2], far_column=-48, terminal_row=60,
                new_full=len(after['full']-before['full']),
                new_events=len(after['events']-before['events']), exact_gain=gain,
                complete_extendibility='not asserted')


def main():
    cases = [check_chain(origin, offset, [12, 14, 20, 18, 12, 30],
                         [24, 26, 40, 24, 80, 24])
             for origin, offset in ((31, 0), (-33, -100))]
    cases.append(check_chain(31, 200, [12+2*(index % 5) for index in range(12)],
                             [24+2*(index % 7) for index in range(12)], (1, 6, 11)))
    assert min(case['minimum_gain'] for case in cases) == -1
    print(json.dumps(dict(status='PASS', cases=cases, sharp_local_witness=sharp_witness(),
        scope='Exact OLD H3 frontier and full receipt SETS for one arbitrary-far '
              'internal E incident-ten original. General geometric proof is written. '
              'No arbitrary-both-far simultaneous theorem or complete-extension claim.'), indent=2))


if __name__ == '__main__':
    main()
