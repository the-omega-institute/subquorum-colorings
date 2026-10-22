# No standard rotor in a complete six-row full-U/rotor pocket

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and main theorem

Use exactly the complete six-row pocket hypotheses of
`SIX_ROW_CEILING_DESCENT.md` and `SIX_ROW_ALL_PHASE_HORIZONTAL_BUDGET.md`:

* P=[0,5] x [0,N-1], N even, with its old occupied endpoint boundary
  and no old endpoints inside P;
* every new original is an immutable full canonical U(B,d,f), even
  B>=6,d,f>=4, or standard rotor, wholly confined to P;
* new endpoint sets are pairwise disjoint and individually connected;
* every original support not consumed by an actual endpoint remains
  occupied, and every retained support inside P has exactly one occupied
  neighbour.

The full-U/rotor decomposition is an assumption. The preceding accepted
ceiling theorem is used as a geometric input: boundary H0/H5 are excluded;
the remaining H1/H4 projections contain NO foreign endpoint in any row,
including the extreme row that H itself does not occupy. The only U types
are consequently those H and transverse V=U(6,d,f), whose bars fill all
six rows and whose even-depth stems occupy rows0,5.

**Theorem. No standard rotor occurs in P.**

This holds for arbitrary pocket width and arbitrary U depths, directions
and column phases. There is no finite-width extrapolation in its proof.
The key is a closed top-row interval, followed by a bottom-tip parity
contradiction. We then exclude the middle row phase separately.

As a consequence the previous all-phase rotor-free budget now applies to
EVERY complete pocket in this assumed source model. In the notation of
that note,

    Phi(P)>=a+2b+sum_H(B_H-1)+u,    u=b-2p-c>=0.          (1)

An empty pocket has Phi=0. Every nonempty complete pocket has Phi>=2;
if it contains any horizontal H, Phi>=5. The corresponding established
spanning-upward-U chamber increments are at least5,7,10 respectively.
The nonempty bound2/7 is sharp in the locally complete two-V families for
every even original chamber width W>=12. These claims control all new
originals in that chamber pocket, not just selected compensators.

The general source decomposition, other gate/chamber branches, exterior
inventory and unrestricted global5/6 improvement remain open. This is
not yet the rectangular-grid triple equality or a complete global result.

## Two shape facts and ownership inside a rotor projection

Normalize a rotor's left column to0. The two endpoint shapes are

    A={(0,1),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,2)},
    B={(0,2),(1,0),(1,1),(1,2),(2,1),(2,2),(2,3),(3,1)}.

All dihedral images normalize to one of these. A rotor has top row0,1
or2. Every endpoint at its top row has an endpoint immediately below it.
The original supports of A are

    {(-1,1),(0,0),(0,3),(1,4),(2,-1),(3,0),(3,3),(4,2)},

and those of B are

    {(-1,2),(0,0),(0,3),(1,-1),(2,4),(3,0),(3,3),(4,1)}.

Translate both lists with the rotor. These are the complete immutable
records, not supports recomputed after fusion.

No V bar can occupy ANY column of a rotor projection: each of its four
columns contains some rotor endpoint and a V bar fills all rows in either
of its columns. No H projection can contain a column of the rotor
projection, by the accepted no-foreign-endpoint property for H. In
particular an actual consumer at a point in a rotor projection cannot
be an H or V bar. It must be a V stem at row0/5, or another rotor.

For A at top0, no other rotor confined to rows0..5 and disjoint from A
can own any of (0,0),(0,2),(0,3). Indeed such a rotor must also have top0.
If its top endpoint is at column z, its normalized left column is z-1
for shape A, or z-2 for B. The following explicit collisions exhaust
the three possible z, without a translation bound:

| z | Other A collision | Other B collision |
|---|---|---|
| 0 | (1,1) | (2,0) |
| 2 | (1,2) | (1,1) |
| 3 | (1,3) | (1,1) |

Thus these points, when forced, can be consumed only by V stems.

## A top0 rotor forces the entire top row between two V bars

First suppose A has top0 and left0. Its supports (0,0),(0,3) are inside
P. Each has its own rotor endpoint neighbour and the old boundary
neighbour above. Completeness forces both points to be actual endpoints.
The preceding owner classification leaves only V stems.

The V owning (0,0) must approach from the left, since a stem from the
right would pass the existing rotor endpoint (0,1). Its top tip is exactly
0; extending any farther also hits (0,1). Call it V_left, with bar start
ell and even top depth f_left. Thus

    ell+f_left=0,             ell even.                  (2)

The V owning (0,3) must approach from the right, since an approach from
the left crosses (0,1). Its top tip is2 or3; it cannot be<=1 or>3.
Call its bar start r. These two V sources are different, since one
stem owning both points would contain (0,1).

The full-height bars at ell,ell+1 and r,r+1 are walls. Every other
source owning a point strictly between them stays in that gap, by
connectedness and six-row confinement. No source outside can cross a
wall to supply an endpoint inside. This includes arbitrary U depths.

The right tip cannot be3. In that case its immutable beyond-tip support
z=(0,2) has its own endpoint neighbour (0,3) and the old boundary above,
and must be consumed. H and V bars are excluded at column2 by the rotor
projection, and another rotor is excluded by the shape table. The two
existing V stems do not contain z. Nor can a third V supply it: any
third V bar inside the two walls needs two adjacent row0 points, whereas
the existing sources already fill that row everywhere in the gap except
column2. A bar outside the walls cannot send a connected endpoint path
to z without hitting a wall. Thus there is no actual owner of z.

Consequently the right top tip is2. If its even top depth is f_right,

    r+1-f_right=2,           r odd.                     (3)

Now EVERY row0 point strictly between the walls is an endpoint: V_left
covers through column0, A owns column1, and V_right covers from column2
to its bar. Hence:

1. There is no further V bar in the gap, because its row0 endpoints
   would collide with existing endpoints.
2. There is no further rotor with top0, because its top endpoint would
   collide with those already occupied row0 points.
3. There is no H in the gap. Its projection would contain a foreign
   row0 endpoint, contradicting the ceiling theorem. This applies to
   both H phases, including H4 with only two row0 leg endpoints.

All remaining possible sources strictly in the gap are therefore rotors
with top1 or2. The only V endpoint owners in the gap are the two wall
sources' stems.

## Exactly one lower-rotor role can survive the filled top row

Take any rotor with top2 in the gap and let v be its left column. Its
top endpoint is at column v+1 for A, or v+2 for B. The point immediately
above it, at row1, is its immutable original support. Its upper neighbour
on row0 is occupied by the filled top row, while its lower neighbour
is that rotor's top endpoint. Completeness therefore forces this support
to be an actual endpoint.

It cannot be owned by a V bar or H, since neither exists in the gap, or
by a V stem, since it is at row1. A top2 rotor cannot reach row1. A
top1 rotor owning that row1 point has its own endpoint directly below
it, colliding with the current top2 rotor. The only remaining owner is
the ORIGINAL A at top0: all other top0 rotors were already excluded.

The support column must thus lie in {1,2,3}, the original A's row1
endpoint columns. The candidate lower left ends are precisely

    A at v=0,1,2;       B at v=-1,0,1.

All but A at v=2 collide with the original A:

| Lower candidate | Collision with original A |
|---|---|
| A, v=0 | (2,1) |
| A, v=1 | (2,2) |
| A, v=2 | no collision |
| B, v=-1 | (2,1) |
| B, v=0 | (2,2) |
| B, v=1 | (3,2) |

Thus there is at most ONE top2 rotor in the entire gap, namely A
translated by (2,2). Its only row5 endpoint is (5,4). It may itself
collide with the V stems; allowing it regardless only weakens the
exclusion we prove next. Top1 rotors have no row5 endpoints.

## Bottom parity gives the contradiction

Let the two even bottom depths be d_left,d_right and their bottom tips

    x=ell+d_left,       y=r+1-d_right.

By (2),(3), BOTH x and y are even. Their two bottom stems must be
endpoint-disjoint, so x<y and therefore x+1<y. The point

    s=(5,x+1)

is V_left's immutable beyond-tip support, strictly inside the wall gap.
Indeed d_left>=4 places it past the left bar, and d_right>=4 with x<y
places it before the right bar. It has its own endpoint neighbour (5,x)
and the old boundary neighbour on row6. Completeness forces an actual
owner.

Neither existing V stem contains s, and there is no further V or H in
the gap. No top0/1 rotor reaches row5. The only possible top2 rotor
has its sole row5 endpoint at column4. But x is even, so x+1 is odd
and cannot equal4. There is no owner, a contradiction.

This excludes A at top0. Horizontal reflection interchanges A and B
and preserves the full-U even-depth model and retained-support condition,
so it excludes B at top0 as well. Reflection in row5/2 then excludes
both shapes at top2. No column phase or width bound was used.

## The middle phase has no possible corner consumer

Only top1 rotors remain. Consider one with left0. Its support immediately
above its top endpoint is (0,t), where t=1 for A and2 for B. This support
has the old boundary neighbour above and the rotor endpoint below, so
it must be consumed. Boundary-phase rotors have been excluded; H and
V bars are impossible at its projection columns. Hence a V stem owns
(0,t).

A V bar cannot meet the four-column rotor projection. A right-facing
stem reaching t from a bar strictly to the left must also cover column0;
a left-facing stem from a bar to the right must also cover column3.
In the first case the rotor's corner support (1,0), and in the second
(1,3), has two endpoint neighbours: the row0 V endpoint above and its
own adjacent rotor endpoint on row1. The support must be consumed.

It is at an interior row and rotor projection column, so the only
possible consumer is another rotor. Every rotor now has top1. If its
top endpoint is at the relevant corner, the two endpoint shapes give
the following unavoidable collisions, again with no translation cutoff:

| Current shape | Corner column | Other A collision | Other B collision |
|---|---|---|---|
| A | 0 | (2,1) | (3,0) |
| A | 3 | (2,3) | (2,1) |
| B | 0 | (2,0) | (2,0) |
| B | 3 | (3,3) | (2,1) |

No consumer is possible. This excludes both top1 shapes and completes
the general rotor exclusion.

## Whole-pocket consequences and nonreuse

Apply the independently accepted all-phase H/V theorem to the entire
remaining family. It classifies every source charge, mixed full tile
and source-labelled event, with immutable supports; its disjoint V
classes yield (1) without spending any surplus twice. The new exclusion
does not remove endpoints and then assume completeness; it proves that
there were no rotors in the original complete pocket in the first place.
Thus the completeness premises used by the H/V theorem are intact.

If any H occurs, its mass B-1>=5 makes Phi>=5. If H is absent, every
source is transverse V and the accepted singleton exclusion forces at
least two sources in any nonempty complete pocket, giving Phi>=2.
The actual two-V complete local families attain2 at every even N>=10.
The established chamber identity Delta=5+Phi then gives the stated5/7/10
bounds. These cover arbitrary numbers of all-source additions and remove
the V/rotor residual gap for this particular six-row pocket model.

This does not establish the sign of the exterior contribution, classify
all wider gate choices, or justify a full-U/rotor decomposition for every
grid configuration. No unrestricted global coefficient improvement or
rectangular-grid equality is claimed. The submitted manuscript stays
unchanged until a separately reviewed addendum is appropriate.

## Checks and formalization scope

`develop/check_six_row_rotor_exclusion.py` reconstructs full canonical
records. It checks all six boundary-anchor roles, all six lower upper-
support roles and their unique survivor, all eight middle-corner roles,
142 disjoint closed-top V pairs,16 wrong-tip controls and36 middle-stem
controls, including depth2000. These are controls of the explicit shape
identities and interval reasoning, not finite-width proof of the theorem.
The final verifier also checks all eight normalized FULL original records
and both reflections, including supports and matching edges. These extra
controls were added after audit submission, without changing the proof.

`formal/SubQuorum/SixRowRotorExclusion.lean` checks normalized shape
collisions at arbitrary integer translations, the unique lower role,
the top-endpoint neighbour, both V bottom parities, forced bottom gap,
and the resulting numerical pocket/chamber implications. Full canonical
adapters, completeness-to-actual-owner reasoning, connected-wall confinement
and the source-to-inventory assembly remain written proofs.

Execution and independent review are recorded in
`output/six-row-rotor-exclusion-validation.json`. The older all-phase
budget audit does not cover this new rotor exclusion.
