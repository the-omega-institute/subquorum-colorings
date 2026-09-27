# Parity and group-transport continuation

Date: 2026-09-27. This continues `grid-beta-uniform-2026-09-27.md`, Sections 11-13, without changing their statements. Full proofs and the reusable theoretical definitions are maintained in trureturing PR #10765:

https://github.com/the-omega-institute/trureturing/pull/10765

Pinned theory: https://github.com/the-omega-institute/trureturing/blob/ee33195db81fb50c5ea0ba633488d38ff8666cc8/docs/develop/theory/RECTANGULAR_GRID_PARITY_TRANSPORT.md

## Typed ports and the exact defect

For the existing residual multigraph Gamma, a vertex of positive capacity r has one real port per incident residual edge and 2r-deg(v) distinct slack ports. Pair its 2r ports. A residual-zero leaf is an unpaired L terminal; a slack port is an H terminal. The resulting port graph decomposes into paths and cycles. Write a,b,c for LL,HH,LH path counts and o for odd-length LL paths. All real edges are retained individually.

Then q=C-R=a-b for every pairing. Capacity-one vertices have a unique pairing; capacity-two vertices have three pairings, with the auxiliary routing action S4/V4=S3. This acts on routing choices, not on physical colorings. The signed defect q is invariant under every routing switch.

With D=mn/2-|T| and the previously proved saturated-attachment budget, the new paper bound on even-by-even rectangles is

    D >= 3q + 4b + 2c + o,
    2mn - 4|T| - 3|M| >= 4b + 2c + o.

If every two connected residual-zero leaves have distance at least d>=2, then

    |T| + ((d+1)/(d+2))*|M| <= mn/2.

Thus d=3 gives 4/5 and d=4 gives 5/6. These require the stated extra separation; no universal 4/5 or 5/6 bound is claimed. If no connected leaf pair exists, q<=0. Sharp abstract paths show that the abstract port/capacity assumptions alone cannot yield coefficient one.

## A real componentwise counterexample

On a 4x6 grid with row-major numbering 0,...,23, take

    T = {0,5,12,17,19,22}
    M = {(1,2),(3,4),(7,13),(10,16),(8,9)}.

This is feasible. Its residual capacities are [0,1,0,0,2,0], retaining saturated tiles as isolated zero-capacity vertices, and its residual edges are (0,1),(1,2). The path component has C-R=1, while the separate blank tile of capacity two compensates it. Global q=-1 and |T|+|M|=11<12. Thus the stronger proposed condition that every actual residual component must have nonpositive excess is false. The global grid conjecture is unaffected.

## Repository interfaces and limits

The trureturing companion separates coordinate parity, path-length parity, permutation parity, and prime-factor parity. It proves the classical checkerboard change of basis JQ=B and integer saturation of bipartite incidence; a nonnegative right-hand-side example on P4 shows why all-prime modular solvability cannot replace capacity inequalities. Prime-coordinate abelianization Z^2 ~= <2,3> and an integer Heisenberg lift distinguish endpoint information from path order. A unique-common-neighbor obstruction still prevents S^2=dI for same-support finite-dimensional invertible group gains.

The unrestricted Omega/psi_sq formula remains unproved. A prospective global LL-to-HH compensation must retain the surrounding geometry, including capacity outside a single residual component.

## Executed verification

The companion includes the actual standard-library checker and its result record. Checks passed on all 24 S4 permutations; all 1,099 nonempty labeled graphs through order five for incidence ranks modulo 2,3,5,7; 21,845 lattice words; 261,868 feasible representative pairs on four even rectangles with one seeded routing per pair; 59 sharp abstract paths; and the explicit 4x6 instance. These are finite regression checks, not a universal or Lean proof.

Executed script SHA256: 9356bd14bba1f256015b4c1d023915dc30c4ffe71ad4e3eab01d0292cce898eb. Remote Git blob cb1c75eb210236c98cd616c7ef3593cc87e9e3ba matches the executed source.

No existing Lean, Scribe, strip certificate, manuscript, or CI configuration is changed by this continuation.
