# Terminal strands: exact compensation without reusing tile capacity

7 October 2026. This continues [residual-cycle pruning](RESIDUAL_CYCLE_PRUNING.md)
and [exterior-component budgets](EXTERIOR_COMPONENT_BUDGETS.md). We reduce any
deficient region, including capacity-two branching and diagonal passages, to
disjoint physical matching strands and unused-slot reserves. This gives an
exact integer shortage formula and completely describes neutral receivers.
It does not establish a universal supply of compensation.

## 1. Pairing residual endpoints inside a tile

Fix a feasible pair on an even-by-even rectangle and a tile region D containing
only deficient tiles. Degrees d include residual matching edges leaving D.
As before r is residual capacity, rho=d/2-r, p counts residual boundary
edges, a counts active zero-capacity leaves, and H=sum_{r>0}(2r-d).

In each tile pair as many of its residual matching endpoints as possible
using disjoint adjacent corner pairs. These are auxiliary pairs, not yet
changes to the matching. Let u_Q be the number of unpaired endpoints in a
positive-capacity tile, and H_Q=2r_Q-d_Q. The possibilities are:

| r | d | Endpoint geometry | u_Q | H_Q | c_Q=(H_Q-u_Q)/2 |
|---|---|---|---|---|---|
| 1 | 0 | empty | 0 | 2 | 1 |
| 1 | 1 | one corner | 1 | 1 | 0 |
| 1 | 2 | adjacent, by the capacity-one passage lemma | 0 | 0 | 0 |
| 2 | 0 | empty | 0 | 4 | 2 |
| 2 | 1 | one corner | 1 | 3 | 1 |
| 2 | 2 | adjacent | 0 | 2 | 1 |
| 2 | 2 | diagonal | 2 | 2 | 0 |
| 2 | 3 | three corners | 1 | 1 | 0 |
| 2 | 4 | all four corners | 0 | 0 | 0 |

A capacity-zero tile has d=0 or 1; in the latter case its sole endpoint is
an active positive leaf. Each table row follows from the four-cycle of tile
corners; capacity-one degree two uses the previously proved adjacency lemma.
Thus u_Q<=H_Q and H_Q-u_Q is nonnegative even. Write u=sum u_Q and
c=sum c_Q, so H=u+2c. A deterministic tie choice suffices, but no uniqueness
of the resulting strands is claimed. Reserves are accounting tokens; c_Q
does not assert that another feasible matching edge can be inserted there.

## 2. A physical strand decomposition

Take every residual matching edge with at least one endpoint tile in D,
and add the auxiliary within-tile pairs. Regard their physical endpoint
vertices as graph vertices. Each has one matching edge and at most one
auxiliary pair. Every component is consequently an alternating path or
alternating cycle. Matching endpoints are distinct, so components share no
physical vertex or edge, even if several strands visit the same tile.

Path endpoints have exactly three types:

* L: an unpaired endpoint in an active zero-capacity tile;
* S: an unpaired endpoint in a positive-capacity tile;
* P: the outside endpoint of a boundary residual matching edge.

There are exactly a L ends, u S ends and p P ends. A path may consist of a
single matching edge; no minimum-length assumption is used. Let n_XY count
paths with endpoint types X,Y, without orientation. Then

    a = 2n_LL+n_LP+n_LS,
    p = 2n_PP+n_LP+n_PS,
    u = 2n_SS+n_LS+n_PS.                                (1)

**Theorem 1 (exact strand shortage).** For every such region,

    epsilon(D)=p/2+rho(D)
              =n_LL+n_LP+n_PP-n_SS-c.                  (2)

In particular D pays all its p half-unit port demands exactly when

    n_LL+n_LP+n_PP <= n_SS+c.                           (3)

**Proof.** The prior terminal identity gives 2rho=a-H, and H=u+2c.
Subtract the third equation of (1) from the sum of the first two, then
divide by two. This proves (2) and the equivalent criterion (3). QED.

The individual contributions are transparent:

| Strand | rho contribution | epsilon contribution |
|---|---|---|
| LL | +1 | +1 |
| LP | +1/2 | +1 |
| PP | 0 | +1 |
| LS | 0 | 0 |
| PS | -1/2 | 0 |
| SS | -1 | -1 |
| Each unused-slot reserve c_Q unit | -1 | -1 |
| Alternating cycle | 0 | 0 |

These are ledger contributions, not charges of tile-disjoint subregions.
At a shared capacity-two tile each S endpoint uses one distinct token among
H_Q, and the remaining tokens form c_Q pairs. L endpoints occur once and
boundary matching edges occur once. An SS strand and a reserve cannot claim
the same token, and a strand cannot be claimed again through another route
name. This is a single-use decomposition for the entire region.

For the previous disjoint source patches, with every residual crossing an
actual marked lower export into the deficient remainder, applying (2) to
each maximal incident exterior component gives

    q <= sum_i tau_i
         +sum_j(n_LL,j+n_LP,j+n_PP,j-n_SS,j-c_j)
         +rho(W_0).                                    (4)

Thus the exact geometric task is to pay LL, LP and PP strands with distinct
SS strands or reserve units, plus any explicit remainder budget. This is
an exact refinement of the old component balance, not another budget added
to it. Equation (4) retains the earlier source-patch geometry and width-six
local lemma. Saturated attachments remain absorbed in tile capacities;
tau exports and inter-patch edges still require separate treatment.

## 3. Whole-grid and neutral-region consequences

Let D contain every deficient tile. Then p=0, every matching edge between
deficient tiles is included, and saturated tiles have charge zero. Equation
(2) becomes the general identity

    |T|+|M|-|V|/2 = n_LL-n_SS-c.                         (5)

This includes capacity-two junctions, repeated tile visits, bent paths and
diagonal passages. The coefficient-one grid target is therefore equivalent
to the single-use inequality n_LL<=n_SS+c for this decomposition. The
identity does not prove that inequality. Existing degree-two path arguments
extend as an exact decomposition; their global source-to-donor geometry
remains a separate research problem.

**Corollary 2 (neutral regions are port conduits).** Suppose every tile of
D has rho=0. Then a=H=u=c=0. Every strand is PP or a cycle, p is even,
and n_PP=p/2. There are equally many black and white inside boundary
endpoints in the physical checkerboard coloring, and each PP strand pairs
one of each. Such a receiver has rho=0 and epsilon=p/2; it supplies no
net negative budget, whatever its capacity-two junctions or internal cycles.

**Proof.** A zero-capacity positive leaf has charge +1/2 and cannot occur.
A positive-capacity neutral tile has d=2r, so H_Q=0. The table gives a
perfect adjacent pairing of its residual endpoints. All path ends are P.
Every pair in a tile joins black to white. Each strand begins and ends
with a matching edge, hence has odd physical length; its outside endpoints
have opposite colors, as do its two inside boundary endpoints. QED.

**Corollary 3 (closed neutral regions can be completely pruned).** If the
neutral region also has p=0, every residual edge belongs to an alternating
cycle. Replace all these cycles by their auxiliary pairs. The selected set,
every occupied vertex, objective, tile charges, saturation and saturated
attachment mates stay fixed; all residual edges incident to D disappear.
Each tile ends with r=d=0. No assumption excludes capacity-two tiles,
diagonal residual cycles or repeated visits to a tile.

**Proof.** With no path ends the strand graph consists entirely of cycles.
The cycle replacement is the earlier alternating-circuit theorem. All
cycles are disjoint in physical endpoints, so replacements may be simultaneous.
Each tile gains d_Q/2=r_Q internal edges and loses all d_Q incidences. QED.

An irreducible closed residual component with no positive leaf and at least
one residual edge must therefore have rho<=-1. Indeed rho<=0 is integer;
equality would make every tile neutral, since each leaf-free tile has
nonpositive charge, and Corollary 3 would provide a cancellation. Neutral
isolated tiles with r=d=0 are harmless and explicitly excluded by the edge
condition.

## 4. Checked sharp cases and scope

The arbitrary-length bent two-port capacity-one receiver has one PP strand,
rho=0 and epsilon=1. Removing its first internal matching edge produces one
reserve unit c=1 and pays both ports exactly. A corridor containing one
source leaf and omitting the other has one LP strand, rho=+1/2 and epsilon=1;
including both leaves gives one LL strand. These explain two different
unpaid demands without inferring a target counterexample.

The irreducible four-tile ring has four S ends at its two diagonal
capacity-two tiles, two SS strands and c=0, giving rho=epsilon=-2. Its
budget is already the SS budget; counting those capacity-two tiles again
would spend it twice. The neutral figure-eight through one capacity-two
tile has only cycles and can be erased completely. Its one-port variation
has one PS strand and rho=-1/2. All coordinates are in the linked verifier.

The earlier normalized 8-by-(6b+14) equality family has precisely one LL
strand, b LS strands, no SS strand and one reserve unit, for every b>=1
and its capacity-two source flip. The source component has two L ends and
no S end, hence exactly one LL strand; each separate E/partner component
has one L and one S end; the isolated J tile has r=1,d=0 and contributes
the single reserve. All other components are closed neutral and contribute
only cycles. Thus (5) gives q=1-0-1=0 directly, with each budget owned once.
This uses the previously proved component construction for all b, rather
than extrapolating the finite controls.

The next nontrivial proof obligation is an injective or capacitated allocation
of the LL/LP/PP debt to SS paths and reserves under actual source geometry.
This note provides the exact resources and ownership, not a universal
allocation theorem or an improvement of the unrestricted 5/6 bound.
The focused manuscript is preserved and no new Lean theorem is claimed.

Run `python3 develop/check_terminal_strands.py --output output/terminal-strand-controls.json`.
Finite controls verify the decomposition, terminal-type counts, all local
choices, simultaneous cycle pruning and fixed boundary matching. The
general proof is the local table and degree-two strand argument above.
