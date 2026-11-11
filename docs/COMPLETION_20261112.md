# Structural equality and source-dependent completion: 12 November 2026

## Exact clean-witness port composition

For any finite simple interface graph R, orient its edges arbitrarily and
join the clean witness ports of copies of G_(1,1). The
[general composition theorem](SELECTED_STAR_PORT_COMPOSITION.md) proves
beta_2(F_R)=7r+alpha(R), while an explicit minimal forming selection has
size8r and only P3 stars/isolates. A full eight-set in a block forces both
internally matched ports, so the full blocks must form an independent
set. Seven-sets omitting both ports attain every complementary block.

Path interfaces give connected maximum-degree-four examples at all orders
12r with beta_2=7r+ceil(r/2), and selected deficit floor(r/2). Cycles give
beta_2=7r+floor(r/2) and deficit ceil(r/2) for r>=3. The r=2 path has
selected16 and true beta15. This is a genuine unrestricted gap. All-size
proofs and an independent checker received **ACCEPT** with no correction.
All three original artifacts were reconstructed with matching hashes; the
original checker ran unchanged with assertions and reproduced its entire
60,288-byte report. Its84 exact-solver calls cover up to48 vertices; the
22 large-family entries up to1536 vertices check certificates, with all-size
optimality supplied by the proof. See `output/selected-star-ports-review.json`.
No exact SF value or rectangular-grid conclusion is asserted.

## Genuine selected-star gaps and a sharp clean-leaf bound

The [complete new proof](SELECTED_STAR_COMPONENT_GAPS.md) refutes the
unrestricted selected-star minimal-set inequality. A connected18-vertex
bipartite graph has a minimal12-set inducing only P3 stars and isolates,
while its true unrestricted dissociation number is11. The general family
G_(a,b) has6(a+b) vertices, minimal selected size4(a+b), and exact
beta_2=3(a+b)+max(a,b,2), proved by four exhaustive structural cases and
three explicit attaining sets. Its forced leaf-retaining optimum is
3(a+b)+max(a,b), which equals the true optimum except at(1,1).

For every such selected-star/edge/isolate selection whose every centre
has a clean leaf with a private outside witness, a general distinct-helper
budget proves |S|-beta_2<=floor(n/12). The assumption is explicit; it is
not inferred from minimality. Connected maximum-degree-six graphs attain
this coefficient at all orders24r: |S|=16r and beta_2=14r. All-size proofs,
actual graph certificates and independent finite checks are included.
Independent review returned **ACCEPT**, with no mathematical correction. All
four original artifacts were reconstructed with matching hashes; the unchanged
checker ran with assertions and reproduced its entire report byte-for-byte.
See `output/selected-star-gap-review.json`. These graphs have pendant vertices and
are not full rectangles; no exact SF_2 value is asserted for them.

## Matching exchanges that retain selected star leaves

The [new exact exchange formula](STAR_LEAF_MATCHING_EXCHANGE.md) is

    max_(D subset S union W, L subset D, Delta(G[D])<=1)|D|
       =|S|-c+e-nu(G[W union I]).

Here selected components are stars/edges/isolates, c counts nontrivial star
centres, L their leaves, e=|L|=|W|, and I is the set of all selected isolates.
Witness conflicts and shared isolates appear in one bipartite graph, with
matching/cover dual certificates. At most one selected isolate implies the existence
of a dissociation set of at least |S| for every such minimal forming set,
even when centres occupy both bipartition classes and witnesses conflict.
The distinct-helper bound e-t>=2c-1 is another sufficient criterion. The
matching formula also certifies the prior full6-by-6 independence obstacle,
where c=2,e=4,nu=2 and the exact leaf-retaining optimum is18.

A connected bounded-degree family shows the exact limitation. Its minimal
forming S has size8r and beta=8r, while every dissociation set retaining all
star leaves has size at most7r. Four disjoint P3 paths per block prove the
true upper bound; explicit dissociation sets and matching/cover certificates
attain both values. It has12r vertices,15r-1 edges and maximum degree5 for
r>=2. The leaves' witnesses are unique and constitute every outside vertex,
so alternative witnesses or additional outside vertices cannot repair
leaf retention. These are full all-r proofs, with a standalone finite
checker. Independent review returned **ACCEPT** with no mathematical
correction: all three artifacts were reconstructed with matching hashes,
the original checker ran unchanged with assertions enabled, and its
50,622-byte report was reproduced exactly. See
`output/star-leaf-budget-review.json` for the complete response and scope. The broader selected-star inequality is refuted by the new construction
above. Arbitrary full-grid equality remains open.

## Geometry at arbitrary width

The [witness geometry note](GRID_WITNESS_GEOMETRY.md) proves, for every
minimal forming S in every full rectangle,

    2|S|-mn<=|Z|+|E|-|H|-ceil(K/2).

Here Z comprises selected components of order at most two, E the degree-two
or degree-three selections without a direct deletion witness, H the
degree-four selections, and K counts selected perpendicular siblings of
chosen clean leaves at exceptional centres. Two caps per H centre are
pairwise disjoint across distinct centres. Exceptional caps have capacity
at most two and are disjoint from H caps. Direct and clean witnesses are
reserved without counting the same leaf resource twice. The exact residual
identity retains the actual exceptional-cap union and unused omitted set.

A separate simultaneous auxiliary-multigraph exchange gives |S|<=beta_2
when selected components are stars/edges/isolates with independent chosen
leaf witnesses. This applies whenever selected degree-at-least-two vertices
lie in one bipartition class, at any width. A complete 6-by-6 example refutes
automatic independence but admits an explicit size-preserving exchange.
The finite audits cover 190,798 grid subsets, 28 protected degree-four
centres, and 50,196 exchange constructions on small bipartite graphs and
explicit cycle/dummy/conflict fixtures. General proofs are written in full.
The independent audit at2958b91 returned ACCEPT without mathematical
changes: all five manifest files were reconstructed, both original checkers
ran unchanged with assertions enabled, and both reports matched byte-for-byte.
Complete execution scope is in output/grid-witness-geometry-review.json.

## Five-row grids at every length

The [five-row proof](FIVE_ROW_STAR_FORMING_EQUALITY.md) establishes
`SF_2(P_5 square P_n)=beta_2=psi_sq=F(5,n)` for every positive n. The
value is 4,6,9 at n=1,2,3 and `8floor(n/3)+3(n mod3)` for n>=4. The
new conclusion is the SF upper bound. The same general deletion-witness
frontier, now stored compactly, gives complete vectors with 8,227,512
reachable states and the exact identity V17=V14+8. Transfer homogeneity
and exact initial values prove the result at arbitrary length.

The independent literal-star implementation compares all 33,554,432 local
kernel entries against the generator, reconstructs all seventeen prefixes
with standard unordered maps, compares every entry and complete support
at both endpoints, and verifies the translation. Its whole-board controls
compare individual subset acceptance with global minimality on 1,082,400
subsets of 5-by-1 through 5-by-4. The new generator also reproduces the
accepted h3/h4 endpoint vectors. Both existing width-five colouring
implementations were rerun and reproduced four archived outputs exactly.
No state truncation or new Lean execution is used. Independent final
review returned ACCEPT at c5d4c45: both original programs completed, both
large vectors were regenerated with exact hashes, and the checker report
and all four prior colouring outputs matched byte-for-byte; both dimensions of a still-uncovered rectangle must
now be at least six. Arbitrary-width equality and a universal 5/6 gain
remain open.

## The four-row extension

The [four-row proof](FOUR_ROW_STAR_FORMING_EQUALITY.md) closes the upper
forming number at height four for every positive length:
`SF_2(P_4 square P_n)=beta_2(P_4 square P_n)=2n+(n mod2)`.
An explicit alternating-column dissociation set attains the bound and has
self-deletion witnesses. The full-vector certificate is V17=V15+4, on all
342,768 reachable states in the 3^16 state domain. The general frontier
proof and homogeneous-transfer induction prove the infinite conclusion.

The independent Python implementation reconstructs both vectors by literal
stars and compares all entries. It also checks all 1,048,576 local masks
and 69,904 whole-board subsets. The vectors are regenerable output, with
their exact hashes in the concise report. With the prior width-four
colouring theorem, all three parameters coincide. This is a computer-assisted
result. The separate independent audit returned **ACCEPT**, ran both
unchanged implementations, and reproduced both reports byte-for-byte and
both vector hashes. It reconstructed the general frontier argument without
assuming the height-three numerical result. The reviewer-reported source
hashes match our pinned manifest; that manifest was not in their attachment.
[The review record](../output/grid-star-height-four-review.json) gives the
complete execution and provenance scope. No code or certificate changed.

## Upper forming number and triple equality at height three

The [three-row proof](THREE_ROW_STAR_FORMING_EQUALITY.md) establishes
`SF_2(P_3 square P_n)=beta_2(P_3 square P_n)=5floor(n/3)+2(n mod3)`
for every positive n. Together with Sahbi's prior width-three colouring
formula, it gives SF_2=beta_2=psi_sq on all three-row rectangles. The new
contribution is the SF upper bound, not a new colouring formula.

The exact frontier retains four columns with omitted/selected-unwitnessed/
selected-witnessed digits. All radius-two formation and deletion tests are
performed at the middle column of each five-column window. A general
soundness/completeness proof identifies accepted strings with globally
minimal forming sets. Both complete maximum-score vectors, at lengths
12 and 15, have 14,726 reachable states and satisfy V15=V12+5 entrywise.
Transfer homogeneity proves the recurrence for every later length.

An independent Python implementation uses literal star triples and
reconstructs both vectors from the empty prefix. It also compares every
44,954 selected subset on 21 small boards with literal global minimality.
The one-column boundary has its own corrected and exhaustively checked
tail. This is a computer-assisted theorem with a finite exact premise,
not scalar extrapolation. The independent audit returned **ACCEPT** and
ran both unchanged implementations and the prior Omega supplier. All
eight supplied result files were reproduced byte-for-byte; the reviewer
also reproduced the erroneous one-column tail and verified its correction.
The [review record](../output/grid-star-transfer-review.json) preserves the
complete answer, pinned source hashes and exact scope. The 33,824 local
patterns describe literal-kernel construction; the explicit per-subset
acceptance comparisons number 44,954. The full arbitrary-width triple
equality and universal 5/6 improvement remain open.

## Exact decoration formula and sharp path-residual values

The [decorated-interface theorem](EXACT_DECORATED_INTERFACE_FORMULA.md)
proves SF_2(D(H))=12|H|-sf_2(H) for every finite simple H. Each interface
vertex is replaced by the fixed 21-vertex F_2 module. A selected interface
with internal activity costs at least two of the twelve available units.
These extra units pay, once each, for any extra interface selections
needed to turn a globally minimal decorated set into a forming set of H.
Conversely every minimal forming set Q of H lifts to a minimal decorated
set of size 12|H|-|Q|. Taking Q minimum proves the exact identity.

For H=P_s, minimum forming sets have exact size
mu(s)=2floor(s/4)+min(s mod4,2), by selected-run counting and printed
attaining binary patterns. Hence the earlier connected residual has
SF_2(R_s)=12s-mu(s), and its single-ear discrepancy is exactly mu(s).
This closes the residual optimum, rather than merely proving it grows.
The roots in that family still have increasing degree; fixed-degree
error boundedness follows from the separate local-stability theorem.

The independent checker covers every interface graph through order 5,
all binary path strings through order 14, 1,265 lifted minimal sets, 70,717
specified deletion witnesses, and 44 seeded globally minimal decorations.
There is no exhaustive SF search over the large decorated graphs.
Independent **ACCEPT** reconstructed the general proof and dependencies,
ran the unchanged original checker with assertions enabled, and reproduced
its 550-byte report and stdout byte-for-byte. None of its original 1,309
upper-map calls triggers augmentation. The reviewer separately checked
two minimal decorations with 54 deletions, including two augmentation
indices choosing the same added vertex. A separate local literal-star
checker now reproduces these cases; its output is recorded separately.
The complete response and execution scopes are preserved in
`output/decorated-interface-review.json`.

## Fixed-degree local stability and arbitrary interfaces

The [local stability theorem](LOCAL_STAR_FORMING_STABILITY.md) proves,
for every finite simple graph G and U subset V(G), with H=G-U,

    SF_2(H)-b_3(U)<=SF_2(G)<=SF_2(H)+|U|+b_5(U),

where b_r counts surviving vertices within distance r of U. Its stronger
adaptive version repairs exactly the unformed residual vertices A,
which lie within distance two of U, and preserves all old selections
outside B_2(U) union B_3(A). Radius-three addition locality and radius-five
canonical-repair locality both have explicit sharp P9 witnesses. These
are sharp certificate radii, not sharp parameter-difference constants.

For k disjoint square ears, the exact two-selections cap improves this to

    0<=SF_2(G)-(2k+SF_2(F))<=|F intersect B_5(roots)|.

If Delta is the maximum degree of the final graph, its upper bound is
2k(Delta-2)sum_(j=0)^4(Delta-1)^j. Thus unbounded single-ear error
cannot occur at fixed maximum degree. The earlier unbounded examples
require growing root degrees, as their constructions explicitly state.
Deleting a general interface and using disjoint-union additivity gives
a two-sided composition estimate without assuming minimality of a
restriction to an arbitrary component.

The standalone literal checker passes1,100 exhaustive small graphs,
96 seeded larger graphs, the sharp P9 example and a claw regression:
973,858 induced-selection states,669,163 interface repairs and329 ear
models. The research-stage answer's overstrong all-minimal-set minimum
is explicitly rejected by the claw. Final statements use the correct
fixed-S inequality. Independent **ACCEPT** reconstructed the entire local proof and supplying
square theorem, ran the unchanged original C++17 checker with checks
active, and reproduced its622-byte report byte-for-byte. Exact input
hashes, full response and finite execution limits are recorded separately
in `output/local-star-stability-review.json`. No new Lean is claimed.

## Bipartiteness does not rescue exact partial-ear addition

The [bipartite obstruction note](BIPARTITE_PARTIAL_EAR_OBSTRUCTION.md)
gives exact connected families F_q,G_q, q>=1, with

    |V(F_q)|=10q+1, |V(G_q)|=10q+5,
    SF_2(F_q)=max(5q+1,6q-1), SF_2(G_q)=6q+2.

G_q is obtained by adding roots d,e with de,dy and attaching just one
square along de. Thus deleting the roots gives exactly F_q. For q>=2
the full SF exceeds2+SF(F_q) by one. Disjoint unions give an additive
error k with k ears, within bipartite graphs. The q=2 graph is connected,
has maximum degree five and exact SF=14, while the residual21-vertex
graph has SF=11. The violating selected pair in the ear is adjacent
and internally active; formation of the exterior y, rather than
root activity from the residual selection, permits the extra vertex.

The original Oracle research supplied the25-vertex lower witness and
residual upper proof. The local reconstruction proves the all-q local
caps with an arbitrary exterior at y, both residual attaining sets,
and the additional exact whole-graph upper bound6q+2. The independent
all-q audit returned **ACCEPT**, executed both unchanged original
checkers, and reproduced both reports byte-for-byte. The C++ checker
computes literal formation for all2,097,152 residual and33,554,432 final
subsets. A nonminimal set is rejected at its first forming deletion;
each accepted minimal set passes every deletion. It finds beta/SF=11/11
and13/14. Named-vertex certificates test q in {1,2,3,4,8,16,32,128},
not all integers up to128:16 models,3,314 deletions and1,180 specified
witnesses.

A stronger one-ear amplification has exact values

    |V(J_s)|=21s+4, SF_2(R_s)=11s, SF_2(J_s)=12s+2,
    SF_2(J_s)-(2+SF_2(R_s))=s.

Here the residual is the disjoint union of s copies of F_2, all attached
through their y vertices to a single root d. The base and final graph
are connected and bipartite. The arbitrary-exterior cap bounds each
copy by12; the common active root lets every copy attain12 simultaneously.
A separate independent **ACCEPT** reconstructs this all-s proof and ran
the unchanged new certificate checker, reproducing its report byte-for-byte:
s in {1,2,3,8,16,64}, six models and1,140 single deletions. The two complete
audits and exact input hashes are in
`output/bipartite-partial-ear-review.json`.

The [connected-residual amplification](CONNECTED_RESIDUAL_EAR_AMPLIFICATION.md)
adds a path through the y vertices and attaches its odd/even indices to
the two roots. It proves, for every s>=1,

    |V(R_s)|=21s, |V(J_s)|=21s+4,
    SF_2(R_s)<=12s-ceil(s/3), SF_2(J_s)=12s+2.

The base, final graph and residual are all connected and bipartite.
Every residual module contributing12 would omit y and all Z vertices;
formation of y then requires a selected neighbouring y, whose module
contributes at most11. The modules with a positive loss therefore form
a dominating set of the path, forcing at least ceil(s/3) total loss.
One active root pair removes this requirement in the final graph,
while each selected vertex retains a private deletion witness. The
single-ear discrepancy is consequently at least ceil(s/3). The residual
has maximum degree six; the final root degrees grow with s. The later
decorated-interface theorem above sharpens the residual bound to the exact
value 12s-mu(s), and the discrepancy to mu(s). The original proof and review
of this connected-residual construction establish the weaker domination
bound and the exact final-graph value independently of that later theorem.

The standalone checker passes seven sizes s in {1,2,3,4,8,16,64},1,190
single deletions and1,190 named witnesses, and32,766 path subsets. Its
independent review returned **ACCEPT** and ran this unchanged original
checker with assertions enabled, reproducing both its349-byte report
and stdout byte-for-byte. Its complete response and precise scope are
recorded separately in `output/connected-residual-ear-review.json`.
The reviewer also reconstructed the referenced square-ear lemma directly;
that accepted proof is now included in the note. The earlier audits do
not cover this later construction. All-s bounds rely on the written proof.

## Four exact parameters on two-connected outerplanar median graphs

The [ear-ladder family](EAR_LADDER_FOUR_PARAMETERS.md) gives, for every
r>=1, a graph of order16r, maximum degree4, two-connected, outerplanar
and median, with exact values

    beta_2=sf_2=SF_2=8r,
    psi_sq=Omega=9r.

The proof classifies the local representative budget of each attached
square. Only an opposite T pair with one old P root can exceed2 units,
contributing5/2. In each two-column ladder interval at most one of the
two row squares can have that type. This gives Omega<=9r, counting
each actual matching endpoint by one half. Alternating the selected
row in consecutive four-column blocks gives a legal9r-colour partial
sub-quorum colouring. The square-pair classification gives all star-forming
values and the exact dissociation value independently.

The standalone checker literally examines all65536 subsets of the
16-vertex base, its6668 actual matchings and1369324 possible disjoint
T subsets after the forced >=2-P-neighbour exclusion. It obtains
beta=SF=8, all1296 minimal forming sets, and Omega=9 without using the
exceptional-square upper proof. Ten sizes through r128 pass2620 coloured
closed-neighbourhood tests and2096 deletion witnesses. All-r statements
have the written proof; finite controls do not replace it.

The triple-equality extension to two-connected outerplanar median graphs
is therefore false. The weaker SF_2=beta_2 question in planar degree-four
median graphs remains open; this family satisfies that equality. It
does not consist of full rectangular grids. In fact H_r is the4-by-4r
grid with all between-pair edges on its first and last rows deleted;
for r=1 these are just two boundary edges. The note gives the explicit
coordinate isomorphism.

The new four-parameter theorem received independent **ACCEPT** at
snapshot a7737b0. The reviewer ran the original Python checker unchanged,
with assertions enabled, reproduced the report byte-for-byte, and
independently verified all-r counting, block-boundary colouring and
structural proofs. The checker does not enumerate all colourings or
calculate lower sf separately; those values follow from the proof.
Only a previous/next-block wording clarification and the explicit
coordinate identification were added afterward; no checker changed.
The complete response and exact scope are in
`output/ear-ladder-four-parameter-review.json`.

## Square attachments and the exact composition obstruction

The [square-ear note](SQUARE_EAR_STAR_FORMING_COMPOSITION.md) proves that
for an arbitrary finite simple base B and a matching of k old edges,
adding a square along each edge gives, with F the base minus all roots,

    beta_2(G)=2k+beta_2(F),
    2k+SF_2(F)<=SF_2(G)<=2k+|V(F)|.

Every minimal forming set selects exactly two vertices in each square.
For a perfect root matching all 6^k pair choices are precisely the minimal
forming sets, so beta_2=sf_2=SF_2=2k. There are companion pendant-path
formulas and a full-root classification with 3^k minimal sets.

The proposed exact SF addition for partial root sets is false. For every
m>=5 an explicit 6m-vertex square family has F=K_m disjoint-union K_m,
SF_2(F)=4, beta_2(G)=2m+4 and SF_2(G)=3m. The analogous pendant-path
example has 5m vertices and the same values. Full all-m upper proofs and
three explicit deletion witnesses per index explain the activity
dependency responsible for the error m-4. These families use cliques;
they do not refute a bipartite or median equality.

Square attachments preserve medianity, planarity and two-connectivity;
they preserve maximum degree four when all roots previously have degree
at most three. Fully covered ladders provide an infinite outerplanar
median degree-four class with no automorphism mapping every vertex to
a neighbour, and with all minimal forming sets classified.

The Python checker passes 329 square models,1099 path models,681648
literal subsets,126 fully covered models,2008 minimal-set lifts and58263
local-cap tests. It checks80 larger pair selections,7 structural median
models (including2 with interior-edge attachments),6651 metric triples,
117 vertex deletions, and2124 specified obstruction deletion witnesses.
The independent C++ implementation checks all7962624 two-per-square
sets and248832 two-per-path sets for m=5, obtaining exact SF=15 in both.
Its exhaustive domain uses the proved local-cap lemma; it does not
enumerate all 2^30 unrestricted subsets or assume the p/q upper proof.

## Restricted median graphs

The [restricted median note](RESTRICTED_MEDIAN_CUBE_CHAINS.md) reconstructs
the cube-chain theorem: in any finite planar median graph with Delta<=4,
every connected collection of intersecting induced cubes is an induced
convex C_4 square P_(r+1). External edges meet only the end layers and
number at most eight; when r>=2, each outside component attaches to one
end. Two-connectivity requires at least two attachment vertices per
nonempty outside component. Planarity is used through the bipartite
Euler bound, which excludes adjacent-face branching and cycles of cubes.

Every finite two-connected median graph with Delta<=3 is a ladder or
Q_3 and has SF_2=beta_2. The classification is explicitly attributed as a
consequence of Bandelt--Chepoi--Eppstein Proposition9, checked in the full
arXiv0905.4537v1 primary manuscript. The forbidden book has degree four;
the source's suspended cogwheels have hubs of degree at least five.
The existing bipartite prism theorem supplies the exact parameter values.

The structural checker passes39 models,84 cubes in24 components,69816
metric triples and786 vertex deletions. A nonplanar Q_4 control confirms
that degree four and medianity alone do not force the cube-chain property.
These checks support the implementation of the all-size proof. The
two-connected planar median Delta<=4 equality remains open, including
the exchange problem in cube-free squaregraph regions and compatible
activation/deletion data across square interfaces.

The independent complete-package audit found the new ear, pendant,
all-m obstruction and cube-chain arguments sound and ran all three
original checkers, reproducing every report byte-for-byte. Its verdict
was REVISE for one missing exact dependency locator: the upper-SF
prism theorem used in the parameter corollaries. The restricted note
now states that theorem precisely and links its complete proof at
957ef94, Section5 Theorem4/Corollary5, with definitions and the prism
isomorphism in Sections1/3. This supplier file is byte-identical to
the pinned revision. Targeted independent closure returned **ACCEPT**,
after reconstructing the full supplier proof and all three applications.
That closure did not rerun code or independently authenticate the remote
GitHub bytes; the local check verified that the supplied complete source
is byte-identical to the pinned Git object. The first complete audit's
three original checker executions remain the execution evidence.
Complete response and input scope are in
`output/square-ear-composition-review.json`. No new Lean execution is claimed.

## Median graphs: explicit failure and bounded-degree amplification

The [median obstruction note](MEDIAN_STAR_FORMING_OBSTRUCTION.md) proves
that for every r>=1 there is a connected median graph G_r with

    |V(G_r)|=38r, Delta(G_r)=5,
    beta_2(G_r)=21r, SF_2(G_r)>=22r.

The base is P_4 square P_4 square K_2 with two pendant leaves at each
of three lower corners. A four-cube pattern proof gives beta_2=15 after
removing those three attachment vertices; simultaneous leaf normalization
then gives beta_2=21. A 22-set has explicit witnesses for every deletion.
Bridging distinct leaf ports preserves medianity, the exact dissociation
value, and all minimality witnesses. This disproves the general median
SF/beta equality and shows a linear gap with a fixed maximum degree.
It does not determine exact SF_2 of these examples or refute rectangular-grid
equality. They contain pendant vertices and degree-five vertices.

The standalone checker passes all256 cube subsets, all4096 forced block
pattern tuples,893000 median triples, and10010 deletion witnesses over
10 family sizes through r=256. The written proof establishes the all-r
claim; the finite controls test its implementation. The original Oracle
research response supplied the fixed counterexample. A separate independent
review returned **ACCEPT** for the reconstructed proof and new connected
amplification. It inspected the checker source and supplied outputs but
did not execute code. Local execution and proof acceptance are distinguished
in output/median-obstruction-review.json. The final note makes the face
incidence count and the column containing the deleted vertices explicit.


## Arbitrary Cartesian prisms and their sharp gaps

The [complete prism note](ADJACENT_INVOLUTIONS_AND_PRISM_GAPS.md) proves

    SF_2(H square K_2)=Omega(H square K_2)=2n-nu(D(H))

for every finite simple H, with no bipartiteness requirement. The upper
witness argument extends to any graph with an adjacent involutory
automorphism; its quotient determines exact Omega and an SF upper bound.
Prism attainment uses a layer selection over the residual critical-set
graph, with explicit opposite-rung deletion witnesses. An arbitrary graph
with this involution need not attain the SF upper bound: K_(2n) has
SF_2=2 and Omega=n for n>=3.

Over all n-vertex bases, both maximum gaps SF_2-beta_2 and SF_2-psi_sq are
exactly max(0,n-4). For n>=5 their positive equality bases are respectively:

- K_n with any matching of edges deleted, for SF_2-beta_2;
- K_n or K_n with one edge deleted, for SF_2-psi_sq.

For H=K_n with m disjoint edges deleted, n>=5, the complete values are

| Parameter | Exact value |
| --- | --- |
| beta_2 | 4 |
| psi_sq | 4 if m<=1, and 5 if m>=2 |
| SF_2 and Omega | n |

These are all-size proofs. A complete-base prism is n-regular,
n-connected and vertex-transitive, so those properties alone do not
extend the bipartite four-way equality. The note also proves direct
terminal completion in any paired graph for every feasible independent
T, including selections using both layers. Independence excludes direct
TT paths; no such TT-free assertion is made for arbitrary adjacent T.

`python3 scripts/check_paired_graphs.py` passes 1,100 prism bases and
1,065,509 literal subsets, 60,296 minimal forming sets, 4,166 general
paired graphs and 1,052,741 further subsets, 89,860 further minimal sets,
6,715 representative pairs, 5,397 direct completions including 496
mixed-layer selections, and 3,396,244 canonical partial colourings over
79 models. The latter exhausts all bases through order four and three
near-complete bases of order five. Twelve larger prism certificates and
31 larger extremal-family certificates also pass.

The research-stage Oracle audit reconstructed and accepted all proposed
formulae and equality classifications; it did not inspect or run code.
The complete note, both new Python files and their existing matcher
dependency received independent **ACCEPT** at f44adbc. The reviewer ran
the original complete checker unchanged, with assertions enabled, and
reproduced the 813-byte report byte for byte. The final note clarifies
the n<=4 case of the gap corollary and refers explicitly to vertices of T
in representative attainment. Two later checker assertions require all
selected vertices to have deletion witnesses and connect the outer optimum
to its matching dual. A full local rerun with these assertions reproduced
the same report. The external run predates these small additions. Complete
responses and exact scopes are in `output/paired-graph-review.json`.
No new Lean verification or historical priority claim is made.

## Extended double covers and Cartesian prisms

The [complete extended-cover proof](EXTENDED_DOUBLE_COVER_PARAMETERS.md)
establishes, for every finite simple H of order n,

    SF_2(E(H))=beta_2(E(H))=psi_sq(E(H))=Omega(E(H))
              =n+delta(H)=2n-nu(D(H)).

The proof covers nonbipartite bases as well. The independent-set deficiency
delta(H) equals the ordinary double-cover Hall deficiency. A TP-to-PZ rung
injection bounds every feasible representative pair, allowing selected
vertices in both colours. A separate minimal-forming proof counts the
union of deletion witnesses with capacity two per empty rung. Neighbours
of isolated selected rung edges are reserved and contribute no witness
capacity to the other doubly selected rungs. This proves the SF upper
bound without a general-graph assertion SF_2<=Omega.

There are exact nonnegative remainders describing every optimal feasible
representative pair and every maximum minimal forming set in this class.
For example, a maximum minimal set can induce a square; the statement is
an equality of optima and includes these nondissociation maximizers.

The common value and an attaining set have polynomial matching/vertex-cover
certificates. If H is bipartite, E(H) is its Cartesian prism and the common
value is 2 alpha(H). This closes all four parameters on every bipartite
prism, including all ladders and all hypercubes of dimension at least two.
Taking a prism eliminates any SF_2/beta_2 gap in a bipartite base.

For arbitrary actual M and any feasible white selected set T, disjoint
two-rung swaps provide a full auxiliary matching that pairs all selected
vertices directly with black terminals. Thus the true TH optimum is zero
for every nonnegative weighting on the whole extended-cover class.

Run `python3 scripts/check_extended_double_cover.py`. The independent
literal controls cover all 1,100 labelled bases of orders zero through
five, 1,065,509 selected subsets, all 54,160 minimal forming sets and their
65,820 empty-rung budgets, 36,306 feasible representative pairs on bases
through order four, and 5,036 direct-terminal constructions. These certify
14,236 white selected subsets, rather than 14,236 separate construction
calls. Fifteen larger matching/dual and attaining-set certificates cover
base orders 8,17,64,257,1024. All-size conclusions use the written proofs.

The initial three-parameter theorem and zero-completion algorithm received
independent ACCEPT at snapshot 5044cd7; the reviewer ran its complete
embedded checker and reproduced the report. That reviewer also supplied
a malformed external certificate exploiting Python negative indices. The
checker now validates vertex domains before indexing and rejects that
exact regression. The new SF theorem, its equality remainders and the
expanded checker received a separate independent **ACCEPT** at snapshot
6000a72. The reviewer reconstructed the all-size proof, extracted the two
Python files verbatim, ran the full unchanged checker with assertions
enabled, and confirmed equality of the generated and attached JSON data.
The exact negative-index fake certificate was also separately rejected
before graph indexing. The final note adds the requested explicit standard
partial-colouring definition; no proof or algorithm change was needed.
`output/extended-double-cover-review.json` preserves both complete verdicts
and the exact attached-file manifests. No new Lean verification or full
priority comparison is claimed.

## Source-dependent TH completion

The [complete proof note](EXACT_TH_OPTIMIZATION_AND_LADDERS.md) gives five
results, with an exact integer implementation and independent controls:

1. Binary labels, fixed to one at selected white terminals and zero at
   other white terminals, and equal along actual and chosen auxiliary
   edges, minimize exactly the genuine TH expense. Label-one cycles can
   overcharge individual pairs but never improve the minimum. Every
   minimizing labelled pair gives a truly optimal full matching.
2. Deleting complete disjoint retained paths and adding their fixed
   expense gives the exact retaining problem, while allowing all remaining
   HH paths to reroute freely.
3. A standard frontier DP needs just the label and auxiliary matched bit
   per active vertex. At most h+1 vertices are active, for shorter bounding
   side h. It uses O(n 4^(h+1)) state transitions; tuple and integer-bit
   overheads are stated separately. It returns an optimum and full witness
   or reports infeasibility. This solves the unrestricted exact optimizer
   question left in the preceding residual-Hall notes at bounded width.
4. On every full 2-by-n ladder, any monochromatic selected Q set with at
   most one occupied neighbour per selected vertex has a zero-expense
   full completion. Disjoint adjacent-column swaps give a linear proof
   and construction for every n, arbitrary M and nonnegative weights.
5. On the full 3-by-6r grid, an explicitly feasible all-white-Q selection
   and four unit actual edges per block have exact optimum r. Each black
   centre needs its own paid component, and nine printed auxiliary edges
   per block attain the bound. Thus the height-two universal zero-expense
   conclusion cannot extend to height three.

## Reproduction

Run from the repository root:

```sh
python3 scripts/check_source_label_dp.py
```

The checker uses literal perfect-matching enumeration and overlay scoring,
not the DP recurrence, to determine small true optima. Its output records:

| Control | Exact scope |
| --- | --- |
| Rectangular models | 750 models, 37,659 full-N scores; 631 have feasible selected sets |
| Masked boards | 180 models, 279 full-N scores; 92 are infeasible |
| Alternative scans / value-only | 122 / 61 comparisons |
| Independent colour enumeration | 26 models |
| Full ladder actual-match enumeration | 10,992 matchings for n=1,...,8 |
| Selected subsets covered by maximal-T certificates | 79,016 combinations |
| Ladder DP / translation and transpose controls | 114 / 228 |
| Full versus retaining 2-by-4r | 36 controls, r through 128, 1,024 vertices |
| Positive 3-by-6r family | 18 controls, r through 128, 2,304 vertices |

The controls include zero and 401-bit actual weights, a positive-cost
ladder violating the neighbour condition, an infeasible retained-path
example and a balanced board with an isolated vertex. Finite tests check
implementation; all-size statements have the written proofs above.
No Lean execution or verification is claimed.

## Scope and review

The proof/source snapshot 4a3aa6e received independent **ACCEPT for the
mathematics and optimizer**. The reviewer inspected both Python files and
reported 17,788 calls to the unchanged optimizer using a new literal-reference
harness, including 13,148 full-matching scores. That harness also reproduced
the 10,992 ladder constructions and all 36 cascade work-counter records.
The original attached checker initially could not run because the attachment
omitted its helper-module dependency. This package issue is corrected: the
exact independent enumerator, overlay scorer and serializer are now included
in the checker, whose only project import is the optimizer under test; it
creates its output directory. An isolated local full rerun reproduced all
three committed reports byte-for-byte. No claim is made that the reviewer
executed this corrected original checker.

The later height-three theorem received its own independent **ACCEPT**, based
on its all-r proof and explicit coordinates; that reviewer did not claim code
execution. `output/source-label-dp-review.json` records both exact review
scopes, responses and the completed packaging correction. The empty-board,
preprocessing-memory and forced-scan conventions are explicit in the note.

The earlier forced-cascade review and its identical retry both ended with
terminal infrastructure failures and no mathematical response. The prior
positive-attainment equivalence and unit 18-by-18 optimizer-choice result
retain their existing ACCEPT, scoped to their original input.

## Remaining questions

| Question | Current status |
| --- | --- |
| All four parameters on E(H), and on every bipartite Cartesian prism | Proved by the matching and witness-capacity theorem above |
| SF_2 and Omega on arbitrary Cartesian prisms | Proved; sharp SF/beta and SF/psi gaps and all positive equality bases classified |
| Extending four-way prism equality to arbitrary bases | False; the exact near-complete families above separate the parameters |
| Exact genuine TH expense at fixed grid width, with retained paths | Solved by the source-label DP, exponential in width |
| Zero expense for all feasible ladder and E(H) instances | Proved, arbitrary M and nonnegative weights |
| Zero expense for every feasible full grid instance | False: the explicit 3-by-6r family has expense r with unit actual weights |
| Simultaneous endpoint counting for overlapping Hall-tight regions | Proved with one global HH budget; compatible physical routing and a universal coefficient gain remain open |
| SF_2=beta_2 for all finite median graphs | False; the bounded-degree connected family above has linear gap |
| SF_2=beta_2 for two-connected subcubic median graphs | Proved, using the cited ladder/cube classification and the prism theorem |
| Exact SF addition for arbitrary partial square or pendant-path attachments | False; explicit all-m families have additive error m-4 |
| Exact SF addition for partial square attachments to bipartite bases | False; unbounded error with exactly one ear, even with connected base, final graph and residual |
| Unbounded partial-ear error at fixed ear count and fixed maximum degree | Impossible; explicit radius-five footprint and degree bound above |
| General composition through a bounded deleted interface | Two-sided local-error theorem for every finite simple graph; optimal constants remain open |
| Full root coverage by square or pendant-path attachments | Complete minimal-set classification and exact beta_2=sf_2=SF_2 |
| SF_2=beta_2 for two-connected planar median graphs of maximum degree four | Open; cube chains and full-coverage ear classes proved |
| SF_2=beta_2=psi_sq for two-connected outerplanar median graphs of maximum degree four | False; H_r has beta_2=SF_2=8r and psi_sq=Omega=9r |
| Rectangular-grid SF_2=beta_2=psi_sq when one side is three | Proved for every positive other side; complete-vector computer-assisted proof, independently accepted with original executions |
| Rectangular-grid SF_2=beta_2=psi_sq when one side is four | Proved for every positive other side by the full-vector extension; separately accepted with original executions |
| Rectangular-grid SF_2=beta_2=psi_sq when one side is five | Proved for every positive other side; independent ACCEPT with both original executions and exact vector hashes |
| Exact exchange within S union W retaining all selected star leaves | Solved by bipartite matching for every fixed witness assignment |
| Selected-star minimal sets with at most one selected isolate | Proved cardinality at most beta_2, allowing witness conflicts and centres in both parts |
| Always retaining every selected star leaf in a size-preserving exchange | False; connected12r family has leaf optimum7r but true beta=8r equals the selected size |
| General selected-star minimal-set inequality without further hypotheses | False; both the18-vertex example and connected maximum-degree-four port families have genuine gaps |
| Exact dissociation composition through clean witness ports | Proved beta_2=7r+alpha(R) for every oriented finite interface graph; selected size8r and degree-four path/cycle counterexamples |
| Sharp gap for all selected-star minimal sets without the private clean-leaf hypothesis | Open coefficient question; the zero-gap assertion is false, while the clean-leaf subclass has the sharp n/12 theorem |
| Sharp gap for selected-star sets with a private outside witness at one leaf of every centre | Proved: floor(n/12), attained by connected maximum-degree-six graphs at all orders24r |
| Arbitrary-width rectangular-grid SF_2=beta_2=psi_sq | Open; new arbitrary-width cap inequality and one-class exchange criterion proved, not an unconditional equality |
| Improvement of the universal mixed-direction 5/6 coefficient | Open |
| Sharp gap under simultaneous specified degree/connectivity restrictions | Open beyond the previously proved exact classes and general bounds |
| Intrinsic recognition of positive sharp n/10 equality in bipartite graphs | Proved by intrinsic layers and the exact all-subsets neighbourhood criterion; separate from E(H) |
| Replacing the incomplete-core all-subsets criterion by local conditions | Open simplification question; the exact recognition theorem is already proved |

The new structural theorem does not extend automatically to wider grids:
if both sides of a rectangle are at least three, a corner has degree two
but all its neighbours have degree three. No adjacency-preserving map can
send that corner to an adjacent vertex. Such a rectangle therefore cannot
admit the adjacent-pair involution used for the extended-cover argument.
This rules out applying this particular structural criterion, without
deciding the equality itself. No arbitrary-width polynomial claim is made.
The sharp bipartite n/10 gap theorem and previous composition manuscript
are preserved. No email, submission or submitted-version edit is implied.
