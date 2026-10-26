# A sharp component cut obstruction and a capacity-two square exchange

Subsequent research [refutes universal rematching alone](UNIQUE_MATCHING_HOLE_COMPENSATION_BARRIER.md): a sharp all-width footprint has a unique matching and no feasible endpoint-only certificate. A guarded-hole cover and one-selection relocation provide alternative compensation there. The conditional transport lemmas below remain valid.

For a fixed actual matching, the ownership criterion in
[the turning compensation note](TURNING_ACTUAL_EDGE_COMPENSATION.md) is not
universally feasible. We give a sharp, feasible `h × 4` family for every even
`h>=6` with an explicit Hall deficiency of one actual edge. Unlimited routing
inside individual tiles cannot bridge its empty intercomponent cut.

The obstruction concerns that certificate and transfer support. Every board in
the family has `J=area/2`; it does not refute the numerical target. A single
alternating square exchange repairs the certificate while keeping the endpoint
set, selected vertices and matching size. That exchange changes two actual
matching edges, so it is explicitly outside a rule that freezes M.

## 1. Exact assumptions and coordinates

Use ordinary grid adjacency and the aligned disjoint 2-by-2 tiling. As before,
`P` is the endpoint set of a matching M, `T` is disjoint from P, `H` consists of
the remaining vertices, and each selected vertex has at most one occupied
neighbour in `O=P union T`. For a tile B write

    q_B=|T intersect B|-|H intersect B|,
    d_B=max(0,|O intersect B|-2).

Fix any even `h>=6`, let `k=h/2`, and use rows `0,...,h-1` and columns `0,...,3`.
Set

    T={(0,1),(1,0),(0,3),(h-2,0),(h-1,1),(h-1,3)},
    H={(0,0),(0,2),(2,0),(h-3,0),(h-1,0),(h-1,2)}.

All other vertices are P. The matching consists of

* `(1,1)--(1,2)` and `(h-2,1)--(h-2,2)`;
* `(r,3)--(r+1,3)` for odd `r=1,3,...,h-3`;
* `(r,c)--(r+1,c)` for even `r=2,4,...,h-4`, `c in {1,2}`;
* `(r,0)--(r+1,0)` for odd `r=3,5,...,h-5`.

The last range is empty for h=6. Its occupancy is

    H T H T
    T P P P
    H P P P
    H P P P
    T P P P
    H T H T

**Feasibility for every h.** In column zero, precisely rows `3,...,h-4` are P,
paired consecutively by the last family. In columns one and two, rows one and
`h-2` are covered by the two horizontal end edges, and rows `2,...,h-3` by the
vertical even-row family. In column three, rows `1,...,h-2` are paired by the
odd-row vertical family. Thus every P vertex is covered exactly once, with no
T or H endpoint and no non-grid edge.

The top selected vertices `(0,1),(1,0),(0,3)` have respectively the unique
occupied neighbours `(1,1),(1,1),(1,3)`. The other existing neighbours are holes.
Reflection in the horizontal midline proves the same assertion for the bottom
three selected vertices. This proves the occupied-degree hypothesis at every
height, independently of finite enumeration.

There are six selected vertices, six holes, and `2h-6` matching edges. Hence

    J=6+(2h-6)=2h=area/2.                                   (1)

## 2. The violated cut: one missing physical resource

Index tiles by `(i,j)`, `0<=i<k`, `j in {0,1}`. Let

    U={(0,0),(k-1,0)} union {(i,1):0<=i<k}.

The two left end tiles are positive, with one P and two T each. The two right
end tiles are neutral, with two P and one T. The `k-2` intermediate right tiles
are all-P. These form a single matching-component path in the order

    (0,0),(0,1),(1,1),...,(k-1,1),(k-1,0).                  (2)

No actual matching edge leaves U. The only horizontal matching edges occur at
the two ends; all other matching edges stay in one tile column.

Each of the four end tiles in U has demand one, and each intermediate right
tile has demand two. Therefore

    sum_{B in U} d_B=4+2(k-2)=2k=h.

Its distinct actual resources are the `k+1` path edges in (2) and `k-2` internal
right-tile edges. Thus

    |{e in M:e has an endpoint in U}|=2k-1=h-1.             (3)

The Hall condition would require `h<=h-1`. This is a written all-height
counterexample to universal fixed-M ownership and, by the equivalence in the
turning note, to universal feasible bounded endpoint charges for that M.

In particular, more all-P relay capacity, arbitrary intratile routing, turns,
revisits, or a different choice of H/V intratile passages cannot fix an empty
intercomponent cut. Any resource rule confined between tiles to the actual
matching edges and paying each physical reserve only once has the same problem.

The complementary tiles `(i,0)`, `1<=i<=k-2`, form a second path. They have
`h-5` distinct resources and total demand `h-6`, so exactly one resource can be
spared. For h=6 this is one 2P/2H tile with one internal edge and zero demand.
For h>=8 its ends are 3P/1H tiles and all intervening tiles are all-P. This
checks that the deficit is connectivity of the certificate, not absent global
numerical slack.

## 3. Signed accounting and why the reserve cannot be counted twice

Use the horizontal endpoint charges from the
[signed-strip lemma](TWO_ROW_SIGNED_BOUNDARY_COMPENSATION.md). Every tile in
this family has zero local slack. The two positive tiles give total q=+2, the
negative tiles in the complementary component give total q=-2, and all other
tiles have q=0.

Inside U, exactly the actual edges

    (1,3)--(2,3), (h-3,3)--(h-2,3)

have charge sum +1. Every other actual edge in U has sum zero. In the other
component, the total actual-edge charge is -2 and no actual edge has positive
sum. For h=6, the edge `(2,1)--(3,1)` has sum -2. For h>=8 the only negative
endpoints are `(3,0)` and `(h-4,0)`; at h=8 they belong to the same actual edge.
These assertions follow directly by applying the fixed local table to the
end/neutral/all-P/negative tile types just listed.

Thus the signed ledger is `+2-2=0`, but its two parts cannot communicate along
actual matching edges. The negative tile budget and negative actual-edge sum
are two descriptions of the same payment. They must not be added as if they
were separate reserves.

The units in the two ledgers are related exactly. On a closed tile set with
all occupancies at least two, `sum q_B=2(sum d_B-|M_inside|)`. Here signed excess
two is a deficit of one physical resource; signed payment minus two is the
one physical spare in the other component. This explains the factor two
without manufacturing a second spare.

## 4. A general capacity-two square exchange lemma

**Lemma.** Suppose a partial one-owner certificate for an actual matching M has
all tile demands paid except tile B, which owns exactly `d_B-1` resources.
Assume two adjacent tiles A,B contain an all-P square straddling their boundary.
Its two opposite matching edges are internal edges `e_A` of A and `e_B` of B.
Assume `e_A` is unused and `e_B` is owned by B. In particular `d_B>=2`.

Replace these two matching edges by the other two sides of the square, each
joining A to B. Assign both new edges to B; retain every other old owner. Then
this is a complete one-owner certificate for the new matching M'. It preserves
P, T, all demands, matching size, J and occupied-degree feasibility. It retains
every surviving old resource and its owner.

**Proof.** The four vertices were paired solely by `e_A,e_B`, so replacing them
by the two other square sides again matches exactly those four vertices and
conflicts with no other edge. The new edges are distinct physical resources,
each incident to B. Removing unused `e_A` costs no tile a payment. Removing
owned `e_B` reduces B's payment from `d_B-1` to `d_B-2`. Its two new resources
raise it to `d_B`; no other tile payment changes. Both new edges are counted
once, and no old edge is assigned twice. Because the endpoint and selected
sets are unchanged, occupancy and selected degrees are unchanged. Exactly two
edges are removed and two added, so matching size and J are unchanged. This
proves all assertions. The lemma changes M; it is not a certificate for the
original frozen matching. ∎

## 5. Explicit repair of every member of the obstructing family

Take `A=(1,0)`, `B=(1,1)` and the square on rows 2,3 and columns 1,2. Its vertical
edges are `e_A=(2,1)--(3,1)` and `e_B=(2,2)--(3,2)`. Its two horizontal sides
will be the new matching edges.

A partial certificate satisfying the lemma is available at every h:

1. In U, use every internal matching edge. On the two arms of path (2), assign
   each path edge to its endpoint farther from B. Each tile outside B owns its
   internal edges plus one arm edge and is paid exactly. B owns only `e_B`,
   leaving one unit of its demand two unpaid.
2. In the complementary left path, use every internal edge except `e_A`.
   Assign each intertile path edge to its endpoint nearer A. For h>=8 the first
   tile A receives its one unit from the next tile; every intermediate all-P
   tile receives one internal and one path edge; the last 3P tile receives its
   internal edge. For h=6 the complement is just A, of demand zero, so leaving
   `e_A` unused pays it exactly.

All old resources except `e_A` are used once; all demands except one unit at B
are paid. Apply the square exchange lemma. B loses its old internal edge and
receives the two new horizontal edges. Every tile now owns exactly its demand,
with no unused edge. The repair works for every even `h>=6` and uses the one
spare once. It neither enlarges the matching nor changes its endpoints.

This produces a precise cross-component compensation operation when rematching
is allowed. Since J is invariant under rematching, existence of a suitable
rematching could support a proof of the numerical target. We have not proved
such existence on arbitrary feasible grids; a family repair cannot establish
that universal statement. A proof requiring the original physical M to remain
fixed must instead introduce and justify another form of transfer support.

## 6. The same payment on the original matching, without changing it

The square exchange also gives a certificate expressed entirely using the
original M. This relaxes the failed requirement that every individual actual
edge have nonpositive charge; it does not require altering the given board.

**Paired-original-edge compensation lemma.** Let endpoint charges lie in `[-1,1]` and satisfy
`q_B<=sum_{p in P intersect B} sigma(p)` in every tile. Partition some actual
matching edges into pairs, each consisting of the two opposite M edges of an
all-P square; no actual edge may occur in two pairs. Suppose every unpaired
actual edge has charge sum at most zero, and for each pair the sum over its four
endpoints is at most zero. Then `J<=area/2` for the original M.

Indeed sum the tile inequalities once. Since matching edges partition P,
partitioning these edges into the disjoint pairs and remaining single edges
counts every endpoint exactly once. Thus `T-H<=sum_P sigma<=0`, equivalent to
`T+M<=area/2`. This proof spends each paired negative payment once; it does not
add a second copy of the negative tile budget.

If disjoint alternating square flips yield a matching M' with an ownership
certificate, its endpoint charges automatically satisfy this grouped rule on M:
unflipped edges are unchanged, and the total over each original square pair
is the total over the two new matching edges, which is nonpositive. The squares
have disjoint endpoint sets because their original M edges are disjoint. Thus
one can use M' to construct the charges while leaving M as the board being
certified. This implication does not prove that suitable flips always exist.

For the family of Section 5 the induced charges give

    sigma(2,1)=sigma(3,1)=-1,
    sigma(2,2)=sigma(3,2)=+1.

Hence the original edge e_A has sum -2 and the original edge e_B has sum +2.
Every other original edge has sum zero. Pair e_A with e_B on their common
all-P square: their total is zero. All tile inequalities are equalities and
all resources are accounted for once. This is an explicit all-height
cross-component compensation certificate for the ORIGINAL matching, using one
capacity-two signed payment. It coexists with the Hall obstruction because
that obstruction excludes individually nonpositive charges on every edge;
the grouped rule allows the one specified +2 edge and pays it by one -2 edge.

## 7. General transport by disjoint alternating cycles

There is a uniform version which does not count overlapping square exchanges
as separate sources of payment.

**Alternating-cycle compensation lemma.** Let M and M' be grid matchings with
exactly the same endpoint set P. Let T be disjoint from P. Suppose charges
`sigma:P -> [-1,1]` satisfy every tile inequality `q_B<=sum_{p in B}sigma(p)`
and every M' edge has nonpositive endpoint sum. Then M has a compensation
certificate partitioned into common edges and disjoint alternating cycles,
and `|T|+|M|<=area/2`.

**Proof.** At any vertex where M and M' use the same edge, that edge is a common
resource. Every other vertex has exactly one incident M edge and one distinct
incident M' edge. Thus the symmetric difference is a disjoint union of even
alternating cycles, with distinct vertices and actual M edges across cycles.
On each such cycle C, the old M edges and the new M' edges both partition the
same vertex set. Consequently

    sum_{e in M intersect C} sum_{p in e} sigma(p)
      = sum_{e in M' intersect C} sum_{p in e} sigma(p) <= 0. (4)

Common edges have nonpositive sum separately. These groups partition the
original M. If `L=sum_B(sum_{p in B}sigma(p)-q_B)>=0`, the exact ledger is

    |T|-|H| = sum_{common e} c_e
                + sum_C (positive_mass_C-negative_mass_C) - L,
    c_e=sum_{p in e}sigma(p),
    positive_mass_C=sum_{e in M intersect C}max(0,c_e),
    negative_mass_C=sum_{e in M intersect C}max(0,-c_e).

By (4), `positive_mass_C<=negative_mass_C` separately for each cycle. Every old
negative edge contributes to just one payment group; block slack is counted
once and is not added to those negative masses a second time. Distinct cycles
may visit different endpoints of the same tile; this does not create a second
copy of its q_B budget, because the tile inequalities were summed only once. Summing gives
`T-H<=0`, equivalent to the claimed bound because `|P|=2|M|`. ∎

An ownership certificate for M' supplies the required charges by the turning
lemma. A sequence of overlapping rematchings must therefore be summarized by
the FINAL symmetric difference with M before payments are counted. Adding
credits separately for each intermediate flip could spend the same original
negative edge repeatedly. The disjoint-cycle ledger avoids that issue even
when intermediate squares overlap or a matching edge disappears and returns.

This lemma is conditional on one consistent endpoint charge assignment and a
single final matching M'. It does not combine incompatible charge choices,
show that such M' always exists, or permit spending the same terminal reserve
in different cycles. In the explicit h-by-4 family there is exactly one
alternating cycle, the four-corner square in Sections 4-6, and its masses are
exactly two and two.

For every even h in our family, the same fixed witness M'_h can also certify
ANY other perfect matching on the specified P_h: apply this lemma to that
matching and M'_h with the same charge assignment. The resulting groups may
be longer cycles rather than squares. This statement concerns those fixed
endpoint/selected sets, not arbitrary grid configurations.

## 8. Verification and provenance

`python3 develop/check_component_cut_exchange.py` checks 50 controls, every even
height 6 through 104: actual coverage/selected degrees, cut closure, distinct
resource counts, both signed ledgers, the partial assignments, the exact
post-exchange certificate, and the original-M paired -2/+2 certificate. It verifies P and matching size are retained and
explicitly records that the ownership flip changes the matching. An additional
77 controls enumerate all 11 perfect matchings on P_6 and all 66 on P_8 and
check their full disjoint-cycle partitions against one fixed witness per
height, including cases with two cycles. These later cycle controls were not
part of the initial reviewer code rerun. Finite controls test
the written all-height proof; they do not replace it.

The separate [turning formal audit](../output/turning-ownership-formal.json)
contains seven local Lean declarations for scalar resource/charge accounting
and arbitrary-length path forcing. Neither this coordinate family nor the
Hall adapter or square exchange assembly is claimed as an end-to-end Lean
proof.

The explicit cut family and the suggestion to inspect its crossing all-P square
came from Oracle proof assistance db526909 (conversation conv_fd50f2a62673ff1c).
The local proof above, ownership implementation, repair proof and grouped original-M/cycle lemmas were checked
separately. That assistance is not an independent review of this note. Its
additional general port-switch theorem is not imported here.

The 11 October manuscript, public main/PR #3 and star-forming/C4 remain outside
this research change. No email is sent or edited.

Independent review accepts the cut/changed-M repair (a50072dc) and, in a
separate fresh review, Sections 6-7 (83638f29). The intervening follow-up failed
at infrastructure typing without a mathematical verdict; it is preserved in
the [scope and review receipt](../output/turning-compensation-independent-review.json).
The first reviewer reports rerunning the original supplied Python checkers;
the later reviewer evaluated the written additions only. Neither compiled Lean.
