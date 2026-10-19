# Private clauses and exact boundary ownership

## Purpose and status

The [sharp omission theorem](LONG_CORE_SHARP_OMISSION.md) determines
beta_2(L_k), while exact SF_2(L_k) remains open for k>=8. This note
gives a general graph-level certificate reduction and an attachment
lemma for that next step. It also exhibits an all-length obstruction
to an overly restrictive robust-deletion rule. It does not claim a
new exact SF value or an improved asymptotic gap coefficient.

The reduction to private clauses is an elementary reformulation used
here as a research tool; no priority or new complexity result is claimed.
The boundary lemma makes the location and ownership of any extra
minimality certificate explicit.

## Exact clauses for star formation

For every vertex u of a finite simple graph G, define

    A_u = {u} union N(u).

For each oriented edge uv define

    B_(u,v) = {u} union (N(u) minus {v}) union (N(v) minus {u}).

Let H(G) be this family of vertex sets, removing duplicate sets if desired.
Then S is two-star-forming exactly when S meets every member of H(G).

To prove this, suppose u is omitted. The A_u clause requires at least
one selected neighbor v. If u has two selected neighbors, every B_(u,w)
retains at least one of them. If u instead has a selected neighbor v
with a selected neighbor t, then B_(u,w) contains v when w!=v, and
B_(u,v) contains t. Thus formation implies all clauses are hit. A
selected u itself hits every clause with first index u.

Conversely, take an omitted u and a selected neighbor v supplied by A_u.
The B_(u,v) clause supplies either another selected neighbor of u or a
selected neighbor of v. This is exactly a non-induced two-star on u
and two selected vertices. No degree, bipartite or girth restriction
is needed, and isolated vertices are handled by their singleton A_u.

An inclusion-minimal forming set is consequently an inclusion-minimal
transversal of H(G). Equivalently, it hits all clauses and each selected
vertex v owns a private clause E, meaning E intersect S={v}.
If a selected v owns none, deleting it leaves all clauses hit. If each
selected v owns one, any proper subset omits an owner and misses its
private clause. A single clause cannot be private to two selected vertices.

## The boundary-certificate lemma

Let K be a graph whose edges and vertices lie in a core C of G. Require
that G retains all K edges, and that every core non-port has exactly
its K neighbors in G. Only specified core ports P may have additional
edges, either to other ports or to external vertices. Let S be a
minimal forming set in G and T=S intersect C.

**Lemma.** Every selected non-port v in T satisfies at least one of:

1. v owns a private clause in H(K), restricted to the core selection T;
2. some selected core port p has v as its sole selected K-neighbor.

No formation hypothesis on T inside K is assumed.

Choose a global private clause for v. If it is A_u, its containing v
means u=v or u is a neighbor of the non-port v. Thus u lies in the
core, and the core clause A_u(K) contains v and is contained in A_u(G).
It is private to v inside T.

Now consider a global clause B_(u,w). If uw is an old K edge, its core
version is contained in its global version. Since edges incident to
v are unchanged, membership of v in the global clause implies membership
in the core version, giving case1 again.

Suppose uw is a new edge. If v=u, this contradicts v being a non-port.
If v lies in N_G(u) minus {w}, then u is a core port and A_u(K) is
contained in B_(u,w)(G): w is not an old K neighbor. This gives case1.
In the remaining case v lies in N_G(w) minus {u}, so w is a core port.
Every selected K-neighbor of w lies in the global private clause and
must therefore equal v. If w is selected, this is case2. If w is
omitted, A_w(K) is itself private to v inside T, giving case1.
These exhaust the possible positions of v in a clause.

**No repeated boundary charge.** Let U consist of selected non-ports
owning no internal private clause. By the lemma, every v in U is the
sole selected core neighbor of some selected port. A port can have
only one such owner. Hence, for finite cores,

    |U| <= #{selected ports of selected core degree one}.

When several disjoint cores are used, the charges belong to actual
ports of their respective cores. No one port can pay for two different
non-port owners. This is a necessary certificate budget, not yet a
bound of12k on long-core selections.

In particular, a selected non-port owning no private core clause and
not being the unique selected core neighbor of a selected port cannot
occur in a global minimal selection. Deleting it preserves formation
in any surrounding graph allowed by the lemma. This gives an exact
way to search for safe core deletions without assuming the core
selection itself is forming.

## An all-length obstacle to the robust shortcut

Use Q_k and its local twenty-vertex labels from the omission notes.
In every six-index block select

    H{0,1,3,4,5}, U{0,2,4,5}, X{0,1,3}, Y{0}.

Call the resulting13k-vertex set T. The H5--nextH0 seams are selected,
while X5 is omitted on every X seam. The selected core degrees, in
the order of the displayed local sets, are

    H: 3,1,1,3,3; U: 3,1,2,1; X: 1,0,0; Y: 3.

T forms Q_k. The omitted H2 has three selected neighbors; omitted U1,
U3,X2,X4,X5 each have two; and omitted Y1 sees selected U5, which is
active through H5.

Nevertheless T has no robust non-port deletion under the sufficient
rule of [exact Heawood composition](EXACT_CUBIC_COMPOSITION.md).
The following table identifies an explicit failed condition for each
of its ten selected non-port types.

| Candidate | Failure of robust-deletion condition |
|---|---|
| H0 | Selected neighbor H1 has selected degree one |
| H4 | Selected neighbor H3 has selected degree one |
| H5 | Selected neighbor U5 has selected degree one |
| U0 | Selected neighbor X0 has selected degree one |
| Y0 | Selected neighbor U2 has selected degree one |
| H1 | Omitted U1 has two selected neighbors; its other neighbor X1 is isolated |
| H3 | Omitted U3 has two selected neighbors; its other neighbor X3 is isolated |
| U2 | Omitted X2 has two selected neighbors; its other neighbor X1 is isolated |
| U4 | Omitted X4 has two selected neighbors; its other neighbor X3 is isolated |
| U5 | Omitted Y1 has just one selected neighbor |

This is not a larger minimal forming set. Each H0 is safely deletable:
the newly outside H0 has three selected neighbors; H5 and U0 remain
active; H1 becomes isolated, but its omitted neighbors H2 and U1 retain
three and two selected neighbors respectively. No selected core port
loses activity. Thus the deletion also works under arbitrary attachments
at X ports. Failure of the robust shortcut is distinct from failure
of the desired SF upper bound.

## A small exact binary formulation

The clause equivalence yields a finite exact model for SF discovery.
For a subcubic graph, there are at most4n distinct clauses, each of
size at most5. Introduce a binary selection x_v and one binary marker
p_E per clause. Impose

    sum_(v in E) x_v >= 1;
    sum_(v in E) x_v + (|E|-1)p_E <= |E|;
    sum_(E containing v) p_E >= x_v.

A marked clause has exactly one selected vertex. For a selected v,
the last inequality therefore supplies a private clause containing v.
Conversely, any minimal forming selection is feasible by marking its
singleton-intersection clauses. Maximizing sum x_v is exactly SF_2(G),
using at most5n binary variables and9n constraints before optional
proved inequalities are added. These model equivalences are general
arguments, rather than inferences from solver output.

The [exploratory solver](../scripts/explore_long_core_SF.py) applies the
model to L_8 and searches for a minimal set of size289, the only possible
improvement over288 allowed by the proved SF interval. A45second run
timed out without a feasible incumbent. A separate30second core search
at k2 also timed out. Both results are inconclusive; no infeasibility
or new SF value is inferred.
[Discovery receipts](../output/long-core-SF-discovery.json).

## Verification and next step

[PrivateClauses.lean](../formal/StarForming/PrivateClauses.lean) proves
five general graph-level results: the exact clause equivalence,
private-clause characterization of inclusion-minimality, unique ownership,
monotonicity of clause support, and the boundary-certificate lemma.
All passed local Lean with standard axioms only.
[Formal receipt](../output/private-clauses-formal-check.json).
The finite cardinal budget and optimization model are written deductions.

[Independent checks](../scripts/check_private_clauses.py) compare literal
stars, the clause test and all-proper-subset minimality on every graph
of order at most five, plus the ten-vertex counterexample and Heawood.
They also test the periodic robust-rule obstruction and exhaust all
dense selections in the fixed Q_1 core. The latter suggest that every
selection larger than12 there has a safe non-port deletion, but this
is only a finite lead; a general long-core statement is not proved.
[Controls](../output/private-clauses-controls.json).

The live [Oracle research question](reviews/2026-10-19-long-core-SF-research-question.md)
asks for the all-k SF theorem or a larger verified minimal witness.
Continue by resolving the remaining core certificate geometry or by
finding a coupled core/Heawood compensation rule. The submitted manuscript
and upstream trureturing are unchanged.
