# Activated singletons cancel the zero-rotor event deficit

20 October 2026. In the complete fixed-source U/rotor model we prove a
universal event reserve, with additional payment for activated positive
tips and marked sides whose gates remain blank. No width, leg-height,
phase, receiver-separation or contact-graph restriction is imposed.
The proof counts all activated singleton occurrences at once: rotor
forwarding terms cancel, so no path termination assertion is required.

## 1. Hypotheses and result

Use the complete fixed-source model and established ledger of
ALL_PHASE_JOINT_COMPENSATION_SLOTS.md and the accepted half-slot theorem
ACTUAL_IRREGULAR_HALF_SLOT_BUDGET.md. Each U has arbitrary even width
at least six and independent even leg heights at least four. Every
lattice isometry, translation and effective phase is allowed, as are
arbitrarily many rotors of every phase. The family is finite. Original
endpoint sets are disjoint; P and M are their unions. All original
supports outside P persist in T. Final feasibility requires every
selected point to have at most one occupied neighbor. Optional extra
selections obey the original model's restrictions. All ownership and
profile counts below refer to original sources, even after components
merge.

Retain N, S, C, Kirregular, G, B11, BU, BR and Lambda from the half-slot
note. In particular Lambda_Q=i_Q+b_Q-2(k_Q-c_Q)>=0, Lambda=sum Lambda_Q,
and the exact identity is

    2(S+C-Kirregular)=2B11-BU-BR+Lambda.              (1)

Call an original 1P2T singleton occurrence activated if at least one of
its two original intratile supports is in final P. Occurrences retain
their source and tile labels. Let Aplus count activated positive-U
terminal singleton occurrences, and Gb count marked canonical sides
whose gate is finally blank. There are two such original positive
terminal occurrences per positive U, so 0<=Aplus<=2N; also 0<=Gb<=G.

**Singleton-flow theorem.** Every complete feasible fusion satisfies

    BU+BR+Aplus+Gb <= 2B11+Lambda.                   (2)

Consequently

    Kirregular <= S+C-ceil((Aplus+Gb)/2),            (3)
    sigma >= N-G+ceil((Aplus+Gb)/2).                 (4)

In particular Kirregular<=S+C universally. This removes the previous
floor(BR/2) event penalty. If G=0, sigma>=N>=0 without any zero-rotor
phase restriction. In these unmarked complete-source fusions the
coefficient-one inequality |T|+|M|<=mn/2 improves the existing 5/6
matching coefficient by |M|/6. This is a statement about the stated
source model, not a decomposition theorem for every grid configuration.

## 2. Activated singleton capacity in one physical tile

Let d_Q count activated original regular (1P2T) singleton occurrences.
Let f_Q indicate a final full 3+1 tile whose singleton is regular.
Then

    d_Q <= Lambda_Q+f_Q.                            (5)

Here is the general local classification. Original supports remain
occupied whether selected or consumed. For an activated regular
singleton q, both adjacent corners of its tile are therefore occupied.
If the final tile has two endpoints, one support has been consumed;
the other remains selected. Its original anchor q forces the fourth
corner to remain blank. The consumed endpoint is an inactive irregular
singleton, so i_Q=1, k_Q=c_Q=b_Q=0 and Lambda_Q=1. There is only one
regular singleton in this tile.

If the nonfull tile has three endpoints, both original supports were
consumed: retaining either would give it two occupied neighbors. The
old regular singleton is the elbow of the L. Its two leaves are
diagonal and cannot form one connected original pair. Each leaf's
other adjacent corner is finally blank and hence was originally
blank. Thus both are inactive irregular singletons. Here Lambda_Q=2
and d_Q=1.

For a full 2+1+1 tile, the accepted table gives Lambda_Q=2-q, where q
counts irregular singleton owners; this is exactly its regular
singleton count. For four singletons Lambda_Q=4-q, again their regular
singleton count. In a full 3+1 tile with a regular singleton,
Lambda_Q=0 and d_Q=f_Q=1. All other partitions have d_Q=0. An
unactivated regular singleton needs no payment. This proves (5).

Split F=sum f_Q into FU and FR by the original three-endpoint owner.
The complete catalogue says that owner is a phase11 U or a zero rotor.
Every phase11 U has exactly two original triples. A triple counted in
BU has an irregular singleton in its fourth corner, whereas one
counted in FU has a regular singleton. These are disjoint uses, giving

    BU+FU <= 2B11.                                  (6)

## 3. A filled zero-rotor triple activates a distinct singleton

Normalize the source to Rplus(-3,0). Its triple in
Q={0,1} x {2,3} consists of (0,2),(0,3),(1,3), with missing corner
p=(1,2). The same source has a regular singleton q=(0,1) in
Q'={0,1} x {0,1}, with original supports (0,0),(1,1).
If p is a final endpoint, the old support x=(1,1) sees both q and p.
It must therefore be consumed into P, activating the singleton in Q'.

The half-turn (r,c)->(-1-r,5-c) preserves this source and the tiling.
It gives the second pair: missing corner (-2,3), support (-2,4),
singleton anchor (-1,4). These are its two distinct triples and its
two distinct regular singletons. Thus the pairing is bijective.
Tiling-preserving isometries transport it to every placement of a
zero rotor with 3P0T groups. The other zero-rotor phase has no triples.
This finite role calculation is exhaustive for the rotor orbit, not
a bounded search over possible foreign sources.

Let DR count all activated regular singleton occurrences owned by zero
rotors. Every actual BR contact fills a triple, and every FR contact
does too. The bijection and support forcing give

    BR+FR <= DR.                                    (7)

The DR occurrences and Aplus occurrences have different original
sources. If D=sum d_Q counts all activated regular singletons, then

    BR+FR+Aplus <= D.                               (8)

## 4. Blank-gate marks use separate local capacity

Normalize a marked positive canonical tile to
u=(2,2), z=(2,3), x=(3,2), y=(3,3), where u is its finally blank gate.
The established marked-side assignment and rotor barrier give an
original phase11 U owner at a witness t in {x,z}. Its original profile
in this tile is either the upper-corner irregular pair {t,y} (2P0T),
or the terminal regular pair {t,y} (2P1T).

In the upper-corner case Lambda_Q is two if the final tile contains
only this pair, and one if the remaining available corner becomes
an endpoint. In the terminal case its original selection is the
remaining corner of {x,z}. It sees its own anchor and the persistent
positive endpoint (3,1) or (1,3), respectively, and must be consumed.
The resulting inactive irregular singleton gives Lambda_Q=1.

This tile contains no original regular singleton: x and z each have
the finally blank u as a neighbor, while y already belongs to the
assigned pair. In particular d_Q=f_Q=0. Distinct marked canonical
sides have distinct tiles by the established donor-tile injection.
Thus, with g_Q indicating a blank-gate mark, the local statements
combine without sharing any unit:

    d_Q+g_Q <= Lambda_Q+f_Q,
    D+Gb <= Lambda+FU+FR.                           (9)

The full support condition matters here. A finally blank gate was
unoccupied in every original source. One cannot replace that fact by
its absence from an endpoint lower-bound mask.

## 5. Global cancellation and consequences

Combine (8) and (9), cancel the same FR on both sides, and use (6):

    BR+FR+Aplus+Gb <= Lambda+FU+FR,
    BU+BR+Aplus+Gb <= Lambda+2B11.

This proves (2). No route is selected, and no acyclicity is assumed.
Cycles of forwarding contacts contribute equally to both sides and
cancel. Each activated occurrence, U triple and physical tile capacity
was counted once. Lambda already uses c_Q after all regular events
were paid; the argument never spends C separately again.

Equation (1) now gives 2(S+C-Kirregular)>=Aplus+Gb. Integrality yields
(3), and substitution into the established ledger yields (4).
The general coefficient-one target still requires

    2G+BU+BR <= 2N+2B11+Lambda.

The theorem proves it whenever 2G<=2N+Aplus+Gb. A violation must have
2G-Aplus-Gb>=2N+2, because both sides in the exact reserve comparison
are even. Thus a violating fusion with N=1 would need G=2, Aplus=Gb=0
and S+C-Kirregular=0. These are necessary conditions, not a feasible
counterexample. Occupied gates whose supports do not activate positive
tips remain the unresolved obstruction. The source-width subclass
claims in the exploratory Oracle response are not adopted here.

## 6. Verification and formal scope

develop/check_activated_singleton_budget.py independently checks the
complete local signed catalogue, the zero-rotor pairing and complete
physical fusion controls. The local classification, full support
forcing, source normalization and cancellation above are the general
proof; finite examples do not substitute for them. The existing
physical fixtures exercise activated positive tips and both kinds of
zero-rotor filled triples. They contain no blank-gate mark; that
branch is checked separately by its complete normalized local cases
and the written source/side argument in Section 4.

formal/SubQuorum/ActivatedSingletonBudget.lean checks both complete
local tables, the two original support bridges and distinct target
tiles, and conditional cancellation/reserve/slack arithmetic.
The arbitrary-source normalization, source-to-profile adapter,
geometric blank-gate assignment, summation and incidence injection
remain written. This is not a full Lean theorem of arbitrary fusions.
Execution and individual axiom evidence are separate from proof review.

All434 feasible local packings pass, including six normalized blank-gate
states;32 rotor images and640 complete physical images pass. Positive
tip activation occurs in224 images, BR contacts in eight and FR contacts
in eight. All10 scoped Lean declarations and individual axiom audits
pass locally with Lean4.33.0, one job, no sorryAx/native_decide. See
output/activated-singleton-budget-controls.json and
output/activated-singleton-budget-formal-check.json for exact scope and
reproduction. Review2d57a5d5 on original stream75421 terminated with
infrastructure_retry_exhausted/cdp_disconnected@typing after four broker
attempts, with no mathematical answer. Its failure is archived. After
that terminal state, a fresh combined review of this proof and
OCCUPIED_GATE_ACTIVATION_AND_WIDTH_SIX.md was submitted on original
stream28290 with one text attachment. It is live without a verdict;
no earlier ACCEPT covers either proof.

The support-routing idea originated in exploratory Oracle task
ef7e27ea-8c3f-4cdc-8b5d-721df8e896c6. This note reconstructs the
universal part as a direct incidence cancellation. That exploratory
answer is not an independent review of this proof. The unrestricted
occupied-gate allocation and rectangular-grid equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
