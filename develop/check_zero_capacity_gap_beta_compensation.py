"""Check frozen zero-capacity gap barriers and cross-component beta pairing."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data, solve
from check_endpoint_free_gap_compensation import gap_access
from check_native_guard_compensation import force_matching
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, components, direct_family, terminal_data, uniform_certificates,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def barrier_family(width, depth, reflect_left=False):
    assert width >= 6 and width % 2 == 0 and depth >= 1
    shift = 2*depth+4
    selected, matching, copies = set(), [], []
    for size, vertical, horizontal, reflect in [(width, 0, 0, False),
                                                (width+2, -1, -2*depth-5, reflect_left),
                                                (width+2, -1, 2*depth+5, False)]:
        base = direct_family(size, 4)
        move = lambda point: (point[0]+vertical,
                              (10-point[1] if reflect else point[1])+horizontal+shift)
        following = {move(point) for point in base[2]}
        endpoints = {move(point) for edge in base[3] for point in edge}
        assert not (selected | {point for edge in matching for point in edge}) & (following | endpoints)
        selected |= following
        matching += [tuple(move(point) for point in edge) for edge in base[3]]
        copies.append((size, base))
    original = set(selected)
    for row, opposite in [(5, 4), (width+4, width+5)]:
        for step in range(1, 2*depth+1):
            selected.add((opposite if step % 2 else row, 2-2*depth+step+shift))
            selected.add((row if step % 2 else opposite, 7+step+shift))
    assert len(selected-original) == 8*(depth-1)
    current = width+12, 4*depth+20, selected, matching
    bands = [[((row, column), (row+1, column)) for column in range(current[1])]
             for row in range(2, width+7, 2)]
    return current, bands, selected-original, copies, shift


def zero_gap_links(current, bands, kinds):
    _, labels, _, _, _, _, _ = terminal_data(current, bands)
    result, witnesses = [], {}
    for band, columns in enumerate(bands):
        position = 0
        while position < len(columns):
            if 'P' in labels[band][position]:
                position += 1
                continue
            first = position
            while position < len(columns) and 'P' not in labels[band][position]:
                position += 1
            if first == 0 or position == len(columns):
                continue
            if not all(sorted(labels[band][column]) == ['B', 'T']
                       for column in range(first, position)):
                continue
            boundaries = [[point for point in columns[column] if point in kinds]
                          for column in (first-1, position)]
            if not all(len(points) == 1 for points in boundaries):
                continue
            first_point, second_point = boundaries[0][0], boundaries[1][0]
            if kinds[first_point] == kinds[second_point]:
                continue
            link = ((first_point, second_point) if kinds[first_point] == 'TP'
                    else (second_point, first_point))
            assert link not in witnesses
            cells = {point for column in columns[first:position] for point in column}
            assert len(cells)//2 == len(current[2] & cells)
            result.append(link)
            witnesses[link] = dict(band=band, first=first, last=position-1,
                                   columns=position-first, vertices=cells)
    return result, witnesses


def pp_cut_control(current, bands, kinds, pairs, resources, width, depth, shift, margin, totals):
    cut = ((width+4, 2-2*depth+shift), (width+5, 2-2*depth+shift))
    endpoints = {point for edge in current[3] for point in edge}
    assert set(cut) <= endpoints and not set(cut) & set(kinds)
    assert frozenset(cut) in {frozenset(edge) for edge in current[3]}
    auxiliary = [tuple(column) for columns in bands for column in columns
                 if set(column) <= endpoints and frozenset(column) != frozenset(cut)]
    new_kinds = dict(kinds)
    new_kinds.update({point: 'BP' for point in cut})
    new_pairs = [tuple(record['ends']) for record in components(endpoints, current[3]+auxiliary)
                 if record['ends']]
    assert {frozenset(pair) for pair in new_pairs} == {frozenset(pair) for pair in pairs+[cut]}
    _, alphas, betas, _ = owner_data(new_kinds, new_pairs)
    assert len(alphas) == 1 and len(betas) == 3
    link = ((width+4, 3+shift), cut[1])
    _, inventory, _ = cancel_pairs(new_kinds, new_pairs, [link], Counter())
    assert inventory['TP', 'TP'] == 0 and inventory['BP', 'BP'] == 2
    assert len(resources)+inventory['BP', 'BP'] == margin+1
    assert len(resources)+inventory['BP', 'BP']-1 == margin
    assert 2-inventory['BP', 'BP'] == 0
    totals['explicit_pp_cycle_cut_debt_controls'] += 1


def general_pp_cut_controls(current, bands, kinds, resources, margin, totals):
    endpoints = {point for edge in current[3] for point in edge}
    auxiliary = [tuple(column) for columns in bands for column in columns if set(column) <= endpoints]
    original = components(endpoints, current[3]+auxiliary)
    owner = {point: record for record in original for point in record['vertices']}
    for edge in auxiliary:
        record = owner[edge[0]]
        ends = record['ends']
        label = ('cycle' if not ends else
                 'alpha' if all(kinds[point] == 'TP' for point in ends) else
                 'beta' if all(kinds[point] == 'BP' for point in ends) else 'mixed')
        totals['single_pp_cut_on_original_'+label] += 1
    choices = [(edge,) for edge in auxiliary]
    choices += [tuple(auxiliary[:count]) for count in range(len(auxiliary)+1)]
    for cuts in choices:
        removed = {frozenset(edge) for edge in cuts}
        remaining = [edge for edge in auxiliary if frozenset(edge) not in removed]
        new_kinds = dict(kinds)
        new_kinds.update({point: 'BP' for edge in cuts for point in edge})
        assert len(new_kinds) == len(kinds)+2*len(cuts)
        pairs = [tuple(record['ends']) for record in components(endpoints, current[3]+remaining)
                 if record['ends']]
        _, alphas, betas, _ = owner_data(new_kinds, pairs)
        assert len(betas)-len(alphas) == 1+len(cuts)
        assert len(resources)+len(betas)-len(alphas)-len(cuts) == margin
        totals['arbitrary_pp_cut_set_ledger_controls'] += 1


def auxiliary_rematching_control(current, bands, kinds, resources, width, depth, shift, margin, totals):
    endpoints = {point for edge in current[3] for point in edge}
    auxiliary = [tuple(column) for columns in bands for column in columns if set(column) <= endpoints]
    outer = 2-2*depth+shift
    removed = [((4, column), (5, column)) for column in (outer, outer-1)]
    added = [((5, 3+shift), (4, outer)), ((5, outer), (5, outer-1)),
             ((4, outer-1), (4, outer-2))]
    removed_sets = {frozenset(edge) for edge in removed}
    assert removed_sets <= {frozenset(edge) for edge in auxiliary}
    following = [edge for edge in auxiliary if frozenset(edge) not in removed_sets]+added
    covered = [point for edge in following for point in edge]
    assert len(covered) == len(set(covered))
    source, beta_terminal = added[0][0], added[-1][-1]
    assert kinds[source] == 'TP' and kinds[beta_terminal] == 'BP'
    assert endpoints-set(covered) == set(kinds)-{source, beta_terminal}
    assert {point for edge in auxiliary for point in edge} <= set(covered)
    corridor = {(row, column) for row in (4, 5) for column in range(outer+1, 3+shift)}
    assert len(corridor) == 4*depth and len(current[2] & corridor) == 2*depth
    assert not corridor & endpoints
    assert all(first in endpoints and second in endpoints
               and abs(first[0]-second[0])+abs(first[1]-second[1]) == 1
               for first, second in added[1:])
    new_kinds = {point: kinds[point] for point in endpoints-set(covered)}
    pairs = [tuple(record['ends']) for record in components(endpoints, current[3]+following)
             if record['ends']]
    _, alphas, betas, mixed = owner_data(new_kinds, pairs)
    assert (len(alphas), len(betas), len(mixed)) == (0, 1, 8)
    joined = frozenset(((width+4, 3+shift), (width+5, outer-4)))
    assert joined in {frozenset(pair) for pair in pairs}
    assert len(resources)+len(betas)-len(alphas) == margin
    totals['zero_debt_auxiliary_rematching_repairs'] += 1
    totals['pp_auxiliary_edges_replaced'] += 2
    totals['new_auxiliary_witness_edges'] += 3


def control(width, depth, totals, reflect_left=False):
    current, bands, added, copies, shift = barrier_family(width, depth, reflect_left)
    direct_check(*current)
    occupied = current[2] | {point for edge in current[3] for point in edge}
    assert all(not any(abs(point[0]-other[0])+abs(point[1]-other[1]) == 1
                       for other in occupied-{point}) for point in added)
    for size, base in copies:
        uniform_certificates(base, size, 4, totals)
    force_matching(current, totals)
    frozen, _ = frozen_certificate(current)
    assert frozen == {point for edge in current[3] for point in edge}
    original, kinds, pairs, resources, access, _, gaps = gap_access(current, bands, totals)
    assert (original['alpha'], original['beta'], original['gamma']) == (1, 2, 7)
    assert len(current[2]) == 8*depth+31 and len(current[3]) == 3*width+16
    margin = (2*depth+6)*width+4*depth+7
    assert original['boundary_budget'] == width+6
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*margin
    assert len(resources) == margin-1
    if (width, depth) in [(6, 1), (8, 2)]:
        general_pp_cut_controls(current, bands, kinds, resources, margin, totals)
    ordinary = [(first, second) for first in kinds for second in kinds
                if kinds[first] == 'TP' and kinds[second] == 'BP'
                and first[0] == second[0] and abs(first[1]-second[1]) == 1]
    old = solve(kinds, pairs, ordinary, access, resources)
    assert old['value'] == 0 and old['deficit'] == 1 and old['cut'] == []
    central = {(row, column+shift) for row in (5, width+4) for column in (3, 5, 7)}
    assert all(kinds[point] == 'TP' and not access[point] for point in central)
    assert all(second in central for first, second in pairs if first in central
               and kinds[second] == 'TP')
    gap_links, witnesses = zero_gap_links(current, bands, kinds)
    if reflect_left:
        assert not gap_links
        repaired = solve(kinds, pairs, ordinary+gap_links, access, resources)
        assert repaired['value'] == 0 and repaired['deficit'] == 1 and repaired['cut'] == []
        boundaries = [(row, column+shift) for row in (4, width+4)
                      for column in (2-2*depth, 2*depth+8)]
        endpoints = {point for edge in current[3] for point in edge}
        assert all({point, (point[0]+1, point[1])} <= endpoints for point in boundaries)
        assert not {point for corner in boundaries
                    for point in (corner, (corner[0]+1, corner[1]))} & set(kinds)
        pp_cut_control(current, bands, kinds, pairs, resources, width, depth, shift, margin, totals)
        auxiliary_rematching_control(current, bands, kinds, resources,
                                     width, depth, shift, margin, totals)
        totals['fully_frozen_reflected_pp_barriers'] += 1
        totals['unrestricted_zero_gap_pairing_obstructions'] += 1
        return dict(width=width, depth=depth, reflected_left=True, margin=margin,
                    full_gap_and_corridor_pairing_maximum=0, deficit=1,
                    whole_original_beta_resources=2, corridor_columns=2*depth,
                    naive_pp_opening_overcount=1, zero_debt_auxiliary_repair=1,
                    auxiliary_edges_removed=2, new_auxiliary_edges=3)
    chosen = ((width+4, 3+shift), (width+5, 2-2*depth+shift))
    assert chosen in gap_links
    owners, alphas, betas, _ = owner_data(kinds, pairs)
    assert owners[chosen[0]] in alphas and owners[chosen[1]] in betas
    assert witnesses[chosen]['columns'] == 2*depth
    assert all(not witness['vertices'] & {point for edge in current[3] for point in edge}
               for witness in witnesses.values())
    reduced, inventory, records = cancel_pairs(kinds, pairs, [chosen], totals)
    assert inventory['TP', 'TP'] == 0 and inventory['BP', 'BP'] == 1
    assert any(record['alpha'] == record['beta'] == 1 for record in records)
    repaired = solve(kinds, pairs, ordinary+gap_links, access, resources)
    assert repaired['value'] == 1 and repaired['cost'] == 1
    assert repaired['payments'] == []
    assert len(repaired['links']) == 1 and repaired['links'][0] in gap_links
    assert len(resources)+inventory['BP', 'BP']-inventory['TP', 'TP'] == margin
    totals['fully_frozen_zero_gap_barriers'] += 1
    totals['unrestricted_full_gap_access_obstructions'] += 1
    totals['single_zero_gap_beta_repairs'] += 1
    totals['zero_gap_link_witnesses'] += len(witnesses)
    return dict(width=width, depth=depth, selected=len(current[2]), matching=len(current[3]),
                packet_shape=[width+6, 4*depth+20], inventory=dict(alpha=1, beta=2, mixed=7),
                margin=margin, unmarked_interval_units=len(resources),
                full_gap_access_maximum=old['value'], deficit=old['deficit'], empty_separator=old['cut'],
                corridor_columns=2*depth, chosen_corridor_link=chosen,
                augmented_maximum=repaired['value'], minimum_total_virtual_links=repaired['cost'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for width, depth in itertools.product((6, 8, 12, 20), range(1, 25)):
        record = control(width, depth, totals)
        reflected = control(width, depth, totals, reflect_left=True)
        if (width, depth) in [(6, 1), (8, 8), (20, 24)]:
            examples.extend([record, reflected])
    record = dict(status='PASS', totals=dict(totals), examples=examples,
                  scope='Finite controls for the written arbitrary-length frozen three-copy '
                  'obstruction to unrestricted full-gap resource access and its single '
                  'zero-surplus corridor accounting pairing into one whole original beta. '
                  'Also covers the reflected PP-boundary obstruction to free-terminal corridor '
                  'pairing, explicit PP-opening debt, selected single/prefix cut sets, and '
                  'two-PP-edge/three-new-edge auxiliary rematching with zero net debt. '
                  'All surgeries change auxiliary accounting strands, not actual matching '
                  'or selected vertices. No universal grid inequality or Lean geometry proof.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
