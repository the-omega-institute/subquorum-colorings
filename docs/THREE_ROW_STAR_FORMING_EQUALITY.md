# Upper two-star-forming sets on every three-row rectangular grid

For every integer n>=1, let G_n=P_3 square P_n. With non-induced K_(1,2)
formation and deletion of the newly omitted vertex included in minimality,
we establish the computer-assisted all-length identity

    SF_2(G_n)=beta_2(G_n)=5 floor(n/3)+2(n mod 3).            (1)

Combined with Sahbi's already established width-three colouring theorem,
this gives SF_2(G_n)=beta_2(G_n)=psi_sq(G_n) for every n>=1. The colouring
and dissociation formula is prior work; the new conclusion here concerns
the upper minimal forming number. The finite premise for (1) is an exact
translation of entire frontier vectors, proved sufficient for every length
by the induction below. A list of repeated scalar optima would not supply
that premise. No arbitrary-width conclusion is asserted.

## 1. A complete local test for minimality

For any finite simple graph, a set S forms an outside vertex x precisely
when a non-induced three-vertex star on {x,a,b} exists with a,b in S.
Equivalently, x has two selected neighbours, or a selected neighbour that
itself has a selected neighbour. Formation is upward closed. Therefore
S is inclusion-minimal forming exactly when it forms every outside vertex
and for each v in S there is an unformed vertex after deleting v.

A deletion witness x for v is either x=v or originally outside S. In the
second case a former forming star at x must use v, so dist(x,v)<=2.
Whether x is formed after deleting v depends only on selection in the
closed distance-two neighbourhood of x. The same assertion covers x=v.

Consequently the following tests are necessary and sufficient:

* every outside x is formed;
* mark v whenever a test at an outside x finds that S-{v} fails to form x;
* also mark a selected x if S-{x} fails to form x;
* require every selected vertex to be marked by the end.

A witness may mark more than one selected vertex. This records separate
single-deletion failures; it does not allocate a physical matching resource.
No distinct-witness assumption is imposed or needed.

## 2. An exact four-column frontier

Number columns from zero. A radius-two neighbourhood of a vertex in column c
lies in columns c-2 through c+2. After introducing column k, every formation
and deletion-witness test centred in column k-2 can be completed exactly.

Before introducing a column, retain four columns. Give each retained vertex
one of three digits:

    0: omitted;
    1: selected, with no witness yet processed;
    2: selected, with a witness already processed.

There are 3^(4h) possible states for height h. The computation below uses
h=3, hence 531,441 possible states. Digits within a column run from its top
to its bottom; the oldest column occupies the lowest ternary positions.
The score is the total number selected in the prefix, including forgotten
vertices. Begin with four absent columns, all digits zero, and score zero.
Absent columns contain no vertices and never serve as witness centres.

To introduce a real column, choose any of its 2^h selected masks. The new
selected vertices initially have no processed witness. The four retained
columns and the new column form a five-column window. If its middle column
is real, perform all tests of Section 1 centred in that column:

1. Reject if an omitted middle vertex is not formed.
2. For each omitted middle vertex x, mark every selected v in the window
   for which deleting v leaves x unformed.
3. For each selected middle vertex x, mark x if deleting x leaves x unformed.

All tests are exact in this window. Every selected neighbour of a middle
vertex, and every selected neighbour needed for that neighbour's activity,
lies inside it. No selected vertex outside the window can belong to a
forming star at a middle vertex. At the top, bottom and left boundaries,
the absent positions introduce no additional selected vertex or graph edge
between real vertices. If the middle column is absent, skip these tests.

Before forgetting the oldest column, reject if any selected vertex in it
is unmarked. Its column is k-4; all possible witness centres for it lie
at columns at most k-2 and have now been processed. Conversely, a centre
not yet processed is too far away to witness its deletion. Thus the
forgetting test loses no possible future witness. Remove the oldest
column and retain the other four. Add the number selected in the new
real column to the score, and maximize scores at identical states.

For a board of length n, introduce four absent columns at the right end,
with selected mask zero and no added score. Process a middle column exactly
when its index is between zero and n-1. Require the final state to be zero.
Every real vertex is then tested and forgotten.

**Frontier lemma.** An input sequence of n selected column masks is accepted
if and only if its selected set is inclusion-minimal forming in G_n. Its
score is exactly that set's cardinality. Maximizing scores computes SF_2(G_n).

**Proof.** Every real witness centre is processed exactly once, two
introductions after its own column. Its formation and deletion tests use
its entire relevant neighbourhood, as proved above. Thus every mark is an
actual global deletion failure and every outside formation condition is
tested. When a selected vertex is forgotten, all and only its possible
witness centres have been processed. Acceptance therefore requires, and is
implied by, a witness for every selection and formation of every outside
vertex. These are exactly Section 1's conditions. Scores count each selection
on introduction once. Finally, future tests and forgetting depend only on
the last four selected columns and their accumulated witness flags. Prefixes
with the same state have the same possible continuations and future score
increments, so retaining the greatest score is exact. QED.

## 3. Whole-vector translation and the infinite conclusion

Let V_n be the maximum-score vector immediately after n real columns,
before right-end closure. An unreachable state has value minus infinity.
The first two introductions skip the middle-column tests because their
centres are absent. From the third introduction onward, one fixed transfer
Phi applies. It chooses the new mask, performs the tests above, and maximizes
at each target state. Hence

    V_(n+1)=Phi(V_n) for n>=2,
    Phi(V+c)=Phi(V)+c.                                    (2)

Here addition preserves minus infinity. For n>=2, closure is the same fixed
operation: introduce four zero masks, process the middle in the first two
steps, and skip it in the last two. It adds no score. Denote its scalar
maximum by Z. It also satisfies Z(V+c)=Z(V)+c. For n=1, the four closure
steps instead have middle flags absent, real, absent, absent; this case is
checked separately. The empty grid has value zero.

The two implementations reconstruct V_12 and V_15 from the empty prefix
and verify, including identical unreachable support,

    V_15=V_12+5.                                         (3)

There are exactly 14,726 reachable states at each endpoint, serialized
in increasing ternary code in the two accompanying TSV certificates.
Equation (3), not just equality of the terminal maxima, is the finite
certificate. It is independently regenerated by literal three-vertex stars.

Induct on j>=0 using (2):

    V_(15+j)=Phi^j(V_15)
            =Phi^j(V_12+5)=V_(12+j)+5.

Applying the fixed closure proves

    SF_2(G_(n+3))=SF_2(G_n)+5 for every n>=12.              (4)

The exact initial values for lengths 1 through 14 are

    2,4,5,7,9,10,12,14,15,17,19,20,22,24.

They equal 5 floor(n/3)+2(n mod3), which itself increases by five under
n -> n+3. The initial values and (4) prove (1)'s upper-SF formula for
all positive lengths. The argument after the finite certificate is an
ordinary induction on arbitrary length, not extrapolation from a finite
list. Its finite premise is computer checked, not Lean kernel verified.

## 4. Attainment, dissociation, and the colouring corollary

In columns with residue 0 or 1 modulo 3, select the top and bottom vertices.
In columns with residue 2, select the middle vertex. This selects five
vertices in every full three-column block and two for each residual column.
The selected subgraph has maximum degree one. An omitted middle vertex
has its top and bottom neighbours selected. An omitted top or bottom vertex
is in a residue-two column and sees the active selected vertex immediately
to its left; that vertex is paired with its selected left neighbour.
So the selection forms every outside vertex. Deleting a selection fails
at that newly omitted vertex: an isolated selection has no selected
neighbour, while the sole mate of a selected edge becomes inactive.
Thus this is a minimal forming and dissociation set of the size in (1).

For completeness, beta_2(G)<=SF_2(G) for every finite simple graph: a maximum
dissociation set is minimal forming. If an outside vertex were unformed,
it would have no selected neighbour, or just one selected neighbour that
is isolated, and could be added without creating selected degree two.
This contradicts maximality. Deleting any selected vertex fails at itself
by the same isolated-vertex or isolated-edge argument above. Consequently
the SF upper bound and the printed dissociation construction also give
beta_2(G_n) equal to (1), without assuming the grid formula as an input.

Sahbi's *Sub-quorum colorings of graphs*, arXiv:2609.25128v1, Theorem 5.5,
already establishes psi_sq(G_n)=F(3,n) for every n>=1. Its width-three case
is also independently reproduced by the archived Omega transfer and its
full-vector certificate: start 3, period 3, doubled increment 10, 65 states.
Here F(3,n)=5 floor(n/3)+2(n mod3). Thus the prior colouring theorem and
(1) yield the triple equality on every three-row grid. This does not
claim a new width-three colouring result or a solution at arbitrary width.

## 5. Reproduction and scope

Run from the repository root, choosing a disposable binary path:

```sh
c++ -std=c++17 -O3 -Wall -Wextra scripts/grid_star_transfer.cpp -o /tmp/sahbi-grid-star
/tmp/sahbi-grid-star 3 15 output
python3 -B scripts/check_grid_star_transfer.py
```

The C++ generator uses the selected-neighbour/activity test. The independent
standard-library Python checker imports no project algorithm and instead
builds literal three-vertex stars by their edge patterns. It reconstructs
both complete vectors from the empty prefix and compares every saved entry.
The checker also compares its acceptance with literal global minimality
for every selected subset on the stated small boards: 21 boards, 44,954
subsets, heights one through three. In particular, the one-column closure
has an explicit exhaustive regression. The literal-star kernels are fully
constructed on all 33,824 five-column masks at heights one, two and three.
This is distinct from the 44,954 explicit transfer-acceptance comparisons;
the checker does not compare every C++ kernel or transition-table entry
against Python. These finite tests check the implementations; Sections
1--3 prove the general frontier specification and its all-length implication.

The initial exploratory closure used the n>=2 tail at n=1 and incorrectly
reported three for P_3; the literal reference found two. Both final programs
use the correct one-column tail, and the original discovery output is
retained locally as provenance, not a theorem or final validation report.
The endpoint certificate at lengths 12 and 15 was unaffected.

The independent audit returned **ACCEPT** for the mathematical proof and
finite premise. The reviewer ran the unchanged C++ generator and the
unchanged Python checker with assertions enabled, rebuilt both complete
vectors from the empty prefix, and reproduced both TSVs and both new JSON
reports byte-for-byte. An additional independent canonical serialization
of the Python vectors matched the TSV bytes. The reviewer also reran the
old Omega generator and checker and reproduced its four width-three
outputs exactly. They reproduced the wrong one-column tail and confirmed
the corrected boundary handling. No mathematical revision was requested.

The full response, pinned input hashes and actual execution scope are in
[the review record](../output/grid-star-transfer-review.json). The reviewer
could not retrieve the original arXiv v1 text to confirm the exact theorem
number; their independent check of the supplied prior Omega proof and
certificates supports the colouring corollary without that retrieval.
The wording above distinguishes literal-kernel construction from explicit
acceptance comparisons, as suggested in review. Code and certificates are
unchanged after review. There is no exhaustive subset search on large G_n,
no general SF<=Omega premise, no new Lean execution, and no arbitrary-width
claim.
