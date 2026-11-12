# Three-connected degree-three threshold examples at every scale

For every integer k>=1 there is a finite simple bipartite graph G_k and
specified inclusion-minimal two-star-forming set S, inducing P_3's and
isolates, with

    n=28k, |S|=16k, beta_2(G_k)=14k,
    kappa(G_k)=delta(G_k)=3, Delta(G_k)=5.

Here beta_2 is the unrestricted dissociation number: the largest order
of an induced subgraph of maximum degree at most one. Formation uses
not necessarily induced copies of K_(1,2). The selected gap is n/14,
exactly Delta*n/(12Delta+8delta-14). Together with
[MAXIMALLY_CONNECTED_DEGREE_THRESHOLD.md](MAXIMALLY_CONNECTED_DEGREE_THRESHOLD.md),
this proves threshold sharpness with kappa=delta for EVERY delta>=3.
The statement concerns a specified minimal selection, not exact SF_2.

## A four-port piece

There are two left and two right blocks, each a path a-x-c-y-b-i.
Indices j are 0,1. Select c,x,y,i in every block. Between witnesses
{a_0,b_0,a_1,b_1} in the two wings, put K_(4,4) minus the two edges
b_j^L b_j^R. Add connectors A_0,A_1 in the colour of left centres and
B_0,B_1 in the colour of right centres. A_j meets left y_j, both left
i's and right c_(1-j); reverse wings for B_j. There are no other edges.
Call this 28-vertex graph H.

Equivalently, H is the base F in
[DEGREE_THREE_THRESHOLD_AND_SELECTED_PORT.md](DEGREE_THREE_THRESHOLD_AND_SELECTED_PORT.md)
with ALL four edges x_j^L A_(1-j), x_j^R B_(1-j) deleted simultaneously.
Every x has degree 2, every connector degree 4, other selected vertices
degree 3, and every witness degree 5. We prove its exact cap directly;
one-edge safe deletion alone would not imply simultaneous safety.

## Exact dissociation cap: beta_2(H)=14

Fix any dissociation set D. Let C be its chosen connectors, with q_L
left and q_R right, m=q_L+q_R; let w be its chosen witnesses. Each of
the four selected P_3's contributes at most two vertices. In a wing
with q=0,1,2 chosen connectors, at most 2,1,0 isolates i are chosen.
For q=1 this uses the connector's ONE total chosen-neighbour capacity,
shared by both i's and its other neighbours. Consequently

    |D intersect S| <=12-m.                          (1)

The two disjoint complete witness slots (L_0,R_1),(L_1,R_0), where
L_j={a_j^L,b_j^L}, imply w<=4: a dissociation set has at most two
vertices in each K_(2,2). If w<=2, (1) gives |D|<=14.

If witnesses lie in both wings, either wing has at most two: every
witness has at most one non-neighbour in the opposite wing, so three
opposite chosen witnesses would give two chosen neighbours. For w=3,
the singleton witness must be b_j; the opposite pair is b_j,z, with
z one of a_j,a_(1-j),b_(1-j). The singleton and z are cross-saturated,
meaning each already has its permitted chosen neighbour across wings.
For w=4 mixed, all four b's are chosen and cross-saturated. A saturated
a forbids its own x; a saturated b forbids both its own y and i.

### Four or three witnesses entirely in one wing

Orient that wing left; reversing wings preserves H.

For w=4, both left blocks contain a,b. Each contributes at most two
selected vertices, since the entire P_6 has dissociation number four.
If q_L>=1, all left i's are absent, because they would meet b and a
chosen A. For every chosen A_j, its y_j is likewise absent. That block
then has at most one of c_j,x_j: choosing both would give x_j its a_j
and c_j as two chosen neighbours. Thus the left selected count is at
most 4-q_L. The right selected count is at most 6-q_R by its two star
caps and isolate count. Hence |D|<=10-m+4+m=14.

For w=3, one left block has both a,b and the other a single witness.
Their selected contributions are at most two and three, respectively.
If q_L=1, both i's are absent. If the chosen A_j indexes the full block,
that block contributes at most one and the other at most three. If it
indexes the single-witness block, that block contributes at most two
(its i is absent); the full block contributes at most two. Either way,
the left count is at most four. If q_L=2, both i's are absent and the
full block contributes at most one, the single-witness block at most
two. In all cases the left count is at most 5-q_L. The right contributes
at most 6-q_R, giving |D|<=11-m+3+m=14.

### Four mixed witnesses

All y,i are absent. The remaining selected vertices are four edges c-x. Each chosen connector is
adjacent to a different opposite centre. In that centre's c-x edge,
both endpoints cannot be chosen (the centre would have two neighbours).
Therefore each of the m distinct affected edges contributes at most
one instead of two. Hence |D intersect S|<=8-m and |D|<=12.

### Three mixed witnesses

Suppose the singleton is left b_j and the right pair b_j,z. If (1) is
strict, its integral deficit already gives |D|<=14. It remains to rule
out equality in (1). Equality requires every star to contribute two
vertices and each wing to attain its isolate bound 2-q.

Whenever a connector and its opposite centre were both chosen, that
centre could not coexist with a leaf, so its star could not contribute
two. Thus a chosen connector forces its opposite centre absent in this
equality case. A star with centre absent must choose both leaves.
A star with y absent must choose c,x.

The saturated left b_j forces y_j,i_j absent, and hence c_j,x_j chosen.
Thus q_L>=1 (otherwise its missing isolate violates equality), and
B_(1-j) is absent (otherwise chosen c_j has two neighbours). Therefore
q_R is either zero or one; in the latter case its connector is B_j.

If q_R=0, both right i's are chosen. The chosen right b_j then forbids
y_j; its star must choose c_j,x_j. Hence A_(1-j) is absent. Since q_L>=1,
only A_j is chosen, and the left equality isolate is i_(1-j). It uses
all A_j capacity, forcing right c_(1-j) absent. The three possible z
now contradict equality: z=b_(1-j) forbids a required right isolate;
z=a_j forbids the required right x_j; z=a_(1-j) forbids right x_(1-j)
while its centre is also absent, leaving its star fewer than two.

If q_R=1, B_j is chosen and its one required right isolate consumes
its capacity. Hence right y_j and left c_(1-j) are absent. The right
j-star chooses c_j,x_j, again forcing A_(1-j) absent. Thus only A_j is
chosen, with left i_(1-j) consuming its capacity; right c_(1-j) is absent.
If z=b_(1-j), saturation forbids right y_(1-j), so that star has both
centre and y absent. If z=a_j, right x_j is forbidden. If z=a_(1-j),
right x_(1-j) and its centre are both absent. Every case contradicts
its required two star vertices. This exhausts the mixed patterns.

Thus |D|<=14 for every D. Choose c,x,i in each left block and x,y,a,b
in each right block, with no connectors. Its only edges are left cx and
right xa,yb; it has fourteen vertices. Therefore beta_2(H)=14.

## Local attachment after any two vertex deletions

Let Z have at most two vertices. The surviving witness core is connected.
If each side retains at least three witnesses, two witnesses in one side
have a common opposite neighbour (each misses at most one). If one side
has only two, both cuts were on that side and the other side is untouched;
its two universal a's join the surviving pair, and every other witness
has an opposite neighbour. Call a survivor attached if it can reach this
core in H-Z.

Each connector has two vertex-disjoint own-wing i_j-b_j routes. If both
routes are hit, exactly two deletions are spent in that own wing. Its
opposite centre is untouched and has an untouched path c-x-a to the
core, so the connector attaches there. Otherwise one own route attaches
it. This proves all surviving connectors attached without assuming the
centres attached.

Each surviving i has three distinct attached potential neighbours b,A_0,A_1
(or b,B_0,B_1); one survives. A surviving y attaches through b or its own
connector if either survives. If both are deleted, all cuts are spent,
so the untouched route y-c-x-a attaches it. A surviving centre attaches
through y or its opposite connector if either survives. If both are
deleted, its untouched route c-x-a attaches it. Finally x attaches through
its a or centre unless Z is exactly {a,c} in its block. In that case x
is the only unattached survivor; all other survivors are attached by the
preceding argument. There can be only one such exceptional x.

## Exact composition through arbitrary port matchings

Take k disjoint H-pieces. Match all 2k left x-ports bijectively to all
2k A-connectors, and independently all 2k right x-ports to all 2k
B-connectors. Each port is used exactly once; pairings may lie in one
piece or across pieces. The resulting graph G is simple and bipartite:
H has no x-connector edge and physical endpoints never repeat. All x
degrees become3 and connector degrees5. The other degrees are unchanged.

Every dissociation set restricts in each H-piece to at most fourteen.
Repeating the fourteen-set above avoids every connector, so every such
composition has beta_2(G)=14k, independently of its interface pattern.
Also every partial restoration of the four original edges has beta14:
it is a supergraph of H, and the same fourteen-set still attains14.

The selected subgraph stays four P_3's and four isolates per piece.
Each witness a is formed through selected x, each b through selected y,
and every connector through its own selected y. Removing selected x,y,c,i
makes a,b,a,i, respectively, fail formation. These literal failures use
only the unchanged witness edges or the absence of any selected neighbour
of i. Thus S forms and is inclusion-minimal for every interface pattern.

Define the quotient multigraph Q by shrinking each H-piece to one vertex
and retaining every interpiece port edge with its multiplicity. Discard
within-piece loops for cuts. For k>=2, the following criterion is exact:

    kappa(G)=3  if and only if  every nontrivial edge cut of Q has size>=3.
                                                               (2)

For sufficiency, delete any at most two physical vertices. Each piece
has its connected surviving witness core. If there is no exceptional x,
at most two links are lost and every surviving endpoint attaches to its
own core. The surviving quotient is connected by the edge-cut assumption.
If there is an exceptional x, both cuts were its own a,c, which are not
port vertices. Thus no link is deleted; the sole link incident to that
exceptional x may fail to join its own core, but every other link joins
attached endpoints. Removing that one quotient edge still leaves a
connected quotient. The exceptional x itself attaches through its matched
connector, which survives and attaches to its core, even when both are
in the same piece. Hence the whole graph survives the cut. Minimum
degree3 gives kappa(G)=3. For k=1 the same attachment argument directly
proves kappa=3 for all four within-piece pairing patterns.

For necessity, if a quotient cut has size at most two, delete one physical
port endpoint on each crossing edge. The two sides retain their nonempty
witness cores, but no physical edge crosses between them. This destroys
connectivity using at most two vertices. An empty cut already makes G
disconnected. This proves (2).

For an explicit all-scale three-connected family, pair

    x_j^L(h) to A_(1-j)(h+1),
    x_j^R(h) to B_(1-j)(h+1),

with h modulo k and j=0,1. At k>=3 the quotient is a cycle with four
parallel links in each consecutive bundle, so every edge cut has size
at least8. At k=2 its two directed bundles give eight distinct edges;
at k=1 the original four edges are restored. Thus every k has
kappa=delta=3, and n28k, selected16k, beta14k prove the stated threshold
sharpness. The arbitrary-interface theorem and criterion(2) provide a
composition result beyond the cyclic family.

## Reproduction

Run `python3 -B scripts/check_three_connected_degree_three.py`.
It checks all sixteen subsets of port-edge deletions by an independent
exact dissociation recursion, the four-piece patterns in the proof, every
cut of size at most two in H, and degrees, literal minimality and all
two-vertex cuts in completed small lifts. Independent port permutations
check the quotient criterion, including disconnected and two-edge-cut
interfaces. Larger lifts have physical controls. The all-k cap and connectivity are proved above; finite checks
are implementation controls. No Lean, exact unrestricted SF_2, priority,
authorship or submission claim is made.

The final independent exact-source audit returned **ACCEPT**, including the
arbitrary-interface composition and both directions of the quotient criterion.
It reconstructed all13manifest files and ran the original checker unchanged
with assertions enabled, terminal exit0, reproducing the complete31,295-byte
report byte-for-byte (SHA-256
9da1c5f6fb086abd176079c90e87b445bca9d83b845b6dd2f89d1542e3e9eda2).
The reviewer captured1,064bytes of unrelated Python-startup spreadsheet-runtime
stderr; the warning and its execution qualification are preserved in
`../output/three-connected-degree-three-review.json`. This evidence paragraph
is the only addition to the frozen reviewed note; proof and checker are unchanged.
