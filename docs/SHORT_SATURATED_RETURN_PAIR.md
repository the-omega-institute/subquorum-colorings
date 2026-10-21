# A four-row chamber pays short saturated vertical-corner returns

21 October 2026. This extends the width-ten compensation mechanism to
arbitrarily wide incident legs, including the width-twelve return
U(6,8,6). The unrestricted mixed U/rotor allocation and rectangular-grid
triple equality remain OPEN. This is a conditional theorem in the complete
original-source model, not an assertion of complete Vcorner realizability.

## 1. Model and geometric theorem

Use finite complete original U/rotor families: original endpoints are
pairwise disjoint, original matching edges persist, and every unconsumed
original support remains selected with its original endpoint anchor as its
sole occupied neighbor. Optional selected vertices have no endpoint neighbor.
Endpoint graphs are connected by unit lattice edges. U widths are even
and at least six; their two independent legs are even and at least four.
Charts preserve the fixed aligned two-by-two tiles.

Suppose two original sources have frames

    X=U(b-2,a,k), X(r,c)=(c+2,r+3),
    Q=U(6,g,g-2), Q(r,c)=(b+2-c,g+3-r),
    b>=8, a>=4, k>=4, g>=k+2,

with all parameters even. Their endpoint sets are disjoint. There is no
upper bound on b,a,k or g. The far leg g-2 of Q is called saturated here
only as a dimension description: it reaches physical column5. This is
unrelated to other uses of saturated adjacent bands.

**Pair theorem.** In every complete extension retaining X and Q, the tile

    J={b-2,b-1} x {4,5}

contains exactly the two original X lower-bar endpoints in column4; its
two column5 vertices are unoccupied. J is a permanent original irregular
2P0T pair, contributing two units to the existing exact defect sum 2R,
equivalently one unit to R.

Only X and Q are needed for this permanence statement. In particular no
dimension restriction on other owners, sign restriction, source-count
bound or finite enumeration assumption enters it.

## 2. A four-row chamber with a bottom obstruction

The entire lattice boundary of

    D=[b-4,b+1] x [4,g+2]

consists of X/Q endpoints. Q's far stem supplies the top from column5,
with X at column4; Q supplies the entire bottom and right side; X supplies
the left side through row b, immediately before Q's bottom-left corner.
The strict interior has precisely FOUR rows b-3,b-2,b-1,b, with no
restriction on its number of columns. X has interior endpoints only on
its far stem, row b and columns5 through k+3; Q has none.

Any foreign source meeting the strict interior is confined there: a unit
endpoint path leaving it must cross the already owned boundary. A U
cannot fit, since every orientation spans at least five rows. A rotor
has extent exactly four rows and four columns, so a confined rotor uses
all four interior rows.

We need exclude rotor endpoints only on the FIRST interior column5, not
every rotor in the chamber. Such a rotor has its leftmost tip at column5.
Up to translation its two possible endpoint footprints, with that tip
at x=(0,0), are

    R-={(-2,1),(-1,1),(-1,2),(-1,3),
         (0,0),(0,1),(0,2),(1,2)},
    R+={(-1,2),(0,0),(0,1),(0,2),
         (1,1),(1,2),(1,3),(2,1)}.

For R-, confinement in the four rows makes x.row=b-1; its bottom
endpoint is then (b,7). For R+, it makes x.row=b-2; its bottom endpoint
is (b,6). Both are original X far-stem endpoints, since k>=4. Thus
neither rotor can have an endpoint on column5. Endpoint uniqueness rules
out each of them individually, irrespective of other foreign sources.

This proves that no foreign owner has an interior endpoint on column5.
It does NOT claim that the whole wide chamber is empty. For example
farther-right rotor endpoint footprints may fit geometrically; their
full support feasibility is a separate question and unnecessary here.

Neither (b-2,5) nor (b-1,5) is an X or Q endpoint. Both lie on that
first interior column, so neither can become an endpoint in any complete
extension. A selected point there would have its west X endpoint as its
sole original anchor and would therefore have to be an original X support.
Its X coordinates are respectively (2,b-4) and (2,b-3), whereas original
row-two supports occur only at columns0 and b-1. Neither point is an
X support; optional selected vertices cannot be adjacent to X either.
Thus neither is selected. This proves the pair theorem.

The rotor obstruction is essential. Four rows alone exclude U sources,
but permit rotors. The proof uses X's specific bottom endpoints at columns
6 and7 instead of incorrectly applying a three-row empty-chamber theorem.

## 3. Actual marked-side demands and joint injection

Now suppose X occurs as the actual Vcorner consumer in a normalized
marked positive-side chain with actual original owners

    A=U(w,L,K), A(r,c)=(r,c),
    B=U(W,b,e), B(r,c)=(b+3-r,c+1),
    C=U(V,h,f), C(r,c)=(c+1,h+2-r),
    X=U(b-2,a,k), X(r,c)=(c+2,r+3),
    h>=8, 4<=a<=h-4, h<=w-4.

The actual gate is t=(3,2) and X consumes y=(3,3). Assume its forced
support q=(b+1,3) is consumed by the Q in Section1. This is an explicit
condition on the ACTUAL original consumer, not a claim that every larger
band forces that return. In particular W must allow the endpoint-disjoint
occurrence. The consumer Q has negative phase in these charts; its two
supports at q are B-owned, giving no positive activation receipt.

Assign this actual Vcorner demand to J. The target reconstructs its
unique original owner X, its lower bar, the adjacent far bar end, and
therefore the OPPOSITE actual corner y=(3,3). Its west gate endpoint fixes
B. The two possible positive-producer anchors are (3,1),(4,2), of which
(4,2) is B-owned. Unique endpoint ownership at (3,1) and established
canonical-gate uniqueness identify the original positive marked side.
Hence different such demands have different targets.

The same reconstruction proves compatibility with every previously
certified maximal-width-ten Vcorner demand, whose target was identical.
A demand satisfying both theorems is one demand. A pair with two
certificates remains one physical pair. The two Vcorner classes are
combined by SET UNION, not by adding their cardinalities.

There is also no reuse with any established short/long H demand. An H
demand targeting the same pair must use X's ADJACENT far corner (b,3).
Its chart transforms by Phi(r,c)=(b+3-c,r). Its old p=(2,2) maps to
(b+1,2), already B-owned. The established H transverse-source theorem
requires a consumer C_old(r,c)=(c+1,h_old+2-r), h_old>=4. Transporting
it gives (b+1-h_old+r,c+1). Unique ownership of (b+1,2) identifies this
source with B. But its bar endpoint (0,2) maps to
(b+1-h_old,3), whereas B has endpoints in column3 only on rows b+2,b+3.
Contradiction. This comparison does not depend on W,k,g or a. Recurring
owners are allowed; the forced identification with B is specifically
disproved, rather than assuming that each consumer is a fresh owner.

The target pair is disjoint from the existing upper-bar pairs: X uses
its other intrinsic bar row, and different owners cannot share endpoints.
It is disjoint from caps and m8 triples by its exact two-endpoint profile.
It contains no original terminal. Every external positive-producer anchor
at either endpoint is X-owned, so it is not a positive canonical gate tile.
Activations stay in their existing separate term of the exact identity.

## 4. Single-use accounting and the enlarged coverage class

Let V be the UNION of eligible residual maximal-W10 Vcorner demands and
the actual short saturated return demands above. Only demands outside
the previously certified activation and cap classes are selected. Let
H be the existing short/long H demand set and put s=|H union V|. Include
all new certificates in the SAME physical lower-pair union P; write p=|P|.
The joint injection proves s<=p. No other unclassified demand is removed
from the residual set, whose cardinality is t.

With the established nonnegative quantities n0,u,m8,rho and accepted
activation/cap counts q,c, the same complete-family ledger gives

    G=q+c+s+t<=2(N-n0),
    Aactivation>=q+rho,
    2R>=Aactivation+m8+c+2p+2u,
    mu=N+R-G>=n0+u+p+ceil((m8-s-t+rho)/2).

If t=0, this becomes

    mu>=n0+u+(p-s)+ceil((m8+s+rho)/2)>=0.

Thus the earlier automatic coefficient-one coverage class now includes
arbitrary g short saturated returns, including g8 in W12. Through the
established sigma>=mu reduction it yields |T|+|M|<=mn/2 on that covered
class, improving its prior5/6 matching coefficient. There is no universal
improvement or arbitrary-grid decomposition claim.

With the other certificate quantities fixed, if Jnew is the new physical
pair set and Pold the previous set, then
the increase in this certified floor is EXACTLY |Jnew minus Pold|:
moving demands from t to s leaves s+t unchanged. A previously counted
pair contributes no new capacity. This remains true if a width-ten demand
or the same source receives several geometric descriptions.

For a complete retained family I extended to J, let L be the sum of
negative reserve increments of the added endpoint components. Count p
only for certificates already established in I with X and Q retained.
The permanent floor holds in the ONE intermediate family containing
exactly the losing components, so the established argument gives

    L<=R(I)-p-u-ceil((A(I)+m8(I)+z)/2).

No per-component copy of R(I), p or the same pair is allocated.

## 5. The remaining opening

The short far leg U(6,8,4) leaves a two-column opening at the top of the
prospective chamber; Section2 does not apply. For every even b>=10,
X=U(b-2,a,6) and that Q permit the endpoint-disjoint partial intruder

    D=U(6,4,4), D(r,c)=(c+b-7,r+5),

which fills both missing column5 points of J. This is a counterexample
to protection based on these endpoint sets ALONE, not to permanence in
complete families, not to a proposed complete-family compensation rule,
and not to mu>=0. Additional owners A/B/C can also have disjoint endpoints;
their full support feasibility has not been established.

The partial intruder forces Q's support (b-5,7) and D's support (b-5,8)
to become endpoints. Their consumers may be the SAME owner. For example,
when b>=14 the single endpoint-disjoint source

    P=U(6,4,4), P(r,c)=(b-4-c,11-r)

consumes BOTH points (and the third forced point (b-5,9)). Consequently
one cannot derive impossibility by assigning those adjacent supports to
distinct owners. Further continuations or a different compensation rule
are required. No finite partial stencil here is a complete-family witness.

These claims are explicit all-parameter endpoint calculations. D's bar
occupies rows b-6 through b-1 in columns5,6, its two stems are on rows
b-6 and b-1 and end at column9. At (b-5,7), Q supplies the south endpoint
and D supplies the north and west endpoints. At (b-5,8) and (b-5,9),
their north D and south Q endpoints are distinct. All three points must
therefore be consumed. P's near stem is exactly row b-5, columns7..11;
its bar is on columns10,11 and its far stem on row b-10. Thus it avoids
X,Q,D and B, and b>=14 keeps its endpoints below the top row2 of C.
For an endpoint-disjoint actual A/B/C stencil, one can take a=4,
h=b+4, V=b+4, f=e=4, w=b+8 and both A legs4. C's bar then lies beyond
column11 and its far stem below B. These remain partial families with
unresolved retained-support violations.

## 6. Validation

The written proof above handles arbitrary sizes and numbers of additional
sources. Independent geometric controls PASS on168 endpoint-disjoint
X/Q patterns,1344 aligned tile images,15936 confined rotor images,
1248 first-column rotor collisions and216 U extent controls. Another9312
endpoint-only rotor images farther right explicitly check why the proof
must not claim that arbitrary-width four-row chambers are empty. Eighteen
partial actual marked-chain patterns and234 old-H frame exclusions pass.
Sixteen short-leg partial intruders and fourteen shared-consumer partial
continuations pass; none is a complete-family counterexample. See the
[checker](../develop/check_short_saturated_return_pair.py) and
[control receipt](../output/short-saturated-return-pair-controls.json).

All16 scoped Lean4.33.0 declarations pass, finalsession66230 exit0, with
individual axioms only propext, Classical.choice and Quot.sound, no
sorry/native axiom. The authorized local Mac had49% free memory and no
actual lean/lake executable by comm basename before starting. The first
run's two tactic errors were repaired; that failed run is not validation.
The formal source includes the combined first-column barrier under an
explicit source-catalogue hypothesis, as well as walk confinement, rotor
collisions and the integer coverage corollary. The adaptation of all actual
sources to that catalogue and the global joint injection remain written.
See the [direct Lean source](../formal/SubQuorum/ShortSaturatedReturnPair.lean)
and [formal receipt](../output/short-saturated-return-pair-formal-check.json).

A five-source width-twelve short-saturated seed has a41358-candidate
bounded U/rotor UNSAT in[-6,28]^2, added widths6..12, legs4..8 and at most32
additional sources. The run exited0 in59.99seconds. This supplies neither
a complete Vcorner witness nor a general noncompletion proof. It is not
a premise of the pair theorem. See the [seed](../output/short-saturated-width-twelve-seed.json)
and [bounded receipt](../output/short-saturated-width-twelve-discovery.json).

Independent written audit03bc52af is running in conversation
conv_c92ee3713bd6a7fd, originalstream13069. No review conclusion is
claimed before that original task completes.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
