# Vertical TP injection and the short-mixed exception budget

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

We extend the original-alpha missing-port injection to **every original TP
terminal whose actual matching edge is vertical across the aligned band
boundary**, including mixed owners. The proof uses local matching geometry
and a two-point freezing contradiction, not the far end of the strand.
Combined with the established partial two-slot certificate theorem, this
localizes possible compensation loss to short horizontal mixed terminals
without immediate BB ports, and to actual marked-boundary port exceptions.
In particular it gives a full compensation class with arbitrary bent/long
mixed strands. It does not prove universal compensation or improve 5/6.

## 1. Original board, available resources, and exceptional tips

Use a feasible selected set T and actual matching M in an aligned,
matching-closed two-row packet. Its first column is blank; its last column
has a blank corner, so TP terminal columns are internal. Every original
matching endpoint has a finite complete freezing certificate for M. It may
use arbitrary original data outside the packet. An endpoint needs two
distinct nonmate neighbors which are selected, or whose actual mates froze
strictly earlier. All geometry below refers to this original board.

Keep the original PP-strand decomposition, original BB--TT interval identities
and the existing marked boundary set K. Available resources I exclude K.
Whole-owner support W(x) is as in the full model. An immediate BB port is
one of the two horizontally adjacent columns with both positions blank;
its original interval identity is retained.

Partition original TP tips into four classes, in this order:

1. A tip with an immediate port in I is port-paid in the certificate.
2. A tip with ports but all their identities in K is a boundary exception H.
3. A tip with no immediate BB port, and actual mate across the band boundary,
   belongs to the vertical demand set X.
4. Every remaining tip belongs to E: it has no immediate BB port and is
   horizontally matched in its own band.

Every E tip is the TP end of an original **one-matching-edge mixed strand**.
Indeed its horizontal mate's within-band partner is blank, by feasibility
of the TP selection. That mate is already BP, so the original open strand
ends there. This uses actual strand length, not a declared link or a virtual
cancellation. Every original alpha TP is vertical, so E contains no alpha
ends. A mixed TP can be vertical regardless of its far BP end.

No additional arbitrary reservations are hidden in this statement. If extra
resources are reserved, their port tips must be added to the exception set;
the bound on H by the boundary marks alone no longer applies.

## 2. Geometric injection for all vertical missing tips

**Theorem 1.** For any subset Y of X, all horizontal BP neighbors N(Y) form
row-path components with Y. Each component is either an isolated TP--BP edge
or a BP-ended alternating path. If c(Y) counts the latter, then

    card(N(Y)) = card(Y)+c(Y).                                  (1)

The BP owners in any one such component are distinct. Thus X has a
simultaneous injection into different adjacent original BP tips. In a
BP-ended component, any one BP tip can be omitted by choosing the injection.

**Proof.** A TP selection lies across the band from its endpoint v. The
selection's two horizontal neighbors are blank by feasibility. Since v has
no BB port, both its horizontal neighbors are occupied; any endpoint among
them is therefore a BP terminal. The two neighbors cannot both be selected:
they would force both horizontal neighbors of v's vertical actual mate blank,
leaving that mate occupied degree at most two, contrary to complete freezing.
Thus v has one or two BP neighbors. BP tips have at most two such horizontal
neighbors. The adjacency graph is a union of finite paths in single physical
rows; there is no row cycle.

The essential stronger exclusion is local. Suppose two vertically matched
TPs u,w share their middle BP v. All three are consecutive in a physical row.
Normalize so the TP selections are above, and all three actual mates below.
The middle BP must indeed be vertically matched: its upper neighbor is blank
and both horizontal neighbors are already vertically matched. If the outer
horizontal neighbor of u were selected, feasibility there would force the
site directly below that selection blank. Put a=mate(u), b=mate(v).
Freezing v requires u retained, hence a frozen strictly earlier. Freezing a
requires b retained, hence v earlier: a has its own mate above, a blank outer
horizontal neighbor, b on the other side, and at most one further neighbor
below. The two ranks cannot each precede the other. The same argument applies
to the outer neighbor of w. This contradiction depends on vertical actual
matching at u,w, **not** on their owning alpha strands.

Consequently a Y tip of BP degree one, whose other neighbor is selected,
cannot share its BP with any other Y tip. Its component is an isolated edge.
Every other component has Y degree two throughout and BP endpoints, proving
the classification and (1). Different BPs in a row component have the same
checkerboard color. An original open PP strand has odd physical path length
(its actual matching edges alternate with within-band PP edges); its two
terminal colors are opposite. A beta therefore cannot own two of these BP
tips, and a mixed owner has only one BP. Ownership within the component is
distinct, though not necessarily between different components.

For a BP-ended component enumerate D_0,A_0,D_1,...,A_(n−1),D_n. To omit D_h,
assign A_i to D_i when i<h, and to D_(i+1) when i>=h. These targets are distinct,
adjacent and avoid h. Isolated edges are forced. Components have disjoint
physical BP identities, so their injections combine. The argument applies
to every Y with all its BP neighbors kept, proving the subset statement. □

This theorem is about original tips. It neither permits modifying M nor
extends automatically to virtual tips of an arbitrarily contracted system.
A chosen target can be a BP of the same original mixed strand; such a link
may close a neutral cycle and supplies no new alpha payment. The certificate
and normalization below explicitly allow that possibility.

## 3. A geometric partial certificate and a necessary deficit signature

Choose one unmarked immediate port for each class-1 TP and assign its tip
to one of that interval's two labelled certificate slots. This is always
possible: an original interval has only two ends, each with at most one
adjacent TP position. Choosing a port consumes at most two slots for the
same original identity across the **entire packet**. Such a direct access
is an eligible W(owner) witness. Independently use Theorem 1 to assign all
X tips to BP targets. BP targets and interval slots have different types.
The resulting partial two-slot certificate has holes **exactly E union H**.
This construction does not require solving an all-TP maximum matching.

Let D run over original owner/resource interaction components, formed using
all actual declared TP--BP links and all original whole-support incidences.
Let a_D be its alpha count, e_D its number of E tips, and h_D its H count.
Let k be total original alpha count. Write V_ord for maximum ordinary payment
and V_full for maximum full payment, allowing beta forks. Then

    k−V_full <= k−V_ord
             <= sum_D min(a_D, floor((e_D+h_D)/2)).            (2)

There exists an ordinary packing attaining at least the right-hand payment
bound using at most card(X) actual links.

**Proof.** Apply the proved partial-certificate lift to the displayed
geometric assignment. Its BP assignments form a terminal matching, including
any neutral cycles. Every remaining free TP is either interval-assigned or
a hole. Each final alpha has two free TP ends, and each original interval
has at most two assigned slots. In each connected final-alpha/assigned-
interval component, the unmatched alpha count is at most half its holes,
rounded down. These smaller components lie within the original interaction
components. Summing their floors is at most floor((e_D+h_D)/2), and cannot
exceed a_D. The actual allocation uses different original intervals; the
subset normal-form reduction removes unused links/cycles and gives ordinary
stems without increasing the card(X) chosen links. Full compensation includes
all ordinary packings, proving the first inequality. □

Taking floors only after merging shared original identities is essential.
Two components' putative half units must not be rounded independently if
an actual resource or mixed/BP gate connects them in the interaction graph.
Conversely, independently separated components do not need to pool their
single holes into a spurious loss.

A marked boundary interval has at most one interior-side neighboring TP:
it is the extreme interval in its band. Hence each H tip may choose a marked
port injectively, and card(H)<=card(K). A coarser universal bound is therefore

    k−V_full <= floor((card(E)+card(H))/2)
             <= floor((card(E)+card(K))/2).                   (3)

Formula (2) is stronger when many components have zero or one exception.
A positive full compensation deficit in a frozen configuration requires
an alpha-containing original interaction component with **at least two**
short-mixed/boundary exceptions. Quantitatively, two exceptions are necessary
per unit of the actual full deficit globally. Exceptions need not cause a
loss: holes on final neutral mixed paths can be ignored, and other legal
assignments/routes can repair an initially bad certificate.

**Full compensation corollary.** If e_D+h_D<=1 for every alpha-containing
interaction component, all original alphas have an ordinary compensation
packing. Its link count is at most card(X). In particular this holds if
there are no boundary exceptions and every original short horizontal mixed
TP has an available immediate BB port. Arbitrarily long and bent mixed
strands, arbitrary mixed directions, cycles and cross-component connections
are allowed. This is a stated geometric subclass, not a proof that every
frozen board belongs to it.

## 4. A new actual mixed-vertical missing-tip witness

Start from the previously checked 14x16 shared-mixed-gate board. Replace

    (9,10)--(10,10)

by the two actual edges

    (9,10)--(8,10),       (10,10)--(10,9).

Keep all original selections and other matching edges. The new matching has
33 edges/66 different endpoints and the same 20 selections. The source
fixture and a strict-rank certificate are saved permanently; feasibility
and complete freezing are checked anew, not inferred from surgery.

The original mixed path

    (5,8),(6,8),(7,8),(8,8),(9,8),(10,8)

is unchanged. It still has BP (5,8) and TP (10,8), whose actual mate is (9,8).
But (10,8) now has no immediate BB port: (10,7) is selected and (10,9) is P.
Its BP neighbor (10,9) is the entrance of a different short mixed strand.
Thus Theorem 1 genuinely covers a mixed TP not covered by the older
alpha-only statement. The checker includes it in the same simultaneous
injection as the alpha tips, not in a separate competing injection.

The new board has two short-mixed holes, (10,10),(10,12), and no boundary
exceptions. Formula (2)'s coarse budget is one, but the displayed certificate's
fine deficit is zero. The full original board pays its two alphas with zero
links using the old distinct bypass intervals. Thus the new fixture is a
nonvacuous geometric extension and a check of safe accounting, not a target
counterexample or a claim that these two short holes cause a real deficit.

For any q>=1 take copies shifted by 14 rows. Their occupied sets have blank
separating rows, so all rank witnesses replay independently and there are no
cross-copy terminal links/support incidences. There are exactly q such
mixed-vertical missing tips and 2q short-mixed holes. The same direct bypasses
pay all 2q alphas at cost zero. The certificate lifts, coarse/fine distinction,
and original resource identities remain copywise. Finite checks q<=8 only
corroborate this all-q separation proof.

## 5. Controls and scope

The saved PP-sealed single/paired fixtures show why (2) is a bound and why
a chosen geometric injection need not itself attain full payment. On the
paired fixture the canonical certificate has deficit one although the full
ordinary optimum pays both alphas. Neither a terminal injection nor a large
number of distinct BP targets may be declared a complete global proof.

The known degree-three nonfrozen board has three vertically matched missing
TPs in a row and only two adjacent BP tips. It refutes replacement of full
freezing by minimum occupied degree three in Theorem 1. The closed two-point
fork argument identifies the missing hypothesis.

Verification reconstructs all original strands and resources, checks row
classification and distinct owners, constructs the joint partial certificate,
checks actual cancellation/allocation lifts and the component exception bound,
and compares ordinary/full optima. Its named small controls also use independent
primitive packing. Carried isometries transport the bands; they do not silently
change the band pairing. Saved strict ranks and the Lean kernel separately
check the new concrete 66-endpoint board.

The Lean file includes the original generic strict-rank freezing theorem,
concrete matching feasibility, all 66 endpoints frozen, and the actual mixed
path with vertical mate/blocked ports/adjacent BP. It also verifies the
arbitrary-length omit-one-target row assignment, its injectivity/adjacency/
bound/avoidance, the strict two-rank contradiction, and the one-exception
budget implication. The geometric row adapter, original-port ownership and
partial allocation lift remain written proofs; this is not an end-to-end
formalization. Exact counts and axiom audits are retained in output receipts.

Reproduce:

    python3 develop/check_vertical_tip_injection.py --output output/vertical-tip-injection-validation.json
    cd formal
    lean SubQuorum/VerticalTipInjection.lean

The next target is the remaining exceptional **short** horizontal mixed
strand: use its actual occupied neighboring bands and freezing dependencies
to repair a pair of exceptional holes jointly or derive a precise capacity
two obstruction. Preserve the full exterior network and original resources;
do not physically delete a beta or neutral branch and assume freezing survives.
The 11 October manuscript, public main and 5/6 bound remain unchanged.

## 6. Correction to the preceding joint-block note

The preceding note's introductory statement that a normal form identifies
ordinary and fork optima was too strong. General full fork compensation can
strictly exceed ordinary-only compensation, as the existing fork-flow note
already shows. Its introduction now correctly identifies full cancellation
with the BP-aware full fork network. The joint-block proof and its exact
network retain that full network; neither the local allocation theorem nor
its projection/lift needs a general ordinary/full equality. This correction
changes no solver or theorem hypothesis. The new bound (2) deliberately keeps
the inequality V_full>=V_ord rather than asserting equality.

## Continuation: short-chain and corridor reduction

The [short mixed chain note](SHORT_MIXED_CHAINS_AND_CORRIDOR_HOLE_BUDGET.md)
strengthens the displayed certificate by assigning BT-corridor slots and
all non-tail short TPs. It replaces short-owner hole counts by unported
chain-tail counts and proves exact full-flow contraction with the required
internal-link toll. The original hypotheses and statements here are retained.
