# Crossing actual matching edges: exact ports, retained packs and residual reserves

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

We extend the [cut-respecting rectangle gluing lemma](OPPOSED_DIRECTION_INTERFACES_AND_PIECEWISE_COMPENSATION.md)
to partitions that cut actual matching edges. The extension has an explicit
interface demand term; that term cannot be omitted, even on completely frozen
physical grids. Unused original resources give a further joint compensation
bound without spending any unit twice. This is a statement about the existing
whole-owner-support counting model, not a new general flow theorem.

## 1. Model and hypotheses

Let an even grid carry a feasible selected set T and actual matching M, with
P=V(M). Partition all vertices into disjoint even-by-even rectangles. In each
rectangle choose horizontal or vertical two-line bands. Their auxiliary
matchings N_R combine into one genuine perfect matching N of the board.
The directions may differ. Let E_cut consist of actual M edges with endpoints
in different rectangles, and put e=|E_cut|. We retain P when cutting M.
Every endpoint of an edge in E_cut is a PORT C, rather than a blank vertex.

Work with the complete local even-band BB/TT resource convention. Its original
units have immutable(region,band,interval) identities. A BB/TT forest component
of imbalance1 is one resource; a balanced boundary chain contributes zero.
The physical domains of different rectangles are disjoint. Put Q_R for these
units and Q for their disjoint union. We use the established whole-owner
support convention: an owner supports units in no-P gaps incident to its body.
Declared terminal links include the valid links within each chosen local band.
Additional justified links may be admitted; they cannot weaken our lower
bounds. The mixed-direction sharp examples below use precisely these local
band links; the uniform-direction subfamily is the full original aligned
whole-board model.

Remove E_cut temporarily. In each rectangle take the multigraph of internal
M edges and auxiliary N edges with both endpoints in P. Coincident M and N
edges retain their different identities, making a two-edge alternating cycle.
Each component is an alternating path or cycle. A vertex missing an N edge
inside P has ordinary tip T or B according as its N mate is selected or blank.
A vertex missing its M edge has a port C. An isolated endpoint may supply both
one ordinary tip and one C at that same vertex; these are DIFFERENT incidences.
This convention prevents losing single-vertex half-paths.

Write A_R,B_R,X_R for closed TT,BB,BT path counts, and t_R,b_R,c_R for CT,BC,CC
half-path counts. Cycles carry no tips. A closed owner has no port; an open
component has a C incidence and is not a closed local owner. For local payment
packs below, use only CLOSED local owners, their declared links, and Q_R.
This exclusion is a substantive hypothesis: treating an open half-path as a
closed alpha or beta would change the model.

## 2. Exact local and global objective ledgers

Define the cut local slack using only the retained internal matching edges:

    S_R^cut = |R|/2 - |T intersect R| - |M internal to R|.

Then

    S_R^cut = |Q_R| + B_R - A_R + b_R + c_R.              (1)

In particular b_R and c_R in(1) are PORT CORRECTIONS, not additional usable
original resources. Let t=sum t_R,b=sum b_R,c=sum c_R, and A0=sum A_R,
B0=sum B_R. The original whole-board slack is exactly

    S = sum_R S_R^cut - e
      = |Q| + B0-A0 + b+c-e.                             (2)

**Proof.** Within a rectangle count auxiliary edges of types BB,TT,BT,PP,PT,PB
by n_BB,...,n_PB. If m is its internal actual edge count and p its port count,
then |P intersect R|=2m+p. The auxiliary perfect matching gives

    |R|/2 = n_BB+n_TT+n_BT+n_PP+n_PT+n_PB,
    |T intersect R| = 2n_TT+n_BT+n_PT,
    |P intersect R| = 2n_PP+n_PT+n_PB.

The tips of alternating paths give

    n_PT=2A_R+X_R+t_R,   n_PB=2B_R+X_R+b_R,
    p=t_R+b_R+2c_R.

Subtracting yields S_R^cut=n_BB-n_TT+B_R-A_R+b_R+c_R.
The complete even-band forest convention gives |Q_R|=n_BB-n_TT. Its proof is
unchanged by cutting M, since T,P,N and the BB/TT forest never change.
Finally |M|=sum internal m+e; areas and selected counts add, proving(2). QED.

One can instead assign half an actual-edge cost to each port endpoint. That
balanced local quantity is

    S_R^half = |Q_R|+B_R-A_R+(b_R-t_R)/2,
    S = sum_R S_R^half.                                  (3)

It can be half-integral. A fractional ledger entry is not a physical resource
and must not be allocated as one.

## 3. Restore the actual matching: an exact boundary skeleton

Make a graph on all C ports. Each local CC path gives one port-to-port edge;
each crossing M edge gives one edge. A CT or BC half-path labels its C port
with its other end, T or B. Every port has exactly one crossing-M incidence
and either one CC incidence or one T/B label. Thus this skeleton consists
of labelled-end paths and unlabelled cycles. Let aI,bI,xI be its TT,BB,BT
path counts. Its cycles have no new alpha or beta credit. Restoring E_cut
gives exactly these additional global owners; closed local owners persist.
Consequently

    A_global=A0+aI,    B_global=B0+bI,
    t=2aI+xI,         b=2bI+xI,
    e=c+aI+bI+xI,     b+c-e=bI-aI.                       (4)

In particular aI<=e, and the precise number of new ordinary-ended interface
paths is e-c. This remains true with arbitrarily long CC relays or pure port
cycles: a skeleton path has one more crossing-M edge than CC edges, whereas
a skeleton cycle has equally many of each. Equation(2) becomes

    S=|Q|+B_global-A_global.

This supplies an exact common ledger for mixed local directions with actual
matching edges crossing their boundaries. It provides no numerical bound
beyond that identity by itself.

## 4. Compensation lemma with a retained pack and unused original reserves

In each rectangle choose a feasible closed-owner pack of value v_R and cost
l_R. Its unpaid closed alpha count is D_R=A_R-v_R. Let U subset Q be exactly
the original units spent by the union of these packs. Different regions use
different units, even when their local interval coordinates look the same.

Let I be the set of aI NEW interface alpha owners. Build a bipartite graph
from I to Q minus U, with an edge if that actual whole owner supports that
original unit. Let nu be a maximum matching size. This is one JOINT matching,
not a sum of separate matches that each reuse a shared reserve. Then

    V_global >= sum_R v_R + nu,
    D_global <= sum_R D_R + aI - nu
             <= sum_R D_R + e.                          (5)

There is a witness attaining at least sum v_R+nu with total link cost sum l_R.
This is a cost for that constructed value, not a claim that the minimum cost
at a potentially larger global optimum is at most sum l_R.

In particular, if each closed local alpha is paid and the unused-reserve
matching covers every interface alpha, the whole partition fully compensates
all its alphas. If all local packs have zero links, that full witness has zero
links. The same holds without reserves when aI=0, EVEN IF e>0. The earlier
no-crossing-M gluing lemma is the special case e=0.

**Proof.** A closed local component has both its actual mate and any PP
auxiliary neighbour inside its local body. Restoring removed M edges therefore
cannot merge it with any open component or another region. It is the SAME
full global owner, with the same ordinary endpoints and all its old supports
and links retained. Its internal paths remain valid, including two-entry beta
forks. Mapping a local owner to its actual unchanged physical body is injective
across regions. The resource map is likewise injective on physical units.
Thus all local packs combine into a feasible global pack; no mixed gate,
beta gate, endpoint or original unit is spent twice.

Every new interface alpha contains a port and is distinct from every closed
owner already used. A direct interval payment from it uses no link and no
other owner. The joint matching assigns different unused original units to
different interface alphas, so these payments extend the retained pack.
The value is sum v_R+nu and the cost is sum l_R. Subtract this value from
A_global=A0+aI and use(4) to obtain(5). QED.

The criterion is sufficient. Failure of this particular unused-reserve
matching need not preclude global payment by links, beta forks, or rerouting
the retained local packs. Nor do we assert that a chosen local optimum
maximizes the subsequent reserve matching. All those changes must still use
one common original resource pool.

## 5. Sharp actual fully frozen family, including mixed local directions

For every even W>=8 and q>=1 use the earlier actual module configuration
`configuration(W,q)` on a(W+2)-by-(10q+2) board. Its counts are

    |T|=(7q+2)W/2+3q+2,   |M|=q(3W/2+5),   S=2q.

All endpoints are frozen, M is unique, and T is a true fixed-P maximum, by
the earlier [adjacent module theorem](FORCED_MATES_AND_ADJACENT_MAXIMA.md).
Cut horizontally after rows0,1. The ONLY crossing actual edges are

    ((1,10i+5),(2,10i+5)),    0<=i<q.                    (6)

For both choices below the lower rectangle uses horizontal bands.

**Uniform control.** Use horizontal bands also in the top rectangle. Each
original alpha is split into two CT half-paths by exactly its one crossing
edge. There are no closed local alphas, no betas and no CC half-paths.
Every local closed alpha is therefore paid, but this says nothing about
the q pairs of open ends. The original full model still has V=0 and deficitq.
This already proves the e term in(5) is sharp on fully frozen physical grids
with all original units available, using the full original aligned network.

**Mixed-direction version.** Pair columns in the top rectangle. In module i
its CT half-path is explicitly

    (1,10i+3) --M-- (1,10i+4) --N-- (1,10i+5),

with T end(1,10i+3), since its auxiliary mate(1,10i+2) is selected, and C
end(1,10i+5). The remaining top endpoints form the two parallel-edge cycles
on column pairs6/7 and8/9 in that module. Thus the top rectangle has no
closed alpha, beta or mixed owner and no raw resource; it has q CT half-paths
and2q cycles. It has no declared TP--BP link: its sole ordinary endpoint in
each module has a selected, rather than endpoint, vertical band neighbour.

The lower CT half-paths and their terminal T ends(W,10i+5) are unchanged.
All bottom original intervals and permitted links are unchanged. Closing
the q ports again creates exactly q interface alphas. Their top T ends have
no outgoing declared link or support; the reachable lower mixed owners
have empty complete support and no beta by the previous terminal-gap proof.
Thus no alpha can pay by any length route or beta fork. All3q original
units remain available, but they lie outside this reachable support. Hence

    A0=B0=0, t=2q,b=c=0,e=q,aI=q,bI=xI=0,
    |Q_top|=0, |Q_bottom|=3q,
    S_top^cut=0, S_bottom^cut=3q,
    V=nu=0, D=q, S=0+3q-q=2q.                           (7)

The local closed systems are source-free; this is not a new example of
individually positive local payment being lost to a resource collision.
The failure is the creation of new demands when actual matching ports are
rejoined. Forgetting those demands is the invalid extension of local gluing.
The board remains fully frozen because T and M never changed. The mixed
version concerns the stated piecewise model, without a claim about arbitrary
extra cross-band terminal-link rules or other auxiliary decompositions.

The smallest mixed example uses W8,q1: a10-by12 board with41 selections,
17 actual matching edges and34 frozen endpoints. One crossing edge turns
two CT half-paths into one alpha. The global pool has3 units, yet none can
pay that alpha; S=2. This is not a counterexample to the numerical target
inequality or an improvement of the universal5/6 bound.

## 6. Port cycles and arbitrarily long CC relays are not spare resources

Two physical controls test the incidences that are easy to omit.
On a2-by4 board take P to be both rows in columns1,2, T empty, M horizontal
across the cut between columns1,2, and vertical auxiliary pairs in both2-by2
regions. There are two CC half-paths and two crossing actual edges. They
restore one alternating cycle, with no alpha or beta. The apparent local
CC corrections cancel the two crossing-edge costs exactly. Only the two
actual BB resources outside P remain; there are no two additional credits.

For arbitrarily many m>=0 CC relays, use m+2 consecutive2-by2 rectangles.
Use horizontal auxiliary pairs in the two end rectangles and vertical ones
in the m middle rectangles. Select the two outer top corners. Put one top
P vertex at each inward end, all four vertices in every middle rectangle,
M across every top boundary and along the bottom row within each middle
rectangle. There are e=m+1 crossing edges and c=m CC components, yet only
ONE new TT interface path, in agreement with e-c=1. It can use an actual
end-region BB resource directly. Both these controls are feasible physical
grids; they are not claimed fully frozen. Their purpose is to check the
port accounting independently of the separate freezing hypothesis in Section5.

## 7. Verification and formal scope

The solver-free verifier checks303 physical partition controls:288 two-/four-
region configurations, three recoveries of the prior no-crossing lemma,
one pure port cycle, and11 CC relay lengths. The frozen family covers W in
{8,10,20,40}, q in{1,2,3,7}, with32 sharp interfaces across the two top
choices. It retains edge identities, isolated half-path incidences, every
original resource ID and the actual local-to-global owner map.

For every partition it reconstructs the boundary skeleton independently of
the full alternating endpoint graph, checks(1)--(4), embeds every chosen
local primitive including forks into the same global model, and checks the
residual reserve matching and(5). There are183 strict reserve improvements,
using540 distinct-original-unit assignments across their separate controls.
Twelve small global systems also agree with independent primitive packing;
the uniform sharp controls agree with the previous full-board compiler.
Finite checks test the proofs above; they do not establish the general lemmas.

Local Lean4.33.0 passes15 new declaration audits and39 dependency audits,
without warnings, placeholders, native evaluation or new axioms. It proves
local port-ledger and skeleton-correction arithmetic, the interface-alpha
bound and zero port-cycle correction, generic exact reachability of a closed
body, injectivity of old-plus-unused reserve assignments, and both deficit
bounds and the full-payment implication. On the actual W8/q1 board it reuses
the complete freezing theorem, checks the single crossing edge and internal
counts, verifies the connected closed mixed-direction alpha path, and proves
that every-length routes in the compiled closed owner set have no payment
exit. The coordinate-to-network support adapter remains outside Lean.

Reproduce from the repository root:

    python3 develop/check_crossing_matching_ports.py --output output/crossing-matching-ports-validation.json
    python3 develop/check_crossing_ports_formal.py --lean /path/to/lean-4.33.0 --output output/crossing-matching-ports-formal-validation.json
The general graph-to-resource geometry and all-W/q specialization have written
proofs, with finite Python checks; we do not claim an end-to-end formal grid
compensation theorem. The next step is to bound the unreserved interface
alpha term using geometry and freezing, or find partitions with stronger
reserves. A small number of crossing M edges alone cannot guarantee zero
loss, even after fixed-P selection optimization and complete freezing.
