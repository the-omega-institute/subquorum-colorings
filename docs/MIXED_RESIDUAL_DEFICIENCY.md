# Residual deficiency in the canonical mixed intervals

1 October 2026. This note records the exact residual accounting of the two
smallest globally feasible mixed-direction words that receive no certified
full or guarded half donor from the local budget automaton. It is a finite
coordinate result, not a general mixed-interval theorem.

## Residual graph and the quantity being measured

For a feasible pair `(T,M)` on an even-by-even rectangle, let `Q` be a tile.
Write `t(Q)` for its selected vertices, `h(Q)` for matching edges internal to
the tile, and `s(Q)` for matching edges from a saturated tile to an outside
endpoint. The residual capacity is

\[
 r(Q)=2-t(Q)-h(Q)-s(Q).
\]

The unsaturated tiles form a residual multigraph. For a connected component
`C`, let `e(C)` be its number of residual edges and `R(C)` the sum of the
capacities of its tiles. Its excess is `e(C)-R(C)`. Summing over components
recovers the exact objective ledger:

\[
 q=|T|+|M|-mn/2=\sum_C(e(C)-R(C)).
\]

Thus a negative component is a genuine remainder term. It cannot be counted
as a donor certificate a second time: the residual edge or capacity that makes
the component negative is already part of the exact global ledger.

## Width-four word

The parent exit word is

```text
PP/BP, BT/TB, BP/TP, PP/PB.
```

The `6 x 12` rectangle has a feasible completion with `|T|=7`, `|M|=26`, and
`q=-3`. For this fixed selected set, the checker supplies an upper-bound cover
with 22 ordinary endpoint constraints and 4 selected-vertex occupancy
constraints, so no completion with the same `T` can use more than 26 matching
edges. Its residual components are:

| component type | tile coordinates `(row,column)` | `e(C)` | `R(C)` | excess |
| --- | --- | ---: | ---: | ---: |
| boundary corridor | `(0,0),(0,1),(1,0),(1,1),(2,0)` | 6 | 7 | -1 |
| opposite corridor | `(0,5),(1,5),(2,5)` | 3 | 4 | -1 |
| turn-side remainder | `(2,3)` | 0 | 1 | -1 |
| all remaining components | `(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,2)` | — | — | 0 |

The component excesses are therefore `[-1,-1,-1,0,0,0,0,0]`. Two units come
from connected residual corridors and one from an isolated capacity-one tile.
The mixed child itself does not provide a negative tile charge, so these three
units are remainder rather than certified local donor budget.

## Width-five word

The second word is

```text
PP/BT, PP/BP, BT/TB, BP/TP, PP/PB.
```

The `6 x 14` rectangle has a feasible completion with `|T|=8`, `|M|=31`, and
again `q=-3`. For this fixed selected set, the checker supplies an upper-bound
cover with 28 ordinary endpoint constraints and 3 selected-vertex occupancy
constraints, proving that 31 is maximal for that `T`. Its components are:

| component type | tile coordinates `(row,column)` | `e(C)` | `R(C)` | excess |
| --- | --- | ---: | ---: | ---: |
| mixed boundary corridor | `(0,5),(0,6),(1,4),(1,5),(1,6)` | 6 | 7 | -1 |
| isolated turn remainder | `(1,2)` | 0 | 1 | -1 |
| lower turn component | `(2,3),(2,4)` | 1 | 2 | -1 |
| all remaining components | `(0,0..4),(1,0),(1,1),(1,3),(2,0..2),(2,6)` | — | — | 0 |

Again the total excess is `-3`: two boundary/turn-connected units and one
additional turn-side unit. The extra `PP/BT` delay state changes the shape of
the residual corridors without removing the negative remainder.

## Refined width-four word

The width-four parent word also admits a closer completion with the same
necessary labels:

```text
PP/BP, BT/TB, BP/TP, PP/PB.
```

On a `6 x 12` rectangle, take

```text
T = {(0,4),(2,5),(3,4),(3,6),(4,9),(5,8),(5,10)}.
```

The archived matching has `|M|=27`, hence `q=-2`. A fixed-`T` cover with 24
ordinary endpoint constraints, 3 selected-vertex occupancy constraints, and
the displayed B vertices forbidden certifies that no matching with this `T`
can use more than 27 edges. Its only negative residual components are

| tile coordinates | `e(C)` | `R(C)` | excess |
| --- | ---: | ---: | ---: |
| `(0,1),(1,0),(1,1)` | 3 | 4 | -1 |
| `(1,3),(1,4),(1,5),(2,3)` | 3 | 4 | -1 |

All other residual components have zero excess. This is a genuine mixed word
with only two units of negative remainder, so the three-unit observation from
the earlier two coordinate choices is not a lower bound at the parent-word
level.

## Near-saturated width-four word

The same parent word admits a still closer `6 x 12` completion with

```text
T = {(0,11),(2,5),(3,4),(3,6),(4,3),(4,5),(5,4)}.
```

The archived matching has 28 edges, giving `q=-1`. Its fixed-`T` certificate
uses 24 ordinary endpoint constraints, 3 selected-vertex occupancy constraints,
and the one remaining edge `(5,5)--(5,6)` at capacity one. Every admissible edge
is covered, so 28 is an upper bound for that selected set with the prescribed
blank labels. The residual excesses are

```text
[-1,0,0,0,0,0,0].
```

There is only one negative component, on tiles
`(0,1),(0,2),(0,3),(0,4),(0,5),(1,1),(1,4),(1,5),(2,4)`.
It has 10 residual edges and capacity 11. All other residual components have
zero excess. Thus a two-unit parent-word remainder floor is false; the
possibility of `q=0` remains open.

## Parent-label-only `q=0` relaxation

The checker also records a separate `6 x 12` feasible configuration with
`|T|=27`, `|M|=9`, and `q=0`, while fixing the same four parent labels

```text
PP/BP, BT/TB, BP/TP, PP/PB.
```

This is deliberately a relaxation: it constrains the parent tiles and the
matching feasibility, but does not impose the neutral pressure-band labels on
the surrounding tiles. The displayed completion has non-neutral tiles
`(0,0) = TB/PP` and `(2,0) = TB/TB`. Consequently it is not a counterexample
to the mixed-interval hypotheses. It does establish a precise obstruction to
any aggregate lemma whose hypotheses mention only the parent word: the proof
must use the neutral bands, boundary placement, or a component-routing
condition in an essential way. The coordinates, matching, and label checks
are archived under `parent_label_relaxation` in
`output/guarded-half-donors-controls.json`.

## Neutral-frame MILP discovery

To separate the relaxed obstacle from the neutral-band question, an optional
SciPy/HiGHS MILP restricts every tile outside the designated parent row to one
of the twelve locally neutral states. Tiles on the parent row may use any
locally feasible state, while the displayed parent labels, matching endpoint
incidence, and selected-vertex occupancy are imposed exactly. The resulting
solutions are then rechecked by `direct_check` and `canonical`.

For the width-four word on `6 x 12`, the corrected MILP optimum is
`|T|+|M|=35`, hence `q=-1`; its residual component excesses are
`[-1,0,0,0,0,0]`. For the width-five word on `6 x 14`, the corrected optimum
is `39`, hence `q=-3`, with three negative unit components and the rest zero.
Thus these two neutral-frame models do not admit a `q=0` completion, even
though the parent-label-only relaxation does.

**Correction.** The first exploratory version of the optional script minimized
only `|M|` and reported the superseded values `q=-2` and `q=-4`. The objective
now includes both selected vertices and matching edges, and the archived
output has been regenerated. The earlier values were never used by the
required CI controls or a manuscript claim.

This is finite discovery evidence, not a general neutral-frame theorem. The
model fixes two small parent words and treats the parent row more freely than
an eventual geometric proof may allow; it also says nothing about arbitrary
bends or larger frames. The complete MILP inputs, tile labels, matchings,
component excesses, and script hash are archived in
`output/neutral-frame-milp-controls.json`. The optional search is
`develop/search_neutral_frame_milp.py` and is not required by CI.

## One-sided neutral-band obstacle

The coordinate checker also records a different `6 x 12` feasible completion
with `|T|+|M|=36` and `q=0`. It has the same four parent labels, and every tile
in the upper adjacent row is neutral:

```text
PP/PP, PP/PP, BT/TB, PP/TB, BT/TB, TB/BT.
```

The lower adjacent row is unrestricted and contains the non-neutral labels
`PT/TB`, `BB/TP`, `TB/PT`, and `TP/BT`. The full matching is feasible, the
canonical routing check passes, and all nine residual component excesses are
zero. Thus a compensation rule using only one neutral pressure side cannot
force a negative remainder, even for this fixed parent word. The certificate
is stored as `one_sided_neutral_obstacle` in
`output/guarded-half-donors-controls.json`; it is an explicit coordinate
obstacle, not a general counterexample to the two-sided mixed-interval
hypotheses.

## What this does and does not prove

These fixed-`T` maximum completions establish a concrete obstruction to a
pure donor-budget proof: the shortest zero-budget mixed words are globally
realizable, but their exact ledger can contain only one negative unit outside
the local certificate count. The right invariant is therefore a residual-demand
quantity, not simply the number of guarded tiles or the parent word. A plausible
future aggregate statement must use the surrounding boundary placement and
turn-side capacity deficits, then prove that its assignments are disjoint under
bends and capacity-two passages.

The coordinate witnesses do not prove that every mixed interval has one unit
of negative excess, nor that the same decomposition survives arbitrary
boundary placement, overlapping sources, or repeated capacity-two visits. They
also do not produce a new Lean theorem. The general obligation remains to show
that every unresolved mixed interval either reaches a certified donor or forces
an aggregate residual inequality of this kind, with a capacitated Hall argument
to prevent reuse across sources.

The exact coordinates, matching edges, component excesses, and input hashes
are archived in `output/guarded-half-donors-controls.json`; the finite checker
is `develop/check_guarded_half_donors.py`.
