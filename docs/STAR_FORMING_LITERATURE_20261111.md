# Literature comparison for the sharp bipartite gap

Checked 11 November 2026 for the working manuscript `manuscript/starforming-gap.tex`.
The headline assertion is SF2(G)-beta2(G)<=floor(|V(G)|/10) for all finite
simple bipartite graphs, with exact four-attachment attaining compositions.
No first-ever, smallest-example, or complete equality-classification claim is made.

## Primary sources and what they support

1. M. Chellali and O. Favaron, *On k-star-forming sets in graphs*, JCMCC 68
   (2009), 205--214. [Publisher scan](https://combinatorialpress.com/article/jcmcc/Volume%20068/vol-068-paper%2014.pdf).
   All ten pages were inspected through OCR; pages 207--208 were separately
   inspected in the independent proof audit. Section 2 defines non-induced
   stars and inclusion-minimality; Theorem 2.1 gives beta_k<=SF_k. Its
   Theorem 2.3 is a bound on LOWER sf_k and must not be relabelled upper SF_k.
   The article supplies deletion/irredundance background, not the stated n/10 theorem.

2. O. Favaron, *Bounds on the Upper k-Domination Number and the Upper
   k-Star-Forming Number of a Graph*, JCMCC 80 (2012), 321--332.
   [Publisher scan](https://combinatorialpress.com/article/jcmcc/Volume%20080/vol-080-paper%2022.pdf).
   All twelve pages were inspected through OCR. Theorem 10, page 326, gives
   SF_k<=n-delta+k-1 when 1<=k<=delta. Theorem 13 characterizes its endpoint.
   This is an order/minimum-degree bound, not the new comparison with beta2.
   Its Gamma_k denotes upper k-domination, not ordinary upper domination.

3. R. Sahbi, *Upper k-Star-Forming Sets, k-Independence, and Upper Domination*,
   [arXiv:2610.03785v2](https://arxiv.org/abs/2610.03785v2), 6 October 2026.
   The PDF and TeX source were inspected. Conjectures 4.1 and 4.2 (page 4)
   assert bipartite equality; Conjecture 7.2 (page 9) asserts triangle-free
   equality for k=2. Definition 2.1/Lemma 2.2 (page 2) use the same local
   star predicate; Proposition 3.4 gives disjoint-union additivity.
   Section 5, Lemmas 5.1--5.3, develops the deletion-certificate restrictions
   and bipartite witness classification used as the starting point here.
   The two averaged dissociation exchanges and universal gap bound are
   not stated in that source.
   The current unversioned record was independently retrieved by the main
   session: v5, 27 October 2026, withdrawn, comment "Invalid conjectures".
   The manuscript therefore cites the numbered statements to v2 and records
   subsequent withdrawal. Withdrawal is not a new journal decision on the
   separate sub-quorum paper.

4. D. Bhattacharjee, *Upper k-star-forming sets and k-independence in bipartite
   graphs*, archived version 1.1.0, 14 October 2026,
   [DOI](https://doi.org/10.5281/zenodo.23360032),
   [versioned source](https://github.com/creelie/Conjecture-002/blob/v1.1.0/preprint/main.tex).
   The full manuscript source was read, including the higher-k construction,
   chain-graph equality and complexity sections. The construction for k>=3
   varies k, unlike the present fixed-k=2 gap theorem. The bipartite and
   planar-bipartite threshold complexity questions are already settled there.
   Its local safe deletions are relevant antecedents; broad deletion-method
   novelty would be inappropriate. It credits the earlier ten-vertex public
   counterexample. This is an archived source/software deposit, not an
   invented journal publication.

5. F. Bock, J. Pardey, L. D. Penso and D. Rautenbach, *A bound on the
   dissociation number*, Journal of Graph Theory 103 (2023), 661--673,
   [DOI](https://doi.org/10.1002/jgt.22940),
   [primary preprint](https://arxiv.org/pdf/2202.09190).
   Metadata was checked against Crossref; Theorems 1--2 and Lemma 3/Theorem 4
   were read. These concern dissociation lower bounds and attachment equality,
   including maximum sets avoiding a specified vertex. They do not control SF2.

6. P. Li, *A characterization of graphs attaining a lower bound on the
   dissociation number*, [arXiv:2610.35408v1](https://arxiv.org/abs/2610.35408v1),
   26 October 2026. All nine pages were read. Attachment operations on pages
   3--4, Theorem 1.3 and Lemma 2.1 concern equality in the Bock et al. bound.
   This new adjacent source is acknowledged when comparing attachment methods.
   It does not establish an upper-star-forming theorem.

## Search coverage, priority and length

An independent literature pass searched arXiv, OpenAlex, Crossref, publisher
records, Zenodo and versioned manuscript sources, following the 2009 and 2012
citation chains. Queries included upper k-star-forming, P3-forming,
star-irredundance, H-forming, safe deletion and dissociation, the direct
SF2-beta2 comparison, and cubic/triangle-free extremal families. The recent
search included October 2026 results. No inspected source supplies the
universal n/10 theorem or the four-attachment ambient cap.

MathSciNet, zbMATH and Google Scholar returned HTTP 403. Google Search supplied
challenge pages; Bing results were unusable. Some Crossref searches returned
429; successful individual records were used. The full text of Haynes et al.,
*H-forming sets in graphs*, Discrete Mathematics 262 (2003), 159--169,
doi:10.1016/S0012-365X(02)00496-X, remained inaccessible (Elsevier FULL 401,
ScienceDirect and repository 403). No theorem or absence claim is attributed
to that unread source. These limits prevent a comprehensive priority claim.

The manuscript is a focused five-page note with one sharp inequality, its
attainment and an independent ambient deletion lemma. Six references were
selected because each supports an actual comparison or definition. This is
a documented narrow-note exception to the writing guide's 12--20 reference
search target, not a claim to have met that numeric target. The retained
mathematical results have self-contained proofs; no inaccessible theorem is
used as a proof premise. Further source access and coauthor review can refine
the introduction before submission.
