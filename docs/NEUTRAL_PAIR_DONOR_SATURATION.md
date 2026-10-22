# A neutral pair can saturate a virtual-guard donor

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

This note gives an all-parameter obstruction to two candidate compensation
rules. A completed positive core has a local unit donor, but that physical
tile is saturated on the original board. The only neighboring completed
core has charge zero. Thus neither automatic donor transport nor automatic
payment by a negative neighboring core is valid. The target half-area
inequality remains true for this family. We also identify a different,
original donor that pays its demand.

## 1. Definitions and construction

Use the original-board tiling, receiver charge rho, endpoint-free deficit D,
and even-bridge completion from EVEN_BRIDGE_SUPPORT_COMPLETION.md. For a
completed piece retain original selected vertices adjacent to its endpoints,
and restore neighboring endpoints across removed even bridges as selections.
The exact identity is

    mn/2-|T|-|M| = D-sum_K rho(completed K).                 (1)

All deficits in (1) belong to the ORIGINAL board. A local completed-board
deficit is not automatically available there.

Let W>=6 and H>=4 be even. Start with the standard elbow E(W,H), translated
by (4,5), with exactly the endpoint set, selected supports and prescribed
matching of Section 4 of NATIVE_GUARD_COMPENSATION_AND_VIRTUAL_GUARD_OBSTRUCTION.md.
Write its endpoints as O, its selections as T_E, and its matching as M_E.
Add the selected vertex b=(6,7). Attach a two-endpoint pair with

    p=(6,5), q=(7,5), s=(8,5),
    c=(7,6), u=(8,4), v=(9,5).

Here p is the elbow's short-tip endpoint and q is one of its original
selected supports. The pair has matching edge q--s and isolated supports
p,c,u,v. Define the original whole configuration by

    P = O union {q,s},
    M = M_E union {q--s},
    T = (T_E union {b,p,c,u,v}) minus P,
    m=H+8, n=W+12,

with all unlisted vertices blank. Exactly q and p are consumed as mutual
supports. The physical tile of interest is

    Q={6,7} x {6,7}.

## 2. Feasibility and the complete endpoint decomposition

The standard elbow occupies its bar in rows4,5 and its right leg in
columns W+3,W+4. Apart from p, its endpoints below the bar are on that
right leg. The added pair lies in column5 at rows7,8, so the ONLY
endpoint edge between it and O is p--q. There are no other contacts even
at W=6,H=4, because the leg's left column is at least9.

The extra selection b sees exactly the elbow endpoint (5,7); its other
neighbors (6,6),(6,8),(7,7) are blank. The selection c sees exactly q;
its other neighbors (6,6),(7,7),(8,6) are blank. Likewise u and v see
exactly s, with all their other neighbors blank. The closest old elbow
support to u is (6,4), at distance two, and the closest right-leg
supports have column at least8. None is adjacent to the new selections
or endpoints. All retained old selections therefore keep their original
single occupied neighbor. At p, the old occupied support q simply becomes
an endpoint. Thus the pair is feasible, and every endpoint has occupied
degree at least three. All named vertices are within the stated board.

The edge p--q is a bridge separating two even endpoint sets. In the elbow,
all nontip edges lie on unit endpoint squares, while its two tip bridges
separate an odd number of endpoints. Attaching two endpoints changes none
of those cut parities. The pair's internal edge q--s separates a single
endpoint and is odd. Consequently p--q is the only even bridge; there
are exactly TWO final completed pieces.

Those completed pairs are exactly

    outer: endpoints O, selections T_E union {b}, matching M_E;
    pair:  endpoints {q,s}, selections {p,c,u,v}, matching {q--s}.

In particular c is not retained in the outer completion: it is anchored
to q. The added b is retained there: it is anchored to (5,7).

## 3. Unique matching and exchange terminality for all parameters

The accepted standard-elbow leaf order proves that O has a unique perfect
matching for every W,H. The pair has one matching edge. An even bridge
cannot occur in a perfect matching: deleting its endpoints would leave
an odd number on each side. Hence every whole matching factors into
these two unique matchings, and the displayed M is the only one.

For the completed outer pair, retain the standard elbow freezing proof.
Adding b deletes no old support, so every old retained-neighbor witness
still works. The new selection is feasible as checked above. For the
completed pair, q sees the two distinct selected supports p,c, and s
sees the two distinct selected supports u,v. Both endpoints freeze
immediately. The accepted even-bridge theorem now implies whole exchange
terminality, including simultaneous exchanges using both pieces. This
argument uses a general proof, not parameter enumeration.

## 4. Exact charges and disappearance of the local unit donor

The completed outer receiver still has W/2+H+1 tiles, H+4 selected
corners and W+H-1 matching edges. Its additional selection b is outside
the endpoint receiver, so its charge remains

    rho_outer = (W+H-1)+(H+4)-2(W/2+H+1) = 1.

The pair meets tiles {6,7}x{4,5} and {8,9}x{4,5}. Exactly p,u,v
are selected within those tiles; c is outside. Thus

    rho_pair = 1+3-2*2 = 0,
    rho_whole = 1.

The completed outer capped witness consists of endpoints
(5,5),(5,6),(5,7),(5,8),(6,5) and selected guard q=(7,5).
The two upper corners of Q are not endpoints. Q has no outer endpoints
and contains precisely the single outer selection b. Its LOCAL deficit
is therefore one. In the original configuration, Q still has no endpoints,
but its selected vertices are the two opposite corners b,c. Its ORIGINAL
deficit is zero. No original supply remains at Q.

This is stronger than merely placing foreign endpoints in a locally blank
capacity-two tile: even an endpoint-free local unit donor can disappear
by saturation. Moreover the sole adjacent completed core has charge zero,
so it has no negative-charge surplus to cover the lost unit.

## 5. Original counts and a genuine relocated donor

The whole counts are

    |M|=W+H, |T|=H+7, |T|+|M|=W+2H+7.

The two completed receivers overlap in just the bridge tile. Their union
therefore has W/2+H+2 tiles. Its original selected count is H+5; exactly
b,c are selected outside it. Hence

    D=mn/2-W-2H-6,
    mn/2-|T|-|M|=D-1.

The distinct physical tile R={8,9}x{6,7} is entirely blank in this explicit
family. The pair and its supports lie at column at most5 apart from c in
row7. The elbow endpoints at these rows have column at least9, and its
nearest inward leg supports have column at least8. Thus R has no endpoint
or selection, for every stated W,H. Its ORIGINAL deficit is two and pays
the whole demand one. Only one unit is needed; do not add the vanished
unit at Q or invent a negative charge at the pair.

For the smallest W=6,H=4 example the board is 12 by18, |M|=10, |T|=11,
charges are 1 and0, D=88, and the actual half-area margin is87.

## 6. What fails, and what remains open

The construction disproves these universal candidate rules:

- A completed capped local unit donor with a virtual guard is necessarily
  a positive-deficit original donor, even if it stays endpoint-free.
- Whenever such a donor is lost, the adjacent completed piece necessarily
  has negative charge sufficient to pay the loss.

It does not disprove the native-guard theorem, identity (1), or the target
inequality. For this explicit family Section5 gives a valid different
donor. A universal relay theorem must justify continued transport through
arbitrary exteriors and assign original physical capacity without reuse.
The blank R here is a property of the specified family, not a claim about
every feasible exterior of this portal. In particular the present theorem
does not establish unrestricted grid compensation or grid triple equality.

The companion verifier checks coordinates, the only even cut, uniqueness
by independent leaf elimination, full freezing, charges, Q saturation,
R payment and original counts over a stated finite range and all eight
tile-preserving symmetries. Scoped Lean lemmas separately check local
geometry, pair exchange exclusion and count identities. Neither replaces
the all-parameter geometric proof above. The earlier native-guard theorem
and this construction now have separate independent accepted written
reviews; see output/neutral-pair-donor-saturation-review-accepted.json for
the latter. The subsequent arbitrary-exterior corridor theorem and its
different accepted review are in NEUTRAL_PORTAL_STRIP_COMPENSATION.md.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
