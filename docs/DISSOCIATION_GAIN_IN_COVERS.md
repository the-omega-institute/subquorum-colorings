# Dissociation in covers: exact budgets and two limits on amplification

19 October 2026. All graphs are finite, simple and undirected. A dissociation
set induces maximum degree at most one. The results below separate actual
new selections in a cover from full pullbacks and identify two precise
obstacles to a generic covering argument. No priority claim is made.

## Full pullbacks and the direction of the parameter inequality

For a locally bijective map pi:H->G and selection D in G, its full pullback
is dissociation whenever D is. Any two selected neighbors of a selected
lift project to selected neighbors of its image. Base dissociation makes
their images equal, and local injectivity makes the lifts equal.
If pi is surjective, the converse follows by lifting a base selected center
and any two selected neighbors. Hence for a k-sheeted cover

    beta_2(H)>=k beta_2(G).                                (1)

The general graph pullback/reflection equivalence is checked in
formal/StarForming/DissociationCover.lean, with no finite-cardinality
assumption. The counting corollary (1) is written. The additional gain
beta_2(H)-k beta_2(G) depends on selections which are not full pullbacks.

## An exact owner budget in cubic bipartite graphs

Let L,R be the parts of a cubic bipartite graph, each of size N. For
A subset L, write r_j for the number of R vertices with j neighbors
in A. Let p be the number of distinct A vertices which occur as the sole
neighbor of at least one degree-one R vertex. The exact one-part formula
from COVERING_PULLBACK_AND_CUBIC_SEARCH.md gives

    beta_2(G)=max_A (|A|+r_0+p).

For each such A, degree counting gives 3|A|=r_1+2r_2+3r_3 and
N=r_0+r_1+r_2+r_3. Thus

    3(|A|+r_0+p-N)=3p-2r_1-r_2
                       =p-2(r_1-p)-r_2.                  (2)

Every counted private owner has at least one degree-one R vertex, so
e=r_1-p>=0 counts repeated private-neighbor incidences beyond the first
for each owner. In particular

    3(beta_2(G)-N)=max_A (p-2e-r_2).                       (3)

The maximum is nonnegative, since A=L gives zero. The bracket is always
a multiple of three. Strict improvement over one bipartition part is
equivalent to finding A with p>2e+r_2. Owners are counted once; counting
all private vertices as distinct owners would omit the exact penalty 2e.
This is a reformulation of the existing exact formula, not a new claim
about the complexity of computing beta_2.

## A transversal cannot detect gain in a two-sheeted cubic cover

Let G be cubic bipartite with base parts of size N, and H a two-sheeted
cover. Suppose A in the lifted left part contains exactly one of the two
lifts of each base left vertex. Then

    |A|+r_0+p<=2N=|V(H)|/2.                              (4)

For each base right vertex, its three distinct base neighbors each supply
exactly one selected lift. Across its two lifts the selected-neighbor
counts therefore sum to three. They are either 0 and 3, or 1 and 2, so
exactly one of the two is of selected degree zero or one. Summing over
base right vertices gives r_0+r_1=N. Since |A|=N and p<=r_1,
(4) follows. Equality requires p=r_1, so the degree-one right vertices
must have distinct owners.

This argument does not require connectedness or any sign normalization.
It proves that a dissociation set larger than half of H cannot have a
left part that is a full fiber transversal. If its left part nevertheless
has N vertices, it must contain both an empty base fiber and a doubly
selected base fiber. It does not claim that every gaining selection has
the same number of left and right vertices.

Thus searching only for one selected point lift above each Fano point
will necessarily miss the dissociation gain in connected Heawood double
covers. This is a failure of that restricted witness search, not evidence
against the desired Heawood bound beta_2>=15.

## A fractional square certificate can prevent every gain

Suppose a balanced bipartite graph G has nonnegative weights lambda_C
on a collection of four-cycles, with

    sum_(C containing v) lambda_C=1  for every vertex v.  (5)

Every dissociation set meets a four-cycle in at most two vertices:
any three of its four vertices contain a selected vertex with two selected
neighbors. Extra edges do not invalidate this upper bound. Summing yields

    |D|=sum_C lambda_C |D intersect C|
       <=2 sum_C lambda_C=|V(G)|/2.

The last equality follows by summing (5) over vertices, so
4sum_C lambda_C=|V(G)|. Either bipartition part gives the matching lower
bound, proving beta_2(G)=|V(G)|/2. The local square capacity is checked
in Lean; the finite weighted summation is the written argument above.

If a k-sheeted cover preserves every certificate four-cycle as k disjoint
four-cycles, give each lifted cycle its base weight. The lifted weights
still satisfy (5), because each lifted vertex lies in exactly one lift
of each incident base certificate cycle. Hence

    beta_2(H)=|V(H)|/2=k beta_2(G).                         (6)

The entire cover may be connected. A global nontrivial sheet permutation
does not force strict dissociation gain when the local capacity certificate
survives. This is a sufficient mechanism for zero gain, not a converse
classification of all zero-gain graphs or covers.

## Explicit connected cubic counterexamples to automatic strict gain

For even m>=4 let P_m=C_m square K_2. Its vertices are (j,s), with
j modulo m and s in {0,1}, with horizontal cycle edges and vertical rungs.
It is simple, cubic, bipartite and two-connected. A spanning cycle visits
the top row in increasing order, crosses the final rung, visits the
bottom row in decreasing order, and crosses the first rung.

There are m square faces, each vertex belongs to exactly two, and weight
one-half on each face satisfies (5). Therefore beta_2(P_m)=m.
For every k>=1 the map

    P_(km)->P_m,   (j,s) maps to (j mod m,s)

is a locally bijective k-sheeted cover. The source is connected and
two-connected, and the same face count proves beta_2(P_(km))=km.
For k>=2 this gives a nontrivial connected cubic bipartite cover with
exactly zero additional gain. This refutes the proposed rule

    connected nontrivial cubic bipartite cover
       implies beta_2(H)>k beta_2(G).

It does not refute (1), a Heawood-specific strict bound, or a proposed
star-forming gap inequality. We make no all-orders claim about SF_2(P_m).
The prisms have four-cycles, whereas Heawood and its covers do not; the
square certificate does not supply an obstruction for Heawood covers.

Conversely, even an exact square certificate does not force star-forming
equality. FRACTIONAL_SQUARE_GAP_OBSTRUCTION.md gives closed-form weights
for every sharp G_d, d>=4, while SF_2=beta_2+1. It also provides an
independent all-degree dissociation cap for those single-block graphs.

## Heawood witnesses and the remaining proof obligation

In the existing normalized double-cover controls, signature1has an
attaining left selection of size7 with p=7,r_1=7,r_2=4. Equation(2)
gives surplus 3 and hence beta_2=15. Signature 10 has a size-eight left selection
with p=8,r_1=8,r_2=2, surplus 6 and beta_2=16. The checker records literal
attaining sets and independently recomputes these two optima. These are
examples, not a proof for all signatures.

The structural implication is now proved in HEAWOOD_DOUBLE_COVER_GAIN.md:
binary switching classes identify with traceless3-by-3matrices, a complete
algebraic classification gives six nonzero types, and explicit fifteen-sets
prove strict gain for all connected double covers. The original Oracle
research question completed; its proposed argument was independently
expanded and the six local certificates checked. The previous255-signature
computations are not used as a proof premise. HEAWOOD_HIGHER_COVER_BOUNDS.md
further transfers this density to arbitrary covers admitting such a quotient;
two explicit sixteen-sets give a stronger bound for two quotient types.

## Verification

Use

    python3 scripts/check_dissociation_covers.py --output output/dissociation-cover-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit dissociation --lean PATH_TO_LEAN --output output/dissociation-cover-formal-check.json

The formal audit checks dissociation pullback, reflection, equivalence,
four-cycle triple exclusions and capacity two. It does not claim a Lean
proof of the global fractional summation, prism parameter formulas or
the subsequent matrix classification. All general conclusions
above have written proofs independent of the finite controls.

The recorded controls pass 11,894 full-pullback/reflection selections
in 760 covers of all 75 labeled graphs of orders one through four;
18,144 local square subsets in 36 prism covers; 2,268 vertex-deletion
connectivity checks; 12 independent small-prism optima; and all 32,640
full fiber transversals in the 255 connected Heawood double-cover controls.
Five local graph declarations pass Lean4.33.0 in 6.214 seconds with peak
child RSS 691,453,952 bytes, allowing only standard axioms. Memory and
actual lean/lake basenames were checked before sequential compilation.
