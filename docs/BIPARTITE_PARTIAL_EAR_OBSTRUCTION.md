# Exact failure of partial-ear addition in bipartite graphs

The identity SF_2(G)=2k+SF_2(F) for square attachments along a partial
matching remains false when the base is bipartite, even for k=1.
We give connected bipartite graphs F_q,G_q, q>=1, with

    |V(F_q)|=10q+1, |V(G_q)|=10q+5,
    SF_2(F_q)=max(5q+1,6q-1),
    SF_2(G_q)=6q+2.                                      (1)

Here G_q is obtained by adding roots d,e with edges de,dy to F_q and
then attaching the square d-alpha-beta-e-d along de. Thus the residual
graph is exactly F_q. For every q>=2, the proposed formula gives6q+1,
one less than the true value6q+2. For q=2 this is a25-vertex example
with SF_2(F_2)=11 and SF_2(G_2)=14.

## 1. Construction and formation convention

For each c=1,...,q, take disjoint two-element sets A_c,V_c,W_c,Z_c,
with indexed vertices a_(c,i),v_(c,i),w_(c,i),z_(c,i), i=1,2, and
vertices p_c,u_c. Include exactly the edges

    all A_c--V_c edges; all W_c--Z_c edges;
    a_(c,i) z_(c,i), v_(c,i) w_(c,i),
    p_c z_(c,i), u_c w_(c,i) for i=1,2.

Add y adjacent to every Z_c vertex and no others. This gives F_q.
It is bipartite with sides

    L={y} union all (A_c union W_c union {p_c}),
    R=all (V_c union Z_c union {u_c}).

Add d,e with edges dy,de to give the base B_q. Attach two new vertices
alpha,beta with edges d-alpha,alpha-beta,beta-e to give G_q. Its sides
are L union {e,alpha} and R union {d,beta}. The one matched base edge is
de, and B_q-{d,e}=F_q. All graphs are connected. For q=2 the maximum
degree of G_q is five. No medianity or two-connectivity is asserted.

A selected set S is forming by a non-induced K_(1,2) exactly when each
outside vertex has two selected neighbours, or a selected neighbour
which itself has a selected neighbour. A selected vertex with such a
neighbour is active. Every deletion below tests the newly deleted vertex.
Since formation is upward closed, failure of every single deletion is
equivalent to inclusion-minimality.

Put T_c=A_c union V_c union {p_c,u_c}. This six-set forms its block:
every outside w_(c,i) sees v_(c,i),u_c and every outside z_(c,i) sees
a_(c,i),p_c. Deleting a_(c,i) leaves z_(c,i) with only the inactive p_c;
deleting v_(c,i) leaves w_(c,i) with only the inactive u_c; deleting
p_c or u_c leaves the deleted vertex with no selected neighbour.
These witnesses remain valid when y is outside and all other blocks
are attached as specified.

## 2. A local cap with a selected exterior vertex

Consider any one block, suppress c, and let Q be a minimal forming set
in the whole graph. The argument also permits an arbitrary exterior
attached only through y. Write a,v,w,z for the selected counts in its
four two-element groups and P,U for the selection indicators of p,u.
Let b=a+v+w+z+P+U be the block's contribution. We prove

    b<=6;
    z>0 implies b<=5;
    y selected implies b<=5.                             (2)

If z=0 then P=1, and if w=0 then U=1, since otherwise the omitted p
or u has no selected neighbour. All safe deletions used below avoid Z.
Thus selection and activity of a selected y are unchanged. For an
outside y we preserve its block contribution to formation explicitly:
either two selected Z neighbours remain, or an active Z neighbour
remains; if z=0, its selected neighbours in this block are unchanged.
External vertices see only y, so these protections make the deletions
safe in the entire graph, including G_q.

**Case w,z>0.** Selected W and Z vertices are mutually active.
A selected p is safely deletable: the newly outside p sees active Z,
and all outside Z still see active W. A selected u is safely deletable
by the same argument. Hence P=U=0. The eight-vertex core is K_(4,4)
minus a perfect matching on sides A union W and V union Z. If b>=6,
each core side has at least two selected vertices. When a+w>=3 delete
a selected A vertex, which exists since w<=2. Otherwise a+w=2 and
v+z=4; delete a selected V vertex. At least two selections remain on
each side. Every selected core vertex remains active and every outside
core vertex has an active selected neighbour. W,Z remain nonempty,
so p,u and an outside y also remain formed. This contradiction proves
b<=5 in this case.

**Case w=0,z>0.** Here U=1. Suppose b>=6. If a=v=2, delete a selected
V vertex. It has two A neighbours; the other selected V keeps all A
active; every selected Z remains active through its matched A. These
active vertices form every outside core vertex and p, and an outside
y. Thus a+v<=3 in a minimal set of this size. The remaining possibilities
and safe deletions are:

| Conditions | Forced counts | Delete |
| --- | --- | --- |
| z=1 | P=1, a+v=3 | The singleton in A or V |
| z=2, P=1 | a+v>=2 | p |
| z=2, P=0 | a+v=3 | The singleton in A or V |

In the first row the opposite A/V group remains fully selected, forming
all outside A/V vertices including the deletion. The active p-Z edge
forms all outside W,Z and an outside y. In the second row, p, all outside
W and an outside y have two Z neighbours. On A/V either both groups
remain nonempty with an active selected edge, or one is empty and the
other fully selected. In the third row the same two-neighbour argument
forms A/V after the singleton deletion, while outside W,p,y all have
two selected Z neighbours. In all rows u remains selected. All deletions
are safe. Thus z>0 implies b<=5.

**Case z=0.** Here P=1. If w=0 then U=1, giving b<=6. If w>0 and
b>=7, consider U. For U=0, counting forces (a,v,w)=(2,2,2); delete an
A vertex. The remaining A keeps both V active; both W remain active
through their matched V. The outside u and every Z have two W neighbours.
For U=1 the possible triples are exactly

    (2,2,1), (2,1,2), (1,2,2), (2,2,2).                  (3)

Delete an A vertex when a=2, otherwise a V vertex. Both A and V stay
nonempty and mutually active. Selected u and W are mutually active,
forming every outside W,Z. The newly deleted vertex is formed through
the retained A-V edge. There is no selected Z in this block, so y's
formation or activity does not change. Hence b<=6.

**Case y selected,z=0.** Here P=1 and every Z has the two selected
neighbours p,y, which remain throughout. Suppose b>=6. If w=0 then
U=1 and a=v=2; delete an A vertex. It sees two V neighbours, an active
A-V edge remains, and every outside W sees its matched V and u.

If w>0,U=0 then a+v+w>=5, giving exactly the triples (3). Use the same
A/V deletion. An active A-V edge remains. If w=2 the outside u has
two W neighbours; if w=1 the triple is (2,2,1), so the retained V pair
keeps the selected W active and forms the outside u. Every outside W
has an active selected V neighbour. Z retains p,y.

If w>0,U=1 then a+v+w>=4. If a=2,v>0 delete an A vertex; if v=2,a>0
delete a V vertex. An active A-V edge remains, and u and W stay mutually
active. Otherwise the only possibilities are w=2 and

    (a,v)=(2,0), (0,2), or (1,1).

Delete u. The newly outside u has two W neighbours, no W is outside,
and Z retains p,y. On A/V an empty group has two selected opposite
neighbours, or a=v=1 leaves an active selected A-V edge. Each deletion
is safe. This proves b<=5 and completes (2).

## 3. Exact value on the residual graph

If y is selected, (2) bounds every block by five, so |Q|<=5q+1.
If y is outside, formation of y requires some selected Z. That block
contributes at most five, and all other blocks at most six, giving
|Q|<=6q-1. This proves the upper bound in (1).

Both terms are attained by minimal forming sets. The entire left side
L has5q+1 vertices, and every right vertex has at least two selected
neighbours. It is independent, so each deletion fails at the deleted
vertex itself. Alternatively select V_1 union Z_1 union {u_1}, five
independent vertices in the first block, and T_c in each other block,
leaving y outside. The first block is formed, and y has two selected
Z_1 neighbours. A deletion in that first block fails at the deleted
vertex, while all T_c deletions have the protected witnesses in Section1.
This gives6q-1. Therefore SF_2(F_q)=max(5q+1,6q-1).

## 4. Exact value after the single square attachment

Select all T_c and the adjacent pair {d,alpha}. The6q+2 vertices form:
all blocks are formed as above, y and e see active d, and beta sees
active alpha. The block deletion witnesses remain valid since y is
outside. Deleting d leaves e with no selected neighbour; deleting alpha
leaves beta with no selected neighbour. Hence this is a minimal forming
set of size6q+2.

Every minimal forming set selects exactly two vertices of the square:
the local safe-deletion proof in the square-ear note applies, since
alpha,beta have no outside neighbours. The block cap (2) is valid with
the exterior root attached at y. If y is outside the total size is
at most2+6q. If y is selected it is at most2+1+5q<=6q+2 for q>=1.
Thus SF_2(G_q)=6q+2 exactly.

For q>=2, SF_2(F_q)=6q-1 and the exact addition fails by one with
just one ear. Disjoint unions of k copies of q=2 give bipartite bases
with k attached squares and discrepancy k, since formation and minimality
separate over components. This is unbounded error within bipartite graphs.

The violating selection uses an internally active adjacent pair in the
new square. Its mechanism differs from reliance on an externally activated
opposite pair: the adjacent pair forms y, permitting all block six-sets
to coexist, while the same union fails to form F_q. Requiring selected
roots to remain active inside their ears therefore does not rescue the
proposed exact formula. The exact dissociation addition, local two-point
cap, and lower star-forming bound remain valid.

## 5. Unbounded discrepancy with one fixed ear

In fact no additive correction depending only on the number of ears
can hold for arbitrary bipartite bases. Take s>=1 disjoint copies of
F_2 and name their exterior vertices y_1,...,y_s. Let R_s be their
disjoint union, so SF_2(R_s)=11s by componentwise formation and minimality.
Add just two roots d,e, the edge de, and all edges dy_j. Finally attach
one square d-alpha-beta-e-d. Call the result J_s. The base and J_s are
connected and bipartite, and the single matched edge is still de.

Every minimal forming set of J_s meets that square in exactly two
vertices. For each copy of F_2, the local cap (2) still applies with
the exterior attached through y_j. If y_j is omitted, its two blocks
contribute at most12; if y_j is selected, they contribute at most10,
so the whole copy contributes at most11. Each copy therefore contributes
at most12 in all cases. This gives SF_2(J_s)<=12s+2.

For attainment, select both six-sets T_c in every copy and the adjacent
pair {d,alpha}, omitting every y_j. The active d forms all y_j. Every
block deletion has the witnesses from Section1; deleting d or alpha
has the same private square witnesses e or beta as in Section4.
The resulting12s+2-set is minimal forming. Consequently

    |V(J_s)|=21s+4,
    SF_2(J_s)=12s+2,
    SF_2(J_s)-(2+SF_2(R_s))=s.                            (4)

The discrepancy is unbounded although the ear count is fixed at one
and both the base and the final graph are connected. The root degree
grows with s; no fixed maximum-degree conclusion is drawn from (4).

## 6. Verification and independent review

The all-q proof and arbitrary-exterior cap received independent **ACCEPT**.
The reviewer extracted both unchanged original checkers, verified all six
input-file hashes, executed them with assertions enabled, and reproduced
both reports byte-for-byte. The literal C++ computation enumerates all
2,097,152 subsets of F_2 and 33,554,432 subsets of G_2. It computes literal
formation for every subset; the minimality loop rejects a nonminimal set
as soon as it finds a forming deletion. All deletions of each accepted
minimal set are checked. This gives beta/SF=11/11 and13/14, respectively.

The separate named-vertex Python checker tests the three witness families
at q in {1,2,3,4,8,16,32,128}:16 graph models,24 witness sets,3,314 single
deletions and1,180 named witnesses. It does not test every integer up to128.
The general conclusions depend on the written local proof.

Section5 received a separate independent **ACCEPT**. That reviewer ran
`python3 scripts/check_single_ear_amplification.py` unchanged, with
assertions enabled, and reproduced its203-byte report byte-for-byte:
s in {1,2,3,8,16,64}, six models and1,140 single deletions. The exact
upper bound for all s comes from the written arbitrary-exterior cap.
`output/bipartite-partial-ear-review.json` preserves both full responses,
input-file hashes, observed models and execution scopes. No Lean execution
is claimed.

The [connected-residual amplification](CONNECTED_RESIDUAL_EAR_AMPLIFICATION.md)
proves a further unbounded-error theorem with the residual connected as
well. That later construction has its own independent review record;
it was not in either input reviewed above.
