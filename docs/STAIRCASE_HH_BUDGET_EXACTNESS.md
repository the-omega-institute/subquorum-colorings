# Exact HH-source compensation across an arbitrary staircase of cores

The shared-source two-core completion extends to ANY number of cores.
A single global outer matching absorbs the independently chosen internal
relays, and a capacity-one matching assigns the free white sources.
For every rematching and every nonnegative weight vector, the global
TH optimum is exactly the smallest of the core TH distances. This is
an explicit class where the cross-component source-budget bound is
attained, including positive source ambiguity and positive HH expense.

## 1. The feasible all-size family and the theorem

Choose r>=1 and positive integers k_1,...,k_r; no ordering is required.
Put S=sum_i k_i, H=4S+2, W=4S+2r. In the H-by-W rectangle set

    R_i=4 sum_(a<i) k_a,
    C_i=sum_(a<i)(4k_a+2),     n_i=4k_i+2,
    S_i=[R_i,R_i+4k_i] x [C_i,C_i+4k_i],
    h_i=(R_i+2k_i,C_i+2k_i),   P_i=S_i\{h_i}.

Black means even coordinate sum. Each S_i has black corners and black
centre. Let P be the union of the P_i, and let M be ANY actual grid
matching covering exactly P. Its edges split among the P_i: adjacent
core squares are separated by one Q column, and nonadjacent ones are
farther apart. Give the actual edges arbitrary nonnegative weights w_e.

Between consecutive cores put the white hole

    z_i=(R_i+4k_i,C_i+4k_i+1),     i=1,...,r-1.

Write Z={z_1,...,z_(r-1)}, Q=V\P, T=Q_white\Z, Hholes=Q\T.
Each z_i lies between the bottom-right black corner of S_i and the
top-left black corner of S_(i+1). These are the ONLY white Q vertices
with two P neighbours. Every T has at most one P neighbour and no T
neighbour, so the configuration is feasible under every rematching.
Its counts include

    |M|=8 sum_i k_i^2 + 4S,
    area/2=8S^2+4S(r+1)+2r,
    |T|=area/2-|M|-(r-1),
    |Hholes|=area/2-|M|+(r-1),
    J=area/2-(r-1).                                         (1)

For each core let rho_i be the minimum actual expense of a T-to-h_i
alternating terminal path whose interior lies in P_i. Only selected T
vertices are eligible paid sources; the white holes z_i are excluded.

**Theorem (exact staircase compensation).** Every rho_i is finite. For
EVERY M above and EVERY nonnegative actual-edge weighting,

    f* := min_(N full) f(N) = min_i rho_i.                    (2)

Moreover the generic capacity-one HH source-budget lower bound, using
all black Q terminals, shortest T-source fees, and ordinary directed HH
reachability, is exactly

    Lambda = min_i rho_i.                                   (3)

An optimal full N uses one shortest TH relay in a minimizing core. Each
other core receives a DIFFERENT white hole and one HH relay. All unused
actual edges are doubled; all remaining terminal components are direct
TH. The statement allows nonzero HH expense and arbitrarily many cores.
It is a geometry-specific theorem, not a general TH optimization algorithm.

## 2. Individual relay existence does not depend on M

The odd-square pad argument in
[the two-core note](SHARED_SOURCE_EXACT_WEIGHTED_REMATCHING.md#2-a-relay-to-a-boundary-white-pad-exists-for-every-actual-matching)
applies separately in every S_i. Pair an exterior white pad a with its
adjacent black boundary c and tile S_i\{c}. Taking the tagged union of
that auxiliary matching of S_i union {a} with M_i gives an alternating
h_i-to-a path, regardless of M_i. The other components are P-only cycles.

For each bottom midpoint, deleting c permits vertical pairing of the
first 4k_i rows and horizontal pairing of both even remaining bottom-row
intervals. Its exterior pad is selected T, supplying a TH relay. Deleting
the bottom-right or top-left corner permits vertical pairing of all but
the remaining end row, which is paired horizontally. Hence z_i can relay
to h_i or h_(i+1) under every rematching. All needed rho_i are finite.
Simple relays may be chosen, deleting nonnegative cycles if necessary.

## 3. A single near-perfect outer matching exposes every white vertex

Let B_i be the n_i-square block with top-left corner (R_i,C_i), and L_i
its outer right-column/bottom-row L, ordered downward then leftward.
Column intervals of the B_i are disjoint. Consecutive block row intervals
overlap in two rows. The only Q vertices in B_i are L_i and h_i.
For i<r, z_i is the even-index vertex 4k_i of L_i.

Remove every centre and white hole and write

    O=Q\({h_1,...,h_r} union Z).

O has one more white vertex than black; its white vertices are all T.
It is the disjoint union of L_i\{z_i} for i<r, the full last L_r, and

    U_i=[0,R_i-1] x [C_i,C_i+n_i-1],          i>1,
    D_i=[R_i+n_i,H-1] x [C_i,C_i+n_i-1],      i<r.

All nonempty U_i,D_i have positive even height at least four and positive
even width n_i.

**Outer deletion lemma.** For ANY white t in O, O\{t} has a perfect
direct matching.

Proof. Construct A on O as follows. In each L_i, i<r, delete z_i and pair
both even remaining segments consecutively. In L_r delete its FIRST
white vertex t_0=(R_r,W-1), and pair its remaining even path. Pair each
U_i,D_i horizontally in every row. Thus A covers exactly O\{t_0}.

Orient non-A grid edges white-to-black and A edges black-to-white. The
white vertices in any one U_i or D_i are mutually reachable. Contracting
horizontal A pairs proves this: vertical neighbours have directed
connections in both directions; horizontal directions alternate by row,
and an adjacent row supplies the reverse direction. This is the same
local rectangle argument as in the two-core outer lemma.

The upper rectangles U_2,...,U_r are mutually connected in BOTH directions.
For consecutive U_i,U_(i+1), their common row interval has positive even
height R_i. Across their adjacent column boundaries, even and odd rows
supply opposite alternating directions. Their individual strong
connectivity therefore joins all upper rectangles. Likewise D_1,...,
D_(r-1) are mutually connected: neighbouring lower rectangles have a
common suffix of rows of positive even height. The same opposite-parity
boundary edges provide both directions.

Starting from t_0, follow the alternating L_r to reach all its white
vertices. If r>1, the upward edge from t_0 enters U_r, reaching every
white U_i vertex. The leftward edge at the bottom-left white vertex
(H-1,C_r) of L_r enters D_(r-1), reaching every white D_i vertex.
For r=1 there are no rectangles or other L_i, and this L_r path alone
already covers all white O vertices.

For every i<r, the prefix white L_i vertices before z_i have coordinates
(R_i+2j,C_i+n_i-1), j=0,...,2k_i-1. Their predecessor black vertices one
row below have white neighbours directly to the right in U_(i+1).
Those black vertices' A mates are the indicated prefix whites. Thus
all these prefix whites are reachable. The remaining white L_i vertices
are on its bottom row, at (R_i+n_i-1,C_i+2j), j=0,...,2k_i. The black
vertices immediately to their right have white neighbours directly below
in D_i and A mates at the indicated bottom-row whites. These whites
are therefore reachable as well.

Every white O vertex is now reachable from t_0. Flip a simple alternating
t_0-to-t path in A; this matches t_0, exposes t, and preserves every
other incidence. It gives a perfect matching of O\{t}. QED.

This is a WHOLE exterior completion statement. The internally chosen
relays do not have to choose predetermined boundary ports, and the proof
preserves simultaneous competition for all black Q vertices.

## 4. A capacity-one free assignment and exact attainment

Every centre is a distinct black Q terminal. A full N has r-1 white HH
sources and hence can place at most r-1 centres on HH paths. At least
one centre h_i is TH, costing at least rho_i. Other TH fees are nonnegative,
so f(N)>=min_i rho_i.

Choose a minimizing core j. Assign white sources by

    z_i -> core i       for i<j,
    z_i -> core i+1     for i>=j.                            (4)

Every white hole is used ONCE and every core except j receives ONE.
The corner-pad argument supplies each of these HH relays. Choose a
shortest TH relay in core j, from a selected white vertex t to h_j.
Their internal P sets are disjoint; their terminal white endpoints are
z_1,...,z_(r-1),t, all distinct. Each relay uses full actual pairs
internally. Take their auxiliary edges and double every unused M edge.
This covers exactly P, all centres, all white holes, and t.

Apply the outer deletion lemma to O\{t}. It directly covers precisely
all remaining vertices. Its white endpoints are all T, so these new
components have zero TH expense. HH actual expense is free for f. The
only paid actual edges lie on the chosen TH relay, each used once.
Thus f=rho_j and (2) is proved.

For the generic source budget, every black O vertex has a direct T
neighbour, witnessed by A. Its shortest TH fee is zero. The centres have
shortest fees rho_i. A white source z_i can enter only cores i or i+1:
its other outgoing choices immediately meet black Q sinks, and internal
P routes cannot cross between cores. Both adjacent centre routes exist
by the corner-pad argument. Thus its positive-benefit graph is the path
incidence graph z_i--{h_i,h_(i+1)}. Any discount matching omits at least
one centre, so its benefit is at most sum rho_i-min rho_i. Assignment
(4), choosing a minimizing j, ATTAINS that benefit. Consequently
Lambda=sum rho_i-(sum rho_i-min rho_i)=min rho_i, proving (3). QED.

The discounts in this argument are a matching, not r independent claims
on the same white sources. The costs on paid paths sum across disjoint
actual-edge sets, not across projected components with reused resources.

## 5. Relation to forced all-terminal optimizer overpayment

For the old canonical M_i and unit weights, geometry gives rho_i>=k_i,
and each old straight relay attains k_i. Therefore f*=min_i k_i.
Using all straight TH relays, direct L_i completions and horizontal
outer pairings gives C=f=sum_i k_i. Each white hole z_i is directly
paired to the next black L_i vertex, so its HH expense is zero.

In ANY full N, a centre on TH contributes at least k_i actual edges.
If a centre h_i is HH, its source must be z_(i-1) or z_i. Each is at
distance 4k_i+1 from that centre, so this HH contributes at least 2k_i.
Hence every full N satisfies

    C(N)>=sum_i k_i + sum_(HH centres i) k_i.

Thus min C=sum_i k_i for the displayed canonical matching, and EVERY
C-minimizer must leave all centres TH. Since f<=C, every such minimizer
has f=sum_i k_i. The exact TH algorithm instead chooses which single
core pays and accepts positive HH relays in all the others.

With every k_i=1, the ratio is r. With r=2 and scales (K,1), it is K+1
while both area deficit and true TH optimum stay one, recovering the
stronger fixed-deficit obstruction from the earlier note. The exact
numeric attainments concern the canonical M. Arbitrary rematchings are
governed by rho, not by an assumed unchanged unit value k_i.

## 6. Algorithm and validation limits

`develop/staircase_source_completion.py` builds the family, computes every
rho by ordinary reversed Dijkstra search, chooses a minimum, and computes
the other cores' corner HH relays. It assigns sources as (4), flips one
outer alternating path, doubles unused actual edges and returns full N.
Selected boundary targets are found by scanning each core's P neighbours,
so constructing r target sets does NOT scan the whole board r times.
The core regions are disjoint and have bounded-degree grid graphs; all
shortest searches together, outer completion and reconstruction take
O(v log v) arithmetic operations and O(v) memory. Exact nonnegative
integer weights are accepted; the proof permits nonnegative real weights.
Dijkstra and alternating matching flips are standard algorithms.

The independent finite checks compare full physical decompositions and
the generic weighted HH discount lower bound, exercise paid cores at
both ends and in the interior, and verify every white outer deletion on
selected small footprints. The two-core specialization additionally has
all 38,416 actual matching pairs at its smallest footprint checked.
These computations test implementations; Sections 2-4 prove arbitrary
numbers of cores, sizes, rematchings and nonnegative weights. No new
Lean verification, literature priority or universal 5/6 improvement is
claimed. The exterior deletion property and core separation must be
proved afresh before applying this exactness beyond the staircase family.

Local result: `python3 develop/check_staircase_source_completion.py`
passed 1,703 white outer deletions on ten footprints, 588 single-core
rematching slices (all 196 matchings separately at each of three positions,
NOT all joint triples), and 49 weighted changed-rematching models. Each
weighted case compares independent forward Bellman-Ford distances, the
generic HH source budget, brute discount matching and old physical
decomposition. Twenty-one cases force the paid core at each available
position; zero and 401-digit weights are included. Canonical C witnesses,
three small complete-flow comparisons and four larger chains also pass.
The reproducible report is
[`output/staircase-source-exact-completion.json`](../output/staircase-source-exact-completion.json).

The two-core predecessor at `1aae8d6` independently received ACCEPT and
had its full checker rerun, task `0568223b-a629-49d0-ba3c-b1a664f97892`.
That verdict does not cover this subsequent arbitrary-r extension.
