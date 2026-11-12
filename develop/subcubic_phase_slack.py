"""Exact owner-class slack and strengthened physical gap certificates."""
from fractions import Fraction
from subcubic_phase_pairing import template_certificates as baseline_template
from subcubic_phase_pairing import full_certificate as baseline_full


def owner_slack(m,pairing):
    ordinary=distinguished=0;rows=[]
    for key,c in pairing['classes'].items():
        nonsquare=c.get('non_square_mono',False)
        good=not nonsquare and (len(c['remaining'])==2 if c['distinguished'] else not c['remaining'])
        if not good:
            if c['distinguished']:distinguished+=1
            else:ordinary+=1
        margin=c['budget']-c['loss']
        threshold=Fraction(0) if good else Fraction(1,6) if c['distinguished'] else Fraction(1,12)
        assert margin>=threshold
        rows.append(dict(key=key,good=good,distinguished=c['distinguished'],margin=margin,threshold=threshold))
    sigma=Fraction(len(m['I']),6)-Fraction(pairing['odd'],3)-pairing['rho']
    assert sigma==sum(r['margin'] for r in rows)
    assert (sigma==0)==(ordinary+distinguished==0)
    assert 12*sigma>=ordinary+2*distinguished
    return dict(sigma=sigma,ordinary_violations=ordinary,distinguished_violations=distinguished,classes=rows)


def template_certificate(m):
    D,data=baseline_template(m);slack=owner_slack(m,data['pairing'])
    assert 5*len(D)>=13*len(m['I'])+3*slack['sigma']
    return D,dict(baseline=data,slack=slack)


def full_certificate(g,S,colour,beta):
    D,data=baseline_full(g,S,colour,beta);slack=owner_slack(data['template'],data['phase']['pairing'])
    sigma=slack['sigma'];terms=list(data['terms']);terms[0]-=3*sigma
    assert all(t>=0 for t in terms)
    assert sum(terms)==8*len(g)-81*(len(S)-beta)-3*sigma
    return D,dict(baseline=data,slack=slack,terms=terms)
