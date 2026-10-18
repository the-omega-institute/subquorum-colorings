# Sharp omission compensation on every long core

## Theorem

Use the graphs Q_k and L_k, labeling, omission count m(D), and local
patterns A and B defined in
[the long-core obstruction](LONG_CORE_WORD_OBSTRUCTION.md). For every k>=1,

    F(k) := max_{D dissociating in Q_k} (|D|+m(D))
          = 12k+floor(k/2).
    beta_2(L_k) = 33k+floor(k/2).
    36k <= SF_2(L_k) <= 36k+floor(2floor(k/2)/7).

In particular SF_2(L_k)=36k for 1<=k<=7. The theorem does not determine
SF_2(L_k) for all k or the optimal connected cubic gap coefficient.

The all-k lower bound and compatible Heawood witnesses were already
proved in the preceding note. This note proves the matching upper bound
through a local inequality and the actual interblock seams. It resolves
the corrected upper-bound question without using finite enumeration as
a premise.

## Normalize the outside pairs

Given any dissociation set D, remove its selected endpoint from every
original cut pair that contains exactly one selected endpoint. Taking a
subset preserves dissociation. Each such operation decreases |D| by one
and increases m(D) by one. It therefore preserves |D|+m(D), globally and
within each six-index block.

After normalization, each original cut pair is wholly selected or wholly
omitted. Write z_j=1 in the first case and z_j=0 in the second. Each pair
contributes 2z_j+(1-z_j)=1+z_j to |D intersect X|+m(D). Thus the score
of a block is three plus its number of selected H,U,Y vertices plus
the sum of its three z variables. Opening the interblock H and X seams
introduces no extra omission terms: m counts only the original cut pairs.

## A two-index cell inequality

In an open block, let a_i and v_i indicate selection of h_i and u_i.
Let q be its number of selected Y hubs. Define, for j=0,1,2,

    C_j = a_(2j)+a_(2j+1)+v_(2j)+v_(2j+1)+z_j.
    sigma = 3+C_0+C_1+C_2+q.

Every cell has C_j<=3. If z_j=0, its four H/U vertices contain
the path u_(2j)-h_(2j)-h_(2j+1)-u_(2j+1); all four cannot be selected.
When three are selected, both U vertices and exactly one H vertex must
be selected: selecting both H vertices excludes both adjacent U vertices.
If z_j=1, both X vertices are selected, so a_i+v_i<=1 at each
coordinate, since otherwise u_i has two selected neighbors h_i,x_i.
This again gives C_j<=3, with equality forcing a_i+v_i=1 at both
coordinates. Call a cell tight when C_j=3.

## Sharp open-block inequality

We prove that sigma<=12, except for exactly pattern A, whose score is13.

If q=0, the three cell inequalities immediately give sigma<=12.

If q=1, assume its even hub is selected. The reflection i->5-i
preserves the open graph, exchanges the hubs and permutes the cut pairs,
so this covers the other case too. In a tight cell with z_j=0, both
U vertices are selected. Its even H vertex is then omitted because its
U partner already meets the selected hub; the odd H vertex is selected.
In a tight cell with z_j=1, its even U vertex is omitted because its
hub and X partner are selected, so its even H vertex is selected, and
exactly one of its odd H/U vertices is selected.

Two consecutive tight cells cannot have the latter cell's z equal to1.
If the preceding z is0, its odd H vertex is already matched to its
selected U partner, and the latter cell's even H vertex supplies a
second selected neighbor across the H edge. If the preceding z is1,
the internal X edge between the two cells is selected at both ends,
forcing the preceding odd U vertex to be omitted. Tightness selects its
odd H vertex, which then meets both its own even H vertex and the next
even H vertex. Both cases contradict dissociation.

Were all three cells tight, the preceding observation would force
z_1=z_2=0. The middle and last even U vertices would both be selected,
giving their selected even hub two selected neighbors. Thus at least
one cell is not tight, sum C_j<=8, and sigma<=3+8+1=12.

If q=2, no tight cell can have z_j=0: its selected H vertex would
give the selected U partner a second selected neighbor in addition to
its hub. Hence a tight cell has z_j=1, both U vertices omitted and
both H vertices selected. Two consecutive tight cells are impossible,
since they would select four consecutive H vertices. At most two cells
are tight, so sum C_j<=8 and sigma<=13.

If sigma=13, the cell weights must be3,2,3. The outer tight cells
force z_0=z_2=1, select H0,H1,H4,H5, and omit U0,U1,U4,U5.
The selected edges H0H1 and H4H5 force H2,H3 omitted. If z_1=1,
the selected hubs would also force U2,U3 omitted, giving middle weight1
instead of2. Therefore z_1=0 and U2,U3 are selected. This is exactly
pattern A. Its selected edges and score13 were checked directly in the
preceding note. We have proved

    sigma_b <= 12+alpha_b,

where alpha_b indicates that the normalized block is A.

## Boundary control and cyclic summation

In A, both boundary H vertices are selected and already internally
matched: H0H1 and H4H5. Two adjacent A blocks would give their seam
endpoints a second selected neighbor. Hence, cyclically,

    alpha_b+alpha_(b+1) <= 1.

This includes k=1: the seam H5H0 closes the same block, and A is
impossible. For k=2 the two actual H seams also prohibit two A blocks.
Summing counts each alpha exactly twice, giving

    sum alpha_b <= floor(k/2).
    |D|+m(D) = sum sigma_b <= 12k+floor(k/2).

The first equality is valid because the original cut pairs and vertices
belong to distinct blocks. There is no reused surplus: the sole positive
block deviation is an actual indicator, and the cyclic exclusion counts
each such indicator twice. Normalization preserved the original score,
so the bound holds before normalization as well. The alternating A/B
words attain it, completing the proof of the exact F(k).

## Consequences for the full family

For any dissociation set in L_k, each attached broken Heawood graph
contributes at most8. Each eight-set saturates both ports, forcing the
corresponding core pair wholly omitted. Distinct blocks have distinct
core pairs, so their surplus above7 is charged injectively to m(D).
Therefore

    beta_2(L_k) <= 21k+F(k) = 33k+floor(k/2).

The compatible seven/eight-set construction in the preceding note
attains this value. Its inclusion-minimal forming witness gives
SF_2(L_k)>=36k. Applying 7SF_2<=3n+2beta_2 now yields

    7SF_2(L_k) <= 252k+2floor(k/2),

which proves the claimed SF interval. Its upper and lower ends coincide
for k<=7. For k>=8 the interval alone does not settle SF. The previously
derived gap bound and exclusion of the proposed3/62target remain valid.

## Proof and verification scope

The proof uses necessary induced-degree constraints and direct equality
analysis; no solver value or enumerated state table is a hypothesis.
The Oracle supplied this structural upper argument; its
[original response](reviews/2026-10-19-long-core-omission-research-response.txt)
is archived with [metadata](../output/long-core-omission-oracle-question.json).
We checked the normalization, hub cases, reflection, equality and k1/k2
seams independently before incorporating the result.

[LongCoreUpper.lean](../formal/StarForming/LongCoreUpper.lean) checks ten
conditional cell/count declarations, including tight-cell structure,
the one-hub obstruction and two-hub sharp count. Its explicit Valid and
Across hypotheses are necessary star inequalities extracted in the
written proof. Graph-to-count extraction, reflection, full identification
of A, cyclic summation and attachment retain written proofs.
[Formal receipt](../output/long-core-upper-formal-check.json).

[Independent local controls](../scripts/check_long_core_upper.py) exhaust
the normalized open block and verify the reflection, unique exceptional
pattern and saturated boundary. These finite checks test the general
proof; they do not replace it.
[Control receipt](../output/long-core-upper-controls.json).

Next determine SF_2(L_k) for larger k, and whether its gap can improve
on the established1/24family. The grid triple equality is a separate
open question; this theorem makes no claim to improve its5/6bound.
