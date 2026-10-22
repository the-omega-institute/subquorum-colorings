# The two matching-cost-fourteen branches: a conditional reduction

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Status and inherited scope

Historical checkpoint: the conditional reduction below predates the completed
written geometry in COST_FOURTEEN_GEOMETRY_AND_37_39.md. That follow-on note
closes the two obligations stated here, with its own validation and independent
review status. The previous 35/37 theorem has since received independent ACCEPT.
The remainder of this document preserves the original conditional checkpoint.

This is a research reduction, not a completed improvement theorem. The written
complete-source coefficient remains 35/37, with its independent review pending.
Use exactly the finite COMPLETE immutable full-even-U/standard-rotor model and
representative ledger in LOW_COST_EXCEPTIONAL_DOUBLES_AND_35_37.md. No claim
about an arbitrary rectangular grid follows without the missing source bridge.

The only dimensions outside the existing compensated class C* with original
matching size at most 14 are U(8,6,8), U(8,4,10), and their reflections. All
other exceptional dimensions cost at least 15. Indeed m=w+(a+b)/2-1; w>=12
costs at least 15, width 6 is covered, and width 10 with m<=14 has legs in
{4,6}. Width 8 then gives a+b<=14; the uncovered possibilities have sum 14
and unordered legs {6,8} or {4,10}.

## Local evidence and the two geometric obligations

Normalize the producer's bar to rows 0,1 and its legs to columns 1,8. If both
terminals are unactivated, their retained beyond-tip supports force the points
(a+1,2),(b+1,7) finally blank. Filter the existing occupied-gate catalogue
against these points and original endpoint disjointness.

For Y=U(8,6,8), the finite catalogue leaves only one noncolliding pair of gate
roles: a COMMON inverted U(6,4,4), in the chart (r,c)->(6-r,c+1). The tile
Q={6,7}x{2,3} has its original pair (6,2),(6,3), no original support, and
the finally blank point (7,2). The producer has neither endpoints nor supports
in Q. Thus the local pair data match the old forced-witness construction in
SHORT_LEG_DEFECT_INJECTION.md, Sections 2--4. This suggests one actual defect
unit for Y. It does not give two: the other side need not stay nonfull.

For X=U(8,4,10), every endpoint-disjoint role pair in the finite catalogue has
a left transverse phase11 terminal of incident height 4 and breadth 6, and a
right longitudinal phase11 terminal of incident height 8. Thus a zero-activation
X double with both gates occupied appears to force an original negative long
terminal. The right gate corner is (2,7); it is DIFFERENT from the fixed
support (3,7) whose consumption defines the corresponding actual mark.

These observations suggest the following precise obligations, still OPEN here:

1. Prove both role conclusions for arbitrary incoming dimensions. Assign one
   actual A/H unit to every cost-fourteen actual double except the special X
   sources just described. Prove jointly that these units avoid every unit
   already assigned to C*: activated source occurrences, blank marked tiles,
   and occupied forced-witness tiles. The old witness argument is relevant,
   but a finite role list is not a proof of this extension.
2. Inject the remaining special X sources into DISTINCT original negative
   legs of length at least 8. In particular, prove the source-to-gate mapping
   is injective in the same immutable ownership system used by the existing
   marked-side capacity budget. Do not equate gate occupation with marking.

The companion finite checker tests local masks, not complete physical
realizations of these branches. It reports that limitation explicitly.

## A proved conditional counting lemma

Let z,s,t be C* actual doubles with zero, one, two activated terminals. Let p
count cost-fourteen actual doubles, x the special X exceptions, and q all
remaining actual doubles. Let n0 be the unmarked positive count. Suppose the
two geometric obligations supply, in ONE shared pool,

    0<=x<=p,   2R>=2z+s+2t+p-x.                     (A)

The separate original matching credit is not geometric reserve. A negative U
with b of its two original legs of length at least 8 has at least 9+2b matching
edges. Summing original matchings ONCE gives Mminus>=9B+2x if the long-leg
injection exists. The inherited mark capacity G<=4B then gives

    4Mminus>=9G+8x.                                 (B)

An owner can have two counted long legs; both increments are already included
in its ONE matching size. No matching edge or defect is spent again.

The positive matching sizes independently give Mplus>=9N+5p+6q. The original
matchings partition M, so (B) implies

    4M>=36N+20p+24q+9G+8x.                          (C)

Write mu=N+R-G=n0+R-z-s-t-p-q. From (A),

    2(-mu)<=2q+s+p+x.                               (D)

If mu=-ell<0, then N>=s+p+q and R>=0 give

    4M>=45s+65p+69q+9ell+8x.

The inequality

    2(45s+65p+69q+8x)-69(2q+s+p+x)
       =21s+61p-53x >= 0

follows from s>=0 and 0<=x<=p. By (D), 4M>=78ell. If mu>=0, coefficient
one follows directly from the ledger. In both cases sigma>=mu therefore gives
the CONDITIONAL conclusion

    |T_sel|+(37/39)|M|<=mn/2,
    equivalently 78|T_sel|+74|M|<=39mn.

This would gain 4|M|/1443 over 35/37 and 3|M|/26 over 5/6 on the same
complete-source domain. No unconditional 37/39 bound or sharpness is claimed.
The scalar reduction is already universal; finite enumeration only checks it.

## Verification and next step

`formal/SubQuorum/CostFourteenBudget.lean` checks the long-leg matching
inequality, aggregate mark/long-leg budget, the conditional shared-reserve
margin, combined matching budget, and the conditional coefficient. It ASSUMES
the geometric injections and source ledger; it does not formalize them.

`develop/check_cost_fourteen_reduction.py` tests the existing anchored-role
library, the exact small-size classification and conditional signed budgets.
The next decisive work is the all-parameter geometry and shared physical
injection above. Until that is complete, communicate 35/37 as the established
written result, with its review status, and 37/39 only as a candidate reduction.
