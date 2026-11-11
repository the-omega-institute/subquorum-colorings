# Exact upper star-forming numbers and sharp gaps in Cartesian prisms

For every finite simple graph H on n vertices, its Cartesian prism has

    SF_2(H square K_2)=Omega(H square K_2)=2n-nu(D(H)),         (1)

where D(H) is the ordinary bipartite double cover, without diagonal edges.
No bipartiteness assumption on H is needed. Among all n-vertex bases, the
largest prism gap SF_2-beta_2 is exactly max(0,n-4). For n>=5 the bases
attaining it are precisely complete graphs with a matching of edges
deleted. We determine all four parameters on that entire extremal class.

The upper bounds hold more generally in graphs admitting an
adjacency-preserving involution that sends every vertex to a neighbour.
This symmetry also gives direct terminal completion for every feasible
independent selected set, including selections in both layers.

## 1. Definitions and the quotient matching formula

All graphs are finite and simple. A dissociation set induces maximum
degree at most one; beta_2 is its maximum cardinality. A set S is
2-star-forming if every x outside S lies in a not necessarily induced
K_(1,2) inside S union {x}. Equivalently, x has at least two neighbours
in S, or a neighbour in S that has a neighbour in S. Formation fails
exactly when x has no selected neighbour, or its unique selected neighbour
is isolated in the selected graph. SF_2 is the largest cardinality of an
inclusion-minimal forming set. Formation is upward closed, so testing
all single deletions characterizes inclusion-minimality.

A partial colouring is sub-quorum if at every coloured vertex at least
half its coloured closed neighbourhood has its colour. The maximum number
of nonempty colours is psi_sq. A feasible representative pair consists
of a matching M, endpoint set P=V(M), and T disjoint from P, with
deg_(T union P)(t)<=1 for each t in T. Omega maximizes |T|+|M|.

For every graph, beta_2<=psi_sq<=Omega. Distinct colours on a dissociation
set prove the first inequality. For the second, retain one edge from
each colour class containing an edge, and one vertex from each independent
class. A retained singleton originally had no same-colour neighbour,
so its quorum condition allows at most one other coloured neighbour.
The retained representatives are feasible, with one contribution per colour.

Let G have 2n vertices and a fixed-point-free involution tau preserving
adjacency, with v adjacent to tau(v) for every v. Call each two-vertex
orbit a rung. The quotient H has these n rungs as vertices, adjacent
when any edge of G joins the two rungs. Between two rungs G may have
parallel edges, cross edges, or both. The involution ensures every
neighbouring rung meets each endpoint of the other rung.

Write N_H(X) for all vertices adjacent to some member of X; it can
intersect X. Define

    delta(H)=max_(I independent)(|I|-|N_H(I)|),

allowing the empty set. Then

    delta(H)=max_(X subset V(H))(|X|-|N_H(X)|)
            =n-nu(D(H)).                                    (2)

Indeed I=X minus N_H(X) is independent and N_H(I) is contained in
N_H(X) minus X, so its deficiency is at least that of X. Hall deficiency
in D(H), whose left neighbourhood is the right copy of N_H(X), gives
the second equality. An ordinary maximum matching together with an
equal-size vertex cover certifies this value. Alternating reachability
from unmatched left vertices gives a deficient set X, and I=X minus N(X)
attains delta. Thus the values below have polynomial matching certificates.

## 2. What an adjacent involution guarantees

**Theorem 1.** For every G with the supplied adjacent involution and
quotient H,

    Omega(G)=n+delta(H),              SF_2(G)<=n+delta(H).    (3)

For each minimal forming S, if I_S indexes its rungs that are isolated
edge components in G[S], the stronger statement is

    |S|<=n+|I_S|-|N_H(I_S)|.                                (4)

**Representative proof.** Put Z=V(G) minus (T union P). Classify rungs
by endpoint labels TT,ZZ,TP,PZ,TZ,PP, and let a,b,u,v be the counts
of the first four types. Counting labels gives

    |T|+|M|=n+a-b+(u-v)/2.                                  (5)

For a TP rung write its endpoints as t and p=tau(t), and let q be p's
actual mate. The reflected actual edge gives t adjacent to tau(q).
This is distinct from p, so feasibility forces tau(q) into Z. Thus q's
rung is PZ. Its unique occupied endpoint q and unique actual mate recover
the source rung, proving a TP-to-PZ injection and u<=v.

The TT indices I are independent in H. Every neighbouring rung is ZZ:
each of its endpoints sees an endpoint of a TT rung, which already has
its selected rung partner. Hence b>=|N_H(I)|. Equation (5) bounds the
objective by n+|I|-|N_H(I)|<=n+delta(H).

For attainment choose critical I, put

    R=V(H) minus (I union N_H(I)),

select both endpoints of I as T, and use the rungs over R as actual M.
Every selected vertex sees only its selected rung partner in T union P.
The objective is 2|I|+|R|=n+delta(H), proving the exact Omega formula.

**Star-forming proof.** First suppose s,tau(s) are selected and an
original outside x becomes unformed when s is deleted. We claim tau(x)
is outside too. Otherwise it remains selected (it cannot equal s), and
failure forces it to be x's unique selected neighbour and to be isolated
after the deletion. If x is adjacent to s, reflection makes tau(x)
adjacent to the still-selected tau(s), a contradiction. If x is not
adjacent to s, its selected neighbourhood was unchanged. Its original
formation forces tau(x) to have had s as a selected neighbour. Reflection
then makes x adjacent to the still-selected tau(s), again a contradiction.
Thus every such original witness is on an empty rung.

For a minimal forming S split doubly selected rungs into C_0=I_S and
C_1, and let Z be its empty rungs. Then

    |S|=n+|C_0|+|C_1|-|Z|.                                 (6)

The set C_0 is independent in H and N_H(C_0) is contained in Z. Each
endpoint s of a C_1-rung belongs to a three-vertex star already in S:
either it has two selected neighbours, or its rung partner has another
selected neighbour. Thus s itself is still formed after deletion, so
minimality requires an original outside failure, on an empty rung.
Let Q be the 2|C_1| such endpoints. For each empty rung z let W_z be the
UNION of members of Q whose deletion is witnessed by either endpoint of z.

If z has a quotient neighbour c in C_0 union C_1, each endpoint of z
has a fixed forming star using the selected rung c. Deleting anything
outside c preserves both stars, so W_z is contained in the two endpoints
of c. If c is in C_0, this gives W_z empty. If z has no doubly selected
neighbour, neither endpoint x is adjacent to Q. Its selected neighbours
stay fixed when s in Q is deleted. To lose formation, x must have a
fixed unique selected neighbour t, with N_S(t)={s}. Each endpoint x
therefore witnesses at most one such deletion. In all cases |W_z|<=2.

Every member of Q has a witness. Reserving N_H(C_0) and counting each
empty rung's complete union just once gives

    2|C_1|=|union_z W_z|
           <=sum_(z outside N_H(C_0))|W_z|
           <=2(|Z|-|N_H(C_0)|).                             (7)

Substituting in (6) proves (4) and the SF upper bound in (3). No
bipartiteness assumption, nor general-graph assertion SF_2<=Omega,
was used outside this explicitly proved class. QED.

The SF upper bound in (3) need not be attained in an arbitrary such G.
For G=K_(2n), n>=3, the quotient is K_n, delta=0 and Omega=n, but
SF_2=beta_2=psi_sq=2. In a clique any two selected vertices form every
outside vertex, and all larger forming sets are redundant. Each
nonempty colour class must cover at least half the coloured support,
so at most two colours are possible. A perfect matching attains Omega=n.
Thus the SF attainment below uses the prism structure in addition to
the involution.

## 3. Exact star-forming numbers for every Cartesian prism

The prism P(H)=H square K_2 has vertices w_i,b_i, parallel copies of
all H edges inside its two layers, and rungs w_i b_i. Layer exchange
is an adjacent involution with quotient H.

**Theorem 2.** For every finite simple H,

    SF_2(P(H))=Omega(P(H))=n+delta(H)=2n-nu(D(H)).             (8)

**Proof of attainment.** Choose critical I and R as above. The graph
H[R] has no isolated vertex: any such vertex could be added to I without
enlarging N_H(I), increasing its deficiency. Let S contain both lifts
of I, no lifts of N_H(I), and only the w lifts of R.

Each outside lift over N_H(I) is formed using a neighbouring selected
I-rung. An outside b_r over R has its selected rung neighbour w_r,
which has a selected neighbour in H[R]. Thus S is forming. Deleting
a selected endpoint over I leaves that newly omitted endpoint unformed:
its only selected neighbour was its rung partner, which becomes isolated.
Deleting w_r over R leaves b_r with NO selected neighbour; there are
no edges from I to R and no other selected b lift in its neighbourhood.
These explicit witnesses prove minimality, with

    |S|=2|I|+|R|=n+delta(H).

The upper bound and Omega identity follow from Theorem 1. Empty graphs
and empty remainders are included. QED.

The same proof describes all maximum minimal forming sets in a prism.
For a minimal S, the notation of (6) gives the exact nonnegative remainder

    n+delta(H)-|S|
      =[delta(H)-(|C_0|-|N_H(C_0)|)]
        +[|Z|-|N_H(C_0)|-|C_1|].                            (8a)

Thus S is maximum exactly when C_0 is critical and
|C_1|=|Z minus N_H(C_0)|. At equality, (7) forces the available W_z to
partition Q into pairs. This criterion is conditional on S being minimal
forming; its counting equalities alone do not imply feasibility.

In particular a base with a fractional perfect matching has SF_2(P(H))=n;
this also follows from (2), or from the standard identity
nu(D(H))=2nu_f(H). A layer of P(H) is itself minimal forming whenever
H has no isolated vertices: the opposite rung vertex witnesses every
deletion. For bases with positive deficiency the critical-set construction
in the proof increases this layer value to the exact optimum.

When H is bipartite, the separate extended-cover theorem gives
beta_2=psi_sq=SF_2=Omega=2 alpha(H). The present theorem extends the exact
SF and Omega values to arbitrary bases; it does not extend that four-way
equality. The next sections describe the precise failure on dense bases.

## 4. The largest star-forming gap among all prisms

**Theorem 3.** Over all n-vertex graphs H,

    max [SF_2(P(H))-beta_2(P(H))]=max(0,n-4).                 (9)

For n>=5 equality holds exactly when H is K_n with a matching of edges
deleted, allowing the empty matching.

**Proof.** Choose critical I and let r=|R|. A dissociation set may include
both lifts of I together with any dissociation set in P(H[R]), since
there are no H edges from I to R. Every r-vertex base has a prism
dissociation set of size at least min(r,4). For r>=4 choose two w lifts
and two b lifts with disjoint index pairs. For r=3 choose two w lifts
and the b lift of the remaining index. For r=2 take one whole layer;
for r=1 take either vertex; r=0 is empty. All these selections induce
maximum degree at most one. Consequently

    beta_2(P(H))>=2|I|+min(r,4),
    SF_2(P(H))-beta_2(P(H))<=max(0,r-4)<=max(0,n-4).          (10)

For n<=4, the upper bound is zero. A maximum dissociation set is always
minimal forming: maximality forces formation of every omitted vertex,
and each deletion leaves the deleted vertex unformed. Thus the gap is
nonnegative, proving equality in (9) in these small orders too.

For n>=5 we first show

    beta_2(P(H))=4 iff Delta(complement H)<=1.                (11)

If v has two nonneighbours a,b in H, the triple {v,a,b} is dissociation.
Select its three w lifts and two b lifts at other indices, possible
since n>=5. This is a size-five dissociation set. Conversely, if the
missing edges form a matching, any three vertices within either layer
induce at least two edges, so a dissociation set uses at most two vertices
per layer. Disjoint index pairs attain four.

If (9) has positive equality, (10) forces r=n, hence delta=0, SF_2=n
and beta_2=4. Equation (11) gives the asserted form of H. For such a
base, every nonempty independent set has size one or two. A singleton
has at least n-2 neighbours; an independent pair has exactly n-2.
Their deficiencies are strictly negative for n>=5, so delta=0. Theorem 2
and (11) now give SF_2=n and beta_2=4, attaining (9). QED.

The equality classification concerns prisms of a prescribed base order;
it is separate from the sharp n/10 gap problem for bipartite graphs.
The dense positive equality bases here are nonbipartite.

## 5. Exact sub-quorum values on every extremal base

**Theorem 4.** Let H be K_n with m pairwise disjoint edges deleted,
n>=5 and 0<=m<=floor(n/2). Then

    beta_2(P(H))=4,
    psi_sq(P(H))=4+1_(m>=2),
    SF_2(P(H))=Omega(P(H))=n.                               (12)

**Proof of the colouring upper bound.** Fix any partial sub-quorum
colouring, and in one layer let a be the number of coloured vertices,
q its number of colours, and r the multiplicity of one colour there.
Each vertex has at most one missing neighbour within that layer.
If its rung partner is not coloured with its colour, quorum implies

    2r>=a-1.

If its rung partner has the same colour, its coloured closed neighbourhood
has size at least a and its same-colour count is at most r+1, giving

    2r>=a-2.                                                (13)

Missing a same-colour layer neighbour can only strengthen these necessary
conditions. They imply the following complete list of possibilities for
a layer with q>=3:

| Coloured vertices a | Colours q | Colours necessarily shared with the other layer |
| --- | --- | --- |
| 3 | 3 | At least one |
| 4 | 3 | At least two |
| 4 | 4 | All four |
| 6 | 3 | All three |

For a>=7, (13) requires r>=ceil((a-2)/2), so three multiplicities cannot
fit; for a=5 they are each at least two, also impossible. Sizes at most
two have q<=2. At a=6,q=3 each multiplicity is two, and the stronger
inequality without a same-colour rung would fail, so all three colours
are shared. At a=4 every singleton colour requires its same-colour rung,
giving the listed shared counts. At a=3,q=3 the layer triple contains
at least two edges. Some vertex has two coloured layer neighbours, so
its singleton colour requires a same-colour rung; at least one is shared.

If both layers have at most two colours, their union has at most four.
If one has four, those four must be shared, so the other also has four
and there are only four total. If one has three and the other at most
two, their at least one shared colour gives at most four total. If both
have three, their shared count gives at most five. Hence psi_sq<=5.

Five colours force exactly three colours per layer and only one shared
colour. The table forces exactly three coloured vertices in each layer,
all distinct within that layer. The singleton colour at a degree-two
vertex of a layer triple needs a same-colour rung. Thus each triple must
be a P3 whose centre has the one shared colour; the centres are rung mates.
Each leaf pair must be a deleted edge of H. The leaf pairs in the two
layers cannot share an index: such an occupied leaf rung would have
different colours, increasing that leaf's coloured closed neighbourhood
from two to three while leaving its colour count one. Therefore two
distinct deleted edges are necessary for five colours.

If m>=2, choose their two disjoint missing pairs and any fifth index c.
Select the c-rung, both w lifts of one pair and both b lifts of the other.
Colour the rung with one colour and the four leaves with four distinct
colours. Each centre sees two of its colour among four coloured closed
neighbours; each leaf sees one among two. This attains five. If m<=1,
five is impossible; four distinct colours on the dissociation selection
from Theorem 3 attain four. The other parameters were proved above. QED.

In particular K_n square K_2, n>=5, has SF_2=Omega=n while beta_2=psi_sq=4.
These graphs are n-regular, n-connected and vertex-transitive. To check
connectivity directly, removing fewer than n vertices leaves both layer
cliques nonempty and at least one intact rung among the n disjoint rungs.
The remaining cliques are connected by that rung. Removing all n neighbours
of one vertex isolates it, so the connectivity is exactly n. Simultaneous
regularity and high connectivity therefore do not make the four parameters
equal outside the bipartite-base prism theorem.

At n=5,m=2 the four values are beta_2=4 and psi_sq=SF_2=Omega=5.
This also shows that the prism colouring equality beta_2=psi_sq cannot
be extended to arbitrary bases, even when the exact SF formula persists.

**Corollary 4a.** Over all n-vertex bases H, the maximum of
SF_2(P(H))-psi_sq(P(H)) is also max(0,n-4). For n>=5 the bases with
positive equality are precisely K_n and K_n with one edge deleted.

Indeed beta_2<=psi_sq gives the upper bound from Theorem 3, and the
complete base attains it by (12). Positive equality requires equality
in Theorem 3 and psi_sq=beta_2=4, so (12) restricts the deleted matching
to size zero or one. Since SF_2=Omega for every prism, the same exact
extremal statements apply with Omega in place of SF_2.

## 6. Direct completion with selected vertices in both layers

**Theorem 5.** In any graph with the adjacent involution of Section 1,
let (T,M) be feasible and suppose T is independent. There is a perfect
auxiliary matching pairing every t in T directly to a vertex outside
T union V(M). This holds for selected vertices in either or both layers.

**Proof.** Start with all rungs. Each rung with t in T and p=tau(t) in P
is TP. If q is p's actual mate, the injection from Theorem 1 shows that
q's rung is PZ, with z=tau(q) outside T union P and t adjacent to z.
Replace these two rungs by pq and tz. The TP source rungs and PZ image
rungs are disjoint classes; the injection makes all image rungs distinct.
Thus all swaps are disjoint. Other selected vertices keep their rung
partners, which lie outside T union P: no TT rung exists since T is
independent, and all TP rungs were handled. This is the required perfect
matching. QED.

In the tagged union with M, every path containing T is a direct terminal
edge and uses no actual edge. Thus its TH expense is zero under arbitrary
nonnegative actual-edge weights. No bipartite orientation is required
for this direct-terminal statement. Dropping independence requires allowing
direct TT paths; this theorem makes no TT-free claim in that case.

## 7. Verification and remaining scope

`scripts/paired_graphs.py` implements the quotient dual certificate,
the general witness and representative budgets, exact prism witnesses,
the two-colour-layer completion and the extremal-family colourings.
Its sole project dependency is `scripts/extended_double_cover.py`, whose
iterative ordinary matching algorithm supplies a matching and equal-size
vertex cover. The complete dependency set is explicit in the checker.

`scripts/check_paired_graphs.py` independently builds physical adjacency,
enumerates subsets and actual matchings, tests formation by its literal
local definition, enumerates canonical partial colourings, and checks
the explicit deletion witnesses and direct terminal partners. Run

    python3 scripts/check_paired_graphs.py

from the repository root; the report records exact finite scopes.
The arbitrary-size theorems above rest on their written proofs. No new
Lean verification is claimed. The matching deficiency identity and
Cartesian prism operation are standard; a complete priority comparison
for these parameter formulas is not claimed.

The general rectangular-grid equality, the universal mixed-direction
5/6 improvement and sharp restricted gap constants for arbitrary bipartite
graphs remain separate questions. The nonbipartite examples here delimit
the precise scope of a structural extension; they do not refute any of
those grid or bipartite assertions. No manuscript submission or
correspondent approval is implied.
