# One-sided interval and whole-beta allocation

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We give an exact maximum allocation theorem for a system in which a resource
has at most two demand owners. Applied to the full selected-cap access relation,
it pays alpha paths using just ONE accessible unmarked interval per demand;
both terminals need not have ports. It identifies every local allocation
obstruction as a tree component with no singly owned resource, contributing
exactly one unpaid demand. Original beta paths can be included in the same
resource graph under an explicit incidence hypothesis, counting each whole
path once. This is a conditional compensation theorem, not a general proof
of the grid inequality.

The allocation argument is elementary graph matching. Its role here is to
give a precise grid resource adapter and explicit frozen applications.

An explicit completely frozen grid family realizes arbitrarily long deficient
chains. Every demand has an accessible interval, but these candidates number
one fewer than the demands. One additional horizontal link exposes a previously
unused interval and pays the entire chain without repeated resources. A second
application separates mere two-end access from access to a usable unmarked
resource, with an unbounded difference at fixed height ten.

## 1. Exact allocation with resource degree at most two

Let D be a finite set of demands and R a finite set of unit resources. Specify
an incidence relation in which each resource is incident to zero, one or two
DISTINCT demands. A valid allocation assigns some demands to incident resources,
injectively. Different resources with the same pair of owners remain distinct.

Form a multigraph on D. A resource incident to two demands is one edge joining
them. A resource incident to one demand is recorded at that vertex; it is not
an ordinary edge. An unused resource belongs to no demand component. A resource
accessible at two ports of the SAME demand is singly owned, not two credits.

Call a connected component deficient if its multigraph is a tree and it has
no singly owned resource. An isolated demand with no resource is included.
Let t be the number of these components. Then the maximum number of demands
that can be assigned is EXACTLY

    |D|-t.                                                     (1)

There is a constructive allocation leaving one chosen root unpaid in each
deficient component and paying every demand in every other component.

Proof. In a component with n vertices, choose an ordinary spanning tree.
Its n-1 edge resources pay the nonroot vertices by their parent edges, each
resource once. If there is a singly owned resource, root the tree at its
owner and use it to pay the root. If there is an ordinary edge outside the
spanning tree, choose one such resource e. Root at an endpoint of e and use
a spanning tree avoiding e, which exists because the original tree avoids e.
Pay the root with e and all other vertices with their parent edges. This also
covers parallel-edge cycles. Thus every component that is not deficient is
fully paid. In a deficient component its entire neighbourhood consists of
exactly n-1 resource owners, so an injective allocation of all n demands is
impossible; the parent-edge construction attains n-1. Resource owners cannot
belong to two different components, since a two-owner resource would join
them. Summing proves both optimality and the absence of cross-component reuse.

If Q is the set of resources unused by this maximum allocation, then

    |R|=|D|-t+|Q|.                                           (2)

Resources in Q retain their individual identities; cycles contribute no
additional credit. This theorem makes no claim that an arbitrary external
demand can access every resource in Q.

## 2. The grid adapter and conditional compensation

Use a matching-closed aligned two-row packet J, actual matching M and selected
set T as in the terminal-cancellation note. The first column in each band is
BB and the last has a blank. Let L be its number of BB--TT interval vertices,
B the number of distinct interval resources carrying boundary marks, and S its
exact surplus. Multiple boundary marks on one interval exclude that resource
only once. The displayed frozen families have distinct interval resources
for their boundary marks. For any permitted
opposite-label terminal matching C, let alpha',beta' be the virtual inventories.
The established identity is

    S-B=(L-B)+beta'-alpha'.                                  (3)

Take D to be ALL virtual TP--TP paths, including those lacking one or both
ports. Take R to be ALL unmarked interval vertices. A path is incident to an
interval if EITHER free TP terminal can access it directly or via an allowed
TP--BT--BB cap. All accesses remain inside J, with the selected mediator in
the endpoint's physical row. Keep all candidate choices, rather than choosing
one connector at each end first. Boundary-marked intervals are excluded.

A resource has at most two distinct demand owners. Indeed each interval side
has at most one candidate terminal user: its immediately exterior column is
either TP (direct access), or BT with one possible TP user one column farther
out (cap access). These cases are exclusive. The two sides therefore supply
at most two terminals; a free terminal belongs to only one virtual alpha.
If both belong to the same alpha, the resource is still one singly owned unit.
The cap mediator itself supplies no extra unit. This argument needs no
straightness, mate orientation, matching uniqueness or freezing assumption.

Apply (1). If q=|Q| denotes its unused interval count, (2) and (3) give the
EXACT ledger

    S-B=q+beta'-t.                                           (4)

In particular, if every demand component contains a cycle or a singly owned
unmarked interval, t=0 and S>=B. More generally, the remaining count to pay
is t, not the number of missing terminal ports. Formula (4) is an exact
counting reduction; it does not assert that t<=q+beta' always holds.

A convenient sufficient condition is that each demand has at least two
DISTINCT unmarked interval neighbours. A deficient tree on n vertices has
total demand degree 2(n-1), and so cannot have degree at least two at every
vertex. Hence t=0. Two usable neighbours can come from one free terminal;
there is no requirement that each terminal separately have a port.

The physical global adapter still requires disjoint packets and complete
original receiver closure, and retains the outside overlap correction2N_out.
Nothing here makes that correction disappear or licenses mixing physical
intervals from different tiling alignments.

## 3. Original beta paths in the same resource graph

There is also a unified version BEFORE cancellation. Use original alpha paths
as demands, and the disjoint union of unmarked intervals and ORIGINAL beta
paths as resources. Every interval has the same at-most-two owner property.
For each beta resource declare a witnessed subrelation with at most two distinct
original alpha owners, each with a certified original TP--BP horizontal link
into that beta path. Every incidence records both terminal witnesses. Candidate
links need not all be mutually disjoint: the injective allocation selects at
most one link per alpha owner and per whole beta resource.
A fixed matching of such terminal links is one sufficient way to supply this
list. Do not include all possible beta neighbours without checking this degree
condition: two BP terminals alone do not imply at most two candidate owners
when several alternative links are retained.

The same allocation theorem applies. Its resource count is L-B+beta and its
demand count alpha, so the exact ledger is now

    S-B=q-t.                                                 (5)

One beta path supplies one resource even when both ends have candidate links.
For each demand allocated to a beta path, execute ONE certified link. The
chosen links form a terminal matching: distinct allocated demands have disjoint
original alpha terminals, distinct beta resources have disjoint BP terminals,
and no alpha or beta owner is selected twice. Each such component contains
one alpha and one beta, becomes mixed, and consumes both counts by one.
Leave the remaining proposed links unexecuted. Demands allocated to intervals
are untouched by these cancellations and retain their original access.

This explicitly realizes the hybrid allocation, with no double use of an
interval, beta owner or terminal. Mixing ORIGINAL beta resources with the
post-cancellation beta' inventory would be incorrect; (4) and (5) are two
alternative representations. Mixed paths are never resources in either one.
The degree-two beta hypothesis is sufficient, not asserted universally.

## 4. A frozen shared-resource chain of arbitrary length

For every even W>=6 and r>=2, take r translated copies of direct_family(W,4),
copy i shifted horizontally by8i for 0<=i<r. Preserve their selections and
actual matching edges. Consecutive copies have an empty separating column;
all selected occupied degrees remain unchanged. The old freezing certificates
replay independently, and the endpoint graphs are disjoint unions of the
uniquely matched old endpoint graphs. Thus the union is feasible, completely
frozen and uniquely matched for every W,r.

Take the compact packet rows4..W+5 and columns0..8r+1. It consists of complete
physical tiles and includes every original receiver. Both extreme columns
are BB. Direct counting gives

    dimensions (W+2) by (8r+2), |T|=13r, |M|=(W+4)r,
    S=(3W-9)r+W+2, B=W+2, S-B=(3W-9)r>0.                    (6)

Each copy's alpha has free terminals in rows5 and R=W+4, initially at local
column3. A row endpoint may be placed in one of three states by links internal
to that copy:

    left:   no link, free TP3, cap2 to BB1;
    middle: TP3--BP4, free TP5, no direct or cap access;
    right:  TP3--BP4 and TP5--BP6, free TP7, cap8 to BB9.

Add8i to each column in copy i. For each adjacent pair i,i+1 choose the upper
band if i is even and the lower band if i is odd. Put copy i's endpoint in
that band in the right state, and copy i+1's endpoint there in the left state.
The alternating band choices give each interior copy one left and one right
endpoint. Put the unused endpoint of the first and last copies in the middle
state. Exactly2r disjoint links have been used. There remain r alpha demands,
zero beta, and3r mixed paths.

The pair i,i+1 shares exactly the unmarked singleton interval at column9+8i
in its chosen band. It is accessed from TP7+8i via BT8+8i on the left, and
TP11+8i via BT10+8i on the right. Its adjacent columns are BT, not TT, so it
is a separate interval vertex. The middle endpoints have no other access.
The demand resource graph is therefore EXACTLY a path on r demands with r-1
edge resources and no singly owned resource. All demands have at least one
unmarked interval neighbour, yet a full allocation through those candidates
is impossible. Its entire path is the explicit Hall witness r>r-1.

This disproves the candidate rule "one accessible interval per demand is
enough" in a completely frozen physical configuration, not just an abstract
incidence model. The target inequality is strictly true by (6).

The obstruction concerns these virtual demands after the displayed C. It is
not an obstruction to choosing another C: with C empty, every original alpha
already has its two left-cap intervals, singly owned by that demand. No
claim of an unavoidable grid-wide allocation obstruction is made.

Now add just the link (R,5)--(R,6), in the first copy's previously unused lower
row. Its free terminal moves fromTP5 toTP7 and accesses lower BB9 through
cap8. That interval is unmarked and has no other demand owner: the second
copy's lower endpoint is either middle (r=2) or right (r>2), not left. This
exposes exactly one singly owned resource in the same connected chain.

Assign the new lower BB9 to demand0, and the shared interval between i and
i+1 to demand i+1. This pays all r demands with r distinct real intervals.
One extra cancellation link therefore resolves an arbitrarily long chain.
No beta resource is used. One alpha still lacks access at its other endpoint;
the ordinary two-ended connector omission remains1, while this allocation
has t=0. Before and after, (4) reads respectively

    S-B=(S-B+1)-1,       S-B=(S-B)-0.

The extra link exposes an EXISTING unused interval; it creates no new credit.

## 5. Fixed height: access distance and payment distance differ

In relay_family(8,4,L,L), L>=3, the compact packet is10 by(2L+10), with
|T|=4L+13, |M|=2L+14 and S-B=4L+13. Both right cap targets are boundary
marked. Both left cap targets are unmarked and require L links each. There
is one demand and zero beta.

Its exact minimum costs are:

    two-ended direct-or-cap access:                    4;
    allocation to one accessible unmarked interval:    L;
    two-ended access with h2=0 (no twice-marked connector): L+2.

Proof. Every interior TP tip has BP neighbours on both sides, so it has neither
direct nor selected-cap access. The only cap exits are the two far tips of
each relay row. Each right exit is two gates away, so four links expose both endpoints;
the resulting connector has two marks and no unmarked paying neighbour.
To reach any unmarked interval, at least one row must reach its left exit,
which requires L links by the established simple-chain argument. Moving only
one endpoint left attains that cost and pays the demand, although its other
endpoint remains unported. For a two-ended connector with h2=0, at
least one end must go left and the other must reach either exit; L+2 is a
lower bound and is attained by one left route and the other right route.

Thus bounded access alone can conceal unbounded distance to an actual usable
resource. It also shows why demanding both ports can impose unnecessary
cancellations once one injectively owned resource already pays the demand.

## Verification and remaining work

The permanent checker exhausts19283 abstract degree-two incidence models,
compares the constructive allocation with an independent augmenting-path
maximum matching, and checks whole-beta resource labels separately. It tests
92 fully frozen shared chains, including all W in{6,8,10,16}, r=2..24,
eleven physical parallel-cycle controls, and six fixed-height relay controls
through L=64. Computation checks the
adapters and examples; (1), the coordinate argument and the chain proof are
general mathematical proofs.

A separate actual-beta adapter check covers320 completely frozen occupied-band
images, including160 nonempty whole-beta allocations and80 interval demands
whose owners remain untouched by the selected beta links. It checks the exact
original-resource ledger and the actual cancellation inventories. None of its
beta owner lists needs truncation; the general theorem nevertheless retains
the explicit at-most-two-owner hypothesis.

The standalone Lean source verifies capacity-two owner uniqueness, strict-rank
injectivity of parent-resource allocations, combination with a disjoint paid
core, and the exact residual ledger. The spanning-tree construction, grid
incidence adapter, freezing, hybrid beta links and physical families remain
written proofs; they are not claimed to be kernel checked.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_one_sided_interval_allocation.py --output output/one-sided-interval-allocation-validation.json

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_one_sided_beta_adapter.py --output output/one-sided-beta-adapter-validation.json

The universal question is now whether residual deficient demand trees can
always gain distinct usable resources, possibly by further mixed-path
cancellation, without losing existing assignments or sharing a beta owner.
One additional incident resource suffices in the abstract model for one
connected deficient tree. In the frozen chain, the extra link instead exposes
an existing unused interval by changing its ownership incidence. We have not
proved that different trees can acquire different resources in arbitrary
frozen grids. General grid equality, computational complexity and a universal
improvement of5/6 remain open. The submitted manuscript is unchanged.
