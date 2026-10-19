# A capped chamber corner owns a distinct unit of physical deficit

19 October 2026. A local corner witness gives a coefficient-one criterion
without any channel-cover hypothesis. It applies to all positive-phase thick
elbows in `ELBOW_SOURCE_COMPENSATION.md`, in arbitrary tile-preserving directions,
and more generally to every terminal configuration whose positive receivers
have charge at most one and possess the witness below. Other components need
not be prescribed straight combs. The argument assigns an actual no-endpoint
physical square to each positive component and proves these assignments
injective. No source phase is added as a second resource.

This result was developed after the phase-note review was submitted. It is
outside that review's input until separately assessed.

## 1. The local witness and deficit lemma

Let Q={0,1} x {0,1} be one actual physical square, in local coordinates.
Write P for matching endpoints and T for selected sites. A capped chamber
corner witness in the north/west orientation consists of

    (-1,-1),(-1,0),(-1,1),(-1,2),(0,-1) in P,
    (1,-1) in T,
    (0,0),(0,1) not in P.                           (1)

All named vertices and Q lie in the ambient grid. The four consecutive north
endpoints and the west short tip belong to a single endpoint component H.
The other seven orientations are obtained by physical-square-preserving
rotations/reflections. Assume the usual feasibility at selected vertices and
terminality: every endpoint has occupied degree at least three.

**Local deficit lemma.** Q has no endpoints and at most one selection, hence
its actual physical deficit d_Q=2-|T intersect Q| is at least one.

Proof. The selected support (1,-1) already sees the short-tip endpoint
(0,-1), so (1,0) is blank. Site (0,0) sees endpoints (-1,0),(0,-1), so
cannot be selected; it is not an endpoint by (1), hence is blank as well.

Suppose (1,1) were an endpoint. Then (0,1), already not an endpoint, could
not be selected because it would see both (-1,1) and (1,1). Thus (0,1)
would be blank. Endpoint (1,1) would then have two blank neighbors, (0,1)
and (1,0), so occupied degree at most two, contrary to terminality. Therefore
neither lower corner is an endpoint. The two upper corners are excluded
in (1), proving Q endpoint-free.

Only (0,1),(1,1) can be selected. If both were selected, (0,1) would see
(-1,1) and (1,1), violating feasibility. Hence Q contains at most one
selection. This proof allows arbitrary feasible data outside the witness.
QED.

For a thick elbow, translate relative (2,1) to the northwest corner of Q.
The four north endpoints are chamber sites (1,0),(1,1),(1,2),(1,3), the
short tip is (2,0), and the selected support is (3,0). The two upper Q
sites (2,1),(2,2) are outside its complete endpoint component; any foreign
endpoint there would join that component through row 1. Thus (1) holds
for all even w>=6,h>=4. The square lies inside the ambient rectangle
because the chamber extends through column 3 and the support exists in
row 3. In the sharp-flank configuration Q has exactly one selection at
(2,2), so the one-unit deficit bound is sharp.

## 2. Injectivity across arbitrary components and orientations

**Unique-owner lemma.** Two capped corner witnesses assigned to the same
physical square have the same endpoint component.

Proof. Each witness marks a full side of Q by a run of four consecutive
endpoints, extending one site beyond each corner. If the full sides of two
witnesses are the same, they share endpoints. If the full sides are adjacent,
the two extended runs meet at their common exterior corner. For example,
the north run (-1,-1),...,(-1,2) and east run (-1,2),...,(2,2) share
(-1,2). Thus in either case the witnesses belong to the same component.

If the full sides are opposite, rotate the first to north/west form (1),
reflecting horizontally if needed. The second has a south run through
(2,-1),(2,0),(2,1),(2,2), regardless of the direction of its short tip.
The selected support (1,-1) would see both (0,-1) and (2,-1), contradicting
feasibility. Thus opposite full sides cannot occur. These cases exhaust
the four possible full sides. QED.

The use of the extended four-endpoint run is essential to this injectivity
proof. A reduced two-endpoint-side pattern alone admits abstract shared
local models; those do not realize two distinct complete corner witnesses.
Their presence would not contradict the result under its full hypotheses.

## 3. A general coefficient-one theorem

Use a feasible terminal representative in an even-by-even grid and the
whole component-receiver identity

    Delta=mn/2-|T|-|M|=D_all-sum_H rho_H,            (2)

where D_all is the sum of actual deficits d_Q over physical squares with
no endpoints, and rho_H is the whole corrected charge of component H.
Endpoint-square ownership is the established terminal component lemma.
Every no-endpoint deficit is nonnegative: three selected corners would give
one selected vertex two occupied neighbors.

**Capped-corner compensation theorem.** Suppose every positive receiver H
has rho_H<=1 and admits at least one witness (1) in a tile-preserving
orientation. Then

    |T|+|M|<=mn/2.                                 (3)

Proof. Choose one witness for each positive receiver and assign its square
Q_H to H. The local lemma makes Q_H a physical no-endpoint square with
d_(Q_H)>=1. The unique-owner lemma makes the assignment injective across
different endpoint components. For B positive receivers,

    sum_(rho_H>0) rho_H <= B
       <= sum_(rho_H>0) d_(Q_H) <= D_all.

All other receiver charges are nonpositive. Substitute into (2). Every
physical deficit occurs at most once; no phase, shifted square or already
retained selection is counted as extra supply. QED.

**Elbow consequence.** If all positive endpoint components are the complete
positive-phase thick elbows with the prescribed retained supports, then
(3) holds, even if all other terminal components have arbitrary shapes and
nonpositive charge. Each elbow has charge exactly one and the required
corner witness. Unlike the earlier channel certificate, this consequence
requires no channel-cover existence or signed-comb-flux assumption.

The same conclusion holds for an initial representative whose authorized
normalization preserves the complete frozen elbow data and ends in this
class: normalization does not decrease the objective, and the elbow freezing
theorem protects its matching endpoints and retained supports. Other final
components must still satisfy the stated charge condition.

This improves the universal 5/6 coefficient to one on the entire stated
class. It leaves unrestricted positive bends and the general grid equality
open. The criterion applies to local witnesses, not to all positive receivers
merely because they contain a turn or a square.

## 4. Combining with other certificates

This is a direct physical donor certificate. It can be used as an alternative
to the phase/channel certificate; the same elbow cannot be paid by both
without a new incidence check. If a unit h_Q in {0,1} has been reserved for
an elbow at Q, the unit-ledger deficit remaining there is d_Q-h_Q. Any
additional whole-deficit certificate must fit those remaining amounts.

For the doubled long-source mouth ledger with elbow tax -2B_E, a sufficient
pointwise condition for simultaneously paying the owned elbows and channels is

    2h_Q+d_Q sum_(j:Q in C_j) w_j <= (2-m_Q)d_Q.    (4)

Sum (4), use sum_Q h_Q=B_E and the channel raw lower bounds, and substitute
in the corrected ledger. This pays the elbow tax exactly once and then
allows the remaining channel certificate. Condition (4) may fail for a
choice of overlapping channels even though either certificate separately
works; such a failure concerns that allocation, not (3) or the grid target.

## 5. Verification scope

The accompanying checker verifies the local deficit implication and the
incompatibility of distinct complete elbow witnesses sharing a square,
using actual endpoints, supports and all eight orientations. It checks
sharp unit donors and separated multi-elbow bundles. These finite controls
support the general geometric proof above, rather than replace it.

Lean separately checks the local deficit lemma from its actual grid-label
hypotheses and the opposite-run contradiction. Full coordinate mapping,
adjacent-side ownership and the global receiver adapter remain written;
the established general owned-donor sum theorem supplies the final counting
principle. No submitted manuscript is changed.
