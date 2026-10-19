# Frozen occupied rails: an isolation obstruction with exact nonpositive cost

20 October 2026 Singapore. This note extends the prescribed thick-elbow family
by arbitrarily long occupied adjacent bands. The bands cannot be removed by
any sequence of endpoint promotions: every added endpoint is universally
frozen. Nevertheless each band's exact whole-receiver contribution is
nonpositive. A band aligned inside complete physical column pairs can preserve
positive charge one, so the obstruction is present even for positive receivers.
The old capped-corner donor still pays that unit once.

This refutes extending the stepped one-port isolation rule to all frozen
positive cores. It does not refute the grid inequality. Completeness of the
enlarged component is an explicit hypothesis for the receiver calculation;
it is unnecessary for the freezing proof. Submitted manuscripts are unchanged.

## 1. Prescribed matching and selected supports

Use the relative coordinates of ELBOW_SOURCE_COMPENSATION.md: physical tiles
have even row starts and odd column starts. Let w>=6 and h>=4 be even. Retain
the elbow endpoint set H_0, actual matching M_0 and selected supports S_0
from Sections 1--2 of that note. The elbow's chamber contains
{0,1} x {0,...,w-1}. Its matching and supports alone freeze every H_0
endpoint; that argument does not require component completeness.

Choose finitely many nonempty disjoint intervals

    I_i={a_i,...,a_i+2ell_i-1} subset {0,...,w-1}, ell_i>=2,

with at least one omitted column between consecutive intervals. For each
interval prescribe a rail and its consecutive horizontal matching:

    R_i={(-1,c): c in I_i},
    ((-1,a_i+2j),(-1,a_i+2j+1)), j=0,...,ell_i-1.

Prescribe the two selected caps

    (-2,a_i), (-2,a_i+2ell_i-1).

All named sites belong to the ambient grid. Additional selected sites and
matching edges are permitted subject to feasibility. Write H=H_0 union_i R_i.
For the charge theorem assume H is the complete endpoint component, with the
displayed matching. For freezing and the isolation obstruction, only the
prescribed actual matching and selections are required.

The blank-exterior construction is feasible for all these parameters. Each
cap sees only its own rail endpoint. The two caps on one rail are separated
by at least three columns; caps on different rails are separated by at least
two. No cap is adjacent to an original selected support. Every rail point
sees its distinct underlying chamber endpoint. The old supports keep their
original single occupied neighbor: the exterior side sites (-1,-1),(-1,w)
remain blank. Thus no selected vertex gains an unintended occupied neighbor.

## 2. Two acyclic waves freeze every rail

Let m be the actual matching involution. Every original chamber endpoint
and its mate are frozen. Consequently each chamber endpoint remains occupied
in every feasible simultaneous promotion bundle, including bundles that use
exterior matching edges.

For a rail beginning at a, first freeze (-1,a). Its selected cap (-2,a)
and its retained chamber neighbor (0,a) are distinct. Its mate (-1,a+1)
therefore remains occupied. Inductively freeze

    (-1,a+2), (-1,a+4), ..., (-1,a+2ell-2).

At each step the two retained neighbors are the underlying chamber endpoint
and the left rail neighbor, which is the mate of the preceding frozen point.
Starting at the opposite selected cap gives a reversed wave

    (-1,a+2ell-1), (-1,a+2ell-3), ..., (-1,a+1).

The waves are disjoint and exhaust the rail. They use only prescribed
matching edges, cap selections and already frozen chamber endpoints. They
work for every ell>=2, every number of rails, and arbitrary feasible exterior.
All points of H are therefore universally frozen.

In particular H_0 need not be a complete endpoint component even though its
full frozen certificate survives. In the blank-exterior construction no
nonempty promotion bundle can start. In an arbitrary exterior no bundle can
promote or remove a rail endpoint, since both endpoints of each rail matching
edge are frozen. Hence endpoint promotions cannot isolate H_0 from these
rails. The obstruction affects mixed bundles as well as single promotions.

## 3. Exact whole-receiver charge, with the physical phase retained

Assume now that H is the complete endpoint component. Let rho_H be its
original corrected whole receiver charge, as defined in
COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md. That note's generic ownership
theorem assumes single-terminality. The following local closed-receiver
argument proves the present identity without that ambient assumption.

For a tile Q write t_Q,p_Q for its selected and endpoint counts, and
e_Q=t_Q+p_Q/2-2 for its raw excess. Feasibility implies t_Q<=2. The local
saturated-tile lemma of GRID_ABSORPTION_PROOF.md applies to every feasible
pair: if t_Q=2, then p_Q<=1, and any endpoint there is matched to a deficient
tile. Its corrected charge is zero. A deficient tile's corrected charge
is e_Q+s_Q/2, where s_Q counts its endpoints matched to saturated tiles.

Let U be any finite union of full physical tiles such that every endpoint
in U has its actual mate in U. For each saturated endpoint in U its mate
is in a deficient tile of U. Conversely every deficient endpoint of U
counted by s_Q has its saturated mate in U. The matching therefore gives
a bijection between these two counted sets. The raw excess of a saturated
tile is exactly p_Q/2; thus its omitted raw excess equals the sum of the
deficient corrections in U. Consequently

    sum_(Q in U) rho(Q)=sum_(Q in U) e_Q.

For our geometry the following exhaustive labels show that all endpoints
in the receiver belong to H. Its prescribed matching is closed on H, so
this local lemma applies. It gives

    rho_H=|T intersect V(receiver)|+|H|/2-2|receiver|.

The original elbow receiver tiles lie in row bands starting at 0 or below
the chamber. Their labels are unchanged by the new rails, which lie in the
separate band {-2,-1}. Completeness of H excludes every foreign endpoint
from the old receiver boundary just as in the elbow proof. Thus the old
receiver contributes exactly one.

For rail i let t_i count the selections (-2,c), c in I_i, and put
epsilon_i=1 if a_i is even, otherwise 0. Its rail tiles are disjoint from
the old receiver and from those of every other rail. Indeed all rails lie
in one physical row band, while a blank column between two intervals
prevents their endpoints from sharing a two-column tile.

If a_i is odd, the rail occupies ell_i complete physical column pairs,
so its receiver has ell_i tiles. If a_i is even, its first and last
columns occupy separate end tiles and its interior occupies ell_i-1
full pairs, giving ell_i+1 tiles. The two unprescribed sites in each
partial end tile in this even-start case are blank: its upper outside site is forced blank by the cap;
the lower outside site cannot be P by completeness, and cannot be T since
it sees a rail endpoint and an underlying chamber endpoint. At the extreme
columns -1,w, the original side support instead forces that lower site blank.
There are no other selected sites in these rail tiles beyond the counted
t_i. This is an exhaustive receiver-label argument, not a blank-exterior
assumption.

In the odd-start case each end tile instead has two rail endpoints, its
selected upper cap and one upper blank forced by that cap. No lower outside
site occurs. Since w is even, an odd start plus an even interval length
ends at an even column, at most w-2; it cannot be clipped at w-1. These
parity facts also cover intervals adjacent to either chamber boundary.

Adjacent top selections would each see their own endpoint and each other,
so are infeasible. Pairing the 2ell_i top sites in consecutive pairs gives
t_i<=ell_i. Each rail contributes exactly

    lambda_i=t_i+ell_i-2(ell_i+epsilon_i)
            =t_i-ell_i-2epsilon_i <= -2epsilon_i.       (1)

Writing L=sum_i(ell_i-t_i)>=0 and E=sum_i epsilon_i gives the exact theorem

    rho_H=1-L-2E <= 1.                                (2)

Thus rho_H>0 precisely when E=0 and every t_i=ell_i, in which case
rho_H=1. A single even-start rail instead forces rho_H<=-1. These counts
include each physical tile once and retain the actual matching correction.
No phase gain or separate copy of the rail's negative charge is added.

Both bounds are sharp at every length: for ell>=2 select the two caps and
the top sites with offsets 2,4,...,2ell-4. This has ell selections and
is independent. An odd-start rail costs zero; an even-start rail costs -2.
Taking w=2ell+2, a=1 gives positive frozen extensions at every length.

## 4. Owned compensation and an exact non-reuse formula

The capped corner of the original elbow, Q={2,3} x {1,2}, still has the
same four-endpoint north run, short tip and selected support. Its two near
corners are not P because H is complete and the rails lie above the chamber.
The capped-corner deficit lemma therefore gives no endpoints in Q and
d_Q=2-|T intersect Q|>=1. The unique-owner lemma applies to the entire
enlarged endpoint component; two different components cannot claim Q.

Consider a terminal configuration whose components consist of s such
complete rail-extended elbows in their positive root phase and arbitrary
other components of nonpositive whole charge. Let Z be minus the sum of
the other charges, so Z>=0. Choose one owned tile Q_i per elbow, including
those whose charge is nonpositive. These tiles are distinct. The exact ledger is

    Delta=mn/2-|T|-|M|
         =sum_(unchosen no-P Q) d_Q
           +sum_i(d_(Q_i)-1)+sum_i L_i+2sum_i E_i+Z >=0.       (3)

Each term has a single owner. In particular an even-start rail's two-unit
loss is already included in rho_H; it cannot also be allocated as a separate
donor while rho_H is kept unchanged. Choosing donors only for the positive
components yields the equivalent weaker sufficient estimate. Formula (3)
also gives equality exactly when every displayed nonnegative term vanishes.
With no additional components its terms are integers; for arbitrary other
components their original nonpositive charge is retained in Z.

This proves coefficient one on the stated enlarged receiver class, removing
the |M|/6 loss of the general 5/6 estimate there. It does not supply a cover
of arbitrary positive components or a universal receiver ceiling. An initial
configuration may be normalized into this class only when the normalization
preserves these prescribed complete frozen components and the remainder
has the required final charge condition.

## 5. A concrete positive obstruction and verification scope

Take w=6,h=4,a=1,ell=2. The added matching edges are
(-1,1)--(-1,2) and (-1,3)--(-1,4); the added caps are (-2,1),(-2,4).
The full component has 22 endpoints and 11 matching edges, is universally
frozen, and has charge one. Add the permissible corner selection (2,2)
to make its old owned donor have deficit exactly one. This is an explicit
positive component containing the prescribed elbow as a proper connected
frozen subset. Neither singles nor mixed bundles can extract that elbow.
It refutes the proposed general extraction rule, not inequality (3).

The checker recomputes feasibility, actual endpoint components, all retained
freezing witnesses, the ordered two rail waves, physical receiver labels,
charges, exact donor and ledger terms. It exhausts top selection words at
small lengths and tests all eight tile-preserving directions and separated
mixed-phase component packs. A complete oriented-bundle check is performed
on the concrete 11-edge example. These are controls for the preceding
all-parameter proof, not substitutes for it.

The new Lean module checks the abstract anchored freezing induction, rail
charge identity and bound, positive-charge rigidity, and the conditional
aggregate ledger with its equality case. Its coordinate adapter, physical
receiver classification, donor ownership and whole-grid application remain
written. Execution receipts and independent-review status are recorded
separately. The first independent assessment returned REVISE for a missing
local ledger justification and end-tile wording; both are addressed in
Section 3. The same-conversation repair assessment completed ACCEPT for
the written mathematics under these stated hypotheses.

Executed controls pass for 464 independent top-selection words, 36 larger
parameter cases through rail length 128, four multi-rail cases through eight
rails, 320 symmetry images and three mixed-component packs. Twelve extra
fixtures have a nonterminal exterior matching edge and verify the local
closed-receiver formula directly without a terminal ambient pair. The concrete
11-edge example passes all 177147 oriented choices; only the empty choice
is feasible. The physical receipt is output/frozen-rail-elbow-controls.json.

Sequential local Lean 4.33.0 completed 141 scoped declarations without
warnings at 2026-10-19T16:17:53.873893+00:00, including the four additions.
Peak child RSS was about 1.05 GB; the real lean/lake executable-basename
count was zero before execution. The receipt is
output/frozen-rail-elbow-formal-check.json. No admitted or compiler-reduction
axioms occur. The task-owned reproducible formal cache was removed after
confirming no actual lean/lake executable remained.

A full written-proof audit with the complete elbow and ownership dependencies
completed REVISE as task cebf5747-94ef-4a06-b9ad-0bdb6ed16a26, conversation
conv_d2e686fef1f9355a, observed gpt_6/pro. The exact response is archived in
output/frozen-rail-elbow-review-response.json. It confirms the freezing,
charge formula and non-reuse ledger; the generic terminal-ownership citation
is now replaced by the explicit local closed-receiver argument above.
The parity wording is clarified without adopting the review's impossible
odd-start endpoint at w-1. Repair task 5ba5f6de-e82e-44fc-99f1-0f6ca39f4887
completed ACCEPT at 2026-10-19T16:24:20.229+00:00, observed gpt_6/pro. Its
exact answer matches both the original follow-up stream and terminal server
response, archived in output/frozen-rail-elbow-repair-review-response.json.
It confirms the parity correction and the local saturated/deficient bijection
without requiring ambient terminality. Metadata and independent scope
are in output/frozen-rail-elbow-review.json. Older phase-review quota rejections
are different requests and are not restarted or counted as this assessment.

    python3 develop/check_frozen_rail_elbows.py --output output/frozen-rail-elbow-controls.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
