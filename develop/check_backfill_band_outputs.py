"""Independent source profiles and single-use occupied-band output controls."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cap_continuation_budget import phase_of
from check_cooperative_promotion import neighbors
from check_minus_one_tip_obstructions import source
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def band_sources(role, companion_width, companion_height, companion_far,
                 width, incident, far):
    companion = transform_module(source(companion_width, companion_height, companion_far),
                                 (True, False, False), (-1, -companion_height-1))
    current = transform_module(source(width, incident, far),
                               (True, role == 'B', False),
                               (0, -1 if role == 'B' else -incident-1))
    return companion, current


def profile_controls():
    counts = Counter()
    complete = []
    parameters = itertools.product(('B', 'D'), (6, 10, 18), (6, 8, 12, 20),
                                   (4, 10), (6, 8, 14), (4, 6, 10, 18), (4, 8, 16))
    for role, companion_width, companion_height, companion_far, width, incident, far in parameters:
        companion, current = band_sources(role, companion_width, companion_height,
                                          companion_far, width, incident, far)
        counts['source_pairs'] += 1
        if companion['endpoints'] & current['endpoints']:
            counts['original_endpoint_overlap'] += 1
            continue
        assert incident <= companion_height-2
        point, forced = (1, -incident-1), (1, -incident-2)
        north = (0, -incident-1)
        cells = set(itertools.product((0, 1), (-incident-2, -incident-1)))
        assert current['endpoints'] & cells == {point}
        assert current['selected'] & cells == ({north, forced} if role == 'B' else {north})
        assert phase_of(current) == ('00' if role == 'B' else '10')
        assert phase_of(companion) == '11'
        assert north in companion['endpoints']
        if incident == companion_height-2:
            assert companion['endpoints'] & cells == cells-{point}
            assert not companion['selected'] & cells
            counts[role+'_cap_profiles'] += 1
            network = combine([companion, current])
            occupied = network['endpoints'] | network['selected']
            if all(sum(adjacent in occupied for adjacent in neighbors(selected)) <= 1
                   for selected in network['selected']):
                assert len(network['endpoints']) == len(companion['endpoints'])+len(current['endpoints'])
                assert len(network['endpoints']) == 2*len(network['matching'])
                counts[role+'_complete_two_source_cap_bands'] += 1
                complete.append(dict(role=role, companion=[companion_width, companion_height, companion_far],
                                     output_owner=[width, incident, far]))
        else:
            assert incident <= companion_height-4
            pair = {(0, -incident-2), north}
            assert companion['endpoints'] & cells == pair
            assert companion['selected'] & cells == {forced}
            assert all(sum(adjacent in companion['endpoints'] for adjacent in neighbors(endpoint)) >= 2
                       for endpoint in pair)
            assert set(neighbors(forced)) & (pair | {point}) == {(0, -incident-2), point}
            counts[role+'_interior_profiles'] += 1
    assert all(counts[role+'_'+kind+'_profiles'] > 0 for role in ('B', 'D')
               for kind in ('cap', 'interior'))
    assert counts['B_complete_two_source_cap_bands'] > 0
    return dict(counts=counts, complete_band_examples=complete[:3],
                complete_critical_U10_events=0,
                scope='Endpoint-disjoint source-pair profiles are partial. Feasible two-source cap bands '
                      'are complete source fusions but contain no phase01 source or critical event. '
                      'No complete critical U10 or interior-output realization is supplied.')


def ledger_controls():
    counts = Counter()
    parameters = itertools.product(range(3), range(2), range(2), range(3), range(3), range(2))
    for negative_cap, irregular, old_regular, corner_events, negative_band, unused in parameters:
        for negative_second in range(corner_events+1):
            positive_second = corner_events-negative_second
            pool = negative_cap+irregular+old_regular+corner_events+negative_second+negative_band+unused
            if pool % 2:
                continue
            phase01, phase10 = pool//2, 0
            for positive_cap, unfilled in itertools.product(range(2), range(3)):
                cap = negative_cap+positive_cap+unfilled
                if cap % 2:
                    continue
                phase11 = cap//2
                delta = phase11-phase01-phase10
                for positive_band, extra, rotor, boundary in itertools.product(range(3), range(2),
                                                                              range(2), range(3)):
                    activation = positive_cap+positive_second+positive_band+extra
                    twice_reserve = activation+unfilled+rotor+boundary
                    if twice_reserve % 2:
                        continue
                    reserve = twice_reserve//2
                    retained = 2*delta+irregular+old_regular+2*corner_events+negative_band+positive_band
                    assert twice_reserve == retained+extra+rotor+boundary+unused
                    assert retained+rotor+boundary <= twice_reserve
                    assert 2*phase11+irregular+old_regular+2*corner_events+negative_band+positive_band <= (
                        2*phase01+2*phase10+activation+unfilled)
                    terminal = extra
                    positive_routes = positive_cap+positive_band
                    assert terminal+positive_second+positive_routes <= activation
                    activated_corner = activation
                    direct = boundary//2
                    unactivated_corner = 0
                    old_stops = boundary-direct
                    rotor_stops = rotor
                    counted = direct+unactivated_corner+activated_corner+terminal
                    assert counted+old_stops+rotor_stops+positive_cap+positive_second+positive_band+unfilled <= (
                        2*reserve+activation)
                    assert counted+old_stops+rotor_stops+retained+unused <= 2*reserve+activation
                    counts['simultaneous_ledger_instances'] += 1
                    if delta < 0:
                        counts['negative_source_census_instances'] += 1
    assert counts['negative_source_census_instances'] > 0
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = dict(status='PASS', source_profiles=profile_controls(), ledgers=ledger_controls(),
                  scope='Finite controls only. General occupied-band geometry, output injection/separation '
                        'and source-occurrence adapters have written proofs. Conditional arithmetic is '
                        'also formalized. FULL allocation and grid equality remain OPEN.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
