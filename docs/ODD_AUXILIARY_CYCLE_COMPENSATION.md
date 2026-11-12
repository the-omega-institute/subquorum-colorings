# All odd quotient cycles strengthen the unrestricted subcubic gap

12 November 2026. All graphs are finite, simple and bipartite. Formation
uses a not necessarily induced K_(1,2) with exactly two selected vertices;
minimal means inclusion-minimal. The dissociation number beta_2 is
unrestricted.

**Theorem.** For every graph G of maximum degree at most three and every
minimal two-star-forming set S,

    |S|-beta_2(G) <= floor(19|V(G)|/192).

In particular the same bound holds for SF_2-beta_2. No connectivity,
minimum-degree or selected-component condition is required. The coefficient
19/192 improves the preceding11/111 by1/7104, and the general1/10 by1/960.
Graph sharpness is not asserted.

## A stronger partial-template lemma

Use the partial template H with layers I,C,X of orders b,2b,2b:
I is independent, each i has two X neighbours and these pairs partition X;
C--X is the perfect owner matching; F=H[C] has maximum degree two; and
Q=H[X] is a possibly partial matching. There are no other edges.
The original bipartition need not be balanced. Pair the two neighbours of
each i by an auxiliary P edge. It is not an edge of H.

The components of P union Q are alternating paths of order2h, beginning
and ending with P, or cycles of order4ell. Let o count cycles with ell odd,
including ell=1.

**Lemma.** beta_2(H)>=ceil(31b/12), constructively in polynomial time.

**First construction.** The two one-core-side constructions from the
partial-template proof have base sizes summing to5b, without a balance
assumption. An alternating cycle of order4ell contributes floor(ell/2)
to the average gain. An alternating path with h P-pairs contributes at
least h/4, since the two quotient path orders sum to h and each gain is
the ceiling of half its order. Hence

    beta_2(H) >= 5b/2 + b/4 - o/2.                         (1)

For a cycle, floor(ell/2)=(2ell)/4-1/2 when ell is odd,
and equals (2ell)/4 otherwise. This accounts for every component,
including isolated P edges and paths of order four.
The actual compatible vertex choices and unbalanced base calculation are
given in UNRESTRICTED_SUBCUBIC_GAP_IMPROVEMENT.md; no new choice is needed.

## Low-degree credits and isolated-cycle credits

Independently choose one proper two-colouring class from each auxiliary
component, uniformly. Call their union Y. Then |Y|=b, Y contains one
endpoint of each P and Q edge, and the residual owners

    R_C=C minus {c(x):x in Y}

have size b. For any dissociation set Z in F[R_C], the set I union Y union Z
is dissociation in H. Write

    Phi=beta_2(F[R_C])-b/2.

A path component on m vertices contributes at least L/4 to Phi, where
L counts its vertices of degree at most one. For m=1,2 this is direct;
for m>=3 use beta_2(P_m)=ceil(2m/3)>=m/2+1/2. Every even cycle
contributes nonnegatively. Every even cycle other than C4 contributes
at least one, since floor(2m/3)-m/2>=1 for every even m>=6.

Fix one of the o odd quotient cycles. Its owners split into two auxiliary
phase classes U_0,U_1, each of order2ell congruent to2 modulo4.
Each U_j is either wholly retained in R_C or wholly omitted.

Call U_j intact if every vertex has degree two in F[U_j]. Then all its
core degree is spent internally. Its components are isolated even cycles
in F and remain isolated cycles in F[R_C] whenever U_j is retained.
They cannot all be C4: their total order is2 modulo4. Thus at least one
of these cycles contributes one to Phi. Give this class one credit when
it is retained. Its expected credit is1/2.

Otherwise call the class broken. Let

    B_j={v in U_j:deg_(F[U_j])(v)<=1}.

Then |B_j|>=2. To prove this, if exactly one vertex had degree at most
one, it could not have degree one by parity of the number of odd-degree
vertices. It would be isolated, and all remaining vertices would lie in
even cycles, making |U_j| odd, a contradiction.

For each v in B_j,

    Pr(v in R_C and deg_(F[R_C])(v)<=1) >= 1/4.            (2)

Indeed, v is retained with probability1/2. If its full core degree is at
most one the low-degree conclusion is automatic. Otherwise at least one
core neighbour lies outside U_j. If it belongs to the same auxiliary
component, it is in the opposite phase class and is omitted when v is
retained. If it belongs to another component, its phase is independent,
so that neighbour is omitted with conditional probability1/2.
No independence between v's two neighbours is assumed.

Give each such retained low-degree v a credit1/4. Its expected credit is
at least1/16; the broken class has at least two such vertices and therefore
expected total credit at least1/8. An intact class has expected credit1/2,
so every one of the2o classes has expected credit at least1/8.

These credits do not overlap. Broken classes use distinct vertices among
the global low-degree count. Intact classes use isolated cycle components
entirely inside their disjoint owner classes, and these components contain
no low-degree vertices. Different intact classes cannot claim the same
cycle. The preceding path/cycle bounds therefore show, for every actual
phase assignment, that Phi is at least the total assigned credit.
Consequently

    E[Phi] >= o/4,
    beta_2(H) >= 5b/2 + o/4.                              (3)

The credit score can be derandomized. Each low-degree indicator involves
the phases of at most three auxiliary components (its vertex and its at
most two core neighbours); an intact-class indicator involves one bit.
Enumerating at most eight local completions computes each conditional
expectation exactly. Fix each successive phase to a value not decreasing
the expectation, then optimize the residual paths and cycles.

The constructions (1) and (3) are alternatives. Their maximum is at least
their convex combination with coefficients1/3 and2/3. The o terms cancel,
giving

    beta_2(H) >= 5b/2 + (b/4-o/2)/3 + (2/3)(o/4)
               = 5b/2+b/12 = 31b/12.

This compares guaranteed cardinalities; it does not combine incompatible
vertex sets or spend a cycle credit in a second construction.
Integrality completes the lemma.

## Lifting the template and the exact global identity

Use the fixed witness decomposition proved in
SHARP_BIPARTITE_STAR_FORMING_GAP.md and restated in
UNRESTRICTED_SUBCUBIC_GAP_IMPROVEMENT.md. R consists of selected components
of order one or two. There are p disjoint chosen triples and u remaining
owner--witness pairs, with both chosen centres and chosen leaves removed
before assigning these pairs. Thus |S|=|R|+2p+u.

For the selected isolates count the incident residual pair witnesses h.
Let a count h=1, b count h>=2, and b3 count h=3. Put

    d=|S|-beta_2(G), m=min(a,p), alpha=a-m, pi=p-m,
    e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u, tau=m+b-2d.

All these slacks and e-b3 are nonnegative. The universal two exchanges
give tau>=0, and one helper per witness gives u>=a+2b+b3.
The exact old ledger is

    n-10d=r+m+3alpha+3pi+2e+q+5tau.                        (4)

The h=2 isolates I0, their assigned witnesses X0 and distinct owners C0
induce exactly a partial template with b'=b-b3 helpers. The precise
selected neighbourhood of every X0 vertex is its owner and helper.
Each owner has at most two core neighbours; each witness has at most one
interface neighbour. No balance, regularity or interface completion is used.

Every dissociation set in this induced template can simultaneously retain
R minus I0 and all p chosen leaves. Their internal and cross-edge exclusions
were proved in the preceding partial-template note: R has no edge to C0,
the exact neighbourhoods exclude their edges to X0, and each chosen leaf
has its unique selected neighbour at its omitted triple centre.
Thus

    beta_2(G) >= |R|-b'+p+31b'/12.

Set Z=12beta_2(G)-12(|R|-b'+p)-31b'>=0. Direct substitution gives

    2d+Z=19m+12alpha+12pi+5tau+12e+19b3.                   (5)

Subtract(5) from nineteen times(4):

    19n-192d = Z+19r+45alpha+45pi+7e
                 +19(e-b3)+19q+90tau >=0.                 (6)

All terms refer to one fixed physical allocation. Equation(6) proves the
theorem for the arbitrary minimal S, and hence for SF_2.
The empty graph and empty template satisfy the same identities.
Finite verification checks implementation; it is not a premise of the
all-order argument. Graph-sharpness, cubic selected-star existence and
rectangular-grid consequences remain separate questions.
