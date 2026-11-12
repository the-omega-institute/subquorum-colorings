# Sharp odd-cycle phase compensation and the unrestricted8n/81 bound

12 November 2026. All graphs are finite, simple and bipartite; beta_2 is
unrestricted dissociation. Minimal two-star formation uses non-induced
K_(1,2) with exactly two selected vertices and inclusion-minimality.

**Theorem.** Every graph G of maximum degree at most three and every
minimal two-star-forming S satisfy

    |S|-beta_2(G)<=floor(8|V(G)|/81).

No connectivity, minimum-degree or selected-component hypothesis is used.
The coefficient improves19/192 by1/5184; graph sharpness is open.
The auxiliary phase-expectation coefficient1/3 proved below IS sharp.
These are different sharpness questions.

## 1. Template, retained owners and the first alternative

Use the partial template with layers I,C,X of sizes b,2b,2b: helper
neighbour pairs partition X; the owner matching C--X is perfect; F=H[C]
has maximum degree two; Q=H[X] is a partial matching. No other edges.
The original bipartition may be unbalanced. Auxiliary P pairs the two
witnesses at a helper, and is not a physical graph edge.

Each P union Q component is an alternating even path or a cycle of order
4ell. Let o count cycle components with odd ell. Each auxiliary component
has two equal proper phase classes. Independently choose one phase for
Y subset X; retain its complementary owners A subset C. Then |Y|=|A|=b,
and I union Y union Z is dissociation for every dissociation Z of F[A].
Each owner phase class U is retained wholly or omitted wholly, with fair
probability1/2. There are2o distinguished classes of order2ell=2mod4.
All owner classes partition C; other class sizes need not be even.

The accepted two one-core-side constructions have base sizes summing5b.
Their cycle gain is floor(ell/2), and each auxiliary path with h helper
pairs contributes at least h/4 to the average gain. Consequently their
maximum gives

    beta_2(H)>=5b/2+b/4-o/2.                             (1)

The explicit compatible choices, degenerate loop/parallel quotients and
unbalanced base calculation are in ODD_AUXILIARY_CYCLE_COMPENSATION.md.

## 2. Pairing a retained core cycle with a broken phase

Write T(A)=beta_2(F[A])-2|A|/3. Paths contribute nonnegatively to T.
A residual cycle must be a full component K of F, because its vertices
use both core degrees. Let its even order be m.

If K contains opposite literals of the same phase bit, it can never be
fully retained and always leaves paths. It contributes nonnegatively.
Otherwise its full-retention event E0 specifies k distinct fair bits.
Partition its vertices by these phase classes, with positive group sizes
n_1,...,n_k. Then Pr(E0)=2^-k. If m=0mod3, its full cycle also has zero
T contribution, so it needs no correction.

For m=1 or2mod3 let delta be2/3 or1/3, respectively. The full cycle has
T=-delta. Flip a nonempty proper set J of its specified bits, leaving
a total r=sum_(j in J)n_j omitted vertices. The resulting event EJ has
the same probability2^-k as E0. It leaves only paths. Their total
rounding surplus is at least

    ceil(2(m-r)/3)-2(m-r)/3.                             (2)

The following choices completely classify the needed correction.

* If m=1mod3 and a group has size2mod3, flip that group. If instead
  two groups have size1mod3, flip both. In either case r=2mod3,
  and(2) is2/3, cancelling delta.
* If m=1mod3 and neither choice exists, exactly one group has size1mod3
  and all others have size0mod3. When k>=2, flip one0mod3 group.
  It has at least three vertices, is a proper subset, and(2) is1/3.
  Half the full-cycle deficit remains. When k=1, no positive surplus
  is paired to the full cycle.
* If m=2mod3 and k>=2, a0mod3 group can be flipped to give(2)=2/3,
  or a1mod3 group to give(2)=1/3. If all groups have size2mod3, their
  number is1mod3, hence at least four; flip two. Again(2)=1/3.
  Thus delta is fully cancelled. For k=1 no surplus is paired.

Let gamma be the cancellation amount, capped at delta. For each cycle
use the score gamma*1_EJ-delta*1_E0, omitting the EJ term when gamma=0.
Pointwise its T contribution is at least this score: on E0 the deficit
is exact; on EJ use(2); every other nonfull event leaves paths.
Different core components are physically disjoint, so scores add even
when they depend on the same phase bit.

Let rho=sum_K(delta-gamma)2^-k. Then

    E[beta_2(F[A])]>=2b/3-rho.                           (3)

Only two kinds of positive losses remain:

1. A monochromatic core cycle, wholly within one owner phase class U.
   Its loss is delta/2, at most m/12. For C4 the loss is exactly1/3=m/12.
   Every other even cycle has slack at least1/2 between m/12 and its
   loss: check m6,8,10 and then use delta/2<=1/3 for m>=10.
2. A nonmonochromatic exceptional cycle from the second bullet, with
   k>=2, one group of size1mod3 and every other group of size0mod3.
   Its loss is(1/3)2^-k<=1/12. Assign it to ONE of its0mod3 groups,
   using at least three vertices of that group. Such a group exists.

No cycle loss is assigned twice.

## 3. Owner-class budgets and the two-singleton case

Fix an owner phase class U. Remove its monochromatic core cycles and
let r_U be the number of its remaining vertices. Let q_U count the
nonmonochromatic exceptional losses assigned to U. Their supporting
groups lie in different full core components, so their vertex sets
are disjoint. Thus3q_U<=r_U.

If U is not distinguished, its total charge is at most

    (|U|-r_U)/12+q_U/12<=|U|/12.                         (4)

Suppose U is distinguished, so |U|=2mod4. If one of its monochromatic
cycles is not C4, the slack at least1/2 described above gives a charge
at most |U|/12-1/2, and hence at most(|U|-2)/12.
If every monochromatic cycle is C4, then r_U=2mod4 and r_U>=2.
For r_U=2 we have q_U=0. For r_U>=6,

    q_U<=floor(r_U/3)<=r_U-2.

The charge is again at most(|U|-2)/12. This argument includes a class
whose only internal defective components are TWO ISOLATED VERTICES;
no assumption that its two defects are endpoints of a single path is used.

Sum(4) and the distinguished budgets over the partition of C. Each
core vertex is allocated to exactly one class; each exceptional cycle
is charged to one disjoint supporting group. There are2o distinguished
classes and |C|=2b. Therefore

    rho<=2b/12-(2o)*2/12=b/6-o/3.                       (5)

Equations(3)--(5) prove the sharp phase-expectation lemma

    E[beta_2(F[A])-b/2]>=o/3.                            (6)

This is a general counting proof; no enumeration is a premise.

## 4. Construction, optimal phase coefficient and the template lemma

Each E0 or EJ is a conjunction of specified component bits. Its
conditional probability is zero if an already fixed bit conflicts,
and otherwise2^-f, where f counts its unfixed specified bits. Thus
conditional expectations of the sum of cycle scores are exact and
polynomial-time computable. Fix successive bits without decreasing
that expectation, then optimize the actual residual paths/cycles.
The resulting set satisfies beta_2(H)>=5b/2+o/3.

Together with(1), take the maximum of the alternative actual sets.
A convex combination with weights2/5,3/5 cancels o and yields

    beta_2(H)>=5b/2+(2/5)(b/4-o/2)+(3/5)(o/3)
             =13b/5.                                  (7)

These guarantees are compared; no incompatible sets are united.
Integrality gives ceil(13b/5).

The connected30-vertex fixture has b6 and o3. Its core consists of two
C6s. In phase000 it leaves the two paths(21,19,25) and(27,29,23).
The core permutations(18 19)(20 21) and(26 27)(28 29) flip the two outer
phase bits separately. The core automorphism

    (18 26)(19 27)(20 28)(21 29)(22 23)(24 25)

exchanges the outer bits and flips the middle bit. These permutations
preserve all core edges and act transitively on the eight phase vectors.
Thus EVERY phase leaves2P3 and gives surplus1=o/3. Disjoint unions of
k copies give surplus k with o3k, proving sharpness of the constant1/3
in(6). The fixture also supplies a17-set while every phase construction
has size16; this rules out optimality of the phase restriction, at every
scale by taking unions. It does not assert that13/5 is graph-sharp.

## 5. Unrestricted lifting and its exact certificate

Use the same fixed witness decomposition as in the preceding19/192
proof: |S|=|R|+2p+u, counts a,b,b3, and b'=b-b3 h=2 helpers. Both
chosen centres and chosen selected leaves have been removed before
allocating residual owner--witness pairs. The exact induced partial
template has b' helpers. Every certificate in it can be enlarged
simultaneously by L=|R|-b'+p vertices from retained R and chosen leaves.
Their complete cross-edge exclusions are proved in the cited notes.

For d=|S|-beta_2, set m=min(a,p), alpha=a-m, pi=p-m,
 e=u-a-2b, r=|R|-a-b, q=n-|S|-p-u, tau=m+b-2d.
All these slacks and e-b3 are nonnegative. The fixed ledger is

    n-10d=r+m+3alpha+3pi+2e+q+5tau.

By(7), Z=5beta_2(G)-5L-13b'>=0. Substitution gives

    d+Z=8m+5alpha+5pi+2tau+5e+8b3,

    8n-81d=Z+8r+19alpha+19pi+3e
                  +8(e-b3)+8q+38tau>=0.                (8)

This proves the theorem for every minimal S, hence for SF_2. Empty
cores/templates satisfy the same formulas. No connectivity, positive
minimum degree, selected-star or regularity assumption was inserted.
The existing square correction and core-girth hierarchy remain valid
additional instance-dependent certificates. Neither a new grid theorem
nor cubic specified-star existence follows from this result.
