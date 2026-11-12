# Auxiliary squares: all owner paths and even cycles

The owner-size condition is removed. Let A be a disjoint union of C4s on
N=4s indices, and let B be any finite simple graph on the same indices whose
components are paths or even cycles. Then there is an A-independent set S
which is dissociation in B and satisfies |S|>=ceil(N/3). No physical colouring
is needed in this abstract theorem.

For a physical partial template N=2b. The previously proved exact normalization
beta_I=2b+max|S| gives beta_I>=ceil(8b/3) whenever every auxiliary component
is a square. The30vertex block with beta_I16=8b/3 proves the coefficient sharp.
General auxiliary paths and longer even cycles remain open.

## Why the multiple exchanges can be used together

Each exceptional owner cycle, of order4mod6 or2mod6, has a prescribed-edge
exchange between two maximum dissociation sets differing exactly at that
edge's ends. Choose at most one edge per owner cycle, and require their
projections onto auxiliary squares to form a forest of rankr. The choices
are then independent on the owner graph. Leaf-to-root toggles make at least
r square intersections odd. Choosing independent subsets in each square
therefore produces at leastceil((beta_2(B)+r)/2) compatible owners.

The required rank exists after handling two closed types separately: one
ownerC4 on one auxiliary square, or two ownerC4s on two auxiliary squares.
They give2 and3 compatible owners respectively. Coincidence here means the
same vertex support, not necessarily identical owner/auxiliary edge sets.

For any subset of remaining exceptional cycles, a connected projected component
withx cycles of order4mod6 andy of order2mod6 uses at leastx+2y squares.
Its rank is thus at least(2x+y)/3. The two apparent exceptions would fill
one or two squares completely and hence be exactly the closed types removed.
This holds for EVERY cycle subset, not just the whole source set.

Rado's independent-representative rank formula, proved in the manuscript,
then supplies one rainbow forest withr at least the total owner deficit
relative to2N/3. Thus beta_2(B)+r>=2N/3, proving the target. Each owner cycle
supplies one exchange, each square contributes its rounding once, and all
subset rank constraints belong to the same forest.

[Full proof](../manuscript/auxiliary-square-forest-proof.tex) includes the graphic
representative lemma with its tight-set contraction and dummy-edge arguments.
Rado's classical theorem is credited; the new deduction is the square-capacity
rank inequality and its use to remove the owner-size hypothesis.

## Construction and verification

Run `python3 -B scripts/check_auxiliary_square_forest.py`.
The [construction](../develop/auxiliary_square_forest.py) returns actual owner
and witness indices, maximum owner choices, a rainbow forest, its parity flips,
and a dual graphic/partition rank upper certificate. The upper certificate
independently certifies maximum forest size; larger cases do not claim exact
all-helper optima. The executable API validates physical colours, while the
written theorem is colour-free.

The deterministic checker covers:

- 2,644 physical templates and valid certificates, including331 which fail
  the preceding owner-size criterion; largest cases have64helpers/320physical
  vertices. There are273 exact small all-helper comparisons and47,520 literal
  owner-subset evaluations.
- 420 coloured multigraph controls,81,197 literal edge subsets and5,016
  literal Rado rank subsets, with parallel edges and loops included.
- 2,644 dual rank cuts and37,934 cycle-subset rank inequality checks. The
  returned constructions use5,640 residual forest edges and explicitly handle
  73 closed four-index and29 closed eight-index components.
- 360 abstract models without imposed physical colour compatibility, checked
  against all252,000 auxiliary-independent subset choices.
- The three preceding critical fixtures, a new connected100vertex fixture, empty template, and an excluded
  auxiliary eight-cycle. Exclusion of a longer auxiliary cycle is an API
  applicability result, not a counterexample to the general target.

The all-size theorem has a complete written proof. Finite computation checks
its construction and boundaries. The independent review and actual exact-source
execution scope are recorded in output/auxiliary-square-forest-review.json.

For a fixed actual witness extraction with auxiliary squares, the retained set
therefore gives the existing conditional5/51 graph bound without an owner-size
condition. To bound SF_2-beta_2 requires such an extraction from a
maximum-cardinality minimal forming set. The unrestricted subcubic interval
[1/20,7/71], general template8b/3, physical multiple-Hall routing, universal
unit5/6 improvement and arbitrary-width rectangular grid triple equality remain
open. October's submitted manuscript is preserved.

## A connected instance rejected by both preceding sufficient tests

The [fixed five-C8 input](../develop/fixtures/auxiliary-square-forest.json)
has20helpers,40indices and100physical vertices. Its owner graph is fiveC8s,
so beta_2(B)=25 while the preceding size threshold is26. Its K4-free owner
matching2SAT remains unsatisfiable: the three obstructing auxiliary squares
of the previous two-C8 fixture are untouched, while the fourth square and
three appended C8s are connected through opposite-colour P-pair swaps.
Thus all four old owner-phase combinations still contain a K4 regardless
of the three new phases. All auxiliary components remain C4s.

The new certificate has a rainbow forest of size5 and56physical selected
vertices, all with selected degree at most1. The instance is connected,
bipartite, minimum degree2 and maximum degree3. This verifies an actual
construction; no exact all-helper or unrestricted optimum is asserted for
the100vertex graph.
