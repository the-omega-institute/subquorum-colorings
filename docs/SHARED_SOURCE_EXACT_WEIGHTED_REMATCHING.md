# Exact weighted TH completion for shared-source cores under every rematching

For the unequal two-core family of
[the source-budget note](HH_SOURCE_BUDGET_AND_FORCED_FLOW_OVERPAY.md),
the capacity-one HH source bound is ATTAINED for every actual rematching
and every nonnegative weighting. A shortest relay in one core and an HH
relay in the other always have a compatible FULL outer completion. The
choice of which core pays is determined by the two weighted TH distances,
not by core size or the original all-terminal objective.

## 1. Fixed footprint, arbitrary matching and weights

Fix integers K>=l>=1. Use the same board of height H=4K+4l+2 and width
W=4K+4l+4, odd core squares S_1,S_2, black centres h_1,h_2, and unique
white hole z:

    S_1=[0,4K] x [0,4K],             h_1=(2K,2K),
    S_2=[4K,4K+4l] x [4K+2,4K+4l+2],
    h_2=(4K+2l,4K+2+2l),           z=(4K,4K+1).

Put P_i=S_i\{h_i}, P=P_1 union P_2, Q=V\P, T=Q_white\{z}.
White means odd coordinate sum. Let M be ANY grid matching covering
exactly P, and give every actual edge e an arbitrary nonnegative weight
w_e. No actual edge can join P_1 and P_2: their nearest columns differ
by two. Thus M splits into matchings M_i on P_i. The original feasibility
condition and J=area/2-1 depend on P,T and survive every such rematching.

For i=1,2 let rho_i be the minimum w expense of a T-to-h_i alternating
terminal path with internal vertices in P_i. Such a path starts and ends
with auxiliary edges and uses actual M_i edges between them. Its only Q
vertices are its endpoints. T can be anywhere adjacent to that core,
including the upper and left sides of S_2. The shared hole z is NOT an
admissible TH source.

**Theorem.** Both rho_i are finite. The exact unrestricted full-N optimum is

    min_(N full) f(N) = min(rho_1,rho_2).                     (1)

There is an optimal full N whose only TH component containing actual
edges is a rho-minimizing relay in one core. Its unique HH component
joins z to the OTHER centre. All other terminal components are direct
TH edges; every unused actual edge is doubled as a free P-only component.
Actual edges and terminal vertices are used once each.

Furthermore the earlier weighted source-budget calculation, using shortest
T-source expenses on ALL black Q terminals and ordinary HH reachability,
has exact value

    Lambda = min(rho_1,rho_2).                               (2)

This is a structured-family result, not a general solution of positive
source ambiguity. It is stronger than unit-weight attainment for one
canonical matching and must not be read as saying every rematching has
optimum l. The two weighted rho values determine the answer.

## 2. A relay to a boundary white pad exists for every actual matching

Let S be an odd square with black corners, h its black centre, and M any
perfect matching of S\{h}. Let a be a white vertex just outside S, adjacent
to a black boundary vertex c for which S\{c} has a perfect grid matching.
Pair a with c and use that matching on S\{c}. This gives an auxiliary
matching of S union {a}. In its tagged union with M, only h and a have
degree one. Their component is an alternating h-to-a path; all other
components are P-only cycles. It exists independently of M.

We need only the following explicit boundary deletions. For a bottom-right
corner c of the odd square, pair the first 4k rows vertically, and pair
the remaining bottom row horizontally after deleting c. For a top-left
corner c, pair the last 4k rows vertically and the remainder of the top
row horizontally. For the bottom midpoint c, pair the first 4k rows
vertically and the two even bottom-row intervals on either side of c
horizontally. Each construction covers S\{c} fully.

The shared z is adjacent to the bottom-right black corner of S_1 and the
top-left black corner of S_2. The corner constructions therefore supply
z-to-h_i HH relays for BOTH cores under EVERY M. The white pad below each
bottom midpoint is selected T, so the midpoint construction supplies at
least one TH relay for each core. In particular rho_i is finite. A
minimum-weight relay may be taken simple by deleting nonnegative cycles.

## 3. The entire outer region can expose ANY white vertex

Set n_1=4K+2 and n_2=4l+2. Let L_1 be the right-column/bottom-row outer
L of B_1=[0,n_1-1]^2, ordered top-to-bottom then right-to-left. Let L_2 be
the corresponding L of the n_2-square block B_2 with top-left corner
(4K,n_1). Both have odd length, and white vertices have even index.
The only Q vertices in B_i are L_i and h_i. Define

    R = Q \ {h_1,h_2,z}.

All white R vertices are selected T. R has one more white vertex than
black vertices. It is the disjoint union of

    L_1\{z},  L_2,
    U=[0,4K-1] x [n_1,W-1],
    D=[n_1,H-1] x [0,n_1-1].

The rectangular pieces U,D have positive even heights 4K,4l and positive
even widths n_2,n_1.

**Outer completion lemma.** For EVERY white t in R, the induced grid
R\{t} has a perfect direct matching.

Proof. Construct a near-perfect matching A of R exposing only

    t_0=(4K,W-1), the FIRST white vertex of L_2.

In L_1, z has even index 4K. Delete z and consecutively pair both even
segments. In L_2 pair consecutive vertices AFTER t_0. Pair U and D
horizontally in each row. These disjoint pieces cover exactly R\{t_0}.

Orient non-A edges white-to-black and A edges black-to-white. It suffices
to show every white R vertex is reachable from t_0: flipping a simple
alternating path from t_0 to t exposes t instead and preserves every
other matching incidence.

First all white L_2 vertices are reachable by following the alternating
L_2 path. From t_0 its upward non-A edge enters U at black vertex
(4K-1,W-1), and the A edge reaches its white mate. At the bottom-left
white vertex (H-1,n_1) of L_2, the leftward non-A edge enters D at
(H-1,n_1-1), and its A edge reaches a white D vertex.

In a horizontally matched rectangle of at least two rows and positive
even width, all white vertices are mutually reachable by alternating
paths. To see this, contract each horizontal A pair. Vertically adjacent
pairs are connected in BOTH directions by two-step alternating walks.
Between adjacent column pairs the horizontal direction alternates with
row parity. An adjacent row and the bidirectional vertical connections
supply the reverse horizontal direction. Thus the contracted rectangular
array is strongly connected. This applies to U and D, so every white
vertex in both is reachable.

The white L_1 vertices before z are at (r,n_1-1) for even r=0,...,4K-2.
The white U vertex (r+1,n_1) reaches black (r+1,n_1-1), whose A mate is
(r,n_1-1). The remaining white L_1 vertices are (n_1-1,c) for even
c=0,...,4K. The white D vertex (n_1,c+1) reaches black (n_1-1,c+1),
whose A mate is (n_1-1,c). Therefore all remaining white R vertices are
reachable. The alternating flip proves the lemma. QED.

The lemma concerns the WHOLE outer matching. It handles competition for
boundary black vertices and the upper/left entrances of the second core.
No individually feasible path is assumed to extend without this argument.

## 4. Lower bound and simultaneous attainment

In any full N, each black centre is the endpoint of its own terminal path.
A terminal path cannot contain another Q vertex internally and has
opposite-colour endpoints. At most one centre can be HH because z is the
only white hole. Therefore at least one centre is TH. Its internal P
vertices remain in its own core and its cost is at least its rho_i.
Other TH components have nonnegative cost, giving

    f(N)>=min(rho_1,rho_2).

Choose a core j attaining the smaller rho. Take a simple optimal TH relay
from some t in T to h_j; t belongs to R. In the other core choose a simple
z-to-centre HH relay, which exists by Section 2. Their internal vertices
lie in DISJOINT P sets, and their two white endpoints t,z are distinct.
Each relay uses full actual M pairs internally. Select its auxiliary
edges, and double every actual M edge unused by either relay. This covers
exactly P union {h_1,h_2,z,t} without conflict.

Apply the outer lemma to obtain a direct perfect matching of R\{t}.
It covers precisely every remaining vertex. Its white endpoints are all
T, so these are direct TH components of fee zero. The unique HH relay
contributes zero to f regardless of its actual expense. The only paid
actual edges are those on the chosen TH relay, once each. Hence the
constructed full N attains f=rho_j, proving (1).

For (2), the only black Q terminals with possibly positive shortest T
expense are h_1,h_2: every black R vertex has a direct T neighbour, as
witnessed by A above. Their shortest fees are rho_1,rho_2. There is one
white HH source z, which can reach BOTH centres. Its maximum discount is
max(rho_1,rho_2), counting a zero-weight centre as zero. Consequently
Lambda=rho_1+rho_2-max(rho_1,rho_2)=min(rho_1,rho_2). This argument does
not select two incompatible free uses of z. QED.

## 5. Construction, complexity and scope of validation

`develop/shared_source_exact_completion.py` runs standard Dijkstra in the
REVERSED physical graph, from each black centre to its selected white
boundary targets. Black-to-white non-M steps cost zero; white-to-black M
steps cost the original weight. The lexicographic (expense,hops) key
prevents a zero-cost predecessor cycle. After choosing the paid core it
finds a relay from the other centre to z in the same way. It flips one
alternating path in the explicit outer near-perfect matching, doubles
unused actual edges, and returns the full N and its exact paid-edge set.

On these grids, three shortest searches, the outer alternating BFS and
reconstruction take O(v log v) arithmetic operations and O(v) memory.
The implementation accepts exact nonnegative INTEGER weights; the theorem
permits nonnegative reals. It is a standard shortest-path application and
an explicit geometry-specific extension theorem, not a new generic shortest-
path algorithm or general two-source routing solver.

The independent checker verifies outer white deletions, compares reverse
shortest fees with independent FORWARD Bellman-Ford distances, checks the
old physical component decomposition and generic capacity-one HH budget,
and exercises actual rematchings rather than just reweighting one M.
The recorded finite scope is in `output/shared-source-exact-completion.json`.
Arbitrary K,l, all rematchings and all nonnegative real weights follow
from Sections 2-4, not from finite enumeration. No new Lean or universal
numerical 5/6 improvement is claimed.

This closes the attainability question for this shared-source geometry.
For general positive ownership ambiguity, neither the outer deletion
lemma nor the independent-core relay construction is currently established.
