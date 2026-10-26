# Mixed relays and beta forks: exact shared fees by dual resource parity

**Protected-path continuation:** [extreme-resource linear corridors](PROTECTED_LINEAR_CORRIDORS.md)
give a geometric class with arbitrarily many original units and overlapping
route prerequisites that reduces to one polynomial min-cost fork flow.
Simultaneous endpoint privatization makes the retained prerequisites disjoint;
a one-unit corridor retains one shared output. This does not supply a parity
algorithm for arbitrary instances of the theorem below.

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

The [capacity-two gate-bundle theorem](CAPACITY_TWO_GATE_BUNDLES.md) required
direct residual alpha sources and an independent fixed mixed/beta baseline.
We remove that restriction. The entire competing mixed-relay and beta-fork
network now participates in the optimization. Independently activated groups
of at most two original intervals, with one fee per group, give an exact
**weighted matroid parity problem in the dual output-resource matroid**.
The reduction includes the two separate physical BP gates of each beta,
one whole-beta output, and all shared mixed capacity-one gates.

This is an application of classical flow matroids and matroid parity, not
a new general matroid theorem or a priority claim. It extends the exact
adapter class, but does not by itself give a polynomial algorithm from a
rank oracle, a universal compensation lemma, or an improvement to the
universal 5/6 bound. Section 8 states these limits precisely.

## 1. Full support-only adapter

Fix the original owners, TP/BP types, actual terminal links, and all unit
capacities from [the exact whole-support fork flow](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
Alpha sources can enter arbitrary mixed relays and beta tips; all owners
can have their prescribed whole-owner interval supports. No separation into
baseline and residual owners is assumed. Keep every original interval ID,
including currently unsupported intervals, and one whole-beta output per beta.

Partition a subset of the original intervals into disjoint nonempty groups
R_j of size one or two. All remaining intervals are free. For each group:

* When inactive, none of its intervals is supported by any owner.
* When active, each interval has a fixed, arbitrary set of supporting owners,
  including mixed owners or beta bodies. All nongroup incidences are fixed.
* Groups are independently activatable, with nonnegative integer fees c_j.
  Activating j costs c_j once, even if both its intervals are used.

These are assumptions on a physical adapter, not consequences of disjoint
tiles. One sufficient implementation uses nonempty pairwise-disjoint sets
G_j of prerequisite gates: every primitive gate subset is feasible; owners,
types, links and inventory stay fixed; group j gains exactly its declared
support if and only if all of G_j is open; partial prerequisites have no
other effect; and no old support is lost. The fee c_j is the sum of its gate
fees. Delete every incomplete prerequisite set from a candidate operation:
it changes no support and cannot increase the cost. Thus optimal operations
reduce to independent whole groups with additive once-per-group fees.

For a physical forest replacement, it suffices to prove a simultaneous
bijection between each group's unsupported old original units and its new
units in every state. This is an inventory-preserving identification, not
creation of new units. Unsupported inactive group units can equivalently
be deleted from the network. The five-gate example below checks this contract
against complete original forest decompositions for every operation subset.

Let J be the group index set, C = sum_j c_j, and N the all-enabled network.
Let r be its maximum integral flow value. By the full fork-flow theorem,
r is the maximum physical compensation over all activation choices.

## 2. The output-resource matroid

Let U consist of all interval output labels, one private whole-beta output
label for every beta, and a dummy label d_j for each one-interval group.
Dummy labels have no incident path and are loops, not physical resources.
They only pad every group to a pair P_j:

    P_j = {two interval labels}             if |R_j| = 2,
    P_j = {the interval label, d_j}         if |R_j| = 1.

The pairs are disjoint. Free interval labels and whole-beta labels remain
unpaired. Define rho(S) to be the maximum integral flow in N with only
output-sink arcs labelled in S enabled; dummy loops supply no such arc.
Every real output-sink arc has capacity one. Write r = rho(U).

**Lemma 1 (resource linkability).** The sets S satisfying rho(S)=|S| are
the independent sets of a matroid M on U, and rho is its rank function.

**Proof.** The empty set is independent. An independent S has an integral
flow using each of its outputs exactly once. Decompose into paths and discard
paths ending outside a subset, proving hereditary independence.

Let S,T be independent and |S|<|T|. Restrict available output arcs to S union T.
Start from a flow of value |S| paying all S outputs. A flow of value |T|
exists, so a residual augmenting s--t path exists. Choose it simple and stop
at its first visit to t. It cannot traverse a reverse output-sink arc: that
would require leaving t. Hence no old S output is lost, and the new final
output is some e in T minus S. Its unit sink capacity makes S union {e}
independent. This is the matroid exchange axiom.

For arbitrary S, a maximum integral flow ends at rho(S) distinct outputs
in S, yielding an independent subset of that size. Conversely, an independent
subset of S cannot have size exceeding rho(S). Thus the matroid rank is rho.
Loops are automatically excluded. Finite capacities cause no change to this
argument. ∎

This is a standard flow-linkability matroid (a gammoid): expanding integer
arc capacities and subdividing capacity arcs gives the usual vertex-gate
model. The elementary exchange proof suffices here; we require no algebraic
representation or external parity algorithm in order to establish the result.

**Beta identity caution.** A general independent output set is a network
object. Two paths through different BP tips may both end at supported
intervals of one beta, even when its whole-beta output is not selected.
Beta normalization changes one interval output to that unused whole-beta
output. Therefore arbitrary output bases do not have an identity-preserving
bijection with normalized physical packs. The proof below uses deletion
of closed *interval groups* and retains every whole-beta output, so the
normalization is always allowed. It never introduces a deleted interval.

## 3. Exact parity and fee theorem

For a closed group set T subset J put X_T = union_(j in T) P_j. Its real
labels are exactly the closed intervals; any other labels in X_T are dummy
loops. Let M* be the dual of M. Its rank formula is

    rho*(X) = |X| - r + rho(U minus X).                         (1)

In particular X is independent in M* if and only if rho(U minus X)=r.

**Theorem 2 (mixed-network shared-fee compensation).** Under Section 1,
the minimum activation fee among all states attaining maximum payment r is

    f* = C - max { sum_(j in T) c_j :
                   X_T is independent in M* }.                (2)

This is weighted matroid parity on the disjoint pairs P_j in M*. Ground
elements not in any pair remain in the dual matroid. A dummy is a loop of
M and a coloop of M*, so padding a one-unit group adds no false restriction.

**Proof.** For a state with exactly J minus T active, close the interval
outputs of T in the all-enabled network. Inactive intervals have no incoming
support. Deleting those unsupported intervals has exactly the same maximum
flow value as removing their sink arcs. All other owner gates, supports and
outputs are identical. Thus the maximum payment in that state is

    rho(U minus X_T).                                          (3)

The full fork-flow equivalence applies to this deletion network. Normalize
each used beta by giving it its private whole-beta unit first; that output
has not been deleted. This preserves every paid alpha source, never introduces
a closed interval, and can only release an open interval. Thus (3) is the
physical maximum, regardless of the output identities of the initial flow.

By (1), (3) equals r precisely for the parity-feasible closed sets in (2).
The activation fee in that state is exactly

    sum_(j not in T) c_j = C - sum_(j in T) c_j.

Taking minima on the left and maxima of saved fees on the right proves (2)
in both directions. Each group is charged once; each actual interval is one
capacity-one output; all shared routing capacities remain in M. No independent
per-path or per-component reserves have been added. ∎

The theorem also gives the exact budget test: maximum payment r is attainable
within budget b if and only if the maximum parity saving is at least C-b.
The all-enabled flow itself determines r. If r is below the required demand,
no activation subset in this adapter can cure that routing deficit.

## 4. One cut ledger for cross-component compensation

For each s--t cut Z of the all-enabled network let c(Z) be its capacity,
and I(Z) the original interval labels whose output vertices are on the source
side. Use the network with fixed source capacities, mixed gates, distinct
beta BP gates, whole-beta sinks, and support/link arcs. Dummy loops have no
cut arc. For a closed T, max-flow/min-cut rewrites (3) exactly as

    rho(U minus X_T)
      = min_Z [ c(Z) - sum_(j in T) |R_j intersect I(Z)| ].      (4)

Consequently T is parity-feasible if and only if every cut satisfies

    sum_(j in T) |R_j intersect I(Z)| <= c(Z) - r.               (5)

**Proof.** Only closed original interval-to-sink arcs are removed, each of
capacity one. Each such arc crosses Z precisely when its interval output
is on the source side. This proves (4). The value cannot exceed r, so it
equals r precisely when all changed cut capacities are at least r. ∎

Equation (5) is a uniform cross-component accounting condition. It retains
shared mixed bottlenecks and actual beta entries inside c(Z); it charges each
original interval ID once, however many components support it. The same
resource may constrain several cuts, but this is simultaneous feasibility,
not a sum of independent reserve credits. No cut slack is separately assigned
to multiple demands. This extends the earlier [individual interval release
formula](SIMULTANEOUS_INTERVAL_RELEASE_AND_PHYSICAL_CIRCUITS.md) to weighted
all-or-nothing release of disjoint pairs.

## 5. Retaining old sources costs no extra activation fee

**Corollary 3.** Let P be any alpha source set payable with no optional
group activated. Every fee-optimal maximum-payment activation state has a
packing of value r retaining all of P. Its activation fee is the same f*.

**Proof.** That state contains the entire old zero-activation network. Start
from an old integral flow paying precisely P (discard other source paths
if necessary). Augment it to value r within the chosen state. A simple
augmenting path cannot use a reverse source arc, because that would revisit
s. Hence each initially used unit source arc remains saturated. Remove any
circulations and apply beta normalization; both preserve source identities
and use no closed output. The activation state and its fee are unchanged. ∎

P need not be a maximum old source set, and the chosen optimal state need
not depend on P. The conclusion does not retain the old routes, old interval
assignments, or old minimum number of links. After fixing a fee-optimal
state one can minimize links inside that state; arbitrary tie-breaking in
weighted parity does not prove a globally optimal *third* objective over
all fee-optimal states.

## 6. Two explicit failed shortcuts

**Reachability matching ignores a mixed gate.** Take alpha sources a_0,a_1,
one mixed owner m, links from each alpha TP to m's same actual BP, and two
intervals supported by m. Both sources individually reach both intervals.
An ordinary source--interval reachability matching predicts two payments.
The capacity-one mixed gate permits only one. The resource rank and Theorem 2
give one. With a beta in place of m, different actual BP tips permit two
payments (whole beta plus one interval); the same BP tip still permits one.

**Closed groups do not form a matroid.** Take two direct sources a,b. A group
0 of two units supports a and b separately; singleton group 1 supports only
a, singleton group 2 only b. No other support exists. Maximum payment is two.
Both closed sets {0} and {1,2} retain it, but neither {0,1} nor {0,2} does.
The exchange axiom on *group indices* fails. With fees (3,2,2), a descending
saved-fee greedy rule closes group 0 first, saves 3 and pays 4 to open groups
1,2. The optimum closes 1,2, saves 4 and pays 3 to open group 0.

This is a counterexample to that greedy rule, not to the parity theorem or
to the target grid inequality. It also explains why simply using ordinary
weighted matroid greedy on group indices cannot replace parity optimization.

## 7. A complete frozen adapter with optional mixed routing

Start from the 16×58 [two-module capacity-two board](CAPACITY_TWO_GATE_BUNDLES.md).
Keep T=166, matching M=70, all 140 original endpoints strictly frozen in the
same eleven waves, alpha=4, beta=4, mixed=10, and all 228 original interval
units. In addition to the previous three V-oriented gates, set (4,12) and
(4,44) to V. These remove the former two fixed mixed-owner interval supports.
The zero-activation state now pays **zero**, not the previous fixed baseline two.

The five independent P-free single-tile gates have these activation effects:

| Gate j | Tile V→H | Original units | Active supporting owners |
|---|---|---:|---|
| 0 | (2,28) | 2 | a_L and a_R, for either unit |
| 1 | (10,16) | 1 | a_L |
| 2 | (10,40) | 1 | a_R |
| 3 | (4,12) | 1 | mixed z_L |
| 4 | (4,44) | 1 | mixed z_R |

All six old group units are unsupported. Each group replaces the same
number of old units by its declared active units, simultaneously for every
subset. The other 222 original units remain in the pool with fixed support.
No interval restriction is substituted for the raw inventory.

The only external links leaving these four alpha sources or the two z owners
are b_L TP (5,17) → z_L BP (5,16), and b_R TP (5,40) → z_R BP (5,41).
Neither b has direct interval support. Each z is genuinely mixed and has
no onward link. Thus gates 3 and 4 are part of the optional shared-resource
optimization, and paying b_L or b_R necessarily uses its mixed gate.

For selected gate set F the exact values, with independently checked minimum
link count, are

    direct(F) = 2  if 0 in F or {1,2} subset F,
                1  if neither holds and F intersects {1,2},
                0  otherwise;
    V(F) = direct(F) + 1_(3 in F) + 1_(4 in F),
    links(F) = 1_(3 in F) + 1_(4 in F).

In particular the all-enabled payment is four, using two mixed links.
For fees (3,2,2,4,5), the minimum full-payment fee is 3+4+5=12;
activating the two private direct groups instead costs 2+2+4+5=13.
For fees (5,1,1,0,0), the private direct pair is preferable and full payment
costs two. One shared group can still supply two distinct original units,
but one mixed gate cannot multiply its capacity.

## 8. Verification, algorithmic scope, and the remaining geometric step

The standard-library validator [check_mixed_resource_parity.py](../develop/check_mixed_resource_parity.py)
uses an independent Edmonds--Karp output-rank oracle. It compares the parity
formula to the existing full minimum-cost fork flow and independent primitive
packing DP, checks matroid rank/exchange and dual deletion on complete small
ground sets, checks every cut in the small controls, and retains every old
feasible source subset within the *same* chosen fee-optimal state. It also
checks the complete 32-state frozen physical adapter and four cost profiles.
The checked counts and controls are in [the validation record](../output/mixed-resource-parity-validation.json).
Finite enumeration tests these statements; Sections 2–5 are their general proofs.

The scoped [Lean kernel](../formal/SubQuorum/ResourceDualParity.lean) checks the
dual-rank/deletion equivalence and the two directions of transferring optimal
saved fees to optimal spent fees. Its validation record states the exact
formal boundary. The flow exchange theorem, physical fork normalization,
matroid representation, parity reduction's adapter and grid geometry remain
written proofs with independent executable checks, not end-to-end Lean.

Weighted matroid parity is a classical problem. S. Iwata and Y. Kobayashi,
“A Weighted Linear Matroid Parity Algorithm,” STOC 2017,
[doi:10.1145/3055399.3055436](https://doi.org/10.1145/3055399.3055436), and its
2021 journal version [doi:10.1137/17M1141709](https://doi.org/10.1137/17M1141709),
give the relevant weighted *linear-representation* algorithmic context.
A maximum-flow rank oracle alone is not an explicit faithful linear
representation with a justified construction cost. We do **not** infer a
deterministic polynomial implementation for the present mixed extension from
the rank oracle. The previous direct-source subclass already has its separate
ordinary weighted-matching polynomial algorithm; it remains valid.

The present extension requires disjoint additive prerequisite bundles and
support-only activation. It does not cover destructive support losses,
overlapping prerequisite gate costs, or operations that change the mixed/BP
routing capacities. Nor does it prove that arbitrary frozen grids admit this
adapter, that all-enabled payment equals alpha, or that every cut satisfies
a universal geometric compensation estimate. Those are the remaining steps
toward improving 5/6. The contribution here is the exact shared-fee criterion
with arbitrary fixed mixed/beta competition, and the precise obstruction to
the tempting group-greedy simplification.

The 11 October manuscript, public main, PR #3 and shared CI are preserved.
No email operation is part of this research continuation.
