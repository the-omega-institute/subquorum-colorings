# A capacity-one HH source budget, and forced factor-two TH overpayment

A scalar hole count cannot be spent separately by two components. This
note makes that restriction into a weighted matching lower bound and a
feasible all-size counterfamily for the all-terminal optimization rule.
The family has J=area/2-1 and positive TH optimum k. EVERY minimum-C full
matching has TH fee 2k. The failure concerns the choice of objective C,
not existence of a good physical matching or the numerical 5/6 target.

## 1. A weighted source-capacity lower bound

Keep the one-colour setting and physical digraph D of
[SOURCE_OWNERSHIP_FEE_SANDWICH.md](SOURCE_OWNERSHIP_FEE_SANDWICH.md).
Write W=H_white for the free HH source set, and K any subset of black Q
terminals. For each b in K choose a finite nonnegative number ell_b that
lower-bounds the actual w expense of EVERY TH path ending at b.
Use any bipartite graph Gamma on W and K which contains a link h--b
whenever an HH terminal path from h to b is possible in a full N.
Ordinary reachability h-to-b in D supplies a computable safe superset.
Give each link h--b benefit ell_b. Let Delta be the maximum total benefit
of a matching in Gamma; sources and black terminals both have capacity 1.

**Theorem (weighted HH source budget).** Every full N satisfies

    f(N) >= Lambda := sum_(b in K) ell_b - Delta.             (1)

This is a GLOBAL lower bound, with no selection of mutually incompatible
TH routes and no assumption that independently shortest routes can coexist.

Proof. Every black Q vertex is the endpoint of exactly one terminal path;
its white endpoint is either T or a member of W. The HH paths ending in
K induce a matching of their distinct W sources with their distinct black
endpoints in Gamma. Its benefit is at most Delta. The other black endpoints
in K belong to distinct TH paths, each of fee at least ell_b. These TH
paths have disjoint actual edge sets in the tagged physical decomposition,
so their charges may be added once each. Therefore

    f(N) >= sum_(b in K with a TH endpoint) ell_b
          = sum_(b in K) ell_b - sum_(b in K with an HH endpoint) ell_b
          >= sum_(b in K) ell_b - Delta.

The same white hole cannot be matched to two black endpoints in this
argument. Ignoring that matching capacity would invalidate (1). QED.

A useful cardinal special case is r mandatory black terminals, each with
TH expense at least ell, and only s admissible HH sources. Then
f(N)>=(r-s)_+ ell. Gamma can improve on the raw count when different
sources can only reach certain groups of black terminals.

For a computable choice use the shortest D-path expense from any T to b.
If no such path exists, ell_b=0 is a safe finite relaxation (the endpoint
must actually be HH). This deliberately does not enforce consumption of
a hole source by unreachable endpoints, and may weaken the lower bound;
it cannot overstate it. Unit-weight geometric distance bounds are another
choice, as used below. Combining (1) with the static-cost lower bound L
from the preceding note gives max(L,Lambda)<=f*.

The discount matching is a standard weighted bipartite matching. An
implementation with nonnegative costs sends one unit from each h, with
an unmatched option of cost K0=max ell_b and a link of cost K0-ell_b.
Subtracting that minimum cost from |W|K0 gives Delta. This is an exact
finite algorithm for the lower bound, not an exact algorithm for general
TH optimization.

## 2. Two odd cores sharing a single white source

For k>=1 put n=4k+2 and use a rectangle of height 8k+2 and width 8k+4=2n.
Let the two odd core squares be

    S_1 = {0,...,4k} x {0,...,4k},
    S_2 = {4k,...,8k} x {4k+2,...,8k+2}.

Their black centres are h_1=(2k,2k) and h_2=(6k,6k+2). Put
P_i=S_i\{h_i}, and let M_i be the established mixed-direction isolated-
hole matching translated into S_i. Let M=M_1 union M_2, P=P_1 union P_2.
The P sets have no adjacent pair across cores, so every actual rematching
on P also remains within its own core. Select

    z=(4k,4k+1),       T=Q_white\{z}.

Thus z is the ONLY white H. The only white Q vertex adjacent to both
cores is z, situated between their black corners (4k,4k) and (4k,4k+2).
All other white Q vertices have at most one P neighbour. Since T is
monochromatic, it has no T neighbour; the configuration is feasible.

Counts are

    |M|=16k^2+8k,
    |T|=16k^2+16k+3,
    |H|=16k^2+16k+5,
    J=32k^2+24k+3=area/2-1.                                (2)

Both centres are isolated in Q and belong to different terminal paths:
both are black, whereas every terminal path has opposite-colour endpoints.
Every T is outside its respective S_i, at distance at least 2k+1 from
h_i. Hence every TH path ending at either centre has at least k actual
edges, regardless of rematching on P. Only z can provide an HH path.
The source-budget theorem with K={h_1,h_2}, ell_1=ell_2=k and |W|=1 yields

    f(N)>=k                                                  (3)

for every full N and every rematching, under unit actual weights. This
is exactly the point at which independently crediting z to both cores
would incorrectly yield zero.

## 3. An explicit full matching attaining the TH lower bound

The old n-square completion block B_1={0,...,n-1}^2 contains S_1 and its
outer right/bottom L_1 path. The second completion block B_2 is its
translation by (4k,n). The blocks are vertex-disjoint. Their row intervals
overlap in two rows, but their column intervals are disjoint.

Use in B_1 the L-shaped alternating relay from z to h_1:

    z, (4k,4k), (4k-1,4k), ..., (2k,4k),
       (2k,4k-1), ..., (2k,2k)=h_1.

Its first and last edges are N edges; its interior alternates with the
old M. It has length 4k+1 and exactly 2k actual edges. Both endpoints are
H, so all its actual expense is FREE for f. In L_1, z has even index 4k.
Delete z, pair consecutive vertices in the two even remaining segments,
and double every unused M_1 edge. This covers B_1 fully, as in the old
completion lemma, with one long HH and all other paths direct TH.

In B_2 use the translated old straight relay from (8k+1,6k+2) to h_2,
with k actual edges; its white endpoint is selected T. Delete that even-
indexed endpoint from L_2, pair its two even remaining segments, and
double unused M_2. This covers B_2 fully, with one long TH of fee k.

Outside the two blocks, each row consists either of the right n-column
interval (rows 0..4k-1), no vertices (rows 4k..4k+1), or the left n-column
interval (rows 4k+2..8k+1). All intervals have even width. Pair them
horizontally. Those vertices are all Q and every white one is selected T,
so every such pair is direct TH. No vertex is left unmatched or shared.

This full N has f(N)=k and C(N)=3k. Together with (3),

    f*=k                                                     (4)

for the explicit M. Only the lower bound, not attainment k, is asserted
uniformly under all actual rematchings. For the explicit M the weighted
source-budget implementation also gives Lambda=k: the shortest T-to-
centre fees are k and the unique H source can discount at most one.

## 4. EVERY all-terminal minimizer incurs TH fee 2k

In each block instead use its old straight k-edge relay and its direct L
completion, double unused M, and horizontally pair the same outside rows.
Both long relays are TH. The unique z lies on a DIRECT HH edge in the
left L completion. Hence this full N satisfies C=f=2k.

For any full N, consider the paths of the two centres. If both are TH,
they contribute at least 2k to C. If one is HH, its white endpoint is z.
For BOTH i,

    distance(z,h_i)=4k+1,

so that HH path has at least 2k actual edges. The other centre must be
TH and contributes at least k. Thus the second case has C>=3k. It follows
that Phi=min C=2k and every C-minimizer has both centres on TH paths.
Those two paths already contribute TH fee at least 2k. Since f<=C=2k,
EVERY C-minimizer satisfies

    f(N_C)=2k = 2 f*.                                       (5)

This is stronger than merely showing Phi>f*: no choice of tie-breaking
among all-terminal optimal flows repairs the TH overpayment. Accepting
a longer positive-expense HH relay is necessary to achieve TH optimum.
The additive overpayment k is unbounded while the area deficit stays one.

The counterexample refutes the rule "optimize the all-terminal expense,
then its returned TH fee is optimal". It does not refute the valid upper
bound f*<=Phi, conditional exactness under (Z), or the source-separated
modified objective of the preceding note. Nor does it refute the target
numerical colouring inequalities or improve their universal coefficient.

## 5. Evidence, implementation, and the remaining problem

`develop/terminal_source_budget.py` computes shortest T-source distances
and the capacity-one maximum discount. The two static complete flows
remain coupled physical routes; their candidate matchings are evaluated
under the original objective. A candidate meeting max(L,Lambda) is then
certified optimal. Positive ambiguity with a remaining interval is still
unresolved in general.

Worst-case arithmetic-operation costs for the budget implementation are
O(v^4) time and O(v^2) memory: its auxiliary bipartite graph can be dense,
and it reuses the existing Bellman-Ford successive augmentations. Physical
reachability and the two original grid flows themselves use O(v^3) time,
O(v+e) memory. Exact integer bit lengths are additional; the written lower
bound permits arbitrary nonnegative real weights. No new generic matching
algorithm, shared CI change, manuscript edit or Lean verification is made.

`develop/shared_hole_chambers.py` gives both explicit full matchings and
its long HH path. `develop/check_source_ownership_cost_bounds.py` checks
all-size-family coordinate instances, exact paid-edge identities, weighted
source-budget bounds against independent full-N enumeration and the old
exact frontier, and weighted maximum-discount matching by separate brute
force on the small instances. The generated report records finite scope.
The statements for EVERY k and every C-minimizer rest on Sections 2-4,
not on extrapolation from enumeration.
