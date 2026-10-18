# Unbounded star-forming gaps in two-connected subcubic bipartite graphs

19 October 2026. The maximum-degree-four hypothesis in the earlier gap
construction is unnecessary. The construction below gives two-connected
bipartite graphs of minimum degree two and maximum degree three with an
unbounded gap. The argument is general; finite checks are independent controls.

## Statement and definitions

A set S is 2-star-forming if every vertex x outside S belongs to a
non-induced K_{1,2} in the subgraph on S union {x}. Equivalently, either
x has at least two neighbors in S, or x has a neighbor in S which has a
neighbor in S. SF_2 is the maximum cardinality of an inclusion-minimal
2-star-forming set. The dissociation number beta_2 is the maximum size of
a set inducing maximum degree at most one.

**Theorem.** For each even integer r>=2 there is a two-connected bipartite
graph J_r with 11r vertices, 14r edges, minimum degree two and maximum
degree three such that

    beta_2(J_r) = 13r/2,       SF_2(J_r) >= 7r.

Consequently

    SF_2(J_r) - beta_2(J_r) >= r/2 = |V(J_r)|/22.

The SF value is a proved lower bound; no exact value for general r or
optimality of the coefficient 1/22 is claimed. In particular, maximum degree
three does not guarantee beta_2=SF_2, even with two-connectivity and no leaves.

## The twelve-vertex building block

Let H have bipartition a0,...,a5 and b0,...,b5 with cross-edge matrix

    000001
    011100
    000111
    101010
    010010
    010001

Use zero-based numerical labels a_i=i and b_i=6+i. Thus

    N(0)={11},        N(1)={7,8,9},     N(2)={9,10,11},
    N(3)={6,8,10},    N(4)={7,10},      N(5)={7,11},
    N(6)={3},         N(7)={1,4,5},     N(8)={1,3},
    N(9)={1,2},       N(10)={2,3,4},    N(11)={0,2,5}.

The leaves 0 and 6 will be called ports. All other vertices form a core K.
The core has the spanning cycle

    1,9,2,11,5,7,4,10,3,8,1.

Its only additional edges are 1--7 and 2--10. In particular K is
two-connected. The full block has fourteen edges and maximum degree three.

### A minimal eight-set

Put S={0,1,4,5,6,7,8,9}. Vertices 0 and 6 are isolated in H[S]; the other
six selected vertices induce a double star, with adjacent centers 1 and 7.
The four outside vertices satisfy the local star test:

| Outside vertex | Selected neighbors | Reason |
| --- | --- | --- |
| 2 | {9} | 9 has selected neighbor 1 |
| 3 | {6,8} | two selected neighbors |
| 10 | {4} | 4 has selected neighbor 7 |
| 11 | {0,5} | two selected neighbors |

The following deletion witnesses prove minimality.

| Deleted vertex | Failing outside vertex | Reason after deletion |
| --- | --- | --- |
| 0 | 0 | no selected neighbor |
| 1 | 2 | only selected neighbor 9, now isolated |
| 4 | 10 | no selected neighbor |
| 5 | 11 | only selected neighbor 0, isolated |
| 6 | 6 | no selected neighbor |
| 7 | 10 | only selected neighbor 4, now isolated |
| 8 | 3 | only selected neighbor 6, isolated |
| 9 | 2 | no selected neighbor |

Star formation is upward closed: a star witnessing an outside vertex
remains available when selected vertices are added. Hence failure of every
single deletion proves inclusion-minimality. This proves SF_2(H)>=8.

### Exact dissociation bound, with port states

**Lemma.** Every dissociation set D of H has size at most seven. If neither
port belongs to D, it has size at most six. Both bounds can be attained.
More precisely, for prescribed port memberships (00,01,10,11), the maximum
sizes are (6,7,7,7), respectively. In every state an attaining set can be
chosen so that each selected port is isolated in the selected subgraph.

First, a dissociation set in a ten-cycle has size at most six. Otherwise
the cycle's ten consecutive triples, each containing at most two selected
vertices, would give 3|D|<=20. Since K contains a spanning ten-cycle, the
same bound applies to K. This proves the claim when both ports are absent.

To bound an arbitrary dissociation set of H, we may assume both leaves
0 and 6 are selected without decreasing cardinality. If a leaf is absent
and its neighbor is present, replace that neighbor by the leaf. If both
are absent, add the leaf. These operations preserve dissociation. The two
leaf neighbors are distinct non-leaves, so the operations do not remove a
previously selected leaf.

Write x=11 and y=3 for their neighbors. There are four cases.

* If x,y are selected, vertices 2,5,8,10 must be absent. The remaining
  four core candidates {1,4,7,9} induce the path 4--7--1--9, so at most
  three are selected. Together with 0,6,x,y this gives at most seven.
* If y is selected and x is absent, vertices 8,10 are absent. The remaining
  six candidates {1,2,4,5,7,9} contain the disjoint three-vertex paths
  4--7--5 and 1--9--2. At most four of them are selected. Adding 0,6,y
  gives at most seven.
* If x is selected and y is absent, vertices 2,5 are absent. The remaining
  six candidates {1,4,7,8,9,10} contain disjoint paths 8--1--9 and
  7--4--10. Again at most four are selected, giving at most seven overall.
* If x,y are absent, the remaining core candidates
  L={1,2,4,5,7,8,9,10} induce a six-cycle 1--7--4--10--2--9--1 with
  pendants 8 at 1 and 5 at 7. We show that at most five can be selected.
  If both 1 and 7 are omitted, all six remaining candidates would include
  the path 9--2--10--4. If 1 is selected in a six-set, its degree-three
  neighborhood forces both omissions to be two of {7,8,9}. Omitting
  {7,8}, {7,9}, or {8,9} leaves, respectively, a selected path
  2--10--4, 2--10--4, or 4--7--5. The case with 7 selected follows from
  the automorphism (1 7)(9 4)(2 10)(8 5) of L. Thus no six-set is a
  dissociation set. Adding the two ports gives at most seven.

The following sets attain the four port-state bounds; selected ports have
no selected neighbor in each set:

| Membership of (0,6) | Dissociation set | Size |
| --- | --- | --- |
| (0,0) | {2,3,4,5,8,9} | 6 |
| (0,1) | {1,4,5,6,8,10,11} | 7 |
| (1,0) | {0,2,3,4,5,8,9} | 7 |
| (1,1) | {0,1,2,4,5,6,8} | 7 |

This proves the lemma by a readable case argument, not by enumeration.
It also proves beta_2(H)=7 and hence a strict subcubic gap in the block.

## Cyclic identification and degree control

Take r copies H_i, indexed cyclically. Identify port 6 of H_i with port 0
of H_{i+1}; denote the resulting shared vertex by w_i. Every original port
is used exactly once in an identification and every w_i lies in exactly
two distinct blocks, also when r=2. No core vertex is identified. The
resulting graph is J_r.

There are ten core vertices and one shared vertex per block, hence 11r
vertices. No edges coincide under identification, so there are 14r edges.
Each shared vertex has degree two, with neighbors 3 in H_i and 11 in
H_{i+1}. All core degrees remain their original degrees, either two or
three. Thus the minimum and maximum degrees are two and three.

For even r, reverse the original bipartition in alternating copies.
The two ports being identified then belong to the same global part.
Every edge still crosses the global bipartition, so J_r is bipartite.

Each core has its spanning ten-cycle. Deleting a core vertex leaves that
core connected and can destroy at most one inter-core connection, since
its two port-neighbors 3 and 11 are distinct. Deleting a shared vertex
destroys exactly one inter-core connection. The cyclic quotient of cores
remains connected after losing at most one connection. When r=2 the two
connections are distinct and one survives. The surviving shared vertices
also attach to the surviving cores. Thus deleting any vertex leaves J_r
connected, proving two-connectivity.

## Exact global dissociation number without double counting

Let D be any dissociation set of J_r. Let k be the number of selected
shared vertices and c the number of blocks incident to at least one
selected shared vertex. The port-state lemma gives

    sum_i |D intersect H_i| <= 6r+c.

Every core vertex is counted once in this sum and every selected shared
vertex exactly twice. Therefore

    |D| = sum_i |D intersect H_i| - k <= 6r+c-k.

Each selected shared vertex touches two blocks, so c<=2k; also c<=r.
Consequently

    c-k <= min(k,r-k) <= floor(r/2).

For even r this proves beta_2(J_r)<=13r/2. The subtraction of k is essential:
a shared selected port cannot be counted as two independent contributions.

For attainment, select alternating shared vertices around the cycle.
Every block has precisely one selected port. In each block take the
corresponding seven-vertex port-state witness from the table. Each selected
port is isolated in its local selected subgraph on both sides, so these
choices combine into a global dissociation set. There are seven selections
per block, with r/2 shared selections counted twice, giving

    7r-r/2 = 13r/2.

This establishes the exact dissociation number.

## Global minimal star formation

Take the union of the block eight-sets S. The two identified ports are
selected in every block, so the resulting set S_r has size

    |S_r| = 8r-r = 7r.

All shared vertices remain isolated in J_r[S_r], since their two core
neighbors, 3 and 11 in the incident blocks, are outside S_r. Every outside
vertex is a core vertex and retains the star in its own block listed in
the first table. Thus S_r is star-forming.

Delete a selected core vertex. Its deletion witness in its own block is
a non-port outside vertex and has no new incident edges. The isolation
conditions in the deletion table are unchanged: in particular, a shared
port remains isolated in the selected set. That witness still fails.
If instead a shared vertex is deleted, it itself has no selected neighbor
and fails the star condition. Hence every single deletion fails. Upward
closure proves inclusion-minimality, and SF_2(J_r)>=7r follows.

Together with the exact dissociation number this proves the theorem for
every even r>=2, without extrapolating any finite enumeration.

## Degree two: a sharp threshold for two-connected graphs

For completeness, every cycle C_n, n>=3, satisfies

    SF_2(C_n) = beta_2(C_n) = floor(2n/3).

Here is a direct upper-bound argument. In a minimal star-forming selection
there is at least one selected and one omitted vertex. Split the cyclic
word into maximal selected runs and omitted gaps. Every gap has length one
or two, since the middle of three consecutive omitted vertices has no
selected neighbor. A selected run has length at most four: deleting the
third vertex in a run of at least five preserves its two neighbors'
selected-neighbor activity and leaves the newly omitted vertex with two
selected neighbors, so it preserves every outside star.

A run of length three must have a neighboring gap of length two. Otherwise
deleting its middle vertex leaves both adjacent omitted vertices with two
selected neighbors, and preserves every other star. A run of length four
must have gaps of length two on both sides: if the left gap has length one,
delete the second vertex of the run; if the right gap has length one,
delete the third. The same star test shows each deletion is safe.

Let there be t runs and q gaps of length two. For each run of length l,
the excess l-2 is at most the number of incidences with length-two gaps:
this is automatic for l<=2, and is exactly the restrictions just proved
for l=3,4. Summing counts every length-two gap twice, including when it
is adjacent to both ends of the same run. Thus the selected size s obeys

    s<=2t+2q=2(n-s),

so s<=floor(2n/3). This also explicitly prevents reuse of gap compensation:
each length-two gap has precisely two incidences and supplies at most two
units of excess in the entire argument.

Every dissociation set in C_n has size at most floor(2n/3), by summing the
n consecutive-triple inequalities. The bound is attained by the cyclic
binary words (110)^a, (110)^a0, or (110)^a10 according as n=3a,3a+1,3a+2.
A maximum dissociation set is a minimal star-forming set: maximality says
that adding any outside vertex creates a two-leaf star through that vertex;
after deleting any selected vertex, that vertex has either no selected
neighbor or a unique selected neighbor which is now isolated. This gives
SF_2>=beta_2 and finishes the cycle equality.

A finite simple two-connected graph of maximum degree two is a cycle.
Consequently maximum degree three is the first degree bound at which a
strict gap can occur in two-connected bipartite graphs. This is a degree
threshold, not a smallest-order assertion.

## Research boundary

This construction resolves the maximum-degree-three feasibility question
and amplifies its gap within two-connected bipartite graphs of minimum
degree two. The source paper arXiv:2610.03785v2 was reread on October19:
its bipartite and triangle-free equality conjectures are the relevant
context; no subcubic or cycle specialization was found there. This is not
a complete literature-priority search. The exact SF_2(J_r), a sharp universal gap bound for subcubic
bipartite graphs, cubic regular graphs, and rectangular-grid equality
remain separate questions. No smallest-order or literature-priority claim
is made. The original submitted sub-quorum manuscript is unchanged.

## Reproduction and verification scope

Run the independent literal-star and proper-subset checks, port-state
enumeration and cyclic controls with

```sh
python3 scripts/check_subcubic_starforming.py --output output/subcubic-starforming-controls.json
g++ -std=c++20 -O3 scripts/explore_subcubic_starforming.cpp -o /tmp/subcubic-check
/tmp/subcubic-check --two-block-cycle
python3 scripts/check_subcubic_formal.py --lean /path/to/lean-4.33.0 --output output/subcubic-starforming-formal-check.json
```

The C++ check enumerates every subset of the 22-vertex J_2. Its exact
values beta_2=13 and SF_2=14 are finite evidence, not an all-r SF upper bound.
The Python checks compare the literal and local star predicates on all
4,096 block subsets and test all proper subsets for block minimality.
They give beta_2(H)=7, SF_2(H)=8 and check 16 cyclic graphs, r=2,4,...,32.

The standalone Lean4.33.0 module uses only Std, independently of Mathlib
caches. It verifies base simplicity, the local star predicate, deletion
minimality, the dissociation port cap over all 4,096 masks and the general
arithmetic inequality excluding double counting. Its star definition is
the center-or-leaf local characterization used in this note. The existing
[literal/local equivalence](../formal/StarForming/Amplification.lean) separately
relates that characterization to literal two-leaf stars. There is no new
formal bridge between the standalone relation encoding and SimpleGraph.
The cyclic identification, exact global attainment, connectivity and
cycle equality have written proofs here; they are not claimed as newly
Lean formalized.
