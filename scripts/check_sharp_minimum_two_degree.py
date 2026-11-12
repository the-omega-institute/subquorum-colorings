#!/usr/bin/env python3
"""Independent literal and closed-table checks of the exact interface theorem."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
import witness_interface_optimizer as opt

if not __debug__:raise RuntimeError('Run with assertions enabled.')


def diss(g,Q):return all(len(g[x]&Q)<=1 for x in Q)


def literal(g,S,x,removed=None):
    # Enumerate physical stars at their centres, independently of active-neighbour rules.
    inside=lambda v:v in S and v!=removed
    for centre in {x}|g[x]:
        if centre!=x and not inside(centre):continue
        for a,b in combinations([v for v in g[centre]if v==x or inside(v)],2):
            if x in(centre,a,b)and sum(inside(v)for v in(centre,a,b))==2:return True
    return False


def one_part_beta(g):
    col={}
    for root in range(len(g)):
        if root in col:continue
        col[root]=0;todo=[root]
        while todo:
            a=todo.pop()
            for b in g[a]:
                if b not in col:col[b]=1-col[a];todo.append(b)
                assert col[b]!=col[a]
    left=[a for a in col if col[a]==0];right=[a for a in col if col[a]==1]
    if len(left)>len(right):left,right=right,left
    masks=[sum(1<<j for j,a in enumerate(left)if a in g[b])for b in right]
    best=0
    for mask in range(1<<len(left)):
        free=0;single=set()
        for neighbours in masks:
            hits=mask&neighbours
            if hits==0:free+=1
            elif hits&(hits-1)==0:single.add(hits)
        best=max(best,mask.bit_count()+free+len(single))
    return best,1<<len(left)


NO_U=((3,3,2),(3,2,1),(3,2,1))
U_ZERO=((2,2,2),(2,2,1),(2,1,1))
DIST_ZERO=((2,2,2),(1,1,1),(1,1,1))


def closed_wing(p,w,sat):
    no=zero=0;available=False
    for j in range(p):
        a=0 if not(w>>(2*j)&1)else 2 if sat>>(2*j)&1 else 1
        b=0 if not(w>>(2*j+1)&1)else 2 if sat>>(2*j+1)&1 else 1
        no+=NO_U[a][b];zero+=(DIST_ZERO if j==0 else U_ZERO)[a][b]
        available|=b==0
    return w.bit_count()+max(no,1+zero+available)


def table_controls():
    cases=0
    for a,b,u,dist in product(range(3),range(3),range(2),range(2)):
        w=(a>0)+2*(b>0);sat=(a==2)+2*(b==2)
        # Physical vertices c,x,y,i,a,b,u and two private external neighbours.
        g=[set()for _ in range(9)]
        es=[(0,1),(0,2),(1,4),(2,5),(3,5),(6,3)]
        if dist:es.append((6,2))
        if a==2:es.append((4,7))
        if b==2:es.append((5,8))
        for x,y in es:g[x].add(y);g[y].add(x)
        fixed=({4}if a else set())|({5}if b else set())|({6}if u else set())
        fixed|=({7}if a==2 else set())|({8}if b==2 else set())
        truth={}
        for mask in range(16):
            Q=fixed|{j for j in range(4)if mask>>j&1}
            if diss(g,Q):
                used=len(g[6]&Q)if u else 0
                truth[used]=max(truth.get(used,-1),mask.bit_count())
        computed=opt.local_options(w,sat,u,dist)
        assert {k:v[0]for k,v in computed.items()}==truth
        if not u:assert truth[0]==NO_U[a][b]
        else:
            assert truth[0]==(DIST_ZERO if dist else U_ZERO)[a][b]
            assert truth.get(1)==(truth[0]+1 if b==0 else None)
        cases+=1
    # Independent full physical wing subsets, then every possible external saturation.
    wing_rows=[]
    for p in(1,2):
        g,_=opt.graph(p,p,[0]*(2*p));vertices=list(range(6*p))+[12*p]
        ws=[6*j+a for j in range(p)for a in(4,5)];truth={}
        for mask in range(1<<len(vertices)):
            Q={x for i,x in enumerate(vertices)if mask>>i&1}
            if not diss(g,Q):continue
            w=sum(1<<j for j,x in enumerate(ws)if x in Q)
            can_sat=sum(1<<j for j,x in enumerate(ws)if x in Q and not(g[x]&Q))
            sat=can_sat
            while True:
                truth[w,sat]=max(truth.get((w,sat),-1),len(Q))
                if sat==0:break
                sat=(sat-1)&can_sat
        for(w,sat),value in truth.items():assert opt.wing(p,w,sat)[0]==closed_wing(p,w,sat)==value
        assert len(truth)==3**(2*p)
        wing_rows.append({'p':p,'literal_subsets':1<<len(vertices),'ternary_states':len(truth)})
    # All ternary witness states of a whole5-block wing, DP versus closed table.
    count=0
    for states in product(range(3),repeat=10):
        w=sum(1<<j for j,s in enumerate(states)if s);sat=sum(1<<j for j,s in enumerate(states)if s==2)
        assert opt.wing(5,w,sat)[0]==closed_wing(5,w,sat)
        count+=1
    return {'physical_local_cases':cases,'literal_whole_wings':wing_rows,'all_p5_ternary_states':count}


def small_controls():
    rows=[];totals=Counter();rng=random.Random(2026111210)
    models=[]
    for pl,pr in((1,1),(1,2),(2,1)):
        for bits in range(1<<(4*pl*pr)):
            adj=[(bits>>(a*2*pr))&((1<<(2*pr))-1)for a in range(2*pl)]
            models.append(('all_R_'+str(pl)+'_'+str(pr),pl,pr,adj))
    for pl,pr,trials in((2,2,24),(3,3,4)):
        for _ in range(trials):models.append(('seeded_R_'+str(pl)+'_'+str(pr),pl,pr,[rng.randrange(1<<(2*pr))for _ in range(2*pl)]))
    for label,pl,pr,adj in models:
        g,S=opt.graph(pl,pr,adj);result=opt.exact(pl,pr,adj);beta,subsets=one_part_beta(g)
        assert result['beta']==beta and diss(g,set(result['attaining_set']))and len(result['attaining_set'])==beta
        assert all(literal(g,S,x)for x in range(len(g))if x not in S)
        assert all(any(not literal(g,S,x,removed=v)for x in(set(range(len(g)))-S)|{v})for v in S)
        totals['graph_inputs']+=1;totals['one_part_subsets']+=subsets;totals['literal_minimal_selections']+=1
        totals['feasible_witness_pairs']+=sum(row['feasible_pairs']for row in result['rows'])
        row=next((r for r in rows if r['range']==label),None)
        if row is None:row={'range':label,'models':0};rows.append(row)
        row['models']+=1
    return {'totals':dict(totals),'ranges':rows,'scope':'Every witness graph R at the three stated part sizes, plus labelled seeded ranges; one recipe-defined selection per graph.'}


def independent_frontier(g,p):
    # Enumerate every pair of physical witness subsets, without optimizer pruning.
    L=[6*j+a for j in range(p)for a in(4,5)]
    R=[6*j+a for j in range(p,2*p)for a in(4,5)]
    Lsets=[{x for j,x in enumerate(L)if mask>>j&1}for mask in range(1<<(2*p))]
    Rsets=[{x for j,x in enumerate(R)if mask>>j&1}for mask in range(1<<(2*p))]
    caps=[];counts=[];classes={}
    for left,A in enumerate(Lsets):
        maximum=-1;count=0
        for right,B in enumerate(Rsets):
            if any(len(g[x]&B)>1 for x in A)or any(len(g[x]&A)>1 for x in B):continue
            satA=sum(1<<j for j,x in enumerate(L)if x in A and g[x]&B)
            satB=sum(1<<j for j,x in enumerate(R)if x in B and g[x]&A)
            score=closed_wing(p,left,satA)+closed_wing(p,right,satB)
            maximum=max(maximum,score);count+=1
        caps.append(maximum);counts.append(count)
        size=left.bit_count();classes[size]=max(classes.get(size,-1),maximum)
    return {'caps':caps,'feasible_counts':counts,'maximum':max(caps),'by_left_size':classes}


def connected(g,removed=()):
    rest=set(range(len(g)))-set(removed);seen={min(rest)};todo=list(seen)
    while todo:
        x=todo.pop()
        for y in g[x]&rest-seen:seen.add(y);todo.append(y)
    return seen==rest


def sharp_controls():
    all_records={}
    for p in(5,6):
        fixture=opt.degree_fixture(p);file=ROOT/('develop/fixtures/degree-basis-'+str(p)+'.json')
        assert json.loads(file.read_text())==fixture
        n=12*p+2;adj=fixture['adjacency_masks'];g,S=opt.graph(p,p,adj);Q=set(fixture['attaining_set'])
        assert min(map(len,g))==2 and max(map(len,g))==p+1 and len(S)==8*p and len(Q)==7*p and diss(g,Q)
        assert all(literal(g,S,x)for x in range(n)if x not in S)
        assert all(any(not literal(g,S,x,v)for x in(set(range(n))-S)|{v})for v in S)
        records={}
        for label,deleted in(('H',False),('H_minus_safe_port',True)):
            new=list(adj)
            if deleted:new[1]^=1<<1
            physical,T=opt.graph(p,p,new);result=opt.exact(p,p,new)
            reference=independent_frontier(physical,p)
            assert reference['maximum']==result['beta']==7*p
            assert reference['caps']==[r['cap']for r in result['rows']]
            assert reference['feasible_counts']==[r['feasible_pairs']for r in result['rows']]
            assert all(connected(physical,[v])for v in range(n))
            reference['vector_sha256']=hashlib.sha256(json.dumps(reference['caps'],separators=(',',':')).encode()).hexdigest()
            records[label]=reference
        # One outside-edge control that fails the needed deletion-cap hypothesis.
        new=list(adj);new[0]^=1
        unsafe_graph,_=opt.graph(p,p,new);unsafe=opt.exact(p,p,new)
        assert unsafe['beta']>7*p and diss(unsafe_graph,set(unsafe['attaining_set']))
        cycle=[]
        for t in range(2*p):
            r=(t+3)%(2*p)
            cycle +=[6*(t//2)+4+t%2,6*(p+r//2)+4+r%2]
        h=[set(ns)for ns in g];a,b=fixture['safe_port_edge'];h[a].remove(b);h[b].remove(a)
        assert len(set(cycle))==4*p and all(cycle[(j+1)%(4*p)]in h[x]for j,x in enumerate(cycle))
        all_records[str(p)]={'base_caps':records,'unsafe_deleted_edge':[4,6*p+4],
                            'unsafe_deleted_beta':unsafe['beta'],'backbone_hamiltonian_cycle':cycle,
                            'single_vertex_deletions':2*n}
    return all_records


def lifts():
    rows=[]
    for p,k in[(p,k)for p in(5,6,7,8,9,10,17,32,65)for k in(1,2,3)]+[(5,128),(6,64)]:
        g,S,Q=opt.cyclic_lift(p,k);n=12*p+2
        assert len(g)==n*k and len(S)==8*p*k and len(Q)==7*p*k and diss(g,Q)
        assert min(map(len,g))==2 and max(map(len,g))==p+1
        assert all(literal(g,S,x)for x in range(len(g))if x not in S)
        failures=0
        for copy in range(k):
            for j in range(2*p):
                c=n*copy+6*j
                for v,w in((c,c+4),(c+1,c+4),(c+2,c+5),(c+3,c+3)):
                    assert not literal(g,S,w,v);failures+=1
        if p<=10 and k<=3:assert all(connected(g,[v])for v in range(len(g)))
        else:assert connected(g)
        rows.append({'p':p,'k':k,'order':len(g),'selected':len(S),'attaining_beta':len(Q),'selected_gap':p*k,
                     'literal_deletion_failures':failures,'single_vertex_deletions':len(g)if p<=10 and k<=3 else 0})
    # Direct exact controls on the first shared-u extensions and their port deletion.
    extension=[]
    for p in(7,8):
        adj=opt.degree_adjacency(p)
        for removed in(False,True):
            new=list(adj)
            if removed:new[1]^=1<<1
            result=opt.exact(p,p,new);assert result['beta']==7*p
            extension.append({'p':p,'removed':removed,'beta':result['beta'],'feasible_pairs':sum(r['feasible_pairs']for r in result['rows'])})
    return {'physical_models':rows,'exact_extension_controls':extension}


def invalid_controls():
    tests=[lambda:opt.graph(0,1,[]),lambda:opt.graph(1,1,[-1,0]),lambda:opt.graph(1,1,[4,0]),
           lambda:opt.graph(1,1,[0]),lambda:opt.cyclic_lift(5,0),lambda:opt.wing(1,0,1)]
    for f in tests:
        try:f()
        except ValueError:continue
        raise AssertionError('Invalid domain accepted')
    return len(tests)


def main():
    report={'status':'PASS','local_and_wing_controls':table_controls(),'small_graph_controls':small_controls(),
            'sharp_base':sharp_controls(),'lifts':lifts(),'invalid_domain_rejections':invalid_controls(),
            'scope':'General exact-interface and all-k proofs are written separately. Fixed62/74-vertex caps are computer-assisted integer certificates, independently recomputed by closed-table/full-boundary enumeration. Large-lift optima follow the general composition theorem, not finite sampling. No exact SF value or unrestricted selected-structure claim.'}
    out=ROOT/'output/sharp-minimum-two-degree-check.json';out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','small_graph_totals':report['small_graph_controls']['totals'],
                      'base_caps':{p:[r['maximum']for r in data['base_caps'].values()]for p,data in report['sharp_base'].items()},
                      'lift_models':len(report['lifts']['physical_models']),'full_ternary_wing_states':report['local_and_wing_controls']['all_p5_ternary_states']},sort_keys=True))


if __name__=='__main__':main()
