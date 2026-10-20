# Critical returns have two original bar slots per phase01 owner

20 October 2026. The complete critical closed-owner obstruction admits a
precise replacement for the false freshness rule. Every phase01 owner of
a critical second point owns that point as an upper outer bar corner, in
an originally full tile. Each original phase01 owner has exactly two such
slots; their receiving tiles are distinct and are disjoint from ALL first
and LONG second receiving tiles. A seven-source complete family attains
both slots of ONE closed owner. These are geometric capacities, not reserve
payments. The unrestricted coefficient-one allocation and grid equality
remain OPEN.

## 1. Hypotheses and the exact owner role

Use the finite complete original U/rotor model, disjoint original endpoints,
unchanged matchings, mandatory support retention, selected occupied degree
at most one and transported fixed tile partition of
[the critical continuation theorem](PHASE11_CRITICAL_CONTINUATION_AND_ALL_OWNER_COUNT.md).
All legal U dimensions are even, with width>=6 and both heights>=4. Original
owners can recur. Consider ALL critical continuations of actual neutral01
contacts, including those on open components.

Normalize one critical second point t to (0,0), its frame to s=N,d=E. Its
physical receiving tile is Q={0,1}x{0,1}, not the ordinary receiver northwest
of a first/long point. The active phase01 owner O owns (-1,0), while the
first phase11 owner F owns (0,-1). The established critical geometry excludes
O,F and the original passive owner from owning t. These two neighboring
endpoints are therefore foreign to t's original owner G.

Suppose G has phase01. Write its canonical endpoint predicate as

    0<=r<=1, 1<=c<=w; or c=1, 2<=r<=l; or c=w, 2<=r<=h.

The canonical origin parity is (0,1). If the inverse signed permutation is
pull(transpose,flipRow,flipColumn,anchor,x), the pulled Q origin is

    (anchor.row - int(flipRow), anchor.column - int(flipColumn)).

Thus its coordinates have residues (0,1). Splitting the bar and two stem
roles and the eight signed permutations, exclusion of (-1,0),(0,-1) leaves
exactly

    flipRow=false;
    flipColumn=false, anchor=(0,1), or
    flipColumn=true,  anchor=(0,w).

The transpose bit is unrestricted. This is an arbitrary-dimension role
proof using inequalities and parity. In particular t is an upper outer bar
corner, never a terminal or another stem/bar point. The four pulled corners
of Q are respectively rows0,1 and columns1,2 or w-1,w, so ALL FOUR are
original endpoints of G. The tile was full before fusion.

## 2. Injective return tiles and separation from regular receivers

Let Kb count critical contacts whose second point is owned by ANY phase01
source, and let Mb be the number of distinct such original owners. Their
second points are globally injective by the established critical theorem.
Each phase01 source has exactly two upper outer bar corners, hence

    Kb<=2Mb.                                                   (1)

The assertion also restricts to any chosen set of receiving original owners.
For example, returns to a chosen closed-owner set C satisfy Kb(C)<=2|C|.
This is not a bound on a chosen set of producing port components unless
their actual receiving owners are included too.

The two corners of one source differ by w-1>=5 along its bar. They cannot
lie in the same physical tile. If two return tiles coincide, both are full
of their own original owner's endpoints, so endpoint uniqueness identifies
the same owner. The two-corner separation identifies the same corner; the
critical point injection identifies the same contact. Thus the return-to-tile
map is injective even when receiving owners recur.

Every first/LONG receiver has an exact original regular2P1T profile of its
active phase01 source. It cannot also be an original full tile of a return
owner: different owners would overlap, while the same owner would have
both an exact pair and a full profile in one tile. Hence ALL Kb return tiles
are disjoint from ALL first/LONG physical receivers, including full regular
receivers. This is stronger than merely separating the forced positions.

These return tiles contain no foreign original singleton, pair or triple.
In particular they are not original phase11 cap tiles, mixed3P0T stops, or
tiles used by the foreign-pair singleton reservation. Their corner positions
are not in the U negative singleton pool, which consists of phase01 terminals
and phase10 outer corners. Counting these bar corners must not be substituted
for that different pool's unused terminal occurrences.

## 3. One exact joint endpoint count

Keep the existing ALL-first/LONG event family, with C01 first contacts,
L11 long seconds and J=J01+J11 nonfull receivers. Let X be their additional
final endpoint set outside their active original pairs, so

    |X|+J=2(C01+L11).

Let Vb be the union of ALL FOUR original endpoints in each of the Kb return
tiles, and Yb the critical points themselves. The preceding injection and
physical tile separation give

    |Vb|=4Kb,   X intersect Vb=empty,   |Yb|=Kb;
    |X union Vb|+J=2(C01+L11)+4Kb.                             (2)

Thus all these particular critical points are also separated from the OTHER
extra corner of every first/LONG full receiver. Possible coincidences with
that corner remain only in critical branches owned by other effective phases
or rotors; no general separation for those branches is asserted.

The subsequent [complete-owner proof](ALL_CRITICAL_REGULAR_RECEIVER_SEPARATION.md)
resolves those remaining branches too: ALL critical points avoid every
first/LONG physical receiving tile. That stronger result has a separate
independent review task and must not inherit this note's review status.

Use the SAME existing inequality B+J<=2A+H once, to obtain

    |X union Vb|+2A+H >= 2(C01+L11)+4Kb+B.                     (3)

In one qualifying nonexceptional AA endpoint component, restrict ALL events
and return tiles to that component. The direct H packing makes J=0. For
ell selected closed neutral curves, C01>=4ell gives

    |X union Vb|>=8ell+2L11+4Kb.                              (4)

If first contacts are selected, their first/LONG counts use precisely that
selection; Kb can be a selected family of phase01 returns in the SAME full
endpoint component. The return tile is in that component because its critical
point is adjacent to its producing O and F endpoints. Vb may intersect the
chosen closed owners: (4) is a JOINT endpoint requirement, not an outside-owner
bound. A need not vanish. No term4Kb is added to R, H or another reserve.

## 4. A complete family saturating both slots of one closed owner

For every even W>=20 use the following seven canonical U sources. Matching
and support formulas are those explicitly given in
[the complete six-source certificate](CRITICAL_CLOSED_OWNER_COUNTEREXAMPLE.md).
The ambient grid is20 by(W+4), with standard even tile origins.

| Name | (width,left,right) | Image of (r,c) |
|---|---|---|
| O | (W,12,12) | (r,c+1) |
| Fleft | (10,4,4) | (c+1,r+3) |
| Fright | (10,4,4) | (c+1,W-r) |
| Bleft | (6,4,4) | (c+11,7-r) |
| Bright | (6,4,4) | (c+11,r+W-4) |
| G | (W-12,6,6) | (r+2,c+7) |
| Hsource | (W-14,4,4) | (8-r,c+8) |

All dimensions are legal. Their original phases are01,11,11,01,01,01,10.
The original endpoint sets are disjoint, as follows directly from the row
interval table below; its intervals belonging to different sources are
disjoint, including at W=20. Define reflected column rho(c)=W+3-c. The union
P of original endpoints has precisely these columns in each row:

| Row | Columns of P |
|---|---|
| 0,1,2 | [2,W+1] |
| 3,7,8 | [2,4] union [8,W-5] union [W-1,W+1] |
| 4,5,6 | [2,4] union [8,9] union [W-6,W-5] union [W-1,W+1] |
| 9,10 | [2,4] union [W-1,W+1] |
| 11,12 | [2,7] union [W-4,W+1] |
| 13,14,15,16 | [6,7] union [W-4,W-3] |
| 17 | [3,7] union [W-4,W] |

All unlisted rows are empty. To retain source labels within the first three
rows, O supplies rows0,1 completely and columns2,W+1 below; Fleft/Fright
supply their two vertical bar columns3,4/W-1,W and their horizontal end
legs; G supplies the central bar rows2,3 and stems8,W-5; Hsource supplies
the central rows7,8 and stems9,W-6. Bleft/Bright supply the remaining lower
bars and legs. These descriptions also directly distinguish all sources.

For completeness, the full labelled endpoint refinement is:

| Source | Rows | Columns |
|---|---|---|
| O | 0,1 | [2,W+1] |
| O | 2 through12 | 2,W+1 |
| Fleft | 2,11 | [3,7] |
| Fleft | 3 through10 | 3,4 |
| Fright | Same rows as Fleft | Column reflection rho of Fleft |
| Bleft | 12,17 | [3,7] |
| Bleft | 13 through16 | 6,7 |
| Bright | Same rows as Bleft | Column reflection rho of Bleft |
| G | 2,3 | [8,W-5] |
| G | 4 through8 | 8,W-5 |
| Hsource | 7,8 | [9,W-6] |
| Hsource | 4,5,6 | 9,W-6 |

The union of mandatory original supports minus P is T=Tleft union rho(Tleft),
where rho acts only on the column and Tleft has these22 points:

| Row | Columns of Tleft |
|---|---|
| 0,2 | 1 |
| 3 | 6 |
| 4,6,8 | 1,7 |
| 5 | 10 |
| 9,11 | 8 |
| 10 | 1,6 |
| 12 | 1 |
| 13 | 2,4 |
| 16 | 4 |
| 17 | 2 |
| 18 | 3,5,7 |

Substituting the seven support formulas gives exactly this table: all other
original supports are in P. For W>=20 the two22-point sets are disjoint.
Comparing the P and T tables shows that every T point has exactly one
occupied neighbor, its original anchor. There are no adjacent T points and
no additional opposite-side neighbor at the minimum W=20. This proves
support retention and complete feasibility for EVERY even W>=20, without
using a finite width cutoff. All vertices are within the stated grid.

An explicit support check can retain the source labels as well. O contributes
(r,1) for r=0,2,...,12 and(13,2), with anchors(r,2) and(12,2).
Fleft contributes(3,6),(10,6),(11,8), anchored respectively at(2,6),(11,6),
(11,7). Bleft contributes(13,4),(16,4),(17,2),(18,3),(18,5),(18,7), with
anchors(12,4),(17,4),(17,3),(17,3),(17,5),(17,7). G contributes(r,7) for
r=4,6,8 and(9,8), anchored at(r,8) and(8,8). Hsource contributes(5,10),
anchored at(5,9). Reflection supplies the other22 points. Every omitted
original support is consumed: O's odd inner supports by Fleft/Fright;
each F's remaining supports by O, its B and G; each B's remaining supports
by its F and O; G's outer bar supports by the two F's and its odd inner
supports by Hsource; Hsource's remaining eight supports by G.

The union matching has3W+37 edges and6W+74 distinct endpoints. Since |T|=44,

    |M|+|T|=3W+81,   half-area-(|M|+|T|)=7W-41>0.             (5)

The O/Bleft and O/Bright contacts have first forced points (11,3),(11,W).
Their active heights12 and phase11 widths10 make both exits critical.
The second points are(2,8),(2,W-5), precisely G's TWO upper outer bar corners.
They lie in distinct original full tiles of G. G's terminals(8,8),(8,W-5)
meet Hsource's bar ports(8,9),(8,W-6) in two actual neutral2P1T tiles.
Hence G/Hsource form a closed two-owner neutral port component. Kb=2 and
Mb=1 in this family, attaining(1). Receiving-owner injection is therefore
false, even for returns into closed phase01 owners.

This complete family is not AA or a target-inequality counterexample. It
proves that two labelled original bar slots per owner are necessary and
sufficient for these particular returns. It does not turn those slots into
two independently available reserve payments.

## 5. Verification boundary and next allocation task

Ten new scoped Lean declarations compile, and all ten axiom prints pass.
Together with the later ALL-critical proof, the combined validation receipt
records19 declarations in
[the formal receipt](../output/critical-bar-regular-separation-formal-check.json).
Independent review a2e3a2cb-b711-454f-be21-c1467e16cc48 completed ACCEPT
at10:44:18 UTC. Its19,102-character answer matches the original exit0/DONE
stream exactly, observed gpt_6/pro. It independently reconstructs the role
proof, labelled endpoints, consumed/retained support and anchor tables,
minimum width, matching counts and closed parallel contacts for ALL even
W>=20. Inherited injections/census/AA remain explicit inputs. It does not
certify local executions or novelty, or review the later ALL-critical
extension. Its record is in
[the review receipt](../output/critical-phase01-bar-returns-review.json).

The [reproducible controls](../develop/check_critical_phase01_bar_returns.py)
pass1,984 phase01 original endpoint images with96 surviving bar-corner
roles. The13 family widths are20 through40 by2, plus60 and100; with the
preceding six-source fixture give112 complete partition-preserving images:
216 critical returns,216 distinct original full bar tiles and104 cases
using both corners of one receiving owner. There are432 regular additional
positions and864 bar-tile endpoint positions,1296 jointly distinct positions
in total. Complete long-second, other-phase-critical, closed01--closed01
contact and AA coverage is zero. See
[the control receipt](../output/critical-phase01-bar-returns.json).

The arbitrary-dimension role/full-tile proof and the two-corner width
separation have scoped Lean companions in
[`CriticalPhaseOneBarReturns.lean`](../formal/SubQuorum/CriticalPhaseOneBarReturns.lean).
Generic event-to-tile injection, original full/pair tile separation, the
two-position pool and joint-count algebra retain their stated physical
adapters. The seven-source family is proved by the explicit source and
row tables above; finite controls verify instances and do not prove the
unbounded statement. No general Lean proof of the entire family or the
unrestricted allocation is claimed.

The next unrestricted allocation step must combine this distinct physical
bar-tile pool with all remaining critical owner phases, full phase10
continuations and existing cap/singleton/H reservations. The new pool has
an exact owner capacity, but it contains original full tiles already in
the source ledger. A proof must identify a compensating charge rather than
add their endpoint count to R.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
