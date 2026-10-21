# A short return with a four-step incident leg cannot be completed

21 October 2026. This removes an entire residual return class at arbitrary
incident width, rather than adding another numerical resource. In the
complete original-source model, maximal X with far leg4 and the prescribed
short return Q=U(6,8,4) have NO complete U/rotor extension. The proof forces
a unique rotor, which Q then traps around an original support in a one-row
cavity. The analogous far leg6 branch and the unrestricted allocation/grid
objectives remain OPEN.

## 1. Model and theorem

Use the finite complete original U/rotor model of the
[opposed-stem theorem](OPPOSED_STEM_SUPPORT_GAP_OBSTRUCTION.md). Original
endpoint ownership is unique and original matchings do not change. Every
unconsumed original support remains selected with its original anchor as
its sole occupied neighbor; consuming a support leaves it occupied as an
endpoint. Optional selected points have no endpoint neighbor. U widths are
even and at least6, their independent legs even and at least4; rotors are
the two chiral original footprints, up to lattice symmetries. Every source
endpoint graph is connected. U and rotor require at least five and four
rows respectively, in every orientation. No fresh-owner assumption is made.

**Theorem.** Suppose two prescribed original sources have frames

    X=U(b-2,a,4), X(r,c)=(c+2,r+3),
    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    b>=8, a>=4, with legal even b,a.

Their original endpoints are disjoint. They have no complete extension by
any finite number of original U/rotor sources of arbitrary legal dimensions.
The statement does not need A/B/C or a marking assumption. Thus in the
actual maximal Vcorner chain it excludes this return whenever k=4, for
every b, including b>=12. It does not exclude k=6.

## 2. A forced consumer has exactly one possible footprint

Put w=(b,8). This is Q's original near-leg inner support, intrinsic (3,2),
with anchor (b+1,8). X owns the west neighbor (b,7). Hence retaining w as
a nonendpoint would leave two distinct occupied neighbors; completeness
forces w to be an original endpoint. Neither X nor Q owns it. Therefore
its consumer differs from both named owners, before using their endpoints
as blockers. The west and south neighbors of w are unavailable to that
consumer, so its own endpoint neighbors lie only north/east.

The U catalogue is exhaustive here: interior bars and inner corners have
three own neighbors; nonterminal straight legs have two opposite own
neighbors. Only north/east terminals and the two outer-corner orientations
remain. A north terminal of incident length>=4 crosses Q's far endpoint
(b-4,8). An east terminal of incident length>=4 crosses Q's bar endpoint
(b,10). A vertical outer bar extending north has width>=6 and crosses
(b-4,8); a horizontal outer bar extending east crosses (b,10). These
arguments allow arbitrary width and the other leg, and allow exchanging
leg labels. Thus no U can own w.

Every rotor nontip has three own endpoint neighbors, so a rotor must have
a north/east tip at w. The four distinct tip footprints comprise two north
tips and two east tips. Three contain (b-1,10), a Q endpoint. The sole
remaining footprint R has endpoints

    (b-3,7),
    (b-2,7), (b-2,8), (b-2,9),
    (b-1,6), (b-1,7), (b-1,8),
    (b,8).

It is the canonical rotor translated by (b-4,5). Its original matching is

    (b-3,7)--(b-2,7), (b-2,8)--(b-2,9),
    (b-1,6)--(b-1,7), (b-1,8)--(b,8).

This classifies an actual consumer, not an endpoint-only guessed successor.

## 3. The forced rotor is itself incompatible with Q

More generally, for any translation parameter b, prescribed Q and the
displayed R alone have no complete extension. Their endpoint sets are
disjoint, but fill the entire boundary of

    D=[b-4,b-2] x [7,10].

Q supplies the top and right. R supplies the bottom except its Q-owned
right corner and the left except its Q-owned top corner. Neither source
has an endpoint strictly inside. The strict interior consists of only
(b-3,8) and (b-3,9), on ONE row.

Use Q's original far-leg support q=(b-3,8), intrinsic (3,5), with anchor
(b-4,8) and the additional R neighbor (b-3,7). Hence q must be consumed.
Neither Q nor R originally owns q. This uses only Q's original support
rule and R's displayed endpoint set; no rotor support convention is needed.
As an additional check, p=(b-3,9) is also an original R support, with anchor
(b-2,9) and the additional Q neighbor (b-4,9), but it is not needed.

Any foreign source entering this strict interior is confined by its
connected unit-edge endpoint graph: a path leaving must pass through an
already owned boundary endpoint. No original U or rotor fits in a single
row. Thus no foreign consumer exists, a contradiction. This proves the
Q/R obstruction and then the X/Q theorem. Arbitrary extra sources cannot
change it; repeated owner names cannot bypass exact original ownership.

## 4. Consequences and precise remaining scope

The [earlier support-gap note](OPPOSED_STEM_SUPPORT_GAP_OBSTRUCTION.md)
proved permanent lower pairs for Q=U(6,8,4), k in {4,6}, b in {8,10}.
Its k=4 subcase is now known to have no complete instance; that conditional
pair theorem remains true, but does not create a resource in a realized
family. Its previous necessary north-terminal escape at b>=12 is now
relevant only to k=6 in this short-return class.

No reserve unit, positive activation, demand or physical pair is added for
the excluded k=4 occurrences. Existing H/W10/short-saturated joint resource
unions and the ledger mu=N+R-G are unchanged. N still counts positive
owners only. Any reduction of the residual demand set must classify an
actual complete family before accounting; an impossible stencil is not a
second compensation receipt. Consequently this is a structural exclusion,
not a universal improvement of the5/6 bound or a proof of the full target.

The k=6 case is genuinely outside the argument: w=(b,8) is then already
an X endpoint, so it need not acquire a new consumer. The point (b,10)
must not be substituted for w: it is a Q endpoint, not an original Q
support. Continue the k=6 north-terminal escape and other return dimensions,
nonmaximal corners and occupied adjacent bands. No complete Vcorner
realization is asserted. Submitted manuscripts and primary C4-free results
are preserved.

## 5. Verification

The [independent checker](../develop/check_short_return_rotor_cavity.py)
PASSes24 forced-consumer patterns, b=8,10,12,16,24,40 and a=4,6,20,52:
zero U consumers and exactly the displayed R each time. Endpoints, original
supports and matching agree separately. Six translated Q/R cavities,
including negative and odd translations, and all four rotor tip footprints
pass. Controls also check why the k6 forcing argument is unavailable.
The bounded U role library stops at18 and does not replace the written
unbounded catalogue proof. See the [control receipt](../output/short-return-rotor-cavity-controls.json),
session37329 exit0.

All22 standalone Lean4.33.0 declarations PASS, finalsession5748 exit0.
Before invocation the authorized local Mac had45% free memory and no
actual lean/lake executable by comm basename. Individual axioms are only
propext, Classical.choice and Quot.sound, no sorry/native. The first run's
two tactic/unfolding issues were repaired before this complete check;
the failed run is not validation. The [formal source](../formal/SubQuorum/ShortReturnRotorCavity.lean)
proves the Q/R contradiction over an arbitrary owner family using only Q's
support retention, as well as the X/Q composition under explicit endpoint
catalogue and Q-support-retention adapters.
Actual orientation adaptation to that catalogue remains written. See the
[formal receipt](../output/short-return-rotor-cavity-formal-check.json).

Independent written audit6f8a1da8 ACCEPTS the full arbitrary-dimension X/Q
theorem, standalone Q/R cavity, all endpoint roles, repeated-owner exclusions
and k6/accounting limitations. The13233-character answer exactly matches
originalstream85949 exit0 and the completed API, [DONE], no errors, observed
gpt_6/pro. The reviewer could not retrieve the relatively linked earlier
note, so distinguished the rotor support catalogue from endpoint geometry;
the accepted Q-support witness makes that catalogue unnecessary. This
editorial strengthening is now in both the written and formal proofs,
followed by the complete22-declaration Lean recheck. Execution, historical
ledger dependencies, realizability and the full target are not certified.
See the [full response](../output/short-return-rotor-cavity-review-response.md)
and [review receipt](../output/short-return-rotor-cavity-review.json).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
