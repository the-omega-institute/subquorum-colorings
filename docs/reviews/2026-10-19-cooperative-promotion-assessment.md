# Independent assessment of cooperative-promotion review

19 October 2026. Original broker task0204a4ca-b994-4252-878f-0eb4b0569340
completed REVISE at04:34:40UTC, observedgpt_6/pro. It was collected by
the same task after transport EOF, without submitting a duplicate.
The exact response is in output/cooperative-promotion-oracle-response.json.

## Real correction

The previous note incorrectly said that the second bridge tile's P was
matched inside the bridge. Its actual edge goes to the omitted column-zero
deficient tile. The first bridge tile also has two actual incidences:
one to the central deficient tile above, and one to an omitted deficient
tile on its left. Thus the bridge pair adds two crossings and removes
one previous crossing, increasing j by one. No mate here is saturated.

The actual checked-in fixture, independent coordinate checks and all-r
charge formulas already use those correct matching edges. The error was
in the written explanation, not a change to the construction or formula.
The revised note states each incidence and the net crossing change.

## Clarifications accepted and incorporated

The witness vertex set is explicitly the k internally attached saturated
owners. It is not all Q=k+eta saturated endpoints. Complete one-per-T and
marked-cap reservations and inclusion of unused free blanks are repeated
where the witness graph is defined. Using all Q would need a -eta term.
The underlying earlier witness proof and checker already used k.

Receivers are disjoint from assigned sources, and combined cores are
pairwise disjoint with an explicitly controlled remainder. The graph
convention is finite/simple/undirected. The runtime includes the initial
examination through (|M|+1). The exhibited absorption sequence is described
without implying confluence or that all its vertices avoid boundary columns.

## Scope

The reviewer accepts the bundle/single/cycle proofs, same-state gap lemma,
transition coefficient under its stated hypotheses, physical8x4 fixture,
stacked formulas after correction, and explicit all-r repair. It also
accepts the earlier general tile-cycle inequality d<=nu_R by independence
of unit-square boundaries. Its assertion about the separate all-subset
staircase fixture is conditional because that earlier matching list was
not in the supplied input; no expanded review claim is made for it.

The reviewer did not execute the code or certify novelty. It did not
review PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md or FrozenPromotion.lean,
which were developed while this review was pending. That new obstacle
answers its remaining normal-form question, but does not change the
historical REVISE verdict. A follow-up may review the corrected note and
new result together; no ACCEPT is inferred before it returns.
