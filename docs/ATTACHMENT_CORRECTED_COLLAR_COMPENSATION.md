# Removing ordinary pressure faces: the exact internal-attachment debt

19 October 2026. This strengthens the pressured-collar sufficient theorem by
removing the pressure requirement on every unmarked tile. Receiver regions
may be thick, contain degree-four tiles or be disconnected. The replacement
is an explicit internal saturated-attachment budget, and a corrected parity
term. The unrestricted grid problem remains open.

## Definitions

Use the same feasible pair (T,M), aligned 2x2 tiles and full-configuration
charges as in `PRESSURED_COLLAR_COMPENSATION.md`. A deficient tile has at
most one T vertex; a saturated tile has exactly two. Write P for matching
endpoints and B for blank vertices. All quantities refer to the original
configuration, including crossings between regions to be combined later.

Let R be any finite tile region. Choose L distinct marked tiles, each with
one BB face and its two perpendicular faces pressured by actual occupied
neighbors. There is no pressure, tree or degree condition on any other tile.
Define:

- D(R): the sum of b_Q-t_Q over deficient tiles Q in R only;
- k(R): matching edges wholly in R joining a deficient tile to a saturated
  tile; within-tile matching edges are not included;
- sigma: matching edges from a deficient tile in R to a saturated tile
  outside R;
- eta: matching edges from a saturated tile in R to a deficient tile
  outside R;
- Q: matching endpoints in saturated tiles of R;
- j: all physical matching edges crossing R's boundary.

The letter Q here is an endpoint count, not a tile name. Every saturated
tile has at most one P vertex, so Q also counts the saturated tiles with P.

## Local facts without pressure

Every deficient tile satisfies b_Q>=t_Q. For t_Q=0 this is immediate. For
t_Q=1, its selected corner has two internal neighbors and at most one may
be occupied, so at least one is blank. No external pressure is needed.

A saturated tile has t_Q-b_Q=p_Q with p_Q<=1. Adjacent selected corners
force both remaining corners blank. For diagonal selected corners, both
remaining corners cannot be occupied, since each T would have two occupied
internal neighbors. The vertex partition then gives b_Q=2-p_Q.

There is no matching edge between two saturated tiles. Both endpoints would
be their tiles' unique P corners, with diagonal T corners. Across the shared
tile face the two companion corners would be adjacent T vertices, each
already adjacent to its own P corner, violating feasibility.

The marked-tile argument from the pressured lemma gives b_Q-t_Q>=2 and
also makes every marked tile deficient. Summing over deficient tiles yields

    D(R) >= 2L.                                         (1)

## Exact ledger and corrected parity

**Theorem.** For every region and marking satisfying the stated hypotheses,

    Q = k+eta,
    2rho(R) = -D(R)+k+sigma,
    D(R) mod2 = (j+Q) mod2,
    2rho(R) <= -2L+k+sigma-((j+Q) mod2).                (2)

Proof. Every saturated P endpoint is matched to a deficient tile. Splitting
its mate according to membership in R proves Q=k+eta; the matching gives
one edge per endpoint and there is no double counting.

For each deficient tile the earlier elementary identity is

    2rho_Q=t_Q-b_Q+s_Q,

where s_Q counts matching edges to saturated tiles anywhere. Its sum over
R has sum s_Q=k+sigma. Saturated tile charges are zero. This proves the
second identity without a missing incoming-boundary correction.

For total counts t,b in R, the saturated local identity gives

    D(R)=b-t+Q.

The exact matching vertex partition 4|R_tiles|=t+b+2mu+j implies b-t and j
have the same parity. Thus D has parity j+Q. Its lower bound (1) is even,
so D>=2L+((j+Q) mod2). Substitute in the exact charge identity. QED.

Equivalently, using the existing regional ledger directly gives
2rho=t-b+sigma-eta=-D+Q+sigma-eta=-D+k+sigma.
Incoming saturated endpoints do not create a free deficit or an extra
resource; their count cancels eta exactly. Internal saturated attachments
remain as actual debt.

## Uniform compensation and the pressure-free sufficient class

For pairwise tile-disjoint source regions U_i, disjoint from R, assume
sum rho(U_i)<=L. Full-configuration additivity and (2) give

    2rho(R union all U_i) <= k+sigma-((j+Q) mod2).        (3)

In particular k+sigma<=((j+Q) mod2) pays all source regions simultaneously.
This includes **k=sigma=0 for arbitrary unpressured or thick receivers**,
with unrestricted eta. No assumption about residual-component closure,
matching directions, capacity-two visits, or the shape of R is used.

The one budget D is summed over disjoint deficient tiles; each marked tile
is used once and each actual internal attachment contributes once to k.
An overlapping second application to the same receiver remains invalid.
Packing disjoint compensated cores with a nonpositive remainder proves
|T|+|M|<=mn/2 on this enlarged sufficient class. The universal 5/6 bound
and arbitrary internal-attachment compensation are not settled by (3).

The previous pressured theorem is recovered exactly: pressure on every
tile implies Q=0 and hence k=eta=0, restoring its parity j mod2.

## Two necessary corrections, with explicit physical witnesses

All coordinates are zero-based in a 10-by-16 rectangle. Vertices not listed
as selected or matching endpoints are blank.

**The parity cannot remain j mod2 after pressure is dropped.** Let

    T={(4,10),(5,11)},
    M={((4,11),(4,12))},
    R=the single tile at tile coordinate (2,5).

Each T has exactly one occupied neighbor, the P at (4,11). R is saturated
with Q=eta=j=1, k=sigma=D=0 and rho=0. The old uncorrected bound at L=0
would assert 2rho<=-1 and is false. The corrected parity j+Q is even and
(2) is exact. This refutes a pressure-free parity rule, not the grid target.

To include a genuine marked terminal, add tile (2,2) to R and matching
edges (4,5)--(5,5), (3,4)--(3,5), (6,4)--(6,5). Its left face is BB and
top/bottom faces are pressured. Then L=1, D=2, rho(R)=-1 and Q=eta=j=1.
The old bound would say 2rho<=-3, still false. Formula (2) gives -2 exactly.
This receiver is disconnected, as permitted by the general theorem.

**The internal debt coefficient cannot be decreased.** Take

    T={(2,2),(3,3),(3,5)},
    M={((2,3),(2,4)),((2,5),(1,5))},
    R=the two adjacent tiles (1,1),(1,2).

All selected vertices have one occupied neighbor. The first tile is
saturated; the second has labels PP/BT and (r,d)=(0,1). Thus
Q=k=j=1, eta=sigma=D=0, 2rho(R)=1. Formula (2) is exact. Dropping k
would assert rho(R)<=0, which fails. This is a connected physical
obstruction to that local rule; its whole-grid objective is only 5<80.

There is an unbounded connected version. For every ell>=1, use a
6-by-(2ell+8) rectangle, keep the preceding T and two matching edges,
and include the two lower tiles and upper tile row0, columns2,...,ell+1
in R. Add the following matching edges:

- (0,4)--(1,4);
- (1,2c)--(1,2c+1) for 3<=c<=ell+1;
- (0,2c+1)--(0,2c+2) for 2<=c<=ell+1.

All endpoints are distinct; every selected vertex keeps its one occupied
neighbor. Every upper tile is full P, with h=1,r=1,d=2 and zero charge.
The residual path goes upward from the deficient gadget and turns right
through the upper row; its final edge leaves R into a deficient tile.
Thus R is an induced tile path, k=Q=j=1, D=eta=sigma=0 and rho(R)=1/2
at every length. Its global objective is 2ell+5<6ell+24=mn/2. This is an
all-length obstruction to paying the internal debt merely by a long or
bent receiving route, not a counterexample to the grid inequality. QED.

## Verification and scope

The general argument above is the proof; finite enumeration is auxiliary.
`develop/check_attachment_collar_compensation.py` checks local unpressured
states and actual matching fixtures, with the original regional ledger and
eight grid symmetries. The thick-region fixtures include a degree-four tile
and an incoming saturated endpoint with no pressured face, outside the
previous theorem's hypotheses.

`formal/SubQuorum/AttachmentCollarCompensation.lean` kernel-checks the local
unpressured implications and conditional corrected parity/aggregate counts.
The geometry-to-count and attachment identities retain the written proof;
end-to-end grid formalization is not claimed. The local combined audit
passes ten declarations (six original, four new), with axiom sets contained
in {propext, Quot.sound}. Finite controls pass 40 unpressured deficient
states, ten saturated states, 45 physical regions and 360 symmetry images,
including debt-path lengths zero through forty. These finite ranges do
not replace the all-length construction or general proof.

```sh
python3 develop/check_attachment_collar_compensation.py --output output/attachment-collar-controls.json
python3 scripts/check_collar_formal.py --lean /path/to/lean4.33.0/bin/lean --output output/attachment-collar-formal-check.json
```

The earlier collar ACCEPT covers its earlier hypotheses, not this new
extension or its two obstruction rules. The same-conversation follow-up
2e81689f-ebdb-4ef9-902c-0c3af27da282 is pending; its original stream and
prompt identity are retained. See `output/attachment-collar-oracle-review.json`.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
