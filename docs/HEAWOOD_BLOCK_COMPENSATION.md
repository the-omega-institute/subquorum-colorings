# Two units per Heawood block: a general compensation theorem

19 October 2026. This note proves SF_2(L_k)=36k for every k>=1. More
generally, disjoint broken Heawood blocks attached to distinct core
ports force two units each in the cubic private-witness budget. The
proof uses selected isolates and actual unused witness capacity, not
an assumption that every directional signal forces a lost block vertex.
No improved sub-quorum coloring bound for rectangular grids is claimed.

## The theorem and hypotheses

All graphs are finite and simple. Two-stars are non-induced, and minimal
means inclusion-minimal. Let G be cubic and bipartite, with its vertices
partitioned into a core K and b disjoint blocks B_j. Each B_j is the
Fano incidence graph H with an incident point-line edge P_j L_j removed.
Each of its two ports has exactly one neighbor in K, and these are all
edges from the block to the rest of G. Every core vertex is adjacent to
at most one block. In particular the two core neighbors of a block are
distinct, and their remaining neighbors lie in K. The core itself need
not be connected or regular as an induced subgraph.

Throughout, beta_2 is the maximum cardinality of a dissociation set,
equivalently a selected set inducing maximum degree at most one. It is
not the minimum forming-set cardinality.
An active selected vertex has at least one selected neighbor; a high
has at least two. The block ports P,L are distinct from their adjacent
core attachment vertices a,b.

**Theorem.** Every minimal forming selection S satisfies

    5|S|+2b <= 3|V(G)|.

Thus SF_2(G)<=floor((3|V(G)|-2b)/5). The distinct-core-port condition
is part of the theorem: it prevents charging a single core isolate to
several blocks and prevents a length-two witness from crossing two blocks.

For L_k there are3k blocks and62k vertices. The theorem gives |S|<=36k,
and the established uniform witness attains36k. Consequently

    SF_2(L_k)=36k,
    beta_2(L_k)=33k+floor(k/2),
    SF_2(L_k)-beta_2(L_k)=3k-floor(k/2).

This removes the previous additive uncertainty
floor(2floor(k/2)/7) in the SF upper bound for larger k. Its asymptotic
gap coefficient is5/124, below the existing1/24 construction; enlarging
this long-core architecture therefore does not improve that coefficient.

## The exact cubic witness budget

Fix a minimal S and put a(v)=|N(v) intersect S|. A selected high vertex
has a(v)>=2 and demand a(v)-1. An omitted resource x has capacity
c(x)=3-a(x). Every high has an omitted deletion-failure witness, and
different highs have disjoint sets of possible witnesses. These are the
general graph lemmas in [RegularBound.lean](../formal/StarForming/RegularBound.lean).

The exact failure classification, independently formalized in
[PortReturn.lean](../formal/StarForming/PortReturn.lean), gives three types:

1. An adjacent omitted vertex with just the high as selected neighbor.
2. An adjacent omitted vertex with the high and a selected isolate as
   its two selected neighbors.
3. A nonadjacent omitted vertex with a unique selected neighbor, a leaf
   whose unique selected support is the high.

In the second type, bipartiteness ensures that the other selected
neighbor is already isolated before deletion. A resource with one
selected neighbor has capacity two; one with two has capacity one.
The capacity always pays the high's demand: an adjacent high has
selected degree two, while a degree-three high must use the third type.

Choose one witness f(v) for each high. Witness disjointness makes this
map injective. Pay the entire demand at f(v), and write W>=0 for total
unused capacity. If i counts selected isolates, the exact identity is

    3n-5|S| = i+W.                                      (1)

Indeed total demand is sum_(v in S)a(v)-|S|+i, total resource capacity
is3(n-|S|)-sum_(x outside S)a(x), and the sum of all a(v) is3|S|.
This is the established [degree-capacity identity](REGULAR_STAR_FORMING_BOUND.md),
with each resource used once. We will show i+W>=2b.

## Local account at one block

Write s_B=|S intersect B| and delta_B=8-s_B>=0; nonnegativity is the
established ambient [robust block cap](EXACT_CUBIC_COMPOSITION.md).
Let q_B count selected block ports, p_B selected adjacent core vertices,
i_B selected isolates in B measured globally, and W_B unused capacity
on omitted vertices of B.

Let E_B be demand of core highs paid by block resources, and I_B demand
of block highs paid by core resources; put F_B=E_B-I_B. Every crossing
witness has length at most two. A core vertex has only one block edge,
so no such witness can reach a second block.

Summing selected-neighbor incidences in B gives

    sum_(v in B) a(v)=3s_B-q_B+p_B.

The sign tracks an outgoing incidence for each selected block port and
an incoming incidence for each selected adjacent core vertex. Hence

    W_B+F_B=42-5s_B-i_B+q_B-p_B.                         (2)

For example, block resource capacity minus block high demand equals
42-5s_B-i_B+q_B-p_B; the same difference is W_B+E_B-I_B by the
chosen witness payments.

Let t_B count selected isolated core vertices adjacent to B. We prove

    F_B+p_B-q_B <= 5delta_B+t_B.                        (3)

Combining (2), (3) and s_B+delta_B=8 gives

    i_B+W_B+t_B >= 2.                                  (4)

The terms in (4) are actual isolates or residual capacity. They are
not the overlapping bare-port/import lower certificates previously
shown unsafe to add.

## Four available local facts

These follow from the preceding complete Fano proofs; no enumeration
is a premise. The [bare-port theorem](BARE_HEAWOOD_PORT_COMPENSATION.md)
and [saturated transfer theorem](SATURATED_HEAWOOD_TRANSFER.md) apply to
arbitrary ambient restrictions, not just internally minimal sets.

**H1.** At size eight, no port is omitted together with both its
internal neighbors. This is |C|+t<=8 with one bare port.

**H2.** At size eight, a selected port with no selected internal neighbor
and a selected external neighbor has no internal omitted neighbor whose
unique selected neighbor is that port. Otherwise the oriented clause
B_(z,q) at that omitted neighbor z and selected port q is private to
the selected external vertex. The saturated transfer theorem says its
port must instead be omitted, a contradiction. This includes a selected
K_2 across the interface.

**H3.** If an omitted port has a selected external neighbor and exactly
one selected internal neighbor, a global isolate, then the eight-selection
is a six-cycle and two non-port isolates. The opposite port lies on the
cycle, its two internal neighbors are selected highs, and it must import
demand one or two according as its external neighbor is omitted or
selected. The external owner need not be active.

To see the last assertion, its clause B_(q,T) is private to the external
vertex, so the eight-template classification applies. The opposite port
has two selected internal neighbors, each retaining a second selected
neighbor after its deletion. There is no omitted internal neighbor at
all. Its failure witness is therefore in the core, as proved in the
general protected-port return theorem. Its selected degree is two or
three, giving precisely the displayed import demand.

**H4.** If both ports are omitted with neither having an internal
selected neighbor, then s_B<=6. This is the two-bare-port theorem.

## Blocks of size at most seven

At a port interface write q for selection of the block port and p for
selection of its adjacent core vertex. Exports at one interface total
at most two. The possibilities for E_interface+p-q have bounds

| Core vertex | Block port | Upper bound |
|---|---|---:|
| Omitted | Either | 0 |
| Selected | Selected | 2 |
| Selected | Omitted | 3 |

An export through a selected port uses that port as a selected leaf of
a core high, and an internal resource with just that port selected.
An export through an omitted port uses the port itself as the resource,
directly for its selected core high or through its selected core leaf.
In either case there is at most one high owner at that interface, and
its demand is at most two.

The value three requires an omitted port with no internal selected
neighbor: its capacity two pays a degree-three high through a selected
core leaf. Thus E_B+p_B-q_B<=6. If delta_B>=2 this is at most5delta_B.
If delta_B=1, exceeding five would require value three at both ports;
H4 forbids that when s_B=7. Since imports are nonnegative, (3) follows
for every s_B<=7, without using t_B.

## Closed Heawood eight-selections

We need one structural consequence of established general inequalities.

**Lemma.** Every minimal forming eight-set in the closed Heawood graph
is one selected six-cycle plus two isolates. Each omitted vertex has
exactly one selected cycle neighbor and one selected isolate neighbor.

**Proof.** The maximum dissociation cardinality beta_2(H)=7 is established
by the Fano saturation proof.
The [bipartite isolate inequality](AUGMENTED_ISOLATE_COMPENSATION.md)
gives16<=14+i, while (1) gives40+i<=42. Hence i=2 and W=0.

A leaf of a high has an adjacent private resource with selected
neighborhood consisting of that leaf and possibly an isolate. A two-
neighbor resource of this kind cannot pay any high and would leave
positive unused capacity. Thus every such leaf has a one-neighbor
resource, which must pay its parent high. That parent has degree three;
degree two would leave one unused unit. It has exactly one leaf: two
leaves would have distinct one-neighbor resources but only one can pay
their common high, again leaving unused capacity. Conversely a
degree-three high has all its graph neighbors selected, so no adjacent
omitted witness is available. Its failure witness must be the third
type in the exact classification, through a selected leaf whose sole
selected support is that high. Thus every degree-three high has
exactly one leaf, and every degree-two high has none.

The graph induced by highs is consequently two-regular. It is nonempty,
since otherwise every selected vertex would have selected degree at
most one. The eight-selection would itself be a dissociation set,
contradicting the maximum dissociation cardinality beta_2(H)=7.
Girth six and only six selected nonisolates force exactly
one high six-cycle and no leaves or matching components. Each high
needs a distinct resource; all six omitted vertices are therefore
two-neighbor resources, with that high and an isolate selected. QED.

## Eight-selections: cases with zero or two selected ports

If q_B=2, H2 excludes all exports: a selected port can mediate an export
only as an internally isolated selected leaf with an internal one-neighbor
resource. A resource with two selected neighbors cannot fail when the
external core high is deleted: both its selected block neighbors remain.
It therefore cannot export through a selected port. The one-neighbor
resource must be supported only by that port, whose selected activity
comes only from the external high; H2 excludes precisely this case.
Hence E_B=0 and F_B<=0<=q_B-p_B+t_B, proving (3).

If q_B=0, first restrict to B. The exact
[attachment certificate](PRIVATE_CLAUSES_AND_BOUNDARY_ACCOUNTING.md)
states: whenever an inside graph retains all its edges in the ambient
graph and every non-port has exactly its inside neighbors, each selected
non-port of an ambient minimal set either owns a private inside clause,
or is the sole selected inside neighbor of a selected port. There is no
inside-formation hypothesis and no restriction on the ambient core's
selection or edges. It is also the general graph-level theorem
[boundary_certificate](../formal/StarForming/PrivateClauses.lean).
Apply it with inside graph B and its two ports. The second alternative
is impossible because both ports are omitted. Thus every selected
vertex of B has an internal private clause.
Formation also holds internally. A port with no selected internal neighbor
is excluded by H1. A port with just one internally isolated selected
neighbor would either fail global formation if its external neighbor
were omitted, or force the opposite port selected by H3. All other
port configurations already form internally.

Restore PL. Both endpoints are omitted, so adding this edge changes
neither formation nor any deletion test. We have a minimal closed-Heawood
eight-set, of the classified cycle-and-two-isolates form. If an external
core neighbor of either port were selected, that omitted port would
have three selected neighbors. The cycle high attached to that resource
would lose its unique witness. It has two high cycle neighbors and no
selected leaf, so has no alternate transferred witness. This contradicts
global minimality. Thus p_B=0. There are no exports, and (3) follows.

## Eight-selections: exactly one selected port

Call the omitted port pi and selected port lambda, and their core
neighbors a and b respectively. If p_B=0 there is no export, and the
required bound is immediate. If p_B=1, an export can occur only through
pi with a selected. H1 excludes a one-neighbor resource there; the only
export is one unit through a two-neighbor resource with an internal
isolate. H3 forces an opposite import of at least one, so F_B<=0.
This is exactly q_B-p_B=0.
If b is selected and a omitted instead, pi cannot export and H2 excludes
export through lambda, again giving F_B<=0.

Suppose p_B=2. If a is isolated, neither interface exports: a cannot
be a high or a leaf of a high, and H2 excludes export through lambda.
The selected b is active through lambda. Thus t_B=1 and F_B<=0,
which is the required q_B-p_B+t_B=0.

It remains that a,b are active. If any export occurs, it is the one-
unit two-neighbor export through pi. H3 forces an import of two at
lambda, since b is selected. Therefore F_B<=-1 as required.

If there is no export, we show I_B>=1. Suppose I_B=0. Remove the
external edges and restore pi--lambda. We claim the restriction becomes
a minimal forming eight-set in the closed H.

**Formation.** At pi, the selected external a is replaced by selected
lambda. There is at least one internal selected neighbor by H1, giving
two selected neighbors after restoration. Other omitted block vertices
can lose coverage only if lambda loses activity and was their unique
selected neighbor. That requires lambda to have internal selected degree
zero and such a vertex to be an internal one-neighbor resource, excluded
by H2. Thus all omitted vertices remain formed.

**Necessity of non-ports.** Choose a global private clause for a selected
non-port v. Its support cannot reach v if its center or both edge endpoints
are outside B. A clause based at pi on an original edge contains selected
a; a closed clause there also contains a. A clause based at lambda either
contains selected lambda, or, in the reversed orientation, selected b.
None can be private to v. On an interface edge, the only orientation not
immediately blocked by a selected center is B_(pi,a). In this branch a
is active by assumption. Its only block neighbor pi is omitted, so a
has a selected neighbor in the core. That neighbor also belongs to
B_(pi,a) and is different from v. Thus this clause is blocked too.

The private clause must have its closed center or both edge endpoints
among the non-ports. Their neighborhoods are unchanged by the restoration.
It remains private to v in H, so every selected non-port remains essential.
This clause argument explicitly handles leaves and isolates as well as highs.

**Necessity of lambda.** If its internal selected degree is zero, it becomes
isolated and is self-private. Otherwise its original selected degree was
at least two. I_B=0 means its chosen failure witness lies inside B. After
deleting lambda, the restored edge pi--lambda joins two omitted vertices,
so it cannot create a new covering star. Removing exterior vertices also
cannot create one. Its old internal failure witness therefore still fails.
Thus lambda remains essential too.

We have proved the claim. The closed classification now gives a six-cycle
and two isolates. If lambda lies on the cycle, it has no witness internal
to the detached block B before restoration:
both its internal neighbors are highs, and it has no internal omitted
neighbor. It must import, contradicting I_B=0. If lambda is an isolate,
activation through b destroys the private two-neighbor resources of the
cycle highs associated with its two internal omitted neighbors. Those
cycle highs are non-ports with two high selected neighbors and no alternate
leaf witness, contradicting global minimality. Both cases are impossible.

Hence I_B>=1, and F_B<=-1=q_B-p_B. This completes (3) in all cases.

## Global summation and attainment

Each block contributes at least two by (4). The i_B are on disjoint
selected vertices and W_B on disjoint omitted resources. The t_B use
only isolated core vertices, and every such vertex touches at most one
block. Therefore

    2b <= sum_B(i_B+W_B+t_B) <= i+W.

Unused core capacity and uncharged core isolates are nonnegative. Using
(1) proves5|S|+2b<=3n. No capacity is used by two high owners, no block
resource is counted in two blocks, and no core isolate pays two blocks.

Selected isolates support the private clauses; they are not omitted
capacity resources. An isolate can appear in several clauses, but its
vertex contributes only once to i_B or to its uniquely owned t_B.

For L_k, select all core H,U and in every block select
{1,2,3,5,7,9,10,11}. The core contributes12k and blocks24k. Every
omitted X_i has selected neighbor U_i active through H_i, and each hub
has three selected U neighbors. Deleting U_i uncovers X_i; deleting H_i
leaves its unique selected neighbor U_i isolated and again uncovers X_i.

In a block the selected graph is the cycle1-9-2-10-3-11-1 with isolates
5,7. Its omitted vertices0,4,6,8,12,13 have selected-neighbor pairs
{7,10},{7,11},{7,9},{5,1},{5,2},{5,3}. Each pair is an isolate and a
cycle vertex. They give formation and failure on deletion of every cycle
vertex; each isolate is self-private. All adjacent core X are omitted.
Thus the uniform36k selection is minimal and attains the upper bound.

## Evidence, scope and provenance

The original [Oracle response](reviews/2026-10-19-long-core-SF-research-response.txt)
supplied the block ledger and upper proof. Its
[completion metadata](../output/long-core-SF-oracle-answer.json) verifies
the original task completed with observed gpt_6, effort pro. This is a
research response, not a separate ACCEPT review. We independently checked
the identity signs, exports, imports, closed classification and no-reuse
summation. H1-H4 were reduced to existing proved lemmas; the delicate
restoration branch above is written with explicit private-clause preservation.

The [boundary controls](../output/heawood-block-ledger-controls.json) check
49104 boundary states, including192 active-parent states with forced imports
and64 isolated-parent boundary cases, plus all28 closed minimal eight-sets
and224 private deletion certificates. Abstract parent vertices have their
two core neighbors; locality, not a finite list of cores, handles arbitrary
ambient core edges in the proof. Finite checks verify the argument and do
not prove the all-order theorem by extrapolation.

[HeawoodBlockLedger.lean](../formal/StarForming/HeawoodBlockLedger.lean)
checks four conditional count statements: local credit, list summation,
global no-reuse and the long-core bound. The
[receipt](../output/heawood-block-ledger-formal-check.json) permits only
standard logical axioms. Graph-to-ledger extraction, Fano facts, restoration
and attainment retain full written proofs. The entire graph theorem is
not claimed fully formalized.

The accompanying [return and core-deficit note](DIRECTIONAL_RETURN_AND_CORE_DEFICIT.md)
proves four general graph facts in Lean, refines direct-return slack, and
gives an all-k34k minimal family with every block saturated and k zero-loss
signals. That obstruction explains why the present ledger uses residual
capacity rather than charging every signal to lost block vertices.

A separate [independent review](../output/heawood-block-compensation-review.json)
completed on original task507dce65, observed gpt_6 with effort pro,
with verdict REVISE. Its [exact response](reviews/2026-10-19-heawood-block-compensation-review-response.txt)
accepted the ledger signs and no-reuse mechanism but requested explicit
leaf forcing, attachment-certificate scope and restoration details.
Those passages are expanded above. Two conditional concerns do not
apply: beta_2 is maximum dissociation cardinality, and L is selected
in the bare-port p3/M=L branch. Both definitions are now explicit.
The [same-conversation follow-up](../output/heawood-block-compensation-followup.json)
completed ACCEPT at02:23UTC on19October, observed gpt_6 with effort pro.
Its [exact response](reviews/2026-10-19-heawood-block-compensation-followup-response.txt)
accepts the complete revised general theorem under the explicit dependencies,
all attachment/restoration branches, no-reuse summation and the all-k
SF_2(L_k)=36k consequence. The remaining terminology and symmetric-case
suggestions are now explicit. This is a separate independent review,
distinct from the original research response above. It does not cover
the later shared-port architecture theorem, which has its own review.

Reproduction:

    python3 scripts/check_heawood_block_ledger.py --output output/heawood-block-ledger-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit block-ledger --lean /path/to/lean-4.33.0 --output output/heawood-block-ledger-formal-check.json

The subsequent [closed-high-cycle theorem](CLOSED_HIGH_CYCLE_COMPENSATION.md)
improves the connected cubic coefficient from1/24 to3/62 by preserving
each H six-cycle and joining only through X. Its SF upper proof uses
the established cubic compensation inequality, independently of this
block ledger. The next extremal task is to improve3/62 or tighten the
universal1/14 ceiling. The rectangular-grid bridge
and its mixed-direction geometry remain separate open work. No change to
the submitted DMGT revision is implied by the present result.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
