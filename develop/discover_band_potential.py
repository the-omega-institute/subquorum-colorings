#!/usr/bin/env python3
"""Discover a finite potential for the all-length two-row band theorem."""
import json


def column(index):
    return divmod(index, 3)


def cost(index):
    return sum(1 if label == 0 else -1 if label == 1 else 0 for label in column(index))


def endpoint(index):
    upper, lower = column(index)
    return upper != 1 and lower == 0


def allowed(left, middle, right):
    upper, lower = column(middle)
    upper_left, lower_left = column(left)
    upper_right, lower_right = column(right)
    return (upper != 1 or lower == upper_left == upper_right == 0) and (
        lower != 1 or sum(label != 0 for label in (upper, lower_left, lower_right)) <= 1)


def index(parity, left, current):
    return parity*81+left*9+current


def discover():
    values = [None]*162
    for current in range(9):
        if endpoint(current):
            values[index(1, 0, current)] = cost(current)
    for iteration in range(163):
        changed = False
        for parity in range(2):
            for left in range(9):
                for current in range(9):
                    value = values[index(parity, left, current)]
                    if value is None:
                        continue
                    for right in range(9):
                        if allowed(left, current, right):
                            destination = index(1-parity, current, right)
                            candidate = value+cost(right)
                            if values[destination] is None or candidate < values[destination]:
                                values[destination] = candidate
                                changed = True
        if not changed:
            break
    else:
        raise AssertionError('Negative cycle or unfinished relaxation')
    final = []
    for parity in range(2):
        for left in range(9):
            for current in range(9):
                value = values[index(parity, left, current)]
                if value is not None and endpoint(current) and allowed(left, current, 0):
                    assert value >= 2-parity
                    final.append(dict(parity=parity, left=left, current=current, minimum=value))
    return dict(potential=values, reachable=sum(value is not None for value in values),
                stabilization_round=iteration, terminal_minima=final,
                encoding='0 blank,1 selected,2 occupied; column=3*upper+lower; state=81*parity+9*left+current')


if __name__ == '__main__':
    print(json.dumps(discover(), indent=2))
