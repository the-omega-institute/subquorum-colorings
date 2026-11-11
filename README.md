# Current continuation

The [sharp selected-star theorem](docs/SHARP_SELECTED_STAR_GAP.md) proves
`|S|-beta_2(G)<=floor(n/12)` for every inclusion-minimal two-star-forming
set S in a finite simple bipartite graph whose selected components are
stars, edges or isolates. A private clean leaf at each centre is no
longer required. A matching of centres to twice-touched isolate helpers
makes the repairs compatible and supplies the missing budget inequality.
The connected degree-six family attains the coefficient. Positive equality
forces the six-vertex-block template, including at least n/6 pendant
vertices; minimum degree at least two therefore improves the integer bound
to `floor((n-1)/12)` for such selections. The complete proof, standalone
checker and finite report are included. Both independent proof reviews returned
[ACCEPT](output/selected-star-general-budget-review.json). The final reviewer
hash-checked all four supplied files, ran the original checker unchanged with
assertions to completion, and reproduced the 27,335-byte report exactly.

The [minimum-degree refinement](docs/SELECTED_STAR_MINIMUM_DEGREE_BOUND.md)
strengthens this for nonempty graphs with minimum degree at least delta>=2
and maximum degree Delta. Put `L=max(7(delta-1),Delta)`. Every such selected-star
minimal set satisfies `|S|-beta_2<=floor(L*n/(12L+2(delta-1)))`.
For minimum degree two and Delta<=7 this becomes `floor(7n/86)`.
The proof retains the exact unused-vertex remainder and counts the additional
neighbours required by singly touched selected isolates. Two independent
[ACCEPT reviews](output/selected-star-degree-budget-review.json) checked the
argument and ran the original controls to completion, including 727,240
feasible integer ledgers and a genuine 38-vertex minimum-degree-two example
with selected size24 and exact unrestricted beta22. No sharpness of the new
degree constant is asserted.

The [whole-cut degree theorem](docs/FULL_DEGREE_CAPACITY_FOR_SELECTED_STARS.md)
counts the degree demands of all selected vertex types in a single cut and
adds the bipartition bound `beta_2>=n/2`. For the same selected-star minimal
sets, minimum degree at least delta>=3 and maximum degree at most Delta>=4 give
`d<=floor((Delta-delta+1)n/(2(5Delta+delta-7)))`. In regular degree k>=4 this
is `floor(n/(12k-14))`; cubic graphs satisfy `floor(7n/146)`.
A positive gap in regular degree at least four requires selected edge
components, with an explicit lower bound on their number of vertices.
The constants are optimal in the explicitly stated six-ledger relaxation
for the proved parameter ranges; graph-sharpness remains open.

Retaining actual degree deficits also gives a boundary-sensitive version
without a minimum-degree assumption. In a full h-by-w rectangle it implies
`d<=floor((hw+4h+4w)/34)` for every specified selected-star minimal set,
with a stronger location-dependent form in the note. This does not assume
that all minimal grid selections are of that form. Literal finite checks
and exact rational controls pass; independent source review is pending.

The [clean-witness port composition](docs/SELECTED_STAR_PORT_COMPOSITION.md)
gives an exact unrestricted formula for every finite interface graph R,
with any orientation: `beta_2(F_R)=7|V(R)|+alpha(R)`. Its explicit minimal
forming selection has size `8|V(R)|`, inducing only P3 stars and isolates.
A full eight-set in a block forces both already-paired ports; hence such
blocks form an independent set of R. Port-omitting seven-sets attain the
complementary blocks simultaneously. Directed paths give connected
maximum-degree-four graphs with selected deficit `floor(r/2)` at order12r;
cycles give `ceil(r/2)`. General proofs and independent controls are included;
the separate
[ACCEPT audit](output/selected-star-ports-review.json) reconstructed all three
files with matching hashes, ran the original checker unchanged to terminal
completion with assertions, and reproduced its report byte-for-byte.

The [selected-star gap theorem](docs/SELECTED_STAR_COMPONENT_GAPS.md)
resolves the unrestricted selected-star question negatively. A connected
18-vertex bipartite graph has a minimal forming selection of size12 whose
selected components are three P3 stars and three isolates, but beta_2=11.
The two-parameter construction has exact beta_2=3(a+b)+max(a,b,2).
A general matching-budget argument proves the sharp bound
`|S|-beta_2<=floor(n/12)` when every centre has a leaf with a private
outside witness. Connected maximum-degree-six graphs attain that coefficient
at every order24r, with selected size16r and beta_2=14r.
These are all-parameter proofs with explicit attaining sets and independent
finite checks. Independent
[ACCEPT review](output/selected-star-gap-review.json) confirmed every proof,
reconstructed all four artifacts with matching hashes, ran the original
checker unchanged with assertions and reproduced its report byte-for-byte.

The [leaf-retaining exchange theorem](docs/STAR_LEAF_MATCHING_EXCHANGE.md)
handles conflicts by one auxiliary bipartite matching. For a minimal forming
selection with selected star/edge/isolate components, fix one witness per
star leaf, let c count centres, e leaves, and Q=G[W union I] on witnesses
and selected isolates. The exact largest dissociation set in S union W
retaining all star leaves has size `|S|-c+e-nu(Q)`. Hence the desired bound
holds without any witness-independence assumption when S has at most one
selected isolate. The matching criterion also certifies the earlier6-by-6 witness
obstacle. A connected12r-vertex family has true beta `8r` but exact
leaf-retaining optimum `7r`, proving that the restriction can lose an
unbounded amount. This is a limitation of leaf retention, with an explicit
size-preserving exchange still available. The general proofs, certificate
construction and independent finite checker received independent
[ACCEPT](output/star-leaf-budget-review.json). The reviewer verified all
three attached files against their hashes, ran the original checker
unchanged with assertions, and reproduced the report byte-for-byte.

The [arbitrary-width witness geometry](docs/GRID_WITNESS_GEOMETRY.md) proves
`2|S|-mn<=|Z|+|E|-|H|-ceil(K/2)` for every minimal forming grid selection:
each
selected-degree-four centre supplies two omitted caps, distinct across
centres and from direct-witness resources; exceptional caps have capacity
at most two and supply the K term. It also proves a simultaneous
star exchange through independent leaf witnesses, including shared selected
isolates. In particular, selected branching confined to one bipartition
class implies `|S|<=beta_2` at all dimensions. An explicit full 6-by-6
example refutes automatic independence of the witnesses while admitting
a same-size dissociation exchange. The general proofs and two literal
finite checkers are included. A separate
[ACCEPT audit](output/grid-witness-geometry-review.json) reconstructed all
five manifest files, ran both original checkers unchanged with assertions
enabled, and reproduced both reports byte-for-byte.

The [five-row theorem](docs/FIVE_ROW_STAR_FORMING_EQUALITY.md) extends the
all-length star-forming result to height five. For every n>=1,
`SF_2(P_5 square P_n)=beta_2=psi_sq=F(5,n)`; the value is 4,6,9 at lengths
1,2,3 and `8floor(n/3)+3(n mod3)` thereafter. A compact nontruncating
generator finds `V17=V14+8` on 8,227,512 reachable states. An independent
literal-star implementation compares every one of the 33,554,432 local
kernel entries, reconstructs both complete vectors with standard maps,
and checks 1,082,400 individual small-board selections. The general
frontier and induction prove the all-length implication. The prior
colouring supplier was rerun separately. Its independent
[ACCEPT audit](output/grid-star-height-five-review.json) ran both original
programs, regenerated both large vectors with exact hashes and reproduced
the independent checker report and all four prior colouring outputs
byte-for-byte. Arbitrary width and the universal 5/6 improvement remain open.

The [three-row upper-forming theorem](docs/THREE_ROW_STAR_FORMING_EQUALITY.md)
establishes `SF_2(P_3 square P_n)=5floor(n/3)+2(n mod3)` for every n>=1,
by an exact deletion-witness frontier and whole-vector translation followed
by induction. With the prior width-three colouring theorem, this closes
the proposed triple equality at height three. The finite certificate is
independently rebuilt from the empty prefix using literal three-vertex
stars. This computer-assisted all-length proof has an independent
[ACCEPT review](output/grid-star-transfer-review.json): both unchanged
implementations and the prior Omega supplier were executed, with all eight
attached output files reproduced byte-for-byte. Arbitrary width remains open.

The [four-row extension](docs/FOUR_ROW_STAR_FORMING_EQUALITY.md) gives
`SF_2(P_4 square P_n)=beta_2(P_4 square P_n)=2n+(n mod2)` for every n>=1.
Its independent literal-star reconstruction verifies `V17=V15+4` on all
342,768 reachable states. The same general frontier proof and induction,
together with the prior width-four colouring theorem, give triple equality
at height four. Its separate [ACCEPT review](output/grid-star-height-four-review.json)
ran both unchanged implementations, reproduced both reports byte-for-byte,
and matched the two endpoint hashes. The two audits preserve their exact
input snapshots and execution scopes.

The [exact decorated-interface formula](docs/EXACT_DECORATED_INTERFACE_FORMULA.md)
converts a minimum interface forming set into a maximum minimal forming
set of a 21-fold decoration: `SF_2(D(H))=12|H|-sf_2(H)` for every finite
simple H. A stronger activity cap pays for each extra interface selection
once. It gives the exact connected path residual and the exact single-ear
discrepancy `mu(s)=2floor(s/4)+min(s mod4,2)`, strengthening the earlier
domination estimate. Its independent ACCEPT review ran the unchanged
original checker and reproduced the report byte-for-byte. The review
also checked two additional minimal decorations exercising the augmentation
and repeated-choice branches; a separate literal-star checker reproduces
those two controls locally. Exact scopes are recorded with the proof.

The [local stability theorem](docs/LOCAL_STAR_FORMING_STABILITY.md)
proves two-sided bounds for deleting an arbitrary interface in any finite
simple graph. The repair preserves original selections beyond radius five;
adding selections affects deletion witnesses only within radius three,
and both certificate radii are attained on P9. Consequently the error
from a fixed number of square ears is bounded at fixed maximum degree,
independently of graph order. Explicit union-of-balls bounds extend this
to arbitrary components glued through a bounded interface.

The [bipartite partial-ear obstruction](docs/BIPARTITE_PARTIAL_EAR_OBSTRUCTION.md)
proves that exact SF addition fails even for one attached square and that
its error is unbounded while the ear count stays fixed at one. Connected
bipartite examples have `SF_2(R_s)=11s` and `SF_2(J_s)=12s+2`, so the
error is exactly s. Both the all-q local proof and this amplification
have independent ACCEPT reviews with original-checker executions.
The [connected-residual version](docs/CONNECTED_RESIDUAL_EAR_AMPLIFICATION.md)
keeps the base, final graph and residual connected and bipartite. Its
original bound `SF_2(R_s)<=12s-ceil(s/3)` is strengthened by the exact
decoration formula above to `SF_2(R_s)=12s-mu(s)`; `SF_2(J_s)=12s+2`.
The residual degree
is at most six; root degrees grow with s. Its all-s proof and standalone
certificate checks have a separate independent ACCEPT, which also reran
the unchanged checker and reproduced its report byte-for-byte.

The [four-parameter ear-ladder family](docs/EAR_LADDER_FOUR_PARAMETERS.md)
has, for every r>=1, order16r and exact values
`beta_2=sf_2=SF_2=8r < psi_sq=Omega=9r`.
These graphs are two-connected, outerplanar, median, and have maximum
degree four. Every local selected/endpoint configuration is charged
once to prove the upper bound; an explicit9r-colour partial colouring
attains it. Thus even in this restricted class, SF/dissociation equality
does not imply sub-quorum equality. Arbitrary-width rectangular grids remain open.

The [square-ear composition theorem](docs/SQUARE_EAR_STAR_FORMING_COMPOSITION.md)
classifies every minimal forming set when squares are attached along a
perfect matching of an arbitrary base: all 6^k choices of two vertices
per square are minimal, with beta_2=sf_2=SF_2=2k. For a partial matching,
the exact dissociation addition and star-forming bounds hold, but the
analogous exact SF addition is false by an explicit all-m family with
unbounded error. A pendant-path variant has the same obstruction.
An outerplanar median degree-four equality family has no automorphism
sending every vertex to a neighbour.

The [restricted median reduction](docs/RESTRICTED_MEDIAN_CUBE_CHAINS.md)
settles the two-connected subcubic median case as a consequence of the
squaregraph characterization and the prism formula. In planar median
graphs of maximum degree four, intersecting cubes form induced convex
chains with at most eight external edges at their ends. The full
degree-four equality question remains open.

The [median-graph obstruction](docs/MEDIAN_STAR_FORMING_OBSTRUCTION.md)
proves that medianity does not force SF_2=beta_2. For every r>=1 a
connected median graph of order38r and maximum degree5 has beta_2=21r
and a minimal forming set of size22r. The base is a 4-by-4-by-2 prism
with six pendant leaves; disjoint leaf ports give the connected family.
Complete deletion witnesses and an elementary exact dissociation proof
are included. These graphs are not rectangular grids.

The [Cartesian-prism theorem](docs/ADJACENT_INVOLUTIONS_AND_PRISM_GAPS.md)
extends the exact star-forming and representative values to every finite
base H: `SF_2(H square K_2)=Omega(H square K_2)=2n-nu(D(H))`.
The largest SF/dissociation gap among n-vertex bases is `max(0,n-4)`;
for n>=5 all equality bases are complete graphs with a matching deleted.
Their four parameters, and the sharp SF/colouring gap and its equality
cases, are determined exactly. This shows precisely where the four-way
prism equality needs the bipartite-base hypothesis.

The [extended-double-cover theorem](docs/EXTENDED_DOUBLE_COVER_PARAMETERS.md)
now proves, for every finite simple base H on n vertices,
`SF_2(E(H))=beta_2(E(H))=psi_sq(E(H))=Omega(E(H))=2n-nu(D(H))`.
Here D(H) is the ordinary double cover without rungs. An ordinary matching
and equal-size vertex cover certify the common value. The new star-forming
proof gives each empty rung one shared budget of two deletion witnesses.
For every bipartite H, its Cartesian prism therefore has all four values
equal to `2 alpha(H)`. The same symmetry gives zero genuine TH expense
for arbitrary actual matchings and feasible white-only selections.

The 12 November continuation gives [exact source-dependent TH optimization
by grid width and a zero-expense theorem for every feasible two-row ladder](docs/EXACT_TH_OPTIMIZATION_AND_LADDERS.md).
The implementation returns a full optimal auxiliary matching and handles
retained paths, zero weights and free HH rerouting together.
The current [completion and remaining-problem record](docs/COMPLETION_20261112.md)
distinguishes these proved classes from wider rectangular grids and the
remaining degree/connectivity problems.

The 11 November results on intrinsic equality, degree constraints, general
boundary composition and simultaneous Hall budgets are indexed in
[the completion note](docs/COMPLETION_20261111.md).

# Sub-quorum colorings: hypercubes, boundary matchings, and grids

[![Verification](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml/badge.svg)](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml)

**11 November 2026: sharp star-forming gap.** Every finite bipartite graph
satisfies `SF_2 - beta_2 <= floor(n/10)`. The bound is attained by
two-connected graphs of minimum degree two and maximum degree four. The
[general proof](docs/SHARP_BIPARTITE_STAR_FORMING_GAP.md),
[four-attachment composition theorem](docs/FOUR_PORT_STAR_FORMING_COMPOSITION.md),
[working manuscript](manuscript/starforming-gap.tex), and
[reproduction instructions](docs/REPRODUCE_STAR_FORMING_GAP.md) give the
statements, proofs and exact validation scope.

Research sources and reproducibility materials for **From hypercubes to grids:
sub-quorum colorings and structural bounds**, with contributions by Wenlin
Zhang (National University of Singapore; Chrono AI, Singapore) and Haobo Ma
(Chrono AI, Singapore).

**Start with the [current mathematical results](docs/GRID_RESULTS.md)**:
the uniform grid dissociation formula, directional matching bounds, and the
five-sixths estimate for mixed directions. This companion includes complete
proofs and extends the earlier manuscript, which covers the hypercube,
structural results and exact strip certificates.

The starting result resolves Conjecture 6.4 of Rafik Sahbi's
[Sub-quorum colorings of graphs, arXiv:2609.25128v1](https://arxiv.org/abs/2609.25128v1):
the sub-quorum coloring number of the n-dimensional hypercube is 2^(n-1)
for **every n >= 2**, with a dimension-independent Lean proof.

Starting from this solved family, the project advances two research directions:

1. **Rectangular grids:** use exact strip certificates and the boundary viewpoint
   to seek a proof of Sahbi's formula at arbitrary width and length.
2. **Structural characterization:** determine conditions for psi_sq=beta_2,
   using the signed boundary theorem as a sufficient mechanism and the grafted
   tree families as explicit obstructions.

The [research agenda](docs/RESEARCH.md) connects current results to the next
mathematical targets. The manuscript follows the same progression from the
hypercube solution to these geometric and structural questions.

The [C4-free pair-packing theorem](docs/C4_FREE_REPRESENTATIVE_EQUALITY.md)
gives beta_2=psi_sq=Omega=N for D-regular bipartite graphs with N vertices
per side, D>=3, no four-cycle and N<=2(D-1)(D-2)+4. In particular every
finite projective plane of order q>=2 has incidence-graph sub-quorum
number q^2+q+1. The Heawood case gives beta_2=psi_sq=7<SF_2=8, linking
the two research directions without settling the grid equality. The
proof is general; external priority of this specialization is not claimed.
Every optimal representative pair in a plane of order q>=3 has all
singleton representatives in one bipartition class. The eighteen-vertex
Pappus graph has exact beta_2=psi_sq=Omega=10, showing the cubic
sixteen-vertex equality threshold is sharp. Its optimal representative
pairs have no matching edges. Ten scoped Lean declarations, including
three finite Pappus certificates, and independent controls pass.

The new [closed-high-cycle construction](docs/CLOSED_HIGH_CYCLE_COMPENSATION.md)
improves this project's connected cubic gap coefficient from1/24 to
**3/62**. For every r>=1 it gives a two-connected cubic bipartite graph
Z_r of order62r with **beta_2=33r and SF_2=36r**. Keeping each H six-cycle
closed, while connecting only through X edges, prevents the former
exceptional local gain. A general omission proof charges all three
Heawood blocks independently. The coefficient3/62 is also optimal within
the distinct-port C_1/Heawood architecture under arbitrary X-only gluing.
Seven conditional Lean counts and fixed-core/actual-ring controls pass.
The independent Oracle review accepts the all-r Z_r theorem; the later
architecture corollary was outside its input. A stronger
[two-witness architecture theorem](docs/CORE_BLOCK_GAP_BARRIER.md) now
permits reused core X attachments, arbitrary bipartite high cycles and
regrouped hub triples: beta>=max(12r+7b,9r+8b)>=33n/62 still forces
gap<=3n/62. Equality requires b=3r; the wrong block/core ratio has an
explicit deficit. Eleven conditional Lean counts and285actual-gluing
controls pass. Its own separate independent review now completed ACCEPT.
The general upper coefficient1/14 and the rectangular-grid bridge remain open.

The preceding [block compensation theorem](docs/HEAWOOD_BLOCK_COMPENSATION.md)
proves **SF_2(L_k)=36k for every k>=1**. More generally b disjoint broken
Heawood blocks attached to distinct core ports force5|S|+2b<=3n in cubic
bipartite graphs. Actual isolates and unused witness capacity pay each
block once. Complete written proofs and conditional Lean ledger checks
are provided. Its independent review now accepts the revised general
theorem and all-k consequence. The [return theorem and obstruction](docs/DIRECTIONAL_RETURN_AND_CORE_DEFICIT.md)
add four general graph Lean proofs and an all-k minimal34k family with
k directional signals but zero block losses. The earlier
[eight-template classification](docs/SATURATED_HEAWOOD_TRANSFER.md) supplies
the local geometry. The separate rectangular-grid bridge remains open.

The related [star-forming project](docs/EXACT_STAR_FORMING_COMPOSITION.md)
has a separate composition theorem: joining r ten-vertex copies through
arbitrary b1-to-a1 interfaces gives beta_2=5r and SF_2=6r. Cyclic interfaces
give two-connected bipartite graphs of maximum degree four with exact gap
|V|/10. The note contains the full local deletion proof and a three-page PDF;
the general SF upper bound and an attaining minimal set are checked in Lean.

A [subcubic construction](docs/SUBCUBIC_STAR_FORMING_GAPS.md) now gives
two-connected bipartite graphs J_r of minimum degree two and maximum degree
three, for every even r>=2, with order 11r, beta_2=13r/2 and SF_2=7r.
The [exact upper-bound proof](docs/EXACT_SUBCUBIC_COMPOSITION.md) limits
each ten-vertex core to six selected vertices in any outside graph
attached only at its designated vertices. Thus their gap is exactly
|V|/22. Cycles have beta_2=SF_2=floor(2n/3),
so three is the first maximum-degree bound permitting a gap among
two-connected bipartite graphs. An explicit perfect matching also gives
Gamma=alpha=11r/2, separating all three parameters. The full proof tracks identified ports
without double counting; base certificates and its arithmetic bound are
checked with standalone Lean4.33.0. Five further Lean audits check supported
deletion, the dense-core certificate, its arbitrary-outside lift, the
per-core cap and the new arithmetic accounting.

The [cubic construction](docs/CUBIC_STAR_FORMING_GAPS.md) strengthens the
regularity restriction: for every r>=1 there is a two-connected cubic
bipartite graph F_r of girth six and order 14r with Gamma=alpha=7r,
beta_2=7r+floor(r/2), and SF_2=8r. Its exact gap is ceil(r/2), at least order/28.
A Fano-plane saturated-port lemma gives the exact dissociation count, and
rewiring only outside the fixed selected set preserves its minimality.
The [exact composition theorem](docs/EXACT_CUBIC_COMPOSITION.md) supplies
the matching upper bound even for arbitrary port interfaces, and an
interaction graph Q gives beta_2=7r+alpha_0(Q), where looped vertices are
excluded from independent sets. The exact gap is its vertex-cover number.
Written proofs and independent controls are available. The
[literature check](docs/STAR_FORMING_LITERATURE_20261019.md) also identifies
Bhattacharjee's external bipartite/planar-bipartite complexity theorem,
which narrows the remaining complexity agenda to additional restrictions.

The [degree-capacity theorem](docs/REGULAR_STAR_FORMING_BOUND.md) now gives
a sharp order bound for every d-regular graph: SF_2<=floor(dn/(2d-1)),
including SF_2<=floor(3n/5) for all cubic graphs. Its general version tracks
the degrees of selected vertices and charges pairwise disjoint failure
witnesses. All regular extremal sets have an explicit five-part structure;
for bipartite regular graphs, attaining this bound forces beta_2=SF_2.
It also gives the sharp comparison SF_2<=6 Gamma/5 for cubic bipartite graphs.
The same weighted argument gives the rectangular-grid star-forming bound
SF_2(P_m square P_l)<=floor((4ml+2m+2l)/7), for m,l>=2. This does not
establish the separate bridge to sub-quorum colorings. General written
proofs, twelve symbolic Lean audits and independent controls are available;
the full equality characterization and finite cardinal summation have
written proofs rather than complete Lean formalizations.

The [general bipartite compensation theorem](docs/SHARP_REGULAR_BIPARTITE_GAP.md)
proves sum_(v in S)(deg(v)+Delta+1)<=Delta n+2beta_2 for every minimal
forming set in every bipartite graph with maximum degree at most Delta>=3.
For d-regular bipartite graphs it gives(2d+1)SF_2<=dn+2beta_2 and the
sharp gap bound floor(n/(4d+2)), for every d>=3. An explicit two-connected
graph of order4d+2 attains both. For every d>=4, the
[connected sharp-gap construction](docs/REGULAR_CONNECTED_SHARP_GAPS.md)
attains the same coefficient at arbitrarily large orders and gaps:
n=(4d+2)r, beta_2=(2d+1)r and SF_2=(2d+2)r. Its broken-block cap is
proved and summed without interface compensation; an explicit eight-set
explains why the identical cubic port argument fails. General proofs,
five additional symbolic Lean audits, arbitrary bipartite controls and
independent connected-instance optima are provided. Oracle accepted the
general-degree theorem. Its connected-ring review requested one omitted
degree-four count case; the uniform repair is incorporated, and the
original conversation's follow-up now accepts the complete ring theorem.

The [exact stability remainder](docs/REGULAR_COMPENSATION_EQUALITY.md)
now characterizes the isolate-tight partition in every regular degree
d>=3. For d>=4, linear compensation equality forces this partition,
balanced selected isolates and maximum explicit exchange sets; the
degree-two unused-witness coefficient explains why the same deduction
does not follow from the cubic accounting alone. Five symbolic audits
and independent partition controls support the general written proofs.
A [covering pullback theorem](docs/COVERING_PULLBACK_AND_CUBIC_SEARCH.md)
also shows that minimal forming sets pull back under graph covers of
triangle-free bases. It proves exact SF_2=16 for every two-sheeted
Heawood cover. Finite connected-cover discovery controls found beta_2
15or16, rather than14. A new [structural proof](docs/HEAWOOD_DOUBLE_COVER_GAIN.md)
establishes this without the255-signature search: switching classes are
traceless3-by-3binary matrices, their six nonzero similarity types have
explicit fifteen-vertex dissociation certificates. Hence beta_2=14
holds exactly for the disconnected double cover; connected double covers
have SF_2-beta_2 at most one. The classification and transfer are written
proofs, with independently checked local certificates, not a new Lean
formalization. Arbitrary-order connected cubic sharpness remains open.

The [augmented isolate compensation](docs/AUGMENTED_ISOLATE_COMPENSATION.md)
now proves 2|S|<=2beta_2+z for every minimal forming selection in every
bipartite graph, where z counts its selected isolates. Each unreserved
leaf contributes an actual unused witness to one of two compatible
matching augmentations. This completes the regular equality reduction
also in degree three: linear equality forces the isolate-tight partition.
In the [cubic path normal form](docs/CUBIC_EQUALITY_PATH_NORMAL_FORM.md),
the slack is at least twice the number of high paths, with an additional
componentwise signed-debt bound. Thus actual equality excludes high
paths altogether. An explicit connected28-vertex example explains why
the original unaugmented balance rule was insufficient. Two graph
lemmas and ten conditional arithmetic lemmas pass Lean;19,550augmented
exchanges and347path/established controls pass finite checks. The
connected cubic asymptotic optimum and grid bridge remain open.

The [four-port padding rings](docs/CUBIC_EQUALITY_PADDING_RINGS.md)
now realize unbounded gap on the cubic linear-equality stratum itself.
For any r>=1 and positive k_i, put K=sum k_i. The two-connected graphs
have n=14r+20K, beta_2=7r+12K and SF_2=8r+12K. A six-periodic integer
weight proves that omitting either pair of a core's four ports costs
one vertex, even when its other pair is freely used. This prevents
shared compensation when the cores are joined cyclically. The gap r
attains isolate compensation with z=2r, so its1/2coefficient is sharp
on connected cubic graphs with unbounded gaps. Seven new Lean audits,
an exhaustive fixed-core port check and fifteen ring controls pass.
This gives gap coefficient1/34 when all k_i=1. Its separate Oracle
review returned ACCEPT for the full four-port and ring theorem.

The [three-pair additive compensation lemma](docs/CUBIC_TRIPLE_PORT_COMPENSATION.md)
now improves our connected cubic gap coefficient from1/28 to1/24.
The fixed20-vertex six-port core satisfies |D|+m<=12, where m counts
wholly omitted cut pairs. A general local case proof shows that two
Heawood obstructions require two distinct losses in this same core.
The resulting two-connected cubic bipartite graphs have n=48r,
beta_2=26r and SF_2=28r for every r>=1, with gap n/24 and linear
compensation equality. Eight conditional Lean count theorems and
independent controls of every fixed-core subset and ten rings pass;
the full graph theorem retains a written proof. Its separate Oracle
review returned ACCEPT. The connected asymptotic optimum is therefore
between1/24 and1/14; neither optimality nor the grid bridge is settled.

The [arbitrary core interfaces and second-cut obstruction](docs/HEAWOOD_SECOND_CUT_OBSTRUCTION.md)
now extend those exact values to every allowed simple bipartite cubic
matching between c six-port cores and b pendant one-cut Heawood blocks:
n=20c+14b,beta_2=12c+7b,SF_2=12c+8b. Isolate compensation gives
attainment without restricting the remaining core matching. For c>=2,
connectedness forces b<=2c, so this entire architecture cannot beat
the asymptotic1/24coefficient. A general Fano proof shows that deleting
any two disjoint Heawood incidences still gives beta_2=8, but an explicit
34-vertex module disproves extending the old saturated-port charge to
such a second cut: its local dissociation count is20rather than19.
The uncharged obligation moves to its new interface. Nine new Lean
audits and all168cut choices/44interface controls pass; the general
incidence and interface proofs remain written. The separate review returned
ACCEPT. All density-equality interfaces in this architecture have a cyclic
quotient, including the two-module parallel-edge quotient.

The [long-core A/B obstruction](docs/LONG_CORE_WORD_OBSTRUCTION.md)
now disproves additive omission charging beyond the fixed core. A general
cyclic word construction gives F(k)>=12k+floor(k/2), including an explicit
forty-vertex score25counterexample to the proposed24cap. Attaching all3k
Heawood blocks gives beta_2>=33k+floor(k/2) on62kvertices, and therefore
7(SF_2-beta_2)+5floor(k/2)<=21k. This excludes the proposed3/62gap target
for this family when k>=2. The exact SF theorem below also fixes its
asymptotic gap coefficient at5/124, below1/24.
The general word dissociation theorem and eight supporting declarations
pass Lean. The [matching all-k upper bound](docs/LONG_CORE_SHARP_OMISSION.md)
is now proved by score-preserving normalization, a two-index cell inequality
and the exclusion of adjacent exceptional blocks. Hence F(k)=12k+floor(k/2)
and beta_2=33k+floor(k/2) exactly. Ten further conditional cell/count Lean
declarations pass. The subsequent
[block-capacity proof](docs/HEAWOOD_BLOCK_COMPENSATION.md) closes the full
forming interval: SF_2=36k for all k, with gap3k-floor(k/2).
The original Oracle responses supplied the structural upper argument and
new block ledger; both were independently checked and developed into
written proofs. Finite optimization is discovery evidence only.

The [private-clause and boundary certificate](docs/PRIVATE_CLAUSES_AND_BOUNDARY_ACCOUNTING.md)
gives an exact graph-level tool used in the completed SF proof. Formation
is equivalent to hitting at most4nclauses of size at most5in subcubic graphs;
minimality means every selected vertex owns a private clause. Under port-only
attachments, each selected non-port owns an internal private clause or is
the sole selected core neighbor of a selected port, whose charge cannot
be reused. Five general Lean theorems pass. A13kcore selection shows why
the older robust-deletion shortcut is insufficient, even though H0remains
safely deletable. Finite solver timeouts settle no new SF value; the exact
all-k SF question remains live.

The [bare Heawood port lemma](docs/BARE_HEAWOOD_PORT_COMPENSATION.md)
now proves |C|+t<=8 for the restriction of any ambient minimal forming
set to a broken Heawood block, where t counts ports omitted together
with both internal neighbors. Two bare ports cost two selected vertices,
preventing repeated use of one deficit. A 25r-vertex core phase in Q_(2r)
disproves a core-only certificate cap, but forces r distinct attached
blocks to lose a vertex; consequently every minimal set with that phase
has size at most 72r=36k. The local Fano proof and all-r phase argument
are written proofs. Four Lean declarations check the general boundary
inference and conditional accounting; all 16,384 local selections,
twelve phase lengths and a literal 62-vertex ambient witness pass finite
controls. This does not settle the unrestricted all-k SF question.

The [general export theorem and bare-only obstruction](docs/EXPORTED_BOUNDARY_AND_BARE_ONLY_OBSTRUCTION.md)
now sharpen that picture. Any selected core non-port without a private
internal clause exports through a selected core port to an omitted
external vertex with exactly that selected neighbor; different owners
cannot share that vertex. Both general graph statements pass Lean.
However the stronger bare-only compensation rule is false: for every
r>=1 an explicit minimal set in L_(2r) selects25r core vertices and
62r vertices in total, with no bare Heawood ports at all. Its core
restriction itself forms, and its fourteen selected non-ports in the
base example all own internal clauses. A general triangle-free cover
pullback proves the all-r family; explicit base stars and62deletion
certificates are independently checked. Actual non-bare block losses
total11r, so this refutes the candidate rule, not the desired36k cap.

The [higher-cover density transfer](docs/HEAWOOD_HIGHER_COVER_BOUNDS.md)
now gives SF_2-beta_2<=floor(9n/196) for every graph cover factoring
through a connected Heawood double cover, including all connected regular
Heawood covers with nontrivial finite2-group deck group. Two quotient
types have explicit16-vertex certificates, checked in Lean, and improve
that bound to floor(n/49). A [sharp traceless-space threshold](docs/TRACELESS_SUBSPACE_THRESHOLD.md),
derived from de Seguins Pazzis's existing matrix-space theorem with a
self-contained binary proof, ensures such a quotient for every connected
regular Heawood cover whose deck group has at least four independent
binary characters. This includes nonabelian deck groups of unbounded
order, as well as elementary abelian covers of rank at least four.
These covers all satisfy the n/49gap bound. No exact higher-cover SF value
is assumed, and the matrix-space theorem is attributed to its source.

The [exact cover-stability criterion](docs/COVER_STABLE_MINIMAL_SELECTIONS.md)
now removes the global triangle-free restriction: a fixed minimal selection
is preserved by every graph cover exactly when every selected deletion
has a safe self or outside failure certificate. A missing certificate
constructs a two-sheeted cover with an explicitly redundant selected lift.
Both directions, the canonical cover and boundary/triangle-free corollaries
are checked in [Lean](formal/StarForming/CoverStability.lean), with22axiom
audits. For connected bases the counter-cover is connected by a separate
written proof. Independent controls check7,882minimal selections,
25,724pullbacks and250canonical counter-covers. Thus covering minimality
is fully resolved for a fixed selection; the dissociation gain in covers
remains a distinct obstruction to connected cubic gap amplification.
The written criterion, canonical counter-cover and connectedness corollary
have now received Oracle ACCEPT, with a concluding minimality qualifier fixed.

The [dissociation-cover budget](docs/DISSOCIATION_GAIN_IN_COVERS.md)
identifies two limitations of this route. Full fiber transversals on one
side of a cubic double cover cannot give a dissociation set larger than
half the cover. Connected even-prism covers have exactly zero additional
dissociation gain, proved by a fractional square-capacity certificate.
The exact private-owner surplus records repeated private neighbors with
their full multiplicity. Five further graph-level Lean declarations check
dissociation pullback/reflection and the local square capacity; the
global weighted count and all-prism formulas have complete written proofs.
An [explicit square certificate](docs/FRACTIONAL_SQUARE_GAP_OBSTRUCTION.md)
for every sharp G_d,d>=4 gives a shorter dissociation upper-bound proof.
These graphs have exact fractional square covers yet SF_2=beta_2+1,
so square capacity alone cannot establish the grid's proposed equality.
The certificate has positive closed-form weights in every degree and
is checked with exact rational arithmetic.

The [sharp cubic bipartite compensation theorem](docs/SHARP_CUBIC_BIPARTITE_GAP.md)
proves7SF_2<=3n+2beta_2 for all finite simple cubic bipartite graphs,
and the sharp gap bound SF_2-beta_2<=floor(n/14). Two explicit dissociation
exchanges pay2(|S|-beta_2) from3n-5|S| for every minimal selection,
including selected isolates. Heawood and its disjoint unions attain the
gap coefficient. Its focused Oracle review has accepted the complete
universal argument. Thirteen symbolic Lean audits and31,790corrected
exchange controls pass; the graph-level cardinal proof is written.
The [earlier weaker compensation proof](docs/CUBIC_STABILITY_COMPENSATION.md)
and its3n/34bound remain available as intermediate results.
The [exact isolate-tight structure](docs/CUBIC_ISOLATE_TIGHT_STRUCTURE.md)
reduces every case with delta=z to mixed selected even cycles and an
outside path/cycle system. Degree balance forces both high classes to
balance across the bipartition; a strict gap there needs selected isolates
on both sides. The corrected exchange now covers all such systems as
part of the full theorem.

A [port-deficiency theorem and exact connected family](docs/CUBIC_STABILITY_PORTS.md)
now identify a stability boundary: for every k>=1 there is a two-connected
cubic bipartite graph on 14+20k vertices with SF_2=8+12k and
beta_2=7+12k. These graphs attain the proved general inequality
7SF_2<=3n+2beta_2. Their positive gap stays one while SF_2/n tends to3/5,
so positive gap alone permits no uniformly smaller order coefficient.
The proof counts port deficiencies once; literal-star controls and three
independent integer-optimization checks support the general written proof.

## Results and verification

| Result | Scope | Verification |
| --- | --- | --- |
| Hypercube coloring number | All dimensions n >= 2 | Lean 4, pinned Mathlib; original modules from trureturing |
| Boundary matching | Feasible (T,M) in graphs with signed adjacency S^2=dI, d>=2 | Written energy estimate and Hall argument |
| Bipartite signed graphs and Cartesian products | All graphs satisfying the stated hypotheses | Written proof and exact matrix controls |
| Exact grafting theorem | Every finite nonempty base graph F | Written proof; tree-DP cross-checks |
| Unbounded gap on subcubic trees | R(P_k), every k>=1; gap floor(k/3) | Written proof; checks k=1..30 |
| Rectangular grid formula | Widths 8,9,10,11 at every positive length | Exact full-vector certificates, independently recomputed |
| Grid dissociation number beta_2=F | Every positive width and length | Written row-profile proof; exact finite checks |
| Directional Omega_H=Omega_V=F | Every positive width and length | Written ladder-rigidity argument; exact finite checks |
| Mixed matching bound with coefficient 5/6 | Every positive even-by-even rectangle | Written residual-geometry proof; exhaustive and constructed controls |
| Exact star-forming composition | Every finite b1-to-a1 interface relation on the fixed ten-vertex copies; SF_2=6r and beta_2=5r | General written proof; Lean SF bound and attainment; local finite controls |
| Subcubic star-forming gaps | Two-connected bipartite J_r, even r>=2; beta_2=13r/2, SF_2=7r, gap=order/22; arbitrary-outside core cap; cycle equality gives the degree threshold | General written proofs; standalone Lean certificates; independent deletion controls and full J_2 enumeration |
| Exact Heawood-port composition | Arbitrary simple graph on the ports of r broken Heawood blocks; SF_2=8r, beta_2=7r+alpha_0(Q), gap=the interaction graph's vertex-cover number | General geometric and saturation proofs; Lean arbitrary-outside cap; independent local, ambient and port-state controls |
| Cubic star-forming gaps | Two-connected cubic bipartite F_r, every r>=1; girth six, beta_2=7r+floor(r/2), SF_2=8r, exact gap=ceil(r/2) | General Fano and interface proofs; standalone Lean certificates; independent base and family controls |
| Sharp regular star-forming order bound | All d-regular graphs, d>=1: SF_2<=floor(dn/(2d-1)); exact regular extremal structure; bipartite attainment forces beta_2=SF_2; weighted grid corollary | General injective witness-capacity proof; twelve symbolic Lean audits; 1,301 finite graph controls; completed Oracle review |

The Lean theorem explicitly states psi_sq(Q_n)=2^(n-1). The beta_2 identity
was already established by Sahbi and also follows from the written proof;
beta_2 is not defined in the archived Lean module. The subsequent structural
and grid results are not yet Lean formalized. The unrestricted mixed-direction
grid coloring formula remains open.

The grid extension uses Sahbi's Omega reduction and max-plus method. Huang's
signed hypercube matrix is the key input to the hypercube proof. Tree-result
priority is still to be compared with the earlier caterpillar work cited
by Sahbi; the draft makes no historical priority claim about that work.

## Contents

- `manuscript/paper.tex`: research draft, proofs and tree recurrence appendix.
- `docs/GRID_RESULTS.md`: current grid results and links to their complete proofs.
- `develop/`: two exact C++ transfer implementations, independent small controls,
  tree recurrence, and mathematical notes.
- `develop/results/`: full integer state vectors, finite readouts and hashes.
- `formal/`: standalone Lean package with the original two proof modules.
- `docs/REPRODUCE.md`: build and verification instructions.
- `docs/RELEASING.md`: verification, version tags and Zenodo connection.

See [releases](https://github.com/the-omega-institute/subquorum-colorings/releases)
for the PDF and source/reproduction archives. CI recomputes certificate endpoints
from the empty state, runs finite controls, builds the paper, and checks Lean.

## Attribution and license

This repository contains the project's research artifacts. Sahbi is credited for
the source problems and methods; this deposit does not assign him authorship
of the current draft. The manuscript author list is provisional.
AI assistance included mathematical exploration, code development, cross-checking
and drafting, as described in the manuscript.

Original material and the imported trureturing modules are distributed under
Apache-2.0; see `LICENSE` and `NOTICE`. External dependencies retain their
upstream licenses. Cite `CITATION.cff`; a DOI will be added only after Zenodo
confirms an archival record for this repository.
