# Sharp global completion and distinct physical reserves for negative frozen strips

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [degree-four sharp family](OCCUPIED_STRIP_DEGREE_FOUR_BUDGET.md) has
regional surplus (1-k)/2, arbitrarily negative although all endpoints are
frozen and the actual matching is unique. Here we prove a positive and sharp
compensation theorem for that SAME endpoint footprint. It permits arbitrary
reselection of T for the upper bound, and every retained-T completion for the
physical no-reuse allocation. Finite optimization discovers the attaining
pattern; the upper bound is proved by an explicit disjoint geometric cover.

## 1. Exact statement and scope

Fix k>=0. The board is 6-by-(6k+4). The actual matching and original selections
(T0,M) are the one-corner b=1 family in the cited note. Explicitly the left
pair is (1,1)--(2,1). For each i=0,...,k-1 set s=3+6i and place

    (1,s+2)--(1,s+3), (1,s+4)--(2,s+4),
    (2,s+3)--(3,s+3), (3,s+4)--(3,s+5).

These give P=V(M), |P|=8k+2 and |M|=4k+1. The original T0 is the union of

    (0,1),(1,2),(2,0),(3,1);
    (0,3+6i),                         i=0,...,k;
    (0,s+2),(0,s+4),(1,s+1),(1,s+5),
    (4,s+3),(4,s+5),(3,s+6),          s=3+6i, i=0,...,k-1.

All unlisted sites are blank. Every original endpoint has the strict freezing
certificate in the cited note; the matching is forced by leaf elimination.
Let I be the top two rows, through the whole width.

**Sharp global completion theorem.** For EVERY feasible selected set T with
this fixed P (disjoint from P, selected occupied degree at most one),

    |T| <= 13k+11,
    |T|+|M| <= area/2-k.

This upper bound requires neither T0 subset T nor complete freezing.
There is an explicit feasible T* containing T0 with |T*|=13k+11. Hence it
is a TRUE maximum over all feasible reselections for the fixed P, not only
an inclusion-wise maximal extension. Its original M is still unique and
all endpoints still freeze. The occupied strip has exactly its original
surplus (1-k)/2 even at this true maximum.

**Physical compensation lemma.** For EVERY feasible retained extension
T0 subset T with the SAME P and M:

* Nothing is added inside I; its exact budget remains C=1, D4=k,
  2S_I=1-k. All old endpoint-receiver tile inventories are unchanged.
* The boundary exterior tile Q_(1,0) has half-unit surplus c=-1. The
  internal half-unit C=1 pays this demand once.
* For every i, the distinct exterior tile Q_(1,4+3i) has c=+1 and pays
  the actual D4 at (1,7+6i), one half unit, once.
* The different endpoint-free tiles Q_(1,2+3i) each have at least one
  FULL unit of deficit. None was used above. Thus k full units remain.

Here Q_(a,b) is the ORIGINAL tile {2a,2a+1} x {2b,2b+1}, and
c(Q)=4-2|T intersect Q|-|P intersect Q| is surplus in half units. All other
outside endpoint tiles have c=0, and all endpoint-free tiles have c>=0.
There is no omitted outside positive-charge demand. The donor families and
boundary tile are disjoint in physical tile identities, and each D4 uses
one different tile. For k>=2 the regional deficit is genuine, and this
allocation pays it without reusing either half units or interval credits.

The theorem is a coefficient-one bound, with an additional sharp k-unit
margin, on this specified class. It does not assert general compensation
for arbitrary endpoint footprints, new matching endpoints, arbitrary mixed
directions, or a universal improvement of 5/6.

## 2. Two elementary local facts

A unit square has at most two selected corners: any three contain one
vertex adjacent to the other two, violating selected occupied degree <=1.
This holds whether other occupied vertices lie outside the square or not.

If adjacent sites a,b include a site a with a DIFFERENT neighbor p in P,
then at most one of a,b is selected. Selecting both would give a the occupied
neighbors b,p. If a site has two distinct neighbors in P, it is never selected.
These statements use actual fixed endpoints; the matching inside P is irrelevant.
The endpoint p can justify several inequalities, but is never counted as a
reserve. The counted selected sites in the cover below are disjoint.

## 3. A disjoint 13-selection cover of each six-column module

Partition the board into the first four columns and k consecutive six-column
blocks beginning at 4+6i. Each block has the same endpoint footprint, in local
coordinates:

    P_mod={(1,1),(1,2),(1,3),(2,2),(2,3),(3,2),(3,3),(3,4)}.

The sites (2,1),(2,4) each have two P neighbors and cannot be selected.
The following diagram partitions every other non-P site. Identical letters
in A,...,G form an adjacent two-site block with an anchored P neighbor;
H,I,J are disjoint unit squares. P marks fixed endpoints and X forbidden sites.

```text
DDCCHH
EPPPHH
EXPPXF
AAPPPF
IIGBJJ
IIGBJJ
```

For clarity, the exact blocks, with no diagram convention needed, are

    unit faces: top-left (0,4), (4,0), (4,4);
    pairs:
      (3,1)--(3,0),  anchored at (3,1) by P(3,2);
      (4,3)--(5,3),  anchored at (4,3) by P(3,3);
      (0,3)--(0,2),  anchored at (0,3) by P(1,3);
      (0,1)--(0,0),  anchored at (0,1) by P(1,1);
      (1,0)--(2,0),  anchored at (1,0) by P(1,1);
      (3,5)--(2,5),  anchored at (3,5) by P(3,4);
      (4,2)--(5,2),  anchored at (4,2) by P(3,2).

The three faces, seven pairs, eight P and two X account for all 36 sites
exactly once. Section 2 gives at most 3*2+7=13 selections in the block.
External neighbors can only add restrictions, so the same bound holds when
these blocks are placed next to one another in the full board.

The initial six-by-four block has P={(1,1),(2,1)}. Its disjoint cover is

    unit faces: top-left (0,2), (2,2), (4,0), (4,2);
    pairs: (0,1)--(0,0), (3,1)--(3,0), (1,0)--(2,0).

The pairs are anchored by (1,1),(2,1),(1,1), respectively. Together with
the two P sites these cover all 24 sites, giving at most 4*2+3=11 selections.
Summing the disjoint column blocks proves |T|<=13k+11 for arbitrary T.
Since area/2=18k+12 and |M|=4k+1, the global surplus is at least k.
No candidate selections have been enumerated in this argument.

## 4. A periodic fully frozen attaining completion

Let w=6k+4. Define T* row by row:

| Row | Selected columns |
| --- | --- |
| 0 | every odd column 1,...,w-1 |
| 1 | 2, and 4+6i,8+6i for i=0,...,k-1 |
| 2 | 0,3 |
| 3 | 1,3, and 5+6i,9+6i for i=0,...,k-1 |
| 4 | every even column 0,...,w-2 |
| 5 | 0, and every odd column 3,...,w-1 |

Their row counts are 3k+2,2k+1,2,2k+2,3k+2,3k+2, summing to 13k+11.
The original T0 is contained in this list, by substitution in Section 1.
The two selected-selected pairs are (2,3)--(3,3) and (4,0)--(5,0).
Each has no other occupied neighbor. All other row-0, row-1 and core-adjacent
row-3/row-4 selections either see their single prescribed P or are isolated;
row-5 odd selections are isolated. Consecutive core patterns differ by six
columns, so the nearest selections in the same row are still separated by
one blank, except the two displayed vertical pairs. The formulas also
cover k=0. Checking these fixed row patterns proves feasibility for all k.

Because T0 is retained, every original two-witness strict freezing certificate
remains valid for the same M. Feasibility has just been checked anew; freezing
is not inferred from an unverified addition. P has not changed, so the old
leaf-forced uniqueness proof is unchanged. This gives an attaining completely
frozen maximum, with no tradeoff between true maximality and freezing here.

## 5. Forced original physical reserves in every retained completion

First examine Q_i=Q_(1,2+3i), with columns 4+6i,5+6i and rows 2,3.
Its upper-left site lies directly below T0(1,4+6i), which already sees
P(1,5+6i); hence it is blank. Its upper-right site sees the TWO fixed
endpoints (1,5+6i),(2,6+6i), so cannot be selected and, since P is fixed,
is blank. The lower-right site (3,5+6i) sees P(3,6+6i). Therefore both lower
sites cannot be selected simultaneously. Q_i has no endpoints and at most
one selection, so its actual deficit 2-|T intersect Q_i| is at least one.
Different i give different original tiles, not overlapping auxiliary squares.

Next the rebate Q'_i=Q_(1,4+3i) has the fixed endpoint (3,8+6i), the retained
selection (3,9+6i), and two forced blanks above. The blank at (2,8+6i) is
forced by T0(1,8+6i), already seeing P(1,7+6i); the other is forced by
T0(3,9+6i), already seeing its P neighbor. Thus c(Q'_i)=1 in every retained
completion. This tile is different from Q_i and from every other core tile.

The only other exterior endpoint tiles are the all-P tiles Q_(1,3+3i),
with c=0, and the boundary tile Q_(1,0). The latter has P(2,1), retained
T0(2,0),T0(3,1), and a forced blank at (3,0), giving c=-1.
Within I every odd site in row 0 is already selected. Any even row-0 site
other than column 0 sees two such selections; column 0 is forbidden because
its selected neighbor (0,1) already sees P(1,1). The remaining row-1 blanks
are column 0 and columns 3+6i for i=0,...,k. Column 0 sees P(1,1) and the
retained T0(2,0). Every blank 3+6i is adjacent to the retained selection at
2+6i, which already sees a fixed endpoint. Thus none can be added. All
original band labels are preserved, and its exact C=1,D4=k budget remains.
The endpoint tile inventories outside I were exhausted above, so the original
full endpoint receivers remain neutral as well.

Assign the internal half unit C to the boundary's one half-unit demand.
For each i assign the DISTINCT physical half unit c(Q'_i)=1 to D4_i.
These exhaust all demands D4 plus outside positive charge. The endpoint-free
Q_i reserves are unspent, each supplies at least one full unit, and every
other endpoint-free tile has nonnegative deficit. The exact whole ledger is

    2S_whole=(1-k)+(k-1)+2D_out=2D_out,
    D_out >= k.

At T*, each Q_i has exactly one selection and all other exterior endpoint-free
tiles have two; hence D_out=k and the margin is sharp. This identifies the
unused physical surplus after payment, rather than counting the same surplus
once as a receiver credit and again as a donor.

## 6. Verification and Lean scope

The standard-library validator checks the disjoint covers, constructs the
all-k attaining pattern, replays the original strict ranks and unique-matching
leaf order, reconstructs actual strip budgets and every exterior endpoint-tile
charge, and identifies the two disjoint physical resource families. Independent
column dynamic programming optimizes both arbitrary reselections and retained
extensions for k=0,...,5, corroborating the general cover bound. Random partial
and greedy maximal retained completions also check the unchanged band, actual
raw ledger and k distinct unused full-unit reserves.

Lean verifies the universal local implications directly from selected occupied
degree<=1: a face contributes at most two, an anchored pair at most one, and a
two-P-neighbor site zero. It checks the exact module/cap partitions and proves
T<=13 and T<=11 for ANY predicate T satisfying local feasibility, then the
arbitrary-list aggregation. These are universal local proofs, not enumeration
of all selected subsets. It also checks the concrete k=2 6-by-16 attaining
board, 37T/9M/18P, feasibility, all 18 endpoints inductively frozen, its negative
regional surplus -1/2, and the distinct physical full-unit and half-unit tiles.

The all-k translation of covers into the global board, the row-pattern attaining
adapter, retained-completion label invariance and full all-k physical allocation
remain written proofs with executable checks. No end-to-end formalization of
the entire parameterized grid theorem is claimed.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_strip_completion_reserves.py --output output/frozen-strip-completion-reserves-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_strip_completion_reserves_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/frozen-strip-completion-reserves-formal-validation.json

The search for a universal residual-capacity cut remains open. This theorem
settles the previously negative-strip sharp family even at its true fixed-P
maximum; it does not replace the general geometric covering problem. The
submitted 11 October manuscript and correspondence are unchanged.
