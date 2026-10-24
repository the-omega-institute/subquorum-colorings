"""Direct original-support charge counts and complete earlier-owner separation."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import old_chain


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def counts(record):
    tiles = {(row//2, column//2) for row, column in record[0]}
    inside = {point for point in record[1] if (point[0]//2, point[1]//2) in tiles}
    return len(record[2]), len(tiles), len(inside)


def main():
    receiver_controls = consumer_controls = separated = 0
    for breadth, far, anchor, column in itertools.product(
            (6, 28, 54, 200), (4, 22, 26, 2000), (-33, 31, 49), (-101, 1, 201)):
        receiver = independent_source((breadth, 10, far), (False, False, True),
                                      (anchor-11, column+1))
        assert counts(receiver) == (breadth+4+far//2,
                                   breadth//2+5+far//2, 5+far//2)
        tiles = {(row//2, value//2) for row, value in receiver[0]}
        moved = lambda point: (anchor-11+point[0], column+1-point[1])
        expected_inside = {moved((row, 2)) for row in range(3, 10, 2)}
        expected_inside |= {moved((row, breadth-1)) for row in range(3, far, 2)}
        expected_inside |= {moved((11, 1)), moved((far+1, breadth))}
        assert {point for point in receiver[1]
                if (point[0]//2, point[1]//2) in tiles} == expected_inside
        assert all((point[0]//2, point[1]//2) not in tiles
                   for point in ((anchor-11, column+1), (anchor-11, column-breadth)))
        assert charge(receiver) == -1
        receiver_controls += 1
        consumer = independent_source((breadth, 4, far), (False, False, True),
                                      (anchor-8, column))
        assert counts(consumer) == (breadth+1+far//2,
                                   breadth+2+far//2, 4+far//2)
        tiles = {(row//2, value//2) for row, value in consumer[0]}
        moved = lambda point: (anchor-8+point[0], column-point[1])
        expected_inside = {moved((0, 0)), moved((0, breadth+1))}
        expected_inside |= {moved((row, 0)) for row in (2, 4)}
        expected_inside |= {moved((row, breadth+1)) for row in range(2, far+1, 2)}
        assert {point for point in consumer[1]
                if (point[0]//2, point[1]//2) in tiles} == expected_inside
        assert all((point[0]//2, point[1]//2) not in tiles
                   for point in (moved((5, 1)), moved((far+1, breadth))))
        assert all((point[0]//2, point[1]//2) in tiles
                   for point in ((anchor-8, column), (anchor-8, column-breadth-1)))
        assert charge(consumer) == 1-breadth
        consumer_controls += 1
    for anchor, offset, root in itertools.product((-33, 31), (-100, 0, 200), (6, 200)):
        widths = [12, 14, 20, 18, 30, 12, 50]
        depths = [24, 26, 40, 2000, 80, 24, 28]
        records, bases, unused, sites = old_chain(anchor, offset, widths, depths, root)
        size = len(sites)
        for index in range(1, size):
            origin, unused, lateral = sites[index]
            near_column = lateral+widths[index]+13
            assert near_column == sites[index-1][2]+1
            for earlier in range(index):
                for record in bases[earlier]:
                    assert min(column for row, column in record[0]) >= near_column+1
                    separated += 1
                for position in (9*size+1+earlier, 10*size+1+earlier, 11*size+1+earlier):
                    assert max(row for row, column in records[position][0]) <= origin-16
                    assert max(row//2 for row, column in records[position][0]) < (origin-11)//2
                    separated += 1
            assert min(column for row, column in records[9*size][0]) >= near_column+1
            separated += 1
    print(json.dumps(dict(status='PASS', receiver_charge_controls=receiver_controls,
        consumer_charge_controls=consumer_controls, earlier_original_controls=separated,
        scope='Exact immutable-support counts refute the proposed R positive-charge '
              'correction. General count and earlier-owner separation proofs are written; '
              'finite controls do not prove catalogue exhaustion or global allocation.'), indent=2))


if __name__ == '__main__':
    main()
