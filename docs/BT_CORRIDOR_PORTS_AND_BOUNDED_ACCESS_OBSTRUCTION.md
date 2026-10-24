# Extreme-interval compression, BT corridors and an exact access obstruction

25 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The main result is an exact compression of the endpoint-free gap model:
**one available interval at each side of a gap suffices to preserve every
simultaneous interval payment**, including its paying terminal and all chosen
terminal links. Consequently maximum compensation and its minimum link cost
are unchanged. This holds with arbitrary fixed interval reservations when
the extremes are recomputed among the available units. With only the original
boundary reservations, the compressed accesses are precisely direct BB accesses
and accesses through a consecutive BT corridor to its first BB column.

We also give a smaller three-parameter fully frozen obstruction to bounded
BT access, with an exact two-link repair and a concrete Lean certificate.
The impossibility of any fixed access radius was already proved in
[the endpoint-free gap note](ENDPOINT_FREE_GAP_COMPENSATION.md), Section 3;
that impossibility is not a new theorem here. The new reduction explains why
the full gap model needs neither dense terminal-to-interval access nor a
separate resource for either side. It does not establish universal coverage
by gaps or improve the unrestricted 5/6 bound.

## 1. Hypotheses and original resource identities

Use the feasible pair (T,M), actual endpoints P, matching-closed aligned
two-row packet J, and original BB--TT interval forest from
[the terminal ledger](TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md).
A gap is a maximal consecutive set of columns in one band containing no P.
It contains only BB, BT and TT columns. Every original interval is a connected
BB--TT component, has a contiguous column span, begins and ends in BB, and
belongs to exactly one gap. Different spans in a gap are disjoint and linearly
ordered. These facts follow directly from TT having two BB neighbors and
the interval edges joining adjacent BB and TT columns.

Let L be the original interval count, B the number of distinct marked boundary
intervals, and F any additional fixed set of reserved original intervals.
The available set is I = all intervals minus (boundary marks union F).
These are original unit identities: a unit seen from two sides remains one unit.
No beta or mixed strand is an interval unit.

Fix ANY matching C of permitted opposite-label original terminal links.
After cancellation, a surviving virtual alpha may be paid at one of its free
TP terminals. Full gap access lets such a terminal use any available original
interval in either immediately adjacent gap. Each terminal is in a column
with just one endpoint. Therefore a gap has at most two candidate terminals,
one at either end. This property holds before and after C, independently of
freezing, actual path bends and the number of occupied bands elsewhere.

## 2. Exact compression theorem, including reservations

For each gap G with at least one available interval, order its available
units left to right. Keep only this access from each candidate terminal:

* the terminal on G's left accesses its LEFTMOST available unit;
* the terminal on G's right accesses its RIGHTMOST available unit.

Empty gaps supply no access. A terminal may retain one access in each of its
two adjacent gaps, so it has at most two compressed targets in total.

**Theorem 1 (extreme-interval compression).** For every fixed C and every
injective full-gap payment of surviving virtual alphas, there is a compressed
payment of exactly the same virtual alphas at exactly the same free terminals.
All links of C are preserved. The reverse inclusion of feasible payments is
immediate. Thus full and compressed gap access have the same maximum payment
for each C, and the same maximum total compensation and minimum link count
when C also varies. The result holds for any fixed F.

**Proof.** Group the old interval payments by their gap. Since a free terminal
can pay only its one virtual alpha, and G has at most two candidate terminals,
each group contains at most two payments.

If G supplies no payment, do nothing. If it supplies one, move that payment
to the extreme available unit nearest its existing terminal. If it supplies
two, they must use the two different candidate terminals. Their old targets
were distinct, so G has at least two available units. Its first and last
available units are therefore distinct. Assign these respectively to its
left and right candidate. This keeps both payments and both witnesses.

Within a gap the new targets are different. Between gaps they are different
because every original unit belongs to exactly one gap. No link, free
terminal, virtual alpha or beta consumption has changed. Thus no unit or
strand is reused. Since compressed accesses were full-gap accesses, both
directions follow for each C. Maximizing the compensation value
beta-beta_C+number_of_interval_payments and then minimizing |C| proves the
two optimization equalities. QED.

In the directed normal form this can be performed by changing only the last
interval target of each paid route. Original sources, mixed gates, witnessed
links and link costs stay fixed. In particular any fixed forbidden mixed
gates or allowed-source subset can be retained in the theorem. The result
does not assert that a particular old interval remains used, or that an old
source-to-interval assignment remains fixed. Additional reserved units must
be removed BEFORE computing the available extremes.

**Why reservations matter.** A gap with ordered units J1,J2 and one left
candidate has compressed target J1. Reserve J1. Full gap access can still
pay through J2, but deleting J1 from the OLD compressed graph loses that
payment. Recompute the available extreme to obtain J2. This refutes the
fixed-nearest-target-after-deletion rule, not compression with recomputation.
Similarly, giving BOTH sides the same first unit would lose a valid pair
of payments when two units are available. The theorem uses opposite extremes,
and never gives separate side credits for a single unit.

The uniform bound of two candidate targets for a gap is sharp: the previously
constructed physical two-port/two-unit gap pays both terminals. The result
is a resource-interface reduction, not a proof that every source has a route.

## 3. Boundary reservations give precisely first-BB BT corridors

Assume now F is empty. From a TP terminal look into an adjacent gap, skip
its consecutive BT columns, and take the first BB column, if there is one.
Keep its original interval if it is unmarked. Call this a BT-corridor access;
zero intervening BT columns gives direct access. If there is a first BT
column, its selection is in the terminal's row: the terminal's selected
vertical partner already sees that endpoint and cannot also see a horizontal
selection. No alternating-row condition on the entire corridor is needed.

**Theorem 2 (exact boundary-reserved specialization).** These BT-corridor
targets are exactly Theorem 1's available extremes. Thus the sparse BT graph
and full gap graph have the same maximum compensation and minimum link cost.

**Proof.** A TT column cannot be the first non-BT column met from TP: a TT
adjacent to TP is infeasible, and a TT adjacent to BT is infeasible because
every TT has two BB neighbors. The first interval met from that side begins
at the first BB, reached across BT alone. It is the first interval in the
gap's linear order from that side.

An internal gap has no boundary marks, so that interval is available.
A gap touching a packet end has at most one candidate terminal. If it has
a boundary mark, its marked interval is the opposite, outermost interval.
If the nearest interval is marked, it is therefore the only interval in
that gap and no available target exists. Otherwise the nearest interval is
the nearest available one. Gaps spanning the entire band have no candidate
terminal. This exhausts the cases. QED.

**Unique-side ownership and exact connector ledger.** For either side of an
interval, follow its adjacent maximal BT run outward. There is at most one
TP column at the far end and just one candidate terminal in it. This proves
that each interval side has at most one corridor user, simultaneously over
ALL candidates, before any connector selection. A nonempty BT corridor is
also owned by at most one candidate: a maximal BT run must have TP at one
end and BB at the other. Different bands have disjoint columns.

Consequently chosen two-ended virtual-alpha connectors have interval degree
at most two; a marked boundary interval has degree at most one. With alpha',
beta' the post-C inventory, u the virtual alphas omitted from connectors,
and h_j the connector PATH components with j marks, including isolated
vertices, the unchanged exact identity is

    S_J - B = h_0 + beta' - h_2 - u.

This follows from S_J=L+beta'-alpha', L-(alpha'-u)=h_0+h_1+h_2 and
B=h_1+2h_2. Connector cycles have zero Euler contribution. It is the earlier
connector theorem with its access adapter extended to arbitrary BT runs.
One-sided resource allocation and two-ended connectors are different uses
of this geometry; having a route to one interval does not erase a two-ended
connector's u or h_2 debit without the corresponding construction.

## 4. A small obstruction with exact repair cost

Take even W>=6,H>=4 and any integer d>=2. Start with direct_family(W,H) in
[the terminal cancellation note](TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md),
Sections 3 and 8, whose complete coordinate lists and serial freezing and
unique-matching proofs are retained. Put R=W+4. Add these 2d selections:

    (4,1), (R+1,1);
    (5,7+j) if j is odd, (4,7+j) if j is even, j=2,...,d;
    (R,H+3+j) if j is odd, (R+1,H+3+j) if j is even, j=2,...,d.

Every added selection is isolated from all old occupied vertices and every
other addition. Consecutive new right selections alternate rows, and the
nearest additions are diagonal to the old cap. Their vertical and horizontal
outside neighbors are blank. Feasibility follows. P and M have not changed,
so the old forced-leaf matching proof and every old freezing witness still
apply. The actual matching remains unique and all endpoints freeze.

Let epsilon=d mod 2 and n=H+d+6+epsilon, which is even. Take J to have rows
4,...,R+1 and columns 0,...,n-1, a union of whole original tiles. All original
receiver tiles and all additions lie inside. Its first and last columns are
BB in every band. Direct counting gives

    |T|=H+9+2d,       |M|=W+H,
    alpha=1, beta=0, mixed=H+1, B=W+2,
    S_J-B=(W/2-1)(H+d)+W-5+(W/2+1)epsilon >= 13.        (1)

The original alpha has tips (5,3),(R,3). Every horizontal route from it
stays in the following two rows: upper TP columns 3,5,7; lower TP columns
3,5,...,H+3. A link from TP at c enters the BP at c+1 of a mixed one-edge
strand and exits at TP c+2. A link back into its own mixed strand is a
discardable self-cycle. No beta or other reachable row exists.

The new BT column1 blocks the former left single-cap exit. Under unbounded
BT access the only left target is BB0, a marked unit, so it still cannot
pay. At the upper right terminal (5,7), columns8,...,7+d are BT and
column8+d is BB. At the lower right terminal (R,H+3), the corresponding
first BB is H+4+d. Both are unmarked singleton original intervals; each
has another BB before the packet's final marked column. Earlier TP tips
have endpoint columns on their right and cannot skip those to reach a gap.

Thus every BT-access bound shorter than d intervening columns has
maximum compensation0 and deficit1, even with arbitrarily many horizontal
links or reassignment. This includes the old direct/single-cap model.
For arbitrary fixed bound K, choose d>K. No finite enumeration proves this
quantifier; it follows from the preceding exhaustive route closure.

Unbounded BT access pays the sole demand through the upper terminal after
exactly these two links:

    (5,3)--(5,4), (5,5)--(5,6), then access from (5,7).

The two mixed owners and one original interval are distinct. Zero links
reach only the two old alpha tips, which have no unmarked target. One link
reaches upper or lower TP5, again with no target. Hence maximum compensation
is1 and its minimum link cost is EXACTLY2 for all W,H,d. By Theorem 2 this
is also the exact optimum of the FULL gap model, not just a sparse subgraph.

If a two-ended connector is required instead, advance both ends: use the
two upper links and lower links (R,c-1)--(R,c), c=4,6,...,H+2. The resulting
virtual alpha has free tips (5,7),(R,H+3), each with its displayed unmarked
target. The two resources are in different bands. Thus u=h_2=beta'=0 and
h_0=S_J-B. The minimum number of links for this two-ended-unmarked connector
is EXACTLY 2+H/2: each end must traverse its row's entire mixed chain, and
the original alpha is the only strand joining the two reachable rows. All
horizontal cancellation components without that alpha have net charge zero.

For W=6,H=4,d=2 the packet is8 by12, with17 selections,10 matching edges
and20 endpoints. Its target margin is13, old compensation is0, full-gap
compensation is1 at two links, and the two-ended connector needs four links.
The failure concerns a restricted access rule, not the target inequality.

## 5. Verification and formal scope

The deterministic verifier reconstructs actual strands, interval identities,
maximal gaps and physical BT corridors. It compares the full and compressed
maximum flows and minimum link costs, then transports the full optimum's
actual interval payments while preserving its original link set and paying
terminals. Reservations include empty, first-unit, last-unit, alternating-unit
and all-unit patterns. It separately checks a physical two-port capacity-two
gap and a TT forest, preventing the check from relying only on isolated BBs.

The run passes 1840 optimization/transport controls on 592 fully frozen geometry
controls, including 280 parameter families, 24 isometries of the obstruction
and 288 carried configurations. Across 592 boundary-only adapters, first-BB
BT targets equal the computed available extremes exactly. It checks 1560
reservation patterns and 9727 abstract reserved payment transports. The full
gap adapters expose 19736 access occurrences, reduced to 4793; these are totals
over controls, not a universal compression factor. It transports 888 actual
interval payments without resource reuse.

The Lean companion checks 16 theorem audits with ordinary kernel reduction,
without sorry or native evaluation. These cover the two-side compression's
injectivity and available-target mechanism, the general strict-rank freezing
criterion, the concrete geometry and all 20 frozen endpoints, the complete
open-path/pure-cycle decomposition, arbitrary finite original relay closure,
absence of every old exit, a two-link exit, and the margin13 count. The two
coincident actual/vertical PP cycles are retained explicitly; dropping them
would omit four endpoints from the concrete decomposition.

Physical gap ordering, its at-most-two candidates, the global lifting and
optimization equivalence, and the all-parameter construction and exact costs
are the written proofs above. No new external independent review is claimed.
The broader frozen-grid inequality, outside-receiver budget and 5/6 improvement
remain open. The submitted manuscript is unchanged.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_bt_corridor_ports.py --output output/bt-corridor-ports-validation.json
    cd formal && lean SubQuorum/BTColumnCorridorObstruction.lean

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
