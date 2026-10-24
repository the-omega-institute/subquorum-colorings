"""Controls for the general guarded-pocket proof; enumeration is not its proof."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_even_bridge_support_completion import endpoints_of
from check_frozen_beta_support_fork import fixture,stacked,A,C,B,FORK
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import whole_support_data,primitive_certificates,evaluate,ordinary_flow,canonical

if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')

POCKET=((12,3),(12,4),(13,3),(13,4))
EDGE=((12,3),(12,4))


def local_states():
    base,_=fixture();old=endpoints_of(base);out=[]
    for labels in itertools.product('BTP',repeat=4):
        selected=base[2]|{v for v,k in zip(POCKET,labels) if k=='T'}
        added={v for v,k in zip(POCKET,labels) if k=='P'}
        occupied=selected|old|added
        adjacent=lambda a,b:sum(abs(x-y) for x,y in zip(a,b))==1
        if any(sum(adjacent(t,w) for w in occupied)>1 for t in selected):continue
        # Every new endpoint must have a new adjacent mate. Old endpoints
        # already have immutable mates. The lower pocket cells are forbidden
        # occupied by the old selected guards; all remaining neighbors of a
        # top pocket cell except the other top cell are old matched vertices.
        if any(not any(adjacent(v,w) for w in added-{v}) for v in added):continue
        if added and added!=set(EDGE):continue
        out.append(''.join(labels))
    assert out==['BBBB','PPBB']
    return out


def feasible(current):
    try:direct_check(*current)
    except AssertionError:return False
    return True


def extend(seed,insert):
    rng=random.Random(seed);base,_=fixture()
    current=(*base[:3],base[3]+([EDGE] if insert else []))
    # Keep the designated old beta's BP tips and one body interval so the
    # fork whose replacement is being tested still exists.
    protected={(4,6),(13,6),(8,7),(9,7)}
    actions=[('T',((r,c),)) for r in range(16) for c in range(14)]
    actions += [('M',((r,c),(r+dr,c+dc))) for r in range(16) for c in range(14)
                for dr,dc in ((0,1),(1,0)) if r+dr<16 and c+dc<14]
    rng.shuffle(actions);changes=0
    for kind,vertices in actions:
        if set(vertices)&protected:continue
        if any(c in (0,13) for r,c in vertices):continue
        occupied=current[2]|endpoints_of(current)
        if set(vertices)&occupied:continue
        candidate=(current[0],current[1],current[2]|set(vertices) if kind=='T' else current[2],
                   current[3]+[vertices] if kind=='M' else current[3])
        if not feasible(candidate):continue
        if kind=='M' and frozen_certificate(candidate)[0]!=endpoints_of(candidate):continue
        current=candidate;changes+=1
        if changes==8:break
    return current,changes


def replay(data,pack):
    allowners=[o for p in pack for o in p['owners']]
    units=[p['interval'] for p in pack if p['interval'] is not None]
    assert len(allowners)==len(set(allowners)) and len(units)==len(set(units))
    keep=set(allowners);pairs=[pair for o,pair in enumerate(data[1]) if o in keep]
    free={v for pair in pairs for v in pair}
    chosen=[e for p in pack for e in p['links']]
    support={i:data[3][o] for i,o in enumerate(o for o in range(len(data[1])) if o in keep)}
    restricted=({v:data[0][v] for v in free},pairs,
                [e for e in data[2] if set(e)<=free],support,data[4])
    result=evaluate(*restricted[:2],chosen,*restricted[3:])
    assert result['value']==sum(p['value'] for p in pack)
    return len(chosen)


def check(current,copies,rng,totals):
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,_=whole_support_data(current,whole_bands(current))
    owners,alphas,betas,_=owner_data(*data[:2])
    primitives=primitive_certificates(*data);fixed=[];replacement=[];held=set();used=set()
    empty=filled=0
    for i in range(copies):
        move=lambda v:(v[0]+16*i,v[1]);a,c,b=(owners[move(x[0])] for x in (A,C,B))
        assert a in alphas and c in alphas and b in betas
        links=tuple(tuple(map(move,e)) for e in FORK)
        f=next(p for p in primitives if p['kind']=='fork' and p['beta']==b and set(p['links'])==set(links))
        fixed.append(f);held|=set(f['owners']);used.add(f['interval'])
        left=next(p for p in primitives if p['kind']=='beta' and p['links']==(links[0],))
        top=tuple(map(move,EDGE));lower=tuple(map(move,POCKET[2:]))
        assert not set(lower)&(current[2]|endpoints_of(current))
        if not set(top)&endpoints_of(current):
            assert not set(top)&current[2]
            js={meta['owner'][6+8*i,col] for col in (3,4)}
            assert len(js)==2 and js<=data[4]
            assert all({o for o,w in data[3].items() if j in w}=={c} for j in js)
            j=min(js)
            right=next(p for p in primitives if p['kind']=='interval' and p['owners']==(c,) and p['interval']==j)
            empty+=1
        else:
            assert set(top)<=endpoints_of(current)
            assert any(set(e)==set(top) for e in current[3])
            e=owners[top[0]];assert e==owners[top[1]] and e in betas and e!=b
            incoming=[edge for edge in data[2] if owners[edge[1]]==e]
            assert incoming and {owners[edge[0]] for edge in incoming}=={c}
            right=next(p for p in primitives if p['kind']=='beta' and p['beta']==e and set(p['owners'])=={c,e})
            filled+=1
        replacement.extend([left,right])
    # Keep an arbitrary compatible collection of OTHER ordinary/fork
    # certificates unchanged. In particular do not reserve the new beta by
    # assumption: its inaccessibility from outside C is checked above.
    others=[];shuffled=list(primitives);rng.shuffle(shuffled)
    for p in shuffled:
        if held&set(p['owners']) or p['interval'] in used:continue
        if rng.randrange(3)==0:continue
        others.append(p);held|=set(p['owners'])
        if p['interval'] is not None:used.add(p['interval'])
    old=fixed+others;new=replacement+others
    oldcost=replay(data,old);newcost=replay(data,new)
    assert newcost==oldcost-empty
    assert sum(p['value'] for p in old)==sum(p['value'] for p in new)
    assert sum(p['kind']=='fork' for p in new)==sum(p['kind']=='fork' for p in old)-copies
    totals['boards']+=1;totals['pockets']+=copies
    totals['empty_private_interval_replacements']+=empty
    totals['filled_exclusive_beta_replacements']+=filled
    totals['outside_certificates_preserved']+=len(others)
    totals['actual_links_saved']+=oldcost-newcost
    return dict(copies=copies,endpoints=len(endpoints_of(current)),empty_pockets=empty,
                filled_pockets=filled,old_links=oldcost,new_links=newcost,
                unchanged_outside_certificates=len(others))


def mixed_arm_controls(totals):
    for length in range(1,13):
        for other_length in range(1,7):
            for filled in (False,True):
                count=length+other_length-2
                kinds,pairs,_=canonical('AAB'+'M'*count+('B' if filled else '')+'A')
                support={o:set() for o in range(len(pairs))}
                support[2]={0};support[len(pairs)-1]={2}
                if not filled:support[0]={1}
                def arm(source,mixed,tip):
                    out=[];p=pairs[source][0]
                    for o in mixed:
                        out.append((p,pairs[o][0]));p=pairs[o][1]
                    return out+[(p,tip)]
                left=arm(0,range(3,3+length-1),pairs[2][0])
                right=arm(1,range(3+length-1,3+count),pairs[2][1])
                links=left+right
                if filled:links.append((pairs[0][1],pairs[3+count][0]))
                data=(kinds,pairs,links,support,{0,2} if filled else {0,1,2})
                primitives=primitive_certificates(*data)
                f=next(p for p in primitives if p['kind']=='fork')
                other=next(p for p in primitives if p['kind']=='beta' and p['links']==tuple(right))
                if filled:
                    replacement=next(p for p in primitives if p['kind']=='beta' and p['links']==(links[-1],))
                else:
                    replacement=next(p for p in primitives if p['kind']=='interval'
                                     and p['owners']==(0,) and p['interval']==1)
                outside=next(p for p in primitives if p['kind']=='interval' and p['interval']==2)
                before=replay(data,[f,outside]);after=replay(data,[other,replacement,outside])
                assert before-after==length-(1 if filled else 0)
                flow=ordinary_flow(*data)
                assert (flow['value'],flow['cost'])==(3,other_length+(1 if filled else 0))
                totals['abstract_mixed_arm_replacements']+=1
                totals['abstract_tied_fork_controls']+=filled and length==1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();rng=random.Random(20261028);controls=[]
    states=local_states();mixed_arm_controls(totals)
    for insert in (False,True):
        for seed in range(100):
            current,changes=extend(20261028+seed,insert)
            controls.append(dict(seed=seed,initial_insertion=insert,added_actions=changes,
                                 **check(current,1,rng,totals)))
            totals['accepted_extension_actions']+=changes
    for q in range(1,9):
        for pattern in ('none','all','alternating'):
            current=stacked(q)
            additions=[tuple((r+16*i,c) for r,c in EDGE) for i in range(q)
                       if pattern=='all' or pattern=='alternating' and i%2==0]
            current=(*current[:3],current[3]+additions)
            controls.append(dict(pattern=pattern,**check(current,q,rng,totals)))
            data,_,_=whole_support_data(current,whole_bands(current))
            owner=owner_data(*data[:2])[0]
            guarded={owner[(C[0][0]+16*i,C[0][1])] for i in range(q)}
            assert all(set(p['owners'])&guarded for p in primitive_certificates(*data)
                       if p['kind']=='fork')
            flow=ordinary_flow(*data)
            assert (flow['value'],flow['cost'])==(3*q,q+len(additions))
            totals['exact_stack_ordinary_value_cost_controls']+=1
    report=dict(status='PASS',local_label_assignments=81,feasible_local_states=states,
                totals=dict(totals),controls=controls,
                scope='General guarded-pocket monotone-extension dichotomy and compatible-packing '
                      'replacement have written proofs. Finite controls verify fully frozen '
                      'extensions and simultaneous distinct-resource replacements with unchanged '
                      'outside certificates. Does not prove all-grid compensation or forbid '
                      'every fork in every tied lexicographic optimum.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
