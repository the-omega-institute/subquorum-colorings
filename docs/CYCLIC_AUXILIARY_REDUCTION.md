# Reducing the universal all-helper target to cyclic physical templates

13 November 2026. A two-copy completion removes auxiliary paths. A four-copy
completion also removes owner paths, including isolated owners. Both retain
the actual physical colouring, matching degrees and all original edges in
each copy. They reduce the universal target; they do not prove the remaining
mixed-cycle inequality.

## 1. Exact formulation

Use N=2b indices, a perfect helper matching P, a partial witness matching Q,
and A=P union Q. The physical colouring c is constant on P and changes on
Q and owner edges B. The owner graph B has maximum degree two, hence paths
and even cycles. Define

    tau(A,B) = min {nu(A[U]): Delta(B[V minus U])<=1}.

The established identity beta_I=3b-tau makes the universal target equivalent to

    tau(A,B) <= floor(N/6).                                  (1)

Every auxiliary path has even order, begins and ends with P, and has exactly
two Q-unmatched endpoints. Every auxiliary cycle has order divisible by four:
its P,Q edges alternate, and the number of colour-changing Q edges is even.
The auxiliary bipartition used for matching is distinct from physical c.

**Theorem1 (two copies).** Assertion1 for all physical templates is equivalent
to assertion1 restricted to templates with Q perfect, or equivalently with A
a union of cycles C_(4k).

**Theorem2 (four copies).** Assertion1 for all physical templates is equivalent
to assertion1 restricted to templates with Q perfect and B a union of even
cycles. On every nonempty such physical graph helpers have degree2, and all
witnesses and owners have degree3. In particular its minimum degree is2 and
maximum degree3. No regularity assertion for all actual vertices is intended.

## 2. Two-copy physical auxiliary completion

Take copies V_0,V_1 of V, with colouring

    c_hat(v_j)=c(v) xor j,       j in {0,1}.

Copy all original P,Q,B edges internally; keep the owner graph exactly two
disjoint copies of B. For each original auxiliary path of order m:

| Original path | Endpoint colours | New Q edges | Completed components |
|---|---|---|---|
| P_(4k), k>=1 | Opposite | Join its ends inside each copy | Two C_(4k) |
| P_(4k+2), k>=0 | Equal | Join each end to its corresponding end in the other copy | One C_(8k+4) |

Indeed, along the path there are m/2-1 Q edges, and only those edges change
physical colour. The parity therefore gives the two endpoint claims. In the
second row corresponding vertices have opposite colours by complementation.
The case m=2 produces a simple four-cycle, with no repeated edge. The first
row has m>=4, so its endpoints were not already adjacent.

Keep the original auxiliary cycles. Every previously Q-unmatched endpoint
receives exactly one new edge, and no other endpoint receives an edge. Thus
Q_hat is perfect, P_hat remains perfect, their colours have the required
relations, and A_hat is a union of C_(4k). All original edges remain present.
The completed physical graph has 2b helpers and 10b vertices, and remains
bipartite with maximum degree3. This comparison object is constructed without
requiring any unproved cyclic certificate.

## 3. Exact transfer and integer rounding

Suppose U_hat is any permitted omission in a completion on t original copies,
with all original A and B edges retained in each copy. Extra inter-copy B
edges are allowed in this statement. Define U_j by restriction to copy j.
Then U_j is permitted, since removing vertices and edges cannot increase
induced owner degrees.

Let M_j be a maximum matching in original A[U_j]. Its copied edges are present
in A_hat[U_hat]. The t copies have disjoint vertices; hence their union is
one matching. Therefore the exact transfer inequality is

    sum_j nu(A[U_j]) <= nu(A_hat[U_hat]).                     (2)

It does not claim that original matching costs equal the completed cost:
the added edges can strictly increase the latter. Each actual edge belongs
to its unique copy; there is no independently allocated per-component credit.

If the completed certificate meets its target on tN indices, choose the
cheapest original copy. Its integer cost satisfies

    min_j nu(A[U_j])
      <= floor(nu(A_hat[U_hat])/t)
      <= floor(floor(tN/6)/t)
       = floor(N/6).                                        (3)

For any real x and positive integer t, floor(floor(tx)/t)=floor(x), as seen by
writing x=q+r with integer q and 0<=r<1. Thus no divisibility or rounding
assumption about b is missing. Taking t=2 proves Theorem1; its reverse
implication is the restriction of a universal assertion.

Recompute maximum independent witnesses T in ORIGINAL A[U_j]. Since A[U_j]
is bipartite, |T|=|U_j|-nu(A[U_j]). Selecting all b original helpers, those
witnesses, and original owners V minus U_j gives an actual dissociation set
of size3b-nu(A[U_j]). Physical validity uses only original edges. In
particular no invalid mixed identity beta_I=2b+h is used.

**Short-class alternative.** When original A has only P2/P4/C4 components,
the two-copy completion consists only of squares. The square theorem
therefore proves1 outright. In fact its [path-surplus refinement](SHORT_AUXILIARY_COMPLETION_AND_PATH_SURPLUS.md)
has R(B_hat)=2R(B), so the completed cost is at most
floor((2N-2R(B))/6). Applying2 and the same nested floor gives

    min_j nu(A[U_j]) <= floor((N-R(B))/6).

This is a second proof of the physical short-component theorem, avoiding the
single-ghost construction; the latter additionally covers colour-free inputs.
The original two-copy auxiliary reduction and this basic short-class route
were supplied in an independent Oracle research answer. The four-copy owner
closure below is a subsequent deduction. These are provenance statements,
not literature-priority claims.

## 4. Closing every owner path with four copies

Take four copies, j=0,1,2,3, with c_hat(v_j)=c(v) xor(j mod2).
Perform the auxiliary completion of Section2 separately in pairs(0,1) and
(2,3). Q_hat is now perfect and every auxiliary component is C_(4k).

Keep all original B edges. For each owner component:

* If it is already an even cycle, keep all four copies unchanged.
* If it is a path of order l>=2 with ends x,y, add owner edges x_0x_1,
  y_0y_1 and x_2x_3,y_2y_3. The first pair of copies becomes one simple
  cycle of order2l, as does the second. This includes l=2, giving C4.
* If it is an isolate v, add v_0v_1,v_1v_2,v_2v_3,v_3v_0. This is one
  simple C4, and supplies its two missing owner neighbours without parallel
  edges. Two copies alone could not close an isolated owner in this manner.

All added edges join corresponding vertices in opposite-coloured copies.
Every nontrivial path endpoint receives exactly one additional edge; every
isolate receives two; original internal path vertices retain degree2.
Distinct original owner components have disjoint vertices, so the additions
are simple and nonconflicting. Consequently B_hat is a disjoint union of
even cycles. It retains every original B edge, although it is no longer the
disjoint union of the four original owner graphs.

The completed physical graph has4b helpers and20b vertices. Each helper has
degree2. Each witness has its helper, owner and one Q neighbour, and each
owner has its witness and two B neighbours. Bipartiteness follows from the
explicit colouring. Applying2-3 with t=4 proves Theorem2. No estimate of
owner dissociation by averaging across separate owner paths is required.

## 5. Exact remaining scope

In the completed class, tau is additive over connected components of A unionB:
permission is independent between them, and matching numbers add. Their
index orders are divisible by four, since each is a union of whole auxiliary
cycles. If every such component meets1, then

    sum tau_i <= sum floor(N_i/6) <= floor(sum N_i/6).

Therefore any counterexample has a connected component that is itself a
counterexample. By the [all-square theorem](ALL_OWNER_AUXILIARY_SQUARES.md)
and the [no-auxiliary-C4 theorem](OWNER_MATCHING_AND_FOUR_CYCLE_OBSTRUCTIONS.md),
that component must contain BOTH an auxiliary C4 and an auxiliary C_(4k)
with k>=2. These theorems apply to arbitrary owner paths/even cycles, hence
to the completed owner-cycle domain.

Thus, if the universal physical target is false, a counterexample exists with
A unionB connected, Q perfect, B2-regular, and both short and long auxiliary
cycles. Its physical graph is connected, bipartite, with the degree pattern
of Theorem2. There is no claim that every original failure stays connected
under completion, or that the minimum counterexample has unchanged order.

This narrows the unsolved existence problem. It does not prove the cyclic
mixed target, exhibit a failing physical instance, settle an unrestricted
sharp graph-gap constant, or improve unit-weight grid5/6. General safe
composition and geometric multiple-Hall routing remain separate objectives.

## 6. Constructor and verification

[cyclic_auxiliary_reduction.py](../develop/cyclic_auxiliary_reduction.py) returns
the completed template, every added Q/B edge, all original-copy matching
costs, the chosen copy, and its actual original owner/witness certificate.
The transfer API requires a completed target certificate by default; it does
not silently fabricate one for an unsolved longer-cycle instance. Its optional
non-target mode certifies2 for any permitted supplied omission.

Run `python3 -B scripts/check_cyclic_auxiliary_reduction.py`. Independent
physical adjacency reconstruction, literal matching recurrences, complete
small physical inputs and permitted completed omissions, every path parity,
isolates, crossing owner components and exact square constructions test the
implementation. General proofs above establish the reductions at all orders;
finite tests do not decide the remaining cyclic conjecture. Exact execution
scope, source identity and independent review are recorded separately.
