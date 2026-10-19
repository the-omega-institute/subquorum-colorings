# Regular-tile review: incomplete submitted constructor context

The initial long-text task cd57f384 failed terminally during browser input,
with infrastructure_retry_exhausted/cdp_disconnected@typing after four
attempts. It has no mathematical verdict. The original stream is retained.

Replacement attachment task 7bafeabd-1b51-442f-b8d8-7fd9b7b5c962 completed
REVISE at 2026-10-19T22:34:34.508UTC, gpt_6/pro. The reviewer found a real
error in the hand-written constructor context: only (a-1,2),(b-1,w-1)
were listed as inward supports. At U(6,6,4), this literal list omits (3,2),
making endpoint (3,1) have occupied degree two and destroying its proposed
donor. Its phase catalogue then differs from the stated one. A review of
that literal packet must be REVISE.

The actual repository constructor two_leg_case has always included EVERY
odd inward support at rows3,5,...,a-1 and3,5,...,b-1. The original general
construction note states the same complete alternating lists. Their
selection count is 2n+2, n=(a+b)/2. Coordinate checks used this complete
source, so the omitted list was a submission-context error, not an error
in their implementation or a newly changed module family. The reviewer's
recommended corrected T* equals the existing repository constructor.

We make this definition explicit in the regular-tile note and submit a
short same-conversation correction. We do not change correct constructor
code, discard the REVISE, or inherit an ACCEPT for the corrected packet.
The reviewer explicitly validates regular-tile capacity under actual
degree-three hypotheses, the complete fixed rotor role barrier and the
all-length degree-four rotor chain, and explains why the remaining
budgets follow with the complete selection lists. A new verdict remains
separate. The subsequent minus-one joint classification and gate witness
were outside the reviewed input.
