# Hall regions with positive slack and one shared HH budget

11 November 2026. Balanced tight sets are the zero-slack case of a more
general accounting identity. Positive-slack regions are essential for
simultaneous exposure: their neighbourhood may admit one entrance but not
two. This note counts arbitrary overlapping regions without granting a
separate HH capacity to each region.

## Setting

Use the separated-core terminal notation of
`SIMULTANEOUS_PORT_COMPLETION.md`. The exterior direct graph on black B and
white T has a B-saturating matching, with |T|=|B|+q, q>=1. There are r
black centres C and r-q white HH sources W. A full physical auxiliary
matching gives a terminal bijection pi:T disjoint-union W -> B disjoint-union C.
Let k be the number of TH centre paths. Then k>=q, and exactly k-q HH
paths end in B. Centres have no direct selected neighbours. An actual
edge is charged only on its one TH component.

For a finite nonempty collection of nonempty D_j subset B, put
F_j=N_T(D_j) and s_j=|F_j|-|D_j|>=0. The regions may overlap or be nested.
Choose nonnegative weights lambda_j, not all zero, and define

    phi_B(b)=sum_j lambda_j 1_(b in D_j),
    phi_T(t)=sum_j lambda_j 1_(t in F_j),
    S=sum_j lambda_j s_j,       mu=max_(b in B) phi_B(b)>0.

Put phi_B=0 on centres. Unlike the tight case, the white and black maxima
need not coincide. The denominator mu below is the BLACK maximum.

For TH paths define total withdrawal and compensation

    A=sum_(t in T) (phi_T(t)-phi_B(pi(t)))_+,
    L=sum_(t in T) (phi_B(pi(t))-phi_T(t))_+,
    R=sum_(t in T, pi(t) in C) phi_T(t).

## Shared-slack theorem

For every full physical N,

    A-L = S + sum_(w in W) phi_B(pi(w)),
    S <= A-L <= S+(k-q)mu.                                  (1)

If z is the number of TH paths with positive compensation, then

    z >= max(0,ceil((A-S-(k-q)mu)/mu))
      >= max(0,ceil((R-S-(k-q)mu)/mu)).                       (2)

All z paths end in exterior B and are non-direct. When actual weights
are at least one,

    f(N) >= k + max(0,ceil((A-S-(k-q)mu)/mu)).                (3)

**Proof.** Summing the regional cardinality differences gives
sum_T phi_T - sum_B phi_B = S. Since pi is a bijection,

    sum_(t in T) [phi_T(t)-phi_B(pi(t))]
      = S + sum_(w in W) phi_B(pi(w)).

The left side is A-L. Exactly k-q HH endpoints are in B, each with
potential at most mu; all other HH endpoints are centres of potential
zero. This proves (1).

For every direct edge t--b, membership b in D_j forces t in F_j.
Consequently phi_T(t)>=phi_B(b). A TH path with positive compensation
cannot be direct and cannot end at a centre. Its compensation is at most
phi_B(b)<=mu. Therefore z mu>=L>=A-S-(k-q)mu. The centre TH paths
contribute their whole source potential to A, so A>=R. This proves (2).
The k centre paths and the z compensating exterior paths are distinct,
non-direct paths. Each uses at least one actual edge, and their actual
edge sets are disjoint. Charging one such edge per path proves (3). QED.

Each HH endpoint contributes its actual potential ONCE in (1). Its
membership in several regions is already included in phi_B and capped
by mu. The same argument counts the intrinsic slacks in the single scalar
S; it does not give a fresh source budget to each region. The previous
tight-set theorem is recovered by s_j=0 and q=1.

## Exposure and the physical examples

If all W sources serve centres, k=q and there are no exterior HH endpoints.
If all other TH paths are direct, L=0 and (1) says A=S. In particular
R<=S. For a single region with unit weight this gives

    number of centre entrances in F <= |F|-|D|.               (4)

For fixed chosen entrance set, imposing (4) for ALL D is precisely Hall's
condition for its simultaneous exposure, as proved in the completion note.
Thus the same slack ledger has a constructive matching interpretation
under the specified direct-exterior hypotheses.

In the 8-by-12 example, the two specified centre paths withdraw twice
from a region with |D|=7, |F|=8. If k=2, then q=k=2, S=mu=1, R=2,
and any full extension needs z>=1 and at least three unit expenses.
If k=3, the third centre path itself supplies a third unit; this case
does not require positive exterior compensation from the R-only bound.
The exact optimum remains two by choosing a different entrance.
In the 12-by-18 family the analogous region has |D|=17, |F|=18.
The two cheap centre paths incur the same incompatibility; an attaining
full matching replaces one by a K edge and has exact fee K+1.

Formula (3) applies to actual path configurations. It does not supply a
geometric lower estimate on A for arbitrary full N, route an arbitrary
endpoint assignment, or prove a universal 5/6 improvement or the grid
triple equality. The new completion theorem supplies explicit physical
routes in its centre-relay/direct-exterior class.

Run `python3 scripts/check_hall_slack_budget.py` for independent finite
endpoint controls at q=1,2,3. The checker includes non-tight regions,
overlapping and nested choices, multiple weights, and full terminal
bijections. The all-input assertions have the proof above. No new Lean
verification is claimed.
