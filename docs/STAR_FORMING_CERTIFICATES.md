# An elementary global certificate bound for 2-star-forming sets

Let G be a finite simple graph. A set S is 2-star-forming when every x outside
S belongs to a three-vertex path in G[S union {x}]. Paths need not be induced.
Minimal means inclusion-minimal. Write SF_2(G) for the largest cardinality
of a minimal such set, and beta_2(G) for the dissociation number.

For s in a minimal S, a certificate is a vertex x outside S\{s} that lies
on no three-vertex path in G[(S\{s}) union {x}]. If d_S(s)>=2, then x cannot
be s, since s itself lies on such a path centered at s in G[S]. Thus every
high-degree vertex has a certificate outside S.

**Lemma 1 (global injectivity).** In any graph, an outside vertex cannot be
a certificate for two distinct vertices s,t of S with d_S(s),d_S(t)>=2.

**Proof.** Suppose x certifies both. Since S is star-forming, there is a
three-vertex path containing x in G[S union {x}]. Every such path must contain
s and t, since deletion of either destroys all paths containing x. Its vertex
set is therefore {x,s,t}, so x is adjacent to at least one of s,t, say s.
Since d_S(s)>=2, s has a neighbor y in S distinct from t. The path x,s,y
avoids t, contradicting x's certification of t. QED.

This proof uses neither bipartiteness nor triangle-freeness. In particular,
the certificate sets of all high-degree vertices are pairwise disjoint, not
just those of one bipartition class.

**Corollary 2.** Put H={s in S:d_S(s)>=2}. Then

    |H|<=|V\S|,
    |S|<=floor((|V|+beta_2(G))/2),
    SF_2(G)<=floor((|V|+beta_2(G))/2).

**Proof.** Choose one certificate for each member of H. Lemma 1 makes this
an injection into V\S. The set S\H is a dissociation set, because its vertices
already had degree at most one in G[S]. Consequently

    2|S|-|V| <= |S|-|H| = |S\H| <= beta_2(G).

Taking the maximum over minimal S proves the final statement. QED.

The cardinality bound does not prove SF_2=beta_2. Replacing H by its certificates
can create new three-vertex paths among the inserted vertices or at a retained
vertex. Injectivity gives distinct inserted vertices; it does not bound their
degrees in the exchanged set.

## The coloring comparison requires a narrower graph class

Let D be the six-vertex double star with adjacent centers u,v, leaves a,b at
u, and leaves c,d at v. It is a bipartite tree. Its parameter values are

    beta_2(D)=SF_2(D)=4 < 5=psi_sq(D).

The dissociation and coloring values have the direct proof in
[the structural section](../manuscript/paper.tex): the four leaves form a
maximum dissociation set; coloring the two centers together and the four
leaves separately gives five colors, and six distinct colors fail at a center.

For SF_2, the four leaves are a minimal star-forming set. Each outside center
is the center of a path through two leaves. Removing any leaf fails: when
added back to the other three leaves it lies on no three-vertex path.
Every five-set contains a four-set that is still star-forming. If the omitted
vertex is a center, delete the remaining center to obtain the four leaves.
If the omitted vertex is a leaf at u, delete v. The resulting set is
{u,b,c,d}, up to symmetry: the omitted leaf participates in a path through
u and b, and v participates in one through c and d. The full vertex set
is not minimal either. Thus SF_2=4.

Accordingly psi_sq<=SF_2 fails for the classes of all bipartite graphs and
all triangle-free graphs. A rectangular-grid comparison requires a separate
proof even if SF_2=beta_2 has been established on that class.

## Verification

`python3 develop/check_star_forming_certificates.py --output
develop/results/star-forming-certificates-2026-09-30.json` checks the certificate
bound on all labelled graphs through five vertices and evaluates the double
star. The all-graph proof is Lemma 1, not the finite enumeration. This note
records consequences of the definition; the established general lower
comparison beta_2<=SF_2 is due to Chellali and Favaron's work on k-star-forming
sets (2009).
