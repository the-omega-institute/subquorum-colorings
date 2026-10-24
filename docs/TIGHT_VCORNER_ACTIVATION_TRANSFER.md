# Tight vertical corners transfer to unused positive activations

21 October 2026. This resolves the tight incident-leg subclass of the
negative Vcorner role in the [all-length companion catalogue](ALL_LENGTH_SINGLETON_COMPANION_INJECTION.md).
It proves a new joint activation transfer and two small-width no-extension
obstructions. Unrestricted mixed allocation and rectangular-grid triple
equality remain OPEN. Finite controls are not used as a general proof.

## 1. Complete source model and the new subclass

Use finite complete original U/rotor families with disjoint original
endpoints and unchanged original matching. Every original support not
consumed by an endpoint is retained, with its original anchor as its sole
occupied neighbor. Original endpoint graphs are connected. The optional
selections allowed in the source model have no endpoint neighbor. Work in
the fixed aligned physical tile chart, transporting the whole original
source, supports and anchor assignments together under permitted isometries.
All widths are even>=6 and both independent leg lengths are even>=4.

An actual claim is one labelled marked side (original positive owner,
intrinsic leg index). Use the established canonical-gate normalization:

    A=U(w,L,K),       A(r,c)=(r,c),
    B=U(W,b,e),       B(r,c)=(b+3-r,c+1),
    C=U(V,h,f),       C(r,c)=(c+1,h+2-r),
    X=U(d,a,k),       X(r,c)=(c+2,r+3),
    t=(3,2), p=(2,2), y=(3,3).

A is positive; B consumes t as a negative singleton; C consumes p as a
negative terminal; X consumes y in the negative Vcorner role. These owners
are distinct. The all-length catalogue gives

    b>=6, 4<=h<=w-4, d<=b-2, a<=h-4.

Our additional hypothesis is a=h-4. In particular h>=8 and w>=12.

**Theorem.** Every such complete occurrence has a positive original owner

    Q=U(omega,ell,nu), Q(r,c)=(ell+3-r,h+1-c),
    6<=ell<=V-4,                                  (1)

with an actual activated positive terminal at x=(3,h). Assigning the
original marked side to that terminal occurrence is injective and disjoint
from ALL old S/P/R transfer targets and all all-length E/S companion
targets. The two consumed supports count as ONE activation, not two.

The forced-consumer and dimension assertions use only the prescribed C,X;
the claim reconstruction and old-S collision also use the actual A,B.
In particular prescribed endpoint-disjoint C,X have no complete extension
at V=6 or8. No bound is imposed on the number or sizes of extra sources.

## 2. Force the positive terminal, without a finite-search premise

X's near terminal is X(a,1)=(3,h-1). Its mandatory beyond-tip support is
x=X(a+1,1)=(3,h). The north and east neighbors of x are C endpoints

    (2,h)=C(2,1),  (3,h+1)=C(1,2).

Together with X's terminal west of x, these give three distinct fixed
endpoint neighbors. Keeping x as a selected support would violate its
original-anchor condition, so x must be consumed by an endpoint owner.
Neither C nor X owns x. Its consumer can have an own endpoint neighbor
only south of x. Every U endpoint of own degree one is a leg terminal;
every rotor endpoint of own degree one is a tip. Thus these are the only
possible roles, with no size restriction or enumeration assumption.

For the canonical rotor R from the original catalogue, the two distinct
south-pointing tip footprints at x are the images

    (r,c)->(r+2,c+h-2),
    (r,c)->(r+2,h+2-c).

Their endpoints include C's (4,h+1) and (5,h+1), respectively. Both C
points exist on its bar for every V>=6. Endpoint disjointness excludes
both rotor chiralities. The consumer is a U terminal with southward stem.
Let ell be its incident length and omega its width, allowing exchange of
its two original leg names. Its stem occupies column h from row3 through
ell+3. C has the fixed far-leg endpoint C(2,V)=(V+1,h), since f>=4.
Avoiding it forces ell+3<V+1; evenness gives ell<=V-4.

Its bar cannot point right: it would contain (ell+2,h+1), on C's bar
because ell>=4 and ell<=V-4. Its bar must point left, giving precisely
the Q frame in (1). Both reflection constants ell+3,h+1 are odd, so this
chart preserves the fixed physical tiles and Q is positive.

Q's original terminal supports are exactly the north/east corners
(2,h),(3,h+1) of its terminal tile. They are both consumed by C. Thus x
is ONE actual activated terminal, keyed by (original Q owner, terminal
index). The tile has three C endpoints and Q's terminal. We claim no
additional pair, triple, cap or unused-terminal reserve at that full tile.

## 3. The stronger lower bound and two obstructions

If omega<=h-4, Q's far leg is in column j=h+1-omega, with
5<=j<=h-5. X's near stem occupies row3 through columns3,...,h-1.
If nu>=ell, Q's far leg contains (3,j), a collision with that stem.
Therefore nu<=ell-2. Since nu>=4, necessarily ell>=6.

Otherwise parity gives omega>=h-2. Then Q's bar contains column4.
If ell<=d, its endpoint (ell+2,4) belongs to X's vertical bar, which
occupies column4 from row3 through d+2. Disjointness and evenness imply
ell>=d+2>=8. These two exhaustive width branches prove ell>=6.

Combined with ell<=V-4, this gives V>=10: V6 and V8 are impossible for
any complete extension. At h=8 the short-bar branch would require
omega<=4, impossible. Hence ell>=d+2 and V>=d+6 in that case. These are
necessary conditions, not claims that every remaining dimension choice
has a complete realization. The excluded configurations create no reserve.

## 4. Reconstruct the original labelled side from the target

The target is an original positive terminal, whose stem direction fixes
its outward endcap support and its other intratile support. At this target
they are (2,h),(3,h+1). Unique endpoint ownership identifies the same
negative owner C at both supports. Their C roles are different: the
first incident-leg point after the bar, intrinsic (2,1), and the adjacent
internal lower-bar point (1,2). They fix C's bar end, incident direction
and original incident terminal p. The opposite bar end cannot give the
same tile because C has width at least6. This reconstructs the normalized
frame, including t=(3,2).

The actual owner at t is the negative B. Of the two possible external
producer anchors (3,1),(4,2), the latter is B-owned. Hence the positive
producer owns (3,1). Unique ownership and canonical-gate uniqueness recover
the original labelled side of A. Consequently two distinct tight-Vcorner
claims cannot use the same activated Q occurrence. This reconstruction
uses actual source roles and ownership, not simply the name of a channel.

## 5. Joint nonreuse with every established transfer

We use the established S/P/R transfer theorem with its exact frames.
An old S target is the consuming terminal itself; in its producer chart
its recipient frame is (r,c)->(ell+3-r,3-c). An old P recipient frame
is T(r,c)=(c+2,r+2), its target is its incident terminal, and its producer
width w_old satisfies ell<=w_old-4. This is the arbitrary-length bound
from the positive pair-transfer theorem, not a width-six specialization.
All old R targets have one intratile support owned by their preceding
rotor. The all-length E/S targets have their two terminal supports owned
by DISTINCT original U owners B,C. These are the precise dependencies.

If x were also an S target, comparing recipient frames forces the old
positive producer map (r,c)->(r,c+h-2). It owns (0,h-1), the image of
its endpoint(0,1). But h<=w-4 makes (0,h-1) an endpoint of A. The old
producer cannot be A: all its endpoint columns are at least h-1>1,
whereas A has endpoints in column1. Thus this is a different-owner
endpoint collision, excluding S including a self-producer loophole.

If x were also a P target, comparing Q's frame with T gives the old
positive producer map

    (r,c)->(ell+5-c,h+3-r).

Its original endpoint(1,ell+2) exists because w_old>=ell+4. It maps to
(3,h+2), an endpoint of C. The hypothetical producer cannot be C:
it has bar endpoints on column h+3, whereas every C endpoint has column
at most h+2. Thus P is also impossible, at arbitrary ell.

An R collision would require one of x's supports to be rotor-owned;
both are C-owned U endpoints. An old E/S collision would require these
two supports to have distinct owners, whereas here they have the same
owner C. Endpoint uniqueness excludes both cases. This proves global
joint injectivity, even when the source family has many components and
recurring source roles. No per-component activation pool is introduced.

## 6. Effect on the same global allocation inequality

Let q0 count old S/P/R claims and qT all all-length E/S claims. Let kappa
count the tight-Vcorner claims. Their original gate consumers are negative
singletons, distinguishing them from the old S/P/R gate classes. Their
uniquely normalized companion at y has the actual negative Vcorner role,
distinguishing them from the E/S companion classes. The kappa claims are
reclassified from the former uncertified remainder, so these are disjoint
classes of labelled demands. This demand classification is separate from
target nonreuse. The above physical joint injection proves

    q=q0+qT+kappa <= Aactivation.                  (2)

Use the SAME established cap, upper-pair, lower-pair and m8 receipt inventory
in the same complete family. Let c,s,t be the remaining cap claims,
resolved lower-pair claims and uncertified claims AFTER removing kappa
from the former uncertified class. The established ledger hypotheses are

    G=q+c+s+t<=2(N-n0), s<=p,
    2R>=Aactivation+m8+c+2p+2u.

Here n0 counts independently certified distinct positive owners with both
sides unmarked, and N counts positive owners only. Substitution gives

    2mu>=2n0+2u+2p+m8-s-t,
    mu>=n0+u+p+ceil((m8-s-t)/2).                   (3)

If t_old is the previous uncertified count, t=t_old-kappa; no physical
receipt or activation is copied. The real lower bound for 2mu improves
by kappa. Its integer mu floor improves by

    ceil((m8-s-t_old+kappa)/2)-ceil((m8-s-t_old)/2),

which may be zero for one claim, depending on parity. The sufficient
condition for allocation can equivalently be written

    s+t_old<=2n0+2u+2p+m8+1+kappa.

On complete configurations satisfying that condition, the existing
sigma>=mu implication yields coefficient1 instead of5/6, a gain |M|/6.
No universal improvement to5/6 follows without universal residual coverage
and the arbitrary-grid source decomposition. Nontight Vcorner, unpaid H,
filled corridors and vertical regular exits remain substantive open cases.

## 7. Verification scope

The checker reconstructs original endpoints, supports and signs, the two
rotor-tip blockers, both U bar directions, independent dimension branches
and the old S/P producer collisions with their self-owner exclusions.
C/X and C/X/Q examples are PARTIAL: no complete marked Vcorner witness
or complete-extension existence theorem is claimed from them. The proof
above, not the finite controls, establishes arbitrary-extension forcing.
The scoped Lean file records unbounded coordinate, dimension, predecessor
collision and integer-ledger lemmas. The general role catalogue, claim
reconstruction and full physical injection are written proof adapters.

All20 declarations in TightVcornerActivation.lean pass localLean4.33.0,
finalsession28110exit0, with individual axiom audits using only ordinary
propext/Classical.choice/Quot.sound, no sorry/native reduction. Preflight
measured47% free memory and no real lean/lake comm basename. Controls pass
288 disjoint C/X patterns,3020 disjoint C/X/Q partial patterns,123 small-
width no-consumer controls, both rotor tip footprints and48 collisions
against each old S/P producer frame. They do not establish completeness
of the partial examples. Separate written audit2c96d3ca ACCEPTS the general
forcing, dimensions, labelled-claim injection, all supplied target exclusions
and conditional ledger. Its 15,028-character response matches original
stream71377 exactly, with [DONE], exit0 and observed gpt_6/pro. Section6
incorporates its clarification distinguishing demand classification from
target nonreuse. This review does not certify finite controls or Lean
execution, complete-extension existence, universal coverage or grid equality.
See the [full response](../output/tight-vcorner-review-response.md) and
[receipt](../output/tight-vcorner-review.json).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
