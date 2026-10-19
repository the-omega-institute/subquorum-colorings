# Keep the high cycle closed: connected cubic gaps of three over sixty-two

19 October 2026. All graphs are finite and simple. Two-star formation
is non-induced and minimality is by inclusion. This note improves this
project's connected cubic gap coefficient from1/24 to3/62. It is not
a literature-priority claim. The journal manuscript is unchanged.

## The exact family

**Theorem.** For every integer r>=1 there is a two-connected cubic
bipartite graph Z_r satisfying

    |V(Z_r)|=62r,
    beta_2(Z_r)=33r,
    SF_2(Z_r)=36r,
    SF_2(Z_r)-beta_2(Z_r)=3r=3|V(Z_r)|/62.

Moreover7SF_2=3|V|+2beta_2, so the established cubic compensation
inequality is attained. The displayed minimal forming set has6r
selected isolates, balanced between the bipartition classes.

Since3/62>1/24, this improves the previous asymptotic construction.
The general upper coefficient remains1/14; its connected asymptotic
optimality is not settled. No new rectangular-grid bound is asserted.

The difference from L_r is precise: every H six-cycle stays closed.
Only one surviving X edge per module is opened for the cyclic interface.
The previously troublesome exceptional local state requires the H seam
to be open as well. Keeping that edge excludes the state locally.

## The core and its independent omission budget

Start with C_1 on20vertices, with all indices modulo six:

    H={h_0,...,h_5}, U={u_0,...,u_5}, X={x_0,...,x_5},
    Y={y_0,y_1}.

Both H and X initially induce six-cycles. Add h_i--u_i--x_i and
u_i--y_(i mod2). Delete the three designated X pairs

    e_j=x_(2j)--x_(2j+1), j=0,1,2,

and also delete x_5--x_0. Call the resulting graph R. Its only
remaining X edges are x_1--x_2 and x_3--x_4. In particular H remains
an intact six-cycle. For a dissociation set D in R let m(D) count
the designated pairs whose two endpoints are omitted.

**Closed-high-cycle lemma.** Every such D satisfies

    |D|+m(D)<=12.                                        (1)

The inequality allows arbitrary choices at both interface vertices
x_0,x_5. No restriction on a neighboring module is consumed.

**Normalization.** At each designated pair with exactly one endpoint
selected, remove that endpoint. This preserves dissociation and
preserves |D|+m(D), decreasing its first term and increasing its
second term by one. After normalization each pair is wholly selected
or wholly omitted. Write z_j in{0,1} for its common selection state;
write a_i,v_i for the H,U indicators, and q for the number of selected
Y vertices. The normalized score is

    sigma=3+C_0+C_1+C_2+q,
    C_j=a_(2j)+a_(2j+1)+v_(2j)+v_(2j+1)+z_j.             (2)

**Cell bound.** Each C_j<=3. If z_j=0, its four H/U vertices form
u_(2j)--h_(2j)--h_(2j+1)--u_(2j+1); all four cannot be selected.
Equality forces both U vertices and exactly one H vertex. If z_j=1,
a_i+v_i<=1 at each of the two indices, since otherwise u_i has both
h_i and x_i selected. Again C_j<=3. Call a cell tight at equality.

**No hub.** If q=0, (2) and the three cell bounds give sigma<=12.

**One hub.** The reflection i->5-i preserves R, exchanges the two
hubs, and reverses the three designated pairs. Thus assume y_0 is
selected. For a tight cell with z_j=0, both U vertices are selected,
its even H vertex is omitted and its odd H vertex is selected. For
a tight cell with z_j=1, its even U vertex is omitted, its even H
vertex is selected, and exactly one of its odd H/U vertices is selected.

Two consecutive tight cells, at j,j+1 for j=0 or1, force z_(j+1)=0.
Indeed, suppose z_(j+1)=1. If z_j=0, the selected odd H of the first
cell already meets its U partner and would gain the next even H as
a second selected neighbor. If z_j=1, the retained X edge between
the cells forces the first cell's odd U to be omitted. Its odd H
is then selected and meets both the even H in its own cell and the
next cell's even H. Each case contradicts dissociation.

If all three cells were tight, z_1=z_2=0. Then u_2,u_4 would both
be selected neighbors of selected y_0, another contradiction. Hence
sum C_j<=8 and sigma<=3+8+1=12. Only the two retained X edges were
used; no interface X edge has been restored.

**Both hubs.** A tight cell cannot have z_j=0: its selected H would
give the selected U partner a second neighbor beside its hub. Thus
every tight cell has z_j=1, both U vertices omitted, and both H
vertices selected. Two tight cells would then select four consecutive
vertices on the intact H six-cycle. This violates dissociation. All
three pairs of cells are adjacent on that cycle, including the first
and last across h_5--h_0. At most one cell is tight, so sum C_j<=7
and sigma<=3+7+2=12.

These cases prove(1) for normalized sets and hence every D. This is
a direct graph proof, not an inference from the finite optimum.

## Attach three blocks and join through X only

Take r disjoint copies R_i. At each of their three designated pairs,
attach a separate broken Heawood graph B_(i,j), obtained by removing
point0--line8 from the Fano incidence graph. Add

    point0_(i,j)--x_(2j+1,i),
    line8_(i,j)--x_(2j,i).

Finally add x_(0,i)--x_(5,i+1) cyclically. At r=1 this restores the
single missing X interface edge. At r=2 the two new edges have distinct
endpoint pairs. The resulting graph is Z_r.

Give h_i,x_i parity i mod2, u_i the opposite parity, and y_j parity j.
The Heawood point side has even color, its line side odd. Every displayed
edge joins opposite colors. Every vertex has degree three; simplicity
and order20r+14(3r)=62r follow directly.

## Exact dissociation number, without reused deficits

Let D be any dissociation set of Z_r. Its core restriction D_i is
dissociating in R_i. The established Heawood saturation lemma says
that each block contains at most eight vertices of D; if it contains
eight, both block ports are selected and each already has a selected
internal neighbor. Both adjacent core vertices must then be omitted.

Let b_i count these eight-vertex blocks in module i. They use distinct
designated pairs, so b_i<=m(D_i). The three block restrictions together
have size at most21+b_i. Thus(1) gives

    |D intersect module_i|<=|D_i|+21+b_i
                          <=|D_i|+21+m(D_i)<=33.

Each core vertex, block vertex and dense-block surplus occurs once.
The local inequality places no selection condition on the neighboring
module. Consequently beta_2(Z_r)<=33r, even though modules are joined.

For attainment select all seven points in every Heawood block, and

    U union H_odd union X_even

in every core. The core selection has twelve vertices and induces a
matching: each U meets its H partner at odd indices or X partner at
even indices. Every block interface and cyclic interface has an omitted
endpoint. The full selection is dissociating and has21r+12r=33r vertices.

## Exact SF and two-connectivity

In every core select H union U. Every x_i has unique selected neighbor
u_i, whose selected support is h_i; every y_j has three selected U
neighbors. Deleting h_i leaves x_i adjacent only to the now-isolated
u_i, and deleting u_i leaves x_i with no selected neighbor. Thus this
twelve-set is minimal forming in the unmodified C_1.

In every Heawood graph use its established eight-set
{1,2,3,5,7,9,10,11}, with ports0,8 omitted. It is minimal forming,
induces a six-cycle and two isolates, and has explicit deletion witnesses.
All cut and newly added edges in the construction have both endpoints
outside the union S of these fixed selections. More generally, if two
graphs differ only on edges within V minus S, then every T subset S is
forming in one exactly when it is forming in the other. A covering
two-star for an omitted vertex uses that vertex and two vertices of T;
every required edge has an endpoint in T and is therefore unchanged.
This also applies to T=S minus a selected vertex: no changed edge meets
that removed vertex, since it belonged to the original S. Formation
and every deletion failure are preserved. Therefore S is minimal in
Z_r and has12r+8(3r)=36r vertices.

The established general cubic bipartite inequality yields

    7SF_2(Z_r)<=3(62r)+2(33r)=252r,

so SF_2(Z_r)<=36r. This proves the exact value. This upper proof does
not depend on the newer Heawood block-capacity theorem pending review.

For the edge-swap fact, let A,B be disjoint two-connected graphs with
edges ab,cd. Replacing those edges by ad,bc preserves two-connectivity.
Both graphs remain connected after their edge is removed. If a vertex
v of A other than a,b is deleted, A-v is connected and cutting ab can
only separate a from b; the connected B-cd supplies the bypass. If
v=a or b, the surviving cross-edge joins the connected A-v to B-cd.
The argument for a vertex of B is symmetric. Thus every vertex deletion
leaves the joined graph connected.

For connectivity, start with C_1 and three separate Heawood graphs.
Perform three successive two-edge swaps, each joining one Heawood graph
to its designated core pair. Each input graph is two-connected, and
the edge-swap vertex-deletion argument preserves two-connectivity.
The intermediate full62-vertex module is therefore two-connected.
Its x_5--x_0 edge survives these swaps. Delete that edge in every
module and join the exposed endpoints cyclically. If one vertex is
deleted, its module minus that vertex was connected before the edge
cut. Cutting the edge can split it into at most two pieces containing
the two ports; the path through the other modules reconnects them.
If the deleted vertex is a port, that module minus the port is connected
and the remaining modules form an attached chain. Other modules with
one edge removed stay connected. This covers r>=2, including r=2;
at r=1 the interface edge is restored. Thus Z_r is two-connected.

## The coefficient is optimal within the distinct-port C_1 architecture

The following later deduction applies to a broader class than the rings.
Take r copies of C_1 and b broken Heawood blocks. Preserve every core
edge incident to H,U,Y and every internal broken-block edge. Attach
each block's two ports to two core X vertices, with all2b attachment
vertices distinct. Choose the remaining edges arbitrarily among core
X vertices, subject to simplicity, cubic degree and the standard
bipartition. No other interface edges are allowed. Connectivity is
not needed for this corollary; every Z_r is in this class with b=3r.

**Architecture bound.** Every resulting graph G satisfies

    SF_2(G)-beta_2(G)<=b,
    62(SF_2(G)-beta_2(G))<=3|V(G)|.                       (3)

In particular no X-only gluing within this entire class improves3/62.

**Proof.** The core has6r X vertices, so distinct attachment gives
2b<=6r. In every core take U union H_odd union X_even. In every
Heawood block take its seven vertices in the global even color class.
The selected core edges form a matching. Every additional X edge or
block-to-core edge has an omitted endpoint: its odd X endpoint is
omitted, or its odd block endpoint is omitted. This gives a dissociation
set of size12r+7b, for every allowed X gluing. Thus beta>=12r+7b.
Writing n=20r+14b and g=SF_2-beta, the established cubic inequality gives

    7g<=3n-5beta<=3(20r+14b)-5(12r+7b)=7b.

Hence g<=b. Since b<=3r,

    62g<=62b<=60r+42b=3n.

This proves(3), independently of the pending general block ledger.
The conclusion is restricted to the stated architecture, not a universal
cubic bound. A subsequent [two-witness theorem](CORE_BLOCK_GAP_BARRIER.md)
removes the distinct-attachment assumption and permits arbitrary bipartite
high two-factors and hub regrouping, while preserving the3/62ceiling.
Thus reusing core attachment vertices or changing high cycles alone does
not escape the bound. Improving the coefficient requires changing other
core incidences or obstruction blocks. The earlier long-core result also
shows how modifying high edges can increase beta and reduce the gap.

## Evidence and scope

The proof of(1), its graph-to-count extraction, block charging, all-r
construction, attainment and connectivity are written proofs. Enumeration
is only an independent control. Existing saturation and cubic compensation
theorems are explicit dependencies.

The [companion checker](../scripts/check_closed_high_cycle.py) exhausts
the fixed20-vertex core and tests its
normalization, cell cases, hub reflection, score and port behavior.
It constructs the actual ring graphs and checks cubic bipartiteness,
literal formation and each selected deletion, the dissociation witness,
and connectivity after every vertex deletion. Larger exact beta/SF
labels follow from the written proof, not a numerical optimization.

The [Lean source](../formal/StarForming/ClosedHighCycle.lean) proves
conditional cell/count statements, including
the exclusion of the two-hub exceptional state by the intact H seam.
Graph-to-count extraction, the arbitrary-r graph theorem and connectivity
are not claimed fully Lean-formalized. Verification receipts and the
separate independent review status are recorded alongside this note.

The [finite receipt](../output/closed-high-cycle-controls.json) records
all1,048,576core subsets,96,788dissociation sets,64port patterns and
nine interface degree patterns, all with maximum score12. Normalization,
hub cases and reflection pass. Ten actual rings give1,980literal
selected-deletion checks and3,410vertex-deletion connectivity checks.
The [Lean receipt](../output/closed-high-cycle-formal-check.json) records
the seven original declarations, one reused from the previous one-hub
proof, and four later counts for the enlarged two-witness architecture
bound. All eleven use only standard logical axioms. Local validation ran sequentially on the
authorized machine after memory and lean/lake basename preflight.
One hundred additional arbitrary X-gluing instances, with one to five
cores and every permitted block count, check the architecture's explicit
dissociation lower bound and8,640selected deletion failures for its
unchanged forming witnesses. Their beta/SF values are not optimized.

The [independent Oracle review](../output/closed-high-cycle-oracle-review.json)
completed ACCEPT on19October at02:06UTC, with observed model gpt_6 and
effort pro. Its [exact response](reviews/2026-10-19-closed-high-cycle-review-response.txt)
accepts the all-r construction, local omission lemma, distinct surplus
charges, exact beta/SF attainment and two-connectivity, including r=1,2.
The optional all-T rewiring statement and edge-swap exposition are now
explicit above. The later architecture-bound corollary was not in that
input and remains a separate written deduction with a conditional Lean
count. The separate general block-ledger review initially returned REVISE;
its same-conversation [follow-up](../output/heawood-block-compensation-followup.json)
now accepts the clarified general theorem and all-k SF consequence.
Neither review is a premise of this construction or its architecture bound.

Reproduce:

    python3 scripts/check_closed_high_cycle.py --output output/closed-high-cycle-controls.json
    python3 scripts/check_cover_pullback_formal.py --audit closed-high-cycle --lean /path/to/lean-4.33.0 --output output/closed-high-cycle-formal-check.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
