# Holes obstruct an uncorrected Euler bound for whole receivers

20 October 2026. A general all-k counterexample to the proposed stronger
invariant rho_H<=chi(R_H) under single terminality. This is not a
counterexample to rho_H<=1 for fully frozen components, or to the grid
coefficient-one inequality. The distinction is certified explicitly below.

## 1. A complete matching-closed receiver with k holes

Let k>=1. Work first on the integer lattice with the physical tile partition
having even/even lower coordinates. Take the endpoint set

    H=({0,...,5} x {0,...,4k+1})
      minus union_(i=0,...,k-1) ({2,3} x {4i+2,4i+3}).

Thus a 3-by-(2k+1) rectangle of physical tiles loses k middle-row tiles,
in alternating interior columns. Every remaining tile contains four P.
Match its two rows horizontally inside that tile. These edges form an
actual perfect matching of H. Set

    T={(-1,0),(-1,4k+1),(6,0),(6,4k+1)}.

Translate everything by (2,2) into a 10-by-(4k+6) grid, retaining the physical
phase. All unlisted vertices are blank. The endpoint graph is connected:
the top and bottom two-row strips are intact, and the undeleted even tile
columns join them. The holes are interior and pairwise separated by an
undeleted tile column.

Every selected vertex has exactly its one corner endpoint neighbor and no
selected neighbor. The four outer endpoint corners have two P neighbors
and one T neighbor. Every other endpoint has at least three P neighbors:
the deleted rectangles have height and width two, are separated, and avoid
the outer boundary, so no remaining endpoint has two deleted neighbors.
The pair is feasible and single-terminal. H is its sole complete endpoint
component, and all of its actual mates lie in its receiver.

## 2. Exact charge and topology

The physical receiver is exactly the remaining full-P tiles. It has

    |R_H|=3(2k+1)-k=5k+3,
    |H|=4(5k+3),       |T intersect V(R_H)|=0.

Every tile is deficient, contains two internal matching edges and has no
saturated transfer. Its original corrected charge is zero. Equivalently,
the closed-receiver identity gives

    rho_H=0+|H|/2-2|R_H|=0.

Regard R_H as the union of its closed unit tile squares, with all their
edges and vertices. It is a rectangle with k disjoint interior square
holes. Its cubical Euler characteristic is

    chi(R_H)=1-k.

One can also obtain this by starting with the full tiled rectangle and
removing each hole's 2-cell while retaining its four boundary edges and
vertices, which still belong to adjacent receiver tiles. Each removal
decreases V-E+F by one. Consequently for every k>=2,

    rho_H=0>1-k=chi(R_H).

There is no constant additive correction independent of k that repairs
rho_H<=chi(R_H)+C under single terminality. A boundary or topological proof
using this expression must account for holes or use a stronger hypothesis.

## 3. Why this does not refute the frozen-receiver ceiling

Each endpoint has at most one selected neighbor, so the initial freezing
wave is empty and the complete freezing closure is empty. More explicitly,
choose either checkerboard color and promote every matching endpoint of
that color, deleting all opposite-color endpoints. Each promoted vertex
then has no endpoint neighbor and at most one original T neighbor. Original
T only loses neighbors. This is a feasible nonempty bundle by the bundle
criterion, preserving the objective.

Thus these examples are single-terminal but not bundle-terminal. They
cannot be presented as counterexamples under the complete freezing
hypothesis. Their charge zero also satisfies the weaker ceiling rho_H<=1.
For fully frozen components the proposed Euler bound and the ceiling need
separate proofs or counterexamples; neither is decided here.

The checker constructs every displayed matching and selection, recomputes
the original charge and cubical V-E+F, checks the empty freezing closure,
and executes both explicit color bundles. The general proof is the preceding
all-k argument. This note is outside the separate straight-chamber review
request and has no newly inferred Oracle acceptance or Lean verification.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
