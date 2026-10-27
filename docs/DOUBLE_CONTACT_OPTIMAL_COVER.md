# Optimal disjoint pair compensation with one or two contacts

This note turns the isolated two-contact repair theorem into a costed
coverage certificate. It optimizes exactly over a stated class: match
distinct original TT paths to distinct original HH paths, and use either
one square or a reverse-order pair for each matched pair. Original TH
paths are unchanged. Coverage in this class is Hall coverage of DIRECT
TT/HH contacts; costs require both the lengths of the chosen HH paths
and the actual cycle credit. The theorem does not assert that this class
contains an optimum among all multi-contact or shared-component networks.

## 1. Exact local optimizer

Fix a feasible actual M and full auxiliary N, as in the
[contact-network theorem](CONTACT_NETWORK_CYCLE_CREDIT.md). For an
original TT path A and HH path B, list all available alternating unit
squares between them. These CANDIDATES need not all have disjoint
supports: only the one or two eventually chosen for this pair must.

Orient both paths from black Q to white Q. For contact g let x_g be the
number of M edges before its N cut on A, and y_g the analogous number on
B. If m_A,m_B are their total M-edge counts, then

    0<=x_g<=m_A, 0<=y_g<=m_B.                         (1)

Different N cuts on a terminal path have different prefix counts, since
successive N edges have exactly one M edge between them. A pair g,h
repairs A/B precisely when, after interchanging their names if necessary,

    x_g<x_h and y_g>y_h.                              (2)

Its closed cycle contains exactly their inner fragments, hence credit

    kappa(g,h) = (x_h-x_g)+(y_g-y_h).                 (3)

The strict inequalities ensure distinct cuts on BOTH paths. Their four
old N edges are therefore distinct edges of a matching, so have disjoint
vertices. Those edges comprise the two square supports. Thus (2) already
ensures the required square-support disjointness. No unverified geometric
compatibility constraint is missing from (3).

If at least one contact exists, define

    kappa_AB=max({0} union {kappa(g,h): (2)}),
    c_AB=m_A+m_B-kappa_AB.                            (4)

A single contact realizes the zero-credit option. Otherwise choose a pair
attaining the maximum. The previous two-contact dichotomy shows these
are ALL successful operations with at most two contacts on A/B, so c_AB
is exactly their minimum payment M cost. It is nonnegative because the
two inner fragments lie in the two original paths and use no edge twice.

There is an O(d log d) optimizer for d candidates. Sort by x, processing
equal-x contacts in a batch. For a current h query prior contacts g with
y_g>y_h for the minimum x_g-y_g. Equation (3) becomes

    kappa(g,h)=(x_h-y_h)-(x_g-y_g).                   (5)

A suffix-minimum structure on compressed y coordinates answers this and
stores a witness. Query a whole equal-x batch before inserting any of
its contacts, and use a STRICT y comparison. This handles candidate
squares sharing a cut without inventing zero-length or overlapping
cycles. Compare the resulting credits with zero. The code uses a
Fenwick minimum structure with reversed y ranks; the mathematical proof
is the invariant that the queried set is exactly x_g<x_h,y_g>y_h.

## 2. Exact batch coverage and cost theorem

Let L be all original TT paths and R all original HH paths. Form a
bipartite graph with edge AB exactly when at least one direct contact
exists, weighted by c_AB. A permitted batch chooses a matching F in
this graph and, for every AB in F, the one- or two-contact repair above.

**Batch theorem.** If |F|=s and original terminal counts are (a,b,t),

    (a,b,t) -> (a-s,b-s,t+2s).                        (6)

All affected physical resources have unique owners. If O denotes the M
resources of original TH paths, R_AB the M resources of A and B, and
C_AB the chosen pair's cycle resources (empty for a single contact),
then the final TH resources are EXACTLY

    U=O disjoint-union
       disjoint-union_(AB in F) (R_AB \ C_AB).         (7)

For arbitrary successful local choices write hat_kappa_AB=|C_AB|<=kappa_AB.
Their exact cost is |O|+sum_F(m_A+m_B-hat_kappa_AB). When EVERY chosen
local witness is optimal this equals |O|+sum_F c_AB and each actual credit
is kappa_AB. In both cases the C_AB sets are pairwise disjoint. They can
all be normalized into retained
auxiliary M edges simultaneously, without changing actual M or payments.

Proof. Different matching edges use distinct ORIGINAL paths. All their
vertices, chosen square supports and M resources are consequently
disjoint, even if unchosen candidates elsewhere share paths or cuts.
Apply the isolated single/two-contact theorem separately. Each replaces
one TT and one HH with two TH and possibly one P-only cycle. This proves
(6), (7) and all disjointness assertions. Normalization is componentwise
on the disjoint cycles. No original TH resource is reassigned or charged
again, and a cheap M-free bad path is not mistaken for a repaired path.

In particular the permitted class covers ALL selected terminals iff F
saturates L. Such an F exists iff |N(S)|>=|S| for every S subset L. Under
that condition its exact minimum payment M cost is

    |O| + min_(F saturates L) sum_(AB in F)
                     (m_A+m_B-kappa_AB).              (8)

Every FULL-COVERING permitted batch supplies a matching saturating L
and a valid local option on each matched pair, so
it costs at least (8). Conversely a minimum-cost saturating matching
and the local witnesses attain (8), proving both directions. A standard
unit-capacity min-cost flow computes it. When saturation fails, residual
reachability supplies S with |N(S)|<|S|; this certifies failure of THIS
direct, disjoint-pair class, not of other N, TH relays or general payment.

Maximizing total credit ALONE is not the cost objective: matched HH paths
can have different lengths. The m_A terms are fixed under full coverage,
but m_B and kappa_AB must both remain in (8). Original component matching
prevents reuse of a HH path even when it offers several attractive
double-contact repairs. Unlike the previously refuted individual-relay
Hall graph, the witnesses here have genuinely disjoint original resources.

For a fixed matched set F, replacing its single-square repairs by optimal
double-contact options saves EXACTLY sum_F kappa_AB actual payment M
edges. These savings change the certificate cost, not actual |M|. When
L is covered, J=|T|+|M|=area/2-(b-a); no universal coverage or new universal
5/6 inequality follows from optimizing within this class.

## 3. Arbitrarily many simultaneous zero-cost repairs

For q>=1 and even W>=4 take a 4q-by-W board. For each j=0,...,q-1 put
horizontal M edges at odd starting columns in rows 4j+1 and 4j+2. Let N
be horizontal pairs starting at even columns in EVERY row. Select the
two end sites of each row 4j+1; all other Q sites are holes.

Each selected site has one horizontal P neighbour and vertical hole
neighbours; different blocks' selections are separated. This is feasible.
The middle rows of every block form one original TT and one original HH.
Pair those two paths and choose squares (4j+1,0),(4j+1,W-2). By the
all-length ladder theorem each pair gives two zero-M TH payments and a
cycle containing its entire 2(W/2-1)=W-2 original M edges. Across all q
blocks everything is disjoint. Therefore

    |M|=q(W-2), |T|=2q,
    (a,b,t)=(q,q(W+1),0) -> (0,qW,2q),
    total credit=q(W-2), final payment M cost=0.       (9)

Nonnegative costs show this attains the exact class optimum, not merely
a computed upper bound. The supports, actual M, and old N are explicit
at every q,W. The 4-row case already has unbounded savings per pair;
(9) proves simultaneous savings with arbitrarily many distinct owners.
These boards have J=qW and area/2=2qW, so they are not sharp obstructions
for the numerical target. Their role is to realize the exact batch ledger.

## 4. Validation boundary

The checker compares the fast local optimizer with quadratic pair search,
the min-cost matching with exhaustive small matching assignments, and the
chosen batch with direct physical path/cycle decomposition. It checks
actual M-edge and vertex sets, full auxiliary matching, terminal coverage,
retention normalization and Hall witnesses. The all-size proofs above
do not depend on these finite controls. Scoped Lean verifies the ordered
prefix-credit identity and conditional batch sums; the geometric adapters
and weighted matching theorem remain written.

The [actual five-contact counterfamily](FIVE_CONTACT_SPARSIFICATION_BARRIER.md)
now proves that arbitrary multi-contact repairs can beat every one/two-contact
option by an UNBOUNDED factor, even on a feasible planar grid with just two
original paths. This does not alter the exact class optimum (8); it rules out
extending that class theorem to unrestricted contact subsets. More general
networks and universal 5/6 improvement remain outside this theorem.

The [review receipt](../output/double-contact-cover-review.json) records the initial
REVISE, the two corrected quantifiers in Section 2, reproduced Python output
and the follow-up infrastructure failure; no final acceptance is claimed.
