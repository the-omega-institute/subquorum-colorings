# Frozen half-area equality forces the entire actual matching

27 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The four terminal edges of the previous theorem propagate through the whole
occupied band. Every completely frozen half-area equality configuration has
exactly the matching of the explicit frozen attainer. Its selected set need
not be unique. Missing any one of these required edges restores one unit of
reserve, but missing many edges does not produce that unit many times.

## 1. Statement and inherited premises

Use exactly the 6 by (6m+10) board, m>=2, retained selections R'', old endpoint
set P0 and feasibility conditions in
[the frozen half-area theorem](FROZEN_HALF_AREA_ATTAINERS.md). Actual matching
edges, rather than a rematching with the same occupied sites, are at issue.
Put c=6m+9, n=3m+2. Keep its names A_j,...,H_j, U_j,V_j, g_i,b_i,
Z_l=(4,5+2l), K_l=(4,6+2l), and Q=(4,c).
Define the prescribed matching

    M* = M0 union {U_j V_j:0<=j<=m}
             union {g_i b_i:0<=i<m} union {g_m Q}
             union {Z_l K_l:0<=l<n}.                 (1)

The prior results used below are the unrestricted half-area upper bound,
the saturated pocket/pair/block equality conditions, their unique terminal
occupation pattern, and the four forced terminal edges of a frozen equality
board. Their proofs are linked in the preceding note; they are not consequences
of the finite discovery checks here.

**Rigidity theorem.** Every completely frozen feasible configuration with
R'' subset T, P0 subset P and J=|T|+|M|=18m+30 has

    M=M*,    |M|=9m+9,    |T|=9m+21.                 (2)

In particular all old matching edges are forced even though every old optional
selection is absent. For any completely frozen configuration in these
permissions, let d=|M* minus M| and delta=min(1,d). Then

    J <= 18m+30-delta,
    Cplus >= Cminus+m+2delta.                        (3)

Both values delta=0,1 are attained for every m. The second inequality uses the
same original physical tile tokens as before: pay exterior negative demands,
then strip demands, then count the remaining distinct tokens as reserve.
It does not allocate a second copy of an already paid token.

This is a theorem for the fixed occupied-band footprint and retained set,
not a universal grid improvement of 5/6.

## 2. Two elementary consequences of complete freezing

Let tau(v) be the first synchronous freezing round of an endpoint. In a
completely frozen finite configuration it is a positive integer. A neighbour
site is available at that round if it is selected, or if its actual mate has
strictly smaller tau. The endpoint's own mate is unavailable at its first
freezing round.

First every endpoint has at least three occupied neighbours. Its own mate
accounts for one, and freezing requires two other distinct occupied neighbours.
This observation includes endpoints at the boundary.

Second we use the trap principle from the preceding note. A nonempty endpoint
set S is impossible in a completely frozen configuration if every member has
at most one selected neighbour or endpoint neighbour whose actual mate is
outside S. Taking the first freezing round meeting S proves the assertion.
The sites of a witness and their mates must not be interchanged in this test.

From this point through Section 7, the standing hypotheses include complete
freezing AND half-area equality, except that the pocket inequality (4) itself
is valid without freezing. All block occupation facts refer to that equality.

## 3. A stronger pocket port inequality

Let L=W(A') be the sixteen-site pocket weight, U=U_0=(2,5),
V=V_0=(3,5), q=(4,5), and r=(5,5). In addition to the preceding two pocket
bounds, the same weighted certificate proves

    L <= 9+o_U.                                     (4)

Here o denotes actual occupation, and this assertion does not require freezing.
It suffices to rule out L=10 and o_U=0, since L is integral and L<=10.
At L=10 the preceding bounds force t_r=o_q=1. Since V already sees old
endpoint F_0 and occupied q, it is not selected. Thus t_V=o_U=0.
In the twelve-row certificate of
[Boundary withdrawals, Section 4](BOUNDARY_WITHDRAWAL_AND_PROPAGATED_COMPENSATION.md#4-the-left-pocket-can-gain-at-most-one-unit-and-then-starts-the-state),
the inequalities

    t_V+o_U<=1                 (weight 4),
    t_V+o_U+o_q<=2             (weight 2)

alone have weighted slack 4+2=6. The total weighted right side is 58, so the
weighted left side is at most 52. Its exact matching-incidence identity is

    weighted left side + 6t_r = 6L+H,   H>=0.

At L=10,t_r=1 this left side equals 54+H>=54, a contradiction. This proves
(4) using the single actual matching, including all pocket crossing edges.
Consequently half-area equality always has U_0 occupied.

## 4. Every old EF edge is forced before any band induction

Fix a core j and suppress its subscript. The retained selections force all
unlisted neighbours of B,U,D blank, and A,C can only match into {B,U,D}:
A can match B or U, and C can match B or D. The old endpoint E has possible
mates B,U,D,F.

If EF is absent, A,C,E are three distinct old endpoints whose mates all lie
in S={B,U,D}. Matching disjointness therefore makes all three members of S
endpoints, each paired to one of A,C,E. Their occupied neighbours are

    B: A,C,E;   U: A,E,V;   D: C,E,G.

All A,C,E have mates in S. The only possible outside supports are V at U
and G at D; B has none. No listed core neighbour is selected. Thus S is a
trap. Complete freezing forces EF, for every core simultaneously.
The isolated left old pair is forced by its available neighbours as before.

If GH is also present, covering D forces CD and then covering B forces AB.
Whenever U is occupied it cannot be selected, because it sees old endpoints
A,E. With AB,CD,EF present, U must match V. For j>=1, saturation makes the white b_(j-1) occupied. The black V_j
sees both b_(j-1) and old endpoint F_j, so it cannot be selected. Its
saturated anchored pair has t_(V_j)+o_(U_j)=1, forcing U_j occupied.
Equation (4) gives the same fact at j=0. Hence

    GH_j forces AB_j, CD_j, EF_j, U_j V_j.            (5)

Here AB_j means A_j--B_j, and similarly for the other pairs.

## 5. The actual-mate time inequalities in a canonical core

Suppose the five edges AB,CD,EF,GH,UV are present. The white endpoints B,D,U
have precisely the three possible occupied neighbours displayed above. Their
own mate cannot support their first freezing. Therefore

    tau(D)>tau(F),tau(H),
    tau(B)>tau(D),tau(F),
    tau(U)>tau(B),tau(F).                            (6)

In particular tau(U)>tau(F). Let k=(4,6+6j), the lower neighbour of F_j.
Apart from its own mate E, F sees V,G,k. V becomes kept only after U freezes,
which is later than F. Thus F must use both G and k. Saturation gives t_k=0 (a block x-site,
or the terminal x-site at j=m), so k must be an endpoint and

    tau(H_j)<tau(F_j),
    tau(mate(k))<tau(F_j)<tau(U_j).                  (7)

These are necessary time inequalities under the standing half-area equality
hypotheses, not an assumption that it follows the explicit construction's rank table.

## 6. Backward propagation through one complete block

Suppose j>=1, GH_j is forced, and the actual edge

    ZR KR = (4,s+5)--(4,s+6),  s=6j,

is forced. By (5) this core is canonical. Equation (7) yields

    tau(ZR)<tau(U_j).                               (8)

Use these further names:

    b=(3,s+4), g=(3,s+3), H=(3,s+2), G=(3,s+1),
    X=(4,s+4), L=(4,s+3), Y=(4,s+2), W=(4,s+1),
    k=(4,s), Z=(4,s-1).

Here H,G belong to core j-1. Saturation gives selected bottom sites below
ZR,L,W, blank bottom sites below X,Y,k, occupied white b,L,W, and no
selection at X,Y,k. These facts follow from the transmitted block state.

ZR has its selected bottom neighbour, its own mate KR, upper neighbour V_j
whose mate U_j is later by (8), and left neighbour X. Thus X must be an
endpoint with tau(mate(X))<tau(ZR). Its only remaining mates are b and L.
If Xb were actual, b would need the kept site V_j as one of its two witnesses:
its other possible nonmate neighbour is g, while its upper neighbour is blank.
This would give

    tau(U_j)<tau(b)<tau(ZR)<tau(U_j),

a contradiction. Therefore XL is forced and tau(L)<tau(ZR).
The white occupied site b cannot be selected: it sees the two endpoints V_j
and X. Its only unused mate is g, so gb is forced. Its two nonmate witnesses
are V_j and X, giving

    tau(U_j)<tau(b),    tau(L)<tau(b).                (9)

Next L has selected bottom neighbour, own mate X, upper neighbour g whose
mate b is later than L, and left neighbour Y. Hence Y is an endpoint and

    tau(mate(Y))<tau(L).

Its only unused mates are H and W. If YH were actual, H would need g as one
of its two nonmate witnesses, implying tau(b)<tau(H). This contradicts

    tau(H)<tau(L)<tau(ZR)<tau(U_j)<tau(b).

Thus YW is forced. Covering old endpoint H now forces GH, since g and Y
are already matched and its upper neighbour is blank. This proves GH_(j-1)
and then all five canonical core edges by (5).

It remains to pass the lower-row edge to the next block. H has only G as its
own mate, g and Y as possible nonmate occupied neighbours, so

    tau(W)<tau(H).

At W, the upper neighbour G is therefore unavailable before W freezes.
Besides selected bottom neighbour and own mate Y, only k can support it.
Thus k is an endpoint with tau(mate(k))<tau(W). Its right neighbour W is
already matched to Y, its upper neighbour F_(j-1) is already matched to
E_(j-1), and its bottom neighbour is blank. Matching disjointness therefore
forces kZ. This is the lower edge required for the next backward step.
The argument includes j=1: the pocket port inequality made U_0 occupied,
so (5)--(7) apply there.

At j=m the previously proved four terminal edges supply GH_m and ZR KR.
The j-step forces lower-edge indices 3j-1,3j-2,3j-3; all steps cover
0,...,3m-1. The terminal package supplies indices 3m and 3m+1, covering
all 0<=l<n. Backward induction also forces GH_j for all j, every old core
edge, every U_jV_j and every g_i b_i. Together with g_m Q
and the isolated old pair this proves M* subset M for every length.

## 7. There are no extra pocket matching edges

All possible remaining matching edges now lie in A', since the pair, band,
and terminal endpoints have their prescribed mates. The other crossing edges
at U_0,V_0,q are already used, and (5,6) is blank. The selected r=(5,5) and
occupied q force (5,4) blank.

The following potential pocket sites cannot be endpoints: (2,3),(4,0) each
have at most one possible occupied neighbour; (5,0),(5,1),(4,2),(5,3) each
have at most two (including the forced blank (5,4) for (5,3)). Complete
freezing excludes all of them by Section 2. The site (5,2) then has no
possible endpoint mate. After removing the already matched U_0,V_0,q and
selected r, any extra edge must therefore use only the four sites

    a=(3,3), u=(3,4), v=(4,3), z=(4,4).              (10)

Suppose an extra edge exists, so at least one of the black sites a,z is an
endpoint. Either has at most three possible occupied neighbours. Consequently
both u and v must be occupied. The white u is adjacent to the fixed endpoint
V_0 and to at least one new endpoint a or z, so u cannot be selected; it is
an endpoint. Its three possible occupied neighbours force both a,z occupied.
The site z cannot be selected, since it sees both u and the fixed endpoint q.
The site a cannot be selected, since it sees both occupied u and v. Thus a,z
are endpoints, and v cannot be selected because it sees both of them. All
four sites in (10) are endpoints and their actual mates lie within this square.

Now S={a,z} is a trap for either of its two internal perfect matchings. All
u,v neighbours have their mates in S. The only possible outside support is
(2,3) at a and q at z, one per member. This contradicts complete freezing.
There is no extra edge, proving M=M* and then the cardinalities in (2).

## 8. Sharp compensation, nonadditivity, and nonunique selections

If d>0, (2) excludes half-area equality. Integrality and the previous upper
bound give J<=18m+29; if d=0 the original bound applies. This proves (3).
The half-area family attains delta=0. The inherited all-g frozen attainer
has J=18m+29 and delta=1 for every m, proving sharpness of the binary bound.

In fact this latter family retains M0, all U_jV_j for j>=1 and all g_i b_i, but has
neither U_0V_0 nor any of the n=3m+2 lower Z_lK_l edges, nor terminal g_mQ.
It therefore has

    d=3m+4,   area/2-J=1.                            (11)

For an independently readable attaining family, start with (T*,M*) from the
half-area construction and set

    M_g=M* minus ({U_0V_0,g_mQ} union {Z_lK_l:0<=l<n}),
    T_g=(T* minus {(2,c)}) union {V_0,g_m} union {K_l:0<=l<n}.

Each newly selected K_l sees only its upper endpoint (F_j,H_j or b_j);
its lower-row neighbours become blank. New selected V_0 sees only F_0,
and g_m sees only H_m after removing (2,c). Old selections remain feasible.
The counts are |M_g|=6m+5 and |T_g|=12m+24, giving J_g=18m+29.
For freezing, first freeze A_j,C_j and the isolated pair, then E_j,G_j,
then internal g_i and V_j (j>=1) using the previous actual-mate witnesses.
H_m has two selected witnesses g_m,K_(3m+1). Returning from j=m downwards,
freeze F_j using G_j and selected K_(3j), then D_j,B_j and U_j when j>=1.
The next b_(j-1) uses V_j and selected K_(3j-1); H_(j-1) then uses g_(j-1)
and selected K_(3j-2). At j=0 only F_0,D_0,B_0 remain; U_0 is absent.
This covers every endpoint and proves the all-length frozen construction.
Its matching is exactly the inherited all-g matching; an immaterial left
selection swap distinguishes the two presentations.

Thus the proposed additive strengthening J<=area/2-d is false, by an explicit
fully frozen all-length family. Even forbidding the single terminal edge
and all 3m+2 lower edges together supplies only one unit in this example.
The obstruction concerns that additive rule, not the upper bound (3), and
makes no universal 5/6 claim. The two original half-unit reserve tokens in
this example must not be counted again for each missing edge.

Matching rigidity does not imply selection rigidity. Starting from the frozen
half-area construction, replace

    {(4,2),(5,1)} by {(5,0),(5,2)} in T.              (12)

The selection count is unchanged. The new selected pair (4,0),(5,0) and pair
(5,2),(5,3) each have just their partner as occupied neighbour; no endpoint
gets a different selected neighbour. Thus feasibility and every endpoint's
freezing process are unchanged. Both configurations have the same M* and
different T. This supplies a general example, not merely a solver witness.

## 9. Evidence and scope

The proof above is the all-length argument. Its new ingredients are the pocket
port slack, robust three-endpoint trap, strict actual-mate time propagation,
and final two-endpoint pocket trap. Finite optimization only suggested the
statement. An exploratory solver run concerning a different, unfrozen pocket
constraint timed out as UNKNOWN and establishes no assertion.

The accompanying standard-library verifier checks the geometry and all needed
actual time inequalities for the two selection families, the nonadditive
family, local EF matching cases and pocket traps, negative alternating-cycle
controls, and all eight isometries. The Lean audit covers the abstract traps,
strict time-cycle contradictions (including an auxiliary redundant vertical-mate exclusion), backwards induction, binary deficit bound
and token arithmetic. Coordinate-to-graph membership and witness exhaustion
remain the written proof plus executable controls; this is not an end-to-end
Lean coordinate theorem.

Reproduce the saved checks from the repository root:

    python3 develop/check_frozen_equality_matching_rigidity.py --output output/frozen-equality-matching-rigidity.json
    python3 develop/check_frozen_equality_matching_rigidity_formal.py --output output/frozen-equality-matching-rigidity-formal.json

The saved solver-free run passes 25 lengths through m=100, 100 fully frozen
boards, 488 core-time and 463 backwards-step controls, 100 original-token
allocations, 123 actual pocket-port controls, three noncanonical EF traps,
six actual extra-square traps, 292 nonfrozen short alternating-cycle controls,
12 independent synchronous replays and 24 isometries. Both attaining
selection variants have exactly the same endpoint freezing times.

The local Lean 4.33.0 audit passes 16 declarations with only standard logical
axioms, no admitted proofs and no custom mathematical axioms. It includes an
arbitrary-length backwards induction, rather than a collection of fixed-size
instances. Its exact adapter limits are stated above and in the receipt.

The [independent Oracle audit](../output/frozen-equality-matching-rigidity-oracle.json)
returns ACCEPT (observed gpt_6, pro). It accepts the new all-length rigidity,
actual-mate propagation, final pocket trap, binary compensation and
nonadditivity, with the earlier upper bound, equality patterns, pocket
certificate, terminal-edge lemma and attainers as premises. It performs no
code execution. Its equality-scope, unused-mate and terminal-index wording
clarifications are incorporated; the direct all-g construction above is an
expository consequence supplied by the reviewer and independently checked.

## 10. Ambient limitation resolved by a zero-charge cap

The freezing hypothesis above is LOCAL to this isolated board. It cannot be
replaced by global freezing in a larger board plus matching closure of the
old region. The [ambient activation construction](AMBIENT_BAND_PORT_ACTIVATION.md)
preserves its T/P footprint and local half-area but switches its last two
horizontal edges to verticals. A six-column zero-charge cap makes the whole
union completely frozen, although the restricted band has four unfrozen
endpoints. Arbitrarily many such regions can occur at zero reserve. This
refutes that ambient transfer rule; the theorem proved here is unchanged.
