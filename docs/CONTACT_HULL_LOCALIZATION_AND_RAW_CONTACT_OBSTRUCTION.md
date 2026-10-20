# Exact loss localization needs the feasible contact hull

21 October 2026. A component extension's signed effect is determined by a
canonical complete feasible contact core, not necessarily by its raw neighboring
owners. The correct core is the Horn closure of those owners. This gives a
local simultaneous loss bound for every collection of losing components.
An explicit complete nine-source configuration shows why omitting that closure
invalidates a proposed local budget. Full allocation and grid equality remain OPEN.

## 1. The canonical contact core

Keep every original-source hypothesis of
[the component theorem](COMPONENT_LOSS_AND_THE_MARKED_DEMAND_GAP.md). Let I subset J
be complete feasible mixed U/rotor families with arbitrary finite source count,
dimensions, phases and isometries. N always counts positive source occurrences.
R, component reserve increments and mu are integers in the original counting
ledger; the total number of all source owners is a separate quantity.
Partition the added owners by their connected NEW endpoint components Bj.

For any index set T let B(T)=union over j in T of Bj, and let

    D(T)={i in I: an original endpoint of i is adjacent to
                   an original endpoint of a B(T)-owner},
    C(T)=cl_J(D(T)).

This is the exact complete-source Horn closure, including implications caused
by original support/support conflicts. Because I is itself legal and contains
D(T), leastness gives C(T) subset I. The closure is complete feasible and is
the UNIQUE least complete feasible family containing every old contact owner.
It does not depend on witness choices. One may equivalently close inside I:
the closed subsets of J contained in I have the same feasibility semantics.

There is no endpoint edge from B(T) to I minus C(T), since every directly
adjacent old owner was already included in D(T). The complete family
X(T)=I union B(T) is feasible by the component theorem. Apply feasible-core
gluing to X(T), with shared core C(T) and exclusive parts B(T), I minus C(T).
Both sides are complete feasible. In particular

    Y(T)=C(T) union B(T)

is physically feasible, with all originally mandatory supports correctly
restored. Cases with empty exclusive parts are identities, not applications
of a theorem requiring nonempty branches. For T empty, D(T)=C(T)=empty.

The inherited shared-core theorem permits the empty complete feasible core,
with R=N=G=mu=A=0 there. For completeness, consider T nonempty but D(T) empty
directly. There is no endpoint edge between I and B(T). If a B(T) support
were consumed by an I-endpoint, its own B(T) anchor would make such an edge,
a contradiction. Thus every selection of B(T) is already selected in X(T)
and remains safe when occupancy decreases. Every full endpoint tile belongs
to one side, since its connected square graph cannot span both sides without
an endpoint edge. Directed events and gate-consumer incidences cannot cross
either. Source counts are additive. Hence all four valuations add with empty
overlap, and Y(T)=B(T) is complete feasible. This proves the boundary case
without requiring a nonempty contact core.

## 2. Exact signed localization and a local simultaneous loss bound

For Q in {R,N,G,mu}, the same complete feasible-core valuation gives

    Q(X(T))-Q(I)=Q(Y(T))-Q(C(T)).                     (1)

For R this counts actual source mass, events and mixed full tiles with the
same signs. Events and mixed full tiles in both sides are exactly those of
C(T). For G the fixed gate's unique consumer removes duplicate-new-core marks.
Thus no boundary credit, relaxed support condition or extra reserve is used.

Write dj=R(I union Bj)-R(I). If T consists only of reserve-losing components,
put ell(T)=sum over j in T of (-dj). The component theorem and (1) imply

    ell(T)=R(C(T))-R(Y(T)).                          (2)

Every positive activation already in C(T) persists in Y(T). Applying the SAME
global exact reserve identity 2R=A+U0+Z0+H to the complete family Y(T) gives

    2ell(T) <= 2R(C(T))-A(C(T)),
    ell(T) <= R(C(T))-ceil(A(C(T))/2).                (3)

This holds for EVERY collection of losing groups simultaneously. It localizes
the loss to the actual feasible contact core instead of granting each group
the reserve of all I. Overlapping C(T) are NOT independent resource pools:
one must apply (3) to the whole selected collection, rather than add separate
inequalities that reuse a shared contact core.

In particular a nonempty collection of strictly losing groups requires a
nonempty feasible contact core and 2R(C(T))-A(C(T))>=2. A core whose entire
reserve is already forced by its activation floor cannot support strict loss.

The core operator is monotone in T, and

    C(T union U)=cl_J(C(T) union C(U)).               (4)

This follows from leastness and D(T union U)=D(T) union D(U). It is a closure
identity. It does not assert monotonicity or submodularity of R(C(T)), nor
provide a fixed donor system to which a matching theorem can be applied.
Restored supports and changed original tile profiles matter when comparing
different retained cores. No sum of their standalone reserves is claimed.

## 3. A raw contact set can be physically infeasible

Use the explicit complete family J24 from
[the nine-source construction](DEMAND_HULL_RESERVE_COMPARISON_OBSTRUCTION.md),
with its fixed original matching, endpoint and support data. Take

    I={V6,V8,V9},       B=J24 minus I.

The old core I is complete feasible. The new owners B form a connected
endpoint group. Only V6 and V8 have endpoint edges to B, so

    D={V6,V8},         C=cl_J(D)={V6,V8,V9}=I.

Here is the explicit obstruction to using D as if it were feasible.
The point x=(-36,4) is an original V6 support, with own anchor a=(-35,4).
The retained V8 endpoint b=(-36,3) is its second occupied neighbor.
No D-owner has an endpoint at x. Hence x is mandatory selected in D but has
two occupied endpoint neighbors, a contradiction to complete feasibility.
In the full family x is the original endpoint of V9, which consumes that
support. Thus the exact Horn clause is {V6,V8} forces V9. V9 has NO direct
endpoint contact to B, yet its presence is necessary for the old core budget.

For a readable certificate of I's feasibility, write rho=physical row+24.
Its original endpoints are the three fixed constructors V6,V8,V9 in the
referenced table; they give60distinct endpoints and30disjoint matching edges.
All26finally selected points and their sole occupied neighbors are:

| Owner | Selected point(s) in (rho,c) | Sole occupied neighbor(s) |
|---|---|---|
| V6 | (-12,11),(-11,12),(-10,5),(-10,10),(-9,12),(-7,12) | (-11,11),(-11,11),(-10,4),(-10,11),(-9,11),(-7,11) |
| V8 | (-13,c), c=-3,-1,1,3 | (-12,c) |
| V8 | (-12,-4),(-11,-2),(-11,0),(-8,0),(-7,-2) | (-12,-3),(-12,-2),(-12,0),(-7,0),(-7,-1) |
| V8 | (-6,c), c=-1,1,3 | (-7,c) |
| V9 | (-18,c), c=4,6,8 | (-17,c) |
| V9 | (-17,3),(-16,5),(-13,5) | (-17,4),(-17,5),(-12,5) |
| V9 | (-11,c), c=6,8 | (-12,c) |

These are exactly the original supports outside the endpoint union. Substituting
the explicit endpoint intervals and this support list verifies every displayed
neighbor and excludes any second occupied neighbor. Original occupied sets
persist, so original endpoint degrees and matching remain valid. This is a
finite explicit counterexample certificate to raw-contact feasibility, not a
bounded enumeration standing in for a general allocation proof. The invalid
raw family cannot be assigned a feasible reserve budget from the exact ledger.

## 4. Localization does not restore reserve monotonicity

In the canonical demand-hull extension H70 subset J70, the added group is
{V5,...,V9} and its raw contact set and contact hull are both {V3}.
The contact hull is a strict subset of H70, yet its reserve77 is GREATER than
R(H70)=48. The local extension {V3,V5,...,V9} has reserve53, while R(J70)=24.
Both calculations give the SAME actual loss24:

    R(H70)-R(J70)=48-24=77-53=R(C)-R(Y).

Thus localization is an exact signed statement, not a claim that the smaller
core's standalone reserve is uncommitted inside the larger family. In
particular (3) does not replace the target L<=mu(H) with L<=R(C).
The previously established example of two losing groups sharing V3 still
requires their aggregate loss to use its reserve only once.

For the FULL allocation target, the next question is whether the contact cores'
actual overlap with marked-demand owners protects enough of their reserve to
give L<=mu(H), including H=J. Equations (1)--(4) and the raw-contact obstruction
do not prove that remaining inequality or construct a negative-margin family.

## 5. Verification scope

The checker reconstructs actual contact neighbors and exact Horn closures,
tests complete support feasibility of C(T), Y(T) and X(T), checks event/full
tile unions AND intersections and actual mark valuations, and verifies the
aggregate local loss bound on every tested collection of negative groups.
It records raw-contact failure witnesses and the concrete core certificates.
Finite controls supplement the general proof in Sections1--2.

The Lean source works with arbitrary source and vertex types. It proves that
the contact hull stays inside the old feasible family, contains every old
owner adjacent to added endpoints, gives a feasible local extension with
restored supports, and is the least feasible contact carrier. These are
source-level results using the earlier Horn and feasible-core theorems.
The physical component, event/full-tile/mark counts, reserve localization and
activation-floor adapters remain written; no end-to-end Lean or full target
claim is made.

Four new source-level Lean4.33 declarations compile and pass axiom audit:
the endpoint separation declaration is axiom-free; the other three use only
propext, Classical.choice and Quot.sound. The physical controls pass704images
and383680contact subextensions, including314368proper contact cores,
448raw-contact failures and896strictly losing component collections.
The separate explicit raw-contact certificate independently reconstructs
all source endpoints, supports and canonical matching edges and verifies
every one of the26selected points. It is reproducible by importing
raw_contact_obstruction_certificate from develop/check_contact_hull_localization.py.

Independent review088ddf2e accepts the written localization theorem and the
J24 certificate under the inherited model. Its requested clarification of
empty shared cores is explicitly supplied in Section1 above, together with
a direct no-contact proof; the integer ledger convention is explicit as well.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
