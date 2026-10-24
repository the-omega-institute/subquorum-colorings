# Cooperative promotion and the cost of mixed matching corners

19 October 2026. Research note; the submitted manuscript is unchanged.
This continues the exact ledgers in ATTACHMENT_CORRECTED_COLLAR_COMPENSATION.md
and the geometry in DIAGONAL_WITNESS_CHAINS.md. The results below are written
general proofs, with independent finite controls. They do not establish the
unrestricted grid inequality or a new universal coefficient in the 5/6 bound.

## 1. Objective-preserving promotions on any finite graph

A finite simple undirected graph has a feasible pair consisting of a vertex
set T and a matching M disjoint from T,
such that every vertex of T has at most one neighbor in the occupied set
A=T union V(M). Its objective is |T|+|M|. Write deg_A for occupied degree.

**Bundle lemma.** Choose distinct edges x_i y_i of M and orient each by
choosing its endpoint x_i. Set X={x_i}, Y={y_i}, and remove these edges
from M while adding X to T. The new occupied set is exactly A minus Y.
The resulting pair is feasible if and only if

    deg_(A minus Y)(x_i)<=1 for every i.                 (1)

The objective is unchanged, T grows by the number of chosen edges and M
shrinks by the same number.

Proof. Matching disjointness makes X,Y,T pairwise disjoint and ensures
the surviving edges avoid T union X. Existing selected vertices only lose
occupied neighbors. Thus the only new feasibility conditions are precisely
(1). Each removed matching edge contributes exactly one new selected vertex.
This proves both directions and the objective assertion. QED.

In particular, an endpoint of occupied degree at most two can always be
promoted alone: its mate is removed, leaving degree at most one. This has
no neutrality, attachment, tile or boundary hypothesis. Repeating single
promotions stops with every remaining matching endpoint of degree at least
three. Unlike the restricted neutral move, this general move need not
preserve any tile charge, marked cap, residual component or certificate.
Those objects must be reconstructed after normalization.

**Cycle lemma.** In a bipartite graph, fix one side. Orient each matching
edge from its endpoint x on that side to its mate y. Retain as candidates
the edges with deg_A(x)=3. Put a directed arc i to j, for distinct candidate
edges, when x_i is adjacent to y_j. Every directed cycle of distinct
candidate edges can be promoted simultaneously.

Proof. For each edge of the directed cycle, the removed set Y contains
both its own mate and the next edge's mate. These are distinct occupied
neighbors of x_i. Its initial occupied degree is three, so its remaining
degree is at most one. Apply the bundle lemma. QED.

In physical grid edges this is an M-alternating even cycle. A two-vertex
directed cycle is a square with two opposite matching edges. This cycle
is different from either a tile-adjacency cycle or a shared-blank double
link; none of their resource counts may be substituted for another.

**Normalization theorem.** Every finite feasible pair in a bipartite graph
has an objective-preserving representative, retaining all original T,
such that all matching endpoints have occupied degree at least three
and both degree-three dependency digraphs are acyclic.

Proof. Repeat an eligible single promotion, or, if none exists, a directed
cycle promotion on either side. Each move strictly decreases the number
of matching edges and preserves feasibility and objective. There are at
most the original |M| moves. On termination neither type is available,
which is exactly the asserted condition. QED.

Consequently an objective maximizer chosen to maximize |T| already has
this stronger condition. A terminal point for single moves alone need
not have it. No confluence or order independence is asserted. Recomputing
degrees and running a linear directed-cycle search after each move gives
O((|M|+1) (|V|+|E|)) time and O(|V|+|E|) storage. On a bounded-degree grid this
is quadratic time. The supplied checker independently validates every
resulting feasible pair, rather than relying on a cycle-search assertion.

## 2. A two-sided chain bound with an explicit transition penalty

Use TL,TR,BL,BR corner order. Suppose the saturated tiles

    S_i=(r0+i,c0-i), 0<=i<v, v>=2,

all have selected corners TR,BL and exactly one matching endpoint at TL
or BR. Call this choice their P-state. Include both intervening tiles
(r0+i,c0-i-1) and (r0+i+1,c0-i) for every consecutive pair, and assume
all those tiles are deficient. Let R consist of exactly these 3v-2 tiles.
Assume every matching endpoint in the full configuration has occupied
degree at least three. Let a count P-state changes along the chain.

**Local gap lemma.** If consecutive owners have the same P-state, each
of their two intervening tiles has b-t>=1.

Proof. Place the two owners east and south of the northwest intervening
tile Q. Their selected corners force Q.BR blank. First let both owners
have P at BR, hence their TL corners blank. The external right neighbor
of Q.TR and external lower neighbor of Q.BL are therefore blank.

Every deficient tile has b>=t. If Q had b=t, its forced blank would
imply t=b=1, with its other two vertices P. T at TL would then have
two occupied internal neighbors, impossible. T at TR would leave BL
as P with just one occupied internal neighbor, an external blank below,
and at most one occupied external neighbor to the left. That P would
have degree at most two, also impossible. T at BL is symmetric. Thus
b-t>=1. This argument only uses actual occupied degrees, even if a mate
crosses the region boundary.

The southeast intervening tile has TL forced blank, with its TR and BL
external neighbors both P. Again b=t would mean t=b=1. T at BR has two
internal occupied neighbors. T at TR or BL has an occupied internal
neighbor and its external P neighbor. All cases are impossible. Rotate
the complete picture by 180 degrees for the common TL P-state. QED.

The intervening tile sets of distinct consecutive pairs are disjoint:
the first kind has coordinate sum r0+c0-1 and the second r0+c0+1,
and their row coordinates identify the link uniquely. Thus the v-1-a
equal-state links contribute without overlap:

    D>=2(v-1-a).                                        (2)

Let sigma count matching edges with a deficient endpoint in R and a
saturated endpoint outside R, and eta the reverse crossings. There are
v saturated matching endpoints in R, so k=v-eta. The exact original
configuration ledger 2rho(R)=-D+k+sigma gives

    2rho(R)<=2-v+2a+sigma-eta.                          (3)

For a homogeneous chain this is rho(R)<=1-v/2+(sigma-eta)/2.
For instance, v>=4 and sigma<=eta supply at least one unit of negative
charge, enough for tile-disjoint sources with total original charge at
most one. Each receiver must be tile-disjoint from its assigned sources,
and the combined receiver-plus-source cores must be pairwise tile-disjoint.
If those cores cover every positive source and all remaining tiles have
nonpositive total charge, the usual additive ledger proves
coefficient one for that class. Tile disjointness, the source allowance
and the boundary imbalance are essential hypotheses, not conclusions
of the normalization theorem. No resource is reused: (2) sums actual
disjoint deficient tiles, and each source/core enters the regional sum once.

## 3. A complete single-promotion-terminal mixed diamond

Here is an 8 by 4 grid configuration, with zero-based vertex coordinates:

    T={(0,0),(0,2),(2,3),(3,0),(3,2),
       (4,1),(4,3),(5,0),(7,1),(7,3)}
    M={ (2,2)--(2,1), (2,0)--(1,0), (1,1)--(1,2),
        (5,1)--(5,2), (5,3)--(6,3), (6,1)--(6,2) }.

All remaining vertices are blank. The following vertex array also lists
all labels, with each two by two block a tile:

    T B | T B
    P P | P B
    ----+----
    P P | P T
    T B | T B
    ----+----
    B T | B T
    T P | P P
    ----+----
    B P | P P
    B T | B T

Each T has exactly one occupied neighbor. The two saturated-owner P
vertices (2,2),(5,1) have occupied degree four; the other ten P vertices
have degree three. This is a full feasible pair with no eligible single
promotion. Its objective is 10+6=16, exactly half of the 32 vertices.

Take R={(1,0),(1,1),(2,0),(2,1)} in tile coordinates. Its owners are
(1,1) with P at TL and (2,0) with P at BR. Both intervening tiles have
t=b=1. Thus

    D=0, k=Q=2, sigma=eta=0, j=2, rho(R)=1.

There is no free blank after the one-blank-per-T reservation. Its witness
graph consists of two isolated owners. The exterior has charge -1;
the full grid has charge zero. Therefore occupied degree at least three
alone does not imply nonpositive regional charge, even with no saturated
boundary transfer. This is a counterexample to that regional rule, not
to the global grid inequality. For (3), v=2,a=1 attains 2rho(R)=2, so
the coefficient two on a cannot be reduced while keeping the other terms
fixed under these hypotheses.

## 4. Arbitrarily large connected receivers, and their exact repair

Stack r copies of this 8 by 4 block, shifting each by (8i,0). At a block
boundary, occupied vertices in the two facing rows have opposite column
parities; hence no new occupied adjacency is created. The resulting
8r by 4 pair remains feasible and terminal for single promotions, with
|T|=10r, |M|=6r and objective 16r, exactly half the grid size.

Include the four central tiles of every block and, between consecutive
blocks, add tile (4i+3,1) and tile (4i+4,1). This tile-connected receiver
R_r has 6r-2 tiles. It is not claimed residual-connected. Each first
bridge tile has t=1,b=1 and charge zero; each second bridge tile has
t=1,b=2 and charge -1/2. Every matching endpoint in these tiles has its mate
in a deficient tile, so there are no saturated attachments. In particular,
the second bridge tile's P is matched outside the receiver. The first
bridge tile internalizes one former boundary crossing and introduces one
new crossing; the second introduces another. The net increase in j per
bridge pair is therefore one. Directly,

    D=r-1, k=Q=2r, sigma=eta=0,
    j=2r+(r-1)=3r-1, rho(R_r)=(r+1)/2.

The second bridge tile's crossing goes to the omitted tile in column zero.
The other new crossing goes from the first bridge tile's upper-left P to
its omitted neighbor in column zero; its upper-right P is matched to the
included central tile above it. Each second bridge
has one free blank, adjacent to exactly one neighboring owner. Hence H
has 2r isolated owners, p=r-1 private blanks, d=u=0. The exact witness
ledger is again 2rho=2r-(r-1)=r+1. The remainder has charge -(r+1)/2.
So single-promotion-terminal pairs have unbounded positive charge on
tile-connected receivers. This still does not obstruct a representative
maximizing |T|, since the following cooperative repair increases |T|.

In the top half of each block, simultaneously promote (2,1),(1,2) and
remove (2,2),(1,1), deleting their two matching edges. Each promoted
vertex initially has degree three and loses both these removed neighbors.
This is exactly a two-cycle in the dependency digraph. Now (1,0) can
be promoted singly, removing (2,0). In the bottom half, simultaneously
promote (5,2),(6,1) and remove (5,1),(6,2); then promote (6,3), removing
(5,3). These are the 180-degree reflected moves.

No move crosses a block interface, and the facing boundary rows stay
unchanged. Perform this displayed sequence independently in every block.
The final pair has no matching edges and 16r selected
vertices, retains the original 10r selected vertices, and preserves the
objective. This proves for every r that the displayed obstacle is
eliminated by the stronger normalization. It does not prove that every
mixed-state receiver in that normal form is compensated.

## 5. Reproduction and remaining question

Run:

    python3 develop/check_cooperative_promotion.py --output output/cooperative-promotion-check.json

The checker independently reconstructs every matching, occupied degree,
selected-neighbor constraint, regional charge and blank allocation. It
checks r=1 through 32 and all eight grid symmetries, all 12,752 feasible
pairs on the 2 by 2, 2 by 4 and 2 by 6 controls, and all 81 local ternary
tile states for each implication in the local gap lemma. Each algorithmic
move is rechecked by actual coordinates. These finite checks support the
proofs above; they are not substitutes for the all-size arguments.

The scoped Lean module SubQuorum/MixedPChainCompensation.lean proves both
finite gap implications by kernel reduction and the conditional transition
charge bound by integer arithmetic. The bridge from actual occupied degrees
to the local predicates, the disjoint-link geometry, the graph normalization
theorem and the all-r family remain written proofs. The combined audit now
contains 22 declarations; it does not claim full formalization of this note.
Independent review0204a4ca completed REVISE: the all-size formulas and
main arguments survive, while the bridge-mate description and crossing
explanation above are corrected. Internal-owner conventions, source
packing, simple-graph conventions and the empty-matching runtime are
made explicit. The exact response and independent assessment are archived.
No ACCEPT is claimed for this revision; external priority remains open.

The follow-up PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md now gives a
physical obstruction surviving even every oriented endpoint-promotion
bundle. It also gives an exact fixed-side threshold-core algorithm that
handles degree-four endpoints. The remaining task is an actual exterior
compensation or more general selected-vertex exchange argument; degree-four
and mixed selected-corner geometry remain outside the homogeneous run
bound. General grid equality and a universal improvement of 5/6 remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
