"""Check balanced mixed free-end activation and a uniform seven-edge repair."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory
from check_full_domain_marker_compensation import full_signs, model, physical_sign
from check_mixed_relay_orientation import forest_budget
from check_native_guard_compensation import force_matching
from check_port_choice_rematching_cost import candidate_graph, family
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    components, terminal_data, uniform_certificates,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def perfect_matchings(vertices):
    if not vertices:
        yield []
        return
    first, *remaining = vertices
    for index, second in enumerate(remaining):
        for following in perfect_matchings(remaining[:index]+remaining[index+1:]):
            yield [(first, second)]+following


def activate(data, active_records):
    vertices, actual, auxiliary, kinds, chosen, marker_indices = data
    signs, cycles, markers = full_signs(*data)
    following_chosen = set(chosen)
    for record in active_records:
        assert len(record['ends']) == 2
        assert {kinds[point] for point in record['ends']} == {'TP', 'BP'}
        assert not following_chosen & set(record['ends'])
        following_chosen.update(record['ends'])
        signs.update({point: -signs[point] for point in record['vertices']})
    assert all(signs[point] == physical_sign(kind)*(1 if point in following_chosen else -1)
               for point, kind in kinds.items())
    assert all(signs[first]+signs[second] == 0 for first, second in auxiliary)
    return following_chosen, signs, cycles, markers


def verify(data, active_records, replacement, totals, explicit_signs=None):
    vertices, actual, auxiliary, kinds, chosen, marker_indices = data
    following_chosen, colours, cycles, markers = activate(data, active_records)
    free = set(kinds)-following_chosen
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices-free
    sources, relays = len(chosen)//2, len(active_records)
    assert len(replacement) == len(auxiliary)+sources+relays
    old = {frozenset(edge) for edge in auxiliary}
    following = {frozenset(edge) for edge in replacement}
    assert len(following-old) == len(old-following)+sources+relays
    original = inventory(components(vertices, actual+auxiliary), kinds)
    records = components(vertices, actual+replacement)
    final = inventory(records, {point: kinds[point] for point in free})
    assert 2*final['alpha']+final['mixed'] == 2*original['alpha']+original['mixed']-sources-relays
    assert 2*final['beta']+final['mixed'] == 2*original['beta']+original['mixed']-sources-relays
    assert final['beta']-final['alpha'] == original['beta']-original['alpha']
    assert sum(final[key] for key in ['alpha', 'beta', 'mixed']) == sum(original[key] for key in ['alpha', 'beta', 'mixed'])-sources-relays
    alphas = [record for record in records if record['ends']
              and all(kinds[point] == 'TP' for point in record['ends'])]
    marker_sets = [{unit for edge, (_, unit) in markers.items() if edge <= record['vertices']}
                   for record in alphas]
    no_marker = sum(not units for units in marker_sets)
    _, rank = forest_budget(replacement, colours, cycles, {'alpha': no_marker})
    orientations = []
    if explicit_signs is not None:
        orientations.append(explicit_signs)
    else:
        for flips in itertools.product((-1, 1), repeat=len(cycles)):
            signs = dict(colours)
            for cycle, flip in zip(cycles, flips):
                signs.update({point: colours[point]*flip for point in cycle})
            orientations.append(signs)
    units = sorted(marker_indices.values())
    for flags in itertools.product((False, True), repeat=len(units)):
        backed = {unit for unit, flag in zip(units, flags) if flag}
        unbacked = set(units)-backed
        assert len(unbacked) == original['alpha']-sources-len(backed)
        paid, demand_markers, error_components = set(), set(), []
        for record, local in zip(alphas, marker_sets):
            if local & backed:
                unit = min(local & backed)
                endpoint = next(point for edge, (point, marker) in markers.items()
                                if marker == unit and edge <= record['vertices'])
                assert endpoint in record['ends'] and endpoint in free and unit not in paid
                paid.add(unit)
            elif local:
                unit = min(local)
                assert unit in unbacked and unit not in demand_markers
                demand_markers.add(unit)
            else:
                error_components.append(record)
        deficit = final['alpha']-len(paid)
        old_deficit = original['alpha']-len(backed)
        assert deficit <= old_deficit-sources+rank//2
        for signs in orientations:
            negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
            positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
            assert negative == positive
            assert deficit <= old_deficit-sources+negative
            assert final['alpha'] <= original['alpha']-sources+negative
            assert final['beta'] <= original['beta']-sources+negative
            errors = set()
            for record in error_components:
                witnesses = [frozenset(edge) for edge in replacement if set(edge) <= record['vertices']
                             and signs[edge[0]] == signs[edge[1]] == -1]
                assert witnesses and witnesses[0] not in errors
                errors.add(witnesses[0])
            for record in records:
                actual_local = [edge for edge in actual if edge[0] in record['vertices']]
                new_local = [edge for edge in replacement if edge[0] in record['vertices']]
                actual_ends = [point for edge in actual_local for point in edge]
                new_ends = [point for edge in new_local for point in edge]
                assert Counter(new_ends+list(record['vertices'] & free)) == Counter(actual_ends)
            for spare in (0, 2):
                interval_count = len(backed)+spare
                margin = interval_count+original['beta']-original['alpha']
                remainder = interval_count-len(paid)+final['beta']
                assert margin == remainder-deficit
                totals['exact_residual_ledgers'] += 1
            if negative == 0:
                decrease = original['alpha']-sources-final['alpha']
                assert 0 <= decrease <= min(original['alpha']-sources, original['beta']-sources)
                assert final['mixed'] == original['mixed']+sources-relays+2*decrease
                totals['coherent_progress_controls'] += 1
            totals['backing_and_sign_controls'] += 1
    totals['complete_replacements'] += 1
    totals['activated_mixed_pairs'] += relays
    return dict(final={key: final[key] for key in ['alpha', 'beta', 'mixed', 'cycle']},
                sources=sources, relays=relays)


def abstract_controls(totals):
    relay_choices = [(), (('alpha', 0),), (('alpha', 1), ('mixed', 0)),
                     (('alpha', 0), ('mixed', 1)),
                     (('alpha', 0), ('alpha', 0), ('mixed', 0), ('mixed', 0)),
                     (('beta', 1), ('mixed', 0), ('mixed', 0)),
                     (('mixed', 0), ('mixed', 0))]
    for sources in (0, 1, 2):
        for sizes in itertools.product(range(2), repeat=2*sources):
            for relays in relay_choices:
                for cycle_pairs in (0, 1):
                    for chosen_ends in itertools.product((0, 1), repeat=2*sources):
                        for marker_ends in itertools.product((0, 1), repeat=sum(kind == 'alpha' for kind, _ in relays)):
                            data = model(sources, sizes[:sources], sizes[sources:], relays,
                                         marker_ends, chosen_ends, cycle_pairs)
                            vertices, actual, auxiliary, kinds, chosen, _ = data
                            mixed = [record for record in components(vertices, actual+auxiliary)
                                     if record['ends'] and {kinds[point] for point in record['ends']} == {'TP', 'BP'}]
                            for flags in itertools.product((False, True), repeat=len(mixed)):
                                active = [record for record, flag in zip(mixed, flags) if flag]
                                domain = vertices-set(kinds) | chosen | {point for record in active for point in record['ends']}
                                if len(domain) > 8:
                                    continue
                                for replacement in perfect_matchings(sorted(domain)):
                                    verify(data, active, replacement, totals)


def physical_controls(totals):
    parameters = set(itertools.product((6, 8, 12, 20, 32), (1, 2, 4, 8), (4, 6, 10, 20, 32)))
    parameters.update((4*index, depth, 2*index) for index in range(2, 17) for depth in (1, 5))
    examples = []
    for width, depth, tail in sorted(parameters):
        current, bands, owners, bases, shift = family(width, depth, tail)
        direct_check(*current)
        force_matching(current, totals)
        for base, size, height in bases:
            uniform_certificates(base, size, height, totals)
        vertices = set(owners)
        original, labels, _, _, kinds, _, _ = terminal_data(current, bands)
        auxiliary = [tuple(column) for band in bands for column in band if set(column) <= vertices]
        edges, portals, _ = candidate_graph(current, bands, labels, vertices)
        lower, bottom, outer = width+4, width+5, 2*depth+8+shift
        source, donor = (lower, 3+shift), (bottom, outer+4)
        relay_pairs = [{(lower, 4+shift), (lower, 5+shift)},
                       {(lower, 6+shift), (lower, 7+shift)}]
        records = components(vertices, current[3]+auxiliary)
        active = [next(record for record in records if set(record['ends']) == pair)
                  for pair in relay_pairs]
        assert all(len(record['vertices']) == 2 for record in active)
        route = [(lower, 7+shift), (bottom, outer), (lower, outer),
                 (lower, outer+1), (bottom, outer+1), (bottom, outer+2),
                 (lower, outer+2), (lower, outer+3), (bottom, outer+3), donor]
        added = [((lower, 3+shift), (lower, 4+shift)),
                 ((lower, 5+shift), (lower, 6+shift))]+list(zip(route[::2], route[1::2]))
        removed = {frozenset(edge) for edge in zip(route[1:-1:2], route[2:-1:2])}
        assert len(added) == 7 and len(removed) == 4
        assert all(frozenset(edge) in edges for edge in added)
        assert sum(frozenset(edge) in portals for edge in added) == 1
        assert removed <= {frozenset(edge) for edge in auxiliary}
        following = [edge for edge in auxiliary if frozenset(edge) not in removed]+added
        data = vertices, current[3], auxiliary, kinds, {source, donor}, {}
        chosen, signs, cycles, _ = activate(data, active)
        boundary = next(cycle for cycle in cycles if route[1] in cycle)
        assert boundary == {route[1], route[2]}
        if signs[route[1]] != 1:
            signs.update({point: -signs[point] for point in boundary})
        assert all(signs[first]+signs[second] == 0 for first, second in following)
        result = verify(data, active, following, totals, signs)
        assert (result['final']['alpha'], result['final']['beta'], result['final']['mixed']) == (0, 1, 6)
        assert len(chosen) == 6 and len(following)-len(auxiliary) == 3
        margin = (2*depth+6)*width+4*depth+7+(width+2)*(tail-4)//2
        assert original['surplus_twice']-2*original['boundary_budget'] == 2*margin and margin > 0
        totals['frozen_physical_seven_edge_repairs'] += 1
        if (width, depth, tail) in {(6, 1, 4), (32, 1, 16), (64, 5, 32)}:
            examples.append(dict(width=width, depth=depth, tail=tail,
                                 old_prescribed_port_minimum=min(tail+1, width//2+3),
                                 new_cost=7, removed=4, activated_mixed=2,
                                 final_inventory=result['final']))
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    abstract_controls(totals)
    abstract_totals = dict(totals)
    examples = physical_controls(totals)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals),
        abstract_totals=abstract_totals, examples=examples,
        scope='Finite controls for balanced whole-mixed-port activation, arbitrary complete '
              'auxiliary replacements, injective partial-payment witnesses and exact costs. '
              'All-parameter seven-edge physical construction follows from written coordinates. '
              'No seven-edge optimality, universal grid bound or global Lean claim.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
