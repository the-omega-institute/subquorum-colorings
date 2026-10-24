"""Explicit coordinate constructors for branched leaf-splice networks."""

from check_leaf_spliced_networks import module_record
from check_two_leg_corner_obstruction import two_leg_case


def affine(point, symmetry, offset=(0, 0)):
    transpose, flip_row, flip_column = symmetry
    row, column = point
    row = -row if flip_row else row
    column = -column if flip_column else column
    if transpose:
        row, column = column, row
    return row+offset[0], column+offset[1]


def labeled_module(selected, matching, ports, guard=None):
    record = module_record(selected, matching)
    record.update(ports=set(ports), guard=guard)
    return record


def transform_module(module, symmetry, offset=(0, 0)):
    move = lambda point: affine(point, symmetry, offset)
    guard = tuple(move(point) for point in module['guard']) if module['guard'] else None
    return labeled_module({move(point) for point in module['selected']},
                          [tuple(move(point) for point in edge) for edge in module['matching']],
                          {move(point) for point in module['ports']}, guard)


def two_leg_module(width, height):
    current, _ = two_leg_case(width, height, height)
    return labeled_module(current[2], current[3], {(height, 1), (height, width)},
                          ((3, 2), (3, 1), (2, 3), (1, 3)))


def rotor():
    selected = {(0, 2), (1, 1), (2, 5), (1, 4), (5, 3), (4, 4), (3, 0), (4, 1)}
    matching = [((2, 2), (1, 2)), ((2, 3), (2, 4)),
                ((3, 3), (4, 3)), ((3, 2), (3, 1))]
    return labeled_module(selected, matching, {(1, 2), (2, 4), (4, 3), (3, 1)})


def combine(modules, ports=()):
    endpoints = set.union(*(module['endpoints'] for module in modules))
    selected = set.union(*(module['selected'] for module in modules))-endpoints
    matching = [edge for module in modules for edge in module['matching']]
    return labeled_module(selected, matching, ports)


def star_modules(width=6):
    base = two_leg_module(width, 4)
    adapters = [((False, False, False), (-4, 2-width)),
                ((True, True, False), (2-width, 9)),
                ((False, True, False), (9, 2)),
                ((True, False, False), (2, -4))]
    return [rotor()]+[transform_module(base, symmetry, offset) for symmetry, offset in adapters]


def star(width=6):
    return combine(star_modules(width),
                   {(0, 3-width), (3-width, 5), (5, width+2), (width+2, 0)})


def chain_modules(amount):
    assert amount >= 1
    base = star_modules(14)
    connector = transform_module(two_leg_module(14, 4), (True, False, False), (-25, 0))
    modules = []
    for index in range(amount):
        symmetry = False, False, bool(index % 2)
        offset = -40*index, 5 if index % 2 else 0
        modules.extend(transform_module(module, symmetry, offset) for module in base)
        if index+1 < amount:
            modules.append(transform_module(connector, symmetry, offset))
    shift = 12+40*(amount-1), 12
    return [transform_module(module, (False, False, False), shift) for module in modules]


def chain(amount):
    modules = chain_modules(amount)
    network = combine(modules)
    return (40*amount-10, 30, network['selected'], network['matching']), modules
