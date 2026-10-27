# Direct Hall coverage need not extend to a full auxiliary matching

The direct T-to-H Hall defect from the closed-ladder note detects a shortage
of direct hole partners. It does not detect every obstruction to extending
those partners to a perfect matching of the entire board. Here we give an
exact whole-board test, a component-replacement lower bound, and a feasible
family on every even h-by-w board, h,w>=4, with direct defect zero but
unavoidable payment. The family has J=hw/2-1 and an exact weighted optimum.

These statements concern physical compensation certificates. They do not
refute the numerical target, improve the universal 5/6 coefficient, or
change the manuscript supplied for journal submission.

## 1. Definitions and an exact extension criterion

Let G be an even-area rectangular grid. Let M be a fixed grid matching,
P its endpoints, T a subset of V(G)\P, and H=V(G)\(P union T). A full
auxiliary matching N covers every vertex. The tagged union M+N decomposes
into alternating paths with endpoints in T union H and P-only cycles;
a shared M/N edge is a doubled cycle. Write a(N) for its number of TT
paths and Paid(N) for the set of actual M edges on TH paths. Set
p(N)=|Paid(N)| and f(N)=sum_(e in Paid(N)) w_e for nonnegative weights.
Each actual edge has exactly one component owner.

Define G_0 by retaining precisely the grid edges uv satisfying

    (u not in T or v in H) and (v not in T or u in H).           (1)

Thus every T may connect only to H; all grid edges within P union H
remain. In particular every actual M edge remains. Rectangular even-area
grids have equally many black and white vertices, n=|V|/2. Let

    delta_0 = n - nu(G_0),                                     (2)

where nu is maximum matching cardinality. By the standard bipartite
matching theorem this also equals max_(X subset black)
(|X|-|N_(G_0)(X)|). This is an application of ordinary bipartite matching,
not a new maximum-matching algorithm.

**Theorem 1 (exact empty-paid-set criterion).** A full N with a(N)=0
and Paid(N) empty exists if and only if delta_0=0.

Proof. With a=0, every T is an endpoint of a TH path. If Paid is empty,
no such path contains an M edge. Each is therefore a single N edge from
T to H. All N edges satisfy (1), so N is perfect in G_0. Conversely,
a perfect matching in G_0 pairs each T directly with H. Such a pair is
an entire tagged component because both endpoints lie outside P. Hence
there are no TT paths and no paid M edges. QED.

If every actual weight is strictly positive, Theorem 1 is equivalent
to the lexicographic numerical optimum (a,f)=(0,0). With zero weights,
this equivalence to numerical zero need not hold: a nonempty paid set
can have total weight zero. The empty-paid-set statement itself is
independent of weights.

For comparison, put d=|T|-nu(G[T,H]), the direct T-to-H defect. Always
delta_0=0 implies d=0, but the converse fails in Section 4. There is a
useful exact-density exception: if |T|=|H|, then d=0 does suffice. A
matching covering T also covers all H, so its union with M is already a
full N in G_0. In the notation J=|M|+|T|, this case is J=|V|/2.
Consequently the example at J=|V|/2-1 occurs at the first integer below
this density where such an extension obstruction could occur.

## 2. Component replacement gives a stronger counting inequality

**Theorem 2.** For every full N, without a selected-degree hypothesis,

    a(N) + p(N) >= delta_0.                                    (3)

More precisely, if k(N) counts the TH paths containing at least one
actual M edge, then a(N)+k(N)>=delta_0.

Proof. On each TT path replace all its N edges by all its M edges. Do
the same on each nontrivial TH path. An alternating terminal-to-terminal
path starts and ends with N, so it contains one more N edge than M
edge. Each replacement loses exactly one matching edge and leaves its
two terminal endpoints unmatched. This includes direct TT paths, whose
M edge set is empty. Keep the original N edges on direct TH paths,
HH paths and P-only cycles.

The tagged components have disjoint vertex sets, so all replacements
and retained edges together form a matching. Every retained direct TH
edge lies in G_0; HH paths and P-only cycles contain no T; every inserted
M edge lies in P. The resulting matching is therefore in G_0 and has
exactly n-a-k edges. By (2), delta_0<=a+k. Distinct nontrivial TH paths
own disjoint nonempty sets of actual M edges. Choosing one actual edge
from each gives an injection into Paid(N), so k<=p. This proves (3).
No resource is assigned to two replacement components or counted twice.
QED.

Together with the earlier direct-hole estimate 2a+p>=d, this gives

    p >= max(0, d-2a, delta_0-a).                              (4)

For unit actual weights, p=f. In particular a=0 forces f>=delta_0;
this can be stronger than f>=d, including when d=0. For arbitrary
nonnegative weights, (3)-(4) bound the NUMBER of paid actual edges,
not their total weight. They are lower bounds on any certificate, not
upper bounds establishing a globally cheap certificate.

## 3. A four-by-four core

Use zero-based coordinates and set

    e_top   = (0,1)--(0,2),
    e_left  = (1,0)--(2,0),
    e_right = (2,3)--(3,3),
    M = {e_top,e_left,e_right},
    T = {(0,3),(1,2),(2,1),(3,0)}.

The vertex types, with each P paired by the displayed M, are

    H P P T
    P H T H
    P T H P
    T H H P

Every T has exactly one neighbour in P union T, so the original
selection condition |N_G(v) intersect (P union T)|<=1 is satisfied.
Here J=3+4=7=16/2-1. The four disjoint direct edges

    (0,3)--(1,3), (1,2)--(1,1),
    (2,1)--(2,2), (3,0)--(3,1)                                (5)

cover T, proving d=0.

Nevertheless the black set

    X = {(0,0),(0,2),(2,0)}

has exactly two G_0 neighbours,

    N_(G_0)(X) = {(0,1),(1,0)}.                               (6)

Indeed the other neighbours of (0,2) are T=(0,3),(1,2), and the other
neighbours of (2,0) are T=(2,1),(3,0); those edges were deleted. Thus
delta_0>=1 and no direct matching covering T can extend to a full
zero-paid-set auxiliary matching.

Two complete N witnesses will also be used for weighted exactness:

    N_top = {(0,3)--(0,2), (0,1)--(0,0),
             (1,2)--(1,3), (2,1)--(1,1),
             (3,0)--(3,1), (3,2)--(2,2),
             (1,0)--(2,0), (2,3)--(3,3)},

    N_left = {(3,0)--(2,0), (1,0)--(0,0),
              (0,3)--(1,3), (1,2)--(1,1),
              (2,1)--(3,1), (2,2)--(3,2),
              (2,3)--(3,3), (0,1)--(0,2)}.                    (7)

Both have a=0. Their paid sets are respectively {e_top} and {e_left};
the other two actual edges are doubled free cycles. Replacing the
unique nontrivial TH path by its M edge leaves a G_0 matching of size
seven. Together with (6), this proves delta_0=1.

## 4. An arbitrary-size near-half-area family and its exact optimum

**Theorem 3.** For every even h,w>=4 there is a feasible mixed-direction
configuration with

    J=hw/2-1,  d=0,  delta_0=1,

and, under ANY nonnegative weights on all actual edges, exact unrestricted
lexicographic optimum

    (a_min,f_min_given_a_min) = (0,min(w_top,w_left)).           (8)

The paid set cannot be empty, even when the minimum weight is zero.

In fact every full N in this family has a(N)=0, not just the optimum.

Construction. Start with Section 3 in the northwest corner. For each
added column pair c,c+1, c=4,6,...,w-2, in rows 0..3, use

    H T
    T H
    P P   [horizontal actual edge]
    P P   [horizontal actual edge].                           (9)

For each added row pair r,r+1, r=4,6,...,h-2, put HT/TH in columns
0,1. In columns 2,3 put one vertical actual edge per column. In every
remaining column pair 4,5;6,7;... put a horizontal actual edge in each
row. All these actual edges are disjoint.

Feasibility. The core T at (0,3),(3,0) acquire only H neighbours when
extended; the two other core T keep their existing neighbours. Each
new T in row 1 has exactly one P neighbour below; its other neighbours
are H. Each new T in row 0 has only H neighbours. In every lower band,
T=(r,1) has its sole P neighbour at (r,2), and T=(r+1,0) has only H
neighbours, including across the next band boundary. Neighbours across
successive column pairs and row bands respect these same labels.
Thus every T has at most one neighbour in P union T.

Counts and direct coverage. Each top four-row column pair adds two
actual edges and two T, increasing J by four, exactly half its area.
Each added two-row band has w-2 actual edges and two T, increasing J
by w, again half its area. Hence J=hw/2-1. Add to (5) the horizontal
TH edges in each new HT/TH pair. They cover all T without collisions,
proving d=0. This also explicitly gives |H|=|T|+2.
More explicitly, |T|=h+w-4, |M|=hw/2-h-w+3 and |H|=h+w-2.

Persistent obstruction. Extending right and downward adds no neighbours
to X in (6), so that deficient Hall set persists. Hence delta_0>=1.
Extend either N in (7) by the horizontal TH pairs just described and
by doubling every added actual edge. These choices cover every added
vertex and have no cross-block N edges. All added actual edges remain
free doubled components. The resulting full N has a=0 and respectively
paid set {e_top} or {e_left}. Theorem 2 gives delta_0<=1, so delta_0=1.

Weighted lower bound. Every full N must match some vertex of X outside
the two neighbours in (6). The ONLY grid edges from X missing in G_0
are the four edges from (0,2) to the two adjacent T and from (2,0) to
the two adjacent T. Thus N must contain one of these four T-to-P
edges. Its tagged alternating component contains the actual M mate of
that P vertex, namely e_top or e_left. If a=0, the component starting
at that T ends at H, so this actual edge belongs to Paid(N). Since
all weights are nonnegative, f>=min(w_top,w_left). The two witnesses
attain the two respective weights, proving (8). This argument also
proves Paid nonempty independently of numerical zero weights. QED.

There is also a local way to see the forced payment, noted in the
independent review. Every T in the construction has odd coordinate sum.
An alternating terminal path has one more N edge than M edges, hence
odd length and opposite-colour endpoints. Consequently no full N can
have a TT path in this family. Moreover H=(0,0) must be N-paired to
(0,1) or (1,0). Following its actual mate reaches (0,2) or (2,0),
respectively. Its remaining possible N neighbours are all T (the
predecessor P is already N-matched to the corner H). Thus this forced
TH component contains e_top or e_left. This gives the weighted lower
bound directly for EVERY full N, including zero-weight cases.

For unit weights this has (a,f)=(0,1), saturating (3), while the earlier
direct estimate only gives f>=0. The example disproves the RULE that
d=0 alone guarantees a zero-paid-set full extension. It does not
disprove existence of full coverage or any proposed numerical bound
on J. At exact half-area the rule is valid by Section 1.

## 5. Relation to previous results and validation

The direct bound and the all-size closed-ladder construction are in
[CLOSED_LADDER_ZERO_FEE_COMPENSATION.md](CLOSED_LADDER_ZERO_FEE_COMPENSATION.md).
The known d=1 family with unbounded minimum relay expense is in
[UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md](UNBOUNDED_ISOLATED_HOLE_RELAY_COST.md).
That earlier result already shows that direct defect cannot quantitatively
control expense from above. The additional issue here is failure of full
extension when d=0, its exact standard matching test, the a+p lower bound,
and an arbitrary-size feasible example with an exact weighted formula.
No literature-priority claim for these elementary matching deductions is
made. The frontier solver and its proof remain unchanged.

Implementation: `develop/zero_fee_extension.py` builds G_0, uses standard
iterative augmenting paths, and returns a maximum matching and a Hall set
attaining delta_0. Here E(G) denotes the AMBIENT grid edges, not just the
retained G_0 edges. Its time bound is O(|V||E(G)|), O(|V|^2) on a grid,
with O(|V|+|E(G)|) memory. More explicitly, including sorted vertices,
the time is O(|V| log |V| + |V| (|E(G_0)|+1)); the ambient rectangular
grid has |E(G)|=Theta(|V|). The distinction matters when G_0 has no
edges. It also constructs Theorem 3's witnesses.
`develop/check_zero_fee_extension.py` compares with exhaustive matching
recursion and an independent older tagged-component decomposition;
`output/zero-fee-extension.json` records the actual completed checks.
Those finite checks test implementations and controls. The arbitrary-size
statements are established by the proofs above. No Lean verification is
claimed for this note.

Independent review `92ca804c-6440-4d28-909e-71d0e5d168a7` returned ACCEPT
for source `303aecac07227a3b250352187144a021e6301ad4`. The reviewer actually
ran the original checker and reproduced all 3,137 exhaustive models,
24,621 full-N evaluations and 800 frontier comparisons, matching the
report both as parsed JSON and byte for byte; no Lean was run. The
reviewer's nonblocking ambient-edge complexity clarification and the
same-colour/corner observations above were incorporated. The strengthened
all-family-N no-TT assertion was then rerun locally; that revised-source
execution is distinct from the reviewer's original execution. See
`output/hall-extension-review.json` for the full response and exact scope.
