# Mixing strip certificates by incidence component

20 October 2026. Two valid allocation rules can be mixed on disjoint
resource components. This improves on choosing one rule globally, resolves
the first charge-four obstruction to the unit-per-run rule, and identifies
the remaining resource loss exactly. A separate fully frozen example
refutes reservation monotonicity for the new score. The general geometric
coverage inequality and the unrestricted grid bound remain open.

## 1. Physical hypotheses and the two rules

Use a feasible selected/matching pair(T,M)on an even rectangle, its fixed
disjoint2-by2tiling, and endpoint-free tiles Z. Each such tile has actual
integer capacity d_Q=2-|T intersect Q| in{0,1,2}. First reserve distinct
physical units:integer0<=a_Q<=d_Q, B=sum a_Q, r_Q=d_Q-a_Q,
D=sum d_Q, R=D-B.

Retain the ORIGINAL maximal horizontal and vertical Z-runs after reservation.
Form the residual bipartite multigraph with runs as vertices and each
physical slot(Q,unit)as an edge joining h(Q)and v(Q). Every run pair meets
in at most one tile and hence has multiplicity at most two. Components
here are components of this RESOURCE graph, not endpoint receiver components.
Zero-capacity isolated runs have no credit and may be retained or omitted.

For a connected component C, let v_C,e_C be its vertex/slot counts and
o_C the number of odd-degree run vertices. Define

    K_C = min(v_C,e_C),
    W_C = sum_{s in C} floor(deg(s)/2) = e_C-o_C/2.

K_C is the previously proved exact one-request-per-run rank. W_C is the
half-capacity rule, allowing several requests at one run. The handshake
identity makes o_C even. Parallel slots count as separate edges and each
degree is computed AFTER reservations.

**Half-capacity feasibility.** Give run s exactly floor(deg(s)/2)copies
of a one-unit request. For any subset Y of request copies, let A be its
support set of runs. Then

    |Y| <= sum_{s in A} floor(deg(s)/2)
        <= (sum_{s in A} deg(s))/2
        <= number of distinct slots incident with A.

The last inequality holds because each slot has at most two ends in A.
All copies of a run see all its incident slots, so the last count is the
neighbor count of Y. Hall's theorem gives distinct actual units. This
support-subset argument handles partial subsets of copies; checking only
complete groups of copies would not state every Hall condition.

## 2. General non-reuse lemma

**Theorem1.** There is a non-reusing allocation of

    F(r) = sum_C max(K_C,W_C)                                  (1)

credits, choosing one of the two complete rules independently on each
resource component. In particular,

    max(sum_C K_C,sum_C W_C) <= F(r) <= R.                      (2)

**Proof.** In C choose a K_C-credit allocation if K_C>=W_C, and a
W_C-credit allocation otherwise. The first is the exact incidence-rank
construction; the second is the Hall construction above. Each uses
distinct slots within C. Different graph components have disjoint slot
sets. Their union therefore uses every physical unit at most once.
It is precisely(1). Each branch is bounded by e_C, proving the upper
bound; choosing a maximum componentwise proves the lower bounds. QED.

This is the exact maximum for the specified family that chooses one
complete rule per component. It is NOT claimed to be the largest possible
allocation with arbitrary requests per run; such a model could simply
assign every slot to one of its incident runs. The contribution is the
safe combination of these two particular sufficient certificates.

The improvement can be strict. In a2-by-3tile array give tiles(0,0),
(0,1)capacity2, tile(1,2)capacity1and all others zero. One component
has v=3,e=4,K=3,W=4; the other has v=2,e=1,K=1,W=0.
Thus global K=4and global W=4, but F=5=R. This resource pattern is
physically realized on a4-by-6vertex rectangle by taking an independent
checkerboard selection, deleting both selections from the two capacity-two
tiles and one selection from the capacity-one tile, with M empty.
Its receiver charge is zero. It demonstrates a strict allocation-budget
improvement, not a frozen obstruction or a new grid extremum.

## 3. Exact remaining loss and the receiver consequence

Since K_C=min(v_C,e_C)and W_C=e_C-o_C/2,

    E_mix(r) = R-F(r)
             = sum_C min(max(0,e_C-v_C),o_C/2).                (3)

Thus a component loses capacity under this certificate only if it has
MORE edges than vertices AND at least one odd-degree run. Trees, components
with exactly one cycle, and components whose run degrees are all even
use their entire slot budget. Both conditions concern the residual graph.

Now assume single terminality, complete receivers and the ORIGINAL corrected
identity sigma=mn/2-|T|-|M|=D-rho, where rho=sum_H rho_H. Put q=rho-B.
The mixed sufficient coverage condition and its consequence are

    q <= F(r)  =>  rho <= B+F(r) <= D  =>  |T|+|M| <= mn/2.    (4)

Equivalently, coverage by this certificate asks

    sigma=R-q >= E_mix(r).                                    (5)

This is a global inequality: it does not attach each run to a particular
receiver. If an application requires such routing, it must add that
restriction. The theorem itself does not prove(4)'s coverage hypothesis
for every grid configuration. No unrestricted five-sixths improvement or
grid triple equality is asserted.

The reservation failure below now has an exact parity/surplus accounting
and a safe order for its two actual donors. See
[Safe reservations and cross-component parity compensation](SAFE_RESERVATIONS_AND_CROSS_COMPONENT_PARITY.md).
That follow-up also proves a batch criterion and excludes double use
of parity changes from rank-branch components.

## 4. First possible separating failure moves to residual charge five

**Theorem2.** If F(r)<q but the target survives, sigma=R-q>=0, then
q>=5. If q=5, there is exactly one resource component with positive
capacity; it has

    v=4, F=4, e=R in{5,6}, sigma=R-5 in{0,1}.                 (6)

At e=5the graph is any connected bipartite multiplicity-at-most-two
four-vertex graph with five edges. At e=6it is the doubled-diagonal
four-cycle with multiplicity matrix

    2 1
    1 2

up to swapping the sides and their vertex orders. Isolated runs are
irrelevant. These are resource shapes, not asserted frozen realizations
with residual charge five.

**Proof.** Suppose a component loses a slot in(3). Then e>v and o>0.
It cannot have v=1because there are no loops, or v=2because multiplicity
is at most two. If v=3, its bipartition has sizes1and2, so e<=4.
The only e>v possibility is two doubled edges, whose degrees4,2,2are
all even, contradicting o>0. Hence every component with positive loss
has v>=4and K_C=v>=4, so its mixed credit is at least four.

If F<q<=R, at least one component has positive loss. Thus F>=4and
integer q>F implies q>=5. This uses no enumeration. In particular,
the unit-rank charge-four resource obstruction has W=R=4and is paid
completely by the mixed rule.

If q=5, F<5gives F<=4. A positive-loss component already contributes
at least four, so there is exactly one positive-capacity component,
F=4, K_C=v=4and e>v. Since W=e-o/2<=4and o<=v=4, e<=6.
Target survival gives e=R>=5. Thus(6)holds.

For e=5, the two part sizes are1and3or2and2. In the first case edge
multiplicities are2,2,1; in the second, each side has exactly one odd
degree because its degree sum is five. In either case o=2and W=4,
so every connected admissible five-edge shape has F=4.

For e=6, W<=4forces o=4. Part sizes1and3would have an even-degree
central vertex of degree six, impossible. The sizes are2and2. Each
run has positive odd degree at most four, and the degree sum on each
side is six, forcing all four degrees to be three. A2-by-2matrix with
entries0,1,2and every row/column sum three has the displayed form.
Conversely it has e=6,K=W=F=4. QED.

In the five-edge2-by-2case, the multiplicity matrices are, up to row/column
orders and transposition,

    2 2      1 2      2 1
    1 0      2 0      1 1

together with the1-by-3star(2,2,1). The first two are different weighted
paths, and the last is a cycle with one doubled edge. No adjacency of
the actual physical tiles is inferred; zeros and intermediate zero-residual
tiles can occur in the original runs. At positive reservations, a residual
capacity-one tile may be originally blank with one unit consumed, so its
selected count must not be inferred from residual capacity alone.

## 5. Reservation monotonicity DOES NOT extend to this mixed score

The earlier monotonicity B+K(d-a)under additional distinct reservations
remains valid. The analogous assertion for B+F(d-a)is FALSE, even
when the new reservation is an actual owned donor in a fully frozen
configuration. Feasibility and non-reuse of Fremain valid after each
reservation; its total must be recomputed.

Use two_leg_case(6,4,6), with the20-step freezing proof in the checker:

    TPPPPPPT
    .PPPPPP.
    TP....PT
    .PT..TP.
    TP....PT
    .T...TP.
    ......PT
    ......T.

Coordinates start at zero. There are20endpoints,12selected vertices,
10matching edges and one complete receiver with nine tiles/nine selected
vertices. Its ORIGINAL corrected charge is1; outside capacity is D=11.
The objective is22<half-area32. The original two saturated-endpoint
transfers are included in the verified ledger.

The three horizontal maximal runs have degrees2,3,6and the three vertical
runs degrees2,5,4. The residual incidence graph is connected, giving

    K=6, W=F=10, B=0.

At tile Q_(1,2), selected vertex(3,5)has endpoint anchor(3,6). The
opposite corner is(2,4), with guard(1,4): that guard is an endpoint
of occupied degree three, all its neighbors are endpoints, and it has
the same endpoint-component owner as the anchor. This is a valid fourth
saturated-endpoint donor with actual capacity1, as verified by the
existing general donor theorem and the independent physical checker.

Reserve its one unit. Original runs stay fixed. Their degrees become
1,3,6horizontally and2,5,3vertically. The graph is still connected:

    K=6, W=F=8, B=1, B+F=9<10.

Thus a genuine additional owned reservation lowers the mixed certificate
total by one. It does not refute the allocation theorem or the target:
charge1is paid both before and after. It also does not refute the old
pure-rank monotonicity; B+Kgoes from6to7. Nor does this one-step example
assert failure of a policy that reserves every available donor at once.

The mechanism is parity: deleting this slot changes two even run degrees
to odd, reducing Wby two while increasing Bby only one. An even simpler
resource-only control is an all-blank2-by-6rectangle: F=6before a single
reservation and B+F=1+4=5after it. That control has no endpoint donors;
the20-endpoint example above supplies the actual owned-donor case.

## 6. Validation and scope

The implementation constructs the chosen requests per component, matches
them to individual slots, and checks their union for physical non-reuse.
The checker independently verifies branch request counts and every Hall
subset on all729multiplicity0/1/2patterns on a2-by-3tile array. Six
patterns strictly improve on max(global K,global W). Exactly60have the
first charge-five separating RESOURCE shape:54with R=5and six with
R=6. These counts are controls of the general proofs, not their basis.

There are96physical fixture/symmetry/reservation cases and six separated
mixed-receiver cases, checked for feasible grids, branch demand counts
and distinct actual assigned units. Their large Hall-subset families are
not enumerated. The frozen donor counterexample includes exact coordinates,
the actual matching, its20-row ordered proof and the original corrected
ledger in output/component-strip-certificates-controls.json. The earliest-
promoted-endpoint argument using the two retained neighbors excludes every
mixed simultaneous promotion bundle, not just single-color moves.

Run:

    python3 -B develop/check_component_strip_certificates.py --output output/component-strip-certificates-controls.json

The Oracle ACCEPT for LOW_CHARGE_RANK_BARRIER.mdcovers its earlier
unit-rank lemmas only; it does NOT cover this new mixed theorem, first
charge-five classification or monotonicity counterexample. Formal and
external review evidence for this extension must be recorded separately.

Four local Lean4.33.0Std declarations in
formal/SubQuorum/MixedStripCertificates.lean prove the exact loss formula,
its zero-loss characterization, the component budget upper bound and the
general parity-based arithmetic decrease after a reservation. All compile
and are axiom-audited: three use propext/Quot.sound, and the zero-loss
equivalence additionally uses Classical.choice. The physical/Hall adapter,
first-failure classification and frozen donor geometry remain written plus
independently checked; these four arithmetic statements do not formalize
those parts. See output/mixed-strip-certificates-formal-check.json.

A separate new Oracle review is live as task
d3ca9d1e-c4b9-4d3d-9449-7cc13d636171, conversation conv_6b2cadf34fbc51fe,
original stream execution87019. It receives the complete written note and
the exact physical counterexample/matching/freezing certificate. It has
no final verdict yet and does not execute code or Lean. The request and
original stream are preserved, with no inherited acceptance from the
earlier rank-only result.
