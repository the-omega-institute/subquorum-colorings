# Objective-preserving saturation of diagonal neutral relays

2 October 2026. The [all-neutral relay obstacle](NEUTRAL_RELAY_OBSTACLE.md)
shows that a relay need not force a donor. Here we remove such relays by an
explicit feasible-pair move, with no positive-source or pressure hypothesis.
The exact charge distribution and all nontrivial residual components survive.

## 1. A local move independent of the side caps

Use the aligned 2-by-2 tiling and feasibility convention of the
[absorption proof](GRID_ABSORPTION_PROOF.md). Occupied vertices are selected
vertices T and matching endpoints P. Each T has at most one occupied neighbor.

**Lemma 1 (diagonal relay saturation).** Let Q be a deficient tile whose only
occupied corners are two diagonally opposite vertices. Assume every P in Q
is matched to a vertex in a saturated tile. Delete all those matching edges,
promote their Q endpoints to T, and make their other endpoints blank.
Then the new pair is feasible and has the same |T|+|M|. Q becomes saturated;
each receiving tile remains saturated. The charge of every tile is unchanged.
The residual multigraph is unchanged except for deleting the isolated
zero-capacity vertex Q.

**Proof.** There are p=2-t(Q) matching endpoints in Q, with p in {1,2}.
Diagonal occupancy excludes internal matching edges, and every P is a
saturated attachment, so h=0,s=p,r=2-t-p=0,d=0. Q has charge zero.

At each promoted endpoint x, both within-Q neighbors are blank. At most
two external grid neighbors exist; one is its mate y, which becomes blank.
Thus x has at most one occupied neighbor after the move. The two promoted
corners, when p=2, are diagonal and do not neighbor one another. Promotion
does not add an occupied vertex: x was already P. The occupied set only loses
the removed mates. Every old T therefore keeps or decreases its occupied
degree. Remaining matching edges are disjoint and avoid the enlarged T,
so the pair is feasible.

Exactly p edges are removed and p selected vertices added, preserving the
objective. The saturated receiving tiles keep their original two T vertices;
only their P is removed. All other deficient tiles retain their labels,
internal edges, saturated attachments and residual edges. Q has no matching
edge to any other deficient tile before the move and none afterward, so
newly saturating Q does not reclassify an edge elsewhere. Its charge changes
from zero to saturated zero; every other tile's charge is unchanged. The
residual edges, their endpoint corners and capacities of remaining vertices
are identical. Q was an isolated vertex of capacity zero, so deleting it
does not change any other residual component or its excess. QED.

This move removes saturated-attachment edges. It differs from the internal
edge fork moves in absorption Section D, and uses a different invariant.
It preserves tile charges, rather than creating a donor.

## 2. Simultaneous normalization and independence of order

**Proposition 2.** All tiles satisfying Lemma 1 in a feasible pair can be
saturated in any order. Each original eligible tile remains eligible until
processed; no other deficient tile becomes eligible. The final pair is
independent of order, and all residual components with positive or negative
excess are exactly preserved.

**Proof.** Distinct eligible tiles are deficient. The deleted edge of one
joins it to a saturated tile, never to another eligible tile. Their promoted
endpoints are in different tiles; their removed mates are disjoint by the
matching property. A move changes no labels or matching edges in any other
deficient tile, and changes no tile's saturation status except Q. Since Q
has no edge to another deficient tile, that new status changes no other
attachment count. Hence eligibility elsewhere is unchanged. Lemma 1 applies
at every step, even when eligible tiles are adjacent.

The final selected set is the original T union all original eligible P
endpoints, and the final matching is the original matching minus their edges.
These sets are independent of order. At most mn/4 tile moves are required;
the number of matching edges strictly decreases at each move. Only isolated
zero-excess residual components disappear. QED.

## 3. Consequence for same-direction donors

**Corollary 3 (half-unit dichotomy after normalization).** Every feasible pair
has an objective-equivalent normalized pair in which every tile between the
specified same-direction caps of the
[capacity lemma](SAME_DIRECTION_CAPACITY_DONORS.md) is either saturated or
has charge at most -1/2. If its residual capacity is two, the stronger bound
rho<=-1 still holds. No occupied entry guard is required.

**Proof.** Apply Proposition 2. Now inspect a tile satisfying the cap
hypothesis in the resulting pair. The capacity lemma proves rho<=0 and
classifies its deficient zero-charge possibilities: its only occupied
corners are diagonal and all its P are attached to saturated tiles.
Such a tile would satisfy Lemma 1, contradicting normalization. A deficient
tile therefore has strictly negative half-integral charge, at most -1/2.
The capacity-two bound follows from rho<=-r/2. QED.

Equivalently, a pair maximizing |T| subject to a fixed objective value has
no diagonal relay: the move would increase |T| without changing that value.
In particular, an objective maximizer with maximum |T| among maximizers
satisfies the corollary. Normalization is therefore legitimate when proving
an upper bound on the maximum representative objective.

## 4. Accounting and limits

Positive source components and their residual edges survive this move, so it
can be performed in configurations containing bent positive paths and
capacity-two passages. Every existing tile deficit is also unchanged.
However, a saturated receiving tile loses its P and may stop being a cap
certificate for another region. The corollary concerns cap patterns that
exist in the normalized pair. It does not preserve every old pressure-band
or source-to-donor incidence description. Any geometric allocation must be
checked in that pair or justified across the move.

Saturated gaps still have zero charge, including the saturated R,L child in
the earlier 6-by-20 example. This normalization does not prove that each source
reaches a deficient gap or a donor, nor does it establish weighted Hall or
rho(W)<=0. It sharpens the local obstruction: after normalization a
same-direction deficient gap is always a half-unit donor; the unresolved
zero gaps are saturated.

For K disjoint source regions of charge at most one and H distinct deficient
same-direction donor tiles in the normalized pair, the ledger gives
q<=K-H/2+rho(W), with any additional certified regions included once.
Geometrically justified weighted Hall and nonpositive remainder give q<=0,
hence coefficient one on that covered class. No universal improvement of
the 5/6 theorem is claimed here.

## 5. Reproduction

Run `python3 develop/check_diagonal_relay_normalization.py --output output/diagonal-relay-normalization-controls.json`.
The checker tests the three neutral receiving types, the complete 8-by-8
all-neutral configuration, and the mixed 6-by-14 and 6-by-20 source examples
under eight symmetries. It checks feasibility and canonical routing before
and after, objective preservation, every tile charge, unchanged residual
edges and component data, and all six processing orders of the three diagonal relays in
the all-neutral example. These controls support the general written proof;
no new Lean theorem is claimed.
