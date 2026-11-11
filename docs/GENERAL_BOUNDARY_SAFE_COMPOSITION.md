# A boundary criterion for safe deletion and exact composition

11 November 2026. Stars need not be induced. The result applies to any finite
simple ambient graph for safe deletion, the cap theorem and the
star-forming composition. Bipartiteness enters the dissociation identity. A forming set covers every outside vertex by a
non-induced K_(1,2) in the selected set plus that vertex, with two distinct
selected vertices. SF_2 is the largest size of an inclusion-minimal such
set; beta_2 is the largest induced maximum-degree-at-most-one set. Formation
is upward closed, so single-deletion failure is equivalent to minimality.

## Safe deletion from an induced block

Let B be an induced subgraph of G and P subset V(B) contain every vertex
of B with a neighbour outside B. Suppose S forms G, C=S intersect V(B),
and v in C minus P. If

1. C minus {v} forms B;
2. every p in C intersect P with a neighbour in C still has a neighbour
   in C minus {v},

then S minus {v} forms G.

**Proof.** Every newly outside or previously outside vertex of B is
covered by (1). Consider an outside vertex x beyond B. It is not adjacent
to v. An old witnessing star can be lost only if v was its selected leaf,
with selected centre p in P and x its other leaf. Condition (2) supplies
a selected internal neighbour y of p different from v; x,p,y replace the
old star. All other old witnessing stars survive. QED.

A necessary local condition for a global forming set is the following:
for every x in V(B) minus (C union P), either x has at least two C
neighbours, or it has a C neighbour y which has a C neighbour or belongs
to P. Call this condition (A). Indeed x has no external neighbour. If its
unique selected neighbour y uses an external selected vertex as the
star's other leaf, then y belongs to P. This allows activity supplied
from beyond the boundary rather than assuming it is internal.

**Cap theorem.** Suppose that, for every C subset V(B) of size greater
than s satisfying (A), there is a v in C minus P satisfying (1)--(2).
Then every globally inclusion-minimal forming set meets B in at most s
vertices, for every ambient graph whose block boundary is contained in P.

**Proof.** The intersection of a global forming set with B satisfies
(A). If its size exceeded s, the safe-deletion lemma would contradict
global minimality. QED. This is a finite sufficient predicate on the
block and boundary, not a claimed necessary condition for a cap.

## Robust lower witnesses and exact compositions

Start with finitely many pairwise vertex-disjoint blocks B_i, and obtain
G from their disjoint union by adding only edges between prescribed
boundaries P_i,P_j of distinct blocks. No further vertices are present.
Suppose these blocks have caps s_i as above and fixed
internal minimal forming sets C_i of size s_i. Require for each selected
v in C_i a vertex x in V(B_i) minus P_i, outside C_i minus {v}, such that
after deletion either

    N_(C_i-v)(x) is empty,

or it equals {y}, where y is not in P_i and has no neighbour in C_i-v.
These are protected failure witnesses. Under any edges added between
blocks through their boundaries, the union of the C_i remains forming
and every deletion still fails at its protected x. The empty-neighbour
case cannot gain a selected neighbour; in the one-neighbour case neither
x nor y acquires external edges. Hence the union is minimal, and the cap
bounds prove

    SF_2(G)=sum_i s_i.                                      (B)

For dissociation, if all B_i are bipartite with both parts of size b_i
and beta_2(B_i)=b_i, and all added edges respect these chosen sides,
then restriction to blocks gives beta_2(G)<=sum_i b_i, while a whole
global side gives the reverse inequality. Therefore

    beta_2(G)=sum_i b_i.                                    (C)

Blocks and interfaces need not be identical, and the port graph has no
connectivity or degree restriction. The theorem supplies explicit
hypotheses; it does not assert safe composition under arbitrary ports.
For the specific four-port H, the full cap proof, balanced dissociation
value and all six protected witnesses are given in
[the four-port proof](FOUR_PORT_STAR_FORMING_COMPOSITION.md). The direct
finite predicate checks at the end of this note also verify the cap and
witness conditions. Thus (B)--(C) recover that exact composition.

## Why boundary activity must be retained

Take B to be the path p--v--a--b, boundary P={p}, and C=V(B).
After deleting v, C minus {v} still forms B: v has two selected neighbours
p,a. Attach one outside vertex x adjacent only to p. Originally x is
covered by x--p--v. After the deletion p has no selected neighbour and
x is uncovered. Thus internal formation alone does not ensure a safe
global deletion. This is an actual five-vertex graph demonstrating the
need for the boundary activity safeguard in the local lemma.

Finite controls exhaust all simple blocks through order four, every
boundary and two-vertex exterior interface: 82,110 ambient presentations,
2,173,790 forming sets and 286,368 qualifying deletions. In addition,
the finite H cap test accepts all 174 eligible selections of size above
six, each with at least two safe choices, and checks all six protected
witnesses. The cap theorem and additive conclusions rely on their
general proofs; these computations independently inspect the predicates.

## Sharpness of boundary activity under uniform ambient extensions

Given the internal-formation hypothesis (1), condition (2) is also
necessary if deletion must be safe for every allowed ambient extension
with selected intersection C. If a selected port p loses its only internal
selected neighbour v, attach a new unselected leaf x to p and select only
C. Internal formation after deletion implies internal formation before
deletion by upward closure; the new leaf is initially covered by x--p--v.
After deletion its sole selected neighbour p has no selected neighbour.
This proves necessity with the stated universal quantifier. For an
individual ambient graph external activity can make the safeguard
unnecessary; that weaker fixed-graph necessity is not claimed.
