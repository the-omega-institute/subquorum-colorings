# Paired holes: exact certificate deficit and maximum-matching traps

Continuation: [the all-live shared-gate tradeoff](LIVE_GATE_CERTIFICATE_TRADEOFF.md)
resolves the remaining ABSTRACT existence question negatively: even after
safe pruning, every maximum certificate can lose q-1 payments, at terminal
degree two. It proves the exact coverage/payment frontier. Frozen realization
remains open; 576 existing physical systems have explicit optimum maximum
certificates.

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

The [partial-certificate theorem](PARTIAL_TIP_COMPENSATION_AND_SAFE_PRUNING.md)
has an exact refinement: its fine budget is the actual deficit of the
certificate's assigned-interval allocation, not merely an upper bound. Every
component has at most two holes. Exactly the two-hole components lose one
payment each. Moreover, optimizing over ALL partial certificates recovers the
ordinary whole-support compensation optimum, and an optimal certificate can
be extended to an inclusion-maximal one without losing payment.

Maximum cardinality is a different requirement. A four-owner abstract system
has a UNIQUE maximum terminal matching, and it loses a payment that a smaller
matching certifies. This particular trap disappears under safe pruning. A
separate completely frozen physical construction survives safe pruning and
has two holes in one original interaction component. It has both bad and good
maximum terminal matchings: moving one slot assignment to a second original
interval repairs the bad one, with no new links and no reused resource.

The all-parameter constructions and general proofs below do not depend on
enumeration. These results identify failures of certificate-selection rules;
they are not counterexamples to the frozen-grid inequality and do not improve
the universal 5/6 bound.

## 1. Fixed model and exact two-hole chains

Use the finite original alpha/beta/mixed owner system, declared TP--BP links,
fixed whole supports W and available ORIGINAL interval set I of the preceding
note. Previously immutable links have already been contracted. A partial
certificate injects some TP ends into actual neighboring BP identities or
I times {0,1}. A slot assignment requires its owner's support witness. No
maximum-matching hypothesis is imposed.

Select its BP-assigned links C. Form Q on final alpha paths and the original
intervals actually assigned to their free TP ends. Retain one incidence edge
PER ASSIGNED END, so two ends using the two slots of one interval give parallel
edges. Each alpha vertex has degree 2 minus its hole count; each interval
vertex has degree at most two. Isolated alpha vertices remain in Q; intervals
with no assigned alpha end can be omitted. A hole on a final mixed path is
not an alpha demand.

**Lemma 1 (exact certificate deficit).** For every Q component K, its hole
count h_K belongs to {0,1,2}. The maximum injective allocation using exactly
Q's incidence relation leaves h_K/2 rounded down alphas unpaid. Consequently

    B(M) = sum_K floor(h_K/2)
         = number of two-hole Q components
         = a - (b-b_C+r_Q),                              (1)

where r_Q is the maximum assigned-interval allocation, a,b are original
counts and b_C is the remaining beta count. Thus the fine budget is exact
for this certificate's allocation. It need not equal the deficit with all
other support choices or links allowed.

**Proof.** The finite incidence multigraph has maximum degree two, so each
connected component is a path, a cycle (including a two-edge parallel cycle),
or an isolated alpha. If it has A alpha vertices, J interval vertices and E
edges, then

    E+h=2A,  E<=2J,  A+J<=E+1.

These imply h<=2 and max(A-J,0)=floor(h/2). More concretely, a path with two
alpha endpoints has h=2 and A=J+1. Its J distinct edge-resource vertices
can pay all but any chosen root alpha, by orienting the chain away from
that root. A path with one alpha and one interval endpoint has h=1 and A=J;
alternation pays every alpha. A path with two interval endpoints has h=0
and J=A+1, and a cycle has h=0 and J=A; again every alpha can be paid.
An isolated alpha has h=2 and no payment. These allocations are optimal by
their component resource counts. Different components have disjoint original
intervals. Finally a_C-b_C=a-b and a_C-r_Q=sum floor(h_K/2) give (1). QED.

This is the degree-two path specialization of the existing
[one-sided allocation theorem](ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md),
applied to the ASSIGNED-SLOT incidence graph. The general tree allocation
principle is already in that note; it is not a new theorem here. The extra
observation is that the partial certificate also bounds the demand degrees,
so arbitrary branching trees and components with three holes cannot occur
in Q. An original interaction component CAN contain arbitrarily many holes;
it must not be confused with a component of Q.

## 2. Completeness of partial certificates; a safe extension rule

Write delta_ord for the minimum unpaid original alpha count among ordinary
whole-support stems, without beta-body forks. Then

    min over ALL partial certificates M of B(M) = delta_ord.   (2)

**Proof.** The preceding partial-certificate lifting theorem constructs
ordinary compensation of deficit at most B(M), so delta_ord<=B(M) always.
For the reverse direction take an optimum owner-disjoint ordinary stem
packing, as supplied by the existing
[normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md). Select all its actual
TP--BP route links. For each interval stem, assign the free TP at its last
alpha/mixed witness owner to slot zero of its payment interval. The witness
TP is free because the stem ends there. Distinct stems use distinct owners
and payment intervals, so this is an actual injective partial certificate.

A beta stem becomes mixed and contributes no final alpha demand. Each paid
interval stem becomes one final alpha with one assigned end, one hole and a
private assigned interval identity in Q. Each unpaid original alpha is an
isolated final alpha with two holes. Other unused owners are mixed or beta.
Therefore B is exactly the number delta_ord of unpaid original alphas.
This also constructs the certificate using exactly the packing's route links.
Together with the first inequality it proves (2). QED.

Equation (2) is a representation of the established ordinary flow optimum,
not a new faster optimization algorithm or a geometric saturation theorem.

There is a useful monotonicity rule. Replace every original interval j by
one artificial beta strand with two labelled BP ends j0,j1, and turn the
certificate's slot assignments into TP--BP links to these ends. This is an
auxiliary counting graph, never an extra grid resource. Lemma 1 implies that
its final alpha count is exactly B(M): after C, a final mixed component has
a permanently free BP end and cannot become alpha through interval links;
the remaining alpha components are precisely Q's two-hole chains.

**Lemma 2 (direct extension).** Adding one legal assignment between an
unassigned TP and an unused BP/interval slot never increases B. Hence an
optimal partial certificate can be extended to an inclusion-maximal one
while retaining B=delta_ord.

**Proof.** In the auxiliary strand graph the new assignment joins a free TP
end to a free BP end. If they are in the same path, that path was mixed and
closes to a cycle. Otherwise the possible endpoint component types are
alpha+beta -> mixed, alpha+mixed -> alpha, mixed+beta -> beta, or
mixed+mixed -> mixed. None increases the number of final alphas. Iterate
until no direct unused-target assignment remains. The finite process cannot
decrease B below delta_ord by (2), so an optimal starting certificate stays
optimal. QED.

This permits additions only. A bipartite matching augmentation that REASSIGNS
earlier targets is not covered. Inclusion-maximal and maximum-cardinality
certificates are different, as the next example proves.

## 3. A unique maximum can be strictly suboptimal

Use four original owners with NO intervals:

    A=(a0,a1) alpha;  B=(b0,b1) beta;
    M=(mBP,mTP) mixed; N=(nBP,nTP) mixed.
    Declared links: a0->b0, mTP->b0, a0->nBP.             (3)

The one-link certificate a0->b0 pays A, so delta_ord=0. It is inclusion-
maximal: the only other assignable TP mTP would need the occupied b0, while
a0 is already used and a1,nTP have no targets.

The UNIQUE maximum terminal matching has two assignments:

    mTP->b0, a0->nBP.

To achieve size two, mTP must take b0 and a0 must take nBP, proving uniqueness
without enumeration. It creates an alpha path A+N ending at a1,nTP and a beta
path M+B. Thus B=1 and its selected links pay no alpha. In particular,

    min_{maximum-cardinality M} B(M) > min_{all partial M} B(M).

For q disjoint copies the maximum is still unique, of size 2q and B=q,
whereas q one-link certificates have B=0. The gap is unbounded. This refutes
both automatic payment-preserving extension to a maximum and optimization
restricted to maximum certificates in the UNPRUNED abstract model.

Here M is unreachable from an alpha and N cannot reach any resource, so safe
pruning deletes both. This example does not refute existence of an optimal
maximum certificate in every safely pruned system. The physical example below establishes the
weaker, relevant point that an ARBITRARY maximum remains unsafe even after
pruning.

## 4. A completely frozen physical paired-hole configuration

Take the PP-sealed 10x16 fixture in
[the internal obstruction note](FROZEN_TIP_SLOT_OBSTRUCTION.md). For even
w>=30, put one original copy and its horizontal reflection

    (r,c) -> (r,w-1-c)

in a 10xw board. For q>=1 stack these paired boards by shifts (10i,0),
0<=i<q. Optionally append any even number of blank columns at the right.
The executable construction retains the full original T and matching sets;
safe pruning below changes only the compensation graph.

**Feasibility and complete freezing for every q,w,padding.** Each original
copy has all occupied points in rows 1..8 and columns 1..13. Its reflection
has columns w-14..w-2. At w>=30, the two occupied sets are at least three
columns apart; successive vertical copies are at least three rows apart.
Consequently no occupied adjacency is added between copies, the matching
edges remain disjoint, and all existing feasibility inequalities are
unchanged. Transport the base strict-rank freezing witnesses through each
reflection/translation and take their unions rank by rank. Every required
local witness is unchanged, so all 40q matching endpoints freeze. Blank
padding adds no occupied neighbor. This is an all-parameter proof, independently
checked against the actual freezing closure in the finite controls.

For one paired board, safe pruning leaves exactly two alphas A_L,A_R, two
betas B_L,B_R and two productive mixed owners R_L,R_R. The relevant tips are

| Owner | Left tips | Reflected right tips |
|---|---|---|
| A | TP (3,6), (6,6) | TP (3,w-7), (6,w-7) |
| B | BP (3,5), (4,5) | BP (3,w-6), (4,w-6) |
| R | BP (3,7), TP (3,8) | BP (3,w-8), TP (3,w-9) |

Both A supports are empty. Each lower A tip has no target after pruning.
This follows from the base PP seal and its reflection; neither blank padding
nor graph pruning releases any new physical gap. R_L and R_R have the same
original interval support: in band rows 2,3, the endpoint-free gap between
their TP ends has BT end columns 9 and w-10 and BB columns 10..w-11.
It therefore contains exactly w-20>=10 distinct, available interval units,
each shared by the TWO R owners. They are actual distinct original intervals,
not copies of one gap identity. These shared supports connect both alpha/beta
subsystems into ONE original interaction component.

There are six TP ends after pruning, of which the two lower A ends are
isolated. Maximum terminal matching cardinality is exactly four: an assignment
of all other four is given next. Thus the single alpha-containing interaction
component has a_D=2,h_D=2. This disproves automatic h_D<=1 for frozen pruned
systems. For q stacked pairs there are q such components, each with two holes.

**A bad maximum and its exact repair.** Choose two DIFFERENT interval units
j,k from this one shared gap. Assign

    upper A_L -> BP of R_L; upper A_R -> BP of R_R;
    TP of R_L -> (j,0);    TP of R_R -> (j,1).            (4)

This is a valid maximum terminal matching. Its Q is the chain

    [one hole] A_L+R_L -- original j -- A_R+R_R [one hole].

The two slots do not create two payments: j pays just one of its two alpha
demands, so h=2 and B=1, exactly as Lemma 1 states. Change ONLY the last
assignment to TP of R_R -> (k,0). The two Q components now each have one
hole and one private assigned interval, so B=0. The two selected links and
terminal coverage remain the same. The allocation pays the left path with
j and the right path with k; neither beta is consumed and no interval is
reused. This is a concrete capacity-two-or-larger gap repair, using the
existing one-sided allocation principle with its actual resource identities.

There is also an independent two-link beta payment, upper A_L->B_L and
upper A_R->B_R. Since both A supports are empty, at least one link is needed
per alpha, so the optimum is exactly two payments at minimum two links.
For q copies the same statements give 2q payments at minimum 2q links.
The defective maximum certificate, repaired maximum certificate and true
optimum therefore separate on an actual frozen geometry, even after all
safe mixed deletion.

**Reservation control and scope.** If the A->R links in (4) are the only
permitted links and all shared intervals except j have been reserved, there
really is a one-payment deficit in this restricted model. Both alphas have
just the ONE remaining unit. Restore k and the exact repair works. Restore
all original links instead and the two distinct betas already pay both
alphas, even with only j retained. Thus the exhibited failure is of the
certificate/resource restriction, not of the unrestricted target inequality.
For reservations across components, the same original j or k must never be
booked again; physical blank space or two interval slots supply no extra unit.

## 5. Reproducible verification and formal scope

Run:

```sh
python3 develop/check_paired_hole_certificates.py \
  --output output/paired-hole-certificates-validation.json
cd formal
lean SubQuorum/PairedHoleCertificates.lean
```

The deterministic checker verifies 3,750 certificates and 4,941 Q components:
400 seeded abstract systems, complete enumeration of all partial certificates
in 32 seeded small systems, 452 monotone direct additions, 16 disjoint-copy
unique-maximum traps, and 80 actual frozen physical systems. Physical controls
include q=1..8, w in {30,32,40}, right padding in {0,2,10}, and eight square
isometries with the two-row bands carried along. They check strict ranks and
actual complete freezing, independent reconstruction of strands, safe pruning,
maximum size, bad and repaired certificates, exact payment/minimum link cost,
and the restricted-resource versus restored-link distinction.

An independent auxiliary-strand computation replaces every interval by ONE
two-ended beta object and checks its final alpha count against both the Q
allocation and the preceding lifting verifier. Sparse optimal certificates
are extracted from independently optimized ordinary stem packings and extended
without reassignment. These finite checks support the written arguments;
they do not establish a universal geometric theorem.

Local Lean checks the connected-component arithmetic forcing h<=2 and exact
deficit floor(h/2), the identity counting two-hole components, and the
endpoint-type merge rule for a direct addition with arbitrary unchanged
components. It does not formalize the general
graph classification, normal-form extraction, all-parameter physical adapter,
or certificate optimization completeness. Those claims have written proofs
and computational controls. The previous base geometry module remains
available but is not relabelled as formal verification of this extension.

No new external Oracle review was obtained in this round. The previous broker
attempt terminated with model_unavailable, not an active review or acceptance.
The 11 October submitted manuscript, public main, PR #3 and shared CI are
preserved. This round does not read or send mail or change a draft.

The next geometric problem is to control the two-hole chains AFTER allowing
all legitimate distinct interval substitutions and productive mixed routes,
with earlier reservations fixed. A bad maximum matching alone cannot supply
that obstruction. Whether safely pruned physical systems always have SOME
maximum certificate attaining the ordinary optimum also remains open here.

The continuation linked above settles this question for general safely pruned
abstract systems; the frozen-grid restriction is still open.
