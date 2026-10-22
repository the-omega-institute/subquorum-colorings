# A prescribed terminal can force unbounded auxiliary repair cost

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The two ends of a deficient alpha need not be interchangeable for auxiliary
repair. We extend the reflected frozen family by a third parameter and
determine the exact number of new auxiliary edges needed to consume one
original alpha/beta pair. One alpha end always permits cost three. Fixing
the other end can force arbitrarily large cost, even with unrestricted
internal surgery and arbitrary-length zero-surplus corridor links.

The obstruction concerns choosing a terminal before optimizing the repair.
It does not obstruct compensation when both alpha ends remain available,
and it is not a counterexample to the grid inequality. The lower bound
does not impose coherence; explicit coherent repairs attain it.

## 1. Physical family and candidate edges

Let W>=6 and H>=4 be even, and d>=1. Use the arbitrary-width, arbitrary-height
direct_family D(V,K) and its established serial freezing and unique-matching
certificates. Superimpose three copies in raw coordinates:

    central: D(W,4), displacement (0,0);
    left:    D(W+2,H), reflect column x to 10-x,
             then displacement (-1,-2d-5);
    right:   D(W+2,4), displacement (-1,2d+5).

Fill the four extreme-band corridors exactly as in
ZERO_CAPACITY_GAP_BETA_COMPENSATION.md: for r=5,W+4 and the other row r* of
its aligned band, and j=1,...,2d, select

    (r* if j odd else r, 2-2d+j),
    (r if j odd else r*, 7+j).

Changing H only extends the reflected flank away from the central copy.
No new occupied-neighbour contact between copies is introduced. The new
corridor selections are isolated and leave all old degrees unchanged.
The all-V,K serial certificates therefore replay separately, and the
original endpoint graphs stay disjoint and uniquely matched. Thus this
family is feasible, completely frozen, and uniquely matched for every
allowed W,H,d.

Take the matching-closed physical packet J with rows 2..W+7 and columns
-2d-H..2d+15. Translate columns by 2d+H for nonnegative coordinates.
The translation is even, preserving the original aligned tile phase.
The packet contains all selections, endpoints and receiver tiles. Direct
counting, or comparison with H=4, gives

    dimensions = (W+6) by (4d+H+16),
    |T| = 8d+H+27,        |M| = 3W+H+12,
    B = W+6,
    S_J-B = (2d+6)W+4d+7 + (W+2)(H-4)/2 > 0.             (1)

Original strand inventory remains (alpha,beta,mixed)=(1,2,7). The central
alpha ends are s_u=(5,3) and s_l=(W+4,3). Put c=2-2d, r=W+4, R=W+5.
The left beta ends are t_u=(4,c-2), t_l=(R,c-H). The odd-phase analysis
of D(W+2,H) is the same as at H=4: column c consists of independent
actual/auxiliary two-edge cycles; the adjacent column c-1 and the lower
two-row continuation form the beta. Its only other open strand is mixed.

Let P be the actual endpoint set, and A its original vertical PP matching.
Use the following precise candidate relation E:

1. Every grid edge whose two ends belong to P.
2. For every maximal P-free all-BT gap in an aligned band, every pair of
   endpoint vertices in its two boundary columns, allowing either row.

The second type is a declared zero-surplus auxiliary corridor witness.
It supplies no interval unit. This relation includes all occupied grid
edges, not merely the old free-terminal links; it permits the earlier
reflected repair. No finite range restriction is imposed on a corridor.
Coherence is an additional property of an auxiliary matching, not a
restriction used in the lower-bound argument.

Fix s in {s_u,s_l} and choose one free endpoint t of either original beta.
A complete repair is a matching N using E that covers precisely
dom(A) disjoint-union {s,t}. All other original free ends remain uncovered;
M, T and the physical interval identities are fixed. Measure cost by

    C(N)=|N setminus A|.

If q=|A setminus N|, cardinalities give C(N)=q+1. The measure counts
new auxiliary edges even if one duplicates an actual edge of M.

## 2. Exact terminal-choice theorem

For the family and candidate relation above, minimizing over the chosen
original beta endpoint and over all complete repairs gives

    C_u = 3,
    C_l = min(H+1, W/2+3).                               (2)

Both minima are attained by coherent repairs, with final inventory
(alpha_N,beta_N,mixed_N)=(0,1,8). In particular the same minima hold with
or without the coherence constraint. No positive interval unit is used.

### Geometric isolation after deleting the unselected free ends

The four maximal all-BT gaps are exactly the filled extreme-band
corridors. Each has one central free terminal at column 3 or 7 and two
PP vertices at its far flank boundary. There are eight candidate portal
edges. All other P-free gaps have a BB column and are not of type 2.
These assertions follow directly from the support lists of D(V,K):
the vertical occupied strip has consecutive columns 3,4; the two-row
lower continuation has an endpoint in every column through K+3; and
the only intervening P-free regions are the separated copies' corridors.

Delete all original free ends except s and the possible beta targets.
The two central terminals at column 7 are deleted, as is the other
central column-3 terminal. All portals except the two incident to s
are therefore unavailable. Grid edges never join two of the separated
original copies. Consequently any simple alternating path from s to a
beta must start with one portal into the LEFT column-c PP pair in s's
band and remain inside the left flank afterwards. Starting into the
central copy cannot reach any beta without revisiting s. Neither right
beta endpoint is reachable. The selected left beta endpoint is the
path's only possible additional free end.

This isolation statement permits arbitrary internal auxiliary changes;
it does not protect source or donor tails or restrict original cycle use.

### Lower bound for every matching replacement

The symmetric difference A triangle N has degree at most two. Its only
degree-one vertices are s,t, because both matchings cover every original
PP vertex, A covers no original free end, and N additionally covers just
s,t. Hence it consists of an A/N alternating path from s to t and
alternating cycles. The path starts and ends with N edges. All its N
edges belong to N setminus A, so its new-edge count is at most C(N).
Extra alternating cycles cannot lower that cost.

By isolation, the path's first edge is a portal. After it, every new
edge is a grid edge inside the left flank. Project a physical vertex to

    pi(row,column) = (floor(row/2), column).

An old vertical PP edge has zero displacement under pi. A grid edge
changes either its column by one, or its band index by at most one;
it never changes both. Therefore a tail of the alternating path using
L new grid edges has quotient Manhattan displacement at most L. This
holds for any finite walk, including detours: sum the coordinate-step
inequalities and use the triangle inequality.

For s_u the portal enters band 2 at column c. The quotient distances to
t_u,t_l are respectively 2 and W/2+H. Including the portal gives C>=3.
For s_l the portal enters band r/2 at column c. The two distances are

    distance to t_u = W/2+2,
    distance to t_l = H.

Including the portal proves C>=min(W/2+3,H+1). This bound holds for any
complete N on E, whether coherent or not and regardless of its internal
changes on any original component. It is not merely a shortest-path
bound for the old fixed-owner network.

### Explicit repairs attaining all bounds

The upper-end repair is the previously known five-edge alternating path

    s_u, (4,c), (5,c), (5,c-1), (4,c-1), t_u.              (3)

Its edges alternate new, A, new, A, new. Replacing the two A edges by
the three new ones gives cost three, for every H as well as every W,d.

For s_l to t_u, start

    s_l, (r,c), (R,c), (R,c-1), (r,c-1).

Then, for j=r,r-2,...,6, take the new vertical grid edge
(j,c-1)--(j-1,c-1), followed by the A edge to (j-2,c-1).
Finally take (4,c-1)--t_u. There is one portal, two horizontal new edges,
and W/2 new vertical edges. Cost is W/2+3.

For s_l to t_l, start

    s_l, (R,c), (r,c), (r,c-1), (R,c-1).

For j=1,...,H-1, take the horizontal grid edge from column c-j to c-j-1
in row R when j is odd and row r when j is even. After every such step
except the last, take the vertical A edge to the other row. Since H is
even, the last step ends at (R,c-H)=t_l. Cost is one portal followed by
H horizontal new edges, namely H+1.

All displayed paths are simple. Their internal vertices are old PP
vertices, and their old edges belong to A. Flipping along any of them
therefore preserves every old PP coverage and covers exactly s,t.

For coherence, use the full-domain signing with the chosen source and
the chosen left beta. All M and A edges on that beta cross signs.
Each displayed path first opens exactly one column-c two-edge cycle,
then enters the beta at a vertex whose A-first continuation ends at the
chosen t. Every edge of that continuation alternates A,M and crosses.
Its entry vertex has sign plus because t has sign plus and the
continuation has even length. Orient the opened two-edge cycle with
its portal entry plus and its exit minus. With s minus, the portal
and the next grid edge both cross. Every other retained A edge crosses.
Thus the complete replacement is coherent. The full-domain theorem,
with k=1,b=2,g=7 and one selected alpha/beta pair, gives final (0,1,8).
The real resource consumed is one original beta, not the opened cycle.

## 3. Unbounded cost from fixing the wrong endpoint

Take W=4q, H=2q, any d>=1, and q>=2. Equation (2) becomes

    C_u=3,             C_l=2q+1.

Thus no uniform bound on the number of auxiliary pairs replaced can
hold after an arbitrary alpha endpoint is fixed: the lower endpoint
requires at least 2q old PP deletions, whereas two deletions suffice
from the upper endpoint of the very same original alpha.

This is an obstruction to an endpoint-insensitive bounded-repair rule.
It does not rule out bounded repair when endpoint choice is optimized,
nor prove a lower bound for other enlarged candidate relations. The
target physical margin (1) stays strictly positive. General grid
compensation, the universal 5/6 improvement, and triple equality remain
open. Global packet resources and the outside-overlap correction must
still be counted once.

## 4. Validation scope

The companion checker passes 127 physical models, 254 endpoint shortest-walk
checks, 381 complete coherent repairs and 1,016 portal witnesses. It
reconstructs the three physical copies and their
candidate relation, checks feasibility, serial freezing and unique actual
matching, and verifies all eight portal identities and the isolated
left-flank geometry. An independent directed alternating-walk search
checks the cost formula on the stated finite controls. Each displayed
repair is reconstructed as a complete matching and independently checked
for coherent signs, domain, original resource identity and final inventory.
Enumeration supports the coordinate proof; it does not replace it.

The standalone Lean development compiles all seven named audited statements
in Lean 4.33.0, using only propext and Quot.sound, with no sorry, native
evaluation or new axioms. It verifies quotient-step telescoping and its
cost consequences from supplied coordinate-walk hypotheses. It does not
formalize the physical construction or matching symmetric difference.
Execution records are `output/port-choice-rematching-cost-validation.json`
and `output/port-choice-rematching-cost-lean.json`.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_port_choice_rematching_cost.py --output output/port-choice-rematching-cost-validation.json

    lean --stdin < formal/SubQuorum/PortalRematchingCost.lean

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
