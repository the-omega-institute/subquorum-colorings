"""Core-cycle event pairing with disjoint owner-class budgets."""
from collections import Counter
from fractions import Fraction
from subcubic_partial_template import decompose,layers,one_side
from subcubic_core_cycles import core_cycles
from subcubic_intrinsic_obstruction import path_cycle_optimum


def pairing_data(m):
    inverse={c:x for x,c in m['owner'].items()};classes={}
    for j,order in enumerate(m['components']):
        for bit in (0,1):
            U={m['owner'][x] for x in order if m['colour'][x]==bit}
            classes[j,bit]=dict(U=U,monochromatic=set(),mono_loss=Fraction(0),mixed=[],
                               distinguished=m['cyclic'][j] and len(order)%8==4)
    rows=[];terms=[];rho=Fraction(0);odd=sum(m['cyclic'][j] and len(c)%8==4 for j,c in enumerate(m['components']))
    for K in core_cycles(m):
        full={};counts=Counter();consistent=True
        for v in sorted(K):
            x=inverse[v];j=m['group'][x];need=1-m['colour'][x]
            if j in full and full[j]!=need:consistent=False
            full[j]=need;counts[j]+=1
        if not consistent:continue
        size=len(K);delta=Fraction((2*size)%3,3);gamma=Fraction(0);flip=[];charge=None
        if delta:
            zero=sorted(j for j,n in counts.items() if n%3==0)
            one=sorted(j for j,n in counts.items() if n%3==1)
            two=sorted(j for j,n in counts.items() if n%3==2)
            if size%3==1:
                if two:flip=[two[0]];gamma=delta
                elif len(one)>=2:flip=one[:2];gamma=delta
                elif len(full)>1:
                    assert len(one)==1 and zero
                    flip=[zero[0]];gamma=Fraction(1,3);charge=(zero[0],1-full[zero[0]])
            elif len(full)>1:
                if zero:flip=[zero[0]]
                elif one:flip=[one[0]]
                else:
                    assert len(two)>=4;flip=two[:2]
                gamma=delta
        loss=(delta-gamma)/2**len(full);rho+=loss
        other=full|{j:1-full[j] for j in flip}
        row=dict(K=K,full=full,counts=dict(counts),delta=delta,gamma=gamma,
                 flip=flip,compensation=other,loss=loss,charge=charge)
        rows.append(row)
        if delta:terms.append((-delta,full))
        if gamma:
            removed=sum(counts[j] for j in flip)
            assert 0<removed<size
            remaining=size-removed
            rounding=Fraction((2*remaining+2)//3)-Fraction(2*remaining,3)
            assert rounding>=gamma
            terms.append((gamma,other))
        if len(full)==1:
            j=next(iter(full));key=j,1-full[j]
            classes[key]['monochromatic']|=K;classes[key]['mono_loss']+=loss
            if size!=4:classes[key]['non_square_mono']=True
        elif loss:
            assert charge is not None and loss<=Fraction(1,12)
            support={v for v in K if (m['group'][inverse[v]],m['colour'][inverse[v]])==charge}
            assert len(support)>=3
            classes[charge]['mixed'].append((support,loss))
    allocated=Fraction(0)
    for key,data in classes.items():
        used=set(data['monochromatic']);remaining=data['U']-used;loss=data['mono_loss']
        for support,cost in data['mixed']:
            assert support<=remaining and not support&used
            used|=support;loss+=cost
        assert 3*len(data['mixed'])<=len(remaining)
        budget=Fraction(len(data['U']),12)-(Fraction(1,6) if data['distinguished'] else 0)
        assert loss<=budget
        data.update(loss=loss,budget=budget,remaining=remaining)
        allocated+=loss
    assert allocated==rho
    assert rho<=Fraction(len(m['I']),6)-Fraction(odd,3)
    return dict(rows=rows,terms=terms,rho=rho,odd=odd,classes=classes)


def expectation(terms,fixed):
    value=Fraction(0)
    for coefficient,requirements in terms:
        if any(j in fixed and fixed[j]!=bit for j,bit in requirements.items()):continue
        value+=coefficient/Fraction(2**sum(j not in fixed for j in requirements))
    return value


def template_certificates(m):
    data=pairing_data(m);fixed={};steps=[expectation(data['terms'],{})]
    assert steps[0]==-data['rho']
    for j in range(len(m['components'])):
        a,b=(expectation(data['terms'],fixed|{j:bit}) for bit in (0,1))
        fixed[j]=int(b>a);steps.append(max(a,b));assert steps[-1]>=steps[-2]
    Y={x for x in m['X'] if m['colour'][x]==fixed[m['group'][x]]}
    A=m['C']-{m['owner'][x] for x in Y};Z=path_cycle_optimum(m['g'],A)
    b=len(m['I']);score=steps[-1]
    assert Fraction(len(Z))-Fraction(2*b,3)>=score
    assert 6*len(Z)>=3*b+2*data['odd']
    phase=m['I']|Y|Z
    first,da=one_side(m,0);second,db=one_side(m,1)
    assert len(first)+len(second)==5*b+da+db
    assert 2*(da+db)>=b-2*data['odd']
    best=max((first,second,phase),key=lambda d:(len(d),sorted(d)))
    assert 5*len(best)>=13*b
    return best,dict(pairing=data,phases=fixed,steps=steps,Y=Y,A=A,Z=Z,
                     alternatives=(first,second,phase),score=score)


def full_certificate(g,S,colour,beta):
    w=decompose(g,S);m=layers(g,w['C0'],w['I0'],w['X0'],w['owner'],w['centre'],colour)
    inner,data=template_certificates(m)
    retained=(w['R']-w['I0'])|{ell for c,ell,x in w['triples']};D=inner|retained
    p,u,a,b,b3=len(w['triples']),len(w['pairs']),w['a'],w['b'],w['b3']
    minimum=min(a,p);alpha=a-minimum;pi=p-minimum;e=u-a-2*b
    r=len(w['R'])-a-b;q=len(g)-len(S)-p-u;d=len(S)-beta;tau=minimum+b-2*d
    Z=5*beta-5*len(retained)-13*len(w['I0'])
    terms=[Z,8*r,19*alpha,19*pi,3*e,8*(e-b3),8*q,38*tau]
    assert all(t>=0 for t in terms) and sum(terms)==8*len(g)-81*d
    return D,dict(witnesses=w,template=m,inner=inner,retained=retained,
                  phase=data,terms=terms,counts=dict(p=p,u=u,a=a,b=b,b3=b3,m=minimum,
                  alpha=alpha,pi=pi,e=e,r=r,q=q,d=d,tau=tau,Z=Z))
