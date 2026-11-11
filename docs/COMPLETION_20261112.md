# Structural equality and source-dependent completion: 12 November 2026

## Arbitrary Cartesian prisms and their sharp gaps

The [complete prism note](ADJACENT_INVOLUTIONS_AND_PRISM_GAPS.md) proves

    SF_2(H square K_2)=Omega(H square K_2)=2n-nu(D(H))

for every finite simple H, with no bipartiteness requirement. The upper
witness argument extends to any graph with an adjacent involutory
automorphism; its quotient determines exact Omega and an SF upper bound.
Prism attainment uses a layer selection over the residual critical-set
graph, with explicit opposite-rung deletion witnesses. An arbitrary graph
with this involution need not attain the SF upper bound: K_(2n) has
SF_2=2 and Omega=n for n>=3.

Over all n-vertex bases, both maximum gaps SF_2-beta_2 and SF_2-psi_sq are
exactly max(0,n-4). For n>=5 their positive equality bases are respectively:

- K_n with any matching of edges deleted, for SF_2-beta_2;
- K_n or K_n with one edge deleted, for SF_2-psi_sq.

For H=K_n with m disjoint edges deleted, n>=5, the complete values are

| Parameter | Exact value |
| --- | --- |
| beta_2 | 4 |
| psi_sq | 4 if m<=1, and 5 if m>=2 |
| SF_2 and Omega | n |

These are all-size proofs. A complete-base prism is n-regular,
n-connected and vertex-transitive, so those properties alone do not
extend the bipartite four-way equality. The note also proves direct
terminal completion in any paired graph for every feasible independent
T, including selections using both layers. Independence excludes direct
TT paths; no such TT-free assertion is made for arbitrary adjacent T.

`python3 scripts/check_paired_graphs.py` passes 1,100 prism bases and
1,065,509 literal subsets, 60,296 minimal forming sets, 4,166 general
paired graphs and 1,052,741 further subsets, 89,860 further minimal sets,
6,715 representative pairs, 5,397 direct completions including 496
mixed-layer selections, and 3,396,244 canonical partial colourings over
79 models. The latter exhausts all bases through order four and three
near-complete bases of order five. Twelve larger prism certificates and
31 larger extremal-family certificates also pass.

The research-stage Oracle audit reconstructed and accepted all proposed
formulae and equality classifications; it did not inspect or run code.
The complete note, both new Python files and their existing matcher
dependency have a separate independent audit at f44adbc. Its final scope
and verdict are preserved in `output/paired-graph-review.json`.
No new Lean verification or historical priority claim is made.

## Extended double covers and Cartesian prisms

The [complete extended-cover proof](EXTENDED_DOUBLE_COVER_PARAMETERS.md)
establishes, for every finite simple H of order n,

    SF_2(E(H))=beta_2(E(H))=psi_sq(E(H))=Omega(E(H))
              =n+delta(H)=2n-nu(D(H)).

The proof covers nonbipartite bases as well. The independent-set deficiency
delta(H) equals the ordinary double-cover Hall deficiency. A TP-to-PZ rung
injection bounds every feasible representative pair, allowing selected
vertices in both colours. A separate minimal-forming proof counts the
union of deletion witnesses with capacity two per empty rung. Neighbours
of isolated selected rung edges are reserved and contribute no witness
capacity to the other doubly selected rungs. This proves the SF upper
bound without a general-graph assertion SF_2<=Omega.

There are exact nonnegative remainders describing every optimal feasible
representative pair and every maximum minimal forming set in this class.
For example, a maximum minimal set can induce a square; the statement is
an equality of optima and includes these nondissociation maximizers.

The common value and an attaining set have polynomial matching/vertex-cover
certificates. If H is bipartite, E(H) is its Cartesian prism and the common
value is 2 alpha(H). This closes all four parameters on every bipartite
prism, including all ladders and all hypercubes of dimension at least two.
Taking a prism eliminates any SF_2/beta_2 gap in a bipartite base.

For arbitrary actual M and any feasible white selected set T, disjoint
two-rung swaps provide a full auxiliary matching that pairs all selected
vertices directly with black terminals. Thus the true TH optimum is zero
for every nonnegative weighting on the whole extended-cover class.

Run `python3 scripts/check_extended_double_cover.py`. The independent
literal controls cover all 1,100 labelled bases of orders zero through
five, 1,065,509 selected subsets, all 54,160 minimal forming sets and their
65,820 empty-rung budgets, 36,306 feasible representative pairs on bases
through order four, and 5,036 direct-terminal constructions. These certify
14,236 white selected subsets, rather than 14,236 separate construction
calls. Fifteen larger matching/dual and attaining-set certificates cover
base orders 8,17,64,257,1024. All-size conclusions use the written proofs.

The initial three-parameter theorem and zero-completion algorithm received
independent ACCEPT at snapshot 5044cd7; the reviewer ran its complete
embedded checker and reproduced the report. That reviewer also supplied
a malformed external certificate exploiting Python negative indices. The
checker now validates vertex domains before indexing and rejects that
exact regression. The new SF theorem, its equality remainders and the
expanded checker received a separate independent **ACCEPT** at snapshot
6000a72. The reviewer reconstructed the all-size proof, extracted the two
Python files verbatim, ran the full unchanged checker with assertions
enabled, and confirmed equality of the generated and attached JSON data.
The exact negative-index fake certificate was also separately rejected
before graph indexing. The final note adds the requested explicit standard
partial-colouring definition; no proof or algorithm change was needed.
`output/extended-double-cover-review.json` preserves both complete verdicts
and the exact attached-file manifests. No new Lean verification or full
priority comparison is claimed.

## Source-dependent TH completion

The [complete proof note](EXACT_TH_OPTIMIZATION_AND_LADDERS.md) gives five
results, with an exact integer implementation and independent controls:

1. Binary labels, fixed to one at selected white terminals and zero at
   other white terminals, and equal along actual and chosen auxiliary
   edges, minimize exactly the genuine TH expense. Label-one cycles can
   overcharge individual pairs but never improve the minimum. Every
   minimizing labelled pair gives a truly optimal full matching.
2. Deleting complete disjoint retained paths and adding their fixed
   expense gives the exact retaining problem, while allowing all remaining
   HH paths to reroute freely.
3. A standard frontier DP needs just the label and auxiliary matched bit
   per active vertex. At most h+1 vertices are active, for shorter bounding
   side h. It uses O(n 4^(h+1)) state transitions; tuple and integer-bit
   overheads are stated separately. It returns an optimum and full witness
   or reports infeasibility. This solves the unrestricted exact optimizer
   question left in the preceding residual-Hall notes at bounded width.
4. On every full 2-by-n ladder, any monochromatic selected Q set with at
   most one occupied neighbour per selected vertex has a zero-expense
   full completion. Disjoint adjacent-column swaps give a linear proof
   and construction for every n, arbitrary M and nonnegative weights.
5. On the full 3-by-6r grid, an explicitly feasible all-white-Q selection
   and four unit actual edges per block have exact optimum r. Each black
   centre needs its own paid component, and nine printed auxiliary edges
   per block attain the bound. Thus the height-two universal zero-expense
   conclusion cannot extend to height three.

## Reproduction

Run from the repository root:

```sh
python3 scripts/check_source_label_dp.py
```

The checker uses literal perfect-matching enumeration and overlay scoring,
not the DP recurrence, to determine small true optima. Its output records:

| Control | Exact scope |
| --- | --- |
| Rectangular models | 750 models, 37,659 full-N scores; 631 have feasible selected sets |
| Masked boards | 180 models, 279 full-N scores; 92 are infeasible |
| Alternative scans / value-only | 122 / 61 comparisons |
| Independent colour enumeration | 26 models |
| Full ladder actual-match enumeration | 10,992 matchings for n=1,...,8 |
| Selected subsets covered by maximal-T certificates | 79,016 combinations |
| Ladder DP / translation and transpose controls | 114 / 228 |
| Full versus retaining 2-by-4r | 36 controls, r through 128, 1,024 vertices |
| Positive 3-by-6r family | 18 controls, r through 128, 2,304 vertices |

The controls include zero and 401-bit actual weights, a positive-cost
ladder violating the neighbour condition, an infeasible retained-path
example and a balanced board with an isolated vertex. Finite tests check
implementation; all-size statements have the written proofs above.
No Lean execution or verification is claimed.

## Scope and review

The proof/source snapshot 4a3aa6e received independent **ACCEPT for the
mathematics and optimizer**. The reviewer inspected both Python files and
reported 17,788 calls to the unchanged optimizer using a new literal-reference
harness, including 13,148 full-matching scores. That harness also reproduced
the 10,992 ladder constructions and all 36 cascade work-counter records.
The original attached checker initially could not run because the attachment
omitted its helper-module dependency. This package issue is corrected: the
exact independent enumerator, overlay scorer and serializer are now included
in the checker, whose only project import is the optimizer under test; it
creates its output directory. An isolated local full rerun reproduced all
three committed reports byte-for-byte. No claim is made that the reviewer
executed this corrected original checker.

The later height-three theorem received its own independent **ACCEPT**, based
on its all-r proof and explicit coordinates; that reviewer did not claim code
execution. `output/source-label-dp-review.json` records both exact review
scopes, responses and the completed packaging correction. The empty-board,
preprocessing-memory and forced-scan conventions are explicit in the note.

The earlier forced-cascade review and its identical retry both ended with
terminal infrastructure failures and no mathematical response. The prior
positive-attainment equivalence and unit 18-by-18 optimizer-choice result
retain their existing ACCEPT, scoped to their original input.

## Remaining questions

| Question | Current status |
| --- | --- |
| All four parameters on E(H), and on every bipartite Cartesian prism | Proved by the matching and witness-capacity theorem above |
| SF_2 and Omega on arbitrary Cartesian prisms | Proved; sharp SF/beta and SF/psi gaps and all positive equality bases classified |
| Extending four-way prism equality to arbitrary bases | False; the exact near-complete families above separate the parameters |
| Exact genuine TH expense at fixed grid width, with retained paths | Solved by the source-label DP, exponential in width |
| Zero expense for all feasible ladder and E(H) instances | Proved, arbitrary M and nonnegative weights |
| Zero expense for every feasible full grid instance | False: the explicit 3-by-6r family has expense r with unit actual weights |
| Arbitrary-width rectangular-grid SF_2=beta_2=psi_sq | Open; positive TH expense alone does not refute this equality |
| Improvement of the universal mixed-direction 5/6 coefficient | Open |
| Sharp gap under simultaneous specified degree/connectivity restrictions | Open beyond the previously proved exact classes and general bounds |
| Simpler incomplete-core equality structure for general bipartite graphs | Open; the exact remainders here describe only E(H) |

The new structural theorem does not extend automatically to wider grids:
if both sides of a rectangle are at least three, a corner has degree two
but all its neighbours have degree three. No adjacency-preserving map can
send that corner to an adjacent vertex. Such a rectangle therefore cannot
admit the adjacent-pair involution used for the extended-cover argument.
This rules out applying this particular structural criterion, without
deciding the equality itself. No arbitrary-width polynomial claim is made.
The sharp bipartite n/10 gap theorem and previous composition manuscript
are preserved. No email, submission or submitted-version edit is implied.
