# Completed results and remaining questions, 11 November 2026

The universal theorem on the preceding branch proves

    SF_2(G)-beta_2(G) <= floor(|V(G)|/10)

for every finite simple bipartite graph. The present continuation answers
several further questions about equality, degree constraints and safe
composition, and extends the separate grid compensation accounting.

## Proved here

- [Intrinsic equality](INTRINSIC_STAR_FORMING_EQUALITY.md): exactly n/5
  degree-two vertices; graph-determined isolate/witness/core layers;
  a unique maximizing minimal forming set; an exact global neighbourhood
  recognition criterion; and a paired-neighbourhood classification for
  complete cores. This is unrounded positive equality, not arbitrary
  attainment of the floor bound.
- [Degree refinements and constructions](DEGREE_STABILITY_AND_FIRST_EQUALITY.md):
  (10D+2)g<=Dn+n_2, and (10D+2d-4)g<=Dn under the stated degree
  hypotheses. Fixed minimum degree, with unbounded maximum degree,
  preserves asymptotic optimal density 1/10 even under two-connectivity.
  H is unique at order ten. The all-r six-cycle family attains n/10
  with no spanning H-factor, so local H-block composition is not a
  complete equality classification.
- [General boundary composition](GENERAL_BOUNDARY_SAFE_COMPOSITION.md):
  a sufficient finite safe-deletion condition independent of the ambient
  graph, protected lower witnesses, and exact additive compositions
  under explicit boundary hypotheses. A five-vertex graph shows why
  retaining boundary activity matters.
- [Several Hall regions](MULTIPLE_HALL_REGION_BUDGET.md): a simultaneous
  conservation identity for arbitrarily overlapping or nested tight
  sets, normalization by maximum endpoint multiplicity, and unit-weight
  paid-path lower bounds. Explicit endpoint models show both the failure
  of unnormalized addition and the information lost when exterior
  withdrawals are discarded. No geometric realization of these abstract
  models is asserted.

The readable star-forming manuscript is `manuscript/starforming-gap.tex`.
Its proofs are self-contained apart from the identified literature context.
The grid result is kept as a separate proof because it addresses a different
optimization model. All infinite claims above have written proofs.

## Reproduction

From the repository root:

    clang++ -std=c++17 -O3 -Wall -Wextra scripts/check_degree_stability.cpp -o /tmp/sahbi-degree
    /tmp/sahbi-degree
    /tmp/sahbi-degree --intrinsic
    /tmp/sahbi-degree --cycle 1
    /tmp/sahbi-degree --cycle 2
    /tmp/sahbi-degree --cycle 3
    /tmp/sahbi-degree --cycle 4
    /tmp/sahbi-degree 3 3
    /tmp/sahbi-degree 4 4
    python3 scripts/check_minimum_degree_sharpness.py
    python3 scripts/check_cycle_equality.py
    python3 scripts/check_boundary_safe_composition.py
    python3 scripts/check_multiple_hall_budget.py

The corresponding JSON reports in `output/` state their finite scopes.
The intrinsic checker exhausts 65,536 interface presentations, checks the
one-side formula 131,328 times, and compares four twenty-vertex models
with literal full-subset formation/minimality enumeration. The general
degree checker tests 108,871 graph presentations and 29,658,535 literal
subsets; it also crosschecks the private-neighbour formula. The boundary
checker tests 82,110 physical ambient graphs and 286,368 safe deletions.
The Hall checker tests 48,754 abstract terminal bijections.
These are controls for the proofs, not substitutions for them. This
continuation adds no Lean verification; older formalizations retain
only their stated scope.

## Questions still open

A simpler local characterization for arbitrary incomplete cores remains
open; the all-subset recognition criterion is exact but exponential as
stated. The new bounded-degree inequalities are not claimed optimal for
every degree range; the optimal connected cubic coefficient remains
unresolved. The Hall theorem does not prove compatible physical routing
or full-board completion from endpoints, nor the universal unit-weight
5/6 improvement or the proposed rectangular-grid triple equality.
Those remaining questions are not marked solved by finite evidence.

The coauthor-facing draft does not choose author order or a venue and
records no approval by the correspondent, email send or submission.
