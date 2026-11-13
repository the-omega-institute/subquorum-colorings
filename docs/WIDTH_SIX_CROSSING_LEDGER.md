# A three-band crossing ledger for the width-six grid

13 November 2026. Let `G(6,n) = P_6 square P_n`, and let a feasible
representative pair `(T,M)` have the usual meaning: `M` is a matching,
`T` is disjoint from `V(M)`, and every vertex of `T` has at most one
neighbor in `T union V(M)`. This note isolates a class of width-six pairs
for which the mixed-direction problem is already settled.

Partition the rows into the three two-row bands

\[
 B_1=\{1,2\},\qquad B_2=\{3,4\},\qquad B_3=\{5,6\}.
\]

Assume that `M` has no edge across either horizontal seam, between rows
2 and 3 or between rows 4 and 5. Put

\[
 J_i=|T\cap B_i|+|M\cap E(G[B_i])|.
\]

The restriction to each band remains feasible: removing vertices and
matching edges outside the band can only lower the occupied degree of a
selected vertex. Since every matching edge is internal to one band,

\[
 |T|+|M|=J_1+J_2+J_3.                              \tag{1}
\]

For even `n`, the closed two-row ladder theorem gives `J_i <= n`, so

\[
 |T|+|M|\le 3n=F(6,n).                              \tag{2}
\]

For odd `n`, the same theorem gives `J_i <= n+1`. Equality in a band
is rigid: that band has no matching edges, its odd columns are `TT`, and
its even columns are `BB`. Call such a band exceptional.

No two adjacent bands can both be exceptional. At an odd column on their
common seam, the lower `T` vertex of the upper exceptional band already
has its vertical `T` partner. If the adjacent vertex in the lower band
were `T` or an endpoint of `M`, it would be a second occupied neighbor,
contradicting feasibility.

If the first and third bands are both exceptional, the middle band has
both vertices `B` in every odd column: each such vertex is adjacent to a
`T` vertex in one of the exceptional bands, so either `T` or `P=V(M)`
there would violate the same one-occupied-neighbor condition. With its odd
columns equal to `BB`, the middle band contributes at most `n-1`: no
matching edge can use an odd-column vertex, and each of its
`(n-1)/2` even columns contributes at most two to `J_2`. Therefore

\[
 J_1+J_2+J_3\le 2(n+1)+(n-1)=3n+1.                \tag{3}
\]

If at most one band is exceptional, the bound is immediately
(3n+1). Thus every no-seam-crossing pair satisfies

\[
 |T|+|M|\le
 \begin{cases}
 3n,&n\text{ even},\\
 3n+1,&n\text{ odd},
 \end{cases}
 =F(6,n),                                           \tag{4}
\]
where the displayed values follow by substituting `m=6` in the known
formula for `F(m,n)`.
\]

The row-periodic dissociation constructions attain these values, so the
restricted optimum is exactly `F(6,n)`. Consequently any width-six
representative pair that could exceed the conjectured value must use a
matching edge across at least one of the two seams. This is a structural
reduction for the unresolved mixed-direction problem; it does not claim
that such crossing pairs exist or that the full width-six equality is
proved.

The finite checker
[`check_grid_width_six_no_crossing.cpp`](../scripts/check_grid_width_six_no_crossing.cpp)
enumerates all matchings and all compatible `T` on two-row ladders of
length at most six. It checks the closed-ladder maxima and the (BB)-odd
boundary penalty used in (3). These finite checks validate the local
counting statements; the all-`n` conclusion is the argument above.
