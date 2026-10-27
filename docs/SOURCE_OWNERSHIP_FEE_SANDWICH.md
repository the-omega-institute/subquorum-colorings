# Source ownership gives a two-sided TH fee certificate and an exact separated class

The complete-terminal flow in
[the preceding note](MONOCHROMATIC_COMPLETION_FLOW_AND_UNBOUNDED_ZERO_DEFECT_COST.md)
minimizes all-terminal expense C, which may overcharge free HH paths.
Here two static reweightings bracket the actual TH objective. Their error
is confined to actual edges reachable from BOTH kinds of source. If no
positive-weight actual edge has that ambiguity, one standard complete
flow solves the TH problem exactly, even when HH paths necessarily have
arbitrarily large positive actual expense.

The construction couples all terminal routes in the SAME physical network.
It does not combine separately optimal component routes or duplicate an
actual edge. This is an application of standard flow optimization, not a
new general flow algorithm or a universal improvement of the 5/6 bound.

## 1. Data and the physical directed graph

Let G be a positive even-area rectangular grid; M any grid matching;
P its endpoints; Q=V\P; T a monochromatic subset of Q; H=Q\T.
Name the selected checkerboard colour white. T may be empty, in which
case choose either colour. Assign nonnegative actual-edge weights w_e.
Selection feasibility is not needed for the following theorem. In
particular it applies to feasible mixed-direction configurations.

Use the complete physical digraph D: M arcs black-to-white, other grid
arcs white-to-black. Q_white consists of the T sources and the H_white
sources; Q_black consists entirely of sinks. Write R_T and R_H for
ordinary directed reachability from those two sets, respectively. Paths
cannot pass through another Q source or continue beyond a Q sink.
For an actual edge e let b(e) be its black tail. Partition actual edges as

    A = {e: b(e) in R_T \ R_H},
    B = {e: b(e) in R_T intersection R_H},
    E = {e: b(e) in R_H \ R_T},
    F = M \ (A union B union E).

The sets include zero-weight edges. Put W_B=sum_(e in B) w_e, and define
nonnegative static actual-arc costs

    c_-(e) = w_e if e in A, otherwise 0,
    c_+(e) = w_e if e in A union B, otherwise 0.       (1)

Non-M arcs always have cost zero. For each weighting solve the SAME
complete flow problem of value q=|Q_white|=|Q_black|=area/2-|M|.
Let L and U be its respective minimum costs. Flow reconstruction, removing
circulations and doubling unused M, gives full auxiliary matchings N_-
and N_+. Let f(N) be the original w expense on TH paths, and f*=min_N f(N).
Define the computable full certificate

    F_best = min(f(N_-), f(N_+)).

## 2. Pointwise identities and the global sandwich

**Theorem 1.** Every full auxiliary N has zero TT paths. Let P_N be the
set of actual edges on ALL its terminal paths, and Paid_N the set on TH
paths. For the static all-terminal costs C_-(N) and C_+(N),

    f(N) - C_-(N) = sum_(e in Paid_N intersection B) w_e,      (2)
    C_+(N) - f(N) = sum_(e in (P_N\Paid_N) intersection B) w_e. (3)

Consequently

    L <= f* <= F_best <= U <= L+W_B.                          (4)

Thus F_best-L is a valid additive optimality certificate, at most W_B.
The easier-to-report interval [L,U] is also valid and U is no larger than
the earlier minimum original all-terminal expense Phi.

Proof. Each terminal path has odd length and opposite-colour endpoints,
so all TH paths begin at T and all HH paths begin at H_white when oriented
in D. Every actual edge on a TH path has its tail in R_T; thus it lies
in A or B. An actual edge on an HH path has tail in R_H; thus it lies in
E or B. Therefore an A edge on a terminal path is necessarily TH, an E
edge is necessarily HH, and F edges occur on no terminal path. This
proves (2)-(3), since P-only doubled components and other P-only cycles
contribute zero to all three costs.

All actual edges in a tagged M+N decomposition belong to exactly one
component. In particular the two sums in (2)-(3) use disjoint subsets of
B, and

    C_+(N)-C_-(N) = sum_(e in P_N intersection B) w_e <= W_B.  (5)

The standard complete-flow adapter supplies minima over ALL full N for
both static costings; it saturates every source and every sink and
reconstructs a full matching. Minimizing the pointwise inequalities gives
L<=f* and f(N_+)<=C_+(N_+)=U, hence the first four comparisons in (4).
Finally evaluate (5) on the lower-cost optimizer N_-:

    U <= C_+(N_-) <= C_-(N_-)+W_B = L+W_B.

This comparison uses a single compatible N_-; it never sums separately
optimized paths. Since c_+<=w edge by edge, its all-terminal minimum
U<=Phi. QED.

The number of potential paths through an ambiguous edge does not multiply
its contribution to W_B. Capacity one and the tagged component partition
are the reason for the bound. Neither d nor delta_0 provides this physical
resource information.

## 3. Exactness with positive HH expense

**Theorem 2 (separated positive source supports).** Suppose W_B=0; that
is, every actual edge reachable from BOTH source classes has weight zero.
Then for EVERY full N,

    C_-(N)=f(N)=C_+(N),

and either modified complete flow computes f* exactly. The hypothesis is
sufficient; it is not claimed necessary. Even if W_B>0, a returned
certificate with F_best=L proves its matching optimal.

Proof. The sums in (2)-(3) vanish under W_B=0. Apply Theorem 1. The last
claim follows directly from its lower bound and feasible certificate.
QED.

This strictly extends the earlier condition (Z), which required every
positive actual edge reachable from H_white to be absent. Condition (Z)
implies W_B=0, but the present condition allows arbitrarily expensive
actual HH paths in E. Those edges receive zero static cost. T and H may
still compete for direct sinks; the complete flow preserves that joint
constraint. The separation criterion is about positive ACTUAL resources,
not about independent spatial boxes or disjoint Q neighbourhoods.

This result does not assert that original all-terminal C equals f.
Typically it does not. The modified objective and its full-flow solver
are essential.

## 4. A feasible all-k family showing strict extension

For k>=1 put n=4k+2. Take two copies of the established n-square isolated-
hole core, placed in the left and right n-square blocks of an n by
(2n+2) rectangle, with a two-column Q strip between them. The right copy
is translated by n+2 columns, an even translation. Each core has

    S={0,...,4k}^2, black hole h=(2k,2k), P_core=S\{h},

and the old explicit mixed-direction M covering P_core. Its surrounding
right-column/bottom-row L contains all its white Q and its other black Q;
the black centre h is isolated in Q. In the whole rectangle select T to
be ONLY the white L vertices of the left copy; select no vertex in the
right copy or separating strip.

Every T has at most one P neighbour and no T neighbour, so the original
selection feasibility holds. The two-column strip separates the P cores.
A white Q source can enter a core only through its adjacent black P
boundary. All white Q neighbours of the left core are its selected T;
all white Q neighbours of the right core are H. After leaving a core,
a path hits a black Q sink and stops. Thus no actual edge can be reached
from both source types. All actual weights may be positive: W_B=0.
This source separation depends only on the two endpoint footprints, so
it persists under any actual rematching within either footprint. No edge
can connect the two P sets across the strip.

For unit weights each centre-to-boundary terminal path has length at
least 2k+1 and therefore at least k actual edges, under every rematching.
The left path must be TH. The right path must be HH: there is no T
source that can enter its core. Hence every full N has TH fee at least
k and original all-terminal expense at least 2k.

For the displayed old M, use its straight k-edge relay and direct L
completion in each block; double unused actual edges; pair the two strip
columns horizontally in every row. This is a full N. Its only nondirect
terminal paths are one TH and one HH, each with k actual edges. Therefore

    f*=L=U=k,       Phi=2k,       W_B=0.                     (6)

The original (Z) fails: the HH relay contains positive actual edges.
Indeed every full N must pay at least k in its HH path as measured by C.
The new modified flow nevertheless optimizes TH expense exactly. Thus
positive HH expense can be unbounded without creating any TH optimization
ambiguity. This example is NOT a counterexample to the numerical 5/6 or
half-area target.

## 5. Sharp width and the meaning of an ambiguous edge

The additive comparison U-L<=W_B can be tight within the theorem's stated
domain. On the 3-by-4 board use unit weights and

    M={[(1,1),(1,2)], [(1,3),(2,3)], [(2,0),(2,1)]},
    T={(0,1),(1,0)}.

There is exactly one ambiguous actual edge, [(1,3),(2,3)]. For a zero-TH
certificate take

    N_0={[(0,0),(1,0)], [(0,1),(0,2)], [(0,3),(1,3)],
         [(1,1),(1,2)], [(2,0),(2,1)], [(2,2),(2,3)]}.

Its only nondirect terminal path is HH using [(1,3),(2,3)], so f*=L=0.
All three actual edges are in A union B. The black Q vertex (2,2) has
only P neighbours, so every full N has all-terminal cost at least one.
For an upper certificate take

    N_1={[(0,0),(0,1)], [(0,2),(0,3)], [(1,0),(1,1)],
         [(1,2),(2,2)], [(1,3),(2,3)], [(2,0),(2,1)]}.

Its all-terminal cost is one. Thus U=1, and
U-L=W_B=1; scaling all three actual weights by w>=0 scales this width to w.
This small control does not satisfy the original selection-feasibility
condition (T=(1,0) has two P neighbours). It establishes sharpness for
Theorem 1, which explicitly does not assume that condition; no sharpness
claim restricted to feasible selections is inferred.

An ambiguous edge need not create an actual optimality gap. The same
example's lower optimizer can attain f=0, so the a posteriori certificate
F_best=L closes the gap despite U>L. Reachability records possible
origins independently of simultaneous capacity competition, and therefore
supplies safe bounds, not a necessary obstruction to exact optimization.

## 6. Implementation and validation scope

`develop/source_ownership_cost_bounds.py` performs the two multi-source
reachability searches and calls the existing complete-flow adapter with
c_- and c_+. It compares the two returned FULL matchings under the original
weights. It makes no shared solver, CI, or manuscript change. Arithmetic-
operation time for these two flows is O(v^3) on grids, memory O(v+e), for
exact nonnegative integer weights; bit-operation costs depend on integer length. The
mathematical theorem permits nonnegative real weights. Under W_B=0 the
two costings coincide and a single call would suffice; the implementation
keeps both for uniform certificate output.

`develop/check_source_ownership_cost_bounds.py` checks (2)-(3) pointwise
against independent full-N decompositions, compares f* with the existing
exact frontier, tests residual dual potentials, and verifies the all-k
family's explicit full N and source supports. It also includes zero and
401-digit weights, both checkerboard colours, T empty and all sources
selected. Its report is `output/source-ownership-cost-bounds.json`.
Finite checks establish implementation evidence; Sections 2-4 prove the
arbitrary-size statements. No new Lean verification is claimed.

The implementation additionally computes the capacity-one
[weighted HH source budget](HH_SOURCE_BUDGET_AND_FORCED_FLOW_OVERPAY.md)
and combines the two lower bounds. This auxiliary matching calculation
has separate worst-case O(v^4) time and O(v^2) memory bounds.

The unresolved general case is positive B with max(L,Lambda)<F_best. The interval
makes that remaining ownership ambiguity explicit. It does not solve the
full two-source TH optimization or provide a universal fee upper bound
from scalar Hall defects.
