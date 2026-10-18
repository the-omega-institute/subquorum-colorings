# Pulling back minimal forming sets through covers

19 October 2026. The covering lemma below is a general proof. The final
two-sheeted Heawood computations are discovery controls and do not prove
a bound for arbitrary connected cubic graphs or arbitrary covering degree.

## Covering pullback theorem

Let pi:V(H)->V(G) be a graph covering of finite simple graphs: it maps
edges to edges, and for each vertex h the induced map
N_H(h)->N_G(pi(h)) is a bijection. Suppose G is triangle-free.
If S is an inclusion-minimal two-star-forming set in G, then

    S_tilde=pi^(-1)(S)

is an inclusion-minimal two-star-forming set in H. If every fiber has
size k, then SF_2(H)>=k SF_2(G).

Here an outside vertex is covered when it has two selected neighbors,
or a selected neighbor with a selected neighbor. Local bijectivity
preserves each selected-neighbor count under full pullback, including
the selected-neighbor counts at its neighbors. Thus formation pulls back.
It remains to prove minimality; formation alone would not suffice.

Fix a selected lift v_tilde of v in S. There are four exhaustive cases.

1. If v is selected-isolated, so is v_tilde. Deleting it makes that
   vertex outside with no selected neighbor, hence uncovered.
2. If v belongs to a selected K2 component, v_tilde has one selected
   neighbor, which also has selected degree one. After deleting v_tilde,
   that sole remaining selected neighbor is isolated, and v_tilde fails.
3. If v is a selected leaf whose support has selected degree at least
   two, minimality provides an adjacent outside failure witness x with
   selected neighborhood {v} or {v,i}, where i is selected-isolated.
   The leaf itself survives deletion through its support. An old outside
   nonneighbor cannot fail, since any destroyed star at that support
   can replace v by another selected neighbor. The adjacent witness
   classification then gives the two stated neighborhoods. Lift x to
   the unique neighbor x_tilde of v_tilde over x. After deleting v_tilde,
   x_tilde has no selected neighbor or only a selected-isolated lift
   of i. Thus x_tilde fails.
4. If v has at least two selected neighbors, deleting it leaves v
   covered. Some old outside x must fail. If x is adjacent to v, its
   selected neighborhood is {v} or {v,i}, with i selected-isolated.
   Indeed a third selected neighbor would preserve a centered star;
   the other selected neighbor must have no neighbor after deletion.
   If it previously had v as its unique selected neighbor, the edges
   through x would give a triangle. Triangle-freeness excludes that
   alternative. The unique lift adjacent to v_tilde now fails exactly
   as in case3. If x is nonadjacent to v, it has a unique selected
   neighbor u whose unique selected neighbor is v. Lift the path
   v--u--x starting at v_tilde, obtaining u_tilde,x_tilde. Their full
   pullback selected neighborhoods are {v_tilde} and {u_tilde},
   respectively. Deleting v_tilde leaves u_tilde isolated and x_tilde
   with that sole selected neighbor, so x_tilde fails.

Every selected single deletion fails. Formation is upward closed,
so this proves inclusion-minimality. Apply the result to a largest
minimal S and count its fibers to obtain the SF inequality. The theorem
asserts triangle-freeness as a sufficient hypothesis, not as a necessary
condition for every cover to preserve minimality.

The proof does not assert that dissociation optima pull back: preimages
of a dissociation set do give the lower bound beta_2(H)>=k beta_2(G),
but new dissociation sets can be larger. That additional gain is exactly
the issue in attempting to amplify a sharp SF-beta gap by connected covers.

## Why a triangle-containing base can fail

The triangle-free assumption cannot simply be dropped from the theorem.
Take the seven-vertex base with vertices v,u,t,i,x,y,z (labels0through6)
and edges

    vu, vt, vx, ux, uy, iy, tz, iz.

Let S={v,u,t,i}. Its outside vertices x,y,z each have two selected
neighbors, so it forms. Deleting v,u,t,i respectively uncovers x,y,z,i:
after deleting v the sole selected neighbor of x is the now-isolated u;
after deleting u or t, the corresponding y or z has only the isolate i;
deleting i leaves itself uncovered. Upward closure proves minimality.

Construct a two-sheeted cover with every edge preserving sheets except
vx, which crosses sheets. Write subscripts0,1for sheet labels. The full
pullback has eight vertices. Delete v_0. It still forms: v_0 has two
selected neighbors u_0,t_0; x_0 has v_1,u_0; x_1 has only u_1, but u_1
has the selected neighbor v_1. Both y copies retain u,i and both z
copies retain t,i. These are all outside vertices after the deletion.
Thus the full pullback is not minimal. The base triangle v-u-x is
precisely what lets the surviving lift u_1 keep support from v_1.

This is a counterexample to the unrestricted pullback rule. It does not
refute the triangle-free theorem or any asserted SF inequality for these
two particular graphs. The explicit argument above proves the obstruction;
`scripts/check_cover_triangle_obstacle.py` additionally checks all proper
base subsets, local bijectivity and literal non-induced-star witnesses.

## Consequence for two-sheeted Heawood covers

The Heawood graph has a minimal forming eight-set. Every two-sheeted
cover therefore has a minimal forming16-set by the theorem. It is cubic
on28vertices, so the universal degree-capacity bound gives

    SF_2<=floor(3*28/5)=16.

Thus SF_2=16 in every such cover, without any enumeration and without
assuming connectedness. Two disjoint base copies have beta_2=14.
For connected covers the dissociation gain must be assessed separately.

## Exact one-part formula used for discovery

For a bipartite graph with parts L,R and A subset L, define

    Z(A)={x in R:N(x) intersect A is empty},
    P(A)={a in A:some x in R has N(x) intersect A={a}}.

Then the exact identity is

    beta_2(G)=max_(A subset L)(|A|+|Z(A)|+|P(A)|).           (1)

For a fixed chosen left part A, a chosen right vertex has zero or one
neighbor in A. All zero-neighbor vertices can be taken. The one-neighbor
vertices split into groups according to their unique A neighbor, and
at most one can be taken from each group. Taking one from every nonempty
group is feasible because the groups have distinct selected neighbors
and R is independent. The optimum for this A is exactly the displayed
sum. Maximizing over A proves(1). This supplies a direct exact algorithm
using2^|L|subsets; no novelty claim is made for this standard selection
argument. It also returns a literal attaining dissociation set.

## Two-sheeted discovery controls and their limits

Choose a13-edge spanning tree in the21-edge Heawood graph. Switching
the two sheet labels at individual base vertices makes every tree-edge
sign zero. The remaining eight cotree edges give256 normalized binary
signatures. The zero signature is the disjoint cover; every nonzero
signature connects the sheets through a cotree edge and the lifted tree.

The discovery script checks255nonzero signatures, each of order28. It
checks the pulled-back16-set and all vertex-deletion connectivity tests.
The exact one-part formula gives beta_2=15 in143controls and beta_2=16
in112controls. These controls therefore have displayed gaps one or zero,
with no beta_2=14 example found. This is finite search evidence about
this proposed construction route, not a proof for arbitrary-order covers,
nor a proof of the optimal connected cubic asymptotic gap coefficient.

The first20optima agree with independent MILP controls. The21st MILP
hit its30-second limit; this is not evidence of a mathematical failure.
Its original prefix is archived separately, and the exact one-part
algorithm completed all255controls without that optimization dependency.
The written formula(1) justifies the exact computation, while the general
covering pullback and SF identity above have separate non-enumerative proofs.

Reproduce with `python3 scripts/explore_heawood_two_lifts.py --output output/heawood-two-lift-exploration.json`.
The generic pullback controls use `scripts/check_cover_pullback.py`:
579 triangle-free bases,1,737 covers,9,408 pulled-back minimal sets
and71,004 literal deletion tests pass, including odd cycles and the
Petersen graph. The one-part formula also agrees with independent full
subset optima on576small bipartite graphs. These controls do not replace
the general covering and one-part arguments above.
This covering theorem and exploration were derived after the regular
compensation and connected-ring Oracle inputs and are outside those reviews.
