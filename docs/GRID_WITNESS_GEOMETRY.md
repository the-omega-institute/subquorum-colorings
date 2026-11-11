# Deletion witnesses and simultaneous exchanges on rectangular grids

For an inclusion-minimal two-star-forming set S in a full rectangular grid,
selected vertices of degree four force two distinct omitted vertices each.
These vertices are disjoint across centres and from the direct witnesses
of the other active selections. This gives the arbitrary-width bound

    2|S|-mn <= |Z|+|E|-|H|,                              (1)

where Z comprises the selected components of order at most two, E comprises
selected-degree-two-or-three vertices with no adjacent outside deletion
witness, and H comprises selected-degree-four vertices. A second argument
converts S to a dissociation set of at least its size when the selected
components are stars and their leaf witnesses can be chosen independently.
In particular it applies in every width when all selected vertices of
degree at least two lie in one checkerboard class.

## Definitions and the complete witness classification

All graphs are finite and simple. A set S forms an outside vertex x if
there are distinct a,b in S such that {x,a,b} contains a not necessarily
induced K_(1,2). A forming set forms every outside vertex; it is minimal
if no proper subset forms. Formation is upward closed, so it suffices to
test every single deletion, including whether the newly omitted vertex
itself is formed. SF_2 is the maximum size of a minimal forming set. A
dissociation set induces maximum degree at most one; beta_2 is its maximum
size. Write d_S(v) for selected degree and call a selected vertex active
when d_S(v)>0.

In a bipartite graph an outside vertex x is formed precisely when either
it has at least two selected neighbours, or it has one selected neighbour
which is active. Two neighbours cannot be adjacent in a bipartite graph.

Let v belong to a selected component of order at least three. Then v lies
in a selected three-vertex path. After deleting v, it is consequently
formed by the other two vertices of that path. Minimality supplies a
previously omitted vertex x that becomes unformed. The possibilities are:

1. x is adjacent to v and N_S(x)={v};
2. x is adjacent to v and N_S(x)={v,i}, with i a selected isolate;
3. x is not adjacent to v, N_S(x)={u}, and N_S(u)={v}.

Indeed in the adjacent case x can have at most one remaining selected
neighbour i, which must be inactive after deletion. Since i and v lie in
the same bipartition class, deleting v cannot change i's selected degree:
i was already isolated. In the nonadjacent case the selected neighbours
of x do not change. There must be exactly one, u, whose only selected
partner was v. These cases exhaust failure of formation at x.

Call cases 1 and 2 direct witnesses. Such a witness has exactly one active
selected neighbour, its owner v. Direct witnesses of different active
owners are therefore distinct. A selected leaf in a component of order at
least three must have a direct witness: its selected neighbour has degree
at least two, so deleting that leaf deactivates no other selection.

## Two omitted vertices for every degree-four centre

Let G=P_m square P_n have coordinates (r,c), with both coordinates within
their actual finite ranges. Put O=V(G) minus S. Let Z,E,H be as in (1).
The sets are disjoint. Every member of S outside Z union E union H has
a direct witness, by the leaf observation and the definition of E.

Fix v in H. All four neighbours of v are selected. There is no direct
outside witness for v, and v cannot witness its own deletion. Thus case 3
gives a selected leaf u=v+e and an omitted x with N_S(x)={u}. Here e is
a cardinal unit vector. Choose a perpendicular cardinal unit vector f.
The outside neighbours of u other than v are v+2e and v+e+f, v+e-f.
The latter two see respectively v+f and v-f, both selected and active
through v. Neither can be x. Hence

    x=v+2e,     N_S(x)={u}.                              (2)

In particular the straight position in (2) exists in the actual board.
Both bent positions

    C(v,u)={v+e+f, v+e-f}                               (3)

exist because v is an interior vertex, and are omitted because u is a
selected leaf. Each has at least two active selected neighbours: u and
the appropriate v+f or v-f. Therefore none is a direct witness of an
active selected owner. We call the two positions in (3) caps in this proof.

**Lemma.** For distinct v,w in H, the sets C(v,u) and C(w,t) are disjoint,
for every allowable choice of clean leaves u and t as in (2).

First, two members of H cannot be two steps apart along an axis. Suppose
they were v and w with midpoint z, necessarily selected. After deleting z,
z itself is formed by v,w. A perpendicular neighbour q of z, if omitted,
has three selected neighbours before deletion: z, a neighbour of v, and
a neighbour of w. Both latter neighbours exist since v,w have degree four.
So q cannot be a direct deletion witness. If q is selected it has those
same three selected neighbours, and is not a selected leaf. The other
selected neighbours v,w of z also have degree four. Consequently z has
neither a direct witness nor any selected leaf furnishing a witness of
case 3. This contradicts minimality, by the complete classification.

Suppose now that y is a cap of both v and w. Both centres lie diagonally
from y, at two of its four diagonal positions. Adjacent positions in this
cyclic list are axis-distance two, which was just ruled out. The only
remaining possibility is a pair of opposite positions. Translate and
rotate so y=(0,0), v=(-1,-1), w=(1,1). To offer cap y, the chosen leaf of
v is either (-1,0) or (0,-1). By (2), its clean witness is respectively
(-1,1) or (1,-1). Since w has all four neighbours selected, that witness
also sees respectively (0,1) or (1,0), as well as its original leaf. This
contradicts its clean selected neighbourhood in (2). The lemma follows.

Choose one direct witness for each member of S outside Z union E union H,
and choose one clean leaf at each member of H. There are
|S|-|Z|-|E|-|H| distinct direct resources, and 2|H| distinct cap resources.
The two families are disjoint. Counting them in O proves

    |O| >= |S|-|Z|-|E|+|H|,                              (4)

and hence (1). Every resource is counted once. No matching theorem or
assumption of globally distinct deletion witnesses is needed here.

If Z=E=empty, this yields 2|S|<=mn-|H| at all dimensions. Since one
checkerboard class is a dissociation set, beta_2(G)>=ceil(mn/2); therefore
such S satisfies |S|<=beta_2(G).

There is also an exact residual identity. For the choices above, let Q
be the omitted vertices left unused after reserving all direct witnesses
and both caps per centre. Then

    2|S|-mn=|Z|+|E|-|H|-|Q|.                           (5)

For a desired target F, the remaining inequality |S|<=F is exactly
|Z|+|E|<=|H|+|Q|+2F-mn. That inequality is not established in general;
(5) specifies the part still requiring proof.

## Additional compensation from exceptional degree two and three

The exceptions themselves supply a further unconditional geometric saving.
For each v in E choose an indirect witness triple (v,u_v,x_v), with
u_v=v+e a selected leaf and N_S(x_v)={u_v}. For every selected perpendicular
sibling v+f, the position v+e+f exists in the full rectangle and is omitted,
since u_v is a leaf. It sees the active selections u_v and v+f. Offer this
position as a cap of v. Put t_v equal to the number of selected perpendicular
siblings, choosing a clean leaf to maximize t_v, and put K=sum_(v in E)t_v.
A degree-three exception has t_v>=1. A degree-two exception whose selected
edges are perpendicular has t_v=1; a straight degree-two exception has t_v=0.
Here x_v may be bent: a bent clean witness cannot turn towards a selected
sibling, but the caps on the selected sibling sides still exist.

An omitted position is offered by at most two distinct exceptional centres.
All offering centres lie at its four diagonal positions. If three or four
of those positions were centres, one centre would have both adjacent
diagonal positions occupied by selected centres. Neither of its two possible
leaves towards the cap could then be a selected leaf. Thus, writing R for
the union of the chosen exceptional caps,

    |R|>=ceil(K/2).                                     (6)

No exceptional cap can equal a chosen degree-four cap. For axis-separated
centres normalize the degree-four centre to v=(0,0), the exceptional centre
to w=(2,0), and the common cap to (1,1). The midpoint z=(1,0) is selected
and cannot be a leaf of either centre. Therefore both offered caps use
leaves (0,1) and (2,1). Deleting z leaves z formed by v,w, leaves both
centres active, and leaves the omitted cap formed by its two active leaf
neighbours. The other side neighbour (1,-1), if omitted, retains the active
selection (0,-1); if selected, it retains that same selected neighbour.
All four neighbours of z therefore either remain active when selected or
remain formed when omitted. There is no direct or indirect witness, a
contradiction. All coordinates mentioned exist because v has degree four
and w lies in the full rectangle.

For opposite diagonal centres normalize v=(0,0), w=(2,2) with cap (1,1).
Offering the cap forces both (1,2) and (2,1) to be selected neighbours of
w, one the chosen leaf and one its sibling. Either possible straight clean
witness of v sees one of those selections, contradicting (2). These are
all possible relative centre positions, proving the disjointness.

For the stronger count, reserve the centre and its chosen leaf for every
member of H union E. The leaves are distinct and no leaf is a centre.
There remain |S|-|Z|-2|H|-2|E| direct owners, all admitting direct witnesses.
Add the |H|+|E| chosen clean witnesses. A clean witness is not also counted
for its leaf, since that leaf was reserved and removed from the owner list.
Their singleton selected neighbourhoods make clean witnesses distinct and
disjoint from the remaining direct witnesses. The 2|H| degree-four caps
and |R| exceptional caps are disjoint from those resources because each
cap has at least two active selected neighbours. Thus

    |O|>=|S|-|Z|-|E|+|H|+|R|
        >=|S|-|Z|-|E|+|H|+ceil(K/2).                    (7)

Let E_3 denote degree-three exceptions and E_(2,angle) the bent degree-two
exceptions. Since K>=|E_3|+|E_(2,angle)|, (7) gives an explicit saving of
at least ceil((|E_3|+|E_(2,angle)|)/2) over (4). A sufficient condition
for |S|<=beta_2(G), at any dimensions, is

    |H|+ceil(K/2)>=|Z|+|E|.

More precisely, if Q' is the omitted set left after the reservations for
(7), its exact residual identity is

    2|S|-mn=|Z|+|E|-|H|-|R|-|Q'|.                     (8)

The full-rectangle hypothesis is substantive. Subdivide each edge of
K_(1,4) once and select its centre and four subdivision vertices. Each
omitted terminal leaf is formed along its arm. Deleting any subdivision
vertex uncovers that terminal, and deleting the centre makes every arm
neighbour inactive. This is a minimal forming set with |S|=5, |O|=4,
Z=E=empty and |H|=1, contradicting the proposed extension of (4) to
arbitrary bipartite maximum-degree-four graphs. It also explains why caps
cannot be supplied across holes or deleted grid edges without extra proof.

## Simultaneous exchange through independent leaf witnesses

**Theorem.** Let G be bipartite and S minimal forming. Suppose every
component of G[S] is a star, an edge or an isolate. For each leaf ell of
a selected star of order at least three, choose a direct witness w_ell.
If the chosen set W is independent, there is a dissociation set
D contained in S union W with |D|>=|S|.

Write C for the nontrivial star centres, L for their leaves, and I for
the selected isolates touched by chosen witnesses. The classification
gives N_S(w_ell)={ell} or {ell,i_ell} with i_ell in I. The witnesses are
distinct because each has just one active selected neighbour.

Construct an auxiliary multigraph A with actual vertices C union I.
Each leaf ell indexes an edge joining its centre c to i_ell when present.
Otherwise give that leaf its own new dummy endpoint d_ell and add cd_ell.
Parallel edges are allowed. Subdivide each edge into

    c -- ell -- w_ell -- i_ell,

using d_ell for the private case; the dummy and its last edge are bookkeeping
only. In the actual graph a private case is the length-two path c,ell,w_ell.
This is exactly the induced graph on the relevant actual vertices: selected
components specify the S--S edges, witness classification specifies every
S--W edge, and independence excludes W--W edges. Selected isolates not
touched and isolated selected edges have no edge to these witnesses.

For each connected component of A let e count its edges, v its endpoints
including dummies, and a its actual endpoints. It contributed a+e vertices
to S. If it is a tree, root it at any endpoint, including a dummy. Retain
every actual endpoint and, for each subdivided edge, exactly the internal
vertex adjacent to its child endpoint. A retained endpoint sees at most
its parent-edge partner. A retained internal vertex sees at most the
retained child endpoint. Dummy endpoints are omitted. Thus the retained
induced degree is at most one and its cardinality is exactly a+e.

If the component has a cycle (including a pair of parallel edges), e>=v>=a.
Omit all endpoints and retain both internal vertices of every edge. They
induce disjoint edges and contribute 2e>=a+e vertices. Perform these choices
simultaneously and retain all untouched selected isolates and isolated
selected edges. This gives D and proves the theorem.

If all selected vertices of degree at least two lie in one bipartition
class, every selected component of order at least three is automatically
a star centred in that class. Its leaf witnesses lie in the centre class,
so are independent. Consequently |S|<=beta_2(G). This applies to every full
rectangular grid without a width restriction. Any counterexample to
SF_2=beta_2 on a bipartite graph must have selected high-degree vertices
in both classes in every maximizing minimal selection exceeding beta_2.

For completeness, the construction also bounds the cost of witness conflicts.
Without independence, ignore W--W edges while constructing the same set,
and let W_* be the witnesses retained. Its size is |S|+q, where q is the
sum of e-a over cyclic auxiliary components. Delete a vertex cover of
G[W_*]. All extra edges are removed, so

    beta_2(G)>=|S|+q-tau(G[W_*]).                       (9)

Witness choices and tree roots affect W_*. An edge in W alone does not
imply failure of the desired inequality.

## A full six-by-six obstacle to automatic independence

The assertion that independent choices always exist under the selected-star
hypothesis is false. In one-based coordinates select the following columns
in rows 1 through 6:

    1,4,6;  1,3,5;  1,3,4,6;  2,6;  3,5;  1,2,4,6.

There are 18 selections. The two selected P_3 components are
(1,1)--(2,1)--(3,1) and (2,3)--(3,3)--(3,4). There are also selected edges
(3,6)--(4,6) and (6,1)--(6,2); the other eight selections are isolated.

All omitted vertices have at least two selected neighbours, except (1,2),
(4,4), and (5,1). They are formed along the paths
(1,2)--(1,1)--(2,1), (4,4)--(3,4)--(3,3), and
(5,1)--(6,1)--(6,2), respectively. All selections in components of order
one or two witness their own deletion. The six P_3 selections have witnesses:

| Deleted vertex | Vertex left unformed |
| --- | --- |
| (1,1) | (1,2) |
| (2,1) | (1,2) |
| (3,1) | (4,1) |
| (2,3) | (1,3) |
| (3,3) | (4,4) |
| (3,4) | (4,4) |

Thus S is globally minimal. For the leaves (1,1) and (2,3), the complete
deletion-witness sets are respectively {(1,2)} and {(1,3)}. To check
completeness, deleting a leaf leaves its centre active, so only direct
outside neighbours can fail. The first leaf has only (1,2) outside. The
second has outside neighbours (1,3),(2,2),(2,4): the latter two retain an
active neighbour and three selected neighbours, respectively. The forced
witnesses (1,2),(1,3) are adjacent, disproving automatic independence.

The same-size exchange

    D=(S minus {(2,1),(3,3)}) union {(1,2),(4,4)}

is nevertheless dissociation. Its new vertices are paired only with
(1,1) and (3,4), respectively; other former star leaves become isolated.
The example therefore refutes the witness-selection rule and leaves the
grid equality intact.

## Reproduction and scope

Run from the repository root, with Python assertions enabled:

```sh
python3 scripts/check_grid_disjoint_caps.py
python3 scripts/check_star_witness_exchange.py
```

The geometric checker uses literal three-vertex stars and every global
single deletion. It compares the activity predicate on all 190,798 subsets
of its listed small full rectangles, audits 3,176 minimal sets in total,
and checks all clean-leaf choices in its degree-four cases. Twelve protected
cross fixtures on 7-by-7, 7-by-15 and 15-by-15 boards contribute 28 actual
degree-four centres and 28 centre pairs. The protected crosses retain their
straight private witnesses throughout greedy deletion; these are nonvacuous
tests of the lemma. The deterministic report lists all coordinates.

The geometric audit additionally checks the exceptional caps for every
minimal set, all clean-leaf alternatives, multiplicity at most two across
different owners, disjointness from degree-four caps, and both the stronger
actual-union and incidence bounds. Alternative choices at the same centre
are not counted simultaneously.

The exchange checker exhausts 5,013 labelled bipartite graphs over all part
sizes on at most six vertices (up to exchanging the parts), plus part sizes
3 and 4. It tests 578,599 selections and 39,067 minimal selections, including
5,214 with nontrivial selected stars satisfying the component hypothesis.
All witness assignments and all auxiliary tree roots are covered, giving
50,196 constructions including 18 with conflicting witnesses. Targeted
fixtures cover shared isolates, private dummies, parallel cycles, an ordinary
four-cycle, positive cycle surplus, and extra witness edges. The exact
minimum vertex cover of retained conflicts is checked by brute force. The
six-by-six example and its explicit size-18 dissociation set pass separately.
The full report is `output/star-witness-exchange-check.json`.

The all-graph and all-width claims use the written proofs above. The finite
checks test the implementation and explicit examples. General rectangular
triple equality still requires handling both checkerboard classes and
controlling the residual in (8). The separate strip theorems now cover
every positive length when the shorter side is at most five. No Lean
verification is claimed for this note.


The independent audit of scientific revision 2958b91 returned **ACCEPT**,
with no required mathematical changes. The reviewer reconstructed all five
manifest files, checked their byte counts and hashes, and ran both original
Python scripts unchanged with assertions enabled. Both generated JSON
reports matched the supplied reports byte-for-byte. It independently
reconstructed the witness classification, cap-disjointness and capacity
arguments, clean-leaf reservation, exact residual, auxiliary tree/cycle
exchange, conflict-cover variant and the six-by-six obstacle. The complete
response, attachment manifest and actual execution scope are preserved in
`output/grid-witness-geometry-review.json`. This verdict covers the stated
conditional and defect-counting results; the further inequality needed
to control the defect in (8) remains open.
