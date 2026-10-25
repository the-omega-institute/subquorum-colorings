# Interacting square switches: shared-beta cuts and exact repair

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The [single-switch result](FROZEN_SQUARE_SWITCH_AND_INTERVAL_REPAIR.md) loses
one beta payment and repairs it through inherited original intervals. Two
switches on the SAME actual frozen board now lose two beta payments. Their
repairs interact through two shared entrances; distinct original intervals
alone need not suffice. We prove an exact full-payment criterion for an
arbitrary-support three-source/two-gate interface, formalize that criterion
in Lean for arbitrary resource identity types, and establish its application
to the complete original network of the new actual frozen board. We also
prove its exact value and minimum-link formulas for every availability Q.

Full interval availability still pays all sources. This is an obstacle to
independent beta/interval repair rules, not a counterexample to the numerical
grid target or an improvement of 5/6. Arbitrary interacting rematching remains
open. The submitted manuscript is preserved.

## 1. Two actual switches, fixed occupied sites

Start with the original 28-by-24, 49-selected/154-matching/308-endpoint fixture.
For each c in {4,18}, replace

    (5,c)--(6,c), (5,c+1)--(6,c+1)

by

    (5,c)--(5,c+1), (6,c)--(6,c+1).                    (1)

These switches use disjoint physical sites, but the resulting source routes
interact on the same board. Every other matching edge, all selected sites T
and all endpoint sites P are unchanged. Feasibility is unchanged. The new
matching has its OWN 48-layer strict rank certificate for all 308 endpoints;
it is completely frozen. Complete freezing is not assumed invariant under
arbitrary square switches.

The first surgery produces the previous 40-point alpha D, with TP ends
(24,4)/(14,11), and a two-point mixed path with TP/BP (5,4)/(5,5).
The second surgery exchanges the old right alpha and upper-right mixed
path, giving a 42-point alpha B with TP ends (24,19)/(12,14), and another
two-point mixed path with TP/BP (5,19)/(5,18). Each long body is exactly
the union of its two old bodies minus the two upper tip vertices. The other
two alpha sources are the unchanged top A and bottom C.

Counts remain four alpha, six beta and fifteen mixed. Original interval
identities, standard boundary marks, TP/BP sites and physical horizontal tip
adjacencies remain identical. Whole-owner assignments change. Two old
source/gate incidences become mixed self-links, so the old source/gate C4
is NOT preserved. In particular no retained-matching theorem is contradicted.

## 2. Complete reachable routes and the original support classes

A has no direct interval and has an exclusive one-link whole beta through
(5,17)->(5,16). No other alpha reaches this beta or the intermediate owners
on A's other branches. Any A payment costs at least one link. Thus A can be
prepaid, preserving value and never raising cost, and releases any interval
it might otherwise use.

The complete remaining reachable network has three sources B,D,C and two
mixed gates u,w. Gate u has BP (24,18), TP (18,15); w has BP (24,5),
TP (19,11). Let P,L,R denote direct original supports of B,D,C respectively,
and U,W the original supports of u,w. Their complete paying routes are:

| Source | Allowed route | Original unit | Link cost |
| --- | --- | --- | ---: |
| B | direct | P | 0 |
| B | enter u | U | 1 |
| B | enter u, then beta | one fixed whole beta | 2 |
| D | direct | L | 0 |
| D | enter w | W | 1 |
| C | direct | R | 0 |
| C | enter u | U | 1 |
| C | enter u, then beta | the SAME fixed whole beta | 2 |
| C | enter w | W | 1 |

All other reached mixed tails have empty support and no non-self continuation.
D has no beta path at any length. B and C reach the same beta only through
the SAME capacity-one u entrance. The beta's body support is a subset of W;
a route into its body can be changed to the whole-beta exit at equal cost,
releasing its interval. Two-arm forks there would reuse u and are impossible.
All other betas have at most one reachable alpha. Ordinary/full optima agree.
Every original owner, original beta and link remains in the model; this is
a reachable classification, not deletion of competing exits.

| Class | Original identities (band,column) | Size |
| --- | --- | ---: |
| P | band5 cols10,12; band6 cols12,15,16 | 5 |
| L | band5 cols10,12; band6 col12; band7 cols5..7,9,10,13,15; band8 cols5,7..11 | 16 |
| R | band12 cols7,12..16 | 6 |
| U | band7 cols13,15; band9 cols13,14 | 4 |
| W | band9 cols8..10,13,14; band10 cols12..15 | 9 |

The nonempty pairwise overlaps are precisely

    Z=P intersect L = {(5,10),(5,12),(6,12)},
    X=L intersect U = {(7,13),(7,15)},
    Y=U intersect W = {(9,13),(9,14)}.                  (2)

In particular R is disjoint from all others, P is disjoint from U,W,
L is disjoint from W, and U is contained in L union W. Each identity in
an overlap is still ONE original unit, with one sink capacity.

## 3. General shared-beta repair lemma

The next lemma applies to arbitrary finite identity sets and arbitrary
support sets P,L,R,U,W; it does NOT assume the sizes or overlaps in (2).
Assume exactly the route table above, actual capacity-one gates u,w,
a single whole-beta fallback through u, and simultaneous lifting of any
route assignment that uses different interval identities and different gates.
Routes of different sources have no other shared owners or BP entrances;
all other reachable alternatives have been dominated or excluded as in
Section 2. A is an additional, independent private payment of cost one.
These hypotheses must be checked from geometry in each application.

Write Pair_Q(E,F) if there are DISTINCT identities e in E intersect Q and
f in F intersect Q. Write SDR_Q(E,F,G) for three DISTINCT identities,
one in each indicated available set. They can overlap as sets, but the
chosen original identities cannot repeat.

**Lemma (exact full repair).** All four sources can be paid if and only if

    F(Q) := Pair_Q(L, P union R union W)
             OR Pair_Q(W, P union R).                    (3)

**Proof, necessity.** Remove the private A payment. If B is paid directly,
then D's payment either uses L directly or W through w. Their different
original interval identities give Pair(L,P) or Pair(W,P), both in (3).
If B is not direct, it occupies u, whether its exit is a U interval or
beta. C can then use neither U nor beta: it must take a direct R unit or
use w. If D is direct, these cases give Pair(L,R) or Pair(L,W). If D
uses w, C must be direct, giving Pair(W,R). These exhaust all cases and
establish (3), including both interval and entrance nonreuse.

**Sufficiency.** There are five possible distinct-unit pairs in (3):

| Pair witness | B | D | C |
| --- | --- | --- | --- |
| L,P | direct P | direct L | u-to-beta |
| L,R | u-to-beta | direct L | direct R |
| L,W | u-to-beta | direct L | w-to-W |
| W,P | direct P | w-to-W | u-to-beta |
| W,R | u-to-beta | w-to-W | direct R |

Each row uses two different original intervals, u at most once, w at most
once and the whole beta once. The lift hypothesis supplies actual
simultaneous routes. Add A's private beta payment. QED.

Notably U does not occur in (3): its interval exit shares the entrance of
the unconditional beta fallback, so it cannot independently add a third
payment. This does NOT say U is irrelevant to minimum cost.

A fixed choice of which source prepays the shared beta is insufficient.
For a pool confined to P and L, full payment requires C to take beta;
for a pool confined to L and R, it requires B to take beta. The choice
must remain part of the joint allocation.

## 4. Exact value and minimum link cost for EVERY Q

Let e(Q) mean Q meets P union L union R union W, and let F(Q) be (3).
For the general interface, including the private A payment,

    V(Q) = 2 + 1_e(Q) + 1_F(Q).                          (4)

**Proof.** A and one of B,C can always use their two different betas.
If e is false, all routes avoiding u have no available interval, so the
other three sources can pay only one through u. If e is true, a second
residual payment is possible: use a P unit for B and beta for C; an L unit
for D and beta for B; an R unit for C and beta for B; or a W unit for D
and beta for B. Thus the value is at least three exactly when e holds.
Lemma (3) characterizes value four. F implies e. QED.

To give a complete exact cost formula, subtract A's mandatory cost one.
For each attained residual value, the minimum cost is the smallest row
cost whose test below holds. Tests at a row are joined by OR. These tests
use the available sets, with original identities counted once.

| Residual payments V-1 | Cost | Availability test |
| --- | ---: | --- |
| 1 | 0 | Q meets P union L union R |
| 1 | 1 | Q meets U union W |
| 1 | 2 | always: one u-to-beta |
| 2 | 0 | Pair(P,L) or Pair(P,R) or Pair(L,R) |
| 2 | 1 | Pair(U,P union L union R) or Pair(W,P union L union R) |
| 2 | 2 | Q meets P union L union R, or Pair(U,W) |
| 2 | 3 | Q meets W |
| 3 | 0 | SDR(P,L,R) |
| 3 | 1 | SDR(P,L,W), SDR(P,W,R), SDR(U,L,R), or SDR(P,L,U) |
| 3 | 2 | Pair(L,R), Pair(P,L), SDR(U,L,W), SDR(U,W,R), or SDR(P,U,W) |
| 3 | 3 | Pair(W,L union P union R) |

Add one to obtain the actual total link cost c(Q). At each attained value,
at least one test holds, by (4) and its proof.

**Proof of exact costs.** Each payment route has cost zero (direct), one
(interval through u or w), or two (beta through u). Each gate can be used
at most once. For one payment this gives the first three rows. For two
payments, cost zero means two direct intervals of different sources. Cost
one means one gate interval and a direct interval of a different source;
u can be assigned to B or C and w to D or C, so precisely the two Pair
unions in that row result. Cost two means beta plus an eligible direct
payment, or two interval routes through the different gates. Cost three
means beta through u and an interval through w.

For three payments, zero cost requires three direct identities. Cost one
uses exactly one gate interval: the four possible source choices give the
four listed SDRs. Cost two either uses beta plus two direct payments (B
beta leaves L,R; C beta leaves P,L), or uses both interval gates and one
direct payment (B via u leaves L,W or W,R; C via u leaves P,W). Cost three
uses beta through u, an interval through w and one direct payment, giving
the final Pair union. No higher-cost pattern is possible: there are only
two gate capacities. These are all route patterns. Every listed test
constructs the corresponding simultaneously compatible paths; every legal
packing gives one listed test at its exact cost. Taking the least feasible
cost therefore proves both the lower bound and attainment, without
inference from finite enumeration. QED.

## 5. Actual simultaneous-repair controls

The following are complete original-network values and costs. Q restricts
only interval availability; all original beta resources remain present.

| Available original Q | V/c | Meaning |
| --- | --- | --- |
| empty | 2/3 | A plus one of B,C through shared u-beta |
| one Z unit | 3/3 | B,D share one direct identity |
| two Z units | 4/3 | B,D use different identities, C takes beta |
| both X units | 3/2 | distinct identities; C's U exit conflicts with B's beta entrance |
| both Y units | 3/3 | separate u,w units still cannot provide three residual paths |
| two W-only units, (9,8),(9,9) | 3/4 | two distinct units still share one w entrance |
| one R and one P-only, (12,7),(6,15) | 3/1 | B,C direct, but D has no reachable available interval |
| one L-only and one R, (7,5),(12,7) | 4/3 | B takes beta; D,C direct |
| one L-only and one W-only, (7,5),(9,8) | 4/4 | B beta, D direct, C through w |
| all original intervals | 4/1 | distinct P,L,R direct payments; A private beta |

For the two-X pool, a matching of sources to individually reachable sink
resources would incorrectly permit B->beta, C->one X, D->the other X.
Both the beta path and C's X path must enter u. This is a physical, fully
frozen example of a reachability matching failing to lift to simultaneous
routes, even with different original units. For the W-only pool the two
cheap interval payments instead conflict at w. These are distinct failures.

The two actual switches keep T, P, |M|, I, b,k and I+b-k unchanged.
Beta-only payment falls 4 to 2; full availability remains complete, with
cost 2 before and 1 after. Thus unchanged beta COUNT cannot justify unchanged
beta PAYMENT, and two available units cannot be counted as two repairs
without the joint criterion (3). The numerical target is not contradicted.

## 6. Verification and formal scope

The permanent fixture and verifier reconstruct the two actual surgeries,
all 308 strict freezing witnesses, all source-reachable original paths,
whole supports, interval identities and the no-fork assertion. All 12,430
actual availability models pass, including capped incidence-class controls,
every original singleton/pair and random larger pools. There are 256
independent ordinary/full primitive comparisons, 128 independent abstract
route comparisons, 1,280 arbitrary-support abstract controls and four frozen
reflections. The all-Q theorem and exact costs are proved above, not inferred
from those computations.

[TwoGateRematchingRepair.lean](../formal/SubQuorum/TwoGateRematchingRepair.lean)
proves (3) for arbitrary identity types and arbitrary support predicates.
Its route constructors encode the actual source choices, both shared gate
capacities and pairwise original-unit nonreuse. It also proves the gate-only
obstruction and the two-distinct-shared-direct-unit sufficiency. These are
general symbolic theorems, not just checks of the concrete board.

[DoubleSquareSwitch.lean](../formal/SubQuorum/DoubleSquareSwitch.lean)
checks actual geometry, inductive complete freezing of the NEW matching for
all 308 endpoints, eight disjoint alternating strands, their terminal types
and the retained physical tip adjacencies. The old owner C4 is not asserted.
The physical full-network support/reachability adapter and exact-cost/value
formulas remain written/Python, not end-to-end Lean allocation theorems.
All eight audits completed locally under Lean 4.33.0 with exit zero, using
only propext/Quot.sound and no sorry/native evaluation. The
[formal receipt](../output/interacting-square-switches-formal-check.json)
and [computational receipt](../output/interacting-square-switches-validation.json)
record the exact counts and scope.

The next substantive question is how arbitrary interacting rematching
changes the joint cut, including gates on longer shared chains. Full
compensation from freezing and the resulting universal 5/6 improvement
remain open; separate copies or a finite switch scan do not settle them.
