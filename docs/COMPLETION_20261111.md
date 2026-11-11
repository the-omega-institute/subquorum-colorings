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
The grid result appears in a separate appendix because it addresses a
different optimization model. The final editor accepted coauthor
circulation subject to an explicit disjoint-union hypothesis; that
hypothesis is now inserted. The review manifest records the exact
mathematical review scope and the implemented corrections. All infinite claims above have written proofs.

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

## Simultaneous-port continuation

The subsequent same-day round is indexed in
[`SIMULTANEOUS_PORT_COMPLETION.md`](SIMULTANEOUS_PORT_COMPLETION.md) and
[`HALL_SLACK_SHARED_BUDGET.md`](HALL_SLACK_SHARED_BUDGET.md). It supplies an
exact physical completion theorem for several centre entrances, a q-root
budget-attainment criterion, arbitrary positive-slack Hall accounting,
an 8-by-12 unit obstruction and a 12-by-18 all-K source-budget gap.
The integrated manuscript now has fifteen pages. Previous round evidence
and its review manifest remain version-bound to their own source.

Reproduce the new finite controls from the repository root:

```sh
python3 scripts/check_multiport_completion.py
python3 scripts/check_hall_slack_budget.py
```

The first report covers 1,721 weighted assignment controls, 4,373 exterior
graphs, 23,611 entrance sets, 384 physical weighted models, a direct exterior
HH control with two TH centres at surplus one, and all 18,061 auxiliary
matchings of a 4-by-10 board. The second report covers 1,259,376 terminal
bijections and 2,355,108 weighted regional identities. The 12-by-18 family
has a general all-K proof and a fixed row-by-row attaining matching;
the twelve weighted samples are implementation controls.

The further coordinate note
[`RETAINING_PAIR_EXACT_UNIT_COST.md`](RETAINING_PAIR_EXACT_UNIT_COST.md)
sharpens the unit example: retaining its specified bad pair has exact
minimum expense four, while the unrestricted optimum is two. The proof
excludes HH compensation into its deficient region and shows every incoming
TH compensation needs at least two actual edges. It includes a complete
row-tiling construction and an independent standard-library checker:

```sh
python3 scripts/check_retaining_pair_optimum.py
```

This strengthening is a separate coordinate note; the accepted fifteen-page
PDF remains bound to its original scientific revision and states the valid
weaker retaining-pair lower bound three.

## Residual physical compensation continuation

[`RESIDUAL_HALL_COMPENSATION.md`](RESIDUAL_HALL_COMPENSATION.md) gives a
general lower bound for every full completion retaining specified alternating
paths R. For any residual black-terminal region D, its direct selected
neighbourhood yields a demand d. Let h_D be its maximum physical HH supply,
s=(d-h_D)_+, C_s the minimum expense of s disjoint outside-TH paths, and J_d
the minimum cardinality-d endpoint-assignment expense. Then

    f_R* >= b_R+max(C_s,J_d).

The two bounds charge the same additional expense. A successful direct-TH
remainder matching for some optimal C_s family certifies equality with
b_R+C_s. This criterion permits extra non-centre TH relays and arbitrary
free HH routing. It gives exact retained-pair optima four on the unit
8-by-12 board and K+2 for every integer K>=2 on the 12-by-18 board; their
unrestricted optima remain two and K+1. On the second board, a centre and
an exterior deficit compete for a single HH source, so only their union
forces the K-cost compensation. Two additional all-K controls show neither
residual relaxation dominates the other.

Reproduce this continuation from the repository root:

```sh
python3 scripts/check_residual_hall_compensation.py
```

The report covers 344 seeded physical models, 984 regional checks, 6,894
independent full-matching scores, 473 literal path-packing controls and 972
exact completion certificates. The checker independently reconstructs the
printed complete tiling and the flow dual/cut certificates. General and
all-K conclusions have written proofs. This coordinate note is proposed
appendix material; the fifteen-page PDF and submitted version are unchanged.
