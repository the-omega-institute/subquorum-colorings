# Several Hall-tight regions with one exterior HH budget

11 November 2026. This extends the endpoint conservation lemma in
[the multicentre note](https://github.com/the-omega-institute/subquorum-colorings/blob/b7ac9ce363223bf33aee42ab9d44b446183079e1/docs/MULTICENTRE_HALL_BALANCE.md).
It proves simultaneous counting for arbitrary overlapping tight regions.
It does not assert that an endpoint assignment extends to a full grid matching.

## Setting

Let the direct exterior graph have white side T, black side B, a matching
saturating B, and |T|=|B|+1. There are r black centres C, r-1 other white
sources W, and a full auxiliary matching N. As in the separated-core
model, the terminal alternating paths of M union N define a bijection
pi:T disjoint-union W -> B disjoint-union C. A path starting in T is TH;
one starting in W is HH. Let k be the number of TH paths ending in C.
Thus k>=1 and exactly k-1 HH paths end in B. A direct TH path is an edge
of the direct exterior graph. Assume centres have no direct T neighbour.
For unit actual-edge weights, every other TH path costs at least one;
different paths use disjoint actual M edges. The same bounds hold for
weights at least one. Paths and grid completion are not inferred from a
bijection alone.

For each index j choose a nonempty balanced tight set D_j subset B,
F_j=N_T(D_j), with |F_j|=|D_j|. Sets may overlap or be nested. Choose
finite nonnegative real weights lambda_j and put

    phi_B(b)=sum_j lambda_j 1_(b in D_j),
    phi_T(t)=sum_j lambda_j 1_(t in F_j),
    mu=max_(b in B) phi_B(b).

On centres put phi_B=0. Ignore the all-zero choice; then mu>0.

## Simultaneous conservation theorem

For a TH path t->v, define its withdrawal and compensation amounts as

    A(t,v)=(phi_T(t)-phi_B(v))_+,
    B(t,v)=(phi_B(v)-phi_T(t))_+.

Let A_tot and B_tot be their sums over TH paths. Then

    A_tot-B_tot = sum_(w in W) phi_B(pi(w)),
    0 <= A_tot-B_tot <= (k-1)mu.                         (1)

Moreover max_T phi_T=mu. Every TH path with B(t,v)>0 is a non-direct
path ending in B, and its compensation is at most mu. If q is the number
of such compensating paths and

    R=sum_(t in T, pi(t) in C) phi_T(t),

then

    q >= max(0,ceil((A_tot-(k-1)mu)/mu))
      >= max(0,ceil((R-(k-1)mu)/mu)).                    (2)

In particular the unit-weight expense obeys

    f(N) >= k + max(0,ceil((R-(k-1)mu)/mu)),             (3)
    f(N) >= k + max(0,ceil((A_tot-(k-1)mu)/mu)).         (4)

**Proof.** Fix any direct matching saturating B. For a tight pair D_j,F_j,
the matching maps every vertex of D_j into F_j and their equal cardinalities
force a bijection between these two sets. Consequently t belongs to F_j
if and only if its matched black partner belongs to D_j; unmatched whites
belong to no F_j. The potentials on the two sides have the same multiset
of nonzero values, proving their equal maximum, and

    sum_T phi_T = sum_B phi_B.

The terminal bijection counts each black terminal once. Subtract its HH
contribution from that equality to obtain the identity in (1). Only
k-1 HH paths end in B; each contributes at most mu. In particular an HH
endpoint in several tight regions contributes its actual summed potential
once, bounded by mu. It is never granted one unit separately per region.

For every direct edge t--b, membership b in D_j implies t in F_j.
Nonnegative weights therefore give phi_T(t)>=phi_B(b). Such an edge
cannot have positive compensation. For a compensating TH path its endpoint
is exterior, and its positive amount is at most phi_B(b)<=mu. Thus
q mu>=B_tot>=A_tot-(k-1)mu. All centre TH paths contribute their whole
phi_T source value to A_tot, so A_tot>=R. This proves (2). The k centre
paths and the q compensating paths are distinct non-direct paths. Each
uses at least one actual edge; these actual edges are disjoint between
components. This proves (3) and the stronger (4) with no repeated fee. QED.

For pairwise disjoint D_j and lambda_j=1, mu=1, the F_j are also disjoint
by the fixed matching argument. Formula (1) then couples all regions using
just k-1 total exterior HH units. For overlapping regions, the factor mu
is essential. Rational weights permit exact integer arithmetic after a
common rescaling. For each fixed full N, any finite maximum over choices
of regions and weights remains a valid bound. Exact minimization must
retain the joint dependence of k,R on N; separate minima can give a
weaker valid bound.

## An explicit obstruction to adding unnormalized region counts

The following is an endpoint countermodel, not a rectangular-grid
counterexample. Its purpose is to refute endpoint-only reasoning that
sums HH use over overlapping regions and still subtracts just k-1.
Take

    T={t0,t1,t2,e}, B={b0,b1,b2},
    direct edges={t0--b0,t1--b1,t2--b2},
    C={h0,h1}, W={w},
    pi={t0->h1,t1->h0,t2->b2,e->b0,w->b1}.

Let D1={b0,b1}, D2={b1,b2}, with F1={t0,t1}, F2={t1,t2}.
Both are distinct balanced tight regions. Here k=2 and the single exterior
HH path ends at b1, inside BOTH regions. Their separate unweighted counts
are (a1,b1,c1)=(2,1,1), (a2,b2,c2)=(1,0,1), where a is withdrawal, b TH
compensation and c HH compensation. Thus sum c_j=2>k-1=1. The proposed
inequality sum b_j>=sum a_j-(k-1) would incorrectly say 1>=2.
The correct weighted sum uses mu=2 and permits 1>=3-2. The compensated
path e->b0 is counted once in this example. This falsifies the unnormalized
counting rule; it says nothing against a geometric grid bound.

## What this yields at unit weights

If all k centre sources have maximum potential mu, (3) forces an additional
paid exterior TH path and gives f(N)>=k+1. This simultaneously includes
all overlapping tight regions obeying that source condition. Also R<=k mu,
so the extra integer term in (3) is at most one. Thus the R-only bound (3) cannot certify k+2. The stronger A_tot
bound (4) can do so: it also retains exterior withdrawals. For example,
let T={t1,t2,t3,e}, B={b1,b2,b3}, C={h}, W empty, direct edges
{t1--b1,t2--b2,t3--b3,t2--b3}, D={b1,b2}, F={t1,t2}, and
pi={t1->h,t2->b3,t3->b1,e->b2}. Then k=mu=R=1 but
A_tot=B_tot=2, so (4) yields f(N)>=3=k+2 for any physical realization
obeying the hypotheses. This is a second endpoint illustration, without
a grid-realization claim. Additional path length, capacity, source
eligibility or completion information can further strengthen these counts. The theorem does not resolve the universal
5/6 colouring bound or the proposed grid triple equality.

The accompanying checker enumerates direct graphs, all their balanced
tight sets, several weight combinations, and terminal bijections. It
verifies every identity and count without importing the grid algorithms.
This is a finite implementation control for the general proof, not an
existence proof for simultaneous geometric routing. No Lean claim is made.
