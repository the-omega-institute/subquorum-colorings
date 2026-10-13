# Unbounded star-forming gaps in two-connected bipartite graphs

13 October 2026. We prove the ten-vertex counterexample directly and amplify
its gap in two-connected bipartite graphs of maximum degree four.
Every conclusion below has a general proof; finite controls check the construction.

## Definitions and the local test

For a finite simple graph G, beta_2(G) is the maximum size of a vertex set
inducing maximum degree at most one. A set S is 2-star-forming if each x
outside S belongs to a copy of K_{1,2} in G[S union{x}]. Copies are not
required to be induced. SF_2(G) is the largest cardinality of an
inclusion-minimal such set.

Write d_S(x)=|N(x) intersect S|. The condition is precisely

    for every x outside S:
    d_S(x)>=2, or there is u in N(x) intersect S with d_S(u)>=1.       (1)

In the first case x is the centre; in the second x is a leaf and u the
centre. The second leaf is in S, hence distinct from x. This proves both
directions of (1). Star formation is upward closed: a witnessing star
survives enlargement of S for every vertex still outside. Thus inclusion
minimality is equivalent to failure of every single-vertex deletion.

## A global bound used in the exact upper proof

For minimal S put H={s in S:d_S(s)>=2}. Every s in H has a witness x outside
S for failure after deleting s. The removed vertex s cannot itself fail,
because its two selected neighbors still form a star centred at s.

No outside vertex witnesses failure for two distinct members s,t of H.
If x did so, every star through x before deletion would contain both s,t.
Such a star has vertex set{x,s,t}, so x is adjacent to at least one, say s.
Since d_S(s)>=2, s has another neighbor y in S distinct from t. Then x,s,y
is a star avoiding t, a contradiction. Distinct members of H consequently
have disjoint nonempty witness sets, yielding |H|<=|V(G) minus S|.

S minus H induces degree at most one. Hence

    2|S|-|V(G)| <= |S|-|H| <= beta_2(G),
    SF_2(G) <= floor((|V(G)|+beta_2(G))/2).                         (2)

This is the existing global witness bound, recalled with proof.

## Exact ten-vertex example

Let A={a1,...,a5}, B={b1,...,b5}, with no edges inside the parts and
cross-edge matrix

    1 1 0 0 1
    1 1 0 1 0
    0 0 0 1 1
    0 1 1 1 1
    1 0 1 1 1

Call this graph H0 and put S0={a1,a2,a3,b1,b2,b3}. The matrix is symmetric,
so exchanging a_i and b_i is an automorphism. Vertex degrees on either
side are (3,3,2,4,4). The graph has 16 edges.

**Proposition 1.** beta_2(H0)=5 and SF_2(H0)=6.

**Dissociation proof.** A is independent, so beta_2>=5. To exclude a
six-set, let p,q be its sizes on A,B. By the side-swap symmetry assume p<=q.
The only splits are (1,5), (2,4), (3,3). For (1,5), the selected A vertex has
at least two selected neighbors. For (2,4), omission of one B vertex can
reduce degree to at most one only for a3; two distinct selected A vertices
cannot both be a3. For (3,3), omission of two B vertices cannot reduce
degree four to at most one, so the selected A vertices must be a1,a2,a3.
Both a1 and a2 then require two omitted neighbors. Their common neighbors
are exactly b1,b2, so those must be the omitted B vertices. But a3 has
both b4,b5 selected, again impossible. No six-set is dissociation; larger
sets contain six-sets. This proves beta_2=5.

**Star formation and minimality.** Each vertex outside S0 has two selected
neighbors:
a4 sees b2,b3; a5 sees b1,b3; b4 sees a2,a3; b5 sees a1,a3.
Thus (1) holds with each outside vertex as centre. Deletion failures are

| Deleted | Failure vertex | Its remaining selected neighbors |
|---|---|---|
| a1 | b5 | a3 |
| a2 | b4 | a3 |
| a3 | a3 | none |
| b1 | a5 | b3 |
| b2 | a4 | b3 |
| b3 | b3 | none |

a3 and b3 are isolated in H0[S0]. Therefore the sole neighbor in each
nonempty row has no selected neighbor and cannot serve as centre. All six
deletions fail (1). Upward closure proves inclusion-minimality and SF_2>=6.

**Upper bound without enumeration.** Equation (2) gives SF_2<=7. Suppose
a minimal star-forming set S has size seven. Its side sizes, up to symmetry,
are (2,5) or (3,4). For (2,5), B is already star-forming, since every A vertex
has degree at least two; it is a proper subset of S, a contradiction.

For (3,4), exactly two A vertices and one B vertex are absent. At most one
selected A vertex can have selected degree at most one, since only a3 has
original degree two. On the B side, b4,b5 cannot have selected degree at
most one, since they have original degree four and lose at most two
neighbors. The only possible low-degree B vertices are b1,b2,b3. They
cannot all be low: making both b1,b2 low requires the omitted A pair to
be {a1,a2}, their only common neighbor pair, leaving both a4,a5 selected
and giving b3 selected degree two. Thus there are at most two low-degree
B vertices and at most three low-degree selected vertices in total.
At least four members of S have selected degree at least two, but only
three vertices lie outside S. This contradicts witness injectivity above.
No minimal seven-set exists; the bound excludes larger sizes. Hence SF_2=6.
QED.

## Additivity

**Proposition 2.** For finite disjoint graphs G1,...,Gr and positive k,

    beta_k(disjoint union G_i)=sum beta_k(G_i),
    SF_k(disjoint union G_i)=sum SF_k(G_i).                         (3)

A k-star is connected, so a star containing an outside vertex lies in its
summand. A set is k-star-forming exactly when all restrictions are. Its
inclusion-minimality is equivalent to minimality of each restriction,
because any proper global subset shrinks at least one restriction.
Taking maxima proves the SF equality. Selected degrees are local to
summands, giving the beta equality. This also handles empty summands.
For r copies of H0, the parameters are 5r and 6r, with gap r.

## Connected and two-connected amplification

For r>=2 take r disjoint labelled copies H_i of H0. Add the cyclic edges

    b1^(i) -- a1^(i+1),   i=0,...,r-1, indices modulo r.            (4)

No original edge is removed. Denote the resulting graph C_r, and let
S_r be the union of the six-sets S0 in the copies.

**Theorem 3.** For every r>=2, C_r is a two-connected bipartite graph with
10r vertices, 17r edges, minimum degree two and maximum degree four, and

    beta_2(C_r)=5r,
    SF_2(C_r)>=6r,
    SF_2(C_r)-beta_2(C_r)>=r=|V(C_r)|/10.                          (5)

**Graph properties.** Each added edge joins a B vertex to an A vertex.
The endpoint degrees of a1,b1 rise from three to four; all other degrees
are unchanged. Edges in (4) are distinct even when r=2. Thus the order,
size, degree bounds and bipartiteness follow.

Each H_i contains the Hamilton cycle

    a1,b1,a2,b2,a4,b3,a5,b4,a3,b5,a1.

Hence each copy stays connected after deletion of any one vertex. The
cyclic interfaces connect all copies. Removing one vertex destroys at
most one interface edge, because the two ports a1,b1 in a copy are
distinct. A cycle with at most one edge removed is connected. For r=2
there are two distinct interfaces and at least one remains. All nonempty
copy remnants are consequently connected through the surviving interfaces.
This proves C_r minus any vertex is connected, and proves two-connectivity.

**Dissociation.** Every dissociation set restricts to one in each induced
H_i, and hence has at most 5r vertices by Proposition 1. All A vertices form
an independent set of size 5r. Therefore beta_2=5r.

**Minimal star formation.** All outside vertices retain their two selected
neighbors from their copy, so S_r is star-forming. The new edges have
endpoints only among a1,b1 in the selected sets. The four outside failure
vertices a4,a5,b4,b5 have exactly the same selected neighbors after each
local deletion as in the table above. The possible sole remaining
centres a3,b3 remain isolated in S_r and are untouched by (4). Deleting
a3 or b3 likewise leaves that vertex with no selected neighbor.
Each of the 6r selected vertices therefore retains its original deletion
failure witness. S_r is inclusion-minimal and has size 6r. This proves (5).
QED.

The theorem gives an unbounded gap in a bounded-degree, two-connected
bipartite class, without disjoint components or attachment leaves.
Equation (2) also gives SF_2(C_r)<=7r. We do not infer exact SF_2(C_r)=6r
from the existence of this one minimal set.

Deleting one cyclic interface produces a connected chain with 10r vertices,
17r-1 edges and the same parameter bounds; all minimality proofs still hold.
More generally any additional edges only between the selected a1,a2,b1,b2
vertices of different copies preserve the displayed failure witnesses, as
long as bipartiteness is retained. Degree bounds require explicit control
of port usage.

## Scope and next questions

Conjectures 4.1, 4.2 and 7.2 of arXiv:2610.03785v2 fail by Proposition 1.
Equation (5) establishes unbounded connected-bipartite gaps, with two-connectivity
and maximum degree four. It does not classify smallest-order obstructions,
settle computational complexity, or prove a rectangular-grid identity.
The exact value of SF_2(C_r) and extremal sharpness of (2) remain questions.

The grid bridge psi_sq<=SF_2 needs a grid-specific proof: the earlier
six-vertex double star has beta_2=SF_2=4<psi_sq=5. General bipartiteness alone
cannot establish that bridge.

## Verification and reproducibility

The existing pipeline Lean source checks literal definitions and the separating
bounds for H0. The new [Amplification.lean](../formal/StarForming/Amplification.lean)
proves literal two-leaf-star/local-test equivalence, the single-deletion
minimality implication, and preservation of all deletion witnesses for any
index type and any interface relation linking b1 to a1. It proves bipartiteness
for these graphs. The concrete `cycle_minimal_card` theorem defines the modular
cyclic graph and proves that its displayed set is inclusion-minimal and has
6r vertices for every r. These declarations passed Lean 4.33.0 locally, with
only the standard axioms propext, Classical.choice and Quot.sound.

The exact beta_2 and SF_2 upper proofs, general additivity, degree bounds and
two-connectivity above are written proofs, not claims of completed Lean
formalization. Local finite tables in the Lean proof certify fixed base-graph
facts; the family theorem itself is proved for an arbitrary index type.

The independent Python checker compares literal centre/two-leaf stars with
the local predicate on all 1024 subsets of H0, tests all proper subsets for
minimality, and returns beta_2=5, SF_2=6, with 37 minimal sets of size four,
48 of size five and one of size six. It also checks the chain and cyclic
families for every r=2,...,30 (58 graphs), including all single deletions and
all vertex deletions for the two-connectivity control.

A separate C++ checker exhausts all 2^20 subsets of C_2 and returns
beta_2(C_2)=10 and SF_2(C_2)=12. Its minimal-set counts by size are
6:18, 7:276, 8:1130, 9:1704, 10:1100, 11:36, 12:1. This exact two-copy result
does not determine SF_2(C_r) for general r.

Reproduce the controls with:

```sh
python3 scripts/check_starforming_gap.py --output output/starforming-gap-controls.json
clang++ -std=c++17 -O2 scripts/check_starforming_two_blocks.cpp -o /tmp/sahbi-two-block-check
/tmp/sahbi-two-block-check
python3 scripts/check_starforming_formal.py --lean /path/to/lean-4.33.0 \
  --package-cache /path/to/matching/.lake/packages \
  --output output/starforming-formal-check.json
```

The Lean runner reuses a matching package cache read-only and builds only the
new module and its axiom audit. It does not change upstream code or CI.
