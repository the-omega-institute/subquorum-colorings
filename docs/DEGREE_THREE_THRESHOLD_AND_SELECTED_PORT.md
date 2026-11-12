# Degree three, maximum degree five, and a safe selected-leaf port

**Theorem.** For every integer k>=1 there is a finite simple two-connected
bipartite graph G_k of minimum degree 3 and maximum degree 5, with a
specified inclusion-minimal two-star-forming set S inducing P_3's and
isolates, such that

    n=28k, |S|=16k, beta_2(G_k)=14k, d=2k=n/14.

Here beta_2 is the unrestricted dissociation number, and formation uses
not necessarily induced K_(1,2). The selected gap attains

    d=Delta*n/(12Delta+8delta-14), delta=3, Delta=5.

Thus the degree coefficient is sharp at its necessary threshold
Delta=4delta-7 also for delta=3. Together with the dense-witness theorem,
this settles threshold sharpness for EVERY integer delta>=3. It concerns
the specified minimal selected-component class, not an exact SF_2 value.

The crucial port edge joins a selected leaf to an outside connector.
Every edge with both endpoints outside the selected set is unsafe in the
base: deleting it raises beta_2 from 14 to 15. Consequently the example
also shows why restricting a composition search to outside-outside edges
can miss a valid degree-preserving construction.

## The 28-point base and its deletion

Use left and right blocks j=0,1, each with local path a-x-c-y-b-i.
Select c,x,y,i in every block. Cross-witness edges form K_(4,4) minus
b_0^L b_0^R and b_1^L b_1^R. Thus all a-witnesses are universal to the
opposite witnesses, and the b-interface consists of the off-diagonal
matching b_0^L b_1^R, b_1^L b_0^R.

Add A_0,A_1 on the colour of the left centres, B_0,B_1 on that of the
right centres. Each pair meets both i's in its own wing. Own x_0 meets
index 1, own x_1 index 0; own y_0 meets index 0, own y_1 index 1.
Finally A_0 meets right c_1, A_1 right c_0, B_0 left c_1, B_1 left c_0.
No other connector edges occur. Call this F, and set

    e=x_0^L A_1, F^-=F-e.

All selected vertices have degree 3 in F; every outside vertex has
degree 5. In F^- the two ports have degrees 2 and 4. The completed
cyclic construction below restores their degrees.

Select c,x,i in the left blocks and x,y,a,b in the right blocks, with
no connectors. This dissociation set has size 14 in F and F^-; its only
edges are left cx and right xa,yb. We prove the matching upper bound
for every dissociation set of F^-, without a finite optimum premise.

## Basic counts and witness patterns

Fix D in F^-. Write q_A,q_B for its chosen connector counts, m=q_A+q_B,
and w for its chosen witness count. There are four selected stars P_3,
contributing at most eight vertices to D. In a wing with q=0,1,2 chosen
connectors, at most 2,1,0 isolates i can be chosen: for q=1 their one
TOTAL neighbour capacity is shared, and for q=2 an i would have two
chosen neighbours. Thus the total isolate count is at most 4-m. If
w<=2, immediately

    |D|<=8+(4-m)+w+m<=14.                            (1)

We may assume w=3 or 4. The complete slots (L_0,R_1),(L_1,R_0) give
w<=4. If witnesses occur in both wings, each side has at most two.
Three mixed witnesses have the following exact pattern: the singleton
is b_j; on the other side are its non-neighbour b_j and one additional
witness z. The singleton and z are cross-saturated (each has a cross
neighbour in D). Four mixed witnesses must be all four b's, each
cross-saturated by the off-diagonal matching. A cross-saturated a forbids
its own x; a cross-saturated b forbids its own y and i.

With no chosen connector, witnesses in one wing give at most two full
P_6 blocks contributing eight and two witness-free blocks contributing
six. For three mixed witnesses, a cross-saturated b removes one isolate
from the usual selected capacity 12, giving 11+3=14. For four, all y
and i are absent, giving at most eight selected vertices plus four
witnesses. Hence the no-connector case holds.

For m=1,2 it suffices to prove the cases in which A_1 is chosen. If
A_1 is absent from D, the deleted edge is irrelevant and D is also a
dissociation set in F. Swapping wings and simultaneously interchanging
block indices and connector indices are automorphisms of F. They map
any single chosen connector to A_1, a same-colour pair to A_0,A_1,
and an opposite-colour pair to A_1,B_s. The image is a dissociation set
of F and hence of F^-. Thus bounds for those cases in F^- cover all.
This uses actual symmetries of the undeleted graph, not a claimed
symmetry of the one-deleted-edge graph.

## Exactly one chosen connector, A_1

Remove its at most one chosen neighbour R. Left i_0,i_1 and left y_1
are absent afterwards, as is right c_0. In left block 0, only i_0 was
forced out; in left block 1, i_1,y_1 are out. The left selected capacity
is at most four, and the right selected capacity is at most six.

If witnesses lie only on the right, the left contributes at most four
and the two full right blocks at most eight: at most twelve vertices
remain after removing the connector and R. Restoring them gives 14.

If witnesses lie only on the left, left block 0 is the path
 a_0-x_0-c_0-y_0-b_0, contributing at most four; left block 1 is a P_3
plus an isolated b_1, contributing at most three. Together with right
selected capacity six, the residual count is at most thirteen. A total
exceeding 14 would have to be 15, attaining every bound and |R|=1.
The four-point optimum of that P_5 is uniquely {a_0,x_0,y_0,b_0}; the
three-point optimum of the other four-vertex graph includes b_1. Right
x_0,y_0 are also chosen, since right block 0 has centre absent and must
contribute all three x_0,y_0,i_0.

No possible A_1-neighbour can be restored: left i_0,i_1 would each have
its own chosen b and A_1; left y_1 would have b_1 and A_1; right c_0
would have its chosen x_0,y_0. These are all A_1-neighbours in F^-.
This contradicts |R|=1. Hence the total is at most 14.

For mixed witnesses, four means all b's are saturated, forcing all y,i
absent. The total is then at most eight selected vertices, four witnesses
and the connector, hence 13. With three mixed witnesses, if a saturated
b lies on the right, its block has selected capacity at most two instead
of three even after the removal, giving residual selected total at most
nine. Restoring R and A_1 gives at most 9+3+2=14.

The only other pattern is a saturated singleton left b_j and right
b_j plus a saturated right a_k. If j=0, right c_0 is absent and the
chosen right b_0 permits at most one of y_0,i_0; that block contributes
at most two. If j=1,k=1, the right block has both witnesses chosen and
a_1 saturated, so its selected contribution is at most two. If j=1,k=0,
right block 0 has both c_0,x_0 absent, leaving only y_0,i_0, at most two.
In every case the right selected capacity loses one, giving the same
9+3+2 bound. This completes m=1.

## Two connectors of the same colour, A_0,A_1

Both left i's are absent. The left selected capacity is at most four;
the right at most six. We need selected total at most nine when w=3,
and at most eight when w=4.

Any left block with both witnesses chosen has selected contribution at
most ONE, even in F^-. In block 0, y_0 is forbidden by its owner b_0
and A_0; x_0 can pair to a_0 but then c_0 is absent. In block 1, both
leaves are forbidden by their owners and their chosen connectors, leaving
only c_1. A full right block has selected contribution at most two,
since the P_6 has dissociation number four including its two witnesses.

For w=4 in one wing, these facts give either left 2 plus right 6, or
left 4 plus right 4. For mixed w=4 all b's are saturated. Left block
0 permits at most c_0,x_0, left block 1 at most one of c_1,x_1 (x_1
already meets A_0); the right permits at most its four c,x. This is at
most seven selected vertices. All w=4 cases therefore satisfy the cap.

For w=3 in one wing, at least one block in that wing has both witnesses.
It gives either left at most 1+2=3 and right 6, or left 4 and right at
most 2+3=5. For mixed w=3 with singleton on the right, its saturated b
forbids its isolate, giving right at most five and left four.

It remains that the singleton is left b_j. If j=1, y_1 is absent, and
x_1 cannot coexist with c_1 because it meets A_0. Thus left block 1
contributes at most one, left block 0 at most two: left at most three,
right at most six.

If j=0, the right pair is b_0,z. For z=b_1 the saturated b_1 removes
one right isolate; for z=a_0 the full block with saturated a_0 has
selected contribution at most two. Both give right at most five and
left four. For z=a_1, right selected total six would require all its
isolates and two star vertices per block. The chosen b_0 and i_0 force
y_0 absent, so block 0 must contain c_0,x_0. Saturated a_1 forces x_1
absent, so block 1 must contain c_1,y_1. Both right centres are chosen,
using the neighbour capacities of A_0,A_1. Thus left x_1,y_1 are absent;
its block 1 has only c_1, while block 0 contributes at most two. Left
then contributes at most three, again total at most nine. All cases of
w=3 follow, proving the same-colour-pair cap 14.

## Two opposite-colour connectors, A_1,B_s

Each wing has selected capacity at most five: at most four star vertices
and one isolate. If the right wing attains five, its chosen isolate uses
all B_s capacity, excluding the B_s-neighbour leaf in each right block.
Attaining two star vertices per block then requires both right centres.
In particular right c_0 consumes the capacity of A_1, so no left isolate
can be chosen. The left selected capacity is at most four. If the right
does not attain five, it is at most four and the left at most five.
Thus total selected count is always at most nine, enough for w<=3.

For w=4 only on the left, each chosen b forbids its i (which also meets
A_1). Left block 0 can contribute at most two selected vertices, and
left block 1 at most one, since y_1 has both its owner and A_1 chosen.
The right contributes at most five: total at most eight. For w=4 only
on the right, each full block contributes at most one selected vertex:
i meets b and B_s, one leaf meets its owner and B_s, and the other leaf
cannot coexist with its centre because its owner is chosen. Thus right
at most two, left at most five. For mixed w=4 all y,i are absent,
leaving at most the eight c,x vertices. This completes m=2.

## At least three connectors: an incidence bound

Let C be the actual chosen connector set, |C|=m, and put

    U_C={v in S: v has NO neighbour in C}.

Every vertex of D intersect (S minus U_C) uses at least one chosen
connector's physical neighbour capacity. Counting actual incidences gives

    |D intersect (S minus U_C)|
      <=sum_(v in D intersect S) |N(v) intersect C|
       =sum_(c in C) |N(c) intersect D intersect S| <=m.

Consequently |D intersect S|<=|U_C|+m. This inequality permits one
chosen neighbour per connector; it does not exclude all those neighbours.

For m=3 both colours occur, so no isolate belongs to U_C. Among all
star vertices c,x,y, only left x_0 has no connector neighbour at all.
Every other star vertex has exactly one connector neighbour, and each
connector has at most three star neighbours. The sole unchosen connector
therefore accounts for at most three more uncovered star vertices.
Thus |U_C|<=4, |D intersect S|<=4+3=7, and |D|<=7+4+3=14.

For m=4, U_C consists of left x_0 only. Hence |D intersect S|<=1+4=5
and |D|<=5+4+4=13. Together with (1) and the preceding cases this proves

    beta_2(F^-)=beta_2(F)=14.                         (2)

The upper cap covers every dissociation set. No exhaustive optimum is
an assumption of (2).

## All scales and minimality

The witness offsets 1 and 2 give a Hamiltonian cycle on the eight
witnesses: follow left index s, right s+2, left s+1 modulo 4. Both
offsets survive the two missing diagonal b-edges. Attach each
 a-x-c-y-b path as an open ear. Every connector has at least two old
neighbours among its own leaves and the opposite centres, even A_1
which has lost x_0. Add the connectors, then each i with its b and its
two connectors. This gives a two-connected spanning subgraph of F^-.

Take k copies of F^- and add x_0^L(h) A_1(h+1) cyclically. At k=1 it
restores e. At k>=2, removing a vertex leaves each affected piece
connected and destroys at most one link, as its two ports are distinct.
The cycle of pieces stays connected, including k=2. Both port degrees
are restored; minimum is 3 and maximum 5.

The selected subgraph is unchanged by the new edges. Every witness is
formed through its selected leaf; each connector retains an active
selected leaf neighbour even after deletion of e. Deleting x,y,c,i
from S makes a,b,a,i respectively fail to be formed. The new edges touch
only connectors and selected x's; they change none of these literal
failures, since each tested a or b has selected neighbours confined to
its own block and each i still has no selected neighbour. Thus S remains
forming and inclusion-minimal at every k.

A dissociation set restricts in each piece to at most 14 by (2). Repeating
the displayed fourteen-set attains 14k, since every new link has its
connector endpoint unchosen. This proves the theorem for all k.

## Why every outside-outside edge fails as a port

All such edges are witness-interface edges. Deleting any a-a edge
 a_u^L a_v^R gives a 15-set: choose c,y,i in all four blocks and add
both left a's and right a_v. These three witnesses induce at most one
edge and meet no chosen local x.

Deleting a-b edge a_u^L b_v^R gives another: choose witnesses
 a_u^L,b_v^R,a_(1-v)^R; choose c,x,i in right block v and c,y,i in the
other three. Its only possible cross-witness edge joins the two a's;
its chosen b meets only its own i. Reverse wings for a deleted b-a edge.

Deleting a retained b-b matching edge leaves a b with no opposite b
neighbour. Choose that b and both opposite b's, plus c,x,i in all four
blocks. The witnesses are independent and each meets only its own i.
All these sets have size 15. Since deleting one edge can increase beta_2
by at most one (remove an endpoint from any set violating the restored
edge), all outside-outside deletions have exact beta_2=15. The selected
leaf edge e instead has the exact safe cap (2).

## Verification

Run `python3 -B scripts/check_degree_three_threshold.py`. It checks the
physical family, literal deletion failures and every vertex deletion,
including the lowered-degree F^- and completed k=1,2,3,4,8. Independent
exact graph recursion checks both bases and all 54 single-edge deletions,
returning literal attaining sets. Only the four connector-x edges are
safe in that scan; every outside-outside edge yields an explicit 15-set.
These finite controls verify the written arbitrary-D proof and its
all-scale construction; they do not supply a universal inference by
extrapolation. No Lean or priority claim is made.

The independent final exact-source audit returned **ACCEPT**. It reconstructed
all 9 manifest files and ran the original checker unchanged, with
assertions enabled, terminal exit status 0. Startup-through-exit stderr was empty (0 bytes). The complete 26,108-byte report was reproduced byte-for-byte
(SHA-256 c8ff86d6ac6ef92a70ac8bab0aab869fac21e41f6f95c376f511b114e7b15924). The exact source manifest, full response and
execution scope are in `../output/degree-three-threshold-review.json`. Only this evidence paragraph
was added after the reviewed source freeze; the proof and checker are unchanged.
