# Successor ownership gives sharp compensation; connected bands need a stronger cut

26 October 2026. Wenlin Zhang and Haobo Ma. Research note.

We prove another exact compensation theorem for the occupied-strip family,
including arbitrary actual rematching. A change of ownership of isolated
sites avoids charging an additional loss for a second lower-guard family.
We then give a rational obstruction, at every chain length, to a specified
collection of local inequalities. A separate actual integer configuration
refutes the proposed isolated connected-component cut under arbitrary
rematching. It leaves the whole-board target intact and is not completely
frozen. The two obstructions have distinct scopes.

## 1. Sharp successor-guard compensation theorem

Use the b=1 family (T0,M0) on the 6-by-(6k+4) grid, k>=2, with
P0=V(M0). Coordinates and its completely frozen sharp completion (T*,M0)
are given in [the completion note](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md).
In particular |T0|=8k+5, |P0|=8k+2, |T*|=13k+11 and |M0|=4k+1.
For 0<=i<=k-2 write

    c_i=9+6i,
    g_i=(3,c_i), h_i=(4,c_i-1), f_i=(4,c_i+3).

The new f_i is the guard previously indexed (4,6+6j) with j=i+1.
The leftmost guard (4,6) is excluded. Every h_i remains selected here.

**Theorem 1.** Let G,F be arbitrary subsets of {0,...,k-2}. Let T,P be
disjoint sets such that every vertex of T has at most one neighbour in
T union P, and let M be an actual grid matching with endpoint set exactly P.
Assume P0 is contained in P and

    R = T0 minus {g_i:i in G} minus {f_i:i in F} is contained in T.

Then

    |T|+|M| <= 17k+12+|G| = area/2-(k-|G|).          (1)

For every permissions pair G,F equality is attained by a completely frozen
configuration. The construction is the earlier g-withdrawal attainer, which
retains all f_i. Thus the maximum is exact, and adding any F permissions
has zero further cost. Permissions do not require actual deletion.
Old matching edges need not be retained; all old endpoints must be retained.
No freezing assumption is needed for the upper bound.

### 1.1 A disjoint cover using successor isolated sites

Let U be the set of sites outside R union P0 not forced blank by a retained
selection adjacent to P0. Explicitly set newT=T minus R and newP=P minus P0;
a restored permitted selection belongs to newT. Both increments lie in U.
The old free graph had one fixed 15-site pocket, k-1 gate/star pairs, and
k+1 isolated bottom sites. Instead of attaching the preceding isolate to
slot i, attach its **successor**

    R_i=(5,c_i+4)=(5,13+6i).

The two unassigned isolates are (5,7) and (5,6k+3). Their columns lie outside
the list 13,19,...,6k+1. The map i -> R_i is injective.

For c=c_i use these names:

    d=(2,c), u=(2,c+2),
    g=(3,c), b=(3,c+1), v=(3,c+2),
    a=(4,c+1), x=(4,c+2), f=(4,c+3),
    l=(5,c), s=(5,c+1), r=(5,c+2), z=(5,c+3), R=(5,c+4).

With neither permission, the slot is {u,v}, {a,l,s,r}, {R}. Removing g
from the retained set adds exactly d,g,b. Removing f adds exactly x,f,z.
The additions are independent. Retained h_i forces (4,c) blank, and the
next retained h, or the terminal retained guard (4,6k+2), forces (4,c+4) and
(5,c+5) blank. Hence no free edge joins consecutive slots. The pocket and
its two possible old-P0 boundary vertices remain unchanged: (2,5),(3,5).
These give three possible edges to P0, namely (2,5)--(1,5),
(2,5)--(2,6), and (3,5)--(3,6). A port means a vertex, not a unique edge.

This also proves the cover for every k: inspect rows2,3,4,5 using the
displayed sites and blockers; rows0,1 have no newly available sites.
The cases at the first and last slot leave exactly the two stated isolates.
Thus U has 7k+10+3|G|+3|F| sites, and the four slot states are:

| Permissions | Free pieces | Maximum doubled contribution |
| --- | --- | --- |
| neither | gate + star + successor isolate | 2+6+2=10 |
| g only | old nine-site tree + successor isolate | 12+2=14 |
| f only | ten-site cyclic region {u,v,a,x,f,l,s,r,z,R} | 12 |
| g and f | thirteen-site region with all displayed sites | 16 |

Doubled contribution is Q=2 newT+newP, independent of the locations of
actual mates. An endpoint is counted once at its own site, including when
its mate is in P0. The first two capacities were proved in the
[rematching note](WITHDRAWAL_REMATCHING_JOINT_BOUND.md); the next two follow below.

### 1.2 The ten-site region: matching removes the equality excess

Its internal edges are uv,vx,ax,as,xf,xr,fz,ls,sr,rz,zR. It has two
independent cycles, including squares a-x-r-s-a and x-f-z-r-x. The
certificate below uses the actual grid edges and needs no acyclicity.

Write t_v,p_v for selection/endpoint indicators and o_v=t_v+p_v. For the
ten sites, Q=sum(t_v+o_v). Add the following inequalities with weight one:

    t_u=0;                     o_v<=1;
    t_v+o_u<=1;                t_x+o_a+o_r<=2;
    t_f+o_z<=1;                t_l<=1;
    t_s+o_a+o_l<=2;            t_r+o_x+o_s<=2;
    t_z+o_f+o_R<=2;            t_R<=1.

If B is their summed left side, their right sides sum to13 and

    B+t_a = Q+o_a.

Since t_a<=o_a, Q<=B<=13. If Q=13, every displayed upper bound is tight
and t_a=o_a. In particular t_l=t_R=1. The selected-subset bounds give
o_l=o_R=1 and t_s+o_a=1.

If t_s=1, then o_a=0. The genuine wedge t_s+o_l+o_r<=2 gives o_r=0,
so the tight x wedge forces t_x=2, impossible. Hence t_s=0 and t_a=o_a=1.
The wedge t_a+o_x+o_s<=2 gives o_x+o_s<=1; tightness at r forces
t_r=1 and o_x+o_s=1. If o_s=0, then o_x=1. The wedge
t_r+o_x+o_z<=2 forces o_z=0, while the tight f anchor forces t_f=1.
This contradicts the other f anchor t_f+o_x<=1. Therefore o_s=1.

Thus equality forces s to be an endpoint and a,l,r to be selected. Those
are **all** possible occupied neighbours of s: it has no old endpoint
neighbour or other grid neighbour in U. It has no endpoint mate, contrary
to actual matching coverage. Consequently Q<=12.

There are two feasible integer occupation patterns of charge13 if actual
matching coverage is omitted. The matching assumption is essential here.

### 1.3 Thirteen-site universal weighted certificate

Use the thirteen names in Section1.1, and Q=sum(t+o). In addition to
t_u=0 and t_x<=o_x, t_r<=o_r, use these nonnegative integer weights:

| Weight | Inequality |
| --- | --- |
| 3 | t_g+o_d<=1 |
| 3 | t_v+o_u<=1 |
| 2 | t_f+o_x<=1 |
| 1 | t_f+o_z<=1 |
| 1 | t_b+o_g+o_v<=2 |
| 2 | t_b+o_g+o_a<=2 |
| 2 | t_a+o_b+o_x<=2 |
| 1 | t_a+o_b+o_s<=2 |
| 2 | t_x+o_v+o_r<=2 |
| 1 | t_s+o_a+o_l<=2 |
| 2 | t_s+o_l+o_r<=2 |
| 2 | t_r+o_s+o_z<=2 |
| 3 | t_z+o_f+o_R<=2 |
| 3 each | t_d,t_l,t_R<=1 |

Add 3t_u<=0. If A is the resulting weighted left side, direct coefficient
accounting gives the identity

    A+t_x+t_r = 3Q+o_x+o_r,       A<=50.

It follows that 3Q<=50. Since Q is an integer, Q<=16. This certificate
allows mates outside the region and uses no freezing hypothesis.

### 1.4 Sum once; remove one half-unit slack once

The retained contribution is |R|+|P0|/2=12k+6-|G|-|F|. Each slot has
contribution at most 5+2*1_G+1_F. The unique pocket contributes at most
9+1/2 by the previously proved boundary-aware actual-matching certificate;
the two remaining isolates contribute at most2. Therefore

    |T|+|M| <= 12k+6-|G|-|F| + 9+1/2+5(k-1)+2|G|+|F|+2
             =17k+12+|G|+1/2.

The integer objective gives (1). This is one global rounding, not a
separate rounding of each half-weight contribution. The predecessor
g-attainer is valid for every F and proves sharpness.

### 1.5 Actual original-tile compensation without reused credit

Use the fixed disjoint original2-by-2 tile partition, rather than all
overlapping windows. For a tile D write c(D)=4-2|T intersect D|-|P intersect D|.
The top strip still has total1-k. By (1), the exterior signed charge is
at least3k-1-2|G|. Let Cplus sum positive exterior charges and Cminus be
the absolute sum of negative exterior charges. Then

    Cplus >= Cminus+(k-1)+2(k-|G|).                   (2)

Label each actual positive half-unit by (original tile,unit index). In a
fixed order first pay all exterior negative half-units, then the k-1 net
strip half-demands, and reserve the remaining tokens. The allocation is
injective; no paid token is also reserved. At least2(k-|G|) remain.
Both local ownership and the final physical-token accounting are explicit.
This is a global net allocation; it makes no direction-constrained routing
claim for individual D4 exports, or claim of whole-unit reserves in original tiles.

### 1.6 Sharp actual f deletion and its precise freezing defect

For any F start at (T*,M0), remove each f_i from T*, and add edge
f_i--z_i, z_i=(5,c_i+3). This gives

    |T|=13k+11-|F|, |M|=4k+1+|F|, |T|+|M|=17k+12.

Each z_i has selected neighbours (5,c_i+2),(5,c_i+4), so it freezes at
rank0. Retain all old strict ranks and witness coordinates from the b=1
family. The only altered old witness is at (3,c_i+3), whose rank is1;
its former selected witness f_i is now an endpoint with rank0 mate z_i.
All old certificates therefore remain strict. Every endpoint except the
new f_i freezes. Each f_i has only its actual mate z_i and old endpoint
(3,c_i+3) occupied nearby; its own mate cannot be a strict witness, so
it never freezes. This proves the exact defect for every k,F. It does
not assert that every actual-f-deletion maximizer has this defect.

## 2. A barrier for fully connected G/H/F chains

Now remove from the retained set all g_i,h_i for i=0,...,m-1 and f_i
for i=0,...,m-2 on the k=m+1 board, m>=2. These remain permissions:
the actual configuration may select some permitted sites again. The
newly available free region containing g_0 is C_m:

    row2: 9+6j,11+6j                   (0<=j<m)
    row3: 9+6j,10+6j,11+6j             (0<=j<m)
    row4: every column8,...,6m+4
    row5: every column7,...,6m+5.

It is connected and has17m-4 sites. Outside it remain the fixed pocket
and isolates (5,6m+7),(5,6m+9). Its old-P0 neighbour counts are2 at row2 residue5,
1 at row3 residues3,5 and row4 residues0,1,2, and0 elsewhere. The retained
old-T count is5m+14 and the old matching size is4m+5.

The natural connected cut that would cancel the extra m-1 guard
withdrawals at the same rate is

    Q(C_m) <= 18m-2.                                (3)

Together with the pocket/isolate bounds and one global rounding, (3)
would give |T|+|M|<=18m+29=17k+12+m. The actual configuration in Section2.3
refutes (3) in this arbitrary-rematching permissions class. Before giving
that example, we identify a separate bulk weakness in the local relaxation.

### 2.1 The exact relaxation being obstructed

Allow real variables 0<=t_v<=o_v<=1 on C_m. Put d_v equal to its number
of neighbours in C_m, and b_v equal to its old-P0 neighbour count. Include:

1. t_v=0 when b_v>=2; all anchors t_v+o_u<=1 when b_v>=1.
2. Every ordinary wedge t_v+o_a+o_b<=2, for distinct free neighbours a,b.
3. The full selected-degree inequality
   (d_v+b_v-1)t_v+sum_(u adjacent in C_m)o_u<=d_v at every vertex.
4. Every bottom closed-star charge at most6.
5. Every fully contained module translate (horizontal shift6i) of the
   old gh thirteen-site cut Q<=16, old h seven-site cut Q<=10,
   new gf thirteen-site cut Q<=16, and new f ten-site cut Q<=12.

These are valid necessary constraints for integer feasible configurations
with actual matching, including the two cuts proved using mate coverage.
The relaxation contains these cuts but does not impose all matching or
freezing constraints. In particular it includes no general matching-flow,
Hall or integer-disjunction description.

The matching-dependent h7 and f10 cuts remain valid for contained windows:
their equality-exclusion endpoint s has its entire grid neighbourhood
{a,l,r} inside its window, so an outside mate cannot repair the exclusion.
The gh13 and gf13 certificates use only internal wedges and unchanged
old-P0 anchors. Extra outside occupation only adds feasibility restrictions.
For c=9+6i, the older h7 window is {(4,c-1),(4,c+1)} together with
{(5,c-2),(5,c-1),(5,c),(5,c+1),(5,c+2)}. Adding
{(2,c),(2,c+2),(3,c),(3,c+1),(3,c+2),(4,c)} gives the old gh13 window.
Their established capacities are dependencies from the preceding guard note.

### 2.2 One rational point works at every chain length

Assign by row and column modulo6 as follows:

| Site phase (row,residue) | t | o |
| --- | --- | --- |
| (2,3) | 1 | 1 |
| (2,5) | 0 | 1 |
| (3,3) | 0 | 7/12 |
| (3,4) | 2/3 | 1 |
| (3,5) | 0 | 3/4 |
| (4,0) | 1/3 | 1/2 |
| (4,1) | 1/2 | 2/3 |
| (4,2) | 1/3 | 1/2 |
| (4,3) | 23/36 | 2/3 |
| (4,4) | 1/3 | 1/3 |
| (4,5) | 7/12 | 2/3 |
| (5,0) | 2/3 | 2/3 |
| (5,1) | 1/2 | 1/2 |
| (5,2) | 2/3 | 2/3 |
| (5,3) | 1/2 | 2/3 |
| (5,4) | 2/3 | 2/3 |
| (5,5) | 1/2 | 2/3 |

All17 bulk vertex types satisfy the listed inequalities by substitution.
The four window charges, independent of their module translate, are
533/36, 15/2, 59/4, 21/2 respectively, below their bounds16,10,16,12.
Every bottom-star charge is at most6.
These are finite rational substitutions into explicit inequalities, not
enumeration of grid configurations.

For completeness, restriction to C_m does not automatically preserve a
full selected-degree inequality, because its right side also decreases.
There are precisely five surviving boundary types with changed free
neighbours; check them separately:

| Boundary vertex | Surviving free neighbours | Full-degree slack |
| --- | --- | --- |
| (3,6m+5) | (2,6m+5),(3,6m+4) | 0 |
| (4,8) | (4,9),(5,8) | 0 |
| (4,6m+4) | (3,6m+4),(4,6m+3),(5,6m+4) | 0 |
| (5,7) | (5,8) | 1/3 |
| (5,6m+5) | (5,6m+4) | 1/3 |

All other constraints restrict by deleting nonnegative terms, or are fully
contained module windows with the same phase values. This proves that
the point satisfies the complete stated finite relaxation for **every** m>=2.

The sum of t+o in one full period is349/18. Relative to m periods, C_m
omits row4 residues0,1,5 and row5 residue0, once each; their total is55/12.
Consequently

    Q_frac(C_m) = 349m/18-55/12 = (698m-165)/36,
    Q_frac(C_m)-(18m-2) = (50m-93)/36 > 0   (m>=2).   (4)

Already C_2 has30 sites and fractional charge1231/36>34 by7/36.
No nonnegative linear combination of the constraints in Section2.1 can
prove (3), since that combination would hold at this rational point.
More generally the relaxation itself does not logically imply (3).

The failed statement is the **sufficiency of this local relaxation**.
The point is neither an integer occupation nor an actual matching or
completely frozen configuration. It alone does not disprove (3), the
proposed zero-extra-cost G/H/F frontier, or the half-area/grid target.
At m=2 its gap is less than1, so it alone also leaves a final integer
rounding argument possible. At m>=3 the gap exceeds1. More generally
its bulk slope349/18 is greater than18, so no fixed boundary correction
18m+B can hold throughout this real relaxation.

One elementary matching constraint already excludes this particular point.
At l=(5,9+6j), p_l=o_l-t_l=1/6. Its complete neighbourhood is inside C_m,
and the sum of neighbour endpoint weights is1/36: the upper neighbour
has p=1/36 and the two horizontal neighbours have p=0. Actual matching
coverage requires p_l<=sum_(u adjacent l)p_u, violated by5/36. Thus the
point does not establish that nonlocality is necessary, or that all
stronger local matching systems fail. Whether matching constraints suffice
for a corrected component/boundary inequality remains open.

### 2.3 A verified integer counterexample to the isolated cut

On the 6-by-22 board take k=3, m=2, G=H={0,1}, F={0}, and

    R=T0 minus {g_0,g_1,h_0,h_1,f_0}.

Set T=R union A, where

    A={(2,9),(2,15),(3,10),(3,16),(4,8),(4,11),(4,15),
       (5,7),(5,9),(5,10),(5,12),(5,14),(5,16),(5,17)}.

Starting from M0 remove these seven actual edges:

    (1,5)--(1,6), (1,7)--(2,7), (1,11)--(1,12),
    (1,13)--(2,13), (2,12)--(3,12),
    (3,7)--(3,8), (3,13)--(3,14).

Add these eleven actual edges:

    (1,5)--(2,5), (1,6)--(1,7), (1,11)--(2,11),
    (1,12)--(1,13), (2,7)--(3,7), (2,12)--(2,13),
    (2,17)--(3,17), (3,8)--(3,9), (3,12)--(4,12),
    (3,13)--(4,13), (3,14)--(4,14).

The result is a matching, all P0 remain covered, and R is retained. All
added occupied sites lie in the permitted free set. Retained selections
therefore remain feasible. In the order displayed for A, their numbers
of occupied neighbours are1,0,1,1,1,1,1,0,1,1,1,1,1,1, respectively.
This verifies feasibility directly, independently of the solver that
discovered the pattern.

In C_2 there are14 selections and exactly seven endpoints:

    (2,11),(2,17),(3,9),(3,17),(4,12),(4,13),(4,14).

Thus Q(C_2)=28+7=35>34, disproving (3) for this class. The omitted half-unit
cannot simply be discarded at this component boundary. The actual
matching joins C_2 to old P0 and, through old-endpoint rematching, has one
new pocket endpoint (2,5). Counting endpoint halves separately is valid;
rounding the C_2 contribution down is not.

The whole configuration has |T|=38, |M|=17 and objective55, below65. It
has23 frozen endpoints out of34; for example (2,5) has only its mate and
one other occupied neighbour and cannot freeze. This counterexample is
to the isolated permissions-based cut without freezing. It does not refute
that cut restricted to completely frozen configurations, or the whole-board
G/H/F frontier. It also restores h_0 as a selection: a theorem requiring
every permitted site actually deleted would be a different statement.

The full coordinates and actual freezing set are saved in
`develop/fixtures/connected_component_cut_counterexample_k3.json`.

## 3. Validation and exact formal scope

The standard-library G/F checker verifies both coefficient identities,
all7,885 f-only and108,625 gf local occupations, including the two
unmatchable charge13 patterns. It checks513 board configurations through
k=128, including116 models changing old matching edges,156 sharp frozen
permission attainers,45 sharp actual-f-deletion patches and8,302 explicit
partial strict-rank events. All513 original-tile token allocations are
injective and leave the claimed unpaid-token remainder.

The separate rational checker verifies the17 bulk types, five boundary
types and four module-window cuts exactly with Fraction arithmetic, and
checks actual free-coordinate adapters for18 chain lengths through m=128.
It checks6,053 full-degree instances,18,941 wedges and2,144 bottom stars.
The all-m proof is periodic substitution, the explicit boundary table and
the algebra (4); the length checks are controls.

It also independently checks every grid edge, matching disjointness,
selection degree, retained-site hypothesis and actual frozen set of the
integer counterexample, and replays all the listed local cuts on it.

Lean4.33.0 checks19 declarations: the two universal weighted identities,
the integer local bounds and matching equality exclusion, successor-isolate
injectivity, component sum and permission cancellation, sharp patch counts,
all integer-scaled bulk/window/boundary checks, period/omission sums and
the positive gap for every m>=2. Three additional kernel checks verify
the explicit6-by-22 example's grid feasibility/actual matching, inclusion
of its supplied R/P0 lists, and component35/whole55 charges.
No sorry, native_decide or new axioms.
The general coordinate classification, grid-to-inequality/matching adapters,
patch freezing geometry and physical-token interpretation remain written
proofs with executable controls. This is not an end-to-end formal grid theorem.
In particular the concrete R/P0 lists' identification with the original
family and the C_2 component adapter remain written/Python checks.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_successor_guard_compensation.py --output output/successor-guard-compensation-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_connected_band_local_relaxation.py --output output/connected-band-local-relaxation-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_successor_guard_compensation_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/successor-guard-compensation-formal-validation.json

The next research problem is a corrected matching-aware C_m/pocket boundary
cut under simultaneous G/H/F activation, with explicit endpoint-half charges.
One must either use complete freezing essentially, or permit the extra
component half-unit exhibited above and compensate it jointly. Arbitrary old-P0 withdrawal,
general bent/mixed footprints and a universal improvement of5/6 remain open.
These are research notes; the submitted11 October manuscript is preserved.

A subsequent [strengthening with every basic local mate-coverage inequality](CONNECTED_BAND_MATE_COVERAGE_BARRIER.md)
has a new92-scaled all-length rational point and four additional Lean checks.
It was developed after dispatch of this note's Oracle review and is outside
that review's input scope.
