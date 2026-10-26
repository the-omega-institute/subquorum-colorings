# Basic mate coverage still leaves a bulk gap in connected bands

26 October2026. Wenlin Zhang and Haobo Ma. Strengthening of
[the connected-band relaxation barrier](SUCCESSOR_GUARD_COMPENSATION_AND_CONNECTED_CUT_BARRIER.md).

The previous36-scaled periodic point is excluded by the elementary necessary
matching inequalities p_v<=b_v+sum_(u adjacent v)p_u, where p=o-t and b_v
counts old-P0 neighbours. We now show that adding **every** such inequality
still does not repair that local relaxation. This is a second rational point,
not a claim that the original point satisfies mate coverage.

Use the same17m-4-site connected C_m, m>=2, and the same bounds, anchors,
wedges, full selected-degree inequalities, bottom-star cuts and four contained
module-window cuts. Add all the displayed basic mate-coverage inequalities.

Assign the following scaled values by row and column modulo6:

| Phase | 92t | 92o |
| --- | --- | --- |
| (2,3) | 92 | 92 |
| (2,5) | 0 | 92 |
| (3,3) | 0 | 67 |
| (3,4) | 56 | 92 |
| (3,5) | 0 | 61 |
| (4,0) | 36 | 54 |
| (4,1) | 38 | 56 |
| (4,2) | 36 | 54 |
| (4,3) | 47 | 56 |
| (4,4) | 36 | 36 |
| (4,5) | 53 | 56 |
| (5,0) | 55 | 56 |
| (5,1) | 54 | 54 |
| (5,2) | 49 | 56 |
| (5,3) | 54 | 70 |
| (5,4) | 56 | 56 |
| (5,5) | 54 | 58 |

At the single bottom-right site v=(5,6m+5), reduce o_v from58/92 to54/92,
so that o_v=t_v. All other values use the table.

**Proposition.** This point satisfies the complete strengthened real
relaxation at every m>=2, and

    Q(C_m)=(891m-204)/46,
    Q(C_m)-(18m-2)=(63m-112)/46>0.

**Proof.** Substitute the table into the17 periodic vertex types, including
the mate-coverage inequalities, and four module windows. All inequalities
hold with rational arithmetic. This finite list of substitutions checks
explicit inequalities, not an enumeration of grid configurations.

Truncation has the same five boundary types as before. At (3,6m+5),
(4,8),(4,6m+4), the full-degree slacks are0; at the two bottom ends the
slacks are9/23. The unpatched bottom-right site has no available endpoint
neighbour, which is why its p is set to0. The other bottom end already has
p=0. The two boundary sites with positive old-P0 counts have their basic
mate inequality automatically, since p<=1<=b; the remaining boundary
row4 site has p=0. Reducing bottom-right o only makes bounds, neighbour
occupation, star and window inequalities easier. Its only surviving
neighbour is (5,6m+4), which also has p=0, so that neighbour's mate
inequality survives the reduction. Thus the five boundary types and this
one neighbour cover every changed constraint. All other instances are
periodic or lose nonnegative terms. This proves validity at every length.

One period has charge891/46. The four omitted phases (4,0),(4,1),(4,5),
(5,0) have total101/23. The single endpoint reduction costs1/23. Therefore

    Q(C_m)=891m/46-101/23-1/23=(891m-204)/46.

Subtract18m-2 to get the displayed positive gap. In fact the bulk slope
891/46 is greater than18, so no bound18m+B with fixed boundary constant B
holds throughout this strengthened relaxation. The natural corrected
candidate18m-1 is also exceeded for m>=3. QED.

This point is not asserted to come from fractional matching-edge variables:
vertexwise mate coverage does not impose simultaneous capacity on shared
mate sites or matching edges. Nor is it an integer occupation or completely
frozen example. The separate actual6-by-22 integer counterexample in the
companion note still only refutes the isolated non-frozen permissions cut.
The full matching-edge system, integrality, actual freezing and the
C_m/pocket joint boundary bound remain the next questions.

The standard-library checker verifies all periodic and boundary constraints
exactly and controls18 actual coordinate domains through m=128. The general
proof is the substitutions, explicit boundary patch and linear charge formula.
There are6,054 exact vertex checks, each including local mate coverage.
Lean4.33.0 checks four further declarations: all scaled periodic/window
inequalities, the six changed boundary/neighbour cases, the period/omission/
patch counts, and the positive gap at every m>=2. The first three are
axiom-free kernel computations; the arithmetic theorem uses only the
standard axioms. No sorry, native_decide or new axioms. The all-length
coordinate-to-boundary reduction remains a written proof with Python controls.
This strengthening was obtained after dispatch of the companion note's
Oracle review and is outside that review's scope.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_connected_band_mate_coverage_barrier.py --output output/connected-band-mate-coverage-barrier-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_connected_band_mate_coverage_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/connected-band-mate-coverage-barrier-formal-validation.json

A subsequent [simultaneous-edge construction](CONNECTED_BAND_SIMULTANEOUS_MATCHING_BARRIER.md) gives an exact terminal Hall obstruction to this particular92-scaled point, but a different80-scaled all-length point satisfies the entire matching-edge system and violates the specified whole-board fractional bound for m>=18. This strengthens the relaxation barrier; integer and freezing-aware bounds remain open.
