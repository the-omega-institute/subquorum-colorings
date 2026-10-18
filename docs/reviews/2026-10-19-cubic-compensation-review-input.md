Audit the following proposed general compensation theorem and its full proof for finite simple cubic bipartite graphs. Check every classification, cardinality and claimed non-reuse of witnesses. Return a precise acceptance or a mathematical flaw; if valid, identify any stronger consequence already justified by this proof. Do not treat finite experiments as proof. Definitions: a two-star-forming selection covers each outside vertex by a non-induced K_1,2 on it and two selected vertices. Equivalently it has two selected neighbors or a selected neighbor with a selected neighbor. Minimal means inclusion-minimal. beta is maximum size inducing maximum degree at most one; SF maximizes sizes of minimal forming sets.

For completeness, the earlier generic witness fact used below has this proof: a high selected vertex v (at least two selected neighbors) is itself covered after deletion, hence minimality provides an old outside failure witness. If one outside x witnessed two distinct high v,w, every old covering star would contain both; in a three-vertex star on x,v,w, at least one of v,w, say v, is adjacent to x. A second selected neighbor of v different from w gives a covering star avoiding w, contradiction. Thus the failure sets are disjoint. A witness cannot have three selected neighbors; a nonadjacent witness must have exactly one selected neighbor, a selected leaf supported only by the deleted high vertex. The exact regular slack identity follows by adding the cut identity to the sum of capacity minus high demand; its specialized version is rederived below.

# Cubic bipartite compensation and the isolated-vertex residual

19 October 2026. The sharp candidate7SF_2<=3n+2beta_2remains open in
general. This note proves it whenever a maximum minimal star-forming set
has no selected-isolated vertices, and proves a weaker unconditional
stability inequality and a gap bound3n/34for all cubic bipartite graphs.
The arguments are general; finite controls only check them.

## Statement

Let G be a finite simple cubic bipartite graph on n vertices, S any
inclusion-minimal two-star-forming set, s=|S|, z the number of vertices
isolated in G[S], and delta=3n-5s. Let beta=beta_2(G). Then

    2(s-beta) <= delta+2z <= 3delta.                          (1)

In particular, choosing a maximum-cardinality minimal set gives

    17SF_2 <= 9n+2beta_2,
    SF_2-beta_2 <= floor(3n/34).                              (2)

If some maximum-cardinality minimal set has z=0, then

    7SF_2 <= 3n+2beta_2.                                     (3)

The coefficient3/34in (2) is an improved universal upper bound relative
to the earlier n/10consequence of the regular order bound; it is not
claimed sharp. The unrestricted candidate (3), which would yield n/14,
is not settled here. These are bounds on SF_2, not sub-quorum improvements.

## Failure witnesses and exact slack

Write T=V(G) minus S and a(v)=|N(v) intersect S|. Let I be the selected
isolates, U the selected leaves adjacent to a selected vertex of degree
at least two, P the vertices in selected K2 components, and
H={v in S:a(v)>=2}. They partition S into I,U,P,H. For v in H write
c(v)=|N(v) intersect U| and put

    E=sum_(v in H) max(c(v)-1,0).

The [degree-capacity theorem](REGULAR_STAR_FORMING_BOUND.md) proves that
each v in H has an outside failure witness f(v), that witnesses for
different high vertices are disjoint, and that f can be chosen injective.
A failure witness is covered before v is deleted but not afterwards.
It has one or two selected neighbors. If f(v) is nonadjacent to v,
it has a unique selected neighbor u, which is a selected leaf supported
by v. Indeed, a center with two selected neighbors would survive; for
the remaining leaf-star to fail, u must have v as its sole selected
neighbor. In particular c(v)>=1 in this case, and f(v) and v lie in
the same bipartition part.

If f(v) is adjacent to v, then a(v)=2, since the degree is three.
If a(f(v))=2, its other selected neighbor w is in I. Otherwise w has a
selected neighbor remaining after deletion, or w has v as that neighbor.
The first case preserves coverage and the second makes a triangle with
f(v), impossible in a bipartite graph.

Partition H into A,B,C,H3 as follows:

- A: selected degree two, adjacent witness with a(f(v))=1.
- B: selected degree two, adjacent witness with a(f(v))=2.
- C: selected degree two, nonadjacent witness.
- H3: selected degree three; its witness is necessarily nonadjacent.

Use A,B,C also for their cardinalities when they occur in arithmetic.
Let r1 and r2 count unused outside vertices of selected degree one and
two, respectively, where unused means outside f(H). The exact regular
slack identity is

    delta = z+A+C+2r1+r2.                                   (4)

To verify it, a high vertex of selected degree two needs one unit of
capacity. A witness of selected degree one has capacity two and leaves
one unit unused; a witness of selected degree two has capacity one
and leaves zero. A selected degree-three vertex needs two units and
its nonadjacent witness has capacity two. Outside vertices not used
by f contribute their full capacities. This is also obtained by adding
the cut identity, as in the preceding general proof. Thus z<=delta.

## The leaf budget uses disjoint resources

Every u in U has an outside failure witness g(u) adjacent to u. The
newly omitted u is covered through its high support, so some old outside
vertex must fail. A nonneighbor of u cannot fail: any affected star
uses u as a leaf at its high support, which can replace u by another
selected neighbor. Hence g(u) is adjacent to u. It has either just u
as a selected neighbor, or exactly u and an isolated selected vertex.
For the second assertion, if the other selected neighbor w had a
selected neighbor after deletion, coverage would persist. If w had u
as its only selected neighbor, u's unique support would be w, which is
high and therefore retains another selected neighbor. Both are impossible.

The g(u) are distinct: a degree-one witness identifies u, while a
degree-two witness has one leaf neighbor and one isolate neighbor and
therefore also identifies u. Write g2 for the number with selected degree
two. Such witnesses cannot belong to f(H), since adjacent high witnesses
have a high selected neighbor and nonadjacent high witnesses have
selected degree one. Thus g2<=r2.

Among the selected degree-one leaf witnesses g(u), at most |C|+|H3|
belong to f(H). Each remaining such witness is counted in r1. Hence

    |U|-(|C|+|H3|) <= r1+g2.

Every vertex of C union H3 has at least one leaf, so
E<=|U|-(|C|+|H3|). Consequently

    E <= r1+g2.                                             (5)

Each chosen witness of a B vertex has an isolated selected neighbor.
The B witnesses and the g2 witnesses are disjoint outside vertices,
so their incidences to I use distinct edges. Every vertex of I has
degree three. Therefore

    B+g2 <= 3z.                                             (6)

Equations (5),(6) charge the same resource only once: a chosen high
witness is excluded from r1,r2, a leaf witness shared with that choice
is removed before counting the residual leaf demand, and the isolate
incidences for B and g2 are disjoint. In particular,

    A+B+E <= A+3z+r1 <= delta+2z,                            (7)

where the last step uses (4) and nonnegativity of C,r1,r2.

## Two explicit dissociation exchanges

Let L,R be the bipartition and call C union H3 the good high vertices.
Construct D_L by starting with all of I union U union P, keeping all
high vertices in L, and adding f(v) for good high vertices v in R.
For each high vertex kept in L with c(v)>1, retain exactly one of its
U neighbors and remove the other c(v)-1 leaves. These leaf removals
are disjoint because a selected leaf has a unique high support. Define
D_R with the two parts reversed.

Both sets are dissociation sets. Kept high vertices lie in one part
and have at most one retained leaf each. Added witnesses lie entirely
in the opposite part and have precisely one original selected neighbor,
their associated leaf. That leaf's high support has been omitted, and
no leaf belongs to two added witnesses: a degree-one leaf witness can
fail on deleting only that leaf's unique high support, and f is a
function. None of these leaves is removed in the trimming step, since
its support lies in the omitted part. The added vertices are mutually
nonadjacent; their unique selected neighbors also rule out edges to
the kept high vertices, I or P. Each vertex of P keeps only its mate,
and selected isolates have no new neighbors. Thus every selected
vertex in D_L or D_R has selected degree at most one.

The cardinalities are exact:

    |D_L|=s-|(A union B) intersect R|
             -sum_(v in H intersect L)max(c(v)-1,0),
    |D_R|=s-|(A union B) intersect L|
             -sum_(v in H intersect R)max(c(v)-1,0).

Their sum is2s-A-B-E. Since beta is at least each size,

    2(s-beta)<=A+B+E.                                       (8)

Combining (7),(8) proves the first inequality in (1); z<=delta proves
the second. This establishes a general cross-component inequality with
explicit dissociation sets, without assigning one outside witness twice.

## Parameter consequences

Apply (1) to an attaining S. Substituting delta=3n-5s into
2(s-beta)<=3delta gives17s<=9n+2beta. Regular bipartite graphs have
balanced parts, so beta>=n/2. With gap=s-beta this gives

    2gap <= 9n-15s <= 9n-15(gap+n/2),
    34gap <= 3n.

If an attaining set has z=0, the first inequality in (1) instead gives
7s<=3n+2beta, proving (3) under that explicit structural hypothesis.
The general remaining difficulty is the isolate-incidence budget (6):
up to three different high failures can use the edges at one isolate.
Replacing3zby z is false even in the Heawood example. A proof of the
unrestricted candidate must improve the exchange or track those joint
configurations; it cannot assert that (6) has an injective map to I.

## Validation scope

The proofs above do not use enumeration. The checker, formal sources and
review receipt accompanying this note state their exact coverage separately.
Full finite cardinal summation and the complete graph-level theorem are
written proofs, not claimed as fully formalized in Lean.
