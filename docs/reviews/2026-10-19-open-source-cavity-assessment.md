# Partial-source cavity theorem and sharp obstruction: accepted review

Task 112a9b99-7049-43d8-929a-c3a9f9019b35 completed ACCEPT on 19 October
2026 at 13:29:23 UTC, observed gpt_6/pro, in the existing conversation
conv_801d22eac492fed2. The exact response is archived in
`output/open-source-cavity-review-response.json`, extracted from the original
completed stream and checked against the authoritative terminal task state.

The reviewer accepts the nonnegative partial prescribed-source phase,
complete row-band accounting, exact open-cavity identity, physical donor
incidence and weighted allocation, normalization preservation, and the
arbitrary-count sharp family with D_C=2 and zero foreign phase. The review
agrees that the family refutes automatic two-unit credit for each touching
source, without refuting the global coefficient-one target.

Two requested clarifications are incorporated in the construction. Every
unlisted vertex is blank, including outside the cavity, except for the
prescribed supports and listed sharp-flank selections. The deleted even-row
sites c,c+2,c+4 are optional filler, while the prescribed supports at row 6
and at (8,c+3) are retained. Direct source-table extraction confirms these
support coordinates. No theorem, parameter range or construction changes.

One incidental count in the response calls [c-1,c+5] a six-column interval;
it has seven columns. The submitted proof uses its endpoints and the correct
25 intervening columns between envelopes spaced 32 apart, so this wording
error has no mathematical consequence. Full-source phase two and phase zero
inside the cavity remain explicitly distinct.

The reviewer read the written proof and did not execute Python or Lean.
The 90 physical cases, eight symmetry images, and cumulative 120 scoped
Lean declarations have separate execution receipts. A resumed regression
of the existing open-source controls passes with the same counts. All seven
CI checks at research revision 5ccdda0 have now passed, including the previously
running width-11 certificate check. That CI predates this archival revision.

The accepted scope excludes arbitrary positive bent receivers, existence of
enough low-multiplicity cavities, uncontrolled negative comb exits, and the
unrestricted grid triple equality. Whole channels between comb walls are a
next research candidate, not a theorem certified by this review.
