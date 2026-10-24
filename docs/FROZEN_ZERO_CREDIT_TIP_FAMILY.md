# Fully frozen tip events with no residual square credit

20 October 2026. A connected three-module family has one minus-one tip
event, no new aligned full tiles and no regular intratile events. Thus
K_minus_one=1 while J=K_regular=C=0, even under complete freezing. This
refutes paying every tip event from the global unused regular square
credit, including payment transported from arbitrarily distant tiles.
The original negative-module mass pays the event without violating the
target inequality. Separated copies make the pure-credit deficit unbounded.

The independent review of the preceding joint witness theorem suggested
the reference three-module construction. We reconstructed it independently,
proved the parameter extension and complete freezing below, and verified
the reference coordinates and its complete freezing certificate in Lean.
The review's ACCEPT covers the earlier joint theorem; it is not an ACCEPT
of this later family or freezing proof.

## 1. The family and exact statement

Use the COMPLETE constructor U(W,a,b) and support lists from
MINUS_ONE_TIP_EVENTS_AND_LOCAL_OVERLOAD.md. All six parameters below are
even and satisfy

    W,w >= 6, b,k >= 4,
    a >= max(b+4,w+4), h >= W+k+2.                 (1)

Take three original modules, with their transported original matchings:

    A   = U(W,a,b),   (r,c) -> (r-a,c-1),
    H_1 = U(w,h,k),   (r,c) -> (c-1,h+1-r),
    H_2 = U(w,h,k),   (r,c) -> (-c,h+1-r).

The original endpoint sets are pairwise disjoint. All three original
charges are -1. Form the complete retained-support union. It is feasible,
connected and fully frozen under the matching-promotion model: no
nonempty oriented bundle of these matching edges can promote endpoints
to selections and discard their mates while retaining the existing T.

For every parameter choice (1),

    N=0, B_minus=3, R_minus=G=0,
    J=K_regular=C=0, K_irregular=K_minus_one=1,
    rho_final=-2, finer guaranteed slack=2.       (2)

After common translation (a,2), an ambient rectangle is

    (a+w+2) by (h+4).

The exact cardinalities are

    |M| = W+2w+(a+b)/2+h+k-3,
    |P| = 2|M|,
    |T| = a+b+h+2k+1.                           (3)

Here B_minus counts charge-minus-one U modules, R_minus counts negative
rotors, and K_minus_one counts irregular events sourced from the former.
There are no rotors in this family. Write sigma=mn/2-|T|-|M| and let D
be the sum of 2 minus the selection count over endpoint-free physical
tiles. Every selection retains its endpoint anchor, so final feasibility
excludes adjacent selections and D>=0. Splitting all tiles gives the
exact identity sigma=D-rho_final.

The reference W=w=6,a=10,b=4,h=12,k=4 lies in an 18-by-16 rectangle
with |P|=76, |M|=38, |T|=35 and actual half-area slack71.

## 2. Endpoint separation and complete support retention

Before the common translation, A's bar occupies rows -a,-a+1 and
columns 0,...,W-1. Its long leg ends at p=(0,0); its short leg ends
at row b-a<=-4, column W-1. The two horizontal long legs occupy

    H_1: row 0, columns 1,...,h-1;
    H_2: row -1, columns 1,...,h-1.

Their bars occupy columns h,h+1, respectively at rows 0,...,w-1
and -w,...,-1. Their short legs occupy rows w-1 and -w, with columns
h+1-k,...,h-1. These endpoint sets are disjoint. The vertical long leg
lies in column zero; its bar is above the remote horizontal short leg
by (1), and its short leg does not reach rows -1 or 0. The remote
horizontal bars and short legs lie to the right of A's endpoints.

Exactly these original support incidences become endpoints:

    A:   {(-1,1)},
    H_1: {(-1,c): c=1,3,...,h+1} union {(0,0)},
    H_2: {(0,c): c=1,3,...,h+1} union {(-1,0)}.    (4)

No other support is deleted. In particular, H_1's retained long-leg
inward supports lie at (1,c), c=2,4,...,h-2; those of H_2 lie at
(-2,c) with the same even columns. The nearest such sites to A are
(1,2),(-2,2), each at distance at least two from every non-anchor
occupied A site. A's retained inward supports nearest this interface
include (-3,1) and its lower-tip support (1,0); these are also at
distance at least two from the other retained supports.

For the remote interfaces, a>=w+4 separates A's bar from H_2's outer
short-leg supports. The inequality h-k>=W+2 separates all remote
horizontal short-leg supports from A's rightmost occupied column W.
The remaining possible approach is between H_2's row -2 inward supports
and A's short leg. Its endpoint rows are at most -4. If its below-tip
support reaches row -3, that support has odd column W-1, whereas the
row -2 supports have even columns; their grid distance is at least two.
These exhaust the interval interfaces. Every retained support therefore
has its original anchor and no second occupied neighbor, proving final
feasibility for all (1). Counting (4) gives (3): A retains a+b+1
selections, and each H module retains h/2+k. These lists are disjoint.

## 3. Exactly one intratile event, and no aligned full-tile credit

The unique irregular event is

    p=(0,0) -> v=(0,1).

Here p is A's terminal tip, v is H_1's long-leg tip, and the original
A profile on Q={0,1} squared is 1P1T. Its original selection (1,0)
survives. The final Q contains endpoints p,v, selection (1,0), and
blank (1,1). It is not full.

The old inward support z=(-1,1) is consumed by H_2's tip, as final
feasibility requires. Its physical tile {-2,-1} x {0,1} contains the
three endpoints (-2,0),(-1,0),z and no selections. Its foreign edge
(-1,0)z replaces mutual original supports, so it produces no
new-neighbor tail. These are the only two mixed-owner physical tiles.

All other A/horizontal interactions are excluded by the separations
above. The two horizontal long legs and their facing bar endpoints lie
in rows -1 and 0, which belong to DIFFERENT physical tile rows. Their
new contacts therefore do not contribute to K. All full physical tiles
are original single-owner bar tiles. This proves J=0, K_regular=0
and K_irregular=1 directly, independently of the receiver ledger.

The full unit square {-1,0} x {0,1} at the three-way contact straddles
the physical tiling boundary. It supplies no J. An unaligned unit square
cannot be silently counted as aligned correction credit.

The original charge sum is -3. The exact ledger now gives rho_final=-2.
Since actual endpoint-free deficit D is nonnegative, sigma=D+2>=2.
Equivalently the finer budget N+S+C-K_irregular-G=3-1=2 pays the event
from the negative-module mass S, not from C. Nothing here refutes the
global compensation target or the accepted corner/tip witness bound.

## 4. Uniform complete-freezing proof

An endpoint is frozen if it cannot be promoted in a feasible bundle.
A selected site is permanently occupied. If x is frozen, its matching
mate is permanently occupied too, because that mate can be discarded
only when x is promoted. An endpoint adjacent to two distinct such
kept sites is frozen. Induction validates every step of the schedules
that follow; additional foreign occupied sites do not weaken a step.

We first describe the ordinary one-sided U schedule in original
coordinates. Start at the short tip (b,W), whose two supports are kept.
Freeze the even short-leg endpoints b,b-2,...,2. Each step has its
outward support and the matching mate of the previous frozen endpoint.
Then freeze (0,W), followed by the alternating bar walk

    (1,W-1),(0,W-2),(1,W-3),...,(0,2),(1,1).

Each bar step has the two kept adjacent mates created by the preceding
alternating steps; the starting corner also has its exterior support.
More explicitly, writing t_c=(0,c), b_c=(1,c), its order is
t_(2j), b_(2j-1) for j=W/2,...,1. After the first corner, t_(2j)
uses kept t_(2j+1), b_(2j), and b_(2j-1) uses kept t_(2j-1), b_(2j).
Now freeze the odd long-leg endpoints (3,1),(5,1),...,(a-1,1), using
their inward support and the kept even predecessor. This freezes one
endpoint of every matching edge along that long leg, so all their
even mates, including the long tip, are kept. After the long tip can
itself be frozen, the even long-leg return wave reaches the bar; the
reverse alternating bar walk and the odd short-leg wave complete the U.
The reverse bar order is t_(2j-1), b_(2j) for j=1,...,W/2.
The initial t_1 uses its exterior support and kept b_1; later top steps
use t_(2j-2), b_(2j-1), and bottom steps use t_(2j), b_(2j-1).
This description works at minimum dimensions as well as larger ones.

Apply its first half to H_1 and H_2. Their short-tip supports, short-leg
supports, starting exterior bar supports and long-leg inward supports
all survive (4). Thus their long tips

    v=(0,1), z=(-1,1)

are kept, and all odd-column sites of their long legs are kept. Their
long-side exterior bar endpoints at column h+1 are kept by the first
alternating bar walk as well.

For A, its long tip p has two retained supports, so its even long-leg
wave is available independently of the short-tip wave. Both bar walks
and the leg waves freeze all A endpoints except possibly q=(-1,0):
only q's inward support was consumed. In particular (-2,0) is kept,
and p is frozen. Since z is now kept, q has the two kept neighbors
(-2,0),z and freezes. Consequently p is kept as q's mate. The site q
was already kept as p's mate.

In this A schedule the odd long-leg wave stops at original row a-3,
before q, until z is independently kept by H_2's first half. Since
a>=w+4>=10, that predecessor step exists at every allowed parameter.

Freeze H_2's tip z using the kept sites q and v. Freeze H_1's tip v
using the kept sites p and z. These steps do not require the opposite
tip to be frozen: both tips were already kept by their own first waves.

Complete the return waves in the two H modules. Their consumed outward
long-leg supports at odd columns are kept sites of the opposite module,
as established in its first wave. Each returning step therefore still
has two kept neighbors. The consumed exterior support of the long-side
upper bar corner is likewise a kept opposite bar endpoint. The reverse
bar walks and ordinary odd short-leg waves then freeze every remaining
endpoint. This is a uniform forcing proof for all (1), not an inference
from the finite controls.

## 5. Unbounded pure-credit deficit, with compensation preserved

In the reference rectangle all occupied columns lie between 1 and 15.
For any integer r>=1, translate r copies by (0,16i), i=0,...,r-1,
inside an 18-by-16r rectangle. Occupied sites in different copies have
column separation at least two. There are no shared or adjacent sites,
and the even translations preserve physical tiles. The original matching,
feasibility and complete freezing certificates remain valid independently
in each copy. All ledgers add, giving

    B_minus=3r, J=K_regular=C=0, K_irregular=r,
    |P|=76r, |M|=38r, |T|=35r, rho_final=-2r,
    finer guaranteed slack=2r, actual sigma=71r.

Thus K_minus_one<=C fails by an arbitrarily large amount even among
fully frozen fusions. No fixed additive constant repairs that rule.
This repeated construction is disconnected; the individual parameter
family is connected and has unbounded size. No connected unbounded-deficit
claim is inferred from separated copies.

## 6. Verification, scope and next step

The independent checker reconstructs the reference, 144 admissible
parameter choices, eight tiling-preserving dihedral images and six
separated-copy controls. Each is fully frozen. For every parameter control,
it also replays the specific first-wave, A-wave, tip-closure and return-wave
schedule in Section 4, checking two kept neighbors at every step, separately
from the generic freezing calculation. Run

    python3 develop/check_zero_credit_tip_family.py \
      --output output/zero-credit-tip-family-controls.json

The Std-only Lean source formal/SubQuorum/ZeroCreditTipFamily.lean checks
the actual three sources, their charges and source feasibility, matching
and distinct endpoints, complete final feasibility, counts76/38/35,
the single minus-one tip event, its nonfull tile, zero new full tiles,
the nonaligned square, receiver30/20 with charge -2 and slack71. A
complete 76-step certificate is replayed: each step has two distinct
adjacent kept witnesses derived only from T or earlier frozen mates,
and every endpoint is covered. The two-kept forcing rule and repeated
scalar consequences are separate declarations. The all-parameter
coordinate adapter and uniform schedule proof above remain written.

The complete review and assessment of the preceding joint theorem are
archived separately. The reference originated in its optional discussion;
the stronger full-freezing claim and parameter extension were checked
here. No finite control, reviewer verdict or kernel receipt substitutes
for the general geometric proof. General grid decomposition and triple
equality remain open.

The separate review of THIS parameter-family and freezing proof has now
completed ACCEPT, task b4761670-eb2a-42aa-af31-9d7b8a1c271e, observed
gpt_6/pro. Its original stream ended with DONE and exactly matches the
17213-character terminal response. The reviewer independently reconstructs
the support lists, receiver counts, full forcing schedule and separated-copy
argument. The auxiliary notation and bar-walk clarifications above implement
its presentation suggestions. This verdict does not cover the later
all-phase joint-slot extension; execution receipts remain separate evidence.

Next study joint allocation of S, remaining square credit and marked-side
loss, rather than attempting K_irregular<=C. A valid transport mechanism
must recognize that a fully frozen nonfull tip tile can have no square
credit anywhere in its component, while still preserving the disjoint
corner/tip witness accounting.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
