# Exact receiver-overlap correction and unbounded PP boundary-source collisions

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We correct the scope defect identified by the independent review of the
PP-path note, by deriving the precise correction for arbitrary feasible
configurations. Separately, an explicit fully frozen family has arbitrarily
many disjoint PP paths, each joining two first-boundary source intervals.
Its connector graph has no cycles: even acyclicity does not preserve the
native proof's injection of boundary sources into different joint paths.
The packet bound remains true for the family.

## 1. Original receivers overlap only at a diagonal endpoint tile

Work on an even-by-even finite grid with its original 2-by-2 physical tiles.
Let (T,M) be any feasible pair, P the actual matching endpoints, and let K
range over the connected components of the graph induced by P. Define

    R_K = {physical tiles meeting K},
    rho_K = |K|/2 + sum_{Q in R_K} (|T intersect Q|-2).

Each actual matching edge belongs to one K, so |K| is even. For a tile Q
meeting P, let m_Q be the number of distinct endpoint components meeting Q.

If m_Q>=2, choose endpoints from different components in Q. They cannot be
adjacent, hence occupy opposite corners. Neither remaining corner can be an
endpoint: it is adjacent to both chosen endpoints and would join the components.
Neither can be selected: it would see two occupied neighbors. Thus Q contains
exactly two diagonal endpoints, from two different components, and two blanks.
In particular m_Q=2 and |T intersect Q|=0. Conversely a tile with precisely
two diagonal endpoints need not have m_Q=2: the endpoints might be connected
outside Q. We count only tiles where their GLOBAL endpoint components differ.

Let N be the number of these shared-component tiles. Comparing the sum of
the component charges with the charge of their receiver union, defined by
rho_union=|M|+sum_{Q meeting P}(|T intersect Q|-2), gives

    rho_union = sum_K rho_K +
                sum_{Q meeting P} (m_Q-1)(2-|T intersect Q|)
              = sum_K rho_K + 2N.                     (1)

This is an exact all-size identity. Each shared tile contributes its penalty
once, even though it occurs in two component receiver lists. It has no
selected corners to change the weight. A disconnected LOCAL endpoint profile
alone is insufficient; the component labels must come from the whole graph.

Each endpoint in a shared tile has two blank neighbors inside Q and at most
two occupied neighbors outside Q. Therefore if every endpoint has occupied
degree at least three, N=0. This recovers the receiver disjointness of the
single-terminal setting. It is the specific reason that setting allowed an
additive receiver ledger.

## 2. Correct global ledger, with disjoint physical packets

Let J_1,...,J_s be disjoint unions of original physical tiles. Require every
original endpoint-component receiver meeting a packet to lie wholly inside
that packet. Individual bands within a packet need not have that property.
An outside receiver cannot intersect a packet: any such tile would contain
an endpoint in the packet, invoking the closure condition.

Put S_j=|J_j|/2-|T intersect J_j|-|P intersect J_j|/2. Let q be the sum
of positive rho_K outside all packets, R_out the absolute sum of negative
outside rho_K, and D_out the deficit sum 2-|T intersect Q| on outside
endpoint-free tiles. Let N_out count shared-component tiles outside packets.
The correct arbitrary-feasible identity is

    mn/2-|T|-|M| = sum_j S_j + D_out-q+R_out-2N_out.    (2)

To prove it, partition physical tiles into packet tiles, outside endpoint-free
tiles and the outside receiver union. The first class contributes sum S_j
directly; the second contributes D_out. The last contributes minus its union
charge, which is minus sum rho_K minus 2N_out by (1). These classes are
disjoint. Receiver overlaps INSIDE a packet are already included in S_j,
so they must not also be charged in N_out.

An endpoint-free feasible tile has at most two selections, since any three
corners include a selection adjacent to two other selections. Hence D_out>=0,
and R_out>=0 by definition. If the local PP-path reserve inequality proves
S_j>=k_j+t_j, then

    q+2N_out <= sum_j(k_j+t_j)                         (3)

is sufficient for the coefficient-one, half-area bound. One may also include
the actual unused D_out+R_out on the right. In the single-terminal setting
N_out=0 and (2),(3) reduce to the previous global corollary. The local PP-path
identities require no restriction and remain unchanged.

For a complete check of the reviewer's counterexample, take the 8-by-4 board,
T empty, and actual matching

    (1,0)--(2,0), (3,1)--(4,1), (6,1)--(6,2).

The sole packet is rows6,7 and all four columns. Its first and last columns
are BB, k=t=1, S=3. The outside charges are -3,-3, D_out=6, q=0,
R_out=6 and N_out=1. The erroneous uncorrected expression gives 15, whereas
(2) gives 3+6+6-2=13, the actual margin 16-3. This is a ledger counterexample,
not a counterexample to the target bound. Credit for identifying this omitted
scope condition and concrete example belongs to the independent review.

## 3. A fully frozen source-collision family

Choose even W>=6,H>=4 and an integer r>=1. Start with the ORIGINAL neutral
configuration N(W,H) from NEUTRAL_PAIR_DONOR_SATURATION.md, whose board has
H+8 rows and W+12 columns. Add four selections

    (2,4), (2,5), (2,W+4), (2,W+5).                    (4)

They form two disjoint horizontal TT pairs. All original occupied vertices
have row at least4, so (4) is separated from them by blank row3. Each new
selection sees exactly its paired selection; there are no other new contacts.
The original matching and its unique-matching and complete-freezing proofs
therefore persist for every W,H. No added selection is an endpoint or an
extra retained support inserted by completion.

Transpose and then move every vertex one column to the right:

    (old row,old column) |-> (old column,old row+1).

The new block has W+12 rows and H+10 columns. Stack r identical blocks by
row translations j(W+12), j=0,...,r-1. Occupied rows in each block are
4,...,W+5, so distinct blocks have no occupied adjacency. The endpoint
components and unique matchings are independent, and the whole pair fully
freezes. It has

    |T|=r(H+11), |M|=r(W+H).

Take J to be ALL rows and columns 2,...,H+7. Its width n=H+6 is even;
it consists of original physical tiles, since the first column is even and
the width is even. Its k=r(W/2+6) two-row bands have BB first and last
columns, so t=k. All original selections and all endpoint-component receivers
lie inside J. The two outside column pairs are completely blank. Thus this
obstacle does not rely on a physical phase mismatch or partial receivers.

## 4. Exact PP inventory and collision of first-boundary sources

Use actual column coordinates in J. In each block there is one TP--TP path
at column5, whose band indices are

    2,3,...,W/2+2,

plus the block's band offset j(W/2+6). It has W/2 matching edges and
W/2-1 interior PP columns. It comes from the original upper elbow bar.
Both TP terminals have exactly one original selected neighbor and freeze
through retained support in the known complete certificate.

All W/2-1 lower-bar edges are PP matching loops. The right leg gives H/2
single-edge TP--BP paths and its left column gives H/2-1 such paths. The short
tip and neutral pair contribute one more each. These exhaust

    W/2 + (W/2-1) + (H+1) = W+H

matching edges in a block. Hence, in the whole packet,

    alpha=r, beta=0, gamma=r(H+1),
    PP loops=r(W/2-1).                                (5)

At EACH terminal of each TP--TP path, the adjacent column4 is BB, whereas
column6 is BP. The ONLY adjacent-BB port is therefore on the LEFT side.
Under the native connector convention both are outgoing RIGHT endpoints of
BB--TT intervals. There is no direction with one outgoing and one incoming
port that respects this convention.

The added selections (4) create TT column3 in each of the two terminal bands.
Consequently each adjacent BB column4 belongs to the exact alternating
interval

    column2 BB -- column3 TT -- column4 BB.             (6)

It contains the first-column boundary source of that band and ends immediately
before its terminal TP column5. The two intervals are distinct and belong to
different bands. Their matching path therefore joins two different
FIRST-BOUNDARY source intervals.

Even ignoring directions and joining these pairs by undirected connectors
does not recover the native boundary injection. The r connectors have disjoint
interval endpoints, so their graph is r isolated edges and otherwise isolated
vertices, with NO cycle. Among the k first-boundary intervals, exactly 2r are
paired this way, so the number of joint components meeting the first boundary is

    k-r.                                               (7)

The k final BB intervals are distinct isolated vertices and meet none of those
first-boundary components: their actual endpoint column H+7 is odd, whereas
the intervals in (6) end at even column4, and no connector uses a final interval.
Thus the joint components that meet either boundary number exactly

    2k-r,                                              (8)

r less than the native count k+t=2k. This loss is unbounded in r. Acyclicity
alone cannot stop boundary sources from merging; the one-in/one-out orientation
and boundary ownership in the native theorem were essential.

## 5. The target holds, with exact unused reserve

Direct whole-packet counts, or the PP ledger, give

    S_J=r(WH/2+2W+4H+25),
    L=r(WH/2+2W+4H+26),
    L-alpha=S_J.

The connector graph has L vertices and r independent edges, hence L-r=S_J
components. Besides the 2k-r components meeting a boundary, it has precisely

    S_J-(2k-r)=r(WH/2+W+4H+14)

components meeting neither boundary. In particular

    S_J-(k+t)=r(WH/2+W+4H+13)>0.                       (9)

Thus the family disproves a UNIVERSAL boundary-source injection after PP-path
contraction, even for physical-tile-aligned receiver-closed packets with unique
matching and complete freezing. It does not disprove the PP identity, the
native-support theorem, or the desired packet/global bound. The extra interior
interval reserve in (9) pays for the collisions here. A general proof must
justify enough such reserve rather than assuming acyclicity keeps sources apart.

## 6. Proof, verification and remaining problem

Sections1--5 are uniform proofs in all parameters. Finite controls and scoped
Lean verification are separate companion artifacts. The graph/coordinate
adapters remain written; no finite search is used as an all-size proof.

The permanent checker develop/check_receiver_overlap_and_pp_source_collision.py
passes 6589 receiver-ledger models, including 66 with receiver overlap and
explicit globally connected diagonal controls. It also passes 425 uniquely
matched, fully frozen source-collision packets: 351 parameter triples,
24 symmetry images and 50 multiplicities through r=50. There are 39320
matching edges and 2150 source collisions across those packets. The physical
receiver closure is checked separately in 351 parameter triples and all
24 symmetry images. Exact results are in
output/receiver-overlap-and-pp-source-collision-validation.json.

Local Lean4.33.0 passes 14 scoped theorems and 14 individual axiom audits,
without errors, warnings, sorry or native evaluation. The local 81-profile
lemmas use kernel reduction; the arbitrary-size inventory/global arithmetic
uses induction and ordinary axioms. The execution scope and audit are in
output/receiver-overlap-and-pp-source-collision-lean.json, with source
formal/SubQuorum/ReceiverOverlapAndPPSourceCollision.lean. This does not
formalize the entire grid-to-graph or coordinate/freezing adapter.

Run the permanent finite controls with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_receiver_overlap_and_pp_source_collision.py --output output/receiver-overlap-and-pp-source-collision-validation.json

The original PP note's initial review was REVISE, because of the global scope
defect repaired by Sections1--2. Its local results and phase computations were
confirmed, not rejected. There is no final ACCEPT inferred from that initial
answer. Further review status is recorded separately.
The original follow-up task is aa9e1dd1-aab2-4a8a-b5cb-7b59bb23d3fe in
conversation conv_7d6fdd1e46228804, original streaming session35550. Its
29605-character prompt agrees exactly with the service session. It covers
the corrected prior note and this complete new general proof, not execution.
It remains dispatched/waiting_response at this record; no new verdict is
inferred. See output/receiver-overlap-and-pp-source-collision-review-live.json.

The next problem is to charge source collisions and any possible connector
cycles to disjoint ORIGINAL interior interval or BP--BP reserves, with the
outside overlap term in (2) included whenever single terminality is absent.
No such universal geometric charge theorem is proved here. General grid
compensation and triple equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
