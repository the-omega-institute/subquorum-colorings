# Directional return certificates and a zero-block-loss obstruction

19 October 2026. This note completes the return step for a saturated
directional Heawood block. It also disproves charging every such signal
to positive loss in another block: an explicit all-k minimal selection
has k signals and no block loss anywhere. Core underoccupation matters.
The subsequent [block-capacity theorem](HEAWOOD_BLOCK_COMPENSATION.md)
uses a different resource ledger and proves SF_2(L_k)=36k for all k.

## Exact failure shapes in any simple graph

Let S form G, let p be selected, and let w be omitted before deleting p.
Write N_S(v)=N(v) intersect S. The deletion uncovers w if and only if
one of the following mutually exclusive shapes holds:

| Shape | Selected neighborhoods before deletion |
|---|---|
| Direct | N_S(w)={p} |
| Split | N_S(w)={p,z}, z!=p, N_S(z) contained in {p} |
| Relay | w is not adjacent to p; N_S(w)={y}, N_S(y)={p} |

For a split witness in a triangle-free graph, z is globally selected-
isolated: an edge zp would close a triangle through w. These statements
do not require p high, regularity, finiteness or bipartiteness; only
the isolate conclusion uses triangle-freeness.

**Proof.** If w is adjacent to p, three selected neighbors would leave
two after deletion. With one selected neighbor the direct shape holds.
With two, the remaining neighbor z must have no selected neighbor other
than possibly p, or it would cover w as a center after deletion. These
are exactly the first two cases.

If w is not adjacent to p, its selected-neighbor set is unchanged. It
has exactly one selected neighbor y, since formation holds before but
fails after deletion. Before deletion y must be active, and deletion of
p must remove its last selected neighbor. Thus N_S(y)={p}. Conversely
each listed shape leaves w with zero selected neighbors or just one
which is isolated after deletion, proving the equivalence. QED.

The full equivalence is checked for arbitrary vertex types in
[PortReturn.lean](../formal/StarForming/PortReturn.lean).

## A protected high port returns its witness to the core

Let p be a selected high in a block, with just one neighbor y outside
that block. Suppose every omitted internal neighbor remains covered
after deleting p, and every selected internal neighbor has another
selected neighbor besides p. Suppose y belongs to a core and all its
neighbors other than p belong to that core.

**Return theorem.** Some omitted core vertex w witnesses deletion of p.
It is either y itself or a relay through selected y with
N_S(y)={p}, N_S(w)={y}. Different high ports cannot use the same w.
Moreover a failed w is adjacent to no other selected high.

**Proof.** Highness covers the newly omitted p after deletion, so
minimality supplies a previously omitted failure w. An adjacent internal
failure is excluded by protection, leaving only y. In the nonadjacent
case the exact classification gives a selected leaf neighbor of p as
support. An internal neighbor has a replacement selected neighbor, so
this support must be y. Its omitted neighbor w lies in the core.

Disjoint high-witness sets give uniqueness. If w were adjacent to another
selected high h, deleting p would leave h active: it has at least two
selected neighbors and loses at most one. The retained star through h
would cover w. This proves the stronger adjacency exclusion. QED.

All three graph statements, together with the exact classification,
are proved in Lean. The [formal receipt](../output/port-return-formal-check.json)
also includes one conditional arithmetic corollary. Only standard logical
axioms are used; no finite graph table is a proof premise.

In the eight [saturated templates](SATURATED_HEAWOOD_TRANSFER.md), the
signal port p has both its internal neighbors selected. Each of those
neighbors has another selected neighbor. Protection therefore holds:
there are no omitted internal neighbors to check. Its imported owner
at the other port is selected, while its return at the opposite core
vertex y has exactly one of the three shapes in the table. In L_k,
y is an X-vertex and a relay terminal is one of its two core neighbors,
an adjacent U or surviving X neighbor.

If a relay terminal is an X-vertex, its attached block cannot itself be
a saturated directional import. The terminal is omitted, so cannot be
that block's selected incoming owner; its adjacent high signal port is
also forbidden by the adjacency exclusion. This is a constraint on
signal routing, not a conclusion that the terminal block must lose a vertex.

## Direct returns give real capacity slack

For a cubic minimal S let d_2 count selected degree-two vertices p with
an omitted neighbor w satisfying N_S(w)={p}. Then

    5|S|+i+d_2 <= 3n.

Choose this direct witness for each such p and extend to all selected
highs. Witness sets are disjoint, so the prescribed choices cannot
conflict. Its resource has capacity two and pays demand one, leaving
one real unused unit. The exact cubic identity3n-5|S|=i+W therefore
has W>=d_2. This is an application of the established capacity identity,
not a separate claim of priority for that identity.

In bipartite graphs isolate compensation2|S|<=2beta_2+i gives

    7|S|+d_2 <= 3n+2beta_2.

Let h count saturated directional blocks and a their direct returns.
Their signal ports are distinct qualifying degree-two roots, so a<=d_2.
Each such block has two global non-port isolates, giving i>=2h. For
L_k, writing |S|=36k+q, the necessary inequalities are

    7q+a <= 2floor(k/2),
    5q+2h+a <= 6k.

Isolates and unused capacity are separate terms in an exact identity;
this does not add the overlapping bare-port/import loss certificates.
The full block theorem subsequently gives the stronger q<=0.

## A signal does not force any positive block deficit

The following is an explicit minimal34-set in L_1. Label the core
H_i=i,U_i=6+i,X_i=12+i,Y_j=18+j. Blocks start at offsets20,34,48,
with the usual Heawood local labels. Select

    Core: {1,2,3,4,6,8,9,10,11,12},
    Block0: {0,3,4,5,7,9,10,11},
    Block1,Block2: {1,2,3,5,7,9,10,11}.

Every block contributes eight; all actual block deficits are zero.
Block0 has the omitted port28 private clause B_(28,25) owned by
selected core12. Its signal port20 is selected with two selected
internal neighbors. Its opposite core vertex13 is omitted and has
N_S(13)={20}, so13 is the direct return witness. No other block has
an outside owner, since its two adjacent core X are omitted.

Formation has a direct check. In every block, each omitted vertex has
two selected neighbors, except that block0's port28 uses internal25
and external12. For the ten omitted core vertices use the following
stars; entries list target,center,other leaf when the target is a leaf:

| Target | Covering star vertices |
|---:|---|
| 0 | 0,1,6 |
| 5 | 5,4,11 |
| 7 | 7,1,2 |
| 13 | 13,20,27 |
| 14 | 14,8,2 |
| 15 | 15,9,3 |
| 16 | 16,10,4 |
| 17 | 17,11,12 |
| 18 | 18,6,8 |
| 19 | 19,9,11 |

In rows0,5,17,18,19 the target is the center. In the remaining rows
the middle entry is the selected center. For inclusion-minimality,
the following complete table gives an uncovered vertex after deletion:

| Deleted | Failure | Deleted | Failure |
|---:|---:|---:|---:|
| 1 | 7 | 2 | 7 |
| 3 | 15 | 4 | 5 |
| 6 | 6 | 8 | 14 |
| 9 | 15 | 10 | 16 |
| 11 | 11 | 12 | 12 |
| 20 | 13 | 23 | 33 |
| 24 | 32 | 25 | 25 |
| 27 | 26 | 29 | 29 |
| 30 | 22 | 31 | 21 |
| 35 | 42 | 36 | 46 |
| 37 | 47 | 39 | 39 |
| 41 | 41 | 43 | 40 |
| 44 | 34 | 45 | 38 |
| 49 | 56 | 50 | 60 |
| 51 | 61 | 53 | 53 |
| 55 | 55 | 57 | 54 |
| 58 | 48 | 59 | 52 |

Every failure has at most one selected neighbor after deletion; if
one, it is isolated. Formation is upward closed, so the34 single-deletion
failures prove inclusion-minimality, not merely failure of a particular
local sufficient rule.

## All-k persistence of the obstruction

For every k, repeat the core pattern

    H1,H2,H3,H4; U0,U2,U3,U4,U5; X0,

in each six-index cell; select neither Y. Repeat the three displayed
Heawood patterns at its three cut pairs. Fold H,U,X indices modulo6,
Y indices modulo2, and block indices modulo3 to obtain pi:L_k->L_1.
The H and surviving X seams have their usual two distinct neighbors
modulo6; U/hub incidences preserve parity, and all port attachments
preserve their local labels. Thus pi is a neighborhood-bijective
k-sheeted cover, including the k=1 identity.

L_1 is bipartite and hence triangle-free. The general
[triangle-free covering theorem](COVERING_PULLBACK_AND_CUBIC_SEARCH.md)
therefore pulls back this specific minimal set to a minimal selection
T_k, with

    |T_k|=34k,   |T_k intersect core|=10k,
    all3k block sizes=8,   h=a=k,   sum_B delta_B=0.

The direct witnesses are the k distinct X_(6j+1), each having only
its selected block signal port as selected neighbor. This disproves
the candidate rule h<=sum_B delta_B, and any assignment requiring a
positive block deficit for every signal. It does not refute the target
|S|<=36k: this selection has a core deficit12k-10k=2k instead of a
core excess. The full capacity theorem explicitly accommodates it.

## Validation

[General controls](../output/port-return-controls.json) compare the exact
failure shapes against literal stars on1147graphs,21187forming selections
and172135deletion/target pairs. They also check23protected ports,
disjointness at high witnesses, and24actual minimal ambient examples:
all eight Fano templates with each of the three return shapes, totaling
232literal deletion checks. These examples show that split and relay
returns cannot simply be omitted from the analysis.

[Core controls](../output/port-return-core-controls.json) check all70
labeled cubic graphs of order six,770minimal selections and120strict
direct-capacity corrections. They verify the explicit34base deletions
and twelve neighborhood covers, private-clause minimality, zero block
loss, actual signals and refined capacity counts. The all-k proof is
the covering argument, not finite extrapolation.

Reproduction:

    python3 scripts/check_port_return.py --output output/port-return-controls.json
    python3 scripts/check_port_return_core.py --output output/port-return-core-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit port-return --lean /path/to/lean-4.33.0 --output output/port-return-formal-check.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
