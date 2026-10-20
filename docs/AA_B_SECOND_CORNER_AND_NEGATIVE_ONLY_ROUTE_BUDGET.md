# No B occupied-band exit exists in the specified AA residual

20 October 2026. In the SPECIFIED established failing nonexceptional R1
endpoint component, B occupied-band exits are impossible. The generic
seven-point B stencil alone leaves two rotor roles. AA's actual incoming owner
removes them; opposite incoming owners exclude positive ownership; and the
remaining negative terminal must cross the companion's stem or bar. The
joint all-route census then has an exact negative-only form with no A term.
The unrestricted allocation and rectangular-grid equality remain OPEN.

## 1. Precise setting and the B frame

Retain ALL complete-source, original-ownership, matching, mandatory-support,
degree and fixed transported-partition hypotheses of
[the D two-corner theorem](BACKFILL_D_INTERIOR_TWO_CORNER_COMPENSATION.md).
This note additionally restricts to its SAME established AA endpoint component:
R=1, A=2, U0=Z0=H=0, exactly two doubly marked width6 positives, whose only
activated terminals are their short tips. Other unactivated positives and
arbitrarily many negative sources/rotors are permitted. The accepted incoming-
owner normalization and Fpos=0 come from the four-stem/cap-continuation proofs.
Section5's census uses the D note's AA consequence Cplus=Dplus=0 as a stated
dependency. The standalone no-B proof in Sections1--4 does not use it.
The letter b in those sections denotes a legal short height, not the old
B-interior event count; that event count is zero by the theorem below.

Every B event is interior: its cap case injects into Fpos=0. In its original
band normalization, the positive owner O and companion F have

    O(r,c)=(c,-r-1), F(r,c)=(c-1,r-h-1),
    x=(1,-a-1), y=(1,-a-2), a<=h-4.

The output x is an activated ORIGINAL terminal, so it is one of AA's two short
tips. Normalize that positive source instead to O=U(6,long,b), long>b, with

    z=x=(b,6), y=(b+1,6),
    R1(r,c)=(k+2-r,c+4) on U(v,k,f), k>=b.                 (1)

The B terminal's outward west direction maps to south at z; its north side
support maps to east. This uniquely gives the signed displacement map

    (dr,dc)->(-dc,-dr).

It sends the two companion endpoints to (b,7),(b+1,7), and y one step south
of z. Thus the incident B height is b. The partition is transported: z is
the even-row/even-column corner and y the odd-row/even-column corner.

## 2. The actual incoming endpoint removes the remaining rotor roles

At k=b, R1 owns (b+1,7) but lacks (b,7). Since F owns both points, F differs
from R1 and collides at (b+1,7). This is impossible. Both heights are even, so

    k>=b+2.                                                 (2)

For (2), R1 lacks y=(b+1,6): its inverse coordinate is(k-b+1,2), a strictly
below-bar interior column. But R1 owns p=(b+1,5), a near-stem endpoint.
Therefore p is FOREIGN to the actual original owner J of y. The owner J
is already different from F,O because y has exact singleton profile in the
full B output tile.

Relative to y in the ORIGINAL B frame, the complete F/O endpoints contain

    Bstencil={(-1,-2),(-1,-1),(-1,0),(-1,1),(0,1),(0,2),(0,3)}.

The first four are F's complete horizontal stem run and the last three are
O's incident stem. All sixteen anchored two-chirality rotor roles leave exactly
two distinct endpoint images avoiding Bstencil:

    {(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)},
    {(0,0),(1,-2),(1,-1),(1,0),(2,-1),(2,0),(2,1),(3,-1)}.

Both contain(1,0). The signed map in Section1 sends(1,0) to the actual incoming
endpoint p relative to y. Hence Bstencil union{(1,0)} excludes EVERY rotor
role. The original J is a U. This additional blocker is why the result is
restricted to AA; the generic B stencil does not prove a U-only exit.

In physical AA coordinates J has foreign endpoint neighbors north(z),
east(F), and west(R1). A complete U nonterminal endpoint has at least two
original endpoint neighbors; it cannot fit with three of the four neighboring
positions foreign. Therefore y is an original U terminal, whose stem extends
south and whose outward direction is north. The original singleton catalogue
leaves phase01 or phase00, with no phase10 bar-corner alternative.

## 3. Positive ownership would force two distinct incoming owners to overlap

Suppose J were positive. Its singleton has its two original intratile supports
north/east, both consumed. It is therefore the OTHER actual AA short-tip
activation (it differs from z). If its short height is t>=4, singleton parity
and the north-pointing terminal fix its other stem to the west. Its normalized
map is exactly

    O2(r,c)=(b+1+t-r,c), O2 is U(6,long2,t), long2>t.

Transport the SAME accepted incoming-owner theorem to O2. Its incoming original
source has map

    R2(r,c)=(b+t-l-1+r,c+4) on U(v2,l,f2), l>=t.           (3)

Set q=(b+t-l-1,6), on R2's first bar row. Then

    p=(b+1,5) belongs to R1 AND R2,
    q belongs to R2 but NOT R1.                             (4)

The inverse R2 coordinate of p is(l-t+2,1), with2<=l-t+2<=l;
q has coordinate(0,2), so both are endpoints. Its physical row is at mostb-1.
The inverse R1 coordinate of q is(k-b-t+l+3,2), whose row is at least5
by k>=b+2 and l>=t. Column2 is not either stem column because v>=6.
Thus q is not an R1 endpoint. All equal-height boundary cases l=t are included.

In particular (4) proves R1 and R2 are DIFFERENT original sources; they cannot
be a single recurring incoming owner. Their common p then violates original
endpoint uniqueness. This excludes positive J. Therefore

    EVERY B second corner in AA is a negative phase01 U terminal.            (5)

The argument uses only original endpoints and the two actual AA short-tip
normalizations; it does not demand a new positive source or assume fresh owners.

## 4. The remaining negative terminal cannot fit

In the physical normalization of Section1 the companion has exact map

    F(r,c)=(h-r,8-c) on U(v,h,f), h>=b+4.

Its near stem owns(0,7) through(h,7), and its full bar owns(h-1,6).
The remaining phase01 terminal at y points north, has its other stem to the
east, and therefore has exact form

    J(r,c)=(b+t+1-r,c+5) on U(w,t,fJ), t>=4.

Its incident stem owns(b+1,6) through(b+t+1,6), and its bar owns(b+t+1,7).
If b+t+1>=h-1, that stem meets F's bar at(h-1,6), since h-1>b+1.
If b+t+1<h-1, its bar point(b+t+1,7) lies on F's complete near stem.
Either case violates endpoint uniqueness: J differs from F by the original
singleton/pair profiles in the output tile. Independent far heights and all
legal widths are unrestricted. Consequently

    KB=Binterior=0 in the specified AA endpoint component.  (6)

This final crossing proof is unbounded and does not extrapolate from a finite
search. Combined with Sections2--3 it excludes every possible owner of y.

## 5. One negative-only all-route census in AA

Let LAA be the SAME enlarged negative complement Lnew from the D two-corner
proof, now restricted to this AA component. No B second-corner occurrences
are added: there are no B events. Here Cminus=KC, Dminus=d, Fpos=U0=0.
The original cap and negative-pool partitions give exactly

    Fneg=2K11,
    2(K01+K10)=2K11+e+2KC+2d+LAA, LAA>=0.                 (7)

Retain the original selected-cap identity and Q from the accepted all-route
proof, and KB=0, KD=KDcap+d. Since

    2K11+2KC+2d=Kback+KC+d+Q,

equation(7) becomes

    2(K01+K10)=Kback+KC+d+e+Q+LAA,                         (8)
    Kback+KC+d+e+Q<=2(K01+K10).                            (9)

This removes the right-hand +2 in the preceding AA necessary inequality.
The exact negative pool no longer contains any possible positive second exit
or B activation. It does NOT spend A again or change R. The separate activation
constraint becomes Eterm<=2. All counts concern this specified endpoint component.

## 6. Scope

The finite rotor calculation is an exhaustive fixed-template argument. Source
stencils and incoming-owner examples supplement the all-parameter written proof;
they do not supply a complete AA or critical U10 realization. Scoped Lean
statements check the rotor counts, exact signed frame, unbounded U terminal
classification, incoming endpoints/missing points, and conditional single-pool
all-route identities. Physical singleton/phase transport, AA incoming theorem
application and global occurrence packing remain written adapters.

All10 scoped Lean4.33.0 declarations compile without warnings and pass individual
axiom audits, with only propext, Classical.choice and Quot.sound as applicable.
The two rotor declarations are axioms-free; there is no sorry/native_decide or
additional axiom. Final source86458 exit0/free44%; axiom chunkb919f1 exit0/free45%.
Memory and actual lean/lake comm basenames were checked before every invocation.
See the [source](../formal/SubQuorum/AABSecondCorner.lean) and
[formal scope](../output/aa-b-second-corner-formal-check.json).

The [controls](../output/aa-b-second-corner-controls.json) include all16 rotor
roles,34partial B stencils,81equal-height companion collisions,162opposite
incoming collisions (54upper equal-height boundaries),405final stem/bar
crossings and990conditional AA ledger identities. Complete feasible critical
U10 and AA coverage remains ZERO. These collisions test impossibility adapters,
not feasible combined examples. The new B theorem has its own completed
[independent ACCEPT](../output/aa-b-second-corner-review.json), task491d89ef,
completed20October14:06:15UTC, observedgpt6/pro. Its19793-character answer
matches the original completed stream exactly. No must-fix mathematical issue
was found. The verdict is a mathematical/static-source review, not certification
of compilation, controls or the unrestricted target. The census acceptance
retains inherited occurrence/cap identities and the earlier C grouped-stencil
adapter as explicit dependencies; that C source was absent from this packet.
The preceding D/AA review cannot substitute for this separate B verdict.

This is a new necessary condition for the unresolved AA branch, not an exclusion
of all AA fusions. No proof yet forces its left side to exceed the available
negative source count. The FULL unrestricted allocation and rectangular-grid
triple equality remain the active objectives. The preceding D/AA review packet
does not include this later B theorem; its review scope must be recorded separately.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
