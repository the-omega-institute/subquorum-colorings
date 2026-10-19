# Stepped-arm phase, charge-aware channels, and a negative-charge obstruction

19 October 2026. The arbitrary-length frozen family of
`GUARDED_CORNER_AND_STEPPED_ARMS.md` has nonnegative partial phase in both
directions in its prescribed physical alignment. Its full phase is at least
two, sharply, even though its corrected receiver charge is one. We extend
the existing conditional channel certificate to these components with their
actual charge included. A one-column translation of the same frozen family
then disproves a different proposed rule: a component's nonpositive charge
does not necessarily pay all of its negative phase.

These are all-parameter written proofs. The finite controls below test them;
they do not replace them. The universal coefficient-one grid inequality and
rectangular-grid triple equality remain open. Submitted manuscripts are unchanged.

## 1. Retained configuration and admissible regions

Fix k>=1 and b=2k+4. Retain exactly the complete endpoint component H_k,
actual matching, and prescribed selected supports in Sections 2-3 of
`GUARDED_CORNER_AND_STEPPED_ARMS.md`. Physical squares have relative starts
at even rows and odd columns. All prescribed sites lie in the ambient grid.
The complete all-k freezing proof there applies in any feasible exterior
preserving that matching, component and selected supports.

For clarity, the endpoint set is

    ({0,1} x {0,1,2,3}) union ({2,3} x {0,...,5})
      union ({4,...,b} x {0,1,2,5}).                 (1)

Feasibility means every selection has at most one occupied neighbor. A
complete endpoint component excludes any additional endpoint adjacent to H_k.
The physical receiver labels are fixed and its charge is one. This assertion
does not make every nonendpoint receiver corner blank: prescribed selections
remain occupied, as corrected in the companion note after written review.

Let C be a rectangular union of complete physical squares. For a horizontal
shift require both extreme columns of C to be endpoint-free, and trim them
before partitioning into squares shifted one column. For a vertical shift
require and trim endpoint-free extreme rows instead. These conditions concern
all endpoints in the configuration, not just H_k.

Let E_C(H_k) be the sum of raw excess

    |T intersect Q| + |H_k intersect Q|/2 - 2

over physical squares in C containing H_k endpoints; let E'_C(H_k) be the
corresponding shifted sum. Put Gamma_C(H_k)=E_C(H_k)-E'_C(H_k). This is
a raw partition difference, not a corrected charge for a truncated matching.

Each endpoint path within a physical two-row band is a consecutive horizontal
run; within a physical two-column band its endpoint set is connected and
occupies every row between its first and last endpoint rows. An encountered
path must therefore be included in full in the shifting direction: otherwise
it crosses an extreme column or row containing an endpoint. In a two-row
band the thick and thin arms may be included separately, and are counted
separately below. No claim is made for arbitrary nonrectangular regions or
cuts through an endpoint path.

## 2. The complete list of optional flank selections

Only the following additional selections can affect the raw tables:

    a = 1_T(-1,3),     c = 1_T(1,5),
    a_r = 1_T(r,3),    r=6,8,...,b-2.              (2)

Set a_4=0. Indeed (4,3) has the two endpoint neighbors (3,3),(4,2).
The bottom selection (b,3) is prescribed, not optional.

Here is a boundary check that makes this list exhaustive for arbitrary
feasible exterior data. All physical receiver labels are already fixed.
A new corner in a horizontal shifted endpoint square is on the inner
thick-arm flank, or one of the cap/chamber boundaries. The only unresolved
thick-arm corner is (r,3) at an even r strictly between 4 and b; the odd
corner (r+1,3) is blank beside prescribed (r+1,4). At the chamber boundary
the candidate (4,3) has two endpoint neighbors. In a vertical shifted
endpoint square, the top cap has only (-1,3) unresolved, since (-1,1)
is prescribed and forces its adjacent flank corners blank. The right
chamber cap similarly has only (1,5) unresolved: (1,6) is blank beside
(2,6). Bottom flank corners are fixed by the three axial selections in
row b+1. All remaining candidates either have two H_k neighbors or neighbor
a prescribed selection already incident to H_k. Completeness excludes
foreign endpoints next to H_k; in each singleton square the retained
selection excludes the opposite corner, so foreign components cannot share
an endpoint square in either partition.

All sites in (2) can be selected simultaneously in the blank exterior.
Each has exactly its adjacent H_k endpoint as an occupied neighbor. The
even inner-flank sites are spaced two rows apart; their neighboring odd
supports have a different column. The two cap sites are separated from
each other and from the inner-arm flank. Thus every subset of (2) is
feasible. The same old freezing witnesses remain valid.

## 3. Horizontal table and the loss of repeated thick-arm credit

Each row is an exact raw partition calculation for the indicated complete
endpoint path. The other arm in the same band, if present, is independent.

| Relative row band and path | Physical raw | Shifted raw | Gain |
| --- | --- | --- | --- |
| {0,1}, four-column cap | 0 | 0 | 0 |
| {2,3}, six-column chamber | 0 | 0 | 0 |
| {r,r+1}, thick arm, even r=4,...,b-2 | 0 | -1+a_r | 1-a_r |
| {r,r+1}, thin arm, same r | 0 | 0 | 0 |
| {b,b+1}, three-endpoint thick cap | 1/2 | 1/2 | 0 |
| {b,b+1}, thin-arm tip | 1/2 | -1/2 | 1 |

To check the repeated row directly, the physical thick-arm squares have
endpoint counts two and four, with respectively one and zero selections;
both raw excesses vanish. The shifted four-endpoint square has raw zero
and the shifted two-endpoint square has the single optional selection a_r,
giving -1+a_r. The physical thin-arm pair has its outer support; after
shifting it has the odd-row inner support, giving raw zero in both phases.
At the bottom thick cap, the shifted two-endpoint square has one selection
and the shifted singleton has two; its total remains 1/2. The thin-arm
singleton loses one selected corner when shifted and earns one. The cap
and chamber consist of full squares or two-endpoint squares with one support,
so both have zero raw excess in both phases. This includes k=1.

Path completeness from Section 1 now proves Gamma_C(H_k)>=0 for every
admissible horizontal C. For a whole-component region, summing gives

    Gamma_full,h = k+1 - sum_(r=6,8,...,b-2) a_r >= 2.         (3)

The all-blank optional flank gives k+1. Selecting all k-1 inner optional
sites reduces it to two. Thus claiming one immutable unit from every thick
arm band overcounts by k-1 in a feasible exterior. This is an unbounded
error in that proposed band-credit rule, not in the nonnegative phase theorem.

## 4. Vertical table and sharpness in both directions

There are four physical column bands containing endpoints:

| Relative column band | Physical raw | Shifted raw | Gain |
| --- | --- | --- | --- |
| {-1,0} | 1/2 | -1/2 | 1 |
| {1,2} | 0 | 0 | 0 |
| {3,4} | 0 | -2+a | 2-a |
| {5,6} | 1/2 | -1/2+c | 1-c |

For {-1,0}, all ordinary vertical pairs have raw zero; the bottom physical
singleton with two selections is replaced by a top shifted singleton with one.
For {1,2}, the physical full pairs and bottom two-endpoint cap have raw
zero; the top and bottom shifted caps also have raw zero and the interior
full pairs contribute zero. For {3,4}, the shifted pieces are a top singleton
with raw -1/2+a, a three-endpoint junction with raw -1/2, and a bottom
two-endpoint cap with raw -1. Their sum is -2+a. For {5,6}, the lower
axial and alternating side supports cancel between phases; the upper
shifted singleton has raw -1/2+c instead of the physical end contribution
1/2. These exhaust the finite cap cases and the repeated zero-raw pairs.

Each band path is connected in the vertical direction. Consequently the
table applies to every admissible rectangle meeting that path, even if H_k
escapes C in the other direction. Every entry is nonnegative, and

    Gamma_full,v = 4-a-c >= 2.                     (4)

Selecting every optional site in (2) simultaneously attains two in both
(3) and (4). The original physical receiver labels, charge one, and exact
unit guarded-corner donor remain unchanged. In particular its bottom donor
is still Q={b,b+1} x {3,4}, anchored at (b,3) and guarded by (b+1,5).

## 5. Adding stepped components to the channel ledger

Retain the terminal normalization, original long-source mouths, complete
straight combs and actual residual capacities of `COMB_CHANNEL_COMPENSATION.md`.
Allow in addition B_E prescribed positive elbows from
`ELBOW_SOURCE_COMPENSATION.md` and B_S stepped components in the positive
alignment of Section 1, with their actual matchings and selected supports.
Assume all other receivers are nonpositive. The endpoint-square ownership
check in Section 2 makes their raw contributions additive in both partitions.
Sections 3-4 give nonnegative partial stepped phase in either direction.

Let F be the original signed comb-end mouth incidence, A>=0 the additional
nonnegative source phases in those mouths, and Dprime>=0 their shifted
no-endpoint deficit. For each original no-endpoint physical square Q let
d_Q=2-|T intersect Q| and m_Q in {0,1,2} be its original mouth multiplicity.
Writing Delta=mn/2-|T|-|M|, the corrected exact doubled ledger is

    2Delta = F+A+Dprime + sum_Q (2-m_Q)d_Q + 2E
               -2B_E-2B_S,        E>=0.            (5)

Proof. The whole-receiver identity is
Delta=-B_L-B_E-B_S+D_all+E, with E the nonpositive receivers' slack.
The original mouth identities sum to
2B_L+F+A+Dprime=sum_Q m_Q d_Q. Substitute this into twice the first identity
and use 2D_all=sum_Q 2d_Q. This proves (5), including the actual charge of
every new positive receiver. No mouth is invented for a new component. QED.

For admissible whole channels C_j, let delta_j indicate unequal wall ends,
G_L,j,G_E,j,G_S,j be actual raw source phases and Phi_j the actual signed
comb-end phase. The boundary identity is unchanged:

    D_Cj = 2-delta_j+G_L,j+G_E,j+G_S,j+Phi_j+D'_Cj.

For nonnegative channel weights w_j satisfying, on every positive donor,

    sum_(j:Q in C_j) w_j <= 2-m_Q,                (6)

equation (5), nonnegative omitted terms, and the channel identity give

    2Delta >= F-2B_E-2B_S
      + sum_j w_j(2-delta_j+G_L,j+G_E,j+G_S,j+Phi_j).          (7)

This is a coefficient-one certificate whenever the right-hand side is at
least -1 and Delta is integral. For example every fully enclosed stepped
component contributes at least two phase units to a weight-one channel,
paying its doubled charge tax, provided (6) actually holds. A mere contact
with a regular band can contribute zero and does not pay that tax.

All phases here certify original physical deficits. They are not independent
supplies. If a direct guarded-corner payment has already reserved one unit
of a donor, the corresponding remaining physical capacity must be reduced
before applying a channel certificate. In particular the unmodified
full-weight channel and that direct payment cannot both spend the same unit.
The extension improves the old 5/6 bound to one for configurations satisfying
these explicit coverage and capacity hypotheses; no universal improvement
of 5/6 is claimed.

## 6. A uniform mixed-channel family with exact payments

Take even W>=32, d>=1, y=2d+4, k>=1 and wall half-lengths
ell_L,ell_R>=k+4. Begin with `occupied_family(W,d,ell_L,ell_R,blocker='none')`
of `develop/check_comb_channels.py`, namely the root, vertical walls at
columns 9 and 22 starting in row y+1, and its zero-payment original mouth.
Put the stepped construction at relative origin (y+4,13). Let
ell=min(ell_L,ell_R), delta=1 if the wall ends differ and zero otherwise.

The stepped support footprint lies in columns 12,...,19; the inward wall
supports lie at columns 10 and 21. The root arms lie outside these at
columns 3 and W+2. The top stepped support has row y+3, two rows after
the last mouth filling. Its bottom endpoint row is y+2k+8<=y+2ell and its
last support row is at most y+2ell+1. Hence the full footprints are separated
by blank columns/rows, and feasibility and the individual full freezing
proofs combine for every stated parameter. This also holds after adding all
optional flanks (2). The root and stepped receiver have charge one each;
both walls have charge zero.

The channel C has rows y,...,y+2ell+1 and columns 10,...,21. It contains
the entire stepped receiver, including the bottom tip in its terminal band
at minimal wall length. There are 6(ell+1) physical and 5(ell+1) shifted
squares. The original mouth still has zero payment and signed flux F=-2;
the walls have no end tiles inside C, so Phi_C=0. There is no extra stepped
mouth. Exact counts are:

| Optional flank choice | G_S | D_C | D'_C |
| --- | --- | --- | --- |
| None | k+1 | 10ell-7k-20-delta | 10ell-8k-23 |
| All | 2 | 10ell-8k-21-delta | 10ell-8k-25 |

For the physical count, the 3k+10 receiver tiles leave 6ell-3k-4 no-endpoint
tiles. Their selections are the twelve first-band mouth selections,
2(ell-1) intermediate wall supports, delta continuing-wall corners, and
k+2 stepped supports outside its physical receiver. Thus their total is
2ell+k+12+delta, giving the first D_C. All k+1 optional selections lie
in physical no-endpoint tiles, proving the second D_C.

In the shifted partition the stepped endpoint-square count is 3k+8:
two cap squares, three chamber squares, three per regular arm band and
three in the bottom band. It leaves 5ell-3k-3 no-endpoint squares. These
contain ten first-band selections, k+7 stepped supports and no intermediate
wall supports, hence k+17 selections. This gives the first D'_C.
The two optional cap sites (-1,3),(1,5) are in shifted no-endpoint squares,
while each optional inner-arm site lies in a shifted endpoint square.
Consequently the sharp choice reduces D'_C by exactly two, not by zero.
This distinction is necessary for the exact identity

    D_C-D'_C = 2-delta+G_S.                        (8)

Every positive physical channel donor has m_Q=0. Weight two therefore
satisfies (6) once. Taking B_S=1,B_E=0 in (7) gives

    2Delta >= -2-2+2(2-delta+G_S)=2(G_S-delta).

The baseline bound is Delta>=k+1-delta, and the sharp-flank bound is
Delta>=2-delta. Ignoring the new receiver's tax would overstate the doubled
bound by two. Reusing the weight-two channel or additionally spending its
guarded donor without reducing the allocation fails (6). These are errors
in those allocation choices, not counterexamples to the grid target.

## 7. A frozen negative-charge component that cannot fund all negative phase

Keep the same H_k, matching and prescribed selections, with no optional
flanks, but translate it by one column relative to the physical tiling.
Its physical square starts in relative coordinates are now even/even.
Translation preserves feasibility, completeness and the entire all-k
freezing certificate. The horizontal band table becomes

| Relative row band | Physical raw | Shifted raw | Gain |
| --- | --- | --- | --- |
| {0,1} | 0 | 0 | 0 |
| {2,3} | 0 | 0 | 0 |
| {r,r+1}, even r=4,...,b-2 | -1 | 0 | -1 |
| {b,b+1} | 0 | 1 | -1 |

The roles of the two horizontal partitions in Section 3 are reversed;
their endpoint-free exterior columns contain no missing endpoint squares.
Thus the displayed values follow directly from that already proved table.
The new physical receiver has 3k+8 tiles, 8k+24 endpoints and k+4 selected
corners, so

    rho_phys = (k+4)+(4k+12)-2(3k+8) = -k,
    Gamma_full,h = -(k+1).                         (9)

This disproves the candidate rule

    Gamma_full(H) >= rho_phys(H) for every frozen H with rho_phys(H)<=0.

Even spending its entire negative charge leaves one unpaid phase unit,
for every k. There are arbitrarily many negative bands in one fully frozen
component. This is not an issue caused by counting the same component twice.
It also lies outside the positive-alignment source hypotheses of (7).

For an explicit finite-grid realization use even row offset 4, column
offset 6, and ambient dimensions (2k+12) by 16. All unlisted sites are blank.
There are |T|=3k+11 and |M|=4k+12, so its objective is 7k+23 and its
global half-area deficit is 9k+73>0. Hence (9) refutes the proposed payment
rule, not the coefficient-one grid inequality or the triple equality.

More generally, for a region containing the whole component and both whole
endpoint-square receivers, with unique endpoint-square ownership in both
partitions, the actual matching has no net boundary transfer and

    Gamma_full(H) = rho_phys(H)-rho_shift(H).       (10)

This follows immediately by writing both whole receiver charges as their
raw sums. Therefore the failed rule is equivalent to requiring
rho_shift<=0 for that class. The family (9) has rho_shift=1. The weaker
candidate Gamma_full>=rho_phys-1 would follow from a universal ceiling
rho_shift<=1, and is attained by (9). That ceiling remains an open research
question here; finite searches have not proved it. Neither (10) nor this
example controls arbitrary partial-band phase.

## 8. Reproducible controls and next target

Run without Python optimization:

    python3 develop/check_stepped_arm_phases.py --output output/stepped-arm-phase-controls.json

The receipt records ALL_CHECKS_PASSED: twelve baseline/sharp parameter cases
through k=32, 1,728 admissible partial rectangles, every one of 252 optional
flank subsets through k=6, six translated negative-charge examples, 96 mixed
channels and eight tile-preserving symmetry images. It independently checks
feasibility, actual terminality and complete frozen certificates, raw tables,
whole receiver charges, exact no-endpoint payments and residual capacities.
The all-k geometric case divisions and ledger proof above are written proofs.
Existing 133 scoped Lean declarations retain their separate earlier receipt;
they do not formalize these new phase tables or the translated obstruction.

The original guarded/stepped review completed REVISE for the blanket
nonendpoint-corner sentence repaired in Section 1. Its conditional statement
that the repair would merit acceptance is not a terminal ACCEPT. The
new phase and channel extension require a separate completed assessment.
Its first same-conversation follow-up was rejected with HTTP 429 because
the user's ten in-flight task slots were occupied. No new task or review
verdict was produced; the unique request and stream are preserved and
`output/stepped-arm-phase-review.json` records this state.

The next general issue is a phase budget for arbitrary frozen components
that handles (9) and respects actual donor capacity. Establishing a universal
whole-receiver ceiling would address one whole-phase bound, but would not
by itself establish the partial-region estimates or channel coverage needed
for the grid inequality.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
