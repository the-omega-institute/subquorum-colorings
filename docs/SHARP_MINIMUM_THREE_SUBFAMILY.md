# Attaining the minimum-degree-three bound at maximum degrees 15,20,25,...

The following construction concerns specified inclusion-minimal forming
sets inducing selected stars and isolates. It does not assert an exact
SF_2 value. Write beta_2 for the unrestricted dissociation number.

**Theorem.** For every even p>=6 and integer k>=1 there is a two-connected
simple bipartite graph G_(p,k), with a specified minimal two-star-forming
selection S, such that

    n=(12p+4)k, |S|=8pk, beta_2=7pk,
    minimum degree=3, maximum degree=5p/2.

Its selected gap pk attains exactly the upper bound
Delta*n/(12Delta+10) of
[COMBINED_CENTRE_LEAF_DEGREE_BOUNDS.md](COMBINED_CENTRE_LEAF_DEGREE_BOUNDS.md)
at delta=3 and Delta=5p/2. Consequently that coefficient is sharp in the
specified selected-component class, even two-connected, for every maximum
degree allowance Delta=15,20,25,... . Sharpness at other degree allowances
and at higher minimum degree is not inferred.

## The base graph and its four shared vertices

Use the 2p six-vertex blocks and witness interface of
[SHARP_MINIMUM_TWO_DEGREE_BOUND.md](SHARP_MINIMUM_TWO_DEGREE_BOUND.md).
In each block the local edges form the path a-x-c-y-b-i. The first p
blocks are left and the next p right, with opposite bipartite orientations.
Witness index2j denotes a_j and2j+1 denotes b_j in each wing. A left witness
of index t meets right indices t,...,t+p-2 modulo2p; if t is even it also
meets t+p modulo2p. Select all c,x,y,i.

Replace the two old unused vertices by A_0,A_1,B_0,B_1. A's have the colour
of left centres, B's that of right centres. With wing indices0<=j<p, add

- A_0--i_j^L and A_1--i_j^L for every j;
- A_0--x_j^L and A_1--y_j^L for every j;
- B_0--i_j^R and B_1--i_j^R for every j;
- B_0--x_j^R and B_1--y_j^R for every j;
- B_0--c_j^L for j<p/2 and B_1--c_j^L for j>=p/2;
- A_0--c_j^R for j<p/2 and A_1--c_j^R for j>=p/2.

There are no other edges incident to the four new vertices. Call the
graph F_p, and put e=b_0^L b_0^R. Write F_p^- for F_p-e. The exact claims
below hold in both graphs. The omitted edge is outside every witness
relation used in the cap proof.

Each c,x,y has degree3 and each i has degree3. Every witness has degree
p+1 in F_p, with only the two port degrees reduced by one in F_p^-.
Each of A_0,A_1,B_0,B_1 has degree p+p+p/2=5p/2. Thus both graphs have
minimum degree3 and maximum5p/2.

The selected subgraph consists of2p copies of P_3 and2p isolates. Each
outside witness is formed through its leaf owner. Each added vertex has
an active selected leaf neighbour. Deleting x,y,c makes respectively
a,b,a fail, by the same literal witnesses as before. Deleting i makes
the newly omitted i fail: all its neighbours are outside S. Extra edges
have outside endpoints, so none changes these failures. This proves
inclusion minimality in both graphs.

## A cap for every dissociation set

Fix an arbitrary dissociation set D in F_p^-. Let r be the number of
chosen vertices among A_0,A_1,B_0,B_1. Any chosen added vertex has at most
ONE neighbour in D over its entire neighbourhood, including the opposite
wing's centres.

The witness slots (L_j,R_(j+1)), j modulo p, each contain a complete
K_(2,2). Hence at most two witnesses of any slot can belong to D: if both
sides are nonempty, both have size one. The total chosen witness count
is therefore at most2p. The same slots and the predecessor relations used
in the earlier proof remain present after deleting e.

**No added vertex chosen.** The graph on the remaining vertices is exactly
the graph obtained by omitting both old u's from H_p-e. The earlier
good-slot proof gives |D|<=7p. It uses only the surviving witness kernel.

**Exactly one chosen vertex, of type A_1 or B_1.** In a comparison copy of
H_p-e, identify A_1 (respectively B_1) with the old u of its wing, and
leave the other old u unchosen. Every edge of that comparison graph
having both endpoints in D is present in F_p^-: the chosen added vertex
meets every i and in particular the distinguished y. Thus D is a
dissociation set in H_p-e, whose proven cap is7p.

**Exactly one chosen vertex, of type A_0 or B_0.** First suppose A_0 is
chosen. Delete from D all its chosen neighbours, at most one vertex.
In each left block x and i are now absent. Its remaining vertices are
a,c,y,b, comprising the path c-y-b and isolated a. Their contribution is
at most2 plus the indicator that a is chosen. The right wing has no
chosen added vertex, so the earlier local good-block bound gives3p+g_R.
Let a_L count chosen left a-witnesses. We claim a_L+g_R<=p.

In a slot containing both a chosen left a and a good right block,
complete adjacency forces its two chosen witnesses to be exactly the
two a's. They saturate each other. The left a excludes both witnesses
in the preceding right block, and the right a excludes both in the
preceding left block. Thus the predecessor slot has neither a chosen
left a nor a good right block. Double slots inject into zero slots,
proving the claim. The remaining set has size at most
2p+a_L+3p+g_R<=6p. Restore at most one removed neighbour and A_0 to get
|D|<=6p+2<=7p.

For B_0 use the same slots, now counting good left blocks and chosen
right a's. A double slot again consists of just the two a's and forces
its predecessor empty. Thus g_L+a_R<=p. Removing at most one B_0-neighbour
gives the same6p+2 bound. This argument does not assume that the full
witness interface has a reflection symmetry.

**At least two added vertices chosen, all on one side.** They must be
A_0,A_1 or B_0,B_1. For the A case, remove their chosen neighbours from D;
the union has size at most two, since each chosen A has capacity one.
All left x,y,i are absent afterwards. Among S, only the p left centres
and the3p right x,y,i may remain, giving at most4p selected vertices.
The witness bound contributes at most2p. Restore at most two neighbours
and the two A's: |D|<=6p+4<=7p. The B case reverses the wings.

**Chosen added vertices on both sides.** Pick one chosen A and one chosen
B and remove all their chosen neighbours, at most two vertices in total.
In each wing all i and one of x,y are now absent. Each block's remaining
four vertices induce a P_3 and an isolate, so contribute at most3.
The2p blocks contribute at most6p. Restore the two possible neighbours
and all r<=4 added vertices: |D|<=6p+2+r<=6p+6<=7p, since p>=6.

These cases cover every D, proving beta_2(F_p^-)<=7p. The set containing
c,x,i in every left block and x,y,a,b in every right block, with no added
vertices, is dissociation of size7p in both graphs. Its only edges are
left cx and right xa,yb. Therefore

    beta_2(F_p^-)=beta_2(F_p)=7p.                        (1)

The deletions in this proof use only the at most one chosen neighbour
of each chosen added vertex. A common neighbour is removed once in the
union; no source supplies a separate allowance to each block.

## Two-connectivity and every lift size

The witness offsets2,3 form a Hamiltonian cycle and avoid e. Attach each
path a-x-c-y-b as an open ear. This gives a two-connected spanning graph
on all vertices except the i's and four added vertices. Adjoin each of
A_0,A_1,B_0,B_1 with its p distinct x- or y-neighbours already present.
Adjoining a vertex with at least two old neighbours preserves
two-connectivity. Finally each i has its old b-neighbour and its two
added neighbours, so can be adjoined in the same way. This constructs a
two-connected spanning subgraph of F_p^-. Adding the other edges preserves
two-connectivity.

Take k disjoint copies of F_p^-, and add b_(0,r)^L b_(0,r+1)^R cyclically.
For k=1 this restores e. For k>=2 the two ports of each copy are distinct;
after any vertex deletion each surviving copy is connected and at most
one linking edge is lost. The cycle of pieces remains connected, including
k=2, when one of the two links survives. Degrees and literal deletion
witnesses are preserved.

Every dissociation set restricts to one in each F_p^-, giving the upper
bound7pk. Repeating the displayed7p-set attains it: every new link has its
left port outside that set. This proves the exact all-k claims. Finally
Delta=5p/2 gives

    Delta*(12p+4)/(12Delta+10)=p.

Together with the general upper theorem, this proves sharpness along
the stated degree subfamily. No finite cap or asymptotic extrapolation
is a premise of (1).

## Verification scope

This is a new proof, outside the final audits of the minimum-degree-two
family and of the two general upper bounds. Its original research handle
and a separate final proof/execution audit must be recorded with their
actual results. The structural checker tests physical vertices, edges,
literal deletions, complete witness slots and every
single-vertex deletion; the infinite-parameter cap is the case proof above.
The independent research response verified the global load constraints
and offered exploratory solver values, but explicitly did not establish
the all-p cap. The case proof above was developed separately afterwards;
no numerical optimum reported by that response is used as a premise.

Run `python3 -B scripts/check_sharp_minimum_three_subfamily.py`. It checks
20 physical models at p=6,8,10,12,20 and k=1,2,3, including the five
single-copy safe-edge deletions. It verifies3,136 literal deletion
failures and4,844 single-vertex deletion connectivity checks. Smaller
abstract witness kernels have1,118,464 fully enumerated witness-subset
pairs; every legal pair satisfies the two chosen-a/good-slot inequalities
and the2p witness cap. Those kernel checks are not large physical-graph
optimum computations. No Lean or priority claim is made.

The independent final exact-source audit returned **ACCEPT**. All10 files
matched their manifest. After creating an initially absent output directory
in its reconstruction, the reviewer ran the unchanged checker to exit0
and empty stderr, reproducing the complete8,090-byte report byte-for-byte
(SHA-256 ef5c942545abd74b728228f242e1288f150dc82f199cee71aa5d0faae0bee7c7).
The report has20 physical models in total,15 lifts plus5 safe-edge
deletions. The full response, original setup failure and two wording
clarifications are preserved in
`../output/sharp-minimum-three-subfamily-review.json`. Only this evidence
paragraph was added after the reviewed source freeze.
