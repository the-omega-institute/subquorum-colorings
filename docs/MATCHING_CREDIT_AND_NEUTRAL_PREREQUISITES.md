# Matching-owned credit with zero-credit prerequisites

A replacement can help a coordinated batch even when its removed point is
unmatched and contributes no direct saving. Fixing a tight matching/cover pair
assigns each saving to one original matching edge, while allowing unmatched
removals as prerequisites. The final certificate can also retain edges at added
points: isolation of every addition is unnecessary. This rule reaches cost zero
on both all-scale barriers to the earlier exact-one-saving-per-removal rule.

## A tight matching/cover transfer

Let A be a finite simple graph, U a subset of its vertices and G=A[U]. Supply
a vertex cover C of G and a matching M of G such that

$$ |M|=|C|=\nu_0. $$

Matching weak duality proves that both certificates are optimal. Every edge of
M has exactly one endpoint in C, and M saturates C: each matching edge needs
a distinct cover point, and equality leaves no unused point or double use.
Write I=U\setminus C. In particular I is independent, although C need not be.
These assertions require only the supplied tight pair, not bipartiteness of A.

Specify candidate replacements x_i\mapsto y_i with distinct x_i in I and
distinct y_i outside U. Define credit w_i to be one if x_i is matched in M,
and zero otherwise. For a batch S put

$$
 X_S=\{x_i:i\in S\},\quad Y_S=\{y_i:i\in S\},\quad
 R_S=\{M(x_i):i\in S,\ w_i=1\},
$$
$$
 U_S=(U\setminus X_S)\cup Y_S,\qquad C_S=C\setminus R_S,
 \qquad M_S=\{e\in M:e\cap X_S=\varnothing\}.
$$

Here M(x) is the mate of a matched point. A retired cover point remains in
U_S; it leaves only the proposed cover.

**Theorem 1.** If C_S covers A[U_S], then

$$
 \boxed{\nu(A[U_S])=\nu_0-\sum_{i\in S}w_i},\qquad
 |M_S|=|C_S|=\nu(A[U_S]).                         \tag{1}
$$

**Proof.** Each positive-credit removal is outside C and owns its unique
incident M-edge. Distinct removals own different edges: an M-edge has only
one endpoint outside C. Their cover mates are also distinct. Thus exactly
sum w_i matching edges and cover points are deleted from the certificates.
All edges of M_S still lie in U_S, and by hypothesis C_S is a cover there.
Their equal sizes give the matching lower and cover upper bounds in (1). ∎

There is no duplicated per-component surplus. Every positive credit records
a different edge of the fixed initial matching; zero-credit removals consume
no such edge. The theorem concerns the batch endpoint. It does not assert
that each replacement has its credit as its sequential cost decrease, or
that an arbitrary batch admits a nonincreasing execution order.

## Exact dependencies and conflicts

Let d(u) be the candidate removing u, when present. A cover point c has a
retirement trigger t(c) precisely when its M-mate is some x_j; then t(c)=j.
Compile these conditions, with implication i→j meaning that choosing i
requires choosing j. A conflict forbids choosing both endpoints; a self
conflict permanently blocks its label.

1. For an old edge c-u with c in C and u in I, retiring c requires removing
   u. Add t(c)→d(u), or block t(c) if d(u) is absent.
2. For an old edge c-d within C, the retirement triggers of c and d conflict
   when both exist. If either endpoint has no trigger, it always stays covered.
3. For an edge y_i-u with u in I, add i→d(u), or block i if d(u) is absent.
4. For an edge y_i-c with c in C, i conflicts with t(c), when that trigger
   exists. If it is i itself, block i.
5. For an edge y_i-y_j, the labels i,j conflict.

Self implications are harmless and allowed. Multiple reasons for the same
constraint do not add credit or capacity.

**Theorem 2.** A batch S is closed under these implications, contains no
blocker and contains no conflict pair if and only if C_S covers A[U_S].

**Proof.** Initially every old edge touches C. If both endpoints are in C,
it becomes uncovered exactly when both cover points are retired, which is
case 2. If just c lies in C, it becomes uncovered exactly when c is retired
and its other endpoint survives; this is case 1. These are all old edges
that can survive. For an edge from a chosen addition to an initial point,
the initial point either lies in I and must be removed (case 3), or lies in
C and must not be retired (case 4). Neither endpoint of an edge between two
chosen additions belongs to C_S, giving case 5. Edges to unchosen additions
or other points outside U_S do not occur in the final induced graph.
This exhausts the possible final edges and proves both directions. ∎

The old C-C case is essential. For example use indices 0 through 7,
P={01,23,45,67}, Q={12}, and owner squares (0,4,1,5), (2,6,3,7).
The physical colours (0,0,1,1,1,1,0,0) satisfy the model. Start with
U={0,1,2,3}, C={1,2}, M={01,23}. The individually permitted operations
0→4 and 3→6 would retire both cover points. The old edge 12 survives,
so their labels must conflict. Either singleton has cost one; both also
have actual cost one, although incorrectly dropping this conflict would
give a false zero-cost certificate.

Additions need not be isolated. With the same P and owner squares, instead
take Q={24}, physical colours (1,1,1,1,0,0,0,0), U={0,1,2,3},
C={0,2}, M={01,23}. The permitted operation 1→4 retires 0. The retained
cover {2} covers both 23 and 24, and the surviving matching {23} certifies
cost one, down from two. Added point 4 has a final neighbour 2.

## Exact optimization with a small conflict cover

The following optimization also permits arbitrary nonnegative integer weights
w_i on labels; physical matching credits in Theorem 1 remain only zero or one.
These general weights are not weighted physical matching costs.

Let H be the conflict graph and K a vertex cover of H, with k=|K|.
For each of the 2^k choices F=S∩K:

* Reject F if it contains a conflict pair.
* Exclude all blockers, K\setminus F, and every conflict neighbour of F.
  Propagate exclusions backwards through all implications.
* Reject the choice if an element of F is excluded. Otherwise let L_F be
  all labels still available.
* Return the forward dependency closure of F together with every positive
  weight label of L_F. Call this trimmed batch T_F.

**Theorem 3.** L_F is the greatest feasible batch with intersection F on K.
Its weight is maximal for that intersection. T_F has the same weight and is
the unique minimum-cardinality maximum-weight batch for that intersection.
Choosing the largest weight, then smallest cardinality, among all T_F is
globally optimal for the compiled rule, in time 2^k times a polynomial in
the input size, including the integer bit lengths.

**Proof.** Every excluded label is impossible: the initial exclusions follow
from the fixed F or feasibility, and any predecessor of an impossible label
is itself impossible. Hence every feasible batch with this F is contained
in L_F. The complement of a predecessor-closed exclusion set is closed under
forward implications. No conflict remains inside L_F: there are no edges
outside K, all neighbours of F were excluded, and F itself is independent.
Also L_F∩K=F and no blocker remains. Thus L_F is feasible and greatest.

Nonnegative weights make L_F optimal. To achieve its weight, every surviving
positive-weight label must occur, since omitting one loses positive weight
and no unavailable label can replace it. Every feasible batch with the fixed
intersection also contains F and their full dependency closure. That closure
is T_F, is contained in L_F, is feasible, and has its full weight. It is
therefore the unique smallest optimal batch for this intersection.
Enumerating every intersection covers every feasible batch. ∎

The implementation obtains a default K from all endpoints of a greedy
maximal matching in H. These endpoints cover H, and any vertex cover must
meet each of the disjoint matching edges. Thus k≤2τ for the minimum conflict
cover size τ, giving a 4^τ polynomial-time bound without computing τ.
When there are no conflicts there is just one assignment. A large conflict
cover can make this algorithm exponential; no unrestricted polynomial
optimization claim is made. Across different F there may be tied optimal
batches, so global uniqueness is not asserted.

## Physical certificate

Use the helper/witness/owner model of
[cover-saturated exchanges](COVER_SATURATED_COORDINATED_EXCHANGES.md).
There are N=2b indices, a perfect matching P, a partial matching Q and
A=P∪Q. Owner edges B form paths or even cycles. The physical colours give
P equal-colour endpoints and Q,B opposite-colour endpoints; they need not
be an A-bipartition. Every A-cycle alternates the two matchings and is even.
An omission U is permitted when B[V\setminus U] has maximum degree at most
one. The exact all-helper objective is

$$ \beta_I=3b-\min_{U\ \mathrm{permitted}}\nu(A[U]). $$

Require U initially permitted, at most one candidate from each connected
owner component, and each individual replacement permitted in its component.
Then every subset of candidates, including every sequential prefix, is
owner-permitted: on each component it agrees with U or its one individually
verified replacement. All original cover points remain in the omission,
because each removal is outside C.

For the optimal compiled batch, Theorem 1 supplies M_S,C_S. Select all b
helpers, the owners indexed by V\setminus U_S and the witnesses indexed by
U_S\setminus C_S. The latter set is A-independent. Each selected witness
has its single selected helper neighbour, no helper has two selected witness
neighbours, and no Q-edge has two selected witness endpoints. No selected
owner has its indexed witness selected, and its selected B-degree is at most
one. This is a physical dissociation set of size

$$ 3b-|C_S|=3b-\nu_0+\sum_{i\in S}w_i. $$

No matching computation on the final omission is necessary. The implementation
may compute the initial pair when it is not supplied. With several operations
in one owner component, individual permittedness would no longer suffice;
that case is outside this wrapper's contract.

## All-scale escapes from the earlier barriers

**Plateau family.** For every m≥1, use the two-connected 20m-vertex family
of the [unbounded plateau note](UNBOUNDED_NEUTRAL_EXCHANGE_PLATEAU.md).
There are 8m indices, b=4m, A=C_(8m) with its natural consecutive edges.
In each block j write v_t=8j+t. Its owner squares, in cyclic order, are
(v_0,v_6,v_1,v_7) and (v_2,v_4,v_3,v_5), and the initial omission is
{v_1,v_2,v_3,v_6}. Take C={v_2:all blocks} and M={v_1v_2:all blocks}.
The initial cost is m. Specify two operations per block:

$$ v_1\mapsto v_0\quad(w=1),\qquad v_3\mapsto v_4\quad(w=0). $$

Each belongs to its different owner square and is permitted. Retiring v_2
requires removing both v_1,v_3, hence the positive-credit operation requires
the zero-credit one. Added v_0 requires removal of v_1, and added v_4
requires removal of v_3. Their other neighbours v_(previous block,7),v_5
are absent from every final omission. No conflict occurs, and these are all
nontrivial conditions. Selecting all 2m operations is feasible, has credit
m and final omission exactly the even indices. Its empty cover and matching
prove cost zero and the exact all-helper value β_I=12m. The earlier rule
allowing only removals in a minimum cover had no nonempty applicable batch.
Here exactly m unmatched removals supply its missing prerequisites.

**Shared odd-path family.** For even r≥4 use N=4r, b=2r, A=C_(4r),
physical colour floor(v/2) modulo 2, and owner squares

$$ K_i=(2i,\ 2r+2(i\mathbin{\mathrm{xor}}1),\ 2i+1,
                 \ 2r+2(i\mathbin{\mathrm{xor}}1)+1),\quad 0≤i<r. $$

Start at U={1,…,2r-1}∪{2r+2}, C={2,4,…,2r-2} and
M={12,34,…,(2r-3)(2r-2)}. Its cost is r-1. Use

$$ 1\mapsto0,\qquad 3\mapsto2r,\qquad
 2i+1\mapsto2r+2(i\mathbin{\mathrm{xor}}1)\quad(2≤i<r). $$

Each is in K_i and is a permitted replacement. Every removed odd point is
outside C; all except 2r-1 are matched. Selecting all r candidates leaves
exactly the even indices, retires all r-1 cover points, and has no uncovered
edge. The compiler is exact, so this batch is feasible. In fact its conflict
graph is empty: C and all additions are even and hence mutually nonadjacent;
all old/new edges into the remaining initial odd points give implications.
Every candidate of positive credit is selected by the optimizer, and the
retirement of 2r-2 requires removing its neighbour 2r-1, forcing the one
zero-credit candidate too. Thus one conflict assignment selects all r
operations, gives cost zero and β_I=6r. The earlier all-cover exact-deletion
rule had sharp cost one on this same family.

**Cyclic dependency family.** For r≥3 reuse
[the cyclic construction](COVER_SATURATED_COORDINATED_EXCHANGES.md), with
A=C_(4r), U={4i,4i+1:0≤i<r} and the prescribed operations
4i+1→4(i+1)+2, cyclically. Use C={4i} and M={4i(4i+1)}.
All removals are matched outside C. The old isolation dependencies now give
a cyclic implication system; all r candidates are feasible together and
have total credit r, leaving an independent omission and cost zero. No
zero-credit operation is needed in this particular family.

These are analytic proofs at every stated scale. The inherited physical
families and their bipartiteness, degree bounds and two-connectivity were
proved in the linked notes. The new conclusions concern the complementary
exchange rule, not a new universal numerical dissociation bound. The old
barrier families already satisfy the proposed 8b/3 threshold.

## Scope and a reproducible limitation

This rule fixes C, M and a list of operations whose removals lie outside C.
It optimizes certificates using exactly C_S, not every possible final cover.
It complements the earlier rule that removes points inside a minimum cover;
neither statement says it dominates all other physical exchanges.

A 20-vertex physical example makes the fixed-cover limitation explicit.
Use b=4, P={04,26,37,15}, Q={07,41,25,63}, owner squares
(0,7,4,1),(2,5,6,3), and colour v modulo 2. Let U={0,2,5,7},
C={0,2}, M={07,25}, with candidates 7→4 and 5→3 in the two squares.
The first is blocked: it retires 0 but adds its neighbour 4. The second
requires the first to remove 7, because its addition 3 is adjacent to 7.
The rule therefore selects nothing and certifies cost two. Physically,
5→3 alone yields the path 0-7-3 and isolate 2, of cost one, covered by
{7} instead of the inherited {0}. The four candidate subsets have costs
2,2,1,1, so the actual fixed-list optimum is one. Choosing a different
initial cover can help, but is not part of Theorem 3's fixed input.

## Verification and review

Run the unchanged assertion-enabled checker from the repository root:

```sh
python3 -B scripts/check_matching_credit_exchange.py
```

The report is [matching-credit-exchange-check.json](../output/matching-credit-exchange-check.json).
It tests every simple graph through four vertices, every induced U, every
tight matching/cover pair, and every partial injection from U\setminus C
to its complement: 5,209 compiler models, 9,646 subsets and 7,671 literal
matching/cover transfers. The optimizer is compared with brute force over all
implication/conflict/blocker/binary-credit systems through three candidates,
plus seeded larger systems through ten candidates. There are 33,126 weighted
models, 66,709 optimizer runs and 176 large-integer controls.

Physical validation checks 260 full matching/cover/dissociation certificates,
17,874 candidate subsets in 180 fixed-list models, explicit nonisolated and
old-cover-conflict fixtures, and 27 plateau, 26 odd-path and 25 cyclic scales
through parameters 128. All 180 rule optima agree with literal certificate
enumeration. In 166 cases they also attain the actual fixed-list minimum;
14 have a gap, with the first fully preserved in the report. These gaps are
not discarded or labelled theorem failures. No Lean execution, literature
priority claim or universal 8b/3, unit-weight 5/6 or general rectangular-grid
triple-equality proof is provided by this milestone.

The independent exact-source audit and its actual execution scope are recorded
separately in [the review receipt](../output/matching-credit-exchange-review.json).
