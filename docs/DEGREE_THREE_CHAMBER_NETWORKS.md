# Straight chamber networks and localization of geometric junctions

20 October 2026. This is a structural reduction for arbitrary endpoint
components, rather than a prescribed drawing. It separates the degree-three
case from the junctions created by degree-four endpoints. The whole-receiver
ceiling and its compensation coverage remain open. Submitted manuscripts are
unchanged.

## 1. Setting and square chambers

Let (T,M) be feasible on a finite rectangular nearest-neighbor grid. Write
P=V(M), A=T union P; every T has at most one neighbor in A. Assume single
terminality, namely deg_A(p)>=3 for every p in P. Outside the rectangle
vertices are blank. A P-face is any unit square with all four corners in P;
it need not align with the physical disjoint 2-by-2 tiling.

Join two P-faces when they share an edge. A square chamber is a connected
component of this face adjacency graph, together with all its corner
vertices. A straight chamber has vertex set a full 2-by-w rectangle, w>=2,
possibly rotated. Chambers here are maximal face components, not the
maximal full-column intervals used only for thin components in
THIN_COMPONENT_CLASSIFICATION_AND_BOUND.md.

We use the established local turn/branch lemmas from
SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md: a terminal P vertex with at least
three P neighbors lies in a P-face; a vertex with exactly two perpendicular
P neighbors also lies in a P-face. Those local lemmas and the promotion
cycle criterion are prior ingredients, not new claims of this note.

## 2. General geometry when endpoint degree is at most three

**Straight-chamber network theorem.** Suppose deg_P(p)<=3 for every p in P.
Then:

1. Every square chamber is straight, and distinct chambers have disjoint
   vertex sets.
2. Every component of P after deleting all chamber vertices is a straight
   finite path, allowing a single vertex. Each such path meets at most two
   chamber vertices, one through each end; its contacts and the path are
   collinear whenever there is an internal path vertex at that end.
3. Every connection to a chamber uses a corner of its 2-by-w rectangle.
   Each corner has at most one external P neighbor. Direct edges between
   two different chambers are also allowed; the theorem does not require
   a positive number of intervening path vertices.

Proof. If a P-face has neighbors on two perpendicular sides, the corner
at which those sides meet has all four grid neighbors in P. This contradicts
the degree bound. Consequently the face adjacency graph has degree at most
two, and a degree-two face has its neighbors on opposite sides. Every
connected finite component is therefore a consecutive horizontal or vertical
strip of faces, with vertex set exactly a 2-by-w rectangle. A cycle cannot
occur, since the direction could never turn. Two faces in distinct strips
cannot share a corner: they would meet diagonally, giving that shared
vertex all four P neighbors. Sharing an edge would instead put them in
the same chamber. This proves the first assertion.

Let U be the P vertices on no P-face. The local branch lemma gives total
P degree at most two at each vertex of U. The local turn lemma shows that
any two P neighbors there are collinear. Thus a component of G[U] is a
straight path or singleton, never a cycle. An internal path vertex has
its two P neighbors already and cannot contact a chamber. An end with
one path neighbor can have at most one chamber neighbor, and this neighbor
must continue its line. A singleton has total P degree at most two, and
two contacts, if present, are opposite. This proves the second assertion,
including the contact bound.

A noncorner vertex of a 2-by-w chamber already has three chamber neighbors
in P, so no further P contact is possible. A corner already has two and
can have at most one additional contact. This also covers direct chamber
edges. QED.

This is a network description: it does not assert that the chamber quotient
is a tree, that its paths have one universal parity, or that different
chambers have disjoint physical receiver tiles. Those additional properties
must not be used without proof.

## 3. Exact matching exits in the occupied-degree-three frozen case

Now assume every P has deg_A(p)=3 and the pair is bundle-terminal. The
existing cycle criterion implies that M is the unique perfect matching of
G[P]. Indeed, two different perfect matchings have an alternating cycle;
promoting all its endpoints of one color removes two occupied neighbors
from each degree-three promoted vertex, giving a feasible nonempty bundle.
Conversely, in the degree-three single-terminal case a nonempty one-color
bundle has a directed cycle in its matching dependency graph. Thus uniqueness
is also sufficient for bundle terminality by bipartite promotion completeness.
This equivalence is an immediate consequence of the earlier promotion results.

For a chamber C let an exit mean an actual matching edge with exactly one
endpoint in C. Every exit is at one of its four corners by Section 2.

**Matching-exit theorem.** In the occupied-degree-three bundle-terminal case,
each chamber has two or four exits. More precisely, write its rectangle as
{0,1} x {0,...,w-1}.

- For w>=4 it has exactly two exits, one at each longitudinal end. If the
  left corner row is r, the right corner row is r+w modulo 2.
- For w=3 it has either the same two-end pattern, or all four corners exit.
- For w=2 it has either two adjacent exiting corners of its square, or all
  four corners exit.

For each listed exit pattern the internal matching, if part of the actual
configuration, is unique. The list is a necessary classification of chamber
matching restrictions; it does not assert that every pattern has a feasible
exterior or that the separate chamber choices always compose globally.

Proof. The chamber has 2w vertices, so its number of exits is even. With
no exits its matching is a perfect matching of a full 2-by-w rectangle.
That rectangle has at least two perfect matchings for w>=2: use all vertical
edges, or replace the first two vertical edges by the two horizontal edges
of their square. Replacing the chamber matching would give a second global
perfect matching, which is impossible. Thus there are two or four exits.

With four exits remove the four corners. The remaining graph is the full
2-by-(w-2) rectangle. For w>=4 it again has at least two perfect matchings,
so four exits are impossible. For w=2 it is empty; for w=3 it is one
vertical edge. Those internal matchings are unique.

With two exits in the same end column, the remainder is a full 2-by-(w-1)
rectangle. This is nonunique for w>=3, excluding that case. For w=2 its
remaining vertical edge is unique. Otherwise one exit is at each end.
Their colors must be opposite, since the other chamber vertices are
matched internally between the two colors. If the left row is r and the
right row is s, this says r+s+w-1 is odd, equivalently s=r+w modulo 2.

For these opposite-end patterns the matching is forced. At the left end
the remaining corner has just one possible internal neighbor, in column1.
Delete that forced edge. The remaining vertex of column1 then has just
one available neighbor in column2. Continue alternating rows, obtaining
one forced edge per column transition until the last remaining corner.
The color condition ensures that this is precisely the corner not exiting
at the right. For w=2 this includes the horizontal adjacent exit pair;
the same-end case supplies its vertical rotations. This proves all claims.
QED.

The theorem applies to complete components with any number of differently
oriented chambers and connecting paths. It extends the matching-exit
analysis beyond the previous two-row support hypothesis. It does not remove
the degree-three hypothesis: a degree-four occupied endpoint can block an
alternating-cycle promotion, so uniqueness of M is no longer forced.

## 4. Locate all geometric turns in the general case

Allow degree-four P vertices and put

    J={p in P: deg_P(p)=4}.

Mark every P-face containing a member of J. There are at most4|J| marked
faces. After deleting those faces, every remaining face component is a
straight strip, and their vertex sets are pairwise disjoint.

Proof. A perpendicular pair of face adjacencies at a common face forces
the incident corner to have four P neighbors, as in Section2. That corner
belongs to J, so all faces witnessing the turn were marked. The same
argument excludes diagonal corner sharing between two remaining components.
Consequently the previous straight-strip proof applies. Each grid vertex
lies on at most four unit faces, giving the marking bound. QED.

For one initially connected face component, if b faces were marked, the
number of surviving strips is at most1+3b, hence at most1+12|J|. Removing
one vertex from a graph of maximum degree four increases the number of
components by at most three; iterate from the initially connected dual
graph. Empty remaining graphs cause no difficulty. This bound is per
original face component, not a bound on the number of chambers in a whole
endpoint component when J is empty.

The geometric set J is smaller than the set of occupied-degree-four
endpoints: a vertex with three P neighbors and one T can obstruct matching
uniqueness while producing no face junction. Both kinds must be retained
in any subsequent charge argument.

## 5. Consequence for the compensation programme

The arbitrary degree-three problem reduces to matching-constrained networks
of straight chambers and straight links; long chambers have only the two
forced matching exits. Genuine turns within a face component are localized
by Section4 when degree four is present. This supplies structural variables
for a general counting argument instead of assuming that a whole component
is a thin ladder, a particular elbow, or an extractable core.

It does not yet prove rho_H<=1. In particular, physical receiver tiles can
meet different pieces of the same network, so adding separate chamber or
path charges would risk double counting. A future network ledger must sum
each original tile once, retain the saturated-mate transfers, and account
for junctions and nonunit holes. Donor coverage remains a further question
even after a receiver ceiling is proved.

The [punctured-receiver obstruction](PUNCTURED_RECEIVER_EULER_OBSTRUCTION.md)
separately explains why an uncorrected Euler characteristic is insufficient
under single terminality. Its examples are explicitly promotable, so it
does not refute the fully frozen ceiling.

## 6. Validation and continuing discovery

Run the standard-library checker with

    python3 develop/check_degree_three_chambers.py --output output/degree-three-chamber-controls.json

The saved passing receipt covers65,536endpoint masks in a4-by4box:
58,640have no degree-four P vertex;6,896have one or more. Marked-face
localization and the1+3bcomponent bound are checked as well. Exact column
transfer counts cover2,032corner-exit subsets through chamber width128;
112small cases are independently enumerated by graph perfect matchings.
There are258unique internal-matching cases. Finally96complete physical
fixtures and768symmetry images check the network, exits and original
receiver charge, including positive bent caps and four-exit crosses.
These controls test the general proofs rather than replace them.

The independent written-proof review is pending on original stream13282;
the request includes this note before the validation addition and the prior
turn/branch and promotion-cycle proofs. No new Lean execution or independent
acceptance is inferred for this note.

The separate general-ceiling Oracle question remains task
eb07cc29-ff20-402b-aa9b-2a7d2ef567a9, conversation conv_4073388056c31250,
worker lt4r7693kj-go-1, original stream77285. Its last authoritative state
was dispatched/waiting_response, with no answer or verdict observed. It has
not been restarted. This is a different question from the chamber proof audit.

The optional Z3 discovery sources are
develop/search_frozen_receiver_ceiling.py and
develop/search_punctured_frozen_receivers.py. They use z3-solver5.3.1 and
an actual matching, strict finite freeze ranks and, in the unrestricted
rectangle search, an endpoint connectivity certificate. The8-by10rooted
charge-at-least2search timed out after60seconds, both with and without the
freezing requirement. Neither result is UNSAT. The fixed six-row three-hole
template is UNSAT only in its stated finite shape/support domain, independent
of physical translation. It is not a general hole-free theorem.

Seven fixed encoding controls independently compare actual physical
configurations with the solver: three positive frozen fixtures are accepted;
the degree-four promotable patch and a degree-three alternating square are
rejected with freeze ranks and accepted under single terminality alone.
The former patch is not a frozen example, despite its degree-four vertices.
Run these controls in an environment containing the pinned optional solver:

    python develop/check_frozen_receiver_search_encoding.py --output output/frozen-receiver-search-encoding-controls.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
