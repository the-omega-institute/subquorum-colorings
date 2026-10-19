# Exported boundary evidence and the limit of bare-port charging

19 October 2026. There are two results here: a general graph-level
export theorem, and an explicit infinite obstruction to a proposed
compensation rule. The obstruction disproves that rule, not the target
SF_2(L_k)<=36k. The established Heawood inequality |C|+t<=8 remains valid.

## General export theorem

Use the star clauses

    A_u={u} union N(u),
    B_(u,v)={u} union (N(u) minus {v}) union (N(v) minus {u}), uv an edge.

A selection forms precisely when it hits all these clauses; it is
inclusion-minimal precisely when every selected vertex owns a private
clause, intersecting the selection only at itself. The
[private-clause proof](PRIVATE_CLAUSES_AND_BOUNDARY_ACCOUNTING.md) establishes
these equivalences for arbitrary simple graphs.

Let K be an internal graph on a specified core of an ambient simple
graph G. All K edges remain, and every core non-port has exactly its
K-neighbors in G. Only designated ports can have additional edges.
Let S be a minimal forming selection in G and C its core restriction.
Call a selected core non-port **unsupported internally** when it owns
no private star clause in K with respect to C. C need not form K.

**Theorem 1 (exported private evidence).** Every internally unsupported
vertex u has a selected core port p and an adjacent vertex q across
a new edge such that:

1. u is the sole selected K-neighbor of p;
2. q is omitted and p is its sole selected G-neighbor.

Different unsupported vertices cannot use the same q. No finiteness,
degree, bipartite or core-formation hypothesis is needed.

**Proof.** Choose a global private clause for u. A closed clause gives
a private core clause by restriction. An oriented clause on an old
K-edge also gives one, since all edges incident with u are unchanged.
For a clause on a new edge, u cannot be its first endpoint, because u
is a non-port. If u is adjacent to its first endpoint a, the core
closed clause A_a is contained in the global oriented clause: its
other endpoint is not an old K-neighbor of a. This again gives an
internal private clause.

The only remaining case is B_(q,p) on a new edge qp, with u an old
neighbor of p. Thus p is a core port. All selected old neighbors of
p belong to this private clause, so u is the sole one. If p were
omitted, A_p(K) would be private to u, a contradiction. Hence p is
selected. Also q is omitted, since q itself belongs to B_(q,p) and
q!=u.

Suppose some selected z!=p is adjacent to q. Then z belongs to the
private B_(q,p), so z=u. But if q were adjacent to u, that edge would
be old since u is a non-port. The core clause A_q(K) would then
contain u and be contained in B_(q,p)(G), since qp is not old. This
would be an internal private clause for u. The contradiction proves
that p is q's only selected neighbor.

Finally, if two owners use the same q, its sole selected neighbor
forces their ports p to agree; that port's sole selected old neighbor
forces their owners to agree. This proves the no-reuse assertion. QED.

Both the full export theorem and owner uniqueness are checked in
[BoundaryLoss.lean](../formal/StarForming/BoundaryLoss.lean).
The [receipt](../output/boundary-loss-formal-check.json) records two
general graph-level declarations with standard logical axioms only.

## Consequence for Heawood compensation

In L_k, each new edge from a core port reaches one of its attached
broken Heawood blocks. Thus the q supplied by Theorem 1 is a bare
Heawood port: it and both its internal block neighbors are omitted.
If U denotes all internally unsupported core non-ports, and T the
total number of bare Heawood ports, injectivity gives

    |U|<=T.

The [additive block-loss theorem](BARE_HEAWOOD_PORT_COMPENSATION.md)
then gives, with C_j the attached block restrictions and C_0 the core,

    delta_j=8-|C_j| >= t_j,
    |S|=24k+|C_0|-sum_j delta_j
       <=24k+|C_0|-T
       <=24k+|C_0|-|U|.

These inequalities are general and sum every block once. Two exported
owners in one block require two distinct bare ports, hence two losses.
They extend the earlier periodic-phase reasoning without requiring a
specific core pattern.

To conclude |S|<=36k from only these quantities, one might hope that

    |C_0|-12k<=T,                                      (R)

or even that selected core ports plus selected internally private
non-ports always total at most12k. Both proposals are false. The
following actual ambient minimal selection disproves them even when
C_0 itself forms the core. This is stronger than a local set which
merely passes a necessary certificate test.

## Explicit base obstruction in L_2

The base has124vertices. Core labels are

    H_i=i, U_i=12+i, X_i=24+i (0<=i<12), Y_j=36+j (0<=j<4).

H and X initially form12cycles, H_i--U_i--X_i, and
U_(6b+j)--Y_(2b+(j mod2)). Delete X_(2j)X_(2j+1) for0<=j<6.
Attach block j with local labels0,...,13 at offset40+14j. In every
block points are0,...,6 and line7+a meets a,a-1,a-3 modulo7; delete
edge0--8. Join its local0 to X_(2j+1) and local8 to X_(2j).

Select the following25core vertices:

    C_0={1,5,7,10,12,14,15,17,19,21,23,
         24,25,26,28,29,30,31,32,33,34,35,36,37,38}.

Select these local vertices in the six attached blocks:

| Block j | Local selection | Size | Bare ports | Actual loss8-size |
|---|---|---:|---:|---:|
| 0 | 1,4,6,10,12,13 | 6 | 0 | 2 |
| 1 | 3,4,6,7,8,12,13 | 7 | 0 | 1 |
| 2 | 0,1,4,6,12,13 | 6 | 0 | 2 |
| 3 | 4,8,9,10,12,13 | 6 | 0 | 2 |
| 4 | 3,7,8,9,12,13 | 6 | 0 | 2 |
| 5 | 1,4,6,10,12,13 | 6 | 0 | 2 |

The full selection S has25+37=62vertices. It has T=0, although
|C_0|-12k=25-24=1. Thus (R) fails. Its eleven actual block losses
amply compensate the core excess; the target bound is not violated.

The core restriction itself forms Q_2: all omitted core vertices have
at least two selected core neighbors except3,4,8, covered by the
core-only stars(3,15,37),(4,5,17),(8,7,19). Its fourteen selected non-ports
all have private internal clauses, as this explicit table shows.
The other eleven selected core vertices are ports. Consequently the
suggested partial private-owner cap would have to bound25by24.

| Owner | Private core clause | Owner | Private core clause |
|---:|---|---:|---|
| 1 | A_1 | 5 | A_4 |
| 7 | A_8 | 10 | A_10 |
| 12 | B_(0,1) | 14 | B_(2,1) |
| 15 | A_3 | 17 | B_(4,5) |
| 19 | B_(8,7) | 21 | B_(9,10) |
| 23 | B_(11,10) | 36 | B_(16,28) |
| 37 | B_(3,15) | 38 | A_38 |

This example has U empty, consistent with Theorem 1. It shows why
controlling exported non-port certificates alone cannot settle the
whole core count. Selected ports and other block states still matter.

## Direct formation and minimality certificates

All omitted base vertices have at least two selected neighbors except
the fifteen listed below. Each listed triple gives an omitted vertex,
its sole selected neighbor, and that neighbor's selected neighbor.
Each triple is therefore a non-induced star with the omitted vertex
as a leaf. The displayed adjacency rules verify the triples directly.

    (3,15,37), (4,5,17), (8,7,19), (54,61,58), (55,62,26),
    (56,66,58), (63,60,61), (64,57,67), (70,80,72), (71,81,74),
    (78,68,29), (89,86,94), (93,86,94), (106,99,109), (107,99,109).

For minimality, align each row's selected vertices with its row of
failure vertices. After deleting the selected vertex, the indicated
vertex is outside and has either no selected neighbor or a sole
selected neighbor which is isolated in the remaining selection.
This directly certifies failure of every one of the62deletions.

| Group | Deleted selected vertices, in order | Corresponding failure vertices |
|---|---|---|
| Core | 1,5,7,10,12,14,15,17,19,21,23,24,25,26,28,29,30,31,32,33,34,35,36,37,38 | 1,4,8,10,0,2,3,4,8,9,11,48,40,55,28,78,18,82,20,96,118,110,16,3,38 |
| Block0 | 41,44,46,50,52,53 | 41,44,46,50,42,43 |
| Block1 | 57,58,60,61,62,66,67 | 64,56,63,54,55,56,64 |
| Block2 | 68,69,72,74,80,81 | 78,69,70,71,70,71 |
| Block3 | 86,90,91,92,94,95 | 86,83,88,85,89,85 |
| Block4 | 99,103,104,105,108,109 | 99,100,97,98,98,106 |
| Block5 | 111,114,116,120,122,123 | 111,114,116,120,112,113 |

Formation is upward closed, so failure of every single deletion proves
inclusion-minimality. This is an explicit certificate proof, not an
inference from a reported optimum or solver infeasibility.

## An infinite obstruction from covers

**Theorem 2.** For every r>=1, L_(2r) has an inclusion-minimal forming
selection S_r with

    |S_r|=62r,  |S_r intersect V(Q_(2r))|=25r,  T(S_r)=0.

In particular, (R) fails by r on this infinite family of actual minimal
selections, even though their core restrictions form the core.

**Proof.** Use the following projection pi from L_(2r) onto L_2:

    H_i -> H_(i mod12),  U_i -> U_(i mod12),  X_i -> X_(i mod12),
    Y_j -> Y_(j mod4),
    local vertex v of block b -> local vertex v of block(b mod6).

It preserves all incidences, deleted-pair attachments and cyclic
seams. At H the two cyclic neighbors project to distinct neighbors
and its U-neighbor projects to the third. At U its H,X,Y-neighbors
project to the three different types. At X the one retained cyclic
neighbor, U-neighbor and attached port project to its three neighbors.
At a hub the three U-neighbors retain their three distinct indices
within a six-index block. Within a Heawood block the local incidence
map is the identity; a port's extra neighbor also projects correctly.
These cases prove that pi is locally bijective. Every fiber has size r.

The base L_2 is bipartite, hence triangle-free. The general
[triangle-free cover pullback theorem](COVERING_PULLBACK_AND_CUBIC_SEARCH.md)
therefore makes S_r=pi^(-1)(S) inclusion-minimal and forming. That
theorem has a general non-enumerative proof and
[Lean source](../formal/StarForming/CoverPullback.lean).
The same local bijections show that the restricted core is covered
by its25rselected vertices, because its base core restriction forms.

Fiber counting gives62rselected vertices and25rselected core vertices.
The internal neighborhoods of block ports project bijectively, so the
absence of bare ports is preserved. There are6rblocks whose patterns
repeat the displayed six selections; their total actual loss is11r.
This proves all assertions. QED.

The numerical identities here are

    core excess = r > T=0,
    total actual block loss =11r,
    |S_r|=48r+25r-11r=62r <72r=36k.

Thus the candidate rule fails while the target inequality holds on
these witnesses. The theorem makes no claim that these selections
maximize SF_2, and does not alter exactSF for k<=7 or the larger-k
interval.

## Verification and next mathematical target

The [export controls](../scripts/check_boundary_loss.py) check1100small
graphs,5774minimal sets and180779induced-core/selection instances,
with120unsupported owners. They independently check the export and
unique-ownership conclusions and a nonvacuous L_2phase example.
The finite k=1 partial private-owner budget is12; the explicit k=2
example above disproves extrapolating that budget.
[Export receipt](../output/boundary-loss-controls.json).

The [obstruction checker](../scripts/check_bare_port_only_obstruction.py)
checks the exact base stars and failure table, independently repeats
all62deletions using literal stars, and checks twelve covering lengths
for local bijectivity, private clauses, all block losses and zero bare
ports. The all-r proof uses the covering theorem, not finite extrapolation.
[Complete certificate](../output/bare-port-only-obstruction.json).

Bounded SAT discovered the examples. Its
[archived receipts](../output/boundary-loss-sat-discovery.json) are
separate from the explicit proofs and independent controls. No solver
UNSAT or timeout is used as a premise.

The next target must incorporate **non-bare block losses** and the
private evidence of selected core ports. The exact accounting variable
is delta_j=8-|C_j|, not merely its lower certificate t_j. A sufficient
uniform theorem would charge |C_0|-12k to sum_j delta_j, with actual
ownership or a local potential preventing repeated use. The present
results neither establish that theorem nor refute its equivalent
target |S|<=36k.

Reproduction:

    python3 scripts/check_boundary_loss.py --output output/boundary-loss-controls.json
    python3 scripts/check_bare_port_only_obstruction.py --output output/bare-port-only-obstruction.json
    python3 scripts/check_cover_pullback_formal.py --audit boundary-loss --lean /path/to/lean-4.33.0 --output output/boundary-loss-formal-check.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
