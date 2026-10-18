Please audit this new structural continuation of the accepted regular compensation theorem. Check the exact nonnegative remainder, the degree>=4 linear-equality implication, the necessity and sufficiency of the all-degree isolate-tight partition, and the bipartition/isolate imbalance claims. Preserve the stated distinction between a necessary partition and the extra maximum-dissociation condition. No priority claim is requested. Return ACCEPT/REVISE/REJECT and exact gaps.

# Residual stability and the structure forced by regular compensation equality

19 October 2026. This extends the cubic isolate-tight classification to
all regular degrees d>=3 and gives a new necessary structure for linear
compensation equality when d>=4. All graphs are finite, simple and
bipartite; forming sets are inclusion-minimal, with non-induced two-stars.
The complete exchange and degree-capacity proofs appear in
SHARP_REGULAR_BIPARTITE_GAP.md. No literature-priority claim is made.

## An exact nonnegative remainder

Fix a minimal selection S in a d-regular graph, d>=3. Use the chosen
injective high witness map f, good high vertices, leaves U, isolates I,
and the two explicit dissociation sets D_L,D_R from the exchange proof.
Put s=|S|, beta=beta_2(G), z=|I|, K=|U|-number of good high vertices,
and r_j=number of outside vertices of selected degree j not in f(H).
For each high vertex put

    q_v=d-a(f(v))-(a(v)-1)>=0,
    B=dn-(2d-1)s,
    W=dn+2beta-(2d+1)s.

All outside vertices have selected degree at least one. The exact
capacity identity and exact exchange-size sum give

    W=(beta-|D_L|)+(beta-|D_R|)+sum_H q_v
       +(d-2)r_1+(d-3)r_2
       +sum_(j=3 to d-1)(d-j)r_j+(r_1+r_2-K).              (1)

To check it directly, the capacity identity is
B=z+sum_H q_v+sum_(j=1 to d-1)(d-j)r_j, and the exchange sum is
|D_L|+|D_R|=2s-z-K. Subtract2s-2beta from B and collect terms.
Every term on the right of(1) is nonnegative, including the final term
by the injective leaf-witness budget. Thus(1) is a stability refinement
of the regular compensation inequality, not just an equality argument.

If d>=4 and W=0, the positive coefficients force r_1=r_2=0. The final
term forces K=0; all q_v vanish and every other unused positive capacity
vanishes. In particular

    B=z,
    |D_L|=|D_R|=beta.                                    (2)

The degree threshold is explicit: at d=3 the coefficient of r_2 in(1)
is zero, so this accounting alone cannot force r_2=0. This is a limitation
of that equality deduction, not a counterexample to the cubic theorem.

## Complete isolate-tight partition in every regular degree

For any d>=3, B=z if and only if G,S have the following partition.
Some classes may be empty.

- S consists of selected isolates I, selected matching vertices P,
  selected leaves U, and high classes A,C of selected degrees d-1,d.
- H=A union C induces a(d-1)-regular bipartite graph.
- Outside vertices split into X1,X2,Y of selected degrees one,two,d.
- The paths c--u--x give bijections C<->U<->X1; each c in C has one
  selected leaf, each u has one C and one X1 neighbor, and all its
  other d-2 neighbors lie in Y. Each X1 has no other selected neighbor.
- A<->X2 is a bijection through edges; each X2 has one A neighbor
  and one I neighbor. Every remaining I edge goes to Y.
- Each P vertex has its matching mate and d-1 neighbors in Y.
  Each Y has all d neighbors in I union P union U.
- The outside graph on X1 union X2 has degrees d-1 at X1 and d-2
  at X2. Y has no outside neighbors.

For necessity, B=z makes every high-witness surplus and every unused
capacity zero. A nonadjacent witness has selected degree one, so zero
surplus forces its good owner to have selected degree d. An adjacent
degree-one witness has surplus at least one, so is excluded. Every
remaining bad witness has selected degree two, with a high owner and
an isolate; zero surplus forces selected degree d-1 at that owner.
There are no unused degree-one or degree-two outside vertices, since
d>=3 makes both capacities positive. All unused vertices have selected
degree d. Thus X1 is exactly the good witness image, and X2 the bad image.

Every selected leaf has a distinct degree-one or degree-two witness.
A degree-two leaf witness belongs to neither high image and would
therefore have positive unused capacity. Hence every leaf uses X1,
and overlaps can only have its unique good support as owner. Every
good owner needs at least one leaf, so the resulting injections force
|U|=|C|=|X1| and the displayed bijections. In particular bad owners
have no selected leaves. Removing one leaf at each full-degree high
vertex leaves selected degree d-1 at every vertex of H. The remaining
selected degree-one vertices are precisely the matching vertices P.
The selected-neighbor descriptions and regular degrees force all other
neighborhood statements. This proves the full necessity assertion.

For sufficiency, every X1 vertex is covered through U--C, every X2
has its two selected neighbors, and every Y has d selected neighbors.
Deleting I or P uncovers the deleted vertex. Deleting an A vertex
uncovers its associated X2, now adjacent only to an isolate. Deleting
either c or its matched u uncovers the associated X1. Thus S is minimal.

Write b=|A|, h=|C|=|U|=|X1|, p=|P|, y=|Y|. Then

    dy=(d-2)h+(d-1)p+dz-b,
    s=z+p+b+2h,
    n=z+p+2b+3h+y.

Substitution gives dn-(2d-1)s=z. This proves sufficiency and exact
accounting. At d=3 the outside graph consists of X1 cycles and paths
with endpoints in X2, recovering the previous complete cubic theorem.

## Forced bipartition balance

Let b_L,b_R,h_L,h_R count the two high classes. The(d-1)-regular
selected high graph has equally sized parts, hence

    b_L+h_L=b_R+h_R.

The outside degree sums give

    (d-1)h_L+(d-2)b_R=(d-1)h_R+(d-2)b_L.

Combining these equations yields(2d-3)(b_L-b_R)=0. Since d>=3,

    b_L=b_R,  h_L=h_R,
    b<=2d min(|I intersect L|,|I intersect R|).              (3)

The last inequality follows from X2-to-isolate incidences, at most d
per isolate. It does not inject many distinct X2 demands into a single
isolate; the degree multiplicity is retained explicitly.

On this partition the exchanges perform no trimming. Their sizes are

    |D_L|=s-|I intersect L|,
    |D_R|=s-|I intersect R|.

Consequently every isolate-tight selection satisfies

    W>=abs(|I intersect L|-|I intersect R|).                (4)

Indeed beta is at least the larger exchange, while W=z-2(s-beta).
For d>=4, every linear equality selection W=0 must therefore have the
complete partition above and equally many isolates in the two parts.
Moreover both explicit exchanges are maximum dissociation sets.

Conversely, the partition with balanced isolates and maximum explicit
exchanges gives W=0 directly. The maximality condition is essential:
the partition by itself is not asserted to characterize equality of
the graph invariants. The uniform attaining families satisfy it by their
separate exact dissociation proofs.

## Relation to the connected sharp constructions

In the degree-d attaining graph and its d>=4 connected rings, C,U,P,Y
are empty. The class A is the selected high crown or its disjoint union,
X2 is all outside vertices, and every isolate uses all d edges at X2.
The exact local caps establish maximality of the two exchange sets.
Thus these families meet every zero term in(1), including isolate balance.

The conclusion does not classify every graph with beta=n/2, nor every
possible equality graph up to isomorphism. It supplies the complete
isolate-tight partition and the necessary structural reduction for
linear equality in degrees at least four. The cubic connected extremal
problem still requires an additional argument.

## Verification scope

The proof above is general. Independent controls inspect the partition,
both balances and exchange sizes on explicit regular families and on
small exact graph instances. Symbolic Lean checks are identified in
their receipts; they are not a full formalization of this partition.
This theorem was derived after both general-degree and connected-ring
Oracle inputs and is outside their reviews unless separately stated.
