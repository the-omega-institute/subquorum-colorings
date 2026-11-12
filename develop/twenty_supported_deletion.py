"""The explicit local case choices in the supported-deletion proof for F20."""
from supported_local_deletion import supported

HELPERS=set(range(4));WITNESSES=set(range(4,12))
A={12,13,16,19};B={14,15,17,18};PORTS={4,12}
MATE={4:11,11:4,5:9,9:5,6:8,8:6,7:10,10:7}


def ready_owners(g,C):
    ready=set()
    for square in (A,B):
        if len(C&square)==4:ready|=square-PORTS
        if len(C&square)==3:
            ready|={v for v in C&square-PORTS if len(g[v]&C&square)==1}
    return ready


def thirteen_choice(g,C):
    """Return a supported vertex and the proof's branch for a thirteen-set."""
    C=set(C)
    if len(C)!=13 or not C<=set(range(20)):
        raise ValueError('Use a thirteen-subset of F20')
    for v in sorted(ready_owners(g,C)):
        if supported(g,C,PORTS,v):return v,'ready-owner'
    for v in sorted(C&HELPERS):
        if supported(g,C,PORTS,v):return v,'helper'
    h=len(C&HELPERS);k=len(C&(A|B));D=WITNESSES-C
    if h==2:
        assert k==5 and D=={8,9} and C&HELPERS=={1,2} and 14 not in C
        v=18 if 18 in C else 17
    elif h==3 and k==4:
        j=next(iter(HELPERS-C))
        if j==0:
            if 17 in C:v=min(C&B-{17})
            elif C&A=={12,13}:v=13
            else:v=5
        elif j==1:v=8 if 14 in C else 10
        elif j==2:v=6 if 16 in C else 7 if 18 in C else 9
        else:v=5 if 17 in C else 7
    elif h==3 and k==5:
        j=next(iter(HELPERS-C))
        if j==1:
            assert D=={4,5,9} and len(C&A)==3
            v=14 if C&B=={14,15} else 6
        else:
            assert j==0
            if 16 not in C:v=5
            elif D=={7,8,9}:v=5
            else:v=18 if 18 in C else 17
    elif h==4 and k==5:
        W=C&WITNESSES
        assert W in ({6,7,10,11},{6,7,8,11})
        v=7 if 10 in W else 6
    elif h==4 and k==4:
        choices={frozenset(d):v for d,v in (
            ({4,5,8},7),({4,5,10},6),({6,7,11},9),({6,7,9},11),
            ({7,8,9},5),({4,8,9},7),({6,10,11},8),({5,10,11},6))}
        v=choices[frozenset(D)]
    else:
        raise AssertionError(('Uncovered proof case',h,k,sorted(C)))
    assert supported(g,C,PORTS,v)
    return v,f'finish-h{h}-k{k}'


def choose(g,C):
    """Use upward closure to handle every selected intersection of size>=13."""
    C=set(C)
    if len(C)<13 or not C<=set(range(20)):
        raise ValueError('Use a subset of F20 of size at least thirteen')
    v,branch=thirteen_choice(g,set(sorted(C)[:13]))
    assert supported(g,C,PORTS,v)
    return v,branch
