# A forced continuation repairs one return, but repeated returns spend the band

21 October 2026. Owners: Haobo Ma and Wenlin Zhang. General written
proofs with finite corroboration. The verification scope and review
state are recorded separately below.

Retain the exact Q,D,L,C,E,W family and definitions of the
[third-left return note](SECONDARY_TEN_NORTH_THIRD_LEFT_RETURN.md):
b even, a=b-9 odd, w>=12 even, N counts positive ORIGINAL owners only,
Rraw=S+2F-Ev, Phi=N+Rraw. The initial six-owner package has Phi
exactly3 below Q/D/W. All source endpoint sets are disjoint.

Add its returning consumer

    T0=U(w+6,6,4), T0(r,c)=(a-4+r,w+11-c).

It supplies DeltaPhi=1. Its original support x=(a+2,w+11) is absent,
with T0's terminal to the west and E's endpoint to the south. Thus
any complete extension must consume x. Original supports are never
redefined after consumption. A support already occupied by another
original owner's endpoint is not a fresh owner or a second credit.

## Necessary next-consumer forms

Every actual consumer V of x is a north-terminal U, in one of the
two frames, with legal even k>=6, ell,z>=4:

    Vright(r,c)=(a+2-ell+r,w+10+c),
    Vleft (r,c)=(a+2-ell+r,w+12-c).

Proof. Its own endpoint neighbors can only be north or east, because
west and south already have fixed foreign owners. The complete U
endpoint catalogue leaves a north terminal, an east terminal, or an
outer corner with north/east neighbors. Every east-terminal or such
outer-corner role contains x+(0,3): along its incident leg or its bar
there are at least four consecutive endpoints. But x+(0,3)=(a+2,w+14)
is C's far-leg endpoint, since C=U(8,6,4). This rules those roles out.
Straight interiors need opposite neighbors and degree-three roles need
three neighbors. The two north-tip rotor forms each contain (-2,-1)
relative to x, occupied by T0. The two east-tip forms each contain
(-1,2), occupied by E. Hence no rotor role survives. A north-terminal
U can point right or left; both must be retained, including arbitrarily
wide left escapes beyond the finite catalogue's dimension bound.

## Exact repair in the right and interior-left branches

For every Vright above, all original endpoints are disjoint and

    Delta S=k-1, Delta N=0,
    Delta Rraw=Delta Phi=k-1-[ell=4]>=4.       (1)

Proof. Its near column w+11 shares a tile pair with T0's near
column w+10. For ell>=6 the three full shared tiles are

    (a-3,w+10), (a-1,w+10), (a+1,w+10),

where coordinates denote tile lower corners. Each has two endpoints
of each owner, gains one mixed full tile and two directed events.
At each row the original lateral supports exclude the other two
potential directions; this remains so at the T0 bar junction and both
terminals. Thus their total 2F-Ev is zero.
The top shared tile (a-5,w+10) has T0's upper corner and one V endpoint
when ell=6, or two V endpoints when ell>=8. It is not full, and both
directions of its single horizontal contact meet original supports.
It contributes F=Ev=0.

For ell=4 the first of these tiles has two T0 endpoints and only one
V endpoint. Its horizontal contact is excluded in BOTH directions by
the two original supports, so F=Ev=0 there. The other two full tiles
retain one full tile and two events each. One additional shared tile
(a-1,w+12) has two V lower-bar endpoints and E's far terminal at
(a,w+13). It has no full tile and one event V to E; E's reverse
direction meets its original axial terminal support. Thus its debit
is exactly1. No other contact is possible: D/L end before these tile
columns; Q/W are further left; C's stems are w+7,w+14 below V's bar;
E's near stem is left and its far terminal is the stated exceptional
contact. V's far column is at least w+16, beyond C/E, for every z.
This proves (1). Together T0 and Vright repair the prior loss3 with
at least2 remaining in THIS inventory, not yet a globally unused credit.

For Vleft with k<=w+6, disjointness holds exactly when z<=ell-8.
For every such candidate,

    Delta S=k-1, Delta F=3, Delta Ev=7,
    Delta N=0, Delta Phi=k-2>=4.              (2)

Proof. Its far column w+12-k lies between6 and w+6, within T0's
bar columns. The ell=4,6 bar positions collide with T0. For ell>=8,
the far leg cannot reach T0's upper bar row a-4, giving
a+2-ell+z<=a-6, or z<=ell-8 by even parity. Conversely that
inequality implies ell>=12 and separates the entire bar and far leg
from every fixed endpoint tile. Only the near leg shares tiles, now
the three full tiles above plus the top tile (a-5,w+10). The latter
has one T0 upper-bar endpoint and two V near-leg endpoints, no full
tile, and one event V to T0. T0's reverse event is excluded by its
original top-corner support. The three lower tiles give six events.
This proves (2). In particular an interior-left consumer repairs as
well, but an arbitrarily wide left return is not covered by (2).

## Two further forced returns: a sharp failure of per-consumer credit

The following escaped-left classification was derived AFTER the initial
independent review request. That initial verdict, when available, does
not by itself cover this strengthening.

### Complete escaped-left local count

For Vleft with k>=w+8 put f=w+12-k<=4 and d=a+2-ell. Its
endpoints are disjoint from all seven fixed owners exactly when

    ell>=8, and if f=4 then d+z<=a+8.        (3)

If ell>=10, its exact increment is

    DeltaPhi=k-2-[f=4 and d+z>=a-4]
                  -[f=2 and d+z>=a+10].     (4)

At most one bracket is1, so this is at least k-3>=w+5>=17.
If ell=8, the exact increments are instead

    k=w+8:   DeltaPhi=1, with 4<=z<=14;
    k=w+10:  DeltaPhi=2-[z>=16];
    k>=w+12: DeltaPhi=k-w-8>=4.              (5)

Thus, after T0 and this NEXT consumer, the displayed package remains
below Q/D/W only for ell=8 with k=w+8 (any legal z<=14), or k=w+10
and z>=16. Its remaining difference is exactly-1 in both cases.
The small-z k=w+10 branch is neutral; every other right/interior-left/
escaped-left branch above repairs with positive margin. This classifies
the remaining LOCAL obstruction for every dimension of V. It does not
classify every possible third consumer before the prescribed T0, nor
arbitrary external owners or complete realizations.

Proof. The ell=4,6 bar positions collide with T0 even when f<=4.
For ell>=8 the bar is above T0 and the near leg is in the adjacent
column, leaving only the far leg's possible collision with Q. If f=4
that leg meets Q's horizontal near stem at row a+10 when d+z>=a+10.
Since the last row is odd, avoidance is exactly d+z<=a+8. For f<=2
there is no far-column endpoint collision with any fixed owner. This
proves (3), including all directions of the disjointness criterion.

For ell>=10 the near-leg seam is exactly the F3,Ev7 seam in (2).
If f=4 and the far leg reaches row a-4, the top contact tile(a-5,4)
contains T0's upper corner and two V far-leg endpoints, adding F0,Ev1.
Each subsequent contact tile(a-3,4),(a-1,4), if reached, adds F1,Ev2,
which cancels. There is no Q contact in this case because (3) leaves
one tile row before its near stem. If f=2, the only possible far-leg
contact is Q's tip at(a+10,3) in tile(a+9,2), reached exactly when
d+z>=a+10. It adds F0,Ev1: Q's reverse event meets its original
axial support. For f<=0 there is no far-column tile contact. Neither
far-column case shares any near-leg tile. This proves (4).

For ell=8 the lower bar at a-5 meets T0's upper bar at a-4. In the
central tiles with columns6,8,...,w+8 there are F1,Ev4 each. The
near end tile(a-5,w+10) adds F1,Ev3, and the three lower near-leg
tiles add F1,Ev2 each. If f=4, the far end tile(a-5,4) adds F1,Ev3,
the next far tile(a-3,4) adds F1,Ev2, and the final far tile(a-1,4)
adds F1,Ev2 exactly when z>=6. Thus

    Delta F=w/2+8+[z>=6], Delta Ev=2w+22+2[z>=6].

If f<=2 the far end tile(a-5,4) instead contains two V bar endpoints
and T0's upper corner, adding F0,Ev2. Its far leg is in a different
tile column. This gives Delta F=w/2+6 and Delta Ev=2w+19, plus
the one Q event exactly when f=2 and z>=16. Substituting the original
mass k-1 proves (5). Every shared tile is in the displayed partition;
there is no omitted width-dependent contact or separate rounding credit.

### An explicit chain through the narrow residual branch

For j=0,1,2 define the exact originals

    Tj=U(w+6+2j,6+2j,4),
    Tj(r,c)=(a-4-2j+r,w+11+j-c).

All nine owners Q,D,L,C,E,W,T0,T1,T2 are endpoint-disjoint. T1
consumes x; T2 consumes T1's original support (a+2,w+12), which
has T1 west and E south. Thus BOTH are genuine candidate consumers
of the next forced missing supports, rather than arbitrary placements.
The exact successive insertion counts into the common inventory are:

| Insertion | Delta S | Delta F | Delta Ev | Delta Phi |
| --- | ---: | ---: | ---: | ---: |
| T0 | w+5 | w/2+2 | 2w+8 | 1 |
| T1 | w+7 | w/2+8 | 2w+22 | 1 |
| T2 | w+9 | w/2+5 | 2w+19 | 0 |

All three have negative original charge 1-(w+6+2j), so Delta N=0.
The complete nine-owner partial package is still lower than Q/D/W
by1. Consequently even "each further forced consumer adds at least1"
is false for these partial source families. This is NOT a complete-model
or target counterexample. The Phi of the displayed instance remains
positive; the claim concerns a local difference, not its absolute sign.

Here is a general exhaustive shared-tile proof of the two new rows.
For T1, the shared bar tiles with T0 at lower row a-5 have columns
6,8,...,w+8. There are (w+4)/2, each contributing F1,Ev4. The two
end tiles at columns4 and w+10 each have three T1 endpoints and one
T0 endpoint, contributing F1,Ev3. Below them, the three shared near-leg
tiles with T0 at (a-3,w+10),(a-1,w+10),(a+1,w+10), and the one
shared far-leg tile (a-3,4), each contribute F1,Ev2. Summing gives
Delta F=(w+4)/2+6=w/2+8 and Delta Ev=2(w+4)+14=2w+22.

For T2, all shared bar tiles with T1 have lower row a-7 and columns
4,6,...,w+10. There are (w+8)/2, each contributing F1,Ev4. T2's
near column w+12 is now in E's far-column tile pair. Tile(a-1,w+12)
has two T2 endpoints and E's terminal: F0,Ev1, the sole direction
being E to T2. Tile(a+1,w+12) has two endpoints of each: F1,Ev2.
No other tile is shared with any old owner. In particular T2 and T1's
near columns, and their far columns3 and4, lie in DIFFERENT tile pairs.
Thus Delta F=(w+8)/2+1 and Delta Ev=2(w+8)+3, proving the last row.
The support exclusions in these small tiles are original exclusions;
an earlier source's consumption changes none of them.

There is no fourth member of this particular translated pattern:
T3 would have its near column w+13 and terminal(a+2,w+13), already
an E endpoint. T2's lateral terminal support there is ALREADY consumed
by E; E cannot be counted again as a new consumer or positive owner.
Instead closure exposes E's original axial support

    y=(a-1,w+13),

which is still absent and sees T2 west and E south. The three far-side
axial supports(a+1,5),(a-1,4),(a-3,3) are also absent, each with
its own Tj endpoint north and a preceding owner's endpoint east.
These four obligations must be resolved in any complete extension.
They do not imply four distinct owners or four independent credits.

## Scope and next step

The branching lemma and exact counts are general written arguments.
The [checker](../develop/check_secondary_ten_north_return_closure.py)
independently reconstructs original supports and actual event SETS,
including the exceptional tile types and all forced-support identities.
Its [receipt](../output/secondary-ten-north-return-closure-controls.json)
is finite corroboration, not an all-parameter proof. The separate
[Lean source](../formal/SubQuorum/SecondaryTenNorthReturnClosure.lean)
formalizes the unbounded nested/fixed endpoint separation, pending-support
absence and anchors, pre-consumed terminal and fourth-pattern collision.
It does NOT formalize the full U/rotor classification or event/tile counts.
Its scope and actual execution are recorded in the
[formal receipt](../output/secondary-ten-north-return-closure-formal-check.json).
This source was added after the independent review request; that review
does not establish Lean execution. Earlier ACCEPTs do not cover this note.

The remaining task is to resolve the actual consumers of y and the
far-side supports in one signed inventory, or prove a stronger
complete-family restriction. Arbitrary additional owners can add signed
external interactions and cannot be dropped. The unrestricted allocation
and rectangular-grid triple equality remain OPEN. The submitted manuscript
is unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
