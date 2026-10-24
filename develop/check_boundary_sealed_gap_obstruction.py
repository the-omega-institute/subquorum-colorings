"""Full-gap route obstruction and whole-support gap allocation.

Written all-parameter proofs: BOUNDARY_SEALED_GAP_OBSTRUCTION.md.
No solver or finite run establishes those universal statements.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_bt_corridor_ports import compile_model, compress_gap_access
from check_colored_row_owner_deficiency import verify_phase_network
from check_compensation_flow_normal_form import solve
from check_cooperative_promotion import neighbors
from check_endpoint_free_gap_compensation import gap_access
from check_even_bridge_support_completion import endpoints_of, tiles_of
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_one_sided_interval_allocation import allocate, independent_maximum
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_terminal_cancellation_and_stranded_demand import (
    all_link_matchings, cancel_pairs, direct_family, uniform_certificates,
)

if not __debug__:
    raise RuntimeError('Verification requires assertions; do not run with -O.')


def family(width, height, columns):
    assert width >= 6 and height >= 4 and columns >= height+6
    assert width % 2 == height % 2 == columns % 2 == 0
    base = direct_family(width, height)
    r = width+4
    added = {(4, 1), (r+1, 1)}
    added |= {(4 if (c-8) % 2 else 5, c) for c in range(9, columns-1)}
    added |= {(r+1 if (c-height-4) % 2 else r, c)
              for c in range(height+5, columns-1)}
    occupied = base[2] | endpoints_of(base) | added
    assert not added & base[2]
    assert all(not (set(neighbors(v)) & (occupied-{v})) for v in added)
    current = width+12, columns, base[2] | added, base[3]
    crop = [[((rr, c), (rr+1, c)) for c in range(columns)] for rr in range(4, r+1, 2)]
    cells = {v for band in crop for column in band for v in column}
    assert current[2] | endpoints_of(current) <= cells
    receiver_cells = {v for rr, cc in tiles_of(endpoints_of(current))
                      for v in itertools.product((2*rr, 2*rr+1), (2*cc, 2*cc+1))}
    assert receiver_cells <= cells
    return current, crop, added


def support_allocation(current, bands, data, meta, fixed, totals):
    """Intervals can see the full support of a virtual alpha, not only its tips.

    This is an additional COUNTING access model, not terminal route equivalence.
    """
    kinds, pairs, _, _, resources = data
    reduced, inventory, records = cancel_pairs(kinds, pairs, fixed, Counter())
    alphas = [pair for pair in reduced if all(kinds[v] == 'TP' for v in pair)]
    tip_owner = {v: i for i, pair in enumerate(pairs) for v in pair}
    old_to_new = {}
    for component in records:
        new = next((i for i, pair in enumerate(alphas)
                    if set(pair) == set(component['ends'])), None)
        for v in component['vertices']:
            old = tip_owner[v]
            if old in old_to_new:
                assert old_to_new[old] == new
            old_to_new[old] = new
    assert set(old_to_new) == set(range(len(pairs)))
    endpoints = endpoints_of(current)
    node_owner = {}
    for component in meta['original']['components']:
        if component['kind'] == ['cycle']:
            old = None
        else:
            node = component['nodes'][0]
            tip = next(v for v in bands[node[0]][node[1]] if v in endpoints)
            old = tip_owner[tip]
        for node in component['nodes']:
            assert node not in node_owner
            node_owner[node] = old
    _, _, _, rr, terminal_access, _, gaps = gap_access(current, bands, Counter())
    assert rr == resources
    incidence = {j: set() for j in resources}
    compressed = {j: set() for j in resources}
    witness = {}
    for gap in gaps:
        b, first, last = gap['band'], gap['first'], gap['last']
        units = sorted((j for j in resources if meta['intervals'][j]['band'] == b
                        and first <= meta['intervals'][j]['first'] <= last),
                       key=lambda j: meta['intervals'][j]['first'])
        for side, c in enumerate((first-1, last+1)):
            old = node_owner.get((b, c))
            if old is None or old_to_new[old] is None:
                continue
            new = old_to_new[old]
            if meta['labels'][b][c] == ('P', 'P'):
                totals['internal_pp_support_candidates'] += 1
            for j in units:
                incidence[j].add(new)
                witness[new, j] = dict(node=(b, c), original_strand=old)
            if units:
                compressed[units[0] if side == 0 else units[-1]].add(new)
    assert all(len(owners) <= 2 for owners in incidence.values())
    result = allocate(len(alphas), incidence)
    optimum = independent_maximum(len(alphas), incidence)
    assert len(result['assignment']) == optimum
    assert independent_maximum(len(alphas), compressed) == optimum
    terminal_incidence = {j: {i for i, pair in enumerate(alphas)
                              if any(j in terminal_access[v] for v in pair)} for j in resources}
    assert all(terminal_incidence[j] <= incidence[j] for j in resources)
    terminal_paid = independent_maximum(len(alphas), terminal_incidence)
    assert terminal_paid <= optimum
    defect, spare = len(result['deficient']), len(result['spare_resources'])
    margin = spare+inventory['BP', 'BP']-defect
    assert 2*margin == meta['original']['surplus_twice']-2*meta['original']['boundary_budget']
    totals['whole_support_allocation_controls'] += 1
    totals['strict_whole_support_improvements'] += optimum > terminal_paid
    totals['whole_support_payments'] += optimum
    totals['support_deficient_controls'] += bool(defect)
    totals['support_deficient_tree_occurrences'] += defect
    totals['two_alpha_interval_occurrences'] += sum(len(users) == 2 for users in incidence.values())
    return dict(alpha=len(alphas), beta=inventory['BP', 'BP'], paid=optimum,
                terminal_paid=terminal_paid, defect=defect, spare=spare, margin=margin,
                payments=[dict(alpha=a, interval=j, **witness[a, j])
                          for a, j in sorted(result['assignment'].items())])


def control(current, bands, totals, exhaustive=False):
    direct_check(*current)
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints_of(current)
    data, meta = compile_model(current, bands, Counter())
    full, sparse, _, _ = compress_gap_access(current, bands, meta, data[-1], Counter())
    kinds, pairs, links, _, resources = data
    answer = solve(kinds, pairs, links, full, resources)
    assert (answer['value'], answer['cost']) == (solve(*data)['value'], solve(*data)['cost'])
    colors = {v: sum(v) % 2 for v in kinds}
    phase = verify_phase_network(kinds, pairs, links, full, resources, colors, Counter())
    assert phase['deficit'] == answer['deficit']
    support = support_allocation(current, bands, data, meta, [], totals)
    choices = all_link_matchings(links) if exhaustive else ([],)+tuple([link] for link in links)
    enumerated = 0
    for fixed in choices:
        check = support_allocation(current, bands, data, meta, fixed, totals)
        if answer['value'] == 0 and meta['original']['beta'] == 0:
            assert check['terminal_paid'] == 0
        totals['fixed_cancellation_controls'] += 1
        enumerated += 1
    if exhaustive:
        totals['exhaustive_horizontal_matchings'] += enumerated
    totals['frozen_geometry_controls'] += 1
    return dict(alpha=meta['original']['alpha'], beta=meta['original']['beta'],
                mixed=meta['original']['gamma'],
                margin=meta['original']['surplus_twice']//2-meta['original']['boundary_budget'],
                resources=len(resources), full_gap_value=answer['value'],
                full_gap_deficit=answer['deficit'], min_cut=answer['cut'],
                blocked=answer['blocked'], phases=phase['phase_blocked_at_min_cut'],
                support=support)


def stack(current, count):
    selected, matching = set(), []
    for i in range(count):
        move = lambda v: (v[0]+i*current[0], v[1])
        selected |= {move(v) for v in current[2]}
        matching += [tuple(move(v) for v in pair) for pair in current[3]]
    return count*current[0], current[1], selected, matching


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals, examples = Counter(), []
    for w, h, extra in itertools.product(range(6, 23, 2), range(4, 19, 2), (0, 2, 8)):
        n = h+6+extra
        current, crop, added = family(w, h, n)
        uniform_certificates(direct_family(w, h), w, h, Counter())
        assert len(current[2]) == 2*n-5
        assert len(added) == 2*n-h-14
        crop_margin = (w//2-1)*n+3-2*w-h
        whole_margin = (w//2+4)*n-2*w-h-7
        assert crop_margin >= 7 and whole_margin == crop_margin+5*(n-2)
        for name, bands, margin in (('crop', crop, crop_margin),
                                    ('whole_board', whole_bands(current), whole_margin)):
            result = control(current, bands, totals)
            assert (result['alpha'], result['beta'], result['mixed']) == (1, 0, h+1)
            assert result['margin'] == margin
            assert result['full_gap_value'] == 0 and result['full_gap_deficit'] == 1
            assert result['min_cut'] == [] and result['phases'][0] == result['phases'][1] == result['blocked']
            assert result['support']['paid'] == 1 and result['support']['defect'] == 0
            if (w, h, extra) in ((6, 4, 0), (6, 4, 8), (22, 18, 2)):
                examples.append(dict(parameters=[w,h,n], packet=name, result=result))
            totals['uniform_family_packet_controls'] += 1
    base, crop, _ = family(6, 4, 10)
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*base, *symmetry)
        move = image_map(*base[:2], symmetry)
        bands = [[tuple(move(v) for v in column) for column in band] for band in crop]
        result = control((*shape, selected, matching), bands, totals)
        assert result['full_gap_deficit'] == result['support']['paid'] == 1
        totals['carried_band_isometries'] += 1
    for count in range(1, 9):
        model = stack(base, count)
        result = control(model, whole_bands(model), totals)
        assert result['full_gap_deficit'] == result['alpha'] == count
        assert result['min_cut'] == [] and result['margin'] == 47*count
        assert result['support']['paid'] == count and result['support']['defect'] == 0
        totals['separated_stack_controls'] += 1
    result = control(base, crop, totals, exhaustive=True)
    totals['all_horizontal_matchings_smallest_fixture'] = 1
    # Carried configurations exercise multiple virtual sources and pure cycles.
    from check_compensation_flow_geometry_frontier import pad_image
    from check_exchange_terminal_nonunique import fixture, matching_orders
    from check_frozen_first_destination_allocation import fixture as unported
    from degree_three_fusion import occupied_bands
    from rotor_networks import rotor
    module=rotor(); bent=fixture()
    fixtures=[(*bent[:3], list(x['matching'])) for x in matching_orders()]
    fixtures += [unported()[0], occupied_bands(6)[0],
                 (6,6,module['selected'],module['matching']), (8,8,{(2,2),(3,2)},[])]
    two=direct_family(6,4)
    move=lambda v:(v[0],v[1]+9)
    two=(18,30,two[2] | {move(v) for v in two[2]},
         two[3]+[tuple(move(v) for v in edge) for edge in two[3]])
    fixtures.append(two)
    # After TWO links the first alpha, rather than a separate mixed owner,
    # owns the left side of the physical shared two-unit gap.
    two_data,two_meta=compile_model(two,whole_bands(two),Counter())
    shared_result=support_allocation(two,whole_bands(two),two_data,two_meta,
        [((5,3),(5,4)),((5,5),(5,6))],totals)
    assert shared_result['alpha']==shared_result['paid']==2
    support_only_counterexample=None
    for model, symmetry, offset in itertools.product(fixtures,
            itertools.product((False,True), repeat=3), itertools.product((2,3),repeat=2)):
        model=pad_image(model,symmetry,offset)
        result=control(model,whole_bands(model),totals)
        if result['support']['defect'] and symmetry==(False,False,False) and offset==(2,2):
            support_only_counterexample=dict(source_fixture='develop/fixtures/unported_shared_mixed_gate.json',
                symmetry=symmetry,offset=offset,result=result,
                scope='Real frozen interval-only t=0 counterexample; beta resources pay both sources in terminal network.')
        totals['carried_geometry_controls'] += 1
    assert support_only_counterexample is not None
    assert totals['two_alpha_interval_occurrences'] > 0
    frozen,layers=frozen_certificate(base)
    fixture_record=dict(shape=base[:2], selected=sorted(base[2]), matching=base[3],
                        freezing_layers=layers, crop_bands=crop)
    report=dict(status='PASS',totals=dict(totals),examples=examples,fixture=fixture_record,
                support_only_counterexample=support_only_counterexample,
                physical_two_owner_gap_control=shared_result,
                scope='Written uniform fully frozen uniquely matched obstruction to FULL endpoint-free-gap terminal routes, '
                      'including whole-board packets and arbitrarily many separated sources; empty two-phase cut deficit. '
                      'Whole-support gap incidence has at most two virtual-alpha owners per original interval, '
                      'exact standard allocation defect and sparse extreme compression; conditional counting model, '
                      'not free-terminal routing equivalence or a universal grid/5of6 proof.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__ == '__main__':
    main()
