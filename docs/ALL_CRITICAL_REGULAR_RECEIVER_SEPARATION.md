# All critical points avoid every first and LONG receiving tile

20 October 2026. Complete original-owner geometry excludes the apparent
critical/other-corner coincidence left by endpoint tags alone. This applies
to ALL critical second points, whether their original owner is a U in any
effective phase or a rotor. Their physical receiving tiles are disjoint
from ALL first/LONG receiving tiles. Critical receiving tiles are not proved
mutually distinct. Combining this separation with the exact phase01 return
capacity gives one joint endpoint ledger, with no repeated positions or
reserve. The full coefficient-one allocation and grid equality remain OPEN.

## 1. Standing hypotheses and the remaining three cases

Use the same complete original U/rotor sources, legal even U dimensions,
original endpoint uniqueness, retained original supports, selected occupied
degree at most one and transported physical tile partition as
[the critical point theorem](PHASE11_CRITICAL_CONTINUATION_AND_ALL_OWNER_COUNT.md).
The first/LONG receiver theorem and global critical/first/LONG forced-point
injection are inherited with their full hypotheses. Owner recurrence and
open port components are allowed.

Normalize a critical point t to0 and its frame to(N,E). Its tile is

    Q={(0,0),(1,0),(0,1),(1,1)}.

Its active original phase01 source O has endpoints(-1,-1),(-1,0),(-1,1),
all tagged N. Its first original phase11 owner F has endpoints(0,-1),(0,-2),
tagged none. These are the established complete critical stencil. In
particular the north and west neighbors of t belong to owners other than
t's owner G.

Suppose Q also receives a first or LONG point x, with frame(s',d'). Those
receivers have an exact original phase01 pair of their active owner and
the four active tags at -s'-d',-d',s'-d',2s'-d' relative to x. The other
original owner is a U: phase01 passive at a first event, phase11 corner at
a LONG event. It supplies x-s' and x-s'+d'.

The global forced-point theorem gives x!=t. Exhausting the eight cardinal
frames and the other three tile corners, their actual tile sets and these
tags leaves exactly:

| Case | x | (s',d') | Active original pair | Other U's endpoints |
|---|---|---|---|---|
| A | (1,0) | (N,W) | (0,1),(1,1) | (2,0),(2,-1) |
| B | (1,1) | (N,E) | (0,0),(1,0) | (2,1),(2,2) |
| C | (0,1) | (W,N) | (1,0),(1,1) | (0,2),(-1,2) |

This finite orientation classification is exhaustive by the definition of
cardinal frames; it places no bound on dimensions, number of sources or
lattice placement. Tags alone permit these cases, which is why the older
partial stencil was not a counterexample to geometric separation.

## 2. Case B contradicts the phase01 owner's original full profile

In case B, t belongs to the ordinary active pair. Original endpoint
uniqueness identifies G as that phase01 source. The two foreign critical
anchors north/west, and the pulled origin parity of Q, force G to own t
as an upper outer bar corner, by
[the phase01 return role theorem](CRITICAL_PHASE01_BAR_RETURNS.md).
Its original profile in Q is therefore full4P0T. The ordinary active
source's exact profile in Q is2P1T. One fixed original source cannot have
both profiles in the same fixed tile. Thus case B is impossible.

## 3. Cases A and C contradict the complete owner of t

Consider A. The ordinary active source has t outside its exact original
pair, so it differs from G. Thus G has NO original endpoint at any of

    (-1,0), (0,-1), (0,1).                                    (1)

If G is a U, any nonterminal stem point has two opposite original endpoint
neighbors, and every inner/interior bar point has at least three. An upper
outer bar corner has two perpendicular original endpoint neighbors. Only
the south neighbor is available under(1), so t must be a terminal with
its incident stem pointing south. Its legal incident height is at least4.
In exact canonical coordinates, for either leg and either reflection,

    G owns (2,0),    G does NOT own (2,-1).                     (2)

The first assertion is the second stem point. At that distance from the
terminal the canonical row is incidentHeight-2>=2, so it is still a stem
point, not a bar; width>=6 separates the other stem. This proves the second
assertion. The formal statement derives(2) directly from the three blocked
neighbors by an arbitrary-dimension endpoint-role proof. It needs no phase
or parity assumption about G.

But the ordinary other U owner D owns BOTH (2,0),(2,-1). Original endpoint
uniqueness at(2,0) forces D=G, contradicting(2). This handles ALL four U
phases without assuming that either owner is fresh.

If G is a rotor, a central endpoint has three original endpoint neighbors
and cannot satisfy(1). Thus t is a tip whose central neighbor is south.
The rotor's central2x2 square contains (2,0). One can also check this
directly over the two rotor chiralities and their eight original endpoint
roles, which exhaust all translations owning t by quarter-turn symmetry.
The ordinary D is a U and G is a rotor, so they are different original
source indices. Their shared endpoint(2,0) is impossible.

Case C is A with the two coordinate axes exchanged. Its ordinary active
pair makes the south neighbor foreign too. A U owning t has a terminal
stem pointing east and owns(0,2) but not(-1,2), contradicting D's two
endpoints. A rotor owns(0,2), again contradicting the distinct U owner D.
All three cases are excluded.

We have proved that NO critical second point lies in ANY first/LONG
physical receiving tile. Because aligned tiles form a partition, the
critical receiving tile is consequently different from every first/LONG
receiving tile. This does not prove injection among critical tiles, and
does not restore the false critical closed-owner exclusion.

## 4. A single count with closed returns and external exits

Choose a set C of original phase01 owners on closed specified neutral
components, and write P_C for their original endpoints. Keep the same
first/LONG event family as before, with counts C01,L11,J=J01+J11 and
additional endpoint set X. The accepted theorem gives

    |X|+J=2(C01+L11),   X intersect P_C=empty.

Split a chosen critical event family into Kc points owned by C and Ke
points not owned by C. Their points are globally injective. Let Ye be
the Ke external points and Vc the union of the four original endpoints
in each Kc receiving tile. The phase01 bar-return theorem gives

    Kc<=2|C|,  |Vc|=4Kc,  Vc subset P_C.

Every tile in Vc is disjoint from every ordinary receiver. The new theorem
also separates Ye from every ordinary receiver, and ownership separates Ye
from Vc. Hence all three sets are pairwise disjoint and

    |X union Ye|+J=2(C01+L11)+Ke,
    (X union Ye) intersect P_C=empty;                          (3)
    |X union Ye union Vc|+J=2(C01+L11)+Ke+4Kc.                 (4)

Use the SAME B+J<=2A+H ledger once. Equations(3)--(4) yield respectively

    |X union Ye|+2A+H >= 2(C01+L11)+Ke+B,
    |X union Ye union Vc|+2A+H >= 2(C01+L11)+Ke+4Kc+B.          (5)

All terms use their actual, jointly chosen physical families. Each owner in
C contributes to Vc through at most its two labelled upper outer bar corners.
No H or cap/singleton
reservation is spent twice, and neither Vc nor a critical point is declared
a reserve payment.

Within one qualifying nonexceptional AA full endpoint component, select
ell closed curves and the associated first/LONG events. The direct H
packing gives J=0, and the established turning bound gives C01>=4ell.
For critical events and receiving owners in that SAME endpoint component,

    |X union Ye|>=8ell+2L11+Ke outside P_C,
    |X union Ye union Vc|>=8ell+2L11+Ke+4Kc.                   (6)

The external endpoint bound improves the preceding8ell+2L11 by Ke. Returns
to C add their actual full-bar endpoint tiles to the JOINT count instead;
they are not incorrectly counted as external. A need not vanish.

## 5. Formalization, controls and remaining theorem

Nine new scoped Lean declarations compile and their nine axiom prints
pass. With the preceding phase01 return result, all19 statements are
recorded in [the formal receipt](../output/critical-bar-regular-separation-formal-check.json).
Controls check all32 normalized frame/point possibilities, with8 actual
same-tile cases,2 excluded by the inherited forced-point separation, and
exactly3 tag-compatible remaining cases. They also check14,400 original U
endpoint images,144 downward terminal survivors and all16 rotor translations
owning the origin, with2 three-blocker survivors. See
[the control receipt](../output/all-critical-regular-separation.json).
Independent review13288890-8893-4d75-ae5a-c48f772e87c3 completed ACCEPT
on20 October at10:49:47 UTC, observed gpt_6/pro. It checked this new theorem,
the original-owner/profile/parity adapters and equations(3)--(6) under the
explicit inherited hypotheses. See [its own receipt](../output/all-critical-regular-separation-review.json)
and [full response](../output/all-critical-regular-separation-review-response.txt).
Its suggested clarification restricts the two-bar-corner wording to owners
in C, as now stated above. This is independent mathematical/source review,
not execution certification, a seven-source-family audit or a proof of the
remaining unrestricted allocation.

[`CriticalRegularReceiverSeparation.lean`](../formal/SubQuorum/CriticalRegularReceiverSeparation.lean)
formalizes the exhaustive normalized three-case catalogue, arbitrary legal
U terminal two-step stencil, complete rotor-root catalogue, owner-collision
implications and exact count/shared-H/AA algebra. The physical normalization,
other-owner U type, original exact pair/full profiles and axis-exchange
adapters are written in Sections1--3. It does not assume a fresh owner or
the desired receiver separation as a premise. The full unrestricted
allocation is not a formal consequence claimed here.

The seven-source family in the preceding note gives actual complete
critical returns to the same closed owner, while demonstrating no collision
with its ordinary receiving tiles. Its endpoint count12 equals four ordinary
additional positions plus eight original bar-tile endpoints. It provides
no complete other-phase-critical or AA control. General separation in
those branches follows from the owner-role proof above, not from that
fixture or a bounded dimension search.

The remaining full goal is a compensating CHARGE inequality. Original full
bar tiles already belong to the source ledger; their4Kc endpoint positions
cannot simply be added to R. Critical receiver overlap with each other,
phase10/phase11 terminal continuations and rotor exits must still be
accounted for through the original cap/singleton/H reservations. Equations
(3)--(6) remove a specific reuse obstruction without asserting that missing
global inequality.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
