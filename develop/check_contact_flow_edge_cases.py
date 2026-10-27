"""Post-submission zero-cost terminals, physical bottleneck and off-diagonal checks."""
import json
from pathlib import Path
from check_contact_flow_cut import (
    control, edge, greedy_family, physical, specified_gates, star_family,
)

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT=Path(__file__).resolve().parents[1]


def main():
    n={edge((r,0),(r,1)) for r in range(2)};m=set();t={(0,0),(0,1)}
    zero=[]
    for squares in [[],[(0,0)]]:
        gates=specified_gates(2,2,m,n,t,squares);net,actual=physical(2,2,m,n,t,gates)
        r=control(net,actual,weighted=True)
        assert r['delta']==(0 if squares else 1)
        zero.append(dict(contacts=len(gates),flow=r['flow'],minimum_TT=r['delta'],M=0))
    d=star_family('HHHTTT');h,w,m,n,t=[d[k] for k in ['h','w','M','N','T']]
    gates=specified_gates(h,w,m,n,t,d['squares']);net,actual=physical(h,w,m,n,t,gates)
    r=control(net,actual);U={3,4,5};exits=[j for j,(u,v,_,_) in enumerate(net.arcs)
        if u[0]==v[0]=='g' and u[1] in U and v[1] not in U]
    assert len(exits)==1 and net.cut(U)==r['delta']==2
    bottleneck=dict(word='HHHTTT',cut_contact_ids=sorted(U),supplies=3,hole_exits=0,
        interior_exit_fragments=1,minimum_TT=2,flow=r['flow'],
        unique_exit_M_edges=[[[*a],[*b]] for a,b in sorted(net.resources[exits[0]])],
        unique_exit_M_weight=net.arcs[exits[0]][2])
    offdiagonal=[]
    for L,d in [(4,1),(4,7),(6,1),(6,2),(8,3),(10,1),(12,5),(16,2)]:
        h,w,m,n,t,squares=greedy_family(L,d);gates=specified_gates(h,w,m,n,t,squares)
        assert all(g['vertices']<={v for e in m for v in e} for g in gates)
        net,actual=physical(h,w,m,n,t,gates);control(net,actual,weighted=True)
        joint=net.cost_model();lex=net.cost_model(True)
        assert joint['cost']==5*d+5*L+78
        assert joint['red_cost']==2*L+4*d+70
        assert lex['cost']==(L+5)*d+7*L+80 and lex['red_cost']==2*d+42
        assert joint['switches']=={0,1} and lex['switches']=={2}
        for bits in range(8):actual({j for j in range(3) if bits>>j&1})
        offdiagonal.append(dict(L=L,d=d,joint_cost=joint['cost'],sequential_cost=lex['cost']))
    out=dict(status='PASS',zero_M_terminal_controls=zero,physical_star_cut=bottleneck,
        offdiagonal_greedy_families=offdiagonal,
        scope='Local post-submission additions; not part of the independent reviewer execution packet. General proofs remain in notes.')
    (ROOT/'output/contact-flow-edge-cases.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
