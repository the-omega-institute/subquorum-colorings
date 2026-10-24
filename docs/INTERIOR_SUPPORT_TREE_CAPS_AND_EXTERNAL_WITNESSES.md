# Interior frozen support trees and a two-external-witness bound

25 October 2026. Research branch; Haobo Ma and Wenlin Zhang.

There are two results. First, the earlier frozen two-owner deficient support
tree can be sealed by an explicit PP cap at any odd column: its interval-only
defect now survives arbitrary blank right padding. Second, for **original**
alpha strands of a completely frozen configuration, every deficient
whole-support tree has at least two external terminal witnesses. Counting
these with their original identities bounds the defect after direct
whole-beta compensation. Neither result proves a beta Hall failure or an
improvement of the universal 5/6 bound.

The first result removes the boundary-release limitation of
[the preceding example](FROZEN_SUPPORT_TREE_AND_FORCED_REROOT.md). The second
combines the proved [missing-tip injection](FROZEN_MISSING_PORT_BP_TERMINAL_INJECTION.md)
with the [joint tree--beta theorem](JOINT_TREE_BETA_COMPENSATION.md).

Subsequent result: [safe beta closing](BETA_CLOSING_AND_SHARP_MIXED_DEFECT.md)
adds one selection, preserving every original interval and alpha support,
but turning the sole beta into mixed. The resulting physical family attains
the bound below with arbitrary positive direct-beta Hall defect, yet admits
full mixed repair. Thus universal direct-beta saturation under the stated
feasibility/freezing hypotheses is now refuted, not an open lemma to prove.
This note's original physical controls and their zero defect remain unchanged.

## 1. An all-length interior cap

Start with exactly the 12-by-18 configuration, selections T, actual matching M,
and strict freezing certificate of the preceding example. Its permanent source
is `develop/fixtures/frozen_support_tree_reroot.json`. Write

    A = ((5,8),(8,8)), B = ((5,10),(8,14)),
    beta = ((3,12),(5,11)).

For any integer d>=1 put c=17+2d, and use a 12-by-(c+3) board. Retain every
old selection and every old matching edge. Add the tail selections

    (r,j) if j is odd; (r+1,j) if j is even,
    for r in {6,8} and j=17,...,c-1.

Add the four anchors

    (5,c), (6,c+1), (8,c+1), (10,c),

and the two actual matching edges

    (6,c)--(7,c), (8,c)--(9,c).                 (1)

All coordinates are zero based. The two new within-band PP edges coincide
with (1); retain their multiplicity in the PP multigraph. They form two pure
two-edge cycles, **not** two new beta resources.

**Proposition 1.** For every d>=1 this configuration is feasible and completely
frozen. Its original whole-support interval graph consists of the two alpha
owners A,B joined by the sole incident available interval J, at band2/column9.
The deficiency is t=1. The unique direct alpha--beta link remains
B:(5,10)->(5,11); hence mu=1. This support defect remains t=1 after adding
any even number 2r>=0 of blank columns to the right.

**Proof of feasibility and freezing.** Each new matching endpoint is distinct
and outside the old occupied support. Consecutive tail selections lie in
opposite rows; selections in the two tail bands are also never adjacent.
They avoid all old P endpoints. The first new tail selections at column17
are diagonal to the old selections at rows7,9/column16. Thus they give no
old selection a new occupied neighbor. A tail selection has no occupied
neighbor except at the last column c-1, where (7,c-1),(9,c-1) each sees its
single new P endpoint. Each anchor sees precisely its intended new endpoint.
This checks every new selection and preserves every old feasibility condition.

Every old freezing witness remains valid: old T and old actual mates are
unchanged. Freeze the new endpoints in two ranks. First freeze (6,c), using
the selected neighbors (5,c),(6,c+1), and (9,c), using (9,c-1),(10,c).
Then freeze (7,c), using selected (7,c-1) and retained (8,c), whose actual
mate (9,c) just froze. Freeze (8,c), using selected (8,c+1) and retained
(7,c), whose mate (6,c) just froze. These are distinct nonmate witnesses.
There is no cycle in their dependencies. This proves freezing for arbitrary
length, with no enumeration or matching-uniqueness assumption.

**Proof of access and padding stability.** The original PP paths and their
tips are unchanged. The new P columns belong only to the two cycles. The
complete original A/B P-column supports are therefore still

    A: (2,8),(3,8),(4,8);
    B: (2,10),(3,10),(3,11),(3,12),(3,13),(3,14),(4,14).

Their complete list of nonempty adjacent endpoint-free gaps is now

| Owners | Band | Gap | Types | Available units |
|---|---:|---|---|---:|
| A | 2 | columns5--7 | BT only | 0 |
| A,B | 2 | column9 | BB | 1, J |
| B | 3 | columns15--c-1 | BT only | 0 |
| B | 4 | columns15--c-1 | BT only | 0 |

The latter two gaps terminate at the new PP column c. All remaining neighboring
columns of the displayed supports are P columns. Consequently J is the only
incident interval, using the full supports rather than only tips. Every listed
gap is now bounded internally by P columns. Empty columns beyond c+2 cannot
enlarge any of them. Hence right padding cannot release any A/B resource.
The direct terminal geometry of A,B and the sole beta is unchanged. QED.

“Interior” here asserts internal bounds on all source-adjacent gaps and this
specific right-padding stability. It is not an assertion about arbitrary
changes in the rest of the grid.

## 2. Exact inventory and both compensation interfaces

The exact inventory is

    |T|=33+4d, |M|=25, |P|=50,
    alpha=2, beta=1, mixed=8, pure PP cycles=5.

For completeness, count BB--TT interval components band by band. The one
original TT merger in band1 is retained. No new TT column is introduced.

| Band | BB sites | TT sites | Interval components |
|---:|---:|---:|---:|
| 0 | 19+2d | 0 | 19+2d |
| 1 | 11+2d | 1 | 10+2d |
| 2 | 9+2d | 0 | 9+2d |
| 3 | 3 | 0 | 3 |
| 4 | 3 | 0 | 3 |
| 5 | 19+2d | 0 | 19+2d |

Each band has two distinct boundary interval marks. Thus raw intervals are
63+8d, marks12, and available original intervals I=51+8d. One is paid,
so U=50+8d. The exact ledger is

    U+beta-t = 50+8d
      = 12(20+2d)/2 -(33+4d)-25-12.             (2)

Fix the maximum interval baseline B->J with A unpaid. Since only B reaches
the sole beta, full direct compensation is forced to assign A->J and B->beta.
Maximum payment is2, minimum direct beta links1, and minimum number of changed
old assignments1. The previously paid B stays paid; the old used interval set
remains exactly {J}. Starting instead with A->J gives zero old changes.

The wider mixed interface retains the old alternative (8,8)->(8,9). Its new
A has TP endpoints (5,8),(8,10) and can use the original unit K at band4/column11,
while B keeps J and beta remains unused. It uses one link, adds K to the used
interval set, and changes zero old assignments. The two ledgers are respectively

    direct: U=(50+8d), beta=0, t=0;
    mixed:  U=(49+8d), beta=1, t=0.

Both equal (2). Neither spends J, K or beta twice. Zero links cannot pay both
alphas because their complete original supports see only J; either one-link
construction pays both. Thus the full terminal model has exact minimum link
count1, independently of an optimization run.

Adding 2r blank right columns adds 2r singleton intervals in each of six bands
and preserves two marks per band. Therefore

    I=51+8d+12r, U=50+8d+12r, t=1, mu=1,
    margin=50+8d+12r.                           (3)

This is the opposite behavior to the preceding uncapped example, whose defect
vanished under the same padding operation. For arbitrary q>=1, translate q
copies of the capped board by (12i,0). The occupied bottom row10 of a copy and
first occupied row13 of the next copy are separated, no feasibility or freezing
witness changes, and resources lie in distinct bands. Hence

    alpha=2q, beta=q, t=mu=q, I=(51+8d)q,
    U=margin=(50+8d)q.

The specified B_i->J_i baselines require q distinct beta links and q old changes
in the direct interface. The q mixed alternatives use distinct links and K_i,
keep all old assignments and consume no beta. This realizes arbitrarily many
simultaneous two-owner trees, not one tree with arbitrarily many owners.

## 3. Two external witnesses per original-alpha deficient tree

We now give a general statement, not restricted to the above construction.

**Hypotheses.** Use a finite feasible, completely frozen actual matching and a
matching-closed aligned packet satisfying the boundary hypotheses of the
missing-tip injection theorem. Original TP columns are internal; the boundary
marks are precisely original interval components touching a band endpoint.
Take **C0 empty**. Let alpha owners be the original TP--TP strands, and build
the complete whole-support incidence graph on available original intervals,
as in the joint tree--beta theorem. A deficient component is a tree with no
private interval, having n alpha owners and n-1 shared original interval units.
Keep distinct original beta, mixed and marked-interval identities throughout.

Construct two tokens for every original alpha, one at each of its two TP tips:

1. If the tip has an immediate BB neighbor in its band, choose one such neighbor
   and its original interval identity. Prefer an unmarked choice if one exists;
   the theorem allows any choice.
2. Otherwise apply the simultaneous missing-tip injection f to that tip and
   use the original strand containing the adjacent BP tip f(v). It is a beta
   or mixed strand; retain the actual direct link v->f(v).

The token is an endpoint witness, not an allocated payment. The construction
is defined for every tip by the existing injection theorem.

**Fiber capacities.** An unmarked interval gets at most2 tokens; a marked
interval gets at most1; a whole beta gets at most2; a whole mixed strand gets
at most1. These bounds hold across all alpha owners, not just within a tree.

To see the interval bound, an original BB--TT interval is a single row-band
chain. A TP tip with an immediate BB port can approach this chain only at one
of its two physical ends: internal BB sites are flanked by TT columns in the
chain. At each end there is one neighboring column and at most one TP tip in
that column, since the TP column contains a selection in its other row. Thus
each end supplies at most one token. A marked chain touches a packet boundary,
so only its inward end can supply a tip. If it touches both boundaries it has
no such end. The beta and mixed bounds follow from injectivity of f and the
fact that an original beta has two BP tips and an original mixed has one.
In particular two beta tokens still name **one** payment resource.

**Lemma 2 (two external witnesses).** Every deficient whole-support tree has
at least two tokens with destinations outside its unmarked interval resources.
Choose and retain any two such tokens for each tree. The chosen tokens can
only name beta strands, mixed strands or marked intervals, with global fiber
capacities2,1,1 respectively.

**Proof.** A chosen unmarked tip-interval destination is eligible for its
alpha's whole support. It therefore belongs to the same incidence component.
For a deficient tree on n owners all these internal destinations lie among
its n-1 units. Their capacity is at most2(n-1). The owners have exactly2n
tokens, so at least2 are external. The previously proved global fiber
capacities persist after selecting two per tree. QED.

The scope restriction to original alphas matters. A virtual alpha after
arbitrary cancellation may end at a tip originally belonging to a mixed
strand, to which the original-alpha missing-tip theorem does not apply.
This note makes no such extension.

## 4. A global beta Hall-defect inequality without repeated credit

Let D be the set of t deficient trees. Let G be the bipartite graph from D
to **whole original beta strands**, putting an edge whenever any alpha owner
in the tree has an actual direct TP--BP link to that beta. Let mu be its
maximum matching size. In Lemma2 retain two external tokens per tree, and
write q(X),h(X) for the numbers of distinct mixed and marked identities named
by chosen tokens of a subset X of trees. These destinations have capacity1,
so they are distinct across those trees. N_beta(X) denotes the neighbor set
in the full graph G, including direct links not selected by the token rule.

**Theorem 3.** For every X subset D,

    2|X| <= 2|N_beta(X)| + q(X)+h(X).            (4)

Consequently the exact joint interval/direct-beta defect delta=t-mu satisfies

    delta <= floor((q(D)+h(D))/2).               (5)

In particular q(D)+h(D)<=1 forces full joint compensation. If none of the
source-adjacent gaps sees any marked interval, h(D)=0, and a beta Hall failure
requires at least two distinct selected external mixed strands.

**Proof.** The trees in X have exactly2|X| selected tokens. Each beta token
gives an actual direct link, so its whole strand belongs to N_beta(X).
The global beta fiber capacity is2; mixed and marked fiber capacities are1.
Counting the tokens gives (4), with no assumption that a beta tip is itself
a credit. By the finite bipartite matching deficiency identity,

    t-mu = max_{X subset D} (|X|-|N_beta(X)|).

For every X, (4) gives twice this expression at most q(X)+h(X), which is at
most q(D)+h(D). Taking the maximum and integrality proves (5). Equivalently
one may use the alternating-reachable Hall witness of a maximum matching;
no enumeration of subsets is needed to construct that witness. The preceding
joint compensation theorem turns its distinct matched betas into distinct
tree-root payments, using each old interval once and preserving the baseline's
used interval set. QED.

**Reserve corollary.** Let b be the total number of original betas and U the
number of original intervals unused by a maximum interval baseline. The joint
repair uses mu distinct betas and preserves that used interval set. Its signed
boundary ledger is therefore exactly

    margin = U+(b-mu)-(t-mu)
           >= U+(b-mu)-floor((q(D)+h(D))/2).     (6)

In particular U+(b-mu)>=floor((q(D)+h(D))/2) suffices for a nonnegative ledger.
Here U names only unused original intervals and b-mu names only unconsumed
whole beta strands. They are disjoint from each other and from all paid
resources; neither may be credited separately to several trees. This is a
conditional sufficient test for the existing boundary target. No geometric
estimate proving its hypothesis for every grid, or new universal5/6 constant,
has been obtained.

This is a bound on residual defect, not a license to pay half a unit from a
mixed strand. In the abstract capacity model, one tree with two distinct mixed
tokens and no beta has delta=1 and attains (5). This is **not** asserted to be
a geometric counterexample. Conversely, our capped physical tree has two
selected mixed tokens (at tips (8,8),(8,14)), h=0, yet delta=0 because B has
the unselected direct beta edge. Thus the token upper bound can be strict;
the full direct-beta graph must be retained. Distinctness of BP terminals
alone never permits claiming two resources from one beta.

## 5. Evidence, proof status and the remaining question

The all-d cap feasibility/freezing, complete gap list, inventory formulas,
all-q stacking and padding arguments above are written general proofs.
Lemma2 and Theorem3 use the previously proved geometric injection, elementary
fiber counting and the standard matching deficiency identity. Enumeration is
only a regression check and does not replace any of these arguments.

Solver-free `develop/check_interior_support_tree_caps.py` checks d=1..16,
64 padded boards,16 carried isometries and36 stacks, actual links, preservation
of original interval witnesses, and independent flat allocation optimization.
`develop/check_tree_external_witness_bound.py` checks the original-alpha token
construction on59 physical models, including161 nonsingleton deficient trees,
and1,847 abstract two-token models, with24,619 subset inequalities. It keeps
the original identities of every strand and marked interval. The abstract
controls include sharp positive deficiencies; the physical examples do not
claim a new beta Hall failure.

`formal/SubQuorum/InteriorSupportTreeCaps.lean` proves cap freezing for every
positive column c with actual nonmate witnesses, mate closure, arbitrary-column
tail alternation/nonadjacency, the parametric numeric ledger, and the scalar
two-witness/Hall-defect implications. These are eight scoped declarations.
The full-board geometric adapter, interval inventory, missing-tip injection,
fiber counts and general matching specialization are written proofs with
computational regression checks; they are **not** claimed fully formalized.
The local driver records the executable, memory/process preflight and axiom
audits. No new external review is claimed.

The subsequent safe-beta-closing result realizes the two-mixed-end Hall-deficient
structure and tracks its accessible original interval reserves. The remaining
geometric task is a general continuation mechanism beyond this realized family.
Any continuation through mixed strands must retain gate capacity and original
interval identity; the earlier shared-gate obstruction rules out replacing
this with an unrestricted source-to-resource projection. Universal direct-beta
saturation is false under these hypotheses; general mixed compensation and a
new numerical 5/6 improvement remain open. The submitted manuscript is unchanged.
