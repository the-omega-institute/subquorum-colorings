# Residual Hall demand and the price of physical compensation

11 November 2026. The earlier fixed-path completion test decides whether
all other TH paths can remain direct. Here a residual deficit also gives
a lower bound on the expense of additional paths. The argument allows
arbitrary additional TH and HH routes and needs no separated-core model.
The optimizers used below are standard matching and integral min-cost flow.

## 1. Retained paths and residual terminals

Let G be a finite bipartite graph with equally many white and black vertices,
M a matching, P its endpoints, and Q=V minus P. Let T be any subset of
white Q; W is the other white Q. Actual M edges have nonnegative weights.
A full auxiliary matching N perfectly matches V. In the tagged M union N,
terminal components alternate from white Q to black Q. TH components start
in T and pay their actual edges; HH components start in W and pay zero.
Closed components, including doubled common edges, are free.

Specify vertex-disjoint simple alternating terminal paths R, each starting
at a white Q vertex and ending at a black Q vertex, with all interiors in
P and edges auxiliary, actual, ..., auxiliary. R may contain both TH and HH
paths, including direct paths. Let b_R be their fixed TH expense. Remove
their vertices; every removed interior occurs with its actual mate. Thus
no actual edge crosses the deletion. Use primes for the remaining M', P',
Q', T', W'. Let B' be the remaining black Q terminals. A completion must
retain every path in R, not merely selected actual edges from those paths.

For any D subset B', put

    F=N_(T')(D),       d=max(0, |D|-|F|),       U=T' minus F.       (1)

Here N_(T') means direct adjacency in the residual graph. D may include
remaining centres, exterior terminals, or their union.

Use the residual alternating digraph: orient actual M' edges black-to-white,
and all other graph edges white-to-black. Sources are white Q' and sinks
black Q'. A path cannot pass through another source or continue beyond a
sink. Give each physical arc capacity one. The actual arc is the unique
outgoing arc of its black P' endpoint and unique incoming arc of its white
P' endpoint; its single capacity protects both vertices. Terminals also
have unit source/sink capacities. In particular every auxiliary arc has
capacity one, and no residual Q source or sink can be an internal vertex.

Define h_D as the maximum number of vertex-disjoint residual HH paths
from W' into D. Compute it by ordinary max flow with zero costs; actual
HH weights do not enter the TH objective. Set

    s=max(0,d-h_D).

Let C_s be the minimum total actual weight of s vertex-disjoint alternating
paths from U to D, with C_0=0 and infeasibility represented by infinity.
One min-cost flow of value s computes it; source-to-destination identities
are free, rather than prescribed labelled pairings.

A second relaxation retains source and destination identity but forgets
internal disjointness. For x in U union W' and b in D, add an assignment
edge whenever an alternating x-to-b path exists. Give it cost zero for
x in W', and cost equal to the shortest actual-weighted x-to-b path for
x in U. Let J_d be the minimum cost of a cardinality-d matching in this
endpoint graph, with J_0=0 and infinity for infeasibility.

## 2. Residual compensation theorem

Let f_R* be the minimum TH expense of a full matching retaining R. Then

    b_R + max{C_s,J_d} <= f_R*.                                 (2)

Equivalently, this lower bound holds for EVERY full matching N retaining
all of R, before taking the minimum defining f_R*.

In particular, an infinite relaxation certifies that no retaining completion
exists. No selection-feasibility, core-separation or positive-weight
assumption is needed for the lower bound.

**Proof.** In a retaining full matching, the residual terminal paths give
a bijection from T' union W' to B'. At most |F| paths ending in D can
start in F. At least d paths into D therefore start in U union W'.

Select any d such incoming paths. Their sources and destinations are all
distinct. Contracting them to endpoint pairs yields a cardinality-d matching
in the relaxation defining J_d. Shortest TH path costs do not exceed their
actual costs, and HH pairs remain free. Nonnegative expenses allow all other
paths to be discarded, proving f(N)-b_R >= J_d.

The HH paths ending in D form a vertex-disjoint residual family, so at most
h_D of the incoming paths can be HH. There must consequently be at least
s TH paths from U to D. Choose s of them. They form a feasible physical
flow of value s, with expense at least C_s. Their actual edges are disjoint
from R and from all other terminal components. Hence f(N)-b_R >= C_s.
Taking the maximum and then minimizing over retaining N proves (2). QED.

The bounds C_s and J_d concern the SAME additional expenses and must not be
added. In the 8-by-12 unit example below, both equal two, but the entire
additional expense is two. Adding them would falsely predict total expense
six although a full matching of expense four exists.

The network representation is exact for the physical s-path subproblem.
An integral flow decomposes into paths and circulations. Nonnegative
circulations can be discarded; actual-edge and terminal capacities make
the paths vertex-disjoint. Conversely every such path family induces the
flow. This subproblem does not assert that its optimizer extends to a full
matching or that separately optimized HH and TH flows coexist. The number
h_D is an upper bound on usable HH capacity in a full completion, which is
exactly the direction required in (2).

## 3. Constructing a matching that attains the lower bound

Take the s physical TH paths returned by C_s and add them to R. Remove
all these paths. On the remaining graph forbid auxiliary edges from any
remaining selected white terminal to a black vertex of P. A perfect
matching in this graph, together with the fixed path edges, is a full N
whose only non-direct TH paths are those already fixed. Its expense is
b_R+C_s. HH paths in the remainder can have arbitrary positive actual
weights and still cost zero.

Precisely, suppose there EXISTS an optimal physical s-path family for C_s
whose direct-TH remainder has a perfect matching. Then it certifies

    f_R*=b_R+C_s.                                               (3)

Success itself forces C_s>=J_d by (2); that comparison is not an extra
hypothesis. If the test fails for a chosen optimizer, its residual
Hall set only rejects that particular direct-TH remainder. It does not
prove general infeasibility or reject other minimum physical flows.
The proof is the earlier fixed-path extension lemma: every remaining TH
path is direct exactly when its first auxiliary neighbour is black Q.
This construction permits additional non-centre TH paths and makes no
one-relay-per-core assumption. It supplies a certificate criterion, not
a general exact optimizer for unrestricted TH expense.

### When the attainment criterion is also necessary

The expense-splitting argument used earlier for separated-core normal forms
extends to arbitrary retained paths and residual regions as follows.

Suppose C_s is finite and every residual non-direct TH path has strictly
positive expense. This holds whenever all residual actual edges have strictly
positive weights; it also permits zero-weight actual edges that cannot occur
on a zero-expense non-direct TH path. Then

    f_R*=b_R+C_s
    iff some optimal C_s family has a perfect direct-TH remainder.   (3a)

**Proof.** Sufficiency is (3). For necessity take a retaining full matching
of expense b_R+C_s. Such a matching exists when this finite equality holds,
because a finite graph has finitely many auxiliary matchings. As in Section 2,
choose s of its TH paths from U into D. Their expense is at least C_s.
The total residual TH expense is exactly C_s, so the chosen paths attain C_s
and all other residual TH paths have expense zero. By the hypothesis these
other TH paths are direct. Restricting the full matching to their remainder
therefore supplies the perfect matching required in (3a). QED.

There is a quantitative version. If the minimum expense eta of any residual
non-direct TH path is finite, and m(N) is the number of those paths in a
retaining full matching N, then m(N)>=s and

    f(N) >= b_R+C_s+(m(N)-s) eta.                             (3b)

Indeed, after selecting the s compulsory paths, the remaining m(N)-s
non-direct TH components have disjoint actual-edge sets and each costs at
least eta. If eta>0 and f(N)<=b_R+C_s+epsilon, with epsilon>=0, this gives

    m(N) <= s+floor(epsilon/eta).

If no residual non-direct TH path exists, every retaining full matching has
m(N)=s=0 and expense b_R; no infinite product in (3b) is intended.

The coefficient eta in (3b) is sharp even for connected bipartite graphs.
For r>=1 take white vertices t_i,w_i and black vertices b_i,z_i, i=1,...,r.
Use edges t_i--b_i, b_i--w_i, w_i--z_i, and w_i--b_(i+1) for i<r.
Let M consist of b_i--w_i, all of weight eta>0; set T={t_i}, W empty,
R empty and D={z_1}. This graph is a tree. Its leaf edges force the unique
full N to contain t_i--b_i and w_i--z_i for every i. Thus s=1, C_s=eta,
m(N)=r and f(N)=r eta, attaining (3b). Every selected source has one P
neighbour. This family establishes sharpness in the general graph domain.

Both the positivity hypothesis and the existential optimizer quantifier have
content. For positivity, take two disjoint four-vertex paths, embedded as
grid vertices (r,c) with r in {0,2} and c in {0,1,2,3}. In each row the middle
edge (r,1)--(r,2) is actual, the selected source is (r,3), and the black
terminal is (r,0). Give the row-0 actual edge weight one and the row-2 edge
weight zero. All other graph edges are the path edges. Let R be empty and
D={(0,0)}. Then W is empty, d=s=1, C_s=1, and the unique optimal physical
family is the row-0 path. The unique full auxiliary matching pairs columns
0--1 and 2--3 in both rows and has expense one. After removing the row-0
path, however, its row-2 selected source can be matched only through P.
The direct-TH remainder is impossible. Thus equality with b_R+C_s need not
imply the direct-remainder condition when additional zero-expense TH paths
are allowed. Each source has one P neighbour; this is a finite grid-board
example, with two components, rather than a full rectangle.

The hypothesis in (3a) is decidable by a one-path shortest-cost flow: delete
all direct arcs from T' to B' in the residual alternating network, and find
the minimum expense from T' to B'. Its finite value is eta. A zero value
means a zero-expense non-direct TH path exists; absence of any such path
also satisfies the hypothesis. This is a test of the stated hypothesis,
not a search over all optimal C_s families.

### Unit weights still require choosing a compatible optimizer

The existential quantifier in (3a) cannot be replaced by an arbitrary
minimum physical flow, even on a full rectangle with feasible selected
vertices and unit actual weights. Reuse the five-square geometry of the
[earlier branched-source construction](https://github.com/the-omega-institute/subquorum-colorings/blob/b7e74a95f8250ef94234ccb3a485f10dcfa51622/docs/EXPOSABLE_PORTS_AND_BRANCHED_SOURCE_OBSTRUCTION.md),
now with its canonical matching and all weights one. Here are the full
specification and an attaining certificate.

The board is [0,17]^2. Its five 5-by-5 square origins are

    (6,6), (2,0), (0,10), (10,12), (12,2).

Remove the black centre of each square to obtain P. In each local square
use vertical actual pairs (a,b)--(a+1,b) for a=0,3 and b=0,...,4, and
the two horizontal actual pairs (2,0)--(2,1), (2,3)--(2,4). Select all
white Q vertices except the four HH sources

    W={(5,10),(6,5),(10,11),(11,6)}.

Every selected white has at most one P neighbour. Take R empty and let D
be all five centres. None has a direct selected neighbour, so d=5.
The four HH paths printed below show h_D=4; since there are only four HH
sources, h_D cannot be larger. Hence s=1 and C_s=1.

Two minimum one-edge TH paths to the central centre are

    A_bad:  (5,8),(6,8),(7,8),(8,8),
    A_good: (8,5),(8,6),(8,7),(8,8).

The bad path has no direct-TH completion. To see this, take the chamber

    ([0,1] x [0,9]) union ([2,5] x [5,9]).

It has twenty black and twenty selected white vertices, and the direct
selected neighbourhood of its black vertices is exactly its white set.
A_bad withdraws the chamber white (5,8) to the central centre. If all
other TH paths were direct, the other four centres would require all four
HH sources, leaving none for the chamber. Its twenty black terminals would
then have only nineteen available selected neighbours, contradicting Hall.
The actual direct-remainder matching network also returns a physical Hall
certificate with 83 black vertices and only 82 allowed white neighbours.

For A_good, assign the four HH sources to their respective arm centres:

    (5,10),(4,10),(3,10),(3,11),(4,11),(4,12),(3,12),(2,12),
    (6,5),(6,4),(5,4),(4,4),(4,3),(4,2),
    (10,11),(10,12),(11,12),(11,13),(10,13),(10,14),(11,14),
        (11,15),(10,15),(10,16),(11,16),(12,16),(12,15),(12,14),
    (11,6),(12,6),(13,6),(14,6),(14,5),(14,4).

Each HH path lies inside its own square except for its first vertex.
Together with A_good these paths are vertex-disjoint, use fourteen actual
edges and supply nineteen auxiliary edges. Include the remaining forty-six
actual edges as common M/N edges.

For the exterior, use vertical pairs (a,b)--(a+1,b) in these columns:

| a | Columns b |
| --- | --- |
| 0 | 8,9,17 |
| 2 | 7,8,9,15,16,17 |
| 4 | 5,6,7,8,9,15,16,17 |
| 6 | 11,12,13,14,15,16,17 |
| 8 | 0,11,12,13,14,15,16,17 |
| 9 | 1 |
| 10 | 0,2,5,17 |
| 11 | 1,7,8,9 |
| 12 | 0,10,11,17 |
| 13 | 1,7,8,9 |
| 14 | 0,10,11,17 |
| 15 | 1,7,8,9,12,13,14,15,16 |
| 16 | 0,17 |

Remove the five square footprints, W, the entrance (8,5), and those vertical
endpoints. The remaining horizontal intervals are:

| Row | Intervals |
| --- | --- |
| 0,1 | [0,7], [15,16] |
| 2,3 | [5,6] |
| 4 | empty |
| 5 | [11,14] |
| 6 | empty |
| 7 | [0,5] |
| 8 | [1,4] |
| 9 | [2,5] |
| 10 | [3,4] |
| 11 | [3,4], [10,11] |
| 12,13,14,15 | empty |
| 16 | [10,11] |
| 17 | [1,16] |

All intervals have even length and tile horizontally. The sixty-four vertical
and thirty-three horizontal pairs give ninety-seven direct terminal paths.
The total is 19+46+64+33=162 disjoint edges, covering all 324 vertices.
Only A_good is a non-direct TH path, so the expense is one. A centre must
be TH because five centres share four HH sources, and every centre TH path
uses an actual edge. Thus the unrestricted optimum is exactly one.

Consequently, the same unit-weight physical subproblem has a minimum path
with a perfect direct remainder and another minimum path without one.
This refutes the rule that an arbitrary minimum C_s family may be used
to decide attainability. It supports the existential formulation of (3a)
without refuting that theorem or the grid colouring targets.

## 4. Exact recovery of the unit retained-pair optimum

Retain A and C from `RETAINING_PAIR_EXACT_UNIT_COST.md`. In the residual
8-by-12 board choose its seven-vertex Hall region D. Its remaining direct
selected neighbourhood has six vertices, so d=1. No residual HH path can
enter D, so h_D=0 and s=1. The shortest TH compensation from outside F
uses two actual edges:

    (0,11),(1,11),(2,11),(3,11),(3,10),(4,10).

Thus C_s=J_d=2 and b_R=2. The residual matching test succeeds and constructs
the full N of expense four. Equations (2)--(3) recover the exact retaining
optimum without enumerating full matchings. The unrestricted optimum remains
two. This also demonstrates why the two residual lower bounds cannot be
summed.

## 5. A centre and an exterior deficit compete for the same HH source

Use the fixed 12-by-18 geometry, actual matching and two cheap actual edges
from Section 6 of `SIMULTANEOUS_PORT_COMPLETION.md`. Retain both cheap paths

    A: (6,15),(5,15),(4,15),(3,15),
    C: (9,12),(9,11),(9,10),(9,9).

Their total expense is two. All residual actual edges have the same integer
weight K>=2. For a self-contained specification, the board is [0,11] x
[0,17], with 5-by-5 square origins (1,3),(1,13),(7,7). Delete the black
centre of each square to obtain its core. In each core translate the four
local actual edges

    (0,2)--(1,2), (2,0)--(2,1),
    (2,4)--(2,3), (4,2)--(3,2),

and the horizontal tilings of the four corner 2-by-2 squares with origins
(0,0),(0,3),(3,0),(3,3). These 36 edges form M. The cheap edges are
(5,15)--(4,15) and (9,11)--(9,10), each of weight one; all other actual
edges have weight K. Select every white Q except W={(6,7)}.

Let D_0 be the 17 black vertices in

    ({6} x [13,17]) union ([7,11] x [12,17]),

and let h_0=(3,5) be the remaining centre. In this coordinate region, row 6
contains TWO black and three white vertices, and rows 7--11 contain fifteen
of each. Thus there are 17 black vertices BEFORE AND AFTER the retained-path
deletion. The original selected neighbourhood has 18 white vertices. The
two removed entrances (6,15),(9,12) are both WHITE, leaving 16 direct selected
neighbours. No vertex of D_0 is removed. The sole HH source is (6,7).
The following residual capacities explain the obstruction:

| Region | Black vertices | Direct selected neighbours | Demand d | h_D |
| --- | ---: | ---: | ---: | ---: |
| D_0 | 17 | 16 | 1 | 1 |
| {h_0} | 1 | 0 | 1 | 1 |
| D_0 union {h_0} | 18 | 16 | 2 | 1 |

Each region separately could receive the one HH source. Their union can
receive it only once. At least one incoming path to the union is TH and
cannot be direct from outside its selected neighbourhood. It therefore
uses a residual actual edge, of weight K. This proves

    f_R* >= K+2.

The bound is exact for EVERY integer K>=2. Retain A,C and add

    T_0: (0,5),(1,5),(2,5),(3,5),

of expense K, and the free HH path

    (6,7),(7,7),(7,8),(7,9),(8,9),(8,8),(8,7),(9,7),(9,8),
    (10,8),(10,7),(11,7),(11,8),(11,9),(10,9),(10,10),(10,11),(10,12).

The four paths are vertex-disjoint and alternate with M. The HH path uses
eight residual actual edges; all are free in the TH objective.

For completeness, a direct exterior matching is fully specified by vertical
edges (a,b)--(a+1,b) at the following coordinates:

| a | Columns b |
| --- | --- |
| 0 | 2 |
| 1 | 8,9,12 |
| 2 | 2 |
| 3 | 0,1,8,9,10,11,12 |
| 4 | 2 |
| 5 | 0,1,8,9,10,11,12 |
| 6 | 2,3,4,5,6,13,14 |
| 7 | 0,1,12,17 |
| 8 | 2,3,4,5,6,15,16 |
| 9 | 0,1,17 |
| 10 | 6 |

Remove the three square footprints, HH source, selected entrances
(6,15),(9,12),(0,5), the exterior HH endpoint (10,12), and these vertical
endpoints. The remaining horizontal intervals are:

| Row | Intervals |
| --- | --- |
| 0 | [0,1], [3,4], [6,17] |
| 1,2 | [0,1], [10,11] |
| 3,4,5 | empty |
| 6 | [16,17] |
| 7 | [15,16] |
| 8,9 | [13,14] |
| 10 | [2,5], [13,16] |
| 11 | [0,5], [12,17] |

All intervals have even length. The 42 vertical and 26 horizontal edges
cover all 68 direct terminal pairs. The four relays supply 15 auxiliary
edges; put the 25 unused actual edges into N as common M/N edges, hence
doubled common components in the tagged overlay. The resulting
15+25+42+26=108 disjoint edges cover all 216 vertices. Its TH expense is
1+1+K, independent of the positive expense on the HH path. Consequently

    f_R*=K+2.                                                   (4)

Separately, the unrestricted optimum is K+1 by the independent lower bound
and attaining row tiling in Section 6 of
[`SIMULTANEOUS_PORT_COMPLETION.md`](SIMULTANEOUS_PORT_COMPLETION.md), fixed at
scientific revision `fe425797c43f4b8dc6c30ad3d98ef0fd3c5d7dfa`. It does not
follow from the retained-path theorem. The explicit 108-edge N, actual M,
terminal paths and capacity certificates accompany this note in
`output/residual-hall-certificates.json`; the independent checker reconstructs
their edge incidence, disjointness and complete coverage.

For the union region, h_D=1 and C_s=J_d=K. The constructed matching also
verifies that the matching test in Section 3 can succeed when an extra TH
centre releases the HH source for exterior compensation. Looking at the
two regions separately only gives the retained fee two, with an arbitrarily
large gap to (4).

## 6. The two residual lower bounds are incomparable

Here are two fixed-board controls, each with an all-K argument. They explain
why keeping both mechanisms is useful. They introduce no new matching method.

First use the 4-by-10 board with two 3-by-3 rings at origins (1,1),(1,7).
Translate the four-edge local ring matching from the 8-by-12 example.
Give every left-core actual edge weight K>=2 and every right-core actual
edge weight one. Set W={(0,7)} and select all other white Q. These selected
vertices have at most one P neighbour. Take R empty and D={(2,2),(2,8)},
the two black centres. Its direct neighbourhood is empty, so d=2. The
unique HH source can reach only the right core, giving h_D=1 and s=1.
A TH route into the right core has fee one, so C_s=1. The joint assignment,
however, must supply the left centre by TH, of fee at least K; pairing W
to the right centre attains J_d=K.

The true optimum is K. Take TH path (0,1),(1,1),(1,2),(2,2) and HH path
(0,7),(1,7),(1,8),(2,8). Match exterior vertices vertically in columns 0,6
between rows 0--1 and 2--3. The remaining row intervals are [2,5],[8,9]
in row 0 and [4,5] in each of rows 1--3; tile them horizontally. Retain the
six unused actual edges as common M/N edges. This gives a full matching.
Thus J_d/C_s=K can be unbounded even for feasible selected vertices.

For the reverse direction use [0,5] x [0,5], T={(2,1),(3,2)}, W empty,
D={(1,3),(2,4)}, R empty, and actual matching

    (0,0)--(0,1), (0,2)--(0,3), (0,4)--(0,5),
    (1,0)--(2,0), (1,1)--(1,2), (1,4)--(1,5),
    (2,2)--(2,3), (2,5)--(3,5),
    (3,0)--(3,1), (3,3)--(3,4),
    (4,0)--(4,1), (4,2)--(4,3), (4,4)--(4,5),
    (5,0)--(5,1), (5,2)--(5,3), (5,4)--(5,5).

Give (2,2)--(2,3) weight one, all other actual edges weight K>=2. Both
selected sources can reach both destinations through that cheap edge, so
J_d=2. But d=s=2, and two physical paths cannot share that edge. Each
needs an actual edge, so their joint fee is at least K+1. The disjoint
paths

    (2,1),(2,2),(2,3),(1,3),
    (3,2),(3,3),(3,4),(2,4)

attain K+1; retaining all other actual edges gives a full N. Hence
C_s=f*=K+1, and C_s/J_d is unbounded. This second control lies in the
general theorem's domain; its selected vertices have several P neighbours,
so it is not a feasible-selection example for the colouring problem.

## 7. Implementation and remaining scope

`scripts/residual_hall_compensation.py` computes both residual bounds,
physical path/cut and min-cost dual certificates, and the direct-TH remainder
test. Its `cheapest_non_direct_TH` function tests the hypothesis in (3a)
by the one-path network described above. It uses exact nonnegative integer
costs; the theorem permits real
nonnegative weights. The residual physical capacities are unique, including
in the HH max-flow computation. All reported lower bounds combine by max.

`scripts/check_residual_hall_compensation.py` checks full small-board matchings,
literal disjoint path families, endpoint assignments, reconstructed residual
dual potentials and cuts, and both explicit grid applications. Written proofs
establish the general and all-K statements; finite controls test the code.
The additional `scripts/check_positive_attainment.py` compares all optimal
physical path families with independent full-matching enumeration on small
boards, verifies (3a)--(3b), checks the zero-weight obstruction, and reconstructs
the printed unit-weight 18-by-18 matching and its rejected-path Hall certificate.
No universal unit-weight colouring improvement, rectangular-grid triple
equality, unrestricted exact optimizer or new Lean verification is claimed.
