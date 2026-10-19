"""All small capacity/reservation vectors and a corrected frozen-donor batch."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_low_charge_rank_barrier import array_records
from check_component_strip_certificates import independent_selected_case
from check_component_receivers import verify_terminal
from check_residual_corridors import transformed
from check_two_leg_corner_obstruction import inspect, saturated_endpoint_donors, two_leg_case
from component_strip_certificates import certify_reservation_batch
from sealed_strip_allocation import maximal_strips


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def abstract_controls():
    tiles, records = array_records(2, 3)
    counts = Counter()
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        before = dict(zip(tiles, capacities))
        for after_values in itertools.product(*(range(capacity+1) for capacity in capacities)):
            after = dict(zip(tiles, after_values))
            report = certify_reservation_batch(records, before, after)
            counts['transitions'] += 1
            counts['sufficient'] += report['sufficient_condition']
            counts['componentwise_sufficient'] += report['componentwise_sufficient_condition']
            counts['strict_cross_component_improvement'] += (
                report['sufficient_condition'] and not report['componentwise_sufficient_condition'])
            counts['decreases'] += report['score_change'] < 0
            counts['sufficient_with_decrease'] += (report['sufficient_condition']
                                                  and report['score_change'] < 0)
            counts['uncertified_but_nondecreasing'] += (not report['sufficient_condition']
                                                       and report['score_change'] >= 0)
            changed = [tile for tile in tiles if before[tile] != after[tile]]
            if len(changed) == 1 and before[changed[0]]-after[changed[0]] == 2:
                assert report['sufficient_condition'] and report['score_change'] >= 0
                counts['parallel_pair_batches'] += 1
    assert counts['transitions'] == 6**6
    assert counts['sufficient_with_decrease'] == 0
    assert counts['decreases'] > 0 and counts['uncertified_but_nondecreasing'] > 0
    return dict(counts)


def cross_component_controls():
    _, records = array_records(3, 5)
    before = {(row, column): 0 for row in range(3) for column in range(5)}
    before.update({(0, 0): 2, (0, 1): 2, (0, 2): 2,
                   (1, 3): 1, (1, 4): 2, (2, 3): 2, (2, 4): 2})
    after = dict(before)
    after[(0, 0)] -= 1
    after[(1, 3)] -= 1
    positive = certify_reservation_batch(records, before, after)
    positive_grid = independent_selected_case(3, 5, before)
    positive_ledger = verify_terminal(positive_grid)
    physical_runs, _, physical_before = maximal_strips(positive_grid)
    physical_positive = certify_reservation_batch(physical_runs, physical_before, after)
    assert not positive_ledger['receivers']
    assert physical_positive['score_change'] == positive['score_change']
    assert positive['sufficient_condition']
    assert not positive['componentwise_sufficient_condition']
    assert (positive['before'], positive['residual_after'], positive['score_change']) == (12, 10, 0)
    assert positive['weighted_odd_before'] == positive['weighted_odd_after'] == 2
    _, records = array_records(2, 4)
    before = {(row, column): 0 for row in range(2) for column in range(4)}
    before.update({(0, 0): 2, (0, 1): 2, (0, 2): 2, (1, 3): 1})
    after = dict(before)
    after[(0, 0)] -= 1
    after[(1, 3)] -= 1
    negative = certify_reservation_batch(records, before, after)
    negative_grid = independent_selected_case(2, 4, before)
    negative_ledger = verify_terminal(negative_grid)
    physical_runs, _, physical_before = maximal_strips(negative_grid)
    physical_negative = certify_reservation_batch(physical_runs, physical_before, after)
    assert not negative_ledger['receivers']
    assert physical_negative['score_change'] == negative['score_change']
    assert not negative['sufficient_condition'] and negative['score_change'] == -1
    assert (negative['before'], negative['residual_after']) == (7, 4)
    assert sum(component['odd_before'] for component in negative['components']) == 2
    assert sum(component['odd_after'] for component in negative['components']) == 2
    assert (negative['weighted_odd_before'], negative['weighted_odd_after']) == (0, 2)
    return dict(weighted_to_weighted_compensation=positive,
                all_component_parity_counterexample=negative,
                scope='Abstract resource examples, realizable with independent selected '
                      'vertices and empty matching. No positive receiver charge, '
                      'owned-donor or freezing assertion for these examples.')


def frozen_controls():
    current, certificate = two_leg_case(6, 4, 6)
    inspect(current, certificate)
    donors = saturated_endpoint_donors(current)
    assert {(1, 1), (1, 2)} <= {tuple(donor['tile']) for donor in donors}
    runs, _, before = maximal_strips(current)
    _, _, after_right = maximal_strips(current, {(1, 2): 1})
    _, _, after_left = maximal_strips(current, {(1, 1): 1})
    _, _, after_both = maximal_strips(current, {(1, 1): 1, (1, 2): 1})
    right = certify_reservation_batch(runs, before, after_right)
    left = certify_reservation_batch(runs, before, after_left)
    both = certify_reservation_batch(runs, before, after_both)
    second_safe_step = certify_reservation_batch(runs, after_left, after_both)
    assert not right['sufficient_condition'] and right['score_change'] == -1
    assert left['sufficient_condition'] and left['score_change'] == 0
    assert both['sufficient_condition'] and both['score_change'] == 0
    assert second_safe_step['sufficient_condition'] and second_safe_step['score_change'] == 0
    images = 0
    for symmetry in itertools.product((False, True), repeat=3):
        shape, chosen, matching = transformed(*current, *symmetry)
        physical = *shape, chosen, matching
        inspect(physical)
        runs, _, residual = maximal_strips(physical)
        image_donors = saturated_endpoint_donors(physical)
        assert len(image_donors) == 2
        individual = []
        final = dict(residual)
        for donor in image_donors:
            tile = tuple(donor['tile'])
            after = dict(residual)
            after[tile] -= 1
            individual.append((after, certify_reservation_batch(runs, residual, after)))
            final[tile] -= 1
        assert sorted(report['score_change'] for _, report in individual) == [-1, 0]
        safe_after = next(after for after, report in individual if report['sufficient_condition'])
        assert certify_reservation_batch(runs, safe_after, final)['sufficient_condition']
        assert certify_reservation_batch(runs, residual, final)['sufficient_condition']
        for tile in residual:
            if residual[tile] == 2:
                after = dict(residual)
                after[tile] = 0
                parallel_pair = certify_reservation_batch(runs, residual, after)
                assert parallel_pair['sufficient_condition']
        images += 1
    return dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                ordered_freezing_certificate=certificate, owned_donors=donors,
                symmetry_images=images,
                unsafe_right_donor=right, safe_left_donor=left,
                safe_two_donor_batch=both, safe_second_step=second_safe_step,
                conclusion='The original right-first step loses one credit. Reserving '
                           'the left owned unit first makes both individual steps safe; '
                           'reserving both as one batch is also safe. The two units are '
                           'distinct physical tiles; no credit is reused.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='PASS', abstract=abstract_controls(),
                  cross_component=cross_component_controls(), frozen=frozen_controls(),
                  scope='Every one of 46656 capacity/removal vectors on a two-by-three '
                        'abstract tile array checks the exact handshake identity, '
                        'component splitting and the signed aggregate parity inequality '
                        'with the OLD weighted-branch mask held fixed, nonnegative '
                        'recovery surplus and the necessary and sufficient budget test. '
                        'All full two-unit tile removals satisfy the rule. The rule is '
                        'sufficient, not necessary; failed certification is not itself '
                        'a decrease. Actual owned-donor order/batch checks use the frozen '
                        '20-endpoint example with its original ledger and all eight '
                        'symmetries. No universal safe ordering of all donors or grid '
                        'coverage theorem is asserted.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], abstract=report['abstract'],
                         frozen_summary=report['frozen']['conclusion'])))


if __name__ == '__main__':
    main()
