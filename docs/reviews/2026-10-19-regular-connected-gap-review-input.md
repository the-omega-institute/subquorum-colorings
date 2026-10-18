Audit this new broken-block and connected-ring theorem for every integer degree d>=4 and any number of blocks. Check the dissociation cap after deleting the outside port edge, the small degree-four boundary cases, the cubic counterexample, and two-connectivity after every vertex deletion. Treat the universal inequality (2d+1)SF_2<=dn+2beta_2 as an explicit hypothesis here; its proof is under separate review. Verify the connected-family consequences given that hypothesis. Return ACCEPT/REVISE/REJECT with any exact mathematical gap. Finite controls are not the proof.

Base construction:

Fix d>=3. Take independent classes A={a_i}, B={b_i}, X={x_i}, Y={y_i},
each indexed by i modulo d, and vertices p,q. The bipartition is

    L=A union X union {p},  R=B union Y union {q}.

Add all a_i--b_j with i!=j; add a_i--y_i and b_i--x_i; join p to all
Y and q to all X. Finally add x_i--y_j precisely when

    j-i is not congruent to1or2 modulo d.

The outside X--Y graph is(d-2)-regular and contains every x_i--y_i.
Thus G_d is simple, bipartite and d-regular of order4d+2.
The set S=A union B union {p,q} has size2d+2. Each outside vertex has
two selected neighbors, its high matching neighbor and one isolate.
Deleting a_i uncovers y_i, deleting b_i uncovers x_i, and deleting
p or q uncovers the deleted isolate itself. Hence S is minimal forming.
The degree-capacity bound gives

    SF_2 <= floor(d(4d+2)/(2d-1))=2d+2,

since d(4d+2)=(2d-1)(2d+2)+2 and2<2d-1. Thus SF_2=2d+2.

The high crown graph G[A union B] is two-connected. One explicit
Hamilton cycle alternates a_i,b_(i+2),a_(i+1), with indices modulo d.
Both adjacent high indices differ because d>=3. Adding each internally disjoint
path a_i--y_i--x_i--b_i preserves two-connectivity, as does adding p
and q, each with at least two neighbors already present. The remaining
edges also preserve it. This proves two-connectivity without computation.



# Arbitrarily large two-connected sharp gaps in every degree at least four

19 October 2026. The general-degree exchange theorem and the uniform
G_d construction are proved in SHARP_REGULAR_BIPARTITE_GAP.md.
This continuation proves that its sharp gap coefficient is attained
by arbitrarily large two-connected graphs in every degree d>=4.
It also identifies why the same port argument fails at d=3.

## Theorem

For every d>=4 and r>=1 there is a finite simple two-connected
d-regular bipartite graph J_(d,r) satisfying

    n=(4d+2)r,
    beta_2(J_(d,r))=(2d+1)r,
    SF_2(J_(d,r))=(2d+2)r,
    SF_2-beta_2=r=n/(4d+2).

Thus the universal coefficient1/(4d+2) remains sharp under
two-connectivity, even along unbounded orders and unbounded gaps.
This does not settle the corresponding asymptotic cubic problem.

## Deleting an outside edge preserves the local cap for d>=4

Use the classes A,B,X,Y and p,q of G_d. Let B_d be obtained by deleting
the edge x_0--y_0. Its two ports have degree d-1 and all other vertices
degree d. We prove

    beta_2(B_d)=2d+1  for every d>=4.                       (1)

The independent bipartition part gives the lower bound. For the upper
bound take any dissociation set D and use the counts a,b,x,y,epsilon,eta
from the preceding proof. The high crown and high-to-port matching edges
are unchanged. Thus if a,b>0, then a,b<=2; if a=b=2 then x,y<=d-2.
The constraints epsilon=1 implies y<=1 and eta=1 implies x<=1 also
remain valid.

Only x_0,y_0 now have three nonneighbors in the opposite outside class;
every other outside vertex still has two. If x,y>0 and y>=4, every
selected X vertex must be x_0, so x=1 and y<=4. Moreover y=4 forces
at least one chosen Y neighbor of x_0. The isolate p cannot be selected
because y=4, and q cannot be selected because x_0 already has a selected
Y neighbor. Hence in this case x+y+epsilon+eta=5. The symmetric
statement holds if x>=4. In all remaining mixed-outside cases x,y<=3,
and the old isolate constraints show

    x+y+epsilon+eta<=6,

with equality only at x=y=3, epsilon=eta=0. This is exactly the aggregate
bound used by the preceding proof. Notice that it is proved after the
edge deletion, rather than inferred from the intact graph.

For d>=5, the earlier count cases now apply verbatim: mixed high classes
contribute at most four, a single high class at most d, and mixed outside
classes with isolates at most six. Thus their totals are at most10 or
d+6, respectively, both at most2d+1. With at most one outside class,
the previous isolate and matching-port counts are unchanged and give
the same upper bound. With no high class the bound is immediate.

For d=4, mixed high and outside classes could have size ten only when
a=b=2 and x=y=3 without isolates, contradicting the unchanged matching
restriction x,y<=2. With exactly one high class and mixed outside
classes, size ten would require all four vertices in that high class
and x=y=3, again without isolates. Assume the high class is A. Each
selected Y already has its A partner, so no selected X--Y edge is
permitted. But among three selected X vertices at least two differ
from x_0. Each has only two nonneighbors among Y and therefore meets
the three chosen Y vertices, a contradiction. Interchanging the sides
covers high class B. If at most one outside class is present, the old
bound is9 when a+b<=3 and8 when a=b=2. With no high class it is at
most six. This proves(1) for every d>=4.

This local bound applies to the restriction of any dissociation set in
an arbitrary surrounding graph, since internal edges of B_d remain.
There is no interface compensation to charge and no shared remainder.

## Joining any number of blocks

Take r disjoint copies of B_d. Add x_0^(i)--y_0^(i+1) for indices modulo r.
For r=1 this restores G_d. For r>=2 the new edges join different blocks,
so simplicity is preserved. Degrees become d and the displayed
bipartitions are compatible. This defines J_(d,r).

Every dissociation set restricts to at most2d+1 vertices in each B_d,
by(1), giving beta_2<=r(2d+1). A whole part is independent of exactly
that size, so equality holds.

Let S be the union of A,B,p,q in every block. All modified edges have
both endpoints outside S. The covering condition of S and every
single-deletion sub-selection depends only on edges with at least one
selected endpoint, so these changes preserve formation and minimality.
Equivalently, the displayed high-to-port and isolate deletion witnesses
survive literally. Thus SF_2>=r(2d+2). Apply the general regular
compensation theorem using the exact beta value:

    (2d+1)SF_2 <= dn+2 beta_2
      = (2d+1)(2d+2)r.

This proves the exact SF value and gap. The local dissociation cap is
summed once per disjoint block; cross edges can only decrease feasible
dissociation selections and cannot create a hidden additional budget.

## Two-connectivity of the ring

The intact G_d is two-connected by the crown-and-ears proof. Hence B_d
is connected: a two-connected graph has no bridge. The ring is connected.

Delete one vertex v. Blocks not containing v remain connected. If v is
a port of its block, that block with v deleted is exactly G_d with v
deleted, hence connected, and it attaches to the rest of the ring via
the surviving port. The other blocks form a connected path between
the two neighbors of the affected block; for r=2 the other block itself
is that path. If v is not a port, restoring x_0--y_0 in the affected
block gives G_d-v, which is connected. Consequently B_d-v is either
connected or has exactly two components, one containing each port:
one added edge can connect only these two endpoint components. The
rest of the ring connects those ports, so every component lies in
the same connected graph. Thus deletion of any vertex leaves the
ring connected. For r=1 use the intact G_d. This proves two-connectivity.

## The cubic obstruction is an actual local-cap failure

At d=3 the outside graph of G_3 is just the identity matching.
Deleting x_0--y_0 admits the dissociation set

    A union Y union {x_0,q},

of size eight. It consists of the three matching edges a_i--y_i and
the edge x_0--q. The whole graph B_3 has maximum degree three, and
the exact dissociation deficiency bound from CUBIC_STABILITY_PORTS.md
gives5|D|<=3*14-2+2*2=44; thus beta_2(B_3)<=8. Therefore

    beta_2(B_3)=8 > 7=beta_2(G_3).

The failure is the proposed seven-vertex local cap after deletion.
It does not refute the global cubic gap inequality or decide whether
a different cubic construction attains its coefficient at unbounded
connected orders. A port-specific or cross-block restriction is needed
in the cubic case; the earlier Heawood compensation family supplies
such restrictions but only a smaller asymptotic gap coefficient.

## Verification scope

The proofs above are general and do not use finite enumeration. The
companion controls independently inspect broken blocks and connected
examples, with exact finite optima where recorded. The already submitted
general-degree Oracle input predates this continuation, so its verdict
does not cover this ring or broken-block lemma unless a separate review
explicitly says so. This note is not a claim of full Lean graph formalization.
