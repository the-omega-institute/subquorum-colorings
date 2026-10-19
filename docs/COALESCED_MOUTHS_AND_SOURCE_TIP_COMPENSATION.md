# Coalesced mouths: source tips recover the payment lost by merging overlaps

19 October 2026. This extends the closed-network theorem to prescribed
positive long sources whose mouths overlap. The donors are counted on the
union once. Internal tips of other long sources replace the repeated boundary
terms, so the final bound still counts every source. Universal grids remain open.

## 1. Configuration and enlarged contact hypotheses

Use the even rectangular grid, feasible pair (T_0,M_0), physical tiling,
normalization and whole-receiver ledger in
`COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`. There are B prescribed complete
positive long sources, with their actual matching and all supports from
`LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`, Section 1, in any
tile-preserving orientation. Their source receivers have charge +1. The
two terminal tip tiles of each source are saturated, each containing one
P and two T. The source and complete-comb freezing results are granted here.

Every other complete initial endpoint component is thin, has at most one
P-square, or is a prescribed complete straight contact comb with all its
alternating side and axial selected supports. Thin means containment in two
consecutive rows or columns, as in the accepted receiver theorem.

For each source H let F_H be its usual one-tile-wide physical mouth. Impose
the following contact condition on every endpoint initially in F_H:

- It belongs to a prescribed complete straight contact comb whose axis is
  perpendicular to the mouth; or
- It is one of the two terminal tips of another prescribed long source K,
  and F_K is parallel to F_H.

In particular, a source chamber or nonterminal arm cannot enter any mouth,
and tips from a perpendicular source are excluded. No disjointness of mouths
is assumed. Contact combs and sources can be shared between several mouths.
We do not assert that arbitrary feasible configurations satisfy this condition.

Normalize to a single-terminal pair. Every prescribed source and contact comb
is frozen; their supports remain. Each mouth endpoint therefore persists,
and a promotion elsewhere cannot change any mouth label. The contact
condition, source shapes and mouths pass unchanged to the final pair.
Nonprescribed thin/one-square final receivers have nonpositive charge.
For all subsequent geometric arguments work at this terminal representative.

## 2. Perpendicular mouths cannot intersect

**Geometric lemma.** Under the contact condition, two mouths with
perpendicular directions have no common physical tile.

Proof. Normalize the first source to raw chamber rows 0,1, arm columns
0,w-1 and tip row r, so its mouth is

    {r,r+1} x {1,...,w-2},

and its chamber and arms enclose

    I={2,...,r-1} x {1,...,w-2}

on three sides. Suppose a perpendicular source K has a vertical mouth
intersecting this horizontal mouth. Both columns of its mouth then lie
strictly between the first source's arms. Its two tips have a common column
c in {1,...,w-2} and rows u<v. Because both mouths are unions of full
physical tiles and the vertical mouth lies strictly between its tips,

    u<=r-1, v>=r+2.

If u<=0, the vertical mouth contains a chamber endpoint (1,c) of H.
This is a foreign source endpoint with perpendicular mouth direction,
contrary to the contact condition for K. If u=1, K's upper tip already
belongs to H. Thus 2<=u<=r-1: one tip of K lies in I and the other outside.

The complete connected source K has a P path between these tips. The first
exit from I must cross its upper boundary row 1, its side boundaries columns
0,w-1, or its bottom boundary row r. The first three alternatives enter H
and join distinct complete components. The last enters F_H with a K
endpoint, again a foreign source whose mouth is perpendicular to F_H, which
the contact condition forbids. All alternatives are impossible. QED.

This proves exclusion using the complete source path, not using an assertion
that the overlapping tile is empty. Arbitrary other comb occupancy does not
affect the argument.

## 3. Merge parallel mouths and count source tips exactly

Group mouths in the same physical row band, or the same physical column band.
Within each band, take connected components of their union as intervals of
tile indices, merging adjacent intervals as well as overlapping ones. Call
the resulting strips G_1,...,G_C. Perpendicular mouths are disjoint by the
lemma, so these strips are globally disjoint and their union is exactly
the union of all original mouths. No new tile is introduced by coalescing.

For one horizontal strip, a source with mouth interval

    {L_H+1,...,R_H-1}

has its two terminal tip tiles at L_H,R_H. A vertical strip has the same
description after transposition. The tip tiles of distinct sources are
distinct: each physical endpoint tile at a terminal representative has a
single complete-component owner. A source's two tip tiles are distinct too.

If one strip contains b source mouths, let L=min L_H and R=max R_H. Its
tile interval is {L+1,...,R-1}. Exactly two of those sources' 2b tip tiles
are outside the strip: the unique extreme left and extreme right tiles
L,R. Every other tip is strictly between them, hence inside the strip.
An excluded extreme tip cannot belong to another strip: in the same band
that would make the two union components adjacent, while a perpendicular
mouth containing it violates the contact condition. Different parallel bands
have different tip row/column pairs. Consequently the exact number of source
tip tiles in the full union G is

    U_source=2B-2C.                                      (1)

All these tips are saturated in the original physical tiling, including
sources opening in opposite directions. This is the important replacement
for counting each original mouth's boundary twice.

Both vertex columns at the two extreme edges of a horizontal G_i are blank.
Indeed they are the extreme blank columns of the source mouths attaining
L and R. The usual next-arm and axial supports force these blanks, regardless
of whether the two extreme sources open in the same direction. The analogous
two rows are blank for a vertical strip.

## 4. The same two-tiling identity applies to every merged strip

Every endpoint-containing column in G_i is a full perpendicular contact-comb
column, a partial comb end, or a terminal source tip. Its physical tile type
is respectively (P,T)=(2,1),(1,1), or (1,2), with either partial comb type
allowed. Source tips have the last type. No tile contains two owners.

Partition after removing the two extreme blank vertex columns using the
one-column shifted squares, exactly as in
`COMB_END_FLUX_AND_CLOSED_CONTACT_NETWORKS.md`. A full column stays full;
sparse and saturated singleton columns exchange types. For a source tip,
its axial support and the alternating support of the next arm endpoint
force the two opposite-side corners blank, just as for a complete comb end.
The next arm endpoint always exists since the prescribed arm length is at
least three. Source tip types therefore obey the same type swap.

A shifted square cannot acquire two different endpoint columns. Adjacent
endpoints would join their complete components; diagonal singleton ends
would make an axial selected support adjacent to both endpoints. This also
handles a tip next to a comb and tips from oppositely opening sources.

Let S_i,U_i count sparse/saturated physical singleton columns in G_i, let
D_i be its actual physical no-P deficit, and let D'_i be the sum of 2-t over
shifted no-P squares. The exact selected/endpoint-weight count gives

    D_i=2-S_i+U_i+D'_i,       D'_i>=0.                    (2)

The constant is two per merged strip, not two per original source mouth.
Source-tip tiles are not donors: their contribution in (2) explains the
value of the existing physical no-P payment. D'_i likewise is an auxiliary
count, not a second set of allocated physical donors.

## 5. Source conservation, comb conservation and the global bound

For each complete contact comb, flag whether its sparse and saturated
physical end tiles lie in G. Define I,O,J by both, sparse-only and
saturated-only membership, as in the accepted end-flux theorem. A complete
comb has at most one singleton of each type, and the disjoint G_i give
unique membership. Thus

    S_comb=I+O,       U_comb=I+J.

All noncomb singleton columns in G are source tips. Equation (1) gives

    sum S_i=I+O,
    sum U_i=I+J+2B-2C.

Summing (2) over disjoint G_i cancels both the internal comb contacts and
the number of merged strips:

    D_total=2C-(I+O)+(I+J+2B-2C)+sum D'_i
           =2B+J-O+sum D'_i.                            (3)

Every prescribed whole source still has charge +1 and occurs once. Define
Remainder to be all other whole-receiver deficits plus all physical no-P
deficits outside G. The receiver theorem gives Remainder>=0. The original
physical ledger and objective preservation now yield the exact identity

    mn/2-|T_0|-|M_0|
      =-B+D_total+Remainder
      =B+J-O+sum D'_i+Remainder.                         (4)

**Coalesced-mouth theorem.** Under the initial hypotheses of Section 1,

    |T_0|+|M_0| <= mn/2-B+O-J.                          (5)

Coefficient one follows if O<=B+J. If every sparse comb end in G has its
saturated end there too, O=0 and

    |T_0|+|M_0| <= mn/2-B-J.                            (6)

This removes the whole |M_0|/6 loss from the universal 5/6 bound within the
enlarged covered class and gives the additional strict margin B+J when
closed. It permits any number of overlapping parallel mouths and all
tile-preserving source orientations; no laminarity assumption is used.

There is no repeated resource in (4). A no-P physical tile belongs to one
G_i or to the remainder. Each complete source and comb receiver occurs
once. Internal source tips are counted as endpoint types in the exact
formula for D_total, not as negative partial receivers. Signed matching
exports remain inside the whole receivers.

## 6. Explicit arbitrarily nested families outside the disjoint-mouth class

For every k>=1, index sources by i=0,...,k-1 and put l=k-i. Take width
8l+6, depth 2l+1, and translate the raw source origin to (4i,4i), before
the common physical translation (2,3). All sources open downward.
Every tip has common raw row 4k+4; consecutive chambers are four rows
apart and consecutive left/right arms four columns apart. Source supports
on neighboring arms have distance at least two; inner chambers and their
supports stay at least three columns from an outer arm. Consecutive chamber
bands are separated by two rows. Thus no selected support acquires a
second occupied neighbor, no P edge joins sources, and all matching/support
data fit in the (4k+10)-by-(8k+14) rectangle. Leave every unlisted site blank.
The existing source freezing waves apply independently in this completion.

Their mouth intervals are strictly nested, with one merged strip C=1 and
2k-2 internal saturated source tips. There are no contact combs, so O=J=0.
Equation (6) gives objective<=mn/2-k for every k. At every k>=2 the original
mouths overlap and the disjoint-mouth theorem's hypotheses fail. The number
of overlapping claims is unbounded.

The unaugmented family has |T|=4k^2+14k and |M|=6k^2+15k. Its merged
strip contains 4k+2 physical tiles, 2k-2 source-tip tiles and 2k+4 empty
no-P tiles. Hence D=4k+8 and D'=2k+8, verifying (3) symbolically. No finite
optimization is required for this all-k existence proof.

There is also an explicit all-k filling attaining the minimum physical
payment D=2k in (3). This strengthens the construction independently of any
strip optimizer. In raw coordinates put r=4k+4 and a=4k-4, the innermost
source's left arm column. Add selected vertices

    (r+1,4i-2), (r+1,8k+7-4i),          1<=i<k,
    {r,r+1} x {a+3,a+5,a+7,a+9,a+11}.

The first two groups put one isolated lower selected vertex in each of the
2k-2 no-P gap tiles between successive source tips. Such a vertex has
distance two from either neighboring axial support and no occupied vertex
immediately above it, so it has no occupied neighbor. All these vertices
are four columns apart on either side. The last group consists of five
vertical selected pairs inside the width-14 innermost mouth. They are
separated by blank columns; the preceding row has source supports only
outside those columns. Thus every vertex has exactly its partner as
occupied neighbor. The gap additions stay at least four columns from these
pairs. All original supports and freezing waves persist.

The 2k-2 gap tiles each have deficit one, and the six innermost no-P tiles
have total deficit two. These are all no-P tiles of the union. Therefore

    D=(2k-2)+2=2k,       D'=0,
    |T|=4k^2+16k+8,      |T|+|M|=10k^2+31k+8.

Hence the coalesced-strip lower bound D>=2B is sharp for every number of
nested sources, even though summing their original mouths would reuse
donors. The full rectangle need not be extremal. This later explicit sharp
filling was not included in the initial independent review input.

In this filling the i-th original mouth has actual no-P deficit 2(k-i):
it contains 2(k-i-1) gap tiles of deficit one and the innermost deficit two.
Summing those overlapping claims would give k(k+1), whereas the union has
only 2k. The repeated amount is k(k-1), unbounded and quadratic. For three
sources the naive payment is twelve and the true payment six. The merged
ledger counts six exactly and pays the three whole source charges once.

## 7. Interleaved mouths need not be nested

There is also an explicit family with k arbitrarily interleaved mouths.
Start with the positive width-22, depth-3 source in translated coordinates:
chamber rows 2,3, tip row 10, arm columns 3,24. For i=0,...,k-1 translate
its columns by 14i. For odd i additionally reflect rows by row -> 21-row;
for even i keep the rows. Leave every other site blank and use a rectangle
with 22 rows and 14k+16 columns.

All mouths occupy row pair 10,11. Each contains ten physical tile columns,
and successive mouth intervals advance by seven tiles. They overlap in
three tiles and neither contains the other. Sources of the same direction
are 28 columns apart, leaving six columns between their chambers and arms.
Opposite directions have chamber bands 2,3 and 18,19, and their arms end
in rows 10 and 11 respectively. All distinct tip columns are at least seven
apart. These separations exclude every new selected adjacency and every
cross-component endpoint edge, so the prescribed supports, matching and
freezing all persist. Foreign source endpoints in a mouth are only the
parallel source tips in row 10 or 11, exactly the allowed contact type.

The merged union has C=1 and 7k+3 tiles. Exactly 2k-2 contain saturated
internal source tips; its other 5k+5 tiles are empty in this baseline.
Therefore D=10k+10 and D'=8k+10, agreeing with D=2k+D'. The full counts
are |T|=18k and |M|=29k. The theorem gives objective<=mn/2-k. This
all-k family proves that the enlarged class requires neither disjointness
nor nesting of mouth intervals. Its construction proof is separate from
the nested-family version supplied in the first independent review input.

## 8. Verification

Run from the repository root:

    python3 develop/check_coalesced_mouths.py --output output/coalesced-mouth-controls.json

The controls check complete source ownership and freezing, saturated tips,
coalesced unions without added cells or overlaps, physical/shifted type
counts, exact source/comb conservation, the full original ledger and the
repeated payment that a naive sum over original mouths would count twice.
They include nested and interleaved sources, all six complete-comb contact
types in both support phases, two nested clusters joined by complete combs,
mixed horizontal/vertical clusters and tile-preserving symmetries.
All 271 configurations and 32 symmetry images pass, including explicit
nested families through k=40. Strip optimization is a finite verification
aid. The arbitrary-k existence
proofs above use only explicit source placements and selected-vertex formulas;
in particular the sharp nested family does not call the strip optimizer.

Independent review task c71b6706-97f9-45b8-b411-15d7c10a137b completed
ACCEPT at 10:39:40 UTC, observed gpt_6/pro. Its exact response and independent
assessment are archived. It covers the main coalescing theorem and the
unaugmented nested construction. The later explicit sharp filling and
interleaved construction have separate written/finite validation and were
not included in that review input. Subsequent contact extensions do not
inherit this verdict.

## 9. Remaining scope

This is a source-level extension to overlapping mouths, not a solution for
all unmatched comb ends. The all-radius obstacle still has B=1,O=2,J=0 and
lies beyond the sufficient criterion. A mouth crossed by a source chamber,
a nonterminal arm, a perpendicular source tip, a bent contact or an
unprescribed component is outside the hypotheses. General grid and triple
equality remain open. No new Lean claim is made for this full geometric
extension; written proofs and finite controls have separate scopes.
