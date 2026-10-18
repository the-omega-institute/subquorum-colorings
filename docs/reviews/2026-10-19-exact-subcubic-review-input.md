Independently referee the following mathematical proof. Your task is to decide whether the local cap for every arbitrary outside graph follows rigorously, with particular attention to the robust deletion criterion, upward closure, completeness and correctness of every case table, and replacement of a deleted leaf in external stars. Do not trust finite enumeration or reported Lean checks. Identify an actual gap or counterexample if one exists; otherwise explain why each logical step works and give any necessary clarifications. The previously proved cyclic construction has r disjoint copies of K plus r shared ports, external edges only at3,11, and an inclusion-minimal set consisting of {1,4,5,7,8,9} in each core and all shared ports; assume its attainment for this review. Review the new upper-bound deduction under these assumptions. This is one proof review, not a novelty/literature check.

# Exact star formation in the subcubic cyclic family

19 October 2026. The family from
[the subcubic gap note](SUBCUBIC_STAR_FORMING_GAPS.md) has the exact value
SF_2(J_r)=7r. The upper bound follows from a stronger local theorem:
an inclusion-minimal star-forming set contains at most six vertices of
each ten-vertex core, even in an arbitrary surrounding graph attached
only at the two specified core vertices. This note gives an explicit
deletion argument and a complete small case proof of its local hypothesis.
No conclusion is extrapolated from finite enumerations.

A set S is 2-star-forming if, for every x outside S, the graph induced
by S union {x} contains a non-induced copy of K_{1,2} through x.
Equivalently, x has two distinct neighbors in S, or it has a neighbor
u in S with a neighbor in S. Minimality means inclusion-minimality;
SF_2 is the maximum cardinality of such a minimal set.

## The core and the deletion criterion

Use the original labels from the twelve-vertex block. Its core K has

    V(K)={1,2,3,4,5,7,8,9,10,11},

with the following open neighborhoods inside K:

    N(1)={7,8,9},  N(2)={9,10,11}, N(3)={8,10},
    N(4)={7,10},   N(5)={7,11},    N(7)={1,4,5},
    N(8)={1,3},    N(9)={1,2},     N(10)={2,3,4},
    N(11)={2,5}.

Only A={3,11} may have neighbors outside K. Put B={1,2,7,10} and
D=V(K) minus B={3,4,5,8,9,11}. Degrees in K are three on B and two on D.
For C subset V(K), call v a robust deletion vertex if:

1. v belongs to C minus A and has a neighbor in C;
2. every selected neighbor u of v has another neighbor in C minus {v};
3. every x outside C but adjacent to v has either at least three neighbors
   in C, or exactly two neighbors in C, the other one u having a neighbor
   in C.

All three conditions concern only K. In condition3 the other neighbor
u remains active after deleting v: if its selected neighbor was v,
condition2 supplies a replacement. This distinction is needed; merely
having two selected neighbors at x does not always make deletion safe.

**Lemma 1 (upward closure).** If v satisfies these conditions for C, it
satisfies them for every C' containing C.

The first condition persists. A selected neighbor already in C keeps its
replacement from condition2. A newly selected neighbor u of v was outside
C. Condition3 gives u at least two neighbors in C, so it has a selected
neighbor other than v. This proves condition2 for C'. An outside x still
outside C' keeps its original selected neighbors. Three original selected
neighbors suffice; with exactly two, the selected neighbor different from
v keeps its original selected neighbor. Adding more selected neighbors
only helps. This proves condition3 and the lemma.

## A robust deletion in every seven-set

**Lemma 2.** Every C subset V(K) of size at least seven has a robust
deletion vertex.

By Lemma1 it suffices to prove this for |C|=7. Put W=V(K) minus C,
so |W|=3, and let t=|W intersect B|. There are four cases, t=0,1,2,3.
The following choices use only the displayed neighborhoods.

### No branch vertex omitted: t=0

All of B is selected. If 4 is selected, delete4; if 9 is selected,
delete9. Their neighbors retain the selected chord neighbors on 1--7
and 2--10, so all three conditions hold. If both4and9are omitted,
only one further member of D is omitted. At least one of the pairs
{5,11} and {8,3} is therefore entirely selected. Delete5for the first
pair or8for the second. Both neighbors remain active: 7 retains1,
11 retains2, 1 retains7, and3 retains10, as appropriate.

### Exactly one branch vertex omitted: t=1

There are two omissions in D. The table gives a priority rule; use its
first applicable choice.

| Omitted branch | First choice, if selected | Second choice and condition | Otherwise |
| --- | --- | --- | --- |
| 1 | 9 | 4, if {4,5} subset C | 8 |
| 2 | 9 | 4, if {4,3} subset C | 8 |
| 7 | 4 | 9, if {9,8} subset C | 5 |
| 10 | 4 | 9, if {9,11} subset C | 5 |

Here is the verification of the first two rows; the last two follow from
the automorphism

    (1 7)(2 10)(3 11)(4 9)(5 8),

which preserves A. If1is omitted and9selected, deleting9leaves2active
through10. The only adjacent omitted core vertex is1. It retains the
selected neighbor7and, unless8is omitted, the selected neighbor8.
If8is omitted, at most one of4,5is omitted, so7remains active. This
verifies condition3. If9is omitted, deleting4works when4and5are selected.
If that choice fails, the two omissions in D are {9,4} or {9,5}.
Then8and3are selected, and deleting8leaves3active through10; the outside
vertex1retains7, which is active through5or4, respectively. Thus8works.

If2is the omitted branch, the same argument uses the selected chord
1--7. A selected9can be deleted: outside2retains10and possibly11;
when11is omitted at least one of3,4is selected and activates10.
When9is omitted,4works if4and3are selected. Otherwise the D omissions
are {9,4} or {9,3}. In the first case8has selected neighbors1and3,
which retain7and10. In the second it has only selected neighbor1,
which retains7; the outside3retains10, active through4. Thus8works.

### Exactly two branch vertices omitted: t=2

Let z be the unique omitted member of D. The selected branch pair and z
determine a robust deletion as follows.

| Selected branch pair | Choice of deleted vertex |
| --- | --- |
| {1,7} | 4 if z not in {4,3,8}; otherwise9 |
| {2,10} | 4 if z not in {4,5,11}; otherwise9 |
| {1,2} | 9 if z not in {9,8,11}; 5 if z in {9,8}; 1 if z=11 |
| {7,10} | 4 if z not in {4,5,3}; 8 if z in {4,5}; 7 if z=3 |
| {1,10} | 4 if z not in {4,3}; otherwise9 |
| {2,7} | 9 if z not in {9,11}; otherwise4 |

For {1,7}, deleting4preserves activity at7through1. The outside10has
only3left as a selected neighbor, and3is active through8. Thus4works
whenever z avoids {4,3,8}. The alternative9works whenever z avoids
{9,11,5}: it preserves activity at1through7and covers outside2through
11--5. These two exceptional triples partition D, proving the first row.
The second row has the same argument with the selected chord2--10:
4covers outside7through5--11, while9covers outside1through8--3.

For {1,2}, deleting9works if9,8,11are selected, because1retains8and2
retains11. If z is9or8, delete5: its selected neighbor11retains2,
and the outside7retains the two selected neighbors1,4. If z=11,
delete1: selected neighbors8,9retain3,2, respectively, while outside7
retains4,5. This proves the third row. Its image under the automorphism
gives the fourth row.

For {1,10}, deleting4works if4and3are selected:10retains3, and outside7
retains1,5unless z=5, in which case1is active through8,9. If z is4or3,
delete9:1retains8; outside2retains10and11, since neither is omitted.
The last row is the image of this one under the automorphism.

Every listed vertex is selected and avoids A. The preceding neighbor
checks verify conditions2and3; the chosen vertex also has a selected
neighbor, proving condition1.

### Three branch vertices omitted: t=3

All six members of D are selected. If the remaining branch is1or2,
delete9; if it is7or10, delete4. The selected branch retains its other
selected neighbor on a length-three subdivided edge. The other branch
adjacent to the deleted vertex is omitted, but it retains a selected
neighbor on the other length-three subdivided edge, whose next vertex
is also selected. Thus the new outside vertex and the previously omitted
neighbor both have the required star. No selected neighbor loses its last
selected neighbor. This proves all three conditions and finishes Lemma2.

This proof partitions the omissions by branch membership and derives
each rule from neighborhoods. The accompanying finite checks test the
rules; they are not used to infer the lemma.

## The local upper bound in every outside graph

**Lemma 3.** Let G be any finite simple graph containing an induced copy
of K. Suppose every edge between this copy and the rest of G has its K
endpoint in A={3,11}. If S is inclusion-minimal 2-star-forming in G, then

    |S intersect V(K)| <= 6.

There is no restriction on the outside graph, its bipartiteness, the
number of attachments at A, or the membership of any outside vertex in S.

Suppose C=S intersect V(K) has at least seven vertices, and take v from
Lemma2. Put S'=S minus {v}. For the newly outside vertex v, choose its
selected core neighbor u. Condition2 gives a selected core neighbor of
u other than v, yielding a star through v in S' union {v}.

Now let x be an old outside vertex. If x is adjacent to v, then x lies
in K because v is not an attachment vertex. Condition3 gives a star after
deletion: either two selected neighbors remain, or its remaining selected
neighbor u has a selected neighbor that survives by condition2.

If x is not adjacent to v, take its former witnessing star. A star not
using v survives. A star using v must have v as a leaf and a selected
center u adjacent to v. Since v has no external neighbors, u lies in C.
Condition2 supplies another selected core neighbor of u, which replaces
v as the other leaf. Thus x is still covered.

Every outside vertex is covered, so S' is star-forming, contradicting
inclusion-minimality. This proves the local cap independently of the
outside configuration.

## Exact cyclic value and equality structure

**Theorem.** For every even r>=2, the earlier cyclic family satisfies

    SF_2(J_r)=7r,
    Gamma(J_r)=alpha(J_r)=11r/2,
    beta_2(J_r)=13r/2,
    SF_2(J_r)-beta_2(J_r)=r/2=|V(J_r)|/22.

The ten-vertex cores are disjoint. All remaining vertices are the r shared
ports. Lemma3 gives at most6rselected core vertices, and at most rshared
ports can be selected. Hence every minimal star-forming set has size at
most7r. The earlier union of double-star six-sets and all isolated shared
ports is minimal and has size7r, proving the exact value. The other
identities were proved in the earlier note.

Equality in this bound forces every shared port to be selected and each
core to contain exactly six selected vertices. This is a necessary
condition for attaining sets, not a complete classification of them.
No surplus assigned to one core is needed by another: the local cap holds
with arbitrary external edges, and each global vertex is counted once.

## Scope and next questions

This settles the exact SF value left open in the earlier note and gives
a reusable local upper bound for other compositions of the same core.
It proves no sharp universal coefficient for all subcubic graphs and no
planar or cubic-regular equality theorem. The existing K_{3,3} subdivision
still makes this cyclic family nonplanar. Rectangular grids remain a
separate open problem. The submitted sub-quorum manuscript is preserved.
