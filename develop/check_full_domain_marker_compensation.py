"""Check payment markers when selected source and donor tails are rematched."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory, matchings
from check_mixed_relay_orientation import forest_budget
from check_native_guard_compensation import force_matching
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import components, terminal_data
from check_zero_capacity_gap_beta_compensation import barrier_family


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def physical_sign(kind):
    return -1 if kind == 'TP' else 1


def full_signs(vertices, actual, auxiliary, kinds, chosen, payments):
    adjacency = defaultdict(list)
    for index, (first, second) in enumerate(actual+auxiliary):
        adjacency[first].append((second, index))
        adjacency[second].append((first, index))
    colours, cycles, markers = {}, [], {}
    for record in components(vertices, actual+auxiliary):
        ends = record['ends']
        start = min(ends or record['vertices'])
        defect = None
        if ends:
            selected = set(ends) & chosen
            assert len(selected) <= 1
            initial = physical_sign(kinds[start]) * (1 if start in chosen else -1)
            if not selected and all(kinds[point] == 'TP' for point in ends):
                paid = next(point for point in ends if point in payments)
                defect = adjacency[paid][0][1]
                edge = frozenset(actual[defect])
                markers[edge] = paid, payments[paid]
            elif not selected and all(kinds[point] == 'BP' for point in ends):
                defect = adjacency[start][0][1]
        else:
            initial = 1
            cycles.append(set(record['vertices']))
        current, previous, sign = start, None, initial
        while current not in colours:
            colours[current] = sign
            following = [(point, index) for point, index in adjacency[current] if index != previous]
            if not following:
                break
            point, index = following[0]
            sign *= 1 if index == defect else -1
            previous, current = index, point
        if not ends:
            assert current == start and sign == initial
    assert set(colours) == set(vertices)
    assert all(colours[point] == physical_sign(kind)*(1 if point in chosen else -1)
               for point, kind in kinds.items())
    assert all(colours[first]+colours[second] == 0 for first, second in auxiliary)
    assert {frozenset(edge) for edge in actual
            if colours[edge[0]] == colours[edge[1]] == 1} == set(markers)
    return colours, cycles, markers


def model(sources, source_sizes, donor_sizes, relays, paid_ends, chosen_ends, cycle_pairs):
    vertices, actual, auxiliary, kinds, chosen, payments = set(), [], [], {}, set(), {}
    specifications = [('alpha', size, True) for size in source_sizes]
    specifications += [('beta', size, True) for size in donor_sizes]
    specifications += [(kind, size, False) for kind, size in relays]
    selected_index = paid_index = 0
    for index, (kind, size, selected) in enumerate(specifications):
        path = [('path', index, position) for position in range(2*size+2)]
        vertices.update(path)
        actual += list(zip(path[::2], path[1::2]))
        auxiliary += list(zip(path[1:-1:2], path[2:-1:2]))
        kinds[path[0]] = 'BP' if kind == 'beta' else 'TP'
        kinds[path[-1]] = 'TP' if kind == 'alpha' else 'BP'
        if selected:
            chosen.add(path[0] if chosen_ends[selected_index] == 0 else path[-1])
            selected_index += 1
        elif kind == 'alpha':
            paid = path[0] if paid_ends[paid_index] == 0 else path[-1]
            payments[paid] = index
            paid_index += 1
    if cycle_pairs:
        cycle = [('cycle', 0, position) for position in range(2*cycle_pairs)]
        vertices.update(cycle)
        auxiliary += list(zip(cycle[::2], cycle[1::2]))
        actual += [(cycle[2*position+1], cycle[(2*position+2) % len(cycle)])
                   for position in range(cycle_pairs)]
    assert len(chosen) == 2*sources
    return vertices, actual, auxiliary, kinds, chosen, payments


def verify(data, replacement, totals, exhaustive_flips=True):
    vertices, actual, auxiliary, kinds, chosen, payments = data
    free = set(kinds)-chosen
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices-free
    colours, cycles, markers = full_signs(*data)
    original = inventory(components(vertices, actual+auxiliary), kinds)
    records = components(vertices, actual+replacement)
    final = inventory(records, {point:kinds[point] for point in free})
    used, unpaid = set(), []
    for record in records:
        if not record['ends'] or not all(kinds[point] == 'TP' for point in record['ends']):
            continue
        local = [edge for edge in markers if edge <= record['vertices']]
        if local:
            point, unit = markers[local[0]]
            assert point in record['ends'] and point in free and unit not in used
            used.add(unit)
        else:
            unpaid.append(record)
    assert len(used)+len(unpaid) == final['alpha']
    sources = len(chosen)//2
    paid = original['alpha']-sources
    betas = original['beta']-sources
    minimum = len(replacement)
    orientations = (itertools.product((-1,1), repeat=len(cycles)) if exhaustive_flips else
                    [tuple(-1 if position == flipped else 1 for position in range(len(cycles)))
                     for flipped in range(-1,len(cycles))])
    for flips in orientations:
        signs = dict(colours)
        for cycle, flip in zip(cycles, flips):
            signs.update({point:colours[point]*flip for point in cycle})
        negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
        positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
        assert negative == positive
        assert final['alpha'] <= paid+negative and final['beta'] <= betas+negative
        assert len(unpaid) <= negative
        witnesses = set()
        for record in unpaid:
            errors = [frozenset(edge) for edge in replacement if set(edge) <= record['vertices']
                      and signs[edge[0]] == signs[edge[1]] == -1]
            assert errors and errors[0] not in witnesses
            witnesses.add(errors[0])
        for record in records:
            local = record['vertices']
            new_ends = [point for edge in replacement if edge[0] in local for point in edge]
            old_ends = [point for edge in actual if edge[0] in local for point in edge]
            assert Counter(new_ends+list(free & local)) == Counter(old_ends)
            charge = sum(signs[point] for point in new_ends)-sum(signs[point] for point in old_ends)
            assert charge == sum(physical_sign(kinds[point]) for point in record['ends'])
        if negative == 0:
            assert not unpaid
            cancelled = paid-final['alpha']
            assert 0 <= cancelled <= min(paid,betas)
            assert final['beta'] == betas-cancelled
            assert final['mixed'] == original['mixed']+sources+2*cancelled
            totals['coherent_full_domain_certificates'] += 1
        minimum = min(minimum,negative)
        totals['signed_full_domain_controls'] += 1
    errors, rank = forest_budget(replacement,colours,cycles,{'alpha':len(unpaid)})
    if exhaustive_flips:
        assert (errors == 0) == (minimum == 0)
    elif minimum == 0:
        assert errors == 0
    assert final['beta']-final['alpha'] == original['beta']-original['alpha']
    assert sum(final[key] for key in ('alpha','beta','mixed')) == sum(original[key] for key in ('alpha','beta','mixed'))-sources
    selected_support = set().union(*(record['vertices'] for record in components(vertices, actual+auxiliary)
                                     if set(record['ends']) & chosen))
    removed = {frozenset(edge) for edge in auxiliary}-{frozenset(edge) for edge in replacement}
    if any(edge <= selected_support for edge in removed):
        totals['selected_tail_internal_rematchings'] += 1
    totals['full_domain_replacements'] += 1
    totals['transported_payment_occurrences'] += len(used)
    totals['marker_free_alpha_occurrences'] += len(unpaid)
    return dict(original=original, final=final, sampled_minimum_error_pairs=minimum,
                cycle_flips_exhaustive=exhaustive_flips, forest_rank=rank)


def physical_controls(totals):
    examples = []
    for width, depth in itertools.product((6,8,12,20),(1,2,4,8,16)):
        current,bands,_,_,shift = barrier_family(width,depth,True)
        direct_check(*current)
        force_matching(current,totals)
        vertices = {point for edge in current[3] for point in edge}
        assert frozen_certificate(current)[0] == vertices
        original,_,_,_,kinds,_,_ = terminal_data(current,bands)
        auxiliary = [tuple(column) for columns in bands for column in columns if set(column)<=vertices]
        outer = 2-2*depth+shift
        removed = {frozenset(((4,column),(5,column))) for column in (outer,outer-1)}
        added = [((5,3+shift),(4,outer)),((5,outer),(5,outer-1)),((4,outer-1),(4,outer-2))]
        source, donor = added[0][0], added[-1][-1]
        chosen = {source,donor}
        paths = components(vertices,current[3]+auxiliary)
        donor_path = next(record for record in paths if donor in record['ends'])
        assert all(kinds[point] == 'BP' for point in donor_path['ends'])
        assert any(edge <= donor_path['vertices'] for edge in removed)
        following = [edge for edge in auxiliary if frozenset(edge) not in removed]+added
        corridor = {(row,column) for row in (4,5) for column in range(outer+1,3+shift)}
        assert len(corridor) == 4*depth and len(corridor & current[2]) == 2*depth
        assert not corridor & vertices
        for column in range(outer+1,3+shift):
            assert sum((row,column) in current[2] for row in (4,5)) == 1
        assert all(abs(first[0]-second[0])+abs(first[1]-second[1]) == 1 for first,second in added[1:])
        result = verify((vertices,current[3],auxiliary,kinds,chosen,{}),following,totals,
                        exhaustive_flips=False)
        assert result['sampled_minimum_error_pairs'] == 0 and result['forest_rank'] <= 1
        assert (result['final']['alpha'],result['final']['beta'],result['final']['mixed']) == (0,1,8)
        assert original['surplus_twice']-2*original['boundary_budget'] == 2*((2*depth+6)*width+4*depth+7)
        totals['frozen_physical_unprotected_beta_tail_repairs'] += 1
        if width == 6 and depth in (1,16):
            examples.append(dict(width=width,depth=depth,source=source,donor=donor,
                                 removed=[sorted(edge) for edge in removed],added=added,**result))
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--max-covered',type=int,choices=(8,10),default=8)
    arguments = parser.parse_args()
    totals = Counter()
    for sources in (1,2):
        sizes = itertools.product(range(3),repeat=2*sources)
        for sizes_tuple in sizes:
            for relays in ((),(('mixed',0),),(('mixed',1),),(('alpha',0),),(('alpha',1),),
                           (('beta',0),),(('beta',1),),(('alpha',0),('beta',0))):
                for cycle_pairs in (0,1,2):
                    if 2*(sources+sum(sizes_tuple)+sum(size for _,size in relays)+cycle_pairs) > arguments.max_covered:
                        continue
                    for chosen_ends in itertools.product((0,1),repeat=2*sources):
                        for paid_ends in itertools.product((0,1),repeat=sum(kind=='alpha' for kind,_ in relays)):
                            data = model(sources,sizes_tuple[:sources],sizes_tuple[sources:],relays,paid_ends,chosen_ends,cycle_pairs)
                            vertices,_,_,kinds,chosen,_ = data
                            for replacement in matchings(sorted(vertices-(set(kinds)-chosen))):
                                if 2*len(replacement) == len(vertices)-len(kinds)+len(chosen):
                                    verify(data,replacement,totals)
    print(json.dumps(dict(stage='abstract',totals=dict(totals)),sort_keys=True),flush=True)
    examples = physical_controls(totals)
    report = dict(status='PASS',max_covered=arguments.max_covered,totals=dict(totals),physical_examples=examples,
                  scope='Full original actual matching, no tail contraction or selected-tail protection. '
                  'All complete N up to max_covered, selected source/donor paths through '
                  'two PP pairs, both chosen ends, optional paid alpha/beta/mixed relays and cycles '
                  'through two pairs, exhaustive cycle flips in abstract controls. Physical controls '
                  'check the base and individual cycle flips plus the forest assignment, rather '
                  'than enumerating all independent original two-edge cycle orientations. '
                  'Physical reflected all-length repair controls certify unchanged '
                  'M, feasible fully frozen uniquely matched grids, zero-BT corridor witness and '
                  'rematching inside the selected beta. General graph proof is written; no new Lean '
                  'execution, universal route existence or scalar improvement is claimed.')
    arguments.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),sort_keys=True))


if __name__ == '__main__':
    main()
