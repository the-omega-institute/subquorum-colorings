# Square attachments and exact star-forming compositions

Let B be any finite simple graph and let E_0 be a matching of k edges
d_i e_i. For each edge add two new vertices a_i,b_i and the path
d_i-a_i-b_i-e_i, retaining d_i e_i. Write G for this graph, D for the
2k old endpoints, and F=B-D. The added square is called an ear here.
No new vertex has any other neighbour.

We prove

    beta_2(G)=2k+beta_2(F),                                  (1)
    2k+SF_2(F)<=SF_2(G)<=2k+|V(F)|.                          (2)

Every minimal forming set uses exactly two vertices in each ear-square.
If E_0 is a perfect matching, all minimal forming sets are precisely
the independent choices of two vertices per square. There are 6^k of
them, all of size 2k, and beta_2=sf_2=SF_2=2k. The graph on the old
vertices is arbitrary; neither bipartiteness nor medianity is required.

Square attachments also preserve medianity. When the old graph is plane
and two-connected and the matching endpoints have degree at most three, the new graph remains plane and
two-connected and has maximum degree at most four if the old graph does.
Thus a strict SF_2/beta_2 gap in the punctured core F transfers to this
restricted class. This statement is a reduction, not an assertion that
such a punctured core has been found.

## 1. Definitions

A dissociation set induces maximum degree at most one; beta_2 is its
maximum size. A set S is forming by a non-induced K_(1,2) if every x
outside S has two neighbours in S or a neighbour in S with a neighbour
in S. A selected vertex is active if it has a selected neighbour.
The upper and lower star-forming numbers SF_2 and sf_2 are respectively
the largest and smallest sizes of inclusion-minimal forming sets.

Formation is upward closed. Consequently a forming set is minimal
exactly when deletion of every one of its vertices fails. The newly
deleted vertex is included in that test.

## 2. Exact local safe deletion

Fix an ear Q={d,e,a,b}, with cycle d-e-b-a-d. The only vertices of Q
with possible outside neighbours are d,e.

**Lemma 1.** A minimal forming set of G meets Q in exactly two vertices.

**Proof.** If there are fewer than two, some new vertex is unformed.
With no selection this is immediate. If d is the only selected vertex,
b has no selected neighbour; the case e is symmetric. If a alone is
selected, b has only the isolated selected neighbour a; the case b is
symmetric. Outside neighbours of the roots cannot change these failures.

If d,e,a are selected and b is omitted, delete a. The selected old edge
d-e remains active and forms both the newly omitted a and the omitted b.
The activity of every selected root is retained, so any outside vertex
whose old star used a as a leaf at d still has a star through e.
The case with d,e,b selected is symmetric.

If d,a,b are selected and e is omitted, delete b. The newly omitted b
is formed through the active edge a-d; e is formed through the same edge
using its old neighbour d. No selected root loses activity. The deleted
b has no neighbour outside Q, so all other outside stars remain. The
case with e,a,b selected is symmetric.

With all four vertices selected, delete a. It still has two selected
neighbours d,b, and the old edge d-e keeps the selected roots active.
No outside star is lost. Thus a minimal set cannot use three or four
vertices of Q. This proves the lemma. QED.

**Lemma 2.** Every two-set of Q forms Q. Each of its selected vertices
has a deletion witness among the new vertices which is unaffected by
arbitrary edges between old vertices.

The complete table lists the deleted vertex and its witness. A witness
may be reused for two alternative deletions; these are separate minimality
tests, not simultaneous allocations.

| Selected pair | First deletion / witness | Second deletion / witness |
| --- | --- | --- |
| d,e | d / a | e / b |
| a,b | a / a | b / b |
| d,a | d / b | a / b |
| e,b | e / a | b / a |
| d,b | d / a | b / b |
| e,a | e / b | a / a |

In each entry, after deletion the witness has no selected neighbour or
one isolated selected neighbour. All relevant vertices other than an
omitted root are new vertices of Q, so outside edges cannot rescue the
witness. The formation assertion follows directly from the square:
an omitted vertex either sees the two selected opposite vertices or is
adjacent to an endpoint of the selected edge. This proves the lemma.

## 3. Dissociation and star-forming formulas

Every dissociation set uses at most two vertices of a square, since any
three induce a two-edge path. The k ear-squares are vertex-disjoint,
and the remaining selected vertices lie in F. Hence beta_2(G) is at most
2k+beta_2(F). Choose all new pairs a_i,b_i together with a maximum
dissociation set of F. The roots are omitted, so these new pairs have
no selected neighbours in F or in other pairs. This attains (1).

Let S_F be any minimal forming set of F. Add all new pairs. Every old
root outside the resulting selection is formed through the active new
edge in its square. All remaining outside vertices retain their stars
in F. A deletion witness in F is unchanged: no root is selected and no
new selected vertex is adjacent to F. A new-vertex deletion has the self
witness in Lemma 2. Thus the resulting set is minimal forming, of size
2k+|S_F|. Taking a maximum S_F proves the lower bound in (2). Lemma 1
gives its upper bound. Subtracting (1) gives the general gap transfer

    SF_2(G)-beta_2(G)>=SF_2(F)-beta_2(F).                     (3)

If F is empty, Lemma 1 forces size 2k in every minimal forming set.
Conversely Lemma 2 proves that every independent choice of two vertices
per square is minimal forming in G. The choices are distinct and number
6^k. Formula (1) gives beta_2=2k. This includes k=0 and the empty graph.

For partial matchings the tempting identity SF_2(G)=2k+SF_2(F) is false,
with an unbounded additive error. The counterexample in Section 4 gives
exact values, including an upper proof and all deletion witnesses.

## 4. Exact obstruction to the partial-matching formula

Fix m>=5. Let T={t_1,...,t_m} and X={x_1,...,x_m} each induce a clique.
For every i add distinct roots d_i,e_i and exactly the edges

    d_i e_i, d_i t_i, d_i x_i.

There are no other base edges. Attach a square along each d_i e_i by
adding d_i-a_i-b_i-e_i. Thus k=m, |V(G)|=6m, and F is the disjoint union
of two K_m's. The exact values are

    SF_2(F)=beta_2(F)=4,
    beta_2(G)=2m+4,
    SF_2(G)=3m.                                           (5)

In a clique of order at least two, the minimal forming sets are exactly
the pairs: a singleton leaves each other vertex with its sole selected
neighbour inactive, and any pair forms. A dissociation set has at most
two vertices. The first equality follows componentwise, and (1) gives
the displayed value of beta_2(G).

For the SF lower bound select S=T union {d_i,b_i:1<=i<=m}. The omitted
a_i,e_i see both d_i and b_i. Each omitted x_i sees the active d_i,
whose selected neighbour is t_i. Hence S forms. All deletions fail:

| Deleted vertex | Unformed witness | Reason after deletion |
| --- | --- | --- |
| t_i | x_i | Its sole selected neighbour d_i has become inactive |
| d_i | a_i | Its sole selected neighbour b_i is inactive |
| b_i | b_i | Both a_i,e_i are omitted |

In particular all m vertices of T are indispensable. This proves
SF_2(G)>=3m by a complete minimality argument.

For the upper bound let R be any minimal forming set, p=|R intersect T|,
q=|R intersect X|. Lemma 1 gives |R|=2m+p+q. If p>=3 and q>=1, delete
any selected t_i. All outside square vertices remain locally formed by
their unchanged selected pairs. Every outside T vertex, including t_i,
has at least two selected T neighbours. Among selected vertices outside
T, only d_i could lose activity. This could affect only the outside
vertex x_i; if d_i is selected, x_i also sees a selected X vertex,
so it still has two selected neighbours. If d_i is omitted it cannot
cause a loss. Other outside X vertices retain formation, including the
activity of their selected X neighbours. The deletion is safe, a
contradiction. Thus p>=3 implies q=0. Symmetrically q>=3 implies p=0.
Either p+q<=m, or p,q<=2 and p+q<=4<=m. Consequently |R|<=3m,
proving (5) for every m>=5.

The proposed exact addition therefore underestimates SF_2(G) by m-4.
For m=5 this is a 30-vertex counterexample with SF_2=15 and beta_2=14.
It uses cliques and is not offered as a bipartite, planar, or median
counterexample. The mechanism is external activity: the opposite pair
{d_i,b_i} forms its square, but selected d_i depends on t_i to become
active. This creates a deletion witness at x_i which does not exist
in F. Indeed S intersect F=T does not form the second clique. The
valid dissociation identity, local cap, and inequalities (1)--(3)
survive unchanged.

## 5. Medianity, planarity and two-connectivity

**Lemma 3.** Adding one square along an edge of a median graph preserves
medianity.

**Proof.** The new graph is the induced subgraph of B square K_2 on

    (V(B) times {0}) union ({d,e} times {1}).

The two new vertices are (d,1),(e,1). This subgraph is isometric in the
product. Distances between old vertices are unchanged; from an old x
to a new d they are dist_B(x,d)+1, attained through (d,0); the two new
vertices are adjacent. Cartesian-product distance is additive, so the
product is median with coordinatewise median.

The subset is closed under that median. If its median has second
coordinate one, at least two inputs are new vertices. If their first
coordinates differ, they are d,e and the first-coordinate median lies
in I_B(d,e)={d,e}. If they agree, it is that common coordinate. In
either case the median belongs to the subset. An isometric median-closed
subset inherits the unique interval median. This proves the lemma.
Apply it successively for all ears. QED.

For a plane two-connected B, the matching edges have disjoint endpoints.
Draw each new path in a small strip along one side of its old edge, inside
an incident face. Because the edges and endpoints are disjoint, the strips
can be chosen disjoint. This works for interior as well as outer-face
edges and gives a plane drawing. To check two-connectivity, delete a vertex. If it was old, the
remaining old graph is connected and every surviving ear path has a
surviving attachment endpoint. If it was new, the old graph remains
connected and the remainder of its ear attaches to its other endpoint.
All other ears attach as before. Thus no vertex deletion disconnects G.

Each old root gains exactly one neighbour, every other old degree is
unchanged, and new degrees are two. Hence roots of degree at most three
preserve the maximum-degree-four bound. These arguments establish all
the claimed structural properties, without treating finite samples as
the proof.

## 6. A degree-four median family beyond adjacent involutions

Let n>=4 be even. In the ladder with vertices (i,j), i in {0,1},
0<=j<n, attach a square along each row edge (i,2j)(i,2j+1).
These n edges form a perfect matching of the old graph. The resulting
graph has 4n vertices, is two-connected, outerplanar, median, and has
maximum degree four by Section 5. Section 3 classifies all its 6^n
minimal forming sets, all of size 2n; beta_2=sf_2=SF_2=2n.
For outerplanarity, draw every ear outward along its old row edge;
its new three-edge path replaces that edge on the outer boundary.

This family has no automorphism sending every vertex to a neighbour.
The two new vertices a,b of a square attached to a corner row edge have
degree two, while their respective old neighbours have degrees three
and four. Such an automorphism must send a to b, its only degree-two
neighbour, and b to a. The edge from a to its old neighbour then forces
the degree-three old neighbour to map to the degree-four one, impossible.
Thus the equality and full minimal-set classification here are not
consequences of the adjacent-involution criterion.

For n=4r, a separate [four-parameter proof](EAR_LADDER_FOUR_PARAMETERS.md)
determines psi_sq=Omega=9r while beta_2=sf_2=SF_2=8r. Thus this class
also shows why the established SF/dissociation equality alone cannot
settle the grid's separate sub-quorum comparison.

## 7. Pendant paths and a companion exact class

Another shielding operation attaches d-a_d-b_d at each vertex d of an
arbitrary set D of old vertices. Put F=B-D. The disjoint triples are
P_3's, each of dissociation capacity two. Selecting all a_d,b_d gives

    beta_2(G)=2|D|+beta_2(F),
    2|D|+SF_2(F)<=SF_2(G)<=2|D|+|V(F)|.                     (4)

For the local cap, a forming set must select at least two vertices in
each triple: d alone leaves b with no selected neighbour; a alone
leaves b adjacent to the isolated a; b alone leaves a adjacent to the
isolated b. If all three are selected, delete b. Vertex b is then formed
through a-d, root d remains active through a, and b has no other outside
neighbour. Thus every minimal set has exactly two per triple. Each of
the three pairs is locally forming and has a new-vertex deletion witness,
independent of outside root edges. These facts give (4) by the same
disjoint-capacity and minimality-lifting proof as above.

If D=V(B), every two-per-triple choice is minimal forming. There are
3^|V(B)| such sets and beta_2=sf_2=SF_2=2|V(B)|. Attaching paths preserves
medianity and planarity but introduces cut vertices. The square operation
provides the corresponding two-connectivity-preserving construction.

The partial-root identity SF_2(G)=2|D|+SF_2(B-D) also fails. In Section 4,
omit e_i and the two edges incident with it in each square, leaving the
pendant path d_i-a_i-b_i. The same selection T union {d_i,b_i} forms,
and exactly the same three deletion witnesses apply. The upper argument
only used the local cap, local formation of every pair, and the neighbours
of d_i in T union X. All remain valid. Hence this 5m-vertex graph has
beta_2=2m+4 and SF_2=3m for every m>=5, again an additive discrepancy m-4.

## 8. Verification and remaining question

The standalone checker `scripts/check_square_ear_composition.py` uses
literal formation, dissociation and single-deletion tests on small
graphs. It compares the exact beta formula and star-forming bounds,
checks every local cap, classifies every minimal set in the fully
covered cases, and checks the structural constructions and explicit
witnesses at larger sizes. It also checks the counterexample's entire
deletion table and an attaining dissociation set at several sizes.
A separate C++ checker exhausts all square-pair choices and all residual
selections for m=5, without using the upper-bound classification.
General results have the proofs above.

The two-connected planar median maximum-degree-four equality question
remains a separate research question. Finite corner-deletion, cube-chain
and boundary-ear searches have found no strict-gap punctured core, but
do not prove equality. No new Lean execution or historical priority claim
is made. Independent review scope is recorded with the final package.
