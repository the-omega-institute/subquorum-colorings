# Opposed direction interfaces: both uniform directions fail, a valid partition pays all

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

Follow-up: [exact interface optima](FROZEN_INTERFACE_OPTIMALITY.md) settles the
one-point uncertainty: the unrestricted fixed-P maximum is2t, whereas the
maximum with all endpoints frozen is exactly2t-1, attained by this construction.
Only two specified frozen endpoints force the interface loss. The statements
below retain their original near-maximum formulation.

The [perpendicular repair theorem](PERPENDICULAR_GUARDED_RESERVES_AND_JOINT_MAXIMALITY.md)
fully compensates every selection on the homogeneous module endpoint family.
It does not extend to choosing a single better direction on a mixed board.
We construct, for every q>=1, an actual fully frozen board with unique actual
matching, jointly inclusion-maximal T and P, such that BOTH aligned global
directions pay only q of their2q alphas, with every original resource available.
The gap is unbounded even though the displayed T is at most ONE selection
below the true fixed-P maximum. A valid two-region partition, using different
directions in the two regions, pays all2q with zero links and disjoint physical
resources.

The obstruction concerns uniform-direction full compensation. Its numerical
slack is4q+1, so it is not a counterexample to the target numerical inequality.
We do not optimize over deleting/replacing T or P, or over other band phases.
The universal5/6 improvement remains open. The submitted manuscript is unchanged.

## 1. Explicit opposed construction and its one necessary interface deletion

Put W=10q and L=W+2. Let H_q be the L-by-L configuration of the preceding
notes: `configuration(W,q)`, with endpoint set P_H, unique actual matching
M_H and maximum selected set T_H. Its exact counts are

    t=35q^2+13q+2,    m=15q^2+5q,    S_H=2q.              (1)

Use coordinates0..L-1 in each square. Put H_q on the left of an L-by-2L
board. On the right put its reflected transpose under

    f(r,c)=(L-1-c,L+r).                                 (2)

This reflects original columns before transposing and translating. Retain
both endpoint sets and actual matchings. Delete exactly the left selection

    x=(2,L-1).                                          (3)

Call the resulting full pair(T,M), with P=V(M). The counts are

    |T|=70q^2+26q+3,    |M|=30q^2+10q,
    |V|/2=L^2,         S=|V|/2-|T|-|M|=4q+1.             (4)

Here is a direct feasibility proof for all q. No endpoint lies on either
side of the seam: columnsL-1 andL contain selections or blanks only.
The left boundary selections in columnL-1 are at rows0,2,3,5,...,W-3,W-1,W+1.
The right boundary selections in columnL are at even rows0,2,...,W. Their
only intersections are rows0,2. At row0 the two selections were individually
isolated, so their new cross-seam pair is feasible. At row2, the left x
already sees(3,L-1) in T, and the right selection b=(2,L) already sees the
endpoint(2,L+1). Keeping both would give each two occupied neighbours.
Deleting x removes this conflict and changes no other cross-seam contact.
Every remaining selected point therefore has at most one occupied neighbour.
The uncorrected union is infeasible; at least one deletion is necessary for
these displayed placements. One deletion suffices for every q.

## 2. Complete freezing and unique actual matching

The deleted point x is not among the selected seeds of ANY translated
right-module reduced-T freezing certificate in the preceding note. The
left square retains all those seeds. Replay its uniform strict-rank schedule;
replay the reflected/translated original schedule on the right. Every selected
witness and every earlier mate witness is retained. There are no cross-seam
P edges: left endpoints have columns at mostL-3, right endpoints at leastL+1.
Consequently the two schedules are independent, and every endpoint is frozen.
This proves all-q freezing, rather than relying on finite peeling output.

The same separation gives matching uniqueness. Each of the2q original P slabs
has the previous forced leaf-pair order; transpose/reflection transports it
on the right. No new P adjacency joins slabs or squares, so every perfect
matching of the full induced endpoint graph must equal M. This assertion
is independent of T.

## 3. Both aligned GLOBAL directions have exact deficit q

For horizontal bands, the left square originally has q alphas, no beta,
7q mixed strands and complete reachable support empty. The removed x lies
in the SECOND band and is not a band partner of any endpoint. It changes
no endpoint label, original strand, link or pure cycle. Every mixed owner
reachable from a left alpha still touches only the two terminal bands;
PP bodies are shielded by P columns.

Horizontal no-P gaps can extend across the new seam, so this must be checked
rather than assuming the two old networks simply add. The right square has
NO endpoints in its first or last horizontal band, and each of those whole
bands has exactly L selections in L columns. Indeed these are the reflected
original last-two and first-two column pairs of H_q; both have zero band
capacity. When appended to a left terminal gap of capacity zero, they add
zero capacity. Capacity is columns minus selections; the full BB/TT adapter
counts balanced boundary chains with zero credit. The merger therefore
creates no resource accessible to a left source. There are no cross-seam
TP--BP links because there are no endpoints on the seam columns.

Thus the entire closed directed owner set reachable from the q left alphas
contains no beta and has empty complete interval support. The whole-support
route/cancellation normal form implies none of those alphas can pay, even
by a long mixed route or beta fork, giving V_H<=q.

On the right, the reflected version of the preceding vertical two-reserve
lemma supplies q direct payments. Choose its INTERNAL guarded singleton
units, which remain present after gluing; no source or physical unit is used
twice. This gives the matching lower bound, hence V_H=q with minimum cost0.

For vertical bands, the seam is a boundary between aligned column pairs,
so no original band is extended across it. The right square retains its
entire bad-direction decomposition and has q alphas with empty reachable
support and no reachable beta. The left square is in its good direction:
its q alphas keep both internal private singleton reserves. The removed x
is in its last vertical band, outside all alpha supports. Hence V_V=q and
minimum cost0 as well.

The complete inventories in BOTH directions are

    alpha=2q,    beta=q,    mixed=5q(q+1),
    original intervals=5q+1,    V=q,    deficit=q,    c=0.  (5)

The alpha/beta/mixed counts follow from the preceding two inventories and
the unchanged tip labels at x. The raw count then follows from the exact
whole-band ledger S=L_raw+beta-alpha and(4). Every raw resource is available;
there are no locked or reserved units. The failed sources are locally zero,
so this is not a new assertion of individually full components failing only
through resource collision. It excludes the proposed global direction fix.

## 4. A valid piecewise partition pays all, without adding incompatible credits

Partition the board into its two even-by-even L-by-L squares. In the LEFT
square pair columns; in the RIGHT square pair rows. All actual M edges lie
inside their square. These local auxiliary pairings together are a genuine
matching covering every board vertex; no vertex receives two auxiliary mates.
In contrast, independently rotating arbitrary overlapping component supports
would not supply a valid global auxiliary pairing.

For left module i the chosen direct reserve has physical cells

    {(2,10i+2),(2,10i+3)}.

For the reflected right module i choose the image under f of the same
original guarded pair, with physical cells

    {(L-3-10i,L+2),(L-4-10i,L+2)}.                      (6)

All2q units are actual singleton resources in their stated local decomposition.
They lie in disjoint squares, are disjoint within each square, and support
different alpha owners. Their union pays every one of the2q local alphas
with no links. This is a new PIECEWISE decomposition, not an allocation from
the unchanged raw pool of either uniform direction.

Its inventories are alpha=2q,beta=2q,raw=4q+1; again S=4q+1. The only
extra raw unit beyond the4q guarded units comes from the deleted selection.
Thus every decomposition has the same exact numerical slack, while the
piecewise one improves actual compensation by q over either uniform one.

**Rectangle partition gluing lemma.** Let an even-by-even grid be partitioned
into finitely many disjoint even-by-even rectangles. Assume no actual matching
edge crosses a rectangle boundary. Choose horizontal or vertical bands in
each rectangle, and use the complete even-width BB/TT resource convention.
If each rectangle fully compensates all its original alphas with zero links,
then the piecewise decomposition does too. Its ledger is

    S_global=sum_R S_R=sum_R(L_R+beta_R-alpha_R).         (7)

Proof. Restricting T,P,M to a rectangle preserves feasibility and cuts no
actual matching edge. Its auxiliary band pairing stays in that rectangle;
all the local pairings together cover the board exactly once. Local alpha,
beta and interval components have disjoint physical domains. Assign each
resource its rectangle and local component identifier; this is injective
on physical units because rectangles are disjoint. The union of the local
zero-link assignments is feasible and injective, paying every alpha. The
numbers of vertices, selected points and actual matching edges add, so the
local objective ledgers add to(7). Cross-boundary T contacts cause no extra
counted credit and were already checked for global feasibility. QED.

For nonzero local link costs the same construction only promises a feasible
assignment of total local cost. It does not assert global minimum-cost
additivity in a model admitting extra cross-boundary links. The zero-cost
case needs no such qualification because costs are nonnegative.

The no-crossing-M and rectangle-partition hypotheses are essential to this
argument. One cannot assign different directions to overlapping arbitrary
P-component neighbourhoods and simply sum their resource budgets.

## 5. Joint inclusion maximality despite arbitrary rematching

We can rule out a maximality explanation for the new failure too. Any
feasible(T',M') satisfying T subset T' and P subset V(M') must have
T'=T, V(M')=P and M'=M. Neither old M retention nor a one-edge insertion
assumption is imposed. This remains inclusion maximality, not a global
maximum over replacements of T or P.

First establish that T has no individually addable point with P fixed.
Inside the unchanged right square this follows from its exact maximum.
On the left, deleting x from a maximum can only change an addition test
within graph distance two of x. The only remaining selected neighbour of
x is(3,L-1). The blank points in that distance-two neighbourhood other
than x are

    (1,L-1), (2,L-2), (2,L-3), (3,L-2), (4,L-1).

The first two touch the already saturated selection(1,L-2); the third has
both the endpoint(1,L-3) and the selection(2,L-4) as neighbours; the fourth
has at least the three selections(3,L-1),(3,L-3),(4,L-2); the fifth has
(3,L-1),(4,L-2),(5,L-1). They cannot be added. Finally x cannot be restored
because the right selection(2,L) already faces P(2,L+1). All other additions
were already forbidden before deleting x. Feasibility is monotone under
removing added selections, so no simultaneous selected enlargement is possible.

For possible new endpoints define the necessary hull of sites whose adjacent
selected vertices are ALL currently isolated, as in the preceding note.
Let H_0 be the exact hull of the isolated maximum square H_q, given there
by its full row table. A necessary hull of the combined configuration is

    H_coarse=H_0 union f(H_0) union {y},    y=(3,L-2).     (8)

To prove containment, the right square loses no selected point, so every
new endpoint there was already in f(H_0). On the left, deleting x only
unsaturates the old selected neighbour(3,L-1), so it can only create new
candidates at x,(4,L-1),(3,L-2). The first is blocked by the saturated
right selection(2,L); the second by(4,L), which faces the endpoint(4,L+1).
Thus only y remains. Additional cross-boundary occupancies can exclude
candidates but cannot create any other ones.

By the old hull table, all H_0 candidates outside

    E_0={(W-1,10i+9):0<=i<q}
          union{(W-1,10i+3):1<=i<q}

are isolated in P_H union H_0, and E_0 is entirely checkerboard colour0.
The right image f(E_0) is entirely colour1, because f reverses parity.
The new y has no P neighbour and no neighbour in H_coarse. The old isolated
candidates remain isolated after gluing: the right hull has local columns
at least4, left hull columns are at mostL-1, and all cross-square endpoint
separations are at least four. Thus no edge of the induced graph on
P union H_coarse crosses the square partition.

Any new endpoint covered by M' must therefore lie in E_0 on the left, or
in f(E_0) on the right. A global colour balance alone would be insufficient:
these are opposite colours. Instead apply balance separately in the two
squares, which cannot exchange a matching edge even after all allowed
insertions. Each old P portion is balanced; any nonempty new subset in that
square has just one colour and cannot be perfectly matched. Hence no new
endpoint is possible. The unique-matching result then gives M'=M. With P
unchanged, the previous selected-hull argument gives T'=T. QED.

This componentwise distinction is material: equal TOTAL numbers of new
black and white candidates do not help if they are in separated matching
regions. The proof uses the full simultaneous hull, so arbitrary rematching
cannot open a missing cross-region path.

## 6. Within one of the true fixed-P maximum

The displayed T need not be advertised as a maximum without a proof.
For ANY feasible U on this full endpoint set, restrict U to either square.
Each restriction has at most t selected points by the preceding exact
fixed-P theorem, transported by f on the right. Thus

    |T|=2t-1 <= max_fixed_P |U| <= 2t=|T|+1.             (9)

We do not decide between these two integers here. The bound proves that
the uniform-direction deficit q is unbounded even when the selection
objective is within one of its true optimum, and even under joint inclusion
maximality and unique actual matching. Thus a bound on this compensation
failure solely by a bounded cardinality loss from selection optimality
cannot hold. A different exact-optimum representative might still repair
it; no contrary claim is made.

The smallest example q1 is a12-by24 board with99 selected vertices,40
matching edges,80 frozen endpoints and slack5. Each uniform direction has
two alphas, one beta, six raw units, value1,cost0,deficit1. The two-region
choice has two alphas, two betas,five raw units,value2,cost0. Its true fixed-P
selection maximum is99 or100 by(9).

## 7. Verification and formal scope

The direct checker tests q=1..8,10,12:10 boards,28040 strict freezing
witnesses and14020 forced matching pairs, with independent peeling agreement.
It computes both complete raw networks, proves their failed-owner closures
have empty support and no beta, and verifies20 exact full-pool flows. For
q<=3 an independent primitive-certificate optimizer confirms all six optima.
All eight carried isometries of q1..3 give48 additional direction controls.
The116 piecewise direct payments have distinct physical cells.

For every tested q it checks the full endpoint hull against(8), its isolated
and square-specific single-colour candidates, absence of any crossing hull
edge, the empty selection-addition hull, and an independent augmenting-path
matching search on P union H. The known matching is already maximum on
that hull; no new endpoint augmentation is possible. These are checks of
Section5's general proof, not an enumeration substitute for it.

The Lean source supplies a general no-payable-exit consequence of a closed
route set, an injectivity lemma for region-tagged payments and the finite
partition ledger arithmetic. It checks the actual q1 feasible99T geometry,
all80 endpoints frozen, the concrete closed zero-support/no-beta certificates
in BOTH directions and the corresponding arbitrary-length route exclusions,
together with direct payment witnesses. The all-q interface formulas,
coordinate-to-owner/resource adapters, endpoint-hull classification and
piecewise geometric partition lemma remain written proofs plus Python checks.
We do not call this end-to-end formal verification of the grid claims.

Reproduce from the repository root:

    python3 develop/check_opposed_direction_interfaces.py --output output/opposed-direction-interfaces-validation.json
    python3 develop/check_opposed_direction_formal.py --lean /path/to/lean-4.33.0 --output output/opposed-direction-interfaces-formal-validation.json

The next geometric question is how to find a suitable cut-respecting rectangle
partition, or control the matching edges that obstruct such a partition.
Selecting a single global direction is insufficient; assigning directions
without a valid disjoint partition remains unjustified. All numerical
ledgers here are positive and consistent with the target inequality. Other
band phases, unrestricted adaptive decompositions and the universal5/6
improvement remain open. No mail is sent by this research update.
