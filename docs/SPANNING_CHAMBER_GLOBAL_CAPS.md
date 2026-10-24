# Complete finite realizations of spanning chambers and pocket states

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Construction and conclusion

This note provides a whole retained-support realization of the local
pockets used in the preceding notes. No global extendibility of those
states was asserted there. The construction here supplies it for the
explicit canonical fusion model, without claiming the unrestricted grid
inequality or any new equality between graph parameters.

Choose an even width W>=6 and any integer g>=0. Put a_i=2+10i for
0<=i<=g. Retain

    A=U(W+2,D,F), chart(r,c)=(r,c-1),
    B_i=U(W,4,4), chart(r,c)=(a_i+r,c),

where D,F are even and at least a_g+10. For every i<g choose either

    D_i=U(W,4,4), chart(r,c)=(a_i+5+r,c),
    U_i=U(W,4,4), chart(r,c)=(a_i+9-r,c).

Finally add the bottom cap

    C=U(W,4,4), chart(r,c)=(a_g+9-r,c).

All endpoint sets are disjoint. Retain every original support not consumed
by an endpoint. The resulting WHOLE finite fusion has every retained
support of occupied degree exactly1 and every matching endpoint of
occupied degree at least3. All endpoints are covered by the disjoint
original matching. An even translation embeds all original records and
supports inside a finite even-by-even rectangle without clipping.

If d is the number of D_i choices, its exact inventory is

    Phi=4g+(W-4)d+5.                                    (1)

Moreover, in every U_i pocket, independently insert ANY finite full-source
state satisfying the established pocket retained-support condition relative
to its old core. The whole fusion remains complete in the same sense. If
its local inventory is phi_i, then

    Phi=4g+(W-4)d+5+sum_i phi_i.                         (2)

This is a realization/gluing theorem for the stated canonical model. It
does not assert that every grid configuration has that model or that this
choice of cap minimizes possible exterior inventory.

## Exact all-parameter retained-support proof

The outer A has endpoint walls at columns0,W+1. Each B_i occupies full
bar rows a_i,a_i+1 and side columns1,W through row a_i+4. Each selected
D_i or U_i fills both side columns1,W on rows a_i+5 through a_i+9.
The cap fills those columns from a_g+5 through a_g+9. Hence the inner
side columns1,W are occupied at every row2 through a_g+9.

Canonical A's supports on its inside sides are at odd rows3,5,...,
D-1 in column1, and3,5,...,F-1 in column W. Those through a_g+9 are
all consumed by the displayed endpoints. Those starting at a_g+11
remain, each with just its own horizontal wall neighbour. Their vertical
neighbours are empty, since the inner sources end by row a_g+9. Outside
A the supports at even rows in columns-1,W+2, its two bar-end supports
and its two beyond-leg supports remain, each with exactly its own wall,
bar-end or leg-tip neighbour. They are pairwise nonadjacent. The bound
D,F>=a_g+10 keeps both leg ends away from every inner endpoint/support.

For B_i, its bar-end and outside-leg supports at columns0,W+1 are
consumed by A. Its two beyond-leg supports (a_i+5,1),(a_i+5,W) are
consumed by the chosen next source or, for i=g, by C. Its only retained
supports are

    (a_i+3,2), (a_i+3,W-1).

They have exactly their own side-leg neighbour. For D_i, all exterior
side/bar supports are consumed by A, its beyond-leg supports at row
a_i+10 are consumed by B_(i+1), and its only retained supports are

    (a_i+8,2), (a_i+8,W-1).

For U_i and C, all exterior side/bar supports are consumed by A, their
beyond-leg supports at row a_i+4 are consumed by B_i, and their only
retained supports are

    (a_i+6,2), (a_i+6,W-1).

This exhausts the immutable original support lists. Different listed
interior support rows differ by at least3. The two columns differ by
W-3>=3. No remaining support is adjacent to another; each has only the
one stated endpoint neighbour. This proves the occupied-degree condition
for every support, including those outside all sealed chambers.

The endpoint sets are disjoint by their displayed row intervals, side
columns and the gap between the two walls. Their original matchings
therefore remain disjoint and cover all endpoints. Each canonical endpoint
already has at least3 occupied neighbours in its own endpoint/support
record. Fusion never removes an occupied site: a consumed support is
replaced by an endpoint at the same site. Thus every endpoint retains
degree at least3 in the full occupied set.

All original records are finite. An even translation puts their minimum
coordinates above0, and sufficiently large even rectangle dimensions
contain their maximum coordinates and all original supports. This gives
the asserted actual finite rectangle, with no clipped support or boundary
exception. The claim is the retained-support/matching fusion condition,
not a separately unproved extremality or graph-parameter identification.

## Gluing arbitrary locally complete U-pocket states

For a chosen U_i, its pocket is

    P_i=[a_i+2,a_i+7] x [2,W-1].

Its entire one-step boundary consists of old-core endpoints: B_i above,
U_i below, and their continuous side columns1,W. New sources in a pocket
have endpoints strictly inside it. All their original supports outside
the pocket lie on that already occupied boundary and are consumed.
Hence they introduce no retained support outside P_i.

A retained old support outside P_i cannot acquire an adjacent new endpoint
inside P_i: an outside site adjacent to an inside site is on the one-step
boundary, already an endpoint and therefore not a retained support. Inside
P_i the assumed local complete condition checks all new and inherited
retained supports against exactly the same endpoint boundary and occupied
set. Thus gluing preserves the support-degree condition everywhere.
Different pockets do not meet or share such a boundary support. The same
argument works simultaneously for any number of the chosen U pockets.

This proof does not use the new rotor exclusion: it applies to ANY finite
canonical locally complete pocket state of the specified model. It does
not assume that deleting a subset of that state preserves completeness.

## Exact inventory and no reused exterior contribution

The old A plus all B_i has Phi=-g by the established even-bar ledger.
Each spanning D_i adds W+1, while each spanning U_i adds5 before pocket
sources. Their whole physical-tile and labelled-event differences separate
by chamber against that same baseline.

The cap adds5 as well. Its charge is+1; it creates6 mixed full tiles
and8 directed original-support-excluded events, giving1+12-8=5. These
are exactly the spanning-U receipt with A and B_g. A hypothetical B_(g+1)
at a_g+10 would have no endpoint in any physical tile of the cap, whose
maximum row a_g+9 is odd, so its absence changes none of that receipt.
All other B_i and chamber sources are separated from these tiles. Thus
the cap's five units are counted once in the exterior contribution.

Summing against the single old baseline gives

    -g+(W+1)d+5(g-d)+5=4g+(W-4)d+5.

Every pocket begins at even row/column and ends at odd row/column, so
its tiles are entirely inside it and disjoint from old-core endpoint
footprints, although inherited old supports can lie inside the pocket. The
same established inventory separation adds exactly its phi_i. There is
no event or full mixed tile shared by pockets, chambers or the cap.
This proves (1),(2), including simultaneous nonreuse.

## Fully realized negative horizontal marginals

Use g=1, select U_0 and the bottom cap, and put k blocks of the odd-H
family from `SIX_ROW_ALL_PHASE_HORIZONTAL_BUDGET.md` in P_0. For any
even B>=6 set W=k(B+34)+2. The local AFTER state has k H and6k V, with
Phi=k(B+9); the local V-only BEFORE inventory is16k. The gluing theorem
proves that the entire BEFORE and AFTER fusions are complete, with

    Phi_before=9+16k,
    Phi_after=9+k(B+9),
    marginal=k(B-7).

At B=6 this is25 to24 for k=1, and marginal-k for arbitrary k. This
strengthens the earlier locally complete obstruction to an explicit
whole finite retained-support realization. The example refutes nonnegative
H marginal even when BOTH before and after are complete. It does not
refute the target inequality, since both displayed total budgets are
positive. No general completeness-preserving deletion principle is used.

Here is a direct all-parameter completeness proof for BEFORE. Normalize
one block to P=[0,5] x [0,N-1], N=B+34. Its six V specifications
(bar,direction,bottom depth,top depth) are

    (0,+1,4,4), (5,+1,4,4), (15,-1,6,6),
    (B+17,+1,4,4), (B+22,+1,4,4), (B+32,-1,6,6).

Their endpoint union on each extreme row0,5 is

    [0,16] union [B+17,B+33].

The interior-row endpoints occur only in the two-column bars. The
immutable support lists leave exactly the following V supports inside P:

    {1,4} x {3,8,11,13,B+20,B+25,B+28,B+30}.            (3)

Every other V support either lies on the occupied exterior boundary or
is consumed by a neighbouring bar or facing stem. The inherited old
supports {1,4} x {0,N-1} are consumed by the extreme bars. Each support
in (3) has exactly its endpoint neighbour on row0 or5; no horizontal
neighbour is an endpoint or a retained support. The two support rows
are separated by3. Thus the V-only state is locally complete.

The H projection [17,B+16] contains none of these retained supports or
inherited old supports. Its two additional retained supports lie at
(4,18),(4,B+15) for H1, or their row reflections
(1,18),(1,B+15) for H4. Each has only
its own side-leg neighbour, so AFTER is locally complete as well.
At a block interface N is even: no physical tile crosses the interface,
and the nearest retained support columns from different blocks differ
by7. The two complete local states therefore juxtapose for every k>=1.
Applying the gluing theorem separately to each state proves the claimed
whole completeness of both configurations, with no deletion inference.

The cap also realizes the two-V sharp nonempty pocket states within a
whole complete finite fusion. Therefore those local sharpness statements
can be accompanied by actual whole retained-support examples; no global
extremality assertion follows from that fact.

## Verification and scope

`develop/check_spanning_chamber_global_caps.py` checks every retained
support in each whole fusion, every endpoint's occupied degree, disjoint
matching coverage, even ambient containment and full inventory. It tests
arbitrary D/U patterns in selected lengths and large width, plus fully
realized negative-H families. The preceding coordinate and locality proof
establishes the all-parameter theorem independently of finite controls.
No new Lean theorem is claimed for this gluing result. Prior local Lean
scopes do not certify its complete source-to-ambient assembly.

Initial independent review task954ec124-3bdf-47a5-b087-dd0c9aa4e473
returned REVISE: it accepted the cap/gluing proof and inventory, but
found that the explicit BEFORE is complete too, contrary to the original
categorical scope exclusion. The direct support proof (3) and both-state
whole checks above implement the stronger correction. The final local
run passes170 capped cores,18 both-complete negative-marginal families
with exact BEFORE support lists, and12 sharp pocket embeddings.
Follow-up task4248a536-93ef-48dd-bde7-613344d1ee0e confirmed the new
BEFORE support list, interfaces and both-complete obstruction, but
returned REVISE for a transposition of the H1/H4 orientation labels in
the new support paragraph. Those labels are now corrected explicitly:
H1 supports lie on row4, H4 supports on row1. The checker additionally
compares each complete AFTER pocket support set to the exact V-plus-H
list in both orientations. The original REVISE is retained in
`output/spanning-chamber-global-cap-review-terminal.json`; it is not
recorded as a final ACCEPT of the corrected note; follow-up REVISE is in
`output/spanning-chamber-global-cap-followup-review-terminal.json`.

Final follow-up47746304-ac4e-4b34-a29c-b9ae9f97245c returned ACCEPT
after the orientation-label correction. It accepts the full cap/gluing
construction, both-complete negative marginal and exact support lists
within the stated canonical model. The1732-character answer matches
the completed original stream and terminal API, observed gpt_6/pro.
It assessed the written argument and assertion logic without executing
the checker. Both earlier REVISE receipts are retained; the final receipt
is `output/spanning-chamber-global-cap-final-review-terminal.json`.

This construction produces a positive exterior increment5. It does NOT
bound the exterior increment of an arbitrary complete extension from
below; other gate branches and the unrestricted global problem remain
open. The submitted manuscript and public main remain unchanged.
