# Exact parameters and zero-expense completion in extended double covers

For every finite simple graph H, we prove that the upper star-forming number,
dissociation number, sub-quorum colouring number and representative optimum
of its extended double cover are all equal to 2n-nu(D(H)). The common value
has an ordinary bipartite matching certificate. The star-forming upper bound
counts deletion witnesses with a single capacity of two per empty rung.
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

The empty set is allowed, so delta>=0. Here N_H(X) is the set of vertices
adjacent to some member of X; it can intersect X. A
dissociation set induces maximum degree at most one; beta_2 is its maximum
size. A partial colouring is sub-quorum if, at every coloured vertex, at
least half of the coloured vertices in its closed neighbourhood have its
colour; psi_sq is the largest number of nonempty colours in such a colouring.
A feasible representative pair consists of a matching M and a set T
disjoint from its endpoints P, such that every t in T has at most one
neighbour in T union P. The quantity Omega maximizes |T|+|M|. T may use both
colours. Sahbi's representative reduction supplies

beta_2(G) <= psi_sq(G) <= Omega(G).                        (1)

For clarity, the two reductions have direct proofs. Give each vertex of a
dissociation set its own colour. Its coloured closed neighbourhood has size
at most two, so that vertex alone supplies at least half. Conversely, from
each colour class containing an edge retain one such edge; from each
edge-free colour class retain one vertex. A vertex of the latter type has
no same-colour neighbour in the original coloured support. Its sub-quorum
condition therefore allows at most one coloured neighbour, and hence at
most one neighbour in the retained set. The retained edges and vertices
give a feasible pair with one contribution per colour. The proof below
bounds every such pair and constructs an attaining dissociation set.

A set S is **2-star-forming** if every x outside S belongs to a not
necessarily induced K_(1,2) inside S union {x}. The exact local test is
that x has at least two neighbours in S, or has a neighbour in S with a
neighbour in S. SF_2 is the maximum size of an inclusion-minimal such set.
Formation is upward closed: when S is enlarged, every still-outside vertex
keeps a witnessing star. Thus testing every single deletion characterizes
inclusion-minimality. An empty graph has all four parameters zero.

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
the same deficiency: Lemma 1 gives at least the Hall deficiency, which
already equals the global maximum. The dissociation selection above is optimal. The
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

The proof also characterizes all optimal feasible representatives through
an exact nonnegative remainder. With I the TT indices and a,b,u,v as above,

    n+delta(H)-(|T|+|M|)
      = [delta(H)-(|I|-|N_H(I)|)]
        + [b-|N_H(I)|] + (v-u)/2.                           (6a)

Each summand is nonnegative. Thus the pair is optimal exactly when I is
critical, the ZZ rungs are exactly N_H(I), and u=v. In the last condition
the TP-to-PZ injection is a bijection. This criterion allows both colours
in T and does not require M to be a subset of the rungs.

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

## 5. Exact upper star-forming number

**Theorem 4.** For every finite simple H,

    SF_2(E(H))=beta_2(E(H))=psi_sq(E(H))=Omega(E(H))
              =n+delta(H)=2n-nu(D(H)).                        (8)

More precisely, for each inclusion-minimal forming S let I_S consist of
the indices whose rungs are isolated edge components of E(H)[S]. Then
I_S is independent in H and

    |S| <= n+|I_S|-|N_H(I_S)|.                               (9)

**Proof.** We prove (9) by allocating all deletion witnesses on empty
rungs just once. Write N_A(v) for the neighbours of v in A. An outside
vertex fails formation exactly when it has no selected neighbour, or its
unique selected neighbour is isolated in the selected graph.

First suppose S is forming, both s and tau(s) belong to S, and an original
outside vertex x becomes unformed after deleting s. We claim tau(x) is
outside S too. Otherwise tau(x) remains selected: it cannot equal s, as
then x=tau(s) would already be selected. Failure at x forces

    N_(S minus {s})(x)={tau(x)},
    N_(S minus {s})(tau(x))=empty.                            (10)

If x is adjacent to s, symmetry makes tau(x) adjacent to the still-selected
tau(s), contradicting (10). If x is not adjacent to s, its selected
neighbours were unchanged. Formation before deletion therefore requires
tau(x) to have a selected neighbour before deletion, which by (10) can
only be s. Symmetry then makes x adjacent to tau(s), a still-selected
vertex different from tau(x), again a contradiction. This proves the claim:
every outside witness for an endpoint of a doubly selected rung lies on a
completely empty rung.

Fix now a minimal forming S. Let C index its doubly selected rungs and Z
its empty rungs. Put C_0=I_S and C_1=C minus C_0. Counting rungs gives

    |S|=n+|C_0|+|C_1|-|Z|.                                  (11)

Every neighbour of an index in C_0 is in Z, since a selected lift in an
adjacent rung would give one endpoint of this isolated selected edge a
second selected neighbour. Thus C_0 is independent and N_H(C_0) is a
subset of Z.

Every endpoint s of a C_1-rung lies in a three-vertex path inside S. If
its selected degree is at least two it is a star centre; otherwise its
only selected neighbour is tau(s), which has another selected neighbour
because their rung is not an isolated edge component. The newly omitted
s is therefore still formed after its deletion. Minimality forces some
original outside vertex x to fail. By the preceding claim, x is on an
empty rung. Let Q consist of the 2|C_1| endpoints of all C_1-rungs.

For each z in Z let W_z be the set of vertices in Q whose deletion is
witnessed by at least one of w_z,b_z. We prove

    |W_z|<=2,             W_z=empty if z belongs to N_H(C_0). (12)

If z has an H-neighbour c in C, both outside lifts have fixed forming
stars w_z-b_c-w_c and b_z-w_c-b_c. Deleting any selected vertex outside
{w_c,b_c} preserves both stars. Hence W_z is contained in this pair. If
c lies in C_0 neither of its endpoints belongs to Q, so W_z is empty.

If z has no H-neighbour in C, neither outside lift x=w_z or b_z is
adjacent to any member of Q. For x to witness a deletion s in Q, its
selected-neighbour set must stay fixed at a singleton {t}; two neighbours
would still form x, and zero could not have formed it before deletion.
The vertex t must have N_S(t)={s}, so deletion of precisely that s makes
t isolated. For fixed x both t and its unique selected neighbour s are
fixed. Each outside lift therefore witnesses at most one member of Q,
again proving the capacity two. This proves (12) in all cases.

Every member of Q has at least one outside witness. Counting unions via
the capacity bound, while reserving N_H(C_0), gives

    2|C_1| <= sum_(z in Z) |W_z|
             =sum_(z in Z minus N_H(C_0)) |W_z|
             <=2(|Z|-|N_H(C_0)|).

The same empty rung has total capacity two across all deletions; none
is charged separately for different centres or witness choices. Substitute
this inequality into (11) to obtain (9), and hence SF_2<=n+delta(H).

To attain it, take the dissociation set D constructed in Theorem 2 from
a deficiency-maximizing independent I, with R=V(H) minus (I union N_H(I)).
The graph H[R] has no isolated vertex: otherwise adding such a vertex
to I would increase its deficiency by one without enlarging N_H(I).
Each outside lift over N_H(I) is formed using a neighbouring selected
rung over I. Each outside black b_r over R has selected neighbours w_r
and w_(r') for some r' adjacent to r in R. Thus D is forming. Deleting
any selected vertex leaves that vertex unformed, because the induced
graph on D has maximum degree one and contains no three-vertex star.
D is therefore minimal forming and has size n+delta(H). This proves (8).
The empty graph follows directly from the definitions. QED.

For a maximum minimal forming set, (9) shows that I_S must itself attain
delta(H). In fact, (11) gives the exact nonnegative remainder

    n+delta(H)-|S|
      = [delta(H)-(|C_0|-|N_H(C_0)|)]
        + [|Z|-|N_H(C_0)|-|C_1|].                          (9a)

Among minimal forming sets, S is maximum exactly when C_0 is critical
and |C_1|=|Z minus N_H(C_0)|. In that event the sets W_z, for z outside
N_H(C_0), partition Q into pairs: equality at both steps of the capacity
count forces every such W_z to have size two and no deletion to occur in
two different W_z. This describes all equality cases within this graph
class, including maximum sets that contain stars. The theorem does not say
that every maximum minimal forming set
is a dissociation set. On the 2-by-4 ladder the four middle-column vertices
induce a square and form a minimal set of size four: each endpoint of the
square has its deletion witnessed by the adjacent outside end-column
vertex. There are two C_1-rungs and two empty rungs, each witnessing exactly
two deletions, so the capacity in (12) is sharp.

**Corollary 5 (Cartesian prisms).** If H is bipartite then

    SF_2(H square K_2)=beta_2(H square K_2)=psi_sq(H square K_2)
                     =Omega(H square K_2)=2 alpha(H).         (13)

This follows from (6) and (8). In particular the prism operation eliminates
the star-forming/dissociation gap of any bipartite base. For the ten-vertex
sharp gap block B with beta_2(B)=5 and SF_2(B)=6, its prism has all four
parameters equal to ten. For each d>=2 the hypercube Q_d has all four
parameters equal to 2^(d-1). For every ladder P_2 square P_k they equal
k if k is even and k+1 if k is odd. These are all-size consequences of
the witness-capacity proof, not extrapolations of finite computation.

## 6. Verification

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

The star-forming extension additionally tests every minimal forming set of
the small cover graphs, all its deletion witnesses, the empty-rung capacities
and the zero budget on neighbours of isolated selected rungs. The upper
bound for SF_2 comes from Theorem 4, independently of the representative
inequality (1); no general-graph assertion SF_2<=Omega is used.

## 7. Sources and scope

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
