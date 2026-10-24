# Accepted attachment-corrected collar review

Original task 2e81689f-ebdb-4ef9-902c-0c3af27da282 completed ACCEPT at
03:31:45 UTC on 19 October 2026, observed gpt_6/pro. The exact task
response is archived in output/attachment-collar-oracle-response.json.
No mathematical revision was requested.

The reviewer independently derives the deficient-only surplus bound, the
internal attachment ledger, Q=k+eta, the corrected parity j+Q and the
source-union estimate. It checks both physical parity/debt counterexamples
and the bent residual-path construction at every length, explicitly
distinguishing failed regional rules from the whole-grid target.

Its additional boundary check is j=j_DD+sigma+eta, where j_DD counts
deficient-to-deficient boundary matching edges. Hence j+Q has the same
parity as j_DD+sigma+k. In particular, incoming saturated endpoints do
not create an independent parity resource.

We checked that every source charge remains measured in the original
configuration. Boundary crossings are retained and receivers, deficient
tile surplus and saturated endpoints are each counted once.

The review did not execute code or Lean, establishes no external priority
claim and does not cover the later shared-blank compensation theorem.
Full Verification run 39194639195 at 7a5eeca completed successfully.
