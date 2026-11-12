# Owner matching certificates beyond the path/6k class

12 November 2026. This note extends the sufficient classes for the all-helper
8b/3 bound to arbitrary owner paths and even cycles when an explicit auxiliary
obstruction is absent. It gives an exact 2-SAT test for that absence in a
specified matching family, and a connected thirty-vertex template showing that
this test is not necessary for the bound. The universal 8b/3 question remains
open. The complete argument, including the eight-case upper certificate, is in
[the integrated manuscript source](../manuscript/owner-matching-proof.tex).

## Setting and theorem

Use the physical partial template of ALL_HELPER_EXACT_OPTIMIZATION.md. There
are b helpers, 2b witnesses and 2b owners. Index witnesses and their distinct
owners by V. The helper pairing P is a perfect matching joining equal physical
colours; the partial witness matching Q and the owner graph B join opposite
colours. The owner graph has maximum degree two. There are no further edges.
A dissociation set induces maximum degree at most one; beta_I requires all
helpers to be selected.

Let o count the odd-order path components of B, including isolated vertices.
It is even because |V|=2b. Build a matching R separately in each component:

- on an even-order path use its unique perfect matching;
- on an odd-order path use either alternating matching leaving an endpoint;
- on a square use the two opposite-vertex pairs;
- on every other even cycle use either perfect matching.

Let W be its matched vertices and J_R=(P union Q union R)[W] as a simple graph.
If J_R has z components K4, then

    beta_I >= b+(2b+o)/2+z+ceil((2b-o-4z)/3)
           = ceil(8b/3+(o-2z)/6).                         (1)

Thus z=0 gives beta_I>=ceil(8b/3+o/6), and even z<=o/2 suffices for8b/3.
If P union Q has no four-cycle component, z=0 for every choice above. Owner
cycles may have arbitrary even lengths, including8 and10, and may be mixed
with paths and squares. This is a joint condition on the actual template;
there is no assertion that arbitrary such owner mixtures satisfy it.

**Proof.** J_R has maximum degree three. Every K4 is an entire component,
uses one edge of each matching type at every vertex, and leaves an auxiliary
P/Q four-cycle after the R edges are deleted. The P/Q degrees are exhausted,
so this is also a component before restriction to W. In its absence, Brooks's
three-colouring theorem applies componentwise; odd cycles need only three
colours as well. Remove the z K4 components, choose a largest colour class
on the remaining graph, and add one vertex per K4. This gives an independent
set T of at least z+ceil((2b-o-4z)/3) witness indices.

Choose all uncovered owners, and one endpoint outside T per R edge, forming
S. Then |S|=(2b+o)/2 and S avoids T. On a path or non-square cycle, B-R is a
matching; no R edge lies within S. In a square exactly two owners are selected,
so its induced graph also has maximum degree one. Components have no edges
between them. Hence B[S] is dissociation. All helpers, S and T therefore form
an actual dissociation set in the physical template. Adding cardinalities
proves1. Each helper, uncovered endpoint and matching edge is used once.

Brooks's theorem is a standard input, not a new independence theorem here:
R. L. Brooks, *On colouring the nodes of a network*, Proc. Cambridge Philos.
Soc.37(1941),194–197, DOI10.1017/S030500410002168X. Bibliographic metadata was
freshly checked against Crossref; no new literature-priority claim is made.
The implementation searches for a three-colouring and does not claim polynomial
runtime for that search.

## An exact 2-SAT test for this matching family

Each non-square cycle and nontrivial odd-order path has a phase variable. The
other choices are fixed. An auxiliary P/Q square becomes a K4 exactly when
both missing diagonals belong to R. Each diagonal is unavailable, fixed, or
present in one phase of one variable. Forbid their conjunction. This gives
clauses of length zero, one or two; contradictory requirements on one variable
produce no obstruction. The two diagonals can belong to different owner
components, so binary clauses are necessary.

The formula is satisfiable if and only if this specified family contains a
K4-free R. The implication-graph algorithm returns phases or an empty clause
or two directed contradictory paths. This equivalence concerns K4 avoidance.
Its failure does not refute the all-helper or unrestricted cardinality bound,
and it does not quantify over all maximum matchings of an odd path.

## Exact thirty-vertex obstruction and unbounded construction loss

Use V={0,...,11}, with colours0 on0,...,5 and1 on6,...,11. Take

    P={(0,1),(2,3),(4,5),(6,7),(8,9),(10,11)},
    Q={(0,8),(1,9),(2,11),(3,10),(4,6),(5,7)},
    B=cycle(0,7,4,8,3,11,2,10,1,6,5,9).

The physical graph is connected, bipartite, minimum degree2, maximum degree3,
and has30vertices. B has precisely two perfect matchings, both included in the
test. The first produces a K4 on{2,3,10,11}; the second produces one
on{4,5,6,7}. Their remaining eight-vertex graphs have spanning cycles

    (0,1,6,4,8,9,5,7),   (0,1,10,11,2,3,8,9),

respectively. In both, edges(0,8),(1,9) forbid the two alternating four-sets.
An independent four-set of an eight-cycle must be alternating. Thus each
remainder has independence number at most3. Independent four-sets in the full
J_R are respectively{0,2,4,9} and{0,2,4,10}, proving both independence numbers
are exactly4.

Despite K4-avoidance failing, beta_I=17. A17-set consists of all6helpers,
owners{3,4,6,7,9,10,11} and witnesses{1,2,5,8}. The upper bound follows from
the exact all-helper formula and an eight-case structural classification:
beta_I=18 would require U independent in P union Q and B[V-U] dissociation.
Extend U to maximal independent. The auxiliary graph has three squares with
opposite-pair choices({0,9},{1,8}),({2,10},{3,11}),({4,7},{5,6}). In each of
the eight choices the complement contains a P3; the integrated proof and
coordinate fixture give every triple. Thus18 is impossible.

For r disjoint copies, beta_I=17r but the best construction selecting exactly
one owner per R edge and an independent witness set in J_R has size16r.
All2^r owner perfect-matching choices are covered by additivity. This is an
unbounded additive loss for that construction; the examples are disconnected
for r>1. They satisfy, rather than refute, the full-cycle matching-selection
threshold max_R alpha(J_R)>=ceil(|V|/3). That conjecture, and general8b/3,
remain open. No unrestricted beta_2 optimum is asserted for the30vertex graph.

## Fixed-extraction consequence and verification

For a minimal forming set in a bipartite graph of maximum degree three, if
its actual extracted template admits the K4-free choice, the physically
separate retained set of sizeL combines with the template. With b' helpers,
Z=3beta_2-3L-8b'>=0. The existing exact witness ledger gives

    5n-51d = Z+5r+12(alpha+pi)+24tau+7(e-b3)+2b3+5q >=0.

Hence51d<=5n for that set; it bounds SF_2-beta_2 if a maximum minimal set
admits this extraction. The coefficient5/51 is unchanged; the sufficient
class is enlarged. The unrestricted7/71 bound remains current.

Run `python3 -B scripts/check_owner_matching_certificate.py`. The unchanged
checker covers548templates,1,040 independent phase/K4 comparisons,522 complete
small2SAT truth tables,268 exact all-helper optimizations,493,633 literal
physical subsets,12 nonempty template lifts, and4,227 minimal-set lifts on879
small graphs. Large cases are actual physical certificates through128helpers,
not large unrestricted optimizations. The all-order and all-r results have
the written arguments above. Exact external audit scope is recorded in
`output/owner-matching-review.json` when available. No Lean validation or
new grid coefficient is claimed.
