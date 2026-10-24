# Shared-blank components are straight diagonal chains

19 October 2026. This refines BLANK_WITNESS_COMPENSATION.md using the
physical geometry of saturated attachment owners. The abstract multigraph
allocation theorem allows arbitrary cycles. The actual grid witness graph
has a substantially smaller class: straight diagonal chains, with at most
two distinct edges per consecutive owner pair. The only possible cycle
resources are parallel pairs.

## 1. The shared-corner displacement lemma

Keep the feasible pair, tile region, marked caps, reserved internal blanks,
free deficient blanks F and saturated attachment owners A of the preceding
note. Specifically, A contains only saturated tiles whose P is matched to
a deficient tile inside R, so |A|=k, not Q=k+eta. Reserve exactly one
internal blank for each deficient T and two additional disjoint blanks
for every marked cap. F contains every remaining deficient blank,
including those with no owner. If instead all Q owners were used, the
charge formula would require an additional -eta term. Tile coordinates
are integers; a tile (r,c) has corner coordinates
(2r,2c),(2r,2c+1),(2r+1,2c),(2r+1,2c+1), in TL,TR,BL,BR order.

Let a free blank z have two distinct owners S and S'. Both selected
vertices witnessing ownership are external neighbors of z, outside its
deficient tile. They must be its two external neighbors: one vertical,
one horizontal. Those neighbors lie in diagonally opposite owner tiles.

More explicitly, if S witnesses z through its selected corner x, then
the other owner tile and its selected corner are forced:

| Corner x of S | S'-S | Corner of S' |
| --- | --- | --- |
| TL | (-1,-1) | BR |
| TR | (-1,+1) | BL |
| BL | (+1,-1) | TR |
| BR | (+1,+1) | TL |

For example, if x is S.TL=(2r,2c), z is either (2r-1,2c) or
(2r,2c-1). In the first case z lies at the BL corner of tile (r-1,c),
whose other external neighbor is (2r-1,2c-1). In the second it lies at
the TR corner of tile (r,c-1), with exactly the same other external
neighbor. Thus S'=(r-1,c-1) and its witnessing corner is BR. The other
three rows follow by reflection. Missing outer-boundary neighbors simply
prevent the corresponding shared blank; they create no exception.

For each diagonally adjacent owner pair there are only two possible
physical shared blank vertices, the two common neighbors of their
nearest selected corners. Therefore an edge pair has multiplicity at most
two. Each such vertex belongs to F separately; one may be absent,
reserved, occupied or in a saturated tile, leaving fewer edges.

## 2. Classification theorem

**Theorem.** Each connected component of the shared-blank multigraph H
lies on one straight tile diagonal. All its owners have the same selected
diagonal orientation. After parallel edges are collapsed, it is a finite
path, possibly a single vertex. Along that path every link has multiplicity
one or two.

Proof. An owner is saturated with a matching endpoint, so its selected
corners are either TL/BR or TR/BL. In the first case the displacement
table permits only steps (-1,-1) and (+1,+1); every neighbor has the
same orientation and the invariant c-r is constant. In the second,
only (-1,+1) and (+1,-1) occur, the neighbor orientation is again the
same and c+r is constant.

Induction along any walk proves the assertion for a whole connected
component. For either orientation, there is at most one possible owner
at each row coordinate on its fixed line, and edges join consecutive
rows. A finite connected subset is therefore an interval of these rows;
a missing row or missing link separates components. Its underlying
simple graph is exactly a path. The preceding lemma bounds multiplicity
by two. QED.

In particular, the graph is bipartite by row parity and has no simple
cycle of length at least three. Turning a physical residual path does
not turn a shared-blank component: the two graphs describe different
incidences.

## 3. Exact payment with double links

Let d count unordered owner pairs joined by two distinct free blanks.
If H has v owners and c components, its underlying paths have v-c links,
so e=v-c+d and its cycle rank is exactly mu=d. Write p for private
degree-one free blanks and u for unused degree-zero free blanks as before.
The exact charge identity becomes

    2rho(R)=-2L+sigma+c-d-p-u.                    (1)

A component admits a distinct adjacent blank for every owner exactly
when it has a double link or a private blank. A chain with all links
single and no private blank leaves exactly one owner unmatched.

For a double link, assign its two distinct blanks to its two endpoints
and assign every other chain vertex its edge toward those endpoints.
For a private blank, root the chain at its owner, assign that private
blank to the root and each other vertex its edge toward the root.
These constructions use each actual blank at most once. Conversely,
a chain with v vertices, all links single and no private blank has only
v-1 incident blanks. Omitting one root attains precisely v-1 assignments.

For disjoint source regions of total charge at most L,

    2rho(R union sources)<=sigma+c-d-p-u.         (2)

Thus d+p+u>=c+sigma is a sufficient aggregate compensation condition.
An unpaid single-link chain costs exactly one doubled-charge unit.
Every double link, private blank and unused free blank contributes one
unit to the signed regional ledger; no abstract longer cycle is available.
Several such resources in one component can pay deficits of other
components additively, even though an adjacent assignment cannot cross
between components.

Equation (1) is independent of reservation choices because c-d-p-u=k-|F|.
A different valid reservation can change the incidence and component
description, but cannot manufacture additional aggregate charge slack.
An augmentation that merely changes reservations is therefore not, by
itself, a new numerical compensation theorem.

## 4. Double-link payment consumes a tile cycle

Let G_R be the simple graph of physical tile adjacency induced by R,
with cycle rank nu_R=|E(G_R)|-|R|+components(G_R). Then

    d<=nu_R.                                           (3)

Proof. The two distinct free blanks between a consecutive owner pair
lie in the two different intermediate deficient tiles of their unit
tile square. All four tiles belong to R. Thus each double link gives
a distinct unit-square cycle in G_R. Distinct owner pairs cannot give
the same square: its saturated owner diagonal and deficient intermediate
diagonal are fixed.

These unit-square cycles are linearly independent over the field of
two elements. In any nonempty selection of them, choose a topmost square.
Its upper edge belongs to that square and to no other chosen square,
so their edge symmetric difference is nonempty. To bound their number
by nu_R, choose a spanning forest of G_R. A cycle is determined by its
edges outside that forest: a nonzero difference supported only on a
forest cannot have even degree everywhere. There are exactly nu_R
nonforest edges, proving the dimension bound and (3). QED.

**Forest obstruction.** If G_R is a forest, H has no double links at all:
every shared-blank component is a single-link diagonal chain. Consequently

    2rho(R)=-2L+sigma+c-p-u.                            (4)

Paying worst-case disjoint source charge L by this regional certificate
is possible exactly when p+u>=c+sigma. Mere length, branching or bending
of a tree-shaped tile receiver cannot create a cycle payment resource.
Private or unused free blanks must pay the remaining chain components.
If the actual source charge is s<=L, the exact union charge is instead
(sigma+c-d-p-u)/2-(L-s); unused source allowance may also compensate.
A failed worst-case certificate alone does not imply positive union charge.

The cycle ranks of G_R, the shared-blank graph H and the residual matching
graph are different quantities. Here a tile cycle can support a beneficial
double link. In EXTERIOR_COMPONENT_BUDGETS.md a residual cycle consumes
capacity. The two effects must not be substituted for each other.

## 5. Arbitrarily many independent double-link resources

Use the a-owner staircase of BLANK_WITNESS_COMPENSATION.md, a>=2:

    S_i=(1+i,a-i), 0<=i<a,
    W_i=(2+i,a-i), 0<=i<a-1.

The S tiles have labels BT/TP; W tiles have BP/PP. All original matching
edges are as in that note. For any subset I of {0,...,a-2}, add tiles

    V_i=(1+i,a-i-1), i in I,

with labels PP/PB. Match V_i.TL to V_i.BL and V_i.TR to its immediate
upper external neighbor. In vertex coordinates the new endpoints are

    (2i+2,2a-2i-2)--(2i+3,2a-2i-2),
    (2i+2,2a-2i-1)--(2i+1,2a-2i-1).

All these coordinates lie in the original (2a+4)-by-(2a+6) rectangle.
The first edge family uses even columns and its two stated rows; the
second uses odd columns and different columns for different i.
At each of its rows, the new endpoints lie strictly to the left of
the original occupied vertices in that row. Consequently the new matching edges have disjoint
endpoints and avoid the original endpoints and selected vertices.

The only new occupied vertices adjacent to an S tile lie across its
nonselected corners. The added V_i.BR=(2i+3,2a-2i-1) remains blank and
is adjacent to S_i.BL and S_(i+1).TR. Thus all original T vertices keep
exactly their existing internal P neighbor. Every V_i has t=0,b=1,
h=1,s=0,crossing=1, hence r=1,d=1 and rho=-1/2.

The BR blank is a second shared blank for the pair S_i,S_(i+1);
the original W_i.TL is the first. There are no new owners. Other
original free blanks keep their owners, giving

    c=1, d=|I|, p=u=0, k=a,
    D=a-1+|I|, sigma=eta=0,
    rho(R_I)=(1-|I|)/2.                         (5)

Hence one chain can contain arbitrarily many double-link resources.
One such link pays its own initial shortage; every further double link
supplies another half-unit of negative regional charge. These are
distinct physical blanks, not repeated uses of one cycle certificate.
The full-grid objective is 4a-1+2|I|, still below mn/2.

The original tile-adjacency graph is a path. Every added V_i has exactly
the two neighbors S_i,S_(i+1) in R_I; no two V_i are tile-adjacent.
It adds one vertex and two edges without changing connectivity.
Therefore nu_(R_I)=|I|=d: bound (3) is sharp for arbitrarily large d.

## 6. Scope

The displacement, classification and all-subset staircase extension are
general written proofs. Finite physical controls and local Lean facts
support them separately; they do not replace the arguments above.

Controls pass all 254 double-link subsets through a=8, and six selected
subsets for each a=9..32: 398 physical regions and 3184 symmetry images.
They also recheck 115 inherited regions, including a marked tile with
t=1. Eight local ordered corner incidences check the displacement table.
The checker independently recovers components, orientations, diagonal
line invariants, path intervals, double-link multiplicities and maximum
assignments from the physical matching.

The combined Lean audit passes 19 declarations, including four new
statements. It checks the unbounded integer-coordinate
shared-corner displacement, orientation propagation, the two possible
shared-blank coordinates and the conditional double-link ledger. Graph
cardinalities, the finite-path classification and full constructive
allocation remain written proofs. Standard logical axioms may include
propext, Classical.choice and Quot.sound; no sorry or native reduction
axiom is used.

Reproduce:

    python3 develop/check_diagonal_witness_chains.py --output output/diagonal-witness-controls.json
    python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/diagonal-witness-formal-check.json

The theorem sharply identifies the remaining unpaid shared-blank
components but does not prove that every mixed-direction grid core
contains enough double links, private blanks or exterior compensation.
The universal grid conjecture and overlapping-core coverage remain open.

The first blank-witness review returned REVISE; the precise reservation
and source-domain clarifications are incorporated, and the private-repair
coordinate objection is answered with explicit vertices. The same-reviewer
follow-up 1ae400a9-caf3-4b0b-b7c1-151d15716024 reviews those clarifications
and the diagonal-chain/multi-double-link theorem. It completed ACCEPT
at03:59:29UTC, observedgpt_6/pro; exact response and assessment are
linked from output/diagonal-witness-oracle-review.json. Section 4's tile-cycle
rank corollary was added after that submission and is outside its input.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
