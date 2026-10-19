# Exact colorwise guard criterion for long matched-interior two-row ladders

19 October 2026. Continuation of SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md.
This is an objective-preserving reduction for genuine multi-square components,
not an additional payment for every P-square. All coordinates are zero-based.
No submitted manuscript changes.

## 1. General reduction theorem

Let (T,M) be feasible in a finite rectangular grid: P is the set of matching
endpoints, A=T union P, and every T has at most one neighbor in A. Extend
labels outside the rectangle by blank. Translate/rotate a two-row strip to

    C={(row,column): row in {0,1}, 0<=column<w},   w>=4,
    I={(row,column): row in {0,1}, 1<=column<=w-2}.

Assume precisely:

1. Every vertex of C belongs to P.
2. Every vertex of I has its actual matching mate in I. Thus M restricted
   to I is a perfect matching of the induced2-by-(w-2)ladder. Its matching
   directions may be arbitrarily mixed.

Write G={(-1,1),(-1,w-2),(2,1),(2,w-2)} for the four guards. For a grid
bipartition color epsilon, let G_epsilon be the two guards whose grid color
is opposite to epsilon. These are one site at each end, and G_0 and G_1
partition G.

No assumption on other exterior labels, single terminality, alignment with
the fixed tiling, or the shape of the rest of the endpoint component is needed.

**Exact colorwise criterion.** For a grid bipartition color epsilon,
promote all vertices U of I with (row+column) mod2=epsilon and remove their
matching mates. This bundle is feasible if and only if both guards in
G_epsilon are blank. When feasible it uses exactly w-2 matching edges. It
preserves |T|+|M|, adds w-2 selected vertices, and removes every P vertex of I.
All w-1 P-squares wholly in C disappear; no P-square is created anywhere.

Proof. Each matching edge in I joins opposite grid colors. Hence U chooses
one endpoint from each of its w-2 edges, and its mates are exactly I minus U.
The new occupied set is A minus (I minus U). Original selected vertices
therefore do not gain any occupied neighbors.

Every neighbor in I of a promoted vertex has opposite grid color and is
deleted. For an interior column2,...,w-3, its only possible retained neighbor
outside I is the one outside C in the perpendicular row direction. For a
vertex in column1 or w-2, there can instead be a retained neighbor in its
adjacent end column0 or w-1. Its perpendicular exterior neighbor is one of
the two blank guards in G_epsilon. Since w>=4, the two boundary columns of I are distinct:
no promoted vertex is adjacent to both end columns. Every promoted vertex
therefore has at most one retained occupied neighbor. The promoted vertices
are mutually nonadjacent. Thus all newly selected vertices are feasible too.

Exactly w-2 edges are deleted and w-2 vertices added to T, so the objective
is unchanged. The entire endpoint set inside I disappears, and every unit
square contained in C uses at least one of these columns. Outside I the
endpoint set only shrinks, so no other square is created.

Conversely, an occupied guard in G_epsilon is adjacent to a promoted
boundary vertex of I. That vertex also retains its occupied end-column
neighbor. The guard lies outside I and is not removed. These two distinct
retained neighbors make the promoted vertex infeasible. This proves necessity. QED.

**Four-blank-guard corollary.** If all four guards are blank, either color
bundle is feasible, with the objective and square-removal conclusions above.

The theorem works at the boundary: a guard outside the physical rectangle
is already blank. All four sites must still be accounted for, not silently
omitted when an exterior occupied band is present.

## 2. Consequences for terminal configurations and straight-arm components

**Terminal obstruction.** In a configuration with no nonempty fixed-side
promotion bundle, every all-P two-row strip of width at least four either
has an interior matching edge leaving I, or has an occupied guard in each
of G_0 and G_1. In the latter case there are at least two distinct occupied
guards of opposite colors. This follows by applying the exact criterion
to each color. It is a necessary alternative for bundle terminality.
Two such guards block both canonical color bundles; they need not block
all other bundles, so this is not a sufficient terminality criterion.

**Straight-arm corollary.** Suppose an endpoint component H consists exactly
of C and four straight vertical arms, extending north from its two upper
corners and south from its two lower corners. Assume all four arms are
nonempty and each central corner is matched to its arm's first P. Then for
w>=4 the component admits the reduction, in every feasible exterior.

Proof. Each arm is a path whose only attachment to the core is its corner.
Its length is odd and its remaining matching is forced. None of the other
core vertices can be matched outside I: the four corners already have their
arm mates, and H has no endpoint beside a middle core vertex. Thus the
matching on I is closed.

Consider the north guard (-1,1). It is adjacent to P at (0,1) and to the
first corner-arm P at (-1,0), so it cannot be T. If it were P it would
belong to H, contrary to H's specified complete vertex set. Hence it is B.
The same argument proves all other guards blank. Apply the theorem. QED.

All P-squares of this straight-arm component lie inside C when w>=4:
the parallel exterior rays are separated by w-1>=3 columns. After the
reduction its remaining endpoint components are the two vertical end-column
paths with their arms, so contain no square. Further single promotions
terminate in the already classified straight-comb form; deleting P never
creates a square and every move preserves the objective. Other endpoint
components are unaffected by this reduction, apart from losing occupied
neighbors, which cannot harm feasibility.

Thus long ladder cores in this explicit class are removable, rather than
receivers requiring an independent payment for every square. Genuine terminal
multi-square components must leave this class through matching escape,
occupied guards, another endpoint attachment, or a short core.

## 3. Sharp short-core obstruction

For w=3, I is one column. Each of its two vertices is adjacent to both end
columns, whose vertices remain occupied. Either central color promotion would
therefore create a selected vertex with two retained occupied neighbors,
even if all four guards (two distinct sites in this degenerate case) are blank.

The complete6-by6two-square fixture in SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md
realizes this obstruction: the strip is at rows2,3and columns2,3,4, its
middle vertical matching edge is internal, and the outside guards (1,3),(4,3)
are blank. Its four pendant P freeze, then its middle pair, then its four
corners. It has no oriented bundle and whole-grid charge-1, with the full
saturated attachment correction. Thus the width condition is necessary,
and the short frozen case cannot be removed by the proposed central bundle.
This is an obstacle to extending this reduction, not to the global inequality.

The blank guards are also substantive. If a boundary vertex of I has an
occupied perpendicular guard, that guard and its neighboring end-column P
both remain occupied in this particular central bundle. Promoting the vertex
of its color is infeasible. This establishes the exact local failure of that
color's proposed rule; another bundle may still exist. The companion checker
adds a feasible selected guard and explicitly tests this distinction.

## 4. Verification and remaining scope

The theorem and its straight-arm consequence have general proofs above.
Physical controls range over multiple widths, all perfect matchings of small
strict interiors, larger vertical/horizontal examples and independent arm
lengths when feasible. They directly verify the original and transformed
pairs, both color bundles, objective equality, disappearance of core squares,
and the short-core and occupied-guard failures.

The completed run covers widths4through12and all230interior perfect
matchings in that range, with4122feasible arm placements,32976symmetry
images,65952color bundles and230normalizations to square-free combs.
Eighteen arm placements fail original feasibility and are excluded. A
separate complete16-mask guard test at each width has137feasible masks,
7infeasible masks and274color checks;74feasible masks block both canonical
colors. The exact iff is checked independently against physical feasibility.

Scoped Lean verifies the general integer-grid fact used in the proof: after
deleting the opposite interior color and its two active guards, any promoted vertex
has at most one retained grid neighbor for every integer width>=4. It also
checks the sharp width-three failure. The matching-to-bundle adapter, physical
embedding and full reduction remain written proofs. Finite enumeration is
auxiliary, not a substitute for those proofs.

The combined local sequential Lean4.33.0audit passes43declarations, including
the two new ladder statements; no sorry or new/compilation-reduction axioms.

Occupied guards are obstructions to this reduction, not compensation tokens.
Different strips can refer to the same exterior vertex, so the necessary
two-guard count cannot be summed across components without an explicit
ownership or incidence bound. This theorem uses no donor budget, and its
objective-preserving moves are sequentially safe: occupied labels only
decrease, but a later strip must still satisfy its own matching closure.

Both single-square review turns completed REVISE and their valid capacity,
exposition and counterexample-scope corrections have been applied. This
later ladder reduction is outside those review inputs. Source coverage,
general occupied-guard compensation, escaping interior matchings, branching
multi-square cores and the unrestricted grid/triple equality remain open.

    python3 develop/check_ladder_reduction.py --output output/ladder-reduction-controls.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
