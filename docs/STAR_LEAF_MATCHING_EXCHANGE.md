# Matching certificates for exchanges retaining all selected star leaves

Let G be a finite simple bipartite graph and S an inclusion-minimal
two-star-forming set whose selected components are stars, edges or isolates.
Choose one deletion witness for each leaf of every selected star of order
at least three. Write C for those star centres, L for their leaves, I for
the selected isolates, P for the vertices of isolated selected edges, and
W for the chosen witnesses. Put c=|C| and e=|L|=|W|. The auxiliary graph

    Q=G[W union I]

gives an exact exchange formula:

    max |D| = |S|-c+e-nu(Q),                              (1)
    D subset S union W,   L subset D,   Delta(G[D])<=1.

Here nu is maximum matching size. Thus the maximum ranges over all
dissociation sets in S union W that retain every star leaf; retaining
centres is automatically impossible in this family. For a fixed witness
assignment, both the optimum and an attaining set have bipartite matching
and vertex-cover certificates.

In particular, if S has at most one selected isolate, then |S|<=beta_2(G), even
when witnesses conflict and selected star centres occur in both bipartition
classes. The same conclusion holds whenever nu(Q)<=e-c. For full rectangular
grids these are arbitrary-width criteria.

The leaf-retention restriction has a genuine limitation. A connected
bipartite family G_r of order12r and maximum degree at most five has a
minimal forming selection S_r of size8r, with selected star components,
such that

    beta_2(G_r)=8r,     max_(D dissociation, L_r subset D)|D|=7r.  (2)

All leaf witnesses in this family are forced. The gap in (2) concerns
the exchange restriction, while S_r itself satisfies |S_r|=beta_2(G_r).

## Formation and the leaf witnesses

A set S forms an outside vertex x if distinct a,b in S make {x,a,b}
contain a not necessarily induced K_(1,2). It is forming if every outside
vertex is formed, and minimal if no proper subset is forming. Formation
is upward closed, so minimality is equivalent to failure of each single
deletion, including a possible failure at the newly omitted vertex.
A dissociation set induces maximum degree at most one; beta_2 is its
maximum possible cardinality.

In a bipartite graph x outside S is formed exactly when it has at least
two selected neighbours, or one selected neighbour which has a selected
partner. Call a selected vertex active if it has a selected neighbour.

If ell is a leaf of a selected star of order at least three, deleting ell
leaves its centre active. No remaining selected vertex becomes inactive.
The newly omitted ell is formed by its centre and another leaf. Consequently
some previously omitted vertex adjacent to ell must fail. After deleting
ell it has either no selected neighbour, or just one inactive neighbour.
In the latter case that neighbour i and ell lie in the same bipartition
class, so i's selected degree was already zero before the deletion. Hence
every chosen leaf witness satisfies exactly one of

    N_S(w_ell)={ell},   N_S(w_ell)={ell,i_ell}, i_ell in I.       (3)

Each witness has exactly one active selected neighbour, its owner leaf.
Thus witnesses of distinct leaves are distinct and |W|=|L|. The choices
are otherwise arbitrary. In particular, edges between distinct witnesses
are allowed, and an isolate can be the helper of many witnesses.

The selected set has the disjoint partition

    S=C disjoint-union L disjoint-union I disjoint-union P,

and e>=2c. There is no edge from W to P or C; (3) lists every edge from
a chosen witness to S. A leaf has no selected neighbour apart from its
centre, and it meets only its own chosen witness among W.

## Proof of the exact leaf-retaining optimum

Take a dissociation set D subset S union W containing all L. Every centre
has at least two leaves in D, so no member of C is in D. If a witness is
retained, its owner leaf is retained and already supplies its one permitted
neighbour. It cannot retain any neighbour in W union I. Since I has no
internal edges, D intersect (W union I) is therefore an independent set
of Q. The old selected edges P are disjoint from all these vertices and
may all be added without interference. Conversely, for every independent
set J of Q,

    D=L union P union J                                  (4)

is dissociation: it consists of the old selected edges, disjoint leaf--witness
edges and isolates. Consequently the exact maximum in (1) is

    |L|+|P|+alpha(Q).

For a finite bipartite graph, a maximum matching and a minimum vertex
cover have equal size, and the complement of a minimum cover is a maximum
independent set. Therefore alpha(Q)=|W|+|I|-nu(Q), proving (1). A cover
K of Q also directly supplies the exchange

    D=((S minus C) union W) minus K,
    |D|=|S|-c+e-|K|.                                    (5)

This construction counts a helper isolate once, irrespective of how many
witnesses meet it. A chosen witness belongs to exactly one owner leaf.
No centre, leaf or isolate is allocated separately to two exchanges.

For completeness, the matching/cover equality has an elementary certificate.
Let M be a maximum matching in a bipartite graph with parts A,B. From all
unmatched A vertices, traverse nonmatching edges from A to B and matching
edges from B to A; write Z for the reached set. No unmatched B vertex is
reached, since it would give an augmenting path. Then

    K=(A minus Z) union (B intersect Z)

covers every edge. A matching edge has both ends reached or both ends
unreached, and contributes exactly one endpoint to K. Every unmatched
A vertex is reached, and no unmatched B vertex is reached, so |K|=|M|.
Every cover meets every matching edge, proving optimality of both. This
also gives an attaining independent set and hence (4), without enumerating
dissociation sets.

The graph Q and the matching problem depend on the fixed chosen witnesses.
Optimizing over all possible witness assignments is a separate question;
no polynomial claim is made for that outer optimization.

## Unconditional subclasses and the distinct-helper budget

If no selected isolate is touched by W, then Q consists of G[W] and
isolated vertices. Since it is bipartite, nu(Q)<=floor(e/2). Equation (1)
and e>=2c give

    max |D| >= |S|-c+ceil(e/2) >= |S|.                   (6)

In particular, every minimal forming selection with selected star/edge
components and no selected isolates has a dissociation exchange of at
least its cardinality. There is no assumption on witness conflicts or
on which bipartition classes contain its centres.

A simple criterion also allows touched isolates. Fix a bipartition A,B
and write W_A=W intersect A, W_B=W intersect B, e_A=|W_A|, e_B=|W_B|.
Let J_B=N(W_A) intersect I and J_A=N(W_B) intersect I, with t_B=|J_B|,
t_A=|J_A| and t=t_A+t_B. These are distinct touched isolates, not incidence
counts. The sets

    K_A=W_B union J_B,   K_B=W_A union J_A

are vertex covers of Q, including when Q contains further untouched
isolates. Their exchanges in (5) give

    beta_2(G)>=|S|-c+max(e_A-t_B,e_B-t_A)
             >=|S|-c+ceil((e-t)/2).                     (7)

Thus e-t>=2c-1 suffices for |S|<=beta_2(G). The integer threshold is exact
for the averaged bound in (7); it need not be necessary for either the
sharper colour bound or the matching optimum. The matching formula dominates
both colour choices because it uses a minimum vertex cover.

Since e>=2c, at most one touched selected isolate (t<=1) always satisfies
this criterion. Thus the unconditional subclass extends to every such S
with at most one selected isolate, and also to larger I when only one or
none is touched. More quantitatively, if |S|-beta_2(G)=d>0, then (7) forces

    t>=e-2c+2d>=2d.                                    (8)

This is a necessary condition for a genuine parameter deficit, for every
permissible witness assignment. It does not turn a large t into a
counterexample.

For a fixed witness assignment define delta=c-e+nu(Q). The exact best
leaf-retaining size is |S|-delta. A positive delta is a shortfall of this
restricted exchange. It gives no conclusion that beta_2(G)<|S|.

## The full six-by-six witness obstacle is certified by this matching

Use one-based grid coordinates and select columns

    1,4,6;  1,3,5;  1,3,4,6;  2,6;  3,5;  1,2,4,6

in rows1 through6. This is the previously checked minimal forming selection
with18 vertices. Its two selected P_3 centres are (2,1),(3,3), with four
leaves. Every omitted vertex has at least two selected neighbours except
(1,2),(4,4),(5,1), formed through the selected edges (1,1)--(2,1),
(3,4)--(3,3),(6,1)--(6,2), respectively. The selected isolates and edge
endpoints witness their own deletions. The two centres have deletion
witnesses (1,2) and (4,4), respectively. The four leaves have the direct
witnesses in the table below. These facts verify formation and every
single deletion. The complete forced leaf witnesses are

| Leaf | Witness | Selected isolate helper, if present |
| --- | --- | --- |
| (1,1) | (1,2) | none |
| (3,1) | (4,1) | (4,2) |
| (2,3) | (1,3) | (1,4) |
| (3,4) | (4,4) | none |

The only witness--witness edge is (1,2)--(1,3). The nontrivial components
of Q are the path (1,2)--(1,3)--(1,4) and the edge (4,1)--(4,2);
(4,4) and the other selected isolates are isolated in Q. Thus nu(Q)=2.
Here e=4,c=2, so (1) gives an exact leaf-retaining size of18. For example,
the cover {(1,3),(4,1)} gives

    D=(S minus {(2,1),(3,3)}) union {(1,2),(4,4)}.

This is the previously exhibited size18 dissociation set, now supplied by
a matching certificate. Independence of all chosen leaf witnesses is false
in this example, but the new matching criterion succeeds.

## A connected family where retaining all leaves loses one per block

Construct a twelve-vertex block with vertices

    x,y,a,b,c,d,p,q,A,B,C,D.

Its edges are precisely

    xa,xb,yc,yd;  aA,bB,cC,dD;  Bp,Dq;
    AC,AD,BC,BD.                                         (9)

Its bipartition classes are {x,A,B,c,d,q} and {y,C,D,a,b,p}.
Select S_1={x,y,a,b,c,d,p,q}. Its selected components are the stars
a--x--b and c--y--d, together with the isolates p,q.
Every outside vertex is formed through its active owner leaf. Deleting
a,b,c,d leaves respectively A,B,C,D unformed: in the helper cases only
the isolated p or q remains selected. Deleting x leaves A adjacent only
to the now-inactive a; deleting y analogously uncovers C. Deleting p or q
uncovers the newly omitted vertex itself. Therefore S_1 is minimal forming.
Each leaf witness is unique, since deleting a leaf leaves both centres
active and no other outside vertex loses formation.

For r>=1 take r disjoint labelled blocks and add

    B_i -- D_(i+1),    i=1,...,r-1.                     (10)

Call the resulting graph G_r and put S_r=union S_i. The blocks are connected,
so G_r is connected. The edges (10) respect the displayed bipartition.
The graph has12r vertices and15r-1 edges; its maximum degree is four at
r=1 and five for r>=2. The added edges join originally omitted vertices,
so they change no selected neighbourhood, no formation test, or single
deletion witness for S_r. Thus S_r remains minimal with size8r and has
the same selected stars and isolates. Its4r leaf witnesses are still
unique, and they constitute every vertex outside S_r.

Every dissociation set contains at most two vertices from each of the
four disjoint three-vertex paths per block

    {x,a,A}, {y,c,C}, {p,B,b}, {q,D,d}.                  (11)

These paths partition all vertices, proving beta_2(G_r)<=8r. The union of

    {x,y,b,d,p,q,A,C}

over blocks is dissociation of size8r: its only edges in each block are
xb,yd,AC, and the added edges (10) touch no retained vertex. Hence
beta_2(G_r)=8r.

The auxiliary Q has6r vertices. The3r edges

    B_i p_i, D_i q_i, A_i C_i

form a perfect matching, so nu(Q)=3r. The vertices B_i,C_i,D_i over all
blocks are a vertex cover of size3r, even after adding (10). Since c=2r,
e=4r, formula (1) gives the exact value7r. It is attained by all4r leaves
and the vertices p_i,q_i,A_i, an independent set of Q. This proves (2).

Consequently the assertion

> Every minimal forming selection with selected star/edge/isolate components
> admits a dissociation set of at least its size retaining all its star leaves.

is false, with a deficit that grows linearly even in connected bipartite
graphs of bounded degree. For this family S_r union W=V(G_r) and the
witness choices are forced, so neither extra outside vertices nor alternative
witness choices repair the leaf-retention rule. A successful exchange must
drop some leaves. The displayed8r-set does so.

These graphs have pendant vertices and are not full rectangular grids.
They do not refute grid equality, or the more general still-open assertion
|S|<=beta_2(G) for minimal forming selections with selected star components.
No exact SF_2 value for this family is claimed here.

## Reproduction and status

Run the standalone standard-library checker with assertions enabled:

```sh
python3 scripts/check_star_leaf_budget.py
```

The general matching theorem and all-r family use the proofs above.
Finite controls compare literal formation, every single deletion and
dissociation maxima, all admissible witness assignments, matching/cover
duals and exact leaf-retaining optima. The exhaustive range covers5,399 labelled bipartite graphs and599,877
selected subsets, with40,024 admissible witness assignments. Every such
assignment is checked by both full restricted-subset enumeration and
independent-set enumeration, as well as matching/cover duality. Targeted
fixtures supply actual witness conflicts and failed sufficient criteria.
The6-by-6 control enumerates262,144 leaf-retaining candidate subsets.
Twenty-two disjoint/connected family controls use r=1,...,8,16,64,128,
reaching1,536 vertices, with3,904 single-deletion failures and1,952 unique
leaf witnesses checked. They verify the printed P_3 partition, perfect
matching, explicit cover/independent set and both attaining dissociation
sets. Exact coverage is recorded in `output/star-leaf-budget-check.json`.
The proof/source snapshot c15cbb4 received independent **ACCEPT**, with no
mathematical correction required. The reviewer reconstructed all three
attached files byte-for-byte and verified their manifest hashes, ran the
complete original checker unchanged with assertions enabled, and reproduced
the entire 50,622-byte report exactly. The complete response and execution
scope are in `output/star-leaf-budget-review.json`.
There is no new Lean verification or claim of worldwide priority.
