# A north consumer's internal contact debit is one or two, independent of width

21 October 2026. This computes the exact pair-contact ledger for the
remaining secondary-ten north branch. Its isolated negative mass w-1
is already largely cancelled by mandatory D/L contacts. It is not an
independently available reserve payment. Completion and all external
contacts remain separate obligations.

## 1. Exact endpoint functional and hypotheses

Let b be even, w,m even with w>=8 and m>=w+2, and let t,v be independent
even integers>=4. Use the original U matching/support constructor and
the actual physical frames

    D=U(m,10,t), D(r,c)=(b-11+r,c+5),
    L=U(w,4,v), L(r,c)=(b-9+r,c+6).

Their endpoint sets are disjoint for every such choice. Both isolated
charges are negative: 1-m and1-w. Original ownership is never changed.
For ANY endpoint-disjoint source family, complete or incomplete, define

    Rraw = S+2F-E,

where S sums negative ORIGINAL charge magnitudes, F counts full physical
tiles not full in any one original owner, and E counts actual directed
intratile events (owner,endpoint,foreign endpoint) outside the owner's
original endpoint/support set. This is exactly the existing event-reserve
formula; without completeness it is only an algebraic functional. In a
complete feasible family it equals the physical reserve R. We do not
claim that D alone or the D/L pair is a feasible closed subfamily.

Write Delta for insertion of L beside D, and k=w/2. Then

    m=w+2: d=min(t-2,v)/2,
             Delta S=w-1, Delta F=k+3+d, Delta E=2w+6+2d,
             Delta Rraw=-1;

    m>=w+4: Delta S=w-1, Delta F=k+2, Delta E=2w+5,
             Delta Rraw=-2.                          (1)

The same increment holds with the prescribed Q=U(6,8,4) already present,
Q(r,c)=(b+2-c,11-r). It shares no endpoint tile with L when w>=8.
The formulas make no assertion that either partial stencil is completable.

## 2. General tile partition and proof

The D lower bar and L upper bar share the tile row with lower coordinate
b-10. L's upper bar occupies columns7,...,w+6, so its first and last
column pairs are (6,7) and(w+6,w+7). Between these are k-1 complete
two-column pairs. D's near stem is at column6, L's at7. If m=w+2,
D's far stem is at w+7 beside L's at w+6. If m>=w+4 these far stems
are in different column pairs and have no intratile contact.

The following table exhausts every tile with D and L endpoints. Entries
give the endpoint partition D+L, number of tiles, new mixed-full count
per tile, and directed-event count per tile. Event counts use ORIGINAL
supports, including supports subsequently consumed by the other owner.

| Tile class | Partition | Number | F per tile | E per tile |
|---|---|---|---|---|
| Left upper-bar end | 3+1 | 1 | 1 | 3 |
| Upper-bar interior | 2+2 | k-1 | 1 | 4 |
| Right upper-bar end, m=w+2 | 3+1 | 1 | 1 | 3 |
| Right upper-bar end, m>=w+4 | 2+1 | 1 | 0 | 2 |
| Near parallel stems | 2+2 | 2 | 1 | 2 |
| Far parallel stems, m=w+2 | 2+2 | d | 1 | 2 |

For a bar-interior tile each of its two cross-owner vertical edges
creates both directed events, hence4. At the left3+1 tile D has2
events and L has1: the other potential L event meets its original support
(b-9,6). The same calculation holds at the tight right3+1 tile, using
L's original bar-end support. At the separated right2+1 tile each owner
has1 event. In a parallel-stem tile each owner has1 event: the other
cross-owner neighbor is that owner's alternating original leg support.
Thus this table counts directed events, not unweighted endpoint contacts.

The two near-stem tiles have lower rows b-8,b-6. Tight far-stem tiles
start at b-8 and continue while both two-row original stem segments
exist. D provides t-2 consecutive rows beginning there, L provides v;
both lengths are even. Their number is therefore d=min(t-2,v)/2.
No other contact is possible: away from these bar and parallel-stem
positions, either physical row pairs or physical column pairs are disjoint.
Neither original negative-phase U contains a full tile of its own, so
every full tile in this table is a new mixed full tile.

Summing gives tight F=1+(k-1)+1+2+d=k+3+d and
E=3+4(k-1)+3+4+2d=2w+6+2d. In the separated case F=k+2 and
E=3+4(k-1)+2+4=2w+5. Substitution into

    Delta Rraw=(w-1)+2 Delta F-Delta E

proves(1) for arbitrary dimensions. Width and common far-stem length
cancel exactly. Q's endpoint rows begin at b-4; L's near/bar endpoint
tiles end by b-5, while its far-stem column pair begins at w+6>=14,
beyond Q's maximum endpoint column11. Thus Q changes no table entry.

## 3. External sources: the exact remaining signed term

Let W be ANY other endpoint-disjoint original sources, possibly from
other components, with D retained. Add L to D union W. Every D/L full
tile in Section2 is necessarily a NEW full tile in this insertion: it
contains an L endpoint, which was absent before insertion, and W cannot
own an endpoint there because D/L already fill all four cells.

Write Fextra for the remaining newly full mixed tiles, excluding the
D/L full tiles already counted, and E(L,W) for all directed intratile
events between L and W in BOTH directions. Source-labelled event sets
split exactly by the other endpoint's original owner. Therefore

    Rraw(D union W union L)-Rraw(D union W)
      = -delta+2Fextra-E(L,W),
    delta=1 if m=w+2, otherwise2.                    (2)

Fextra>=0. This identity does not say the extra signed term is nonnegative.
Each new full tile and each source-labelled directed event enters once.
An external full tile already used elsewhere cannot also pay this insertion.
When both compared families are complete feasible, Rraw is physical R;
otherwise(2) remains an exact algebraic partition only.

This changes the local task: the pair's width-dependent isolated mass
does not require a new payment of w-1, but it also provides no free
surplus. The remaining pair debit is1/2 PLUS the signed external-contact
term in(2). A global argument must bound these terms jointly, retaining
every external source's OWN signed contribution and the common initial
margin once. No monotone reserve theorem, independent per-owner surplus,
or counterexample to the full allocation inequality is inferred.

There is a concrete next closure site when m>=w+4: L's original upper
bar-end support u=(b-9,w+7) is absent from D,L,Q but has its L anchor
(b-9,w+6) immediately west and D's lower-bar endpoint (b-10,w+7)
immediately north. Any complete extension must therefore consume u.
It may already be consumed by an actual external owner; no fresh-owner
claim is made. When m=w+2, the same point is already D(2,m), so it is
not a new consumer demand and must not be credited again.

For a concrete obstruction to the ENDPOINT-ONLY rule 2Fextra>=E(L,W),
take b=40, D=U(12,10,4), L=U(8,4,6) in the displayed charts, and

    W=U(6,4,4), W(r,c)=(32+c,9+r), charge(W)=-5.

All three original endpoint sets are disjoint. The two extra full tiles
have lower coordinates (32,10),(32,12). There are SEVEN directed L/W
events: L at (32,c) points to W at (33,c), for c=9,10,11,12,13;
W at (33,c) points back to L at (32,c), for c=10,12. All other
potential directions meet that owner's original supports or are absent.
Hence 2Fextra-E(L,W)=4-7=-3. Inserting L beside D alone costs2;
inserting it beside D and W costs5, with Rraw falling16 to11.

This refutes that endpoint-only external nonnegativity rule, not a rule
additionally assuming COMPLETE feasible families and not the target
allocation inequality. In fact the displayed triple is explicitly
incomplete: L's original support (31,15) remains unconsumed but has
both its L anchor (31,14) and a D neighbor (30,15). Further owners are
mandatory. Their physical signed contributions must be included in any
complete extension; they cannot be silently discarded or assumed helpful.

## 4. Verification and remaining scope

The subsequent [gap-four package theorem](SECONDARY_TEN_NORTH_GAP_FOUR_PACKAGE.md)
classifies the actual consumer when m=w+4 and proves exact local neutrality
of an outward positive package, with a stronger external-sign obstruction.
Its [cavity continuation](SECONDARY_TEN_NORTH_OUTWARD_CAVITY.md) forces a
second, negative actual owner, excludes h=t and bounds the tight h=t+2 case.
Those are separate proof and validation milestones; no global credit is
inferred from the isolated package.

The table and endpoint separation above are the all-parameter proof.
A [separate checker](../develop/check_secondary_ten_north_contact_debit.py)
directly reconstructs original matchings/supports, all shared tiles and
directed events, and the external insertion partition. Its
[recorded controls](../output/secondary-ten-north-contact-debit-controls.json)
PASS640 parameter patterns at widths8,10,20,50,200, including160 tight,
480 separated and640 Q-neutral checks. All1068 endpoint-disjoint
external-source stencils satisfy(2);205 have positive external owners,
863 negative. The external signed term is negative in12 cases, with
minimum -3. The explicit witness, seven original directed events and
its missing forced support are reconstructed independently. Finite checks
do not establish complete realizability or the missing external bound.
This note is outside the separate completed all-upward proof review.

Unrestricted mixed allocation and rectangular-grid equality remain OPEN.
N continues to count positive ORIGINAL owners only. Submitted DMGT and
primary C4-free results are preserved; no mail or draft action is made.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
