# Internal-consumer chains, fresh forced owners and zero-gain repairs

21 October 2026. This addresses the selected-consumer-outside-bases hypothesis
in the [packed batch theorem](SECONDARY_TEN_BATCH_TERMINAL_BUDGET.md).
There are arbitrarily long endpoint-disjoint dependency paths, with zero
signed contact remainder, for which the sum of the local baselines fails.
Completeness forces one fresh negative U per block, with no owner reuse.
Nevertheless a simultaneous family of fresh consumers has exactly zero
net gain because of occupied adjacent bands. These are partial-inventory
obstructions to proposed rules, not counterexamples to the complete-model
inequality or the global5/6 target.

## 1. The full-original chain

Fix n>=1. Choose independent even w_i>=12 and z_i>=24, an odd a_0,
an even s_0, and an even h>=6. For i=0,...,n-2 set

    a_(i+1)=a_i+z_i-6,     s_(i+1)=s_i-w_(i+1)-12.

Let A_i be the second prescribed eight-original residual with parameters
a_i,w_i,k_i=w_i+10,z_i, translated by (0,s_i). All transformations act
on the ORIGINAL matching, support and endpoint sets. In particular

    V_i=U(w_i+10,8,z_i),
    (r,c)->(a_i-6+r,w_i+12+s_i-c).

For clarity the complete A_i charts are below; add s_i to every column
in the last column. These are the existing residual originals, not new
replacement copies with reconstructed support data.

| Owner | Canonical dimensions | Chart at a=a_i,w=w_i, before column shift |
|---|---|---|
| Q | U(6,8,4) | (a+11-c,11-r) |
| D | U(w+4,10,4) | (a-2+r,5+c) |
| L | U(w,4,6) | (a+r,6+c) |
| C | U(8,6,4) | (a+6-r,w+6+c) |
| E | U(6,4,4) | (a+4-r,w+7+c) |
| W | U(6,4,4) | (a+1+c,w+1+r) |
| T0 | U(w+6,6,4) | (a-4+r,w+11-c) |
| V | U(w+10,8,z) | (a-6+r,w+12-c) |

Adjoin the north east-terminal rotor R_i=R_N at
t_i=(a_i+1,x_i), where x_i=w_i+14+s_i, and put B_i=A_i+R_i.
The unconsumed upper support is e_i=(a_i,x_i). Define the single root

    K=U(h,6,4), (r,c)->(a_0-6+r,w_0+13+s_0+c),
    H_0=(union_i B_i) union {K},     b_i=w_i+9.

**Chain obstruction theorem.** All9n+1 original endpoint sets in H_0
are pairwise disjoint, the B_i are disjoint actual-owner sets, and

    Phi(H_0)=sum_i b_i+h-1-n.                         (1)

The n new mixed full tiles outside the internal B_i are precisely

    T_i={a_i-1,a_i} x {x_i,x_i+1}.

Each has exactly the two directed events between (a_i,x_i) and
(a_i,x_i+1), one in each direction. Thus their total signed contribution
is zero and there is no further exterior event or full-tile remainder.

The actual upper U for B_0 is K. For i>=1 it is the already counted
owner V_(i-1). Indeed leg exchange rewrites that FULL original as

    U(w_(i-1)+10,z_(i-1),8),
    (r,c)->(a_i-z_(i-1)+r,w_i+13+s_i+c).

The recurrence gives both coordinate equalities. Even breadth and leg
lengths make leg exchange preserve the matching and ORIGINAL supports.
The resulting dependencies B_i->B_(i-1)->...->B_0->K form a path.

In particular n>h-1 gives Phi(H_0)<sum_i b_i, despite acyclicity and
zero signed exterior remainder. The deficit can be arbitrarily large
with the root fixed. Absolute Phi(H_0)=sum_i(w_i+8)+h-1 is positive.
This does not refute any complete-model target.

### General geometric proof

Separate the long far stem of V_i from the body of B_i. Every remaining
endpoint lies between rows a_i-6 and a_i+10. Every B_i endpoint has
column at least s_i+2. Its largest column is x_i+3, on its rotor.
The body of B_(i+1) starts at row a_i+z_i-12>=a_i+12, leaving no
shared endpoint tile or adjacency with the preceding body. V_i's near
stem and bar lie to the right or above that later body. Its far stem is
exactly the upper-right U in the later block's chart. The accepted
upper-right/north-rotor receipt gives only T_(i+1) and its two events.

For j>=i+2, the maximum B_j column is at most s_i-19, whereas every
B_i endpoint has column at least s_i+2. Thus nonadjacent bases have no
shared endpoint tile or adjacency. The root K is disjoint from B_0
by the upper-right receipt; it lies at columns at least x_0 and has no
contact with later blocks, whose largest column is at most s_0+5.
These facts prove endpoint disjointness and exhaust all cross contacts.

Each base has Phi(B_i)=b_i-1 by the accepted residual and north-rotor
receipts. K contributes h-1 once. Its contact with R_0 is neutral.
Adding the n neutral cross tiles proves(1). No mass for V_(i-1) can
be added a second time when it is selected by B_i: that actual original
already belongs to B_(i-1). This is the precise failure of extending the
packed formula without its outside-bases hypothesis.

## 2. Completeness forces n distinct fresh negative owners

For each block put

    p_i=(a_i+2,w_i+12+s_i)=(a_i+2,x_i-2).

**Fresh-owner lemma.** If a complete feasible original U/rotor family G
contains H_0, the actual owners P_i of the p_i are n distinct U originals
outside H_0. Every P_i has charge1-H_i, with even H_i>=6. Consequently
their negative mass, counted once per actual owner, is

    M=sum_i(H_i-1)>=5n.                             (2)

**Proof.** The point p_i is V_i's ORIGINAL support(8,0). It is absent
from B_i and its rotor. Every preceding block has minimum endpoint column
s_j+2=x_(j+1)>=x_i, while p_i has column x_i-2. Every later block
starts at row at least a_i+12. The root has columns at least x_0>=x_i.
Hence p_i is absent from H_0. The preceding body row maximum is only
bounded by a_i-8 when z_(i-1)=24; no stronger row separation is used.
Its three foreign endpoint neighbors are

    west:  V_i:(a_i+2,x_i-3),
    east:  E_i:(a_i+2,x_i-1),
    south: E_i:(a_i+3,x_i-2).

An unconsumed original support would have at least three occupied
neighbors, contradicting completeness. Its actual consumer must have
its own matching partner north, its only available own-neighbor direction.
The two north-tip rotors both contain E_i:(a_i,x_i-1), so neither can
be its owner. This is the same full-rotor collision used in the accepted
[depth-eight proof](SECONDARY_TEN_DEPTH_EIGHT_COMPLETE_EXCLUSION.md).
Thus it is a north-terminal U, in one of the two frames

    (r,c)->(a_i+2-d+r,w_i+11+s_i+c),
    (r,c)->(a_i+2-d+r,w_i+13+s_i-c),

with arbitrary even breadth H_i>=6 and depths d,f>=4. These frames are
even translations of the accepted upper-U frames, so q(P_i)=1-H_i.

All p_i have odd row and even column. The two leg terminals of ANY
legal U have opposite checkerboard colors: in intrinsic coordinates
their coordinate sums differ by f-d+H_i-1, an odd integer. This property
survives every integer grid isometry. Since p_i are distinct points of
the same checkerboard color, two of them cannot be terminals of the
same original. Thus all P_i are distinct and outside H_0. This proves(2),
with no copied source mass or reused terminal. In particular the weak
two-terminal capacity estimate is unnecessary here.

For their actual union P, persistence and exact set differences give

    Phi(H_0 union P)=sum_i b_i+h-1-n+M+2|F_new|-|E_new|. (3)

Here the new sets are differences against the full H_0 inventory and
include every P/base and P/P interaction. Therefore

    Phi(H_0 union P)>=sum_i b_i+h-1+4n+2|F_new|-|E_new|.

This is a source-mass and exact-ledger result. A favorable sign for the
new contact term is not assumed, and(2) alone is not a compensation theorem.

## 3. All n fresh consumers can have zero gain simultaneously

There is a general choice of the forced owners at p_i that is endpoint
disjoint from the entire H_0 and from every other such choice:

    P_i^0=U(w_i+12,10,4),
    (r,c)->(a_i-8+r,w_i+13+s_i-c),
    H_1=H_0 union {P_i^0:0<=i<n}.

Each P_i^0 consumes p_i and is a different actual full original. Yet

    Phi(H_1)=Phi(H_0)=sum_i b_i+h-1-n.              (4)

Here is the exact full-tile and event computation. Its original charge
is -(w_i+11). Its bar endpoint row a_i-7 is adjacent to V_i's bar
row a_i-6. Over the k_i=w_i+10 columns s_i+2 through s_i+w_i+11,
there are k_i/2 aligned full tiles, each with FOUR surviving directed
events. Neither direction targets an original support; the V target
has intrinsic row-1 and the P target row2 in a non-stem column. The V endpoints in
that band have no original support to the north, and the P bar endpoints
have no original support to the south in those columns. The band
therefore contributes signed value-k_i.

The remaining contact is with E_i in the near-stem column. It consists
of one three-endpoint tile at rows a_i-1,a_i and one full2+2 tile at
rows a_i+1,a_i+2, both in columns x_i-2,x_i-1. Its three events are

    E_i:(a_i,x_i-1)       -> P_i^0:(a_i,x_i-2),
    E_i:(a_i+2,x_i-1)     -> P_i^0:(a_i+2,x_i-2),
    P_i^0:(a_i+1,x_i-2)   -> E_i:(a_i+1,x_i-1).

Thus this contact has (DeltaF,DeltaE)=(1,3), signed value-1.
The total increment is exactly

    (w_i+11)+2*(k_i/2+1)-(2*k_i+3)=0.

These contacts cannot overlap different i. P_i^0 ends at row a_i+2;
P_(i+1)^0 starts at row a_i+z_i-14>=a_i+10. Every preceding B_j has
minimum endpoint column at least x_i, while P_i^0 has maximum endpoint
column x_i-2. Thus its entire preceding inventory is separated by at
least two columns, even when the endpoint row ranges meet. Later blocks
start at row at least a_i+12. P_i^0's far stem is in
column s_i+1, immediately left of V_i's column s_i+2, but those two
columns belong to different tiles; its only band contact is the one
already counted. The root is also two columns beyond P_0^0's near
stem, in a different tile column. This proves the disjointness and
exhaustiveness needed to sum the increments and proves(4).

**Explicit remaining incompleteness.** For every i,

    q_i=(a_i-3,s_i+1)

is P_i^0's original far axial support and is absent from H_1. It sees
the retained P_i^0 far terminal(a_i-4,s_i+1) to the north and V_i's
far-stem endpoint(a_i-3,s_i+2) to the east. Thus it must be consumed
in any complete extension. This proves H_1 is incomplete even though
all the p_i have been consumed. No nonextendibility is claimed.

## 4. Consequences and verification scope

The path family disproves the endpoint-only rules that acyclic internal
borrowing is safe, or that fresh negative consumers automatically provide
positive net repair. Both failures have exact general receipts. They do
not disprove the complete-model inequality: H_0 and H_1 are incomplete,
their absolute Phi is positive, and subsequent forced consumers may repair
the relative deficit. The outside-bases hypothesis of the accepted packed
theorem remains necessary for its stated formula.

The fresh-owner lemma also gives constructive positive information:
completeness forces n unused original-owner budgets, all distinct by
checkerboard color. The occupied-band computation explains exactly why
their charge cannot be used without debiting their contacts in the same
ledger. The next question is the actual q_i-consumer closure and its
joint signed remainder, not a new count of the already exhausted P_i^0
mass. The global5/6 improvement and rectangular-grid triple equality remain
open; the submitted11October manuscript is unchanged.

The general proofs above do not use an enumeration cutoff. The companion
checker reconstructs full ORIGINAL sources and verifies exact physical
full-tile and owner-labelled event SETS, including nonuniform chains.
The standalone Lean file verifies local coordinate, parity, budget and
renewed-support certificates. Complete ownership/role classification,
the general inter-block separation and final set partition remain ordinary
proofs; local formalization is not an end-to-end certificate.

Validation:96 exact chain/zero-gain set controls, three nonuniform chains
of7,12,24 blocks, eight tile-preserving isometries,288 full-original
terminal parity controls and24 full-original rotor exclusions PASS.
The8-block witness has baseline168 and Phi165, both before and after
the eight zero-gain consumers; the latter add mass184,96 full tiles and
376 directed events, giving184+192-376=0. It remains incomplete at
eight explicitly listed renewed supports.

All34 declarations, including24 theorems, in
[the standalone Lean source](../formal/SubQuorum/SecondaryTenInternalConsumerChains.lean)
pass locally with every individual axiom list checked, no warnings and
no sorry/native axioms. The [control receipt](../output/secondary-ten-internal-consumer-controls.json)
and [Lean receipt](../output/secondary-ten-internal-consumer-lean-validation.json)
record their precise scope. A separate written-proof review is ACCEPT,
with the preceding-block column-separation justification now explicit.
Focused controls check371 preceding-block/repair column pairs and12
cases where the preceding body reaches the repair's first bar row.
It does not stand in for either execution check; see the
[review receipt](../output/secondary-ten-internal-consumer-review.json).

The [renewed-support continuation](SECONDARY_TEN_RENEWED_SUPPORT_ESCAPE.md)
proves two further simultaneous zero-gain stages, excludes the long positive
escape in interior blocks, gives its exact negative tail debit, and constructs
a specified-owner compensation for the full chain. Its validation and written
review have separate scopes and records.
