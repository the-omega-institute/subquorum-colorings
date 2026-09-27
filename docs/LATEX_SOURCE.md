# Editable LaTeX source

This archive contains `paper.tex`, the working manuscript *From hypercubes
to grids: sub-quorum colorings and structural bounds*.

Compile from the extracted archive directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

Use a standard TeX Live installation with amsmath, amsthm, TikZ, hyperref,
cleveref, microtype, fancyhdr, booktabs and Latin Modern.
The document is self-contained and needs no external bibliography or figures.

The accompanying `research-package.zip` contains the exact computational
certificates, Lean sources, verification receipts and full reproduction guide.
See https://github.com/the-omega-institute/subquorum-colorings for updates.
