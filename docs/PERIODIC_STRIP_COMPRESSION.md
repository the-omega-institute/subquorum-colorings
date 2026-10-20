# Periodic strip compression for the full mixed-source allocation problem

21 October 2026. Any complete feasible family of n>=1 original U/rotor sources
can be compressed to coordinate spans at most 512n+2, preserving its exact
legal-owner Horn lattice and all canonical side marks. Reserve and allocation
margin do not increase, simultaneously for every legal retained subfamily.
Thus a negative allocation counterexample, including its canonical least
demand-preserving hull, cannot require arbitrarily long geometric dimensions
at fixed source count. This is a reduction for the FULL unrestricted finite
source problem, not a proof of allocation or rectangular-grid equality.

## 1. Setting and theorem

Retain the complete fixed-source hypotheses of
[source retention](SOURCE_RETENTION_HORN_CLOSURE.md) and the exact identity
[2R=A+U0+Z0+H](EXACT_GEOMETRIC_EVENT_RESERVE.md). U widths w>=6 and independent
leg heights a,b>=4 are even. Every phase, lattice isometry, finite number of
owners and permitted rotor is allowed. Original endpoints are disjoint;
original supports outside the endpoint union are mandatory. Source labels
are kept fixed throughout compression, but U dimensions and their canonical
matchings are reconstructed when a straight section is shortened.

There is a finite sequence of deletions of aligned two-row or two-column
strips producing another allowed complete family F' with the SAME n owners:

1. A set of retained owners is feasible in F exactly when it is feasible
   in F'. The nontrivial original-owner Horn clause keys are identical.
2. Every original positive owner stays positive, and every one of its two
   actual side indicators is identical in each legal restriction. Thus N
   and G, including their labelled incidences, are preserved.
3. For every legal retained owner set I, R'(I)<=R(I) and mu'(I)<=mu(I).
4. Both occupied coordinate spans of F' are at most 512n+2. An even
   translation and at most two boundary rows/columns place it inside an
   aligned even rectangle of side lengths at most 512n+4.

There is no source-count restriction. The linear constant is deliberately
loose; no sharpness is claimed. All-source and all-subfamily assertions have
general proofs below. The finite controls are separate verification.

## 2. A bounded set of distinguished coordinates per source

Normalize a U as the endpoint set

    {0,1} x {1,...,w}
      union {2,...,a} x {1}
      union {2,...,b} x {w}.

Its support set consists of the four isolated points

    (0,0), (0,w+1), (a+1,1), (b+1,w),

and the four period-two strings

    (r,0),       r=2,4,...,a;
    (r,2),       r=3,5,...,a-1;
    (r,w+1),     r=2,4,...,b;
    (r,w-1),     r=3,5,...,b-1.

For the endpoint rectangles use their opposite corners: (0,1),(1,w),
(2,1),(a,1),(2,w),(b,w). Together with the four support points and both
ends of the four strings these give 18 feature points. Their row and column
coordinates include every interval endpoint of every original P/T piece,
also after an isometry.

Add the two canonical guard records, four points each. Finally add all four
corners of every original regular-singleton or triple tile. The U catalogue
has at most two such tiles: positive phase00 has two regular singletons,
phase11 has two triples, and the other phases have neither. This gives at
most 18+8+8=34 feature points per U.

A rotor has eight endpoints and eight original supports. Use all 16 points
and the corners of its at most four regular-singleton/triple tiles, giving
at most 32 feature points. Its diameter is at most five in either axis.
Thus at most 40n distinguished row coordinates, and at most 40n distinguished
column coordinates, suffice for every allowed family. The padding to 40
does not grow with any U dimension.

## 3. The local source-preserving splice

Let q be even. Assume neither q nor q+1 is within distance four of any
distinguished row coordinate. Delete these two rows and map every remaining
point (r,c) to itself for r<q and to (r-2,c) for r>=q+2. The four rows
q-1,q,q+1,q+2 are away from all endpoint/support interval changes. For
EQUAL ORIGINAL OWNER labels, both endpoint and support patterns satisfy

    row(q-1)=row(q+1),   row(q)=row(q+2).             (1)

Indeed each P/T piece is either constant or period two along this entire
feature-free band. The same periodicity extends through rows q-3,...,q+4.

Each U stays an allowed U. If the deleted strip is along its stems, its
bar is protected, and each stem crossing the strip is shortened by two;
the two heights can change independently. If the strip is along its bar,
the two outer stems and their nearby guard records are protected, and an
interior deletion shortens the width by two. Otherwise the source merely
translates or is unchanged. Signs and tile phases are unchanged since the
translation has even length. The four-row protection around interval ends
excludes shortening to a forbidden width or height. In particular a width
below six or height below four cannot arise from a permitted cut.

The explicit period-two support strings and isolated support points map
to exactly the new constructor's original support set. Endpoints map to
its new endpoint set. Regenerate the constructor's canonical matching;
when a matching edge crossed a deleted row it is the new seam pairing,
rather than the incomplete old matching, that must be used. All original
matching requirements hold in the NEW family. No old proof asserts this
operation is a retained subfamily of the OLD fixed family.

A rotor cannot straddle this strip: all its occupied rows are protected,
and its diameter is smaller than the combined protective intervals. It
therefore stays rigid, possibly translated by two.

## 4. Feasibility in both directions, with the same Horn lattice

For any owner subset I, the new endpoint and occupied patterns are the
pullbacks of the old patterns by the inverse embedding r -> r for r<q,
r -> r+2 for r>=q. At the upper seam, the new downward neighbor has the
same owner-labelled data as the deleted old downward neighbor by (1).
At the lower seam the corresponding statement follows from the other
equality in (1). All other neighbors transport directly. Thus each retained
point has exactly its old occupied degree, original support labels and
endpoint labels. Selected feasibility, endpoint degrees and endpoint
ownership survive for EVERY subset.

Conversely, an old violation at a retained point has the same violation
after transport. An old support conflict located in a deleted row has a
copy two rows later, outside the deleted strip: all original endpoint,
support and neighbor labels repeat, since the larger feature-free band
extends past those neighbors. The same original producer, occupying owner
and consuming endpoint owner occur. Every old nontrivial Horn clause
therefore still has an occurrence; every new occurrence lifts to an old
one, including across the seam. The ORIGINAL OWNER clause keys are exactly
equal, even though their coordinate witnesses can move or disappear.

The exact Horn characterization now proves feasibility equivalence for
all retained owner subsets and equality of closure on every seed. This is
stronger than checking legality of the full family alone. It covers restored
support/support conflicts as well as endpoint/support conflicts.

## 5. Exact margin loss: only nonnegative boundary defect is removed

All regular-singleton and triple tiles were distinguished and protected,
together with their intratile support points. Their owner-labelled profiles,
activation and final fullness are unchanged in every retained subset.
Rigid rotor singleton/triple pairings are unchanged too. Therefore for
every legal I the three counts A(I),U0(I),Z0(I) are invariant.

Every physical tile outside the deleted strip transports to exactly one
new tile, with the SAME original endpoint/support profiles and final
endpoint owners. Its local boundary defect h_Q is identical. The deleted
strip is one whole aligned tile row because q is even. Let

    Hstrip(I)=sum of h_Q(I) over that tile row.

Every h_Q is nonnegative by the exact geometric defect theorem. Hence

    2R'(I)=A(I)+U0(I)+Z0(I)+H(I)-Hstrip(I),
    2(R(I)-R'(I))=Hstrip(I)>=0.                     (2)

The deleted total is automatically even, by the two integer reserves;
evenness is not a further hypothesis or an empirical observation.

Canonical guard records are protected. Each side's fixed original support
and its unique endpoint consumer keep their labels. The gate-consumption
theorem therefore gives exactly the same side marks in every feasible
retention. Positivity is unchanged by the even source-phase transport.
Equivalently, one can check marks directly without the gate theorem:
the protected anchor/guard records protect their three original endpoint
protectors, whose actual occupied degrees are unchanged. This gives the
same degree-four side indicators in every legal retention.
Thus N'(I)=N(I), G'(I)=G(I), and (2) gives the exact formula

    2(mu(I)-mu'(I))=Hstrip(I)>=0.                   (3)

This counts one deleted tile defect once. It neither spends original
negative mass again nor assumes reserve monotonicity under adding owners.
The operation shortens geometry; it is not source deletion or legal union.

## 6. Termination and the linear coordinate bound

Every permitted deletion reduces the total occupied row span by two;
the global extremal occupied rows occur among the source interval ends
and are protected. Repeat until no permitted even q exists.

With K<=40n distinguished row coordinates, their distance-four protective
intervals contain at most 9K integer rows and have at most K components.
Between these intervals every remaining unprotected run has length at most
two. A run of length at least three contains an aligned even-starting pair,
which would permit another deletion. There are at most K+1 such runs.
Thus the occupied row span is at most

    9K+2(K+1)=11K+2 <= 440n+2 <= 512n+2.

Recompute feature coordinates after each operation; their number remains
bounded by 40n because the reconstructed sources stay in the same catalogue.
The count above applies to the final configuration, regardless of how many
steps occurred. Transpose, repeat for columns, and transpose back. Column
compression leaves the established row span unchanged. This proves the
two-axis bound. Even translation preserves the physical phases; padding
the resulting coordinate box gives the stated aligned rectangle bound.

## 7. Consequence for the unrestricted compensation target

If mu(F)<0 then mu(F')<=mu(F)<0. The number of sources is unchanged, so a
source-minimal counterexample also has a representative in this bounded
geometric form. More strongly, all labelled positive/consumer incidences
and all Horn closures are unchanged. Its canonical least demand-preserving
hull is therefore EXACTLY the same owner subset after compression.

The signed-loss target from a canonical hull H is

    R(H)-R(F) <= mu(H),

whose failure is exactly mu(F)<0. Such a failure also survives compression,
including the actual canonical hull. No negative example is lost by choosing
the representative above. At fixed n only finitely many orientations,
integer dimensions and placements within this box remain. The statement
does not supply a bound on n, exclude all those configurations, or replace
the missing general compensation proof by finite enumeration.

The existing connected nine-source reserve-loss family remains consistent:
at k70 the full reserve stays 24 through 27 compressions in the first image,
while its occupied spans shrink to 43 by 22. Its demand and canonical hull
are retained, with the hull still exactly owners V1,V2,V3,V4. The complete
family and hull have the following independently computed values:

| Quantity, k70 first image | Before | After |
|---|---:|---:|
| R(full) | 24 | 24 |
| R(canonical hull) | 48 | 21 |
| mu(full) | 23 | 23 |
| mu(canonical hull) | 47 | 20 |
| R(hull)-R(full) | 24 | -3 |
| Signed loss minus initial hull margin | -23 | -23 |

Thus compression need not preserve the sign of the failed reserve comparison;
it preserves the actual owner hull and the relevant counterexample direction
for FULL margin. In this example the apparent reserve loss and its available
initial margin decrease by exactly the same amount. Long geometric parameters
alone are therefore not the final obstruction; irreducible interactions
between feature bands remain.

## 8. Verification scope

`develop/check_periodic_slab_compression.py` reconstructs every shortened U
from its exact independent coordinate constructor and regenerates its
matching. It checks owner-coloured seam periodicity, identical nontrivial
Horn clause keys, complete feasibility, actual side indicators, unchanged
A/U0/Z0, transported local defects and exact equation (2). All 32 phases
and isometries are included, with asymmetric long legs and bars. Final
retained subsets are exhaustive through nine owners and deterministic
seed-hull samples above nine. These checks supplement the general proof.
The current receipt covers 800 images, 6,480 compression steps, 1,680 steps
with strictly falling reserve, and 18,488 legal restriction controls.

`formal/SubQuorum/PeriodicStripCompression.lean` formalizes exact occupied-
degree preservation at the seam and its selected-feasibility/endpoint-degree
consequences, under explicit two-row occupancy equalities. The catalogue
construction, reverse Horn-clause transport, feature bound, marked-side
adapter, defect identity application and iteration remain written proofs.
Compilation/axiom status is recorded separately. No end-to-end Lean claim
for this reduction or the full allocation problem is made.
The three seam lemmas compile and pass axiom audit using only propext and
Quot.sound. The independent written-proof review is pending, separately
from the already accepted correction to the earlier single-source separator
note. See `output/periodic-strip-compression-formal-check.json` and
`output/periodic-strip-compression-review.json` for exact scope and handles.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
