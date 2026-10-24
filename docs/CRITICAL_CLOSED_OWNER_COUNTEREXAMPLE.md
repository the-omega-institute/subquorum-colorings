# A critical second point can enter a closed phase01 owner

20 October 2026. The blanket extension of closed-owner exclusion from first
and LONG second points to CRITICAL second points is false. The following
six complete original U sources give a feasible finite configuration in which
a critical second point is an original outer bar corner of a phase01 owner
on a closed neutral component. The receiver is that owner's original full
bar tile. This refutes the proposed exclusion rule, not the coefficient-one
allocation or rectangular-grid equality.

## 1. Complete coordinate certificate

Coordinates are integer pairs (row,column) in the 20 by 30 grid. Its fixed
tiles have origins (2i,2j). A canonical U(w,l,r), with even w>=6 and l,r>=4,
has matching edges

    (0,1+2i)--(0,2+2i),           0<=i<w/2;
    (1,2+2i)--(1,3+2i),          0<=i<w/2-1;
    (1+2i,1)--(2+2i,1),          0<=i<l/2;
    (1+2i,w)--(2+2i,w),          0<=i<r/2.

Its original support consists of (0,0), (0,w+1), (l+1,1), (r+1,w), together
with (j,0) for even 2<=j<=l and (j,2) for odd 2<=j<=l, and (j,w+1) for even
2<=j<=r and (j,w-1) for odd 2<=j<=r. Original endpoints are precisely the
matching endpoints. Use these six affine images:

| Index | Name | (w,l,r) | Image of (row,column) | Phase | Original charge |
|---|---|---|---|---|---|
| 0 | O | (26,12,4) | (row,column+1) | 01 | -1 |
| 1 | F | (10,4,4) | (column+1,row+3) | 11 | -9 |
| 2 | B | (6,4,4) | (column+11,7-row) | 01 | -1 |
| 3 | H | (6,4,4) | (8-row,column+8) | 10 | -5 |
| 4 | G | (8,6,6) | (row+2,column+7) | 01 | -1 |
| 5 | E | (10,4,4) | (column+1,20-row) | 11 | -9 |

Let M be the union of all six matchings, P its endpoint set, and T the union
of all six original supports with P removed. All 90 edges have disjoint
endpoints, so |P|=180. There are 38 retained supports. Every point lies in
the stated grid, T is disjoint from P, and each t in T has at most one
neighbor in P union T. In particular, no mandatory original support is
discarded unless it is occupied by an original endpoint.

The last source E matters: it consumes G's other outer support (2,16),
which otherwise has two persistent occupied neighbors. The five-source
subconfiguration is not a feasible certificate. The six-source certificate
above retains all required supports and is feasible.

## 2. The actual critical exit

O's left terminal is p=(12,2); B has terminal q=(12,3). Their receiving tile
of origin (12,2) has final profile 2P1T. The first forced position is

    z=(11,3).

It belongs to the original supports of both O and B and is occupied by F's
canonical bar endpoint (0,10). The receiving tile of z has origin (10,2)
and is full, with an O pair and an F pair. The active leg height is a=12
and F's width is v=10, so this is the critical case a=v+2, not a long exit.
F has an original 3P0T tile of origin (10,4), confirming its actual phase11
profile in the fixed partition.

F's opposite leg has height h=4. Its terminal is (2,7) and its outward
terminal support is

    t=(2,8).

The O endpoint (1,8) and the F endpoint (2,7) are two distinct neighbors of
t. Support retention and the selected-degree condition therefore force t
into P. The certificate occupies t using G's canonical endpoint (0,1).
This is an outer bar corner, not either terminal. The tile of origin (2,8)
is already G's original full 4P0T bar tile.

## 3. G really lies on a closed neutral component

G's two terminals are (8,8) and (8,15). H's two phase10 bar ports are (8,9)
and (8,14). The actual tiles of origins (8,8) and (8,14) both have final
profile 2P1T, with endpoint pairs respectively

    {(8,8),(8,9)},    {(8,14),(8,15)}.

Each original owner contributes a singleton 1P1T profile to each of these
tiles. Both G ports are matched to H, and both H ports to G. Thus {G,H}
is a closed component of the specified neutral U-port multigraph: two
distinct physical contacts form the two parallel edges. Parallel contacts
are legitimate in this graph, whose edges are contacts rather than unordered
owner pairs. No other port can attach to these already matched ports.

Consequently t belongs to the ORIGINAL endpoint set of a phase01 owner
on a closed neutral component. This is exactly the proposed exclusion's
negation. The coordinate construction, rather than a finite search bound,
establishes the counterexample.

## 4. What fails, and what survives

The correct [first/LONG theorem](FULL_FIRST_AND_LONG_RECEIVER_INJECTION.md)
remains intact. There its regular receiver has an active original phase01
pair; any phase01 owner of the forced point must be a terminal. That role
restriction excludes owners with neutral closed terminal tiles. At the
critical point above there is no such regular-pair stencil: G can own an
outer full-bar corner without any terminal collision. The long hypothesis
cannot be removed from that proof.

This example does not show that a critical point equals the OTHER extra
corner of a first/long full receiver. It does not disprove critical point
injection, first/long receiver injection, the shared H inequality, or the
same-component AA deduction. Here A=0, H=32 and R=18, so this is not AA.
There is no closed01--closed01 contact in this fixture. The full target
coefficient-one/grid theorem remains OPEN.

The objective is |M|+|T|=128 versus half-area 300, leaving slack 172. The
existing exact census gives

    U0=4, Z0=0, H=32, A=0,  2R=A+U0+Z0+H=36.

Thus a return into a closed owner alone supplies no target-inequality
counterexample. It prevents treating all critical positions as fresh external
payments. A valid continuation argument must permit entry through a closed
owner's full bar and reserve that physical resource only once. Whether a
more restrictive exclusion holds within a nonexceptional AA component is
not decided by this configuration.

## 5. Verification and coverage

The subsequent [critical return theorem](CRITICAL_PHASE01_BAR_RETURNS.md)
identifies every phase01 return as an original outer bar corner, with two
distinct physical slots per original owner. A complete seven-source family
uses BOTH slots of the same closed owner for every even ambient width
W>=20 in its stated parameterization. The correct replacement permits
returning owners and tracks their labelled slots; it does not restore the
false blanket exclusion refuted here.

[`check_critical_closed_owner_counterexample.py`](../develop/check_critical_closed_owner_counterexample.py)
reconstructs the six existing source constructors and independently compares
them to the explicit matching/support formulas above. It checks feasibility,
all contact and owner coordinates, the closed port component and the existing
exact reserve/joint census. Eight signed coordinate isometries, with parity
offsets preserving the physical tile partition and even containment shifts,
all pass. Run

    python3 develop/check_critical_closed_owner_counterexample.py --output output/critical-closed-owner-counterexample.json

[`CriticalClosedOwnerCounterexample.lean`](../formal/SubQuorum/CriticalClosedOwnerCounterexample.lean)
constructs M, P and T directly from the six specifications. Six concrete
theorems check legal dimensions/charges, full feasibility, cardinalities,
first contact and phase11 ownership, the critical full-bar corner, and both
actual G/H neutral contacts. The first three use no axioms; the last three
use only propext. No native_decide, sorry or additional axiom occurs.
The closed-graph and critical-geometry deductions from these coordinates
are written in Sections 2--3. This is not a general formalization of the
complete neutral-port graph or unrestricted allocation.

See [Python receipt](../output/critical-closed-owner-counterexample.json) and
[Lean receipt](../output/critical-closed-owner-formal-check.json). Complete
critical coverage is now positive. The older first/long control batch still
has zero critical cases; this additional fixture does not change that batch.
Complete long-second, closed01--closed01 contact and AA coverage remain zero
in these new controls. The prior independent Oracle ACCEPT predates and does
not cover this new certificate.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
