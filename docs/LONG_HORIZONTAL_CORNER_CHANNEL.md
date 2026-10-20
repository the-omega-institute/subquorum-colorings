# A permanent pair for arbitrarily long negative H companions

21 October 2026. The unrestricted allocation mu=N+R-G>=0 and rectangular-grid
triple equality remain OPEN. This note resolves a genuine unbounded subclass
of the negative H companions left by the
[all-length theorem](ALL_LENGTH_SINGLETON_COMPANION_INJECTION.md).
It also gives complete connected realizations with arbitrarily long
singleton and corner legs. Those realizations rule out an attempted blanket
exclusion of long H; their allocation margins are positive.

## 1. Model and the long-channel lemma

Use the finite complete original U/rotor model, unchanged original endpoints
and matching, and every original support retained unless consumed by an
original endpoint. Each retained selected point has exactly one occupied
neighbor, its original anchor. Source endpoint graphs are connected.
Widths are even and at least six; both independent leg lengths are even
and at least four. The chart preserves the fixed aligned physical tiles.

Suppose a complete family contains the two endpoint-disjoint negative owners

    B=U(6,b,e), B(r,c)=(b+3-r,c+1),
    H=U(d,b-2,k), H(r,c)=(r+3,c+2),
    b>=6, d>=6, k>=4, e>=b-2.                       (1)

Then the physical tile

    Q={4,5} x {4,5}                                (2)

permanently has exactly H's original irregular 2P0T pair at (4,4),(4,5),
and its other two positions are unoccupied. This holds under ANY complete
extension by arbitrary permitted U/rotors, with no bound on b, k, d, or the
number and dimensions of additional owners. Q supplies two units in the
existing exact defect sum 2R, not a new reserve pool.

In an actual normalized gate chain, B is the negative singleton consumer
at t=(3,2), C consumes p=(2,2), and H consumes y=(3,3). Thus (1) is the
subclass W=6, a=b-2, e>=b-2 of the unresolved H row of the all-length
catalogue. The proof of permanence needs only B and H, not A or C.

**Proof.** Endpoint disjointness first makes e=b-2. If e>=b, B's far leg
contains (3,7), while H's upper bar contains that point because d>=6.
Evenness and e>=b-2 leave exactly e=b-2.

The entire lattice boundary of

    D=[4,b+2] x [3,7]                              (3)

is endpoints of B or H. H's lower bar supplies its top side, H's near
leg supplies its left side, B's upper bar supplies its bottom side, and
B's far leg supplies its right side. The last leg starts at physical row
b+3-e=5; H supplies the top-right corner at row4. This checks the corners
as well as the side interiors. The left leg reaches row b+1, immediately
before the bottom boundary at b+2.

Neither owner has an endpoint strictly inside D. H's far leg lies in
column d+2>=8, and B's near leg in column2. Their bars lie on or outside
the horizontal boundary. The strict interior has columns exactly4,5,6.

If a foreign source had an interior endpoint, a lattice-edge path in its
connected endpoint graph to any noninterior endpoint would visit the
already occupied boundary. Endpoint uniqueness forbids that. Its entire
endpoint graph would have to fit in three columns. Every permitted U has
column extent at least five in every orientation, and every rotor has
column extent four. Neither fits. Thus there are NO interior endpoints
of any owner. This argument applies separately to every foreign source;
several sources cannot collectively cross the fixed endpoint boundary.

Both (5,4) and (5,5) are strictly inside D. A selected point at either
position would be adjacent to H's endpoint immediately above. Since each
selected point keeps its unique original endpoint anchor, H would have
to be its support producer. H has neither point as an original support:
their original coordinates are (2,2) and (2,3), while the only supports
on original row2 are in columns0 and d+1. Therefore neither point can
be selected. H originally has just (4,4),(4,5) and no support in Q,
so its permanent profile is precisely 2P0T. This proves (2).

For b=6 this overlaps the old short-H certificate. For b>=8 the enclosure
may have arbitrarily many rows; it is its THREE COLUMNS, not a three-row
bound or a finite search, that supply the proof.

## 2. Injective payment and simultaneous nonreuse

Assign an actual marked-side claim satisfying (1) the pair Q at the
corresponding H corner. This assignment is injective, including jointly
with old short-H claims.

Indeed a physical pair has its unique original endpoint owner H. Its
original lower-bar row and position next to a bar end determine which
intrinsic upper corner y of H is used, and its outward orientation.
For the two opposite bar ends the adjacent first pairs have columns
{4,5} and {d,d+1}; they are distinct even at d=6. At the reconstructed y,
the west original terminal is the actual B endpoint t, while the north
original straight-leg endpoint belongs to C. The known gate reconstruction
then fixes the positive producer: of the external anchors (3,1),(4,2),
the latter is B-owned, leaving only (3,1). Unique original ownership and
canonical-gate uniqueness fix the marked side. A new long claim cannot
repeat a short claim on the same pair: reconstruction would give the same
B incident length, both b>=8 and b=6.

Let P be the UNION of distinct physical lower pairs certified either by
the old corridor enclosures or by (1), and let p=|P|. Let s count the
union of old short-H and new long-channel H claims. Then s<=p. The set
union is essential: a tile independently certified by several arguments
is still just one pair.

The new pairs are disjoint from the established upper pairs: for the same
owner the intrinsic upper/lower bar rows differ, while different owners
cannot share the two endpoints. They are disjoint from caps and m8 triple
receipts because they contain exactly two endpoints. They contain no
original terminal and are not canonical positive gate tiles, by the same
owner/profile argument as for the earlier lower pairs. In particular,
when a blank corner of Q was an original support of a retained positive
source, support retention would require it to be occupied, contrary to
the permanent profile. Activation occurrences remain in their existing
separate summand of the exact identity, with no new copy of activation.

With q the accepted joint activation claims, c certified cap claims and
t every remaining negative claim, use ONE complete family throughout:

    G=q+c+s+t <= 2(N-n0), q<=Aactivation, s<=p,
    2R>=Aactivation+m8+c+2p+2u.

The previous integer calculation now applies to this enlarged PHYSICAL
pair union:

    mu>=n0+u+p+ceil((m8-s-t)/2),
    s+t<=2n0+2u+2p+m8+1  ==>  mu>=0.                (4)

If a newly resolved claim supplies a pair not previously in P, then p
increases by one while that claim moves from t to s, leaving s+t fixed.
Thus this certified floor rises by one, and the sufficient threshold
rises by two. If the pair was already in P, no new capacity is added;
merely renaming its claim is not a numerical improvement. No per-component
copy of p, R, or any receipt is permitted. For component-loss applications,
apply the enlarged permanent floor once in the family containing all losing
added components, exactly as in the prior corridor theorem.

On complete configurations satisfying (4), the established sigma>=mu
gives matching coefficient one, improving the existing5/6 by |M|/6.
Universal residual coverage and an arbitrary-grid decomposition remain
unproved. This note proves neither the whole target nor an improvement
for every rectangular grid.

## 3. Complete connected H realizations at every incident length

Let z>=0 be any EVEN integer. The following eleven original U sources
form a complete connected family F_z:

| Owner | Dimensions | Original-coordinate map |
|---|---|---|
| A | (12,4,4) | (r,c) |
| B | (6,6+z,4+z) | (9+z-r,c+1) |
| C | (14+z,8,4) | (c+1,10-r) |
| H | (6,4+z,4+z) | (r+3,c+2) |
| E | (6,4+z,4+z) | (r+5,c-5) |
| F | (6,4,8) | (r-4,c-6) |
| J | (6,6,6) | (c+15+z,r+6) |
| K | (8,4,8) | (5-c,17-r) |
| L | (10,4,4) | (6-r,c+10) |
| M | (10,4,6) | (14+z-r,c-2) |
| Q0 | (10,6,6) | (21+z-r,c-5) |

Every source retains its original matching and ALL original supports,
except supports consumed by the displayed original endpoint union.
F_0 is the previously checked complete eleven-source H witness.

Here is an all-parameter insertion proof, rather than extrapolation from
checked z values. In the full endpoint and final selected sets of F_0,
move every point of row>=7 down by z. In the inserted rows7,...,6+z,
the additional endpoint columns are EXACTLY

    -4, 1, 2, 3, 7, 8, 9, 10.

The additional RETAINED selected columns are

    odd rows:  {-5},
    even rows: {-3,0,4,6}.                          (5)

These formulas follow directly from the original source intervals. E
provides endpoint columns-4,1; B provides2,7; H provides3,8; C provides9,10.
On odd rows E's outer near support at-5 survives; E's outer far support2,
H's outer supports2,9, and B's outer supports1,8 are consumed by the other
displayed endpoints. On even rows E's inner supports-3,0, H's near inner
support4 and B's far inner support6 survive; H's far inner support7 and
B's near inner support3 are consumed. No other source meets the slab.
Every support is therefore accounted for, including supports consumed by
other original sources; no mandatory selection is silently dropped.

Each selected column in (5) has exactly one endpoint neighbor, its
horizontal anchor. None of its other horizontal or vertical neighbors is
occupied. The upper and lower slab interfaces have the same adjacent
endpoint/selected row patterns as the original upper interface and the
two-periodic internal pattern; z is even, so parity agrees at both ends.
All unchanged regions are translated copies of the feasible F_0 regions.
This proves selected-degree feasibility for ALL z. Original-source interval
disjointness follows from the same columns and the translated old endpoints.
Each F_z uses its sources' canonical original matchings for the displayed
new dimensions, so they are disjoint unit-edge matchings. The point-set
insertion identity does not assert that an F_0 matching edge crossing the
cut is translated as a single edge: the longer original constructor uses
its consecutive canonical pairing through that region.
Every endpoint keeps all three original occupied neighbors, since each
original support remains occupied. Thus this is a complete feasible family.

The old endpoint contacts outside the slab persist or are translated. Across
the slab each spanning source has its own connected endpoint graph. The
original owner-contact graph is unchanged or gains contacts, so connectedness
of F_0 proves connectedness of every F_z. The positive owners and marked
gates keep their original local geometry. In particular B consumes A's
negative-singleton gate, C consumes p, H consumes y, and (1) applies with
b=6+z, a=e=4+z. These are complete actual long-H occurrences for every
even b>=6, not merely endpoint-disjoint partial roles.

More explicitly, original row7 has exactly the slab endpoint columns and
the sole retained selection(7,-5), with the displayed ownership. Thus the
first inserted odd row reproduces that complete row. Old row6 has selected
columns4,6,21, all blank in the new row7, while row6 has no occupied point
at column-5. At the lower interface an even slab row meets translated old
row7, giving the same even/odd compatibility as internally. Every old
endpoint edge crossing rows6/7 has both ends in one of the eight slab
columns and both ends of the same original owner. In F_z each such edge
is replaced by an endpoint path THROUGH THAT SAME OWNER, which proves
connectedness without assuming that an arbitrary original edge persists.

Exactly eight endpoints occur per new row, with five selected points per
two-row period. Consequently

    |P|=278+8z, |M|=139+4z, |T|=62+5z/2.

The aligned physical tile ledger is also explicit. Every old tile with
first row>=8 is translated down by z, and old tiles at first row<=6 keep
the same endpoint and FINAL SELECTED-point profiles. Original consumed
support provenance can change: for example M's consumed support at(7,8)
moves to(7+z,8), while H still owns(7,8). Each extra two-row block beginning at
row8,10,...,6+z has exactly one nonzero NEW defect: C's exposed bar pair
in columns10,11 is irregular2P0T and contributes2. All other new receiver
tiles have regular or full profiles. Aactivation=4, U0=2 and Z0=0 remain
unchanged. The exact defect identity therefore gives

    N=3, G=2, R=26+z/2, mu=27+z/2.                 (6)

The source-specific assertions do not follow just from final occupancy.
Even z preserves all aligned phases. The positive sources A,F,K and ALL
their original endpoints/supports lie in rows<=5; their radius-one
neighborhoods lie in rows<=6 and are unchanged. Thus their marks and
terminal activations stay fixed. Only C and E have the both-shifted phase
with U triples: their original end-cap tiles persist or translate, with
the same fullness, while the new C bar tiles are pairs, not new caps.
This proves U0=2 separately. There are no rotors, so Z0=0.

Thus long H is genuinely realizable without any upper length bound.
These examples have POSITIVE margin and refute neither allocation nor
grid equality. They exclude the proposed shortcut that all b>=8 H
branches are impossible, and show the new lemma covers actual families.

## 4. Validation and remaining scope

The independent checker reconstructs original endpoints, supports and unit
matching edges, then verifies the enclosure, permanent pair, exact global
support formulas, local defect translation and complete-family ledgers.
It checks80 endpoint-disjoint two-owner patterns and256 phase/isometry images
of eight complete families, including b=66. Those controls supplement the
unbounded proofs in Sections1--3 and do not prove them by enumeration.
Among those images,64 preserve the physical tile partition; all64 new pair
certificates are also detected in the existing common lower-pair union.
The existing persistent-corridor certificate detector now recognizes the
long-channel first pair in the SAME deduplicated lower-pair set. Its old
short certificates and strip/cap counts retain their original definitions.

LongHorizontalCornerChannel.lean proves ten unbounded scoped declarations:
exact far-leg length, endpoint boundary, absence of boundary-owner interior
endpoints, connected unit-walk trapping in three columns, first-pair
coordinates, opposite-corner separation and the conditional integer bound.
All ten pass local Lean4.33.0 with individual axiom audits, session16726,
exit0, after60% free memory and no actual lean/lake by comm-basename check.
Only propext/Classical.choice/Quot.sound appear; no sorry/native reduction.
The U/rotor extent adapter, physical profile and marked-side injection,
all-parameter insertion/support and tile-ledger adapters remain written.
There is no end-to-end formalization of allocation or grid equality.

The open cases include H with wider B, unmatched H/B leg lengths,
Vcorner, filled corridors and vertical regular exits. The long-channel
lemma narrows the remaining claim set and supplies an actual permanent
receipt, but does not establish the universal coverage condition in (4).
Submitted manuscripts are unchanged.

Independent written review5a0cae69 completed ACCEPT for the initial channel,
joint nonreuse and all-parameter realization. Its11,900-character response
matches original stream51636 exactly, exit0, observed gpt_6/pro. The
interface, matching and source-provenance clarifications above incorporate
its recommendations. It does not certify execution. The subsequent
[four-column rotor barrier](FOUR_COLUMN_CORNER_BARRIER.md), which forces
the return length in a wider subclass, has a separate review scope.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
