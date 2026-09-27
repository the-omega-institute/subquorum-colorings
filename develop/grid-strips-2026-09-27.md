# Exact Omega certificates for grid widths 8, 9, 10 and 11

Research status: independently checked computer-assisted strip extension.
No Lean formalization and no claim of an arbitrary-width solution or a
worldwide priority search. This extends the width range established in the
inspected arXiv:2609.25128v1, whose Theorem 5.5 covers widths 3 through 7.

## Result

Let G_(m,n) be the m-by-n rectangular grid and define

    F(m,n) = max(ceil(m/2)*ceil(2n/3) + floor(m/2)*floor(n/3),
                 ceil(n/2)*ceil(2m/3) + floor(n/2)*floor(m/3)).

For each m in {8,9,10,11} and every positive integer n, the checked certificates,
together with the transfer argument below, establish

    beta_2(G_(m,n)) = psi_sq(G_(m,n)) = Omega(G_(m,n)) = F(m,n).

In particular, width 8 gives 4n for even n and 4n+2 for odd n;
width 10 gives 5n for even n and 5n+2 for odd n. For width 9 the formula is

    max(5*ceil(2n/3) + 4*floor(n/3), 6*ceil(n/2) + 3*floor(n/2)).

The existing periodic construction supplies the lower bound; our work here
is an independent exact Omega enumeration and its new-width certificates.
The max-plus periodicity method is already used in Sahbi's Theorem 5.5.

## Why Omega is sufficient

Omega(G) maximizes |T|+|M| over a matching M and a set T disjoint from its
endpoints, with each vertex of T having at most one neighbor in
A = T union V(M).

The inequality psi_sq(G) <= Omega(G) can be seen directly for any admissible
partial coloring. Choose an internal edge from each color class containing
an edge; choose one representative from every remaining color class.
Different classes give disjoint vertices, so the edges form a matching M
and the representatives form T. A representative from an edge-free class
has zero same-color neighbors. Its sub-quorum inequality therefore forces
at most one colored neighbor, hence at most one neighbor in A. The number
of colors is |T|+|M|. This proves the reduction without assuming connected
color classes or modifying a coloring.

For the lower bound, in odd-numbered rows select columns not divisible by
3, and in even-numbered rows select columns divisible by 3. Selected
vertices have no vertical selected neighbors and at most one horizontal
selected neighbor. This gives the first term of F. Transpose the
construction for the second term. Give each selected vertex its own color;
the center and at most one colored neighbor satisfy Definition 2.2.
Thus F <= beta_2 <= psi_sq <= Omega.

## Exact frontier enumeration

Process a strip of width m one row at a time, within each row left to right.
The frontier has one digit per column. Each processed vertex touching the
unprocessed portion has one of these labels:

| Digit | Meaning |
| --- | --- |
| 0 | Vertex outside A |
| 1 | Vertex in T, no occupied processed neighbor |
| 2 | Vertex in T, one occupied processed neighbor |
| 3 | Matching endpoint whose partner is already processed |
| 4 | Matching endpoint whose partner must be immediately below |
| 5 | Matching endpoint whose partner must be immediately right |

Occupancy means membership in A. A vertex in T may never receive a second
occupied neighbor. Its digit changes from 1 to 2 when its next occupied
neighbor is processed. An outgoing matching request must be satisfied by
the next vertex in its direction; simultaneous requests from above and
left are forbidden. A newly chosen matching edge can point only right or
down, since its first endpoint chooses it. No edge points right from the
last column. The vertex labels enforce endpoint disjointness.

Every feasible (T,M) determines exactly one such sequence of local choices:
orient every matching edge by processing order. Conversely, every accepted
sequence defines disjoint T and matching endpoints, closes each matching
edge exactly once, and checks the neighbor condition at every T vertex.
Only processed vertices adjacent to unprocessed vertices can gain new
neighbors, so forgetting older vertices loses no condition. These facts
prove soundness and completeness of the frontier enumeration.

Assign weight 2 to T vertices, 1 to matching endpoints, and 0 to unused
vertices. A terminal frontier has no pending matching edges. Its weight is
therefore exactly 2(|T|+|M|). Intermediate vectors permit edges awaiting the
next row, which is essential: they are not terminal optima.

For each frontier s, V_n(s) is the maximum doubled weight after n rows,
with unreachable states interpreted as minus infinity. The initial vector
is supported only at the all-zero state, with weight zero. The row transfer
Phi is independent of n and satisfies Phi(V+c)=Phi(V)+c. At each local
step it enumerates every legal assignment and takes a maximum on identical
frontiers. Thus it computes the stated V_n exactly using integer addition
and comparison.

At a row boundary no label 5 can remain. To compute Omega(G_(m,n)), take
half the largest entry of V_n whose state also has no label 4. The first
program checks that all such terminal weights are even.

## Translation certificates and the infinite conclusion

The saved vectors verify the following equalities entry by entry, including
identical reachable support:

| Width m | Starting length a | Period p | V_(a+p) - V_a | Reachable states |
| --- | --- | --- | --- | --- |
| 8 | 9 | 2 | 16 | 40,855 |
| 9 | 15 | 3 | 28 | 148,196 |
| 10 | 12 | 2 | 20 | 537,561 |
| 11 | 16 | 3 | 34 | 1,949,930 |

Homogeneity gives V_(n+p)=V_n+delta for every n>=a by induction, hence
Omega(G_(m,n+p))=Omega(G_(m,n))+delta/2. This is equality of entire vectors,
not an inference from repeated scalar optima.

The exact finite values for 1<=n<=a+p-1 agree with F(m,n). The target F has
the same scalar recurrence for n>=a. For widths 8 and 10 this follows
immediately from the parity formulas. For width 9, write the two terms as
A(n)=5*ceil(2n/3)+4*floor(n/3) and
B(n)=6*ceil(n/2)+3*floor(n/2). For n>=15,
A(n)>=14n/3 and B(n)<=9n/2+3/2, so A(n)>B(n).
Also A(n+3)=A(n)+14. This establishes the required recurrence without an
unbounded numerical check. The initial values and induction prove the
displayed theorem for all positive lengths.

At width 11, A(n)=6*ceil(2n/3)+5*floor(n/3) >= 17n/3 and
B(n)=8*ceil(n/2)+3*floor(n/2) <= 11n/2+5/2. Thus A(n)>B(n)
for n>=16, and A(n+3)=A(n)+17. The same induction applies.

## Validation and reproduction

- `grid_omega.cpp` constructs vectors and finds exact translations.
- `check_omega.cpp` separately enumerates candidate local assignments and
  recomputes vectors from the empty grid. It compares every saved entry at
  both endpoints of each certificate. Widths 3 and 7 are checked as controls.
- `check_small.py` exhaustively enumerates every matching and every allowed
  T for seven small grids, including 3-by-4, independently of frontier states.
- `verify_results.py` checks all 336 finite results: widths 1 through 10
  at lengths 1 through 30 and width 11 at lengths 1 through 36, against
  explicit lower-bound constructions,
  verifies vector translations, and writes a SHA256 manifest.

Run from this directory:

```sh
clang++ -std=c++17 -O3 -Wall -Wextra grid_omega.cpp -o /tmp/sahbi-grid-omega
clang++ -std=c++17 -O3 -Wall -Wextra check_omega.cpp -o /tmp/sahbi-check-omega
for width in 1 2 3 4 5 6 7 8 9 10; do
  /tmp/sahbi-grid-omega "$width" 30 "results/omega-w$width" > "results/omega-w$width.csv" 2> "results/omega-w$width.log"
done
/tmp/sahbi-check-omega 8 9 2 16 results/omega-w8
/tmp/sahbi-check-omega 9 15 3 28 results/omega-w9
/tmp/sahbi-check-omega 10 12 2 20 results/omega-w10
/tmp/sahbi-grid-omega 11 36 results/omega-w11 > results/omega-w11.csv 2> results/omega-w11.log
/tmp/sahbi-check-omega 11 16 3 34 results/omega-w11 > results/independent-w11.log
python3 check_small.py
python3 verify_results.py
```

Saved check results are in `results/independent-vector-check.json`,
`results/small-exhaustive-check.json`, and `results/verification-summary.json`.
The two implementations share the mathematical frontier specification;
they are not independent formal proofs of it. The soundness/completeness
argument above and the computations together form a computer-assisted proof.
The new strip results have not been kernel checked in Lean.

## Next scientific step

The certificates extend the known width range and give concrete material to
discuss with Sahbi. They do not supply a uniform-in-width boundary estimate.
The recurring patterns suggest examining which boundary configurations cause
the additive correction and whether an invariant can replace width-specific
state enumeration. No such invariant has yet been proved.

Before proposing a publication around these extensions, compare with the
author's actual verifier and any further work he knows. The downloaded v1
source archive contains the TeX file and 00README.json, but none of the
scripts or verification logs described in its data-availability section.
No standalone scientific-priority claim follows from this first exploration.
