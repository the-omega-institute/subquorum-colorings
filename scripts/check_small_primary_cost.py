"""Literal matching/assignment controls for exact small-cost threshold tests."""
from pathlib import Path
from itertools import combinations, permutations
from functools import lru_cache
from collections import Counter
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from small_primary_cost import primary_cost_at_most
from nonisolated_exchange_frontier import validate
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();rng=random.Random(13112699)


def literal_matching(n,E,U):
    @lru_cache(None)
    def solve(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit
        options=[solve(rest)]
        for a,b in E:
            w=b if a==v else a if b==v else None
            if w is not None and rest>>w&1:options.append(1+solve(rest^(1<<w)))
        return max(options)
    return solve(sum(1<<v for v in U))


def inspect_obstruction(data,failed):
    covered=set(failed['covered']);clauses=failed['clauses'];sources=failed['clause_edges'];q=len(data['operations'])
    assert len(clauses)==len(sources)
    E={tuple(sorted(e)) for e in data['edges']}
    for clause,(a,b) in zip(clauses,sources):
        assert tuple(sorted((a,b))) in E and a not in covered and b not in covered
        for mask in range(1<<q):
            selected={i for i in range(q) if mask>>i&1}
            final=(data['U']-{data['operations'][i][0] for i in selected})|{data['operations'][i][1] for i in selected}
            assert (a in final and b in final)==all((mask>>i&1)==s for i,s in clause)
            counts['edge_clause_truth_controls']+=1
    obs=failed['obstruction']
    if 'empty_clause' in obs:
        assert clauses[obs['empty_clause']]==[];counts['constant_edge_obstructions']+=1;return
    implications=set()
    for clause in clauses:
        assert clause
        f=[2*i+s for i,s in clause]
        if len(f)==1:f*=2
        a,b=f;implications.add((a,b^1));implications.add((b,a^1))
    v=obs['variable']
    for key,start,end in [('zero_to_one',2*v,2*v+1),('one_to_zero',2*v+1,2*v)]:
        path=obs[key];assert path[0]==start and path[-1]==end
        assert all((a,b) in implications for a,b in zip(path,path[1:]));counts['SCC_obstruction_paths']+=1


def check(n,E,U,ops):
    costs=[]
    for mask in range(1<<len(ops)):
        S={i for i in range(len(ops)) if mask>>i&1}
        final=(set(U)-{ops[i][0] for i in S})|{ops[i][1] for i in S}
        costs.append(literal_matching(n,E,final));counts['literal_assignment_costs']+=1
    optimum=min(costs);data=validate(n,E,U,ops)
    for B in range(min(n//2,2)+1):
        result=primary_cost_at_most(n,E,U,ops,B)
        assert result['feasible']==(optimum<=B)
        if result['feasible']:
            cert=result['certificate'];final=set(cert['U']);cover=set(cert['cover']);M=cert['matching'];EE={tuple(sorted(e)) for e in E}
            assert cert['actual_cost']==literal_matching(n,E,final)<=B
            assert len(cover)==len(M)==cert['actual_cost']
            assert len({v for e in M for v in e})==2*len(M)
            assert all(tuple(sorted(e)) in EE and set(e)<=final for e in M)
            assert all(a in cover or b in cover for a,b in E if a in final and b in final)
            exception=set(result['final_exception_cover'])
            assert exception<=final and len(exception)<=B
            assert all(a in exception or b in exception for a,b in E if a in final and b in final)
            counts['positive_witnesses']+=1
        if result['first_zero_obstruction'] is not None:
            inspect_obstruction(data,result['first_zero_obstruction'])
        if not result['feasible']:
            expected=sum(1 for j in range(min(B,n)+1) for _ in combinations(range(n),j))
            assert result['tested_covers']==expected;counts['exhausted_cover_searches']+=1
        counts['threshold_decisions']+=1
        digest.update(json.dumps([n,E,sorted(U),ops,B,result],sort_keys=True).encode())
    counts['models']+=1


for n in range(5):
    possible=list(combinations(range(n),2))
    for mask in range(1<<len(possible)):
        E=[e for i,e in enumerate(possible) if mask>>i&1]
        try:validate(n,E,set(),[])
        except ValueError:continue
        for umask in range(1<<n):
            U={v for v in range(n) if umask>>v&1};outside=sorted(set(range(n))-U)
            for q in range(min(len(U),len(outside))+1):
                for X in combinations(sorted(U),q):
                    for Y in permutations(outside,q):check(n,E,U,list(zip(X,Y)))
        counts['all_small_ambient_graphs']+=1

for trial in range(160):
    n=rng.randrange(5,13);order=list(range(n));rng.shuffle(order);E=list(zip(order,order[1:]))
    if n%2==0 and rng.randrange(2):E.append((order[-1],order[0]))
    U={v for v in range(n) if rng.randrange(2)};X=sorted(U);Y=sorted(set(range(n))-U);rng.shuffle(X);rng.shuffle(Y)
    q=rng.randrange(min(len(X),len(Y),5)+1);check(n,E,U,list(zip(X[:q],Y[:q])))
    counts['seeded_path_cycle_models']+=1

# One-shot calls and thresholds larger than N still obey decision semantics.
args=(4,[(0,1),(1,2),(2,3)],{0,1},[(0,2),(1,3)])
for B in (0,1,2,9):
    expected=primary_cost_at_most(*args,B)
    assert primary_cost_at_most(4,iter(args[1]),iter(args[2]),iter(args[3]),B)==expected
    counts['one_shot_controls']+=1
for bad in (-1,True,1.5):
    try:primary_cost_at_most(*args,bad)
    except ValueError:counts['invalid_threshold_rejections']+=1
    else:raise AssertionError('Invalid threshold accepted')

report=dict(scope='Fixed-list zero-cost 2SAT and exact small primary-cost XP decisions on bipartite maxdegree2 auxiliaries. Literal all assignments/matching costs, actual cover/matching witnesses and edge-traced SCC obstruction checks. No FPT, unrestricted omission, graph parameter or grid complexity claim.',counts=dict(sorted(counts.items())),digest=digest.hexdigest())
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/small-primary-cost-check.json'));dest=Path(p.parse_args().output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
