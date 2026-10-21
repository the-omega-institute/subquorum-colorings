# Compensation for every actual consumer of the prescribed residual pair

21 October 2026. This removes the common-consumer hypothesis from the
[joint-consumer lemma](SECONDARY_TEN_JOINT_PAIR_COMPENSATION.md). The result
is an actual-original subinventory theorem for the two prescribed residual
families. Global package nonreuse and arbitrary signed exterior control are
still required for a global allocation theorem.

## Model and statement

Use the fixed tile phase, full original matching/support data, complete
feasible U/rotor model and eight-original residual A of the
[all-north-terminal note](SECONDARY_TEN_ALL_NORTH_TERMINAL_PAIR_CONSUMERS.md).
Thus a is odd,w>=12 even, A=Q,D,L,C,E,W,T0,V and
V=U(w+8,8,z),z even4..14, or V=U(w+10,8,z),z even>=16,
at(r,c)->(a-6+r,w+12-c). Set B=w+12-k in {4,2}.
Write N for the number of positive ORIGINAL owners, S for the sum of
negative original charge magnitudes, F for mixed full endpoint tiles and
Ev for intratile directed foreign contacts excluding ORIGINAL supports.
The functional is Phi=N+S+2F-Ev. The established baseline is

    Phi(A)=Phi(Q,D,W)-1.

**Theorem.** For every complete feasible original family G retaining A,
there is an actual-original subinventory I with

    A subset I subset G,  |I minus A|<=2,
    Phi(I)>=Phi(Q,D,W).

There is no assumption that the persistent supports e=(a,w+14) and
t=(a+1,w+14) have the same actual original consumer. On the distinct-owner
branch one can in fact choose I with Phi(I)>=Phi(Q,D,W)+3, by the
[subsequent depth-eight exclusion](SECONDARY_TEN_DEPTH_EIGHT_COMPLETE_EXCLUSION.md).
The original proof below establishes the weaker excess1 directly; the
addendum rules out its exceptional depth-eight prefix in every complete family.
The conclusion does not assert completeness of I or monotonicity of Phi
under further insertions.

## Distinct owners force an east terminal at t

Completeness forces e,t to be endpoints of actual originals, as in the
full mandatory-support closure proof. Suppose they have distinct owners
and let J be the actual owner of t. North belongs to the owner of e,
west is E:(a+1,w+13), and south is C:(a+2,w+14).
Only east can be an own endpoint neighbor of J at t.

Every original has a matching partner at each endpoint, so this own
neighbor set is exactly {east}. Only a leg terminal of U or a tip of a
rotor has one own neighbor. Full-source leg reflection preserves the
matching and support sets, as proved in the accepted joint-consumer audit.
The exhaustive U frames, with legal even h>=6,ell,f>=4, are

    J_N=U(h,ell,f), (r,c)->(a+2-c,w+14+ell-r),
    J_S=U(h,ell,f), (r,c)->(a+c,w+14+ell-r).

Both contain t and omit e. The two full rotor originals are

    R_N(r,c)=(a-2+r,w+13+c),
    R_S(r,c)=(a+4-r,w+13+c),

applied to the standard rotor. Quarter-turn invariance of its endpoints,
supports and matching makes this a full-original classification.

## Every surviving east-terminal U gives immediate compensation

The exact endpoint-disjointness criteria and increments against A are:

| Frame | Breadth | Necessary and sufficient far-leg bound | DeltaPhi |
|---|---|---|---:|
| J_N | h=6 or8 | f<=ell+2 | h-1 |
| J_N | h>=10 | Any legal f | h-1 |
| J_S | h=6 | f<=ell-2 | h-2 |
| J_S | h=8 or10 | f<=w+ell+2 | h-2 |
| J_S | h>=12, B=2,z>=h+6 | f<=w+ell+10 | h-2 |
| J_S | h>=12, otherwise | Any legal f | h-2 |

Here and below the criteria concern endpoint disjointness, not existence
of a complete extension. For J_N the bar and near stem are to the right
of old endpoints. Its far row is a+2-h. For h=6,8 its first old endpoint
when moving west is V in column w+11. The terminal column is
w+14+ell-f, which is even; avoiding that point is exactly f<=ell+2.
For h>=10 the far row and its endpoint tiles precede every old endpoint.

For J_S the far row is a+h. At h=6 the first old endpoint is C in
column w+14, so the even far terminal column must be at least w+16,
equivalently f<=ell-2. At h=8,10 the first old endpoint is Q in
column11, so the far terminal must be at least12, equivalently
f<=w+ell+2. For h>=12 only V's arbitrarily long far stem in the
second residual can reach this row. It does so exactly when z>=h+6,
at column2. The even far terminal must then be at least4, giving
f<=w+ell+10. Otherwise the far row and tiles follow all old endpoints.
The bar lies at columns w+13+ell,w+14+ell, at least w+17; the near
stem lies in row a+1 and starts at column w+14. These give sufficiency
and show there are no other endpoint obstructions.

Put H=(ell+f)/2. In both frames the matching count is h+H-1.
For J_N its bar occupies h+2 endpoint tiles and the stems add H-2;
exactly H+2 original supports lie in these tiles. For J_S the bar
occupies h endpoint tiles and the stems add H-2; exactly H-2 original
supports lie in them. In each frame these counts give q=1-h.
For J_N the counted supports are its two bar-corner supports and H
even-indexed outward supports. For J_S they are the H-2 odd-indexed
inward supports. Terminal axial supports are outside endpoint tiles.

The common tile at t and C:(a+2,w+14) has three endpoints. For J_N
each directed contact targets its source's original support, giving zero.
For J_S only J_S:t->C:(a+2,w+14) survives, giving one event.
There are no other contacts except a possible J_S,W overlap when h=8.

In that case the new far row a+8 meets W's last row a+7, whose
endpoints are precisely columns w+1 through w+5. The new row is a
contiguous interval with even left end. Its bar is farther right and
cannot meet W. The complete shared tiles are exactly the reached pairs
{w+2,w+3} and {w+4,w+5}; each has one new full tile and two surviving
events. If the new interval reaches w or earlier, the additional tile
{w,w+1} has three endpoints and no surviving event: both directions
at w+1 target the corresponding ORIGINAL support. These exhaust the
overlap and give net 2DeltaF-DeltaEv=0. Old Q tiles lie to the left of
the disjointness bound. Thus the displayed increments are exact.
Every east-terminal U therefore gives at least4, repairing the deficit
with at least3 to spare in I=A+J.

## Two rotor obstructions at the upper support

The following exclusions hold in every complete family retaining A,
independently of which original consumes t. The two north-terminal
rotors at e, expressed using the standard rotor, are

    Z_-(r,c)=(a-4+r,w+11+c),
    Z_+(r,c)=(a-4+r,w+17-c).

Neither can be an actual retained original in such a complete family.

For Z_-, let p0=(a,w+12). It is V's original support(6,0).
Its west and east neighbors are V:(a,w+11), E:(a,w+13), and
Z_- adds its north neighbor(a-1,w+12). All three remain foreign
endpoints. Completeness forces p0 to be an endpoint with own neighbor
south. Every south-terminal U contains p0+(3,0), since its incident
leg has length at least4; that site is E:(a+3,w+12). The two
south-terminal rotors contain respectively E:(a+2,w+13) and
E:(a+1,w+13). All possible actual consumers collide with E.
Additional originals cannot remove these retained collisions.

For Z_+, let q0=(a-1,w+13), E's original far axial support.
Its north and east neighbors are Z_+ endpoints(a-2,w+13),
(a-1,w+14), and its south neighbor is E:(a,w+13).
An actual consumer must have its own neighbor west. Every west-terminal
U and both west-terminal rotors contain q0+(0,-2)=(a-1,w+11),
which is a retained near-stem endpoint of V. Again no actual consumer
exists. Both are complete-family exclusions, not finite-search evidence.

## Rotor at t forces a positive-gain U at e

Direct original-support accounting gives

    q(R_N)=q(R_S)=0,
    DeltaPhi(R_N|A)=0,  DeltaPhi(R_S|A)=-1.

R_N shares only the three-endpoint C tile with no surviving event.
R_S completes that C tile with two directed events and also shares the
next C tile T(a+3,w+14), which is not full and has one directed event.
The total is one new full tile and three directed events.
The zero original charges contribute to neither N nor S.

Let K be the actual owner of e. Its own neighbors can only be north
or east, since west is E and south belongs to the rotor at t.
R_N occupies the site one step east of e. R_S occupies the site two
steps east of e. Every allowed U terminal or outer corner with an own
east neighbor also contains that second east site; a rotor east tip
does as well. Hence neither east terminals nor north/east corners can
occur, and K must have only its own north neighbor.

The two north-terminal rotors were just excluded in every complete
extension of A. Thus K is an actual north-terminal U. Its normalized
right and left frames are

    K_R=U(h,d,f), (r,c)->(a-d+r,w+13+c),
    K_L=U(h,d,f), (r,c)->(a-d+r,w+15-c).

K_R is endpoint-disjoint from A and either rotor for every legal dimension.
For K_L put g=w+15-h. Its exact disjointness criterion is

| Far-column regime | Exact condition |
|---|---|
| g>=B | d>=12,f<=d-8 |
| g=3,B=4 | d>=8,f<=d+8 |
| g<=1 | d>=8, any legal f |

Depth4 or6 hits V's near stem/bar. At depth8 its bar misses V's
endpoints but the far stem must escape the V bar. In the internal regime
its first possible far-column collision is V at row a-6, forcing f<=d-8.
At the first-residual column3 the obstruction is Q at row a+10,
forcing f<=d+8 by parity. Further-left columns miss every old endpoint.
At depth at least10 the bar precedes all old endpoint tiles. These
observations prove both necessity and sufficiency of the table.

Every allowed K has q(K)=1-h. Put k=w+12-B, the retained breadth of V.
The exact increment in either rotor prefix is

    DeltaPhi(K|A+R_N)=DeltaPhi(K|A+R_S)
      =h-1-k*[K is left and d=8] >=3.

For K_R the tile/support counts are h+H-2,H-2, and for K_L they
are h+H,H+2, where H=(d+f)/2; the matching count is h+H-1.
There is no C contact because K ends in the preceding tile row.
The only possible old-A contact is K_L's depth8 bar above V. Its far
column has escaped V, so it covers whole aligned pairs of the V bar;
each pair adds one mixed full tile and FOUR directed events, net minus2.
There are exactly k/2 such pairs, so this exceptional debit is exactly k.
Disjointness at depth8 forces the far column to escape V, hence h>=k+4.
Consequently h-1-k>=3. The same width that permits the escape therefore
pays the entire bar contact debit from this original's own charge magnitude.
The far stems have no old shared tile, including both terminal boundaries.

There is no K/R_S shared tile. For R_N there is exactly one shared
tile T(a-1,w+14), completed by the two near-stem endpoints of K and
two R_N endpoints. It adds one full tile and two events, again net zero.
Original support exclusions determine those events; no per-site credit
is introduced. Therefore the total new increment of R_N,K is
h-1-k*[K left,d=8], at least3. For R_S,K it is
h-2-k*[K left,d=8], at least2. No old V contact receipt is reused.

The width debit cannot be omitted. For every even w>=12 in the first
residual, take k=w+8,z=4, R_S at t and K_L=U(w+12,8,4).
This endpoint-disjoint partial inventory has DeltaPhi(K_L|A+R_S)=3
and total DeltaPhi(R_S,K_L|A)=2, hence Phi(A+R_S+K_L) is exactly
one above baseline. This is a receipt witness, not a claim of complete
extendibility. The subsequent depth-eight exclusion proves that this
entire prefix has no complete extension in the stated model. It therefore
does not establish sharpness of the complete-family bound. The false
simpler formula h-1 would overestimate its
increment by k; counting all four directed events per V tile repairs it.

## Proof of the theorem and remaining global obligations

Let J be the actual owner of t. If it also owns e, apply the accepted
joint-consumer lemma, which chooses at most two actual originals beyond A.
Otherwise the east-terminal classification is exhaustive. A U gives
I=A+J with gain at least4. A rotor forces its distinct actual north-U
consumer K at e, and I=A+J+K has gain at least2. The old deficit is1,
so the distinct-owner branch is at least1 above baseline. This proves
the theorem in every case, without a common-consumer hypothesis.

Every selected original is an actual member of the given complete family.
The receipts use the same prefix, original support exclusions, full-tile
set and directed-event set. A consumed support is not a separate credit.
This proves nonreuse inside one prescribed residual package only.
It does not assign disjoint owner budgets to different packages, establish
nonnegative exterior marginal, or imply Phi(G)>=baseline from I subset G.
The global5/6 improvement and rectangular-grid triple equality remain open.

## Verification scope

The ordinary proof is the all-parameter role, interval and original-support
argument above. The independent checker reconstructs matching/support sets,
both endpoint-disjointness directions and the complete directed-event sets,
including the depth8 width debit and arbitrarily long sampled old/new legs.
The standalone Lean module proves the forced-support geometry, all U/rotor
collision certificates used to exclude the two upper rotors, and the
exceptional-width budget inequality. Source cardinalities, full role
classification and the final subinventory theorem remain written proofs.

The final [control receipt](../output/secondary-ten-distinct-consumer-controls.json)
records10560+27072 disjointness controls and7980+18840 exact source/tile/event
sets,48 rotor receipts,48 blocker certificates and3714 full-source role controls.
The [Lean receipt](../output/secondary-ten-distinct-consumer-lean-validation.json)
records14 clean declarations with individual ordinary axioms. The earlier
common-consumer theorem and this extension each have an
[ACCEPT written review](../output/secondary-ten-unconditional-review.json).
That review covers the original excess1 bound and explicitly excludes
independent execution certification. The subsequent depth-eight exclusion
and excess3 strengthening have separate local verification and review.
