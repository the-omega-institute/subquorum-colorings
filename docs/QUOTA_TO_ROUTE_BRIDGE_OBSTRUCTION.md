# Local slot quotas do not by themselves give route compensation

24 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The local-quota strip certificate and the mixed-owner route-flow certificate
measure different capacities. A matching between runs and residual physical
slots can be complete even when all source-to-slot routes pass through one
unit-capacity mixed owner. This note isolates that gap and gives a precise
sufficient condition under which the simpler run-slot projection is safe.

## 1. The projection that fails

Let sources be alpha owners, let mixed owners be unit-capacity gates, and let
resources be distinct beta or interval units. A source-resource edge in the
projection means that some directed source-to-resource route exists. Give each
source quota one and each resource capacity one. The resulting bipartite
matching is only a reachability test: it forgets which mixed gates the route
uses.

The smallest obstruction has two sources A and B, one mixed gate g, and two
resources R0 and R1. Both sources have a witnessed link into g, and g has a
witnessed access to both resources:

    A -> g -> R0,   A -> g -> R1,
    B -> g -> R0,   B -> g -> R1.

The run-slot projection is K_{2,2}. It has a saturating matching, so its
quota score is 2. The actual route network has one mixed split arc of capacity
one, so at most one source can be compensated:

    A(G)=2,       nu(G)=1,       delta=1.

This is a capacity obstruction, not a resource-identity collision: R0 and R1
are distinct and can be assigned to different sources in the projection. The
same mixed owner is the unit that is counted twice by the projection.

Thus a proof of `q <= A(G)` from local strip quotas cannot be substituted for
the route-flow condition `q <= nu(G)` unless it also controls mixed-owner
incidence. The obstruction is abstract and does not claim a frozen-grid
counterexample to the global inequality.

## 2. A safe source-separated bridge

The projection becomes sufficient under the following explicit hypothesis.

**Source-separated gate lemma.** Suppose every mixed owner g is reachable
from at most one alpha source in the directed route network. If the
source-resource reachability graph has a matching saturating all k sources,
then the route network has k pairwise gate-disjoint source-to-resource paths.

**Proof.** Let the matching assign resource r_s to source s. By reachability,
choose one directed source-to-r_s path for each s. If two chosen paths used
the same mixed owner g, then g would be reachable from both of their sources,
contrary to the hypothesis. Their resources are distinct by the matching,
and each source is used once. The resulting paths are therefore a legal
unit-capacity route packing. QED.

The hypothesis is stronger than necessary. It is useful because it is local,
checkable, and explains exactly what the run-slot abstraction must establish
before it can replace a mixed-owner flow calculation. A multiplicity-m version
would require that every gate be used by at most m supplied certificates; the
low-congestion theorem then supplies the correct replacement for strict source
separation.

## 3. Exhaustive small controls

The verifier enumerates all 225 labeled three-layer networks
`{A,B} -> {g0,g1} -> {R0,R1}`, with edges only between consecutive layers
and both edge layers nonempty. It compares the exact gate-disjoint route
packing with the source-resource projection. Among these 225 networks, the
projection is exact in 211 and strictly overstates route flow in 14. The
source-separated condition is checked in 120 cases, and every one of those
cases has equality.

The minimal obstruction and the separated control are checked directly, and
the exhaustive enumeration is only a finite sanity check. It does not replace
the two proofs above and does not assert that every physical band realizes one
of these abstract networks.

The result identifies the missing geometric task for occupied bands: either
prove source separation (or an m-fold low-congestion analogue) for the mixed
relays selected by the strip quota construction, or retain the full
mixed-capacity route network and prove its separator deficit is paid by a
nonduplicated exterior budget.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_quota_to_route_bridge_obstruction.py --output output/quota-to-route-bridge-obstruction.json

The recorded run passes. No universal grid route-cover theorem or 5/6
improvement follows from this note.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
