# The sharp selected-star coefficient at minimum degree two and maximum degree at least six

All graphs are finite and simple. A two-star-forming set S forms every
outside vertex using two distinct selected vertices and a not necessarily
induced K_(1,2). The dissociation number beta_2 is the maximum cardinality
of a vertex set inducing maximum degree at most one. Minimality below
means inclusion-minimality. Put d=|S|-beta_2(G) and n=|V(G)|.

**Theorem.** For every integer Delta>=6, among bipartite graphs of minimum
degree at least2 and maximum degree at most Delta, with a specified
minimal forming set S inducing stars, single edges or isolates, the sharp
asymptotic gap coefficient is

    C_Delta=(Delta-1)/[12(Delta-1)+2].                    (1)

The universal upper statement d<=floor(C_Delta*n) is the preceding
[free-unused-vertex theorem](FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md).
Here we prove attainment by two-connected graphs at every order
n=[12(Delta-1)+2]k, k>=1. Their exact selected sizes and unrestricted
optima are

    p=Delta-1>=5,
    n=(12p+2)k, |S|=8pk, beta_2(G)=7pk, d=pk.           (2)

Thus the same sharp coefficient holds even after imposing two-connectivity.
This does not assert an exact SF_2 value, pointwise attainment at other
orders, a structure theorem for every maximizing minimal selection, or
sharpness at maximum degree2,...,5 or minimum degree at least3. These
nonregular graphs have vertices of degree at least6 and are not full grids.

The proof has three distinct parts: a general exact witness-interface
formula; computer-assisted integer caps for fixed bases of orders62 and74;
and written all-p, all-k composition arguments. The infinite conclusion
is not inferred from testing finitely many lifts or degree parameters.

## An exact interface formula with one unused vertex per wing

Take positive integers p_L,p_R. There are p_L six-vertex blocks in the
left wing and p_R in the right wing. Block j has vertices c,x,y,i,a,b
and edges

    cx,cy,xa,yb,ib.                                     (3)

Select c,x,y,i in every block. In each wing add a vertex u adjacent to
all its i vertices and to the y of one distinguished block, indexed0
within that wing. An arbitrary simple bipartite interface R joins the
a,b witnesses of one wing to those of the other wing. There are no other
edges. Orient the wings oppositely, so all edges respect bipartiteness.
The resulting order is6(p_L+p_R)+2 and |S|=4(p_L+p_R).

For every R this S is minimal forming. Each witness has an active selected
leaf, and each u has its distinguished active leaf. Deleting x makes a
fail; deleting y leaves b with only inactive i; deleting c leaves a with
only inactive x; deleting i makes i itself outside with no selected
neighbour. The interface edges have two original outside endpoints, so
none changes these literal deletion failures.

Consider arbitrary selected witness subsets A,B in a dissociation set Q.
They are admissible exactly when R[A union B] has maximum degree at most1.
For an admissible pair, assign each witness state0 if absent,1 if present
with no selected cross neighbour, and2 if present with one selected cross
neighbour. State2 spends its entire residual degree on that cross edge.
For each block let alpha,beta be its a,b states.

The following table counts only the four variable vertices c,x,y,i.
F is their maximum when u is absent. G is their maximum when u is present
and none of these four is adjacent to it; G_0 is the corresponding value
in the distinguished block. When u is present and exactly one chosen
local neighbour is allowed, the score is G+1 (or G_0+1) if beta=0;
that local option is impossible if beta is1 or2.

| alpha | beta | F | G | G_0 |
| --- | --- | --- | --- | --- |
|0|0|3|2|2|
|0|1|3|2|2|
|0|2|2|2|2|
|1|0|3|2|1|
|1|1|2|2|1|
|1|2|1|1|1|
|2|0|3|2|1|
|2|1|2|1|1|
|2|2|1|1|1|

For a direct verification, write c,x,y,i as bits. An included c requires
x+y<=1; an included x requires c+[alpha>0]<=1; an included y requires
c+[beta>0]+u[distinguished]<=1; and an included i requires[beta>0]+u<=1.
An included a additionally requires x+[alpha=2]<=1; an included b requires
y+i+[beta=2]<=1. These are precisely all physical induced-degree
constraints in a block. They give the nine rows above by choosing at
most16 local assignments. The used u-neighbour count is
u(i+[distinguished]y); all other selected neighbours of u lie in other
blocks. Here u in this expression is its0/1 selection bit.

Let w be the number of chosen witnesses in a wing, let F_sum be the sum
of its F entries, let G_sum sum G on ordinary blocks and G_0 on the
distinguished block, and let epsilon be1 if some block has beta=0 and0
otherwise. The exact optimum on that wing, with the witness states fixed,
is

    M=w+max(F_sum,1+G_sum+epsilon).                      (4)

Indeed, when u is absent, blocks are independent and give F_sum. When u
is present, its ONE degree capacity can be used in at most one block.
The table gives a possible gain of exactly one if and only if epsilon=1.
It cannot be added separately in several blocks. Every local table
maximum is attained, so these upper statements are simultaneous lower
constructions as well. The only cross-wing edges are the fixed witness
edges; their consumed capacities have already been marked by state2.
Therefore the exact unrestricted formula is

    beta_2(G_R)=max_(admissible A,B)(M_L+M_R).             (5)

This proves the formula for every positive wing size and every interface,
not just the two bases below. The implementation instead uses the
equivalent two-state DP recording0 or1 total used neighbour of u while
processing the blocks. The transition adds one local contribution and
rejects total use exceeding1. Induction over the processed blocks proves
that recurrence exactly; backtracking returns a physical optimum set.
There are at most2^[2(p_L+p_R)] witness subset pairs. A direct evaluation
uses O(p_L+p_R) local operations per pair, apart from graph/bit overhead.
No polynomial-in-width claim is made.

## Two fixed bases and their exact caps

Let q be5 or6. Use q blocks in each wing, labelled j=0,...,2q-1,
with c_j=6j,x_j=6j+1,y_j=6j+2,i_j=6j+3,a_j=6j+4,b_j=6j+5.
The two unused vertices have labels12q and12q+1. The distinguished
blocks are0 and q. Index the witnesses of each wing by t=0,...,2q-1,
with even t denoting a and odd t denoting b.

Join left witness t to right witnesses

    t,t+1,...,t+q-2 modulo2q,

and for even t also join it to right t+h, where h=4 at q=5 and h=6
at q=6. Thus a witnesses have q cross neighbours and b witnesses q-1;
parity makes the right degrees identical. Every witness has full degree
q+1 after its one or two selected neighbours are included. Each unused
vertex has degree q+1. Centres, ordinary leaves and isolates have degree2;
the two distinguished leaves have degree3. Hence the bases have exact
minimum degree2 and maximum degree q+1.

Call these bases B_q. Put e_q=b_0b_q, with physical labels(5,6q+5).
The fixed exact integer certificates establish

    beta_2(B_5)=beta_2(B_5-e_5)=35,
    beta_2(B_6)=beta_2(B_6-e_6)=42.                     (6)

The explicit lower set takes c,x,i in every left block and x,y,a,b in
every right block. It avoids both unused vertices, has size7q, and is
dissociation: left c-x and right x-a,y-b are matching edges, left i
vertices are isolated, and no cross-witness edge has both ends chosen.
It remains valid after deleting e_q.

For the upper certificate, apply the general formula(5) to the explicit
interface masks printed in the two coordinate fixtures. For each left
witness subset compute the maximum over every admissible right subset.
There are1024 left subsets at q=5 and4096 at q=6. The checker independently
enumerates all pairs of PHYSICAL witness subsets and evaluates the closed
table(4), comparing every row cap and every admissible-pair count with
the optimizer's pruned subset loop and two-state DP. The report retains
the full row-cap and count vectors and their hashes, not only a solver's
claimed optimum. Their largest entries are35 and42 respectively, both
before and after deletion. The local table and formula prove why these
finite integer certificates are upper bounds on unrestricted beta.

This is a computer-assisted part of the theorem: it certifies two fixed
labelled bases, not an infinite-family conclusion by sampled enumeration.
The written general formula justifies the complete search domain. The
written composition proofs below supply all other degrees and all k.
Deleting the different outside edge a_0a_q gives cap36 at q=5 and43 at
q=6; therefore outside endpoints alone do not establish the needed cap.

## Two-connectivity before the safe-edge composition

The witness interface of B_q-e_q contains the Hamiltonian cycle formed
by offsets2 and3: repeatedly use

    L_t -- R_(t+3) -- L_(t+1),

with indices modulo2q. It visits every witness once and returns to L_0.
These edges exist for both q, and none is the deleted offset0 edge.
Starting from this cycle, all other witness-interface edges can be added.
For every block add the ear a_j-x_j-c_j-y_j-b_j. In either wing, introduce
its unused vertex and two isolates through the ear
b_(j0)-i_(j0)-u-i_(j1)-b_(j1), using distinct j0,j1. Introduce each other
isolate through the ear b_j-i_j-u. Add the distinguished u-y edge last.
Each ear has distinct old endpoints and new internal vertices. After
any one vertex deletion its surviving path segments attach to surviving
endpoints, while the old graph remains connected. Thus ear addition
preserves two-connectivity. This proves B_q-e_q is two-connected for
both bases, independently of finite deletion tests.

## All maximum degrees from two bases and24-vertex modules

Let p>=5. Set q=5 if p is odd and q=6 if p is even, and put m=(p-q)/2.
Take B_q together with m extra pairs of wings, each containing two
six-vertex blocks per wing with complete K_(4,4) witness adjacency.
These24-vertex modules are G_(2,2) from the earlier selected-star proof.
Do not add new unused vertices. Instead join every newly added isolate
i in each wing to the SAME unused vertex u of that wing in B_q. No
new distinguished u-y edge is added. Call the result H_p.

For completeness a24-vertex module without u has beta14: a wing
partitions into four P3's and contributes at most8; a wing without
chosen witnesses contributes at most6 (two selected P3's plus isolates).
If both wings contain witnesses, completeness forces exactly one on each
side and bounds the total by7+7=14. If one side is empty, the bound is
8+6=14. Taking c,x,i on one side and x,y,a,b on the other attains14.
This local proof does not require enumerating these modules.

The two common unused vertices now have degree p+1. The initial witness
degrees are q+1<=p+1; new private witnesses have degree5 and new helped
witnesses degree6. Every selected vertex has degree2 except the two
distinguished leaves of degree3. Thus delta(H_p)=2 and Delta(H_p)=p+1.
Its order is12p+2 and its specified minimal set has size8p. Formation
and every literal deletion failure follow exactly as in(3); the common
u vertices still have their original active distinguished leaves.

Partition the vertex set into the initial B_q, including both u vertices,
and the m added24-vertex modules. The induced graphs on these parts are
precisely B_q and those modules; edges from a common u to a new isolate
cross the partition and can only restrict a dissociation set. Consequently
(6) and the module cap give beta(H_p)<=7q+14m=7p. The common explicit
maximizer avoids the two u vertices and attains7p in every part, proving

    beta(H_p)=7p, beta(H_p-e_q)=7p.                    (7)

The same argument proves the second equality by using B_q-e_q in the
first part. This is an exact restriction-and-attainment argument for
EVERY m, not repeated use of the same unused vertex as a free resource.

H_p-e_q is also two-connected. A new24-vertex module together with the
two common u vertices and their isolate edges is two-connected by the
same ear argument from K_(4,4); no distinguished u-y edge is needed.
Each such piece shares the two distinct vertices u_L,u_R with B_q-e_q.
The union of two-connected graphs sharing at least two vertices is
two-connected: after deleting any vertex, the pieces stay connected
and have at least one shared surviving vertex. Iterating proves the
claim for arbitrary m.

## Arbitrary scale at the same maximum degree

Take k disjoint copies of H_p. In each remove e_q=ab and add a in copy j
to b in copy(j+1 modulo k). For k=1 this restores the original edge.
For k>=2 the new edges join different copies and give no loops or
parallel edges. Each port loses and gains one edge, so all degrees and
the bipartition are preserved. All modified edges have two outside
endpoints, so selected adjacency, formation and EVERY single-deletion
failure remain unchanged, including failures at a newly omitted vertex.

Any dissociation set restricts to H_p-e_q in each copy and is bounded
by7p there. Repeating the explicit7p-set in each copy attains7pk: it
uses no left witness and every right witness, so no new cross-copy
edge has both endpoints selected. This proves the exact unrestricted
beta in(2). There is no repeated assignment of a port or actual edge.

Each H_p-e_q is two-connected. The cross-copy links form a cycle of
pieces with distinct entry and exit ports. Deleting any one vertex
keeps every piece connected and removes at most one link of that cycle.
The surviving links still connect all pieces; for k=2 there are two
links at distinct ports and one survives. Hence the whole graph remains
connected after any single deletion. The k=1 case was proved above.

Finally p=Delta-1 makes the gap/order ratio in(2) equal to(1). This proves
sharpness for every integer Delta>=6, including under two-connectivity.
It does not assert that all minimal forming sets have selected-star
components, and it does not turn a selected gap into an exact SF value.

## Reproduction and verification scope

Run `python3 -B scripts/check_sharp_minimum_two_degree.py`. The optimizer
and checker use only the standard library. Both coordinate fixtures,
full fixed-base row certificates and the finite report are included.
The general proof above supplies all-interface, all-p and all-k claims.
The local/whole-wing literal controls and independent physical-boundary
scores test the implementation, without substituting finite samples for
those general implications. The local checker passes556 interface graphs with2,819,008 independent
one-part subsets,59,049 complete ternary wing states, and four exact base
caps35,35,42,42. It also checks29 physical all-degree/lift models with
15,824 literal deletion failures and3,312 single-vertex deletions; larger
connectivity statements use the written proof. Direct exact controls on
the shared-u extensions p=7,8 and their safe-edge deletions give49,49,56,56.
These ranges are listed separately in the report. Final independent
exact-source and original-checker execution review is pending.
