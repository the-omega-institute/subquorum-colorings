# Auxiliary squares: an owner-size criterion and a parity exchange

The [complete proof](../manuscript/auxiliary-square-proof.tex) establishes an
additional sufficient class for the all-helper8b/3 bound. It uses a global
maximum owner dissociation set and, when needed, changes it on one owner cycle.

## The theorem and its physical consequence

Let A be a disjoint union of auxiliary C4 components on N=4s vertices, and let
B be any finite simple graph on the same vertices whose components are paths
or even cycles. If

    beta_2(B) >= 2ceil(N/3)-2,

then there is an A-independent set S which is dissociation in B and satisfies
|S|>=ceil(N/3). The combinatorial theorem does not need a physical colouring.
For a physical partial template with b helpers and N=2b index vertices, exact
normalization on each auxiliary square gives

    beta_I(H)=2b+max{|S|: S independent in A, B[S] dissociation}.

Consequently this owner-size condition proves beta_I(H)>=ceil(8b/3).
It concerns the owner graph B, not the30vertex physical graph or its unrestricted
dissociation number. The condition can be checked from the explicit formula

    beta_2(B) = sum_paths ceil(2m/3) + sum_even_cycles floor(2m/3).

It permits arbitrary paths and6k-cycles mixed with one6k+4-cycle, or with at
most two6k+2-cycles, when their orders sum to N. Simple6k+2-cycles start at
order8. More generally positive path surplus can offset cycle deficits.
The general all-helper8b/3 question remains open.

## The parity correction

Choose a maximum B-dissociation set D. Taking independent subsets in the
auxiliary squares gives at leastceil(|D|/2) vertices. The criterion leaves just
one possible deficit: |D|=2ceil(N/3)-2, an even integer. We must gain one
vertex. This is belowceil(2N/3) in every permitted residue ofNmod6.

Some owner cycle then has length not divisible by six. On such a cycle, any
prescribed consecutive vertices can be exchanged between two maximum
dissociation sets: use minimum deleted sets whose cyclic gaps2,3 change to3,2.
For cycles of length1mod3 choose a further gap2 elsewhere. The four-cycle case
uses arbitrary two-element sets. These are particular admissible gap patterns;
there are also minimum covers with a gap1 in the1mod3 residue.

If the owner cycle crosses auxiliary squares, choose an edge crossing two of
them. The exchange toggles parity in exactly those two squares. One of the two
global maximum owner sets has at least two odd intersections, which provide
the two half-unit rounding gains. All other owner components keep their maximum
choices, and the total owner count stays fixed.

If the owner cycle lies in one auxiliary square, it is a C4 on exactly that
square. Select an auxiliary opposite pair there. Its independence contribution
is2 instead of the half-cardinality bound1. Thus it supplies the same missing
vertex. Both arguments produce an actual compatible selection.

For a fixed minimal forming set whose actual extracted template satisfies this
criterion, combine the physically separate retained set as before. The resulting
Z>=0 supplies the existing conditional5/51 graph bound. To bound SF_2-beta_2,
an extraction for a maximum-cardinality minimal forming set is required.

## Construction and verification

[The algorithm](../develop/auxiliary_square_parity.py) returns selected owners,
witnesses and the intermediate maximum owner set, together with the exchange
when one was used. An inapplicable result states which sufficient condition
failed. It is not a counterexample to the target bound.

Run `python3 -B scripts/check_auxiliary_square_parity.py`. The deterministic
[report](../output/auxiliary-square-parity-check.json) covers2,133 templates,
of which1,923 satisfy the criterion and yield physical certificates, through
N=128 index vertices (64 helpers,320 physical vertices). There are241 exact
all-helper comparisons,39,840 literal owner-subset checks,12 crossing-edge
corrections and35 coincident-square corrections. Among the smaller controls,
37 satisfy this criterion while the preceding K4-free matching criterion fails.
The run also retains210 owner-size failures and a separate auxiliary-eight-cycle
failure, instead of applying the theorem outside its assumptions.

Three [fixed inputs](../develop/fixtures/auxiliary-square-parity.json) exercise
the critical C16 exchange, a coincident C4 with two other C6 components, and the
two-C8 template whose preceding matching-family2SAT instance is unsatisfiable.
The weaker threshold admits60 additional controls belowfloor(2N/3),
covering residuesNmod6=0 and2; the empty construction is checked as well.
Larger tests verify actual certificates; they do not assert large exact optima.
The all-size statement is proved by the exchange argument.

An earlier independent mathematical audit accepted the criterion. The exact
final-source executable audit and its scope are recorded separately in
output/auxiliary-square-parity-review.json. This sufficient class and the sharp
all-helper block leave the unrestricted subcubic interval[1/20,7/71] and the
general unit-weight grid questions unchanged.
