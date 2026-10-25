# Pressured gaps in bent paths: sharp private reserves and exact beta repair

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [adjacent-band reserve theorem](ADJACENT_BAND_BOUNDARY_REPAIR.md) required
immediate BB exposure at aligned P columns. An occupied neighbour can block
that witness while forcing a larger reserve elsewhere in the same no-P gap.
We give general internal-gap bounds and an arbitrary-width frozen application
where the old immediate-exposure pair count is zero.

For every even w>=6, the existing occupied-adjacent-bands family has one bent
alpha. In EVERY feasible selection extension preserving its P,M,old T and
endpoint degree profile, that alpha supports at least

    g(w)=floor(w/3)+2

PRIVATE original intervals. This is the exact minimum over the entire extension
class, attained by an explicit extension. Separated copies have disjoint private
sets. Arbitrary withdrawals of r distinct intervals leave at most floor(r/g(w))
sources unpaid by the direct certificate. Moreover each alpha has its own actual
one-link beta cancellation: the FULL model always pays every alpha, at exact
minimum link cost equal to the direct deficit. Each whole beta is spent once.

The underlying frozen family and its numerical compensation are existing work
in [degree-three fusion, Section 9](DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md).
The new conclusions are the sharp reserve bound over all retaining extensions,
the direct/whole distinction under arbitrary withdrawals, and the general gap
adapters below. The universal 5/6 bound remains open.

## 1. Fixed physical model and unit identities

Use feasible T and actual matching M on an even rectangle. Uniform two-row bands
may be replaced by disjoint even-by-even regions with independent band directions,
as in the [restored matching-port ledger](CROSSING_MATCHING_PORT_LEDGER.md).
All actual M edges are retained before identifying GLOBAL open owners. N is
the perfect matching supplied by these bands.

A gap is a maximal consecutive run of columns containing no P in one local band.
It is internal if both ends face P columns inside that region. Its original
positive BB/TT forest components are the actual unit resources. Every TT column
has BB neighbours wherever the neighbouring column exists, by feasibility.
In an internal gap a TT cannot be an end column: it would see its selected
partner and at least one P in the adjacent column. Thus every BB/TT forest
in an internal gap starts and ends in BB and has imbalance one. Its unit count is

    L_gap = number(BB)-number(TT) = gap_length-|T in gap|.  (1)

If the gap has no units, it has no BB or TT and all columns are BT or TB. Adjacent
single-row selections may form horizontal pairs: a zero-unit word need NOT
alternate BT and TB. For example BT,TB,TB,BT is locally possible. Confusing
feasibility with independence would overestimate the pressured-row reserve.

A whole open owner supports every unit in an incident gap. Each gap has at most
two different boundary owners; if both boundaries belong to the same alpha, all
its units are private among all open owners. The two boundary incidences do NOT
create two copies of a unit. Different maximal gaps have disjoint unit sets.

## 2. General local bounds, including occupied adjacent bands

**Blank-row pressure.** Suppose an internal gap has n columns and one of its
physical rows is blank throughout. Then it has at least floor(n/3) units.
Indeed TT is absent, so each BB is a singleton unit. In the other row three
consecutive selections are forbidden: the middle one would have two selected
neighbours. Partition into disjoint triples and find a blank in each. Adjacent
selected pairs are allowed; a one-half density estimate is invalid.

**Anchored pressure.** In addition suppose n>=4, both end sites of the other
row are selected, and each already sees its exterior boundary P in that row.
The next site inward at each end must be blank. These are two different sites.
Among the n-4 remaining sites, every disjoint triple has a blank, giving

    L_gap >= 2+floor((n-4)/3)=floor((n+2)/3).             (2)

This does not require the whole gap to have immediately exposed BB next to P:
the end columns are BT. In applications the blank row can be forced by an
occupied adjacent P row together with preservation of endpoint degrees.

**Two BB ends.** An internal even-length gap with BB at both ends has at least
two DIFFERENT units. Each end BB lies in a positive forest. If these were the
same forest, it would span the whole gap, be an alternating BB,TT,...,BB word,
and have odd length. This contradicts even gap length. Odd length only guarantees
one unit; BB,TT,BB is a sharp local example. No freezing or endpoint-degree
hypothesis is needed for these local statements.

Several bounds for the SAME gap are combined by their maximum, not their sum.
For one alpha, bounds for different gaps can be added because their unit sets
are disjoint. Across alphas use the actual shared interval identities, whose
incidence with different open owners is at most two. Consequently if h_A units
are certified distinctly within each alpha, H=sum h_A satisfies H<=2L, the
coefficient-one criterion H+2beta>=2alpha-1 remains sufficient, and h_A>=2
for every alpha gives simultaneous zero-link allocation. If the chosen units
are private, H<=L. These statements use the original global ledger, including
restored interface owners and the actual matching seam debit.

## 3. Boundary exclusion without aligned columns

The preceding adjacent-band lemma also has an offset-free version. In two
consecutive parallel bands of the SAME region, let an owner support an exterior
no-P gap facing the same lateral boundary in each band. Suppose each gap contains
at least one BB, anywhere in the gap. Then at least one gap supplies a positive
unit. P-column coordinates and BB coordinates need not agree between bands;
intervening BT columns are allowed.

If a BB in such a gap does not lie in a positive forest, its balanced forest
must reach that lateral region boundary with a TT there. If BOTH gaps had no
unit, the two consecutive bands would have TT at the same boundary column,
violating selected degree at most one. Physical neighbours outside a region
cannot fix this contradiction. Rotation handles vertical bands. Combining
several pair witnesses still requires disjoint underlying gap/unit sets; one
must not add a pair credit to credits already drawn from the same gap.

A further individual certificate uses phase. In a left-balanced forest BB
columns have odd local column index, and in a right-balanced forest they have
even local index, because each regional band has even length. A BB of the
opposite parity is therefore positive. These are sufficient geometric tests,
not a claim that they detect every usable original interval.

## 4. An arbitrary-width frozen bent family with zero old pair count

Use occupied_bands(w), even w>=6, in degree_three_fusion.py. It is the union of
two existing two-leg modules under H(r,c)=(4-r,c-w), translated by (2,w), on an
8-by-(2w+2) board. Keep its actual matching. The existing uniform ordered
certificate occupied_band_certificate(w) freezes every endpoint. Its inventories:

    |P|=4w+12, |M|=2w+6, |T0|=14,
    alpha=1, beta=w-1, no mixed owners,
    S=6w-12.

Four endpoints have occupied degree four, at (3,w),(3,w+1),(5,w),(5,w+1);
all others have degree three. This application genuinely includes occupied
adjacent bands and degree-four points, rather than assuming them away.

The sole alpha's body is exactly

    {2,3} x {w+1,...,2w}
    union {4,5,6} x {w+1,2w},                            (3)

with TP tips (6,w+1),(6,2w). It has no immediate BB/P pair in two consecutive
bands of the kind previously counted: near the top the intermediate row is P;
in band rows4/5 both gap end columns are BT, blocking alignment with the lower
band. Thus its old adjacent-exposure witness count is zero. This observation
only concerns that sufficient witness rule, not absence of direct resources.
Initially the two internal gaps described below contain w-4 and w-2 units,
respectively. Every other incident gap is absent or a single BT column, with
zero capacity. Adding T at fixed P cannot increase any gap's unit count
length-|T in gap|, so such zero-capacity gaps remain zero in every extension.

Consider EVERY extension retaining P,M,T0, adding no P, and keeping the whole
endpoint occupied-degree profile unchanged. Equivalently, new T cannot touch P;
feasibility is also required. PP components, ordinary tip types and all open
owners are unchanged, and the old strict freezing witnesses replay. No claim
about arbitrary P additions, deletion of old T or degree-changing extensions
is included.

The two internal gaps in the alpha's whole support occupy columns
w+2,...,2w-1, of even length n=w-2:

* In band rows4/5, row4 stays blank because it is directly below the retained
  P bar in row3. The end sites (5,w+2),(5,2w-1) are retained selections, each
  already seeing its boundary P. Anchored pressure gives floor(w/3) units.
* In band rows6/7, both end columns stay BB. Their row6 sites touch boundary
  P and cannot become selected. Their row7 sites touch retained selections
  (7,w+1),(7,2w), each already seeing its TP anchor. The two-BB-ends lemma
  gives two different units.

The unit sets lie in different bands, and both boundaries of each gap belong
to this SAME alpha. All these units are private. This proves g(w)=floor(w/3)+2
for every extension, without enumeration or an immutable-old-singleton assumption.

## 5. The bound is attained by a retaining extension

Write j=c-(w+2), 0<=j<n=w-2. Define

    K={0,n-1} union {j:2<=j<=n-3 and (j-2) mod3 is 0 or1}.

Retain T0 and add (5,w+2+j) for j in K. For every 1<=j<=n-2 also add

    (7,w+2+j) if j in K,
    (6,w+2+j) if j not in K.                             (4)

The end sites j=0,n-1 of row5 are already in T0. All other additions lie away
from P. Row5 has anchored end selections, forced blanks j=1,n-2, and interior
TT,B blocks. Its blank runs have length at most two; its selected runs also
have length at most two. In rows6/7 each interior column has one selection:
where row5 is selected, use row7, and where row5 is blank, use row6. Every
selected pair sees only its partner; remaining additions are isolated. No new
selection is adjacent to an old selection outside these gap rectangles, and
no endpoint gains a neighbour. This proves feasibility and degree preservation
for arbitrary even w>=6, including the empty middle at w=6.

Row5 has exactly floor(w/3) blanks, so the upper gap has exactly that many BB
singletons. In the lower gap only its two end columns are BB; every other column
is BT or TB. Thus it has exactly two singleton units. No other gap in the
alpha's support contains a unit. The private support is exactly g(w).
The extension has

    |T|=2w+6-floor(w/3),
    S=4w-4+floor(w/3).

This attains the private-support minimum, not the minimum global numerical
slack. The rest of the board can contain other resources unavailable directly
to this alpha. In particular, the initially guessed half-density bound would
fail already at w=8: the actual extension has four private units, not five.

For w=8 the four physical rows inside the two gaps are displayed below; B is
a blank site. Horizontal selected pairs in rows5 and7 are allowed.

| Row | Gap columns10,...,15 |
| --- | --- |
| 4 | BBBBBB |
| 5 | TBTTBT |
| 6 | BTBBTB |
| 7 | BBTTBB |

The upper two rows supply two BB singletons, and the lower two supply two.
The [permanent w8 fixture](../develop/fixtures/bent_occupied_band_sharp_w8.json)
contains all 44 endpoints, 22 actual matching edges, 20 selections and the full
retained freezing schedule.

## 6. Cross-component repair and exact withdrawal cost

Place q>=1 copies at row offsets10i on a (10q-2)-by-(2w+2) board. Two blank rows
separate copies. Retain each matching and old selected set, and permit ANY
feasible no-new-P extension preserving all endpoint degrees. The same local
proofs give q alphas, (w-1)q betas and g(w) private units per alpha. Fixed
freezing schedules replay separately. The sets of all currently supported
original units U_i are private, disjoint, and satisfy |U_i|>=g(w).

Reserve any set R of distinct ORIGINAL INTERVALS, fixing T and M. Put

    t(R)=number of i with U_i subset R.

The maximum direct allocation has EXACT deficit t(R), since each unblocked
source can take its own private unit and every blocked source has none. Hence

    g(w)t(R)<=|R|.                                      (5)

Each copy also has its own beta B_i whose body is the actual horizontal matching
edge (6+10i,w-1)--(6+10i,w). Both N mates in row7+10i are blank, so these are BP
ends, and B_i has empty interval support. There is an actual TP--BP link

    (6+10i,w+1) -- (6+10i,w).                            (6)

Use this one link to cancel a blocked alpha with B_i: one alpha and one whole
beta become mixed. The beta supplies ONE credit; its other BP tip supplies
no second credit. Distinct copies use distinct beta owners and distinct tips.
Sources paid directly use none of these beta credits.

These are the ONLY declared TP--BP links in the fixed uniform band model.
There are no mixed owners. Thus for every R the exact full-model result is

    maximum value=q,
    minimum links=t(R).                                 (7)

For the upper bound use the direct/private assignments and (6). For the lower
bound every source with U_i subset R must use at least one link; a link has
one source owner, and these q physical links are distinct. It follows that
interval withdrawal never creates a full-model deficit in this family, even
when EVERY original interval is reserved. A sharp direct obstruction is not
therefore a full-network obstruction. Betas themselves are NOT reserved in
(7); preserving a locked old pack or changing the auxiliary directions is a
different model and is not implicit here.

At the saturating extensions, reserve all g(w)q direct units. Then t(R)=q,
equality holds in (5), and the full model still pays q at exact cost q. This
gives an all-width, all-copy distinction between direct resource loss and
cross-component repair, with no shared beta credit counted twice.

The private inventory also gives L>=g(w)q and therefore

    S>=beta+(g(w)-1)q=(w+floor(w/3))q.

This is a conditional coefficient-one statement on a family already known to
satisfy numerical compensation. It does not upgrade the universal5/6 result.

## 7. Reproducibility, formal scope and remaining cases

Run from the repository root:

    python3 develop/check_bent_gap_private_reserves.py --output output/bent-gap-private-reserves-validation.json
    python3 develop/check_bent_gap_private_reserves_formal.py --lean /path/to/lean-4.33.0 --output output/bent-gap-private-reserves-formal-validation.json

The arbitrary-size proofs are Sections1--6. Python checks the actual inventories,
endpoint degree profiles, old ordered freezing certificates, retained global
owner bodies, gap identities and private incidence. It compares withdrawal
formulas with independent resource allocation and the existing whole-fork
min-cost compiler. General mixed controls restore all crossing actual M edges.
Counts and executed scope are in the saved receipts; finite tests do not replace
the proofs.

The saved run passes 140 frozen family models: seven widths 6,8,10,14,20,32,64,
four copy counts 1,2,3,7, and each baseline, sharp extension and three random
retaining completions. These replay 45,500 strict endpoint events; the stored
w8 fixture independently replays 44 more. There are 1,400 interval-withdrawal
checks and 420 exact whole-model value/cost comparisons. The smallest private
gap domain has 11 feasible retaining completions, exhaustively checked; its
minimum is four. These computations test the all-width proofs above.

Another 66 partition models include 56 genuinely mixed-direction cuts, compared
independently with the existing crossing-M compiler. Twenty-five source
occurrences with old pair count below two now have at least two certified
units. All 66 small reserve assignments also agree with exhaustive allocation.
There are 9,050 local internal words and eight actual shifted-boundary controls;
the latter test the local boundary exclusion without claiming those local
P columns form an alpha. No claim that all general controls are frozen is made.

Local Lean 4.33.0 passes 10 declaration and individual axiom audits, with no
warnings, placeholders, native evaluation or new axioms. It proves
arbitrary-length list induction for the correct triple density,
anchored pressure, even-gap forest parity, private bound and ledger arithmetic.
It allows adjacent selected pairs. General coordinate/gap adapters, full physical
freezing for the inherited family, global private-set matching, beta cancellation
and arbitrary-width saturation are written proofs with executable checks, not
end-to-end Lean certification.

Permanent evidence:
[checker](../develop/check_bent_gap_private_reserves.py),
[Lean source](../formal/SubQuorum/BentGapPrivateReserves.lean),
[physical receipt](../output/bent-gap-private-reserves-validation.json),
[formal scope and receipt](../output/bent-gap-private-reserves-formal-validation.json).

The remaining cases include short bends without a pressured blank row, no-P
gaps filled entirely by BT/TB, degree-changing completions, and mixed seams
where a beta fallback is shared by several alphas or already reserved. These
require joint resources; the private/dedicated structure here must not be
assumed there. Submitted manuscripts and correspondence are unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
