# Arbitrary-entrant relays: empty rectangles and exact local cost

The subsequent [physical square-interface analysis](SINGLE_SQUARE_WIRES_AND_SOURCE_FREE_PRUNING.md)
proves the aligned unique-square class source-free and gives a fully frozen
capacity-two tile whose two local wires are one mixed owner. It is an actual
obstruction to inferring this note's relay capacity from tile residual r=2.

25 October 2026. Wenlin Zhang and Haobo Ma.

This extends [multi-source bypass lifting](MULTISOURCE_RELAY_BYPASS_AND_DEFECT_BOUND.md).
The number of original source entrants is now unrestricted. The result is a
finite-network theorem with a general proof, not a new grid decomposition.
In particular a tile's residual capacity two is not automatically a relay
capacity two. The submitted manuscript is unchanged.

## 1. Complete model and the bypass relation

Keep the earlier complete one-stage model. Each original source is used at
most once, each original resource identity at most once, and each route is
either source-private or passes through exactly one relay. Different sources'
private route owners and all relay regions are disjoint. Alternative routes
of the same source may overlap. A relay g has integer capacity c_g>=1,
arbitrary finite entrant set U_g and output set R_g. Every entrant reaches
every output at nonnegative separable cost e_g(a)+o_g(j). Internal conflicts
are exactly the stated relay capacity; no other shared owner may be hidden.
Source and resource sets may overlap between relays; their global identities
are retained. Fix the available original resource set Q.

Let d_a(j) be the least cost of a private route, or infinity if absent.
Define the cost-dominating private relation

    B_g(a,j) iff d_a(j)<=e_g(a)+o_g(j),
    a in U_g, j in R_g intersect Q.                         (1)

An **empty rectangle** X times Y has no pair in B_g. Its sides consist of
distinct original sources and distinct original units. Distinct units in one
support interval remain distinct; two names for the same unit do not.

## 2. Local exact formula, including costly bypasses

Fix equally sized S subset U_g and J subset R_g intersect Q, |S|=|J|=t.
All t routes originally use g. Let mu_all(S,J) be the maximum matching size
in the relation of ALL existing private routes, and mu_cheap(S,J) the maximum
matching size in B_g. Then the maximum number payable while using only these
sources, these units, private routes and g is exactly

    min(t,c_g+mu_all(S,J)).                               (2)

Indeed a private matching of size mu_all leaves equal-sized unused source
and resource sets. Pay min(c_g,t-mu_all) of those pairs through g. Conversely
any packing has at most mu_all private payments and c_g relay payments.

If all t can be paid, put

    W(S,J)=sum_(a in S)e_g(a)+sum_(j in J)o_g(j).

Their exact minimum cost is

    W(S,J) + min_H sum_((a,j) in H)[d_a(j)-e_g(a)-o_g(j)], (3)

where H ranges over private matchings on S,J with |H|>=t-c_g (the quota is
zero when t<=c_g). For any such H the remaining vertices pair arbitrarily
through the common-output relay. Its cost is exactly the displayed expression.
Conversely every full packing determines such an H and the same expression.
The minimum includes optional extra cheap private routes. Merely finding a
maximum-cardinality private matching does not generally minimize cost.

Using only cheap private routes, all t payments lift with no cost increase
whenever mu_cheap>=t-c_g. More generally the constructive loss certificate is

    ell_g(S,J)=max(0,t-c_g-mu_cheap(S,J)).                 (4)

Choose a maximum cheap matching, then pay up to c_g remaining pairs through g.
Only unused sources and units are discarded. Their nonnegative entry/output
costs and the nonpositive adjusted private costs prove that the resulting
total cost is at most W(S,J). Formula (4) is exact for the cheap-route
subsystem's cardinality. It need not be the true loss when expensive private
routes or other relays are available. Equation (3) resolves the cost tradeoff.

## 3. A sharp uniform criterion with no entrant bound

**Theorem 1.** A single relay has a cost-nonincreasing full lift for EVERY
choice of equally sized S,J and EVERY pairing of them through the relay,
preserving their source and resource sets, if and only if its cheap relation
has no empty (c_g+1)-by-(c_g+1) rectangle.

**Sufficiency.** If the current relay load exceeds c_g, take any c_g+1 current
sources and their c_g+1 current units. There is a cheap pair (a,j). If a is
currently assigned k and b is assigned j, pay a privately at j and assign b
to k through g; if a=b, simply bypass that route. All other assignments stay.
Separable cost gives

    d_a(j)+e_g(b)+o_g(k)
      <=e_g(a)+o_g(j)+e_g(b)+o_g(k).

The old two-route cost has the same right side. Original sources and units
are preserved, and relay load decreases by one. Repeat until load<=c_g.
This is a terminating proof for every finite load, with no enumeration.

**Necessity.** Suppose X,Y form an empty square of side c_g+1. Paying those
sources at exactly those units requires at least one private route. Every
such route has strictly positive adjusted cost d_a(j)-e_g(a)-o_g(j), or is
absent. The baseline W(X,Y) is the same for every all-relay pairing. Equation
(3) therefore says every full lift costs strictly more than baseline, or no
full lift exists. This distinguishes failure of cardinality from failure of
cost preservation. Other relays can repair a local obstruction, so necessity
is for the isolated local universal property, not for a multi-relay optimum.

An equivalent, directly checkable statement is: every c_g+1 entrants together
privately cover all but at most c_g available original outputs. It is not
enough that ALL entrants together cover those outputs. If |U_g|<=c_g+1 this
recovers precisely the earlier condition; if fewer than c_g+1 entrants or
outputs exist, the new condition is vacuous and the module is safe.

**Corollary 2.** If every module satisfies Theorem 1's condition, every
projected source-resource matching lifts with the same payments, same source
and resource sets and no greater cost. Thus maximum payment and minimum cost
at that value equal the weighted bipartite projection. Full payment is
equivalent to its Hall inequalities. Repairs at distinct modules use disjoint
selected source groups and do not enter another relay. Actual private owner
disjointness prevents hidden cross-component capacity reuse.

For an abstract capacity-two relay, the criterion is the absence of an empty
3-by-3 rectangle, even with arbitrarily many entrants. This is a stronger
interface than the earlier three-entrant special case, not a proof that any
physical capacity-two tile supplies that interface.

## 4. Joint residual loss without reusing sources, units or bypass owners

For a projected matching P group its relay routes into (S_g,J_g), each of
size t_g. Their source groups and resource groups are separately disjoint.
Apply (4) to obtain a feasible packing of at least

    |P|-sum_g ell_g(S_g,J_g), cost<=cost(P).              (5)

Let H_g be a maximum cheap matching on S_g,J_g. Its unmatched source set X_g
and unmatched unit set Y_g have the same size q_g=t_g-|H_g|. Their rectangle
is empty: a cheap pair between two unmatched vertices could be added to H_g.
Thus ell_g=(q_g-c_g)_+.

Define K_rect(Q) as the maximum of sum_g(q_g-c_g) over choices of at most one
empty square X_g times Y_g per module with q_g=|X_g|=|Y_g|>c_g, requiring all
chosen X_g to be pairwise disjoint and all chosen Y_g to be pairwise disjoint.
Both conditions are essential. The unmatched sets just extracted are a legal
joint certificate, so with nu the projected maximum and V the actual maximum,

    V>=nu-K_rect(Q),
    |A|-V<=max_(Z subset A)(|Z|-|N_Q(Z)|)+K_rect(Q).      (6)

The second line uses the standard finite matching deficiency identity.
Because the chosen squares pair through their modules in the projection,
their total q_g<=nu. K_rect is a coupled maximum, not a sum of local maxima.
When all entrant counts are <=c_g+1 it equals the earlier kappa: each square
uses the full entrant group and c_g+1 outputs uncovered by that entire group.
No old special-case bound is lost.

The cheap maximum matching is a valid constructive choice for (5); it need
not give the smallest possible loss certificate for that P. The rectangle
bound itself can be conservative, and its failure does not refute the target
grid inequality. No projection-relative positive constant uniform in entrant
count follows without extra geometry or bypass density, as the next family
shows.

## 5. Sharp families and failure distinctions

For any integers c>=1,k>=1,n>c+k, take n sources, n units, one capacity-c relay
with every entry cost one and every output cost zero. Exactly k sources have
private routes of cost zero to every unit; the other n-k have none. Every
output is covered, by k distinct sources, but

    nu=n, V=c+k, K_rect=n-c-k.                           (7)

The uncovered sources and any n-k units form a maximum empty square.
This attains (6). Merely increasing the number of sources covering each
output cannot replace the subset criterion. These are abstract modules;
no frozen-grid embedding or global grid counterexample is asserted.

A cost-only control has c=1, two sources and two units, relay costs one per
route, and all private costs two. Its cheap 2-by-2 rectangle is empty.
Both payments are possible, but minimum cost is three instead of the
projection's two. Failure of the cheap rule here is a cost failure only.

Cheap-matching loss can also overestimate even the loss of one specified
all-relay packing. Take c=1, three sources A,B,C and units x,y,z, all relay
entry costs ten and output costs zero, private A->x of cost zero and B->y
of cost eleven, and no other private routes. The cheap matching has size
one, so (4) discards one payment. Nevertheless A->x, B->y and C->z pay all
three at cost 21, below the original all-relay baseline 30. The extra costly
bypass is offset by A's saving. The projection optimum costs 20, however,
so its full optimum cannot lift without a cost increase. Equation (3)
records these distinct comparisons exactly.

An unsafe diagonal-private module can nevertheless have an exact optimum:
with four sources and four units, private a->a of cost zero and capacity-one
all-to-all relay, disjoint two-source/two-unit subsets obstruct universal
lifting, while the complete pool pays four privately at cost zero.

Two locally bad modules sharing a source or sharing a unit cannot automatically
contribute two units to K_rect. The verifier checks joint rank one in both
cases. A private route sharing an internal capacity with another purported
private route still violates the model; the previous shared-owner 4-to-3
control is not repaired by this stronger relation criterion.

## 6. Geometry and verification scope

The odd-arm theorem already supplies exact original tile charge -2 for each
aligned unique-square receiver, with four distant exclusive half-donors;
occupied-strip flux requires its actual exported-TP debit. Neither fact by
itself creates mutually usable relay paths. This result removes an abstract
entrant-count restriction only after common outputs, separable costs and
private-owner disjointness have been proved. Multiple vertical layers and
physical capacity-two tile interfaces remain geometric tasks. The existing
beta-free one-layer H-forest adapter remains valid unchanged.

The companion verifier exhausts all 512 binary 3-by-3 bypass relations at
capacities one and two: 1,024 relation/capacity cases, 20,480 equal-sized local
interfaces, 177,920 independently enumerated local packings and 34,816 all-relay
pairings. Exactly 845 relation/capacity cases have the uniform property.
Another 160 weighted private-quota controls include expensive bypasses and
25,827 independent packings. Across 433 network models, 35 are independently
checked by 14,904 route packings; 40 joint ranks strictly improve the sum of
local maxima. All 243 existing frozen-board original-pool patterns agree
with the complete physical flow, with 162 safe and one value-gap pattern.
The new rank equals the earlier kappa in all 317 applicable controls.
See the [computational receipt](../output/relay-bypass-rectangles-validation.json). All general statements above
are proved independently of that enumeration.

The Lean module checks arbitrary-size no-hole restriction, existence of a
cheap pair in every overloaded indexed group, an unmatched-pair augmentation
interface, cost transposition, and the local/global loss arithmetic. It does
not formalize the full finite matching/quota optimization, joint-rank extraction
or physical grid adapter. All 15 declarations pass locally with Lean 4.33.0;
four are axiom-free and the others use only standard logical axioms, with no
warning, sorry, native computation axiom or new axiom. See the
[Lean source](../formal/SubQuorum/RelayBypassRectangles.lean) and
[formal receipt](../output/relay-bypass-rectangles-formal-validation.json).
These are applications of standard finite matching and separable-cost
arguments to the original-resource relay model; no literature-priority or
independent novelty claim is made.

Reproduce:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_relay_bypass_rectangles.py \
  --output output/relay-bypass-rectangles-validation.json
```

The unrestricted 5/6 bound is unchanged. No mail was read, drafted or sent in
this milestone. AI tools were used for proof development and verification.
