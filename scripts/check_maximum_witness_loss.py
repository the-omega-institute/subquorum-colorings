from pathlib import Path
from collections import Counter
from itertools import product
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from maximum_witness_loss import instance
from all_helper_optimization import solve
from owner_matching_certificate import prepare,certificate as matching
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();digest=hashlib.sha256()

# Independent literal local model: all256 subsets of a path of order eight.
local=[]
for mask in range(256):
    counts['literal_local_subsets']+=1
    if any(mask>>v&3==3 for v in range(7)):continue
    e=sum(mask>>v&1 for v in (0,2,4,6));o=sum(mask>>v&1 for v in (1,3,5,7))
    g=min(e,2)+min(o,2)
    assert g<=4
    if g==4:assert mask&1 and mask&128 and mask.bit_count()==4 and e==o==2
    local.append((mask&1,mask>>7&1,g,mask))
    counts['independent_local_subsets']+=1
# Every possible forbidden set in a C4 independently confirms min(2,4-k).
for forbidden in range(16):
    best=0
    for selected in range(16):
        counts['literal_C4_pairs']+=1
        if selected&forbidden:continue
        if any(selected>>v&1 and (bool(selected>>((v-1)%4)&1)+bool(selected>>((v+1)%4)&1)>1) for v in range(4)):continue
        best=max(best,selected.bit_count())
    assert best==min(2,4-forbidden.bit_count())

def exact_witness_dp(r):
    # Full local independent-subset vectors, preserving both boundary bits.
    # Cyclic closure is checked after r blocks; no claimed formula is used.
    answer=-1
    for first in (0,1):
        state={last:g for f,last,g,m in local if f==first}
        # Multiple subsets can share a boundary state: retain the best value.
        state={last:max(g for f,z,g,m in local if f==first and z==last) for last in state}
        for i in range(1,r):
            nxt={}
            for previous,value in state.items():
                for start,end,g,m in local:
                    counts['vector_transitions']+=1
                    if previous and start:continue
                    nxt[end]=max(nxt.get(end,-1),value+g)
            state=nxt
        answer=max(answer,max(value for last,value in state.items() if not(last and first)))
    return answer


def articulation_points(g):
    # Independent iterative low-link certificate; avoids a size-dependent
    # recursion limit on the largest physical graph.
    tin={0:0};low={0:0};parent={};children=Counter();cut=set()
    stack=[(0,iter(g[0]))]
    while stack:
        v,neighbours=stack[-1]
        try:u=next(neighbours)
        except StopIteration:
            stack.pop()
            if v in parent:
                p=parent[v];low[p]=min(low[p],low[v])
                if p in parent and low[v]>=tin[p]:cut.add(p)
            elif children[v]>1:cut.add(v)
            continue
        if parent.get(v)==u:continue
        if u in tin:low[v]=min(low[v],tin[u])
        else:
            parent[u]=v;children[v]+=1;tin[u]=len(tin);low[u]=tin[u]
            stack.append((u,iter(g[u])))
    assert len(tin)==len(g)
    return cut

def verify(r):
    x=instance(r);n=8*r;b=4*r
    prepare(b,x['P'],x['Q'],x['B'],x['colour'])
    g=[set() for _ in range(5*b)]
    def edge(u,v):g[u].add(v);g[v].add(u)
    for i,(u,v) in enumerate(x['P']):edge(i,b+u);edge(i,b+v)
    for u,v in x['Q']:edge(b+u,b+v)
    for v in range(n):edge(b+v,3*b+v)
    for u,v in x['B']:edge(3*b+u,3*b+v)
    selected=set(range(b))|{b+v for v in x['witnesses']}|{3*b+v for v in x['owners']}
    assert len(selected)==x['beta_I']==11*r+r//2
    assert all(len(g[v]&selected)<=1 for v in selected)
    physical_colour={}
    for v in range(n):physical_colour[b+v]=x['colour'][v];physical_colour[3*b+v]=1-x['colour'][v]
    for i,(u,v) in enumerate(x['P']):physical_colour[i]=1-x['colour'][u]
    assert all(physical_colour[v]!=physical_colour[u] for v in range(5*b) for u in g[v])
    seen={0};todo=[0]
    while todo:
        for u in g[todo.pop()]-seen:seen.add(u);todo.append(u)
    assert len(seen)==5*b and min(map(len,g))==2 and max(map(len,g))==3
    assert not articulation_points(g);counts['two_connectivity_certificates']+=1
    if r<=8:
        for removed in range(5*b):
            reached={int(removed==0)};queue=list(reached)
            while queue:
                for u in g[queue.pop()]-reached-{removed}:reached.add(u);queue.append(u)
            assert len(reached)==5*b-1;counts['single_vertex_deletion_controls']+=1
    assert exact_witness_dp(r)+8*r==x['beta_I']
    counts['full_vector_exact_optima']+=1
    # The two maximum auxiliary-independent sets are independently scored.
    for phase in (0,1):
        T=set(range(phase,n,2));remaining=set(range(n))-T
        owner_blocks=[{8*i+p+2*j for j in range(4)} for i in range(r) for p in (0,1)]
        owner_opt=sum(min(2,len(K&remaining)) for K in owner_blocks)
        assert b+len(T)+owner_opt==10*r==x['maximum_witness_restricted_optimum']
        counts['maximum_witness_phase_controls']+=1
    if r<=2:
        exact=solve(b,x['P'],x['Q'],x['B'])
        assert exact['beta_I']==x['beta_I'];counts['exact_original_all_helper_controls']+=1
        # Literal independent sets verify the maximum-witness restriction itself.
        largest=0;largest_sets=[]
        for mask in range(1<<n):
            counts['literal_auxiliary_subsets']+=1
            if any(mask>>u&1 and mask>>v&1 for u,v in x['P']+x['Q']):continue
            size=mask.bit_count()
            if size>largest:largest=size;largest_sets=[mask]
            elif size==largest:largest_sets.append(mask)
        assert largest==b and len(largest_sets)==2
    if r<=8:
        assert matching(prepare(b,x['P'],x['Q'],x['B'],x['colour']))['feasible']
        counts['prior_matching_certificate_controls']+=1
    counts['physical_certificates']+=1
    digest.update(json.dumps(x,sort_keys=True).encode())
    return x

examples=[verify(r) for r in range(1,65)]
for r in (96,128,256):verify(r)
for bad in (0,-1,True,1.5):
    try:instance(bad)
    except ValueError:counts['invalid_inputs_rejected']+=1
    else:raise AssertionError('invalid input accepted')
fixture=json.loads((ROOT/'develop/fixtures/maximum-witness-loss.json').read_text())
assert fixture==json.loads(json.dumps(examples[:2]));counts['fixed_fixture_controls']+=2
report={'counts':dict(sorted(counts.items())),'examples':[{'r':x['r'],'physical_vertices':20*x['r'],'beta_I':x['beta_I'],'maximum_witness_restricted_optimum':x['maximum_witness_restricted_optimum'],'loss':x['restricted_loss']} for x in examples[:6]],'largest_physical_vertices':5120,'deterministic_sha256':digest.hexdigest(),'scope':'General written all-r theorem. Original exponential all-helper optimizer used only for r1and2. Full-vector DP retains all local independent subsets and verifies exact optima on all listed r; larger physical graphs certify actual sets. This refutes maximum-witness retention, not general8b/3, nor any unrestricted beta_2 claim.'}
parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
out=Path(args.output) if args.output else ROOT/'output/maximum-witness-loss-check.json'
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
