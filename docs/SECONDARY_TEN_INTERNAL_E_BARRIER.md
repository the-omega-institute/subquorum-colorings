# A predecessor barrier at every internal E support

22 October 2026. This note retains ALL H3 originals and the explicit
complete full-U/rotor model of
[the mandatory E-footprint theorem](SECONDARY_TEN_MANDATORY_E_FOOTPRINT.md).
Every actual original is a lattice-isometric full even U(L,d,f), L>=6,
d,f>=4, or a standard rotor. Original endpoints, supports and matching
are immutable; endpoints of different originals are disjoint; every
unconsumed original support has occupied degree one. No exhaustion of
arbitrary grid components by this catalogue is asserted.

## Statement

Let a_j be odd, s_j even, and all w_j>=12,z_j>=24 even, with

    a_j=a_(j-1)+z_(j-1)-6,
    s_j=s_(j-1)-w_j-12,
    C_j=s_j+w_j+13=s_(j-1)+1.

At EVERY internal index j>=1 in a complete extension, the actual owner
R_j of the old E support y_j=(a_j-1,C_j) is LEFT north-terminal:

    U(L,d,f), chart(r,c)->(a_j-1-d+r,C_j+1-c),
    10<=d<=z_(j-1)-10, with L,d,f even, L>=6,f>=4.       (1)

These are necessary conditions, not a full breadth/far-leg classification
or an existence assertion. In particular every such owner has original
charge -1 and contains ELEVEN consecutive endpoints

    {(r,C_j): a_j-11<=r<=a_j-1}.                         (2)

Only the first E owner can have positive charge. If n_L,n_R count all
E-owner phases, n_R<=1 and n_L>=n-1. The previously proved exact
immutable inventory remains Delta(N+S)=sum(L_j^(t)-1)+n>=6n; this
refinement allocates its E part as DeltaS_E=n_L, DeltaN_E=n_R.
It is not a net Phi bound.

For an internal j with j+1<n, a right actual t_(j+1) owner with breadth
w_j+w_(j+1)+26, incident depth D and far depth g necessarily satisfies

    D<=z_j-12   OR   D-g>=z_j+2.                         (3)

In particular D=z_j+4 is impossible for EVERY even g>=4. The first
possible deep incident depth is at least z_j+6, and at that depth g=4.
Neither surviving phase is asserted sufficient or completely extendible.

## Proof of the predecessor barrier

The mandatory-footprint theorem applies without alteration: y_j is
absent from H3, its west/south/east neighbors belong to retained different
originals, and completeness requires a fresh north-terminal consumer.
Both rotor roles collide with old endpoints. A U consumer is in one of
the two charts

    (r,c)->(a_j-1-d+r,C_j+1-c)  left,
    (r,c)->(a_j-1-d+r,C_j-1+c)  right.

Its incident column occupies EVERY row from a_j-1-d to a_j-1,
including bar rows zero and one. Left depths 4,6,8 collide with P_j.
A right owner has d>=z_(j-1)+2, because its lower bar endpoint at
(a_j-d,C_j+1) collides with V_(j-1) for every even d<=z_(j-1).

There is an additional retained original above this INTERNAL root:

    X_(j-1)=U(6,4,4),
    chart(r,c)->(a_(j-1)+2-r,s_(j-1)+2-c).

Its near column is s_(j-1)+1=C_j and includes all FIVE endpoints
at rows a_(j-1)-2,...,a_(j-1)+2, equivalently

    a_j-z_(j-1)+4,...,a_j-z_(j-1)+8.                     (4)

Since z_(j-1)>=24, the top row a_j-z_(j-1)+8 is above y_j.
The incident interval, which ends at y_j, can avoid (4) only by starting
strictly below that top row:

    a_j-1-d > a_j-z_(j-1)+8.

Thus d<z_(j-1)-9. Both depths are even, giving d<=z_(j-1)-10.
This applies to BOTH U orientations. It contradicts the necessary right
depth d>=z_(j-1)+2. The owner is left, and its previous lower bound
d>=10 proves (1). Its incident column then contains (2). The full-original
charge calculation in the cited theorem gives charge -1 independently
of breadth/far depth. Distinctness of the E owners and their distinction
from all t owners follow from that theorem's same-color terminal argument.
Consequently all n-1 internal E owners contribute to S, and only the
root owner can contribute to N. This proves the inventory assertions.

## Refined internal depth gap

Put a=a_j,C=C_j,z=z_j. The proposed right t_(j+1) owner B has far
column C and occupies its entire interval

    [a+z-10-D, a+z-10-D+g].                              (5)

It is distinct from R_j. Indeed, if B contained y_j on this column,
the next row a would also belong to its interval: y_j has even row
and the interval's last row is odd. That next point is a retained E_j
endpoint, contradicting endpoint disjointness. Therefore (5) must avoid
the eleven R_j endpoints AND the old endpoint (a,C), hence every row
in [a-11,a]. Both endpoints of (5) have the same odd parity as a.
Its last row must be at most a-12, or its first row at least a+2.
These alternatives are exactly D-g>=z+2 or D<=z-12, proving (3).
In the deep phase g>=4 gives D>=z+6; equality gives g=4.

For the earlier first-deep choice D=z+4, the far-column interval starts
at a-14 and, for every g>=4, contains (a-10,C). This point belongs
to R_j by (2). Thus it cannot occur at any internal root. In the
smallest case g=4, B ends at a-10, so it does not contain y_j and
the collision involves two distinct originals directly.

## What fails, and what remains valid

The first-root staircase and width-five stack theorems remain valid in
their stated scope. This result obstructs the proposed way to APPLY
the first-root package independently at all internal blocks. It does
not refute the target global inequality or the conditional additivity
of NEW stack increments on disjoint physical tile footprints.

The obstruction is stronger than an old-endpoint collision. For example,
take H3 at a_0=31,s_0=0,h=6, widths (12,12,12), depths (24,24,24).
Then j=1 has a=49,s=-24,C=1. The first-deep right t_2 candidate is

    B=U(50,28,4), chart(r,c)->(35+r,-49+c).

Its endpoints are disjoint from ALL H3 original endpoints. Nevertheless
it contains (39,1), while any actual R_1 must contain every (r,1)
for 38<=r<=48. Hence H3+B has NO complete feasible extension in
the stated model. This is a precise obstruction to that partial family's
complete extendibility, not a complete-family counterexample to Phi.

## Validation scope and next step

The companion verifier checks complete original endpoint/support/matching
records at varied internal indices, nonuniform dimensions and translations;
the predecessor's five points; both-orientation incident bounds; charge
phases; eleven-point inclusion; refined B decisions; and old-disjoint
but nonextendible first-deep candidates. The scoped Lean source proves
the coordinate barrier, orientation exclusion, interval gap and depth
consequences. Actual-owner normalization and the general charge inventory
use the written earlier theorem, not a finite census.

Exact controls pass 84 predecessor guards, 37,800 full-original U roles,
16,632 eleven-point inclusions and 13,536 refined depth-gap decisions.
There are 6,492 sampled old-disjoint left owners; 1,008 old-disjoint B
candidates fail the mandatory footprint, including 60 first-deep examples.
The displayed uniform example is checked separately. Standalone local
Lean passes 22 declarations, including 16 theorems, with individual axiom
reports, no warnings and no sorry/native axioms. The independent review
is running in the existing cavity/stack conversation; no verdict is
claimed. See the [validation record](../output/secondary-ten-internal-e-barrier-validation.json).

Next: classify the surviving internal LEFT E owners and their exact
joint receipts, including renewed support obligations. Any bulk allocation
must use actual internal configurations. No global 5/6 improvement,
complete-family allocation or rectangular-grid triple equality is claimed.
The submitted 11 October manuscript is unchanged.
