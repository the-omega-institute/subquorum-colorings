"""Even-length-chain subcubic family; see COMPACT_SUBCUBIC_SELECTED_STAR_GAPS.md."""


def core(length=4, port=True):
    if type(length) is not int or length < 4 or length % 2:
        raise ValueError('length must be an even integer at least four')
    n = 12*length
    graph = [set() for _ in range(n)]
    colour = {}

    def edge(a, b):
        assert a != b and b not in graph[a]
        graph[a].add(b)
        graph[b].add(a)

    for j in range(2*length):
        for t in range(6):
            colour[6*j+t] = (j % 2) ^ (j // length) ^ (t % 2)
        for t in range(5):
            edge(6*j+t, 6*j+t+1)
    for h in (0, length):
        for t in range(length-1):
            edge(6*(h+t), 6*(h+t+1)+4)
        edge(6*(h+length-1), 6*h)
        edge(6*(h+length-1), 6*(h+length-2))
    edge(4, 6*length+4)
    if port:
        edge(6, 6*(length+1))
    selected = {6*j+t for j in range(2*length) for t in (1, 2, 3, 5)}
    attaining = {6*j+t for j in range(2*length)
                 for t in ((0, 2, 3, 5) if j < length else (1, 2, 4, 5))}
    attaining.remove(6*(length-1))
    return graph, selected, attaining, colour


def base(length=4):
    graph, selected, attaining, colour = core(length)

    def edge(a, b):
        assert a != b and b not in graph[a]
        graph[a].add(b)
        graph[b].add(a)

    for j in range(length):
        other = length+(j ^ 1)
        offset = len(graph)
        graph.extend(set() for _ in range(4))
        for t in range(4):
            colour[offset+t] = colour[6*j+5] ^ (t % 2)
            edge(offset+t, offset+(t+1) % 4)
        edge(6*j+5, offset+1)
        edge(6*other+5, offset+3)
        selected.update((offset, offset+2))
        attaining.update((offset, offset+2))
    return graph, selected, attaining, colour


def family(k, length=4):
    if type(k) is not int or k < 1:
        raise ValueError('k must be a positive integer')
    h, s, d, c = base(length)
    n = len(h)
    graph = [{n*j+b for b in h[a]} for j in range(k) for a in range(n)]
    u, v = 6, 6*(length+1)
    for j in range(k):
        graph[n*j+u].remove(n*j+v)
        graph[n*j+v].remove(n*j+u)
    for j in range(k):
        a, b = n*j+v, n*((j+1) % k)+u
        graph[a].add(b)
        graph[b].add(a)
    return (graph, {n*j+a for j in range(k) for a in s},
            {n*j+a for j in range(k) for a in d},
            {n*j+a: c[a] for j in range(k) for a in c})


def spanning_ears(length=4):
    """A spanning open ear decomposition of base(length), not a graph search."""
    # Validate the parameter using the same public entry-point contract.
    if type(length) is not int or length < 4 or length % 2:
        raise ValueError('length must be an even integer at least four')

    def body(h):
        result = [6*h]
        for j in range(h+1, h+length):
            result.extend(6*j+t for t in (4, 3, 2, 1, 0))
        return result+[6*h]

    first, second = body(0), body(length)
    connector = [6, *reversed(second[:6]),
                 6*length+1, 6*length+2, 6*length+3, 6*length+4,
                 4, 3, 2, 1, 0]
    result = [first, connector, second[5:]]
    for j in range(length):
        other = length+(j ^ 1)
        o = 12*length+4*j
        result.append([6*j+4, 6*j+5, o+1, o, o+3, 6*other+5, 6*other+4])
        result.append([o+1, o+2, o+3])
    return result
