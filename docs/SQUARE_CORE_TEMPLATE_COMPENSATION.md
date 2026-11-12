# A compatible witness construction for square owner cores

12 November 2026. For every finite simple bipartite partial template with b
helpers, if its owner core has only isolated vertices, isolated edges and
four-cycles as connected components, we prove

    beta_2(H) >= 3b-floor(2t/3) >= ceil(8b/3),             (1)

where t is the number of core four-cycles. This gives a conditional 5/51 gap
bound for minimal two-star-forming sets in maximum-degree-three graphs.
The coefficient5/51 already holds for acyclic extracted cores by the earlier
core-cycle theorem. The new construction gives an additional sufficient
condition allowing four-cycles and an explicit integer structural surplus.
The general template question beta_2(H)>=ceil(8b/3) remains open.

## Template and construction

The disjoint layers I,X,C have orders b,2b,2b. Each helper has two witnesses,
each witness has one helper and one distinct owner, and owner:X->C is a
bijection. All other edges are a partial matching Q on X and a bipartite
maximum-degree-two core on C. These are the only template edges. Physical
bipartition colours distinguish helpers/owners from their witnesses. Auxiliary
P edges pair a helper's two witnesses; both endpoints have the same physical
colour. Q edges cross physical colours.

For every core square, pair its two owners on each physical side. Transport
these two pairs to witness pairs R via the owner bijection. Let U be all
witnesses whose owners lie in core squares. Build an auxiliary SIMPLE graph J
on U using the restrictions of P,Q and R. Parallel occurrences in P and R
are a single adjacency; no multigraph degree or capacity is counted twice.

J has maximum degree three: at most one edge of each type meets a vertex.
It has no triangle. A triangle crossing physical colours would need two Q
edges at one vertex, whereas Q is a matching. A triangle in a single physical
colour would lie in the union of the two matchings P and R. Such a union is
bipartite (its simple components are paths or even cycles) and has no triangle.

We use the following elementary independent-set fact with its full argument.

**Lemma.** Every finite simple triangle-free graph J of maximum degree three
has a polynomially constructible independent set Y of size at least |J|/3.

**Proof.** Start with an empty set and extend greedily to a maximal independent
set. If some y has two outside vertices a,b whose only neighbour in the set
is y, replace y by a,b and extend greedily again. Triangle-freeness makes a,b
nonadjacent, so the replacement is independent and strictly increases size.
At most |J| such exchanges occur. At termination every outside vertex has a
neighbour in Y, and each y has at most one outside vertex whose unique
Y-neighbour is y. Write B=V(J)-Y and B1 for those with one Y-neighbour. Then

    |B1|<=|Y|,
    2|B|<=e(Y,B)+|B1|<=3|Y|+|Y|=4|Y|.

Hence |J|<=3|Y|. Recomputing all neighbourhoods and scanning all vertices
at each step gives a direct polynomial implementation. The proof also covers
the empty graph. QED.

Apply the lemma to J, which has 4t vertices. Since Y is R-independent, its
owners contain at most one vertex from each R-pair. Extend those owners to
Z by choosing exactly one owner in each such pair. Then |Z|=2t. In each
square C-Z contains one owner of each physical colour, hence one edge. Keep
all nonsquare owners as well; their components are single vertices or edges.
The actual template set is

    D=I union (C-Z) union Y.

It is a dissociation set: the owners induce only edges and isolates; each
selected witness has its owner in Z, has no selected Q-mate, and pairs with
its helper. P-independence means at most one selected witness per helper.
No other incidences exist. All resources are simultaneous: each witness has
one helper and one owner; no helper or square-pair is used twice. Therefore

    |D|=b+(2b-2t)+|Y|
        >=3b-2t+ceil(4t/3)=3b-floor(2t/3).

As 4t<=2b, this proves (1). If t=0, the set I union C has size3b directly.
This construction does not fix an auxiliary phase or an owner physical side.

## Lifting to a minimal two-star-forming set

Fix the disjoint witness extraction from `UNRESTRICTED_SUBCUBIC_GAP_IMPROVEMENT.md`
and the general witness proof in `SHARP_BIPARTITE_STAR_FORMING_GAP.md`.
For completeness the ledger needed here is stated explicitly. For a minimal
set S in a finite simple bipartite graph G of maximum degree three, R consists
of selected isolates and selected isolated edges. Disjoint triples (c,ell,x)
use a selected centre, its selected leaf, and a private outside leaf witness;
p counts them. Each remaining selected nontrivial vertex has a distinct
outside witness, giving u owner-witness pairs. An assigned witness has at most
one other selected neighbour, necessarily a selected isolate. Let a count
isolates assigned one such witness, b those assigned at least two, and b3
those assigned three. The degree-two helper extraction has b'=b-b3 helpers
and 2b' distinct owners and witnesses.

The extracted template is induced on these layers. The retained set is all R
outside those helpers plus one selected leaf from each triple. It is a
dissociation set of size L=|R|-b'+p and has no edge to any template vertex.
Consequently (1) extends physically to G; it is not just a numerical sum of
incompatible candidates.

Suppose THIS extracted owner core has only P1,P2,C4 components. Put

    d=|S|-beta_2(G), m=min(a,p), alpha=a-m, pi=p-m,
    e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u,
    tau=m+b-2d, Z=3beta_2(G)-3L-8b'.

The fixed witness proof gives r,q,alpha,pi,tau,b3,e-b3>=0. The new construction
gives Z>=0, and more precisely

    Z>=b'-2t+3ceil(4t/3)-4t.                            (2)

Direct counting, without any extra geometric assumption, gives

    n=10d+m+r+3(alpha+pi)+2e+q+5tau,
    d+Z=5m+3(alpha+pi)+3e+5b3+tau.

Subtracting the second identity from five times the first proves the exact
certificate

    5n-51d = Z+5r+12(alpha+pi)+24tau
               +7(e-b3)+2b3+5q >=0.                   (3)

Thus |S|-beta_2(G)<=floor(5n/51), with the structural correction (2).
This applies to the particular S and extraction satisfying the condition.
It bounds SF_2(G)-beta_2(G) whenever a maximum-cardinality minimal S has such
an extraction. The condition concerns the actual extracted core: deleting
owners from a square can leave a P3, so a larger square-core presentation
does not by itself imply that a later extraction meets the condition. The unrestricted 7/71 bound remains applicable without the
condition. No sharpness or attaining construction is asserted for (1) or (3).

## Reproduction and scope

Run `python3 -B scripts/check_square_core_template.py`. The checker independently
scores every returned physical set, tests minimality with the local star
predicate, compares small templates against unrestricted dissociation optima,
and checks the lifting on all minimal sets of small graph controls.
Finite computations test implementation; the preceding arguments prove all
orders. The auxiliary independent-set lemma is an elementary local-exchange
bound, not a new general independence theorem. The template reduction and its
fixed-extraction consequence are the contributions here. This research note
uses existing checked witness results rather than making a new priority claim
for dissociation bounds. No new Lean execution is claimed.
