# Ceiling descent excludes boundary horizontal U and isolates interior H

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and conclusions

Work in the established six-row chamber pocket

    P=[0,5] x [0,N-1],

with its occupied old endpoint boundary and no old endpoints inside P.
Every new original is a full
canonical even U or standard rotor, wholly confined to P. Their endpoint
sets are pairwise disjoint; their nearest-neighbour endpoint graphs are
connected. All original supports not consumed by actual endpoints remain
occupied, and every retained support in P has exactly one occupied
neighbour. The full-U/rotor decomposition is an explicit assumption, not
a claim about every possible grid configuration.

A horizontal U has width B>=6 even, both depths4, projection I=[L,R],
R=L+B-1, and one of four outer-bar rows:

| Type | Outer/inner bar rows | Leg endpoints extend to |
|---|---|---|
| H0, Down boundary | 0,1 | row4 |
| H1, Down interior | 1,2 | row5 |
| H4, Up interior | 4,3 | row0 |
| H5, Up boundary | 5,4 | row1 |

A transverse V is U(6,d,f), arbitrary even depths>=4, with a full-height
two-column bar and horizontal stems on rows0,5. No phase or alignment
restriction is made on any horizontal projection in the geometric claims.

The following statements hold for every complete pocket in this model:

1. H0 and H5 cannot occur.
2. No V endpoint occurs anywhere over the projection of an H1 or H4.
3. No endpoint of any other original, including a rotor, occurs over an
   H1 or H4 projection.
4. Consequently, if the surviving horizontal projections all start at
   even L, they peel off the exact inventory with no contact correction:

       Phi(all)=Phi(V union rotors)+sum_H(B_H-1).           (1)

Here the full-model inventory is

    q_i=M_i-2T_i+S_i,
    Phi(Y)=number(q_i>0)+sum_i max(0,-q_i)+2J(Y)-K(Y),

using the immutable original-support event predicate and the established
canonical counts. The positive-source term matters when rotors are
allowed. Every aligned interior H has charge1-B, so contributes B-1.

In particular, when there are NO rotors and all H are tile-aligned,

    Phi(all)=Phi(V)+sum_H(B_H-1)
            >= a+2b+sum_H(B_H-1),                         (2)

where a,b count even/odd V bars. This sharpens the earlier complete H
marginal lower bound B/2-2 to the exact B-1. A pocket with at least one
H has Phi>=5; its whole chamber increment is at least10. Nonempty
transverse-only pockets still have sharp Phi>=2 and chamber increment7.
With rotors present, (1) makes no claim about the sign of its residual
V/rotor inventory.

## All strip types and a corner-receiver lemma

The canonical full U(B,d,f) has horizontal breadth B and vertical
endpoint span max(d,f)+1 before transposition. Because B>=6 and d,f>=4
are even, confinement to six rows leaves exactly two possibilities.
Without transposition, d=f=4, and the outer bar is on row0,1,4 or5 as
listed above. After transposition, B=6 and its bar fills all six rows;
its stem depths remain arbitrary. A rotor has span4 rows and4 columns.
Thus the listed horizontal types, V, and rotors exhaust this ASSUMED
source model without bounding any horizontal width or V depth.

Every horizontal source has a full interior bar row1 or4, and both
side columns contain all rows1..4. Ordering projection left ends shows
that two horizontal projections cannot overlap: the later left side
would meet the earlier full interior bar row. A V bar cannot intersect
a horizontal projection for the same reason.

Call H0 and H4 north sources. Both have a full side column at L on
rows0..4, endpoints at (0,L),(4,L), and original support (4,L-1).
These facts follow directly from the canonical supports: H0 uses its
outer depth4 leg support, while H4 uses its outer-bar end support.

We need a corner-receiver fact. If a full source lies in a rectangle
with rows0..4 and right boundary column c, and has endpoint (4,c), it
is a north source with right end c. A transverse U cannot fit five
rows. A nontransposed U can fit only with depths4, and since it contains
row4 its outer bar must be0 or4. Its projection ends at c. A rotor
cannot occupy its bounding rectangle's southeast corner. In normalized
coordinates its two possible endpoint shapes are

    A={(0,1),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,2)},
    B={(0,2),(1,0),(1,1),(1,2),(2,1),(2,2),(2,3),(3,1)}.

All eight dihedral images normalize to one of these shapes. Neither
contains (3,3). Equivalently, every rotor endpoint has an endpoint
strictly below it or strictly to its right. It therefore cannot be
the southeast corner of any containing rectangle, regardless of its
translation. This is a finite shape identity, not a finite-width search.

## A V bottom stem cannot enter a north projection

Suppose a right-facing V has bar columns b,b+1, top depth f>=4, and
bottom depth d>=4, and its bottom stem enters a north source A from the
left. Its left end L satisfies

    b+2<=L<=b+d.

Because A owns (0,L), endpoint-disjointness from V's top stem gives

    b+f<L; hence L>=b+5.                                 (3)

Let s=(4,L-1), an original support of A. It has the distinct occupied
neighbours (4,L) from A and (5,L-1) from V. The second point is in V's
bottom stem by (3). The point s is not an endpoint of A or V, and lies
strictly inside the pocket, not on the old boundary. Completeness
therefore forces an actual third original C to own s.

All endpoints of C lie in the rectangle

    Q=[0,4] x [b+2,L-1].                                 (4)

Indeed, the V bar supplies an occupied full-height wall at column b+1.
The north source supplies a wall at column L in rows0..4, completed
by V's bottom endpoint at (5,L). V also occupies all row5 points
between these walls. C cannot intersect either wall or that bottom
row. Its endpoint graph is connected and stays in rows0..5. A
nearest-neighbour endpoint path from s to any point outside (4) would
hit one of those occupied walls or row5. This proves confinement,
including sources of arbitrary widths and depths.

Apply the corner-receiver fact at s, the southeast corner of (4).
C is another north source, with right end L-1 and left end L'. Its
width is at least6, hence

    b+2<=L'<=L-6.                                        (5)

V's bottom stem reaches L' because L'<=L<=b+d. The same argument
therefore applies to C. In particular its own row0 left endpoint
gives b+f<L', and its renewed original support (4,L'-1) must be
consumed by another north source strictly to its left.

This is impossible. Every such left end is an integer at least b+f+1,
but each forced successor decreases it by at least6. One may take the
least left end in this nonempty bounded-below integer set and obtain
a smaller one, or apply well-founded induction to L-(b+f+1). No
distinct source, credit or event is counted repeatedly; the strictly
decreasing coordinate already prevents a cycle.

For a V bar to the right, reflect horizontally and use the symmetric
original support (4,R+1), obtaining a strictly increasing bounded-above
chain. Since a V bar cannot intersect a horizontal projection, any
bottom stem meeting that projection enters from one side. We have
therefore proved

    no V bottom endpoint over any north-source projection. (6)

The proof uses actual retained-support completeness, not a monotone
endpoint-only inventory rule.

## Boundary exclusion and reflected version

An H0 has original support t=(5,L). It has the occupied neighbours
(4,L) from its own leg and (6,L) from the old boundary. Completeness
forces an actual endpoint at t. Any nontransverse full source having
an endpoint on row5 also has its own endpoint immediately above it:
H1 has its leg, H5 has its inner bar, and a rotor's bottom tip has
an upper neighbour, as both explicit shapes show. Such an owner
would collide with H0 at (4,L). H0 and H4 have no row5 endpoints.
Thus the actual owner must be V, and (6) excludes it. No H0 occurs.

Reflection r->5-r preserves the strip, its old occupied boundary,
the full source model and support retention. It maps H0 to H5, H4
to H1, and bottom V stems to top stems. Therefore H5 is also absent,
and V top endpoints cannot occur over H1 projections.

For H1, bottom V stems are already excluded by its own terminal
endpoints at (5,L),(5,R): a stem from either side would hit one of
them. For H4 the analogous exclusion applies to row0. Together with
(6), its reflection, and the bar-projection exclusion, this proves
that no V endpoint occurs anywhere over an interior H projection.

## Rotor separation and exact peeling

Consider H1. Its rows1,2 are full across I, and its side columns
are full from row1 to5. No rotor endpoint can lie on row0 over I:
such an endpoint is a topmost rotor endpoint and has its own endpoint
immediately below, colliding with H1's row1 bar. Any rotor endpoint
in rows3..5 over I must lie strictly between the H side columns.
Its connected endpoint graph is then trapped below the occupied
row2 bar, between the side columns, and above the end of the six-row
strip. It would fit in a rectangle of only three rows, whereas a
rotor has span4. This is impossible. The reflected proof applies to
H4. Other horizontal projections were already proved disjoint.

Thus every interior H projection contains no foreign endpoints.
If L is even, its even width makes I a union of whole physical tile
columns. A foreign endpoint outside I cannot be in any of its tiles.
There are no H/foreign mixed tiles or intratile labelled events.
Remove ALL aligned H sources simultaneously: the remaining V/rotor
inventory is unchanged, and each H contributes only its source mass
B-1. This is the exact nonreusing partition (1), even with arbitrary
V/rotor contacts in the residual family. No residual sign is assumed.
If no rotor remains, use the accepted Phi(V)>=a+2b to obtain (2).

## Verification scope and remaining frontier

`develop/check_six_row_ceiling_descent.py` reconstructs full original
records, checks corner roles, bottom-support owner roles and explicit
partial consumer chains, including width2000. Its finite checks support
the source-shape identities and catch incorrect roles; the confinement
and infinite-descent proofs above have no size cutoff.

`formal/SubQuorum/SixRowCeilingDescent.lean` verifies north side endpoints,
top-stem clearance, the two neighbours of each renewed support, its
exclusion from its current two owners, the six-column descent, both
explicit rotor shapes' upper-neighbour and southeast-corner properties,
and arbitrary bounded integer descent. All16 explicit declarations
including10 local theorems are individually axiom-audited. The final
local Lean4.33.0 run exits0 with only ordinary axioms, no warnings,
sorry or native reduction. Full canonical adapters, source enumeration,
connected-wall confinement, completeness assembly and inventory peeling
remain written; this is not an end-to-end formalization.

This ceiling-descent theorem is distinct from the earlier accepted mixed
debit theorem. Its own task2a3b4f9e-f29d-42dc-aa8e-2901bb8e7f1c returned
ACCEPT, observed gpt_6/pro, with16326 characters archived from the terminal
task API. The original stream27595 ended in transport EOF; the same
dispatched task was recovered from its conversation, not resubmitted.
The reviewer independently checked the unbounded classification,
confinement, descent, boundary exclusion, rotor separation and exact
peeling, including its no-rotor/aligned scope for the chamber>=10
corollary. They did not rerun the Python checker or Lean. The original
review packet's charge transcription error has been explicitly corrected;
the authoritative charge throughout this note is M-2T+S.

The general complete V/rotor residual budget, odd-start H boundary-tile
interactions, arbitrary source decomposition, exterior contribution,
global5/6 improvement and rectangular-grid triple equality remain open.
The submitted manuscript and existing main results are unchanged.
