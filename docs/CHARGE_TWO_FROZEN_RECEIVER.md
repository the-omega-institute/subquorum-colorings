# A completely frozen receiver of charge two, with distinct owned compensation

20 October 2026. The proposed universal whole-receiver ceiling rho_H<=1 is
false, even when no simultaneous promotion bundle of any orientation is
feasible. This explicit example has rho_H=2. It refutes that intermediate
rule, not the coefficient-one grid inequality or the proposed triple equality.
In fact it has four distinct capped-corner donor tiles, enough to pay its
charge without reusing any physical deficit.

The candidate came from Oracle task eb07cc29-ff20-402b-aa9b-2a7d2ef567a9.
The original response is archived without alteration. The construction,
certificate and original corrected-charge computation below were independently
checked by develop/check_charge_two_frozen_receiver.py. No Lean validation is
claimed for this new example or the weighted criterion below.

## 1. Complete physical specification and feasibility

Use nearest-neighbor adjacency on {0,...,13} x {0,...,9}. Coordinates always
have the first axis of length 14 and the second of length 10. Physical tiles
are Q_(i,j)={2i,2i+1} x {2j,2j+1}. All unspecified vertices are blank.
The machine-readable complete specification is
develop/charge_two_frozen_receiver.json.

Take the following 20 selected vertices:

    T={(0,4),(1,5),(2,3),(2,1),(3,0),(3,5),(5,0),(4,6),(5,7),(8,0),(9,6),(7,7),(8,9),(9,8),(10,0),(10,5),(11,4),(11,2),(12,0),(13,1)}.

Take all 19 matching edges:

    (1,4)--(2,4)
    (3,1)--(4,1)
    (3,4)--(4,4)
    (6,2)--(7,2)
    (6,5)--(7,5)
    (7,3)--(8,3)
    (7,4)--(8,4)
    (9,1)--(10,1)
    (9,4)--(10,4)
    (11,1)--(12,1)
    (4,2)--(4,3)
    (5,1)--(5,2)
    (5,3)--(5,4)
    (5,5)--(5,6)
    (6,3)--(6,4)
    (8,1)--(8,2)
    (8,5)--(8,6)
    (8,7)--(8,8)
    (9,2)--(9,3)

The endpoints are distinct, T is disjoint from them, and every edge is a
nearest-neighbor edge. Put P=V(M). There are no T--T edges; every selection
has exactly one occupied neighbor. The full endpoint set has 38 vertices
and is connected: its central {4,...,9} x {2,3,4} rectangle is connected,
and the remaining displayed endpoint segments attach to it. Thus H=P is
one complete endpoint component.

The certificate below also checks single terminality: its two witnesses
are distinct occupied neighbors of v_i, different from its actual mate.
Consequently every endpoint has occupied degree at least three. Direct
counting gives 28 endpoints of occupied degree three and 10 of degree four.

## 2. A proof excluding every mixed-direction promotion bundle

Write m for the actual matching involution. In each row, the two witnesses
are distinct neighbors of v_i, neither is m(v_i), and each is either in T
or the actual mate of an earlier listed endpoint.

| Step i | Endpoint v_i | First retained witness | Second retained witness |
| --- | --- | --- | --- |
| 1 | (1,4) | (1,5) in T | (0,4) in T |
| 2 | (3,1) | (3,0) in T | (2,1) in T |
| 3 | (3,4) | (3,5) in T | (2,4) = m(v1) |
| 4 | (5,1) | (5,0) in T | (4,1) = m(v2) |
| 5 | (5,6) | (5,7) in T | (4,6) in T |
| 6 | (8,8) | (8,9) in T | (9,8) in T |
| 7 | (10,4) | (10,5) in T | (11,4) in T |
| 8 | (12,1) | (12,0) in T | (13,1) in T |
| 9 | (4,2) | (4,1) = m(v2) | (5,2) = m(v4) |
| 10 | (5,3) | (5,2) = m(v4) | (4,3) = m(v9) |
| 11 | (5,4) | (5,5) = m(v5) | (4,4) = m(v3) |
| 12 | (8,6) | (8,7) = m(v6) | (9,6) in T |
| 13 | (10,1) | (10,0) in T | (11,1) = m(v8) |
| 14 | (4,3) | (4,4) = m(v3) | (5,3) = m(v11) |
| 15 | (4,4) | (4,3) = m(v9) | (5,4) = m(v10) |
| 16 | (5,2) | (5,3) = m(v11) | (4,2) = m(v14) |
| 17 | (8,1) | (8,0) in T | (9,1) = m(v13) |
| 18 | (8,4) | (8,5) = m(v12) | (9,4) = m(v7) |
| 19 | (9,2) | (9,1) = m(v13) | (8,2) = m(v17) |
| 20 | (2,4) | (2,3) in T | (3,4) = m(v15) |
| 21 | (4,1) | (4,2) = m(v14) | (5,1) = m(v16) |
| 22 | (6,4) | (7,4) = m(v18) | (5,4) = m(v10) |
| 23 | (7,3) | (7,4) = m(v18) | (6,3) = m(v22) |
| 24 | (7,5) | (7,4) = m(v18) | (8,5) = m(v12) |
| 25 | (8,3) | (8,2) = m(v17) | (9,3) = m(v19) |
| 26 | (9,3) | (9,4) = m(v7) | (8,3) = m(v23) |
| 27 | (5,5) | (5,4) = m(v10) | (6,5) = m(v24) |
| 28 | (6,2) | (6,3) = m(v22) | (5,2) = m(v4) |
| 29 | (6,3) | (7,3) = m(v25) | (5,3) = m(v11) |
| 30 | (6,5) | (6,4) = m(v29) | (5,5) = m(v5) |
| 31 | (7,2) | (7,3) = m(v25) | (8,2) = m(v17) |
| 32 | (7,4) | (7,5) = m(v30) | (7,3) = m(v25) |
| 33 | (8,2) | (8,3) = m(v23) | (9,2) = m(v26) |
| 34 | (8,5) | (8,4) = m(v32) | (7,5) = m(v30) |
| 35 | (8,7) | (8,6) = m(v34) | (7,7) in T |
| 36 | (9,1) | (9,2) = m(v26) | (8,1) = m(v33) |
| 37 | (9,4) | (9,3) = m(v19) | (8,4) = m(v32) |
| 38 | (11,1) | (11,2) in T | (10,1) = m(v36) |

These 38 rows list every endpoint once. Suppose a nonempty feasible bundle
promotes a set S of endpoints, choosing at most one endpoint from any
matching edge and removing precisely their mates. Choose the least i with
v_i in S. Original selections remain occupied. A witness m(v_j) with j<i
also remains occupied: its deletion would require promoting v_j, contrary
to the choice of i. Thus both distinct witnesses of v_i remain occupied,
contradicting feasibility at this newly selected vertex.

This is a finite acyclic certificate plus an argument for arbitrary bundles.
It does not enumerate bundles and imposes no checkerboard restriction.
The same certificate works in any larger feasible configuration preserving
these endpoints, matching edges and selected supports.

## 3. Exact original charge, including saturated-mate transfers

The receiver has 17 tiles. Its inventory is:

| Endpoint count p | Selected count t | Blank count b | Number of tiles | Raw excess per tile t+p/2-2 |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 6 | 1/2 |
| 2 | 1 | 1 | 5 | 0 |
| 3 | 0 | 1 | 2 | -1/2 |
| 4 | 0 | 0 | 4 | 0 |

Exactly the three selections (2,3), (7,7), (11,2) lie outside the receiver.
It therefore contains 17 selections, 38 endpoints and 13 blanks, giving

    rho_H = 17 + 38/2 - 2*17 = (17-13)/2 = 2.

The table gives raw excesses, not the original corrected charge of each
individual tile. In particular a saturated (p,t)=(1,2) tile has original
corrected charge zero, rather than 1/2. Its half unit transfers to the tile
containing the actual mate. All six transfers stay within the complete
receiver, so the whole raw and corrected sums agree. Direct computation
from the original graph record gives twice-charge 4: the four tiles
(1,2), (2,0), (4,3), (5,0) each have corrected charge 1/2, and every other
receiver tile has corrected charge zero. This separately checks the
original definition rather than assuming that the raw tile values are
already corrected values.

Every receiver blank is forced blank when these supports and the complete
component are preserved: it either has two endpoint neighbors, or is adjacent
to a selected support which already sees an endpoint. Hence a feasible
exterior completion cannot change the receiver labels or its charge.

The whole 14-by-10 rectangle has objective |T|+|M|=39, half-area 70 and
deficit 31. Its 18 endpoint-free tiles have total deficit D_all=33. The
original ledger reads 70-39=33-2. This is not a counterexample to the grid
inequality.

## 4. More than one owned unit per component

The old capped-corner witness from ELBOW_OWNED_DONORS.md appears at these
four distinct physical tiles:

| Tile index | Northwest vertex | Selections in tile | Actual deficit |
| --- | --- | --- | --- |
| (1,1) | (2,2) | (2,3) | 1 |
| (3,0) | (6,0) | none | 2 |
| (3,3) | (6,6) | (7,7) | 1 |
| (5,1) | (10,2) | (11,2) | 1 |

There are five oriented witness descriptions, because two describe the
same tile (3,0). They provide four resources, not five. The verifier deduplicates
by physical tile identity before adding capacities. Their actual total
capacity is 5. The capped-corner lemma guarantees at least one unit per
tile in any feasible single-terminal exterior preserving the complete
component and selected supports. In particular the distinct tiles (1,1)
and (3,3) pay the entire charge 2. Each contains its displayed prescribed
selection, so its deficit stays exactly 1 in such an exterior. No second
copy of their deficit, phase gain or negative charge is added.

The old unique-owner proof also guarantees that a capped witness of a
different complete endpoint component cannot claim either reserved tile.

**Weighted owned-witness criterion.** Consider a feasible single-terminal
representative on an even-by-even rectangle. For each complete endpoint
component H of positive corrected charge choose a set W_H of distinct
physical tiles, each with an old capped-corner witness assigned to H.
Suppose

    sum_(Q in W_H) (2-|T intersect Q|) >= rho_H

for every such H. Then |T|+|M|<=mn/2. No upper bound of one on rho_H is
required.

Proof. Each witness tile is endpoint-free and has nonnegative actual
deficit at least one by the old local lemma. Its unique-owner lemma makes
W_H and W_K disjoint for different components H and K. Each W_H is a set,
so multiple orientations of one witness tile contribute only once.
Consequently

    sum_(rho_H>0) rho_H
      <= sum_(rho_H>0) sum_(Q in W_H) d_Q
      <= sum_(Q has no endpoints) d_Q = D_all.

Nonpositive receiver charges only decrease the total. Substitution into
the exact original identity mn/2-|T|-|M|=D_all-sum_H rho_H proves the claim.
The proof uses the existing local and unique-owner lemmas; its extension
is allowing several distinct owned tiles to pay a receiver's actual
charge instead of assuming rho_H<=1. QED.

A purely structural sufficient condition is at least ceiling(rho_H)
distinct witness tiles per positive component, since every such tile has
deficit at least one. The example satisfies this with room to spare.
This establishes a usable criterion and compensation for the obstruction,
not its universal coverage. Whether every frozen positive component
admits sufficient owned capacity from the two old corner rules has since been
refuted, even in occupied degree three. See the
[corner-coverage obstruction and compatible endpoint guard](CORNER_FREE_FROZEN_RECEIVER_AND_ENDPOINT_GUARDS.md).
General coverage by that enlarged three-rule collection is also false; see
[the second frozen obstruction](THREE_RULE_FROZEN_COVERAGE_OBSTRUCTION.md).

## 5. Verification and next research

22 October update: the original fixed-matching freezing certificate remains
valid, but this fixture is not terminal under matching replacement followed
by promotion. One square exchange unlocks a five-edge bundle and splits it
into two uniquely matched, fully frozen charge1 components. All three freed
tiles are saturated, so total receiver charge stays2 and no deficit is
created. See [the general exchange and flux lemma](REMATCHING_NORMALIZATION_AND_RECEIVER_FLUX.md).
This strengthens the normal form available for future extremal arguments;
it does not change the original counterexample's fixed-matching scope.

Run:

    python3 develop/check_charge_two_frozen_receiver.py --output output/charge-two-frozen-receiver-controls.json

The checker validates feasibility, all actual matching edges, connectivity,
the ordered certificate, an independently computed freezing closure, original
corrected charge and transfers, all receiver labels, all distinct capped
witness resources, the exact global ledger, and all eight physical symmetries.
Closure layers have sizes 6,4,4,4,5,6,4,3,2. These checks supplement the
least-index proof; no exhaustive bundle search is being used as a proof.

The unrestricted ceiling must be removed from the research next actions.
The next structural question is charge-sensitive donor coverage, including
positive components with few or no owned corners. A second question is whether
fully frozen charge can grow without bound in a single connected component.
This example alone does not establish unboundedness. The earlier coefficient-one
theorems under explicitly stated charge-at-most-one hypotheses remain valid.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
