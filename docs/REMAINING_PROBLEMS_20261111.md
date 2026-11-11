# Exact open questions after the 11 November completion round

The following are mathematical questions, not pending routine checks. Their
scope is kept separate from the proved results in COMPLETION_20261111.md.

1. **Incomplete-core equality.** The intrinsic theorem and all-subsets
   neighbourhood criterion recognize every positive equality graph exactly.
   Can the global criterion be replaced by a simpler structural description
   for arbitrary incomplete cores? Paired expansion alone is false: the
   disjoint K_(2,2)-core/matching-interface example admits six selected
   dissociation vertices per ten-vertex module. Complete cores with at
   least four vertices per side are already settled by the paired criterion.
2. **Bounded-degree optima.** Fixed minimum degree alone has sharp asymptotic
   density 1/10. This does not determine the optimum with a simultaneous
   fixed maximum degree. The new incidence inequalities are upper bounds,
   not sharpness claims. The older regular bounds and connected cubic
   constructions remain their own benchmarks; the exact connected cubic
   asymptotic optimum is not supplied by the present work.
3. **Routing several Hall compensations.** The simultaneous-port theorem
   now constructs and exactly optimizes physical completion with any number
   of centre relays and direct exterior TH/HH paths; it couples local routes,
   source assignment and exterior exposure in one weighted matching. For
   arbitrary extra non-centre relays, the residual Hall theorem now gives
   b_R+max(C_s,J_d) as a lower bound for every completion retaining specified
   paths R. A physically optimal extra TH family with a matchable direct-TH
   remainder attains b_R+C_s. This includes additional non-centre relays and
   certifies the exact retained-pair optima four and K+2 in the two grid
   examples. The remaining target is a general choice of regions and paths
   guaranteeing compatible completion, or an unrestricted exact TH optimizer;
   failure of one minimum-flow remainder is not an impossibility proof.
   Under the absence of zero-expense non-direct TH paths, the existential
   minimum-flow remainder criterion is now necessary and sufficient for
   attaining b_R+C_s. A unit-weight 18-by-18 example shows an arbitrary
   physical optimizer may fail while another succeeds, so choosing a
   compatible optimizer remains substantive even with positive weights.
   The 12-by-18 all-K example still separates source budget two from the
   unrestricted optimum K+1, even though each cheap entrance is exposable.
4. **Unit-weight numerical gain.** For weights at least one, the new theorem
   gives f>=k+ceil((A-sigma-(k-q)mu)/mu)_+, with A the total withdrawal
   potential, sigma the weighted regional Hall slack, and q the exterior
   white surplus. This includes arbitrary overlapping non-tight regions.
   This is a path-dependent lower bound. A useful universal numerical
   improvement needs an independent geometric lower estimate on A and
   control of physical routes; no such universal estimate is claimed here.
5. **Rectangular-grid triple equality and 5/6.** Neither the general triple
   equality proposed in Sahbi's grid question nor a universal improvement
   of the unit-weight 5/6 colouring coefficient follows from these results.
   The abstract endpoint countermodels refute specified counting shortcuts;
   they are not grid counterexamples to either target.

No candidate absent from this list is silently treated as resolved by
finite enumeration. No author approval, email send or submission is inferred
from mathematical review. No new Lean verification was performed.
