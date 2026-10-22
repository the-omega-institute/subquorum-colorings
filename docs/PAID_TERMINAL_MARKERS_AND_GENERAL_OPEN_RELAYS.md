# Paid-terminal markers preserve payments through open-strand surgery

## Hypotheses

Fix a matching-closed packet with actual matching M, PP auxiliary matching
A, original interval units I, and S_J-B=|I|+b-k. Choose r different
unpaid original alphas and r different original betas, one free terminal
on each. Their internal tails stay unchanged; let U be the chosen ends.
Every other original alpha has an injective payment by an original unit
of I, witnessed at a specified one of its TP free ends. Require that this
access certificate depends only on that endpoint, unchanged physical
T,P data and the original unit identity, rather than its original path
owner or a mutable actual-cycle edge. The witnessing endpoint remains
free in the replacement.

All other open strands may now be used internally, including paid alphas,
unselected betas and mixed paths. Their original free ends F stay N-free.
The complete replacement N is one matching: it covers every original PP
vertex and every chosen end in U, leaves every end in F uncovered, and
changes no edge on the selected alpha/beta tails. It has permitted,
stable geometric witnesses. Closed PP cycles are allowed as well. No
existence of N is assumed beyond these explicit conditional hypotheses.

Contract the selected tails as in the mixed-relay note. In the reduced
graph M covers every relay/cycle vertex and no vertex of U; N covers all
vertices except F. Original physical labels at U are preserved by the
contracted tails. Each endpoint in F keeps its original physical label.

## Put the signed defect at the paid terminal

Use TP=minus, BP=plus on U. On every other open strand give its original
free ends the reverses of their physical labels, and require every A
edge to cross signs. The remaining actual-edge signs can be chosen as
follows:

- A mixed relay has all M edges crossing signs.
- A paid alpha has exactly one plus--plus M edge, namely the actual
  edge incident to its specified paid TP end; all other M edges cross.
- An unselected beta has exactly one minus--minus M edge, chosen at
  either original end; all other M edges cross.
- Every original cycle has alternating signs, with either global flip.

To see existence, list an old open strand from one free end to the other.
Its edges alternate M,A,...,M. Starting with the required end sign, flip
at every edge except the one marked M edge. On an alpha start at its
paid end, whose colour is plus; the first edge then has two plus ends,
and the even number of remaining sign flips ends at plus. Betas are the
minus version. Mixed ends are opposite, so flip at every edge. Thus all
A edges cross, including when an open strand is a single actual edge.

Each plus--plus actual edge is one distinct paid-terminal marker with
one distinct original interval payment. These are actual edge identities,
not one credit per newly exposed auxiliary endpoint.

## General endpoint identity and safe transfer theorem

Let h_minus,h_plus count same-sign N edges. The N-covered vertices are U
and all old A-covered vertices, so their sign sum is zero. Hence
h_minus=h_plus=:h. For any final reduced component D, let M_plus(D),
M_minus(D), N_plus(D), N_minus(D) be its same-sign edge counts. Then

    N_plus(D)-N_minus(D)-M_plus(D)+M_minus(D)
      = -1 for alpha, +1 for beta, 0 for mixed/cycle.       (1)

Proof. N incidences minus M incidences leave exactly plus the U signs
and minus the F signs. The latter are the physical signs by the chosen
reversal. All crossing edges contribute zero; dividing the signed
endpoint-incidence equality by two gives (1). QED.

**Paid-terminal transfer theorem.** Every final alpha can be assigned
either a different original paid-terminal marker, with its original
interval unit, or a different minus--minus N edge. Thus at most h final
alphas need compensation beyond the transported old payments. If all
new N edges cross signs, every final alpha inherits a distinct old
interval payment, even though paid original alphas may have been split
and reconnected internally. Consequently S_J>=B for this packet.

Proof. For an alpha, rearrange (1):

    M_plus(D)+N_minus(D)=M_minus(D)+N_plus(D)+1.          (2)

If M_plus(D)>0, choose one of its actual paid-terminal markers. That
marker is incident to its original paid TP end. The actual edge remains
in D, and that end is still N-free by hypothesis. Hence the endpoint
and its unchanged access certificate belong to this very final alpha.
Transport the original interval payment through this endpoint.

Distinct final components have disjoint actual and auxiliary edge sets.
They therefore choose different markers, and the original payment map
was injective, so they receive different interval units. No old unit is
assigned twice. If an alpha contains no positive actual marker, (2)
gives N_minus(D)>=1. Choose one such edge; again different components
choose different edges. This bounds the number of remaining unpaid
alphas by h. A component containing several markers receives only one
payment; unused original units are not counted again elsewhere.

When N is coherent, h=0. Thus every final alpha receives an injective
allocation from I, and the unchanged exact ledger
S_J-B=|I|+beta_N-alpha_N proves S_J>=B. Equal numbers r of original TP
and BP ends were newly covered and no PP vertex was left uncovered, so
there is no cut debt. QED.

The theorem preserves payments through their free endpoints. It does
not assert preservation of the old one-to-one path-owner assignment,
the old path shapes, or access depending on an entire old strand.

The scalar consequence alone is already implied by the hypotheses:
the u=k-r old injective payments give |I|>=u, and the r selected distinct
betas give b>=r, so |I|+b-k>=0 before surgery as well. The new content
is the assignment after surgery and the explicit bound on lost payments,
not a stronger scalar inequality. A general grid application still
requires an independent argument that enough donors and legal routes
exist, or a different certified budget for the remaining unpaid alphas.

## Count bound and orientation certificate

Write u=k-r for the number of originally paid alphas and v=b-r for the
number of unselected betas. There are exactly u positive actual markers
and v negative actual markers. Applying (2) componentwise gives

    alpha_N<=u+h, beta_N<=v+h.                          (3)

For coherent N there is some 0<=d<=min(u,v) such that

    alpha_N=u-d, beta_N=v-d, mixed_N=g+r+2d.            (4)

The exact signed ledger gives beta_N-alpha_N=v-u. The r newly covered
TP/BP pairs reduce the total number of open components by r. Together
with (3) for h=0 these facts prove (4). Additional old alpha/beta pairs
may cancel; no loss of a payment follows from their disappearance.

After all open-strand marker locations and designated endpoints are
fixed, a relay's vertex colours are
fixed by its designated free end and marker location. Only closed-cycle
flips remain variable. The same XOR constraint graph can test coherence
of a supplied N. If its forest assignment has q nonforest constraints,
there are 2h<=q violating N edges, so at most floor(q/2) final alphas
lack a transported old payment. Every leftover unit or separate external
payment must retain its own geometric access certificate and identity.

Changing the marker location can change coherence. Moving it away from
the paid end without an independent transport argument loses the key
payment guarantee. The theorem supplies a sufficient certificate; it
does not solve the search over N, cycle flips and paid-end choices, nor
establish a universal grid inequality or 5/6 improvement. It composes
with actual closed-cycle normalization because that exchange preserves
the open paths and paid-terminal incident actual edges. The global
outside-overlap correction is retained once.

## Verification boundary

The completed checker reports 24,128 complete replacements and 45,608
signed controls, including 7,916 coherent certificates. It transports
14,868 old payments and checks 14,184 distinct error witnesses over
the cases; these are aggregate occurrences, not distinct physical grid
resources. There are 7,088 low-rank certificates with all final alphas
paid. The record is
`output/paid-terminal-marker-compensation-validation.json`.

The misplaced-marker control has eight full endpoints. Let the actual
edges be t--t', p--p', q0--x and y--q1, and let A contain x--y.
The ends t,t',q0,q1 are TP and p,p' are BP. Suppose the old payment is
available only at q0. Place the positive actual marker incorrectly at
y--q1, giving signs q0+, x-, y+, q1+, t-, p+. Then
N={t--y,x--p} is coherent for these signs. Its final alpha has ends
t',q1, whereas q0 lies on the final mixed path ending at p'. Thus that
marker does not carry the payment available at q0 into the final alpha.
With the correct marker at q0--x, this N is incoherent and the theorem
does not assert automatic payment. The example refutes arbitrary marker
relocation without transport, not the packet inequality or the theorem.
It is an abstract endpoint example, without a claimed grid realization.

The checker uses original alpha, beta and mixed internal relays, both
paid-end choices, cycles, arbitrary complete N replacements and all
cycle flips. It reconstructs final components, verifies (1), transports
payments only through marker-adjacent surviving endpoints, checks their
unit identities and nonreuse, and bounds the unmatched alphas by the
distinct same-sign N-edge witnesses. These are finite checks for the
general proof, not evidence of universal geometric availability.
Unit identities in these models are distinct abstract indices representing
the assumed injective original payment map. Selected tails are restored
as one-edge representatives of the contracted paths; the written proof
permits arbitrary unchanged tail lengths.

The general endpoint identity and marker-or-error witness inequality are
verified in the supplied Lean source from a sign-occurrence incidence
permutation. The graph realization, marker-to-physical-terminal transport,
actual distinct edge identities and interval access hypotheses remain
in the written proof and graph checks. Universal compensation and the
rectangular-grid triple equality remain open.

The nine audited endpoint-accounting statements in
`formal/SubQuorum/MixedRelayEndpointAccounting.lean` passed local Lean
4.33.0. The three added marker statements and execution scope are
recorded in `output/paid-terminal-marker-compensation-lean.json`.
The earlier six-statement mixed-relay review input does not include
this extension. Separate independent review 04e51f70 returned ACCEPT
of the conditional transfer theorem, its nonreuse and error budget, the
misplaced-marker obstruction and all stated counts. It confirms that
the scalar bound already follows from the original hypotheses. The
full response is archived in
`output/paid-terminal-marker-compensation-oracle.json`. The review is
source-level mathematics and does not independently execute the checker
or Lean. Its optional wording clarifications are applied above.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
