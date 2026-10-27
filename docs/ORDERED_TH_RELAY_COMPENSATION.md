# Ordered TH relays with a fixed actual matching

The fixed-M square lemma extends from an adjacent TT/HH pair to an arbitrary
chain of intervening TH paths. The exact extra physical cost is the M-resource
set of the two bad endpoint paths: intermediate TH resources are rearranged,
not charged a second time. There is an essential order condition on the two
contacts of each intermediate path. Under the disjoint-square hypotheses below,
that condition is both necessary and sufficient for the specified chain of
switches to turn all its paths into TH paths.

This is a sufficient certificate for grid compensation, derived from the
standard matching decomposition. It does not assert that every footprint has
such a chain, or that these switches minimize payment cost. An explicit feasible
6-by-12 example refutes dropping the order condition. An arbitrary-length
feasible family has no direct TT/HH square at its starting N, yet admits these
ordered relays. Both claims have coordinate proofs below.

## 1. Hypotheses and order of contacts

Use the setup of [fixed-M mixed terminal compensation](MIXED_TERMINAL_SQUARE_COMPENSATION.md).
M is the fixed actual matching with endpoints P. Q=V\P is partitioned into T,H.
N is an auxiliary perfect matching on all of V, allowed to touch holes.
Its superposition with M has vertex-disjoint terminal paths, internal vertices
in P, each starting and ending with an N edge. The matching statements do not
need selected-degree feasibility; the two actual grid constructions below have it.

Choose DISTINCT ORIGINAL path components

    A0 (TT), C1 (TH), ..., Cr (TH), A1 (HH),       r >= 0.

Between each consecutive pair choose a unit square whose opposite sides are
N edges, one on each of the two paths. All r+1 witness squares must have
pairwise disjoint vertex sets. Call a square's chosen old edge on a path its
contact. Thus each internal Ci has two distinct N-edge contacts.

Orient each Ci from its T terminal to its H terminal. Let out_i be the position
of its contact with the next path, and in_i the position of its contact with
the preceding path. Positions are edge indices along the original path. The
ordered-relay condition is

    out_i < in_i,     for every i=1,...,r.              (1)

In words, walking from T toward H meets the outgoing contact BEFORE the
incoming contact. These are positions on the original TH path, not an
arbitrary orientation of a component-contact graph. No condition is needed
when r=0, recovering direct TT/HH compensation.

Switch all witness squares to their other two sides, changing N to N'. The
squares are vertex-disjoint, so the switches commute and N' is a full matching.
Every old and new square edge is outside M: old edges lie on terminal paths;
new edges join two different original M+N components. In particular

    M intersect N' = M intersect N.                    (2)

## 2. Exact ordered-relay theorem

**Theorem.** Under these hypotheses, all r+2 original paths become r+2 TH paths
if and only if (1) holds at every internal Ci. Every component outside the chain
is unchanged. If (1) holds, global path-type counts change as

    (a,b,t) -> (a-1,b-1,t+2).                          (3)

The union of original physical M edges on the affected paths is unchanged,
with each edge in exactly one resulting path. Let R(A) denote the set of
actual M edges of an original path A. Comparing the TH payments before and
after the operation gives the exact additional used set

    new used-M set = old used-M set disjoint-union R(A0) disjoint-union R(A1).
                                                                    (4)

Consequently the incremental payment cost is |R(A0)|+|R(A1)|, irrespective of
how many intermediate TH paths are traversed. The endpoint paths may themselves
be arbitrarily long; (4) is not a uniform constant cost bound.

Proof of sufficiency. Process the squares in order from A0 to A1; commutation
allows this order without changing N'. Initially the active component is TT.
Suppose the active TT meets the untouched TH path Ci at its incoming contact.
Cutting both N edges splits the TT into two T arms and Ci into a T arm and an
H arm. The two square edges cross-join these arms. They create one new TT
component, formed with Ci's T arm, and one TH component, formed with its H arm.
The two resulting paths partition the original two paths, just as in the
direct TT/HH square lemma; no cycle or repeated physical edge is created.

By (1), Ci's outgoing contact lies on its T arm, so is now on the active TT.
It is untouched: the next square has disjoint support from the current one.
The next component is a fresh original TH path. This proves the induction.
At the last square the active TT meets the untouched HH path A1, yielding two
TH paths. There are r TH outputs from the r transport steps, and two from the
last compensation step, for r+2 in total. All outside components remain fixed.
This proves (3). All arms partition their old vertex and physical-edge sets;
the same property persists under this induction. Taking their disjoint union
proves resource preservation and (4).

Proof of necessity for this specified operation. Suppose (1) first fails at Ci.
All earlier transport steps are valid, so their active TT meets Ci at its
incoming contact. The new TT contains Ci's T arm. Since the outgoing contact
now lies AFTER the incoming contact in T-to-H order, it belongs to Ci's H arm,
on the other resulting component. None of the remaining chosen squares touches
the new TT: their contacts lie on that H arm or on later original components.
The earlier squares have already been used and have disjoint support. Thus
this TT is stranded and persists in the final superposition. N' does not give
all TH paths on the affected chain. Because the switches commute, reordering
these SAME switches cannot change this conclusion. QED.

The necessity statement concerns the specified original chain and witnesses.
It does not exclude different witnesses, other N, extra switches or a different
payment. The feasible example in Section 5 makes this distinction explicit.

## 3. Several chains: the shared component constraint

Suppose s such ordered chains have pairwise disjoint ORIGINAL component sets.
Their supports and resource sets are disjoint, so they can be processed together:

    (a,b,t) -> (a-s,b-s,t+2s),
    unpaid T = 2(a-s), unused H = 2(b-s).              (5)

The TH payment cost increases by the sum of |R(A0)|+|R(A1)| over the chains.
Every summand refers to a different original bad path; old TH resources occur
once in the single final payment, not once per contact or per chain traversal.
If the chains cover all original TT components, then a<=b and

    J = area/2-(b-a),
    |T|+(5/6)|M| = area/2-(b-a)-|M|/6.                (6)

Thus chain coverage is a sufficient condition extending direct-square Hall
coverage, with the same exact numerical margin. Universal chain coverage and
the universal 5/6 improvement remain open.

A coarse graph connecting TT to HH whenever some component chain exists is
insufficient: it forgets (1), and a matching of its edges can reuse the same
intermediate TH component. Our theorem requires actual, ordered witnesses and
disjoint original components. It does not justify a Hall assertion on that
coarse reachability graph. More permissive reuse of portions of a TH component
would require a new proof with its physical subpaths and capacities explicit.

## 4. Arbitrary-length feasible grid relays with no initial direct repair

For any r>=1 take the (2r+2)-by-4 grid, rows 0,...,2r+1. Put an actual edge
(0,1)--(0,2) in the first row. For i=1,...,r put the vertical actual edge

    (2i-1,2)--(2i,2).

Select T={(0,0),(0,3)} union {(2i,3):1<=i<=r}; all other non-P sites are H.
The selected top corners each see their one P neighbour. Every other selected
vertex sees its P neighbour at column 2 and holes above and below. Hence the
configuration is feasible for every r.

Choose auxiliary N as follows:

* top row: (0,0)--(0,1), (0,2)--(0,3);
* each band of rows 2i-1,2i: vertical N edges in columns 0,1 and one horizontal
  N edge between columns 2,3 in each row;
* bottom row: horizontal N edges between columns 0,1 and between columns 2,3.

These edges partition every row/band and form a full perfect matching. The
superposition has one TT path along row zero, r TH paths

    (2i,3), (2i,2), (2i-1,2), (2i-1,3)

oriented from T to H, two direct HH paths per band on the left, and two HH
paths on the bottom row. Its counts are

    (a,b,t)=(1,2r+2,r),
    |T|=r+2, |H|=5r+4, |M|=r+1,
    J=2r+3=area/2-(2r+1).                             (7)

There is NO initial direct TT/HH square. The TT path's two N edges are
horizontal in row zero. The only possible opposite N edge is immediately
below the right one, and belongs to C1, a TH path; below the left one the N
edges are vertical. The two top TT vertices have no square above them.

Nevertheless take the r+1 squares with top-left corners (2i,2), i=0,...,r.
They are vertex-disjoint, connect TT,C1,...,Cr,HH on the right, and have outgoing
and incoming edge positions 0 and 2 on each internal Ci. The theorem applies.
The final counts are (0,2r+1,r+2), paying every T. The old TH payments use r
actual edges; the final payments use r+1. A single final payment from (0,0)
travels through all original P vertices to (2r+1,2), has length 2r+3 and uses
all r+1 actual edges once. The other r+1 payments are adjacent right-column
pairs. Thus the incremental cost is exactly ONE, consistent with (4).

For q>=1, place q copies side by side with offsets 6j, j=0,...,q-1,
separating consecutive copies by two all-H columns. Pair each gap column
vertically in N. The full rectangle has height 2r+2 and width 6q-2. Gap sites
are unoccupied, so no selected degree increases. Each copy retains exactly its
original terminal paths, and the gap edges are additional HH components.
The q relay chains have disjoint original component sets and add exactly q
actual edges to the old TH payment cost qr, producing cost q(r+1). Counts
change from (q,(2q-1)(2r+2),qr) to
(0,(2q-1)(2r+2)-q,q(r+2)). This proves a two-parameter actual realization of
the packing statement; the gap creates no extra credit.

This is not a minimum-cost example: (0,0)->(1,0), (0,3)->(1,3) and
(2i,3)->(2i+1,3) give complete disjoint adjacent payments, of actual cost zero.
The family establishes a nonvacuous arbitrary-length extension beyond the
initial direct-square operation class, not a lower bound on unrestricted cost.
Its exact weighted margin from (6) is 2r+1+(r+1)/6.

## 5. A feasible wrong-order obstruction with two disjoint actual squares

On the 6-by-12 grid let the following three vertex sequences be original
terminal paths:

    A (TT): (1,1),(1,2),...,(1,10),
    C (TH): (4,3),(3,3),(2,3),(2,4),(2,5),
            (2,6),(2,7),(2,8),(3,8),(4,8),
    B (HH): (3,5),(3,6).

On each path take edges in positions 1,3,5,... as the actual M edges and
positions 0,2,4,... as N edges. This gives eight actual M edges. Select

    T={(1,1),(1,10),(4,3)}.

All other non-P sites are H. Each selected vertex has just its one P neighbour,
so the actual full-grid configuration is feasible. Complete N on the remaining
50 vertices by the explicit 25 HH edges listed in the checker/output record.
These pairs can be checked individually; no solver or existence assumption
is needed. There are no other selected endpoints, so (a,b,t)=(1,26,1).

Use the square at (1,3) between A and C, and the square at (2,5) between C and B.
They have disjoint vertex sets and each uses opposite original N edges.
Along C from T to H, its incoming contact (2,3)--(2,4) has position 2, whereas
its outgoing contact (2,5)--(2,6) has position 4. This is the WRONG order.

After the first switch the new TT has endpoints (1,1),(4,3). The outgoing
contact lies on the other new path, with endpoints (1,10),(4,8). The second
switch therefore acts on TH and HH; it cannot touch the stranded TT. Its
outputs have endpoints (1,10),(3,5) and (3,6),(4,8), of types TH and HH.
All other components stay unchanged. Final counts remain (1,26,1).

This is an actual feasible grid counterexample to deleting (1) from the
specified-chain rule. It refutes neither complete-payment existence nor the
numerical target: three disjoint adjacent payments to (0,1),(0,10),(5,3)
use zero actual M edges, and J=11<36=area/2. Different squares or a different
certificate are not excluded.

## 6. Verification and open work

The [standalone relay checker](../develop/check_ordered_th_relay.py) checks
original contact ownership, vertex-disjoint square supports, all port orders,
the active TT induction, commutation, physical edge-set preservation, exact
counts and disjoint payments. It checks 80 actual family lengths, 40 actual multi-chain packings and the full
wrong-order board; [the output](../output/ordered-th-relay.json) includes the
complete negative witness. Matching-only exhaustive 2-by-4 controls include
both orders; feasibility is not assumed for those tiny controls and is checked
separately on both coordinate constructions above. A later local supplement
checks all 510 contact-orientation words at r=1,...,8 (eight successful words,
502 stranded-TT words); these additional controls were not in the initial
independent-review attachment. They also impose no selected-degree feasibility.

The arbitrary-length sufficiency, necessity and chain-packing statements are
written proofs. Finite controls do not supply general chain existence or a
numerical inequality beyond (6). The open problem is to find useful geometric
conditions guaranteeing component-disjoint ordered chain coverage, or extend
the surgery to shared TH subpaths with an honest capacity ledger.

The preceding independent ACCEPT covers the earlier square/retention and all-k
relay-cost notes. A separate review of this new ordered-relay result is recorded
below. The submitted manuscript,
Mail, public main/PR3, star-forming/C4 and shared CI are outside this branch.

[Seven local Lean declarations](../formal/SubQuorum/OrderedTHRelay.lean), with
[execution and axiom audit](../output/ordered-th-relay-formal.json), verify that
four-arm resource-list reconnection preserves permutation, that any finite
sequence of such abstract surgeries preserves resource uniqueness (Nodup), and
the exact conditional cost/residual/family arithmetic. These lists enumerate
physical resources; they are not ordered vertex walks. The geometric adapter,
port-order iff statement and coordinate constructions remain written proofs.

[Independent review ACCEPT](../output/ordered-th-relay-review.json) covers the
full written theorem and coordinate constructions. The reviewer executed the
submitted checker (80 lengths,40 packings,32 tiny matching controls and the
negative witness), reproduced the submitted JSON, and did not run Lean. The
later 510 orientation-word checks and direct payment-resource-set assertion
are local additions, not reviewer-executed. The latter implements the review's
suggestion to check (4) directly, including pairwise disjointness; the local
checker was rerun after adding it. No mathematical statement changed.
