Audit the following proposed exact graph-theoretic equivalence, especially the necessity via the canonical two-sheeted counter-cover and the connectedness corollary. The safe-certificate sufficiency (with explicit definitions Forms and Minimal matching the text) has passed a full arbitrary-vertex-type Lean proof with only standard axioms. Necessity/connectedness are written, not Lean-certified. Do not substitute finite experiments for proof. Start with ACCEPT, REVISE, or REJECT. If false, give a reproducible counterexample and distinguish a rule failure from an SF-parameter inequality. Check all cases of the canonical lift carefully. No priority claim is being made.

# Exact local criterion for preservation of minimality in every graph cover

19 October 2026. All graphs below are simple and undirected, and two-stars
are non-induced. The theorem concerns a fixed inclusion-minimal forming
selection, not a numerical inequality between the maximum parameters of
two graphs. No literature-priority claim is made.

## Definitions and exact theorem

Write F(T,x) when x has two distinct neighbors in T, or a neighbor u in T
with a neighbor in T. A selection T forms if F(T,x) holds for every x
outside T. For a fixed minimal forming S and v in S, let T_v=S minus v.

A safe certificate for deleting v is either:

1. A self failure: F(T_v,v) is false.
2. An old outside vertex x for which F(T_v,x) is false and, if x is
   adjacent to v, no selected neighbor u of x is adjacent to v.

The second condition excludes a triangle x-u-v with u,v selected and x
outside, but only at this particular failure witness. It imposes no
restriction on triangles elsewhere. A nonadjacent failure is always safe.

For any finite simple graph G and minimal forming selection S, the
following statements are equivalent:

- Every graph cover pi:H->G has minimal forming full pullback pi^(-1)(S).
- Every two-sheeted graph cover has minimal forming full pullback.
- Every selected vertex has a safe certificate.

Covers are locally bijective graph maps and may be disconnected. If G
is connected and the certificate condition fails, the explicit two-sheeted
counter-cover constructed below is connected. Thus the condition is also
necessary when one tests only connected two-sheeted covers of connected G.

The sufficiency proof works for arbitrary vertex types, without finiteness,
surjectivity onto unused base components or a common fiber cardinality.
It is fully checked in Lean as
`StarForming.CoverPullback.minimal_pullback_of_safe_certificates`.
The converse and connected-counter-cover argument below are written proofs,
with independent literal-star controls; they are not yet Lean-formalized.

## Sufficiency: transport an actual deletion failure

Let pi be locally bijective. The full pullback forms: lift either the two
selected neighbors or the selected edge supporting an outside leaf. Fix
a selected lift v_tilde. We show its deletion has an uncovered vertex.

For a self certificate, suppose v_tilde were covered after deletion.
A centered star projects to two distinct selected neighbors of v,
distinct by neighborhood injectivity and different from v by simplicity.
A leaf star v_tilde-u_tilde-w_tilde also projects to a star avoiding v:
u cannot project to v by simplicity, and if w_tilde projected to v,
the two neighbors w_tilde,v_tilde of u_tilde would have the same image.
Local injectivity would force w_tilde=v_tilde, contradicting deletion.
Thus the projected star contradicts the self certificate.

For a safe adjacent failure x, lift the edge v-x from v_tilde to x_tilde.
Any surviving selected neighbor of x_tilde projecting to v would have
to equal the deleted lift by local injectivity. A leaf star at x_tilde
whose selected leaf projected to v would project to the excluded triangle
x-u-v. Therefore every star covering x_tilde after deletion would project
to a star covering x in T_v, contrary to its failure.

For a nonadjacent failure x, formation before deletion and failure after
it force a unique path x-u-v with

    N(x) intersect S={u},    N(u) intersect S={v}.

Indeed two selected neighbors of x would both survive; a covering selected
edge at its unique neighbor can only have v as its other endpoint.
Any other selected neighbor of u would also preserve coverage after deletion.
Lift v-u-x from v_tilde. The lifted selected neighborhoods are the same
singletons by local bijectivity. After deleting v_tilde, u_tilde is isolated
and x_tilde has this sole selected neighbor, so x_tilde fails.

Every selected single deletion therefore fails. Formation is upward closed,
so no proper sub-selection forms. This proves minimality. This argument
does not assign one witness to two deletions or require a global witness
injection: each single-deletion contradiction is separate.

## Necessity: a canonical two-sheeted counter-cover

Suppose a selected v has no safe certificate. Then v is covered by T_v,
and every old outside failure x is adjacent to v and participates in a
triangle x-u-v with u selected. Each such failure is necessarily of the form

    N(x) intersect S={v,u},    N(u) intersect S={v}.        (1)

To prove (1), u is different from v by simplicity. A third selected
neighbor of x would leave two after deletion. Any selected neighbor of u
other than v would leave a selected edge covering x. Both contradict failure.

Build a two-sheeted lift with vertices w_0,w_1. Cross exactly the edges
v-x with x outside S; every other edge preserves sheets. This is an ordinary
locally bijective two-sheeted cover. In particular, every selected-selected
edge preserves sheets. Let S_tilde be the full pullback, and delete v_0.

The new outside vertex v_0 is covered: lift its star in T_v within sheet0.
For every old outside x not adjacent to v, failure in T_v would be safe,
so T_v covers x. Its star avoiding v lifts within either sheet.
For an old outside neighbor x of v, consider its two lifts separately.

- At x_0, every base selected neighbor is still represented, with v_1
  in place of v_0. If x has at least two selected neighbors they still
  cover x_0. If it has only v, original formation gives a selected
  neighbor of v, and its sheet1 lift supports v_1.
- At x_1, if T_v covers x, that star lifts entirely in sheet1 and avoids
  the deleted vertex. If T_v does not cover x, (1) applies: x_1 has the
  selected neighbor u_1, and u_1 is supported by the retained v_1.

These cases cover every vertex outside S_tilde minus v_0. Consequently that
proper selection still forms, so the full pullback is not minimal.
This proves the contrapositive of necessity. The other implication, from
all covers to all two-sheeted covers, is immediate.

If G is connected, minimality and coverage of v by T_v guarantee at least
one old outside failure. Its triangle in (1) has exactly one crossed edge
in the constructed lift. Going around that triangle changes sheets, so the
two lifts of one vertex are connected. Lifting base paths then connects
both lifts of every vertex. The counter-cover is therefore connected.

## Consequences and the exact role of triangles

The previous triangle-free theorem follows at once: no adjacent failure
can contain the prohibited triangle. More generally, it is enough that no
triangle have exactly two vertices in S. This selection-dependent boundary
condition is checked in Lean as
`minimal_pullback_of_boundary_triangle_free`.

The boundary condition is sufficient but not necessary. In K3, any pair
S of vertices is minimal forming. Each selected vertex has a self failure
after deletion, so every cover preserves minimality despite the boundary
triangle. Conversely, the earlier seven-vertex example fails the exact
certificate condition only at its selected high vertex v.

There is a complete family of explicit obstructions. Take k>=2 selected
leaves u_1,...,u_k around selected v and a selected isolate i. For each j,
add an outside y_j adjacent to u_j,i. Choose a nonempty J subset {1,...,k};
for each j in J add an outside x_j adjacent to v,u_j. There are no other
edges. The selection S={v,i,u_1,...,u_k} forms. Deleting u_j uncovers y_j,
deleting i uncovers itself, and deleting v uncovers every x_j. Thus S is
minimal. At v, all outside failures are exactly the fragile triangles,
and v itself survives deletion because k>=2. Hence v has no safe certificate.
The canonical connected double cover crosses the v-x_j edges and permits
deletion of v_0 from the full pullback. The k=2, |J|=1 member is the
seven-vertex obstruction already recorded. This is a rule obstruction,
not a claim that SF_2(H)<2SF_2(G).

If every selected vertex having a selected neighbor has at least two
selected neighbors, no failure can have form (1). Every minimal selection
of this kind is therefore preserved by all covers, even when G contains
triangles. This is a written corollary of the criterion; selected isolates
are allowed. A maximum/minimum parameter calculation is not needed.

## Verification and research use

The Lean source imports only Std through RegularBound and proves the
graph theorem for arbitrary vertex types. The audit allows only propext,
Classical.choice and Quot.sound; it excludes sorryAx and compiler-trust
reduction axioms. The converse and connectedness are proved above, separately
from computational checks. Use

    python3 scripts/check_cover_pullback_formal.py --lean PATH_TO_LEAN --output output/cover-pullback-formal-check.json
    python3 scripts/check_cover_stability.py --output output/cover-stability-controls.json

The theorem identifies exactly when this particular amplification mechanism
preserves a minimal selection. It does not stop the cover's dissociation
number from increasing, so it does not settle the connected cubic asymptotic
gap or the rectangular-grid equality. For bipartite bases every selection
already has safe certificates; that removes the minimality issue and isolates
the dissociation gain as the remaining covering obstruction.
