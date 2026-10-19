# External private evidence in a saturated Heawood block

Subsequent completion: the [block compensation proof](HEAWOOD_BLOCK_COMPENSATION.md)
uses this classification to prove SF_2(L_k)=36k for all k. The open-target
language below records the state at this earlier local milestone.

19 October 2026. Two different outside owners force two units of actual
block loss. One outside owner can instead have zero loss, but then the
block has one of eight explicit directional patterns. Bare-port loss
and outside-owner loss can overlap: they cannot be added as independent
charges. These are local theorems for arbitrary ambient attachments,
not a proof of SF_2(L_k)=36k or an improved grid coloring bound.

## Setting and exact meaning of ownership

Let H be the Fano incidence graph, let P lie on L, and put B=H-PL.
Embed B in a simple graph G so that every non-port vertex has exactly
its B-neighborhood. Only P,L may acquire additional edges. Let S be an
inclusion-minimal 2-star-forming selection in G and C=S intersect V(B).
The established [ambient block cap and bare-port theorem](BARE_HEAWOOD_PORT_COMPENSATION.md)
give |C|<=8 and |C|+t<=8, where t counts ports omitted together with
both their internal neighbors. These statements do not require C to
form B or be minimal in B.

Recall the global star clauses

    A_u={u} union N_G(u),
    B_(u,v)={u} union (N_G(u) minus {v}) union (N_G(v) minus {u}).

A clause is private to x if its intersection with S is exactly {x}.
Formation and minimality are characterized by these clauses in the
[general private-clause theorem](PRIVATE_CLAUSES_AND_BOUNDARY_ACCOUNTING.md).

An **outside owner for B** is an x in S minus V(B) with a private
clause whose closed center is in B, or whose oriented edge is an
original edge of B. Clauses on an added interface edge are excluded
from this definition. Let e be the number of distinct such owners.
This distinction matters when applying the result to the long core:
the present theorem does not account for all possible core evidence.

Every clause witnessing such an owner is based at exactly one port q:
it is A_q, B_(q,z), or B_(z,q), where z is an internal neighbor of q.
Indeed only a port can have an outside neighbor, and no original B
edge joins the two ports. Each of these clauses contains every external
neighbor of q. Privacy therefore forces x to be the unique selected
external neighbor of q. In particular, different outside owners use
different ports and e<=2. This observation holds for arbitrary numbers
of external neighbors, not just one attachment per port.

The two underlying graph-level statements are proved in
[PortClauseOwnership.lean](../formal/StarForming/PortClauseOwnership.lean).
The [Lean receipt](../output/port-clause-ownership-formal-check.json)
checks both declarations without axioms. The Fano arguments below are
written proofs, not claimed fully formalized.

We use the following sufficient deletion criterion throughout. A selected
vertex is robust if it is active, every selected neighbor has at least
two selected neighbors, and every omitted neighbor has either at least
three selected neighbors or two with the other selected neighbor active.
A robust non-port in B can be deleted in every permitted ambient graph:
all its neighbors retain internal star certificates, and any external
star using it as a leaf can replace that leaf at its selected port
center. Thus C has no robust non-port. Robustness persists on enlarging
a selection. The preservation proof is in the linked block-cap note.

## Two outside owners cost two vertices

**Theorem 1.** If e=2, then |C|<=6. The conclusion holds even when
neither port is bare.

**Proof.** For each port q its owner's clause has empty intersection
with C. Its B-support is either the closed neighborhood A_q(B), of
size three, or one of the four oriented supports at q, of size four.
The distance between P and L in B is five: a shorter alternate path
would give a cycle of length below six in H, while a six-cycle through
PL gives a path of length five. Each support is contained in its port's
radius-two ball. The two supports are therefore disjoint.

If both supports are oriented, at least eight of B's fourteen vertices
are omitted, giving |C|<=6 directly. If both are closed, both ports
are bare and the earlier additive bare-port theorem gives |C|<=6.

Suppose exactly one is closed. By duality take the closed port to be
the point P, and write L={P,R,T}, with the oriented support at L using
its internal neighbor R. The omitted supports have sizes three and
four, so |C|<=7. If equality holds, C is their full complement.

For B_(L,R) this complement consists of the four points outside L,
the point R, and the two lines avoiding P and R. For B_(R,L) it
consists of those four outside points, the line L, and the same two
lines. The two selected non-port lines meet at T and partition the
four outside points into two pairs. Each outside point is therefore
active. Its selected line neighbor has two selected points. Its other
incident lines are the line through P and the line through R: the
former has two active selected outside points, and the latter has
either two active selected outside points or three selected points,
depending on whether R is omitted or selected. Every outside point
is robust, a contradiction. Thus equality seven is impossible. QED.

## The complete zero-loss directional pattern

**Theorem 2.** Suppose |C|=8 and e>=1. Then e=1. One port q is omitted
and has just one selected internal neighbor T, which is isolated in C.
The opposite port p is selected and has two selected internal neighbors.
Precisely eight local selections are possible, described below. Every
one has two selected isolates, both non-ports and hence globally isolated.

For the orientation q=L, write L={P,R,T}. Choose T among the two
internal neighbors of L, and choose one of the two lines M through R
other than L. Write M={R,a,b}. Then

    selected points = {P,T,a,b},
    selected lines = the four lines not through T.

The selected isolates are T and the other line M' through R different
from L,M. There are four choices in this orientation; duality gives
four more with q=P. The outside owner's private internal-edge clause
is B_(L,T) in this orientation. Its external owner must be the unique
selected external neighbor of L. These patterns describe the necessary
local restriction; particular ambient attachments can impose further
conditions. A genuine minimal ambient realization is given below.

**Proof: reduction to two alternatives.** A closed private clause
would make its port bare, contrary to the eight-vertex cap with a bare
port. For an oriented clause B_(q,z), empty internal intersection
forces q omitted, all its internal neighbors other than z omitted,
and all neighbors of z other than q omitted. If z is omitted too,
q is bare, again impossible. Hence z is selected and isolated in C,
and q has just this selected internal neighbor.

For B_(z,q), z and all its neighbors other than q are omitted,
as are all internal neighbors of q other than z. If q is omitted,
q is bare. Otherwise q is selected and internally isolated, and z's
only selected internal neighbor is q. We first exclude this second
alternative at size eight.

**A selected isolated port is impossible.** By duality let q=P and
z=A be a line through P other than L. Write B' for the remaining line
through P. P is selected; A,B' and the other two points of A are
omitted. If p is the number of selected points and ell the number of
selected lines, then p+ell=8, p in {3,4,5}. The available lines are
L and the four lines not through P. We exhibit a robust non-port.

If p=3, all five available lines are selected. The two selected
non-P points belong to B' or L. If both belong to the same one, all
four non-P lines are active and robust. In particular an inactive L
cannot obstruct their deletion: its other points have three selected
line neighbors. If one selected point lies on B' and one on L, three
non-P lines are active and one is inactive. That inactive line can
obstruct candidates only at its intersections with A and B', at most
two candidates; its intersection with L has three selected neighbors.
One of the three active candidates is robust.

If p=4, the three selected non-P points are three of the four points
outside A. Every non-P line meets them. If L is omitted, all four
non-P lines are selected and robust. If L is selected, exactly one
non-P line M is omitted. Among the other three non-P line candidates,
only the intersections M intersect A and M intersect B' can obstruct
robustness, excluding at most two candidates. The first intersection
can have selected degree one as an omitted point; the second can have
selected degree one as a selected or omitted point. Every other
omitted point retains another active selected line, including L when
needed. A robust non-port line remains.

If p=5, all four points outside A are selected, and ell=3. View the
four non-P lines as the edges of K_(2,2) between the two B'-points
and the two L-points. L, if selected, adds the edge between the latter
two points. Every selected line has two selected internal points.
If L is omitted, three K_(2,2) edges form a four-vertex path. Its two
middle points are robust: they each have two selected lines; a missing
K_(2,2) edge has an active other point, B' has three selected points,
and L has two active selected points in B.

If L is selected, there are two selected K_(2,2) edges. If they form
a matching, both L-points are robust. If they meet at a B'-point, that
point is robust, since its omitted B' has three selected points. If
they meet at an L-point, that point has all three incident lines
selected and is robust. All these points are non-ports. The selected
isolated-port alternative is excluded in every case.

**Classification at an omitted port.** By duality now let q=L, with
sole selected internal neighbor T, isolated in C, and L={P,R,T}.
All three lines through T and the point R are omitted. Thus p is
4,5 or6, with ell=8-p chosen among the four lines avoiding T.

If p=4, all four lines avoiding T are selected. If P is omitted,
the other three selected points are outside L. Every selected line
is active and robust: selected points on it have two selected lines,
and omitted points retain another active selected line. If P is
selected, write a,b for the other two selected points outside L.
The joining line ab meets L in P,R or T. If that intersection is P,
the selected points P,a,b are collinear and every selected line is
active and robust. If it is T, the line ab is omitted and again every
selected line is active and robust. To check both assertions, each
selected non-isolated point has two selected lines; an omitted point
off L has two active selected lines, while the omitted R has two
selected lines avoiding T, each meeting a or b or P. Consequently a
non-port selected line could be deleted. Only intersection R remains.
Then M=ab is one of the two lines through R other than L; the selected
points are exactly P,T,a,b and the selected lines are exactly the four
avoiding T. The points P,a,b and their three joining lines form the
selected six-cycle. Point T is isolated, as is the fourth selected line
through none of P,a,b. The opposite port P lies on that cycle and has
its two internal cycle neighbors selected. This is precisely the
stated directional template.

If p=5, consider the selection first in H before deleting PL. The
three selected lines cover at least six points, so T is its only
selected isolate. The joining line of the two omitted points is the
only line with exactly one selected point; it can obstruct at most
its third point. Any other failure of a selected point's robustness
needs an omitted line with two selected points, one the isolate T.
Such a line passes through one of the two omitted points, excluding
at most two further candidates. Including T itself, at most four of
the five selected points fail robustness. Some selected point is
robust in H. If P is selected, it already fails robustness at the
omitted L, whose other selected point is T. Thus the robust point is
not P. Deleting PL cannot affect robustness of any other non-port
point: only P and T are selected points incident with L, and T is
already isolated. A robust non-port remains in B, a contradiction.

If p=6, only R is omitted among points; two lines are selected.
In H there are at least two robust selected points. If the chosen
lines meet at R, their four other points are robust. If exactly one
chosen line contains R, its other two points are robust: both are
active and their omitted incident lines avoid R and have three
selected points. If neither chosen line contains R, they cover five
active selected points and leave the isolate T. The three lines
through R pair the other six points; the two pairs avoiding T give
four robust points, since their partner is active and their other
omitted lines avoid R. As in the p=5 case, P is already blocked at L
when selected, and deleting PL preserves the remaining robust
non-port points. This is again impossible.

Only the p=4 construction survives. Its two isolates and the selected
degree two at P follow directly from Fano incidence. Theorem 1 gives
e=1. This completes the classification. QED.

## Joint accounting without duplicate charges

Put delta=8-|C| and define s=1 if delta=0 and e=1, and s=0 otherwise.
The preceding results imply

    e <= delta+s,
    delta >= max(t,e-s).

Indeed e<=2 always. If delta=0, Theorem 1 permits at most one owner
and Theorem 2 specifies its signal. If delta=1, Theorem 1 again
permits at most one owner. If delta>=2, e<=2<=delta. Combine this
with delta>=t from the bare-port theorem. This is a general proof,
not an inference from tested local maxima.

For several blocks, assign each outside selected owner whose evidence
is being counted to one block and one private clause. Sum each block's
delta once. Its assigned owners are a subset of the owners counted by
e, so their total is at most sum(delta+s). Each unpaid unit is an
explicit saturated directional signal at the opposite selected port.
This controls evidence rooted on original block edges; added-interface
clauses and other core private evidence still require separate treatment.

One cannot replace max(t,e-s) by t+e-s. Bare-port and ownership
certificates can use the very same lost vertex, as the third example
below proves. Equally, e<=delta without a signal term is false, by
the first example. Tracking these two failures prevents both an
unjustified positive charge and an unjustified reuse of a real loss.

## Three explicit minimal ambient examples

Label points0,...,6 and lines7+j, with line7+j incident to j,j-1,j-3
modulo7. Delete0--8. Add outside vertices14,15 and only the edges
listed in the table. All examples are simple bipartite graphs on16
vertices. The selected sets form the whole ambient graph, and the
following literal deletion certificates prove inclusion-minimality.

| Example | Added edges | Selected S | t | e | delta |
|---|---|---|---:|---:|---:|
| Free directional import | 0--14,8--15 | 0,3,4,5,7,9,10,11,15 | 0 | 1 | 0 |
| Two non-bare imports | 0--14,8--15 | 0,2,3,5,9,11,14,15 | 0 | 2 | 2 |
| Overlapping bare/import loss | 0--14,14--15 | 1,2,4,9,11,12,13,14,15 | 1 | 1 | 1 |

In the first example15 owns B_(8,5). Its block restriction is the
template with isolated selected point5 and selected signal port0.
The omitted vertex14 makes0 essential. This is actual zero-loss
external evidence in a minimal set, not just a locally admissible state.

In the second example14 owns B_(7,0) and15 owns B_(8,5). Neither
port is bare; Theorem 1 is sharp at six selected block vertices.

In the third example14 owns A_0. The bare port0 and this import
share the same single block loss. The claimed additive charge
delta>=t+e would require1>=2 and is false. This refutes that rule,
not the target long-core bound. No unsupported-core claim is made
about vertex15.

For each row below, deletion of a selected vertex in the first list
leaves the corresponding vertex in the second list without a star:

| Example | Deleted selected vertices, in order | Failing vertices, in order |
|---|---|---|
| Free import | 0,3,4,5,7,9,10,11,15 | 14,13,12,5,6,9,2,1,8 |
| Two imports | 0,2,3,5,9,11,14,15 | 0,2,3,5,6,4,7,8 |
| Overlap | 1,2,4,9,11,12,13,14,15 | 8,10,7,6,3,5,13,0,0 |

The [independent control output](../output/saturated-heawood-transfer-controls.json)
records all clauses and26 literal star-deletion checks. The checker
also tests all16384 block subsets with four parent-selection patterns,
all25 pairs of empty port clauses and the16 relevant seven-selection
robustness tests. It finds940 two-owner states with block size at
most six, and16 saturated directional states, namely the eight
templates with two statuses of the other parent. Such local states
are necessary conditions, not asserted ambient realizations.

## Consequences and remaining target

For the long-core graph L_k, write C_0 for its core restriction and
delta_j=8-|C_j| for its3k Heawood blocks. The exact identity remains

    |S|=24k+|C_0|-sum_j delta_j.

The open all-k target is |C_0|-12k<=sum_j delta_j. The
[previous bare-only obstruction](EXPORTED_BOUNDARY_AND_BARE_ONLY_OBSTRUCTION.md)
shows why t_j alone cannot replace delta_j. The present result adds
precise evidence on non-bare and saturated states: two outside owners
cost two, whereas a zero-cost owner forces an omitted port with an
isolated selected neighbor and an opposite selected port of degree two.
A global proof must control propagation or termination of these
directional signals together with the remaining core evidence. No
assumption that every signal is automatically paid elsewhere is used.

The established bounds are still

    beta_2(L_k)=33k+floor(k/2),
    36k<=SF_2(L_k)<=36k+floor(2floor(k/2)/7).

In particular SF_2(L_k)=36k for k<=7; the unrestricted larger-k equality
and the separate rectangular-grid bridge remain open.

Reproduction:

    python3 scripts/check_saturated_heawood_transfer.py --output output/saturated-heawood-transfer-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit port-ownership --lean /path/to/lean-4.33.0 --output output/port-clause-ownership-formal-check.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
