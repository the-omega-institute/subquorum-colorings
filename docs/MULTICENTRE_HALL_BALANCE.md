# One global HH budget for multiple TH centres

The canonical exterior Hall barrier forces compensation even when several
centres have TH paths. The same white HH source cannot be used separately
to excuse each centre's withdrawal from the tight exterior region. Counting
all terminal endpoints together removes the unrestricted two-centre branch
from the earlier lower bound, replacing it by a more restrictive branch.
On a fixed 18-by-18 positive-weight grid, the earlier bound is 2 whereas
the refined bound and the true optimum are K for every integer K>=3.

## 1. Hypotheses and notation

Use the complete hypotheses of Sections 1--2 of
`CANONICAL_HALL_BARRIER_AND_PAIR_COMPLETION.md`. Explicitly: M is an actual
grid matching on a finite even rectangle, P=V(M), Q=V minus P, and T is
a feasible white subset of Q (each selected vertex has at most one P
neighbour). The r>=1 internally M-covered cores P_i partition P and are
pairwise nonadjacent. There is one distinct black Q centre h_i per core,
whose P neighbours belong only to that core. Every centre has a TH relay.
The white HH sources W=Q_white minus T have size r-1. Their local relay
graph Gamma into the centres has a W-saturating matching. The direct
exterior graph has black side B=Q_black minus the centres, white side T,
white surplus one, and a black-saturating matching. No centre has a direct
T neighbour (H6). All actual weights are finite and nonnegative; the
implementation accepts exact nonnegative integers.

N denotes a full perfect auxiliary grid matching. A TH path has one
selected endpoint in T and one black Q endpoint; its actual M edges are
paid. HH paths and P-only components contribute zero to f(N). Let f* be
the minimum of f(N). The canonical exterior sets are E (exposable whites),
F=T minus E, and D={b in B: N_T(b) intersect E is empty}. The previously
proved canonical barrier lemma gives N_T(D)=F and |D|=|F|.

Let J be the set of centres which can be omitted by a W-saturating Gamma
matching; C_J={h_j:j in J} and C_-={h_i:i not in J}. Lambda is the generic
HH-source lower bound. Let sigma_j be the cheapest centre relay whose
source belongs to E, with infinity if none, and U_1=min_(j in J) sigma_j.
U_1 is the exact one-TH-centre/direct-other-TH normal form optimum, and
provides a full-N upper bound whenever finite. Empty minima mean infinity.

## 2. Exact conservation and single ownership

**Global balance lemma.** For any full N, orient each terminal path from
its white Q endpoint to its black Q endpoint, and let

* k be the number of centres whose paths start in T;
* a count paths whose sources lie in F and endpoints lie outside D;
* b count paths whose sources lie in E and endpoints lie in D;
* c count paths whose sources lie in W and endpoints lie in D.

Then

    k>=1,   a=b+c,   #HH paths ending outside centres=k-1,
    0<=c<=k-1.                                             (1)

If every TH-centre source is in F, then a>=k and b>=1.

Proof. The tagged union of M and N consists of alternating terminal
paths and P-only cycles (including doubled actual edges). Each terminal
path has one more N edge than M edges, so has odd length and opposite
coloured endpoints. Every Q vertex occurs on exactly one path. The paths
therefore define a bijection from white Q=T disjoint-union W to black Q.
There cannot be r HH centres with only r-1 white HH sources, so k>=1.

Of the |F| sources in F, exactly |F|-a end in D. The other sources
ending in D belong to E or W, giving

    |D|=|F|-a+b+c.

Since |D|=|F|, this proves a=b+c. Exactly r-k white HH sources end at
centres, leaving (r-1)-(r-k)=k-1 HH sources for ALL exterior endpoints.
The c paths ending in D are a subset of those paths, hence c<=k-1.
If every TH-centre source lies in F, their k distinct sources all end
outside D, so a>=k and b=a-c>=k-(k-1)=1. QED.

This is a global budget: the k-1 sources have one owner each among all
exterior HH paths. No per-centre or per-tight-subset reuse is permitted.
Every E-to-D path is nontrivial, since D has no direct neighbour in E.

**Eligible-centre lemma.** Every full N has a TH centre in C_J.

Proof. The HH-centre paths give a partial Gamma matching: their sources
and centres are distinct, and core separation forces their interiors
into the destination core (or the relay is direct). Augment this partial
matching until it saturates W, possible because Gamma admits such a
matching. Each augmenting path preserves every previously matched right
vertex and adds a new right vertex. The unique omitted centre is thus
one of the original TH centres. By definition it belongs to J. QED.

## 3. Refined lower bound without assuming J contains every centre

Retain F_H from the preceding note: the minimum total expense of two
vertex-disjoint nontrivial TH paths, sources one each in F,E and black
endpoints one each in C_J,D. Define F_X in exactly the same way but with
endpoints one each in C_J,C_-. In BOTH relaxations, source-to-endpoint
identity is unrestricted: crossed pairing is allowed. An empty group or
an infeasible physical pair gives infinity.

**Multicentre theorem.** Under Section 1's hypotheses,

    B_M=max{Lambda,min(U_1,F_H,F_X)} <= f*.                  (2)

It dominates the previous
B_H=max{Lambda,min(U_1,F_H,F_CC)}, where F_CC allowed any two centres.
In particular, when J contains every centre,

    max{Lambda,min(U_1,F_H)} <= f*.                        (3)

Proof. Fix a full N. If an eligible TH centre has source in E, its
individual path has expense at least sigma_j>=U_1.

Otherwise every eligible TH centre has source in F. At least one exists
by the eligible-centre lemma. If some ineligible TH centre has source
in E, choose its path and an eligible TH-centre path. They are distinct
components of the same M,N union, so are vertex-disjoint, with one source
in each F,E and endpoint in each C_J,C_-. H6 makes both paths nontrivial.
They witness f(N)>=F_X.

In the remaining case ALL TH-centre sources lie in F. The balance lemma
gives an E-to-D TH path, necessarily nontrivial. Choose it and an eligible
TH-centre path. They witness the F_H quotas and f(N)>=F_H.

The cases are exhaustive for arbitrary k, not merely k=1 or 2.
Nonnegative weights allow discarding the other TH expenses. Combining
the minimum of these three bounds with the already proved Lambda gives
(2). Every F_X-feasible pair is F_CC-feasible after forgetting its extra
quotas, so F_X>=F_CC, proving dominance. If C_- is empty, F_X=infinity,
giving (3). QED. The argument also covers infinite relaxation values.

F_X cannot be discarded merely because at least one eligible centre is
TH. At the abstract endpoint level take r=2, W={w}, Gamma={w--0}, so
J={1}; take F={f}, E={e}, D={d}, with sole exterior direct edge f--d.
The terminal bijection w->d, f->h_1, e->h_0 is consistent with the
HH-centre Gamma restriction, has k=2, a=c=1, b=0, and belongs to the
F_X case, not the U_1 or F_H cases used above. This abstract countermodel
alone refutes an endpoint-only proof that omits the case. Section 6 gives
a separate realizable grid family refuting inequality (3) without J=I.

For a physical proper-J control, place canonical 5-by-5 cores at (0,0)
and (0,8) in a 6-by-14 board. Remove their centres, use their canonical
M, set W={(5,2)}, and let T be all other white Q. Then Gamma has only
(5,2)--core0, J={core1}, F={(5,0),(5,4)}. The checker supplies a full
attaining matching and finite F_X=3 at unit weights. This tests proper-J
handling, not necessity of F_X for a strict grid improvement.

## 4. Fixed geometry with an arbitrarily large improvement over B_H

Use the CANONICAL M from `branched_source_obstruction.branched_family()`:
18-by-18 board, five 5-by-5 squares with origins

    (6,6), (2,0), (0,10), (10,12), (12,2),

and centres origin+(2,2). Inside each square, M pairs local rows 0--1
and 3--4 vertically in every column, and pairs middle-row columns 0--1
and 3--4 horizontally. The r-1 white HH sources are

    W={(5,10),(6,5),(10,11),(11,6)}.

All other white Q vertices are selected. Gamma is the five-vertex star
incidence graph, hence J=I. The canonical F,D are the white and black
vertices of the region

    ([0,1] x [0,9]) union ([2,5] x [5,9]),

with 20 vertices of each colour. The preceding note supplies the exact
neighbour equality and direct exterior matching/exposure certificates.

Give ONLY the following two actual edges weight one:

    e_N={(2,2),(3,2)},   e_C={(6,8),(7,8)};

all other actual edges have weight integer K>=3. These are a different
M and weight assignment from the preceding three-cheap-edge example.
The two paths

    A: (1,2),(2,2),(3,2),(4,2),
    B: (5,8),(6,8),(7,8),(8,8)

are disjoint cheap centre paths, both with sources in F. Thus F_CC=2,
since every nontrivial path costs at least one. The centre minimum fees
are rho=(1,1,K,K,K), so Lambda=1.

For the first actual edge of a nontrivial path from E to be cheap,
its source must be a white Q neighbour of cheap black endpoint (2,2)
or (6,8). The ONLY such selected neighbours are (1,2) and (5,8),
respectively; both belong to F. All other neighbours of these black
endpoints are in P. Consequently every nontrivial E-source path has
expense at least K, already at its first actual edge. In particular
U_1>=K and F_H>=K+1, regardless of crossed pairing.

The central E-source path

    L: (8,5),(8,6),(8,7),(8,8)

has one K edge and, by the normal-form construction, extends to a full N
with expense K: assign each star source to its own arm, double unused M,
and use the direct exterior matching exposing (8,5). The exact finite
edge list of this N is provided as a witness, not defined by enumeration.
It uses no cheap paid edge and exactly one other paid actual edge; its
symbolic expense is therefore K for every K>=3. Hence U_1=K.

For F_H, path A and the disjoint exterior compensation path

    R: (7,4),(6,4),(5,4),(5,5)

have sources in F,E, endpoints in C_J,D, and expense 1+K. Thus F_H=K+1.
Since C_- is empty, F_X=infinity. Equations (2)--(3) and attainment give

    B_H=2,   B_M=f*=U_1=K,   F_H=K+1       (K>=3).        (4)

The additive improvement K-2 and ratio K/2 over B_H are unbounded on
the same footprint and M. This improves a weighted lower bound; it does
not supply a universal unit-weight improvement of the colouring 5/6 bound.

## 5. A full two-centre witness with sharp HH use

Fix all three paths A,B,R just displayed. The fixed-path extension
criterion from the preceding note supplies a full N with all other TH
paths direct. It has exactly two TH centres and symbolic fee K+2.
Its exact terminal counts are

    k=2,   a=2,   b=1,   c=1,   exterior HH count=1=k-1.

Thus the one exterior HH source really can compensate for one of the
two withdrawals from F, yet one E-to-D TH path remains necessary. The
full matching and that HH path are saved as coordinate certificates.
This N is a sharp count witness, not an optimum claim (the optimum is K).

## 6. The mixed-centre branch is necessary: an actual all-K grid obstruction

Use a 12-by-14 board with two canonical 5-by-5 cores at origins (0,6)
and (6,0), centres h_0=(2,8), h_1=(8,2), and canonical M as defined in
Section 4. Set W={(0,5)} and select every other white Q vertex. The
only Gamma incidence is (0,5)--core0: the white hole touches core0 only,
and the relay

    (0,5),(0,6),(1,6),(2,6),(2,7),(2,8)

reaches its centre. Hence J={1}, so h_0 is ineligible and h_1 eligible.
Both centres have only P neighbours and T is feasible. The canonical
balanced tight region is

    F = white vertices of [0,5]^2 minus {(0,5)},
    D = black vertices of [0,5]^2 minus {(5,5)},

each of size 17. Direct inspection gives N_T(D)=F. The certificate
contains a direct exterior matching exposing (8,5); independently testing
every exterior deletion gives E=T minus F, not just a subset thereof.
These fixed coordinate facts establish all Section 1 assumptions.

Give only e_1={(6,2),(7,2)} and e_0={(3,8),(4,8)} weight one, and every
other M edge integer K>=3. The following disjoint centre paths are cheap:

    A_1: (5,2),(6,2),(7,2),(8,2),       F -> eligible h_1,
    A_0: (5,8),(4,8),(3,8),(2,8),       E -> ineligible h_0.

An explicit complete N fixes both, uses the direct HH edge
(0,5)--(0,4), and has every other TH path direct. Its only paid actual
edges are e_1,e_0, so its fee is 2 for EVERY K. Its global terminal
balance is a=c=1, b=0, k=2: the unique HH source compensates the one F
withdrawal and no E-to-D TH path is forced. Thus F_X=2 (the two paths
attain it and each nontrivial path costs at least one).

Any all-cheap nontrivial path from E must first use e_0: the only selected
neighbour of the other cheap black endpoint (6,2) is (5,2) in F. After
e_0 its white endpoint (3,8) has only one black Q neighbour, namely
ineligible h_0. Reaching any other endpoint requires an additional,
K-weight actual edge. The two cheap edges lie in separate cores, so
cannot form a longer cheap-only alternating path. Consequently every
E-source nontrivial path ending in C_J or D costs at least K.

It follows that U_1>=K and F_H>=K+1, even when crossed pairings are
allowed. The eligible centre relay

    (8,5),(8,4),(8,3),(8,2)

has one K edge and is completed by the normal-form construction, with
only one expensive paid actual edge. Thus U_1=K. The disjoint paths A_1
and

    (5,6),(4,6),(3,6),(3,5)

attain F_H=K+1, since the second starts in E and ends in D. Therefore

    Lambda=1,  F_X=f*=B_M=2,  U_1=K,  F_H=K+1.            (5)

The true optimum follows from (2) and the explicit N of fee 2.
Deleting F_X would instead assert the false lower bound K<=2 for K>=3.
This refutes the unconditional version of (3), not the main theorem (2),
not the J=I corollary, and not the colouring 5/6 target. It also shows
why merely finding one eligible TH centre is insufficient: another,
ineligible TH centre can start outside F and release a source into D.

The full matching lists, symbolic paid vectors (2,0) and (0,1), tight
sets and HH edge are explicit checkable certificates. Their discovery
used finite search; the first-edge argument and fixed certificates prove
all K, rather than extrapolating from the tested samples.

## 7. Algorithms and validation boundary

F_X uses the preceding capacity-one physical grid network, with source
collectors F,E and sink collectors C_J,C_-. There is one actual M arc
black-to-white with cost w and capacity one, non-M arcs white-to-black,
and direct T-to-black-Q arcs removed. Two integral flow units enforce
the quotas without copying any actual edge or imposing labelled demands.
The accepted flow/path correspondence and residual optimality/cut
certificates apply unchanged. Computing the refined bound retains
O(v^2) arithmetic time and O(v) stored words; integer bit costs are extra.

An attaining normal form, or a minimum F_H/F_X pair at the bound which
passes the fixed-path completion test, certifies an optimum. Failure of
one returned pair is not global infeasibility; the method is a sufficient
certificate procedure, not a general exact optimizer.

The checker exhausts small source graphs and partial centre assignments
for the eligible-centre lemma, independent abstract terminal bijections
for (1) and the case classification, and full small-grid matchings for
the bound. It rechecks all 48 original changed-M controls and includes a
physical proper-J example. Explicit complete-N witnesses are independently
rescored with the older tagged decomposition, including zero costs and
401-digit integers. The all-K proof above uses first-edge restrictions
and fixed symbolic witnesses; finite samples do not replace it.

No new Lean verification, universal 5/6 improvement, manuscript revision,
or email operation is claimed. The next research step is to couple
multiple tight regions without counting their overlapping entrance paths
more than once, and to find unit-weight structural gains.

Local validation commands:

    python3 develop/check_multicentre_hall_balance.py
    python3 develop/check_multicentre_coordinates.py

They passed all 4,165 small source graphs and 69,941 partial assignments;
28,369 endpoint bijections, including 4,938 mixed-centre cases; 216 full
small-grid matching/weight comparisons; the 48 original changed-M exact
controls; and the proper-J physical example with 320 independently
enumerated paths and 1,914 qualifying pairs. The weight controls include
zero costs, and the five K samples include a 401-digit K. The standalone audit imports
no project module and independently checks all 98 exterior deletions in
the main family, 17 in the first proper-J family and 59 in the new
proper-J counterexample, all complete-N symbolic expense vectors, and
both cheap-only endpoint obstructions. The actual counterexample is also
tested at five K values including a 401-digit integer. Results and exact
scope are recorded in the three `output/multicentre-*.json` reports.
