# Long cores: a general obstruction to additive omission charging

The matching upper bound has now been proved in
[sharp long-core omission](LONG_CORE_SHARP_OMISSION.md). Thus F(k) and
beta_2(L_k) below are exact. This note gives the original lower construction
and the failure of the proposed additive rule.

## Statement and scope

The fixed six-port inequality in
[three-pair compensation](CUBIC_TRIPLE_PORT_COMPENSATION.md) is genuinely local
to its twenty-vertex core. Cutting every alternating outside edge in a longer
periodic core does not preserve that inequality additively. We prove below,
for every positive integer k, that its omission score satisfies

    F(k) := max_D (|D| + m(D)) >= 12k + floor(k/2).

Here D induces maximum degree at most one, and m(D) counts cut pairs whose
two endpoints are both omitted. The proof is an explicit cyclic word
construction, rather than an extrapolation from finite optimization.

Attaching a broken Heawood block to each cut pair gives a cubic bipartite
graph L_k with

    n = 62k, beta_2(L_k) >= 33k + floor(k/2).

It has an inclusion-minimal forming set of size 36k, but that fact does not
establish SF_2(L_k) = 36k. Combining the dissociation lower bound with the
established cubic inequality gives

    7(SF_2(L_k) - beta_2(L_k)) + 5 floor(k/2) <= 21k.

Consequently this construction cannot give gap 3k for k >= 2, which would
have yielded the hoped-for coefficient 3/62. This disproves the proposed
local additive rule and this family's exact target; it does not disprove
the cubic global inequality or exclude all improvements on 1/24.

## Graph and labeling

Let H and X be cycles of length 6k, with vertices h_i and x_i. Add u_i
and edges h_i u_i, u_i x_i. For each block t in {0,...,k-1}, add two hubs
y_(2t), y_(2t+1) and join u_(6t+j) to y_(2t+(j mod 2)), for 0 <= j < 6.
Remove the 3k edges x_(2j) x_(2j+1). The resulting graph is Q_k.
Subscripts on H and X are cyclic.

The computational global labels are H = 0,...,6k-1,
U = 6k,...,12k-1, X = 12k,...,18k-1, Y = 18k,...,20k-1.
The cut pairs have indices j = 0,...,3k-1 and endpoints
(12k+2j,12k+2j+1).

Open each six-index block by deleting the two seams to the next block:
h_(6t+5) h_(6(t+1)) and x_(6t+5) x_(6(t+1)). Local labels in an open
block are H0,...,H5, U0,...,U5, X0,...,X5, Y0,Y1, in that order.

## Two local patterns and their accounting

Use the following selected sets in an open block.

| Type | H indices | U indices | X indices | Y indices | Size | Omitted cut pairs | Score |
|---|---|---|---|---|---:|---:|---:|
| A | 0,1,4,5 | 2,3 | 0,1,4,5 | 0,1 | 12 | 1 | 13 |
| B | 1,4 | 0,1,2,3,4,5 | 2,3 | none | 10 | 2 | 12 |

In A, the selected edges are H0H1, H4H5, U2Y0, U3Y1; all four
selected X vertices are isolated. In B, the selected edges are H1U1,
H4U4, U2X2, U3X3; U0 and U5 are isolated. Thus both selections
are dissociation sets. The omitted-pair counts follow directly from the
three pairs (X0,X1), (X2,X3), (X4,X5).

All four boundary vertices H0,H5,X0,X5 are selected in A and omitted
in B. Therefore any cyclic A/B word with no adjacent A, including across
the last/first seam, selects no seam edge. Its selected induced subgraph
is the disjoint union of the local selected induced subgraphs.

For a copies of A and b copies of B, with a+b=k, this gives

    |D| = 12a+10b, m(D) = a+2b, |D|+m(D) = 12k+a.

Choose (AB)^r for k=2r, and (AB)^r B for k=2r+1. For k=1 the
word is B. These are legal cyclic words with a=floor(k/2), proving
the asserted all-k lower bound. No omitted pair or selected vertex is
shared between blocks, and every seam is explicitly checked; the extra
score cannot be removed by charging the same local loss twice.

For k=2, this gives the following explicit forty-vertex counterexample:

    D = {0,1,4,5,7,10,14,15,18,19,20,21,22,23,24,25,
         28,29,32,33,36,37}.
    omitted pair indices = {1,3,5}.
    |D|+m(D) = 22+3 = 25 > 24.

This is already a direct counterexample to |D|+m(D) <= 12k.

## Attachment and a full-graph dissociation witness

At every removed pair (x_(2j),x_(2j+1)), attach a fresh Heawood graph
with the edge (0,8) removed. Join its point 0 to x_(2j+1) and its
line 8 to x_(2j), using the labeling of
[the Heawood construction](CUBIC_STAR_FORMING_GAPS.md). Each new vertex
pair belongs to its own block. The graph L_k is simple, connected,
cubic and bipartite: Q_k is connected through its H cycle and paths
H-U-X and U-Y; each broken Heawood graph is connected and attaches
by two edges. All port degrees are restored, and the two attachments
respect opposite bipartition classes. Its order is 20k+14(3k)=62k.

For a wholly omitted core pair, take the eight-set

    E = {0,1,2,3,7,8,12,13}

in the corresponding broken Heawood graph. Otherwise take its seven-set

    P = {1,2,4,5,7,10,13}.

Both are dissociation sets, as checked directly in the existing Heawood
proof. P omits both ports; E selects the ports, but their new core
neighbors are omitted. Consequently no attachment edge has two selected
ends. This is a general compatible gluing argument, with exactly one
eight-set assigned to each wholly omitted pair.

The resulting full dissociation set has size

    |D| + 8m(D) + 7(3k-m(D))
      = 21k + |D| + m(D) = 33k + floor(k/2).

Conversely, the established one-cut Heawood cap says each attached block
contributes at most eight vertices, and an eight-set saturates both
ports. Its core pair must then be wholly omitted in a full dissociation
set. Thus beta_2(L_k) <= 21k+F(k). The matching all-k upper bound
F(k) <= 12k+floor(k/2) is now proved in the linked sharp-omission note.

## The forming witness and compulsory slack

Select every H and U vertex in the core, and the existing minimal
eight-set S_B={1,2,3,5,7,9,10,11} in every Heawood block. This has
size s=12k+8(3k)=36k and z=2(3k)=6k selected isolates.

In the core every X vertex is formed via U_i-H_i, and each Y vertex
has three selected U neighbors. Deleting either H_i or U_i makes
the corresponding X_i unformed. In each Heawood block the existing
eight-set and its deletion witnesses apply. Every removed or added edge
has both endpoints outside this fixed selection, so the local forming
test and every deletion failure remain unchanged. This proves
inclusion-minimality for every k, giving SF_2(L_k) >= 36k.

The established cubic inequality 7SF_2 <= 3n+2beta_2 yields

    7(SF_2-beta_2) <= 186k-5beta_2 <= 21k-5floor(k/2).

The slack of the fixed selection, 3n+2beta_2-7s, is at least
2floor(k/2). For even k=2r the gap is at most floor(37r/7), strictly
less than the proposed 6r for every r>=1. Asymptotically this gives
gap/n <= 37/868, which is larger than 1/24. Therefore the current
argument excludes the specific 3/62 target for L_k, while leaving
open whether L_k can improve on the established 1/24 family at all.

## Verification and next question

[LongCoreWord.lean](../formal/StarForming/LongCoreWord.lean) proves a
general graph-level theorem for any successor-indexed A/B word with
no adjacent A: every selected edge is internal, hence the global set
dissociates. Kernel reduction checks the two local patterns and counts.
The remaining declarations audit conditional counting, compulsory slack
and gap implications. All nine declarations passed local Lean; the
[receipt](../output/long-core-word-formal-check.json) states the exact
scope. Cyclic cardinal summation and full Heawood attachment are written
arguments above, rather than claimed as fully formalized.

The independent [checker](../scripts/check_long_core_words.py) verifies
literal stars and all selected-vertex deletion failures on L_k, core
and full dissociation witnesses, and the stated counts. Its
[controls](../output/long-core-word-controls.json) are finite tests of
the general proof, not its premises. Finite binary optimization for
k=1,...,10 returned F(k)=12k+floor(k/2); the
[discovery receipt](../output/long-core-omission-discovery.json) records
these observations without treating them as a proof.

The [Oracle research question](reviews/2026-10-19-long-core-omission-research-question.md)
has now yielded a structural upper proof, independently checked and written
in the linked sharp-omission note. It determines beta_2(L_k) exactly and
gives 36k<=SF_2(L_k)<=36k+floor(2floor(k/2)/7), hence exact SF=36k
for k<=7. SF for larger k and improving the1/24family remain open.
