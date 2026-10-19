# A frozen receiver can need deficit beyond all neighboring physical tiles

20 October 2026. The failure of local corner rules is not repaired simply by
allowing every endpoint-free neighboring tile to donate. The explicit frozen
8-by-10 configuration below has corrected receiver charge one, while every
endpoint-free tile sharing an edge OR a corner with its receiver has deficit
zero. Its only positive resource is a physical tile at tile distance two.

This refutes the neighboring-resource coverage inequality even for
one complete component, where competition between owners is absent. It does
not refute the full grid target: its objective is 39, below half-area 40.
The first drawing includes boundary vertices; the selected-border extension
below puts every endpoint strictly inside a larger rectangle and retains the
obstruction. No invariance under unchanged blank padding and no new Lean
formalization are claimed.

## 1. Exact configuration

Use coordinates {0,...,7} x {0,...,9}, with all unlisted sites blank.
The selection set is

    T={(0,0),(0,2),(0,9),(1,1),(2,0),(2,6),(2,9),(3,5),(3,7),
       (4,0),(4,3),(4,6),(4,9),(5,2),(5,4),(5,5),(5,7),
       (6,0),(6,3),(6,6),(6,9),(7,1),(7,3),(7,6),(7,8)}.

The actual matching consists of these fourteen edges:

    (0,3)--(0,4)   (0,5)--(0,6)   (0,7)--(0,8)
    (1,3)--(2,3)   (1,4)--(1,5)   (1,6)--(1,7)
    (1,8)--(2,8)   (2,1)--(2,2)   (2,4)--(3,4)
    (3,1)--(4,1)   (3,2)--(3,3)   (3,8)--(4,8)
    (5,1)--(6,1)   (5,8)--(6,8).

They cover 28 distinct endpoints P. The whole drawing is

```text
T.TPPPPPPT
.T.PPPPPP.
TPPPP.T.PT
.PPPPT.TP.
TP.T..T.PT
.PT.TT.TP.
TP.T..T.PT
.T.T..T.T.
```

The selections (0,0) and (4,6) are isolated. Three pairs of selections are
adjacent: (5,4)--(5,5), (6,3)--(7,3), and (6,6)--(7,6). Each of their
endpoints has no other occupied neighbor. Every other selection has exactly
one endpoint neighbor. Thus every selection has occupied degree at most
one and the configuration is feasible.
The bar and the left chamber are joined by (1,3)--(2,3); the right column
joins the bar at (1,8). The legs attach to the chambers. Thus P is one
complete connected component H. Of its endpoints, 23 have occupied degree
three and five have occupied degree four.

## 2. A complete certificate excludes every mixed bundle

Write m for the actual mate. The following table lists all 28 endpoints
once. Every row has two distinct adjacent neighbors other than its own
mate, each either selected or the mate of an earlier row.

| i | v_i | First retained neighbor | Second retained neighbor |
| --- | --- | --- | --- |
| 1 | (2, 1) | (1, 1) in T | (2, 0) in T |
| 2 | (6, 1) | (6, 0) in T | (7, 1) in T |
| 3 | (6, 8) | (6, 9) in T | (7, 8) in T |
| 4 | (4, 1) | (4, 0) in T | (5, 1)=m(v_2) |
| 5 | (4, 8) | (4, 9) in T | (5, 8)=m(v_3) |
| 6 | (2, 8) | (2, 9) in T | (3, 8)=m(v_5) |
| 7 | (3, 2) | (2, 2)=m(v_1) | (3, 1)=m(v_4) |
| 8 | (0, 8) | (0, 9) in T | (1, 8)=m(v_6) |
| 9 | (2, 3) | (2, 2)=m(v_1) | (3, 3)=m(v_7) |
| 10 | (3, 4) | (3, 3)=m(v_7) | (3, 5) in T |
| 11 | (0, 3) | (0, 2) in T | (1, 3)=m(v_9) |
| 12 | (1, 4) | (1, 3)=m(v_9) | (2, 4)=m(v_10) |
| 13 | (1, 7) | (0, 7)=m(v_8) | (1, 8)=m(v_6) |
| 14 | (0, 5) | (0, 4)=m(v_11) | (1, 5)=m(v_12) |
| 15 | (0, 6) | (0, 7)=m(v_8) | (1, 6)=m(v_13) |
| 16 | (1, 6) | (1, 5)=m(v_12) | (2, 6) in T |
| 17 | (0, 7) | (0, 6)=m(v_14) | (1, 7)=m(v_16) |
| 18 | (1, 5) | (0, 5)=m(v_15) | (1, 6)=m(v_13) |
| 19 | (0, 4) | (0, 5)=m(v_15) | (1, 4)=m(v_18) |
| 20 | (1, 8) | (0, 8)=m(v_17) | (1, 7)=m(v_16) |
| 21 | (1, 3) | (0, 3)=m(v_19) | (1, 4)=m(v_18) |
| 22 | (3, 8) | (2, 8)=m(v_20) | (3, 7) in T |
| 23 | (2, 4) | (1, 4)=m(v_18) | (2, 3)=m(v_21) |
| 24 | (3, 3) | (2, 3)=m(v_21) | (4, 3) in T |
| 25 | (5, 8) | (4, 8)=m(v_22) | (5, 7) in T |
| 26 | (2, 2) | (2, 3)=m(v_21) | (3, 2)=m(v_24) |
| 27 | (3, 1) | (2, 1)=m(v_26) | (3, 2)=m(v_24) |
| 28 | (5, 1) | (4, 1)=m(v_27) | (5, 2) in T |

Suppose a nonempty feasible bundle promotes endpoints of distinct actual
matching edges and removes their mates. Choose its least promoted row i.
Original selections remain occupied. A neighbor m(v_j) with j<i also remains
occupied: deleting it would require promoting v_j, contradicting minimality
of i. Consequently v_i retains both displayed neighbors and is not feasible
as a selection. This contradiction proves complete freezing for arbitrary
mixed bundles, without enumerating them.

Each row additionally displays two occupied neighbors besides its actual
mate, directly certifying single terminality.

## 3. Exact receiver and original corrected charge

Use physical tiles Q_(i,j)={2i,2i+1} x {2j,2j+1}. The complete receiver is

    R_H={(0,1),(0,2),(0,3),(0,4),
         (1,0),(1,1),(1,2),(1,4),
         (2,0),(2,4),(3,0),(3,4)}.

It has 12 tiles, 28 endpoints, 11 selections and nine blanks. Therefore

    rho_H=11+28/2-2*12=1.

The original corrected definition includes two half-unit transfers from
the saturated bottom tiles Q_(3,0),Q_(3,4) along their actual mates into
Q_(2,0),Q_(2,4). Both remain in the complete receiver. Summing the original
corrected graph charges independently gives twice-charge two, in agreement
with this inventory. Individual raw tile charges are not substituted for
the corrected definition.

## 4. Exhaust every possible neighboring donor tile

The eight endpoint-free tiles have the following inventories. Let
dist_edge be physical tile Manhattan distance to R_H and dist_corner the
Chebyshev tile distance, which allows both edge and corner steps.

| Tile Q | Selections | Actual deficit | dist_edge | dist_corner |
| --- | --- | --- | --- | --- |
| (0,0) | (0,0),(1,1) | 0 | 1 | 1 |
| (1,3) | (2,6),(3,7) | 0 | 1 | 1 |
| (2,1) | (4,3),(5,2) | 0 | 1 | 1 |
| (2,2) | (5,4),(5,5) | 0 | 1 | 1 |
| (2,3) | (4,6),(5,7) | 0 | 1 | 1 |
| (3,1) | (6,3),(7,3) | 0 | 1 | 1 |
| (3,2) | none | 2 | 2 | 2 |
| (3,3) | (6,6),(7,6) | 0 | 1 | 1 |

There are no other endpoint-free physical tiles. In particular all seven
tiles sharing an edge or corner with R_H have zero deficit. The only
positive tile Q_(3,2) has corners (6,4),(6,5),(7,4),(7,5) and is entirely
blank. Its closest vertex is at graph distance three from P. Hence

    sum_(Q endpoint-free, dist_corner(Q,R_H)=1) d_Q = 0 < rho_H=1.

This is a fully explicit refutation of that coverage inequality, rather
than a failure of a particular pattern scanner. All four previously proved
corner rules also have zero capacity: their deficit-positive tiles would
be among the neighboring tiles just exhausted.

The total original outside deficit is two, so the full ledger is

    mn/2-|T|-|M|=40-25-14=1=2-rho_H.

One unit of Q_(3,2)'s actual capacity can be reserved for H, and the other
remains. It would be incorrect to spend this same tile once per route
reaching it in a future allocation proof. With one component the reservation
is immediate; the general multi-component routing statement is not proved
by this example.

## 5. Verification and implication

Run the standard-library checker:

    python3 -B develop/check_remote_deficit_obstruction.py --output output/remote-deficit-obstruction-controls.json

It checks feasibility, matching, complete connectedness, every row of the
28-step certificate, an independently calculated freezing closure, the
original corrected receiver ledger and saturated transfers, all eight
endpoint-free tile capacities and distances, and all four local donor scans.
All eight physical symmetries pass. The selected-border extension below
also passes all eight symmetries, including restriction to the original
labels and the translated full freezing certificate. The exact JSON source
includes both configurations and the certificate; they can be checked
without a solver.

Discovery used Z3 5.3.1 in the original 8-by-10 rectangle with a connected
fully frozen positive receiver and a strict deficit in its endpoint-adjacent
resource set. The returned configuration was then found to satisfy the
stronger edge-or-corner tile-neighborhood obstruction above. No search result
is used to prove a universal claim. No minimality or smallest-radius
optimality is claimed, and no blank-padded symmetry conclusion is asserted.

Together with the unbounded degree-three two-leg family, this changes the
next general research question: enlarging local corner patterns to ALL
immediate neighboring tiles still does not suffice. A general compensation
proof must either transport original physical deficit across intervening
tiles, or use a stronger objective-preserving normalization. The allocation
must reserve each donor capacity globally across all components. A universal
bound on transport distance remains unproved, as do the full grid bound and
triple equality.

## 6. The obstruction persists with every endpoint in the interior

Translate the entire original configuration by (2,2) into a 12-by-14
rectangle, preserve every label in the original subrectangle, and add only
the selected sites displayed outside it below. The matching is exactly the
translated original matching. All unmarked sites are blank.

```text
..T.TT.TT.TT.T
...T..T..T..T.
T.T.TPPPPPPT.T
.T.T.PPPPPP.T.
T.TPPPP.T.PT.T
.T.PPPPT.TP.T.
T.TP.T..T.PT.T
.T.PT.TT.TP.T.
T.TP.T..T.PT.T
.T.T.T..T.T.T.
T.T......T.T.T
T.T.TT..T.T..T
```

There are 65 selections and the same 28 endpoints and 14 matching edges.
Every endpoint is at least two grid edges from the boundary. Feasibility
can be checked directly from the displayed labels; no selected vertex has
more than one occupied neighbor. All original retained witnesses remain,
so the identical ordered freezing proof translates unchanged. The receiver
inventory and corrected charge remain 12 tiles, 11 selections, nine blanks
and rho=1.

Every endpoint-free tile at edge-or-corner distance one from the translated
receiver still contains exactly two selections. Thus its entire immediate
neighborhood has capacity zero. The closest positive deficit tiles have
tile distance two. The full outside deficit is six and the objective is
65+14=79, below half-area 84, leaving deficit five. The added selections
change the border, so this is a selected-border completion, not a claim
that an unchanged blank border preserves neighboring capacities.

The precise larger selected set, matching and translation are included in
the JSON field interior_extension. The independent checker verifies all
eight physical images, preservation of the original labels, the shifted
28-step certificate, the original corrected ledger and zero neighboring
capacity. This establishes that having endpoint vertices on the ambient
boundary is not necessary for the neighboring-resource obstruction.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
