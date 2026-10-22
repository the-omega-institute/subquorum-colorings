# Actual rematching removes the cycle-only orientation obstruction

## Cycle normalization

Fix a feasible grid pair (T,M), its actual endpoint set P, and the
auxiliary matching A of vertical PP pairs in a matching-closed aligned
packet. Every A edge is also a legal grid edge on P. Retain actual and
auxiliary edge multiplicity. Let C be any union of cycle components of
M union A. Replace the actual matching inside C by the A edges there:

    M* = {e in M: V(e) disjoint from V(C)} union A|C.       (1)

**Normalization theorem.** M* is a perfect matching on exactly P, every
new actual edge is a legal grid edge, and (T,M*) is feasible with the same
objective, endpoint labels, interval identities and physical surplus.
Every original open M union A path is unchanged. Inside C, M* union A
is a union of two-edge cycles, one per original auxiliary pair. In
particular k,b,g and the packet ledger S_J-B=|I|+b-k are unchanged.

Proof. Each original cycle is closed under both matchings. Its A edges
cover every vertex once and are legal actual edges. Distinct cycles have
disjoint vertex sets, and no actual edge connects a cycle to its exterior.
Thus (1) is a matching covering all original endpoints exactly once.
Selections and the occupied endpoint set do not change; feasibility at
every selection depends only on T union P, so remains valid. The number
of actual edges is |P|/2. Every changed region is inside the packet, so
matching closure is retained. A new actual edge coincides with its A edge
and forms a two-edge cycle. Nothing on an original open strand changes.
All ledger identities follow from these unchanged data. QED.

This is an actual matching exchange, not merely an auxiliary surgery.
Fixed-matching freezing certificates need not survive in general. If the
starting pair is exchange-terminal in the sense of
REMATCHING_NORMALIZATION_AND_RECEIVER_FLUX.md, every actual matching on
its endpoint set is terminal, including M*. Otherwise new promotions
after normalization are possible and may be used by the existing
objective-preserving normalization; their accounting is a separate step.
No assertion of freezing invariance for an arbitrary fixed matching is made.

**Uniqueness corollary.** If G[P] has a unique perfect matching, every
original PP alternating cycle has two edges. Otherwise (1) applied to a
cycle of length at least four changes its actual matching to A and gives
a second perfect matching. This explains why the earlier unique-matching
physical controls have no nontrivial shared-cycle obstruction.

## Complete simultaneous compensation through normalized cycles

Select r distinct original alpha paths and r distinct original beta
paths. Suppose there are r vertex-disjoint simple A-augmenting paths,
each from one selected alpha's TP to one selected beta's BP, with each
selected source and donor used exactly once. Require every internal
vertex of every augmentation to lie on original cycle components of
M union A. Let C contain all those touched cycles. Every new auxiliary
edge must have a legal declared geometric witness that remains valid
when actual matching changes inside C; dependence only on T,P,A and
the original unchanged open paths is sufficient.

Normalize M inside C by (1), then toggle the augmentations in A to get N.

**Cycle-only simultaneous compensation theorem.** The resulting actual
and auxiliary matchings satisfy

    alpha_(M*,N)=k-r,
    beta_(M*,N)=b-r,
    mixed_(M*,N)=g+r.                                  (2)

All original PP vertices remain auxiliary-covered, equal numbers of
original TP and BP ends are newly covered, and there is no cut debt.
Unselected original open paths, their labels, and local interval-payment
certificates depending only on them and original interval units remain
unchanged. Neither distinct operations nor the normalization introduce
additional beta or interval credit.

Proof. Alternating augmentation and vertex disjointness make the toggle
a matching, preserve original PP coverage and cover precisely one chosen
TP and one chosen BP per path. An internal old A edge of an augmentation
now coincides with an M* edge. Therefore each augmentation itself is a
complete alternating connection in M* union N from its chosen TP to its
chosen BP. Attach the two unchanged original open tails: the resulting
strand joins the other TP end of that alpha to the other BP end of that
beta, and is mixed.

These r full strands are disjoint: their augmentations are vertex
disjoint, their original source and donor paths are all distinct, and
internal cycle vertices are disjoint from every original open strand.
Every normalized pair not used by the augmentations stays a two-edge
cycle. Other cycles and unselected open strands are unchanged. This
proves (2) and the old-certificate assertion. Coverage and equal removal
of signs prove the zero-debt ledger. QED.

Unlike the fixed-M coherent-orientation theorem, this statement permits
arbitrarily conflicting directions through the same original cycle.
It handles that conflict by changing the actual matching on the cycle.
It does not cover augmentations passing internally through other open
strands, source/donor reuse, or intersecting augmentations. Nor does it
prove that the required vertex-disjoint augmentations exist universally.

If the other k-r alphas have distinct old interval payments, their
payments remain valid and the familiar conditional packet bound follows:

    S_J-B=(|I|-(k-r))+(b-r)>=0.

This is the unchanged scalar ledger with a sound routing certificate;
normalization does not itself improve its numerical value.

## Effect on the all-length shared-cycle obstruction

For every cyclic word in SHARED_CYCLE_ORIENTATION_AND_COMPENSATION.md,
normalize the one original cycle. The r augmenting paths in that
construction meet all the theorem's hypotheses, regardless of the word.
All r original alpha/beta pairs therefore become mixed. The fixed-M
loss floor(r/2) for alternating words disappears completely after this
legal actual matching exchange. The obstruction refutes the fixed-M
counting rule, rather than the possibility of compensation after rematching.

## Verification scope and next obstruction

The permanent checker normalizes the actual cycles, verifies endpoint
coverage, unchanged open strands and the exact inventories, then toggles
the supplied disjoint augmentations. Abstract controls include every
qualifying small replacement used by the orientation checker and all
its cyclic-word controls. Physical controls use the existing exchange-
terminal nonunique core and elbow grafts, with symmetries and band phases,
checking feasible grid edges and complete freezing before and after the
exchange. These controls do not establish a general existence theorem.

The local run passes 11,731 complete simultaneous-compensation controls:
3,195 qualifying small replacements and 8,536 cyclic-word repairs, including
alternating words through length 128. It also checks 320 physical instances
(the core and nine grafts, eight symmetries, four phases); 80 change the
actual matching. Every physical instance is feasible and completely frozen
both before and after this particular exchange. There are 12,051 total
normalization controls and 10,549 nontrivial cycles normalized across them.

The associated Lean source proves the normalization involution, absence
of fixed points, preservation of permitted adjacency, equality to A on
the closed region and equality to M elsewhere, under the stated closure
and matching hypotheses. It does not formalize finite graph component
classification, the simultaneous route decomposition or grid witnesses.
All five named statements and their individual axiom audits pass locally
in Lean 4.33.0. The three matching/adjacency statements use no axioms;
the two simplification statements use propext. This development was added
after the initial shared-cycle orientation review request and is outside
that request's input until separately submitted.

The remaining geometric problem is now more specific: handle paths whose
interiors meet other open strands, or prove a disjoint cycle-only linkage
exists for enough demands. Shared cycle orientation alone cannot be a
permanent obstruction when the legal actual exchange is available.
Universal grid compensation, the universal 5/6 improvement and triple
equality remain open. Keep the outside-overlap correction once.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
