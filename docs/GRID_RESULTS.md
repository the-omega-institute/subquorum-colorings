# From hypercubes to uniform grid bounds

Wenlin Zhang and Haobo Ma, The Omega Institute

We begin with the proof of Sahbi's hypercube conjecture and develop two
directions suggested by it: rectangular grids and the structural conditions
for equality between the sub-quorum coloring number and the dissociation
number. This note summarizes the current results and links their proofs.

## Starting point and notation

For every n >= 2, the hypercube satisfies

$$
\psi_{\rm sq}(Q_n)=\beta_2(Q_n)=2^{n-1}.
$$

Sahbi established the dissociation-number identity and conjectured the
coloring-number identity. Our proof of the latter uses Huang's signed
adjacency matrix to obtain a boundary injection; it is formalized in Lean 4.
The written argument also gives a boundary matching covering the selected
edge-free color representatives. The [manuscript](../manuscript/paper.tex)
contains this proof and the structural results below.

For a graph G, a feasible representative pair (T,M) consists of a matching
M and a disjoint vertex set T such that every t in T has at most one neighbor
in T union V(M). Sahbi's parameter Omega maximizes |T|+|M| over these pairs,
and his representative reduction gives

$$
\beta_2(G)\le\psi_{\rm sq}(G)\le\Omega(G).
$$

For the rectangular grid G_(m,n)=P_m square P_n, write

$$
F(m,n)=\max\left\{
\left\lceil\frac m2\right\rceil\left\lceil\frac{2n}3\right\rceil+
\left\lfloor\frac m2\right\rfloor\left\lfloor\frac n3\right\rfloor,
\left\lceil\frac n2\right\rceil\left\lceil\frac{2m}3\right\rceil+
\left\lfloor\frac n2\right\rfloor\left\lfloor\frac m3\right\rfloor
\right\}.
$$

Sahbi's periodic constructions attain F(m,n) with dissociation sets.
The full grid target is psi_sq(G_(m,n))=F(m,n).

## Uniform results for all dimensions

**Dissociation number.** For all positive m,n,

$$
\beta_2(P_m\square P_n)=F(m,n).
$$

Our independent proof uses the rigid equality case on a two-row ladder.
For odd width, the row counts give an odd-integer profile. At each integer
level, path-neighborhood expansion controls its positive entries; the only
positive defect is the full alternating path joining the two endpoints.
This yields the formula uniformly, including both odd side lengths.

**One-direction matchings.** Let Omega_H and Omega_V restrict M to horizontal
and vertical edges, respectively. For all positive m,n,

$$
\Omega_H(G_{m,n})=\Omega_V(G_{m,n})=F(m,n).
$$

Restricting a horizontal matching to a row or two adjacent rows cuts no
matching edge, so the same profile argument applies. On an odd-width closed
ladder, equality forces M to be empty and T to consist of both vertices in
every odd column. Consequently, any coloring exceeding F by d needs at least
d classes with horizontal but no vertical edges, and at least d classes
with vertical but no horizontal edges.

[Complete row-profile, ladder and directional proofs](GRID_PROFILE_PROOF.md).

## Mixed directions on even-by-even rectangles

**Five-sixths bound.** For all positive even m,n and every feasible (T,M),

$$
|T|+\frac56|M|\le\frac{mn}{2}.
$$

Partition the rectangle into 2-by-2 tiles. Saturated tiles constrain the
corners of adjacent matching attachments. The remaining matching edges form
a graph with capacities 0, 1 or 2. Pairing its real and unused ports produces
paths between zero-capacity leaves and slack terminals. The excess

$$
q=|T|+|M|-mn/2
$$

is exactly the number of leaf-to-leaf paths minus the number of slack-to-slack
paths. The grid geometry lets us charge every two- or three-edge leaf path
to an internal matching edge or an available slack path, without double
counting. Keeping the internal-edge contribution yields

$$
mn/2-|T|\ge5q,\qquad |M|\ge6q.
$$

Thus any coloring exceeding F by d >= 1 requires at least 6d color classes
containing an edge. The full bound already holds when |M| <= 5 or
|T| >= mn/2-4. There is also an objective-preserving normalization that removes
every capacity-one fork, by a promotion or a matching flip.

[Complete residual-geometry and five-sixths proof](GRID_ABSORPTION_PROOF.md).

## Exact strips and structural obstructions

For widths 8, 9, 10 and 11, exact transfer certificates establish

$$
\beta_2(G_{m,n})=\psi_{\rm sq}(G_{m,n})=\Omega(G_{m,n})=F(m,n)
\quad\text{for every }n\ge1.
$$

The certificate is a translation of the full transfer vector, which
propagates by induction to every length. Two integer implementations
independently reconstruct the certificate endpoints.

For the structural question, the signed boundary argument proves equality
on bipartite graphs with an orthogonal signed adjacency matrix, and is
compatible with Cartesian products. In the other direction, attaching a
fixed double-star gadget at every vertex of a nonempty base graph F gives

$$
\beta_2(R(F))=4|V(F)|+\beta_2(F),\qquad
\psi_{\rm sq}(R(F))=5|V(F)|.
$$

Taking F=P_k gives trees of maximum degree three with gap floor(k/3).
Equality therefore needs a stronger condition than bounded tree degree.
The equality class is also not hereditary.

## Next mathematical targets

The general mixed-direction coloring formula remains open. On even-by-even
rectangles the target is to strengthen 5/6 to 1. The short-path argument
suggests studying how longer leaf paths can be compensated by the surrounding
slack, which may lie in a different residual component. Odd side lengths
add boundary terms to this accounting.

For structural characterization, the next goal is to identify sufficient
conditions beyond the signed-matrix class and test them against the grafted
trees. These questions connect the completed hypercube proof with the two
broader directions.

## Evidence and attribution

The hypercube coloring identity is Lean-verified. The uniform grid results
have written proofs and exact finite checks, including explicitly constructed
short-path configurations. The [reproduction guide](REPRODUCE.md) gives the
commands and coverage. Formalization of these newer results is a subsequent
step.

Sahbi's [Sub-quorum colorings of graphs](https://arxiv.org/abs/2609.25128v1)
supplies the conjectures, representative reduction, grid constructions and
strip method. The dissociation formula is presented here as an independent
proof, with reusable equality conditions. Its relationship with earlier
path-cover results, particularly Bresar et al., *On the vertex k-path cover*,
Discrete Applied Mathematics 161 (2013), 1943-1949, and Jakovac and Taranenko,
*On the k-path vertex cover of some graph products*, Discrete Mathematics 313
(2013), 94-100, still needs a full comparison. The tree results likewise
require comparison with the earlier caterpillar work cited by Sahbi.
