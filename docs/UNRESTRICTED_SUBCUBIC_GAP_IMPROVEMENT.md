# A uniform improvement of the bipartite gap bound at maximum degree three

12 November 2026. Graphs are finite, simple and bipartite. A
two-star-forming set S covers every vertex outside S by a not necessarily
induced K_(1,2) containing exactly two selected vertices. Minimal means
inclusion-minimal. The dissociation number beta_2 is the largest size of
a set inducing maximum degree at most one.

**Theorem.** If G has order n and maximum degree at most three, then every
minimal two-star-forming set S satisfies

    |S|-beta_2(G) <= floor(11n/111).

Consequently SF_2(G)-beta_2(G)<=floor(11n/111). There is no connectedness,
minimum-degree or selected-component hypothesis. The coefficient 11/111
is smaller than 1/10, strengthening the preceding exclusion of exact
n/10 equality by a uniform linear margin. No sharpness is asserted.
The selected-star bounds 4/57,8/121 and1/24 have stronger coefficients
under their additional selected-component hypotheses.

## A partial template without balance or regularity

Consider a bipartite graph H with disjoint layers I,C,X, of orders
b,2b,2b. Every i in I has exactly two neighbours, both in X, and these
neighbour pairs partition X. The C--X edges form a perfect matching;
write c(x) for the owner of x. The remaining edges are a core F=H[C]
of maximum degree at most two and a matching Q=H[X], possibly partial.
There are no other edges. No balance of either side is assumed.

**Lemma.** Such a graph has beta_2(H)>=ceil(18b/7). Moreover a
dissociation set of that order can be constructed in polynomial time.

**Proof.** The case b=0 is empty. Pair each two neighbours of an I vertex
by an auxiliary edge, forming a perfect matching P on X. P edges preserve
the original bipartition side and are not graph edges. The components of
P union Q are alternating cycles of order4ell or alternating paths of
order2h, beginning and ending with P edges. A cycle has ell P-pairs on
each original side. A path has h P-pairs, whose original sides alternate.
Let b0 count all P-pairs in components of order four, including paths
and cycles, and put t0=b-b0.

First select all owners C_A and none of C_B. Let J be a collection of
P-pairs in X_B, with union T. Omit their I_A centres and all Q-neighbours
of T. Keep every other I_A centre. From each I_B-centred pair keep the
centre and one available X_A vertex, or only the centre if neither
witness is available. Each T vertex is paired with its selected owner;
each chosen X_A vertex is paired only with its I_B centre. These choices
are compatible and constitute a dissociation set of order

    |A(H)|+|J|-z(J),

where z(J) counts opposite P-pairs wholly in N_Q(T). To check the base
term, if |I_A|=r,|I_B|=s, it is 3r+2s. The reverse construction has
base 2r+3s. Their bases therefore sum to 5b even without balance.

On an alternating cycle, the quotient on one side's P-pairs is an
ell-cycle, with a loop at ell=1 and two parallel edges at ell=2.
The maximum of |J|-z(J) is floor(ell/2): proper selected subsets count
their cyclic runs, and alternating selections attain the bound. On an
alternating path, the quotient on either side's r' P-pairs is a path
on r' vertices, with no contribution from the opposite endpoint pairs
whose Q edge is missing. Its maximum is ceil(r'/2), attained by every
other vertex. The empty quotient contributes zero. These statements
also follow directly by counting the runs of any selected quotient set.

Let delta_A,delta_B be these maximizing gains, summed over components
for the two orientations. A long cycle with 2ell P-pairs contributes
2floor(ell/2)>=2ell/3 to their sum. A path with h P-pairs contributes
at least h/2, because its two quotient orders sum to h. Discarding the
nonnegative gains of the short components therefore yields

    beta_2(H) >= 5b/2+(delta_A+delta_B)/2
              >= 5b/2+t0/6.                                  (1)

For a second construction independently choose one proper two-colouring
class of each auxiliary component, with equal probabilities. Their union
Y contains exactly one endpoint of every P and Q edge. Every path has
even order, so |Y|=b. The residual owners

    R_C=C minus {c(x):x in Y}

also have order b. If Z is dissociation in F[R_C], then I union Y union Z
is dissociation in H. Its order is 2b+|Z|.

Write L_C for the number of vertices of degree at most one in F[R_C].
The path/cycle component bounds beta_2(P_m)=ceil(2m/3) and
beta_2(C_m)=floor(2m/3) for even m>=4 give

    beta_2(F[R_C]) >= b/2+L_C/4.                             (2)

For a path, the degree-at-most-one count is one if its order is one,
and two otherwise. Orders one and two check directly; for m>=3 use
2m/3>=m/2+1/2. Even cycle components contribute at least half their order.

Each short auxiliary component contains one P-pair of each original
side. Conditional on one of its owners v being in R_C, exactly one
owner of each original side in that component remains. If v has fewer
than two core neighbours it is automatically low degree. If both distinct
core neighbours belong to its component, they cannot both remain. In
every other case at least one neighbour lies in an independently phased
component and remains with conditional probability one half. Thus

    Pr(v in R_C and deg_(F[R_C])(v)<=1) >= 1/4.

The short components have 2b0 owners. Linearity of expectation gives
E[L_C]>=b0/2. Equation(2) and the second construction imply

    beta_2(H) >= 5b/2+b0/8.                                 (3)

No independence between different owners' events is required. Each event
depends on at most three auxiliary-component phase bits; conditional
expectations determine a phase assignment with L_C>=b0/2 in polynomial
time, enumerating at most eight local completions per expectation term.
An optimal dissociation set of the residual paths and cycles is explicit.

The sets in(1) and(3) are alternatives. If M=max(t0/6,b0/8), then
b=t0+b0<=14M, giving beta_2(H)>=5b/2+b/14=18b/7. Integrality and the
explicit constructions prove the lemma. No completion of H is needed.

## Extracting the template from an arbitrary minimal set

Fix S and put d=|S|-beta_2(G). Use the proved deletion-witness
decomposition from SHARP_BIPARTITE_STAR_FORMING_GAP.md. For clarity,
its notation and disjointness requirements are restated here.

Let R be the selected vertices in components of G[S] of order one or
two, and I the selected isolates. From every vertex admitting a type-3
deletion witness choose one triple (c,ell_c,x_c), where ell_c has unique
selected neighbour c and x_c has unique selected neighbour ell_c. There
are p vertex-disjoint triples. Remove both their centres and their chosen
leaves from S minus R. Every remaining selected owner v has a distinct
outside witness x_v, whose selected neighbourhood is {v} or {v,i} for
one selected isolate i. There are u such pairs. No pair witness belongs
to a chosen triple. In particular |S|=|R|+2p+u.

Let h(i) count these u pair witnesses incident with i. Let a count
h=1 isolates, b count h>=2 isolates and b3 count h=3 isolates. Maximum
degree three ensures there are no larger h values. Set

    m=min(a,p), e=u-a-2b, r=|R|-a-b,
    q=n-|S|-p-u, tau=m+b-2d,
    alpha=a-m, pi=p-m.

All these numbers and e-b3 are nonnegative. For e-b3, each pair witness
has at most one isolate helper, so u>=a+2b+b3. For tau, the two
established dissociation exchanges give 2d<=min(a+b,p+b)=m+b.
The exact vertex count is

    L:=n-10d=r+m+3alpha+3pi+2e+q+5tau.                       (4)

Let I0={i:h(i)=2}, so b'=|I0|=b-b3. Take its 2b' pair witnesses X0
and their distinct owners C0. The induced graph on I0 union C0 union X0
is precisely a partial template of the lemma. The only selected
neighbours of each X0 vertex are its owner and its I0 helper. Each
owner spends one degree on its witness, leaving core degree at most two.
Each witness spends two degrees on its owner and helper, leaving at
most one interface edge. There are no I0--C0 edges because I0 consists
of original selected isolates. This checks all template hypotheses,
including perfect owner coverage, without requiring a balanced graph.

Two other resources can be retained simultaneously with ANY dissociation
set in this template: all R minus I0, and the p chosen leaves ell_c.
The former induce only edges and isolates and have no edge to C0.
They have no edge to X0 because X0's selected neighbours were specified
exactly. A chosen leaf has its only selected neighbour at its omitted
triple centre, so it meets neither C0 nor R minus I0 nor another chosen
leaf. Nor can it meet X0, by that same exact selected-neighbour condition.
The two added sets are disjoint. These observations verify every possible
cross edge, not only the internal dissociation conditions. Consequently

    beta_2(G) >= |R|-b'+p+18b'/7.                            (5)

## An exact nonnegative certificate

Define the nonnegative template slack

    Z=7 beta_2(G)-7(|R|-b'+p)-18b'.

Substitution of |S|=|R|+2p+u, b'=b-b3 and b=2d-m+tau yields

    d+Z=11m+7alpha+7pi+3tau+7e+11b3.                        (6)

Subtract(6) from eleven times(4):

    11n-111d = Z+11r+26alpha+26pi+4e
                 +11(e-b3)+11q+52tau >= 0.                 (7)

This is an identity in the actual witness counts and unrestricted
dissociation number, with all terms proved nonnegative. It proves the
theorem for the fixed S; maximizing S gives the stated SF_2 bound.
All allocated pair witnesses, triple leaves, R vertices and template
vertices have unique ownership. The three template constructions are
alternative dissociation sets, and their improvements are not added.

## Verification and remaining scope

The standalone checker constructs the three partial-template certificates,
the witness decomposition and the full lifted dissociation set. It checks
the actual induced edges, all cross edges to retained vertices, and the
exact identity(7), including unbalanced templates, partial interfaces,
pendant vertices, isolates and h=3 helpers. Finite exact dissociation
optimization is independent of these constructions. General conclusions
follow from the proofs above, not the finite tests. The report and review
record their actual execution scopes. No new Lean, graph-sharp coefficient,
positive cubic selected-star example or rectangular-grid theorem is claimed.
