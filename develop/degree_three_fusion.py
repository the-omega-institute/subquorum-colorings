"""Physical fusions without prescribed ports or a once-used-port restriction."""

from rotor_networks import combine, transform_module, two_leg_module


def four_way_modules(width):
    assert width >= 8 and width % 2 == 0
    modules = [transform_module(two_leg_module(width, 4), (False, False, False), (-4, 0))]
    for _ in range(3):
        modules.append(transform_module(modules[-1], (True, True, False), (0, 1)))
    return [transform_module(module, (False, False, False), (width, width)) for module in modules]


def four_way(width):
    modules = four_way_modules(width)
    network = combine(modules)
    return (2*width+2, 2*width+2, network['selected'], network['matching']), modules


def corner_join(width=6):
    base = two_leg_module(width, 4)
    modules = [base, transform_module(base, (False, True, True), (0, 1))]
    modules = [transform_module(module, (False, False, False), (6, width)) for module in modules]
    network = combine(modules)
    return (12, 2*width+2, network['selected'], network['matching']), modules


def occupied_bands(width=6):
    base = two_leg_module(width, 4)
    modules = [base, transform_module(base, (False, True, False), (4, -width))]
    modules = [transform_module(module, (False, False, False), (2, width)) for module in modules]
    network = combine(modules)
    return (8, 2*width+2, network['selected'], network['matching']), modules


def occupied_band_certificate(width):
    def reflect(point):
        return 4-point[0], point[1]-width

    def reflected(witness):
        return tuple(reflect(point) for point in witness)

    certificate = [((4,width),(4,width+1),(5,width)),
                   ((2,width),(2,width+1),(3,width))]
    certificate.extend(reflected(witness) for witness in
                       [((4,1),(4,0),(5,1)),((2,1),(2,0),(3,1))])
    certificate.append(((0,width),(0,width+1),(1,width)))
    for column in range(width-1,1,-1):
        row = (width-column)%2
        certificate.append(((row,column),(1-row,column),(row,column+1)))
    certificate.append(reflected(((0,1),(0,0),(1,1))))
    for column in range(2,width):
        row = 1 if column%2 == 0 else 0
        certificate.append(reflected(((row,column),(1-row,column),(row,column-1))))
    certificate.extend([
        ((1,1),(0,1),(1,2)), ((3,0),(4,0),(3,-1)),
        ((3,1),(3,2),(2,1)), ((1,0),(1,-1),(2,0)),
        ((4,1),(5,1),(4,0)), ((0,0),(-1,0),(0,1)),
        ((2,1),(2,0),(3,1)), ((2,0),(2,1),(1,0)),
        ((0,1),(0,0),(1,1)), ((4,0),(4,1),(3,0))])
    for column in range(2,width):
        row = 1 if column%2 == 0 else 0
        certificate.append(((row,column),(1-row,column),(row,column-1)))
    for column in range(width-1,1,-1):
        row = (width-column)%2
        certificate.append(reflected(((row,column),(1-row,column),(row,column+1))))
    certificate.extend([((1,width),(0,width),(1,width-1)),
                        reflected(((1,1),(0,1),(1,2))),
                        ((3,width),(3,width-1),(2,width)),
                        reflected(((3,1),(3,2),(2,1)))])
    return [tuple((row+2,column+width) for row,column in witness) for witness in certificate]
