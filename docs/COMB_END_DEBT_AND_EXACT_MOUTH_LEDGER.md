# Comb-end debt and an exact occupied-mouth ledger

19 October 2026. General extension of the transverse-comb mouth theorem.
This includes complete perpendicular straight combs ending inside mouths.
It gives an exact debt-and-slack identity rather than assuming those ends
are automatically compensated. The universal grid bound remains open.

## 1. Configuration and prescribed contacts

Use the feasible-pair, original corrected physical-tile ledger and whole
receiver conventions of the earlier notes. Prescribe B distinct positive
long-source components, with actual matching, supports and positive physical
alignment as in `LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`, including
its corrected even-arm freezing recurrence. Each source receiver has charge+1.
Normalize a source mouth as F={r,r+1} x {1,...,w-2}, w even>=8.
It has N=(w-2)/2 physical tiles, and both boundary columns are forced blank.

Allow every endpoint in F to belong to a prescribed complete perpendicular
straight comb. The comb has an even positive number of endpoints, consecutive
matching pairs, alternating perpendicular selected supports at all endpoints,
and one axial selected support beyond each end. Its endpoints can stop within
the mouth, pass through it, or start within it. We do not require extension
beyond both rows. All supports are actual original T.

Every prescribed comb is fully frozen by its two end-to-end waves, using the
retained-mate principle, independently of exterior bundles. The long sources
are also fully frozen. Thus all these endpoints, matching edges and supports
persist through objective-preserving normalization; other P can only disappear.
Every mouth still contains endpoints of prescribed perpendicular combs only.

Each whole comb receiver has original charge zero. No mouth contains P of
another prescribed long source. The earlier parallel/perpendicular separator
argument therefore still makes the physical mouths pairwise disjoint, even
though they now contain comb ends. This argument needs exclusion of other
long-source P, not exclusion of all P.

## 2. Exactly three physical types of endpoint tile

At a final single-terminal representative, the endpoint set in every unit
square is connected. A square inside F therefore meets at most one complete
comb, and its P consists of one full or one partial perpendicular column.
Two different complete combs cannot supply adjacent P; opposite-corner-only
P would force the other corners blank and violate occupied degree>=3.

Consequently every endpoint tile of F has one of the following counts:

| Type | P | T | Raw weight t+p/2 |
| --- | --- | --- | --- |
| Full column | 2 | 1 | 2 |
| Saturated end | 1 | 2 | 5/2 |
| Sparse end | 1 | 1 | 3/2 |

For a full column, alternating supports put one T in the paired adjacent
column, and that T forces the other corner blank. For a partial column,
the P is a comb endpoint and its axial T lies in the same physical tile.
If its perpendicular T is in the paired column, there are two T and the
last corner is blank. If the perpendicular T lies across the other tile
face, only the axial T is in this tile. The possible extra T at the endpoint's
unselected perpendicular neighbor is forbidden by the alternating support
of its next comb endpoint; the other corner is forbidden by the axial T.
This also holds for a two-endpoint comb. Completeness excludes unlisted P.

Let K be the number of endpoint tiles in F, S the sparse ends and U the
saturated ends. Put E=S+U, the number of one-P tiles. Every such one-P vertex
is a comb endpoint. A comb that occupies both mouth rows instead contributes
a full column, even if it starts at the upper row or ends at the lower row.

These are raw weights, not original corrected charges of partial receivers.
The latter may have matching transfers across the mouth boundary and remain
inside their actual whole comb receivers throughout the global argument.

## 3. Shifted squares give the sharp one-unit debt per sparse end

Use shifted unit squares with column pairs (2,3),(4,5),...,(w-4,w-3).
They partition the mouth after removing its two blank boundary columns.
Each square with no P has at most two T. With two P in a column it has at
most one T, since two would each see a P and the other T. With one P it has
at most two T, hence raw weight at most5/2. There are exactly E one-P squares
in this shifted partition: every partial-column endpoint lies in exactly one
square, whereas every full P column contributes its two vertices to the same
square. The blank boundary columns contain none.

Thus, writing mu(F)=|T in F|+|P in F|/2,

    mu(F)<=2(N-1)+E/2.

Define the shifted-square slack

    A=2(N-1)+E/2-mu(F).                              (1)

It is a nonnegative integer, not just a nonnegative half-integer. Indeed if
C is the number of full P columns, then |P in F|=2C+E and

    A=w-4-|T in F|-C.

Let Z_F be the physical no-P tiles in F, and let

    D_F=sum_(Q in Z_F)(2-t_Q).

The physical type table gives

    mu(F)=2K+(U-S)/2+sum_(Q in Z_F)t_Q,
    D_F=2N-mu(F)+(U-S)/2.

Substituting (1) and E=U+S yields the exact identity

    D_F=2-S+A,        A>=0 integer.                  (2)

In particular D_F>=2-S. Full transverse columns and saturated ends carry no
debt in this formula; each sparse end costs one unit, with additional slack
accounted exactly. The coefficient one is necessary: the earlier one-end
fixture has S=1,A=0,D_F=1, and the two-ending-comb fixture has S=2,A=0,D_F=0.
These are physical witnesses to the sharp coefficient, not an enumeration
argument for the all-length identity.

All assigned donors remain actual no-P tiles, whose original charge is t-2.
No original partial comb charge is used in (2), and no matching transfer is
closed at a mouth boundary.

## 4. A complete comb can incur this sparse-end debt only once

Consider one entire vertical comb in a fixed physical tiling. If its first
endpoint row is even, its last row is odd, so the physical endpoint tiles
contain full two-P columns. There is no physical one-P endpoint tile.
If its first endpoint row is odd, its last row is even. Its two physical end
tiles each have one P and an axial T. The endpoint perpendicular supports are
on opposite sides, because the number of endpoints is even. The paired adjacent
column is the same side for every tile along the comb. Therefore exactly one
end tile is saturated and the other sparse. Rotation gives the horizontal case.

Thus every complete comb has at most one sparse physical end tile. The mouths
are disjoint, so that tile is counted in at most one S_H. Consequently

    sum_H S_H <= number of prescribed crossing/contact combs.    (3)

More precisely the left side counts distinct combs whose unique sparse end
tile lies in a mouth. A comb can pass through any number of mouths, or meet
one through its saturated end, without being charged again. This supplies
unique ownership of debt as well as unique ownership of no-P resources.
It does not supply a compensating resource for that debt.

## 5. Exact global ledger and a broader coefficient-one criterion

Let an initial feasible pair have complete endpoint components each thin,
with at most one P-square, or one of the B prescribed long sources. Thin
means contained in two consecutive rows or columns. Impose the prescribed
complete-comb contact condition of Section1 in every source mouth, with the
actual comb matching and supports present initially.

Normalize globally. The prescribed sources and combs persist; endpoint deletion
preserves thin containment and cannot create new P-squares. Each nonprescribed
final receiver is nonpositive by the established thin/one-square theorem.
Every prescribed long receiver has charge+1. The physical no-P sets Z_(F_H)
are mutually disjoint and outside every endpoint receiver. Put S_total=sum S_H,
A_total=sum A_H, and let Z be all physical no-P tiles. The exact original ledger
and (2) give

    mn/2-|T_0|-|M_0|
      = sum_nonprescribed(-rho(R_J))
        + B-S_total+A_total
        + sum_(Q in Z minus union_H Z_(F_H))(2-t_Q).     (4)

Every term other than B-S_total is nonnegative, so

    |T_0|+|M_0|<=mn/2-B+S_total.                     (5)

In particular coefficient one holds whenever S_total<=B, and a strict
B-S_total deficit is obtained when S_total<B. The zero-debt case recovers
the transverse-comb theorem while allowing saturated ends and full columns
whose endpoints lie at the mouth boundaries. Sparse contacts are now covered
as well when their total count is at most the number of sources.

If S_total>B, (4) identifies the exact extra requirement: the unused no-P
deficits, shifted slack and nonprescribed receiver deficits must pay
S_total-B. We do not assert that this happens automatically. The two-end
obstruction has B=1,S_total=2,A_total=0, so mouth-only payment is insufficient.
Its actual global deficit is positive, supplied by resources elsewhere.

The original universal 5/6 bound remains available when (5) is weaker.
There is no global counterexample here, no arbitrary-comb-contact equality
claim, and no assumption that a zero-charge comb receiver pays a new unit.
The remaining task is to prove or refute an exterior payment theorem for the
distinct sparse-end owners in (3), with all matching transfers retained.

## 6. Verification and scope

The separate verifier `develop/check_comb_end_debt.py` checks 696 optimized
complete-source/contact configurations, six contact types, both support phases,
depths three and six, up to six contacts per mouth, and twelve reflection
images. Exact dynamic programming maximizes the added selected vertices for
each fixed contact set. It checks feasibility, terminality, full freezing,
whole receiver charges, physical tile types, shifted-square capacities, integer
slack, identity (2), and unique sparse-end ownership. The receipt is
`output/comb-end-debt-controls.json`.

A further fixture connects two source mouths by one complete comb. The two
mouths have (S,A,D)=(1,0,1) and (0,1,3). Thus one comb owns exactly one debt
unit despite contacting two mouths; the total donor payment is four and the
two source charges total two. The second mouth has unavoidable shifted slack
one in this fixture.

These are controls of the written general proof, not its replacement. No new
Lean statement is asserted for (2)-(5); the previous 81-declaration scoped
audit remains separate. The completed transverse-comb ACCEPT covers the
previous theorem and ending-contact obstacle, not this later extension.

The subsequent `COMB_END_FLUX_AND_CLOSED_CONTACT_NETWORKS.md` proves the
stronger identity A=U+D' by swapping end types in the shifted tiling. It
cancels internal comb connections and replaces the coarse S_total criterion
by a boundary count. Its proof and verification scope are recorded separately.
