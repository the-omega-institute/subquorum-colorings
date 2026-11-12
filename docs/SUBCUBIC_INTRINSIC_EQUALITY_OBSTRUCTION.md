# Alternating interface cycles exclude subcubic gap equality

12 November 2026. All graphs are finite, simple and bipartite.
A dissociation set induces maximum degree at most one; its maximum size
is beta_2. A two-star-forming set covers every unselected vertex by a
not necessarily induced K_(1,2) with exactly two selected vertices.
SF_2 is the maximum size of an inclusion-minimal such set.

**Theorem 1.** Every nonempty bipartite graph G of maximum degree at most
three satisfies

    SF_2(G)-beta_2(G) <= ceil(|V(G)|/10)-1.                    (1)

Thus positive unrounded equality in the universal n/10 gap bound requires
maximum degree at least four. There is no connectivity hypothesis. For
orders not divisible by ten, (1) is the previously proved floor(n/10)
bound. For orders divisible by ten it removes the equality case. It does
not give a smaller asymptotic coefficient for all subcubic graphs.

The proof supplies a quantitative improvement for the entire degree-three
intrinsic template, without assuming paired-neighbourhood expansion.

## The template and its alternating cycles

Fix k>=1. The layers I,C,X have respective orders 2k,4k,4k. Each layer is
balanced between the two bipartition sides. Each vertex of I has two
neighbours in X; these disjoint pairs partition X. Write P for the
auxiliary perfect matching pairing those two neighbours, and i(P) for
their common centre. The edges of P are auxiliary same-side pairs, not
edges of G. The edges C--X form a perfect matching, with c(x) the core
owner of x. The remaining graph edges are a simple bipartite two-regular
core F=G[C] and a perfect matching Q=G[X]. There are no other edges.

The graph G has n=10k and degrees two on I and three on C union X.
S=I union C has size 6k and is inclusion-minimal forming. Each x has
selected neighbours c(x),i(P(x)). Deleting i makes that omitted vertex
uncovered, since it has no remaining selected neighbour. Deleting c
leaves its witness x with just its isolated selected neighbour i.
These are literal deletion failures and prove minimality.

The auxiliary graph P union Q is a disjoint union of alternating cycles
of lengths 4 ell. Indeed P preserves the graph bipartition side and Q
switches it; every cycle therefore contains an even number of Q edges.
Each such cycle has ell P-pairs on each side. Let

    k0 = number of cycles with ell=1,
    t  = sum of ell over cycles with ell>=2 = k-k0,
    delta = sum over all cycles of floor(ell/2).

**Theorem 2.** Every graph in this template has

    beta_2(G) >= 5k + max(delta, ceil(k0/4))
              >= 5k + ceil(k/7).                            (2)

Both alternatives in the first bound are attained as lower certificates
by explicitly constructible dissociation sets. They are alternative sets;
their improvements are not added or spent simultaneously. No sharpness
of either coefficient is asserted.

## The one-core-side construction

Select all C_A and no C_B. For a union T of P-pairs in X_B, let J be
its collection of pairs and let z(J) count P-pairs in X_A wholly contained
in N_Q(T). Keep T and the I_A centres whose pairs are disjoint from T.
Every vertex of T is paired with its selected core owner. Omit N_Q(T).
For each I_B-centred pair retain its centre and one available witness
if any is available, and just its centre otherwise. These choices form
a dissociation set: selected X_B vertices have no selected Q-neighbour
or I_A centre, and every retained X_A vertex is paired only with its
I_B centre. Its order is exactly

    2k + 2|J| + (k-|J|) + (2k-z(J)) = 5k+|J|-z(J).          (3)

On an alternating 4 ell-cycle, contract each X_B P-pair to a vertex.
Each X_A P-pair records the two neighbouring contracted vertices. For
ell>=3 this is a cycle of length ell, for ell=2 two parallel edges,
and for ell=1 a single loop. Thus z(J) counts edges whose two ends
are in J, with the loop counted when its vertex is in J. The maximum
of |J|-z(J) is floor(ell/2). For ell=1 it is zero. For ell>=2, a proper
nonempty selection has |J|-z(J) equal to its number of cyclic runs;
each run requires an omitted vertex and hence there are at most
floor(ell/2). Alternating selected and omitted vertices attain this
value, including the two-vertex parallel-edge case. The empty and full
selections both give zero. Choose the maximizing pairs independently
on each alternating component. Equation (3) proves the delta bound.
In particular delta>=t/3, since floor(ell/2)>=ell/3 for ell>=2.

## Complementary phases and low-degree core vertices

Independently choose one of the two bipartition classes of each even
cycle P union Q, with probability one half each. Their union Y contains
exactly one endpoint of every P edge and every Q edge. Put

    R = C minus {c(x):x in Y}.

Thus |Y|=|R|=2k. For any dissociation set Z of F[R], the set

    I union Y union Z                                      (4)

is dissociation in G and has order 4k+|Z|. Each selected I vertex is
paired with its sole chosen witness; Y has no Q edge, and the owners
of Y were all omitted. Core vertices in Z see no selected witness.

Let L(R) count vertices of degree at most one in F[R]. A path on m
vertices has dissociation number ceil(2m/3), by omitting every third
vertex and the converse three-consecutive-vertex bound. A cycle of
even length m>=4 has dissociation number floor(2m/3), by the analogous
cyclic count and a cyclic pattern of runs of length at most two. A
path contributes at least m/2 plus one quarter of its vertices of
degree at most one: for m=1 the two sides are 1 and 3/4; for m=2 they
are 2 and 3/2; for m>=3 use m/6>=1/2. An even cycle contributes at
least m/2. Summing over the path and cycle components of F[R] gives

    beta_2(F[R]) >= |R|/2+L(R)/4 = k+L(R)/4.                (5)

Consider any core vertex v whose owner-mate x lies in a length-four
P union Q component. Conditional on v being in R, that component's
phase is fixed. Exactly one core vertex on each original bipartition
side in that component belongs to R. The two distinct F-neighbours of
v therefore cannot both belong to R if both are in its own component.
Otherwise at least one neighbour belongs to another independently
phased component, and its conditional probability of belonging to R
is one half. In all cases

    Pr(deg_(F[R])(v)<=1 | v in R) >= 1/2.

The probability v is in R is one half. There are 4k0 such v, so by
linearity of expectation E[L(R)]>=k0. Independence between these events
is neither asserted nor needed. Some phase assignment has L(R)>=k0;
(4)--(5) give beta_2(G)>=5k+ceil(k0/4).

The construction is deterministic in polynomial time by conditional
expectations. Each indicator counted in this expectation depends on
at most the three component phases of v and its two F-neighbours.
Fix phases one at a time, choosing a value that does not decrease the
conditional expectation. Each local expectation is computed from at
most eight completions. The final count is at least its original
expectation, hence at least k0. Paths and cycles then give Z explicitly.

Together the two constructions prove the first part of (2). If
M=max(delta,ceil(k0/4)), then t<=3 delta<=3M and k0<=4M, so k<=7M.
Integrality proves M>=ceil(k/7), completing Theorem 2.

## Excluding every subcubic equality graph

The proved intrinsic equality theorem states that any graph with
SF_2-beta_2=n/10>0 has n=10k, SF_2=6k, beta_2=5k, and precisely the
layers above, with minimum core degree at least two and minimum
interface degree at least one. If its maximum degree were at most
three, the C--X owner edge forces every core degree to be exactly two.
Each witness already has one I neighbour and one core owner, so its
interface degree must be exactly one. The graph is therefore a template
of Theorem 2, which gives beta_2>=5k+ceil(k/7)>5k, a contradiction.

Now the universal bound gives SF_2-beta_2<=floor(n/10). When 10 does
not divide n, this is (1). When n>0 is divisible by ten, the excluded
equality is positive, so integrality strengthens it to n/10-1. This
proves Theorem 1 for all nonempty graphs, including disconnected ones.

The dependencies are the written proofs in
[the universal bipartite bound](SHARP_BIPARTITE_STAR_FORMING_GAP.md) and
[intrinsic equality recognition](INTRINSIC_STAR_FORMING_EQUALITY.md).
The quantitative template bound is for its specified 6k-set. A maximum
minimal set of an arbitrary subcubic graph need not have these layers.
The cubic selected-star existence question, a sharp general subcubic
coefficient, and rectangular-grid equality are separate open questions.

## Verification

`python3 -B scripts/check_subcubic_intrinsic_obstruction.py` builds
physical graphs, checks literal formation and every selected deletion,
constructs both dissociation certificates and the conditional-expectation
phases, and compares finite optima with an independent exact solver.
The general theorems have the proofs above; finite controls test the
algorithm and its boundary cases. The report and exact-source review
record their actual execution scopes. No new Lean verification is claimed.

The checker exhausts the two labelled k=1 templates and all 90 labelled
two-regular cores times 24 matching interfaces at k=2: 2,162 models in
total. Their unrestricted optima are computed by an excluded/isolated/
paired recurrence and independently by the private-neighbour formula.
The k=1 cases also use all 2,048 literal vertex subsets. All 5,764 phase
assignments of those exhaustive models are checked against independently
optimized residual cores. Sixty seeded templates use k=3,4,5,7,8, with
full unrestricted optimization for the twelve k=3 controls. Nine larger
templates use k=16,64,256, up to 2,560 vertices; they check the physical
certificates, not exact unrestricted optima. Thirty-five path/cycle models
test the constructive residual optimizer. The report includes a complete
20-vertex graph with selected size 12 and exact beta_2=11.
