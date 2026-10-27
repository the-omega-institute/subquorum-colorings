# Canonical Hall barriers and completion of a paid path pair

The two-nontrivial-TH-path bound forgets which exterior whites can be
exposed. Restoring that information gives a stronger physical-capacity
bound. We also give an exact extension test for a specified paid path
list, and a strictly positive-weight example where one minimum pair
cannot extend at the optimum although another minimum pair does.

## 1. Model and the canonical exterior barrier

Use assumptions 1--5 of
`EXPOSABLE_PORTS_AND_BRANCHED_SOURCE_OBSTRUCTION.md` and H6 of
`TWO_NONTRIVIAL_TH_PATH_BOUND.md`. Thus M covers P=V(M) on a finite even
rectangle, N is a perfect auxiliary grid matching, T is a feasible
white subset of Q=V minus P, and W=Q_white minus T has size r-1.
There are r separated M-covered cores and black Q centres h_i whose
P neighbours are in their own core. Every centre has finite TH fee,
the HH-source graph saturates W, and the direct exterior graph G_O
has black side B, white side T, and a black-saturating matching with
white surplus one. No centre has a T neighbour (H6). All weights are
finite and nonnegative; the Python implementation uses exact integers.

Retain J (eligible unmatched core indices), rho_i, Lambda, E (exposable
exterior whites), and U_1 (the exact one-TH-centre/direct-other-TH normal
form optimum). Put C_J={h_j:j in J}, F=T minus E, and

    D={b in B: N_T(b) has no vertex in E}.                  (1)

**Canonical barrier lemma.** For any black-saturating direct matching A,

    D={b in B:A(b) in F},     N_T(D)=F,     |D|=|F|.        (2)

In particular D does not depend on which matching A was chosen.

Proof. Start the usual alternating search at the one unmatched white
vertex of A, orienting nonmatching edges white-to-black and matching
edges black-to-white. Its reachable whites are exactly E, by the
exposure lemma. A black vertex b is reachable iff A(b) is reachable:
one direction uses its matching arc; in the other, a matched white
can only first be reached through its own matched black vertex.

Every reachable black vertex has a white neighbour in E. Conversely,
if b has a neighbour e in E, then either b--e is nonmatching and b
is reached from e, or e=A(b) and b is reached by the preceding iff.
Thus the unreachable blacks are exactly D in (1), and their matched
white vertices are exactly F. This gives |D|=|F|, F subset N_T(D),
and N_T(D) subset F by (1). QED. Empty F,D are permitted.

## 2. A stronger source-and-endpoint inequality

Define two physical path relaxations, with +infinity for infeasibility:

* F_CC is the minimum expense of two vertex-disjoint nontrivial TH
  paths, both ending at centres. Their selected sources are distinct.
* F_H is the minimum expense of two vertex-disjoint nontrivial TH
  paths with one selected source in F and one in E, and one black
  endpoint in C_J and one in D. Source-to-endpoint identities are
  NOT prescribed: the cross pairing is allowed in this relaxation.

Nontrivial means containing at least one actual M edge. All capacities
belong to the physical actual edges, not copies in separate layers.

**Hall-barrier theorem.** Under the stated hypotheses,

    B_H := max{Lambda,min(U_1,F_CC,F_H)} <= f*.             (3)

If U_1 is finite, the previous construction gives f*<=U_1.
This bound dominates the accepted two-path bound B_2, because both
F_CC and F_H are at least F_2^C after forgetting their extra quotas.

Proof. There is at least one TH centre, since there are r centres
and only r-1 white HH sources. If at least two centres are TH, their
two nontrivial paths witness f(N)>=F_CC; H6 makes both nontrivial.

Suppose exactly one centre h_j is TH, from selected source t. The
other r-1 centre paths consume every white hole. Their HH assignment
saturates W onto the other centres, so j belongs to J. All other
black Q terminals are consequently paired with selected white T.

If t belongs to E, its centre path costs at least sigma_j>=U_1,
regardless of any other nontrivial TH components.

If t belongs to F, consider the |D|=|F| black exterior endpoints in D.
All have selected sources. At most |F|-1 of those distinct sources
can belong to F, since t is already used by the centre path. Hence
at least one D path starts in E. It cannot be direct, because
N_T(D)=F. Together with the h_j path it gives a feasible pair for
F_H: one source in each of F,E, one endpoint in each of C_J,D,
with disjoint physical resources. Thus f(N)>=F_H.

These cases exhaust every full N. Nonnegativity permits discarding
the other TH expenses in each case, yielding the minimum in (3).
The independent HH-source inequality supplies Lambda. QED.

The source and sink quotas in F_H are all capacity one. Allowing
cross pairing can only decrease its minimum, so the theorem does
not confuse a one-commodity flow with prescribed labelled demands.
It neither assumes a relaxed pair extends nor pays for an HH path.

## 3. Physical flow certificates

Use the earlier directed grid: M black-to-white with capacity one
and its weight; non-M edges white-to-black with capacity one and
cost zero; delete direct T-to-black-Q arcs. For F_CC, only centres
are terminal sinks. For F_H, put a capacity-one source collector in
front of each of F,E, and a capacity-one sink collector after each
of C_J,D. A value-two flow must use one vertex of each group.

The original actual arc remains the unique outgoing arc at black P
and unique incoming arc at white P. Thus its one capacity protects
both endpoints. Terminal/source capacities protect Q vertices. An
integral flow decomposes into two vertex-disjoint physical paths
and circulations; minimum-cost circulations have zero cost and may
be discarded. Conversely each admissible path pair gives such a flow.
These are the same physical bottleneck and circulation arguments as
the accepted F_2^C representation, with additional endpoint quotas.

Two Bellman--Ford augmentations compute each minimum. Nonnegative
reduced costs on every residual arc certify minimum fixed-value cost;
if fewer than two units can be sent, a residual cut has capacity at
most one. On the bounded-degree grid, the complete lower-bound
procedure takes O(v^2) arithmetic time and O(v) stored words. Integer
bit costs are additional. The underlying matching/flow tools are
standard; the content of (3) is the forced exterior compensation.

## 4. Exact completion test for fixed TH paths

This next lemma needs no core or exterior hypotheses. Let M be a
matching on a finite balanced grid board, let T be white Q vertices,
and specify any vertex-disjoint simple nontrivial alternating paths
from selected T to black Q, with interiors in P and edges N,M,...,N.
Remove all their vertices and fix their auxiliary edges. Let R be the
remaining vertices. No actual pair crosses from R to its complement.
Form a bipartite graph H on R using every remaining grid edge EXCEPT

    t--b with t in remaining T and b in remaining P.         (4)

**Fixed-path extension lemma.** The specified paths extend to a full
auxiliary N with every other TH path direct iff H has a perfect
matching. In that event all paid actual edges are exactly those on
the specified paths. Otherwise a Hall set S in black R with
|N_H(S)|<|S| certifies failure of this specified extension problem.

Proof. For any valid extension, removing the fixed paths leaves a
perfect matching on R. A remaining selected white has a direct TH
path iff its auxiliary neighbour is a black Q vertex: a Q endpoint
terminates the alternating component immediately. Thus the direct
condition is exactly deletion (4). Conversely a perfect matching of
H, together with the fixed auxiliary edges, covers the original
board. The fixed paths remain full components, since all their
actual pairs and auxiliary incidences are fixed internally. Every
remaining selected white is matched to black Q, so all remaining
TH paths are direct. Other components are HH or P-only and are free
for TH expense. Hence no actual resource is reused or additionally
charged. Hall's theorem gives the failure certificate. QED.

A standard iterative augmenting matching finds the perfect matching,
or an alternating reachable Hall set at a failed augmentation. It
takes O(v^2) time and O(v) storage on this grid. The implementation
returns the complete N or the explicit deficient neighbour sets.

Consequently, if a returned minimum F_CC or F_H pair has expense
B_H and passes this extension test, it certifies f*=B_H. If U_1=B_H,
the old normal-form construction already certifies the optimum.
Failure for a particular minimum pair is NOT a necessity result:
other minimum pairs may extend, and additional nontrivial TH paths
may permit extensions outside the specified direct-remainder class.

## 5. A minimum pair can select the wrong ports

Use the SAME fixed 18-by-18 footprint and M,N from
`develop/fixtures/two-th-compensation.json`. Give these three edges
weight one and every other actual edge integer K>=3:

    e_A={(2,2),(3,2)}, e_B={(6,9),(6,10)},
    e_C={(6,6),(6,7)}.

The previous complete N still has paid paths A and B, each costing
one, so f(N)=2. Its third cheap edge e_C is on an HH path, not charged.
The old normal-form matching still costs K. The only cheap-only
centre path is A from (1,2) to (4,2): e_A is in the northwest core;
within the central core neither cheap white endpoint (6,7),(6,9)
is adjacent to its centre, and neither is adjacent to the OTHER
cheap black endpoint. Thus no chain of the two central cheap actual
edges can reach a centre. The northwest source (1,2) lies in F.
As before, a normal-form centre path must therefore use a K edge,
and the existing normal-form N attains K. Hence U_1=K. Since any
nontrivial path costs at least one, the two-path bound gives f*>=2.
The fixed complete N attains it, giving f*=F_2^C=2 for every K>=3.

But the following ALSO is a minimum F_2^C pair:

    A: (1,2),(2,2),(3,2),(4,2),
    C: (5,6),(6,6),(6,7),(5,7).

It has cost two, disjoint vertices, and one centre endpoint. Both
selected sources lie in F, whereas only the endpoint (5,7) lies in D.
If it extended at expense two, positivity would force all remaining
TH paths to be direct. The other four centres would be HH and use
all four white holes. Of the original 20 black chamber endpoints,
19 remain, but only 18 chamber white sources remain after A,C.
No direct source from E can enter D. The required chamber matching
is impossible. Thus this minimum pair cannot extend at the true
optimum. The exact physical residual matching test also returns a
Hall obstruction of 51 black vertices with only 50 allowed whites.

The pair A,B, in contrast, has one source in F and one in E, with
endpoints in C_J and D. It passes the extension test at cost two.
The source quotas exclude A,C from F_H. This refutes the rule that
ANY minimum centre-containing pair extends at its fee; it does not
refute the relaxed lower bound or the existence of an optimal
compensating pair. The argument holds for all K>=3, not just the
tested integer samples.

## 6. Validation scope and the old 48-control benchmark

The checker independently enumerates all small surplus-one bipartite
graphs for the barrier lemma, physical path pairs for the four
quotas, and full small-grid matchings for the fixed-path extension
test. It verifies residual reduced costs and all failed Hall cuts.

On the original 48 changed-M controls, B_H certifies 47 normal-form
optima; variants 14,23,45 are newly certified relative to B_2.
For variant 31 the original weights, not a symbolic reweighting,
give B_H=0 and U_1=2. The minimum Hall pair A,B passes the extension
test and its full N costs zero, so this original control also has
certified f*=0. All 48 thus have an attaining complete N and a
matching general lower bound. This is a finite implementation
benchmark, not a claim of a general exact optimizer.

The general mathematical statements are proved in Sections 1--4;
the all-K failure of arbitrary minimum-pair extension is proved in
Section 5. No Lean verification or universal 5/6 improvement is
claimed. Multiple Hall regions and extra nontrivial TH paths remain
part of the wider research problem.
