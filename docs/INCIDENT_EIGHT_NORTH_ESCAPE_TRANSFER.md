# A short secondary north escape forces a jointly unused positive activation

21 October 2026. This continues the
[six-step obstruction](INCIDENT_SIX_NORTH_ESCAPE_OBSTRUCTION.md). An actual
eight-step north intrusion forces a negative six-step north terminal followed
by a positive east terminal. The same positive transfer holds for EVERY
incident length j>=8 whenever its secondary north terminal has length6. The positive
terminal gives one jointly unused activation for each eligible residual
labelled demand. All source dimensions and additional-source counts are
unrestricted. No complete marked Vcorner occurrence or unrestricted allocation
theorem is asserted.

## 1. Source model and a general secondary escape

Use the complete original U/rotor model: unique original endpoint ownership,
immutable original matching, and retention of every unconsumed original support
with its original anchor as sole occupied neighbor. Consuming a support preserves
occupancy. Optional selections have no endpoint neighbor. U widths are even>=6,
independent legs even>=4, and all rotor symmetries/chiralities are allowed.
Physical tiles remain the fixed aligned two-by-two tiles. N counts positive
owners only.

First prescribe only

    X=U(b-2,a,6), X(r,c)=(c+2,r+3),
    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    H=U(d,j,z), H(r,c)=(b-1-j+r,c+4),
    8<=j<=b-6, a,z>=4, d>=6, all dimensions legal even integers.

**Secondary escape lemma.** Every complete extension has an original owner

    D=U(m,ell,t), D(r,c)=(b-1-ell+r,c+5),
    6<=ell<=j-2.

D consumes s=(b-1,6), X's original far inner support, and differs from X,Q,H.
This is a necessary form, not an existence assertion or a fresh-owner rule for
unrelated sources.

**Proof.** X's anchor at (b,6) and H's endpoint (b-1,5) force s to be an
endpoint. None of X,Q,H owns s: X's far leg is on row b, Q's bar on columns
10,11 and its near leg on row b+1, while H has legs on columns5,d+4 and
its bar above s. Its own endpoint neighbors can therefore only be north/east.

For a U, degree-three points and straight interiors are excluded. An east
terminal continues at least four steps, and a vertical outer bar corner with
an east leg also continues at least four steps. Both hit Q at (b-1,10).
A horizontal outer bar corner extending east hits that same Q point because
its width is at least6. The only U possibility is a north terminal.
Both north rotor-tip forms contain (b-3,5), an H endpoint. Both east forms
contain (b,8), an X endpoint. Every rotor is excluded.

Write R=b-1-j for H's outer bar row and S=b-1-ell for the consumer's outer
bar row. If S<=R+1, its column6 stem crosses H's lower bar at (R+1,6).
Thus S>=R+2, using legal parity. A leftward bar would then contain (S,5),
an H near-leg endpoint, so the bar points right. The incident length4 puts
its lower bar on row b-4 and across Q's endpoint (b-4,7), impossible.
Hence ell>=6 and S>=R+2 gives ell<=j-2. This proves the lemma.

## 2. The short-secondary chain and an incident-eight width obstruction

Now impose j=8. The lemma forces ell=6, hence

    H=U(d,8,z), H(r,c)=(b-9+r,c+4),
    D=U(m,6,t), D(r,c)=(b-7+r,c+5).

Endpoint disjointness forces

    8<=m<=d-2.

Indeed m=6 puts D's far leg on column11 through Q's endpoint (b-4,11).
If m>=d, D's upper bar contains H's far endpoint (b-7,d+4), since z>=4.
Evenness gives the displayed upper bound. The upper bound m<=d-2 in this
paragraph uses j=8 and is not asserted for longer parent incident lengths.

For the following positive transfer, allow ANY j>=8 and suppose the actual
secondary length is ell=6. Its frame remains D(r,c)=(b-7+r,c+5). The same
Q collision excludes m=6, so m>=8 without a bound relating m and d.

Put q=(b-5,7), Q's original upper far support, intrinsic (4,7), anchored at
(b-4,7). It has three fixed endpoint neighbors:

    north=(b-6,7)=D(1,2),
    west =(b-5,6)=D(2,1),
    south=(b-4,7)=Q(4,6).

Thus q must be consumed. It belongs to none of X,Q,H,D before their endpoints
are used as blockers. The only allowed own endpoint neighbor is east. A U
consumer must therefore be an east terminal. Both east rotor tips contain
q+(-1,2)=(b-6,9), on D's lower bar, and are impossible.

Let g be the U's incident length and T=g+7 its outer bar column. Its horizontal
stem must stop before D's far endpoint (b-5,m+5). Since T and m+5 are odd,
g<=m-4. An upward bar crosses D at (b-6,T). For g=4, a downward bar also
hits Q at (b-4,10). Therefore the consumer is precisely

    E=U(omega,g,nu), E(r,c)=(b-6+c,g+7-r),
    6<=g<=m-4,

with independent legal width omega and far leg nu. In particular

    m>=10; if j=8, also d>=12.                         (1)

Thus the prescribed X/Q/H eight-step intrusion has no complete extension
at H widths6,8,10, for arbitrary b,a,z and unrestricted added sources.
This noncompletion creates no reserve or activation. More generally (1)
is a necessary condition, not a complete-extension claim.

E is positive in the fixed physical tiling: its reflected intrinsic row
coordinate lands in columns g+7-r with odd reflection constant, and its
intrinsic column coordinate lands in rows b-6+c with even offset. Its isolated
tile charge is +1, independently of omega,g,nu. H and D instead have charges
1-d and 1-m. Their appearance alone is never credited as a positive resource.

E's original terminal supports at q are exactly west and north in the table,
both consumed by D. Hence q is ONE actual positive activation, keyed by
(original E owner, incident terminal index). The full terminal tile consists
of E's terminal and three D endpoints. No pair, cap, m8 or second activation
is added there.

## 3. Actual labelled claims and injective reconstruction

For compensation, retain the actual A/B/C/X/Q chain of the
[opposed-stem theorem](OPPOSED_STEM_SUPPORT_GAP_OBSTRUCTION.md), with k=6,
W>=12, and an actual lower intrusion v=(b-1,5) whose original owner is H with
incident length j>=8, and suppose its actual secondary consumer D has
incident length6. When j=8 the latter condition is automatic. X is the actual negative Vcorner at (3,3), Q the actual
consumer of its bar-end support (b+1,3), and H the actual consumer of v.
All actual-source premises, including C's endpoint (2,5), remain in force.

The actual B fence strengthens (1). If omega=6, E's far stem lies on
row b. It meets Q's endpoint (b,11) whenever nu>=g-4. Endpoint disjointness
and parity therefore give nu<=g-6, and nu>=4 implies g>=10. If omega>=8,
E's vertical bar reaches row b+2. When g+7<=W+1 it meets B's bar there,
so disjointness and parity give g>=W-4. These collisions involve different
original owners: E owns q, which is absent from Q; q has B coordinates
(8,6), outside B's bar rows and both leg columns because W>=12. Thus E is
neither Q nor B, even when auxiliary owners recur. These are exhaustive alternatives:

    omega=6: 4<=nu<=g-6 and g>=10;
    omega>=8: g>=W-4.                              (3)

Thus every actual short-secondary chain has g>=8,m>=12. At W>=14
the stronger bounds are g>=10,m>=14. ONLY when j=8 does m<=d-2 also give
d>=14, strengthened to d>=16 at W>=14. These are necessary conditions,
not new activations or realizability assertions. In particular, WHEN j=8,
actual H width12 is impossible, although the three-source-only obstruction above
excludes only H widths<=10. B is essential to this stronger statement.

From E's original terminal occurrence, its ordered axial/lateral supports
identify D's first near-leg point (2,1) and adjacent lower-bar point (1,2).
They fix D's physical bar end and directed chart, and thus q's south neighbor.
The unique original owner of that neighbor is Q. It is Q's far terminal
(4,6); Q's whole original source fixes its opposite near terminal (b+1,3).
Its north neighbor (b,3) is X's adjacent original bar corner. X's original
bar and other end recover the actual Vcorner at (3,3), followed by the actual
B gate at (3,2). B also owns (4,2), leaving only (3,1) for the positive
producer anchor. Unique original ownership and canonical-gate uniqueness
recover the original positive labelled A side. This also fixes v=(b-1,5),
its unique original H owner and its physical incident leg, so a different
description using another j cannot create a second label for the same claim.

Thus equal E terminal occurrences recover equal actual labelled claims.
Equal original leg lengths do not exchange the physical bar end or ordered
support roles. No auxiliary owner is presumed new merely because it has a
new letter. Additional components do not provide copies of the same occurrence.

## 4. Joint nonreuse with the identified existing activation targets

Take the SAME precise old simultaneous target set: S/P/R, all-length E/S
companions, tight Vcorner targets, BOTH near-tight targets, the whole
unsaturated-band D/L union, and nonmatched positive upward successors. These
are the target families certified in the
[nonmatched successor theorem](GAP_EIGHT_NONMATCHED_SUCCESSOR_TRANSFER.md).
An unnamed numerical activation bound is not substituted for this set.

For old S/P compare whole-source recipient charts using the actual incident
length g. Their frames in their own positive producer charts are

    S_old(r,c)=(g+3-r,3-c), P_old(r,c)=(c+2,r+2).

Solving F composed with the old frame equals E gives

| Old channel | Forced old positive producer F(r,c) | First required endpoint | Second required endpoint |
|---|---|---|---|
| S | (b-3-c,r+4) | (0,1)->(b-4,4), X-owned | (1,1)->(b-4,5), H-owned |
| P | (b-8+r,g+9-c) | (0,g+3)->(b-8,6), outside D | (1,g+3)->(b-7,6), D-owned |

Both endpoints in each row exist: the old P bound is w_old>=g+4; S needs
only width>=6. For S, the two fixed owners X and H are distinct: its second
witness is H(j-3,1), valid for every j>=8. For P, ownership at the second
witness forces the hypothetical producer to be D, while its first witness
lies one row above D's outer bar and is not D-owned. This excludes P even
when that first point is not H-owned, as can happen for j>8. Both arguments
exclude every self-owner identification without an independent freshness premise.

Old R targets have a rotor-owned support, whereas both new supports are U-owned.
All-length E/S companions, near-tight Q1, and all unsaturated D/L targets have
DISTINCT owners at their two supports; the new target has D at both.

Tight and near-tight Q2 targets also have one owner at both supports, with
ordered owner roles (2,1) at the axial support and (1,2) at the lateral support.
Thus equality would identify that old transverse source and its physical near
leg with D. That incident leg has length6. Tight targets require h_old>=8,
and near-tight Q2 targets require h_old>=10. Both are impossible, even after
exchanging intrinsic leg labels: the ordered physical bar end identifies the
leg whose length is being compared.

Finally, nonmatched positive upward-successor targets have original axial
support C(1,V-1) of degree3 in its owner's original endpoint graph, V>=10.
Our axial support is D(2,1), of original degree2 on a straight leg. Unique
ownership forbids these two original profiles at the same axial support.
Ambient degrees are not used.

This proves one simultaneous injection on the old target set together with
the new actual claims. No separate component, channel or parity pool is made.

## 5. Exact same-ledger effect

Let q0+rho be a lower bound witnessed by the identified old activation targets,
retaining all already certified extra activations in rho. Let t0 be the
remaining labelled demand set AFTER all those activation, cap and certified
pair classes are removed. Choose the new short-secondary class only inside that
residual set, across all j>=8, and put kappa equal to its cardinality. The j=8
subclass belongs to this union once, not as a second demand class. Then

    q=q0+kappa, t=t0-kappa, 0<=kappa<=t0,
    Aactivation>=q+rho.

Keep the SAME total G, physical pair union P, p=|P|, and inventory:

    G=q+c+s+t<=2(N-n0), s<=p,
    2R>=Aactivation+m8+c+2p+2u, mu=N+R-G.

Consequently

    mu>=n0+u+p+ceil((m8-s-t0+kappa+rho)/2).          (2)

Relative to the old certificate, set H0=m8-s-t0+rho. The exact gain in (2)
is ceil((H0+kappa)/2)-ceil(H0/2). One new claim can gain zero or one by parity;
every two new claims gain exactly one. A sufficient coefficient-one threshold
is

    s+t0<=2n0+2u+2p+m8+rho+kappa+1.

With the established sigma>=mu reduction, configurations meeting this threshold
have matching coefficient1 rather than5/6. No universal bound improvement,
complete marked-chain example or full rectangular-grid equality is claimed.
The new E tile does not also contribute pair or cap capacity. Demands already
covered elsewhere are not counted again in kappa, nor is kappa added to rho.
If the incident-eight-only subclass with kappa8 claims has already been
included in the baseline certificate, enlarging it to this union adds only
kappa-kappa8 new claims; kappa8 is not credited again.

## 6. Verification and remaining scope

The argument is general; finite controls only check coordinates and role claims.
- [Independent controls](../develop/check_incident_eight_north_transfer.py):
  36 secondary patterns with1744 surviving U roles;264 short-secondary
  patterns across parent lengths8/10/12 with17880 surviving positive U roles;
  all bounded endpoint anchors and rotor directions checked, with96 width-eight
  no-consumer controls. The72 fixed-source-intersecting parameter sets are
  excluded explicitly. There are630 old-frame compositions,1377 ceiling
  controls, and576 actual-B fence patterns with60 disjoint PARTIAL roles.
  These are not complete marked-chain examples.
  [Output](../output/incident-eight-north-transfer-controls.json).
- [Lean source](../formal/SubQuorum/IncidentEightNorthTransfer.lean):39 scoped
  declarations pass Lean4.33.0, final local execution45758 exit0 with no
  warnings. Each declaration has an individual axiom audit; only propext,
  Classical.choice and Quot.sound occur, without sorry or native computation.
  Coordinates, necessary collision bounds, support-degree profiles, all-j S/P
  ownership witnesses and the integer ledger are formal. Complete catalogue
  role/orientation adapters, charge phase, actual labelled reconstruction,
  and simultaneous global injection remain written proofs.
  [Scope receipt](../output/incident-eight-north-transfer-formal-check.json).
- Initial independent written audit978dd41f **ACCEPTS** the j8 theorem and
  simultaneous ledger consequence. The13553-character answer equals the
  completed task response exactly; original stream71752 exits0 with DONE/no
  errors, observed gpt_6/pro. This audit preceded the all-j short-secondary
  extension and B fence additions, which are reviewed separately in the
  same conversation. The review does not certify execution or novelty.
  [Receipt](../output/incident-eight-north-transfer-review.json) and
  [full response](../output/incident-eight-north-transfer-review-response.md).
- Follow-up written audite40dcc6f **ACCEPTS** the all-j, actual-ell6
  transfer, joint nonreuse, actual B fence and unchanged ledger. Original
  stream42073 exits0 with DONE/no errors; the answer equals the completed
  task response exactly, observed gpt_6/pro. The suggested explicit j8-only
  scope of the H width12 exclusion and the incremental kappa-kappa8 baseline
  distinction are incorporated above. No complete realizability or global
  allocation theorem is certified.
  [Receipt](../output/short-secondary-transfer-followup-review.json) and
  [full response](../output/short-secondary-transfer-followup-review-response.md).

Secondary lengths ell>=8, complete actual-chain realizability,
other return widths, nonmaximal corners, occupied adjacent bands and the full
allocation/grid target remain OPEN. Submitted DMGT and primary star-forming
results are preserved. This research turn has no mail or draft action.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
