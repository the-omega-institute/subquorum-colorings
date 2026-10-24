# Canonical gate consumption and the least demand-preserving hull

21 October 2026. In any complete feasible mixed U/rotor source family, an
actual canonical side of an original positive U source is marked if and only
if its fixed original support is consumed into an endpoint. This identifies
each marked side with one unique original consumer, without choosing among
degree-four witnesses. It also removes the duplicate-mark correction from
legal shared-core gluing. The unrestricted allocation inequality and the
rectangular-grid triple equality remain open.

## Hypotheses and the local geometric theorem

Use the fixed original source catalogue and complete-source feasibility of
[the retention theorem](SOURCE_RETENTION_HORN_CLOSURE.md). Original endpoint
sets are pairwise disjoint; every original support has its fixed endpoint
anchor. Occupied original sets persist under retention. In a complete feasible
family every selected point has exactly one occupied neighbor, its original
anchor, and every endpoint has at least three occupied neighbors.

For one canonical positive side, normalize the lattice by an isometry so
its original support is t=(3,2), with anchor a=(3,1). Its three protectors
are (2,1),(4,1),(1,3), each having exactly three original occupied neighbors.
Their respective missing neighbors are p=(2,2), q=(4,2), r=(2,3).
These points are original blanks of this positive source. Thus the actual
degree-four marking condition is exactly that at least one of p,q,r is
occupied. Write u=(3,3). This fixed stencil is present for all allowed U
widths at least six and leg heights at least four; reflection supplies the
other side. Changing the global tile phase does not affect the argument.

First, each occupied trigger p,q,r must be an endpoint. Otherwise it is a
selected support of a foreign owner. It sees both its original anchor and
the retained positive protector. Those are distinct: equality, by unique
endpoint ownership, would make the support belong to the positive source,
contradicting its being an original blank. This violates feasibility.

If p or q is occupied, t has its own occupied anchor and an additional
occupied neighbor. Hence t cannot remain selected and must be consumed.
If r is occupied and t remains selected, both p and u must be blank, since
they are neighbors of t different from a. But r is an endpoint whose two
neighbors p,u are blank. Its occupied degree is at most two, a contradiction.
Thus every mark forces t to be an endpoint, including a mark witnessed
initially only at the guard.

Conversely, suppose t is an endpoint. If both p and q were blank, its only
possible occupied neighbors would be a,u, giving occupied degree at most
two. Thus p or q is occupied and the side is marked. In fact a marked side
always has a leg-protector witness, even when it also has a guard witness.
This proves the equivalence by local geometry, without enumeration.

## Fixed consumers and exact demand retention

Fix a complete feasible full family F. For each actually marked side s of
positive owner i, let j(s) be the unique endpoint owner of its fixed gate
t(s). The gate is an original support of i, so j(s) differs from i. For
every complete feasible retained subfamily I containing i, the theorem and
endpoint ownership give

    side s marked in I  iff  j(s) belongs to I.                 (1)

No sign condition on j(s) is used or follows: a gate consumer can itself
be a positive source. It need not be the owner of an earlier assigned
negative marked-side endpoint; those are different geometric roles.

An unmarked full-family side cannot become marked on restriction, since its
protector occupancy only decreases. Hence G(I) is exactly the number of
labelled incidences (i,s,j(s)) with both owners retained. Different sides
remain distinct labels even when they share a consumer. Multiple witnesses
for one side contribute one incidence, not multiple demands.

Seed all full-family positive owners and the unique gate consumers of all
their actual marked sides. The exact Horn closure H of this seed is feasible
and preserves all positives and all full-family side marks. Every other
feasible family preserving those data contains the seed by (1), and therefore
contains H by leastness of Horn closure. Thus H is the unique least
demand-preserving complete family, independent of witness choices.

Every feasible witness-seeded hull preserving demand contains H; some
witness choice is available entirely inside H, because H itself retains
each marked side. Closure of that choice therefore equals H. This does not
assert that every arbitrary witness choice produces the same larger hull.
The nine-source reserve obstruction already has exactly this canonical seed
and hull, so canonicalization does not restore reserve monotonicity.

## No duplicate-new-core marks and exact shared-core transfer

Let L,K be any two feasible retained families, C=L intersection K. Horn
intersection makes C feasible. If a common positive side is marked in both
L and K, its unique gate consumer lies in both, hence in C. The side was
therefore already marked in C. The duplicate-new-core count D is identically
zero for actual complete-source configurations, without a minimum-
counterexample assumption.

Under the no-exclusive-cross-endpoint-edge hypothesis of
[feasible-core gluing](FEASIBLE_CORE_SEPARATOR_TRANSFER.md), and assuming
the ordinary union F=L union K is itself complete feasible, every mark
incidence of F=L union K lies in at least one side. Indeed i and j(s)
have adjacent endpoints a(t(s)) and t(s); they cannot lie in opposite
exclusive parts. Their overlap is precisely the incidences inside C. Thus

    G(F)=G(L)+G(K)-G(C),
    mu(F)=mu(L)+mu(K)-mu(C).                                  (2)

Here the already established reserve identity subtracts actual R(C),
including its internal events and full-tile credits. All resources and all
labelled demands are counted once. For r exclusive branches with no endpoint
edge between different branches, the same proof gives

    mu(F)=sum_t mu(C union A_t)-(r-1)mu(C).                    (3)

For a single shared positive source, duplicate separator-side marks are
impossible. Equations (2)--(3) sharpen the earlier valid OR-mark formulas;
their formal duplicate corrections vanish under the physical hypotheses.

## Supermodularity of demand, and the remaining gap

For any fixed pair of owners, the indicator that both are retained is
supermodular under ordinary union and intersection. Sum over the fixed
labelled mark incidences. For feasible L,K the lattice join is the Horn
closure of their union; adding owners can only add incidences. Consequently

    G(L)+G(K) <= G(L intersection K)+G(cl(L union K)).          (4)

This statement concerns G only. The existing physical failures of reserve
and margin submodularity/supermodularity are unaffected.

In a source-minimal negative-margin allocation counterexample all proper
legal branches have nonnegative margin. To apply this to (3), assume at
least TWO exclusive A_t are nonempty, so every counted branch C union A_t
is proper. The valuation itself permits empty parts. Equation (3) then requires
(r-1)mu(C)>=1 for every such separator. A feasible zero-margin shared core
is excluded. A positive core margin may still be counted across several
branches, so this reduction does not supply the full compensation proof.
The connected nine-source family has unbounded canonical-hull reserve loss
but positive full margin 23. It refutes reserve comparison, not allocation.
The next target is a signed-loss inequality controlled by the actual
canonical hull margin, rather than by its reserve alone.

## Verification scope

`formal/SubQuorum/MarkedSideGateConsumption.lean` proves the normalized local
equivalence, the foreign-blank endpoint bridge, and unique-consumer retention.
These source-level statements have explicit hypotheses; the adapter from
the complete U catalogue, the labelled counting formulas and Horn-hull
consequences are written proofs here, not end-to-end Lean theorems.
`formal/SubQuorum/FeasibleCoreSeparator.lean` separately formalizes shared-
core feasibility and event cover/intersection, not the full square valuation.
Compilation and axiom evidence is recorded in the corresponding receipt.

Run `python3 develop/check_marked_side_gate_consumption.py` for actual
degree-based marks on legal complete restrictions, consumer retention,
canonical-hull inclusion, legal pair intersections and demand supermodularity.
All 32 phase/isometry images are checked. Restriction enumeration is
exhaustive only through nine owners; larger families and large pair spaces
use documented deterministic samples. These controls supplement the general
proof and do not establish the unrestricted allocation conjecture.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
