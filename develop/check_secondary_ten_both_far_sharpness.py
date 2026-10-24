"""Full-original exact sharpness counts with arbitrarily long pairs and chains."""

import json

from check_secondary_ten_arbitrary_t_consumers import old_chain
from check_secondary_ten_both_far_compensation import check_group


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    cases = []
    for pairs, far in ((1, 4), (2, 4), (5, 4), (11, 4),
                       (2, 10), (5, 10), (1, 100), (3, 100),
                       (1, 2000), (2, 2000)):
        widths, depths = [12]*(pairs+1), [far+24]*(pairs+1)
        fixed, unused, unused, sites = old_chain(31, -100, widths, depths, 6)
        choices = [(index, 6, 0, far+2, far) for index in range(1, pairs+1)]
        result = check_group(fixed, sites, widths, choices)
        assert result['exact_gain'] == 4*pairs
        assert result['new_full'] == pairs*(far//2+5)
        assert result['new_events'] == pairs*(far+12)
        cases.append(dict(pairs=pairs, consumer_far=far, receiver_far=far+2,
                          exact_gain=result['exact_gain'], new_full=result['new_full'],
                          new_events=result['new_events']))
    print(json.dumps(dict(status='PASS', cases=cases,
        scope='Exact physical full/event SETS and sharp counts for a written '
              'all-m/all-even-g family. Selected-union endpoint-disjointness '
              'only; no complete feasible extension or global equality claim.'), indent=2))


if __name__ == '__main__':
    main()
