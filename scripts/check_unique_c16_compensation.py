#!/usr/bin/env python3
"""Independent matching, original physical graphs, Rado cuts and mixed regions."""
from pathlib import Path
from collections import Counter
from itertools import combinations,product
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from unique_c16_compensation import certificate,clean
from c16_regional_compensation import mixed_ten,mixed_eight
from owner_matching_certificate import prepare
from all_helper_optimization import solve
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();methods=Counter();features=Counter();digest=hashlib.sha256();rng=random.Random(16842113)


def parts(V,E):
    adj={v:set() for v in V}
    for a,b in E:adj[a].add(b);adj[b].add(a)
    unseen=set(V);out=[]
    while unseen:
        C={min(unseen)};todo=list(C)
        for a in todo:
            for b in adj[a]-C:C.add(b);todo.append(b)
        unseen-=C;out.append(C)
    return out


def literal_cost(n,E,U):
    adj=[0]*n
    for a,b in E:adj[a]|=1<<b;adj[b]|=1<<a
    @lru_cache(None)
    def f(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;ans=f(rest);ns=adj[v]&rest
        while ns:
            u=ns&-ns;ns-=u;ans=max(ans,1+f(rest^u))
        return ans
    return f(sum(1<<v for v in U))


def physical(x,S,T):
    b=x['b'];n=2*b;g=[set() for _ in range(5*b)]
    def edge(a,c):g[a].add(c);g[c].add(a)
    for j,(a,c) in enumerate(x['P']):edge(j,b+a);edge(j,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    col=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(col[a]!=col[c] for a in range(5*b) for c in g[a])
    D=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
    assert all(len(g[v]&D)<=1 for v in D)
    counts['literal_original_physical_scores']+=1;return len(D)


def check_rank(projected,owners,B,reserved,forest_size,epsilon,full=False):
    of={v:j for j,C in enumerate(projected) for v in C};families=[i for i,C in enumerate(owners) if len(C)%6 and i not in reserved]
    if len(families)>10:return
    best=len(families)
    total_weight=sum(2 if len(owners[i])%6==4 else 1 for i in families)
    for bits in range(1<<len(families)):
        J={i for j,i in enumerate(families) if bits>>j&1};V={v for i in J for v in owners[i]}
        E=[(of[a],of[b]) for a,b in B if a in V]
        rank=len(projected)-len(parts(range(len(projected)),E))
        weight=sum(2 if len(owners[i])%6==4 else 1 for i in J)
        # An early-return constructor certifies the TOTAL Rado threshold.
        # A particular subfamily need not pay its own weight: omitted labels
        # can supply the surplus. Full representatives retain the stronger
        # rank>=|J| condition below.
        assert 3*(len(families)-len(J)+rank)>=total_weight-epsilon
        if 3*rank<weight-epsilon:counts['subfamilies_requiring_omitted_label_surplus']+=1
        if full:assert rank>=len(J)
        best=min(best,len(families)-len(J)+rank);counts['independent_subset_rank_controls']+=1
    assert best==forest_size and 3*best>=total_weight-epsilon
    counts['independent_Rado_minmax_controls']+=1


def inspect(x,exact=False):
    rec=certificate(**x);assert rec['applicable'];n=2*x['b'];U=set(rec['U']);T=set(rec['witnesses']);M=rec['matching'];A=x['P']+x['Q'];cover=U-T
    assert physical(x,set(range(n))-U,T)==rec['beta_I_lower']==3*x['b']-len(M)>=(8*x['b']+2)//3
    assert len(cover)==len(M) and len({v for e in M for v in e})==2*len(M)
    E={frozenset(e) for e in A};assert all(set(e)<=U and frozenset(e) in E for e in M)
    assert all(a in cover or b in cover for a,b in A if a in U and b in U)
    odd=sum(len(C)%2 for C in parts(U,[e for e in A if set(e)<=U]));assert odd==len(U)-2*len(M)
    if n<=40:assert literal_cost(n,A,U)==len(M);counts['literal_full_matching_comparisons']+=1
    if exact:assert solve(x['b'],x['P'],x['Q'],x['B'])['beta_I']>=rec['beta_I_lower'];counts['exact_small_all_helper_optima']+=1
    owners=parts(range(n),x['B']);assert len(U)==sum((len(C)+2)//3 for C in owners) or any(row['certificate']['method'] in ('at most one auxiliary square','owner C4/6k','inherited sufficient class') for row in rec['components'])
    for row in rec['components']:
        K=row['vertices'];rr=row['certificate'];methods[rr['method']]+=1
        idx={v:j for j,v in enumerate(K)};B=[(idx[a],idx[b]) for a,b in x['B'] if a in idx];ow=parts(range(len(K)),B)
        localU={idx[v] for v in U&set(K)};localA=[(idx[a],idx[b]) for a,b in A if a in idx]
        if 'forest' in rr:
            check_rank(rr['projected_auxiliary'],ow,B,rr['reserved_owner_indices'],rr['forest']['size'],rr['rank_epsilon_thirds'],rr['full_representation'])
        if 'local' in rr:
            z=rr['local'];R=set(z['region']);UR=localU&R;d=len(UR)-2*literal_cost(len(K),localA,UR) if len(K)<=80 else len(UR)-2*sum(len(C)//2 for C in parts(UR,[e for e in localA if set(e)<=UR]))
            assert d==z['deficiency'];counts['independent_regional_deficiencies']+=1
            if 'boundary' in rr:assert localU&set(rr['boundary'])==set(rr['fixed_boundary'])
        for stage in rr.get('history',[]):
            cut=stage['cut'];projected=cut['projected_auxiliary'];of={v:j for j,C in enumerate(projected) for v in C};J=set(cut['Rado_family']);V={v for i in J for v in ow[i]};EJ=[(of[a],of[b]) for a,b in B if a in V]
            rank=len(projected)-len(parts(range(len(projected)),EJ));assert rank==cut['total_subset_rank']
            assert len(cut['family_indices'])-len(J)+rank==cut['forest_size']
            rootpart=next(C for C in parts(range(len(projected)),EJ) if 0 in C);assert set(cut['root_nodes'])==rootpart
            assert cut['root_rank']==len(rootpart)-1 and set(cut['root_region'])=={v for j in rootpart for v in projected[j]}
            counts['independent_Rado_dual_support_controls']+=1
    counts['physical_models']+=1;digest.update(json.dumps([x,rec],sort_keys=True).encode());return rec


def template(lengths):
    P=[];Q=[];off=0
    for m in lengths:
        P += [(off+j,off+j+1) for j in range(0,m,2)];Q += [(off+j,off+(j+1)%m) for j in range(1,m,2)];off+=m
    return dict(b=off//2,P=P,Q=Q,colour=[(v//2)%2 for v in range(off)])


def pool(x,V,lengths):
    sides=[[v for v in sorted(V) if x['colour'][v]==c] for c in (0,1)]
    for side in sides:rng.shuffle(side)
    B=[];off=0
    for m in lengths:
        C=[v for p in zip(sides[0][off:off+m//2],sides[1][off:off+m//2]) for v in p];off+=m//2;B+=list(zip(C,C[1:]+C[:1]))
    assert 2*off==len(V);return B
# Fixed branch inputs, created before this checker. Names assert only those
# methods actually discovered; structural proof alternatives may be preempted
# by a stronger base case or ordinary common forest.
examples=json.loads((ROOT/'develop/fixtures/c16-reservation-examples.json').read_text())
for name,x in sorted(examples.items()):
    rec=inspect(x)
    if not name.startswith('history:'):assert any(row['certificate']['method']==name for row in rec['components'])
    counts['frozen_branch_models']+=1
# The independent reviewer found a valid total-threshold certificate whose
# three parallel square labels violate the unnecessary per-subfamily bound.
regression=json.loads((ROOT/'develop/fixtures/c16-rado-threshold-regression.json').read_text())
prior_surplus=counts['subfamilies_requiring_omitted_label_surplus']
rr=inspect(regression)
assert rr['cost']==3 and rr['beta_I_lower']==45
assert any(row['certificate']['method']=='unique C16 contained 4' for row in rr['components'])
assert counts['subfamilies_requiring_omitted_label_surplus']>prior_surplus
counts['reviewer_total_rank_threshold_regressions']+=1
# Small all-helper exact optima, independent of producedmatching/certificate.
for s,number in ((0,8),(1,2)):
    for trial in range(number):
        x=template([16]+[4]*s);x['B']=pool(x,range(2*x['b']),[2*x['b']]);inspect(x,exact=True)
for trial in range(220):
    s=rng.randrange(2,25);x=template([16]+[4]*s);n=2*x['b'];m=n;lengths=[]
    while m:
        opts=[a for a in range(4,m+1,2) if m-a!=2];a=rng.choice(opts);lengths.append(a);m-=a
    x['B']=pool(x,range(n),lengths);inspect(x)
# Relabel each core branch, add a disjoint auxiliary square component, reverse
# physicalcolours and edgeorientations; recompute entireactualcertificate.
for name,x in sorted(examples.items()):
    if name.startswith('history:'):continue
    for extra in (0,2):
        y=json.loads(json.dumps(x));n=2*y['b']
        for j in range(extra):
            off=n+4*j;y['P'] += [(off,off+1),(off+2,off+3)];y['Q'] += [(off+1,off+2),(off+3,off)];y['B'] += [(off,off+2),(off+2,off+1),(off+1,off+3),(off+3,off)];y['colour'] += [0,0,1,1];y['b']+=2
        n=2*y['b'];perm=list(range(n));rng.shuffle(perm);z=dict(b=y['b'],colour=[0]*n)
        for v,c in enumerate(y['colour']):z['colour'][perm[v]]=1-c
        for key in ('P','Q','B'):z[key]=[(perm[b],perm[a]) for a,b in reversed(y[key])]
        inspect(z);counts['relabel_reassembly_controls']+=1
# Local C10 constructor: every possible contactmatching on six free endpoints
# perphysicalcolour (15 choices each), no reserved squares h0.
def all_matchings(V):
    if not V:yield [];return
    a=V[0]
    for b in V[1:]:
        for tail in all_matchings([v for v in V[1:] if v!=b]):yield [(a,b)]+tail


def local_ten(x):
    data=prepare(**x);reserved=[i for i,(C,_) in enumerate(data['owner_components']) if len(C) in (4,10)];V=set(range(2*x['b']));F=sorted(V-{v for i in reserved for v in data['owner_components'][i][0]});assert len(F)==2
    for mask in range(4):
        F0={v for j,v in enumerate(F) if mask>>j&1};U,z=mixed_ten(data,V,reserved,F0)
        h=len(reserved)-1;assert U&set(F)==F0 and all(len(U&set(data['owner_components'][i][0]))==(4 if len(data['owner_components'][i][0])==10 else 2) for i in reserved)
        cost=literal_cost(2*x['b'],x['P']+x['Q'],U) if x['b']<=24 else sum(len(C)//2 for C in parts(U,[e for e in x['P']+x['Q'] if set(e)<=U]))
        assert len(U)-2*cost==z['deficiency']>=h and cost<=(h+4+len(F0))//2
        assert sum(z['candidate_budgets'])<=2*(h+4+len(F0))
        bits=dict(z['bit']);assert all(bits[a]!=bits[b] for a,b in x['P'])
        for table in z['tables']:
            features['C10_contact_'+str(table['contact_pairs'])]+=1
            features['C10_F_mate_position_'+str(table['order'][4])]+=1
        counts['fixed_two_boundary_C10_controls']+=1
        digest.update(json.dumps([x,clean(z)],sort_keys=True).encode())
left=list(range(0,12,2));right=list(range(1,12,2))
for p0 in all_matchings(left):
    for p1 in all_matchings(right):
        r=right[:];rng.shuffle(r);x=dict(b=6,P=p0+p1,Q=list(zip(left,r)),B=[(j,(j+1)%10) for j in range(10)],colour=[j%2 for j in range(12)]);local_ten(x);counts['complete_C10_endpoint_contact_models']+=1
for h in (1,2,3,4,7,16,63):
    for trial in range(32):
        n=4*h+12;x=template([16]+[4]*((n-16)//4));sides=[[v for v in range(n) if x['colour'][v]==c] for c in (0,1)]
        for side in sides:rng.shuffle(side)
        F={sides[0][-1],sides[1][-1]};x['B']=pool(x,set(range(n))-F,[10]+[4]*h);local_ten(x)
# MixedC8 local lemma, all16fixedsubsets in each accepted placement.
for trial in range(120):
    lengths=[16,4] if trial%2 else [12,4,4];x=template(lengths);V=set(range(20));sides=[[v for v in V if x['colour'][v]==c] for c in (0,1)]
    for side in sides:rng.shuffle(side)
    F=set(sides[0][-2:]+sides[1][-2:]);x['B']=pool(x,V-F,[8,4,4]);data=prepare(**x);reserved=[i for i,(C,_) in enumerate(data['owner_components']) if len(C) in (4,8)];ac=parts(V,x['P']+x['Q']);of={v:j for j,C in enumerate(ac) for v in C}
    if any(len({of[v] for v in data['owner_components'][i][0]})<2 for i in reserved):continue
    FF=sorted(F)
    for mask in range(16):
        F0={v for j,v in enumerate(FF) if mask>>j&1};U,z=mixed_eight(data,V,reserved,F0);cost=literal_cost(20,x['P']+x['Q'],U)
        assert U&F==F0 and len(U)-2*cost==z['deficiency']>=2
        assert len(z['nonmonochromatic_cycles'])>=2 and max(z['candidate_imbalances'])>=2
        counts['fixed_four_boundary_mixed_C8_controls']+=1;digest.update(json.dumps([x,clean(z)],sort_keys=True).encode())
# Exact all-integer classification: all possibilities from x+5y+9a/2<=10.
rows=[]
for q in range(1,7):
 for x in range(11):
  for y in range(3):
   for a in range(3):
    if 4*x+8*y+6*a<=4*q+16 and 2*x+y>=3*q+2:
     assert q+3*y+3*a<=6 and y+a<=1;rows.append((q,x,y,a))
assert len(rows)==18;counts['complete_serious_rank_integer_types']=len(rows)
required=['unique C16 ordinary rank','unique C16 pure four boundary','unique C16 pure eight boundary','unique C16 mixed C8 four boundary','unique C16 mixed C10 two boundary','closed one C8 plus squares','unique C16 contained 4','unique C16 contained 4,4','unique C16 contained 8','unique C16 contained 4,8','unique C16 contained 10','unique C16 contained 4,10','unique C16 contained 14']
assert all(methods[s] for s in required)
report=dict(status='PASS',counts=dict(sorted(counts.items())),methods=dict(sorted(methods.items())),features=dict(sorted(features.items())),deterministic_sha256=digest.hexdigest(),scope='All-size written uniqueC16 theorem, actualminimumowneromissions plus one finalcommonforest; matching/cover and original5bphysicalcertificates. MixedC10 allh and mixedC8crossinglocalcontrols. Finite labelled/seeds do not prove theorem; absorption proofalternatives may be preempted by strongerbase/ordinaryforest and are not claimed fully covered. Generalmixedcyclic and physicalgrid remainopen.')
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/unique-c16-compensation-check.json');a=p.parse_args();a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
