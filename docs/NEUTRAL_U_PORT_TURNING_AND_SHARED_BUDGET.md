# Turning of neutral U-port curves and a shared compensation budget

20 October 2026. This reconstructs the neutral-port proposal in completed
research f583ea6c and extends it to curves containing passive phase10 ports.
It concerns the unrestricted finite complete U/rotor model; no dimension or
source-count cutoff is imposed. It does not close general coefficient one or
rectangular-grid triple equality. Rotor ports and open U-port paths remain
outside the closed-curve count and must be handled in the full problem.

## 1. The specified port graph

Keep the source, support-retention, endpoint-disjointness and fixed physical
partition assumptions of PASSIVE_CORNERS_AND_NEUTRAL_OWNERSHIP_CYCLES.md.
Use only the following original U singleton occurrences:

- phase01: the two original terminal 1P1T profiles;
- phase10: the two original outer-bar-corner 1P1T profiles.

Join two such ports precisely when their physical tile has actual profile
2P1T, its endpoints belong to these two distinct original singleton owners,
and exactly one original support is consumed. The other support remains
selected. Equivalently one port is active (its original blank is the other
endpoint and its support remains selected), and the other is passive (its
original support is the other endpoint and its blank remains outside P).
This is a neutral edge, not an activation of a positive source counted by A.

Each specified port has at most one partner: its fixed tile has exactly two
endpoints. Each source has two ports, giving a finite multigraph of degree
at most two. There are no self-loops because an original singleton receiver
contains only one endpoint of its original owner. Two different source owners
may share both ports, giving a legitimate two-vertex/two-edge cycle.
All other contacts of a source remain allowed. In particular a closed component
here need not be a component of the full endpoint-ownership contact graph.

Let the collection of all closed components of this specified port graph be
denoted by \(\mathcal C\),
and let ell be their number. Count original owners only once:

    M01, M10: phase01 and phase10 owners in this collection;
    B10: passive phase10 ports in this collection;
    Q01: phase01 owners in this collection with both ports passive.

Every port counted by B10 is a B occurrence from the passive-corner theorem.
Original owners and port occurrences do not recur across these components,
so B10<=B. Counts are over the same source collection as any budget used below.
The inclusion is the identity on original (owner, corner_index) keys; an owner
belongs to only one specified component. The checker now reconstructs these
two occurrence sets and verifies the subset directly, as well as the numerical
budget. The symbol C in the reserve ledger remains the numerical credit.

## 2. Main closed-curve inequalities

The unrestricted geometric statements are

    4ell <= M01-M10+2B10,
    2ell <= Q01+B10.                                (1)

The difference M01-M10 is signed. An equivalent subtraction-free form of the
first inequality is 4ell+M10<=M01+2B10. These are necessary conditions on actual
neutral U-port cycles, with arbitrary original owners and dimensions elsewhere.
They assign no fresh event reserve to a cycle.

The passive-corner budget B<=2A+H gives the simultaneous consequences

    4ell+M10 <= M01+4A+2H,
    2ell <= Q01+2A+H.                               (2)

Together with 2R=A+U0+Z0+H, the first also gives

    4ell+M10+2H+4U0+4Z0 <= M01+8R.                 (3)

These substitute one shared bound for the original B10 pool. They do not
add a new B10 payment to A or H, or add these conclusions to an unrelated
lower bound for R. A single A occurrence may receive both a corner and a
terminal claim in the underlying B theorem; its factor two is preserved.

## 3. Embedded curves and the signed turn identity

For a phase01 source, connect its two ports along its two original stems
and outer bar. For a phase10 source, use its original outer-bar row. Each
is a simple lattice arc contained in that source's original endpoint set.
Different original owners have disjoint endpoint sets. Connect paired ports
by their unit neutral contact edge. A closed port component therefore gives
a simple closed lattice polygon. Unit lattice edges cannot cross in their
interiors; any intersection would share an integer endpoint. No source arc
or contact repeats a port. Other endpoint contacts not used by this curve
do not change its simplicity. The elementary total-turn theorem for a simple
orthogonal polygon gives total signed quarter-turns +4 or -4.

At either original port p let s be the unit direction from p into the chosen
source arc and d the direction toward its unique original blank in the tile.
The original support is p-s. The source catalogue gives

    chi=det(s,d) in {-1,1}.

The two ports of either source have opposite chi. Traversing its source arc
from entry to exit contributes -2chi quarter-turns for phase01 and zero for
phase10, where chi is evaluated at its exit. These statements follow directly
from the two stem turns or the straight outer-bar path; independent stem
heights change lengths, not directions or turns. Reflections reverse all signs.

Across an active-to-passive contact p to q=p+d_p, its two original supports
and the remaining tile corner give

    s_q=d_p, d_q=-s_p.

Thus chi is preserved across a contact and reversed across each source.
A closed component has an even number n of sources. Orient it, write chi_i
at each exit, u_i=1 for phase01 and 0 for phase10, and beta_i=1 for an active
exit and -1 for a passive exit. Indices are cyclic. Contact turns contribute
-chi_i beta_i, including the possible bend at the next source's entry.
The exact turn identity is consequently

    T=sum_i chi_i(2u_i+beta_i) in {-4,4}.           (4)

Here the polygon's measured turn is -T; this sign convention has no effect
on the bounds. Put a_i equal to the number of active ports of source i.
The entry port is active precisely when the preceding exit is passive, so

    a_i=1+(beta_i-beta_(i-1))/2.

Since chi_(i+1)=-chi_i and sum_i chi_i=0, cyclic reindexing gives

    sum_i chi_i beta_i=sum_i chi_i a_i,
    T=sum_(01) chi_i a_i+sum_(10) chi_i(a_i-2).   (5)

These equalities account for the contact and source turns together. Omitting
the passive10 correction would incorrectly apply the AA specialization to
unrestricted curves.

## 4. Proof of the two counting inequalities

For one component let m01,m10 be its counts, b10 its passive10 occurrences,
and q01 its double-passive01 owners. Exactly one active port occurs per edge,
and a cycle has one edge per owner. Hence

    sum_all a_i=m01+m10,
    sum_(10) a_i=2m10-b10.

Apply the triangle inequality to(5), using 0<=a_i<=2:

    4=|T| <= sum_(01) a_i+sum_(10)(2-a_i)
           =m01-m10+2b10.

This proves the first bound without claiming any independence of resources.

For the second, let p01,q01 count double-active and double-passive phase01
owners, and p10,q10,t10 the double-active, double-passive and singly-active
phase10 owners. Total active-port balance gives

    p01+p10=q01+q10, b10=2q10+t10.

Using sum_all chi_i=0, rewrite(5) as

    T=sum_(01) chi_i(a_i-1)+sum_(10) chi_i(a_i-3).

The triangle inequality bounds this by

    |T| <= p01+q01+p10+3q10+2t10
          =2q01+4q10+2t10=2(q01+b10).

Thus q01+b10>=2. Summation over the ell closed components proves(1).
The sum uses distinct original owners and passive ports; there is no reuse
across components even when their full endpoint-contact components coincide.
Substitution B10<=B<=2A+H gives(2), and the exact reserve identity gives(3).

## 5. AA: closed neutral components need excess01 owners and two sinks

Fix one full endpoint component c satisfying the established nonexceptional AA
residual hypotheses. Every curve and every count in this section is restricted
to c. A phase10 owner with one B corner has its other corner receiver full.
A phase10 owner in a
closed neutral component has BOTH port receivers nonfull. It therefore has
no passive port, giving B10=0. The resulting necessary restrictions are

    M01>=M10+4ell, Q01>=2ell.                      (6)

For a pure phase01 component, active/passive balance also gives at least two
double-active owners as well as two double-passive owners. These are actual
original phase counts and sink occurrences. They are not event-reserve units:
C-Kirregular still appears in R. Rotors, full receivers and open paths can
escape this specified graph. Equation(6) alone does not exclude AA or prove
strict Epair excess. The full finite closure remains the primary target.

There is a concrete continuation obligation at each neutral01-to-01 edge.
Orient it from active p to passive q=p+d, with s pointing into the active
source. Since the legal terminal height is even and at least four,

    z=p+s+d

is an original inward support of the active source, anchored at p+s. It is
also the original exterior support of the passive terminal, anchored at q:
its blank direction is -s. The two anchors are distinct persistent endpoints.
Retention therefore forces z into P, owned by neither incident source.
This proves an actual additional endpoint requirement, not a fresh reserve
or a new owner distinct from all other sources in the curve.

In AA no neutral edge joins two phase10 owners, since both would be active.
Counting the two incidences at every phase10 owner shows that the number
of neutral01-to-01 edges is exactly M01-M10, hence at least4ell. Consequently
each closed component has at least four distinct contacts with this forced
endpoint requirement. The later direction-tag injection in
DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md proves their forced points
globally distinct, even across port components. It also excludes their ownership
by any phase01 source on a closed port component. They may still share other
original owners and are not independent compensation units.
This continuation corollary is a later written addition, outside the initial
turning-review snapshot and its11 scoped Lean declarations.

## 6. Validation scope

The checker reconstructs source arcs, original supports/blanks, actual neutral
edges, closed components, full polygon vertices and turns from complete-source
fixtures. It includes parallel-edge two-source cycles and checks original
port nonreuse. General arbitrary-dimension arc and planar arguments above,
rather than finite enumeration, establish the theorem. Scoped Lean statements
verify the signed-capacity aggregation and conditional count/budget deductions;
physical source/planar/AA adapters remain written.

Initial controls pass640 complete feasible images,72 neutral edges and32
closed components. Existing opposed-band examples have m01=m10=1,b10=2,q01=0
and attain BOTH unrestricted inequalities. They demonstrate why the passive10
term cannot be dropped. Complete no-passive10 or AA curve coverage is ZERO.
Eight complete-fixture neutral01 contacts exercise the later forced-support
corollary and verify that its point is an actual foreign original endpoint.
Local arc/frame controls cover64 phase01/10 source images in all isometries.
69904 abstract cyclic sign/phase words include17064 with total turn magnitude4
and218 with no passive10. These words are algebra controls, not geometric or
complete feasible realizations. Execution and independent-review receipts
are separate; no pending review is described as accepted.

A separate endpoint-disjoint partial geometry attains the no-passive10 bounds.
Take standard sources with the following exact maps:

    U(14,4,4): (r,c)->(r,c+1),
    U(6,4,4):  (r,c)->(c+3,7-r),
    U(14,4,4): (r,c)->(13-r,c+1),
    U(6,4,4):  (r,c)->(c+3,r+10).

Their port graph is one four-phase01 cycle, with two double-active and two
double-passive owners. The only infeasible mandatory retained supports are
(3,3),(3,14),(10,3),(10,14), each seeing two persistent endpoint neighbors.
They would have to be consumed by additional original owners. This is a
nonvacuous simple-curve control, not a complete feasible fusion or AA example.
It identifies four actual continuation obligations, not four new payments.

All11 scoped Lean4.33.0 declarations compile/build locally and pass individual
axiom audits, using only propext, Classical.choice and Quot.sound as applicable.
The list moment bound is proved by arbitrary-list induction; the subsequent
count deductions retain their stated physical/topological premises.
See output/neutral-port-turning-formal-check.json. Independent review uses
taskbb9caa70, original streaming session7500, completed ACCEPT at07:57:45.327UTC,
observed gpt_6/pro. The review accepts the physical polygon/sign proof, both
counts, original occurrence inclusion and same-component AA deduction under
the accepted dependencies, not executions. Its requested explicit AA component
restriction and separate curve/credit notation are incorporated above; its
suggested direct occurrence-set check is also implemented. The later forced01
continuation/injection/any-pair extension is outside that initial review snapshot.
See the review receipt for original-stream transport status. The passive-corner
review3361b134 is separate and its completed answer was recovered from its same
task API after original stream failure.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
