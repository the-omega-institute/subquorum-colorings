"""Opposed two-leg chambers with unbounded harmless degree-four contacts."""

from rotor_networks import combine, transform_module, two_leg_module


def opposed_modules(width, height):
    assert width >= 6 and width % 2 == 0
    assert height >= 4 and height % 2 == 0
    modules = [two_leg_module(width, height),
               transform_module(two_leg_module(width+2, height+2),
                                (False, True, False), (height+2, -1))]
    return [transform_module(module, (False, False, False), (1, 1)) for module in modules]


def opposed_bands(width, height):
    modules = opposed_modules(width, height)
    network = combine(modules)
    return (height+4, width+4, network['selected'], network['matching']), modules


def opposed_band_certificate(width, height):
    certificate = []
    sides = ((0, 1, -1, 2), (width+1, width, width+2, width-1))
    for outer, inner, exterior, interior in sides:
        certificate.append(((0, outer), (-1, outer), (0, exterior)))
        for row in range(2, height+1, 2):
            certificate.append(((row, outer), (row-1, outer), (row, exterior)))
        for row in range(3, height, 2):
            certificate.append(((row, inner), (row, outer), (row, interior)))
        certificate.append(((height+2, outer), (height+1, outer), (height+2, exterior)))
        certificate.append(((height+1, inner), (height, inner), (height+1, outer)))
    for column in range(2, width+1):
        row = height+2 if column % 2 == 0 else height+1
        other = 2*height+3-row
        certificate.append(((row, column), (other, column), (row, column-1)))
    for column in range(width-1, 0, -1):
        row = height+2 if column % 2 else height+1
        other = 2*height+3-row
        certificate.append(((row, column), (other, column), (row, column+1)))
    for outer, inner, exterior, interior in sides:
        certificate.append(((height+1, outer), (height+2, outer), (height+1, inner)))
        for row in range(height, 1, -2):
            certificate.append(((row, inner), (row, outer), (row+1, inner)))
            certificate.append(((row-1, outer), (row-1, inner), (row, outer)))
        certificate.append(((0, inner), (0, outer), (1, inner)))
    for column in range(2, width):
        row = 1 if column % 2 == 0 else 0
        certificate.append(((row, column), (1-row, column), (row, column-1)))
    for column in range(width-1, 1, -1):
        row = column % 2
        certificate.append(((row, column), (1-row, column), (row, column+1)))
    for outer, inner, exterior, interior in sides:
        certificate.append(((1, inner), (0, inner), (1, interior)))
    return [tuple((row+1, column+1) for row, column in witness) for witness in certificate]
