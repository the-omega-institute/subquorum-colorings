# Wide-gate forced-rotor compensation

Subsequent disposition: `ALL_WIDTH_NESTED_SEED_NONEXTENSION.md` excludes
complete extensions of this nested seed at every even width. The partial
inventory identities here remain exact; their complete-extension owner
implications do not supply a bound for a realizable complete family.

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Statement and scope

Use the full-U/standard-rotor original-source model, immutable original
supports and matching, physical tiles with even top-left coordinates, and
the source-labelled event inventory of `EVEN_BAR_CONTACT_LEDGER_AND_TWO_GATES.md`.
Write Phi=N+S+2F-E. A complete extension must consume any original support
that has at least two retained endpoint neighbours. All endpoint sets of
different originals are disjoint. Completeness and this source model are
explicit hypotheses, not a classification of arbitrary grid configurations.

Let W>=8, n>=2 and a>=2 be even except that n is arbitrary. Retain

    A=U(W+2,D,F), chart(r,c-1),
    B_i=U(W,4,4), chart(a+8i+r,c), 0<=i<n,

where D,F are even and at least a+8(n-1)+4. The walls of A are columns
0 and W+1. Put g=n-1 and a_i=a+8i. The retained inventory has Phi=-g:
each of the n positive B_i has two contact bands with the negative A.

In any complete extension by full even U originals and standard rotors
in arbitrary lattice orientations, the 2g original supports

    p_i=(a_i+5,1), q_i=(a_i+5,W), 0<=i<g,

belong to 2g distinct rotor originals. Each has exactly one of the two
records described below, or its reflection at the right gate. Select
these owners together with A and all B_i; other extension originals are
not included in this selected inventory. If u selected owners have the
upper record, then exactly

    Phi(selected)=3g+u >=3g.                                (1)

Equivalently, adding these forced owners to the retained inventory gains
4g+u. This is an all-parameter simultaneous compensation identity for
the selected inventory. It asserts neither existence of a complete
extension nor nonnegative marginal under arbitrary further originals.

## Why only rotors can own the gates

At p_i the north neighbour belongs to B_i and the west neighbour belongs
to A. Thus p_i must be occupied, and only east and south directions are
available within its owner's endpoint graph. In a full U, a degree-three
branch point needs three directions, and a straight stem point needs
opposite directions. Its only possible roles are an east/south outer
corner or an east or south terminal.

An east/south corner has either a south-going stem of depth at least4
or a south-going bar of breadth at least6. Either contains (a_i+8,1),
on B_(i+1). A south terminal also contains this point. For an east
terminal of even depth k>=4, its continuous stem runs from column1 to
column1+k. If k>=W it hits A at columnW+1. If k<W, its perpendicular
bar is in column1+k within [1,W]. An upward bar of breadth at least6
reaches rowa_i; a downward bar reaches rowa_i+8. Both hit retained bars.
This excludes every full U at p_i without any dimension cutoff.

The standard rotor's endpoint graph has degrees one or three. With only
east/south available, its owner must therefore be an east or south terminal.
Inspection under the eight lattice isometries excludes its south-terminal
roles by wall or next-bar collisions. The two surviving east-terminal records are listed
in full below. This is a check of the fixed rotor's finite role list;
no bounded U search supplies the preceding all-depth argument.
The right-gate argument is the reflection c -> W+1-c.

All gates have different owners. A rotor has column-coordinate diameter
three and occupies at most four columns,
whereas opposite gates differ by W-1>=7. Its row span is at most four,
whereas gates in different gaps differ by at least eight rows. Full U
owners have already been excluded separately at every gate.

## Exact canonical records

Subtract a_i from all rows. A record contains endpoint set T, immutable
support set H and matching M. The upper left record is

    T_up={(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)};
    H_up={(2,2),(3,1),(3,4),(4,5),(5,0),(6,1),(6,4),(7,3)};
    M_up={[(3,2),(4,2)],[(4,3),(4,4)],
          [(5,1),(5,2)],[(5,3),(6,3)]}.

The lower left record is

    T_down={(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)};
    H_down={(3,3),(4,1),(4,4),(5,0),(6,5),(7,1),(7,4),(8,2)};
    M_down={[(4,3),(5,3)],[(5,1),(5,2)],
            [(6,2),(7,2)],[(6,3),(6,4)]}.

Reflect all three parts for the right records. Since W+1 is odd, the
reflection preserves physical tiles. Charges of upper and lower records
are respectively -2 and0 on either side. Thus their contributions to
N+S are respectively2 and0. Listing supports as well as endpoints is
essential: event directions targeting original supports remain excluded
after another original consumes the support.

## Receipt partition and nonreuse proof

Each rotor creates exactly one new mixed full tile. Its top-left point
is (a_i+4,0) on the left and (a_i+4,W) on the right. It has three owners:
A supplies its outside column, B_i its inside top cell and the rotor
its inside bottom cell. Each upper rotor creates exactly one event,
from its gate (a_i+5,1) to B_i at (a_i+4,1), or the reflected event.
Each lower rotor creates none. The reverse direction from B_i targets
its own original axial support and is excluded. The wall direction is
also excluded by the wall's original lateral support. Directly listing
the above endpoint/support records against the retained bars and walls
exhausts the old/new intratile adjacencies. There is no other new full
tile on either side. Therefore an upper rotor gains2+2-1=3 and a lower
rotor gains0+2-0=2.

For W>=10 the opposite rotor footprints have disjoint tile columns.
For W=8 the only possible shared tile column has physical columns4,5.
An upper rotor can meet it only in rowa_i+4; a lower rotor only in
rowa_i+6. If opposite modes differ, they do not share a tile. If modes
agree, the shared tile contains only its two upper cells. Neither a
retained original nor these rotors fills its lower cells. Both possible
horizontal cross directions target immutable rotor supports, as the
records show. Thus even W=8 introduces no cross event or extra full tile.

Every new rotor endpoint lies in rows[a_i+3,a_i+7]. The corresponding
physical tile rows in different gaps are disjoint, since a_(i+1)=a_i+8.
The newly created gate tiles are distinct on opposite sides and in
different gaps. Their source-labelled event sets are also disjoint.
Old/old events cannot change: their endpoints and their originating
source's immutable supports have not changed. Consequently all rotor
gains add in the same retained baseline. There are 2g rotors, so their
total gain is4g+u. Adding the retained Phi=-g proves (1).

The lower-only choices attain3g as selected partial inventories. This
does not establish sharpness within complete extensions. In particular,
further forced-support tests can rule out some selected choices, and
adding other originals can create additional negative cross events.

## Validation and formal scope

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_wide_gate_rotor_compensation.py

The verifier reconstructs original endpoint/support/matching records,
checks2592 U roles and128 rotor roles at W=6,8,10,20, and checks1360
complete full-tile and source-labelled-event inventories over all upper/
lower assignments for n=2..5, W=8,12 and two even translations.
There are16 lower-only equality cases and four additional controls up
to W=2000, n=12 and large translations/depths. These finite controls
test the written proof and do not replace its all-parameter argument.

`formal/SubQuorum/WideGateRotorCompensation.lean` has15 explicit
declarations, including9 local theorems: all-depth east-terminal
collision, rotor endpoint bounds, opposite endpoint disjointness,
excluded middle directions at W=8, different-gap tile-row separation,
gate-tile injection and budget arithmetic. Lean4.33.0 verifies all15
declarations with individual axiom audits, no warnings and no sorry or
native evaluation. Source-role completeness, the complete-extension
adapter and the exact inventory partition above remain written proofs.
The entire original-source model is not claimed fully formalized.

Independent review of this result and the subsequent escape-pair theorem
completed with ACCEPT as task4ea2ca1d-03f9-4e8c-9e82-383e2a72f7a2,
conversationconv_ed4025a182e9f9d9, original stream15686 exit0. Its19396
characters match the terminal receipt exactly; the review checks written
proofs and does not independently execute code/Lean. Two coordinate-wording
corrections have been applied. The later far-offset exclusion and all-width
closure were outside that packet.
The predecessor contact-ledger review completed with ACCEPT on its original
stream25032, with an exact11448-character stream/terminal match. That
request does not contain this result; its receipt is
`output/even-bar-contact-ledger-review-terminal.json`.

## Next question

For a lower left rotor, its original support (a_i+7,1) has retained
west/east/south neighbours. For an upper left rotor, (a_i+2,2) has
retained north/west/south neighbours. These are different next-owner
constraints and should be studied before claiming complete-family
sharpness. Rotated U receivers and their possible mutual contact bands
must be charged in one joint inventory. The global5/6 improvement,
general full-family allocation and rectangular-grid triple equality
remain open.
