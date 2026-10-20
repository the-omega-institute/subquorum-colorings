# Permanent corridors and a single-use strip compensation theorem

21 October 2026. Work in the complete original U/rotor model of
[source retention](SOURCE_RETENTION_HORN_CLOSURE.md) and the
[exact geometric reserve](EXACT_GEOMETRIC_EVENT_RESERVE.md). All widths are
even and at least six; both leg lengths are independently even and at least
four. Endpoints and matching edges retain their original owners. Every
unconsumed original support remains selected, with occupied degree one.
All tiles below are the fixed aligned two-by-two physical tiles. A chart
is permitted only when it preserves that partition.

We prove permanent mixed caps and complete upper strips, with a separate
lower-strip enclosure theorem. Their capacities are disjoint from the
previous m8 receipts. Consequently every legal component extension satisfies

    L <= R(I)-p-u-ceil((A(I)+m8(I)+z)/2).                 (1)

Here L is the SUM of all negative component reserve increments, z counts
distinct certified caps, u counts upper-strip pairs ONCE per original strip
owner, and p counts distinct certified lower pairs. This is a conditional
compensation theorem with an explicit coverage condition, not the full
allocation theorem. The unrestricted target mu=N+R-G>=0 and rectangular-grid
triple equality remain OPEN. N counts positive sources, not all owners.

## 1. A corridor that is empty or filled from its first point

Suppose a complete feasible family contains original owners

    B=U(d,a,e),  B(r,c)=(r+2,c+1),
    D=U(v,b,f),  D(r,c)=(r+5,c+2).                      (2)

In this chart B and D are negative sources. Endpoint disjointness gives
v<=d-2: otherwise D's row-five bar would contain B's far-leg endpoint
(5,d+1). Define the corridor

    C={(4,c): 3<=c<=v+2},   z0=(4,3).

**Corridor theorem.** Either C is entirely unoccupied, or a single original
negative U fills C with endpoints. In the second case its form is

    F=U(s,h,k),  F(r,c)=(c+3,h+3-r),
    v+2<=h<=d-4.                                       (3)

These are necessary conditions; no complete realization of the second
alternative is asserted here.

Every corridor point has fixed endpoint neighbors immediately north in B
and south in D, so none can remain selected. If any is an endpoint, choose
the leftmost. If it lies strictly to the right of z0, its north and south
neighbors belong to other owners, and its west neighbor is not an endpoint.
Its only possible own endpoint neighbor is east. The original U/rotor
catalogue then makes it a U terminal or rotor tip. In either case its
original mandatory endcap support is immediately west. That support cannot
remain selected, because it also has the fixed north and south neighbors.
It must be an endpoint, contradicting leftmost choice. Thus filling must
start at z0.

At z0 the fixed north (3,3) and west (4,2) neighbors belong to B, while
south (5,3) belongs to D. Again only an east-pointing U terminal or rotor
tip is possible. For the canonical rotor endpoint set

    {(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)},

the two east-tip footprints at z0 are represented by (r,c)->(r+1,c+2)
and (r,c)->(7-r,c+2). The first contains B's endpoint (3,4); the second
contains B's endpoint (3,5). Both are excluded.

For a U terminal let h be its incident leg. Its stem occupies row four
from column three through h+3. Avoiding B(4,d+1) gives h+3<d+1, or
h<=d-4 by evenness. If its bar points north, its two bar columns h+2,h+3
cross B's row-three bar; these columns lie inside that bar by the preceding
bound. Its bar must therefore point south, giving exactly F in (3).
On row five its bar columns h+2,h+3 must avoid D's bar columns 3..v+2.
Thus h>v and evenness gives h>=v+2. Its incident stem consequently fills
every point of C. This proves the theorem, without restricting other
sources or their dimensions.

**Protected-width corollary.** If v>=d-4, the corridor is permanently
unoccupied in every complete extension retaining B and D. Indeed (3)
would require v+2<=d-4, a contradiction. Together with v<=d-2, the
protected width cases are v=d-4 and v=d-2 when those widths are allowed.

## 2. Actual persistent capacities

Under the protected-width hypothesis, the cap and upper strip are

    T={4,5} x {2,3},
    Q_j={4,5} x {4+2j,5+2j},  0<=j<=v/2-2.

Their exact permanent profiles are

    T:    B  empty          Q_j:  empty empty
          B  D                     D     D

Empty means unoccupied, including absence of selected supports. Thus T is
one mixed 3P0T tile and contributes one L3 unit. Each Q_j is an original
irregular 2P0T pair and contributes two units through 2L2bar. There are
v/2-1 such pair tiles. No endpoint in these tiles is an original terminal:
B contributes its first internal leg pair, D an upper corner or internal
upper-bar pair.

One important occurrence is the full-bar demand route: B consumes the
canonical positive gate (3,2). If a=4 and B's terminal tile {6,7}x{2,3}
is full, B's support (5,3) has its original anchor (5,2) and another
occupied neighbor (6,3), so it must be consumed. The theorem applies when
its actual consumer is the D in (2) with protected width. The theorem
itself does not require a=4, an unactivated positive producer, or this
particular forcing route.

## 3. A separate lower-strip enclosure

Suppose a complete family contains

    D0=U(d,4,e),  D0(r,c)=(r+3,c+2),
    E=U(W,b,f),   E(r,c)=(9-r,c+1),
    m=min(d+2,W+1).                                    (4)

The boundary of [4,8]x[3,m] consists entirely of original endpoints:
its top is D0's lower bar, bottom is E's upper bar, left is D0's incident
leg, and right is the far leg of the owner determining m. D0 and E have
no endpoints in its strict interior, which has only three rows.

Any foreign owner with an interior endpoint would have all its endpoints
inside: its endpoint graph is connected by lattice edges and cannot cross
the boundary without sharing an original endpoint. Every allowed U has
extent at least five rows in any orientation, and every rotor has extent
four. Neither fits in three rows. This excludes foreign interior endpoints
in any complete extension.

The tiles {4,5}x{4+2j,5+2j} with 5+2j<=m-1 therefore have D0's lower
bar pair on top and no endpoint below. A bottom point cannot be selected:
its adjacent D0 endpoint would have to be its own original anchor, but
D0 has no support at that point. The exact profile is original 2P0T,
contributing two units per tile. Their number is

    min(d/2-1,W/2-2).                                  (5)

Define p as the number of DISTINCT physical tiles certified by all such
enclosures, not the sum over potentially repeated descriptions.

## 4. Nonreuse, including the previous protected receipts

Define z as the number of distinct cap tiles in Section 2. If caps are
assigned to actual marked-side claims, the assignment is injective. The
unique two-endpoint owner of a cap identifies B; its first internal leg
pair fixes the incident leg and the bar end. The gate is then B's original
support (3,2). Of its two external anchor positions, (4,2) already belongs
to B, so a positive producer must own (3,1). Unique endpoint ownership and
the canonical-gate uniqueness theorem identify that original positive side.
Thus distinct marked-side claims cannot receive the same cap.

For each distinct D owner appearing in a certified cap, count its ENTIRE
upper strip once. Let this set of owners be Dset, and put

    u=sum_{D in Dset}(v_D/2-1).

Each D has at most two cap positions, at its two intrinsic upper corners.
The strips described from the opposite corners are the SAME strip, not
two resources. Different owners cannot share a pair tile, because the
two endpoints have a unique original owner. Since v_D>=6,

    z<=2|Dset|<=u.                                     (6)

In particular one can assign each corner its adjacent first pair without
collision: the opposite first pairs have columns {4,5} and {v,v+1}, which
are distinct at v>=6. Counting all u pairs gives the stronger bound (1).

Upper and lower pairs are disjoint. For the same original owner they use
different intrinsic bar rows; different owners cannot share endpoints.
Caps have three endpoints, pairs have two, so those classes are disjoint.

For completeness none of these tiles is a positive canonical gate tile.
For an upper or lower pair, every potential external gate anchor at an
occupied corner is another endpoint of its negative owner; a blank corner
cannot be an original mandatory support. In cap coordinates all eight
oriented gate choices are excluded as follows:

| Gate point | External anchor | Reason |
|---|---|---|
| (4,3) | Either | Permanently unoccupied |
| (4,2) | (3,2) | Negative B owns the anchor |
| (4,2) | (4,1) | Positive frame (r,c)->(7-r,c) meets B(6,2) |
| (5,2) | (6,2) | Negative B owns the anchor |
| (5,2) | (5,1) | Positive frame (r,c)->(r+2,c) meets B(2,2) |
| (5,3) | (5,4) or (6,3) | Negative D owns both anchors |

The m8 receipts of
[the earlier theorem](PAIR_GATE_TRANSFERS_AND_PROTECTED_DEFECTS.md) are
also disjoint from these capacities. An m8 receipt is either a single-owner
original U triple, or a mixed triple with an original irregular 2P0T pair
and a terminal singleton. A new cap is mixed and has a REGULAR 2P1T pair:
B's original support at (5,3) is consumed by D. Thus a cap cannot be an
m8 receipt, even if its two-owner split is 2+1. New pairs have only two
endpoints and cannot be any triple receipt. In addition, new caps and
pairs contain no original terminal. This supplies an ownership/profile
proof of disjointness, rather than inferring it from different labels.

## 5. Single-use compensation across arbitrary added components

Let I be any complete feasible retained family and J a complete extension.
Take the caps, distinct strip owners, and distinct lower pairs already
certified in I. Their profiles persist in EVERY complete intermediate
extension F. Previous activations and m8 receipts persist as well.
The exact reserve identity and Section 4 therefore give

    2R(F)>=A(I)+m8(I)+z+2u+2p,
    R(F)>=p+u+ceil((A(I)+m8(I)+z)/2).                  (7)

Let the added-owner groups be components of the graph of adjacent added
endpoints. By the established component-subunion theorem every union of
these groups together with I is complete feasible, and R is affine on
this Boolean cube. Write delta_j for the group's reserve increment and
L=sum_j max(0,-delta_j). Take ONE intermediate family F containing exactly
the groups with delta_j<0. Then R(F)=R(I)-L. Applying (7) to this ONE
family proves (1). No per-component copy of R(I), activation or strip
is used. The result remains meaningful when there are no added groups.

If I is a canonical demand hull H preserving all positive owners and all
marked sides of J, a sufficient coverage condition is

    p+u+ceil((A(H)+m8(H)+z)/2)>=G-N.                  (8)

Then L<=R(H)-(G-N)=mu(H), so every component subextension has nonnegative
mu, including H=J. Through the established sigma>=mu inequality this gives
|T|+|M|<=mn/2 for covered complete-source configurations, an improvement
of |M|/6 over the existing 5/6 matching coefficient on those configurations.
There is no universal coverage proof for (8), nor an arbitrary-grid
decomposition theorem here.

## 6. An all-parameter realization and a legal failure of lower persistence

For every even d>=6, g>=4 take

    A=U(d+4,g+8,g+8),
    B=U(d+2,4,4)+(2,1),
    E=U(d+2,g,g), E(r,c)=(g+7-r,c+1),
    D=U(d,g,g)+(5,2).

Put I={A,B,E}, J=I+{D}. Their original endpoint intervals are

| Owner | Two-row bar | Remaining legs |
|---|---|---|
| A | rows 0,1; columns 1..d+4 | columns 1,d+4; rows 2..g+8 |
| B | rows 2,3; columns 2..d+3 | columns 2,d+3; rows 4..6 |
| D | rows 5,6; columns 3..d+2 | columns 3,d+2; rows 7..g+5 |
| E | rows g+6,g+7; columns 2..d+3 | columns 2,d+3; rows 7..g+5 |

The intervals are pairwise disjoint, so all original matching edges remain
disjoint and unchanged. The original endpoint graphs are connected to
each other by adjacent endpoints: A to B, B to E, and D to B and E.

The retained supports of J are exactly

    (r,0),(r,d+5), r=0,2,...,g+8;
    (g+9,1),(g+9,d+4);
    (r,4),(r,d+1), r=8,10,...,g+4.                    (9)

Each has its unique original anchor as its sole occupied neighbor. To
verify exhaustiveness, A's inner supports on rows 3,5 belong to B and
those on odd rows 7..g+7 belong to E. B's outer supports belong to A,
inner supports to D, and endcaps to E. D's upper outer supports belong
to B, outer leg supports to E, and endcaps to E's bar. E's outer supports
belong to A, inner supports to D, and endcaps to B. This accounts for
every original support. Endpoints retain their original three occupied
neighbors because all mandatory supports remain occupied. Thus J is
complete feasible for every stated parameter.

Removing D replaces the last line of (9) by

    (5,3),(5,d+2);
    (r,3),(r,d+2), r=8,10,...,g+4.                   (10)

These also have unique occupied anchors, proving I complete feasible.
Only A is positive, both gates are consumed by B, and neither terminal
is activated: N=1,G=2,Aactivation=0. B's support (7,2) sees its original
anchor and A(7,1), so the seed {A,B} forces E. Since I is already feasible,
its least feasible closure inside J is exactly I.

The aligned tile scan is particularly simple. The long stem pairs are
regular, except for the two facing terminal tiles in I; the two-row bars
are full except at their named ends and the internal upper/lower strips.
In I the B/E terminal singleton pair in each tile with origin (6,2) or
(6,d+2) consists of two mutually consumed irregular singletons. All other
nonfull stem pairs retain their original regular profiles. In J those
terminal tiles become full. At origins (4,2),(4,d+2) the B leg pair and
D corner create exactly the two mixed caps. Along D's upper and lower
bar the internal d/2-1 pairs have an empty opposite row; its remaining
stem pairs retain their regular supports from (9). Thus the COMPLETE
nonzero reserve ledger is

| Family | Nonzero counts | R | mu |
|---|---|---|---|
| I | L2mutual=2 | 2 | 1 |
| J | L3=2, L2bar=d-2 | d-1 | d-2 |

For all even d>=8,g>=6 add

    C=U(d-2,g-2,g-2)+(7,3),  K=J+{C}.                (11)

C's bar is rows 7,8, columns 4..d+1; its legs are columns 4,d+1,
rows 9..g+5, disjoint from every old endpoint. Its outer supports are
consumed by D and its endcaps by E's bar. The formerly retained inner
supports of D are consumed by C; the only retained inner supports now are

    (r,5),(r,d), r=10,12,...,g+4.                     (12)

Together with the first two lines of (9), these have unique occupied
anchors. This proves complete feasibility for all parameters in (11).
Every lower pair of D, including {6,7}x{4,5}, is now full. C's two original
unfilled triples contribute U0=2; its lower bar contributes d/2-3 irregular
pairs; D's permanent upper strip contributes d/2-1. The two caps persist.
Thus K has exactly L3=2,U0=2,L2bar=d-4 and

    R(K)=d-2, mu(K)=d-3, R(K)-R(J)=-1.               (13)

Directly counting the endpoint intervals and supports gives

| Family | Endpoints | Matching edges | Selected supports |
|---|---|---|---|
| I | 6d+4g+34 | (6d+4g+34)/2 | 2g+12 |
| J | 8d+6g+32 | (8d+6g+32)/2 | 2g+10 |
| K | 10d+8g+22 | (10d+8g+22)/2 | 2g+8 |

In J both cap descriptions use the same D upper strip: z=2 but
u=d/2-1, not d-2. At g=4 the lower enclosure also applies and
p=u=d/2-1, so (7) is exact: R>=d-1=R(J). At g>=6 the lower enclosure
hypothesis fails; (11) proves those lower pairs need not persist.
This is a counterexample to that stronger persistence rule, with positive
allocation margins throughout, not a counterexample to mu>=0.

## 7. Validation scope and remaining work

Run python3 develop/check_persistent_corridor_capacity.py. It independently
reconstructs original matching/support data, exact retained-support formulas,
complete degree feasibility, connectedness, Horn hull, all nonzero defects
and actual tile receipts. It checks partition-preserving certificate detection
across all 32 phase/isometry images, opposite-corner strip deduplication,
cross-class exclusion with both m8 examples, and actual component subunions.
Partial east-entry catalogue controls are discovery/checks, not complete
filled-corridor realizations. The general arguments are Sections 1-6.

formal/SubQuorum/PersistentCorridorCapacity.lean formalizes unbounded
coordinate collision/gap lemmas, arbitrary predecessor descent, the
protected-gap consequence, per-owner strip capacity, and the aggregate
integer loss/coverage implications. Original source-role exhaustion,
physical-to-count adapters, m8 receipt disjointness and the parametric
support/tile scan remain written proofs with independent Python controls.
No end-to-end source geometry or grid formalization is claimed.

The [later residual-coverage corollary](CORRIDOR_RESIDUAL_COVERAGE.md)
combines the reserve floor with joint S/P/R activation injection to give
mu>=p+u+ceil((m8-t)/2). The final source contains twelve scoped declarations,
including two integer corollaries added after the original review request.

The full-bar obstruction's original audit5a86d678 completed ACCEPT during
this turn,15154characters with exact stream/API agreement and independent
reading. Its scope does not include this note. The completed research
response b90c01ca proposed the
corridor and parametric family; this note independently reconstructs those
arguments and adds the explicit combination with the existing m8 theorem.
Any new independent review of this note has its own receipt and scope.

The remaining full-target work is universal coverage: filled corridors
allow v+2<=h<=d-4, but this compares a width and a leg and does not supply
a decreasing invariant for subsequent owners. Vertical full-bar regular
exits also remain uncovered. A general terminating transport rule must
produce enough distinct actual receipts to prove (8), or a complete
feasible family must disprove the allocation. Neither is established here.
Submitted manuscripts are unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
