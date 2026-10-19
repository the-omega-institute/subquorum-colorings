# Exclusive-strip review: correct mechanism, repaired geometric proof gap

Task fcb4aa67-e6d9-4f74-af8d-c0c33fcd2160 completed at
2026-10-19T11:57:14.858Z, observed gpt_6/pro. Verdict: REVISE.
The response is preserved in `output/adaptive-strip-compensation-review-response.json`.
Its original stream failed during observation, but the same task was already
completed and was recovered by its original id. It was not restarted.

The review accepts the exclusive compensation inequality, weighted bipartite
cut and scalar relaxed-model optimum. It finds a real error in the first
all-p feasibility proof: facing chamber endpoints can be at distance three,
so distance four cannot be used to exclude adjacent supports. This is a
proof gap, not an infeasible-example witness.

The correction retains the verified original coordinates and gives the full
support template. A later source has no support in the row immediately
above its chamber origin. That excludes the only possible support adjacency
across the distance-three facing-chamber interface. Other endpoint
separations are at least four. The same explicit argument is transposed
where reused in the new capacity-aware construction.

Other incorporated clarifications: individual tip conservation follows
from per-strip upper bounds plus the accepted exact global sum; the fixed
family completion class has no additional endpoint component meeting G;
O,J use union end membership; optional edge deletions need uniform vanishing
for a uniform claim; feasible flow witnesses, in addition to cut and
independent-set witnesses, certify exact optimization.

Follow-up c91ffe7a-1550-4fe1-94b7-087d8bc51f8b is dispatched in the same
conversation conv_b78981283a599e89, original stream 32679. No final ACCEPT
is inferred. This review predates the capacity-aware and remote-rung notes,
which have their own separate live review.
