# Exact star formation under arbitrary Heawood-port interfaces

19 October 2026. The cubic family from
[the Fano construction](CUBIC_STAR_FORMING_GAPS.md) has the exact value

    SF_2(F_r)=8r,       r>=1.

More generally, take r disjoint Heawood graphs, distinguish one incidence
P_i--L_i in each, delete these r incidences, and add any simple graph on
the 2r distinguished ports. The upper 2-star-forming number is always 8r.
The interface may connect like bipartition classes, restore deleted
incidences, or be disconnected. Only the cyclic point-to-line interface
is asserted cubic and bipartite.

The upper bound follows from a stronger local theorem: in every surrounding
graph whose attachments to a broken-incidence block are confined to its
two ports, a minimal star-forming selection uses at most eight block vertices.
Restoring the deleted incidence is also allowed. The proof is geometric
and counts safe deletions; finite controls do not replace it.

Stars are non-induced copies of K_{1,2}. Thus a set S is 2-star-forming
when every vertex outside S has two selected neighbors, or a selected
neighbor having another selected neighbor. Minimality is inclusion-minimality,
and SF_2 maximizes the size of a minimal set. This convention also applies
when arbitrary port edges create triangles.

## Robust deletion and its obstruction set

Let K be a finite simple graph and C a set of its vertices. Write
d_C(v)=|N_K(v) intersect C|, and call a selected vertex active when its
selected degree is positive. A vertex v is a robust deletion for C if:

1. v belongs to C and is active;
2. every selected neighbor u of v has d_C(u)>=2;
3. every omitted neighbor x of v has d_C(x)>=3, or has d_C(x)=2 with
   its selected neighbor other than v active.

Condition 2 ensures that a selected neighbor retains activity after v is
deleted. Together these conditions provide a star for the newly omitted v,
preserve stars at omitted neighbors of v, and provide replacement leaves
for any old star using v as a leaf. The definition does not require C
itself to be star-forming.

**Preservation lemma.** If C is star-forming and v is robust, then
C minus {v} remains star-forming. Every retained selected vertex which
was active stays active: a nonneighbor of v loses nothing, and a neighbor
of v retains another selected neighbor by condition 2. Conditions 1 and 2
cover the newly omitted v. For an old omitted neighbor of v, condition 3
leaves two selected neighbors or one which stays active. For an omitted
nonneighbor, its selected neighbors and their previous activity persist.
These are all omitted vertices after deletion.

For hand checking, the vertices which are not robust are exactly the
following selected vertices:

- selected isolates;
- the unique selected neighbor of any vertex of selected degree one,
  whether that vertex is selected or omitted;
- for an omitted x of selected degree two, a selected neighbor v whose
  other selected neighbor at x is isolated in K[C].

Indeed these are precisely the failures of conditions 1, 2 and 3.
An omitted vertex of selected degree zero has no selected neighbor to
delete, and degree at least three cannot cause a failure of condition 3.

**Upward closure.** If v is robust for C and C subset C', then v is robust
for C'. Old selected neighbors retain a replacement. A newly selected
neighbor u of v was omitted before and had at least two selected neighbors,
by condition 3, so it too retains a neighbor other than v. An omitted x
still omitted keeps either three selected neighbors or its active other
neighbor. Thus all three conditions persist.

## A degree-three edge-deletion budget

**Lemma 1.** Let K have maximum degree at most three, let e=ab be an edge,
and put K'=K-e. For a fixed selection C, at most four robust deletions in
K either belong to {a,b} or cease to be robust in K'. If exactly one
endpoint is selected, this number is at most two; if neither is selected,
it is zero.

When both endpoints are omitted, deleting their edge changes no selected
degree or edge incident to a selected vertex, so there is no change.

Suppose a is selected and b omitted. No selected vertex changes selected
degree. Apart from excluding a, only condition 3 at b can fail for a
non-port candidate. If d_C(b)=2, at most its one remaining selected neighbor
is affected. If d_C(b)=3, it has two selected neighbors after removing e.
A candidate v must be active; it can fail only if the other remaining
neighbor is isolated. At most one of those two can be an active candidate
with an isolated other neighbor. If d_C(b)=1, there is no remaining
selected neighbor to affect. Thus there is at most one additional loss.

Now suppose both endpoints are selected. Let d_a,d_b be their selected
degrees before deletion; each lies in {1,2,3}. A non-port candidate keeps
its own selected neighbors, and no omitted vertex changes selected degree.
The only new failures are:

- if an endpoint u has d_u=2, its one selected neighbor other than the
  opposite endpoint can fail condition 2;
- if d_u=1, u becomes isolated. Each of its at most two omitted neighbors
  can then disqualify at most one candidate by condition 3.

Charge at most f(d_u) candidates to endpoint u, where

    f(1)=2, f(2)=1, f(3)=0.

Also, the opposite endpoint can have been robust only if d_u>=2:
otherwise it had the selected degree-one neighbor u and failed condition 2.
Charge that possible port exclusion to u as well. For each endpoint,

    f(d_u)+1_(d_u>=2)<=2.

Summing the two charges gives at most four losses. Overlap only reduces
the count. This proves the lemma without assuming C dominates K.

Both nonzero budgets are sharp. In the four-cycle a--b--c--d--a, delete
ab. If C consists of all four vertices, all four are initially robust;
c,d cease to be robust after deletion and a,b are excluded as ports,
giving four losses. If C={a,c,d}, exactly a,c are initially robust;
deletion makes c fail at the omitted b, and a is excluded, giving two.

## Robust deletions in every dense Fano selection

Let H be the Heawood incidence graph of the Fano plane. Fix any incidence
e=P--L, and let B=H-e. We prove:

**Lemma 2.** Every C subset V(B) with |C|>=9 has a robust deletion in B
which is neither port P nor port L.

By upward closure it suffices to treat |C|=9. By point-line duality we
may assume C has p selected points and q selected lines with p<=q. The
incidence axioms and the distinguished flag dualize together, so the
lemma is unchanged by this interchange. Necessarily (p,q) is (2,7), (3,6)
or (4,5).

### Two selected points and seven selected lines

Exactly five lines meet the two selected points: their joining line and
two other lines through each point. All five are robust in H. They have
a selected point neighbor, every selected point has selected degree three,
and every omitted point has three selected line neighbors. Lemma 1 loses
at most four of these candidates when the flag is deleted and ports are
excluded. At least one remains.

### Four selected points and five selected lines

Let U be the three omitted points, and let M,N be the two omitted lines.
The point O=M intersect N is the only point of selected degree one;
every other point has selected degree two or three. Its unique selected
line neighbor is the third line through O, denoted R.

If U is noncollinear, write U={a,b,c}. The four selected points are
x=a+b, y=a+c, z=b+c and n=a+b+c. The three side lines ab,ac,bc each
have selected degree one, with selected neighbors x,y,z respectively.
The other four lines have selected degree two or three. All selected
vertices are active. The obstruction description therefore excludes
exactly x,y,z,R from the nine selected vertices. The other five are robust.

If U is collinear on a line T, every line other than T has selected
degree two, and T has selected degree zero. Every selected point is active.
There is at most one selected isolate, namely T, and the only possible
degree-one obstruction is R. Further obstructions can only come from
omitted points on T having selected degree two: their other selected
neighbor may be the isolated selected T. Such a point lies on exactly
one of M,N. There are at most two of them, since M and N each intersect
T once unless equal to T; if one equals T, then T is not a selected
isolate and gives no such obstruction. Each point excludes at most one
additional selected line. In total at most 1+1+2=4 selected vertices
are excluded. Thus at least five robust deletions exist in this case too.

Lemma 1 leaves at least one of these five candidates robust in B and
different from both ports.

### Three selected points and six selected lines

Let M be the sole omitted line and t the number of selected points on M.
Every selected point has selected degree at least two. Thus a selected
line is robust in H if it is active and each omitted point on that line
which lies on M retains another active selected line. Omitted points
outside M have selected degree three and cause no obstruction.

There are at least four robust line candidates, as follows.

- t=0: the three selected points lie outside M, with only one other
  point outside M omitted. Each of the two non-M lines through any
  point of M therefore contains a selected point. All six selected
  lines are robust.
- t=1: the two non-M lines through the selected point of M are robust.
  Write b,c for the selected points outside M. At least one of the
  two omitted points of M is different from the intersection bc intersect M.
  Its two non-M lines contain b,c separately and are both robust. They
  differ from the first two lines, giving four candidates.
- t=2: the four non-M lines through the two selected points of M are
  distinct, active and robust.
- t=3: every selected line contains a selected point on M, and every
  omitted point is outside M. All six selected lines are robust.

For these line candidates the flag deletion excludes at most two, a
stronger bound than Lemma 1. One exclusion is the port L itself, if selected.
We show that at most one other line candidate can lose robustness.

If P is omitted and L selected, only condition 3 at P can change. The
one-endpoint-selected argument from Lemma 1 gives at most one affected
non-port candidate. If L is omitted, its removal changes no condition
at a non-port line candidate: selected point degrees do not change, and
an omitted line is not adjacent to another line.

It remains that P and L are selected. A line candidate's condition 2
can fail only at P, and only if P lies on M, so d_C(P)=2. At most the
one selected line through P other than L is affected. In this case
L intersects M at the selected point P, so no omitted point on L has
selected degree two; loss of activity at L cannot affect another
candidate's condition 3.

If P does not lie on M, its selected degree is three and condition 2
does not fail. Only L can lose activity, and only if its sole selected
point is P. It can then spoil condition 3 only at its one intersection
with M, since other omitted points have selected degree three. At that
point, at most the other selected line candidate is excluded. Thus in
all cases there is at most one non-port loss, in addition to L.

At least four candidates minus two exclusions leaves a robust non-port
line. This completes all three cases and proves Lemma 2.

## The upper bound in an arbitrary surrounding graph

**Theorem 3.** Let G contain the fourteen labeled vertices of B, keep
every edge of B, and require N_G(w)=N_B(w) for every block vertex w other
than P,L. In particular, PL may be restored, and arbitrary external
vertices and edges at the ports are allowed. If S is inclusion-minimal
2-star-forming in G, then

    |S intersect V(B)|<=8.

In this hypothesis every non-port of the block has exactly its B-neighbors
in G; the only possible extra internal edge is PL.

Suppose C=S intersect V(B) has at least nine vertices and choose a robust
non-port v in (B,C) from Lemma 2. This v is also robust in (G,S). Its
neighborhood is unchanged, so it remains active and every selected
neighbor has at least the two selected core neighbors required by
condition 2. Every omitted neighbor x of v lies in the block. It has
three selected core neighbors, or has two with the other one active in
the core. Additional port edges either leave these two selected neighbors
and their activity intact or increase the count to at least three.
Thus condition 3 transfers too. The preservation lemma deletes v from
the global star-forming S, contradicting minimality. No star-forming
property of C inside B is assumed.

The same argument gives SF_2(G)<=8q+p for q disjoint such blocks and
p remaining vertices, with the attachment condition at every block.
No vertex or local contribution is counted twice.

The unchanged non-port neighborhoods are essential. If a separate pendant
x_w is attached to every block vertex w, the set of all fourteen block
vertices is minimal star-forming: each pendant sees an active selected
neighbor, but deleting w leaves x_w with no selected neighbor. This
violates the attachment hypothesis and permits fourteen selected core
vertices, so the theorem cannot be extended to arbitrary non-port attachments.

## Exact composition and the cyclic family

**Corollary 4.** Take r disjoint copies of B and add any simple graph
on their 2r ports. Then SF_2=8r.

Theorem 3 gives at most eight selected vertices per block in every
minimal set, hence the upper bound 8r. For the lower bound choose the
eight-set S in each original Heawood graph so that the distinguished
incidence has both endpoints outside S. Such a choice exists for every
flag by Fano symmetry; equivalently use the fixed labeling of the earlier
note in every copy. The union of these sets is minimal in the disjoint
union of the Heawood graphs. Every deleted or added edge has both endpoints
outside this union. The already proved rewiring lemma preserves its
minimality, giving an attaining set of size 8r. This includes r=1 with
PL present or absent.

For the symmetry assertion, represent a flag by a nonzero vector P and
a two-dimensional subspace L containing it. Extend P and a second vector
of L to a basis. The linear map between any two such bases preserves
incidence and sends the first flag to the second.

For the cyclic interface, combine this identity with the earlier exact
dissociation calculation and structural proofs to obtain, for every r>=1,

    |V(F_r)|=14r,   girth(F_r)=6,
    Gamma(F_r)=alpha(F_r)=7r,
    beta_2(F_r)=7r+floor(r/2),   SF_2(F_r)=8r,
    SF_2(F_r)-beta_2(F_r)=ceil(r/2).

These graphs are two-connected, cubic and bipartite. The gap coefficient
is exactly 1/28 for even r, with the displayed rounding for odd r.
This is an exact construction, not a universal extremal or priority claim.

## The interaction graph gives the exact dissociation number

The arbitrary-interface statement also has an exact beta formula. Let Q
have one vertex for each block. Join two distinct block indices when at
least one port edge connects them, and put a loop at an index when its
deleted incidence is restored. Multiple port interfaces give only one
adjacency in Q. Let alpha_0(Q) be the maximum size of a set containing
no looped vertex and no adjacent pair. Then

    beta_2(G)=7r+alpha_0(Q),
    SF_2(G)-beta_2(G)=r-alpha_0(Q).

For a loopless Q, alpha_0 is its usual independence number, and the gap
is exactly its minimum vertex-cover number tau(Q). If loops are present,
the same interpretation holds with a cover required to contain every
looped vertex.

To prove the upper bound, restrict any dissociation set D to each block.
The earlier saturated-port lemma gives at most eight vertices per block;
every eight-block selects both ports, each already of internal selected
degree one. Two eight-blocks cannot have an interface between them, and
an eight-block cannot have its deleted incidence restored. Thus its set I
of eight-blocks is independent in Q and contains no looped vertex. Counting
every other block at most seven gives

    |D|<=7r+|I|<=7r+alpha_0(Q).

Conversely, take an attaining independent set I in Q. In each indexed
block choose the previously displayed D_8, which selects both ports and
induces four independent edges. In every other block choose D_7, which
omits both ports. No interface has two selected endpoints. The union is
dissociation of size 7r+|I|, proving equality. Each block contributes once;
there is no allocation of one neighboring block to multiple dense blocks.

In particular, SF_2=beta_2 in this composition class if and only if Q
has no edge and no loop. Any nonempty port interface creates a strict gap.
The cyclic family's interaction graph is a cycle for r>=3, one edge for
r=2, and one loop for r=1, recovering the earlier formula in every case.

For clarity, in the cyclic Fano labeling write p_a for point a and ell_a
for line a, where p_a is incident with ell_a,ell_(a+1),ell_(a+3), and delete
p_0--ell_1. The matchings M_0={p_a--ell_a} and M_3={p_a--ell_(a+3)} both
survive. Their union is a spanning cycle: following M_3 then M_0 moves
point a to a+3 modulo seven, visiting every point and line. Thus B has
a perfect matching and B minus any vertex is connected. Flag transitivity
transports this certificate to any distinguished incidence.

**Corollary 5 (a two-connected realization of every connected loopless interaction graph).**
For any connected loopless simple Q of order r>=1, take r copies of B
and, for each edge ij of Q, add both L_i--P_j and L_j--P_i. The resulting
graph G_Q is two-connected and bipartite, with

    |V(G_Q)|=14r,
    Gamma(G_Q)=alpha(G_Q)=7r,
    beta_2(G_Q)=7r+alpha(Q),
    SF_2(G_Q)=8r,
    SF_2(G_Q)-beta_2(G_Q)=tau(Q).

Its maximum degree is max(3,2+Delta(Q)). The assertions for r=1 concern
the single broken-incidence graph, so the maximum degree is three there.
All added edges are point-to-line. The unchanged shift-zero matching
gives alpha(G_Q)=7r, and the existing bipartite identity gives Gamma=alpha.
Each block has a spanning cycle. After any vertex deletion every affected
block stays connected, and every edge of Q retains at least one of its
two interfaces: the paired interfaces have distinct endpoints in either
block. Contracting the remaining connected blocks therefore still gives
a connected graph. This proves two-connectivity, including r=1 by the
block's spanning cycle. The parameter identities follow from Theorem 3
and the interaction formula.

This realizes a classical vertex-cover parameter as the exact star-forming
gap in two-connected bipartite graphs. It is an algebraic construction;
no new complexity-priority claim is made. It does not prove hardness of
SF_2 on this class, where SF_2 is explicitly 8r.

### A branching obstruction to reusing the cyclic injection

Take Q=K_(1,t), with one center and t>=2 leaves, and use the reciprocal
realization. Then r=t+1, alpha(Q)=t and tau(Q)=1, so

    beta_2(G_Q)=8r-1,   SF_2(G_Q)=8r,   gap=1.

An attaining dissociation set takes D_7 in the center block and D_8 in
every leaf block. All t dense leaf blocks share the same nondense neighbor.
Thus the rule "each dense block has a nondense neighbor, hence at most
half of the blocks are dense" is false for branching interfaces. It
silently reuses the center block t times. In the earlier cyclic proof the
successor map was injective; there is no analogous injection here.

Already t=2 gives a two-connected bipartite42-vertex graph of maximum
degree four with Gamma=alpha=21, beta_2=23, SF_2=24 and gap1. Label the
center block0 and leaves1,2. Its four interfaces are

    8--14, 22--0, 8--28, 36--0,

where each block uses the earlier0,...,13labels shifted by14times its
index. Use D_7 in block0 and D_8 in blocks1,2 for the explicit23-set.
The standard eight-set in every block attains24. The general local cap
and saturation proofs supply the matching bounds.

This is a counterexample to extending the cyclic charging rule to
arbitrary port interfaces, not to the exact interaction formula or the
cubic cyclic theorem. It identifies exactly where a shared compensating
block would be counted repeatedly. In general the correct gap is tau(Q),
which can stay one while the number of blocks grows.

These interfaces also mark two structural limits of the construction.
Every graph contains B as a subgraph. B is already nonplanar: it is
two-connected with14vertices,20edges and girth six, while a planar graph
of girth six satisfies m<=3(n-2)/2=18. For r>=2 the two ports of any block
separate its twelve non-port vertices from all other blocks. Thus a
three-connected amplification needs more than two attachment vertices;
changing only the graph on the existing ports cannot supply it.

## Verification status

The proof above derives the local existence lemma from Fano incidence and
a general degree-three perturbation budget. Its
[independent controls](../output/exact-cubic-controls.json), produced by
[the checker](../scripts/check_exact_cubic.py), pass the following tests:

- all2,002nine-element selections in H and all21deleted incidences,
  totaling42,042flag perturbations; all3,473dense selections in fixed B;
- the direct robust predicate against its obstruction-set description,
  and70,796upward-closure candidate checks;
- all842labeled subcubic graphs of orders2through5 and112,292edge/selection
  perturbations, checking the0,2,4loss budgets;
-32arbitrary surrounding graphs,18,144core/outside selections and50,661safe
  deletions checked using literal non-induced stars;
-114arbitrary port graphs: all graphs on two or four ports, and24sampled
  graphs each on six and eight ports. Independent optimization over all
  feasible block port states agrees with7r+alpha_0(Q), including loops;
-16larger arbitrary-interface minimal8r-sets and16reciprocal connected
  realizations, checking vertex deletion, bipartiteness and matching;
- the sharp four-cycle budgets, forbidden non-port pendant example, and
  explicit42-vertex branching obstruction with its23- and24-set witnesses.

The general proof is not inferred from this finite coverage.

Independent Oracle review accepted the degree-three budget, every Fano
case, the arbitrary-outside upper bound and arbitrary-interface exact SF.
Its [receipt](../output/exact-cubic-oracle-review.json) and
[complete response](reviews/2026-10-19-exact-cubic-oracle-response.txt) preserve
the actual model and scope. Its three requested exposition revisions are
incorporated. The eight-set and earlier cyclic beta formula were supplied
premises. A separate follow-up accepted the interaction-graph beta formula,
loop-aware vertex-cover identity and reciprocal two-connected realization
without a substantive gap. Its requested heading clarification and explicit
spanning-cycle/matching certificate are incorporated. Its
[receipt](../output/interaction-oracle-review.json) and
[complete response](reviews/2026-10-19-interaction-oracle-response.txt) preserve
that distinct scope. The response also explains the star-interaction example;
the explicit42-vertex labeling is a subsequent specialization checked below.

Eight new local Lean4.33.0 audits pass. The
[certificate source](../formal/StarForming/CubicDense.lean) proves Boolean
reflection for actual star witnesses and supported deletions, then checks
all16,384selection masks in64separate kernel-checked chunks. The
[ambient theorem](../formal/StarForming/CubicExact.lean) lifts that certificate
through an embedding into any surrounding graph with the stated non-port
neighborhoods, proving the eight-vertex cap with unrestricted port edges.
It also checks disjoint-block accounting and the exact cyclic gap arithmetic.
The [receipt](../output/exact-cubic-formal-check.json) records166.643seconds
and peak child RSS3.34GB, with only standard logical axioms and no sorry or
compiler-trust certificate. Memory and actual lean/lake executable basenames
were measured before each run; compilation was sequential.

The analytic perturbation/Fano proof is independent of this finite certificate.
The concrete multi-block embedding, global attaining-set instantiation, the
full graph-level SF identity, and the interaction-graph beta formula have
written proofs; they are not claimed fully newly formalized. Generic rewiring
invariance and the local eight-set were formalized in the earlier cubic source.
The submitted manuscript and correspondence are unchanged.

Reproduction:

    python3 scripts/check_exact_cubic.py --output output/exact-cubic-controls.json
    python3 scripts/check_subcubic_formal.py --cubic-exact --lean /path/to/lean-4.33.0 --output output/exact-cubic-formal-check.json
