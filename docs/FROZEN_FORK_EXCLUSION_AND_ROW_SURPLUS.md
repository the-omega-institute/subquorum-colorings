# Frozen fork exclusion, exact row surplus and mixed-target avoidance

25 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We strengthen the missing-port BP-terminal injection by a local freezing
obstruction. Its row graph has only isolated edges and BP-ended paths.
This gives an exact surplus formula for every subset of missing tips, a
sharpened weighted owner inequality, and an optimal choice of terminal
injection minimizing mixed targets. Surplus BP terminals are not new unit
credits. This does not prove universal compensation or improve the global
5/6 bound.

## 1. Setting and a forbidden local fork

Use the feasible pair (T,M), aligned matching-closed band packet and original
PP strands of `INTERVAL_CONNECTOR_CYCLES_AND_MISSING_PORTS.md`. Every original
endpoint is completely frozen by the actual matching: an endpoint freezes
when two distinct nonmate neighbors are selected, or are endpoints whose
actual mates froze earlier. The full certificate may use arbitrary vertices
outside the packet. An alpha strand has two TP tips, a beta strand two BP
tips, and a mixed strand one of each. A tip is *missing* when it has no
immediately adjacent BB column in its own band. These are original types,
not types produced by later cancellations.

**Fork exclusion.** Suppose original alpha TP tips u,w share a horizontal
BP neighbor v, so their columns are consecutive u,v,w in one row. Neither
outer horizontal neighbor of u,w can be selected in a fully frozen pair.
The tips u,w may belong to the same alpha; no distinct-owner hypothesis is
needed for this local statement.

**Proof.** Reflect vertically and translate so that

    u=(r,c-1), v=(r,c), w=(r,c+1),
    mate(u)=(r+1,c-1), mate(w)=(r+1,c+1).

An original alpha TP tip has vertical actual mate across the band boundary:
a horizontal mate would be a BP tip, terminating a mixed strand instead.
The within-band neighbors above u,w are selected, and the site above v is
blank. Since u,w are already vertically matched, v must have actual mate
b=(r+1,c). Suppose z=(r,c-2) is selected and write a=mate(u). Feasibility
at z, which already sees u, forces (r+1,c-2) blank.

The nonempty pair U={v,a} has no possible first freezing event. The only
nonmate occupied neighbors of v are u,w; freezing v requires a earlier.
The nonmate neighbors of a are a blank site on its left, b on its right,
and at most one further site below. Even if that last site supplies a
witness, freezing a requires b retained, hence v earlier. These two strict
dependencies contradict either a finite freezing order or induction on
freezing stages. Reflect horizontally to exclude a selected outer neighbor
of w. Exterior data cannot add further neighbors to v or supply a second
non-b witness to a. This proves the claim. ∎

In particular, if either fork tip is missing, its outer horizontal neighbor
is occupied and is not selected; it is another BP tip. The BP label follows
because the selected within-band partner of the TP tip forces the
within-band partner of that horizontal endpoint blank.

## 2. Checkerboard ownership is essential

Every open original PP strand has q actual matching edges alternating with
q-1 within-band PP edges. Expanding it in the physical grid gives a path
of odd length 2q-1. Thus its two tips have opposite checkerboard colors.
This also covers a strand with no internal PP column. Pure cycles are
irrelevant. Consequently, different BP tips at the same column parity in
one physical row have different original owners: a beta cannot own both,
and a mixed strand has only one BP tip.

At a fork whose left tip is missing, its new outer BP and the central BP
therefore have different beta/mixed owners. If both tips are missing, the
three BP owners are pairwise distinct. In particular a missing fork alpha
cannot have all its horizontal BP neighbors owned by the one central beta.
This explains the failed bounded discovery templates with that restriction;
the general exclusion follows from Section 1 and parity, not from UNSAT.

## 3. Exact classification for every subset of missing tips

Let X be ANY subset of missing original alpha TP tips. Let N(X) consist
of ALL horizontally adjacent BP tips, and form H_X from these adjacencies.
Every X vertex has degree one or two, every BP vertex at most two, and
components are finite paths along a physical row. The degree lower bound
uses full freezing as in `FROZEN_MISSING_PORT_BP_TERMINAL_INJECTION.md`:
a missing tip has both horizontal neighbors occupied; if both were selected,
its vertical mate would have occupied degree at most two and could not freeze.

**Row classification and surplus theorem.** Every component of H_X is either
an isolated X--BP edge or a BP--BP path. If c(X) counts the latter, then

    |N(X)| = |X| + c(X).                                      (1)

Moreover BP owners are distinct within each component.

**Proof.** If an X vertex has degree one, its other horizontal neighbor is
selected. Its BP neighbor cannot also be adjacent to another X vertex,
by fork exclusion. Both ends of this component therefore have degree one,
so the component is an isolated edge. Every other component has all its X
vertices of degree two and hence both endpoints BP. Each isolated edge has
equal part sizes; each BP-ended path has exactly one extra BP. Summing gives
(1). BP positions in any such row path have the same checkerboard color,
so Section 2 proves distinct ownership within the component. The argument
uses only the chosen X and keeps all its BP neighbors, so applies to every
subset without an induced-subgraph coverage assumption. ∎

A beta may have tips in two DIFFERENT components, with opposite colors;
it must still be counted only once as a unit resource. We do not assert
distinct ownership between components.

## 4. Sharpened weighted owner inequality and scalar budget

For any set Y of original alphas whose BOTH tips are missing, use X consisting
of those 2|Y| tips. Let N_beta(Y), N_mixed(Y) be the distinct original owners
of the BP tips in N(X), and abbreviate c(Y)=c(X). Each beta contributes at
most two tips and each mixed owner at most one. Equation (1) implies

    2|Y| + c(Y) <= 2|N_beta(Y)| + |N_mixed(Y)|.                (2)

This is a weighted owner inequality for every Y, stronger than the same
bound without c. It does not identify two beta tips as two resources.

If all k original alphas have both tips missing, let b,q count their
neighboring beta,mixed owners, c=c(X), and let I be the number of distinct
original unmarked interval resource units. Then (2) yields, in integers,

    I+b-k >= I + ceil((c-q)/2),
    2(I+b-k) >= 2I+c-q.                                      (3)

Thus q<=2I+c is a sufficient condition for this scalar budget to be
nonnegative. Other beta owners can only increase the budget. Equation (3)
requires the stated all-missing hypothesis; partially ported alphas need
separate handling. It is a scalar counting conclusion, not a construction
of admissible compensation routes. Interval resources must retain the
original unit ownership used in the flow model. If using connector-component
resources instead, supply the corresponding ledger rather than reusing I.

The term c measures extra terminals already contained in N(X); it is NOT
an additional supply to add to b or I. In particular no BP-ended row
component is automatically a new beta or an interval reserve.

## 5. Exact minimum number of mixed targets in a terminal injection

Let q_X be the number of mixed BP tips in N(X), and let c_m(X) be the number
of BP-ended components containing at least one mixed BP tip. Then among
all injections X -> N(X) using horizontal edges, the exact minimum number
of mixed targets used is

    q_X - c_m(X).                                            (4)

**Proof.** An isolated edge forces its BP target. In a BP-ended path with a
X vertices and a+1 BP vertices, any single prescribed BP vertex may be
omitted: enumerate the path D_0,A_1,D_1,...,A_a,D_a; to omit D_j, match
A_i to D_(i-1) for i<=j and to D_i for i>j. Every image is adjacent and
these images are distinct. Exactly one BP is unused in every full injection
on this component. If it contains a mixed tip, omit one such tip, saving
one mixed target; otherwise none can be saved. Components are disjoint,
so summation proves both the lower bound and its attainment. ∎

For all-unported alphas, apply this injection to both tips of every alpha.
In the previous owner graph F, alpha degree is two, beta degree at most two,
and mixed degree at most one. Its residual mixed-ended demand paths then
satisfy

    t <= floor((q_X-c_m(X))/2).                               (5)

Here q_X counts ALL neighboring mixed tips, whereas the earlier t bound
counted mixed tips USED by its chosen injection. Formula (4) is the precise
bridge. This minimizes mixed terminal use; it need not minimize t or the
cost of a later route packing. Establishing access from the remaining
mixed-ended paths to distinct original reserves remains open.

## 6. A full geometric compensation class, with an explicit application

**Mixed-avoidance compensation corollary.** Suppose both tips of EVERY
original alpha are missing, no isolated row edge has a mixed BP target,
and every BP-ended row component contains at most one mixed BP target.
Then all k alpha demands can be cancelled against k distinct original beta
strands using exactly k horizontal links. No interval or mixed gate is used.
Consequently the packet ledger has S>=B, with B the marked boundary budget.

**Proof.** The hypotheses give q_X=c_m(X), even when q_X is arbitrarily
large. Formula (4) supplies an injection using only beta BP tips. Its owner
multigraph has alpha degree two and beta degree at most two, counting
multiplicity. Each path has both endpoints beta, while each cycle is even;
choose alternating edges to match every alpha to a distinct beta. Equivalently
2|Y| witness incidences enter at most 2|N_beta(Y)| slots for every Y,
so Hall applies. Choose one witnessed terminal link for each matched pair.
Different alpha and beta owners give disjoint original tips and disjoint
owner supports. Each link removes exactly one alpha and one beta; no beta
is spent twice. Thus beta>=k. The original ledger S=L+beta-k and L>=B yield
S>=B. This proves the conditional packet bound and the actual allocation. ∎

For the frozen no-direct-access fixture from
`FIRST_DESTINATION_ALLOCATION_AND_UNPORTED_GATE.md`, the four missing tips
are (3,6),(5,9),(5,11),(10,11). Their row graph has three BP-ended components,
with respectively 1,2,1 alpha tips and 2,3,2 BP tips. There are three mixed
BP targets, one per component: c=q_X=c_m=3. The corollary therefore supplies
two beta cancellations with no mixed relay, using only horizontal original
links. One choice is

    alpha 1: (3,6)--(3,7), into beta owner 2;
    alpha 4: (5,11)--(5,12), into beta owner 5.

The two beta owners are different. This derives its two-link full compensation
from the new geometric classification; the earlier full-network verifier
already established that numerical optimum. The earlier shared-mixed
projection still pays at most one, so its local-rule counterexample survives.
The new result explains a systematic way to avoid that projection's bottleneck.

## 7. Explicit nonfrozen control and reproducibility

On an 8-by-8 board take vertical matching edges

    (3,2)--(4,2), (3,3)--(4,3), (3,4)--(4,4)

and selections {(2,2),(2,4),(3,1),(5,2),(5,4)}; all other sites are blank.
This is feasible and every endpoint has occupied degree at least three.
Its upper row has the fork with outer selected site (3,1), but
U={(3,3),(4,2)} never freezes, exactly as Section 1 predicts. It refutes
replacement of full freezing by degree-three terminality in the fork
claim. It does not refute the target grid inequality.

The checker `develop/check_frozen_fork_surplus.py` reconstructs original
strands and missing-tip adjacency from fully frozen physical configurations,
checks fork exclusion and checkerboard ownership, checks (1) on subsets and
(2) on alpha-owner subsets, constructs the injection in (4), and compares
its cost against an independent subset dynamic program. Finite checks
corroborate the proofs; they do not establish the general statements.
The deterministic run passes 859 frozen geometry controls (including the
480 carried physical controls), 18 observed forks, 1550 tip-subset checks
with independent minimum-cost comparisons, 1047 weighted owner-subset checks
and 400 optimized beta-deficit checks. The complete beta-only class has 273
controls, nine with nonempty alpha demands. The canonical unported shared-gate
fixture has c=q_X=c_m=3 and the two explicit links in Section 6. Results are
in `output/frozen-fork-surplus-validation.json`.

A fully frozen shared-beta SAT discovery fixture is preserved separately:
it has full payment two and protected payment two and does not demonstrate
a necessity for exchange gates. Restricted-template UNSAT receipts are
bounded discovery results only.

The companion Lean file formalizes the closed two-witness obstruction for
the inductive freezing stages, its two-vertex fork specialization, and
weighted-budget arithmetic. Grid-to-dependency geometry, row classification,
parity and the optimal injection remain the written proofs above; no full
formalization of these geometric theorems is claimed. Local Lean 4.33.0
passes all four theorems without warnings, sorry or native evaluation. The
two freezing-obstruction theorems use no axioms; the arithmetic theorems use
only propext and Quot.sound. The execution receipt and explicit limits are
in `output/frozen-fork-surplus-lean-validation.json`. This note has not had
an independent external mathematical review.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
