#!/usr/bin/env python3
"""Literal graph controls and exact rational certificates for the whole cut.

Imports only the preceding standalone checker's generic graph utilities.
No LP solver is used: all parameter claims have explicit identities/proofs.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random
import check_selected_star_general_budget as old

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def values(v,delta,maximum):
    c,q,s,a,b2,b3,mu,m,z0,u=v
    t=a+b2+b3
    n=5*c+2*s+q+t+m+z0+u
    J=c+s+2*q-a-2*b2-3*b3
    T=t-s
    R=c-q+b2+b3-mu
    D=q+s+2*mu-2*b2
    F=maximum*u-(3*delta-7)*c-(delta-4)*s-delta*t+3*q-(delta-1)*m-delta*z0
    B=c-q+t+m+z0-u
    return n,(J,T,R,D,F,B)


def check_identity(v,delta,maximum):
    c,q,s,a,b2,b3,mu,m,z0,u=v
    n,(J,T,R,D,F,B)=values(v,delta,maximum)
    if maximum>=4:
        h=maximum-delta+1
        rhs=(2*maximum-5)*J+(2*maximum-3)*(T+R)+D+2*F+(maximum+delta-1)*B
        rhs+=(2*maximum-5)*(s+mu)+(2*maximum-7)*b3+2*z0
        assert h*n==rhs
    if delta==maximum==3:
        assert 7*n==8*J+18*T+20*R+4*D+14*F+35*B+6*s+4*a+12*mu+14*z0
    if delta==maximum:
        assert F+delta*B==m-(2*delta-7)*c-(delta-3)*q-(delta-4)*s


def arithmetic_controls():
    identities=primals=0
    for delta in range(3,65):
        for maximum in range(delta,delta+33):
            for j in range(10):
                v=[0]*10;v[j]=1
                check_identity(v,delta,maximum);identities+=1
        for maximum in range(max(4,delta),4*delta-6):
            h=maximum-delta+1
            m=Q(2*(4*delta-7-maximum),h)
            v=[Q(2),Q(0),Q(0),Q(2),Q(0),Q(0),Q(0),m,Q(0),m+2]
            assert min(v)>=0
            n,(J,T,R,D,F,B)=values(v,delta,maximum)
            assert (J,T,R,D,F,B)==(0,2,2,0,0,2)
            assert n==Q(2*(5*maximum+delta-7),h)
            check_identity(v,delta,maximum);primals+=1
    v=list(map(Q,[Q(12,7),Q(12,7),0,0,Q(6,7),Q(8,7),0,Q(30,7),0,Q(30,7)]))
    n,slacks=values(v,3,3)
    assert n==Q(146,7) and slacks==(0,2,2,0,0,2)
    check_identity(v,3,3)
    # Identities are homogeneous; these controls test exact large-integer arithmetic.
    for exponent in (64,401,1024):
        scale=10**exponent+7
        check_identity([scale*(j+1) for j in range(10)],3,3)
        check_identity([scale*(j+1) for j in range(10)],7,9)
    return {'basis_identity_checks':identities,'low_dispersion_primal_witnesses':primals,
            'cubic_primal_witness':True,'large_integer_identity_checks':6,
            'scope':'exact algebra/primal controls; no graph-sharpness inference'}


def allocations(g,s):
    centres,leaves,isolates=old.structure(g,s)
    owner={ell:next(iter(g[ell]&centres)) for ell in leaves}
    outside=set(range(len(g)))-s
    opts=[tuple(w for w in sorted(outside) if not old.literal(g,s-{ell},w)) for ell in leaves]
    assert all(opts)
    clean={owner[ell] for ell,choices in zip(leaves,opts) if any(g[w]&s=={ell} for w in choices)}
    direct=sorted(centres-clean)
    direct_opts=[tuple(w for w in sorted(outside) if centre in g[w] and not old.literal(g,s-{centre},w)) for centre in direct]
    assert all(direct_opts)
    for leaf_ws in product(*opts):
        if {owner[ell] for ell,w in zip(leaves,leaf_ws) if g[w]&s=={ell}}!=clean:continue
        for centre_ws in product(*direct_opts):
            W=set(leaf_ws)|set(centre_ws)
            assert len(W)==len(leaves)+len(direct)
            h={i:len(g[i]&W) for i in isolates}
            gamma=[]
            for ell,w in zip(leaves,leaf_ws):
                helper=g[w]&isolates
                if helper:
                    i=next(iter(helper))
                    if h[i]==2:gamma.append((owner[ell],i,ell,w))
            mu=old.augmenting_matching(gamma)
            assert mu==max(map(len,old.all_matchings(gamma)))
            touched={i for i in isolates if h[i]}
            P=s-centres-set(leaves)-isolates
            U=outside-W
            v=[len(centres),len(direct),len(leaves)-2*len(centres),
               sum(x==1 for x in h.values()),sum(x==2 for x in h.values()),sum(x>=3 for x in h.values()),
               mu,len(P),len(isolates-touched),len(U)]
            yield v,W,U,P,sum(h.values())


def audit(g,s,beta,count):
    delta,maximum=min(map(len,g)),max(map(len,g))
    d=len(s)-beta
    for v,W,U,P,H in allocations(g,s):
        boundary_audit(g,s,beta,v,U,count)
        c,q,surplus,a,b2,b3,mu,m,z0,u=v
        e=2*c+surplus;t=a+b2+b3
        assert len(s)==3*c+surplus+t+m+z0
        assert H<=c+surplus+2*q
        cut_SW=sum(len(g[x]&W) for x in s)
        internal=sum(len(g[x]&s) for x in s)
        cut_SU=sum(len(g[x]&U) for x in s)
        assert cut_SW==e+q+H and internal==2*e+m
        assert cut_SU==sum(len(g[x]) for x in s)-internal-cut_SW
        assert cut_SU<=sum(len(g[x]) for x in U)<=maximum*u
        assert cut_SU>=delta*len(s)-3*e-m-q-H
        assert cut_SU>=(3*delta-7)*c+(delta-4)*surplus+delta*t-3*q+(delta-1)*m+delta*z0
        for lower in range(3,delta+1):
            for upper in range(maximum,maximum+3):
                n,(J,T,R,D,F,B)=values(v,lower,upper)
                assert n==len(g) and min(J,D,F)>=0
                assert min(T,R,B)>=2*d
                check_identity(v,lower,upper)
                if upper>=4:
                    assert 2*(5*upper+lower-7)*d<=(upper-lower+1)*n
                    assert d<=((upper-lower+1)*n)//(2*(5*upper+lower-7))
                else:
                    assert lower==upper==3 and 146*d<=7*n
                count['degree_parameter_checks']+=1
        if delta==maximum:
            assert m>=2*delta*d+(2*delta-7)*c+(delta-3)*q+(delta-4)*surplus
            if delta>=4 and not m:assert d<=0
            count['regular_resource_checks']+=1
        count['witness_allocations']+=1
        count['with_selected_edges']+=bool(m)
        count['with_stars']+=bool(c)
        count['untouched_isolate_allocations']+=bool(z0)
        count['positive_deficit_allocations']+=d>0
        count['nonregular_allocations']+=delta!=maximum
        count['cut_edges_checked']+=cut_SU


def boundary_audit(g,s,beta,v,U,count,rectangle=None):
    c,q,surplus,a,b2,b3,mu,m,z0,u=v
    d=len(s)-beta
    for k in range(max(4,max(map(len,g))),max(4,max(map(len,g)))+3):
        eps_s=sum(k-len(g[x]) for x in s)
        eps_u=sum(k-len(g[x]) for x in U)
        n,(J,T,R,D,F,B)=values(v,k,k)
        Fhat=F+eps_s-eps_u
        assert n==len(g) and min(J,D,Fhat)>=0 and min(T,R,B)>=2*d
        check_identity(v,k,k)
        lower=(3*k-7)*c+(k-4)*surplus+k*(a+b2+b3)-3*q+(k-1)*m+k*z0-eps_s
        cut=sum(len(g[x]&U) for x in s)
        assert lower<=cut<=k*u-eps_u
        assert (12*k-14)*d<=n+2*eps_s-2*eps_u
        assert d<=(n+2*eps_s-2*eps_u)//(12*k-14)
        assert m+eps_s-eps_u>=2*k*d+(2*k-7)*c+(k-3)*q+(k-4)*surplus
        if rectangle is not None and k==4:
            h,w=rectangle
            assert sum(4-len(g[x]) for x in range(n))==2*h+2*w
            assert d<=(n+4*h+4*w)//34
            count['rectangle_boundary_checks']+=1
        count['boundary_degree_checks']+=1
        count['negative_deficit_differences']+=eps_s<eps_u
        count['positive_gap_boundary_checks']+=d>0


def literals(g):
    # Actual three-vertex stars, independent of active-neighbour shortcuts.
    rules=[];n=len(g)
    for x in range(n):
        rules.append([sum(1<<v for v in (a,b)) for a,b in combinations([v for v in range(n) if v!=x],2)
                      if int(a in g[x])+int(b in g[x])+int(a in g[b])>=2])
    formed=[]
    for mask in range(1<<n):
        formed.append(all(any(mask&pair==pair for pair in rules[x]) for x in range(n) if not(mask>>x&1)))
    return formed


def models():
    rows=[]
    # All labelled cubic graphs with fixed parts (3,3),(4,4).
    for size in (3,4):
        for missing in [()] if size==3 else permutations(range(size)):
            edges=[(a,size+b) for a in range(size) for b in range(size)
                   if size==3 or missing[a]!=b]
            rows.append(('all_cubic_'+str(size),old.graph(2*size,edges)))
    # All labelled degree-four graphs with fixed parts (4,4),(5,5).
    rows.append(('all_quartic_4',old.graph(8,list(product(range(4),range(4,8))))))
    for missing in permutations(range(5)):
        rows.append(('all_quartic_5',old.graph(10,[(a,5+b) for a in range(5) for b in range(5) if missing[a]!=b])))
    rows.append(('complete_degree5',old.graph(10,list(product(range(5),range(5,10))))))
    # Seeded controls are reported separately from exhaustive labelled ranges.
    rng=random.Random(2026111201)
    for size,degree,trials in [(5,3,12),(6,3,12),(6,4,8)]:
        seen=set()
        while len(seen)<trials:
            candidate=[]
            for _ in range(degree):
                perm=list(range(size));rng.shuffle(perm);candidate+=list(enumerate(perm))
            if len(set(candidate))!=size*degree:continue
            key=tuple(sorted(candidate))
            if key in seen:continue
            seen.add(key)
            rows.append(('seeded_regular_'+str(size)+'_'+str(degree),old.graph(2*size,[(a,size+b) for a,b in key])))
    for left,right in [(3,4),(3,5),(4,5)]:
        rows.append(('complete_nonregular_'+str(left)+'_'+str(right),old.graph(left+right,list(product(range(left),range(left,left+right))))))
    for _ in range(12):
        g=old.graph(10,[(a,5+b) for a in range(5) for b in range(5) if (b-a)%5 in (0,1,2)])
        for a in range(5):
            b=(a+3)%5
            if rng.randrange(2):g[a].add(5+b);g[5+b].add(a)
        rows.append(('seeded_nonregular',g))
    return rows


def graph_controls():
    counts=Counter();ranges={}
    for label,g in models():
        assert min(map(len,g))>=3
        col=old.colors(g)
        beta,subsets=old.one_part_beta(g,col)
        assert beta==old.beta_literal(g)
        formed=literals(g)
        local=Counter()
        for mask,ok in enumerate(formed):
            local['selected_subsets']+=1
            if not ok:continue
            s={v for v in range(len(g)) if mask>>v&1}
            if any(formed[mask^(1<<v)] for v in s):continue
            local['minimal_selections']+=1
            if old.structure(g,s) is None:
                local['excluded_nonstar_minimal_selections']+=1;continue
            local['eligible_minimal_selections']+=1
            assert old.minimal(g,s)
            audit(g,s,beta,local)
        local['graphs']+=1;local['one_part_subsets']+=subsets
        counts.update(local);ranges.setdefault(label,Counter()).update(local)
    # Existing sharp unrestricted cubic example is explicitly outside our class.
    heawood=old.graph(14,[(i,7+j) for i in range(7) for j in (i,(i+1)%7,(i+3)%7)])
    chosen={1,2,3,5,7,9,10,11}
    assert old.minimal(heawood,chosen) and old.structure(heawood,chosen) is None
    beta,_=old.one_part_beta(heawood,old.colors(heawood));assert beta==7
    return {'totals':dict(sorted(counts.items())),
            'ranges':{name:dict(sorted(row.items())) for name,row in sorted(ranges.items())},
            'excluded_heawood_control':{'order':14,'selected_size':8,'beta':7,'selected_nonstar_component':'six-cycle'}}


def boundary_controls():
    counts=Counter();rows=[]
    boards=[(1,w) for w in range(1,9)]+[(2,w) for w in range(2,8)]+[(3,w) for w in range(3,6)]+[(4,4)]
    for h,w in boards:
        edges=[(r*w+c,(r+dr)*w+c+dc) for r in range(h) for c in range(w)
               for dr,dc in ((1,0),(0,1)) if r+dr<h and c+dc<w]
        g=old.graph(h*w,edges)
        beta,subsets=old.one_part_beta(g,old.colors(g));assert beta==old.beta_literal(g)
        formed=literals(g);local=Counter()
        for mask,ok in enumerate(formed):
            local['selected_subsets']+=1
            if not ok:continue
            s={v for v in range(len(g)) if mask>>v&1}
            if any(formed[mask^(1<<v)] for v in s):continue
            local['minimal_selections']+=1
            if old.structure(g,s) is None:
                local['excluded_nonstar_minimal_selections']+=1;continue
            local['eligible_minimal_selections']+=1
            for v,W,U,P,H in allocations(g,s):
                boundary_audit(g,s,beta,v,U,local,(h,w));local['witness_allocations']+=1
        local['graphs']+=1;local['one_part_subsets']+=subsets
        counts.update(local);rows.append({'height':h,'width':w,'checks':dict(sorted(local.items()))})
    positive=[]
    for a,b in ((1,2),(2,2)):
        g,s=old.gap_family(a,b)
        assert old.minimal(g,s) and old.structure(g,s) is not None
        beta,subsets=old.one_part_beta(g,old.colors(g));assert beta==old.beta_literal(g)
        assert len(s)-beta>0
        local=Counter()
        for v,W,U,P,H in allocations(g,s):boundary_audit(g,s,beta,v,U,local)
        positive.append({'a':a,'b':b,'order':len(g),'selected_size':len(s),'beta':beta,
                         'minimum_degree':min(map(len,g)),'maximum_degree':max(map(len,g)),
                         'one_part_subsets':subsets,'checks':dict(sorted(local.items()))})
    return {'rectangle_totals':dict(sorted(counts.items())),'rectangles':rows,
            'positive_gap_controls':positive,
            'scope':'All selections on the specified finite rectangles; positive gaps occur only in separate nonrectangular minimum-degree-one controls.'}


def main():
    report={'status':'PASS','graph_controls':graph_controls(),'arithmetic':arithmetic_controls(),
            'boundary_controls':boundary_controls(),
            'scope':'Finite literal graphs and exact identities; all-parameter theorem proved in the note. Rational primal points certify only the stated numerical relaxation.'}
    path=Path(__file__).resolve().parents[1]/'output/full-degree-capacity-check.json'
    path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'totals':report['graph_controls']['totals'],
                      'arithmetic':report['arithmetic'],'output':str(path)},sort_keys=True))


if __name__=='__main__':main()
