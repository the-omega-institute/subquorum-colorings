# Whole comb channels compensate even when the terminal band is occupied

19 October 2026. A whole-channel partition removes the endpoint-free
terminal-band hypothesis from the remote-rung mechanism. The exact boundary
contribution is two for equal terminal heights and one for unequal heights.
Prescribed positive sources may enter or leave the channel; complete combs
contribute their actual signed end flux. A residual-capacity theorem combines
channels with the original mouth ledger without using a donor twice.

These are conditional geometric and counting theorems for the retained
prescribed-source class. They do not assert that every configuration has
enough channels or prove the unrestricted grid inequality.

## 1. Hypotheses and a forced boundary

Use actual grid coordinates with physical squares starting at even rows and
even columns. Retain the fixed terminal representative, actual matching,
prescribed positive long sources and complete straight comb definitions of
`OPEN_SOURCE_CAVITY_COMPENSATION.md` and `REMOTE_COMB_RUNG_COMPENSATION.md`.
In particular each source has positive physical phase, even chamber width
at least eight, its prescribed matching and retained supports. A complete
comb has its prescribed alternating side supports and both axial supports.

Two distinct complete vertical comb endpoint components are

    P_L={u_L,...,s_L} x {a},    P_R={u_R,...,s_R} x {b},

where a is odd, b even, b-a>=5, the u's are odd, the s's even, and
max(u_L,u_R)<=min(s_L,s_R). On odd endpoint rows, their side supports face
inward, at a+1 and b-1. On even rows they face outward, at a-1 and b+1.
Thus both top physical singleton ends are sparse and both bottom ends are
saturated. Other directions follow by physical-tile-preserving symmetries.

Set t=max(u_L,u_R)-1, s=min(s_L,s_R), and delta=0 if s_L=s_R, otherwise one.
The whole channel is the physical rectangle

    C={t,...,s+1} x {a+1,...,b-1}.                 (1)

It lies in the ambient grid. All endpoint components meeting C are complete
prescribed positive sources or complete straight combs, possibly extending
outside C. The walls themselves have no endpoints inside C. There is no
endpoint-free assumption on the terminal band {s,s+1} x {a+1,...,b-1}.

**Boundary lemma.** Both extreme columns of C are endpoint-free. If r=s-t+2
is its even number of rows, their combined selected count is

    tau=r-2+delta.                                 (2)

Proof. Each odd row t+1,t+3,...,s-1 has the prescribed inward side support
on both sides. Each such support already sees its wall endpoint. Feasibility
therefore forces its vertical neighbors blank, including the even first row
t and all even rows through s, and excludes endpoints there as well.

At row s+1 a terminating wall has its axial support at the wall column.
That support already sees the terminal endpoint in row s, forcing the
adjacent channel corner blank. A continuing wall has its next inward support
at row s+1: its even terminal height is at least s+2. This corner is selected
and sees its prescribed endpoint. Exactly delta walls continue. There are
r/2-1 selected odd rows before the corner on each side, so tau=r-2+delta.
This proves the exact labels and endpoint exclusion on the whole boundary.
The forcing supports need not belong to C. QED.

## 2. Exact whole-channel identity

Let D_C be the sum of 2-|T intersect Q| over original physical squares
Q in C with no endpoints. Remove both extreme columns and partition the
remaining rectangle into squares shifted one column; let D'_C be its
analogous no-endpoint deficit. Both are nonnegative by feasibility.

For every prescribed source K let Gamma_C(K) be the difference of its
physical and shifted raw endpoint-square excesses, where raw excess is
|T intersect Q|+|P intersect Q|/2-2. Put

    G_C=sum_K Gamma_C(K),
    Phi_C=sum_complete_combs (saturated end in C - sparse end in C).

Actual physical end tiles, not artificial component ends at the cut, determine
Phi_C. The walls have neither singleton end tile in C and contribute zero.

**Whole-channel identity.** Under Section 1,

    D_C=2-delta+G_C+Phi_C+D'_C,    G_C,D'_C>=0.     (3)

Proof. Suppose the physical partition has N squares, the shifted one N'
squares, C contains p endpoints and z selected sites. Write E,E' for their
raw endpoint-square excess sums. The physical and shifted deficit identities
are

    2D_C=4N-2z-p+2E,
    2D'_C=4N'-2(z-tau)-p+2E'.

Each partition consists of complete squares. The boundary lemma ensures
trimming deletes no endpoint, so the same p occurs in both equations.
There is one fewer square in each of the r/2 row bands, hence N-N'=r/2.
Subtracting and using (2) gives

    D_C-D'_C=2-delta+(E-E').                       (4)

The accepted partial-source row-band calculation applies to this rectangle:
it needs complete physical row pairs and endpoint-free extreme columns,
rather than a root source. A parallel source contributes the number of its
actual physical tip tiles in C, zero, one or two. A perpendicular interior
chamber band contributes 2-ell-q>=0, since each two-site flank has at most
one selection. An end-arm band contributes 1-optional_selection>=0.
Any encountered horizontal arm path is complete between the endpoint-free
extreme columns; otherwise its connected endpoint path would cross a
forbidden boundary endpoint. These cases cover every intersecting source
band. Thus G_C>=0, and a fully enclosed source still contributes at least two.

For a complete straight comb, the established raw phase table gives exactly
its physical saturated-minus-sparse singleton-end membership. A matching
edge can cross the top or bottom boundary without altering these raw square
identities; there is no corrected partial-receiver charge. Summing components
gives E-E'=G_C+Phi_C and proves (3). QED.

In particular, if G_C+Phi_C>=0 then D_C>=2 for equal terminal heights and
D_C>=1 otherwise. The signs are essential: escaping complete combs may
give negative Phi_C. Endpoint occupancy by itself is not negative phase,
and a complete contained source actually earns at least two extra units.

## 3. Combining channels with mouths without donor reuse

Retain the established doubled mouth ledger

    2Delta=F+A+Dprime+Dsingle+2R,                  (5)

where Delta=mn/2-|T_0|-|M_0| is integral, and A,Dprime,Dsingle,R>=0.
F is complete-comb signed end incidence with original mouth multiplicity.
For an original physical no-endpoint square Q put d_Q=2-|T intersect Q|.
Let m_Q in {0,1,2} be its original mouth-strip multiplicity. Its residual
capacity in (5), after the original strip identities, is exactly

    (2-m_Q)d_Q.                                   (6)

Indeed a singly covered donor contributes d_Q to Dsingle, an exterior
donor contributes 2d_Q to 2R, and a doubly covered donor contributes zero.
R can also include nonnegative outside-receiver slack, which is not needed
for this donor budget. An already selected support remains in the actual
count |T intersect Q| and is not an extra resource.

**Weighted channel compensation theorem.** For channels C_j satisfying
Sections 1-2, choose nonnegative weights w_j such that, on every positive
physical donor Q,

    sum_(j:Q in C_j) w_j <= 2-m_Q.                 (7)

Then

    2Delta >= F+sum_j w_j(2-delta_j+G_j+Phi_j).     (8)

Consequently a right-hand side at least -1 proves |T_0|+|M_0|<=mn/2.

Proof. Original physical incidence and (7) give

    sum_j w_j D_Cj
      =sum_Q d_Q sum_(j:Q in C_j)w_j
      <=sum_Q (2-m_Q)d_Q
      <=Dsingle+2R.

All sums use original no-endpoint squares only. Equation (3) and D'_Cj>=0
give the lower bound by the sum in (8). Substitute in (5), discard only
the nonnegative A and Dprime, and use integral Delta for the consequence.
G_j, Phi_j and shifted deficits are terms in identities for the same
physical payment. None is added to donor supply afterward. QED.

**Simple pairing consequence.** Suppose each of q channels has G_j+Phi_j>=0.
Use weight one for equal ends and weight two for unequal ends. If (7) holds,
then sum_j w_j D_Cj>=2q, so F+2q>=-1 suffices for coefficient one.
An unequal-end channel needs both residual slots on each of its positive
donors; such a donor cannot already be used by a mouth or another channel.
An equal-end channel uses one slot and can share only when (7) permits it.
One cannot multiply a geometrically overlapping channel certificate without
checking these actual slots.

The baseline weights need not be used when actual phase pays more. An
unequal-end channel with G_C+Phi_C>=1 already has D_C>=2, so weight one
suffices. This can be essential when it contains positive donors of mouth
multiplicity one: weight two would violate (7), while weight one is allowed.
The phase improves the certified payment of the same physical donors; it
does not supply a second donor account.

For initial configurations impose complete prescribed frozen endpoint data
for every component meeting a channel, or state the theorem at the fixed
terminal representative. The previously proved normalization retains all
old selections, acts only on its own old endpoints, and cannot alter a frozen
component. It creates no new endpoints. Thus the channel labels persist
even when a prescribed component escapes. Outside nonpositive-receiver
coverage remains the separate hypothesis behind (5).

This improves the universal 5/6 coefficient to one on the classes certified
by (7)-(8), including occupied terminal bands. No general channel-cover or
signed-flux existence assertion is included.

## 4. A uniform occupied-band family with zero mouth payment

Take even W>=32, h>=1 and ell_L,ell_R>=2. Use the usual positive source
of chamber origin (2,3), width W and depth h; set y=2h+4. Add the two
downward comb walls

    column 9: endpoint rows y+1,...,y+2ell_L,
    column 22: endpoint rows y+1,...,y+2ell_R,

with the prescribed inward odd-row supports, outward even-row supports,
consecutive matching and both axial supports. Let ell=min(ell_L,ell_R)
and s=y+2ell. Add a horizontal complete comb in row s, columns 14,...,17.
Its axial supports are (s,13),(s,18); its other supports are (s-1,14),
(s+1,15),(s-1,16),(s+1,17). Match 14--15 and 16--17.

Retain every prescribed source/comb support and add these mouth selections:

| Row | Additional selected columns |
| --- | --- |
| Both y and y+1 | 5,7 and even 24,...,W |
| y | 9,11,14,17,20,22 |
| y+1 | 10,12,13,15,16,18,19,21 |

All unlisted vertices are blank except the prescribed supports. The ambient
rectangle is (y+2max(ell_L,ell_R)+4) by (W+8), with zero-based coordinates.
The channel is rows y,...,s+1 and columns 10,...,21. Its terminal band
contains four endpoints, so the earlier endpoint-free terminal-rung
hypothesis fails for these walls.

### Feasibility and exact payment for every parameter

The source arms are at columns 3,W+2. The wall endpoint columns 9,22
and their support columns 8,10,21,23 are separated from them. At the mouth,
the listed selections form horizontal pairs or vertical pairs: columns
5,7 and even columns 24,...,W form vertical pairs, while columns 9,22 in
row y see their axial wall endpoint below instead of the blank neighbor
in row y+1. The additional middle pairs are (y+1,12)--(y+1,13),
(y+1,15)--(y+1,16), and (y+1,18)--(y+1,19); their upper neighbors are blank.
Selections at (y,11),(y,14),(y,17),(y,20) are isolated: their adjacent
lower-row sites and same-row neighboring columns are blank.
The inward supports at (y+1,10),(y+1,21) see just the wall endpoint.
These checks also account for the prescribed root supports near each tip.

Away from the mouth, each wall support sees only its own endpoint.
The internal horizontal comb and its supports are in columns 13,...,18,
at least two columns from the facing wall supports. Its top supports are
at row s-1>=y+3, hence separated from the mouth filling. Each such support
sees exactly its own horizontal endpoint; the bottom and axial supports
have the same property. If one wall continues below s, its inward support
at row s+1 is at column 10 or21 and still separated from the blocker.
Thus no selected vertex has two occupied neighbors and no endpoint
components join. The complete prescribed support lemmas freeze every
component. This checks all interfaces for every W,h,ell_L,ell_R.

The original source mouth has zero physical and shifted no-endpoint
deficit. Its two wall contacts are sparse while their saturated ends are
outside the mouth, so F=-2. The blocker is complete inside C, giving
Phi_C=0, and the root has no endpoints in C, giving G_C=0.

There are 6(ell+1) physical channel squares. The two blocker endpoint
squares are excluded, leaving 6ell+4 no-endpoint squares. Their total
selection count is 2ell+14+delta: the first band contributes twelve,
the ell-1 intervening bands contribute 2(ell-1) wall supports plus two
blocker top supports, and the last band contributes its two axial blocker
supports plus delta continuing-wall supports. Therefore

    D_C=10ell-6-delta,
    D'_C=10ell-8,      G_C=Phi_C=0.                (9)

All positive channel donors are outside the original mouth: every original
mouth no-endpoint square has zero deficit. Thus every positive channel
donor has residual capacity two. Weight two in (8) proves Delta>=1 for
aligned ends and Delta>=0 for unequal ends, despite F=-2 and the occupied
terminal rung. The numerical payment in (9) is not claimed sharp among
all fillings; the boundary contribution in (3) is the reusable conclusion.

### A contained source repairs the weight conflict

For an additional explicit all-parameter family, take the same root, walls
and mouth filling, with ell_L,ell_R>=6, and omit the horizontal comb blocker.
Instead put a prescribed rightward positive source of width eight and depth
one with chamber rows y+5,...,y+12 and columns 14,15, and tips at column18.
Use its prescribed matching/supports and add the sharp outer-flank selections
at column13 in rows y+5,y+7,y+9,y+11, and inner-flank selections at column16
in rows y+7,y+9. All other sites are blank except the named supports and
the preceding mouth filling.

The added source/support footprint is in columns 13,...,19, separated from
the wall inward support columns 10,21 by at least one blank column. Its
first support row is y+4, separated from the last mouth-filling row y+1.
The prior complete-source sharp-flank feasibility proof therefore applies
without any interaction with the root or walls. Deleting the earlier comb
only removes occupied vertices. This proves feasibility and complete
freezing for all the stated parameters. The source is fully inside C,
including its lower arm at y+12<=s. When min(ell_L,ell_R)=6 it occupies
the terminal band; longer channels retain the same theorem.

Its whole phase is exactly 8-4-2=2. It is the only source with endpoints
in C, and both wall end tiles remain outside C, so G_C=2 and Phi_C=0.
The root mouth is the old zero-payment horizontal strip in rows y,y+1.
The new source mouth is the vertical strip in columns18,19 and rows
y+6,...,y+11. These two mouth strips are disjoint, so m_Q<=1 everywhere.
The two sparse wall ends are the only comb-end contacts with either mouth,
hence F=-2. Weight one on C satisfies (7) for every donor. Equation (8)
gives

    2Delta >= -2+(2-delta+2)=2-delta,

and thus Delta>=1 even for unequal terminal heights. In contrast, applying
the baseline unequal-end weight two fails on the three positive physical
donors in the new source mouth. Each such donor has only one residual slot.
There are no selections in that vertical mouth: its three tiles each have
d_Q=2. The rejected assignment overuses six units in the doubled ledger.
This is a failure of that sufficient allocation choice, repaired by using
the actual phase in (8), rather than a failure of the channel theorem or
the grid target.

## 5. Verification scope

`develop/check_comb_channels.py` recomputes both raw partitions, source-band
gains, complete-comb end flux, exact wall labels, feasibility and freezing.
It checks the all-parameter family's formula, unequal starts, signed
escaping combs, complete perpendicular sources in the channel, symmetry,
and pointwise residual capacity, including rejected repeated claims.
The checker passes 194 physical cases and eight symmetry images. Its eight
source-containing controls check both the rejected baseline assignment for
unequal heights and the valid phase-aware weight-one certificate.

`formal/SubQuorum/CombChannels.lean` formalizes the conditional tall-channel
partition, aligned/unequal baseline weighting and the integral consequence
of the residual ledger. Full boundary geometry, component adapters and
the coordinate family remain written proofs. Finite controls discover and
test these statements; they do not prove the general theorem.

The local Lean4.33.0 sequential audit passes 123 scoped declarations, including
these three additions; the receipt is `output/comb-channel-formal-check.json`.
The original 90-case/eight-image open-source regression is checked separately.

Arbitrary positive bent receivers, existence of enough admissible channels
and control of their signed flux remain open. Submitted manuscripts are
kept separate from these research notes.
