# The sharp selected-star coefficient at minimum degree two and every maximum degree at least six

All graphs are finite and simple. A two-star-forming set S forms every
outside vertex using two distinct selected vertices and a not necessarily
induced K_(1,2). Beta_2(G) is the unrestricted dissociation number, the
maximum cardinality of a set inducing maximum degree at most one.
Minimality means inclusion-minimality. Put d=|S|-beta_2(G), n=|V(G)|.

**Theorem.** For every integer Delta>=6, among bipartite graphs of minimum
degree at least2 and maximum degree at most Delta, with a specified
minimal forming set S inducing stars, single edges or isolates, the sharp
asymptotic gap coefficient is

    C_Delta=(Delta-1)/[12(Delta-1)+2].                    (1)

The universal bound d<=floor(C_Delta*n) is the preceding
[free-unused-vertex theorem](FREE_UNUSED_VERTICES_AND_DEGREE_REFINEMENT.md).
For each p=Delta-1>=5 and k>=1, the explicit two-connected family below
attains it, with

    n=(12p+2)k, |S|=8pk, beta_2(G)=7pk, d=pk.           (2)

Both the all-p exact cap and the all-k composition have complete
combinatorial proofs. Finite computations verify the implementation;
no enumerated base cap is an assumption of this theorem.
This is not an exact SF_2 value or pointwise attainment at other orders.
No structure theorem for every maximizing minimal selection, sharpness
at maximum degree<=5 or minimum degree>=3, regular theorem or grid theorem
is claimed. The family is nonregular and has vertices of degree>=6.

## A single explicit construction for every p>=5

The base H_p has blocks j=0,...,2p-1. Write

    c_j=6j, x_j=6j+1, y_j=6j+2, i_j=6j+3,
    a_j=6j+4, b_j=6j+5,

and add c_jx_j,c_jy_j,x_ja_j,y_jb_j,i_jb_j. The left wing comprises
blocks0,...,p-1 and the right wing blocks p,...,2p-1. Reindex each wing
by j in Z/pZ and write L_j,R_j for its block positions. In each wing,
witness index t=2j denotes a_j and t=2j+1 denotes b_j.

Join left witness t to right witnesses t,t+1,...,t+p-2 modulo2p.
For even t also join it to right witness t+h, where

    h=p-1 if p is odd, and h=p if p is even.             (3)

This extra offset is even and outside0,...,p-2, so it adds one new edge
from every a-witness to an a-witness. Add u_L=12p adjacent to every left
i and to y_0; add u_R=12p+1 adjacent to every right i and to y_p.
Let S consist of c,x,y,i in every block, so |S|=8p and H_p[S] consists
of2p copies of P3 and2p isolates.

Centres, ordinary leaves and isolates have degree2. The two distinguished
y vertices have degree3. Each u has degree p+1. A-witnesses have p cross
neighbours and one selected neighbour; b-witnesses have p-1 cross
neighbours and two selected neighbours. The right cross degrees agree:
the baseline has degree p-1, and the extra even-offset matching adds one
edge exactly at the right a-witnesses. Hence delta(H_p)=2,Delta(H_p)=p+1.
Orient the wings oppositely, with c,a,b,u of a wing in one colour and
x,y,i in the other. Every edge respects the resulting bipartition.

Every outside witness has an active selected leaf, and each u has its
distinguished active leaf, so S is forming. Deleting x_j makes a_j fail;
deleting y_j leaves b_j with only the inactive isolate i_j; deleting c_j
leaves a_j with only inactive x_j; deleting i_j makes i_j itself outside
with no selected neighbour. These are literal one-deletion failures,
which prove inclusion-minimality because formation is upward closed.
All later changes have two originally outside endpoints and preserve them.

Set e=b_0^L b_0^R, with physical labels(5,6p+5), and put H_p^-=H_p-e.
We prove beta_2(H_p^-)=beta_2(H_p)=7p without finite enumeration.

## Witness relations that survive deletion of e

For every p>=5, the following relations hold in H_p^-:

- a_j^L meets both witnesses of R_j and both of R_(j+1), and meets
  a_(j+2)^R. The last edge has offset4; at p=5 it is the extra edge,
  while at p>=6 it belongs to the baseline.
- b_j^L meets both witnesses of R_(j+1), and meets a_(j+2)^R.
- Consequently L_j and R_(j+1) have complete K_(2,2) witness adjacency.
- a_k^R meets both witnesses of L_(k-1) and of L_(k-2), while b_k^R
  meets both witnesses of L_(k-1).

Every displayed edge survives: the only deleted edge is b_0^L b_0^R,
which has offset0. Additional witness edges only restrict dissociation.

Fix an arbitrary dissociation set D of H_p^-. A chosen witness is
cross-saturated when it has a chosen witness neighbour in the opposite
wing. Such a witness has no other chosen neighbour. Call a block occupied
if at least one witness is chosen; good if occupied and its b-witness
is not cross-saturated; and full cross-free if both witnesses are chosen
and neither is cross-saturated. Let o_T,g_T,f_T count these types in wing T.
An absent b is not cross-saturated, so a block containing only a is good,
even when a itself is cross-saturated.

## Three local bounds, with one capacity for each u

Each six-vertex block contributes at most3 plus its good indicator.
If neither witness is chosen, x,c,y contribute at most2 and i at most1.
If b is cross-saturated, neither y nor i can be chosen; a,x,c form a
P3 and contribute at most2, together with b at most3. In all other
occupied blocks, partition the path a-x-c-y-b-i into two P3's to get4.
Thus when u_T is absent,

    |D intersect V_T|<=3p+g_T.                           (4)

If u_T is chosen, at most ONE of all p isolates i in that wing is chosen.
Ignoring i, the path a-x-c-y-b contributes at most

    2+[occupied]+[full cross-free].                      (5)

With neither witness chosen it is at most2. With one chosen it is at
most3. With both chosen and either cross-saturated, its adjacent x or y
is excluded and the contribution is at most3. With both cross-free it
is at most4. Adding u_T and at most one isolate to the sum of(5) gives

    |D intersect V_T|<=2p+2+o_T+f_T  if u_T is chosen.    (6)

The u-to-distinguished-y edge can only strengthen this upper bound.
Its one total neighbour capacity has not been assigned once per block.

Finally every entire wing, including its u, contributes at most4p.
Partition the distinguished block and u into P3={a,x,c} and
C4={y,b,i,u}, each of dissociation number2. Each other block is a P6
of dissociation number4. Therefore

    |D intersect V_T|<=4p.                              (7)

## Neither unused vertex is chosen

Partition the2p block positions into slots P_j=(L_j,R_(j+1)). If both
blocks in a slot are good, complete K_(2,2) adjacency implies that neither
contains a chosen b: any such b would have a chosen cross neighbour and
would not be good. Their chosen witnesses are exactly a_j^L,a_(j+1)^R,
which are adjacent and hence both cross-saturated. The witness relations
then force every witness in R_j and in L_(j-1) to be absent. Thus the
preceding slot P_(j-1) is empty of chosen witnesses, in particular of
good blocks. The predecessor map is injective. If d_2,d_0 count double-good
and empty-of-good slots, then d_2<=d_0 and

    g_L+g_R=p+d_2-d_0<=p.

Applying(4) to both wings proves |D|<=7p.

## Both unused vertices are chosen

For every slot P_j, the sum of occupied and full-cross-free indicators
of its two blocks is at most2. If only one block is occupied it contributes
at most2. If both are occupied, complete adjacency makes every chosen
witness cross-saturated, so neither block is full cross-free and the sum
is exactly2. Consequently o_L+o_R+f_L+f_R<=2p. By(6),

    |D|<=4p+4+2p=6p+4<=7p,

where the last inequality follows from p>=5.

## Exactly one unused vertex is chosen: both orientations

First let u_L be chosen and u_R absent. Let J be the indices of good
right blocks and r=|J|. Equation(4) bounds the right wing by3p+r.
We prove the left wing contributes at most4p-r.

If r=0, use(7). If 1<=r<=p-1, then o_L<=p-1. Indeed, if all left blocks
were occupied, a chosen a_k^R would meet a chosen witness in each of
the distinct blocks L_(k-1),L_(k-2), violating degree1. A chosen b_k^R
in a good block would meet a chosen witness in L_(k-1), contradicting
its cross-isolation. A good right block would therefore be impossible.

Any chosen witness in R_k excludes both L_k and L_(k-1) from being full
cross-free: a_k^L meets both witnesses of R_k, and L_(k-1),R_k are completely
joined. Hence

    f_L<=p-|J union(J-1)|<=p-r-1.

The last step uses only that J is a nonempty proper subset of the cyclic
index set. Equality |J union(J-1)|=|J| would imply invariance under one
cyclic shift, forcing J to be empty or the whole cycle. Combining with(6),

    |D intersect V_L|<=2p+2+(p-1)+(p-r-1)=4p-r.

If r=p, then f_L=0 and o_L<=p-2. We have excluded o_L=p. If o_L=p-1,
let L_h be its unique empty block. A good R_k containing a_k^R requires
an empty block among L_(k-1),L_(k-2), so k is h+1 or h+2. A good R_k
containing b_k^R requires L_(k-1) empty, so k=h+1. Thus all good right
indices would lie in a set of size2, contradicting r=p>=5. Equation(6)
now gives |D intersect V_L|<=2p+2+(p-2)=3p=4p-r. In every case the total
is at most(3p+r)+(4p-r)=7p.

For u_R chosen and u_L absent, the needed index relations are explicit:
a_j^L meets both witnesses in R_j and R_(j+1); b_j^L meets both in R_(j+1);
and any chosen witness in L_j excludes full cross-free blocks R_(j+1)
and R_(j+2). The last exclusion uses a_(j+2)^R, which meets both witnesses
of L_j. If J indexes good left blocks, the same proof gives o_R<=p-1
and f_R<=p-|(J+1) union(J+2)|<=p-r-1 for 1<=r<=p-1. When r=p, a unique
empty right block R_h would permit good left indices only h,h-1, again
impossible. Thus o_R<=p-2,f_R=0. The r=0 case uses(7). This proves the
same total bound in the second orientation; no graph symmetry is assumed.

## Exact cap, two-connectivity and arbitrary scale

The three cases prove beta_2(H_p^-)<=7p for every p>=5. For attainment,
take c,x,i in every left block and x,y,a,b in every right block, and
neither u. This7p-set consists only of left c-x pairs, isolated left i's,
and right x-a,y-b pairs. No cross-witness edge has both ends chosen.
It is dissociation in both H_p and H_p^-. Since adding edges cannot
increase beta,

    7p<=beta_2(H_p)<=beta_2(H_p^-)<=7p.                  (8)

The witness edges of offsets2 and3 form a Hamiltonian cycle: follow
L_t--R_(t+3)--L_(t+1) with witness indices modulo2p. It visits all4p
witnesses, and none of its edges is e. Start from this cycle and add
all other witness edges of H_p^-. Add ears a_j-x_j-c_j-y_j-b_j. In each wing
add b_(j0)-i_(j0)-u-i_(j1)-b_(j1) for two distinct indices, then ears
b_j-i_j-u for its remaining isolates, and finally its u-y edge. Each
ear has distinct old endpoints and new internal vertices. After any
one deletion its surviving segments attach to a surviving endpoint,
while the old graph remains connected. This proves H_p^- is two-connected.

Take k disjoint copies of H_p^-. Add a in copy j to b in copy(j+1 modulo k),
where a=b_0^L,b=b_0^R. At k=1 this restores e. At k>=2 the new edges are
simple cross-copy edges. Every port loses and gains one edge, preserving
all degrees and the bipartition. All changed edges have two originally
outside endpoints, preserving selected adjacency and every one-deletion
failure, including at a newly omitted selected vertex.

Any dissociation set restricts to at most7p in each copy by(8). Repeating
the displayed7p-set attains7pk: it omits every left port, so no new edge
has both ends chosen. This proves the exact unrestricted beta in(2).
Each base remains connected after any one deletion. Distinct entry and
exit ports imply a deletion destroys at most one link of the cycle of
bases, whose surviving links still connect all pieces. At k=2 there
are two links at distinct ports and one survives; k=1 follows from the
base. Therefore the family is two-connected for every k>=1.

Finally p=Delta-1 gives the ratio(1), proving sharpness for every
integer Delta>=6, even under two-connectivity. The proof has no finite
base-cap premise and makes no exact SF_2 claim.

## An exact interface formula with one unused vertex per wing

Take positive integers p_L,p_R. There are p_L six-vertex blocks in the
left wing and p_R in the right wing. Block j has vertices c,x,y,i,a,b
and edges

    cx,cy,xa,yb,ib.                                     (I1)

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

    M=w+max(F_sum,1+G_sum+epsilon).                      (I2)

Indeed, when u is absent, blocks are independent and give F_sum. When u
is present, its ONE degree capacity can be used in at most one block.
The table gives a possible gain of exactly one if and only if epsilon=1.
It cannot be added separately in several blocks. Every local table
maximum is attained, so these upper statements are simultaneous lower
constructions as well. The only cross-wing edges are the fixed witness
edges; their consumed capacities have already been marked by state2.
Therefore the exact unrestricted formula is

    beta_2(G_R)=max_(admissible A,B)(M_L+M_R).             (I3)

This proves the formula for every positive wing size and every interface,
not just the two bases below. The implementation instead uses the
equivalent two-state DP recording0 or1 total used neighbour of u while
processing the blocks. The transition adds one local contribution and
rejects total use exceeding1. Induction over the processed blocks proves
that recurrence exactly; backtracking returns a physical optimum set.
There are at most2^[2(p_L+p_R)] witness subset pairs. A direct evaluation
uses O(p_L+p_R) local operations per pair, apart from graph/bit overhead.
No polynomial-in-width claim is made.

## Verification and provenance

The exact-interface formula above is a separate general result and
verification tool; the sharpness proof does not depend on evaluating it.
Run `python3 -B scripts/check_sharp_minimum_two_degree.py`. Literal local
stars, independent one-part optima on556 interface graphs, every59049
p5 ternary wing state, physical boundary scores at p5,p6, and29 physical
all-degree/lift models check the implementation. The report separates
finite verification from the all-p and all-k combinatorial proofs.

An independent research response supplied the p5 good-slot argument.
The all-p witness relations, both orientation cases and the single
closed-form construction above are its explicitly written generalization.
The preceding source snapshot used two fixed base certificates and a
parity/common-vertex composition. That argument remains a valid earlier
route, with its exact source and ongoing original review preserved.
The present direct proof removes those computational premises. The
revised source has its own independent proof/execution review, pending.
No Lean, priority, authorship commitment or manuscript submission is implied.
