#!/usr/bin/env python3
"""Independent controls for the written all-scale four-port theorem."""
from pathlib import Path
from itertools import combinations,permutations
import random
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_degree_three_threshold import base,exact
from check_sharp_minimum_two_degree import diss,literal
if not __debug__:raise RuntimeError('Assertions required.')
PORTS=((1,25),(7,24),(13,27),(19,26))
W={6*j+a for j in range(4)for a in(4,5)}
X={6*j+1 for j in range(4)}


def piece():
    g,S,Q=base()
    for a,b in PORTS:g[a].remove(b);g[b].remove(a)
    return g,S,Q


def reached(g,omitted,root):
    seen={root};todo=[root]
    while todo:
        for b in g[todo.pop()]:
            if b not in omitted and b not in seen:seen.add(b);todo.append(b)
    return seen


def local_cuts():
    g,S,Q=piece();rows=[];checks=0
    for n in range(3):
        for cut in combinations(range(28),n):
            omitted=set(cut);root=min(W-omitted);seen=reached(g,omitted,root)
            assert W-omitted<=seen
            missed=set(range(28))-omitted-seen
            expected={6*j+1 for j in range(4)if omitted=={6*j,6*j+4}}
            assert missed==expected
            if missed:rows.append({'cut':list(cut),'unattached':sorted(missed)})
            checks+=1
    return {'checks':checks,'exceptions':rows}


def boundary_controls():
    """Enumerate outside states, then local physical patterns with ONE C budget.

    This is independent of the global recursion and of the proof cases.
    DP states are actual used chosen-connector masks, not per-block credits.
    """
    g,S,Q=piece();wlist=sorted(W);rows=[]
    for wmask in range(1<<8):
        chosenW={wlist[j]for j in range(8)if wmask>>j&1}
        if not diss(g,chosenW):continue
        for cmask in range(16):
            chosenC={24+j for j in range(4)if cmask>>j&1}
            outside=chosenW|chosenC
            dp={0:0}
            for j in range(4):
                options=[]
                for pattern in range(16):
                    chosen={6*j+a for a in range(4)if pattern>>a&1}
                    local=chosen|outside
                    # Check all chosen selected vertices and all chosen witnesses.
                    # Connector TOTAL capacities are retained by the outer DP.
                    if any(len(g[a]&local)>1 for a in chosen|chosenW):continue
                    used=0;valid=True
                    for a in chosenC:
                        count=len(g[a]&chosen)
                        if count>1:valid=False;break
                        if count:used|=1<<(a-24)
                    if valid:options.append((used,len(chosen)))
                nxt={}
                for used,value in dp.items():
                    for more,size in options:
                        if used&more:continue
                        key=used|more;nxt[key]=max(nxt.get(key,-1),value+size)
                dp=nxt
            optimum=max(dp.values()) if dp else None
            if optimum is not None:
                assert optimum+len(outside)<=14
            rows.append({'witness_mask':wmask,'connector_mask':cmask,'selected_optimum':optimum})
    digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'outside_states':len(rows),'exact_rows_sha256':digest,'maximum_total':14,
            'scope':'All dissociated witness masks and all chosen connector masks; four local-pattern DP steps retain single total connector capacity.'}


def lift(k):
    if type(k)is not int or k<1:raise ValueError('Integer k>=1 required.')
    old,S,Q=piece();g=[set()for _ in range(28*k)]
    for h in range(k):
        for a in range(28):
            for b in old[a]:g[28*h+a].add(28*h+b)
        for a,b in PORTS:
            u,v=28*h+a,28*((h+1)%k)+b;g[u].add(v);g[v].add(u)
    return g,{28*h+a for h in range(k)for a in S},{28*h+a for h in range(k)for a in Q}


def physical(k,all_cuts=False):
    g,S,Q=lift(k);n=len(g)
    assert n==28*k and len(S)==16*k and len(Q)==14*k and diss(g,Q)
    assert min(map(len,g))==3 and max(map(len,g))==5
    colours={0:0};todo=[0]
    while todo:
        a=todo.pop();assert a not in g[a]
        for b in g[a]:
            assert a in g[b]
            if b not in colours:colours[b]=1-colours[a];todo.append(b)
            assert colours[b]!=colours[a]
    assert len(colours)==n
    for a in set(range(n))-S:assert literal(g,S,a)
    for a in S:
        h,j=divmod(a,28);block,kind=divmod(j,6)
        failure=28*h+6*block+{0:4,1:4,2:5,3:3}[kind]
        assert not literal(g,S,failure,a)
    checks=0
    if all_cuts:
        for size in range(3):
            for cut in combinations(range(n),size):
                omitted=set(cut);root=next(x for x in range(n)if x not in omitted)
                assert len(reached(g,omitted,root))==n-size
                checks+=1
    return {'k':k,'n':n,'selected':len(S),'attaining_size':len(Q),'minimum_degree':3,'maximum_degree':5,
            'literal_failures':len(S),'all_cuts_up_to_two':checks,'connectivity':'General written attachment/bundle proof; exhaustive controls only when explicitly counted.'}


def interface_controls():
    rows=[];rng=random.Random(20261112);physical_cuts=0;small_quotient_cuts=0
    for k in (1,2,3,4,6):
        size=2*k
        if k==1:pairs=[(a,b)for a in permutations(range(size))for b in permutations(range(size))]
        else:
            pairs=[(tuple(range(size)),tuple(range(size)))]
            for _ in range(11):
                a=list(range(size));b=list(range(size));rng.shuffle(a);rng.shuffle(b);pairs.append((tuple(a),tuple(b)))
        for left,right in pairs:
            old,S,Q=piece();g=[set()for _ in range(28*k)];links=[]
            for h in range(k):
                for a in range(28):g[28*h+a].update(28*h+b for b in old[a])
            for wing,perm in ((0,left),(1,right)):
                for source,target in enumerate(perm):
                    h,j=divmod(source,2);t,l=divmod(target,2)
                    a=28*h+12*wing+6*j+1;b=28*t+24+2*wing+l
                    assert b not in g[a];g[a].add(b);g[b].add(a)
                    links.append((h,t,a,b))
            selected={28*h+a for h in range(k)for a in S};attain={28*h+a for h in range(k)for a in Q}
            assert min(map(len,g))==3 and max(map(len,g))==5 and diss(g,attain)
            for a in set(range(28*k))-selected:assert literal(g,selected,a)
            for a in selected:
                h,j=divmod(a,28);block,kind=divmod(j,6)
                assert not literal(g,selected,28*h+6*block+{0:4,1:4,2:5,3:3}[kind],a)
            best=None;cut_links=[]
            if k>=2:
                for mask in range(1,(1<<k)-1):
                    crossing=[(a,b)for h,t,a,b in links if bool(mask>>h&1)!=bool(mask>>t&1)]
                    if best is None or len(crossing)<best:best=len(crossing);cut_links=crossing
            expected=k==1 or best>=3
            if not expected:
                omitted={a for a,b in cut_links}
                assert len(omitted)<=2
                root=next(a for a in range(len(g))if a not in omitted)
                assert len(reached(g,omitted,root))<len(g)-len(omitted)
                small_quotient_cuts+=1
            # The full physical two-cut condition is independent of quotient enumeration.
            if k<=4:
                actual=True
                for count in range(3):
                    for cut in combinations(range(len(g)),count):
                        omitted=set(cut);root=next(a for a in range(len(g))if a not in omitted)
                        physical_cuts+=1
                        if len(reached(g,omitted,root))!=len(g)-count:actual=False;break
                    if not actual:break
                assert actual==expected
            rows.append({'k':k,'left_permutation':left,'right_permutation':right,'quotient_edge_connectivity':best,
                         'three_connected':expected,'small_cut_witness':[a for a,b in cut_links]if not expected else None})
    return {'models':rows,'physical_cut_checks':physical_cuts,'small_quotient_cut_certificates':small_quotient_cuts}


def main():
    original,S,Q=base();deletions=[]
    for mask in range(16):
        g=[set(v)for v in original]
        for j,(a,b)in enumerate(PORTS):
            if mask>>j&1:g[a].remove(b);g[b].remove(a)
        result=exact(g);assert result['beta']==14
        deletions.append({'deleted_port_mask':mask,**result})
    rows=[physical(k,k<=4)for k in(1,2,3,4,8,16,32)]
    record={'status':'PASS','physical_models':rows,'simultaneous_port_deletion_controls':deletions,
            'local_attachment_controls':local_cuts(),'independent_boundary_controls':boundary_controls(),'arbitrary_interface_controls':interface_controls(),
            'scope':'All-parameter conclusions rely on the written arbitrary-D cap and two-cut attachment proof; finite exact recursion and physical controls check implementation.'}
    out=ROOT/'output/three-connected-degree-three-check.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(rows),'port_subsets':len(deletions),
                      'literal_failures':sum(x['literal_failures']for x in rows),
                      'full_lift_cut_checks':sum(x['all_cuts_up_to_two']for x in rows),
                      'local_cut_checks':record['local_attachment_controls']['checks'],
                      'outside_states':record['independent_boundary_controls']['outside_states'],'interface_models':len(record['arbitrary_interface_controls']['models']),'interface_cut_checks':record['arbitrary_interface_controls']['physical_cut_checks']},sort_keys=True))

if __name__=='__main__':main()
