"""Standalone certificate audit: standard library only, no project imports."""
import json
from pathlib import Path

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def adjacent(v):
    r,c=v
    return {(r-1,c),(r+1,c),(r,c-1),(r,c+1)}


def edges(raw):return {tuple(sorted((tuple(a),tuple(b)))) for a,b in raw}
def vertices(raw):return {tuple(v) for v in raw}


def matching(board,raw,full=False):
    result={}
    for a,b in sorted(edges(raw)):
        assert a in board and b in board and b in adjacent(a)
        assert a not in result and b not in result
        result[a]=b;result[b]=a
    if full:assert set(result)==board
    return result


def decompose(board,raw_m,raw_n,t):
    mm=matching(board,raw_m);nm=matching(board,raw_n,True)
    q=board-set(mm);seen=set();paid=set();pairs=[];paths=[]
    for source in sorted(v for v in q if sum(v)%2):
        assert source not in seen;path=[source];actual=set()
        while True:
            black=nm[path[-1]];path.append(black)
            if black in q:break
            assert black in mm
            white=mm[black];actual.add(tuple(sorted((black,white))));path.append(white)
            assert len(path)==len(set(path))
        assert not seen&set(path);seen|=set(path)
        if source in t:paid|=actual
        pairs.append((source,black));paths.append(path)
    assert seen&q==q
    return paid,pairs,paths


def saturates(black,white):
    used={}
    def augment(b,seen):
        for w in sorted(adjacent(b)&white):
            if w in seen:continue
            seen.add(w)
            if w not in used or augment(used[w],seen):used[w]=b;return True
        return False
    return all(augment(b,set()) for b in sorted(black))


def coordinate_audit(data):
    board=vertices(data['board']);t=vertices(data['T']);centres=list(map(tuple,data['centres']))
    parts=[vertices(p) for p in data['parts']];mm=matching(board,data['M']);q=board-set(mm)
    assert set().union(*parts)==set(mm) and sum(map(len,parts))==len(mm)
    assert all(not(adjacent(v)&(set(mm)-part)) for part in parts for v in part)
    assert all(not(adjacent(v)&t) for v in centres)
    assert all(len(adjacent(v)&set(mm))<=1 for v in t)
    W={v for v in q if sum(v)%2}-t;B={v for v in q if sum(v)%2==0}-set(centres)
    assert len(W)==len(centres)-1 and len(t)==len(B)+1
    E={v for v in t if saturates(B,t-{v})};F=t-E
    D={v for v in B if not(adjacent(v)&E)}
    assert len(F)==len(D) and set().union(set(),*(adjacent(v)&t for v in D))==F
    gamma={w:set() for w in W}
    for i,(h,part) in enumerate(zip(centres,parts)):
        for w in W:
            seen={w};todo=[w]
            while todo:
                v=todo.pop()
                if v==h:gamma[w].add(i);break
                if sum(v)%2:options=(adjacent(v)&(part|{h}))-({mm[v]} if v in mm else set())
                else:options={mm[v]} if v in mm else set()
                for z in options-seen:seen.add(z);todo.append(z)
    # Exhaust all centre images; at most 4! for the supplied certificates.
    from itertools import permutations
    eligible=set();sources=sorted(W)
    for image in permutations(range(len(centres)),len(sources)):
        if all(i in gamma[w] for w,i in zip(sources,image)):
            eligible|=set(range(len(centres)))-set(image)
    assert eligible
    return board,t,centres,W,B,E,F,D,gamma,eligible


def main():
    raw=json.loads((ROOT/'output/multicentre-hall-certificates.json').read_text());data=raw['all_K']
    board,t,C,W,black,E,F,D,gamma,J=coordinate_audit(data)
    assert vertices(data['E'])==E and vertices(data['F'])==F and vertices(data['D'])==D
    assert vertices(data['W'])==W and J==set(range(5)) and len(F)==len(D)==20
    cheap=edges(data['cheap_edges']);mm=matching(board,data['M'])
    cheap_neighbours=[]
    for e in sorted(cheap):
        b=next(v for v in e if sum(v)%2==0)
        ns=adjacent(b)&t
        assert not ns&E and len(ns)==1
        cheap_neighbours.append(dict(black=b,selected_neighbours=sorted(ns)))
    rows=[]
    for name,N,expected in [('optimum',data['optimum_N'],[0,1]),
                            ('sharp_two_centre',data['sharp_two_centre_N'],[2,1])]:
        paid,pairs,paths=decompose(board,data['M'],N,t)
        coefficients=[len(paid&cheap),len(paid-cheap)];assert coefficients==expected
        k=sum(a in t and b in C for a,b in pairs)
        a=sum(s in F and z not in D for s,z in pairs)
        b=sum(s in E and z in D for s,z in pairs)
        c=sum(s in W and z in D for s,z in pairs)
        assert a==b+c and sum(s in W and z not in C for s,z in pairs)==k-1
        if name=='sharp_two_centre':
            assert (a,b,c,k)==(2,1,1,2)
            assert list(map(tuple,data['sharp_two_centre_HH_to_D'])) in paths
        rows.append(dict(matching=name,full_N_edges=len(N),paid_coefficients=coefficients,a=a,b=b,c=c,k=k))
    # Verify displayed attaining relaxations against actual coordinates and M.
    for key in ['cheap_centre_paths','Hall_quota_attaining_paths']:
        owned=set();fee=[0,0];sources=[];ends=[]
        for raw_path in data[key]:
            path=list(map(tuple,raw_path));assert not owned&set(path);owned|=set(path)
            assert path[0] in t and path[-1] in board-set(mm)
            sources.append(path[0]);ends.append(path[-1])
            for i,(u,v) in enumerate(zip(path,path[1:])):
                e=tuple(sorted((u,v)));assert v in adjacent(u)
                assert (e in edges(data['M']))==(i%2==1)
                if i%2:fee[0 if e in cheap else 1]+=1
        if key=='cheap_centre_paths':assert fee==[2,0] and set(ends)<=set(C)
        else:
            assert fee==[1,1] and sum(s in F for s in sources)==sum(s in E for s in sources)==1
            assert sum(z in C for z in ends)==sum(z in D for z in ends)==1
    data2=raw['proper_J'];b2,t2,c2,w2,_,e2,f2,d2,g2,j2=coordinate_audit(data2)
    assert g2=={(5,2):{0}} and j2=={1} and f2=={(5,0),(5,4)}
    paid2,_,_=decompose(b2,data2['M'],data2['attaining_N'],t2);assert len(paid2)==1
    data3=raw['proper_J_counterexample']
    b3,t3,c3,w3,_,e3,f3,d3,g3,j3=coordinate_audit(data3)
    assert g3=={(0,5):{0}} and j3=={1}
    assert f3==vertices(data3['F']) and d3==vertices(data3['D']) and len(f3)==17
    cheap3=edges(data3['cheap_edges']);mm3=matching(b3,data3['M']);q3=b3-set(mm3)
    # Independently compute terminal endpoints of all nontrivial cheap-only
    # E-source walks. Only the ineligible centre may occur, so every E path
    # to either an eligible centre or D uses a K edge, including cross pairs.
    reached={(v,False) for v in e3};todo=list(reached);cheap_ends=set()
    while todo:
        v,paid_flag=todo.pop()
        if v in q3 and sum(v)%2==0:
            if paid_flag:cheap_ends.add(v)
            continue
        if sum(v)%2:options=[(z,paid_flag) for z in adjacent(v)&b3 if mm3.get(v)!=z]
        elif v in mm3 and tuple(sorted((v,mm3[v]))) in cheap3:options=[(mm3[v],True)]
        else:options=[]
        for item in options:
            if item not in reached:reached.add(item);todo.append(item)
    assert cheap_ends=={c3[0]} and not cheap_ends&(d3|{c3[i] for i in j3})
    p3,pairs3,paths3=decompose(b3,data3['M'],data3['attaining_N'],t3)
    assert p3==cheap3 and list(map(tuple,data3['HH_to_D'])) in paths3
    normal3,_,_=decompose(b3,data3['M'],data3['normal_N'],t3)
    assert len(normal3)==1 and not normal3&cheap3
    assert (sum(a in f3 and z not in d3 for a,z in pairs3),
            sum(a in e3 and z in d3 for a,z in pairs3),
            sum(a in w3 and z in d3 for a,z in pairs3),
            sum(a in t3 and z in c3 for a,z in pairs3))==(1,0,1,2)
    out=dict(status='PASS',project_imports=False,all_K_independent_exterior_deletions=len(t),
             eligible_roots=sorted(J),canonical_F_size=len(F),canonical_D_size=len(D),
             cheap_black_selected_neighbours=cheap_neighbours,full_N_symbolic_checks=rows,
             proper_J_eligible=sorted(j2),proper_J_independent_exterior_deletions=len(t2),
             proper_J_counterexample=dict(independent_exterior_deletions=len(t3),F_size=len(f3),D_size=len(d3),
                 eligible=sorted(j3),nontrivial_E_cheap_only_endpoints=sorted(cheap_ends),
                 optimum_paid_coefficients=[2,0],normal_paid_coefficients=[0,1],terminal_balance=[1,0,1,2]),
             scope='Standalone standard-library adjacency, full matching and path audit; computes exposure by every deletion and Gamma by local walks. Symbolic paid coefficients certify fees K and K+2 for fixed N; general theorem is proved separately.')
    (ROOT/'output/multicentre-coordinate-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
