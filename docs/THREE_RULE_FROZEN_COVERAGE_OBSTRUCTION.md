# All three local corner rules can miss a fully frozen positive receiver

20 October 2026. An explicit8-by10configuration has a complete fully frozen
receiver of corrected charge1, but zero capacity from capped corners,
selected-guarded corners AND the new same-component two-endpoint guards.
All three conditional deficit and ownership theorems remain valid; their
universal coverage fails. This is an obstacle to a purely corner-based
proof, not to the global coefficient-one grid inequality.

The first two-rule obstruction in
CORNER_FREE_FROZEN_RECEIVER_AND_ENDPOINT_GUARDS.md has occupied degree3and
is repaired by the third rule. The present independent construction has
four occupied-degree4endpoints, including one geometric four-way P junction.
It explains why the local repair must not be promoted to a general solution.

## 1. Physical specification and complete freezing proof

Use {0,...,7} x {0,...,9} with nearest-neighbor edges and original aligned
2-by2tiles. All unlisted vertices are blank. Take

    T={(2,0),(4,0),(6,0),(1,1),(7,1),(5,2),(4,3),(5,4),(7,6),(1,7),(4,7),(6,7),(3,8),(2,9)}.

The eleven actual matching edges are:

    (2,1)--(2,2)
    (2,3)--(2,4)
    (2,5)--(2,6)
    (2,7)--(2,8)
    (3,2)--(3,3)
    (3,4)--(3,5)
    (3,1)--(4,1)
    (3,6)--(4,6)
    (4,5)--(5,5)
    (5,1)--(6,1)
    (5,6)--(6,6)

They cover22distinct endpoints. There are no T--T edges, and every selected
vertex has exactly one occupied neighbor. The complete2-column rectangle
{2,3} x {1,...,6} is connected. The horizontal upper arm, lower band and
vertical tail attach to it, so P is a single complete endpoint component H.

Write m for the actual mate. Every following row lists two distinct adjacent
witnesses other than the row's own mate. Each is selected or the mate of
an earlier endpoint:

| Step i | Endpoint v_i | First witness | Second witness |
| --- | --- | --- | --- |
| 1 | (2,1) | (1,1) in T | (2,0) in T |
| 2 | (2,8) | (2,9) in T | (3,8) in T |
| 3 | (6,1) | (6,0) in T | (7,1) in T |
| 4 | (6,6) | (6,7) in T | (7,6) in T |
| 5 | (4,1) | (4,0) in T | (5,1) = m(v3) |
| 6 | (4,6) | (4,7) in T | (5,6) = m(v4) |
| 7 | (5,5) | (5,4) in T | (5,6) = m(v4) |
| 8 | (2,6) | (2,7) = m(v2) | (3,6) = m(v6) |
| 9 | (3,2) | (2,2) = m(v1) | (3,1) = m(v5) |
| 10 | (3,5) | (2,5) = m(v8) | (3,6) = m(v6) |
| 11 | (2,3) | (2,2) = m(v1) | (3,3) = m(v9) |
| 12 | (2,4) | (2,5) = m(v8) | (3,4) = m(v10) |
| 13 | (3,3) | (2,3) = m(v12) | (3,4) = m(v10) |
| 14 | (3,4) | (2,4) = m(v11) | (3,3) = m(v9) |
| 15 | (2,2) | (2,3) = m(v12) | (3,2) = m(v13) |
| 16 | (2,5) | (2,4) = m(v11) | (3,5) = m(v14) |
| 17 | (2,7) | (1,7) in T | (2,6) = m(v16) |
| 18 | (3,1) | (2,1) = m(v15) | (3,2) = m(v13) |
| 19 | (3,6) | (2,6) = m(v16) | (3,5) = m(v14) |
| 20 | (4,5) | (3,5) = m(v14) | (4,6) = m(v19) |
| 21 | (5,1) | (4,1) = m(v18) | (5,2) in T |
| 22 | (5,6) | (4,6) = m(v19) | (5,5) = m(v20) |

All22endpoints occur once. The two witnesses and actual mate also show
single terminality directly. If a nonempty bundle promoted endpoints in
any checkerboard orientations, its first promoted row would retain both
witnesses: original selections remain, and deleting m(v_j) would require
promoting an earlier v_j. This contradicts feasibility. The proof covers
arbitrary simultaneous mixed bundles, with no enumeration.

Direct counting gives18endpoints of occupied degree3and4of occupied
degree4. The geometric junction set {p:deg_P(p)=4} is exactly {(3,5)}.
The full JSON instance is develop/three_rule_frozen_obstruction.json.

## 2. The original corrected receiver charge is one

The receiver has10physical tiles,10selections and8blanks. Thus

    rho_H=10+22/2-2*10=(10-8)/2=1.

All three actual saturated-mate transfers are included. The original
corrected graph calculation in the physical checker independently gives
twice-charge2. The whole rectangle has objective14+11=25, half-area40,
outside no-endpoint deficit16and total deficit15:

    40-25=16-1.

There is ample global deficit; the local rules fail to recognize a
sufficient owned resource. The construction does not refute the global
grid target or the proposed triple equality.

## 3. Exhaust every capped-corner orientation

A capped witness must have an extended exterior side of four consecutive
endpoints, with the central pair aligned with one physical tile side. The
maximal endpoint runs of length at least four are exactly:

- first coordinate2, second coordinates1through8;
- first coordinate3, second coordinates1through6;
- second coordinate1, first coordinates2through6;
- second coordinate5, first coordinates2through5;
- second coordinate6, first coordinates2through6.

Matching these runs to the original physical parity gives only the five
candidate tiles below. For each extended side there are two possible
tip/support orientations. Here P,T,B are the actual endpoint, selected
and blank labels; a valid cap requires the ordered pair (P,T).

| Physical tile | All possible tip/support label pairs |
| --- | --- |
| (0,1) | (T,B), (B,B) |
| (0,2) | (B,B), (B,B) |
| (0,3) | (B,B), (B,B) |
| (2,1) | (P,P), (B,T), (P,P), (B,B) |
| (2,2) | (T,B), (P,P), (P,P), (B,B) |

There are14candidate orientations and none has (P,T). They already fail
before imposing the other non-endpoint-corner conditions. No other extended
side is physically aligned, so this excludes every capped witness.

## 4. Exhaust both selected-corner guard rules

Both selected-guarded and two-endpoint-guarded witnesses require a selected
corner x whose unique occupied neighbor lies outside its physical tile in
H. The complete list of eligible selections is the following four. For
their opposite corners z, list all exterior neighbors, treating sites
outside the rectangle as blank; such outside sites cannot be witnesses.

| x | Opposite corner z | First exterior neighbor of z | Second exterior neighbor of z |
| --- | --- | --- | --- |
| (1,1) | (0,0) | (-1,0), outside | (0,-1), outside |
| (1,7) | (0,6) | (-1,6), outside | (0,5), blank |
| (4,3) | (5,2) | (5,1), endpoint | (6,2), blank |
| (5,2) | (4,3) | (3,3), endpoint | (4,4), blank |

There is no selected exterior guard in any row, and no row has two exterior
endpoint guards. Therefore neither guard rule applies, even before the
same-component restriction of the new rule is considered. Together with
Section3, the union of all three donor sets is empty.

Translating everything by(2,2)inside a12-by14blank rectangle preserves
physical phase, all certificates and the absence of all three rules.
The new border contains no selections or endpoints to make a missing
witness; the listed outside sites simply become ordinary blanks. All eight
padded symmetry images are independently checked.

## 5. Verification, provenance and implications

Run the standard-library checker:

    python3 -B develop/check_three_rule_obstruction.py --output output/three-rule-obstruction-controls.json

It checks the complete actual matching, selected feasibility, connectedness,
all22ordered freezing rows, an independently computed freezing closure,
original corrected receiver charge, all14extended-side orientations, and
absence of all three guard/cap rules. All8physical symmetries and8blank-
padded symmetries pass. This second22endpoint example is not newly Lean
formalized. The35local Lean declarations in the preceding milestone cover
the first20endpoint obstruction and the general normalized guard lemma;
their scope is not extended to this example by association.

The construction came from the original follow-up Oracle question
70a39946-4663-49b8-8ae0-48b1fd1454fd. It completed on19October at
17:35:48UTC, observed model gpt_6 with effort pro. The original streamed
answer matches the terminal server response exactly; see
output/weighted-owned-coverage-review-response.json. That question specified
the two old rules. The answer's counterexample was independently verified
and also checked against the third rule, which was not supplied in the
request. Thus the three-rule conclusion is an additional checked deduction,
not a verdict the Oracle supplied on our new ownership proof.

The current distinction is:

- universal receiver charge<=1: false by the earlier charge-two example;
- universal coverage by the two old rules: false even in occupied degree3;
- universal coverage by the enlarged three rules: false in general here;
- the proved conditional weighted compensation criteria: still valid;
- coverage restricted to all occupied-degree3networks: still unresolved;
- the general grid bound and triple equality: still unresolved.

The next proof must account for original physical deficits beyond these
three local witnesses, or use a stronger normalization than endpoint
promotion alone. In a network approach, donor capacity shared by different
routes/components must be reserved globally rather than counted once per
incident route. A valid next result would construct that allocation or
isolate a precise structural condition guaranteeing it; merely adding
another unproved universal corner rule is not justified by these examples.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
