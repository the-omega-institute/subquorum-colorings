# Local stability of upper two-star-forming sets

For every finite simple graph G, write SF_2(G) for the largest size of
an inclusion-minimal two-star-forming set. We prove that deleting a
bounded interface changes SF_2 by a bounded local error. This gives a
general composition estimate and shows that the unbounded single-ear
errors in the preceding constructions require growing degrees.

For U subset V(G), put H=G-U and

    B_r(U)={x in V(G): dist_G(x,U)<=r},
    b_r(U)=|B_r(U) minus U|.

Thus B_r includes U; B_r(empty)=empty, and vertices in different
components have infinite distance. All distances below are in G.

**Theorem 1 (deleting an interface).** For arbitrary U,

    SF_2(H)-b_3(U) <= SF_2(G)
                      <= SF_2(H)+|U|+b_5(U).               (1)

More precisely, if S is any minimal forming set of G, let

    S_H=S minus U,
    A={x in V(H) minus S_H: x is not formed by S_H in H}.

Then A subset B_2(U), S_H union A forms H, and every minimal forming
subset of S_H union A contains

    S_H minus (B_2(U) union B_3(A)).                        (2)

Consequently

    |S| <= SF_2(H)+|S intersect U|
            +|S_H intersect (B_2(U) union B_3(A))|.        (3)

In particular the rightmost loss in (3) is confined to B_5(U).
The locality radii three for adding selections and five for this
canonical deletion repair are attained on a nine-vertex path. These
are sharp radii for the certificate-preservation statements, not claims
that the numerical error bounds in (1) are optimal.

## 1. Formation and protected deletion witnesses

A selected set S forms x outside S if G[S union {x}] contains a
not-necessarily-induced K_(1,2) containing x. Equivalently x has two
selected neighbours, or a selected neighbour with a selected neighbour.
A selected vertex with a selected neighbour is active. Formation is
upward closed. A forming set is inclusion-minimal if and only if each
single deletion fails, including at the newly omitted vertex.

If v in S is essential, choose an unformed vertex x after deleting v.
Either x=v, or x was outside S and was formed before the deletion.
In the latter case each former forming star at x contains v, so

    dist_G(v,x)<=2.                                       (4)

**Lemma 2 (adding selections).** Let A be disjoint from S. For a deletion
witness x as above, if x ceases to be a witness after replacing S-{v}
by (S union A)-{v}, then dist_G(v,A)<=3. In particular every old
selection at distance greater than three from A remains essential.
The proof requires formation before deletion only at x, rather than
at all vertices outside S.

*Proof.* If x=v becomes formed, its new forming star contains a vertex
of A, giving distance at most two from v. If x belongs to A, (4) gives
the same conclusion. Suppose x remains outside S union A. It has an
old forming star on {x,v,w}, for some w in S-{v}, and a new forming
star using A. If v is adjacent to x, every new star places an A vertex
at distance at most two from x, giving distance at most three from v.
If a new forming star has an A vertex adjacent to x, (4) gives the
same bound.

The only remaining case is that v is not adjacent to x and no A vertex
of the new star is adjacent to x. The old star must have centre w,
with edges xw,wv. The new star must have a centre t in S-{v} adjacent
to x and to an A vertex a. If t differs from w, then x already has the
two selected neighbours t,w after deleting v, contradicting its failure.
If t=w, the path v-w-a has length two. This exhausts the possibilities.
The argument also covers triangles, since stars need not be induced.
No bipartiteness assumption is used. Square.

## 2. Proof of the interface theorem

For an outside vertex x of H that is unformed by S_H, an original
forming star at x cannot have both its selected vertices in H. It
therefore contains a selected vertex of U, so x is within distance two
of U. This proves A subset B_2(U). Selecting every vertex of A repairs
formation: previously formed outside vertices remain formed by upward
closure, and the previously unformed vertices are now selected.

Take v in the set (2), and an original deletion witness x for v in G.
If x differs from v, (4) holds. Since v is outside B_2(U), x does not
belong to U. Since v is outside B_3(A), Lemma 2 says that x remains
unformed after adding A and deleting v in G. Removing U cannot create
a forming star at a surviving outside vertex. Thus x is still unformed
in H by (S_H union A)-{v}. The same argument applies when x=v.
So v is essential even in the enlarged repaired selection.

Any forming subset of S_H union A must contain every such v: otherwise
it would be contained in the nonforming set obtained by deleting v,
contrary to upward closure. A minimal forming subset exists because the
graph is finite. Its cardinality is at least that of (2), proving (3).
Every vertex in B_3(A) is in B_5(U), and B_2(U) subset B_5(U), so (3)
implies the upper bound in (1).

For the lower bound, take a maximum minimal forming set T of H. The
set T union U forms G, since all new vertices are selected and each
old outside vertex retains its old star. If v in T is outside B_3(U),
its old witness x lies in H. Lemma 2, applied to that witness with
added set U, shows that it remains a witness in G. Its proof applies
although T alone need not form all of G: formation of the old outside
witness in H is all that the proof uses. Hence every forming subset
of T union U contains T minus B_3(U). Extracting a minimal one proves
SF_2(G)>=|T|-b_3(U), as asserted. Empty graphs, isolated vertices and
U=empty satisfy the same proof.

## 3. A sharp path example for the locality radii

Let G=P_9 on vertices 0,1,...,8, with consecutive edges, and select

    S={0,1,4,5,6,8}.

It forms. The deletion failures are:

| Deleted vertex | An unformed vertex |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 4 | 3 |
| 5 | 3 |
| 6 | 7 |
| 8 | 8 |

Thus S is minimal. Adding A={2} makes vertex5 deletable: its own two
neighbours4,6 stay selected; vertex3 gains selected2 in addition to4;
vertex7 retains selected6,8. The remaining outside vertices are formed.
Since dist(5,2)=3, distance three in Lemma 2 cannot be replaced by two.

Now delete U={0}. The restricted set S_H is unformed exactly at2,
so the canonical repair set in Theorem1 is A={2}. Vertex5 is again
deletable after repair, and dist(5,U)=5. A forming subset omitting5
therefore exists, and can be minimized without reintroducing5. Thus
one cannot guarantee preservation of every original selected vertex at
distance five in this repair procedure. The theorem guarantees those
at distance strictly greater than five. This example has maximum degree
two and is bipartite. It does not assert sharpness of the SF difference.

## 4. General bounded-interface composition

Suppose deleting U from G leaves components F_1,...,F_r. Formation and
inclusion-minimality separate over disjoint components, so

    SF_2(G-U)=sum_i SF_2(F_i).

Theorem1 therefore gives

    sum_i SF_2(F_i)-b_3(U) <= SF_2(G)
           <= sum_i SF_2(F_i)+|U|+b_5(U).                  (5)

Each affected vertex is counted in the union B_r(U) once. Intersecting
balls are not independently allocated to several components. No
minimality of an arbitrary restriction to a component is assumed.

If G has maximum degree Delta>=1, a breadth-first count gives

    b_r(U)<=|U| Delta sum_(j=0)^(r-1) (Delta-1)^j.        (6)

At distance one there are at most |U|Delta vertices; at later layers
each vertex has a predecessor, leaving at most Delta-1 forward edges.
Overlaps only reduce the count. At Delta=1 the sum is interpreted
literally, with (Delta-1)^0=1. At Delta=0, b_r(U)=0.
Thus a fixed interface size and fixed maximum degree yield an error
bound independent of the sizes of the components.

## 5. Square ears: the bounded-degree answer

Let B be a finite simple base, E_0 a matching of k base edges, R its
2k endpoints, and F=B-R. Attach a square along each matched edge by
adding two new internal vertices, producing G. The square-ear theorem
gives exactly two selected vertices in each square in any minimal
forming set, and gives the lower bound 2k+SF_2(F).

Apply (3) after deleting the union U of all four-vertex squares.
The residual is exactly F, |S intersect U|=2k, and distances from F
to U equal distances in B to R. Indeed a route into a new interior
vertex first meets an old root, and the square's new three-edge route
between its roots does not shorten the existing base edge. Hence

    0 <= SF_2(G)-(2k+SF_2(F))
          <= |{x in V(F):dist_B(x,R)<=5}|.                (7)

If Delta is the maximum degree of the final graph G and k>0, then
Delta>=2. Each root has its matched root neighbour and one new interior
neighbour, leaving at most Delta-2 neighbours in F. A simultaneous
breadth-first count from all roots therefore gives

    SF_2(G)-(2k+SF_2(F))
       <=2k(Delta-2) sum_(j=0)^4 (Delta-1)^j.             (8)

At Delta=2 the right side is zero and the formula is exact. At k=0 it
is exact by G=F. If instead delta is a bound for the maximum degree of
the base B, the analogous bound is 2k sum_(j=1)^5 (delta-1)^j for
delta>=1. These are explicit valid bounds, not claimed optimal constants.

In particular no family of fixed maximum degree and fixed ear count
can have unbounded error. The preceding connected bipartite examples
with one ear and unbounded error are consistent with (8): their root
degrees grow. This settles that bounded-degree existence question while
leaving the best dependence on Delta and stronger connectivity open.

## 6. Verification and provenance

The proof is general. The independent literal checker
`scripts/check_local_star_stability.cpp` checks formation, minimality,
induced deletions, added selections and all sharp-path certificates.
It does not use the theorem to compute SF_2. It independently compares the activity predicate with literal three-vertex
star enumeration. Controls cover all1,100 labelled graphs of orders0 to5,
96 seeded graphs of orders6 to9, the P9 witness, and an additional claw
regression. It computes973,858 induced-selection states and157,822
minimal sets, tests85,850 addition pairs and669,163 interface repairs,
and checks57,419 exact parameter comparisons. The329 square-ear models
use28,015 literal subsets. These are finite implementation controls;
the universal conclusions use the proofs above.

The research-stage answer included a false minimum over all minimal
sets in one displayed strengthening. The claw K_(1,3), with all vertices
deleted, refutes it: SF=3 but the smallest minimal forming set has size2.
The final statement (3) is for each fixed S; SF(G) on the left requires
an SF-maximizing S. The report includes that exact regression. Complete
provenance is in `output/local-star-research.json`. A separate final
independent review is recorded in `output/local-star-stability-review.json`;
it must not be inferred from the research response.

The local perturbation question was posed to Oracle after the preceding
ear obstruction. The final proof and checker are reconstructed locally;
research-stage suggestions and independent final review have separate
records. No Lean verification or historical priority claim is made.
