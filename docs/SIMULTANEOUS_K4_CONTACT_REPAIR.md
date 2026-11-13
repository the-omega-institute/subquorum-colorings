# Simultaneous K4 repair through separated owner pairs

13 November 2026. This gives a sufficient contact criterion for the actual
all-helper bound, a pseudoforest corollary, and a connected mixed-cycle family
with exact all-helper optimum. Criterion failure does not refute the bound.

## 1. Domain and theorem

Use N=2b indices, a perfect helper matching P, a partial witness matching Q,
and A=P union Q. Physical colours agree on P and differ on Q and owner
edges B. Assume B consists of even-order paths and even cycles. In the
physical graph each helper is adjacent to its P-pair of witnesses; witness v
is adjacent to owner v, and Q joins witnesses while B joins owners. Write
beta_I for the largest dissociation set containing every helper. The exact
established identity is

    beta_I=3b-tau,   tau=min_{Delta(B[V minus U])<=1} nu(A[U]).       (1)

The target is beta_I>=ceil(8b/3), equivalently tau<=floor(N/6).

Choose R as follows. On an owner C4 use its two VIRTUAL opposite diagonals;
on every other owner component choose a perfect matching of actual owner
edges. Thus R is a perfect matching on the indices. Define F by taking the
remaining owner edges outside owner C4s. Then F is a matching. Contract each
R-pair to a node to form H, with edges supplied by F. H has maximum degree
two; the two virtual nodes of every owner C4 are isolated. Outside those
owner squares, no pair of R-nodes has two F-edges: that would itself be an
owner C4, for which we used the virtual convention instead.

Let J=A union R. A K4 component of J consists of an entire auxiliary square
and its two R-diagonals. Call such a component bad. The missing diagonals of
an auxiliary square change physical colour, whereas the virtual opposite
diagonals of an owner C4 preserve it. Thus a bad component contains no vertex
of an owner C4. Every bad component gives a binary part consisting of its
two R-nodes.

Join candidate nodes from DISTINCT binary parts when their H-distance is one
or two. These are the contacts. Multiple witnesses for the same candidate
contact are collapsed; contacts involving different candidate members of the
same two parts remain distinct. The resulting graph on parts is a multigraph.

**Theorem.** If one can select one node from each binary part with no contact
between any two selected nodes, then beta_I>=ceil(8b/3). This selection is an
exact 2-SAT problem: a contact forbids one pair of binary choices. This is a
sufficient criterion, not a characterization of the target. Owner paths of
odd order are outside this version of the theorem.

## 2. Three actual physical certificates

Call selected R-pairs active and the other bad pairs inactive. Distinct active
nodes have H-distance at least three. Delete all bad components from J.
Its exterior is properly three-colourable: it has maximum degree three and
has no K4 component, so Brooks' theorem applies, with paths and cycles also
three-colourable. Fix such a colouring with labels 0,1,2.

Each active pair has at most two F-neighbours. For each exterior neighbour x,
forbid the colour of the R-mate of x as a bonus colour for that active pair.
There are at most two forbidden colours. Choose any remaining colour g.
Neighbours in another bad component belong to its inactive pair, since two
active pairs cannot be adjacent. Such an inactive pair supplies no owners.

For each colour c construct a physical selected set D_c containing:

* All b helpers.
* Exterior witnesses of colour c, and both witnesses of each inactive pair.
* Both owners of an active pair if c is its bonus colour, otherwise one of
  its owners.
* One owner from each exterior R-pair, avoiding the chosen witnesses and all
  F-neighbours of doubled active pairs. No inactive-pair owner is chosen.

The last choice always exists. Proper R-colouring forbids at most one
endpoint through its witness. H-distance at least three ensures at most one
active pair can demand an endpoint of this exterior R-pair. There cannot be
two F-edges from a single active pair to it, by the owner-C4 convention.
If a demand forbids x, the bonus rule ensures the other endpoint, its R-mate,
has colour different from c, so that other endpoint is available.

Witnesses are independent in A. Exterior witnesses of one colour are
independent in J; an inactive bad R-pair is an opposite pair in its auxiliary
square; and a bad J-component has no exterior A-edge. Every chosen witness
therefore has its helper as its only chosen neighbour, and no chosen owner.
Each helper has at most one chosen witness, by independence on P.

Outside owner C4s, a singly chosen R-pair contributes no induced R-edge and
at most one F-edge at each chosen owner. A doubled active pair has its R-edge
and no chosen F-neighbour. Inactive pairs supply no owners. Each owner C4
has exactly two chosen owners, one from each virtual R-pair; any two vertices
of C4 induce maximum degree at most one. Thus D_c is a dissociation set in
the original physical graph, using actual B edges throughout.

An exterior R-pair contributes two witnesses and three owners across the
three sets, total five. A bad component contributes six witnesses and four
owners, total ten for its two pairs. Helpers contribute 3b in total. Hence

    |D_0|+|D_1|+|D_2|=5b+3b=8b.                            (2)

At least one set has size ceil(8b/3). Its witness set may subsequently be
optimized in original A for the same owners using (1). No matching edge or
owner is independently credited to two simultaneous repairs.

The implementation uses an iterative feasibility search for exterior colouring,
with an explicit stack so its search depth has no Python recursion-limit cap;
no polynomial runtime bound for that supplied search is asserted. The binary
contact test itself is polynomial 2-SAT.

## 3. Pseudoforest corollary, including parallel contacts

If each connected component of the contact MULTIGRAPH on binary parts has
at most one cycle, the theorem applies. Indeed, every subgraph then has at
most as many edges as vertices. In the incidence bipartite graph between
contact edges and their endpoint parts, Hall's condition holds: a collection
of edges has at least as many incident parts. Assign each contact edge to a
different endpoint part. A part assigned an edge chooses its member not
incident with that edge; an unassigned part chooses arbitrarily. Every
contact is avoided by its owner part. Different contacts between the same
two parts must be retained as parallel edges for this count. Flattening them
would invalidate the sufficient condition.

## 4. A connected family with unavoidable many K4s and exact optimum

For every integer r>=2 take r copies of the following b=8 physical block.
Its physical colours are v mod2. B has the natural cycles (0,...,7) and
(8,...,15). Its matchings are

    P: 02,13,9-11,10-12,5-15,6-14,48,7-13
    Q: 03,12,9-12,10-11,5-14,6-15,4-13,78.

Here 02 denotes the edge {0,2}, and hyphens separate multi-digit indices.
The machine-readable [fixture](../develop/fixtures/k4-contact-base.json)
removes any ambiguity. The auxiliary squares are {0,1,2,3}, {9,10,11,12},
{5,6,14,15}, and {4,7,8,13}. In copy j add offset 16j. Replace each free
Q-edge {4_j,13_j} by {4_j,13_(j+1 mod r)}. The free squares merge into one
C_(4r); the three other squares in each block remain. Consequently

    A=3r C4 union C_(4r),   B=2r C8,   b=8r.                (3)

The graph on 40r actual vertices is connected and bipartite. Helpers have
degree two and witnesses/owners degree three. The swapped Q edges preserve
the physical opposite-colour condition, perfect Q, and simple edges.

On each block the two owner-C8 matching phases have the following complete
table of bad K4s (phase 0 starts at the least vertex in natural cycle order):

| Two phases | Bad auxiliary squares |
|---|---|
| 00 | {0,1,2,3} |
| 01 | {0,1,2,3}, {9,10,11,12} |
| 10 | {5,6,14,15} |
| 11 | {9,10,11,12} |

Every phase on the 2r owner cycles therefore has at least r bad components.
Taking phase 00 in every block gives exactly r bad components and no contacts
between them, so simultaneous repair applies at every scale. An explicit
exterior colouring is stored in the fixture and repeats across blocks: the
cross-copy Q-edge joins colours 0 at index4 and 2 at index13. The three
certificates have sizes 23r,22r,19r, summing to64r=8b.

In fact the exact optimum is

    tau=r,                 beta_I=23r.                     (4)

For its lower bound on tau delete the free Q-edge {4,13} in one block. The
local A is three squares and the path (4,8,7,13). Suppose a permitted U has
matching cost zero there, so it is independent. Enlarge its intersection on
each square to an opposite pair; this preserves independence and permission,
since adding omissions cannot increase retained owner degrees. Those choices
are {0,1} or {2,3}; {9,10} or {11,12}; and {5,6} or {14,15}.

If the third pair is {5,6}, owners14,15 are retained. The owner triples
(13,14,15) and (14,15,8) force omissions13,8. Independence on the path
then forbids omissions4,7. But the first square choice forces respectively
4 by (2,3,4), or 7 by (7,0,1), a contradiction.

If the third pair is {14,15}, owners5,6 are retained. The triples (4,5,6)
and (5,6,7) force omissions4,7, so path independence forbids8,13. The second
square choice forces respectively13 by (11,12,13), or8 by (8,9,10), again a
contradiction. Thus the local matching cost is at least one.

For any global permitted U its restriction to each block is permitted for
the local owner cycles. Choose a maximum local matching in each block with
the free edge deleted. These r matchings have disjoint vertices and their
union is one actual matching in global A[U]. Hence nu(A[U])>=r. This is a
single global lower count, not r charges against a shared edge.

For equality repeat the following physical certificate in every block:

    owners S0={0,1,5,6,8,11,12,15},
    witnesses T0={2,3,4,7,9,10,14},   all eight helpers.

Each selected owner has at most one selected owner neighbour; S0 and T0
are disjoint; T0 is independent on P and all local Q edges. A new cross edge
has endpoint4 selected and endpoint13 absent, so repetition remains valid.
Its size is 8+8+7=23 per block, proving (4). This is the exact optimum with
all helpers required; no exact unrestricted dissociation or star-forming
optimum is claimed.

For r>=4 this family lies beyond the named all-square/short-component,
all-owner-C4/6k, at-most-one-exceptional-owner-cycle, and at-most-one-K4 tests.
Its minimum omission size is6r; the earlier one-saving estimate3r-1 exceeds
floor(8r/3). This does not assert failure of every prior activated-support or
coordinated-exchange method. At r=2 the new unique-C8 class also applies;
the simultaneous repair theorem covers all r, including arbitrarily long
mixed components.

## 5. Criterion rejection is not a target obstruction

Take b=4, colours v mod2, B=(0,...,7),

    P: 04,15,26,37;       Q: 41,50,63,72.

The canonical R gives two bad squares and all four forbidden binary
contacts, so its contact 2-SAT instance is unsatisfiable. Nevertheless the
exact all-helper optimum is11=ceil(32/3). For example owners {1,3,4,6,7},
witnesses {2,5}, and all four helpers attain11. U={0,2,5} has the single
matching edge {0,5}. Thus rejection applies only to this sufficient rule.
The exact upper check is a finite control, not needed for the general theorem.

## 6. Implementation, checks and scope

[k4_contact_repair.py](../develop/k4_contact_repair.py) returns all three
actual certificates, the physical J/H model, contact paths, 2-SAT choices
or SCC contradiction paths, bonus colour lists, and optional pseudoforest
edge ownership. It validates the virtual owner-square convention. Odd-order
owner paths return a scoped rejection.

Run `python3 -B scripts/check_k4_contact_repair.py`. The independent checker
enumerates binary contact assignments, reconstructs physical adjacency and
all certificate degrees, checks matching/cover dual witnesses, compares exact
small optima, and tests the all-scale construction at r=2 through64. The
two-case proof, table, and explicit repeated certificate establish (4) at all
orders; finite computation is supplemental. Report and independent audit
are recorded separately. No Lean verification is claimed.

The universal mixed cyclic target, sharp unrestricted graph-gap coefficient,
general safe composition, physical multiple-Hall routing, unit-grid5/6 and
grid triple equality remain open. The simultaneous contact rule is a new
sufficient class within that active goal.
