# Exterior components: exact port budgets and single-use compensation

7 October 2026. This follows the [mixed-band boundary-debt lemma](MIXED_BAND_BOUNDARY_DEBT.md).
We compute exactly when a whole exterior residual component can pay its
incoming half-unit demands. The incidence is given by the actual residual
edges, so no additional donor-window hypothesis is needed for this class.
The counting argument applies to bent paths, capacity-two tiles, branching,
and parallel residual edges. It does not establish the criterion for all grids.

## 1. The exterior component identity

Use a feasible pair on an even-by-even rectangle with the aligned residual
multigraph Gamma. A deficient tile has capacity r in {0,1,2} and charge
rho=d/2-r; a saturated tile has charge zero. Edges of Gamma are matching
edges between distinct deficient tiles. Parallel edges remain distinct.

Let D be a nonempty connected component of the graph induced by any chosen
set of deficient tiles. Write v=|D|, e for its internal residual edge count,
p for its residual edges to deficient tiles outside D, and R=sum_D r.
Let l count its capacity-zero tiles, h its capacity-two tiles, and
mu=e-v+1 its cycle rank. Degrees here include every external residual port.
Define its integer balance B(D)=1+h-l-mu. Then

    rho(D)=e+p/2-R=p/2-B(D),
    p/2+rho(D)=p-B(D).                                    (1)

**Proof.** Degree summation gives sum_D d=2e+p. Because every tile capacity
is zero, one or two, R=v+h-l. Connectivity gives e=v-1+mu, including
parallel edges. Substitution proves both identities. QED.

Thus D supplies p/2 units of net negative charge to its actual p incoming
ports **if and only if**

    p+mu+l <= 1+h.                                       (2)

This is a necessary and sufficient condition for paying these demands from
D alone. It is not a sufficient condition for grid feasibility. Each extra
capacity-two tile adds one unit to B; each independent cycle or capacity-zero
tile consumes one. The charge budget itself is -rho(D)=B(D)-p/2, rather
than raw residual capacity R or the number of route visits.
Here h is the number of capacity-two tiles, not the tile-internal matching
count denoted by h in earlier notes.

For a component with c connected pieces, the same proof gives
B=c+h-l-mu, with mu=e-v+c. We use maximal connected components below so
each resource has a canonical identity.

## 2. A component-based global compensation theorem

Let A_i=U_i union S_i union C_i be pairwise tile-disjoint patches satisfying
the full geometric hypotheses of Lemma 2 in the preceding note. Saturated
side caps omitted from A_i have zero charge. Write beta_i and tau_i for
their lower-boundary residual and saturated export counts. Assume:

1. Every residual edge from A=union_i A_i to the deficient remainder W is
   one of the lower-boundary beta_i exports, and every beta_i export ends
   in W. In particular, no beta export ends in another accounting patch.
2. D_1,...,D_s are the maximal connected components of Gamma[W] incident
   to these exports. Let p_j be their total number of incoming ports,
   counting every matching edge once, including ports from different patches.
3. W_0 consists of all other deficient remainder tiles. Its charge is
   retained explicitly.

These are auditable geometric and graph hypotheses. Hypothesis 1 is not
inferred from tile-disjointness alone. It excludes exports between patches
and any unmarked residual crossing. Saturated attachments are already
included in the tile capacities and do not become residual ports.

**Theorem 1 (exterior-component compensation).** Put
epsilon_j=p_j+mu_j+l_j-h_j-1=p_j-B(D_j). Then

    q <= sum_i tau_i + sum_j epsilon_j + rho(W_0).        (3)

Consequently, if every tau_i=0, every epsilon_j<=0, and rho(W_0)<=0, then
q<=0. On this covered class `|T|+|M|<=mn/2`, replacing the uniform
`|T|+(5/6)|M|<=mn/2` estimate by coefficient one.

**Proof.** The preceding lemma gives rho(A_i)<=beta_i/2+tau_i. Every
residual crossing is counted once in beta and once as an exterior port,
so sum_i beta_i=sum_j p_j. The exact tile partition gives

    q=sum_i rho(A_i)+sum_j rho(D_j)+rho(W_0)
      <=sum_i tau_i+sum_j(p_j/2+rho(D_j))+rho(W_0).

Apply (1) to each component. This proves (3) and its consequence. QED.

The no-reuse step is explicit. If n_ij is the number of actual beta_i edges
entering D_j, allocate x_ij=n_ij/2 from D_j to patch i. Under (2),
sum_i x_ij=p_j/2<=-rho(D_j), so the one budget of D_j pays every incident
patch simultaneously. Summing over j pays beta_i/2. Components are disjoint
and each appears once in the ledger, irrespective of route names or repeated
visits. This directly proves the capacitated Hall condition for this actual
incidence whenever (2) holds; it is not an assumed Hall theorem for arbitrary
proposed windows. Tau still requires separate compensation.

Even if individual components fail (2), (3) retains their signed balances.
Negative epsilon from other components or W_0 may pay a positive epsilon.
The simpler diagnostic `delta_ext=sum_j max(0,epsilon_j)` yields
q<=sum tau_i+delta_ext+rho(W_0), but discards useful negative balances.
A positive epsilon identifies failure to pay ports from that component
alone. It does not refute the grid target.

## 3. Bent forests and shared receivers

For an exterior tree without capacity-zero tiles, (2) becomes

    p <= 1+h.                                            (4)

Its embedding and turns are irrelevant to this count. A capacity-one tree
with one port has charge -1/2 and pays that port exactly. With two ports it
has charge zero and is short by one full unit, regardless of its length.
An additional capacity-two tile lowers its charge by one and lets the
same tree pay both half-unit demands. More generally a shared tree with
p incoming ports is sufficient precisely when h>=p-1.

This is a shape-independent sufficient class for arbitrary bent exterior
trees. It does not cover arbitrary bent positive source regions: each source
still needs the geometric local lemma and the partition hypotheses above.

**Proposition 2 (arbitrarily long normalized bent shared receiver).** For
each k>=2 there is a feasible configuration on an 8-by-(2k+4) rectangle,
with an induced exterior path D of k+1 capacity-one tiles, two external
ports and a right-angle turn. Every tile of D has charge zero. Hence this
shared receiver supplies no net compensation, even though it has arbitrary
length and is already neutral-attachment normalized.

**Proof.** Select no vertices. Let D consist of tile row 1, columns 1..k,
and tile row 2, column k. Match:

* (1,2)--(2,2), the first external port;
* (3,2j)--(3,2j+1) for 1<=j<k, the bottom pair in each straight tile;
* (2,2j+1)--(2,2j+2) for 1<=j<k, joining the upper corners of adjacent tiles;
* (2,2k+1)--(3,2k+1), the right pair of the turning tile;
* (3,2k)--(4,2k), the downward turn;
* (5,2k)--(5,2k+1), the bottom pair in the final tile;
* (4,2k+1)--(4,2k+2), the second external port.

These edges have disjoint endpoints. With no selected vertices, feasibility
is immediate. Every D tile has four P corners, one internal matching edge,
no saturated attachment, r=1 and residual degree two. Its k internal residual
edges form the stated path, with p=2, h=l=mu=0. Equation (1) gives rho(D)=0
and epsilon=1. There are no saturated tiles or attachments, so normalization
has no move. The total objective is 2k+3<8k+16=|V|/2. This refutes the
long-or-bent receiver rule, not the grid inequality. QED.

Deleting the first tile's internal bottom edge preserves feasibility and
the path edges. Its capacity becomes two and its charge becomes -1; all
other D charges stay zero. Now epsilon=0 and its one budget pays both ports.
Alternatively deleting the second external port leaves a capacity-one
one-port path of charge -1/2. Both modifications attain the claimed bounds.

Cycles must also be retained. On a 6-by-8 grid with no selected vertices,
take D as the two tiles in rows 2,3 and columns 2..5. Match the two parallel
cross-tile edges (2,3)--(2,4) and (3,3)--(3,4), the right internal edge
(2,5)--(3,5), and the two external edges (2,1)--(2,2), (3,1)--(3,2).
The first D tile has r=2,d=4 and the second r=1,d=2. Thus p=2,h=1,mu=1,
l=0, rho(D)=0 and epsilon=1. Ignoring the parallel-edge cycle would falsely
declare its two ports paid. Deleting the right internal edge makes h=2,
rho(D)=-1 and epsilon=0. All configurations are feasible and satisfy the
grid target with slack.
These are receiver-region witnesses. Their remaining tiles are not the
filled-source accounting patches required by Theorem 1.

## 4. Applying the theorem to the previous equality family

In the 8-by-(6b+14) family, take A=U union S union C. The only residual
crossings to W are the b lower exports. Each receiving component is a
single capacity-one tile with p=1, so B=1, rho=-1/2 and epsilon=0.
Every other exterior deficient tile has charge zero. Also tau=0. Theorem 1
therefore proves q<=0 for every b, with equality, including the capacity-two
source version. The beta debts are now paid by their actual outside
components once, rather than by an assumed list of local donors.

This completes the allocation argument for that unbounded obstacle family
and the larger stated component class.

## 5. Closing a bounded-depth envelope without a component sign condition

There is a second way to handle shared neutral receivers, using the already
established all-length Omega theorems for widths eight and ten. Its additional
geometry is explicit, and it does not assume (2).

Retain one filled-source patch U,S,C. Let H be eight or ten and let Z be the
H-by-N window, N=2k+4, consisting of its first six vertex rows together with
H-6 further rows underneath, across the full source width. Require the two
tiles of rows 4,5 outside C to be saturated with no matching endpoints.
Let D be all tiles in the additional rows. U,S,C and the specified outer
tiles have no matching exit from Z: their fixed source edges, side caps and
receiving caps close their upper and lateral boundaries. Therefore every
matching edge leaving Z has its inside endpoint in D.

Let beta_Z count these edges with both endpoint tiles deficient, and tau_Z
those with the inside tile deficient and the outside tile saturated. An
edge whose inside tile is saturated is counted in neither. Both the lower
and lateral boundaries of D are included, including exits into another
candidate window.

**Lemma 3 (eight- or ten-row envelope).** Under these hypotheses,

    rho(C)+rho(D) <= -1+beta_Z/2+tau_Z,
    rho(Z) <= beta_Z/2+tau_Z.                             (5)

**Proof.** Delete all matching edges leaving Z, without promoting endpoints.
The charge in Z decreases by beta_Z/2+tau_Z, using the exact deletion
identity; saturated inside endpoints retain zero charge. Restrict to Z.
The pair is feasible and no matching endpoint is left unmatched. For even
N, the existing all-length strip theorem gives Omega(G_(H,N))<=HN/2 for
H=8 or 10. Hence its global charge is at most zero. Before deletion,
rho(Z)=1+rho(C)+rho(D): S and all remaining side tiles have zero charge.
Restoring the accounted boundary changes gives (5). QED.

When beta_Z=tau_Z=0, the larger region C union D pays the source's full
unit even if it contains merged two-port receivers or residual cycles.
For tile-disjoint closed envelopes and a nonpositive deficient remainder,
summing gives coefficient one. Boundaries are counted at the envelope,
so an edge between candidate envelopes is not silently declared closed.
This corollary covers only the stated depth and frame geometry. It uses
the existing width-eight/ten computer-assisted theorems, not an independent
proof for arbitrary depth or width. No physical vertex changes other than
deleting external matching edges are required.

The previous 8-by-(6b+14) family satisfies these outer-tile hypotheses and
has a closed eight-row envelope. Its C union D charge is exactly -1, for
every b and also after the capacity-two source flip. Lemma 3 proves the
same compensation directly, without requiring each exterior component
to pass (2). Complete indexed vector certificates can be reproduced by
`python3 scripts/check_strip.py 8` and `python3 scripts/check_strip.py 10`
after compiling the two exact transfer programs. The all-length argument
is in `develop/grid-strips-2026-09-27.md`.

Universal grid compensation still
requires proving enough negative total balance, handling zero-capacity
leaves and cycles, and accounting for saturated or inter-patch exports.
The journal manuscript is preserved. This is an elementary graph-counting
corollary combined with the established width-six/eight/ten strip bounds; no new Lean
theorem or priority claim for graph theory is made.

Run `python3 develop/check_exterior_component_budgets.py --output output/exterior-component-controls.json`.
The finite controls check the written identities, feasible bent/cyclic
witnesses, all eight symmetries, and the previous equality family. They are
validation, not the all-size proof.
