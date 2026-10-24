# Transverse combs preserve terminal-mouth compensation

19 October 2026. General written extension of
`LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`. The endpoint-free-mouth
hypothesis is replaced by explicit complete transverse-comb contacts. This is
not a universal occupied-mouth theorem or a claim about all thin contacts.

## 1. Allowed contacts and the normalization invariant

Retain the prescribed even-width w>=8, odd-arm long sources of the preceding
note, their actual matching, selected supports and positive alignment. Their
whole receivers have original corrected charge +1. Normalize one source so
its mouth is F={r,r+1} x {1,...,w-2}, r=2h+2. Its first and last columns
are forced completely blank, independently of endpoint-free assumptions.

A permitted crossing owner is a distinct complete straight vertical endpoint
component at a column c inside F. Its number of endpoints is even, its actual
matching pairs consecutive endpoints from one end, and it extends to at least
row r-1 above and row r+2 below F. Require its usual straight-comb supports:
one perpendicular T at every endpoint, alternating left/right along the path,
and an axial T beyond each end. All these supports are actual original T.
The same owner can cross more than one source mouth; no payment is assigned
to the owner itself. For rotated sources, require perpendicular crossings.

Suppose every endpoint in each mouth belongs to such a complete prescribed
crossing comb. In particular the mouth contains no endpoint of another long
source. A comb appearing in a mouth occupies both its rows in one column;
no endpoint of that comb lies in any other column.

These crossing components are universally frozen. An end has axial and
perpendicular selected supports and cannot be promoted. From that end, the
odd-index endpoint wave uses a perpendicular support and the retained mate
of the preceding frozen odd endpoint. From the other end the analogous wave
freezes the even indices. The actual consecutive matching makes these two
waves exhaustive. The retained-mate argument applies to simultaneous exterior
bundles. Therefore both the long sources and all prescribed crossing combs
persist during global bundle normalization. Other endpoints can only disappear,
so no unprescribed endpoint enters a mouth.

The complete straight-comb theorem gives whole receiver charge exactly zero
for each crossing comb in every physical alignment. This is a statement about
its entire receiver. Individual mouth tiles may have nonzero corrected charge
because their matching mates can lie beyond the mouth.

## 2. A weighted bound in shifted squares

For a vertex set S define its raw weight

    mu(S)=|T intersection S|+|P intersection S|/2.

This is only a counting weight. We continue to use the original corrected
physical-tile ledger for the global inequality.

Every unit square contained in F has mu<=2. Indeed, its P set is either empty
or one complete two-row column. There cannot be two P columns in the square:
they would be adjacent and hence in the same endpoint component, contrary to
the prescribed distinct complete straight crossings. If there is no P, local
feasibility allows at most two selected corners. If there are two P in a
column, only the other two corners can be T. They cannot both be selected:
each would see its P neighbor and the other selected corner. Hence t<=1,
p=2 and mu<=2.

Both boundary columns of F have weight zero. Partition the remaining even
width w-4 into shifted unit squares with column pairs (2,3),(4,5),... . Thus

    mu(F)<=w-4.                                      (1)

This argument is independent of the number of crossings, their spacing and
the phase of each alternating support pattern. It is not a finite-state
extrapolation.

## 3. Remove neutral crossing tiles before spending any deficit

Let N=(w-2)/2 be the number of physical mouth tiles, K those that contain P,
and Z_F the remaining physical tiles. Each P tile contains exactly one
two-row comb column. Alternating perpendicular supports put precisely one
T in the other column of that physical tile. The other site is blank,
because that T already has its adjacent endpoint and forbids another occupied
neighbor. Consequently every such tile has raw weight exactly 2.

As a result,

    mu(F)=2K+sum_(Q in Z_F) t_Q,
    |Z_F|=N-K,
    sum_(Q in Z_F)(2-t_Q)=2N-mu(F)>=2.                (2)

These are physical no-P tiles, so their original charge is t_Q-2, without
any saturated matching correction. Formula (2) is the desired compensation
lemma for arbitrarily many complete transverse combs.

We do not sum the original charges of crossing tiles inside F and call that
the donor. Such a tile can receive a positive half-unit from a saturated mate
outside F. Nor do we claim mu equals original charge on this partial region.
Instead, all crossing tiles stay inside their actual whole comb receivers,
each of charge zero, and only Z_F is assigned as payment. This avoids both
unclosed matching transfers and repeated use of any part of a comb receiver.

## 4. The allocated no-P tiles are disjoint across orientations

The pairwise-disjoint-mouth argument needs a weaker hypothesis than an
endpoint-free mouth: for distinct prescribed long sources H,J, it suffices
that F_H contains no P of J and F_J contains no P of H. The present contact
condition supplies exactly these two exclusions.

For parallel mouths, unequal overlapping tile intervals place a tip of one
long source in the other's mouth, contradicting that exclusion. Equal
intervals identify or join the two tips and contradict distinct complete
components.

For perpendicular mouths, normalize H as above. A vertical mouth F_J meeting
F_H has tip rows u<=r-1 and v>=r+2 and both columns strictly between H's arms.
If u<=0, F_J contains a chamber endpoint of H. If u=1, the tip belongs to H.
Otherwise J has one endpoint in I={2,...,r-1} x {1,...,w-2} and one outside I.
A P path in J cannot exit I through the upper or lateral boundary, which
belongs to H. It cannot exit through the lower boundary, whose sites belong
to F_H and contain no endpoint of J. That boundary may contain crossing-comb
endpoints, but none belongs to J; a J path cannot use them without merging
the purported distinct complete components. Connectedness of J is contradicted.
Thus all physical F_H are disjoint, and so are their subsets Z_(F_H).

In addition every Z_(F_H) is disjoint from every endpoint receiver. This is
the actual payment partition. A comb receiver may meet several mouths, but
its charge is included exactly once, as an ordinary whole receiver; none of
its tiles is used in any mouth payment.

## 5. Initial-pair theorem with occupied mouths

Let (T_0,M_0) be feasible on an even-by-even rectangular grid. Every complete
initial endpoint component must be thin, have at most one P-square, or be one
of B prescribed positive long sources with their actual matching and selected
supports. In every prescribed mouth, require all initial endpoints to belong
to prescribed complete perpendicular crossing combs of Section 1. Their
matching and alternating/axial T supports must be present initially. Here
thin means contained in two consecutive rows or columns, and B counts distinct
complete initial long-source components. The resulting inequality is

    |T_0|+|M_0|<=mn/2-B.                             (3)

Run objective-preserving bundle normalization. The long sources and crossing
combs persist by their universal freezing; no P is added elsewhere. The
mouth contact condition and complete components persist. Containment in the
original two rows/columns survives endpoint deletion, and deletion creates
no new all-P square. Thus thin/one-square coverage passes to every other
final component, whose whole receiver is nonpositive. All assigned no-P sets
are mutually disjoint by Section 4, and equation (2) pays at least two units
for each source's positive unit.

For the final pair write D_H=sum_(Q in Z_(F_H))(2-t_Q) and let Z be all no-P
tiles. The original ledger gives exactly

    mn/2-|T_0|-|M_0|
      = sum_nonprescribed(-rho(R_J))
        + sum_prescribed(D_H-1)
        + sum_(Q in Z minus union_H Z_(F_H))(2-t_Q).

The middle sum is at least B; all other terms are nonnegative. Every actual
matching transfer closes inside its own complete receiver, and every donor
tile occurs in one explicitly disjoint no-P set. This proves (3).

The preceding endpoint-free theorem is the zero-crossing special case. The
earlier fully frozen width-ten/depth-two comb-crossing fixture now satisfies
this theorem. Thus the extension covers a genuine occupied-mouth obstruction
to the preceding proof, while retaining a precise contact hypothesis.

## 6. Remaining configurations

The argument does not cover a comb ending within the two-row mouth, a
parallel comb lying in it, a bent/branched receiver entering it, or another
positive source whose endpoints meet it. In these cases P need not occur
as full transverse columns, the shifted-square weight bound or the exact
neutral physical-tile removal can fail, and whole matching transfers must
be retained. General grid coefficient one and triple equality remain open.
Finite optimization and physical controls are supplementary; verification and
independent-review scope are recorded separately.

There is a concrete obstruction to allowing arbitrary comb ends while keeping
the same no-P-mouth payment rule. Take w=12,h=3,r=8 in the sparse source
baseline. Add a four-endpoint vertical comb in column 4 at rows 5,...,8 and
another in column 7 at rows 9,...,12, each with consecutive matching pairs.
Their selected supports are respectively

    {(4,4),(9,4),(5,3),(6,5),(7,3),(8,5)},
    {(8,7),(13,7),(9,6),(10,8),(11,6),(12,8)}.

Finally select both row-8 and row-9 sites in columns 2 and 9. Every selected
site sees exactly one occupied neighbor: a source/comb endpoint, or its own
vertical selected partner. All remaining sites are blank. The source and
both complete combs are universally frozen by their fixed supports and matching.
In the physical mouth, all three no-P tiles are saturated. Hence its assigned
no-P deficit is zero; the proposed broader payment rule fails even with two
zero-charge whole comb receivers. Translation (2,3) gives a 16-by-20 fixture.

The two comb endpoint tiles in the mouth each have original charge -1/2.
Their whole receivers have charge zero, so their remaining tiles outside
the mouth have total charge +1. Spending that partial -1 while simultaneously
counting the whole comb receivers as zero would omit the compensating +1
outside. The saved fixture checks these exact original matching transfers.
This is a counterexample to the broader payment rule, not to the grid bound.

## 7. Completed verification and review boundary

`develop/check_transverse_comb_mouths.py` checks 147 source/comb families,
including up to eight simultaneous crossing components, every support phase
through four crossings, and longer unequal extensions above and below the
mouth. For each fixed endpoint configuration, an exact column dynamic program
maximizes every additional selected site in the entire mouth, and the resulting
physical pair is checked independently. All no-P payment deficits are at least
two. There are also 24 symmetry images. For the width-ten/depth-two fixture,
independent exhaustive enumeration checks all 4,096 additional-selection masks,
finds 20 feasible completions and confirms the sharp deficit two.

A two-source fixture has one complete comb crossing both mouths. Its two
disjoint no-P payments each equal two, while the shared comb receiver is
counted once at charge zero. The two-ending-comb obstacle is independently
checked with exact original inside/outside receiver charges. The receipt is
`output/transverse-comb-mouth-controls.json`. These controls are not premises
of the general proofs.

The sequential local Lean 4.33.0 audit passes 81 declarations, three new in
`formal/SubQuorum/TransverseCombMouths.lean`: the corrected all-length even-arm
freezing wave on the actual integer grid, under explicit mate identities;
physical transverse-square selected capacity; and conditional neutral-tile
removal arithmetic. The complete comb classification, prescribed mate adapters,
shifted-square cardinalities, perpendicular separator and global covered-class
theorem remain written. The receipt is
`output/transverse-comb-mouth-formal-check.json`.

The preceding long-arm review was REVISE for a real adjacency error in its
even-arm recurrence. The original note is corrected and the recurrence above
is now formally checked; the review is archived without claiming ACCEPT.
The original conversation has a follow-up reviewing both the repair and this
extension. Its verdict is recorded separately; prior unit-tail ACCEPT does not
cover the extension or the two-ending-comb obstruction.
