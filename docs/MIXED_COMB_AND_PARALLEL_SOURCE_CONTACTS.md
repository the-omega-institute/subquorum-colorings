# Mixed comb directions and complete parallel-source contacts

19 October 2026. This enlarges the accepted coalesced-mouth theorem in two
ways: complete straight combs may run along a mouth as well as across it,
and any part of a parallel prescribed source may enter a mouth, including
its chamber and nonterminal arms. The exact physical payment and initial
bound survive. The invariant is the signed raw excess, not individual end
type counts. Arbitrary source orientations at a contact remain excluded.

## 1. Initial hypotheses

Keep the even physical rectangle, feasible pair, actual matching, normalization
and whole-component ledger from
`COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`. Prescribe B distinct complete
positive long sources with the matching, supports, width/depth and positive
tile-preserving alignments of
`LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`, Section 1. Each source
is universally frozen and its complete physical receiver has charge +1.
Its mouth is the same one-tile-wide strip F_H as before.

Each other initial complete endpoint component is thin, contains at most
one P-square, or is a prescribed complete straight contact comb with its
actual consecutive matching, alternating side supports and both axial
supports. Require every endpoint initially in F_H to belong either to one
of these prescribed contact combs, in either direction, or to a prescribed
source K with F_K parallel to F_H. Any part of such a parallel source is
allowed. A source with perpendicular mouth direction is forbidden there.

No mouth-disjointness or nesting hypothesis is imposed. These are explicit
coverage hypotheses, not automatic properties of all feasible grid pairs.

All endpoints in any mouth belong to frozen prescribed components. Therefore
normalization leaves every mouth label and the full source/comb data fixed.
Other initial components only shrink and split; their final components retain
thin/one-square coverage and nonpositive receiver charge. In what follows work
at a single-terminal representative, retaining the initial objective.

## 2. The geometric union and internal source-tip count are unchanged

The proof excluding perpendicular mouth intersections in
`COALESCED_MOUTHS_AND_SOURCE_TIP_COMPENSATION.md`, Section 2, still applies.
Its trapped path belongs to the perpendicular source K, so cannot use a
parallel source or a comb as an exit through F_H. The enlarged condition
still forbids every K endpoint in F_H. Thus perpendicular mouths are disjoint.

Coalesce overlapping/adjacent parallel mouths within each physical band into
C strips G_i. They are globally disjoint and add no tile to the union G.
The extreme vertex columns of each horizontal strip, or extreme rows of a
vertical strip, remain forced blank by the extreme sources' supports.

Every source has two saturated physical tip tiles. Exactly two tips per
coalesced interval lie outside it, and every other tip of that interval's
sources lies inside. Terminal tile ownership makes all tips distinct.
Excluded extreme tips cannot enter a different parallel band or interval,
and cannot enter a perpendicular mouth under the new contact condition.
Hence, just as before,

    U_source=2B-2C.                                      (1)

Allowing chambers or nonterminal arms in other bands does not move a source's
tips: their physical tile band is still its own mouth band. Thus these new
contacts change none of the exclusions used in (1).

## 3. Parallel combs are wholly contained and have zero signed excess

For a unit square Q define its raw excess e(Q)=t_Q+p_Q/2-2. This is an
auxiliary counting weight; it need not equal its corrected physical charge.

**Parallel-comb lemma.** If a complete contact comb runs along G_i and meets
it in an endpoint, all its endpoints and its whole receivers in both column
phases lie inside G_i. The raw excess of each such receiver sums to zero.

Proof for a horizontal strip. The comb is a consecutive horizontal endpoint
path in one of its two rows. It cannot cross either extreme column, since
both vertices there are forced blank. Thus the entire endpoint path lies
between them. Every original physical tile containing one of these endpoints
is in G_i. After removing the two extreme blank vertex columns, every shifted
square containing an endpoint is also in G_i. Both collections contain every
endpoint of this complete component and hence all actual matching mates.

The complete straight-comb receiver formula in either alignment gives raw
sum zero: an aligned receiver has only p=2,t=1 tiles; a misaligned receiver
has p=2,t=1 middle tiles and one singleton of each of p=1,t=1 and p=1,t=2.
The two singleton excesses -1/2,+1/2 cancel. Transposition proves the other
direction. A comb contained in G_i cannot meet a perpendicular disjoint strip
in an endpoint. QED.

Individual end types need not exchange. For example a horizontal comb whose
even number of endpoints starts at an even column has no physical singleton
tiles. Under a one-column shift it gains one sparse and one saturated tile.
Its signed singleton excess is zero in both phases. Assuming type-by-type
exchange here would be false.

## 4. The complete parallel-source table includes chambers

Consider a source with horizontal chamber parallel to a horizontal G_i.
In the physical tiling all endpoint-containing source tiles have one of

    (p,t)=(4,0), (2,1), (1,2).

The first two have raw excess zero. The last are exactly its two terminal
tip tiles, each with excess +1/2. All labels are forced by the source supports.
In particular a full arm tile's raw excess is zero even if its corrected
physical charge receives a positive matching transfer.

Shift the square columns by one while keeping the same row pair. A chamber
occupies two complete physical rows and an even number of columns starting
at an odd column. Its physical interior tiles have p=4,t=0 and its two
physical edge tiles have p=2,t=1. In the shifted partition the entire chamber
is partitioned into p=4,t=0 squares. Its lateral selected supports lie outside
those endpoint squares and are counted wherever they occur as ordinary
selected vertices, possibly in shifted no-P squares.

Every full arm column has p=2,t=1 in both phases: alternating supports put
one selected vertex on either paired side. Each terminal tip changes from
p=1,t=2 to p=1,t=1. Its axial support and the next arm endpoint's support
force both opposite-side corners blank. These statements persist under
tile-preserving reflection and transposition. Thus a parallel source's only
nonzero endpoint-square excesses in the two partitions are +1/2 at each
physical tip and -1/2 at each shifted tip.

No unit square, shifted or physical, mixes different endpoint components.
This is the accepted terminal ownership lemma for any unit square: two
diagonal P with neither other corner P force both other corners blank, which
would leave either P with occupied degree at most two. All other nonempty
P subsets of the four-cycle are connected. Thus the source and comb tables
can be applied component by component, including chamber tiles with four P.

## 5. Only the signed imbalance must swap

Let S_i,U_i be all physical sparse/saturated singleton counts in G_i, including
parallel comb ends and source tips. Let S'_i,U'_i be the corresponding shifted
counts. All other endpoint-containing squares have raw excess zero.

Perpendicular comb ends exchange types as before. Source tips change from
saturated to sparse. Each parallel comb has both or neither singleton ends
in each partition and hence zero signed imbalance in both phases, by Section 3.
It follows that

    U'_i-S'_i=-(U_i-S_i).                               (2)

The separate identities S'_i=U_i and U'_i=S_i need not hold. Equation (2)
is the necessary and sufficient type information for the counting argument.

Put mu_i=|T in G_i|+|P in G_i|/2 and let n_i count physical tiles. Denote
actual physical no-P deficit by D_i and shifted no-P deficit by D'_i.
The physical raw table gives D_i=2n_i-mu_i+(U_i-S_i)/2. The shifted squares
count the same vertices after removing two blank columns and number n_i-1.
Equation (2) therefore gives

    D'_i=2(n_i-1)-mu_i-(U_i-S_i)/2,
    D_i=2-S_i+U_i+D'_i,       D'_i>=0.                  (3)

This is the same physical identity as before, now justified without a false
type-by-type swap or a false assertion that each encountered arm has zero
corrected charge. Selected vertices outside shifted endpoint squares are
fully included in mu_i and D'_i; none is dropped as a support.

## 6. Global coefficient-one theorem in the enlarged class

For each complete contact comb flag whether its original physical sparse
and saturated end tiles lie in G. Let I,O,J count both, sparse-only and
saturated-only membership. A parallel comb contributes both or neither and
so never contributes O or J. Complete-comb conservation and (1) give

    sum S_i=I+O,
    sum U_i=I+J+2B-2C.

Sum (3) over the disjoint strips. As in the accepted theorem,

    D_total=2B+J-O+sum D'_i.

Every whole source receiver is still counted once at charge +1. All other
whole receiver deficits and all physical no-P deficits outside G form a
nonnegative remainder R. The original corrected ledger gives exactly

    mn/2-|T_0|-|M_0|=B+J-O+sum D'_i+R.

**Mixed-contact theorem.** Under the initial hypotheses in Section 1,

    |T_0|+|M_0| <= mn/2-B+O-J.

In particular O<=B+J gives coefficient one, and O=0 gives strict margin B+J.
Within this enlarged class the entire |M_0|/6 loss in the universal 5/6 bound
is removed. No actual no-P tile is allocated more than once. Parallel combs
are closed whole receivers in both auxiliary partitions; source arms are not
declared separate neutral receivers. Every source matching transfer remains
inside its full receiver in the original ledger.

## 7. Two arbitrary-size families newly admitted by the theorem

The following source-only families have O=J=0 and C=B=k. Source i, for
0<=i<k, has raw chamber origin (4i,4i) and width 8(k-i)+6. Apply the common
translation (2,3) and leave every unlisted vertex blank.

For the **arm-contact family**, set depth h_i=2k+1-i. Its raw tip row is
4k+4+2i. Every earlier source mouth contains the two full arms of every
later source. It contains no foreign tip or chamber. Sources are distinct,
complete and feasible: chamber origins differ by four in both coordinates,
arms differ by at least four columns, and the earliest mouth is eight rows
below the last chamber's origin. Every selected support therefore retains its single
intended endpoint neighbor. The freezing waves apply in this completion.
There are exactly k(k-1) full arm tiles in all mouths.

The two positive corrected half-charge tiles immediately above source i's
tips lie in source i-1's mouth for i>=1. Their total corrected charge inside
other mouths is k-1, despite each arm tile's raw excess being zero. This is
a direct reason to retain whole source receivers in the proof. The family
fits in (6k+8)-by-(8k+14), has |T|=6k^2+12k and |M|=7k^2+14k, and receives
the proved bound objective<=mn/2-k for every k.

For the **chamber-contact family**, set h_i=1. Its raw tip row is 4i+4,
which is exactly the next source's chamber row. Consecutive sources meet
the same two-row band only through the outer source's tips and the inner
source's chamber, separated by four columns at either side. More distant
sources have separated occupied row ranges. These separations prove full
feasibility, completeness and freezing at every k. Each mouth except the
last contains the entire chamber of the next source. There are
2(k^2-1) physical p=4,t=0 tiles in all mouths, so a proof restricted to
full endpoint columns cannot cover them. The family fits in
(4k+6)-by-(8k+14), has |T|=10k and |M|=4k^2+13k, and also satisfies the
proved bound objective<=mn/2-k for every k.

These are general constructions with symbolic proofs, not finite inference.
They lie outside the earlier tip-only contact condition for every k>=2.

## 8. Remaining scope

Perpendicular-source intrusion, arbitrary bent endpoint components and
unmatched sparse debt beyond O<=B+J remain open. The earlier all-radius
end-local donor obstruction is unaffected. This note concerns the matching
bound in its stated class; it does not establish grid triple equality.
The earlier coalesced-mouth ACCEPT covers the earlier hypotheses, not this
extension. Written proofs, finite controls and any scoped Lean verification
must be reported separately.

## 9. Reproducible verification and review status

`develop/check_mixed_source_contacts.py` checks 253 physical configurations
and 56 symmetry images; `output/mixed-source-contact-controls.json` records
ALL_CHECKS_PASSED. The explicit arm/chamber families are checked through
k=24, together with parallel and perpendicular complete comb contacts,
both support phases and mixed-orientation disjoint clusters. The controls
check feasibility, complete endpoint ownership, freezing, both square
partitions, the full original physical ledger and unique physical donor
ownership. In 224 cases the individual type-count swap fails while the
signed identity (2) holds. These finite checks test the general proof;
they do not establish its arbitrary-size conclusion.

The standalone local Lean 4.33.0 audit passes 90 scoped declarations,
recorded with source hashes in `output/mixed-source-contact-formal-check.json`.
The five new declarations in `formal/SubQuorum/ParallelCombFlux.lean`
prove four exact tile-count formulas for an explicitly labeled horizontal
comb of arbitrary positive even endpoint length, and prove its whole raw
receiver balance in both column phases by finite-sum induction. This is an
unbounded coordinate/count proof. General placement, geometric containment,
the source chamber/arm table, coalesced union counts and the complete
mixed-contact theorem above remain written proofs. The other 85 declarations
retain their prior scopes. No full geometric formalization is claimed.

The earlier coalesced-mouth review c71b6706-97f9-45b8-b411-15d7c10a137b
completed ACCEPT for its supplied theorem and unaugmented nested family;
see `docs/reviews/2026-10-19-coalesced-mouth-assessment.md`.
The new mixed-contact review 40d1b52d-a624-4622-a41b-f1a442bad51a failed
with `infrastructure_retry_exhausted` / `cdp_disconnected@typing` after four
broker attempts. It produced no mathematical assessment. Its exact terminal
record is archived in `output/mixed-source-contact-review-response.json`.
The earlier ACCEPT does not cover the new extension.

Reproduce the controls and formal audit with:

```sh
python3 develop/check_mixed_source_contacts.py --output output/mixed-source-contact-controls.json
python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0 --output output/mixed-source-contact-formal-check.json
```
