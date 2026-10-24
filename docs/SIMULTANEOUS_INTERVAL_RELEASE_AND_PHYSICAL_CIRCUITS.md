# Simultaneous interval release: exact capacity and physical circuits

25 October 2026. Wenlin Zhang and Haobo Ma.

We give an exact criterion for original intervals to be simultaneously
unused while retaining a prescribed set of paid sources. It applies to the
complete whole-support flow, including mixed relays and beta forks. It counts
actual unused resources, rather than matching far-side witnesses to receivers.
We then identify two obstacles on the existing completely frozen 16 by 14
board: an eleven-interval minimal obstruction to simultaneous release, and
a two-interval obstruction if minimum link cost must also be retained.
These are failures of proposed reserve rules, not of the grid inequality.

## 1. Fix the sources whose payments must survive

Use the network and normalization in
[whole-support fork flow](WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md).
Choose a set P of original alpha sources that can all be paid. Retain the
source arcs of P and remove the source arcs of the other alphas. An alpha
has no incoming owner link, so it cannot be needed as an internal relay.
All mixed gates, the two actual BP entries of each beta, whole-beta sinks,
original interval sinks, links and whole-support incidences are retained.
Put p=|P|. Every flow of value p pays exactly P, not an arbitrary p sources.

For an original interval set H, *release H* means find a value-p flow that
does not use any interval in H. Delete their interval-to-sink arcs to test
this. This is a reservation of resource identities, not a change to the
physical board, matching, freezing witnesses or interval decomposition.
Let nu_H be the maximum flow after these deletions. Write c(S) for an
original s-t cut capacity and I(S) for its source-side interval identities.

## 2. Exact simultaneous release theorem

**Theorem 1.** For every candidate interval set F, the largest number of
members of F that can be simultaneously released while paying every source
in P is

    R_P(F) = |F| - p + nu_F
           = min_S [c(S)-p+|F minus I(S)|].                 (1)

In particular a specified set H is releasable if and only if

    |H intersect I(S)| <= c(S)-p   for every s-t cut S.     (2)

The optimization is over all cuts of the complete network, including cuts
through mixed gates and actual BP entries. No two-owner assumption is needed.

**Proof.** In any value-p flow, retain only the path components ending at
interval/beta sinks outside F. They form a feasible flow in the network
with F deleted, hence at most nu_F payments end outside F. At least
p-nu_F DIFFERENT intervals in F are therefore used. This proves the upper
bound |F|-p+nu_F on the number unused.

Conversely, take an integral maximum flow of value nu_F after deleting F.
Restore their sink arcs and augment to value p. Each augmenting path can
be chosen simple and stops at its first visit to t, so it never uses a
reverse sink arc. All nu_F terminal units already used remain used, even
though internal routes may change. A value-p flow cannot use more than
nu_F terminal units outside F, by the preceding path-restriction argument.
Exactly p-nu_F final terminal units thus belong to F. This attains the
upper bound. Normalizing beta outputs can only release further intervals;
it never introduces a deleted interval. The same upper bound applies to
the normalized packing, so it attains (1) as well.

Deletion changes a cut by exactly |F intersect I(S)|. Max-flow/min-cut gives
nu_F=min_S[c(S)-|F intersect I(S)|], proving the second form of (1).
The same equality for H, together with nu_H<=p, proves (2). Every original
interval identity is charged once even if multiple owners support it. QED.

This is an application of integral flow augmentation and cut duality, not a
new general flow theorem. Its role here is to give an exact reserve ledger
for the complete compensation model. One maximum-flow computation after
deleting F gives R_P(F); there is no need to enumerate subsets of F.
The theorem permits route changes and increased link cost. It preserves
all paid source identities P, but does not preserve all old used intervals.
It must not replace the earlier identity-preserving exchange theorem when
those stronger requirements are imposed.

## 3. What a minimal obstruction looks like

**Corollary 2.** A single interval j is releasable precisely when its node
lies outside the largest-source-side minimum cut. If a set H is minimally
nonreleasable, then nu_H=p-1 and there is an original cut S with

    H subset I(S),       c(S)=p+|H|-1.                     (3)

**Proof.** A single deletion reduces maximum flow by at most one. It reduces
the maximum below p precisely when a capacity-p cut contains its sink arc.
The largest source-side minimum cut contains the source side of every
minimum cut, giving the first assertion.

For minimal H, deleting H minus {h} retains value p for every h in H.
Deleting its last unit reduces value by at most one, so nu_H=p-1.
Choose a minimizing cut after deleting H. If some h in H were not in I(S),
the same cut would already have capacity p-1 after deleting H minus {h},
a contradiction. Thus H subset I(S), and its original capacity is p+|H|-1.
QED.

In particular, for two individually releasable intervals, their joint
release fails exactly when a capacity-(p+1) cut contains BOTH sink arcs.
Looking only at capacity-p cuts, or only at individual residual paths to
t, cannot detect this obstruction. For larger candidate sets, near-minimum
cuts consume several proposed reserve units together.

The previous strict beta-promotion theorem gives matched far-side
witnesses. The first part of this corollary additionally shows that each
far-side interval can actually be released individually while keeping P.
Equation (2), rather than separate individual releases, decides whether
several such operations can be combined. It supplies no free multiplication
of one available exit into several reserve units.

## 4. A minimal eleven-interval obstruction on a frozen board

Keep the existing fixture, all original selections/matching, the standard
bands, and ALL three alpha sources. The solver-free freezing and strand
traces are in
[the frozen beta fork note](FROZEN_BETA_SUPPORT_FORK_AND_RESERVED_RESOURCE_GAIN.md).
Call the alphas A,C,D, the betas B,E and the mixed owner X. The complete
nontrivial owner links are

    A -> B,   C -> B,   D -> E,   D -> X.

The two links entering B use different actual BP tips. X has no onward
link or interval support. An original within-X actual edge is ignored as
an owner self-link. Original interval supports are disjoint and have sizes

    W(A): 5,    W(C): 2,    W(B): 4,
    W(E): 5,    W(D)=W(X)=empty.

Set F=W(A) union W(C) union W(B). Its ELEVEN distinct original singleton
units have the following band/column coordinates:

| Owner | Original unit coordinates (band,column) |
| --- | --- |
| A | (1,3),(1,4),(1,5),(1,6),(2,4) |
| C | (6,3),(6,4) |
| B | (4,7),(4,8),(4,9),(4,10) |

The full board has 43 unreserved original intervals; F is not a redefinition
of that pool. The five E units and every other unit remain available.

**Proposition 3.** Every proper subset H of F can be released while paying
A,C,D. F itself cannot be released: the maximum payment then is exactly 2.
Consequently R_P(F)=10, although each of its eleven members is individually
releasable. No smaller-subset failure occurs inside F.

**Proof.** If any A unit remains, pay A there, C by its link to whole B,
and D by its link to whole E. If any C unit remains, interchange A and C.
If only B-supported units remain, use A and C's two-link fork at B, paying
one source by whole B and the other by one remaining B-supported original
unit; pay D by E. Thus ANY one surviving member of F suffices.

With all F removed, the isolated A,C,B sector has only one terminal unit,
whole B. It can pay at most one of A,C. There is no outgoing link to the
D,E,X sector. That sector has only source D and pays at most one, attained
by D->E. The two private beta payments attain the upper bound 2. QED.

The corresponding original cut has capacity 13=p+11-1. Put A,C,B bodies,
both B entry nodes, and all eleven F nodes on the source side, put D on the
sink side, and keep the rest sink-side. The crossing edges are whole B,
the eleven F sink arcs, and the source arc to D: capacity 1+11+1=13.
Deleting F leaves capacity 2. This explicit near-minimum cut verifies (3).

This is a physical obstruction to simultaneous release in the complete
whole-support model, including forks and arbitrary rerouting. It does not
claim an unpaid source in the original unrestricted board. Deleting sinks
is a resource reservation, and does not reduce the physical scalar count
of intervals in the grid inequality.

## 5. Capacity two: minimum link cost creates a smaller obstruction

Let a,c,b count the surviving members of W(A),W(C),W(B) after deleting
H subset F. The complete local optimum is

| Remaining support | Maximum payment | Minimum links at that payment |
| --- | --- | --- |
| a>0, c>0 | 3 | 1 |
| exactly one of a,c is positive | 3 | 2 |
| a=c=0, b>0 | 3 | 3 |
| a=c=b=0 | 2 | 2 |

The constructions are those in Proposition 3; in the first case both A,C
use intervals. For lower bounds, D has no support and needs at least one
link. Each of A,C without own support must use a link leaving that source.
Those are different links and cannot be supplied by D's sector. With
a=c=0 and b>0 both beta entry links are necessary. With no F resource,
paying one source in each sector requires two links. These arguments prove
the whole table without finite enumeration.

In particular the adjacent BB pocket at (band 6,columns 3,4) has two
different original unit identities. Deleting either alone preserves the
original optimum (payment 3,minimum links 1). Deleting both gives (3,2).
Thus the two units can be simultaneously unused if link cost may increase,
but cannot both be declared free in a replacement that promises no extra
links. The surviving beta resource is genuine, and the additional link
must be counted. Applying Theorem 1 as though it retained minimum link
cost would give the wrong conclusion.

For F as a whole, at most nine units can be unused at original cost 1:
one A unit and one C unit must remain used. Nine are attainable. Without
the cost restriction, ten are attainable. These are different capacities.
For ANY candidate K subset F their exact values are

    R_P(K) = min(|K|,10),
    R_at_cost_1(K) = min(|K intersect W(A)|,4)
                   + min(|K intersect W(C)|,1)
                   + |K intersect W(B)|.                  (4)

The second formula holds because a one-link full payment must spend that
link on D, leaving A and C paid by two different own-support units.
Conversely every choice retaining one unit of each own support achieves it.

## 6. Arbitrarily many physical copies

Use the existing separated vertical stack of q copies, translated by
16 rows. The original freezing certificates translate inside each copy;
the blank separators prevent links or owner-support incidences between
copies. Original interval identities in F_i are disjoint. For any
reservation H subset union F_i, let z be the number of copies whose entire
F_i was removed, a0 the number with no A unit left, and c0 the number with
no C unit left. Summing the proved local table gives the exact optimum

    maximum payment = 3q-z,
    minimum links at that payment = q+a0+c0-z.              (5)

All 3q prescribed sources survive precisely when z=0. The full candidate
pool of 11q units has simultaneous release capacity 10q, but only 9q at
the original minimum link cost q. For the 2q C-pocket units alone, all
2q can be released while paying 3q, at link cost 2q. At original cost q,
exactly q can be released. More generally, deleting both C units in s
copies and at most one in every other copy gives exact links q+s.
For a general candidate K subset union F_i, sum the two formulas in (4)
over K intersect F_i. This computes the exact simultaneous reserve for
every subset and both cost requirements, counting each physical unit once.

These are all-q proofs by geometric separation and the local lower bounds,
not extrapolations from the finite checks.

## 7. Verification and limits

The companion checker exhausts all 2048 reservations H subset F and
compares the local table with the complete flow and independent primitive
packing optimization. It verifies the actual board, complete freezing,
original unit coordinates, supports, links, both C-pocket singleton
releases, the joint cost increase, and the explicit capacity-13 cut.
Additional seeded abstract systems test (1) against all deletion subsets,
retaining a fixed paid-source set even when the initial full system is
deficient. The phase audit reselects horizontal bands after all eight
isometries and four parity offsets; it does not carry the old partition
through a quarter-turn or claim that the same owners survive.

Results: 320 fixed-paid-source abstract systems, including 205 initially
deficient systems; 3244 exact release-capacity comparisons, 786 canonical
single-release checks and 359 minimal obstructions. There are 546 independent
abstract primitive comparisons. All 2048 physical reservations pass both
optimizers: 1488 give (3,1), 544 give (3,2), 15 give (3,3), and only the full
eleven-unit deletion gives (2,2).
An independent subset dynamic program also checks both formulas (4) for
all 2048 candidate sets K against the optimized reservation outcomes.
The 112 stack controls cover q=1..16 and
seven reservation patterns, with 21 independent small-stack optimizations.
All 32 reselected-band images are fully compensated and agree with ordinary
flow. With padding, their (alpha count,minimum links) are (3,0),(0,0),
(0,0),(2,0) for the four transpose/row-phase choices. This finite phase audit
does not prove an all-phase geometric theorem.

The standalone Lean module audits the reserve upper-bound ledger, the
near-cut capacity identity and arbitrary-copy count/extra-link identities.
Integral flow augmentation, the complete flow adapter, the physical support
table and all-q geometric separation remain written proofs supported by
the cited existing fixture certificates. No full Lean proof of max-flow
or the grid conjecture is claimed.

Eight scoped Lean statements pass with no warnings or additional axioms;
the audits use only propext, Classical.choice and Quot.sound. The explicitly
selected local machine had 16 GiB physical memory, 45% free, and no active
Lean/Lake processes under the comm-basename check. Reproduce with:

```sh
python3 develop/check_simultaneous_interval_release.py --output output/simultaneous-interval-release-validation.json
python3 develop/check_simultaneous_interval_release_formal.py --lean /path/to/lean-4.33.0 --output output/simultaneous-interval-release-formal-validation.json
```

The submitted 11 October manuscript is unchanged. No universal 5/6
improvement follows. The next geometric question is whether the canonical
deficit cut forces enough joint reserve capacity across its entire
neighborhood, possibly paying an explicit additional-link cost, rather
than whether each receiver has a separately releasable witness.
