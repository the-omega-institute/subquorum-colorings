# Complete terminal flow and unbounded expense at two fixed Hall defects

The previous note showed d=0 need not extend to a zero-paid-set full N.
Here the obstruction becomes arbitrarily expensive while BOTH d=0 and
whole-board defect delta_0=1 remain fixed. We also give a polynomial,
unrestricted physical completion adapter using ordinary minimum-cost flow.
It gives an upper bound on TH expense, and is exact under an explicit
condition preventing positive expense on HH paths. A second family shows
why that condition cannot simply be dropped.

These are statements about physical compensation, not a new universal
numerical coefficient. They leave the submitted manuscript unchanged.

## 1. Definitions and the distinction between two costs

Let G be an even-area rectangular grid, M any fixed actual grid matching,
P its endpoints, Q=V\P, T a subset of Q of one checkerboard colour, and
H=Q\T. Call the selected colour white; interchange the names if needed.
M may have both horizontal and vertical edges. We do not need selection
feasibility for the flow theorem.

Every full auxiliary matching N gives terminal paths of the tagged M+N
union, and P-only cycles (a common M/N edge is a doubled cycle). Each
terminal path has odd length, so opposite-colour endpoints. Therefore
no TT path is possible when T is monochromatic. Every white Q vertex
is a path source and every black Q vertex its sink. Black Q is all H;
white Q consists of T and possibly additional H.

For nonnegative actual-edge weights define

    f(N) = total M weight on TH paths,
    C(N) = total M weight on ALL terminal paths, including HH.

P-only cycles contribute zero to both. Resources are the actual edges,
not projected component counts. Since each actual edge belongs to exactly
one tagged component,

    0 <= f(N) <= C(N).                                        (1)

Let Phi=min_(N full) C(N), and f_*=min_(N full) f(N). The inequality
f_*<=Phi is an upper bound from a constructible certificate, unlike the
Hall lower bounds from the preceding note.

## 2. A standard one-commodity flow that preserves full completion

Orient every actual edge from its black endpoint to its white endpoint,
with capacity one and cost equal to its weight. Orient every NON-M grid
edge from white to black, with capacity one and cost zero. Add a super
source with capacity-one zero-cost arcs to EVERY white Q vertex, and
capacity-one arcs from EVERY black Q vertex to a super sink. Let

    q=|Q_white|=|Q_black|=|V|/2-|M|.

Actual vertices themselves enforce capacity: at a black P vertex the
unique actual outgoing arc has capacity one, and at a white P vertex
the unique actual incoming arc has capacity one. Terminal capacities
serve the same purpose on Q. There is no independent copy of an actual
edge for each potential payment. Full routing requires value q, not |T|.

**Theorem 1 (complete flow adapter).** This network has an integral flow
of value q. Its minimum cost among value-q flows is exactly Phi. A
minimum-cost flow constructs a full physical N with no TT paths and

    f(N) <= C(N) = Phi.                                      (2)

There is no restriction to prescribed tiles, band-closed M, bounded
width or bounded cycle rank.

Proof. Begin with any full N, which exists on the ambient even-area
rectangle. Its tagged terminal paths, oriented from white Q to black Q,
alternate zero-cost N arcs and actual M arcs, with actual direction as
specified. Their vertices are disjoint. They produce a feasible value-q
flow of cost C(N); ignore P-only cycles. Shared physical M/N edges are
doubled P-only components and never occur on such a terminal path, so
excluding M from the zero-cost arc set is correct.

Conversely, decompose an integral value-q flow into source-sink paths and
circulations. Remove the circulations; nonnegative weights mean this
cannot increase cost. The unit capacities just described imply that
physical paths have disjoint vertices, including actual M pairs and
terminal endpoints. Delete the super arcs. Use their white-to-black
NON-M arcs as N edges. Every unused actual edge is then also placed in
N as a doubled component. Used actual pairs are covered by the two
adjacent N edges along their path; unused actual pairs are covered by
that doubled edge. Every Q vertex is a source or sink because value=q
saturates all q source arcs and all q sink arcs. Thus N covers ALL board
vertices. Its terminal-path resource sets are exactly the used actual
path arcs, each once. This constructs N with C(N) at most the flow cost.
Comparing both directions proves equality of minima, and an optimal
flow can be chosen without circulations. Equation (1) gives (2). QED.

This is the standard matching-decomposition and integral min-cost-flow
construction, adapted to the unrestricted physical model. It is not a
new general flow theorem. The earlier strand/contact flows optimize
specified links or gates; here all physical non-M grid edges are available
and EVERY Q vertex must be accounted for.

## 3. A sufficient condition for exact TH expense

Let D be the oriented physical network before adding the super nodes.
Let R be the vertices reachable in D from the white holes H_white.
Assume

    every actual arc whose black tail is in R has weight zero. (Z)

Reachability ignores capacity competition, so it is a safe sufficient
condition, not a claimed necessary test.

**Theorem 2 (zero-expense HH reachability).** Under (Z), every full N
satisfies C(N)=f(N). Consequently the complete flow adapter computes the
exact unrestricted TH optimum f_*=Phi.

Proof. An HH path must have its white endpoint in H_white and is oriented
from that endpoint in D. Every actual arc on it therefore has tail in R,
so weight zero by (Z). Thus the HH contribution C-f is zero for every
full N. Apply Theorem 1. QED.

Two easy sufficient cases are:

* H_white has NO neighbour in P: every HH path is a single direct HH edge.
* H_white is empty, including every monochromatic selection with
  J=|M|+|T|=|V|/2. Indeed Q is colour-balanced, and this equality forces
  T=Q_white, so there are no HH paths.

The second case allows any actual mixed-direction M and arbitrarily
wide boards. It is an exact physical fee algorithm for that class,
not a proof that every configuration belongs to it. Condition (Z) also
allows HH relays through zero-weight actual edges.

Implementation reuses the existing exact-integer residual `Network` in
`develop/check_residual_reserve_cost_profile.py`; no shared solver or CI
is modified. Successive Bellman-Ford residual shortest augmentations,
including reverse arcs, give a minimum-cost maximum flow. A final residual
potential verifies nonnegative reduced costs. With v physical vertices,
e ambient grid edges and q sources, the implementation has time
O((q+1) v e), hence O(v^3) on grids, and O(v+e) memory, counting arithmetic
operations on exact integers. Zero-cost circulations are discarded before
doubling unused M. The implementation accepts nonnegative INTEGER weights;
the mathematical adapter and Theorem 2 hold for nonnegative real weights.

## 4. New family: d=0, delta_0=1, but exact TH fee=k

**Theorem 3.** For every integer k>=1 there is a feasible (4k+4)-square
configuration with both actual directions present and

    J=area/2-1, d=0, delta_0=1, min_(N full) f(N)=k             (3)

under unit actual weights. Every full N has zero TT paths. The lower
bound k holds under EVERY rematching on its endpoint footprint; the
explicit M below attains k. It follows that no finite bound depending
only on (d,delta_0,area/2-J) can control actual TH expense.

We reuse the established isolated-hole core from
[UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md](UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md),
whose earlier family had d=1 at exact half-area. The additional work here
is an outer completion with direct defect ZERO and only one unit of
area deficit, while the long path remains forced to be TH, not free HH.

Construction. Put n=4k+2 and enlarge the old n-square to side n+2. Let

    S={0,...,4k}^2, h=(2k,2k), P=S\{h}, z=(0,4k+3).

Use the old actual M covering P: vertical pairs in every column of S,
with first rows 0,2,...,2k-2 and 2k+1,2k+3,...,4k-1; in row 2k use
horizontal pairs in columns 0..2k-1 and 2k+1..4k. Define

    T={white vertices of V\P}\{z}, H=V\(P union T).

Thus z is the ONLY white H. It lies three columns outside S and has
only black H neighbours. The central black hole h is isolated in Q.
Every T outside S has at most one P neighbour (along a flat side of S),
and no T neighbour. Hence this configuration is feasible, under every
actual rematching on P. Counts give

    |M|=8k^2+4k, |T|=12k+7, |H|=12k+9,
    J=8k^2+16k+7=(4k+4)^2/2-1.                              (4)

Explicit direct coverage. Let L be the old outer L-path

    (0,n-1),(1,n-1),...,(n-1,n-1),(n-1,n-2),...,(n-1,0).

It has 8k+3 vertices and starts and ends in T. Pair consecutive vertices
of L AFTER its first vertex. Pair that first T=(0,n-1) with (0,n).
In the added two columns n,n+1, pair horizontally in rows 1..n-1.
In the added bottom two rows n,n+1, pair vertically in every column
0..n+1. These edges cover precisely Q\{h,z}: each has one T and one
black H. Therefore d=0. This direct matching together with M is a
G_0 matching of size area/2-1, proving delta_0<=1.

Persistent whole-board Hall witness. Let X be ALL black vertices of S.
Its G_0-neighbours are precisely the white vertices of S. Every physical
neighbour outside S is white T and is excluded by the G_0 rule; z is too
far away to add a neighbour. Since S is an odd square with black corners,

    |X|=|M|+1, |N_(G_0)(X)|=|M|.

Hence delta_0>=1, proving delta_0=1.

Unavoidable weighted path length. All T are white, so every full N has
no TT path. The only white H, z, has no P neighbour and therefore always
belongs to a direct HH edge. The isolated h cannot lie on that HH edge;
its tagged path must run to a white T. Every T is outside S, at Manhattan
distance at least 2k+1 from h. A terminal path with r actual edges has
length 2r+1, so its TH path has r>=k distinct actual edges. This argument
uses only the endpoint footprint, colour and geometry, so survives every
actual rematching on P. Unit TH expense is at least k.

Attainment for the explicit M. Use the old straight path

    (4k+1,2k),(4k,2k),...,(2k,2k)=h,

with k actual edges. Remove its first T from L and pair consecutive
vertices in the two remaining even subpaths. Double every actual M edge
not used by the long path. In the added columns pair horizontally in
ALL rows 0..n-1; in the added bottom rows pair vertically in all columns.
This is a full N. All added pairs are TH except the pair z--(0,n), which
is direct HH. Its only paid actual edges are the k edges on the displayed
long TH. This attains (3). No actual edge or hole is used twice. QED.

Theorem 2 applies because z has no P neighbour. Thus ordinary complete
min-cost flow computes exact weighted TH optimum on this family for any
fixed actual rematching and weights. Only the unit lower bound k is
asserted uniformly over rematchings; a rematching may have higher optimum.

## 5. Why complete flow cost is not always exact TH cost

**Theorem 4 (unbounded free-HH overcharge).** Without (Z), Phi-f_* can
be unbounded even with T nonempty, J=area/2-1 and d=delta_0=0.

Use the ORIGINAL side-(4k+2) isolated-hole core with its P and M. Move
only the old straight path's source t*=(4k+1,2k) from T to H; keep every
other old selected vertex. This is feasible. The same old full matching
now has the long path as HH, and every remaining T is directly matched
to H. Its TH expense is zero; therefore f_*=0 and its matching lies in
G_0, giving delta_0=d=0. Here |T|=4k+1>0 and J=area/2-1.

Nevertheless every full N has a terminal path ending at isolated h,
and every other Q vertex lies on L at distance at least 2k+1. Whatever
its endpoint type, that path has at least k actual edges counted by C.
The displayed full matching attains C=k, hence Phi=k while f_*=0.
This does not refute the complete flow upper bound. It refutes treating
its all-terminal objective as an unconditional exact TH objective. QED.

## 6. Evidence and remaining problem

`develop/monochromatic_completion_flow.py` is the standard complete-flow
adapter; `develop/zero_defect_long_relay.py` builds both families by reusing
the established core. `develop/check_monochromatic_completion_flow.py`
independently compares against full N enumeration and the existing exact
frontier on small boards. Its completed scope is recorded in
`output/monochromatic-completion-flow.json`.

The arbitrary-size constructions, rematching lower bound and objective
separations above are written proofs, not extrapolations from the finite
checks. No new Lean verification or literature-priority claim is made.
The remaining issue for this adapter is positive-cost HH routing, and
for the original compensation programme is a useful global expense bound
from geometry and unique resource capacities. Scalar Hall defects alone,
even with one unit of area deficit, cannot supply that bound.

The local completed check has 778 exhaustive one-colour models on seven
small boards, plus 76 seeded larger models. It scores 44,331 complete N
and makes 854 exact frontier comparisons. Both families have 40 coordinate
controls; for k=1..8, 24 complete flow computations and 16 whole-board
matching tests check the claimed costs, sufficient-condition flags,
zero-weight reachability and Hall defects. These are implementation checks
with fixed integer weights, not exhaustive weight assignments.
