# Uniform twelve-thirteenths bound for complete U/rotor fusions

The later CHARGE_AWARE_COMPLETE_SOURCE_COEFFICIENT.md strengthens these
constants to14/15 and21/22 by counting original marked-side owners' matchings;
its original G/S notation error is corrected there. The newer
MARKED_SIDE_MATCHING_BUDGET.md further gives33/35 and26/27.
The proof below remains a valid earlier deduction.

20 October 2026. The accepted two-slot compensation theorem implies a
uniform matching coefficient12/13 for the entire permitted finite
complete-source model, with no bound on the number, dimensions, phases
or contact graph of its U/rotor sources. If every positive U dimension
is nonexceptional, the coefficient improves to17/18. These are deductions
from the established compensation theorem, not claims of sharpness.
The coefficient-one allocation and arbitrary-grid triple equality remain open.

## 1. Exact assumptions and conclusions

Use the complete-source assumptions of
TWO_SLOT_COMPENSATION_FOR_UNACTIVATED_DOUBLES.md: U(w,a,b) has even
w>=6 and independent even a,b>=4; arbitrary isometries, translations
and rotor phases are allowed. Original endpoint sets are disjoint,
P and M are their unchanged unions, all original supports outside P
are retained, and every finally selected vertex has occupied degree
at most one. The ambient even-by-even rectangle and any optional
selections satisfy the same source-ledger assumptions. In particular

    sigma=mn/2-|T|-|M| >= n0-e-floor(s/2).

Here e counts actual exceptional DOUBLE-MARKED positive sources;
s counts nonexceptional double-marked positives with exactly one
activated terminal, and n0 counts unmarked positives. Nonexceptional
dimensions are w=6 at arbitrary permitted heights, or w in{8,10}
with a,b in{4,6}. Other source classes have no new restriction.

**Uniform complete-source theorem.** Under those hypotheses,

    |T|+(12/13)|M| <= mn/2.                         (1)

If all positive U sources have nonexceptional dimensions, then

    |T|+(17/18)|M| <= mn/2.                         (2)

Relative to the5/6 coefficient on the same configurations, the gains
are7|M|/78 and|M|/9, respectively. This does not extend the uniform
arbitrary-grid5/6 theorem: no decomposition of arbitrary boundary
objects into these complete sources has been proved.

## 2. Matching cost of the remaining losses

The original U constructor has w/2 matching edges in its upper bar,
w/2-1 in its lower interior bar, and a/2+b/2 on its two legs. Hence

    m(w,a,b)=w+(a+b)/2-1 >=9.                       (3)

An exceptional positive has w!=6 and either w>=12 or max(a,b)>=8.
If w>=12, (3) gives m>=15. Otherwise w is8 or10 and one height is
at least8, so m>=8+(8+4)/2-1=13. Thus every source counted by e
has at least13 original matching edges; every source counted by s
has at least9. These two source lists are disjoint. Since original
endpoint sets are disjoint and matching ownership is unchanged,

    |M| >=13e+9s >=13(e+floor(s/2)).                (4)

This is a matching-size budget. No defect slot, activation, full-tile
credit or support-chain resource is spent again. In particular, (4)
does not assert any new injection from a loss to a defect tile.

## 3. Proof of the two coefficients

By the accepted compensation theorem and n0>=0,

    sigma >=-e-floor(s/2) >=-|M|/13.

Substitute the definition of sigma and move |M|/13 to the other
side to obtain (1). Equivalently, the integer form is

    26|T|+24|M| <=13mn.

When e=0, the stronger matching budget |M|>=9s>=18floor(s/2)
gives sigma>=-|M|/18, proving (2), or

    36|T|+34|M| <=18mn.

Every inequality holds for arbitrary finite source counts and all
permitted dimensions. Finite controls are supplementary. The improved
paid-single and J/X bounds can further improve an individual instance;
they are not needed for these uniform constants.

## 4. Verification scope and next question

formal/SubQuorum/CompleteSourceCoefficient.lean checks seven arithmetic
declarations: the two constructor-size lower bounds, matching payment,
the two scaled slack bounds, and the two integer boundary conversions.
The physical constructor count, source partition and accepted geometric
compensation theorem are written dependencies, not an end-to-end Lean
formalization of arbitrary physical fusions.

All seven declarations pass local Lean4.33.0 compilation, object build
and individual axiom audits, with only propext and Quot.sound and no
sorry or native_decide. See output/complete-source-coefficient-formal-check.json.
The constructor controls check2548 dimension triples, including2344
exceptional triples, and attain the respective minima9 and13. All35937
universal budget cases and1089 nonexceptional cases pass. These controls
add no new complete physical-fusion fixture coverage. Reproduce with:

```sh
python3 develop/check_complete_source_coefficient.py --output output/complete-source-coefficient-controls.json
```

The remaining central problem is still to prove coefficient one by
excluding the coupled full-chain obstruction, or to exhibit a complete
feasible allocation obstruction. A negative sufficient margin mu would
not by itself refute the ambient inequality sigma>=0. These constants
provide quantitative progress without resolving that obstruction.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
