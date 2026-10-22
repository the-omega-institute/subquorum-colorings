"""Check both matchings, universal freeze transcripts and positive elbow grafts."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_rematching_receiver_flux import canonical, perfect_matchings
from check_residual_corridors import direct_check, transformed
from owned_corner_witnesses import physical_donors


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SELECTED = {(0, 1), (0, 3), (1, 0), (1, 5), (3, 6),
            (4, 0), (4, 5), (5, 1), (5, 3)}
FORCED = [((1, 1), (1, 2)), ((3, 5), (3, 4)), ((4, 1), (4, 2)),
          ((4, 3), (3, 3)), ((3, 2), (2, 2))]
SQUARE = [((1, 3), (1, 4)), ((2, 3), (2, 4))]


def fixture():
    return 6, 8, set(SELECTED), FORCED+SQUARE


def matching_orders():
    endpoints = endpoint_data(fixture())[0]
    records = []
    for matching in perfect_matchings(endpoints):
        frozen, layers = frozen_certificate((*fixture()[:3], list(matching)))
        assert frozen == endpoints
        records.append(dict(matching=matching, layers=layers))
    assert len(records) == 2
    return records


def graft(width, height, phase=(0, 0)):
    source = elbow(width, height)
    move = lambda point: (5-point[0], point[1])
    other_matching = [tuple(move(point) for point in edge) for edge in source[3]]
    other_endpoints = {point for edge in other_matching for point in edge}
    endpoints = endpoint_data(fixture())[0]
    assert not endpoints & other_endpoints
    contacts = {(point, other) for point in endpoints
                for other in set(neighbors(point)) & other_endpoints}
    assert contacts == {((1, 4), (1, 5))}
    other_selected = {move(point) for point in source[2]}
    assert SELECTED & other_endpoints == {(1, 5)}
    assert other_selected & endpoints == {(1, 4)}
    selected = (SELECTED | other_selected)-(endpoints | other_endpoints)
    offset = (height+2+phase[0], 2+phase[1])
    shift = lambda point: tuple(point[index]+offset[index] for index in range(2))
    rows = 2*((height+10)//2)
    columns = 2*((width+14)//2)
    current = (rows, columns, {shift(point) for point in selected},
               [tuple(shift(point) for point in edge)
                for edge in fixture()[3]+other_matching])
    return current


def inspect(current):
    direct_check(*current)
    endpoints = endpoint_data(current)[0]
    assert endpoint_components(current) == [endpoints]
    records = []
    for matching in perfect_matchings(endpoints):
        frozen, layers = frozen_certificate((*current[:3], list(matching)))
        assert frozen == endpoints
        assert all(layer for layer in layers)
        records.append(canonical(matching))
    assert len(records) == 2 and records[0] != records[1]
    return verify_terminal(current)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    base = fixture()
    base_ledger = inspect(base)
    assert base_ledger['objective'] == 16
    assert base_ledger['receivers'][0]['charge_twice'] == 0
    assert Counter(occupied_degrees(base).values()) == {3: 11, 4: 3}
    remaining = set(endpoint_data(base)[0])
    for leaf, partner in FORCED:
        assert set(neighbors(leaf)) & remaining == {partner}
        remaining.difference_update((leaf, partner))
    assert remaining == {(1, 3), (1, 4), (2, 3), (2, 4)}
    base_images = 0
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*base, *symmetry)
        inspect((*shape, selected, matching))
        base_images += 1
    graft_records = []
    phase_charges = {}
    for width in range(6, 23, 2):
        for height in range(4, 19, 2):
            for phase in itertools.product((0, 1), repeat=2):
                current = graft(width, height, phase)
                ledger = inspect(current)
                receiver = ledger['receivers'][0]
                assert len(current[2]) == height+11
                assert len(current[3]) == width+height+6
                assert receiver['endpoints'] == 2*width+2*height+12
                charge = receiver['charge_twice']//2
                phase_charges.setdefault(str(phase), set()).add(charge)
                if phase == (0, 0):
                    assert receiver['tiles'] == width//2+height+7
                    assert receiver['selected'] == height+9
                    assert charge == 1
                    donor = (height//2, 4)
                    donors = physical_donors(current, True)
                    assert any(tuple(record['tile']) == donor and record['deficit'] == 2
                               for record in donors)
                graft_records.append(dict(width=width, height=height, phase=phase,
                                          receiver=receiver))
    symmetry_grafts = 0
    for width, height in ((6, 4), (10, 8), (22, 18)):
        for symmetry in itertools.product((False, True), repeat=3):
            current = graft(width, height)
            shape, selected, matching = transformed(*current, *symmetry)
            ledger = inspect((*shape, selected, matching))
            assert ledger['receivers'][0]['charge_twice'] == 2
            symmetry_grafts += 1
    report = dict(status='PASS', base_shape=base[:2], base_selected=sorted(base[2]),
                  base_matching=base[3], forced_matching_order=FORCED,
                  base_ledger=base_ledger, both_matching_certificates=matching_orders(),
                  base_symmetry_controls=base_images, positive_family_parameters=72,
                  all_phase_graft_controls=len(graft_records),
                  phase_charges={key: sorted(value) for key, value in phase_charges.items()},
                  positive_graft_symmetry_controls=symmetry_grafts,
                  scope='Finite controls of the separate general forcing, freeze-transcript '
                        'and positive all-even-parameter graft proofs. No universal compensation '
                        'or coefficient improvement follows from the counterexample.',
                  graft_records=graft_records)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('graft_records', 'both_matching_certificates')}, indent=2))


if __name__ == '__main__':
    main()
