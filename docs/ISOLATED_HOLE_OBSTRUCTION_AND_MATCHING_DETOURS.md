# Isolated holes obstruct adjacent payment; disjoint actual-edge detours repair it

For every q>=1 there is a fixed endpoint footprint on a 6-by-8q rectangle
whose induced endpoint graph has a UNIQUE perfect matching, exact unrestricted-selection maximum
J=area/2, and a sharp selection whose maximum adjacent T-to-H matching misses
exactly q selections. Thus the preceding adjacent-hole injection cannot be
universal. Even a nonnegative fractional exact cover by forced-hole singletons,
guarded adjacent pairs and endpoint-free unit squares is impossible here.

A single additional type of piece repairs the accounting: a forced hole paired
with a site three steps away, through ONE specified actual matching edge.
An explicit disjoint cover proves the half-area bound for EVERY feasible T on
this footprint, with both selection colours allowed. At equality the cover
provides vertex-disjoint payments of length one or three. At equality exactly q distinct
actual matching edges are necessary and sufficient in this specified payment model.
Padding by even nonnegative integers on each side preserves the construction and puts the isolated holes
arbitrarily far from the outer boundary.

The numerical six-row half-area bound was established earlier by a boundary
certificate. The new results here are the structural fixed-footprint proof,
the obstruction to the proposed cover/adjacent-payment rules, and the exact
physical-edge cost of their repair. No freezing hypothesis is imposed or proved.

## 1. Setup and a general mixed-cover lemma

Let V be an even-by-even rectangular grid, M a matching of actual grid edges,
P its endpoint set, Q=V\P, T a subset of Q, and H=Q\T. Put O=P union T and
J=|M|+|T|. Assume each t in T has at most one neighbour in O. There is no
degree restriction on a vertex of P beyond its actual matching membership.

A site with two distinct P neighbours is a forced hole. An adjacent pair in Q
is guarded if at least one of its endpoints has a P neighbour. A guarded pair
contains at most one selection: selecting both would give that guarded endpoint
two occupied neighbours. An endpoint-free unit square has at most two selections:
any three vertices of its four-cycle include a selected vertex with two selected
neighbours. These facts also apply when there are occupied sites outside a piece.

A **matching-detour pair** is a pair {h,t} in Q with h forced to be a hole,
t adjacent to x, {x,y} an actual edge of M, and y adjacent to h. Require the
four vertices t,x,y,h to be distinct. If t is selected, the path t-x-y-h
pays it to h. If not, both sites of the pair are holes. This is a payment
certificate, not a claim that occupation can be moved along the path.

**Mixed-cover lemma.** Suppose Q is partitioned into f forced-hole singletons,
g guarded adjacent pairs, b matching-detour pairs, and s endpoint-free unit
squares. Require the b detour pairs to use distinct actual edges of M. Then

    |T| <= g+b+2s,
    |H|-|T| = f+2D,
    2J = |V|-f-2D,       D=g+b+2s-|T| >= 0.                (1)

Every feasible T has a T-to-H injection by mutually vertex-disjoint paths,
each of length one or three. At most b actual M edges are used internally.

Proof. Each singleton contains zero selections; each pair contains at most one;
each square contains at most two. Add these inequalities, using the disjoint
partition, and use |Q|=f+2g+2b+4s and |V|=2|M|+|T|+|H| to obtain (1).
For a guarded pair send its selection to its other, necessarily hole, endpoint.
Use the specified detour in a detour pair. Inside a square, zero selections
need nothing; one has an adjacent hole; two adjacent selections have two
different adjacent holes on the opposite side; two opposite selections can be
paired to the other two corners. Thus the square injections use only that
square. Piece endpoint sets are disjoint, all detour interiors lie in P,
and distinct edges of a matching have disjoint endpoints. Consequently all
payment paths are vertex-disjoint, and every image hole and actual edge is
used at most once. Logical P guards may justify several exclusions; this
does not create or spend additional physical payment resources. QED.

It is important to distinguish this exact lemma from an existence conjecture:
no universal existence of this mixed cover is claimed.

## 2. A four-by-four discovery seed

The small endpoint footprint

    P={(0,1),(0,2),(1,0),(2,0)}

has two isolated induced matching edges. Its only forced-hole sites are
(0,0) and (1,1), both of even checkerboard colour. The first is isolated in Q.
Q has six sites of each colour. Every adjacent pair or endpoint-free square
is colour-balanced. Any proposed partition into those pieces and forced-hole
singletons must use the singleton (0,0), contributing positive even-colour
imbalance, with no possible odd-colour singleton to cancel it. It cannot exist.

Selecting every odd-colour site outside P gives

    H P P T
    P H T H
    P T H T
    T H T H

with |T|=|H|=6, |M|=2 and J=8. No T has two occupied neighbours.
An adjacent T-to-H injection is impossible since the six holes include the
isolated (0,0). This is a failure of the payment rule, not of the half-area bound.
The interior construction below amplifies this mechanism without relying on
an isolated site at the corner of the rectangle.

## 3. The interior footprint and its disjoint cover

In a 6-by-8 cell use the four actual edges

    (0,2)--(1,2),   (2,0)--(2,1),
    (2,3)--(2,4),   (3,2)--(4,2).                         (2)

Call their endpoint set P*. The induced graph on P* is exactly four disjoint
edges: the even-colour endpoints are (0,2),(2,0),(2,4),(4,2); their only P*
neighbours are respectively (1,2),(2,1),(2,3),(3,2). Thus (2) is the unique
perfect matching. This observation is independent of any search.

The forced holes are exactly

    F*={(1,1),(1,3),(2,2),(3,1),(3,3)},                  (3)

all even-coloured. To check completeness, a site with two P* neighbours is
a common neighbour of two same-colour endpoints. Distinct even endpoints
in (2) have Manhattan distance four, so have no common neighbour. The six
pairs of odd endpoints give precisely the centre and four diagonals in (3).
The centre h*=(2,2) has all four neighbours in P*, so is isolated in Q.

Here is a partition of Q into seven guarded pairs, six endpoint-free squares
and ONE matching-detour pair. For squares, list the top-left corner.

| Piece | Sites / square corners | Actual guard or internal edge |
|---|---|---|
| Guarded pair | (0,0)--(1,0) | (2,0) guards (1,0) |
| Guarded pair | (0,1)--(1,1) | (0,2) guards (0,1) |
| Guarded pair | (0,3)--(1,3) | (0,2) guards (0,3) |
| Guarded pair | (3,0)--(3,1) | (2,0) guards (3,0) |
| Guarded pair | (3,3)--(4,3) | (2,3) guards (3,3) |
| Guarded pair | (3,4)--(3,5) | (2,4) guards (3,4) |
| Guarded pair | (5,2)--(5,3) | (4,2) guards (5,2) |
| Six squares | (0,4), (0,6), (2,6), (4,0), (4,4), (4,6) | All four sites of each square are outside P* |
| Detour pair | {(2,2),(2,5)} | (2,5)--(2,4)--(2,3)--(2,2), using the third edge in (2) |

The pair endpoints occupy 14+2=16 sites and the squares 24 sites; a direct
row-by-row check shows all forty Q sites occur exactly once. In particular
the forced centre appears in the detour pair, not as an additional singleton.
Its empty-site credit must not be added a second time as an unused forced hole.

For q>=1 translate the cell by (0,8j), j=0,...,q-1, in a 6-by-8q board.
Use the translated P*, M and cover pieces. The cells partition the board.
Endpoints in different cells have column separation at least four; in
particular there are no new P-P adjacencies or common neighbours of endpoints
from different cells. Equations (2),(3), unique matching, and the q isolated
centres therefore remain valid globally. Cover pieces from different cells
are disjoint. The q detours use q different actual edges.

The mixed-cover lemma now has

    f=0, g=7q, b=q, s=6q, |M|=4q,
    |T| <= 20q,      J <= 24q=area/2,                    (4)
    |H|-|T|=2(20q-|T|).

This is an all-q proof for arbitrary feasible selections T of either colour;
it is not an extrapolation of finite-width optimization. Every feasible T
has the stated disjoint payment paths, even though it need not have an
adjacent-hole injection.

For the original weighted target this also gives the sharp fixed-footprint
statement |T|+(5/6)|M|<=area/2-2q/3, since |M|=4q. This is a consequence on
this specified class, not an improvement of the coefficient for arbitrary grids.

## 4. Sharp selection, exact adjacent deficiency and minimum detour cost

Take T to be every odd-colour site outside P. Each cell has 24 odd sites,
four of which are in P, so |T|=20q. T is independent. Distinct even P endpoints
within or between cells have distance at least four, so no selected vertex
has two P neighbours. Thus T is feasible. All remaining even-colour sites
outside P are holes, giving

    |T|=|H|=20q,   |M|=4q,   J=24q.                    (5)

Each guarded pair has exactly one selection, each square exactly two, and
each detour pair exactly one selection, namely (2,8j+5). All pieces attain
their capacities, so all holes are used once by the mixed-cover injection.

Let nu_adj be the maximum matching size in the actual adjacency graph
between T and H. The q isolated centres have no T neighbour, hence
nu_adj<=20q-q=19q. Discard the q detour payments from the explicit injection.
All other payments are adjacent and retain 19q different selections and holes.
Therefore

    nu_adj=19q,        |T|-nu_adj=q.                     (6)

This lower certificate and the isolated-hole upper certificate establish
exactness without solving a maximum-matching instance.

More generally consider injections T->H realized by vertex-disjoint paths
that are either single grid edges or alternate non-M / M / non-M / ...,
with all internal vertices in P. Because (5) makes any injection a bijection,
all q isolated centres must be used. A path ending at such a centre cannot
have length one. It must use at least one actual M edge internally. Disjoint
paths cannot use the same physical edge. Thus EVERY such payment system
uses at least q distinct actual M edges. The displayed paths attain q, one
length-three detour per cell. The exact minimum is q.

This is a resource lower bound for this specified path model. It does not
say that every arbitrary numerical certificate must use matching edges, or
that a selection has been relocated, or that M has been changed.

## 5. Why even fractional local covers fail

On this footprint Q has equally many even and odd sites. Every adjacent pair
and every unit square is colour-balanced. All eligible forced-hole singletons
are even, by (3). An isolated centre belongs to no eligible adjacent pair or
endpoint-free square, so its coverage must come from its singleton.

For an ordinary partition, subtract the number of odd Q sites from the
number of even Q sites. This forces the number of singleton pieces to be zero,
contradicting the q necessary centre singletons.

The same argument excludes a nonnegative FRACTIONAL EXACT cover: assign
nonnegative weights to all eligible pieces and require the weights covering
each Q site to sum to one. Multiply these coverage equations by +1 on even
sites and -1 on odd sites, then add. Balanced pieces contribute zero; each
forced-hole singleton contributes its nonnegative weight. The sum must be
zero, but each isolated centre has singleton weight one, so the sum is at
least q>0. Contradiction. This covers all grid alignments of unit squares,
not merely a fixed tiling. It does not rule out larger or different pieces.

The detour pair is itself colour-balanced. It reaches the isolated centre
through P without removing that centre from the conservation law, which is
precisely how it avoids this obstruction.

## 6. Padding, scope and the next geometric question

Add any even number of rows above/below and any even number of columns
left/right, translating the core by the top/left offsets. Tile the added
area by disjoint endpoint-free 2-by-2 squares: first the full-width top/bottom
strips, then the left/right strips beside the core. Extend T by all odd sites
outside P. No two even P endpoints acquire a common neighbour, so feasibility
and (3) are unchanged. The cover extends by these squares. Formula (4)
becomes J<=area/2 and is attained; (6) still has exact deficiency q and the
minimum number of actual relay edges is still q. The isolated centres can
therefore be arbitrarily far from the external boundary.

The preceding all-rematching obstruction and this obstruction concern
different certificates. The earlier family has an adjacent-hole injection
but no unchanged endpoint-charge certificate. Here adjacent payment and the
suggested purely local mixed cover fail, while distinct actual-edge detours
restore a complete injection. A general proof must allow both kinds of credit
and prove their joint availability. A guard is a logical witness, a hole is
a physical image, and a detour edge is a separately tracked physical route
resource; none is an extra numerical rebate on top of the same payment.

The remaining question is whether an appropriate disjoint cover or payment
normal form exists on arbitrary footprints, or whether forced-hole detours
themselves have a joint Hall obstruction. Existence is not assumed. General
5/6 improvement, universal half-area bounds and freezing remain outside this
note. The submitted manuscript, public main/PR3, Mail, C4 and shared CI are
unchanged.

The follow-up [unbounded relay-cost theorem](UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md)
already rules out a fixed maximum detour length: one adjacent deficit can
require k different actual matching edges for arbitrarily large k, even
under rematching. A general normal form must permit unbounded paths or
different pieces, and must prove their disjoint availability.

## 7. Verification scope

The solver-free checker validates the actual coordinates, every guard,
disjointness, all forced holes, induced matching uniqueness, sharp feasibility,
square injections, disjoint paths, both sides of (6), padding and minimum-cost
witnesses. A separate column dynamic program checks the exact maximum with
arbitrary selections at small q; it does not use the cover inequalities.
The initial exact-cover search found the seed and the displayed cover; the
proofs above no longer depend on its completeness or its implementation.
Local Lean checks the indicated geometric centre exclusion, square capacity,
unrestricted-list summation and obstruction/objective arithmetic. The periodic
coordinate cover, fractional argument, path assembly and resource-minimality
adapter remain written mathematics, with finite computational controls.

Recorded controls: q=1,...,50, 200 feasible selections using either colour,
four padded boards, all eleven feasible square states, and all 4,096 selection
subsets of the corner seed (195 feasible). The separate column DP agrees with
that seed exhaustion and gives maxima |T|=20q for q=1,...,4; it counts 19,38,76,152
maximizers respectively. Seven scoped Lean declarations compile locally with
individual axiom audits. None of these finite controls replaces the all-q proof.

Independent review d8f1fe44 returned ACCEPT for the full all-q written proof.
The reviewer reports executing the supplied standalone Python verifier and
matching the JSON exactly; no Lean was run. Three opening scope clarifications
were applied. This review excludes the later unbounded-cost theorem, whose
review is recorded separately. See the [receipt](../output/isolated-hole-detours-review.json).
