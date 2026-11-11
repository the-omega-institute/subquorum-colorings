# An exact upper-to-lower star-forming composition formula

Let H be any finite simple graph on n vertices. Replace each vertex v
by a copy of the 21-vertex graph F_2 from the bipartite ear obstruction,
using y_v as its interface. Join y_u to y_v exactly when uv is an edge
of H. Call the result D(H). We prove the exact formula

    SF_2(D(H))=12n-sf_2(H),                                (1)

where sf_2(H) is the minimum size of a forming set of H, equivalently
of an inclusion-minimal forming set. SF_2 is the maximum such size.
All stars are non-induced K_(1,2), and all deletions test the newly
omitted vertex. In particular, this theorem is valid for nonbipartite H.

For nonempty H, D(H) has order 21n, minimum degree two, and maximum degree
max(5,4+Delta(H)). It is connected exactly when H is connected, and it is
bipartite exactly when H is bipartite. The induced graph on all y_v is H;
a bipartition of H extends by choosing the corresponding orientation
of each bipartite F_2 module. No median or planar assertion is made.

## 1. Blocks and a stronger activity cap

Each module contains y and two disjoint ten-vertex blocks. A block has
two-sets A,V,W,Z and vertices p,u, with all A--V and W--Z edges, and

    a_i z_i, v_i w_i, p z_i, u w_i, y z_i, i=1,2.

Only y has neighbours in other modules. The supplying arbitrary-exterior
cap in `BIPARTITE_PARTIAL_EAR_OBSTRUCTION.md`, Section 2, proves that a
block's contribution b to a globally minimal forming set satisfies

    b<=6; z>0 implies b<=5; y selected implies b<=5.        (2)

Here z is the number of selected Z vertices. We need the strengthening

    y selected and z>0 imply b<=4.                         (3)

The following proof permits arbitrary exterior attached through y.
Every deletion keeps y selected and active, so it preserves every
exterior formation condition.

First, selected p is safely deletable: every selected Z is active
through y, the newly omitted p sees such a Z, and outside Z vertices
see active y. Thus p is omitted in a minimal set under these hypotheses.
If w>0, selected u is similarly deletable through the active W--Z edge.
When w=0, u must be selected. By (2), it suffices to exclude b=5.

Suppose w>0. We have p=u=0. The core is K_(4,4) minus a perfect matching
on sides A union W and V union Z. If its selected side sizes are 2 and 3,
delete a non-Z selection from the side of size 3: a V vertex on the
second side, or an A vertex on the first. It exists because W,Z each
have size at most 2. Two selections remain on each side, making every
selected core vertex active and forming every omitted one. W and Z
stay nonempty, so p,u are formed and y stays active.

The remaining side sizes are 1 and 4. If A union W has size1, then it
is a single W_i, while all V,Z are selected. Delete V_i. It sees active
W_i; all outside A see their own active selected Z, and outside W,p,u
see active Z or W. If V union Z has size1, it is a single Z_i, with
all A,W selected. Delete A_i. Every outside V sees its active matched
W, and every outside Z sees active y. All other vertices retain the
same protections. In both cases y stays active through selected Z.

Now suppose w=0. Then u=1,p=0 and a+v+z=4. The exhaustive count cases
and safe deletions are:

| z | (a,v) | Delete |
| --- | --- | --- |
| 1 | (2,1) or (1,2) | The singleton A or V group |
| 2 | (2,0) | Any selected A |
| 2 | (1,1) | The selected V |
| 2 | (0,2) | One selected Z |

In the first row the fully selected opposite A/V group gives two
neighbours to every omitted A/V vertex, including the deletion. Every
W sees selected u and Z; p sees active Z, and outside Z sees active y.
In the second row, remaining A is active through its matched selected Z,
forming outside V; all omitted A see active Z. In the third row the
remaining A has the same protection and forms the deleted V and the
other outside V. In the last row both V stay selected, forming outside
A by two neighbours. Each W retains u and one selected Z. The retained
Z and y remain mutually active, forming the deleted Z and p. Thus this
last deletion of a Z vertex also preserves y's activity. These cases
exhaust b=5 and prove (3).

Let m_v be the whole module contribution and c_v=12-m_v. Combining
(2)--(3) gives

    c_v>=0;
    y_v selected implies c_v>=1;
    y_v selected with an internal selected Z implies c_v>=2. (4)

If c_v=0, y_v is omitted and both blocks omit every Z. The last
observation follows already from (2).

## 2. From a large minimal set to a small forming interface

Take any globally minimal forming set S of D(H). Put

    C=sum_v c_v, P={v:c_v>=1}.

We construct a forming set Q of H of size at most C. Start with P.
For every v in P such that y_v is selected and internally active,
and v has no neighbour in P but has at least one neighbour in H,
choose one neighbour a(v), keeping the original P fixed. Let I be this set of v and
let Q=P union {a(v):v in I}. Each v in I has c_v>=2 by (4). Therefore

    |Q|<=|P|+|I|<=sum_v c_v=C.                             (5)

Repeated choices of the same a(v) only decrease |Q|.

To prove Q forms H, take x outside Q. Then c_x=0, so y_x is omitted
and has no selected internal Z neighbour. Its formation in D(H)
therefore uses only selected interface neighbours.
If it has two such neighbours, both indices belong to P subset Q,
so x is formed. Otherwise it has an active selected interface neighbour
y_v. If y_v has a selected interface neighbour, both indices are in P
and v remains active in Q. If y_v is active through an internal selected
Z, either v already has a neighbour in P, or v belongs to I and has
the added neighbour a(v). Here v cannot be isolated in H because it
is adjacent to x. Thus v is active in Q in all cases, and it forms x.
This proves Q forms H.

Hence sf_2(H)<=C. Since |S|=12n-C, we obtain the upper bound in (1).
The losses are charged once per module; each additional interface
selection is paid by a distinct extra unit at its index in I.

## 3. An attaining minimal set from a minimum interface

Choose a minimum forming set Q of H. It is inclusion-minimal, since
a proper forming subset would contradict minimum size.
In each module indexed by Q, select y and A union W union {p} in both
blocks. This contributes 11 selections. In every other module select
A union V union {p,u} in both blocks, omitting y; this contributes 12.
Call the resulting set S. No Z vertex is selected anywhere.

Every outside block vertex is formed. In a Q module, each outside V
sees both A, each outside Z sees both W and p, and outside u sees both
W. In a non-Q module, outside W_i sees v_i,u and outside Z_i sees a_i,p.
The selected interface vertices are exactly Q. Since no Z is selected,
their activity and the formation of every omitted y agree exactly with
the activity and formation in H under Q. Thus S forms D(H).

All selections are essential. Each non-interface selection in a Q
module is isolated in S, so deleting it fails at the deleted vertex.
In a non-Q module the six-set witnesses apply: deleting a_i leaves
z_i with only inactive p; deleting v_i leaves w_i with only inactive u;
deleting p or u fails at itself. The module's y stays omitted.
Finally, deleting a selected y reproduces a failed interface deletion
of Q: its witness is an interface vertex, and no Z selection can repair
it. This includes a witness at the newly omitted y itself. So S is
minimal and has size11|Q|+12(n-|Q|)=12n-sf_2(H), proving (1).

## 4. The exact path residual and single-ear discrepancy

For s>=0 put

    mu(s)=2 floor(s/4)+min(s mod4,2).

We first prove sf_2(P_s)=mu(s). For a forming selection of p>0 path
vertices, partition the selected vertices into maximal runs. Call runs
of length one isolated and the others active. Every gap has length at
most two; a two-zero gap requires active runs at both ends. A boundary
zero requires an active end run. Let a,t be the numbers of active and
isolated runs, b the number of consecutive groups of active runs in
the run-index sequence, and e the number of active ends of that sequence
(counting both ends when it consists of one active run). There
are a+t-1 internal gaps, a-b active--active adjacencies, and at most
e boundary zeros. Consequently the number z of omitted vertices is

    z<=(a+t-1)+(a-b)+e=2a+t-1-b+e.

If t=0, then b=1,e=2, so z<=2a<=p; equality requires every run to
have size two, and hence p even. If t>0, e<=b (also when a=b=e=0),
so z<=2a+t-1<=p-1. Therefore s<=2p, with strict inequality when p is
odd. This implies p>=mu(s), by considering s modulo four.

For attainment, repeat the four-bit pattern 0110. For remaining length
one append 1, for remaining length two append 11, and for remaining
length three append 110. Each pattern forms the path and uses mu(s)
selections. The empty path has value zero. Thus sf_2(P_s)=mu(s).

Taking H=P_s in (1) gives the exact residual from the preceding note:

    SF_2(R_s)=12s-mu(s),                                  (6)

where, for s>=1, R_s is connected, bipartite, has 21s vertices and maximum degree
at most six. Its earlier upper bound 12s-ceil(s/3) is valid but weaker.
The same single-ear graph J_s in the preceding connected-residual
construction has SF_2(J_s)=12s+2. Hence, for every s>=1,

    SF_2(J_s)-(2+SF_2(R_s))=mu(s).                         (7)

This strengthens that unbounded-error result to an exact all-s formula.
The roots of J_s still have growing degrees. The local stability theorem
separately excludes unbounded error at fixed maximum degree and ear count.

## 5. Verification scope

The stronger local cap has the explicit general deletion proof above.
Finite block enumeration checks its implementation. A standalone checker
also enumerates small interface graphs to compute sf_2(H) literally,
constructs the attaining sets and tests every deletion, checks arbitrary
globally minimal decorations obtained by deterministic reductions,
validates the constructive upper map Q, and tests all binary path strings
at small orders. Its report distinguishes these controls from exhaustive
computation of SF_2 on the exponentially larger decorated graphs.
The checker passes all 1,024 block patterns, including 483 forming
candidates at or above the sharper cap. It checks all 1,100 labelled
interface graphs of orders 0 to 5: every minimal interface set through
order 4, and one literal minimum set per order 5 graph. Together with
three larger paths these give 1,265 lifted minimal sets and 70,717 specified
deletions. Forty-four seeded greedy minimal decorations test the general
upper map independently of the prescribed lower construction. All 32,767
binary strings for paths of orders 0 through 14 test the exact path formula;
the large path certificates have 17, 32, 65 modules (up to 1,365 vertices).
These are the precise sizes tested, not all sizes through 65.

The independent final review returned **ACCEPT**, reconstructed the general
proof and its dependencies, and ran the unchanged original checker with
assertions enabled. Both the generated report and stdout matched the supplied
550-byte report byte-for-byte. It also identified a coverage limitation:
all 1,309 original upper-map calls have I empty, so none exercises the
extra-neighbour augmentation. The general proof covers that branch.

The reviewer separately checked two explicit globally minimal decorations
on K_(1,1) and K_(1,2), with 22 and 32 selections respectively. Each leaf
has loss two and an internally active selected interface; each chooses
the centre, which has loss zero, as its extra neighbour. Thus K_(1,2)
checks two additions choosing the same vertex. All 54 single deletions fail.
The supplementary `scripts/check_decorated_augmentation.py` reproduces these
two cases locally using literal three-vertex stars and calls the original
upper-map routine. Its report is separate from the unchanged original report.
Complete response, original input hashes and exact execution scopes are in
`output/decorated-interface-review.json`.
No Lean execution or external novelty claim is made.
