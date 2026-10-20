# Signed reserve transfer on legal extensions; the reserve is not a lattice rank

20 October 2026. For arbitrary nested COMPLETE FEASIBLE source subfamilies
I contained in J of the fixed U/rotor family, the exact reserve change is

    R(J)-R(I) = S(J minus I)+2F(I,J)
               -E(old,new)-E(new,old)-E(new,new).        (1)

All terms on the right are actual source or directed-event counts, defined
below. There are no per-restored-support payments. The feasible-source Horn
lattice also has an explicit obstruction: even after fixing every positive
owner and actual marked side, R is neither submodular nor supermodular on
that lattice. Thus its exact legal closure structure does not justify treating
R as a polymatroid rank or invoking either lattice inequality without proof.
These results do not establish the missing signed bound or full allocation.

## 1. Exact setting and original ledger

Use all complete-source hypotheses and legal retention semantics of
[the source closure theorem](SOURCE_RETENTION_HORN_CLOSURE.md). No dimensions,
phases, recurring owners, full contacts or rotors are excluded. Original
endpoint sets are disjoint, matchings unchanged, and all original supports
outside retained endpoints remain mandatory. Both I and J are feasible.

Let S(I) be the sum of the magnitudes of NEGATIVE original charges in I.
Let F(I) be the set of actual full physical tiles in P_I that are not full
tiles of any one original owner in I. For every owner i define its unchanged
original occupied set O_i=P_i union T_i. Define the ACTUAL directed intratile
event set

    E(I)={(i,p,q): i in I, p in P_i, q in P_I minus O_i,
                    p adjacent q, tile(p)=tile(q)}.      (2)

This contains regular and irregular events together. Its key includes the
original source and endpoint direction; an undirected contact may yield zero,
one or two events. Neither original support consumption nor a repeated use of
the same owner is automatically a new event. The established ledger gives

    R(I)=S(I)+2|F(I)|-|E(I)|.                           (3)

Indeed C=2|F|-Kregular and |E|=Kregular+Kirregular. R in(3) is the SAME
reserve as 2R=A+U0+Z0+H; these are not two independently available pools.

## 2. Monotone event and new-full-tile sets

E(I) is a subset of E(J): all original occupied sets O_i are fixed, and
retained endpoints only increase. Each old event therefore remains the SAME
source-labelled directed occurrence.

Also F(I) is a subset of F(J). A formerly mixed full tile remains full. It
cannot become a newly added owner's original full tile, since its four old
endpoints would then overlap that owner's original endpoint set. Its original
owners keep their original profiles. Thus the tile remains mixed full.

Write F(I,J)=|F(J) minus F(I)|. This counts actual newly full mixed tiles,
not arbitrary receiver overlaps, original full tiles of new sources, or holes
in a proposed spatial cut.

## 3. The three disjoint new-event classes and proof of(1)

Each q in P_J has a unique original endpoint owner. Partition E(J) minus E(I)
by its event owner i and the owner of q:

- E(old,new): i belongs to I and q's owner belongs to J minus I;
- E(new,old): i belongs to J minus I and q's owner belongs to I;
- E(new,new): both owners belong to J minus I.

There is no old-old event in the difference: with both original owners already
in I, every condition in(2) was already true. The three classes are disjoint
and exhaust the difference, including all recurring-owner and same-tile cases.
S(J)=S(I)+S(J minus I) by unchanged source ownership. Subtract(3) for I from(3)
for J and use the two monotone sets and this exact event partition. This proves
(1) for every legal extension, with no bounded enumeration or new injection.

If ALL original positive owners and actual marks are preserved, then N and G
are unchanged, so the allocation margin has the SAME signed change as R.
In particular an induction from a legal marked hull I would need

    E(old,new)+E(new,old)+E(new,new)
      <= S(J minus I)+2F(I,J)+[N+R(I)-G]                (4)

to conclude N+R(J)-G>=0. Equation(4) is an explicitly identified remaining
obligation, not a proved inequality. The bracket is the initial common margin,
which may not be spent separately on multiple extensions. Along a nested chain
each directed event and each newly full tile enters at most once, so(1)
telescopes with the original source masses. This does not make its signed
increments nonnegative.

## 4. Actual feasible closure lattice with fixed positive demand

Take the four complete negative sources V1,V2,V3,V4 of
[the certified source-cut example](SOURCE_CUT_BOUNDARY_PAYMENT_OBSTRUCTION.md).
Their individual negative charges are1,1,1,5. Each singleton is feasible and
has no foreign events or new mixed full tiles, hence reserves1,1,1,5. The
full four-source fusion is feasible with reserve3. Its exact eight dependency
rules imply that every two-owner seed has the full four-owner closure.

Take also the established seven-source marked-gate chamber B, translated by
(30,30). Its exact original construction is given by marked_gate_modules in
the existing checker. It has N=1,G=2,A=2,H=10,R=6. It is far from the negative
example, so there are no cross-component endpoint contacts or support conflicts.
Every whole B-union fusion below is complete feasible, with exactly the SAME
positive owner and two marked sides. Exact component additivity gives:

| Added negative owners besides B | N | G | R | N+R-G |
|---|---:|---:|---:|---:|
| none | 1 | 2 | 6 | 5 |
| V1 | 1 | 2 | 7 | 6 |
| V2 | 1 | 2 | 7 | 6 |
| V3 | 1 | 2 | 7 | 6 |
| V4 | 1 | 2 | 11 | 10 |
| V1,V2,V3,V4 | 1 | 2 | 9 | 8 |

The feasible families in this sublattice have meet I intersect J and join
Cl(I union J), where Cl is the exact physical-source Horn closure. Separate
endpoint components have no nontrivial dependency coupling them: a consumed
support lies next to its producer anchor, and if an occupying neighbor is
itself a support, its distinct anchor forces its consumption too. Thus the
four-source closure computed here is unchanged by the distant chamber.

For I=B union{V1}, J=B union{V2}, their meet is B and their join contains all
four negative sources. Therefore

    R(I)+R(J)=14 < 15=R(I meet J)+R(I join J),           (5)

contradicting lattice SUBMODULARITY. For I=B union{V3}, J=B union{V4}, the
same meet and join give

    R(I)+R(J)=18 > 15=R(I meet J)+R(I join J),           (6)

contradicting lattice SUPERMODULARITY. These are exact complete-source
counterexamples to the two candidate inequalities, not abstract count vectors.
The join is a legal completion; it is not an infeasible plain union.

The examples use a separate negative endpoint component. They do not exclude
a stronger connected or demand-local theorem. All allocation margins are
positive. Also R(B)=6 is BELOW every displayed extension's reserve: these
examples do NOT disprove a reserve comparison specifically with a least
marked-source hull. That separate comparison remains open.

## 5. Implication and verification scope

The retention theorem supplies an exact feasible closure system, but reserve
is not automatically a monotone/submodular/supermodular resource on it. A
successful global argument must control the actual directed costs in(1), using
their geometric relation to demand or a stronger legal restriction. It cannot
replace them by the number of closure rules, sources or restored supports.
The unrestricted mu>=0 and rectangular-grid equality remain OPEN.

Run `python3 develop/check_closed_extension_reserve.py`. It reconstructs actual
new full tiles and directed events on legal nested subfamilies of existing
complete fixtures, checks the three-way event partition, and verifies the six
displayed reserves independently with the exact geometric defect checker.
Closed sets are exhaustive only through seven owners; larger fixtures use
sampled hulls. The general proof in Sections1--3 is separate from these finite
controls. This new note has no new Lean verification or independent-review
verdict; the preceding closure review does not cover it.
