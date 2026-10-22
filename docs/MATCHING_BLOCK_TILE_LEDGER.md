# Matching-block tile accounting and exchange-terminal occupied bands

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. Setting and the new issue

Use a finite even-by-even rectangular grid with its fixed physical two-by-two
tiling. Let (T,M) be feasible, P=V(M), and A=T union P. Selected vertices
have at most one neighbor in A. Assume d_A(p)>=3 for every p in P.
Let C_i be the allowed-edge matching blocks of G[P], as defined in
`FLEXIBLE_BLOCK_ENTRY_REDUCTION.md`. Every matching restricts independently
to these blocks. A forced block has two vertices; every endpoint of a
larger, flexible block has at least two allowed neighbors in that block.

We first prove a tile geometry fact requiring only these assumptions.
For the nonpositivity and compensation statements also assume exchange
terminality, so every flexible endpoint has at most one T-neighbor by
the accepted two-selection square-unlocking lemma.

The distinction from the earlier module-fusion identity is substantive:
these are the actual matching blocks of an arbitrary induced endpoint
graph. No U/rotor decomposition, original support system, preservation
of original module degrees, or original-source labeling is assumed.
We never replace adjacent endpoints in other blocks by selected supports.

## 2. Every block intersects each endpoint tile in a connected set

**Block-tile connectivity lemma.** If C_i meets a physical tile Q, the
grid induced by C_i intersect Q is connected. The entire P intersect Q
is connected too. No intersection-splitting correction is needed.

Proof. A nonempty disconnected subset of a four-cycle consists of its
two diagonal corners. The entire endpoint set cannot have that form:
each other corner would be adjacent to both endpoints, so cannot be
selected and must be blank. Each endpoint would then have at most two
occupied neighbors outside Q, contradicting d_A>=3.

Now suppose one matching block C meets Q in exactly diagonal corners
a=(0,0) and d=(1,1). This block is flexible. Neither other corner
b=(0,1), c=(1,0) belongs to C. Thus the two allowed neighbors of a
must be its two exterior neighbors (-1,0),(0,-1), and both corresponding
edges are allowed. Likewise d has both exterior edges allowed.

If b is an endpoint, it is outside C and its matching mate cannot be
a or d. Its mate is either (-1,1) or (0,2), in b's own block. In the
first case independently combine that block matching with a C-matching
containing a--(-1,0). These two matched edges are opposite sides of
a unit square. Flipping it makes a--b allowed, contradicting b outside C.
In the second case use d--(1,2) and the other unit square, with the
same contradiction. A reflected argument excludes c as an endpoint.

Neither b nor c can be selected because each is adjacent to a,d.
Both must therefore be blank, again contradicting d_A(a)>=3. Hence
the diagonal intersection is impossible. Other nonempty subsets of
a four-cycle are connected. This proves the lemma. Missing exterior
grid sites cannot help: the required two allowed exterior edges would
then already be impossible. QED.

## 3. Actual-support block charges are all nonpositive

For every endpoint tile Q put t_Q=|T intersect Q| and d_Q=2-t_Q.
Let R_i be the physical tiles meeting C_i. Define the RAW BLOCK CHARGE
using the actual final selections, not hypothetical isolated supports:

    gamma_i = |C_i|/2 + sum_(Q in R_i)(t_Q-2).

These are integers. Although block endpoint sets are disjoint, their
tile receivers R_i may overlap. A selected count t_Q is deliberately
repeated here once per meeting block; Section 4 corrects it exactly.

**Nonpositive block-charge lemma.** Every gamma_i<=0 in an exchange-terminal
pair. For forced blocks this conclusion needs only feasibility.

For a flexible block write n=|C_i intersect Q|. Its local summand is
n/2+t_Q-2. If n=1, two selections in Q would have to be the two corners
adjacent to that endpoint: adjacent selections would already violate
feasibility, and these are the only nonadjacent two-corner choices in
the remaining three sites. This would give two T-neighbors to a flexible
endpoint, which is excluded. Thus t_Q<=1, and the summand is at most -1/2.
If n=2, feasibility gives t_Q<=1, and the summand is at most zero.
This holds whether the two endpoints are adjacent or diagonal; in the
diagonal case neither other corner could be selected. If n=3 or4,
every remaining corner touches at least two endpoints, so t_Q=0 and
the summand is again nonpositive. Summing proves the flexible case.

For a forced block C_i={p,q}, its two adjacent endpoints either occupy
one physical tile or two. In one tile the remaining corners are adjacent;
both cannot be selected, since each already touches an endpoint. Hence
t_Q<=1 and gamma_i=1+t_Q-2<=0.

For an edge crossing two tiles, use a rotation and reflection so p=(0,1),
q=(0,2), with tile rows0,1 and columns0,1 or2,3. The six remaining
sites can be paired as

    {(0,0),(1,0)}, {(1,1),(1,2)}, {(1,3),(0,3)}.

Each pair consists of adjacent vertices and at least one member already
has p or q as an occupied neighbor. Both members cannot be selected.
At most three of the six sites are selected, so

    gamma_i=1+t_left+t_right-4<=0.

No selection or degree hypothesis outside these tiles was added. QED.

Put B_i=-gamma_i>=0 and B=sum_i B_i. Flexible-block summands are
nonpositive tile by tile. A forced block can instead have a positive
half-unit at one endpoint tile, cancelled by its mate's tile. Thus a
forced block's nonnegative B_i must not be asserted tile by tile.

Another consequence is that every positive WHOLE-TILE charge
t_Q+|P intersect Q|/2-2 occurs at a singleton endpoint with two selections.
That endpoint belongs to a forced block. Flexible blocks introduce no
such positive singleton. This locates positive tiles; it is not an
allocation of their compensation.

## 4. Exact interface tax and full-square correction

Let R be all endpoint tiles, m_Q the number of matching blocks meeting Q,
and e_Q the number of P-edges in Q joining different matching blocks.
Let J count full endpoint tiles meeting at least two blocks. Define

    X=sum_(Q in R) (2-t_Q)e_Q.

Every edge is counted in its ONE physical tile. A tile with at least two
endpoints has t_Q<=1, so every interface edge carries weight one or two.
These are actual tile counts, not spare copies of donor capacity.

The total whole-receiver charge, summed over endpoint components, is

    rho=|P|/2+sum_(Q in R)(t_Q-2).

**Exact matching-block ledger.** Under the hypotheses of Section 1,

    rho = sum_i gamma_i + X - 2J.                    (1)

In particular, under exchange terminality,

    rho = X-2J-B,       B>=0.                       (2)

Proof. Both the whole P subset of a tile and each block intersection are
connected by Section 2. If the tile is not a mixed full square, contracting
the internal block intersections leaves a tree, so e_Q=m_Q-1. For a
mixed full square it leaves one cycle, so e_Q=m_Q. Parallel edges are
retained in this count, including the two edges between two block parts.
If all four endpoints belong to one block there is no interface and
m_Q=1. Thus in all cases

    e_Q=m_Q-1+I[Q is mixed and full].

Each mixed full tile has t_Q=0. Consequently

    sum_Q (m_Q-1)(2-t_Q)=X-2J.                       (3)

On the other hand block endpoints partition P, whereas t_Q-2 occurs
m_Q times in sum_i gamma_i and once in rho. Their exact difference
is the left side of (3). This proves (1), then Section 3 gives (2). QED.

Let D=sum_(Q outside R)(2-t_Q), the total actual deficit of endpoint-free
tiles. Feasibility gives t_Q<=2 even on those tiles, so D>=0. Counting
one half-area and one copy of the objective gives

    mn/2-|T|-|M| = D-rho = D+B+2J-X.                (4)

No donor has been assigned or used twice: D counts each endpoint-free
tile once; B_i belongs to one matching block; each intratile interface
edge enters X once; and each mixed full tile enters J once. These are
terms in one conservation identity, not independent benefits that can
be spent again after applying (4).

**Concrete sufficient classes.** Exchange-terminal pairs with X<=D+2J
satisfy the coefficient-one half-area bound, with additional margin at
least B. In particular, if every endpoint tile meets just one matching
block, then X=J=0 and the exact margin is D+B. On these specified classes
the matching coefficient increases from the existing5/6 to1. No claim
is made that the stated physical condition holds on every grid pair.
The unrestricted missing inequality is precisely X<=D+B+2J.

## 5. An explicit obstruction to ignoring shared block receivers

Use the previously proved positive nonunique graft with w=6,h=4 in
`EXCHANGE_TERMINAL_NONUNIQUE_MATCHINGS.md`. The constructor
`graft(6,4)` gives32endpoints,15selections and16matching edges on a
14-by20board. Five forced core pairs and the unique nine-edge elbow
matching leave one flexible square; the sole bridge belongs to no
perfect matching. Thus there are14forced blocks and one flexible block.
The existing proof freezes both matchings, including mixed bundles.

Its independently reconstructed block charges and interfaces are

    sum_i gamma_i=-21,   X=28,   J=3,
    rho=-21+28-6=1.

The raw flexible charge is -5 and every forced-block charge is at most
zero. Hence the rule "all raw block charges are nonpositive, so their
union has nonpositive charge" fails on an actual exchange-terminal
positive receiver. The omitted overlap correction is22. This failure
already occurs for unique-matching elbows; the graft shows that retaining
the flexible block and counting its entries does not repair that omission.

This is a counterexample to BLOCK ADDITIVITY / OMITTED INTERFACE TAX,
not to the target half-area inequality. The established capped elbow
donor has canonical capacity2, or guaranteed capacity at least1 under
the specified terminal exteriors, and pays the one-unit demand once.
The new decomposition does not generate another copy of that donor.

## 6. Occupied adjacent bands are exchange-terminal for every width

Take the previously constructed occupied bands: U=two_leg_case(w,4,4)
and H(U), where H(r,c)=(4-r,c-w), even w>=6. Keep the original matchings
and consume the mutual selected supports. The prior all-width proof
establishes feasibility, degree at least three, and complete fixed-matching
freezing. Here we establish uniqueness of the endpoint matching, which
upgrades that conclusion to exchange terminality.

All endpoint contacts between the two sources lie on the five rungs
(r,0)--(r,1), 0<=r<=4. First remove these forced pairs in U's free arm:

    (4,w)--(3,w), (2,w)--(1,w),
    (r,c)--(r,c-1), c=w,w-1,...,2,
    where r=0 for even c and r=1 for odd c.

At each step the first named endpoint has exactly one neighbor in the
remaining endpoint graph. The two leg removals initiate the usual
alternating bar wave. It ends by removing (0,2)--(0,1).

Independently remove H-images of the free-left-arm pairs

    (4,1)--(3,1), (2,1)--(1,1),
    (r,c)--(r,c+1), c=1,2,...,w-1,
    where r=0 for odd c and r=1 for even c.

These are again degree-one forced pairs, ending with the H-image of
(0,w-1)--(0,w), which removes the seam endpoint (4,0).
The unshifted endpoint profile is

    rows0,1: {1-w} union [0,w],
    row2:    {1-w,0,1,w},
    rows3,4: [1-w,1] union {w}.

It shows that there are no other contacts or unremoved exterior vertices.
The remaining seam is the five-rung ladder with (0,1),(4,0) removed.
Its matching is forced successively by

    (0,0)--(1,0), (1,1)--(2,1),
    (2,0)--(3,0), (3,1)--(4,1).

Every step removes a leaf and its sole neighbor; all4w+12endpoints are
covered. There is therefore exactly one perfect matching, equal to the
actual one. Together with the prior complete freezing certificate this
proves exchange terminality for every even w>=6. No finite matching
enumeration substitutes for this forcing argument.

### Exact block ledger of the band family

Every matching block is a forced pair. Use unshifted tile indices, so
Q_(r,k)={2r,2r+1} times {2k,2k+1}. The endpoint profile and actual
matching give the following full inventory; intervals of k are inclusive.

| (endpoint count,t_Q,m_Q,e_Q) | Physical tiles | Number |
|---|---|---|
| (1,1,1,0) | (2,-w/2) | 1 |
| (1,2,1,0) | (2,w/2) | 1 |
| (2,0,1,0) | (1,k), -w/2+1<=k<=-1 | w/2-1 |
| (2,0,2,1) | (2,k), -w/2+1<=k<=-1 | w/2-1 |
| (2,1,1,0) | (0,-w/2),(1,-w/2) | 2 |
| (2,1,2,1) | (0,w/2),(1,w/2),(2,0) | 3 |
| (4,0,3,3) | (0,k),0<=k<=w/2-1; and (1,0) | w/2+1 |

The union of these lists is precisely all endpoint tiles. The original
selected support formulas give the listed t_Q; the two bar parity
patterns give the matching-block multiplicities. Thus the table is an
all-width coordinate count, not an extrapolated fit.

For each row, the sum of raw block charges within its tile is
n_Q/2+m_Q(t_Q-2). Substituting the table yields

    B=4w+3,  X=4w+7,  J=w/2+1,
    rho=X-2J-B=2-w.

After the even translation (2,w), the board is8-by-(2w+2), with
T=14 and M=2w+6. The exact endpoint-free deficit is D=5w-10, and (4)
gives the known exact total margin6w-12. This is a second derivation of
the prior charge and margin using actual matching blocks. The new result
is its all-matching terminality and its interface-resolved block ledger;
the prior degree-four module ledger and charge are not claimed anew.

## 7. Verification and limitations

The checker reconstructs blocks from the union of all perfect matchings
on bounded fixtures, verifies tile intersections and the exact ledger,
and supplies deliberately nonterminal controls. It separately checks
the all-width band forcing certificate, complete freezing transcript and
every inventory position in a stated finite width range. Formal checks
cover local finite tile inequalities, the tile contraction identity and
the ledger arithmetic; the general matching/square geometry, freezing
adapter and all-width band forcing remain written proofs.

The completed Python run passes1295models/6046matchings,19102block-tile
connectivity checks and74separated-block cases. Controls include the
complete1086model3-by4endpoint-box domain,64fixture symmetry images,
96occupied-band phase/symmetry images, and48band widths6through100,
with5376degree-one forced matching edges checked. Reproduce it with

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_matching_block_tile_ledger.py --output output/matching-block-tile-ledger-validation.json

Local Lean4.33.0 passes9theorems with9individual axiom audits, ordinary
axioms only, no warnings/errors/sorry/native evaluation. The source is
`formal/SubQuorum/MatchingBlockTileLedger.lean`; the exact source hash,
preflight and execution receipt are in
`output/matching-block-tile-ledger-formal-check.json`. This formal scope
does not include the general matching-block geometry or all-width
forcing proof. The prior entry reduction has a separate accepted review
in `output/flexible-block-entry-review-accepted.json`.

This gives an explicit obstacle to independent block payment and a usable
physical interface formula. It does not prove the remaining inequality
X<=D+B+2J for arbitrary exchange-terminal grids. Entry counts alone do
not provide that inequality. General equality and a global improvement
of5/6 remain open; the submitted manuscript is unchanged.
