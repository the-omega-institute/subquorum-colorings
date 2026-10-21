# Simultaneous internal compensation with unbounded t far legs

22 October 2026. This strengthens the
[internal short-pair theorem](SECONDARY_TEN_INTERNAL_SHORT_PAIR.md): only
the E owner's far leg remains four; the t owner's far leg is ARBITRARY.
The standing hypotheses are the same full-original H3 chain and explicit
complete even-U/rotor model. Actual t/E owners are distinct by the earlier
terminal-color argument. No arbitrary-grid catalogue exhaustion, complete
extension existence or exterior-owner monotonicity is assumed.

## Statement

Fix one complete extension and any subset J of its INTERNAL chain blocks
whose actual E owner has incident ten and far four. At each j in J,
the proved actual-owner coupling forces

    R_j=U(L_j,10,4), chart(a_j-11+r,C_j+1-c),
    T_j=U(M_j,4,g_j), chart(a_j-8+r,s_j+1-c),
    L_j=w_j+M_j+14+q_j, q_j>=0 even,
    M_j>=6,g_j>=4 even, C_j=s_j+w_j+13.

Let delta_j be the OLD-chain far-contact deduction of the accepted
[left-chain exterior theorem](SECONDARY_TEN_LEFT_CHAIN_EXTERIOR.md).
Explicitly, put ell_j=s_j+1-M_j and y_j=a_j-8+g_j. Let k>j be the
first index with ell_j>=s_k-3, if any. Then delta_j=1 exactly when
ell_j=s_k-3 and y_j is a_k-2 or a_k; otherwise delta_j=0. Because
T_j is an actual owner it is endpoint-disjoint from H3, so that theorem
applies. Whenever delta_j=1, M_j=s_j-s_k+4>=28.

Then the selected-union increment is EXACTLY

    Phi(H3 union all selected R_j,T_j)-Phi(H3)
       =sum_(j in J) (M_j-2*[q_j=0]-delta_j) >=4*|J|.    (1)

Every pair's FULL endpoint tile footprint is disjoint from every other
selected pair's footprint, even if g_j is arbitrarily long and their
row ranges overlap. This geometric assertion uses the endpoint disjointness
of the actual owners and the retained P bars. It is not a hypothesis
postulating an allocation or a finite observation.

Only NEW increments against the single retained H3 inventory are summed.
Old wall-owner charges, full tiles and directed events are never credited
again. Arbitrary E far legs, deeper E incident legs and the remaining
actual owners still require analysis. In particular (1) is not a global
5/6 improvement or a rectangular-grid triple equality theorem.

## Exact one-pair calculation with arbitrary g

Write a,s,w,L,M,g,q at one selected block. R's entire endpoint/support/
matching record is the same as in the short-pair proof; its old-chain
gain is exactly one. The accepted left-chain exterior theorem gives
T's entire old-chain gain M-1-delta, with no finite depth bound.

The R/T calculation is independent of g. Their near/bar parts have
the same separation as before. Put F=s-M-q, R's even far column, and
G=s-M+1, T's odd far column. If q>=2 their physical tile columns are
disjoint wherever their row ranges meet. If q=0, R's far interval is
[a-11,a-7], while T's far interval is [a-8,a-8+g]. As g>=4, their
overlap is STILL exactly rows a-8,a-7. At the first row both directions
target original supports; at the second both directions are events.
Neither of the two shared tiles becomes full: the top one lacks T at
row a-9, the bottom one lacks R at row a-6. Thus the mutual receipt
is exactly zero new full tiles and 2*[q=0] new events, for EVERY g.

T's possible extra OLD far receipt is at block k>j, in rows at least
a_k-2>=a_j+16. It is disjoint from all R endpoint tiles, whose last
row is a_j. There can be no hidden three-owner full tile involving
R and that far contact. Old full tiles/events persist. Consequently

    DeltaPhi({R,T}|H3)=1+(M-1-delta)-2*[q=0].          (2)

The bound is at least four. If delta=0, use M>=6. If delta=1, use the
structural width M>=28 to obtain at least25, even in the tight case.
The old exceptional deduction is paid from its own original T mass once;
it is not silently discarded or charged to a second group.

The tight new forced support x=(a-6,F) from the short-pair theorem
remains forced for every g: north is in R and east in T, while x is
absent from H3,R,T. The theorem does not claim support closure.

## Why arbitrary actual pairs have disjoint endpoint tile footprints

Take selected indices i<j and let a=a_j,s=s_j. Since a_j-a_i>=18,
every endpoint of R_i and every bar/near-leg endpoint of T_i is above
row a_i-1, whereas R_j begins at a_j-11>=a_i+7 and T_j at a_j-8.
Their physical tile rows are therefore disjoint. The ONLY part of pair i
that could share an endpoint tile with pair j is T_i's long far column,
at the ODD column ell=ell_i. Its continuous endpoint interval starts
at a_i-8 and ends at the ODD row y=y_i.

First compare with R_j. R_j's bar rows a-11,a-10 are an entire row
of full physical tiles, with column interval [F_j,C_j], F_j even,C_j
odd; its two stems stay inside those same tile columns below the bar.
If the physical tile column of ell meets this range, parity gives

    F_j+1<=ell<=C_j.

If y>=a-11, then T_i contains (a-11,ell), an R_j bar endpoint,
contrary to actual endpoint disjointness. Therefore y<=a-12. This is
an ODD row immediately above R_j's first EVEN bar row a-11, so the
two endpoint tile-row sets are disjoint. If the tile columns do not
meet, separation follows from columns. This covers all of R_j.

Now compare with T_j. Its endpoint tile-column range runs from its
ODD far column G_j=s-M_j+1 through its EVEN near column s. If ell's
tile column meets it, parity gives G_j<=ell<=s+1, with ell odd.
There are two cases.

- If G_j<=ell<=s-1, then (a-8,ell) is an actual T_j bar endpoint.
  Since T_i starts above that row, disjointness forces y<a-8. Both y
  and a-8 are odd, hence y<=a-10.
- If ell=s+1, the retained P_j bar contains (a-8,s+1). Old endpoint
  disjointness gives the SAME bound y<=a-10. The old P guard is essential:
  T_j itself has no bar endpoint in this outside column.

The last possible T_i tile row is then (a-11)/2, whereas T_j's first
bar endpoint tile row is (a-9)/2. The tile footprints are disjoint.
Outside the stated column interval, column separation applies. T_j's
far/near stems use tile columns already covered by this interval, so
arbitrary g_j introduces no additional case.

This proves endpoint tile-footprint disjointness for EVERY ordered pair
i<j in the actual extension, without imposing any maximum g. In
particular if T_i's old exceptional frontier block k is selected, its
long column would hit T_k's earlier bar before reaching X_k; such an
activation is impossible. Formula (1) also permits exceptional contacts
at unselected old blocks, whose actual contributions remain unchanged.

## Exact simultaneous ledger

Each new full tile contains a new endpoint, so it lies in its new
pair's endpoint footprint. Every new directed intratile foreign event
also lies in that footprint. Different pairs have disjoint footprints,
so neither an event nor a newly full physical tile can use two pairs.
Every original source owner is distinct, and its immutable charge enters
once. The whole new full-tile/event sets are thus the disjoint union of
their one-pair increments, including the individual OLD far receipts.
Equation (2) adds exactly, proving (1). No overlapping old-prefix
reserve, unassigned exterior loss or presumed monotonicity is involved.

## Verification scope

Full-original finite controls supplement the general separation proof:
they cover activated old X receipts, long legs beyond the chain, mixed
gaps, arbitrary selected subsets and nonuniform chains. The scoped Lean
source handles parity/column gates, collision-to-terminal bounds, tile
row separation and conditional ledger induction. Actual-owner adapters
and full geometric receipt partitions remain written.

The verifier passes 2,264 exact arbitrary-far pair sets, including80
activated old X receipts, and58 actual endpoint-disjoint batch groups
of3/4/5pairs. Explicit far-depth2000 groups of2/5/11pairs have exact
gains2324/6810/19218 and disjoint endpoint tile footprints. Scoped local
Lean passes22declarations/17theorems with individual ordinary-axiom
reports and no warnings/sorry/native axioms. These checks supplement
the all-parameter proof. See the
[validation record](../output/secondary-ten-internal-long-pair-validation.json).

This strengthening was written after the short-pair audit input; no
independent ACCEPT for it is claimed. Its separate audit runs in the accepted
barrier conversation, on retained original stream65504. The submitted 11 October manuscript
and the primary star-forming/C4-free results are preserved.

The subsequent [E far-frontier theorem](SECONDARY_TEN_E_FAR_FRONTIER.md)
classifies every old-chain contact for incident-ten E owners with arbitrary
far legs. Their exact one-owner gain is 1-d with 0<=d<=2, and -1 is
attained. The further [both-far theorem](SECONDARY_TEN_BOTH_FAR_COMPENSATION.md)
combines this with nonstacking and an aligned-bar separation argument to
remove far4 as well. It has a separate proof, validation and live review;
the present audit does not cover that later input.
