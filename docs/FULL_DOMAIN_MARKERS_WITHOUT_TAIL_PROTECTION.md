# Full-domain payment markers without protected selected tails

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The earlier mixed-relay and paid-terminal marker theorems suppressed the
selected source and donor tails and required those tails to stay unchanged.
That restriction is unnecessary for the signed transfer argument. Keeping
the entire original endpoint set gives a simpler incidence identity and
permits surgery inside selected source and donor paths as well. This matters
geometrically: the reflected zero-capacity corridor repair cuts an auxiliary
pair inside the selected beta path, so it is outside the protected-tail
formulation even though its complete replacement has zero debt.

## Hypotheses and full-domain signs

Fix a finite endpoint set P, a perfect actual matching M on P and the
original PP auxiliary matching A. Every A-free vertex has its physical
TP or BP label. The original alternating paths have counts k,b,g and
the exact physical ledger is S_J-B=|I|+b-k.

Choose r distinct original alphas and r distinct original betas, and
one original free endpoint on each, forming U. Let F be all the other
original free endpoints. Let N be any matching with covered domain

    dom(N)=dom(A) disjoint-union U=P minus F.             (1)

All edges have the required stable permitted witnesses. No original PP
endpoint becomes free. No edge on an original selected tail is required
to remain auxiliary-paired as before. The actual matching M stays fixed.
Internal surgeries may visit any original open path or cycle.

Every unselected alpha has an injective old payment from I at a designated
TP free endpoint. Its access certificate depends only on that surviving
endpoint, unchanged T,P and the original interval identity. It does not
depend on an old path owner or mutable path geometry. Mark the actual
edge incident to that designated paid endpoint.

Give each selected endpoint in U its physical sign, TP minus and BP plus.
Give each endpoint in F the reverse physical sign. Then choose signs on
the internal vertices of every original strand as follows:

- A selected alpha has opposite endpoint signs: minus at U and plus at F.
  Alternate across all its actual and auxiliary edges.
- A selected beta has plus at U and minus at F; again alternate everywhere.
- An original mixed path has opposite reversed endpoint signs and alternates.
- An unselected alpha has plus at both ends. Its paid-terminal incident
  actual edge is plus--plus; all its other edges cross signs.
- An unselected beta has minus at both ends. One terminal-incident actual
  edge is minus--minus; all its other edges cross signs.
- On a closed original cycle use either alternating orientation.

All original open paths have odd alternating length M,A,...,M, so these
assignments exist, including single-edge paths. Every A edge crosses.
Every positive actual edge is precisely one of the k-r old paid-terminal
markers; there are b-r negative actual markers. No contraction is used.

## Full incidence theorem and payment transfer

For every final component D of the coloured multigraph M union N,

    ends(N|D) multiset-union (F intersect D)=ends(M|D).   (2)

Indeed M covers every vertex once, while N covers every vertex except F
once. Vertices of U now have BOTH incidences, so they make no boundary
term. Each vertex of F has only its actual incidence. Consequently

    N_plus(D)-N_minus(D)-M_plus(D)+M_minus(D)
      = -1 for alpha, +1 for beta, 0 for mixed/cycle.    (3)

To prove (3), subtract the M endpoint-sign sum from the N sum in (2).
The result is minus the sign sum on F, which equals the physical sign
sum of the final endpoints. Every same-sign edge contributes plus or
minus two, and crossing edges contribute zero. Divide by two. This is
the existing general Lean incidence theorem with chosen=[] and relay=F;
the permutation concerns sign occurrences, while (2) supplies its graph
interpretation. No new formal graph-realization claim is made.

The N-covered domain is dom(A) disjoint-union U. The first part is paired
by crossing A edges and U has r signs of each type. Hence N has equal
numbers h of positive and negative same-sign edges.

For a final alpha, (3) gives

    M_plus(D)+N_minus(D)=M_minus(D)+N_plus(D)+1.          (4)

If it contains a positive actual marker, the marker's old paid endpoint
is still in F and incident to that unchanged actual edge. It is therefore
a degree-one endpoint of this final component. Its original interval
payment remains accessible. Different final components select different
actual markers and hence different old interval units. This transports
payments without retaining any old path-owner assignment.

If there is no marker, (4) supplies a negative N edge in that component.
These error witnesses are distinct across final alphas. Thus at most h
final alphas lack a transported payment. If N is coherent, every final
alpha receives a different original payment, with no protected-tail
hypothesis. An error witness bounds remaining demand; it is not itself
a donor resource.

Writing u=k-r and v=b-r gives alpha_N<=u+h and beta_N<=v+h. If h=0,
for some 0<=d<=min(u,v) the exact inventories are

    alpha_N=u-d, beta_N=v-d, mixed_N=g+r+2d.            (5)

Proof: the remaining TP/BP end counts are 2k+g-r and 2b+g-r, respectively.
Subtracting gives beta_N-alpha_N=v-u; adding gives total open components
k+b+g-r. Combine with the two count bounds. All interval identities and
the zero-debt ledger remain unchanged. The fixed open-strand signs and
variable cycle flips admit the same grounded XOR/forest certificate,
with at most floor(q/2) marker-free final alphas for q nonforest constraints.

For the specialization with every unselected alpha untouched and already
paid, but no other internal alpha/beta relays, there are no actual markers
in the affected selected-source/donor/mixed/cycle subgraph. It follows that
the earlier a<=h mixed-relay theorem also holds when the selected tails
are used internally. Here a can include alphas formed from the other
free ends of the selected paths; the argument does not prescribe which
source becomes joined to which donor.

## Geometric consequence and limits

The reflected family of ZERO_CAPACITY_GAP_BETA_COMPENSATION.md supplies
a real full-domain replacement: two old PP pairs are removed and three
new edges inserted. One removed pair lies inside the selected beta path.
Its chosen original free BP endpoint and the chosen alpha TP endpoint
are newly covered, all other free endpoints survive, and all old PP
vertices remain covered. Thus (1)--(4) apply without suppressing the
beta tail. The physical repair is the previously proved one; the new
result places it in the full-domain sign and payment-transfer framework.

It also has an explicit coherent orientation for every even W>=6,d>=1.
In the raw coordinates of that note put c=2-2d, a=4 and z=5. The chosen
alpha end (z,3) has sign minus and chosen beta end (a,c-2) has sign plus.
The actual edge (a,c-2)--(a,c-1) crosses, so (a,c-1) is minus. Its old
auxiliary partner (z,c-1) is plus. Orient the original two-edge boundary
cycle with (a,c) plus and (z,c) minus. The three inserted edges are then

    (z,3) minus -- (a,c) plus,
    (z,c) minus -- (z,c-1) plus,
    (a,c-1) minus -- (a,c-2) plus.

Every retained auxiliary edge already crosses; all other original cycle
orientations are irrelevant. Thus N is coherent. The interval length d
only changes the zero-BT corridor witness, not these signs. The full-domain
theorem gives alpha_N=0,beta_N=1,mixed_N=8, without a protected beta tail.
For arbitrary replacements coherence still requires its own certificate;
the sign/error and transfer identities apply even when coherence fails.

The original r distinct beta choices and u injective old payments already
give |I|>=u and b>=r, so S_J>=B is implied by the original hypotheses.
The new result is a strictly less restrictive safe-surgery certificate,
not a stronger scalar bound or a proof of enough donors/routes in every
grid. The global outside-overlap correction remains once. General grid
compensation, universal 5/6 improvement and triple equality remain open.

## Partial-payment extension: certified incremental progress

There is a useful stronger formulation that does not assume all unselected
alphas are already paid. Suppose only f original alphas have different
old interval payments, each at a specified surviving TP endpoint. Put
delta_old=k-f. Choose the r source alphas from the unpaid ones, so
0<=r<=min(delta_old,b). Leave every other original free end in F as before.

Put a positive terminal-incident actual marker on EVERY unselected alpha.
For a paid alpha put it at its paid endpoint. For an unpaid alpha choose
either end, calling its marker unbacked. An unbacked marker is a demand
label, not an interval unit and not a donor. There are exactly

    k-r-f=delta_old-r unbacked markers.

All signs, the full-domain incidence identity, global h balance and the
count bounds above remain valid. For each final alpha containing a backed
marker, assign one such marker's old interval. These assignments are
injective by the same endpoint and component argument. For each remaining
alpha, (4) supplies an unbacked actual marker or a negative N edge.
Choose the former when present, otherwise the latter. Different final
components choose different markers or edges. Hence the number delta_N
of final alphas lacking a transported old payment satisfies

    delta_N <= delta_old-r+h.                            (6)

In particular a coherent replacement reduces the certified unpaid count
by at least r even when there are unpaid alphas outside the selected set
and even when surgery passes through them or through old paid paths.
The forest assignment gives delta_N<=delta_old-r+floor(q/2). This
preserves a progress measure rather than a fixed path-owner assignment.

If f_N payments are actually transported, define

    Q_N=|I|-f_N+beta_N, delta_N=alpha_N-f_N.

The exact residual ledger is still S_J-B=Q_N-delta_N. The old payments
are replaced by the new assignment, not retained as additional charges;
unbacked markers never enter |I| or Q_N. This extension does not already
assume the target inequality: k=2,b=1,|I|=f=0,r=1 with one selected
alpha/beta and a second untouched unpaid alpha has an abstract coherent
replacement with delta_N=1 and S_J-B=-1. Thus (6) has a nonvacuous
incremental meaning even when the starting scalar margin is negative.
That abstract signed example is not a grid counterexample. General grid
donor availability and route existence remain to be established.

This partial-payment extension was developed after submitting the
39356-character full-domain review request. It is outside that review
input until separately audited; no acceptance of it is inferred from
the earlier paid-marker review.

The partial-payment checker passes 210,096 complete replacements,
569,712 choices of backed-marker subsets and 781,020 sign controls.
It reconstructs 1,562,040 exact residual ledgers, including 442,916
abstract controls with negative initial margin, and 187,776 coherent
controls with a strict reduction in certified unpaid count. It includes
r=0,1,2 and explicitly keeps unbacked marker indices out of the resource
pool. The record is
`output/partial-payment-full-domain-progress-validation.json`. These
are finite checks for the general injective-witness proof, not a proof
of route existence. No additional Lean formalization of the partial
global allocation is claimed beyond the twelve local endpoint-accounting
statements already described.

## Verification scope

The checker reconstructs signs on the complete original graph, rather
than restoring contracted one-edge tails. It passes 253,924 abstract
complete replacements on at most eight N-covered vertices, both chosen
ends, selected source/donor paths individually through two PP pairs,
paid alpha/beta/mixed relays and cycles through two pairs. There are
342,448 exhaustive abstract sign controls, 81,316 coherent certificates
and 212,528 replacements that change an old auxiliary edge inside a
selected source/donor path. It checks (2) with vertex identities before
taking signs, all component identities, distinct old-unit transport and
negative-edge witnesses, exact inventories and the forest certificate.

Twenty reflected physical controls use W in {6,8,12,20} and
d in {1,2,4,8,16}. They check feasibility, full freezing, unique actual
matching, the selected beta's removed internal edge, PP and endpoint
coverage, the all-BT corridor witness and the full-domain identities.
Physical orientation checks use the base choice, each individual old
cycle flip and the forest certificate; they do not enumerate every
combination of irrelevant independent physical cycle flips. The explicit
all-parameter orientation above supplies the general proof. Aggregate
counts include 253,944 replacements and 342,833 sign controls. These
counts are modeled occurrences, not distinct physical resource units.

The extended standalone Lean source has twelve named audited statements.
The three new full-domain statements prove (3) from the supplied
full-domain sign-occurrence permutation, its alpha marker-or-error
consequence and its coherent marker corollary. All twelve compile in
Lean 4.33.0; the three additions use propext and Quot.sound, with no
sorry, native evaluation or new axioms. Physical incidence construction,
marker-to-terminal transport and the actual injective payment assignment
remain written proofs and graph checks. Execution records are
`output/full-domain-marker-compensation-validation.json` and
`output/full-domain-marker-compensation-lean.json`.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
