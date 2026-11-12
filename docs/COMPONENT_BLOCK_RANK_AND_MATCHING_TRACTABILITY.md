# Component-block cycle rank and the P2/P4 complexity boundary

13 November 2026. The primary-cost hardness construction uses only P2/P4
ambient components. This companion result explains why P2 alone is a
different algorithmic class. It also sharpens the cycle-rank parameter by
separating independent candidate-component blocks. This is a standard
factorization of the preceding exact frontier algorithm, not an
unrestricted graph-parameter complexity classification.

## 1. Factorization over connected candidate blocks

Let A be a finite simple bipartite graph of maximum degree at most2, U a
fixed initial set, and (x_i,y_i) a fixed list of replacements with distinct
x_i in U and distinct y_i outside U. All subfamilies are allowed; there is
no final-isolation condition. Write U_S=(U minus {x_i:i in S}) union
{y_i:i in S}, and F(t)=min_{|S|=t} nu(A[U_S]).

The candidate multigraph K has one vertex per complete ambient component
of A and one edge per replacement; loops and parallel edges are retained.
Let K_j be its connected blocks, including isolated vertices. Let N_j be
the number of ambient vertices in block j, q_j its candidate count, and
k_j=q_j-|V(K_j)|+1 its cycle rank. Put q=sum q_j, N=sum N_j, and
kappa=max_j k_j, taking kappa=0 when N=0.

**Theorem1.** The complete exact-count frontier and explicit batches, final
covers and matchings can be computed in

    O(sum_j 2^k_j N_j(q_j+1)^2 + N(q+1) + q^2)
    <= O(2^kappa N(q+1)^2)

arithmetic transitions for N>=1. The empty instance has a single zero-cost
row. Masks, indices and witness bit operations have polynomial bit overhead.
The exponent depends on the largest block cycle rank rather than their sum.

**Proof.** No ambient edge crosses blocks, since each block consists of
complete ambient components. No replacement crosses blocks by the definition
of K. Every global S therefore has a unique decomposition into local S_j,
with |S|=sum |S_j| and

    nu(A[U_S])=sum_j nu(A_j[U_{S_j}]).

Conversely any local choices combine into an allowed global choice. The
previous [cycle-rank algorithm](COMPONENT_CYCLE_RANK_FRONTIER.md) computes
each F_j in O(2^k_j N_j(q_j+1)^2) transitions. Combine these by exact min-plus
convolution F(t)=min_{sum t_j=t} sum F_j(t_j), retaining the disjoint candidate
masks. Every candidate contributes once in one local block and once to its
global mask; the convolution never charges an auxiliary edge from another
block. For blocks with q_j>0 the convolution work is O(q^2): pairwise cross
terms sum to at most q^2, and there are at most q such blocks. Blocks with
q_j=0 contribute a single fixed cost and take O(q+1) work apiece, hence
O(N(q+1)) total. Local covers and matchings unite because the blocks are
vertex-disjoint, or the final batch can be certified once on A. The displayed
coarser bound follows from q_j<=q and sum N_j=N. QED.

This is an algorithmic refinement, with no claim that kappa is the smallest
possible parameter or that all large-kappa inputs are hard.

## 2. A polynomial class at the smallest ambient component size

**Corollary2.** If every ambient component is an isolated vertex or P2,
the complete exact-count frontier is polynomial-time computable, even when
the total cycle rank of K is arbitrarily large.

**Proof.** Each ambient vertex belongs to at most one candidate endpoint:
the removals are distinct, the additions are distinct, and their sets are
disjoint. Thus an ambient component of order at most2 contributes at most
two incident candidate half-edges. A loop consumes both of them. K has
maximum degree at most2, with loops counted twice. Every connected block
is an isolated vertex, a path, or a cycle (including a loop or a parallel
two-edge cycle). Hence k_j<=1. Apply Theorem1. For a physical template with
one individually permitted replacement per distinct owner, all subsets and
prefixes stay permitted, so its final batches give actual dissociation
certificates of size3b-cost as before. QED.

For a concrete separation from the former total-rank bound, use r disjoint
ambient pairs (a_j,b_j), with U={a_j}, and candidate a_j->b_j on every pair.
K has r isolated loop blocks and total rank r, whereas kappa=1. Every batch
has cost0; the algorithm outputs all r+1 rows using only two conditioned
branches per block. This example concerns the auxiliary optimization domain;
no physical embedding or lower bound for arbitrary algorithms is claimed.

Together with the [primary NP-completeness reduction](UNBUDGETED_PRIMARY_EXCHANGE_HARDNESS.md),
this yields a precise small-component distinction: P2-only auxiliary graphs
admit a polynomial exact algorithm, while permitting both P2 and P4 suffices
for primary NP-completeness, even in the stated two-connected bipartite
physical domain. These are fixed-list results. They neither settle SF/beta
complexity nor strengthen the universal graph or rectangular-grid bounds.

## 3. Reproduction

The implementation is [blockwise_component_frontier.py](../develop/blockwise_component_frontier.py).
Run `python3 -B scripts/check_blockwise_component_frontier.py`. Its checker
uses literal candidate subsets and an independent subset-matching recursion,
tests loops/parallel edges, isolated ambient vertices, empty instances,
one-shot inputs, candidate permutations and many disconnected cycle blocks.
Finite checks supplement the general factorization proof.
