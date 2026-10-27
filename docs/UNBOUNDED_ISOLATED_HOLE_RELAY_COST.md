# A single adjacent-payment defect can require arbitrarily many actual relay edges

The [preceding detour cover](ISOLATED_HOLE_OBSTRUCTION_AND_MATCHING_DETOURS.md)
repairs one isolated-hole defect with one actual matching edge. That cost is
not universal: for every k>=1 there is a feasible (4k+2)-square board at exact
half-area, with adjacent-hole matching defect ONE, for which every complete
vertex-disjoint alternating-path payment uses at least k actual matching edges.
An explicit actual matching attains this lower bound using a single path of
length 2k+1 and otherwise adjacent payments. For k>=2, the augmented local
cover with only length-three forced-hole detours still fails, even fractionally.
More generally, no fixed maximum detour length suffices for that cover rule.

The lower bound holds under ANY rematching on the same endpoint footprint;
the explicit equality construction is for the matching specified below.
The assertions concern the named path/cover certificates, not a failure of
the numerical half-area target. No freezing condition is assumed.

## 1. Actual endpoint footprint and a perfect matching

Let k>=1, n=4k+2, V={0,...,n-1}^2, and let

    h=(2k,2k),
    P={0,...,4k}^2 minus {h}.

The endpoint footprint is the odd square in the top-left corner with its
central even-colour site removed. Q=V\P is the union of {h} and the outer L

    L={(r,4k+1):0<=r<=4k+1}
       union {(4k+1,c):0<=c<=4k}.

Choose the following actual matching M:

* vertical edges (r,c)--(r+1,c), every c=0,...,4k, with
  r=0,2,...,2k-2 and r=2k+1,2k+3,...,4k-1;
* in row 2k, horizontal pairs covering columns 0,...,2k-1 and,
  separately, columns 2k+1,...,4k.

The first group covers all rows except the central one. The second covers
the central row except h, in two intervals each of even length 2k.
These edges are disjoint and cover exactly P. In particular

    |P|=(4k+1)^2-1=16k^2+8k,  |M|=8k^2+4k.              (1)

M need not be unique. Statements below that are independent of M explicitly
apply to every perfect matching of this same P.

## 2. A sharp feasible selection with only one adjacent deficit

Let T be all odd-colour sites of L. Let H=Q\T. Traversing L from (0,4k+1)
down the last column, then left along the bottom row, gives a simple path
of 8k+3 vertices, alternating T,H,T,...,H,T. Consequently

    |T|=4k+2,  |H intersect L|=4k+1,  |H|=4k+2,
    J=|M|+|T|=8k^2+8k+2=n^2/2.                          (2)

T is independent. Every site of L except its bend has precisely one P
neighbour, and the bend (4k+1,4k+1) has none. Hence every selected site has
exactly one occupied neighbour, its P neighbour; the bend is even and unselected.
The selection is feasible under every actual rematching on P.

The hole h is isolated in Q because all four of its neighbours are in P.
No adjacent T-to-H matching can use h, so its size is at most 4k+1. This
bound is attained by pairing consecutive sites of L, leaving its final T
unmatched. Thus the exact adjacent deficiency is

    |T|-nu_adj=1.                                       (3)

## 3. At least k actual edges are necessary under every rematching

Use the same payment model as in the preceding note: an injection T->H
realized by vertex-disjoint paths, each either an adjacent edge, or an odd
path alternating non-M/M/non-M/.../M/non-M with all internal vertices in P.
An odd path with a actual M edges has length 2a+1.

By (2) any injection is a bijection, so some selected vertex must be paid
to h. Every selected vertex lies on L. Its Manhattan distance from h is at
least 2k+1: its row or column is 4k+1, while both coordinates of h are 2k.
The path ending at h therefore has length at least 2k+1 and uses at least
k actual M edges. A path is simple, so these edges are different. This
lower bound holds for EVERY perfect matching of P: the distance, equality
of |T| and |H|, and location of T do not depend on the rematching.

This is stronger than merely requiring one nonadjacent payment. A single
defect can have unbounded relay-edge cost, despite J remaining exactly half.

## 4. The explicit matching attains k with no repeated hole or edge

For M from Section 1 take the straight path

    (4k+1,2k), (4k,2k), (4k-1,2k), ..., (2k,2k)=h.       (4)

It has length 2k+1, with k actual vertical M edges at its alternating
internal steps. All internal vertices belong to P, and its initial site
t*=(4k+1,2k) belongs to T. The k matching edges in (4) are different.

The index of t* in the traversal of L starting at index zero is 6k+2,
which is even. Delete t* from L. The two remaining subpaths have respectively
6k+2 and 2k vertices, both even. Pair consecutive vertices in each subpath.
Each pair contains one T and one H and is an adjacent grid edge. There are
4k+1 such pairs. They cover exactly T\{t*} and H\{h}.

Together with (4) they form a complete vertex-disjoint payment system: all
short paths lie on L\{t*}; the long path has no other site of L and lies
otherwise in P union {h}. Every hole is used once, and exactly k physical
M edges are used once. Equations (3),(4) prove the exact separation

    adjacent deficit = 1,    minimum relay-edge cost = k               (5)

for the explicit M. The arbitrary-rematching assertion is the lower bound
k; no claim is made that every rematching attains that cost.

For completeness, a payment system does exist for every rematching of this
P, although its minimum cost can be larger. Choose any perfect matching N
of the even square V, for example its horizontal dominoes. The standard
decomposition of M union N into alternating paths and cycles gives paths
whose endpoints are exactly Q and whose internal vertices belong to P.
Every path starts and ends with an N edge, so has odd length and opposite
checkerboard-colour endpoints. Here every odd Q site is in T and every
even Q site in H, so these paths give the required bijection. Common M/N
edges form doubled-edge components entirely in P and can be omitted.
This is the standard matching decomposition, not an additional numerical
result or a new claim of a bounded repair cost.

## 5. No fixed-length forced-hole cover suffices

The only forced-hole site in Q is h: it has four P neighbours, whereas sites
of L have at most one. Thus all eligible forced-hole singletons have the
same even colour. Q is colour-balanced because V is balanced and P is
covered by a matching. Every eligible adjacent pair and endpoint-free unit
square is colour-balanced.

Fix an integer ell>=0 and allow, in addition to those local pieces,
forced-hole detour pairs joined through at most ell actual M edges by an
alternating path with internal vertices in P. Their length is at most
2ell+1. If k>ell, such a detour cannot contain h: its other endpoint would
have to lie on L at distance at least 2k+1. No other forced hole is available,
so no eligible detour pair exists at all, under any rematching of P.

The isolated h must therefore be covered by its forced-hole singleton.
Subtracting odd-colour coverage from even-colour coverage yields zero on Q,
zero on every balanced piece and a positive contribution from this singleton.
This is impossible for an ordinary partition or a nonnegative fractional
exact cover. In the fractional case exact coverage at h forces its singleton
weight to be one, and no negative or odd-colour singleton weight can cancel it.

Taking ell=1 and k>=2 excludes the length-three extension itself. Taking
k>ell for every fixed ell excludes any fixed detour length for this rule.
The failure is proved by geometry and conservation; it is not inferred
from a finite exact-cover search.

## 6. Research consequence and checks

The q-cell theorem and (5) isolate two different costs: the number of
nonadjacent payments and the number of actual relay edges. The first can
grow as q with one actual edge per payment; the second can grow as k even
when the first is one. Neither can be replaced by the other in a uniform
resource estimate. Changing M cannot evade the latter geometric lower bound.
An arbitrary-length proof must track a whole path's actual resources and
interactions, or use different pieces. It cannot simply add a bounded menu
of forced-hole detours to the preceding local cover and assume universality.

The verifier checks the explicit family, actual matching and sharp selection,
the unique forced hole, distance, adjacent deficiency and complete disjoint
payment witnesses for k=1,...,40. A general proof is given above. The new
Lean kernels verify the arbitrary-k distance estimate and the deduction
from alternating path length to required actual edges; the geometric
matching/path adapters and decomposition remain written. No submitted
manuscript, Mail, public main/PR3, C4 or shared CI is modified.

The [separate independent review](../output/unbounded-hole-relay-review.json)
is still live after a broker browser-input failure. The earlier q-cell ACCEPT
does not cover this later theorem. The mathematical evidence here is the
written all-k proof, local coordinate controls and two conditional Lean kernels;
no independent acceptance is claimed while the original task remains pending.
