"""Actual all-size five-contact counterfamily to pair sparsification.

The construction extends an Oracle-proposed explicit L=20,d=11 board.
General family, asymptotic gap and geometric proof are written separately.
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from check_mixed_terminal_compensation import edge, grid, mates, selected_feasible

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT=Path(__file__).resolve().parents[1]


def path_builder(start):
    result=[start]
    def to(target):
        x,y=result[-1];a,b=target
        assert x==a or y==b
        while (x,y)!=(a,b):
            x += (a>x)-(a<x); y += (b>y)-(b<y)
            result.append((x,y))
    return result,to


def family(L,d,internal=False):
    assert L>=4 and L%2==0 and d>=1
    c3=d+9;c4=d+13;c5=2*d+14
    a,to=path_builder((0,0));to((c4,0));to((c4,2))
    for row in range(2,L):
        to((c4+d if row%2==0 else c4,row));to((a[-1][0],row+1))
    to((c5,L));to((c5,0));to((c5+4,0))
    b,to=path_builder((c3+1,1));to((c3,1));to((c3,3))
    for row in range(3,L+1):
        to((9 if row%2 else c3,row));to((b[-1][0],row+1))
    for target in [(8,L+1),(8,1),(7,1),(7,L+4),(2*d+20,L+4),
                   (2*d+20,-3),(c5+1,-3),(c5+1,-1),(c4,-1),
                   (c4,-3),(-2,-3),(-2,2),(4,2),(4,1)]:to(target)
    if internal:to((2,1))
    assert len(a)==len(set(a)) and len(b)==len(set(b))
    assert not set(a)&set(b)
    def domino(q):
        i,j=q;left=(j+4,2*i+6);right=(j+4,2*i+7)
        return (left,right) if j%2==0 else (right,left) # black,white
    def expand(path):return [v for q in path for v in domino(q)]
    av,bv=expand(a),expand(b)
    m={edge(p[j],p[j+1]) for p in [av,bv] for j in range(1,len(p)-1,2)}
    h,w=L+10,4*d+50
    n={edge((r,c),(r,c+1)) for r in range(h) for c in range(0,w,2)}
    t={av[0],av[-1]}
    # Both endpoints at a cut may be Q; the internal variant extends B's tail.
    squares=[(4,2*4+6),(4,2*8+6),(4,2*c3+6),
             (3,2*c4+6),(3,2*c5+6)]
    indices_a={q:j for j,q in enumerate(a)};indices_b={q:j for j,q in enumerate(b)}
    ca=[(4,0),(8,0),(c3,0),(c4,0),(c5,0)]
    cb=[(4,1),(8,1),(c3,1),(c4,-1),(c5,-1)]
    xa=[indices_a[q] for q in ca];yb=[indices_b[q] for q in cb]
    assert sorted(range(5),key=lambda j:xa[j])==[0,1,2,3,4]
    assert sorted(range(5),key=lambda j:yb[j])==[2,1,4,3,0]
    return h,w,m,n,t,av,bv,squares,xa,yb


def decompose_linear(board,m,n,t,affected):
    mm=mates(board,m);nm=mates(board,n,full=True)
    assert not m&n
    q=board-mm.keys();assert t<=q and selected_feasible(set(mm),t)
    unseen=set(board);counts=Counter();paid=set();cycles=[];path_sets=[]
    for first in board:
        if first not in unseen:continue
        found={first};todo=[first];rs=set()
        while todo:
            u=todo.pop()
            if u in mm:rs.add(edge(u,mm[u]))
            for v in [nm[u]]+([mm[u]] if u in mm else []):
                if v not in found:found.add(v);todo.append(v)
        unseen-=found;ends=found&q
        if not ends:
            assert found<=set(mm)
            if found&affected:cycles.append(rs)
        else:
            assert len(ends)==2
            selected=len(ends&t);kind=['HH','TH','TT'][selected];counts[kind]+=1
            if kind=='TH':
                assert not paid&rs;paid|=rs
            if found&affected:path_sets.append((kind,rs))
    cycle_m=set().union(*cycles)
    assert sum(map(len,cycles))==len(cycle_m)
    assert not paid&cycle_m
    return dict(counts=tuple(counts[k] for k in ['TT','HH','TH']),
                paid=paid,cycles=cycles,cycle_M=cycle_m,affected_paths=path_sets)


def control(L,d,internal=False):
    h,w,m,n,t,a,b,squares,xa,yb=family(L,d,internal)
    board=grid(h,w);affected=set(a)|set(b)
    assert len(m)==(2*L+3)*d+6*L+82+2*internal
    before=decompose_linear(board,m,n,t,affected)
    b0=17*d+19*L+167-2*internal
    assert before['counts']==(1,b0,0)
    gates=[];support=set()
    for r,c in squares:
        old={edge((r,c),(r,c+1)),edge((r+1,c),(r+1,c+1))}
        new={edge((r,c),(r+1,c)),edge((r,c+1),(r+1,c+1))}
        vs={v for e in old for v in e}
        assert old<=n and not old&m and not new&m and not vs&support
        assert sum(set(e)<=set(a) for e in old)==1
        assert sum(set(e)<=set(b) for e in old)==1
        if internal:assert vs<=set(mates(board,m))
        support|=vs;gates.append((old,new))
    results=[]
    for k in range(1,6):
        for chosen in combinations(range(5),k):
            nn=set(n)
            for j in chosen:old,new=gates[j];nn=nn-old|new
            after=decompose_linear(board,m,nn,t,affected)
            full=after['counts'][0]==0
            assert after['counts'] in [(1,b0,0),(0,b0-1,2)]
            if full:
                assert after['counts']==(0,b0-1,2)
                assert len(after['paid'])+len(after['cycle_M'])==len(m)
            if k==1:assert full and len(after['paid'])==len(m)
            if k==2:
                i,j=chosen;inverse=(xa[i]-xa[j])*(yb[i]-yb[j])<0
                assert full==inverse
                if full:
                    assert len(after['cycles'])==1
                    assert len(after['cycle_M'])==abs(xa[i]-xa[j])+abs(yb[i]-yb[j])
            if k==5:
                assert full and len(after['cycles'])==2
                expected=(L-1)*d+2*L+1+(d+1)
                assert sorted(map(len,after['cycles']))==[expected,expected]
                assert len(after['paid'])==2*L+3*d+78+2*internal
                cycle_vertices={v for z in after['cycle_M'] for v in z}
                normalized={e for e in nn if e[0] not in cycle_vertices}|after['cycle_M']
                assert m&normalized==after['cycle_M']
                normal=decompose_linear_allow_retention(board,m,normalized,t)
                assert normal==after['counts']
            results.append(dict(contacts=[j+1 for j in chosen],full=full,
                                paid_M=len(after['paid']),cycle_M=len(after['cycle_M']),cycles=len(after['cycles'])))
    pair=min(r['paid_M'] for r in results if r['full'] and len(r['contacts'])<=2)
    five=results[-1]['paid_M']
    proper=min(r['paid_M'] for r in results if r['full'] and len(r['contacts'])<5)
    assert proper==pair
    assert min(r['paid_M'] for r in results if r['full'])==min(pair,five)
    assert pair==(L-1)*d+2*L+14+2*internal
    return dict(L=L,d=d,internal_contacts=internal,board=[h,w],M=len(m),T=sorted(t),
                initial_counts=before['counts'],best_one_two=pair,best_proper_subset=proper,five_contact_cost=five,
                gap=pair-five,all_subset_optimum=min(r['paid_M'] for r in results if r['full']),
                same_prescribed_contacts=True,subsets=results)


def decompose_linear_allow_retention(board,m,n,t):
    """A separate linear endpoint walk also permits retained doubled edges."""
    mm=mates(board,m);nm=mates(board,n,full=True);q=board-mm.keys();unseen=set(q);counts=Counter()
    for start in q:
        if start not in unseen:continue
        v=start
        while True:
            v=nm[v]
            if v in q:break
            v=mm[v]
        assert v in unseen and v!=start;unseen-={start,v}
        counts[['HH','TH','TT'][int(start in t)+int(v in t)]]+=1
    return tuple(counts[k] for k in ['TT','HH','TH'])


def main():
    source=control(20,11);assert source['best_one_two']==263 and source['five_contact_cost']==151
    internal=control(20,11,True);assert internal['best_one_two']==265 and internal['five_contact_cost']==153
    rows=[control(L,L) for L in range(12,61,2)]
    assert all(r['gap']==L*(L-4)-64 and r['gap']>0 for L,r in zip(range(12,61,2),rows))
    out=dict(status='PASS',actual_full_subset_boards=len(rows)+2,subsets_per_board=31,
        source_oracle_board=source,strictly_internal_source=internal,
        square_family_controls=len(rows),largest=rows[-1],
        formulas=dict(M='(2L+3)d+6L+82',best_one_two='(L-1)d+2L+14',five_cost='2L+3d+78',gap='(L-4)d-64',
                      square_parameters='d=L, even L>=12',ratio_lower_bound='(L^2+L+14)/(5L+78) -> infinity'),
        trust_boundary='General coordinate simplicity/feasibility/full-N and exact gap proof written. Finite31-subset checks validate each actual instance, not a general proof. Symbolic serial-block proof establishes best proper subset=C2 and all-subset optimum=min(C2,C5). Same prescribed contact family only; other squares/N/payments unrestricted.')
    (ROOT/'output/five-contact-barrier.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',boards=len(rows)+2,subsets=31*(len(rows)+2),
                         source=[263,151],largest=[rows[-1]['best_one_two'],rows[-1]['five_contact_cost']],
                         largest_gap=rows[-1]['gap'])))


if __name__=='__main__':main()
