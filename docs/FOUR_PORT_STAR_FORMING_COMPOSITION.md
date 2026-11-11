# Exact composition through four attachment vertices

11 November 2026. This extends the two-attachment theorem in
`EXACT_STAR_FORMING_COMPOSITION.md`. The new part is that all four vertices
`a1,a2,b1,b2` can meet the surrounding graph simultaneously. No restriction
on the number of edges at these vertices is needed for the local upper bound.

## Definitions and a general deletion principle

A set S in a finite simple graph is 2-star-forming when every x outside S
belongs to a (not necessarily induced) K1,2 in G[S union {x}]. Equivalently,
x has at least two selected neighbors, or a selected neighbor with a selected
neighbor. Let SF2 be the maximum size of an inclusion-minimal such set;
beta2 is the maximum size of a set inducing maximum degree at most one.

**Ambient deletion lemma.** Let K be an induced subgraph of G, and let P
contain every vertex of K with a neighbor outside K. Put C=S intersect V(K)
for a forming set S. Suppose v belongs to C minus P, C minus {v} is forming
inside K, and every selected p in P having a selected neighbor in K before
deletion still has one afterwards. Then S minus {v} is forming in G.

Proof. Every omitted vertex in K has an internal witnessing star, including
the newly omitted v. An omitted x outside K keeps an old witnessing star
unless it uses v. Since x is not adjacent to the nonattachment vertex v,
such a star has selected center p in P and leaves x,v. Replace v with a
surviving selected internal neighbor of p. This neighbor differs from x,
since it is internal and selected. This proves the assertion. In particular,
if these hypotheses supply a deletion whenever |C|>q, every minimal global
forming set contains at most q vertices of K. Disjoint induced subgraphs
with these bounds can be counted simultaneously; no vertex is counted twice.

## The four-attachment theorem

Let H have bipartition A={a1,...,a5}, B={b1,...,b5} and cross-edge matrix

    11001
    11010
    00011
    01111
    10111

Let P={a1,a2,b1,b2}. If H is induced in any finite simple G and every
external edge touches H at P, every minimal forming set S satisfies

    |S intersect V(H)| <= 6.                                      (1)

The outside graph need not be bipartite. Here is a complete proof of the
new local assertion.

Every edge xy of H satisfies deg(x)+deg(y)>=6. If a dominating T has at
least six vertices, an outside x with unique selected neighbor u cannot
have u isolated in H[T]: the disjoint sets N(x) minus {u} and N(u) would
both lie in the complement of T, forcing that complement to have at least
five vertices. They are disjoint by bipartiteness. Therefore domination
and formation coincide for selections of size at least six.

Suppose C=S intersect V(H) has at least seven vertices; write W=V(H) minus C,
so |W|<=3. First C dominates H. An undominated x would satisfy N[x] subset W.
Only the degree-two vertices a3,b3 can have closed neighborhoods this small.
Neither belongs to P, so such an x would have no selected neighbor even in G,
contradicting formation of S.

There are at most two vertices whose deletion destroys internal domination.
Indeed, the closed neighborhoods of size three are the disjoint triples
{a3,b4,b5} and {b3,a4,a5}. At most one deletion can complete one of these
triples from W, because each completion needs two points of W. The four
closed neighborhoods of size four are those of a1,a2,b1,b2; any two
intersect in at most two vertices. A deletion completes such a neighborhood
only if |W|=3 and W lies in it, so at most one deletion can do so. The other
closed neighborhoods have size five and cannot be completed by W union {v}.

Put t=|C intersect P|. If t<=2, there are at least 7-t nonattachment
candidates. At most two destroy domination, and at most t further candidates
destroy the internal activity of a selected attachment: each attachment has
at most one unique selected neighbor. Since 7-t>2+t for t<=2, a safe
candidate exists. If t>=3, the selected attachment vertices induce a
complete bipartite graph with both sides nonempty. Every selected attachment
has a selected attachment neighbor, which no nonattachment deletion removes.
There are at least 7-4=3 candidates and at most two domination failures.
Again a safe candidate exists. After deleting it, at least six vertices
remain, so domination implies formation. The ambient deletion lemma now
contradicts minimality of S and proves (1).

The boundary-induced K2,2 is what permits four attachments: the old coarse
count that charges one possible activity failure to every attachment is
unnecessarily large when three or four of them are selected.

## Exact arbitrary interfaces

Take r disjoint induced copies of H. Add any edges between distinct copies,
always from one of {b1,b2} to one of {a1,a2}. Then

    beta2(G)=5r,             SF2(G)=6r.                           (2)

The local theorem gives the SF upper bound. In each copy select
S0={a1,a2,a3,b1,b2,b3}. Every omitted vertex has two selected neighbors.
The following deletion failures persist under every allowed interface:

| Deleted | Failure vertex | Its remaining selected neighbors |
| --- | --- | --- |
| a1 | b5 | {a3} |
| a2 | b4 | {a3} |
| a3 | a3 | empty |
| b1 | a5 | {b3} |
| b2 | a4 | {b3} |
| b3 | b3 | empty |

Vertices a3,b3 remain isolated in the selected subgraph, because they have
no external edges. Thus every deletion fails. Formation is upward closed,
so the union of these sets is inclusion-minimal, proving SF2=6r.

For beta2, the independent A side gives 5r. A dissociation set restricts
to at most five vertices in each H. To see the local upper bound without
enumeration, a dissociation six-set has side split (1,5),(2,4), or (3,3),
up to exchanging the sides (the matrix is symmetric). The first fails
minimum degree two. In the second, omitting one B vertex permits only
the degree-two vertex a3 on the A side, not two vertices. In the third,
a4,a5 cannot be selected, since each sees at least two of any three B
vertices. Thus the A side is {a1,a2,a3}. Both a1,a2 need b1,b2 omitted,
leaving B={b3,b4,b5}, and a3 then has two selected neighbors. This proves
beta2(H)=5 and hence (2). The empty graph gives both values zero.

## Two-connected maximum-degree-four realizations beyond cycles

Let Q be a finite connected loopless graph with an orientation such that
each vertex has at most two incoming and two outgoing edges. Suppose Q
has no bridge. Replace each vertex i with H_i. Assign different outgoing
edges at i to b1_i,b2_i and different incoming edges at i to a1_i,a2_i;
join the assigned ports for each directed edge. The resulting graph has
order 10|V(Q)|, is bipartite and two-connected, has maximum degree four,
and has exact gap |V(Q)|=|V(G)|/10.

Each attachment is used at most once, so its degree rises from three to
at most four. Each H has the Hamilton cycle

    a1,b1,a2,b2,a4,b3,a5,b4,a3,b5,a1.

Deleting one vertex leaves its copy connected and removes at most one
interface edge, because all incident interfaces use distinct ports. The
remaining Q is connected by the no-bridge assumption; therefore the entire
graph remains connected. This proves two-connectivity.

In particular every connected simple four-regular Q qualifies: an Euler
orientation has two incoming and two outgoing edges at every vertex, and
a connected graph with all degrees even has no bridge. For Q=C_m squared,
m>=5, this gives an explicit 10m-vertex family with 18m edges, eight degree-four
vertices and two degree-two vertices per block. The square here joins
cyclic distances one and two; for m=5 it is K5. The two-attachment theorem
does not cover these realizations, since every one of the four attachments
in each block has an external neighbor.

## Scope and verification

The new results are the simultaneous four-attachment cap, the corresponding
larger exact-composition class, and its bridge-free interface realization.
The base graph, two-attachment theorem, and density 1/10 are earlier results.
No larger gap density or universal extremal bound is inferred. Unit-weight
grid equality and the sub-quorum 5/6 question remain separate problems.

The verifier `scripts/check_four_port_composition.py` checks the local
neighborhood counts, all dense selections, surrounding graphs and full
small-composition optima. Its standalone C++ helper evaluates the original
star condition and all single deletions directly. The all-interface theorem
and connectivity statements rest on the proofs above. Existing Lean sources
formalize the earlier two-attachment theorem; this extension is not claimed
as newly Lean-checked.
