# Two-connected subcubic graphs with positive selected-star gaps

For every positive integer k there is a finite simple bipartite graph H_k
and a specified inclusion-minimal two-star-forming set S_k such that

    |V(H_k)|=90k, |S_k|=56k, beta_2(H_k)=55k,
    delta(H_k)=kappa(H_k)=2, Delta(H_k)=3.

The selected subgraph consists of 12k copies of P_3 and 20k isolates.
Thus the selected gap is exactly k=|V(H_k)|/90. In particular, positive
linear gaps in this selected-component class survive both the removal of
pendant vertices and the restriction to maximum degree three. This does
not determine the optimal coefficient for that class or the exact
unrestricted value of SF_2(H_k). Since S_k is minimal, it does imply
SF_2(H_k)-beta_2(H_k)>=k.

Here beta_2 denotes the maximum size of a vertex set inducing maximum
degree at most one. A set S is two-star-forming when every vertex outside
S belongs to a copy of K_(1,2) with exactly two vertices in S; the copy
need not be induced. Minimality is with respect to inclusion, as in
R. Sahbi, *Upper k-Star-Forming Sets, k-Independence, and Upper
Domination*, arXiv:2610.03785. The construction addresses the degree and
connectivity question suggested by Sahbi in correspondence, 5 November
2026. The previously established general bipartite n/10 bound and the
smaller selected-star upper bounds have different scopes from the lower
family here.

## A sixty-vertex core

For j=0,...,9 take the disjoint paths

    a_j - x_j - c_j - y_j - b_j - i_j.

For each h in {0,5}, add the six edges

    a_h b_(h+1), a_h b_(h+2),
    a_(h+1) b_(h+3), a_(h+1) b_(h+4),
    a_(h+2) a_(h+3), a_(h+2) a_(h+4).

Add b_0 b_5. Call this graph Q. Its specified selection contains
x_j,c_j,y_j,i_j for every j and has size 40.

**Lemma 1.** beta_2(Q)=39.

**Proof.** A dissociation set contains at most four vertices of each
P_6. The six possible four-vertex sets, using the path indices 0,...,5,
are

    0134, 0135, 0145, 0235, 0245, 1245.

If a is present, replace the local set by A={a,c,y,i}=0235; otherwise
the set is already B={x,c,b,i}=1245. Each replacement retains only a
subset of the old interface vertices {a,b}, and weakly decreases their
induced internal degrees. These are the only vertices with neighbours
in other blocks of Q. Consequently the replacements preserve the
dissociation condition in Q. This normalization is used only on Q,
before adjoining any attachments.

Suppose a set had size 40. Normalize every block as above. An edge
a_u b_v forbids state A at u and state B at v: b_v already has its
selected neighbour i_v. Thus state A at h forces A at h+1 and h+2,
and then A at h+3 and h+4. But a_(h+2) would then have two selected
neighbours a_(h+3),a_(h+4), which is impossible. Each of blocks 0 and
5 therefore has state B. The edge b_0 b_5 now violates the already
saturated degree of both its endpoints. This rules out size 40.

For attainment, use A on blocks 0,...,4 and B on blocks 5,...,9,
then omit a_3. Inside the first group the only remaining interface
edge is a_2 a_4, whose endpoints are internally isolated. The second
group retains no a vertex, and b_0 is absent. All other retained
edges belong to the local matchings. This is a 39-vertex dissociation
set D_Q. The upper and lower bounds agree. QED.

## Removing all pendant vertices

For each of the four pairs

    (1,8), (2,9), (3,6), (4,7),

take a fresh cycle z_0 z_1 z_2 z_3 z_0, add i_j z_1 and i_l z_3
for its pair (j,l), and select z_0,z_2. Distinct pairs have disjoint
cycles. For each j in {0,5}, take a fresh seven-vertex attachment

    a'_j - x'_j - c'_j - y'_j - b'_j - i'_j,
    u'_j y'_j, u'_j i'_j, u'_j i_j.

Select x'_j,c'_j,y'_j,i'_j. Finally add a'_0 a'_5. This defines H
on 60+16+14=90 vertices and its 56-vertex selection S.

Bipartiteness can be read directly from the following colouring. The
colours of a_0,...,a_9 are

    (0,1,1,0,0, 1,0,0,1,1).

Alternate along each path. On a square for (j,l), give z_0,z_2 the
colour of i_j=i_l. In the attachment at j give a'_j the colour of
a_j and alternate along the path, with u'_j the colour of a'_j.
Every listed edge has opposite colours at its ends. The four square
pairs go between the two groups of five; pairing within each group
instead would leave cut vertices and is not the construction here.

All former pendant i_j gain one neighbour. Each square has two
vertices of degree two and two of degree three. In a seven-vertex
attachment, u'_j and y'_j have degree three, and a'_j gains its
second neighbour through a'_0 a'_5. All remaining degrees are two
or three. Hence delta(H)=2 and Delta(H)=3.

**Lemma 2.** S is inclusion-minimal two-star-forming, and beta_2(H)=55.

**Proof.** Every outside vertex a or a' has its selected neighbour x
or x', which is paired with its selected centre. Each outside b or b'
similarly has the selected edge y-c or y'-c'. A square's outside
vertices z_1,z_3 have the two selected neighbours z_0,z_2. Each u'
has the selected edge y'-c'. This proves formation by explicit stars.

For deletion minimality, a selected isolate fails formation at the
deleted vertex itself. If x is removed, its outside witness a loses
its only selected neighbour. If y is removed, b has only its isolated
selected neighbour i, which cannot complete a star. If c is removed,
a has only x, now isolated. The same witnesses apply in the two
seven-vertex attachments. These cases cover all selected vertices;
the square selections are isolates. Failure after every single
deletion proves inclusion minimality: the forming property is
upward closed, since every vertex outside a larger selection
already has its required star in any smaller forming selection.
Thus a proper forming subset would imply a forming single deletion.

For the upper bound, restrict an arbitrary dissociation set to the
vertex-disjoint core Q, the four squares, and the two seven-vertex
attachments. Their bounds are respectively 39, 2 each, and 4 each.
The last bound follows by partitioning the attachment into the
P_3 on {a',x',c'} and the C_4 on {y',b',i',u'}, each contributing
at most two. Cross edges can only impose more restrictions. Thus

    beta_2(H)<=39+4*2+2*4=55.

For the reverse bound, use D_Q, both z_0,z_2 on every square, and
{a',c',y',i'} on each seven-vertex attachment. The u' and square
attachment vertices adjoining Q are omitted. The two retained a'
vertices were internally isolated, so their joining edge causes
no violation. This gives 55 vertices and proves equality. QED.

## Two-connectivity and the cyclic construction

The following explicit open ear decomposition supplies a short
certificate of two-connectivity of H. Number a_j,x_j,c_j,y_j,b_j,i_j
as 6j,...,6j+5. Number the squares 60,...,75 in the displayed pair
order, and the two attachments 76,...,82 and 83,...,89 in the
order a',x',c',y',b',i',u'. The first row is a cycle; every later
row is a path whose distinct endpoints already occur and whose
internal vertices are new.

```
0 10 9 8 7 6 22 23 69 68 71 41 40 30 31 32 33 34 4 3 2 1 0
69 70 71
6 28 29 73 72 75 47 46 30
73 74 75
0 16 15 14 13 12 18 19 20 21 22
12 24 25 26 27 28
10 11 61 60 63 53 52 36 37 38 39 40
61 62 63
16 17 65 64 67 59 58 36
65 66 67
46 45 44 43 42 48 49 50 51 52
42 54 55 56 57 58
4 5 82 79 78 77 76 83 84 85 86 89 35 34
79 80 81 82
86 87 88 89
```

All 90 vertices occur. A cycle is two-connected, and adjoining an
open ear preserves two-connectivity: after deleting an old vertex,
the old remainder is connected and any surviving ear segments
attach to it; after deleting an internal ear vertex, its two
segments attach to the connected old graph. Induction proves that
the displayed spanning subgraph, and hence H, is two-connected.

Delete the edge e=a'_0 a'_5 and take k copies of H-e. For each copy
j add the edge from its a'_5 to a'_0 in copy j+1, with indices modulo
k. This defines H_k and S_k; for k=1 it restores H.

The same block partition proves beta_2(H_k)<=55k, since e was not
used in any upper-bound part. The union of the previous attaining
sets still works: after deleting e its two endpoints are isolated
in each attaining set, and the new edges give each such endpoint
exactly one neighbour. Thus beta_2(H_k)=55k. All changed edges have
both endpoints outside S_k, so the formation and deletion witnesses
are unchanged. The colouring and degrees also survive.

For completeness, cyclic edge substitution preserves
two-connectivity for any two-connected graph H and edge uv. H-uv
is connected. After deleting a vertex z in one copy, every component
of (H-uv)-z contains u or v when they survive: otherwise that
component would already be separated in H-z. If z is an endpoint,
the affected copy is connected to the other endpoint because H-z
is connected. If neither endpoint is deleted, the other k-1 copies
and the new links give an external u-v path, joining all components
of the affected copy. Hence the whole remainder is connected.
For k=1 use the established property of H. Since degree-two
vertices remain, kappa(H_k)=2. This finishes the theorem.

## Verification scope

Run `python3 -B scripts/check_subcubic_selected_stars.py`. It verifies
the six normalization cases, all 32 five-block and 1,024 ten-block
normalized states, and independently computes beta_2(Q)=39 by exact
branching. It also enumerates all physical subsets of each attachment,
validates the displayed spanning ears, and checks literal formation,
all single deletions of S, attaining sets, degrees, colours and all
single-vertex cuts for k=1,2,3,5,8,13. The arbitrary-k conclusions
follow from the proofs above. The checker does not run an exact
unrestricted whole-H_k optimizer or assert an exact SF_2 value.
