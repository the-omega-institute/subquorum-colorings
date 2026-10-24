# A complete four-source obstruction to pointwise source-cut payment

20 October 2026. The proposed unrestricted source-cut inequality

    minimum restored-support omissions <= A+U0+Z0+H

is false. A complete feasible four-source fusion has right side6 and exact
minimum omission count7. Its allocation margin is mu=3 and its aligned ambient
slack is70. Thus this is an obstruction to that transfer rule, with positive
margins for both targets. It is not a counterexample to either target.

The construction was supplied by the completed full-target Oracle research
task2395afc0; the concrete witness and its exact omission certificate were
then independently reconstructed with the repository's original constructors.

## The source cut and its exact obstruction

In any complete feasible fusion let P be all original endpoints and let
T=(union_i T_i) minus P be the mandatory selected set. Retain a subset I of
complete original owners, with endpoint set P_I and original supports U_I.
The mandatory set after deletion would be

    T_I = U_I minus P_I = V_I disjoint-union W_I,
    V_I = U_I minus P,
    W_I = U_I intersect (P minus P_I).

Every V_I point retains its original endpoint anchor. The full occupied set
after deletion is a subset of P union T, so these selections remain feasible.
A V_I point cannot be adjacent to W_I: before deletion the latter was already
an endpoint, and the former already had its own retained original anchor.
Each restored point in W_I has at least one persistent endpoint anchor.
Consequently the cut is feasible exactly when every restored point has one
persistent endpoint neighbor and there are no edges within W_I.

Let W2 consist of restored points with at least two persistent endpoint
neighbors, and W1=W_I minus W2. Every point of W2 must be omitted in any
relaxed repair that keeps P_I. All remaining selected-selected conflicts are
exactly the edges induced by W1. Hence the exact minimum omission count is

    kappa(I) = |W2| + minimum-vertex-cover-size(grid[W1]).

This elementary characterization does not legalize any omission: the complete
source model requires every original support outside the retained endpoints.
It only measures failure of the cut. No matching theorem is needed for the
concrete certificate below, since grid[W1] has exactly one edge.

## Exact complete-source manifest

Use the fixed physical partition {2i,2i+1} times {2j,2j+1}. The canonical
U(w,l,h) has endpoints in its two-row bar, columns1 through w, and its two
complete stems at columns1,w through respective even heights l,h. Every
support and every matching edge is taken unchanged from the original
constructor used elsewhere in this repository.

| Owner | Canonical source | Map (r,c) | Original phase |
|---|---|---|---|
| V1 | U(8,14,12) | (r-12,c-1) | 01 |
| V2 | U(6,6,4) | (c+1,7-r) | 01 |
| V3 | U(18,8,4) | (2-c,9-r) | 01 |
| V4 | U(6,10,10) | (-r,c) | 10 |

These have pairwise disjoint endpoints,136 in total, and their unchanged
matching has68 edges. After removing consumed supports there are30 selected
points. Every selected point has exactly one neighbor in the FULL occupied
set P union T, and every endpoint has at least three occupied neighbors.
The checker verifies each of these conditions directly, using all complete
sources rather than a partial contact diagram.

The exhaustive endpoint-bearing physical tile census is

| Actual profile | Number |
|---|---|
| 4P0T | 30 |
| 2P1T | 5 |
| 2P0T | 2 |
| 1P1T | 2 |

Both2P0T tiles are exact original irregular V4 bar pairs, and both1P1T
tiles are original singleton profiles. There are no original positive
terminal1P2T profiles, U11 triple profiles, or rotors. The established reserve
identity therefore gives A=U0=Z0=0 and H=2+2*2=6, so R=3.

## Seven unavoidable omissions, and an attaining relaxed repair

Keep exactly V3,V4. Their restored support set has19 points. Six are

    (0,7), (-2,7), (-4,7), (-6,7), (-8,7), (-10,7).

Every one has persistent neighbors in BOTH columns6 and8. The point(0,7)
also has persistent neighbor(1,7). All six therefore must be omitted in any
relaxed repair. Count(0,7) once, despite its three anchors.

Among all other restored points the only induced edge is

    (0,0) -- (1,0).

The first has persistent anchor(0,1) in V4 and the second anchor(1,1) in V3.
Thus at least one of these two selections must also be omitted. They are
different from the six forced omissions, proving kappa>=7. Conversely, omit
those six and(0,0). Every remaining mandatory support has exactly one occupied
neighbor. This explicit attaining repair proves kappa=7, with no exhaustive
optimization assumption. In the actual model the repair is forbidden.

The restored-support total degree excess is9. It is a different statistic
and is not substituted for the exact omission count7.

## Scope and consequence

All original sources are negative: their charges are -1,-1,-1,-5. There
are no positive sources or marked positive sides, so N=G=0 and mu=R=3.
The aligned28-by12 rectangle with rows[-18,9], columns[-2,9] contains all
endpoints and original supports. Its slack is168-68-30=70.

Deleting owners V1,V2 splits an endpoint component and restores supports
along full occupied bands. Whole endpoint-component restriction is unaffected.
The neutral contact between(2,0) in V1 and(2,1) in V2 is an open01 path;
its forced continuation(1,1) belongs to V3. This is not a closed-cycle
counterexample, and supplies no critical-U10/AA realization.

A general induction must therefore preserve the deleted owners' occupied
boundary bands in its state, or prove a demand-dependent cut theorem that
excludes this configuration. The latter possibility remains open, because
this example has no positive demand. Counting external original owners does
not by itself pay for restored supports or create fresh reserve.

## Verification

Run `python3 develop/check_source_cut_boundary_obstruction.py`. Besides the
concrete certificate,24 complete parameter controls use the corresponding
two-parameter manifests. Those finite checks are discovery and verification
evidence, not a proof of an unrestricted parametric assertion. The concrete
counterexample and exact7-versus6 obstruction require only the finite witness
and the general elementary cut criterion proved above. No Lean claim is made
for this new geometric witness.
