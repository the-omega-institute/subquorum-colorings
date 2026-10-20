# A forced bottom owner and the obstruction to a naive descent

20 October 2026. This note continues the unrestricted complete-source
allocation problem. It proves an additional owner requirement at every
unpaid full-chain width-six double and excludes an upward wrapping branch
at clearance four under the zero-defect saturation hypotheses. It does
not settle finite closure, coefficient one for all complete sources, or
the rectangular-grid triple equality.

## 1. Persistent bottom support and a forbidden occupied point

Use the exact model and four original owners of
WIDTH_SIX_FOUR_STEM_COMPENSATION.md. Normalize the positive source
O=U(6,a,b), with left terminal unactivated, and its longitudinal incoming
owner L with tip(2,2), incident height h, width vL and far height fL:

    L(r,c)=(h+2-r,c+1), h<=a-4.

Write g=a-h, an even integer at least four. L's lower bar contains
(h+2,c) for every 2<=c<=vL+1. In particular let

    p=(h+3,2), q=(a+1,2).

Because h+3 is odd and 2<=h+3<=a-1, p is an original support of O.
It has two persistent original endpoint neighbors: (h+3,1) of O and
(h+2,2) of L. Support retention and the final selected-degree condition
therefore force p to be an original endpoint of a source F. It is not
an endpoint of O,L,V,W,R: the latter three incident heights are smaller
than h, and their bars end before row h+3. Thus F is a sixth distinct
original owner, without assigning or spending any defect resource.

The original O support (a+1,1) remains selected because the left terminal
is unactivated. Its neighbor (a,1) is a persistent endpoint. Consequently
q is absent from the final occupied set. In particular q is absent from
EVERY original endpoint set and EVERY original support set, including a
support that another source might otherwise consume.

## 2. Universal role classification at clearance four or six

Translate p to(0,0). Original foreign endpoints include

    {(-1,c):0<=c<=5} union {(r,-1):0<=r<=2}.

The upper row is part of L's bar. The left column is part of O's long
leg and, at g=4, its retained beyond-tip support at the last point.
Although the last point may be selected rather than an endpoint, no
original endpoint can occupy it because the terminal is unactivated.
The forbidden point q has relative coordinates(g-2,0).

Exact two-chirality/eight-role rotor exhaustion against this stencil
is empty. The stencil is fixed, so matching a rotor role to p fixes its
translation and gives an exhaustive result over all translations.

For a U owner, an endpoint with foreign sites immediately up and left
cannot be an interior bar point, lower bar corner, or nonterminal stem
point. Those roles respectively have at least three own endpoint
neighbors or two opposite own neighbors. An upper bar corner could
have its bar down and leg right, or its bar right and leg down. In the
first case the downward bar has at least six sites, and in the second
case the downward stem has incident height at least four. Both contain
the forbidden point at distance two or four below p. A downward terminal
predecessor likewise has at least four sites and hits q. Therefore F
must be a terminal with predecessor immediately right.

This U-role statement holds for arbitrary width and independent heights,
not only the dimensions used in executable controls. The Lean theorem
blocked_vertical_owner_is_horizontal_tip proves it directly from the
original endpoint predicate and all eight lattice isometries; the
forbidden distance can also be one, used in the next section. Its final
signature needs only the immediately upper and left endpoint exclusions,
not the entire nine-point rotor stencil. This makes its application at
the second point literal. The endpoint-role theorem needs only minimum
dimensions; support-direction and phase assertions below additionally use
the model's legal even widths and heights.

The bar direction is NOT yet determined. If d is the incident height,
v the width and f the far height, the two exact forms, after naming the
near leg as the reference left leg, are

    Fdown(r,c)=(h+2+c,d+2-r),
    Fup(r,c)  =(h+4-c,d+2-r),
    Fdown/Fup image of U(v,d,f).

Fdown has its near stem in row h+3 and bar downward. Its terminal
receiver has original pair{(h+3,2),(h+3,3)} and support{(h+2,2)}
under the fixed tile alignment. The source has no original triple caps
(the phase10 class).
Fup has its bar upward and two original triple caps (the phase11 class).
Thus the premise that every original endpoint-containing phase11-U
receiver is full applies to Fup, but not automatically to Fdown.

Upward wrapping genuinely survives these local endpoint/forbidden-point
conditions. For O=U(6,14,4), L=image U(12,10,4) under(12-r,c+1),
take Fup=image U(8,14,4) under(14-c,16-r), or U(6,16,4) under
(14-c,18-r). All three original endpoint sets are disjoint, q=(15,2)
is absent from Fup's endpoints and supports, and Fup has two triple caps.
These are incomplete local arrangements: mandatory supports are still
infeasible. They refute only a claimed local forced-down classification,
not compensation or the target inequality. In particular an upper bar
can wrap beyond the right end of L; a short bounded-dimension check
would miss it.

## 3. Zero-defect saturation excludes upward wrapping at g=4

Assume g=4 and every original endpoint-containing phase11-U receiver is
full, as follows in the accepted complete-source ledger when U0=H=0.
Suppose F=Fup. Its original support

    n=(h+4,2)

is the exterior support of its near terminal. It sees F's endpoint p
above and O's endpoint(h+4,1) to the left. Hence n is an original endpoint
of another owner G. This point is absent from all six existing endpoint
sets. Its forbidden point q=(h+5,2) is immediately below.

Up and left from n are foreign occupied points; a rotor is excluded by
the exact stencil consisting of F's first four near-stem points above
n, O's endpoint left of n, and q below. A U at n can have no downward
own endpoint neighbor because of q. Its only possible role is a terminal
with predecessor right; the same universal U-role lemma, at forbidden
distance one, proves this. Since q cannot even be an original support,
the bar of G must go down: an upward bar would put G's exterior terminal
support precisely at q. This support-direction deduction is also a
universal Lean statement for both reference terminal roles.

The row of n is even and its column is two. A rightward terminal with
bar down is therefore phase11. Its exact original regular terminal
receiver is

    Q={h+4,h+5} x {2,3},
    original pair={(h+4,2),(h+4,3)},
    original support={(h+5,3)}, original blank=q.

Under the saturation hypothesis Q must be full of original endpoints.
But q is forbidden to every original endpoint and support. This is a
contradiction. Thus at clearance four the forced sixth owner is Fdown.
At positive gap a-b=10 the existing four-stem inequalities force
h=b+6 and g=4, so this conclusion applies to every such residual double.

No extra payment is added to J, X, Y or H here. It is a saturation-based
branch exclusion, so there is no assumption of a fresh independently
spendable resource. Nor is a seventh-owner count summed across doubles:
owners in the two staircases might coincide through different tips.

## 4. What this does and does not establish

This gives a forced sixth original owner at every unpaid full-chain
width-six double, a universal horizontal-terminal classification at
clearance four/six, and a phase10 downward continuation at clearance four
under zero-defect saturation. It rules out a tempting shortcut: the
upward alternative is locally possible and needs the global saturation
hypothesis to exclude it in that case.

The surviving phase10 owner has no triple caps. Source-wide phase11
saturation supplies no automatic full chain for it. Also a positive gap
larger than twelve permits clearances at least eight, where corner and
vertical-terminal roles can occur. No global descending measure, complete
feasible AA realization, or coefficient-one proof is obtained here.
Both the unrestricted complete-source allocation and rectangular-grid
triple equality remain OPEN. A future mu<0 example would still require
a separate ambient sigma calculation before it could challenge that target.

Verification files: formal/SubQuorum/WidthSixBottomOwner.lean and
develop/check_width_six_bottom_owner.py. The executable controls include
all U endpoint roles and all eight isometries at representative dimensions,
both upward and downward first-owner branches, and the forced second-owner
profile. Complete feasible new-branch coverage is ZERO. Finite enumeration
supplements the universal proof; it does not replace it. The physical
source-normalization, phase-profile and global saturation adapters remain
written dependencies rather than an end-to-end arbitrary-fusion Lean proof.

All six scoped declarations pass local Lean4.33.0 source checking,
object build and individual axiom audits. The two rotor tables have no
axioms; other declarations use only propext, Classical.choice and Quot.sound
as applicable, without sorry/native_decide. Controls pass32896 first-owner
role tests with100 downward and13 upward survivors at EACH clearance4/6,
and32896 second-owner role tests with200 forced downward-U11 profiles.
See output/width-six-bottom-owner-formal-check.json and
output/width-six-bottom-owner-controls.json. Independent audit f3131137
completed ACCEPT at2026-10-20T05:53:49.100UTC, observed gpt_6/pro,
16263characters. Original stream19690 exits0/DONE and exactly matches
the terminal response. It accepts the structural argument under the
accepted inputs, not executions/provenance. Its requested distinction
between parity-free endpoint roles and even-dimension phase/support claims
is explicit above. Following its suggested weaker adapter, the Lean
classifier now requires only the upper/left exclusions actually used in
its proof, so the second-point application no longer needs the extra
nine-blocker premise. The later positive-owner reserve addition is outside
that review. See output/width-six-bottom-owner-review.json.

Research follow-up54d0581e completed at05:50:36.725UTC, observed gpt_6/pro,
20781characters; its terminal response was recovered from the original
task after stream EOF, with no complete-stream equality claim. It proposes
the further positive-owner reserve obstruction and other boundary/cross-core
leads. Those leads are not established by this note or by this ACCEPT verdict.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
