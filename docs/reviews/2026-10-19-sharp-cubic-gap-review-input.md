Please audit this proposed sharp theorem and its complete proof for finite simple cubic bipartite graphs. The key new point is to keep an adjacent high vertex and its failure witness together as a matching edge, omit only one bipartition side of selected isolates, and use unused leaf witnesses for the exact trimming budget. Check the dissociation construction vertex by vertex, witness overlap count, residual-capacity identity and sharpness. Give an explicit mathematical flaw or a precise acceptance; do not use finite testing as proof. This is a new stronger argument than an earlier pending audit of a weaker3n/34 bound; keep the questions distinct.

# Sharp compensation and gap bounds for cubic bipartite graphs

19 October 2026. A modified two-sided exchange proves the full stability
inequality, including selected isolates. It supersedes the weaker
unconditional bound in the earlier compensation note. The proof is general;
finite computations only check the construction and its accounting.

## Theorem

Let G be a finite simple cubic bipartite graph on n vertices. For every
inclusion-minimal two-star-forming set S of size s,

    7s <= 3n+2 beta_2(G).                                    (1)

Consequently

    7 SF_2(G) <= 3n+2 beta_2(G),
    SF_2(G)-beta_2(G) <= floor(n/14).                         (2)

The coefficient1/14 is sharp, attained by the Heawood graph and every
disjoint union of its copies. The linear inequality is also attained by
arbitrarily large two-connected cubic bipartite graphs from the earlier
port construction. The optimal asymptotic gap coefficient specifically
within the two-connected class is not determined here.

A two-star-forming set covers every outside vertex x by a non-induced
K_(1,2) on x and two selected vertices. Equivalently x has two selected
neighbors, or has a selected neighbor with a selected neighbor. Minimal
means inclusion-minimal, not minimum cardinality. SF_2 maximizes sizes of
minimal sets; beta_2 maximizes sizes inducing maximum degree at most one.

## Disjoint high witnesses and the residual capacity

Put T=V minus S and a(v)=|N(v) intersect S|. Partition S into selected
isolates I, vertices P in selected K2 components, selected leaves U
adjacent to a high selected vertex, and H={v in S:a(v)>=2}. Put z=|I|,
u=|U|, and delta=3n-5s. Vertices in H have selected degree two or three.

Each v in H has an outside failure witness: deleting v leaves v itself
covered by its two selected neighbors, so minimality forces an old outside
vertex to lose coverage. Failure-witness sets of distinct high vertices
are disjoint. Otherwise every old star covering a common witness x would
contain both high vertices v,w. At least one, say v, is adjacent to x;
a selected neighbor of v other than w gives a covering star avoiding w,
a contradiction. Choose an injective high witness map f:H->T.

Every witness has selected degree one or two, since three selected
neighbors would preserve a centered star after a single deletion.

If f(v) is nonadjacent to v, it has exactly one selected neighbor u_v;
otherwise its selected-neighbor set would preserve a centered star.
Coverage before deletion and failure afterwards force u_v to have v
as its sole selected neighbor. Thus u_v belongs to U, and f(v) and v
lie in the same bipartition part.

If f(v) is adjacent to v, then a(v)=2, since there is also the outside
edge. A selected degree-one witness has v as its only selected neighbor.
A selected degree-two witness has selected neighbors v and some w in I.
Indeed, failure after deletion implies w has no remaining selected
neighbor. Either w was isolated or its sole selected neighbor was v;
the latter creates a triangle v--w--f(v), impossible in a bipartite graph.

Call a high vertex good if its chosen witness is nonadjacent, and bad
otherwise. Write g for the number of good vertices. Every good vertex
has at least one selected leaf, and distinct high vertices cannot share
a selected leaf. Therefore u>=g.

Let r1,r2 count the vertices outside f(H) of selected degrees one and
two. The regular degree-capacity accounting gives

    delta >= z+2r1+r2.                                     (3)

For completeness, let q,h count the selected degree-two and degree-three
vertices. Counting the cut gives

    delta=z+sum_(x in T)(3-a(x))-(q+2h).

Each high vertex needs a(v)-1 units, and its injectively chosen witness
pays at least this amount. For a nonadjacent witness the capacity is
two; for an adjacent one, the high selected degree is two and the
capacity is at least one. Thus the used witness capacities pay q+2h,
and unused vertices supply exactly2r1+r2. This proves (3). All capacities
refer to distinct actual outside vertices.

## The leaf deficit is paid by unused witnesses

Each selected leaf u has an adjacent outside failure witness ell(u).
The deleted leaf itself remains covered through its high support. An old
outside nonneighbor cannot fail: a destroyed star using u as a leaf at
that high support can replace u by another selected neighbor. Thus an
outside neighbor must fail.

Its selected neighborhood is either {u} or {u,w} with w in I. Three
selected neighbors would preserve coverage. In the two-neighbor case,
w must have no selected neighbor after deleting u. It could not have
u as its sole selected neighbor: that would make w the high support of
u, which retains another selected neighbor. Therefore w was isolated.

These leaf witnesses are distinct: a witness with one selected neighbor
identifies its leaf, and a witness with two selected neighbors has exactly
one leaf and one isolate. No degree-two leaf witness belongs to f(H):
adjacent high witnesses have a high selected neighbor and nonadjacent
high witnesses have selected degree one. A degree-one leaf witness used
by f can be the witness of only a good high vertex, its leaf's unique
support. At most g leaf witnesses are therefore used high witnesses;
the others occupy the r1+r2 unused outside vertices. Hence

    u<=g+r1+r2,
    K:=u-g satisfies 0<=K<=r1+r2.                           (4)

The overlap between the two witness maps is explicitly subtracted before
the residual capacity is used. No leaf demand reuses a chosen high witness.

## The corrected exchange

Let L,R be the bipartition. To construct D_L, start with

    P union U union (I intersect R) union (H intersect L)
      union {f(v):v in H and f(v) in R}.

Then trim leaves at every kept high vertex v in L. If v is good, retain
exactly one of its selected leaves. If v is bad, remove all its selected
leaves: its chosen adjacent witness in R will be its selected partner.
The trimming sets are disjoint, because a selected leaf has one high
support. Define D_R by reversing the two sides.

Both sets induce maximum degree at most one:

- A kept good high vertex has its one retained selected leaf; all other
  selected high vertices are in its own bipartition part. Every added
  witness has only its stated leaf or its own bad high owner as a
  non-isolated selected neighbor, so it cannot create an edge to this
  good high vertex.
- A kept bad high vertex has no retained selected leaf and is paired
  with its adjacent chosen witness. A degree-two such witness loses its
  other selected neighbor, an isolate in L, because only I intersect R
  was retained. No other chosen witness can meet this high vertex.
- A chosen nonadjacent witness in R has one selected leaf, whose high
  support lies in R and was omitted. No leaf is paired with two chosen
  witnesses, since its support is unique and f is a function. These leaves
  are not trimmed, because trimming occurs at supports in L.
- All added outside witnesses lie in R and are mutually nonadjacent.
  Each has precisely its stated selected partner. Remaining U vertices
  are either paired once or isolated. P keeps only its matching mates,
  and retained isolates in R have no selected neighbor.

Here the adjacent high vertex and its witness are kept together as a
matching edge. The earlier exchange omitted that opportunity and charged
up to three high failures against a single selected isolate. Keeping only
one isolate side removes that obstruction without charging it repeatedly.

Across both exchanges the total number of trimmed leaves is

    sum_(good v)(c(v)-1)+sum_(bad v)c(v)=u-g=K,

where c(v) counts the selected leaves at v. Every vertex of P and U is
initially counted twice, every isolate once, every high vertex once,
and every chosen witness once. Since |f(H)|=|H|,

    |D_L|+|D_R|=2s-z-K.                                    (5)

Since beta_2 is at least each constructed size, (3)--(5) give

    2(s-beta_2)<=z+K<=z+r1+r2<=delta.

Substitute delta=3n-5s to obtain (1). Notice that the only isolate cost
is z across the two exchanges; there is no asserted injection of three
incident failure witnesses into one isolate vertex.

## Consequences and sharpness

Apply (1) to a maximum-size minimal selection to obtain the first part
of (2). Every cubic bipartite graph has equally sized parts, hence
beta_2>=n/2. For gap=SF_2-beta_2, inequality (1) yields

    5 beta_2+7gap<=3n,
    14gap<=n.

The [Fano-plane proof](CUBIC_STAR_FORMING_GAPS.md) gives the Heawood graph
with n=14, SF_2=8 and beta_2=7, attaining both inequalities. Additivity
under disjoint unions gives every integer gap r with n=14r and equality.
The earlier two-connected cubic bipartite G_k family has n=14+20k,
SF_2=8+12k and beta_2=7+12k; it attains the linear inequality for every
k>=1. The exact connected F_r family still supplies unbounded gaps
under two-connectivity, but the sharp gap coefficient for that subclass
is a separate question.

The proof settles the all-cubic-bipartite stability candidate, not the
grid equality problem. The separate psi_sq<=SF_2 bridge and any claimed
improvement of the5/6grid bound remain unproved here.

## Verification scope

The independent compensation checker retains the earlier exchanges and
also constructs and tests these corrected exchanges on every controlled
minimal set. In particular the two Heawood exchanges now have size seven
each, replacing the older sizes five. General validity is proved above,
not inferred from those controls. Formal and Oracle scope is recorded
in the companion receipts; no acceptance or full Lean graph formalization
is presumed before those checks complete.
