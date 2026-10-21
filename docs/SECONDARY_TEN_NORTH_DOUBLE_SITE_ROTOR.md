# One negative rotor consumes two forced sites and repairs the remaining loss

21 October 2026. Owners: Haobo Ma and Wenlin Zhang. This conditional
construction is subsequent to, and OUTSIDE, the initial independent
review input for the [return closure note](SECONDARY_TEN_NORTH_RETURN_CLOSURE.md).

Retain its nine exact original owners Q,D,L,C,E,W,T0,T1,T2, with
b even, a=b-9 odd and even w>=12. Their common Phi=N+Rraw is1
below Q/D/W. The two missing right-side original supports are

    y=(a-1,w+13), owned originally as a support by E,
    z=(a+1,w+14), owned originally as a support by C.

They each have two occupied endpoint neighbors: T2 west/E south for y,
and E west/C south for z. Therefore both must be consumed in a complete
extension. They need NOT have distinct consumers.

## Explicit same-owner repair for every width

Define ONE original rotor Z by the following endpoint and support sets.
The eight endpoints are

    (a-2,w+15),
    (a-1,w+13), (a-1,w+14), (a-1,w+15),
    (a,w+14),   (a,w+15),   (a,w+16),
    (a+1,w+14).

Its four matching edges join, in order,

    (a-2,w+15)--(a-1,w+15),
    (a-1,w+13)--(a-1,w+14),
    (a,w+14)--(a+1,w+14),
    (a,w+15)--(a,w+16).

Its eight ORIGINAL supports are

    (a-3,w+15), (a-2,w+13), (a-2,w+16), (a-1,w+12),
    (a,w+17),  (a+1,w+13), (a+1,w+16), (a+2,w+14).

Equivalently transform the standard rotor by negating its intrinsic row,
then translating by (a+2,w+12). This identifies Z as an allowed original
source, not just an arbitrary eight-point set.

Z is endpoint-disjoint from all nine fixed owners and consumes BOTH y,z.
Its original charge is -2, so it contributes no positive original owner.
Its exact insertion into the common inventory gives

    Delta S=2, Delta F=1, Delta Ev=2, Delta N=0,
    Delta Rraw=Delta Phi=2.                       (1)

Consequently this ten-owner partial family has Phi exactly1 ABOVE Q/D/W.
It repairs the displayed remaining loss1, with1 left only in this fixed
inventory. Neither complete realizability nor a globally unused credit
is asserted; arbitrary further original owners can add signed contacts.

## Proof and exact shared tiles

The endpoint columns of Z are at least w+13, whereas Q,D,L,W and all
three Tj end at w+12 or earlier. Its possible contact with T2 is across
the shared column pair w+12,w+13. C/E have only their far stems near
Z; their bars begin below Z except for their respective terminal tiles.
Direct coordinate separation leaves exactly two shared endpoint tiles.

Tile(a-1,w+12) previously contains T2's two near-leg endpoints and
E's far terminal at(a,w+13). Adding Z's y fills its fourth corner.
It adds precisely the events T2(a-1,w+12) to Z(y), and Z(y) to
E(a,w+13). The other two candidate directions are excluded: y is E's
ORIGINAL axial support, and(a-1,w+12) is Z's ORIGINAL support.
The old E-to-T2 event is retained and not counted as new.
Thus this tile contributes Delta F1, Delta Ev2, net0 to2F-Ev.

Tile(a+1,w+14) contains Z's z and C's far terminal(a+2,w+14),
with no full tile. Both directions meet ORIGINAL axial supports and
are excluded, so Delta F=Delta Ev=0. No other shared endpoint tile
exists. Z occupies five tiles, has four original matching edges, and
exactly four of its original supports lie in those tiles, namely
(a-3,w+15),(a-1,w+12),(a,w+17),(a+2,w+14).
Therefore charge(Z)=4+4-10=-2.
This proves all counts and (1) for every stated a,w.

This repair is conditional on the displayed actual original consumer
being Z; no unique-rotor or mandatory-rotor classification is claimed.
It shows that joint consumption and the signed reserve of a negative
original owner can repair a loss without increasing N.

## Remaining closure and verification scope

The three far-side supports(a+1,5),(a-1,4),(a-3,3) are still absent.
Z also has the absent original support(a-2,w+13), with T2 west and
Z south, so further actual closure remains necessary. This is a partial
source family, not a target counterexample or a proof of full equality.

The return-closure checker reconstructs this actual rotor, all endpoint
and original-support sets, the two new directed events and both shared
tiles in translated/large-width controls. This theorem was developed
after the first review request; that review cannot be cited for it.
No Lean result is claimed for its event count or its complete realization.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
