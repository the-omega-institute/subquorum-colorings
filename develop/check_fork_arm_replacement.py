"""Independent finite controls for the written simultaneous arm-replacement lemma.

All systems here are abstract; the frozen physical witness is checked separately.
Hall subsets are compared with ordinary terminal min-cost flow, including
mixed-arm lengths, prefix witnesses and pre-used original interval identities.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_whole_support_fork_normal_form import canonical,ordinary_flow

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def hall(neighbors):
    for mask in range(1,1<<len(neighbors)):
        chosen=[v for i,v in enumerate(neighbors) if mask>>i&1]
        if len(set().union(*chosen))<len(chosen):return False
    return True


def model(q,lengths,choices,preused):
    types=[];routes=[];betas=[]
    for f in range(q):
        arms=[]
        for side in range(2):
            arm=[len(types)];types.append('A')
            for _ in range(lengths[2*f+side]):arm.append(len(types));types.append('M')
            arms.append(arm)
        beta=len(types);types.append('B');betas.append(beta);routes.append((arms,beta))
    kinds,pairs,_=canonical(types);links=[];support={i:set() for i in range(len(types))}
    # Negative IDs are distinct beta-body intervals; nonnegative IDs are
    # candidate old arm resources, filtered by the residual certificate U.
    resources={-1-f for f in range(q)}
    neighbors=[];fork_cost=0
    for f,(arms,beta) in enumerate(routes):
        support[beta]={-1-f};available=set()
        for side,arm in enumerate(arms):
            for x,y in zip(arm,arm[1:]):
                links.append((pairs[x][0 if types[x]=='A' else 1],pairs[y][0]))
            links.append((pairs[arm[-1]][0 if types[arm[-1]]=='A' else 1],pairs[beta][side]))
            fork_cost+=len(arm)
            for pos,owner in enumerate(arm):
                support[owner]=set(choices[f,side,pos])-preused
                available|=support[owner];resources|=support[owner]
        neighbors.append(available)
    return (kinds,pairs,links,support,resources),neighbors,fork_cost


def check(q,lengths,choices,preused,totals):
    data,neighbors,cost=model(q,lengths,choices,preused)
    flow=ordinary_flow(*data)
    assert (flow['value']==2*q)==hall(neighbors)
    if hall(neighbors):
        assert flow['cost']<=cost-q
        totals['full_replacements']+=1
    else:totals['Hall_obstructions']+=1
    totals['systems']+=1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter()
    for q,r in [(1,3),(2,2),(3,1)]:
        for mask in range(1<<(2*q*r)):
            choices={(f,s,0):{j for j in range(r) if mask>>(r*(2*f+s)+j)&1}
                     for f in range(q) for s in range(2)}
            check(q,[0]*(2*q),choices,set(),totals)
    rng=random.Random(20261025)
    for _ in range(400):
        q=rng.randrange(1,5);r=rng.randrange(1,6)
        lengths=[rng.randrange(3) for _ in range(2*q)]
        choices={(f,s,p):{j for j in range(r) if rng.randrange(3)==0}
                 for f in range(q) for s in range(2) for p in range(lengths[2*f+s]+1)}
        preused={j for j in range(r) if rng.randrange(4)==0}
        check(q,lengths,choices,preused,totals)
    # Both forks can be replaced separately, but jointly their two candidate
    # arm intervals are the SAME old unit. No separate beta-body unit is
    # available to an ordinary stem before entering its beta sink.
    choices={(f,s,0):({0} if s==0 else set()) for f in range(2) for s in range(2)}
    data,neighbors,cost=model(2,[0]*4,choices,set())
    flow=ordinary_flow(*data)
    assert neighbors==[{0},{0}] and not hall(neighbors)
    assert flow['value']==3 and cost==4
    result=dict(status='PASS',totals=dict(totals),shared_old_unit_control=dict(
        forks=2,neighbors=[[0],[0]],fork_value=4,ordinary_value=3),
        scope='Abstract finite checks only. General Hall equivalence and subset-of-links '
              'replacement proof are written; no claim these collision systems are frozen grids.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
