"""Independent tests of physical simultaneous K4 repair and its exact family."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
from functools import lru_cache
import argparse,json,random,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from k4_contact_repair import pair_choices,pseudoforest_choices,certificate,cyclic_family
from owner_matching_certificate import prepare,materialize,three_colour
from all_helper_optimization import solve
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();rng=random.Random(161126)


def graph_components(n,E):
    adj=[set() for _ in range(n)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    unseen=set(range(n));out=[]
    while unseen:
        K={min(unseen)};todo=list(K)
        while todo:
            for v in adj[todo.pop()]-K:K.add(v);todo.append(v)
        unseen-=K;out.append(K)
    return out,adj


def sat_control(pairs,contacts):
    x=pair_choices(pairs,contacts);best=[]
    for choices in product(range(2),repeat=len(pairs)):
        S={p[j] for p,j in zip(pairs,choices)}
        valid=all(not (a in S and b in S) for a,b in contacts)
        if valid:best.append(S)
        counts['literal_pair_assignments']+=1
    assert x['feasible']==bool(best)
    pseudo=pseudoforest_choices(pairs,contacts)
    if pseudo is not None:
        assert best and set(pseudo['chosen']) in best
        assert len(pseudo['edge_owner'])==len(contacts)
        assert len({owner for e,owner in pseudo['edge_owner']})==len(contacts)
        for e,owner in pseudo['edge_owner']:assert set(contacts[e])&set(pairs[owner])
        counts['pseudoforest_orientation_controls']+=1
    if x['feasible']:
        assert set(x['chosen']) in best;counts['feasible_contact_models']+=1
    else:
        counts['unsatisfiable_contact_models']+=1
        o=x['obstruction'];arcs=set()
        for clause in x['clauses']:
            a,b=[2*v+p for v,p in clause];arcs.update(((a,b^1),(b,a^1)))
        for key,start,end in [('zero_to_one',2*o['variable'],2*o['variable']+1),('one_to_zero',2*o['variable']+1,2*o['variable'])]:
            path=o[key];assert path[0]==start and path[-1]==end and all(e in arcs for e in zip(path,path[1:]));counts['literal_SCC_paths']+=1
    counts['contact_models']+=1


for k in range(4):
    pairs=[(2*j,2*j+1) for j in range(k)];possible=[e for e in combinations(range(2*k),2) if e[0]//2!=e[1]//2]
    for mask in range(1<<len(possible)):
        E=[e for j,e in enumerate(possible) if mask>>j&1];sat_control(pairs,E);counts['complete_small_contact_graphs']+=1
for _ in range(340):
    k=rng.randrange(4,10);pairs=[(2*j,2*j+1) for j in range(k)];E=[e for e in combinations(range(2*k),2) if e[0]//2!=e[1]//2 and rng.randrange(8)==0]
    sat_control(pairs,E);counts['seeded_contact_graphs']+=1

# Exhaustive literal feasibility of the iterative shared colouring supplier,
# including failure on K4. This checks actual assignments, not search frames.
for k in range(6):
    possible=list(combinations(range(k),2))
    for mask in range(1<<len(possible)):
        E=[e for j,e in enumerate(possible) if mask>>j&1]
        if any(sum(v in e for e in E)>3 for v in range(k)):continue
        feasible=any(all(c[a]!=c[b] for a,b in E) for c in product(range(3),repeat=k))
        try:labels=three_colour(range(k),E)
        except AssertionError:assert not feasible;counts['literal_colour_rejections']+=1
        else:assert feasible and all(labels[a]!=labels[b] for a,b in E)
        counts['complete_small_colouring_controls']+=1


def physical(x,owners,witnesses):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def add(a,c):G[a].add(c);G[c].add(a)
    for j,(a,c) in enumerate(x['P']):add(j,b+a);add(j,b+c)
    for v in range(n):add(b+v,3*b+v)
    for a,c in x['Q']:add(b+a,b+c)
    for a,c in x['B']:add(3*b+a,3*b+c)
    col=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(col[v]!=col[w] for v in range(5*b) for w in G[v])
    D=set(range(b))|{b+v for v in witnesses}|{3*b+v for v in owners}
    assert len(D)==b+len(owners)+len(witnesses)
    assert all(len(G[v]&D)<=1 for v in D)
    assert max(map(len,G),default=0)<=3
    counts['literal_physical_certificates']+=1
    return G,len(D)


def matching(n,E,U):
    adj=[0]*n
    for a,b in E:adj[a]|=1<<b;adj[b]|=1<<a
    @lru_cache(None)
    def f(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;best=f(rest);W=adj[v]&rest
        while W:
            z=W&-W;W^=z;best=max(best,1+f(rest^z))
        return best
    return f(sum(1<<v for v in U))


def inspect(x,R=None,labels=None,exact=False):
    rec=certificate(**x,R=R,exterior_colouring=labels);n=2*x['b'];data=rec.get('contact')
    if data is not None:
        rr=[tuple(e) for e in data['R']];Rmate={v:j for j,e in enumerate(rr) for v in e};special=set(data['owner_square_vertices'])
        assert sorted(v for e in rr for v in e)==list(range(n))
        FF=[tuple(e) for e in x['B'] if not set(e)&special and tuple(sorted(e)) not in rr]
        H={j:set() for j in range(n//2)}
        for a,b in FF:H[Rmate[a]].add(Rmate[b]);H[Rmate[b]].add(Rmate[a])
        parts={v:j for j,p in enumerate(data['pairs']) for v in p};expected=set()
        for a,b in combinations(parts,2):
            if parts[a]!=parts[b] and (b in H[a] or H[a]&H[b]):expected.add((min(a,b),max(a,b)))
        assert expected=={tuple(e) for e in data['contacts']}
        for row in data['contact_paths']:
            path=row['path'];assert len(path) in (2,3) and set((path[0],path[-1]))==set(row['contact'])
            assert all(b in H[a] for a,b in zip(path,path[1:]));counts['physical_contact_path_witnesses']+=1
        KK,JJ=graph_components(n,x['P']+x['Q']+rr)
        bad=[K for K in KK if len(K)==4 and all(len(JJ[v])==3 for v in K)]
        assert {tuple(sorted(K)) for K in bad}=={tuple(K) for K in data['bad']}
        counts['physical_K4_components']+=len(bad)
    if not rec['applicable']:
        counts['criterion_rejections']+=1
        if 'choice' in rec:assert not rec['choice']['feasible']
        return rec
    total=0
    for s in rec['direct_sets']:
        _,z=physical(x,s['owners'],s['witnesses']);assert z==s['size'];total+=z
    assert total==8*x['b']==rec['direct_size_sum']
    _,z=physical(x,rec['owners'],rec['witnesses']);assert z==rec['beta_I_lower']==3*x['b']-rec['cost']>=(8*x['b']+2)//3
    U=set(rec['U']);T=set(rec['witnesses']);M=rec['matching'];cover=U-T
    assert len(cover)==len(M)==rec['cost'] and len({v for e in M for v in e})==2*len(M)
    EE={tuple(sorted(e)) for e in x['P']+x['Q']}
    assert all(tuple(sorted(e)) in EE and set(e)<=U for e in M)
    assert all(a in cover or b in cover for a,b in EE if a in U and b in U)
    if n<=16:assert matching(n,x['P']+x['Q'],U)==len(M);counts['independent_matching_controls']+=1
    if exact:
        optimum=solve(x['b'],x['P'],x['Q'],x['B'])['beta_I'];assert optimum>=z;counts['exact_all_helper_controls']+=1
    counts['successful_physical_models']+=1
    counts['physical_pseudoforest_models']+=rec['pseudoforest']
    counts['successful_multiple_K4_models']+=len(data['bad'])>=2
    counts['virtual_owner_square_models']+=bool(data['owner_square_vertices'])
    digest.update(json.dumps([x,rec],sort_keys=True).encode())
    return rec


# Arbitrary crossing owner even paths/cycles, partialQ and ownerC4 diagonals.
for trial in range(220):
    n=rng.choice([4,8,12,16,20,24,32,48,64,96]);P=[];Q=[];col=[];off=0
    while off<n:
        m=rng.choice(list(range(4,min(16,n-off)+1,4)));K=list(range(off,off+m));off+=m
        P.extend(zip(K[::2],K[1::2]));Q.extend((K[j],K[(j+1)%m]) for j in range(1,m,2) if rng.randrange(8)!=0)
        col.extend((j//2)%2 for j in range(m))
    white=[v for v in range(n) if col[v]];black=[v for v in range(n) if not col[v]];rng.shuffle(white);rng.shuffle(black)
    order=[v for pair in zip(white,black) for v in pair];B=[];off=0
    while off<n:
        m=rng.choice(list(range(2,min(12,n-off)+1,2)));K=order[off:off+m];off+=m;B.extend(zip(K,K[1:]))
        if m>=4 and rng.randrange(3):B.append((K[-1],K[0]))
    inspect(dict(b=n//2,P=P,Q=Q,B=B,colour=col),exact=n<=8);counts['seeded_general_physical_models']+=1


# Bias toward many actual K4s, while arbitrary owner cycles interact with them.
for trial in range(180):
    r=rng.randrange(1,9);long=rng.randrange(2,5);n=4*r+4*long;P=[];Q=[];col=[];R=[]
    for off in range(0,4*r,4):
        P.extend([(off,off+1),(off+2,off+3)]);Q.extend([(off+1,off+2),(off+3,off)]);col.extend([0,0,1,1]);R.extend([(off,off+2),(off+1,off+3)])
    K=list(range(4*r,n));P.extend(zip(K[::2],K[1::2]));Q.extend((K[j],K[(j+1)%len(K)]) for j in range(1,len(K),2));col.extend((j//2)%2 for j in range(len(K)))
    L=[v for v in K if not col[v]];RR=[v for v in K if col[v]];rng.shuffle(RR);R.extend(zip(L,RR));mate={v:w for a,b in R for v,w in [(a,b),(b,a)]}
    allL=[v for v in range(n) if not col[v]];allR=[v for v in range(n) if col[v]]
    for attempt in range(300):
        rng.shuffle(allR);F=list(zip(allL,allR))
        if any(mate[a]==b for a,b in F):continue
        B=R+F;parts,adj=graph_components(n,B)
        if any(len(K)==4 for K in parts):continue
        break
    else:raise AssertionError('Seeded no-owner-C4 matching not found')
    inspect(dict(b=n//2,P=P,Q=Q,B=B,colour=col),R=R,exact=n<=12);counts['seeded_many_K4_physical_models']+=1


# Local phase table and exact partial block, independently checked.
base=json.loads((ROOT/'develop/fixtures/k4-contact-base.json').read_text());keys=['b','P','Q','B','colour'];original={k:base[k] for k in keys};d=prepare(**original)
used=set()
for phase in product(range(2),repeat=2):
    bad=materialize(d,phase)['K4'];assert bad==base['local_R_phase_bad_blocks'][''.join(map(str,phase))]
    assert len(bad)>=1;used|={v for K in bad for v in K};counts['literal_base_owner_phases']+=1
free=base['free_Q_edge'];assert set(free)<=({4,7,8,13}-used)
partial=dict(original,Q=[e for e in original['Q'] if e!=free])
local=solve(partial['b'],partial['P'],partial['Q'],partial['B']);assert local['beta_I']==23
counts['exact_partial_block_optima']+=1
# All 24 maximal independent sets: literal owner triples witness the zero-cost
# impossibility. The general note gives a two-case logical proof as well.
three=[[(0,1),(2,3)],[(9,10),(11,12)],[(5,6),(14,15)]]
for choices in product(range(2),repeat=3):
    U0=set(v for pair,j in zip(three,choices) for v in pair[j])
    for extra in [(4,7),(4,13),(8,13)]:
        U=U0|set(extra);S=set(range(16))-U
        assert all(not set(e)<=U for e in partial['P']+partial['Q'])
        assert any(sum(v in e and set(e)<=S for e in partial['B'])>=2 for v in S)
        counts['maximal_independent_local_obstructions']+=1
family=[]
for r in (2,3,4,5,8,12,16,24,32,64):
    x=cyclic_family(r);labels={v+16*j:c for j in range(r) for v,c in base['fixed_exterior_colouring']};rec=inspect(x,labels=labels)
    n=16*r;parts,adj=graph_components(n,x['P']+x['Q']);assert Counter(map(len,parts))==Counter({4:3*r,4*r:1})
    bparts,badj=graph_components(n,x['B']);assert len(bparts)==2*r and all(len(K)==8 for K in bparts)
    G,z=physical(x,rec['owners'],rec['witnesses']);partsG,_=graph_components(40*r,[(a,b) for a in range(40*r) for b in G[a] if a<b])
    assert len(partsG)==1 and min(map(len,G))==2 and max(map(len,G))==3
    assert len(rec['contact']['bad'])==r and not rec['contact']['contacts']
    assert rec['beta_I_lower']==23*r and [s['size'] for s in rec['direct_sets']]==[23*r,22*r,19*r]
    assert rec['cost']==r and rec['pseudoforest']
    if r<=5:
        dd=prepare(**x)
        for phase in product(range(2),repeat=2*r):
            assert len(materialize(dd,phase)['K4'])>=r;counts['literal_family_owner_phases']+=1
    if r>=4:assert 3*r-1>8*r//3;counts['beyond_named_global_criteria']+=1
    counts['exact_family_constructions']+=1
    family.append(dict(r=r,actual_order=40*r,helpers=8*r,beta_I=23*r,cost=r,target=(64*r+2)//3,direct_sizes=[z['size'] for z in rec['direct_sets']],unavoidable_K4_min=r))
    if r==4:critical=dict(model=x,certificate=rec)


# The criterion is sufficient, not necessary: its contact2SAT fails although
# the physical target holds at equality, with an independently exact optimum.
x=dict(b=4,P=[(0,4),(1,5),(2,6),(3,7)],Q=[(4,1),(5,0),(6,3),(7,2)],B=[(j,(j+1)%8) for j in range(8)],colour=[j%2 for j in range(8)])
reject=inspect(x);assert not reject['applicable']
rejection_model=x
opt=solve(x['b'],x['P'],x['Q'],x['B']);assert opt['beta_I']==11==(8*x['b']+2)//3
physical(x,opt['owners'],opt['witnesses']);counts['criterion_not_necessary_control']+=1
empty=inspect(dict(b=0,P=[],Q=[],B=[],colour=[]));assert empty['beta_I_lower']==0
# A genuine exterior larger than the default recursion limit; no supplied
# colouring. Auxiliary C1200, physical owner C4s, virtual R=P.
nlarge=1200
large=dict(b=nlarge//2,P=[(j,j+1) for j in range(0,nlarge,2)],Q=[(j,(j+1)%nlarge) for j in range(1,nlarge,2)],
           B=[(off+a,off+b) for off in range(0,nlarge,4) for a,b in ((0,2),(2,1),(1,3),(3,0))],colour=[(j//2)%2 for j in range(nlarge)])
rec=inspect(large);assert rec['applicable'] and len(rec['exterior_colouring'])==nlarge
counts['iterative_exterior_above_default_recursion_limit']+=1
odd=certificate(1,[(0,1)],[],[],[0,0]);assert not odd['applicable'];counts['odd_owner_path_rejection']+=1
for invalid in (0,1,True,2.5):
    try:cyclic_family(invalid)
    except ValueError:counts['invalid_family_rejections']+=1
    else:raise AssertionError('Invalid family parameter accepted')
for x in [dict(b=2,P=[(0,1),(2,3)],Q=[(1,2),(3,0)],B=[(0,2),(2,1),(1,3),(3,0)],colour=[0,0,1,1])]:
    rec=inspect(x,exact=True);assert rec['contact']['owner_square_vertices']
    try:certificate(**x,R=[(0,2),(1,3)])
    except ValueError:counts['invalid_actual_owner_square_R_rejection']+=1
    else:raise AssertionError('Owner square must use virtual diagonals')
assert counts['successful_multiple_K4_models'] and counts['unsatisfiable_contact_models'] and counts['criterion_rejections']
report=dict(counts=dict(sorted(counts.items())),deterministic_sha256=digest.hexdigest(),family=family,critical_example=critical,criterion_failure=dict(model=rejection_model,contact=reject['contact'],optimum=opt),scope='Sufficient actual contact2SAT repair; arbitrary owner even paths/even cycles and auxiliary components. Exact family23r on40rvertices; no universal mixedcyclic target or unrestricted beta/SF optimum claim.')
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/k4-contact-repair-check.json');args=parser.parse_args();args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('critical_example','criterion_failure')}))
