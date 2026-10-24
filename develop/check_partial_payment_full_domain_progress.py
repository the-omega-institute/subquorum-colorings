"""Check partial-payment progress without treating unpaid markers as resources."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory, matchings
from check_full_domain_marker_compensation import full_signs, model
from check_mixed_relay_orientation import forest_budget
from check_terminal_cancellation_and_stranded_demand import components


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def verify(data, replacement, totals):
    vertices, actual, auxiliary, kinds, chosen, marker_indices = data
    free = set(kinds)-chosen
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices-free
    colours, cycles, markers = full_signs(*data)
    original = inventory(components(vertices, actual+auxiliary),kinds)
    records = components(vertices,actual+replacement)
    final = inventory(records,{point:kinds[point] for point in free})
    alphas = [record for record in records if record['ends']
              and all(kinds[point] == 'TP' for point in record['ends'])]
    local_markers = [{unit for edge,(_,unit) in markers.items() if edge <= record['vertices']}
                     for record in alphas]
    all_units = sorted(marker_indices.values())
    sources = len(chosen)//2
    no_actual_marker = sum(not units for units in local_markers)
    errors, rank = forest_budget(replacement,colours,cycles,{'alpha':no_actual_marker})
    for flags in itertools.product((False,True),repeat=len(all_units)):
        backed = {unit for unit,flag in zip(all_units,flags) if flag}
        unbacked = set(all_units)-backed
        assert len(unbacked) == original['alpha']-sources-len(backed)
        payments, unpaid, demand_markers = set(), [], set()
        for record, units in zip(alphas,local_markers):
            if units & backed:
                unit = min(units & backed)
                assert unit not in payments
                edge,(point,_) = next((edge,pair) for edge,pair in markers.items() if pair[1] == unit)
                assert edge <= record['vertices'] and point in record['ends'] and point in free
                payments.add(unit)
            else:
                unpaid.append(record)
                if units:
                    marker = min(units)
                    assert marker in unbacked and marker not in demand_markers
                    demand_markers.add(marker)
        assert payments <= backed and not payments & demand_markers
        old_deficit = original['alpha']-len(backed)
        new_deficit = final['alpha']-len(payments)
        assert new_deficit == len(unpaid)
        assert new_deficit <= old_deficit-sources+rank//2
        for flips in itertools.product((-1,1),repeat=len(cycles)):
            signs = dict(colours)
            for cycle,flip in zip(cycles,flips):
                signs.update({point:colours[point]*flip for point in cycle})
            negative = sum(signs[first] == signs[second] == -1 for first,second in replacement)
            positive = sum(signs[first] == signs[second] == 1 for first,second in replacement)
            assert negative == positive
            error_edges = set()
            for record,units in zip(alphas,local_markers):
                if units:
                    continue
                witnesses = [frozenset(edge) for edge in replacement if set(edge) <= record['vertices']
                             and signs[edge[0]] == signs[edge[1]] == -1]
                assert witnesses and witnesses[0] not in error_edges
                error_edges.add(witnesses[0])
            assert new_deficit <= old_deficit-sources+negative
            for spare in (0,2):
                actual_resources = len(backed)+spare
                original_margin = actual_resources+original['beta']-original['alpha']
                unused_resources = actual_resources-len(payments)+final['beta']
                assert original_margin == unused_resources-new_deficit
                totals['negative_original_ledger_controls'] += original_margin < 0
                totals['exact_partial_payment_ledgers'] += 1
            if negative == 0:
                assert new_deficit <= old_deficit-sources
                totals['coherent_partial_progress_certificates'] += 1
                totals['strict_unpaid_count_reductions'] += sources > 0
            totals['partial_payment_sign_controls'] += 1
        totals['partial_payment_backing_subsets'] += 1
    totals['partial_payment_replacements'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    arguments = parser.parse_args()
    totals = Counter()
    relay_choices = ((('alpha',0),),(('alpha',1),),(('alpha',0),('alpha',0)),
                     (('alpha',1),('mixed',0)),(('alpha',0),('mixed',1)),
                     (('alpha',0),('beta',0)))
    for sources in (0,1,2):
        for sizes in itertools.product(range(2),repeat=2*sources):
            for relays in relay_choices:
                for cycle_pairs in (0,1):
                    if sources+sum(sizes)+sum(size for _,size in relays)+cycle_pairs > 4:
                        continue
                    for chosen_ends in itertools.product((0,1),repeat=2*sources):
                        for marker_ends in itertools.product((0,1),repeat=sum(kind=='alpha' for kind,_ in relays)):
                            data = model(sources,sizes[:sources],sizes[sources:],relays,
                                         marker_ends,chosen_ends,cycle_pairs)
                            vertices,_,_,kinds,chosen,_ = data
                            domain = vertices-(set(kinds)-chosen)
                            for replacement in matchings(sorted(domain)):
                                if 2*len(replacement) == len(domain):
                                    verify(data,replacement,totals)
    assert totals['negative_original_ledger_controls'] and totals['strict_unpaid_count_reductions']
    record = dict(status='PASS',totals=dict(totals),
                  scope='Partial backing of terminal-incident positive actual markers. Every backing '
                  'subset is checked with only backed markers counted as real interval units. '
                  '0..2 selected source/donor pairs, up to eight N-covered vertices, selected '
                  'tails through one PP pair, unselected unpaid/paid alpha relays and optional '
                  'mixed/beta relays and cycles. All replacement matchings, cycle flips, '
                  'injective transported units, separate unbacked demand-marker/error witnesses, '
                  'delta_N<=delta_old-r+h, forest bound and residual ledger including negative '
                  'abstract starting margins. No physical negative-margin grid or route-existence '
                  'theorem is inferred. This extends the full-domain proof after its original review input.')
    arguments.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),sort_keys=True))


if __name__ == '__main__':
    main()
