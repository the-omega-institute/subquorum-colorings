# Long residual paths: a component obstruction and a corridor replacement

29 September 2026. This note advances the residual-path approach to the grid
upper bound. It does not prove the coefficient-one bound.

Use the fixed aligned 2x2 tiling and the notation of GRID_ABSORPTION_PROOF.md.
For a residual connected component J, write

    excess(J) = |E(J)| - sum_{Q in J} r_Q.

The exact global identity is q=sum_J excess(J), with isolated deficient tiles
included. Nonpositive excess in every component is sufficient for q<=0, but
the componentwise condition is false even after capacity-one forks are removed.

## An arbitrarily long positive component without forks

For k>=1 take the rectangle with rows 0,1,2,3 and columns 0,...,N-1,
where N=2k+4. Put

    T = {(0,0), (0,N-1), (2,0), (3,1), (2,N-1), (3,N-2)}.

Choose matching edges:

    ((0,2i+1), (0,2i+2))             for 0<=i<=k;
    ((1,2i),   (1,2i+1))             for 1<=i<=k;
    ((1,1),    (2,1)), ((1,N-2), (2,N-2)).

All other vertices are blank. The matching edges have distinct endpoints.
Every T vertex has exactly one occupied neighbor, so the pair is feasible.
There are six T vertices and 2k+3 matching edges, giving

    |T|+|M| = 2k+9,    H=4k+8,    q=1-2k.

The two outer upper tiles are zero-capacity leaves, each attached to its
lower saturated tile. Each of the k inner upper tiles is full P, with one
internal matching edge and capacity one. Their residual edges form a simple
leaf-to-leaf path of length k+1, with excess (k+1)-k=1. Each of the k inner
lower tiles is blank, isolated, and has capacity two, contributing -2.
These components account for the whole q=1-2k.

For k>=2 there is no capacity-one fork: no internal tile is adjacent to both
leaves. Thus fork normalization alone leaves possible positive components of
unbounded path length. Positive component excess is not a counterexample to
the grid bound; the negative components pay for it.

## A replacement valid in an ambient rectangle

**Proposition.** If the displayed 4x(2k+4) pattern occurs as an aligned patch
inside any feasible pair on a larger rectangle, delete its k matching edges
in row 1 and their endpoints from P, and add (2,2i) to T for 1<=i<=k.
The resulting pair is feasible, has the same objective, increases |T| by k,
decreases |M| by k, and reduces the number of matching edges internal to the
fixed tiling by k.

**Proof.** Deleting occupied vertices can only help the constraints at old
T vertices. Every new T vertex lies strictly inside the patch and has blank
neighbors above and below. Its right neighbor is blank; its left neighbor
is blank except at i=1, where it is the existing saturated attachment P.
Thus its occupied degree is at most one. No new T is adjacent to an old T,
and distinct new T vertices are distance two apart. Outside vertices cannot
be adjacent to the new T vertices. Every undeleted matching edge retains its
endpoints and the deletions preserve matching disjointness. The objective
change is +k-k=0, and exactly k internal edges were removed. QED.

Within the standalone construction, the upper component now has capacity 2k
and excess 1-k<=0; each lower inner tile has capacity one. The operation
therefore removes the positive component. For k=1 it is the blank-companion
fork move; for k>=2 it handles a family of arbitrarily long paths.

The blank-neighbor hypothesis is essential to this proof. It is not a claim
that every long path has such a strip, or that all internal matching edges
can be removed from a general feasible pair.

## Bounded search for another obstruction class

The search in develop/search_residual_paths.py enumerates simple LL tile paths
whose internal tiles all have capacity one and contain no internal matching
edge. Each internal tile is either t=1,h=s=0 or t=h=0,s=1. In both cases the
two residual corners must be adjacent: in the first case diagonal P corners
would give T two occupied neighbors; in the second case the attachment must
be adjacent to its forced blank, leaving an adjacent residual pair.

The enumeration chooses those corners, both possible outward sides, the
T/attachment placement, and all three leaf types. It includes the forced
saturated attachment tiles and checks all physical T-neighbor constraints.
The first edge is fixed using translations and square symmetries. Other tile
visits cannot overlap the already placed leaf/internal/saturated roles; simple
capacity-one components cannot revisit an internal tile. All unassigned
vertices can be blank. Recorded exclusions apply only to this enumerated class.

For lengths 2 through 8, there is no feasible patch in that class. As a
positive control, allowing internal edges at length three reproduces all
32 configurations of the earlier classification. Canonical coordinate witnesses
agree after translations, rotations and reflections. The two enumeration orders
share the patch builder, so this is a control rather than independent verification.
This suggests investigating whether every simple all-capacity-one LL component
must contain an internal matching edge. That is an open structural question,
not an all-length consequence of these finite runs. Paths passing through
capacity-two tiles are outside this search.

## Reproduction and next target

```sh
python3 develop/check_residual_corridors.py --output develop/results/residual-corridors.json
python3 develop/search_residual_paths.py --length 2 --through 8 --output develop/results/residual-paths-no-internal.json
python3 develop/search_residual_paths.py --length 3 --allow-internal --output develop/results/residual-paths-length3-control.json
```

The corridor checker tests k=1,...,40 in all eight square symmetries (320
images), uses a direct coordinate feasibility check, reconstructs residual
components, checks fork absence for k>=2, and verifies the replacement.
The all-k result follows from the proof above, not from the finite range.

Next focus on bent routes, capacity-two passages, and corridors whose adjacent
band is occupied. Any charging rule must preserve the physical corner data and
allow compensation between distinct residual components. A purely componentwise
bound, even after fork removal, cannot be the general proof.
