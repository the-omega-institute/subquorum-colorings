# A general compensation lemma when the persistent supports share a consumer

21 October 2026. This covers every allowed ORIGINAL joint consumer of the
persistent E/C support pair in either prescribed residual family. It uses one
joint original-owner ledger throughout. Separate consumers and global reuse
across different residual packages remain open.

## Exact assumptions and conclusion

Use the complete feasible original U/rotor model, retained original supports,
fixed tile phase, residual inventory A and functional Phi of
[the all-north-terminal note](SECONDARY_TEN_ALL_NORTH_TERMINAL_PAIR_CONSUMERS.md).
Thus a is odd,w>=12 even, A=Q,D,L,C,E,W,T0,V, and V is either
U(w+8,8,z),z even4..14, or U(w+10,8,z),z even>=16, in the established
frame. The existing deficit is Phi(A)-Phi(Q,D,W)=-1.

Let an arbitrary complete feasible U/rotor family F retain all originals of
A. Suppose that the two forced original supports

    e=(a,w+14),  t=(a+1,w+14)

are endpoints of the SAME actual original J of F. No bound is imposed on
J's dimensions, phase beyond its actual placement, or other originals of F.

**Joint-consumer compensation lemma.** There is a subinventory I of actual
originals of F, consisting of A,J and at most one additional original, such
that

    Phi(I) >= Phi(Q,D,W).

The added originals and their receipts are exactly those in the table below.
Every receipt is an increment of the same original-support/tile/event
functional. The subinventory I is not asserted to be complete. In particular
the conclusion does NOT imply Phi(F)>=Phi(Q,D,W), or the global allocation
inequality, without a separate signed exterior estimate.

## Complete classification at the joint terminal

The west neighbor of t is E's endpoint(a+1,w+13); its south neighbor is
C's endpoint(a+2,w+14). These keep their foreign owners. Since e is also
an endpoint of J, J has its own north neighbor at t. Its only possible own
neighbor sets there are therefore {north} or {north,east}.

In a U source, a terminal has one own neighbor; a leg-interior endpoint has
two opposite own neighbors; an outer bar corner has two perpendicular own
neighbors; every other endpoint has three. Opposite pairs cannot fit the
available north/east sites, and three neighbors are impossible. Up to leg
relabeling, every joint U consumer thus has exactly one of these four frames:

| Type | Intrinsic source | Placement of(r,c) |
|---|---|---|
| Right north terminal | U(h,ell,f) | (a+1-ell+r,w+13+c) |
| Left north terminal | U(s,ell,m) | (a+1-ell+r,w+15-c) |
| Horizontal bar corner | U(h,ell,f) | (a+1-r,w+13+c) |
| Vertical bar corner | U(h,ell,f) | (a+2-c,w+14+r) |

All dimensions have their usual legal even lower bounds. The matching and
support sets are transformed together with the endpoints. The original U
constructor is preserved by exchanging the two legs with bar reflection.
Thus this is a classification of originals, including their matching and
support data, not merely unlabelled endpoint silhouettes.

For a rotor, the inner endpoints have three own neighbors and cannot occur
at t. A joint terminal must point north. The two north-terminal rotor forms
are the only remaining catalogue images. One contains t+(-1,-1)=(a,w+13),
an E endpoint, and is blocked. The other is exactly

    Z(r,c)=(a+2-r,w+12+c)

applied to the standard rotor. No other rotor role survives. This argument
uses the explicit full D4 catalogue, not a bounded U census.

## Exact receipts and the one exceptional continuation

| Actual joint consumer J | DeltaPhi(J\|A) | Additional original needed |
|---|---:|---|
| Right north-terminal U, any legal dimensions | 1 | None |
| Allowed rotor Z | 1 | None |
| Horizontal bar corner of breadth h | h-2>=4 | None |
| Vertical bar corner | 1 | None |
| Left north terminal, outside its two zero boundaries | 1 | None |
| Left north terminal, on either zero boundary | 0 | Actual consumer L at p, gain at least4 |

The right-terminal and rotor receipts were proved in the
[persistent-pair note](SECONDARY_TEN_PERSISTENT_PAIR_COMPENSATION.md).
The exhaustive left-terminal classification, including all widths and both
leg lengths, is proved in the
[all-north-terminal note](SECONDARY_TEN_ALL_NORTH_TERMINAL_PAIR_CONSUMERS.md).
Its only zeros are the V-bar contact m=ell-8 when g=w+15-s lies in V's
bar, and the escaped Q-tip contact g=3 in the first residual, m=ell+8.
They force the absent support p=(a+2,w+12) to be consumed by a further
actual original L. The exact L criterion is

    L=U(h,d,f), (r,c)->(a+2-d+r,w+13-c),
    6<=h<=s-4, 14<=d<=ell-2, 4<=f<=d-10.

It gives DeltaPhi(L|A+J)=h-2>=4. The source L differs from every original
of A and from J, since p is an endpoint of none of them. Additional originals
of F cannot remove the forcing condition or a fixed endpoint collision.

## Corner charges and contact proofs for arbitrary dimensions

Both corner frames lie at columns at least w+14 and rows at most a+1.
The earlier originals other than C end at column w+13 or earlier. C's only
endpoints in column w+14 start at row a+2. Thus both frames are
endpoint-disjoint from A for every legal dimension. Their sole shared
endpoint tile is T(a+1,w+14), containing C's far terminal(a+2,w+14).
No endpoint tile at a different column or row can meet an old endpoint.

For the horizontal corner put H=(ell+f)/2. Its two bar rows cross tile
boundaries, while its even-to-odd bar columns align. The exact original
counts are

    matching=h+H-1, endpoint tiles=h+H-2,
    original supports in those tiles=H-2.

The counted supports are precisely the odd-indexed inward lateral supports;
both axial terminal supports and both bar-corner supports lie outside its
endpoint tiles. Thus its original charge is1-h. At the sole shared tile,
the surviving event is J:t->C:(a+2,w+14). The reverse targets C's original
axial support t. C's terminal is not an original support of the horizontal
corner: its intrinsic coordinates are(-1,1), outside the original support list. The tile
has three endpoints and does not become full. Therefore DeltaS=h-1,
DeltaEv=1,DeltaF=DeltaN=0, giving h-2.

For the vertical corner the counts are

    matching=h+H-1, endpoint tiles=h/2+H+1,
    original supports in those tiles=H+4.

The four bar-corner/axial supports and all H even-indexed outward lateral
supports are counted; odd-indexed supports lie outside the endpoint tiles.
Its charge is+1. Now C's terminal IS the transformed bar-corner support
of J, while t is C's axial support. Both directions in the sole shared
tile are excluded. Thus DeltaN=1,DeltaS=DeltaF=DeltaEv=0, giving1.

## Proof of the joint-consumer lemma and scope of nonreuse

The complete role classification puts actual J in one table row. In every
nonzero row retain I=A+J. Its increment is at least1 and repairs the old
deficit1. In a zero row, completeness forces the actual additional L,
and retain I=A+J+L. The two increments are0 and at least4, so this joint
subinventory is at least3 above the baseline. This proves the lemma.

There is one receipt per inserted ORIGINAL, using original support exclusions
even after consumption. J may consume e,t and other outstanding supports;
none of these sites supplies a separate credit. In a zero row J's positive
owner unit and its unique V/Q contact debit are kept in the prefix when L
is inserted. L's three events and single new full tile are counted once.
No compensation is borrowed from a different hypothetical consumer or tile
inventory. Repeated support incidences do not create additional owners.

This establishes nonreuse inside THIS prescribed package. It is not an
injection assigning disjoint original-owner budgets to every residual package
in a larger F. If e and t have distinct actual consumers, the present lemma
does not apply. That separate-consumer case, interactions of multiple packages,
and arbitrary signed exterior contributions remain explicit global obligations.

Finite controls reconstruct both corner source phases and all exact events,
and corroborate the complete joint role classification with the full bounded
endpoint-role library and explicit rotor orbit. The all-parameter proof is
the role and interval argument above. The north-terminal proof has a separate ACCEPT verdict. A followup review
of this final joint-role theorem is pending; no verdict for it is presumed.
