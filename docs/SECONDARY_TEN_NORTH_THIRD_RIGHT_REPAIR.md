# A third right-pointing consumer repairs the displayed external loss

21 October 2026. This is a subsequent restricted compensation theorem for
the all-width six-source family in the [negative cavity note](SECONDARY_TEN_NORTH_OUTWARD_CAVITY.md).
It is outside both earlier independent-review inputs. It is proved by the
general tile partition below; finite checks are corroboration only.

## Statement and exact hypotheses

Let b be even, a=b-9, and w>=12 even. Retain the exact original Q,D,L,C,E,W
from that six-source family: t4,v6, C=U(8,6,4), E=U(6,4,4) and
W(r,c)=(a+1+c,w+1+r), U(6,4,4). All endpoints, supports, original
matching and aligned tiles retain their preceding definitions.

The next absent original support is p=(a+2,w+10). Condition on its
actual original consumer being the right-pointing north-terminal U

    R=U(k,ell,z), R(r,c)=(a+2-ell+r,w+9+c),

with arbitrary legal even k>=6, ell,z>=4. The theorem does not presume
this orientation for every complete extension. No complete realization
of this partial family is asserted. R is endpoint-disjoint from all six
fixed owners for all these parameters. Its terminal's original supports
are consumed by D to the west and E to the south. Its charge is1-k,
so it adds NO positive original owner to N.

Put I=[ell=4] and J=[k=6 and z>=ell], with brackets denoting0/1.
Adding R to Q/D/L/C/E has the exact reserve increment

    Delta Rraw=k-1-I-J>=3.                    (1)

The same increment holds with W present. Since the six-source package
with W had Phi=N+Rraw lower than Q/D/W by3, the seven-source family obeys

    Phi(Q/D/L/C/E/W/R)>=Phi(Q/D/W).           (2)

Equality in (1) occurs at k6,ell4 for every legal z. There is no additional
global credit: this pays the previously exhibited loss. Arbitrary further
owners can contribute signed external terms; they cannot be discarded.

## General proof by exhaustive shared tile types

R's near column is w+10 and its far column is w+9+k>=w+15. Its two
bar rows are a+2-ell and a+3-ell, both at or above a-1. D's last
column is w+9, in the preceding tile column pair. L's last column is
w+6; Q's last endpoint column is11. Thus R has no shared endpoint tile
with D,L,Q. Its bar lies above all C endpoints that could share a tile
column. E has its near stem in the preceding column pair and its bar
in the next tile row below R's terminal. These contacts also share no
endpoint tile. The only possible exceptions are the following two types.

First, if ell=4, R's lower bar row is a-1 and E's far terminal is at
(a,w+13). They share one tile with lower coordinate(a-1,w+12), of
endpoint partition2R+1E. It gains no mixed full tile. It has exactly
one event R to E: the reverse direction meets E's ORIGINAL axial terminal
support. For ell>=6 these endpoints occupy different tile rows.
This contributes Delta F0 and Delta E=I.

Second, only k=6 puts R's far column w+15 in the same tile pair as
C's far column w+14. C starts in this column at row a+2 and ends at
a+6. R reaches row a+2-ell+z. It therefore meets C's first tile exactly
when z>=ell. That tile, with lower coordinate(a+1,w+14), has2R+1C
endpoints. There is one event R to C: the reverse direction meets C's
ORIGINAL lateral terminal support. It contributes no full tile and one
event. If z>=ell+2, the next tile has2R+2C endpoints and contributes
one full tile and two events. If z>=ell+4, the final C tile has the
same counts. At the bar junction and endpoints, the excluded directions
are still ORIGINAL supports; no exclusion is changed by consumption.
There are no later C endpoints. Let d be the number of these latter
two full tiles, so d=[k=6,z>=ell+2]+[k=6,z>=ell+4]. The second type
contributes Delta F=d and Delta E=J+2d.

For k>=8 R's far column is in a tile pair strictly beyond every C/E
endpoint. Its arbitrarily long far leg can therefore add no other
contact. R is in the width-negative phase, with no original full tile;
source endpoint disjointness also rules out any reclassification of an
old full tile. This exhausts all shared endpoint tiles for every ell,z.

Thus Delta S=k-1, Delta N=0, Delta F=d and Delta E=I+J+2d. Substitution
into Rraw=S+2F-E gives (1). Since k>=6 and I,J<=1, its lower bound is3.
W's endpoint columns are at most w+5, while R starts at w+10, so no
R/W endpoint tile or event exists. This proves the same increment with
W present and hence (2), using the previous exact external loss3.

This establishes a genuine repair mechanism for ONE actual continuation
of the displayed obstacle. It leaves the other orientation, arbitrary
larger source families, global simultaneous nonreuse and the unrestricted
allocation/grid problem OPEN. In particular, a negative original owner
may increase physical reserve; its negative charge is not a reason to
discard it or count it as a positive owner.

## Verification scope

The checker directly reconstructs endpoints, original supports, full tiles
and directed events for separated dimensions and both with/without W.
Scoped Lean verifies the exact algebraic cancellation and lower bound.
The geometric shared-tile partition and complete-source interpretation are
written. This theorem was developed after both earlier review inputs;
neither earlier ACCEPT nor a live review is asserted to cover it.
See the [checker](../develop/check_secondary_ten_north_gap_four_package.py),
[512 finite controls and prior branch controls](../output/secondary-ten-north-gap-four-package-controls.json),
[scoped Lean source](../formal/SubQuorum/SecondaryTenNorthGapFourPackage.lean)
and [formal scope receipt](../output/secondary-ten-north-gap-four-package-formal-check.json).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
