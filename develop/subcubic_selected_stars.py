"""Explicit bipartite subcubic selected-star examples; see the accompanying proof."""

PAIRS = ((1, 8), (2, 9), (3, 6), (4, 7))


def base():
    g = [set() for _ in range(90)]
    colours = {}

    def edge(a, b):
        assert a != b and b not in g[a]
        g[a].add(b)
        g[b].add(a)

    for j in range(10):
        colour = (0, 1, 1, 0, 0)[j % 5] ^ (j // 5)
        for a in range(6):
            colours[6*j+a] = colour ^ (a % 2)
        for a in range(5):
            edge(6*j+a, 6*j+a+1)
    for h in (0, 5):
        for a, b in ((0, 1), (0, 2), (1, 3), (1, 4)):
            edge(6*(h+a), 6*(h+b)+4)
        for a, b in ((2, 3), (2, 4)):
            edge(6*(h+a), 6*(h+b))
    edge(4, 34)
    selected = {6*j+a for j in range(10) for a in (1, 2, 3, 5)}
    attaining = {6*j+a for j in range(10)
                 for a in ((0, 2, 3, 5) if j < 5 else (1, 2, 4, 5))} - {18}
    for t, (j, k) in enumerate(PAIRS):
        o = 60+4*t
        for a in range(4):
            colours[o+a] = colours[6*j+5] ^ (a % 2)
            edge(o+a, o+(a+1) % 4)
        edge(6*j+5, o+1)
        edge(6*k+5, o+3)
        selected.update((o, o+2))
        attaining.update((o, o+2))
    for t, j in enumerate((0, 5)):
        o = 76+7*t
        for a in range(7):
            colours[o+a] = colours[6*j] ^ (a % 2)
        for a in range(5):
            edge(o+a, o+a+1)
        for a, b in ((o+6, o+3), (o+6, o+5), (o+6, 6*j+5)):
            edge(a, b)
        selected.update(o+a for a in (1, 2, 3, 5))
        attaining.update(o+a for a in (0, 2, 3, 5))
    edge(76, 83)
    return g, selected, attaining, colours


def family(k):
    if not isinstance(k, int) or k < 1:
        raise ValueError('k must be a positive integer')
    h, s, d, c = base()
    g = [set() for _ in range(90*k)]
    for j in range(k):
        for a in range(90):
            g[90*j+a] = {90*j+b for b in h[a]}
        g[90*j+76].remove(90*j+83)
        g[90*j+83].remove(90*j+76)
    for j in range(k):
        a, b = 90*j+83, 90*((j+1) % k)+76
        g[a].add(b)
        g[b].add(a)
    return (g, {90*j+a for j in range(k) for a in s},
            {90*j+a for j in range(k) for a in d},
            {90*j+a: c[a] for j in range(k) for a in c})
