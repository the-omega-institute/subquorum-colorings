# Exposable ports, a coupled completion criterion, and a branched-source obstruction

Capacity-one HH-source matching prevents spending a white hole twice.
It does not by itself protect the white vertices needed to match the
remaining exterior. We give a constructive criterion coupling these two
requirements, and a feasible 18-by-18 source TREE where the uncoupled
budget is strictly smaller than the true TH optimum. The obstruction
already occurs with unit weights. On the same fixed footprint, positive
weights give an arbitrarily large gap. It refutes source-budget
attainment in general, not a numerical colouring target.

## 1. Hypotheses and the two exposable sets

Use the tagged actual/auxiliary matching model on a finite even rectangle.
Let actual grid matching M cover P, put Q=V\\P, and select a feasible
white T subset of Q: each t has at most one P neighbour and no T neighbour.
Write W=Q_white\\T for the white HH sources. All actual weights w are
nonnegative. Actual edges on TH terminal paths are paid; HH and P-only
components are free for f.

Assume the following conditions, explicitly testable from the physical data:

1. P is partitioned into r>=1 disjoint sets P_i. There is no grid edge
   between different P_i, and M covers each P_i internally.
2. There are r distinct black Q centres h_i. Every P neighbour of h_i
   belongs to P_i. A terminal path to h_i consequently has all its
   interior in P_i, or is a direct edge from a white Q neighbour.
3. |W|=r-1. Every h_i has a finite T-to-h_i alternating path. Its
   minimum actual expense is rho_i.
4. The HH incidence graph Gamma has left side W, right side I={1,...,r},
   and edge z--i exactly when z has an alternating relay to h_i with
   interior in P_i. Gamma has a matching saturating W.
5. In O=Q\\(W union {h_i}), the DIRECT bipartite grid graph G_O has a
   matching saturating all its black vertices. Its white side is T and
   has surplus one.

Neither Gamma nor the exterior needs to be connected or a path.
Edges in Gamma express physical local reachability, not independent
choices of already compatible routes.

Define two exposable sets:

    J = {j in I: Gamma has a matching of W onto I\\{j}},
    E = {t in T: G_O has a perfect matching of O\\{t}}.

Both are nonempty by assumptions 4-5. For each core let sigma_i be the
shortest T-to-h_i expense with its white source restricted to E, or
infinity if there is no such path.

**Standard matching exposure lemma.** Suppose a bipartite graph has
right surplus one and a matching A saturating its left side. Let a_0 be
its unmatched right vertex. Orient nonmatching edges right-to-left and
matching edges left-to-right. A right vertex a is exposable by another
left-saturating matching iff it is reachable from a_0.

Proof. A simple directed path to a can be flipped, matching a_0 and
exposing a. Conversely the symmetric difference with any matching
exposing a contains an alternating path between a_0 and a (or a=a_0).
Every other component is an even alternating cycle. QED.

Thus J and E are each found by ONE saturating matching and ONE alternating
reachability search. Exposing a requested vertex uses one path flip.
This uses ordinary bipartite matching, not a new matching algorithm.

## 2. Coupled completion theorem

**Theorem.** Under assumptions 1-5, the generic weighted HH-source budget
over ALL black Q terminals is

    Lambda = min_(j in J) rho_j.                            (1)

The minimum over full matchings in the following specified normal form is

    U_1 = min_(j in J) sigma_j:                             (2)

exactly one centre is TH, all other centres are HH, and every other
terminal path is a direct TH edge. P-only components may be replaced by
doubled unused M edges. Infinity means the normal form is impossible.
Whenever U_1 is finite,

    Lambda <= f* <= U_1.                                   (3)

In particular U_1=Lambda certifies the true full-N optimum and constructs
an attaining N. The criterion is weaker than requiring E=T.

If, in addition, every actual edge has STRICTLY positive weight and
every rho_i>0, then

    f*=Lambda  iff  U_1=Lambda.                            (4)

For nonnegative weights alone, equality U_1=Lambda is sufficient; we do
not assert its necessity. Nor is U_1 a general exact TH optimizer when
it exceeds Lambda.

The later note `TWO_NONTRIVIAL_TH_PATH_BOUND.md` gives a general
two-path lower bound and a fixed strictly positive-weight family with
f*=2 but U_1=K for every integer K>=3. This is an explicit failure of
global normal-form exactness; it preserves the restricted theorem here.

Proof of (1). Every black O vertex has a direct T neighbour witnessed
by its saturating matching, hence shortest TH fee zero. The centre fees
are exactly rho_i by core separation. The generic discount problem is
therefore maximum-weight matching in Gamma with benefit rho_i at i.

Any partial matching in Gamma can be augmented to cardinality r-1:
there is a saturating matching, and the usual augmenting-path argument
applies until maximum cardinality. An augmentation preserves the set
of already matched right vertices and adds one new right vertex.
Nonnegative benefits therefore never decrease. Some maximum-benefit
matching saturates W, omitting exactly j in J, so its benefit is
sum rho_i - min_(j in J) rho_j. This proves (1), including zero fees.

Proof of (2)-(3). Choose j in J, a relay from t in E to h_j, and a
source matching of W onto the other centres. Each matched pair has a
physical HH relay by the definition of Gamma. Interiors of different
relays lie in different P_i; all white endpoints are different and all
centres are different. Thus actual pairs and auxiliary incidences are
never shared. Add the relay N edges and double all unused M edges.
Exactly O\\{t} remains; an exterior matching exposing t covers it directly.
The only paid actual edges lie on the chosen relay. This constructs
every finite candidate in (2).

Conversely a full matching in the specified normal form determines a
root j in J, its TH source t in E, and expense at least sigma_j. Thus
(2) is the exact NORMAL-FORM optimum. The general source-budget theorem
and the constructed full N give (3).

Proof of (4). Let a full N attain Lambda. Its HH-centre paths induce
a matching in Gamma. Extend it to a W-saturating matching as above.
The omitted centre j lies among the original TH centres. Their paths
are distinct, and their actual-edge sets are disjoint, so

    f(N) >= sum_(TH centres i) rho_i >= rho_j >= Lambda.

If there were at least two TH centres, positive rho would make the
second inequality strict. Therefore exactly one centre is TH, its fee
is rho_j=Lambda, and all r-1 white holes are used on the other centres.
Every remaining terminal path is TH. It has zero expense because the
centre relay already spends the full budget. Strictly positive actual
weights force every remaining TH path to contain NO actual edge, hence
to be direct. Thus N has the specified normal form; (2) gives
U_1<=Lambda, and (3) gives equality. The reverse implication was proved
already. Nonnegative zero-cost extra TH relays are precisely why this
necessity proof needs strict positivity. QED.

The implementation uses iterative augmenting searches for the two
matchings, their exposure searches, and local reversed Dijkstra. Grid
degree bounds the total exterior edges and Gamma incidence by O(v).
Pad sets are constructed by scanning each disjoint core's neighbours.
The stated implementation takes O(v^2) arithmetic time and O(v) stored
words, v=|V|; integer bit costs are additional. Faster standard matching
algorithms could improve that matching step, but are not needed here.

## 3. A feasible five-core tree with a tight exterior chamber

Use the 18-by-18 board with zero-based rows and columns 0,...,17.
There are five scale-one odd squares S_i=a_i+[0,4]^2, in this order:

    a_0=(6,6),   a_1=(2,0),   a_2=(0,10),
    a_3=(10,12), a_4=(12,2).

Their centres are a_i+(2,2), and P_i=S_i\\{h_i}. The only white Q
vertices with more than one P neighbour are

    W={(5,10),(6,5),(10,11),(11,6)}.

Select all other white Q vertices as T. Thus |M|=60, |T|=98,
J_count=|M|+|T|=158=area/2-4. (J_count is distinct from the root set J.)
Each T has at most one P neighbour. No P edge crosses cores.
Corner-pad matching supplies both adjacent relays for every rematching.
Gamma is the incidence graph of the four-edge STAR on core 0 and arms
1,2,3,4; each white source has capacity one. Every core can be the
omitted root, so J=I.

Define the following explicit subset of O:

    D = ([0,1] x [0,9]) union ([2,5] x [5,9]),
    B_D = even-sum vertices of D,
    F   = odd-sum vertices of D.

There are exactly 20 vertices of each colour. Direct coordinate
inspection gives

    N_(G_O)(B_D) = F,       |B_D|=|F|=20.                  (5)

All remaining neighbours of B_D are P vertices or white HH sources.
Thus deleting ANY t in F leaves only 19 white neighbours for the 20
black vertices B_D. Hall's inequality prohibits an exterior matching.
In particular t_*=(5,8) is not exposable. This is an exact finite
coordinate certificate, not a numerical search extrapolation.

The supplied direct matching certificate saturates all 97 black O
vertices; alternating exposure gives E=T\\F (78 exposable whites).
The obstruction proof only needs (5), nonexposability of F, and the
explicit attaining full N; it does not require extrapolating this
finite exposure computation to other footprints.

## 4. Unit actual weights: Lambda=1 but the true optimum is 2

Use the explicit three local matching lists UNIT_CENTRAL, UNIT_NW and
UNIT_ARM in `develop/branched_source_obstruction.py`, translated by the
above origins. Use UNIT_ARM on arms 2,3,4. Every list contains 12 disjoint
grid edges covering its 24 P vertices. They are fixed witnesses; the
constructor does not enumerate matchings to define them.

An alternating path with just one actual edge has form t,b,w,h_i,
where w is a white neighbour of h_i, b is its M mate, and t is a selected
neighbour of b. Checking the FOUR possible w at each centre gives:

    centre 0: possible one-actual-edge T sources = {(5,8)},
    centres 1,2,3,4: no one-actual-edge T source.

Every centre has only P neighbours, so no centre path is direct.
Consequently rho_0=1, while the explicit length-five relays give
rho_1=rho_2=rho_3=rho_4=2. Since J=I, Lambda=1.

Suppose a full N had f=1. At least one centre is TH. It must be centre 0,
using its unique one-edge source t_*=(5,8). The other four centres must
be HH; they consume all four W sources once each. Every other TH path
must be direct because there is no paid actual edge left. Those direct
edges would match O\\{t_*}, contradicting (5). Hence f>=2.

The explicit attaining N uses the central TH relay

    (6,11),(6,10),(6,9),(6,8),(7,8),(8,8),

containing two actual edges. Assign each shared source to its own arm,
use one HH relay per arm, double unused M and use the provided exterior
matching exposing (6,11). All four holes and all actual resources have
single owners. This is a full N with f=2. Therefore

    Lambda=1,       f*=U_1=2.                              (6)

Source allocation was correct; the missing condition was simultaneous
exterior completion. Even a tree incidence graph and disjoint core
interiors do not suffice for budget attainment.

## 5. Fixed geometry, unbounded weighted budget gap

Now use the old canonical isolated-core matching in every square:
vertical pairs in local rows (0,1) and (3,4) in every column, and
horizontal pairs (2,0)-(2,1), (2,3)-(2,4) in the middle row.
Give the single edge

    e_* = {(6,8),(7,8)}

weight one and EVERY other actual edge integer weight K>=2.

The central path t_*=(5,8),(6,8),(7,8),h_0 has expense one.
Every other centre needs at least one actual edge, all its actual
weights are K, and its straight relay attains K. Thus

    rho=(1,K,K,K,K),       Lambda=1.                       (7)

If f(N)<K, no TH path can use an actual edge other than e_*.
At least one centre is TH, hence it is centre 0, and its path must be
the displayed t_*-to-h_0 path: e_* is its only actual edge and both
adjacent terminal edges are forced. The other centres are all HH,
consume all W sources, and every other terminal path must be direct.
Equation (5) again forbids the resulting exterior matching. Therefore
f(N)>=K for every full N.

To attain K, take the central TH relay

    (8,5),(8,6),(8,7),(8,8),

with its ONE K-weight actual edge. The HH source-to-arm assignment is
unchanged. The supplied exterior matching exposes (8,5), and unused
M edges are doubled. This full N has f=K. Hence on the SAME fixed
18-by-18 footprint, for every integer K>=2,

    Lambda=1,       f*=U_1=K.                              (8)

The multiplicative gap K and additive gap K-1 are unbounded. This is a
weighted fixed-footprint obstruction, not a unit-weight all-size gap
claim. It refutes equality of the source-capacity lower bound with the
physical TH optimum. The lower bound itself remains valid, and no
universal 5/6 or half-area numerical target is refuted.

## 6. Evidence and scope

The checker independently exhausts small abstract bipartite graphs to
test the standard exposure implementation, checks every white deletion
of the branch exterior using the older recursive matching routine,
compares independent forward core costs and the generic HH budget,
rescoring all constructed full N with the older tagged decomposition.
The explicit Hall set, one-edge source lists and attaining auxiliary
matching are saved as coordinate certificates. Seeded weighted and
rematched controls include zero and 401-digit weights and compare the
staircase specialization with its accepted solver.

The proofs of Sections 1-2 establish the criterion for arbitrary inputs
under its hypotheses. Sections 3-5 prove the stated concrete obstruction
and every K using exact coordinates, Hall's inequality and explicit
attainment; enumeration only discovered and checks the fixed witnesses.
No new Lean proof, general exact TH algorithm, or universal coefficient
improvement is claimed. The next problem is to incorporate exterior
Hall constraints into a stronger source budget, allowing several paid
paths and zero-cost noncentral relays when present.

Local command `python3 develop/check_exposable_source_completion.py`
passed all 4,165 small bipartite graphs (3,175 saturating graphs and
7,993 exposure flips), 98 independent exterior deletions, six positive
K controls including a 401-digit integer, 48 changed-M weighted branch
controls and 24 comparisons with the accepted staircase algorithm.
Among the 48 branch controls, 39 meet the budget and are certified
globally exact; four satisfy the strictly-positive nonattainment criterion.
The other cases are not labelled globally optimized by this normal form.
The readable coordinate certificates and complete auxiliary matchings
are in [`branched-source-coordinate-certificates.json`](../output/branched-source-coordinate-certificates.json);
the full validation scope is in
[`exposable-source-completion.json`](../output/exposable-source-completion.json).
The separate source/proof and execution review task
`5f87e45b-9ef5-41b8-bf14-b89fd2bb5cb7` ACCEPTED the supplied source
snapshot assembled at `5a7c154`, including the general criterion and
both exact obstructions. The reviewer executed the entire checker,
reproducing BOTH output files structurally and byte for byte, and
reports additional independent coordinate scripts checking the Hall
neighbourhood, one-edge sources and both full-N certificates. Remote
GitHub retrieval was unavailable to the reviewer; the receipt separates
supplied-snapshot review from remote identity verification. Full scope is in
[`exposable-source-review.json`](../output/exposable-source-review.json).
The predecessor staircase ACCEPT does not cover this new theorem or
the branched-source obstruction.
