# Gap-eight occupied bands: two jointly unused positive-terminal channels

21 October 2026. At every unsaturated band width omega<=V-4, two specified
positive terminal roles transfer actual gap-eight claims to jointly unused
activations. Section5 combines both roles and all widths in one injection;
Sections1-4 first prove the tight-band subcase and classify its negative
continuation. The theorem is conditional on the actual consumer role. It does
not resolve all gap-eight configurations, unrestricted allocation, or
rectangular-grid equality.

The later [nonmatched successor theorem](GAP_EIGHT_NONMATCHED_SUCCESSOR_TRANSFER.md)
adds the positive up successor when f!=j+2, jointly with the entire D/L union.
The [maximal-band obstruction](MAXIMAL_VCORNER_BAND_OBSTRUCTION.md) excludes
d=b-2,k>=W-4, including the displayed matched-return partial seed.

The subsequent [old-pair return identity](GAP_EIGHT_SUCCESSOR_OLD_PAIR_RETURN.md)
proves that the tight negative branch's positive successor can reuse an old P
target only when f=j+2. This is not yet a new global compensation certificate.

## 1. Complete-source hypotheses and the two-role reduction

Use exactly the finite complete original U/rotor model, fixed aligned physical
tiles and actual labelled marked-side claims in
[the near-tight theorem](NEAR_TIGHT_VCORNER_DOUBLE_ACTIVATION.md). In particular
endpoint ownership is unique and every original support remains occupied:
it is an endpoint when consumed, and otherwise selected with only its original
anchor as occupied neighbor. N counts positive owners only. All widths are
even>=6, and both independently chosen leg lengths are even>=4.

Normalize an actual negative-Vcorner demand by

    A=U(w,L,K), A(r,c)=(r,c),
    B=U(W,b,e), B(r,c)=(b+3-r,c+1),
    C=U(V,h,f), C(r,c)=(c+1,h+2-r),
    X=U(d,h-8,k), X(r,c)=(c+2,r+3),
    b>=6, h>=12, h<=w-4, d<=b-2.

Condition on the actual consumer of X's forced endcap (3,h-4) being an
east-pointing U terminal. The preceding
[adjacent-band lemma](GAP_EIGHT_ADJACENT_BAND_EXITS.md) gives

    E=U(omega,4,nu), E(r,c)=(c+2,h-r), omega<=V-2.

Our new hypothesis is omega=V-4. In particular V>=10. Put

    y=(V-1,h), z=(V,h).

**Role reduction.** The actual consumer of y is necessarily one of

    D=U(s,g,t), D(r,c)=(c+V-2,r+h-g),       positive, g>=f;
    U=U(s,g,t), U(r,c)=(V-c,r+h-g),         negative, g>=nu+2.

The letters D and U name downward- and upward-bar terminal roles, not new
resource pools. The width s and the other leg t are independent. These are
necessary forms only; no complete occurrence is asserted.

**Proof.** y is E's original bar-end support. Its north neighbor
(V-2,h)=E(0,omega) and east neighbor (V-1,h+1)=C(1,V-2) are occupied.
Neither E nor C owns y, so its actual consumer differs from both. It can
have own neighbors only west/south. A U endpoint with a south own neighbor
continues at least two steps south, whether it is a terminal or either
outer corner; it would meet C at (V+1,h). Straight nonterminal points and
degree-three points cannot have their own neighbors confined to west/south.
Thus any U consumer is a west terminal.

There are four rotor-tip footprints with only a west or south own neighbor.
The two west forms contain respectively (-1,-2) and (-1,-1), relative to y;
these are E far-leg endpoints since nu>=4. The two south forms contain
(2,0), a C far-leg endpoint since f>=4. All rotors are excluded. This uses
the fixed sources only, so arbitrary additional sources cannot remove a
blocker. A consumer at y cannot be either blocker owner, as y is in neither
of their endpoint sets.

For a west terminal with incident length g, its bar columns are h-g and
h-g+1. If the bar points down, it crosses row V+1. A length g<=f-2
would meet C's far leg at (V+1,h-g+1), so g>=f. Its frame is D.
If the bar points up, it crosses row V-2. A length g<=nu would meet
E's far leg at (V-2,h-g+1), so evenness gives g>=nu+2 and the frame U.
The physical phases give charge +1 for D and -1 for U, independently of
s,g,t. In the D case the axial support east of y is C-owned, and its
lateral support north of y is E-owned, so its terminal is actually activated.

## 2. The D targets inject jointly with all earlier targets

Let K_D be the actual labelled claims satisfying Section1 whose actual y
consumer is D. Assign each claim its original D terminal occurrence at y.
This is one activation, even though both original terminal supports are
consumed. Its two support owners C,E are distinct U owners.

**Reconstruction.** From the terminal occurrence and its ordered original
supports, the lateral support identifies E's outer far bar corner
E(0,omega). The original E source, this bar end and its direction determine
the opposite incident leg, of length four, and its terminal x=(3,h-4).
The source at the west neighbor (3,h-5) is the actual X terminal. Its actual
leg and source determine X's outer corner (3,3), fixing the original
normalization. At (3,2) the actual owner is B; its own neighbor (4,2) is
also B-owned. Of the two possible external positive producer anchors at
B's terminal, only (3,1) remains. Endpoint uniqueness and the established
canonical-gate reconstruction recover the original positive labelled side.
Hence two claims cannot receive the same D occurrence. Source roles and
ordered supports, rather than guessed new owner identities, are used here.

We must also exclude every OLD target in the SAME complete family. Name the
actual target incident leg g. The accepted old recipient frames, in their
own positive producer charts and after any incident-leg reindexing, are

    S_old(r,c)=(g+3-r,3-c), P_old(r,c)=(c+2,r+2),
    E_comp(r,c)=(c+2,g+3-r), S_comp(r,c)=(g+3-r,c+2).

The first two are the old S/P dependencies used in the tight and near-tight
theorems; the last two are the all-length E/S companion targets. Equating
one of these actual whole-source frames, transported by an old producer
chart F, to D forces the following F. All collisions are with C.

| Old channel | Forced producer F(r,c) | Old endpoint giving collision | A different old endpoint outside C |
|---|---|---|---|
| S | (V+1-c,h+3-r) | (1,1) -> (V,h+2) | (0,1) -> (V,h+3) |
| P | (r+V-4,c+h-g-2) | (0,g+3) -> (V-4,h+1) | (0,1) -> (V-4,h-g-1) |
| E companion | (r+V-4,h+3-c) | (0,1) -> (V-4,h+2) | (0,6) -> (V-4,h-3) |
| S companion | (c+V-4,h+3-r) | (1,1) -> (V-3,h+2) | (0,1) -> (V-3,h+3) |

The P endpoint exists because its old bound is w_old>=g+4. The other
endpoints exist at every permitted width. Since V>=10 and g>=4, the
outside-C points in the table are neither on C's bar nor either of its
legs. Therefore the hypothetical old positive producer cannot equal C.
Each collision is a genuine different-owner violation, not a self-owner
identification. These arguments do not bound the old producer's legs.

Old R targets have a rotor-owned original support, whereas D's supports
are both U-owned. Tight and near-tight Q2 targets have the SAME owner at
their two supports, whereas D has distinct C/E owners. Finally a near-tight
Q1 target has an outward axial support at its transverse owner's original
straight leg point (4,1), of original endpoint degree two. D's axial
support is C(1,V-2), of original endpoint degree three: V-2 is an internal
bar column because V>=10. A terminal's axial support is intrinsic, and
unique endpoint ownership prevents one point being both types of the same
original source. This excludes every near-tight Q1 target as well.

Thus all the previous targets, including BOTH near-tight targets, and all
new D targets form ONE simultaneous injection. Equal or recurring owners,
different endpoint components and a target described in another chart do
not give extra copies of an occurrence. The target tile is full; no new
cap, pair or m8 receipt is asserted there.

## 3. Exact effect in the existing ledger

Write the accepted old simultaneous activation certificate as

    Aactivation>=q_old+rho,

where rho>=0 retains the already proved extra activations, for example one
per near-tight double-activation claim. This is an IDENTIFIED old target set
with at least q_old+rho distinct occurrences, drawn from precisely the old
S/P/R, all-length E/S, tight and BOTH near-tight target families excluded
in Section2. A bare numerical lower bound or unnamed further target family
would not suffice. Let t_old be the uncertified demand
remainder AFTER those old classes have been removed. Put kappa=|K_D| and

    q=q_old+kappa, t=t_old-kappa.

The demand classes are disjoint by the actual Vcorner role and a=h-8,
as opposed to old gate/terminal/H classes or a=h-4,h-6. Thus kappa<=t_old,
and the total G is unchanged.

Section2 proves Aactivation>=q+rho with no change to rho. Use the SAME
physical family and existing inventory:

    G=q+c+s+t<=2(N-n0), s<=p,
    2R>=Aactivation+m8+c+2p+2u, mu=N+R-G.

Consequently

    2mu>=2n0+2u+2p+m8-s-t_old+kappa+rho,
    mu>=n0+u+p+ceil((m8-s-t_old+kappa+rho)/2).

The exact gain over the same old certificate is the difference between
this ceiling and ceil((m8-s-t_old+rho)/2); it can be zero for one new
claim. We do not claim the one-per-claim gain of the double-activation
theorem. The sufficient threshold is

    s+t_old<=2n0+2u+2p+m8+rho+kappa+1.

On configurations satisfying it the established sigma>=mu gives matching
coefficient one rather than5/6. No universal improvement is obtained.

## 4. The negative branch is not silently credited

If y is U instead, its mandatory lateral terminal support is z=(V,h).
This point has U north, C east and C south, so it must be consumed; only
an own west neighbor is possible. Both west rotor tips meet U's near leg
at relative offsets (-1,-2) or (-1,-1). Thus its actual consumer is another
west U terminal. Its two remaining possible forms are

    up:   U(tau,j,ell), (r,c)->(V+1-c,r+h-j), positive, j>=g+2;
    down: U(tau,j,ell), (r,c)->(c+V-1,r+h-j), negative, j>=f.

The up alternative's bar must pass strictly left of U's near stem; the
down alternative's bar must pass left of C's far leg. These give the
stated bounds by evenness. The up terminal is actually activated by two
C-owned supports, but Section2 does NOT assign it a new receipt: its
frame comparison with the old P channel need not produce the C collision
used for D. No claim of reuse or nonreuse in COMPLETE configurations is
made without that additional analysis. The down alternative remains open.
Neither branch is included in K_D or added to rho.

This is the baseline of the present note. The subsequent nonmatched successor
theorem credits the up branch under f!=j+2 in a separate simultaneous extension;
it does not include the down branch or matched f=j+2 cases.

Negative consumers at other omega values, the matched-return pair, other gap-eight consumer
roles, wider H, vertical exits, universal residual coverage and an arbitrary
grid decomposition remain open. This theorem does not assert a complete
Vcorner witness. Verification and separate review scopes are recorded with
the accompanying controls; a finite library cannot prove exhaustion at
arbitrary dimensions.

## 5. Extension to all unsaturated widths and both positive terminal roles

The new injection extends beyond the tight-band role exhaustion. Retain the
same actual A/B/C/X/E chain, but now allow ANY omega<=V-4. Put
y=(omega+3,h). This E bar-end support is forced as before. Condition on
its actual consumer having either of the following frames:

    D(r,c)=(c+omega+2,r+h-g),
    L(r,c)=(g+omega+3-r,h+1-c).

D is a west terminal with a downward bar; L is a south terminal with a
leftward bar. Both are positive, with independent width and far leg. Their
original supports at y are precisely

    north=(omega+2,h)=E(0,omega),
    east=(omega+3,h+1)=C(1,omega+2).

For D the east support is axial, while for L the north support is axial.
Both supports are consumed, so each case supplies ONE activation. No claim
is made that these exhaust actual consumers at larger gaps.

A south terminal at y necessarily has the L frame: its stem cannot meet
C's far leg at (V+1,h), so g<=V-omega-4; its bar then lies above C's
far leg and a rightward bar would meet C's bar. Consequently L requires
V-omega>=8. D need not obey g>=f unless its width reaches C's far-leg
row; this restriction from Section1 is not silently extended to arbitrary
omega. The general D injection below does not require it.

The lateral/axial support at E(0,omega) again reconstructs the opposite
E terminal, the actual X terminal and corner, B and the original positive
labelled side exactly as in Section2. This gives one injection on the
UNION of all D and L claims. A D target cannot equal an L target: its
axial support has original endpoint degree three, whereas the L axial
support has degree two and two perpendicular own neighbors.

Here are ALL eight old-channel comparisons; each hypothetical old producer
is F. The fourth column supplies a genuine original endpoint outside C,
excluding a self-owner interpretation of the collision in the third column.

| New / old | Forced F(r,c) | Old endpoint -> C collision | Old endpoint -> outside C |
|---|---|---|---|
| D / S | (omega+5-c,h+3-r) | (1,1) -> (omega+4,h+2) | (0,1) -> (omega+4,h+3) |
| D / P | (r+omega,c+h-g-2) | (0,g+3) -> (omega,h+1) | (0,1) -> (omega,h-g-1) |
| D / E | (r+omega,h+3-c) | (0,1) -> (omega,h+2) | (0,6) -> (omega,h-3) |
| D / S companion | (c+omega,h+3-r) | (1,1) -> (omega+1,h+2) | (0,1) -> (omega+1,h+3) |
| L / S | (r+omega,c+h-2) | (0,3) -> (omega,h+1) | (0,1) -> (omega,h-1) |
| L / P | (g+omega+5-c,h+3-r) | (1,g+3) -> (omega+2,h+2) | (0,g+3) -> (omega+2,h+3) |
| L / E | (c+omega,h+3-r) | (1,1) -> (omega+1,h+2) | (0,1) -> (omega+1,h+3) |
| L / S companion | (r+omega,h+3-c) | (0,1) -> (omega,h+2) | (0,6) -> (omega,h-3) |

Use omega>=6, omega<=V-4, g>=4 and the old P bound w_old>=g+4.
Every displayed C collision lies on its bar; every outside-C point lies
strictly between C's leg rows or in column h+3. All are original endpoints
of the old producer, at every permitted independent old leg length.

The R exclusion and distinct-versus-same support-owner exclusion for tight
and near-tight Q2 targets remain unchanged. A near-tight Q1 target has a
straight degree-two axial support, so it cannot be D's degree-three axial
support OR L's perpendicular degree-two axial support. Straight versus
perpendicular refers to the original owner's endpoint graph and is invariant
under all source/chart isometries. Thus the union of ALL new D/L targets is
jointly disjoint from ALL earlier targets, not merely separately injective
within each width or role. Use the same Section3 ledger with kappa counting
this entire new union, in place of only its tight-band D subfamily. No
extra activation or capacity pool is introduced.

The pre-gap-eight old target set in Section3 does NOT separately include the
Section1 tight-band D claims. Those claims are a subset of this enlarged
union, with exactly the same assigned targets. They are counted ONCE in
kappa. Relative to a ledger that already included them, only the additional
claims outside that tight-band subset may be newly added.

This extension was derived after the first tight-band audit packet was sent.
Its review and validation scope must be established separately; acceptance of
that earlier packet alone does not certify this extension.

## 6. Verification and review scope

All28 scoped declarations in
[TightGapEightBandCompensation.lean](../formal/SubQuorum/TightGapEightBandCompensation.lean)
pass standalone local Lean4.33.0 and individual axiom checks, finalsession26072
exit0. The user-selected local Mac had46% free memory and no actual lean/lake
process by comm basename before invocation. Only ordinary propext,
Classical.choice and Quot.sound occur, with no sorry/native reduction.
The formal scope includes arbitrary-width support/endpoint coordinates,
degree-three/straight/perpendicular neighbor stencils, incident-leg collision
bounds, old producer collision/self-exclusion coordinates, the abstract
adjacent-support consumption principle and the same physical ledger/threshold.
Source-role exhaustion, physical signs, affine source-frame derivations,
labelled reconstruction and GLOBAL joint injection remain written. Earlier
24923 passed20 declarations;55834 passed28 with an unused-binder warning,
which was removed before the clean final run. See
[the formal receipt](../output/tight-gap-eight-band-formal-check.json).

The independent checker passes23,328 anchored tight-band U roles,3,240
positive D roles,1,296 negative U roles and both successor alternatives;
four initial rotor exclusions and two successor exclusions;72 collision and
self-owner controls for EACH of the original four comparisons; and1,722
integer/parity controls. General-width controls add228 D and72 L PARTIAL
targets,288 south/right-bar exclusions, and288 collision/self-exclusion/frame
controls for EACH of all eight old-channel comparisons. A normalized six-source
A/B/C/X/E/D chain has disjoint endpoints and the claimed consumed supports;
it is PARTIAL only. See [the controls](../output/tight-gap-eight-band-controls.json).

Finite completion discovery of that seed is UNSAT in a36,137-candidate U-only
library, within rows[-8,32], columns[-8,30], added widths6..10, independent
legs4..8 and at most16 additions. This does NOT exclude arbitrary U/rotor
extensions, prove a general obstruction, or supply a complete witness. The
existing discovery tool now accepts an explicit seed and bounds and checks
that all fixed occupied points lie inside them. See
[the bounded discovery receipt](../output/tight-gap-eight-discovery.json).

Separate written review1769c22a, conversation conv_00c07da2ddad56a1,
originalstream39040exit0, ACCEPTS Sections1-4 of the initial tight-band packet:
role exhaustion, labelled reconstruction, every old-target exclusion including
the axial-degree Q1 test, the negative continuation's necessary roles, integer
gain and threshold. Its17,877-character response exactly matches terminal API
and original SSE with [DONE], observed gpt_6/pro. It does not certify execution,
complete realizability, the later general-width D/L extension or the full target.
Its identified-old-target-set clarification is explicit in Section3. See
[the initial review](../output/tight-gap-eight-band-review-response.md) and
[its receipt](../output/tight-gap-eight-band-review.json).

Separate follow-up review2dfcb73c ACCEPTS Section5, including all eight frame
comparisons, uniform reconstruction, the D/L union, perpendicular-versus-straight
Q1 exclusion, south-leg bound and the unchanged ledger. Its15,907-character
response exactly matches the terminal API and originalstream47470exit0 with
[DONE], observed gpt_6/pro. The old tight-band subset is expressly replaced,
not counted twice. This accepts the written general-width extension; it does
not certify execution, complete realizability, further consumer classes or the
unrestricted target. See [the follow-up response](../output/general-gap-eight-band-review-response.md)
and [receipt](../output/general-gap-eight-band-review.json).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
