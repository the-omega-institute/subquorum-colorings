# Frozen sparse ends can be arbitrarily far from a no-endpoint donor

19 October 2026. This note rules out a fixed-radius allocation rule for the
unmatched sparse ends in the boundary-flux ledger. It does not disprove the
global grid inequality. All distances below are Manhattan distances between
original physical tiles, not between vertices or shifted squares.

## 1. Statement and scope

Use the feasible pair (T,M), endpoint set P, complete-component receivers and
corrected physical charges of `COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`.
A selected vertex has at most one neighbor in T union P. A physical no-P
tile Q supplies its actual nonnegative deficit 2-|T intersect Q|.

**End-locality obstruction.** For every integer R>=1 there is an even
rectangular feasible pair with one prescribed positive long source and two
complete straight combs, all endpoints universally frozen, such that:

1. Both combs approach the source mouth from the same side and end there in
   sparse physical tiles. The whole receiver charges are +1,0,0.
2. Every physical no-P tile within distance R of either sparse end has
   deficit zero. The nearest positive no-P deficit is at distance exactly
   R+1 from each end.
3. Each comb has corrected charge -1/2 inside the displayed neutral patch
   and +1/2 outside. Its unique positive corrected tile is at distance R+1.

Thus no radius independent of the instance can guarantee a positive actual
no-P donor near every unmatched sparse end, even within this frozen class.
The claim concerns neighborhoods of the ends. It does not exclude donors
near other parts of the long source, distant allocation, or a proof that
repartitions signed charges while explicitly retaining every transfer.

## 2. Source, combs and the physical patch

All coordinates in the construction are raw coordinates until translated by
(row,column) -> (row+2,column+3). Put

    w=4R+14, h=2R+3, r=2h+2=4R+8, a=R+2,
    c=2R+4, d=c+5=2R+9, ell=R+1, N=(w-2)/2=2ell+4.

Use the complete long source of width w and depth h from
`LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`, without optional
interior saturation. Its endpoint set is

    ({0,1} x {0,...,w-1}) union ({2,...,r} x {0,w-1}).

For completeness, match the even/odd consecutive pairs in row 0; match
(1,1)-(1,2), (1,3)-(1,4), ..., (1,w-3)-(1,w-2); match the chamber corners
(1,z)-(2,z) for z=0,w-1; and match (3,z)-(4,z), ..., (r-1,z)-(r,z).
Select (0,-1),(0,w), the axial tips (r+1,0),(r+1,w-1), and, for
1<=j<=2h+1, select the two side supports at row j+1: columns -1,w when
j is odd, columns 1,w-2 when j is even.

Add two complete combs in columns c,d and rows r-2a+1,...,r, with consecutive
matching pairs starting at the first row. Their axial supports are
(r-2a,z),(r+1,z). At even rows the c-comb's side support is in column c+1,
and at odd rows in c-1; the d-comb uses d-1 at even rows and d+1 at odd rows.
All these supports are selected. No other endpoints or matching edges are
introduced. The first comb row is 2R+5, separated from the chamber. The
comb centers differ by five and stay clear of the source arms and supports.

The source mouth is {r,r+1} x {1,...,w-2}. A physical band at level q uses
raw row pair (r+2q,r+2q+1) and column pairs (1+2j,2+2j), 0<=j<N.
After the translation these are original even/odd physical tile pairs.
Let K be all these tiles for -R<=q<=R.

The following four-letter words list a tile's top-left, top-right,
bottom-left, bottom-right labels. B means blank, T selected and P endpoint.
Write A=TBBT, C=BTTB, L=TBTB, V=BTBT and H=BBTT. Superscripts denote
repetition of whole tiles, not vertices. Prescribe the band words

    -R<=q<0:  C^ell  BPTP  A  C  PBPT  A^ell
    q=0:      V^ell  BPBT  A  C  PBTB  L^ell
    q=1:      L^(ell+2)  C^(ell+1)  H
    2<=q<=R:  C^(2ell+3)  H.

Each word contains exactly N tiles. At R=1 the last range is empty. These
labels agree with the fixed endpoints and preserve every original support
in K. Add the indicated T vertices; retain the original source/comb supports
outside K; leave every remaining site blank. Translate as specified and use
the rectangle with (6R+14) rows and (4R+22) columns. All endpoints, supports
and displayed tiles lie inside it, as does one further outward blank band.

## 3. General feasibility and freezing

Here is a direct all-R verification of the words, including their interfaces.
It uses no search or extrapolation from controls.

Inside an inward band, the repeated diagonal tiles C and A have no horizontal
selected adjacency within their repeated regions. Their extreme lower
selected vertices at raw columns 1,w-2 see the intended source-arm endpoint.
Each full comb tile BPTP or PBPT contains its intended side support. The
upper selected vertices in the two central diagonal tiles see their intended
comb endpoints. Their lower selected vertices form one horizontal T pair,
with no other occupied neighbor. At transitions into the repeated diagonal
regions, the selected positions are separated by a blank column or the
intended endpoint. Consequently no selected vertex has two occupied neighbors.

In the mouth band the repeated V and L tiles are vertical selected pairs.
Each has only its partner as occupied neighbor. The sparse tiles BPBT and
PBTB contain the intended axial supports below the last endpoints. The
central A,C upper selected vertices see their intended comb endpoints,
and the central lower vertices again form one horizontal selected pair.
The repeated-region interfaces have blanks at the positions beside these
supports. The extreme mouth columns are blank as required by the source.

The first outward band consists of vertical pairs in L^(ell+2), isolated
checkerboard selected vertices in C^(ell+1), and a last horizontal bottom
pair H. The L-to-C and C-to-H interfaces introduce no selected adjacency.
Every later outward band is a checkerboard region C^(N-1) followed by H,
with the same property. These bands have no endpoints.

It remains to check adjacency between bands. Consecutive inward bands have
disjoint lower/upper selected column sets, by opposite parity in the repeated
regions and the explicit four central tiles. The same check applies from
the last inward band to the mouth. At these interfaces a full comb tile's
selected support lies beside an endpoint, not below a selected vertex.
The mouth's lower selected columns are exactly

    {2,4,...,c+2} union {c+3,c+5,...,w-3}.

The first outward band's upper selected columns are

    {1,3,...,c+1} union {c+4,c+6,...,w-4},

which are disjoint from them. The first outward band's lower selected
columns are all odd columns 1,...,w-3 together with w-2. Every later
band's upper selected columns are the even columns 2,...,w-4. Hence the
first-to-later and later-to-later interfaces also have no selected adjacency.
The only axial selected-to-endpoint contacts are the intended comb ends.

Above K the only selected vertices immediately against its top boundary
are original side supports, a subset of the lower selected pattern of a
preceding inward band. No new adjacency is introduced there. Below K all
sites in the next band are blank. At the two lateral boundaries the source
arms and their supports have the same compatible alternating pattern as
the inward words, and the mouth corners remain blank. Original supports
elsewhere retain their original single endpoint neighbor. This exhausts
all possible neighbors of every selected vertex and proves feasibility.

The original source and complete-comb supports have all been retained.
The general chamber-to-arm and comb retained-mate freezing waves therefore
apply in this feasible completion. Every endpoint is universally frozen,
so the pair is terminal even with respect to simultaneous feasible promotion
bundles. No endpoints of distinct prescribed components are adjacent.
The whole-receiver formulas give source charge +1 and comb charges zero.

## 4. Radius, matching transfers and exact counts

In translated physical tile coordinates put b=(r+2)/2=2R+5. The sparse
end tiles are (b,R+3) and (b,R+6), and K is the rectangular tile set

    {b-R,...,b+R} x {2,...,2R+7}.

For either end, the nearest excluded column is at least R+2 away and the
nearest excluded row R+1 away. Thus its entire radius-R tile neighborhood
lies in K. Every no-P tile in K is one of A,C,L,V,H and has exactly two T,
so every such deficit is zero. The next outward band, at level R+1, has
blank tiles in both end columns, each with deficit two. Its distance is
R+1. This proves the exact nearest-donor assertion separately for each end.

For each comb the initial endpoint has translated odd row 2R+7. Its top
physical singleton is saturated and lies at level -(R+2). The first matching
edge crosses into the full physical tile at level -(R+1). The corrected
charge convention transfers 1/2 from that saturated singleton to its actual
matching-partner tile: the singleton's corrected charge is zero and the
next tile's corrected charge is +1/2. All subsequent full comb tiles have
charge zero, and the bottom sparse singleton at level zero has charge -1/2.
Thus the patch contains exactly the negative half and misses the positive
half, which is at distance R+1. Whole comb charge remains zero.

This is precisely the omitted resource if one tries to spend the two local
negative halves and simultaneously treat each whole comb as neutral. The
outside corrected halves must be retained; they are not physical no-P donors.

There are (2R+1)N=4R^2+14R+6 patch tiles. Two per inward band and two in the
mouth contain endpoints, giving 4R^2+12R+4 no-P patch tiles. The patch has
8R^2+26R+10 selected vertices: two in each no-P tile and one in each endpoint
tile. Of the original 12R+30 supports, 6R+4 are inside the patch, leaving
6R+26 outside. Hence

    |T|=8R^2+32R+36,
    |M|=(w+2h+1)+2a=10R+25,
    |T|+|M|=8R^2+42R+61.

The half-area is 12R^2+94R+154, so the global deficit is

    mn/2-|T|-|M|=4R^2+52R+93 > 0.

In the boundary-flux notation B_source=1,O=2,J=0, and the mouth has
S=2,U=0,D=D'=0. The obstructed local part has balance -1, but the full
configuration has ample distant deficit. The global target is not refuted.

## 5. Reproduction and next question

Run from the repository root:

    python3 develop/check_frozen_end_locality_obstacle.py --output output/frozen-end-locality-controls.json

The explicit generator uses only the displayed words and formulas, not a
solver. The receipt checks R=1,...,12,16,24,40 and 24 symmetry images,
including transposition. It checks feasibility, complete freezing, whole
charges, counts, radius coverage, exact nearest donors and actual matching
transfers. The smallest full coordinates are included. These controls test
the independent general proof above; they do not establish it by enumeration.
No new Lean theorem or independent review is claimed for this note.

The useful remaining question is whether the unmatched sparse-end debt can
be routed to distant original donors with an injective allocation, perhaps
using geometry near the whole source rather than a fixed neighborhood of
each end. Any such argument must include both the physical donor capacity
and the positive halves exported by partial receiver cuts. The accepted
closed-network theorem settles the internally paired case; this construction
isolates a genuine limit on the next proposed local extension.
