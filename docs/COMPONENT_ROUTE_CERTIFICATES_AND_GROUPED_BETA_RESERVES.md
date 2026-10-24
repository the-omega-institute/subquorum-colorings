# Component route certificates and grouped beta reserves

25 October 2026. Research branch only; the submitted manuscript is unchanged.

This note proves a sufficient cross-component compensation lemma. It groups
beta reserves by an entire first-witness component, chooses internal pairings
after exterior routes, and lifts every reduced route certificate to an actual
terminal matching. A reserve component supplies exactly one extra beta unit.
The reduced network can be strictly weaker than the unrestricted network.

Dependencies are the original-terminal normal form in
[COMPENSATION_FLOW_NORMAL_FORM.md](COMPENSATION_FLOW_NORMAL_FORM.md), the
cancellation ledger in
[TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md](TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md),
and the missing-port injection used in
[FIRST_DESTINATION_ALLOCATION_AND_UNPORTED_GATE.md](FIRST_DESTINATION_ALLOCATION_AND_UNPORTED_GATE.md).
The contribution here is the component accounting and witnessed lifting
construction, using elementary alternating-path matchings. It is not a new
general flow or matching theorem.

## 1. Hypotheses and exact component account

Work in the finite original-terminal model of the cited normal form. Each
original owner has two distinct terminals: alpha has two TP, beta two BP,
and mixed one BP and one TP. Owners and terminals are disjoint. Allowed
links join a TP to a BP of a different owner. An original unmarked interval
is a single resource, however many terminals access it. Let I be their number.
Access may include already justified selected-cap access; it creates no new
resource identity. Marked boundary intervals are excluded throughout.

Assume a set F of allowed links covers each original alpha TP exactly once,
uses no BP twice, and has no source outside the original alphas. Each target
is an original beta or mixed owner. These are the full combinatorial
hypotheses. For completely frozen grid systems in which every original alpha
tip has no direct adjacent BB port, the previously proved missing-port
injection supplies F. No assertion about virtual alpha tips is used.

Form the owner bipartite **multigraph** H of F. Every alpha has degree two,
every beta degree at most two, and every incident mixed owner degree one.
Include every isolated original beta. Isolated mixed owners have no effect
on H but remain available as gates in the network below. Parallel edges are
retained; a two-edge alpha--beta cycle is a balanced component.

The components have the following counts, with n a nonnegative integer:

| Component | alpha count | beta count | residual role |
| --- | ---: | ---: | --- |
| Path with mixed at both ends | n+1 | n | one demand |
| Path with beta at both ends | n | n+1 | one reserve |
| Path with mixed and beta ends | n | n | balanced |
| Alternating cycle | n | n | balanced |

The first row includes mixed--alpha--mixed. The second includes an isolated
beta. The last two nonempty types have n>=1. These exhaust the components:
all degrees are at most two, alpha cannot be a path endpoint, and any mixed
owner must be a path endpoint.

Write k for the total original alpha count, b for the beta count, t for the
number of demand components, and s for the number of reserve components.
Summing the table gives the exact identities

    b+t = k+s,                  I+b-k = I+s-t.                 (1)

In particular, a reserve component with n+1 original betas has only **one**
beta unit left after paying its n internal alphas. Counting those n+1 betas
as exterior reserves would spend the internal payments again.

## 2. Arbitrary roots in the internal matching

**Lemma 1 (root choice).** In a demand component, any prescribed alpha can
be the unique unmatched alpha of an F-matching using all its betas. In a
reserve component, any prescribed beta can be the unique unused beta of an
F-matching paying all its alphas. Balanced components admit a complete
alpha-to-beta F-matching.

**Proof.** Ignore the mixed leaves of a demand path. Its order is

    a_0, b_0, a_1, b_1, ..., b_(n-1), a_n.

To leave a_r free, pair b_i to a_i if i<r, and to a_(i+1) if i>=r.
Each pair is an edge of F. The selected alpha indices are exactly all
indices 0,...,n except r, once each. The beta indices are all different.
This also works for n=0.

A reserve path has the same ordered pattern with alpha and beta interchanged.
The same rule leaves any chosen b_r unused. A balanced mixed--beta-ended
path is matched consecutively from its beta end; an alternating cycle is
matched by either alternating edge class, including the two-parallel-edge
case. In each case we choose the actual F terminal witness of each edge.
Distinct matched owners imply distinct terminals. QED.

The index map is skip(r,i)=i for i<r, and i+1 otherwise. Its bounds,
injectivity, adjacency and coverage for every n and r<=n are formalized in
[ComponentRouteCertificate.lean](../formal/SubQuorum/ComponentRouteCertificate.lean).
This is an arbitrary-length result, not a finite path enumeration.

## 3. The reduced network Q

The following construction uses original terminal witnesses on every arc.

* Each demand component becomes one unit source. Its possible departures
  are the outgoing links and interval accesses of **all** original alpha
  TPs in that component, not only those next to a mixed end.
* Every original mixed owner remains a gate of capacity one, entered at its
  BP and exited at its TP. This includes mixed owners not incident to F.
* Each reserve component becomes one unit sink. It can be entered through
  either BP of **any** original beta in that component. Its capacity is one
  for the whole component, not one per original beta.
* Each unmarked original interval is a separate unit sink.
* Retain an allowed TP--BP link precisely when its tail belongs to a mixed
  owner or to an alpha in a demand component, and its head belongs to a
  mixed owner or to a beta in a reserve component. Retain accesses from
  those same allowed tail owners to unmarked intervals.

Thus a route starts at one demand component, uses zero or more distinct
mixed gates, and ends at one reserve component or original interval. A
packing uses each source, gate and sink at most once. Cyclic flow can be
discarded. Each arc keeps the actual original link or access that realizes
it. Parallel reduced arcs can be kept separately, or one witness retained:
source and reserve capacities are one, and a mixed gate has a unique BP/TP.
The root choices in Lemma 1 make every retained witness interchangeable for
this restricted network.

Balanced-component alpha and beta ports, and beta owners of demand
components, are deliberately absent from Q. This restriction is material;
Section 5 gives a strict example.

## 4. Compensation and lifting theorem

**Theorem 2.** Under the hypotheses of Section 1, let a witnessed route
packing in Q have value mu and use c_Q actual TP--BP links. There is an
original-terminal matching and a set of distinct legal interval payments
which compensate exactly

    p = k-t+mu

original demands, leave exactly t-mu unpaid alpha strands, and use exactly

    k-t+c_Q

links. No original beta unit, interval unit, mixed gate or terminal is used
twice. Consequently mu=t is a sufficient condition for full compensation.

**Proof.** For each used demand component, the first arc witness specifies
an original alpha and one of its TPs. Leave that alpha free in Lemma 1's
internal matching. Choose any alpha root in each unused demand component.
For each used reserve component, the last link witness specifies an
original beta and its BP. Leave that beta unused internally. Choose any beta
root in every unused reserve component. Completely match each balanced
component. These choices produce k-t alpha--beta core links.

The exterior packing starts only at the chosen unmatched alphas, enters
only the chosen spare betas, and otherwise uses mixed owners. Hence it
uses no owner that participates in a core link. Different exterior routes
share no source component, reserve component, mixed gate or interval.
Within a route, a mixed owner uses its BP for entry and its distinct TP for
exit. Thus all core and exterior links together form a terminal matching.

Each core alpha--beta link consumes one alpha and one beta. An exterior
route ending at a spare beta consumes one more alpha and one more beta;
a route ending at an interval leaves one spliced TP--TP alpha strand, with
its last TP retaining the witnessed access to that interval. Pay that
strand with that interval. These interval identities are all different,
and none was used by the core. The original-terminal cancellation normal
form justifies the splicing and these payments; no virtual tip is assigned
a newly inferred missing-port witness.

The core compensates k-t demands; each of the mu exterior routes compensates
one more. Each unused demand component leaves exactly one alpha. Core links
and exterior links have disjoint owners, so their link counts add. This
proves all three exact formulas and the nonreuse claims. QED.

For example, enough gate-disjoint witnessed routes from the t demand
components to t distinct reserve components/intervals prove full
compensation even though the original alpha-to-beta injection leaves t
unmatched. Routes need not have a fixed geometric direction. They may start
at any alpha inside a demand component and enter any beta inside a reserve
component, since the internal matching is chosen afterwards.

**Scalar implication and scope.** If mu=t, the packing uses at most I+s
different sinks, hence t<=I+s. Identity (1) gives I+b-k>=0. In the one-sided
packet ledger of the dependencies this is the nonnegative boundary-adjusted
budget condition. This is a conditional complete-compensation class. We
have not proved that arbitrary frozen grids admit such an F and a saturating
Q packing; there is no new unconditional numerical improvement of 5/6.
The cancellation and routing reorganize the fixed scalar account (1), and
do not by themselves increase that account.

## 5. Two explicit abstract obstructions

These are original-terminal systems, **not claimed to be realizable frozen
grids**. Terminal names below are the integers used by the verifier. Each
owner occupies a consecutive pair (2i,2i+1); alpha is TP/TP, beta BP/BP,
mixed BP/TP. Only the listed links and accesses are allowed.

**Grouped reserve.** Take owners in order

    A, B, C, x, y, m0, m1, m2, m3

with A,B,C alpha, x,y beta and m0,...,m3 mixed. Let

    F = [(0,10),(1,12),(2,14),(3,16),(4,6),(5,8)]

and add links (0,7),(2,9), with no intervals or accesses. The components of
A and B are demand paths. The component x--C--y is one reserve path.
Its internal payment pays C. Either A can enter x or B can enter y, but
both cannot be paid in addition to C: there are only two whole betas and no
intervals. Here k=3,b=2,t=2,s=1, Q has maximum value one, and the lifted and
unrestricted compensation optima are both two. A rule treating x and y as
two **additional** reserves would falsely claim three payments. The rule
fails; the scalar account is genuinely -1 in this abstract system. This
does not refute the grid inequality.

**Balanced exchange.** Take owners A,B,m0,m1,m2,x, with A,B alpha, m0,m1,m2
mixed and x beta. Let

    F = [(0,4),(1,6),(2,8),(3,10)],
    extra link = (0,11),
    access = {2: {J}}, with one unmarked interval J.

A is in a demand component; B and x are in the balanced path m2--B--x.
There is no reserve component. Q cannot use B's access or x, so mu=0 and
the lifted compensation is one. The full system pays two: link A to x by
(0,11), and pay B directly at terminal 2 with J. Therefore Q is a
**sufficient lower bound**, not an exact quotient of unrestricted flow.
Its deficiency must not be presented as an original-network obstruction.
The following extension handles such exchanges with explicit compatibility.

## 6. Compatible balanced-component exchanges

**Lemma 3 (ordered transfer).** Order a balanced path from its mixed end as

    m, a_0, b_0, a_1, b_1, ..., a_(n-1), b_(n-1).

After deleting alpha a_i and beta b_j, its other n-1 alphas can be matched
to its other n-1 betas using F **if and only if i<=j**. In a balanced cycle,
any prescribed alpha/beta pair can be deleted with such a matching remaining.

**Proof.** If i<=j, match a_l, for l!=i, to b_(l-1) when i<l<=j,
and to b_l otherwise. These are adjacent in F, and the beta indices used
are exactly 0,...,n-1 except j. If j<i, deletion of b_j separates the prefix
a_0,b_0,...,a_j, which has j+1 alphas and only j betas. None of these alphas
can reach the remaining path in F, and the removed a_i lies outside this
prefix. A saturating matching is impossible. For a cycle, deleting opposite
types splits the remaining cycle into two paths, each with an even number
of vertices (one may be empty). Pair consecutively in each. QED.

In particular a balanced component cannot safely be replaced by an ordinary
unrestricted relay gate: in m,a_0,b_0,a_1,b_1, entry through b_0 and departure
through a_1 leave a_0 with no beta neighbour. The ordered compatibility is
essential, even when this component is visited only once.

**Theorem 4 (lifting with balanced transfers).** Enlarge the route-certificate
class of Section 3 as follows. A route may enter a balanced component at a
specified original beta b_j and depart at a specified original alpha a_i,
using their actual incoming-link and outgoing-link/access witnesses. Each
balanced component is used by at most one route and at most once in that
route. For a path require i<=j in the order of Lemma 3; for a cycle allow
any alpha/beta pair. All other source, mixed, reserve and interval capacities
and restrictions stay as in Section 3. Do not identify incompatible port
pairs via a common relay node.

Let the resulting packing have mu routes, h used balanced components, and
c actual TP--BP links. It lifts to an original-terminal matching and
distinct interval payments with

    compensation = k-t+mu,
    unpaid = t-mu,
    selected links = k-t-h+c.                                  (2)

**Proof.** Choose demand and reserve roots from route witnesses as before.
In every used balanced component delete its witnessed departing alpha and
entering beta from the internal matching; Lemma 3 matches all remaining
owners. Unused balanced components remain completely matched. The core
therefore has k-t-h links. All exterior links use only the removed roots
and unused mixed owners, so they are terminal-disjoint from the core.

A balanced transfer is an accounting transition, not an extra original
link or a mixed owner. Split each certificate route at its balanced
transfers. A route with h_r transfers yields h_r+1 genuine original
normal-form pieces. At each split, the earlier piece ends at the removed
beta, while the next starts at the removed alpha. Every piece ends at a
different beta or at its route's distinct final interval. Across all routes
there are mu+h paid pieces, using different root owners and mixed gates.
Adding the k-t-h core payments gives k-t+mu, and all actual link counts
add as in (2). The same disjointness argument proves nonreuse and leaves
exactly one unpaid alpha per unused demand component. QED.

The balanced-exchange example in Section 5 is covered with mu=1,h=1,c=1:
the core has zero links, the exterior has the link A--x and B's payment
by J, and both demands are paid. Chains of arbitrarily many compatible
balanced transfers have the same proof; no fixed geometric direction or
bounded rematching length is required. Formula (1) is unchanged.

This is a certificate theorem with a prescribed port-pair compatibility
condition. We have not reduced the enlarged class to an ordinary unit-gate
max-flow instance, proved it equals unrestricted compensation, or proved
the existence of sufficient routes in arbitrary frozen grids. A geometric
route-existence or separator-budget argument is still needed for a universal
result. The new theorem repairs the stated balanced exchange, without
claiming that this exhausts all reasons Q can be conservative.

## 7. Verification and reproducibility

Run from the research root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_component_route_certificate.py \
      --output output/component-route-certificate.json
    cd formal
    lean SubQuorum/ComponentRouteCertificate.lean

The Python checker reconstructs original links, chooses roots from route
witnesses, checks each internal matching, performs actual terminal
cancellation and verifies distinct interval payments. It checks 600 seeded
abstract systems (428 lifted exterior routes; 17 strict lower bounds), both
obstructions, all 12 valid injections of the fully frozen 14x20 unported
shared-gate fixture, five separated missing-alpha stacks, and 18 frozen
asymmetric depth-relay systems. The relay cost is min(upper,lower) in the
one-sided budget: the short right exits enter marked intervals and cannot
pay it. The finite controls validate the implementation and examples;
the general result is the proof above.

For the extension it checks all 2,870 ordered root pairs for path sizes
1,...,20, including the infeasible i>j choices via an independent maximum
matching, and reconstructs 12 chains of 1,...,12 compatible balanced
transfers with varying path lengths and interior roots. Each chain is
checked by actual original-terminal cancellation, one interval payment,
the h-corrected link count, and the unrestricted solver. These extension
examples are abstract terminal models, not additional physical-grid tests.
It also checks all 2,870 alpha/beta deletion pairs in balanced cycles of
sizes 1,...,20, including the parallel-edge cycle at size one.

The standalone Lean file verifies the arbitrary-root path matching and the
component count/signed ledger identities for arbitrary finite lists, and
the ordered-transfer formula's bounds, injectivity and coverage for arbitrary
path length. It does not formalize the necessity of i<=j, the cycle deletion
case, graph classification, Q construction, flow existence, full lifting
theorems or grid geometry. No independent Oracle review of this
note has yet been obtained. The previous broker model failures are not
review acceptance.
