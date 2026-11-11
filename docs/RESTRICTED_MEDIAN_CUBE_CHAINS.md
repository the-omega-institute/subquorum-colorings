# Cubes in planar median graphs of maximum degree four

A median graph is a connected graph in which the three pairwise metric
intervals of any three vertices have a unique common vertex. We prove
that the induced three-dimensional cubes of a finite planar median graph
of maximum degree at most four form convex chains. This reduces the cube
part of the restricted star-forming equality question to chains with
attachments at their ends. The cube-free degree-four case remains open.
The maximum-degree-three case follows completely from a verified
squaregraph characterization and the bipartite prism formula.

## 1. Elementary median facts

Median graphs are bipartite. Fix a root o. If adjacent u,v had equal
distance from o, the median of o,u,v would be an endpoint of I(u,v)={u,v};
neither endpoint belongs to the interval from o to the other endpoint.
Thus adjacent distances differ by one, providing a parity bipartition.

Distinct vertices have at most two common neighbours. If a,c had three
common neighbours b,d,e, these neighbours would be pairwise at distance
two, and both a,c would lie in all three pairwise intervals of b,d,e.
This contradicts the unique-median property.

Every four-cycle is convex: its opposite vertices already have two
common neighbours, so no other length-two geodesic exists. The remaining
pairs are adjacent. In particular every square is induced.

Every induced cube Q_3 is convex. It is first isometric: distance-two
pairs remain at distance two, and antipodes remain at distance three by
bipartiteness and inducedness. Only an antipodal pair u,v could admit a
geodesic leaving the cube. An outside vertex z on it can be taken, after
interchanging u,v, to satisfy d(u,z)=1,d(z,v)=2. For any cube neighbour a
of u, the vertices z,a,v are pairwise at distance two. Their median must
be adjacent to all three. Its membership in I(a,v), a convex cube square,
places it at a cube vertex w at distance two from u. But z is then a
third common neighbour of u,w, impossible. Therefore the cube is convex.

A cube subgraph automatically is induced. Any additional cube edge in
a bipartite graph must join antipodes. If u,v are these antipodes and a
is a cube neighbour of u, the distance-two cube pair a,v would have its
two cube common neighbours and the extra common neighbour u. This is
impossible by the preceding bound.

Finally, any nonempty convex subset of Q_3 is a coordinate face. Translate
one of its vertices to 000 and choose a vertex w of maximum Hamming
weight in the subset. If another vertex z had a 1 outside the support of
w, I(w,z) would contain the coordinatewise union, of larger weight.
Thus all supports are inside that of w. Convexity of I(000,w) then
includes every such support. This proves the assertion directly.

## 2. The maximum-degree-three case

**Corollary of the squaregraph characterization.** Every finite
two-connected median graph of maximum degree at most three is a ladder
P_t square K_2, t>=2, or Q_3. Here two-connected requires at least three
vertices. In particular

    SF_2(P_t square K_2)=beta_2(P_t square K_2)=2 ceil(t/2),
    SF_2(Q_3)=beta_2(Q_3)=4.

**Proof.** If a cube occurs, all its vertices already have degree three,
so connectedness forces the whole graph to be that cube. Otherwise use
Bandelt--Chepoi--Eppstein [1, Proposition 9]: a finite median graph has
a squaregraph plane embedding precisely when it has no induced cube,
book K_2 square K_(1,3), or suspended cogwheel. The book has maximum
degree four. A suspended cogwheel is a bipartite wheel with a pendant
vertex at its hub; the source requires at least four spokes, so the
hub has degree at least five. All three obstructions are excluded.

In a squaregraph every bounded face is a quadrilateral and every
interior vertex has degree at least four. Thus here there are no
interior vertices. Two-connectivity makes the outer boundary a simple
cycle containing all vertices. The remaining edges are noncrossing
chords, and they form a matching: each vertex already has two boundary
edges and can have at most one chord.

The weak dual of this polygon quadrangulation is a tree, because each
chord separates the polygon and gives a dual bridge. Every face has at
most two chord edges, which must be opposite because chords share no
endpoints. Thus the weak dual is a path, and adding its faces in order
constructs precisely a ladder. The equality formulas follow from the
bipartite prism theorem, since alpha(P_t)=ceil(t/2) and Q_3=C_4 square K_2.
This is a consequence of [1], not a new structural classification. QED.

## 3. The chain theorem

**Theorem.** Let G be a finite planar median graph with Delta(G)<=4.
Form a graph whose vertices are the induced Q_3 subgraphs of G and whose
edges join cubes with nonempty vertex intersection. Each connected
component is a path. The union of a component with r>=1 cubes is an
induced convex subgraph

    T = C_4 square P_(r+1).

Only the two end C_4 layers of T can have neighbours outside T. There
are at most eight edges from T to its complement. If r>=2, each connected
component of G-V(T) attaches entirely to one end layer. If G is also
two-connected, each nonempty outside component has at least two distinct
attachment vertices.

**Proof.** Two intersecting cubes have a convex intersection, hence a
coordinate face by Section 1. If its dimension is d, each intersection
vertex has at least 6-d incident edges in their union. The degree bound
forces d>=2. Distinct cubes have d<=2, so their intersection is a square.

At most one other cube meets a fixed cube on a specified face. After one
attachment, every vertex of that face has degree four: two neighbours
on the face and one in each cube off the face. A further attached cube
would have to use the same four off-face neighbours, and so would be the
same cube.

Two other cubes cannot meet a cube C on adjacent faces. Suppose they did,
with faces sharing edge ab. At a the external neighbours supplied by
the two cubes must coincide, since C already gives three neighbours;
likewise at b. Call the common new neighbours a',b'. The three cubes
have pairwise square intersections, with the two attached cubes sharing
exactly the square a-b-b'-a'-a. The triple intersection is exactly ab.
Their edge-union would have

    3*8-3*4+2=14 vertices,
    3*12-3*4+1=25 edges.

A simple planar bipartite graph on 14 vertices has at most 24 edges.
This contradiction means that a cube can meet other cubes only on
opposite faces, at most two. The cube intersection graph thus has
maximum degree two.

A cycle of r>=3 cubes is also impossible. The two shared faces of every
cube would be opposite and disjoint, so there are no triple intersections.
The union would have 4r vertices and 8r edges, contradicting the bound
8r<=2(4r)-4. Consequently all components are paths.

Along such a path, the two shared faces in every internal cube are
opposite. Relabel consecutive square layers to remove the possible
face automorphisms. The edge-union is C_4 square P_(r+1), with

    v=4r+4, e=8r+4=2v-4.

An additional edge of G on these vertices would violate the planar
bipartite edge bound. Thus the union T is induced.

In the inherited plane embedding, T is two-connected and bipartite,
so all facial boundaries are cycles of length at least four. Equality
e=2v-4 forces every facial boundary to be a square. Each connected
outside component lies in one face. If a geodesic between T vertices
left T, one maximal excursion would have endpoints on that facial
square and internal vertices outside it. The excursion is itself a
geodesic, contradicting the convexity of every square. Thus T is convex.

An internal-layer vertex already has degree four in T. An end-layer
vertex has degree three, so it admits at most one outside edge. This
gives the bound of eight. When r>=2 every square of T is either one
layer or a Cartesian square in consecutive layers; no square meets both
end layers. Each outside component therefore attaches at one end.
Finally, a single attachment vertex would be a cut vertex of G.
This proves all assertions. QED.

## 4. Parameter consequence and remaining interface

The previously proved bipartite prism theorem applies to the isolated
chain, since

    C_4 square P_(r+1) = (K_2 square P_(r+1)) square K_2.

The base ladder has independence number r+1: its r+1 rungs bound every
independent set, and a bipartition class attains the bound. Hence

    beta_2(T)=SF_2(T)=2(r+1)=|V(T)|/2.

The structural theorem does not identify the parameters after arbitrary
attachments. At a shared square, selections must agree, selected-degree
capacities must be respected, and activity or deletion witnesses may
come from either side. The explicit activity counterexample in
`SQUARE_EAR_STAR_FORMING_COMPOSITION.md` explains why a parameter formula
cannot be obtained by discarding this interface information.

The restricted question is whether every two-connected planar median
graph with Delta<=4 has SF_2=beta_2. The theorem above and the exact
square-ear classes reduce the search; they do not establish that equality.

## Reference and source verification

[1] H.-J. Bandelt, V. Chepoi and D. Eppstein, *Combinatorics and geometry
of finite and infinite squaregraphs*, SIAM Journal on Discrete Mathematics
24 (2010), 1399--1440. DOI: [10.1137/090760301](https://doi.org/10.1137/090760301).
The statement used here is Proposition 9, on page 13 of the checked
[arXiv:0905.4537v1 author manuscript](https://arxiv.org/abs/0905.4537v1).
The definition immediately before it specifies a cycle of length 2k>6
and one pendant vertex at the hub, verifying the degree-five threshold.
Crossref metadata and the full primary PDF were read; the theorem is
not inferred from a secondary summary.
