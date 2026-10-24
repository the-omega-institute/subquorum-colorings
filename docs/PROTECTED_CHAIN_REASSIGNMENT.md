# Protected allocations and unbounded reassignment in frozen chains

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

A fixed maximum interval allocation need not admit a complete extension when
all its paid owners and resources are protected. We prove this in an arbitrary
length completely frozen grid family, classify every possible unpaid root,
and quantify the reassignment needed by an optimal repair. One additional
terminal link suffices for full compensation, but can force every old interval
assignment to change. Two additional links suffice while changing one old
assignment. Thus minimum link count and minimum change to an existing
allocation are distinct optimization questions.

The distinction was identified in the mathematical review of the flow normal
form through a two-demand boundary example. Here we give the all-length
classification and reassignment tradeoff. The grid target remains strictly
positive throughout; the obstruction concerns the protected extension rule.

The independent mathematical review of Theorems 1--3 completed with ACCEPT
on 23 October 2026 at 01:36:04 Singapore. Its complete response is archived in
output/protected-chain-reassignment-oracle.json. It inspected the supplied
proofs and source without executing Python or Lean. The later Theorem 4 below
has a separate review request and is outside that earlier acceptance scope.

## 1. Physical family, current strands and old allocations

Let W>=6 be even and r>=2. Use the r translated direct_family(W,4) copies
of the earlier one-sided allocation note, with copy i shifted by 8i columns.
The actual selected set and matching are completely frozen and uniquely
matched. Write R=W+4. The receiver-closed packet has rows 4..W+5, columns
0..8r+1, dimensions (W+2) by (8r+2), and exact inventory

    |T|=13r, |M|=(W+4)r, B=W+2,
    S-B=(3W-9)r>0.                                         (1)

Fix the previous terminal matching C0 with 2r links used to construct the
shared chain. In each extreme physical row of a copy the alpha endpoint has
one of three states, with local column numbers:

    left:   TP3, cap2 to BB1, no link used;
    middle: TP5, no access, previous link TP3--BP4;
    right:  TP7, cap8 to BB9, previous links TP3--BP4, TP5--BP6.

For the pair i,i+1, choose the upper band if i is even and the lower band if
i is odd. Put copy i in its right state and copy i+1 in its left state in
that band. The two unused end states are middle. There are r current alpha
strands d_0,...,d_(r-1), zero beta strands, and 3r mixed strands.

Let g_i be the singleton interval BB at column 9+8i in the chosen band.
The current one-sided incidence graph is exactly

    d_0 -- g_0 -- d_1 -- ... -- g_(r-2) -- d_(r-1).

There is no other currently accessible unmarked interval. Each g_i has the
two indicated demand owners. Consequently every maximum old allocation pays
r-1 demands, leaving one root j unpaid. The allocation with root j is unique:

    F_j(g_i)=d_i       if i<j,
    F_j(g_i)=d_(i+1)   if i>=j.                              (2)

To prove uniqueness, the component to either side of the unpaid root is a
path with equally many demands and incident resources. Starting at its far
end forces the consecutive allocations towards the root. Equivalently,
orient every resource edge away from the unpaid root. This also constructs
every F_j.

Here an interval allocation maps a resource to its paid demand. A changed old
assignment means that a formerly used physical g_i is allocated to a different
demand. Demand identities remain their translated copy indices: every further
route considered below preserves one alpha per copy and uses no beta credit.

To protect F_j literally, forbid all additional terminal links touching either
free terminal of any paid current alpha owner, and reserve all its allocated
g_i. Existing C0 links are fixed. This is precisely the restricted extension
class in the flow-normal-form theorem, not every strategy that preserves the
number of already paid demands.

## 2. Classification for every protected root

**Theorem 1.** After protecting F_j, the minimum number of additional links
needed for full compensation is

    1          if j=0;
    2          if 1<=j<=r-2;
    impossible if j=r-1.                                   (3)

The middle case is absent when r=2. In the impossible case there is a genuine
directed reachability obstruction in the residual network: the remaining
source reaches no unreserved unmarked interval, even without deleting any
further unit. Thus Z empty is a deficit-one certificate in the separator
formula.

### Complete route geometry

The original terminal component containing each alpha is closed in its two
extreme physical rows: its mixed continuations stay in those rows, and the
alpha strand is their only cross-row connection. Other mixed paths are in
different terminal rows. Adjacent translated copies have intervening BT/BB
columns, so there is no horizontal terminal link joining their route systems.
The original direct-family terminal description proves these facts uniformly
in W. Previous C0 links consume terminals; they cannot open a new link across
one of these barriers.

In a left state the only available continuation is

    TP3 -- BP4 / TP5 -- BP6 / TP7,

where a slash denotes the original mixed strand leading from the BP to the
next TP. One link reaches the middle tip with no access. Two links reach the
right cap. A middle state can only take its one remaining right link. A right
state cannot move: BP6 on its left is already used in C0, and its right
neighbour is selected BT. In particular no route can reverse through a used
terminal.

### Root 0

Its upper endpoint is right and its lower endpoint is middle. Its old upper
resource g_0 is reserved. The lower link

    (R,5)--(R,6)

exposes lower TP7, cap8 and singleton BB9. Call that resource h_0. It is
unmarked and not one of the g_i: g_0 is in the upper band, and no later g_i
has this column. It is accessible only to d_0. The link uses an unprotected
alpha and one unused mixed strand, so every old protected owner and allocation
remains unchanged. Zero links cannot work because all r-1 existing resource
units are reserved. Thus the minimum is one.

### Interior root j

Its incoming-band endpoint is left, accessing reserved g_(j-1); its other
endpoint is right, accessing reserved g_j. The right endpoint cannot move.
Move the left endpoint through its two unused gates to its right cap. The
target h_j is singleton BB at column 9+8j in the incoming band. The neighbouring
gap g_j has the same column but is in the opposite band. Hence h_j is distinct
from every old g_i. Since j<=r-2, it is not a right boundary interval and is
unmarked. These two links expose an available payment for d_j without changing
another alpha owner. A single link reaches only the unported middle tip and
cannot expose an unreserved resource. Thus the minimum is two.

### Last root

Its incoming-band endpoint is left, accessing reserved g_(r-2); its other
endpoint is middle. Both possible rightward continuations end at a BB interval
in column 8r+1, the marked right boundary. The left endpoint's intermediate
tip has no access, and the middle endpoint has no reverse continuation because
its left BP is already used in C0. By the complete route geometry there is no
other exit. The last root therefore cannot reach any unreserved unmarked
interval. In the residual network after protection and removal of marked
intervals, the separator certificate is Z empty. There is no beta resource.
Arbitrarily many further terminal links
cannot produce full compensation while the protected core is fixed. This
proves (3).

This is a counterexample to: “every existing maximum interval allocation can
be fully repaired by modifying only unpaid alpha owners and unused resources.”
It is not a counterexample to the scalar grid inequality, which is positive
by (1), or to the unrestricted flow theorem.

## 3. Optimal one-link repair forces an unbounded reassignment

**Theorem 2.** Start with F_(r-1), so g_i is assigned to d_i and only the last
demand is unpaid. Allow additional links to touch previously paid owners and
allow old resources to be reassigned, while keeping C0 fixed. The minimum
additional link count for full compensation is one. Every repair attaining
that minimum changes all r-1 old interval assignments.

Proof. Without a new link there are r demands and r-1 accessible resource
units, so full compensation is impossible. The root-0 link from Theorem 1
adds access to h_0 and gives the full allocation

    h_0 -> d_0,       g_i -> d_(i+1),  0<=i<r-1.             (4)

This proves the one-link upper bound.

We now classify every single additional link. A link between two unused mixed
owners, including a mixed self-link, changes no alpha free tip and therefore
cannot add an alpha-resource incidence. There is no beta credit. A link that
changes an alpha tip has the following exhaustive possibilities from Section 2:

- left to middle: loses access and exposes no new interval;
- a middle end to right: exposes h_0 at the first copy, or a marked boundary
  interval at the last copy;
- a right end cannot move.

Thus the only single link capable of full payment is the specified root-0
link. After it, the entire accessible resource pool is g_0,...,g_(r-2),h_0.
All r units must be used. Resource h_0 has only owner d_0, so it pays d_0.
Then g_0 must pay d_1; otherwise d_0 would receive two resources while some
demand remained unpaid. Inductively g_i must pay d_(i+1). This proves that
(4) is the unique full allocation after the unique one-link extension.
Originally every g_i paid d_i. All r-1 assignments therefore change. QED.

Since r is arbitrary, no bound independent of r controls the number of old
assignments changed by a repair using the fewest additional links. This is an
allocation statement; the physical resources and the scalar surplus are not
created or multiplied. A safe implementation first replaces d_0's old payment
by h_0, freeing g_0, then successively replaces each subsequent paid demand's
old payment by the freed preceding resource, finally paying the last demand.
It can record each resource's current owner at every step without double use.

## 4. Two links with one old resource reassigned

**Theorem 3.** If r>=3, the same old allocation F_(r-1) has a full extension
using two additional links and changing exactly one old interval assignment.
All earlier paid owners except the penultimate one can be protected literally.

Proof. Put j=r-2. Keep g_i assigned to d_i for i<j and protect those paid
owners and resources. The penultimate demand d_j and the unpaid last demand
remain unprotected. Use the two-link incoming-band continuation of Theorem 1
to expose h_j for d_j. Assign g_j to d_(j+1). Every other old assignment is
unchanged. The new resource h_j is distinct from the old pool, so all payments
are injective. Exactly g_j changes old owner.

Under this specified protected core, one link cannot suffice: it cannot change
a protected owner, and the only one-link full extension from Theorem 2 touches
d_0, which is protected because j>=1. The two-link construction is consequently
optimal within this restricted class. QED.

The cost pairs exhibited are therefore

    (new links, changed old assignments) = (1,r-1) and (2,1).

The one-link repair physically modifies only d_0; its other changes are
resource reassignments. The two-link repair physically modifies only d_(r-2).

They separate a purely monotone protected extension, an optimum in link count,
and an extension preserving most old assignments.

## 5. Exact Pareto frontier for this family

The following deduction is subsequent to the accepted review of Theorems 1--3.
It is not included in that review's acceptance scope.

**Theorem 4.** Start from F_(r-1), keep C0 fixed, and allow arbitrary additional
permitted links and interval reassignments. Every full repair must reassign
g_(r-2) to d_(r-1). Consequently its number of changed old assignments is at
least one, regardless of its link budget. The nondominated cost pairs are
exactly

    {(1,1)}                   if r=2,
    {(1,r-1),(2,1)}            if r>=3.

Both coordinates are minimized; the second counts old physical resources
now allocated to a different demand, as before. This classification is for
this family and this starting allocation, not arbitrary configurations.

Proof. Use the unrestricted residual network, without protecting any paid
owner or old resource. By Section 2's complete route geometry, the last
alpha can access the unmarked g_(r-2) from its left tip, while every other
possible exit is either unported or marked. Removing only g_(r-2) therefore
blocks that source even in the unrestricted network. There is no beta credit.
Any full compensation, normalized using the general flow theorem, must route
the last source to g_(r-2).

For clarity, normalization does not conceal a different payment in the
original full repair. There are initially no beta owners. In any terminal
matching component containing d alpha owners, the excess of TP over BP
terminals is 2d. An alternating path has at most two free terminals, and a
cycle none. Hence a component containing an alpha contains exactly one and
remains alpha. Its two possible endpoint continuations are exactly those
listed in Section 2. Thus every actual full allocation pays the last demand
with g_(r-2), which originally paid d_(r-2). At least this old assignment
changes.

Zero links are impossible. By Theorem 2, one link forces r-1 changes and
attains that pair. For r>=3 Theorem 3 attains (2,1). Any other feasible
pair with at least two links has at least one change and is dominated by
(2,1). Neither displayed pair dominates the other, since r-1>1. For r=2,
(1,1) dominates every feasible pair. This proves the exact frontier. QED.

The subsequent augmentation checker independently deletes only g_(r-2) in
the unrestricted network in 69 physical parameter cases and checks that the
last source is blocked. For W=6 and r=2,3 it additionally enumerates every
additional terminal matching and every injective full interval allocation,
recovering the displayed frontiers. These controls are separate from the
earlier single-link loop and from its accepted review.

## 6. Verification and remaining geometric problem

The permanent checker accepts externally specified protected allocations,
checks their actual incidences and distinct resource ownership, and checks
every possible old root. It also exhausts all single additional links in the
physical family, confirms the unique one-link extension, and checks a computed
maximum allocation against the forced form. It does not enumerate all interval
allocations: uniqueness follows from the written argument and Lean interface.
It also validates the explicit two-link/one-reassignment construction.

The recorded run covers W in {6,8,12}, r=2..24: 69 completely frozen uniquely
matched grids, 11,362 independently forced matching edges, 897 externally
specified protected roots, 963 residual flow models and 4,485 single-link
controls. There are 66 two-link one-reassignment controls and 828 old resource
assignments checked to change at the one-link optimum. These finite controls
support the all-parameter route and ownership proofs above.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_protected_chain_reassignment.py --output output/protected-chain-reassignment-validation.json

Two standalone Lean theorems verify the combinatorial forcing argument in
Theorem 2: a path-edge assignment avoiding an already paid root, incident only
to its two endpoints and injective on demands, must assign every edge to its
right endpoint; hence every old left-end assignment changes. The freezing,
route geometry, protected-root costs and two-link construction remain written.

The general grid target now needs a route-and-allocation argument permitting
controlled reassignment when necessary. A proof requiring every arbitrary old
maximum allocation to remain frozen would be false by Theorem 1. A bound on
additional links alone also supplies no bound on allocation changes, by
Theorem 2. The exact flow theorem remains valid; the missing step is the
geometric resource/cut budget in arbitrary frozen grids. The universal grid
inequality, triple equality and improvement of the existing 5/6 bound remain
open. The submitted manuscript is unchanged.
