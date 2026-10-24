# All north-terminal U consumers of the persistent pair

21 October 2026. This completes the LOCAL north-terminal U branch for every
legal breadth and both leg lengths, including all far-column escapes. It
does not classify the other endpoint roles at the pair or arbitrary exterior
contributions, and gives no new global5/6 bound or grid-equality theorem.

## Hypotheses and the exhaustive left-terminal classification

Keep the original-source model, fixed tile phase and either residual inventory
A=Q,D,L,C,E,W,T0,V of the earlier notes. Let a be odd, w>=12 even, and

    V=U(k,8,z), (r,c) -> (a-6+r,w+12-c),

where k=w+8,z even4..14, or k=w+10,z even>=16. Write B=w+12-k, the even
left bar column of V: B=4 or2. The near terminal column of V is w+11.
The common baseline is Phi(A)-Phi(Q,D,W)=-1.

Consider ANY left-pointing north-terminal U source consuming
t=(a+1,w+14):

    K=U(s,ell,m), (r,c) -> (a+1-ell+r,w+15-c),

with arbitrary even s>=6 and ell,m>=4. It also consumes e=(a,w+14).
Its far column is g=w+15-s, an odd integer at most w+9.

**Theorem1.** The following table is an exact endpoint-disjointness
classification for K against A. A row's condition is both necessary and
sufficient. Every disjoint K has original charge+1.

| Far-column regime | Exact disjointness condition | DeltaPhi(K\|A) |
|---|---|---|
| g>=B, equivalently s<=k+2 | ell>=12 and m<=ell-8 | 1-[m=ell-8] |
| g=3,B=4 | ell>=10 and m<=ell+8 | 1-[m=ell+8] |
| g<=1 | ell>=10, arbitrary legal m | 1 |

These rows exhaust every legal width. In particular the formerly unclassified
short far legs and arbitrarily wide escapes all have gain1, except for the
two displayed zero-contact boundaries. There is no negative insertion in this
entire left-north-terminal class.

## Proof of disjointness

For ell=4,6,8, the lower bar endpoint(a+2-ell,w+11) of K belongs to V:
its V intrinsic row is8-ell, either a bar row or near-stem row. The point
is K's intrinsic(1,4), present since s>=6. Thus ell>=10 is necessary.
For ell>=10, K's bar is entirely above V and every other A endpoint.
K's near column w+14 ends at row a+1, just before C's far stem starts
at a+2. It therefore misses all old endpoints. Only the far column remains.

If g>=B, it lies inside V's upper bar. K's far stem reaches the old endpoint
(a-6,g) exactly when m>=ell-7. Avoiding it is m<=ell-8, which also gives
ell>=12 as m>=4. This bound ends K's far stem at most a-7, above every
other A endpoint in that column. It is therefore sufficient as well.

If g=3 and B=4, the far column misses V, T0, D,L,C,E,W. Its first old
endpoint is Q's near tip(a+10,3). K reaches that point exactly when
m>=ell+9, so disjointness is exactly m<=ell+8. This includes far stems
that go below the V bar because their column has escaped it.

Finally g<=1 misses every old endpoint column. There is no upper bound
on m, and ell>=10 is sufficient. Since g is odd and B is2 or4, the three
cases are exhaustive without a width or height cutoff.

## Original charge and exact contact sets

Put H=(ell+m)/2. The bar starts at even row and odd far column and ends
at even near column. It occupies s/2+1 tiles; its two stems add H. The
matching has s+H-1 edges. Exactly H+4 original supports lie in endpoint
tiles: the two bar-corner supports, both terminal axial supports and all H
even-indexed lateral supports. Odd-indexed lateral supports lie outside.
Thus q(K)=(s+H-1)+(H+4)-2(s/2+H+1)=1.

All disjoint K share the harmless C terminal tile(a+1,w+14). Each of its
two possible directions targets an ORIGINAL axial support, so it contributes
DeltaF=DeltaEv=0. No old tile meets the K bar. The only additional shared
tile can occur at one of the two far-terminal boundaries:

| Boundary | Shared tile lower corner | Sole new directed event |
|---|---|---|
| g>=B,m=ell-8 | (a-7,g-1) | V:(a-6,g)->K:(a-7,g) |
| g=3,B=4,m=ell+8 | (a+9,2) | Q:(a+10,3)->K:(a+9,3) |

Both have DeltaF=0. The reverse event targets K's original far axial
support and is excluded. In the first case V has no original support north
of its bar, so V-to-K survives. In the second case Q's original terminal
axial support is west of its tip and its terminal lateral support is south,
so Q-to-K survives. Shorter
far stems have no such shared tile. The old endpoint tiles all have columns
at least2, so g<=1 creates no far-column shared tile, however long the stem.

Consequently DeltaN=1,DeltaS=DeltaF=0 and DeltaEv is the single boundary
indicator. This proves Theorem1 as an exact set identity.

## Both zero boundaries force a repairing consumer

**Theorem2.** Suppose K is on either zero boundary in Theorem1 and a complete
feasible U/rotor family retains A+K. The actual original consumer of the
missing V support p=(a+2,w+12) must be

    J=U(h,d,f), (r,c) -> (a+2-d+r,w+13-c),

and its exact endpoint-disjointness criterion against A+K is

    6<=h<=s-4, 14<=d<=ell-2, 4<=f<=d-10.           (1)

Its contribution into the prescribed SAME inventory is DeltaPhi=h-2>=4.
Hence the joint package is at least3 above Q/D/W. In particular zero cases
with s=6,8 or ell=10,12,14 cannot have any complete feasible extension.

The support p has V west and E east and south. Thus every original consumer
must have its own matching partner north. The two rotor terminal forms hit
E; every right U collides with K's near stem or bar. A left U with d>=ell
hits K's bar; with d<=8 it hits V. In either zero regime m>=ell-8, so for
10<=d<ell a left bar spanning K's far column hits its far stem. Avoidance
therefore requires h<=s-4, exactly as in the earlier tight-cap proof.

On both zero boundaries s<=w+12 and hence J's far column c=w+13-h is at
least5. It lies inside V's bar in both residual families. Reaching(a-6,c)
would collide with V, forcing f<=d-10, and thus d>=14. These are all the
necessity conditions in(1). Conversely, under(1), J's bar lies below K's
bar, both J columns lie strictly between K's two stems, and its far stem
ends above V. The near-column separation from all old endpoints is unchanged.
This proves sufficiency, even for the long far leg m=ell+8 of the Q-tip case.

The exact original charge and E/J shared tiles are the same as in
[the tight-cap compensation proof](SECONDARY_TEN_TIGHT_CAP_COMPENSATION.md):
q(J)=1-h, with two shared tiles(a-1,w+12),(a+1,w+12) contributing respectively
(F,Ev)=(0,1),(1,2). No K tile is shared: its bar tile row is separated from
J's, and both stem tile columns are outside J. Thus DeltaS=h-1,DeltaN=0,
DeltaF=1,DeltaEv=3, giving h-2. K's already counted V-to-K or Q-to-K debit
stays in the old inventory and is not charged or credited again.

## Combined local north-terminal result and remaining scope

If the actual consumer at t is a right-pointing north-terminal U, the
[persistent-pair theorem](SECONDARY_TEN_PERSISTENT_PAIR_COMPENSATION.md)
already gives exact gain1 in every legal dimension. Theorem1 and Theorem2
complete the left-pointing case: it either supplies1 immediately or forces
a distinct original consumer at p supplying at least4 in the same joint
inventory. The explicit rotor from the previous note also supplies1.

This is a local compensation result conditional on the ACTUAL original
consumer being in the stated class. East-terminal and corner roles at t,
consumers that do not jointly consume e, other prescribed residual prefixes,
and arbitrary signed exterior contributions are not classified here. Neither
the local joint package nor its feasibility as a standalone subfamily is
assumed. A complete-family global inequality still requires its own proof.

Finite controls reconstruct the exact disjointness conditions and contact
sets, including both zero boundaries and arbitrarily long sampled far legs.
They corroborate the general role/interval/counting proof above. The initial
tight-cap review predated this extension; the subsequent separate review
accepted this all-width/far-leg theorem, as recorded below. Lean geometry
and execution receipts specify their actual scope.

## Review and extension

The unbounded mathematical arguments received ACCEPT in the independent
[written-proof review](../output/secondary-ten-all-north-review.json).
The [joint-consumer lemma](SECONDARY_TEN_JOINT_PAIR_COMPENSATION.md) adds
outer-corner and rotor roles. Distinct consumers, global budget nonreuse
and signed exterior estimates remain open.
