"""Frozen vertical-fork escape and serial-skeleton compensation controls.

General proofs: docs/FROZEN_SERIAL_FORK_ESCAPE.md. No optional solver needed.
Physical local controls and abstract serial allocation controls are separate.
"""
import argparse
from collections import Counter,defaultdict
import itertools,json,random
from pathlib import Path
from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors
from check_coupled_link_retraction import serial
from check_frozen_beta_fork_escape import fixture as escape_fixture
from check_frozen_shared_mixed_gate import check_rank_certificate,fixture as head_fixture
from check_interacting_square_switches import model as switched_model
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import whole_support_data,ordinary_flow,contract,evaluate
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Run without -O; assertions required.')


def scan(cur,totals):
    direct_check(*cur)
    frozen,layers=frozen_certificate(cur)
    mate={v:w for e in cur[3] for v,w in (e,e[::-1])}
    assert frozen==set(mate)
    rank={tuple(w['endpoint']):i for i,layer in enumerate(layers) for w in layer}
    check_rank_certificate(cur,[[tuple(w['endpoint']) for w in layer] for layer in layers])
    data,meta,_=whole_support_data(cur,whole_bands(cur))
    owner,aa,bb,mm=owner_data(*data[:2]);O=set(mate)|cur[2]
    heads={}
    for x in mm:
        bp=next(v for v in data[1][x] if data[0][v]=='BP')
        r,c=bp
        adj=[(r,c-1),(r,c+1)]
        if not all(data[0].get(a)=='TP' and owner[a] in aa for a in adj):continue
        assert owner[adj[0]]!=owner[adj[1]]
        assert all(mate[a][1]==a[1] for a in adj)
        assert mate[bp]==(r+(1 if r%2 else -1),c)
        tp=next(v for v in data[1][x] if data[0][v]=='TP')
        assert mate[tp][1]==tp[1]
        heads[x]=bp;totals['actual_alpha_alpha_mixed_heads']+=1
    motifs=[]
    for t in sorted(data[0]):
        if data[0][t]!='TP' or mate[t][1]!=t[1]:continue
        r,c=t;eps=1 if r%2 else -1
        for s in (-1,1):
            b,u,n=(r,c-s),(r,c-2*s),(r,c+s)
            if data[0].get(b)!='BP' or owner[b] not in bb or data[0].get(u)!='TP':continue
            a,bm,z,h=(r+eps,c),(r+eps,c-s),(r+eps,c+s),(r+2*eps,c)
            assert mate[t]==a and mate[b]==bm
            assert rank[a]<rank[b]
            assert z in O and h in O
            assert z in cur[2] or rank[mate[z]]<rank[a]
            assert n not in cur[2]
            item=dict(tip=t,beta_entry=b,owner=owner[t],nested_head=heads.get(owner[t]))
            if n in mate:
                assert data[0][n]=='BP' and mate[n]==(r,c+2*s)
                assert z in mate and rank[mate[z]]<rank[a]<rank[n]
                item.update(kind='BP',target=n,target_owner=owner[n])
                if owner[t] in mm:
                    bp=next(v for v in data[1][owner[t]] if data[0][v]=='BP')
                    if mate[bp][1]==bp[1]:
                        assert owner[n]!=owner[t]
                        totals['actual_double_vertical_mixed_bp_escapes']+=1
            else:
                assert n not in O and (r^1,n[1]) not in O
                j=meta['owner'][r//2,n[1]]
                marked=j in meta['boundary']
                assert marked or j in data[3][owner[t]]
                item.update(kind='BB',target=j,marked=marked,coordinate=meta['intervals'][j])
            if item['nested_head'] is not None:totals['actual_complete_nested_motifs']+=1
            motifs.append(item)
    bp=[x for x in motifs if x['kind']=='BP'];ports=[x for x in motifs if x['kind']=='BB']
    assert len({x['target'] for x in bp})==len(bp)
    # Actual color identifies ORIGINAL beta units, not the two BP entrances.
    for color in (0,1):
        chosen=[x for x in bp if sum(x['tip'])%2==color]
        owners=[x['target_owner'] for x in chosen]
        assert len(owners)==len(set(owners))
        totals['same_color_actual_owner_injection_checks']+=1
    counts=Counter(x['target'] for x in ports)
    assert all(v<=2 for v in counts.values())
    marked=Counter(x['target'] for x in ports if x['marked'])
    assert all(v==1 for v in marked.values())
    # Separately exercise the immediate-BB-to-original-identity adapter on
    # all actual TP ports. These are not labelled beta-fork escape instances.
    direct=[]
    for t in data[0]:
        if data[0][t]!='TP':continue
        for s in (-1,1):
            c=t[1]+s
            if not 0<=c<cur[1] or (t[0],c) in O or (t[0]^1,c) in O:continue
            j=meta['owner'][t[0]//2,c]
            assert j in meta['boundary'] or j in data[3][owner[t]]
            direct.append((t,j))
    direct_counts=Counter(j for t,j in direct)
    assert max(direct_counts.values(),default=0)<=2
    assert all(v<=1 for j,v in direct_counts.items() if j in meta['boundary'])
    totals['separate_actual_immediate_bb_port_checks']+=len(direct)
    totals['physical_frozen_models']+=1
    totals['actual_vertical_beta_fork_motifs']+=len(motifs)
    totals['actual_forced_bp_targets']+=len(bp)
    totals['actual_forced_bb_ports']+=len(ports)
    return motifs


def reflect(cur,fr,fc):
    mv=lambda v:(cur[0]-1-v[0] if fr else v[0],cur[1]-1-v[1] if fc else v[1])
    return (*cur[:2],{mv(v) for v in cur[2]},[tuple(map(mv,e)) for e in cur[3]])


def physical(totals):
    records=[]
    for q,pad,plug in itertools.product(range(1,5),(0,2),(False,True)):
        cur,_=escape_fixture(q,pad,plug)
        for fr,fc in itertools.product((False,True),repeat=2):
            motifs=scan(reflect(cur,fr,fc),totals)
            records.append(dict(family='earlier_beta_escape',copies=q,padding=pad,plug=plug,
                                reflect_rows=fr,reflect_columns=fc,motifs=len(motifs)))
    cur=head_fixture()
    switched=switched_model()[0]
    for name,base in [('earlier_shared_head',cur),('earlier_double_switch',switched)]:
        for fr,fc in itertools.product((False,True),repeat=2):
            motifs=scan(reflect(base,fr,fc),totals)
            records.append(dict(family=name,reflect_rows=fr,reflect_columns=fc,motifs=len(motifs)))
    new=Path(__file__).parent/'fixtures/frozen_nested_serial_fork.json'
    if new.exists():
        x=json.loads(new.read_text());base=(*x['shape'],set(map(tuple,x['selected'])),[tuple(map(tuple,e)) for e in x['matching']])
        for fr,fc in itertools.product((False,True),repeat=2):
            motifs=scan(reflect(base,fr,fc),totals)
            assert any(m['nested_head'] is not None for m in motifs)
            records.append(dict(family='new_nested_fork',reflect_rows=fr,reflect_columns=fc,motifs=len(motifs)))
    assert totals['actual_vertical_beta_fork_motifs']>0
    assert totals['actual_alpha_alpha_mixed_heads']>0
    assert totals['actual_forced_bp_targets']>0
    assert totals['separate_actual_immediate_bb_port_checks']>0
    return records


def decorated(lengths,spec):
    kinds={};pairs=[];links=[];W={};old=[];baseline=[];roles=[]
    for n,case in zip(lengths,spec):
        d,C=serial(n);offset=len(pairs);tipoffset=2*offset
        mv=lambda e:tuple(v+tipoffset for v in e)
        kinds.update({v+tipoffset:k for v,k in d[0].items()});pairs.extend(map(mv,d[1]));links.extend(map(mv,d[2]))
        W.update({o+offset:set() for o in d[3]});old.extend(map(mv,C))
        baseline.extend(mv((d[1][n+i][1],d[1][2*n+max(0,i-1)][0])) for i in range(n) if i!=1)
        source=offset+n+1;tp=pairs[source][1]
        roles.append((source,tp,case))
    resources={int(case[1:]) for case in spec if case.startswith('I')}
    extra=[]
    for source,tp,case in roles:
        if case.startswith('I'):W[source].add(int(case[1:]))
        if case in ('B','M'):
            o=len(pairs);v=2*o
            pairs.append((v,v+1));W[o]=set();kinds[v]='BP';kinds[v+1]='BP' if case=='B' else 'TP'
            links.append((tp,v))
            if case=='B':extra.append((tp,v))
    data=kinds,pairs,links,W,resources
    return data,old,baseline,extra


def allocation(totals):
    rng=random.Random(20261025047);records=[]
    specs=[x for q in range(1,4) for x in itertools.product(('B','M','H','I0','I1'),repeat=q)]
    specs += [tuple(rng.choice(('B','M','H','I0','I1')) for _ in range(4)) for _ in range(100)]
    for spec in specs:
        lengths=tuple(2+(i%3) for i in range(len(spec)));q=len(spec);N=sum(lengths)
        data,C,base,extra=decorated(lengths,spec)
        b=spec.count('B');m=spec.count('M');h=spec.count('H');u=sum(s.startswith('I') for s in spec)
        r=len({s for s in spec if s.startswith('I')})
        expected=N-q+b+r
        fixed=contract(data,C)
        for flow in (ordinary_flow,fork_flow):
            ans=flow(*fixed);assert ans['value']==expected
            totals['abstract_fixed_c_value_comparisons']+=1
        selected=C+base+extra
        assert len({v for e in selected for v in e})==2*len(selected)
        assert len(selected)==2*N-q+b
        assert evaluate(*data[:2],selected,*data[3:])['value']==expected
        totals['simultaneous_explicit_certificate_checks']+=1
        multiplicity=Counter(s for s in spec if s.startswith('I'))
        if max(multiplicity.values(),default=0)<=2:
            assert u<=2*r and q-b-r<=m+h+u//2
            totals['physical_multiplicity_bound_controls']+=1
        else:totals['abstract_high_multiplicity_excluded_from_geometric_bound']+=1
        if spec in [('I0','I0'),('B','B'),('I0','I1'),('M','M')]:
            records.append(dict(spec=spec,sources=N,kept_old_links=len(C),payment=expected,
                                remaining_deficit=N-expected,selected_links=len(selected)))
    assert any(r['spec']==('I0','I0') and r['remaining_deficit']==1 for r in records)
    return records


def necessary_hypotheses(totals):
    path=Path(__file__).parent/'fixtures/nonfrozen_nested_serial_fork.json'
    x=json.loads(path.read_text())
    cur=(*x['shape'],set(map(tuple,x['selected'])),[tuple(map(tuple,e)) for e in x['matching']])
    direct_check(*cur)
    data,_,_=whole_support_data(cur,whole_bands(cur))
    owner,aa,bb,mm=owner_data(*data[:2])
    mate={v:w for e in cur[3] for v,w in (e,e[::-1])}
    head,t,b,u,n=map(tuple,[x['head'],x['output'],x['beta_entry'],x['other_tp'],x['outer_selected']])
    assert owner[head]==owner[t] in mm and owner[b] in bb
    assert all(owner[tuple(a)] in aa for a in x['head_alphas'])
    assert len({owner[tuple(a)] for a in x['head_alphas']})==2
    assert data[0][t]==data[0][u]=='TP' and n in cur[2]
    a,bm=mate[t],mate[b]
    assert a==(9,9) and bm==(9,10)
    occupied=cur[2]|set(mate)
    assert set(neighbors(b))&occupied-{bm}=={t,u}
    assert set(neighbors(a))&occupied-{t}<={bm,(8,9)}
    ff,_=frozen_certificate(cur)
    assert b not in ff and a not in ff and len(ff)<len(mate)
    totals['nonfrozen_literal_hypothesis_controls']+=1
    # Different phases allow two different BP escapes into ONE whole beta.
    from check_whole_support_fork_normal_form import canonical
    kinds,pairs,_=canonical('AAB')
    links=[(pairs[0][0],pairs[2][0]),(pairs[1][0],pairs[2][1])]
    d=kinds,pairs,links,{i:set() for i in range(3)},set()
    assert len({v for u,v in links})==2 and fork_flow(*d)['value']==1
    totals['opposite_phase_single_beta_countercontrols']+=1
    return dict(shape=cur[:2],endpoints=len(mate),selected=len(cur[2]),frozen_endpoints=len(ff),
                strict_dependency_cycle=[a,b],scope='Feasible NONFROZEN. It is not a frozen serial embedding.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();totals=Counter()
    pp=physical(totals);aa=allocation(totals);control=necessary_hypotheses(totals)
    totals.setdefault('actual_complete_nested_motifs',0)
    totals.setdefault('actual_double_vertical_mixed_bp_escapes',0)
    out=dict(status='passed',counts=dict(totals),physical=pp,abstract=aa,nonfrozen_control=control,
        scope='Arbitrary-size geometric proof is written; local frozen fork/head controls and abstract simultaneous serial certificates are separate. No frozen serial-family embedding inferred.')
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='passed',counts=dict(totals)),indent=2))

if __name__=='__main__':main()
