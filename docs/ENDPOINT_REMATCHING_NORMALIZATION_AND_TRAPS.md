# Arbitrary rematching: sharp compensation, even-core normalization, and frozen rigidity

26 October 2026. Wenlin Zhang and Haobo Ma. Independent research continuation.

We remove the retained-old-edge assumption from the preceding
[endpoint-invasion theorem](ENDPOINT_INVASION_SHARP_STRIPS.md). Retaining the
old SELECTED sites and old ENDPOINT sites suffices. Every actual perfect
matching can be normalized back to one retaining all old edges, without
changing a single occupied site. Moreover, a completely frozen matching must
already retain those old edges: every noncanonical core has an unavoidable
three-endpoint freezing trap. An explicit exponentially large matching family
also has a matching-specific no-reuse allocation of all actual D4 demands.

## 1. The enlarged sharp theorem

Fix k>=1 and the original 6-by-(6k+4) b=1 family (T0,M0), with P0=V(M0),
as defined in [the sharp-completion note](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md).
Suppose T0 is a subset of T, P0 is a subset of P, T and P are disjoint,
every selected site has at most one occupied neighbour, and M is ANY grid
perfect matching of exactly P. No old matching edge is prescribed. Then

    |T|+|M| <= 17k+12 = area/2-k.                      (1)

The bound is sharp. The preceding fully frozen invading completion already
attains it. Furthermore, if (T,M) is completely frozen under its ACTUAL mate
map, then M0 is necessarily a subset of M. Consequently every newly matched
endpoint lies in the same fixed 15-vertex pocket from the preceding note,
and there are at most seven genuinely new matching edges, independent of k.
Seven remains only a uniform upper bound, not an asserted exact maximum.

Old selections and old endpoint sites are retained throughout. We have not
proved (1) after deleting either, or for arbitrary endpoint footprints. In
particular this is not a universal improvement of the 5/6 bound.

## 2. An even island with two adjacent ports

We first state the general matching argument. Let C be an even set of old
endpoint sites with a prescribed internal perfect matching N. Suppose the
only neighbours of C that can be endpoints outside C are two distinct sites
u,v, and uv is itself a permitted matching edge. In any actual perfect
matching covering C, let I be the internal edges and B the crossing edges.
Counting endpoints of C exactly once gives

    |C| = 2|I|+|B|.

At most two crossing edges are possible, one using u and one using v, since
an actual matching cannot use either port twice. Thus |B| is either 0 or 2.
With no crossing edges replace the internal matching by N. With two, both
ports are actual endpoints already matched into C; the region C union {u,v}
is closed under the actual matching. Replace its edges by N union {uv}.
No endpoint is added or removed, and the number of matching edges is unchanged.
All replacement edges are permitted. Edges outside the closed region remain
untouched. For pairwise disjoint islands and distinct ports these operations
can be performed simultaneously.

This proof neither assumes an exchange sequence exists in advance nor changes
the selected set. Feasibility depends only on T union P and is preserved.
Freezing depends on the mate map and is treated separately in Section 4.

## 3. Why every old core satisfies this lemma

Use these names for the first eight-endpoint core and its two ports:

    A=(1,5), B=(1,6), C=(1,7), D=(2,7),
    E=(2,6), F=(3,6), G=(3,7), H=(3,8),
    U=(2,5), V=(3,5).

Core i is translated by (r,c)->(r,c+6i). Its prescribed old edges are

    AB, CD, EF, GH.

All additional occupied sites still lie in the free set F_free classified
row by row in Section 2 of the preceding note: anchoring uses retained T0
and P0, so does not require retaining M0. The only F_free neighbours of each
old core are precisely its U,V. No old core has an old endpoint neighbour in
another core. The isolated old left pair has no F_free neighbours and its
matching is forced. Distinct cores and their two ports are disjoint, and UV
is a vertical grid edge. These assertions follow by substituting the old
coordinates into that row table; they hold for every k.

Normalize each core by Section 2. The result Mhat contains M0 and has exactly
the original P, T and |M|. The preceding retained-edge theorem therefore
applies to (T,Mhat), proving (1) for the original arbitrary M. Top-strip
occupation and every physical tile charge are unchanged. Individual actual
exports and BP credits can change; we do not transport a matching-dependent
payment map merely by claiming occupation is unchanged.

## 4. All three noncanonical matchings have a fixed freezing trap

Here is a direct matching classification, used as a local mathematical case
split. The site H has only G as an eligible endpoint neighbour, so GH is
forced. With no core crossing, F must pair with E, then D with C and B with A.
Thus a zero-crossing core already has the old matching.

With two crossings both U,V are matched into the core. V has only F as an
old endpoint neighbour, so FV is forced. After removing GH,FV the remaining
six vertices form the cycle A-B-C-D-E-U-A with chord BE. If A pairs with B,
the other edges are CD,EU. If A pairs with U, the remaining B-C-D-E square
has either BC,DE or BE,CD. Hence the three noncanonical possibilities are

| Mode | Actual edges on core plus ports |
| --- | --- |
| 1 | AB, CD, EU, FV, GH |
| 2 | AU, BC, DE, FV, GH |
| 3 | AU, BE, CD, FV, GH |

The normalized fourth possibility is AB,CD,EF,GH,UV. The classification is a
forced-edge proof on a fixed local graph, not an inference from finite search.
It does not forbid V alone from being matched elsewhere in the first pocket;
that possibility has zero core crossings and preserves the old core edges.

In ALL three noncanonical modes set S={B,U,D}. No neighbour of a vertex in S
can be selected: its possible occupied neighbours are fixed old endpoints
or U,V, which are endpoints in these modes. The other grid neighbours are
forced blank by retained anchored T0. The mate of all but at most one of
those occupied neighbours lies in S. Explicitly the outside-S mate witnesses
are: none at B, only V at U (whose mate is F), and only G at D (whose mate
is H). This list holds for each of the three modes.

If any endpoint in S froze, take the FIRST freezing layer meeting S. A
retained endpoint-neighbour is usable only when its mate has already frozen;
at this layer all neighbours whose mates belong to S are unavailable. There
are no T neighbours and at most one usable outside-S witness. Two distinct
witnesses are required, a contradiction. Therefore NONE of B,U,D ever
freezes, even if every endpoint outside S were available as support. This
is robust under every allowed additional T/P site, not merely under the
specific attaining completion.

Equivalently, in strict ranks, any certified member of S would require an
earlier certified member of S, contradicting a minimum rank. The argument
also excludes partial freezing certificates containing even one member of S.
Complete freezing consequently forbids every noncanonical old core. All
old M0 edges must be retained; the prior frozen-localization theorem applies.

## 5. Exponentially many sharp matchings and an actual no-reuse ledger

Take the preceding sharp invading completion Tdag,Mdag. For each repeated
gate i=1,...,k-1, remove the selection V_i and add both U_i,V_i as endpoints,
initially matched by U_i V_i. Call the resulting occupation Tbar,Pbar. Each
upper U_i was previously blank, and each lower V_i already saw only its old
P neighbour. Replacing that selection by an endpoint and adding U_i changes
no other selected site's occupied neighbours, by the free-component table.
Thus the occupation is feasible for every k. Its counts are

    |Tbar|=12k+11, |Pbar|=10k+2, |Mbar|=5k+1,
    |Tbar|+|Mbar|=17k+12.

The induced endpoint graph is k disjoint copies of the ten-site core/ports
graph, plus the isolated old left edge. Each core has exactly the four
matchings just classified. Hence there are exactly 4^k actual perfect
matchings, ALL attaining (1). For k>=2 none is completely frozen: a
noncanonical core has the trap above, while a canonical repeated gate has
the degree-two lower-endpoint obstruction from the preceding note.

The original single-invader occupation Tdag,Pdag instead has four matchings,
since only the first core has ports. Its normalized matching is fully frozen;
the other three contain S. Thus exactly one of its four matchings is fully
frozen, for every k, at the same sharp objective.

For Tbar,Pbar, let n3 be the number of mode-3 cores. The actual top-strip
inventory, reconstructed with the ORIGINAL matching M, is exactly

    boundary budget B=1, unused BP half credits=n3,
    unported D4 exports=k+n3, unused forest end slots=0,
    ported exports=1, safe-cross refund=0.

The original D4 in a core is at C_i for modes 0,1, at A_i for mode 2, and
at BOTH A_i,C_i for mode 3. In mode 3 only, B_i is a BP whose actual mate
E_i lies outside the strip, yielding one unused-BP half credit. Therefore

    2S_strip=1+n3-(k+n3)=1-k.

There is an explicit allocation for every mode string. Give each core's
original exterior half-unit rebate tile Q_(1,4+3i) to C_i when it is a D4,
otherwise to A_i (mode 2). In mode 3 give that core's DIFFERENT unused-BP
half credit at B_i to the additional D4 at A_i. All targets and all resource
identities are distinct. The BP credits are SPENT here and cannot also be
counted as unspent intervals, beta units or full-unit reserves.

The exterior tile charges remain exactly those of the preceding invading
completion: replacing one V selection by two port endpoints leaves c(Q)
unchanged. Thus Q_(1,2) is still neutral, Q_(1,1) replaces its old full
unit, and Q_(1,2+3i), i>=1, retain the other k-1 full units. Every rebate
still has c=1; the boundary Q_(1,0) still has c=-1, paid once by B=1.
Every other exterior tile has c=0. The actual complete ledger is

    (1+n3)-(k+n3)+(k-1)+2k=2k.

This proves a matching-specific physical compensation allocation, with k
unspent whole units, for an explicit family with 4^k actual rematchings.
The arbitrary-extension theorem (1) is more general; the displayed payment
map is not asserted for arbitrary reselected additional sites.

## 6. Verification and formal scope

The standard-library checker verifies the boundary geometry for
k=1,...,16,32,64,128; independently enumerates the four LOCAL matchings as
a control of the written classification; tests all mode strings through k=4
and larger representative strings; normalizes arbitrary actual matchings;
and checks that no trap vertex ever freezes under the independently iterated
process. It also varies additional T and P, checks sharpness, reconstructs
actual top-strip credits and every exterior charge, and verifies resource
identity injection for every actual D4. The k=2 fixture has two noncanonical
cores, unchanged objective 46 and whole margin 2, with six explicitly
unfrozen trap endpoints. Its normalized matching has the same T and P.

Lean 4.33.0 checks 14 declarations: the universal closed-region matching
splice, even-cut/two-port arithmetic, strict-rank trap exclusion for partial
certificates, scalar-bound transfer, the three local trap geometries, resource
identity injection and exact refund-demand cancellation. The all-k geometric
port adapter, finite cut-count identity derived from an actual matching,
forced-edge classification and all-k actual payment adapter remain written
proofs with executable checks. No end-to-end formal board theorem is claimed.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_endpoint_rematching_normalization.py --output output/endpoint-rematching-normalization-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_endpoint_rematching_normalization_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/endpoint-rematching-normalization-formal-validation.json

The remaining structural issue is withdrawal of old T or old P: it can open
more than two ports, destroy the forced blanks, and break the rank trap.
General bent/mixed configurations and the universal 5/6 improvement remain
open. The submitted 11 October manuscript, public main, PR #3, shared CI,
C4/star-forming work and correspondence are preserved.
