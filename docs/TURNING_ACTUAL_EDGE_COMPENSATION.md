# Actual-edge compensation through turns and unbounded forced ownership changes

The signed two-row lemma leaves positive cross-strip charges that cannot always
be eliminated by choosing horizontal or vertical charges separately on each
tile. This note proves an exact, broader compensation criterion using each
**actual matching edge once**, including all-P tiles as relays. A sharp geometric
family shows why a nearby unused resource need not admit a local ownership
repair: restoring one selected vertex from the specified reversed baseline
forces arbitrarily many ownership changes,
while the actual matching and all previously used physical resources are kept.

The ownership criterion is conditional. Its universal feasibility for a fixed
actual matching is disproved by the [component-cut family](ACTUAL_MATCHING_COMPONENT_CUT_AND_SQUARE_EXCHANGE.md), which also gives an explicit repair when a square rematching is allowed. No new universal 5/6 bound or freezing
statement is claimed.

## 1. Physical resources and the exact compensation criterion

Partition an even-by-even rectangular grid into disjoint 2-by-2 tiles. Let `M`
be an actual matching, `P` its endpoints, `T` disjoint from `P`, `O=T union P`,
and `H` the holes. For the geometric applications, every selected vertex has
at most one occupied neighbour. The algebraic criterion itself only uses the
matching, disjointness and the tile partition.

For a tile B put

    t_B=|T intersect B|, p_B=|P intersect B|, o_B=t_B+p_B,
    q_B=t_B-|H intersect B|=2t_B+p_B-4,
    d_B=max(0,o_B-2), r_B=max(0,2-o_B).

An ownership certificate assigns some actual matching edges to tiles containing
at least one of their endpoints. Every actual edge has **at most one owner**,
even when both endpoints are in the same tile. Tile B must own at least `d_B`
distinct edges. An all-P tile needs two actual edges; a tile with three occupied
sites needs one. Two endpoints of a single internal matching edge do not supply
two resources.

**Actual-edge compensation lemma.** The following conditions are equivalent:

1. An ownership certificate exists.
2. For every set U of tiles,

       sum_{B in U} d_B <= |{e in M: e has an endpoint in U}|.   (H)

3. There are endpoint charges `sigma(p) in {-1,+1}` such that every actual
   matching edge has endpoint-charge sum at most zero and every tile has
   endpoint-charge sum at least `q_B`.
4. The same charge inequalities are feasible with real charges in `[-1,1]`.

Each condition implies

    J=|T|+|M| <= area/2.

If a certificate pays each tile exactly its demand, and `u` actual edges are
unused, then the stronger exact identity is

    J = area/2 - u - sum_B r_B.                              (1)

**Proof.** Replicate tile B into `d_B` distinct demand slots, each adjacent to
the actual matching edges incident to B. Hall's theorem gives the equivalence
of (1) and (2). It suffices to test full tile sets in (H): a partial collection
of slots has no more slots, and the same neighbourhood, as all slots of its
supporting tiles. Thus no hidden separate endpoint capacity is introduced.

Given owners, charge the chosen endpoint of each owned edge +1 and its other
endpoint -1. For an edge owned by a tile containing both endpoints, choose one
of them for +1; this still contributes only one resource. Charge both endpoints
of an unused edge -1. If B owns `m_B` actual edges, its charge sum is

    2m_B-p_B >= 2d_B-p_B >= 2t_B+p_B-4=q_B.

Every owned actual edge has sum zero and every unused actual edge has sum -2.
This proves (1) implies (3); (3) implies (4) immediately.

Conversely put `x_p=(sigma(p)+1)/2`. For each actual edge `uv`,
`x_u+x_v<=1`, so the endpoint weights define a fractional assignment of at most
one unit of that physical edge to its incident tile or tiles. Within B,

    sum_{p in P intersect B} x_p
      >= (q_B+p_B)/2 = o_B-2.

Weights are nonnegative, so this is at least `d_B`. Summing over a tile set U
proves (H): each incident actual edge contributes at most one. Hall's theorem
then yields integral ownership. No unproved rounding of geometric configurations
is involved; it is the ordinary bipartite resource assignment that is integral.

For the bound, discard any excess owned resources tile by tile so that each
tile owns exactly `d_B` edges. Write `d=sum d_B`, `r=sum r_B`, and `b` for the
number of tiles. Then `|M|=d+u` and

    |T|+2|M|-2b = sum_B(o_B-2) = d-r.

Substitution gives `|T|+|M|=2b-u-r`, which is (1). Every unused edge and every
sparse-tile unit has a single physical identity; neither can be spent twice.
This completes the proof. The Hall test has polynomial size as a flow problem;
on failure, an unmatched-slot search returns a precise violated tile set.

This is an exact criterion for this broader endpoint-charge/ownership scheme.
A failed Hall cut would refute the scheme on that configuration, not by itself
the numerical half-area target. No claim that every feasible grid passes (H)
is inferred from finite searches.

## 2. Local horizontal/vertical directions do not suffice

Use the following feasible 4-by-4 occupancy, with rows/columns numbered from zero:

    P P P T
    P P P H
    P P P T
    P H T H

The actual matching is

    (1,2)--(2,2), (0,1)--(0,2), (0,0)--(1,0),
    (1,1)--(2,1), (2,0)--(3,0).

There are three selected vertices, five actual matching edges and three holes,
so `J=8=area/2`. Each selected vertex has exactly one occupied neighbour.
Call the top-left, top-right, bottom-left and bottom-right tiles A,B,C,D.
They are respectively all-P, vertical neutral, three-P negative, and positive.

Allow each tile independently to use the horizontal charge table from the
[signed-strip lemma](TWO_ROW_SIGNED_BOUNDARY_COMPENSATION.md) or its transpose.
At B the horizontal charges on its two endpoints `(0,2),(1,2)` are both zero.
The vertical charges are respectively `+1,-1`. Tile D's unique endpoint `(2,2)`
always has charge +1. Hence the actual edge `(1,2)--(2,2)` requires B to use
the vertical choice. But then `(0,2)` has charge +1 and its actual mate `(0,1)`
in all-P tile A has charge zero under either choice. That edge requires B to
use the horizontal choice. These two requirements contradict each other.

The ownership criterion nevertheless succeeds. Assign the D--B edge to D,
the B--A edge to B, A's internal edge to A, the A--C edge to A, and C's
internal edge to C. Demands `(d_A,d_B,d_C,d_D)=(2,1,1,1)` are met with five
different actual resources. The associated charge certificate gives A both
positive and negative endpoint charges, whereas its restricted H/V charges
were all zero. A neutral all-P tile can relay a credit; its total charge is
zero without every endpoint charge being zero.

## 3. General forced path relay lemma

Suppose an ownership component has pairwise distinct tile vertices `v_0,...,v_l`, and distinct actual
edges `e_i` joining `v_i` to `v_{i+1}`, and `a_i` internal actual matching edges
in tile `v_i`. These are all incident resources in the component. Assume

    d_i=a_i+1 for i<l, and d_l=a_l, with a_l>=1.

Then the only full ownership certificate assigns every internal edge to its
own tile and every `e_i` to `v_i`.

Indeed the number of resources equals the total demand. Thus every resource
must be used, every tile must be paid exactly, and every internal edge must
belong to its unique incident tile. After those payments, `v_0` must own `e_0`.
Then `v_1` must own `e_1`, and induction forces all the displayed owners. The
terminal tile receives its demand from its internal edges. This proves both
existence and uniqueness at arbitrary path length.

Now reduce only `d_0` by one. There is a valid baseline certificate assigning
each `e_i` to `v_{i+1}`, using every internal edge except one chosen internal
edge at `v_l`. Restoring the missing unit at `v_0` forces every `e_i` to change
owner and the unused terminal edge to be activated. Exactly `l+1` physical
edges have changed ownership status: `l` previously paid edges plus one reserve.
All previously used physical edges stay used, and all old tile demands remain
paid. This is a capacity-one augmentation, not multiple payments from one edge.

Components satisfying these hypotheses can be combined when their actual edge
resources and tile sets are disjoint. The certificates unite, so the count and
preservation properties add without any shared reserve. General components
with cycles, branching or additional ports require their own Hall analysis.

## 4. Sharp feasible bent family of arbitrary length

For every integer `q>=1` take four rows and `w=2q+2` columns. Set

    T={(0,2q+1),(2,2q+1),(3,2q)},
    H={(1,2q+1),(3,2q+1),(3,2q-1)}.

All other vertices are P. The selected vertices have respectively the unique
occupied neighbours `(0,2q),(2,2q),(2,2q)`. Thus the occupied-neighbour condition
holds independently of the matching choices below.

Index tiles by `(row pair, column pair)`. The quotient path is

    (1,q), (0,q), (0,q-1),...,(0,0), (1,0),...,(1,q-1).       (2)

It has `2q+2` different tiles and `2q+1` edges, covers every tile, and bends
around the all-P region. The source tile `(1,q)` is positive, its next tile
`(0,q)` is vertical neutral, and the final tile `(1,q-1)` has three P and one H.
The other `2q-1` tiles are all-P.

For q=1 use the five edges in Section 2. For q>=2 use the following pairwise
disjoint actual edges, where each range is empty if its upper endpoint is
smaller than its lower endpoint:

* `(1,2q)--(2,2q)` and `(0,2q)--(0,2q-1)`;
* `(0,2j+1)--(0,2j+2)` for `0<=j<=q-2`;
* `(1,2j)--(1,2j+1)` for `1<=j<=q-1`;
* `(0,0)--(1,0)`, `(1,1)--(2,1)`, `(2,0)--(3,0)`;
* `(3,2j+1)--(3,2j+2)` for `0<=j<=q-2`;
* `(2,2j)--(2,2j+1)` for `1<=j<=q-2`;
* `(2,2q-2)--(2,2q-1)`.

To verify coverage for every q, the two rightmost tiles have only their path
ports. Each intermediate all-P tile has two distinct adjacent ports and one
internal edge covering its remaining side: top straight tiles use an internal
bottom edge, the left turns use an internal left edge, and bottom straight
tiles use an internal top edge. The terminal three-P tile has one path port
and one internal edge covering its other two endpoints. Consecutive path ports
are joined in their common row or column. Consequently the listed edges cover
exactly P once and no selected vertex or hole.

There are `2q+1` intertile edges and `2q` internal edges, hence `|M|=4q+1`.
With `|T|=|H|=3`,

    J=4q+4=area/2.

The positive and neutral source tiles have no internal matching edge and
demand one each; every all-P tile has one internal edge and demand two; the
terminal three-P tile has one internal edge and demand one. Thus (2) satisfies
the general forced path lemma and has a unique complete ownership certificate.

Remove only selected vertex `(3,2q)`. The actual matching stays unchanged.
The source tile's occupancy drops from three to two and its demand from one
to zero; every other demand stays the same. This is a feasible baseline with
`J=area/2-1`. Use the reversed path ownership of Section 3 and leave the one
terminal internal edge unused. Restoring that selected vertex is feasible and
forces exactly

    2q+1 old resource owners to change, plus one reserve activation:
    2q+2 changed ownership statuses in total.                  (3)

Every old used physical edge is retained. The source and the reserve tile are
adjacent in the original grid, at tile coordinates `(1,q)` and `(1,q-1)`, for
all q, but their shared boundary carries no actual matching edge. Thus their
geometric proximity does not bound the required ownership
chain length. Formula (3) is a general induction result with explicit feasible
boards, not a finite-width extrapolation or an abstract unrealized flow path.

## 5. Verification, formal scope and remaining geometry

Run `python3 develop/check_turning_edge_ownership.py`. It independently checks
the actual matching, selected degrees, full endpoint coverage, tile demands,
one-owner capacities, both ownership assignments, induced endpoint charges and
the forced augmentation for q=1,...,50. It also checks the literal contradictory
H/V requirements. These are controls for the written all-q construction and
proof; they do not establish universal Hall feasibility.

The formal source `formal/SubQuorum/TurningOwnership.lean` records the scalar
resource/charge identities and unrestricted-length forcing induction. Its
local inequality and trace hypotheses are explicit. The coordinate adapter,
Hall theorem application and universal grid feasibility are not claimed as
end-to-end Lean results. Compilation and exact scope are recorded separately.

The [component-cut family](ACTUAL_MATCHING_COMPONENT_CUT_AND_SQUARE_EXCHANGE.md)
proves that (H) need not hold for a fixed actual matching, and repairs that
family using a single capacity-two square exchange. Universal existence of a suitable rematching is now refuted by the
[unique-matching hole barrier](UNIQUE_MATCHING_HOLE_COMPENSATION_BARRIER.md).
A general transfer rule admitting direct hole budgets or selection relocation
remains open. Finite discovery checks do not decide either universal question. A conditional owner certificate is stronger than merely having a
nonpositive total numerical excess, so failure of a candidate ownership rule
must remain distinct from failure of the target inequality.

This note does not modify the 11 October manuscript, public main/PR #3, or the
star-forming/C4 project. No email is part of this research milestone.

The full written ownership/forcing/construction argument received independent
ACCEPT a50072dc. Its later paired-edge/cycle extension has separate ACCEPT
83638f29. See the [review scope and receipts](../output/turning-compensation-independent-review.json); local Lean remains limited to the seven stated scalar/path declarations.
