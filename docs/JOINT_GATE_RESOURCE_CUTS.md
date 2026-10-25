# Joint mixed-entrance and original-interval cuts

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The [boundary-split calculation](RESERVE_BOUNDARY_SPLIT_AND_JOINT_COMPENSATION.md)
assumed disjoint intermediate owners. We now allow different sources to meet
at the same capacity-one mixed entrance, and allow different entrances to
compete for the same original interval. An exact joint cut formula handles
both restrictions together. In its two-source-per-entrance specialization,
the source term is a count of tree components, including isolated sources.
This gives an explicit union inequality with each original unit counted once.

The result is a structural specialization of the established exact strand
flow and standard matching/min-cut facts, not a new general flow theorem.
It is proved for the interface hypotheses below, not for arbitrary frozen
grids. We verify its application to the COMPLETE original active-merger
board for every interval-availability subset. A separate four-source abstract
example satisfies all three natural marginal matching tests but fails their
joint packing. No physical embedding of that example is claimed. Universal
compensation and improvement of the 5/6 bound remain open.

## 1. Explicit interface hypotheses

Work on the original strand allocation model, before any cancellation.
All interval labels below are original resource identities, not access arcs.
Let S be the alpha sources. The following are assumptions to be established
from the full original geometry in each application.

1. Each paying route either uses a source-private alternative or enters one
   designated mixed gate g and ends at a supported available original
   interval in W(g). There are no other reachable whole-beta sinks, forks,
   or routes from one designated gate to another. Unreachable owners and
   betas may remain in the original network.
2. A gate includes its actual BP entrance and has capacity one. For every
   declared source-gate incidence there is a real entry route. Before that
   entrance, routes from DIFFERENT sources use disjoint mixed owners and
   BP tips. Gate exit branches are disjoint from other gates' exit branches
   and from all entry/private branches. Routes belonging to a single source
   may overlap: at most one will be used. Different routes through the SAME
   gate may overlap: at most one will be used. Consequently any distinct-
   source/distinct-gate/distinct-interval assignment lifts simultaneously
   to actual legal paths, with the stated route costs. Projection of every
   legal payment to such an assignment is also required by (1).
3. A source-private alternative uses an original interval or exclusive whole
   beta unavailable to every other source/gate. Alternatives for different
   sources are mutually disjoint and do not occupy another source's entry
   or any gate-exit branch. Let P consist of sources having such an available
   alternative, and let d_p be its minimum actual-link cost.
4. For the COST elimination only, d_p is no larger than every available
   gate-route cost from p. This is unnecessary for the value formula.

These conditions permit bent physical paths, occupied neighbouring bands,
and arbitrarily many original intervals shared between gates. They exclude
unmodelled shared entry chains and shared gate-exit owners. Complete freezing
alone does not imply these conditions. In particular, a BP has at most two
horizontal neighbours, but a feeder that has already merged sources can
violate the later two-source-per-gate assumption.

**Private-alternative elimination.** Some maximum payment prepays every p
in P by its private alternative. If a maximum packing leaves p unpaid, its
unused private alternative would increase the value, a contradiction. If it
pays p through a gate, replace just that path by the private path, releasing
its gate and interval. Hypotheses (2)--(3) ensure compatibility. Repeat for
all p. This preserves value, and under (4) never raises cost. Thus a minimum-
cost maximum packing with all these private prepayments exists. They spend
one actual resource each; gate support does not include those resources.

Put U=S minus P. Remove gates with no incidence to U. The remaining gate set
is G. Define E(g) subset U to be its nonempty source-incidence set, and retain
its available original interval set W(g). An interval in several W(g)'s is
still one unit. Let

    r_U(H) = maximum matching size between U and gates H,
    r_I(H) = maximum matching size between gates H and original intervals.

## 2. General joint rank formula, with proof

**Theorem 1.** Under hypotheses (1)--(3), the maximum payment is

    V = |P| + min_(H subset G) [ r_U(H) + r_I(G minus H) ].       (1)

Under (4), its minimum actual-link cost is sum_p d_p plus the minimum
entry/exit route cost of a maximum distinct-source/gate/interval packing
on U,G,I. In particular, paying all private alternatives is justified for
both objectives under the stated dominance assumption. Without that
assumption it is only a value-preserving reduction; the cost claim must
not be used.

**Proof.** After private prepayment, use a source--gate--interval network:
each source has capacity one, each gate is split by a capacity-one arc,
each original interval has one capacity-one sink arc, and all incidence
arcs have capacity |U|+1. Integral paths correspond to distinct triples.
Hypothesis (2) projects/lifts them to legal original strand paths; their
entry and exit tolls add to the number of actual links. A gate has only one
used path, so any pair of minimum entry/exit realizations for that gate can
be concatenated; cross-gate/source disjointness gives a simultaneous lift.

Let f be the maximum value of this network. For ANY H, split a maximum
packing's used gates into H and G minus H. The first part injects into U
and is bounded by r_U(H). The second injects into original intervals and
is bounded by r_I(G minus H). Hence f is at most the right side of (1).

For the reverse bound take an integral minimum cut. Its capacity is at most
|U|, so no |U|+1 incidence arc crosses it. Let X be the sources on its source
side. Write A,B for the gates whose entry/exit halves lie on that side.
We may normalize the cut so that

    N_G(X) subset A,    B subset A,
    every interval in N_I(B) lies on the source side.

Indeed an exit half on the source side whose entry is not can be moved to
the sink side without increasing the cut. Irrelevant entry halves and
intervals can likewise be removed, giving cut capacity

    |U minus X| + |A minus B| + |N_I(B)|.

Set H=G minus B. A source-to-H matching uses at most |U minus X| sources
outside X and at most |N_G(X) minus B| gates for sources inside X. Therefore

    r_U(H) <= |U minus X| + |A minus B|,
    r_I(G minus H)=r_I(B) <= |N_I(B)|.

Their sum is at most this minimum cut, which equals f. Together with the
first bound this proves equality, for arbitrary finite sets and supports.
The cost statement follows from private elimination and the same path
projection/lift. QED.

No enumeration or assumption of independent local surplus is used in this
proof. The two ranks must be evaluated at the SAME partition H of the
original gates; separately optimizing them would discard the joint cut.

## 3. Two-source gates give an explicit tree/union inequality

Assume additionally 1<=|E(g)|<=2 for every remaining gate. Make a multigraph
on U: a gate with two incident sources is an edge, and a gate with one is a
loop at that source. Keep parallel gates distinct. For H subset G let t(H)
be the number of TREE connected components of (U,H), counting isolated
vertices as trees. A component with a loop is not a tree.

**Lemma 2 (source rank).** r_U(H)=|U|-t(H).

**Proof.** A source/gate matching assigns each chosen edge to a different
incident vertex. On a tree with v vertices only v-1 edges exist, giving an
upper bound v-1; root the tree and assign each edge to its nonroot child to
attain it. On a connected non-tree component take a spanning tree plus one
additional edge (possibly a loop or parallel edge). Orient its unique cycle
cyclically, assigning each cycle edge to its head, and assign remaining
tree edges away from the cycle. This gives one different edge per vertex,
attaining the upper bound v. Components are disjoint; sum these ranks.
The isolated-vertex case has rank zero and contributes one to t(H). QED.

**Corollary 3 (exact joint deficit).** Write D=|S|-V. Then

    D = max_(H subset G) [ t(H) - r_I(G minus H) ].             (2)

Full payment is possible exactly when r_I(G minus H)>=t(H) for EVERY H.
Equivalently, eliminating the bipartite matching rank by its elementary
Hall deficiency formula,

    D = max_(H subset G, J subset G minus H)
          [t(H) - |G minus (H union J)| - |N_I(J)|].          (3)

Thus the explicit joint compensation condition is

    t(H) <= |G minus (H union J)| + |union_(g in J) W(g)|     (4)

for every disjoint H,J. Empty W(g)'s are allowed. The union counts the same
original interval once even when many gates support it. The other term
counts different mixed entrances, also once. The tree count is computed
on the ORIGINAL residual source set U, including its isolated vertices;
recomputing it only on nonisolated vertices would erase genuine demands.

For completeness, r_I(K)=min_(J subset K)(|K minus J|+|N_I(J)|): any matching
uses at most |K minus J| gates outside J and at most |N_I(J)| resources
inside J. A minimum cut of the ordinary bipartite matching network gives
an attaining J. Substituting this equality in (2) proves (3)--(4).

These are exact conditions for this interface class. To derive unrestricted
frozen-grid compensation one would still have to establish the interface
hypotheses or a more general reduction, then prove its joint union bounds
from freezing and geometry. We have not proved those missing assertions.

## 4. All three marginal matching tests can pass while the joint test fails

Use four sources a,b,c,d, five mixed gates 0,...,4 and four original
intervals x,y,z,w:

| Gate | Source incidence E(g) | Interval support W(g) |
| --- | --- | --- |
| 0 | a,b | x,y |
| 1 | b,c | z |
| 2 | c,a | z |
| 3 | d | x,w |
| 4 | d | y,w |

Every source has two incident gates, every gate has one or two incident
sources, and every interval is supported by exactly two gates. All supports
are nonempty. Three marginal tests have value FOUR:

- Source-to-gate: a->0,b->1,c->2,d->3.
- Gate-to-interval: 0->x,1->z,3->w,4->y.
- Source-to-reachable-interval: a->x,b->y,c->z,d->w.

Nevertheless joint payment is exactly THREE. Sources a,b,c can only use
gates 0,1,2. At most one can use gate0, and every other such payment must
use the SAME original z. Thus they together pay at most two; d pays at
most one. The packing a->0->x,b->1->z,d->4->y attains three.

Equation (2) detects this with H={3,4}: a,b,c are three isolated tree
components, d has loops and is not a tree component; hence t(H)=3, while
r_I({0,1,2})=2. Equation (3) can take J={1,2}: the remaining gate0 gives
one entrance, and N_I(J)={z} gives one interval, so 3>1+1.

This refutes the RULE that these three marginal matchings suffice jointly,
even with both two-incidence bounds. This interface is abstract: no planar
embedding, physical feasibility or complete freezing is asserted. It is not
a counterexample to the original grid inequality. Its purpose is to identify
exactly which joint geometric inequality the remaining proof must supply.

## 5. A necessary physical parity test, and an even-cycle obstruction

There is an additional geometric restriction worth retaining. Color a grid
point by its chessboard parity. Every actual matching edge and every PP band
partner edge changes color. An open original strand has alternately M/PP
edges, starting and ending with M, so has an odd number of edges and
opposite-colored terminals. Equivalently, a one-edge strand has opposite
colors, and extending it by one M edge and one PP edge preserves that fact.
This gives an arbitrary-length induction, also checked in Lean.

If one alpha enters gate g at one terminal and gate h at its OTHER terminal,
the gate BPs have opposite colors: both entry links change color, while the
two alpha tips have opposite colors. Thus, when each source's two gate
incidences use different original terminals, the graph on gates with a
source joining its two gates must be bipartite. In particular the triangle
on gates0,1,2 in the four-source example cannot use different terminals at
every source. This does not forbid two gates accessed from the SAME alpha
tip, and does not establish physical impossibility without that hypothesis.

Even imposing this necessary two-terminal parity does not make the marginal
tests sufficient. Use five sources a,b,c,d,e, six gates, five intervals
x,y,z,w,t, and this interface:

| Gate | Source incidence | Interval support |
| --- | --- | --- |
| 0 | a,b | x,y |
| 1 | b,c | z |
| 2 | c,d | w |
| 3 | d,a | z |
| 4 | e | x,t |
| 5 | e | y,t |

Give gates0,2,4 one color and gates1,3,5 the other. Each source has two gates
of opposite colors, so it passes the terminal parity test. Every gate has
one or two sources, and every interval has at most two supporting gates.
All marginal tests have value FIVE: source-to-gate uses0,1,2,3,4; gate-to-
interval can use0->x,1->z,2->w,4->t,5->y; source-to-interval can use
 a->x,b->y,c->z,d->w,e->t.

Joint payment is exactly FOUR. Sources a,b,c,d can use only gates0..3.
Gate0 contributes at most one, gates1/3 share z and contribute at most one
together, and gate2 contributes at most one. Source e contributes at most
one. The packing a->0->x,b->1->z,d->2->w,e->5->y attains four. The joint cut
uses H={4,5}, with four isolated trees and r_I({0,1,2,3})=3. In the union
form choose J={1,3}: the remaining gates0,2 give two distinct entrances and
the shared original z gives one interval, while four sources need payment.

This is a stronger abstract control, still not a physical frozen-grid
realization. It shows that source/gate degrees, two-owner interval supports,
and the necessary terminal-color condition together still leave a genuine
joint condition. A geometric proof must supply more than these tests.

## 6. Complete physical board, arbitrary available original intervals

Use the saved completely frozen 14x18
[active-merger board](../develop/fixtures/frozen_active_short_tail_merger.json),
with the four frozen left-cap states E,T,C,CB. Retain ALL original owners,
links, betas and interval identities; vary only interval availability A.
There are exactly two alpha sources, L=(3,1)/(5,6) and R=(3,15)/(5,12).

Both feed the same long mixed gate with BP(5,9), via different one-edge
mixed tails. Each entry costs two actual links. The gate's own support is
six old units at band5 columns10,12..16. Its further mixed exit branch costs
one more link and supports five old units at band5 columns1..5. Both sources
can reach that branch only THROUGH the common capacity-one gate. Neither
original non-cap beta is alpha-reachable. In CB, L additionally has its
exclusive empty-body beta at cost1. No two-arm beta fork is accessible.

There are five mutually disjoint interval classes:

| Class | Original identities | Cost |
| --- | --- | --- |
| Left direct | cap's 3/2/2/0 units in E/T/C/CB | L:0 |
| Left private relay | band1 columns5,6 | L:1 |
| Right direct | band1 columns11..14 and band2 column13 | R:0 |
| Gate direct | band5 columns10,12..16 | either source:2 |
| Gate tail | band5 columns1..5 | either source:3 |

Every other original interval is alpha-unreachable. These facts follow by
tracing all actual terminal links. The verifier reconstructs all of them
from the physical board and checks that no additional reachable transition
or shared intermediate owner is omitted. The two source-private branches
and the two gate-entry tails are disjoint except at their own source; the
only cross-source meeting is the displayed common gate and its exit tail.

Let ell=0 when A meets Left direct, else1 when A meets Left private relay
or the cap is CB, else infinity. Let r=0 when A meets Right direct, else
infinity. Set h=2 when A meets Gate direct, else3 when A meets Gate tail,
else infinity. Put p=number of finite entries among ell,r, and d=sum of
those finite entries. Private costs are at most1, while any gate payment
costs at least2, verifying hypothesis (4).

**Proposition 4 (all original availability subsets).** In both ordinary and
full models,

    V = p + min(2-p, 1 if h is finite else 0),
    c = d + h if p<2 and h is finite, else d.                  (5)

**Proof.** Apply private elimination. The remaining graph has 2-p sources
and one gate with capacity one. If it has any available interval, exactly
one remaining source can use it; otherwise none can. The two real entry
chains give cost2, or3 if only the tail supports an available interval.
No alternate route bypasses the shared gate, by the complete reachable
classification. Different private/gate resources and route branches ensure
a compatible lift. Unreachable original betas cannot create forks, so the
ordinary/full optima coincide for this board. This proves (5) for every A,
not just tested subsets. QED.

In E/T/C, making all ELEVEN gate-reachable interval units available while
reserving all private alternatives still gives only V1/c2. Releasing more
of those eleven units cannot repair the missing source: the obstruction is
the entrance. Releasing ONE source-private unit repairs it, giving V2/c2
for a direct private unit (or V2/c3 for L's one-link private alternative).
In CB, even that gate-only interval pool has V2/c3 because L has its private
whole beta. Full pools pay V2/c0 in E/T/C and V2/c1 in CB. These are exact
restricted-availability statements, not physical-deletion counterexamples.

## 7. Verification, formal scope, and next mathematical task

Run from the repository root:

    python3 develop/check_joint_gate_resource_cuts.py \
      --output output/joint-gate-resource-cut-validation.json

The independent controls compare the tree/rank formula with the existing
full strand flow and exhaustive primitive packing. Systematic three-source
multigraphs include loops and parallel gates; randomized controls include
empty and shared supports. Both abstract obstructions are checked against
all three marginal matchings and a joint packing; the second also passes
the necessary distinct-terminal gate-color test. Physical tests retain
every original owner/link/beta, test class availability, every singleton and
pair of original identities, and larger random subsets on all four caps.
The arbitrary-size result is the cut/tree proof above, not these finite
computations. The saved receipt contains 6,834 joint-cut/independent
abstract-pack models and 6,834 private-prepayment controls, plus 6,883 complete-
board availability models checked against 13,766 independent ordinary/full
primitive packs. All passed.

The accompanying scoped Lean file checks a nonreusing partition encoding,
its injectivity consequences, arbitrary-length strand color parity,
the distinct-terminal gate-color consequence and triangle exclusion, and
the four-source obstruction with matching
witnesses for the three marginal tests and a joint lower witness. It does
not formalize the full max-flow/min-cut theorem, the graph rank lemma, or
the physical support adapter; those are written proofs and Python checks.
All 12 audited Lean declarations pass on local Lean4.33.0, using only
propext and Quot.sound (no sorry/native execution). Before the one-process
Lean check, the local16GiB machine had44% system-wide free memory and no
lean/lake process under the comm-basename check. No new external review is claimed.

The next geometric problem is now explicit: which original frozen mixed-gate
interfaces force (4) simultaneously? Separate gate counts, interval counts,
or source-to-resource Hall matchings cannot establish it. For arbitrary
frozen boards, shared entry chains, reachable beta-body forks and overlapping
exit branches additionally require the complete resource-cut model. No
change to the submitted manuscript or unrestricted 5/6 bound follows yet.
