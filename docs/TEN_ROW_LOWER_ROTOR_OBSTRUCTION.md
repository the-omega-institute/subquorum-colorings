# A three-original obstruction and the stronger spacing-ten budget

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Statement and source model

Use the same complete full-even-U/standard-rotor source model as
`TEN_ROW_GATE_OWNER_COMPENSATION.md`. U breadths are even and at least6;
depths are even and at least4. All orientations are allowed. Distinct
endpoint sets are disjoint. Original supports and matchings are immutable.
An original support that remains outside the endpoint union has exactly
one occupied neighbour in a complete extension. No universal source
decomposition for arbitrary rectangular grids is asserted.

Fix even W>=6 and even a>=2. Retain only:

    A=U(W+2,D,F), chart(r,c-1), even D,F>=a+14;
    C=U(W,4,4), chart(a+10+r,c);
    L=the lower east-terminal rotor at (a+5,1).             (1)

There is no complete extension containing (1), even with arbitrary
additional retained originals and arbitrary orientations of new originals.
The earlier inner source B at rowa is not needed for this obstruction.

Consequently, in the spacing-ten family of the preceding note, neither
gate can have a lower-rotor actual owner. The per-gap joint marginal
improves from J>=4 to

    J>=5 for EVERY even W>=6.                              (2)

For n>=2 coextensive U(W,4,4) originals inside one outer U, at even
bar rows a+10i and with walls covering every tip, selecting the actual
owners of both axial gates at each gap, counting a shared owner once,
therefore gives

    Phi(selected)=1-n+sum J_i >=4(n-1).                    (3)

The result still concerns precisely this selected inventory, not an
arbitrary extra old baseline or the entire extension. It does not prove
that a complete extension exists or that unselected actual sources have
nonnegative total marginal. The global5/6 improvement and rectangular-grid
triple equality remain open.

## A short vertical interval cannot contain a full stem

The elementary geometric fact used below is unbounded in all U dimensions.
Suppose an original owns z=(7,1), and the only internal endpoint directions
available there are north and south. Every permitted U realizes z as a
vertical terminal or a vertical straight-stem point: an outer bar corner
requires perpendicular directions, and all other bar/branch points have
degree three. Thus z lies on a whole vertical stem, whose endpoints have
row coordinates l,h, with

    l<=7<=h, h-l>=4,

and every (row,1), l<=row<=h is that original's endpoint.

Such a stem must contain either (5,1) or (10,1). If l<=5, the former
lies between l and h because h>=7. If l>5, integer l>=6 and h>=l+4>=10;
since l<=7, the latter lies between l and h. Equivalently, the open
interval between the two forbidden rows5 and10 has just four lattice
points6,7,8,9, whereas a depth-at-least-four stem has at least five.
This proof also covers a straight-stem role arbitrarily far from its bar;
it does not presume z is a terminal or bound a source's dimensions.

## The lower rotor leaves precisely this impossible gate

Subtract a from rows. The lower rotor has endpoint record

    L={(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)}.

Its original support is z=(7,1). To check its provenance directly,
take the canonical rotor chart (r,c)->(3+r,5-c). The canonical
support (4,4) maps to z; the canonical endpoint (4,3) maps to (7,2),
and the canonical endpoint (2,4) maps to (5,1). The same chart carries
the original matching. Nothing is added to or reassigned in H or M.

The point z is absent from A,C,L endpoints. Its west neighbour (7,0)
is on A's wall and its east neighbour (7,2) is on L. Completeness
therefore forces a different original to own z, with only north/south
available internally. The retained endpoint (5,1) is on L, while
(10,1) is on C. The vertical-interval argument excludes every U owner.

Every rotor at z must be a north or south terminal. For a south terminal,
the two full endpoint records have offsets from z

    S_1={(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)},
    S_2={(0,0),(1,-2),(1,-1),(1,0),(2,-1),(2,0),(2,1),(3,-1)}.

Both contain z+(2,-1)=(9,0), on A. Reflecting row about z gives the
two north-terminal records, both containing z+(-2,-1)=(5,0), on A.
These four records exhaust all orientations after fixing the terminal
and its internal direction. Thus no rotor can own z either.

The forced original support z has no owner, a contradiction. Every wall
point used lies in normalized rows5,7,9 and is retained under the stated
depth bound. An additional retained original that already consumes z is
itself an owner in the exhaustive classification and is excluded by the
same argument. Additional occupied neighbours only narrow its available
directions. This proves the three-original theorem. Whole-configuration
reflection gives the right-gate exclusion, and arbitrary lattice isometries
give the corresponding transformed obstructions.

## Improving the simultaneous bound without a second use of surplus

The preceding note classifies a left gate owner as D_b,U_b,V_b,H or L.
Delete L by the new obstruction. A single owner consuming both gates
is still D_W or U_W, with exact joint marginal W+1 or5; both are at
least5. For distinct owners:

- Two U types each have single marginal at least3 and new/new correction0.
- Two H rotors each have single marginal3 and correction0.
- H with D or U has correction0 and single marginals at least3+3.
- H with V has correction-1 and single marginals3+3, giving exactly5
  when the pair is tight; at separation the correction is0.

Hence (2) holds in every case. This uses the OLD exact receipt table;
no additional credit is assigned to the missing support, the wall, or
the exclusion proof. Source/tile/event separation across different gaps
is unchanged. Summing the same per-gap receipts against the same retained
baseline Phi=1-n proves (3), without double counting a spanning owner or
charging the former lower rotor's unused surplus a second time.

All full-width U_W choices attain J=5 and Phi=4(n-1) as partial
inventories. This does not assert complete-family sharpness. In particular,
the preceding two-L partial inventories still attain J=4, but the new
three-original theorem proves that none of them can completely extend.
The earlier J>=4 statement remains correct; its partial equality was never
a complete-extension witness.

## Nonuniform spacing and a density criterion

The same argument applies to a nonuniform sequence of even bar rows
a_0<...<a_(n-1), a_0>=2, with every successive gap at least10 and the
outer walls covering all tips. Let m be the number of gaps equal to10.
Select actual gate owners ONLY at those m gaps, counting any spanning
owner once. The even-bar contact ledger still gives old Phi=1-n: each
inner positive U has precisely its two outer-wall contact bands, and
different inner originals have disjoint tile-row intervals. Each selected
gap has its same two bounding bars at relative rows0 and10, so the proof
above gives J>=5 there. Owner windows from different selected gaps remain
separated by at least10 rows, with no new cross-gap tile or event.
Consequently the exact inventory and its general lower bound are

    Phi(selected)=1-n+sum_(selected gaps) J_i >=5m-(n-1).   (4)

In particular, if 5m>=n-1, these actual selected owners suffice to make
this baseline inventory nonnegative. This criterion spends each selected
gap's receipt once, even when several unselected wider gaps lie between.
It does not make an assertion about the unknown owners at those wider
gaps or about the final complete-family budget. With six inner sources
and gaps10,12,12,12,12, taking one spanning U_W at the ten-row gap gives
the exact PARTIAL value0, illustrating the threshold without claiming
complete-extension feasibility. Equation (3) is the case m=n-1.

### An explicit unbounded residual from wider gaps

For any integer r>=0, retain inner U(W,4,4) originals at rows

    a, a+10, a+22, ..., a+10+12r,

inside an outer U whose even depths cover every tip. Add just the one
spanning U_W owner with chart(x,y)=(a+9-x,y) at the first gap. These
are full immutable records with disjoint endpoints. There is one ten-row
gap and r twelve-row gaps. The old even-bar ledger is -(r+1), and the
spanning owner adds exactly5, without meeting any of the r later sources.
Hence the exact partial-inventory formula is

    Phi=4-r.                                               (5)

Every added twelve-row-spaced positive U contributes exactly-1 through
its two contacts with the retained outer walls. Thus even a compensated
core with Phi=4 can have arbitrarily negative endpoint-disjoint extensions.
The first negative example has r=5 and Phi=-1. This refutes the proposed
inference that the compensated core remains nonnegative under arbitrary
additional endpoint-disjoint sources. It does NOT refute the target
complete-family inequality: no complete extension of these partial
inventories is asserted. In a complete extension, the newly forced gates
at the twelve-row gaps must also be handled. Those gates, rather than
further compensation layers on the excluded lower rotor, are the next
unresolved family. This formula is also an exact partial sharpness example
for the density criterion, not a complete-family sharpness claim.

## Verification and independent-review scope

The companion Python verifier checks the complete immutable L support and
matching chart, every sampled U orientation/endpoint role at z, all four
vertical terminal rotor records, reflection and even translation controls,
the exact stronger joint receipts and mixed multi-gap selected inventories.
The unbounded stem proof and source-role exhaustion are written above;
bounded exclusions do not replace that proof. The companion Lean file
formalizes the arbitrary-length interval collision, all four rotor wall
collisions, removal of L from the joint arithmetic, and the simultaneous
4(n-1) bound. Complete source-to-role/support assembly remains written.

This obstruction and improved bound were found AFTER the spacing-ten
review request (original stream71332) was submitted. They are outside that
request's initial packet; that pending review is not claimed to cover them.
The previous all-width spacing-eight proof has independently received ACCEPT.

Final Python40515 exited0:64 transformed three-source cases excluded475136
U and1024 rotor roles, plus7424 U/16 rotor roles at width2000. All824
compatible pairs without L satisfy J>=5;384 mixed uniform batches and64
shared-spanning partial equality cases passed. Nonuniform controls passed832
cases,560 satisfying the density criterion, including16 exact neutral cases.
The24 residual controls at r=0,1,4,5,20,40 agree exactly with4-r.

Final local Lean4.33.0 process57168 exited0:20 explicit declarations and12
local theorems individually audited, ordinary axioms only, without warnings,
sorry or native reduction. Preflight45% memory free and comm-basename
inspection found no active Lean/lake process. The preceding check75747
already passed the initial obstruction and uniform bound before the two
nonuniform arithmetic theorems were added. No whole-model formalization or
independent-review acceptance is inferred from these scoped local checks.

## Subsequent all-even-gap compensation

`ALL_EVEN_GAP_AXIAL_COMPENSATION.md` now classifies the actual left axial
owner for EVERY even gap>=10 into four U families and H/L. Every such
owner has exact marginal>=2. This supplies the missing selected owners
at wider gaps: the general mixed selected bound is g+3m, with g gaps and
m gaps10, without the earlier density condition. The exact partial4-r
family above is necessarily supplemented in any complete extension by
r distinct left owners, yielding selectedPhi>=4+r. The old partial4-r
calculation and failure of arbitrary endpoint-only monotonicity remain
valid; neither the old nor the augmented partial family asserts complete
existence or a whole-family bound. Unselected actual-source signed terms
are the next frontier. The new theorem is outside original71332's packet.

Original71332 has subsequently completed ACCEPT for its original
spacing-ten classification and gap6/minimum10 packet:18842 characters,
exact original-stream/terminal match, observed gpt_6/pro. That acceptance
does not cover this lower-L obstruction. The distinct general-gap
review11740 has now completed ACCEPT,20944 characters exactly matching
the terminal API, observed gpt_6/pro. It directly verifies this lower-L
obstruction, the stronger gap10 joint bound and the all-even-gap theorem.
It does not cover later sealed-chamber localization or R/Z/N repair.
