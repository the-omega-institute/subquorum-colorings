# A robust twenty-vertex block for two-connected subcubic gaps

12 November 2026.

For every integer r>=1 we construct a two-connected bipartite graph G_r with
minimum degree two, maximum degree three, and

    |V(G_r)|=20r,   beta_2(G_r)=11r,   SF_2(G_r)>=12r.

Thus SF_2-beta_2>=r=|V|/20. This raises the lower coefficient of our earlier
[exact cyclic family](EXACT_SUBCUBIC_COMPOSITION.md), whose gap is |V|/22.
The two families differ: the previous SF value is exact at every admissible
order; the present argument proves an SF lower bound. The unrestricted upper
bound remains floor(7n/71). No sharp coefficient for the whole subcubic class
is asserted.

Here a dissociation set induces maximum degree at most one, and beta_2 is its
largest size. A set S is two-star-forming if each x outside S lies in a not
necessarily induced two-leaf star in G[S union {x}]. Equivalently, x has two
selected neighbours, or a selected neighbour with a selected neighbour.
SF_2 is the maximum size of an inclusion-minimal such set.

## The explicit block

Start with a graph H on {0,...,19}. Set

    I={0,1,2,3}, X={4,...,11}, C={12,...,19}.

Each helper i in I is adjacent to 4+2i and 5+2i. Each witness x in X is
adjacent to its owner x+8. Add the witness matching

    4--11, 5--9, 6--8, 7--10,

and the two complete bipartite squares

    {12,13} x {16,19},    {14,15} x {17,18}.

These are all the edges. One bipartition class is

    A={0,1,8,9,10,11,12,13,14,15};

the other class is its complement. Delete the owner edge 4--12 and call the
result F. Its two ports are 4 and 12, of opposite colours. The coordinates
and certificates are in [the fixture](../develop/fixtures/twenty-vertex-subcubic-core.json).

**Lemma 1.** beta_2(F)=beta_2(H)=11. An optimum avoiding both ports is

    D={0,2,3,6,7,9,11,13,14,15,16}.

**Proof.** The induced graph on I union X is the twelve-cycle in cyclic order

    (0,4,11,3,10,7,1,6,8,2,9,5).

Every three consecutive cycle vertices contain an omission from a dissociation
set, so at most eight of them can be selected. Each core square contributes
at most two selected vertices. Thus every dissociation set of F has size at
most twelve. A set of size twelve would have exactly eight cycle vertices and
four core vertices.

If eight vertices of the twelve-cycle are selected, each cyclic gap between
two successive omitted vertices is at most three edges: a larger gap would
contain three consecutive selected vertices. There are four omissions and the
gaps sum to twelve, so every gap equals three. Hence the omitted positions
are exactly one of the three residue classes modulo three. The selected cycle
vertices have the following three possible forms:

| Selected cycle vertices | Core vertices not forbidden by a selected cycle neighbour | Maximum core contribution |
| --- | --- | --- |
| all eight witnesses X | {12} | 1 |
| I union {5,7,8,11} | {12,14,17,18} | 1+2=3 |
| I union {4,6,9,10} | {12,13,15,16,19} | 2+1=3 |

To justify the forbidden entries, in the first row each selected witness is
already paired with its witness-matching neighbour. In the other two rows
each selected witness is paired with its helper. An adjacent owner would give
that witness a second selected neighbour. The deleted edge makes owner12
available even in the last row. In the middle row the available core consists
of an isolate12 and the three-vertex path17--14--18. In the last row it
consists of the first whole square and the isolate15. Neither row permits
four selected core vertices. A twelve-set is therefore impossible.

The displayed D induces exactly the five edges 2--9,3--11,6--14,7--15,13--16
and the isolate0. It avoids both ports, so it is a dissociation set in F and
also after restoring 4--12. Adding an edge cannot increase beta_2, proving
both asserted equalities. This is a structural upper-bound proof, not an
inference from the finite controls. QED.

**Lemma 2.** F is two-connected.

**Proof.** It has the Hamilton cycle

    (4,0,5,13,19,12,16,8,2,9,17,15,18,14,6,1,7,10,3,11).

All consecutive pairs, including the closing pair11--4, are edges of F.
Deleting any one vertex leaves the spanning path from this cycle connected.
QED.

## Exact dissociation composition through the ports

**Proposition 3.** Take r>=0 disjoint copies of F and any disjoint finite
simple graph A, whose induced graph is kept equal to A. Add any collection
of new edges subject to the rule that,
at every copy of F, all endpoints of new edges belong to its two ports.
One may also restore the edge between the two ports within a copy. If G is
the resulting graph, then

    beta_2(G)=11r+beta_2(A).

**Proof.** Restrict a dissociation set to each block and A. Its block
restriction is a dissociation set of F even if the port edge has been added,
so Lemma1 bounds it by eleven. The restriction to A has size at most beta_2(A).
This proves the upper bound. Conversely, use D in each block and an optimum
in A. Every new edge with an endpoint in a block meets an unselected port;
there are no new edges between two vertices of A, whose induced graph is A
by definition. The union is a dissociation set of size11r+beta_2(A). QED.

There are no degree, connectivity, or bipartiteness requirements in this
proposition. It uses the elementary restriction-and-union argument; the
specific ingredient here is the explicit port-avoiding optimum of F.
The analogous SF additivity is not claimed under these arbitrary attachments.

## All-order two-connected family

Take F_i, i in the cyclic group of order r, with labels v_i. Add

    4_i--12_(i+1)   for every i.

For r=1 this restores the deleted edge, giving H. For r=2 the two cross-edges
are distinct edges between the two blocks. In all cases the resulting G_r is
simple and bipartite. Its two bipartition classes have size10r. The four
helpers in each block have degree2 and the other sixteen vertices have degree3;
therefore its order is20r and its edge count is28r.

**Theorem 4.** Every G_r is two-connected and satisfies

    beta_2(G_r)=11r,   SF_2(G_r)>=12r,   SF_2(G_r)-beta_2(G_r)>=|V(G_r)|/20.

**Proof.** Proposition3 with A empty gives the exact beta value. For
connectivity, each block remains connected after any one vertex deletion by
Lemma2. For r>=2, contracting the connected surviving parts of the blocks
gives a cycle of blocks, with two parallel quotient edges when r=2. A deleted
vertex removes at most one joining edge, since the two port vertices are
distinct. A cycle of blocks remains connected after losing at most one edge.
Thus the graph after deletion is connected. For r=1, F is a spanning
Hamiltonian subgraph of G_1=H, and gives the assertion directly.

Let S be the union of all helper and owner layers I_i union C_i. It has size
12r, and every outside witness has exactly two selected neighbours: its helper
and its owner, with the owner of4_i now12_(i+1). Thus S is star-forming.
The helpers are isolated in the selected graph, so deleting any helper leaves
that vertex uncovered. The owners assigned to witnesses remain a bijection.
Deleting an owner leaves its unique assigned witness with only its helper
selected. That helper remains isolated in the selected graph; the witness
therefore has no two-leaf star. Every selected vertex is essential, proving
inclusion-minimality. Subtract the exact beta value to obtain the gap. QED.

For r=1, the known bound SF_2-beta_2<=floor(7n/71)=1 gives SF_2(H)=12.
For general r we do not assert SF_2(G_r)=12r. The universal bound and this
family place the asymptotic extremal coefficient for two-connected bipartite
graphs of minimum degree2 and maximum degree3 in [1/20,7/71]. Whether this
interval can be narrowed is open.

## Verification

Run

    python3 scripts/check_twenty_vertex_subcubic.py --output output/twenty-vertex-subcubic-check.json

The standalone checker constructs the block independently from coordinates,
tests the cycle argument, literally checks every subset of F and H, compares
small arbitrary-attachment optima to the composition formula, and checks
actual full family certificates at larger orders. It distinguishes exact
finite optima from larger explicit certificates. The all-r conclusions are
the written proofs above. The original October manuscript is unchanged;
this result is included in the separate working star-forming manuscript.
Independent review scope is recorded in output/twenty-vertex-subcubic-review.json.
