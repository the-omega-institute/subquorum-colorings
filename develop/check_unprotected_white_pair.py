"""Solver-free controls for the written unprotected-white capacity proof.

Finite controls check, rather than replace, the structural argument and
explicit all-length constructions in UNPROTECTED_WHITE_PAIR_AND_PREFIX_BUDGET.md.
"""
import argparse
from collections import Counter
import itertools
import json
import random
from pathlib import Path
from check_frozen_half_area_attainers import frozen_family,certificate,verify_ranks
from check_endpoint_invasion_sharp_strips import endpoints
from check_promotion_cores import frozen_certificate
from check_frozen_equality_matching_rigidity import first_times
from check_residual_corridors import direct_check
from check_whole_board_endpoint_invasion import BLACK,WHITE,local_ok,check_cases,random_whole_board,neighbors

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')

PAIR_EDGES=[(0,2),(0,4),(1,3),(1,4),(1,5)] # r,s,d,e,g,h
BP=set(BLACK)|{(0,0),(0,2),(1,3),(2,2),(2,4),(0,4),(0,6)}
WP=set(WHITE)|{(0,1),(0,3),(1,2),(0,5),(0,7),(1,4)}


def all_matchings(edges):
    out=[]
    def visit(i,used,M):
        if i==len(edges):out.append(tuple(M));return
        visit(i+1,used,M)
        a,b=edges[i]
        if not {a,b}&used:visit(i+1,used|{a,b},M+[edges[i]])
    visit(0,set(),[]);return out


def local_controls(counts):
    matchings=all_matchings(PAIR_EDGES)
    N={v:{u for e in PAIR_EDGES if v in e for u in e if u!=v} for v in range(6)}
    types=Counter()
    for state in itertools.product(range(3),repeat=6): # empty, selected, endpoint
        T={v for v,x in enumerate(state) if x==1};O={v for v,x in enumerate(state) if x}
        if any(len(N[v]&O)>1 for v in T):continue
        for M in matchings:
            P={v for e in M for v in e}
            if any(state[v]!=2 for v in P):continue
            # White endpoints have no outside neighbours; unmatched black
            # endpoint sites are allowed distinct optimistic exterior mates.
            if any(state[v]==2 and v not in P for v in (0,1)):continue
            D=len(T&{2,3,4,5});r=int(0 not in O);s=int(1 not in O)
            if 0 in O and 1 in O:
                assert 4 not in T and not {2,3,5}<=T
            elif 0 in O or 1 in O:assert D<=3
            assert D<=2+r+s
            counts['six_site_actual_models']+=1
            types[str((state[0],state[1]))]+=1
    assert types[str((1,1))] and types[str((1,2))] and types[str((2,1))]
    for bits in itertools.product((0,1),repeat=10):
        A,B,C,D,u,v,w,x,y,z=bits
        if not (A<=u+v and B<=min(u,w) and 2*C<=w+x+y and 2*D<=x+y+z):continue
        assert A+B<=u+v+w and C+D<=x+y+z
        assert A+B+C+D<=u+v+w+x+y+z
        counts['top_block_binary_models']+=1
    return dict(types)


def generalized_board(cur,counts,frozen=False):
    h,width,T,M=cur;c=width-1;direct_check(*cur);P=endpoints(M);O=T|P
    tail={(5,k) for k in range(5,c+1,2)};L={(5,k-1) for k in range(5,c+1,2)}
    assert h==6 and c>=5 and c%2==1
    assert {v for v in T if sum(v)%2==0}<=set(BLACK)|tail
    assert {(2,1)}|{(4,k) for k in range(5,c+1,2)}<=O
    H=set(itertools.product(range(h),range(width)))-O
    bits=tuple(int(v in T) for v in BLACK);blanks=tuple(int(v in H) for v in WHITE)
    assert local_ok(bits,blanks)
    assert sum(bits[i] for i in (3,4,6,7))<=2+blanks[7]+blanks[8]
    check_cases(bits,blanks)
    paid={(5,k-1) for r,k in T&tail}
    assert paid<=H and len(paid)==len(T&tail) and paid.isdisjoint(WHITE)
    Hw={v for v in H if sum(v)%2};Tb={v for v in T if sum(v)%2==0}
    assert len(Tb)<=len(Hw)
    J=len(T)+len(M)
    assert J==3*width+len(Tb)-len(Hw)<=3*width
    counts['generalized_boards']+=1
    counts['selected_protected_white_sites']+=len(T&{(5,0),(5,2)})
    if frozen:
        assert frozen_certificate(cur)[0]==P and set(first_times(cur))==P
        assert J==3*width
        counts['sharp_frozen_white_replacements']+=1


def white_replacement(m):
    h,w,T,M=frozen_family(m)
    return h,w,(T-{(5,1),(5,3)})|{(5,0),(5,2)},M


def frozen_terminal_black(m):
    h,w,T,M=frozen_family(m);c=w-1
    T=(T-{(0,c),(1,c-1),(2,c)})|{(1,c)}
    M=M+[((2,c-1),(2,c))]
    rec=[]
    for v,r,a,b in certificate(m):
        if v==(1,c-2):r=1;a=(0,c-2);b=(1,c-3)
        elif v==(2,c-3):r=2
        elif v==(3,c-2):r=3
        elif v==(3,c):r=5;a=(2,c);b=(3,c-1)
        elif v[0]==4 and v[1]%2==0:r+=2
        elif v==(3,5):r+=2
        rec.append((v,r,a,b))
    rec += [((2,c-1),4,(2,c-2),(3,c-1)),
            ((2,c),3*m+3,(1,c),(3,c))]
    return (h,w,T,M),rec


def terminal_board_control(cur,counts):
    h,w,T,M=cur;c=w-1;v=(1,c)
    direct_check(*cur);P=endpoints(M);O=T|P
    tail={(5,k) for k in range(5,c+1,2)};L={(5,k-1) for k in range(5,c+1,2)}
    assert v in T and {z for z in T if sum(z)%2==0}<=set(BLACK)|tail|{v}
    assert {(2,1)}|{(4,k) for k in range(5,c+1,2)}<=O
    H=set(itertools.product(range(h),range(w)))-O
    bits=tuple(int(z in T) for z in BLACK);blanks=tuple(int(z in H) for z in WHITE)
    assert local_ok(bits,blanks)
    assert sum(bits[i] for i in (3,4,6,7))<=2+blanks[7]+blanks[8]
    check_cases(bits,blanks)
    X={(0,c),(1,c-1),(2,c)}
    assert X.isdisjoint(set(WHITE)|L) and len(X&H)>=2
    assert {(5,k-1) for r,k in T&tail}<=H
    old_black={z for z in T if sum(z)%2==0}-{v}
    assert len(old_black)<=len(H&(set(WHITE)|L))
    assert len(T)+len(M)+1<=3*w
    counts['terminal_upper_bound_boards']+=1


def random_terminal(m,seed):
    rng=random.Random(seed);cur,_=frozen_terminal_black(m);h,w,T,M=cur;c=w-1
    edges={tuple(sorted(e)) for e in M};old=set(edges)
    squares=[[(r,k),(r+1,k),(r,k+1),(r+1,k+1)] for r in range(h-1) for k in range(w-1)]
    rng.shuffle(squares)
    for a,b,d,e in squares:
        vertical={tuple(sorted((a,b))),tuple(sorted((d,e)))}
        horizontal={tuple(sorted((a,d))),tuple(sorted((b,e)))}
        if vertical<=edges:edges=(edges-vertical)|horizontal
        elif horizontal<=edges:edges=(edges-horizontal)|vertical
    M=sorted(edges);T={v for v in T if v==(1,c) or rng.randrange(3)}
    P=endpoints(M)
    choices=sorted(v for v in set(itertools.product(range(h),range(w)))-(T|P) if sum(v)%2)
    rng.shuffle(choices)
    for v in choices:
        trial=T|{v};O=trial|P
        if all(len(neighbors(z,h,w)&O)<=1 for z in trial):T=trial
    return (h,w,T,M),edges!=old


def prefix_obstruction(m):
    c=6*m+9
    T={(0,0),(0,2),(0,4),(1,3),(2,2),(2,4),(3,3),(4,4),(5,3)}
    M=[((1,1),(2,1)),((1,0),(2,0)),((3,0),(4,0)),
       ((3,1),(4,1)),((4,2),(5,2)),((5,0),(5,1))]
    M += [((r,k),(r+1,k)) for k in range(5,c+1) for r in (0,2,4)]
    return 6,c+1,T,M


def check_obstruction(m,counts):
    cur=prefix_obstruction(m);h,w,T,M=cur;P=endpoints(M);direct_check(*cur)
    assert endpoints(frozen_family(m)[3])<=P
    H=set(itertools.product(range(h),range(w)))-(T|P)
    expected={(0,1),(0,3),(1,2),(1,4),(2,3),(3,2),(3,4),(4,3),(5,4)}
    assert H==expected and len(T)==len(H)==9
    assert T<=BP and len(BP)==len(WP)==15 and len(H&WP)==8
    assert H-WP=={(5,4)} and len(T)+len(M)==18*m+30
    # This does not satisfy complete freezing: no first event is possible.
    assert all(len(neighbors(v,h,w)&T)<2 for v in P)
    assert not frozen_certificate(cur)[0] and not first_times(cur)
    counts['all_length_prefix_obstructions']+=1
    counts['literal_exterior_hole_payments']+=1
    # All actual 2x2 tile units are neutral in this family. The unbalanced
    # candidate prefix is not a union of original physical tiles.
    charges=[]
    for r in range(0,h,2):
        for c in range(0,w,2):
            tile={(r+i,c+j) for i in (0,1) for j in (0,1)}
            charges.append(4-2*len(T&tile)-len(P&tile))
    assert all(x==0 for x in charges)
    return dict(m=m,selected=9,matching=len(M),objective=len(T)+len(M),
        pocket_black_selected=9,pocket_white_holes=8,
        exterior_white_hole=[5,4],initial_freezing_events=0,
        nonzero_aligned_tile_charges=sum(x!=0 for x in charges))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();types=local_controls(counts);obstacles=[]
    for m in list(range(2,41))+[64,100]:
        cur=white_replacement(m);generalized_board(cur,counts,True)
        verify_ranks(cur,certificate(m),counts)
        new,rec=frozen_terminal_black(m)
        direct_check(*new);verify_ranks(new,rec,counts);terminal_board_control(new,counts)
        assert endpoints(frozen_family(m)[3])<=endpoints(new[3])
        assert set(first_times(new))==endpoints(new[3])
        assert len(new[2])+len(new[3])==18*m+29
        assert (1,6*m+9) in new[2]-frozen_family(m)[2]
        counts['all_length_frozen_new_black_terminals']+=1
        obstacles.append(check_obstruction(m,counts))
        if m in [2,3,8,20]:
            for seed in range(16):
                terminal,changed=random_terminal(m,seed)
                terminal_board_control(terminal,counts)
                counts['terminal_models_changing_old_matching']+=changed
                h,w,T,M=random_whole_board(m,seed,True)
                # Extend the old sampler to all white sites, including r,s.
                for v in [(5,0),(5,2)]:
                    if v in T|endpoints(M):continue
                    trial=T|{v};O=trial|endpoints(M)
                    if all(len(neighbors(u,h,w)&O)<=1 for u in trial):T=trial
                generalized_board((h,w,T,M),counts)
    out=dict(status='PASS',theorem='Two-white actual capacity without banning white selections; sharp half-area for the occupied-anchor/Bstar skeleton with arbitrary white selections; sharp maximum half-area minus one when the sole additional permitted black site is the selected terminal (1,c). All-length fully frozen new-black construction at half-area minus one; half-area-attaining actual matching refutes the independent 15-site prefix budget.',
        proof='Written structural mate/degree case proof, previous four-case pocket inequality, disjoint tail holes and explicit formulas; finite controls do not replace the proof.',
        counts=dict(counts),six_site_white_types=types,prefix_obstructions=obstacles,
        scope='Arbitrary simultaneous black selections outside Bstar remain open under retained P0; the selected single-terminal permission is settled. Prefix obstruction is not frozen and does not refute the global half-area target.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='prefix_obstructions'},indent=2))

if __name__=='__main__':main()
