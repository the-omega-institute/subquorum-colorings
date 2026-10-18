Thank you; your three exposition revisions are applied. Please independently referee this further exact interaction-graph formula and the reciprocal two-connected realization. Treat our already reviewed arbitrary-interface SF=8r theorem as a premise. The earlier saturated-port lemma says every dissociation set in B=Heawood-PL has size<=8, and any eight-set selects both ports with internal selected degree1. Explicit local witnesses are D8={0,1,2,3,7,8,12,13}, selecting ports0,8 with four matching edges, and D7={1,2,4,5,7,10,13}, omitting both ports. Base bipartition points0..6, lines7..13; the removed edge is0--8. Check the formula for completely arbitrary simple graphs on all ports, including restored within-block incidences (loops in Q), the claim of exact vertex-cover gap, and all connectivity/degree/independence claims of the reciprocal construction. Find any hidden interaction or double counting. No enumeration or Lean as proof; no novelty claim.

## The interaction graph gives the exact dissociation number

The arbitrary-interface statement also has an exact beta formula. Let Q
have one vertex for each block. Join two distinct block indices when at
least one port edge connects them, and put a loop at an index when its
deleted incidence is restored. Multiple port interfaces give only one
adjacency in Q. Let alpha_0(Q) be the maximum size of a set containing
no looped vertex and no adjacent pair. Then

    beta_2(G)=7r+alpha_0(Q),
    SF_2(G)-beta_2(G)=r-alpha_0(Q).

For a loopless Q, alpha_0 is its usual independence number, and the gap
is exactly its minimum vertex-cover number tau(Q). If loops are present,
the same interpretation holds with a cover required to contain every
looped vertex.

To prove the upper bound, restrict any dissociation set D to each block.
The earlier saturated-port lemma gives at most eight vertices per block;
every eight-block selects both ports, each already of internal selected
degree one. Two eight-blocks cannot have an interface between them, and
an eight-block cannot have its deleted incidence restored. Thus its set I
of eight-blocks is independent in Q and contains no looped vertex. Counting
every other block at most seven gives

    |D|<=7r+|I|<=7r+alpha_0(Q).

Conversely, take an attaining independent set I in Q. In each indexed
block choose the previously displayed D_8, which selects both ports and
induces four independent edges. In every other block choose D_7, which
omits both ports. No interface has two selected endpoints. The union is
dissociation of size 7r+|I|, proving equality. Each block contributes once;
there is no allocation of one neighboring block to multiple dense blocks.

In particular, SF_2=beta_2 in this composition class if and only if Q
has no edge and no loop. Any nonempty port interface creates a strict gap.
The cyclic family's interaction graph is a cycle for r>=3, one edge for
r=2, and one loop for r=1, recovering the earlier formula in every case.

**Corollary 5 (a two-connected realization of every interaction graph).**
For any connected loopless simple Q of order r>=1, take r copies of B
and, for each edge ij of Q, add both L_i--P_j and L_j--P_i. The resulting
graph G_Q is two-connected and bipartite, with

    |V(G_Q)|=14r,
    Gamma(G_Q)=alpha(G_Q)=7r,
    beta_2(G_Q)=7r+alpha(Q),
    SF_2(G_Q)=8r,
    SF_2(G_Q)-beta_2(G_Q)=tau(Q).

Its maximum degree is max(3,2+Delta(Q)). The assertions for r=1 concern
the single broken-incidence graph, so the maximum degree is three there.
All added edges are point-to-line. The unchanged shift-zero matching
gives alpha(G_Q)=7r, and the existing bipartite identity gives Gamma=alpha.
Each block has a spanning cycle. After any vertex deletion every affected
block stays connected, and every edge of Q retains at least one of its
two interfaces: the paired interfaces have distinct endpoints in either
block. Contracting the remaining connected blocks therefore still gives
a connected graph. This proves two-connectivity, including r=1 by the
block's spanning cycle. The parameter identities follow from Theorem 3
and the interaction formula.

This realizes a classical vertex-cover parameter as the exact star-forming
gap in two-connected bipartite graphs. It is an algebraic construction;
no new complexity-priority claim is made. It does not prove hardness of
SF_2 on this class, where SF_2 is explicitly 8r.

