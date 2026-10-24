# Connected least marked hulls can lose an unbounded amount of reserve

21 October 2026. The least-marked-hull bridge R(full)>=R(hull) is FALSE,
even when both endpoint graphs are connected, all actual positive demand is
preserved, and adjoining one negative owner forces the entire extension.
For every even k>=6 the complete nine-source family below has

    R(H_k)=k/2+13, R(J_k)=24, N=1, G=2,
    mu(H_k)=k/2+12, mu(J_k)=23.

Thus R(H_k)-R(J_k)=k/2-11 is unbounded, with only five added sources and
fixed added original negative mass17. In particular k24 is a strict
counterexample. This refutes that comparison rule, not the unrestricted
allocation mu=N+R-G>=0 or rectangular-grid triple equality; both remain OPEN.

The nine-source construction and insertion proof were proposed by Oracle
task592801f9. We independently reconstructed the original matching, support,
occupied feasibility, actual marked hull, tile census and signed events.
The proof below supplies the parameter argument; seven finite controls are
checks on that proof, not an inference from a search. No Lean verification
of the nine-source family or independent review verdict for this note is claimed.

## 1. Complete sources in a fixed physical partition

Tiles are {2i,2i+1} x {2j,2j+1}. The canonical source U(w,L,H) has matching

    (0,c)--(0,c+1), odd1<=c<w;
    (1,c)--(1,c+1), even2<=c<w-1;
    (r,1)--(r+1,1), odd1<=r<L;
    (r,w)--(r+1,w), odd1<=r<H.

Its original supports are (0,0),(0,w+1),(L+1,1),(H+1,w), together with
(r,0) for even2<=r<=L, (r,2) for odd3<=r<=L, and their right-leg analogues
(r,w+1) for even r and (r,w-1) for odd r up to H. All original endpoints
and matching edges are retained. After fusion only supports consumed by
endpoints disappear from the selected set; all other supports are mandatory.

| Owner | Source | Physical map of (r,c) |
|---|---|---|
| V1 | U(8,k+4,k+2) | (r-k-2,c) |
| V2 | U(6,6,4) | (c+1,8-r) |
| V3 | U(k+8,8,4) | (2-c,10-r) |
| V4 | U(6,k,k) | (-r,c+1) |
| V5 | U(6,k+6,4) | (-r,c+10) |
| V6 | U(8,4,4) | (-k-7-r,c+3) |
| V7 | U(6,4,8) | (c-k-12,r-3) |
| V8 | U(6,4,6) | (-c-k-6,3-r) |
| V9 | U(6,4,4) | (-c-k-11,8-r) |

Put H_k={V1,V2,V3,V4} and J_k={V1,...,V9}. Only V1 is positive; its phase
is00. V2,V3,V4 have phase11, and V5,...,V9 have phases10,01,10,01,10.
The old negative mass is k+17; added negative masses are5,1,5,1,5.
H_k is F(k,8) from the source-retention note translated by(0,1). This is
an isometry of the feasibility problem, but phases and reserves here are
recomputed in the unchanged physical tile partition.

## 2. Actual marks force exactly the old hull

The potential foreign marked-trigger points of V1 are

    (-k,2),(-k+2,2),(-k,3), (-k,7),(-k+2,7),(-k,6).

The four in columns2,7 belong to V4; the other two are blank. None belongs
to an added owner. Both actual marked sides therefore have the UNIQUE
witness owner V4, irrespective of which trigger is selected. All actual
positive/mark seed choices have owner set{V1,V4}; N=n2=1,n0=0,G=2.

The original V1 support t=(1,2) has anchor(1,1) and the additional retained
V4 neighbor(0,2). Its actual consumer is V3, forcing V3. Next the original
V3 support u=(2,2) has anchor(1,2) and the retained V1 neighbor(2,1);
its actual consumer is V2. Hence every legal retained family containing
the seed contains all four old owners. H_k itself is feasible, so the
[exact retention theorem](SOURCE_RETENTION_HORN_CLOSURE.md) proves

    cl_J({V1,V4})=H_k.

The positive terminal(2,1) retains both supports(2,0),(3,1). The terminal
(0,8) loses both(0,9),(1,8) to V3. Thus A=1 in both families.

## 3. Complete extension feasibility at every length

Substitution in the constructors gives the following new endpoint sets;
all intervals contain integer coordinates:

    P5={-1,0}x[11,16] union[-k-6,-2]x{11} union[-4,-2]x{16};
    P6={-k-8,-k-7}x[4,11] union[-k-11,-k-9]x{4,11};
    P7=[-k-11,-k-6]x{-3,-2} union{-k-11}x[-1,1]
       union{-k-6}x[-1,5];
    P8=[-k-12,-k-7]x{2,3} union{-k-7}x[-1,1]
       union{-k-12}x[-3,1];
    P9=[-k-17,-k-12]x{7,8} union{-k-12,-k-17}x[4,6].

The old chamber ends at column10. P5 lies beyond it; P6,P8,P9 lie above
it. The sole row where P7 reaches the old chamber is-k-6, where P7 ends
at column5 and the old endpoints start at6. The displayed intervals also
separate all new owners from each other. All unchanged original matchings
are consequently disjoint and cover every endpoint.

Exactly four previously selected old supports are consumed:

    (-k-7,6),(-k-7,8),(-k-7,10) by V6; (-k-6,5) by V7.

The complete new retained-support certificate is below. For V6--V9 use
normalized coordinates(rho,c)=(physical row+k,column); V5 uses physical
coordinates. Each right entry is the only occupied neighbor of its left entry.

| Owner | Retained supports | Unique occupied neighbors |
|---|---|---|
| V5 | (r,12), odd-k-5<=r<=-3 | (r,11) |
| V5 | (0,17),(-2,17),(-4,17),(-3,15),(-5,16) | (0,16),(-2,16),(-4,16),(-3,16),(-4,16) |
| V6 | (-12,11),(-11,12),(-10,5),(-10,10),(-9,12),(-7,12) | (-11,11),(-11,11),(-10,4),(-10,11),(-9,11),(-7,11) |
| V7 | (-10,0) | (-11,0) |
| V7 | (-5,c), c=-3,-1,1,3,5 | (-6,c) |
| V8 | (-13,c), c=-3,-1,1,3 | (-12,c) |
| V8 | (-12,-4),(-8,0) | (-12,-3),(-7,0) |
| V9 | (-18,c), c=4,6,8 | (-17,c) |
| V9 | (-17,3),(-16,5),(-13,5) | (-17,4),(-17,5),(-12,5) |
| V9 | (-11,c), c=6,8 | (-12,c) |

The coordinate intervals exclude any other endpoint neighbor and any
selected-selected edge. They also exclude new neighbors of every old
selection except the four consumed points. Thus every final selection has
exactly one occupied neighbor. Original occupied vertices persist under
consumption, so every original endpoint retains occupied degree at least
three. This proves complete feasibility in P union T, not just in P.

There is a useful direct induction behind the parameter calculation.
To pass from k to k+2, shift points of row<=-6 upward by2 and fix rows>=-5.
The inserted rows-7,-6 contain the following complete original points:

| Owner | Endpoints in each inserted row | Supports in row-7 | Supports in row-6 |
|---|---|---|---|
| V1 | columns1,8 | 2,7 | 0,9 |
| V3 | columns9,10 | none | none |
| V4 | columns2,7 | 3,6 | 1,8 |
| V5 | column11 | 12 | 10 |

Other owners translate or stay fixed. This follows from their explicit
intervals, with k>=6 keeping the height-four V5 leg below the cut. After
consumption both rows have endpoints1,2,7,8,9,10,11; row-7 has selections
3,6,12 and row-6 has selection0. All have their unique horizontal anchor.
The boundary rows reproduce the same alternating vertical pattern, so no
new cross-boundary support conflict appears. For J the insertion adds
three regular2P1T tiles and two full tiles, with no new defect. For H omit
V5: the extra tile at column origin10 is an original irregular V3 pair.
It adds two defect units, or one reserve unit. This proves the unbounded
parameter recurrence directly from the constructors.

## 4. Connectivity and dependencies of the added sources

H_k is connected by the inherited four-source contacts. New contacts are

    V3--V5: (r,10)--(r,11);
    V5--V6: (-k-6,11)--(-k-7,11);
    V3--V7: (-k-6,6)--(-k-6,5);
    V7--V8: (-k-7,-2)--(-k-7,-1);
    V8--V9: (-k-12,3)--(-k-12,4).

Thus J_k is connected too. Moreover cl_J(H_k union{V5})=J_k. The forcing
chain has antecedents, original support and forced consumer as follows:

| Retained antecedents | Support that cannot be restored | Consumer |
|---|---|---|
| V3,V5 | (-k-7,10) | V6 |
| V3,V6 | (-k-6,5) | V7 |
| V6,V7 | (-k-7,3) | V8 |
| V6,V8 | (-k-12,4) | V9 |

The first support is anchored at(-k-6,10) and sees V5's original support
(-k-7,11), which remains occupied even if consumed. The other extra
neighbors are endpoints(-k-7,5) of V6,(-k-6,3) of V7, and(-k-12,3) of V8.
These are actual Horn implications, not a recomputation of source ownership.

The five added owners alone are NOT feasible. Their restored supports
(-k-6,6) and(-k-6,10) each have two endpoint neighbors among V5,V6,V7.
Their original endpoint consumer belongs to the old V3. Consequently this
loss is not removable as an independently feasible negative component.

## 5. Exact reserve and nonrepeated signed loss

H has A=1,U0=5,Z0=0 and k/2+10 irregular pair defects, with no other
defects. J has L1=5,L2bar=17,L2mutual=0,L3=3. Its mixed triple origins
are(0,10),(-k-12,4),(-k-8,-2); five other triples are unchanged U11 caps.
The actual full tile census of J is

| Physical profile | Count |
|---|---|
| 4P0T | k+20 |
| 2P1T | 3k/2+17 |
| 2P0T | 17 |
| 3P0T | 8 |
| 1P1T | 5 |
| 1P2T | 1 |

These counts follow by splitting the explicit endpoint intervals into even
tiles. Equivalently the k6 base census is the displayed fixed catalogue
and the insertion above adds only the indicated two full/three regular
pair tiles. This gives a finite base with a general constructor induction,
not finite enumeration in place of a general proof. The unchanged activation
and five U caps give

    2R(H)=1+5+(k+20)=k+26;
    2R(J)=1+5+(5+2*17+3)=48.

The same loss can be counted without mixing ledgers. In the established
[signed-extension identity](CLOSED_EXTENSION_SIGNED_RESERVE_AND_LATTICE_OBSTRUCTION.md),
actual fresh directed occurrences have the following targets and producers:

* Old-to-new: V3 toward(r,11), every-k-6<=r<=0, giving k+7 events.
* New-to-old: V5 toward(r,10), odd-k-5<=r<=-1, giving k/2+3 events.
* New-to-new: V7 toward(-k-12,-2),(-k-12,0),(-k-7,-1), and V8 toward
  (-k-11,-1),(-k-11,1),(-k-11,-3), giving six events.

There are k/2+3 new full tiles at(r,10), even-k-6<=r<=-2, and two at
(-k-12,-2),(-k-12,0). No previously full mixed tile disappears. The three
event classes are disjoint by their original producers and actual endpoint
consumers. Each full tile is included exactly once. Therefore

    Delta R=17+2*(k/2+5)-(k+7)-(k/2+3)-6=11-k/2.

Each tile of the long old-irregular/new-regular interface has three fresh
events and two full-tile credits. The repeated one-unit signed loss is the
mechanism missed by monotone-hull comparisons. Original full tiles, geometric
defects and source masses are not separate pools that can be added again.

There is also a direct consequence for negative-source separator pruning.
V3 is an actual articulation: no endpoint edge joins{V1,V2,V4} to the five
new owners. Its original negative mass is S3=k+7. The complete connected
branch K={V3,V5,...,V9} has NO positive source or marked side. Applying the
[legal separator identity](SOURCE_SEPARATOR_SIGNED_TRANSFER.md) gives

    R(K)=R(J)-R(H)+S3=k/2+18.

For every even k>=24 this is strictly LESS than S3. Thus a positive-free
branch need not cover its shared separator's negative mass. At k70 it has
reserve53 versus shared mass77. This refutes a universal sufficient pruning
rule R(branch)>=S_s as well as the marked-hull comparison. It does not refute
the exact margin-dependent deletion criterion or allocation; deleting that
branch in this positive-margin example simply raises the margin from23 to47.

## 6. Margins, concrete witness and verification scope

At k70 the genuine connected marked hull has R48 and mu47. The connected
extension has R24 and mu23. Its endpoint/matching/selected counts are
668,334,184. Both retain the same sole doubly marked positive source.
In general |P(J)|=7k+178, |M(J)|=7k/2+89, |T(J)|=2k+44. The aligned
containment[-k-18,9]x[-4,17] has dimensions(k+28)x22 and actual slack
11k/2+175>0. No separate hull bounding-rectangle slack is spent here.

Run `python3 develop/check_connected_marked_hull_obstruction.py` for seven
complete controls k6,8,12,24,40,70,100. This independently rebuilds source
matching/support formulas and checks endpoint uniqueness, complete feasibility,
both connectivities, unique witness owners, exact closure, defect/event
agreement, direct event classes and the explicit two-row insertion.

An independent earlier construction has18 sources, N5,G6,n0=2,n2=3, and
connected full endpoints. At k=h20 its least marked hull has R58 versus
full R50, with mu57 versus49. Its hull has FOUR endpoint components, so
that example alone did not settle the connected-hull variant. The present
nine-source construction does. The18-source checker retains its explicit
manifest and12 parameter controls. Its six-source core is the separate
scope of `formal/SubQuorum/DemandHullReserveObstruction.lean`; that source
does not formalize either full family or either parameter theorem.

The viable remaining target is to control signed loss by the EXISTING
allocation margin of the hull, with actual capacities used once, or find
a complete physical violation. Almost all of an arbitrarily large hull
margin can disappear here, but23 remains. The universal allocation,
rectangular-grid equality and improvement of the universal5/6 bound are
not established by this obstruction.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
