"""Exact owner and support controls for transverse-gate compensation."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_minus_one_tip_obstructions import source
from check_width_eight_u_cap_obstruction import rotor_owners
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def candidates(target, forbidden_endpoints, forbidden_occupied, parameters):
    for width, left, right in parameters:
        module = source(width, left, right)
        for symmetry in itertools.product((False, True), repeat=3):
            for endpoint in module['endpoints']:
                origin = affine(endpoint, symmetry)
                offset = target[0]-origin[0], target[1]-origin[1]
                moved = transform_module(module, symmetry, offset)
                if moved['endpoints'] & forbidden_endpoints:
                    continue
                if (moved['endpoints'] | moved['selected']) & forbidden_occupied:
                    continue
                yield (width, left, right), endpoint, symmetry, offset, moved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = list(itertools.product((6, 8, 14), (4, 6, 10), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    counts = Counter()
    tables = []
    for incident in (4, 6):
        blocked = {(row, 1) for row in range(1, 6)}
        blocked |= {(2, column) for column in range(2, incident+3)}
        blocked |= {(row, column) for row in range(2, 7) for column in (incident+1, incident+2)}
        assert rotor_owners((3, 2), blocked) == []
        tables.append(dict(target=[3, 2], incident=incident, roles=16, survivors=[]))
        for positive_height, width, far in itertools.product((4, 6, 10), (6, 14), (4, 8)):
            if incident == 6 and positive_height > 6:
                continue
            positive = source(14, positive_height, 4)
            incoming = transform_module(source(width, incident, far), (True, True, False), (1, incident+2))
            if positive['endpoints'] & incoming['endpoints']:
                continue
            forbidden = positive['endpoints'] | incoming['endpoints'] | {(positive_height+1, 1)}
            blank = {(positive_height+1, 2)}
            surviving = list(candidates((3, 2), forbidden, blank, parameters))
            counts['gate_contexts_'+str(incident)] += 1
            if incident == 4:
                assert not surviving
            for dimensions, endpoint, symmetry, offset, moved in surviving:
                width_owner, left, right = dimensions
                assert endpoint in ((left, 1), (right, width_owner))
                assert endpoint[0] == 4
                assert affine((endpoint[0]-1, endpoint[1]), symmetry, offset) == (3, 3)
                across = affine((endpoint[0], endpoint[1]+(1 if endpoint[1] == 1 else -1)), symmetry, offset)
                assert across == (4, 2)
                assert (4, 3) in moved['selected']
                cells = vertices_of({(2, 2)})
                assert cells & moved['endpoints'] == {(4, 5), (5, 5)}
                assert not cells & moved['selected']
                counts['height_six_forced_owner_controls'] += 1
    blocked = {(3, column) for column in range(2, 7)}
    blocked |= {(row, column) for row in range(4, 7) for column in (5, 6)}
    blocked |= {(4, 1), (5, 1)}
    assert rotor_owners((4, 3), blocked) == []
    tables.append(dict(target=[4, 3], roles=16, survivors=[]))
    for positive_height, width, far in itertools.product((4, 6), (6, 14), (4, 8)):
        positive = source(14, positive_height, 4)
        forced_owner = transform_module(source(width, 4, far), (True, True, False), (2, 6))
        assert not positive['endpoints'] & forced_owner['endpoints']
        forbidden = positive['endpoints'] | forced_owner['endpoints'] | {(positive_height+1, 1)}
        blank = {(positive_height+1, 2)}
        assert not list(candidates((4, 3), forbidden, blank, parameters))
        counts['second_support_contexts'] += 1
    pool_cases = strict = 0
    for zero_count, single, paid, chain, exterior, fresh in itertools.product(range(5), repeat=6):
        if paid > single:
            continue
        effective = max(paid, fresh-2*zero_count)
        assert max(2*zero_count+paid, fresh) == 2*zero_count+effective
        reserve = (single+chain+exterior+max(2*zero_count+paid, fresh)+1)//2
        margin = reserve-zero_count-single
        bound = -((single-chain-exterior-effective)//2)
        old_bound = -((single-chain-exterior-paid)//2)
        assert margin == bound >= old_bound
        strict += bound > old_bound
        pool_cases += 1
    result = dict(status='PASS', rotor_tables=tables, parameters=len(parameters),
                  constructor_controls=dict(counts), signed_pool_cases=pool_cases,
                  strictly_stronger_arithmetic_bounds=strict,
                  new_complete_physical_Y_fixture_coverage=0,
                  scope='Exact16-role rotor exclusions, representative arbitrary-image U role/support tests and signed maximum-pool arithmetic. These are local controls, not complete fused Y fixtures or a substitute for the general written proof and geometric injection.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', controls=dict(counts), pool_cases=pool_cases, strict=strict)))


if __name__ == '__main__':
    main()
