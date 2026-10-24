# Closed-cavity review: corrections and scope

The independent task 9d682a80-b279-4f0c-8574-22c217421985 completed
REVISE on 19 October 2026 at 12:50:24 UTC, observed gpt_6/pro.
The exact response is in output/closed-source-cavity-review-response.json.
It reviewed the earlier closed-cavity note, not the later escaping-comb
flux extension or the mixed-direction source lemma. No ACCEPT is claimed.

The reviewer accepted the conditional two-partition algebra and physical
donor-incidence accounting. We agree with its correction of the statement
that an occupied saturated-tip rung refutes sufficiency: the example
shows incomplete coverage by the older sufficient criterion. The revised
note explicitly distinguishes the lower sparse-tip mouth corridor.

The requested boundary cases, exact tiling phase, shifted source label
table, normalization operation and symbolic nested-family interface
bounds are now explicit. Closure quantifies over every endpoint component
meeting the cavity, including any unlisted component; there is no exception
for a component with an inconvenient shape.

The two proposed source-phase counterexamples do not satisfy positive
physical alignment. A one-column translation makes original raw charge
-1, whereas the theorem requires the prescribed +1 source phase. An
even-constant row reflection does not preserve the fixed row pairs.
The revision gives the exact allowed parities rather than leaving the
meaning of positive alignment to a cross-reference.

An extra support-envelope clearance assumption is unnecessary for receiver
containment: the cavity is a union of complete physical row/column pairs,
and after the proved endpoint-free extreme columns are removed, it is a
union of complete shifted pairs. Every endpoint square is therefore
contained. A prescribed support outside the cavity can still force its
neighboring corner inside it. The revised label proof makes this explicit.
For the first boundary row, the forcing inside support is the next one
in row 3, not the preceding row 1 used in the review's proposed sketch.

The new whole perpendicular-source proof separately shows phase gain at
least two using adjacent chamber-flank exclusions. Its geometry is written;
the corresponding local exclusions and conditional arithmetic are Lean
checked. The old review does not certify that new result. Universal
cavity coverage, partial foreign sources and arbitrary positive bent
components remain open.
