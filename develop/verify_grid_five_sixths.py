#!/usr/bin/env python3
"""Exact regression checks of the paper's no11 interface and five-sixths bound.

Universal claims rest on the accompanying written geometric proofs.
This script does not prove the full rectangular-grid conjecture or run Lean.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json
from pathlib import Path
if not __debug__:
 raise RuntimeError("Run without -O: verification uses assertions.")
import collections,random

def bits(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x^=b

def graph(m,n):
 adj=[0]*(m*n);edges=[]
 for v in range(m*n):
  for w in ([v+1] if v%n+1<n else [])+([v+n] if v//n+1<m else []):
   adj[v]|=1<<w;adj[w]|=1<<v;edges.append((v,w))
 return adj,edges

def pairs(m,n):
 adj,_=graph(m,n)
 def ok(T,A):return all((adj[v]&A).bit_count()<=1 for v in bits(T))
 def rec(left,T,A,M):
  if not left:yield T,A,M;return
  bit=left&-left;v=bit.bit_length()-1;rest=left^bit
  yield from rec(rest,T,A,M)
  if ok(T|bit,A|bit):yield from rec(rest,T|bit,A|bit,M)
  for w in bits(adj[v]&rest):
   wb=1<<w
   if ok(T,A|bit|wb):yield from rec(rest^wb,T,A|bit|wb,M+((v,w),))
 yield from rec((1<<(m*n))-1,0,0,())

def canonical(m,n,T,M):
 assert m%2==n%2==0
 adj,_=graph(m,n);A=T;mate={}
 for v,w in M:
  assert adj[v]>>w&1 and v not in mate and w not in mate and not(T>>v&1) and not(T>>w&1)
  mate[v]=w;mate[w]=v;A|=(1<<v)|(1<<w)
 assert all((adj[v]&A).bit_count()<=1 for v in bits(T))
 Q=m*n//4;tile=lambda v:(v//n//2)*(n//2)+(v%n//2)
 corners=[[] for _ in range(Q)]
 for v in range(m*n):corners[tile(v)].append(v)
 t=[0]*Q;h=[0]*Q;s=[0]*Q;edges=[];ports=[[] for _ in range(Q)]
 for v in bits(T):t[tile(v)]+=1
 assert max(t)<=2
 for v,w in M:
  a,b=tile(v),tile(w)
  if a==b:h[a]+=1
  elif t[a]==2:s[b]+=1
  elif t[b]==2:s[a]+=1
  else:edges.append((v,w));ports[a].append(v);ports[b].append(w)
 r=[2-t[q]-h[q]-s[q] for q in range(Q)];assert min(r)>=0
 deg=list(map(len,ports));leaves={q for q in range(Q) if r[q]==0 and deg[q]==1}
 for q in range(Q):assert deg[q]<=(1 if not r[q] else 2*r[q])
 assert all(not(tile(v) in leaves and tile(w) in leaves) for v,w in edges)
 pairing={};kind={};pos={};adjp=collections.defaultdict(list);holes=0
 def link(v,w,real):adjp[v].append((w,real));adjp[w].append((v,real))
 for v,w in edges:link(v,w,1);pos[v]=tile(v);pos[w]=tile(w)
 for q in range(Q):
  if not r[q]:
   if deg[q]:kind[ports[q][0]]='L'
   continue
  if r[q]==2:
   assert not(t[q] or h[q] or s[q]);lp=sorted(corners[q])
   for v in lp:
    pos[v]=q
    if v not in ports[q]:
     assert not(A>>v&1);kind[v]='H';holes+=1
   leafports=sorted(v for v in ports[q] if tile(mate[v]) in leaves)
   slack=sorted(v for v in lp if v not in ports[q])
   assert len(leafports)<=2
   forced=[]
   if slack:
    # Use as much local slack as possible. One leaf remains only in the
    # three-real-port/two-leaf case; it is paired to the remaining real port.
    for v,w in zip(leafports,slack):forced.append((v,w))
   else:
    # All four ports are real. Pair each leaf port with the companion
    # corner on the same side through which the leaf edge enters.
    for v in leafports:
     comp=(v+n if (v//n)%2==0 else v-n) if v//n==mate[v]//n else (v+1 if v%2==0 else v-1)
     assert comp in lp and not(comp in ports[q] and tile(mate[comp]) in leaves)
     forced.append((v,comp))
   flat=[v for e in forced for v in e];assert len(flat)==len(set(flat)),('overlap',m,n,T,M,q,forced)
   rest=[v for v in lp if v not in flat];assert len(rest)%2==0
   pp=forced+list(zip(rest[::2],rest[1::2]))
  else:
   lp=sorted(ports[q]);extra=2-deg[q]
   for k in range(extra):
    v=m*n+2*q+k;lp.append(v);pos[v]=q;kind[v]='H';holes+=1
   pp=[tuple(lp)]
  for v,w in pp:link(v,w,0);pairing[v]=w;pairing[w]=v
 for v in pos:assert len(adjp[v])==(1 if v in kind else 2)
 visited=set();paths=[];a=b=c=0;used=0
 for start in kind:
  if start in visited:continue
  v=start;prev=None;length=0;internal=[];visited.add(v)
  while True:
   choices=[(w,z) for w,z in adjp[v] if w!=prev];assert len(choices)==1
   w,real=choices[0];length+=real
   if not real:internal.append(pos[v])
   prev,v=v,w;assert v not in visited;visited.add(v)
   if v in kind:break
  typ=''.join(sorted((kind[start],kind[v])))
  if typ=='LL':a+=1
  elif typ=='HH':b+=1
  else:c+=1
  paths.append(dict(typ=typ,length=length,internal=internal,ends=[pos[start],pos[v]]));used+=length
 for start in pos:
  if start in visited:continue
  stack=[start];visited.add(start);count=0
  while stack:
   v=stack.pop()
   for w,real in adjp[v]:
    count+=real
    if w not in visited:visited.add(w);stack.append(w)
  assert count%2==0;used+=count//2
 assert used==len(edges)
 q=len(edges)-sum(r);D=m*n//2-T.bit_count();K=sum(h)+sum(s);ell=len(leaves)
 assert q==a-b==T.bit_count()+len(M)-m*n//2 and D==sum(r)+K and sum(s)>=ell
 f2=f3=0;charged=set();slack_charged=set()
 for path in paths:
  if path['typ']=='LL' and path['length'] in (2,3):
   if path['length']==2:f2+=1
   else:f3+=1
   choices=[v for v in path['internal'] if h[v]==1]
   if choices:
    v=choices[0];assert v not in charged;charged.add(v)
   else:
    assert path['length']==3,('two-edge nonfork',m,n,T,M,path,r)
    choices=[v for v in path['internal'] if r[v]==2 and deg[v]==3
             and sum(tile(mate[w]) in leaves for w in ports[v])==2]
    assert choices,('unpaid three-edge path',m,n,T,M,path,r,h)
    v=choices[0];assert v not in slack_charged;slack_charged.add(v)
    assert any(p['typ']=='HL' and p['length']==1 and p['ends'][-1]==v or
               p['typ']=='HL' and p['length']==1 and p['ends'][0]==v for p in paths)
 assert f2<=b and f2+f3<=sum(h)+len(slack_charged) and len(slack_charged)<=c
 assert D>=5*q+6*b-f2+2*c-len(slack_charged)>=5*q+5*b+c
 assert 6*T.bit_count()+5*len(M)<=3*m*n
 return dict(q=q,D=D,a=a,b=b,c=c,f2=f2,f3=f3,slack_charges=len(slack_charged),h=sum(h),t=t,r=r,paths=paths)



def no11_checks():
    """Check the explicit bijection, its inverse, and weighted path DP."""
    counts=[];words=0;subsets=0
    for m in range(15):
        image={}
        for mask in range(1<<m):
            words+=1
            if mask&(mask<<1): continue
            covered=mask|(mask<<1)
            free=((1<<(m+1))-1)^covered
            assert free not in image
            image[free]=mask
            # Unique adjacent domino tiling of each even complement interval.
            rebuilt=0;i=0
            while i<=m:
                if free>>i&1:i+=1;continue
                assert i<m and not(free>>(i+1)&1)
                rebuilt|=1<<i;i+=2
            assert rebuilt==mask
        even_gap=set()
        for free in range(1<<(m+1)):
            subsets+=1;i=0;good=True
            while i<=m:
                if free>>i&1:i+=1;continue
                start=i
                while i<=m and not(free>>i&1):i+=1
                if (i-start)%2:good=False;break
            if good:even_gap.add(free)
        assert even_gap==set(image)
        counts.append(len(image))
    assert counts[:9]==[1,2,3,5,8,13,21,34,55]
    assert all(counts[i+2]==counts[i]+counts[i+1] for i in range(len(counts)-2))
    weighted=0
    for m in range(7):
        masks=[b for b in range(1<<m) if not b&(b<<1)]
        for w in itertools.product(range(-2,3),repeat=m):
            dp0=dp1=0
            for weight in w:dp0,dp1=dp1,max(dp1,dp0+weight)
            brute=max(sum(w[i] for i in range(m) if b>>i&1) for b in masks)
            assert dp1==brute;weighted+=1
    return dict(all_words=words,all_boundary_subsets=subsets,
                counts_by_length=counts,weighted_instances=weighted,
                six_bit_total=64,six_bit_admissible=21,
                six_bit_rejected=43,seven_bit_admissible=34)


def planted_checks():
    from grid_three_step_patterns import classification
    report=classification();hist=collections.Counter();examples=[]
    for example in report['all_examples']:
        states={tuple(v):s for v,s in example['states']}
        matching=[tuple(map(tuple,e)) for e in example['edges']]
        for reflection in range(2):
            for rotation in range(4):
                def transform(v):
                    x,y=v
                    if reflection:y=-y-1
                    for _ in range(rotation):x,y=y,-x-1
                    return x,y
                transformed={transform(v):s for v,s in states.items()}
                transformed_m=[(transform(v),transform(w)) for v,w in matching]
                low_x=min(v[0] for v in transformed)//2*2
                low_y=min(v[1] for v in transformed)//2*2
                for dr,dc in itertools.product((0,2,4),repeat=2):
                    dx=-low_x+dr;dy=-low_y+dc
                    m=2*((max(v[0]+dx for v in transformed)+2)//2)+2
                    n=2*((max(v[1]+dy for v in transformed)+2)//2)+2
                    def index(v):return (v[0]+dx)*n+v[1]+dy
                    selected=[index(v) for v,s in transformed.items() if s=='T']
                    T=sum(1<<v for v in selected)
                    M=tuple((index(v),index(w)) for v,w in transformed_m)
                    z=canonical(m,n,T,M)
                    hist['cases']+=1;hist['three_edge_paths']+=z['f3']
                    hist['two_edge_paths']+=z['f2'];hist['slack_charges']+=z['slack_charges']
                    assert z['f3']>=1
                    if len(examples)<3:
                        examples.append(dict(m=m,n=n,T=selected,M=M,
                                             counts={k:z[k] for k in ('q','D','a','b','c','f2','f3','h','slack_charges')}))
    for extra in (False,True):
        selected=[0,5,12,17,19,22]
        T=sum(1<<v for v in selected)
        M=((1,2),(3,4),(7,13),(10,16),(8,9))+(((14,15),) if extra else ())
        z=canonical(4,6,T,M)
        assert z['f2']==1
        hist['earlier_fork_cases']+=1;hist['earlier_two_edge_paths']+=z['f2']
        examples.append(dict(m=4,n=6,T=selected,M=M,
                             counts={k:z[k] for k in ('q','D','a','b','c','f2','f3','h','slack_charges')}))
    return dict(summary=dict(hist),local_cases=report['total'],
                accepted_local_cases=len(report['all_examples']),
                local_table=report['table'],local_rejections=report['rejections'],
                examples=examples)


def check_r2():
 from itertools import product,combinations
 from collections import Counter
 from grid_three_step_patterns import Patch,Conflict,CORNERS,point,add,tile_of
 hist=Counter();examples=[]
 for deg in (2,3,4):
  for real in combinations(CORNERS,deg):
   for ell in (1,2):
    if ell>deg:continue
    for leaves in combinations(real,ell):
     nonleaf=[c for c in real if c not in leaves]
     for choices in product(range(2),repeat=deg):
      dirs={c:(((-1 if c[0]==0 else 1),0),(0,(-1 if c[1]==0 else 1)))[i] for c,i in zip(real,choices)}
      for shapes in product(range(3),repeat=ell):
       hist['attempts']+=1;p=Patch()
       try:
        p.shape((0,0),{c:'P' if c in real else 'B' for c in CORNERS},'r2')
        for c,shape in zip(leaves,shapes):p.leaf(point((0,0),c),dirs[c],shape)
        for c in nonleaf:
         v=point((0,0),c);w=add(v,dirs[c])
         if p.roles.get(tile_of(w)) in ('leaf','sat','r2'):raise Conflict('nonleaf_role')
         p.edge(v,w)
        p.finish()
       except Conflict as e:hist['rejected']+=1;continue
       minx=min(v[0] for v in p.states)//2*2;miny=min(v[1] for v in p.states)//2*2
       dx=2-minx;dy=2-miny
       m=2*((max(v[0]+dx for v in p.states)+2)//2)+2;n=2*((max(v[1]+dy for v in p.states)+2)//2)+2
       index=lambda v:(v[0]+dx)*n+v[1]+dy
       selected=[index(v) for v,s in p.states.items() if s=='T'];T=sum(1<<v for v in selected)
       M=tuple((index(v),index(w)) for v,w in p.mate.items() if v<w)
       r=canonical(m,n,T,M)
       center=(dx//2)*(n//2)+dy//2
       assert r['r'][center]==2
       hist['accepted']+=1;hist[f'deg{deg}_leaves{ell}']+=1
       hist['f2']+=r['f2'];hist['f3']+=r['f3'];hist['slack_charges']+=r['slack_charges']
       if len(examples)<3:examples.append(dict(m=m,n=n,T=selected,M=M,center=center,degree=deg,leaves=ell))
 return dict(summary=dict(hist),examples=examples)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('grid-five-sixths-verification.json'))
    parser.add_argument('--random-per-size',type=int,default=100)
    args=parser.parse_args()
    if args.random_per_size<0:parser.error('--random-per-size must be nonnegative')
    report={'scope':'Exact finite regression checks; universal paper proofs are separate. No full conjecture, Lean, or CI claim.',
            'no11':no11_checks(),'exhaustive':[],'random':[]}
    for m,n in [(2,2),(2,4),(2,6),(4,4)]:
        count=0;hist=collections.Counter()
        for T,A,M in pairs(m,n):
            z=canonical(m,n,T,M);count+=1
            hist['two_edge_paths']+=z['f2'];hist['three_edge_paths']+=z['f3']
        row=dict(m=m,n=n,pairs=count,path_counts=dict(hist))
        report['exhaustive'].append(row);print(json.dumps(row),flush=True)
    rng=random.Random(2026092801)
    for m,n in [(4,6),(6,6),(8,10),(12,14),(20,20)]:
        adj,E=graph(m,n);hist=collections.Counter()
        for _ in range(args.random_per_size):
            A=T=0;M=[];rng.shuffle(E)
            for v,w in E:
                mask=(1<<v)|(1<<w)
                if not(A&mask) and rng.random()<0.3:A|=mask;M.append((v,w))
            vertices=list(range(m*n));rng.shuffle(vertices)
            for v in vertices:
                bit=1<<v
                if not(A&bit) and all((adj[w]&(A|bit)).bit_count()<=1 for w in bits(T|bit)):
                    T|=bit;A|=bit
            z=canonical(m,n,T,M)
            hist['two_edge_paths']+=z['f2'];hist['three_edge_paths']+=z['f3']
        report['random'].append(dict(m=m,n=n,pairs=args.random_per_size,path_counts=dict(hist)))
    report['random_seed']=2026092801
    report['planted']=planted_checks()
    report['capacity_two_patches']=check_r2()
    report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    classifier=Path(__file__).with_name('grid_three_step_patterns.py')
    report['classifier_sha256']=hashlib.sha256(classifier.read_bytes()).hexdigest()
    report['limitations']=[
        'The small exhaustive and random cases have no two/three-edge LL paths; the planted cases test these nonvacuously.',
        'The route is a specified auxiliary pairing, not enumeration of every possible pairing.',
        'The slack-paid exceptional routing case is retained in the proof; these planted witnesses use internal-edge charges.',
        'No weighted quotient of the full two-dimensional frontier into 21 states is claimed.'
    ]
    report['result']='ALL_LISTED_CHECKS_PASSED'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['planted']['summary']),flush=True)
    print(report['result'],flush=True)

if __name__=='__main__':main()
