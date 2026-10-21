# A narrow north corridor has an exact neutral two-owner package

21 October 2026. This continues the [north contact debit](SECONDARY_TEN_NORTH_CONTACT_DEBIT.md)
in the first separated case m=w+4. It proves a general consumer dichotomy,
an exact local compensation identity when the first consumer points outward,
and an explicit obstruction to extending that identity by endpoint disjointness
alone. It does not prove unrestricted allocation or grid equality.

## 1. Original-source hypotheses and forced consumers

Use the finite complete original U/rotor model, fixed endpoint ownership
and matching, legal even U widths>=6 and independent even legs>=4.
Every original support not consumed by an endpoint remains occupied with
its original anchor as its sole occupied neighbor. Whole original sources,
including supports and anchors, move together. Tiles are aligned 2 by 2.
N counts positive ORIGINAL owners only; b is even. Prescribe disjoint sources

    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    D=U(w+4,10,t), D(r,c)=(b-11+r,c+5),
    L=U(w,4,v), L(r,c)=(b-9+r,c+6), w>=8.

Write a=b-9 and u=(a,w+7). L's original support u has original anchor
(a,w+6) to its west; D owns (a-1,w+7) to its north. The point is absent
from Q/D/L. Completeness forces its actual consumer C, distinct from all
three. D also owns (a,w+9), exactly two steps east of u.

**Consumer dichotomy.** C is a south-terminal U in precisely one of the
two frames below, with legal even dimensions k,h,f:

    C_R=U(k,h,f), C_R(r,c)=(a+h-r,w+6+c), h>=t,
    C_L=U(k,h,f), C_L(r,c)=(a+h-r,w+8-c), h>=v+2.

Its isolated charge is +1 for C_R and -1 for C_L. Both original supports
of its terminal u are consumed: its axial support by D, and its lateral
support by L in C_R. For C_L the lateral support u2=(a,w+8) must instead
be consumed by another actual owner, as proved below. These are necessary
forms; C_L may have further disjointness restrictions.

Proof of exhaustion. The north/west occupied neighbors of u belong to
different actual owners, so C's own neighbors can only be south/east.
Every east-bearing U terminal or corner reaches (a,w+9): incident legs
have length>=4 and an outward bar extends at least five steps. Straight
interiors require opposite own neighbors, and junctions/other bar roles
have degree3. Thus the only remaining U role is a south terminal, with
its bar below and pointing right or left. This gives the displayed charts.

All four rotor tips are excluded by mandatory original endpoints:

| Tip | Relative blocker at u | Owner |
|---|---|---|
| South A | (2,-1) | L(2,w) |
| South B | (1,-1) | L(1,w) |
| East A | (-2,1) | D(0,w+3) |
| East B | (-1,2) | D(1,w+4) |

Rotor nontips have degree3. These blockers do not depend on any upper
bound on source dimensions. If C_R had h<=t-2, its first bar row
(a+h-1,w+9) would meet D's far stem. Hence h>=t by evenness.
If C_L had h<=v, its first bar row at column w+6 would meet L's far
stem, hence h>=v+2. The established U phase table gives the stated charges.

**Negative continuation.** If the actual C is C_L, completeness forces
a distinct actual owner C2 at u2=(a,w+8). This owner is again a south
terminal U. In its right-pointing frame it has charge -1 and incident
length h2>=t; in its left-pointing frame it has charge +1 and h2>=h+2.

Indeed u2 is C_L's original lateral support, anchored west at u. D owns
its north neighbor and its immediate east neighbor (a,w+9). The point
is absent from Q/D/L/C_L. Thus its own endpoint neighbors can only be
south. South rotor A contains u2+(2,-1), and south B contains u2+(1,-1),
both on C_L's near stem (h>=v+2>=6). Only a south-terminal U remains.
A right bar must pass below D's far stem, giving h2>=t as before.
A left bar must pass below C_L's entire near stem, so h2>=h+2.
The column parity has changed, interchanging the +1/-1 phases. Explicitly,
write lambda=(h+f)/2 and retain the ORIGINAL support count in touched tiles:

| Physical phase | Matching edges | Touched tiles | Original supports inside | Original full bar tiles | Charge |
|---|---|---|---|---|---|
| C_R; left-pointing C2 | k-1+lambda | k/2+1+lambda | 4+lambda | k/2-1 | +1 |
| C_L; right-pointing C2 | k-1+lambda | k/2+lambda | lambda | k/2 | -1 |

The first phase has two bar-end supports, two axial terminal supports
and lambda even-row lateral supports inside touched tiles. The second
has two axial terminal supports and lambda-2 odd-row lateral supports.
Substitution into matching+inside-2*tiles gives the charges directly.
The independent review reconstructs this same all-dimension phase table.
No positivity of C2 is presumed; the two consecutive consumers can both
have negative charge at the endpoint-disjoint level.

## 2. Exact local compensation for the outward positive branch

For any endpoint-disjoint original family define the algebraic functional

    Rraw=S+2F-E, Phi=N+Rraw,

with the same ORIGINAL negative charge mass S, actual mixed full tiles F,
and source-labelled directed intratile events E as in the preceding note.
Rraw equals physical reserve only for a complete feasible family. Partial
families below are used for exact accounting, not asserted feasible.

Assume the actual C is C_R. For arbitrary legal k,h,f with h>=t its
endpoint set is disjoint from Q/D/L. Put d=min(h,v)/2. Then insertion
of C_R into Q/D/L has the exact counts

    Delta S=0, Delta N=1,
    Delta F=1+d, Delta E=1+2d,
    Delta Rraw=1, Delta Phi=2.                  (1)

Combining this with insertion of L into Q/D, whose debit is2, gives

    Phi(Q union D union L union C_R)=Phi(Q union D).    (2)

Thus the outward package exactly restores the local N+Rraw potential;
there is no leftover local credit. It does not give an additional owner
count, activation credit or global coefficient improvement.

Proof of (1). C_R's minimum column is w+7>=15, beyond Q's last endpoint
tile at columns10/11. Apart from the tile containing u, the only shared
endpoint tiles are L/C_R's parallel stems at columns w+6,w+7, on paired
rows (a+1,a+2),...,(a+min(h,v)-1,a+min(h,v)). There are d of these.
D's far stem is in the next column pair w+8,w+9. The bar of C_R starts
at row a+h-1, whereas D ends at a+t-2. Since h>=t, even at equality
these rows lie in different tile rows. Thus there is no additional D/C_R
tile contact. C_R's far stem lies strictly to the right of D and L.

The tile containing u had two D endpoints and one L endpoint; C_R fills
its fourth cell. It gains one full tile and exactly one directed event,
from D's north endpoint to u. L's eastward direction meets its ORIGINAL
bar-end support u, and C_R's north/west directions meet its ORIGINAL
terminal supports, so these are not events. Each parallel-stem tile gains
one full tile and two directed events: one in each direction on the odd
intrinsic stem row; the other cross directions meet original supports.
This remains true when a stem ends in that tile or C_R's bar starts there.
Every mixed full tile in this partition contains a previous owner's
endpoint; C_R's own full bar tiles are excluded from F. The partition
exhausts every shared tile and proves (1) for arbitrary independent dimensions.
The charge +1 gives Delta S=0 and Delta N=1. Equation (2) follows from
the previous general debit2 theorem. Its numerical cancellation is exact.

## 3. External contacts: the package still has a signed obstruction

Let W be any other endpoint-disjoint original family, disjoint from the
whole prescribed package. Write P={L,C_R}. Let Fextra count newly mixed
full tiles in adding P to Q/D/W, excluding the package's internal full
tiles; let E(P,W) include BOTH directions of all actual intratile events
between P and W. Then

    Phi(Q/D/W/P)-Phi(Q/D/W)=2Fextra-E(P,W).       (3)

Every internal full tile contains an L or C_R endpoint absent from the
base, so it is necessarily new; W cannot have an endpoint in it. All new events split
uniquely into internal events and events with an external endpoint owner.
The negative source mass and positive owner count are additive on the
actual source sets. Applying (2) yields (3). No tile, event, owner or
initial margin is used twice. No sign for the right-hand side is implied.

In fact external nonnegativity remains false even after the missing
support u has been consumed by the positive C_R. Take

    b=40, w=12, t=4, v=6,
    C_R=U(6,4,4), C_R(r,c)=(35-r,18+c),
    W=U(6,4,4), W(r,c)=(32+c,13+r).

All five original endpoint sets Q,D,L,C_R,W are disjoint. C_R has no
endpoint tile in common with W, so the same two extra full tiles and
seven L/W events from the previous counterexample survive after a
four-column translation, which also avoids Q:

    2Fextra-E(P,W)=4-7=-3.

The package consumes u=(31,19), and its terminal is genuinely positive
with both original supports consumed by D and L. Nevertheless adding
the whole package decreases Phi by3 in this PARTIAL five-source family.
This refutes endpoint-only external nonnegativity even for the repaired
positive package. It is not a complete-model counterexample. For example
D's original support (32,20) remains absent from all endpoints, while
its anchor (32,21) and C_R's endpoint (32,19) are occupied. It is also
C_R's original support with the other anchor. A complete
extension must still consume it, and no favorable payment is presumed.

## 4. Verification scope and next step

The accompanying checker independently constructs original matchings,
support sets, tiles and directed events. It checks every bounded U/rotor
role at both forced points, exact all-parameter formulas over separated
large test dimensions, source phases and the explicit package obstruction.
These finite checks corroborate the formulas on the tested instances;
the catalogue exhaustion and tile partition establish the general statements.

Scoped Lean verifies blocker coordinates, geometric collision implications,
forced-site absence, parity bounds and exact ledger algebra. Catalogue
exhaustion, geometric tile partition and actual-source interpretation remain
written. No full allocation formalization or global target nonreuse is claimed.
See the [independent checker](../develop/check_secondary_ten_north_gap_four_package.py),
[controls and exact witness events](../output/secondary-ten-north-gap-four-package-controls.json),
[scoped Lean source](../formal/SubQuorum/SecondaryTenNorthGapFourPackage.lean)
and [formal scope receipt](../output/secondary-ten-north-gap-four-package-formal-check.json).
The initial written [review](../output/secondary-ten-north-gap-four-package-review.json)
COMPLETED with ACCEPT, no mathematical hypothesis or accounting repair.
Two wording clarifications distinguish external endpoints from original
supports and finite corroboration from the general proof. The subsequent
cavity theorem and six-source family are outside that audit's input.

The remaining task is to control the signed external term using COMPLETE
support closure, or prove a general rule for the two negative-consumer branch.
The subsequent [cavity theorem](SECONDARY_TEN_NORTH_OUTWARD_CAVITY.md)
forces another negative owner in the outward branch, excludes h=t and
proves K>=8 when h=t+2. It is outside this note's initial review input.
An isolated neutral package cannot be spent as fresh global surplus. This
note proves no universal improvement of5/6 and no rectangular-grid equality.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
