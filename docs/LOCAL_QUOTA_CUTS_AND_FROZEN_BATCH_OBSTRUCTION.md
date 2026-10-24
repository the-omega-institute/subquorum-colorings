# Local strip quotas and a frozen obstruction to every donor batch

20 October 2026. The componentwise mixed certificate can be strengthened
by combining its two allowed quotas separately at each run. Standard
capacitated incidence matching gives an exact cut formula. It eliminates
two of the four five-slot first-obstruction motifs. A different result
is negative and geometric: an unbounded fully frozen two-leg family has
exactly two available corner donors, and EVERY nonempty subset of them
lowers both the old and the stronger budgets. Neither choosing an order
nor reserving all these donors simultaneously restores monotonicity.
The target grid inequality and universal initial coverage remain open.

## 1. Local quotas, physical allocations and a standard cut theorem

Use the original fixed maximal horizontal/vertical endpoint-free runs,
and label each residual capacity unit by its tile and unit number. The
incidence graph G has these runs as vertices and the residual physical
slots as edges. The original capacity D, old distinct reservation B and
remaining edge count R satisfy R=D-B. Reservations delete slots; they
do not change which original runs are used.

For a run v with degree d(v), use quota

    b(v) = 0                              if d(v)=0,
           max(1,floor(d(v)/2))           otherwise.

Let A(G) be the largest number of distinct slots that can be assigned
to incident runs, using at most b(v) slots at each run. This is a
capacitated incidence matching problem. Every old one-per-run allocation
and every old half-capacity allocation obeys these quotas, including
the old componentwise choices. Hence, writing F for the preceding score,

    F(G) <= A(G) <= R.                                         (1)

This permits local combinations within a component; it does not add
two allocations using the same slots. A chosen allocation still assigns
each physical slot at most once. The quotas are a specified certificate
family, not an unrestricted allocation model that could assign every
slot to an arbitrary endpoint. As before, relating its budget to receiver
charge requires a separate geometric coverage argument.

For U a set of original runs let E(U) be the slots with BOTH ends in U,
and let delta(U) be the slots with exactly one end in U. All counts
include parallel physical units. The standard capacitated matching dual is

    L(G) := R-A(G) = max_U (|E(U)|-sum_{v in U} b(v)).           (2)

The empty set is included, so the maximum is nonnegative.

**Proof, including an attaining cut.** Any allocation can assign at most
sum_{v in U} b(v) internal slots to U; an internal slot has no other
possible owner. Thus it leaves at least the displayed deficiency unused.

Expand each vertex v into b(v) request copies adjacent to every incident
slot, and take a maximum bipartite matching. Start from all unmatched
slots. From a reached slot reach all request copies of both incident
runs; from a reached copy traverse its matched slot. No reached copy
is unmatched, since that would give an augmenting path. Let U be the
reached runs. Every one of their quota copies is reached and matched.
Their assigned slots are reached as well. Every reached slot has both
ends in U. Conversely every internal slot is either unmatched (a starting
slot) or matched to a run in U, so is reached. Thus the reached slots
are exactly E(U), partitioned into all unmatched slots and exactly
sum_{v in U} b(v) matched slots. This attains the deficiency in (2).
It also gives a checkable upper-bound witness alongside the allocation.
QED. This is a standard matching argument, not a new general graph theorem.

## 2. Exact odd-core loss, cross-component counting and reservations

For a subset U, use degrees in the WHOLE current residual graph. Put

    a(U) = number of vertices in U of odd degree at least three,
    l(U) = number of vertices in U of degree one,
    c(U) = |delta(U)|.

Then the degree-sum identity yields

    2(|E(U)|-sum_U b) = a(U)-l(U)-c(U),
    L(G) = (1/2) max_U [a(U)-l(U)-c(U)].                       (3)

**Proof.** The total degree on U is 2|E(U)|+c(U). Rounding half-degrees
down subtracts one half for each odd-degree vertex. The local quota adds
one back for each degree-one vertex. Thus the odd contribution is
(a+l)-2l=a-l. Substitution proves the first equality, and (2) proves
the second. Every bracket is even. QED.

An obstruction therefore needs an internal cluster of odd nonleaf runs
whose count exceeds its leaves and boundary slots. A whole-component odd
count can miss the worst internal cut; the attaining cut in the algorithm
uses full-graph degrees and counts every boundary slot once.

Cuts separate over resource components: E(U), vertex quotas and the
boundary counts are additive across them. Consequently L is the sum of
their individual maximum deficiencies. They share no slots. This gives
one unified count without assigning a surplus to two receivers or adding
the budgets of competing rules on the same component.

For a further batch of t distinct reservations, with graph G' and B'=B+t,

    B+A(G) = D-L(G),
    B'+A(G')-(B+A(G)) = L(G)-L(G').                            (4)

Thus safe reservation is exactly nonincrease of the maximum cut deficiency.
This is a different score from F; the previous fixed-old-branch parity
identity remains valid for F and is not silently transferred to A.

With the ORIGINAL corrected ledger sigma=D-rho and residual charge
q=rho-B, coverage by the new certificate asks

    q <= A(G)  iff  sigma >= L(G).                             (5)

By (1), L is at most the old mixed loss. Equation (5) is conditional;
no universal coverage theorem or unrestricted five-sixths improvement
follows from matching feasibility alone.

## 3. The remaining first-charge-five resource motifs

If A(G)<q<=R, (1) and the preceding mixed threshold imply q>=5.
At q=5 the old classification forces one positive-capacity resource
component, four vertices, and five or six slots. The new classification
keeps exactly these multiplicity matrices, up to exchanging the two
sides and their orders:

    five slots:    1 2       2 1
                   2 0       1 1

    six slots:     2 1
                   1 2

In the five-slot cases the degrees are 2,2,3,3; every quota is one.
In the six-slot case every degree is three and every quota is also one.
The exact one-per-run rank is four, so A=4 in each case. These are a
weighted path, a four-cycle with one doubled edge, and a four-cycle
with two opposite doubled edges. No frozen charge-five realization is
asserted.

The two removed five-slot motifs are the star (2,2,1) and the matrix
[[2,2],[1,0]]. In the star, give every leaf one slot and the two
remaining slots to the central run, whose quota is two. In the matrix,
give the degree-one row its slot, the degree-four row one slot from
each doubled tile, and each column the remaining slot of its doubled
tile. All five slots are paid in both cases. This proves the exclusion
without enumeration. The checker confirms that exactly30of the previous
60first-q5patterns on a2-by-3tile array are repaired: remaining counts
are24with R5and6with R6. All three remaining motifs have no leaves.

Their physical positive-capacity tiles occupy three or four corners of
an axis-aligned tile rectangle. The two horizontal runs must belong to
different tile rows: they share a vertical run and cannot both meet that
run at different tiles in one row. The same argument separates the two
vertical bands. Edges of the resource graph enforce endpoint-free
intervals between the corresponding positive tiles. In the three-tile
case no claim is made that the fourth corner is endpoint-free; in the
four-tile cases all four connecting intervals are endpoint-free. These
are additional concrete geometric targets for the next coverage proof.

## 4. An unbounded frozen obstruction to EVERY nonempty donor batch

Take two_leg_case(w,6,6), with w=2k even and k>=4. The full physical
construction and retained-witness proof are given in
TWO_LEG_DEGREE_THREE_COVERAGE_OBSTRUCTION.md. It has a two-row bar
at rows0,1 and columns1,...,w, with two height-six legs at columns1,w.
The displayed actual matching and alternating selected supports make
every endpoint have occupied degree exactly three. The bottom-up leg
waves, the two opposite bar waves and final odd leg waves freeze every
endpoint. The earliest promoted endpoint in that order retains two
occupied witnesses, ruling out every simultaneous mixed promotion bundle.

Section 4 of TWO_LEG_DEGREE_THREE_COVERAGE_OBSTRUCTION.md proves uniformly
for every even w>=6 and both even leg heights at least four that the three
older corner rules have no donors. Apply that written theorem with a=b=6
to every even w>=8 here; the donor-completeness dependency is general and
is not inferred from the finite or Lean controls. For the fourth rule,
the selected corner must have its
unique occupied anchor outside its tile. The only eligible selections
are the odd-row inner supports, at rows3and5. On the left, their opposite
corners are respectively(2,3)and(4,3). The exterior neighbors of the first
are(1,3), a bar endpoint, and(2,4), blank. The exterior neighbors of the
second are(3,3)and(4,4), both blank. Hence only the row3support has an
endpoint guard. Reflection proves the right-hand statement. The guard's
other three neighbors are bar endpoints and its occupied degree is three.
Thus the fourth rule has EXACTLY two unit donors: Q_(1,1) and Q_(1,k-1).
Both have the same complete receiver owner. The following examines every
donor from all four current rules, not a favorable subcollection.

The endpoint-free tiles form exactly the rectangle

    rows 1,2,3; columns 1,...,k-1.

In rows1,2 the first and last tile have capacity one, with every middle
tile capacity two. In row3 every tile has capacity two. This follows
directly from the selected inner supports at physical rows3,5; all
unlisted endpoint-free vertices are blank. In particular the resource
graph is connected and has

    R=D=6k-10=3w-10,
    horizontal degrees 2k-4,2k-4,2k-2,
    first/last vertical degrees 4,4 and all others 6,
    K=k+2,  W=F=A=R.

All active degrees are even and at least four. The two donor slots lie
in the same first horizontal run and in the two distinct outer vertical
runs. Delete either donor. Its two run degrees become odd, still at
least three. All active runs have degree at least two, so local quotas
equal half-degree floors, whose total is R-2. The half-capacity matching
attains this, while the sum of quotas is an upper bound. Hence

    B'+F'=B'+A'=1+(R-2)=R-1.                                 (6)

Delete both donor slots instead. The first horizontal degree drops by
two and is even and at least two; the two outer vertical degrees each
drop from four to three. Exactly two odd vertices remain. The local
quota total and half-capacity score are R-3. Again both bounds coincide:

    B'+F'=B'+A'=2+(R-3)=R-1.                                 (7)

The graph stays connected, with rank k+2, which is below R-3 for k>=4;
therefore the old mixed rule also chooses the weighted branch in every
case. Equations (6)-(7) prove the all-width assertion. Every nonempty
subset loses one budget unit. Neither sequential order has a safe first
step, and the complete simultaneous batch loses the same unit. Choosing
no new reservation retains R; it is the only safe subset among these
two donors. Allowing different additional donor rules is outside this
negative statement.

For w=8, the fully frozen example is8-by-10 with26endpoints,14selections
and13matching edges. The receiver has11tiles,10selections and corrected
charge1, including both actual saturated-endpoint transfers. D=14,
objective27<half-area40. Its four reservation states are

| Reserved donors | Remaining capacities by horizontal run | Odd runs | F=A | B+F=B+A |
|---|---|---|---|---|
| none | 4,4,6 | 0 | 14 | 14 |
| left only | 3,4,6 | 2 | 12 | 13 |
| right only | 3,4,6 | 2 | 12 | 13 |
| both | 2,4,6 | 2 | 11 | 13 |

The guard coordinates are selected(3,2),anchor(3,1),guard(1,3) on the
left and selected(3,w-1),anchor(3,w),guard(1,w-2) on the right. The exact
matching, ordered26-row freezing certificate, ledger, distinct allocations
and attaining cuts are embedded in output/local-quota-strip-controls.json.

The family never refutes initial coverage or the grid target: rho=1,
and its objective w+19 has slack3w-11>0. It refutes the proposed general
safe-order and complete-batch reservation repairs for these scores, even
with genuine same-owner donors in frozen occupied-degree-three geometry.

## 5. Validation and formal scope

Run from the repository root:

    python3 develop/check_local_quota_strip_allocation.py --output output/local-quota-strip-controls.json

The checker covers729capacity arrays and all23,328run subsets on the
2-by-3tile model. It verifies the exact cut/odd-core identities, attaining
matching and cut, physical non-reuse and dominance of the old score.
The new score strictly improves192patterns. There are96physical
fixture/symmetry/reservation controls and3separated-receiver controls.
The old20-endpoint right-donor failure is repaired by the local quota;
that repair is specific and does not override the wider negative family.

The frozen family is tested at14even widths including64, every physical
symmetry and all four donor subsets:448symmetry/batch cases. Its all-width
proof is in Section4, not inferred from these cases. A separate blank
4-by-4 resource-only monotonicity counterexample is also retained with
zero receiver charge and no claimed donor.

FrozenDonorBatchObstruction.lean checks the finite26-endpoint physical
configuration: actual coordinates/matching, selected feasibility,
terminal endpoints, the full inductive frozen certificate and exclusion
of every promotion bundle, original corrected charge and residual quota
counts for all four subsets. It also proves the arbitrary-width budget
arithmetic from k>=4. The general matching/cut theorem, all-width
coordinate adapter, donor-rule completeness and graph rank/attainment
are written and computationally checked, not claimed fully formalized
by this finite development. Submitted manuscripts remain unchanged.

The48declarations compile locally with Lean4.33.0and pass their individual
axiom audits: many finite checks have no axioms, others use propext, and
the combined frozen-exclusion and all-width arithmetic declarations
add Classical.choice/Quot.sound. No sorryAx or native_decide occurs.
The scoped build imports only the Std-based FrozenPromotion dependency;
its temporary compiled output is removed after checking. No Mathlib
rebuild or shared CI change is involved. See
output/frozen-donor-batch-formal-check.json for the execution receipt.

The restricted search now has --first-local-quota-obstruction. Its
four-active-run/no-degree-one encoding is checked against independent
allocation on all729patterns, accepting exactly30. It still imposes
originalcharge5, B0and absence of the four old donor types. No new
timeout run is presented as geometric exclusion or as general coverage.

Next: examine the three leaf-free first-q5geometries using the original
receiver ledger. Do not assume that any ordering or the complete batch
of current corner donors preserves an existing optimal resource score.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
