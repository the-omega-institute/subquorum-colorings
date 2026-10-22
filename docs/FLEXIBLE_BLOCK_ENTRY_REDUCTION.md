# Forced boundary edges and degree-four entries into flexible matching blocks

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. Setting and conclusions

Work on a finite induced rectangular nearest-neighbor grid. Let T be the
selected vertices, P the endpoints of a matching, and A=T union P, with
T and P disjoint. Feasibility means every vertex of T has at most one
neighbor in A. Assume every p in P has occupied degree d_A(p)>=3.
An edge of H=G[P] is allowed if some perfect matching of H contains it.
The connected components of the allowed-edge graph are matching blocks.
A two-vertex block is a forced edge; a larger block is flexible.

Exchange terminality means that for every perfect matching N of H, no
nonempty promotion bundle is feasible. A bundle promotes one endpoint
of each chosen matching edge and deletes its mate; every promoted
endpoint must have at most one remaining occupied neighbor.

We prove the following structural reduction.

1. A flexible endpoint with two selected neighbors permits a replacement
   matching and a feasible bundle of exactly two promoted endpoints.
2. In an exchange-terminal pair, every source and sink of the directed
   matching-block graph is a forced edge. Every nonempty endpoint
   component consequently has a P-leaf in each checkerboard color.
3. For every flexible block and each checkerboard color, the first
   endpoint of that color frozen in that block has occupied degree four,
   exactly two neighbors inside the block and exactly two already
   persistent neighbors outside. At least one outside neighbor is in P.
4. If there are f flexible blocks and j occupied-degree-four endpoints,
   then 2f<=j. The two entry endpoints of each block are distinct, and
   entries belonging to different blocks are distinct.

This is a reduction for arbitrary feasible exchange-terminal grid pairs,
not only the previously parameterized source families. It supplies no
donor deficit or improvement of the global 5/6 bound by itself.

The two-selection lemma, forced-source/sink reduction and first-global-
entry observation were suggested by the structural Oracle response
archived in `output/exchange-terminal-uniqueness-research-response.json`.
Here their hypotheses and proofs are made explicit, and the entry
argument is applied separately to every block, giving the bound 2f<=j.
That response did not settle uniqueness; the separate nonunique positive
receiver construction already disproves uniqueness.

## 2. Matching facts and independent restrictions

Fix a perfect matching N={b_i w_i}, with b_i black and w_i white.
Contract its edges and orient each nonmatching edge b_i--w_j as i->j.
A nonmatching edge is allowed exactly when its arc lies on a directed
cycle. A cycle expands to an alternating cycle and can be flipped;
conversely the symmetric difference with a matching using that edge
contains an alternating cycle through it.

The strongly connected components, with their matched pairs restored,
are exactly the matching blocks. In particular every H-edge internal
to a block is allowed, every matching restricts to a perfect matching
on each block, and restrictions on different blocks can be combined
independently. Each endpoint of a flexible block has at least two
allowed neighbors: its contracted vertex has both an incoming and an
outgoing arc inside its nontrivial strongly connected component.

Orient an edge between distinct blocks from its black endpoint's block
to its white endpoint's block. This condensation is acyclic. Independence
of matching choices is used only between distinct blocks, never to
assert arbitrary compatibility of two allowed edges within one block.

## 3. Two selections unlock an alternating square

Suppose p is flexible and has at least two neighbors in T. It has at
least two allowed P-neighbors, so the grid degree bound forces exactly
two P-neighbors and two T-neighbors.

The P-neighbors cannot be opposite. Otherwise the T-neighbors are
opposite too, and feasibility forces both transverse neighbors of
either P-neighbor to be blank. That P-neighbor would have occupied
degree at most two, a contradiction.

Apply a translation and grid symmetry so that

    p=(0,0), q=(1,0), r=(0,1) are in P,
    (-1,0),(0,-1) are in T.

Feasibility forces (1,-1),(-1,1) to be blank. Since q and r have
occupied degree at least three, all their remaining neighbors are
occupied. Thus

    s=(1,1), v=(2,0), w=(0,2) are occupied,
    d_A(q)=d_A(r)=3.

The vertex s is in P because it is adjacent to both q and r and hence
cannot be selected. The edges pq and pr are allowed: p is flexible
and these are its only P-neighbors. Let C be their common block.

We claim s belongs to C. If not, qs and rs are disallowed. Flexibility
of q forces v in P and qv allowed, and flexibility of r forces w in P
and rw allowed. In any perfect matching s is matched to u=(2,1) or
z=(1,2), since it cannot be matched to q or r. If matched to u, combine
that matching's restriction outside C with a C-matching containing qv.
The two edges qv,su form opposite sides of a unit square. Flip it to
obtain a matching containing qs, a contradiction. If s is matched to z,
combine instead with a C-matching containing rw and flip the other
square to obtain rs, again a contradiction. Thus s belongs to C.

The internal edge qs is allowed. A matching containing qs must also
contain pr, since p has no other available P-neighbor. Promote q and r,
deleting s and p. Each promoted endpoint had occupied degree three
and loses exactly two neighbors, so each retains one. Old selections
retain their former occupied neighbors or lose some, and no occupied
vertex is added. This is a feasible two-endpoint bundle. QED.

Consequently, every flexible endpoint in an exchange-terminal pair
has at most one selected neighbor.

## 4. Forced source and sink edges

Let C be a source of the condensation. Every P-neighbor of a white
endpoint of C lies in C, by the orientation convention. If C were
flexible, every white endpoint would have at most one T-neighbor by
Section 3. Promote all white endpoints of C and delete all their
black mates. Every adjacent endpoint is deleted and at most one
selected neighbor remains, giving a nonempty feasible bundle.
Thus C is a forced edge, and its white endpoint is a P-leaf.

Reverse colors to show that every sink is a forced edge whose black
endpoint is a P-leaf. The finite condensation of every nonempty H
component has a source and a sink, proving the two-color leaf claim.

For completeness the leaf geometry is also forced. A P-leaf has one
P-neighbor and at least two T-neighbors. Two opposite T-neighbors
would force its mate to have occupied degree at most two, as in
Section 3. Three T-neighbors include an opposite pair and are also
impossible. Hence a P-leaf has exactly two perpendicular T-neighbors
and occupied degree three. One transverse selection forces a blank
neighbor of its mate, whose occupied degree is therefore exactly three.

## 5. Exact freezing and the first entry of each block

Fix a matching N and one color c. Starting with E empty, freeze a
c-colored endpoint x when at least two of its neighbors lie in

    T union N(E).

Frozen endpoints cannot be promoted in any c-colored feasible bundle:
inductively their two witnesses cannot both be deleted by such a
bundle. At the fixed point the remaining c-colored endpoints S form
a feasible promotion bundle if nonempty. Indeed, deleting N(S) leaves
as occupied neighbors precisely those in T union N(E), and every
remaining endpoint has at most one such neighbor.

A mixed-color feasible bundle contains a feasible monochromatic
sub-bundle. Keeping only the promoted endpoints of one color restores
deleted vertices of that same color; these cannot be their neighbors
in a bipartite graph. Therefore absence of bundles is equivalent to
complete freezing in both colors. Exchange terminality implies this
for every replacement matching N.

Let C be any flexible block, and let x be the first c-colored endpoint
of C frozen in a sequential order. Every matching mate of a previously
frozen endpoint belongs to that endpoint's block. No internal neighbor
of x is therefore persistent yet: its mate would be an earlier frozen
c-colored endpoint of C. All freezing witnesses for x lie outside C.

Flexibility gives at least two internal neighbors. Freezing gives at
least two outside persistent neighbors. The grid degree bound implies
there are exactly two of each and d_A(x)=4. Section 3 excludes two
selected witnesses, so at least one outside witness is an endpoint.
For a black x this gives an outgoing condensation edge; for a white x
it gives an incoming edge.

This proves the assertion for every block and either color, under any
matching and any valid sequential freezing order. Choosing these two
entries in each flexible block gives 2f distinct degree-four endpoints,
so 2f<=j. In particular if every endpoint has occupied degree three,
there are no flexible blocks and the matching is unique, recovering
the earlier degree-three theorem under exchange terminality.

For the first flexible entry globally in a fixed color, all earlier
endpoints are forced. Its outside witnesses are thus either one
selection and one forced-edge endpoint, or two forced-edge endpoints.
Later block entries may instead use persistent flexible endpoints
from other blocks; the word "forced" cannot be propagated to them.

## 6. Resource accounting and the next missing step

The entry injection counts distinct physical endpoints, not donor
capacity. If a fixed two-by-two tiling has k tiles containing the
degree-four endpoints, the elementary bound j<=4k gives f<=2k.
Such tiles can contain endpoints of several matching blocks of the
same whole endpoint component. This bound is not a payment assignment.

Even selecting one external endpoint witness for each entry gives
only 2f edge incidences. A cross-block edge can be selected at its
black endpoint for one block and at its white endpoint for another.
It has at most two such entry incidences, not necessarily one. Nor
does a forced matching edge or its use in a freezing transcript imply
a distinct empty physical tile.

The accepted nonunique positive graft has one flexible square block,
both-color degree-four entries, and charge one. Its existing capped
donor pays that charge once, independently of the two matching choices.
The new reduction does not spend that donor again. A compensation
proof still needs an exact physical-tile ledger across forced edges
and flexible blocks, with overlap and consumption terms. Unrestricted
compensation, the general-grid equality and a new global coefficient
remain open. The submitted manuscript is unchanged.

## 7. Verification scope

`develop/check_flexible_block_entries.py` independently reconstructs
allowed blocks by taking the union of enumerated perfect matchings.
It checks the two-selection bundle conclusion, source/sink leaves,
all first-entry conditions and the disjoint endpoint count. Controls
include a deliberately unlockable selected-corner rectangle, the
fixed-matching charge-two obstruction (which is not exchange-terminal),
the exchange-terminal nonunique core, its positive grafts and elbow
controls, with all eight grid symmetries. A stated small endpoint-box
domain is also exhausted. Enumeration is validation of these written
general proofs, not their substitute. This note has not yet received
a separate Oracle review or Lean formalization.
