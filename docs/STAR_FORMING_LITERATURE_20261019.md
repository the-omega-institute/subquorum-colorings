# Star-forming literature and priority check, 19 October 2026

This is a limited, source-specific check, not a comprehensive priority search.
It changes the current complexity agenda and supplies context for the cubic
gap theorem. Downloaded third-party PDFs and source checkouts are inspection
inputs, not artifacts redistributed by this repository.

## Chellali and Favaron's original definitions

M. Chellali and O. Favaron, *On k-star-forming sets in graphs*, JCMCC 68
(2009), 205–214. The
[publisher's original scanned article](https://combinatorialpress.com/article/jcmcc/Volume%20068/vol-068-paper%2014.pdf)
was read across all ten pages using OCR and rendered-page checks. Its
definition uses inclusion-minimal selections and non-induced stars. For k=2
the outside vertex can be a centre with two selected neighbors or a leaf
adjacent to a selected vertex having another selected neighbor. This agrees
with the predicate in our written proofs and Lean source.

Their Theorem 2.1 gives beta_k<=SF_k. The paper treats trees, chordal graphs,
and related domination classes. In particular, its Theorem 3.1 on well-k-covered
trees does not assert beta_k=SF_k for all trees: the equalities involving the
lower star-forming number sf_k must not be confused with the upper number.
No Heawood, Fano-plane, cubic-regular or cyclic cubic gap theorem was found
in this full article inspection. That observation alone establishes no
historical novelty. The reference list also identifies Haynes, Hedetniemi,
Henning and Slater, *H-forming sets in graphs*, Discrete Mathematics 262
(2003), 159–169; that broader source remains to be inspected.

## External October 14 complexity result

Deep Bhattacharjee, *Upper k-star-forming sets and k-independence in bipartite
graphs*, version 1.1.0, deposited 14 October 2026:
[Zenodo DOI 10.5281/zenodo.23360032](https://doi.org/10.5281/zenodo.23360032),
[tag v1.1.0](https://github.com/creelie/Conjecture-002/tree/v1.1.0),
inspected source revision
`82c7cf4974d7eab76d5f04afdc4c8d563daecdc1`.
The complete complexity proof in `preprint/main.tex` and the definitions
and final statement in `lean/StarForming/Hardness.lean` were read without
executing the external code or rebuilding its Lean development.

The paper proves that deciding whether SF_2(G)>=t is NP-complete for
bipartite graphs, including planar bipartite graphs. This is the threshold
problem for the maximum size of an inclusion-minimal set, not the problem
of a minimal set of one prescribed exact size. It also gives equality on
chain graphs for all k and counterexample families for k>=3. Its reference
to the k=2 counterexample points to our pipeline PR 14727; the new external
complexity theorem belongs to Bhattacharjee and is not a result of this
collaboration.

Here is the reduction and its relevant scope. From any graph H on n vertices
and m edges, replace every edge uv by u--a--b--c--v, and attach one pendant
v' to every original vertex v. Call the result H-sharp. It is bipartite,
is planar when H is planar, and has order 2n+3m. The exact identity is

    beta_2(H-sharp)=SF_2(H-sharp)=n+2m+alpha(H).

For an independent set I, select all pendants, all middle vertices b, the
original vertices in I, and a when u is not in I, or c otherwise. Every
selected vertex has selected degree at most one. The selection has size
n+2m+|I|, giving the lower bound via beta_2<=SF_2.

For the upper bound, minimality forces at least one of v,v' to be selected.
It forbids selecting all a,b,c on an edge path: deleting b preserves stars,
since an omitted original endpoint also has its selected pendant. If both
endpoint-pendant pairs are fully selected, at most one of a,b,c can be
selected; with two selected, a deletion at the appropriate end of the
inner path preserves coverage, while each original endpoint retains its
selected pendant as a leaf. Let Y be the original vertices whose pair is
fully selected and e(Y) its number of induced edges. These disjoint local
counts yield

    |S|<=n+|Y|+2m-e(Y)<=n+2m+alpha(H).

For the second inequality, H[Y] has at least |Y|-e(Y) components, and one
vertex from each component is independent. The independent-set threshold
therefore reduces to SF_2 at threshold n+2m+t, with planarity preserved.
Membership in NP follows from the polynomial local test and single-deletion
test, justified by upward closure. This reading found no gap in the stated
reduction; it is an external theorem whose Lean build has not been replayed.

Our [independent finite controls](../scripts/check_external_sharp_gadget.py)
check all 33 labeled base graphs of orders 1–3 and order 4 with at most two
edges, totaling 305,108 gadget subsets. They check all-proper-subset minimality,
the three upper-bound constraints, every independent-set lower witness, and
the exact identity. The
[receipt](../output/external-sharp-gadget-controls.json) records the scope.
This enumeration is a consistency check, not the NP-hardness proof.

The gadget has pendant vertices and original degrees deg_H(v)+1. Consequently
the result does not by itself settle cubic, regular, or two-connected restricted
complexity. It settles the broad bipartite and planar-bipartite question that
our earlier agenda left open. Future records and correspondence should use
these more specific remaining questions.

## Relation to the cubic gap theorem

The inspected external text and Lean sources contained no Heawood/Fano or
cubic-regular gap construction. Our new theorem gives two-connected cubic
bipartite graphs of girth six and unbounded linear gap, with exact beta_2,
and remains mathematically distinct from the equality gadget used for
complexity. The original 2009 article and this external work do not constitute
a complete literature search for that theorem. No first, smallest, or sharpest
claim is made. Exact SF_2 of our Heawood-port family is now established in
[the composition note](EXACT_CUBIC_COMPOSITION.md). The
[degree-capacity theorem](REGULAR_STAR_FORMING_BOUND.md) gives the sharp
order bound SF_2<=dn/(2d-1) for every d-regular graph, including the cubic
bound 3n/5, with an irregular-degree version and a bipartite equality
characterization. The optimal cubic gap coefficient and three-connectivity
remain research questions.

## Recheck for the degree-capacity theorem

The original 2009 article was downloaded again and OCR inspected across
all ten pages. Page208 was also inspected visually. Theorem2.3 is a
minimum-degree upper bound for the lower parameter sf_k, not the upper
parameter SF_k. It therefore does not supply or contradict the regular
upper-SF bound. The article's final k-star-irredundance definition is relevant
background for deletion witnesses but contains no stated regular upper-SF
theorem. No historical priority is inferred from this source-specific check.

Crossref identifies the earlier *H-forming sets in graphs* as
[DOI10.1016/S0012-365X(02)00496-X](https://doi.org/10.1016/S0012-365X(02)00496-X).
OpenAlex reports a bronze-open-access DOI landing page but no repository
full-text location or direct PDF. The initial Crossref-provided Elsevier
content route failed with HTTP400. The corrected `/article/pii/` route
returned metadata confirming open-archive status, but its FULL view returned
an authentication error; PDF content negotiation was restricted and the
ScienceDirect PDF route returned HTTP403. The full 2003 text therefore
remains uninspected. Crossref searches for
upper star formation, P3-forming degree bounds and star irredundance did
not return a directly matching theorem; metadata search is not evidence
that none exists. The scope and possible prior appearance of the general
order bound and equality characterization remain to be checked against
that earlier source and subsequent citing papers before making a novelty claim.
