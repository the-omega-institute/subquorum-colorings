"""Check the original-alpha two-external-witness and Hall-defect bounds.

The all-configuration argument is written in the accompanying note. No C0
cancellation is accepted here: the original missing-tip injection is essential.
"""
import argparse
from collections import Counter, defaultdict, deque
import itertools
import json
from pathlib import Path

from check_boundary_sealed_gap_obstruction import family, stack
from check_frozen_missing_port_bp_injection import inspect as inject
from check_frozen_support_tree_reroot import fixture, model_at
from check_interior_support_tree_caps import capped
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_tree_beta_compensation import joint_allocate, min_cost_matching
from check_neutral_portal_strip_compensation import image_map
from check_residual_corridors import transformed
from check_terminal_cancellation_and_stranded_demand import terminal_data

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def hall_set(t,graph,matched):
    """Alternating reachability from unmatched left vertices; no subset search."""
    reached=set(range(t))-set(matched)
    pending=deque(reached); right=set()
    inverse={b:i for i,b in matched.items()}
    while pending:
        i=pending.popleft()
        for b,users in graph.items():
            if i in users and b not in right:
                right.add(b)
                if b in inverse and inverse[b] not in reached:
                    reached.add(inverse[b]);pending.append(inverse[b])
    assert right=={b for b,users in graph.items() if users & reached}
    assert len(reached)-len(right)==t-len(matched)
    return reached


def check_inequality(tokens,graph,matched,totals,all_subsets):
    t=len(tokens)
    assert all(len(row)==2 for row in tokens)
    multiplicity=Counter(dest for row in tokens for dest in row)
    assert all(n <= (2 if dest[0]=='beta' else 1) for dest,n in multiplicity.items())
    assert all(i in graph[dest[1]] for i,row in enumerate(tokens) for dest in row if dest[0]=='beta')
    x=hall_set(t,graph,matched)
    choices=itertools.chain([x],({i for i in range(t) if mask>>i & 1}
        for mask in range(1<<t))) if all_subsets else [x]
    for subset in choices:
        neighbors={b for b,users in graph.items() if users & subset}
        zero={dest for i in subset for dest in tokens[i] if dest[0]!='beta'}
        assert 2*len(subset)<=2*len(neighbors)+len(zero)
        totals['subset_degree_inequalities']+=1
    zero={dest for row in tokens for dest in row if dest[0]!='beta'}
    delta=t-len(matched)
    assert 2*delta<=len(zero)
    totals['hall_defect_bounds']+=1
    totals['positive_beta_hall_defects']+=delta>0
    return dict(trees=t,mu=len(matched),joint_defect=delta,
                distinct_mixed_witnesses=sum(d[0]=='mixed' for d in zero),
                distinct_mark_witnesses=sum(d[0]=='mark' for d in zero),
                hall_set=sorted(x),zero_witness_bound=len(zero)//2)


def physical(current,bands,totals):
    data,meta,rep,model,betas,_=model_at(current,bands)
    injection=dict(inject(current,bands,Counter(),True)['assignment'])
    original,_,intervals,owner,kinds,pairs,ports=terminal_data(current,bands)
    assert len(model['alphas'])==original['alpha']
    pair_owner={v:i for i,pair in enumerate(pairs) for v in pair}
    rows=[]
    for a,pair in enumerate(model['alphas']):
        row=[]
        for tip in pair:
            if ports[tip]:
                choices={owner[p] for p in ports[tip]}
                j=min(choices,key=lambda j:(j in meta['boundary'],j))
                dest=('mark' if j in meta['boundary'] else 'interval',j)
                if dest[0]=='interval':
                    assert a in model['incidence'][j]
                record=dict(alpha=a,tip=tip,destination=dest)
            else:
                bp=injection[tip]; p=pair_owner[bp]
                kind='beta' if all(kinds[v]=='BP' for v in pairs[p]) else 'mixed'
                assert kinds[bp]=='BP' and (tip,bp) in data[2]
                dest=(kind,p)
                record=dict(alpha=a,tip=tip,destination=dest,link=(tip,bp))
            row.append(record)
        rows.append(row)
    counts=Counter(tuple(r['destination']) for row in rows for r in row)
    assert all(n <= (2 if d[0] in ('interval','beta') else 1) for d,n in counts.items())
    result=joint_allocate(len(rows),model['incidence'],betas)
    # Convert beta identity to the ORIGINAL strand index used by the token rows.
    reduced_betas=[pair for pair in model['reduced'] if all(kinds[v]=='BP' for v in pair)]
    beta_original={b:pair_owner[pair[0]] for b,pair in enumerate(reduced_betas)}
    graph={beta_original[b]:users for b,users in result['collapsed'].items()}
    matched={i:beta_original[b] for i,b in result['matched'].items()}
    external=[]; selected=[]
    for tree in result['trees']:
        inside=set(tree['resources']); demands=set(tree['demands'])
        row=[r for a in tree['demands'] for r in rows[a]]
        internal=[r for r in row if r['destination'][0]=='interval']
        assert all(r['destination'][1] in inside for r in internal)
        assert len(internal)<=2*(len(demands)-1)
        outside=[r for r in row if r['destination'][0]!='interval']
        assert len(outside)>=2
        chosen=outside[:2]
        external.append([tuple(r['destination']) for r in chosen]);selected.append(chosen)
    record=check_inequality(external,graph,matched,totals,len(external)<=10)
    totals['original_alpha_physical_models']+=1
    totals['original_alpha_tokens']+=2*len(rows)
    totals['physical_nonsingleton_witness_trees']+=sum(len(t['demands'])>1 for t in result['trees'])
    return dict(shape=current[:2],alpha=rep['alpha'],tokens=rows,
                selected_external_witnesses=selected,**record)


def abstract_controls(totals):
    destinations=[('beta',0),('beta',1),('mixed',0),('mixed',1),('mark',0),('mark',1)]
    rows=list(itertools.combinations_with_replacement(destinations,2))
    examples=[]
    for t in range(5):
        for tokens in itertools.product(rows,repeat=t):
            counts=Counter(d for row in tokens for d in row)
            if any(n>(2 if d[0]=='beta' else 1) for d,n in counts.items()):
                continue
            graph={b:{i for i,row in enumerate(tokens) if ('beta',b) in row} for b in range(2)}
            matched=min_cost_matching(t,graph,lambda i,b:0)
            rec=check_inequality(tokens,graph,matched,totals,True)
            # Hall's exact maximum deficiency independently enumerated.
            deficiency=max((len(x)-sum(bool(users & x) for users in graph.values())
                for x in ({i for i in range(t) if mask>>i & 1} for mask in range(1<<t))),default=0)
            assert deficiency==rec['joint_defect']
            totals['abstract_two_token_models']+=1
            if t==1 and tokens==((('mixed',0),('mixed',1)),):
                assert rec['joint_defect']==rec['zero_witness_bound']==1
                examples.append(dict(tokens=tokens,kind='sharp-abstract-zero-credit-ends',**rec))
    return examples


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();records=[]
    base,_=fixture()
    records.append(physical(base,whole_bands(base),totals))
    for d in range(1,9):
        current,_=capped(d)
        records.append(physical(current,whole_bands(current),totals))
        wider=(current[0],current[1]+8,current[2],current[3])
        records.append(physical(wider,whole_bands(wider),totals))
    current,_=capped(1)
    for q in range(1,17):
        copies=stack(current,q)
        records.append(physical(copies,whole_bands(copies),totals))
    for symmetry in itertools.product((False,True),repeat=3):
        shape,sel,mat=transformed(*current,*symmetry)
        move=image_map(*current[:2],symmetry)
        bands=[[tuple(map(move,col)) for col in band] for band in whole_bands(current)]
        records.append(physical((*shape,sel,mat),bands,totals))
    for w in (6,8,12):
        for h in (4,6,10):
            current,crop,_=family(w,h,h+8)
            records.append(physical(current,crop,totals))
            records.append(physical(current,whole_bands(current),totals))
    examples=abstract_controls(totals)
    # Keep explicit original identities for the base and first interior cap.
    # Larger certificates are regenerated from the constructors and injection.
    for record in records[2:]:
        record['checked_original_tokens']=sum(map(len,record.pop('tokens')))
        record['checked_external_tokens']=sum(map(len,record.pop('selected_external_witnesses')))
    receipt=dict(status='PASS',totals=dict(totals),physical=records,abstract_examples=examples,
        scope='Original completely frozen alpha strands only; C0 empty. Each deficient '
              'whole-support tree supplies two external tokens. Whole beta capacity2, '
              'mixed/marked capacity1; 2|X|<=2|N_beta(X)|+q(X)+h(X), '
              'joint beta defect<=floor((q+h)/2). Zero-credit tokens are NOT payments. '
              'Written geometric injection and Hall argument remain distinct from these checks.')
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':
    main()
