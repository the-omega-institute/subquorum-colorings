# A maximal vertical-corner band cannot close with a long far leg

21 October 2026. This is a general two-source noncompletion theorem in the
finite complete original U/rotor model. It excludes the matched eight-source
partial pattern previously used to test old-P reuse, by an arbitrary-dimension
argument independent of the bounded search. It does not exclude every
matched return or refute the allocation inequality.

## Theorem

Suppose two original sources have disjoint endpoint sets and frames

    B=U(W,b,e), B(r,c)=(b+3-r,c+1),
    X=U(b-2,a,k), X(r,c)=(c+2,r+3),

where widths and legs are even, b>=8, W>=6 and a,e,k>=4. If k>=W-4,
there is NO complete extension by any finite number of original U/rotor
sources of arbitrary dimensions. Original endpoints, matchings and every
unconsumed original support must remain occupied as usual.

Consequently every complete actual Vcorner occurrence with maximal width
d=b-2 necessarily has

    k<=W-6 and W>=10.

There is no condition on X's near leg a, on the auxiliary source C, or on
the phase of additional sources. Prescribed endpoint disjointness is part
of the hypothesis, not something inferred from the dimension inequalities.

Endpoint disjointness alone already gives k<=W-4: for k>=W-2, X's far
stem hits B(3,W)=(b,W+1). The new theorem excludes the remaining boundary
k=W-4. This boundary is not empty as a partial-source hypothesis: for every
even b,W>=8, B=U(W,b,4) and X=U(b-2,4,W-4) in these frames have disjoint
endpoints, but the theorem rules out every complete extension.

## Proof

The original outer-bar support of X

    q=X(0,b-1)=(b+1,3)

has three occupied endpoint neighbors:

    north=(b,3)=X(0,b-2),
    west=(b+1,2)=B(2,1),
    south=(b+2,3)=B(1,2).

Neither B nor X owns q as an endpoint. Completeness therefore forces a
foreign endpoint owner at q. Since three neighbors are already owned by
the fixed sources, its own endpoint neighbors can only be east. Original
endpoint graphs have no isolated endpoints, so its sole own neighbor is
east. In a U source this is a terminal; in a rotor it is one of two tips.

Consider a U terminal, naming its incident leg g and width s. Its stem
contains every point in row b+1 from column3 through column g+3.
B owns (b+1,W+1)=B(2,W), independently of e>=4. If g>=W-2 the stem
hits that point. Evenness thus gives g<=W-4.

The two possible bar frames are

    down: (r,c)->(b+c,g+3-r),
    up:   (r,c)->(b+2-c,g+3-r).

For down, the bar includes (b+2,g+3), its intrinsic (0,2), which is
B(1,g+2). This exists since 4<=g<=W-4. For up, the same intrinsic
endpoint is (b,g+3)=X(g,b-2). It exists since g<=W-4<=k. Both orientations
therefore collide with a fixed source distinct from the consumer. The
other leg length and width s never enter the argument.

For rotors, the two distinct east-pointing tip footprints, relative to q,
are

    {(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)},
    {(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)}.

The first contains (-1,1), mapping to (b,4)=X(1,b-2). The second
contains (1,1), mapping to (b+2,4)=B(1,3). Both collide. This exhausts
all possible original endpoint roles at q; no consumer exists. Added
sources cannot erase these original endpoints, proving noncompletion.

Finally k<W-4 and evenness give k<=W-6; k>=4 then gives W>=10.

## Effect on the matched partial pattern

The eight-source pattern in
[the return-identity note](GAP_EIGHT_SUCCESSOR_OLD_PAIR_RETURN.md) has
B=U(8,8,4), X=U(6,10,4). Thus d=b-2 and k=W-4=4. Its mandatory support
q=(9,3) has no possible consumer, by the theorem above. This proves that
this PARTICULAR matched pattern has no arbitrary U/rotor complete extension.
The previously checked local old-P stencil and exact C=Cprime identification
remain valid; they did not imply complete realizability.

The earlier matched-pattern bounded run used34,210 U/rotor candidates in
[-8,32]x[-8,30], added widths6..10, legs4..8, at most24 additions, and
returned UNSAT. That finite result motivated inspection of q. The theorem
is proved by the independent role and collision argument above, without a
bound on added source sizes. It is not an extrapolation of finite UNSAT.

Matched f=j+2 configurations with d<=b-4, or maximal d=b-2 but k<=W-6,
remain unresolved. Impossible claims contribute zero to the demand count;
they do not create a compensating reserve or an extra activation receipt.

## Validation scope

The independent checker `develop/check_maximal_vcorner_band_obstruction.py`
checks endpoint/support coordinates, terminal and rotor footprints, and the
actual eight-source obstruction. Scoped Lean declarations check the fixed
three-neighbor pattern, stem/bar collision coordinates and evenness bound.
The catalogue exhaustion and complete-family implication remain written.
Review status and actual execution results are recorded separately.

All8 scoped declarations in `formal/SubQuorum/MaximalVcornerBandObstruction.lean`
pass standalone Lean4.33.0 with individual axiom checks, finalsession87367
exit0. The selected local Mac had38% free memory and no actual lean/lake
process by comm basename. Only ordinary propext, Classical.choice and
Quot.sound occur. Independent controls pass46 disjoint fixed pairs,4048
terminal collisions,92 rotor collisions and256 boundary partial pairs.

Separate written auditf337734b ACCEPTS the all-dimension noncompletion proof,
including the matched seed, role exhaustion, same-owner exclusions and parity.
Its9944-character response exactly matches originalstream80661exit0 and the
terminal API, with [DONE], observed gpt_6/pro. It certifies the written proof,
not execution or other matched cases. See [the response](../output/maximal-vcorner-band-review-response.md),
[receipt](../output/maximal-vcorner-band-review.json) and
[formal receipt](../output/maximal-vcorner-band-formal-check.json).

The bounded discovery script now optionally includes rotors and independently
rebuilds SAT outputs to check original endpoints/matching, every retained
support's occupied degree1, and endpoint degree>=3. It passes direct SAT
regressions on the known complete11-U family (278endpoints,139matching,
62selected) and a standalone rotor (8endpoints,4matching,8selected).
This validates both decoding paths, not arbitrary completeness of a search.
Result files are `output/completion-verifier-U-fixture-result.json` and
`output/completion-verifier-rotor-fixture-result.json`.

A second matched partial seed with W10,k4 satisfies the necessary k<=W-6
bound and avoids this obstruction. A51096-candidate U/rotor bounded run
within[-8,34]x[-8,34], widths6..10, legs4..8, at most32 additions is
also UNSAT. No general noncompletion is inferred for that seed. See
`output/matched-successor-wide-return-discovery.json`.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
