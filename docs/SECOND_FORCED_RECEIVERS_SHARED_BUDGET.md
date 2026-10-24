# Long second forced receivers use the existing shared defect budget

20 October2026. This extends the accepted simultaneous corner/first-stop
budget to the long phase11 second points. It uses one set of actual mixed
three-endpoint tiles; the added terms are not additional reserve to spend.
Critical phase11 second points have a different receiver geometry and are
not charged by this lemma. The unrestricted allocation remains OPEN.

## 1. Setting and exact second receiver

Use the complete finite original-source hypotheses and notation of
[the phase11 theorem](NEUTRAL_PHASE11_CORNER_AND_SECOND_FORCE.md). Keep ALL
actual neutral01 contacts, both open and closed. For each long phase11 exit,
normalize firstz=0, active phase01 predecessor s=N and contact direction d=E.
The second point is y=(-v,0), with v even and active height a>=v+4. It is an
original endpoint, outside its active original owner O.

The physical receiving tile of y is

    Qy={-v-1,-v}x{-1,0}.

O's exact original profile in Qy is the regular pair
{(-v-1,-1),(-v,-1)} and its UNIQUE original support y. The fourth corner is
w=(-v-1,0). The pair description follows directly from O's stem and support
parity, not from an assumption that Qy is a new tile. This is the same type
of original2P1T profile as the first forced receivers, farther up the stem.

If Qy is nonfull, its only final endpoints are O's pair and y. Its missing
corner w neighbors both (-v-1,-1) and y, so w cannot be selected. The tile
is therefore an actual mixed3P0T tile and contributes one unit to H.
Let J11 count these nonfull second receivers. Let J01 retain the preceding
count of nonfull FIRST forced receivers over all neutral01 contacts.

The accepted global injection/separation theorem proves that every first or
long second point is distinct, including contacts in different components.
We next prove these nonfull receiving TILES are distinct as well.

## 2. Nonfull first and second receivers cannot coincide

An original regular pair consists of two adjacent endpoint corners. Suppose
two first/long-second events had the same nonfull physical tile Q. If their
active original owners differed, their original pairs would be disjoint by
endpoint uniqueness. Two disjoint two-point pairs fill all four corners,
contradicting nonfullness. Thus their active owner is the same original O.

For a fixed original phase01 source and physical tile with exact2P1T profile,
the original support coordinate is unique. Both forced points are that
coordinate. The accepted point injection and first/long separation identify
the SAME event, including its first-or-second kind. Hence the map from the
joint nonfull event family to receiving tiles is injective. This proof does
not require any closed-component or AA assumption.

The Lean four-corner lemma proves that two connected original pairs in a
nonfull tile have the same owner. Its generic receiver theorem then derives
event injection from the actual unique original support map and the joint
point injection. In particular these are derived inputs, rather than a
fresh-receiver hypothesis added to the budget.

## 3. Separation from the old corner stops and the single H pool

Retain the established passive-corner partition

    B=D+C0+C1+E1,  C1<=A, E1<=A.

D stops have an original negative phase10 irregular pair. C0 stops have an
original positive phase00 regular pair. Their own individual injections and
mutual separation are part of the accepted passive-corner theorem. Every
J01 or J11 stop instead contains an original phase01 regular pair.

If a J01/J11 tile coincided with a D or C0 tile, their original pair owners
would have different phases and therefore differ. Their two disjoint pairs
would fill the tile, contradicting the nonfullness of the stop. Thus ALL four
families D,C0,J01,J11 are simultaneously distinct actual mixed3P0T tiles.
Each uses one H occurrence. Counting them once gives

    D+C0+J01+J11 <= H,
    B+J01+J11 <= 2*A+H.                                        (1)

No closed-component condition is needed for(1). Optional selections cannot
invalidate the missing-corner argument because two original endpoint anchors
remain occupied. Same-source recurrence at different events is allowed.

The exact reserve identity remains

    2*R=A+U0+Z0+H.

Consequently(1) can be substituted into this EXISTING identity as

    B+J01+J11+U0+Z0 <= 2*R+A.                                 (2)

It is invalid to add J11 as a second payment on top of H or on top of an
older H-based inequality. Equation(2) records the substitution explicitly;
it does not assert any separation from older cap endpoint slots or other
witness families beyond the physical tile classes just proved distinct.

## 4. Closed-turn and zero-defect consequences

For the same source collection, the accepted turn bound and passive subset
give 4*ell+M10<=M01+2*B10 with B10<=B. Substituting(1) yields

    4*ell+M10+2*(J01+J11) <= M01+4*A+2*H.                       (3)

Restricting counts to a chosen union of closed curves requires making the
same restriction in the associated stop counts and source capacities; this
is not an identity about arbitrary open port graphs. The unrestricted stop
budget itself remains valid for ALL contacts.

Within one fixed full endpoint component under the established nonexceptional
AA hypotheses, H=0. The direct shared-pool inequality
D+C0+J01+J11<=H therefore gives D=C0=J01=J11=0. A need not vanish;
B=C1+E1<=2*A remains the available passive-corner bound. Thus every long
second receiver produced inside that component must be full. These receivers are in the same full
endpoint component as their original contact: their active pair lies on the
same connected original phase01 source, and y is adjacent to that pair.
This forces further original endpoints; it does not create extra H reserve.

The nonfull proof above alone does not prove full receiver separation.
The later [four-endpoint argument](FULL_FIRST_AND_LONG_RECEIVER_INJECTION.md)
does establish it for ALL first and LONG second receivers, and extends the
whole-owner exclusion. Critical second points remain outside that receiver
injection and cannot simply be added to its opposite-endpoint count.

## 5. Validation and scope

All seven scoped theorems compile locally with Lean4.33.0 and their axiom
prints pass; the combined25-theorem receipt is
[`phase11-critical-shared-budget-formal-check.json`](../output/phase11-critical-shared-budget-formal-check.json).
The AA formal statement uses the direct H pool, preserving A and B.
Independent review task88c8a838-d1cb-407b-a50f-6ef7ef3f9492 ended with a terminal
typing infrastructure failure and no mathematical verdict. A shorter same-conversation
replacement includes the later full-receiver extension. Local validation does
not imply independent acceptance.

`formal/SubQuorum/NeutralSecondStopBudget.lean` proves the exact nonfull-pair
owner catalogue, receiver injection using original support uniqueness,
separation by different original pair owners, and the shared-budget/reserve/
turn/zero-defect deductions. The physical source profiles and stop-to-H
interpretation are proved in Sections1--4 and use the accepted definitions.

The independent controls check all65 nonfull two-owner corner labelings,
including56 admissible two-pair occurrences, and reconstruct945 original
phase01 regular-pair support profiles and468 second receiving stencils.
These stencils are partial: complete feasible second-stop and AA coverage
remains ZERO. The general packing proof is not inferred from those controls.

This advances the shared reserve analysis for nonfull long exits. Full exits,
critical exits, positive/phase01/rotor continuations and their possible reuse
of existing reservations remain part of the full coefficient-one problem.
Rectangular-grid triple equality and mixed-chain termination remain OPEN.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
