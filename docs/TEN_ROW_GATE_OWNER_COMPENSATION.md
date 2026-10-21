# Actual gate owners and simultaneous compensation at spacing ten

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model, statement, and limits

Every original is a full U of even breadth at least six and even depths at
least four, or a standard eight-endpoint rotor, in any lattice orientation.
Different originals have disjoint endpoint sets T; their original supports H
and matchings M are immutable. In a complete extension, an original support
outside the endpoint union has exactly one occupied neighbour. In particular,
two retained endpoint neighbours force a different original to consume it.
The existence of this source decomposition is an explicit hypothesis.

Fix even W>=6, even a>=2, and n>=2. Retain

    A=U(W+2,D,F), chart(r,c-1),
    B_i=U(W,4,4), chart(a+10i+r,c), 0<=i<n,
    D,F even >=a+10(n-1)+4.                                  (1)

For each i<n-1 let p_i=(a+10i+5,1) and q_i=(a+10i+5,W).
In any complete extension, select the actual original owners of these
two points, counting one owner just once if it consumes both. Owners
selected at different i are distinct. Let K be (1) and all these owners.
Then, for the usual immutable, source-labelled inventory,

    Phi(K)>=3(n-1).                                         (2)

At W=6 the stronger Phi(K)>=4(n-1) holds. The theorem also classifies
every owner at p_i, without a dimension cutoff, and gives the exact joint
increment at each gap. It does not assume two different owners per gap.

This is a selected-inventory theorem, with exactly the baseline (1).
It does not assert that (1) has a complete extension, or that arbitrary
remaining originals have nonnegative marginal. It neither proves a global
5/6 improvement nor settles the rectangular-grid parameter equalities.
Unlike the preceding spacing-eight seed, spacing-ten nonextension has not
been proved. Its complete realizability remains open.

## Exhaustive owner classification

Subtract a+10i from rows. The fixed bars of B_i and B_(i+1) occupy
rows0,1 and10,11, respectively. Their stems are in columns1,W through
rows4 and14. The outer walls are at columns0,W+1. The forced point
p=(5,1) is B_i's original axial support, absent from these endpoints;
its north/west neighbours (4,1),(5,0) are occupied. Only east/south
can be internal endpoint directions of its owner.

The endpoint graph of a U has only terminals, straight stem points,
outer bar corners and degree-three points. Straight or degree-three
roles cannot fit these free directions. A rotor can only be a terminal.

An east terminal of a U has even near depth k>=4. If k>=W its
continuous stem crosses the opposite wall (5,W+1). Otherwise its bar
is in an interior column. A bar pointing up has breadth>=6 and hits
B_i at row0; a bar pointing down hits B_(i+1) at row10. Thus this
role is impossible at every permitted dimension.

At an east/south outer corner, a south-going bar of breadth>=6 hits
row10. The bar must go east, with a south-going near stem. A near
depth>=6 hits row10, so its even depth is four. Its even breadth b
is at most W, since a longer bar crosses the opposite wall. Its far
stem also points south, and a depth>=6 hits row10. This gives exactly

    D_b=U(b,4,4), chart(5+r,c), even 6<=b<=W.                (3)

A south terminal has even near depth d>=4. Its outer bar is at row5+d.
If d>=6 its stem crosses row10. Hence d=4, the outer bar is in row9,
and the inner bar is in row8. The bar must point east, since a
west-going bar hits the wall. Again its even breadth b is at most W.
The far stem points north. A far depth>=8 crosses B_i's row1, so
it is four or six. At b=W, depth six already hits B_i's right stem
at row4. We obtain exactly

    U_b=U(b,4,4), chart(9-r,c), even 6<=b<=W;
    V_b=U(b,4,6), chart(9-r,c), even 6<=b<=W-2.             (4)

All the displayed full records avoid the fixed endpoints. Canonical
stem exchange, reflection and rotation introduce no further roles or
records; matching and support records are carried by the same chart.

Both south-terminal rotor records hit column0 (one contains (7,0),
and the other contains (6,0)). The two east-terminal records are

    H={(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)},
    L={(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)}.   (5)

Their supports and matchings are those of the canonical rotor, not
reconstructed from the displayed endpoint sets. Thus (3)--(5) are
the exhaustive full-record list for the actual owner of p. Reflect
column c to W+1-c for the owner of q.

## Exact single-owner receipts

Let F count full physical tiles with endpoints from more than one source,
and E count directed intratile cross events (source,endpoint,target), omitting
directions toward that source's immutable H. Define Phi as positive-source
count plus negative charge mass plus2F-E. Source charges are computed from
their own matching, endpoint tiles and inside-tile original supports.

The table gives the marginal against the entire baseline (1). Set I=1
when b=W and I=0 otherwise; I is always zero for V. All listed contacts
are within the current gap or its two bordering B sources.

| Owner | Charge | New mixed full tiles | New cross events | Delta Phi |
|---|---:|---:|---:|---:|
| D_b | 1-b | 3(1+I) | 5(1+I) | b+I |
| U_b or V_b | 1 | 3(1+I) | 4(1+I) | 3+2I |
| L | 0 | 1 | 0 | 2 |
| H | -2 | 1 | 1 | 3 |

Here is a direct receipt partition, rather than just a count. For either
U type, the left mixed tiles are (2,0),(3,0),(4,0) in normalized physical
tile coordinates. The first tile is completed by the old wall, B_i's tip,
and the new source; it is counted once despite having three sources.
The two horizontal new-to-wall events have endpoint (6,1),(8,1).
The two wall-to-new events have endpoint (6,0),(8,0). For D only there
is the additional new-to-B_i event (5,1)->(4,1). U and V have that
direction in their original supports, so it is excluded. If b=W,
reflect these three tiles and events to the right band; the bands are
different because W>=6. At b<W there is no right-wall contact. The
extra two cells of V's far stem lie in an interior column, with no
additional old endpoint or intratile event.

For either rotor the only new full tile is (2,0). H has the one event
(5,1)->(4,1), and L has none. These are the original two-gate rotor
receipts and do not depend on the next bar being at row8 rather than10.
The other retained B sources have disjoint endpoint-tile rows from
these new owners; there are no omitted old contacts.

## Both gates: repeated owners and all new/new corrections

Assign a horizontal radius b to D_b,U_b,V_b and radius4 to H,L. Each
left-owner endpoint column is in [1,radius]. A reflected right owner's
endpoint columns are in [W+1-radius,W].

One source owns both gates if and only if it is D_W or U_W. Both full
records are invariant under reflection about the middle column; their
matching and H records agree too. V cannot span, and a rotor's column
diameter3 is smaller than W-1. A nonspanning U cannot contain q.
In this case count that source once: its exact marginal is W+1 or5.

For two distinct owners with radii h,j, endpoint disjointness is equivalent
to h+j<=W. Sufficiency follows from the column intervals. For two U
owners, if their intervals overlap, the right owner's left stem at
column W+1-j meets the left owner's full horizontal bar at row5 or8.
For a U and a rotor, failure of the inequality puts the U's radius at
W or W-2. Every U has an endpoint at (5,b); both reflected rotor
records contain (5,W) and (5,W-2). These give a collision. Two rotors
violate the inequality only at W=6; all four mode pairs collide, as
in the accepted width-six theorem. This proves necessity for every pair.

If h+j<=W-2, the owners have disjoint physical tile columns, so their
joint increment is exactly the sum of their single increments. If
h+j=W, the only common physical tile column has cells h,h+1. No old
endpoint lies in these shared tiles, since both owners are nonspanning
and this column is interior. There are therefore no old/new/new triple
corrections. The complete new/new correction C=2F_cross-E_cross is:

| Left and right types | New/new F | New/new E | C |
|---|---:|---:|---:|
| Any two U types, except V/V | 2 | 4 | 0 |
| V/V | 3 | 6 | 0 |
| L with any U type | 0 | 1 | -1 |
| H with V | 0 | 1 | -1 |
| H with D or U | 0 | 0 | 0 |
| Any two rotors | 0 | 0 | 0 |

To check this finite table uniformly in breadths, each U's facing stem
has rows5..9, with outward original supports at rows5,7,9; V extends
this to rows3..9, adding outward support row3. Thus two U stems give
the full tiles in row pairs6/7 and8/9 and four directed even-row
events; V/V adds row pair4/5 and two events. At its facing column4,
H has only the even-row endpoint (4,4), L only (6,4). Both have the
outward same-row original support. Hence their counterpart U gives
one event towards the rotor exactly in the two exceptional cases.
No two rotor facing masks complete a tile or admit a cross event.
This also proves the reflected order of each table row.

Distinct nonspanning U owners each have marginal at least3; two rotors
each have marginal at least2. The only negative correction is a single
unit for a U/rotor pair, whose isolated sum is at least3+2. Therefore
the exact per-gap joint marginal J satisfies

    J>=4; if W=6, J>=5.                                   (6)

At W=6 two distinct owners cannot fit: even the smallest two radii sum
to8. Only the single spanning D_W/U_W cases remain. The bounds are
attained by partial inventories (two L rotors at every gap for W>=8,
or one U_W at W=6); no complete-extension sharpness is asserted.

## Across-gap simultaneity and nonreuse

Every candidate owner's endpoint rows lie in [a+10i+3,a+10i+9].
Candidates from different gaps therefore cannot be the same original,
cannot overlap endpoints, and have disjoint endpoint-tile row sets.
In particular, they cannot create a new/new tile or event across gaps.
The local lists also prove that a candidate meets old endpoints in
tiles only at A or the two bordering B sources. Every mixed full tile
and source-labelled cross event is assigned to one gap and, within it,
to a left band, right band, or the interior new/new correction. The
three-source tip tile is in its boundary band only. A spanning owner
appears once and uses both boundary bands in that one receipt.

The even-bar contact ledger gives Phi(old)=1-n. Consequently the exact
global selected inventory is

    Phi(K)=1-n+sum_(i=0)^(n-2) J_i.

Equation (6) proves (2) and its W=6 strengthening. This sums receipts
against one common baseline, without reusing an owner, physical tile,
source event, or unit of surplus. Remaining unselected originals and
additional retained sources are outside the marginal assertion.

## Validation scope

The companion verifier reconstructs all T,H,M records, checks every
sampled full-U orientation and endpoint anchor against the exhaustive
list, verifies exact single and joint receipts, explicitly checks shared
owners, all25 tight type pairs, separated pairs and mixed multi-gap
batches. Its finite controls check the general argument above; they do
not prove the infinite classification or complete-extension existence.
The companion Lean source checks the local receipt arithmetic, distinct-
owner packing inequalities, cross-gap separation and simultaneous bound.
Source-role adapters, full geometric receipts and complete-extension
selection remain written mathematics, not a fully formal source theorem.

The full verifier completed with exit0 (process84755):7500 U roles,
80 rotor roles,34 normalized U records,980 compatible joint choices at
seven widths,384 mixed multi-gap batches with exact tile/event partitions,
and widths100/2000 with11 spanning shared owners each. Final Lean4.33.0
process95784 exited0:27 explicit declarations/19 local theorems individually
audited, ordinary axioms only, no warnings/sorry/native. Preflight46%
memory free; comm-basename inspection found no active Lean/lake process.

Independent review is submitted through the existing conversation
conv_ed4025a182e9f9d9, original streaming process71332, without a verdict.
It includes this theorem and the earlier unreviewed spacing-six corollary.
The preceding all-width spacing-eight theorem has separately received
ACCEPT (18509-character exact original-stream/terminal match); that verdict
is not attributed to this new result.
