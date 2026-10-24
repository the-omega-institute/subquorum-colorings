Please re-audit the clarified distinct-blank theorem and its new geometric classification below, returning ACCEPT or REVISE. Your preceding REVISE is archived, not overwritten. We made the requested baseline-reservation and explicit-source-domain clarifications. We also need you to reconsider the private-repair objection under the stated row/column coordinates; the physical construction was already feasible.

Clarified preceding theorem:
- Exactly one baseline reservation per deficient t=1 tile. In unmarked tiles choose any internal blank neighbor; in marked tiles the single baseline is the pressure-forced other noncap corner, not an additional reservation. The two cap blanks are separate from it. The baseline/cap sets are disjoint across actual tile vertices. Thus free deficient blanks F have |F|=D-2L.
- Each blank has at most two saturated attachment owners. The sufficient Hall theorem explicitly ASSUMES at least two F-neighbors for every owner. Geometry alone does not imply this left-degree hypothesis. The incidence upper bound plus that explicit hypothesis prove Hall.
- The multigraph is loop-free because the two owners occupy distinct tiles. Each distinct physical blank is its own edge or private/unused resource.
- Sources U_1,...,U_m and R are pairwise TILE-DISJOINT and charges always measured in the original full configuration, including every crossing. Assume sum rho(U_i)<=L. Only R has the witness graph and resource F. Its exact identity is 2rho(R)=-2L+sigma+c-mu-p-u. Additivity directly yields 2rho(R union all U_i)<=sigma+c-mu-p-u. We do not allocate R's blanks again to sources or compute local witness graphs for sources. Recomputing k/F/H on the union is unnecessary because this is addition of original tile charges. Distinct such whole cores must be disjoint. sigma=0 is a condition, never inferred from disjointness. Please distinguish this elementary source aggregation from independently applying the witness assignment twice to the same blank.
- Coordinates are (row,column), first increasing downward, second rightward. For the disputed private repair V=(0,a) is ABOVE S_0=(1,a). Its new matching edges are (0,2a)--(1,2a) and (0,2a+1)--(0,2a+2). Its blank BR=(1,2a+1) neighbors S_0.TR=(2,2a+1). The new endpoint (0,2a+2) is neither S_0.TL=(2,2a) nor any vertex in S_0. For a=2, the complete configuration is:
ambient 8x10;
T={(2,5),(3,4),(4,3),(5,2)};
M={((3,5),(4,5)),((5,3),(5,4)),((5,5),(5,6)),((0,4),(1,4)),((0,5),(0,6))};
R tiles={(1,2),(2,1),(2,2),(0,2)}.
All listed selected vertices have exactly their original internal P neighbor. V.BR=(1,5) is a private blank of S_0. Physical checks passed all a=2..24 plus all eight symmetries; the general coordinate argument, not enumeration, proves every a.

The following new theorem uses the corrected preceding definitions. Please check its geometry independently: every actual shared-blank component is a straight diagonal chain, has only multiplicities one/two, and admits no ordinary simple cycle. The new all-subset construction realizes arbitrarily many independent double links and the exact signed charge. Four new Lean declarations support coordinate displacement/orientation/common-neighbor facts and conditional arithmetic; no full graph formalization or priority claim.

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
note. Tile coordinates are integers; a tile (r,c) has corner coordinates
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

## 4. Arbitrarily many independent double-link resources

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
    rho(R_I)=(1-|I|)/2.                         (3)

Hence one chain can contain arbitrarily many double-link resources.
One such link pays its own initial shortage; every further double link
supplies another half-unit of negative regional charge. These are
distinct physical blanks, not repeated uses of one cycle certificate.
The full-grid objective is 4a-1+2|I|, still below mn/2.

## 5. Scope

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

The combined Lean audit checks the unbounded integer-coordinate
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

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
