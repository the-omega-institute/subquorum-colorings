# Boundary capacity, universal deletion and exact star-forming composition

13 November 2026. The boundary lemma for two-star formation extends to every
positive integer k. We characterize which block selections occur in an
ambient forming set, which selected vertices are indispensable in every
ambient extension, and, under an internal-formation premise, which deletions
are universally safe. The unsafe-deletion certificate needs at most k-1
external vertices, and that bound is sharp. These finite boundary predicates
give an all-k composition theorem.

## 1. Definitions and the local formation test

All graphs are finite and simple. Stars are not required to be induced.
A set S is k-star-forming if every x outside S belongs to a copy of K_(1,k)
in S union {x}, with exactly k selected vertices. Write SF_k(G) for the
largest cardinality of an inclusion-minimal forming set. For C subset V(G),
put N_C(x)=N_G(x) intersect C and d_C(x)=|N_C(x)|. Then x is covered exactly
when

    d_C(x)>=k, or some y in N_C(x) has d_C(y)>=k-1.       (1)

In the first case x is the centre. In the second it is a leaf and y is
the selected centre; the other k-1 distinct leaves are selected neighbours
of y. Extra edges between these vertices do not matter. Formula(1) also
holds for k=1. Formation is upward closed, so a forming S is minimal if
and only if deleting each one of its selected vertices destroys formation.

Let B be an induced block and P subset V(B) its allowed boundary: edges
from B to the exterior may touch only P. The ambient graph is otherwise
arbitrary. Unless a restriction is explicitly stated, universal ambient
claims below range over all finite simple extensions and all forming
selections whose intersection with B is the specified set C.

For two-star formation, the previous boundary result is
`GENERAL_BOUNDARY_SAFE_COMPOSITION.md`. The present all-k statements include
its safety and sufficient composition predicates. The new equivalences
concern the stated universal ambient quantifiers.

## 2. Exactly which selections are realizable

Call C admissible when, for every x in V(B) minus (C union P),

    d_C(x)>=k, or some y in N_C(x) satisfies
    y in P or d_C(y)>=k-1.                              (2)

**Theorem 1.** C is the intersection of a forming ambient set with B if
and only if it is admissible. If so, at most k external selected vertices
are sufficient for a realization.

**Proof.** A nonport x has no exterior neighbour. In a witnessing star it
is either the centre with at least k neighbours in C, or a leaf adjacent
to a selected centre y in C. If y is not a port, all of y's neighbours
also lie in B, giving d_C(y)>=k-1. This proves necessity.

For sufficiency, if P is nonempty, add k new selected vertices and join
each of them to every port. Select C and those new vertices. An unselected
port has k selected neighbours and is covered. Every selected port has
at least k selected neighbours, so it can serve as a centre for any of its
unselected original neighbours. Equation(2) therefore covers every original
unselected nonport. All new vertices are selected. If P is empty, (2)
is already the internal formation test and no new vertex is required. QED.

We call this common extension the saturated extension. Its k new vertices
are shared selected neighbours, rather than private leaves at each port.
The theorem concerns formation, whose local witnessing stars need not be
disjoint.

## 3. Exact universal indispensability

Assume C is admissible and v belongs to C. Put C_v=C minus {v}. Call x a
protected failure for v if

    x in V(B) minus (C_v union P),
    d_(C_v)(x)<k,
    N_(C_v)(x) intersect P is empty,
    d_(C_v)(y)<k-1 for every y in N_(C_v)(x).             (3)

**Theorem 2.** Deleting v destroys formation in every forming ambient
extension with block intersection C if and only if a protected failure
exists. If none exists, the saturated extension of Theorem1 is a forming
ambient set in which deleting v preserves formation. Thus the same at-most-k
external vertices simultaneously test every selected vertex v.

**Proof.** A protected x acquires no exterior neighbours. None of its
selected neighbours is a port, so those neighbours acquire no exterior
activity either. Formula(1) fails at x after deletion, in every extension.

Conversely use the saturated extension. It is forming by admissibility.
After deleting v, every unselected port, including v itself if it is a
port, still has the k new selected neighbours. Every remaining selected
port still has these neighbours, so an original unselected nonport with a
selected port neighbour is covered. If x is another original unselected
nonport, failure of(3) says either d_(C_v)(x)>=k or it has a selected
nonport neighbour y with d_(C_v)(y)>=k-1. It is covered by(1). The exterior
vertices remain selected. Hence deletion preserves formation. QED.

Admissibility is necessary in this statement: otherwise there are no forming
extensions at all and a universal assertion would be vacuous. A vertex may
be indispensable in a particular extension without having a protected
failure; the theorem characterizes indispensability in every extension.

## 4. Exact universal safety with an internal premise

For a selected port p define its truncated internal capacity

    a_C(p)=min(k-1,d_C(p)).                             (4)

Let D be a subset of C minus P, and assume C minus D forms B internally.
The deleted vertices have no exterior neighbours. This internal premise
is part of the following equivalence.

**Theorem 3.** Deleting D preserves formation in every forming ambient
extension with block intersection C if and only if

    a_C(p)=a_(C minus D)(p) for every p in C intersect P.(5)

If(5) fails, an actual extension with at most k-1 new vertices witnesses
failure of safety. For every k>=2 this bound cannot be decreased uniformly.
For k=1 the capacity is identically zero and the internal premise suffices.

**Proof of sufficiency.** Formula(1) covers all unselected vertices of B
after deletion using the assumed internal forming set. For an unselected
exterior x, its selected neighbourhood is unchanged because x is not
adjacent to D. A star centred at x therefore survives. The selected degree
of any exterior centre is also unchanged. If an old witness instead used
a selected centre p in B, that centre is a port. Its total selected degree
is d_C(p)+e_p, where e_p is its unchanged exterior selected degree.
Equality(5) preserves whether this total reaches k-1, for every e_p>=0.
The star can therefore be replaced using surviving selected neighbours.
Every exterior x remains covered.

**Proof of necessity and the size bound.** Suppose(5) fails at p. Set
d_0=d_C(p), d_1=d_(C minus D)(p). Then d_0>=1, d_1<k-1 and d_1<d_0.
In particular k>=2. Add

    h=max(0,k-1-d_0)

selected leaves at p and one further unselected leaf x there. Select C
and the h new selected leaves. The internal premise and upward closure
show that C forms B. Before deletion, p has d_0+h>=k-1 selected neighbours,
so it covers x. After deletion its selected degree is d_1+h<k-1. The leaf
x has only one selected neighbour, fewer than k, and that neighbour cannot
be a star centre. Formation fails at x. Since d_0>=1, h+1<=k-1.

**Sharpness.** Take B=K_(1,k), select all of B, make just one leaf p a port,
and delete its centre v. The remaining k selected leaves form B internally,
and p's selected degree decreases from one to zero. The preceding
construction uses exactly k-2 selected exterior leaves and one unselected
exterior leaf, hence k-1 new vertices.

Consider any counterextension with fewer new vertices. A lost witness for
an exterior vertex x cannot have been centred at x or at an exterior
selected vertex, since no exterior vertex is adjacent to v. It must have
been centred at p and used v as one of its selected leaves. As v is p's
only neighbour in B, that witness needs k-2 distinct selected exterior
vertices as its other leaves, in addition to the unselected exterior x.
It therefore needs at least k-1 new vertices, a contradiction. All vertices
of B outside the post-deletion selection are covered internally. This
proves sharpness. QED.

For k>=3, preserving merely positive activity at a selected port is
insufficient. An all-k counterfamily has 2k vertices: a central edge pv,
k-2 selected leaves at p, k-1 selected leaves at v, and one unselected
leaf x at p. The block excludes x and all its vertices are selected.
After deleting v the block still forms: v has its k selected neighbours.
The port p retains k-2>=1 selected neighbours, but its selected degree has
fallen from k-1 to k-2 and x becomes uncovered. Every graph in this family
is a bipartite tree. This refutes the boolean extension rule, not Theorem3.

## 5. Bipartite ambient extensions

If B has a specified proper bipartition and the ambient graph must respect
it, Theorems1--2 keep exactly the same block predicates. For each physical
side containing ports, add k selected vertices on the opposite side and
join them to all ports on that side. This uses at most 2k new vertices and
gives the same saturated proof within the bipartite class. A selected port
has k new selected neighbours, and an unselected port has k new neighbours.

Theorem3 and its sharp k-1 bound also remain valid in the bipartite class:
the obstruction adds leaves to one port, and the sharpness block is a star.
These realizations impose no upper bound on exterior degrees and need not
preserve higher connectivity or minimum degree. Equivalences for extensions
with those additional restrictions require separate realization arguments.

## 6. Caps and exact composition for arbitrary k

Suppose for every admissible C of size greater than s there is v in C minus
P such that C minus {v} forms B and(5) holds. Then every globally minimal
k-star-forming set meets B in at most s vertices. Indeed its intersection
is admissible by Theorem1, and Theorem3 would otherwise give a safe deletion.
This is a sufficient finite cap predicate; necessity for the cap is not
asserted.

Take disjoint induced blocks B_i with boundaries P_i satisfying such caps
s_i. In each block choose an internally forming C_i of size s_i. Suppose
every v in C_i has a protected failure(3). Add arbitrary edges only between
the boundaries of different blocks. The union of the C_i forms: old local
stars survive every added edge. It is minimal because each deletion still
fails at its protected original witness. The caps give the reverse bound,
so

    SF_k(G)=sum_i s_i.                                  (6)

Blocks and boundaries can differ, and the interface graph has no degree or
connectivity restriction. At k=2 the earlier four-port construction satisfies
these hypotheses with s_i=6. The new checker recovers its 174 cap cases and
all six protected deletions using the all-k predicates.

As an explicit all-k application, start with any finite simple graph H.
At vertex i attach t_i private leaves, where t_i>=max(k,2). Then

    SF_k(G)=beta_2(G)=sum_i t_i.                         (7)

For the forming identity use the star blocks K_(1,t_i), with their centres
as the only ports. The only selection larger than t_i is the entire block.
Deleting a leaf leaves an internal forming set and preserves the centre's
capacity k-1, since t_i-1>=k-1. This proves the cap. Select all private leaves;
they form internally and each is its own protected deletion failure. Apply(6).
For dissociation, restriction to a star of at least two leaves gives at most
t_i selected vertices, and all the private leaves together are independent.
Thus beta_2 is their total even when H is not bipartite. The identity(7)
is an elementary application of the criterion, not an extremal gap claim.

## 7. Verification and scope

`develop/star_boundary_capacity.py` computes admissibility, truncated capacity,
protected witnesses and the explicit realizing or obstructing extensions.
The checker independently enumerates actual stars by a centre and k distinct
leaves, rather than reusing formula(1). It tests all simple blocks through
four vertices, all port and selected subsets, k=1,...,5; arbitrary two-vertex
exteriors through block order three, all interfaces and selections,
k=1,...,4; and the entire smaller-exterior sharpness test at k=2,...,6.
The family arguments above prove every k; these finite computations check
the predicates and coordinates. Corona parameter enumeration has its exact
finite range in the report. Run

    python3 -B scripts/check_star_boundary_capacity.py

The theorem replaces the all-k analogue of the boundary-activity question by
explicit finite local data and gives exact universal lower witnesses. It
does not determine sharp unrestricted degree/connectivity gap constants or
the rectangular-grid triple equality. No new Lean execution is claimed.
