# Upper two-star-forming sets on every four-row rectangular grid

For every integer n>=1, the full grid H_n=P_4 square P_n satisfies

    SF_2(H_n)=beta_2(H_n)=2n+(n mod2).                       (1)

Together with the prior width-four sub-quorum colouring formula, this
establishes SF_2(H_n)=beta_2(H_n)=psi_sq(H_n) for all positive lengths.
The contribution is the upper minimal forming number, rather than a new
colouring formula. As for the three-row result, the proof is computer
assisted: a complete exact frontier and an entrywise vector certificate
supply an induction valid at every length. Arbitrary grid width remains open.

## 1. The same exact frontier at height four

Use the definitions and Frontier Lemma of
[the complete three-row proof, Sections 1--2](THREE_ROW_STAR_FORMING_EQUALITY.md).
Those arguments were given for an arbitrary height h: a formation or
single-deletion failure centred in column c depends only on columns c-2
through c+2. Introduce one column, process all tests at the middle column
of the five-column window, and forget the oldest column only after each
of its selected vertices has an already processed deletion witness.
A selected centre may certify its own deletion; an omitted centre may
certify several different single deletions. All centres of actual columns
are processed exactly once, including the two ends.

Retain the selected/unwitnessed/witnessed ternary information on four columns.
At h=4 there are 3^16=43,046,721 possible states. A sparse implementation
stores only reachable states. Its binary serialization is

    key = s + 2^16 f,     0<=s,f<2^16, f subset s,

where s and f are the selected and witnessed masks on the retained columns,
with the oldest column at the low bits. This is a one-to-one encoding of
the same ternary states; unused binary keys are not extra states.

The soundness and completeness proof applies verbatim at h=4. Thus the
maximum-score vector V_n is exact. For n>=2, adding a real column uses
one fixed max-plus transfer Phi, and right closure is one fixed operation Z:

    V_(n+1)=Phi(V_n),   Phi(V+c)=Phi(V)+c,   Z(V+c)=Z(V)+c.  (2)

The one-column closure again has flags absent, real, absent, absent;
the n>=2 closure has flags real, real, absent, absent. All absent columns
have zero selected masks and are never witness centres.

## 2. The finite certificate and all-length proof

Both implementations independently reconstruct the entire vectors from the
empty prefix and verify

    V_17=V_15+4,                                         (3)

with exactly 342,768 reachable states on each side. Their supports coincide;
every finite entry increases by four, and every other ternary state remains
unreachable. The C++ implementation uses neighbour/activity masks. The
independent Python implementation uses literal three-vertex star edge
patterns, reusing the already supplied Python specification rather than
importing the C++ generator. The vector files are reproducible outputs;
the concise report records their hashes and the exact generation command.

For every j>=0, apply the fixed transfer j times to (3). Homogeneity gives
V_(17+j)=V_(15+j)+4. The fixed closure then proves

    SF_2(H_(n+2))=SF_2(H_n)+4 for every n>=15.              (4)

The finite exact values for n=1,...,16 are

    3,4,7,8,11,12,15,16,19,20,23,24,27,28,31,32.

They agree with 2n+(n mod2). This formula has the same recurrence (4).
Induction proves the asserted upper forming value at every positive n.
The conclusion uses equality of complete vectors, not repeated scalar
optima; the finite identity is a machine-checked premise of the proof.

## 3. An explicit attaining dissociation set

In each even-indexed column select rows 0,1,3; in each odd-indexed column
select only row 2. Every complete two-column block contributes four, and
an odd residual column contributes three, giving 2n+(n mod2).

The selected components are the vertical edges between rows 0,1 in even
columns and otherwise isolated vertices. In an even column, omitted row 2
has both vertical neighbours selected. In an odd column, omitted rows 0,1
see an active selected vertex in the preceding even column. Omitted row 3
has its selected row-2 neighbour and the selected row-3 vertex immediately
to its left. All odd columns have such a preceding even column, including
the last column when n is even. Hence every outside vertex is formed.
Deleting any selection fails at itself because the selected components
have order one or two. The set is both dissociation and minimal forming.

The general inequality beta_2<=SF_2, proved in Section 4 of the three-row
note by extending dissociation sets, and the computed SF upper bound now
prove (1) for both parameters. Sahbi's arXiv:2609.25128v1, Theorem 5.5,
already gives psi_sq(H_n)=F(4,n)=2n+(n mod2). Combining that established
colouring theorem with (1) proves the triple-equality corollary. The old
Omega certificate is another independent source for the colouring bound;
no general SF_2<=Omega premise is used here.

## 4. Reproduction and actual verification scope

From the repository root, use a disposable output directory for the two
large but reproducible vector files:

```sh
c++ -std=c++17 -O3 -Wall -Wextra scripts/grid_star_sparse_transfer.cpp -o /tmp/sahbi-grid-star-h4
/tmp/sahbi-grid-star-h4 4 17 /tmp/sahbi-grid-star-h4-vectors
python3 -B scripts/check_grid_star_height_four.py /tmp/sahbi-grid-star-h4-vectors
```

The Python checker requires `scripts/check_grid_star_transfer.py` alongside
it. It rebuilds both vectors from the empty prefix, compares all entries
with the independently generated C++ vectors, and checks (3) itself. Its
literal local kernel enumerates all 1,048,576 five-column selection masks.
It also compares transfer acceptance with literal whole-graph minimality
for every subset on the four boards 4-by-1 through 4-by-4: 69,904 subsets.
Those small controls test the implementation and boundary cases; the general
frontier proof and vector induction supply the all-n conclusion.

The C++ program enforces a one-million reachable-state resource limit;
exceeding it terminates without a certificate. The successful 17-column
run remains below that limit. No general resource bound is inferred from
the observed reachable count. No Lean execution or arbitrary-width proof
is claimed. Independent review and its executed scope will be recorded
separately from the three-row audit.
