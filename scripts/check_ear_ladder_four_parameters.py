"""Literal independent controls for the all-r four-parameter ear ladder."""
from itertools import combinations
from pathlib import Path
import json


def model(r):
    n=4*r
    g=[set() for _ in range(4*n)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for i in range(2):
        for j in range(n-1):edge(i*n+j,i*n+j+1)
    for j in range(n):edge(j,n+j)
    squares={}
    for i in range(2):
        for s in range(n//2):
            d=i*n+2*s;e=d+1;a=2*n+2*(i*(n//2)+s);b=a+1
            edge(d,a);edge(a,b);edge(b,e)
            squares[i,s]=(d,e,a,b)
    t=set();matching=[]
    for j in range(r):
        i=j%2
        d,e,a,b=squares[i,2*j];t.update((d,b))
        d,e,a,b=squares[i,2*j+1];t.update((e,a))
        matching.append((i*n+4*j+1,i*n+4*j+2))
        for s in (2*j,2*j+1):t.update(squares[1-i,s][2:])
    return g,squares,t,matching


def unformed(g,s):
    active={v for v in s if g[v]&s}
    return {v for v in range(len(g)) if v not in s and len(g[v]&s)<2
            and not(g[v]&active)}


def literal(g):
    # Full unrestricted 2^16 search, including all single deletions.
    rows=[sum(1<<v for v in row) for row in g]
    formed=[];beta=sf=0;minimal=0
    for s in range(1<<len(g)):
        active=sum(1<<v for v,row in enumerate(rows) if s>>v&1 and row&s)
        ok=all(s>>v&1 or (row&s).bit_count()>=2 or row&active
               for v,row in enumerate(rows))
        formed.append(ok)
        if all(not(s>>v&1) or (row&s).bit_count()<=1 for v,row in enumerate(rows)):
            beta=max(beta,s.bit_count())
        if ok and all(not formed[s^(1<<v)] for v in range(len(g)) if s>>v&1):
            sf=max(sf,s.bit_count());minimal+=1
    return beta,sf,minimal


def exact_omega(g):
    """Every matching; every disjoint T, with no local exceptional-square pruning."""
    n=len(g);rows=[sum(1<<v for v in row) for row in g]
    edges=[(a,b) for a in range(n) for b in g[a] if a<b]
    best=0;matchings=0;subsets=0
    def evaluate(p,m):
        nonlocal best,matchings,subsets
        matchings+=1
        available=[v for v in range(n) if not(p>>v&1)
                   and (rows[v]&p).bit_count()<=1]
        # Vertices with >=2 P neighbours cannot occur in feasible T.
        masks=[0]
        for v in available:masks += [s|(1<<v) for s in masks]
        for t in masks:
            subsets+=1;occupied=p|t
            if all(not(t>>v&1) or (rows[v]&occupied).bit_count()<=1
                   for v in available):best=max(best,m+t.bit_count())
    def visit(edge_index,p,m):
        evaluate(p,m)
        for j in range(edge_index,len(edges)):
            a,b=edges[j];bits=(1<<a)|(1<<b)
            if not(p&bits):visit(j+1,p|bits,m+1)
    visit(0,0,0)
    return best,matchings,subsets


def main():
    report=dict(status='PASS',family_models=0,colour_neighbourhoods=0,
                deletion_witnesses=0,full_subsets=65536,new_Lean=False)
    for r in (1,2,3,4,5,8,16,31,64,128):
        g,squares,t,matching=model(r)
        p={v for e in matching for v in e}
        assert len(g)==16*r and len(t)==8*r and len(p)==2*r and not(t&p)
        assert all(b in g[a] for a,b in matching)
        assert all(len(g[v]&(p|t))<=1 for v in t)
        colours={v:j for j,v in enumerate(sorted(t))}
        for j,(a,b) in enumerate(matching):colours[a]=colours[b]=len(t)+j
        assert len(set(colours.values()))==9*r
        support=set(colours)
        for v in support:
            closed=(g[v]&support)|{v}
            assert 2*sum(colours[u]==colours[v] for u in closed)>=len(closed)
            report['colour_neighbourhoods']+=1
        selected={v for q in squares.values() for v in q[2:]}
        assert len(selected)==8*r and not unformed(g,selected)
        assert all(len(g[v]&selected)==1 for v in selected)
        for v in selected:
            # Self-witness after deleting a new vertex of an isolated selected edge.
            assert v in unformed(g,selected-{v})
            report['deletion_witnesses']+=1
        assert max(map(len,g))==4
        report['family_models']+=1
    g,_,_,_=model(1)
    beta,sf,minimal=literal(g)
    assert (beta,sf,minimal)==(8,8,6**4)
    omega,matchings,subsets=exact_omega(g)
    assert omega==9
    report['literal_base']={'beta':beta,'SF':sf,'minimal_sets':minimal,
                            'Omega':omega,'matchings':matchings,'T_subsets':subsets}
    out=Path(__file__).resolve().parents[1]/'output';out.mkdir(exist_ok=True)
    (out/'ear-ladder-four-parameter-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
