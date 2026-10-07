# Residual cycle pruning and automatic one-port compensation

7 October 2026. This continues [exterior-component budgets](EXTERIOR_COMPONENT_BUDGETS.md).
We prove an occupancy-preserving cycle cancellation, including circuits
that visit a capacity-two tile twice. We also remove the tree hypothesis
from one-port compensation. The statements below are elementary and apply
at arbitrary size. The global source-patch conclusion retains the previously
stated local geometric lemma and its width-six Omega dependency.

## 1. Slack terminals identify the actual shortage

For any deficient tile region D, let p be its residual boundary edge count.
Let a count its tiles with r=0,d=1, the positive zero-capacity leaves, and
let H=sum_{Q in D,r_Q>0}(2r_Q-d_Q). Degrees include all boundary ports.
The residual degree bounds give H>=0; other capacity-zero tiles have d=0.
Directly from rho(Q)=d_Q/2-r_Q,

    2rho(D)=a-H,
    p/2+rho(D)=(p+a-H)/2.                                (1)

Since degree summation gives 2rho(D)=2e+p-2R, H is congruent to p+a
modulo two. Thus the signed exterior shortage satisfies

    epsilon(D)<=floor((p+a)/2),                          (2)

and D pays its p incoming half-units exactly when H>=p+a.
The same identity is the terminal form of the earlier component balance;
slack is a single budget, not a new resource added to that balance.

**Lemma 1 (automatic one-port compensation).** If D has p=1 and no
positive zero-capacity leaf, then rho(D)<=-1/2. Connectivity, acyclicity,
bounded diameter and any bound on cycle rank are unnecessary.

**Proof.** With a=0, H>=0 is odd, so H>=1. Apply (1). QED.

More generally a region with a=0 has rho<=0, and if p is odd it has
rho<=-1/2. In particular, a closed exterior remainder with no positive
zero-capacity leaf is automatically nonpositive. For disjoint source
patches satisfying the preceding local lemma, with tau=0, all residual
crossings marked lower exports, no exports between patches, and every
incident exterior component having exactly one port and a=0, Lemma 1
pays every beta edge once. If the whole deficient remainder has no such
positive leaf, no separate remainder-charge assumption is needed. This
proves coefficient one on this unbounded class, allowing bends and cycles.

The leaf exclusion matters. In the corridor construction with k>=2,
take the source row's left leaf and its k inner capacity-one tiles, omitting
the right leaf. This region has p=1,a=1,H=0 and rho=+1/2. The corridor is
feasible, normalized for neutral attachments and fork-free, while its whole
grid satisfies the target with slack. This refutes a one-port rule that
omits the leaf hypothesis. A two-port bent capacity-one receiver has a=H=0,
rho=0 and epsilon=1, attaining (2); its earlier all-length proof still applies.

## 2. The two ports of a capacity-one passage are adjacent

**Lemma 2.** In a feasible pair, a tile with r=1,d=2 has its two residual
matching endpoints at adjacent corners.

**Proof.** Write t for selected vertices, h for internal matching edges
and s for saturated attachments, so t+h+s=1. If t=1, then h=s=0 and the
two residual P corners cannot be diagonal: the T in either remaining corner
would see both. If h=1, the two internal endpoints occupy one tile side;
the other two corners form the opposite side. If s=1, the attachment
forces its side companion blank, by the saturated receiving tile's T
constraint. The other two corners, the residual endpoints, form the opposite
side. These exhaust the cases and prove adjacency. QED.

## 3. Cancellation with fixed boundary matching

Choose any tile region D. Freeze every matching edge except residual edges
with both tile endpoints in D. Form a directed auxiliary graph whose nodes
are those internal residual matching edges. Each has one black and one white
endpoint in the physical grid checkerboard coloring. Whenever the black
endpoint of edge f and the white endpoint of edge g are adjacent in the
same tile, put an arc f->g, labelled by that within-tile vertex pair.
There are no loops, since an internal residual edge joins distinct tiles.

**Theorem 3 (alternating circuit cancellation).** If this auxiliary graph
has a directed cycle of z nodes, remove its z residual matching edges and
add the z within-tile matching edges labelling its arcs. Then:

* the pair stays feasible, its selected set and entire occupied set stay fixed;
* the matching size and objective stay fixed;
* every tile charge, tile saturation status and saturated attachment stays fixed;
* every residual or saturated matching edge crossing the boundary of D stays fixed;
* z residual edges disappear. Each tile's capacity falls by the number of
  new internal edges there, and its residual degree falls by twice that number.

The cycle may visit a tile twice. Such a tile has capacity two and receives
two disjoint internal matching edges; no route visit is counted as a donor.

**Proof.** A directed cycle uses distinct matching-edge nodes. It uses each
black endpoint once as an arc's first endpoint and each white endpoint once
as an arc's second endpoint. The new edges therefore use exactly the old
endpoints, without repetition; all are legitimate within-tile grid edges.
Selected vertices and occupation do not change, so all T neighbor constraints
stay true. Every frozen matching edge keeps its endpoints and mate.

Let z_Q be the number of new edges in tile Q. Internal matching count rises
by z_Q and residual degree falls by 2z_Q. No selected or saturated-attachment
count changes, so r falls by z_Q and d/2-r is unchanged. Feasibility ensures
the new capacities remain nonnegative. A tile can receive at most two new
edges; receiving two requires all four corners among the deleted endpoints,
h=s=t=0 before the move, hence r=2. Saturation depends only on T and is fixed.
Every deleted edge is internal to D; boundary matching is untouched. QED.

Neutral-attachment eligibility is unchanged: occupied neighbor counts,
saturated attachment mates, tile neutrality and saturation are all fixed.
Hence a pair already normalized for those promotions stays normalized.
Positive zero-capacity leaves are unchanged, and each changed positive-capacity
tile retains its unused-slot count 2r-d. If its capacity becomes zero, its
degree is also zero and that count was already zero. Thus both a and H in
the terminal ledger stay fixed.
The residual topology and individual component charges may change because
components split; neither fork-freeness nor the old component identities are
claimed invariant. Geometric certificates depending on unchanged T/P/B labels
and saturated mates retain those data.

Repeatedly cancel any auxiliary directed cycle. Each step removes at least
two residual edges, so there are at most floor(e_initial/2) steps. A standard
directed-cycle search gives a terminating polynomial algorithm. No uniqueness
of the final matching is asserted.

At every step rho(D) and p are fixed, so its total signed shortage
p/2+rho(D) is fixed. If D splits, the sum of the new components' shortages
is the old shortage. This reduction simplifies cycles without manufacturing
new negative budgets or erasing genuine shared-port debt.

## 4. What an irreducible residual cycle must contain

**Corollary 4.** In a region with no auxiliary directed cycle, every simple
residual cycle has at least two tiles of capacity two at which its incident
matching endpoints are diagonally opposite. Parallel residual edges cannot
remain. Every residual cycle containing only capacity-one tiles is removable.

**Proof.** If all endpoint pairs on a simple residual cycle are adjacent,
they form the within-tile replacements of Theorem 3, giving a directed
auxiliary cycle in one orientation. Thus an irreducible cycle has a diagonal
passage. Capacity zero cannot have two residual incidences, and Lemma 2
excludes a capacity-one diagonal passage, so its capacity is two.

The tile grid is bipartite, so the residual cycle has even length z, including
the length-two parallel case. Traversing each matching edge reverses physical
checkerboard color. An adjacent tile passage also reverses color; a diagonal
passage preserves it. Returning to the start forces z plus the number of
adjacent passages to be even. Therefore the number of diagonal passages is
even, and at least two. In a parallel cycle both pairs lie on the shared tile
side and are adjacent, so it is removable. QED.

The classification is sharp. On a 4-by-4 grid select no vertices and match

    (0,1)--(0,2), (1,2)--(2,2),
    (3,2)--(3,1), (2,0)--(1,0),
    (0,3)--(1,3), (2,3)--(3,3).

The four tiles form one residual cycle. The two left tiles have diagonal
residual ports and capacity two; the two right tiles have capacity one.
The auxiliary graph is acyclic, so the move cannot remove this cycle.
Its charge is -2 and its objective is 6<=8. Embedding it with blank padding
and adding one port at the upper-left corner gives p=1, rho=-3/2 and a=0;
it remains irreducible with its boundary matching frozen. Failure to remove
a cycle is therefore not failure of compensation or of the grid target.

A second coordinate control consists of two neutral four-edge residual
cycles sharing one capacity-two tile. One auxiliary circuit removes all
eight residual edges, visits the central tile twice and adds two internal
edges there. After cancellation every participating tile is isolated and
neutral. A one-port version leaves exactly a half-unit at its receiving
tile. These controls distinguish circuits in matching endpoints from simple
cycles in tiles.

The remaining geometry is now sharper: shared ports, positive zero-capacity
leaves, irreducible diagonal capacity-two passages and saturated/inter-patch
exports require further compensation. The universal grid conjecture remains
open. The focused journal manuscript is preserved.

Run `python3 develop/check_residual_cycle_pruning.py --output output/residual-cycle-pruning-controls.json`.
The verifier checks the adjacency lemma, all cancellation invariants, fixed
boundary matching, terminal identities, one-port compensation, repeated-tile
circuits and sharp obstacles. Finite controls validate the written proofs;
no new Lean result or independent arbitrary-width Omega theorem is claimed.
