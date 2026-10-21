# Forced escape pairs and their shared-band correction

Subsequent disposition: `ALL_WIDTH_NESTED_SEED_NONEXTENSION.md` excludes
complete extensions of this seed for every even width. The selected
partial-inventory identities remain exact, but cannot improve a global
bound through complete extensions of this now-excluded family.

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Assumptions and conclusions

Use precisely the complete full-even-U/standard-rotor original-source model
and immutable endpoint/support/matching inventories of
`WIDE_GATE_ROTOR_COMPENSATION.md`. In particular, an original support with
two or more retained endpoint neighbours must be consumed by an original
in a complete extension, and endpoints of different originals are disjoint.
No assertion that every grid configuration has this source decomposition
is used or proved here. Physical tiles have even top-left coordinates.

Retain the negative outer A=U(W+2,D,F), chart(r,c-1), and positive originals
B_i=U(W,4,4), chart(a+8i+r,c), 0<=i<n. Let W>=8 and a>=2 be even, n>=2,
and D,F be even and at least a+8(n-1)+4. Put g=n-1, a_i=a+8i.

Any complete extension in this model must satisfy all of the following.

1. All 2g gate rotors from the preceding theorem have the upper record.
   The retained originals plus these owners have exact Phi=5g.
2. Each gap forces two further distinct originals, both rotated full U's
   of breadth6. On each side their near/far depths k,f obey

       k,f even, 6<=k, 4<=f<=k-2.

   In the same gap their near depths satisfy k_L+k_R<=W-4. Consequently
   W>=16: none of the retained families at W=8,10,12,14 has a complete
   extension. The preceding three-original theorem handles W=6.
3. Select these 2g actual U owners together with the retained originals
   and 2g upper gate rotors. If t gaps have k_L+k_R=W-4, then exactly

       Phi(selected)=13g-6t >=7g.                            (1)

The last assertion is a selected-inventory identity. It neither asserts
existence of any complete extension nor bounds the marginal of arbitrary
additional originals. In particular, further forced supports remain.

## Excluding every lower gate rotor

Normalize a_i=0 on the left. The lower rotor has original support z=(7,1).
Its west neighbour (7,0) is on A, east neighbour (7,2) on that rotor,
and south neighbour (8,1) on B_(i+1). Thus z must be occupied and only
north is available within its new owner's endpoint graph. Every vertex
of a full U or standard rotor has at least one internal endpoint neighbour;
only a north terminal can have its entire neighbour set in that singleton.

A full U north terminal has continuous stem of even depth>=4. Its third
northward step is (4,1), on B_i. The standard rotor has exactly two
north-terminal records at z. Their endpoint sets are

    {(4,0),(5,0),(5,1),(5,2),(6,-1),(6,0),(6,1),(7,1)},
    {(4,2),(5,0),(5,1),(5,2),(6,1),(6,2),(6,3),(7,1)}.

Both contain (5,0), on A. No owner can occupy z, a contradiction.
Reflection gives the right-side exclusion. The upper records are
therefore forced, and the previous identity3g+u becomes5g.
The longer wall hypothesis in this note guarantees the row7 wall point
for every gap; no absent wall endpoint is presumed.

## Classifying the next owners without a size cutoff

The upper left rotor has original support x=(2,2). Its north neighbour
(1,2) is on B_i, west neighbour (2,1) on B_i, and south neighbour (3,2)
on the rotor. Therefore x must be consumed, with only east available
inside its owner's endpoint graph. Only an east terminal can fit.

The two standard east-terminal rotor records at x contain, respectively,
(0,3) and (1,4), both on B_i. Thus its owner is a full U. Let k>=4
be its even near depth. Its near stem starts at (2,2), heading east.
The retained opposite wall and B_i's opposite stem imply k<=W-4:
k>=W reaches columnW+1, while k=W-2 reaches B_i at columnW.
An upward perpendicular bar intersects B_i at row1. A downward bar
with even breadth>=8 intersects B_(i+1) at row8. Breadth must be6.
At k=W-4, its outer bar is columnW-2 and contains (4,W-2), on the
right upper rotor. Hence in fact k<=W-6.

The surviving full record is, in canonical coordinates,

    U(6,k,f), chart(r,c)=(1+c,2+k-r).                       (2)

Its near stem is row2, columns2..k+2; outer bar is columnk+2,
rows2..7; inner bar is columnk+1, rows3..6; far stem is row7,
columnsk+2-f..k+2. These describe its entire endpoint set. The matching
and supports are the images of the canonical original, not reassigned
after joining it to other originals. The right owner is its reflection.

If f>=k+2, the far stem hits A at (7,0). Thus f<=k. If f=k, its
original far axial support is again z=(7,1), with west neighbour on A,
east neighbour on this U, and south neighbour on B_(i+1). The same
north-only argument just proved excludes every owner of z. Therefore
f<=k-2. Since f>=4, this also proves k>=6. All statements above concern
arbitrary dimensions; finite source catalogues are not used as proof.

The two forced points x_L=(2,2) and x_R=(2,W-1) have different owners.
Both would have to be terminals, but a breadth6 vertical-bar U's two
terminals lie in rows differing by5, whereas these points share a row.
Owners in different gaps are also distinct because their entire
endpoint row spans have length5 and the forced rows differ by8 or more.
These owners differ from retained U's and rotors since their forced
points were absent from those endpoints.

The near stems are the intervals [2,k_L+2] and [W-1-k_R,W-1] in row2.
They must be disjoint, so k_L+k_R<=W-4. Conversely, this inequality
separates the entire endpoint column intervals of the two records.
Since both k's are at least6, W>=16 follows. It also implies

    k_L,k_R<=W-10,                                       (3)

which will remove a possible event with the opposite rotor.

## Exact charges and the single-owner boundary exception

For (2), put h=(k+f)/2. Matching edges, endpoint tiles and original
supports inside those tiles have respective counts

    5+h, 4+h, h-2.

Thus its charge is (5+h)+(h-2)-2(4+h)=-5, contributing5 to N+S.
Its immutable supports are exactly

    row1: even columns2..k+2;
    row8: even columnsk+2-f..k+2;
    (2,1), (7,k+1-f);
    row3: odd columns3..k-1;
    row6: odd columnsk+3-f..k-1.

For f<=k-2 and k<=W-6, this U creates no full mixed tile with the old
originals or the two upper rotors. It creates the event

    U:(2,2) -> upperRotor:(3,2).

The reverse direction is excluded by the rotor's original support x.
There is one exception to the claim that this is the only event: when
k=W-6, the outer bar at columnW-4 creates additionally

    U:(4,W-4) -> rightUpperRotor:(4,W-3).

The reverse direction targets the rotor's immutable support and remains
excluded. Listing (2) against the two rotor records and retained bars
exhausts all intratile adjacencies. The exact single-owner gain is

    4 - [k=W-6].                                        (4)

For example, W=16,k=10,f=4 has gain3, refuting the unrestricted
single-owner gain4 rule. Its endpoints and original supports are supplied
by (2), so this is directly reproducible. It is a counterexample to that
rule, not to (1): no right forced owner can coexist with k_L=10 at W=16.
By (3), every actual selected pair avoids this boundary exception.

## Cooperative tiles and events when the two U's touch

For an actual selected pair, each U individually gains4 against the
same retained-plus-upper-rotor baseline. If k_L+k_R<W-4, even parity
puts the nearest outer-bar columns at coordinate difference at least three.
Their physical tile footprints are disjoint, so the joint gain is8.

If k_L+k_R=W-4, put C=k_L+2, an even column. The two outer bars are
columnsC,C+1 for all six rows2..7. They create exactly three full mixed
tiles, with top-left points (2,C),(4,C),(6,C), and exactly twelve
source-labelled directed events: both directions between the bars in
each of the six rows. Neither direction targets the originating U's
support: all supports of the left U have column<=C, and reflection
gives the corresponding bound for the right U. These three tiles were
not full in either single-U inventory. There are no other common tiles
or cross events because each U lies wholly on its own side of this
boundary. The pair correction is therefore2*3-12=-6, and its joint
gain is8-6=2. Counting8 for such a pair would use the same contact band
twice without charging its events.

## Simultaneous counting across all gaps

Translate the preceding receipts by a_i. Every new U endpoint lies
in rows[a_i+2,a_i+7]. Different gaps have disjoint physical tile rows.
Each cooperative tile belongs to exactly one gap and one opposite
pair; every directed event retains its source label. There is no event
or tile shared across gaps. The additional U's cannot alter old/old
events because the old supports are immutable. Consequently their total
gain in the common retained-plus-rotor baseline is8g-6t. Combining with
the already established5g proves (1). Since0<=t<=g, (1) gives7g.
The W=16,k_L=k_R=6,f_L=f_R=4 records attain7g as partial inventories.
No complete extension of those equality records is asserted.

## Verification and remaining scope

Run `PYTHONDONTWRITEBYTECODE=1 python3 develop/check_wide_gate_escape_compensation.py`.
The checker reconstructs endpoint/support/matching originals, including
the canonical-to-formal endpoint/support adapters and the three charge
counts. It verifies north-only exclusions, east-terminal normalization,
the extra single-owner boundary event, exact opposite-pair full-tile and
source-event sets, simultaneous multi-gap partitions, even translations
and large dimensions. These are discovery and validation controls for
the written all-parameter proof, not a finite-search proof of it.

`formal/SubQuorum/WideGateEscapeCompensation.lean` checks local normalized
geometry, near-depth and width frontiers, endpoint separation, actual-pair
avoidance of the exceptional opposite rotor, tight-band endpoint presence
and absence of original supports, tile-row separation, charge and joint
budget arithmetic. Completeness/role adapters and exhaustion of the exact
inventory partition remain written arguments. No global formal theorem
or whole-source-model formalization is claimed.

The completed controls are4644 north-gate U roles,392 rotor roles,1800
east-terminal U roles with31 normalized survivor records,114 single-U
inventories including29 exceptional boundary debits,421 pair inventories
including170 tight pairs, and38 multi-gap/large controls. The local Lean
file before the addendum below has22 explicit declarations and17 theorems; run30420 exit0
has no warnings or sorry/native axioms, with each declaration audited.
Execution used the user-selected local Mac after44% free-memory and
comm-basename process checks confirmed no active Lean/lake invocation.

Independent review task4ea2ca1d-03f9-4e8c-9e82-383e2a72f7a2 completed
with ACCEPT on original stream15686 exit0, conversationconv_ed4025a182e9f9d9.
Its19396-character stream/terminal match and gpt6/pro identity are verified.
The self-contained packet includes both wide-gate proofs, full constructors
and immutable inventory definitions. It does not include the subsequent
far-offset addendum or all-width closure. The older contact-ledger
and width-six three-original obstruction review completed with ACCEPT;
its11448-character original stream exactly matches its terminal receipt.

The next problem is to classify owners of the far axial supports of
these rotated U's and incorporate all subsequent contributions without
reusing the current positive budget. General full-family allocation,
the global5/6 improvement and rectangular-grid triple equality remain open.

## Post-submission addendum: the shortest far offset is impossible

The following deduction was made after the independent-review packet was
submitted and is not part of task4ea2ca1d's initial scope.

In a complete extension, the stronger necessary conditions are

    f<=k-4, k>=8 on both sides, and W>=20.                  (5)

To prove this, normalize a_i=0 on the left and suppose f=k-2. The
escape U's original far axial support is z'=(7,3). Its north neighbour
(6,3) belongs to the upper rotor, east neighbour (7,4) to this escape,
and south neighbour (8,3) to B_(i+1). It must be occupied, with only
west available internally. Thus every U/rotor owner is a west terminal.
A U's minimum depth4 contains (7,0) after three steps, hitting A.
The two standard west-terminal rotor endpoint sets are

    {(6,1),(7,1),(7,2),(7,3),(8,0),(8,1),(8,2),(9,2)},
    {(5,2),(6,0),(6,1),(6,2),(7,1),(7,2),(7,3),(8,1)}.

Both contain (8,1), on B_(i+1). No owner exists, a contradiction.
Reflection proves the right exclusion. Combining f!=k-2 with the even
parity and prior f<=k-2 yields f<=k-4. Then f>=4 implies k>=8;
k_L+k_R<=W-4 implies W>=20. Thus W=16 and18 are excluded as complete
extensions too. The7g identity for selected inventories is unchanged.

The checker adds23 full-source controls, excluding2484 U roles and184
rotor roles at the new forced support. Final Python run42722 exits0
with all earlier receipt controls still passing. Three additional local
Lean theorems formalize the west-terminal collision, even-parity gap and
new width frontier. Final Lean run6021 exits0 with25 declarations/20
theorems individually audited, no warnings/sorry/native; preflight43%
free memory and no real Lean/lake process. The role adapters remain
written. The next open far-offset case has f<=k-4; it is not excluded
by the west-only argument just given.
