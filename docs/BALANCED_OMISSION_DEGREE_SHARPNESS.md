# Balanced omissions attain the degree threshold

Let beta_2(G) be the maximum size of a vertex set inducing maximum degree
at most one. A two-star-forming set S means that every vertex outside S
belongs to a not necessarily induced K_(1,2) with two vertices of S.
Minimality is by inclusion. This note concerns a specified such minimal
S whose induced components are P_3's and isolates; it does not assert
that S maximizes all minimal forming sets or determine SF_2(G).

**Theorem.** For all integers

    t>=2, p>=max(t,5), t divides 3p, k>=1,

there is a finite simple two-connected bipartite graph G, with a specified
minimal two-star-forming S inducing P_3's and isolates, such that

    n=(12p+2t)k, |S|=8pk, beta_2(G)=7pk,
    minimum degree delta=t+1, maximum degree Delta=(4t-3)p/t.

The selected gap d=|S|-beta_2(G)=pk attains

    d = Delta*n/(12Delta+8delta-14).                  (1)

Consequently the coefficient of the general selected-star/edge/isolate
upper bound in COMBINED_CENTRE_LEAF_DEGREE_BOUNDS.md is sharp at these
min/max degree parameters, even with two-connectivity. In particular,
for every delta>=6 and all k>=1, t=p=delta-1 gives

    Delta=4delta-7, n=14(delta-1)k,
    |S|=8(delta-1)k, beta_2(G)=7(delta-1)k=n/2,
    d=n/14.                                         (2)

Thus the necessary threshold Delta>=4delta-7 for positive equality in
that upper bound is attained for every delta>=6. This does not claim
regular sharpness: delta and Delta are different here.

## Construction and physical degrees

Use the witness interface of SHARP_MINIMUM_TWO_DEGREE_BOUND.md. There are
p left and p right six-vertex blocks with local path a-x-c-y-b-i. Left
and right blocks have opposite bipartite orientations. Select c,x,y,i
in each block. Index a_j,b_j by 2j,2j+1 in each wing, j modulo p.
A left witness with index s meets right indices s,...,s+p-2 modulo 2p;
if s is even, also add index s+h, where h=p-1 for odd p and h=p for even p.

Add t vertices A_0,...,A_(t-1) on the colour of the left centres and t
vertices B_0,...,B_(t-1) on the colour of the right centres. In block j:

- left i meets every A; left x meets all A except A_(3j); left y meets
  all A except A_(3j+1); left c meets all B except B_(3j+2);
- right i meets every B; right x meets all B except B_(3j); right y
  meets all B except B_(3j+1); right c meets all A except A_(3j+2).

Connector indices are modulo t. No other connector edges are added.
Call this full base F. Let e=b_0^L b_0^R, and F^-=F-e. The construction
is simple and bipartite. The selected subgraph is exactly 2p P_3's and
2p isolates.

Each c,x,y has degree 2+t-1=t+1; each i has degree 1+t=t+1.
Every witness has degree p+1 in F, and only the two ports have degree p
in F^-. For a fixed connector, its omitted neighbours among x,y and
opposite c have residues 0,...,3p-1 modulo t, each occurring 3p/t times.
Its degree is therefore 4p-3p/t=Delta. Since p>=t>=2, Delta>=t+1 and
p+1>=t+1. Thus F has the stated exact minimum and maximum degrees.
The completed cyclic lifts below restore the port degrees p+1.

At p=t the local deleted piece F^- has minimum degree t=delta-1;
we do not impose a minimum-degree claim on that piece. It is used for
its dissociation cap and two-connectivity. If p>t, it has minimum delta.

Each connector has at least p active selected leaf neighbours: in each
block x and y omit different indices, so it meets at least one of them.
Thus connectors are formed. Every witness is formed through its selected
leaf owner, e.g. a-x-c. Deleting x,y,c makes respectively a,b,a fail to
be formed; deleting i makes i itself fail, since all its neighbours are
outside S. Added edges have outside endpoints and do not change these
literal failures. Hence S is forming and inclusion-minimal in F,F^- and
the completed lifts, with |S|=8p per piece.

## Witness facts used in the dissociation cap

The following facts are proved in SHARP_MINIMUM_TWO_DEGREE_BOUND.md and
SHARP_MINIMUM_THREE_SUBFAMILY.md. We spell out their relevant hypotheses.
The kernel facts used here hold for p>=5 after removal of e, and depend only on a fixed surviving
witness kernel, which excludes EVERY offset-zero b--b edge.

Partition witnesses into cyclic slots (L_j,R_(j+1)); each slot is a K_(2,2).
For any dissociation set there are at most two chosen witnesses per slot,
hence at most 2p overall. A block is good if at least one of its witnesses
is chosen and its b is not cross-saturated (an absent b is not
cross-saturated). A witness is cross-saturated when it has a chosen
opposite-wing witness neighbour.

With no chosen connector, each block contributes at most 3 plus its good
indicator. Double-good slots force their predecessor slots empty of good
blocks. Thus g_L+g_R<=p, and the whole graph without connectors contributes
at most 7p.

If one connector is chosen, meets every i of its wing and some y_j there,
then the same cap 7p holds. This is the single-u cap with distinguished
block j: retain only its edges to all i and that y_j. Both orientations
were proved explicitly in the earlier note. Simultaneous cyclic shifts
of block indices preserve the witness kernel. The kernel, unlike a
single-deleted-edge graph under such shifts, excludes all offset-zero
b--b edges, so the deletion stays harmless for any distinguished j.

One additional fact is needed if a chosen connector meets no y in its
wing. After excluding x and i in that wing, its block contribution is
at most 2+[a chosen], since the remaining vertices are isolated a and
path c-y-b. In the other wing the contribution is at most 3p+g. If a_L
is the number of chosen left a-witnesses, then a_L+g_R<=p; also
 g_L+a_R<=p. To see either inequality, a slot counted twice must have
just the two a-witnesses chosen. They are cross-saturated and exclude
both witnesses in the predecessor slot, so double slots inject into
zero slots. For example a_j^L excludes R_j, and a_(j+1)^R excludes
L_(j-1). These edges are in the fixed kernel. Hence the bound is 6p
after x and i of one wing have been excluded, in either orientation.

## One physical neighbour budget per connector

Fix an arbitrary dissociation set D of F^-, and let q_A,q_B be its
numbers of chosen connectors of each colour, m=q_A+q_B. Each chosen
connector has at most ONE neighbour in D over its ENTIRE neighbourhood.
Any removal below is a union of physical vertices; a common neighbour
is removed once. No connector supplies a separate capacity to each block.

**m=0.** The no-connector cap just given yields |D|<=7p.

**m=1.** Suppose the chosen connector is A_s. If it meets a left y,
the distinguished-y cap yields |D|<=7p. If it meets no left y, then
every left y omits s. Because the x and y omissions differ in each
block, A_s meets every left x, as well as every left i. Remove its
at most one chosen neighbour. Now all left x and i are absent. The
chosen-a/good-slot inequality gives at most 6p remaining block vertices.
Restore at most one neighbour and the connector, yielding 6p+2<=7p.
The B_s case uses the other orientation of the same inequalities.

**2<=m<=3.** If both colours occur, choose an A and a B, and remove their
chosen neighbours, at most two vertices total. All i are absent; in each
block at least one of x,y is absent, since their omitted indices differ.
The remaining block is a subgraph induced by deleting i and one leaf
from the local path, namely a P_3 plus an isolate. Each block contributes
at most 3, for at most 6p total. Restore the at most two removed vertices
and all m connectors: |D|<=6p+2+m<=7p, using p>=5.

If just one colour occurs, choose two connectors of that colour, say A's.
Remove the union of their chosen neighbours, at most two vertices. Each
left x,y and each right c omits only one A and therefore meets the pair;
each left i meets both. These types are absent after removal. The selected
block types left over number at most 4p (left c and right x,y,i).
Witnesses contribute at most 2p. Restoring the removed vertices and all
m connectors gives again |D|<=6p+2+m<=7p. Reverse colours for two B's.

**m=4, with two connectors of each colour.** Remove the union of the
chosen neighbours of all four connectors, at most four vertices. Every
selected block type is adjacent to a chosen connector: each i meets
its entire colour, while each x,y,c omits only one of its colour. Thus
only witnesses remain, at most 2p. Restoring four neighbours and four
connectors gives |D|<=2p+8<=7p.

**All remaining cases.** These have m>=4 with a colour occurring at least
three times, or m>=5 (which always has such a colour). Suppose
q_A>=3. Every left x,y,i and every right c has at least two chosen A
neighbours. Such a vertex cannot belong to a dissociation set at all.
This is an absence conclusion, with no removed-neighbour allowance.

If q_B=0, at most 4p selected block types and 2p witnesses remain. Since
m=q_A<=t<=p, |D|<=6p+m<=7p.

If q_B>=1, choose one B and remove its at most one chosen neighbour.
Now all right i and at least one right leaf per block are also absent.
At most p left c and p right leaves remain among selected block types,
with at most 2p witnesses. Restore at most one neighbour and all m<=2t
connectors. Therefore |D|<=4p+1+m<=4p+1+2t<=6p+1<=7p.
The q_B>=3 case interchanges the wings.

These cases exhaust every D, proving beta_2(F^-)<=7p for every allowed
t,p. For attainment, choose c,x,i in each left block and x,y,a,b in each
right block, with no connector. The only edges induced are left c-x
and right x-a,y-b pairs. The size is 7p, in F and F^-. Hence

    beta_2(F)=beta_2(F^-)=7p.                         (3)

This is an all-parameter combinatorial proof; no finite computed optimum
is a premise.

## Two-connectivity, safe deletion and all scales

The witness edges with offsets 2 and 3 form a Hamiltonian cycle avoiding e:
follow left index s, right s+3, left s+1 modulo 2p. These offsets occur
for p>=5. Attach each a-x-c-y-b path as an open ear. This is two-connected
on all vertices except i and connectors. Each connector has at least p>=5
old x/y neighbours, so may be added with at least two old neighbours.
Each i then has its old b-neighbour and all t>=2 connectors of its colour.
Adding it likewise preserves two-connectivity. Thus F^- is two-connected.

Take k disjoint copies of F^-, and join each left port b_0^L to the right
port b_0^R of the next copy, cyclically. At k=1 this restores e. At k>=2,
deleting any vertex leaves its piece connected, and destroys at most
one linking edge because the two ports in a piece are distinct. The
cycle of pieces remains connected, including k=2 where one of its two
links survives. This proves two-connectivity at every k.

Each port acquires one new edge, restoring degree p+1. All other degrees
are unchanged; the completed graph has exact minimum t+1 and maximum
Delta even at p=t. Literal forming/minimality witnesses are preserved.
Every dissociation set restricts in each piece to size at most 7p by (3).
The repeated attaining set has no left port, hence no new link has both
ends chosen; it attains 7pk. The n,|S| and beta_2 claims follow.
Finally 8delta-14=2(4t-3) and Delta=(4t-3)p/t imply (1) exactly.

## Parameter coverage and verification limits

For t not divisible by 3, the domain is p=tr with
r>=ceil(5/t). Thus r>=2 suffices for t=4, and r>=1 suffices for every t>=5. For t=3 the domain is every p>=5, giving delta=4 and
Delta=15,18,21,24,... . For t=6 it is every even p>=6; for t=9 every
multiple of 3 at least 9. In general if 3 divides t, the step is t/3.
At t=2 the domain starts p=6; these balanced-omission graphs differ
from the preceding uniform-omission family even at common parameters.
Equation (2) holds for every t>=5, including t divisible by 3.

Run `python3 -B scripts/check_balanced_omission_degree_family.py`.
The physical checker verifies both completed lifts and safe-deleted pieces,
including p=t, k=1,2,3, connectors meeting no y, pair/triple coverage,
one-capacity case arithmetic, literal forming and deletion failures,
every single-vertex deletion for connectivity, and the displayed attaining
set. Its report explicitly distinguishes physical checks and the analytical
upper cap. It does not exhaustively solve beta_2 on the large physical
graphs. Previous audits do not cover this extension; it needs its own
exact-source proof and unchanged-checker execution audit.

The independent final audit returned **ACCEPT** for this exact p>=5
extension. It verified all 11 manifest files, ran the original checker
unchanged with assertions enabled, and reproduced the complete 40,530-byte
report byte-for-byte (SHA-256
8ec15dddba70ae00fb3ef8bb7a7be2b8914018edd62771ea0f07c81947933d21),
with exit status 0 and empty stderr. The report covers 59 physical models,
5,704 literal deletion failures, 9,560 vertex-deletion checks, 52 no-y
controls, 3,122 pair and 7,000 triple coverage checks, 3,265 budget checks
and 607 arithmetic parameters. The earlier research critique covered the
p>=6 proof only; it is not relabelled as the p>=5 execution audit.
Full responses and the frozen source manifest are preserved in
`../output/balanced-omission-degree-review.json`. This evidence paragraph
was added after the source freeze; the proof and checker are unchanged.
