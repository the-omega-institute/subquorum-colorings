# Guarded selected corners and frozen three-column stepped arms

19 October 2026. This extends the capped-corner sufficient class to a new
arbitrary-length family without its four-endpoint-run witness. All counting
uses the original whole-receiver ledger. The submitted manuscript is unchanged.

## 1. A second local donor with an intrinsic owner

Use the feasible-pair conventions of `ELBOW_OWNED_DONORS.md`. In an actual
physical square Q={0,1} x {0,1}, suppose

    x=(0,0) in T, p=(0,-1) in P_H,
    s=(1,2) in T, q=(0,2) in P.                    (1)

The endpoint q need not belong to H. More generally s can be either exterior
neighbor of the corner opposite x and can have any occupied neighbor q other
than that opposite corner. All sites are actual grid sites; rotations and
reflections preserve the physical tiling.

**Guarded-corner lemma.** Q contains exactly x as its occupied site. It is
endpoint-free and has physical deficit d_Q=1.

Proof. The selection x already sees p, so its two neighbors inside Q are
blank. The selection s already sees q, so its neighbor (1,1) in Q is blank.
These are the other three corners of Q. No terminality is needed. QED.

Assign this witness to the complete endpoint component of p, the unique
occupied neighbor of x. This assignment is intrinsic to the labels of Q:
if two guarded witnesses use Q, its sole selection is the same x; feasibility
makes their anchoring endpoint the same p. Hence their owners coincide.

**Compatibility with old capped corners.** A guarded witness and an old
capped-corner witness on the same Q have the same owner, or cannot coexist.

Proof. Normalize the old witness to the north/west orientation of (1) in
`ELBOW_OWNED_DONORS.md`. Its upper-left and lower-left corners are blank,
and it has at most one selection. If its selection is upper-right, that
selection sees the old component's north endpoint. A guarded owner must
therefore use this same unique neighbor and belongs to the old component.
If its selection is lower-right, the opposite upper-left corner can only
have an exterior selected guard to its north or west. Both sites are old
endpoints, so no such guard exists. With no selection the old square cannot
be guarded. This exhausts the cases and all orientations. QED.

Consequently one may choose either kind of witness for each positive receiver
without an extra disjointness assumption. If each has rho_H<=1, the resulting
injection into no-P squares gives

    sum_(rho_H>0) rho_H <= #positive receivers
       <= sum_H d_(Q_H) <= D_all,
    |T|+|M| <= mn/2.                                (2)

This is a genuine mixed-witness statement. It does not follow merely by
adding two independently valid certificates. The preceding cross-type
ownership proof is essential. Channel certificates still need their original
pointwise residual-capacity check after these units have been reserved.

## 2. An arbitrary-length family outside the old witness criterion

Work in relative coordinates with physical tile starts at even rows and odd
columns. Fix k>=1 and b=2k+4. Let the complete endpoint component be

    H_k=({0,1} x {0,1,2,3})
         union ({2,3} x {0,1,2,3,4,5})
         union ({4,...,b} x {0,1,2,5}).             (3)

Thus a four-column top cap joins a six-column chamber, with a three-column
left arm and a one-column right arm. The arm length is 2k+1. The matching
in the first four rows consists of

    (0,0)--(0,1), (0,2)--(0,3), (1,0)--(1,1),
    (1,2)--(2,2), (1,3)--(2,3), (2,0)--(2,1),
    (2,4)--(2,5), (3,1)--(3,2), (3,3)--(3,4),
    (3,0)--(4,0), (3,5)--(4,5).

For r=4,6,...,b-2 add

    (r,1)--(r+1,1), (r,2)--(r+1,2),
    (r+1,0)--(r+2,0), (r+1,5)--(r+2,5),

and finish with (b,1)--(b,2). These edges partition H_k. Retain

    (-1,1),(0,-1),(0,4),(2,-1),(2,6),
    (b,3),(b+1,0),(b+1,2),(b+1,5),
    (r,-1),(r,6),  r=4,6,...,b,
    (r,4),         r=5,7,...,b-1.                   (4)

All other sites are blank in the baseline. Each selection sees exactly one
named endpoint. Selections are pairwise nonadjacent, including at k=1.
Every endpoint has occupied degree at least three. These claims follow
directly along the filled cap/chamber and arms; the three bottom corners
have their two distinct selected supports. This proves feasibility and
single-terminality for every k. The construction fits, after translation
by (4,3), inside the even rectangle (2k+12)-by-12.

More generally keep H_k complete, its matching and all supports (4) in any
feasible exterior completion. The following freezing and receiver claims
remain true. No foreign endpoint can join H_k under completeness.

## 3. A complete all-length freezing proof

Write m for the actual matching involution. A frozen endpoint z guarantees
that m(z) stays occupied in every proposed simultaneous promotion bundle.
Two distinct retained neighbors therefore freeze an endpoint.

First freeze (b,0),(b,2),(b,5), using their two selected neighbors. Descend
through even r=b-2,b-4,...,4 in columns 0 and 5. The outer selected support
and m(r+2,c)=(r+1,c) freeze (r,c). The same argument freezes (2,0),(2,5),
using the selected lateral supports and the mates (3,0),(3,5) of (4,0),(4,5).

Next descend through odd r=b-1,b-3,...,5 in the middle column 1. Its left
neighbor (r,0)=m(r+1,0) is retained. At r=b-1 its lower neighbor is
(b,1)=m(b,2). At subsequent r the lower neighbor (r+1,1) is m(r+2,1),
whose odd endpoint was already frozen. Thus all these odd middle endpoints
freeze. Now (3,1) sees m(4,0)=(3,0) and m(5,1)=(4,1), and freezes.

The following finite cap order lists two retained neighbors for each next
endpoint. T denotes a prescribed selection; every m-argument has already
been frozen by the preceding waves or an earlier row of this table.

| Endpoint | First retained neighbor | Second retained neighbor |
| --- | --- | --- |
| (2,2) | m(2,0)=(2,1) | m(3,1)=(3,2) |
| (3,4) | m(2,5)=(2,4) | m(4,5)=(3,5) |
| (1,1) | m(2,2)=(1,2) | m(2,0)=(2,1) |
| (2,3) | m(2,5)=(2,4) | m(3,4)=(3,3) |
| (0,0) | T(0,-1) | m(1,1)=(1,0) |
| (0,3) | T(0,4) | m(2,3)=(1,3) |
| (0,1) | T(-1,1) | m(0,3)=(0,2) |
| (0,2) | m(0,0)=(0,1) | m(2,2)=(1,2) |
| (1,2) | m(0,3)=(0,2) | m(2,3)=(1,3) |
| (1,3) | m(0,2)=(0,3) | m(2,2)=(1,2) |
| (3,2) | m(1,2)=(2,2) | m(3,4)=(3,3) |
| (2,1) | m(1,2)=(2,2) | m(3,2)=(3,1) |
| (3,3) | m(1,3)=(2,3) | m(3,1)=(3,2) |
| (1,0) | m(0,1)=(0,0) | m(2,1)=(2,0) |
| (2,4) | m(1,3)=(2,3) | m(3,3)=(3,4) |
| (3,0) | m(2,1)=(2,0) | m(3,2)=(3,1) |
| (3,5) | m(2,4)=(2,5) | m(3,3)=(3,4) |

Freeze even endpoints in column 2 of the thick left arm, r=4,6,...,b-2.
For r=4 the upper neighbor (3,2)=m(3,1) is retained; thereafter the upper
neighbor is m(r-2,2)=(r-1,2). The same-row neighbor (r,1)=m(r+1,1)
is retained from the odd middle-column wave. This freezes every even (r,2).

For even r=4,6,...,b-2, successively freeze (r,1) and (r+1,0).
At r=4, (r,1) sees m(3,0)=(4,0) and m(3,2)=(3,1).
At larger r it sees m(r-1,0)=(r,0) and m(r-2,1)=(r-1,1).
Then (r+1,0) sees m(r-1,0)=(r,0) and m(r,1)=(r+1,1),
with the first m-argument replaced by (3,0) at r=4. Freeze (b,1) using
m(b-1,0)=(b,0) and m(b-2,1)=(b-1,1).

Finally descend through odd r=b-1,b-3,...,5 in column 2. The same-row
middle neighbor is m(r-1,1)=(r,1). The lower neighbor is m(b,1)=(b,2)
at the first step and m(r+2,2)=(r+1,2) thereafter. Freeze the odd thin-arm
endpoints (r,5), r=5,7,...,b-1, upward from the chamber, using their inside
selection (r,4) and retained upper neighbor m(3,5)=(4,5), then m(r-2,5).
These waves exhaust H_k, including k=1. Every listed pair is distinct and
grid-adjacent. This proves full freezing for arbitrary k and feasible exterior.

## 4. Exact receiver charge, absent old witness, and actual payment

Every receiver corner not prescribed as an endpoint in (3) or as a selection
in (4) is forced blank by a prescribed selection already incident to P.
Thus arbitrary feasible exterior data cannot change the following complete
receiver labels and counts. Prescribed selections remain occupied.

| Receiver part | Physical tiles | Endpoints | Selections |
| --- | --- | --- | --- |
| Rows 0,1 | 3 | 8 | 2 |
| Rows 2,3 | 4 | 12 | 2 |
| k full arm bands | 3k | 8k | 2k |
| Bottom band b,b+1 | 3 | 4 | 5 |
| Total | 3k+10 | 8k+24 | 2k+9 |

Hence the original corrected receiver charge is exactly

    rho_H=(2k+9)+(4k+12)-2(3k+10)=1.                (5)

There is no old capped-corner witness for this H_k. Here is a direct
boundary check independent of any cutoff in k. A horizontal extended run
of four endpoints can occur only in rows 0,1,2,3. For the physical squares
adjacent to these runs, either the excluded near corners are themselves
endpoints, there is no short tip, or the two candidate short-tip supports
at the row-3/row-4 transition are endpoints in row 5. The last alternative
uses k>=1. Lower arm rows have no horizontal run of four. For vertical full
runs, the relevant columns are 0,1,2,3,5. Columns 0,1,3 force near-square
endpoints. Columns 2 and 5 can face the gap at the row-3 transition, but
their candidate short tips in row 3 have their next support in that same
filled row, so it is P rather than T. Farther down these columns there is
no sideways short tip. These exhaust both ends and all four full-side
directions, hence all eight old orientations.

The different physical tile

    Q_k={b,b+1} x {3,4}                            (6)

has the guarded witness x=(b,3), p=(b,2), s=(b+1,5), q=(b,5).
It has exactly one selection and three forced blanks, so d_(Q_k)=1.
The receiver's positive unit is therefore paid exactly, with no channel,
endpoint-free-final-band or extra phase assumption. This is a different
local mechanism from the four-endpoint-run corner used earlier.

Combining Sections 1–4 proves coefficient one for every terminal configuration
whose positive receivers are prescribed old elbows, these stepped-arm
components, or other charge-at-most-one components possessing either complete
witness. All remaining receivers may have arbitrary shape and nonpositive
charge. Distinct donors are proved rather than assumed. Normalization may
be used only when it preserves prescribed frozen data and ends in this class.

The family is an all-length obstruction to claiming that every positive frozen
receiver admits the old capped-corner witness. It is not a counterexample
to the old conditional theorem, the new mixed-witness theorem, or the general
grid target. General positive components and charge greater than one remain open.

## 5. Verification scope

`develop/check_guarded_stepped_arms.py` checks the actual matching, explicit
ordered freezing waves, forced receiver labels, exact charge, absent old
witness, unit donor, all eight directions, and old/new shared-tile attempts.
These are controls for the arbitrary-k proof, not its replacement.
The SMT discovery script records sat, unsat and timeout separately; none of
its finite failures to find an example proves a general upper bound.
Lean checks the local guarded-corner implication, a support-ownership exclusion,
the old lower-corner guard obstruction, and the exact count identity. Complete
all-k geometry and mixed-witness ownership are written proofs.

Executed controls cover k=1,...,16,24,32,64 in all eight directions, 152
physical cases, 576 new/new and 768 old/new shared-donor attempts. All pass,
as do the explicit ordered freezing certificates and forced-label checks.
Sequential local Lean 4.33.0 passes 133 scoped declarations at
2026-10-19T15:09:45.896677+00:00, peak child RSS about 1.12 GB. The four
new declarations have no admitted or compiler-reduction axioms. The formal
receipt is `output/guarded-stepped-arm-formal-check.json`.

Reproduce the physical controls without an SMT dependency:

    python3 develop/check_guarded_stepped_arms.py --output output/guarded-stepped-arm-controls.json

Optional discovery uses a task-local environment with z3-solver 5.3.1:

    python3 -m venv /tmp/subquorum-search
    /tmp/subquorum-search/bin/pip install z3-solver==5.3.1
    /tmp/subquorum-search/bin/python develop/search_corner_coverage.py --rows 12 --columns 12 --exclude-corners --timeout 45 --output /tmp/corner-discovery.json

The search fixes a root endpoint at (3,3), keeps endpoints two sites away
from the ambient boundary, and encodes one connected component, an actual
perfect matching and a strict-rank retained-mate certificate. Every returned
sat witness is independently checked by the existing physical and freezing
verifiers. Unsat means only that specific finite constrained search has no
model; unknown/timeout means no conclusion at all. A fresh run may time out
rather than rediscover the saved model. The proof in Sections 1–4 is independent
of these solver outcomes.

Complete written review a0dc3807-ee9f-4825-b320-d17c57392ef1 completed REVISE
in conv_573957299e557343 at 2026-10-19T15:22:33.672+00:00, observed gpt_6/pro.
It identified the false blanket sentence that every nonendpoint receiver
corner is blank; prescribed selections remain occupied. Section 4 now
excludes both prescribed endpoints and selections from that assertion.
The review found no further substantive gap, but its conditional acceptance
wording is not recorded as a terminal ACCEPT. Exact response and scope are
archived in `docs/reviews/2026-10-19-guarded-stepped-assessment.md` and the
linked response JSON. The companion `STEPPED_ARM_PHASE_AND_CHANNELS.md`
develops new phase tables, charge-aware channels and a translated negative-charge
obstruction; those additions were outside this completed review's input.
The earlier, separate charge-ceiling research request failed with no assistant
output; it produced no mathematical evidence for or against that conjecture.
