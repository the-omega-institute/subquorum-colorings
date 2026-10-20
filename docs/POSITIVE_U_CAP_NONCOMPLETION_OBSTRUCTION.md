# A positive U cap that admits no complete source extension

20 October 2026. An apparent way to stop the forbidden rotor extension
is to let a positive U source own its next forced support. We prove that
the specific cap below cannot occur in ANY feasible complete U/rotor
extension, even when further U sources have arbitrary permitted widths,
independent leg heights, phases and isometries. The obstruction is a
forced rotor followed by a closed two-site cavity. It rules out this
candidate cap, not every U cap and not the target grid inequality.

## 1. Exact partial seed and statement

Use the complete rotor coordinates and Rplus/Rminus normalization in
ROTOR_ONLY_RESERVE_AND_RECTANGULAR_COMPONENTS.md. Put in the partial seed

    Rplus(0,0), Rplus(-3,0), Rplus(-1,-3),
    U(6,4,4)+(-4,-6).                                (1)

The complete reference U(w,a,b) has endpoints

    ({0,1} x {1,...,w}) union ({2,...,a} x {1})
      union ({2,...,b} x {w}),

and all original supports of the established constructor. The U in(1)
is positive phase00. Its right terminal endpoint is(0,0), the support
whose unique rotor owner would continue the Type A chain. The42 original
endpoints of these four sources are disjoint. They retain their original
matching edges. The seed is a PARTIAL source collection; no feasibility
of that partial collection is assumed or claimed.

**Noncompletion theorem.** There is no complete feasible extension of(1)
by further complete rotors and U(w,a,b) sources, with even w>=6 and
independent even a,b>=4, in any phase, chirality or lattice isometry.
As always, original endpoint sets must remain disjoint, P and M are their
original unions, and all original supports outside P are retained.
Permitted optional selections cannot remove an old support or endpoint
and do not evade the argument. Arbitrary translations/isometries of the
whole seed satisfy the same conclusion.

## 2. A four-site barrier excludes every possible U owner

We first prove a local fact valid for ALL permitted U parameters.
Every endpoint p of a complete U satisfies at least one of these three
endpoint-only properties:

1. It has at least three original endpoint neighbors.
2. It has two opposite original endpoint neighbors.
3. One cardinal ray p+d,p+2d,p+3d,p+4d consists of original endpoints.

Here is the complete geometric classification. An interior point in
either bar row has at least three endpoint neighbors. A lower bar corner
also has three, because its stem continues. Each upper bar corner has a
straight endpoint ray along the bar of length w-1>=5, so it has property3.
A nonterminal stem endpoint has two opposite endpoint neighbors. A terminal
tip has a straight ray back up its stem and into the bar, of length at
least a or b, each>=4. This covers every U endpoint and is invariant
under every lattice isometry. No sample of widths is used in this proof.

Consequently no U source can own p when four foreign original endpoints
occupy, relative to p,

    right=(0,1), down=(1,0), two-up=(-2,0), four-left=(0,-4). (2)

Its own endpoints may not overlap any of these sites. Property1 is
impossible since only up and left remain available adjacent positions.
Property2 is impossible since each opposite pair includes down or right.
For property3, down/right rays already collide at their first point;
an upward ray collides at its second point and a leftward ray at its
fourth point. Thus all three possibilities fail. This is an all-parameter
U exclusion, stronger than checking a finite source library.

## 3. The next source is forced to be a particular rotor

In seed(1), p=(-1,-1) is an original selection, in fact with the two
persistent endpoint neighbors

    (-1,0), (0,-1).

If p were not in final P, complete retention would keep it selected
with two occupied neighbors. Therefore it must be a foreign original
endpoint. The four blocking sites for(2) are

    (-1,0), (0,-1), (-3,-1), (-1,-5),

all already endpoints of seed(1). Section2 rules out ANY U owner.

There remain the two rotor chiralities, eight possible original endpoint
roles each. Matching p to a role determines its translation exactly.
Removing candidates whose original endpoints overlap the seed leaves
precisely

    Rplus(-3,-5).                                    (3)

This exact16-role classification is over all integer translations.
Additional sources can only remove candidates, not add a seventeenth
role. Hence every purported feasible extension contains(3).

## 4. A closed cavity excludes every further source

After adjoining the forced rotor(3), the original endpoint union has50
sites, still disjoint. Its old selection q=(-2,-4) has persistent endpoint
neighbors(-3,-4) and(-2,-3), so q must also become a foreign endpoint.

But q belongs to the two-site set

    H={(-2,-4),(-1,-4)}.

Neither site is an endpoint of the five known sources. Every lattice
neighbor of H outside H is one of

    (-3,-4), (-2,-5), (-2,-3),
    (-1,-5), (-1,-3), (0,-4),

and all six are already original endpoints of those known sources.
Thus H is a closed component of the lattice after those endpoints are
removed. This is a local separating barrier; no ambient search box is
involved.

The original endpoint set of any permitted new source is connected.
If it contained q and an endpoint outside H, a path in that source's
own endpoint set would have a first step leaving H. That step meets one
of the six known foreign endpoints, contradicting original endpoint
disjointness. Therefore its whole endpoint set would have to lie in H.
Every rotor has8 original endpoints and every U has

    2w+a+b-2 >=18.

Neither fits in a two-site set. There is no possible owner of q, which
contradicts complete retained-support feasibility and proves the theorem.
The original matching is never changed and no old support is discarded.

## 5. Evidence and limits

The exact fixed seed, four blocking sites,16 rotor roles, forced rotor,
second support and six-site closed boundary are independently checked by
develop/check_positive_u_cap_obstruction.py.
Its27 dimension controls and216 isometry controls verify the endpoint
certificate on representative U sources; the arbitrary-size certificate
has the direct role proof of Section2. These finite controls do not prove
its parameter quantification.

Lean checks the fixed geometry, rotor role list, three-neighbor/opposite/
ray blocking catalogue, closed cavity and generic path-trapping induction.
In addition, every_u_endpoint_hits_stencil universally quantifies over
all integer widths>=6, independent heights>=4, every endpoint and all eight
signed coordinate permutations: one of the four inverse-transformed
blocking offsets is an original U endpoint. This proves the arbitrary-size
stencil exclusion directly in Lean. The source connectedness/cardinality
adapter, coordinate-isometry ownership adapter and assembly into the
noncompletion theorem remain written.
Thirteen declarations and individual axiom audits pass locally with
Lean4.33.0, one job and61% free memory at the audit preflight. No sorryAx/native_decide
is used. See output/positive-U-cap-obstruction-formal-check.json and
output/positive-U-cap-obstruction-controls.json. This is not a full Lean
formalization of arbitrary U/rotor extensions.

A preceding SAT check found UNSAT in a24x24 window, with at most32sources
from a fixed U(6,4,4)/rotor library. That search alone excluded only its
finite window/library/count. Sections2-4 give an independent general proof
that removes all of those cutoffs. It does not infer a theorem from UNSAT.

The result rules out the PARTICULAR positive cap proposed for Type A.
It does not show that no larger, differently oriented or differently
placed U can terminate a rotor extension. It gives no counterexample to
joint allocation or coefficient one: no feasible extension of this seed
exists at all. The remaining mixed-source research must find a different
complete cap or prove that all such caps pay the joint budget.

This new obstruction is outside the completed rotor-only review scope.
No prior ACCEPT covers its additional U argument. No manuscript, email,
draft or shared CI change is part of the result.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
