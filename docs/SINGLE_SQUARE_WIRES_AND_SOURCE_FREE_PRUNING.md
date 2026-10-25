# Capacity-two square wires and source-free single-square components

25 October 2026. Wenlin Zhang and Haobo Ma. Isolated research branch.

The abstract [relay rectangle criterion](RELAY_BYPASS_RECTANGLES_AND_EXACT_LOCAL_COST.md)
requires a genuine common-output route module. Here we settle a specific
geometric interface instead: an all-P capacity-two tile is locally two fixed
wires, and those wires can even belong to ONE original mixed owner. We give
an actual completely frozen example of that obstruction. For the entire
previously classified aligned single-square class we prove an exact routing
decomposition, including all arm lengths and all seven central matchings.

The original selected set, actual matching, band partition, resource identities
and submitted manuscript are preserved. No universal 5/6 improvement follows.

## 1. A full capacity-two tile is a pairing, not a switch

Use original aligned two-row bands and the PP/M strand decomposition. A PP
column joins its two endpoints by an auxiliary within-band vertical edge;
each endpoint also has its one actual M edge. Parallel actual and auxiliary
edges are kept distinct. Strand components are paths or alternating cycles.

Let a fixed aligned tile Q contain four P, all actually matched outside Q.
Denote its corners NW,NE,SE,SW, and the four distinct outside actual mates
by w_NW,w_NE,w_SE,w_SW. Restricted to Q and its actual half-edges, the only
strand connections are

    w_NW --M-- NW --PP-- SW --M-- w_SW,
    w_NE --M-- NE --PP-- SE --M-- w_SE.                  (1)

**Wire lemma.** These are two fixed column pairings. A path restricted to
this local interface cannot connect different columns. The presence of the
horizontal P adjacencies NW--NE and SW--SE does not change (1): those are
neither actual M edges nor auxiliary PP edges, and none of these four P is
a TP or BP terminal eligible for an extra terminal link.

This follows directly from the two matchings defining the original strands.
If the tile has no saturated attachments, its residual ledger has r=2,d=4,
charge zero. Those scalar counts do not authorize an all-to-all capacity-two
router. Also, the exterior may reconnect the two local wires into the SAME
original owner, so local wire disjointness does not imply owner disjointness.

## 2. Actual frozen same-owner obstruction

Use the existing fixture
`develop/fixtures/frozen_mixed_cycle_square_switch.json`: a 28-by-24 board
with 308 endpoints and 49 selected vertices, independently fully frozen.
Tile (5,8), physical rows 10,11 and columns 16,17, has all four P and

    t=h=s=0, r=2, d=4, rho=0.

Both of its PP columns belong to the SAME mixed owner G, with original ends
BP(5,18), TP(12,14). Its actual PP/M trace, in (band,column) coordinates, is

    (2,18),(3,18),(4,18),(5,18),(6,18),(6,17),(5,17),
    (4,17),(4,16),(5,16),(5,15),(5,14),(6,14).           (2)

In particular both (5,16) and (5,17) occur in this one original path.
Two different original alpha owners have tips (5,17) and (5,19) linking
to G's BP(5,18). Their other ends are (5,6) and (24,19); both whole-source
supports are empty. G supports distinct original units (band5,col10) and
(band5,col12), among other original units.

Restrict the proposed local compensation certificate to these two sources,
G, their two actual entrance links and those two original units. Its exact
payment is one, minimum link cost one: G is one original mixed owner and
its single BP can occur in only one selected terminal link. Independent
terminal enumeration checks all three link matchings. Replacing G by a
capacity-two common-output module would incorrectly pay both.

This is a frozen geometric obstruction to that TILE-TO-RELAY ADAPTER, with
two different resource identities. It does not refute the rectangle theorem,
whose internal capacity hypothesis is violated, or the grid target. The
COMPLETE original board pays all four alphas at minimum cost two: two keep
direct units and the two displayed sources use different actual beta exits.
The verifier retains and checks those full-board certificates as well.

## 3. Exact routing classification of aligned single-square components

Assume the hypotheses of the [single-square parity theorem](SINGLE_SQUARE_PARITY_AND_ALIGNMENT.md):
a feasible original pair, every P has occupied degree at least three, one
endpoint component H containing exactly one P-square Q, aligned with the
fixed tiling. That theorem gives four straight pinwheel arms with lengths
l_N,l_E,l_S,l_W>=0, alternating forced perpendicular supports and an axial
selected support at each tip (or at the corner of a zero arm). The two
pinwheel orientations are permitted. Put

    a_i=floor(l_i/2), epsilon_i=l_i mod 2,
    o=sum_i epsilon_i in {0,2,4}.

The odd corners are precisely those matched outside Q; for o=2 they are
adjacent. Thus exactly o/2 odd arms are horizontal and o/2 are vertical.
Let v_Q,h_Q be the numbers of vertical/horizontal M edges internal to Q.
Set z_Q=v_Q+1_{h_Q=2}.

**Theorem 2 (source-free routing decomposition).** The original PP/M
components in H have no alpha and no beta. Their open mixed owners all have
horizontally actually matched BP. After deleting self terminal links, their
routing graph is the disjoint union of the two horizontal-arm chains, of
respective lengths

    L_E=a_E+epsilon_E, L_W=a_W+epsilon_W,                (3)

omitting chains of length zero. Consequently

    gamma=a_E+a_W+o/2,
    nonself links=max(L_E-1,0)+max(L_W-1,0),
    self links=a_E+a_W,
    PP/M cycles=a_N*1_{epsilon_N=0}
               +a_S*1_{epsilon_S=0}+z_Q.               (4)

Every mixed owner in this component is alpha-unreachable in the COMPLETE
original network, for arbitrary feasible exterior under the hypotheses.
In a fully frozen board o=2 or4; the decomposition also covers the removable
o=0 patterns, without calling those patterns frozen.

### Proof of the arm interfaces

Normalize Q to rows 0,1, columns 0,1, with north arm at NW, east at NE,
south at SE, west at SW. Reflection gives the other pinwheel orientation.
On each horizontal arm p_1,...,p_l the forced band labels alternate BP,TP,
BP,TP,... . On a vertical arm the vertices pair into PP columns, except
that an odd arm ends at one TP. These facts use the fixed original band
partition and the alternating forced supports; no new matching is chosen.

If a horizontal arm is even, actual pairs p_1--p_2,p_3--p_4,... are a_i
short mixed owners, each BP horizontally matched. Nonself links point
outward along the resulting chain. Its first BP is adjacent inward to a
central PP vertex, not to a terminal, so it has no extra entrance; its last
TP sees the axial T and its own BP, so has no further nonself exit.

If a horizontal arm is odd, corner--p_1 is an actual edge and p_2--p_3,...
give a_i short mixed owners. Nonself links point inward, ending at the
central mixed owner containing BP p_1. Its BP is also horizontally matched.
The outermost BP has only its actual TP mate and axial T horizontally, so
has no additional entrance. Each short owner contributes one self link;
the central long owner contributes none.

If a vertical arm is even, its a_i actual pairs are also its PP pairs,
giving a_i parallel-edge PP/M cycles. If odd, it is one continuous alternating
strand from its central corner to a TP tip. That TP has a perpendicular T
and an axial T, so neither horizontal neighbor is a different P terminal.
It has no outgoing terminal link. These exhaust every arm point and link.

### Proof of the central interfaces and exhaustion

Combine the two auxiliary vertical edges in Q with its internal actual M
edges. With o=4 there are no internal M edges; (1) pairs each horizontal
odd-arm BP to a vertical odd-arm TP, producing two distinct long mixed
owners. With o=2 the remaining internal M edge leaves exactly one open
central strand, again between a horizontal odd arm and a vertical odd arm.
If that internal M edge is vertical it additionally forms one isolated
parallel-edge cycle; if horizontal there is no central cycle.

With o=0, two horizontal internal M edges form one alternating square cycle,
or two vertical internal M edges form two parallel-edge cycles. There is no
open central strand. Thus z_Q counts exactly the central cycles in all
seven patterns. The horizontal chains exhaust every open owner, proving
(3)--(4), with no alpha, beta, branch or directed nonself cycle.

Every actual M edge, PP auxiliary edge and physical terminal link joins
adjacent P. Hence each stays in one original endpoint component. An exterior
alpha cannot enter H; an alpha inside H does not exist by the classification.
This proves complete-network unreachability, without a freezing-rank or
finite-size extrapolation. The same observation proves the conclusion in
an arbitrary feasible exterior, not only blank padding. QED.

## 4. Exact pruning, but original resource identities must remain

**Corollary 3.** Remove the mixed gate vertices and their incident route
arcs belonging to any collection of these endpoint components. Keep every
other original owner, whole beta, interval identity and support incidence
of the retained owners. For every available original unit subset Q_avail,
maximum payment AND minimum cost at that payment are unchanged in the
complete whole-support fork network.

Every paying path starts at an alpha and cannot visit a removed owner.
Both arms of a beta fork start at alphas as well, and no removed component
contains a beta. Hence every original paying primitive already avoids the
removed owners. The reduced primitives are the same paying primitives,
with the same original units, owner conflicts and costs. The converse is
immediate by inclusion. This proves equality, not just a lower bound.
Original PP/M cycles were never source or sink vertices of that network.

This is a network simplification, not physical endpoint deletion. The
receiver's original charge remains -o/2 by the earlier geometric theorem;
its tiles and forced supports remain on the original board. Neither the
negative charge nor the number of wires creates new interval units.

**Shared-resource obstruction to over-pruning.** For every even C>=10 take
the four length-one odd arms of the earlier constructor, with central Q at
rows4,5 and columns4,5. Add the actual alpha edge (3,C)--(4,C) and selections
(2,C),(5,C),(3,C+1),(4,C-1), in a 10-by-(C+6) rectangle. Keep all original
square selections and matching edges. There are no extra occupied contacts
between the two endpoint components. Each added endpoint has two selected
neighbors, so both it and the earlier square component are fully frozen.

In band1 (rows2,3), the endpoint-free gap columns5,...,C-1 lies between the
square owner's TP(3,4) and the added alpha TP(3,C). Its only selection is
(3,6). Therefore it has C-6 original, unmarked interval units, all supported
by BOTH owners. The alpha can use any one at zero links. In particular with
just one such original unit available, original and correctly pruned payment
are both one, but deleting the resources supported by the pruned square
owner gives payment zero. The square receiver's charge is still -2.

This proves for arbitrary separation why unreachable OWNERS may be removed
while their entire support sets cannot be discarded. It is a failure of a
resource-deletion rule, not a counterexample to the grid inequality.

## 5. Consequence, validation and formal scope

For the aligned unique-square class the apparent capacity-two junction is
fully resolved as an interface: there is no alpha-bearing common-output
relay hidden there. Its known negative tile budget survives unchanged, and
its unreachable routing gates can be pruned with original units retained.
The same-owner fixture shows why an arbitrary multi-square capacity-two tile
requires global strand identity as well as local wire capacity.

The next substantive residual is an alpha-bearing multi-square endpoint
component, or a more general interface with a proven owner-disjoint linkage.
Occupied adjacent bands must retain their original units and export debts.
No coverage theorem for all such components or improved universal coefficient
is claimed here.

The companion checker validates all seven matching patterns, unequal arms,
tile-preserving symmetries, exact original strand/chain/cycle counts, regional
charges, actual same-owner tile trace, all available-pool controls for a
small exterior-alpha model, and shared-unit pruning failures at many widths.
The general coordinate, path and pruning proofs above do not depend on that
enumeration. The Lean module verifies the fixed-wire arbitrary-walk invariant,
component-preserving route reachability and source exclusion, plus the stated
count interfaces. Geometric classification, finite strand extraction and
full primitive/cost pruning remain written proofs and independent Python,
not an end-to-end formalization.

The final [computational receipt](../output/single-square-routing-validation.json)
records 4,543 single-square images over all seven central patterns and eight
symmetries, including 3,245 fully frozen images. Exact counts cover 13,295
source-free mixed owners and 8,545 original PP/M cycles. Eighty-four frozen
shared-gap images give 336 before/after flow comparisons and 84 resource-
deletion failures. All 4,096 subsets of the small model's 12 original
source-support units agree before/after pruning, with independent enumeration
on 64 of those controls. The same-owner obstruction has three independently
enumerated local link matchings and a checked full-board four-payment
certificate.

All 12 declarations in the [Lean source](../formal/SubQuorum/SingleSquareRouting.lean)
pass locally with Lean 4.33.0. Nine are axiom-free; the remaining three use
only standard logical axioms, with no warnings, sorry, native computation
axiom or new axiom. The [formal receipt](../output/single-square-routing-formal-validation.json)
records the precise interfaces and distinguishes them from the full written
geometric classification. No new Oracle review or external priority claim
is made.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_single_square_routing.py \
  --output output/single-square-routing-validation.json
```

No mail was read, drafted or sent. AI tools were used for proof development
and verification.
