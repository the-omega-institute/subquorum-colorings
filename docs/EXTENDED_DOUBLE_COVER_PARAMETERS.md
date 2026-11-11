# Exact parameters and zero-expense completion in extended double covers

For every finite simple graph H, we prove exact formulas for the dissociation
number, sub-quorum colouring number and representative optimum of its extended
double cover. The common value has an ordinary bipartite matching certificate.
The same symmetry extends the two-row zero-TH-expense construction to this
whole graph class, for arbitrary actual matchings and nonnegative weights.

## 1. Construction and parameters

Let H have vertex set {1,...,n}. Its **extended double cover** E(H) has white
vertices w_i and black vertices b_i, with w_i adjacent to b_j exactly when
i=j or ij is an edge of H. The edges w_i b_i are called rungs. This is the
standard construction described by Chen [1], who attributes it to Alon.
The involution tau exchanging w_i and b_i preserves adjacency, and every
vertex is adjacent to its image. H itself need not be bipartite.

The **ordinary double cover** D(H) has the same two sides, but has w_i b_j
only for edges ij of H: it does not include the rungs. Write nu for maximum
matching cardinality, and define

    delta(H) = max_{I independent in H} (|I|-|N_H(I)|).

The empty set is allowed, so delta>=0. Neighbourhoods are open. A
dissociation set induces maximum degree at most one; beta_2 is its maximum
size. A feasible representative pair consists of a matching M and a set T
disjoint from its endpoints P, such that every t in T has at most one
neighbour in T union P. The quantity Omega maximizes |T|+|M|. T may use both
colours. Sahbi's representative reduction supplies

    beta_2(G) <= psi_sq(G) <= Omega(G).                        (1)

The proof below bounds every feasible pair and constructs an attaining
dissociation set; it does not need a converse to (1).

## 2. A matching formula for the independent-set deficiency

**Lemma 1.** For every H,

    delta(H) = max_{X subset V(H)} (|X|-|N_H(X)|)
             = n - nu(D(H)).                                  (2)

**Proof.** For any X put I=X minus N_H(X). No vertex of I has a neighbour
in X, so I is independent and N_H(I) is contained in N_H(X) minus X. Hence

    |I|-|N_H(I)| >= |X minus N_H(X)|-|N_H(X) minus X|
                  = |X|-|N_H(X)|.

Since independent sets are also subsets, the two maxima agree. The
neighbourhood of X on the left side of D(H) is exactly the right copy of
N_H(X), so the matching-deficiency form of Hall's theorem gives the second
equality. QED.

For completeness, this also equals n-2 nu_f(H), where nu_f is the maximum
total weight of a fractional matching with nonnegative edge weights and
incident sum at most one at each vertex. A matching of size q in D(H)
gives a fractional matching of H of weight q/2: assign half for each
chosen directed copy of an edge. Conversely, a fractional matching x of H
gives weight x_ij on each of the two directed copies in D(H), a feasible
bipartite fractional matching of total weight 2 sum x_ij. Integrality of
bipartite maximum flow gives an ordinary matching of at least this size.
Thus nu(D(H))=2 nu_f(H). These are standard matching facts; (2) is proved
here to make the use of deficiency explicit.

## 3. Exact representative, colouring and dissociation values

**Theorem 2.** For every finite simple H, including the empty graph,

    beta_2(E(H)) = psi_sq(E(H)) = Omega(E(H))
                 = n+delta(H) = 2n-nu(D(H)).                  (3)

**Proof of the upper bound.** Fix a feasible (T,M) in E(H). Put P=V(M) and
Z=V(E(H)) minus (T union P). Classify each rung by its two endpoint labels
as TT, ZZ, TP, PZ, TZ or PP, ignoring their order. Let a,b,u,v be the
numbers of TT, ZZ, TP and PZ rungs. Rungs of the last two types contribute
zero to |T|-|Z|, so

    |T|-|Z|=2(a-b)+u-v,
    |T|+|M|=n+(|T|-|Z|)/2.                                  (4)

There is an injection from TP rungs to PZ rungs. In a TP rung let t be
its T endpoint and p=tau(t) its P endpoint. Its actual mate q is outside
this rung because t is not in P. Applying tau to actual edge pq gives
the edge t tau(q). Since t already has neighbour p in P, feasibility
forces tau(q) into Z. Thus q's rung is PZ. Two TP rungs cannot have the
same image rung: that rung has a unique P endpoint q, with a unique actual
mate p. Consequently u<=v. This uses each image resource at most once.

Let I be the set of indices of TT rungs. It is independent in H: if two
such indices were adjacent, a T vertex would have its rung neighbour and
another T neighbour. Every rung whose index lies in N_H(I) is ZZ, because
both its vertices see a selected vertex in a TT rung, and each of those
selected vertices already has its rung neighbour in T. Thus b>=|N_H(I)|.
Equations (4) give

    |T|+|M| <= n+a-b <= n+|I|-|N_H(I)| <= n+delta(H).          (5)

**Attainment.** Choose an independent I attaining delta. Select both lifts
of I, no lift of N_H(I), and just the white lift of every remaining index.
There are no H edges from I to the remaining indices. The only selected
edges involving lifts of I are their rungs, because I is independent.
The other selected vertices are all white and have no edges among them.
The selection therefore induces disjoint rung edges and isolated vertices,
and its size is

    2|I|+n-|I|-|N_H(I)|=n+delta(H).

This proves the matching lower bound for beta_2; (1) and (5) complete (3).
For n=0 all sets, matchings and values are empty or zero. QED.

### Constructive and structural consequences

An ordinary maximum matching in D(H) provides both sides of the certificate.
Start alternating reachability at its unmatched left vertices. If X,Y
are the reached left and right indices, then Y=N_H(X) and
|X|-|Y|=n-nu(D(H)). The construction in Lemma 1 gives I=X minus Y with
the same deficiency. The dissociation selection above is optimal. The
matching together with the minimum vertex cover (left outside X) union Y
certifies its own maximum cardinality. Thus the exact parameter and an
attaining set are computable in polynomial time on this class.

In particular the common value is n if and only if H has a fractional
perfect matching (incident sum exactly one at every vertex). For a
nonempty d-regular H with d>=1, assigning 1/d to every base edge supplies
one. The case of isolated vertices is included by (3), not by this regular
specialization. If H is edgeless, E(H) is n disjoint edges and (3) gives 2n.

When a fractional perfect matching x exists, its edge ij also supplies a
square on the two rungs i,j of E(H), with square weight x_ij. Each cover
vertex has total incident square weight one. This recovers the fractional
square dissociation cap n; the representative proof (5) supplies the
additional colouring bound.

If H is bipartite then E(H) is isomorphic to the Cartesian prism H square
K_2: within each fibre choose which layer is white according to the base
bipartition. Koenig's theorem and (2) give the useful specialization

    beta_2(H square K_2)=psi_sq(H square K_2)=Omega(H square K_2)
                        =2(n-nu(H))=2 alpha(H).               (6)

For H=P_k this recovers the closed-ladder value k for even k and k+1 for
odd k. For H=Q_(d-1) with d>=2 it recovers the hypercube value 2^(d-1).
These are recoveries of previously established families, not separate
novelty claims. The prism assertion (6) requires bipartite H; E(H) is
bipartite even when H is not, but the Cartesian prism then is not.

For another direct example, H=K_3 gives E(H)=K_(3,3) and common value three.
Its unweighted biadjacency matrix has no orthogonal signing: the inner
product of any two rows of a 3-by-3 sign matrix is an odd integer, hence
nonzero. Thus the equality criterion above applies to graphs outside the
orthogonal-signing sufficient condition.

## 4. Zero TH expense for arbitrary actual matchings

Fix any actual matching M in E(H), with endpoints P and remaining terminals
Q. Select T among the white Q vertices with at most one P neighbour per t.
For any full auxiliary matching N, its tagged union with M has alternating
terminal paths, each with one white and one black Q endpoint, and P-only
cycles. TH paths start in T; HH paths start at other white Q vertices.
The expense f(N) is the sum of nonnegative actual-edge weights on TH paths;
HH paths and cycles are free, including common actual/auxiliary edges.

**Theorem 3.** Every such instance in E(H) has a full auxiliary matching
with every selected vertex directly paired to a black Q vertex. Thus

    min_N f(N)=0.                                             (7)

**Proof.** Begin with the rungs. A bad rung has w_j in T and b_j in P.
The actual mate of b_j is w_i for i!=j. Symmetry supplies edge w_j b_i.
Since w_j already has the occupied neighbour b_j, feasibility forces b_i
to be in Q. Replace rungs i,j by actual edge w_i b_j and edge w_j b_i.

All these swaps are disjoint: bad indices have their white vertex in Q,
whereas mate indices have it in P; these two kinds cannot coincide. The
actual matching makes mate indices of distinct bad rungs distinct. Use all
swaps and every untouched rung to obtain a perfect N. A selected vertex
in a bad rung gets the black Q partner b_i. A selected vertex in a nonbad
rung cannot be a mate-rung white vertex and keeps its black Q rung partner.
All TH paths are therefore direct and cost zero. Nonnegativity proves
optimality, for arbitrary weights, including zero. QED.

More generally the same proof applies to any bipartite graph with an
adjacency-preserving colour-exchanging involution tau such that v is
adjacent to tau(v) for every v. Its orbits give exactly the E(H) construction
for a quotient graph H. Recognition from such a supplied involution is
immediate; no graph-isomorphism complexity claim is needed.

## 5. Verification and the separate star-forming question

`scripts/extended_double_cover.py` returns an ordinary matching, equal-size
vertex cover, a Hall-deficient set, the critical independent set and the
attaining dissociation set. It also returns the rung injection for a given
feasible pair and the zero-expense full auxiliary matching for a white-only
selection. Matching uses iterative augmenting paths, not a recursion limit.

`scripts/check_extended_double_cover.py` constructs the cover independently,
enumerates literal selected subsets and representative pairs on small
graphs, walks physical alternating paths to score the full zero-expense
matchings, and verifies the matching/vertex-cover and Hall certificates on
larger graphs. It has no helper-module dependency beyond the implementation
under test. Finite enumeration checks implementations; the proofs above
establish the arbitrary-size statements. No new Lean verification is claimed.

Whether the **upper star-forming number** SF_2(E(H)) also equals (3) is a
separate question at this stage. Its definition maximizes the size of an
inclusion-minimal set S such that each x outside S lies in a not-necessarily-
induced K_(1,2) inside S union {x}. Neither (1) nor the representative proof
is an upper bound on SF_2. Finite equalities found by the checker are
explicitly recorded as observations, not a general proof. The general
rectangular-grid equality involving SF_2 remains separate as well.

## Sources and scope

[1] Zhibo Chen, “Spectra of extended double cover graphs,” *Czechoslovak
Mathematical Journal* 54 (2004), 1077–1082.
[doi:10.1007/s10587-004-6452-2](https://doi.org/10.1007/s10587-004-6452-2).
The [primary full text](https://dml.cz/handle/10338.dmlcz/127952) explicitly
defines this construction and records the supplied-matching characterization.

The construction, Hall deficiency, fractional matching and Koenig identities
are standard. This note supplies complete proofs of the parameter and
completion statements used here. A full priority comparison for these
specific parameter identities has not been completed; no first-in-literature
claim is made. The result gives a structural equality class beyond the
previous signed-matrix sufficient condition. It does not assert that every
wider rectangular grid has the required involution, or improve the universal
5/6 coefficient for mixed-direction representative pairs.
