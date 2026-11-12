"""Ordinary-component replacement and core-path credits at zero budget."""
from fractions import Fraction
from subcubic_partial_template import layers,one_side
from subcubic_phase_pairing import pairing_data,expectation,template_certificates
from subcubic_phase_slack import owner_slack
from subcubic_intrinsic_obstruction import path_cycle_optimum


def components(g,allowed):
    unseen=set(allowed);answer=[]
    while unseen:
        K={min(unseen)};todo=list(K)
        while todo:
            for v in (g[todo.pop()]&allowed)-K:K.add(v);todo.append(v)
        unseen-=K;answer.append(K)
    return answer


def restriction(m,X):
    return layers(m['g'],{m['owner'][x] for x in X},
                  {m['centre'][x] for x in X},X,
                  {x:m['owner'][x] for x in X},
                  {x:m['centre'][x] for x in X},m['graph_colour'])


def path_events(m):
    inverse={c:x for x,c in m['owner'].items()};events=[]
    def literal(v):
        x=inverse[v];return m['group'][x],1-m['colour'][x]
    for K in components(m['g'],m['C']):
        ends=sorted(v for v in K if len(m['g'][v]&K)<=1)
        if not ends:continue
        v=ends[0];key,bit=literal(v);requirements={key:bit};prefix=[v]
        nxt=sorted(m['g'][v]&K)
        boundary=None
        if nxt:
            u=nxt[0]
            if literal(u)==literal(v):
                prefix.append(u)
                tail=sorted((m['g'][u]&K)-{v})
                boundary=tail[0] if tail else None
            else:boundary=u
        if boundary is not None:
            j,keep=literal(boundary)
            assert (j,keep)!=(key,bit)
            assert j not in requirements or requirements[j]==1-keep
            requirements[j]=1-keep
        assert len(prefix) in (1,2) and len(requirements)<=2
        delta=Fraction((3-(2*len(prefix))%3)%3,3)
        assert delta>0 and delta/Fraction(2**len(requirements))>=Fraction(1,12)
        events.append(dict(K=K,prefix=prefix,boundary=boundary,
                           requirements=requirements,delta=delta))
    return events


def zero_budget_certificate(m):
    data=pairing_data(m);slack=owner_slack(m,data)
    if slack['sigma']!=0:raise ValueError('Requires exact zero phase budget')
    ordinary=[];oddX=set();chosen=set();bO=0
    for order,cyclic in zip(m['components'],m['cyclic']):
        if cyclic and len(order)%8==4:oddX.update(order);continue
        sub=restriction(m,set(order));b=len(sub['I']);bO+=b
        assert b%4==0
        assert all(m['g'][c]&m['C']<=sub['C'] for c in sub['C'])
        a,da=one_side(sub,0);bset,db=one_side(sub,1)
        best=max((a,bset),key=lambda s:(len(s),sorted(s)))
        assert 4*len(best)>=11*b
        chosen|=best;ordinary.append(dict(X=set(order),certificate=best,b=b))
    rem=restriction(m,oddX)
    pairing=pairing_data(rem);assert owner_slack(rem,pairing)['sigma']==0
    events=path_events(rem)
    terms=pairing['terms']+[(row['delta'],row['requirements']) for row in events]
    initial=expectation(terms,{})
    assert initial>=-pairing['rho']+Fraction(len(events),12)
    fixed={};steps=[initial]
    for j in range(len(rem['components'])):
        aa,bb=(expectation(terms,fixed|{j:bit}) for bit in (0,1))
        fixed[j]=int(bb>aa);steps.append(max(aa,bb));assert steps[-1]>=steps[-2]
    Y={x for x in rem['X'] if rem['colour'][x]==fixed[rem['group'][x]]}
    A=rem['C']-{rem['owner'][x] for x in Y}
    Z=path_cycle_optimum(m['g'],A)
    assert Fraction(len(Z))-Fraction(2*len(rem['I']),3)>=steps[-1]
    repaired=chosen|rem['I']|Y|Z
    b=len(m['I']);o=data['odd'];t=len(events)
    assert len(repaired)>=Fraction(5*b,2)+Fraction(o,3)+Fraction(bO,4)+Fraction(t,12)
    first,_=one_side(m,0);second,_=one_side(m,1)
    best=max((first,second,repaired),key=lambda s:(len(s),sorted(s)))
    assert 20*len(best)>=52*b+3*bO+t
    return best,dict(ordinary=ordinary,ordinary_helpers=bO,core_paths=t,
                     remainder=rem,events=events,pairing=pairing,terms=terms,
                     initial=initial,phases=fixed,steps=steps,repaired=repaired,
                     alternatives=(first,second,repaired),A=A,Z=Z)
