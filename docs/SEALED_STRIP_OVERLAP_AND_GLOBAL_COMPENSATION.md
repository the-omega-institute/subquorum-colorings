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
For Q in Z write

    d_Q=2-|T intersect Q|.

Every unit square contains at most two selected vertices: any three have
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
integer amounts a_Q with0<=a_Q<=d_Q at physical tiles, each amount assigned
at most once. Let B=sum_Q a_Q and r_Q=d_Q-a_Q. A strip may be used in the
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

An exact weighted variant is also available: for any distinct maximal
runs with residual capacities C_s, the subset sum gives

    sum_s floor(C_s/2) <= sum_Q r_Q.

Replace each strip by floor(C_s/2) identical requests and apply the same
slot argument; each subcollection of requests is dominated by the subset
inequality for its support strips. The one-unit statement is sufficient
for the examples here.

## 5. Consequence for the original complete-receiver ledger

Now assume single terminality. The established tile-ownership lemma makes
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
proves the half-area bound, hence the existing lower bound identifies the
grid coloring value in the corresponding optimization argument. It does
not improve the unrestricted five-sixths bound: proving(5)for all relevant
representatives remains open. An arbitrary feasible pair meeting(5)alone
does not imply that every optimum has such a representative.

## 6. Optional ownership from planarity

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
tile center. Its other interior tiles are endpoint-free, and its K
endpoints are outside R_H, so no further intersection is possible.

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

## 7. A frozen equality example rules out two credits per strip

In the28endpoint frozen configuration from
REMOTE_DEFICIT_FROZEN_OBSTRUCTION.md, the relevant sealed maximal runs are

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

The selected-border completion makes all endpoints interior and retains
these two runs and their local capacities. It has extra resources elsewhere;
the original uncompleted example supplies equality for the total budget.

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
statements. No sorry/native_decide is used. No Oracle review of this new
strip theorem has yet been obtained.

The open task is structural sufficiency: enough reserved capacity and
eligible maximal strips must cover the total corrected receiver charge,
or a new representative transformation must supply that property. The
non-reuse issue for any such strip collection is resolved by(1)-(4);
the unrestricted coverage problem and grid triple equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
