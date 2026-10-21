"""Full-source controls for the spacing-ten lower-rotor nonextension theorem."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_incident_eight_north_transfer import shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_ten_row_gate_compensation import baseline, candidate, checked_pairs
from check_wide_gate_escape_compensation import signature
from check_wide_gate_rotor_compensation import left_rotor, mirror


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def chart_controls():
    canonical = rotor_record((False, False, False))
    move = lambda point: (3+point[0], 5-point[1])
    transformed = ({move(point) for point in canonical[0]},
                   {move(point) for point in canonical[1]},
                   {tuple(sorted((move(first), move(second)))) for first, second in canonical[2]})
    assert transformed == left_rotor(False)
    assert (4, 4) in canonical[1] and move((4, 4)) == (7, 1)
    assert move((4, 3)) == (7, 2) and move((2, 4)) == (5, 1)
    return 1


def libraries():
    originals = [independent_source(size, symmetry, (0, 0))
                 for size, symmetry in itertools.product(
                     itertools.product((6, 8, 14, 40), (4, 6, 12, 40), (4, 6, 12, 40)),
                     itertools.product((False, True), repeat=3))]
    rotors = [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    return originals, rotors


def one_obstruction(width, top, extra, originals, rotors, reflected=False, offset=(0, 0)):
    old = baseline(width, 2, top, extra)
    records = [old[0], old[2], shift(left_rotor(False), (top, 0))]
    if reflected:
        records = [mirror(record, width) for record in records]
    records = [shift(record, offset) for record in records]
    gate = top+7+offset[0], (width if reflected else 1)+offset[1]
    endpoints = set.union(*(record[0] for record in records))
    assert len(endpoints) == sum(len(record[0]) for record in records)
    assert gate in records[-1][1] and gate not in endpoints
    assert set(neighbors(gate)) & endpoints == {(gate[0], gate[1]-1), (gate[0], gate[1]+1)}
    counts = [0, 0]
    normalized_rotors = set()
    for kind, library in enumerate((originals, rotors)):
        for original in library:
            for record in anchor_records(original, gate, {(-1, 0), (1, 0)}):
                assert record[0] & endpoints
                counts[kind] += 1
                if kind == 0:
                    rows = {row for row, column in record[0] if column == gate[1]}
                    assert max(rows)-min(rows) >= 4
                    assert set(range(min(rows), max(rows)+1)) <= rows
                    assert rows & {gate[0]-2, gate[0]+3}
                else:
                    assert {(gate[0]-2, gate[1]-1), (gate[0]+2, gate[1]-1)} & record[0] if not reflected else (
                        {(gate[0]-2, gate[1]+1), (gate[0]+2, gate[1]+1)} & record[0])
                    normalized_rotors.add(signature(shift(record, (-gate[0], -gate[1]))))
    assert len(normalized_rotors) == 4
    return counts


def obstruction_controls():
    originals, rotors = libraries()
    roles = [0, 0]
    cases = 0
    for width, top, extra, reflected, offset in itertools.product(
            (6, 8, 20, 100), (2, 40), (0, 20), (False, True), ((0, 0), (-100, -200))):
        counts = one_obstruction(width, top, extra, originals, rotors, reflected, offset)
        roles = [total+count for total, count in zip(roles, counts)]
        cases += 1
    large = one_obstruction(2000, 2000, 4000, originals, rotors)
    return dict(cases=cases, U_roles=roles[0], rotor_roles=roles[1],
                large_width_2000=dict(U_roles=large[0], rotor_roles=large[1]),
                without_earlier_inner_B=True, full_record_chart_controls=chart_controls())


def stronger_budget_controls():
    generator = random.Random(20261022)
    library = {}
    for width in (6, 8, 10, 12, 14, 20, 30):
        lower = {signature(left_rotor(False)), signature(mirror(left_rotor(False), width))}
        choices = [(records, gain) for records, gain in checked_pairs(width)
                   if not any(signature(record) in lower for record in records)]
        assert choices and min(gain for records, gain in choices) == 5
        library[width] = choices
    batches = sharp = 0
    for width, amount, top, offset in itertools.product(
            (6, 8, 12, 20), (2, 3, 6, 12), (2, 40), ((0, 0), (-100, -200))):
        old = [shift(record, offset) for record in baseline(width, amount, top)]
        before = inventory(old)
        assert phi_from(old, before) == 1-amount
        for trial in range(6):
            new, gains = [], []
            for index in range(amount-1):
                records, gain = generator.choice(library[width])
                new.extend(shift(record, (top+10*index+offset[0], offset[1])) for record in records)
                gains.append(gain)
            after = inventory(old+new)
            assert phi_from(old+new, after) == 1-amount+sum(gains) >= 4*(amount-1)
            batches += 1
        new = [shift(candidate('U', width), (top+10*index+offset[0], offset[1]))
               for index in range(amount-1)]
        after = inventory(old+new)
        assert phi_from(old+new, after) == 4*(amount-1)
        sharp += 1
    return dict(compatible_pairs_without_L={str(width): len(choices) for width, choices in library.items()},
                mixed_batches=batches, shared_spanning_partial_equality=sharp,
                equality_not_complete_extension_witness=True)


def spaced_baseline(width, bars):
    bottom = bars[-1]+4
    return [independent_source((width+2, bottom+20, bottom+40),
                               (False, False, False), (0, -1))]+[
        independent_source((width, 4, 4), (False, False, False), (bar, 0)) for bar in bars]


def nonuniform_spacing_controls():
    generator = random.Random(20261023)
    patterns = [gaps for amount in (1, 2, 3)
                for gaps in itertools.product((10, 12, 20), repeat=amount)]
    patterns += [(10, 12, 12, 12, 12)]
    patterns += [tuple(generator.choice((10, 12, 20)) for index in range(8)) for trial in range(12)]
    cases = neutral = density = 0
    for width, top, offset, gaps in itertools.product(
            (6, 8, 12, 20), (2, 40), ((0, 0), (-100, -200)), patterns):
        bars = [top]
        for gap in gaps:
            bars.append(bars[-1]+gap)
        old = spaced_baseline(width, bars)
        old = [shift(record, offset) for record in old]
        assert phi_from(old, inventory(old)) == -len(gaps)
        new = [shift(candidate('U', width), (bars[index]+offset[0], offset[1]))
               for index, gap in enumerate(gaps) if gap == 10]
        after = inventory(old+new)
        selected = gaps.count(10)
        value = phi_from(old+new, after)
        assert value == 5*selected-len(gaps)
        if 5*selected >= len(gaps):
            assert value >= 0
            density += 1
        neutral += value == 0
        cases += 1
    return dict(cases=cases, density_criterion_cases=density, exact_neutral=neutral,
                note='Spanning U shared owners attain5m-(n-1) as partial inventories; '
                     'no complete-extension or full-family equality claim.')


def residual_gap_twelve_controls():
    results = []
    for width, top, extra_sources in itertools.product((6, 20), (2, 40), (0, 1, 4, 5, 20, 40)):
        bars = [top]+[top+10+12*index for index in range(extra_sources+1)]
        old = spaced_baseline(width, bars)
        new = shift(candidate('U', width), (top, 0))
        assert phi_from(old, inventory(old)) == -extra_sources-1
        exact = phi_from(old+[new], inventory(old+[new]))
        assert exact == 4-extra_sources
        results.append(dict(width=width, top=top, wider_gaps=extra_sources, Phi=exact))
    return dict(cases=len(results), examples=results,
                refutes='Arbitrary endpoint-disjoint extension monotonicity/nonnegativity of the compensated core.',
                does_not_refute='Complete-family target; no complete-extension witness is asserted.')


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', obstruction=obstruction_controls(),
                         stronger_selected_budget=stronger_budget_controls(),
                         nonuniform_spacing=nonuniform_spacing_controls(),
                         residual_gap_twelve=residual_gap_twelve_controls(),
                         scope='Finite full-record controls of the written arbitrary-dimension '
                               'three-original nonextension theorem and stronger selected budget. '
                               'No complete-family existence, arbitrary-old monotonicity or global target.'), indent=2))
