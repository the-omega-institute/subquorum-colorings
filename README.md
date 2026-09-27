# Sub-quorum colorings: hypercubes, boundary matchings, and grids

[![Verification](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml/badge.svg)](https://github.com/the-omega-institute/subquorum-colorings/actions/workflows/verify.yml)

Research sources and reproducibility materials for **Sub-quorum colorings of
hypercubes: boundary matchings and grid strips**, a working draft by Wenlin
Zhang (National University of Singapore; The Omega Institute).

The starting result resolves Conjecture 6.4 of Rafik Sahbi's
[Sub-quorum colorings of graphs, arXiv:2609.25128v1](https://arxiv.org/abs/2609.25128v1):
the sub-quorum coloring number of the n-dimensional hypercube is 2^(n-1)
for **every n >= 2**. This is a dimension-independent Lean theorem, not a
finite computation through dimension 10 or 11.

## Results and verification

| Result | Scope | Verification |
| --- | --- | --- |
| Hypercube coloring number | All dimensions n >= 2 | Lean 4, pinned Mathlib; original modules from trureturing |
| Boundary matching | Feasible (T,M) in graphs with signed adjacency S^2=dI, d>=2 | Written energy estimate and Hall argument |
| Bipartite signed graphs and Cartesian products | All graphs satisfying the stated hypotheses | Written proof and exact matrix controls |
| Exact grafting theorem | Every finite nonempty base graph F | Written proof; tree-DP cross-checks |
| Unbounded gap on subcubic trees | R(P_k), every k>=1; gap floor(k/3) | Written proof; checks k=1..30 |
| Rectangular grid formula | Widths 8,9,10,11 at every positive length | Exact full-vector certificates, independently recomputed |

The Lean theorem explicitly states psi_sq(Q_n)=2^(n-1). The beta_2 identity
was already established by Sahbi and also follows from the written proof;
beta_2 is not defined in the archived Lean module. The subsequent structural
and grid results are not yet Lean formalized. Arbitrary-width grids remain open.

The grid extension uses Sahbi's Omega reduction and max-plus method. Huang's
signed hypercube matrix is the key input to the hypercube proof. Tree-result
priority is still to be compared with the earlier caterpillar work cited
by Sahbi; the draft makes no historical priority claim about that work.

## Contents

- `manuscript/paper.tex`: research draft, proofs and tree recurrence appendix.
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
