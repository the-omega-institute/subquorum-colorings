# Single-square classification review: initial REVISE and corrected follow-up

Original task122da19b-19c8-48d8-bbd2-29fcfcf1d961, conversation
conv_e03faff81c763d9b, terminal79338, completed at05:57:04UTC with REVISE,
observedgpt_6/pro. The exact response is archived in
output/single-square-parity-review-response.json. The reviewer confirms the
classification, parity budget, two-outward-corner freezing and8x8obstacle
survive correction of the prompt's inconsistent introductory capacity.

## Assessment and applied correction

The original request's introductory background sentence said r=2-t-h.
The actual original residual definition, used throughout the public verifier,
is r=2-t-h-s. This is verified directly at
develop/verify_grid_short_path_compensation.py, residual().
The ledger rho=d/2-r=(t-b+s)/2 in that same request was correct.
Every receiver tile in the supplied single-square theorem and the supplied
neutral8-by8fixture has s=0, so this input typo changes none of those proofs
or numerical claims. The later6-by6two-square fixture has s=2 at one tile
and must use the complete formula; the physical checker does so.

The review offers either adding+s to charge with an unadjusted capacity, or
using the adjusted capacity r_eff=2-t-h-s. The repository already uses the
second convention under the name r. No source arithmetic, original charge,
or theorem conclusion is changed. Adopting an extra+s on top of the existing
adjusted r would incorrectly count saturation twice and was not done.

The review's4x4example is independently checked: the upper-right deficient
tile has t1,p1,b2,h0,s1,d0, actual adjusted r0and charge0. Its unadjusted
capacity is1and would give the incorrect charge-1without the correction.
The companion physical checker records this exact case separately.

Applied the three requested exposition clarifications: the local turn lemma
now states that the turning vertex itself lies in the square; the forced-label
proof invokes unused face incidences for length-one arms; coordinates/tile
indices are explicitly zero-based. The prior proofs already establish these
facts. The entire general frozen and counting argument remains unchanged.

The subsequently added all-length odd/odd neutral corollary, finite Lean
witness and6-by6two-square fixture were not supplied in the original turn.
Separate their verification scope from any eventual review verdict.

## Original-conversation follow-up

After the original completed, taskfc9e74ce-9a65-4ad8-a9d1-e3aec3bf50df was
submitted in the same conversation, original streaming terminal62212, worker
lt4r7693kj-go-4. It completed at06:09:07UTC with REVISE, observedgpt_6/pro.
The full response is output/single-square-parity-followup-response.json.
It explicitly supplies
the actual adjusted capacity, applied clarifications, all-length odd/odd
neutral family and6x6two-square saturated-attachment example. It requests a
fresh assessment of these results together, not a second uncorrected review.
The reviewer accepts the corrected original result, neutral family and all
feasibility/freezing/ledger calculations of the6x6fixture. Its remaining
objection is valid: the fixture's aligned square has two outward-matched
corners, so it cannot isolate removal of uniqueness from the earlier
four-outward-matched two-unit theorem. The example refutes two-unit payment
from freezing plus an aligned square alone, and an independent one-unit
assignment to each of these two overlapping squares. Only one square is
aligned. These are now the explicit claims in Section5; the four-outward
extension remains open. The raw occupancy contribution-1and saturated
endpoint contribution+1are now stated separately. No numerical check or
earlier theorem changes, and no overall ACCEPT is inferred.

The subsequent exact colorwise ladder criterion is outside both review inputs.
