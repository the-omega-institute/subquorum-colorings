Independently referee the all-r exact SF theorem below, especially the degree-three perturbation budget and every Fano selection case. Look for counterexamples and hidden dependencies. Do not accept finite enumeration or Lean as proof. The earlier cubic note established an eight-set per block with all ports outside it, and rewiring invariance: if graphs differ only outside S, every induced T union {x} for T subset S is unchanged, so minimal star formation of S is invariant. In the fixed cyclic labeling the eight-set is {1,2,3,5,7,9,10,11}, ports0,8; earlier review accepted the lower bound and exact cyclic beta=7r+floor(r/2). Now check the new upper bound, arbitrary-outside hypothesis and arbitrary port graph composition in full. Report any gap and concrete repair.

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

**Theorem 3.** Let G contain the fourteen labeled vertices of B. Keep
every edge of B, and allow additional edges incident with this block
only at P or L. In particular, PL may be restored, and arbitrary external
vertices and edges at the ports are allowed. If S is inclusion-minimal
2-star-forming in G, then

    |S intersect V(B)|<=8.

In this hypothesis every non-port of the block has exactly its B-neighbors
in G; the only possible extra internal edge is PL.

Suppose C=S intersect V(B) has at least nine vertices, and choose the
robust non-port v from Lemma 2. Put S'=S minus {v}. The vertex v has
no external neighbors. Its selected core neighbor u retains another
selected core neighbor by condition 2, giving a star covering v.

For an old omitted vertex x adjacent to v, x lies in the block and
condition 3 supplies a star after deletion. If it had three selected
core neighbors, two remain. Otherwise its other selected core neighbor
retains activity by condition 2. Additional port edges only help.

For an old omitted x not adjacent to v, a former star not using v
survives. In a star using v, v must be a leaf with selected center u.
The center lies in the block, and condition 2 supplies another selected
core leaf to replace v. That replacement is different from x, which
was not selected. Thus S' remains star-forming, contradicting minimality.
This proves the theorem independently of the outside graph.

The same argument gives SF_2(G)<=8q+p for q disjoint such blocks and
p remaining vertices, with the attachment condition at every block.
No vertex or local contribution is counted twice.

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

## Verification status

The proof above derives the local existence lemma from Fano incidence and
a general degree-three perturbation budget. Finite checks, new Lean scope,
and independent review will be recorded separately; none is assumed as a
premise of this written proof. The submitted manuscript and correspondence
are unchanged.
