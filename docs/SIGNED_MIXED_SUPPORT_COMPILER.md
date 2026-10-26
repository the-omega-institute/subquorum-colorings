# Three-snapshot support compilation for mixed target directions

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We give an exact signed Boolean description of whole-owner interval support
for **arbitrary mixed-target aligned P-free direction changes**, with local
capacities zero, one and two. It requires at most three physical snapshots:
the initial state, all variable tiles H, and all variable tiles V. For each
common original resource there are at most four corridor terms, two in each
possible phase. A term specifies actual gates that must have changed and gates
that must not have changed. The compiler works even when old support is lost.

The signed description gives a polynomial test for all-subset support
monotonicity, with explicit adjacent physical states witnessing rejection.
On accepted inputs all negative literals can be dropped, yielding an exact
positive-prerequisite description. This extends the **recognition and support
compilation** part of [uniform handoffs](POSITIVE_CAPACITY_HANDOFFS.md).
It does not extend that class's matching-based joint fee optimizer.

We also give an all-length feasible bent-owner family that is accepted but
acquires genuinely new support while a positive tile is still in its initial
phase. Its access formula is x_q OR AND_(i<q) x_i. Thus simply keeping old
support and adding final-direction corridor accesses is incorrect for mixed
targets, even under all-subset monotonicity. The obstruction concerns a
compiler rule, not the numerical grid bound or the general matching theorem.

## 1. Physical setting and resource identity

Fix a feasible pair (T,M) on an even-by-even rectangle. Let P be the actual
matching endpoints, and assign H/V directions to aligned 2x2 tiles. Use
canonical maximal same-direction bands, complete restored M/PP owners, actual
terminal links, and whole-owner support of original positive BB/TT forests.
Choose any distinct P-free tiles g_0,...,g_(m-1). Each gate is optional: x_i=0
keeps its initial direction b_i, and x_i=1 changes to the opposite direction.
There is no uniformity requirement on b_i or the target directions.

All owners, terminal/source types, actual links and private beta units remain
fixed: the auxiliary mate of every P vertex is unchanged. Feasibility and
freezing depend only on T,M and are also unchanged. This established P-free
invariance allows the full mixed/beta network to be retained in every state.

Refine the canonical bands into their aligned tiles. Every positive coarse
forest has a unique positive fine child and these children biject to coarse
resources. For children outside variable tiles use the fixed physical child
cell set as ID. A variable tile g_i has

    kappa_i = 2 - |T intersect g_i| in {0,1,2}

positive children in either direction. Pair the sorted H and V children to
IDs (gate,i,k), 0<=k<kappa_i. Each tile lies in one no-P gap in its phase;
all its children therefore have identical supporting-owner sets in that
phase. Any fixed local pairing works. These are transported **original unit
identities**, not a union of independent H and V resources. The raw pool Q,
owner types and ledger S=L+beta-alpha are fixed in all states.

## 2. Two potential snapshots and the signed corridor theorem

For axis D in {H,V}, set **every variable tile** to D while keeping every
other tile fixed. This is a legitimate physical state: its changed-gate set
is F_D={i:b_i differs from D}. These potential states need not be the empty
or full changed set. Together with the initial state they are at most three
snapshots, with duplicates cached.

In the D potential state, take each maximal no-P gap of a D band. Its two
boundaries, when present and open, specify global owners L,R. Fixed opposite
tiles and P columns are genuine boundaries; no proposed corridor crosses
them. For each fine anchor j of direction D in the gap, form a corridor
to each of these boundaries. Let C be the set of variable tiles between j
and that boundary. Include j's own tile when j is local to a variable tile.
The corridor term is

    AND_{i in C} [x_i = (b_i differs from D)].             (1)

Thus each gate on the route must actually have direction D. If its initial
direction already equals D, the term contains the negative literal NOT x_i;
otherwise it contains the positive literal x_i. An empty corridor term is
true. Absent boundaries and closed-cycle boundaries contribute no owner term.
When L=R keep their two alternative terms for that **one** owner.

**Theorem 1 (exact signed support).** In every changed-gate state F, owner o
supports original unit j if and only if at least one of its compiled corridor
terms (1) is true. A fixed unit has at most two terms in total; a local unit
has at most four, two for each phase. Terms for different owners still refer
to the same unit j. Local capacity-two twins have the same support function.

**Proof.** Fix the actual direction D of j's tile in state F. Any actual D
band containing j is a sub-band of the D potential band: the potential state
sets every variable tile to D, and the nonvariable tiles are identical.
Within that potential band the nearest P column on each side is fixed,
because no variable tile contains P. There is no alternative P column that
can become a nearer owner by changing gates. An actual boundary owner can
therefore support j from that side exactly when none of the intervening
variable tiles cuts the corridor. This is precisely (1). If a cut occurs,
the actual gap ends at a band boundary before reaching that P column and
there is no P-free intermediate owner that could replace it.

Whole-owner support includes every positive forest in this actual gap. Its
positive fine anchor j remains in that gap, even if balanced forest pieces
merge or split; the positive-child bijection identifies the actual coarse
resource. Conversely any supporting owner is at one of these two actual
gap boundaries, so comes from a compiled term. For a variable local unit,
each term includes its own direction literal, so the wrong phase contributes
no support. Fixed units have one phase; local units have two, with two sides
per phase. All local children have identical gap/boundary behavior, proving
the twin assertion. QED.

The compiler builds all terms, including destructive accesses. It does not
need support monotonicity and does not solve a flow problem. The number of
terms is at most 4|Q|, each with at most m gate literals. Ordinary geometric
snapshot construction and explicit term storage are polynomial in the input.

## 3. Polynomial all-subset monotonicity test with physical witnesses

For an incidence (j,o), write its signed DNF as f(F). We want

    F subset F'  implies  f(F) <= f(F')                  (2)

for every incidence, not just initially present ones. It suffices to test
adjacent changes F -> F union {g}, g not in F, since any inclusion is a
sequence of such edges. Enumerating those edges is unnecessary.

**Theorem 2 (recognition).** The following test is exact and polynomial.

1. For each old term T containing NOT x_g, fix its other literals true.
   When comparing after the switch, fix x_g=1.
2. Discard every candidate new term already false under these forced values.
   If any new term is already wholly true, T cannot witness a loss.
3. Otherwise choose one currently unforced literal of each remaining new
   term to make false. Test the resulting choices for consistency.
4. A consistent choice gives a loss witness. Complete unspecified gates
   with zero, then use its states x_g=0 and x_g=1 as the adjacent witness.
   Reject if any incidence/gate has such a witness; otherwise accept.

At most **two** new terms remain undecided in step 3. If g is the local
tile of j, the new phase has only two sides. If g is different from j's local
tile, the old term fixes that tile's phase, eliminating its other phase;
the remaining phase again has two sides. Fixed units have only two terms
to begin with. Thus at most m^2 pairs of falsifying literals are tested per
old-term/gate choice, with polynomial checking and output size. A single
failed corridor term alone is not a loss: the opposite side may still
support the same global owner, including unconditionally.

**Proof.** A term true before a 0-to-1 change can cease to be true only if
it contains the negative literal of that gate. Hence every actual loss has
an old true term considered in step 1. Every new term must be false after
the switch. A term not already forced false has an unforced literal made
false by the actual losing assignment, unless it is forced true, which would
contradict loss. Choosing these actual falsifiers is a consistent branch
of step 3. Conversely any consistent branch makes the old term true before
the switch and every term false afterwards. Its compiled witness therefore
is an actual geometric support loss by Theorem 1. This proves necessity,
sufficiency and physical validity, with the stated two-term bound. QED.

Compilation uses at most three physical snapshots. Recognition itself uses
only the terms and performs no further snapshot or optimizer calls. Rebuilding
the reported witness states is an independent check, not a required search
over all states. The old uniform V->H recognizer and this test agree on their
common inputs.

## 4. Exact positive retraction on passing mixed inputs

**Theorem 3.** If the input passes Theorem 2, delete all negative literals
from every corridor term. The resulting positive DNF equals the complete
actual support relation at every state.

**Proof.** Any true original term has all its positive gates present, so it
satisfies its shortened term. Conversely, if F contains all positives of
some term T, let F0 consist of exactly these positive gates. Corridor terms
are consistent, so every negative gate of T is absent from F0. The original
term is true at F0. Since F0 subset F and support is monotone, its incidence
is also true at F. QED.

This is a positive-prerequisite support compiler for mixed targets, including
old-phase accesses. It does not make all alternative terms simultaneously
available without paying their prerequisites. In a rejected signed input,
dropping negatives is unsound. Even on an accepted input, the earlier
uniform-direction fee optimizer needs its original extreme-retraction and
sharing hypotheses; Theorem 3 alone does not supply them.

## 5. All-length obstruction to using only final-direction corridors

For n>=2 take an 8 by (2n+4) board. Let

    T = {(5,1)}
        union {(4,2i),(5,2i+1): 1<=i<n}
        union {(4,2n+2),(5,2n+3)}.

For the capacity-one version also add (4,2n). The actual matching is

    ((4,1),(3,1)), ((3,0),(2,0)), ((2,1),(2,2));
    ((2,c),(2,c+1)) for c=3,5,...,2n-1;
    ((2,2n+1),(3,2n+1));
    ((3,c),(3,c-1)) for c=4,6,...,2n.

Initially all tiles are H except (2,2i), 0<=i<=n, and (4,2i), 1<=i<n,
which are V. The variable gates are g_i=(4,2i), 1<=i<=n. Gates i<n
change V->H and have capacity zero; q=g_n starts H and changes H->V,
with capacity two or one. The final tail tile (4,2n+2) is fixed H with
capacity zero. Write x_q for the last gate's change variable.

**Proposition 4.** These boards are feasible, have one bent mixed owner a
and no alpha or beta owners, and pass all-subset support monotonicity.
Each local original resource j of q has exactly the support formula

    [a supports j] = x_q OR (x_1 AND ... AND x_(n-1)).     (3)

Every other support incidence is constant. In particular the state with
all earlier gates changed and q unchanged has new support absent initially,
even though q is still in its initial direction.

**Proof.** Matching edges are disjoint. The added selections in row 4 are
at even columns, each adjacent to at most one occupied endpoint; selected
sites in row 5 are at odd columns and have no additional occupied neighbour.
The selection (5,1) sees only (4,1). The optional selection (4,2n) sees only
(3,2n). Thus every selected vertex has at most one occupied neighbour.

Following the actual matching and auxiliary PP pairs gives one open body,
with endpoints (3,3) of type BP and (4,1) of type TP. Its interior zigzags
through rows 2 and 3 to column 2n+1. All variable tiles are P-free, so this
body and its mixed type do not change. The full tile resource inventory is
|T|=2n+1+epsilon, |M|=2n+2, L=4n+13-epsilon, where epsilon is zero or one.
No freezing assertion is made.

When q is V, its vertical gap is bounded immediately above by the PP column
in row 3 at columns 2n,2n+1, belonging to a. There is no other variable tile
between it and a. Every local unit therefore supports a unconditionally in
this phase. When q is H, its only possible owner boundary is the P column
at column 1 in the row-4 band. It reaches that column exactly when every
earlier variable tile is H. The fixed zero-capacity tail has no owner on
the right. This proves the signed formula

    (NOT x_q AND AND_(i<n) x_i) OR x_q,

equivalent to (3). Earlier variable tiles and the tail have no local positive
units. There are no positive fine anchors in the PP tiles of row 2; other
fixed bands cannot be changed by these gates. The one resource left of
column 1 has its constant owner boundary. All remaining incidences are
constant. Equation (3) is increasing, proving full monotonicity for every n.
QED.

A compiler that keeps only initial support plus accesses in q's final V
gap would require x_q for j and miss the second alternative in (3). The
failure also affects activation costs: for nonnegative gate fees the exact
minimum fee to establish this incidence is

    min(w_q, sum_(i<n) w_i),                             (4)

whereas that final-phase-only rule gives w_q. Taking earlier fees one and
w_q=n+1 gives the strict discrepancy n-1 versus n+1. This is a physical
support/access-fee obstruction. Since the family has no alpha sources and
is not claimed fully frozen, it is not a payment or extremal-grid counterexample.

## 6. Compensation use and verification

For any actual state F, evaluate the signed terms and pass that single
support model to [exact old-link batch repair](OLD_LINK_BATCH_REPAIR.md).
Its p+g-t formula and mandatory-root condition then use the correct whole
original resources. This avoids a full geometric recompilation for each
candidate state, but choosing the best F remains a separate problem.

Never union all potentially available signed offers as if they belonged
to one state. Requirements x_i and NOT x_i cannot be simultaneously met.
Every route pack must share one consistent global gate assignment; resource
IDs remain capacity one across all phases and all access alternatives.

The standalone implementation and independent audit are in
[check_signed_mixed_support.py](../develop/check_signed_mixed_support.py).
It checks 1,509 physical support states, 4,213 Boolean-lattice edges and
208 rebuilt physical loss witnesses. Ninety-four complete small state
families verify recognition iff all actual edges preserve support; 52 cases
agree with the prior uniform recognizer. There are 95 models, 35 with mixed
targets; 945 independent routing optima, 1,509 old-pack repair evaluations,
and 817 accepted-state checks of positive retraction. Capacity-zero/one/two
and coincident-owner alternative terms are covered. Seven logic controls
include two simultaneous falsifiers and contradictory falsifier choices.

A fully frozen 16x102 control has 35 actual mixed-target gates and 140 frozen
endpoints. The three-snapshot compiler describes its 2^35=34,359,738,368 states
symbolically; 12 selected states and all 38 returned rejection witnesses are
rebuilt, not an enumeration of that state space. Across frozen controls
280 strict freezing events are independently replayed. Six old-phase-birth
controls cover n=2,4,8 and both positive capacities. Their all-n justification
is Proposition 4, not the finite audits.

Run:

```sh
python3 develop/check_signed_mixed_support.py \
  --output output/signed-mixed-support-validation.json
python3 develop/check_signed_mixed_support_formal.py \
  --lean /Users/lexa/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean \
  --output output/signed-mixed-support-formal-validation.json
```

Two general logical kernels in `SignedMixedSupport.lean` are axiom-free:
monotone consistent signed DNFs equal their positive retractions, and any
term lost on a single increasing gate change contains that gate's negative
literal. The physical compiler, four-term geometry, falsifier-search
completeness and all-length board proof are written proofs with executable
checks, not end-to-end Lean formalizations. Local Lean runs use memory and
comm-basename process preflights before each executable invocation.

The submitted 11 October manuscript, public main, PR3, shared CI and C4
correspondence remain separate. This research note makes no universal 5/6
improvement claim and performs no mail operations.
