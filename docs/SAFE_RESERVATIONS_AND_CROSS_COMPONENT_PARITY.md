# Safe reservations and cross-component parity compensation

20 October 2026. This note gives an exact reservation accounting identity
for the componentwise mixed strip certificate. It proves a sufficient
cross-component compensation lemma, repairs the order of two genuine
donors in the previous frozen example, and refutes a tempting stronger
rule that counts parity gains from every component. It preserves an
existing coverage certificate; universal grid coverage remains open.

The later [local-quota and frozen-batch note](LOCAL_QUOTA_CUTS_AND_FROZEN_BATCH_OBSTRUCTION.md)
shows why the safe order in Section5cannot be generalized: a wider
fully frozen two-leg family has exactly two current donors, and every
nonempty subset, including the complete batch, lowers the mixed score.
The sufficient theorem below remains valid with its explicit hypotheses.

## 1. Fixed physical resources and assumptions

Use the original endpoint-free tiles of the disjoint 2-by-2 tiling of a
feasible selected/matching configuration. Retain their original maximal
horizontal and vertical runs throughout all reservations. A tile has
original capacity d_Q = 2-|T intersect Q| in {0,1,2}. Previously reserved
distinct physical slots have total B. Let G be the incidence multigraph
of the remaining slots: each slot joins its tile's two original runs.
The new batch A consists of t distinct slots of G. Delete precisely A
to obtain G'. Thus old reservations, A and the remaining slots are
pairwise disjoint. No geometric donor assertion is required for this
resource theorem. An application using owned donors must independently
establish their validity and distinctness.

For each old positive-capacity connected component C, write

    e_C = |E(C)|, v_C = |V(C)|,
    K_C = min(e_C,v_C),
    o_C = number of odd-degree vertices,
    W_C = sum_v floor(deg_C(v)/2) = e_C-o_C/2,
    F_C = max(K_C,W_C), F = sum_C F_C.

After deleting A_C = A intersect E(C), let t_C = |A_C|. C may split.
Use F'_C to mean the SUM of the mixed scores of its remaining components,
K'_C the sum of their ranks, and W'_C the sum of their half-capacity
scores. Count o'_C over ALL old vertices of C, including newly isolated
ones with degree zero. Isolates contribute no credit. Then

    F' = sum_C F'_C,  t = sum_C t_C,
    W'_C = (e_C-t_C)-o'_C/2,
    F'_C >= K'_C,  F'_C >= W'_C.                       (1)

All these quantities refer to resource components, not receiver
components. Deleting slots cannot merge two old resource components.

The two allocation facts used here have general proofs. A connected
incidence graph has one-request-per-run rank min(v,e): a rooted spanning
tree pays every vertex except its root, and, if an extra edge exists,
a spanning unicyclic subgraph pays all vertices by orienting its cycle
and the attached trees. A tree has only v-1 slots, proving the converse.
For W, any subset of request copies supported on runs S has at most
sum_{s in S} floor(deg(s)/2) requests. This is at most the number of
distinct slots incident with S, since a slot has at most two ends in S.
Hall's theorem supplies distinct slots. Choosing the better complete
rule separately in each component therefore realizes F, and likewise F'.
These facts are also developed in COMPONENT_MIXED_STRIP_COMPENSATION.md.

## 2. Exact compensation identity

Fix the old branch choice BEFORE deleting A:

    J = {C : W_C > K_C}.

Ties use the rank branch. More generally, a fixed choice attaining F_C
at a tie also works, but it must be used consistently in every term.
Do not recompute J from the new components.

Define the counted odd totals and recovery surplus by

    O = sum_{C in J} o_C,  O' = sum_{C in J} o'_C,

    s_C = F'_C-W'_C                    if C in J,
          t_C+F'_C-K_C                 if C not in J,
    S = sum_C s_C.

**Theorem (exact non-reusing reservation accounting).** Every s_C is
nonnegative, and, with B' = B+t,

    2[(B'+F')-(B+F)] = 2S+O-O'.                         (2)

Consequently

    B'+F' >= B+F  iff  O' <= O+2S.                      (3)

In particular, the aggregate parity condition O' <= O is sufficient.
It allows a parity loss in one old weighted-branch component to be
offset by a parity gain in another such component.

**Proof.** Take an attaining old K_C allocation and delete its assignments
to slots in A_C. At most t_C requests are lost, and the remaining
assignments form a feasible one-request-per-run allocation in C-A_C.
Since the exact remaining rank is K'_C, this proves

    K_C <= t_C+K'_C <= t_C+F'_C.                         (4)

Thus s_C >= 0 for a rank-branch component, where F_C = K_C, and its
contribution to the score change is exactly s_C.

For a weighted-branch component, F_C = W_C. Both old and new degree
sums count each slot twice. Therefore

    2W_C+o_C = 2e_C,
    2W'_C+o'_C = 2(e_C-t_C),

so

    2(t_C+F'_C-F_C) = 2(F'_C-W'_C)+o_C-o'_C.            (5)

Here s_C = F'_C-W'_C >= 0 by (1). Sum the rank identity and (5) over
the partition into OLD components. Old selected branches sum to F,
remaining child scores sum to F', and removed slots sum to t. This
gives (2); (3) and the sufficient condition follow. QED.

**Why there is no repeated use of a surplus.** A removed physical slot
belongs to exactly one A_C and contributes one unit to t, once. Remaining
components use disjoint remaining slots; inside each, choose one complete
allocation, never the sum of both rules. Each old component contributes
exactly one s_C and, only for its fixed weighted branch, one signed
parity change. S is an algebraic difference between these budgets, not
a second allocation of their physical slots. In particular, a parity
decrease in a rank-branch component is not additional compensation.

The simpler O' <= O test is sufficient, not necessary: recovery surplus
S can pay a parity increase. A failed sufficient test is therefore not
a counterexample to monotonicity; (3) makes the distinction exact.

## 3. Safe reservation corollaries

1. A single-slot deletion is safe if its old component uses rank, or
   at least one of its two endpoints has odd degree. In the second
   case the odd count stays unchanged or falls by two.
2. Reserving both residual slots of a capacity-two tile is always safe.
   Both endpoint degrees fall by two, so their parities stay unchanged,
   even if the old component splits after the deletion.
3. A batch whose removed subgraph has even degree at every run is safe.
   It preserves all run parities. More generally the aggregate test in
   the theorem permits compensating changes across old weighted components.
4. If rho <= B+F was already proved from the original corrected receiver
   ledger, a safe batch preserves rho <= B'+F'. Both budgets use at most
   the original total capacity D, so the corresponding original target
   |T|+|M| <= mn/2 remains certified. The lemma does not establish the
   initial inequality rho <= B+F or a safe ordering for arbitrary donors.

The unit-deletion endpoint test concerns degrees immediately before the
step. It must be applied anew for each step, with that step's old branch
mask. For a simultaneous batch use the mask before the whole batch.

## 4. Strict cross-component improvement and a false stronger rule

Tile coordinates below begin at zero. Every unlisted tile has capacity
zero. All original horizontal/vertical runs are retained through the
zero-capacity tiles.

**Valid cross-component compensation.** On a 3-by-5 tile array, put
capacity two at (0,0),(0,1),(0,2). Component A is a doubled three-leaf
star with e=6,v=4,K=4,W=F=6,o=0. On rows 1,2 and columns 3,4 put

    1 2
    2 2

to give component B with e=7,v=4,K=4,W=F=6,o=2. Both components use
the weighted branch. Remove one slot from (0,0) and one from (1,3).
For A, F falls to 4 and o rises to 2, so reserving its slot alone loses
one budget unit. For B, F remains 6 and o falls to 0, so reserving its
slot alone gains one unit. Overall O=O'=2, S=0, F=12, F'=10 and t=2.
The combined budget stays 12. The componentwise nonincrease-of-odd-count
condition fails on A, but the new aggregate lemma certifies the batch.

**False rule: count odd vertices over ALL components.** On a 2-by-4
tile array keep the same doubled star in row 0, columns 0,1,2. Put a
single slot at (1,3), forming a separate single-edge rank component
with K=F=1,W=0,o=2. Remove one star slot at (0,0) and that isolated
edge. The total odd count stays two: the star goes 0 to 2 while the
single edge goes 2 to 0. Nevertheless F=7, F'=4 and t=2, so the
combined budget falls from 7 to 6. Only the star belongs to J, giving
O=0,O'=2,S=0, exactly predicting the loss in (2). Using the other
component's parity decrease would count a credit already spent through
its rank allocation and reservation.

Both arrays are realized by independent selected vertices with empty
matching on a 6-by-10 or 4-by-8 vertex rectangle: in each tile select
2-capacity vertices from its same global checkerboard diagonal. The
checker reconstructs actual maximal runs and confirms these budgets.
Their receiver charge is zero. They establish the resource accounting
and refute the stated parity rule, not a grid bound or an owned-donor
coverage claim. The next example uses genuine frozen owned donors.

## 5. Repair of the actual frozen-donor obstruction

Use two_leg_case(6,4,6) from check_two_leg_corner_obstruction.py. It is
the 8-by-8 configuration in section 5 of the preceding mixed note:
20 endpoints, 12 selected vertices, ten matching edges, corrected
receiver charge one, total endpoint-free capacity 11. Its retained
witness certificate excludes every simultaneous mixed promotion bundle.

There are distinct same-owner saturated-endpoint donors of capacity one:

| Tile | Selected vertex | Anchor endpoint | Guard endpoint |
|---|---|---|---|
| (1,1) | (3,2) | (3,1) | (1,3) |
| (1,2) | (3,5) | (3,6) | (1,4) |

The old connected resource graph has F=10,o=2. Reserving the right
donor alone leaves F=8,o=4, giving B+F=9: the published failure of
unrestricted reservation monotonicity. Reserving the left first leaves
F=9,o=2 and B+F=10. Then reserving the right gives F=8,o=2,B+F=10.
Reserving both as a simultaneous batch also leaves the score at ten.
All these steps and all eight physical symmetries are checked with
the original ledger and frozen feasibility. This is a safe order and
batch for these two donors, not an existence theorem for every donor set.

## 6. Validation, search scope and the remaining target

Run from the repository root:

    python3 develop/check_safe_strip_reservations.py --output output/safe-strip-reservations-controls.json
    python3 develop/check_component_strip_certificates.py --output output/component-strip-certificates-controls.json
    python3 develop/check_strip_rank_search.py --output output/strip-rank-search-positive-controls.json

The reservation checker tests all 46,656 capacity/removal vectors on a
2-by-3 tile array. Each tile has six possible pairs 0<=after<=before<=2.
It checks the exact handshake identity, old-component splitting, rank
deletion bound, nonnegative recovery, equality (2) and exact criterion
(3). There are 36,338 parity-certified transitions, zero certified
decreases, 2,223 actual decreases, 8,095 further nondecreasing transitions
paid by recovery, and 1,458 full two-unit tile removals, all safe. This
small array contains no strict aggregate-vs-componentwise improvement;
the explicit larger positive example supplies that separate control.

SafeStripReservations.lean gives ten Std-only Lean declarations for
old branch optimality, local and arbitrary-list exact accounting, the
aggregate sufficient condition, the necessary and sufficient criterion,
and preservation of existing coverage. The graph-to-count adapter,
Hall feasibility, physical geometry and donor hypotheses are proved
in writing and checked computationally; they are not asserted to be
formalized by those arithmetic declarations.

They compile locally with Lean 4.33.0. The individual axiom audit uses
only propext and Quot.sound, with Classical.choice additionally used by
the exact preservation criterion; no sorryAx or native_decide is used.
The execution and audit receipt is
output/safe-strip-reservations-formal-check.json. For source checking,
run the following with formal as the working directory and that toolchain:

    lean SubQuorum/SafeStripReservations.lean

The search control additionally requires z3-solver. It was rerun in the
existing local search environment using Z3 5.3.1; the other two Python
checkers need only the standard library.

The separate discovery encoding now imposes the first mixed resource
obstruction directly: five or six remaining slots, exactly four active
original runs and W<=4. Multiplicity at most two makes these conditions
equivalent to a single four-vertex component of mixed score four. The
encoding agrees with the independent allocator on all 729 patterns,
accepting exactly 60. Frozen 8-by-10 and 10-by-12 searches and a relaxed
single-terminal 8-by-10 search returned UNKNOWN (timeouts), not UNSAT.
These searches additionally require original charge five, no previous
reservations and no donor from the four existing corner rules. They
do not settle arbitrary residual-charge-five configurations.

The next geometric target remains: realize a fully frozen configuration
whose actual corrected charge exceeds its mixed budget, starting with
the classified charge-five shapes, or prove the geometric exclusion
that makes coverage universal. The present theorem repairs reservation
accounting and proves precise cross-component compensation. It gives
no unconditional numerical improvement to the existing five-sixths
bound and does not settle the grid triple equality.
