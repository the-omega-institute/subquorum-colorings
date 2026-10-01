# Boundary-aware compensation for filled corridors

30 September 2026. Research note, separate from the manuscript version supplied
for the arXiv update. Baselines: public research `57645edfddc70fc59d7a45d5db32e761fa75c647`
and Appendix B of manuscript `f79975a27933a6ba7b7ebcca706807650cb043a8`.
Notation follows [the absorption proof](GRID_ABSORPTION_PROOF.md).

We prove an adjacent-band compensation inequality with an exact boundary term.
It permits occupied bands and capacity-two passages. The boundary term is
necessary: an explicit infinite family has a positive corridor component and
**zero capacity throughout its adjacent band**, with compensation only in other
tiles. We also give a bent-path witness and a capacity-two route that revisits
tiles, identifying two different ways a resource count can be overstated.
The unrestricted coefficient-one inequality remains open.

The [transport follow-up](COMPENSATION_TRANSPORT.md) proves compensation through
arbitrarily many specified neutral bands and constructs equality examples whose
only negative-excess component is arbitrarily far from the positive corridor.
Thus bounded-radius charging of the initial residual deficits is insufficient.

## 1. What the existing argument leaves open

Appendix B proves the five-sixths bound using its specified port routing.
Two-edge LL paths are forks; three-edge LL paths have injective internal-edge
or immediate-LH charges. Proposition B.13 handles a specified straight corridor
with a blank adjacent band. It does not establish an arbitrary-path replacement.

The outstanding cases include bent LL paths of length at least four, routes
through capacity-two tiles (including repeated visits), occupied neighboring
bands, and sharing a compensator between paths or components. The previous
length-2-to-8 search excludes only simple all-capacity-one paths without an
internal matching edge. It says nothing universal about these other cases.

There are three distinct resources: residual capacity, slack terminals, and
vertices that can be promoted after deleting matching edges. They cannot be
identified. The ledger below counts each residual incidence exactly once.

## 2. A routing-independent ledger

For each deficient tile Q define

    rho(Q) = deg_Gamma(Q)/2 - r_Q.

For a tile set U, sum rho only over its deficient tiles. Then

    q = sum_Q rho(Q).

For a whole residual component J this equals e(J). For a subset U it equals

    rho(U) = C_inside(U) + C_crossing(U)/2 - R(U).             (1)

Thus an edge between two accounting regions contributes one half to each.
This identity is valid for every routing, including routes revisiting a tile.
For a positive-capacity tile its contribution is minus half its unused-port
count. Each zero-capacity leaf contributes +1/2. Consequently

    e(J) = (number of leaves in J - number of slack ports in J)/2.

Two slack terminals are one unit of compensation; a single HH path cannot pay
two LL demands because its endpoints lie in different tiles.

## 3. A two-row blank-surplus lemma

**Lemma 1.** Consider two rows of even length w >= 2, labeled T, P, B.
Suppose:

1. Every upper-row T has only B neighbors within these two rows.
2. Every lower-row T has at most one occupied neighbor within these rows.
3. The two upper endpoints are not T, and the two lower endpoints are B.

Then the number of B vertices exceeds the number of T vertices by at least two.
The P vertices need not admit a matching for this combinatorial statement.

**Proof.** No column contains two T vertices. Call a T good if its vertical
neighbor is B; associate that distinct B with it. Every other T is a lower-row
T with an upper P. Let X be their column indices. Each member of X is an
interior column, and both neighboring lower vertices are B. Neither neighboring
upper vertex can be T: it would neighbor the upper P and violate assumption 1.
Thus the columns in the path-neighborhood N(X) contain no T and each supplies
a lower B. The same holds for the endpoint columns 1 and w.

The elements of X are nonconsecutive. Divide them into maximal chains with
successive difference two. If X is nonempty and has d chains, their neighbor
sets are disjoint and |N(X)|=|X|+d. If d>=2, this already gives two extra B's.
If d=1, its neighbor set has constant parity; since w is even it cannot
contain both endpoints. Adjoining the missing endpoint again gives at least
|X|+2 columns. If X is empty, the endpoints themselves give two. These B's
are in columns containing no T, so none was associated to a good T. Altogether
there are at least (# good T)+|X|+2 = |T|+2 B's. QED.

**Matching consequence.** If a matching has mu edges wholly inside the band
and j edges with exactly one endpoint there, writing t and b for its T and B
counts gives

    2w = t+b+2mu+j,
    t+mu+j/2 = w-(b-t)/2 <= w-1.                            (2)

The j/2 term must be retained when the band is not closed under the matching.

## 4. The compensation lemma, including boundary attachments

Let k>=2, N=2k+4. Take an aligned patch with rows 0,1,2,3 and columns
0,...,N-1 inside a full even-by-even feasible rectangle. Use the following
frame from Proposition B.13:

    T_frame = {(0,0),(0,N-1),(2,0),(3,1),(2,N-1),(3,N-2)};
    row-0 edges = {((0,2i+1),(0,2i+2)): 0<=i<=k};
    attachments = {((1,1),(2,1)), ((1,N-2),(2,N-2))}.

The other corners of the four outer tiles are B. Every vertex (1,c) with
2<=c<=N-3 is P. Its matching partner is otherwise unrestricted. In particular,
we do **not** require the k row-1 internal edges of B.13. The inner upper
tiles can have capacity one or two. Let U be all k+2 upper tiles, and let S
be the k lower inner tiles, the band with rows 2,3 and columns 2,...,N-3.
Its labels and matching are arbitrary subject to overall feasibility.

Let sigma be the number of matching edges from S to saturated tiles outside S.
Let Delta=(|B intersect S|-|T intersect S|)/2, which may be a half-integer if
the band has matching edges leaving it.

**Theorem 2 (boundary-aware adjacent-band compensation).** Under these exact
hypotheses,

    Delta >= 1,
    rho(U)=1,
    rho(S)=-Delta+sigma/2 <= -1+sigma/2,
    rho(U union S)=1-Delta+sigma/2 <= sigma/2.                (3)

In particular, if sigma=0, the band compensates the corridor's entire unit
of positive charge, even when S is occupied, contains capacity-two tiles,
or has residual matching edges to other components of the complement.

**Proof.** Every upper vertex in S has an occupied P neighbor immediately
above it. If it is T, all of its neighbors within S must be B. The upper
endpoints of S also have a lateral occupied P in the saturated end tile,
so they cannot be T. Each lower endpoint faces the T in that end tile, which
already has its own P neighbor; hence both lower endpoints are B.
Lemma 1 applies with w=2k and gives Delta>=1.

The two outer upper tiles are zero-capacity leaves. Every inner upper tile
is full P and therefore cannot attach to a saturated tile: such an attachment
would require a blank companion. If it has h internal edges, it has
r=2-h and degree 4-2h, and hence rho=0. The two leaves contribute 1/2 each.
This proves rho(U)=1, including the capacity-two case h=0.

A saturated tile in S has no P vertex. If it contains an upper T, the two
adjacent corners must be B, leaving at most the opposite T. If its two T's
are both in the lower row, both upper corners must be B. Thus no matching
edge is incident to any saturated tile within S.

Let mu count matching edges inside S, j those leaving S, and h the sum of
internal-tile matching edges there. In the residual graph,

    C_inside(S)=mu-h,   C_crossing(S)=j-sigma,
    R(S)=2k-t-h-sigma.

Substitution in (1) and then (2) gives the exact identity

    rho(S)=t+mu+j/2-2k+sigma/2=-Delta+sigma/2.

The tile sets U and S are disjoint. Adding their charges proves (3). All
constraints used hold in arbitrary feasible surroundings. QED.

**No reuse of compensation.** For any family of such frames whose sets
U_i union S_i are pairwise tile-disjoint, let W be the remaining deficient
tiles. Applying the identity, not independent path claims, gives

    q = sum_i (1-Delta_i+sigma_i/2) + rho(W)
      <= sum_i sigma_i/2 + rho(W).                          (4)

Every tile occurs once. Any crossing residual edge is split into its two
halves, even if it joins two frames. A band shared by two frames cannot be
inserted twice into (4); such overlapping choices need a new allocation proof.

**Concrete improvement over 5/6.** If the frames have sigma_i=0 and rho(W)<=0,
then (4) proves |T|+|M|<=mn/2, replacing 5/6 by 1 for this class. This includes
every standalone 4x(2k+4) filled frame with an arbitrary feasible lower band,
and any partition of the deficient tiles into such frames with no outward
saturated attachments. It is a geometric sufficient condition, not an
improved universal constant for arbitrary rectangles.

## 5. Sharp occupied bands: one compensator, not k

Start with B.13's complete matching, including the k row-1 internal edges.
In the lower band add

    ((2,2i),(2,2i+1))       for 1<=i<=k;
    ((3,2i+1),(3,2i+2))     for 1<=i<k.

All T vertices remain T_frame. These are disjoint edges on previously blank
vertices. The two lower band endpoints remain B, so each frame T retains its
single occupied neighbor. Thus this is feasible for every k>=2.

The upper residual component is an LL path with k+1 edges, capacity k and
excess +1. The band is a separate path with k-1 edges, capacity k and excess
-1. Each band tile has r=1. Its end tiles have degree one and each supplies
one slack terminal; its internal tiles have degree two and supply none.
The band supplies **one HH path**, of length k-1, in total. Here

    |T|=6, |M|=4k+2, H=4k+8, q=0, Delta=1, sigma=0.

This proves sharpness of the one-unit bound. Summing raw band capacities
would falsely count k units. Treating the two end terminals as separate
unit compensators would falsely count two. These fail as accounting rules;
the target inequality holds with equality.

## 6. Capacity-two passages and repeated tile visits

In the sharp example replace, for each i, the two horizontal matching edges
in rows 1 and 2, columns 2i,2i+1, by the two vertical edges across that square.
All occupied vertices, the matching size and feasibility remain unchanged.

All 2k inner tiles now have capacity two. The upper inner tiles have degree
four. The band end tiles have degree three, and its other tiles degree four.
All residual vertices belong to one component, with 4k edges and total
capacity 4k, so its excess is zero. The band has j=2k, sigma=0, Delta=1 and
rho(S)=-1; U still has rho(U)=1. Formula (3) continues to hold across all the
new residual edges crossing the interface.

For k=3 on the 4x10 rectangle, number tiles by row-major order, starting at
zero. The existing prescribed-routing verifier returns an eight-edge LL path
whose internal-tile visits are

    1, 6, 1, 2, 3, 8, 3,

and a two-edge HH path visiting 6,7,8. Tiles 1 and 3 are revisited by the LL
route; tiles 6 and 8 are shared by the two routes through different port pairs.
The route is simple in ports, not in tiles. A full capacity-two tile has no
slack at all, and neither a repeated visit nor a second port pair creates a
new compensation unit. The complete coordinates and route are in the checker
output. This is a concrete obstruction to extending a simple-tile-path charge
without tracking port ownership.

## 7. A sharp obstruction to unconditional adjacent-band compensation

For every k>=3, use a 6x(2k+4) rectangle. Start with the B.13 frame and its
row-1 internal edges. Add the following matching edges:

    ((2,2i),(2,2i+1))       for 1<=i<=k;
    ((3,2i),(3,2i+1))       for 2<=i<k;
    ((3,3),(4,3)), ((3,2k),(4,2k)).

Add T vertices

    (4,2), (5,3), (4,2k+1), (5,2k).

All unspecified vertices are B. The last two edges attach the band end tiles
to two saturated tiles in the third tile row. The new T vertices each see
their own attachment P and otherwise blanks. The old frame T constraints
remain valid. The receiving saturated tiles are nonadjacent for k>=3; their
P vertices and T vertices cause no extra occupied neighbor. The matching
edges have disjoint endpoints. This proves feasibility for the entire family.

The upper path still has excess +1 and no fork. In the band, the two end
tiles have h=s=1 and r=0; each other tile has h=2 and r=0. All have residual
degree zero. Thus

    Delta=1, sigma=2, rho(S)=0, R(S)=0.

There is **no residual compensation in the adjacent band**. Each of the k
remaining tiles in the third tile row is blank, isolated and has excess -2.
The full ledger is

    +1 from the corridor, 0 from the band, -2k from other components;
    |T|=10, |M|=4k+3, H=6k+12, q=1-2k < 0.

The smallest displayed member is k=3, a 6x10 rectangle with component excesses
1,0,0,0,-2,-2,-2 and q=-5. It refutes the rule “every filled corridor has at
least one unit of residual compensation in its immediate adjacent band.”
It does not refute the coefficient-one inequality or B.13's blank-band move.
It also shows that the sigma/2 term in (3) cannot be discarded.

## 8. A bent path: precise deficit and promotion constraints

On an 8x6 rectangle, encode a vertex (row,column) by 6*row+column. Take

    T = {3,5,8,24,33,35,36,43};
    M = {(9,10),(11,17),(16,22),(23,29),(25,26),(27,28),(31,37)}.

The positive residual component follows tiles 6,7,8,5,2: it turns from right
to up. Its four edges and capacity three give excess +1. Its three internal
tiles have capacities one and contain exactly one internal matching edge in
total, (16,22). Five isolated blank tiles each contribute -2, giving q=-9.
This is outside B.13 and outside the already proved length-two/three cases.

Delete (16,22), with endpoints (2,4),(3,4). Either (2,3) or (3,3) can be
promoted to T, preserving the objective and all constraints. These candidates
are in the same blank capacity-two tile. They cannot both be promoted: they
are adjacent and each already has an occupied neighbor, respectively (1,3)
and (4,3). The maximum compatible set among these two local candidates is
therefore exactly one. The edge cost is one, so this particular bend is
removable. It supplies no general bent-path theorem.

The witness was found with the existing length-four path search; its
coordinate feasibility and replacement are checked separately by the direct
coordinate checker. Its proof is the explicit neighbor count above, not an
inference from absence of counterexamples.

## 9. Verification and proposed manuscript addition

Run from the research repository root:

```sh
python3 develop/check_cross_component_compensation.py --output develop/results/cross-component-compensation-2026-09-30.json
```

The saved run passes 928 family/symmetry controls: k=2,...,40 for the sharp
and capacity-two families, and k=3,...,40 for the escaping-attachment family,
each in all eight square symmetries. It reconstructs residual components and
uses the existing prescribed-routing verifier and its five-sixths assertions.
The new geometric ledger is checked using independent coordinate counts.

All 59,787 B/T/P assignments with prescribed lower endpoints on widths 2,4,6
are examined; 3,653 satisfy the lemma's other hypotheses, and all have blank
surplus at least two. The existing feasible-pair enumerator also examines
12,752 ladder pairs, of which 579 satisfy the band conditions; their optimum
objectives are 1,3,5 respectively. These are finite controls of the written
proof, not substitutes for its arbitrary-length reasoning. Existing corridor
checks (320 symmetry images) and the three-edge classification control
(32 configurations, 17 symmetry classes) also pass unchanged. No Lean run or
new formalization is claimed.

**Proposed addition after joint review:** append Lemma 1, Theorem 2 and the
escaping-attachment example after Proposition B.13, with the sharp occupied
band as its equality example. The capacity-two repeated-visit example should
accompany any discussion of longer routed paths. Keep the current general
5/6 theorem and the open coefficient-one conjecture as stated. The arXiv source
package and its three manuscript inputs have not been edited in this worktree.

The next proof target is to pay the outward saturated-attachment term across
disjoint regions, while retaining the corner constraints at bends. General
bent paths without this filled frame and overlapping candidate bands remain
unresolved. Any extension must preserve (1) or give an equally explicit
injective resource allocation.

The [proper-interval Hall note](PROPER_INTERVAL_HALL.md) gives one conditional
route forward: for tile-disjoint, noncrossing single-bend connectors whose
candidate donors fill the interval between their endpoints, capacitated Hall
reduces to consecutive source blocks. The 8x6 shared-promotion witness and the
6x20 closed mixed successor show why the tile-disjointness and exact-interval
hypotheses must be checked rather than assumed.
