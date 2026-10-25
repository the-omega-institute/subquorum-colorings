# A fixed occupation certificate settles every rematching of the mixed-cycle board

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

The preceding [single](FROZEN_SQUARE_SWITCH_AND_INTERVAL_REPAIR.md) and
[interacting](INTERACTING_SQUARE_SWITCHES_AND_SHARED_BETA.md) switches showed
that beta-only payments can be lost even at fixed occupation. We now settle
ALL actual perfect matchings on this fixed selected/endpoint geometry.

**Result.** For the original 28-by-24 board with 49 selected sites T and
308 endpoint sites P, EVERY grid perfect matching of exactly P has complete
ordinary whole-support compensation. Only the five original interval units

    (band,column) = (6,12), (7,10), (9,10), (12,7), (12,16)     (1)

need remain available; all other interval sinks may be reserved. The matching
need not be completely frozen, need not be connected to the original by
square flips, and need not retain any old matching edge. The alpha/beta counts
may change. There is a constructive bound of 18 actual terminal links.
The same full-payment conclusion consequently holds in the full fork model.

The proof uses a physical certificate depending only on T,P, the aligned
bands and original intervals. The underlying full-certificate sufficiency
is the established partial-certificate theorem, specialized to no holes;
it is not a new general matching theorem. The new contribution is the
explicit occupation-only certificate and its universal rematching consequence.
Five units are necessary for this physical ALL-TP cover scheme, even if two
slots per unit are allowed. We do NOT claim that every compensation of every
matching needs five intervals, or that five is the minimum universally
sufficient payment reserve. The numerical 5/6 target remains open.

## 1. Why the certificate is independent of the matching

Fix a finite aligned two-row packet, selected sites T and endpoint sites P,
with T disjoint from P. Take any perfect matching M of P by actual grid edges.
The PP partner of a site is the other point in its fixed band column.
A physical TP is a point of P whose partner is in T; a physical BP is a point
of P whose partner is blank. Both terminal sets depend only on T,P.
The remaining P points have PP partners. The union of actual M edges and PP
edges is a disjoint union of alternating open strands and neutral cycles.
Changing M changes the terminal pairing and whole-owner bodies, but not the
physical terminal sets, horizontal TP--BP incidences, BB--TT interval forest,
standard boundary marks or original available interval identities.

An endpoint-free gap beside a TP gives support to every eligible original
interval in that gap, for the whole owner containing that TP, under EVERY
M. This local support witness does not depend on the rest of that owner.
Physical corridor access is sufficient; arbitrary body support is not needed.

**Certificate hypothesis.** Assign EVERY physical TP injectively into the
disjoint union of physical BP identities and original interval identities.
A BP assignment must be an actual allowed horizontal TP--BP link. An interval
assignment must have such a physical endpoint-free-gap witness. In this
one-slot version, the same original interval is assigned at most once.
All sites, interval identities and witnesses are fixed before choosing M.

## 2. Universal matching-independent sufficiency

**Theorem.** Under the certificate hypothesis, for every actual perfect
matching M of P all its alpha demands have ordinary compensation using
only the certificate's original intervals and the original beta resources
of THAT M. Its least full-payment link count is at most the number of
BP assignments. Complete freezing is unnecessary.

**Proof.** Select all BP-assigned links C. Certificate injection implies
that no physical TP or BP occurs twice; TPs and BPs are disjoint, so these
links form a legal terminal matching for every M. They can join strands
in any order, merge long paths, or close neutral cycles. No assumption of
component independence or beta persistence is used.

After selecting C, a free TP cannot have had a BP assignment: that selected
link would have used it. Every free TP therefore retains its interval
assignment. In particular each final alpha has two free TP ends carrying
original interval witnesses on the constituent original owners. Choose
one such end per final alpha. Different final alphas have different ends,
and the original certificate's targets are injective. Their chosen interval
identities are thus different. Allocate these original units once each.
Free TP ends belonging to final mixed paths may be ignored. Neutral cycles
have no free ends and create no alpha demand.

Let a,b be the original alpha/beta counts for M and aC,bC the counts after C.
Signed endpoint conservation and the cancellation ledger give

    a+bC=b+aC,      bC<=b,
    payment = b-bC+aC = a.                                (2)

The b-bC credits are consumed original beta units, each once; the aC further
credits are the different original intervals just allocated. The established
non-beta-root normal form converts this cancellation/allocation into
owner-disjoint ordinary interval/beta stems, using a subset of C. Its
physical link cost is at most |C|. Therefore all a sources are compensated.
Forks are not required. QED.

This proof handles simultaneous arbitrary rematching. It neither assumes a
finite rematching sequence nor treats two shared beta entrances as two units.
It is stronger than applying the earlier retained-M core to a few edits.

## 3. The explicit 23-TP certificate

The actual fixed occupation has 23 TPs and 27 BPs. Assign the following
18 TPs to different physical BP targets:

| TP | BP target |
| --- | --- |
| (1,3) | (1,4) |
| (1,6) | (1,5) |
| (2,5) | (2,4) |
| (5,4) | (5,3) |
| (5,6) | (5,5) |
| (5,17) | (5,16) |
| (5,19) | (5,18) |
| (6,1) | (6,2) |
| (15,1) | (15,2) |
| (16,13) | (16,14) |
| (18,15) | (18,16) |
| (20,1) | (20,2) |
| (24,2) | (24,3) |
| (24,4) | (24,5) |
| (24,8) | (24,9) |
| (24,11) | (24,10) |
| (24,19) | (24,18) |
| (24,21) | (24,20) |

The five remaining assignments are

| TP | Original unit (band,column) | Physical witness |
| --- | --- | --- |
| (12,14) | (6,12) | endpoint-free corridor through col13 |
| (14,11) | (7,10) | immediate BB column |
| (19,11) | (9,10) | immediate BB column |
| (24,6) | (12,7) | immediate BB column |
| (24,17) | (12,16) | immediate BB column |

Every selected unit is an eligible singleton original interval, is unmarked,
and is different from the others. Every BP target is distinct; the five
interval targets are distinct; every TP appears once. Thus the theorem gives

    V_ord(M,Q)=V_full(M,Q)=a(M),   c_ord(M,Q)<=18             (3)

for every actual perfect matching M of P and every original availability Q
containing (1). The full-model least cost is at most the ordinary least cost,
so is at most 18 too. Exact costs can vary with M and Q; this is a uniform
bound, not an exact-cost formula.

The terminal inventory also gives b(M)-a(M)=(27-23)/2=2 for every M, although
a,b and the mixed count separately change. That invariant does not itself
imply compensation; certificate (1) does.

## 4. Why this all-TP physical certificate needs five distinct units

Use physical endpoint-free-gap access, rather than expanded whole-owner
support that depends on M. Consider five disjoint TP groups:

| Group H | Its physical BP neighbours | Available interval neighborhood N(H) |
| --- | --- | --- |
| {(12,14)} | empty | band6 cols12,15,16 |
| {(14,11)} | empty | band7 cols5..7,9,10,13,15 |
| {(19,11)} | empty | band9 cols8..10,13,14 |
| {(24,2),(24,4),(24,6)} | (24,3),(24,5) | band12 col7 |
| {(24,17),(24,19),(24,21)} | (24,18),(24,20) | band12 cols12..16 |

Each group has exactly one more TP than different possible BP targets.
Any injective assignment covering all its TPs must consequently send at
least one of them to an interval. The five physical interval neighborhoods
are disjoint. Their five required assignments must therefore use five
DIFFERENT original interval units, even if each interval is given two slots.
Our certificate attains this bound with one unit from each neighborhood.
This is a general Hall-deficiency/disjoint-neighborhood argument, not the
claim that a maximum matching search has proved minimality.

The lower bound is specific to physical all-TP covering. A compensation
packing need not cover every TP, can use whole-owner support, and can exploit
its matching-specific beta routes. It can need fewer than five units. The
preceding double-switch example is one such case. No minimal universal
payment-reserve assertion is inferred from this covering lower bound.

## 5. Scope resolved and scope remaining

The original board, every frozen or nonfrozen square-switch sequence, and
any other perfect matching of the same P are now settled together. Searching
for an uncompensated rematching of this fixed occupation with all intervals
available cannot succeed. The preceding restricted-pool entrance obstructions
remain valid: their Q omits some units of (1), so they do not contradict (3).
Beta-only failures remain possible because this certificate uses original
intervals as well as beta resources.

This is not a theorem for arbitrary changes of T/P. Filling one of the
certificate's blank BP partners can change its terminal type; adding an
endpoint in one of its gap corridors can destroy its interval witness.
Neither type of alteration is included without rechecking the certificate.
Other frozen occupations may have an actual physical Hall obstruction, as
in the earlier tip-slot counterexample. Complete compensation there still
requires the more general joint-cut analysis. The universal grid target
and its 5/6 improvement remain open.

## 6. Verification and formal scope

The verifier reads the same permanent physical certificate for every tested
M, reconstructs all strands and owner supports, lifts its 18 links and
interval assignments, and independently compares ordinary/full flows using
ONLY the five specified interval sinks. All 2,745 distinct matching models
pass, including 309 completely frozen and 2,436 feasible nonfrozen controls.
Their alpha counts range from one to five; this is evidence that counts are
not being held artificially fixed. There are 160 independent primitive-pack
comparisons. The exploration includes the base, all 44 one-flip and 952 new
two-flip matchings, plus 1,748 new random-walk matchings. This is not an
exhaustion of all perfect matchings. Sections 1--3 prove the universal result.
The five disjoint lower-bound neighborhoods are reconstructed separately
using full physical gap access, not whole-owner support.

The Lean file checks the concrete matching-independent occupation
certificate, actual terminal inventory, five resources/18 links, and the
five disjoint physical obstruction neighborhoods. It also proves the general
free-tip interval consequence, interval-injection step and exact payment
ledger. Arbitrary M/PP decomposition, cancellation to final alpha paths and
normal-form lifting are written arguments from the established strand
framework; this is not an end-to-end Lean proof of all-rematching flow.
The formal receipt gives the exact audited declarations and machine scope.

All seven local Lean 4.33.0 audits completed with exit zero, using no
sorry/native evaluation and only propext/Quot.sound where needed; the two
general free-tip/injection lemmas are axiom-free. See the
[formal receipt](../output/occupancy-all-rematchings-formal-check.json),
[computational receipt](../output/occupancy-all-rematchings-validation.json)
and [direct Lean source](../formal/SubQuorum/OccupancyCertificate.lean).
