# Four-row representative pairs and the one-seam width-six reduction

13 November 2026. The earlier height-six ledger settled pairs whose matching
has no horizontal seam crossing. This note handles the next case: a matching
that crosses at most one of the two seams between the three two-row bands.

Write (G_{h,n}=P_h\square P_n). A representative pair is a matching (M)
and a disjoint set (T) such that every (t\in T) has at most one neighbor
in (T\cup V(M)). Its score is

\[
\operatorname{sc}(T,M)=|T|+|M|.
\]

## The four-row transfer theorem

Define (Omega_4(n)) as the largest score of a representative pair on
(G_{4,n}). Also define (Omega_4^{\partial}(n)) by requiring that the
bottom-row vertices in columns (0,2,4,\ldots) are all (B), meaning they
belong to neither (T) nor (V(M)).

**Theorem 1.** For every (n\ge1),

\[
\boxed{\Omega_4(n)=2n+(n\bmod2)},\qquad
\boxed{\Omega_4^{\partial}(n)=2n}.
\]

The proof is an exact finite-state transfer, included here so that the
infinite assertion does not rest on a list of small optima. In a column each
vertex has one of three labels (B,T,P). A (P)-vertex is an endpoint of
(M). For a retained column record:

* the labels in that column;
* the occupied mask of the preceding column;
* the (P)-vertices matched to the preceding and following columns.

All remaining (P)-vertices in the column must be covered by the unique
vertical matching of the induced path on the remaining rows. A (T)-vertex
is checked against its vertical occupied neighbors and the occupied mask on
its left; the right contribution is checked when the next column is added.
The transition adds the new (T)-vertices, the new vertical matching edges,
and the horizontal matching edges from the preceding column. At the right
boundary the following (P)-mask is zero.

This is an exact state description: a horizontal matching edge is recorded at
both ends only through one shared bit, and every vertical endpoint is paired
inside its column. No matching or occupied neighbor is discarded when a
column is forgotten. Adding a constant to every state score commutes with
the transition.

For the unrestricted transfer, the complete reachable state vector at length
5 translates at length 7 by (+4); the supports are identical. The same is
true at the other parity seed, from length 4 to length 6. For the boundary
transfer the column restriction has period two, so the two parity phases have
separate two-column max-plus operators; both parity seeds must be certified.
The exact finite certificates are reproduced by
[`check_grid_height_four_representatives.py`](../scripts/check_grid_height_four_representatives.py):

\[
\begin{aligned}
V^{\rm free}_{7}&=V^{\rm free}_{5}+4,
&V^{\rm free}_{6}&=V^{\rm free}_{4}+4,\\
V^{\partial}_{7}&=V^{\partial}_{5}+4,
&V^{\partial}_{6}&=V^{\partial}_{4}+4.
\end{aligned}
\]

Here each equality is an equality of complete maximum-score vectors: the
reachable supports are identical and every corresponding state value is
translated by 4. For the unrestricted transfer, the one-column max-plus
operator $G$ satisfies $G(V+c)=G(V)+c$. For the boundary transfer, let
$E$ be the one-column operator for an even column (bottom label $B$ required)
and $O$ the operator for an odd column (unrestricted). The two phase-aware
two-column operators are

\[
G_{\rm even}=O\circ E,\qquad G_{\rm odd}=E\circ O,
\]

where the rightmost operator acts first. Both satisfy
$G_{\rm even}(V+c)=G_{\rm even}(V)+c$ and
$G_{\rm odd}(V+c)=G_{\rm odd}(V)+c$. Thus the two identities seed the two
parity classes and give the recurrences

\[
\Omega_4(n+2)=\Omega_4(n)+4,
\qquad
\Omega_4^{\partial}(n+2)=\Omega_4^{\partial}(n)+4.
\]

The exact initial values through (n=5) are respectively

\[
3,4,7,8,11,
\qquad
2,4,6,8,10.
\]

Induction proves Theorem 1 for all (n). The accompanying script also
enumerates every matching and every disjoint (T) on widths (1,2,3) by a
literal independent checker; those controls agree with the transfer values.
The finite enumeration is a check of the state implementation, while the
translation identities and induction are the all-length proof.

The boundary formula is invariant under vertical reflection, so the same
bound holds when the top row is (B) in the even columns.

## The one-seam width-six theorem

We use the following previously proved closed-ladder equality lemma in the
same representative-pair model. On $P_2\square P_n$, every feasible pair has
score at most $n$ for even $n$ and at most $n+1$ for odd $n$. If $n$ is odd
and the score is $n+1$, then $M$ is empty, the two vertices in every
zero-based even column belong to $T$, and the two vertices in every
zero-based odd column are $B$. This is Theorem 6.1 (closed ladder, arbitrary
matching directions) in [`GRID_PROFILE_PROOF.md`](GRID_PROFILE_PROOF.md); its
hypotheses are exactly $T\cap V(M)=\varnothing$ and every $t\in T$ has at
most one neighbor in $T\cup V(M)$.

Let (M) have no edge across the seam between rows (4) and (5), using
one-based row numbering. If it has no edge across the other seam either,
the three-band ledger already gives the known (F(6,n)) bound. Suppose it
has crossing edges only across rows (2\text{--}3). The restriction to the
top four rows is a representative pair, and all its matching edges remain
inside that restriction. The bottom two-row band is also a closed-ladder
representative pair. Hence

* for even (n), the scores are at most (2n) and (n), giving (3n);
* for odd (n), the bottom band has score at most (n+1). If it has score
  at most (n), Theorem 1 gives (2n+1+n=3n+1). If it has score (n+1),
  the closed-ladder equality case forces (M) to be empty in that band and
  forces both bottom-band vertices in columns (0,2,\ldots) into (T).
  Their selected vertical partners mean that the adjacent vertices in the
  fourth row must be (B) in those columns. The boundary case of Theorem 1
  bounds the top four-row score by (2n), so the total is again (3n+1).

The case with crossing edges only across rows (4\text{--}5) follows by
vertical reflection. Combining this with the previous no-seam theorem gives:

**Theorem 2.** If a feasible pair on (G_{6,n}) has score larger than

\[
F(6,n)=
\begin{cases}3n,&n\text{ even},\\3n+1,&n\text{ odd},\end{cases}
\]

then (M) contains at least one edge across rows (2\text{--}3) and at
least one edge across rows (4\text{--}5).

This is a genuine two-seam reduction. It does not prove the full width-six
equality: the remaining case has to couple both crossings through the middle
two-row band. It also does not treat odd or arbitrary rectangle dimensions.

## Verification scope

Run:

```sh
python3 -B scripts/check_grid_height_four_representatives.py
```

The run checks both parity seeds for both all-length transfer translations,
state-support equality, and literal matching/subset optima on the first three
widths. No Lean run is claimed. The transfer certificate is independent of the
width-six exact frontier code; the one-seam deduction uses only this note, the
closed two-row ladder theorem just stated, and the previously proved no-seam
ledger.
