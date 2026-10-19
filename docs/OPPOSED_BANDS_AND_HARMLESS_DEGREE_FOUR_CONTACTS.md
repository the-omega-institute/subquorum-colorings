# Opposed bands: unbounded degree-four overcount with exact compensation

20 October 2026. The broad degree-four count is a sufficient test, not a
necessary resource cost. We construct fully frozen feasible physical fusions
with fixed negative module mass S and J=0 but unbounded d4. The exact loss
K_in+L stays one. Thus d4<=S+2J cannot hold automatically for all such fusions,
even though the finer compensation criterion and the target inequality hold.
The conclusions below have proofs for every stated width and height.

## 1. Definitions and statement

Use the original corrected receiver charge and physical tile partition
Q_ij={2i,2i+1}x{2j,2j+1}. For supported original modules with disjoint
endpoint sets, occupied endpoint degree exactly three, and feasible retained
supports after fusion, the established exact ledger is

    rho = sum_i rho_i - 2J + K_in.

Here J counts new mixed FULL PHYSICAL TILES; K_in counts degree-four endpoints
whose unique new occupied neighbor is in the SAME tile. Let N_+ count positive
modules, S=N_+-sum_i rho_i, and L count positive modules with at least one
canonical protecting endpoint raised to degree four. The surviving distinct
donors and the nonduplicated loss theorem give

    sigma := mn/2-|T|-|M| >= S+2J-K_in-L,
    K_in+L <= d4.

All these quantities are those of DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md.
No new degree-four tax is introduced.

**Opposed-band theorem.** For every even w>=6 and even h>=4 there is a
fully frozen feasible fusion in an (h+4)-by-(w+4) rectangle with

    rho_A=1-w, rho_B=1, S=w-1, J=K_in=0, L=1,
    d4=2h+4, rho=2-w,
    sigma=h(w-4)/2+2 >= w-2 > 0.

The finer compensation credit is w-2, independent of h. At w=6 the coarse
condition asks 2h+4<=5 and fails for every h>=4. Its excess 2h-1 is unbounded.
The target holds strictly throughout. This refutes automatic validity of
the coarse rule; it does not refute its sufficiency or the target inequality.

## 2. Complete physical construction and feasibility

Work first in unshifted integer coordinates. Let A=two_leg_case(w,h,h).
Let B be two_leg_case(w+2,h+2,h+2) transported by

    H(r,c)=(h+2-r,c-1).

Take the union of their matchings, and keep all original selections except
those consumed by the other module's endpoints. Translate everything by
(1,1) at the end. Endpoints before translation are exactly

* A: rows0,1 and columns1 through w, together with (r,1),(r,w) for2<=r<=h;
* B: rows h+1,h+2 and columns0 through w+1, together with (r,0),(r,w+1)
  for0<=r<=h.

These endpoint sets are disjoint and each original module is supported and
individually feasible with occupied endpoint degree three. The final retained
selected set is exactly

    {(-1,0),(-1,w+1)}
    union {(r,-1),(r,w+2): r=0,2,...,h+2}
    union {(r,2),(r,w-1): r=3,5,...,h-1}.              (5)

Every selection in the first two groups touches just its B endpoint.
Every selection in the last group touches just its A endpoint. Horizontal
separation is at least three for the two interior columns when w>=6, and
successive selected rows within each column differ by two. Comparing the
displayed coordinates also excludes adjacency between groups. Thus every
selection has exactly one occupied neighbor. This proves final feasibility
directly, including h=4 and w=6.

The translated occupied sites fit in the claimed rectangle: before the
translation row coordinates run from -1 to h+2 and columns from -1 to w+2.
No extra selections or ambient padding are needed.

All foreign endpoint edges are

    (r,0)--(r,1), (r,w)--(r,w+1),     0<=r<=h,
    (h,1)--(h+1,1), (h,w)--(h+1,w).                  (6)

There are 2h+4 of them. No other cross-module endpoint pairs are adjacent.
In particular, the contacts use whole bands and corners, rather than
declared once-used leaf ports.

## 3. Exact losses, charges and the surviving finer bound

The degree-four endpoints, still before translation, are

    A: (r,1),(r,w),              r=1,3,...,h-1;
    B: (r,0),(r,w+1),           r=0,2,...,h;
    B: (h+1,1),(h+1,w).

Each gets exactly one new occupied neighbor, across the corresponding edge
of(6). The other foreign incidences replace original selected supports and
do not create degree-four endpoints. Thus d4=h+(h+2)+2=2h+4, and every other
endpoint still has occupied degree three.

After the (1,1) translation each horizontal band contact crosses a physical
tile boundary: the left columns become1,2 and the right become w+1,w+2.
Both cap contacts cross a row tile boundary, between h+1 and h+2. Therefore
EVERY new-neighbor event is intertile and K_in=0. Every mixed full unit
square contains one of the band seams, so no such square is an aligned
physical tile; J=0. Nonaligned unit squares are not added to J.

The phase table for two-leg modules gives rho_A=1-w and rho_B=1. B is a
tile-preserving image of the positive reference module, via the map
(r,c)->(h+3-r,c). Its canonical selected donor point (3,2) is sent to
(h,2), which is an A endpoint, namely the translate of(h-1,1). Thus that
particular selected support is consumed. Two of its protecting endpoints
acquire degree four; the third does not. There is exactly one positive
module, so L=1. Multiple affected protectors are not charged multiple times.
This also shows why retaining B's original donor cannot be silently assumed.

Consequently

    S+2J-K_in-L = (w-1)-1 = w-2,
    rho = (1-w)+1 = 2-w.

The exact physical counts independently confirm the result:

    |P|=4w+4h+4, |M|=2w+2h+2, |T|=2h+4,
    |R|=3w/2+2h+2, |T intersect V(R)|=2h+4.

Every selected site of(5) lies in the receiver in this alignment. The
receiver count follows either by listing its tiles, or from the old receiver
counts and the exact fusion identity; substitution gives rho=2-w. Direct
area subtraction gives

    sigma=(h+4)(w+4)/2-(2w+4h+6)=h(w-4)/2+2,
    D=sigma+rho=(w-4)(h-2)/2.

The inequality sigma>=w-2 follows from h>=4,w>=6. This checks both the
complete receiver identity and the strict target without spending a donor
or a degree-four event twice.

## 4. Uniform freezing proof

The certificate below works in the unshifted coordinates for every even
w>=6,h>=4. Write m for the actual union matching involution. A witness is
either in(5), or is m(v) for an earlier frozen v. Two distinct such neighbors
of an endpoint force it not to be promoted: if its mate-witness were absent,
the earlier endpoint would be promoted, contradicting its exclusion. This
is the general frozen-promotion induction, applicable to mixed bundles and
degree-four endpoints. It makes no uniqueness-of-matching inference at degree
four.

Use either side (outer o,inner i,exterior e,interior j) equal to

    (0,1,-1,2) or (w+1,w,w+2,w-1).

Perform the following stages. Within each indicated wave use the displayed
order. Witnesses refer only to previous stages or previous entries in that
wave; the two sides may be processed successively.

1. Freeze B(0,o) using selected(-1,o),(0,e). For even r=2,4,...,h, freeze
   B(r,o) using (r,e) selected and (r-1,o)=m(B(r-2,o)).
2. For odd r=3,5,...,h-1 freeze A(r,i) using selected(r,j) and
   (r,o)=m(B(r-1,o)). Then freeze B(h+2,o) using selected(h+2,e) and
   (h+1,o)=m(B(h,o)). Freeze B(h+1,i) using
   (h,i)=m(A(h-1,i)) and (h+1,o)=m(B(h,o)).
3. Sweep B's bottom bar from left to right: for c=2,...,w take r=h+2
   when c is even, otherwise r=h+1. Freeze(r,c) with witnesses
   (2h+3-r,c) and(r,c-1). The two seeds from stages1,2 start the wave.
   Sweep back for c=w-1,...,1, taking r=h+2 for odd c and h+1 for even c,
   with witnesses(2h+3-r,c),(r,c+1). Freeze the remaining B corners
   (h+1,o) using(h+2,o),(h+1,i). These are all bottom-bar endpoints.
4. Descend each side for even r=h,h-2,...,2. Freeze A(r,i) using
   (r,o),(r+1,i), then B(r-1,o) using(r-1,i),(r,o). At r=h both witnesses
   are mates of the now-frozen bottom-bar endpoints. Each succeeding step
   inherits its witnesses from the preceding two frozen endpoints. This
   finishes the stems and leaves both A(1,i) retained as mates of A(2,i).
5. Freeze A(0,i) with witnesses(0,o),(1,i). For c=2,...,w-1 freeze(r,c),
   where r=1 for even c and0 for odd c, using(1-r,c),(r,c-1). Sweep back
   through c=w-1,...,2, with r=1 for odd c and0 for even c and witnesses
   (1-r,c),(r,c+1). Finally freeze A(1,i) using(0,i),(1,j).

Each wave is the alternating bar matching, so the listed neighbor is the
mate of an earlier entry exactly as in the original two-leg certificate.
The seeds and end cases above handle both extreme widths and heights. The
stages are disjoint and contain all 4w+4h+4 endpoints. Every entry has two
distinct neighbors other than its own mate. Induction excludes every nonempty
feasible promotion bundle, including both colors and both ends of an edge.
The source opposed_band_certificate(w,h) implements these same ordered
stages, with no search in the certificate constructor.

## 5. All four alignment phases

For the same unshifted physical fusion, translate by a vector of parity
(a,b). Directly grouping the two bars and the two seams into physical tiles
gives the following table. The proof is coordinate counting of(5),(6):
each vertical side contributes one full tile per paired row when b=0;
the two cap events are intratile exactly when a=0. All side degree-four
events are intratile exactly when b=0. Hence J and K_in are as below.
The positive module and marked status follow from the established phase
table and the three protecting endpoints as in Section3.

| (a,b) | (rho_A,rho_B) | J | K_in | L | S | finer credit |
|---|---|---|---|---|---|---|
| (0,0) | (1,-w-1) | h+2 | 2h+4 | 0 | w+1 | w+1 |
| (0,1) | (-1,-w-1) | 0 | 2 | 0 | w+2 | w |
| (1,0) | (1-w,-1) | h | 2h+2 | 0 | w | w-2 |
| (1,1) | (1-w,1) | 0 | 0 | 1 | w-1 | w-2 |

Thus the finer sufficient criterion survives ALL alignments for all stated
parameters, while the coarse count fails in multiple alignments. Freezing
and feasibility are invariant under these translations and grid isometries.
The actual degree-four endpoint count is always 2h+4.

## 6. Verification, interpretation and next question

Run:

    python3 develop/check_degree_four_overcount.py --output output/degree-four-overcount-controls.json

The independent checker verifies20parameter pairs(w in6,8,14,40 and h in
4,6,8,20,80), every ordered freezing witness, exact physical ledgers and
640phase/symmetry images, plus80explicit checks of the four-phase formula
table. Sixteen canonical cases and248images fail the
coarse sufficient condition; zero fail the finer condition. These computations
support the separate all-parameter arguments above and do not replace them.

DegreeFourOvercount.lean contains the actual8-by10,44-endpoint,12-selection
configuration. Its67declarations and individual axiom audits pass locally
with Lean4.33.0. It checks physical coordinates, original and final local
degrees, feasibility, original charges,12degree-four endpoints, J=K_in=0,
L=1, the consumed original canonical support, and both criterion statements.
Its ordered FrozenPromotion derivation excludes every mixed promotion bundle
in this actual configuration. The general height-unbounded scalar arithmetic
is also formalized. General geometric counts, the all-width certificate and
the physical adapter for arbitrary parameters are written proofs, not claimed
as kernel-checked general geometry. Only standard propext, Classical.choice
and Quot.sound occur in its audit; there is no sorryAx or native_decide.
See output/degree-four-overcount-formal-check.json for the separate receipt.

The previous branched rotor review has completed ACCEPT, with exact original
SSE/terminal agreement, and is archived separately. It covers the older
once-used-port theorem. The later physical fusion theorem has its own review
task; neither review covers this still later opposed-band theorem. No new
external novelty or general grid/triple-equality claim is made.

This changes the next proof target. Automatic d4<=S+2J is false, even on
fully frozen physical template fusions, so it cannot be a universal bridge.
Use the directional intratile event count K_in and one loss per affected
positive module. The next question is whether K_in+L<=S+2J follows for
broader template contacts, or whether an actual failure needs further donor
recovery. General endpoint-component decompositions remain unproved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
