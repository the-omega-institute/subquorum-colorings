# Uniform rectangular-grid beta_2 formula and the remaining coloring bridge

Date: 2026-09-27.

**Status:** complete ordinary mathematical proof of beta_2(G_(m,n))=F(m,n) for every positive m,n. Independently derived in this research session; no worldwide priority claim, independent referee approval, or Lean verification. The universal psi_sq/Omega upper bound remains UNPROVED. This companion to `grid-strips-2026-09-27.md` does not supersede its stronger three-parameter strip results.

## 1. Exact interfaces

Let G_(m,n)=P_m square P_n. A dissociation set induces maximum degree at most one; beta_2 is its maximum size. A feasible pair (T,M) consists of a matching M and a disjoint set T, each of whose vertices has at most one neighbor in A=T union V(M). Omega is the maximum of |T|+|M|.

Define

\[
F(m,n)=\max\left\{
\left\lceil\frac m2\right\rceil\left\lceil\frac{2n}3\right\rceil+\left\lfloor\frac m2\right\rfloor\left\lfloor\frac n3\right\rfloor,
\left\lceil\frac n2\right\rceil\left\lceil\frac{2m}3\right\rceil+\left\lfloor\frac n2\right\rfloor\left\lfloor\frac m3\right\rfloor
\right\}.
\]

Sahbi [S], Proposition 5.2 and Lemma 5.4, supplies

\[
F(m,n)\le\beta_2(G_{m,n})\le\psi_{sq}(G_{m,n})\le\Omega(G_{m,n}).
\]

Put g(k)=k-2 floor(k/3)=2 ceil(2k/3)-k. Then

\[
2F(m,n)-mn=\max\{(m\bmod2)g(n),(n\bmod2)g(m)\}. \tag{1}
\]

To verify (1), use ceil(2k/3)=k-floor(k/3), and write ceil(m/2), floor(m/2) in terms of m and its parity. Also g(k)>0 for k>=1.

The trureturing source interface [T] is its source-faithful partial coloring and single-vertex/edge representative reduction. The cube proof then uses Huang's operator to bound the boundary. Here the new counting step is path-neighborhood expansion at every integer level of a row profile. The cube operator itself is not asserted to work on rectangles.

## 2. The two-row equality case is rigid

**Lemma 2.1.** A dissociation set in the 2-by-n ladder has at most n vertices for even n and n+1 for odd n. In the odd case, equality forces both vertices of every odd-numbered column to be selected and all even columns to be empty.

**Proof.** Any three vertices in a 2-by-2 square induce a vertex of degree two. Thus each square contains at most two selected vertices. Pair columns into squares; for odd n leave the last column, giving the stated bounds.

At equality for odd n, the last column is full and every square has two selected vertices. The two selected vertices in the last column already have their vertical partner, so column n-1 is empty. Saturation of the last square forces column n-2 to be full. Repeat backwards. The case n=1 is immediate, and the displayed pattern is feasible.

**Corollary 2.2.** For odd n, let x_i be the row counts of a dissociation set in G_(m,n). Then

1. x_i<=ceil(2n/3);
2. x_i+x_(i+1)<=n, unless both counts equal (n+1)/2;
3. three consecutive counts cannot all equal (n+1)/2.

**Proof.** Each row is a path and cannot contain three consecutive selected vertices, proving item 1 by partition into triples. Lemma 2.1 proves item 2. If item 3 failed, both adjacent ladders would attain equality and their odd columns would contain three vertically consecutive selected vertices, a contradiction.

The equality characterization, not just the numerical ladder bound, is essential.

## 3. Exact path-neighborhood defect

**Lemma 3.1.** If P is independent in the path on 1,...,m, then |N(P)|>=|P|, except when m is odd and P={1,3,...,m}. In that exceptional case |N(P)|=|P|-1.

**Proof.** Split P into maximal runs in which successive selected indices differ by two. A run of k indices has k+1 neighbors, minus one for each endpoint of the whole path touched by that run. Different runs have disjoint neighborhoods, since their separating gap is at least three. Every run has at least k neighbors unless it touches both path endpoints. Such a run forces m odd and consists of all odd indices, with no other run present. This also handles the empty set and m=1.

## 4. Odd-integer profile theorem

**Theorem 4.1.** Let A>=1 be odd, and let a_1,...,a_m be odd integers at most A. Suppose

\[
a_i+a_{i+1}\le0\quad\text{unless }a_i=a_{i+1}=1, \tag{2}
\]

and no three consecutive entries are positive. Then

\[
\sum_i a_i\le
\begin{cases}
g(m),&m\text{ even},\\
\max\{A,g(m)\},&m\text{ odd}.
\end{cases} \tag{3}
\]

No lower bound on the negative entries is required.

**Proof.** Let sigma_i be the sign of a_i. For each integer h>=1 set

\[
P_h=\{i:a_i\ge2h+1\},\qquad N_h=\{i:a_i\le-(2h+1)\}.
\]

By (2), P_h is independent and N(P_h) is contained in N_h. Lemma 3.1 implies |P_h|-|N_h|<=0, except possibly when m is odd, P_h is all odd indices, and N_h all even indices. In that case the difference is one. These are the only positive differences possible.

The finite integer level decomposition is

\[
\sum_i a_i=\sum_i\sigma_i+2\sum_{h\ge1}(|P_h|-|N_h|). \tag{4}
\]

If no level has a positive difference, the right side is at most the sign sum. At most ceil(2m/3) signs are positive, because three consecutive positive signs are forbidden. Thus the sum is at most 2 ceil(2m/3)-m=g(m).

If some level has a positive difference, its exceptional configuration forces the entire sign sequence to be +,-,+,-,...,+. Therefore m is odd and the sign sum is one. Every level contributes at most one. For h>(A-1)/2, P_h is empty and the contribution is nonpositive. Hence (4) is at most 1+2(A-1)/2=A. This proves (3).

This separates two mechanisms: ordinary signs are bounded by the no-three-positive rule; a positive imbalance at a higher level is possible only along the full alternating path joining both endpoints.

## 5. Uniform theorem

**Theorem 5.1.** For all positive m,n,

\[
\boxed{\beta_2(P_m\square P_n)=F(m,n).}
\]

**Upper bound.** Let D be any dissociation set. If n is odd, set a_i=2x_i-n for its row counts, and A=g(n). These are odd integers, with a_i<=A. Corollary 2.2 gives (2). Adjacent positive entries must both be one, so three consecutive positives would violate item 3 of the corollary. Theorem 4.1 gives

\[
2|D|-mn\le\begin{cases}g(m),&m\text{ even},\\\max\{g(m),g(n)\},&m\text{ odd}.\end{cases}
\]

Equation (1) now gives |D|<=F(m,n).

If both m and n are even, tile by disjoint 2-by-2 squares to get |D|<=mn/2=F. If n is even and m odd, pair the first m-1 rows into ladders and leave the last row. Then

\[
|D|\le\frac{m-1}{2}n+\left\lceil\frac{2n}3\right\rceil
=\frac{mn+g(n)}2=F(m,n).
\]

This includes m=1 and completes all parity cases.

**Lower bound.** Use Sahbi's construction: in odd rows select columns not divisible by three, and in even rows select columns divisible by three. No selected vertical neighbors occur, and there is at most one selected horizontal neighbor at every selected vertex. It has the size of the first term of F. Transpose to obtain the second term. The larger construction proves equality.

The theorem gives, for example, beta_2(G_(101,103))=5219 and beta_2(G_(100,103))=5167 by symbolic evaluation. These are not large-grid exhaustive computations.

Taking complements also proves tau_3(G_(m,n))=mn-F(m,n), where tau_3 is the minimum number of vertices hitting every three-vertex path. Indeed, maximum degree at most one is equivalent to containing no three-vertex path as a subgraph.

**Scope warning.** The inequality beta_2<=psi_sq points in the wrong direction for deducing a coloring upper bound. Theorem 5.1 alone does not solve the full sub-quorum conjecture.

## 6. A precise remaining bridge

For feasible (T,M), let c_i count T vertices plus horizontal M edges in row i, and let k_i count vertical M edges between rows i and i+1. Set k_0=k_m=0. Choose integers 0<=u_i<=k_i, with u_0=u_m=0, assigning u_i vertical edges to their upper row and the rest to their lower row. The resulting loads satisfy

\[
z_i=c_i+k_{i-1}-u_{i-1}+u_i,\qquad\sum_i z_i=|T|+|M|. \tag{5}
\]

**Unproved orientation bridge.** Every feasible pair admits choices with:

- z_i<=ceil(2n/3);
- for even n, z_i+z_(i+1)<=n;
- for odd n, z_i+z_(i+1)<=n except when both equal (n+1)/2, with no three consecutive loads all equal to (n+1)/2.

**Conditional implication, proved.** This bridge would prove Omega=psi_sq=beta_2=F for all full rectangles: apply Theorem 4.1 to a_i=2z_i-n for odd n; for even n pair adjacent loads and use the single-row bound if one row remains. Equation (5) then bounds every feasible objective by F.

The bridge is sufficient, not established or asserted necessary. Its finite algorithm uses dynamic programming over u_i, the preceding load and the consecutive-high-row flag. The experimental orientation scripts are supplied in the companion research bundle, not in this branch.

A fixed parity orientation fails already on 4-by-3. Use T={(1,1),(1,3),(4,1),(4,3)} and M={(1,2)-(2,2),(3,2)-(4,2)}. Then c=(2,0,0,2). Both matching units must point inward, giving (2,1,1,2). Uniformly pointing to odd rows or to even rows exceeds a boundary row's capacity.

The cube's covering-matching conclusion also fails on the grid. On 4-by-4, using row-major indices 0,...,15, take

T={1,3,6,9,12}, M={{0,4},{7,11},{13,14}}, B={2,5,8,10,15}.

This is feasible, but N_B(T)={2,5,8,10} has size four while |T|=5. Thus no T-to-B covering matching exists. Nevertheless |T|=|B| and |T|+|M|=8=F(4,4). This refutes the stronger transfer mechanism, not the desired numerical formula.

## 7. Verification and formalization scope

The checked-in verifier is `develop/verify_rectangular_beta.py`. From develop, run `python3 verify_rectangular_beta.py --output results/grid-beta-uniform-verification.json`. The standard-library integer checks cover:

- all 46,365 independent path subsets through order 20;
- all 101,634 admissible ladder subsets through width 10, including odd-width equality rigidity;
- 320 exact profile optimizations, lengths through 32, positive upper bounds 1,3,...,19 and entries down to -39;
- both lower constructions on 1,600 rectangles through 40-by-40;
- exact row-frontier beta_2 computations on 240 rectangles, widths 1 through 8 and lengths 1 through 30;
- the explicit boundary-matching counterexample and symbolic examples.

All passed in the local research run. The independent grid DP records the last row mask and the selected vertices already having a selected neighbor. Adding a row cannot create a second neighbor at such a vertex, or both a horizontal and preceding-row neighbor in the new row. Older rows have no future neighbors. Thus accepted histories are exactly dissociation sets. Execution outputs are included in the companion research bundle; this branch includes the proof and beta verifier, not the output JSON files.

Separate local orientation tests passed on 2x3,3x3,4x3,3x4,3x5,5x3,4x4, with 116; 1,145; 11,544; 11,544; 116,011; 116,011; 249,116 feasible pairs respectively. A seeded random search passed 9,000 generated pairs across nine sizes up to 20x20. These are evidence for an UNPROVED bridge, not a universal coloring proof. The orientation scripts and output records are in the companion research bundle and are not checked into this branch.

Proposed Lean order: path-neighborhood defect; finite integer level decomposition and profile theorem; ladder rigidity; row-count conversion; parity normalization and lower construction. No Lean/Scribe or CI success is claimed here, and no existing formal declarations are changed.

## References and priority limits

[S] R. Sahbi, *Sub-quorum colorings of graphs*, arXiv:2609.25128v1 (2026-09-20), Proposition 5.2, Lemma 5.4, Theorem 5.5 and the following grid conjecture. https://arxiv.org/html/2609.25128v1

[T] trureturing dev snapshot cd6c23732d426223b7593d0596fdc7d3c916bd43, `D5/S3/Combinatorics/Graph/HypercubeSubQuorum.lean` and its Blueprint. https://github.com/the-omega-institute/trureturing/blob/cd6c23732d426223b7593d0596fdc7d3c916bd43/Blueprint/D5/S3/Combinatorics/Graph/HypercubeSubQuorum.md

[G] subquorum-colorings main snapshot f71b391717421c6567526ca0f03b9dfa344704a8, `develop/grid-strips-2026-09-27.md`.

Earlier related literature to compare before any novelty claim:
B. Bresar, M. Jakovac, J. Katrenic, G. Semanisin, A. Taranenko, *On the vertex k-path cover*, Discrete Applied Mathematics 161 (2013), 1943-1949; and M. Jakovac, A. Taranenko, *On the k-path vertex cover of some graph products*, Discrete Mathematics 313 (2013), 94-100. Bibliographic records were checked, but their full texts were inaccessible in this session. This note claims an explicit independent proof and reusable interface, not first discovery of a dissociation formula.
