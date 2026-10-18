# Sharp compensation in every regular bipartite degree

19 October 2026. Finite simple graphs, non-induced two-stars, and
inclusion-minimal forming sets are used throughout. Write beta_2 for the
maximum size of a vertex set inducing maximum degree at most one, and
SF_2 for the maximum cardinality of a minimal two-star-forming set.
These are extensions of the cubic compensation theorem, with a uniform
two-connected construction attaining the bound in every degree d>=3.
Literature priority is not asserted by the proof or by finite checks.

A selection S is two-star-forming when every outside vertex x has either
two selected neighbors, or a selected neighbor which itself has a selected
neighbor. Minimality means that every proper subset fails this property.
The condition is upward closed, so testing all single deletions suffices.

## General exchange lemma

Let G be bipartite, S minimal forming, s=|S|, and T=V minus S. Partition S
into isolates I, vertices P of selected K2 components, leaves U supported
by high selected vertices, and H={v in S:|N(v) intersect S|>=2}.
Let a(v)=|N(v) intersect S|, z=|I| and u=|U|.

There is an injective outside failure-witness map f:H->T. A witness
cannot be shared by distinct high vertices: every old covering star
would have to contain both; one high center has a second selected
neighbor giving a replacement star avoiding the other. Each witness has
selected degree one or two. A nonadjacent witness has one selected
neighbor, a leaf whose unique support is its high owner. Call its
owner good. An adjacent witness has selected neighborhood {v} or {v,w}
with w in I: failure requires w to be isolated after deletion, and a
previous edge vw would create a triangle. Call this owner bad.
These statements do not require degree three.

Every selected leaf has an adjacent outside failure witness with selected
neighborhood {u} or {u,w}, w in I. Its deletion leaves the leaf itself
covered through its high support, while a destroyed star at a nonneighbor
can replace the leaf by another neighbor of that support. This forces an
adjacent witness. Its other selected neighbor must be isolated, since
the leaf's sole selected neighbor is its high support. Distinct leaves
have distinct witnesses. A degree-two leaf witness cannot belong to f(H),
and a degree-one overlap belongs only to its leaf's unique good support.

Put g=number of good high vertices. Let r1,r2 count unused vertices of T
of selected degrees one and two. Removing those overlaps before using
unused witnesses gives

    0 <= K:=u-g <= r1+r2.                                  (1)

For a bipartition L,R, form D_L from P, U, I intersect R, H intersect L,
and all witnesses f(v) in R. At each kept good high vertex keep one leaf;
at each kept bad high vertex remove all leaves, keeping its adjacent
witness as its partner. Reverse L,R to obtain D_R.

A kept good high pairs with its retained leaf. A kept bad high pairs with
its witness; the witness's other possible neighbor is an omitted isolate
in L. An added nonadjacent witness pairs with a leaf whose support in R
is omitted. There are no other edges to selected vertices by the stated
witness neighborhoods. The added vertices are all in R and hence
mutually nonadjacent. P keeps its matching edges, and the retained
isolates in R have no selected neighbors. Thus both sets are dissociation
sets. This checks all edge types, with no degree restriction.

Each leaf is trimmed only at its unique support. Total trimming is
sum_good(c(v)-1)+sum_bad c(v)=u-g, where c(v)=|N(v) intersect U|.
Every P/U vertex starts in both sets,
every isolate and high once, and every witness once. Consequently

    |D_L|+|D_R|=2s-z-K,
    2(s-beta_2(G)) <= z+K <= z+r1+r2.                       (2)

This is the general bipartite exchange lemma. In particular, selected
isolates are paid once across the two alternative sets, and leaf demand
never reuses an already chosen high witness.

## Weighted theorem

Let Delta>=3 be any integer bounding the maximum degree of G. Then
every minimal forming S satisfies

    sum_(v in S)(deg_G(v)+Delta+1) <= Delta n+2 beta_2(G).   (3)

Here n=|V(G)|; connectivity and regularity are not assumed. To prove it,
write C_x=Delta-a(x) and q_v=C_f(v)-(a(v)-1). These are nonnegative:
an adjacent witness gives a(v)<=Delta-1 and a(f(v))<=2, while a
nonadjacent witness gives a(v)<=Delta and a(f(v))=1.
The exact cut/slack identity is

    B:=Delta n-sum_(v in S)(deg_G(v)+Delta-1)
      =z+sum_(v in H)q_v+sum_(x in T minus f(H))C_x.

This follows by counting edges across S,T in both directions, as in the
degree-capacity proof. Formation forces a(x)>=1 for every outside vertex.
The unused degree-one and degree-two witnesses therefore supply

    B >= z+(Delta-1)r1+(Delta-2)r2 >= z+r1+r2.

All other unused capacities are nonnegative and are discarded only
after the high witness capacities have been paid. Combining this with
(2) gives2(s-beta_2)<=B, exactly (3). The condition Delta>=3 pays the
degree-two unused witnesses; this argument is not asserted with Delta=2.
For graphs of lower maximum degree one may still choose Delta=3.

If the minimum degree is delta, a consequence is

    (delta+Delta+1)SF_2 <= Delta n+2 beta_2.                 (4)

For every d-regular bipartite graph with d>=3,

    (2d+1)SF_2 <= dn+2 beta_2,
    SF_2-beta_2 <= floor(n/(4d+2)).                         (5)

Indeed beta_2>=n/2, by choosing a bipartition part, so with gap=SF_2-beta_2
the first inequality gives(2d-1)beta_2+(2d+1)gap<=dn and hence
(2d+1)gap<=n/2. This proves the second inequality.

## A uniform two-connected attaining construction

Fix d>=3. Take independent classes A={a_i}, B={b_i}, X={x_i}, Y={y_i},
each indexed by i modulo d, and vertices p,q. The bipartition is

    L=A union X union {p},  R=B union Y union {q}.

Add all a_i--b_j with i!=j; add a_i--y_i and b_i--x_i; join p to all
Y and q to all X. Finally add x_i--y_j precisely when

    j-i is not congruent to1or2 modulo d.

The outside X--Y graph is(d-2)-regular and contains every x_i--y_i.
Thus G_d is simple, bipartite and d-regular of order4d+2.
The set S=A union B union {p,q} has size2d+2. Each outside vertex has
two selected neighbors, its high matching neighbor and one isolate.
Deleting a_i uncovers y_i, deleting b_i uncovers x_i, and deleting
p or q uncovers the deleted isolate itself. Hence S is minimal forming.
The nonnegativity B>=0 gives(2d-1)|S|<=dn for every minimal selection
in a regular graph. Thus the degree-capacity bound, independently of
the dissociation calculation below, gives

    SF_2 <= floor(d(4d+2)/(2d-1))=2d+2,

since d(4d+2)=(2d-1)(2d+2)+2 and2<2d-1. Thus SF_2=2d+2.

The high crown graph G[A union B] is two-connected. One explicit
Hamilton cycle alternates a_i,b_(i+2),a_(i+1), with indices modulo d.
Both adjacent high indices differ because d>=3. Adding each internally disjoint
path a_i--y_i--x_i--b_i preserves two-connectivity, as does adding p
and q, each with at least two neighbors already present. The remaining
edges also preserve it. This proves two-connectivity without computation.

## Exact dissociation number of the construction

Every G_d satisfies beta_2=2d+1. A whole part attains the lower bound.
For d>=4, FRACTIONAL_SQUARE_GAP_OBSTRUCTION.md now gives a shorter
independent upper-bound proof by explicit positive square weights. The
case argument below remains valid and includes the square-free d=3 case.
Here is an upper-bound proof; for d>=4 it even allows any(d-2)-regular
X--Y graph in place of the specified one.

For a dissociation set D write

    a=|D intersect A|, b=|D intersect B|,
    x=|D intersect X|, y=|D intersect Y|,
    epsilon=1_(p in D), eta=1_(q in D).

If a,b>0, then a,b<=2: each selected vertex in the opposite high class
has at least a-1 or b-1 selected neighbors. Thus a+b<=4. If a+b=4,
the two chosen index sets coincide and all four high vertices already
have degree one in D. Their matching ports are forbidden, so

    x,y<=d-2.                                             (6)

If x,y>0, then x,y<=3, since each outside vertex has at most two
nonneighbors in the opposite outside class. Also epsilon=1 implies
y<=1, and eta=1 implies x<=1. It follows that

    x+y+epsilon+eta<=6,                                   (7)

with equality only at x=y=3 and epsilon=eta=0. If one isolate is
selected the left side is at most five, and if both are selected it
is at most four.

For d>=5, suppose first both high classes and both outside classes
are nonempty. The bound a+b<=4 and(7) give|D|<=10<=2d+1. If exactly one high
class is nonempty and both outside classes are nonempty, then
|D|<=d+6<=2d+1. If both high classes are empty, (7) suffices when
both outside classes are nonempty; with only one outside class,
|D|<=d+2<=2d+1.

If exactly one high class is nonempty and at most one outside class is
nonempty, assume b=0 by symmetry. For y=0, either eta=0 and
|D|=a+x+epsilon<=2d+1, or eta=1 forces x<=1 and
|D|<=d+3<=2d+1. For x=0 the same argument uses epsilon to restrict y.
If both high classes are nonempty but at most one outside class is
nonempty, then|D|<=4+d+2=d+6<=2d+1 for d>=5. This covers every case.

For d=4 the preceding one-high/one-outside argument still holds. When
both high classes and both outside classes are nonempty, a size ten
set would require a=b=2 and x=y=3 with no isolates, contradicting(6).
When just one high class and both outside classes are nonempty, a size
ten set would require all four vertices in that high class and x=y=3,
without isolates. Every selected vertex in the matching outside class
already has its high partner, so there can be no edge between the
chosen X,Y. But each chosen X has at least y-2=1 chosen Y neighbor,
a contradiction. If both high classes and at most one outside class
are nonempty, a+b<=3 gives|D|<=3+4+2=9. Otherwise a=b=2; by(6) the
single outside class contributes at most two, giving|D|<=4+2+2=8.
The case with no high class is bounded by at most six. Hence|D|<=9.

For d=3 the specified X--Y graph is the identity matching. The
neighborhoods of left vertices are

    N(a_i)=B minus {b_i} union {y_i},
    N(x_i)={b_i,y_i,q},  N(p)=Y.

Any two left vertices have at most one common right neighbor: two a's
share one b; two x's share q; a_i,x_j share y_i if i=j and b_j
otherwise; pairs with p share only the appropriate y. Thus the graph
has no four-cycle. If a dissociation eight-set existed, choose the
part with at least four selected vertices, and let k<=3 be its omitted
vertices. The other part has k+1 selected vertices, each adjacent to
at least two omitted vertices. Their chosen omitted-neighbor pairs
are distinct, since a repeated pair creates a four-cycle. This gives
k+1<=binomial(k,2), impossible for0<=k<=3. Thus beta_2<=7.
Any larger dissociation set would contain an eight-set, so it is also excluded.

We have proved for every d>=3 that

    |V(G_d)|=4d+2,  SF_2(G_d)=2d+2,  beta_2(G_d)=2d+1.

Both inequalities(5) are equalities. In particular the coefficient
1/(4d+2) is sharp even among two-connected d-regular bipartite graphs.
Disjoint unions attain arbitrary integer gaps at the same coefficient.
Attainment by arbitrarily large connected graphs, or unbounded connected
gaps at that coefficient, is not implied by this fixed-order construction.
The subsequent [broken-block and ring proof](REGULAR_CONNECTED_SHARP_GAPS.md)
does establish both properties for every d>=4, with a precise cubic
obstruction to that same local-cap argument.

## Validation and remaining work

The general proof above does not depend on enumeration or optimization.
The companion checker constructs both exchanges from literal stars on
906 bipartite graph instances and403,976 subsets, testing9,775 minimal
selections and19,550 exchanges. It checks the weighted inequality against
exact dissociation optima, including exhaustive SF optima for G_3,G_4.
Separate controls inspect the displayed attaining family for degrees3to16,
560 vertex removals and693,407 forbidden-size subsets at degrees3,4,5.
These cases are controls, not an exhaustive graph-class classification.

Five additional symbolic Lean4.33.0 audits pass, covering unused capacities,
weighted accounting, regular coefficient conversion, variable-degree
integer gap arithmetic, and the later linear-equality residual vanishing
lemma, using only standard logical axioms. They ran
locally and sequentially after a memory and actual lean/lake preflight.
The graph exchange, finite cardinal summation and construction upper-bound
proof remain written. The complete graph theorem is not claimed fully
Lean-formalized. Reproduce the finite controls with
`python3 scripts/check_regular_compensation.py --output output/regular-compensation-controls.json`.
The symbolic runner is `scripts/check_regular_compensation_formal.py`.

The independent Oracle input is archived in
`reviews/2026-10-19-regular-compensation-review-input.md`. Its completed
response accepts the general exchange, weighted theorem, all-degree
sharpness and two-connectivity. The recommended definition and count-case
clarifications are incorporated. The original response and scope are in
`reviews/2026-10-19-regular-compensation-oracle-response.txt` and
`../output/regular-compensation-oracle-review.json`. That input predates
the connected ring, equality structure and covering pullback results;
those are not attributed to its acceptance. General-degree literature
comparison remains required before any priority claim or manuscript proposal.

The rectangular-grid equality and psi_sq<=SF_2 bridge remain open. This
note does not improve the existing5/6sub-quorum bound.
