# Full representative equality at height six

13 November 2026. This note closes the remaining two-seam case in the
representative-pair problem for the height-six grid. It uses an exact finite
state transfer together with an integer potential certificate. The potential
is the part that turns the finite computation into an all-length upper
bound; the prefix values by themselves would not be sufficient.

Write (G_{6,n}=P_6\square P_n). A representative pair is a matching (M)
and a set (T\cap V(M)=\varnothing) such that every (t\in T) has at most
one neighbour in (T\cup V(M)). Its score is

\[
  \operatorname{sc}(T,M)=|T|+|M|.
\]

The previously established no-seam ledger and the four-row one-seam
reduction leave only pairs whose matching uses both seams between rows
(2,3) and (4,5). The theorem below treats all four seam flags at once,
so it also gives an independent check of those reductions.

## Theorem

For every (n\ge1),

\[
\boxed{\Omega(P_6\square P_n)=
\begin{cases}
3n,&n\text{ even},\\
3n+1,&n\text{ odd}.
\end{cases}}
\tag{1}
\]

Consequently, using the already proved identity

\[
\beta_2(P_6\square P_n)=
\begin{cases}
3n,&n\text{ even},\\
3n+1,&n\text{ odd},
\end{cases}
\]

and Sahbi's representative reduction
(eta_2\le\psi_{\rm sq}\le\Omega), the three parameters agree:

\[
\boxed{\beta_2(P_6\square P_n)=
\psi_{\rm sq}(P_6\square P_n)=
\Omega(P_6\square P_n).}
\tag{2}
\]

The lower bound in (1) is the usual row-periodic dissociation/representative
construction: with zero-based column numbering, select both rows of the top
and bottom two-row bands in even columns and both rows of the middle band in
odd columns. Its score is
(3n) for even (n) and (3n+1) for odd (n). It uses no seam-crossing
matching edge. The work is therefore the upper bound, including the case in
which both seams are crossed.

## Exact transfer states

Process the columns from left to right. Each vertex in the current column
has label (B,T), or (P), where (P) means an endpoint of (M). A state
after a column records

1. the six current labels;
2. the occupied mask of the preceding column;
3. the mask of matching edges entering the current column from the left;
4. the mask of matching edges leaving it to the right; and
5. two monotone flags recording whether a vertical matching edge has
   crossed the (2\)--(3) seam and the (4\)--(5) seam.

For each column, the (P)-vertices not already used by a horizontal matching
edge must be covered by the unique vertical matching of the remaining
induced row path. A proposed transition is rejected if a (T)-vertex has
more than one neighbour in (T\cup V(M)). The transition score is the
number of new (T)-vertices, the number of new vertical matching edges,
and the horizontal matching edges arriving from the preceding column.
At the right boundary the outgoing mask is zero.

This state description is exact. Matching degree is checked by the disjoint
incoming and outgoing masks and the vertical completion; every occupied
neighbour of a selected vertex is checked when its right neighbour is
introduced. Thus no matching edge or local feasibility condition is lost
when a column is forgotten.

The portable state key used in the certificate is

\[
 k=\operatorname{code}(\text{labels})
   +2^{10}o+2^{16}L+2^{22}R+2^{28}\phi,
\]

where the base-three label code uses row zero as its least significant
digit, (o,L,R) are six-bit masks, and
(\phi\in\{0,1,2,3\}). The exact reachable state set after four columns
has 257,792 states. The set after five columns is the same set, and it is
closed under every subsequent one-column transition. The closure check is
explicit: the certificate run encountered zero transitions from the stable
set to a missing state.

## Potential certificate

Let (V_4(s)) and (V_5(s)) be the exact maximum scores reaching state (s)
after four and five columns. For a two-column path from (s) to (t), let
(R(s,t)) be the sum of its two transition scores. The supplied integer
table (p(s)), one value for each of the 257,792 stable states, satisfies

\[
  R(s,t)+p(t)\le 6+p(s)                         \tag{3}
\]

for every legal two-column path in the stable state set. This is checked by
applying the exact max-plus transfer twice to the table and verifying the
entrywise inequality

\[
  \Phi^2(p)\le p+6.
\]

The table was obtained from the zero vector by the monotone iteration

\[
 p_{j+1}=\max\{p_j,\Phi^2(p_j)-6\}.
\]

The four iterations have largest increases (3,1,1,0), and the final
entrywise violation is zero. This construction is only a way to find the
certificate; (3), together with the finite state rules, is the proof
obligation and is checked directly for the final table.

The minimum potential over right-boundary states (R=0) is zero. The exact
seed vectors obey

\[
 \max_s(V_4(s)+p(s))=12,
 \qquad
 \max_s(V_5(s)+p(s))=16.                         \tag{4}
\]

For a path of even length (n=4+2q), summing (3) gives, after its final
state is required to have (R=0),

\[
 |T|+|M|\le 12+6q=3n.
\]

For odd length (n=5+2q), the same argument gives

\[
 |T|+|M|\le16+6q=3n+1.
\]

The lengths (1,2,3) are checked directly by the same exact transfer and
have maxima (4,6,10), respectively. This proves (1) for every positive
length. The four seam flag values have the same maximum at every checked
length; the potential proof bounds them simultaneously rather than using
that numerical observation as an assumption.

## Reproduction and scope

From the repository root run the generator to a disposable path, then compare
its deterministic output with the checked-in certificate:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra \
  scripts/explore_representative_height_six.cpp \
  -o /tmp/explore-representative-height-six
/tmp/explore-representative-height-six \
  --potential /tmp/representative-height-six-two-seam-potential.tsv
cmp output/representative-height-six-two-seam-potential.tsv \
  /tmp/representative-height-six-two-seam-potential.tsv
```

The run recomputes the exact four- and five-column seed vectors, constructs
the stable state set, checks closure, verifies (3), and verifies (4). The
same executable also reports the direct maxima through any requested finite
length; the run through (n=10) gives

\[
4,6,10,12,16,18,22,24,28,30
\]

and all four seam-flag maxima equal the displayed value. The potential TSV
is a deterministic finite proof certificate, not a large-board sample.

No Lean verification is claimed. The theorem is about the representative
optimization; its colouring consequence uses the previously established
representative reduction and the all-rectangle dissociation formula. It
does not by itself prove an arbitrary-height or arbitrary-rectangle
mixed-direction theorem.
