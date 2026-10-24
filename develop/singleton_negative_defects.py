"""Complete local profile catalogue for singleton negative-source defects."""

import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path


def adjacent(corner):
    return {corner ^ 1, corner ^ 2}


def profiles():
    result = []
    for corner in range(4):
        result.append(dict(negative=False, endpoints={corner}, selected=adjacent(corner)))
        for support in adjacent(corner):
            result.append(dict(negative=True, endpoints={corner}, selected={support}))
    for endpoints in itertools.combinations(range(4), 2):
        if endpoints[1] not in adjacent(endpoints[0]):
            continue
        endpoints = set(endpoints)
        result.append(dict(negative=True, endpoints=endpoints, selected=set()))
        for selected in set(range(4))-endpoints:
            for negative in (False, True):
                result.append(dict(negative=negative, endpoints=endpoints, selected={selected}))
    for size in (3, 4):
        for endpoints in itertools.combinations(range(4), size):
            for negative in (False, True):
                result.append(dict(negative=negative, endpoints=set(endpoints), selected=set()))
    assert len(result) == 42
    return result


def packings(catalogue):
    @lru_cache(None)
    def generate(remaining):
        if not remaining:
            return ((),)
        first = remaining[0]
        result = list(generate(remaining[1:]))
        available = set(remaining)
        for index, profile in enumerate(catalogue):
            if first not in profile['endpoints'] or not profile['endpoints'] <= available:
                continue
            after = tuple(corner for corner in remaining if corner not in profile['endpoints'])
            result.extend((index, *tail) for tail in generate(after))
        return tuple(result)
    return generate(tuple(range(4)))


def inspect_local(catalogue, packing):
    current = [catalogue[index] for index in packing]
    endpoints = set.union(set(), *(profile['endpoints'] for profile in current))
    selected = set.union(set(), *(profile['selected'] for profile in current))-endpoints
    occupied = endpoints | selected
    if any(len(adjacent(corner) & occupied) > 1 for corner in selected):
        return None
    irregular = 0
    regular = 0
    reservations = 0
    negative_count = 0
    singleton_count = 0
    irregular_slots = 0
    marked_eligible = False
    for profile in current:
        size = len(profile['endpoints']), len(profile['selected'])
        is_irregular = size in {(1, 1), (2, 0)}
        events = sum(len((adjacent(corner) & endpoints)-profile['endpoints']-profile['selected'])
                     for corner in profile['endpoints'])
        if is_irregular:
            assert profile['negative']
            irregular += events
            irregular_slots += len(profile['endpoints'])
        else:
            regular += events
        if profile['negative']:
            negative_count += 1
            singleton_count += size == (1, 1)
            if size == (2, 0):
                reservations += 1
                marked_eligible |= any(adjacent(corner)-profile['endpoints']-endpoints
                                       for corner in profile['endpoints'])
    full = len(endpoints) == 4
    correction = 2*int(full and len(current) > 1)-regular
    overlap = int(negative_count >= 2 and singleton_count > 0)
    quadruple = int(singleton_count == 4)
    zero_corner = int(negative_count == singleton_count == 1 and
                      any(not profile['negative'] and len(profile['endpoints']) == 3
                          for profile in current))
    exceptional_three = int(full and any(len(profile['endpoints']) == 3 for profile in current) and
                            singleton_count == 1)
    marked = int(marked_eligible)
    assert correction >= 0
    assert irregular+marked <= correction+reservations+overlap+quadruple+zero_corner
    assert 2*(irregular-correction) <= irregular_slots+exceptional_three
    return dict(profiles=list(packing), endpoints=sorted(endpoints), selected=sorted(selected),
                negative_owners=negative_count, negative_singletons=singleton_count,
                irregular=irregular, regular=regular, correction=correction,
                reservations=reservations, maximum_bar_marked=marked,
                irregular_slots=irregular_slots, exceptional_three=exceptional_three,
                singleton_overlap=overlap, quadruple_singleton=quadruple, zero_corner=zero_corner,
                defect=max(0, irregular+marked-correction-reservations))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    catalogue = profiles()
    states = packings(catalogue)
    checked = [report for packing in states if (report := inspect_local(catalogue, packing)) is not None]
    summary = dict(signed_profiles=len(catalogue), endpoint_disjoint_packings=len(states),
                   feasible_packings=len(checked), defect_counts=dict(Counter(report['defect'] for report in checked)),
                   no_singleton_packings=sum(report['negative_singletons'] == 0 for report in checked))
    assert summary['endpoint_disjoint_packings'] == 660 and summary['feasible_packings'] == 434
    assert all(not report['defect'] for report in checked if report['negative_singletons'] == 0)
    serializable = [dict(negative=profile['negative'], endpoints=sorted(profile['endpoints']),
                         selected=sorted(profile['selected'])) for profile in catalogue]
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary, profiles=serializable,
        local=checked, scope='Complete signed LOCAL profile relaxation. Source-to-profile completeness and all-parameter tile proof are written separately. Does not certify realization of local profiles/marks by complete sources or infer a universal nonnegative global bound.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
