# A live shared gate defeats every maximum certificate

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

The [paired-hole note](PAIRED_HOLES_AND_CERTIFICATE_OPTIMIZATION.md) left open
whether safe pruning restores the existence of a maximum-cardinality terminal
certificate attaining ordinary compensation optimum. It does NOT in the
abstract strand model. We give a connected all-live family with terminal link
degree at most two and consistent necessary checkerboard phases. For every
q>=2 it has

    ordinary optimum = q payments at q minimum links;
    maximum terminal assignments = 4q-2;
    payment of EVERY maximum certificate = 1;
    largest certificate paying all q = 3q-1.

Thus full payment requires losing at least q-1 terminal assignments from
maximum coverage, and that exact loss is attainable. More generally the
largest certificate paying at least p alphas is 4q-1-p, for 1<=p<=q.
All original interval supports are empty; all payment units are distinct
whole betas. No resource-identity ambiguity is involved. One actual mixed
owner, shared by all indirect routes, has capacity one.

Shared-gate route conflicts are already present in the repository's frozen
gate examples. The new conclusion here is the failure of EVERY maximum
terminal certificate despite available direct beta bypasses, together with
the exact coverage/payment tradeoff and survival of safe pruning.

This is NOT a frozen-grid realization. Degree and phase conditions alone do
not prove one exists. Conversely, on 576 existing frozen physical controls
we explicitly construct maximum certificates attaining the ordinary optimum.
The new abstract family therefore identifies a geometric exclusion or repair
that a universal frozen-grid proof would have to supply; it does not refute
the grid inequality or improve the universal 5/6 bound.

## 1. The finite strand system

Fix q>=2. Use q alphas A_i, q betas B_i, and mixed owners N_i,M_i for
0<=i<q. Each alpha has one active TP a_i and one TP with no declared link.
Each beta has one active BP b_i and one BP with no declared link. Every mixed
owner has its one BP input and its one TP output. There are NO intervals.
For each i declare just these local links:

    a_i -> b_i;
    a_i -> BP(N_i);
    TP(M_i) -> b_i.                                      (1)

Connect the N outputs through a binary merging tree to a mixed root K;
connect K's output through a binary splitting tree to the M inputs. The
two trees share exactly K. A concrete caterpillar definition, used by the
verifier, is as follows.

Merging mixed owners U_1,...,U_{q-1}, with K=U_{q-1}:

    TP(N_0),TP(N_1) -> BP(U_1);
    TP(U_{j-1}),TP(N_j) -> BP(U_j),  2<=j<=q-1.           (2)

For q=2, split TP(K) to BP(M_0),BP(M_1). For q>=3, introduce mixed
V_1,...,V_{q-2} and declare:

    TP(K) -> BP(M_{q-1}),BP(V_{q-2});
    TP(V_j) -> BP(M_j),BP(V_{j-1}), 2<=j<=q-2;
    TP(V_1) -> BP(M_1),BP(M_0).                          (3)

No other links are permitted. The tree internal-owner count is 2q-3,
including K, so the total owner count is 6q-3 and mixed count is 4q-3.
Original owner identities and their actual BP/TP terminal identities are
fixed throughout. No artificial duplication of K is allowed.

Every N_i is reachable from A_i and can continue through K to a beta.
Every merging owner is reached by some N_i and continues to K. Every
splitting owner and every M_i is reached through K and continues to a beta.
Therefore EVERY mixed owner lies on a declared alpha-to-beta route. The safe
reachability/productivity deletion removes nothing. The original interaction
graph is connected.

Every terminal has at most two candidate links. Give all active a_i and
all mixed TP outputs phase 0, all their BP targets phase 1, and each alpha's
or beta's unused partner the opposite phase from its active end. Then every
original paired strand has opposite-phase ends and every candidate TP--BP
link joins opposite phases. These are necessary checkerboard conditions
for a physical realization, not sufficient geometric or freezing conditions.

The proofs below apply to ANY two rooted full binary trees on these labelled
N and M leaves, with only their mixed root shared. Each has q-1 internal
vertices; the explicit finite controls use the caterpillar realization above.

## 2. Maximum coverage and its forced shared-gate payment

Consider the bipartite terminal graph, WITHOUT original owner-pair edges.
Its nontrivial connected components are disjoint:

- q paths of length three, TP(M_i)--b_i--a_i--BP(N_i);
- q-1 merging stars, each consisting of two TP candidates for one BP;
- q-1 splitting stars, each consisting of one TP and two BP targets.

The unused alpha TP ends and unused beta BP ends are 2q isolated vertices.
A local length-three path has maximum matching size two, uniquely choosing
a_i->BP(N_i) and TP(M_i)->b_i. A merging or splitting star has maximum
size one, with exactly two choices. Because these terminal components are
disjoint, maximum global coverage is exactly

    nu = 2q+(q-1)+(q-1) = 4q-2,                          (4)

and the number of maximum certificates is exactly 4^(q-1).

Every maximum has NO direct a_i->b_i link. It matches all a_i to N_i,
all M_i to B_i, every merging BP to one of its two inputs, and every
splitting TP to one of its two outputs.

Trace the selected incoming edge backwards from K. The merging tree is
finite and acyclic, so the trace reaches exactly one N_i, whose BP is
matched from A_i. Trace the selected outgoing edge forwards from K. It
reaches exactly one M_j, whose TP is matched to B_j. Consequently one
selected path is an ordinary alpha-to-beta stem through K.

Every indirect alpha-to-beta route in the ORIGINAL graph must use K. Since
an ordinary packing cannot reuse a mixed owner, at most one such route can
be selected. There are no direct beta links in a maximum certificate and
no interval payments. Thus EVERY maximum certificate pays exactly one alpha,
regardless of its 4^(q-1) possible tree choices. This also follows directly
by counting its final alpha paths in the selected cancellation graph.

The actual unrestricted ordinary optimum is q: use the q disjoint direct
links a_i->b_i. Fewer than q links cannot pay q alphas because every support
is empty and each paid source needs a route of at least one link. Hence the
minimum link cost is exactly q. There are no beta-body interval forks here.

In particular the conjectured existence of an optimal maximum certificate
fails even after all safe pruning, in a connected system with degree-two
terminal candidates. This resolves the ABSTRACT question left by the
previous note. Its version restricted to genuine frozen-grid systems remains
open.

## 3. Exact coverage/payment tradeoff

Let a partial certificate have m assignments, d of which are the direct
a_i->b_i links, and let P be its actual alpha payment. There are no interval
slots, so assignments here are all actual TP--BP links.

Each direct link uses both internal vertices of its local length-three
terminal path. Its local matching then has size only one instead of two.
Every other local path contributes at most two, and the two tree sides
contribute at most q-1 each. Thus

    m <= 4q-2-d.                                         (5)

Every direct link pays one alpha. Any other paid alpha must route through
K, so the number of such payments is at most one:

    P <= d+1.                                            (6)

These are genuine packing bounds. Equivalently, in any selected cancellation
every alpha has at most one selected outgoing link and every beta has at
most one selected incoming link, because only its active terminal is
incident to candidates. Mixed owners have at most one of each. The owner
graph is directed acyclic. All selected components are directed paths,
and the paid components are precisely the alpha-to-beta paths. Therefore
no nonnormalized cancellation or hidden second beta entry bypasses (6).

If a certificate pays at least p, 1<=p<=q, then d>=p-1. By (5),

    m <= 4q-1-p.                                         (7)

**Theorem (exact frontier).** For every 1<=p<=q,

    max {m : some certificate pays at least p} = 4q-1-p.   (8)

**Construction attaining the bound.** Set d=p-1. Use direct links for
i=0,...,d-1. For every other i use both a_i->BP(N_i) and TP(M_i)->b_i.
Choose an incoming edge at EVERY merging BP so that the backwards trace
from K ends at N_d; choose an outgoing edge at EVERY splitting TP so that
the forwards trace ends at M_d. Such choices exist along the unique tree
paths; choices off these paths can be arbitrary. The terminal stars remain
disjoint, so all choices form a legal matching.

Exactly the d direct alphas and A_d are paid. All d+1 payments use different
betas, namely B_0,...,B_d, and only the A_d stem uses K. Its assignment count is

    d+2(q-d)+2(q-1)=4q-2-d=4q-1-p,

proving (8). For full payment p=q, the largest certificate has 3q-1
assignments. Comparing with (4), the necessary loss from maximum coverage
is exactly q-1. No smaller sacrifice suffices.

This counts terminal assignments, not the minimum number of links needed to
pay the sources. The latter is q for the direct optimum. A large certificate
can contain many selected links in components with no paid alpha.

The earlier rule allowing only direct additions to unused targets remains
valid: it guarantees an inclusion-maximal optimal certificate, never a
maximum-cardinality one. Here (8) proves that reassignment to maximum
coverage must lose payment, even though all the original branches are live.

## 4. Where the two-hole budget becomes sharp but misleading

There are 6q-3 TP ends. A maximum certificate covers 4q-2 of them, leaving
2q-1 holes. The original interaction graph has one component. Its coarse
budget is therefore floor((2q-1)/2)=q-1. Because the certificate actually
pays just one of q alphas, its fine budget is also exactly q-1, and its Q
has q-1 isolated two-hole alpha components (there are no assigned intervals).
The remaining hole lies on the one paid mixed component.

Thus both counts correctly describe the selected certificate while the
ordinary system itself has deficit zero. A tight certificate bound is not
automatically a tight bound on the underlying geometry or full route system.

The shared mixed root is also why one must not independently route every
locally productive branch. All branches reach distinct whole betas, yet
all indirect routes share ONE K. Private terminal matching capacities do
not encode that owner capacity. Direct beta choices bypass K and recover
full payment, at the exact coverage sacrifice in (8).

## 5. Actual frozen controls: positive maximum certificates

The verifier separately revisits the existing internal PP-sealed board,
shared and unported mixed gates, beta-body fork, two bent matching orders,
graft, elbow, missing/collision/cycle stacks, occupied widths 6/8/12, rotor,
and star networks of widths 6/10/20. It applies all eight square symmetries
and four offsets, and constructs the aligned two-row bands anew after each
physical transformation. All 576 resulting boards are completely frozen.

For each board, compute the actual whole-support system and safe pruning,
then its ordinary maximum-payment/minimum-link flow. Extract its sparse
partial certificate from the chosen links and distinct interval payments.
Delete these occupied TP/target identities from the terminal graph and find
a maximum matching of the remainder. Its union with the fixed sparse
certificate is checked for legality, payment and total size.

On EVERY one of these boards the union has the SAME size as an independent
maximum matching of the entire terminal graph, and its fine budget equals
the ordinary optimum deficit. Thus this survey produces an explicit optimum
maximum certificate in each case, rather than treating a failed search for
a counterexample as existence evidence. Of these controls 304 have nonempty
alpha demands and positive payment; the other 272 have no alpha demand.
No universal conclusion follows from this finite collection.

No frozen realization of the new all-live tree-gate family has been obtained.
It cannot be inferred merely by drawing these terminals in separate rows:
the actual matching/PP paths must connect the declared owners, every selected
T must retain its feasibility bound, all endpoints must freeze, and all
other original whole-support intervals and alternative links must be retained
or have separately justified reservations. Extra interval exits could repair
the obstruction. These are unresolved mathematical conditions, not reasons
to identify the abstract system with a grid counterexample.

## 6. Verification and formal scope

```sh
python3 develop/check_live_gate_certificate_trap.py \
  --output output/live-gate-certificate-trap-validation.json
cd formal
lean SubQuorum/LiveGateCertificateTradeoff.lean
```

The checker validates 16,038 abstract certificates. This includes all 10,350
partial certificates for q=2,3 and all 5,460 maximum certificates for q=2..7;
these check sets overlap. Another 209 constructed frontier points span
q=2..20. There are 473 independent restricted-flow/lifting comparisons.
Each finite family checks zero pruning, connected interaction, degree-two
terminal components and necessary phases, maximum size, the sharp coarse/fine
budget and actual payment/minimum-link cost. The physical part constructs
the 576 optimum maximum certificates described above. The all-q results
are proved in Sections 1--4, not inferred from these checks.

Local Lean verifies nine declarations: actual three-edge local-matching capacity, its sum over
arbitrary local groups, the unique-gate injection capacity, and the resulting
coverage/payment frontier upper bounds and exact gap arithmetic. General
directed tree tracing, packing decomposition, frontier witness construction
and frozen physical adapters remain written proofs plus computational checks.
No complete Lean formalization of those adapters or new independent external
review is claimed.

The independent research branch preserves the submitted 11 October manuscript,
public main, PR #3, shared CI and star-forming/C4 work. This round does not
read Mail, change a draft or send a message. The next geometric question is
whether complete freezing excludes this all-live serial bottleneck or forces
an extra distinct interval/beta bypass. The abstract liveness and terminal
degree tests alone are now proved insufficient.
