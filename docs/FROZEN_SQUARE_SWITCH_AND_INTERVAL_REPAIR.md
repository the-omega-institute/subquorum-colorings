# Frozen square switch: beta-only loss and exact original-interval repair

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

One actual2x2 matching switch defeats the beta-only conclusion of the
[persistent cycle core](PERSISTENT_MIXED_CYCLE_BETA_CORE.md) if its matching-
retention hypothesis is dropped. The actual selected and endpoint sets
remain EXACTLY unchanged, and the new matching is completely frozen.
Alpha/beta counts and every original interval identity are unchanged too.
Nevertheless the complete original network's beta-only value falls4->3.

The missing payment is restored by specific unchanged original intervals
whose owner has changed. We prove the full value and minimum-link formula
for EVERY subset of final original intervals, including exact distinct-unit
and shared-entrance corrections. This refutes beta-only persistence under
rematching, not the grid inequality: full interval availability still pays
all four at cost2. No universal5/6 improvement is claimed.

## 1. Actual frozen switch with no occupied-site changes

Start with the actual28x24,49T/154M/308P mixed-cycle fixture. Replace

    (5,4)--(6,4), (5,5)--(6,5)

by

    (5,4)--(5,5), (6,4)--(6,5).                            (1)

Every other actual matching edge and ALL selected/endpoint sites are
unchanged. The four sites are distinct; each replacement is a physical
grid edge. It is a perfect matching on exactly the same endpoint set.
Feasibility depends only on the occupied and selected sets and is therefore
unchanged. Complete freezing is NOT invariant under arbitrary square
switches: the new fixture supplies its own strict rank certificate for ALL
308 endpoints. Induction on these ranks proves actual complete freezing.
The new certificate, actual strand paths and terminal types are checked in
Lean; no search-completeness or bounded-depth inference is used.

The two switched old edges belong to the left alpha D (TP ends5,4/24,4)
and mixed g0 (BP5,5/TP14,11). Cutting them separates their two tip vertices
from the remaining tails. The new upper edge forms the short mixed

    f: TP(5,4) / BP(5,5),

and the new lower edge joins the two remaining tails into the new alpha

    D': TP(24,4) / TP(14,11).

This is the elementary alternating-strand switch: original bodies
D union g0 split into the two-point f and its40-point complementary alpha
body. Other original owners are unchanged. Thus there are still4 alphas,
6 betas and15 mixed paths. The former four-source source/gate cycle is
not retained: the physical TP--BP contact(5,4)->(5,5) is now a self-link
within f. It must not be described as a different four-source realization
of the same C4. The set of physical TP/BP sites and their horizontal
adjacencies remains the same; their owner partition changes.

## 2. Every original interval stays; its whole owner can change

T,P and their band labels are unchanged. Original interval identities,
standard boundary marks and the eligible interval set I are consequently
identical before/after (1). No interval is consumed or created. The gap
boundary witnesses of old D and g0 all lie on the new long D' body, and
none lies on the short f. Therefore exactly

    W(D') = W(D) union W(g0),       W(f)=empty.              (2)

This identity is established by tracing the actual retained gap boundaries,
not by summing two overlapping inventories. All other owner supports stay
unchanged. In particular the gate0-supported original units that were
previously reached by a link now belong directly to D'.

Let A,B,C be the unchanged top, right, bottom alpha sources. A and B still
have empty direct whole support. They have distinct exclusive beta options
of cost1, at(5,17)->(5,16) and(5,19)->(5,20). No route from C or D' enters
either beta or the other source's private branch. Any payment of A or B
needs at least one link. Thus a minimum-cost maximum packing can prepay A,B
at total cost2, releasing any old gate/interval use without raising cost.

All remaining original beta exits and intermediate owners are retained.
The COMPLETE source-reachable classification for C,D' is:

* D' has direct support L, or takes one link into g3 with support W.
  Its other outgoing mixed tail has empty support and no continuation.
  It reaches NO whole beta, along paths of any length.
* C has direct support R; one-link g2 support U or g3 support W; and a
  two-link beta fallback through g2 to bC, of cost2 independently of Q.
* g3 has no further link, while g2's only further link is to bC. The
  body intervals of bC are already in W. Any two alpha arms reaching bC
  would both traverse the same g2 entrance, so no beta fork is possible.
  Every other beta has only one reachable alpha. Ordinary/full optima agree.

The coordinate classes are

| Class | Original units (band,column) | Count |
| --- | --- | ---: |
| L, direct D' | band5 cols10,12; band6 col12; band7 cols5..7,9,10,13,15; band8 cols5,7..11 |16|
| R, direct C | band12 cols7,12..16 |6|
| U, gate g2 | band7 cols13,15; band9 cols13,14 |4|
| W, gate g3 | band9 cols8..10,13,14; band10 cols12..15 |9|

R is disjoint from the other three classes. L intersect W is empty.
The only overlaps are

    X=L intersect U = {(7,13),(7,15)},
    Y=U intersect W = {(9,13),(9,14)}.                      (3)

L also shares some units with g1, reachable by A/B; their private beta
prepayment frees these units. 'Direct' here does not mean exclusive to
one original owner. All identities in (3) are counted once.

## 3. Exact value and cost for every original available subset

For sets E,F write Pair_Q(E,F) if there exist different original units
e in Q intersect E and f in Q intersect F. Two nonempty sets are NOT
enough when they contain just the same one available original unit.
Let l,r,u,w mean that Q meets L,R,U,W respectively, and put

    h = 0 if r, else1 if u, else2.

**Theorem (complete original network, all Q).** For BOTH ordinary and full
fork compensation,

    V(Q) = 3 + 1_(l or w).                                 (4)

If neither l nor w holds, c(Q)=2+h at value3. Otherwise full value4 holds,
and its exact minimum link cost is

| Available classes | Exact c(Q) |
| --- | ---: |
| r and l |2|
| r, no l, and w |3|
| no r, l, and Pair_Q(L,U union W) |3|
| no r, l, and NOT that distinct pair |4|
| no r, no l, w, and Pair_Q(U,W) |4|
| no r, no l, w, and NOT that distinct pair |5|

**Proof of value.** The A,B beta prepayments leave C,D'. C always has its
fixed two-link beta route. D' can be paid exactly when an interval of L
or W is available, since these exhaust its reachable supports and it has
no beta. A direct L route, or one-link g3 route to W, is disjoint from
C's g2/bC fallback and uses no competing interval. This attains four iff
l or w; otherwise precisely A,B,C can be paid. QED.

**Proof of cost.** A,B cost at least2 and their private routes attain it.
If D' is unpaid, C's cheapest route has cost h, proving2+h. At value4,
if r holds then C can take a distinct direct R unit at zero links; D'
costs0 with L or1 with W. These are the first two rows, with obvious
source-specific lower bounds.

Without R, C needs at least one link. If L is available, paying D' directly
costs0. Achieving combined C,D' cost1 requires a different unit for C in
U union W, precisely Pair_Q(L,U union W). These assignments use different
gates because D' is direct. If that fails, total cost cannot be1; C's beta
fallback plus direct D' attains2. Thus c is3 or4 as stated.

Finally if L,R are absent, D' must use g3 at cost1. C CANNOT also use g3,
even if two different W units are available: g3 has capacity one. Combined
cost2 is possible exactly by C->g2->u and D'->g3->w with DIFFERENT original
units, i.e. Pair_Q(U,W). Otherwise C must use its beta fallback, costing2,
and D' costs1. This is compatible with all other routes, proving c4 or5.
The reachable classification excludes all other primitives, including
forks; these lower bounds and simultaneous witnesses are exhaustive. QED.

## 4. Distinct-unit and shared-gate corrections are different

All entries here retain EVERY original owner, beta and actual link.

| Available original Q | V / c after switch | Reason |
| --- | --- | --- |
| empty |3/4| D' has no beta route |
| one X unit, e.g.(7,13) |4/4| D' and C cannot both spend that unit |
| both X units |4/3| direct D' and g2 C use different original identities |
| one Y unit, e.g.(9,13) |4/5| g2/g3 routes compete for that one unit |
| both Y units |4/4| different gates and different units suffice |
| two W-only units,(9,8),(9,9) |4/5| distinct units still share the g3 entrance |
| all original units |4/2| different direct R,L units pay C,D' |

Thus a proposed cheap repair must pass BOTH the distinct-original-unit
test and the capacity-one-gate test. A single original X or Y unit does
repair the missing VALUE, but not always the cheapest proposed cost.
Neither the rule's failure nor beta-only loss is a counterexample to the
numerical grid target: |T|,|M|,I,b,k and I+b-k are unchanged by (1).

For any q separated physical copies and any subset H of copies switched,
the same certificates, supports and routes separate by original identity.
With NO intervals,

    V_beta = 4q-|H|,        c_beta = 5q-|H|.                (5)

With all intervals, V=4q,c=2q. For arbitrary Q, sum (4) and the cost table
over switched copies and the preceding exact unchanged-board formula over
unswitched copies. Even blank buffers preserve all local band coordinates.
This is an unbounded beta-only failure at UNCHANGED numerical inventory,
with a general component proof and an explicit interval repair.

## 5. Verification, formal scope, and what remains

The permanent fixture contains all308new strict freezing witnesses. The
verifier independently reconstructs feasibility, the new ranks, all actual
original owners/links/supports, the square-switch surgery and unchanged
interval identities. It compares (4) and the cost table with the full
original flow and independent ordinary/full primitive packs. Literal
multi-copy boards test (5) and identity separation. All 5,626 original-availability models pass, with 280 independent ordinary/
full primitive comparisons, four frozen reflections and 36 literal frozen
multi-copy availability models. The [receipt](../output/mixed-cycle-square-switch-validation.json)
records the counts and named controls. The all-Q and all-q proofs are above, not inferred from tests.

Local Lean 4.33.0 completed with exit0. All five audited declarations use
only propext/Quot.sound, with no sorry/native evaluation. The
[formal receipt](../output/mixed-cycle-square-switch-formal-check.json) records
the scope and local preflight. The new concrete
[Lean file](../formal/SubQuorum/MixedCycleSquareSwitch.lean) checks feasibility, actual inductive complete
freezing for ALL308endpoints under the NEW matching, eight disjoint actual
strands, their four alpha/four mixed terminal pairs and the retained eight
physical tip adjacencies. It does not call those adjacencies a source/gate
C4: one is now a self-link. Exact support ownership, full reachability and
all-availability cost/value are written/Python, not end-to-end Lean flow.

The earlier persistent-core theorem remains valid under its stated retained-
matching assumption. This actual frozen switch proves that retaining T/P
alone does not suffice for its beta-only conclusion. The next task is to
control more general rematching and simultaneous interval repair, preserving
the original resource identities and entrance capacities. A full five-source
shared-resource obstruction and universal compensation remain open.
