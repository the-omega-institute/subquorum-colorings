# Colored row-owner deficiency and exact one-step resource cuts

25 October 2026. Authors: Haobo Ma and Wenlin Zhang.

We refine the exact row surplus into an exact owner deficit. Besides mixed
tips and surplus row paths, the formula needs beta owners with only ONE tip
in the chosen neighborhood. That term prevents double counting a beta's two
physical tips. Splitting by checkerboard color also gives the exact optimum
of every monochromatic beta allocation. A uniform frozen construction shows
arbitrarily unbalanced mixed counts between the two colors. Standard matching
then gives a necessary and sufficient, witnessed cross-component allocation
criterion including distinct original interval resources. We also prove that
original mixed relays preserve TP checkerboard phase and rewrite the exact
full-route cut using two phase blockers and one shared resource set.

This is a structural application of ordinary bipartite matching, not a new
Hall theorem. The criterion describes one-step beta/interval payments. It is
not necessary for the larger mixed-relay network, nor proved automatic under
freezing. The universal frozen-grid inequality and 5/6 improvement remain open.

## 1. Original owners, row components and colors

Use the hypotheses of [frozen fork exclusion](FROZEN_FORK_EXCLUSION_AND_ROW_SURPLUS.md).
Fix a set U of original alpha owners with both tips missing. Other original
alphas may be present; they are not paid or used as resources here. Every
original beta is initially available, with one unit per whole original strand.
Every permitted interval access has its established original unmarked interval
identity, as in the [normal form](COMPENSATION_FLOW_NORMAL_FORM.md); marked
boundary intervals are excluded. No mixed relay is included in this section's
payment options.

For Y subset U, let X(Y) be its 2|Y| TP tips, D(Y) all horizontally adjacent
BP tips, and H_Y the physical row adjacency graph. The preceding fork theorem
says H_Y consists of isolated TP--BP edges and BP-ended paths. Write:

- c_gamma(Y): number of BP-ended components whose BP tips have checkerboard
  color gamma, for gamma=0,1;
- q_gamma(Y): number of mixed BP tips of color gamma in D(Y);
- b_1,gamma(Y): number of original beta owners with exactly ONE tip in D(Y),
  that tip having color gamma;
- b_2(Y): number of original beta owners with both tips in D(Y);
- i(Y): number of distinct permitted original interval resources accessible
  from the original TP tips of owners in Y, using the declared direct/cap
  access relation.

Put c=c_0+c_1, q=q_0+q_1, b_1=b_1,0+b_1,1. All these refer to the ACTUAL
neighborhood of Y, not a preselected terminal injection. Each original alpha
has one TP tip of each checkerboard color. Every original beta has one BP tip
of each color. The two tips of any original open strand have opposite colors.
BP tips inside a row component all have the same color and different owners.
A beta may appear in two components, one of each BP color; it remains one unit.

## 2. Exact colored owner ledger

**Theorem 1.** Let B(Y) be the distinct neighboring beta owners. Then

    2(|Y|-|B(Y)|) = q(Y)-c(Y)-b_1(Y),                        (1)

and, for EITHER gamma,

    |Y|-|B(Y)| = q_gamma(Y)-c_gamma(Y)-b_1,1-gamma(Y).        (2)

Thus the right side of (1) is even. Negative scores are permitted.

**Proof.** All |Y| alpha tips of color 1-gamma occur in row components whose
BP tips have color gamma. An isolated component has equal part sizes; each
BP-ended component has one extra BP. Therefore

    |D_gamma(Y)|=|Y|+c_gamma(Y).

On the other hand, count BP tips by their ORIGINAL owners:

    |D_gamma(Y)|=b_2(Y)+b_1,gamma(Y)+q_gamma(Y).

Subtract |B(Y)|=b_2+b_1,0+b_1,1 to obtain (2). Sum over gamma to get (1). ∎

The earlier weighted inequality omitted b_1. Equation (1) identifies the
exact correction. A beta appearing once in the terminal neighborhood is
still an entire available unit. This is not extra credit: the formula counts
that owner once and its observed terminal once. Betas seen twice contribute
one owner and one tip of EACH color, not two units.

## 3. Exact unrestricted beta and one-step interval compensation

Allow each a in U either one horizontal link to a neighboring original beta,
or one declared access to an original interval. Let nu_beta be the maximum
number of sources paid using betas only, and nu_simple the maximum number
using these beta/interval options. Define delta_beta=|U|-nu_beta and
delta_simple=|U|-nu_simple.

**Theorem 2 (exact resource-cut criterion).**

    delta_beta = max_(Y subset U) [q(Y)-c(Y)-b_1(Y)]/2,
    delta_simple = max_(Y subset U) [q(Y)-c(Y)-b_1(Y)-2i(Y)]/2. (3)

Equivalently, for EITHER fixed color gamma,

    delta_simple = max_Y [q_gamma-c_gamma-b_1,1-gamma-i](Y).  (4)

The empty subset gives score zero. In particular, EVERY source in U has a
simultaneous one-step payment iff, for every Y subset U,

    q(Y) <= c(Y)+b_1(Y)+2i(Y).                               (5)

**Proof.** Form the ordinary bipartite graph with U on the left and the
DISTINCT original beta owners and interval units on the right. Keep a
geometric link or access witness for every incidence. A matching gives
simultaneous payments. For every Y, at least |Y|-|B(Y)|-i(Y) sources remain
unmatched. Conversely choose a maximum matching, start alternating searches
at all unmatched sources and let Y be all reachable sources. No reachable
resource is unmatched, since that would be an augmenting path. Every neighbor
of Y is reachable: an unmatched incidence is a forward search edge, and a
matched source's matched resource was already used to reach that source.
The matching bijects these resources with the reached matched sources.
Thus |Y|-|B(Y)|-i(Y) equals the total number of unmatched sources. This proves
the exact defect formula. Substitute (1) or (2). Removing intervals gives
the first formula of (3). ∎

**Witnessed lifting and nonreuse.** For each matched alpha--beta incidence
choose its original horizontal link. Distinct alpha and beta owners make
these links disjoint at their actual terminals and owner supports. Each
cancels one alpha and one beta. An alpha assigned an interval has no selected
link and remains an original alpha; its chosen original access pays it.
Different assignments use different interval identities. Beta and interval
targets are typed separately. This realizes nu_simple payments and leaves
|U|-nu_simple of these original demands unpaid. Every other alpha, unused
beta and unused interval retains its identity. No assumption of disjoint
physical tile footprints is used or needed beyond the established access
model.

When U contains ALL original alphas and delta_simple=0, these payments give
beta+I>=alpha and hence S=L+beta-alpha>=B in the packet ledger, with I=L-B
unmarked original interval units. With additional original alphas outside U,
Theorem 2 pays U only. It does not settle those remaining demands.

Formula (5) is an exact geometric rewriting of resource Hall, not a proof
that freezing forces all its inequalities. It excludes mixed relays. The
previous arbitrary-depth frozen relay family has delta_simple=1 but full
route deficit zero. Failure of (5) therefore need not refute full compensation
or the global grid target. Total resource supply alone is not a replacement
for the all-subset condition.

## 4. Exact monochromatic optimum and a larger complete class

For the FULL H_U, let c_m,gamma count BP-ended components of BP color gamma
that contain at least one mixed BP tip. Set

    e_gamma=q_gamma(U)-c_m,gamma.                            (6)

Restrict beta payments to links whose BP endpoint has color gamma.

**Theorem 3.** Their exact maximum cardinality is

    nu_beta,gamma=|U|-e_gamma.

Consequently

    delta_beta <= min(e_0,e_1).                              (7)

In particular e_0=0 OR e_1=0 suffices for full beta-only compensation of U.
This allows arbitrarily many mixed tips in the other color.

**Proof.** Each original alpha has exactly one TP tip opposite to gamma,
so appears exactly once among the selected row components. Each beta has
only one BP tip of color gamma. Hence different BP tips in this color,
including tips in DIFFERENT row components, are different beta owners.
There is no further resource identification between these components.

An isolated edge loses one payment iff its BP is mixed. In a BP-ended row
path with a alpha tips and q mixed BP targets, there are a+1-q beta targets.
If q=0, match all a sources. If q>0, no beta matching can pay more than
a+1-q of them. Omit a mixed BP target and use the preceding arbitrary-root
path injection; exactly q-1 of its used targets are mixed, leaving exactly
a-(q-1) beta payments. This attains the bound. Summing the component deficits
gives q_gamma-c_m,gamma=e_gamma. These physical matchings lift to different
whole beta owners by their monochromatic uniqueness. Maximizing over either
color proves (7). ∎

The preceding mixed-target bound was floor((e_0+e_1)/2); (7) can be arbitrarily
stronger. It is still only an upper bound on the UNRESTRICTED beta deficit:
combining both colors can do better than either monochromatic allocation.
The exact unrestricted answer remains (3).

## 5. A uniform frozen asymmetric construction

For even W>=6, H>=4, use direct_family(W,H) of
[terminal cancellation](TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md), with
R=W+4. Its matching is unchanged, and its selections are

    {(4,3),(4,5),(4,7),(5,2),(5,8),(6,6),(7,5),(R,2),(R,H+4)}
    union {(R+1,c): c=3,5,...,H+3}
    union {(R-2,c): c=6,8,...,H+2}.

DELETE just the selection (R+1,5). This produces a feasible fully frozen
configuration with the same unique actual endpoint matching. It has exactly
one original alpha, one beta and H mixed strands. Both alpha tips are missing.
Their row components are isolated edges, with respectively a mixed BP of
color1 and a beta BP of color0. Thus e_0=0,e_1=1, and the single link

    (R,3)--(R,4)

pays the alpha using the beta strand (R,4)--(R,5).

**General proof of freezing.** Deleting a selected vertex preserves feasibility.
Use the original all-parameter serial certificate, changing only the event
for endpoint (R,5). In the original descending sweep of odd row-R endpoints,
skip (R,5); all endpoints (R,c) for c>=7 still freeze as before. The following
sweep of even endpoints (R-1,c), c>=6, is unaffected: each uses a guard and
(R,c), whose mate (R,c+1) has already frozen. Now freeze (R,5) using
(R-1,5) and (R,6). Their actual mates are respectively (R-1,6), just frozen,
and (R,7), already frozen. Continue the entire original schedule unchanged.
No earlier event needs (R,5), and the removed selection had no other occupied
neighbor. This covers EVERY endpoint for all W,H, including H=4 where (R,7)
was an initial seed. Uniqueness of actual matching is unchanged because the
endpoint graph is unchanged. No finite enumeration establishes this proof.

Only the former mixed strand (R,4)--(R,5) changes type: its TP at (R,5)
becomes BP. Thus beta increases from0 to1, mixed decreases fromH+1 toH,
and the sole alpha (5,3)--...--(R,3) keeps both missing tips. Its upper BP
neighbor (5,4) is mixed; its lower BP neighbor (R,4) is the new beta. This
proves all the claimed row counts and the explicit payment.

The old receiver-closed cropped packet is unchanged. Removing one T raises
its margin by1, giving S-B=WH/2+W-H-4>=10. This is a payment construction, not
a counterexample to the target inequality.

**Unbounded color imbalance and a sharp limit.** Stack p unchanged copies
of the W=6,H=4 construction and q copies shifted one column. Separate them
by the original18-row board height, so their selected/endpoints and freezing
certificates do not interact. Translation by one column swaps checkerboard
colors and preserves band alignment. For p+q>0 the union is fully frozen,
has k=p+q original alphas, and

    e_0=q, e_1=p,              delta_beta=0.

Each alpha uses its own distinct beta through the displayed local link.
With q=0 and arbitrary p, the two-color total mixed-use bound can leave
floor(p/2) demands uncertified, whereas color0 pays all p. With p=q=r,
either monochromatic optimum leaves r unmatched, but using both colors
pays all2r. Thus (7) need not be exact for unrestricted allocations, even
in real fully frozen configurations. This does not contradict the earlier
exact chosen-injection component formula: that formula can already recognize
the full allocation; the new result refines the coarser global mixed count.

## 6. Mixed relays preserve phase; the full cut shares only actual resources

The color distinction also applies to the FULL original-terminal route
network, including all justified original interval accesses. Define a route's
phase sigma to be the checkerboard color of its TP terminals.

**Theorem 4 (phase invariant and exact full-route cut).** Every route has a
single phase. Every original mixed gate belongs to just one phase, that of
its unique TP tip. Opposite-phase route packings have no mixed-gate conflict;
to combine them they must still use different original alpha sources and
different whole beta/interval resources.

For each sigma let G_sigma be any subset of mixed gates of that phase, and
let R be a subset of DISTINCT original resource units (beta owners or unmarked
interval identities). Let F_sigma(G_sigma,R) be the sources in U with no
phase-sigma route to any resource outside R after deleting G_sigma. Then the
unpaid count in the full route network is EXACTLY

    delta_full = max_(G_0,G_1,R)
      ( |F_0(G_0,R) intersect F_1(G_1,R)| - |G_0|-|G_1|-|R| ). (8)

The empty choice is included. The SAME R is used in both phases and charged
ONCE. Neither beta tips nor the two possible interval access colors create
separate resource units.

**Proof.** A horizontal TP--BP link flips checkerboard color. Traversing the
original mixed BP--TP strand flips it again, since that strand has odd
physical length. Thus the next TP has the same color as the preceding TP.
Induct along the route; a direct interval access simply uses its original
TP color. An original mixed owner has only one TP tip, so cannot occur in
both phases. If opposite-phase routes have distinct source and sink owners,
their original mixed supports, alpha supports, beta supports and interval
identities are all distinct. The original normal-form lifting therefore
combines them without a repeated terminal or resource.

For (8), delete Z=G_0 union G_1 union R in the capacity-one normal form.
A source is blocked exactly when BOTH its possible phases are blocked, hence
its blocked set is F_0 intersect F_1. A packing can pay at most |Z| of these
blocked sources, since each such route must use a distinct deleted unit.
This gives the displayed lower bound on unpaid sources for every Z.

Conversely take an integral maximum flow and its residual minimum cut.
Original link/access arcs have capacity |U|+1, so none can cross this cut,
whose capacity is at most |U|. If Y is the source owners on its reachable
side and Z the unit mixed/resource arcs crossing it, the cut capacity is
|U|-|Y|+|Z|. Thus the unpaid count is |Y|-|Z|. Deleting Z blocks every source
in Y; the preceding lower bound prevents its score from exceeding the actual
unpaid count. Therefore this Z attains equality. Partition its mixed gates
by their unique phases to obtain (8). This is the existing normal-form
max-flow cut theorem with a physical phase decomposition, not a new general
flow theorem. ∎

The restriction to missing alphas was needed for Sections 2--4, but the phase
invariant and (8) also hold for an arbitrary set of original alpha sources,
ported or not. They use only original-strand parity, horizontal links, and
the established original access/resource model. Exchange gates created by
reversing old alpha--beta payments are not original mixed gates: their full
port sets can couple the two phases. Such a phase change represents splitting
and reassigning original source payments; the lifted original routes still
preserve their respective phases. The phase-disjoint conclusion must NOT
be extended to those artificial exchange gates.

Subsequent [full-gap obstruction](BOUNDARY_SEALED_GAP_OBSTRUCTION.md) shows
that complete freezing does NOT force the score in (8) to be zero, even
with full endpoint-free-gap access on the entire board. Both gate sets and
the shared resource set can be empty while the blocked-source intersection
has arbitrarily large size. Formula (8) remains exact; automatic geometric
completeness of that terminal-access interface is the implication that fails.

Two small original-terminal controls show why R must be charged once.
Give every terminal j color j mod2. For two alphas (0,1),(2,3) and one beta
(4,5), allow links (0,5) of phase0 and (3,4) of phase1. The sources differ
and there is no mixed gate, but only ONE beta unit. The full deficit is1;
charging that beta separately in both phases makes the cut formula falsely
return0. Likewise two alphas with accesses 0->J and 3->J have two phase
routes but one interval J, again deficit1. These are abstract colored
terminal controls, not claimed fully frozen grids. They refute the doubled
resource-cut rule, not the grid target.

## 7. Verification and scope

`develop/check_colored_row_owner_deficiency.py` reconstructs actual strand
owners, checks complete freezing and exact subset ledgers, compares (3) with
an independent augmenting-path matching, and reconstructs actual terminal
links and original interval payments. It checks monochromatic optima
separately. The asymmetric family has an explicit all-parameter serial
certificate, also replayed on finite controls. Random colored row profiles
stress resource identification; they are NOT claimed realizable frozen grids.
The arbitrary-depth relay controls distinguish a one-step cut from a full
route obstruction. Results are in the accompanying output JSON.

The deterministic run passes624 frozen geometry controls, including480
carried controls,117 asymmetric parameter pairs,24 assemblies and3 original
relay controls. The serial asymmetric certificates contain7020 checked
events. Across these and800 abstract colored row profiles it checks18208
owner-subset identities and2848 exact monochromatic optima. Full-route
checks cover522 networks/790 phase-preserving routes, including160 abstract
seeded networks and two shared-resource controls. All12127 enumerated cuts
of those162 abstract networks agree with the exact phase formula. These
bounded controls corroborate the general proofs above.

The companion Lean source checks monochromatic owner nonreuse from opposite
tip colors, two flips and arbitrary finite relay-chain phase preservation,
and the exact signed count conversions. Six theorems pass local Lean4.33.0
with no warning/sorry/native evaluation. The two owner-nonreuse theorems use
no axioms, the phase lemmas use propext, and the signed arithmetic uses
propext/Classical.choice/Quot.sound. Execution and formal scope are recorded
in `output/colored-row-owner-deficiency-lean-validation.json`. Grid geometry, the row
matching constructions, Hall's augmenting proof, uniform freezing and the
full lifting argument remain the written proofs above. This note has not
yet received independent external review.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
