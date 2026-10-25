# Shared guarded pockets: joint deficit and a full-pool cost obstruction

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The same-alpha hypothesis in the guarded-pocket replacement theorem matters.
We prove the geometric completion dichotomy with different boundary alpha
owners, give an exact simultaneous allocation and link-cost formula for any
finite pocket multigraph, and exhibit two actual completely frozen boards.
In the first, filling a shared pocket loses one payment in the pocket-only
interface, while outside intervals repair it for free. In the second, the
alphas have no outside interval support: the **full** whole-support optimum
still pays both, but its minimum link count rises strictly from zero to two.
Thus even full-pool cost-nonincreasing completion fails. Neither example
refutes universal compensation or improves the 5/6 bound.

The graph allocation argument specializes the elementary theorem in
[ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md](ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md).
The additions are its geometric completion adapter, joint minimum cost,
and verified frozen obstruction. We do not claim a new general matching
theorem, a frozen realization of every multigraph, or exterior repair for
all frozen boards.

## 1. Geometric dichotomy with two source owners

Use zero-based horizontal bands. Fix even r>=2 and interior columns s,s+1.
In the original feasible configuration (T0,M0), assume:

* u=(r,s), v=(r,s+1), d=(r+1,s), e=(r+1,s+1) are blank;
* x=(r,s-1), y=(r,s+2) are TP tips of original alphas A and B;
  A and B are allowed to coincide;
* t=(r+1,s-1), z=(r+1,s+2) are selected;
* a=(r-1,s), b=(r-1,s+1) and their within-band partners
  (r-2,s),(r-2,s+1) are old matching endpoints;
* old selections and **actual matching edges** are retained by the extension.

All listed positions lie on the board. Feasibility means a selected vertex
has at most one occupied neighbour; actual nearest-neighbour matching edges
are disjoint and avoid T. An extension may otherwise be arbitrary and need
not be completely frozen. Only standard outer boundary marks are imposed
on the strictly internal pocket intervals.

**Lemma 1.** In every feasible such extension either all four pocket vertices
stay blank, or the actual horizontal edge uv is added and d,e stay blank.
In the latter case uv forms a whole original two-endpoint beta E with empty
whole-body interval support W(E). Its only possible incoming TP links are
x->u and y->v. These two links are indeed candidates.

**Proof.** The retained selected t already sees x, so d cannot be occupied;
z and y similarly exclude e. The two old occupied neighbours x,a exclude
u from T, and b,y exclude v from T. If u is a new matching endpoint, its
mate can only be x,a,v,d. The first two retain fixed old mates, and d is
blank, so its mate must be v. Matching symmetry gives the reverse mate.
Starting with v gives the same dichotomy.

The lower partners of u,v are blank, so the two endpoints are BP tips and
uv is a whole beta. In the empty case the two adjacent BB columns each
give a different original singleton interval. In the filled case neither
BB column remains and neither pocket endpoint borders a remaining
endpoint-free gap: its other pocket column is now P and its outside
neighbour column is the fixed P column of x or y. Thus W(E) is empty.
The neighbours of u are x,a,v,d. Only x is a TP tip: a is permanently PP,
v is BP and d is blank. The argument for v is identical. QED.

The original A,B paths persist: retained actual mates and all old PP columns
keep their paths intact, and selected partners keep their TP ends from
acquiring PP continuations. In the empty case each of the two singleton
units has eligible open-owner set exactly {A,B}, or {A} if A=B.
Interval identities are coordinate triples (band,first,last), never separate
renumberings for different alphas.

**Lemma 2 (frozen completion).** If the original board is completely frozen,
adding only uv preserves feasibility and complete freezing.

**Proof.** The only selected neighbours of u or v could be their four grid
neighbours; these are respectively x,a,v,d and y,b,u,e, none selected.
Consequently adding the edge increases no old selected occupied degree.
Old freezing witnesses remain valid: T and every old actual mate persist,
so retaining the same order retains every witness. After all old endpoints
freeze, u sees the two distinct old endpoints x,a, and v sees b,y. Their
old mates have already frozen. Append u,v as one final freezing layer.
All endpoints are frozen. QED.

Lemma 1 generalizes the geometry of
[GUARDED_POCKETS_AND_MONOTONE_FORK_REPLACEMENT.md](GUARDED_POCKETS_AND_MONOTONE_FORK_REPLACEMENT.md).
It does **not** generalize that note's exclusive same-alpha replacement:
when A!=B, both sources can compete for the one new whole beta.

## 2. Exact joint pocket-interface theorem

Consider finitely many vertex-disjoint pockets satisfying Lemma 1, with
distinct coordinate interval identities and distinct filled actual edges.
Form the multigraph H whose vertices are the participating original alphas,
and whose edges are the pockets. A pocket between A,B gives an edge AB;
A=B gives a loop. Keep parallel pocket edges distinct. Optional isolated
alpha vertices are allowed.

Declare the **pocket interface** to consist of these alpha owners and only
the following resources and links:

* an empty pocket contributes its two original singleton intervals, each
  with incidence {A,B} (one distinct owner for a loop), at zero links;
* a filled pocket contributes its one whole beta E, incident through the
  two boundary TP links, at one link for any one alpha payment.

No other owner, interval, link or beta is part of this restricted interface.
This restriction is on certificates; the physical board is not deleted.
It excludes mixed relays and exterior resources by definition. Lemma 1
ensures no extra interval on E is silently available to fund a beta fork.
As W(E) is empty and there are no mixed owners, every legal primitive in
this interface is precisely one such interval or beta stem.

Write k=|V(H)|, let Z be the vertices incident to at least one empty edge,
write z=|Z|, and let t be the number of connected components that are
trees and whose edges are all filled. An isolated vertex counts as one
such tree. Loops and parallel cycles prevent a component from being a tree.
Let V be maximum payment and c the minimum total links at that payment.

**Theorem 3 (joint payment and exact cost).**

    V = k-t,                    c = k-t-z.                 (1)

Both ordinary and full beta-fork compensation have these optima. All z
sources in Z can simultaneously be paid at zero links in an optimum.

**Proof.** First assign distinct empty-pocket intervals to all vertices of
Z. For each vertex select one incident empty edge. Label the two interval
identities of every nonloop edge by its two endpoints, and give the vertex
the slot labelled by itself; for a loop use the first slot. Different
vertices selecting the same edge get different slots, and different edges
have different identities. Thus this is an injective zero-link assignment.

In each connected component meeting Z, run a multi-source BFS rooted at
all its Z vertices. Give every other vertex its parent edge. That edge is
filled: an endpoint of any empty edge would already belong to Z. Its
whole beta supplies one payment at one link. No two nonroot vertices can
choose the same parent edge: that would require them to be each other's
parent, contradicting strict decrease in BFS distance. No beta is an
interval identity. Thus this component is completely paid with exactly
n-|Z intersect component| links.

A connected component not meeting Z has only filled edges. If it is a
tree, root it arbitrarily and pay its n-1 nonroot vertices by their parent
edges. There are only n-1 resources in the entire component, so one
unpaid vertex is necessary. If it is not a tree, choose a spanning tree
and an edge outside it. Root at one endpoint of this extra edge, pay the
root with that edge, and pay the other n-1 vertices by tree parent edges.
The same argument includes a loop and parallel edges. This pays all n.
Every payment in these components costs one link.

Resources belong to only one connected component. Each all-filled tree
therefore has an unavoidable deficit one; other components have no deficit.
This proves V=k-t. Zero-link primitives can only pay vertices of Z, hence
any packing of value V costs at least V-z. The construction pays every
vertex of Z for free and every other paid vertex with one link, attaining
V-z. It also proves owner-disjointness: each primitive uses one alpha and,
if needed, one different beta. No two-BP fork can occur without W(E).
This proves (1) for both models. QED.

In particular an all-filled path of **arbitrary** length has deficit one,
an all-filled cycle has deficit zero, and leaving even one edge of a
connected tree empty removes its deficit. Counting one loss per filled
pocket is wrong for a joint chain. Counting two BP ends as two new units
is wrong even for one filled edge.

If e0,e1 are the numbers of empty and filled edges, the total resource
count R=2e0+e1 and unused count Q=R-V give the exact local ledger

    R-k = Q-t.                                             (2)

There is no additional credit for the unspent BP tip of a beta, for a
cycle, or for using the same original interval from its other side.

These formulas are exact for the declared interface. They give compatible
physical certificates whenever the hypotheses hold. They do not identify
the full-board optimum when other source exits, mixed relays or exterior
resources exist. A union with exterior certificates additionally requires
disjoint original owners and disjoint original resource identities.
Even when a block is fully paid locally, its cost need not be the cost
increment in the full system: an exterior interval can give a cheaper exit.

## 3. Actual frozen local value loss, repaired outside

Permanent fixture: `develop/fixtures/frozen_shared_pocket.json`.
It is a 16x14 board with 21 selected vertices and 18 actual edges (36 P),
all endpoints frozen. Its alphas have tip pairs

    A={(3,2),(8,4)},        B={(6,10),(8,7)}.

There are no betas, two mixed owners and five pure PP/M cycles. The only
old candidate links are mixed self-links. The shared pocket is r=8,s=5,
with selected guards (9,4),(9,7), and old PP guards (7,5),(7,6).
The two pocket interval identities are (4,5,5) and (4,6,6); each is
supported exactly by A,B. There are 59 available original units.

Add the actual edge ((8,5),(8,6)). There are now 38 frozen P, one new
empty-support beta and 57 available intervals: exactly the two pocket
identities have disappeared. The restricted interface changes

    (V,c): (2,0) -> (1,1).

The full pool instead has (V,c)=(2,0) on both boards. For example the
different old singleton identities (1,3,3) and (2,12,12) still give A,B
two simultaneous zero-link payments. Thus this is a genuine restricted
rule failure, not an unrestricted compensation counterexample.

For any q>=1 translate copies by (16i,0), 0<=i<q, and fill an arbitrary
subset S of their pockets. Blank separating rows prevent new inter-copy
matching or terminal links; whole-support gaps stay within their bands.
The old rank certificates transport and the added edges freeze last.
The copies therefore give, for every q and S,

    T=21q, P=36q+2|S|, M=18q+|S|,
    alpha=2q, beta=|S|, mixed=2q, I=59q-2|S|,
    pocket-only (V,c)=(2q-|S|, |S|),
    full-pool   (V,c)=(2q, 0),
    I+beta-alpha=57q-|S| > 0.                              (3)

The two explicit outside intervals in each copy remain internal and
unmarked under arbitrary even blank right padding. Their supports and
zero-link payments persist. The local dichotomy and restricted costs do
too. Numerical I counts in (3) are for the unpadded boards.

## 4. Tight support: full-pool minimum cost really increases

Permanent fixture: `develop/fixtures/frozen_shared_pocket_tight.json`.
The following board has 27 T and 72 P, with 36 actual edges recorded in
that file. P positions alone do not specify those edges.

```text
..............
..............
..T..T.T.T.T..
.TPPPPPPPPPPT.
..PPPPP.PPP...
.TPPPPPPPPP...
...PPPPP.PP...
...PPPPPPPP...
.TPPP..PPPPT..
..T.T..T.PP.T.
.T....T..PPPP.
..T...PT.PPPP.
.TPPPPP.TPP.T.
...PPPPT..PT..
.T.T.T....T...
..............
```

There are two alphas, three betas and five mixed owners. The alpha tips are

    A={(3,2),(8,4)},       B={(3,5),(8,7)}.

Both have whole-support set **exactly** {(4,5,5),(4,6,6)}. There are
32 available original intervals. Before filling, the full optimum is
(V,c)=(2,0). Adding the same actual edge uv=((8,5),(8,6)) gives 74
frozen P and removes exactly those two identities. Both alpha support
sets are now empty; no zero-link payment for either source remains.

Every full packing paying both alphas must therefore spend at least two
links. An interval stem beginning at an unsupported alpha needs an outgoing
link; a beta stem does too; a fork pays two sources with two distinct arms,
each containing at least one link. This lower bound allows all mixed
routes, all original intervals and all beta-body forks. It uses no pool
restriction and no finite search for optimality.

The lower bound is attained by the two explicit stems

    (3,2) -> (3,3), ending at the old beta {(3,3),(3,4)},
    (8,7) -> (8,6), ending at the new beta {(8,5),(8,6)}.

These have different alpha owners, different whole beta owners and
different physical terminals. They spend no interval. Consequently both
ordinary and full optima change exactly

    (V,c): (2,0) -> (2,2).                                 (4)

This is a completely frozen **full-pool** counterexample to the rule that
monotone shared-pocket completion cannot increase the minimum link cost
at unchanged full payment. It does not contradict the earlier same-alpha
fork replacement, which requires a specific fork rooted at the exclusive
source. The pocket-only payment still drops 2->1, but other old beta exits
repair that drop. The global target margin remains positive: I+beta-alpha
is 33 before filling and 32 afterwards.

For q vertically separated copies and an arbitrary filled subset S, the
same construction and one-link-per-unsupported-source lower bound prove

    T=27q, P=72q+2|S|, M=36q+|S|,
    alpha=2q, beta=3q+|S|, mixed=5q, I=32q-2|S|,
    full-pool (V,c)=(2q,2|S|),
    I+beta-alpha=33q-|S| > 0.                              (5)

There is no global shortage of payment in this family, despite an arbitrarily
large exact increase in minimum links. Arbitrary even blank right padding
does not add support to these alphas: all their original P boundary columns
and their two complete neighbouring gaps remain fixed strictly to the left
of the old right boundary. The lower bound and explicit stems therefore
persist; the I counts in (5) are for unpadded boards.

## 5. Verification, proof scope and remaining question

`develop/check_shared_pocket_completion.py` imports no SAT solver. It checks
2,912 graph states against ordinary/full flow and an independent resource
assignment DP, including loops and parallel edges; 135 use an independent
primitive packing optimizer. It also checks filled trees/cycles and one-empty
trees through 32 vertices. On 209 frozen physical boards it performs 418
restricted and 418 full-pool value/cost comparisons, 189 exact interval
identity deletion checks and 26 independent physical primitive packs.

`develop/check_tight_shared_pocket.py` reconstructs the second permanent
fixture without Z3, checks actual feasibility, strict transported freezing
certificates and independent closure, and verifies the explicit disjoint
beta stems and exact alpha support sets. On 213 frozen boards it performs
426 full-pool comparisons and 30 independent primitive packs, plus 213
independent strand reconstructions and exact interval identity deletion
checks, including all
fill subsets through six copies, additional copies through twelve, eight
padding controls and sixteen isometries carrying the band convention.
The fixtures include actual matching edges and freezing layers. The
optional discovery script and its two SAT receipts are retained separately;
none is used as an all-size proof.

`formal/SubQuorum/SharedPocketJointDeficit.lean` uses Lean 4.33.0 with no
`sorry`. It formalizes parent-edge injectivity from actual endpoint pairs
and strict distance descent, disjoint interval/beta resource tags, distinct
empty-pocket slots, and the arithmetic consequence of explicit value/cost
count hypotheses. It does **not** formalize BFS existence, the graph
allocation theorem, the full geometry or the frozen board reconstruction.
Those are written proofs with separate computational controls. Exact axiom
output and the solver-free validation manifests are under `output/`.

The next geometric question is whether every all-filled deficient pocket
tree in a completely frozen board has a jointly usable exterior exit,
after private protected singletons have been eliminated. The tight fixture
shows that exterior repair can require two links even for one shared pocket.
Separate reachability of exits is insufficient: shared mixed owners, whole
betas and original intervals must each be reserved once across all residual
trees. The universal compensation theorem and the 5/6 improvement remain open.

The sequel [POCKET_TREE_EXTERIOR_COMPRESSION.md](POCKET_TREE_EXTERIOR_COMPRESSION.md)
now reduces these trees to a jointly capacitated exterior network: one
residual source chooses any original alpha exit in its tree. Maximum payment
is preserved after adding the internal baseline. Unsupported alphas also
give exact minimum links; arbitrary direct support needs the discounted
circulation correction. No exterior saturation theorem is assumed.
