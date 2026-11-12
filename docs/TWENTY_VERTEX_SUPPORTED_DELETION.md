# Supported deletion and exact upper star formation in the twenty-vertex family

12 November 2026.

For the two-connected bipartite family G_r constructed in
ROBUST_TWENTY_VERTEX_SUBCUBIC_GAPS.md, a supported-deletion argument proves

    SF_2(G_r)=12r, beta_2(G_r)=11r, |V(G_r)|=20r,
    SF_2(G_r)-beta_2(G_r)=r=|V(G_r)|/20,  r>=1.

The earlier beta number, topology and canonical minimal12r-set are unchanged.
The new result is the uniform SF upper bound, including every number of blocks.
It does not assert that1/20 is the sharp coefficient for subcubic graphs.
The unrestricted subcubic upper coefficient remains7/71.

## Supported deletion under arbitrary port attachment

Let K be a finite simple block with ports P, and form any finite simple G by
adding edges and vertices only at these ports. Additional port-to-port edges
are allowed; every nonport keeps exactly its original neighbourhood. Fix
C subset V(K). A vertex v is supported when:

1. v belongs to C minus P and has a neighbour in C;
2. every selected neighbour u of v has a neighbour in C minus {v};
3. every outside neighbour x of v has at least three neighbours in C, or
   exactly two with its other selected neighbour active in K[C].

If S is star-forming in G and C=S intersect V(K), deleting v preserves star
formation. The newly outside v retains an active selected neighbour by2.
An old outside neighbour of v retains two selected neighbours or one active
selected neighbour by3; if this neighbour was adjacent to v,2 preserves its
activity. An old outside vertex not adjacent to v can lose a star only if
v was a leaf at its selected centre u. As v is a nonport, u lies in K, and2
supplies a replacement selected leaf. Added port edges do not affect this
argument. No bipartiteness or degree bound is required for the ambient graph.

For fixed v, supportedness is upward closed in C. Old selected neighbours
keep replacements. A newly selected neighbour had, by3, a selected neighbour
other than v, so it too passes2. Outside counts only increase and active
alternatives remain active. Thus if every k-set in K has a supported vertex,
every minimal star-forming set in every permitted ambient G uses at mostk-1
vertices of K. For disjoint blocks, the bounds add with each block counted
once; an exterior of orderq adds at mostq. Attainment needs separate proof.

## The local thirteen-set lemma

Take F=H20 minus4--12 with ports4,12. Every selected set of size at least13
has a supported nonport. A complete written proof appears as Lemma
`lem:twenty-support` in `manuscript/twenty-supported-proof.tex`, included in
the working manuscript. Its classification uses the numberh of selected
helpers, owner countk, and omitted witness setD, with |D|=h+k-5.

The proof first treats owners safe on their square side, and counts the
omitted witnesses required to obstruct them. It then counts obstruction arrows
on the helper four-cycle: each omitted witness can obstruct at most one active
selected helper. For three selected helpers, the exact obstruction sets of
the ready owners are explicit singletons or triples. Their unions rule out
large owner occupancies. The remaining cases use local neighbour checks,
ending in an eight-row table when all helpers are selected. Every activity
check at an outside vertex with two selected neighbours is included.
This is a structural proof, not a conclusion extrapolated from enumeration.

Applying the ambient lemma to every block gives SF_2(G_r)<=12r. The canonical
minimal set of size12r from the earlier construction gives the reverse bound.
Combined with the port-avoiding dissociation optimum, this proves the exact gap.
The same local cap holds with arbitrary edges between ports, arbitrary shared
exterior neighbours, and restored portedges; it does not assert universal
attainment12r under those arbitrary attachments.

## Reproduction and provenance

Run `python3 -B scripts/check_twenty_supported_deletion.py` from the repository
root. It independently specifies F, scores every deletion test, checks all
77,520 thirteen-sets and the explicit case choices, every single-addition step,
the obstruction tables, and actual two-leaf stars in3,000 seeded port extensions.
Larger cyclic controls check internal neighbourhoods and explicit certificates;
they are not unrestricted large exact-SF optimizations. The preceding general
proof and complete local cases supply the all-order theorem.

The structural case argument was obtained through the Oracle broker and then
rewritten and checked locally. The separate independent review receipt records
its exact source hashes and execution scope. The all-helper optimization is a
separate general result in ALL_HELPER_EXACT_OPTIMIZATION.md. No new Lean
execution, email sending, journal/arXiv submission or October manuscript edit
is part of this work.
