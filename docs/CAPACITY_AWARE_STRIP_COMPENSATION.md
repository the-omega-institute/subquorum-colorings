# Capacity-aware strip compensation beyond exclusive allocation

19 October 2026. Retain the exact prescribed-source, matching/support,
normalization and outside-coverage hypotheses of
`DIRECTIONAL_AVERAGING_SOURCE_COMPENSATION.md`. The per-strip input is
D_i>=q_i=max(0,2b_i+f_i), proved in the exclusive-strip note. This note
permits selected strips to overlap, while deducting each possible shared
physical deficit. It gives a further explicit negative-flux family that
the exclusive structural certificate does not cover.

## 1. The general capacity-aware inequality

Let H be the bipartite graph of coalesced horizontal and vertical strips.
For each edge ij choose a verified upper bound c_ij on the original no-P
deficit in G_i intersection G_j. The intersection is one physical tile,
so c_ij=2 always suffices. If it contains a retained endpoint, take c_ij=0.
If it is endpoint-free and contains t required selected supports, take
c_ij=2-t. These are uniform bounds over feasible completions retaining
the prescribed data. An observed optional selection alone cannot justify
the same capacity bound for a larger completion class.

For arbitrary sets A of horizontal strips and Z of vertical strips, put

    C(A,Z)=sum_(i in A)q_i+sum_(j in Z)q_j
           -sum_(ij in E, i in A, j in Z)c_ij.        (1)

**Capacity-aware compensation lemma.** With the original whole-receiver
ledger Delta=-B+D_G+R, R>=0,

    D_G>=C(A,Z),  Delta>=C(A,Z)-B+R.                 (2)

In particular C(A,Z)>=B implies |T_0|+|M_0|<=mn/2.

Proof. In the selected strips, each original physical donor tile appears
zero, once or twice. It appears twice precisely at one edge between A and
Z. Inclusion-exclusion is therefore exact for their actual deficits:

    D_(selected union)=sum_(selected i)D_i
       -sum_(ij selected)D_(G_i intersection G_j).

Use D_i>=q_i and each shared deficit<=c_ij. The selected union is contained
in G, so D_G is at least this value. Substitute once in the original ledger.
An overlapping tile is deducted once, rather than used twice. Endpoint
charges, matching exports and shifted squares are not additional donors. QED.

The exclusive certificate is the special case with no selected graph edge.
Selecting all strips recovers a coarse crossing-capacity subtraction. Neither
choice need optimize (1).

## 2. Exact cut certificate and scalar relaxation

Use capacities q_i on s->horizontal i, q_j on vertical j->t, and c_ij on
horizontal-to-vertical edges. If Q=sum_i q_i, then

    C_star=max_(A,Z) C(A,Z)=Q-mincut.                 (3)

Indeed a cut with horizontal source-side set A and vertical sink-side set
Z has cost Q-sum_A q-sum_Z q+sum_(A,Z)c. Taking its complement gives (3).
Unlike the exclusive network, its minimum cut may cut horizontal-to-vertical
arcs. This is again classical capacitated max-flow/min-cut.

The scalar resource relaxation now requires 0<=x_ij<=c_ij for shared edge
resources, y_i>=0 for private resources, and y_i+sum_(e at i)x_e>=q_i.
Its minimum total cost is exactly C_star. Formula (1) lower-bounds any
feasible resource cost. Conversely a maximum flow f of value v defines
x_ij=f_ij and y_i=q_i-sum_(e at i)f_e>=0, receiving exactly q_i at every
vertex. Its cost is Q-v=C_star. This proves optimality in the relaxation,
not realizability of that relaxation by grid selections. Private resources
are still unrestricted, so failure C_star<B leaves further geometric work.

## 3. A general all-even-width construction

For every even W>=64 use eight prescribed sources, with their full support
template displayed in the corrected exclusive-strip note. Four sources H_i,
i=0,...,3, open downward and have

    chamber origin (2+4i,3+4i), width W-8i,
    tip row 40 for i=0,1,2 and 44 for i=3.

Their depths are respectively 18,16,14,14. Three rightward sources V_j,
j=0,1,2, are the transposed standard origin-(2,3) sources with widths
38-8j, depths 8-2j and translations (18+4j,20+4j). Their chamber origins
are (21+4j,22+4j), bottom chamber rows 58-4j and tip columns 40. The last
rightward source Z is the transpose of width 10, depth 4, translated by
(30,32); its chamber occupies rows 33,...,42, columns 34,35 and its tips
are in column 44.

Add four complete consecutive-matching combs:

| Comb | Endpoint path | Side supports | Axial supports |
| --- | --- | --- | --- |
| C_0 | column 18, rows 37,...,40 | column 19 at odd rows, 17 at even rows | (36,18),(41,18) |
| C_1 | column 50, rows 37,...,44 | column 51 at odd rows, 49 at even rows | (36,50),(45,50) |
| C_2 | row 48, columns 41,...,48 | row 47 at odd columns, 49 at even columns | (48,40),(48,49) |
| C_3 | row 38, columns 45,46 | (37,45),(39,46) | (38,44),(38,47) |

Select only the prescribed source and comb supports. The containing rectangle
is 70-by-(W+10). This is the explicit `capacity_path(W)` generator.

## 4. General feasibility, completeness and freezing

The following interface argument holds uniformly for all even W>=64; it is
independent of the finite controls.

Within the H_i family, endpoint distance is at least three, with distance
three occurring only between consecutive chamber rows. The later source
has no support in the row immediately before its chamber origin. This
excludes the only possible adjacency of two one-step supports across that
three-step gap, as proved with the full support formula in the corrected
exclusive-strip note. All arm/chamber and arm/arm separations are at least
four, which directly give support separation at least two. The V_j,Z
family has exactly the transposed interface argument: consecutive chamber
column pairs are separated by three, and the later source has no support
in the preceding column. Its other endpoint separations are at least four.

Between the horizontal and vertical source families, all H chambers end
by row 15 and all V chambers start at row 21 or later. The innermost H
arms are at columns 15 and W-10>=54, while vertical-source endpoints have
columns 22,...,44. Endpoint separation is at least six. Thus all their
prescribed supports remain mutually compatible and see no foreign endpoint.

For C_0 the only three-step endpoint interface is the H_3 left arm, at
column 15. On odd rows its inside support is at 16 and C_0's support at
19; on even rows its outer support is at 14 and C_0's support at 17.
Nearest supports across rows are diagonal, at distance at least two.
Its axial supports at column 18 also have no adjacent source support.
All other source endpoints are at least four away from C_0's path.

C_1 is at least four from every source endpoint: the nearest H right arm
is at 54, and the furthest vertical-source endpoint is at 44. Its supports
therefore remain separated from source supports. C_0 and C_1 are far apart.

For C_2, the closest source endpoint is on V_2's bottom arm, row 50 with
columns through 40. Its inside supports in row 49 have columns 33,35,37,39;
C_2's row-49 supports have columns 42,44,46,48, so they are separated.
The two closest cross-interface pairs are (48,40) versus (49,39), and
(49,42) versus the source's axial support (50,41); both are diagonal.
Every other source-support interface has greater separation. C_2 is also
at least four from the other new occupied paths or their supports near it.

C_3 is separated by at least four endpoint steps from all sources and C_1:
the latter is at column 50, while C_3 ends at 46. Its supports in columns
44,...,47 do not meet C_1's supports in columns 49,...,51. It is far from
C_0 and C_2. Every selected support therefore retains exactly its own
endpoint neighbor. The prescribed single-component feasibility proofs cover
the internal cases. No endpoint components join.

Increasing even W only moves the right H arms farther from every other
component and extends chamber rows at or above row 15; all non-H components
start below that region and have occupied columns at most 51. The same
interface proof therefore applies for every stated width. All coordinates
fit in the rectangle. Retained-support freezing applies to each complete
component, so the sources have charge +1 and the four combs charge zero.

## 5. Exact strip graph, negative flux and strict certificate improvement

The four merged strips are

| Strip | Physical region | Member sources | Comb flux | Weight |
| --- | --- | --- | --- | --- |
| H | rows 40,41; columns 4,...,W+1 | H_0,H_1,H_2 | -1 | 5 |
| h | rows 44,45; columns 16,...,W-11 | H_3 | -1 | 1 |
| V | rows 22,...,57; columns 40,41 | V_0,V_1,V_2 | -1 | 5 |
| v | rows 34,...,41; columns 44,45 | Z | -1 | 1 |

Their graph has edges HV,Hv,hV, a four-vertex path. Each comb's sparse end
lies in its assigned strip alone. Its saturated end lies outside all four
strips; the relevant singleton row/column pairs follow directly from the
listed odd-start/even-end paths. Interior comb tiles can meet other strips
but contribute zero flux. Thus B=8,F=-4,O=4,J=0, with no duplicated ends.

All three crossing tiles are endpoint-free. HV contains exactly one
required selection, (41,41), the inside support of Z's lower arm. Hv and
hV contain no required selection. In the explicit baseline the crossing
loss is K_loss=1+2+2=5, so the earlier criterion fails:

    K_loss+O=9>B+J=8.

The best exclusive strip set has weight W_exclusive=6: both same-direction
sets have weight six, and each high-weight vertex meets both opposite
vertices. The only independent opposite-direction pair has weight two.
So the previous exclusive criterion also fails, 6<8.

Select H and V together. Their structural sum is ten. Their intersection
is one physical no-P tile, so the universal capacity-two bound gives

    C({H},{V})>=5+5-2=8=B.

The retained support at (41,41) improves its uniform shared capacity to one,
giving the strict bound

    C({H},{V})>=9,       Delta>=1+R.                  (4)

The cut optimum is exactly eight with capacities (2,2,2), and nine with
capacities (1,2,2). The chosen high pair attains these values. Feasible
network flows of values four and three, respectively, give matching upper
certificates since Q=12. Hence the numbers are exact scalar optima, not
only successful choices.

Uniform completion claims here keep the eight sources and four combs as
complete components, retain their matching and supports, and permit no
additional endpoint component to meet these four mouths. Arbitrary additional
feasible selections and allowed nonpositive outside components remain
permitted. The prescribed data fix the flux and retained capacity; optional
selections can only reduce actual shared deficits.

For every k>=1 place k copies of W=64 in 80-by-80 blocks with two-vertex
margins, transpose alternating copies, and translate by (2,2+80j).
They fit because the baseline size is 70-by-74. Different blocks have no
occupied adjacency or mouth intersections. All counts and capacities add:
B=8k,F=-4k, exclusive weight 6k, capacity-two certificate 8k, retained-support
certificate 9k, and baseline K_loss+O=9k>8k. This is a general unbounded
family, with independently allocated physical resources in every block.

## 6. Validation and scope

`develop/check_capacity_aware_strips.py` checks 45 physical configurations,
24 symmetry images and 243 abstract capacity/weight cases. It checks even
W=64,...,84,100,160 and k=1,2,3,4,6,8, including feasible additional
selections. It verifies exact cut witnesses, capacities, original physical
union identities, feasibility, complete freezing and the initial objective
ledger. Small cut problems are independently compared with all subsets.
The prior 70 exclusive controls and 1,024 abstract graphs still pass after
generalizing their flow routine to finite edge capacities.

The local Lean 4.33.0 audit passes 102 scoped declarations. The two additions
prove arbitrary finite capped donor sums and the conditional capacity-two
pair objective implication. Full geometric adapters, all-width constructions
and the classical cut theorem remain written proofs.

Run:

    python3 develop/check_capacity_aware_strips.py --output output/capacity-aware-strip-controls.json
    python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0 --output output/capacity-aware-strip-formal-check.json

This note resolves a further capacity-two sharing regime. It does not settle
arbitrary negative flux, arbitrary positive bent sources or the universal
grid/triple-equality questions. In particular no mouth-based certificate
can pay the known zero-mouth-payment locality family without new exterior
or larger-region information. Submitted manuscripts are preserved.

The complementary `REMOTE_COMB_RUNG_COMPENSATION.md` supplies such exterior
payment for the explicit locality family and for general compatible rung
pairs. A joint independent review of these two new notes is live as task
75dcde82-64ab-4958-bedc-86b704d8f719, conversation conv_d93c64a01f45169f,
original stream 76055. No final ACCEPT is claimed.
