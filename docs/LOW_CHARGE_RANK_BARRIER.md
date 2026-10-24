# Low-charge barrier and the first possible rank-certificate obstruction

20 October 2026. The exact strip incidence certificate has a useful
obstruction threshold: a failure that preserves the desired grid bound
must have residual receiver charge at least four. At charge four, its
residual capacity geometry is completely specified. These are necessary
conditions on a counterexample to the certificate, not a proof of the
grid bound or an assertion that such a counterexample exists.

## Physical assumptions and exact rank

Use the original fixed disjoint2-by2tiling of an even rectangle. T is
selected, P consists of the actual matching endpoints, and Z consists of
tiles without endpoints. Assume the selected feasibility condition, so
each Q in Z has integer d_Q=2-|T intersect Q| in{0,1,2}. Reserve distinct
actual capacity units first:integer0<=a_Q<=d_Q, B=sum a_Q, r_Q=d_Q-a_Q,
D=sum d_Q, R=sum r_Q=D-B.

The residual incidence multigraph has maximal horizontal and vertical
Z-runs as vertices, and one edge per residual unit at Q, between h(Q)
and v(Q). Original runs are not recomputed after reservation. A horizontal
run and vertical run meet in at most one physical tile. Therefore the
graph is bipartite, loopless, and has multiplicity at most two per pair.
This last property is stronger than the arbitrary-multiplicity incidence
matching theorem. It must not be assumed for other resource models.

The previously proved exact one-request-per-run rank is

    K = sum_C min(v_C,e_C).

For a tree component this is e_C=v_C-1; for a component containing a
cycle it is v_C. Isolated vertices contribute zero. All counts below
include parallel edges as separate physical units.

## General quadratic capacity bound

**Lemma1.** If K=0then R=0. If K=1then R=1. For K>=2,

    R <= floor(K*K/2).                                        (1)

**Proof.** In a component containing a cycle, write its two part sizes
as h,w, and put k=h+w=v_C. There are at most2hwedge slots, since each
pair has multiplicity at most two. The identity
(h-w)^2>=0gives2hw<=(h+w)^2/2, hence

    e_C <= floor(k*k/2).

Such a component has k>=2. The sum of the ranks of all tree components,
call it t, equals their total edge count. If there are no cyclic
components, R=Kand the conclusions follow, including K=0or1.

Otherwise let u>=2be the sum of the cyclic component ranks k_i.
Summing their bounds gives

    sum_i e_i <= floor(sum_i k_i*k_i/2) <= floor(u*u/2).

As K=t+u and t,u are nonnegative integers with u>=2,
(t+u)^2-u^2=t^2+2tu>=2t. Therefore

    R <= t+floor(u*u/2) <= floor((t+u)^2/2).

This proves(1). The bounds are sharp for every K>=2: take all tiles
blank in a rectangle with h=floor(K/2)tile rows and w=ceil(K/2)tile
columns. Its incidence graph has h+w=Kvertices and2hwedges, hence
rank K and R=2hw=floor(K*K/2). For K=2it is the parallel two-edge
cycle; for all larger K it remains connected with at least Kedges.
For K=1, one residual unit at one tile gives a single edge. QED.

## Separation of certificate failure from target failure

Now assume single terminality and the original complete-receiver identity

    sigma = mn/2-|T|-|M| = D-rho,

where rho=sum_H rho_H is the ORIGINAL corrected total receiver charge.
It is an integer: each endpoint component contains whole matching edges.
Put q=rho-B. Then sigma=R-q. The hybrid certificate succeeds when

    q <= K.

**Lemma2.** If the hybrid certificate fails, q>K, but the target survives,
sigma>=0, then q>=4. In fact K>=3 and R>=4.

**Proof.** The two assumptions give K<q<=R, hence K<R. If K=0or1,
Lemma1gives R=K. If K=2, it gives R<=2=K. All are contradictions.
Thus K>=3and integer q>K implies q>=4; R>=q>=4. QED.

Equivalently, for q<=3a failure of this certificate would already violate
the target bound. This conditional statement does not prove that target
bound, even in that range. It explains why searching charge-one or
charge-two examples cannot distinguish the stronger certificate from the
target. The same argument applies after valid reservations, with residual
charge q; raw charge alone is not the correct threshold.

## Exact geometry when residual charge is four

**Lemma3.** If q=4, K<q and sigma>=0, then

    K=3, R=4, sigma=0.

Apart from isolated run vertices, the residual incidence graph consists
of one three-vertex component, with two parallel edges on each of its
two distinct run pairs. Thus there are exactly two tiles with positive
residual capacity. Both have r_Q=d_Q=2, contain no selected or endpoint
vertices, have no prior reservation, and share one original maximal
horizontal or vertical Z-run. Their perpendicular runs are distinct.
Every other Z-tile has residual capacity zero. The two tiles need not
be adjacent; no adjacency claim follows from the graph argument.

**Proof.** Lemma2gives K>=3; K<4gives K=3. Equation(1)gives R<=4,
while sigma=R-4>=0gives R>=4. Thus R=4and sigma=0.

If two or more components had positive rank, the positive integer ranks
would partition3as2+1or1+1+1. A rank-one component has one edge and
a rank-two component at most two, giving at most three total edges.
This contradicts R=4. There is therefore one positive-rank component.
It cannot be a tree, since a tree would have only K=3edges. It has
v_C=K=3and e_C=4, so its bipartition sizes are1and2. Its only two
possible run pairs must each have multiplicity two. Each pair arises
from exactly one tile. The shared vertex is one run, while the other
two vertices are perpendicular runs. Finally2=r_Q<=d_Q<=2forces
d_Q=2and a_Q=0; since Q is in Z it is entirely blank. QED.

The blank2-by4vertex rectangle realizes the resource graph in Lemma3,
but its receiver charge is zero, so it is NOT an obstruction to the
hybrid certificate. No physically frozen charge-four example is asserted.

## Consequences for research and validation scope

A restricted first search imposes B=0, original charge rho=4, and the
absence of old corner donors as ADDITIONAL search restrictions. A
target-preserving certificate failure in this subfamily must have
D=R=4, K=3and sigma=0, with exactly the residual support above. In
general, residual charge q=4allows rho=D=B+4with B>0; other tiles may
have positive original capacity fully consumed by reservations. The
classification is exhaustive for the residual support, not for these
additional search restrictions or for higher-charge obstructions. A
reservation-aware search must retain q=rho-Band residual capacities.

The written proofs use the already established exact rank theorem and
the physical multiplicity-two fact. Finite controls and scoped Lean
arithmetic verification are recorded separately. Neither finite search
nor a formal arithmetic implication is presented as a formalization of
the full physical graph adapter or of universal geometric coverage.

The same quadratic bound gives a useful search window. Any separating
failure with q>=4must satisfy

    q <= R <= floor((q-1)*(q-1)/2).                            (2)

Indeed, a failure gives K<=q-1, and Lemma2gives K>=3; apply(1)and
monotonicity of squaring nonnegative integers. Thus charge four forces
R=4, while charge five allows only5<=R<=8. Conversely, for q>=3,
R>floor((q-1)*(q-1)/2)is a sufficient condition for q<=K: if K<=1then
R<=1contradicts this inequality, and if K>=2equation(1)contradicts
K<=q-1. This is a count-based sufficient certificate, not universal
geometric coverage. The square-root scale is sharp for the resource
model by the blank rectangles in Lemma1.

Validation in this revision:

- develop/check_low_charge_rank_barrier.py checks all729multiplicity
  patterns on a2-by-3tile array. Exactly nine have R>=4and K<4,
  all with two doubled tiles sharing one run. Blank rectangles attain
  the general bound for every Kfrom2through64. These blank controls
  have receiver charge zero, so they are not separating examples.
- formal/SubQuorum/LowChargeRankBarrier.lean has seven locally compiled
  Lean4.33.0Std declarations. They prove the small-rank budget across
  arbitrary finite component lists and its charge-four consequences,
  from an explicit per-component interface: e<=k, or k>=2and2e<=k*k.
  Every declaration was axiom-audited: six use propext/Quot.sound;
  charge_four_numeric_shape additionally uses Classical.choice.
  The full graph adapter, all-Kquadratic proof and support classification
  remain written. See output/low-charge-rank-barrier-formal-check.json.
- Two known frozen no-four-corner fixtures are positive SAT controls
  for the search base, with encoded charge equal to the independent
  ORIGINAL corrected ledger. Freeing their selected labels but fixing
  endpoints and matching gives finite UNSAT for a rank failure in each
  fixed geometry. This is not a theorem about other geometries.
- The direct charge-four shape encoding is independently checked on
  all729abstract capacity patterns; it accepts exactly the same nine
  resource shapes. It replaces the expensive vertex-cover variables
  by the proved exact doubled-tile geometry in this specific mode.
  Both the original unrestricted6-by-8single-terminal search and the
  original8-by-10charge-four cover search timed out at60seconds.
  UNKNOWNis not UNSAT. The direct shape search has its own receipt.

An independent Oracle review of Lemmas1-3and their precise physical
scope completed ACCEPT at19:07:22.712UTC on19October, task
6235d011-89c7-48ed-9fd6-f9d5ba2a93f0, conversation conv_2da61158eec5df89,
original stream execution97501, observed gpt_6/pro. The reviewer confirms
all three proofs and recommends the explicit reservation/search scope
now printed above. Its source-note attachment predates the search-window
corollary and these validation paragraphs, and it did not execute code
or Lean. Original stream and terminal response are preserved separately
from local verification. This acceptance does not cover universal grid
coverage or the earlier sealed-strip repair infrastructure failure.
