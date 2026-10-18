# Augmented exchanges: every extra leaf pays for itself

19 October 2026. All graphs are finite and simple; two-star formation
is non-induced, and minimality is by inclusion. The result below has
no degree or connectedness assumption. It strengthens the exchange
lemma in [the regular bound](SHARP_REGULAR_BIPARTITE_GAP.md) and resolves
the cubic equality obstruction identified in
[the path normal form](CUBIC_EQUALITY_PATH_NORMAL_FORM.md).
No literature-priority claim is made.

## Isolate compensation in every bipartite graph

Theorem. If G is bipartite and S is a minimal two-star-forming selection,
write s=|S| and let z be the number of isolated vertices in G[S]. Then

    2s<=2beta_2(G)+z.                                     (1)

More precisely, two explicit dissociation sets E_L,E_R have total size
2s-z. Thus beta_2(G)>=ceil(s-z/2). The number of selected isolates,
rather than a loss for unreserved leaves, pays for the possible gap.

Proof. Use the established injective high-failure map f:H->T, where
T=V minus S. Partition selected vertices into isolates I, selected
matching vertices P, high vertices H and their leaves U. An adjacent
high witness has selected neighborhood {h} or {h,i}, with i in I.
A nonadjacent high witness has a unique selected neighbor g_h, a leaf
whose unique selected support is h. Call the latter owner good and
reserve g_h at each good high. Put F=f(H), let Ue be the unreserved
leaves, and K=|Ue|. Distinct good highs have distinct reserved leaves.

No extra leaf u in Ue is adjacent to F. Indeed an adjacent high witness
has only its high owner and possibly an isolate as selected neighbors.
A nonadjacent high witness has only its designated reserved leaf as a
selected neighbor. These exhaust the selected neighborhoods at F.

For each u in Ue choose its adjacent deletion-failure witness x_u. The
leaf-witness lemma gives selected neighborhood {u} or {u,i_u}, where
i_u is an isolate. Distinct leaves have distinct witnesses. Since u
has no neighbor in F, x_u is unused by the chosen high map.

Fix a bipartition L,R. The original exchange D_L retains P, all leaves,
I in R, H in L and F in R, trimming all leaves at retained bad highs
and all but the reserved leaf at retained good highs. Define D_R by
reversing colors. The established exchange proof verifies that both
are dissociation sets and

    |D_L|+|D_R|=2s-z-K.                                  (2)

If u in Ue lies in L, its support is in R and is omitted from D_L.
Thus u survives trimming. It has no other selected neighbor and no
neighbor in F, so it is isolated in G[D_L]. Its witness x_u lies in R
and is absent from D_L, since it is unused by f. The only neighbor
of x_u in D_L is u: its possible other selected neighbor i_u lies
in I intersect L and is omitted, while every outside neighbor of
x_u lies in T intersect L and is omitted too.

Consequently adding x_u pairs it with the previously isolated u.
Add all these witnesses simultaneously:

    E_L=D_L union {x_u:u in Ue intersect L},
    E_R=D_R union {x_u:u in Ue intersect R}.

Within each augmentation, all added vertices have the same color,
so there are no edges between them. Their leaf partners are distinct.
Each added vertex meets the old exchange only at its isolated partner.
Thus the new edges form mutually disjoint pairs, with no conflicts
with the old matching, and E_L,E_R are dissociation sets. Every extra
leaf contributes exactly once to their total size, so

    |E_L|+|E_R|=|D_L|+|D_R|+K=2s-z.

Bounding both by beta_2 proves (1). This proof also covers empty high
or leaf classes and disconnected graphs. No unused outside vertex is
counted twice within an augmentation, and no selected isolate is added
in place of several demands. The two exchanges are alternative feasible
sets, whose sizes are averaged; they are not asserted to be disjoint.

The subsequent [four-port padding rings](CUBIC_EQUALITY_PADDING_RINGS.md)
attain (1) on two-connected cubic bipartite graphs with z=2r and gap r
for arbitrarily large r. Thus the isolate coefficient1/2 is sharp even
with connectedness, cubic regularity and unbounded gap. That construction
has its own written proof and separate review scope; it was developed
after the accepted review of the present compensation theorem.

## A stronger exact regular remainder

For d-regular bipartite G, d>=3, put a(v)=|N(v) intersect S| and
q_h=d-a(f(h))-(a(h)-1), and define

    B=dn-(2d-1)s,
    W=dn+2beta_2(G)-(2d+1)s.

The established capacity identity is

    B-z=sum_H q_v+sum_(x in T minus F)(d-a(x))>=0.

Using the augmented size sum gives the exact, entirely nonnegative identity

    W=(beta_2-|E_L|)+(beta_2-|E_R|)+(B-z).                 (3)

In particular W>=B-z. The former cubic r_2 coefficient obstruction
disappears because the unreserved leaves have now been paid for by
actual additions to feasible dissociation sets.

Corollary. For **every d>=3**, linear compensation equality W=0 forces
B=z and both augmented exchanges to be maximum. The full isolate-tight
partition from [the existing equality theorem](REGULAR_COMPENSATION_EQUALITY.md)
therefore applies in degree three as well as in higher degrees. In this
partition K=0 and E_L=D_L,E_R=D_R; each high vertex has d-1 high neighbors,
the two high classes have balanced colors, and selected isolates must
be balanced in each connected component. Conversely that partition,
balanced isolates and maximum explicit exchanges imply W=0.

Here is the componentwise balance justification. In a connected component
Q let b_L,b_R count high vertices of selected degree d-1, and g_L,g_R
those of selected degree d. With Delta b=b_L-b_R and Delta g=g_L-g_R,
handshaking in the high and outside graphs gives respectively

    Delta b+Delta g=0,
    (d-1)Delta g-(d-2)Delta b=0.

Thus both differences vanish. The local exchanges then have sizes
s_Q-z_L and s_Q-z_R. If both global exchanges are maximum, each
restriction is maximum in Q, since a better local set would improve
the corresponding global set. Their local sizes are equal, so z_L=z_R.

For cubic graphs the high graph is therefore a union of even cycles.
There can be no high path, including an isolated high vertex, at linear
equality. This completes the equality-structure reduction, with the
maximum-exchange condition still essential. It does not classify all
graphs satisfying that global optimality condition.

## Quantitative path compensation and component debt

In the zero-accounting-remainder cubic normal form, let c be the number
of high path components. The disjoint witness count proves K=2c and
B-z=2c. Thus (3) implies the general, all-order path penalty

    3n+2beta_2-7s>=2c.                                    (4)

In particular the connected n=28,s=16,z=2 examples have beta_2>=15
for every admissible outside wiring. This conclusion is a graph proof,
independent of the finite control histogram.

There is also an exact refinement of the signed debt identity. Let
Delta z=z_L-z_R and Delta h=|H3 intersect L|-|H3 intersect R|. Let
t_L,t_R count extra leaves by their high support's color. Write b_L,b_R
for the H2 counts, Delta b=b_L-b_R and Delta t=t_L-t_R. The normal
form gives Delta b=-4Delta h and Delta t=-6Delta h. The original
exchange sizes are s-z_L-t_L+Delta b and s-z_R-t_R-Delta b. The L
augmentation adds t_R vertices, and the R augmentation adds t_L.
Consequently

    |E_L|=s-z_L+2Delta h,
    |E_R|=s-z_R-2Delta h,
    |E_L|-|E_R|=-(Delta z-4Delta h).

Put Mplus=max(|E_L|,|E_R|). Substituting into (3) gives

    W=2c+|Delta z-4Delta h|+2(beta_2-Mplus).                (5)

Applying this within each connected component Q gives

    W>=2c+sum_Q |Delta z_Q-4Delta h_Q|.                    (6)

More precisely, put Mplus_Q=max(|E_L intersect Q|,|E_R intersect Q|).
The componentwise exact identity is

    W=2c+sum_Q |Delta z_Q-4Delta h_Q|
       +2(beta_2(G)-sum_Q Mplus_Q).

The final term is nonnegative because choosing the larger exchange
independently in each connected component gives a dissociation set
of size sum_Q Mplus_Q in G.

The path witnesses are distinct globally, their matching augmentations
are compatible locally, and the componentwise absolute values exclude
cancellation of opposite color debts across graph components. These
are components of G; high paths within one connected component may
still interact through its remaining vertices.

## Verification and provenance

The original Oracle response to the precise cubic path question supplied
the simultaneous extra-witness augmentation on the zero-remainder normal
form and the inequality W>=2c. Its graph argument was independently
checked against every edge type above. The extension to arbitrary
bipartite graphs in (1), the regular remainder (3) and the refined
component debt (5)--(6) were derived locally after that response.
They are outside the original response's scope. The follow-up review
in the same conversation returned ACCEPT for the general theorem,
regular remainder, equality reduction and component debt, independently
of finite controls or Lean arithmetic. Its three requested presentation
clarifications, concerning a,q,b,Delta t and componentwise balance,
are incorporated above. No substantive mathematical gap was identified.

- [Original response](reviews/2026-10-19-cubic-equality-path-response.txt)
  and [provenance receipt](../output/cubic-equality-path-oracle-question.json).
- [Direct Lean source](../formal/StarForming/CubicPathAccounting.lean):
  two general graph lemmas, including simultaneous isolated-pair
  augmentation, and ten conditional arithmetic lemmas. The augmentation
  graph theorem uses no axioms. The full witness construction, finite
  cardinal sums and equality partition remain written proofs.
- [Formal receipt](../output/cubic-path-accounting-formal-check.json):
  twelve audited declarations pass local Lean4.33.0 after memory/process
  preflight and sequential compilation, with no nonstandard axioms.
- [General finite controls](../output/regular-compensation-controls.json):
  906 graphs, 403,976 subsets, 9,775 minimal selections, 19,550 augmented
  exchanges and 4,854 actual extra-leaf additions. These include arbitrary
  bipartite graphs, all sizes through the displayed exhaustive families,
  irregular and disconnected cases, and the regular sharp constructions.
- [Path controls](../output/cubic-path-accounting-controls.json): 340 new
  instances and seven existing controls. The explicit 28-vertex obstacle
  to the unaugmented balance rule is written out in the normal-form note.

Reproduce with

    python3 scripts/check_regular_compensation.py --output output/regular-compensation-controls.json
    python3 scripts/check_cubic_path_accounting.py --output output/cubic-path-accounting-controls.json

Finite controls support the constructions; they do not replace the
general proofs. The overall sharp order coefficient is unchanged, as
the known attaining families already have no extra leaves. The optimal
unbounded connected cubic coefficient and the rectangular-grid triple
equality remain open. No improvement of the grid five-sixths estimate
or change to the submitted manuscript is claimed.
