# Sealed strips give a global capacity bound despite horizontal–vertical overlap

20 October 2026. We extend the three-tile compensation argument to maximal
endpoint-free strips of arbitrary length in both physical directions. The
two-unit local guarantee and maximum overlap two give a one-unit global
credit per strip, with a genuine capacity allocation. This handles shared
resources without assuming that different descriptions identify different
donors. It is a structural sufficient criterion, not a proof that enough
strips exist in every grid representative.

The sharp example is the fully frozen remote-deficit configuration: its
horizontal three-tile strip and vertical two-tile strip both see the same
capacity-two tile. Crediting both strips with two units would count four
units where only two exist. Crediting one unit to each is exact.

## 1. Physical resources and maximal runs

Let (T,M) be feasible on an even-by-even rectangle. Put P=V(M). Use the
original fixed disjoint2-by2tiling and let Z be its endpoint-free tiles.
Selected means membership in T; blank means membership in neither T nor P.
For Q in Z write

    d_Q=2-|T intersect Q|.

Every unit square contains at most two T-vertices: any three have
a selected corner adjacent to the other two. Thus d_Q is a nonnegative
integer. The entire available budget is D=sum_(Q in Z)d_Q.

A horizontal run is a maximal nonempty consecutive interval of tiles in
Z within one physical row band. A vertical run is defined by transposition.
Runs may meet the ambient boundary. Distinct horizontal runs are disjoint;
distinct vertical runs are disjoint. Each tile of Z therefore belongs to
exactly one run in each direction, and to at most two members of any
subcollection of these runs. A run and its reversed description are the
same run; the horizontal and vertical descriptions of a singleton tile are
two distinct directed-axis runs, each counted once.

A horizontal run is **sealed** if its two outermost vertex columns are
blank in both rows. A vertical run is sealed if its two outermost vertex
rows are blank in both columns. The definition concerns actual labels,
not just absence of endpoints. The support hypotheses from the earlier
three-tile lemma force precisely such sealing in its example.

## 2. Arbitrary-length local capacity

**Sealed-strip lemma.** A sealed run of k>=1 physical tiles has total
actual capacity at least two.

Proof. In the horizontal case the two blank boundary columns leave only
the middle2-by(2k-2)sites available for selections. Partition these sites
into k-1 disjoint unit squares, starting one vertex column after the
physical strip boundary. Each contains at most two selections. Therefore
the original k physical tiles have at most2k-2selections, giving

    sum_(Q in strip)d_Q=2k-|T in strip|>=2.

For k=1 the two blank columns comprise the entire tile and its capacity
is exactly two. Transposition proves the vertical case. The auxiliary
squares bound a selection count only: their capacities are never added
as separate resources. QED.

Maximality is not needed in this local lemma. It is needed in the global
overlap bound: arbitrarily many nested subinterval descriptions must not
be counted as independent strips.

## 3. Global non-reuse inequality and unit allocation

Let S be any collection of distinct sealed maximal runs, in either or
both directions. For any subcollection A of S let U(A) be its union of
physical tiles and m_A(Q) its membership multiplicity. Then

    2|A| <= sum_(s in A) sum_(Q in s)d_Q
          = sum_(Q in U(A))m_A(Q)d_Q
         <= 2 sum_(Q in U(A))d_Q.                         (1)

The first inequality is the sealed-strip lemma. The second uses only
m_A(Q)<=2 and d_Q>=0. In particular

    |A| <= sum_(Q in U(A))d_Q,   and   |S|<=D.             (2)

This counts every physical capacity at most once in the final budget,
including at perpendicular crossings and at doubly described singleton
tiles. It does not require one component to own each strip.

There is also an actual allocation: give Q exactly d_Q distinguishable
unit slots, and connect each strip to slots in its constituent tiles.
For every set A of strips, its slot-neighborhood size is the right side
of(2), at least|A|. The finite marriage theorem consequently matches every
strip to a distinct slot. One can construct this by repeatedly taking an
augmenting path. If a new strip has no such path, the alternating reachable
strips and slots give a set A with fewer neighboring slots than strips,
contradicting(2). Thus each strip receives one real unit, and no tile pays
more than its actual capacity. No geometric movement or relabeling of the
configuration is asserted; this is a deficit allocation.

## 4. Reserve previous credits before adding strip credits

To combine this with earlier corner or component arguments, first reserve
integer amounts a_Q with0<=a_Q<=d_Q at physical tiles Q in Z. Each a_Q
counts distinct actual unit slots already assigned; prior assignments must
not reuse any slot. Let B=sum_Q a_Q and r_Q=d_Q-a_Q. A strip may be used in the
residual argument only if its actual residual capacity satisfies

    sum_(Q in s)r_Q>=2.                                  (3)

Let S_res be any collection of distinct maximal runs meeting(3). They
need not be sealed if(3)is established by another valid argument. Repeat
(1)with r in place of d. The same subset inequalities and matching proof
give one distinct residual unit to each strip, and

    B+|S_res| <= B+sum_Q r_Q = D.                         (4)

This is the required compatibility rule. Sealing proves the original
capacity, not the residual capacity after earlier reservations. Keeping
a strip merely because it was originally sealed would be unjustified if
those reservations removed its needed units.

An exact weighted variant is also available. Define the exact residual
capacity C_s=sum_(Q in s)r_Q and c_s=floor(C_s/2). For any set Y of request
copies, let A be its support set of distinct maximal runs. Then

    |Y| <= sum_(s in A)c_s <= (1/2)sum_(s in A)C_s
        <= sum_(Q in U(A))r_Q = |N(Y)|.

The multiplicity-two bound applies to A before duplication; the copies
themselves need not have multiplicity two. Thus Hall applies to c_s
identical unit requests for each strip. In particular

    sum_s floor(C_s/2) <= sum_Q r_Q.

The one-unit statement is sufficient for the examples here.

## 5. Consequence for the original complete-receiver ledger

Now assume single terminality and use the complete receiver convention

    R_H={physical tiles containing an endpoint of component H}.

Thus each R_H is disjoint from Z, and Z is the complement of their union.
The established tile-ownership lemma makes
the complete endpoint-component receivers disjoint, and the original
corrected ledger is

    mn/2-|T|-|M| = D - sum_H rho_H.

**Cross-component strip compensation theorem.** Suppose reservations and
distinct maximal runs meet the hypotheses of Section4, and

    sum_H rho_H <= B+|S_res|.                             (5)

Then|T|+|M|<=mn/2. The stronger, sometimes easier-to-check condition with
sum_H max(rho_H,0)on the left also suffices.

Proof. Equation(4)bounds the right side of(5)by D. Substitute into the
original ledger. The unit-slot matching describes a concrete non-reusing
way to allocate the additional credits after the reservations. Charges
and resources can come from different endpoint components; no unproved
local owner identification is used. QED.

This replaces the earlier demand for disjoint individual corner donors by
a general overlapping-strip budget. For configurations satisfying(5), it
proves the half-area bound. An optimization equality additionally requires
the external lower bound and the appropriate representative argument;
neither follows from strip capacity alone. It does
not improve the unrestricted five-sixths bound: proving(5)for all relevant
representatives remains open. An arbitrary feasible pair meeting(5)alone
does not imply that every optimum has such a representative.

## 6. Optional ownership from planarity

Use exactly the endpoint-bearing receiver convention in Section5, with
R_H disjoint from Z; padded receiver neighborhoods are not allowed here.
For a run bounded on both ends by receiver tiles of the same component H,
call that run H-enclosed. Its endpoints are the immediately preceding and
following tiles, not arbitrary distant anchors. The following owner fact
is useful when one wants a per-component allocation instead of(5).

**Crossing-owner lemma.** Two perpendicular enclosed maximal runs sharing
a tile must be enclosed by the same endpoint component.

Proof. Work in the planar graph of physical tile centers and shared-edge
adjacency. Receiver tiles of each component form a connected subgraph,
because every endpoint path maps to a tile path. Distinct components have
disjoint receiver tile sets by single terminality.

Suppose a horizontal run is enclosed by H and a crossing vertical run by
K!=H. Join the two horizontal bounding tiles by a simple path in R_H.
Together with the straight path through the horizontal run this forms a
simple polygonal cycle: the interior run tiles contain no endpoints and
cannot occur on the R_H path. The vertical run, extended by its two K
bounding tiles, meets this cycle exactly once, transversely at the common
tile center. Its other interior tiles lie in Z and therefore avoid R_H;
the two straight axis runs intersect only at the common tile. Its K
bounding tiles lie in R_K, avoiding both R_H and the horizontal Z run.
In the planar square-lattice center embedding edges cross only at common
vertices. These facts exclude every other intersection with the cycle.

The two K bounding tiles therefore lie on opposite sides of the cycle.
A tile path within connected R_K would join them without intersecting the
cycle: it uses neither H tiles nor endpoint-free horizontal-run tiles.
This contradicts planar separation by the simple cycle. Hence H=K. QED.

Parallel enclosed maximal runs are disjoint unless identical. Consequently
different owners' enclosed-strip pools are disjoint, even when a pool has
horizontal–vertical crossings within one owner. If H has at least rho_H
eligible enclosed strips after its reserved credits, the same one-unit
allocation can be carried out separately within H. The global theorem
does not need this optional owner condition and also permits runs whose
two bounding components differ or which meet the ambient boundary.
Here positive rho_H is integral: its expression is |T in R_H|+|H|/2-2|R_H|,
and the matching covers H, making |H| even.

## 7. A frozen equality example rules out two credits per strip

In the28endpoint frozen configuration from
[the complete coordinate and ordered-certificate note](REMOTE_DEFICIT_FROZEN_OBSTRUCTION.md),
Sections1-4, and its [exact labels and actual matching](../develop/remote_deficit_frozen_obstruction.json),
the relevant sealed maximal runs are

    horizontal: Q_(3,1),Q_(3,2),Q_(3,3);
    vertical:   Q_(2,2),Q_(3,2).

The first is enclosed by H; the second reaches the ambient boundary.
Both have capacity two. Their only positive-capacity tile is Q_(3,2),
whose actual capacity is two. All other endpoint-free tiles have zero
capacity. Thus

    |S|=2=D,   but   sum_s capacity(s)=4>D=2.

The proposed rule of crediting the full two-unit guarantee separately to
every overlapping strip is false even in a fully frozen representative.
The one-unit global theorem is sharp for the stated overlap information:
the slot allocator gives the two different units of Q_(3,2)to the two
strips. Since rho_H=1, even one of these valid credits pays the positive
receiver, with one unit left.

The source note lists every label, actual matching edge and all28freezing
rows, and computes original receiver charge1and objective39. For direct
maximality checks, the horizontal run is bounded by endpoint tiles
Q_(3,0),Q_(3,4); the vertical run is bounded above by endpoint tile Q_(1,2)
and below by the ambient boundary. Horizontal outer columns2and7in rows6,7
are blank; vertical outer rows4and7in columns4,5are blank. Equality here
means |S|=D=2in the overlap-capacity budget, not equality in the final grid
bound: its final deficit is40-39=1.

The selected-border completion in Section6of that source makes every
endpoint interior, but CHANGES the vertical maximal run. After translation
by(2,2), the horizontal run is Q_(4,2..4), still capacity2. The vertical
maximal run is now Q_(3,3),Q_(4,3),Q_(5,3), capacity4; the new endpoint-free
bottom tile extends it. Both remain sealed; their lengths and capacities
are not both preserved. Exact completion labels and matching are given in
the cited note and JSON. This completion has D=6and objective79<84; only
the original example supplies |S|=D=2. No arbitrary-padding claim is made.

## 8. Verification and limits

The physical scanner identifies maximal runs from endpoint-free tile
intervals, checks their actual blank boundary columns/rows and capacities,
deduplicates run descriptions, then applies reservations before eligibility.
The augmenting-path allocator uses unit copies of actual residual capacity.
Run

    python3 -B develop/check_sealed_strip_allocation.py --output output/sealed-strip-allocation-controls.json

The receipt covers144physical cases across nine fixtures, two reservation
settings and eight symmetries, plus six mixed-component cases. Actual
thick endpoint rings give perpendicular overlaps, including a single
capacity-two tile appearing in both directions. Those rings are
single-terminal, not asserted fully frozen. The remote example supplies
a separate fully frozen sharpness check with two allocations at one tile.

Six local Lean4.33Std-only statements compile: the unit-square selection
bound, arbitrary-length shifted-pair identity and bound, sealed-strip
capacity, and two arithmetic budget lemmas. Their axioms are recorded
explicitly in output/sealed-strip-formal-check.json. Full physical maximal-run
classification, planar owner geometry, double-counting adapter and Hall
allocation remain written proofs, not claimed formalized by these six
statements. No sorry/native_decide is used. The first Oracle review returned
REVISE: it found the core capacity/Hall/reservation proof sound, requested
explicit definitions and the full example dependency, and correctly flagged
the false claim that both maximal runs survive border completion unchanged.
These repairs are incorporated above; a same-conversation follow-up is
pending. This is not a final acceptance. See the
[review assessment](reviews/2026-10-20-sealed-strip-assessment.md).

Universal coverage by the four old corner rules plus capacity-at-least-two
runs is now FALSE: the [32-endpoint capacity-one obstruction](STRIP_INCIDENCE_ALLOCATION_AND_CAPACITY_ONE_OBSTRUCTION.md)
has positive receiver charge, zero corner supply and all maximal runs of
capacity at most one. This does not contradict any conditional theorem here.
The newer exact incidence criterion can safely include degree-one runs;
its general geometric coverage and the grid triple equality remain open.
Non-reuse for the strip collections in this note is resolved by(1)-(4).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
