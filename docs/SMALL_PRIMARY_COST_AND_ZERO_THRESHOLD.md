# Zero primary cost and exact small-cost decisions

13 November 2026. This note adds two standard algorithmic consequences to
the fixed-list complexity boundary: zero cost is a 2-SAT question, and any
fixed cost threshold has a polynomial exhaustive-cover algorithm. No
novelty or fixed-parameter tractability claim is made for these elementary
reductions.

## 1. Zero cost

Let A be a finite simple graph, U an initial set, and (x_i,y_i) a fixed list
with distinct x_i in U and distinct y_i outside U. Every subfamily is
allowed. Introduce bit s_i for operation i. A vertex's membership in U_S
is either a constant, 1-s_i at x_i, or s_i at y_i. Therefore

    nu(A[U_S])=0
    iff every edge ab has not(present(a) and present(b)).

After substituting the constants, each edge gives a clause with at most two
literals. A constant-absent endpoint makes the clause vacuous; two
constant-present endpoints give an empty clause. If the same candidate
occurs at both ends, its opposite membership literals make the clause
vacuous. All other clauses are exactly equivalent to forbidding the edge
with both endpoints selected. Thus satisfiability of this 2-CNF is necessary
and sufficient for zero cost. A satisfying assignment gives a batch; an
unsatisfiable implication graph gives either an empty clause or paths
between a variable and its negation in both directions. Every implication
comes from a specific ambient edge. These are checkable obstructions to
zero cost for the fixed list. This equivalence requires neither
bipartiteness nor a bound on A's degree.

The implementation reuses the existing SCC-based 2-SAT solver. Its sorted
adjacency traversal has polynomial overhead; no strict linear-time claim
is made for that implementation.

## 2. Small positive cost

Now assume A is bipartite and let B>=0 be a primary-cost threshold. By
matching/vertex-cover duality,

    exists S: nu(A[U_S])<=B
    iff exists Z subset V(A), |Z|<=B, exists S: U_S minus Z is independent.

Indeed a final minimum cover is one such Z in the forward direction; in
the reverse direction Z intersect U_S covers every final edge, bounding its
matching number by |Z|. For each Z enumerate the preceding 2-SAT clauses
on edges whose endpoints both avoid Z. Satisfiability gives a batch with
cost at most B. Failure for all such Z proves that no batch reaches B.
The algorithm uses at most sum_{j=0}^{min(B,N)} binom(N,j) SCC tests, each
polynomial in N+|E(A)|+q, plus final certificate extraction. It is polynomial
for every fixed B and is an XP algorithm in B. This does not claim FPT
running time f(B)N^c with c independent of B.

The returned batch need not minimize the number of operations or its actual
cost below B: the contract is feasibility at threshold B. The implementation
currently validates the bipartite maximum-degree2 auxiliary domain and
returns an actual final matching, tight cover and selected operations there.
It returns the first zero-threshold obstruction for diagnosis. In a failed
positive-threshold query it reports the number of exhaustive tests; it does
not package all their individual unsatisfiability certificates into a short
NP certificate.

## 3. Meaning of the complexity boundary

The [primary NP-completeness construction](UNBUDGETED_PRIMARY_EXCHANGE_HARDNESS.md)
uses an input-dependent positive threshold. It is consistent with the
polynomial zero-threshold test and the XP algorithm. Its all-subsets optimum
equals tau(H), so this family can have cost0 precisely when the source H has
no edges. No hard zero-cost decision, operation budget or secondary
minimum-operation optimization follows from that construction.

In the physical domain, the candidate list must still consist of one
individually permitted replacement per distinct owner. Then every returned
batch and prefix is permitted, and the usual3b-cost all-helper dissociation
certificate follows. This does not extend the search to all omission
states, nor settle unrestricted SF/beta or rectangular-grid complexity.

Implementation: [small_primary_cost.py](../develop/small_primary_cost.py).
Run `python3 -B scripts/check_small_primary_cost.py` for independent literal
matching/assignment comparisons and edge-traced SCC obstruction checks.
