# Uniform grid bounds from row profiles

Mathematical companion to [the research overview](GRID_RESULTS.md).

## 1. Definitions

Let G_(m,n)=P_m square P_n. A dissociation set induces maximum degree at most one; beta_2 is its maximum size. A feasible pair (T,M) consists of a matching M and a disjoint set T, each of whose vertices has at most one neighbor in A=T union V(M). Omega is the maximum of |T|+|M|.

Define

$$
F(m,n)=\max\left\{
\left\lceil\frac m2\right\rceil\left\lceil\frac{2n}3\right\rceil+\left\lfloor\frac m2\right\rfloor\left\lfloor\frac n3\right\rfloor,
\left\lceil\frac n2\right\rceil\left\lceil\frac{2m}3\right\rceil+\left\lfloor\frac n2\right\rfloor\left\lfloor\frac m3\right\rfloor
\right\}.
$$

Sahbi [S], Proposition 5.2 and Lemma 5.4, supplies

$$
F(m,n)\le\beta_2(G_{m,n})\le\psi_{sq}(G_{m,n})\le\Omega(G_{m,n}).
$$

Put g(k)=k-2 floor(k/3)=2 ceil(2k/3)-k. Then

$$
2F(m,n)-mn=\max\{(m\bmod2)g(n),(n\bmod2)g(m)\}. \tag{1}
$$

To verify (1), use ceil(2k/3)=k-floor(k/3), and write ceil(m/2), floor(m/2) in terms of m and its parity. Also g(k)>0 for k>=1.

The counting argument uses path-neighborhood expansion at each integer level of a row profile.

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

$$
a_i+a_{i+1}\le0\quad\text{unless }a_i=a_{i+1}=1, \tag{2}
$$

and no three consecutive entries are positive. Then

$$
\sum_i a_i\le
\begin{cases}
g(m),&m\text{ even},\\
\max\{A,g(m)\},&m\text{ odd}.
\end{cases} \tag{3}
$$

No lower bound on the negative entries is required.

**Proof.** Let sigma_i be the sign of a_i. For each integer h>=1 set

$$
P_h=\{i:a_i\ge2h+1\},\qquad N_h=\{i:a_i\le-(2h+1)\}.
$$

By (2), P_h is independent and N(P_h) is contained in N_h. Lemma 3.1 implies |P_h|-|N_h|<=0, except possibly when m is odd, P_h is all odd indices, and N_h all even indices. In that case the difference is one. These are the only positive differences possible.

The finite integer level decomposition is

$$
\sum_i a_i=\sum_i\sigma_i+2\sum_{h\ge1}(|P_h|-|N_h|). \tag{4}
$$

If no level has a positive difference, the right side is at most the sign sum. At most ceil(2m/3) signs are positive, because three consecutive positive signs are forbidden. Thus the sum is at most 2 ceil(2m/3)-m=g(m).

If some level has a positive difference, its exceptional configuration forces the entire sign sequence to be +,-,+,-,...,+. Therefore m is odd and the sign sum is one. Every level contributes at most one. For h>(A-1)/2, P_h is empty and the contribution is nonpositive. Hence (4) is at most 1+2(A-1)/2=A. This proves (3).

This separates two mechanisms: ordinary signs are bounded by the no-three-positive rule; a positive imbalance at a higher level is possible only along the full alternating path joining both endpoints.

## 5. Uniform theorem

**Theorem 5.1.** For all positive m,n,

$$
\boxed{\beta_2(P_m\square P_n)=F(m,n).}
$$

**Upper bound.** Let D be any dissociation set. If n is odd, set a_i=2x_i-n for its row counts, and A=g(n). These are odd integers, with a_i<=A. Corollary 2.2 gives (2). Adjacent positive entries must both be one, so three consecutive positives would violate item 3 of the corollary. Theorem 4.1 gives

$$
2|D|-mn\le\begin{cases}g(m),&m\text{ even},\\\max\{g(m),g(n)\},&m\text{ odd}.\end{cases}
$$

Equation (1) now gives |D|<=F(m,n).

If both m and n are even, tile by disjoint 2-by-2 squares to get |D|<=mn/2=F. If n is even and m odd, pair the first m-1 rows into ladders and leave the last row. Then

$$
|D|\le\frac{m-1}{2}n+\left\lceil\frac{2n}3\right\rceil
=\frac{mn+g(n)}2=F(m,n).
$$

This includes m=1 and completes all parity cases.

**Lower bound.** Use Sahbi's construction: in odd rows select columns not divisible by three, and in even rows select columns divisible by three. No selected vertical neighbors occur, and there is at most one selected horizontal neighbor at every selected vertex. It has the size of the first term of F. Transpose to obtain the second term. The larger construction proves equality.

The theorem gives, for example, beta_2(G_(101,103))=5219 and beta_2(G_(100,103))=5167 by symbolic evaluation. These are not large-grid exhaustive computations.

Taking complements also proves tau_3(G_(m,n))=mn-F(m,n), where tau_3 is the minimum number of vertices hitting every three-vertex path. Indeed, maximum degree at most one is equivalent to containing no three-vertex path as a subgraph.

The coloring upper bound requires controlling representative matching edges as well. We first treat the case in which they have a common direction.

## 6. Closed ladders with arbitrary matching directions

In a feasible pair write P=V(M), B=V(G)\(T union P), and label vertices
T, P, or B. On a two-row band, a column of type TP means either order of
those two labels; likewise for PB. TT and BB mean both labels equal.

**Theorem 6.1 (closed ladder, arbitrary matching directions).** For a
feasible pair in G_(2,n),

    |T|+|M| <= n                 if n is even,
    |T|+|M| <= n+1               if n is odd.

For odd n, equality n+1 forces M empty, TT in every odd column, and BB in
every even column. In particular, there is no different mixed-match
extremizer at that value.

**Proof.** Write a,b,u,v for the numbers of TT, BB, TP, PB columns.
All other column types contribute zero to |T|-|B|, so

    |T|-|B| = 2(a-b)+u-v.                                      (6.1)

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

(6.1) proves both bounds and the complete odd equality case. The periodic
TT/BB construction attains the bound. QED.

The proof operates on feasible representatives, whose feasibility is preserved on restriction when no matching edge is cut.

**Corollary 6.2 (odd ladder color rigidity).** An (n+1)-color sub-quorum
coloring of G_(2,n), for odd n, has exactly the odd-column support and
assigns distinct colors to all its vertices.

**Proof.** Apply the representative reduction, selecting an edge from
every color class containing an edge. Theorem 6.1 forces the selected
matching empty, so no color class contains an edge. Every colored vertex
therefore has colored degree at most one. Its support is a dissociation
set with at least n+1 vertices; Lemma 2.1 forces precisely the displayed
support. Its n+1 colors on n+1 vertices are all distinct. QED.

## 7. The full formula for one-direction representative matchings

Let Omega_H(G_(m,n)) restrict the optimization to horizontal matching
edges, allowing T to be arbitrary. Define Omega_V analogously.

**Theorem 7.1.** For every positive m,n,

    Omega_H(G_(m,n)) = Omega_V(G_(m,n)) = F(m,n).                 (7.1)

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
objective c_i+c_(i+1). Theorem 6.1 gives at most n for even n. For odd n,
it gives at most n except when both row counts equal (n+1)/2; that
exception forces the TT/BB support and no matching edges in these rows.
Three successive row counts cannot all equal (n+1)/2: the two forced
ladder supports would create three consecutive vertical T vertices.

For odd n, apply Theorem 4.1 to a_i=2c_i-n and A=g(n), exactly as in the
proof of Theorem 5.1. For even n, pair adjacent row counts and use the
single-row bound for a final unpaired row. In every case sum c_i<=F(m,n).
The lower construction of Section 5 has M empty and gives equality.
Transpose to obtain the vertical statement. QED.

**Corollary 7.2 (quantitative mixed-direction necessity).** In an arbitrary
sub-quorum coloring with k colors, let p_V count color classes containing
an edge but no horizontal edge, and let p_H count color classes containing
an edge but no vertical edge. Then

    k <= F(m,n) + min(p_H,p_V).                                 (7.2)

In particular, if k>=F(m,n)+d, there are at least d classes of each pure
edge direction. Color classes containing both directions do not by
themselves evade (7.1).

**Proof.** Choose a horizontal representative edge wherever possible;
only the p_V classes require a vertical one. Delete those p_V matching
edges, including their endpoints, from the representative pair. The pair
remains feasible, and its objective is k-p_V. Apply (7.1). Choosing vertical
edges first instead gives k-p_H<=F. Edge-free classes are represented by
single vertices in both arguments. QED.

An optimal coloring may have its color classes taken connected: splitting
a class into its induced connected components changes no same-color
adjacency and preserves every local inequality. For such an optimum,
the pure-direction classes in (7.2) are actual nontrivial vertical and
horizontal monochromatic paths. This describes a necessary interaction
in a counterexample, not a construction of one.

## 8. Exact accounting on an open two-row band

We retain matching edges crossing the band boundary as exposed endpoints;
we do not silently discard their effect on T vertices.

For a band of two adjacent rows, let e be the number of its P vertices
whose matching partner is outside the band. Let i be the number of TP
columns whose P partner is inside. The proof of Theorem 6.1 sends these i
columns injectively to PB columns. Put

    u = #(TP)-i,       v = #(PB)-i,       R=e-u,
    delta = #(BB)-#(TT),
    J = #(T in band) + #(matching edges entirely in band).

Thus u counts the exposed P endpoints in TP columns, while v counts PB
columns unused by the injection. In particular R,v>=0.

**Theorem 8.1 (open-band identity).**

    n-J = delta + (R+v)/2.                                    (8.1)

The right-hand side is an integer. Moreover delta>=0 unless the entire
band is the odd-width TT/BB alternating support; in that exception e=0
and J=n+1.

**Proof.** If t,p,b are the band vertex counts, then p=2|M_internal|+e
and t+p+b=2n. Also t-b=2(#TT-#BB)+u-v, because the i matched pairs of
column types cancel. Therefore

    2J-2n = t-b-e = -2 delta -R-v.

The assertion about delta is exactly Lemma 3.1 applied to TT columns,
whose path neighbors are all BB. QED.

Identity (8.1) gives explicit nonnegative boundary terms. It does not
assert that exposed endpoints from all overlapping bands can be charged
simultaneously. That compatibility issue is retained.

## Reference

[S] R. Sahbi, *Sub-quorum colorings of graphs*, [arXiv:2609.25128v1](https://arxiv.org/abs/2609.25128v1), Proposition 5.2 and Lemma 5.4. The constructions and representative reduction are due to Sahbi.

For the relationship with earlier dissociation and path-cover work, see the overview's attribution paragraph.
