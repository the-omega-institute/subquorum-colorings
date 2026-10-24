# Exact continuation and compensation inside an arbitrary tight cap

21 October 2026. This extends the narrow-cap noncompletion theorem to an
arbitrary internal tight cap. The contribution is an exact local dichotomy,
not a global allocation or grid-equality theorem.

## The general tight-cap family

Retain the same original-source model and residual inventory A of
[the narrow-cap note](SECONDARY_TEN_NARROW_CAP_NONCOMPLETION.md). Let
w>=12, 6<=s<=w+10 and ell>=12 all be even. Define

    K_s=U(s,ell,ell-8), (r,c) -> (a+1-ell+r,w+15-c).

Every such K_s is endpoint-disjoint from A, has original charge+1 and exact
DeltaPhi(K_s|A)=0. Its far column g=w+15-s is odd and at least5; its far
terminal is at row a-7, immediately above V's upper bar. The same exact
charge and two-tile inventory in the narrow-cap note applies for EVERY
allowed s, not just6,8. The upper bound on s keeps this far column within
the old V bar interval; no wider escape is classified here.

The missing V support p=(a+2,w+12) still has V west and E east and south.
In a complete feasible extension its actual consumer is north-terminal.
Both north rotors are blocked by E. Every right-pointing U is blocked by
K_s, by the two right/long collision witnesses of the narrow-cap theorem,
which do not use s<=8. Thus only

    J=U(h,d,f), (r,c) -> (a+2-d+r,w+13-c)

can survive, where h>=6,d>=4,f>=4 are even.

**Theorem.** J is endpoint-disjoint from A+K_s if and only if

    6<=h<=s-4,   14<=d<=ell-2,   4<=f<=d-10.       (1)

For every such J, the exact insertion contribution into the SAME prescribed
inventory A+K_s is

    q(J)=1-h,   DeltaS=h-1,   DeltaN=0,
    DeltaF=1,  DeltaEv=3,    DeltaPhi=h-2>=4.       (2)

Consequently a complete feasible family retaining A+K_s can exist only when
s>=10 and ell>=16. Its actual consumer at p is one of the U sources in(1),
and its prescribed joint subinventory A+K_s+J has

    Phi(A+K_s+J)-Phi(Q,D,W)=h-3>=3.               (3)

This excludes all s=6,8 and all ell=12,14 in this class, and gives an exact
conditional repair for every remaining internal tight cap. It does not assert
that the subinventory is complete or that arbitrary other originals have
nonnegative exterior contribution.

## Necessity: the bar must fit inside the cavity

If d>=ell, J's near leg hits K_s's bar at(a+2-ell,w+12).
If d<=8, J's bar hits V at(a+3-d,w+11). Thus 10<=d<=ell-2.
If h>=s-2, J's bottom bar row contains(a+3-d,g): in J this is intrinsic
(1,s-2), and in K_s it lies on the far stem at intrinsic row ell+2-d.
Since d>=10 and d<ell, that row is between2 and ell-8. Therefore avoiding
K_s forces h<s-2, hence h<=s-4 by evenness.

J's far column is c=w+13-h. Since h<=s-4<=w+6, we have c>=7, so c lies
inside V's upper-bar interval in both residual families. If f>=d-8, J's
far stem reaches(a-6,c), an old V endpoint: its intrinsic row is d-8>=2.
Avoiding that point forces f<d-8, hence f<=d-10 by evenness. As f>=4,
this also forces d>=14. These are exactly the inequalities in(1).

## Sufficiency: all retained endpoint intervals are separated

Assume(1). J's near column is w+12; it misses V and T0, whose maximal
columns are w+11 and w+10, and ends at row a+2 above E's bar starting at
a+3. The other six-source endpoints in that column lie no higher than
E's bar. K_s's near column is w+14, two columns to the right.

J's far column satisfies c>=g+2, so the far stem and bar lie strictly to
the right of K_s's far column. J's top row is a+2-d>=a+4-ell, below
K_s's last bar row a+2-ell. The two K_s stems are consequently outside
the entire J endpoint region. This proves separation from K_s.

The J far stem ends at row a+2-d+f<=a-8, above V's first bar row a-6.
J's own bar ends at row a+3-d<=a-11. Every old A endpoint outside the
near-column contact region is below those rows; V's far column is4 or2,
also strictly left of J. No retained old endpoint can coincide with J.
This proves the converse for arbitrary legal dimensions, including arbitrarily
long ell,z and far stems satisfying(1).

## Exact source and shared-tile counts

Let H=(d+f)/2. J's bar begins at odd row and odd far column and ends at
even near column; both bar rows and both bar ends cross tile boundaries.
The original matching has h+H-1 edges. J occupies h+H endpoint tiles
and has H+2 original supports inside them: the two bar-corner supports
and all H even-indexed lateral supports. Both terminal axial supports
and all odd-indexed lateral supports lie outside its endpoint tiles.
Hence q(J)=1-h.

There are exactly two shared endpoint tiles with A+K_s:

| Lower corner | Newly full | New directed events |
|---|---:|---:|
| (a-1,w+12) | 0 | 1 |
| (a+1,w+12) | 1 | 2 |

Their old endpoints belong only to E. At the upper tile J has two
near-column endpoints and E has its far terminal(a,w+13); J-to-E is
excluded by J's original lateral support, while E-to-J survives. At the
lower tile two near-column endpoints of J and two E endpoints fill the
tile. Four horizontal directions are possible; exactly one in each
direction is excluded by an original lateral support, leaving two.

No V, T0 or K_s endpoint tile is shared: J's far terminal is at most
a-8, whose tile row ends above V's first tile row a-7; its bar is lower
than K_s's bar by at least one tile row, and its
far and near tile columns are separated from the K_s stems. All earlier
originals other than E are outside the near-column tile region. Thus the
table includes every shared endpoint tile, with the old support exclusions
retained even when their sites are consumed.

The unique upper event is E:(a,w+13)->J:(a,w+12). The lower events are
J:(a+1,w+12)->E:(a+1,w+13) and
E:(a+2,w+13)->J:(a+2,w+12).
Summing gives DeltaPhi=(h-1)+2-3=h-2. This proves(2) and(3).

## Scope and validation

The prescribed source/tile/event inventory is used once. Neither p nor K_s's
other consumed supports supply another credit. The positive K_s original is
counted once; its single contact debit remains in the old inventory when J
is inserted. The final lower full tile and its directed events are counted
once as the J increment.

The general proof is the endpoint-role classification, interval argument and
exact two-tile partition above. Finite controls independently reconstruct
the sources and both directions of(1). The narrow-cap Oracle request was
submitted BEFORE this wider theorem was written, and failed terminally at
the infrastructure input stage without a mathematical response. A new
self-contained review includes this entire supplement. Its status is recorded
separately; no verdict is presumed. The local Lean file verifies both necessary
inequalities and sufficient endpoint disjointness in arbitrary dimensions,
in addition to the narrow collision facts. It does not formalize source-cardinality
or directed-event counts, the catalogue role argument or the global source model.

## Subsequent generalization

The [all-north-terminal classification](SECONDARY_TEN_ALL_NORTH_TERMINAL_PAIR_CONSUMERS.md)
removes the internal-width and tight-far-leg restrictions. The
[joint-consumer lemma](SECONDARY_TEN_JOINT_PAIR_COMPENSATION.md) includes
all actual joint U/rotor roles at the persistent pair. These are local
subinventory conclusions; signed exterior control is still required.
