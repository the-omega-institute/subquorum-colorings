# Transverse gates provide compensation and exclude the short-width AA branch

20 October 2026. An unactivated transverse phase11 gate with incident
height4 has a nonfull terminal receiver at every permitted positive
height. At incident height6 and positive height4/6, a full chain forces
a nonfull original irregular-pair receiver. The resulting payments are
injective and separate from all regular-pair chain payments. Combining
them conservatively with the older pool excludes width8/10 doubles from
the nonexceptional R1 AA residual. The finite width-six full-chain closure
and unrestricted mixed allocation remain OPEN.

## 1. Assumptions and actual counts

Use the unchanged complete U/rotor model, original matching/endpoint
ownership, mandatory support retention and final selected occupied
degree at most one. All original endpoint sets are disjoint. Dimensions
are even w>=6 and independent a,b>=4; all isometries, translations and
rotor phases are allowed. Keep the accepted ledger and counts:

    mu=n0+R-(z+s+t+e), sigma>=mu,
    2R=A+U0+Z0+H, A>=s+2t,
    U0+H>=2z+r+J+X.

J is the chain-route count. Define Y to count actual marked gates on
unactivated positive legs of height4/6 whose original owner is a
transverse phase11 U terminal of incident height6 and whose complete
associated cap-to-tip chain is full. Count each gate once. We prove

    U0+H>=J+X+max(2z+r,Y),                         (1)
    mu>=n0-e-floor((s-J-X-max(r,Y-2z))/2).          (2)

The floor and Y-2z in(2) are signed integer operations; max with r>=0
has the same value if Y-2z is first truncated to a natural number.
The maximum is essential: this proof separates Y from J/X, but does
NOT establish separation from every old blank-canonical witness.

## 2. Fixed transverse geometry and a retained blank

Normalize a positive unactivated left leg of height a. Its retained
beyond-tip support(a+1,1) forces

    qA=(a+1,2) outside every original endpoint AND support set.   (3)

The incoming transverse owner B has near stem row2, columns2..h+2;
bar columns h+1,h+2, rows2..v+1; and far stem row F=v+1,
columns h+2-f..h+2. Here v>=6,f>=4 are arbitrary even values.
Its terminal receiver QB={2,3}x{2,3} has original endpoints
(2,2),(2,3), original support(3,3), and blank m=(3,2).

If QB is full, m must have a foreign original owner. Its north and
west neighbors are B's endpoint(2,2) and the positive endpoint(3,1).
Thus the exhaustive U possibilities are an upper corner with own
directions east/south or a terminal with predecessor east/south.
A straight stem interior needs opposite own neighbors, and every
other bar point needs three own neighbors. A rotor could only use an
outer tip with predecessor east/south. These roles cover all dimensions.

For both h=4 and h=6 the rotor role table at m is empty using the positive
column1 endpoints through row4, the retained site(5,1) when a=4,
and B's near stem and first four bar rows. For a>=6, (5,1) is already
a positive endpoint. One may use exactly the same forbidden endpoint
stencil in both cases. Matching m to each of eight roles in either
rotor chirality determines its translation, so all translations are covered.

## 3. Incident height four always breaks the chain

Let h=4, so B's bar is in columns5,6 and its far stem includes(F,2).
A U upper corner with eastward bar hits B at(3,5). A corner with
southward bar has its near leg eastward in row3 and also hits(3,5).
A terminal with east predecessor has at least five consecutive endpoints
in row3 and again hits(3,5).

For a south predecessor of incident height d>=4, the near stem is
column2, rows3..d+3, and its bar rows are d+2,d+3. If its bar goes
right and d+2<=F, it hits B's bar at column5. If d+2>F, its near
stem hits B's far endpoint(F,2). If its bar goes left and d+2<=a,
it hits the positive endpoint(d+2,1). Otherwise d+2>=a+2 by evenness,
and its near stem contains the forbidden endpoint qA. All roles fail.

Consequently QB is not full. It is on the associated cap-to-tip chain,
so this actual gate contributes one J occurrence. No positive height
bound beyond a>=4 is used.

## 4. Incident height six forces a second nonfull receiver

Let h=6 and a in{4,6}. If the B chain is broken it contributes to J.
Assume it full. Then m=(3,2) is an endpoint as above. B's bar is now
in columns7,8. A U corner with eastward bar reaches(3,7). A corner
with southward bar contains qA. A terminal with south predecessor also
contains qA. Rotor ownership is already excluded.

Thus m is a U terminal with east predecessor. Its incident height d
satisfies d+2<7, hence d=4. Its bar cannot go up, since it would hit
B's row2 stem in columns5,6. It goes down. Its exact original owner V
has endpoints

    row3, columns2..6;
    columns5,6, rows3..v'+2;
    row v'+2, columns6-f'..6,

where v'>=6,f'>=4 are arbitrary even values. This is the complete
source image (r,c)->(c+2,6-r) of U(v',4,f'). Its original support
n=(4,3) is anchored at(3,3). In QV={4,5}x{4,5} its exact original
profile is the pair{(4,5),(5,5)} with no original support:2P0T.

Suppose QV were full. Then(4,4) would be an endpoint, forcing the
mandatory support n into P through its two neighbors(3,3),(4,4).
We now exclude every possible foreign original owner of n.

A horizontal U bar or leg through n includes at least five consecutive
endpoints. The forbidden row4 sites at columns1 and5 leave only the
three-site interval2..4 around n, so this is impossible. If n is in
a vertical U bar, the blocked point(3,3) forces that bar to start at
row4, whose bar-end horizontal leg through n is equally impossible.
The only remaining U role is a terminal with predecessor south.

For that tip let its incident height be d>=4, even. Its stem is
column3, rows4..d+4, with bar rows d+3,d+4. A rightward bar hits V's
column5 when d+3<=v'+2; otherwise its stem hits V's far endpoint
(v'+2,3). A leftward bar is excluded by complete supports and(3):

- If a=4, qA=(5,2) is its original interior support.
- If a=6,d=4, qA=(7,2) is its original lower-bar endpoint.
- If a=6,d>=6, qA=(7,2) is its original interior support.

Finally, no rotor can own n. The exact16-role table is empty against
the fixed stencil comprising V's row3 endpoints in columns2..6,
V's column5/6 endpoints in rows4..6, and the forbidden endpoint sites
(4,1),(5,1). The latter is retained support when a=4. In particular
the apparently possible south-tip placement with central columns2,3
forces an outer tip at(5,1), which is forbidden in both cases.

Thus QV is nonfull. Its two other corners cannot be finally selected:
each sees an original V endpoint, and its own endpoint anchor would
have another owner because V has no support in QV. It would have two
occupied neighbors. Hence QV is an actual L2bar or mixed L3 tile,
supplying respectively two or one H units. We select only one.

## 5. Injection, exclusion and the conservative common pool

Each Y occurrence obtains one QV unit. Two different original V owners
cannot assign the same nonfull tile: their two disjoint pairs would
make it full. For a fixed V, the construction identifies an original
terminal tip, its predecessor and bar directions, and the positive
endpoint at its beyond-tip neighbor (normalized(3,1)). That endpoint's
unique original owner identifies the positive leg. Thus one V tip cannot
identify two Y occurrences. If both V tips participate, their witness
tiles lie at opposite bar ends: their bar-axis coordinate intervals
are4..5 and v'..v'+1 in the normalization above. They differ for v'>=6.
The Y tiles are therefore distinct.

Every Y tile contains an original2P0T pair. A J/X regular stopping
tile contains an original2P1T pair. Different owners would require four
endpoints in one nonfull tile; one fixed owner cannot have both profiles
in one tile. A J cap payment contains an original triple; a foreign pair
would require five endpoints, and one owner cannot have both profiles.
Therefore Y is separate from all J/X units. The exact U0/H defect
identity licenses simultaneous addition, giving U0+H>=J+X+Y.

The accepted old assignment gives U0+H>=J+X+2z+r, with the SAME J/X
route choices. Choose the larger remaining family. This proves(1)
without asserting disjointness between Y and the old irregular-pair
payments. Substitute the activation count into the reserve identity:

    2R>=s+2t+J+X+max(2z+r,Y).

Subtract2(z+s+t) and take signed integer floor once to obtain(2).
No full-tile credit, A occurrence or defect slot is paid twice.

## 6. Remove the short-width branch of the AA residual

In a failing nonexceptional R1 component the accepted census forces
n0=z=t=0,s=2,A=2,U0=Z0=H=0,r=J=X=0. If one double has width8/10
and both heights4/6, its unactivated gate is necessarily transverse
phase11. Its incident height h satisfies h+2<w to avoid the opposite
positive endpoint(2,w); evenness gives h<=w-4.

For w=8 this leaves h=4; for w=10 it leaves h=4 or6. Section3 gives
J>=1 in the first case. Section4 gives J>=1 or Y>=1 in the second.
Each contradicts U0=H=0 by(1). Thus BOTH surviving doubles must have
width6. The four-stem theorem then gives height difference at least10
for each. Other sources and their dimensions/phases are still unrestricted.
This does not exclude finite closure of those two width-six staircases.

## 7. Verification and provenance scope

The role classification and mandatory-support arguments above are
general written proofs. Exact rotor tables and representative U
endpoint/support controls supplement them; finite checks do not replace
the proof. The physical owner/profile and Y-tip normalization adapters
are written dependencies rather than an end-to-end Lean theorem.
No complete feasible Y fixture or AA counterexample is asserted.

The transverse argument and height-width tradeoff were proposed by
research task64e2d736, completed at2026-10-20T05:05:00.623UTC, observed
gpt_6/pro. Original stream8313 exits0/DONE and matches its22108-character
terminal response. The four-stem argument was also reconstructed locally
before reading that answer. This research response is not an independent
ACCEPT review of these additions.

All12 scoped Lean declarations compile/build and pass individual axiom
audits with only propext, Classical.choice and Quot.sound as applicable,
without sorry/native_decide. The three exact rotor tables have no axioms.
Controls pass11 height4 contexts,8 height6 contexts with48 forced-owner
profile controls,8 second-support contexts and9375 signed pool cases,
1064 strictly stronger than the previous arithmetic bound. These remain
local role/support tests; complete feasible Y fixture coverage is ZERO.
See output/transverse-gate-compensation-formal-check.json and
output/transverse-gate-compensation-controls.json. Reproduce with:

```sh
python3 develop/check_transverse_gate_compensation.py --output output/transverse-gate-compensation-controls.json
```

Independent review e45d6be7-2e1a-4ef9-a37a-2b71437a2893 remains
dispatched in conv_c4bba27bb36e48a2, original stream51789. It assesses
the new owner/support argument, actual Y injection, maximum pool and
AA exclusion. No verdict is inherited from the research response.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
