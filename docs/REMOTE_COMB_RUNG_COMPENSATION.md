# Remote transverse strips compensate negative comb flux

19 October 2026. This note proves a nonlocal compensation lemma for the
prescribed-source class, including configurations whose original mouths
have zero physical deficit. It permits unequal comb lengths and identifies
the exact physical capacity available when remote strips overlap mouths
or one another. It does not assume that every configuration has the required
endpoint-free transverse strips.

The candidate mechanism was obtained in the completed Oracle research task
f8af741f-8551-49e5-a249-db603145f9ea and is developed here with explicit
proofs, independent physical controls and scoped formal checks. That task
is a mathematical proposal, not an independent ACCEPT review of this note.

## 1. The retained ledger and one-unit comb debt

Retain the exact hypotheses and fixed terminal representative of
`DIRECTIONAL_AVERAGING_SOURCE_COMPENSATION.md`. In particular the prescribed
sources and complete contact combs have their actual matching and selected
supports; the outside coverage/normalization hypotheses still apply. Write

    Delta=mn/2-|T_0|-|M_0|,
    2Delta=F+A+Dprime+Dsingle+2R,                     (1)

where A,Dprime,Dsingle,R are nonnegative. Here F is the complete-comb
saturated-minus-sparse end incidence with strip multiplicity, and R includes
original physical no-P deficit outside the mouth union G together with
nonpositive outside-receiver slack. Delta is an integer.

**Flux lemma.** Each complete comb contributes f_C in {-1,0,1}, even if
an end has strip multiplicity two.

Proof. If a parallel strip contains one end, the complete straight endpoint
path lies in it: otherwise that path would cross a forced-blank extreme
column or row. Thus both end tiles have the same parallel membership.
Parallel memberships cancel in f_C. Perpendicular strips are disjoint,
so each end has perpendicular membership zero or one. Their difference
is -1,0 or 1. A comb without physical singleton ends contributes zero. QED.

Consequently F=N_positive-N_negative, where these counts concern nonzero
comb contributions. Equation (1) also gives the useful unconditional
consequence within this retained class:

    F>=-1 implies Delta>=0.                          (2)

Indeed 2Delta>=-1 and Delta is integral. Thus a failure of the coefficient-one
bound in this class would require F<=-2. In particular the single negative
comb stars in the preceding exclusive-strip note already obey (2); their
explicit physical allocation remains useful, but is not needed for this
weaker objective conclusion.

## 2. Exact deficit of a trimmed physical strip

Let Q={s,s+1} x {alpha,...,beta}, with s,alpha even and beta odd, contain
no endpoints. Let n be its number of physical tiles, t its selected count
and tau the selected count in its two extreme columns. Remove those columns
and partition the remaining vertices into squares shifted one column.
There are n-1 shifted squares and t-tau selected vertices. Thus

    D_Q=2n-t,
    Dprime_Q=2(n-1)-(t-tau),
    D_Q=2-tau+Dprime_Q>=2-tau.                        (3)

Each shifted square has at most two selected vertices by feasibility.
D_Q is the sum of original physical deficits; shifted squares only count
the same selections and introduce no new physical resource.

## 3. Remote-rung lemma, including unequal terminal heights

After a common physical-tile-preserving reflection or transposition, let
two prescribed complete comb endpoint paths be

    P_L={u_L,...,s_L} x {a},
    P_R={u_R,...,s_R} x {b}.

Assume a is odd, b even, b-a>=5, both u's are odd, both s's even, and
max(u_L,u_R)<=min(s_L,s_R). Each top singleton is sparse and bottom
singleton saturated. The corresponding required side supports face inward
on odd endpoint rows and outward on even rows: left at a+1/a-1 and right
at b-1/b+1. Include both axial supports, as in the prescribed comb definition.

Put s=min(s_L,s_R) and define the aligned physical transverse strip

    Q={s,s+1} x {a+1,...,b-1}.                        (4)

If Q is endpoint-free, its original physical deficit satisfies

    D_Q>=2 if s_L=s_R,
    D_Q>=1 if s_L!=s_R.                              (5)

There is no bound on comb lengths or on distance from sparse ends to Q.

Proof. Suppose the left comb terminates at s. Its retained inside support
(s-1,a+1) sees endpoint (s-1,a), forcing (s,a+1) blank. Its axial support
(s+1,a) sees endpoint (s,a), forcing (s+1,a+1) blank. The preceding support
exists even at length two, since the odd start satisfies u_L<=s-1.
Thus the left extreme column of Q is blank. Reflect for a right termination.

If both terminate, both extremes are blank, so tau=0 in (3) and D_Q>=2.
If only the left terminates, the right comb continues at least through s+2,
by even parity of terminal heights. Its selected support (s+1,b-1) sees
endpoint (s+1,b), forcing (s,b-1) blank. This extreme column has exactly
one selection, so tau=1 and D_Q>=1. The other unequal case is symmetric.
This proves (5). QED.

The comb receiver column pairs are {a-1,a} and {b,b+1}, entirely outside
Q. A side support inside Q is already part of its actual selected count.
Neither a partial negative receiver half nor a positive matching export
is counted as a donor.

## 4. Compensation by disjoint distant strips

**Remote compensation theorem.** At the fixed terminal representative,
suppose there are q remote rungs satisfying Section 3, all endpoint-free,
outside G and mutually disjoint in physical tiles. If F+2q>=-1, then

    |T_0|+|M_0|<=mn/2.                               (6)

Proof. Every rung has D_Q>=1, and these are distinct original exterior
donors, so R>=q. Equation (1) gives 2Delta>=F+2q>=-1. Integrality proves
Delta>=0. The preserved normalization transfers this to the initial
objective. QED.

In particular it suffices to pair all but at most one negative comb into
such rungs: the flux lemma gives F>=-N_negative and q=floor(N_negative/2).
The condition concerns existence and unique capacity of distant geometry,
not a fixed radius around an end. Positive comb flux can reduce the number
of pairs required.

For an initial-pair theorem, the new rung hypotheses must hold at the
normalized representative or have a separate preservation proof. Preserving
the original mouth data alone is not a blanket assertion about an arbitrary
new exterior region.

## 5. Exact capacity when rungs overlap

Give an aligned-terminal rung weight w_j=1 and an unequal-terminal rung
weight w_j=2. Equation (5) gives w_j D_(Q_j)>=2 in both cases. For an
original physical no-P tile Q let m_Q be its source-mouth multiplicity,
zero, one or two. Its available coefficient in Dsingle+2R_noP is 2-m_Q,
where R_noP is the original exterior no-P part of R.

Impose the explicit allocation condition

    sum_(j: Q in Q_j) w_j <= 2-m_Q                  (7)

on every original no-P tile. It is sufficient to impose it only when its
actual deficit is positive, but that relaxation needs a uniform zero-deficit
argument for a uniform completion-class claim. Under (7),

    2q<=sum_j w_j D_(Q_j)
       <=sum_Q (2-m_Q)d_Q
       =Dsingle+2R_noP<=Dsingle+2R.                 (8)

Therefore 2Delta>=F+2q and (6) again follows if F+2q>=-1. The same physical
deficit is never allocated beyond its coefficient in the single exact ledger.

An unequal-terminal rung uses both doubled-ledger units outside G. An
aligned rung uses one, permitting it to cross one singly covered mouth or
another aligned rung outside G, subject to (7). A doubly covered positive
donor has zero remaining capacity. These are fractional original-ledger
claims with an exact integral doubled ledger, not separate supplies from
the crossing-loss and averaging formulas.

## 6. Explicit arbitrary-length family with zero original mouth payment

Take a width-ten, depth-h source, h>=1, with chamber origin (2,3). Set
y=2h+4. Its mouth has rows y,y+1 and columns 4,...,11. Put two complete
downward combs at columns 5 and 10, with endpoint rows y+1,...,y+2ell_L
and y+1,...,y+2ell_R, respectively, where ell_L,ell_R>=1. Use consecutive
matching and the supports in Section 3. Add selected pairs (y,7),(y,8)
and (s,7),(s,8), where s=y+2min(ell_L,ell_R). Leave other sites blank.
The containing even rectangle is

    max(2h+8,y+2max(ell_L,ell_R)+2) by 18.

The original mouth tiles are the left sparse singleton, a no-P tile with
two selections, another such tile and the right sparse singleton. The
shifted endpoint squares at columns 5,6 and 9,10 each have one endpoint
and two selections, and the middle shifted square contains the selected
pair. Thus F=-2, A=0 and D_G=Dprime=Dsingle=0. Both the exclusive and
capacity-aware mouth certificates have weight zero.

The remote Q has rows s,s+1 and columns 6,...,9. If terminal heights
differ, one extreme is blank and the other contains one side support;
the central selected pair gives exactly three selections in two tiles,
so D_Q=1. At equal heights both extremes are blank and D_Q=2. These
attain (5). The pair exists at arbitrarily large distance from the mouth.

For general feasibility, each source and comb support sees its intended
endpoint. The comb columns differ by five; their facing supports are at
6 and 9 on odd rows, and outside supports at 4 and 11 on even rows.
They do not touch one another. Near the mouth, the source's inside and
axial supports are diagonal to the new occupied sites, never adjacent.
Each added central pair has exactly its partner as an occupied neighbor:
the adjacent comb supports lie one row away at columns 6 or 9, hence
diagonally from the pair endpoints. The directly adjacent central sites
are blank. The two selected pairs occur at different even rows, separated
by at least two; their neighbors in the intervening row are blank. No
endpoint components join. These checks hold for every h,ell_L,ell_R,
and retained-support freezing applies. This proves a complete family,
rather than extrapolating from finite enumeration.

The construction does not assert absence of closer exterior donors; its
purpose is zero original mouth payment and arbitrary remote transport.

## 7. The existing all-radius obstacle is paid remotely

The family in `FROZEN_END_LOCALITY_OBSTACLE.md` still refutes every fixed-radius
end-local rule. Reflect it vertically. Its two top sparse ends then have
the inward-facing normal form of Section 3, with saturated terminal heights
equal. The endpoint columns differ by five. At their common saturated
band, the intervening two physical tiles contain no endpoints: the only
interior endpoint components are these two combs, while source chamber
endpoints and arms lie outside the intervening band/columns. The resulting
rung is outside the original mouth union. Thus D_Q>=2 is a distant original
exterior payment, and (1) with F=-2 gives Delta>=1.

This does not invalidate the locality obstacle. It provides the missing
nonlocal resource for that explicit family; the donor's position depends
on the comb length and lies outside the previously saturated neighborhood.
It also shows why stopping at a zero mouth certificate would miss a real
route toward the grid target.

## 8. Verification and remaining geometry

`develop/check_remote_comb_rungs.py` passes 54 physical configurations,
including 36 unequal-length cases and six instances of the old all-radius
obstacle, through radius 40. It verifies feasibility, complete freezing,
the initial physical ledger, endpoint-free and exterior rung membership,
the exact two-partition identity and original donor payment. Both mouth
certificates are zero in the new zero-mouth family. The finite checks
test the general proofs above; they do not establish the quantifiers.

The module `formal/SubQuorum/RemoteCombRungs.lean` adds four scoped results:
continuing-comb boundary exclusion, the conditional physical/shifted strip
identity, finite weighted donor capacity and integral flux compensation.
The terminating-end boundary exclusion already has a scoped formal proof
in `LongBentTerminalStrips.lean`. Full rung geometry, comb flux membership,
pair existence, normalization adapters and the grid family remain written.
The local sequential Lean 4.33.0 audit passes 106 scoped declarations in
`output/remote-comb-rung-formal-check.json`.

Run:

    python3 develop/check_remote_comb_rungs.py --output output/remote-comb-rung-controls.json
    python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0 --output output/remote-comb-rung-formal-check.json

The remaining step is a general existence-and-capacity theorem: negative
combs may lack a compatible partner or overlapping axial range; prospective
rungs may contain foreign endpoints or compete for already allocated donors.
The current hypotheses do not exclude these cases. The subsequent note
`CLOSED_SOURCE_CAVITY_COMPENSATION.md` proves complete-component cavity
closure, including nested parallel sources and a zero-mouth family whose
only negative-pair rung is occupied. General cavity closure remains an
additional hypothesis. Arbitrary positive bent components,
the universal coefficient-one grid bound and triple equality remain open.
Submitted manuscripts are preserved.

A separate independent review of this note and the capacity-aware extension,
task 75dcde82-64ab-4958-bedc-86b704d8f719, completed ACCEPT at
2026-10-19T12:20:17.053Z, observed gpt_6/pro. It checks the written geometry
and allocation under their stated hypotheses, not execution of controls or
Lean. Its response and scope are archived in
`output/capacity-and-remote-review-response.json` and
`docs/reviews/2026-10-19-capacity-and-remote-assessment.md`.
That verdict predates the subsequent closed-cavity note.
