# Saturated two-gate geometry: shared owners and strict clearance

20 October 2026. This note advances the remaining single-positive-source
obstruction from EXACT_GEOMETRIC_EVENT_RESERVE.md. A zero-reserve failure
with positive width at most ten requires a positive leg of height at least
eight. A source owning both bad gates has an exact nested-U normal form
and requires both positive legs to have height at least eight. The argument
allows all permitted negative dimensions and all rotor phases. It is a
necessary-geometry result, not a solution of the unrestricted joint bound.

## 1. Assumptions and conclusions

Keep the complete fixed-source model and all original ownership/support
assumptions. Normalize a positive U(w,a,b) with bar in rows0,1, left leg
in column1 and right leg in column w. Dimensions are even, w>=6,a,b>=4.
The two canonical gates are u=(2,2) and v=(2,w-1). The positive original
left terminal has support s=(a+1,1); the corresponding right support is
(b+1,w). An unactivated terminal leaves all of its original intratile
supports selected.

**Saturated gate theorem.** Suppose R=0. Any unactivated occupied left
gate owner is one of the previously classified phase01 upper-corner or
phase11 terminal roles. Classify the owner as transverse if it occupies
the complete horizontal segment {(2,c):2<=c<=6}; the other possibility
is a phase11 terminal with predecessor down and bar right. For this
remaining longitudinal role, let h be its incident height. Then

    4 <= h <= a-4.                                  (1)

If this positive side is no longer than the opposite side (a<=b), the
incoming width v' also satisfies v'<=w-2. Thus a longitudinal saturated
gate on a shorter/equal side strictly reduces both incident height and
source width.

Reflect the statement for the right side. Two DISTINCT transverse gate
owners can occupy both gates only if w>=12. If ONE source owns both gates,
then w>=8 and it has exactly one of these endpoint/support normal forms:

    upright:  U(w-2,h,k)+(2,1), h<=a-4, k<=b-4;
    inverted: U(w-2,h,h) reflected in rows then shifted by(h+2,1),
              h<=min(a,b)-4.                        (2)

The effective phases of these forms are01 and11 respectively. In both
forms a,b>=8. No assumption that the two gates have distinct owners is
permitted.

**Single-positive consequence.** Any failure of the exact joint allocation
with N=1 must satisfy

    w>=12 or max(a,b)>=8.                           (3)

Consequently, if the sole positive source has w in{6,8,10} and both leg
heights in{4,6}, the joint allocation and coefficient-one ledger bound
hold for arbitrary other complete negative U and rotor sources. The earlier
width-six theorem also covers all heights at w=6; (3) does not replace it.
More generally the new necessary conditions (1)--(2) apply to every size.
All larger residual classes remain open.

## 2. An unactivated tip forbids original occupancy beside its support

For the left terminal s=(a+1,1), define q=(a+1,2). If s stays selected,
its occupied anchor(a,1) already uses its one permitted neighbor. Thus
q is finally blank. Since original endpoints and original selections both
remain occupied after fusion (a consumed selection becomes an endpoint),

    q is in neither P_j nor T_j for every source j.  (4)

This forbids original selections as well as endpoints. Excluding only
foreign endpoints would miss the shared-upright-owner clearance below.

## 3. Saturation forces irregular pairs full and gives strict clearance

From the exact reserve identity, R=0 forces A=U0=Z0=H=0. Every original
2P0T tile is then full: with only its original pair it contributes to
L2bar, and with one extra endpoint it contributes to L3. A nonfull tile
has no other possible final size. Every original phase11 U triple is also
full, directly from U0=0. This applies regardless of how final endpoint
components merge.

The phase10 gate roles already activate their corresponding positive tip.
The remaining phase11 down/right role has inverse reference coordinates

    (r,c) -> (h+2-r,c-1).

Its near stem occupies column2, rows2 through h+2. If h>=a, it contains
q=(a+1,2), contrary to (4). Even heights therefore give h<=a-2.
Its outside bar tile is

    Q={h+2,h+3} x {2,3}.

This has exactly the original pair{(h+2,2),(h+2,3)} and no original
selection: reference row0 is in the bar, while reference row-1 has no
endpoint or support at columns1,2. Thus it is 2P0T and must be full.
Equivalently the forward map F(r,c)=(h+2-r,c+1) factors as
F(r,c)=g(r+1,c+1), where g(r',c')=(h+3-r',c'). The odd reflection
constant h+3 makes g tiling-preserving; it takes the established phase11
upper-corner 2P0T tile{0,1}x{2,3} to Q, including its zero-support profile.
If h=a-2, fullness places q=(h+3,2) in P, again contradicting (4).
Parity now sharpens the clearance to h<=a-4, proving (1). In particular
any longitudinal unactivated gate in a zero-reserve fusion has side
height at least eight.

For the width statement, if v'+1>=w, the incoming bar crosses column w
in rows h+1,h+2. Endpoint disjointness from the positive opposite leg
then requires h>=b. When a<=b this contradicts h<a. Hence v'+1<w,
which is v'<=w-2. This clearance uses the opposite leg even when its
height is independent of the marked leg.

## 4. Transverse footprints and the distinct-owner case

For a phase01 upper corner, the endpoint directions from u are down
and right. Either the two-row bar runs right, through columns2 to v'+1
with v'>=6, or its near leg runs right, through columns2 to h+2 with
h>=4. Both contain {(2,c):2<=c<=6}. A phase11 right/down terminal also
has a rightward near stem through column h+2>=6 and contains this segment.
These cases, together with the longitudinal role in Section3, exhaust
unactivated occupied gates by the established source-local E catalogue
and rotor gate barrier.

The reflected right footprint is {(2,c):w-5<=c<=w-1}. If6<=w<=10,
the point(2,5) lies in both footprints: 2<=5<=6 and w-5<=5<=w-1.
Distinct original owners cannot overlap in an endpoint. Thus two distinct
transverse owners require w>=12, using that w is even.

## 5. Common ownership: two exact nested-U forms

The preceding footprint argument cannot be applied when both gates belong
to one source. We classify that case separately. The source-local E roles
are the two upper corners A and the two leg terminals F. A square-lattice
isometry permutes and signs the coordinate axes; it cannot mix them.

For two A roles, their reference displacement is(0,v'-1). To map them
to the two gates, the bar must be horizontal with v'=w-2. The bar's second
row must lie below row2, since the positive row1 is already occupied.
The complete source, including selections, is precisely the upright form
in (2), up to exchanging the reference leg labels.

An A and F on the same leg have even displacement length h; the gate
distance w-3 is odd. They cannot match. On different legs, both reference
coordinate differences are nonzero, so a signed coordinate permutation
cannot place them on the same row. This excludes all mixed A/F cases.

For two F roles, their reference displacement is(k-h,v'-1). Same physical
row forces h=k and a horizontal bar axis; v'=w-2. Their predecessors must
lie down, since row1 is positive. This gives exactly the inverted form in
(2), including its original support pattern. The gate barrier excludes
rotor ownership. There is no other common-owner case.

For the upright left leg, if h>=a then its near stem contains q, so h<=a-2.
If h=a-2, its original beyond-tip selection is(h+3,2)=q, contradicting
(4). Hence h<=a-4; the right leg gives k<=b-4. This step uses complete
support retention, not just endpoint disjointness, and does not require
saturation once both positive terminals are unactivated.

For the inverted form, Section3 applies on both sides. Its outside bar
pair tiles must be full at zero reserve, forcing h<=a-4 and h<=b-4.
All incoming heights are at least four, so both forms require a,b>=8.
Their widths are at least six, so w>=8. The common-owner dimensions shrink
by two in width and at least four on the incident positive heights; this
does not by itself define a recursive descent, since the incoming source
has a different phase. No acyclicity or termination theorem is inferred.

## 6. Consequence for the exact joint bound

With N=1, failure requires G=2,R=0 and both positive terminals unactivated,
by EXACT_GEOMETRIC_EVENT_RESERVE.md. Both gates are occupied, since blank
marks consume positive defect capacity. If one owner covers both gates,
Section5 gives both heights>=8. If the owners are distinct and w<=10,
Section4 says that at least one gate is longitudinal, whose side height
is>=8 by Section3. This proves (3), and its contrapositive gives the
stated new coefficient-one class. The proof treats every permitted
negative dimension and phase; no bounded search supplies this implication.

Failure of this sufficient allocation would still not imply failure of
ambient sigma or the unrestricted grid target. The remaining cases in
(3), and the multiple-positive-source counting problem, remain open.

## 7. Controls and formal scope

develop/check_saturated_gate_geometry.py checks348 normalized incoming
roles against98 positive dimension triples. It exercises both common-owner
normal forms, longitudinal near-equality exclusions and transverse-pair
intersections. These are endpoint/support ROLE controls, not complete
feasible source fusions. They cannot establish that any saturated residual
is realizable or impossible. Sections2--6 are the universal written proof.

formal/SubQuorum/SaturatedGateGeometry.lean checks universal coordinate
footprints, the outside irregular bar-pair profile, original upright
beyond-tip support, parity/strict-clearance deductions and conditional
two-gate/one-positive consequences. The source-role normalization, shared-
owner isometry classification and physical saturation adapters remain
written. Execution and individual axiom audits are recorded separately.

All13 declarations compile locally with Lean4.33.0; individual axiom
audits PASS without sorryAx/native_decide. Role controls PASS:933
longitudinal tips,380 near-equality cases excluded by saturation,190
shorter-side width descents,2390 transverse tips,1472 corners,36 upright
and36 inverted common-owner cases, and219086 transverse pair comparisons.
These counts remain role controls, not complete source-fusion realizations.
See output/saturated-gate-geometry-controls.json and
output/saturated-gate-geometry-formal-check.json. Original independent task
eb184fae completed ACCEPT at02:49:47UTC, observed gpt_6/pro, for the written
saturation, complete-support clearance, AA/AF/FF classification, width
descent and N1 consequence. It explicitly confirms that the local geometry
also applies to a chosen positive in arbitrary zero-reserve fusions. It
did not execute controls/Lean. Its optional outside-pair exposition is
incorporated above. See output/saturated-gate-geometry-review.json.
The preceding exact-reserve task2bf0d5dd completed ACCEPT separately.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
