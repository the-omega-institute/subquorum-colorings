# Regular completion preserves minimality but can destroy a selected gap

Let beta_2 be the unrestricted dissociation number. A two-star-forming
set covers every vertex outside it by a non-induced K_(1,2) containing
exactly two selected vertices. Minimal means inclusion-minimal.

There are two conclusions. First, a simple degree-completion operation
preserves any minimal two-star-forming set, with no selected-component
restriction. Second, it does not preserve a positive selected gap:
an explicit all-scale family changes a connected subcubic graph with
selected gap k into a two-connected cubic graph whose specified selected
gap is at most -2k. This does not decide whether other cubic graphs admit
positive gaps in the selected-star/edge/isolate class.

## 1. A general regular-completion lemma

Fix an integer r>=2. Let G be a finite simple bipartite graph with parts
A,B, maximum degree at most r, and a minimal two-star-forming set S.
Suppose every vertex outside S already has degree r. Put

    D_A=sum_(v in S intersect A)(r-deg_G(v)),
    D_B=sum_(v in S intersect B)(r-deg_G(v)).

Choose a nonnegative integer p and add p disjoint selected edges, one
endpoint of each colour. Let P denote their 2p endpoints. Set

    u_A=(D_B+(r-1)p)/r,
    u_B=(D_A+(r-1)p)/r.                                  (1)

Assume these are nonnegative integers, and that each remaining selected
vertex degree deficit on side A is at most u_B and on side B at most u_A.
For a new selected endpoint the deficit is r-1. Add u_A new unselected
vertices on side A and u_B on side B. Join these only to S union P,
using the indicated deficits and giving every new unselected vertex
degree r. Such a simple incidence graph exists. The completed graph H
is r-regular and bipartite, and S'=S union P is minimal two-star-forming.
Moreover H[S'] is the disjoint union of G[S] and p new edges.

**Existence of the incidence graph.** On one side, let the selected
vertices' deficits be d_1,...,d_l, with sum r u and each d_j<=u, where u
is the number of new opposite-colour vertices. Number the latter modulo
u. Allocate to each selected vertex the next d_j consecutive positions
in the list 0,...,ru-1, reducing positions modulo u. No vertex receives
the same new neighbour twice because d_j<=u. Each new vertex occurs
exactly r times in the full list, so has degree r. If u=0 all deficits
are zero and no allocation is required. Apply this independently on
both colours. This is a construction, not a degree-sequence assumption.

**Suitable p always exists.** Since every old outside vertex is already
r-regular, cancelling the two colour degree sums gives

    D_A-D_B=r(|A|-|B|).

Thus both divisibility conditions in (1) are equivalent to
p congruent to D_A modulo r. Taking p in this residue class sufficiently
large makes u_A,u_B exceed every old deficit and r-1. The finite old
deficits are at most r. The constructed final colour classes are balanced,
as also follows from their positive regular degree.

**Formation and minimality.** For an old vertex, both its selected
neighbourhood and all adjacencies among selected neighbours are unchanged;
its new neighbours, if any, are unselected. This remains true after any
single old selected vertex is deleted. Each old outside vertex retains
its original covering star. Each new outside vertex has r>=2 selected
neighbours, hence is covered by a centred star. The new selected endpoints
need no coverage while selected. Therefore S' forms H.

For each old selected vertex v, retain an old vertex at which formation
fails after deleting v. Its selected-neighbour data are unchanged, so
it is still a failure witness in H. For a new selected endpoint v, after
its deletion its only remaining selected neighbour is its mate w. The
mate has no remaining selected neighbour. Thus v has neither two selected
neighbours nor a selected neighbour with another selected neighbour, and
fails formation itself. Every single deletion fails. Formation is upward
closed, so this proves inclusion-minimality. No assumption about beta_2
was used, and no beta_2 preservation follows from this lemma. QED.

## 2. A fixed core and its cubic completion

Use Q=Q_4+e from the
[compact subcubic construction](COMPACT_SUBCUBIC_SELECTED_STAR_GAPS.md).
Its vertices are 6j+t for 0<=j<8, 0<=t<6; write their positions as
(a_j,x_j,c_j,y_j,b_j,i_j). The selected vertices are x_j,c_j,y_j,i_j.
There is the six-vertex path in each block. Within each group h=0,4,
add a_(h+t)--b_(h+t+1) for t=0,1,2, and add
 a_(h+3)--a_h and a_(h+3)--a_(h+2). Add b_0--b_4 and the port
 e=a_1--a_5, which in numerical coordinates is 6--30.
The bipartition colour of 6j+t is (j mod2) XOR floor(j/4) XOR (t mod2).

The preceding all-even-L proof establishes

    |V(Q)|=48, |S|=32, beta_2(Q)=beta_2(Q-e)=31.          (2)

For clarity, the cap is independent of the port e. A dissociation set
has at most four vertices in each of the eight disjoint P6 blocks. At
32 vertices every block is full and can be normalized to
A_j={a_j,c_j,y_j,i_j} or B_j={x_j,c_j,b_j,i_j}, without adding an
external contact at a_j or b_j. Each a_j--b_(j+1) imposes
A_j=>A_(j+1). An A root would force a whole group to A, leaving the
terminal a with two selected a-neighbours. Thus both roots are B,
contradicting the edge b_0--b_4 between two saturated b-vertices.
The explicit 31-set uses A in the first group, B in the second, and
omits a_3. It avoids a_5=30, so works with or without e. This proves (2).
The normalization and full-block argument are detailed in the cited note.
Also Q-e is connected: its two body cycles are joined by the root path
through b_0--b_4, and the other path vertices attach to these bodies.

All 16 vertices outside S already have degree three. The selected degree
deficits are D_A=D_B=20. Set r=3 and p=2 in the completion lemma. Add
selected edges 48--49 and 50--51, with 48,50 of colour zero. There are
u_A=u_B=8 new unselected vertices. The following explicit legal incidence
choice gives a completed graph H. The old 48-vertex induced graph is Q;
there are no other edges besides those just specified.

| New unselected vertex | Its three selected neighbours |
| --- | --- |
| 52 | 7,27,44 |
| 53 | 9,11,29 |
| 54 | 11,14,48 |
| 55 | 25,41,48 |
| 56 | 29,39,41 |
| 57 | 2,23,50 |
| 58 | 21,37,50 |
| 59 | 19,23,32 |
| 60 | 17,33,49 |
| 61 | 5,38,43 |
| 62 | 26,35,47 |
| 63 | 17,47,49 |
| 64 | 1,31,51 |
| 65 | 5,13,15 |
| 66 | 3,45,51 |
| 67 | 8,20,35 |

Each old deficit is filled exactly, and each listed row has three
same-colour selected neighbours. Consequently H is simple cubic
bipartite. Its selected set S'=S union {48,49,50,51} has size36 and
induces eight P3's, eight isolates and two edges. The completion lemma
proves minimality. H-e is connected: Q-e is connected, every new outside
vertex touches an old selected vertex, and every new selected endpoint
has one of these outside neighbours.

Here is an actual dissociation set, not an optimization output:

    D={1,2,4,5,7,8,10,13,15,16,18,19,22,23,24,25,27,29,30,
       31,33,35,36,38,39,41,43,44,46,48,51,53,54,58,60,62,63,66}.

It has 38 vertices; direct inspection of the stated edges gives at most
one retained neighbour at every one of them. In particular 6 is absent.
Thus beta_2(H)>=38, whereas |S'|=36. No exact value of beta_2(H) is
needed or claimed. The originally positive selected gap 32-31=1 has
become at most 36-38=-2.

## 3. An all-scale connected obstruction

For every integer k>=1, take k labelled copies Q_j and H_j. In each
remove its port 6_j--30_j, and insert 30_j--6_(j+1), indices modulo k.
Call the resulting graphs G_k and K_k. The new edges have two endpoints
outside either specified selection. For k=1 the old edge is restored.
For k>=2 all edges are simple, preserve the bipartition and all degrees.
Both deleted-port pieces are connected, so the graphs are connected.

The original selected sets S_k have size32k and are still minimal:
outside-to-outside switching changes no selected-neighbour data, including
after one deletion. Every dissociation set restricts to at most31 vertices
in each Q_j-e by (2). Conversely the explicit 31-set above omits port30
and therefore lifts to every copy without activating a new induced edge.
Hence

    |V(G_k)|=48k, |S_k|=32k, beta_2(G_k)=31k.            (3)

The completed selections T_k have size36k and remain minimal by the same
argument. K_k is exactly a degree completion of G_k of the form in
Section1: all new edges other than the selected matching meet new
outside vertices and old or new selected vertices. The displayed38-set
omits port6, so its union over the copies remains dissociation. Therefore

    |V(K_k)|=68k, |T_k|=36k, beta_2(K_k)>=38k,
    |T_k|-beta_2(K_k)<=-2k.                             (4)

Every connected r-regular bipartite graph with r>=2 has no cutvertex.
Indeed, if deleting a colour-A vertex v gave multiple components C,
let t_C>=1 count their old edges to v. Cancelling internal degrees gives
r(|C intersect B|-|C intersect A|)=t_C. Every t_C is a positive multiple
of r, but their sum is only r, a contradiction. Thus K_k is two-connected.
For k>=2 its connectivity is exactly two: deleting vertices6,30 of one
copy separates the remaining vertices of that copy from all others.
There is no assertion of exact connectivity of K_1 here.

Equations (3)-(4) are an all-k obstruction to inferring gap preservation
from minimality-preserving degree completion. They are not a positive
cubic gap family, a nonexistence theorem for all cubic selected-star
sets, or a statement about exact unrestricted SF_2 values.

## Verification and provenance

Run `python3 -B scripts/check_cubic_completion_gap_loss.py`. The checker
uses literal formation and deletion conditions, checks the fixed38-set
against every actual edge, independently optimizes only the two old
48-vertex core models, and verifies the cyclic embeddings, degrees,
selected components and stated connectivity controls. General degree
completion is tested on small actual graphs and at target degrees2..6.
It never reports an interrupted cubic optimization as an exact answer.

The fixed completion was found while investigating the separate cubic
positive-gap existence question. In240 seeded completions, literal
witnesses of size at least36 reject every sample; those finite experiments
do not imply that all completions or all cubic graphs fail. The published
obstruction instead uses only one explicit fixed graph and a complete
all-k proof. The previous exact cyclic-composition and core-cap results
are reused with their original hypotheses. No new Lean claim is made.
