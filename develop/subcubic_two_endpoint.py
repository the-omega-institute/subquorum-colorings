"""Two endpoint credits and paired class margins for the 15/152 bound."""
from collections import Counter
from fractions import Fraction
from subcubic_partial_template import decompose, layers, one_side
from subcubic_phase_pairing import expectation
from subcubic_joint_margin import resources as preceding_resources
from subcubic_zero_budget_repair import components, restriction
from subcubic_intrinsic_obstruction import path_cycle_optimum


def endpoint_events(word):
    """Return endpoint pieces when BOTH initial literal runs have length<=2.

    word entries are (phase_group, retention_bit). None marks a bad path.
    The whole P1/P2 event is included once, never once per endpoint.
    """
    n=len(word)
    assert n>0
    orders=[list(range(n))] if n==1 else [list(range(n)),list(reversed(range(n)))]
    events=[]
    for order in orders:
        run=1
        while run<n and word[order[run]]==word[order[0]]:run+=1
        if run>2:return None
        prefix=set(order[:run]);requirements=dict([word[order[0]]])
        boundary=order[run] if run<n else None
        if boundary is not None:
            j,bit=word[boundary]
            assert j not in requirements or requirements[j]==1-bit
            requirements[j]=1-bit
        row=dict(prefix=prefix,boundary=boundary,requirements=requirements,
                 delta=Fraction((-2*run)%3,3))
        if not any(old['prefix']==prefix and old['requirements']==requirements for old in events):events.append(row)
    assert sum(row['delta']/2**len(row['requirements']) for row in events)>=Fraction(1,6)
    return events


def resources(m):
    # Reuse the exact accepted pairing, margins and good auxiliary components;
    # rebuild all physical-path ownership for the TWO-endpoint classification.
    res=preceding_resources(m)
    inverse={c:x for x,c in m['owner'].items()}
    def literal(v):
        x=inverse[v];return m['group'][x],1-m['colour'][x]
    events=[];bad=[];paths=[];counts=Counter();tg=0
    for K in components(m['g'],m['C']):
        ends=sorted(v for v in K if len(m['g'][v]&K)<=1)
        if not ends:continue
        order=[];previous=None;current=ends[0]
        while current is not None:
            order.append(current)
            nxt=sorted((m['g'][current]&K)-({previous} if previous is not None else set()))
            previous,current=current,nxt[0] if nxt else None
        assert set(order)==K
        word=[literal(v) for v in order];raw=endpoint_events(word)
        if raw is None:
            choices=[order,list(reversed(order))]
            prefix=next(seq[:3] for seq in choices if len(seq)>=3 and len({literal(v) for v in seq[:3]})==1)
            j,bit=literal(prefix[0]);key=j,1-bit
            counts[key]+=1;bad.append(dict(K=K,triple=set(prefix),key=key))
            paths.append(dict(K=K,order=order,good=False,events=[]))
        else:
            tg+=1;converted=[]
            for row in raw:
                converted.append(dict(K=K,prefix={order[v] for v in row['prefix']},
                    boundary=order[row['boundary']] if row['boundary'] is not None else None,
                    requirements=row['requirements'],delta=row['delta']))
            events+=converted;paths.append(dict(K=K,order=order,good=True,events=converted))
    used=set();rows=[]
    for row in bad:
        assert not row['triple']&used;used|=row['triple']
    for old in res['classes']:
        key=old['key'];c=res['pairing']['classes'][key];p=counts[key];M=old['margin']
        triples=set().union(*(row['triple'] for row in bad if row['key']==key))
        mixed=set().union(*(s for s,cost in c['mixed']))
        assert len(triples)==3*p and triples<=c['remaining']
        assert not triples&(mixed|c['monochromatic'])
        if c['distinguished']:assert 2*p<=12*M
        else:assert M>=Fraction(p,4)
        rows.append(dict(key=key,margin=M,p=p,f=old['f'],
                         distinguished=c['distinguished'],triple_vertices=triples))
    by_key={row['key']:row for row in rows};component_rows=[]
    for j,(order,cyclic) in enumerate(zip(m['components'],m['cyclic'])):
        pair=[by_key[j,bit] for bit in (0,1)]
        if pair[0]['distinguished']:continue
        margin=sum(row['margin'] for row in pair);p=sum(row['p'] for row in pair)
        flag=sum(row['f'] for row in pair)
        assert flag in (0,1) and not (cyclic and flag)
        assert len(res['pairing']['classes'][j,0]['U'])==len(res['pairing']['classes'][j,1]['U'])
        assert 2*p+2*flag<=12*margin
        component_rows.append(dict(j=j,p=p,flag=flag,margin=margin,
            class_order=len(res['pairing']['classes'][j,0]['U'])))
    tb=len(bad);assert 2*tb+2*res['sb']<=12*res['sigma']
    res.update(events=events,bad_paths=bad,classes=rows,component_margins=component_rows,
               physical_paths=paths,tg=tg,tb=tb)
    return res


def template_certificate(m):
    res = resources(m); replaced = set(); goodX = set()
    for row in res['good_components']:
        sub = row['model']
        alternatives = [one_side(sub, bit)[0] for bit in (0, 1)]
        best = max(alternatives, key=lambda d: (len(d), sorted(d)))
        assert 4*len(best) >= 11*row['b']
        replaced |= best; goodX |= row['X']
    rem = restriction(m, m['X']-goodX)
    rres = resources(rem); assert rres['sigma'] == res['sigma']
    assert rres['tg'] == res['tg'] and not rres['good_components']
    pairing = rres['pairing']
    terms = pairing['terms']+[(r['delta'], r['requirements']) for r in rres['events']]
    initial = expectation(terms, {})
    assert initial >= -pairing['rho']+Fraction(res['tg'], 6)
    fixed, steps = {}, [initial]
    for j in range(len(rem['components'])):
        values = [expectation(terms, fixed | {j: bit}) for bit in (0, 1)]
        fixed[j] = int(values[1] > values[0]); steps.append(max(values))
        assert steps[-1] >= steps[-2]
    Y = {x for x in rem['X'] if rem['colour'][x] == fixed[rem['group'][x]]}
    A = rem['C']-{rem['owner'][x] for x in Y}
    core = path_cycle_optimum(m['g'], A)
    assert Fraction(len(core))-Fraction(2*len(rem['I']), 3) >= steps[-1]
    repaired = replaced | rem['I'] | Y | core
    b, o, sigma = len(m['I']), res['pairing']['odd'], res['sigma']
    assert len(repaired) >= Fraction(5*b, 2)+Fraction(o, 3)+sigma+Fraction(res['bG'], 4)+Fraction(res['tg'], 6)
    first, second = [one_side(m, bit)[0] for bit in (0, 1)]
    assert max(len(first), len(second)) >= Fraction(11*b, 4)-Fraction(o, 2)
    best = max((first, second, repaired), key=lambda d: (len(d), sorted(d)))
    assert 5*len(best) >= 13*b+3*sigma+Fraction(3*res['bG']+2*res['tg'], 4)
    return best, dict(resources=res, remainder=rem, remainder_resources=rres,
                      terms=terms, initial=initial, phases=fixed, steps=steps,
                      A=A, core=core, alternatives=(first, second, repaired))


def full_certificate(g, S, colour, beta):
    w = decompose(g, S)
    m = layers(g, w['C0'], w['I0'], w['X0'], w['owner'], w['centre'], colour)
    inner, template = template_certificate(m)
    res = template['resources']; sigma = res['sigma']
    retained = (w['R']-w['I0']) | {ell for c, ell, x in w['triples']}
    lifted = inner | retained
    H = m['I'] | m['C'] | m['X']; exterior = set(range(len(g)))-H
    boundary = {tuple(sorted((v, u))) for v in H for u in g[v]-H}
    by_layer = {name: sum(len(g[v]-H) for v in m[name]) for name in ('I', 'C', 'X')}
    p, u, a, b, b3 = len(w['triples']), len(w['pairs']), w['a'], w['b'], w['b3']
    minimum = min(a, p); alpha, pi = a-minimum, p-minimum
    e, r = u-a-2*b, len(w['R'])-a-b
    q = len(g)-len(S)-p-u; d = len(S)-beta; tau = minimum+b-2*d
    bp = len(m['I']); Z = 5*beta-5*len(retained)-13*bp
    assert bp == b-b3 and e >= b3
    assert all(v >= 0 for v in (alpha, pi, e, r, q, tau, Z))
    assert Z >= 3*sigma+Fraction(3*res['bG']+2*res['tg'], 4)
    assert by_layer['C'] <= 2*(res['tg']+res['tb'])
    assert by_layer['X'] <= 2*(res['sg']+res['sb'])
    assert by_layer['I'] <= 3*q
    B = len(boundary)
    assert B == sum(by_layer.values())
    forbidden = set().union(*(g[v] & exterior for v in inner))
    outer = [{v for v in exterior-forbidden if colour[v] == bit} for bit in (0, 1)]
    assert sum(map(len, outer)) >= len(exterior)-B
    externals = tuple(inner | part for part in outer)
    assert beta >= max(map(len, externals))
    assert beta >= Fraction(len(g), 2)+Fraction(bp, 10)+3*sigma/5-Fraction(18*res['tg']+2*res['bG'], 20)-res['tb']-res['sb']-Fraction(3*q, 2)
    assert 2*beta-len(g)-Fraction(bp, 5) == -2*minimum-alpha-pi+r-2*e-3*b3-q+Fraction(2*Z, 5)
    W = r+2*q+4*Z-(2*minimum+alpha+pi+2*e+3*b3)
    assert W >= 0
    terms = [W, 29*r, 71*(alpha+pi), 42*(e-b3), 13*b3, 28*q, 142*tau]
    assert all(v >= 0 for v in terms)
    assert sum(terms) == 30*len(g)-304*d
    assert 152*d <= 15*len(g)
    best = max((lifted, *externals), key=lambda t: (len(t), sorted(t)))
    return best, dict(witnesses=w, template=m, template_data=template,
        inner=inner, retained=retained, alternatives=(lifted, *externals),
        boundary=boundary, boundary_by_layer=by_layer, nonnegative_terms=terms,
        counts=dict(p=p, u=u, a=a, b=b, b3=b3, m=minimum, alpha=alpha, pi=pi,
                    e=e, r=r, q=q, d=d, tau=tau, Z=Z, W=W))
