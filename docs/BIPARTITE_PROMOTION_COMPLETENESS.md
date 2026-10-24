# Freezing is a complete promotion test in every bipartite graph

19 October 2026. This strengthens the one-side core and frozen-certificate
results in PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md. It concerns the
existing endpoint-promotion operation, with the matching and original selected
vertices fixed. It does not allow rematching or deleting original selected
vertices. No submitted manuscript is changed.

## 1. Definitions

Let G be a finite simple bipartite graph with a fixed bipartition. Let M be
a matching, P its endpoint set, and T disjoint from P. Write A=T union P,
and assume every vertex of T has at most one neighbor in A. Let m be the
matching involution on P. A bundle is an oriented subset of M: its promoted
set U contains at most one endpoint of each edge, its deleted set is m(U),
and its new selected and occupied sets are T union U and A minus m(U).
The empty bundle is the feasible identity. A feasible bundle requires every
vertex of T union U to have at most one remaining occupied neighbor.
Every such move preserves |T|+|M|.

Starting with F_0 empty, define

    F_(j+1) = F_j union {v in P: |N(v) intersect (T union m(F_j))| >= 2}.

The increasing sequence stabilizes after at most |P| strict additions.
Write F for its stable value. Earlier freezes certify that m(F_j) remains
occupied in every feasible bundle. A retained endpoint may become selected;
the argument requires it to remain occupied, not to keep its original label.

## 2. Feasibility factors by promoted color

**Color-restriction theorem.** A bundle U is feasible if and only if both
restrictions U_0 and U_1 to the two bipartition classes are feasible.

Proof. Fix v in U_c. Every neighbor of v has color 1-c. The deleted mates
of U_(1-c) have color c, so none is adjacent to v. Consequently

    N(v) intersect (A minus m(U))
      = N(v) intersect (A minus m(U_c)).

Thus v has exactly the same remaining occupied neighbors under the full
bundle and its own-color restriction. Original T remains feasible under
every restriction because the occupied set only shrinks from A. This proves
necessity. The two restrictions use disjoint matching edges, since U is an
oriented subset of a matching. Their individually feasible union is feasible
by the compatible-union lemma, proving sufficiency. QED.

This is factorization of feasibility, not an assertion that independently
chosen maximum color bundles are compatible. Two independently computed
color cores may choose opposite orientations of the same matching edge.

## 3. Exact universal freezing and constructive completeness

**Complete-freezing theorem.** The following statements hold.

1. F is exactly the set of endpoints that cannot be promoted by any feasible
   bundle, even a bundle using both colors or several endpoint components.
2. For either color c, the entire set U_c=P_c minus F is a feasible bundle.
   It is the unique greatest feasible bundle on that color, under inclusion.
3. A nonempty bundle exists if and only if a nonempty one-color bundle
   exists, if and only if F is not all of P.
4. Therefore a finite freeze transcript ending at F=P is a complete
   certificate that no nonempty endpoint-promotion bundle exists.

Proof of soundness. At the first stage all neighbors used to freeze a
vertex lie in T and are permanent. Inductively, a frozen endpoint cannot
be promoted in any feasible bundle; its mate can only become blank by
promoting that endpoint, so the mate is permanent too. Two distinct
permanent neighbors exclude the next promotion. This proves that every
member of F is universally unpromotable.

Proof of completeness. Fix a color c and promote every endpoint in
U_c=P_c minus F. This selects at most one endpoint of each matching edge.
For v in U_c, every endpoint neighbor has opposite color. Such a neighbor
z survives precisely when its mate m(z), of color c, was not promoted,
which is equivalent to m(z) in F. Original selected neighbors always
survive. Hence the remaining occupied neighbors of v are exactly

    N(v) intersect (T union m(F)).

There are at most one of them: otherwise the stable closure would have
added v to F. Every promoted vertex is therefore feasible, and original
T only loses neighbors. Thus U_c is feasible. In particular every endpoint
outside F can be promoted by choosing its own color. No feasible bundle
can contain a member of F, by soundness, proving the exactness and the
greatest-one-color assertion. The remaining equivalences follow. QED.

The proof works for arbitrary bipartite graphs and arbitrary degrees. Grid
geometry, single terminality, tile alignment and square counts play no role.
Finiteness is needed for the terminating algorithm and finite transcript;
the constructive implication from any closed F with a sound certificate
does not depend on a numerical width bound.

## 4. Consequences for normalization and the residual problem

The two one-side threshold cores computed in the earlier note are exactly
P_0 minus F and P_1 minus F. Indeed, that note identifies each core as the
union of all feasible bundles on its side, and the theorem identifies that
union with the corresponding complement of F. Thus the earlier peeling
algorithm already decides the existence of arbitrary oriented bundles;
it need not enumerate the three choices on each matching edge.

Using adjacency lists, maintain for each endpoint the number of neighbors
in T union m(F). Queue an endpoint when this count reaches two. Freezing
v newly retains m(v); update the counts of its endpoint neighbors once.
Each endpoint freezes at most once and each retained-mate incidence is
processed at most once. Initialization and processing are linear in the
size of the occupied induced graph. A positive answer includes a feasible
one-color bundle; a negative answer includes a freeze transcript.

Repeatedly apply either nonempty color core, recomputing the occupied set,
matching and closure after each actual move. At most the original |M|
nonempty moves are possible. The final feasible pair admits no bundle of
any orientation. This strengthens the earlier termination conclusion,
which had only claimed absence of one-side bundles. It asserts neither
confluence nor a maximum-cardinality global mixed bundle.

Any finite sequence of the stipulated promotions also collapses to one
bundle with the same final pair: each original matching edge is used at
most once, and the final selected and removed sets are the unions of the
stepwise sets. Final feasibility makes that union a feasible bundle against
the original pair, even if later steps were unavailable individually at
the start. In a bipartite graph its color restrictions then serialize the
same result in at most two one-color moves. This existence statement does
not prescribe a greedy algorithm for finding the best final pair.

Mixed colors still matter for square removal in a single operation: the
previous exact ladder family has a unique square-removing mixed bundle.
The color-restriction theorem means its two restrictions can also be
performed consecutively. After performing the first restriction, the
second remains feasible because it only sees further deletions, uses
different matching edges, and the newly selected vertices from the first
move are feasible in the known union. This serializes that given mixed
bundle. It does not say an arbitrary greedy sequence reaches a particular
square-free result, or that every frozen component is square-free.

Thus the remaining geometric question is about completely frozen endpoint
components with squares, not about an undiscovered mixed-only escape from
empty color cores. Existing frozen one-square and overlapping-square
obstacles remain valid. A general compensation proof must handle them and
allocate physical tile charge without reuse.

## 5. Scope and verification

The preceding arguments are general proofs. Computational controls compare
the closure with both one-side cores, enumerate all orientations on small
bipartite examples, and check exact universal unpromotability vertex by
vertex. The new graph-level Lean development uses the occupied induced
graph as its vertex domain: original blanks are absent, and m extends by
the identity on T. The adapter from a physical configuration to this domain
and the algorithmic running-time argument are written proofs.

The local Lean 4.33.0 audit passes 61 declarations in total, including
ten new statements in
[BipartitePromotion.lean](../formal/SubQuorum/BipartitePromotion.lean).
They cover the actual occupied-pair axioms, feasible entire unfrozen color
sets, exact universal unpromotability, greatest one-color bundles, color
restriction and terminality, and an arbitrary-length two-step freezing
induction used by the capped-ladder family. The corresponding
[receipt](../output/bipartite-promotion-formal-check.json) permits only the
standard logical axioms, with no sorry or compiler-reduction axioms.

The [independent controls](../develop/check_bipartite_promotion.py) pass
all 512 bipartite graphs with two labeled parts of size three, all 5,504
graph/matching pairs and all 55,924 feasible selected-set configurations.
They enumerate 169,048 oriented choices, including empty moves, and compare
the universally promotable set with P minus F vertex by vertex. Eight
physical grid fixtures also pass, including five-round freezing and a
degree-four example; the latter's orientations are not exhaustively listed.
See the [finite receipt](../output/bipartite-promotion-controls.json).

Bipartiteness is essential. In K6 with T empty and any perfect matching,
F stays empty. A bundle can promote at most three vertices and therefore
leaves at least three occupied vertices. Every promoted vertex then has
at least two occupied neighbors, so no nonempty bundle is feasible.
All 26 nonempty orientations are checked as a control, but this clique
argument is the proof. Thus the converse cannot be claimed for arbitrary
graphs or inferred from freezing soundness alone.

```sh
python3 develop/check_bipartite_promotion.py --output output/bipartite-promotion-controls.json
python3 scripts/check_collar_formal.py --lean /path/to/lean4.33.0/bin/lean --output output/bipartite-promotion-formal-check.json
```

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
