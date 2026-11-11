# The sharp gap for minimal forming sets with selected star components

Let G be a finite simple bipartite graph of order n. A two-star-forming
set S forms every outside vertex using two distinct selected vertices
and a not necessarily induced K_(1,2). Write beta_2(G) for the maximum
cardinality of a dissociation set, a set inducing maximum degree at most
one.

**Theorem.** If S is inclusion-minimal two-star-forming and the components
of G[S] are stars, edges or isolates, then

    |S|-beta_2(G)<=floor(n/12).                       (1)

The coefficient is sharp, including among connected bipartite graphs
of maximum degree six. No private leaf witness is required at every
centre. The previously established connected 24r-vertex family has
minimal selected size 16r and beta_2=14r, and attains (1).

The result concerns the specified minimal set S. It does not assert that
every graph has a maximum-cardinality minimal forming set of this form.
The general bipartite SF_2-beta_2 bound n/10 remains a separate theorem.

## Chosen witnesses and their distinct resources

Partition S into star centres C, their leaves L, selected isolates I,
and vertices P of selected edge components. Centres refer to stars of
order at least three. Put

    c=|C|,   e=|L|=2c+s,   s>=0,   R0=I union P.

Call a selected vertex active if it has a selected neighbour. In a
bipartite graph an outside x is formed exactly when it has two selected
neighbours, or has one selected neighbour that is active. Formation is
upward closed; thus inclusion-minimality is equivalent to failure of
every single deletion, including failure at the newly omitted vertex.

For every leaf ell, deleting ell leaves its centre active and leaves the
newly omitted ell formed by its centre and another leaf. Therefore an
originally outside vertex must fail. Its selected neighbourhood is

    {ell},   or   {ell,i} with i in I.               (2)

Indeed, after deletion it has either no selected neighbour or a sole
inactive neighbour. In the latter case that neighbour was already a
selected isolate: the only selected neighbour of ell is its centre,
which stays active. Each such witness has exactly one active owner ell.

Say a centre has a clean leaf if some leaf ell has an outside witness
with N_S(w)={ell}. Let p be the number of centres with a clean leaf, and
q=c-p. Choose a private witness at one leaf of each of the p centres,
and one witness of form (2) at every other leaf.

Every one of the remaining q centres has a direct deletion witness with
selected neighbourhood

    {centre},   or   {centre,i} with i in I.         (3)

To see this, deleting a centre leaves the newly omitted centre formed
by two leaves. An outside failure adjacent to the centre has form (3).
If the failure is not adjacent to it, its selected neighbourhood did not
change. It must have had a unique selected neighbour that became
inactive, namely a leaf of this centre. This would be a clean leaf,
contrary to the definition of q.

Let W consist of the e chosen leaf witnesses and these q centre
witnesses. All are distinct: each has exactly one active selected owner,
and all owners in this choice are different. Each chosen witness touches
at most one selected isolate, and at least p of them touch none.
For i in I let h(i)=|N(i) intersect W|, and put

    a=#{i:h(i)=1},   b2=#{i:h(i)=2},
    b3=#{i:h(i)>=3},   t=a+b2+b3.

Counting isolate incidences and then vertices gives

    a+2b2+3b3<=e+q-p=c+s+2q,                         (4)
    n>=c+2e+q+t=5c+2s+q+t.                          (5)

All selected edge vertices, untouched isolates and unused outside vertices
add to the right side of (5). No isolate is counted more than once there.

## The leaf exchange

Using only the e leaf witnesses, the standard colour-cover exchange gives

    beta_2>=|S|-c+ceil((e-t_leaf)/2),                 (6)

where t_leaf counts distinct isolate helpers of those leaf witnesses.
For completeness, keep all leaves and selected edge components and
remove all centres. In the auxiliary graph on leaf witnesses and all
selected isolates, a retained witness already sees its leaf and cannot
retain any auxiliary neighbour. Conversely every auxiliary independent
set gives a valid dissociation set together with those leaves and edges.
If the two witness colour classes have sizes e_A,e_B and touch t_B,t_A
isolates, the covers W_B union I_B(touched) and W_A union I_A(touched)
have average size (e+t_leaf)/2. Their independent complements yield (6).

Write d=|S|-beta_2(G). Since t_leaf<=t, equation (6) implies

    t>=2d+s.                                        (7)

Together with (4), this proves our first ledger inequality:

    B0:=c+2q-b2-2b3>=2d.                             (8)

## Compatible repairs using isolates touched exactly twice

Fix the original bipartition A,B and put T=S union W. The sets

    E_A=(T intersect A) union
        ((R0 intersect B) minus {i in I:h(i)>=2}),    (9)

and the set E_B obtained by reversing colours are dissociation sets.
All selected active vertices from the opposite colour are omitted.
A retained edge-component vertex sees only its original mate; no chosen
witness has an active owner in R0. A retained opposite-colour isolate
touches at most one chosen witness, and every chosen witness touches at
most one such isolate. These observations verify all possible edges.
Their total size is

    |E_A|+|E_B|=|T|+|R0|-(b2+b3)
                 =2|S|-p-b2-b3.                    (10)

Construct a bipartite multigraph Gamma with one side C and the other
side the isolates with h=2. For each leaf ell whose chosen witness
touches such an isolate i, put an edge from its star centre to i,
labelled by ell and its witness. Parallel edges are retained. This
graph splits into C_A--I_B and C_B--I_A. Let their matching numbers be
mu_A,mu_B and put mu=mu_A+mu_B=nu(Gamma).

Take a maximum matching in C_A--I_B. For each matched edge labelled
ell,w_ell, remove w_ell from E_A and add ell and its helper i. This
gains one vertex per matching edge, simultaneously. The reasons are:

* The retained centre was isolated in E_A. Its one new leaf sees that
  centre and no other retained vertex: its only chosen witness was
  removed, and every chosen witness has just one active owner.
* The newly retained helper i has exactly two chosen witness neighbours.
  One was removed, leaving exactly one retained witness neighbour.
  That residual witness was isolated before the repair.
* Distinct matched edges use distinct centres and helpers. A witness
  has at most one helper, so a repair at another helper cannot remove
  the residual witness. All added vertices are in B. Old selected
  edge components and other retained isolate edges are untouched.

Thus the repaired set is dissociation of size |E_A|+mu_A. The reversed
construction has size |E_B|+mu_B. These are alternative sets; their
averaged sizes, not a duplicated simultaneous resource, give

    2d<=p+b2+b3-mu=c-q+b2+b3-mu.                    (11)

Denote the right side by C0.

There are 2b2 witness incidences at the h=2 isolates. At most q come
from centre witnesses, so at least 2b2-q come from leaf witnesses.
Retain any two leaves per star and discard the other s leaves. This
removes at most s edges from Gamma. Call the resulting restricted graph Gamma', before applying the degree bound.
This bipartite multigraph has maximum degree at most two on both sides. Each component is a path
or an even cycle, including a parallel two-edge cycle, so alternating
edges give a matching of size at least half its number of edges.
Consequently

    2mu>=2b2-q-s,
    D0:=q+s+2mu-2b2>=0.                             (12)

This estimate also holds when 2b2-q-s is negative.

## The sharp coefficient and quantitative remainders

Equations (8), (11) and (12) have the weighted consequence

    7B0+13C0+3D0
      =20c+4q+3s-b3-7mu>=40d.                      (13)

Using (5) and (7),

    n>=5c+3s+q+2d.

Multiplying by four and applying (13) proves

    4n>=48d+9s+b3+7mu.                              (14)

In particular n>=12d, proving (1) by integrality. The argument also
applies when d<=0; then (1) is immediate.

A second useful combination is

    (10B0+20C0+5D0)/6
      =5c+(5/6)q+(5/6)s-(5/3)mu>=10d.

It gives the additional stability bound

    6n>=72d+q+13s+10mu.                             (15)

The parameters q,s,b3,mu all refer to the one fixed witness choice
above. Both inequalities hold for every permitted choice. The term mu
measures compatible repairs and is an ordinary bipartite matching
number, with each centre and helper having capacity one.

## Necessary structure of positive unrounded equality

Suppose n=12d>0. Equations (14)-(15) force

    q=s=mu=b3=0.

Then (12) forces b2=0. Equations (8) and (11) give c>=2d. Equations
(5) and (7), with n=12d and s=q=0, give 5c+2d<=12d, so c<=2d.
Hence

    c=2d,   e=2c,   t=a=c,   p=c.                  (16)

All counts in (5) must be exact. There are no selected edge components,
untouched isolates or unused outside vertices. The selected subgraph
therefore consists of c copies of P_3 and c isolates, and the 2c outside
vertices are exactly the chosen leaf witnesses. Each star has exactly
one private leaf witness; its other witness has a unique isolate helper,
and all these helpers are distinct. Every selected isolate is pendant.
The c centres and 2c leaves each have full graph degree two. All remaining
edges lie between the outside witnesses, consistently with bipartiteness.

Thus equality has the six-vertex-block template of the preceding exact
constructions, with arbitrary permitted witness-interface edges subject
to the additional requirement beta_2=7c/2. The template alone is not
asserted sufficient for equality. No exact SF_2 value is inferred.
In particular every positive unrounded equality example has at least
n/6 pendant vertices and at least n/2 vertices of degree two.

If G is nonempty and has minimum degree at least two, this rules out
positive equality n=12d, and improves the integer statement to

    |S|-beta_2(G)<=floor((n-1)/12).                  (17)

For d<=0 the right side is nonnegative. This applies in particular to
selected-star minimal sets in full rectangles with both dimensions at
least two. It does not assume that all minimal grid selections have
selected star components, and does not settle full rectangular equality.

## Attainment and verification

The connected degree-six family in
[SELECTED_STAR_COMPONENT_GAPS.md](SELECTED_STAR_COMPONENT_GAPS.md) has
n=24r, a minimal selected set of size 16r and exact beta_2=14r. Every
centre has a private leaf witness, so it attains (1) for every r>=1.
The degree-four port families and their exact formulas remain unchanged.

Run `python3 scripts/check_selected_star_general_budget.py`. The checker
independently tests literal formation and deletions, the selected-component
classification, all witness allocations in its finite exhaustive range,
both original and repaired colour sets, matching certificates and the
weighted inequalities against independently computed beta_2. Targeted
controls exercise direct-only centres, parallel repair edges and helpers
of larger multiplicity. The all-graph result is proved above. The checker passes on 5,399 graphs and 599,877 selected subsets, covering
39,880 permitted witness assignments and 80,912 repaired sets in that
exhaustive range. Nine targeted models additionally cover multiple witness
choices, large helper multiplicities, the positive equality template and
a positive-gap example with direct-only centres. The 52-vertex disjoint
control uses the previously proved G_(3,3) optimum plus an independent
exact solve of its other component; it is not a whole-graph exact solve.
The initial independent proof check returned ACCEPT. The final exact-source
execution audit is pending. No Lean or historical-priority verification
is claimed.
