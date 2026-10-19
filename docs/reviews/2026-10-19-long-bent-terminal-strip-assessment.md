# Long-arm review: REVISE, with a corrected physical recurrence

19 October 2026. Original task c747589c-8d17-4915-9519-720f2f2b87ac completed
at 09:05:04 UTC, observed gpt_6/pro. Verdict REVISE. Exact response:
`output/long-bent-terminal-strip-review-response.json`. This is not an ACCEPT.

The reviewer identifies a real adjacency error in the final even-arm wave:
the old text treated m(p_1)=(1,c) as adjacent to p_2=(3,c), and similarly
used a mate two rows away at subsequent steps. Finite frozen certificates
were correct, but they do not repair that written induction by themselves.

The corrected recurrence starts with the already frozen chamber corner (1,c).
Its retained mate is p_1, adjacent to p_2. After p_(j-2) has frozen for even
j>=4, its retained mate p_(j-1) is adjacent to p_j. The fixed inside T support
supplies the second neighbor at every step. This repairs the same arbitrary
simultaneous bundle argument. A new Lean statement checks the all-length
physical recurrence under its explicit actual-mate identities.

The note now defines thin as containment in two consecutive rows or columns,
so preservation under endpoint deletion is immediate. It explicitly counts
distinct complete initial long sources. The obstruction statement now excludes
only fixed-depth prefixes of the defined nonterminal inward bands; it does
not exclude taking a remote terminal strip at an arm-dependent distance.
The contradictory saturated-baseline sharpness clause was already removed
before the response arrived; the sharp construction uses the sparse baseline.

The reviewer checks the corrected counts, full original receiver charge,
band feasibility and endpoint-free strip budget. It finds no counterexample
to the perpendicular separator and confirms the exact disjoint ledger once
the recurrence and inherited-class clarification are supplied. This judgment
does not independently validate the later transverse-comb extension or its
two-ending-comb obstacle. A follow-up review records those scopes separately.
