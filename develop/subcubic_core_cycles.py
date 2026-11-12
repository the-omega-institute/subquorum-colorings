"""Correlated square corrections and cycle-length certificates."""
from fractions import Fraction
from itertools import product
from subcubic_partial_template import decompose,layers
from subcubic_intrinsic_obstruction import path_cycle_optimum


def components(g,allowed):
    unseen=set(allowed);answer=[]
    while unseen:
        start=min(unseen);found={start};todo=[start]
        while todo:
            for u in (g[todo.pop()]&unseen)-found:
                found.add(u);todo.append(u)
        unseen-=found;answer.append(found)
    return answer


def core_cycles(m):
    return [c for c in components(m['g'],m['C'])
            if all(len(m['g'][v]&c)==2 for v in c)]


def square_terms(m):
    inverse={c:x for x,c in m['owner'].items()}
    return [[(m['group'][inverse[v]],m['colour'][inverse[v]]) for v in sorted(c)]
            for c in core_cycles(m) if len(c)==4]


def correction_expectation(terms,fixed):
    answer=Fraction(0)
    for literals in terms:
        free=sorted({j for j,bit in literals}-fixed.keys())
        total=0
        for bits in product((0,1),repeat=len(free)):
            phase=fixed|dict(zip(free,bits))
            k=sum(phase[j]!=bit for j,bit in literals)
            total+=5*min(k,2)-3*k
        answer+=Fraction(total,2**len(free))
    return answer


def template_certificate(m):
    terms=square_terms(m);fixed={};eta=correction_expectation(terms,fixed)
    assert (8*eta).denominator==1
    steps=[eta]
    for j in range(len(m['components'])):
        a,b=(correction_expectation(terms,fixed|{j:bit}) for bit in (0,1))
        fixed[j]=int(b>a);steps.append(max(a,b));assert steps[-1]>=steps[-2]
    Y={x for x in m['X'] if m['colour'][x]==fixed[m['group'][x]]}
    A=m['C']-{m['owner'][x] for x in Y}
    Z=path_cycle_optimum(m['g'],A)
    D=m['I']|Y|Z;b=len(m['I'])
    assert 5*len(Z)>=3*b+steps[-1]
    assert 5*len(D)>=13*b+eta
    return D,dict(eta=eta,E8=int(8*eta),terms=terms,steps=steps,phases=fixed,
                  Y=Y,A=A,Z=Z,cycles=core_cycles(m))


def full_certificate(g,S,colour,beta):
    w=decompose(g,S);m=layers(g,w['C0'],w['I0'],w['X0'],w['owner'],w['centre'],colour)
    inner,phase=template_certificate(m)
    retained=(w['R']-w['I0'])|{ell for c,ell,x in w['triples']}
    D=inner|retained
    p,u,a,b,b3=len(w['triples']),len(w['pairs']),w['a'],w['b'],w['b3']
    minimum=min(a,p);alpha=a-minimum;pi=p-minimum
    e=u-a-2*b;r=len(w['R'])-a-b;q=len(g)-len(S)-p-u
    d=len(S)-beta;tau=minimum+b-2*d
    E8=phase['E8'];bp=len(w['I0']);L=len(retained)
    Z=40*beta-40*L-104*bp-E8
    terms=[Z,64*r,152*alpha,152*pi,24*e,64*(e-b3),64*q,304*tau]
    assert all(t>=0 for t in terms)
    assert 64*len(g)-648*d-E8==sum(terms)
    cycle_lengths=[len(c) for c in phase['cycles']]
    hierarchy=[]
    if not cycle_lengths:
        zz=3*beta-3*L-8*bp
        ts=[zz,5*r,12*alpha,12*pi,2*e,5*(e-b3),5*q,24*tau]
        assert all(t>=0 for t in ts) and sum(ts)==5*len(g)-51*d
        hierarchy.append(dict(h='acyclic',Z=zz,terms=ts))
    else:
        for h in range(1,min(cycle_lengths)//6+1):
            zz=(3*h+2)*beta-(3*h+2)*L-(8*h+5)*bp
            ts=[zz,(5*h+3)*r,(12*h+7)*alpha,(12*h+7)*pi,
                (2*h+1)*e,(5*h+3)*(e-b3),(5*h+3)*q,(24*h+14)*tau]
            assert all(t>=0 for t in ts)
            assert sum(ts)==(5*h+3)*len(g)-(51*h+30)*d
            hierarchy.append(dict(h=h,Z=zz,terms=ts))
    return D,dict(witnesses=w,template=m,phase=phase,inner=inner,retained=retained,
                  L=L,Z=Z,nonnegative_terms=terms,hierarchy=hierarchy,
                  counts=dict(p=p,u=u,a=a,b=b,b3=b3,m=minimum,alpha=alpha,pi=pi,
                              e=e,r=r,q=q,d=d,tau=tau))
