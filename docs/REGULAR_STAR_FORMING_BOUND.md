# A degree-capacity bound for upper 2-star formation

19 October 2026. The arguments below apply to finite simple graphs, using
non-induced copies of K_{1,2} and inclusion-minimal star-forming sets.
They do not require bipartiteness, connectivity, or finite enumeration.
Literature priority is not asserted; see the source-specific literature note.
Here beta_2 is the maximum size of a set inducing maximum degree at most
one, and SF_2 is the maximum size of an inclusion-minimal forming set.

Favaron's 2012 Theorem10 already gives SF_k<=n-delta+k-1 for k<=delta,
and her Theorem13 characterizes its SF equality case for k>=2. For
d-regular graphs at k=2, that bound is n-d+1. The degree-capacity bound
below is strictly stronger when d>=2 and n>2d-1. These are different
order bounds and equality problems; this specific comparison does not
establish historical priority over all later literature.

## The bound

Let G have order n and maximum degree Delta. Let S be an inclusion-minimal
2-star-forming set, put T=V(G) minus S, and let z be the number of isolated
vertices of G[S]. Then

    sum_{v in S} (deg_G(v)-1) + z <= Delta |T|.                 (1)

In particular, if G has minimum degree delta and delta+Delta>=2, then

    (delta+Delta-1)|S| + z <= Delta n.                         (2)

For every d-regular graph, d>=1,

    (2d-1)|S| + z <= dn,
    SF_2(G) <= floor(dn/(2d-1)).                              (3)

Thus every cubic graph satisfies SF_2(G)<=floor(3n/5). This is an
order bound for all minimal sets, rather than an evaluation of one family.

## An injective witness budget

Write a(v)=|N(v) intersect S|, and H={v in S:a(v)>=2}. A vertex x outside
a selection is covered precisely when it has at least two selected neighbors,
or has a selected neighbor with another selected neighbor. Formation is
upward closed, so minimality is equivalent to failure of every single deletion.

For v in H, the newly omitted v is covered after deleting v: its two
selected neighbors form a star centered at v. Therefore some x in T loses
coverage. Call such an x a failure witness of v.

No x witnesses two different v,w in H. If it did, every star covering x
before deletion would contain both v and w, and so would have vertex set
{x,v,w}. At least one of v,w is adjacent to x; say v. Since a(v)>=2,
v has a selected neighbor y different from w. The star x--v--y avoids w,
contrary to x witnessing w. Consequently all witness sets are nonempty
and pairwise disjoint. Choose an injective witness map f:H->T.

For x=f(v), a(x)<=2: if a(x)>=3, deleting one selected vertex leaves two
selected neighbors of x. Moreover, if x is not adjacent to v, then a(x)=1,
since its selected-neighbor set is unchanged and it would remain covered
as a center if a(x)>=2. Formation before deletion also gives a(x)>=1.

The witness has enough degree capacity to pay for a(v)-1:

    a(v)-1 <= Delta-a(f(v)).                                 (4)

Indeed, if x is adjacent to v, the outside edge vx gives a(v)<=Delta-1,
while a(x)<=2. If x is not adjacent to v, use a(v)<=Delta and a(x)=1.
These prove (4), including the cases with triangles. If H is empty no
witness choices are needed. Injectivity, and nonnegative unused capacities,
now give

    sum_{v in H}(a(v)-1) <= sum_{x in T}(Delta-a(x)).           (5)

Every witness capacity occurs at most once. This is the precise mechanism
that prevents reuse of the same outside budget at a branch.

The number of edges crossing from S to T has the two expressions

    sum_{v in S}(deg_G(v)-a(v)) = sum_{x in T}a(x).

Add this identity to (5). Since vertices of S outside H have selected
degree zero or one, the resulting left side is exactly
sum_{v in S}(deg_G(v)-1)+z. The right side is Delta|T|. This proves (1).
Lower-bounding each deg_G(v) by delta proves (2), and setting delta=Delta=d
proves (3). An edgeless graph satisfies (1) directly with S=V(G).

There is an exact slack identity useful for stability questions. Put
C_x=Delta-a(x) and q_v=C_{f(v)}-(a(v)-1), all nonnegative. Then

    Delta|T| - [sum_{v in S}(deg_G(v)-1)+z]
      = sum_{v in H}q_v + sum_{x in T minus f(H)}C_x.          (5a)

For a d-regular graph this becomes

    dn-(2d-1)|S|
      = z + sum_{v in H}(d-a(f(v))-a(v)+1)
          + sum_{x in T minus f(H)}(d-a(x)).                 (5b)

Thus equality forces every displayed nonnegative term to vanish; there is
no cancellation between different witnesses or unused vertices.

## Sharpness for every regular degree

For d>=2, take four independent parts A,B,C,D of sizes d,d,d-1,d-1.
Add a perfect matching between A and B, all edges A--D, and all edges
B--C, with no other edges. This is a d-regular bipartite graph, with
bipartition A union C and B union D and order 4d-2.

The set A union B has size 2d and induces a matching. Every omitted vertex
has d>=2 selected neighbors, so the set is star-forming. After deleting
any selected vertex, its only remaining selected neighbor is its matching
partner, now selected-isolated. The deleted vertex is uncovered. Thus the
selection is inclusion-minimal and

    beta_2(G)=SF_2(G)=2d=dn/(2d-1).

The upper beta bound also follows directly by counting the cut of any
dissociation set: each selected vertex sends at least d-1 edges outside,
and each outside vertex receives at most d. For d=1 use a single edge.
The examples are two-connected for d>=2. For d=2 the graph is C6.
For d>=3, each complete bipartite piece stays connected after one deletion,
and at least d-1 surviving matching edges join the pieces.

## Equality structure in all regular graphs

Suppose d>=2, G is a finite simple d-regular graph, and a minimal S attains
(2d-1)|S|=dn. Then the following disjoint decomposition into five labeled
classes is forced; some classes may be empty.

- P consists of the vertices in selected K2 components.
- H consists of selected vertices of selected degree d.
- U consists of selected leaves adjacent to H.
- X consists of outside vertices of selected degree one.
- Y consists of outside vertices of selected degree d.

These five sets partition V(G). Every vertex of H has exactly one neighbor
in U; every vertex of U has exactly one neighbor in H and one in X; every
vertex of X has exactly one selected neighbor, in U. These edges give
bijections H<->U<->X. Both G[H] and G[X] are (d-1)-regular. Every remaining
edge from U or P goes to Y, and Y is independent. In particular, each
vertex of U has d-2 neighbors in Y and each vertex of P has d-1.

Here is the necessity proof, including the equality conditions in the budget.
Equality in (3) forces z=0. It also forces equality at every term in (4),
and forces every unused outside capacity Delta-a(x) to vanish.

First, a selected leaf u adjacent to a high vertex h has a private outside
witness x with N(x) intersect S={u}. Indeed, the newly omitted u remains
covered through h, which retains another selected neighbor. An outside
nonneighbor of u cannot fail: an affected star must use u as a leaf and
h as its center, and h can replace u by another selected neighbor. An
outside neighbor x with at least three selected neighbors also survives.
If x has exactly two selected neighbors u,w, failure requires w to become
selected-isolated. Since z=0, w had u as its sole selected neighbor; but
u's only selected neighbor is h, contradicting a(h)>=2. Thus x has just u.

Such an x has capacity d-1>0, so equality forces x=f(v) for a high v.
It is nonadjacent to v, since u is its sole selected neighbor and is a leaf.
Deleting v can uncover x only by deleting u's support h, hence v=h.
Tightness in (4) now forces a(h)=d. We have proved that every high vertex
adjacent to a selected leaf has full selected degree.

A high v cannot have an adjacent chosen witness with a(x)=1: the outside
edge gives a(v)<=d-1, making (4) strict. An adjacent chosen witness with
a(x)=2 is also impossible. Its other selected neighbor u must become
selected-isolated after deleting v. Since z=0, u was a selected leaf
adjacent to v; the preceding paragraph forces a(v)=d, contradicting the
outside edge vx. Thus all high witnesses are nonadjacent, a(v)=d for
all high v, and their witnesses have a(x)=1. Every unused outside vertex
has a(x)=d. Hence X=f(H), |X|=|H|, and the remaining selected degrees
are one. This proof does not assume triangle-freeness.

For x in X, let u be its sole selected neighbor. Loss of coverage after
deleting its high witness v requires u to have v as its sole selected
neighbor. Hence u is a selected leaf adjacent to v. Distinct v have
distinct such leaves, so |U|>=|H|. Conversely, the private-witness argument
above assigns each u in U a witness in X having u as its sole selected neighbor.
Different leaves cannot share it, so |U|<=|X|=|H|. Equality gives all
claimed bijections. The remaining degree and neighborhood statements follow.

Conversely, any d-regular graph with this decomposition and these
neighborhoods has S=P union H union U minimal star-forming: vertices of Y
are centers, vertices of X are leaves supported by U--H; deleting a P
vertex uncovers itself, deleting u in U uncovers its matched x, and
deleting h in H uncovers the x matched through its unique leaf. The cut
and bijections give (2d-1)|S|=dn.

## Bipartite extremal sets have no gap

If G is d-regular and bipartite, d>=2, then

    SF_2(G)=dn/(2d-1)  if and only if  beta_2(G)=dn/(2d-1).     (6)

The reverse implication follows from beta_2<=SF_2 and (3). To prove the
forward implication, take an extremal S and its partition above. Let L,R
be the bipartition. The matching H<->U<->X pairs each h with an x in the
same part. Replace S by

    D = P union U union (H intersect L) union (X intersect R).

Every u in U has exactly one selected neighbor in D, since exactly one
of its paired h,x is selected. Every selected h or x has its unique U
neighbor and no other neighbor in D. Each P vertex retains only its mate.
Thus D induces a matching and |D|=|S|. This proves (6) constructively.
For d=1 both parameters equal n.

For cubic bipartite graphs, a positive gap therefore forces
5 SF_2<=3n-1. The standard bipartition lower bound beta_2>=n/2 then gives

    SF_2-beta_2 <= n/10,
    10(SF_2-beta_2) <= n-2  when the gap is positive.            (7)

These are universal bounds, not a claim that the gap coefficient 1/10 is
optimal. The exact Heawood family has gap ceil(r/2) on 14r vertices.
Its grid analogue, planar extremal cases, and the optimal cubic gap bound
remain separate questions.

The [subsequent port-deficiency construction](CUBIC_STABILITY_PORTS.md)
gives two-connected cubic bipartite graphs on14+20kvertices with
SF_2=8+12k and beta_2=7+12k. They have positive gap and regular slack two,
and their SF_2/n ratio approaches3/5. Thus the positive-gap endpoint
exclusion does not imply any uniformly smaller order coefficient. They
attain, but do not prove, the general stability candidate7SF_2<=3n+2beta_2.

## A sharp comparison with upper domination

For every nonempty d-regular bipartite graph, d>=1,

    Gamma(G)=alpha(G)=n/2 <= beta_2(G) <= SF_2(G)
        <= (2d/(2d-1)) Gamma(G).                              (8)

In particular, every cubic bipartite graph has SF_2<=6 Gamma/5.
The coefficient is attained by the two-connected ten-vertex d=3 sharp
example above. More generally the degree-d examples attain the coefficient
2d/(2d-1). This comparison concerns SF versus Gamma; the optimal SF-beta
gap remains a different question.

The identity Gamma=alpha for bipartite graphs is classical, not a new
contribution. For clarity, here is a direct argument. In a minimal
dominating set D, let I be its selected-isolated vertices. Every vertex h
in D minus I has a private outside neighbor x_h with N(x_h) intersect D={h}.
For bipartition L,R, the set

    I union ((D minus I) intersect L)
      union {x_h:h in (D minus I) intersect R}

is independent and has size |D|: the last two parts lie in L, and a
private neighbor is adjacent to no vertex of I. Thus Gamma<=alpha;
the reverse inequality follows from maximum independent sets being minimal
dominating. Finally, regular bipartite graphs have equal part sizes and
a perfect matching: Hall's inequality follows by counting the d edges
from every vertex of a chosen subset of one part. Consequently alpha=n/2.
The upper SF comparison in (8) now follows from (3).

## A rectangular-grid consequence, with its precise scope

For a rectangular grid P_m square P_l, m,l>=2, let b(S) be the sum over
selected vertices of 4-deg_G(v). Thus a selected corner contributes two
and any other selected boundary vertex contributes one. Formula (1), using
the degree upper bound four, gives

    7|S| + z <= 4ml + b(S) <= 4ml + 2m + 2l,
    SF_2(P_m square P_l) <= floor((4ml+2m+2l)/7).              (9)

The total degree deficiency of the grid is 2m+2l: its edge count is
2ml-m-l. The second inequality uses each boundary contribution only once.
The asymptotic coefficient here is 4/7 for the star-forming parameter.
It is not a new bound on psi_sq. In particular, (9) does not improve the
existing 5/6 sub-quorum bound without a proof of the separate bridge
psi_sq<=SF_2. Neither that bridge nor beta_2=SF_2 on all grids is proved here.

## Validation scope

The arguments above are general proofs. The
[independent controls](../scripts/check_regular_starforming.py) pass on
1,301 graphs and 262,106 selections, including all labeled graphs through
order five and all regular labeled graphs of order six. They compare
literal stars with the local test 1,672,201 times, check all-proper-subset
minimality, 10,708 failure-witness budgets, and 638 regular extremal sets,
including 540 triangle-free ones and 362 with nonempty H. Sixteen deterministic matching-union
samples, the Heawood graph and twelve rectangles through 4x4 are included.
Explicit witnesses check sharp
degree-one-through-eight examples. A separate cubic bipartite 20-vertex
example has an extremal 12-set consisting of a selected C6 with one leaf
at every vertex; the matching exchange produces a dissociation 12-set.
An additional nonbipartite cubic ten-vertex example has a selected triangle
with one leaf at each vertex and an outside triangle; it exercises the
all-regular extension with triangles inside H and X, and has beta_2=SF_2=6.
These are verification controls, not proofs of the general statements.

The pinned Lean4.33.0
[symbolic source](../formal/StarForming/RegularBound.lean) proves failure
witness existence and disjointness for arbitrary vertex types, the two
structural witness-degree restrictions, and conditional degree/regular/cubic
accounting, including the private-witness lemma for selected leaves that
removes the triangle-free restriction. Twelve audits pass with only
standard axioms. The finite graph
cardinal summation, full graph-level bound, equality partition, exchange and
grid corollary have written proofs; they are not claimed fully formalized.
The [formal receipt](../output/regular-bound-formal-check.json) and
[control receipt](../output/regular-bound-controls.json) record their scopes.
The [independent Oracle response](reviews/2026-10-19-regular-bound-oracle-response.txt)
accepted the original proof without a substantive gap and supplied the
all-regular equality strengthening above. Actual model gpt_6, effort pro;
task d19a25da-c2d8-4dfb-a646-0fd307a6a26b completed on its original stream.
It requested explicit definitions, possibly empty classes, and the detailed
leaf-witness locality argument; all are incorporated. The later Gamma/grid
corollaries and final verification inventory were outside that original input.

## Next question: can the gap be charged to half the defect?

For a cubic bipartite graph, let D=3n-5 SF_2(G). The theorem proves D>=0
and characterizes D=0. A stronger stability candidate is

    2(SF_2-beta_2) <= D,
    equivalently 7 SF_2 <= 3n+2 beta_2.                       (10)

This is **unproved**. If true, combining beta_2>=n/2 would yield the sharp
all-cubic-bipartite gap bound SF_2-beta_2<=n/14, attained by the Heawood
graph and its disjoint unions. Neither this gap bound nor (10) follows
from the endpoint characterization alone.

The [discovery script](../scripts/explore_cubic_stability.py) evaluates all
120 circulant parameter choices through20vertices and six choices on22
vertices, with exact beta and SF computed by subset evaluation. No candidate
counterexample occurred among those126instances; six have a strict gap.
Different parameters may give isomorphic or disconnected graphs. The
[exploration receipt](../output/cubic-stability-exploration.json) records
the graphs and witnesses. This finite evidence only motivates further
proof work and counterexample search; it does not establish (10).
