# Two guard types: a sharp merger frontier and forced guard retention under freezing

26 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

We enlarge the [joint withdrawal/rematching theorem](WITHDRAWAL_REMATCHING_JOINT_BOUND.md)
to a second family of old selections. The newly opened regions include a
seven-site tree and a thirteen-site region with cycles. An integer weighted
certificate proves a sharp upper bound for arbitrary actual rematching.
The additional lower-guard withdrawal permissions do not increase that bound.
Complete freezing, however, forces the lower guard whenever its upper/right
guard remains selected. Explicit sharp configurations can violate this
implication only by leaving exactly one endpoint per lower withdrawal unfrozen.

## 1. The two-guard theorem

Fix the original b=1 family (T0,M0), P0=V(M0), on the 6-by-(6k+4) board,
k>=2. Its coordinates are recorded in the
[sharp-completion note](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md).
For each i=0,...,k-2 define

    c_i=9+6i,   g_i=(3,c_i),   h_i=(4,c_i-1).

Both g_i and h_i are old selections. Let G,H be ANY subsets of these indices,
g=|G|, h=|H|. Suppose T,P are disjoint, every selected site has at most one
occupied neighbour, P0 is a subset of P, and

    T0 minus {g_i:i in G} minus {h_i:i in H} is a subset of T.

Let M be ANY actual grid matching of exactly P. Old edges may be rematched,
and additional endpoints and selections are unrestricted. Then

    |T|+|M| <= 17k+12+g = area/2-(k-g).              (1)

The bound is sharp for every pair (G,H), including among completely frozen
configurations: the previous all-subset g-withdrawal attainer retains every
h_i and remains allowed here. These are permissions to withdraw, so sites
in G or H may be selected again. The upper bound covers their actual deletion
as well. A separate construction below actually deletes an arbitrary set
of h_i at the sharp value with G empty, but cannot be completely frozen.

Thus adding lower-guard permissions has zero extra cost in (1). It is not
valid to assign a further independent one-unit loss to every h_i merely
because the g_i had that cost. No endpoint site of P0 may be deleted, and
no other old-T withdrawal is included in this theorem.

## 2. The exact free slots, including both interactions

Retained old T sites with old P0 neighbours force all their other neighbours
blank. This uses occupation only and survives arbitrary rematching. Apart
from the fixed 15-site pocket, the free graph splits into k-1 disjoint slots
and two final isolated sites. Slot i contains the old gate, star and isolated
site with columns between c_i-2 and c_i+2. The four activation states are:

| Allowed guard withdrawals in this slot | Free components | Contribution bound |
| --- | --- | --- |
| neither | gate + star + isolated site | 1+3+1=5 |
| g only | nine-site tree + isolated site | 6+1=7 |
| h only | gate + seven-site tree | 1+5=6 |
| both | one thirteen-site region | 8 |

Here contribution means new T plus HALF the number of new endpoints, even
when their actual mates lie outside the slot. The fixed pocket contributes
at most 9+1/2 by the preceding boundary-aware proof; each final isolated
site contributes at most one.

For completeness the exact freed sites relative to the original free graph
are {d,g,b} for g only, {h,z} for h only, and {d,g,b,h,e,z} for both, where
for c=c_i

    d=(2,c), u=(2,c+2), g=(3,c), b=(3,c+1), v=(3,c+2),
    h=(4,c-1), e=(4,c), a=(4,c+1),
    L=(5,c-2), z=(5,c-1), l=(5,c), s=(5,c+1), r=(5,c+2).

The site e is available ONLY when both guards are removed from the retained
set: either g or h alone forces it blank. Removing h frees z but does not
free (4,c-2), which is still guarded by retained old T(4,c-3). The same
row-by-row deletion that gave the preceding free table proves there are
no further freed sites. Different slots remain disjoint with no free-grid
edge between them, even at consecutive active indices. Matching edges
to old P0 sites are allowed throughout.

The both-active internal edges are

    dg,gb,ge,bv,ba,uv,he,hz,ea,el,as,zL,zl,ls,sr.

The old endpoint-neighbour counts are one at g,v,h, two at u, and zero
elsewhere. This is the thirteen-site cyclic case missing from the old tree
argument; simply adding independent guard costs would overlook its interaction.

## 3. The seven-site capacity is five under the actual matching

In the h-only case its new component is {h,a,L,z,l,s,r}, with edges
hz,zL,zl,ls,sa,sr. Only h has an old endpoint neighbour. Write t_x for its
selection indicator, p_x for its endpoint indicator, o_x=t_x+p_x, and

    F=sum_x(t_x+o_x)=2 newT+newP.

Add these feasibility inequalities, each with weight one:

    t_h+o_z<=1;
    t_z+o_h+o_L<=2;       t_s+o_a+o_r<=2;
    t_a,t_r,t_L,t_l<=1;   o_l,o_s<=1.

Their left sides sum EXACTLY to F, and their right sides sum to 11. If F=11,
all bounds must be tight, so a,l,r are selected and s is occupied. The wedge
at s makes t_s=0, hence s is an endpoint. Its only eligible endpoint neighbours
are a,l,r: all three are selected. It has no possible actual mate, a
contradiction. Therefore F<=10, proving contribution at most five.

The excluded occupation of charge eleven really exists if matchability is
discarded: select h,a,L,l,r and occupy s as an endpoint. This is feasible
for the selection constraints but s is isolated in the endpoint graph.
The proof therefore uses actual matching coverage at exactly the place
where the occupation-only bound would be insufficient.

## 4. A general thirteen-site integer certificate

Use the thirteen names above, and set F=sum(t_x+o_x) again. We have t_u=0,
t_e<=o_e, t_l<=o_l. The following table lists all other inequalities and
their nonnegative integer weights:

| Weight | Feasibility inequality |
| --- | --- |
| 3 | t_g+o_d<=1 |
| 3 | t_v+o_u<=1 |
| 2 | t_h+o_e<=1 |
| 1 | t_h+o_z<=1 |
| 3 | t_b+o_g+o_v<=2 |
| 2 | t_e+o_h+o_l<=2 |
| 2 | t_a+o_b+o_e<=2 |
| 1 | t_a+o_b+o_s<=2 |
| 1 | t_z+o_h+o_L<=2 |
| 2 | t_z+o_L+o_l<=2 |
| 2 | t_l+o_z+o_s<=2 |
| 3 | t_s+o_a+o_r<=2 |
| 3 each | t_d,t_L,t_r<=1 |

Also add 3t_u<=0. Let A be the sum of these displayed left sides with
their weights. Their right sides sum to 50. Direct coefficient accounting
gives the universal identity

    A+t_e+t_l = 3F+o_e+o_l.

The two selection-subset inequalities imply 3F<=A<=50. Since F is an
integer, F<=16; equivalently this component contributes at most eight.
No matching-boundary restriction or freezing hypothesis was used. The
identity and all weights are explicit, so a solver or finite enumeration
is not needed to prove the inequality. Integer rounding applies to the
integer DOUBLED contribution F here; it does not round half-weight
contributions individually to whole numbers.

The previously proved gate, star and nine-site bounds establish the other
three rows of the slot table. Each slot's contribution is at most
5+2*1_(i in G)+1_(i in H), including the both-active state.

## 5. Sum distinct components, then round the unique pocket slack once

The old retained contribution is

    |T0 minus withdrawn permissions|+|P0|/2=12k+6-g-h.

Every new endpoint belongs to exactly one free component, independent of its
mate, so contributions add without double counting. The free contribution
is at most

    9+1/2 + 5(k-1)+2g+h+2 = 5k+6+1/2+2g+h.

Adding gives |T|+|M|<=17k+12+1/2+g. The objective is an integer, yielding
(1). This final rounding occurs once, for the single fixed pocket. The
additional h permission cancels exactly between the old retained count
and the seven/thirteen-site capacities.

The top strip still has doubled surplus 1-k. Thus the full original-tile
compensation theorem from the preceding note also extends unchanged:

    exterior Cplus >= exterior Cminus+(k-1)+2(k-g).

Positive tokens identified by original tile and half-unit number pay all
exterior negative charges first, then the net strip deficit, leaving at
least 2(k-g) distinct half tokens. No extra credit is charged to H, and
no already-spent token is also kept in the remainder. This is global net
compensation, without a local/directional routing claim for individual D4.

## 6. Complete freezing forces g selected implies h selected

For EVERY allowed configuration, if all actual endpoints are completely
frozen, then, at every internal index,

    g_i in T  implies  h_i in T.                     (2)

This is not restricted to maximizers. Let W=(3,c-1), an old endpoint.
If g is selected, its old neighbour W forces d,b,e blank. Retained old
T(4,c-3) forces (4,c-2) blank, and retained old T(1,c-1) forces (2,c-1)
blank. Consequently h has only W,z as possible occupied neighbours.
If h were an endpoint it would have at most two occupied neighbours.
One is its actual mate, which cannot serve as a strict freezing witness;
at most one other witness remains. Such an endpoint can never freeze.

If h is not an endpoint and is not selected, W has only its old neighbour
(3,c-2) and selected g occupied. Its actual mate must be (3,c-2), since
g is selected. Again it has only its mate and one other occupied neighbour,
and cannot freeze. Both alternatives contradict complete freezing, proving
(2). This is a local two-alternative trapping argument; outside support,
arbitrary rematching and a later freezing time cannot repair either trap.

In particular, actual lower withdrawal in a completely frozen configuration
requires actual upper withdrawal as well. The capacity theorem's permission
to withdraw h must not be mistaken for existence of a completely frozen
attainer that actually deletes h while retaining g.

## 7. A sharp all-k family with exactly the lower endpoints unfrozen

Start with the completely frozen maximum (T*,M0) of the sharp-completion
note. For any H subset of {0,...,k-2}, remove each h_i from T* and add
the actual matching edge

    h_i=(4,8+6i) -- z_i=(5,8+6i).

Keep all g_i selected. Each z_i sees the two unchanged selections
L_i=(5,7+6i), l_i=(5,9+6i). Previously each had no occupied neighbour,
so the added endpoints preserve feasibility. Each new h_i has only its
mate z_i and old W_i as occupied neighbours. The counts are

    |T|=13k+11-|H|,  |M|=4k+1+|H|,
    |T|+|M|=17k+12.

Thus actual lower withdrawal can retain the sharp numerical objective.
Each h_i is nevertheless permanently unfrozen by the degree-two argument.
Every other endpoint does freeze. For an explicit uniform certificate, use
old core names A,B,C,D,E,F,G,H from the rematching note (here H_core is W;
it is distinct from the index set H and lower guard h):

| Endpoint type | Strict rank |
| --- | --- |
| old A,C; every new z_i; isolated old left pair | 0 |
| old E,H_core | 1 |
| old F,G | 2 |
| old D | 3 |
| old B | 4 |

Retain all original old-core witness coordinates. The former lower-T
witness at h_i is now an endpoint whose actual mate z_i has rank zero,
so it remains usable by H_core at rank one. All other original witnesses
have mates of smaller displayed rank. Each new z_i uses its two selected
witnesses L_i,l_i. This proves a strict partial certificate covering exactly
P minus {h_i:i in H} for every k,H. It also agrees with independent iterative
freezing. For nonempty H these configurations refute the idea that one
may delete h while keeping g and still obtain complete freezing; they do
not refute the sharp counting bound or the half-area target.

## 8. Verification, formal scope, and remaining geometric issue

The standard-library checker verifies every feasible local occupation:
110,130 thirteen-site patterns and 975 seven-site patterns. It checks the
integer certificate, the unique unmatchable charge-eleven case, the actual
free graph and all four slot states. It exhausts four-state slot strings
through k=4 and tests larger joint patterns through k=128. The 617 board
models include 133 old-edge rematchings, 156 sharp frozen attainers and
45 exact-trap families. There are 2,216 actual lower withdrawals, 3,805
guard-implication controls and 8,302 independently replayed partial strict-rank
events. All 617 actual original-tile payment maps are injective and account
for external negative charges and remaining half units.

Lean 4.33.0 checks 14 declarations covering the universal thirteen-site
identity/capacity, seven-site identity/equality/mate-coverage bound, all-k
slot count and lower-permission cancellation, sharp margin, strict-mate
witness exclusion, selection forced by two alternative traps, and the patch
count/exterior cut. No sorry, native_decide or new axioms are used. The
all-k coordinate and actual-matching adapters, the guard geometry and explicit
patch freezing schedule remain general written proofs with executable checks.
No end-to-end formal grid theorem is claimed.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_lower_guard_merger_frontier.py --output output/lower-guard-merger-frontier-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_lower_guard_merger_frontier_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/lower-guard-merger-frontier-formal-validation.json

The next issue is withdrawal opening connections BETWEEN these free slots,
or deletion of old P0 sites: disjoint slot capacities then no longer supply
the geometric cut automatically. Individual direction-constrained D4 routing,
arbitrary mixed footprints and a universal improvement of 5/6 remain open.
The submitted 11 October manuscript, public main/PR3, shared CI, C4 work and
correspondence are preserved. No Mail operations are performed at this stage.
