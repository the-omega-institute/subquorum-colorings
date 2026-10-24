# Two-slot terminal certificates: sufficient, sharp, and not necessary

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

The proposed endpoint assignment has a valid general implication: assigning
every original TP terminal either to an adjacent BP terminal or to one of two
slots of an eligible original interval suffices for complete whole-support
ordinary compensation. Two slots are the largest universally sound uniform
allowance. However, complete freezing does **not** imply the existence of such
an assignment, even after restricting attention to owners reachable from an
original alpha. An explicit fully frozen `10 x 16` board has terminal Hall
defect one but complete compensation one, at minimum link cost one.

The obstruction is internal: a frozen PP column seals the implicated gap.
It persists under arbitrary blank right extension and has Hall defect exactly
q in q vertically separated copies, whereas compensation remains complete.
The failing test demands witnesses for a neutral mixed owner's TP terminal
as well as for an alpha end. That extra endpoint demand is not a second alpha
payment. This rules out using the test as a necessary consequence of freezing;
it does not refute the target grid inequality or improve the universal 5/6 bound.

## 1. Precise certificate and its general sufficient condition

Fix any finite original strand system from
[the whole-support normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md). Each owner
has two disjoint terminals and is alpha (TP,TP), beta (BP,BP), or mixed
(TP,BP). Owners have disjoint terminal sets. Let L be the set of declared
physical TP--BP links, and I the set of distinct available original interval
identities. For each owner x fix its support set W(x) subset I. A final
component's eligible intervals are the union of the supports of its owners.
Supports are counting witnesses; no free-tip physical route is inferred.
Any immutable earlier cancellations must first be contracted, with supports
and available resources fixed for that contracted system.

A **two-slot certificate** is an injective assignment from ALL current TP
terminals to the disjoint target set

    {original BP terminals} disjoint-union (I x {0,1}).       (1)

A terminal v can use BP w only if (v,w) belongs to L. It can use (j,k) only
if j belongs to W(owner(v)). Each BP identity is used at most once, and each
original interval therefore receives at most two assigned TP terminals.
BP targets and interval targets are different types, even if represented by
the same integer in some implementation.

Equivalently, the finite Hall criterion is

    |H| <= |N_BP(H)| + 2 |union_(v in H) W(owner(v))|         (2)

for every subset H of TP terminals. All unions are over ORIGINAL resource
identities. Two witnesses for the same interval contribute two slots in total,
never four; two BP tips of one beta remain two terminal identities, not two
whole-beta payment units.

**Theorem 1 (sufficiency).** A two-slot certificate gives a legal cancellation
and allocation with compensation equal to the entire original alpha count.
Moreover, an ordinary stem packing suffices, without beta-body forks. Its
link count is at most the number of BP assignments in the certificate.

**Proof.** Select exactly those links whose TP terminal is assigned a BP
target. Each TP has one assigned target and all BP assignments are different,
so these links form a terminal matching C. The original strand edges together
with C form alternating paths and cycles. Every free TP terminal is assigned
an interval slot, because a BP-assigned TP is incident to its selected link.

Each final alpha path has exactly two free TP terminals. Retain their two
assigned interval identities, including multiplicities within that path.
For any collection K of final alpha paths there are exactly 2|K| such
terminal assignments. They reach intervals in a union J(K), each of which
has at most two assigned terminals in the entire system. Thus

    2|K| <= 2|J(K)|, hence |K| <= |J(K)|.

Hall's theorem allocates distinct intervals to ALL final alpha paths using
only those retained incidences. Each chosen interval has a witness in an
original owner containing one of that path's free TP ends, so it is a valid
whole-support payment. No paid path uses a beta-body-only witness.

Write a,b for the original alpha and beta counts and a_C,b_C for the final
counts. Every component satisfies the signed endpoint identity, giving
a_C-b_C=a-b. Since all a_C final alpha paths are paid, compensation is

    b-b_C+a_C = a.                                        (3)

This counts each consumed whole beta once regardless of how many of its BP
tips were used. It counts each allocated interval once by the second Hall
matching. Mixed paths and cycles create no extra payment. Finally apply the
subset normalization of the linked normal-form note: each paid component's
chosen witness is on a TP owner, hence alpha or mixed, so only ordinary stems
are needed. Normalization selects a subset of C and preserves compensation.
This proves the claimed link bound. QED.

This is a general finite proof; the controls below merely check implementations.
Condition (2) is a uniform cross-component sufficient inequality, but freezing
does not prove it. It must not be substituted for a proved geometric bound.

**Sharpness of two slots.** With three slots, take three alphas A0,A1,A2,
no betas or mixed owners, no links, and two resources j0,j1, with

    W(A0)={j0}, W(A1)={j0,j1}, W(A2)={j1}.

Send both tips of A0 to j0, both tips of A2 to j1, and one tip of A1 to each.
This uses three slots per resource and covers all six TP terminals. Yet only
two of the three alphas can be paid. Each resource has only two owner users,
so even that physical-adapter incidence restriction does not repair the rule.
The same assignment works with any allowance at least three. This is an
abstract strand-system control, with no frozen-grid realization asserted.

## 2. Explicit completely frozen physical obstruction

Use rows 0,...,9 and columns 0,...,15, paired vertically as (0,1), (2,3),
(4,5), (6,7), (8,9). T denotes a selected point, P a matching endpoint,
and a dot a blank point:

```text
................
....T...........
...TP.T.T.......
....PPPPPT......
..TPPPPP........
...T..PP....T...
..T..TPPPT.TP...
.TPPT.T.T.T.PT..
...T......T.T...
................
```

The matching is

```text
(2,4)--(3,4)    (3,5)--(4,5)    (3,6)--(4,6)
(3,7)--(3,8)    (4,3)--(4,4)    (4,7)--(5,7)
(5,6)--(6,6)    (6,7)--(6,8)    (7,2)--(7,3)
(6,12)--(7,12)
```

These ten edges have 20 different endpoints, disjoint from the 21 selected
points. All edges are adjacent. Each selected point has at most one occupied
neighbour, which is the required partial-coloring feasibility condition.
Direct coordinate checks and the Lean kernel verify all of these assertions.

The following strict-rank layers certify complete freezing:

```text
0: (2,4) (3,8) (4,3) (6,6) (6,8) (6,12) (7,2) (7,3) (7,12)
1: (3,6) (5,7)
2: (4,5) (4,6) (4,7)
3: (3,4) (3,5) (3,7) (5,6)
4: (4,4) (6,7)
```

For each endpoint v, at least two distinct grid neighbours are either selected
or are endpoints w whose matching mates have strictly lower rank than v.
Induction on rank gives the actual inductive freezing process. The validation
JSON lists the two witnesses for every endpoint; the verifier checks them
independently of the repository's peeling routine. The Lean module derives
freezing from the existing general rank theorem.

## 3. Strands, exact Hall shortfall, and available compensation

The relevant original endpoint strands, alternating matching edges and the
vertical PP pairing, are

```text
A: (3,6)--(4,6)--(5,6)--(6,6)       TP--TP, alpha
D: (6,7)--(6,8)                     BP--TP, mixed
B: (3,5)--(4,5)                     BP--BP, beta
R: (3,7)--(3,8)                     BP--TP, mixed
```

The other mixed strands have terminal pairs ((4,3),(4,4)) and
((7,2),(7,3)). The remaining PP components are cycles. Thus the full inventory
is a=1, b=1, m=4, and there are six TP terminals.

Let H={(6,6),(6,8)}. Its first point belongs to A; its second belongs to D.
Both have precisely one horizontally adjacent BP terminal, namely (6,7).
Neither A nor D has any whole-support original BB interval witness, EVEN
before deleting the marked boundary units. Hence

    |H|=2, |N_BP(H)|=1, |union W(owner(H))|=0.             (4)

The exact local Hall shortfall is one. Increasing the number of interval
slots cannot help (4), since there is no eligible interval at all.

This is not an irrelevant isolated mixed component: the actual link
(6,6)->(6,7) goes from A into D. Thus both obstructing TP owners are reachable
from original alpha A in the actual directed owner graph. Restricting the
all-TP test to alpha-reachable owners still leaves the failed subset H.

Conversely, the actual link (3,6)->(3,5) joins A to B and consumes ONE whole
beta, paying the only alpha demand with one link. The remaining D can be
left untouched. There is no zero-link payment because W(A) is empty, and
payment cannot exceed the one original alpha. Therefore

    full ordinary payment=1, minimum links=1, deficit=0.    (5)

One can alternatively enter R and use one of its available intervals, also
with one link. This is a second way to pay the SAME alpha, not a second
simultaneous payment. The verifier exhausts all 60 legal terminal matchings
of the full base system and checks the same optimum independently.

The two-slot test's global matching value is exactly five of six. For example,
assign A's upper TP (3,6) to beta BP (3,5), D's TP (6,8) to D's BP (6,7),
R's TP (3,8) to R's BP (3,7), and the other two mixed TP terminals to their
own BP neighbours. The only unmatched tip is (6,6). Formula (4) proves that
no matching can cover all six. Mixed self-links are allowed in this *test*;
they are removable zero-credit cycles in the compensation normalization.
Omitting them from the test also leaves the counterexample valid.

The original ledger has balance49, surplus_twice98, boundary budget10 and
39 available original interval units. Its boundary-adjusted margin is
98-2*10=78. Neither the ledger nor the full compensation has a deficit.

## 4. Why padding and arbitrarily many copies do not repair the test

For A, the occupied columns next to all its body columns already block access
to a BB unit. For D, the endpoint-free gaps in band (6,7) are columns4,5 and
9,10,11. Every one of these columns is BT. Column12 is PP, with endpoints
(6,12),(7,12), and seals the gap to the right. Consequently there is no BB
unit in either gap, and no later BB unit is accessible through that PP seal.
The same argument holds after adding any number of blank columns to the right.
The sealing matching edge freezes at rank zero from its four selected anchors;
it is not an assumed occupied boundary.

For any positive integer q, translate this entire board by (10i,0) for
i=0,...,q-1 and take their union in a 10q by (16+2e) grid, e>=0. The first
and last row of each base board are blank; occupied sets of different copies
have no adjacent points. The vertical pairing, matching strands, strict ranks,
TP--BP links and all relevant endpoint-free gaps remain separate by copy.
Thus feasibility and complete freezing follow from the base certificate.

The union H_q of the q displayed two-tip subsets has size2q, exactly q BP
targets and no interval slots. Its Hall defect is q. The five-tip matching
above in each copy gives a full-system terminal matching of size5q out of6q,
so q is also the EXACT maximum Hall defect, not just a lower bound. Paying
A_i by B_i in each copy gives compensation q with q distinct links and q
distinct whole betas. No alpha has a zero-link interval payment, so q links
are necessary. Hence, for all q>=1 and e>=0,

    terminal Hall defect=q;
    full ordinary compensation=q, deficit=0, minimum links=q.     (6)

This is an all-parameter construction and proof. The finite copy/padding
checks below serve as implementation controls, not as its justification.

## 5. Correct next proof obligation

Counting all TP terminals overcounts the actual source demand: a mixed owner
has one TP and one BP and contributes zero signed charge. For an entire owner
set U with counts a_U,b_U,m_U, the terminal imbalance is

    TP(U)-BP(U)=2(a_U-b_U).                                (7)

But the failing subset H is not an entire owner set: it contains only one
end of A and the TP end of D, excluding D's BP target. Its extra demand is
an artefact of requiring a simultaneous assignment for both ends. A route
certificate can pay A from its other end and discard the unused D branch.

Theorem1 remains useful as a sufficient certificate for a chosen reduced
system. What is ruled out is the unconditional geometric assertion that
freezing, or alpha reachability, ensures it. A reduction deleting neutral
branches before applying (2) requires its own proof that all alpha payments
and shared capacities survive. Merely naming a branch neutral does not
establish that deletion rule in a larger network.

The next general target remains the actual capacitated source cut from
[the exact fork-flow theorem](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md):
its demands are unpaid alphas, its BP/mixed gates retain their true capacities,
and each whole beta and original interval is counted once. After any paid
bypass is fixed, use the simultaneous reserve criteria from
[the residual cost note](RESIDUAL_EXCHANGE_AND_EXACT_RESERVE_COST.md), rather
than assuming that alternative exits remain independently available.

## 6. Reproduction and exact validation scope

```sh
python3 develop/check_frozen_tip_slot_obstruction.py \
  --output output/frozen-tip-slot-obstruction-validation.json
```

The verifier requires Python only, with no Z3. It reconstructs the actual
endpoint multigraph independently of the existing band-strand adapter,
crosschecks terminal pairs, verifies strict ranks, compares all64 TP subsets
and all60 legal cancellation matchings on the base board, and checks48
copy/padding instances (q=1,...,16 and added widths0,2,10) and8 isometries
with the original bands carried along. It also checks1080 deterministic
abstract systems:516 actual two-slot lifts succeed,227 ordinarily complete
systems lack a full tip certificate, and the three-slot unsound control passes.
Rotating the points and then choosing NEW horizontal bands would change the
problem; that is not what the symmetry checks assert.

Local Lean4.33.0 verifies physical feasibility, all20 endpoints frozen,
the three critical strands and terminal types, both empty support sets
(even including boundary units), the forced shared BP target, impossibility
of an injective tip assignment, the alpha-to-mixed and alpha-to-beta links,
and the right PP separator for arbitrary later columns. It reuses the
already-proved general strict-rank criterion. Ordinary `decide` is used;
no `sorry`, custom axioms or `native_decide` occur. The general Hall lifting
proof, arbitrary-copy geometry and flow optimality are written proofs plus
independent controls; they are not claimed as fully formalized in Lean.

No submitted manuscript was changed. The11 October version is preserved.
This result has not received an independent Oracle review in this round.
