# Two-connected selected gaps with fixed maximum degree

The later [sharpness theorem](SHARP_MINIMUM_TWO_DEGREE_BOUND.md) improves
the lower family in this note and closes the minimum-degree2 coefficient
for every maximum degree>=6, including two-connectivity. The present
construction and its original audit remain valid as stated.

For every integer p>=2 and k>=1 there is a finite simple two-connected
bipartite graph H_(p,k), with minimum degree 2 and maximum degree 2p+2,
and a specified inclusion-minimal two-star-forming set S, such that

    n=(12p+2)k, |S|=8pk, beta_2(H_(p,k))=7pk,
    |S|-beta_2(H_(p,k))=pk=n/(12+2/p).                  (1)

S induces 2pk copies of P3 and 2pk isolates. Its stars need not be induced
in the definition of formation, as in the preceding notes. Beta is the
unrestricted dissociation number. We do not assert an exact value for the
upper two-star-forming number SF, or graph-sharpness of a coefficient.

In particular p=2 gives two-connected graphs of minimum degree 2 and
maximum degree 6 with n=26k, |S|=16k, beta=14k and selected gap n/13.
This is a fixed maximum-degree, fixed-connectivity lower family. It does
not concern regular graphs or full rectangular grids.

The proof is a local partition argument and an explicit gluing operation,
not an extrapolation from finite optimization.

## The base H_p and its selected set

Start with the balanced graph G_(p,p) from SHARP_SELECTED_STAR_GAP.md.
For j=0,...,2p-1, its six vertices have labels 6j through 6j+5. Write

    c_j=6j, x_j=6j+1, y_j=6j+2, i_j=6j+3,
    a_j=6j+4, b_j=6j+5.

The local edges are c_jx_j,c_jy_j,x_ja_j,y_jb_j,i_jb_j.
Call indices0,...,p-1 the left wing and p,...,2p-1 the right wing.
All 2p witnesses {a_j,b_j} in the left wing are joined to all 2p
witnesses in the right wing. There are no other old edges.

Add two vertices u_L=12p and u_R=12p+1. Join u_L to every i_j in the
left wing and to y_0. Join u_R to every i_j in the right wing and to y_p.
These are all the base edges. S consists of every c_j,x_j,y_j,i_j.

The two wings have opposite orientations: the witnesses, centres and u
of one wing share a colour, and its leaves and isolates have the other
colour. Complete cross-witness edges therefore respect bipartiteness.
The selected centres and ordinary leaves have degree2, the distinguished
y vertices have degree3, each i has degree2, each u has degree p+1,
each a has degree2p+1, and each b has degree2p+2. Thus the claimed
minimum and maximum degrees hold.

Every outside witness has an active selected leaf neighbour. Every u
has a distinguished active selected leaf neighbour. Hence S is forming.
Removing a selected leaf x_j or y_j leaves its witness a_j or b_j
unformed: a_j has no selected neighbour, or b_j has only the inactive
isolate i_j, respectively. Removing c_j leaves a_j with only the now
inactive x_j. Removing i_j makes i_j itself an outside vertex with no
selected neighbour. These are literal deletion failures, so S is
inclusion-minimal. Its induced components and size are as stated.

## A local proof of beta(H_p)=7p

A dissociation set has induced maximum degree at most one. Partition a
wing, including its u, into the following disjoint vertex sets:

- {u,y_0,b_0,i_0} in the left wing (use index p in the right wing);
  this induces C4, whose dissociation number is2.
- {c_j,x_j,a_j} for every index in that wing; each induces P3.
- {y_j,b_j,i_j} for every other index in that wing; each induces P3.

There are 2p-1 of the P3 blocks. Every dissociation set therefore uses at
most 2+2(2p-1)=4p vertices of a wing. Edges between blocks only restrict
the set further.

If no witness is selected in a wing, partition its other vertices into
p selected P3 blocks {c_j,x_j,y_j} and the star consisting of u and all
p isolates i_j. The p P3 blocks contribute at most2p. Since p>=2,
the star K_(1,p) contributes at mostp, so the whole wing contributes
at most3p. With exactly one selected witness the bound is at most3p+1,
by deleting that witness and applying the previous bound.

Now let Q be any dissociation set in H_p. If both wings contain selected
witnesses, completeness of their cross adjacency forces exactly one
witness in each wing: otherwise a selected witness has at least two
selected neighbours. This case gives |Q|<=6p+2<=7p. If at most one
wing contains witnesses, its bound is4p and the other wing's is3p,
giving |Q|<=7p (and at most6p if both are empty).

For a matching lower construction take all leaves and witnesses in the
left wing, and {c_j,x_j,i_j} in the right wing. Take neither u. There
are 4p+3p vertices. Every selected left witness is paired with its own
leaf, and every right centre is paired with x_j; the right isolates
are isolated. No selected cross-witness edge occurs. This proves the
exact unrestricted optimum beta(H_p)=7p, with a maximizer avoiding both u.

## Two-connectivity

The cross-witness backbone is K_(2p,2p), hence two-connected. For each
index j add the ear a_j-x_j-c_j-y_j-b_j, with distinct backbone endpoints
and new internal vertices. In a wing choose two distinct indices j0,j1
(possible since p>=2), then add the ear

    b_(j0)-i_(j0)-u-i_(j1)-b_(j1).

For every remaining index j add the ear b_j-i_j-u. Finally add the
extra edge u-y_(j0), using j0=0 or p as appropriate. This builds precisely
the base graph from a two-connected graph by adding ears and edges.
For completeness, after deleting any one vertex an ear's surviving
internal path segments each attach to a surviving endpoint, while the
old graph stays connected. Thus ear addition preserves connectivity
after every single deletion. This proves two-connectivity without
appealing to finite graph checks.

## Connect any number of bases without increasing beta

For k=1 use H_p. For k>=2 take k disjoint copies of H_p and add

    u_L in copy j -- u_R in copy (j+1 mod k),
    for j=0,...,k-1.                                   (2)

Orient all copies alike. These new edges join opposite colours and
have two outside endpoints, so selected adjacency and every deletion
failure above remain unchanged. The degree of each u increases by1
to p+2, which is at most2p+2. The minimum and maximum remain exact.

Restricting a dissociation set to each base gives an upper bound7pk.
The explicit maximizer above avoids every u, so the union of these
maximizers remains dissociation after (2) and attains7pk. This proves
exact beta additivity here. No deletion-safe-edge hypothesis is needed:
we add edges and have a common optimum avoiding all their endpoints.

Each base remains connected after deleting any vertex. The inter-base
cycle remains connected; deleting a u removes only one of its cycle
edges and leaves a connected path of bases. For k=2 the two cross edges
have distinct endpoints and one survives each deletion. Thus the full
graph stays connected after every vertex deletion and is two-connected.
This completes the all-p, all-k proof of(1).

## Consequence and limits for fixed maximum degree

For every even Delta=2p+2>=6, the family gives the lower coefficient

    p/(12p+2)=(Delta-2)/[12(Delta-2)+4].                 (3)

For an arbitrary maximum-degree allowance D>=6 use
p=floor((D-2)/2); the constructed maximum degree is at most D.
For D=6 this is1/13. The free-unused-vertex theorem supplies the upper
coefficient5/62 for all specified selected-star minimal sets with
minimum degree at least2 and maximum degree at most6. Consequently

    1/13 <= best asymptotic coefficient in this class <= 5/62.

The lower family itself is two-connected. The present construction supplies the lower endpoint; the separate
sharpness theorem now attains the upper endpoint. No higher-minimum-degree,
regular-extremality or unit-grid claim is made here. For Delta=4 the earlier separate quartic family remains
relevant; it is not subsumed by this construction.

## Verification status

Run `python3 scripts/check_two_connected_bounded_degree_gaps.py` with
assertions enabled. The all-parameter proof above is independent of finite
enumeration. The standard-library checker checks28 physical models with
p in{2,3,4,5,8,16,32} and k in{1,2,3,7}: the block partitions,7,280 literal
deletion failures, every explicit attaining set and the degree counts.
At p<=8 it checks all3,562 single-vertex deletions. Larger connectivity
conclusions use the general ear/gluing proof, not unstated sampled deletion
checks. The largest physical model has2,702 vertices.

Independent one-part optimization checks bases p=1,2,3; a separate
forbidden-triple recurrence also checks p<=2. The p=1 control lies outside
the theorem: its beta is8 rather than7, showing why p>=2 is required.
The final exact-source proof and unchanged-checker execution audit returned
ACCEPT. The reviewer reconstructed/hash-checked all10 files, ran both
original entry points with assertions to exit0, and reproduced both complete
reports byte-for-byte(24,963 and11,730 bytes). No proof, code or report
correction was needed. See
`../output/degree-refinement-and-lower-family-review.json` for the complete
response, frozen manifest and execution scope. Separate helper-main suites
were not rerun.
No new Lean or historical-priority claim is made.
