# All-alignment one-square receivers and a larger coefficient-one class

19 October 2026. This builds on the whole-component receiver theorem and
the earlier complete single-square structure theorem. The submitted manuscript
is unchanged. The argument uses explicit finite base shapes and an arbitrary
two-step arm-extension identity, not an enumerated length cutoff.

## 1. Complete shape and original regional accounting

Let (T,M) be feasible on an even-by-even rectangular grid, with P=V(M),
A=T union P and every T having at most one neighbor in A. Assume single
terminality, so every endpoint has occupied degree at least three.
Suppose one complete endpoint component H contains exactly one all-P unit
square Q, without an alignment assumption. By the single-square parity
theorem in SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md, H has four straight outward
arms in one of two pinwheel orientations. Arm lengths are

    l_i=2a_i+epsilon_i,  a_i>=0,  epsilon_i in {0,1}.

Zero length is permitted. The central corner incident to arm i is matched
outward precisely when epsilon_i=1. If k edges are matched inside Q, then

    o=sum epsilon_i=4-2k in {0,2,4}.

For o=2 the two odd corners are adjacent. The matching and alternating
selected supports on every arm are forced by this parity pattern. Every
endpoint has occupied degree exactly three.

Let R_H be exactly the tiles containing endpoints of H. By the terminal
tile-ownership and closed-receiver lemmas of
COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md, these receiver tiles have no
endpoints from other components, their matching never leaves R_H, and

    rho(R_H)=T_R+P_R/2-2|R_H|.                              (1)

This is the original saturated-transfer ledger summed on the complete
receiver, not an omission of its saturated tiles.

All selected vertices in a terminal endpoint tile are adjacent to some P
in that tile. Indeed, for at least two P the connected P subset of the
four-cycle makes every remaining corner adjacent to P. With just one P,
terminality forces an occupied in-tile neighbor. It is T. A second T at
the diagonal corner would neighbor that T, which already has its P neighbor,
and so is impossible. Thus no additional, unrelated selected vertex can
enter R_H. All its T are the prescribed selected supports of H. Their
positions, and hence (1), are fixed in arbitrary feasible exteriors.

## 2. Extending an arm by two preserves receiver charge

Use normalized Q corners (0,0),(0,1),(1,1),(1,0) and a pinwheel pointing
north, east, south, west respectively. On the north arm, p_j=(-j,0).
For j>=1 its selected perpendicular support is (-j,-1) when j is odd,
and (-j,1) when j is even. Its axial selected support is p_(l+1).
The other arms are rotations of this pattern.

**Two-step counting lemma.** Replace length l by l+2 in this prescribed
pattern, retaining its parity and the other arm lengths. For every alignment,

    Delta P_R=2,   Delta |R_H|=1,   Delta T_R=1.             (2)

This compares counts of two prescribed geometric patterns; it does not
assert a feasible move in a fixed arbitrary exterior.

Proof. The two new path positions occupy exactly one new tile along the
ray, possibly with the first new position in the previous terminal tile.
Each arm's tiles form a straight one-tile-wide ray. A newly reached tile
beyond its tip is outside the central square's tile rows or columns and
cannot meet any of the other three perpendicular arms. Thus exactly one
new tile is added, also when the previous arm length is zero.

There are two end alignments. If p_(l+1) is outside the old receiver, the
two new endpoints lie together in the new tile. Their perpendicular supports
are on opposite sides, exactly one in the tile. The new axial support is
outside the new receiver. Thus the receiver gains one T.

If p_(l+1) is in the old terminal tile, its former axial T is replaced by
P, reducing old receiver T by one. The second new endpoint and the new
axial support lie in the newly added tile. Of the two new perpendicular
supports exactly one lies in the receiver's paired column, either in the
old terminal tile or in the new tile. The new axial support adds one T
and these perpendicular supports add one T, for net change -1+1+1=1.
This argument applies also at l=0: its old axial T is the central corner's
unique external occupied neighbor, and the two new perpendicular supports
follow the same first-odd/second-even pattern. Rotation gives all arms.
QED.

Substitution in (1) gives Delta rho=1+2/2-2=0. Therefore, writing
N=sum a_i, every receiver has

    |R_H|=R_0+N,   T_R=T_0+N,   P_R=4+o+2N,               (3)

where R_0,T_0 are determined by the parity-only base shape a_i=0.

## 3. The explicit parity-only base shapes

Let (u,v) be the two coordinate parities of Q's upper-left corner in the
fixed tiling. Each table entry is (R_0,T_0); P_0=4+o throughout.

| Odd arms o | (u,v)=(0,0) | (0,1) | (1,0) | (1,1) |
| --- | --- | --- | --- | --- |
| 0 | (1,0) | (2,2) | (2,2) | (4,4) |
| 2 | (3,2) | (3,3) | (3,3) | (4,4) |
| 4 | (5,4) | (4,4) | (4,4) | (4,4) |

Here is a direct coordinate specification allowing every entry to be counted
without a search or a matching oracle. Start with the four Q corners. For
o=0 there are no other P and the selected supports are

    (-1,0), (0,2), (2,1), (1,-1).

For o=4 add P at (-1,0),(0,2),(2,1),(1,-1). Their selected supports are

    (-1,-1),(-2,0), (-1,2),(0,3),
    (2,2),(3,1), (2,-1),(1,-2).

For o=2 choose the top internal matching edge. Add P at (2,1),(1,-1),
and take selected supports

    (-1,0),(0,2), (2,2),(3,1), (2,-1),(1,-2).

For each specified alignment the tiles containing these P give the displayed
R_0; counting the listed T inside them gives T_0. Other choices of the one
internal edge are rotations. Rotation exchanges the mixed phases (0,1),
(1,0), whose entries agree, and preserves the equal-phase cases. Reversing
the pinwheel reflects this coordinate pattern and again exchanges the mixed
phases while preserving the equal-phase cases. The two internal perfect
matchings for o=0 have the same endpoint and support sets. These observations
cover all seven matching patterns and both pinwheels.

Using (1) and (3) now gives the all-length original charge table:

| Odd arms o | (0,0) | (0,1) | (1,0) | (1,1) |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | -2 |
| 2 | -1 | 0 | 0 | -1 |
| 4 | -2 | 0 | 0 | 0 |

**All-alignment one-square theorem.** Every complete single-terminal endpoint
component containing exactly one P-square has rho(R_H)<=0. Its charge is
independent of all four a_i and is exactly the table above. Strict negative
budgets depend on alignment; there is no positive payment per odd arm without
that alignment condition. Neutral misaligned frozen crosses agree with the
earlier obstacle. The two-step identity is an arbitrary-length proof.

## 4. A coefficient-one theorem allowing branched components

**At-most-one-square component theorem.** If every initial endpoint component
contains at most one all-P unit square, aligned or not, then

    |T|+|M|<=mn/2.                                         (4)

No initial terminality, matching-direction or collar-disjointness hypothesis
is imposed. In particular, components can contain the four-arm branches
classified above; they need not fit inside two rows or columns.

Proof. Perform feasible singles until single-terminal. The objective is
preserved and endpoints are only deleted. Each resulting component is a
subset of one original component and contains at most one P-square. A
square-free final component is a straight comb with receiver charge zero.
A one-square final component has nonpositive receiver charge by the theorem
above. Terminal tile ownership makes all receivers disjoint. All remaining
tiles have no P and charge t-2<=0. Sum original charges and use the exact
global objective identity. QED.

More precisely, for each final one-square component let b_H be the negative
of its charge in the table. With Z the no-P tiles of that terminal pair,

    mn/2-|T|-|M| = sum_H b_H + sum_(Q in Z)(2-t_Q).          (5)

All terms are nonnegative. Equality requires all final one-square receivers
to have a neutral phase/type in the table and every no-P tile to be saturated.

The class can also include full two-row/two-column rectangles: first apply
their proved complete-component reduction, then the preceding argument.
It can additionally include L prescribed capped-ladder components in the
tile-preserving positions of FROZEN_TWO_ROW_CAPPED_LADDERS.md. Their matching
and supports survive every other reduction and single. Each contributes
one further unit to the right of (5), so the stated combined class satisfies
|T|+|M|<=mn/2-L. Each actual tile and saturated transfer is assigned to its
one whole endpoint receiver. No source-assignment hypothesis is needed on
this covered class. General components with several interacting P-squares
remain open; this is not the universal grid bound or triple equality.

## 5. Verification scope

The independent physical controls check 2,380 family cases: all seven central
matching patterns, all four alignments, 81 small arm-length parameter choices
and four longer unequal choices. They verify (3), original receiver charge,
forced receiver blanks and that every T in the receiver is an actual H support.
There are 448 symmetry images and 336 explicit two-step extension checks.
Complete small enumeration examines 24,296 feasible pairs, of which 22,217
satisfy the initial at-most-one-square-per-component hypothesis; single
normalization and the exact deficit are checked for all of those. The 3-by-4
source shape is padded by a blank fourth row for the even-rectangle ledger.

The earlier frozen 8-by-8 neutral one-square example attains |T|+|M|=32:
its one receiver has charge zero and every no-P tile is saturated. This
checks sharpness and the equality condition. A separate fixture combines
horizontal and vertical combs, a pure rectangle, a capped component and a
misaligned branched one-square component; their whole receivers contribute
exactly two units of strict deficit, plus the no-P tile deficit.

```sh
python3 develop/check_single_square_receivers.py --output output/single-square-receiver-controls.json
```

The 65-declaration local Lean audit includes the physical diagonal bridge
and conditional comb counts used by the preceding receiver note. The new
all-length arm-extension geometry, base counts and one-square global bound
here are written proofs, not new Lean claims. Independent review of this
extension is separate from the earlier square-free receiver submission.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
