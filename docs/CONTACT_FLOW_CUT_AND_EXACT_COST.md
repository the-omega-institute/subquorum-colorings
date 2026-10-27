# Arbitrary contact coverage: an exact flow cut and a physical cost model

For a prescribed pool of vertex-disjoint square contacts, optimizing terminal
coverage does NOT require enumerating its subsets. A unit-capacity directed
flow gives the exact smallest remaining TT count, including arbitrary shared
original components and closed P-only cycles. The cut obstruction counts
actual directed fragments, rather than independently successful relays.

The full payment cost has a separate exact two-colour integral-flow model.
We do not identify it with the cost of the ordinary coverage flow or claim a
polynomial algorithm for that weighted model. These are fixed-M,
fixed-contact-pool theorems, not universal geometric coverage or a new 5/6 bound.

## 1. Hypotheses and the fragment network

Use the hypotheses of the [contact-network theorem](CONTACT_NETWORK_CYCLE_CREDIT.md):
an actual feasible partial matching M on a bipartite rectangular grid, a full
auxiliary matching N, and a POOL of e unit squares with pairwise disjoint
vertex supports. Each square's old N edges lie on two distinct original
terminal paths of M+N. The actual matching and T are fixed. Contacts are
optional; any subset may be switched. Untouched original doubled edges and
P-only cycles are outside the network and cancel from payment comparisons.

Include all n original terminal paths. Orient them from black Q to white Q.
Cut at EVERY candidate N edge. This partitions their vertices and physical M
edges into n+2e fragments, including zero-M or singleton-terminal fragments.
Compress each square to one vertex v_g. A fragment is a directed arc from its
previous cut (or its own black terminal) to its next cut (or white terminal).
Parallel arcs are retained as distinct physical fragments. Assign arc R the
weight w_R=|M intersect R|. Each square vertex has exactly two incoming and
two outgoing arcs. The two possible local bijections are precisely keeping
the old N edges or switching that square; there is no third constraint.

Let B_T be the number of black terminals in T. Add a source s with a
capacity-one arc to each black T terminal, and a sink z with a capacity-one
arc from each white H terminal. Every fragment arc has capacity one.
Other terminals have no super-source/sink edge. Let F be the maximum s-z
flow value. All capacities are integers, so an integral maximum exists.

## 2. Exact optimal terminal coverage

**Theorem.** Among ALL subsets of the prescribed contacts, the minimum
remaining TT count is

    delta = B_T - F.                                      (1)

In particular every selected vertex has a disjoint alternating payment to a
hole iff F=B_T. HH components may remain; they are not required to become TH.
If original counts are (a,b,t), optimal residual counts are exactly

    (delta, b-a+delta, t+2(a-delta)).                      (2)

**Lower bound.** For any chosen switches, trace the resulting terminal paths
whose black endpoint is T and white endpoint is H. Put one unit of flow on
their fragment arcs. Paths do not share fragments, and their transitions
conserve flow at each square. There are B_T-a' such paths if a' TT remain.
Thus B_T-a'<=F, proving a'>=B_T-F. Cycles are omitted and cause no problem.

**Construction.** Take an integral maximum flow and colour its used fragments
1 and the others 0. Each contact has equally many incoming and outgoing 1s.
For two bits on each side, equality of counts implies either the straight
bijection or the crossed bijection preserves BOTH colours. Choose either
consistent bijection, independently at every contact. This decodes to an
actual subset of disjoint square flips and preserves every physical fragment.

A terminal path is monochromatic. Every used source edge starts a colour-1
path at black T; black H has no colour-1 outgoing fragment, and white T has
no colour-1 incoming fragment, by conservation at those terminal vertices.
Thus the F used source edges give F distinct T-to-H paths. This proves
a'<=B_T-F. The lower bound gives equality, including when F<B_T. A colour-0
black T path cannot secretly end in H in the maximum-flow decoding: that
would produce more than F successful paths and contradict the lower bound.
Possible colour-1 cycles carry no source flow and do not affect the argument.
Endpoint incidence then gives (2). Full coverage concerns BOTH colours of T:
when F=B_T, every white T lies on a colour-0 path starting at black H.

As a numerical certificate, if A is the board area and b_opt=b-a+delta,
the unchanged endpoint ledger gives J=|M|+|T|=A/2+delta-b_opt, hence
J<=A/2+delta. A pool with delta=0 therefore certifies the half-area bound
for that configuration. A universal numerical improvement still requires
a geometric estimate or suitable pool construction; the flow theorem alone
does not supply it.

More precisely, for any eta the weighted margin is exactly

    A/2 - [|T|+(1-eta)|M|] = b_opt+eta|M|-delta.

Thus a geometric bound delta-b_opt<=eta|M| proves coefficient 1-eta;
the stronger sufficient condition delta<=eta|M| also works. Eta=1/6
recovers the existing 5/6 coefficient, and eta<1/6 would improve it.
No such universal geometric bound is established here. This identity
uses remaining HH components once, separately from any cycle M credit.

The compressed graph has O(n+e) arcs/vertices. Unit augmenting paths take
O(B_T(n+e)) time, followed by linear local decoding. Extraction from the
physical grid additionally costs its path size. This is an ordinary integral
flow theorem for every finite pool size; finite controls are not its proof.

## 3. The complete directed-fragment cut obstruction

There is a useful exact form without terminal nodes. Let a_iso count original
TT paths with NO candidate contact. For U a subset of square vertices, let

* s_T(U) count touched paths whose black endpoint is T and FIRST contact is in U;
* h_H(U) count touched paths whose white endpoint is H and LAST contact is in U;
* out(U) count original INTERIOR fragments from a contact in U to a contact
  outside U, with multiplicity, irrespective of their M weight.

Then

    delta = a_iso + max_U [s_T(U)-h_H(U)-out(U)].           (3)

The maximum is at least zero by U empty. Complete coverage holds iff a_iso=0
and s_T(U)<=h_H(U)+out(U) for EVERY U. This is a single joint capacity cut;
an interior fragment shared by many prospective relays appears once.

Proof. In a minimum cut, a black-T terminal can be moved to the source side
without increasing capacity: either its source edge or its sole outgoing
fragment previously crossed. Likewise move a white-H terminal to the sink
side. Black H terminals can be put on the sink side, and white T terminals
on the source side, without increasing capacity, because they have no
super-terminal edge and no incoming/outgoing fragment respectively.
For a no-contact TH path with black T the resulting cut contributes exactly
one; a no-contact TT contributes zero. Therefore for fixed square-side U
the minimum cut capacity is

    c0 + (B_touch - s_T(U)) + h_H(U) + out(U),

where c0 is the number of no-contact black-T/white-H paths and B_touch
counts touched black T paths. Since B_T=a_iso+c0+B_touch, max-flow/min-cut
gives (3). Terminal placements realizing this expression are independent,
including the zero-contact paths. The argument uses capacity one even for a
zero-M fragment; zero cost never substitutes for terminal capacity.

### Why the ordered shared star has shortage s-1

In the feasible family whose T-to-H centre order is H^s T^s, the centre is
canonically oriented in the reverse direction. Let U consist of the s TT-leaf
contacts. Then s_T(U)=s, h_H(U)=0 and exactly ONE centre fragment leaves U.
Thus (3) gives delta>=s-1, although all s^2 individually ordered TT/HH relay
pairs exist. One HH-then-TT relay repairs one pair, proving equality for every
s>=1. For order (HT)^s, switching the full alternating word covers all T,
so delta=0. This identifies the physical bottleneck missed by coarse Hall.

The wrong-order relay likewise fails because its directed fragments do not
give sufficient s-z capacity. The same-order two-contact TT/HH fixture is
different: selecting BOTH fails, but the POOL admits either singleton and
therefore has delta=0. The theorem optimizes subsets, not a mandated full batch.

## 4. Exact total M cost: two colours with one shared capacity

Suppose full coverage is feasible. For each fragment R choose binary r_R,b_R
with

    r_R+b_R<=1.                                         (4)

Interpret red as terminal paths from black T to white H, blue as paths from
black H to white T, and neither as HH or a free P-only cycle. At every square
conserve red and blue SEPARATELY. Impose terminal constraints on its sole arc:

| Terminal | Red | Blue |
| --- | --- | --- |
| black T | 1 | 0 |
| black H | 0 | optional |
| white T | 0 | 1 |
| white H | optional | 0 |

Then the minimum possible total TH payment M cost over all prescribed
contact subsets is EXACTLY the integer-program optimum

    min sum_R w_R (r_R+b_R),                            (5)

subject to (4), the terminal constraints and the two conservation equations
per square. There are O(n+e) binary variables and constraints. No polynomial
weighted-optimization claim or integrality of its LP relaxation is made.

Proof. From a covering switch subset colour each TH path according to its
black endpoint and leave all HH/cycles uncoloured. This is a feasible model
point with objective exactly its payment M cost. Conversely at a model point
the three labels red,blue,unused have equal incoming/outgoing multiplicities
at every square: unused follows from degree two and the other equations.
Two ordered pairs with the same label multiset admit a straight or crossed
label-preserving bijection. Decode it at every square. All terminal paths
are TH or HH by the terminal constraints. Every physical fragment is consumed
once. The actual TH cost is at most the objective; any extra coloured cycles
only add nonnegative cost. Deleting each monochromatic directed cycle from
its colour preserves all constraints and cannot increase cost. Thus both
minimum inequalities hold and give equality. Zero-weight cycles are harmless.

The red and blue paths may visit the SAME square using different ports.
They may never use the SAME fragment. Condition (4) enforces physical M
ownership and vertex-disjoint payments, including zero-M fragments with
vertices. This is exactly the cross-component compensation constraint.

For an explicit false shortcut, in the all-length 4-by-W ladder a single
rightmost contact yields one red path of M cost zero but a complementary blue
payment of cost W-2. A second contact at the other end gives BOTH payments
cost zero by moving all inner M resources into a free cycle. Therefore an
arbitrary minimum-cost red flow does not give a minimum total-cost decoding;
its omitted complementary payment can have unbounded cost even when the
joint optimum is zero. This does not refute the unweighted coverage theorem.

A stronger [three-contact all-size counterfamily](ONE_COLOUR_GREEDY_BARRIER.md)
also rules out first minimizing red and THEN optimally completing blue:
for even L>=4 its cost is L^2+12L+80 versus joint optimum 10L+78.
All three contacts are internal. Its unique minimum red flow forces the
bad choice, so neither optimal completion nor favourable tie breaking helps.

The five-contact family now has a complete weighted model beyond the earlier
one/two-contact class. For its prescribed pool the optimum in (5) is C5 in the
positive-gap regime, while every proper subset costs C2. The full model must
allow multiple independently owned fragments from one original component.

## 5. What remains open

This proves an exact algorithm and cut certificate for arbitrary prescribed
contact POOL coverage, replacing coarse path-level Hall rules. It does not
prove that every feasible grid has a vertex-disjoint pool whose cuts all pass.
The cost model is an exact finite reduction, not an efficient general solver
or a proof of its LP integrality. General geometric pool selection, weighted
optimization and the universal 5/6 improvement remain open. The 11 October
manuscript and public main are not modified by this research note.

Local evidence: [physical/abstract controls](../output/contact-flow-cut.json),
[post-submission edge cases](../output/contact-flow-edge-cases.json),
[Lean source](../formal/SubQuorum/ContactFlowCut.lean),
[scoped Lean execution](../output/contact-flow-formal.json), and
[independent audit status](../output/contact-flow-review.json).
The eleven Lean declarations include arbitrary-label local switch completion
and a quantified even-L unbounded-ratio witness; physical embedding, global
flow/min-cut optimality and the cost-model equivalence remain written.
