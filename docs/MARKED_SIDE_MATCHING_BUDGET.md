# Marked-side matching budgets and stronger complete-source coefficients

20 October 2026. The source ledger uses G for marked positive sides, not
negative original charge. Keeping this distinction gives a direct matching
budget from the existing single-use side assignment. It repairs the bridge
in CHARGE_AWARE_COMPLETE_SOURCE_COEFFICIENT.md and strengthens its conclusions
to33/35 for all permitted complete-source fusions and26/27 when actual
double-marked positives are nonexceptional. General coefficient one and
rectangular-grid triple equality remain OPEN.

## 1. Exact scope and notation correction

Retain the finite complete U/rotor model, original disjoint endpoint sets,
unchanged matchings, retained supports, fixed physical aligned partition,
final selected occupied degree<=1, optional-selection restrictions and
even-by-even ambient/source-ledger assumptions of
ALL_PHASE_JOINT_COMPENSATION_SLOTS.md. Widths and independent heights are
legal arbitrary even integers w>=6,a,b>=4. All phases, translations and
isometries and arbitrary finite contact graphs are allowed.

The notation is

    S = total absolute original negative source charge,
    G = number of marked original canonical positive sides,
    R = S+C-Kirregular >=0,
    mu=N+R-G,  sigma=mn/2-|T|-|M|>=mu.

In particular G and S are different counts. The prior charge-aware note
incorrectly called G the negative charge and used the true charge-cost
bound to justify the marked-side budget. That implication did not follow.
Its Lean arithmetic accepted an explicitly supplied budget/ledger bridge;
the old finite aggregate controls also assumed that bridge. Neither
established the physical identification. The previous Oracle acceptance
must therefore be read as conditional on those supplied inputs. This
note replaces the missing bridge; it does not rely on G=S. The existing
complete opposed-band width6 fixture already has N=1,S=5,G=2 and22
matching edges, directly demonstrating that the two counts differ.

Keep the accepted actual-count compensation inequalities

    N>=e+s,  mu>=n0-e-floor(s/2),  n0>=0,
    2R=A+U0+Z0+H,  A>=s.

Here e counts actual exceptional double-marked positive sources and s
counts actual nonexceptional doubles with one activated terminal.
Nonexceptional means w6 with arbitrary legal heights or w8/10 with
both heights4/6. The condition e=0 restricts actual doubles only; other
positive dimensions remain unrestricted. No sharpness is asserted.

## 2. A marked side consumes one original endpoint slot

Use the original physical side assignment proved in Section3 of
ALL_PHASE_JOINT_COMPENSATION_SLOTS.md. Distinct original positive donor
tiles are disjoint. Each marked side is assigned an original endpoint
inside its own donor tile; hence assignments are injective even when a
single foreign original source witnesses several sides. Complete rotor
gate and blank-gate barriers exclude every rotor owner. Positive U images
have no eligible endpoint roles. For a negative U, the complete boundary
catalogue gives the following eligible marked-side endpoints:

| Original effective phase | Eligible original endpoints | Capacity |
|---|---|---:|
| 01 | two upper bar corners | 2 |
| 10 | two terminal tips | 2 |
| 11 | two upper bar corners and two terminal tips | 4 |

This table counts MARK assignments only. The larger joint pool including
irregular-event tails is not the table's capacity. A phase11 upper corner
can supply a marked-side slot only when its own event does not fire, but
we need only the stated upper bound on the total number of marks.

Let B=B01+B10+B11 be the number of original negative U sources and let
Mneg be the total number of their original matching edges. Injectivity
and the table give

    G<=2B01+2B10+4B11<=4B.

Every complete U has matching size w+(a+b)/2-1>=9. Original matching
ownership is disjoint, so Mneg>=9B. Consequently

    9G<=4Mneg.                                    (1)

This is a genuine matching-size budget, not an allocation of fresh
geometric defect units. One source's matching is summed ONCE irrespective
of how many sides it witnesses; each assigned side is counted ONCE by
the original-endpoint injection. No U0,H,X,A or full-tile resource is
spent again. No assigned marked-side endpoint is rotor-owned; rotor
matching edges can be left in the nonnegative unused remainder.

## 3. Combine the positive and marked-side budgets

Positive original matchings cost at least9N+4e, since all positives cost
at least9 and each exceptional double costs at least13. Those matchings
and Mneg are disjoint. Equation(1) therefore gives

    4|M|>=36N+16e+9G
          =45N+16e+9R-9mu.                        (2)

In particular Mneg>=G, so the weaker original budget

    |M|>=9N+4e+G=10N+4e+R-mu

is valid by this NEW marked-side proof. Thus the previous14/15 and21/22
conclusions survive the notation correction. Negative charge S remains
in R=S+C-Kirregular and is not substituted for G anywhere.

## 4. Universal coefficient thirty-three-thirty-fifths

If mu>=0, sigma>=0 already gives coefficient one for that instance.
Otherwise put ell=-mu>0. Accepted compensation yields

    ell<=e+floor(s/2)<=e+s/2.

Use N>=e+s and R>=0 in(2):

    4|M|>=61e+45s+9R+9ell
           >=61(e+s/2)+9ell
           >=70ell.

Hence sigma>=mu>=-2|M|/35, and

    |T|+(33/35)|M|<=mn/2.                         (3)

The exact integer form is70|T|+66|M|<=35mn. Relative to5/6 on the
SAME complete-source configurations the improvement is23|M|/210;
relative to14/15 it is |M|/105. This does not improve a universal
arbitrary-grid theorem without the missing grid/source bridge.

## 5. Nonexceptional coefficient twenty-six-twenty-sevenths

If e=0 and mu=-ell<0, compensation gives s>=2ell. Also
2R>=A>=s, so R>=ell. Equation(2) gives

    4|M|>=45N+9R+9ell>=90ell+9ell+9ell=108ell.

Thus sigma>=-|M|/27, or

    |T|+(26/27)|M|<=mn/2.                         (4)

The exact integer form is54|T|+52|M|<=27mn. Its gain over5/6 is
7|M|/54 and over21/22 is5|M|/594, under the stated class restriction.

## 6. Verification boundaries and remaining objective

The assignment, original boundary-role table, original matching partition
and exact physical ledger are written dependencies. New universal Lean
declarations check arithmetic consequences of the supplied phase capacities,
including 9G<=4Mneg, the combined budget, signed
margin deductions and exact integer coefficients. These are not an
end-to-end formalization of arbitrary physical source fusions.

Source-image and actual complete-fusion controls reconstruct the marked
assignment and count each original owner's matching once. In particular
they keep the original negative charge S separate from marked-side G.
Finite counts supplement the written general proof. All ten new scoped
Lean4.33.0 declarations compile/build and pass individual axiom audits
using only propext and Quot.sound, on the user-selected local Mac.
The older13-declaration source also compiles after renaming the misleading
negativeCharge parameter to markedSides; its propositions are unchanged.
Controls pass896 original U images,192 existing complete-fusion images
(32 marked),57199 signed budgets (23580 negative margins), and4093
nonexceptional budgets. All192 physical controls distinguish G from S.
No new complete AA fixture is claimed. See
output/marked-side-matching-budget-formal-check.json and
output/marked-side-matching-budget-controls.json. Independent audit
f8df3fbb completed ACCEPT at2026-10-20T06:35:51.861UTC, observed gpt_6/pro,
19988characters. Original stream15195 exits0/DONE and exactly matches the
same task's terminal response. The audit reconstructs the physical mark
injection, source-only2/2/4 capacities, source-level matching nonreuse and
both coefficients. It treats the established complete rotor barriers and
support catalogue as identified geometric dependencies; it does not
independently rerun their omitted role enumeration or certify executions.
Its refinements about supplied Lean premises and rotor-owned assignments
are incorporated here. See output/marked-side-matching-budget-review.json.

This quantitative step does not resolve the two width-six negative-source
boundary routes or exclude a complete finite cycle. Continue those routes
with original ownership and no repeated payments, and preserve the
distinction between allocation margin mu and actual ambient slack sigma.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
