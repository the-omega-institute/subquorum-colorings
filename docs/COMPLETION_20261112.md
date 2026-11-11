# Source-dependent TH completion: 12 November 2026

The [complete proof note](EXACT_TH_OPTIMIZATION_AND_LADDERS.md) gives five
results, with an exact integer implementation and independent controls:

1. Binary labels, fixed to one at selected white terminals and zero at
   other white terminals, and equal along actual and chosen auxiliary
   edges, minimize exactly the genuine TH expense. Label-one cycles can
   overcharge individual pairs but never improve the minimum. Every
   minimizing labelled pair gives a truly optimal full matching.
2. Deleting complete disjoint retained paths and adding their fixed
   expense gives the exact retaining problem, while allowing all remaining
   HH paths to reroute freely.
3. A standard frontier DP needs just the label and auxiliary matched bit
   per active vertex. At most h+1 vertices are active, for shorter bounding
   side h. It uses O(n 4^(h+1)) state transitions; tuple and integer-bit
   overheads are stated separately. It returns an optimum and full witness
   or reports infeasibility. This solves the unrestricted exact optimizer
   question left in the preceding residual-Hall notes at bounded width.
4. On every full 2-by-n ladder, any monochromatic selected Q set with at
   most one occupied neighbour per selected vertex has a zero-expense
   full completion. Disjoint adjacent-column swaps give a linear proof
   and construction for every n, arbitrary M and nonnegative weights.
5. On the full 3-by-6r grid, an explicitly feasible all-white-Q selection
   and four unit actual edges per block have exact optimum r. Each black
   centre needs its own paid component, and nine printed auxiliary edges
   per block attain the bound. Thus the height-two universal zero-expense
   conclusion cannot extend to height three.

## Reproduction

Run from the repository root:

```sh
python3 scripts/check_source_label_dp.py
```

The checker uses literal perfect-matching enumeration and overlay scoring,
not the DP recurrence, to determine small true optima. Its output records:

| Control | Exact scope |
| --- | --- |
| Rectangular models | 750 models, 37,659 full-N scores; 631 have feasible selected sets |
| Masked boards | 180 models, 279 full-N scores; 92 are infeasible |
| Alternative scans / value-only | 122 / 61 comparisons |
| Independent colour enumeration | 26 models |
| Full ladder actual-match enumeration | 10,992 matchings for n=1,...,8 |
| Selected subsets covered by maximal-T certificates | 79,016 combinations |
| Ladder DP / translation and transpose controls | 114 / 228 |
| Full versus retaining 2-by-4r | 36 controls, r through 128, 1,024 vertices |
| Positive 3-by-6r family | 18 controls, r through 128, 2,304 vertices |

The controls include zero and 401-bit actual weights, a positive-cost
ladder violating the neighbour condition, an infeasible retained-path
example and a balanced board with an isolated vertex. Finite tests check
implementation; all-size statements have the written proofs above.
No Lean execution or verification is claimed.

## Scope and review

The proof/source snapshot 4a3aa6e was sent through oracle-broker for an
independent audit of Theorems 1–4, the retained adapter and cascade
application. The later height-three result is outside that initial input;
review status and exact source/response bindings are recorded separately
in `output/source-label-dp-review.json` when available. No review verdict
is inferred from dispatch or a local PASS report.

The earlier forced-cascade review and its identical retry both ended with
terminal infrastructure failures and no mathematical response. The prior
positive-attainment equivalence and unit 18-by-18 optimizer-choice result
retain their existing ACCEPT, scoped to their original input.

The general grid triple equality, a universal 5/6 coefficient improvement,
a simpler incomplete-core equality description, and sharp simultaneous
degree/connectivity optima remain research questions. The new optimizer
is exponential in width; no arbitrary-width polynomial claim is made.
The sharp bipartite n/10 gap theorem and previous composition manuscript
are preserved. No email, submission or submitted-version edit is implied.
