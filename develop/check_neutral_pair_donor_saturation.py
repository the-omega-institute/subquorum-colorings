"""Check a zero-charge neighbor that saturates a completed local unit donor."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_even_bridge_support_completion import bridge_cuts, completed, endpoints_of, tiles_of
from check_native_guard_compensation import charge, check_forcing_template, force_matching, pieces
from check_residual_corridors import direct_check, transformed
from search_corner_coverage import witnesses


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def neutral_pair(width, height):
    outer = elbow(width, height, {(2, 2)})
    outer_endpoints = endpoints_of(outer)
    pair_endpoints = {(7, 5), (8, 5)}
    selected = (outer[2] | {(6, 5), (7, 6), (8, 4), (9, 5)})
    selected -= outer_endpoints | pair_endpoints
    current = *outer[:2], selected, outer[3]+[((7, 5), (8, 5))]
    return current, outer_endpoints, pair_endpoints


def inspect(current, totals):
    objective = direct_check(*current)
    assert min(occupied_degrees(current).values()) >= 3
    endpoints = endpoints_of(current)
    cuts = [(first, second) for first, second, side, _ in bridge_cuts(endpoints)
            if len(side) % 2 == 0]
    assert len(cuts) == 1
    cores = pieces(current)
    assert len(cores) == 2
    assert sorted(charge(core) for core in cores) == [0, 1]
    assert charge(current) == 1
    for candidate in (current, *cores):
        force_matching(candidate, totals)
    empty_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    empty_tiles -= tiles_of(endpoints)
    deficit = sum(2-len(current[2] & vertices_of({tile})) for tile in empty_tiles)
    assert deficit >= 2
    margin = current[0]*current[1]//2-objective
    assert margin == deficit-1 and margin >= 1
    totals['models'] += 1
    return dict(completed_charges=sorted(charge(core) for core in cores),
                original_deficit=deficit, original_margin=margin, objective=objective)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    reference = None
    for width in range(6, 31, 2):
        for height in range(4, 21, 2):
            current, outer_endpoints, pair_endpoints = neutral_pair(width, height)
            contacts = {(point, other) for point in outer_endpoints
                        for other in set(neighbors(point)) & pair_endpoints}
            assert contacts == {((6, 5), (7, 5))}
            outer = completed(current, outer_endpoints, {(7, 5)})
            pair = completed(current, pair_endpoints, {(6, 5)})
            check_forcing_template(width, height, outer, (4, 5), totals)
            assert pair[2] == {(6, 5), (7, 6), (8, 4), (9, 5)}
            assert len(tiles_of(outer_endpoints)) == width//2+height+1
            assert len(outer[2] & vertices_of(tiles_of(outer_endpoints))) == height+4
            assert len(tiles_of(pair_endpoints)) == 2
            assert len(pair[2] & vertices_of(tiles_of(pair_endpoints))) == 3
            assert charge(outer) == 1 and charge(pair) == 0
            donor = vertices_of({(3, 3)})
            relay = vertices_of({(4, 3)})
            assert not donor & (outer_endpoints | pair_endpoints)
            assert donor & outer[2] == {(6, 7)}
            assert donor & current[2] == {(6, 7), (7, 6)}
            assert not relay & (outer_endpoints | pair_endpoints | current[2])
            assert any(tuple(witness['square']) == (6, 6)
                       for witness in witnesses(*outer[:2], outer[2], outer_endpoints))
            assert len(current[2]) == height+7 and len(current[3]) == width+height
            assert len(tiles_of(outer_endpoints | pair_endpoints)) == width//2+height+2
            assert len(current[2] & vertices_of(tiles_of(outer_endpoints | pair_endpoints))) == height+5
            record = inspect(current, totals)
            assert record['objective'] == width+2*height+7
            assert record['original_deficit'] == current[0]*current[1]//2-width-2*height-6
            totals['parameter_pairs'] += 1
            if (width, height) == (6, 4):
                reference = dict(parameters=[width, height], shape=list(current[:2]),
                                 selected=sorted(current[2]), matching=current[3], **record,
                                 lost_donor_tile=[3, 3], lost_donor_original_deficit=0,
                                 lost_donor_completed_deficit=1, relocated_donor_tile=[4, 3],
                                 relocated_original_deficit=2)
            if width in (6, 30) and height in (4, 20):
                for symmetry in itertools.product((False, True), repeat=3):
                    shape, selected, matching = transformed(*current, *symmetry)
                    image = *shape, selected, matching
                    image_record = inspect(image, totals)
                    assert image_record == record
                    totals['symmetry_images'] += 1
    assert totals['parameter_pairs'] == 117 and totals['symmetry_images'] == 32
    assert reference['original_deficit'] == 88 and reference['original_margin'] == 87
    report = dict(status='PASS', controls=dict(totals), reference=reference,
                  scope='Finite controls for the all-parameter written neutral-pair saturation theorem. '
                  'Unique matching checked by leaf elimination and complete retained-neighbor freezing; '
                  'both final core charges nonnegative. Refutes two payment rules, not the target. '
                  'The relocated blank donor is established for this explicit family only.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], controls=report['controls'])))


if __name__ == '__main__':
    main()
