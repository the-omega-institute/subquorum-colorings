# A completely frozen beta fork, reserved-resource gain, and simultaneous replacement

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

Complete freezing does **not** exclude beta forks in the whole-owner-support
normal form. We give an explicit 16 × 14 board with 66 completely frozen actual
matching endpoints. Two different original alphas enter the two different BP
tips of a single beta. Its internal PP body supports an available original
interval. The two-link cancellation pays two demands, using **one whole beta
and one different original interval**.

With a declared source/resource reservation this is a strict 2-versus-1 gain
over ordinary owner-support flow, realized on the unchanged physical board.
The unrestricted board has value 3 with one link in both models. Thus the
example refutes universal frozen-fork exclusion, and establishes strict
reserved-interface gain, but does not establish unrestricted gain or a new
universal grid bound. We also prove an exact Hall criterion for simultaneous
ordinary replacement along fixed fork arms. It locates the remaining geometric
question without reusing a shared reserve.

The 11 October submitted manuscript, public main and PR #3 merge state are
unchanged. This is a research note, not an amendment of the submitted paper.

**Later25 October refinement:** [exact fork deficiency and arm-gap exclusion](FORK_REPLACEMENT_DEFICIENCY.md)
give fixed-arm ordinary value h+mu, a sharp Hall/tree defect, and necessary
blocking/DAG structure for a minimum-link maximum packing. In particular a
pre-beta arm gap with at least two available units excludes that fork from
such an optimum. This does not exclude the feasible frozen fork constructed
here or a multiunit gap witnessed only by its beta body.

## 1. Conventions and explicit board

Use rows 0..15, columns 0..13 and the original bands(2b,2b+1), b=0..7.
T denotes a selected vertex; P an endpoint of the actual matching M; B a blank.
Vertical within-band partners join P columns in the auxiliary strand system.
Actual matching edges and vertical PP edges remain different edges, including
when they coincide geometrically and form a two-edge PP cycle.

An available interval is an original interval in the fixed BB/TT forest,
after removing the boundary-marked original intervals. Its identity is fixed
before any cancellation. Whole support W(x) of an open original strand x is
the union of the available intervals in endpoint-free gaps bounded by a P
column of x, including internal PP columns. A pure PP cycle is not an open
owner. After cancellation, supports are unions of their old constituent
supports. These are counting witnesses; no physical free-tip access is asserted.
See [the complete normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md) for the
precise objective p=b-b_C+|F| and its ordinary-stem/fork normalization.

The permanent [fixture](../develop/fixtures/frozen_beta_support_fork.json)
contains T, all 33 actual matching edges and the strict freezing layers.
For a compact human-readable specification, T is

    (1,7) (1,9) (2,2) (2,10) (3,1) (4,3) (4,5)
    (5,1) (5,10) (6,12) (7,1) (10,1) (10,8)
    (12,1) (12,9) (13,2) (13,5) (13,8) (13,10) (13,12) (14,7).

The six open original strands have the following actual-endpoint traces.
Consecutive edges alternate actual matching, vertical PP, actual matching,
and so on; the first and last edges are actual matching edges.

    A: (3,2) (4,2) (5,2) (6,2) (7,2) (7,3)
       (6,3) (6,4) (7,4) (7,5) (6,5) (5,5)
    E: (2,9) (2,8) (3,8) (4,8) (5,8) (6,8)
       (7,8) (7,9) (6,9) (6,10) (7,10) (7,11)
    B: (5,6) (6,6) (7,6) (8,6) (9,6) (10,6) (11,6) (12,6)
    D: (7,12) (8,12) (9,12) (10,12) (11,12) (12,12)
    C: (12,2) (11,2) (10,2) (10,3) (11,3)
       (11,4) (10,4) (10,5) (11,5) (12,5)
    G: (12,10) (12,11).

A,C,D are alpha; B,E are beta; G is mixed, with TP(12,10) and BP(12,11).
The eight remaining components are pure PP cycles in band/column positions

    (1,7), (2,7), (3,7), (4,11), (4,5), (5,11), (5,7), (6,7).

Each cycle consists of its two physical vertices and their actual/vertical
edges. These traces and cycles cover all 66 endpoints exactly once and specify
M completely. They therefore independently reconstruct the fixture.

Feasibility is direct: T is disjoint from the endpoint set, M is a matching
of adjacent vertices, and every vertex of T has at most one occupied neighbor.
For every P vertex v the fixture supplies two distinct adjacent nonmate
witnesses. Each witness is either in T or is a P vertex whose actual mate has
strictly smaller recorded rank. Induction on rank proves all 66 vertices frozen.
The 16 rank layers have sizes

    5,4,4,4,4,4,6,4,4,6,4,5,4,4,3,1.

This is an explicit finite certificate proof, independently checked by
Python and by Lean's kernel; it does not depend on a solver's verdict.

The original interval inventory is:

| Original band | Raw original intervals | Boundary marks | Available intervals |
|---|---:|---:|---:|
| 0 | 12 | 2 | 10 |
| 1 | 8 | 2 | 6 |
| 2 | 6 | 2 | 4 |
| 3 | 2 | 2 | 0 |
| 4 | 10 | 2 | 8 |
| 5 | 4 | 2 | 2 |
| 6 | 4 | 2 | 2 |
| 7 | 13 | 2 | 11 |
| Total | 59 | 16 | 43 |

The whole-board margin is

    I+beta-alpha = 43+2-3 = 42
                  = 16*14/2-|T|-|M|-16.

In particular this board does not violate the target inequality.

## 2. A real fork using a beta-body interval

Let J be the original singleton interval at band 4,column 7, physically
{(8,7),(9,7)}. In this band, columns 7..10 are all BB. Consecutive BB columns 7
and 8 make column 7 a singleton in the fixed interval forest. The gap lies
between PP columns 6 and 11. Neither its singleton nor any other interior
interval here touches the boundary marks at columns 0 and 13. Thus J is an
available original unit, not newly released slack.

The left boundary PP column 6 belongs to B. The right PP column 11 is the
pure two-edge cycle listed above. Consequently **B is the only open original
owner whose whole support contains J**. This statement is about original
owner identity, not about which free tip is closest to J.

The links

    L = ((5,5),(5,6)),     R = ((12,5),(12,6))

are actual same-row adjacent TP--BP pairs. Their four endpoints are different;
the TP endpoints belong to different alpha strands A and C, and the BP
endpoints are B's two different free tips. Applying both links merges A,B,C
into one alpha with free tips(3,2),(12,2). Alpha drops 3 to 2 and beta drops 2
to 1. Allocate J to the merged alpha using B's retained body witness. The
compensation relative to these two designated original demands is

    one consumed whole B + one allocated original J = 2.

B is counted once. J is counted once. The unused whole beta E gives no
extra credit to this certificate. A and C are not the same original strand.
The pure-cycle boundary is not an additional mixed exit.

**Corollary.** The assertion that feasibility and complete freezing forbid
every feasible beta fork is false, already for this explicit finite board.

## 3. Reserved-interface strict gain and immutable first links

Keep the physical board, matching, selected set and original intervals
unchanged. Restrict this particular compensation certificate as follows:

* Designated alpha sources are A and C; the permitted nonalpha owners are B
  and the existing mixed owner G. Other original alpha/beta owners are excluded
  from this certificate interface.
* The only permitted whole-beta unit is B; the only permitted interval is J.
  Each permitted owner's support is intersected with {J}.
* All legal links between these permitted owners remain allowed.

A and C have no permitted interval support. B alone owns J. In an ordinary
owner-support flow, a beta is a unit-capacity sink, so no source can continue
through B to spend J as a second ordinary unit. G has no support and supplies
no route out of these sources. Ordinary value is therefore at most 1; L alone
attains 1 with one link.

The fork of Section 2 attains 2 using two links. Two designated sources bound
its value by 2, and both have no zero-link interval payment, so two links are
also necessary for value 2. Hence the exact lexicographic optima are

    ordinary: (value,min_links)=(1,1),
    fork-capable:               (2,2).

This is strict gain under **declared source/resource reservations**. We have
not proved that another compensation baseline forces those reservations.
Removing other demands or restricting a certificate does not change the
physical occupied set, but it does change the optimization interface.

There is a consistent sequential interpretation. Fix L as immutable C0.
It has already consumed B once, leaving one mixed owner A∪B. That owner's
support contains J and it has the free BP tip(12,6). There are now zero
unconsumed permitted betas. R is an ordinary interval stem from C through
the new mixed owner to J. It adds one interval payment with one additional
link. Total credit is1+1=2; no second beta credit is introduced. Undoing C0
is neither necessary nor allowed in this interpretation.

## 4. The unrestricted optimum and blank right padding

The full board has an ordinary value 3 solution:

* A takes the singleton original interval at band 1,column 3, supported at its
  original body column(1,2).
* C takes the singleton original interval at band 6,column 3, supported at its
  original body column(6,5).
* D takes the beta stem ((7,12),(7,11)) into E.

These use disjoint owners and two different original intervals. Value cannot
exceed the three original alpha sources. D has empty original whole support,
so value 3 cannot be attained with zero links. Thus **both unrestricted models
have value 3 and minimum link cost1**. The fork is a feasible mechanism, but
is unnecessary for unrestricted optimality in this board.

Add2p blank columns to the right, p≥0, without moving old occupied vertices.
Every band gains2p raw intervals. Its old left boundary mark remains; the
rightmost blank singleton becomes its right mark. The total marks remain16,
and

    I(p)=43+16p,    margin(p)=42+16p.

The internal J, its only-open-owner witness, the two links, and the reserved
1-versus2 optimum all persist. For p≥1, however, the old BB column 13 in
band 3 becomes unmarked: it has a new BB neighbor at column 14, so its interval
is separated from the new right boundary mark. D's TP(7,12) now supports that
available singleton. With the old choices for A and C this pays all 3 demands
with **zero** links. Therefore the unrestricted minimum cost drops from1 to0
under positive right padding. Boundary release cannot be ignored in a claimed
padding-stability statement.

## 5. Arbitrarily many frozen physical copies

For every integer q≥1 place copy i, 0≤i<q, at translation

    (r,c) -> (16i+r,c)

inside a16q-by14 board. Original occupied rows are1..14, so the two boundary
rows0 and15 of each copy are blank. Occupied vertices of distinct copies are
never adjacent. Matching edges, original P strands, legal TP--BP links and
strict-rank witnesses are translated internally. Every witness needed for
freezing stays in its copy; hence the same rank induction freezes all 66q
endpoints.

The vertical stride is even, so original two-row bands do not cross between
copies. Each band belongs to exactly one translated base board, with the same
horizontal labels and original interval partition. This proves, for all q,
exact additivity without an extra separating whole band:

    |T|=21q, |M|=33q, |P|=66q,
    alpha=3q, beta=2q, mixed=q, pure_PP_cycles=8q,
    raw_intervals=59q, boundary_marks=16q, I=43q,
    whole_board_margin=42q.

Let B_i,J_i,L_i,R_i be the translated identities. Their actual coordinates
are disjoint; in particular J_i contains(16i+8,7), so J_i=J_j implies i=j.
For the reserved union of copy interfaces, ordinary value and minimum link
cost are(q,q), and the q forks attain(2q,2q). The upper bounds follow from
q whole-beta sinks and2q sources respectively; the link lower bounds follow
because no designated source has initial permitted interval support. No links
or support incidences connect copies. Thus the strict reserved value gap is
exactly q, attaining the beta-to-support matching bound rho=q on an actual
frozen board with the stated reservations.

In the unrestricted pool the base ordinary solutions combine to3q payments
with q links. Conversely the q different D_i have empty initial support; to
pay all 3q sources every D_i must participate in at least one additional link.
No link joins two D_i or two copies, so at least q links are necessary. Thus
unrestricted optimum is(3q,q) in both models. These are general translation
and separation proofs. The finite q≤16 checks below are controls, not their
proof.

## 6. Simultaneous arm replacement: an exact Hall criterion

The next statement applies to arbitrary declared whole-support systems,
including a system already contracted by an immutable C0. It makes no
unproved geometric expansion assumption.

**Arm-replacement lemma.** Let H be a compatible pack of beta forks and K
a pack of ordinary stems on the remaining owners/resources. Every fork f
has two owner-disjoint directed arms from two different alphas through mixed
owners to different tips of its beta B_f. Fork owner sets are pairwise
disjoint and avoid K. Their assigned original intervals J_f are different
and avoid K's used intervals U. Let S_f be all owners on the two arms
**before** B_f, including the original alpha roots. Define

    N(f) = (union_{x in S_f} W(x)) \ U.                    (1)

The following are equivalent:

1. Every fork can be replaced by two ordinary stems, using only a subset of
   that fork's original links/owners, paying its two original sources,
   retaining K, and using different original intervals globally.
2. The sets N(f) have distinct representatives.
3. For every subpack Q⊆H, |union_{f in Q} N(f)| ≥ |Q|.

When these hold, one may retain **one whole-beta consumption per fork**,
keep K's owner and resource choices exactly, and reduce the total number of
links by at least |H|. All old fork intervals J_f are released before choosing
representatives, so an eligible J_g can serve another fork if it is in that
fork's N(f); it cannot be spent twice.

**Proof.** The equivalence of 2 and 3 is the finite marriage theorem.
For2 ⇒ 1 choose different representatives j_f. For each f choose an arm and
an owner x before its beta with j_f∈W(x). Stop this arm at x and pay it by
j_f; retain the other arm through B_f as a beta stem. The truncated arm drops
at least its final entry link into B_f, so at least one link disappears.
The two new stems are owner-disjoint, their owners are subsets of f, and
their terminal links are subsets of its original links. Across forks these
sets were disjoint and avoid K. The chosen intervals avoid U and are
pairwise different. Whole betas B_f are different, so no beta unit is reused.
Both original sources are paid. Any discarded arm suffix can remain as
unused strands; it gives no additional payment and interferes with none of
the retained certificates.

For1 ⇒ 2, consider the two ordinary stems replacing a particular f. Within
its owner set there is only one beta, so at most one of the two payments
can be a beta consumption. At least one must use an original interval.
An ordinary interval stem cannot pass through a beta sink; along the
retained subset of the two original arms its interval witness therefore
lies in S_f. It avoids U. Select one such interval for each f. Global
injectivity of the ordinary allocation makes these representatives distinct.
This proves2 and finishes the proof. ∎

The necessity concerns the stated **fixed-arm subset replacement class**.
Failure of its Hall condition does not rule out rerouting through other
owners, changing K or using additional links in the full network.

For the frozen base board, remove the fork and take K to be D's beta stem
into E. Then U is empty. A or C already supports an available interval, so
N(f) is nonempty and the lemma replaces the fork, explaining why full value
has no strict gain. The explicit three-payment solution in Section 4 removes
both fork links. In the reserved interface N(f) is empty, so this replacement
is impossible; the exact1-versus2 calculation is consistent with the lemma.

Checking each N(f) separately is insufficient. For example, in an abstract
system with two disjoint two-link forks, give each beta its own private
original interval J_1,J_2, and give the first alpha arm of **both** forks the
same additional original interval h. No other arm has interval support.
Each fork separately has a one-unit ordinary substitute. Together
N(f_1)=N(f_2)={h} fails Hall. The forks pay 4; ordinary flow pays at most 3,
from two whole betas and h, and attains 3. This is an exact counterexample
to separate local replacement, not a frozen-grid realization or a target
inequality counterexample. It respects the at-most-two-open-owners condition
for h and identifies precisely the duplicate-reserve error.

## 7. Discovery correction and verification scope

The older normal-form controls contained zero physical forks. Their three
short specified SAT templates were UNSAT; those are historical bounded
controls, not a nonexistence theorem. In the depth-two template, distinct
same-side incoming alpha tips already have actual mates joined by the
forced intervening within-band PP edge, making them one original alpha.
The opposite-side tip would require a mate forced blank by the specified
gap. That geometry is degenerate before freezing is considered.

Moving the gap witness into the middle of a longer beta produced the present
frozen example. The discovery script now enforces rooted connectivity of the
beta-labelled P component: equality of component labels along edges alone
can wrongly label a disconnected pure cycle as part of the beta. It also
forces the original singleton witness rather than merely an endpoint-free
gap, which could still contain only boundary-reserved units. Candidate
solutions are independently compiled and checked. The fixture was reduced
by solver-free deletions. No minimum-size claim is made.

The permanent Python verifier requires no SAT package. It checks the actual
physical cancellation, original interval identities, only-beta ownership of
J, exact ordinary/fork optima and minimum costs, immutable-L continuation,
eight carried isometries, twelve positive blank right paddings and sixteen
stacks. Carried isometries carry the chosen band partition as well; a
quarter-turn does not silently assert the same result for a separately
reselected vertical partition. Counts:

- 20 frozen physical controls with20 actual forks and20 strict reserved gains;
- 160 reserved and192 unrestricted terminal matchings independently enumerated;
- 16 frozen stacks,136 explicitly replayed disjoint fork occurrences;
- 6 small stacks independently optimized by fork packing.

A separate abstract checker compares the Hall subsets with actual ordinary
terminal min-cost flow in 784 systems: exhaustive direct arms, mixed-arm
lengths0..2, internal prefix witnesses and already used resource identities.
It finds 485 full replacements and 299 Hall obstructions, plus the explicit
two-fork shared-unit control. These finite checks support the written proof.

Twelve new Lean4.33.0 declarations, plus 16 dependency audits, pass sequentially
on the explicitly selected local machine after memory/process checks. They
verify the concrete feasible board, complete strict-rank freezing, all six
open traces and eight PP cycles, owner types, different fork tips, the
beta-body PP/gap geometry, whole-board scalar ledger, and arbitrary-copy
occupied-point separation and distinct copied unit coordinates. No sorry,
admit, native_decide or new axioms occur. Audits use only propext,
Classical.choice and Quot.sound. The full interval-construction adapter,
optimization and general Hall theorem are **written proofs**, not claimed
Lean formalizations. No external review is claimed for this note.

Reproduce:

    python3 develop/check_frozen_beta_support_fork.py --output output/frozen-beta-support-fork-validation.json
    python3 develop/check_fork_arm_replacement.py --output output/fork-arm-replacement-validation.json
    python3 develop/check_frozen_beta_support_fork_formal.py --lean /path/to/lean-4.33.0 --output output/frozen-beta-support-fork-formal-validation.json

The remaining question is whether frozen-grid geometry guarantees enough
simultaneous arm substitutes after an appropriate choice of the residual
ordinary allocation, or permits an unrestricted strict-gain board. A failure
of fixed-arm Hall would still require checking possible rerouting. The
general compensation inequality and any universal5/6 improvement remain open.
