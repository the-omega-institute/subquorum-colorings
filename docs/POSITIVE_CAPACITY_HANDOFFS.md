# Positive-capacity handoffs: linear-state recognition and exact support compilation

**Mixed-target continuation:** [three-snapshot signed support compilation](SIGNED_MIXED_SUPPORT_COMPILER.md)
works for arbitrary initial/target directions, including support-losing
families. It gives an exact polynomial monotonicity test and positive
retraction on passing inputs. A genuine old-phase support birth shows why
this note's final-H-corridor compiler and fee adapter cannot simply be
transposed componentwise and unioned for mixed targets.

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We extend the uniform V→H support-recognition theorem from capacity zero to
**all capacities zero, one and two**. If p chosen tiles have positive capacity,
at most 2+2p physical snapshots decide whether *every ordered pair of gate
subsets preserves every original owner–resource incidence*. No subset
enumeration or packing optimization is used by the recognizer.

Passing instances admit an exact prerequisite-set compiler: old incidences
are unconditional, and each additional incidence is enabled by an actual
prefix or suffix of gates in a final H gap. The compiler preserves the full
mixed/beta routing network and every original unit. It does not split a
shared activation fee into independent resource fees.

An explicit all-length feasible family shows that the previous two-state
incidence test fails for positive tiles: all original incidences survive
between the extremes, while intermediate states lose local incidences.
The family is not fully frozen and has zero payment in every state. Its
role is a precise obstruction to the two-state *support* rule. Neither it
nor rejection by the new recognizer is a counterexample to the numerical
grid inequality. A separate fully frozen 16×58 positive-capacity input is
accepted and checked in all eight states.

## 1. Physical assumptions and common identities

Use exactly the physical setting of [uniform zero-capacity openings](UNIFORM_ZERO_CAPACITY_OPENINGS.md):
an even rectangular grid, fixed feasible T and actual matching M, actual
endpoint set P, and one direction per aligned 2×2 tile. Canonical maximal
same-direction bands define the auxiliary matching. Restore all actual
M/PP edges to identify whole original owners, terminal types and actual
terminal links. Keep the full original-resource fork-flow model, including
mixed capacity one and the single whole-beta output.

Choose distinct P-free tiles G, all initially V. Opening a tile changes it
to H; all other data stay fixed. Now allow

    κ(g) = 2 − |T ∩ g| ∈ {0,1,2}.

Feasibility gives |T ∩ g|≤2: three selected vertices in a 2×2 square would
include a selected vertex with two occupied neighbours. Every state is
feasible since T,M are unchanged. Because no gate contains P, auxiliary
mates of P, restored owner bodies/types, actual links and closed cycles
are unchanged in every state.

Fully refine into aligned tiles. Each positive coarse forest contains
exactly one positive fine child, and each positive fine child has one
positive coarse parent, by the existing positive-child coarsening theorem.
Outside G use that child's fixed cell set as ID. Inside g there are κ(g)
positive fine children in either direction. Order each direction's children
lexicographically by cell set and pair the k-th V child with the k-th H
child, giving IDs (g,k). This is a fixed bijection of original capacity
units, not an assertion that coarse cell sets stay fixed.

**Lemma 1 (capacity-two pairing independence).** All local positive units
of g have the same owner support set in each physical state. Consequently
any fixed local bijection gives the same truth value for every support
inclusion used below.

**Proof.** A P-free tile lies entirely in one no-P gap of its current band.
Every positive fine child in it, and its positive coarse parent, is in that
gap. Whole-owner support is exactly the set of its open boundary owners;
it is the same for all units in the gap. With κ=2 this proves the two local
supports are equal in every state. With κ≤1 there is no choice of pairing.
Permutation of equal-support slots changes no incidence inclusion. ∎

Thus the common raw inventory Q, alpha, beta, raw L and S=L+beta−alpha stay
fixed, even though positive forests and local resource directions may change.
Let S_F(j) be the set of original owners supporting unit j when precisely
F⊆G is open. Write q(j)=g for a local unit of g; other units are fixed H or
fixed V according to their unchanging tile direction.

## 2. The phase dichotomy

**Lemma 2.** For F⊆F':

* A fixed H unit has S_F(j)⊆S_F'(j).
* A fixed V unit has S_F'(j)⊆S_F(j).
* A g-local unit has S_F'(j)⊆S_F(j) if g∉F'.
* A g-local unit has S_F(j)⊆S_F'(j) if g∈F.

The last two conclusions apply within one phase; no inclusion across its
own V→H switch is asserted.

**Proof.** With its containing tile H and unchanged between the two states,
a unit's H run can only grow as other gates open. No gate introduces P,
so a former first P boundary remains reachable; a new P boundary can become
reachable across an old artificial band edge. Its support can only grow.
With the containing tile V and unchanged, opening other gates only cuts
or shrinks its V run; a reachable first P boundary can be lost, but no new
one is exposed across a deleted segment. Support can only shrink. Transport
units using their unique positive fine children; Lemma 1 removes any local
pairing ambiguity. These arguments apply whether coarse forests change
shape or T has adjacent TT pairs. ∎

## 3. The exact critical-state test

**Theorem 3 (linear-snapshot recognition).** The following are equivalent:

(A) For every F⊆F'⊆G and every unit j, S_F(j)⊆S_F'(j).

(B) All of the following critical guards hold:

    Fixed V units:       S_∅(j) ⊆ S_G(j).
    Each g-local unit:   S_∅(j) ⊆ S_(G\{g})(j).       [closed-phase guard]
    Each g-local unit:   S_∅(j) ⊆ S_{g}(j).           [handoff guard]

Only positive-capacity gates have local units. The physical states required
are ∅,G and, for each such g, G\{g} and {g}; duplicates are evaluated once.
Thus there are at most 2+2p snapshots, independently of |G| and κ(g).

**Proof, sufficiency.** Fixed H support is already increasing. Fixed V support
is antitone and trapped between its extreme supports, which the first guard
makes equal, so it is constant.

For a g-local unit, consider any closed-g state F. Lemma 2 and the
closed-phase guard give

    S_(G\{g})(j) ⊆ S_F(j) ⊆ S_∅(j) ⊆ S_(G\{g})(j).

Hence all closed-phase support is exactly S_∅(j). Open-g support is increasing
by Lemma 2, and its least state is {g}. The handoff guard puts every closed
support into S_{g}(j), hence into every open-g support. Ordered pairs within
either phase, or crossing from closed to open, therefore preserve support.
An ordered pair cannot cross from open to closed. Apply this separately to
every original unit and owner. This proves (A).

**Necessity.** Every guard in (B) is an instance of (A), comparing ∅ with
G, G\{g}, or {g}. ∎

The theorem quantifies over arbitrary grid sizes and arbitrary gate sets.
Finite checks below audit implementations; they are not the proof. In
particular, testing individual interfering gates cannot replace G\{g}:
a closed-phase owner may have two coincident boundary occurrences, with
either surviving a single cut and neither surviving both cuts.

Every rejected guard provides an actual old owner/unit incidence and an
ordered pair of physical states where it disappears. No inference about
flow deficit, payment loss, impossibility of a destructive repair, or the
universal 5/6 question follows merely from that rejection.

## 4. Exact all-state prerequisite compiler

Assume Theorem 3 passes. Use the full-open canonical H bands. Every maximal
no-P gap has at most two boundary owners (possibly the same owner or absent),
a physically ordered list of H-unit anchors, and its actual variable gates.
Each final H unit and each gate belongs to exactly one such gap. Fixed V
units stay outside these gaps and have constant support by Theorem 3.

For a final H unit j define A_L(j) to be every variable tile between its
left boundary and its final H anchor, **including its own tile if variable**.
Define A_R(j) analogously. Keep a conditional incidence for each existing
boundary owner, labelled by the corresponding prerequisite set. Keep all
old incidences unconditionally. Then for every owner o and state F,

    j ∈ W_F(o) iff
      j ∈ W_∅(o), or
      [o=L(j) and A_L(j)⊆F], or
      [o=R(j) and A_R(j)⊆F].                         (1)

The boundary alternatives exist only for final H units. Coincident owners
use an OR of the two alternatives, not two copies of the resource.

**Proof.** For a fixed H unit, boundary access is exactly uninterrupted
H connectivity across the intervening gates, as in the zero-capacity
compiler. Its old incidences persist and have a corresponding empty
prerequisite, so adding the old set in (1) changes nothing.

For a local unit whose tile g is open, use its fixed paired final H anchor.
It reaches a boundary precisely when every intervening gate, including g,
is open. Every old incidence is preserved by Theorem 3 and therefore is
already among these reachable boundary owners. For a local unit with g
closed, support equals its original support by the closed-phase conclusion;
both H prerequisites include g, so neither new alternative applies. Fixed
V support is constant. These cases prove (1) and leave all actual owner,
link and routing capacities unchanged. ∎

The callable `compile_handoffs` constructs (1) after critical-state
recognition. `compiled_support` evaluates it without rebuilding the grid.
No gate-subset enumeration or packing oracle is called by either API.
The expanded incidence/precondition lists have polynomial size.

**Fee boundary.** A capacity-two gate can occur in both end prerequisites
and enable two different original units for one activation fee. A single
shared output also remains capacity one. Therefore this support compiler
alone does not justify the prior zero-capacity ordinary costed-flow
optimizer. Keep each gate's actual ID in its prerequisites and charge the
union once. The earlier independent-bundle matching and mixed-resource
parity results apply only when their additional independence hypotheses
are established. We do not claim a general polynomial shared-fee optimizer
or a geometric reduction of every passing positive instance to that class.

## 5. An arbitrary-length endpoint trap

For each n≥2 take an 8×(2n+4) grid. Set T={(5,1)} and use the matching

    ((4,1),(3,1)), ((3,0),(2,0)), ((2,1),(2,2));
    ((2,c),(2,c+1))                 for c=3,5,...,2n−1;
    ((2,2n+1),(3,2n+1));
    ((3,c),(3,c−1))                 for c=4,6,...,2n.

All displayed edges are disjoint unit grid edges. T has only one occupied
neighbour, (4,1), so the input is feasible. There are 2n+2 actual edges and
raw inventory 6n+13.

The fixed V tiles are (2,2i), i=0,...,n. Let g_i=(4,2i), i=1,...,n, be the
variable tiles, all initially V. Every other tile is H. The variables are
P-free and have capacity two. The auxiliary/actual edges make the entire
P set one mixed owner a: its TP endpoint is (4,1), paired to T at (5,1),
and its BP endpoint is (3,3), paired to the empty site (3,2). Reading the
matching along row 2 and back along row 3 verifies this one bent path
directly. There are no other owners.

For either unit of g_i, in every state F:

    S_F(g_i,k) = {a}   if g_i is closed,
                 {a}   if g_1,...,g_i are all open,
                 ∅     otherwise.                              (2)

**Proof.** A closed g_i's V gap reaches a above it at row 3 regardless of
other gates, which lie in different V columns. When g_i is H, the only
possible owner is a to its left, at column 1 in the H tile (4,0). It is
reachable exactly when the entire gate prefix through g_i is H. There is
no P boundary to the right. The two local slots share this gap. ∎

No fixed V tile has a positive fine child; fixed H incidences only increase.
Equation (2) shows every local incidence at ∅ survives at G, so **full
original endpoint inclusion passes**. But opening only g_i, i≥2, loses both
of that tile's old incidences. The closed-phase guards pass; exactly the
later singleton handoff guards fail.

For the smallest member n=2, both local supports follow this table:

| Open gates | g_1 units | g_2 units |
|---|---|---|
| none | {a} | {a} |
| g_1 | {a} | {a} |
| g_2 | {a} | empty |
| g_1,g_2 | {a} | {a} |

A capacity-one version adds T at (4,2n). It has just one occupied neighbour,
(3,2n), and is nonadjacent to the old T. The final gate has κ=1 and raw
inventory is 6n+12; the same formula (2) applies to its sole unit. Hence
this is also a counterexample to the naive extension using capacity-one
pivots, not only the capacity-two pairing issue.

The sole owner is mixed; alpha=beta=0 and no paid source exists. All states
have payment=links=0. These controls isolate the support-contract failure;
they make no numerical-bound or full-freezing claim. Using only g_1 as a
variable gives a passing instance with nonempty old local support and a
real legacy handoff, rather than a vacuous unsupported gate.

## 6. Independent verification and formal scope

`develop/check_positive_capacity_handoffs.py` independently builds all
physical gate states of the audit inputs, checks the phase inclusions,
compares recognition with every Boolean-lattice edge, and compares every
accepted compiled support set with the physical set. Each state is also
checked by full fork flow against independent primitive packing. Rejection
witnesses are replayed physically. API controls disable subset enumeration
and both optimization routines and still accept/reject the intended inputs.

The frozen 16×58 fixture has T166, M70, 140 strictly frozen endpoints, three
positive gates of capacities (2,1,1), and the full competing mixed/beta core.
The empty state pays 2. Opening the central capacity-two gate alone pays 4;
each separate capacity-one alternative alone pays 3; opening both alternatives
also pays 4. All eight states have minimum links 2. The new recognizer accepts,
and the support compiler is exact in all eight states. This is an adapter
of the existing frozen bundle construction, not a newly claimed frozen
endpoint trap. Other frozen audits retain capacity-zero corridors and a
positive-gate rejection case. Current exact counts are in the JSON report.

The final audit covers 128 complete subset families (78 accepted, 50 rejected),
1,332 physical states, 2,669 lattice edges and 135,432 phase/unit comparisons.
All 540 accepted-state compiled support sets are exact; all 1,332 primitive
optima agree with full fork flow. The 227 rejection witnesses include all
three guard types (18 fixed V, 25 closed phase, 184 handoff). Six endpoint
traps check n=2,3,5 in both capacities, including 724 exact formula (2)
instances; 4,184 capacity-two twin-support state instances are checked.
There are 490 replayed strict-freeze events and two API controls with
enumeration and packing optimizers disabled.

`formal/SubQuorum/PositiveCapacityHandoff.lean` proves three general logical
kernels over arbitrary states: closed-phase constancy, phase guard implies
all-state monotonicity, and critical guards iff all-state monotonicity.
All three are axiom-free in Lean 4.33.0, with no `sorry`, `native_decide`,
new axioms or warnings. These are general proofs, not finite enumerations.
The geometry, common local pairing, capacity-two support equality, physical
compiler and controls have written proofs and independent executable checks;
they are not claimed to be end-to-end Lean formalizations. The runner checks
memory and actual `lean`/`lake` executable basenames before each invocation.

## 7. What remains

The uniform support-recognition problem is now settled for all three
capacities. This is a structural extension of the preceding capacity-zero
recognition theorem, not yet a compensation theorem for losing supports.

The next concrete optimization question is whether the passing physical
class reduces to disjoint extreme offers with precisely identified shared
capacity-two activation cores. That reduction must preserve existing source
payments, mixed/beta competition, all original units, and each actual gate
fee exactly once. Mixed target directions and compensation after failed
handoffs also remain open. No universal 5/6 improvement is claimed, and the
11 October manuscript, public main, PR #3, shared CI and C4 work are unchanged.
