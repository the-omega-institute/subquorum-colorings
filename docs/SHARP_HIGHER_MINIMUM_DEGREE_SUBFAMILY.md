# Sharp selected-star bounds at every higher minimum degree

**Theorem.** Fix integers delta>=3, r>=3 and k>=1. Put t=delta-1,
p=tr and Delta=(4t-3)r=(4delta-7)r. There is a two-connected finite simple
bipartite graph G with a specified inclusion-minimal two-star-forming set S
inducing only P_3's and isolates, for which

    n=(12p+2t)k, |S|=8pk, beta_2(G)=7pk,
    minimum degree=delta, maximum degree=Delta.

Here beta_2 is the unrestricted dissociation number. The selected gap pk
attains the general coefficient

    Delta/[12Delta+8delta-14]=r/(12r+2).                 (1)

Thus this coefficient is sharp for the specified selected-star class,
even with two-connectivity, for every delta>=3 along all maximum-degree
allowances Delta=(4delta-7)r, r>=3. This does not settle intervening maximum
degrees, regular selected-star sharpness, arbitrary selected-component
structures, exact SF_2 values, or grid triple equality.

## Construction

Use p left and p right six-vertex blocks c,x,y,i,a,b. Each has the local
edges cx,cy,xa,yb,ib, forming the path a-x-c-y-b-i. Opposite wings have
opposite bipartite orientations. Select c,x,y,i in every block.

For the witness interface, index a_j by2j and b_j by2j+1 in each wing,
0<=j<p. A left witness of index s meets right indices s,...,s+p-2 modulo2p;
when s is even it additionally meets s+h, where h=p-1 if p is odd and
h=p if p is even. This is exactly the circulant of
[SHARP_MINIMUM_TWO_DEGREE_BOUND.md](SHARP_MINIMUM_TWO_DEGREE_BOUND.md).

Add A_0,...,A_(t-1) on the colour of the left centres and B_0,...,B_(t-1)
on the colour of the right centres. For each j, add the following edges,
with subscripts on A,B taken modulo t:

- i_j^L meets every A, x_j^L every A except A_j, and y_j^L every A except A_(j+1);
- c_j^L meets every B except B_j;
- i_j^R meets every B, x_j^R every B except B_j, and y_j^R every B except B_(j+1);
- c_j^R meets every A except A_j.

There are no other edges incident to these added vertices. Call the base
F_(t,r), put e=b_0^L b_0^R and write F^- for F_(t,r)-e. Both graphs have
the same all-parameter dissociation cap proved below.

All c,x,y have degree2+(t-1)=t+1 and all i have degree1+t=t+1. Each
witness has degree p+1 in F_(t,r), reduced only at the two ports in F^-.
Every added vertex has p neighbours of type i, and sees all but p/t
vertices in each of the three relevant classes x,y,opposite c. Its degree
is4p-3p/t=(4t-3)r=Delta. Since r>=3 and t>=2, the minimum degree is exactly
t+1=delta and maximum exactly Delta, including after safe-edge deletion.
The graph is simple and bipartite by the displayed orientations.

Every witness is formed through its active leaf owner. Every added vertex
has an active selected leaf neighbour. Deleting x,y,c makes respectively
a,b,a fail, just as in the six-vertex template. Deleting i leaves the newly
omitted i with no selected neighbour. These literal failures are preserved
by the added edges, whose other endpoints are all outside S. Thus S is
inclusion-minimal and forming, with size8p.

## An upper cap with one total capacity per chosen added vertex

Fix any dissociation set D of F^-. Let m be its number of chosen added
vertices. Each such vertex has at most ONE chosen neighbour over its whole
neighbourhood. The union of the chosen neighbours of any two chosen added
vertices therefore has size at most two, even if their neighbourhoods
overlap. All these neighbours lie in the selected block types c,x,y,i.

The witness slots (L_j,R_(j+1)) each contain a complete K_(2,2), avoiding e.
Each slot contributes at most two chosen witnesses: if both sides are
occupied, both sides must have size one. Consequently there are at most2p
chosen witnesses altogether.

**m=0.** The earlier no-u good-slot argument applies verbatim and gives
|D|<=7p. It is a pure combinatorial statement about the block and witness
graph, independent of all added vertices.

**m=1.** Suppose A_s is chosen. It meets every left i, and at least one
left y, since t>=2 and p is a multiple of t. Choose such an index j.
Compare with H_p-e having its old left u adjacent to all left i and to
y_j, and its right u unchosen. This comparison graph's edges between
vertices of D are all present in F^-. The earlier cap remains valid for
this distinguished index j. Indeed the full witness interface is invariant
under simultaneous cyclic shifts of the block indices in both wings;
after shifting j to0, the unchosen right u can be given the shifted
distinguished neighbour arbitrarily, with no effect on D. Deletion of e
at a different index cannot invalidate the earlier proof: its entire
used kernel has no offset-zero b--b edges. Alternatively its single-u
proof uses only that kernel, the i-neighbours and one distinguished y.
Thus |D|<=7p. The B_s case reverses the wings; both single-u orientations
were proved explicitly in the earlier note.

**m=2, one A and one B.** Remove all chosen neighbours of these two added
vertices, at most two vertices in total. In every wing all i are now
absent. In each block, the omitted A- or B-index of x differs from that
of y because t>=2. At least one leaf therefore meets that wing's chosen
added vertex and is absent after removal. The remaining vertices of each
block induce a P_3 plus an isolate or a subgraph thereof; they contribute
at most3 to a dissociation set. All2p blocks contribute at most6p. Restore
at most two neighbours and both added vertices: |D|<=6p+4<=7p, since p>=6.

**At least two chosen A's or at least two chosen B's.** This covers the
remaining m=2 case and every m>=3. Choose two on one side, say two A's,
and remove the union of their chosen neighbours, at most two vertices.
Each left i meets both A's. Each left x,y and each right c omits only
one A, so meets at least one of the chosen pair. All these vertices are
absent after removal. Among the selected block types there remain at
most the p left centres and3p right x,y,i, hence4p vertices. Witnesses
contribute at most2p. Restore at most two removed neighbours and all
m<=2t added vertices. This gives

    |D|<=6p+2+m<=6p+2+2t<=7p,

because p=tr>=3t>=2t+2 for t>=2. The two-B case interchanges the wings.

The cases exhaust D, proving beta_2(F^-)<=7p for every t>=2,r>=3. Taking
c,x,i in every left block and x,y,a,b in every right block, and no added
vertex, gives a dissociation set of size7p in both graphs. Its only edges
are the left cx pairs and right xa,yb pairs. Therefore

    beta_2(F^-)=beta_2(F_(t,r))=7p.                     (2)

No finite physical-graph optimum is assumed in this proof.

## Connectivity, all lift sizes, and sharpness

Witness offsets2,3 give a Hamiltonian cycle avoiding e. Adjoin each path
a-x-c-y-b as an open ear. This is a two-connected spanning graph on all
vertices except the i's and added vertices. Each added vertex has at
least p-p/t>=3 distinct old y-neighbours, so can be adjoined without
destroying two-connectivity. Each i then has its old b-neighbour and
t>=2 added neighbours and can be adjoined in the same manner. Thus F^-
is two-connected.

For k disjoint copies of F^-, join the left port of each copy to the
right port of the next, cyclically. At k=1 this restores e. At k>=2,
deleting one vertex leaves each affected copy connected and loses at
most one link, since the two ports in a copy are distinct. The cycle of
pieces remains connected; at k=2 one of its two links survives. This
proves two-connectivity for every k. Degrees and literal minimality
witnesses are preserved.

A dissociation set restricts in each copy to a set of size at most7p.
The repeated displayed optimum attains7pk because it omits every left
port. Thus n=(12p+2t)k, |S|=8pk and d=pk exactly. The upper theorem in
[COMBINED_CENTRE_LEAF_DEGREE_BOUNDS.md](COMBINED_CENTRE_LEAF_DEGREE_BOUNDS.md)
applies at delta=t+1 and Delta=(4t-3)r. Since 8delta-14=2(4t-3),

    Delta*n/(12Delta+8delta-14)
       =r(12tr+2t)k/(12r+2)=trk=pk,

proving (1) and the stated sharpness.

## Verification and provenance

The degree-three candidate inspired this uniform omission construction;
the new proof uses the shared total neighbour capacities and the earlier
all-p cap. Its research and exact-source audits have separate original
handles; earlier acceptance is not a review of this theorem. The physical
checker tests specified models and literal witnesses; the infinite-parameter
claim is (2), with the all-k restriction and attaining-set proof above.
Run `python3 -B scripts/check_sharp_higher_minimum_degree.py`. It checks
20 physical models at t=2,3,4,6, r=3,4 and k=1,2, including four
single-copy safe-edge deletions. The report separates the exact physical
properties,2,880 literal deletion failures and4,530 delete-vertex
connectivity checks from the analytical dissociation cap. It also checks
every same-colour connector pair's required coverage and each single
connector's distinguished y-neighbours in these models. No large-graph
exhaustive dissociation optimization is claimed.
No exact SF_2, regular-sharpness, grid, Lean or literature-priority claim
is made.

The independent research response supplied an explicit fixed-deletion
single-connector proof. The separate final exact-source audit returned
**ACCEPT**, including both single-connector orientations, odd p, the
kernel excluding every offset-zero b--b edge, and all lift sizes. The
reviewer reconstructed all10 manifest files, ran the unchanged original
checker with assertions enabled to exit0 and empty stderr, and reproduced
the complete9,808-byte report byte-for-byte (SHA-256
2372e79d5f5c40d52776ae09535c2bab666e39bc5272308e1986843bad497415).
See `../output/sharp-higher-minimum-degree-review.json` for the exact
frozen manifest, full responses and execution scope. Only this evidence
paragraph was added after the reviewed source freeze.
