# Forced width-five stacks and their joint compensation

22 October 2026. Wenlin Zhang and Haobo Ma. General written proof;
finite controls, scoped Lean and independent review have separately recorded
states. All hypotheses are those of the
[sealed-cavity theorem](SECONDARY_TEN_SEALED_ROOT_CAVITY.md), including the
explicit full-even-U/standard-rotor model and immutable original supports.
This is not arbitrary-grid catalogue exhaustion.

Let J3 meet P1 and suppose its cavity has width5, equivalently
D3=u+v+18. Write

    T=a-12, Q=a+z-15, c=s1+1, N=Q-T+1=z-2.

The cavity C=[T,Q] x [c,c+4] is initially endpoint-empty. T and c are
odd, Q is even, N>=22 is even. Its complete outside walls belong to B
(left and top), J3 (right), and P1 (bottom). The original B supports
inside C are exactly (r,c) for even r in [T,Q]. No other retained
original has an original support in C. The preceding coordinate charts
give these facts: every staircase original support has column at least
its bar start, which is at least c+5. The depth steps imply L<=v-2,
so A and the first H3 block lie farther right; the P1 bar and other
later-block originals and their supports start below Q in this column range.

## The forced-stack theorem

In any complete extension, the entire set of endpoints inside C is a
stack of k>=1 full U(H_j,4,4) originals, whose even heights satisfy

    H_j>=6, sum_j H_j=N.

Every bar occupies the LEFT two columns c,c+1. Each original fills all
five columns of its top and bottom rows. Starting from bottom Q, its
chart is

    (r,column) -> (Q_j-H_j+column,c+r),
    Q_1=Q, Q_(j+1)=Q_j-H_j.

The bands partition [T,Q] without gaps or overlap. In particular
6k<=N. No other original can have any endpoint in C. This is a
necessary classification in every complete extension. It does not assert
the existence of an extension outside C.

### The corner consumer has only two possible forms

The lower-left corner q=(Q,c) is an original B support and has occupied
neighbors in the left and bottom walls. It must be an endpoint of a fresh
original; the full-wall path argument confines that original to C.

A rotor has no endpoint at any corner of its bounding rectangle: its
extreme row/column pairs are not jointly attained. This remains true
under every lattice isometry. Since q is both a lowest-row and a leftmost-
column endpoint of its consumer, a rotor cannot contain q inside C.

A full U with an untransposed horizontal bar needs at least six columns.
In a transposed orientation it has max(d,f)+1 columns. The width5 cavity
and even d,f>=4 therefore force d=f=4. Its horizontal projection fills
all five cavity columns. Its vertical bar has even height H>=6, ends at
row Q, and begins at Y=Q-H+1. Thus only two endpoint sets are possible:
the two-column bar is at c,c+1, or at c+3,c+4. Both have complete
five-point stems at rows Y,Q. The argument uses actual projections and
the extremal corner; it does not impose an enumeration cutoff.

These normal forms preserve the full immutable data. For even H, reversing
the canonical long axis by column -> H+1-column preserves U(H,4,4).
Each row-zero matching pair starting at odd column j maps to one starting
at odd H-j; each internal row-one pair starting at even j maps to one
starting at even H-j. The two equal stems and their matching edges are
exchanged. The two bar-exterior supports, two axial supports, and each
even/odd lateral-support pair are likewise exchanged. Thus long-axis
reversal introduces no additional matching or original-support phase.

### The right-bar form is impossible

Suppose the bar is at c+3,c+4. Its empty inner notch is

    C'=[Y+1,Q-1] x [c,c+2].

Its four entire outside walls are B's left stem, the new bar at c+3,
and the new full top/bottom stems. Because Y is odd, the point
q'=(Y+1,c) is an original B support. It is absent from the retained
originals and the proposed consumer, and already has two occupied
neighbors: (Y+1,c-1) in B and (Y,c) in the consumer's top stem.
Completeness requires a further original containing q'. That original is
trapped in the width3 notch, contradicting the general projection
obstruction. This excludes every right-bar height, including the partial
inventories whose individual signed marginal was negative.

### Recursion and exhaustion

The consumer must therefore have its bar on the left. Its inner notch is
[Y+1,Q-1] x [c+2,c+4], again width3, with complete walls from its own
bar/stems and the retained J3 bar at c+5. No further original can have
an endpoint there: a connected owner entering it would be trapped in
three columns. The consumer occupies everything else in its own height
band.

If Y=T, the whole rectangle is exhausted. Otherwise the remaining upper
rectangle is [T,Y-1] x [c,c+4]. Its height N-H is even. Its lower wall
is the consumer's full top stem; the other walls remain occupied. The
new lower-left corner (Y-1,c) is again an even-row original B support
with occupied left and below neighbors. The same two-form classification
and right-bar exclusion apply. A positive remaining height below6 is
impossible. Each step removes at least six rows; hence finite descent
ends with exactly a partition of N into even heights at least6. All
remaining inner notches are too narrow for any additional original.

## Exact ledger for the entire forced stack

Let S denote the old selected prefix H3+B+R+A+J0+J1+J2+J3 and let
K be the forced stack. Relative to the SAME immutable physical tiles,
original supports and directed-event definition, the exact increment is

    Phi(S union K)-Phi(S)=N/2-k-4.                (1)

This identity holds for every actual staircase satisfying the hypotheses,
not only for the earlier geometric equality family. New endpoint tiles
can meet old endpoints only along B's top/left walls and P1's bottom
wall. The right wall lies in the next physical tile column. Thus other
retained originals introduce no omitted same-tile receipt.

For each U(H,4,4) in this phase, there are H+3 immutable matching edges,
H+4 endpoint tiles, and6 original supports inside those tiles. Its charge
is (H+3)+6-2(H+4)=1-H<0. The stack therefore adds N-k negative mass
and no positive-owner count.

The full new mixed-tile set is a disjoint union of three tile columns:

* The B-left-wall column has N/2+1 full tiles, including its top/bottom
  boundary tiles.
* The two inner physical tile columns each have k+1 full tiles: one at
  the upper wall, one at the lower wall, and one at each of the k-1
  interfaces between consecutive originals.

Thus there are N/2+2k+3 new full tiles. Every tile was nonfull before
the stack because C was endpoint-empty. The corner tiles with three
owners are each counted once in this physical-tile partition.

The entire new directed foreign-event set has the following disjoint
edge groups:

* Across the left wall: every new endpoint points to B (N events);
  B points back only on odd rows (N/2 events), since its even-row
  targets are ORIGINAL B supports and are excluded from events.
* Across the top wall: B points down at all5 columns; the new original
  points up only at c+1,c+3, its other three targets being its own
  original supports. Total7.
* Across the bottom wall: P1 points up at all5 columns, and the new
  original points down only at c+1,c+3. Total7.
* At each internal interface, each original points to the other only
  at c+1,c+3; the remaining targets are its own original supports.
  Total4(k-1).

There are therefore 3N/2+4k+10 new events. Substituting the three
exact inventories yields

    (N-k)+2(N/2+2k+3)-(3N/2+4k+10)=N/2-k-4.

No old charge changes, no previously credited tile is used again, and
each new tile/event is included in exactly one group. This is a joint
ledger, independent of the order in which stack originals are added.
In particular its top tile row also occurs in the preceding upper ledger,
but its three tile columns lie strictly left of b3=c+5. All its counted
new tiles contain a previously empty cavity site and were nonfull before.

Since N>=22 is even and 6k<=N, (1) is at least4. The width5 selected
prefix already has DeltaPhi>=L/2+7, so its enlargement by the forced
stack has

    DeltaPhi(S union K)>=L/2+11>=14.             (2)

The lower bound4 for the stack is attained geometrically at N22,k3
(heights6,6,10), and at N24,k4 (all heights6). This is not a claim
of global complete extendibility or optimality of (2).

## A twelve-unit selectable-group consequence

Every complete-extension prefix in the stated staircase branch has a
specified enlargement with joint gain at least

    L/2+9>=12.                                  (3)

If J3 meets P1 and W5, add exactly its forced cavity stack and use (2).
If J3 meets P1 and W>=7, leave the prefix unchanged: D3<=u+v+16 and
the accepted bound u+v+L/2+25-D3 gives L/2+9. Widths1/3 are already
excluded, and the width is odd. If only J1 meets P1, the accepted
stronger branch gives L/2+9. With no P1 contact, the bound is at least
L/2+14. These cases exhaust the branch.

Equation (3) concerns ONE chosen group. Allocation among overlapping
root groups remains OPEN; a forced stack cannot automatically be credited
to two groups. No claim is made that arbitrary additional originals have
nonnegative marginals or that a whole complete family satisfies (3).
Global5/6 improvement and rectangular-grid triple equality remain OPEN.

The quantifiers fix a complete extension first, then select its actual
forced stack in the width5 case. The height partition can depend on that
extension; no single predetermined stack is required in every extension.

## Simultaneous cavity compensation without reusing credits

There is also a precise sufficient condition for allocating the NEW stack
contributions among multiple groups. Suppose a single retained endpoint
inventory S contains m cavities satisfying the hypotheses above, and their
physical tile footprints are pairwise disjoint. For a cavity with top T,
bottom Q and left c, that footprint is the integer tile rectangle

    [(T-1)/2,Q/2] x [(c-1)/2,(c+3)/2].

Every added endpoint, every new source's endpoint tile, every new full tile
and every new directed event lies in its own cavity's footprint. Every
outside cell in a tile meeting the cavity is an already occupied retained
wall cell; hence other retained originals cannot change the local receipt
partition. Disjoint footprints preclude a shared new tile or a same-tile
event between different stacks. The source charges are immutable and the
fresh originals are disjoint. Consequently, for the actual forced stacks
K_j in any complete extension,

    Phi(S union all K_j)-Phi(S)
      =sum_j (N_j/2-k_j-4) >=4m.                (4)

No disjointness between the OLD boundary-owner lists is needed beyond the
stated hypotheses: an old owner may supply several walls, but its charge
is not credited anew and its events belong to distinct physical tiles.
This gives a simultaneous inequality for the stack contributions; it does
not add the overlapping original-prefix lower bounds from (3).

For cavities attached to distinct eligible roots of the retained H3 chain,
c_j=s_(j+1)+1. Since s_(j+2)=s_(j+1)-w_(j+2)-12 and w>=12, consecutive
left coordinates decrease by at least24. Their three-column physical tile
footprints are therefore disjoint regardless of overlapping row ranges.
The same separation holds for nonconsecutive roots. This is a separation
certificate conditional on those eligible root configurations coexisting;
their coexistence and the allocation of the OLD prefix reserves are not
asserted. The independent stack review input predates this simultaneous
corollary; its review status is recorded separately.

## Local support closure and remaining obligations

For any such height partition, the stack leaves exactly two unconsumed
new supports per band, at (Y+1,c+3) and (Q_j-1,c+3). Each has just
its adjacent stem endpoint as an occupied neighbor: these supports are
mutually nonadjacent and lie strictly inside C. All even-row B
supports at c are consumed. Every new support outside C is consumed by
a wall or a neighboring band. No unconsumed old support outside C gains
a neighbor: every site immediately outside C is already a wall endpoint.
Thus the construction closes all support obligations inside this cavity
and introduces no exterior support violation. Existing exterior
obligations can persist, so this does not construct a complete global
extension.

The all-parameter corner classification, recursive trapping and physical
receipt partition above are the proof. Finite enumeration is used only to
test them. Lean scope is reported separately; no claim of a fully formalized
catalogue or complete-family theorem is implied.
