# A sealed-cavity exclusion and stronger compensation for complete prefixes

22 October 2026. Owner: Wenlin Zhang and Haobo Ma. Status: general written
proof; exact full-original checks, scoped Lean and independent review have
separately recorded scopes. Use the full-U/rotor model, H3+B+R+A and actual
four-row staircase hypotheses of the accepted
[sharp compensation theorem](SECONDARY_TEN_ROOT_SHARP_STAIRCASE.md).
All original endpoint sets and original supports remain immutable.

Write a=a0,s=s0,u=w0,v=w1,z=z0, s1=s-v-12 and P=s+u+12.
The original charts are B=U(u+v+26,z+4,4) at(a-14+r,s1-1+c),
A=U(L,4,f) at(a-8+r,s+1-c), and

    J_i=U(H_i,D_i,G_i) at(a-10-i+c,P-D_i+r), i0..3.

Every dimension is even. Require u,v>=12,z>=24,L>=6,H_i>=6,G_i>=4,
4<=f<=z-8,D0>=u+L+14,D_i>=D_(i-1)+2,D3<=u+v+22,
H_i<z+i-4, and disjointness from all retained originals. H3 has at
least two blocks. Its P1 first bar row is t+1=a+z-14 and fills the
column interval [s1+1,s]. The ambient grid contains the retained objects;
the argument uses the explicit model, not arbitrary-grid catalogue exhaustion.

## Sealed-cavity lemma

If the selected prefix has a complete extension in the full-U/rotor model,
then

    H_3=z-2 implies D3<=u+v+18.                   (1)

Here H_3 denotes J3's height. Equivalently, a J3 far ray touching P1
cannot have D3=u+v+20 or
D3=u+v+22. This excludes every complete extension of the entire geometric
equality family from the preceding theorem, whose J3 has H_3=z-2 and
D3=u+v+22. Its geometric equality calculation remains valid.

### A general trapping fact

Let C be a finite grid rectangle and suppose every grid neighbor immediately
outside C is occupied by retained endpoints. Any new original containing
an endpoint in C has all its endpoints in C. Indeed, the endpoint-induced
grid graph of a full U or a standard rotor is connected. If one of its
paths left C, its first outside vertex would be an occupied retained
endpoint, violating disjointness between different originals. New originals
cannot enlarge or change one of the full retained originals.

Every orientation of a full even U needs at least five columns. In its
canonical orientation its column span is H-1>=5; after transposition its
column span is max(d,f)>=4. Reflections and translations preserve these
spans. A standard rotor needs exactly four columns in every orientation.
Consequently no permitted original fits in a rectangle of width at most3.
This statement has no height or size cutoff.

### The retained walls and forced site

Assume H_3=z-2, so J3's far row is t=a+z-15. Put b3=P-D3 and

    C=[a-12,t] x [s1+1,b3-1].

Its width is

    W=b3-s1-1=u+v+23-D3.                         (2)

The upper bound D3<=u+v+22 gives W>=1. All four outside walls of C
are occupied by the following retained endpoint sets:

| Wall | Points | Original |
|---|---|---|
| Left | (r,s1), a-12<=r<=t | B near stem |
| Right | (r,b3), a-12<=r<=t | J3 bar |
| Top | (a-13,c), s1+1<=c<=b3-1 | B lower bar |
| Bottom | (t+1,c), s1+1<=c<=b3-1 | P1 first bar row |

These are full walls, not only four guards. In B coordinates the left
wall has rows2..z-1 and column1, and the top wall has row1. The J3
bar starts at row a-12 and ends at t. Finally D3>=D0+6>=u+L+20
implies b3<=s-L-8<s, so the P1 interval covers the whole bottom wall.

The point q=(t,s1+1) is an ORIGINAL support of B: its B coordinates
are (z-1,2), the odd near-lateral support. It is absent from the selected
endpoint union. B has only its near/far stem columns there; all staircase
intervals start at columns at least b3>s1+1. A and the first H3 block
lie farther right, while later blocks start below t. The root and R
also lie to the right.

Both (t,s1) and (t+1,s1+1) are occupied endpoints, respectively of
B and P1. Hence q cannot remain an unconsumed support in a complete
extension: the model requires every unconsumed original support to have
exactly one occupied neighbor. Thus some fresh actual original must
contain q. The trapping fact confines it to C.

If D3>=u+v+20, (2) gives1<=W<=3, so no allowed full original fits.
This contradiction excludes that range. Since D3 is even, it proves (1).
Adding further originals cannot open an occupied wall or undo the forced
support condition. This is a complete-extension obstruction, not merely
a failure of one proposed choice of consumer.

## A ten-unit complete-prefix compensation theorem

For the SAME selected union, if it is a prefix of a complete extension,

    DeltaPhi >= L/2+7 >= 10.                       (3)

The conclusion is about the selected prefix relative to the retained H3
chain. It is not a claim that arbitrary additional originals have nonnegative
marginals, and it is not the global full-family inequality.

Use the accepted exact identity and nonreusing receipt partition:

    DeltaPhi=u/2+v+L/2+22-D3/2+eta.

Only J1/J2 can have a far-pair debit, at least-1. Only J1/J3 can
meet P1 or have an A boundary debit. Split into three exhaustive cases.

1. J3 meets P1. Then H_3=z-2, and (1) gives D3<=u+v+18. The
   previously proved bound DeltaPhi>=u+v+L/2+25-D3 immediately gives
   DeltaPhi>=L/2+7.

2. J3 does not meet P1, but J1 does. J1's far row is t; J2's is
   at most t-1. Thus the only possible far pair J1/J2 is absent.
   J1 has no A debit because it is below A's terminal. J3 also has
   no A debit: its far row is between a-7 and t-2, inside the J1
   bar's row range [a-10,t]. Its far interval starts left of b1.
   Reaching A's adjacent column s-L would cross (y3,b1), a J1
   endpoint. Therefore it stops before b1 and cannot meet A.
   The sole negative receipt group is J1/P1, bounded by -G1/2-1.
   Its far endpoint is at most s, so G1<=D1-u-12. The depth steps
   give D1<=D3-4. Substitution gives

       eta >= -(D3-u-16)/2-1,
       DeltaPhi >= u+v+L/2+29-D3 >= L/2+7.

   There is a further valid strengthening of this branch. J2's far
   row lies inside J1's continuing bar. Avoidance forces
   D2>=D1+G2+2>=D1+6, hence D3>=D1+8. The same ledger then gives
   DeltaPhi>=L/2+9>=12. It is not needed for the uniform bound (3).

3. Neither J1 nor J3 meets P1. Then eta>=-1-2=-3. Using
   D3<=u+v+22 gives DeltaPhi>=v/2+L/2+8>=L/2+14, which is
   stronger than (3).

The three cases introduce no new full-tile credit. All source charges,
upper receipts, pair/P1/rotor tile ownership certificates and directed
event partitions remain those of the accepted theorem. Thus no reserve
or full-tile credit is reused.

## Boundary controls and limitations

The former equality family has cavity width1 and cannot be complete.
Reducing its D3 and G3 each by2, with6<=L<=v-2, gives width3 and
exact joint L/2+5; that family also cannot be complete. The narrower
range is necessary: at L=v the modified J3 and J2 bars collide.
Reducing each by4 gives width5:

    J3=(z-2,u+v+18,v+6),

while leaving the first three originals as before, f6 and6<=L<=v-4.
The same coordinate separations and three far receipt groups give exact
joint L/2+7. This geometric family passes the NEW narrow-width constraint;
complete extendibility remains unproved. Thus (3) is not claimed sharp
over complete extensions. For u=v12,z24,L6 the three controls have joint
gains6,8,10 respectively, and free cavity widths1,3,5.

The first-P1-contact control
(6,44,4),(20,46,22),(6,52,4),(8,54,4), with u12,v20,z24,L6,f4,
has exact joint12, no far-pair event and no A debit. It tests the second
branch without assuming the existence of a complete extension.

The [full-original checker](../develop/check_secondary_ten_sealed_root_cavity.py)
tests entire walls, original-support membership, exact free connected
components, all eight orientations of the canonical shapes and the three
receipt cases. Finite controls supplement the general proof.
The [Lean source](../formal/SubQuorum/SecondaryTenSealedRootCavity.lean)
formalizes rectangle-path confinement, a connected-owner width obstruction,
canonical projection witnesses, retained-wall membership and budget arithmetic.
The H3 catalogue, actual-owner connectivity adapter and complete-prefix
classification are stated in the written proof; verification scopes are
recorded separately. Other additional-owner interactions, global allocation,
arbitrary-grid catalogue exhaustion, global5/6 improvement and rectangular-grid
triple equality remain OPEN.

The subsequent [width5 stack theorem](SECONDARY_TEN_WIDTH_FIVE_STACK.md)
classifies and accounts for every actual owner in that cavity. It closes
the cavity's support obligations, while global complete extendibility and
allocation among overlapping selected groups remain open.
