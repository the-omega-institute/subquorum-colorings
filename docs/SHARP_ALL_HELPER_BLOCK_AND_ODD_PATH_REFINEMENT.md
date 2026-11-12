# Sharp all-helper block and the odd-owner-path refinement

12 November 2026. Complete proofs are integrated in
[the working manuscript](../manuscript/sharp-all-helper-proof.tex).

## Exact obstruction to a stronger all-helper estimate

There is a connected bipartite physical partial template H with b=6 helpers,
30 vertices, 42 edges, minimum degree two and maximum degree three, satisfying

    beta_I(H)=16=8b/3,      beta_2(H)=17.

For r disjoint copies these optima are16r and17r. Thus the proposed universal
all-helper estimate beta_I>=11b/4 is false; any valid universal coefficient in
beta_I>=c b is at most8/3. Forcing all helpers can incur unbounded additive loss
within templates of minimum degree two. The copies are disconnected for r>1.
This does not refute either general8b/3 question, which remains open.

The [coordinate fixture](../develop/fixtures/sharp-all-helper-thirty.json)
specifies P,Q and the two owner six-cycles, colours and both optimum witnesses.
It is a different physical graph from owner-matching-obstruction.json. In that
earlier graph beta_I=17 and a further one-owner-per-matching-edge restriction
has optimum16. In the present graph the all-helper problem itself has optimum16.

For the all-helper upper bound, matching cost at most one in the three
auxiliary squares can be enlarged to a three-set in one square and an opposite
pair in each other square. All three possible charged locations force an owner
three-vertex path in the complement. The proof groups the48 maximal cases
structurally instead of relying on their enumeration.

For unrestricted beta_2, divide the physical graph into three ten-vertex blocks.
The two outer blocks each contribute at most six; every six-set contains an
owner edge. A selected adjacent central owner therefore lowers that outer cap
to five. The central block contributes at most four, six or seven according to
whether its owners meet zero, one or both of the two attachment pairs. Totals
are at most16,17,17 respectively, and an explicit17-set attains the bound.
The disjoint-union statement follows from the restriction-and-union principle.
No universal SF coefficient improvement is inferred from this construction.

## Keeping the odd-path surplus in the final ledger

Fix a minimal two-star-forming set S and an actual disjoint witness extraction,
with b' template helpers and a separate retained set of size L. Suppose the
specified owner matching family has a K4-free choice; let o be the number of
odd-order owner paths. The existing owner-matching theorem gives

    Z=3beta_2-3L-8b' >= o/2.

If0<=gamma<=1 and o>=2gamma b', the exact witness identities yield

    (5+gamma)n-(51+12gamma)d
      =(Z-gamma b')+(5+gamma)(r+q)+(12+3gamma)(alpha+pi)
        +(7+2gamma)(e-b3)+(2+gamma)b3+(24+6gamma)tau >=0.

Here d=|S|-beta_2 and all terms have their previously defined nonnegative
fixed-extraction meanings. The full proof defines the substitution and verifies
the sign of each term. Thus

    d <= floor((5+gamma)n/(51+12gamma)).

At gamma0 this is5/51; at gamma1 it is2/21. To bound SF_2-beta_2 the hypothesis
must hold for a maximum-cardinality minimal forming set. This is a conditional
class refinement, not a new unrestricted maximum-degree-three coefficient.
Its proof is an algebraic consequence of the earlier odd-path and witness
theorems, not an additional independent surplus resource.

## Verification and scope

Run `python3 -B scripts/check_sharp_all_helper.py`. The deterministic report is
[output/sharp-all-helper-check.json](../output/sharp-all-helper-check.json).
The controls include:

- 102,097 feasible literal owner/witness choices and all48 maximal cost-one
  cases, independently of the matching optimizer.
- All3,072 subsets of the three ten-vertex blocks, including the necessary
  owner-edge property of every outer six-set.
- Exact unrestricted optima from each physical bipartition side:32,768 subsets
  per side on the30vertex graph. The private-neighbour optimizer is separately
  checked on all689 binary bipartite graphs with both sides of order at most3,
  using37,477 literal physical subsets. Total one-part evaluations across the
  full run:239,550.
- 3,340 actual physical extractions,16,663 exact-rational ledger comparisons,
  including two with positive odd-path count, plus749 generated numerical
  identities satisfying the ledger hypotheses. The numerical identities are
  not asserted to be graph realizations.
- Ten nonempty-template graph controls and the canonical18-set's literal
  formation/deletion checks. No exact SF optimum is asserted by this checker.

The preceding owner-matching checker is also rerun unchanged, with its report
compared byte-for-byte. The exact independent review, execution scope and source
manifest are recorded in output/sharp-all-helper-review.json when complete.
General all-helper and unrestricted8b/3, the sharp subcubic interval[1/20,7/71],
multiple-Hall geometric routing, universal unit5/6 and arbitrary-width grid
triple equality remain open. October's submitted manuscript is preserved.
