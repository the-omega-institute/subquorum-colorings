# Compensation for bent and branched occupied collars

19 October 2026. This extends the straight opposed receiver argument in
`OPPOSED_SOURCE_COMPENSATION.md`. The extension concerns a precisely defined
class of receiving regions, not arbitrary bent sources or the universal grid
conjecture. The proof below works for all finite sizes without enumeration.

## Setup and local accounting

Fix a feasible representative pair (T,M) in an even-by-even rectangle.
Write P for matching endpoints and B for unoccupied vertices. Every T vertex
has at most one occupied neighbor in T union P. Partition into aligned 2x2
tiles. As in the existing regional ledger, deficient tiles have capacity
r=2-t-h-s and charge rho=d/2-r; saturated tiles (t=2) have charge zero.
All charges and residual degrees refer to the full original configuration,
including edges leaving the region. Matching directions are unrestricted.

A face of a tile is **pressured** if both vertices immediately across it
exist in the ambient rectangle and are occupied. Pressure concerns the
actual two external neighbors, not matching partners or a hypothetical
continuation beyond the outer boundary.

**Local lemma.** In a feasible tile with a pressured face, b>=t; if t=2,
the tile contains no P vertex. If a face is BB and its two perpendicular
faces are pressured, then b-t>=2.

Proof. Three selected corners are impossible: one has two selected internal
neighbors. For t=0 the first bound is immediate. For t=1 the selected corner
has two internal neighbors, at least one of which is blank. For t=2 adjacent
selected corners, both other corners must be blank. For t=2 diagonal corners,
every face contains a selected corner. On a pressured face that corner already
has an occupied external neighbor, forcing its two internal neighbors blank.
This also proves that t=2 leaves no matching endpoint. Finally suppose one
face is BB and both perpendicular faces are pressured. The remaining two
corners are adjacent and each already has an occupied external neighbor.
They cannot both be T; if one is T, the other remaining corner must be B. Thus they contribute
nonnegative b-t in addition to the two cap blanks. QED.

The lemma is a direct argument about the square, including capacity-two
tiles. It does not allocate one unit for every visit of a residual route.

## General collar theorem

Let R be a nonempty tile region. Choose L **distinct** marked tiles, each
with a BB face and two perpendicular pressured faces. Require every other
tile of R to have at least one pressured face. The pressured faces need
not all be exterior to R for this general formulation; their actual outside
neighbors must satisfy the pressure definition. No residual-closure condition
is imposed on R.

Write t,b for vertex counts in R, mu for matching edges wholly in R, and j
for **all** physical matching edges with exactly one endpoint in R. Let sigma
count those edges whose inside endpoint tile is deficient and whose outside
endpoint tile is saturated. Then

    b-t >= 2L + (j mod 2),
    2rho(R) <= -2L + sigma - (j mod 2).                 (1)

Proof. Each marked tile supplies surplus at least two. Every other tile
supplies a nonnegative surplus. Tiles partition R, so b-t>=2L and no vertex
is used in two local counts. The matching vertex partition is exact:

    4|R_tiles| = t+b+2mu+j.

Consequently b-t has the same parity as j. Its least possible value at or
above the even integer 2L is 2L+(j mod 2). The local lemma also proves that
no saturated tile in R has a matching endpoint. In particular there is no
matching edge from a saturated tile inside R to a deficient tile outside.
For a deficient tile, let c count physical matching crossings at the tile.
Then 4=t_tile+b_tile+2h+c and d=c-s. Consequently
2rho_tile=d-2(2-t_tile-h-s)=t_tile-b_tile+s. The saturated tiles inside R
have t_tile=b_tile=2 and no P, so contribute zero to both sides. Every s
edge from a deficient tile of R must end outside R, because no saturated
tile inside has a P endpoint. Summing the tile identities gives

    2rho(R) = t-b+sigma.

Substitution proves the charge estimate. All residual boundary half-charges
remain in rho; no assumption that residual components stay inside R has
been made. QED.

**Tree corollary.** Suppose the induced tile-adjacency graph of R is a tree
of maximum degree at most three, with at least two tiles. In every leaf tile,
take the face opposite its unique neighbor as an end cap and require it BB.
Across every other exposed face of R require both actual exterior neighbors
to exist and be occupied. Then (1) holds with L equal to the number of leaf
tiles. In particular a path, with arbitrarily many bends, has L=2 and
rho(R)<=-2+(sigma-(j mod 2))/2. Branches contribute additional distinct
leaf budgets.

Proof. A leaf's two perpendicular faces are exposed and pressured. Every
nonleaf has degree two or three and therefore at least one exposed pressured
face. Apply the theorem. No straightness or matching direction is used. QED.

The same proof works for any region of maximum tile degree three satisfying
these cap/pressure assumptions; the tree condition is a convenient concrete
class. Degree-four interior tiles need a separate argument.

## Cross-component compensation without reusing a receiver

Let U_1,...,U_k be pairwise tile-disjoint source regions, disjoint from R,
whose full-configuration charges satisfy sum rho(U_i)<=L. They may interact
through residual matching edges, and need not be individual residual
components. Additivity over this tile partition and (1) give

    rho(R union U_1 union ... union U_k)
        <= (sigma-(j mod 2))/2.                        (2)

Thus sigma<=j mod 2 pays the entire aggregate source charge. This includes
sigma=0 and permits one saturated export if j is odd. The latter is a
conditional budget statement, not an assertion of existence for every shape.

The receiver is inserted exactly once in (2); the L leaf budgets belong to
distinct tiles. A capacity-two tile is counted once regardless of how many
residual strands visit it. Counting an external pressured vertex in two
feasibility implications does not consume a charge resource: the resources
being summed are disjoint internal blank surpluses. A proof may not apply
(2) twice to overlapping receivers or omit an uncharged remainder.

For pairwise tile-disjoint compensated cores, if the remaining deficient
tiles have nonpositive aggregate charge, the exact full-grid identity gives
q=|T|+|M|-mn/2<=0. On this explicit sufficient class, the matching coefficient
is one, improving the existing 5/6 coefficient by |M|/6 in the objective.
This does not improve the universal 5/6 bound. Thick regions, unpressured
fronts, and overlapping receivers that cannot be partitioned remain open.

## Checks and precise formal scope

`develop/check_pressured_collar_compensation.py` checks every pressured local
label state and every oriented terminal state. It also constructs actual
ambient-grid matchings for straight, bent and branched receivers, verifies
all matching and feasibility constraints, checks the original residual
regional ledger, and tests all eight rectangle symmetries. The fixtures
include a forced right-angle residual passage and a capacity-two tile.
Further physical fixtures check odd j, a saturated receiver tile, and an
actual single saturated export with odd j and charge exactly -2. The last
fixture realizes the parity-permitted export case in (2).
These are receiver-budget examples, not whole-grid counterexamples or a
claim that every abstract tree admits such a completion.

`formal/SubQuorum/CollarCompensation.lean` separates kernel-checked finite
tile implications from arbitrary-list summation and conditional integer
parity/charge/source accounting. The geometric adapter, matching vertex
partition and regional ledger are explicitly supplied mathematical
interfaces, with written proofs here and in the earlier ledger notes.
It does not formalize arbitrary rectangular grids end to end.

The controls pass 396 feasible pressured label/mask states, 24 oriented
terminal states, 25 physical receiver configurations and 192 symmetry
images. The original local Lean 4.33.0 audit passes six declarations;
all axiom sets are contained in {propext, Quot.sound}. No sorry,
native_decide, compiler trust or new axiom is used. The geometry and
regional identity remain the explicit written interfaces described above.

```sh
python3 develop/check_pressured_collar_compensation.py --output output/pressured-collar-controls.json
python3 scripts/check_collar_formal.py --lean /path/to/lean4.33.0/bin/lean --output output/pressured-collar-formal-check.json
```

Exact receipts are `output/pressured-collar-controls.json` and
`output/pressured-collar-formal-check.json`. The independent Oracle review
b202768d-c3d3-4717-bcec-899be37ac2ae completed ACCEPT, with observed model
gpt_6 and effort pro. It checks the written argument, including exact
boundary accounting and no reuse; it did not execute the code or Lean.
The exact response and assessment are linked from
`output/pressured-collar-oracle-review.json`.

The later [attachment-corrected theorem](ATTACHMENT_CORRECTED_COLLAR_COMPENSATION.md)
removes pressure on unmarked tiles and the tree/degree condition at the cost
of an explicit internal attachment debt and changed parity. That extension
is outside the preceding review input. The current combined local Lean
runner audits ten declarations, six original and four for that extension.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
