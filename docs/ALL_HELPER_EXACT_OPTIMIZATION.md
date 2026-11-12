# Exact all-helper dissociation optimization and its sharp forcing loss

12 November 2026.

For a partial template H with b helpers, this note gives an exact matching
expression for the largest dissociation set containing every helper. It also
proves that forcing all helpers can lose at most b vertices, with equality at
every b. The expression isolates a precise sufficient condition for the open
unrestricted bound beta_2(H)>=ceil(8b/3); failure of that sufficient condition
would not by itself be a counterexample to the unrestricted bound.

## Setting

The finite simple graph H has disjoint layers I,X,C of sizes b,2b,2b. Each
helper is adjacent to its own two witnesses in X and has no other neighbours.
Each witness has a distinct owner in C, and these owner edges form a perfect
matching X--C. Edges inside X form a possibly partial matching Q. The owner
graph H[C] is arbitrary; the intended subcubic bipartite templates have owner
maximum degree at most two. There are no other edges. The empty template is
included.

Use the owner bijection to identify X and C with an index set V of size2b.
Let P be the perfect matching pairing the two witnesses of each helper, let
A=P union Q be a simple graph on V, and let B be the transported owner graph.
The union A of two matchings is bipartite: every nontrivial component is a
path or an even cycle, with duplicate matching edges identified. The intended
physical bipartition forbids such a duplicate, but the argument also allows it.

Write beta_I(H) for the largest dissociation set required to contain I. A
dissociation set induces maximum degree at most one; alpha and nu denote the
independence and matching numbers of a graph, respectively.

## An exact expression

**Theorem1.** Under the stated hypotheses,

    beta_I(H)
      = b + max_{S subset V, B[S] dissociation} (|S|+alpha(A[V minus S]))
      = 3b - min_{U subset V, B[V minus U] dissociation} nu(A[U]).       (1)

**Proof.** With all helpers selected, any selected witness is already paired
with its helper. No other witness of that helper, Q-neighbour, or owner can
then be selected. Conversely, these restrictions suffice at every helper and
selected witness. Hence, writing T for selected witness indices and S for
selected owner indices, the conditions are exactly

    T independent in A,   T intersect S empty,   B[S] dissociation.

The helpers have at most one selected witness by independence on P; selected
witnesses have neither a selected Q-neighbour nor owner; and the selected
owners meet no selected witness, leaving exactly B[S] as their induced graph.
For fixed S, the best choice of T has size alpha(A[V minus S]), giving the
first equality.

Set U=V minus S. The bipartite matching/vertex-cover theorem gives
alpha(A[U])=|U|-nu(A[U]). Therefore
b+|S|+alpha(A[U])=b+2b-nu(A[U])=3b-nu(A[U]). Maximizing over the permitted
S, or equivalently minimizing over permitted U, proves the second equality.
All maxima and minima exist, including b=0. QED.

Consequently beta_I(H)>=ceil(8b/3) holds if and only if there is a set U with
B[V minus U] dissociation and

    nu(A[U]) <= floor(b/3).                                    (2)

Condition2 is sufficient for the same unrestricted lower bound because
beta_2(H)>=beta_I(H). Its necessity has been proved for the all-helper problem,
not for unrestricted beta_2. No polynomial-time optimization over all U is
asserted by formula1; a fixed U can be scored by bipartite matching.

## The sharp cost of forcing the helpers

**Theorem2.** Every such template satisfies

    0 <= beta_2(H)-beta_I(H) <= b.                              (3)

The upper loss b is attained by partial subcubic bipartite templates at every
integer b>=0.

**Proof.** The lower inequality follows because the all-helper family is
restricted. Take an unrestricted maximum dissociation set D. Its restriction
to each disjoint triple consisting of one helper and its two witnesses has at
most two vertices: all three would give the helper degree two. Thus

    |D intersect (I union X)| <= 2b.

The set D' = I union (D intersect C) is dissociation: I is independent and
has no neighbour in C, while D intersect C is dissociation by restriction.
It contains all helpers. Therefore

    beta_I(H) >= b+|D intersect C| >= |D|-b.

This proves the upper inequality.

For sharpness, take b disjoint paths C_left--X_left--I--X_right--C_right,
with no Q edges and no owner-core edges. Each is P5. Its four noncentral
vertices induce two disjoint edges, while all five vertices do not form a
dissociation set, so beta_2=4 per path. If the central helper is required,
at most one witness can be selected; every selected witness excludes its
owner. There are at most three selected vertices, attained by the helper
and both owners. Hence beta_I=3 per path. Disjoint unions add both optima,
proving beta_2=4b, beta_I=3b, and exact loss b. QED.

These sharp examples are disconnected when b>1 and have pendant vertices.
They make no connected/minimum-degree-two sharpness assertion. Their role is
to distinguish unrestricted optimization from an all-helper rule. They do not
refute the target beta_2>=ceil(8b/3); indeed their all-helper optimum is3b.

## Consequences and scope

If the owner graph B has a dissociation set S of size at least4b/3, taking a
largest independent set in the bipartite graph A[V minus S] already gives

    beta_I(H) >= 2b+ceil(|S|/2) >= ceil(8b/3).

The first inequality uses alpha(A[U])>=ceil(|U|/2). The second needs the
integer condition |S|>=ceil(4b/3); rounding then gives the displayed bound.
For example, this applies when every owner component is a path or an even
cycle of length divisible by three: on a path of orderl choose a pattern
110 with suitable end phase to obtain ceil(2l/3), and on a cycle of length
multiple of three use the cyclic110 pattern. These are sufficient classes;
square cores are covered by the separate compatible square-core theorem.
The general all-helper condition2 and unrestricted8b/3 bound remain open.

## A hereditary owner condition and the fixed-extraction gap bound

The owner class consisting of paths and cycles of length6k, k>=1, is closed
under induced vertex deletion: an intact cycle keeps its length, and a proper
induced subgraph of a cycle is a disjoint union of paths. Each path on l
vertices has a dissociation set of size ceil(2l/3), obtained by the pattern110
from an endpoint. The same pattern gives2l/3 on a6k-cycle. Summing gives at
least ceil(4b/3) selected owners, so the preceding construction applies to
every partial template in this owner class in polynomial time.

Fix a minimal two-star-forming S in a finite simple bipartite graph G of
maximum degree three and the disjoint witness extraction used in
SQUARE_CORE_TEMPLATE_COMPENSATION.md. Let R contain selected isolates and
selected isolated edges. Let p count the disjoint centre/leaf/outside-witness
triples, and u the remaining owner-witness pairs. Of the selected isolates,
a receive one witness and b receive at least two; b3 receive three. The
degree-two helper extraction has b'=b-b3 helpers. The retained set, consisting
of R minus these helpers and one selected leaf from each triple, has size
L=|R|-b'+p, is dissociation, and has no edge to the extracted template.

**Corollary.** If the actual extracted owner graph consists of paths and
cycles of length6k, then

    51(|S|-beta_2(G)) <= 5|V(G)|.                             (4)

Consequently this bounds SF_2(G)-beta_2(G) when a maximum-cardinality minimal
S admits such an extraction. This is an additional sufficient class for the
previous conditional5/51 coefficient, extending the acyclic case to6k-cycles.

**Proof.** The owner construction and the physically separate retained set
give beta_2(G)>=L+ceil(8b'/3), hence

    Z=3beta_2(G)-3L-8b' >=0.

Put d=|S|-beta_2(G), m=min(a,p), alpha=a-m, pi=p-m,
e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u, and tau=m+b-2d. The disjoint witness
proof gives r,q,alpha,pi,tau,b3,e-b3>=0 and the exact identities

    n=10d+m+r+3(alpha+pi)+2e+q+5tau,
    d+Z=5m+3(alpha+pi)+3e+5b3+tau.

Thus

    5n-51d=Z+5r+12(alpha+pi)+24tau+7(e-b3)+2b3+5q >=0,

proving4. Each retained/template vertex is used once. QED.

The actual extracted-core condition suffices. If a larger owner presentation
is in this hereditary class and extraction retains an induced subgraph of it,
the condition also follows. Arbitrary mixtures with square components are
not asserted: the separate square theorem requires P1,P2,C4 components and
does not cover arbitrary longer paths mixed with squares.

The proof uses the standard bipartite matching/vertex-cover identity. The
restriction-and-union forcing estimate is independent of any finite controls.
This note derives an optimization reduction and its exact scope; it makes no
literature-priority claim. Verification and exact independent audit scope are
recorded in the corresponding output receipts.
