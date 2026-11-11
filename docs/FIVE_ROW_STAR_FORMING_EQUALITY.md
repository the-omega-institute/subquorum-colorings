# Upper two-star-forming sets on every five-row grid

For every positive integer n, put G_n=P_5 square P_n. Then

    SF_2(G_n)=beta_2(G_n)=psi_sq(G_n)=F(5,n),               (1)

where

    F(5,n)=max(3 ceil(2n/3)+2 floor(n/3),
               4 ceil(n/2)+floor(n/2)).                  (2)

Equivalently, the value is 4, 6, 9 at n=1,2,3, respectively, and

    8 floor(n/3)+3(n mod3) for n>=4.                      (3)

The new result is the upper minimal forming number SF_2. The dissociation
and colouring formulas are prior work. The proof here is computer assisted:
a general exact frontier and an equality of complete score vectors give
an induction valid at every length. The finite premise is checked by two
implementations, including all 33,554,432 local patterns; no large-board
subset extrapolation is used. Widths at least six remain outside this result.

## 1. Formation, global deletion witnesses, and the exact frontier

A set S forms x outside S when some distinct a,b in S make {x,a,b} contain
a non-induced K_(1,2). S is forming when it forms every outside vertex.
SF_2 is the maximum size of an inclusion-minimal forming set; beta_2 is
the maximum size of a set inducing maximum degree at most one. The
sub-quorum parameter psi_sq is the greatest number of colours used by an
onto partial colouring in which every coloured vertex has at least half
of its coloured closed neighbourhood in its own colour. Uncoloured
vertices are excluded from this neighbourhood count.

Formation is upward closed: enlarging S preserves every former forming
pair at any vertex still outside. Therefore inclusion-minimality is
equivalent to failure of every single deletion. After deleting v, the
new outside set consists of the formerly omitted vertices and v itself.
An originally omitted x can witness that deletion only if every formerly
available forming pair at x used v. Hence dist(x,v)<=2. Formation and
deletion failure centred at x both depend only on selected labels in its
closed radius-two neighbourhood. A selected centre tests only its own
deletion, since it remains selected under every other single deletion.

Retain the preceding four columns. Each vertex has one of three states:
omitted, selected without a processed witness, or selected with a processed
witness. After introducing column k, process every formation and deletion
test at the middle column k-2 of the five-column window k-4,...,k. Its
radius-two neighbourhood is now complete. Reject an unformed omitted
centre, and mark every selected deletion it witnesses. A selected centre
is marked if it fails to form after its own deletion. The same omitted
centre may mark several selections: these are separate single-deletion
tests, and do not require distinct matching resources.

Forget column k-4 only when all its selections are marked. Every possible
witness centre for them is at column at most k-2 and has now been processed;
every mark is permanent because later columns are outside the tested
neighbourhood. Four appended zero-mask columns close the board. An absent
column is never a witness centre. Closure centres are real, real, absent,
absent for n>=2, and absent, real, absent, absent for n=1. The first two
real introductions also skip their absent centres.

These rules accept exactly the globally minimal forming selections.
Necessity follows by processing all their actual witnesses; sufficiency
follows because every omitted vertex was formed and every selection was
forgotten with an actual deletion witness. Retaining only the greatest
prefix score at each state is exact: future tests, possible continuations,
and score increments depend only on the retained selected labels and witness
flags. Earlier selections cannot enter a future tested neighbourhood.
This is also the general Frontier Lemma proved in Sections 1--2 of the
[three-row note](THREE_ROW_STAR_FORMING_EQUALITY.md), with h=5 here.

There are 3^20=3,486,784,401 possible four-column ternary states. The
implementations store reachable states only, without truncation. Writing
s and f for their twenty-bit selected and witnessed masks, the serialization

    key=s+2^20 f,     f subset s                         (4)

is a bijection with the legal ternary states. The generator additionally
packs its nonnegative score plus one above the forty key bits. A zero word
then means an unused hash slot, including when the actual state key is zero.
The reference implementation uses ordinary unordered maps instead.

## 2. The exact finite premise and its infinite consequence

Let V_n be the complete maximum-score vector after introducing n real
columns, before closure; absent states have value minus infinity. Starting
with the third introduction, one fixed transfer Phi is used. For n>=2,

    V_(n+1)=Phi(V_n),     Phi(V+c)=Phi(V)+c.

The fixed right closure Z for n>=2 also obeys Z(V+c)=Z(V)+c.
The two implementations reconstruct all prefixes from the empty state and
verify the whole-vector identity

    V_17=V_14+8.                                        (5)

Each endpoint has exactly 8,227,512 reachable states. Their supports
coincide and every finite coordinate increases by eight. All remaining
ternary states are unreachable on both sides. This support assertion follows
from exhaustive reachable-state transitions from the empty prefix; it does
not assume that equal state counts imply equal supports.

For every j>=0, transfer homogeneity and (5) give

    V_(17+j)=Phi^j(V_17)=Phi^j(V_14+8)=V_(14+j)+8.

Applying the fixed closure proves

    SF_2(G_(n+3))=SF_2(G_n)+8 for every n>=14.             (6)

The exact initial values through length sixteen are

    4,6,9,11,14,16,19,22,24,27,30,32,35,38,40,43.

They supply all shorter lengths and the three recurrence seeds 14,15,16.
Expression (3) has increment eight under n->n+3, so (6) and ordinary
induction prove the asserted SF formula for every positive length.

To verify agreement with (2), write n=3q+r. Its first term is 8q+3r.
Its second term is at most 5n/2+3/2, while the first is at least 8n/3;
hence the first dominates for n>=9. Direct substitution covers 4<=n<=8.
The first three values of the maximum are 4,6,9, giving exactly (3).

## 3. Attainment and the prior colouring corollary

For n>=4, in columns of residue 0 or 1 modulo three, select rows 0,2,4;
in columns of residue two, select rows 1,3. The selected components are
isolated vertices or horizontal edges. It has 8q+3r selections. Each omitted
vertex in a residue-zero or residue-one column has two selected vertical
neighbours. Each omitted vertex in a residue-two column sees an active
selected neighbour to its left, paired with the selection one further
column left. Thus all omitted vertices form. Every selection witnesses
its own deletion because its component has order one or two.

At n=1 select rows 0,1,3,4, giving two edges and size four. At n=2 select
rows 0,2,4 in both columns, giving three horizontal edges and size six.
At n=3 transpose the three-row length-five construction: select columns
0,2 in rows 0,1,3,4, and column 1 in row 2. This has size nine and is
minimal forming by the same isolated-edge/isolated-vertex and formation
tests (or by the graph isomorphism with P_3 square P_5).

For every finite simple graph, beta_2<=SF_2. Indeed a maximal dissociation
set D must form: otherwise an unformed outside vertex has no neighbour in D,
or just one neighbour which is isolated in D, so it could be added while
preserving maximum selected degree one. Every vertex of D also witnesses
its own deletion. Thus a maximum dissociation set is minimal forming.
Our exhibited dissociation sets and the established SF upper bound now
give beta_2(G_n)=SF_2(G_n)=F(5,n).

For colouring, use the established width-five result in Sahbi's
*Sub-quorum colorings of graphs*, arXiv:2609.25128v1, Theorem 5.5.
The existing independent Omega supplier provides another complete route:
beta_2<=psi_sq<=Omega, and its width-five complete-vector certificate has
start 9, period 3, doubled increment 16 and 856 states. Together with its
finite initial values and homogeneous-transfer proof in
[the existing strip note](../develop/grid-strips-2026-09-27.md), it gives
Omega(G_n)=F(5,n). The explicit dissociation lower bound therefore forces
psi_sq(G_n)=F(5,n), proving (1). Both the old generator and independent
checker were rerun locally; their four supplied outputs were byte-identical.
This corollary does not use a general SF_2<=Omega premise.

## 4. Independent finite verification and reproduction

The generator computes its local tests using selected-neighbour counts on
the triangle-free grid. For an omitted centre with one selected neighbour u,
u must be active; deleting u fails, and deleting u's sole selected partner
also fails when that partner is unique. With two selected neighbours,
deletion fails exactly when the other is isolated, since they cannot be
adjacent in a triangle-free graph. With at least three, no single deletion
destroys formation. For a selected centre, self-deletion fails exactly when
it has no selected neighbour, or only one whose sole selected partner is
the centre. These cases exhaust the local possibilities.

The reference constructs literal unordered pairs a,b whose three vertices
with the centre have at least two edges. For an omitted centre, the
intersection of all available selected pairs is exactly the set of deletions
that destroy formation. If no pair exists, the centre is unformed. A selected
centre marks itself exactly when no such pair exists; those pairs exclude
the centre, so its deletion is already represented. This reference uses
neither the neighbour-count predicate nor the packed table implementation.

It compares every one of the 2^25 local kernel entries, including invalid
windows, then uses its own kernel and standard unordered maps to reconstruct
all seventeen prefixes. At both endpoints it reads the canonical vector
rows and compares every entry and total support with its reconstructed map.
It separately compares the two endpoint files to verify (5).

It also compares transfer acceptance with literal global minimality for
every selected subset on 5-by-1 through 5-by-4: 1,082,400 subsets in total,
including the distinct one-column closure. These controls check all
individual selections, not only maximum sizes. The compact generator also
reproduces both previously accepted three-row vectors under the encoding
bijection and both four-row vectors byte-for-byte.

From the repository root, choose disposable binary paths and a fresh output
directory (the generator rejects an existing directory):

```sh
c++ -std=c++17 -O3 -Wall -Wextra scripts/grid_star_compact_transfer.cpp -o /tmp/sahbi-grid-five
c++ -std=c++17 -O3 -Wall -Wextra scripts/check_grid_star_compact.cpp -o /tmp/sahbi-check-grid-five
/tmp/sahbi-grid-five 5 45 /tmp/sahbi-five-vectors /tmp/sahbi-five-kernel.bin
/tmp/sahbi-check-grid-five 5 14 3 8 /tmp/sahbi-five-vectors /tmp/sahbi-five-kernel.bin
```

Both programs enforce a twelve-million-state cap and fail rather than drop
states. Only successful exit statuses and a newly produced PASS report
constitute a certificate. Partial files from failed runs are insufficient.
The large vectors and native-endian temporary kernel are regenerable;
their exact hashes are recorded with the concise reports. The mathematical
state serialization is the portable decimal TSV format (4). No global
state-count bound at larger heights is inferred from the observed count.
No new Lean result or arbitrary-width theorem is asserted. Independent
review and its actual execution scope will be recorded separately.
