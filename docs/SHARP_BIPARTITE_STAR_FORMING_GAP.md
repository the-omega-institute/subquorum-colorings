# A sharp gap bound for every bipartite graph

11 November 2026. This is a new general theorem, beyond the regular-graph
bounds already in the archive. The initial Oracle argument was reconstructed
with the chosen leaves explicitly excluded from the remaining-vertex count.
The proof below does not rely on finite enumeration.

All graphs are finite and simple. A two-star-forming set S covers each x
outside S by a not necessarily induced K1,2 in G[S union {x}]. SF2 is the
maximum cardinality of an inclusion-minimal such set. A dissociation set
induces maximum degree at most one, and beta2 is its maximum cardinality.

**Theorem.** Every finite simple bipartite graph G of order n satisfies

    SF2(G) - beta2(G) <= floor(n/10).                              (1)

The constant is attained by the ten-vertex graph H and by the arbitrary
four-attachment compositions described in `FOUR_PORT_STAR_FORMING_COMPOSITION.md`.
In particular it is sharp among two-connected bipartite graphs of minimum
degree two and maximum degree four, at unbounded orders.

## Witness classification and disjoint resources

Fix an inclusion-minimal two-star-forming S. Let R consist of the selected
vertices in components of G[S] of order one or two, and put C=S minus R.
Let I be the selected isolates. Every v in C lies in a three-vertex path
of G[S], so the newly omitted v is still covered after deleting v. Minimality
therefore gives a failing vertex x outside the original S. Its neighborhood
in S has one of these forms:

1. N_S(x)={v};
2. N_S(x)={v,i}, where i belongs to I;
3. N_S(x)={ell}, where N_S(ell)={v}.

For the first two forms, x is adjacent to v. It can have at most one
other selected neighbor i. If present, i is isolated after deleting v;
i and v are in the same bipartition class, so i was already isolated in S.
For the third form, x is not adjacent to v. Its selected neighbors do not
change, so it can lose formation only when it has a unique selected neighbor
ell and that neighbor loses its last selected neighbor v.

For each c in C that admits a witness of form 3, choose one triple
(c,ell_c,x_c). Let p be the number of chosen centers. Such a c has selected
degree at least two, since it belongs to C and is adjacent to a selected leaf.
Each ell_c is a selected leaf with unique selected neighbor c; consequently
different centers have different chosen leaves and no chosen leaf is a center.
The outside witnesses x_c are distinct because each has its own unique
selected neighbor ell_c. Thus the triples are vertex-disjoint.

Remove BOTH the chosen centers and their chosen leaves from C. For each
remaining v choose a witness x_v of form 1 or 2, and let u count these
remaining vertices. Such a witness exists because every center admitting
form 3 has been removed. Each x_v has exactly one neighbor in C, namely v;
these witnesses are distinct from one another and from all x_c. In particular,

    |S| = |R| + 2p + u.                                         (2)

For an isolate i in I, let h(i) count the chosen witnesses x_v adjacent
to i. Let a count the isolates with h(i)=1 and b those with h(i)>=2.
Each x_v has at most one isolate neighbor, so

    u >= a + 2b.                                                (3)

The p triples, the u pairs (v,x_v), and the a+b touched isolates are
mutually disjoint. Counting these vertices once gives

    n >= 3p + 2u + a + b >= 3p + 3a + 5b.                       (4)

## Two dissociation constructions

Fix a bipartition (A,B). In each construction below also exchange A and B
and average the two sizes. No balancing of the bipartition is assumed.

For the first construction, retain all R except touched isolates in A.
From a triple (c,ell_c,x_c), select c,ell_c if c belongs to A, and ell_c,x_c
if c belongs to B. From a remaining pair (v,x_v), select both if v belongs
to A and neither otherwise. Call the resulting set D_A.

Every outside witness actually selected into D_A lies in B. A triple witness sees only its
chosen leaf in S; a pair witness sees its chosen v and at most one touched
isolate in A, which was removed. The only selected C vertices in B are
chosen leaves whose unique selected neighbor is their own center. The
retained components of G[S] of order two have no edges to C, and outside
witnesses have no neighbors in those components. All selected vertices
therefore have degree at most one in G[D_A]. Thus D_A is a dissociation set.

Each triple contributes two vertices in each orientation; each pair
contributes two in one orientation and zero in the other; each touched
isolate is removed once. Using (2),

    beta2(G) >= (|D_A|+|D_B|)/2 = |S|-(a+b)/2.                  (5)

For the second construction, put T=S union {all chosen outside witnesses}.
Select all of T intersect A, together with R intersect B except the
isolates with h(i)>=2. Call this set E_A.

A retained vertex in R intersect B from a two-vertex component sees only
its selected mate: no chosen outside witness meets such a component. A
retained isolate in R intersect B sees at most one chosen witness. On the
A side, a selected vertex of S sees at most one vertex of R intersect B,
while a chosen outside witness sees at most one such isolate. There are no
edges within either bipartition class. Thus E_A is also a dissociation set.

Now |T|=|S|+p+u, and precisely b isolates are removed once across the
two orientations. Equation (2) gives

    beta2(G) >= (|E_A|+|E_B|)/2
             = (|T|+|R|-b)/2 = |S|-(p+b)/2.                   (6)

Combining (4)--(6),

    10(|S|-beta2(G))
      <= 5 min(a,p) + 5b
      <= 3a+3p+5b
      <= n.                                                    (7)

For the middle inequality, if a<=p then 3a+3p-5a=3p-2a>=0;
the other case is symmetric. Choose S of cardinality SF2(G) and take
the integer part to prove (1).

The witnesses used in the two constructions need not be disjoint between
the constructions: these are alternative dissociation sets, not resources
spent simultaneously. Within either construction and in (4), all allocated
triples, pairs and isolates have the explicit disjointness proved above.

## A necessary condition for equality

Suppose SF2(G)-beta2(G)=n/10>0, and use a maximizing S above. Every
inequality in (7) and (4) is then an equality. Equality in
5 min(a,p)<=3a+3p forces a=p=0. Thus u=2b and n=5b. All vertices outside
S are the u pair witnesses, and R consists exactly of the b touched
isolates. Every one of these isolates meets exactly two pair witnesses;
it has no selected neighbor. Its degree in the whole graph is therefore
exactly two. Consequently every positive equality graph has at least n/5
vertices of degree two. This is a necessary condition, not a complete
classification of equality graphs or of floor(n/10) attainment when
10 does not divide n.

## Verification and attribution

The all-graph theorem has the written proof above. The accompanying
`scripts/check_bipartite_gap.cpp` independently enumerates all selected
sets of its finite graph models, reconstructs the witnesses for every
minimal set, checks the two dissociation sets in both orientations, and
checks every equality and inequality used above. The separate four-port
verifier checks the attaining constructions.

This proof is not covered by the older Lean files for the two-attachment
construction or by the arithmetic audits for regular graphs. Any fresh
independent review must identify this theorem and this exact proof.
