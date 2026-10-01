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

An independently optimized, higher-cardinality feasible completion on a
`6 x 12` rectangle has `|T|=7`, `|M|=26`, and `q=-3`. Its residual components
are:

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

An independently optimized, higher-cardinality feasible completion on a
`6 x 14` rectangle has `|T|=8`, `|M|=31`, and again `q=-3`. Its components are:

| component type | tile coordinates `(row,column)` | `e(C)` | `R(C)` | excess |
| --- | --- | ---: | ---: | ---: |
| mixed boundary corridor | `(0,5),(0,6),(1,4),(1,5),(1,6)` | 6 | 7 | -1 |
| isolated turn remainder | `(1,2)` | 0 | 1 | -1 |
| lower turn component | `(2,3),(2,4)` | 1 | 2 | -1 |
| all remaining components | `(0,0..4),(1,0),(1,1),(1,3),(2,0..2),(2,6)` | — | — | 0 |

Again the total excess is `-3`: two boundary/turn-connected units and one
additional turn-side unit. The extra `PP/BT` delay state changes the shape of
the residual corridors without removing the negative remainder.

## What this does and does not prove

These higher-cardinality completions establish a concrete obstruction to a
pure donor-budget proof: the shortest zero-budget mixed words are globally
realizable, but their exact ledger contains three negative units outside the
local certificate count. The right invariant is therefore a residual-demand
quantity, not simply the number of guarded tiles. A plausible future aggregate
statement would assign the observed negative remainder to boundary corridors
and turn-side capacity deficits, then prove that these assignments are
disjoint under bends and capacity-two passages.

The coordinate witnesses do not prove that every mixed interval has three units
of negative excess, nor that the same decomposition survives arbitrary
boundary placement, overlapping sources, or repeated capacity-two visits. They
also do not produce a new Lean theorem. The general obligation remains to show
that every unresolved mixed interval either reaches a certified donor or forces
an aggregate residual inequality of this kind, with a capacitated Hall argument
to prevent reuse across sources.

The exact coordinates, matching edges, component excesses, and input hashes
are archived in `output/guarded-half-donors-controls.json`; the finite checker
is `develop/check_guarded_half_donors.py`.
