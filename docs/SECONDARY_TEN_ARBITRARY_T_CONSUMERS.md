# Arbitrary single-block renewed consumers and nested joint compensation

21 October 2026. Continue the [accepted renewed-support construction](SECONDARY_TEN_RENEWED_SUPPORT_ESCAPE.md).
Use full ORIGINAL U/rotor endpoint, support and matching sets throughout.
Phi=N+S+2F-E has the same meaning as in that note; every old source charge
and every original-support event exclusion persists after consumption.

## 1. Complete single-block classification

Take its SINGLE block H3, with odd a, even s, even w>=12,z>=24 and
root K=U(h,6,4), even h>=6. Its baseline is b=w+9 and

    Phi(H3)=b+h-2.

The unconsumed original support t=(a-4,s) has west Z, east P^0 and south
Z endpoint neighbors. If a complete feasible original family contains H3,
the actual owner T of t must therefore have its own matching neighbor north.
Both north-tip rotor placements contain the retained P^0 endpoint(a-6,s+1).
Every other surviving role is a north-terminal U. Leg exchange of the full
original gives exactly the following frames, with even H>=6,d,f>=4:

    T_left:  U(H,d,f), chart(a-4-d+r,s+1-c),
    T_right: U(H,d,f), chart(a-4-d+r,s-1+c).           (1)

Both have charge1-H. No enumeration limit is used in this role argument.

**Single-block compensation theorem.** The endpoint-disjoint alternatives
in(1) are exactly the cases in the following table. Write
Delta=Phi(H3 union {T})-Phi(H3).

| Frame and parameter case | Endpoint-disjoint iff | Delta |
|---|---|---|
| Left, any H,d,f | always | H-1 |
| Right,d=4 | never | excluded |
| Right,d=6,H<=w+12 | never | excluded |
| Right,d=6,H=w+14 | f<=8 | 1 |
| Right,d=6,w+16<=H<=w+h+14 | never | excluded |
| Right,d=6,H>=w+h+16 | always | H-w-14 |
| Right,d>=8,H<=w+12 | f<=d-6 | H-2 |
| Right,d>=8,H=w+14 | f<=d+2 | H-2-epsilon |
| Right,d>=8,w+16<=H<=w+h+14 | f<=d-4 | H-2 |
| Right,d>=8,H>=w+h+16 | always | H-2 |

Here epsilon=1 exactly when f>=d-4, and is0 otherwise. Since all variables
are even, these breadth intervals exhaust the alternatives without gaps.
Every surviving row has Delta>=1. Equality occurs exactly for the right
frame H=w+14,d=6,f in{4,6,8}. Consequently any actual t-owner in a complete
extension supplies, in THIS selected local union,

    Phi(H3 union {T})>=b+h-1.                       (2)

The conclusion is about the displayed subinventory; it does not assert
Phi(G)>=Phi(H3 union {T}) for an arbitrary larger complete family G.

The same classification and Delta hold if the single-block small X is
replaced by ANY of the accepted tail originals

    J=U(w,D,D-6), chart(a+D-2-r,s+c), even D>=z-2.

Thus every actual t-owner in a complete extension of that tail inventory
gives Phi>=b+h-5>=b+1 in its selected local union. Existence of such a
complete extension is not asserted.

## 2. Charge phase and exact collision frontier

Normalize relative to(a,s). Physical tiles have row pairs{2p-1,2p} and
column pairs{2q,2q+1}. Put R=-4-d, an even relative row (its absolute
row a+R is odd). The north U has bar rows
R,R+1, near stem column0 ending at-4, and far stem ending at R+f.
Its far column is1-H in the left frame and H-1 in the right frame.

Set H=2B,d=2u,f=2v. Both frames have H-1+u+v matching edges. For the right
frame the endpoint-tile and inside-original-support counts are

    F_source=H+u+v-2,   I_source=u+v-2;

for the left they are H+u+v and u+v+2. The bar crosses two tile rows.
Its column interval is aligned in the right frame and unaligned in the
left; this accounts for the difference of two endpoint tiles. The axial
supports are beyond the odd-row terminals and lie in the next tile rows.
On the right only the odd intrinsic lateral rows3,...,d-1 or f-1 contribute
inside supports. On the left the even lateral rows and two exterior bar
supports contribute. Substitution gives charge1-H in both frames.

For left T, the far column is at most-5, while every old endpoint has
column at least-4. At the boundary H=6, columns-5,-4 lie in different
physical tile columns. The bar has maximum column0 and lies above the
western rotor. The near stem shares only its column0/1 tile strip with
P^0. There is no endpoint collision, including for arbitrarily large f.

For right T,d=4, the bar row-8 contains column1, a P^0 bar endpoint.
For d>=6, both bar rows lie above P^0. Endpoint disjointness is determined
by the first old endpoint in its far column C=H-1:

| Far column | First old endpoint row | Original |
|---|---|---|
| 5<=C<=w+11 | -8 | P^0 bar |
| C=w+13 | 0 | E far terminal |
| w+15<=C<=w+h+13 | -6 | K bar |
| C>=w+h+15 | none | outside all old endpoint columns |

These intervals use odd C only. Earlier originals do not create an
exception: P^0 has maximum column w+12; the only potentially earlier
rightward base coordinates belong to V/T0, whose maxima are w+11,w+10.
All other base endpoints in the root-column range start after row-6.
The root reaches farther right than the entire base because h>=6.

The far endpoint has even relative row R+f, hence odd absolute row.
It must stop strictly above the first
old endpoint row. Thus the respective bounds are f<=d-6, f<=d+2,
f<=d-4, or no bound. At d=6 these give the excluded narrow and root
ranges, the three allowed special depths4,6,8, and the unrestricted wide
range. This proves both necessity and sufficiency in the table. The near
stem and bar cannot supply an additional collision once these conditions
hold: the bar is above the old inventory, except for the d=6 adjacent
P^0 band, and the near column0 is absent from H3 at all rows<=-4.

## 3. Exhaustive local full-tile and event receipts

The following table gives counts of NEW mixed full tiles and NEW directed
events against the entire H3, not against a separately truncated strip.
All surviving consumers have negative mass H-1.

| Surviving case | DeltaF | DeltaE |
|---|---|---|
| Left | 2 | 4 |
| Right,d>=8, no special far contact | 2 | 5 |
| Right,d>=8,H=w+14,f>=d-4 | 2+m | 6+2m |
| Right,d=6,H=w+14,f=4+2e | w/2+10+e | 2w+32+2e |
| Right,d=6,H>=w+h+16 | w/2+8 | 2w+29 |

Here m=(f-d+4)/2 in{0,1,2,3} and e in{0,1,2}. Every table row follows
from the next explicit partition; the formulas do not rely on a cutoff.

The common near-stem strip has new full tiles with minima(-7,0),(-5,0).
For left T its surviving events are

    T:(j,0) -> P^0:(j,1), j=-7,-5,
    P^0:(j,1) -> T:(j,0), j=-7,-5.

For right T the corresponding event lists are

    T:(j,0) -> P^0:(j,1), j=-8,-6,-4,
    P^0:(j,1) -> T:(j,0), j=-7,-5.

The side-support parity and the original P^0 bar-exterior support exclude
the omitted directions. Both lists remain valid at d=4 for the legal left
frame. Above the two lower near-stem tiles, the tile with minimum(-9,0)
is partial for left consumers and deep right consumers. It has two
endpoints when left d=4, and three in the other such cases. For right
d=6 it is full and belongs to the bar band counted below. The geometric
adjacencies to Z at t cross tile boundaries, so Z contributes no event
and no shared full tile. The small X also has no new event or full tile:
its upper endpoints start two rows below the near terminal; for the left
frame H=6 the only possible far adjacency crosses the -5/-4 tile boundary.

For right d>=8, any far column inside the P^0 or K breadth must stop above
its first old endpoint. Those columns have no preceding occupied partner
in their physical tile strip. The sole exception is C=w+13, whose partner
column w+12 contains the P^0 near stem starting at row-8. When its endpoint
reaches R+f=-8+2m, the new tiles have minima

    (-7+2j,w+12), j=0,...,m-1,

and the new events are

    T:(j,w+13) -> P^0:(j,w+12), j=-8,-6,...,-8+2m,
    P^0:(j,w+12) -> T:(j,w+13), j=-7,-5,...,-9+2m.

The second list and tile list are empty at m=0. Their counts are m and
2m+1, giving signed debit-1. For f<d-4 there is no overlap with P^0.
This proves all deep rows of the receipt table.

At right d=6, the lower bar row-9 is adjacent to P^0 row-8. The band adds
the two directions between(-9,c) and(-8,c) for every c=1,...,w+12.
All targets survive the ORIGINAL support exclusions. In the wide case its
full tiles have minima(-9,2j), j=0,...,(w+10)/2. The leftmost is completed
by T's near stem, whereas the final P^0 column w+12 lies in a partial
tile. Adding the two lower near-stem tiles and the five near events gives
DeltaF=w/2+8, DeltaE=2w+29.

At the special width H=w+14, the far stem additionally completes the
corner tile(-9,w+12), and f=4+2e adds the e+1 lower far-stem tiles
(-7+2j,w+12), j=0,...,e. Its events are the odd absolute-row T-to-P^0
and even absolute-row reverse directions in that strip:3+2e events.
In relative rows these lists are T-to-P^0 at-8,-6,...,-6+2e and
P^0-to-T at-7,-5,...,-7+2e. These are disjoint from the
bar band and near-stem lists. This proves the last two rows and hence all
Delta formulas in Section1.

For completeness, a legal north T has no intratile interaction with the
replacement tail J. A left T has far column<=-5; its near stem ends at-4,
two rows above J's first endpoint. A right T with far column inside P^0
must stop above-8 and also ends above J. The other right far columns are
at least w+13, beyond J's largest column w; their bars remain above the
old inventory. Thus replacing X by J changes neither classification nor
the new tile/event sets. The inequalities in(2) and its tail version follow.

## 4. Why the single-block gains cannot simply be added

Return to the FULL arbitrary-length H3 chain of the accepted note, with
independent even w_i>=12,z_i>=24, recurrence a_(i+1)=a_i+z_i-6,
s_(i+1)=s_i-w_(i+1)-12 and even root h>=6.

Choose even H_(n-1)>=6 and, backwards, arbitrary even widths satisfying

    H_i>=H_(i+1)+w_(i+1)+14.                        (3)

Choose any odd R_0<=a_0-2n-12 and set R_i=R_0+2i and
d_i=a_i-4-R_i. Adjoin the FULL originals

    T_i=U(H_i,d_i,4), chart(R_i+r,s_i+1-c).          (4)

All d_i are even and at least10; d_(i+1)-d_i=z_i-8>=16. Each T_i
consumes its own t_i. These consumers and H3 have pairwise disjoint
endpoint sets. Every T_i considered ALONE against the full old H3 has

    DeltaPhi(T_i | H3)=H_i-1.                      (5)

Nevertheless adjacent T_i bars generate an exact additional signed debit

    2DeltaF_cross-DeltaE_cross=-(H_(i+1)+2).        (6)

**Nested joint compensation theorem.** The exact joint gain is

    Phi(H3 union all T_i)-Phi(H3)=H_0-3n+2.        (7)

Here H_0 is the first consumer's BREADTH, not the earlier inventory name.
Every source mass H_i-1 is included once. After inserting T_0, each T_j
for j>=1 has incremental gain-3 in the increasing-index insertion order.
Thus even this later forced-consumer stage can have a negative marginal,
despite the positive single-block theorem. Equation(7), rather than the sum
of(5), is the valid compensation calculation.

Condition(3) implies H_0>=6+26(n-1), hence

    H_0-3n+2>=23n-18>=n.                          (8)

The full chain's original relative deficit is therefore compensated by
this entire nested family. The result is an exact full-original construction
and conditional compensation rule for these specified actual owners; it is
not a classification of arbitrary multi-block actual consumers.

## 5. Proof of the nested ledger and nonreuse

Put ell_i=s_i+1-H_i, the odd far column of T_i. Condition(3) gives
ell_i<=ell_(i+1)-2. The bar interval[ell_i,s_i] strictly contains the next
bar interval[ell_(i+1),s_(i+1)], with at least two columns to its left and
at least24 to its right. The bars occupy rows R_i,R_i+1. Each T_i near
stem is to the right of every later bar; its four-deep far stem is left
of every later bar. Later stems start below earlier bars. Thus there are
no endpoint collisions among the consumers, even when their near stems
are arbitrarily long. Nonadjacent consumers share no endpoint tile or
intratile adjacency. Adjacent consumers have only their bar-band contact.

All bar and far-stem endpoints have row at most

    R_(n-1)+4<=a_0-10.

Every H3 endpoint has row at least a_0-8, so those endpoints have no old
intratile contact. Only T_i's near stem can contact H3. Earlier base/repair
originals lie to its right; later old originals start below its terminal
row a_i-4. Its sole local contact is with P_i^0, with the two-full-tile/
four-event left-frame receipt of Section3. This proves(5) against the
WHOLE old H3, not just an isolated local block. The root is also to its
right, and all original supports are retained unchanged.

For an adjacent pair let j=i+1. The lower row R_i+1 of T_i and upper
row R_j=R_i+2 of T_j lie in one physical tile row. Over each column in
[ell_j,s_j], both directions across these rows survive. For T_i the target
has intrinsic row2 and an interior column, because its two stems lie
outside this interval. For T_j the target has intrinsic row-1. Neither
is an original support. There are exactly2H_j events.

The overlap begins at odd ell_j and ends at even s_j. The complete physical
column pairs are therefore

    [ell_j+1,ell_j+2], ..., [s_j-2,s_j-1],

giving H_j/2-1 full tiles. Both extreme tile columns have only three
endpoints. T_i's far stem is two or more columns to the left, so it does
not fill the missing extreme cell; its near stem lies to the right. There
are no other endpoints in the remaining boundary cells. These counts prove
2(H_j/2-1)-2H_j=-H_j-2.

Different adjacent-pair bands are distinct physical tile rows, and all lie
above the old H3 inventory. Their full tiles and directed events are
disjoint from the individual near-stem receipts. Thus the exact SET
partition gives

    sum_i(H_i-1)-sum_(j=1)^(n-1)(H_j+2)=H_0-3n+2.

The same partition at each prefix proves the-3 marginal assertion. Telescoping
(3), w_i>=12 and H_(n-1)>=6 proves(8). The wide outer original pays the
net contact loss; the child masses are canceled in this single joint ledger,
not credited a second time to a local certificate.

The tail-J replacement also has no contact with these T_i: their far stems
and bars lie above every old original, their near stems end at a_i-4, and
J starts at a_(n-1)-2. Its known-4 debit remains a separate term. Combining
(7)-(8) with the accepted base ledger gives a compensated tail value at
least sum_i(w_i+9)+h-5>=sum_i(w_i+9)+1.

These compensated inventories remain incomplete. The last E original axial
support(a_(n-1)-1,s_(n-1)+w_(n-1)+13) is absent and retains its three
endpoint neighbors. The north consumer near stems end above it, and their
other endpoints lie above the entire old inventory. No complete extension
or absolute negative-Phi example is asserted.

## 6. What is proved and what is still needed

The single-block theorem removes the specified-shape hypothesis for the
actual t-owner and proves the full unbounded parameter classification. The
nested theorem handles arbitrarily many overlapping contact bands with one
joint source budget and shows exactly why marginal positivity cannot be
propagated by simply adding local inequalities.

Arbitrary multi-block consumer shapes, all their signed exterior interactions
and global allocation remain open. In particular(7) is proved under explicit
nesting and bar-row hypotheses, not inferred for all actual consumers from a
finite search. The submitted11October manuscript and primary star-forming
results remain unchanged; the global5/6 improvement and rectangular-grid
triple equality are still open.

The companion verifier checks exact full-original tile/event SETS and all
role/phase boundaries. The standalone
[Lean source](../formal/SubQuorum/SecondaryTenArbitraryConsumers.lean)
checks local collision witnesses, parity, receipt arithmetic, gain cases and
the arbitrary-list nested ledger and width budget:48declarations,36theorems,
all passed locally with individual ordinary-axiom audits. Catalogue
completeness and geometric cardinality partitions remain ordinary proofs.
The entire written note received independent ACCEPT; the two nonblocking
tile-count/parity prose clarifications were applied without changing the
theorems or receipts. See the separate
[validation record](../output/secondary-ten-arbitrary-consumers-validation.json)
and [written review](../output/secondary-ten-arbitrary-consumers-review-response.md).
