# A unique-matching barrier, an exact free-selection frontier, and hole compensation

Rematching alone cannot make the previous endpoint ownership criterion universal.
For every even width w>=6 we construct a feasible 4-by-w board with a UNIQUE
actual perfect matching on P and J=area/2-1, yet no rematching on P admits the
required ownership. More strongly, no endpoint-only charge certificate with
the unchanged tile inequalities can work, even with arbitrary groups of old
edges. Four signed units of negative tile budget lie outside the endpoint support;
two remain as numerical margin after payment.

There is nevertheless a complete compensation proof. Two forced holes and w
pairwise disjoint guarded pairs give an adjacent-hole injection for EVERY
feasible selected set on this fixed endpoint footprint. They prove the exact
free-selection maximum J=2w-1. One adjacent relocation of a selected vertex
also repairs the ownership criterion at the same J, keeping P and M fixed.
This separates rematching from relocation of T and direct use of hole credit.

Subsequent research [excludes universal adjacent-hole payment and the proposed
purely local mixed cover](ISOLATED_HOLE_OBSTRUCTION_AND_MATCHING_DETOURS.md):
an interior all-q footprint has exact adjacent deficiency q, while distinct
actual-edge length-three detours provide the missing payments. The guarded
cover proved for P_w below remains valid; it was never a universal cover claim.

## 1. Setup and the fixed endpoint footprint

Use grid coordinates (r,c), 0<=r<4, 0<=c<w, with ordinary grid adjacency and
aligned disjoint 2-by-2 tiles. P is the endpoint set of an actual matching M;
T is disjoint from P, O=P union T, and H is the complement of O. Assume every
selected vertex has at most one occupied neighbour. No freezing is assumed.

For every even w>=6 set

    P_w = {(r,c): r in {0,1}, 1<=c<=w-2}
            union {(2,1),(2,w-2)}.                          (1)

A matching of exactly P_w is

    (1,1)--(2,1), (1,w-2)--(2,w-2),
    (0,c)--(0,c+1) for odd c=1,3,...,w-3,
    (1,c)--(1,c+1) for even c=2,4,...,w-4.                 (2)

These edges partition P_w, so |P_w|=2w-2 and |M_w|=w-1.

**Uniqueness lemma.** M_w is the only perfect matching of the induced grid on
P_w. The two row-two vertices are leaves and force the first two edges in (2).
Remove their four endpoints. Starting at c=1, the remaining top vertex (0,c),
for each successive odd c, has only (0,c+1) left: its left neighbour has
already been removed, and its lower neighbour was removed either by the left
leaf edge (c=1) or by the preceding bottom horizontal edge. Thus the displayed
top edge is forced. If c+1<=w-4, vertex (1,c+1) then has only (1,c+2) left,
forcing the next bottom edge. Continue until the last top edge. Every remaining
endpoint is removed by these forced steps. This is an all-width induction,
not a bounded enumeration of matchings. In particular there is no alternating
cycle on P_w with respect to M_w.

## 2. General guarded-pair and forced-hole facts

If a vertex has two distinct neighbours in P, it cannot be selected: otherwise
it already has two occupied neighbours.

If adjacent sites a,b lie outside P and a has a neighbour in P, they cannot
both be selected. Selecting both would give a its P neighbour and b as two
distinct occupied neighbours. Such a pair is called guarded here; the guard
is an actual occupied endpoint, independent of its matching partner.

**Guarded cover lemma.** Suppose Q=V minus P is partitioned into f forced-hole
sites and m disjoint guarded adjacent pairs. Then every feasible T admits an
injection into adjacent H: send a selected endpoint of a pair to its other
endpoint. No pair has two selections, and its other endpoint is neither P nor
T, hence is a hole. Different pairs give different image holes. In particular,

    |T|<=m,  |H|-|T| = f+2a,                             (3)

where a is the number of pairs with no selection. Every hole is counted once:
one image hole per selected pair, two unspent holes per empty pair, and the
f forced holes. If P has an actual perfect matching, this gives

    J=area/2-f/2-a.                                      (4)

An occupied P guard may justify more than one local exclusion: it is a
logical witness, not a unit of payment. The counted payment resources are the
distinct non-P pair endpoints and actual image holes, which are disjoint.

The statement only uses this explicit disjoint cover. It does not assert that
arbitrary grid footprints admit such a cover.

## 3. Exact maximum with ALL selections free

For P_w the two sites

    F_w={(2,2),(2,w-3)}                                  (5)

are forced holes. Each has its neighbour in row one and its adjacent row-two
leaf in P_w. They are distinct for w>=6.

The rest of Q is partitioned into exactly w adjacent pairs:

* the two vertical pairs `(0,0)--(1,0)` and `(2,0)--(3,0)`;
* their right-edge reflections;
* `(3,1)--(3,2)` and `(3,w-2)--(3,w-3)`;
* `(2,c)--(3,c)` for every c=3,...,w-4.

The first endpoint in each displayed pair has a P_w neighbour. The pairs have
disjoint endpoints and cover Q minus F_w: the four boundary-column pairs
cover those eight sites; the two bottom end pairs cover columns 1,2,w-3,w-2
in row three; the remaining vertical pairs cover both lower rows between.
Their number is 4+2+(w-6)=w. The guarded cover lemma therefore proves, for
ARBITRARY feasible T disjoint from the fixed P_w and any actual matching on P_w,

    |T|<=w,  J=|T|+(w-1)<=2w-1=area/2-1.                 (6)

There is no retained-T or colour restriction. In fact each such configuration
has the exact ledger J=2w-1-a with one physically identified unit for every
empty guarded pair, plus the two forced holes. The T-to-H injection never
uses a hole or pair twice.

## 4. A sharp family that NO endpoint-only scheme can certify

Equality in (6) is attained by

    T_w={(0,0),(0,w-1),(2,0),(2,w-1),(3,1),(3,w-2)}
          union {(2,c): odd c=3,5,...,w-5}
          union {(3,c): even c=4,6,...,w-4}.              (7)

Empty ranges contribute no sites. For w=6 the board is

    T P P P P T
    H P P P P H
    T P H H P T
    H T H H T H

The four boundary selections in rows zero/two have their unique occupied
neighbour immediately inside their row. The two lower end selections have
the row-two P directly above as their unique occupied neighbour. An additional
row-two odd selection has only its row-one P above occupied: all other adjacent
sites are holes. Additional row-three even selections have no occupied
neighbour. Thus (7) is feasible at every width. It has one selection in every
guarded pair, so

    |T_w|=w, |H_w|=w+2, |M_w|=w-1, J=2w-1.              (8)

Let n=w/2 and let U consist of all top tile-row tiles together with the two
bottom end tiles:

    U={(0,j):0<=j<n} union {(1,0),(1,n-1)}.               (9)

This set contains ALL of P_w. Its two lower end tiles are positive 2T/1P/1H,
its two top end tiles are neutral 1T/2P/1H, and its n-2 other top tiles are all-P.
For the old ownership demand d_B=max(0,|O intersect B|-2),

    sum_U d_B=2+2+2(n-2)=w,
    #distinct actual edges incident to U = |M_w|=w-1.     (10)

Thus Hall fails by one physical edge. This holds for every matching on P_w,
even without uniqueness, because all P lies in U and the incident resource
count is fixed by |P|/2. The uniqueness lemma gives the additional obstruction
that no alternating rematching or sequence of square flips is available.

The failure is broader than any chosen pairing of actual edges. Write
q_B=|T intersect B|-|H intersect B| as in the preceding notes. In U,

    sum_U q_B=2.                                        (11)

Every endpoint belongs to U. Consequently ANY endpoint charges satisfying
`q_B<=sum_{p in P intersect B}sigma(p)` in every tile must satisfy
`sum_P sigma>=2`. No partition of the matching edges into nonpositive single
edges, square pairs, alternating cycles, or arbitrary nonpositive groups can
then exist: each such partition would instead imply `sum_P sigma<=0`.
This argument permits arbitrary real charges; restricting them to [-1,1]
does not help. The refuted class keeps the SAME per-tile inequalities and
uses endpoint charges alone. It does not exclude schemes that transfer a
hole budget across tiles or change T while preserving its size.

For w=6 the one omitted bottom tile is empty, with q=-4 and sparse slack r=2.
For w>=8 the first and last omitted bottom tiles have one T and three H each,
with q=-2 and r=1 each; other omitted tiles have two T, two H and q=r=0.
Thus in every case

    sum_outside_U q_B=-4, sum_B r_B=2,
    total d=w>|M|=w-1, J=area/2-1.                     (12)

The global necessary ownership bound J<=area/2-sum r would give the false
upper bound area/2-2 on this feasible family. The prior conditional identity
is valid; the attempted universal existence of its certificate is false.

## 5. What pays the deficit: actual holes, not rematched endpoint credit

The guarded cover is already a full compensation certificate for the ORIGINAL
T_w,P_w,M_w. Its image contains every hole except the two sites in F_w. For
example `(3,1)` is paired with the adjacent hole `(3,2)`, and `(3,w-2)` with
`(3,w-3)`. These are actual payments from the omitted tile row to the two
positive endpoint tiles. Interior selections are paired vertically with holes;
boundary-column selections use their own boundary-column pairs.

There is no negative endpoint resource in those omitted tiles because they
contain no P. Their negative q budget cannot be transported by rematching
P. In the cover it is spent directly on distinct selected-to-hole pairs.
The two forced holes remain unused, proving the exact one-unit margin.
This is a positive all-width compensation proof as well as a barrier to the
endpoint-only route; it does not refute the numerical half-area target.

## 6. One selection relocation repairs ownership, without rematching

For the sharp family (7), replace just

    (3,w-2) in T by (3,w-3),                            (13)

keeping every other selection and the entire actual M_w and P_w. The new site
was a hole. At w=6 it has no occupied neighbour; at w>=8 it has just the
selection `(3,w-4)` beside it, and that selection gains only this neighbour.
The old site becomes a hole; all other selected degrees stay admissible.
So this is feasible and preserves |T| and J.

The last bottom tile loses one selection and its demand falls from one to
zero. The receiving bottom tile still has no P and at most two selections,
so its demand stays zero. All other demands are unchanged. The actual tile
resource graph is the simple path

    (1,0),(0,0),(0,1),...,(0,n-1),(1,n-1),              (14)

with one internal edge at every intermediate all-P top tile and none at its
end tiles. Own every internal edge locally, and every path edge by its earlier
tile in (14). The first bottom tile and every top tile are paid exactly; the
last bottom tile now needs zero. This uses every actual M_w edge once and
pays all demands. Total sparse slack falls from two to one, unused resources
are zero, and the conditional exact margin becomes J=area/2-1 as required.

This is a certificate for the relocated T, not an endpoint certificate for
the original T. It supports a numerical comparison because |T|, P and M are
unchanged in size and feasibility, not because the original tile inequalities
became feasible. Universal cardinality-preserving relocation on arbitrary
footprints is not proved here.

## 7. Verification, formal scope and provenance

`python3 develop/check_unique_matching_hole_barrier.py` checks every even width
6 through 104: actual match coverage and selected degrees; unique-matching
leaf elimination; disjoint guarded cover and its actual guards; sharp counts;
the all-P cut; exact adjacent-hole injection; and the one-relocation complete
ownership certificate. At widths 6 and 8 it also checks every three-state
selector profile of the guarded pairs (7,290 profiles, 3,697 feasible selector
sets, including 16 and 33 maximizers respectively) and independently enumerates
the P perfect matchings (one at each width). These are controls for the written universal-width proofs.

Local Lean records the abstract occupied-neighbour exclusions, guarded-pair
injection and unrestricted slot arithmetic. The coordinate cover, uniqueness
peeling, full geometric adapters and all-width assembly remain written.
Seven declarations compile locally with individual axiom audits; see
[formal scope and output](../output/guarded-hole-cover-formal.json). The abstract
partner involution can be extended by the identity outside the covered pairs;
no selection lies at those uncovered P/forced-hole sites.

A finite Z3 unique-matching/cut search found the width-six seed. Its rank
constraints and SAT model are discovery evidence, not the general proof.
The wider sharp family, guarded cover, no-endpoint-certificate argument and
selection-relocation proof above are separate deductions. A sparse-ledger
search timed out UNKNOWN; it is not evidence of nonexistence.

The previous [component-cut and square-exchange note](ACTUAL_MATCHING_COMPONENT_CUT_AND_SQUARE_EXCHANGE.md)
proved only a conditional rematching/cycle route. This note supplies a precise
all-rematching obstruction and a different hole/selection repair. Submitted
manuscripts, Mail, public main/PR #3, star-forming/C4 and shared CI are outside
this research branch.

Independent review d682d0ba returned ACCEPT for the complete written note.
The reviewer reports rerunning the supplied Python verifier and matching its
output JSON exactly; no Lean or Z3 execution was performed by the reviewer.
The [review receipt](../output/unique-matching-hole-barrier-review.json) records
the exact scope and original response; stream and terminal reply agree.
