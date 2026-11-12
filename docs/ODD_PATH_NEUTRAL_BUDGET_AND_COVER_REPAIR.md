# A shared odd-path neutral budget and exact final-cover repair

This note fixes an initial omission set and candidate replacements. In the
isolated-addition class described below, it gives an exact endpoint formula,
constructs a final minimum cover and matching without a final matching
optimizer, and selects the best batch with a conflict-cover parameter. The
first neutral deletion is charged once per initial odd path, even if many
operations share that path. Changing the final cover is essential: a uniform
physical family separates this rule from every inherited-cover certificate.

The path-matching and smaller-bipartition-side facts are elementary; no
independent novelty claim is made for them. The contribution here is the
shared budget, its exact candidate-selection rule, matching-edge ledger, and
the physical application. There is no literature-priority claim.

## 1. Setting and exact budget

Let A be a finite simple graph, U its initial omission set, and G=A[U]. Assume
G is bipartite and has maximum degree at most two. Supply an **independent
minimum vertex cover** C and a matching M0 of size |C| on G; write I=U-C and
nu0=|C|. The independent-cover hypothesis matters: an arbitrary minimum cover
need not be independent. Such a cover can always be chosen componentwise in
this graph class: use the smaller side on an odd path, either side on an even
path or even cycle, and omit isolates. This also supplies a tight matching
by consecutive pairing. Any supplied tight M0 is allowed below.

Each candidate i removes a different x_i in I and adds a different y_i outside
U. Fix a batch S, X={x_i:i in S}, Y={y_i:i in S}, U_S=(U-X) union Y. Require
that **every point of Y is isolated in A[U_S]**. The ambient A may have other
edges; only this endpoint isolation and the assumptions on G are used.

Every initial component K is either balanced, |K cap C|=|K cap I|, or an odd
path, |K cap I|=|K cap C|+1, including an isolated I-point. A C-heavy initial
path is excluded by the matching saturating C. Let O(S) count the initial
odd components that contain at least one selected removal. Then

**Theorem 1 (exact shared budget).**

    nu(A[U_S]) = nu0 - v(S),       v(S)=|S|-O(S).

Equivalently, a balanced component with t removals saves t, while an odd
component saves max(t-1,0). Thus the neutral cost is one for the entire
initial odd component touched by the batch. It is not one per candidate,
operation pair, auxiliary subregion or chosen Hall set.

**Proof.** C and I are both independent and every edge of G joins them.
On an I-heavy odd path, order from an I-end. With t>=1 removed I-points,
the t-1 internal gaps between successive deletions are nonempty C-heavy odd
paths. The two boundary pieces are empty or balanced paths. For t=0 the
original path remains I-heavy. On a balanced path order from its C-end;
when t>=1, the first boundary piece and t-1 internal gaps are C-heavy,
while the last piece is empty or balanced. On an even cycle, t>=1 deletions
leave t C-heavy gaps; with t=0 it remains balanced. These statements include
adjacent deletions on the I side (one surviving C-point between them) and
endpoint deletions (possibly empty boundary pieces). An initial I-isolate
has t=0 or1 and no saving.

On every surviving C-heavy odd component replace its C-side of the cover by
its I-side. On every other component retain C. Each replacement saves
exactly one; all surviving edges are covered. Pair consecutive vertices in
each ordered surviving path or even cycle. This gives a matching with the
same size as that cover: the smaller side on an odd path, half the order
on a balanced component. Additions are isolates and need no cover or matching
edge. The resulting matching and cover have common size nu0-|S|+O(S), so
weak matching-cover duality proves the formula. No final matching algorithm
or numerical enumeration is needed. QED.

**Corollary 2 (distinct-edge ownership).** Each unit of v(S) can be assigned
a different edge of the supplied initial matching M0 that meets X.

**Proof.** The repair regions are the vertex-disjoint final C-heavy odd
components. In each such region R, |C cap R|=|I cap R|+1. Since M0 saturates
C, some c in C cap R has its M0 mate outside I cap R. The mate cannot lie in
another surviving component, since their M0 edge would connect them; hence
it is a removed point of X. Choose one such edge for R. Different regions
have disjoint C-points; a matching edge has exactly one C-endpoint, so these
chosen edges are different. There is one region per saving by Theorem 1.
Some destroyed original edges need not be charged: this is an injective
ledger for savings, not a claim that every destroyed edge earns credit. QED.

Repair uses components after the whole batch. Counting all intervals between
arbitrary pairs of deletions would overlap; only gaps between **successive**
deletions, or equivalently the actual surviving components, are used.
The endpoint theorem does not assert a nonincreasing sequence of intermediate
matching costs. In the physical setting below every prefix is permitted,
but endpoint isolation may depend on a later prerequisite.

## 2. Exact isolation constraints and batch selection

For every candidate addition y_i inspect its initial neighbours and other
candidate additions. A neighbour x_j imposes i implies j. Any initial
neighbour not removable by the list blocks i. An edge y_i-y_j is a conflict
between i and j. Self implications are harmless. Neighbours outside U and
outside the addition list never enter the final set and impose nothing.
These conditions are necessary and sufficient for the chosen additions to
be isolated finally, since they inspect every edge with a selected new
endpoint. They impose no retirement constraints on old C-points: those are
precisely what final-cover repair replaces.

Give candidate i group g_i=K when x_i lies on initial odd component K, and
g_i=None when it lies on a balanced component. Then

    v(S)=|S|-number of distinct non-None groups represented in S.

Adding a label increases v by zero (the first in an odd group) or one.
In particular v is monotone under inclusion.

**Theorem 3 (exact parameterized optimization).** Given the groups,
implications, blockers and conflicts, and a vertex cover K of the conflict
graph, a best feasible batch, maximizing v and then minimizing operation
count, can be found in 2^|K| times polynomial time. For each fixed
intersection F=S cap K, the minimum-operation maximum-value batch is unique.
No uniqueness is claimed across different F.

**Proof.** Enumerate F subset K. Reject F with an internal conflict. Exclude
blockers, K-F and all conflict neighbours of F, then propagate exclusions
backward through implications. Reject if an F-label is excluded. All
remaining labels L are a feasible implication-closed batch with L cap K=F:
there are no conflicts outside K, and the exclusions eliminate every
conflict incident with F. Every feasible batch with that intersection is a
subset of L. Monotonicity makes L maximum-value for that intersection.

Let R contain F, all balanced labels of L, and every label in each odd group
represented at least twice in L. Take the forward implication closure of R.
It remains within L, hence is feasible. Every maximum-value subset of L must
contain R: a balanced label contributes one independently; an odd group of
size t>=2 contributes t-1, and no proper subset can retain that contribution.
All other groups of L have size one and contribute zero. The closure is
therefore contained in every maximizer and itself attains the value of L.
It is the unique smallest, hence the unique fewest-operation maximizer for
this F. Compare these solutions by value and size over all assignments.
All propagation and group counting is polynomial. QED.

Without a supplied K, endpoints of a greedy maximal conflict matching give
|K|<=2 tau, where tau is the minimum conflict vertex-cover size. This gives
4^tau times polynomial time; it is not a polynomial-time MIS algorithm.
When there are no conflicts the computation is polynomial, including
arbitrary cyclic prerequisites and blockers.

For physical helper/owner instances use A=P union Q on N=2b indexed
witnesses, where P is a partition into pairs, Q is a disjoint matching, and
B is the owner graph with path/even-cycle components. A permitted omission
U has owner complement inducing maximum degree at most one in B. Require
each candidate to replace a point inside one owner component, at most one
candidate per component, individually permitted. All batches and prefixes
are then permitted because owner components are disjoint. Theorem 1 gives
an exact cost and an actual dissociation certificate of size 3b-nu(A[U_S]).
Theorem 3 is exact **within this fixed cover/list and isolation domain**;
nonisolated additions and removals in C are outside this rule.

## 3. Uniform physical separation from every inherited cover

**Theorem 4.** For every integer r>=3 there is a bipartite, two-connected
physical graph of order 20r, minimum degree two and maximum degree three,
with only square owner components, a minimum-cardinality permitted initial
omission U, and r individually permitted candidates on different owners,
such that

    best inherited-cover cost = 2r-2,
    exact fixed-candidate-list endpoint minimum = r-1.

The first minimum allows all initial minimum covers and maximum matchings,
including the preceding mixed-removal rule. The second minimum permits the
final cover to change. The improved certificate has size 11r+1. This is a
lower certificate for the physical all-helper value, not an assertion of
its unrestricted exact optimum.

**Construction.** Set N=8r, b=4r, with indices modulo N. Let P be the even-odd
edges (0,1),(2,3),..., and Q the complementary odd-even cycle edges,
including (N-1,0). Thus A=C_N. Give index v physical colour floor(v/2) mod2:
P pairs have the same physical colour and Q pairs have opposite colours.
These colours are distinct from the auxiliary C/I bipartition. Set

    U={1,...,4r-3} union {4r,4r+4,4r+8},
    C={2,4,...,4r-4},      M0={(1,2),(3,4),...,(4r-5,4r-4)},
    x_j=4j+1,             y_j=4r+2+4j,       0<=j<r.

G=A[U] is one path of order 4r-3 and three isolates; its unique minimum
cover is C and nu0=2r-2. Every x_j has physical colour0, every y_j colour1.
Every new y_j is isolated from U and from the other y's in A; it stays
isolated for every batch.

Here is an explicit deterministic square-owner construction. After setting
aside X={x_j} and Y={y_j}, the remaining U contains r+2 points of physical
colour0 and 2r-2 of colour1. The remaining outside contains r+2 of colour1
and 2r-2 of colour0. Pair sorted U-colour0 points to sorted outside-colour1
points; then pair sorted U-colour1 to sorted outside-colour0. This gives
3r disjoint opposite-colour (u,z) pairs. For the first r pairs make a square
containing x_j,y_j,u,z in that alternating colour order, exchanging u,z
when necessary. Group the remaining 2r pairs in twos and order each square
as colour0 of pair1, colour1 of pair1, colour0 of pair2, colour1 of pair2.
All indices are partitioned by these 2r alternating squares. Each square
has two initial U-points; the first r squares each own one x_j-to-y_j
candidate. Any two omissions in a square are permitted, since the two
remaining owner points induce at most one edge. Fewer than two omissions
leave at least a three-vertex path, so U is minimum-cardinality permitted.
Every candidate subset remains permitted.

**Costs and strict separation.** All r operations share the single initial
odd path. Theorem 1 gives cost 2r-2-max(t-1,0) for **every** t-operation subset.
Selecting all r is the unique optimum of size r-1. The surviving nontrivial
paths are (4j+2,4j+3,4j+4), 0<=j<r-1, with cover {4j+3} and matching edges
(4j+2,4j+3). Everything else is isolated. This explicitly attains the claimed
fixed-list minimum and dissociation size 3b-(r-1)=11r+1.

For the inherited rule C is the unique initial minimum cover and all x's
lie outside it. Every c in C retains a neighbour congruent to3 modulo4;
none of those neighbours is ever removed. The forced-retirement set is
therefore empty for every batch. Every applicable inherited certificate
has unchanged cost |C|=2r-2, and the empty batch attains it. Equivalently,
when t>=2 the path's remaining I-neighbours number 2r-1-t<2r-2=|C|,
so no constrained initial matching can saturate C. Changing the initial
matching or allowing mixed removals cannot avoid this: the cover is unique
and all candidates remove outside it. Thus the additive method gap is r-1,
unbounded, with only one initial odd component, not r separate neutral
budgets.

For comparison with the physical target, floor(b/3)=floor(N/6)=floor(4r/3).
The old cost 2r-2 exceeds this for r>=4; the repaired cost r-1 is below it.
The all-square owner class already has a stronger unrestricted theorem in
the existing research: this family does not settle a new universal class.
It strengthens what can be certified **from this specified starting U and
candidate list**, and is not an adjacency-preserving rectangular-grid
embedding or an improvement of the universal unit 5/6 coefficient.

**Physical realization and connectivity.** For every P-pair introduce a
centre joined to its two witnesses; join each witness to its owner; put
Q-edges among witnesses and B-edges among owners. Give owners the opposite
physical colour from their witnesses and centres the opposite colour from
their P-pair. Every edge is bichromatic. The centres and witnesses form the
cycle A with every P-edge subdivided once, hence a 12r-cycle. Each owner
square has four distinct attachments to this cycle; owner and witness
degrees are three and centre degrees two. Deleting an owner leaves its
square as a connected path still attached, while the cycle remains intact.
Deleting a cycle vertex leaves the rest of that cycle a connected path;
each square retains at least three of its attachments (four if the deleted
vertex was a centre). All surviving vertices are therefore connected after
any single deletion. This proves two-connectivity at every scale. QED.

## 4. Reproduction and boundaries

Implementation: [odd_path_neutral_budget.py](../develop/odd_path_neutral_budget.py).
Run the assertion-enabled original checker:

```sh
python3 -B scripts/check_odd_path_neutral_budget.py
```

The checker uses literal matching enumeration and direct edge scoring,
separately from the consecutive-pairing constructor. It checks every simple
degree-two bipartite graph through six vertices with all independent tight
covers and removal subsets; every initial maximum matching through four
vertices; all isolation-edge systems through three initial points and two
additions; all canonical group patterns, implications, conflicts and blockers
through three labels; larger seeded systems; and random physical optima
within the stated isolation domain. The family is checked through r=512,
with all candidate subsets through r=7 and explicit vertex-deletion
connectivity checks. Exact counts and witnesses are in the
[report](../output/odd-path-neutral-budget-check.json). Arbitrary-size
conclusions rely on the proofs above, not extrapolation from these tests.

The [independent audit receipt](../output/odd-path-neutral-budget-review.json)
records the actual source and execution scope; no Lean verification is
claimed. The inherited-cover Hall barrier is resolved for this class by
changing final covers, not by weakening the matching-capacity test.
General nonisolated additions, mixed removals with cover repair, sharp
remaining degree/gap parameters, compatible physical multi-Hall routing,
universal8b/3, a universal unit5/6 gain and arbitrary-width rectangular-grid
triple equality remain in the full ACTIVE research goal.
