# A near-tight vertical corner forces two jointly unused activations

21 October 2026. This resolves the next incident-leg subclass a=h-6 of
the negative Vcorner role. Unlike a single activation transfer, it improves
the certified integer allocation lower bound by one per new claim, without
a parity loss. Unrestricted mixed allocation and rectangular-grid triple
equality remain OPEN. No complete near-tight witness is asserted here.

## 1. Model and statement

Use exactly the finite complete original U/rotor model and labelled-side
normalization of [the tight theorem](TIGHT_VCORNER_ACTIVATION_TRANSFER.md).
Original endpoint ownership is unique, original matching edges persist,
and every original support not consumed by an endpoint is retained with
its original anchor as its sole occupied neighbor. Optional selections
have no endpoint neighbor. Transport whole sources, supports and anchors;
all physical tiles are fixed aligned two-by-two tiles. Widths are even>=6;
both independent leg lengths are even>=4. N counts positive owners only.

The actual marked side determines distinct owners and frames

    A=U(w,L,K), A(r,c)=(r,c),
    B=U(W,b,e), B(r,c)=(b+3-r,c+1),
    C=U(V,h,f), C(r,c)=(c+1,h+2-r),
    X=U(d,a,k), X(r,c)=(c+2,r+3),
    b>=6, 4<=h<=w-4, d<=b-2, a<=h-4.

Our additional hypothesis is a=h-6. Thus h>=10. Put

    v=h-2, x=(3,v), z=(3,v+1), u=(3,h).

**Theorem.** Every complete occurrence forces three distinct U
owners in the frames

    Q1(r,c)=(ell+3-r,v+1-c),
    D(r,c) =(g+3-r,h-c),
    Q2(r,c)=(j+3-r,h+1-c),

whose widths and far-leg lengths are independent. Q1 and Q2 are positive,
D is negative, and

    6<=ell, ell+2<=g, g+2<=j, j<=V-4.             (1)

The three owners are distinct from each other. Q1 and Q2 are distinct
from A,B,C,X. D is distinct from A,C,X but MAY be B, using B's other
terminal and transported leg labels. No step requires D to be a new
owner or assigns a resource merely for introducing it.

The original terminals x of Q1 and u of Q2 are both actually activated.
For every original near-tight claim, assign BOTH terminal occurrences.
Across all such claims, these assignments are injective and disjoint
from all old S/P/R targets, all all-length E/S targets and all tight
Vcorner targets. In particular V>=14. At h=10, also V>=d+10.

These are necessary conditions on arbitrary complete extensions. Added
sources cannot erase any fixed endpoint collision used below. No bound
is placed on their sizes, their number or the unrelated far legs.

## 2. A small boundary-role lemma

At a point s=(3,c) with h-2<=c<=h-1, suppose its north neighbor is
C-owned and its west neighbor belongs to a different fixed owner. Assume
the consumer of s differs from BOTH those neighboring endpoint owners.
It can then have own endpoint neighbors only east/south. The
original U catalogue leaves a terminal, or one of the two outer upper
bar corners. Other U degree-two points have opposite neighbors; internal
bar/junction points have degree three. Rotor centers have degree three.

Every U role with an east own neighbor is impossible: an east terminal
continues at least four steps, a horizontal bar at least five, and a
horizontal incident leg at an upper corner at least four. Each includes
(3,h+1), C's lower-bar endpoint, at distance at most three to the east.
Thus any U consumer is a south terminal. Its incident length t satisfies
t<=V-4: C's far leg contains (V+1,c), since its original row h+2-c is
3 or4, and f>=4. Its stem would meet that point if t>=V-2. A rightward
bar would contain (t+2,h+1), on C's lower bar because t<=V-4 and its
width is at least six. Consequently its bar points left.

For clarity, all four possible rotor footprints with no north/west own
neighbor, relative to their tip, are

    Rs+={(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)},
    Rs-={(0,0),(1,-2),(1,-1),(1,0),(2,-1),(2,0),(2,1),(3,-1)},
    Re-={(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)},
    Re+={(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)}.

The east-pointing forms hit C: Re- contains (-1,1) and Re+ contains
(-1,2). At c=h-2 these are C near-leg points; at c=h-1 the latter
is C's bar corner (2,h+1). Only the two south-pointing forms Rs+/Rs-
can survive this boundary-role lemma.

Two south-pointing rotor tips in adjacent columns always overlap:

| First at (0,0) | Second at (0,1) | Shared point |
|---|---|---|
| Rs+ | Rs+ | (1,1) |
| Rs+ | Rs- | (1,0) |
| Rs- | Rs+ | (2,1) |
| Rs- | Rs- | (1,-1) |

This is an explicit four-case endpoint collision, not a bounded search.

## 3. Force Q1, D and Q2

X's near terminal is (3,h-3), so x=(3,h-2) is its mandatory original
beyond-tip support. Its north neighbor (2,h-2)=C(4,1) is a second
occupied endpoint. Thus x must be consumed; neither C nor X owns it.
At z=(3,h-1), C has an ORIGINAL inner support, intrinsic (3,2), with
anchor (2,h-1). Once x is an endpoint, z has its anchor and x as two
occupied neighbors and must also be consumed. Neither C nor X owns z.
At x the consumer differs from C and X, as required by the boundary
lemma. At z it differs from C because z is C's original support; after
the boundary lemma classifies x, every surviving x-role has only a south
own neighbor, so its owner cannot also own z. These are application-specific
owner exclusions, not an assumption that every consumer is a new source.

Apply the boundary-role lemma at x. If its consumer were Rs+, a leftward
south-terminal consumer of z would hit it at (4,h-1). If it were Rs-,
that terminal would hit it at (5,h-1). Every such terminal includes both
points on its stem because its incident length is at least four. A rotor
consumer at z must be Rs+ or Rs-, and the table excludes all four pairs.
The consumer at x cannot own z because it has its only own neighbor south.
There is therefore no consumer for z if x is rotor-owned. This excludes
both remaining rotor cases at x. Its consumer is the leftward south
terminal Q1 with the asserted frame and length ell.

Now consider z again. Its south rotor Rs+ contains (5,h-2), on Q1's
stem; its Rs- contains (4,h-2), also on that stem. East rotors and all
other U roles are already excluded. Hence z is the leftward south
terminal of D. The two owners are distinct: Q1 has no endpoint east
of column v, whereas z has column v+1. D's leftward bar contains
(g+2,v). If g<=ell, this belongs to Q1's incident stem. Thus, by
evenness, g>=ell+2.

D's mandatory lateral terminal support is u=(3,h). Its north/east
neighbors are C(2,1)=(2,h) and C(1,2)=(3,h+1), while its west
neighbor is D's terminal. Completeness forces u to be consumed with
its only possible own endpoint neighbor south. The two south rotor
footprints hit C at (4,h+1) or (5,h+1), exactly as in the tight theorem.
Thus the consumer is a U terminal. The C far-leg endpoint (V+1,h)
gives j<=V-4; its rightward bar is blocked by C, forcing the Q2 frame.
It is distinct from C,Q1,D, which do not own u. Its bar contains
(j+2,h-1), so avoiding D's incident stem gives j>=g+2.

For Q1's strengthened lower bound, write omega for its width, nu for
its far length. If omega<=v-4, its far column v+1-omega lies between
5 and v-5, inside X's near row-three stem. If nu>=ell, Q1 would own
(3,v+1-omega), an X endpoint. Hence nu<=ell-2 and ell>=6. Otherwise
omega>=v-2 and Q1's bar reaches column4. Avoiding X's vertical bar
forces ell>=d+2>=8. This proves ell>=6 in both exhaustive branches.
At h=10, v=8, the first branch would require omega<=4 and is impossible;
therefore ell>=d+2, giving V>=j+4>=ell+8>=d+10. Generally (1) gives
V>=ell+8>=14, excluding widths6,8,10,12 without a finite premise.

The odd reflection constants for Q1 and Q2 preserve physical tiles;
they are positive sources. D's constants give the negative-U singleton
phase. Q1's original terminal supports are (2,v) and z, consumed by
C and D, respectively. Q2's are (2,h) and (3,h+1), both C-consumed.
Each terminal is ONE activation despite its two consumed supports.

## 4. Joint injection and every cross-type exclusion

Treat a claim as an actual labelled side (positive original owner,
intrinsic leg), counted once. Recovering a claim from Q2 uses exactly
the tight theorem's reconstruction: its ordered supports are C(2,1)
and C(1,2). They determine C's incident bar end, directed frame and
terminal p=(2,2). Then t=(3,2) is B-owned, and B also owns (4,2).
The sole possible positive producer anchor is (3,1). Endpoint ownership
and canonical-gate uniqueness recover the original labelled A side.
The actual owner at y=(3,3) then distinguishes tight and near-tight
claims by its actual a. This is one injection on their UNION, not an
extra independent copy of a tight-target pool.

For Q1, its ordered outward support is the C-owned (2,v)=C(4,1),
and its other support is the distinct D-owned terminal z. The actual
C role (4,1) identifies the incident leg and bar end; its original
direction fixes C's frame and hence the same p,t,B and labelled A side.
Thus Q1 targets also inject on near-tight claims. No Q1 target equals
a Q2 or tight target: the former have two distinct support owners,
the latter the same original C owner at both supports.

Q2 nonreuse against all old S/P/R and all-length E/S targets is EXACTLY
the tight theorem's frame/ownership argument; it uses A,C,h and the
target frame, not the identity of the endpoint west of u. It therefore
applies unchanged to this combined tight/near-tight target union.

For Q1, use v=h-2. The exact old recipient frames in their original
positive producer charts, with the actual target incident leg named near,
are

    S_old(r,c)=(ell+3-r,3-c), P_old(r,c)=(c+2,r+2),
    E_comp(r,c)=(c+2,ell+3-r), S_comp(r,c)=(ell+3-r,c+2).

The first two are the accepted S/P dependencies from the tight theorem.
The last two are precisely the E and S rows of Section1 of
[the all-length companion theorem](ALL_LENGTH_SINGLETON_COMPANION_INJECTION.md),
with its joint-injection scope in Section2: arbitrary allowed incident
lengths and independent far legs, not only b=6 or ell=4. They describe
the target's actual whole-source frame, so the comparisons apply after
any permitted transport of the old producer chart and leg reindexing.
Distinct support ownership alone would NOT establish the E/S exclusions.
Solving F composed with the respective old frame equals Q1 forces:

| Old target | Forced old producer F(r,c) | Original endpoint | Collision |
|---|---|---|---|
| S | (r,c+v-2) | (0,1) | A(0,v-1) |
| P | (ell+5-c,v+3-r) | (1,ell+3) | (2,h)=C(2,1) |
| E companion | (c,v+3-r) | (1,1) | A(1,v+2) |
| S companion | (r,v+3-c) | (0,1) | A(0,v+2) |

All A collisions lie on its original bar since v+2=h<=w-4. The P
endpoint exists by the established arbitrary-length bound w_old>=ell+4.
Self-owner exclusions are necessary: in the first row all old endpoint
columns are >=v-1>1, unlike A; in the E row all are <=v+3=h+1<w;
in the S-companion row all are <=v+2=h<w. In the P row all old
endpoint columns are <=v+3=h+1, whereas C owns endpoints in column
h+2. Thus none of the collisions merely identifies the old producer
with the fixed owner. Finally every old R target has a rotor-owned
support, while Q1's support owners C,D are both U owners. This excludes R.

Together these facts prove that ALL old/tight targets and BOTH targets
for each near-tight claim are globally distinct. Component boundaries,
repeated appearances of an owner in other roles and equal far lengths
do not create a second copy of a terminal occurrence.

## 5. Integer gain in the SAME allocation ledger

Let q_old count the old S/P/R, all-length E/S and tight-Vcorner claims.
Let t_old be the uncertified remainder AFTER those tight claims have
already been removed. Let kappa count its actual a=h-6 claims. They
are disjoint demand classes by the gate class and actual Vcorner role
and length at the uniquely normalized y. Put

    q=q_old+kappa, t=t_old-kappa.

The simultaneous two-target injection proves the stronger inequality

    q+kappa<=Aactivation.                         (2)

Use the SAME full-family inventory, with no new tile or receipt pool:

    G=q+c+s+t<=2(N-n0), s<=p,
    2R>=Aactivation+m8+c+2p+2u,
    mu=N+R-G.

Substitution, retaining the extra activation in (2), yields

    2mu>=2n0+2u+2p+m8-s-t+kappa
        =2n0+2u+2p+m8-s-t_old+2kappa,
    mu>=n0+u+p+kappa+ceil((m8-s-t_old)/2).         (3)

The certified INTEGER lower bound thus increases by EXACTLY kappa
relative to the same prior ledger. This is an improvement in the
certificate, not a change to the actual margin of a fixed configuration.
The sufficient allocation threshold becomes

    s+t_old<=2n0+2u+2p+m8+1+2kappa.               (4)

We assign one of the two activations to the claim and leave the other
in Aactivation-q. We do not spend either activation again as a cap,
pair, m8 receipt or unused-terminal bonus. In particular both target
tiles are full; no extra defect is asserted at them. The already
established simultaneous inventory is the only source of the 2R bound.

The existing sigma>=mu implication gives coefficient1 instead of5/6
on complete configurations certified by (4), a gain |M|/6 there. This
does not improve the universal5/6 bound. Cases a<=h-8, other H,
occupied corridors, vertical exits, universal residual coverage and
the arbitrary-grid source decomposition remain open.

There is a concrete reason not to extrapolate the boundary-role proof:
at h=18,a=10 (gap8), the endpoint-disjoint PARTIAL sources C=U(18,18,8),
X=U(6,10,4) and E=U(6,4,4) with E(r,c)=(c+2,18-r) place an EAST
terminal at the forced endcap (3,14). Its incident leg ends at column18,
before C's bar at19. This finite control identifies a surviving role for
the next investigation; it is not a complete-extension witness and does
not refute double activation or allocation in complete gap8 families.

## 6. Verification scope

Finite endpoint/support/sign and collision controls supplement this
all-dimensional argument; they do not establish complete realizability.
All24 scoped declarations in
[NearTightVcornerDoubleActivation.lean](../formal/SubQuorum/NearTightVcornerDoubleActivation.lean)
pass local Lean4.33.0 and individual axiom checks, finalsession43824exit0.
The preflight found58% free memory and no real lean/lake process by comm
basename. Only ordinary propext/Classical.choice/Quot.sound occur, with no
sorry/native reduction. The first compilation85949 failed on Decidable
synthesis for the rotor predicate; explicit simp unfolding repaired it.
The accepted final run includes the additional first-leg lower-bound lemma.
See [the formal receipt](../output/near-tight-vcorner-formal-check.json).

The independent checker passes23,040 anchored U boundary roles,1,266
surviving leftward-terminal roles,32 forced-support stencils, all four
adjacent south-rotor collisions and both rotor/terminal orders,364
endpoint-disjoint five-source PARTIAL chains,48 old-target collision and
self-exclusion controls for EACH of S/P/E/S, and1,701 integer/parity
controls. A separate partial control permits the actual middle owner D=B
and verifies the same original endpoints, supports AND matching after
leg reindexing. No complete realization is claimed from these patterns.
See [the control receipt](../output/near-tight-vcorner-controls.json).

Complete source-role exhaustion, physical sign classification and global
labelled reconstruction remain written. Initial separate written review
8bc943f3, conversation conv_4f144ec01fe42cda, originalstream64145exit0,
returns REVISE while confirming forcing, dimensions, signs, two activations
and ledger. It requests the owner-distinctness correction, an explicit
consumer-owner exclusion in the boundary lemma, exact E/S dependency
frames and the corrected physical P collision notation. These are now
incorporated. The D=B correction was already made locally before the
response arrived, and its partial control verifies matching as well as
endpoints/supports. The review's full18,006-character response is archived;
it does not certify execution, complete witnesses or the full target.
Follow-up49d08e51, originalstream50405, reviews all four repairs and the
actual all-length dependency in the same conversation and ACCEPTS. Its
12,742-character response matches the terminal API and original SSE
exactly, with [DONE], exit0 and observed gpt_6/pro. It accepts the two
globally unused activation targets, dimension obstructions, exact integer
gain and threshold under the stated dependencies. There is no circular
dependency on the retrospective link in the all-length note: only its
already established exact frames and joint injection are used. It does
not certify code/Lean execution, complete realizability, the later gap8
partial lead, universal residual coverage or unrestricted allocation.
See the [initial review](../output/near-tight-vcorner-review-response.md),
[accepted repair](../output/near-tight-vcorner-repair-response.md) and
[final receipt](../output/near-tight-vcorner-repair-review.json).

A subsequent [gap-eight adjacent-band note](GAP_EIGHT_ADJACENT_BAND_EXITS.md)
proves further endpoint consumption in the east-terminal branch, including
simultaneous consumption of two adjacent supports at a matched return.
That propagation result has its own written/finite-control scope; the reviews
above do not cover it, and it adds no activation or reserve to this ledger.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
