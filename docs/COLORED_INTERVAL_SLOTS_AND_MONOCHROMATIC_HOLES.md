# Colored interval slots and a frozen same-color-hole obstruction

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The [seam theorem](SEAM_RESIDUAL_COMPENSATION.md) assigns at most one tip to
each original interval. Its same-color-hole argument extends to two tips per
interval under an additional **color capacity** condition. The condition is
necessary for this extension: a completely frozen 14-by-30 board has two
same-color relevant holes and a legal two-slot certificate that still loses
one payment. Both assigned tips use one original interval and have the other
color. Two distinct available intervals repair that certificate without
changing its actual cancellation links.

This is a refinement of the existing partial-certificate and paired-hole
arguments, not a new general matching theorem. The physical example defeats
an unsound extension of the certificate rule, not full grid compensation.

## 1. Fixed model and colors

Use the finite original strand model and fixed original interval identities
of [partial certificates](PARTIAL_TIP_COMPENSATION_AND_SAFE_PRUNING.md).
Owners have disjoint alpha, beta or mixed terminal pairs; physical TP--BP
links are declared, and W(x) is the fixed whole-support set of owner x.
All earlier immutable links have already been contracted. Each interval
still has ONE payment unit, irrespective of its two certificate slots.

In addition, color every terminal by 0 or 1. Assume each original strand
has opposite-color ends and every declared physical link joins opposite
colors. These conditions hold for the actual M+PP strand system in any
rectangular grid, for any band direction or matching: its open paths have
odd length. Selecting any terminal-matching set C of links preserves this
property for final open strands. No fixed-height or retained-copy hypothesis
is required for this finite statement.

Take any partial two-slot certificate, select its BP-assigned links C, and
form Q exactly as in the [paired-hole note](PAIRED_HOLES_AND_CERTIFICATE_OPTIMIZATION.md):
left vertices are final alpha paths, right vertices are ORIGINAL intervals
assigned to their free ends, one incidence edge per assigned end. Each
alpha has degree two minus its holes and each interval has degree at most
two. A free end assigned a BP cannot occur, since that link was selected.
Holes on final mixed paths do not enter Q.

For each Q component K define:

* h_c(K): number of unassigned final alpha ends of color c;
* e_c(K): number of original intervals having TWO assigned ends of color c
  in K. Count their identity once, even if the two ends lie on one alpha;
* s_c(K): number of interval vertices having exactly ONE assigned end in K,
  of color c.

Only assigned ends on final alphas enter e and s. An interval slot occupied
on a final mixed path is not a second alpha incidence. Using larger global
collision counts remains safe but can weaken the bound.

## 2. Color-capacity compensation bound

**Theorem 1.** Let B be the exact deficit of allocation using Q's assigned
incidences. Then ordinary whole-support compensation has deficit at most B,
with no more links than C, and

    B <= sum_K min(floor((h_0(K)+h_1(K))/2),
                   h_0(K)+e_0(K), h_1(K)+e_1(K)).       (1)

In fact the first entry equals the exact deficit in every K by the preceding
paired-hole theorem. The new entries record the physical color capacity.
In particular, if all relevant holes in each K have one color c_K and no
interval has two assigned ends of color 1-c_K, then B=0.

**Proof.** Write A for the number of final alphas in K. Every such alpha
has exactly one end of color c. Exactly A-h_c of these ends are assigned
intervals. Let R_c be the distinct interval identities named by these ends.
Since each interval has at most two assignments, counting those of color c
gives the exact identity

    |R_c| = A-h_c-e_c.

For each member of R_c, choose one alpha whose color-c end names it. The
chosen alphas are different: an alpha has only one color-c end, hence cannot
name two different members of R_c. This pays |R_c| different alphas with
different actual resources, each witnessed by a free-end owner. Therefore
the maximum assigned-incidence allocation leaves at most h_c+e_c unpaid.
Do this separately for c=0 and c=1 and use the better actual allocation,
not the sum of their payments. The paired-hole theorem supplies the first
entry in (1). Different K have different original resource vertices, so
their selected allocations combine without reuse.

Finally the actual cancellation identity is a+b_C=b+a_C. If r final alphas
receive distinct intervals, payment is b-b_C+r=a-(a_C-r). Distinct whole
betas are counted in b-b_C only once. The existing free-end-witness subset
normalization gives ordinary stems and does not increase the selected link
count. This proves (1) and the stated zero-deficit criterion. QED.

**Colored-slot version.** Permit at most one assigned color-0 end and at
most one assigned color-1 end per original interval. Then e_0=e_1=0 and

    B <= sum_K min(h_0(K),h_1(K)).                       (2)

Thus arbitrarily many same-color holes cost no payment, while a resource
may be assigned two opposite-color tips. This strictly relaxes the seam
theorem's one-tip-per-unit sufficient condition. It does not establish that
all frozen configurations possess such a certificate. Each interval still
pays at most one alpha; the proof chooses one of the color allocations.

**Exact signed diagnostic.** Counting assigned colors at alpha and interval
vertices in any K gives

    h_0+2e_0+s_0 = h_1+2e_1+s_1.                       (3)

Each alpha contributes one end of each color; a mixed-color double interval
contributes one of each, a same-color double contributes two, and singleton
intervals contribute the indicated s term. If K has two holes, it is an
alpha-ended path, all interval degrees are two and s_0=s_1=0. Consequently
two color-0 holes force e_1=e_0+1, and two color-1 holes force e_0=e_1+1.
This identifies the color of the resource collision needed by a same-color
two-hole chain. Mere endpoint parity without interval color capacities
cannot exclude that chain.

The bounds are sharp. One isolated alpha with no assignments has one hole
of each color and exact deficit one. Two alphas with color-0 holes and their
two color-1 ends assigned to one interval have e_1=1 and exact deficit one.
Disjoint copies make either loss unbounded. The second pattern is realized
by the frozen configuration below, after safe graph pruning.

## 3. A fully frozen physical same-color-hole family

Let F be the explicit 10-by-16 PP-sealed frozen board in
[the internal obstruction note](FROZEN_TIP_SLOT_OBSTRUCTION.md), whose
selected points, matching and strict rank layers are also declared literally
in `check_frozen_tip_slot_obstruction.py`. For even w>=30 put two transformed
copies in a 14-by-w rectangle:

    L(r,c)=(r+4,c),             R(r,c)=(9-r,w-1-c).       (4)

The left copy is shifted down four rows; the right is turned by 180 degrees.
These transformations preserve the horizontal two-row bands. The occupied
column ranges are 1..13 and w-14..w-2, separated by at least three columns.
Hence no occupied adjacency is added between the two copies. The original
matching edges remain disjoint, every selected feasibility bound is unchanged,
and transporting the strict-rank layers gives complete freezing of all 40
endpoints. There are 42 selected sites. The first and last rows are blank.

For q>=1 stack these paired boards by translations (14i,0), 0<=i<q;
optionally append any even number of blank columns. Consecutive occupied
row ranges are also separated by at least three rows. Thus the same argument
proves feasibility and complete freezing for every q,w and padding value.
The construction has 40q endpoints and 42q selections.

Safe reachability/productivity **graph** pruning retains, per pair, two
alphas A_L,A_R, two betas B_L,B_R and two productive mixed owners R_L,R_R.
It does not erase grid endpoints or release new gaps. The relevant terminals
for one pair are:

| Owner | Left terminals | Right terminals |
| --- | --- | --- |
| A, both TP | (7,6), (10,6) | (6,w-7), (3,w-7) |
| B, both BP | (7,5), (8,5) | (6,w-6), (5,w-6) |
| R, BP then TP | (7,7), (7,8) | (6,w-8), (6,w-9) |

Both A supports are empty. Each lower/outer A end, (10,6) or (3,w-7), has
no remaining target; both have color 0. The A-to-R links use (7,6)->(7,7)
and (6,w-7)->(6,w-8). Both free R tips have color 1. Their whole-support
sets are the SAME w-20 available singleton intervals in band rows 6,7:
BT columns 9 and w-10 bound a gap with BB columns 10..w-11. No PP seal is
crossed in this shared gap. Padding cannot cross either A's old PP seal.

Choose two distinct units j,k in this gap. Select the two A-to-R links and
assign BOTH R tips to j's two slots. This is a legal maximum two-slot
terminal certificate of size four: the two untargetable A ends give an
upper bound four, achieved by these four assignments. Its Q is

    color-0 hole -- A_L+R_L -- j -- A_R+R_R -- color-0 hole.

Thus h_0=2,h_1=0,e_0=0,e_1=1. Its exact assigned-incidence payment is one,
deficit one, attaining (1). All its relevant holes have the SAME color.
The interval connection is virtual counting support, so it need not preserve
the physical checkerboard bipartition. This is exactly where the unqualified
extension of the physical odd-path argument fails.

Change only the right R slot assignment from j to k. The certificate remains
maximum, with the same two physical links. Both Q components now have one
color-0 hole and a private interval; e_0=e_1=0, so (2) gives full payment two.
There is also the independent direct beta payment via (7,6)->(7,5) and
(6,w-7)->(6,w-6). Since A supports are empty, each alpha requires at least
one link. Hence unrestricted ordinary and full payment are exactly two at
minimum cost two.

For q stacks the bad maximum has size 4q, 2q color-0 holes, q different
color-1 collision intervals and exact assigned-incidence deficit q. The
repaired maximum pays all 2q alphas with 2q links and different intervals.
These statements follow from the separated geometry and shared gaps, not
from testing finitely many stacks. Each original interval identity belongs
to its own band and is spent at most once.

**Scope of the failure.** This refutes “monochromatic relevant holes plus
arbitrary two slots imply complete certificate payment,” even for completely
frozen, safely pruned physical systems and maximum certificates. It does not
refute existence of a good maximum certificate, full compensation, or the grid
target. Restricting the pool to j and permitting only the two A-to-R links
does create a true restricted-model deficit one; allowing k repairs it, and
allowing the original beta links also repairs it with j alone. State all
three resource/link models separately.

## 4. Verification and formal scope

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_colored_interval_slots.py \
  --output output/colored-interval-slots-validation.json
cd formal
lean SubQuorum/ColoredIntervalSlots.lean
```

`develop/check_colored_interval_slots.py` reconstructs actual strands,
checks physical feasibility and transported strict ranks, redoes safe graph
pruning, and tests bad/repaired maximum certificates and the distinct-unit
and restored-beta repairs. General colored strand controls check (1)--(3),
including arbitrary partial certificates and actual countercontrols. The
script also supplies an opposite-color double-slot control, so the relaxation
beyond one tip per interval is exercised rather than vacuous.

The accompanying Lean module proves generic one-color resource counting
from an actual map, the signed color identity, two-hole collision necessity,
the zero-deficit color criterion, scoped sharp-family arithmetic, actual
hole/assigned-tip colors, and arbitrary-copy separation and half-turn parity.
Physical arbitrary-copy geometry, Hall/normalization and the actual packing
adapter remain written proofs and Python checks. This is not an end-to-end
formalization of the physical theorem.
All 15 scoped Lean declarations pass on the user-selected local Lean4.33.0;
one is axiom-free and the others use only propext, Classical.choice and
Quot.sound. No warning, sorry or native decision axiom occurs. The 16GiB
machine reported 42% available memory at preflight; wide comm-basename
enumeration found no active Lean/Lake before one process or after completion.
See [validation receipt](../output/colored-interval-slots-validation.json)
and [formal scope](../output/colored-interval-slots-formal-check.json).

No universal numerical 5/6 improvement follows. The next geometric question
is whether frozen configurations permit a resource assignment with no
opposite-color collision on their residual-hole components, or force enough
distinct interval/beta bypasses to pay those collisions. The preceding seam
theorem satisfies the stronger one-tip restriction and is unaffected. The
11 October submitted manuscript, public main, PR #3 and shared CI are preserved;
no Mail action is part of this round.

Completed controls: 400 abstract systems, 550 exhaustively checked partial
certificates within designated small systems, and 144 actual frozen boards
(q=1..8, w=30/32/40, padding=0/2/10, with and without horizontal reflection).
There are 2,039 certificate checks and 4,167 assigned-incidence components,
864 ordinary/full checks across the three resource/link models, and 12
independent primitive comparisons. All 144 transported strict-rank
certificates pass independently of the peeling check. The generic opposite-
color double-slot control pays exactly one alpha with one original unit.
An Oracle broker attempt, task `01d4652b-375b-478b-ad25-08f35120641a`,
terminated with `model_unavailable@selecting_model` and no mathematical
answer; this is not an independent review or acceptance and was not retried.
The [terminal failure receipt](../output/colored-interval-slots-oracle-attempt.json)
is separate from the mathematical validation records.
