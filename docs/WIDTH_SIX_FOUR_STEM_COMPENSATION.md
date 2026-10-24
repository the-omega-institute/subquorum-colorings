# Four forced stems pay width-six doubles through height gap eight

20 October 2026. The full-chain residual at a width-six positive source
forces two additional original U owners between its two incoming gates.
Complete support retention, after the first receiver is filled, is
essential for the second new owner. Four disjoint vertical stems then
force three strict height separations. Together with the accepted chain
pool this extends the all-reserve coefficient-one class from positive
height differences at most four to at most eight. Negative dimensions,
phases, source counts and contacts remain unrestricted. Arbitrary mixed
allocation and the rectangular-grid triple equality remain open.

## 1. Model and theorem

Keep the finite complete U/rotor model and all definitions of
SUPPORT_CHAIN_COMPENSATION_AND_RESIDUAL_SATURATION.md. Endpoints and
matchings retain their original owners, endpoint sets are disjoint,
every original support outside P is retained, and final selected occupied
degree is at most one. U widths are even>=6, heights independently even>=4;
all isometries/translations and rotor phases are allowed.

Keep z,s,t,e,n0,r,J,X and the accepted common-pool bound

    U0+H>=2z+r+J+X,
    mu>=n0-e-floor((s-r-J-X)/2), sigma>=mu.         (1)

Here J is the chain-route count, not the older full-tile count used
in the source-credit definition. Define u8 to count nonexceptional
single-activation doubles that are NOT counted by r and that have
width6 and absolute leg-height difference at most8. Then

    J>=u8.                                        (2)

In particular, if EVERY positive U has width6 and |a-b|<=8, then
z=e=0 and s-r=u8, so (1)-(2) give

    sigma>=mu>=n0>=0,
    |T|+|M|<=mn/2.                                (3)

This has arbitrary source count and reserve. It extends the previous
height-gap-four class; it does not assert a decomposition of arbitrary
grid boundary objects into complete sources.

## 2. Normalize a single-activation width-six double

Reflect sides if necessary. Normalize the unactivated left side of
O=U(6,a,b). The accepted width-six interleaving theorem gives two
distinct original incoming owners L and R with gates

    L tip=(2,2), R tip=(2,5), b<=k<=h-2<=a-4.

Their complete endpoint forms are

    L=F_h(U(vL,h,ell)), F_h(r,c)=(h+2-r,c+1),
    R=G_k(U(vR,k,q)),   G_k(r,c)=(k+2-r,c+4),

with all widths even>=6 and all heights even>=4. L is phase11;
R is phase10 and activates O's right terminal. In particular their
near stems are column2, rows2..h+2, and column5, rows2..k+2.
Their bars contain rows h+1,h+2 from column2 onward, and rows k+1,k+2
from column5 onward. The O bar contains row1, columns1..6.

Assume that L's associated cap-to-tip chain is completely full, so
this marked gate contributes no J route. Its terminal receiver
{2,3}x{2,3} is full. Thus zeta=(2,3) is an endpoint. It is not an
endpoint of O,L,R and has a different original owner V.

## 3. First ownership forces a downward U tip

Use the fixed endpoint stencil

    B=({1}x{1,...,6}) union ({2,...,6}x{2,5}).

B belongs to O,L,R, since h>=k+2>=6 and k>=4. A rotor owner of
zeta is impossible. The exact two-chirality/eight-role table has no
endpoint-disjoint owner against B. Matching zeta to a rotor role fixes
the translation, so this is exhaustion over ALL translations, not a
bounded search. The executable and Lean tables are supplied separately.

Here is the rotor exclusion directly. Normalize its central square as
C={0,1}x{0,1}. The two endpoint forms are
C union{(-1,0),(0,2),(2,1),(1,-1)} and
C union{(-1,1),(1,2),(2,0),(0,-1)}, up to translation.
Quarter-turns preserve each form and reflection interchanges them.
A central rotor point has three original endpoint neighbors, so cannot
fit at zeta with up and left blocked. An outer tip with central neighbor
right has its central square in columns4,5 and contains(2,5).
With central neighbor down, a square in columns2,3 hits(3,2).
A square in columns3,4 and rows3,4 must have its north tip on the
upper-left corner; that pinwheel form has its east tip at(3,5).
Each is a foreign original endpoint. These alternatives exhaust the
two rotor forms. At eta below, only a downward central neighbor is
available, and its central square hits(3,3) or(3,5).

For a U owner, up and left from zeta are foreign endpoints. Every
interior bar point and lower bar corner has three own endpoint neighbors, and each
nonterminal stem point has opposite own endpoint neighbors; both roles
are excluded. At an upper bar corner only right and down can be its two
own directions. A rightward bar collides with (2,5). A downward bar has
its attached stem going right in row2, again colliding with (2,5), since
the incident height is at least4. The only remaining role is a terminal
tip. Its back-ray has length at least4; rightward hits (2,5), so the
back-ray goes down.

Write its incident height d and width v. Its near stem is column3,
rows2..d+2. If its bar went left, it would cross L's stem at rows d+1,d+2,
requiring d>=h+2. But its own near stem would then hit L's bar at row h+1.
Thus its bar goes right, and its exact source is

    V=F_d'(U(v,d,f)), F_d'(r,c)=(d+2-r,c+2).

It is phase10. Its stem must stop before L's bar, and its bar must
start below R's stem. Original endpoint disjointness and even heights give

    k+2<=d<=h-2.                                  (4)

The proof uses the entire original stem and bar, even if some other
source consumes V's original supports later.

## 4. Mandatory support forces a second intermediate U

R's original terminal has exterior support eta=G_k(k,0)=(2,4). This is an
original selection of R and not an endpoint of O,L,R,V. It neighbors
R's tip(2,5) and V's tip(2,3), two persistent endpoints. Complete support
retention therefore forces eta into final P. Let W be its original owner.
None of O,L,R has an endpoint at eta by its displayed stems and bar.
V has near stem in column3, far stem in column v+2>=8 and bar in
rows d+1,d+2, so it also does not own eta. Thus W differs from all
four already identified sources before any endpoint-disjointness argument.

The three sites above, left and right of eta are foreign endpoints:
(1,4) belongs to O, (2,3) to V, and (2,5) to R. A U endpoint with only
one available own-neighbor direction must be a terminal tip pointing
down. A rotor could only use an outer endpoint with its central neighbor
downward. Its central square would then hit V's stem in column3 or R's
stem in column5. Equivalently the exact16-role table against
B union({2,...,6}x{3}) is empty.

Let W's incident height be j. Its stem in column4 must stop before
V's bar, giving j<=d-2. A leftward bar would then cross V's stem, so
the bar goes right. To avoid R's stem it must start below row k+2.
Hence W is the phase11 source

    W=F_j''(U(vW,j,g)), F_j''(r,c)=(j+2-r,c+3),
    k+2<=j<=d-2.                                  (5)

The four original owners L,V,W,R are distinct: they have distinct tips
in row2, and each tip's predecessor is down. Two tips of one original
U can lie in one row only when their separation is its width minus one,
at least5. Here all pairwise separations are at most3. Their original
matching and endpoint ownership are unchanged throughout the argument.

Equations(4)-(5) give the four-stem staircase

    k+2<=j, j+2<=d, d+2<=h, hence h>=k+6.          (6)

This is a necessary condition on a complete feasible fusion with the
full L chain, not a claim that such fusions exist.

## 5. Route every unpaid small-gap double without reuse

If O is not counted by r, the incoming longitudinal height is not tight:
h!=a-2. The existing bound h<=a-2 and evenness sharpen this to h<=a-4.
Together with b<=k and(6), this gives

    a>=h+4>=k+10>=b+10.                            (7)

Consequently an unpaid single-activation width-six double with a-b<=8
CANNOT have a completely full L chain. Its actual marked gate belongs
to J. Choose that gate as its route. Different doubles choose distinct
canonical gates; the original tip/canonical-tile uniqueness in the
accepted chain theorem makes these distinct J occurrences. Thus J>=u8.
No A occurrence is assigned again, and no old H witness is reused.
The common-pool theorem already proves simultaneous disjointness of
these J payments from every 2z+r payment. This proves(2)-(3).

In a failing nonexceptional R1 AA component, r=J=X=0 is already known.
Every width-six double in such a candidate therefore has long-short
height difference at least TEN, and contains the forced four-owner
staircase. Short width8/10 transverse residuals are unchanged. General
full-chain networks, exceptional positives and higher-reserve failures
remain part of the unrestricted objective.

## 6. The far legs impose a height-width budget

Number L,V,W,R from left to right, with tip columns c_i=2+i,
incident heights(d0,d1,d2,d3)=(h,d,j,k), widths v_i>=6 and
far heights f_i>=4. The i-th original far stem is in column
rho_i=c_i+v_i-1, rows d_i+2-f_i through d_i+2. For i<j,
rho_i>c_j. If d_i-d_j<=f_i and rho_i<=rho_j, the point
(d_j+2,rho_i) belongs both to that far stem and to the j-th bar.
This violates original endpoint disjointness. Hence an adjacent pair
satisfies the exact alternative

    v_i>=v_(i+1)+2 OR f_i<=d_i-d_(i+1)-2.

Widths and heights are even. Combining this with the baseline two-row
separation and summing all three adjacent pairs gives

    h-k>=6+sum_{i:v_i<=v_(i+1)} f_i,
    a-b>=10+sum_{i:v_i<=v_(i+1)} f_i              (unpaid double).

Thus at positive height difference10 or12 all three widths must
strictly decrease, forcing(v0,v1,v2,v3)>=(12,10,8,6). If the original
left incoming width is<=10, a full chain on an unpaid double instead
requires a-b>=14. At a-b=10 the incident heights are exactly
(h,d,j,k)=(b+6,b+4,b+2,b). This is not a global descent: a width
may increase when its height gap can accommodate its actual far leg.

The tradeoff was supplied independently in research task64e2d736 and
reconstructed here from the original far-stem coordinates. Its extra
claims are outside the earlier four-stem review request fdbb068e.

## 7. Verification scope

The universal endpoint-role and complete-support arguments above are
the proof. Exact16-role rotor tables and representative independent
dimension/isometry controls check their local inputs. A partial
five-source staircase attains h-k=6 and positive height gap10 with
disjoint original endpoints; it is NOT claimed to be a complete feasible
fusion or a compensation counterexample. Complete physical fixture
coverage of the new four-owner branch is zero.

The Lean companion checks the rotor owner tables, interval crossing,
height separation, unpaid gap10 obstruction and conditional shared-count
allocation. Physical U role/isometry/ownership adapters remain written.
The unrestricted coefficient-one and arbitrary-grid goals remain OPEN.

All18 scoped Lean declarations compile/build and pass individual axiom
audits with only propext, Classical.choice and Quot.sound as applicable,
without sorry/native_decide. The two exact rotor tables have no axioms.
Controls pass7952 U-role tests for each stencil,76 surviving downward
tip roles in each,252 height orders and1785 shared-count cases. The
partial minimal staircase has widths(12,10,8,6) and E-disjointness,
but eight retained supports still fail feasibility. It is not a complete
example. See output/four-stem-compensation-formal-check.json and
output/four-stem-compensation-controls.json. Reproduce controls with:

```sh
python3 develop/check_four_stem_compensation.py --output output/four-stem-compensation-controls.json
```

Independent core review fdbb068e-1440-4879-9155-f0d6effb6a0a completed
ACCEPT at2026-10-20T05:14:02.450UTC, observed gpt_6/pro. Original
stream40409 exits0/DONE and exactly matches the14541-character terminal
response. It accepts the written four-owner/support forcing, J>=u8,
all-reserve gap-eight class and gap-ten residual under the supplied
complete-source dependencies. Its self-contained rotor and owner/support
exposition clarifications are incorporated above. It does not certify
executions or physical realizability. Later height-width additions remain
outside that request. See output/four-stem-compensation-review.json.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
