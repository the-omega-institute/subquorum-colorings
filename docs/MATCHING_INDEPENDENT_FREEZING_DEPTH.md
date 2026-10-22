# Rematching cannot bound freezing depth in the height-ten sharp chains

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. Conclusion

In the height10family of BOUNDED_HEIGHT_SHARP_ENTRY_CHAINS.md, EVERY perfect
matching requires at least3k synchronous freezing rounds. Thus unbounded
freezing depth persists after optimizing over all2^k independent choices
of the flexible square matchings. This strengthens the exact3k+3all-horizontal
calculation: a slow prescribed matching is not the only obstruction.

This is an obstruction to a uniform-depth use of this particular freezing
process. It is not a failure of exchange terminality, a prohibition on other
certificates, or a counterexample to compensation/the half-area inequality.

## 2. Four exact entry times under arbitrary matching choices

Use the site numbering in the bounded-height note. Let the matching choice
in copy i be epsilon_i=0 for horizontal and1 for vertical. All times below
are finite because the earlier two-wave argument supplies a complete finite
retained-neighbor certificate for every matching. Induction along that
certificate shows that the synchronous process eventually freezes every
endpoint: once the preceding endpoints have frozen, both certified witnesses
persist and the current endpoint freezes at the following round at the latest.
Write u_i,a_i,d_i,v_i for the FIRST freezing times of
sites0,2,8,4 respectively. Site12 freezes at round1 in every copy and every
matching: both its nonmate occupied neighbors are retained selections.

The interface rule gives

    u_0=1, u_i=1+v_(i-1) for i>0.                  (1)

Indeed, site0 has one retained selected neighbor and its left port support.
At i=0 that support is selected. Otherwise it is site5 of the preceding
copy, whose mate is site4. No other neighbor can trigger its first freezing:
its native matching mate becomes persistent only after site0 itself freezes.

Site2 has degree four and one selected neighbor. Under H its other nonmate
endpoint neighbors are mates of sites0 and8; under V they are also mates
of sites0 and8, with the latter witness now at site3 instead of site7.
Site8 has degree three and its two nonmate neighbors are mates of sites2
and12 under either choice. Therefore

    a_i=1+min(u_i,d_i), d_i=1+max(a_i,1).           (2)

As a_i>=1, the second equation says d_i=a_i+1. If the minimum in the first
equation were d_i, it would give a_i=d_i+1, impossible. Hence

    a_i=u_i+1, d_i=u_i+2.                          (3)

For site4 the two nonmate neighbors are mates of sites2 and12 under H,
and sites8 and12 under V. Consequently

    v_i=u_i+2+epsilon_i.                           (4)

Combining(1)and(4), with no enumeration of choice strings, yields

    u_i=3i+1+sum_(0<=h<i)epsilon_h,
    a_i=u_i+1, d_i=u_i+2.                          (5)

The sum counts vertical choices BEFORE copy i, so the last copy's own
choice does not enter its arrival time. These are exact first times,
derived from the threshold rule and finite terminality, not merely
timestamps of a chosen sequential proof certificate.

## 3. The all-matching lower bound

For i=k-1, equation(5) gives

    d_(k-1)=3k+sum_(0<=h<k-1)epsilon_h >=3k.

Thus no perfect matching finishes before round3k. In particular for every
fixed round budget R, choosing k with3k>R defeats that budget regardless of
which allowed-edge replacement matching is selected. The height remains10,
the full endpoint graph remains connected, and2f=j=2k remains sharp.

The exact optimum number of rounds over matchings is not needed or asserted
here. The earlier all-horizontal choice still gives the upper bound3k+3
for that optimum. Therefore even the best replacement matching has depth
between3k and3k+3 for every k.

Lean checks the arbitrary-parameter local cycle resolution, both square
transmission rules, the universal prefix recurrence, its exact vertical-count
formula and the3k lower bound. The physical-neighbor identification and its
adapter to actual first-round times remain the written argument above.
Finite controls compare(5) with independently iterated synchronous freezing
for all choices through k=7 and mixed larger chains. The submitted manuscript
is preserved.

Independent Oracle task7f8c892c-da88-4b3e-ac72-00cd5d66ffb3 accepts all four
exact entry times and the all-matching3kbound, actualgpt_6/pro, completed
22October09:21UTC. The clarification above makes finite synchronous
completion follow directly from the two-wave certificate. The reviewer did
not execute Python or Lean. The complete response and verification provenance
are archived in output/matching-independent-depth-review-accepted.json.
