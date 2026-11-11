# Reproduce the sharp bipartite gap controls

The mathematical statements and proofs are in
[the general gap note](SHARP_BIPARTITE_STAR_FORMING_GAP.md),
[the four-attachment note](FOUR_PORT_STAR_FORMING_COMPOSITION.md), and
[the five-page working manuscript](../manuscript/starforming-gap.tex).

Build and run the standalone general-proof verifier:

```sh
c++ -O3 -std=c++17 -Wall -Wextra scripts/check_bipartite_gap.cpp -o /tmp/bipartite-gap-check
/tmp/bipartite-gap-check > /tmp/sharp-bipartite-gap-controls.json
cmp /tmp/sharp-bipartite-gap-controls.json output/sharp-bipartite-gap-controls.json
```

This enumerates every binary adjacency matrix with fixed bipartition sizes
a+b<=8 and 0<=a<=b, including a=0 and the empty graph. Different presentations
are not reduced up to isomorphism. It also checks 256 seeded models of orders
9--16 and the sharp ten-vertex example. For every inclusion-minimal forming
selection it reconstructs disjoint triples and pairs, both dissociation
constructions in both orientations, their size identities and the counting
bound. Each graph's beta2 and SF2 are computed directly from all subsets.
The random generator is C++ mt19937 with an explicit seed and modulo choices,
so no implementation-dependent real distribution is used.

A second standard-library Python verifier exhausts every allowable witness
assignment, rather than selecting a deterministic assignment:

```sh
python3 -E -u scripts/check_bipartite_gap_all_witnesses.py
```

Its final count is 6,401 graph presentations, 50,171 minimal sets and 58,454
witness assignments, recorded in `output/bipartite-gap-all-witnesses.txt`.
The exhaustive portion has 6,101 presentations of orders one through seven;
300 seeded controls have orders 8--11 and may repeat graph isomorphism types.
An empty witness assignment is counted once. This checker does not separately
verify the equality degree condition or the attachment theorem.

Run the independent local/interface controls:

```sh
python3 scripts/check_four_port_composition.py --exact --output /tmp/four-port-composition-controls.json
cmp /tmp/four-port-composition-controls.json output/four-port-composition-controls.json
```

Python's local star predicate is compared against literal star copies on the
base graph. All 174 dense dominating selections receive a safe deletion.
Sixty arbitrary surrounding graphs, including nonbipartite ones, check the
ambient argument. Twenty four-regular interface graphs check the complete
attaining selections, deletion witnesses, degree counts and connectivity
after every vertex deletion. A separately compiled C++ helper enumerates all
2^20 subsets for each of the 256 possible interfaces between two blocks,
using no local upper bound or composition formula. It returns beta2=10 and
SF2=12 in every case. Its temporary executable is automatically removed.

Compile the working manuscript with an ordinary LaTeX installation:

```sh
mkdir -p manuscript/output/starforming-gap
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=manuscript/output/starforming-gap manuscript/starforming-gap.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=manuscript/output/starforming-gap manuscript/starforming-gap.tex
```

The new general inequality, equality necessity and four-attachment theorem
have written proofs; these finite controls check the proofs and implementations.
No new Lean verification is claimed. The existing two-attachment development
does not certify these new theorems. No shared CI or publication workflow
was changed to run this task.
