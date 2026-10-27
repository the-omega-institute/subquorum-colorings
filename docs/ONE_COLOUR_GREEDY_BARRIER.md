# Three internal contacts defeat sequential colour-cost optimization

Even after coverage has been reduced to ordinary maximum flow, its TOTAL
payment cost cannot be optimized by first minimizing one terminal colour's
cost and then optimally completing the other. The approximation ratio of
that sequential rule is UNBOUNDED, with only three prescribed, pairwise
vertex-disjoint, entirely internal squares on ONE original TT/HH pair.

The joint optimum is attained by two contacts; the first-colour minimum
forces the third contact alone. The rule fails even with optimal second-stage
completion and all ties resolved in its favour. The target sub-quorum
inequality and alternative contact pools are not counterexamples here.

## 1. A feasible all-size board

Use the domino coordinates and full horizontal N of the
[five-contact construction](FIVE_CONTACT_SPARSIFICATION_BARRIER.md), with
even L>=4 and d>=1. Thus the physical rectangle is

    -6<=x<=4d+43,  -4<=y<=L+5,

and D(i,j)={(2i,j),(2i+1,j)}. Put c3=d+9,c4=d+13,c5=2d+14.
Keep its complete original B path unchanged. Replace only A's width-d
serpentine by a width-ONE serpentine:

    (0,0)->(c4,0)->(c4,2),
    rows j=2,...,L-1 between columns c4 and c4+1,
    east on even j, west on odd j, and up after each row,
    then (c4,L)->(c5,L)->(c5,0)->(c5+4,0).

The old B is the same explicitly specified path in that note: its serpentine
is columns 9,...,c3, rows 3,...,L, followed by its listed separated exterior
returns and final endpoint (4,1). Each domino is traversed black-to-white;
M joins consecutive white-to-black vertices. Keep

    T={(0,0),(4d+37,0)}.

The new A lies in the old A bounding rectangle, with the SAME top, return
and endpoint segments. Narrowing its serpentine introduces no repetition:
rows remain distinct and its return c5 is beyond c4+1, since d>=1. The old
separation proof from B still applies. The unchanged neighbors of both T
sites give selected degree exactly one. Hence this is an actual feasible
matching on the complete rectangle for EVERY allowed L,d.

Prescribe only old contacts 2,3,4, relabelled g1,g2,g3:

| Local contact | A domino | B domino |
| --- | --- | --- |
| g1 | D(8,0) | D(8,1) |
| g2 | D(c3,0) | D(c3,1) |
| g3 | D(c4,0) | D(c4,-1) |

Their supports are disjoint, and all twelve contact vertices belong to P:
each displayed cut domino has both an incoming and an outgoing M edge.
Their canonical orders are A:g1,g2,g3 and B:g2,g1,g3. No terminal cut is used.

## 2. Exact fragment weights and all successful choices

In A order let the four M-fragment weights be a0,alpha,gamma,a3; in B
order let them be b0,beta,eta,b3. Direct unit-step counts give

    a0=8, alpha=d+1, gamma=4,
    w_A=d+3L-1, a3=w_A+4,
    b0=1, beta=(L-1)d+2L+1,
    eta=2L+3d+33, b3=d+29.                            (1)

Here w_A counts A's excursion from old contact 4 to old contact 5:
2+(L-2)+(L-2)+(d+1)+L=d+3L-1. The remaining B weights are unchanged:
beta is its old serpentine, eta is the sum of its old gaps v+t, and b3 is
its old gap s. Therefore

    |M|=(L+5)d+7L+80.                                (2)

Every singleton repairs the original TT/HH pair. The only successful pair
is {g1,g2}, whose orders are reversed. It creates one P-only cycle with
exact physical M credit alpha+beta=Ld+2L+2. The other pairs are same-order
and fail. All three also fail: the reversed block {g1,g2} swaps the two
terminal destinations, and the later contact g3 swaps them back. Its free
cycle is insufficient to certify terminal coverage. The empty subset fails.
This local structural classification proves for all parameters that

    C_joint=|M|-(alpha+beta)=5d+5L+78,                 (3)

attained uniquely by {g1,g2}. No physical edge is credited twice.

## 3. The first-colour minimum forces the wrong operation

Red denotes the directed TH path from A's BLACK selected endpoint to B's
WHITE hole, exactly as in the [two-colour cost model](CONTACT_FLOW_CUT_AND_EXACT_COST.md).
Blue denotes the complementary TH path. The red M costs of the covering
choices above are

    {g3}:       a0+alpha+gamma+b3 = 2d+42,
    {g1}:       a0+eta+b3        = 2L+4d+70,
    {g1,g2}:    a0+eta+b3        = 2L+4d+70,
    {g2}:       a0+alpha+beta+eta+b3.

Since 2L+2d+28>0, the unique minimum red terminal-path resource set is the
one for {g3}. Nonnegative coloured cycles cannot improve it. Every nonempty
cycle here has positive M weight, so they cannot create another optimum.

One can verify this directly for ALL red flows, including circulations.
Let x,y,u,v be the red bits on alpha,beta,gamma,eta respectively. The
terminal bits on a0,b3 are 1 and those on b0,a3 are 0. Conservation gives
x=y+u and u+v=1, so the only possibilities are
(x,y,u,v)=(0,0,0,1),(1,0,1,0),(1,1,0,1). The first is the direct red
path, the second the cheap red path for g3, and the third the direct path
plus the positive alpha+beta circulation. Their costs are exactly the
ones above. This proves uniqueness over all flows, not only the displayed
terminal paths of successful switch subsets.

This red path uses A through g1 and g2, crossing only at g3. At g1 and g2
red must go straight; at g3 it must cross. Thus fixing this minimum red flow
forces ALL THREE local choices. Even optimal blue completion, or resolving
every tie in favour of total cost, leaves the singleton {g3}, with no cycle:

    C_sequential=|M|=(L+5)d+7L+80.                     (4)

The joint optimum deliberately pays MORE for red and LESS overall. Its blue
cost is b0+gamma+a3=d+3L+8. This is a verified failure of lexicographic
red-first optimization itself, not just of an arbitrary local decoder.

For d=L,

    C_sequential=L^2+12L+80,
    C_joint=10L+78,
    C_sequential-C_joint=L^2+2L+2,
    C_sequential/C_joint -> infinity.                (5)

For an explicit quantified witness, C_joint<=30L for L>=4. For any integer
K>=0 choose even L=100(K+1)>30K. Then

    K*C_joint <= K*30L < L^2 <= C_sequential.

For example L=d=20 gives an actual 30-by-130 board with |M|=720. The red
minimum is 82 and forces total cost 720. Jointly optimizing uses red cost
190 and blue cost 88, total 278. At L=d=40, costs are 2160 versus 478.

## 4. Scope and verification

The sequential rule is: first find a minimum-M full red flow in this SAME
three-contact pool, then find a minimum-M blue completion subject to its
fragment-capacity exclusions. The theorem refutes every constant factor for
that rule. It does not refute the unweighted max-flow coverage criterion,
the exact two-colour joint model, or optimization over other squares/N.

Actual J=|M|+2 is below half-area by Ld+15d+18L+168>0, so no numerical
sub-quorum bound is contradicted. Finite physical controls are validation;
the coordinate, order and weight arguments above prove all allowed sizes.

Local evidence: [physical/abstract controls](../output/contact-flow-cut.json),
[post-submission edge cases](../output/contact-flow-edge-cases.json),
[Lean source](../formal/SubQuorum/ContactFlowCut.lean),
[scoped Lean execution](../output/contact-flow-formal.json), and
[independent audit status](../output/contact-flow-review.json).
The eleven Lean declarations include arbitrary-label local switch completion
and a quantified even-L unbounded-ratio witness; physical embedding, global
flow/min-cut optimality and the cost-model equivalence remain written.

Independent audit: initial REVISE concerned one ancillary five-contact summary
quantifier, now corrected. Follow-up ACCEPT covers the corrected package. The
auditor reproduced the submitted main with complete parsed-JSON equality; no
Lean or new follow-up executions occurred. Post-submission edge cases remain
local-only evidence. Full initial and final responses are linked in the receipt.
