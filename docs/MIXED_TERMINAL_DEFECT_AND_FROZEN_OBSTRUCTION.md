# Mixed-direction terminal defects, crossing-edge tax and frozen sharpness

26 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

We extend [terminal-port compensation](TERMINAL_DEFECT_PORT_COMPENSATION.md)
to arbitrary disjoint even-rectangle H/V partitions with every actual
matching edge restored. The extension needs a new seam-terminal defect: a
three-degree alpha terminal can have no BB port because its actual mate
runs along its local band axis across a change of direction. Each such
terminal charges a **different actual cross-direction matching edge**, once.

With occupied degree at least three at every global alpha terminal, let d4
count the degree-four terminals, b the ordinary local-axis/balanced-boundary
defects defined below, s the seam-terminal defects, and eHV the number of
actual M edges joining oppositely directed rectangles. The exact port graph
has D_port deficient paths and gives

    D_full <= D_port,
    2 D_port <= d4+b+s <= d4+b+eHV.                       (1)

The path/cycle matching mechanism is the existing allocation lemma; the new
geometry is the seam-terminal charge and its sharp frozen realization.
This is a single global allocation of original resources, including sources
created by restoring matching cuts. No local and interface reserve is spent
twice. In particular d4+b+s<=1 guarantees simultaneous zero-link payment of
every alpha. More generally

    S >= beta - floor((d4+b+s)/2),
    d4+b+s <= 2 beta+1  implies  |T|+|M| <= |grid|/2.     (2)

Thus the coefficient-one counting bound holds on this stated geometric
class. We do not prove a universal improvement of 5/6.

The eHV coefficient in (1) is sharp even for fully frozen true fixed-P
maxima with a unique actual matching and **every alpha terminal of degree
exactly three**, with d4=b=0. In an unbounded two-parameter family there
are eHV=2k crossings, s=2k, and full deficit k on the complete original
pool. The family also has an exact frozen repair frontier under arbitrary
reselection of T: complete repair requires net loss k, attained by opening
private body reserves at zero links. The same P admits zero-loss full
compensation by a different N, so it is not an obstruction after optimizing
the decomposition or a numerical counterexample.

## 1. Physical model and a missing term in the uniform argument

Partition an even-by-even rectangular board into disjoint axis-parallel
rectangles, each with both side lengths even. In each rectangle choose
horizontal two-row bands (H) or vertical two-column bands (V). Their local
auxiliary matchings combine into one perfect matching N. T is feasible:
every selected site has at most one neighbour in P union T, where P=V(M)
for the actual matching M. All actual M edges, including crossings, are
retained when determining global M/PP owners. Original BB/TT forest units
are extracted within each local band, with immutable region/band/forest
identities. Whole-owner support is the existing incidence to no-P gaps.
Use the complete original pool and the standard within-band TP-to-BP links;
extra justified links can only improve the bound in (1).

Only the occupied degrees of global alpha terminals are assumed >=3.
Interior endpoints and other owners need no additional degree hypothesis.
Full freezing is sufficient for these terminal degrees, but not necessary.

Every rectangle boundary coordinate is even. Indeed a horizontal line at an
interior row is tiled from column0 by intervals of even length; all endpoints
on that line are even. Apply the same argument to a vertical line for rows.
Thus rectangles of the same direction use the same auxiliary phase. A
crossing between two same-direction rectangles is not a phase discontinuity.

Fix a TP terminal v of a global alpha. Put n=N(v) in T, and let

    w=2v-n

be the other site on the N-normal axis; a site outside the board counts as
unoccupied. Write u for the unit vector along the local band axis. Since n
already sees v in P, feasibility forces both n+u and n-u blank whenever they
exist. Among the other three neighbours of v are w,v-u,v+u. Consequently:

- if degree(v)=4, neither adjacent axis column is BB;
- if degree(v)=3 and w is occupied, exactly one axis neighbour is blank;
- if degree(v)=3 and w is blank, both axis neighbours are occupied, so no BB port exists.

The third case is the new seam defect. In uniform bands an alpha terminal's
actual mate is w and that case cannot occur. Reusing that fact after changing
one region's direction would omit a genuine demand.

A physical port here is an adjacent BB column INSIDE v's own local band.
When degree3 and w occupied, the unique blank axis neighbour may lie outside
that band; this contributes one missing-local-axis boundary defect. If it
lies inside, its BB/TT forest may be balanced at a local lateral boundary;
that contributes one balanced-boundary defect. Let b be the sum of these
two counts. Positive boundary units are retained. We do not set b=0 merely
because v is away from the outer boundary of the whole board.

Let s count degree3 alpha terminals with w blank. This definition is disjoint
from d4 and b. It is a physical terminal count, not a new interval credit.

## 2. The seam-terminal injection into actual edges

**Lemma.** The map v -> {v,M(v)} from seam-defect terminals to actual matching
edges is injective, and its image consists of edges between oppositely
directed rectangles. Hence s<=eHV.

**Proof.** Since n is selected and w is blank, M(v) must lie along the local
band axis. If M(v) belonged to the same-direction auxiliary phase, then
N(M(v)) would be the adjacent site n+u or n-u. That site is blank by the
selected-site constraint above. Thus M(v) would be BP, and the actual edge
would already join the TP end v to a BP end: its owner would be mixed,
contrary to v being an alpha terminal. This argument also excludes different
rectangles with the same direction, since their phase agrees. The actual
mate therefore lies across a change of direction.

For injectivity, an actual edge can have only its two endpoints as preimages.
At v it is parallel to the local band axis. At its opposite-direction mate
p=M(v) it is parallel to the N-normal axis. Thus either N(p)=v, in which
case p is PP and cannot be an alpha terminal, or the opposite normal site
at p is v in P. In that second case p cannot be a seam-defect terminal.
So p is never another preimage. No edge is charged twice. QED.

This is stronger than charging up to two ordinary terminal incidences per
crossing edge. No count of CC relays, restored port cycles or regional slack
is added as a resource. Same-direction crossings contribute zero to eHV.

## 3. One global port graph and its consequences

Form the complete original BB/TT forest in each chosen band, keeping its
balanced boundary components as zero-capacity vertices. Each positive
forest is one capacity-one resource. Every global alpha is one edge whose
two terminal incidences attach to their BB forests, if ports exist. A terminal
without a port receives its own distinct zero-capacity dummy. Include all
positive original units, even if isolated, and retain loops and parallel edges.

At most one port is present at a terminal by Section1. A physical forest has
at most two alpha incidences: a port must be a BB endpoint of the forest,
and the immediately exterior TP column supplies at most one such incidence
on that side. A balanced forest has only one BB endpoint, since its other
end is TT at a local boundary; it has at most one incidence. Dummies have
one incidence. Therefore the multigraph has maximum degree two and all
zero vertices are ends of paths. The components are paths and cycles.

The zero incidences are **exactly** d4+b+s. Pairing two missing terminals
into one invented zero vertex would lose this identity; each has its own
incidence even when it belongs to the same alpha.

A path with m alpha edges and z in {0,1,2} zero ends admits exactly
m-max(0,z-1) payments to different positive vertices. A cycle admits one
payment per edge by cyclic orientation. These are the same elementary
path/cycle allocations proved in the uniform terminal note. In particular,
if D_port is the number of paths with two zero ends, then

    V_port=alpha-D_port,    2D_port<=d4+b+s.

Every assigned unit lies in that alpha's actual whole support. The assignment
is global across regions and restored matching cuts; each original unit is
used at most once. Its payments need no terminal links, gates or beta credits.
The complete fork-capable model can only pay more, proving (1).

Since L, the number of original units, is at least V_port, the exact full
ledger S=L+beta-alpha gives S>=beta-D_port and (2). This uses each beta
once in the ledger; it does not add a beta to an interval payment a second
time. The criterion is sufficient and does not claim every failed port
certificate is a full-network obstruction.

**Joint withdrawals.** Fix T,M,N and remove a set R of distinct positive
original units. For a cycle C let r_C count removed vertices. For a path C
let z_C be its initial zero count. The exact PORT deficit is

    sum_(cycles C) r_C + sum_(paths C) max(0,z_C+r_C-1).   (3)

The old proof applies to this new globally constructed graph. It is an upper
bound for full-network deficit on the remaining pool. It is not generally
an exact whole-support deficit; body reserves, links and beta forks can
improve it. Shared resource identities are removed once globally, not once
for every region, source or terminal that supports them.

## 4. Sharp full-pool frozen mixed-direction obstruction

Use the adjacent-module endpoint family `configuration(W,k)`, for even
W>=8,k>=1, with the unique actual matching M and the explicit true maximum
T*. Its board has rows0..W+1, columns0..10k+1 and

    tau=|T*|=(7k+2)W/2+3k+2,
    |M|=k(3W/2+5),   S=2k.

In module i put c=10i. Give its full-height rectangle of columns[c,c+4)
horizontal bands, and its rectangle[c+4,c+10) vertical bands. Give the final
outside rectangle[10k,10k+2) horizontal bands. This is an actual disjoint
even-rectangle partition. All cuts in M are exactly

    (1,c+3)--(1,c+4),    (W,c+3)--(W,c+4),

so eHV=2k. T*,P and M are unchanged: all endpoints stay frozen, M stays
unique, and |T*| stays the true maximum over ALL feasible selections on P.

The P vertices and M are as in the
[unique-mates theorem](FORCED_MATES_AND_ADJACENT_MAXIMA.md): columns4,5,6
at rows1..W; columns3,9 at rows1,W; columns7,8 at rows1,W-1,W, translated
by c. The M/PP body decomposition is identical to uniform vertical bands.
Indeed in columns0..3 the only P sites are the two column3 leaves, whose
N mates are outside P in either direction; all PP auxiliary edges lie in
the unchanged vertical slabs. Thus the complete vertical strand
classification from [perpendicular reserves](PERPENDICULAR_GUARDED_RESERVES_AND_JOINT_MAXIMALITY.md)
still applies to the bodies. Each module's only possible alpha is L_i,
containing all P in columns(c+4,c+5) and ordinary tips(1,c+3),(W,c+3).
The other open bodies are R_r at column c+6, r=2,4,...,W-4, and the final
bent R_end with tips(W-2,c+6),(W-1,c+8). The R_r partners are adjacent and
cannot both be selected; the latter R_end partner(W-1,c+9) has two fixed
P neighbours and cannot be selected. There is no unlisted alpha.

For T*, both L_i ends have selected horizontal N mates at(0,c+3),(W+1,c+3).
Each leaf also sees its actual P mate and its selected side neighbour at
column c+2; its other normal neighbour is blank because it has two fixed
P neighbours. Thus BOTH terminal degrees are exactly3, and both are seam
defects. There is no degree-four or ordinary boundary defect: d4=b=0,s=2k.

The alpha L_i has **empty whole support**, not merely no immediate ports.
Its only P columns in the horizontal slab are in the two terminal bands.
Their left no-P gaps have length3 and exactly3 selections each, hence no
original unit. Its only P band in the vertical slab is columns(c+4,c+5),
occupied by P at every row1..W. Its two outside single-column gaps at rows0
andW+1 are BT (column5 selected, column4 blank), also with no unit. There
are no other gaps incident to this body.

L_i has no non-self terminal exit: at a column3 end, its left neighbour at
column2 is selected and its right neighbour at column4 is an internal PP
vertex of the same body, not a BP terminal. Hence no length of path, mixed
relay or beta fork can pay it. All other owners and resources stay present.
At T* the exact inventory, inherited from the vertical R bodies, is

    alpha=k, beta=k, mixed=k(W/2-2), L=2k,
    V_full=0, minimum links=0, D_full=k.

Here L=2k also follows from S=L+beta-alpha and S=2k; nothing is withdrawn.
The port graph consists of k edges between their own two zero dummies, so
D_port=k. Thus 2D_full=s=eHV: the coefficient1 on eHV in (1) is sharp.
This refutes extending the degree-three/b=0 full-payment rule unchanged to
mixed directions. The failed rule is that port-geometry extension, not the
numerical coefficient-one inequality; S=2k remains positive.

## 5. Exact arbitrary-T profile and frozen repair frontier in this mixed N

Fix the same P,M and mixed N, but allow ANY feasible final T with the four
leaf seals per module

    (0,c+3),(1,c+2),(W,c+2),(W+1,c+3) in T.

These are equivalent to freezing the two specified column3 leaves, by the
first-freezing-time argument in the
[frozen exchange theorem](FROZEN_SELECTION_REPAIR_FRONTIER.md). Full freezing
is sufficient. No old selections must survive. The same body classification
makes every L_i alpha, with exactly degree3 ends, while no R body is alpha.
No source has a terminal exit.

Use the same disjoint cap cover of total tau from the fixed-P maximum proof.
Let h_i be the sum of losses in its four **unreplaced** aligned tiles at
upper-left coordinates

    (0,c),(W,c),(0,c+4),(W,c+4).

The first two have cap2; the last two have cap1. Then

    |whole support of L_i| = h_i,
    V_full = number of i with h_i>0,
    D_full = number of i with h_i=0,  minimum links=0.    (4)

**Proof.** The seals force outer column c+2 blank. Thus each length-three
terminal gap in the H slab has exactly1 plus the number of selections in
its cap2 tile; its unit count is the cap2 tile loss. The outer column c+4
site is blank because its adjacent seal at column c+3 already has a P
anchor. The outside one-row gap in the vertical(c+4,c+5) band is therefore
BB exactly when its column5 site is absent; its unit count is the cap1
source-tile loss. These four gaps are all the body's support, as in Section4.
Each is incident only to L_i, even relative to other open owners: its
horizontal band has no other P, and its vertical band has no other owner.
Different i use different physical bands. Hence all these supports are
private, and a source with any one unit is paid directly, while a source
without one has no route out. This proves (4). QED.

All four charged tiles are distinct across i and avoid the cap3 replacement
patches, whose left columns are c+2. Nonnegative losses in the whole disjoint
cover sum to ell=tau-|T|, so

    ell >= sum_i h_i >= number of i with h_i>0 = k-D_full,
    ell+D_full >= k.                                   (5)

Thus every fully frozen true maximum still has deficit k in this genuinely
mixed decomposition, under arbitrary replacements of T. For integer0<=d<=k,

    max {|T| : fully frozen, D_full<=d} = tau-k+d.        (6)

For attainment delete (0,10i+5) from T* in any k-d modules. Each deletion
opens the private upper BB singleton in the unchanged vertical(c+4,c+5)
band, so h_i=1 there and0 in every other module. All k alpha sources remain;
V=k-d,D=d and all payments use zero links. The inventory is unchanged and
L=2k+(k-d). The common prefix-plus-uniform freezing schedule in the prior
exchange note works without ANY upper central partner and freezes all
endpoints. Its validity is independent of N: each deleted site could witness
only the already-prefrozen endpoint(1,c+5). Therefore these attainers remain
fully frozen for every W,k and every deletion subset. This proves (6).

Unlike a sum of separately assigned local reserves, (4) counts actual
original units in private supports; (5) charges different physical cap
members. The full-payment lower bound is a net point loss, not merely a
necessary number of deleted old selections.

## 6. Scope, verification and next geometric question

The universal5/6 improvement remains open. Criterion(2) is a coefficient-one
result on the explicitly stated mixed-direction defect class. The sharp
family disproves an uncorrected generalization of the three-degree terminal
rule and shows that full freezing and fixed-P maximality do not remove
cross-direction seam defects. A globally vertical N pays the same P,T*
without loss, so the family does not defeat optimization over decompositions.
Finding a valid partition that jointly controls b,s and terminal d4 is still
the geometric task; minimizing only the number of M crossings ignores local
axis boundary defects and the actual changed terminal identities.

The written proofs above have no size bound and use no enumeration. The
solver-free checker `develop/check_mixed_terminal_defect.py` independently
extracts physical forests, reconstructs each terminal's zero category,
verifies the injective actual-edge charge and global path/cycle allocation,
and checks the exact withdrawal formula against independent matching and
full fork-capable flow. It tests horizontal/vertical cuts, four-region
partitions and independently oriented2-by2 tiles. The family checker permits
arbitrary T rebuilt from only leaf seals, replays a strict rank schedule on
sharp frozen attainers, and rechecks its serialized fixture.

Lean scope and permanent receipts are recorded alongside
`formal/SubQuorum/MixedTerminalDefect.lean` and
`output/mixed-terminal-defect-{validation,formal-validation}.json`. The general
coordinate-to-forest/owner adapter and the complete grid freezing theorem
remain written/executable components, not an end-to-end Lean claim.

The recorded controls pass330 physical partitions (52 with positive seam tax),
243 nonvacuous complete zero-link port certificates,256 nonvacuous numerical
criteria and122 joint original-unit withdrawals. The mixed family passes326
models, including240 arbitrary selections rebuilt from only seals,85 sharp
frozen repair attainers and20 unrepaired sharp obstructions. There are36
independent primitive-optimum comparisons and33,052 strict freezing events.

Local Lean4.33.0 passes16 individual declaration audits without warnings,
placeholders, native evaluation or new axioms. It covers local degree and
zero-category identities, the physical parallel-partner exclusion, abstract
matching-edge charge injectivity, the seam/numerical bounds, and arbitrary-
length private-support loss induction. The complete coordinate, forest and
path-allocation adapters are explicit written/executable dependencies.
