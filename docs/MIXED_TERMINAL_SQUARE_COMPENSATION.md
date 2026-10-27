# Mixed terminal compensation with a fixed actual matching

An alternating square can compensate a TT path and an HH path without changing
the actual matching M or spending a physical resource twice. A matching in the
graph of eligible TT/HH component pairs gives a simultaneous compensation lemma,
including an exact residual count. Hall coverage of the TT components is a
sufficient condition for the half-area bound, with an explicit numerical margin.
No universal geometric Hall condition is assumed or proved.

The auxiliary full matching N used below is a certificate on the whole grid.
It is NOT the occupied matching M: N may touch holes. Switching N changes the
certificate, while M, P, T, H and feasibility all stay fixed. This is different
from rematching the occupied endpoints in the preceding notes.

An all-length feasible mixed-colour family shows why terminal types matter:
unrestricted maximum retention of M predicts cost zero, but a complete legal
T-to-H payment costs exactly one actual M edge. A different starting N has
a TT/HH square pair, and the new lemma repairs it at that same cost one.
Thus the lemma is useful but its geometric existence condition is substantive.

## 1. Fixed graph, paths, resources and terminal types

Let G be a finite bipartite graph with a perfect matching on V, and M an actual
partial matching with endpoint set P. Partition Q=V\P into selected T and holes H.
For the numerical sub-quorum application assume each selected vertex has at
most one neighbour in P union T. The matching lemmas themselves do not need
this additional degree condition. They also apply when |T| is not |H|.

Choose a full auxiliary perfect matching N of V. In the multigraph M+N,
shared edges are doubled-edge components entirely in P. Other components are
alternating cycles entirely in P, or odd alternating paths with endpoints Q
and all internal vertices in P. Each such path starts and ends with an N edge.
Paths are mutually vertex-disjoint. They have types TT, HH or TH according to
their two endpoints, independent of the graph's bipartition colours.

Write a,b,t for the numbers of TT,HH,TH paths. Then

    |T|=2a+t, |H|=2b+t, |H|-|T|=2(b-a),
    J=|T|+|M|=|V|/2-(b-a).                              (1)

The TH paths already give t disjoint payments. TT paths leave 2a selections
unpaid; HH paths have 2b unused hole endpoints. A path's internal actual M
edges are physical route resources. Counts below always use their original
identities. A P-only alternating cycle is not a payment or a new reserve.

## 2. Local square compensation lemma

Suppose a unit square has two opposite N edges, one on a TT path A and the
other on an HH path B. The other two square edges are grid edges outside N.
They are also outside M, since an M edge between A and B would already join
their distinct M+N components. Replace the two N edges by the other two edges.
This produces a full perfect matching N' and leaves M fixed.

**Square compensation lemma.** The two old paths become two TH paths.
Every other M+N component is unchanged. The union of actual M edges on the
two affected paths is unchanged; N' intersect M equals N intersect M.

Proof. Removing the chosen N edge from A splits it into two arms, each with
one T endpoint. Removing the other edge splits B into two arms, each with
one H endpoint. An arm can have length zero when the cut touches a terminal.
The two new square edges each join one arm from A to one from B. Thus each
new component has one T and one H endpoint and is an odd alternating path.
No cycle is produced, since no new edge joins two arms from the same old path.
The four arms partition the old two paths, so all actual M edges and vertices
on them are used once in the new two paths. Old cut edges and new square
edges are all outside M, giving the intersection identity. QED.

In particular, the switch does not create two copies of a spare M edge, and
does not assume a choice of charges can repair an arbitrary fixed footprint.

## 3. Simultaneous cross-component compensation and its exact scope

Form a bipartite graph K whose left vertices are the ORIGINAL TT path components
and right vertices the ORIGINAL HH path components. Join A to B when at least
one actual alternating unit square as above cuts an N edge from each.
Keep a witness square for each edge of K.

**Batch compensation theorem.** Let F be any matching of K, of size s. Choose
one witness square for each matched pair and perform their switches. Then:

* the squares have disjoint vertex sets and their switches commute;
* the path-type counts become a-s, b-s and t+2s;
* the new TH paths pay exactly t+2s different selections to different holes;
* the residual numbers are exactly 2(a-s) unpaid selections and 2(b-s) unused
  hole endpoints, with no physical M edge shared between payment paths;
* the union of actual M edges on ALL path components and the set M intersect N
  are unchanged.

Proof. A matching of K uses no original TT or HH component twice. Each chosen
square lies in its two original components, which are disjoint from those of
every other chosen pair. Consequently the squares are vertex-disjoint. Apply
the local lemma independently to each pair. Existing TH paths, unmatched
components and P-only cycles are untouched. All assertions follow by counting
the endpoints and taking disjoint unions of the affected physical edge sets.

The maximum possible number of TT/HH pairs repaired by this ONE simultaneous
operation class is nu(K). Any component-disjoint batch defines a matching in K,
and a maximum matching is realizable by the construction above. This is NOT
an optimality assertion for arbitrary repeated switches, transport through TH
components, longer N cycles, or general path payments.

In particular, if K has a matching covering all TT components, then s=a<=b.
There is a complete T-to-H injection along disjoint alternating paths, and

    J=|V|/2-(b-a) <= |V|/2,
    |T|+(5/6)|M| = |V|/2-(b-a)-|M|/6.                  (2)

The full hypothesis may equivalently be written as Hall's condition
|N_K(S)|>=|S| for every set S of original TT components. Equation (2) is the
specific improvement on the original weighted target within this class.
The remaining geometric question is to prove such coverage, or to quantify
additional operations where it fails, for the actual grid configurations of
interest. Finite checks do not assert a universal Hall condition.

Only M edges on the resulting TH paths are spent by the payment. Edges on
unmatched HH paths, P-only cycles or doubled common edges are not spent.
They are not additional numerical rebates on top of b-a in (2): that margin
already comes from the exact global T/H count in (1).

## 4. The correct retention optimization at balanced equality

This subsection assumes |T|=|H|. Let N_TH be the set of full perfect matchings
N whose M+N path components all have type TH. Define c_M(T,H) as the minimum
number of distinct actual M edges used by a complete vertex-disjoint T-to-H
alternating-path payment, or infinity if no such payment exists. Then

    c_M(T,H) = |M|-max_{N in N_TH}|M intersect N|,        (3)

when N_TH is nonempty; emptiness is equivalent to the absence of such payment.
This follows from the standard decomposition of two matchings, rather than
being a new general matching-theory theorem.

Proof, payment to matching. Take the non-M edges on every payment path, and
all M edges not used by any path. Internal path vertices occur in complete
M-edge pairs, so these edges form a full perfect matching N. All Q vertices
are used because |T|=|H|. Its path components are precisely the TH payments,
and unused M edges are doubled common components. If the payment uses r
actual M edges, |M intersect N|=|M|-r.

Proof, matching to payment. Choose a retention-maximizing N in N_TH. A
nontrivial M+N cycle in P would allow replacement of its N edges by its M
edges, strictly increasing retention without changing any Q path or terminal
type. Thus an optimum has no such cycle. All omitted M edges then lie on
the TH path components, which give a payment using exactly |M|-|M intersect N|
actual edges. This proves (3) and the stated existence equivalence.

For arbitrary N there may be M edges omitted on P-only cycles, so lost-M count
need not equal payment-path cost before cycle normalization. The formula uses
an optimum, with the cycle argument explicit.

Let R_all maximize |M intersect N| over unrestricted full N, and R_TH maximize
over N_TH. For nonempty N_TH equation (3) can be written

    c_M=(|M|-R_all)+(R_all-R_TH).                        (4)

The second term is a nonnegative terminal-type penalty. The two optima may
use different full matchings; (4) does not provide two separately available
physical reserve sets. The actual spent set is M\N for ONE final constrained
optimum N, and each edge is counted once.

If T is exactly one bipartition colour of Q and H the other, every odd M+N
path has opposite-colour endpoints, hence is TH. Then N_TH is the full set
of full matchings, R_TH=R_all, and the unconstrained retention formula works.
It can fail for feasible mixed-colour selections, as follows.

## 5. A feasible mixed-colour obstruction and a useful square repair

On the 4-by-4 grid let

    M={(0,1)--(0,2), (1,1)--(2,1)},
    T={(0,0),(0,3),(2,0),(2,3),(3,1),(3,3)}.

The board is

    T P P T
    H P H H
    T P H T
    H T H T

The four selections (0,0),(0,3),(2,0),(3,1) each have their one P neighbour;
(2,3),(3,3) have only each other. Feasibility holds. |T|=|H|=6, |M|=2, J=8.
The induced P graph is the four-vertex path
(0,2)--(0,1)--(1,1)--(2,1), whose leaves force the displayed unique M.

A full matching N0 retaining BOTH actual M edges is obtained by adding

    (0,0)--(1,0), (0,3)--(1,3), (2,0)--(3,0),
    (3,1)--(3,2), (1,2)--(2,2), (2,3)--(3,3).

Its last two paths are HH and TT. Thus R_all=2 and unrestricted lost-M cost
is zero. A legal payment cannot cost zero: the hole (1,2) has no selected
neighbour (its neighbours are P,P,H,H), and equality forces every hole to be
used. Equivalently, the four selections {(0,0),(2,0),(3,1),(3,3)} have only
three adjacent holes {(1,0),(3,0),(3,2)}. One actual edge suffices:

    (0,0)--(0,1)--(0,2)--(1,2),
    (0,3)--(1,3), (2,0)--(1,0), (3,1)--(3,0),
    (3,3)--(3,2), (2,3)--(2,2).                         (5)

The paths in (5) are vertex-disjoint. Therefore c_M=1, R_TH=1 and the penalty
R_all-R_TH=1. The unweighted half-area bound is attained: J=|V|/2. The weighted value is
|T|+(5/6)|M|=|V|/2-1/3, so no weighted equality is claimed.

There is also a nontrivial application of the square lemma on THIS board.
Take a different full N_bad with these path components:

    TT: (0,0)--(0,1)--(0,2)--(0,3),
    HH: (1,2)--(1,3),
    TH: (2,0)--(1,0), (3,1)--(3,0),
        (3,3)--(3,2), (2,3)--(2,2),

and the common M edge (1,1)--(2,1). The N edges in the square with top-left
corner (0,2) are (0,2)--(0,3) on TT and (1,2)--(1,3) on HH. Switch them
to (0,2)--(1,2) and (0,3)--(1,3). This produces precisely the two payments
in (5) involving rows zero/one; the rest stay fixed. The old TT path's one
actual M edge is reused ONCE in one new TH path, not credited twice.

For N0 the TT/HH square graph has no edge: its two direct bad edges do not
occupy opposite sides of a unit square. For N_bad the graph is one edge and
Hall holds. Thus the choice of N matters, and square Hall coverage is a
sufficient certificate rather than an automatic geometric fact.

## 6. An arbitrary-length actual grid family

Append 2b rows below this board, for any b>=0, keeping P and M unchanged.
For band j=0,...,b-1, consisting of rows 4+2j and 5+2j, select the two
columns c with c congruent to j modulo 2, in BOTH rows. Leave its other
four sites as holes. Every selected vertex in a band has exactly its vertical
partner occupied; adjacent bands use opposite column phases, and the first
band's selections lie below the old bottom holes at columns zero/two.
No old selection gains an occupied neighbour. Thus the whole (4+2b)-by-4
board is feasible, with

    |T|=|H|=6+4b, |M|=2, J=8+4b=area/2.                (6)

Use horizontal pairs in each new row to extend N0, N_bad and the matching
induced by (5). Each added pair is TH. The internal hole (1,2) still has no
selected neighbour, so every complete payment still needs an actual M edge.
The old payment (5), extended by adjacent row pairs, uses exactly one.
Consequently for ALL b>=0,

    R_all=2, R_TH=1, c_M=1,
    unrestricted retention cost=0, terminal-type penalty=1.            (7)

The N_bad square graph remains the one-edge graph and its switch gives a
complete compensation certificate without additional actual-edge cost.
The induced P graph and its matching uniqueness are unchanged. These facts
are proved by the periodic band construction, not by finite-length optimization.
For the weighted target the exact value is area/2-1/3, since |M|=2.

## 7. Verification and remaining scope

The [standalone checker](../develop/check_mixed_terminal_compensation.py) verifies decomposition and original resource identities, local
square cuts, simultaneous switches, exact component matching optimum in the
specified operation class, residual counts, actual grid feasibility and the
all-length family. Small exhaustive controls include unbalanced terminal
partitions and P-only cycles. Independent full-matching enumeration checks
retention and admissibility on the small core. Scoped Lean verifies terminal
endpoint arithmetic, batch residuals, the conditional numerical improvement,
and the optimum/intersection arithmetic with the geometric hypotheses explicit.
The decomposition, square-arm gluing, Hall theorem and coordinate assembly
remain written proofs rather than end-to-end grid Lean.

General geometric Hall coverage, optimal choice of N for arbitrary mixed
footprints, legal partial payments when T/H are unbalanced, and a universal
5/6 improvement remain open. No submitted manuscript or Mail operation is
part of this research branch.

Validation records: [coordinate/enumeration output](../output/mixed-terminal-compensation.json)
and [seven local Lean declarations and axiom audit](../output/mixed-terminal-compensation-formal.json).
The corresponding [Lean source](../formal/SubQuorum/MixedTerminalCompensation.lean)
contains the stated conditional arithmetic only. The exhaustive checks contain
7,345 strip controls (880 positive batches and 674 nonvacuous full-Hall cases),
360,432 M/N pair controls, and 6,117 feasible balanced core selections, including
eight strict terminal-penalty cases. No inadmissible core was found; this is not
a general existence proof. The coordinate family is checked at 41 lengths.

[Independent written review ACCEPT](../output/mixed-terminal-compensation-review.json)
covers this note and the all-k unbounded relay-cost note. The reviewer executed
none of the Python or Lean commands; the recorded local controls remain separate.
The review does not cover the subsequent ordered TH relay theorem.
