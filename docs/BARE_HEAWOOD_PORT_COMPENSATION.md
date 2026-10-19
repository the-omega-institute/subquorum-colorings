# Bare Heawood ports: an additive compensation lemma

19 October 2026. This note gives a general local loss inequality and applies
it to an infinite periodic class of long-core selections. It also disproves
a proposed core-only certificate bound. The unrestricted conjecture
SF_2(L_k)=36k remains open for k>=8; no improved rectangular-grid bound
is claimed.

## Definitions and the local theorem

Use non-induced two-stars. A selection S forms a graph when every omitted
vertex has either two selected neighbors or a selected neighbor which has
a selected neighbor. Minimal always means inclusion-minimal.

Let H be the incidence graph of the Fano plane, choose an incident point
P and line L, and put B=H-PL. In an ambient simple graph G, assume B is
embedded with precisely its B-neighborhood at every non-port vertex.
Only P,L may have additional neighbors, including a restored edge PL.
Let S be any minimal forming selection of G and C=S intersect V(B).
A port v is **bare** if C misses {v} union N_B(v). Let t be the number
of bare ports, so t is zero, one or two.

**Theorem 1 (additive bare-port loss).** Under these hypotheses,

    |C|+t <= 8.

In particular, one bare port reduces the ambient eight-vertex block cap
to seven, and two bare ports reduce it to six. Counting two demands in
the same block therefore requires two losses, rather than using its
first loss twice. C need not form B and need not be minimal in B.

We use the robust-deletion definition and proved preservation/upward-closure
lemmas in [the exact Heawood composition proof](EXACT_CUBIC_COMPOSITION.md).
For clarity, a selected vertex v is robust in B if it is active, all its
selected neighbors have at least two selected neighbors, and each of its
omitted neighbors has either at least three selected neighbors or exactly
two with the other selected neighbor active. Such a non-port deletion
preserves formation in every allowed ambient graph. Indeed its neighbors
have internal replacement certificates, and any outside star using it as
a leaf can replace that leaf at its retained selected center. Additional
port edges do not invalidate these certificates.

The same proof shows that robustness persists when more vertices are
selected. We prove the stronger local statement that any C with |C|+t>8
has a robust non-port deletion. For t=0 this is the established dense
Fano lemma: every selection of at least nine vertices of B has one.
For t=1 it suffices to consider eight vertices avoiding the closed
B-neighborhood of the bare port. For t=2 it suffices to consider seven
vertices avoiding both such neighborhoods. A larger C contains the
appropriate smaller selection, and upward closure applies. These are
geometric arguments, not an enumeration premise.

## One bare port

By point-line duality suppose the bare port is P. Let A,B' be the two
lines through P other than L. The three vertices P,A,B' are omitted.
An eight-selection has p selected points and q selected lines, with
(p,q)=(3,5),(4,4),(5,3) or (6,2).

For non-port candidates we may check robustness in H. Deleting PL can
only change the selected degree of P (if L is selected): A,B' are
omitted, so P has no selected neighbor other than L in H. No non-port
candidate is adjacent to this changed vertex. No selected vertex loses
activity, since P is omitted. Thus every robust non-port candidate
described below is robust in B as well.

**Three selected points, five selected lines.** All allowed lines are
selected: L and the four lines not through P. Every selected point has
selected degree two or three. If the selected points are collinear,
every line meets them. Every selected non-port line is active and robust:
an omitted point has selected degree two or three and any other selected
line at it is active.

If the selected points are noncollinear, exactly one Fano line M misses
them. If M is omitted, all selected lines are active and the same argument
works. If M=L, the line L is selected but inactive: it is one of the
five allowed selected lines and has no selected point. Its intersections
with non-port lines are different from P and have three selected incident
lines in B. Deleting PL changes only P's degree, not theirs. Points
off L are not incident with M. Thus M
cannot block a non-port candidate. Finally, if M is a selected non-port
line, there are three active non-port line candidates. The inactive M
can block them only at its intersections with A or B', at most two
points/candidates; its intersection with L has selected degree three.
At least one of the three candidates is robust.

**Four selected points, four selected lines.** The omitted lines are
A,B' and a third line M. A selected point could be isolated only at a
common intersection of all three omitted lines; if they are concurrent,
that point is P and is omitted. Thus every selected point is active.
If the three omitted points are collinear, every other line has exactly
two selected points, and every selected point is robust. If the omitted
points a,b,c are noncollinear, their three pair lines have three distinct
third points x,y,z, all selected. The remaining selected point n lies
on no line with exactly one selected point. Its selected line neighbors
therefore retain another selected point, while each omitted incident
line of selected degree two has an active other selected point. Hence
n is robust. P is omitted, so these point candidates are non-ports.

**Five selected points, three selected lines.** Write the omitted points
as P,R. Three distinct Fano lines cover at least six points, so at most
one selected point W is isolated. The line PR is the unique line of
selected point-degree one; its third point Q is the only selected point
which can fail robustness because of such a line, whether PR is selected
or omitted. Other failures require an omitted line with two selected
points, one of which is the isolated W. Such a line must be WP or WR.
These give at most two further failing candidates. Thus at most
one isolate, Q, and two other points fail, at most four of the five
selected points. A robust point remains, and is a non-port.

**Six selected points, two selected lines.** Only P is an omitted point.
The selected lines cannot both pass through P, since A,B' are omitted.
Their intersection O is therefore selected. If its third line avoids
P, O is robust: its selected line neighbors have at least two selected
points and its omitted third line has three. Otherwise the third line
passes through P, so both selected lines avoid P. For any of their four
outer points Q, its selected line has three selected points. The omitted
line QP meets the other selected line in an active selected point, and
Q's other omitted line avoids P and has three selected points. Thus Q
is robust. Again these point candidates are non-ports.

All cases give the required deletion. The dual argument treats bare L.

## Two bare ports

Both closed port neighborhoods are omitted. They comprise the three
points of L and the three lines through P. The allowed vertices are
the four points outside L and the four lines not through P. A selection
of seven therefore has four points and three lines, or its dual.
Take the first case. Each selected point lies on two allowed lines,
at least one selected, so every selected point is active. Every line
incident with a selected point contains exactly two selected points.
Consequently every selected point is robust: a selected line neighbor
retains its other selected point, and an omitted line neighbor also
retains an active other selected point. All four are non-ports. This
proves the seven-vertex assertion and completes Theorem 1.

## Why a core-only certificate bound fails

Use the long core Q_k and attached graph L_k of
[the sharp omission note](LONG_CORE_SHARP_OMISSION.md). In each of k
blocks use local labels H0,...,H5,U0,...,U5,X0,...,X5,Y0,Y1.
H and X run cyclically; H_i--U_i--X_i; Y0 meets U0,U2,U4,
and Y1 meets U1,U3,U5. Delete X0X1,X2X3,X4X5 in every block.
Attach a fresh broken Heawood block at each deleted pair, using its two
ports, with P joined to the odd X and L to the even X. Thus L_k has
20k core vertices and 3k blocks of 14 vertices, in total 62k.

For even k=2r repeat the following two core patterns r times:

    E = {H0,U0,U2,U3,U4,U5,X0,X1,X3,X4,X5,Y0,Y1},
    O = {H1,H4,U0,U2,U3,U4,U5,X0,X1,X2,X4,X5}.

Their sizes are thirteen and twelve, so the core intersection C has
25r vertices. It forms Q_(2r), as follows directly from the local
neighborhoods. In an E block the omitted H1,...,H5 have active selected
neighbors H0,U2,U3,U4,U5 respectively; omitted U1 has the two selected
neighbors X1,Y1, and omitted X2 has U2,X1. In an O block every omitted
vertex already has two selected neighbors: for H0,H2,H3,H5 use
{H1,U0},{H1,U2},{H4,U3},{H4,U5}; for U1,X3,Y0,Y1 use
{H1,X1},{U3,X4},{U0,U2},{U3,U5}. This covers all omitted vertices
independently of the cyclic boundary. Every selected non-port has a private
internal clause except U4 in each O block. Recall

    A_u={u} union N(u),
    B_(u,v)={u} union (N(u) minus {v}) union (N(v) minus {u}).

The following table gives certificates, with all subscripts local to
the owner's block. Checking the displayed incidences proves the table
for every r, including wraparound; none requires a different neighboring
block value.

| Pattern | Owner | Private internal clause |
|---|---|---|
| E | H0 | A_(H1) |
| E | U0 | B_(H1,H0) |
| E | U2 | A_(H2) |
| E | U3 | A_(H3) |
| E | U4 | A_(H4) |
| E | U5 | A_(H5) |
| E | Y0 | B_(H2,U2) |
| E | Y1 | B_(U1,X1) |
| O | H1 | A_(H1) |
| O | H4 | B_(H3,U3) |
| O | U0 | B_(H0,H1) |
| O | U2 | B_(H2,H1) |
| O | U3 | A_(U3) |
| O | U5 | B_(Y1,U3) |

For O's remaining selected non-port U4, X4 is a selected port whose
sole selected core neighbor is U4. The boundary-certificate criterion
therefore holds for all selected non-ports, despite |C|=25r>24r=12k.
Deleting U4 preserves core formation, but loses activity at H4 and X4.
No other core deletion can preserve both internal clause hits and the
activity of selected ports: the table prevents the other non-port
deletions, and X4 prevents deleting U4 under that strengthened test.

For r=1 the selected global core labels are

    {0,7,10,12,14,15,16,17,18,20,21,22,23,
     24,25,27,28,29,30,31,32,34,35,36,37}.

Here H_i=i, U_i=12+i, X_i=24+i and Y_j=36+j.
The exceptional U10 is 22 and its port witness X10 is 34.
This refutes the proposed implication from the boundary-certificate
condition alone to |C|<=12k. It does not refute the full SF conjecture.

## Compensation for the whole periodic phase

First, Theorem 1 gives a uniform accounting inequality for every minimal
forming selection S of L_k, with no phase assumption. Put C_0=S intersect
V(Q_k), C_j=S intersect V(B_j), T=sum_j t_j and
delta_j=8-|C_j|. The ambient cap ensures delta_j>=0 and the theorem
strengthens this to delta_j>=t_j. Since all blocks are vertex-disjoint,

    |S| = 24k+|C_0|-sum_j delta_j <= 24k+|C_0|-T.

Thus |C_0|-12k<=T is a sufficient compensation rule for |S|<=36k.
It is not asserted for arbitrary core intersections. More generally,
other certified block losses can help through sum_j delta_j; failure
of the stronger bare-port rule would not by itself refute the target.
These identities sum each block once, including when both its ports
are bare.

**Theorem 2.** For any r>=1, let S be a minimal forming selection of
L_(2r) whose core intersection is precisely (EO)^r. Then

    |S| <= 72r = 36k.

Fix an O block and put u=U4, h=H4, x=X4. Let q be the external
Heawood port joined to x. We prove q is bare in that block.

Delete u. It becomes an outside vertex with two retained selected
neighbors h,x. The only retained selected vertices whose activity can
be lost are h,x: the third neighbor Y0 of u is omitted. The old omitted
neighbor Y0 of u still has its selected U0,U2. The omitted core
neighbors H3,H5 of h retain two selected core neighbors: H3 retains
H4,U3 and H5 retains H4,U5 (and possibly its selected cyclic neighbor).
The old omitted core neighbor X3 of x retains U3,X4. Thus all these
outside vertices still have two selected neighbors. Every other old
outside vertex keeps its selected neighbors and any selected center's
activity. The only vertex still needing examination is q.

If q is selected, x retains activity through q; hence all old stars
at q's neighbors persist as well and the deletion preserves formation.
If q is omitted and has a selected internal B-neighbor, it retains
two selected neighbors, that neighbor and x. In this case x has no
other omitted external neighbor and no other outside vertex can lose
its star. Deletion again preserves formation. Either case contradicts
minimality. Hence q is omitted and both its internal neighbors are
omitted, exactly the bare condition. No restriction on the selections
in other Heawood blocks was used.

There are r O blocks and their X4 vertices belong to r different
deleted X4X5 pairs, hence to r distinct attached Heawood blocks.
Writing C_j=S intersect V(B_j) and t_j for its bare-port count gives
sum_j t_j>=r. Theorem 1, applied separately to all 6r blocks, yields

    sum_j |C_j| + sum_j t_j <= 8(6r)=48r.

Since the core has 25r vertices, |S|<=25r+48r-r=72r, as claimed.
This also exhibits the general accounting safeguard: even if a later
construction places two forced demands in one block, Theorem 1 charges
its two bare ports separately. A single seven-vertex allowance cannot
be counted twice.

## Verification, scope and next question

**Subsequent result:** the sufficient rule |C_0|-12k<=T proposed here
fails even for actual ambient minimal sets with internally forming
cores. The [export and obstruction note](EXPORTED_BOUNDARY_AND_BARE_ONLY_OBSTRUCTION.md)
gives a general export theorem and an explicit infinite family with
core excess r and zero bare ports. The local additive loss theorem
and the phase theorem in this note remain valid. Further uniform
compensation must also account for non-bare block losses.

The [independent checker](../scripts/check_bare_heawood_ports.py) tests
all 16,384 selections of B. All 3,810 selections violating |C|+t<=8
have a robust non-port deletion; the respective counts for t=0,1,2
are 3,339,462,9. Among selections without such a deletion, the maximum
sizes are eight, seven and six. These are local robustness maxima,
not assertions that every extremal local set extends to an ambient
minimal set. The preceding proofs establish the general theorem.

The checker also checks twelve phase lengths r=1,...,12 and an explicit
62-vertex minimal selection in L_2 (order 124) having exactly the
25-vertex core phase above. It verifies formation and all 62 deletions
using literal non-induced stars. This makes the phase hypothesis
nonvacuous, without asserting that 62 is the largest set in that phase.
The exact selected vertices and block counts are retained in
[the control receipt](../output/bare-heawood-port-controls.json).
The explicit private-clause table and all affected core outside
neighborhoods after the exceptional deletion are checked at each of
the twelve lengths.

The accompanying [Lean module](../formal/StarForming/BareHeawoodPorts.lean) formalizes the general graph-level
single-obstruction inference used above and additive counting, with
the graph-to-obstruction hypotheses explicit. The Fano case proof,
periodic core certificate table and its graph-to-count instantiation
remain written mathematics; no complete Lean formalization of
Theorems 1 or 2 is claimed.

The unresolved step is a uniform charging theorem for **arbitrary**
core intersections, relating any excess above 12k to distinct bare
ports or another quantified block loss. Theorem 2 handles a specific
infinite obstruction class. It changes neither the known exact
beta_2(L_k)=33k+floor(k/2) nor the general SF interval. Finite SAT
timeouts and solver UNSAT reports without checked proof certificates
are not used as premises. The original live Oracle SF question did
not include the later private-clause or bare-port results. Bounded
[SAT discovery receipts](../output/bare-ports-sat-discovery.json) are
archived separately. Their optional discovery script requires
python-sat 1.9.dev16; the independent checker uses only the standard
library and does not invoke SAT.

Reproduction:

    python3 scripts/check_bare_heawood_ports.py --output output/bare-heawood-port-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit bare-ports --lean /path/to/lean-4.33.0 --output output/bare-ports-formal-check.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
