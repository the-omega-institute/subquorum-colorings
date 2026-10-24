# Mixed successors require residual boundary debt

7 October 2026. We give an unbounded, fully normalized equality family that
refutes a whole-band compensation rule, and prove a corrected local bound.
The corrected bound uses the already established all-length width-six Omega
theorem. The construction and its failure calculation have elementary proofs
for every module count. No conclusion rests on absence of finite counterexamples.

We use the aligned 2-by-2 residual graph of the
[boundary-aware note](CROSS_COMPONENT_COMPENSATION.md). A tile is saturated
when it contains two selected vertices; otherwise it is deficient. For a
deficient tile, write t for selected vertices, p for matching endpoints,
h for internal matching edges and s for attachments to saturated tiles.
Its capacity is r=2-t-h-s, its residual degree d counts matching edges to
other deficient tiles, and its charge is rho=d/2-r. Saturated tiles have
charge zero. Thus q=|T|+|M|-|V|/2 is the sum of all tile charges.
Omega is the maximum of |T|+|M| over feasible pairs: each selected vertex
has at most one neighbor among selected vertices and matching endpoints.
P denotes a matching endpoint and B a blank vertex.

## 1. An exact ledger with receiving saturated tiles

For any tile-aligned region Z, let t(Z), b(Z) count its selected and blank
vertices. Let sigma_out(Z) count matching edges from a deficient tile in Z
to a saturated tile outside Z. Let sigma_in(Z) count matching edges from a
deficient tile outside Z to a saturated tile in Z. Then

    2rho(Z)=t(Z)-b(Z)+sigma_out(Z)-sigma_in(Z).              (1)

**Proof.** On a deficient tile, 2rho=2t+p+s-4=t-b+s. A saturated tile
without P has t=b=2. A saturated tile with P has t=2,b=p=1, so its zero
charge is t-b-p. Sum over the region. A matching edge from an internal
deficient tile to an internal saturated tile contributes once through s
and once through the receiving p; these cancel. No edge joins two saturated
tiles. The uncancelled incidences are exactly sigma_out and sigma_in. QED.

The earlier pressure-band identity has sigma_in=0: saturated tiles inside
that band contain no P. A successor below a mixed band can contain saturated
receivers, so that specialization cannot be used unchanged.

## 2. The candidate rule

Let U be the filled source of the boundary-aware compensation note: rows
0,1, columns 0 through N-1, with N=2k+4, k>=3. Row 0 has T at its ends
and the prescribed matching edges (0,2j+1)--(0,2j+2), 0<=j<=k.
Row 1 has B at its ends and P at every other position. Its two extreme P
vertices match downward to the fixed saturated side caps in rows 2,3.
The other row-1 mates are unrestricted. Thus rho(U)=1, including capacity-two
source tiles. The side caps are TP/BT on the left and PT/TB on the right,
both matched upward to U.

For completeness, no saturated tile of S contains P. An upper T already
sees the P above it, so its two tile neighbors are B; a second T can only
be opposite. If both T are lower, both upper corners must be B. Thus no
additional source endpoint can attach to a saturated tile of S. In (1),
U has two T, two B and exactly the two fixed outgoing saturated attachments,
so rho(U)=1 regardless of its interior matching. This also recovers the
entrance restriction proved in the [pressure-band note](PRESSURE_BAND_BRANCHING.md).

Let S be the k inner tiles of rows 2,3 and assume rho(S)=0. Require its
first tile to be PP/BP with its lower-right P matched downward to a saturated
tile, and its last tile PP/PB with its lower-left P similarly matched.
Let C be the entire aligned interval below S, in rows 4,5 and columns
2 through N-3. Its first and last tiles are consequently the saturated
receiving caps TP/BT and PT/TB.

A proposed extension was: if the pair is already normalized and
sigma_out(C)=0, then rho(C)<=-1. This would pay U from the whole outermost
successor even when S is mixed. It is false. In fact rho(C) can be
arbitrarily positive under these hypotheses, while the full grid satisfies
the target inequality with equality and has a genuine positive component.

## 3. An all-size equality construction

Take an integer b>=1, put k=3b+5 and N=6b+14, and use an 8-by-N grid.
Each entry below is one aligned tile, with letters in upper/lower row order.
The four tile rows, indexed 0 through 3, are

```text
source:  TP/BP  (PP/PP)^k                         PT/PB
parent:  TP/BT  R F X^(3b) R F L                  PT/TB
child:   TB/BT  A D (V E G)^b A J B               BT/TB
bottom:  TB/BT throughout, with the replacements specified below
```

The symbols mean

```text
R=PP/BP, F=PP/PP, X=PP/BT, L=PP/PB;
A=TP/BT, D=PP/BT, V=TB/BT, E=TB/PP, G=TB/PT,
J=PP/BB, B=PT/TB.
```

The child letter B denotes the displayed tile, not a blank vertex. In the
bottom tile row, replace the tile below each E by PB/BT and replace the
last three tiles by BT/TB. Every displayed T is selected. Match all P as
follows; rows and tile columns are indexed from zero.

1. Use the source matching of the corridor construction, including every
   row-1 internal pair and its two attachments to the parent side caps.
2. Match the upper PP pair in every inner parent tile internally.
3. At the two R tiles (columns 1 and k-2), match their lower-right P
   downward. At L (column k), match its lower-left P downward.
4. At the first F (column 2), match both lower P downward to D's upper P.
   At the last F (column k-1), match the lower PP pair internally and match
   J's upper PP pair internally.
5. For each E (column 4+3j, 0<=j<b), match its lower-left P downward to
   the PB/BT tile below, and its lower-right P horizontally to G's lower-left P.

These instructions use every P exactly once, with no repeated endpoint.

**Proposition 1 (unbounded failure of whole-band compensation).** For every
b>=1 this is feasible, has no capacity-one fork and no eligible neutral
attachment promotion, and has precisely one positive residual component
of excess +1 and one negative component of excess -1. Every other component
has excess zero. Nevertheless

    rho(U)=1,  rho(S)=0,
    sigma_out(C)=0,  sigma_in(C)=3,
    rho(C)=b/2-1,  rho(outside U,S,C)=-b/2,
    |T|=13b+31,  |M|=11b+25,  q=0.                       (2)

Thus b=1 already refutes rho(C)<=-1, b=2 gives a neutral whole successor,
and b=3 gives a positive one. No width-independent negative budget can be
assigned to the whole successor merely from normalization and sigma_out=0.

**Proof.** The source and parent side-cap T vertices each see their own
single P neighbor. Each parent X has its lower-right T adjacent to its upper
P; the other lower corner, its right exterior neighbor and the child upper
corner below it are B. The child A,B,G T vertices each see their own P and
otherwise B. D's lower T sees its upper P and otherwise B. E's upper T sees
its lower-left P and otherwise B. In each V, the lower T sees the next E's
lower-left P; the upper T sees the preceding D's P only in the first module,
and otherwise no occupied neighbor. The outer child diagonal pairs have
no occupied neighbor.

In the bottom row, a TB/BT upper T can see the G lower P above it and no
other occupied neighbor. Its lower T is isolated except just before the
final BT/TB segment, where it meets that segment's lower T. This pair is
the sole neighbor of both vertices. A PB/BT lower T is isolated. The last
BT/TB upper T vertices are isolated and their lower T vertices have no
neighbor except the one just described. These checks cover every T and
every repeated interface, including the two ends. Thus feasibility holds
for every b; no exhaustive-search optimality claim is used.

The source component is the usual LL path: k+1 edges and total capacity k.
The first F and D form a two-edge parallel component with capacity two and
excess zero. Each E is a residual-zero leaf: t=1,p=2,s=1,r=0,d=1, so its
charge is +1/2. Its lower PB/BT partner has t=1,p=1,s=h=0,r=1,d=1, hence
charge -1/2. Their two-vertex component has excess zero. J has h=r=1,d=0
and charge -1. All other deficient tiles have r=d=0. This lists all
components; none is a capacity-one fork.

The neutral attachments are the three R/R/L exits. Each has three occupied
neighbors at its neutral endpoint: its upper P, its saturated mate, and
the lateral P in the next or preceding F. All other attachments originate
in positive source leaves or positive E leaves, so the neutral-attachment
normalization has no move.

Within C, only the b E tiles and J have nonzero charge, giving b/2-1.
The only nonzero tiles outside U,S,C are the b lower partners, each -1/2.
Alternatively t(C)=5b+7,b(C)=4b+6 and sigma_in(C)=3 give the same result
from (1). The tile rows have respectively 2,3b+4,5b+11 and 5b+14 selected
vertices, totaling 13b+31. The matching instructions give 11b+25 edges.
Their sum is 24b+56=4N=8N/2, proving q=0. QED.

**Capacity-two version.** Flip the two horizontal matching edges in rows
1 and 2 at tile column 3 to the two vertical edges of that square. Both
tiles are deficient and all four corners are P. Occupancy and every tile
charge remain fixed: h decreases by one, r increases by one and d by two
at each affected tile. The source tile now has capacity two. The source
component gains two edges and two capacity units, so still has excess +1.
The child, its lower boundary debt and the separate negative component
are unchanged. Neutral attachment endpoints and their blockers are unchanged.
This gives the same obstruction with a capacity-two passage.

## 4. The corrected local compensation bound

Retain the geometric hypotheses of Section 2, in an arbitrary ambient
rectangle. Let beta count matching edges from a deficient tile in C to a
deficient tile immediately below C. Let tau count matching edges from a
deficient tile in C to a saturated tile immediately below C. Edges exported
downward from saturated tiles of C are not included in either count.

**Lemma 2 (mixed successor with lower boundary debt).**

    rho(C) <= -1+beta/2+tau,
    rho(U union S union C) <= beta/2+tau.                  (3)

In particular, a successor with beta=tau=0 pays the source's full unit even
when its parent and its own tiles are mixed and occupied. The coefficient
of beta is sharp, by Proposition 1. No sharpness assertion is made for tau.

**Proof.** Delete every matching edge crossing the lower boundary of C,
without promoting any endpoint. Feasibility is preserved because occupation
only decreases. Selected counts and tile saturation status do not change.
Deleting a beta edge decreases the deficient endpoint's p and residual
degree by one, hence decreases rho(C) by 1/2. Deleting a tau edge decreases
p and s by one, hence decreases rho(C) by one. Deleting an edge exported
from a saturated tile of C leaves that tile's charge zero. No other tile
of C changes. Therefore the resulting region C' has

    rho(C')=rho(C)-beta/2-tau.                             (4)

Neither U nor S loses a vertex or matching incidence, and their charges
are unchanged. The two extreme receiving caps in C retain their original
P, which is matched upward, and remain TP/BT and PT/TB. Consequently no
matching edge crosses C's lateral boundaries. All other matching endpoints
of U and S lie within the displayed patch: the row-0 edges and the side-cap
mates are fixed, and a side-cap P is already matched. After (4) no edge
leaves the patch downward either.

Take these three tile rows as a standalone 6-by-N rectangle. Put the
leftmost tile in its last tile row in state TB/BT and the rightmost in
BT/TB, with no matching endpoint there. These new T vertices have no
occupied neighbor, and every neighboring old T faces a blank companion.
The parent side caps and C's receiving caps remain feasible. There are no
unmatched P endpoints. This constructs a feasible pair on the standalone
rectangle whose global excess is exactly 1+rho(C').

The already proved all-length strip theorem gives Omega(G_(6,N))<=3N for
even N. Hence 1+rho(C')<=0. Substitution in (4) proves (3). QED.

The dependency here is the **Omega** bound, not merely the coloring bound
psi_sq<=3N. It is established by the exact frontier recurrence and full-vector
translation induction for every length. Width-six metadata is
`develop/results/omega-w6.json`: start 6, period 2, doubled increment 12,
3,105 reachable endpoint states, together with its indexed start/end vectors
and initial readouts. The general transfer argument is in
`develop/grid-strips-2026-09-27.md`; the focused manuscript's strip theorem
explicitly proves the Omega upper bound. Lemma 2 is a corollary of this
existing all-length theorem, not a new independent proof of that theorem
or an inference from a bounded search.

Reproduce this prerequisite with `python3 scripts/check_strip.py 6` after
compiling `develop/grid_omega.cpp` and `develop/check_omega.cpp` as described
in [the reproduction guide](REPRODUCE.md). This recomputes the initial
readouts and both complete indexed vectors and runs the independent checker.

## 5. One budget per outside region

For pairwise tile-disjoint triples (U_i,S_i,C_i) satisfying Lemma 2, let W
be all remaining deficient tiles. The exact ledger gives

    q <= sum_i (beta_i/2+tau_i)+rho(W).                   (5)

This proves coefficient one on the class with every beta_i=tau_i=0 and
rho(W)<=0: the uniform estimate `|T|+(5/6)|M|<=mn/2` becomes
`|T|+|M|<=mn/2` on this explicitly covered class. With boundary debt,
distinct disjoint donor regions contained in W
must pay demands a_i=beta_i/2+tau_i. The existing capacitated Hall lemma
applies to geometrically justified incidence, using each donor region's
single verified capacity. Hall and a nonpositive unallocated remainder
then give q<=0. General Hall for arbitrary source geometries is still open.

In Proposition 1 every lower partner has capacity one and degree one,
so it has one verified half-unit, and the partners are distinct. The b
lower half-units pay exactly beta/2=b/2 in (5), giving equality. Counting
an E leaf's half-edge in C while discarding its negative partner would
leave spurious positive excess. Nor may one assign a half-unit to each
export without checking its partner: a capacity-one tile of degree two
has charge zero, so two exports into such a shared tile do not create
two half-unit budgets. Tile-disjointness and shared capacity are essential.

The new obstacle invalidates normalization plus saturated-boundary closure
as a complete compensation rule. The target grid inequality holds with
equality in every example. Bent source regions, overlapping triples,
uncontrolled residual exits and the universal coefficient-one theorem
remain unresolved. The journal manuscript is preserved.

Run `python3 develop/check_mixed_band_boundary_obstacle.py --output output/mixed-band-boundary-controls.json`.
It checks complete coordinates, routing, region charges, boundary closure
and capacity-two flips under eight symmetries. Optional finite discovery is
`develop/search_blocked_exit_strip.py`; the written statements above do not
depend on solver optimality. No new Lean formalization is claimed.
The verifier also exhausts all feasible pairs and tile regions on 2-by-2,
2-by-4 and 4-by-2 rectangles to check (1) and the deletion identity for all
three boundary edge roles, and records a capacity-one, degree-two receiver
with two ports but zero compensation budget.
