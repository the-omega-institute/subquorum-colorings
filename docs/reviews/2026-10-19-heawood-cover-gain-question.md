Find a non-enumerative proof, or a reproducible counterexample, for this single claim: every connected two-sheeted cover H of the Heawood graph has dissociation number beta_2(H)>=15.

Definitions: a dissociation set induces maximum degree at most one. The Heawood graph is the incidence graph of the seven nonzero vectors in F_2^3 and the seven triples {a,b,a+b}; it has 14 vertices and beta_2=7. A two-sheeted graph cover is an arbitrary binary-sign lift of its 21 edges, modulo vertex sheet switching. A nonzero cohomology class gives a connected 28-vertex cubic bipartite cover.

We have a complete general proof that minimal two-star-forming selections pull back through triangle-free graph covers. The base has a minimal eight-set and the universal cubic bound is SF_2<=floor(3n/5), so every two-sheeted Heawood cover has exact SF_2=16. The current question would prove its connected SF-beta gap is at most one by a structural argument.

Discovery only: normalize all signs on a fixed spanning tree to zero. All 255 nonzero choices on eight cotree edges were checked using the exact bipartite formula below: beta=15 in143 cases and16 in112. This is not the proof being requested. The disjoint zero-sign cover has beta14. A cyclic lift twisting only one base incidence attains15.

Useful exact formula: for a bipartite graph with equal parts L,R of size N and A subset L, let P(A) be the set of distinct A-vertices having a right neighbor whose selected neighborhood in A is exactly that one vertex. Then
beta_2=N+max_A[|A|-|N(A)|+|P(A)|].
For fixed A select all right vertices with zero A-neighbors and one from every nonempty private-owner group. In a cubic graph, if r_j counts right vertices having j A-neighbors, the bracket is |P(A)|-(2r_1+r_2)/3.

A general connected-cover strict-increase principle is false: even prisms C_m square K_2 have beta=m, and C_(km) square K_2 is a connected k-sheeted cover with beta=km. The m square faces each permit at most two dissociation vertices and each vertex is counted twice. Thus an answer must use the Fano/Heawood geometry, not connectedness alone.

We seek a readable structural proof, perhaps showing that beta14 forces all cycle signs to be switch-trivial. A generated table of all255 signatures, a solver optimum for each, or an unproved orbit enumeration is not sufficient. Finite local lemmas proved by geometry or linear algebra are welcome. If unable to close it, identify the exact unproved implication instead of presenting a conjectural step as proved. Do not infer a bound for all higher-sheeted covers from the two-sheeted claim.
