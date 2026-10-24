# Component-isolated simultaneous auxiliary compensation

## Setup and statement

Fix a finite actual endpoint set P, a perfect actual matching M on P, and
an auxiliary matching A. Every A-covered endpoint is an original PP
endpoint. Every A-free endpoint has its original TP (negative) or BP
(positive) label. Retain parallel edges in M union A. Its components are
alternating paths and cycles. Write k,b,g for the numbers of TP--TP,
BP--BP and mixed paths. Assume the matching-closed packet ledger

    S_J-B = |I|+b-k,

where I is the set of distinct original unmarked interval units.

All new auxiliary edges below belong to a declared permitted relation.
The theorem is conditional on that relation's geometric justification.
It concerns endpoint accounting: overlapping drawings of witnesses do not
generate or spend interval units. If a proposed physical interpretation
imposes additional witness capacities, those need separate verification.

An A-augmenting path starts and ends at A-free vertices, has odd length,
and alternates new edges with old A edges, starting and ending with new
edges. It is simple; all its internal vertices are A-covered. Its support
is the set of original M union A components containing its vertices.

**Simultaneous compensation theorem.** Suppose there are r such paths,
each starting at a TP of an original alpha and ending at a BP of an
original beta. Assume each path's support consists of exactly that one
alpha, that one beta, and any number of cycles. Assume the r supports
are pairwise disjoint as sets of original components. Toggle all paths
in A to obtain N. Then:

1. N is a matching covering every original PP endpoint and exactly r
   additional original TP and r additional original BP endpoints.
2. Every affected support contains one final mixed path and any number
   of cycles. Every other original component is unchanged.
3. The final counts are alpha_N=k-r, beta_N=b-r, mixed_N=g+r. Thus
   the original physical ledger is unchanged, with no cut debt.
4. An injective payment of the other k-r original alphas by I remains
   valid, provided its access certificates depend only on those unchanged
   components and the unchanged original interval identities. If f=k-r
   units are used, then

       S_J-B = (|I|-f)+(b-r) >= 0.

No original beta, PP component or interval unit is used twice. The theorem
does not assert that the required supports exist for every frozen grid.

## Proof

First consider one path. At an internal vertex, toggling removes its
unique old A edge and inserts exactly one new edge. At each endpoint it
inserts one new edge. No other A edge changes. Simplicity guarantees that
these operations produce a matching, preserve coverage of every originally
covered endpoint, and newly cover precisely the two stated free endpoints.

The union of all original components in its support is closed under M
and A. Every inserted edge also lies within this union. Therefore no
modified component can leave the support. Originally the support has
exactly four free ends: the two TP ends of its alpha and the two BP ends
of its beta. Toggling covers one of each, leaving exactly one TP and one
BP. In M union N every vertex has degree one or two, since M is perfect
and N is a matching. Each non-cycle component consequently has exactly
two free ends. There is therefore exactly one path in the support; its
ends have opposite labels. All other resulting components are cycles.
The operation consumes exactly one alpha and one whole beta, and creates
one mixed path, irrespective of how the old cycles are rearranged.

Pairwise disjoint supports have disjoint vertex sets. Their removed and
inserted edges cannot compete, so all toggles can be performed at once.
No edge outside their supports changes. Adding the preceding conclusion
over supports proves assertions 1--3. Equal numbers of the two signs
were covered; no artificial free PP ends remain, so no cut debt occurs.

The originally paid alphas lie outside these supports. Their components,
labels and original access certificates are unchanged. The additional
dependency assumption in assertion 4 ensures their existing payments
remain admissible. Those payments consume f distinct original interval
units. Each support consumes a different original beta and uses no
interval unit. Since f<=|I| and r<=b, the displayed identity proves the
inequality. QED.

## Why vertex disjointness is insufficient

Take six endpoints t1,t2,t3,t4,p1,p2. Let A be empty and let M consist of

    t1--t2, t3--t4, p1--p2.

All t endpoints are TP; both p endpoints are BP. There are two alphas
and one beta. The one-edge augmenting paths t1--p1 and t3--p2 are vertex
disjoint and their simultaneous toggle is a valid matching. Nevertheless,
they spend the two ends of the same original beta. The result is the
single alpha path

    t2--t1--p1--p2--t3--t4.

Thus alpha decreases from two to one, rather than to zero, and beta
decreases from one to zero. The signed deficit stays one. Counting both
augmenting paths as separate paid demands would reuse one beta credit.
This refutes that candidate counting rule, not the target grid inequality.
It is an abstract accounting example, with no grid embedding claimed.

## Application and scope

The reflected all-length family in ZERO_CAPACITY_GAP_BETA_COMPENSATION.md
has the required single-support path. Its support consists of the central
alpha, the original left beta and the boundary two-edge PP cycle. The
two-delete/three-add replacement is exactly a toggle along that path.
Consequently it is an instance of this theorem for r=1, not an accidental
numerical cancellation. Collections whose original component supports
are disjoint satisfy the simultaneous conclusion as well.

The accompanying checker enumerates abstract matchings, signs and simple
augmenting paths on at most eight endpoints, checks qualifying paths and
pairs with disjoint supports, reconstructs the explicit false-payment
example, and checks the support condition in 96 reflected physical
controls. These finite checks test the written general proof; they do not
establish geometric existence. This extension is not part of the earlier
Oracle submissions or the nine Lean trace theorems. The universal grid
budget, universal improvement of 5/6 and rectangular-grid triple equality
remain open. The global outside-overlap correction, when applicable,
still has to be retained once; this packet theorem does not remove it.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
