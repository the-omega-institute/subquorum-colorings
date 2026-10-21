# An exact contact ledger and a three-original two-gate obstruction

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Scope

This note advances the external-old question in
`ALIGNED_BAR_BATCH_COMPENSATION.md` in a different, explicitly restricted
family. The contact ledger allows any finite collection of south-going,
horizontal full U originals with even bar top rows, even breadth B>=6,
and even leg depths d,f>=4. Horizontal translations can have either parity;
vertical translations preserve the even bar phase. All endpoints are
pairwise disjoint, and original supports/matchings remain immutable.
There is no arbitrary extra baseline in the ledger theorem.

The subsequent nonextension theorem allows any orientation of every new
full U and every standard rotor. It uses the same complete-extension rule
as the earlier four-original obstruction: an original support absent from
the endpoint union must have exactly one occupied neighbour if it remains
unconsumed. Thus two retained endpoint neighbours force its occupation by
an additional original. No catalogue exhaustion for arbitrary grids is
asserted. The new lemma needs just three retained U originals.

## Exact even-bar contact ledger

For the U with chart (t+r,L-1+c), its endpoint columns range from L through
R=L+B-1, and its leg tips are at even rows t+d,t+f. Call it positive if
L is odd (R even), and negative if L is even (R odd).

With k=(d+f)/2, direct counts of matching edges, endpoint tiles and original
supports inside those tiles are respectively

    positive: B-1+k, B/2+1+k, 4+k;
    negative: B-1+k, B/2+k,   k.

Thus their charges are +1 and -1, respectively. Each contributes exactly
one to N+S in Phi=N+S+2F-E.

Define a finite multigraph G on the originals. For every positive/negative
pair, include one edge per physical tile COLUMN in which their endpoint
footprints meet. Two originals can give two parallel edges; these are two
different physical bands, not a repeated charge for one band. Positive/
positive contacts give no edge. Negative/negative contacts cannot occur.
Then, with c(G) the number of components including isolated vertices and
mu(G)=|E(G)|-|V(G)|+c(G) its cycle rank,

    Phi = |V(G)|-|E(G)| = c(G)-mu(G).                         (1)

Every positive vertex has multigraph degree at most two. In particular,
each tree component contributes exactly1, each unicyclic component0, and
a component with two or more independent cycles has negative contribution.

### Proof of the receipt partition

Every odd-row endpoint has the preceding even-row endpoint of its OWN
original in the same column. Therefore at most one original can occupy
either column of a physical tile: if another owned the odd cell, it would
also own the already occupied even cell. A tile has at most two endpoint
owners. The same property excludes all vertical intratile cross events.

Negative bars fill their entire aligned tile-column interval. The aligned
bar packing lemma proves that any two endpoint-disjoint negatives have
disjoint entire endpoint-tile footprints. The interior tiles of a positive
bar are full within that original. Thus any shared tile lies on an exposed
vertical boundary leg of a positive and another original. For a fixed pair
and tile column, the common endpoint rows form a nonempty continuous
interval [u,w], with u,w even. There are j=(w-u)/2 full shared tiles, and
one terminal tile containing the two even top cells. Its missing odd cell
cannot be filled by a third original, by the same own-predecessor property.

For two positives the adjacent legs are both outward-facing. Their events
toward one another survive precisely at odd rows: even-row directions target
their own original lateral supports (including bar-end supports). There are
2j events, including none at the terminal even row, so 2F-E=0 for this band.

For a positive/negative pair, the positive direction is outward and survives
at odd rows; the negative direction is inward and survives at even rows.
The negative bar must precede the positive bar: if its top lay in the
positive stem interval, its full bar would collide with that stem. Thus
the negative direction always has the stem's stated support phase, including
the positive's first row. There are exactly2j+1 events, giving 2F-E=-1.

All full mixed tiles and all cross events are partitioned by these unordered
source pairs and tile columns. No tile has a third owner and every event
retains its source label. Adding each source's one unit proves the first
equality in (1); the second is the finite multigraph cycle-rank identity.

Finally, a negative sharing a positive boundary must have its bar before
the positive bar and contain the cell immediately across that boundary at
the positive bar's top row. Two negatives on the same positive boundary
would own that same cell. There is at most one negative per boundary,
proving degree<=2. This bounds contacts per POSITIVE, not per negative.

### Exact old/new boundary term within this restricted family

Partition such an inventory into retained originals B and new originals S.
Let e(S) count contact edges with both ends in S, and e(S,B) those crossing
the partition, retaining parallel bands. Subtracting (1) for B from (1)
for B+S gives the exact marginal

    DeltaPhi(S | B)=|S|-e(S)-e(S,B).                         (1a)

Thus the old/new adjustment in this family is exactly minus the number
of old/new positive/negative contact bands, with no unknown full-tile
correction. This uses the even-bar own-predecessor property for EVERY old
original as well as every new one; it does not apply to arbitrary old
rotated, odd-bar or rotor inventories in the earlier root-pair theorem.
If S is a union of whole contact components of B+S, the boundary term
vanishes. Every selected tree component then contributes1 and every selected
unicyclic component0. Such a selection has nonnegative marginal whenever
each selected component has cycle rank at most one. This is a sufficient
nonreusing compensation rule; the nonextension lemma below excludes one
specific family that violates its cycle-rank condition.

## A nested multicyclic family, and why its negative budget is not actual

For every n>=1 take the negative outer source

    A_n=U(8,8n+4,8n+4), chart(r,c-1),

with endpoint walls at columns0,7, and positive inner sources

    B_i=U(6,4,4), chart(2+8i+r,c), 0<=i<n.

Their endpoint sets are disjoint. Each B_i has both boundary bands adjacent
to A_n. Distinct B_i have disjoint endpoint-tile rows. Hence G is one
negative vertex with n positive vertices, two parallel edges to each one,
and no other edges. Formula (1) gives the exact partial-union identity

    Phi(A_n+B_0+...+B_{n-1})=1-n.                             (2)

There is nevertheless no complete full-U/rotor extension for n>=2.
The following local theorem proves this from only A_n,B_0,B_1. It does
not discard (2); it distinguishes a negative partial ledger from a
realizable complete-family obstruction to the target.

## Three-original two-gate nonextension theorem

Fix even a>=2. Retain the originals

    A=U(8,D,F), chart(r,c-1), D,F even >=a+6;
    B=U(6,4,4), chart(a+r,c);
    C=U(6,d,f), chart(a+8+r,c), d,f even >=4.                 (3)

These are endpoint-disjoint. Additional retained originals are permitted
if endpoint-disjoint; they cannot repair the following contradiction.
No complete extension by full even U/standard-rotor originals in arbitrary
lattice orientations can contain (3). The conclusion is invariant under
every translation and square-lattice isometry.

### Both gates are forced

The axial original supports of B are

    p=(a+5,1), q=(a+5,6).

Both are absent from the endpoints of (3). Point p has retained north and
west neighbours (a+4,1),(a+5,0), and q has retained north and east neighbours
(a+4,6),(a+5,7). Each must be occupied by an additional original. At p, the
only possible internal endpoint directions are east and south. At q they
are west and south. This also covers an owner that another additional
retained source has already placed there: it still must avoid (3).

### Every full U owner at p is impossible, with no dimension cutoff

Inspect the endpoint-induced graph of a full U. Its degree-three bar/branch
points cannot fit two free directions. Its degree-two straight-leg points
require opposite directions. The only remaining roles at p are its outer
bar corner with directions east/south, or a terminal directed east or south.

At an east/south corner, either its bar goes east and a continuous leg goes
south, or its bar goes south. In both cases minimum depth4/breadth6 forces
the endpoint (a+8,1), which belongs to C's bar.

A south-terminal role likewise has a continuous stem through (a+8,1),
because even minimum depth4 places its inner bar at least three steps away.

For an east-terminal role let its even depth be k>=4. A depth k>=6 forces
the retained wall point (a+5,7). If k=4, the outer vertical bar is at
column5, with its near end at row a+5. Its breadth>=6 forces it to meet
either B's row-a bar (if it extends up) or C's row-(a+8) bar (if down).
Thus every terminal and corner role is excluded. Horizontal leg exchange
or lattice reflection introduces no other endpoint role. This proves the
full-U exclusion uniformly for arbitrary breadths and far depths.

### The two remaining rotor choices cannot coexist

Normalize a=0 just for the following coordinate lists. All endpoint-induced
degrees of a standard rotor are one or three. Thus at p=(5,1) it can only
be an east or south terminal. The two south-terminal patterns contain,
respectively, (6,0) on A's wall or (8,2) on C's bar, and are excluded.
The only remaining endpoint sets are

    L_up={(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)},
    L_down={(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)}.

The only possibilities at q=(5,6) are their reflections R_up,R_down under
(row,column)->(row,7-column). One rotor cannot own both p and q: its
endpoint-column span is3, whereas their column separation is5. The two
required originals would therefore have to be distinct. But every possible
pair shares endpoints:

| Left choice | Right choice | Retained common endpoints, relative to a |
| --- | --- | --- |
| L_up | R_up | (4,3),(4,4) |
| L_up | R_down | (4,4),(6,3) |
| L_down | R_up | (4,3),(6,4) |
| L_down | R_down | (6,3),(6,4) |

Distinct originals must have disjoint endpoints, a contradiction. This
proves the nonextension theorem and excludes every n>=2 instance of (2).
It does not exclude all multicyclic contact graphs or prove that (1) is
nonnegative in arbitrary complete even-bar inventories.

## Validation and next proof target

`develop/check_even_bar_contact_ledger.py` verifies1006 disjoint source
pairs,40 deterministic greedy batches and five nested families through n12.
It compares exact full/event partitions, two-owner tile occupancy, contact
multigraphs, positive degrees and cycle ranks. The obstruction checks648 U
roles across every symmetry,32 rotor roles, exactly two surviving shapes
per gate and all four unavoidable collision pairs, plus three controls
with large outer depths and distant vertical translations of the local gate.
Finite controls supplement the general proofs above.

`formal/SubQuorum/EvenBarContactObstruction.lean` formalizes the normalized
blocked geometry, all-parameter U role collisions, reflection, south-rotor
exclusion, all four remaining rotor-pair collisions, and final ledger
arithmetic. Lean4.33.0 passes16 explicit declarations/11 local theorems,
each individually axiom-audited with ordinary axioms only, no warnings,
sorry or native evaluation. The full original-source-to-role classification, forced-owner
adapter, contact event counts and multigraph interpretation remain written
proofs. The formal source does not encode an unrestricted grid catalogue.

The next question is which other multicyclic even-bar contact components
are excluded, and which force new rotated or odd-bar owners that compensate
their deficit. Arbitrary external-old adjustments, mixed orientations,
full-family allocation, the global5/6 improvement and rectangular-grid
triple equality remain open. The submitted11October manuscript is unchanged.
