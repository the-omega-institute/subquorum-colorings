# Directional averaging compensates arbitrary intersections of prescribed sources

19 October 2026. The coefficient-one bound below places no restriction on
the number of source mouths, their crossings or their intersection graph.
It follows from the perpendicular-source phase lemma and the physical fact
that coalesced horizontal/vertical strips have multiplicity at most two.

## 1. Exact hypotheses

Work in an even-by-even physical rectangle with mn vertices and a feasible
initial pair (T_0,M_0). The endpoint set P_0 is that of the actual matching;
T_0 is disjoint from P_0, and each selected vertex has at most one neighbor
in T_0 union P_0. The physical tiles start at even row and column coordinates.

Prescribe B distinct complete endpoint components that are positive long
sources: the two-row even-width chamber, two equal odd arms, actual matching
and selected supports in
`LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`, Section 1. Width is at
least eight and depth at least one. Use any translations, reflections or
transpositions that preserve the positive alignment of that definition.
Each whole source receiver has corrected charge one and all its endpoints
are universally frozen.

Each other complete initial endpoint component is thin (contained in two
consecutive rows or columns), contains at most one P-square, or is a prescribed
complete straight contact comb with its consecutive matching, alternating
side supports and both axial supports. Require every endpoint in any source
mouth to belong to a prescribed source or contact comb. Unlike the previous
contact theorems, there is no direction restriction on such contacts.

Normalize as in `COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`. Frozen source
and comb data and all mouth labels persist, the objective is unchanged, and
every other final receiver has nonpositive corrected charge. All subsequent
counts refer to this single-terminal representative. The theorem does not
assert that every positive bent component is a prescribed long source.

## 2. The established strip input

Coalesce overlapping/adjacent parallel mouths in each physical band into C
strips G_i. Their union is G. Within each direction the strips are disjoint;
between the two directions a physical tile has at most one owner of each
direction. Thus every tile of G has multiplicity one or two.

Use the strip identity and exact parallel-tip conservation proved in
`ORTHOGONAL_SOURCE_MOUTHS_AND_CROSSING_LOSS.md`, Sections 2 and 3:

    D_i=2+L_i+U_i-S_i+A_i+D'_i,
    sum_i L_i=2B-2C,      A_i,D'_i>=0.                (1)

Here D_i counts actual physical no-P deficits in the strip. L_i counts
terminal tips parallel to that strip. S_i,U_i count physical sparse and
saturated comb ends with their strip membership. A_i is the nonnegative
perpendicular-source phase gain, accounting for optional flank/cap selections;
D'_i is the auxiliary shifted no-P deficit. A_i is a counting correction,
and shifted squares do not introduce new physical donors.

Let F=sum_i(U_i-S_i), A=sum_i A_i and D'=sum_i D'_i. Summing (1) gives

    sum_i D_i=2B+F+A+D'.                              (2)

The quantity F uses strip multiplicities, not membership only in G. A complete
comb has at most one sparse and one saturated physical singleton end. Its
contribution is m_saturated-m_sparse with each multiplicity in {0,1,2}.

## 3. General directional averaging theorem

For every no-P physical tile Q in G let d_Q=2-t_Q>=0. Split these tiles into
those covered once and those covered twice, with total deficits D_1,D_2.
Both are actual disjoint physical tile sets. Then

    sum_i D_i=D_1+2D_2,
    D_G=D_1+D_2,
    2D_G=sum_i D_i+D_1.                              (3)

Let R>=0 be the total physical no-P deficit outside G plus the deficits
of nonprescribed final receivers. Complete comb receivers have charge zero;
each source whole receiver has charge one. The original corrected ledger is

    Delta=mn/2-|T_0|-|M_0|=-B+D_G+R.

Substituting (2),(3) proves the exact identity

    2Delta=F+A+D'+D_1+2R.                            (4)

**Directional averaging theorem.** Under the hypotheses in Section 1,
F>=0 implies |T_0|+|M_0|<=mn/2, for every number and orientation of prescribed
sources and every mouth-intersection pattern.

Proof. A,D',D_1,R are nonnegative, so (4) gives Delta>=0. QED.

The sufficient end condition m_saturated>=m_sparse for each complete comb
implies F>=0, but only the aggregate inequality is needed. Union closure
O=0 does not by itself imply this condition: a sparse end may occur in two
strips and its saturated end in only one. No such inference is used.

## 4. Unrestricted source-only mouths

**Source-only compensation theorem.** Retain all Section 1 hypotheses and
require every endpoint in G to belong to a prescribed source. Then

    |T_0|+|M_0|<=mn/2.

There is no restriction on the number, orientation or crossing pattern of
the sources. Complete combs outside G and the other allowed outside endpoint
components remain permitted.

Proof. No comb end contributes to any strip, so F=0. Apply (4). QED.

This removes the entire matching loss in the universal bound
|T_0|+(5/6)|M_0|<=mn/2 for the stated source-only class. The earlier crossing
criterion 2X+O<=B+J is unnecessary here, even if X is much larger than B.

There is also a direct allocation interpretation. Give each strip half of
its physical no-P deficit. A physical donor used by one strip supplies one
half; one used by two supplies two halves. Total usage never exceeds the
actual physical deficit. Equation (2) then supplies at least B in aggregate
when F>=0, covering the B complete source charges. The proof never allocates
a source tip, a partial arm receiver or a shifted square as a second donor.

The crossing-loss identity and (4) are two descriptions of the same physical
ledger. Their estimates may be compared, but their supposed resources may
not be added. Equation (4) is valid even when F<0; controlling that negative
comb flux against its other terms remains a separate question.

## 5. Verification and precise scope

The current controls are in `output/directional-averaging-controls.json`.
They check the exact incidence identity (3), doubled ledger (4), donor
multiplicity, frozen source data and the original physical ledger. Dense
crossing controls include ten sources with 25 crossing tiles, outside the
coarse 2X<=B regime. These are finite checks of the general proof, not its
logical basis. The explicit all-width three-unit union obstacle to the old
four-unit local rule is retained and does not contradict this theorem.

The local Lean 4.33.0 audit in `output/directional-averaging-formal-check.json`
passes 97 scoped declarations. Two new declarations in
`formal/SubQuorum/OrthogonalMouthFlux.lean` prove (3) for arbitrary finite lists
of nonnegative donor weights and crossing flags, and the conditional averaging
identity/objective consequence from the three ledger equalities. The earlier
five local crossing/phase declarations retain their scopes. Geometric
classification, coalesced tip cardinality, normalization and the source-only
theorem as a complete graph statement remain written proofs.

The earlier independent review d54c5a35 accepted the strip identities,
crossing-loss theorem and all-width obstacle. Its input predates directional
averaging. A separate follow-up in conv_d54fcca063697f6b reviews this exact
deduction; no inherited verdict is asserted.

Reproduce with:

```sh
python3 develop/check_orthogonal_source_mouths.py --output output/directional-averaging-controls.json
python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0 --output output/directional-averaging-formal-check.json
```

Arbitrary positive bent components outside the prescribed source family,
negative multiplicity-weighted comb flux, the universal grid bound and
the proposed grid triple equality remain open.
