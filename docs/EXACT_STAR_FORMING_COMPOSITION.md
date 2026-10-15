# Exact star formation under arbitrary interfaces

15 October 2026. This note strengthens the cyclic gap construction: its exact
upper star-forming number is six times the number of copies, for every finite
interface relation. The proof bounds every minimal set separately inside
each copy. It uses no enumeration for an all-size conclusion.

## Definitions and construction

Use the graph H from [the earlier note](CONNECTED_STAR_FORMING_GAPS.md), with
parts a1,...,a5 and b1,...,b5 and cross-edge matrix

    11001
    11010
    00011
    01111
    10111

Its degrees on either side are (3,3,2,4,4). Let p=a1 and q=b1 be the only
vertices allowed to have neighbors outside the copy. A set S is 2-star-forming
if every x outside S lies in a non-induced two-leaf star in S union {x};
SF_2 is the largest size of an inclusion-minimal such set. The exact local
test is d_S(x)>=2 or a selected neighbor of x has a selected neighbor.
The dissociation number beta_2 is the largest size of a set inducing maximum
degree at most one.

**Theorem.** Let I be any finite index set and R any directed relation on I.
Take induced copies H_i and add an edge b1^(i)--a1^(j) for every R(i,j).
Loops in R add an edge already in H, and repeated specifications have no
effect. For the resulting simple graph F_R,

    beta_2(F_R)=5|I|,          SF_2(F_R)=6|I|.

In particular the earlier cyclic and chain families have exact gap |I|.
For a directed cycle on r>=2 indices, the graph is two-connected, has
maximum degree four and order 10r, and has gap exactly |V|/10.

The upper-bound argument is stronger: in any finite graph containing an
induced H whose external edges touch only a1,b1, every inclusion-minimal
2-star-forming set uses at most six vertices of that copy. The outside
graph is otherwise unrestricted and need not be bipartite.

## Dense sets: star formation reduces to domination

**Lemma 1.** In H, if |T|>=6, then T is 2-star-forming if and only if every
vertex outside T has a neighbor in T.

The forward implication follows directly from the star definition. For the
reverse implication, suppose x outside T has exactly one selected neighbor
u and u has no selected neighbor. Write Q=V(H) minus T, so |Q|<=4. Both
N(x) minus {u} and N(u) lie in Q. These sets are disjoint because H is
bipartite. Every edge xu of H satisfies d(x)+d(u)>=6: the degree-two
vertices a3,b3 have only degree-four neighbors, and every other vertex
has degree at least three. Thus

    |Q| >= (d(x)-1)+d(u) >= 5,

a contradiction. A vertex with two selected neighbors is itself a star
centre, and a vertex with one selected neighbor can use that neighbor as
centre. This proves the lemma.

## A removable internal vertex in every dense selection

Write N[x]={x} union N(x). The only closed neighborhoods of size at most
four are

    Z_a3 = {a3,b4,b5},             Z_b3 = {b3,a4,a5},
    Z_a1 = {a1,b1,b2,b5},          Z_a2 = {a2,b1,b2,b4},
    Z_b1 = {b1,a1,a2,a5},          Z_b2 = {b2,a1,a2,a4}.

The two triples are disjoint. Any two distinct displayed quadruples have
intersection of size at most two. The four remaining closed neighborhoods
have size five.

**Lemma 2.** Let U subset V(H), |U|>=7, and suppose U dominates H. There
is v in U minus {p,q} such that

1. U minus {v} is 2-star-forming inside H;
2. if a selected port has a selected neighbor inside U, it still has a
   selected neighbor inside U minus {v}.

Put W=V(H) minus U, so |W|<=3. Call a candidate v bad for domination if
U minus {v} fails to dominate. This happens precisely when some closed
neighborhood N[x] lies in W union {v}. Since U dominates, N[x] is not
contained in W. Thus v is the unique member of N[x] not in W.

At most one candidate can complete one of the two triples: each completion
requires at least two members of that triple in W, and the triples are
disjoint. At most one candidate can complete a quadruple: it requires
|W|=3 and W contained in that quadruple; two quadruples cannot both contain
the same three-element W. A size-five closed neighborhood cannot be covered
by W union {v}. At most two candidates are therefore bad for domination.

For each port there is at most one candidate whose deletion destroys its
internal selected-neighbor activity: that candidate must be the port's
unique neighbor in U. Hence at most two more candidates are bad for port
activity. There are at least |U|-2>=5 candidates outside the ports, and at
most four bad candidates in total. Choose a remaining v. Its deletion
preserves domination, and |U minus {v}|>=6, so Lemma 1 gives star formation.
It also preserves the required port activity. This proves the lemma.

This counting argument may overcount bad vertices, which only strengthens
the conclusion. Each port contributes at most one bad vertex; the proof
never allocates the same resource independently to several deletions.

## The local upper bound survives every allowed outside graph

**Lemma 3.** Let G contain an induced copy of H, with external edges
incident only at p,q. If S is inclusion-minimal 2-star-forming in G, then
|S intersect V(H)|<=6.

Suppose U=S intersect V(H) has size at least seven. First U dominates H.
Otherwise x outside U has N[x] contained in W=V(H) minus U, where |W|<=3.
The displayed closed-neighborhood list forces x=a3 or b3. Such a vertex is
not a port and has no selected neighbor anywhere in G, contradicting
star formation of S.

Take v supplied by Lemma 2 and put S'=S minus {v}. Every vertex of this
copy outside S' has a witnessing star entirely inside the copy, since
U minus {v} is star-forming there. Now take x outside the copy and outside
S'. Before deletion it had a star in S union {x}. If this star avoids v,
it remains. If it contains v, the fact that x is not adjacent to the
non-port v forces v to be a leaf and the centre to be a selected port u.
The other leaf is x. Since u had the selected internal neighbor v,
Lemma 2 gives a selected internal neighbor w after deletion. The star
with centre u and leaves x,w remains in S' union {x}.

All vertices outside S' are covered, so S' is star-forming, contrary to
minimality. The lemma follows.

## Exact values for arbitrary finite interfaces

Apply Lemma 3 separately to all copies. Every minimal star-forming set
has at most 6|I| vertices. Conversely the union of

    {a1,a2,a3,b1,b2,b3}

over the copies is minimal of size 6|I|. Each outside vertex has its
original two selected neighbors. The six deletion failure witnesses remain

    a1 -> b5, a2 -> b4, a3 -> a3,
    b1 -> a5, b2 -> a4, b3 -> b3.

The sole possible selected centres after a core deletion are a3,b3; they
remain isolated in the selected set because interfaces touch only a1,b1.
Thus all deletions fail. Upward closure makes this inclusion-minimal.
Therefore SF_2(F_R)=6|I|.

Every dissociation set restricts to one of size at most five in each H_i,
by the earlier exact base proof. All A vertices form an independent set
of size 5|I| because every added edge goes from B to A. This gives
beta_2(F_R)=5|I| and proves the theorem. Empty I gives both values zero.

For completeness, removing any one vertex from a cyclic family leaves
its own H copy connected through the Hamilton cycle displayed in the
earlier note, and destroys at most one interface. The remaining interfaces
connect all copies, including r=2 where at least one of the two distinct
interfaces remains. Each port degree rises from three to four. This
recovers the two-connectivity and maximum-degree assertions.

## Scope

This settles the exact SF_2 value left open in the earlier cyclic note and
shows it does not depend on the interface topology. It establishes a
specific composition theorem, not a classification of all strict-gap
graphs or an optimal gap coefficient for all bipartite graphs. The sharp
global bound, comparison with upper domination, computational complexity
and rectangular-grid triple equality remain separate questions.

Finite controls and any accompanying kernel-checked local certificate
are checks of the explicit graph facts. Lemmas 1--3 and the composition
proof above are the general argument and do not extrapolate from finite
families.

## Reproduction

The [three-page PDF](../output/pdf/starforming-composition-note.pdf) includes
the base definition, deletion table, beta_2 proof and the full composition
argument. Its source is [the LaTeX note](starforming-composition-note.tex).

```sh
python3 scripts/check_starforming_composition.py --output output/starforming-composition-controls.json
python3 scripts/check_starforming_formal.py --lean /path/to/lean-4.33.0 \
  --package-cache /path/to/matching/.lake/packages --composition \
  --output output/starforming-composition-formal-check.json
```

The Lean development starts with the literal star/local-test equivalence in
[Amplification.lean](../formal/StarForming/Amplification.lean).
[Composition.lean](../formal/StarForming/Composition.lean) checks the fixed
local deletion certificate by kernel reduction and proves the general
external-star replacement and per-block upper-bound theorems.
[ExactCard.lean](../formal/StarForming/ExactCard.lean) sums the per-block
bound and exhibits an attaining minimal set. The written local proof above
derives the deletion certificate by neighborhood counting independently of
that kernel enumeration. The dissociation optimum and two-connectivity
remain written proofs rather than claims of newly completed formalization.

The Python control checks all 174 dominating local selections of size at
least seven and 29,656 safe global deletions in 60 deterministic surrounding
graphs, including nonbipartite ones. Its input graph agrees with the earlier
literal-star checks. These controls do not replace the general proof.
