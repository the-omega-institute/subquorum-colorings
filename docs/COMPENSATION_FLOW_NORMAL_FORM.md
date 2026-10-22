# Exact compensation by vertex-disjoint directed paths

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We prove an exact directed-path formulation of terminal cancellation followed
by one-sided interval allocation. It accounts for the capacity of intermediate
mixed paths as well as final interval and beta resources. Every cancellation
and allocation has a normal form using a subset of its links and paying the
same number of demands. Consequently a minimum-cost integral maximum flow gives
both the largest possible compensation and the fewest links needed to attain
it. The beta-incidence restriction in the earlier degree-two adapter is no
longer needed.

The underlying integral flow and minimum-cut theorems are standard. The result
here is the equivalence with the strand cancellation model, including the
reverse normalization and the grid access adapter. We do not claim a new
general flow theorem.

## 1. Finite strand system and the optimization problem

Let P be a finite set of terminals, partitioned into disjoint unordered pairs
called strands. Every terminal is labelled TP or BP. An alpha strand has two
TP terminals, a beta strand two BP terminals, and a mixed strand one of each.
Let their respective initial counts be k, b and g.

Declare a set E of permitted TP--BP links. Links are between terminals, and a
cancellation C is any terminal matching contained in E. A link joining the two
terminals of one mixed strand is allowed in this definition; it closes an
isolated two-edge cycle and will be unnecessary in a normal form.

Let I be a finite set of distinct unit interval resources, with a fixed access
relation A contained in TP x I. Access depends on the physical terminal and
the interval, not on the identity of the virtual strand owning that terminal.
An access can be used only while its terminal is free of cancellation links.
Each interval can pay at most one final alpha strand. No degree restriction
is imposed on E or A in this abstract theorem.

In the multigraph formed by the original strand edges and C, every component
is an alternating path or an alternating cycle. A path's two free terminals
determine its final strand type. Write b_C for the number of final beta
strands. An interval allocation F assigns distinct intervals to distinct
final alpha strands, using a free TP terminal with the stated access.

Define the compensation value of (C,F) to be

    p(C,F) = b - b_C + |F|.                                  (1)

The first term counts original alpha--beta pairs consumed by cancellation;
the second counts surviving alpha strands paid by intervals. Indeed, in a
component with d original alpha and e original beta strands, the final type
is determined by d-e: it is alpha if d=e+1, beta if e=d+1, and mixed if d=e.
A cycle has d=e. Thus exactly min(d,e) alpha and beta units are consumed in
that component, and b-b_C is the total such consumption. In particular
0<=p(C,F)<=k. A beta strand supplies one unit even if both its terminals occur
in C. Mixed strands have no resource credit.

The optimization ranges over all C and all injective F. Its secondary objective
is the minimum number |C| of links among pairs with maximum p(C,F).

## 2. The directed network

Use a directed multigraph retaining the specific terminal witness on every
link and access arc; different witnesses with the same owner-level endpoints
remain separate arcs. Use one source node for each alpha owner. A mixed owner has an entry node and
an exit node joined by an arc of capacity one. A beta owner is one sink
resource, with capacity one regardless of which BP terminal is entered.
Each interval is also one sink resource of capacity one. Add a super-source
with capacity-one arcs to the k alpha nodes and a super-sink receiving the
beta and interval capacity arcs.

Each TP--BP link is directed from its TP owner's exit to its BP owner's entry.
Alpha owners have exits but no entries, and beta owners entries but no exits.
The two terminals of an alpha may give different outgoing arcs, and the two
terminals of a beta may give different incoming arcs. For a mixed owner its
unique BP and TP are respectively its entry and exit terminals. Discard
self-links on one mixed owner.

Each access (terminal,interval) gives an arc from the terminal owner's exit
to that interval. Link and access arcs have capacity k+1. All link arcs have
cost one; every other arc has cost zero. The capacity k+1 is just a finite
replacement for infinity: an optimal cut has capacity at most k and never
needs to cut one of these arcs.

Let nu be the maximum integral flow value and c the minimum cost among
integral flows of value nu.

**Theorem.** The largest compensation value in (1) is nu. The minimum number
of additional links attaining that largest compensation is exactly c.
An optimal pair can be chosen as a union of owner-disjoint directed paths,
each running from one original alpha to one beta or one interval, with mixed
owners as its internal strand owners.

Here original means relative to the strand system at the start of this
optimization; it can already be the virtual system after a fixed earlier C0.

### Forward direction: integral paths give legal compensations

Remove flow cycles and decompose an integral flow into source--sink paths.
There are nu different alpha sources, nu different sink resources, and the
paths have disjoint mixed owners because their split arcs have capacity one.
No alpha or beta owner can occur in a path's interior. Paths can be chosen
simple. Every directed cycle contains a positive-cost link, so a minimum-cost
flow has no positive flow cycle to begin with.

Replace each link arc on a path by its witnessed terminal link. At an internal
mixed owner the incoming link uses its BP terminal and the outgoing link uses
its distinct TP terminal. Source and beta owners use one terminal each.
Different paths have disjoint strand owners. Thus these links are jointly a
terminal matching, with no reuse of a terminal or intermediate strand.

A path ending at beta merges one alpha, one beta and its intermediate mixed
strands into a mixed strand, consuming one alpha and one beta. A path ending
at an interval merges one alpha and its intermediate mixed strands into an
alpha strand whose final free TP has the declared access. Allocate its sink
interval to that strand. The interval is distinct from all other path sinks.
Hence each path pays one demand, and the resulting value is nu. The number
of chosen terminal links is exactly the flow cost.

### Reverse direction: normalize an arbitrary cancellation

Fix C and F. In each component of the strand--C multigraph, suppress the
mixed owners, retaining the alpha and beta owners and the mixed segments
between them. Every segment between retained owners has one alpha and one
beta endpoint, and is directed from alpha to beta. To see this, start at
either terminal of an alpha. Its link enters a BP; at every mixed owner the
strand leads from that BP to its unique TP, whose next link again enters BP.
The next nonmixed owner must therefore be beta. The same argument in reverse
applies starting at beta.

Consequently the retained owners form an alternating alpha--beta path or
cycle, with the possible empty or single-owner cases. Each segment's mixed
interior is disjoint from every other segment. There are also disjoint tails
from a retained end owner to a free terminal, when a path has such tails.

If the component is a cycle, it contains equally many alpha and beta owners.
Choose alternate edges of its compressed even cycle, including the case of
two owners joined by parallel segments. This matches every alpha and beta
once. The selected segments give min(d,e) owner-disjoint alpha--beta routes.
A cycle containing only mixed owners contributes zero and is discarded.

If the component is a path and is not interval-paid, choose a matching of
the compressed alternating path covering its smaller owner class. Explicitly,
when the class sizes are equal, pair consecutive owners starting at one end;
when they differ by one, leave an end owner of the larger class unmatched
and pair the rest consecutively. These segments again give min(d,e) routes.
This includes components with one retained owner or no retained owners.

If the component is interval-paid, it is a final alpha: d=e+1. Choose the
free TP endpoint witnessing its allocated interval. Trace its tail backwards
through mixed owners to the first alpha owner. Reserve that alpha and tail
as a directed alpha--interval route, with zero links if the free tip already
belongs to that alpha. Removing this end alpha from the compressed path
leaves an alternating path with e alpha and e beta owners. Pair its owners
consecutively. This produces e alpha--beta routes in addition to the one
alpha--interval route. All chosen segments and the reserved tail are disjoint.

These constructions give exactly min(d,e), plus one for an interval-paid
component, routes from the component. Different components have disjoint
owners, and F uses distinct intervals. Taken together they give p(C,F)
feasible directed routes. Every link used is already in C; none is added.
This proves nu>=p(C,F), and proves the stronger subset-of-links normalization.
The forward construction proves the opposite optimum inequality.

For the cost assertion, normalize any optimum (C,F). Its selected routes
give a flow of value nu and cost at most |C|, so c<=|C|. Conversely a
minimum-cost maximum flow gives an optimum cancellation with exactly c
links by the forward construction. This proves both assertions.

## 3. Exact obstruction by unit separators

A unit separator Z is any set of mixed owners and sink resources (beta owners
or intervals). Delete these objects from the directed network before adding
the super-source and super-sink. Let U_Z be the alpha sources with no directed
route to any surviving resource. Then

    k-nu = max_Z (|U_Z|-|Z|).                                (2)

The maximum is nonnegative, since Z empty is allowed. Full compensation is
possible exactly when |U_Z|<=|Z| for every Z.

Proof. In any disjoint route packing, routes from U_Z must meet Z. At most
|Z| such routes exist, since each deleted mixed owner and sink resource has
unit capacity. At most k-|U_Z| other routes exist by source uniqueness. Thus
nu<=k-|U_Z|+|Z| for every Z.

For equality choose a minimum source--sink cut. Its capacity is at most k,
so it cuts no arc of capacity k+1. Let Z consist of mixed split arcs crossing
the cut and sink-resource arcs crossing it. Let H be the alpha source nodes
on the source side. After Z is deleted, no alpha in H can reach a surviving
resource: otherwise that route crosses an uncut capacity-k+1 arc or reaches
a resource whose sink arc also crosses the cut. Hence H is contained in U_Z.
The cut capacity is k-|H|+|Z|. Combined with the upper bound just proved,

    nu <= k-|U_Z|+|Z| <= k-|H|+|Z| = nu.

All inequalities are equalities, proving (2). This is a node-splitting
application of integral max-flow/min-cut; the strand equivalence is Section 2.

Checking only sets of reachable sink resources misses intermediate capacity.
For an abstract example, take two alpha sources both linked into the same
BP terminal of one mixed strand, whose TP can access either of two distinct
intervals. Both sources reach both intervals, so the ordinary reachable-resource
Hall tests pass. Yet at most one route can use that mixed owner. Deleting
that owner gives |U_Z|=2 and |Z|=1, and the exact deficit is one. This is an
abstract strand example, not a claimed frozen grid realization.

Likewise any number of alpha owners may have candidate links into a beta
resource. Its one sink-capacity arc still permits only one unit. For example,
four alpha owners can all link to one BP terminal of one beta strand; maximum
compensation is one. No candidate-owner truncation is needed for this theorem.

## 4. Fixed earlier links and a protected paid core

If C0 has already been fixed, replace its alternating path components by
virtual strands on their free terminals and discard its closed cycles. Keep
only links between these free terminals. The virtual strands are disjoint,
and any further matching extends C0 legally. All statements above apply to
additional compensation and additional link costs in this current system.

To preserve an existing interval-paid core literally, declare its current
alpha owners protected: forbid every further link touching either terminal
of such an owner, reserve their assigned intervals, and remove these owners
and intervals from the residual optimization. The theorem is then exact for
this restricted class of extensions. Its forward routes do not alter the
protected owners, their free terminals or their assigned physical resources.

This restriction is sufficient for safe preservation; it is not asserted
equivalent to every possible strategy that keeps the same total payment.
Some improvements may require reassigning the old interval allocation. Using
the unrestricted network allows such reallocation while still counting every
owner and resource at most once.

## 5. Physical grid adapter and the residual ledger

Take a matching-closed aligned packet as in the one-sided allocation note.
Its strand terminals and TP/BP labels give P; E consists of the permitted unit
horizontal adjacencies between opposite-label free terminals in the same band.
I consists of its distinct unmarked physical BB--TT interval resources. An
access is either direct TP--BB access or TP--BT--BB access with the selected
BT mediator in the endpoint's physical row. Physical access remains unchanged
when the free terminal changes virtual owner. Each allowed cap mediator has
one candidate terminal user, as proved in the earlier selected-cap adapter,
so the route construction introduces no extra cap-capacity conflict.

The theorem therefore applies to all such terminal matchings, with arbitrary
mixed relays and without imposing a two-owner condition on beta incidence.
It does not permit new nonterminal links, links into used terminals, access
across bands, marked intervals, or additional credit from mixed owners.

Write r=|I|+b. The physical identity S-B=r-k is unchanged by cancellation.
After an optimum normal form, let Q=r-nu be unused units from this original
interval/beta resource pool, and delta=k-nu its unpaid alpha count. Then

    S-B = Q-delta,
    delta = max_Z (|U_Z|-|Z|).                               (3)

Resources of Q keep their physical identities; an unreachable interval is
not automatically available to repair another source. Full routing is one
sufficient compensation certificate. More generally the original target is
Q>=delta, which need not require full routing. For disjoint physical packets
the earlier outside overlap correction is still required exactly once.

The theorem is an exact reduction, not a proof that every frozen grid satisfies
all the separator inequalities. Establishing the needed geometric cut bound
or the weaker budget Q>=delta remains the general grid problem. No universal
improvement of the existing 5/6 bound follows without that additional argument.

## 6. Repair of the physical shared-donor collision

The earlier collision family consists of two relay_family(W,4,1,1) copies,
the second shifted ten columns, for every even W>=8. Use its packet
(W+2) by 22, and put R=W+4. The prescribed first link is

    (5,5)--(5,6).

There are two unpaid alpha owners. Their two upper continuations

    (5,7)--(5,8),       (5,15)--(5,14)

both expose the same upper-band singleton BB11, so those chosen continuations
alone can never pay both demands. This remains a valid rule counterexample.

The full network nevertheless pays both demands. In the lower band use

    (R,5)--(R,4),       (R,15)--(R,14).

The first exposes TP(R,3), cap(R,2), singleton interval BB1. The second exposes
TP(R,13), cap(R,12), singleton interval BB11. Both intervals are unmarked:
they are singleton intervals with BT on their accessed side, and neither is
a boundary interval at column 0 or 21. They are distinct resources in the
same lower band. The two routes use different mixed owners and are disjoint
from all prescribed upper links. Thus these two lower links pay both demands
for every allowed W. Initially no alpha tip has an unmarked access, so at least
one link per alpha is necessary; the exact additional cost is two.

After either upper continuation, one demand already accesses upper BB11 and
one lower link pays the other demand, so the exact additional cost is one.
After both upper continuations, allocate upper BB11 to one alpha and expose
a lower interval for the other with one link. Zero further links cannot pay
both through their single shared resource. Hence in the four continuation
states the exact costs of full compensation are 2,1,1,1.

For the arbitrary-length shared chain, all r demands are similarly paid with
one additional link, retaining the earlier explicit root repair. The protected
repair uses the specific old allocation assigning the shared interval between
demands i and i+1 to demand i+1, leaving demand 0 unpaid. The checker explicitly
identifies this root-0 allocation before protecting it. Other old maximum
allocations need not admit a protected repair. For
fixed-height relay_family(8,4,L,L), maximum compensation is
one and its minimum link cost is L, recovering the all-length distance theorem.

## 7. Verification scope

The permanent checker compares the flow optimum and its minimum link cost with
independent terminal-matching enumeration. It independently reconstructs free
tips and final components, then solves the final interval matching problem.
Every returned flow is reconstructed as actual terminal links and interval
allocations and checked with the established cancellation inventory code.
Residual cuts are checked by independently recomputing the blocked sources.

Current execution covers 15,033 flow models and 1,242,432 independent terminal
matchings; 14,998 models have exhaustive matching comparisons. The abstract
tests exhaust canonical strand-type multisets through three owners, every
permitted-link subset and every one-interval TP-access subset with an alpha
present, and add 400 deterministic multi-resource tests. There are 402 complete
separator checks, totaling 6,172 deletion subsets. Physical controls cover
83 systems from 59 frozen uniquely matched grids, including 32 occupied-band
adapters, relay depths through 64, shared chains through 24 copies, all four
donor-collision states, 12 explicit lower-route repairs, and 102 protected
already-paid alpha owners. These
controls support the general written proof; they are not its premises.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_compensation_flow_normal_form.py --output output/compensation-flow-normal-form-validation.json

A later geometric probe checks 432 completely frozen images: both actual
matchings of the bent fixture, four tile alignments under all eight grid
symmetries, occupied bands, capacity-two rotors, branched stars, and connected
branched chains through eight modules of stars. Of these images, 206 have
nonempty alpha demand; all of them have full allocation at zero additional
link cost. Thus this probe supplies no new obstruction requiring mixed relay
transport. A separate degree-four control is not completely frozen and its
32 images are excluded explicitly. These are finite geometric controls,
not a general route-existence theorem or part of the original review input.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_compensation_flow_geometry_frontier.py --output output/compensation-flow-geometry-frontier.json

The separate standalone Lean source formalizes the route uniqueness and finite
separator-counting interface, uniqueness of reserved and newly used resource
lists under supplied disjointness assumptions, and the
exact resource ledger. The full alternating-component normalization, integral
flow theorem, minimum-cost argument and grid geometry remain written proofs.
The submitted manuscript is preserved; this is a research note for a later
proposed addition after checking and review.
