# Reproduction

Requirements: C++17 compiler, Python >=3.10 (standard library only), TeX Live
with amsmath, amsthm, TikZ, hyperref, cleveref, microtype and Latin Modern.
Formal verification additionally uses elan and the pinned Lean/Mathlib versions.

## Exact computations

From the repository root:

```sh
python3 scripts/verify_archive.py
mkdir -p build
c++ -O3 -std=c++17 -Wall -Wextra develop/grid_omega.cpp -o build/grid_omega
c++ -O3 -std=c++17 -Wall -Wextra develop/check_omega.cpp -o build/check_omega
python3 scripts/check_strip.py 11
```

Replace 11 with any width from 1 through 11. The checker regenerates every
archived finite readout for that width, compares both certificate vectors,
and invokes the second program to reconstruct both endpoints independently.
Width 11 has 1,949,930 reachable states and needs several GB of available
memory; run one width at a time on a small machine. No floating-point solver
or inferred scalar periodicity is used.

The general all-length implication is proved in the paper and
`develop/grid-strips-2026-09-27.md`. The finite audit has 336 grid cases.

Run small independent controls from `develop/`:

```sh
python3 check_small.py
python3 check_structural.py
python3 tree_parameters.py
```

The last script compares the tree recurrence against direct partial colorings,
checks the six-vertex tree classification and both unbounded-gap families,
and checks grafting over all labelled base trees with 2..5 vertices.
The grafting theorem itself applies to every finite nonempty base graph;
its proof is in the paper and `develop/grafting-2026-09-27.md`.

## Lean proof

The modules are preserved byte-for-byte from the pinned source in
`formal/UPSTREAM.json`. From `formal/`:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

Expected theorem: `subQuorumChromaticNumber_hypercube (n : Nat) (hn : 2 <= n)`.
Expected axioms: `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx`.
Lean proves the coloring-number identity in every dimension n>=2. It does
not formalize the later grid/structural extensions or define beta_2.
CI measures runner memory and active Lean processes before building. The
workflow uses GitHub-hosted runners, with no dependency on a private workstation.

## Manuscript

From `manuscript/`:

```sh
mkdir -p output/pdf
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=output/pdf paper.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=output/pdf paper.tex
```

The release PDF is built from the tag's exact source. Release ZIPs include a
SHA256 member manifest and CI verification receipts. Download the source ZIP
for editing the paper or the research ZIP for the complete reproducibility set.
