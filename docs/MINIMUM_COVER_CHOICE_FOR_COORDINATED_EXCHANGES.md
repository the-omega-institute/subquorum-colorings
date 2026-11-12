# Choosing the minimum cover for a specified coordinated batch

The [cover-saturation theorem](COVER_SATURATED_COORDINATED_EXCHANGES.md)
characterizes deletions saving one matching edge each and solves the largest
isolating batch for a fixed minimum cover. In the physical model, its auxiliary
graph has maximum degree two. This permits an explicit catalogue of **all**
minimum covers and an exact optimization over cover choice for a specified
candidate list. The enumeration can be exponential; the completeness statement
concerns the stated certificate rule, not arbitrary physical exchanges.

## All minimum covers of paths and even cycles

Let $H=A[U]$ be bipartite of maximum degree two. Number the vertices of each
path or cycle consecutively, starting at an endpoint for a path.

* An odd path $v_0,\ldots,v_{2k}$ has exactly one minimum cover,
  $\{v_1,v_3,\ldots,v_{2k-1}\}$. This includes the empty cover for an isolate.
* An even path $v_0,\ldots,v_{2k-1}$ has exactly $k+1$ minimum covers,

  $$
  C_t=\{v_{2j+1}:0\le j<t\}\cup\{v_{2j}:t\le j<k\},
  \qquad 0\le t\le k.                                    \tag{1}
  $$

* An even cycle has exactly two minimum covers, its two bipartition sides.

**Proof.** An odd path has matching number $k$. A minimum cover cannot
contain $v_0$: the remaining path $v_1,\ldots,v_{2k}$ already needs $k$
cover vertices. Thus it must contain $v_1$. Remove $v_0,v_1$ and induct
on the remaining odd path. The case $k=0$ is immediate.

On the even path, the matching $v_0v_1,v_2v_3,\ldots,v_{2k-2}v_{2k-1}$
is perfect. Every minimum cover contains exactly one endpoint of each
matching edge. Encode the choice in pair $j$ by zero for $v_{2j}$ and one
for $v_{2j+1}$. The intervening edge $v_{2j+1}v_{2j+2}$ forbids a zero
followed by a one. Hence every choice word is $1^t0^{k-t}$, giving exactly
(1). On an even cycle the closing edge forbids the same transition around
the circle. The only possibilities are the two constant words. ∎

Choices on distinct components are independent. If the even path components
have orders $2k_1,\ldots,2k_p$ and there are $c$ cycle components, the
exact number of minimum covers is

$$
 L=2^c\prod_{j=1}^p(k_j+1).                              \tag{2}
$$

Odd paths contribute no factor. The empty graph has one empty cover.
The catalogue can be generated with polynomial delay and polynomial working
storage; storing all covers at once is unnecessary. No polynomial bound on
$L$ as a function of graph order is asserted.

## Exact optimization over all covers for fixed candidates

Fix a permitted $U$ and a list of owner operations $(K_i,x_i,y_i)$ with:

1. Different owner components $K_i$, with $x_i\in U\cap K_i$ and
   $y_i\in K_i\setminus U$.
2. Each individual owner replacement is permitted.
3. The entire set of candidate additions is $A$-independent.

For a candidate subbatch $S$, write $X_S=\{x_i:i\in S\}$,
$Y_S=\{y_i:i\in S\}$. Call the batch admissible for this rule when
$Y_S$ is isolated in $A[(U-X_S)\cup Y_S]$ and

$$
 \nu(A[U-X_S])=\nu(A[U])-|S|.                            \tag{3}
$$

**Theorem.** Enumerate every minimum cover $C$ from (1),(2). Discard the
candidates with $x_i\notin C$, then run the fixed-cover dependency closure
on the remaining list. Among the resulting batches, choose one of largest
size. This returns an admissible batch of maximum cardinality over **all**
minimum covers. Its matching cost is exactly

$$
 \nu(A[U])-\max_{S\text{ admissible for this rule}}|S|.    \tag{4}
$$

A full physical matching/cover/dissociation certificate is returned. Runtime
is $L$ times a polynomial in the input size, with no unrestricted polynomial
optimization claim.

**Proof.** Every returned fixed-cover batch satisfies the replacement
theorem, hence (3), isolation, joint owner permittedness and the claimed
matching cost. Conversely, take any admissible $S$. The exact deletion
criterion gives a minimum cover $C$ containing every point of $X_S$.
This cover occurs in the catalogue. None of $S$'s candidates is discarded
on this iteration. Isolation means $S$ is closed under the dependencies
of the filtered list and avoids its permanently blocked labels. By the
fixed-cover theorem, this iteration's largest closed batch contains $S$.
Thus one enumerated batch is at least as large as any admissible $S$.
This proves completeness and (4). ∎

When a discarded candidate was needed to remove an initial neighbour of
another addition, that neighbour becomes a permanent blocker in the filtered
list. Reverse reachability therefore handles this dependency automatically;
one must not simply restrict a closure computed before filtering.

This theorem optimizes the isolation plus exact-deletion certificate for the
**specified operations**. It does not optimize alternative additions within
an owner, conflicting additions, multiple replacements in the same owner, or
exchanges that save cost without final isolation.

## A physical case where the default cover misses a valid saving

A 20-vertex physical model has $b=4$, colours $v\bmod2$, and

$$
 P=\{(2,0),(6,4),(3,7),(1,5)\},\qquad Q=\{(2,1)\}.
$$

Its owner squares have cyclic orders $(2,1,0,7)$ and $(6,5,4,3)$.
Take $U=\{0,2,3,6,7\}$, with candidate operations $2\mapsto1$ and
$6\mapsto4$ on the respective squares. They are individually permitted
and their additions are independent. The initial auxiliary graph consists
of edges $0-2$ and $3-7$, plus isolated vertex 6. Its matching cost is two.

A valid default minimum cover $\{0,3\}$ contains neither proposed removal,
so its certificate saves zero. The minimum cover $\{2,3\}$ allows
$2\mapsto1$: the addition has only the removed initial neighbour 2, so it
is isolated after the swap. The cost becomes one. Vertex 6 is isolated
initially and belongs to no minimum cover, so removing it cannot save another
matching edge. Thus the best admissible batch in this list has size one,
and the returned physical dissociation set has size $3b-1=11$.
This is an exact fixed-list example, not a statement about the unrestricted
physical optimum. The initial $U$ need not be minimum-cardinality.

## Why a matroid greedy argument cannot replace cover selection

The family of sets $X$ contained in some minimum cover is hereditary, but
need not satisfy matroid augmentation. On the path $0-1-2-3$, its minimum
covers are exactly $\{0,2\},\{1,2\},\{1,3\}$. Both $I=\{0\}$ and
$J=\{1,3\}$ are contained in minimum covers, and $|I|<|J|$. Neither
$I\cup\{1\}$ nor $I\cup\{3\}$ is: each deletion leaves one edge and
saves only one matching edge. This precisely obstructs an automatic matroid
justification for greedy enlargement. It does not obstruct maximum sets,
which are the minimum covers themselves, or the exact enumeration above.
This auxiliary example alone is not a physical counterexample to a universal
bound.

## Verification and remaining scope

`develop/cover_choice_exchange.py` implements the catalogue and all-cover
fixed-list optimization. Its separate checker compares the catalogue with
literal vertex-cover enumeration on every induced subset of fixed balanced
bipartite graphs of maximum degree two through six vertices. It also compares
120 physical fixed-list optima against all candidate subsets and independently
enumerated matchings, reconstructs the returned physical sets, and verifies
the default-cover example and omitted-hypothesis controls. Counts and exact
scope are in `output/cover-choice-exchange-check.json`. General conclusions
use the proofs above; finite tests check implementations. Independent review returned **ACCEPT**. The reviewer ran the original
checker unchanged with assertions and reproduced its complete report
byte-for-byte. The full response, frozen hashes and actual execution scope
are preserved in [`output/cover-choice-exchange-review.json`](../output/cover-choice-exchange-review.json). No Lean execution is used.

The general physical $8b/3$ theorem, the unrestricted sharp subcubic gap,
general multi-Hall grid completion, unit-$5/6$ and arbitrary-width rectangular
grid triple equality remain open. Jointly choosing the candidate operations
and allowing conflicts among their additions are subsequent questions.
