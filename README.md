# Sub-quorum colorings: hypercubes, boundary matchings, and grids

[![Verification](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml/badge.svg)](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml)

Research sources and reproducibility materials for **From hypercubes to grids:
sub-quorum colorings and structural bounds**, with contributions by Wenlin
Zhang (National University of Singapore; The Omega Institute) and Haobo Ma
(ChronoAI Pte Ltd; The Omega Institute).

**Start with the [current mathematical results](docs/GRID_RESULTS.md)**:
the uniform grid dissociation formula, directional matching bounds, and the
five-sixths estimate for mixed directions. This companion includes complete
proofs and extends the earlier manuscript, which covers the hypercube,
structural results and exact strip certificates.

The starting result resolves Conjecture 6.4 of Rafik Sahbi's
[Sub-quorum colorings of graphs, arXiv:2609.25128v1](https://arxiv.org/abs/2609.25128v1):
the sub-quorum coloring number of the n-dimensional hypercube is 2^(n-1)
for **every n >= 2**, with a dimension-independent Lean proof.

Starting from this solved family, the project advances two research directions:

1. **Rectangular grids:** use exact strip certificates and the boundary viewpoint
   to seek a proof of Sahbi's formula at arbitrary width and length.
2. **Structural characterization:** determine conditions for psi_sq=beta_2,
   using the signed boundary theorem as a sufficient mechanism and the grafted
   tree families as explicit obstructions.

The [research agenda](docs/RESEARCH.md) connects current results to the next
mathematical targets. The manuscript follows the same progression from the
hypercube solution to these geometric and structural questions.

The related [star-forming project](docs/EXACT_STAR_FORMING_COMPOSITION.md)
has a separate composition theorem: joining r ten-vertex copies through
arbitrary b1-to-a1 interfaces gives beta_2=5r and SF_2=6r. Cyclic interfaces
give two-connected bipartite graphs of maximum degree four with exact gap
|V|/10. The note contains the full local deletion proof and a three-page PDF;
the general SF upper bound and an attaining minimal set are checked in Lean.

A [subcubic construction](docs/SUBCUBIC_STAR_FORMING_GAPS.md) now gives
two-connected bipartite graphs J_r of minimum degree two and maximum degree
three, for every even r>=2, with order 11r, beta_2=13r/2 and SF_2=7r.
The [exact upper-bound proof](docs/EXACT_SUBCUBIC_COMPOSITION.md) limits
each ten-vertex core to six selected vertices in any outside graph
attached only at its designated vertices. Thus their gap is exactly
|V|/22. Cycles have beta_2=SF_2=floor(2n/3),
so three is the first maximum-degree bound permitting a gap among
two-connected bipartite graphs. An explicit perfect matching also gives
Gamma=alpha=11r/2, separating all three parameters. The full proof tracks identified ports
without double counting; base certificates and its arithmetic bound are
checked with standalone Lean4.33.0. Five further Lean audits check supported
deletion, the dense-core certificate, its arbitrary-outside lift, the
per-core cap and the new arithmetic accounting.

The [cubic construction](docs/CUBIC_STAR_FORMING_GAPS.md) strengthens the
regularity restriction: for every r>=1 there is a two-connected cubic
bipartite graph F_r of girth six and order 14r with Gamma=alpha=7r,
beta_2=7r+floor(r/2), and SF_2=8r. Its exact gap is ceil(r/2), at least order/28.
A Fano-plane saturated-port lemma gives the exact dissociation count, and
rewiring only outside the fixed selected set preserves its minimality.
The [exact composition theorem](docs/EXACT_CUBIC_COMPOSITION.md) supplies
the matching upper bound even for arbitrary port interfaces, and an
interaction graph Q gives beta_2=7r+alpha_0(Q), where looped vertices are
excluded from independent sets. The exact gap is its vertex-cover number.
Written proofs and independent controls are available. The
[literature check](docs/STAR_FORMING_LITERATURE_20261019.md) also identifies
Bhattacharjee's external bipartite/planar-bipartite complexity theorem,
which narrows the remaining complexity agenda to additional restrictions.

The [degree-capacity theorem](docs/REGULAR_STAR_FORMING_BOUND.md) now gives
a sharp order bound for every d-regular graph: SF_2<=floor(dn/(2d-1)),
including SF_2<=floor(3n/5) for all cubic graphs. Its general version tracks
the degrees of selected vertices and charges pairwise disjoint failure
witnesses. All regular extremal sets have an explicit five-part structure;
for bipartite regular graphs, attaining this bound forces beta_2=SF_2.
It also gives the sharp comparison SF_2<=6 Gamma/5 for cubic bipartite graphs.
The same weighted argument gives the rectangular-grid star-forming bound
SF_2(P_m square P_l)<=floor((4ml+2m+2l)/7), for m,l>=2. This does not
establish the separate bridge to sub-quorum colorings. General written
proofs, twelve symbolic Lean audits and independent controls are available;
the full equality characterization and finite cardinal summation have
written proofs rather than complete Lean formalizations.

## Results and verification

| Result | Scope | Verification |
| --- | --- | --- |
| Hypercube coloring number | All dimensions n >= 2 | Lean 4, pinned Mathlib; original modules from trureturing |
| Boundary matching | Feasible (T,M) in graphs with signed adjacency S^2=dI, d>=2 | Written energy estimate and Hall argument |
| Bipartite signed graphs and Cartesian products | All graphs satisfying the stated hypotheses | Written proof and exact matrix controls |
| Exact grafting theorem | Every finite nonempty base graph F | Written proof; tree-DP cross-checks |
| Unbounded gap on subcubic trees | R(P_k), every k>=1; gap floor(k/3) | Written proof; checks k=1..30 |
| Rectangular grid formula | Widths 8,9,10,11 at every positive length | Exact full-vector certificates, independently recomputed |
| Grid dissociation number beta_2=F | Every positive width and length | Written row-profile proof; exact finite checks |
| Directional Omega_H=Omega_V=F | Every positive width and length | Written ladder-rigidity argument; exact finite checks |
| Mixed matching bound with coefficient 5/6 | Every positive even-by-even rectangle | Written residual-geometry proof; exhaustive and constructed controls |
| Exact star-forming composition | Every finite b1-to-a1 interface relation on the fixed ten-vertex copies; SF_2=6r and beta_2=5r | General written proof; Lean SF bound and attainment; local finite controls |
| Subcubic star-forming gaps | Two-connected bipartite J_r, even r>=2; beta_2=13r/2, SF_2=7r, gap=order/22; arbitrary-outside core cap; cycle equality gives the degree threshold | General written proofs; standalone Lean certificates; independent deletion controls and full J_2 enumeration |
| Exact Heawood-port composition | Arbitrary simple graph on the ports of r broken Heawood blocks; SF_2=8r, beta_2=7r+alpha_0(Q), gap=the interaction graph's vertex-cover number | General geometric and saturation proofs; Lean arbitrary-outside cap; independent local, ambient and port-state controls |
| Cubic star-forming gaps | Two-connected cubic bipartite F_r, every r>=1; girth six, beta_2=7r+floor(r/2), SF_2=8r, exact gap=ceil(r/2) | General Fano and interface proofs; standalone Lean certificates; independent base and family controls |
| Sharp regular star-forming order bound | All d-regular graphs, d>=1: SF_2<=floor(dn/(2d-1)); exact regular extremal structure; bipartite attainment forces beta_2=SF_2; weighted grid corollary | General injective witness-capacity proof; twelve symbolic Lean audits; 1,301 finite graph controls; completed Oracle review |

The Lean theorem explicitly states psi_sq(Q_n)=2^(n-1). The beta_2 identity
was already established by Sahbi and also follows from the written proof;
beta_2 is not defined in the archived Lean module. The subsequent structural
and grid results are not yet Lean formalized. The unrestricted mixed-direction
grid coloring formula remains open.

The grid extension uses Sahbi's Omega reduction and max-plus method. Huang's
signed hypercube matrix is the key input to the hypercube proof. Tree-result
priority is still to be compared with the earlier caterpillar work cited
by Sahbi; the draft makes no historical priority claim about that work.

## Contents

- `manuscript/paper.tex`: research draft, proofs and tree recurrence appendix.
- `docs/GRID_RESULTS.md`: current grid results and links to their complete proofs.
- `develop/`: two exact C++ transfer implementations, independent small controls,
  tree recurrence, and mathematical notes.
- `develop/results/`: full integer state vectors, finite readouts and hashes.
- `formal/`: standalone Lean package with the original two proof modules.
- `docs/REPRODUCE.md`: build and verification instructions.
- `docs/RELEASING.md`: verification, version tags and Zenodo connection.

See [releases](https://github.com/the-omega-institute/subquorum-colorings/releases)
for the PDF and source/reproduction archives. CI recomputes certificate endpoints
from the empty state, runs finite controls, builds the paper, and checks Lean.

## Attribution and license

This repository is an Omega Institute research artifact. Sahbi is credited for
the source problems and methods; this deposit does not assign him authorship
of the current draft. The manuscript author list is provisional.
AI assistance included mathematical exploration, code development, cross-checking
and drafting, as described in the manuscript.

Original material and the imported trureturing modules are distributed under
Apache-2.0; see `LICENSE` and `NOTICE`. External dependencies retain their
upstream licenses. Cite `CITATION.cff`; a DOI will be added only after Zenodo
confirms an archival record for this repository.
