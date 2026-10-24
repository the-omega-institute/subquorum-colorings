# Bounded-height sharp entry chains and unbounded freezing depth

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. Two all-length conclusions

The connected sharpness construction can be embedded in a strip of height10.
For every positive k it gives a feasible exchange-terminal pair on a
10-by-(6k+2) rectangular grid with

    |P|=16k, |T|=8k+2, |M|=8k, f=k, j=2k,

one endpoint component, exactly2^kperfect matchings, and occupied degree
three at every forced-block endpoint. In particular sharpness of2f<=j
persists in a fixed-height strip with arbitrarily many flexible blocks.

For the matching using the horizontal square choice in every core, the
standard synchronous freezing process takes EXACTLY3k+3rounds. Round0 has
no frozen endpoints; a round freezes every endpoint with at least two
neighbors in T union m(E) from the preceding round. Thus exchange terminality
does not imply a uniform bound on this process's depth, even in height10
and even when the two-entry bound is sharp. This concerns this precise
freezing process; it does not rule out other certificates or proof methods.

## 2. Coordinates, interfaces and all matching choices

Use the16endpoint core and10support sites listed in
CONNECTED_SHARP_ENTRY_CHAINS.md. Write its sites in the following fixed order:

    0:(1,1), 1:(1,2), 2:(1,3), 3:(1,4), 4:(1,5), 5:(1,6),
    6:(2,2), 7:(2,3), 8:(2,4), 9:(2,5), 10:(3,2), 11:(3,3),
    12:(3,5), 13:(4,1), 14:(4,2), 15:(4,3).

The support sites are exactly

    (0,1),(0,3),(0,6),(1,0),(1,7),(3,6),(4,0),(4,5),(5,1),(5,3).

For copy i,0<=i<k, use the map

    phi_i(r,c)=(4+r,c+6i) if i is even,
                (6-r,c+6i) if i is odd.

Retain the union of old support sites minus the union P of endpoints.
The footprint rows are4through9 for even copies and1through6 for odd
copies, and columns6i through6i+7. Hence all sites lie on the stated board.
Nonconsecutive copies have no occupied adjacency. In each consecutive pair
there is exactly one endpoint contact: site5 of copy i to site0 of copy i+1,
at physical coordinates (5,6i+6)--(5,6i+7). Each was the other's selected
support before fusion. These are the only consumed selections.

For a complete interface check it suffices to subtract(4,6i) for even i.
The next copy map becomes (r,c)->(2-r,c+6). The occupied intersections are

    old T intersect next P={(1,7)}, old P intersect next T={(1,6)},
    old P intersect next P=old T intersect next T=empty.

The complete directed old-to-next occupied adjacency list is

    (0,6)--(1,6), (1,5)--(1,6), (1,6)--(1,7),
    (1,7)--(2,7), (1,7)--(1,6), (1,7)--(1,8).

The odd-to-even interface is its reflection. As in the preceding chain
proof, no native endpoint or retained selection acquires a new occupied
neighbor; only consumed selections acquire extra neighbors and become
the neighboring copy's endpoints. This proves feasibility and preserves
the core occupied degrees. There are16k endpoints and8k+2 selections.

Every interface is an endpoint bridge with an even number of vertices on
either side, so no perfect matching uses it. The six forced pairs and the
two square choices in each core therefore classify ALL perfect matchings.
This proves the matching count, block count and degree assertions.

Here is a freezing proof for arbitrary square choices. If the left support
(1,0) of a core is persistent, while the right support(1,7) is unavailable,
the following prefix freezes site4, the mate of its right port site5:

    horizontal choice: site0,site12,site2,site4;
    vertical choice:   site0,site12,site2,site6,site8,site4.

The witnesses are the corresponding rows of the previous note's prefix:
site0 uses(0,1),(1,0); site12 uses(3,6),(4,5); site2 uses(0,3),(1,2).
In H,site4 uses(1,4),(2,5). In V,site6 uses(1,2),(2,3),site8 uses
(2,3),(2,5), and site4 uses(1,4),(2,5). All non-support witnesses are
mates of preceding listed endpoints. This prefix never uses the lower-left
support(4,0), which is in fact retained, or the unavailable right support.

Copy0 has a retained left support. Once its prefix freezes site4, the
endpoint at its right port site5 is persistent. That site is the next copy's
left support. Induction from left to right therefore runs a valid prefix in
every copy. The last copy also has its retained right support, so both of
its port supports are persistent; its original full16row certificate finishes
the copy. Its site1 is now frozen, so its left endpoint site0 is persistent,
giving the preceding copy its right support. Induction back from right to
left finishes every copy. Every matching choice is exchange-terminal.

The exact board margin is30k+10-(16k+2)=14k+8>0. The construction is not a
counterexample to the grid bound and no positive-demand sharpness is claimed.

## 3. Exact synchronous freezing times for all-horizontal choices

Fix this matching and put n=k-1-i. We claim the following are the first
rounds tau_i(e) at which the endpoints freeze. Treat the entries as candidate
times until the simultaneous round induction below proves exactness:

| Site e | tau_i(e) |
|---|---|
| 0 | 3i+1 |
| 1 | 3n+6 |
| 2 | 3i+2 |
| 3 | 3n+5 |
| 4 | 3i+3 |
| 5 | 1 if n=0; otherwise3n+4 |
| 6 | 3i+4 |
| 7 | 4 |
| 8 | 3i+3 |
| 9 | 3n+5 |
| 10 | 3 |
| 11 | 3i+5 |
| 12 | 1 |
| 13 | 1 |
| 14 | 3i+6 |
| 15 | 2 |

Here is a proof of exactness, rather than a finite-range extrapolation.
The horizontal matching partner list for sites0through15 is

    1,0,3,2,5,4,10,8,7,12,6,15,9,14,13,11.

A selected neighbor persists at round0; an endpoint neighbor y persists
when its mate freezes. The mate of x itself persists only after x freezes
and cannot trigger x's first freezing. At a degree-three endpoint x both
other occupied neighbors are required, so its time is one plus the maximum
of their persistence times. At a degree-four endpoint the second-smallest
of the other three times is required. Only sites2 and7 have degree four.

The left port support has candidate persistence time3i: zero at i=0, and otherwise
the time of site4 in copy i-1. The right port support has persistence time
R=0 at n=0 and otherwise R=3n+3, the time of site1 in copy i+1. Suppressing
the copy subscript, the exact threshold recurrences are

    tau(0)=1+3i,                       tau(1)=1+max(tau(3),tau(10)),
    tau(2)=1+min(tau(0),tau(8)),        tau(3)=1+max(tau(5),tau(7)),
    tau(4)=1+max(tau(2),tau(12)),       tau(5)=1+R,
    tau(6)=1+max(tau(0),tau(8)),        tau(7)=1+median(tau(10),tau(3),tau(15)),
    tau(8)=1+max(tau(2),tau(12)),       tau(9)=1+max(tau(5),tau(7)),
    tau(10)=1+max(tau(15),tau(13)),     tau(11)=1+max(tau(8),tau(6)),
    tau(12)=1, tau(13)=1,              tau(14)=1+max(tau(6),tau(11)),
    tau(15)=1+tau(13).

For site2 the selected support has time0, leaving the minimum of the other
two witnesses. For site7 all three nonmate neighbors are endpoints, giving
the displayed median. The other equations follow directly from the site
coordinates and partner list. Substitution of the table verifies every
equation for arbitrary i,n>=0, including n=0 and both boundary relays.

To justify that these equations determine the FIRST times even in the
presence of dependency cycles, induct on the synchronous round t. At t=0
no endpoint is frozen and every displayed time is positive. Assume the
frozen endpoints after t rounds are exactly those with displayed time at
most t. An endpoint not already frozen has its mate still unavailable.
Its other neighbors' availability is given by the induction hypothesis and
the retained selections. The threshold recurrence says it freezes at the
next round exactly when its displayed time is at most t+1. Already frozen
endpoints remain frozen. This completes the induction and proves exactness.

All displayed times are at most3k+3. Site14 of the last copy and site1 of
the first copy both attain3k+3. Therefore the entire process takes exactly
that many rounds for every positive k. Its depth is unbounded despite fixed
height, connectedness, exchange terminality and the sharp degree-four count.

## 4. Verification boundaries

The written all-k geometry, even-cut matching classification and threshold
induction are the general proofs. Finite controls check both interface
orientations, every matching for small k, arbitrary mixed choices in larger
chains, and every individual freezing time against an independently iterated
synchronous process. Lean checks the all-i,n recurrence arithmetic and its
relay/bound/attainment consequences, separately from the generic rank
certificate and finite core tables in ConnectedSharpEntryChains.lean.
Formalizing the physical all-k embedding and matching classification remains
outside that Lean scope. No change is made to the submitted manuscript.

The verifier passes371models,254independent matching classifications,
33280individual all-horizontal time checks across k=1through64 and26264
entry-time checks under mixed matching choices. It covers every choice
string through k=7 and twelve patterns at k=8,16,32,64,128. The8Lean
arithmetic theorems and all individual axiom audits pass locally.

Independent Oracle taskba6d6a73-e349-465f-995c-14c22132c0d9 accepts the complete
written height10construction, all-choice terminality, individual horizontal
times and simultaneous-round exactness argument, actualgpt_6/pro. It does
not execute code or Lean. Its candidate-time wording clarification is applied;
no mathematical correction is required. The full review is archived in
output/bounded-height-sharp-review-accepted.json.

The further result MATCHING_INDEPENDENT_FREEZING_DEPTH.md proves that EVERY
replacement matching still requires at least3k rounds, closing the possibility
of avoiding unbounded depth by changing the square matchings. Its separate
6theorem Lean check and independent review have their own recorded scopes.
