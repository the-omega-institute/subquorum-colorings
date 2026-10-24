# Neutral attachment normalization and blocked pressure exits

7 October 2026. This extends the [diagonal relay move](DIAGONAL_RELAY_NORMALIZATION.md)
to adjacent occupied corners and three-endpoint tiles. The proof is independent
of residual routing, so bent paths, parallel edges and capacity-two passages
are included. The journal manuscript and its five-sixths theorem are unchanged.

## 1. Definitions

Fix a feasible pair (T,M) on an even-by-even rectangular grid with its aligned
2-by-2 tiling. Put P=V(M), A=T union P. Feasibility means that each T vertex
has at most one neighbor in A. A tile is saturated when it has two T vertices.
For a deficient tile Q, let t,p,h,s count its T vertices, P vertices, internal
matching edges and matching endpoints whose mates lie in saturated tiles.
Its residual capacity and degree are r=2-t-h-s and d=p-2h-s. Thus

    2rho(Q)=d-2r=2t+p+s-4.

Saturated tiles have charge zero. Call a deficient tile neutral if rho(Q)=0.
The exact ledger is q=|T|+|M|-mn/2=sum_Q rho(Q).

Write deg_A(x) for the number of occupied grid neighbors of x, including its
matching mate. An eligible attachment is an edge xy in M with x in a neutral
deficient tile Q, y in a saturated tile S, and deg_A(x)<=2.

## 2. A charge-preserving move

**Lemma 1 (neutral attachment promotion).** Delete an eligible edge xy,
promote x from P to T, and make y blank. The resulting pair is feasible,
has the same objective, and has exactly the same charge at every tile.
Every residual edge, its endpoint corners, and every residual capacity and
degree are unchanged. If Q becomes saturated, its former residual vertex
was isolated with capacity zero and is deleted. No other residual component
changes. In particular all positive and negative components are preserved.

**Proof.** The new occupied set is A minus {y}. The new T vertex x has
deg_A(x)-1<=1 occupied neighbors; every old T can only lose neighbors.
The remaining matching avoids the enlarged T. Exactly one matching edge is
removed and one T is added, so the objective is unchanged. For this particular
single-endpoint move, deg_A(x)<=2 is also necessary: after deleting xy,
x still has exactly deg_A(x)-1 occupied neighbors.

The receiving tile S keeps both T vertices and loses only its P vertex, so
it remains saturated. In Q, t increases by one, p and s each decrease by one,
and h is unchanged. Therefore r and d, and hence rho, are unchanged while Q
is deficient. There is no other matching edge incident with y, and removing
xy changes no label or matching incidence in any other deficient tile.

It remains to check saturation of Q. If its original t=1, neutrality and
s>=1 give p+s=2. Since s<=p, necessarily p=s=1. After the move Q has two T
and no P, so its former h,r,d were all zero. No edge elsewhere changes from
residual to saturated attachment when Q becomes saturated, because there is
no remaining matching endpoint in Q. If its original t=0, Q still has t=1
after one move and the preceding calculation applies. Saturated tiles have
charge zero throughout. This proves every asserted invariant. QED.

The cases with an attachment in a neutral deficient tile are precisely

    (t,p,s)=(1,1,1), (0,2,2), (0,3,1).

The first two include adjacent as well as diagonal occupied corners. The
third, omitted by the diagonal lemma, can have (h,r,d)=(1,0,0) or (0,1,2).
In the second case the move preserves a genuine degree-two residual passage.

## 3. Termination and independence of order

**Theorem 2.** Repeatedly apply Lemma 1 until there is no eligible attachment.
The procedure terminates, increases |T| by the number of moves, preserves the
objective and all tile charges, and yields a unique final pair independent
of the order of eligible moves. It has an implementation taking O(mn) time
and space. Its final pair has no diagonal neutral relay.

**Proof.** Each move removes one edge, so there are at most |M| moves.
Each original saturated tile stays saturated. Newly saturated tiles contain
no P; consequently they receive no surviving matching edge. By Lemma 1,
charges remain fixed and every unprocessed endpoint of an original attachment
from a neutral deficient tile to a saturated tile stays P in a neutral
deficient tile. These original attachments form a fixed possible-move set E_0.
No matching edge outside E_0 ever becomes eligible.

For e in E_0, denote its neutral endpoint by x_e and its saturated mate by
y_e. After processing a set F of moves, the occupied set is exactly
A minus {y_f:f in F}. Thus an unprocessed e is eligible precisely when

    deg_A(x_e)-|N(x_e) intersect {y_f:f in F}| <= 2.          (1)

This predicate is monotone as F grows. An eligible unprocessed edge cannot
lose eligibility. Let F_* be the closure obtained by adding all eligible
edges in rounds, starting with the empty set. Every sequential legal move
lies in F_* by induction. Conversely, the terminal processed set of any
sequential procedure contains every round of F_*: induction on the rounds
uses (1) and the absence of any remaining eligible edge. The two sets agree.
The final T is T union {x_e:e in F_*}, and final M is M minus F_*, so both
are independent of order.

For the time bound, compute E_0 and occupied degrees once. Keep a queue of
eligible endpoints. Removing y changes degrees only at its at most four
neighbors; each attachment is removed once. Constant grid degree bounds the
initial work, queue updates and storage by O(mn). A diagonal neutral relay
has two occupied diagonal corners and all its P matched to saturated tiles.
Each such P has two blank internal neighbors and at most two exterior
neighbors, one its mate. It therefore has degree at most two and cannot
remain at termination. QED.

In particular, an objective maximizer with maximum |T| among maximizers
already has this normal form. Normalizing an arbitrary pair does not assert
that this stronger global maximum-|T| condition has been reached.

## 4. Consequence for mixed neutral pressure bands

Consider a pressure band with the full-P row above it and the side caps of
[pressure-band nonpositivity](PRESSURE_BAND_BRANCHING.md). Suppose it exists
in the final configuration of Theorem 2 and has rho(S)=0. Its tiles are
individually neutral. The twelve-state list in the
[mixed-neutral note](MIXED_NEUTRAL_DONORS.md) now reduces to ten:

    PP/PP, PP/BP, PP/PB, PP/BT, PP/TB,
    BP/TP, PB/PT, BB/TT, BT/TB, TB/BT.

**Corollary 3 (blocked exits).** Every saturated attachment leaving S is
from a three-P tile: an R exit in PP/BP or an L exit in PP/PB. For each R,
the immediately following lower-row vertex is occupied. For each L, the
immediately preceding lower-row vertex is occupied. Equivalently every
surviving exit endpoint has occupied degree exactly three. The first exit
is R, the last is L, and there is at least one consecutive R,L pair.

**Proof.** The excluded states TB/BP and BT/PB are diagonal neutral relays
and are absent by Theorem 2. The remaining state list follows from the
complete necessary list already proved for neutral pressure bands.
In PP/BP the exit has its upper P neighbor, its saturated mate below,
a blank left neighbor, and just one other possible neighbor on the right.
If that neighbor were blank, Lemma 1 would apply. It must be occupied,
giving degree three. Reflection proves the L assertion. The outer-exit
orientation lemma applies to this same pressure band and proves the last
three assertions. QED.

This is a necessary local reduction, not a sufficiency test for global
matching realizability. The old side caps of a descendant band may lose P
during normalization, so the corollary concerns bands in the resulting pair.
It does not transport an old cap certificate unchanged through the move.

## 5. Exact examples and the failed unrestricted move

All coordinates below are in a 6-by-6 grid, indexed from zero. Unspecified
vertices are blank. Let Q be rows 2,3 and columns 2,3.

* **Three-P isolated neutral tile.** Take T={(4,2),(5,3)} and
  M={((2,2),(2,3)),((3,3),(4,3))}. Q is PP/BP and has
  (t,p,h,s,r,d)=(0,3,1,1,0,0). Its exit x=(3,3) has degree two.
  Promotion gives PP/BT and preserves all zero capacities and degrees.
* **Neutral residual passage.** Keep T and replace the first matching edge
  by ((2,2),(1,2)) and ((2,3),(1,3)). Now Q has
  (t,p,h,s,r,d)=(0,3,0,1,1,2). Promotion leaves its two residual edges to
  the same neighboring deficient tile and preserves their endpoint corners.
  That neighbor has capacity two; the residual component has excess -1.
* **Blocked exit.** Add ((3,4),(2,4)) to the first example. The pair is
  feasible and Q still has zero charge. Now x has occupied degree three.
  Deleting its attachment and promoting it leaves two occupied neighbors,
  (2,3) and (3,4), so feasibility fails. Thus the rule "promote every neutral
  attachment" is false. The degree condition is exact for this move. This
  is a counterexample to that rule, not to q<=0: here |T|+|M|=5<18.

The previously archived all-neutral 8-by-8 configuration has four matching
edges. The diagonal normalization removes three; Theorem 2 removes all four,
including the adjacent-corner neutral tile BT/BP. Its final pair has |T|=32,
M empty and every tile saturated. This proves that the extension reaches a
previously untreated zero-charge configuration without inventing donor credit.

## 6. Consequences for compensation and the remaining problem

Every positive source and every negative regional charge survives unchanged.
For any fixed tile sets, their charges are identical before and after the
move, including unions crossing bent routes and capacity-two passages.
Previously established disjointness and charge bounds therefore persist.
Geometric source-to-donor incidence must still be established after
normalization; a removed receiving P may change a cap or pressure certificate.

No compensation is created by these moves. For K disjoint source regions
of charge at most one, H distinct certified deficient same-direction donor
tiles and remainder W, the existing ledger remains

    q <= K-H/2+rho(W).

Weighted Hall and a nonpositive remainder still give coefficient one on that
covered class. Theorem 2 extends the available normal form but proves no new
universal constant beyond 5/6. It does not establish weighted Hall for all
sources, remove saturated zero gaps or resolve the grid conjecture.
For every b>=1, the branching family in the pressure-band note is already
irreducible for this move. Its neutral attachments are precisely the 2b
band exits. Each exit has its upper P neighbor, its saturated mate below,
and the lower P of the full tile between its receiving caps, giving occupied
degree three. Its source-end attachments start in positive, not neutral,
tiles. There are no other attachments from neutral tiles. Nevertheless the
source has excess +1, its b donor components each have excess -1, and q=1-b.
Thus infinitely many irreducible configurations still require the separate
compensation argument; normalization cannot replace it.

Run `python3 develop/check_neutral_attachment_normalization.py --output output/neutral-attachment-normalization-controls.json`.
The checker independently checks coordinates and the residual ledger, tests
all feasible pairs on 2-by-2, 2-by-4 and 2-by-6 ladders, exercises all eight
symmetries of explicit mixed and capacity-two examples, compares legal
processing orders and checks 32 irreducible branching examples. These finite
checks support the general proof above;
they are not a general compensation proof or a new Lean formalization.
