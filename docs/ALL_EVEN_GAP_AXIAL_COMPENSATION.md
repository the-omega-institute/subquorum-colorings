# An axial-owner compensation theorem for every even gap

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and statement

Work in the explicit full-even-U/standard-rotor model of
`TEN_ROW_GATE_OWNER_COMPENSATION.md`. A U has even breadth at least six and
two even depths at least four; every orientation is allowed. Different
originals have disjoint endpoint sets T, and each original's support H and
matching M remain immutable. In a complete extension a support outside the
endpoint union has exactly one occupied neighbour. No decomposition theorem
for arbitrary grid configurations is assumed or proved here.

Partition the lattice into tiles {2i,2i+1} x {2j,2j+1}. For an inventory K,
let F(K) be its full mixed tiles: tiles covered by its endpoint union but
not by one original alone. Let E(K) be the set of triples (owner,x,y),
where x is that owner's endpoint, y is another owner's adjacent endpoint
in the same tile, and y is not in the first owner's original H. With q
the original charge, the inventory is

    Phi(K)=sum_K(max(0,-q)+I[q>0])+2|F(K)|-|E(K)|.          (1)

This uses source-labelled events, not unlabelled adjacency pairs. Retain

    A=U(W+2,D,F), chart(r,c-1),
    B_i=U(W,4,4), chart(a_i+r,c), 0<=i<n,

where W>=6 is even, every a_i>=2, D and F are even, n>=2, all a_i are even,
a_(i+1)-a_i>=10, and D,F>=a_(n-1)+4. Let g=n-1 and let m count the gaps
equal to ten. For each gap select the ACTUAL owner of

    p_i=(a_i+5,1).

At the m ten-row gaps also select the actual owner of (a_i+5,W), counting
a shared owner once. Then the resulting selected inventory K satisfies

    Phi(K)>=g+3m.                                         (2)

In particular selecting just the left axial owner at every gap gives
Phi>=g for arbitrary even gap sizes, without a density condition. When
all gaps equal ten, (2) recovers Phi>=4g. This closes the selected-budget
deficit in the earlier mixed ten/twelve-row residual family.

The statement concerns these retained originals and these selected actual
owners. It does not assert existence of a complete extension or control
the signed contribution of arbitrary unselected actual originals. The
global5/6 improvement and rectangular-grid triple equality remain open.

## Classification at one gap, with no dimension cutoff

Normalize a_i=0 and put s=a_(i+1)-a_i, an even integer at least ten. The
two bordering originals have bars at rows0,1 and s,s+1. Their stems are
in columns1,W through rows4 and s+4. The outer walls occupy columns0,W+1
through the entire gap. The original support p=(5,1) of the earlier B is
absent from the retained endpoints. Its north and west neighbours (4,1)
and (5,0) are retained endpoints. Thus completeness forces a new original
to consume p, with internal endpoint directions confined to east/south.

A U at p can only be an east terminal, south terminal, or east/south
outer corner. A straight-stem point needs two opposite directions, and
all remaining bar/branch roles have degree at least three. A rotor can
only be a terminal; its finite orientation list gives H and L from the
spacing-ten note. All U owners fall into the following FOUR families.
Every parameter b,d,e is even, with the ranges stated in the table.
Charts act on the complete canonical T,H,M records.

| Type | U parameters and chart | Exact parameter range |
|---|---|---|
| D | U(b,d,e), (r,c)->(5+r,c) | 6<=b<=W; 4<=d,e<=s-6 |
| U | U(b,d,e), (r,c)->(5+d-r,c) | 6<=b<=W; 4<=d<=s-6; 4<=e<=d+2 if b<W, and 4<=e<=d if b=W |
| R | U(b,d,e), (r,c)->(4+c,1+r) | 6<=b<=s-6; 4<=d,e<=W-2 |
| E | U(b,d,e), (r,c)->(4+c,1+d-r) | 6<=b<=s-6; 4<=d<=W-2; 4<=e<=d |

For an east/south corner with an east-going bar, the stems point south:
this is D. A longer breadth crosses the wall at column W+1; either depth
larger than s-6 crosses the next bar at row s. Both continuous stems and
the bar are inside these barriers exactly in the stated range. If instead
the bar goes south and the stems go east, this is R. A bar ending at row
b+4 cannot reach row s, so even b<=s-6; each horizontal depth must stop
before column W+1, giving even d,e<=W-2. These are both corner choices.

For a south terminal the near stem goes down to the outer bar at row5+d.
Its continuous segment crosses row s if even d>s-6. An east-going bar
must have b<=W; a west-going bar crosses the wall at column0. The far
stem also points north. If e>=d+4 it reaches row1, which is occupied by
the earlier B at every even column b with 6<=b<=W. Hence e<=d+2.
When b=W the earlier B additionally occupies (3,W),(4,W), excluding
e=d+2; this gives U. Conversely every listed U avoids the fixed endpoints.

For an east terminal the near stem goes east to a vertical bar at
column1+d. A west-pointing near stem would use the already occupied west
neighbour of p. The bar cannot go north: breadth>=6 then reaches row0
inside the earlier bar. A south-going bar ends at row b+4, so even
b<=s-6. The near horizontal segment must stop before the right wall,
giving d<=W-2. The far segment points west from column1+d. If e>d it
crosses the left wall; otherwise it stops at column at least1. This is E.
These cases exhaust the full U graph roles, not just sampled dimensions.

For s=10, R/E are empty. D has depths4,4; U has near depth4 and far
depth4 or6, with6 forbidden at b=W. Thus this table specializes exactly
to the previous D_b,U_b,V_b list. At s=12 the new rotated sources have
breadth exactly6, but their horizontal depths need not be equal.

## Exact single-owner receipts

The original charges can also be derived directly at arbitrary dimensions.
Put t=(d+e)/2. The canonical matching has b-1+t edges. In the canonical
alignment its endpoint tiles number b/2+1+t and its original supports
inside those tiles number4+t, so its charge is1. In the D alignment the
corresponding counts are b+t and2+t, giving charge1-b. In the outer-wall
alignment (r,c-1) the counts are b/2+t and t, giving charge-1. These counts
come from the two bar rows, the two disjoint stem tile columns, and their
alternating lateral supports; axial terminal supports lie inside precisely
in the canonical and wall alignments. The U/E charts are tile-preserving
images of the canonical alignment, and R is a tile-preserving image of D.
For H/L the edge/tile/inside-support counts are4/5/4 and4/4/4, yielding
charges-2 and0. Thus the charge column below does not depend on sampling.

Take the marginal against the entire retained old inventory, not just one
wall. Put I=I[b=W] and J=I[e=d]. The complete old/new mixed-tile/event
counts and original charges are:

| Type | New mixed full tiles | New source-labelled events | Charge q | Exact marginal DeltaPhi |
|---|---:|---:|---:|---:|
| D | d/2+1+I(e/2+1) | d+1+I(e+1) | 1-b | b+I |
| U | d/2+1+I(e/2+J) | d+Ie | 1 | 3+2IJ |
| R | b/2 | 3b/2 | 1-b | b/2-1 |
| E | 1 | J | 1 | 3-J |
| H | 1 | 1 | -2 | 3 |
| L | 1 | 0 | 0 | 2 |

Here are direct set partitions behind the table. The coordinates below
are relative to the upper bar; add a_i to rows for the original gap.
Existing full tiles and events persist because all endpoint sets remain
disjoint and no original support is changed.

For D the left mixed tiles are (j,0), 2<=j<=d/2+2. At every even row
6,8,...,d+4 there are the two opposite directed events between columns0
and1; there is also the event from the new p=(5,1) to the old tip(4,1).
The old tip's reverse direction is in its original support, so is not
an event. When b=W, reflecting the same list gives the right band with
d replaced by e. Otherwise no right band occurs. The three-source tile
at the old tip belongs only to this band. This proves the first row.

For U the left mixed tiles have the same row list; the two directed
wall events at rows6,8,...,d+4 give d events. There is no tip event:
each original's axial neighbour is in its own immutable support. If
b=W, the far leg has e wall events and e/2 full tiles, plus one extra
tip tile precisely when its terminal also has row5, namely e=d.
If b<W, the far leg's top row can be3, but its even column is at most
W-2, so it meets neither old wall nor the earlier B in a physical tile.
This gives the second row, including asymmetric far depths.

For R the new outer bar occupies (r,1), 5<=r<=b+4. The mixed full
tiles are exactly (j,0), 2<=j<=b/2+1, including the old tip tile at j=2.
There are b events from this new bar to the wall, one at each of its
rows, and b/2 reverse events from the wall at even rows6,8,...,b+4.
Its inner bar and horizontal stems have no other old contact. The tip
directions are original supports and produce no extra event. Thus
2|newF|-|newE|=-b/2; adding the charge mass b-1 gives b/2-1>=2.

For E the only new full tile is (2,0), using the earlier B's tip and p.
Both potential tip directions and p's west neighbour are in the relevant
original supports. The far terminal meets column1 exactly when e=d,
at the even row b+4. This contributes the single reverse event from the
outer wall( b+4,0 ) to that terminal; the other direction is in the new
source's original support. Its last tile is not full, so there is no
second tile credit. All other points are away from the walls. This gives
3-I[e=d]>=2. The H/L receipts are unchanged from the earlier exact list.

These arguments also show there is no contact with another old B: the
only potentially mixed old tip is that of the bordering upper B, and the
next B begins in a later tile row. Formula(1) now proves

    DeltaPhi(actual left axial owner)>=2                  (3)

for every even gap and every permitted dimension/orientation. At s=10
one may instead select both actual gates: the earlier lower-rotor
nonextension theorem and joint receipt table give a joint marginal>=5,
including a spanning source counted once. No extra credit from excluding
L is assigned to the support or wall in (3).

## Simultaneous allocation and no repeated surplus

The classification gives endpoint rows in [a_i+3,a_(i+1)-1]. Therefore
every tile containing a selected source lies in tile rows

    a_i/2+1,...,a_(i+1)/2-1.

These intervals are disjoint for distinct gaps, even for unequal gaps.
In particular actual selected owners are different across gaps: one
original cannot belong to two disjoint endpoint windows. The only old
endpoints met in these tile rows are A and B_i. New sources from two
different gaps have no common physical tile, hence no mixed full tile
and no new/new event. Old-owner events have their spatial tile and owner
label, so are assigned once even though the same outer A meets many gaps.
The exact full-tile and source-labelled event differences are consequently
disjoint unions of the local receipts, all against the SAME old inventory.

The even-bar ledger gives Phi(old)=1-n=-g. Select one left owner in each
of the g-m non-ten gaps and both actual gate owners in each ten gap,
counting a shared spanning source once. The exact identity is

    Phi(K)=-g+sum_(ten gaps)J_i+sum_(other gaps)DeltaPhi_i.

Each first sum term is at least5 and each second term is at least2. Thus
Phi(K)>=-g+5m+2(g-m)=g+3m, proving(2). If only the left owners are selected,
the same partition gives -g+2g=g. This uses each source, physical tile,
source-labelled event and unit of local surplus once. It does not spend
an unknown right owner's surplus at a wider gap or assume that adding
arbitrary further originals is monotone.

## The earlier unbounded residual is necessarily supplemented

The earlier partial family had bars a,a+10,a+22,...,a+10+12r, one spanning
U_W at the first gap, and exact Phi=4-r. In any complete extension there
must additionally be a left axial owner at each of the r twelve-row gaps.
The new classification and separation give combined increment at least2r,
so this selected augmentation has Phi>=4+r. The omitted owners cannot
be identified with the first spanning U or reused across the r gaps.

The bound on this particular partial augmentation is attained by taking
R=U(6,4,4) with chart(r,c)=(a_i+4+c,1+r) at every twelve-row gap. Each
adds exactly2; all immutable records have disjoint endpoints. This is
partial-inventory sharpness only. The existence and additional signed
contributions of a whole complete extension remain outside the theorem.

## Verification and remaining frontier

The companion full-record verifier checks both inclusion directions of
the classification against sampled source dimensions/orientations, exact
single-owner charges/tile/event receipts, arbitrary mixed gap sequences,
source-labelled disjoint event partitions and the 4-r to 4+r augmentation.
It also tests dimensions and gaps2000. Enumeration supplements the general
classification and receipt proofs above; it is not their justification.

The companion Lean file checks the unbounded dimension frontiers, exact
receipt arithmetic, endpoint/tile-window separation and the simultaneous
g+3m bound. Whole-source role adapters, actual-owner selection, geometric
receipt assembly and complete-extension semantics remain written proofs.

No independent acceptance of this new theorem is inferred from earlier
reviews, including the now accepted original spacing-ten stream71332. The next issue
is the signed marginal of UNSELECTED actual originals and a uniform
whole-family allocation; selecting an already compensated subinventory
does not settle that issue. General mixed geometries and the global grid
targets remain open. The submitted manuscript is unchanged.

Completed Python81720 exited0:12288 U/256 rotor roles over16 width/gap
patterns,490 surviving normalized records,2459 exact T/H/M receipt controls
(750 D,597 U,680 R,400 E,16 H,16 L),256 one-owner and256 mixed ten/both-gate
batches,128 tile-preserving isometries,12 exact residual augmentations,
and all four source types in three dimension/gap2000 controls. Full new
tile/event SETS, not merely their counts, agree with the written lists.

Local Lean4.33.0 process78572 exited0:27 explicit definitions/theorems,
18 local theorems, plus the Mode type individually audited. Only ordinary
propext/Classical.choice/Quot.sound or no axioms; no warnings/sorry/native.
Preflight43% memory free, comm-basename inspection found no active lean/lake.
These scoped checks do not formalize the complete source-role assembly.

A distinct independent audit of this new general theorem was submitted
through the oracle broker, original streaming process11740, after checking
the live pool. The packet includes this proof, exact canonical T/H/M and
inventory definitions, the verifier/Lean sources and the prerequisite
spacing-ten/lower-L proofs. It completed ACCEPT as task42c0656c-b9d1-4444-a380-ea1e09349eab,
conversation conv_e18bcaa504addda4: original11740exit0/DONE,20944 response
characters exactly matching the terminal API, observed gpt_6/pro. The
audit independently reconstructs the all-parameter catalogue, charge
alignments, complete receipt sets and nonreuse, and directly verifies the
lower-L prerequisite and residual augmentation. It reports eleven targeted
reconstructed set comparisons and reviews the Lean declarations without
rerunning Lean. No mathematical correction was requested; this revision
makes W even explicit and adds the suggested charge-count derivation.
See `output/all-even-gap-axial-review-terminal.json` for the full receipt.
Earlier original71332 completed with ACCEPT,18842 response characters exactly matching
the terminal API, observed gpt_6/pro. That earlier written audit covers
spacing-ten classification/receipts/nonreuse and the gap6/minimum10
corollary; it does not cover this general-gap result or the lower-L proof.
Its receipt is archived separately; no request was restarted. The later
`SEALED_CHAMBER_LOCALIZATION_AND_REPAIR.md` was not in either review's
initial packet and is not covered by these acceptances.
