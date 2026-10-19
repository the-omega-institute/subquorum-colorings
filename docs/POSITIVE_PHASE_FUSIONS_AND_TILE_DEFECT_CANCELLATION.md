# Positive-phase fusions: automatic protection and tile-defect cancellation

20 October 2026. The previous two-guard theorem was conditional on the final
marked-side and intratile-event counts. Here we prove that its finer budget
is automatic for fusions consisting entirely of positive-phase two-leg
modules. We allow arbitrary contacts and final occupied degree four.
No decomposition of arbitrary grid configurations is asserted.

## 1. Hypotheses and conclusion

Use the supported-module physical fusion hypotheses of
DEGREE_THREE_FUSION_AND_PROTECTED_DONORS.md. There are N original modules,
each an affine copy of two_leg_case(w,a,b), with even w>=6 and even a,b>=4.
Require every original module to have corrected charge +1 in the chosen
physical tile alignment. Original endpoint sets are disjoint. Retain the
union matching and every original support not consumed by foreign endpoints;
require final selected feasibility. Optional additional selections have no
endpoint neighbor and lie outside the original receiver union. No contact
port, once-use, contact graph or freezing assumption is imposed.

Let J count new mixed full PHYSICAL TILE squares and K count original
degree-three endpoints whose unique new occupied neighbor is intratile.
Let G count affected canonical left/right protector sides, as in the
two-guard note. Let D be actual endpoint-free tile deficit, and
sigma=mn/2-|T|-|M|.

**Theorem.** Under these hypotheses,

    G=0,       D>=2N,       0<=K<=2J,
    rho_final=N-2J+K,
    sigma>=N+2J-K>=N.                              (1)

Thus the coefficient-one half-area bound holds automatically in this class,
with guaranteed slack at least one per original module. In particular the
previous finer sufficient condition K+L<=S+2J holds, with S=L=0. Neither
the theorem nor its proof says that degree-four contacts actually occur in
every subclass, or that this strictly enlarges previously covered examples.
Finding an actual all-positive degree-four fusion is a separate question.

## 2. Three tile profiles and two boundary properties

Every receiver tile of one positive-phase module has one of these profiles:

* one endpoint, its two adjacent corners selected, opposite corner blank;
* two adjacent endpoints, with one selected and one blank remaining corner;
* four endpoints, with no selection.

There are thirteen oriented profiles: four singleton profiles, eight
two-endpoint profiles and one full profile. Two further properties retain
the geometry that the profile list alone does not express:

**Exterior support.** Every original endpoint has an original ENDPOINT
neighbor outside its own physical tile.

**Blank-corner continuation.** If an endpoint p has an originally blank
neighbor v INSIDE its tile, its other intratile neighbor u is an original
endpoint, and the continuation 2p-u, outside the tile, is an original endpoint.

These statements have a direct all-parameter proof. In reference coordinates,
the bar interior tiles have four endpoints. The two bar end tiles and paired
stem rows (2s,2s+1), with 1<=s<height/2, have two endpoints and one exterior
selection on the even row. Each leg has one final tip tile with a single
even-row endpoint and two adjacent selections. These tiles are exhaustive.

For exterior support, bar-interior corners have the horizontal bar neighbor
outside their tile. At a bar end, the row-zero corner has its horizontal
bar neighbor, and the row-one corner has the row-two leg endpoint. On a
paired stem tile the upper endpoint has the preceding leg endpoint and the
lower endpoint has the following leg endpoint, outside the tile. The final
tip has its preceding leg endpoint. These witnesses exist at height four.

An intratile blank can neighbor an endpoint only in a two-endpoint tile.
It neighbors the odd-row endpoint; the other intratile neighbor is the
preceding even-row endpoint, and the following even-row leg endpoint is the
required continuation. This includes row one at each bar end. Singleton
tiles have only an opposite blank, and full tiles have none. Independent
leg heights do not change this reasoning. The unique positive phase from
the established phase table is a tile-preserving transport of this reference
description, so every grid symmetry and positive alignment is covered.

## 3. Old blank sites adjacent to old endpoints cannot become selections

Every original occupied site remains occupied: supports either survive or
become endpoints. A final blank is therefore originally blank in every
module. We will use the following consequence of the fusion hypotheses. If v was
blank in module A and adjacent to p in P_A, then any final occupancy at v
must be an endpoint. Otherwise v is a retained original selection of some
different module B, and it sees its persistent B-anchor and p, two different
endpoint neighbors. This contradicts selected feasibility. An optional added
selection cannot see p either. This argument counts original anchors even
when other support incidences have been consumed.

## 4. Both canonical donor tiles survive without any marked-side assumption

Normalize one module A and its left donor tile:

    u=(2,2), z=(2,3), x=(3,2), y=(3,3).

Initially x is selected and u,z,y are blank. Original A-endpoints include
n=(1,2), a=(2,1), p=(3,1), q=(1,3) and b=(4,1).

First u cannot become an endpoint. If u belonged to a foreign module B,
exterior support would put an original B-endpoint at n or a, the only two
neighbors of u outside this tile. Both are A-endpoints, contradicting endpoint
disjointness. Section 3 also excludes u as a new selection, so u stays blank.

Next x cannot become an endpoint. Blank-corner continuation in its putative
foreign module, applied to its blank intratile neighbor u, would put the
continuation p in that foreign endpoint set. But p is an A-endpoint. Thus x
remains selected. Since it already sees p, final feasibility keeps y and
(4,2) blank, as well as u.

Finally z cannot become an endpoint. Applying blank-corner continuation to
its blank intratile neighbor u puts its exterior continuation q in the same
foreign endpoint set, contradicting disjointness. Section 3, using q,
excludes z as a selection. Thus z stays blank.

This is an actual endpoint-free tile with exactly the retained selection x,
not a formal capacity token. The three blank sites of the left protectors
are u,(4,2),z; all stay blank, so this side is unmarked. Reflect by the
tile-preserving map (r,c)->(r,w+1-c) for the right side. All six protector
events remain absent: G=0. The two within-module donors are different for
w>=6, and the previous actual-selection/anchor injection proves that donors
from distinct modules cannot coincide. Consequently D>=2N without reuse.

## 5. Every intratile event is paid at its own new full tile

Consider an endpoint p contributing to K, and its unique originally blank
neighbor v in the same tile Q. Section 3 shows that newly occupied v is a
foreign endpoint. Of the three original tile profiles, only a two-endpoint
profile has an intratile blank adjacent to an endpoint. Write u for its
other original endpoint and x for its original selection. The four corners
are the edge p,u and the edge v,x. Retained x would touch both u and v,
so x is consumed as a foreign endpoint. Hence Q is full and mixed, counted
once in J.

Each original two-endpoint profile has exactly ONE endpoint adjacent to its
blank corner, so it contributes at most one K event in Q. Its two original
endpoints are different from the endpoints of every other original module.
A four-corner tile contains at most two such two-endpoint groups. Therefore
each new full tile receives at most two K events, and K<=2J. This is a
tile-by-tile injection/capacity bound. No extra donor is assigned to Q:
its only credit remains -2 in the physical fusion charge ledger.

The exact ledger gives rho_final=N-2J+K. Subtract it from D>=2N to obtain
(1). This completes the general proof.

## 6. Why pair discovery alone cannot establish this theorem

Feasibility is not hereditary under deleting original modules. In the width
eight four-way cycle, the full four-module fusion is feasible and fully
frozen. Every one of its six two-module subcollections has a retained
selection with at least two occupied neighbors, so is infeasible. Endpoints
of the omitted modules normally consume those conflicting supports.

The saved finite pair search therefore covers feasible two-module unions
only. It does not classify the contact pairs inside feasible larger unions.
Sections 3-5 above use the FINAL fusion, so do not make that inference.

## 7. Positive-tail cancellation also localizes the mixed-phase problem

The proof in Section 5 needs the positive profile only at the SOURCE of
the intratile event. Foreign endpoint modules can have arbitrary supported
profiles. Consequently, in any feasible fusion of the covered two-leg/rotor
family, partition K=K_positive+K_nonpositive by the original tail's module.
Every positive-source event still lies in a new mixed full tile. Each such
event uses two disjoint original positive endpoints there. Hence

    K_positive <= 2J.

More precisely, let k_positive(Q) be the number of positive-source events
at new full tile Q and define its UNSPENT correction credit

    C = sum_{new full Q} (2-k_positive(Q)) = 2J-K_positive >= 0.

Applying the preceding dual-guard theorem, with all original modules covered
and no additional charge tau, gives the mixed-phase corollary

    sigma >= N+S+C-K_nonpositive-G.                (2)

Thus K_nonpositive+G<=N+S+C is sufficient, and the simpler condition
K_nonpositive+G<=N+S is sufficient as well. The old one-side criterion is
automatic if K_nonpositive+L<=S. These latter conditions are not assumed to
hold for arbitrary mixed fusions.

The partition is by persistent ORIGINAL module ownership, even when final
endpoint components merge. Each positive tail is assigned to its own
physical full tile, and each tile's two correction units are consumed there
before C is used. Those units are never actual donor tiles. The deficit
units remain the distinct unmarked-side tiles from the dual-guard theorem.
This isolates the unsolved tax on nonpositive modules and affected sides,
without spending the same -2J correction twice.

For occupied adjacent bands, K_positive=2,K_nonpositive=2,J=2,G=0,
so C=2 and (2) gives sigma>=w. For canonical opposed bands,
K_positive=K_nonpositive=C=0,G=2, so (2) retains w-2. The latter case
still loses both canonical donors. The corollary was derived after the
automatic all-positive theorem's review input and is outside that input.

## 8. Verification scope and remaining questions

Run the coordinate controls with

    python3 develop/check_positive_phase_fusions.py --output output/positive-phase-fusion-controls.json

The saved run passes 240 positive-phase module images, 57 complete
all-positive fusion controls and 306 mixed-phase controls. Seventy-six mixed
controls have actual positive-source intratile events; the local cancellation
is tested on genuine events, not only the zero-event all-positive examples.
All six two-module subsets in the nonhereditary control fail feasibility
while the four-module union is feasible and fully frozen. No all-positive
degree-four fusion was found among the supplied controls.

The coordinate checker separately verifies the thirteen profiles, exterior
support and blank-corner continuation for positive phases and unequal legs;
it also verifies complete physical fusions and the nonhereditary four-way
example. These are controls for the all-parameter proofs, not their premises.
The Lean source checks the finite LOCAL profile implications and the abstract
exterior/continuation exclusion interfaces and scalar cancellation. The
global coordinate adapter and the all-parameter constructor classification
remain the written arguments above. All 14 declarations and individual axiom
audits pass with local Lean 4.33.0. The local thirteen-profile implications
are finite kernel reductions, not a parameter search extrapolated to grids.
Only standard propext and Quot.sound occur, with no sorryAx or native_decide.
See formal/SubQuorum/PositivePhaseFusions.lean and the separate receipt
output/positive-phase-fusion-formal-check.json for the exact scope.

The preceding dual-guard review completed ACCEPT with its two valid prose
qualifications applied. The present all-positive theorem has a separate
same-conversation review e423b1d5-d4ce-4a95-a7da-c315931443a3, original
stream 20573. Its input includes Sections 1-6 and the earlier verification
scope, before the later mixed-phase corollary was appended. It completed
ACCEPT at 2026-10-19T22:03:47.780UTC, gpt_6/pro. The original stream ended
with DONE and its 19306-character answer matches the terminal response.
Its sole readability suggestion, explicitly stating persistence of original
occupancy, was already applied in Section 3. No mathematical correction is
needed. See reviews/2026-10-20-positive-phase-fusion-assessment.md. The
mixed-phase corollary does not inherit a review of the earlier input.

This proves automatic finer compensation for the stated all-positive class.
The subsequent REGULAR_TILES_ZERO_ROTORS_AND_IRREGULAR_TAX.md extends
automatic compensation to arbitrary zero-charge rotors and isolates a
height-independent irregular tax for mixed phases. Its new results have
separate evidence and review scope. Full mixed-phase coverage, a general
endpoint-component decomposition, the unrestricted grid bound and external
priority remain open.
An actual all-positive degree-four example would test the strict coverage
gain; no such example is asserted here.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
