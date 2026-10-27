"""A single global HH-source budget for any number of TH centres.

Refine the two-centre branch to require an eligible F centre and an
ineligible E centre. When every centre is eligible this branch disappears.
All physical pair routines retain the inherited actual-edge capacities.
"""
from check_mixed_terminal_compensation import mates
from strip_tree_compensation import physical_state_linear
from hall_barrier_pair_bound import (certify_hall_barrier_bound,
    quota_pair_relaxation,complete_fixed_th_paths)


def terminal_balance(board,m,n,t,centres,barrier):
    board=set(board);t=set(t);centres=set(centres)
    p=set(mates(board,m));q=board-p;white={v for v in q if sum(v)%2};holes=white-t
    if not t<=white or not centres<={v for v in q if sum(v)%2==0}:
        raise ValueError('White selected T and black Q centres required')
    if len(holes)!=len(centres)-1:raise ValueError('Exactly r-1 white HH sources required')
    F=set(barrier['forbidden']);E=set(barrier['exposable']);D=set(barrier['dark'])
    if F&E or F|E!=t or not D<=q-centres or any(sum(v)%2 for v in D) or len(D)!=len(F):
        raise ValueError('Balanced exterior D,F and a white T partition required')
    state=physical_state_linear(board,m,n,t);pairs=[]
    for path in state['data']['paths']:
        a,b=path['vertices'][0],path['vertices'][-1]
        if sum(a)%2==0:a,b=b,a
        assert sum(a)%2==1 and sum(b)%2==0
        pairs.append((a,b))
    outgoing=sum(a in F and b not in D for a,b in pairs)
    th_incoming=sum(a in E and b in D for a,b in pairs)
    hh_incoming=sum(a in holes and b in D for a,b in pairs)
    paid_centres=sum(a in t and b in centres for a,b in pairs)
    hh_outside=sum(a in holes and b not in centres for a,b in pairs)
    assert outgoing==th_incoming+hh_incoming
    assert paid_centres>=1 and hh_outside==paid_centres-1 and hh_incoming<=hh_outside
    all_centre_sources_F=all(a in F for a,b in pairs if a in t and b in centres)
    if all_centre_sources_F:
        assert outgoing>=paid_centres and th_incoming>=1
    return dict(a=outgoing,b=th_incoming,c=hh_incoming,k=paid_centres,
                HH_outside_centres=hh_outside,all_TH_centre_sources_in_F=all_centre_sources_F,
                terminal_pairs=pairs,state=state)


def two_cheap_centre_family(k):
    """Fixed canonical 18x18 model: old bound 2, refined bound/optimum K.

    The proof is symbolic for every integer K>=3; the checker rescoring
    explicit full matchings is supplementary finite evidence.
    """
    from branched_source_obstruction import branched_family
    from check_mixed_terminal_compensation import edge
    if type(k) is not int or k<3:raise ValueError('Integer K>=3 required')
    result=branched_family()
    cheap={edge((2,2),(3,2)),edge((6,8),(7,8))}
    result.update(cheap_edges=cheap,weights={e:1 if e in cheap else k for e in result['M']})
    return result


def certify_multicentre_bound(board,m,t,parts,centres,weights=None):
    previous=certify_hall_barrier_bound(board,m,t,parts,centres,weights)
    base=previous['base'];barrier=previous['barrier'];C=set(base['centres'])
    eligible={base['centres'][i] for i in base['eligible_roots']};ineligible=C-eligible
    mixed=quota_pair_relaxation(base['board'],base['M'],base['T'],base['weights'],
                               [barrier['forbidden'],barrier['exposable']],[eligible,ineligible])
    candidates=[v for v in (base['normal_form_optimum'],previous['Hall_pair']['minimum'],mixed['minimum']) if v is not None]
    lower=max(base['source_budget'],min(candidates)) if candidates else None
    assert lower is None or previous['lower_bound'] is None or lower>=previous['lower_bound']
    upper=base['normal_form_optimum'];exact=upper is not None and lower==upper
    if not ineligible:assert mixed['minimum'] is None
    return dict(previous=previous,base=base,barrier=barrier,Hall_pair=previous['Hall_pair'],
                mixed_centre_pair=mixed,all_roots_eligible=not ineligible,
                lower_bound=lower,normal_form_upper=upper,global_optimum_certified=exact,
                minimum_TH_fee=upper if exact else None)


def solve_multicentre_completion(board,m,t,parts,centres,weights=None):
    """Sufficient optimality certificate; failure is not global infeasibility."""
    result=certify_multicentre_bound(board,m,t,parts,centres,weights);base=result['base']
    result.update(auxiliary=base['auxiliary'],state=base['state'],extension_attempts=[],
                  completion_kind='normal_form_upper',normal_form_globally_optimal=result['global_optimum_certified'])
    if result['global_optimum_certified']:
        result['completion_kind']='normal_form_optimum';return result
    for key in ['Hall_pair','mixed_centre_pair']:
        pair=result[key]
        if pair['minimum'] is None or pair['minimum']!=result['lower_bound']:continue
        extension=complete_fixed_th_paths(base['board'],base['M'],base['T'],[p['vertices'] for p in pair['paths']])
        result['extension_attempts'].append(dict(kind=key,**extension))
        if not extension['feasible']:continue
        fee=sum(base['weights'][e] for e in extension['fixed_actual'])
        assert fee==result['lower_bound']
        result.update(auxiliary=extension['auxiliary'],state=extension['state'],completion_kind=key+'_optimum',
                      global_optimum_certified=True,minimum_TH_fee=fee)
        return result
    return result
