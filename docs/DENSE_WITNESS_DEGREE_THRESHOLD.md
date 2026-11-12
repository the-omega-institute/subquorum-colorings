# The equality threshold at every minimum degree at least four

**Theorem.** For every integer p>=3 and k>=1 there is a finite simple
two-connected bipartite graph G with a specified inclusion-minimal
two-star-forming set S inducing only P_3's and isolates, such that

    n=14pk, |S|=8pk, beta_2(G)=7pk,
    delta(G)=p+1, Delta(G)=4p-3.

Formation uses a not necessarily induced K_(1,2); beta_2 is the unrestricted
dissociation number. Thus for EVERY delta>=4 the selected gap attains

    Delta=4delta-7, d=|S|-beta_2(G)=n/14
         =Delta*n/(12Delta+8delta-14).                (1)

The general upper bound for specified minimal selections inducing stars,
edges or isolates therefore has sharp coefficient at its necessary degree
threshold for every delta>=4, even with two-connectivity and at all cyclic
scales. The new small parameters are (delta,Delta)=(4,9),(5,13).
The preceding balanced-omission theorem already treats the threshold for
delta>=6, as well as other degree parameters. The present dense construction
has a separate proof and audit; it is not that previously reviewed graph.

## Construction

There are p left and p right blocks c,x,y,i,a,b, with local path
 a-x-c-y-b-i. The two wings have opposite bipartite orientations. Select
c,x,y,i in every block, and add ALL edges between the 2p witnesses a,b
of the left wing and the 2p witnesses of the right wing.

Add p connectors A_s on the left-centre colour and p connectors B_s on
the right-centre colour, s modulo p. In block j of either wing:

- i meets all connectors of its own wing;
- x meets all of those except index 3j;
- y meets all of those except index 3j+1;
- c meets all opposite-wing connectors except index 3j+2.

Call this F. Set e=b_0^L b_0^R and F^-=F-e. Every c,x,y,i has degree
p+1. Every a has degree 2p+1, every b degree 2p+2 in F, and each connector
has degree 4p-3: the 3p omissions distribute equally over p indices.
The two ports in F^- have degree 2p+1. For p>=3,

    p+1 <= 2p+1 <= 2p+2 <= 4p-3.

Thus BOTH F and F^- have exact minimum p+1 and maximum 4p-3.
As before, x and y omit different connectors in every block, so each
connector has at least p active selected leaf neighbours. Every outside
vertex is formed. Deleting x,y,c,i from S makes a,b,a,i, respectively,
fail the literal formation test. All connector and cross-witness edges
have outside endpoints, so they preserve those failures. Consequently
S is inclusion-minimal, with |S|=8p.

## Kernel facts, including the p=3 boundary

For a dissociation set D, a witness is cross-saturated if it has a chosen
opposite-wing witness neighbour. A block is good if it has a chosen witness
and its b is not cross-saturated, counting an absent b as not saturated.
Let o,g,f count occupied, good, and full cross-free blocks in a wing.
A full cross-free block has both witnesses chosen and neither saturated.

All witness relations below survive deletion of e. In particular none
uses a diagonal b_j^L b_j^R edge. Slots (L_j,R_(j+1)), j modulo p,
are complete K_(2,2)'s, giving at most 2p chosen witnesses total.
Double-good slots have just the two a-witnesses chosen and cross-saturated;
they force every witness of the predecessor slot absent. The same argument
with a chosen-a indicator on one side gives

    g_L+g_R<=p, a_L+g_R<=p, g_L+a_R<=p.               (2)

The predecessor map is injective: a_j^L excludes R_j, and a_(j+1)^R
excludes L_(j-1). These are surviving a-incident edges. Each block has
at most 3+[good] chosen vertices. With no chosen connector, (2) therefore
gives |D|<=7p.

We also need the one-connector bound when that connector meets every i
and some y in its wing. Retain only these i-edges and one such y-edge.
With the chosen connector included, its wing satisfies

    size<=2p+2+o+f, and size<=4p.                    (3)

For the first bound, ignoring i each local a-x-c-y-b path contributes at
most 2+[occupied]+[full cross-free]; there is at most one chosen i over
the whole wing, plus the connector. For the second, partition the
special block and connector into P_3={a,x,c} and C_4={y,b,i,connector},
each with dissociation number 2. Each other P_6 contributes at most 4.

Let r be the number of good blocks in the other wing, whose contribution
is at most 3p+r. If r=0, (3) gives the total cap 7p. If 0<r<p, then
o<=p-1: if every block of the connector wing were occupied, a good a
on the other side would have neighbours in two distinct such blocks,
and a good b would have a cross neighbour. Moreover
f<=p-r-1: a good opposite block at k excludes two consecutive positions
from being full cross-free, and a nonempty proper cyclic subset expands
by at least one when united with its shift. Now (3) gives at most 4p-r
in the connector wing, hence total 7p.

If r=p, f=0 and o<=p-2. Indeed one unique empty block would allow good
opposite blocks at only two indices. Since p>=3, two indices cannot
cover all p. Formula (3) then gives 3p in the connector wing and 4p
in the other. In the left-connector orientation the two excluded positions
are L_k,L_(k-1), and the possible indices from a unique empty L_h are
h+1,h+2. In the right-connector orientation the two excluded positions
are R_(j+1),R_(j+2), and a unique empty R_h allows only h,h-1. Thus
both orientations, including p=3, are covered. Arbitrary distinguished
y follows by simultaneous cyclic rotation of this fixed kernel; it omits
all diagonal b--b edges, so changing the index never moves a needed
edge onto the physical deletion.

If a sole chosen connector meets no y in its wing, it meets every x and
i there. Remove its at most one chosen neighbour. The remaining wing
has block contribution at most 2+[a chosen], and the other at most 3+[good].
Equation (2) gives 6p remaining vertices; restoring the neighbour and
connector gives 6p+2<=7p. At p=3 this is the relevant no-y exception.

These facts establish the cases of zero or one chosen connector without
using the earlier theorem's p>=5 range. Only the explicitly surviving
kernel relations and p>2 are needed here.

## Shared capacities for at least two chosen connectors

Write q_A,q_B for chosen connector counts, m=q_A+q_B. Every chosen
connector has at most ONE chosen neighbour over its whole neighbourhood.
Removed vertices below are unions, and are restored once each.

If at least three chosen connectors share a colour, say A, every left
x,y,i and every right c has at least two chosen A neighbours and is absent
outright. If q_B=0 this gives at most 4p selected block types, 2p witnesses,
and m<=p connectors, hence |D|<=7p. If q_B>0, remove the at most one
chosen neighbour of one B. Only p left centres and at most p right leaves
can remain among selected block types. Restore one vertex and all
m<=2p connectors to obtain |D|<=4p+1+m<=6p+1<=7p.

Assume now both q_A,q_B<=2. Four chosen connectors must have two of each
colour. Removing their at most four chosen neighbours eliminates every
selected block type, leaving at most 2p witnesses. Restoration gives
|D|<=2p+8<=7p, using p>=3.

For three connectors the pattern is two of one colour and one of the
other. With two A's and one B, remove their at most three chosen neighbours.
The A-pair excludes left x,y,i and right c. The B excludes right i and
at least one right leaf per block. Thus at most 2p selected block types
and 2p witnesses remain. Restoration gives |D|<=4p+6<=7p for p>=3.
Reverse wings for two B's and one A.

For two connectors and p>=4, the previous pair bounds suffice. Opposite
colours exclude every i and one leaf per block after removal of at most
two neighbours, leaving at most 6p block vertices. Two of one colour
exclude its wing's x,y,i and the opposite centres, leaving at most 4p
selected block types plus 2p witnesses. Both bounds give
|D|<=6p+4<=7p.

It remains to prove the two-connector case at p=3.

**One of each colour.** The omissions in every block are the constants
0 for x, 1 for y, and 2 for c. If A_s and B_r are chosen, remove their
at most two chosen neighbours. All i are absent. The surviving selected
types in the left wing number at most

    p([r=2]+[s=0]+[s=1]),

and in the right wing at most p([s=2]+[r=0]+[r=1]). Their sum is 2p.
Together with at most 2p witnesses, restoring two neighbours and two
connectors gives |D|<=4p+4<=7p.

**Two of the same colour.** Say two A's. Remove their at most two chosen
neighbours. The generic bound is 6p+4=22, whereas 7p=21. If |D|>21,
every step of the integer bound must be equality: exactly two neighbours
were removed; every left c and every right x,y,i is present afterwards;
and there are exactly 2p chosen witnesses.

Every right b is then absent because its chosen y and i give two
neighbours. A chosen right a already meets its chosen x and so cannot
meet a chosen left witness. Since every right a is adjacent to every
left witness, its presence would force all left witnesses absent,
leaving at most p witnesses in total. This contradicts the required 2p.
Thus no right witness is chosen and all 2p left witnesses are chosen.

No removed A-neighbour can now be restored: a left x or y would have
both its centre and its witness owner as chosen neighbours; a left i
has both chosen A's as neighbours; a right c has its chosen x and y.
Those are all possible neighbours of an A. This contradicts the required
two restored vertices. Therefore |D|<=21. The two-B case reverses wings;
right a's and left a's are equally universal in F^-.

This proves |D|<=7p for every p>=3. Taking c,x,i in every left block
and x,y,a,b in every right block, with no connector, attains 7p in F
and F^-: its only edges are left cx and right xa,yb. Hence

    beta_2(F)=beta_2(F^-)=7p.                         (4)

No finite optimized value is used in this proof.

## Two-connectivity and every cyclic scale

The witness offsets 2 and 3 give a Hamiltonian cycle avoiding e, by
following left s, right s+3, left s+1 modulo 2p. Both offsets are present
in the dense interface. Attach every a-x-c-y-b path as an open ear.
Each connector has at least p>=3 old leaf neighbours, so can be added
with at least two old neighbours. Each i then has its b and all p
connectors as old neighbours. This constructs a two-connected spanning
subgraph of F^-.

Take k copies of F^- and join each left port b_0^L to the next right
port b_0^R cyclically. At k=1 this restores e. At k>=2, deleting any
vertex keeps each affected piece connected and destroys at most one
link, as its two ports are distinct. The cycle of pieces remains
connected, including at k=2 where one of the two links survives.
Port degrees are restored and literal minimality witnesses persist.
Restricting a dissociation set to each piece gives at most 7pk by (4).
The repeated attaining set omits every left port, so no new edge has
both ends chosen; it attains 7pk. Finally 8delta-14=2(4p-3)=2Delta,
which gives (1).

## Verification scope

Run `python3 -B scripts/check_dense_threshold_degree_family.py`.
The physical models check exact degrees, bipartition, formation, every
literal deletion witness, the attaining set and every vertex deletion
for two-connectivity. An independent exact graph recursion additionally
checks p=3,4 full and deleted bases. At a vertex v that recursion exhausts
three possibilities: v absent; v present with no chosen neighbour;
v paired to a chosen neighbour u. The corresponding residuals remove
v, N[v], or N[v] union N[u]. Component splitting is exact. These four
finite computations support (4); its proof is the all-p argument above.
The theorem does not assert an exact SF_2 value or regular sharpness.
The threshold at delta=3 is separate; neither the smaller model nor its
safe-deletion condition is assumed here.

The independent exact-source audit returned **ACCEPT**, reconstructing all
nine manifest files and running the original checker unchanged with
assertions enabled. It reproduced the complete 10,746-byte report
byte-for-byte (SHA-256
8b55484abc9a8c88a8601002dc2c8c06134bdd904e2bf52cc189a0b41b3332b1),
with exit status 0 and empty startup-through-exit stderr. Physical controls
cover 24 models, 1,904 literal deletion failures and 3,332 vertex deletions;
four independent exact graph recursions visit 111,657 states in total.
The all-p cap is the general proof, not those four computed optima.
`../output/dense-threshold-degree-review.json` preserves both complete
responses, manifests and actual execution scope. Only this evidence
paragraph was added after the reviewed source freeze.
