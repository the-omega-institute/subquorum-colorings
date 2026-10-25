# Reserve boundary splitting and exact joint compensation

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

We realize the ownership change left open by the
[frozen ear construction](FROZEN_EAR_REMATCHING_AND_RESOURCE_CONSUMPTION.md).
An actual feasible completely frozen extension retains every old selection
and endpoint, adds four endpoints and one selection, and changes the old
right private singleton into a resource shared by a new alpha and a mixed
chain reachable from the left alpha. Thus preserving a blank interval does
not preserve its private ownership under rematching.

The full original resource pool still pays all sources. We identify where
the right demand moves, give an exact two-source compensation formula for
**every** subset of original available intervals, and compute a repair that
releases a different original interval and frees the shared one at a cost
of three actual links. Combining this repair with cap completion requires
an overlap correction. For q separated copies,

    V=q+|F union E|,
    c=|F|+3|E minus F|.                                    (1)

Here each copy retains its shared J, F denotes filled left caps, and E
denotes copies in which the separate right resource K is available. All
other original intervals are reserved; every original owner, actual link
and whole beta remains. The formula does not spend J twice or pay one
source twice when the repairs overlap. This is a verified failure of
private-ownership persistence, not a counterexample to unrestricted grid
compensation. Universal compensation and the 5/6 improvement remain open.

## 1. The actual rematching and freezing certificate

Start with the saved14 by18 active-merger board and retain all its selected
and endpoint sites. Add selected (9,15) and endpoints

    (6,10), (8,13), (8,14), (8,15).

Remove these six old actual edges:

    (5,9)--(6,9),   (5,10)--(5,11), (5,12)--(6,12),
    (6,11)--(7,11), (7,10)--(8,10), (8,11)--(8,12).

Replace them by eight edges:

    (5,9)--(5,10),   (5,11)--(5,12), (6,9)--(6,10),
    (6,11)--(6,12),  (7,10)--(7,11), (8,10)--(8,11),
    (8,12)--(8,13),  (8,14)--(8,15).

All other old edges remain. Seven of the new edges and all six removed ones
lie on the single alternating augmentation with ends (6,10),(8,13);
the remaining new pair (8,14)--(8,15) supplies part of its freezing support.
There is no overlap of actual matching edges. The new selection sees only
new endpoint (8,15), and the new endpoints do not add occupied neighbors
to any old selected site. Thus feasibility follows directly from the
coordinates. The objective increases by3: two net actual edges and one T.

The [saved actual fixture](../develop/fixtures/frozen_reserve_boundary_split.json)
contains a strict witness at each of its66endpoints. Every listed witness
has two distinct physical neighbors, each selected or with actual mate at
a strictly lower listed rank. This is a complete constructive freezing
proof: induction on the integer rank freezes every endpoint. No solver
completeness or finite search bound is needed. The concrete certificate and
all four left-cap variants are also checked by Lean's inductive freezing
rule. The largest base rank is15; adding the optional left cycle uses16,
and its filled-cap beta uses16/17, as in the prior cap proof.

The same rematching is feasible and completely frozen in cap states
E,T,C,CB. In each case it loses exactly the old band4 singletons at
columns13,14,15 and creates no new original interval. Alpha and beta counts
stay fixed; the I+b-k ledger decreases by3, consistent with the objective
increase. The exact interval counts are53,52,52,50 in E,T,C,CB respectively.

## 2. The interval survives but its source ownership changes

The old right singleton is still exactly

    J=(band2, first13, last13).

Its column13 remains BB, column14 remains BT, and column15 remains PP.
The selected guards are unchanged. But its left TP (5,12) now has actual
mate (5,11), a BP, so it belongs to a one-edge mixed owner. The right PP
boundary belongs to the new alpha R with terminal pair

    (3,15), (10,9).

Its20-endpoint alternating path includes both (4,15),(5,15), follows the
retained right-side path to (6,12), then crosses through (6,11),(7,11),
(7,10),(6,10),(6,9) into the old long mixed tail ending at (10,9).
The original left alpha L still has terminal pair (3,1),(5,6).

Consequently J's whole-support owner set changes from one old alpha to

    {new alpha R, mixed owner [(5,11),(5,12)]}.

L reaches the mixed owner through three original actual TP--BP links:

    (5,6)->(5,7), (5,8)->(5,9), (5,10)->(5,11).

The intervening actual mixed pairs are (5,7)--(5,8), (5,9)--(5,10),
(5,11)--(5,12). Thus L can pay through J at cost3, while R can pay directly
through the same original J at cost0. These are two uses of one resource
identity, not two available copies of it.

R also inherits the old long mixed tail's private singleton

    K=(band5, first10, last10).

Only R supports K. This is an existing original unit, not a new resource
created by the exchange. The original right demand has migrated to a
different terminal pair and inherited different support. Tracking the old
source solely by its tip (5,12) would now misidentify a mixed owner as an
alpha.

## 3. Exact projection of the complete original allocation network

Keep every original owner, terminal link, beta sink/body and interval
identity. Only the set A of available original intervals may vary. Here
original means the final physical board before availability restrictions;
J and K additionally keep their pre-rematching interval identities. The
rematching preserves beta counts, not every old beta path identity.

The alpha-reachable owner graph consists of disjoint mixed branches of L
and R. From L there is one single-link branch with support at band1cols5,6,
and the three-link chain to J. From R there is a single-link branch with
support at band5cols1..5. The branches of the two sources share no owner.
In CB alone, L additionally reaches its exclusive empty-body beta at cost1.
Neither of the two non-cap betas is reachable from an alpha. In particular no beta can
receive two alpha arms, so the ordinary and full fork optima agree here.
This is a property of the displayed complete graph, not a general equality
of the two compensation models.

The reachable original intervals fall into five disjoint classes:

| Class | Original units | Reachable from L | Reachable from R |
| --- | --- | ---: | ---: |
| G_L0 | L's direct cap support:3/2/2/0units in E/T/C/CB | 0links | never |
| G_L1 | band1cols5,6 | 1link | never |
| G_R0 | band1cols11..14 and band5cols10,12..16 | never | 0links |
| G_R1 | band5cols1..5 | never | 1link |
| {J} | band2col13 | 3links | 0links |

Every available original interval outside these classes is unreachable
from either alpha. Some members of G_R0 also support an unreachable neutral
owner; they are reachable only from R among the actual sources. We do not
call all those units private to one whole owner. K itself is supported
only by R. The complete reachable graph and disjointness follow by checking
the displayed actual terminal pairs and every horizontal TP--BP contact;
the verifier independently reconstructs this graph from the physical board.

Define the cheapest private alternative for each source:

    ell=0 if A meets G_L0;
        1 if A meets G_L1 or the cap is CB;
        infinity otherwise.
    r=0 if A meets G_R0;
      1 if A meets G_R1;
      infinity otherwise.

Earlier alternatives take precedence. Let j mean J is in A.

**Theorem 1 (exact two-source joint compensation).** Full payment is
possible if and only if at least one of the following costs is finite:

    ell+r;     ell if j;     3+r if j.                       (2)

Its minimum actual-link cost is the minimum of those finite alternatives.
If no full payment is possible, the value is1 whenever ell or r is finite
or j holds, and otherwise0. At value1 the minimum cost is

    min(ell,r,0 if j).

These formulas hold for every subset A of original intervals, regardless
of how many individual units a class contains or which units are retained.

**Proof.** A paying route for L ends at its private alternative or J;
a route for R ends at its private alternative or J. The reachable-graph
classification excludes any other destination, including old whole betas.
Two paid routes cannot both consume J, whose original capacity is one.
Thus full payment has precisely the three cases: both use private
alternatives, only R uses J, or only L uses J. Their respective costs are
exactly(2), so these give lower bounds.

Conversely choose an available original interval attaining each finite
private cost, or L's actual private beta in CB. The two sources' mixed
branches have disjoint owners; private classes are mutually disjoint and
exclude J. Hence each of the three choices lifts to two actual routes with
no repeated mixed owner, BP entry, whole beta or original interval.
The three-link chain attains L's cost3, and R's J route costs0. These lifts
attain all finite values in(2). The value0/1 statements follow by the same
single-route alternatives. QED.

Theorem1 is a general lemma for any two-source allocation network with this
branch disjointness and one shared unit; replacing3 by any chain toll h
gives the same proof. Its application here includes the entire original
network, not a selected subset of owners or terminal links.

## 4. A precise compensation repair and its actual link price

In E,T,C, reserve all original intervals except J. Both L and R individually
can be paid, but together the optimum is

    V=1, c=0.

Both non-cap whole betas remain in the network; they are unreachable.
This is the promised failure of treating the once-private J as safe to
deduct for R while retaining L's apparent access to the same resource.
It does not describe the unrestricted original interval pool, which still
has V2,c0.

Now release K as well. R can move onto K, leaving J to L. Theorem1 gives

    V=2, c=3.

The extra original resource really restores the missing payment, but it
forces three actual links. This is a joint reassignment of two sources,
not a second use of J. By contrast, completing the left cap to CB supplies
its exclusive whole beta and gives V2,c1 with J alone.

For q separated copies let F be the CB copies and E the copies with K
released. Make every J available and reserve every other original interval.
Per copy the exact outcomes are

| Filled cap? | K available? | V | c |
| --- | --- | ---: | ---: |
| no | no | 1 | 0 |
| no | yes | 2 | 3 |
| yes | no | 2 | 1 |
| yes | yes | 2 | 1 |

**Corollary 2 (simultaneous repair without repeated credit).** Equation(1)
holds for every q,F,E, with deficit q-|F union E|. Equivalently

    V=q+|F|+|E|-|F intersect E|,
    c=|F|+3(|E|-|F intersect E|).

**Proof.** The copies' endpoint and terminal-link graphs are disjoint and
all their resource identities differ by band coordinate. Thus their
feasible packings and costs add. Sum the four cases above. An overlap copy
has only two sources; its beta repair is already cheaper than the K/J
reassignment, so K gives no extra payment there. QED.

This explicitly excludes the incorrect q+|F|+|E| count when repairs overlap.
The formulas are for this stated resource availability on the actual
boards. Reservations are not silently identified with geometric deletion.

## 5. Verification, formal scope and limits

The solver-free checker is

    python3 develop/check_reserve_boundary_split.py --output output/reserve-boundary-split-validation.json

It checks the saved full freezing certificate, reconstructs all four cap
boards, proves the five-class adapter by comparing every original unit's
two source distances, and checks the absence of a shared mixed gate or
accessible fork. It then compares Theorem1 against complete original fork
flow and independent ordinary/full primitive packing on6246availability
models: all5466singleton/pair identity subsets,256class controls,512larger
random subsets and12named full/shared/released controls. There are12492
independent primitive comparisons. It also checks all584cap/release choices
in up to3copies, with72independent copy packings. These computations check
coordinates and implementation; the projection/lift proves every A and the
disjoint-copy argument proves every q.

[ReserveBoundarySplit.lean](../formal/SubQuorum/ReserveBoundarySplit.lean)
checks concrete feasibility and actual inductive complete freezing of all
four boards, the new right-alpha path and mixed pair, the surviving
singleton geometry and three actual TP--BP chain links. It also proves the
general three-alternative full-payment budget, sole shared-unit capacity,
and arbitrary-list overlap/cost ledgers. Nine audited declarations pass
local Lean4.33.0 with only standard propext/Classical.choice/Quot.sound.
The exhaustive whole-support graph adapter, original interval grouping and
general allocation projection/lift are written/Python checked; they are not
claimed as end-to-end Lean flow semantics. No new external review was
received.

This settles a genuine boundary-ownership change and its exact joint
capacity/cost. It does not prove that arbitrary rematchings always inherit
enough replacement units. The next geometric question is to identify a
joint cut condition that guarantees those replacements when many migrated
sources share resources, including cases with shared mixed or BP gates.
The two-source disjoint-branch hypothesis cannot be dropped without checking
those capacities. Public main, PR3, shared CI, the submitted11October
manuscript and correspondence are preserved.
