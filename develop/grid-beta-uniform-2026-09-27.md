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

## 8. Continuation: mixed-match ladder rigidity

Continuation date: 2026-09-27. The upstream representative interface was
rechecked at trureturing/dev `2eb9c73fb562e335e746bbeb596a2b93869c7ff6`;
its relevant Blueprint blob is unchanged. All statements below are ordinary
written proofs. The unrestricted rectangular psi_sq/Omega formula remains
unproved. The ladder value is an existing benchmark; the strengthened
Omega equality case is the interface used in the new arguments.

In a feasible pair write P=V(M), B=V(G)\(T union P), and label vertices
T, P, or B. On a two-row band, a column of type TP means either order of
those two labels; likewise for PB. TT and BB mean both labels equal.

**Theorem 8.1 (closed ladder, arbitrary matching directions).** For a
feasible pair in G_(2,n),

    |T|+|M| <= n                 if n is even,
    |T|+|M| <= n+1               if n is odd.

For odd n, equality n+1 forces M empty, TT in every odd column, and BB in
every even column. In particular, there is no different mixed-match
extremizer at that value.

**Proof.** Write a,b,u,v for the numbers of TT, BB, TP, PB columns.
All other column types contribute zero to |T|-|B|, so

    |T|-|B| = 2(a-b)+u-v.                                      (8.1)

The P vertex of a TP column cannot have a vertical matching partner.
Its horizontal partner lies in an adjacent column. The T vertex already
has its vertical P neighbor, so its horizontal neighbor in that adjacent
column is B. The partner column is therefore PB. This maps TP columns
injectively into PB columns: a PB column has only one P vertex and that
vertex has only one matching partner. Consequently u<=v.

A TT column already gives both T vertices their sole occupied neighbor.
Every adjacent column is BB. Apply Lemma 3.1 to the independent set of TT
indices in P_n. We have a<=b, except when n is odd, TT occupies every odd
column, and BB occupies every even column. In that exception a=b+1 and no
other column type occurs. Since

    2(|T|+|M|)-2n = |T|-|B|,

(8.1) proves both bounds and the complete odd equality case. The periodic
TT/BB construction attains the bound. QED.

This proof does not delete a same-colored neighbor from an arbitrary
coloring and does not assume that a restriction of a coloring is valid.
It operates directly on feasible representatives.

**Corollary 8.2 (odd ladder color rigidity).** An (n+1)-color sub-quorum
coloring of G_(2,n), for odd n, has exactly the odd-column support and
assigns distinct colors to all its vertices.

**Proof.** Apply the representative reduction, selecting an edge from
every color class containing an edge. Theorem 8.1 forces the selected
matching empty, so no color class contains an edge. Every colored vertex
therefore has colored degree at most one. Its support is a dissociation
set with at least n+1 vertices; Lemma 2.1 forces precisely the displayed
support. Its n+1 colors on n+1 vertices are all distinct. QED.

## 9. The full formula for one-direction representative matchings

Let Omega_H(G_(m,n)) restrict the optimization to horizontal matching
edges, allowing T to be arbitrary. Define Omega_V analogously.

**Theorem 9.1.** For every positive m,n,

    Omega_H(G_(m,n)) = Omega_V(G_(m,n)) = F(m,n).                 (9.1)

**Proof.** For horizontal M, let c_i be the number of T vertices plus the
number of matching edges in row i. Then sum c_i=|T|+|M|.

First c_i<=ceil(2n/3). Restrict to that row, where all its matching edges
remain. In any path, a matching edge uv can be removed while promoting u
to T and deleting v from the occupied set. Old T vertices lose neighbors;
u has at most one remaining neighbor because its path degree is at most
two. The objective is unchanged. Iteration produces a dissociation set
of size c_i in P_n, proving the bound.

Next restrict to two adjacent rows. No matching edge is cut because all
matching edges are horizontal. The restriction remains feasible and has
objective c_i+c_(i+1). Theorem 8.1 gives at most n for even n. For odd n,
it gives at most n except when both row counts equal (n+1)/2; that
exception forces the TT/BB support and no matching edges in these rows.
Three successive row counts cannot all equal (n+1)/2: the two forced
ladder supports would create three consecutive vertical T vertices.

For odd n, apply Theorem 4.1 to a_i=2c_i-n and A=g(n), exactly as in the
proof of Theorem 5.1. For even n, pair adjacent row counts and use the
single-row bound for a final unpaired row. In every case sum c_i<=F(m,n).
The lower construction of Section 5 has M empty and gives equality.
Transpose to obtain the vertical statement. QED.

**Corollary 9.2 (quantitative mixed-direction necessity).** In an arbitrary
sub-quorum coloring with k colors, let p_V count color classes containing
an edge but no horizontal edge, and let p_H count color classes containing
an edge but no vertical edge. Then

    k <= F(m,n) + min(p_H,p_V).                                 (9.2)

In particular, if k>=F(m,n)+d, there are at least d classes of each pure
edge direction. Color classes containing both directions do not by
themselves evade (9.1).

**Proof.** Choose a horizontal representative edge wherever possible;
only the p_V classes require a vertical one. Delete those p_V matching
edges, including their endpoints, from the representative pair. The pair
remains feasible, and its objective is k-p_V. Apply (9.1). Choosing vertical
edges first instead gives k-p_H<=F. Edge-free classes are represented by
single vertices in both arguments. QED.

An optimal coloring may have its color classes taken connected: splitting
a class into its induced connected components changes no same-color
adjacency and preserves every local inequality. For such an optimum,
the pure-direction classes in (9.2) are actual nontrivial vertical and
horizontal monochromatic paths. This describes a necessary interaction
in a counterexample, not a construction of one.

## 10. Exact accounting on an open two-row band

We retain matching edges crossing the band boundary as exposed endpoints;
we do not silently discard their effect on T vertices.

For a band of two adjacent rows, let e be the number of its P vertices
whose matching partner is outside the band. Let i be the number of TP
columns whose P partner is inside. The proof of Theorem 8.1 sends these i
columns injectively to PB columns. Put

    u = #(TP)-i,       v = #(PB)-i,       R=e-u,
    delta = #(BB)-#(TT),
    J = #(T in band) + #(matching edges entirely in band).

Thus u counts the exposed P endpoints in TP columns, while v counts PB
columns unused by the injection. In particular R,v>=0.

**Theorem 10.1 (open-band identity).**

    n-J = delta + (R+v)/2.                                    (10.1)

The right-hand side is an integer. Moreover delta>=0 unless the entire
band is the odd-width TT/BB alternating support; in that exception e=0
and J=n+1.

**Proof.** If t,p,b are the band vertex counts, then p=2|M_internal|+e
and t+p+b=2n. Also t-b=2(#TT-#BB)+u-v, because the i matched pairs of
column types cancel. Therefore

    2J-2n = t-b-e = -2 delta -R-v.

The assertion about delta is exactly Lemma 3.1 applied to TT columns,
whose path neighbors are all BB. QED.

Identity (10.1) gives explicit nonnegative boundary terms. It does not
assert that exposed endpoints from all overlapping bands can be charged
simultaneously. That compatibility issue is retained.

## 11. A residual matching graph on even-by-even rectangles

Throughout this section m,n are positive even integers and H=mn/2=F(m,n).
Tile the rectangle by the aligned, disjoint 2-by-2 squares. For a tile Q
let t_Q=|T intersection Q| and delta_Q=2-t_Q. Each t_Q<=2: three T
vertices in a square would include a T with two occupied neighbors.
Call a tile saturated when t_Q=2, and deficient otherwise.

A saturated tile containing P must have two diagonally opposite T
vertices, one P vertex, and one B vertex. If its T vertices are adjacent,
they prohibit every other occupied vertex in that tile. In particular a
saturated tile contains no internal matching edge and at most one P.

**Lemma 11.1 (forced blank at an attachment).** If a matching edge joins
a saturated tile to another tile, the companion corner of the receiving
tile, along the shared side, is B. Consequently no matching edge joins
two saturated tiles.

**Proof.** The companion corner in the saturated tile is T. It already
has its P neighbor within its tile, so the opposite corner across the
shared side must be unoccupied. A saturated receiving tile would have
T at that corner, which is impossible. The same reasoning shows that
P vertices in two saturated tiles cannot be adjacent across their shared
side, even if their adjacency is not the chosen matching edge. QED.

For each deficient tile let h_Q count matching edges internal to Q and
s_Q count matching edges from Q to saturated tiles. Each such attachment
is counted only at its deficient end. Define

    r_Q = delta_Q-h_Q-s_Q.

Let Gamma be the finite multigraph on deficient tiles, with one edge for
each remaining matching edge between two different deficient tiles.
Parallel edges are kept; no loop is included. Write C=|E(Gamma)| and
R=sum_Q r_Q.

**Lemma 11.2 (local capacities).** Every r_Q is nonnegative. A tile with
r_Q=0 has Gamma-degree at most one. A tile with r_Q>0 has Gamma-degree
at most 2r_Q. Every residual-zero tile of positive Gamma-degree has
s_Q>=1.

**Proof.** If t_Q=1, its T corner allows at most one adjacent P and at
most the opposite P, hence at most two P vertices. If both occur they
are adjacent. One of the two P vertices then has T and P at its two
neighboring corners, so by Lemma 11.1 it cannot be attached to a saturated
tile. Thus h_Q+s_Q<=1. If r_Q=0 and h_Q=1, no external endpoint remains.
If r_Q=0 and s_Q=1, at most one endpoint remains for Gamma. For r_Q=1,
there are at most two Gamma endpoints.

If t_Q=0, an attachment to a saturated tile needs a B corner adjacent to
its endpoint. Three such attachment endpoints would leave at most one B;
only two corners of a square are adjacent to that B. Thus three
attachments are impossible. One internal matching edge and two
attachments would occupy all four corners, leaving no required B.
Two internal matching edges leave no external endpoint at all. This
proves h_Q+s_Q<=2.

For r_Q=2 there are at most four Gamma endpoints. For r_Q=1, either one
internal edge uses two corners, or one attachment uses a P corner and
requires a B corner; there are at most two remaining Gamma endpoints.
For r_Q=0, the cases (h_Q,s_Q)=(2,0),(1,1) leave none, and (0,2) leaves
at most one because some corner is B. Every residual-zero tile with a
remaining endpoint therefore has an attachment. QED.

**Lemma 11.3 (residual-zero leaves are independent).** No Gamma edge
has two endpoints with residual capacity zero.

**Proof.** By the preceding proof, a residual-zero tile incident to Gamma
has exactly one of the following forms, up to square symmetries. A letter
s denotes a P endpoint matched to a saturated tile, and c denotes its
sole Gamma endpoint:

    Type I:  T c          Type II:  B s
             B s                    s c

All corners neighboring c within its tile are occupied. Every such
neighbor that is P is an s corner. An s corner has one neighboring B
corner and one neighboring c corner, so Lemma 11.1 forces its attachment
to leave through the unique side containing the B corner.

Suppose two c corners are matched across the shared side of two such
tiles. Consider their companion corners along that side. If either is
T, that T has both its within-tile c neighbor and an occupied companion
across the side, violating feasibility. Thus both companions are s.
Their forced attachments leave on the same perpendicular side of the
two tiles. The two receiving saturated tiles are adjacent and their P
endpoints are adjacent across their shared side. This is prohibited by
the last assertion of Lemma 11.1. The contradiction proves the lemma.
Boundary cases introduce no exception: an asserted attachment must exist
inside the original rectangle. QED.

**Theorem 11.4 (exact residual reduction).** Put D=H-|T|=sum delta_Q and
q=|T|+|M|-H. Then

    q = C-R.                                                  (11.1)

If every connected component of Gamma has at most one residual-zero
vertex of degree one, then q<=0.

**Proof.** Every matching edge is internal to a deficient tile, joins a
saturated tile to a deficient tile, or is counted by Gamma. Hence
|M|=sum h_Q+sum s_Q+C, which proves (11.1). In a component with at most
one residual-zero leaf, Lemma 11.2 and the degree sum give
2|E|<=2 sum r_Q+1. Both |E| and sum r_Q are integers, so |E|<=sum r_Q.
Sum over components. QED.

**Theorem 11.5 (three-quarter absorption).** For every feasible pair on
an even-by-even rectangle,

    |T| + (3/4)|M| <= mn/2,
    equivalently 4|T|+3|M| <= 2mn.                            (11.2)

If q=|T|+|M|-mn/2>0, then

    mn/2-|T| >= 3q,             |M| >= 4q.                    (11.3)

Consequently the full objective bound holds whenever |T|>=mn/2-2,
or whenever |M|<=3.

**Proof.** Let ell be the number of residual-zero vertices of positive
Gamma-degree. They are leaves by Lemma 11.2. Summing degrees gives
2C<=2R+ell, hence ell>=2q by (11.1). By Lemma 11.3 their incident edges
are distinct, so C>=ell. Each such tile receives at least one saturated
tile attachment, counted only there; therefore

    D=R+sum h_Q+sum s_Q >= R+ell.

If q>0, substitute R=C-q to obtain

    D >= C-q+ell >= 2ell-q >= 3q.

If q<=0 the same inequality D>=3q follows from D>=0. Substituting
q=|M|-D yields 3|M|<=4D, proving (11.2). For q>0, |M|=D+q>=4q gives
(11.3). The stated near-extremal consequences use that q is an integer.
QED.

**Corollary 11.6 (few edged color classes).** On an even-by-even rectangle,
any sub-quorum coloring with at most three color classes containing an
edge uses at most F(m,n) colors. More generally an excess of d colors
requires at least 4d such classes and at least d classes of each pure
edge direction.

**Proof.** In the representative reduction, |M| is exactly the number
of color classes containing an edge, and |T|+|M| is the color count.
Apply (11.3) and Corollary 9.2. QED.

The desired unrestricted bound replaces 3/4 in (11.2) by 1. This is a
proved uniform stability estimate, not a proof of that stronger bound.
A possible excess must survive the residual reduction in a component
containing at least two nonadjacent residual-zero leaves. No such
counterexample is asserted to exist.

## 12. Exact even-width orientation criterion and a linear-time witness

This result concerns arbitrary nonnegative integer data c_i,k_i, not
only data already known to arise from a grid. Fix positive even n, set
b=ceil(2n/3), and use k_0=k_m=0. For an interval [a,d] put

    W(a,d)=sum_(i=a)^d c_i + sum_(i=a)^(d-1) k_i,
    L_h=floor(h/2)n+(h mod 2)b = F(h,n).

**Theorem 12.1.** There are integers 0<=u_i<=k_i for which

    z_i=c_i+k_(i-1)-u_(i-1)+u_i,
    z_i<=b,                   z_i+z_(i+1)<=n                 (12.1)

if and only if

    W(a,d)<=L_(d-a+1) for every contiguous interval.            (12.2)

A satisfying orientation, or a violating interval, can be found in O(m)
integer arithmetic operations.

**Proof of necessity.** The load sum on [a,d] is W(a,d) plus the
nonnegative incoming allocation k_(a-1)-u_(a-1)+u_d. Group the loads in
adjacent pairs and, for odd length, one singleton. This gives (12.2).

**Constructive sufficiency.** Put

    S_0=0,
    S_i=sum_(j=1)^i c_j + sum_(j=1)^(i-1) k_j,
    U_i=S_i+k_i,                 U_0=0.

Cumulative loads X_i=sum_(j=1)^i z_j equal S_i+u_i. They must lie between
S_i and U_i, with X_0=0 and X_m=S_m. The upper constraints in (12.1) say
X_i-X_(i-1)<=b and X_i-X_(i-2)<=n. Their componentwise largest candidate
subject to X_i<=U_i is

    Y_0=0,
    Y_1=min(U_1,b),
    Y_i=min(U_i,Y_(i-1)+b,Y_(i-2)+n)       for i>=2.            (12.3)

Because 2b>=n, a shortest sequence of steps of length one and two, with
costs b and n, covering h positions has cost L_h. Unrolling (12.3) gives

    Y_i=min_(0<=j<=i) (U_j+L_(i-j)).                           (12.4)

For j<i we have S_i-U_j=W(j+1,i). Condition (12.2) therefore gives
Y_i>=S_i. Thus S_i<=Y_i<=U_i, and in particular Y_m=S_m. Set
u_i=Y_i-S_i and z_i=Y_i-Y_(i-1). These satisfy (12.1). Nonnegativity of
z_i also follows from Y_i>=S_i>=U_(i-1)>=Y_(i-1).

The recursion uses a constant number of integer additions and comparisons
per row. Track the originating j for each minimizing term. If a lower
bound Y_i>=S_i first fails, that origin supplies an interval [j+1,i]
violating (12.2). Storing the Y_i values reconstructs every u_i. QED.

**Logical consequence for the research route.** On a geometric input,
W(a,d) is exactly the objective of the feasible representative pair in
the subrectangle consisting of rows a through d, after discarding
matching edges crossing its boundary. Therefore, for any fixed even
width, the universal row-orientation bridge is equivalent to the
universal Omega bound for that width across all lengths. An orientation
failure yields an actual smaller rectangular Omega counterexample.
This equivalence prevents using the bridge as an unjustified shortcut.

Odd widths still require the exceptional balanced pair and the exclusion
of three consecutive high rows. The even-width criterion cannot simply
be reused: for n=5, c=(4,2), k=(0), all interval totals meet F, but the
only loads (4,2) violate the odd-width balanced-pair rule. This abstract
profile is not claimed geometrically realizable; Theorem 8.1 excludes
it on the closed two-row grid.

## 13. Continuation verification, scope, and next obstruction

The continuation verifier is `develop/verify_grid_directional_core.py`.
It uses only the Python standard library and exact integers. Run

    python3 develop/verify_grid_directional_core.py --output develop/results/grid-directional-core-verification.json

The checked-in output records 288,804 exhaustive feasible pairs across
ten listed rectangles, 120,680 arbitrary integer orientation profiles,
and 1,200 seeded random geometric pairs across six sizes, including
20-by-20. All listed checks passed. Every intermediate open-band and
residual-capacity assertion is checked; the script checks residual-zero
independence as well as the final coefficient 3/4. The finite runs do not
replace any universal written proof.

This continuation proves the one-direction formula at all dimensions,
the exact exposed-endpoint ledger, the even-by-even three-quarter
absorption estimate and near-extremal cases, and the exact constructive
even-width interval criterion. It leaves the unrestricted mixed-direction
Omega/psi_sq bound unproved. In the even-by-even case its remaining
obstruction is an overloaded residual component as in (11.1), with at
least two nonadjacent residual-zero leaves. The stronger coefficient-one
absorption statement is a target, not an assumption in any proof above.

No Lean, Scribe declaration, CI result, independent referee approval, or
worldwide priority claim is asserted. The source-faithful reduction is
reused from [S] and [T]; the ladder value is not presented as newly
invented. The structural equality case and the subsequent paper proofs
are the continuation's derived results. The inspected upstream source is
`Blueprint/D5/S3/Combinatorics/Graph/HypercubeSubQuorum.md` at the dev
snapshot stated at the start of Section 8. Earlier Sections 1--7 and their
priority qualifications are retained.
