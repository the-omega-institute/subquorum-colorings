# The tight upward successor has a uniquely located near terminal

21 October 2026. Use the complete original U/rotor model and the
[support-closure theorem](SECONDARY_TEN_SUPPORT_CLOSURE.md). This strengthens
the tight gap g=m+2. It does not yet establish global target nonreuse.

Prescribe the actual distinct original sources

    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    D=U(m,10,4), D(r,c)=(b-11+r,c+5),
    E=U(w,m+2,v), E(r,c)=(b-4-c,m+9-r),
    C=U(omega,h,xi), C(r,c)=(b-5-c,m+7-r).

All dimensions are legal even integers, b is even, m>=6, v,xi>=4;
endpoint sets are disjoint. By the support-closure theorem, C is the
actual owner of D's support (b-6,m+5), and 4<=h<=m. The earlier width
collision gives omega<=w-2. In addition omega=6 is impossible because

    C(2,6)=(b-11,m+5)=D(0,m),

so omega>=8 and w>=10. The following rigidity argument only needs
omega>=6; it is valid before this sharpening as well.

**Terminal-rigidity theorem.** Every complete extension satisfies h=m.
Consequently C's positive near terminal and its two consumed supports are

    z=(b-6,7),
    axial support (b-6,6)=D(5,1),
    lateral support (b-5,7)=E(m+2,1).

The activation location is fixed, independently of C's width and far leg.
Its axial support has an original straight degree-two D anchor role,
while the lateral support is E's original terminal. Both owners are
identified, not presumed fresh or different merely by notation.

## 1. A top-row consumer obstruction

We first use only D and E plus an arbitrary already occupied south
neighbor at s=(b-9,c), where7<=c<=m+3. Suppose s is forced to be an
endpoint and its consumer is different from the owners of its north
D neighbor and south occupied endpoint. Then its own neighbors lie only
west/east. No original U or rotor can consume s without meeting D or E.
Using E as a blocker does not require an unproved freshness assumption:
on this row E owns only columns m+8,m+9, outside the interval for s.
D owns only the two wall sites at columns6,m+5, also outside it.

For a U, the only possibilities are horizontal terminals and horizontal
straight leg interiors. At row b-9, D owns both wall sites at columns6
and m+5. Thus the entire incident horizontal segment and its two bar
columns must be strictly between these walls, at columns7,...,m+4.
An upward bar immediately meets D's lower bar on row b-10. A downward
bar of width>=6 meets E's incident row b-5, four steps below. Hence
every U is excluded. This includes all straight interiors, not just tips.

The four horizontal rotor tips have the following blockers relative to s:
east form A has (-2,1), on D's upper bar; east form B has (-1,2), on
D's lower bar; west form B has (-2,-1), on D's upper bar. Their columns
are within the prescribed bars for7<=c<=m+3. West form A has (-1,-2)
on D's lower bar when c>=8. When c=7 it has (0,-1), on D's near stem
at column6 instead. Every rotor nontip has three own neighbors and is
already excluded. This proves the local obstruction for arbitrary source
dimensions. No enclosure, minimum-source-extent assumption or bounded
census is required.

## 2. A shorter incident leg would force one of two north rotors

Suppose h<m and put T=m+7-h. Then T is odd and

    9<=T<=m+3.

C's original beyond-tip support a=(b-6,T-1) has anchor east at its
terminal (b-6,T). E owns its south neighbor (b-5,T-1). The point is
absent from Q,D,E,C, so it must be consumed by a different owner with
own neighbors only north/west.

No U can own a. A north terminal or either north-bearing corner reaches
D's lower bar four steps north at (b-10,T-1). For the two corner
orientations, either the bar runs north for at least five steps, or the
bar runs west and its incident leg runs north for at least four steps.
A west terminal whose
stem reaches column6 hits D's near stem. Otherwise its bar remains
between columns7 and T-1; an upward bar hits D's lower bar on row b-10,
and a downward bar hits E's incident row on row b-5. Straight interiors
and degree-three roles are excluded by the two blocked neighbor directions.

The two west rotor tips also collide with D/E below. West form A contains
a+(1,-1)=(b-5,T-2), always on E's incident row. West form B contains
a+(1,-2)=(b-5,T-3): for T=9 this is D's near stem at column6, and
for odd T>=11 it is on E's incident row. Thus only the two north rotor
tip footprints can remain. In relative coordinates at a they are

    RA={(-3,-1),(-2,-1),(-2,0),(-2,1),
        (-1,-2),(-1,-1),(-1,0),(0,0)},
    RB={(-3,1),(-2,-1),(-2,0),(-2,1),
        (-1,0),(-1,1),(-1,2),(0,0)}.

If either already intersects a prescribed endpoint it is excluded
immediately. Otherwise use its original supports in the next step.

## 3. Either north rotor forces the forbidden top-row consumer

For RA, its original support sA=a+(-3,1)=(b-9,T) has anchor south at
(b-8,T), an RA endpoint, and a distinct north D neighbor (b-10,T).
For RB, its original support sB=a+(-3,-1)=(b-9,T-2) has anchor south
at (b-8,T-2), an RB endpoint, and north D neighbor (b-10,T-2).
These support and anchor statements use the full original rotor source,
not just a plausible endpoint footprint. Explicitly, the original rotor's
support set in the [source catalogue](../develop/rotor_networks.py) is

    {(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)}.

Its support (1,4) has the sole original endpoint neighbor (2,4).
The maps (r,c)->(r-4,c-3) and (r,c)->(r-4,3-c) give RA and RB,
respectively. They take this original support/anchor pair to
(-3,1)/(-2,1) and (-3,-1)/(-2,-1). Thus the two forcing sites have
original-support status, beyond the fact that they are absent from the
endpoint footprints. The independent constructor controls check these
identities as well.

Neither support belongs to Q,D,E,C or its respective original rotor.
At row b-9, Q has no endpoint; D has endpoints only at columns6,m+5;
E's bar columns are m+8,m+9; C's bar columns are m+6,m+7. The respective
support columns lie in [7,m+3]. The horizontal far legs of E,C are above
this row for legal widths. Retention therefore forces a new consumer at
sA or sB with own neighbors only west/east. Section1 rules it out.
This is a contradiction for both remaining rotor forms.

Thus h<m is impossible. Combined with h<=m, this proves h=m and the
three displayed physical coordinates. C is positive because its bar
coordinate m+7 is odd; both original supports at z are actually consumed.

## Scope

The [independent checker](../develop/check_secondary_ten_terminal_rigidity.py)
passes162 top-row sites at secondary widths6,8,12,20,50, with no U or
rotor consumer. All horizontal straight interiors are included. Eighty-four
disjoint short-leg Q/D/E/C stencils have zero first-site U consumers and
132 surviving north rotors (48 RA,84 RB); each forces its original support
at the forbidden top site. Ten rigid-terminal support controls pass.
[Output](../output/secondary-ten-terminal-rigidity-controls.json).
These are partial stencils, not complete realizations, and are validation
of the written unbounded proof.

[Scoped Lean](../formal/SubQuorum/SecondaryTenTerminalRigidity.lean)
passes16 declarations and their individual axiom audits, finalsession36396
exit0, with no warnings or sorry/native axioms. Its scope is the forcing,
blocker and support coordinates, the two rotor footprints and retention
implication; the complete catalogue adaptation and composition into h=m
remain written. [Receipt](../output/secondary-ten-terminal-rigidity-formal-check.json).

Independent written audit20923ea9 **ACCEPTS** the full two-stage h=m
proof and the separate general far-leg-reach width bound. Its original
stream38190 exits0 with DONE/no errors; the11940-character answer exactly
matches the completed task response, observed gpt_6/pro. The original
rotor support identities remain explicit model data, with their catalogue
transport now displayed above. The reviewer also verifies the same-owner
exclusions and all straight U interiors. This review certifies the written
argument, not execution, complete realizability or global nonreuse.
[Review receipt](../output/secondary-ten-terminal-rigidity-review.json)
and [full response](../output/secondary-ten-terminal-rigidity-review-response.md).

The proof fixes a local target and identifies both support owners. A
global injection from actual labelled marked claims and exclusion of
ALL previously reserved targets are still separate obligations. No new
source, reserve or integer-ledger increment is counted twice or claimed
here. Complete actual-chain existence and the full allocation/grid
objective remain OPEN. Submitted manuscripts and the primary C4-free
result are preserved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
