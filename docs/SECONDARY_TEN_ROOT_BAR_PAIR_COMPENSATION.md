# A root and its forced bar-support owner have a nonnegative joint increment

22 October 2026. Continue the [short-return root theorem](SECONDARY_TEN_SHORT_RETURN_ROOT_COMPENSATION.md).
Retain immutable original endpoints, matchings and supports in the explicit
full even-U/standard-rotor model. U breadths are even and at least6; leg
depths are even and at least4. No catalogue exhaustion or existence of a
complete extension is assumed as a result.

## The joint theorem

Use H3,R,T,W and A of the preceding theorem, now at the maximal permitted
short depth D=h+4. Put

    H=H3+R+T+W+A,
    C=h+13, b=C-2, a=23-L, e=b-F.

Thus C,a,e are odd, L>=6 is even, and a<=17. Let an actual root owner
have the east form

    O=U(B0,30-t,f0), chart(t+r,C-1+c),
    t even<=22, B0>=6,f0>=4 even.                (1)

Its exact disjointness condition is t+f0<=24 if B0=6; otherwise there
is no extra far restriction. Write v0=t+f0 and

    delta0=1 if B0=6 and v0=24, otherwise0.

The previous theorem gives DeltaPhi(O|H)=1-delta0. In every complete
extension containing H+O, the original support x=(22,C-1) has a distinct
owner V. Every such owner is one of the complete original records

    EAST V=U(B,22-s,f), chart(s+r,C-2+c);
    WEST V=U(B,22-s,f), chart(s+r,C-c),           (2)

where s is even<=18 and B>=6,f>=4 are even. The exact legal frontiers
are stated below. There is no rotor alternative at x.

For EAST set v=s+f and define three indicators:

    eta=1 if B=B0+2 and v>=t;
    kappa=1 if B0=6, B=8 and v=24;
    chi=1 if kappa=1 and v0=24.                 (3)

Every other value of an indicator is0. The exact marginals are

    EAST: DeltaPhi(V|H+O)=1-eta-kappa+2chi;
    WEST: DeltaPhi(V|H+O)=2.                    (4)

Consequently every actual pair satisfies

    Phi(H+O+V)-Phi(H)>=0.                       (5)

For WEST the stronger lower bound is2. The EAST bound0 is sharp as a
partial-union identity. Formula (5) does not claim that either the pair
or its equality examples admits a complete extension. It remains valid
conditionally for every pair of these actual owners in such an extension.

## Why the next original is forced and normalized

The point x is O's original left bar-end support if t=22, and its original
even-row lateral support if t<=20. It is absent from H+O. Three neighbours
are endpoints of other originals:

    A:(22,C-2), O:(22,C), P0:(23,C-1).

Thus a complete extension must occupy x with a distinct original whose
only internal neighbour there is north. Every other endpoint of its
original matching is disjoint from H+O. This reasoning also applies if
that original was already among the additional originals of the extension.

In a full U, every degree-one endpoint is a leg tip. A rotor with its sole
internal neighbour north has, in both terminal patterns, the fork endpoint
(20,C-2). This belongs to A's vertical bar, whose row interval is a..22
and a<=17. Hence every rotor collides. The U tip is exactly x, its bar
lies at s=22-d with even d>=4, and leg exchange gives (2), preserving
the entire support and matching record. This argument has no size cutoff.

## Exact disjointness frontiers

For EAST, the bar's two rows must precede O's first row t, so s<=t-2.
Its far column J=C+B-2 is odd. These are the remaining exact conditions:

| Breadth | First possible collision | Additional restriction |
|---|---|---|
| B<=B0 | O's bar at row t | v<=t-2 |
| B=B0+2, B0=6 | K's far column at row25 | v<=24 |
| B=B0+2, B0>=8 | none | none |
| B>=B0+4 | none | none |

All A endpoints lie at columns<=C-2, strictly left of EAST V's minimum
column C-1. All remaining H endpoints are at rows>=22, except A, and
have maximum column C+6. O's aligned horizontal bar is the first obstacle
when B<=B0. In the adjacent case J=C+B0, the old far column is J-1;
the only older endpoint in J occurs when B0=6, at K's column C+6.
For B>=B0+4 the far tile lies beyond both O and H. These observations
prove necessity and sufficiency, including arbitrarily long far legs.

For WEST, the bar crosses both columns of A's vertical bar, so its two
rows must precede a. Exactly s<=a-3 is required. Its far column is
J=C-B, odd and at most b-4. There are three exhaustive phases:

| Far column | First old endpoint in J | Additional restriction |
|---|---|---|
| J>=e | A's far horizontal leg at odd row a | v<=a-1 |
| J<=e-2 and J>=-33 | W/A's contiguous row22 | v<=20 |
| J<=e-2 and J<=-35 | none | none |

The W/A row22 union occupies every column from-34 through b. Since J is
odd, its physical tile partner is J-1. In the last phase both tile columns
are left of that union and of A's far terminal; even J=-35 has no intratile
contact with W's first column-34. No later old body can be reached in the
first two phases without the displayed first collision. O lies strictly
east of WEST V, so these restrictions are also sufficient.

## Exact new receipts

Use the single fixed inventory of H+O. Put m=max(s,t), even, and
k=(22-m)/2. For EAST, s<=t-2, so m=t. For either orientation the new
near mixed full tiles are exactly the k+1 tiles with top-left coordinates

    (m,C-1),(m+2,C-1),...,(22,C-1).             (6)

The last has V in its upper-left cell, P0 in its lower-left cell and O
in both right cells. It is one three-owner tile. Every earlier tile has
only O and V. Before V, none of these tiles was full.

The new near events for EAST are

    O:(r,C)->V:(r,C-1), r=t+1,t+3,...,21;
    V:(r,C-1)->O:(r,C), r=t,t+2,...,22;
    P0:(23,C-1)->V:(22,C-1).                    (7)

There are2k+2. For WEST both horizontal directions occur at the odd rows
m+1,m+3,...,21, followed by the same P0-to-V event: there are2k+1.
All other directions target original supports. In particular V's south
direction at x targets its original axial support, while O-to-P0 at row23
already existed and remains old. These lists use the source's immutable
original support set; occupying a support does not convert an old excluded
direction into a new event.

WEST has no far receipt. At a terminal v=a-1, the two possible vertical
directions between V and A each target their source's original support:
V's axial support and A's even-parameter lateral support. The row22 phase
stops at most at20, across a physical tile-row boundary from row22.
All other WEST tile columns are separated from the old union.

For EAST, only the adjacent case eta=1 has a horizontal far band. Put
X=C+B0-1, even, w=min(v,v0), and j=(w-t)/2. Its new mixed full tiles
have top-left coordinates (r,X), r=t,t+2,...,w-2, and its new events are

    O:(r,X)->V:(r,X+1), r=t+1,t+3,...,w-1;
    V:(r,X+1)->O:(r,X), r=t,t+2,...,w.           (8)

Thus this band contributes2j-(2j+1)=-1. A final even row has both
endpoints but lacks the next-row pair, so it contributes an event without
a full tile. No upper bar contact is omitted: V's bar ends before row t.

If kappa=1 there is also the one event

    K:(25,C+6)->V:(24,C+6).                     (9)

Its reverse targets V's original axial support. If additionally chi=1,
the tile with top-left (24,C+5) becomes full: O owns its upper-left cell,
V the upper-right, and K both lower cells. It contributes+2 once.
The existing K:(25,C+5)->O:(24,C+5) event stays OLD. This is why the
correction in (4) is+2chi, rather than a second credit or event deletion.

The near and far tile columns are disjoint because B0>=6. The cap event
(9) is vertical and distinct from every horizontal event in (8). The
three-owner tile is absent from the j band tiles. Thus (6)--(9) are disjoint
sets of genuinely new physical tiles and source-labelled events.

For d=22-s, source counts give

| Orientation | Matching | Endpoint tiles | Inside original supports | Charge |
|---|---|---|---|---|
| EAST | B-1+(d+f)/2 | B/2+(d+f)/2 | (d+f)/2 | -1 |
| WEST | B-1+(d+f)/2 | B/2+1+(d+f)/2 | 4+(d+f)/2 | +1 |

Each has source contribution1 to Phi=N+S+2F-E. EAST's near contribution
is zero, WEST's is1. The far contribution is exactly-eta-kappa+2chi.
This proves every identity in (4) without invoking enumeration.

## The root pays the possible loss once

For EAST, chi=kappa*delta0, while all three other indicators lie in{0,1}.
Consequently

    DeltaPhi({O,V}|H)
      =2-delta0-eta-kappa+2*kappa*delta0
      =2-eta-(delta0+kappa-2*kappa*delta0)>=0,   (10)

because the parenthesized expression is0 or1. For WEST the increment
is3-delta0>=2. This uses only the root's genuinely new contribution
1-delta0. No old H3 or A reserve is assigned again.

The earlier exact baseline is Phi(H)=h+36-D/2=h/2+34 here. Thus the
two-owner extension preserves Phi>=h/2+34. The old inventory is counted
once. Further original owners and overlapping return groups can still
have interactions outside this selected pair; (10) is not their allocation
theorem and does not improve the global5/6 bound.

## Sharp loss and its precise meaning

For every permitted h,g,L,F choose the complete originals

    O=U(6,12,4), chart(18+r,C-1+c);
    V=U(8,6,8), chart(16+r,C-2+c).              (11)

They are endpoint-disjoint from H and each other, satisfy both forced-site
roles and have DeltaPhi(O|H)=+1, DeltaPhi(V|H+O)=-1. The joint increment
is0. Indeed V has five new full tiles and twelve new events, so its source
unit gives1+10-12=-1. For h=12 the successive selected totals are40,41,40.

Thus the endpoint-disjoint rule that each successive support consumer has
nonnegative marginal is false. The two-owner joint inequality survives and
is sharp. We do not assert a complete extension of (11), so this is not a
counterexample to a stronger rule that separately assumes such existence,
and certainly not a counterexample to the target global inequality.

## Verification and remaining scope

The companion verifier reconstructs every full source record, checks both
orientations and every displayed frontier against exact endpoint disjointness,
and compares the complete new tile/event sets with (6)--(9). It explicitly
preserves old events, tests the three-owner correction and checks (11).
Finite controls supplement the all-parameter written proof.

Run `PYTHONDONTWRITEBYTECODE=1 python3 develop/check_secondary_ten_root_bar_pair_compensation.py`.
The final controls pass256 U roles,110 equalities of complete normalized
records,8 rotor exclusions,2509 complete new tile/event sets,2085 collisions
and4 large width/height/far controls. They include8 negative second marginals,
19 zero joint increments and6 essential three-owner corrections.

`formal/SubQuorum/SecondaryTenRootBarPairCompensation.lean` passes18 explicit
declarations/15 local theorems under Lean4.33.0, with every declaration
individually axiom-audited and no warnings, sorry or native evaluation.
It checks the three blocked neighbours, forced north matching, rotor-fork
contradiction, parity/bar frontiers and exact joint budget arithmetic.
The complete original-record/terminal adapter, far-frontier geometry and
receipt-set enumeration are written proofs. Independent review completed
ACCEPT on task623a2234-8c76-4b42-b66c-12f513ae8fd6, original stream65748.
Its full response exactly matches the terminal receipt. It checked the
recursive prerequisites independently. A nonblocking checker issue is now
fixed: candidate bars are restricted to s<=18, excluding incident depth2
outside the model. The updated in-scope counts above replace2529/2121;
the formulas, negative marginals and sharp example are unchanged.
The earlier root review also completed ACCEPT on its original stream92280.

The remaining branches include nonmaximal D, west root owners, later forced
supports and nonreusing budgets across multiple return groups. Arbitrary
complete-family allocation, catalogue exhaustion, global5/6 improvement and
rectangular-grid triple equality remain open.
