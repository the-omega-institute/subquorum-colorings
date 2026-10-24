# Occupied gates activate tips: a mixed coefficient-one theorem

20 October 2026. We connect occupied marked gates to the activated-tip
budget of ACTIVATED_SINGLETON_FLOW_CANCELLATION.md. Every phase10 gate
owner activates the corresponding positive tip, for arbitrary source
dimensions. For width-six positive sources a phase11 gate also activates
the shorter positive tip. This proves the mixed joint allocation when
all positive sources have width six and at most one has unequal legs.
Negative U dimensions, rotor phases and the number of sources remain
unrestricted. The unrestricted positive-width problem stays open.

## 1. Model and exact result

Keep the complete fixed-source model, original ownership, all mandatory
supports, feasibility, and established boundary/marked-side catalogue of
ALL_PHASE_JOINT_COMPENSATION_SLOTS.md. No insertion ordering, receiver
separation, contact graph, freezing or final-degree-three condition is
assumed. Use the singleton-flow theorem

    BU+BR+Aplus+Gb <= 2B11+Lambda,
    2R=2B11-BU-BR+Lambda,
    sigma >= N+R-G,                                 (1)

where R=S+C-Kirregular. This R denotes event reserve, not rotor count.

**Occupied-gate lemma.** If a marked gate is owned by a phase10 U, its
corresponding original positive terminal singleton is activated, for
every positive width and both independent positive heights. If the
positive width is six, an occupied mark on its shorter-leg side is
always activated. Both sides qualify when the legs are equal.

**Width-six mixed theorem.** Suppose every positive U has width six,
and let Uneq count those positive sources whose two heights differ.
All negative sources retain arbitrary permitted widths and independent
heights; all rotor phases are allowed. Then

    Aplus+Gb >= G-Uneq,
    sigma >= N-floor((G+Uneq)/2).                    (2)

In particular the exact sufficient joint allocation

    2G+BU+BR <= 2N+2B11+Lambda                       (3)

holds if Uneq<=1, or more generally if G+Uneq<=2N+1. Thus a single
positive U(6,a,b), with arbitrary independent even a,b>=4 and arbitrary
negative U/rotor sources, satisfies (3). For all equal positive legs,
sigma>=N-floor(G/2)>=0. No equality of negative leg heights is required.
These classes satisfy |T|+|M|<=mn/2, improving the existing 5/6 matching
coefficient by |M|/6. The result is about complete permitted sources;
it is not a decomposition of every rectangular-grid configuration.

## 2. Normalize the positive left side and classify its gate owner

Write the positive source as U(w,a,b), with left stem in column1,
right stem in column w, and bar in rows0,1. Its left gate is u=(2,2).
The original positive endpoints (1,2),(2,1) forbid the gate owner from
having an endpoint predecessor above or left of u. By the established
source-local E catalogue and rotor gate barrier, every occupied gate
owner is either a phase01 upper bar corner or a phase10/11 terminal.
In particular a rotor cannot own it.

At a terminal, let h>=4 be the height of its reference terminal leg,
v>=6 its width and d>=4 its other height. The terminal predecessor is
down or right. The effective phase fixes the perpendicular bar direction:

| Owner | Predecessor from u | Bar extends |
|---|---|---|
| phase10 tip | down | left |
| phase10 tip | right | up |
| phase11 tip | down | right |
| phase11 tip | right | down |

These four forms follow by the signed coordinate permutations of a
reference terminal (h,1) or (h,v), using h even and its paired predecessor
at reference row h-1. The source-local phase catalogue distinguishes
the two row-shifted phases. Their physical endpoint formulas are,
respectively, uEndpoint(v,h,d) at inverse coordinates

    (h+2-r,3-c), (h+2-c,3-r),
    (h+2-r,c-1), (h+2-c,r-1).                       (4)

This covers independent left/right terminal roles by reflecting the
reference U, which exchanges h and d. It is an all-parameter role
normalization, not a finite translation search.

## 3. Every phase10 gate activates its corresponding positive tip

For a down/left terminal the two bar rows are h+1,h+2 and the bar
extends left through column1. If h+1<=a, the endpoint (h+1,1) overlaps
the positive left stem. Thus endpoint disjointness gives h>=a.
The foreign stem in column2 contains every row from2 through h+2,
in particular (a+1,2).

The positive point s=(a+1,1) is an ORIGINAL beyond-tip support, with
original anchor (a,1). Its extra neighbor (a+1,2) persists as a foreign
endpoint. Feasibility therefore forces s into the final P, activating
the original positive terminal singleton. It is foreign ownership of
the original support, not a reclassification into its supporting source.

The right/up alternative is impossible for every w. If h+1<=w, its
bar contains (1,h+1), overlapping the positive upper bar. If h+1>w,
its rightward stem contains (2,w), overlapping the positive right leg.
Its width v>=6 ensures that the upward bar reaches row1. Thus the
down/left alternative is the only feasible phase10 gate role.

Reflection in the positive width exchanges its left/right sides and
a/b. The same argument applies to the right marked side. Distinct
positive sides refer to distinct original terminal occurrences, so
these activations can be counted without duplication.

## 4. Width six eliminates the corner and horizontal phase11 roles

A phase01 upper corner at u has its two own endpoint directions down
and right. Either its bar runs right along row2 or its near leg does.
In the first case that row reaches column v+1>=7; in the second it
reaches column h+2>=6. For w=6 both overlap the positive endpoint(2,6).
The other dimensions of the source do not enter the contradiction.

A right/down phase11 tip has a rightward stem in row2 through column
h+2>=6, so it too overlaps (2,6). Only the down/right phase11 terminal
remains. Its bar rows h+1,h+2 extend through column6. Disjointness from
the positive opposite leg forces h>=b. If the marked left leg is
shorter, a<=b, then h>=a and the same beyond-tip support argument in
Section3 activates its positive terminal.

These arguments include a=b=h=4. The corresponding right-side proof
uses reflection. If a=b, every occupied gate mark has a distinct
activated corresponding tip. If a differs from b, only the longer-leg
side may fail this conclusion; each unequal positive source therefore
contributes at most one exception.

## 5. Count activated sides and close the joint allocation

Separate marks into blank-gate marks (Gb), occupied marks with activated
corresponding positive tips, and remaining occupied marks. By Section4
the last class has at most Uneq members. The association in the middle
class is injective into Aplus, hence

    G <= Gb+Aplus+Uneq.

There is no assertion that every activated tip has a marked side.
Combining with (1) gives 2R>=G-Uneq. Since R is an integer,

    N+R-G >= N-floor((G+Uneq)/2),

which proves (2). If G+Uneq<=2N+1 the right side is nonnegative.
The established two-canonical-sides count gives G<=2N, so Uneq<=1
is an automatic sufficient condition. Equation(1) then yields exactly
(3), rather than only a nonnegative ambient slack from another source.

All budgets retain the original single-use allocation: blank marks
use their previously established local Lambda units, and occupied
marks are assigned to distinct original positive tip occurrences.
No additional use of C or rotor companion routes is made.

## 6. Verification and remaining scope

develop/check_occupied_gate_activation.py checks the complete four-role,
eight-isometry gate normalization for29 incoming dimension triples and
29 positive triples. It obtains348 source-local E candidates and3747
endpoint-disjoint gate comparisons:940 phase10,1532 phase11 and1275
phase01. The width-six survivors are294 phase10 and294 phase11 cases;
all have the asserted downward predecessor and height/activation bounds.
These dimensions provide controls; Sections2-5 give the general proof.

All640 established complete physical images pass the conditional bounds;
72 have at least one positive U and all positive widths six. These
fixtures have no actual phase10 gate or occupied shorter-width-six
gate, so they do not independently exercise those activation branches.
The nonvacuous role controls and the universal coordinate proofs cover
those branches; we do not present incomplete source pairs as feasible
counterexamples or completions.

formal/SubQuorum/OccupiedGateActivation.lean gives universal coordinate
collision, leg clearance and tip-neighbor declarations, original support
inclusion and conditional counting/parity bounds. Gate-role normalization,
source phase adapters, compulsory-support activation and the global
side-to-tip injection remain written; this is not an end-to-end Lean
proof for arbitrary source fusions. Execution evidence is recorded
separately from independent proof review.

All16 new declarations and individual axiom audits PASS locally on the
user-selected Mac with Lean4.33.0, one job and50%/47% free memory before
the final source/audit commands. No sorryAx/native_decide occurs. See
output/occupied-gate-activation-formal-check.json for exact scope and
reproduction. The earlier singleton review failed terminally with
browser infrastructure errors and no mathematical answer; a fresh
combined proof review on original stream28290 completed ACCEPT as broker
task a6ac6319 at 02:12:26 UTC on 20 October. The original stream ended
with EOF; authoritative task retrieval recovered the completed answer
without resubmission. Acceptance covers the written support, collision,
incidence and parity proofs under the supplied source catalogue and
ledger, not execution or end-to-end Lean source adapters. See
output/occupied-gate-compensation-review.json for the full response.

Outside width six, unactivated occupied marks may still have a phase01
upper-corner or phase11 terminal owner. Phase10 no longer contributes
to that residual. With several unequal width-six positive sources the
bound (2) can be negative and supplies no unrestricted solution.
General cap compensation and rectangular-grid equality remain open.

The gate geometry was proposed in exploratory Oracle taskef7e27ea.
This note independently reconstructs its role, support and parity steps.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
