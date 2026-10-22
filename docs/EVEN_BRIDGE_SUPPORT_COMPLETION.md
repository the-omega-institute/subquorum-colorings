# Even-bridge support completion and exact interface cancellation

22 October 2026. Research note, separate from the submitted manuscript.
The graph and geometric statements below are written proofs. Finite controls
and the explicitly scoped Lean statements supplement those proofs.

## 1. Setting and statement

Work in a finite even-by-even grid rectangle with its fixed disjoint 2-by-2
tiling. A feasible pair consists of a selected set T and a matching M disjoint
from T, with every selected vertex having at most one occupied neighbor.
Write P=V(M), A=T union P. Assume single terminality: every endpoint has
at least three occupied neighbors. An exchange promotes one endpoint of
each edge of a nonempty matching subcollection into T and deletes the other
endpoint, leaving the other matching edges unchanged. Exchange terminality
means no such feasible exchange exists, for any perfect matching of P.

Fix a connected component H of the graph induced by P. Every original
selected vertex adjacent to H has exactly one endpoint neighbor. Discard
other endpoint components and retain just those selected neighbors when
regarding H as a separate pair; its occupied endpoint degrees are unchanged.
All supports and completions below use the original board coordinates.

Call a bridge pq of H even when the two components L,R of H-pq have even
cardinality; name p in L, q in R. Define the completed pairs by

    P_L=L, T_L={t in T : N(t) intersects L} union {q},
    P_R=R, T_R={t in T : N(t) intersects R} union {p}.

The support-completion lemma states:

1. Both completed pairs are feasible and single-terminal; every retained
   endpoint has exactly its original occupied degree.
2. Perfect matchings factor as PM(H)=PM(L) times PM(R). The original pair
   is exchange-terminal exactly when both completed pairs are.
3. If R(K) is the set of tiles meeting a pair's endpoints and

       rho(K)=|P_K|/2+sum_(Q in R(K)) (|T_K intersect Q|-2),

   then rho(H)=rho(L)+rho(R), using the completed selected sets on the right.
4. For the actual matching-block ledger of MATCHING_BLOCK_TILE_LEDGER.md,
   J is additive and there is an explicit nonnegative correction chi with

       X_H=X_L+X_R+chi, B_H=B_L+B_R+chi.

   Consequently X-B, and hence receiver demand, is exactly additive.

This is a decomposition theorem for actual endpoint bridges, with no source
model, matching uniqueness or bounded freezing-depth hypothesis.

## 2. Feasibility and matching factorization

The only edge from L to R is pq. Thus q has exactly one neighbor in L, namely
p. Any retained original selected vertex t in T_L cannot be adjacent to q:
it already has an endpoint neighbor in L, whereas original feasibility
forbids two occupied neighbors. Every original selected vertex has no more
occupied neighbors after completion than before. The new selection q has
exactly its one neighbor p. This proves feasibility on L. Every occupied
neighbor of a vertex in L is retained: an original selected neighbor belongs
to T_L, and its only possible outside endpoint neighbor is q, now restored
as a selection. Endpoint degrees are therefore preserved. The proof on R
is identical. In particular each completed pair is single-terminal.

For any matching crossing a cut S, counting its incidences in S gives

    |S| = 2(number of internal matching edges) + (number of cut edges used).

A bridge cut has only one edge available. Every perfect matching omits an
even bridge, and uses an odd bridge. Since an original perfect matching
exists, both even sides have perfect matchings. Restrictions and unions give
the claimed bijection. Allowed edges, and therefore actual matching blocks,
inside either side are unchanged by the split.

## 3. Exchange terminality in both directions

We first recall why a mixed feasible exchange has a nonempty feasible
monochromatic subexchange in a bipartite graph. Keep only the promoted
vertices of either nonempty color. The occupied neighbors of a retained
promoted vertex do not change: deletions caused by the omitted opposite-color
promotions have its own color and cannot be its neighbors. Original selections
only lose occupied neighbors, since an exchange never adds occupied vertices.
Hence that monochromatic subexchange is feasible.

If a completed side admits an exchange for one of its perfect matchings,
extend that matching by any matching of the other side and perform the same
exchange globally. Within its side every promoted vertex sees exactly the
occupancy used by the completed pair. The only cross-edge neighbor is kept
occupied in both configurations. Original selections outside the side cannot
gain occupied neighbors. Thus a completed-side exchange extends globally.

Conversely suppose there is a global exchange. Pass to a nonempty
monochromatic subexchange and, after exchanging color names, let its promoted
vertices be black. Suppose p is black and q white. If R contains any promoted
vertex, restrict the exchange to R. Restoring p as a selection cannot hurt
any black promoted vertex of R, because p is black too. The new selection
p has at most its one neighbor q in R. Original selected vertices retained
on R still satisfy feasibility. This gives a nonempty feasible exchange in
the completed R. If R has no promoted vertex, no vertex of R is deleted
either: all matching edges lie on one side. In particular q stays occupied.
The exchange on L is therefore feasible with q as a selected support, giving
a nonempty exchange in completed L. The other color and bridge orientation
are symmetric. This proves the terminality equivalence for arbitrary mixed
exchanges and arbitrary replacement matchings.

## 4. Tile anchoring and exact receiver-charge additivity

Two elementary consequences of feasibility and endpoint degree at least three
are useful. First, the endpoints in any endpoint-bearing tile are connected:
the only disconnected nonempty pattern is a diagonal pair without intermediate
endpoints. Each of the two intermediate corners would then have to be blank,
since a selected corner would see both endpoints. Each diagonal endpoint
would have at most two occupied neighbors, a contradiction. This argument
also applies to every completed side.

Second, every selected vertex in an endpoint-bearing tile is adjacent to
an endpoint in that same tile. Otherwise an endpoint can only be its diagonal
corner. Neither intermediate corner can be an endpoint by assumption, nor
selected, because it would see both the selected corner and the diagonal
endpoint. The two blank intermediate corners again force endpoint degree at
most two. The selected corner's unique endpoint anchor is therefore internal
to the tile.

Apply these facts to L and R. A tile shared by their receivers contains an
edge between L and R, by connectivity of the original tile intersection.
It must contain pq. There is exactly one such shared tile if pq lies inside
a tile, and none otherwise. Native receiver selections partition between
the completed sides according to their unique internal endpoint anchor.

If pq is intertile, neither restored support belongs to its own completed
receiver: otherwise that tile would be shared. The total receiver selection
count and total tile count are unchanged. If pq is intratile, both restored
supports belong to the shared tile. The sum of receiver selection counts
increases by two, while the sum of receiver tile counts increases by one.
These increments cancel in selected-count minus twice tile-count. Matching
counts always add. Therefore, in both cases,

    rho(H)=rho(L)+rho(R).                                      (1)

This is additivity of completed receivers. It is not additivity of the
original raw matching-block charges, whose tiles can overlap.

## 5. Exact correction in the actual matching-block ledger

Recall the definitions for a single pair. The allowed-edge graph joins two
endpoints if that edge occurs in at least one perfect matching. Its components
are the actual matching blocks C. For each tile Q, let e_Q count grid edges
within Q whose endpoint vertices lie in different blocks. Set

    gamma_C=|C|/2+sum_(Q meeting C)(t_Q-2), B=-sum_C gamma_C,
    X=sum_(Q meeting P)(2-t_Q)e_Q,
    J=number of full endpoint tiles meeting more than one block.

The exact receiver identity is rho=X-2J-B. Exchange terminality implies
gamma_C<=0, but raw B is not a partition of physical donor capacity.

A full endpoint tile is a 4-cycle and cannot cross a bridge. Thus J is
additive under the split. Every nonshared tile has unchanged contributions
to X: the only new selection could be a restored support in a shared tile.
For an intertile bridge set chi=0. For an intratile bridge, its shared tile
has either two or three endpoints; four would put the bridge in a cycle.

With two endpoints, the shared tile has t=0 or 1 original selections.
In fact t=0 is impossible for a bridge. Rotate so the two endpoints form
the top row of the tile. If both lower corners are blank, each endpoint
needs both neighbors outside the tile occupied to reach degree three.
In particular the two vertices immediately above them are occupied and
adjacent. Neither can be selected, because it would see both its endpoint
and the other occupied vertex. Both are therefore endpoints, completing a
4-cycle through pq, contradicting the bridge hypothesis. A missing vertex
at the board boundary only makes the required degree impossible sooner.
Thus every actual two-endpoint bridge tile has t=1. The bridge joins
different matching blocks, so its original contribution is one. Each
completed side has just one endpoint there and no cross-block edge. Thus

    chi=1                       (two endpoints, necessarily t=1).

With three endpoints, their tile graph is a path with two edges. It has
no original selection: its remaining corner sees two endpoints. The split
has two endpoints on one side and one on the other. Let h=1 if the edge
on the two-endpoint side joins different actual matching blocks, otherwise
h=0. The original contribution is 2(1+h). The two-endpoint completed side
has one restored selection and contributes h; the singleton contributes
zero. Hence

    chi=2+h                     (three endpoints, h in {0,1}).

In all cases X_H=X_L+X_R+chi. Combining this with (1), J additivity and
the exact receiver identity gives B_H=B_L+B_R+chi. In particular the
same interface correction appears on both sides of the proposed payment:

    X_H-B_H=(X_L-B_L)+(X_R-B_R).                              (2)

Consequently chi is zero for an intertile cut and belongs to {1,2,3} for
an intratile cut. All three positive values have full finite-model witnesses.
The correction is not a new donor and must not be spent in addition to B.
When several deleted bridges lie in the same tile, apply this binary identity
sequentially. Later cuts use the current completed selections. Do not assign
independent physical slots to the corrections for different original bridges.

## 6. All even bridges and consequences for compensation

Delete all even bridges of H and complete each resulting piece K by retaining
original selected vertices anchored to K and restoring every outside endpoint
neighbor as a selection. Successive binary splits give exactly this completion:
a previously restored support survives in a descendant precisely when its
unique anchor belongs to that descendant. Each detached side has even size,
so cut parity of every remaining bridge is preserved. Consequently every
piece has even size, and its remaining bridges are odd and used by every
perfect matching. Deleting bridges does not change which unremoved edges
belong to a cycle, so no other new bridges are created.

Repeated application of Sections 2--4 proves feasibility, degree preservation,
independent perfect-matching choices, terminality equivalence and

    rho(H)=sum_K rho(completed K).                            (3)

This also establishes that restored supports in one piece cannot conflict;
no additional compatibility assumption on the original pieces is required.
Repeated (2) gives an exact signed interface ledger. No upper bound on the
number of pieces, bridge length or freezing depth is used.

For the whole board, write D for the nonnegative sum of 2-t_Q over tiles
without endpoints. Original whole-component receivers are disjoint, and

    mn/2-|T|-|M|=D-sum_H rho(H)
                    =D-sum_(all completed pieces K) rho(K).  (4)

The D in this formula belongs to the ORIGINAL configuration. It is not the
sum of endpoint-free deficits recomputed on each completed board. Those
would reuse physical tiles. A sufficient condition for the coefficient-one
bound is that every completed piece has nonpositive receiver charge. More
generally it suffices that the single signed sum in (4) is at most D; negative
piece charges can compensate positive ones exactly once through that sum.
On this stated class, |T|+|M|<=mn/2 removes the entire |M|/6 loss from the
existing universal |T|+(5/6)|M|<=mn/2.

A positive receiver charge therefore localizes to at least one positive
completed piece with no even bridge. This does not prove that a smallest
counterexample to the global half-area inequality is itself bridge-irreducible:
the endpoint-free deficits and board geometry change under completion.
Endpoint forests already belong to the older square-free coefficient-one
theorem; the forest bound is not new here. The new reduction allows arbitrary
square-bearing pieces and their actual matching-block interface corrections.
Positive irreducible pieces, including thick elbows, still require physical
donor analysis. The unrestricted inequality X<=D+B+2J remains open.

## 7. Examples and limits of the hypotheses

The nonunique positive graft in EXCHANGE_TERMINAL_NONUNIQUE_MATCHINGS.md has
an even bridge joining its 14-endpoint flexible core to a thick elbow. The
completed charges are respectively 0 and 1 in its reference phase, summing
to the original positive charge 1. The bridge does not supply the missing
physical donor. The bounded-height sharp chains split along their connecting
even bridges into the completed sharp cores. This reduction remains valid
although every replacement matching has freezing depth at least 3k.

Parity is essential: on a 4-by-4 board take P={(1,1),(1,2)} and
T={(0,1),(1,0),(2,2),(1,3)}. Both endpoint occupied degrees are three,
but their bridge is odd, forced and cannot be restricted to singleton
perfect matchings.

The bridge hypothesis is essential as well: take the full endpoint square
P={(1,1),(1,2),(2,1),(2,2)} with
T={(0,1),(1,3),(3,2),(2,0)}. It is feasible and single-terminal. Cut
between its columns. Restoring the opposite column as selections creates
adjacent new selections, each also adjacent to an endpoint in its own
piece, violating feasibility. Arbitrary even cuts do not admit this lemma.

## 8. Reproducibility and formal scope

Run the independent coordinate verifier with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_even_bridge_support_completion.py --output docs/data/even_bridge_support_completion.json

The finite domain includes all 1,086 feasible single-terminal models with
endpoints in a 3-by-4 box, including 80 even-bridge cuts. With explicit
positive grafts, occupied bands, all sharp-chain choices through length four,
and phase/symmetry controls, the suite checks 1,217 input models, 312 even
cuts, 9,243 matching terminal tests and 132 simultaneous all-even-bridge
splits. It tests terminal and nonterminal sides, all possible correction
branches, the positive 0+1 graft, and both failed-hypothesis controls.
These computations discover and check cases; the proofs in Sections 2--6
apply without a size bound.

EvenBridgeSupportCompletion.lean checks the necessary internal-neighbor
bound, finite tile anchoring/connectivity, adjacent occupied support labels,
bridge parity arithmetic, receiver additivity, both interface corrections,
buffer/net cancellation, signed split invariance and the original-deficit
payment implication. The general graph matching bijection, exchange
restriction argument, geometric bridge classification and all-cut adapters
remain written proofs. No full formalization of the global conjecture or
general graph decomposition is claimed.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
