# Zero-budget repairs exclude every positive8n/81 equality

12 November2026. All graphs are finite, simple and bipartite. beta_2 is
unrestricted dissociation. A minimal two-star-forming set is inclusion-minimal;
formation uses a not necessarily induced K_(1,2) with exactly two selected
vertices. All preceding witness and phase definitions are as in
SHARP_ODD_CYCLE_PHASE_COMPENSATION.md and
PHASE_BUDGET_EQUALITY_AND_METHOD_CEILING.md.

**Theorem.** Every nonempty maximum-degree-three graph G and every minimal
two-star-forming S satisfy

    81(|S|-beta_2(G))<8n,
    SF_2(G)-beta_2(G)<=floor((8n-1)/81).                    (1)

This excludes every positive unrounded equality, including orders162k
left unresolved by the preceding parity argument. It is an integer
improvement at every positive multiple of81, not a smaller asymptotic
coefficient. The sharp asymptotic graph coefficient remains open.
The proof does not decide whether an isolated template can attain13b/5.

## 1. Two additional resources when the phase budget is zero

Use a partial template H with |I|=b, |C|=|X|=2b, core F=H[C]
of maximum degree two and possibly partial interface matching Q on X.
The auxiliary P union Q components are even paths or cycles of order4ell.
Their two owner phase classes partition C. Let o count odd-ell cycles.
The accepted exact budget is sigma=b/6-o/3-rho.

Assume sigma=0. The accepted zero-set theorem says every ordinary class
is partitioned into whole monochromatic core C4 components. Each of the
2o distinguished classes has such C4s plus exactly two remaining vertices.
In particular any physical core path uses only these remaining vertices;
no owner class contains more than two vertices of all such paths together.
Whole core C4s have used both core degrees and cannot meet these paths.

Let b_O count helpers belonging to ordinary auxiliary components, meaning
paths and even-ell cycles. Let t count all path components of F, including
isolated vertices. Then

    beta_2(H)>=ceil((52b+3b_O+t)/20).                      (2)

The proof gives actual polynomially constructible dissociation sets.

**Ordinary-component replacement.** Both owner classes of an ordinary
auxiliary component are partitioned into whole core C4s. Thus its owner,
witness and helper vertices have no edges to other template components:
core edges stay in those C4s, interface edges stay in the auxiliary
component, and helper and owner incidences are internal. A phase set
within it always has size5b_j/2: it retains b_j owners in whole C4s,
with dissociation number b_j/2, plus b_j helpers and b_j witnesses.
Its class sizes force b_j divisible by4.

The optimized one-core-side quotient alternatives have average at least
11b_j/4. On an even-ell cycle their two quotient gains sum to b_j/2;
on a path b_j is divisible by4, its two side quotient orders are b_j/2,
and their gains also sum to b_j/2. The two base sizes sum to5b_j.
Choose the larger alternative separately in each ordinary component.
Replacing its phase restriction therefore gains at least b_j/4.
These replacements are compatible with all choices in the remainder.

**Path credit.** Fix one endpoint v of a physical path component K of F.
Let L(v) denote its retention literal. If v is isolated, retaining v
leaves a P1 at that endpoint. If its neighbour u has a different literal,
retain v and omit u, again leaving P1. These requirements are consistent:
when both involve the same bit they are opposite literals; otherwise
there are two independent bits.

If u has the same literal as v, retain both. A possible next vertex z
cannot have that literal, because only two remaining vertices of its
class exist globally. Omit z if it exists; if not the whole path is P2.
The requirements involve at most two fair bits and are again consistent.
Thus an event of probability at least1/4 leaves an endpoint P1 or P2.
Their rounding surpluses above2|V|/3 are1/3 and2/3, respectively.
Every other residual piece of this full physical path is also a path
and has nonnegative rounding surplus. Its expected surplus is therefore
at least1/12. The isolated case has probability1/2 and is stronger.

Different physical path components have disjoint vertices. Their events
may use the same phase bits; linearity of expectation still adds the
credits. The cycle-pairing scores apply only to full physical cycle
components, so none of their resources overlaps a path credit.

Ordinary replacements and the cycle-pairing/path-credit construction on
the remaining odd auxiliary components give an actual alternative of size
at least

    5b/2+o/3+b_O/4+t/12.                                 (3)

All events specify at most two bits, in addition to the already accepted
cycle events. Exact conditional expectations fix the remaining phases
without decreasing the score, then optimize residual paths and cycles.
The global one-core-side alternative still gives11b/4-o/2. Comparing
actual alternatives with weights3/5 for(3) and2/5 for that alternative
cancels o and proves(2). Their selected vertices are never united.

## 2. What actual template equality would force

If b>0 and beta_2(H)=13b/5, then sigma=0 by the accepted strengthened
certificate. The old one-side and phase bounds imply, respectively,

    o>=3b/10 and o<=3b/10,

so o=3b/10. More importantly(2) forces b_O=t=0. Consequently:

* Every auxiliary component is an odd-ell cycle, so Q covers all X.
* Every core component is a cycle, so all C vertices have core degree2.

Every X vertex now has its helper, its owner and its Q partner as three
internal neighbours. Every C vertex has two core neighbours and its owner
witness as three internal neighbours. All C and X vertices have exhausted
the maximum-degree-three capacity in any ambient graph.
This is a necessary template-equality structure, not a proof that such
an equality template exists or is impossible.

## 3. Equality in the original graph is impossible

Suppose for contradiction that81d=8n>0 for a minimal S, where
 d=|S|-beta_2(G). Use the original fixed witness extraction and its
accepted nonnegative ledger

 8n-81d=Z_sigma+3sigma+8r+19alpha+19pi+3e
                       +8(e-b3)+8q+38tau.

All terms vanish. In particular e=q=b3=0, a=p=m>0, and the already
proved exact counts, before the parity refinement, give

 b=15m, n=81m, |S|=49m, beta_2(G)=41m,
 |R|=16m, u=31m, b'=b.

Let H=G[I0 union C0 union X0] be the extracted template. Retaining all
R minus I0 and all chosen triple leaves adds exactly
L=|R|-b+p=2m to EVERY dissociation set in H. Therefore

    13b/5<=beta_2(H)<=beta_2(G)-L=39m=13b/5.

The template equality is exact. Section2 forces all C0 and X0 vertices
to use three internal neighbours, so neither has an ambient edge leaving H.

There can be no extra neighbour of an I0 helper either. It is isolated
in S. Since q=0, every outside vertex is one of the chosen pair witnesses
or one of the chosen triple witnesses. A triple witness has selected
neighbourhood exactly its chosen leaf, so cannot meet I0. Every chosen
pair witness adjacent to i contributes to h(i), which is exactly two
for i in I0. Both such witnesses are already in X0. Thus every helper
has degree exactly two, all within H.

Consequently H is a union of entire components of G. The remaining
induced graph G' has

    |V(G')|=81m-5(15m)=6m.

As a bipartite graph it has an independent, hence dissociation, set of
size at least3m. Its vertices have no edges to H. Unite that set with
a maximum dissociation set of H to obtain

    beta_2(G)>=39m+3m=42m>41m,

a contradiction. This uses neither minimality in G' nor a new gap theorem
for G'. The independent-set lower bound alone suffices.
Thus equality is impossible. The already proved weak81d<=8n and the
integer positive deficit8n-81d>=1 give(1). The empty graph is excluded
from(1); its difference is zero. No equality-graph existence claim,
smaller real coefficient, cubic specified-star existence or new grid
triple equality is inferred.
