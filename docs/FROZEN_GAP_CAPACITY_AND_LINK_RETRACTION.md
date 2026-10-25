# Frozen gap capacities and the exact cost of retracting earlier links

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The [colored-slot theorem](COLORED_INTERVAL_SLOTS_AND_MONOCHROMATIC_HOLES.md)
raises a geometric question: does complete freezing force a second distinct
unit beside two same-color mixed exits? It does not. In its actual paired
board we can prescribe every shared-gap capacity from zero to its initial
size by adding isolated selections, with NO endpoint, matching, terminal
type, link graph, endpoint occupied degree or freezing-witness change.

At capacity one, the earlier same-color collision is an intrinsic shortage
of the FULL shared support, not a poor choice among ten available units.
If both earlier alpha-to-mixed links must remain, no further permitted link
can repair it. One link must be retracted and replaced by an existing beta
bypass. We prove the exact arbitrary-copy capacity/retraction frontier below.

Intrinsic shared-resource collisions and the need for joint allocation are
already established in the [mixed-relay collision note](SHARED_DONOR_COLLISION_AFTER_MIXED_RELAYS.md).
The new points are endpoint-preserving geometric capacity suppression in the
same-color-hole family, and the sharp number of earlier links that must be
allowed to change. This is not a new general flow theorem or a grid-target
counterexample.

## 1. A capacity knob with unchanged endpoints and freezing

Use the paired board F_w in Section 3 of the colored-slot note, for even
w>=30. It has shape 14 by w, 40 endpoints, 42 selections, matching M_w,
and two productive mixed owners R_L,R_R. Their TP exits are (7,8) and
(6,w-9), both odd. Both support exactly the L=w-20 singleton interval
units in band rows 6,7, columns 10 through w-11. The bounding columns
9 and w-10 are BT, with selections respectively in row 7 and row 6.

Choose any integer capacity c with 0<=c<=L. Put m=L-c and add selections

    X_c = {(6,j): 10<=j<=9+m, j even}
           union {(7,j): 10<=j<=9+m, j odd}.             (1)

When m=0 the set is empty. Denote the resulting physical board F_w(c).

**Lemma 1 (isolated-selection suppression).** Every new selection has no
occupied neighbor, either old or new. Consequently F_w(c) is feasible and
completely frozen. Its P, actual M, endpoint degrees, original M+PP strands,
TP/BP labels and ALL physical TP--BP links are exactly those of F_w.
Every old strict-rank witness is still the same witness. Its full original
available interval pool loses precisely the m filled singleton identities.
Both R owners have exactly the SAME c surviving support units, with no
other support.

**Proof.** Old points in rows 5 and 8 are blank in columns 10..w-11:
this follows directly from rows 1,4 of the left PP-sealed base and rows
4,1 of its right half-turn. Both sites in rows 6,7 at these columns were
blank. New selections alternate rows, so they are neither vertically nor
horizontally adjacent to each other. The first new selection is row6,col10,
diagonal to the old row7,col9 selection. If filling reaches col w-11, that
column is odd (w is even), so its selection is in row7, diagonal to the
old row6,col w-10 selection. A shorter prefix ends before that boundary.
These exhaust old/new occupied neighbors. Thus every added selection is
isolated; no old selection or endpoint gains a neighbor.

The old matching and all P remain. No P has an added selection as its band
partner or other neighbor, so terminal types, original strands, link graph
and actual endpoint degrees remain unchanged. The original freezing rank
layers transport unchanged, since all their selected and lower-mate witnesses
are retained. In fact no endpoint's freezing predicate changes.

Each filled column changes BB to BT; no TT is introduced. The old units in
this gap were all singletons, so exactly those m units disappear and no unit
is merged or created. The remaining c columns are BB singletons. Their two
adjacent endpoint owners are still R_L and R_R. No endpoint-free gap can
cross either bounding endpoint column, and the old A owners still have
empty support behind their PP seals. Hence both R supports are exactly the
c shared units. No availability restriction or reservation was imposed:
these are the full supports of the new physical board. QED.

For c=1,w=30 this is a 14-by-30 completely frozen **40P/51T** board.
It has two same-color residual holes and only ONE full-support unit after
the two A-to-R links, at band3,col19. There are 125 available original
units on the whole board; the other 124 are inaccessible to these locked
alphas, not reserved. Its literal occupancy is:

```text
..............................
.................T.T......T...
................TP.T.T.T.TPPT.
.................PT.TPPPT..T..
.................T....PP..T...
....T.................PPPPPT..
...TP.T.T.T.T.T.T.T.TPPPPP....
....PPPPPT.T.T.T.T...T.T.PT...
..TPPPPP.................T....
...T..PP....T.................
..T..TPPPT.TP.................
.TPPT.T.T.T.PT................
...T......T.T.................
..............................
```

The [standalone literal fixture](../develop/fixtures/frozen_intrinsic_one_unit_gap.json)
includes all selected points, actual matching edges and strict rank layers.
For c=0 the board has 40P/52T and no such unit, with all
endpoints still frozen. Thus no positive shared-gap lower bound follows
from complete freezing or unchanged endpoint degree alone. At c=1 both
R owners remain productive, and safe graph pruning retains them.

## 2. Independent copies and exact surviving-link formula

Stack q>=1 boards by shifts (14i,0). Independently choose 0<=c_i<=L.
An even blank right padding p>=0 is allowed. The previous proof and the
three-row occupied-set separation give a feasible completely frozen board
F(q,w,p,c), with

    |P|=40q, |M|=20q,
    |T|=42q+sum_i(L-c_i)=q(w+22)-sum_i c_i.             (2)

Different copies' interval identities belong to different bands. Their
owner/link graphs do not interact. The unchanged endpoint inventory is
2q alphas and 2q betas. Full ordinary AND full-fork compensation are 2q,
at minimum 2q actual links: use each A's direct exclusive A-to-B link;
each A has no own interval support, so every payment needs at least one
source link. Nothing here removes actual beta bypasses from the full model.

Let C0 contain the two old A-to-R links per copy:

    (7,6)->(7,7),     (6,w-7)->(6,w-8),                (3)

translated by 14i. These links are mutually terminal-disjoint. Keep ANY
subset K of C0 as immutable earlier cancellations and contract them before
performing further compensation. Keep every original remaining link, beta
and available original interval. Let k_i in {0,1,2} be the number kept in
copy i, and r=sum_i(2-k_i) the number released from the earlier constraint.

**Theorem 2 (exact compensation after prescribed earlier links).** The
maximum additional ordinary or full compensation is

    V(K)=sum_i [2-k_i+min(k_i,c_i)]
        =2q-sum_i max(0,k_i-c_i).                     (4)

The minimum number of ADDITIONAL actual links at this maximum is exactly
r. Kept links in K are already paid as link operations and are not part
of this additional cost. They themselves consume no beta and pay no alpha.

**Proof.** In a copy, each kept link joins one A to its own R and leaves
an alpha whose free ends are that A's outer hole and R's shared-gap exit.
The R exit's only neighboring BP is already consumed by the kept link.
In the FULL original graph the outer A end can enter a dead mixed owner
D: its BP/TP are (10,7)/(10,8) on the left and (3,w-8)/(3,w-9) on the
right. Each D has empty whole support and its TP's only candidate is its
own BP. Entering it cannot reach a new resource or beta. The established
safe graph-pruning theorem deletes these dead branches without changing
optimum, while retaining all original physical points and interval identities.
Thus a locked alpha has no PRODUCTIVE remaining link, and its entire usable
support is precisely the c_i shared intervals. These k_i
alphas have only c_i different unit resources between them and at most
min(k_i,c_i) can be paid, with zero further links.

The other 2-k_i original A owners can each use their still-free, different
private beta in one link. These beta paths do not touch any R or shared
interval. No other demand is present, so the upper bound just obtained is
attained by these independent choices. Forks cannot enter a locked alpha:
it has no remaining outgoing link and only the same shared interval support.
Every unlocked A has empty own support and needs a source link for payment.
At the maximum every unlocked A must be paid in addition to the locked
maximum, so exactly 2-k_i further links are necessary and sufficient.
Different copies have separate owners, beta identities and bands; summing
proves both claims without reusing any resource. QED.

In particular, if all of C0 remains, V(C0)=sum_i min(2,c_i). At c_i=1
this is only q, although the uncontracted full system pays 2q. No sequence
of ADDING further links while retaining C0 repairs that loss. This statement
concerns the fixed cancellation restriction, not removal of physical M edges.

## 3. Sharp retraction-budget frontier

Put

    d_i=max(0,2-c_i),       D=sum_i d_i.                (5)

Allow at most an integer R>=0 earlier links to be released from C0. Every
released link is then available as an ordinary candidate again; it is not
deleted from the physical graph. New optimization uses ALL original interval
and beta identities, with no reservation. Then

    V_R=2q-max(0,D-R),                                (6)
    minimum further-link cost at V_R = min(R,D).       (7)

Consequently full payment requires and permits exactly D earlier-link
retractions. If every c_i=1, this is EXACTLY one in each copy, hence q.
If c_i=0, both earlier links in that copy must be released. If c_i>=2,
that copy needs no retraction. A full repair attaining D also uses the
minimum possible TOTAL 2q actual links: replace each released A-to-R by its
one A-to-B bypass, keep all other C0 links and allocate different shared units.

**Proof.** With r_i=2-k_i releases, copy i's deficit in (4) is
max(0,d_i-r_i). Each release can remove at most one unit of this deficit.
Thus total remaining deficit is at least max(0,D-R). For attainment list
the d_i repair tokens in each copy, labelled by actual side 0 or 1; there
are D different original links, not D names for shared units. Release the
first t=min(R,D) such links. Each removes one unit of deficit and exposes
its own private beta bypass, proving (6).

Every feasible selection attaining V_R needs at least t releases to gain t
payments over V(C0). By Theorem2 its maximum under that retained subset has
minimum additional cost equal to the number of releases; moreover any
actual packing attaining V_R has at least t unlocked-source payment links,
since locked alphas together can pay at most the baseline shared capacities.
The constructed t beta replacements attain this bound, proving (7).
At R>=D all 2q sources pay. Every source still needs a link, giving the
total-cost lower bound 2q attained by the stated replacement construction.
QED.

This frontier is an elementary specialization of the existing strand flow
under the proved physical interface, not a new flow theorem. The previous
mixed-relay construction already showed shared donor failure. Equations
(1)--(7) add an independently adjustable geometric capacity and an exact
lower bound on route revisions, with SAME old endpoints and actual matching.

The numeric grid target is not threatened: the half-area margin here is

    |V|/2-(|T|+|M|)=(6w+7p-42)q+sum_i c_i>0.          (8)

The exact full available interval count is (6w+7p-56)q+sum_i c_i.
Indeed alpha and beta counts are both 2q, so the established band ledger
gives total interval count equal to the half-area margin. Each of the 7q
bands has two different singleton boundary-marked intervals (its first and
last columns), excluding exactly 14q units. No other interval is excluded.

Nor is ordinary/full compensation itself deficient before imposing K.
This eliminates a proposed purely local route-preserving repair strategy;
it makes no claim of a universal 5/6 improvement.

## 4. Verification and formal scope

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_gap_retraction.py \
  --output output/frozen-gap-retraction-validation.json
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_intrinsic_gap_fixture.py \
  --output output/frozen-intrinsic-one-unit-gap-validation.json
cd formal
lean SubQuorum/FrozenGapRetraction.lean
```

The solver-free verifier reconstructs the original full supports for every
new physical board; no interval is artificially reserved. It checks isolation
of added selections, unchanged endpoints/strands/links/degrees, unchanged
strict-rank witnesses, and deletion of precisely the filled singleton
coordinate identities. It then contracts the actually kept TP--BP links
using unioned whole-owner supports and compares ordinary/full optima with
(4). Small cases enumerate ALL kept-link subsets; larger cases independently
construct frontier witnesses and sample additional subsets. Independent
primitive packings check selected contractions. These are controls for the
general proofs above, not an inference from finite capacity values.

Completed controls: 300 physical completely frozen boards with 300 strict-rank
certificates, checking 4,780 isolated added selections. There are 5,642 retained
link subsets and 11,284 ordinary/full contracted comparisons, 600 original
full-pool comparisons, and 1,932 constructed budget-frontier witnesses. On
252 boards every retained subset is enumerated, yielding 1,260 exhaustive
budget optima. The remaining 48 boards have constructed frontier witnesses
and sampled additional subsets. Forty-eight independent primitive comparisons
check selected family cases. The fast literal-fixture checker separately reads
the full coordinate/matching/rank JSON, without calling the family constructor,
and performs eight more primitive comparisons on its four kept-link subsets.
These are separate runs on overlapping geometry, not 56 different geometries.
No interval availability restriction is used in any of these models.

The Lean companion formalizes isolated-selection feasibility preservation,
capacity/surviving-link arithmetic, the per-copy and global retraction lower
bounds, labelled repair-token allocation and scoped geometry/counts. It does
not formalize the complete physical support adapter, inductive-freezing
transport or ordinary/full flow equivalence. The current submitted manuscript,
public main, PR #3, shared CI and independent star-forming/C4 result remain
unchanged. No mail or new Oracle request is part of this continuation.

All 15 scoped Lean declarations pass locally on Lean4.33.0: two are axiom-free,
the rest use only propext, Classical.choice and Quot.sound, with no warning,
sorry or native-decision axiom. Preflight measured 16GiB physical memory and
42% system available; wide comm-basename enumeration found no active Lean/Lake.
One process was used; the post-run enumeration is empty. The [formal receipt](../output/frozen-gap-retraction-formal-check.json)
states the exact adapter limitations. Mathematical and computational evidence
is in the [family receipt](../output/frozen-gap-retraction-validation.json)
and [literal-board receipt](../output/frozen-intrinsic-one-unit-gap-validation.json).

The remaining geometric question is joint route selection: after intrinsic
same-color collisions, when does frozen geometry guarantee mutually compatible
different beta or interval bypasses? It is insufficient to retain all earlier
locally useful cancellations, to search only new interval assignments, or to
assume two reachable exits provide two original units. Any general argument
must retain real mixed-owner capacities while allowing justified route changes.
