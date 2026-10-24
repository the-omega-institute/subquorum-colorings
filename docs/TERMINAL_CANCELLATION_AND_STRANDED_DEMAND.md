# Terminal cancellation, selected-cap compensation and stranded direct ports

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We resolve the bookkeeping step after the frozen missing-port BP injection.
Disjoint TP--BP cancellation links give a new path/cycle decomposition whose
signed whole-path credit is exactly unchanged. This permits virtual connectors
without reusing an original path or either of its terminals. It also exposes a
specific failure of the proposed continuation: a completely frozen, uniquely
matched family transfers a TP--TP demand through mixed paths, yet leaves a full
unported TP--TP demand after every available horizontal continuation is used.
The target packet inequality remains true in this family. It is the automatic
direct-port-exposure/credit rule that fails. A further selected-cap access
lemma reaches real interval resources and compensates the entire family,
including its cropped physical packets and separated stacks.

## 1. Hypotheses and the general cancellation theorem

Use the feasible pair (T,M), matching-closed aligned two-row packet J, physical
columns, actual PP-path decomposition, interval balance L and boundary budget
B from INTERVAL_CONNECTOR_CYCLES_AND_MISSING_PORTS.md. In particular the first
column is BB in each band, and the last column has a blank corner. With
S=|J|/2-|T intersect J|-|P intersect J|/2, the original exact ledger is

    S=L+beta-alpha.                                             (1)

Every noncyclic PP component has two distinct original terminal endpoints,
each labelled TP or BP. Pair those endpoints by one abstract strand edge,
retaining the actual PP path as its owner. Original pure PP cycles have zero
charge and are set aside. Let C be ANY matching of these terminal vertices
whose edges join opposite labels. For the geometric application the links
are horizontal endpoint adjacencies in a band. The conservation theorem
itself needs neither horizontal adjacency nor freezing.

Add the links C to the strand edges, keeping edge identity and parallel
edges. Each terminal has one strand incidence and at most one link incidence.
Every resulting component is therefore an alternating path or an alternating
cycle. A path has two free original terminals and defines a virtual strand.
A cycle has none. A link may coincide geometrically with an actual matching
edge of a mixed one-edge PP path; it then gives two parallel edges and a
legitimate two-edge cycle, rather than a new resource.

Let alpha', beta', gamma' count virtual strands by their free terminal labels.
Then, for every permitted matching C,

    beta'-alpha'=beta-alpha,
    alpha'+beta'+gamma'=alpha+beta+gamma-|C|,
    S=L+beta'-alpha'.                                          (2)

Proof. Give a TP terminal weight -1 and a BP terminal weight +1. An original
alpha strand has terminal sum -2, a beta strand +2, a mixed strand 0. Every
link consumes one terminal of each label, of total weight zero. Summing within
one connected component leaves precisely its two free terminal weights if
it is a path and zero if it is a cycle. Thus a path with d alpha owners and
b beta owners has b-d=-1,0,+1 according as its free labels are TP--TP,
TP--BP, BP--BP; a cycle has b=d. This proves the first identity in (2)
component by component. Every terminal not incident to a link remains free;
there are 2(alpha+beta+gamma)-2|C| such terminals. Dividing by two proves the
second identity. Substitute the first identity into (1) for the third.

There is a sharper ownership identity. In each cancellation component let
d and b count its original alpha and beta owners. The preceding endpoint
classification shows that its virtual alpha count is max(d-b,0), its
virtual beta count max(b-d,0), and that these are 0 or 1. This includes a
cycle, for which d=b and both counts are zero. Define

    R=sum over cancellation components min(d,b).

Then, exactly,

    alpha'=alpha-R, beta'=beta-R, 0<=R<=min(alpha,beta).        (2a)

Each beta owner belongs to one component even when both its terminals are
linked, so (2a) charges each unit resource at most once. In particular if
beta=0, EVERY cancellation matching leaves alpha'=alpha and beta'=0.
Mixed paths alone can transfer demands but can never pay any of them.

There is a geometric ownership refinement for the proved injection C:
suppose every TP source of C is a terminal of an ORIGINAL alpha path.
Contract each strand edge to its original path owner. The resulting
multigraph has edges from alpha owners to beta or mixed owners. Every
owner has degree at most two; each mixed owner has degree at most one
because it has only one BP terminal. Delete these mixed leaves. In each
remaining component the alpha and beta owners alternate along a path or
cycle, including the possible two-parallel-edge cycle. Such a component
has an explicit matching of min(d,b) distinct alpha owners to distinct
beta owners: on a path pair alternately starting at an end of the larger
part (either end if equal), and on a cycle use alternating edges. Removing
mixed leaves has not disconnected the nonleaf owner graph. An isolated
alpha owner simply contributes min(1,0)=0.

This constructs an allocation of exactly R ORIGINAL alpha demands to R
DISTINCT ORIGINAL beta path resources, each along one chosen original
injection link. It has maximum cardinality within those links, since each component
has only d demands and b resources. Remaining beta owners, alpha demands
and all BB--TT interval components retain separate identities. In
particular two TP demands linked to opposite terminals of the same beta
path do not get two units: at most one of them is matched to that resource.
The unallocated demand count is exactly alpha-R=alpha'. This is a partial
compensation lemma with an explicit allocation and exact residual; it does
not claim that the residual is always zero.

In particular cancellation cannot manufacture beta credit. A chain with one
alpha and any number of mixed owners still carries exactly one full demand
whenever its free terminals are TP--TP. A beta owner has ONE unit of credit,
even when both of its terminals are used in different links. Componentwise
accounting uses that owner once. A cancellation cycle has net zero credit.

## 2. The virtual connector ledger and a conditional compensation lemma

The physical BB--TT intervals and their B marked boundary intervals are
unchanged. Give any subset of virtual TP--TP strands with a BB port at both
free terminals one chosen port per terminal. Connect their two interval
owners. Let a' be the number chosen, and u'=alpha'-a' the number omitted.
Keep loops and parallel connectors. Define h'_j to count connector PATH
components with j boundary marks, j=0,1,2, including isolated vertices.

The connector graph has degree at most two. Indeed a side of a physical
interval can only be used by the immediately adjacent TP column, which
contains a single original terminal. That terminal is free in at most one
virtual strand. This proof depends only on terminal identity; a virtual
strand need not be an original matching path or satisfy its old mate lemma.
Every boundary mark has degree at most one and cannot lie on a connector
cycle. The same path/cycle count as before gives

    L-a'=h'_0+h'_1+h'_2,       B=h'_1+2h'_2.

Together with (2) these yield the exact theorem

    S-B=h'_0+beta'-h'_2-u',
    S>=B  if and only if  h'_2+u'<=h'_0+beta'.                  (3)

There is no additional cancellation-cycle or connector-cycle debit. The
former has zero signed strand credit; the latter has zero Euler difference
and is already excluded from h'_0. Distinct objects in (3) have distinct
owners: each virtual strand is a component of the terminal graph, and each
interval path is a component of the connector graph. This does not assert
that their entire original 2-by-2 physical tile supports are disjoint.

A useful sufficient lemma follows. Suppose complete freezing holds, C consists
EXACTLY of the proved injection links covering EVERY missing terminal of ORIGINAL alpha
paths, and every target of C belongs to an ORIGINAL beta path. Then EVERY
free TP terminal of a virtual alpha strand has an original BB port. An
original alpha terminal lacking a port is incident to C and cannot be free;
original mixed paths are untouched and cannot be owners of an affected
component, so their TP terminals cannot appear at a new alpha endpoint.
Thus all virtual alpha strands can be connected and u'=0. If their chosen
connector graph has no twice-marked path (h'_2=0), (3) proves S>=B.
More generally h'_2<=h'_0+beta' suffices. The targets-in-beta hypothesis is
essential to this argument; no assertion that it always holds is made.

For physically disjoint packets with complete original receiver closure,
the previously proved outside ledger remains

    global margin=sum_J S_J + D_out-q+R_out-2N_out.

Consequently packets satisfying this sufficient lemma give coefficient one
when q+2N_out<=sum_J B_J+D_out+R_out. This is a conditional class, not a
universal improvement of the 5/6 bound. The original receiver correction
and physical packet ownership must still be checked exactly once.

## 3. A fully specified frozen obstruction family

Take even integers W>=6 and H>=4 and the board (W+12)-by-(2H+12), with zero-based
coordinates. Define T to be

    {(4,3),(4,5),(4,7),(5,2),(5,8),(6,6),(7,5),
      (W+4,2),(W+4,H+4)}
    union {(W+5,c): c=3,5,...,H+3}
    union {(W+2,c): c=6,8,...,H+2}.

Define actual matching M by the following disjoint lists:

    (r,3)--(r+1,3), r=5,7,...,W+3;
    (r,4)--(r+1,4), r=6,8,...,W+2;
    (5,4)--(5,5), (5,6)--(5,7);
    (W+4,c)--(W+4,c+1), c=4,6,...,H+2;
    (W+3,c)--(W+3,c+1), c=5,7,...,H+1.

All other cells are blank. This is exactly the missing-port family from
INTERVAL_CONNECTOR_CYCLES_AND_MISSING_PORTS.md: transform the completed
neutral-pair construction by (r,c)->(c,r-1), add its two feasible cap
selections, and blank-pad the board. Its previously established feasibility,
complete freezing and unique actual matching are therefore inherited. The
companion independently compares the direct coordinate lists with that
construction. There are H+9 selections and W+H matching edges, and

    alpha=1, beta=0, gamma=H+1,
    S=WH+5W+10H+63, B=W+12.                                  (4)

The original alpha path has terminal endpoints (5,3),(W+4,3). Their only
horizontal BP neighbors are (5,4),(W+4,4). Thus the proved injection is
forced, and its targets lie on two different MIXED paths. Their other
endpoints are (5,5),(W+4,5). All four old and new TP terminals have no BB
port. After this first cancellation the three owners (one alpha, two
mixed) form one virtual TP--TP strand. Its inventory is

    alpha'=1, beta'=0, gamma'=H-1, u'=1.

The unresolved full demand has moved, not decreased.

## 4. Exhausting every horizontal continuation still leaves the demand

In the upper terminal row 5, the consecutive physical column types are

    BT at 2, TP at 3, BP at 4, TP at 5, BP at 6, TP at 7, BT at 8.

In the lower terminal row W+4 they are

    BT at 2, TP at 3, BP at 4, TP at 5, ..., TP at H+3, BT at H+4.

Every displayed TP lacks a BB port: an adjacent column is BP or BT. The
upper row has three such TP and two BP; the lower has H/2+1 TP and H/2 BP.
These are all their horizontal BP neighbors. Hence no matching of horizontal
TP--BP links can cover all these missing TP terminals. This is a direct
pigeonhole obstruction, for unbounded row length H/2+1. The first injection
theorem is not contradicted: only the leftmost TP in either row belongs to
an ORIGINAL alpha path. The other TP terminals belong to mixed owners.

There is a unique maximal continuation LINK SET, up to interleaving advances
at the two ends, that keeps every previous link and always advances a free
alpha endpoint to an unused BP. On the upper row use
(3,4), then (5,6); on the lower row use (c-1,c), c=4,6,...,H+2, with the
row coordinate fixed. Each step advances through a distinct actual mixed
one-edge path. It ends at (5,7) and (W+4,H+3). Both terminals still lack
BB ports, and their only horizontal BP neighbor has already been used.
All intermediate cancellations preserve one full demand by (2).

The horizontal Hall obstruction also rules out repairing this strategy
merely by reassigning all links until every missing TP is covered. It does
not rule out a future method using other bands, BB--TT interval resources,
or a joint allocation that leaves some mixed terminals free. It refutes
the claims that this cancellation automatically exposes ports, that every
encountered BP contributes one unit, or that the frozen injection can be
reapplied to virtual alpha endpoints without a new hypothesis.

In fact there is a stronger obstruction to ALL horizontal cancellation
matchings, not only the displayed forward continuation. Let V_* be ALL
terminal vertices in rows 5 and W+4. Their original strand edges are the
single alpha edge between (5,3),(W+4,3) and the mixed one-edge paths listed
in these rows. Each original strand with an endpoint in V_* has both
endpoints there. Every possible horizontal opposite-label link from V_*
also stays in V_*: the displayed alternating runs contain all terminals
in these rows, and the adjacent caps are selected, not endpoints.
Thus V_* is closed for the original strands and for ANY horizontal C.
Its original inventory is one alpha, no beta and H/2+2 mixed owners.

Apply the component proof in Section1. A component with no original beta
owner cannot have two free BP terminals, since that would require b-d=1
with b=0. The unique component containing the original alpha owner must
have two free TP terminals, since b-d=-1; it cannot be a cycle. All other
components have no alpha or beta and contribute no new alpha. Consequently
EVERY horizontal cancellation matching C on the full packet leaves exactly
one virtual alpha strand, with both endpoints in V_* and neither having a
BB port. It has one endpoint in each of the two rows, since the original
alpha strand is the only strand or link connecting those rows. In particular

    alpha'=1, beta'=0, u'=1 for EVERY horizontal C.             (4a)

This remains true after arbitrary reassignment or cancellation cycles, and
includes choices that use TP terminals having ports elsewhere in the packet.
It is an obstruction to the entire strategy of exposing both ports solely
by horizontal TP--BP cancellation. A successful proof needs additional
geometry or resources. No assumption about keeping earlier links is needed
for (4a).

For the smallest W=6,H=4, complete freezing can also be checked without
relying on the prior family proof. Successive valid layers of endpoints are

    0: (5,3),(5,7),(10,3),(10,7)
    1: (5,5),(9,6),(10,5)
    2: (6,4),(9,4)
    3: (7,3),(7,4),(8,3)
    4: (6,3),(8,4)
    5: (5,4),(9,3)
    6: (5,6),(10,4)
    7: (9,5)
    8: (10,6).

In layer0 each endpoint has two original selected nonmate neighbors. In
every later layer it has two distinct nonmate neighbors that are selected
or have an actual mate in an earlier layer. The permanent output lists
the two actual witnesses for every event, and all 20 endpoints occur.
Disjoint copies, translated by row offset W+12 and using the same layered
certificate, give arbitrarily many simultaneously stranded unit demands.

## 5. Local deficit and what has not failed

For the forced first injection and for the maximal continuation in this
family, the sole virtual alpha strand has no usable connector. All L=S+1
BB--TT intervals are isolated. Exactly B are marked, so

    h'_2=0, u'=1, beta'=0, h'_0=S+1-B,
    h'_0+beta'-h'_2-u'=S-B=WH+4W+10H+51>0.                   (5)

Thus this family has ample REAL interval reserve, despite having no beta
credit and despite the failed horizontal continuation. The target S>=B
holds. Any successful general proof must explain how its demand can reach
and own an interval reserve, or use a different joint counting argument.
There is no justification for erasing u' when a cancellation link is used.

The obstruction does not rely on the large blank padding of the common
board used to stack different families. Remove that padding and take the
physical packet

    J_*={4,...,W+5} times {0,...,H+5}.

It contains ALL selected vertices, ALL matching endpoints and their complete
original 2-by-2 receiver tiles. Indeed every endpoint lies in rows5..W+4
and columns3..H+3; even a unit square containing it extends by at most one
row or column, staying within J_*. The crop begins at even coordinates
and ends at odd coordinates, so it is a union of whole original tiles.
Its dimensions are (W+2)-by-(H+6), both even;
its first and last columns are BB in every band. Thus B_*=W+2 and, exactly,

    S_*=(WH)/2+2W-H-3,
    S_*-B_*=(W/2-1)H+W-5>0.                                (6)

The terminal graph, closed set V_*, and all-horizontal obstruction (4a) are
unchanged. In the smallest case this physical receiver-closed packet is
8-by-10, has 13 selections and 10 actual matching edges, and has S_*=17,
B_*=8. Its single unported virtual demand still persists for every
horizontal C, while h'_0=10 supplies enough interval reserve in the exact
ledger. This is an explicit compact rule obstruction with honest receiver
ownership, not an artefact of distant empty bands.

## 6. Verification scope

The companion checker constructs the actual PP paths, original terminal
pairing, disjoint links, cancellation components and virtual connectors
independently from the geometric data. It checks signed credit within each
component, total free terminal count, boundary degree restrictions and (3).
It also checks the direct family, the forced first injection, full freezing,
independent forced matching, row Hall counts, maximal continuation, and
two-edge mixed-owner cancellation cycles. Symmetries and mixed stacks test
ownership and coexistence. Abstract controls include balanced cycles and
the case in which both ends of one beta owner are used; those controls are
not claims that every abstract graph occurs in a frozen grid.

The Lean companion verifies the generic signed surgery and finite-list
inventory mechanism, including the common nonnegative drop and the
impossibility of reducing alpha when beta=0. Grid geometry, full freezing of the family, and the
virtual connector adapter remain written proofs; finite validation does
not replace them. The general grid compensation theorem remains open.

Local Lean4.33.0 passes all 22 theorems and their 22 individual ordinary-axiom
audits with no errors, warnings, sorry or native evaluation. The final
preflight reports 46 percent free memory and no real lean/lake executables.
The permanent checker passes 15033 terminal models, including all 13376
horizontal cancellation matchings for six parameter pairs, 1135 geometric
virtual-connector models, 143 independently forced unique fully frozen
family parameters and their 143 cropped physical receiver-closed packets,
eight symmetry controls, 32 stacks and 27 mixed stacks.
The universal all-horizontal obstruction is proved by closed ownership in
Section4; these finite checks do not establish that universal quantifier.

## 7. Selected-cap access: a compensation lemma with unique side ownership

An extended access of a free TP terminal to a physical BB--TT interval is
either its existing immediately adjacent BB port, or the following pattern
of three consecutive columns in the SAME band:

    TP -- BT -- BB,

where the intermediate BT selection lies in the SAME physical row as the
terminal endpoint. All three columns must lie in J. Reflection of the
pattern is allowed. The BB column belongs to the accessed interval. Choose
one such access at each free terminal of any selected virtual alpha strand.
The intermediate selection is already part of T and creates no new credit.

The unique-side-ownership lemma holds for this enlarged access relation.
Fix one side of one physical interval and inspect the immediately external
column. If it is TP, the only possible user of this side is its single
terminal, by direct access. If it is BT, only selected-cap access is possible:
the next column must be TP, its single endpoint must be in the selected
corner's row, and that endpoint is the only possible user. These two cases
are mutually exclusive. Every access reaches an END of the interval, since
the intervening TP or BT column is not part of a BB--TT interval. Thus a
side is used at most once, an interval has degree at most two, and a marked
boundary interval still has degree at most one. A BT mediator also cannot
serve two selected-cap users: one neighbor column must be BB and the other
TP, so its orientation and sole candidate user are fixed. Different bands
have disjoint physical columns and selections.

Consequently, with h^cap_j counting PATH components of the extended connector
graph and u_cap counting omitted virtual alpha strands, the exact ledger is

    S-B=h^cap_0+beta'-h^cap_2-u_cap.                           (7)

This is a general written theorem under the original packet hypotheses,
for ANY opposite-label terminal matching C and any permitted subset of
extended connectors. No vertical actual-mate assumption for a virtual
terminal is used. In particular the explicit sufficient compensation lemma
is: if every virtual alpha strand has chosen extended accesses and their
connector graph has no twice-marked path, then S>=B. More generally an
allocation of h^cap_2 demands to distinct h^cap_0/beta' resources suffices
when u_cap=0; with partial coverage the demand count is h^cap_2+u_cap.
The outside receiver ledger and coefficient-one corollary in Section2
apply with the same unchanged physical ownership hypotheses. This does not
establish the availability of extended access for arbitrary configurations.

Here is a nonvacuous uniform application that pays the stranded family.
Use the cropped physical packet J_* in (6), and choose C to be EMPTY. Each
original alpha terminal, at column3 in rows5 and W+4, accesses BB column1
through the selected BT cap at column2. These two BB columns are isolated
interval vertices in distinct bands. Neither is marked: the left boundary
mark is column0, and the right boundary is column H+5. Adding the one alpha
connector merges two isolated unmarked intervals into one unmarked path.
Thus exactly one interval reserve is consumed, with no reused side, terminal,
intermediate selection or original path:

    u_cap=0, h^cap_2=0, beta'=0, h^cap_0=S_*-B_*.

For W=6,H=4 the initial ten unmarked intervals become nine unmarked connector
paths; one unit compensates the unique missing-port demand. The same access
at column1 in each translated copy uses distinct original interval vertices,
so it pays every demand in separated stacks, with each unit accounted once.
This is a proved compensation family, not merely finite evidence.

Choices matter. After the forced FIRST injection, the free TP endpoints
are at column5 with BP columns on both sides; neither has direct nor selected-
cap access, so u_cap=1 still. After maximal horizontal continuation both
endpoints do have cap access on their right. On the common padded board
these reach unmarked intervals and pay the demand. On the CROPPED packet
with H=4 they reach two marked final-column intervals instead, producing
h^cap_2=1 rather than an automatic bound: the u debit has moved to a boundary
collision debit. For H>4 only the lower target is marked and no such double
collision occurs. The original left-cap choice C=empty avoids this issue
for every W,H. Access availability alone must never be substituted for
the exact boundary/ownership count in (7).

The permanent checker validates all interval-side candidate users, including
both direct and cap access before choosing any connector. Its 496 extended-
access ownership models include 143 cropped compensation families, their
first-injection and maximal-continuation controls, 32 separated stacks and
27 mixed stacks and eight symmetry images. Thirteen H=4 parameter controls explicitly retain the
twice-marked debit after the right-cap choice. The graph arguments above
prove the general lemma; the controls test its adapters and sharp limitations.

## 8. Uniform direct freezing and unique-matching proofs

The all-parameter family also has certificates directly from its coordinates,
without an appeal to enumeration or the prior constructor. Put R=W+4,
A_r=(r,3), B_r=(r,4), U_c=(R-1,c), L_c=(R,c). Call an endpoint retained once
its ACTUAL MATE has frozen. The following is a serial freezing schedule;
the pair after each event gives its two distinct nonmate witnesses.

1. Freeze A_5,(5,7),L_3,L_{H+3}, each using its two adjacent selections.
2. Freeze (5,5), using selection (4,5) and retained (5,6).
3. For odd c=H+1,H-1,...,5, freeze L_c using selection (R+1,c) and retained
   L_{c+1}. For even c=6,8,...,H+2, freeze U_c using selection (R-2,c) and
   retained L_c. Freeze U_4 using retained U_3,U_5.
4. For even r=6,8,...,R-2, freeze B_r using retained B_{r-1},A_r, then
   A_{r+1} using retained A_r,B_{r+1}.
5. For even r=R-2,R-4,...,6, freeze A_r using retained A_{r+1},B_r, then
   B_{r-1} using retained A_{r-1},B_r.
6. Freeze (5,6) using selection (6,6) and retained (5,5).
7. For even c=4,6,...,H+2, freeze L_c using retained L_{c-1},U_c. If c<=H,
   next freeze U_{c+1} using retained U_c,L_{c+1}.

Each witness is adjacent, differs from the event's actual mate, and is
selected or has its actual mate strictly earlier in this schedule. For
example U_3 is retained from the initial freezing of L_3, while U_5 is
retained after U_6 froze in step3. In the forward and backward loops these
dependencies propagate in the displayed direction. The final alternating
loop uses the just-frozen mate at each advance. Every endpoint occurs once,
so complete freezing holds for all allowed W,H. The checker verifies these
explicit witness pairs for all 9152 endpoint events in the parameter controls.

For unique matching, remove the following forced edges in the displayed
order, always taking the first endpoint as a leaf of the remaining
endpoint-induced graph:

    (5,7)--(5,6), (5,5)--(5,4), A_5--A_6;
    B_r--B_{r+1}, A_{r+1}--A_{r+2}, r=6,8,...,R-2;
    L_c--L_{c+1}, then U_{c+1}--U_{c+2} if c<=H,
      c=4,6,...,H+2.

At the first step (5,7) has just the neighbor (5,6); the next two leaves
appear successively. In the column loop, the previously removed two
neighbors leave only the displayed mate of each new leaf. In the final
ladder loop, each L_c loses its preceding horizontal neighbor and U_c,
and each U_{c+1} loses U_c and L_{c+1}, leaving exactly the displayed mate.
These disjoint forced edges exhaust all endpoints, proving uniqueness for
every W,H. The checker verifies the template for all 4576 matching edges
in the parameter controls, independently of its generic leaf-elimination
and freezing algorithms.

## 9. Independent review

The initial review 9f873d31-77a5-4422-8e3b-51e15dc8866d completed ACCEPT at
15:06:52 UTC. The final follow-up 1730792d-c0a6-47d3-af60-634fa8c294f4
completed ACCEPT at 15:26:29 UTC, actual gpt_6/pro. It independently accepts
the common drop and explicit original-link allocation, closed-row obstruction
for all horizontal matchings, cropped physical receiver closure, selected-cap
ownership and compensation, the H=4 right-boundary debit, and the uniform
written freezing/unique-matching schedules. It also confirms the stated
limited scope of the Lean development. This is not execution certification.

The final 40633-character request matches the recorded conversation exactly;
the complete 18985-character response agrees across the original DONE stream,
completed task and session. Original stream session52326 exits0. The full
response is in output/terminal-cancellation-and-stranded-demand-followup-oracle.json.
Minor clarifications now specify maximum cardinality for the owner matching,
retain u_cap=0 when only boundary-collision demands are allocated, and spell
out the coordinate enclosure proving physical receiver closure. No owned
review remains live. General grid compensation remains open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
