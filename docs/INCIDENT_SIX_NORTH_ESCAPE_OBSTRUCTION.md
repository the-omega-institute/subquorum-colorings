# The six-step north escape is impossible; the six-step far return is realizable

21 October 2026. A local three-source obstruction rules out the shortest
north-terminal escape at arbitrary dimensions. In actual marked chains
the surviving escape must have incident leg at least8, so b>=14. This
extends single-use lower-pair compensation to b=12. A separate explicit
complete two-source family shows why the remaining far-leg6 return itself
must not be called impossible. Full allocation and grid equality remain OPEN.

## 1. Complete-source model and the three-source theorem

Keep unique original endpoint ownership, immutable original matchings,
and retention of every unconsumed original support with its original
anchor as its sole occupied neighbor. Consuming a support keeps it occupied.
Optional selections have no endpoint neighbor. Original U widths are even
and at least6, their independent legs even and at least4. Rotors have the
usual eight-endpoint footprint and its reflected chirality, up to lattice
symmetry. No newly encountered consumer is presumed to have a fresh owner.

**Theorem.** Let prescribed sources have frames

    X=U(b-2,a,k), X(r,c)=(c+2,r+3),
    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    H=U(d,6,z), H(r,c)=(b-7+r,c+4),
    b>=8, a,z>=4, d>=6, k in {4,6}, all dimensions legal even integers.

There is no complete original U/rotor family containing these sources.
If their endpoints already overlap, original ownership fails immediately;
the proof below handles every endpoint-disjoint instance. No A/B/C,
marked-side, size bound on d,z or additional-source count is required.

Put p=(b-4,6). It is H's original near inner support, intrinsic (3,2),
with anchor (b-4,5). It is also Q's far-terminal support, intrinsic (5,6),
with a different anchor (b-4,7). Hence it cannot remain a nonendpoint:
two immutable occupied neighbors force it to be consumed. Neither X, Q
nor H originally owns p, so its consumer differs from all three before
their endpoints are used as blockers. Its own endpoint neighbors at p
can only be north/south.

## 2. Unbounded classification of that consumer

No U bar point or outer corner has own neighbors contained in north/south:
inner bar points have three own neighbors, and outer corners have two
perpendicular own neighbors. Thus a U consumer must place p on a vertical
leg, possibly at its terminal. This includes EVERY straight-leg interior
position; an enumeration restricted to terminals and corners would miss it.
The source's horizontal bar lies above or below p.

If the bar lies above p, let S be its outer bar row. Since p is on the
leg rather than the bar, S<=b-6. The vertical leg in column6 from the bar
to p passes through (b-6,6), on H's lower bar. This is an endpoint collision,
independent of which way the bar extends or of both leg lengths.

If the bar lies below p, let T be its outer bar row. Then T>=b-2. If T>=b,
the column6 leg crosses X's far endpoint (b,6). Otherwise T is b-2 or b-1.
A leftward bar contains (T,5), on H's incident leg. A rightward bar has
width>=6 and contains (T,10), on Q's bar. Every possibility collides.

A rotor nontip has three own endpoint neighbors, so it must use a north
or south tip. There are two chiral forms for each direction. Both north
forms contain (b-6,5), an H endpoint; both south forms contain (b-2,5),
also H-owned. Thus every rotor consumer collides too. This exhausts the
catalogue and contradicts the forced endpoint at p, proving the theorem.

The obstruction does not award a reserve or activation. It excludes a
three-source occurrence. It does not require distinct owners for distinct
forced supports, and the shared support p need not have two consumers.

## 3. Stronger escape bound and actual b=12 pair compensation

In the actual chain of the [opposed-stem theorem](OPPOSED_STEM_SUPPORT_GAP_OBSTRUCTION.md),
the lower missing endpoint v=(b-1,5), if present, must have owner

    H=U(d,j,z), H(r,c)=(b-1-j+r,c+4), 6<=j<=b-6.

The new theorem excludes j=6. Legal parity then yields

    8<=j<=b-6, hence b>=14.

The existing upper-to-lower implication excludes the upper missing
endpoint u=(b-2,5) whenever v is absent. For b=12 and k=6, neither point
is therefore an endpoint. Neither is an original X support; any retained
original support there would have to take its west X endpoint as its
original sole anchor, forcing support ownership by X and contradicting
its coordinates. Optional selection is excluded by that endpoint neighbor.
Thus J={b-2,b-1} x {4,5} is a permanent original irregular 2P0T pair.
This extends the earlier b8/10 certificate to b12. The k4/Q6_8_4 class is
already excluded at every b by the [rotor-cavity theorem](SHORT_RETURN_ROTOR_CAVITY_OBSTRUCTION.md).

For actual labelled Vcorner demands, target reconstruction is unchanged:
J identifies X, its adjacent far corner and the opposite actual Vcorner;
the actual B gate and original endpoint ownership recover the positive
producer's labelled side. In the producer frame only (3,1) is an available
positive anchor; the competing (4,2) is B-owned. Equal original leg lengths
do not exchange the physical incident bar end or labelled side.

An old H demand cannot use the same J. The accepted change of frame
Phi(r,c)=(b+3-c,r) transports its transverse source's endpoint (2,2) to
(b+1,2), owned by B. Unique ownership forces that entire source to be B.
Its other required bar endpoint becomes (b+1-h_old,3), h_old>=4, whereas
B has column3 endpoints only in rows b+2,b+3. This is a contradiction,
including the potentially repeated-owner case. Separation from upper
bar pairs and other inventory types uses the same physical X pair profile.

Take the UNION of these b12 demands, earlier b8/10, W10 and short-saturated
Vcorner demands, and all certified H demands. The joint injection uses ONE
physical pair union P: s<=p=|P|. Overlapping certificates, labelled demands
and physical pairs are counted once. Retain all actual A/B/C/X/Q premises,
including C's endpoint (2,5), when using the floor across components.
The intermediate family containing all losing components receives the
floor once; it is not copied component by component. The ledger stays

    mu>=n0+u_upper+p+ceil((m8-s-t_residual+rho)/2).

When all residual demands are covered, t_residual=0 gives

    mu>=n0+u_upper+(p-s)+ceil((m8+s+rho)/2)>=0.

Holding other quantities fixed, the lower-bound gain is exactly the number
of newly certified physical pairs absent from Pold. An already counted
pair adds no capacity. This extends automatic coefficient-one coverage;
it is not a universal improvement of the5/6 bound.

## 4. A complete two-source family prevents an overstrong exclusion

For every even b>=10 and a>=4, the sources

    X=U(b-2,a,6), X(r,c)=(c+2,r+3),
    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r)

alone form a complete original family, using their original matchings
and the union of their original supports minus all endpoints. There is
no extra source or optional selection. This is a complete X/Q family,
NOT a complete actual marked Vcorner chain: it supplies no A/B/C gate or
positive producer, and is not a counterexample to compensation or allocation.

**Proof.** X and Q endpoints are disjoint by their bar and leg intervals.
Their graphs are connected and adjacent along rows b and b+1. Q consumes
X's supports (b+1,3),(b+1,5),(b+1,7),(b+1,9),(b,10), and X consumes Q's
supports (b,4),(b,6),(b,8). No other original support is an endpoint.
The surviving selected vertices are exactly

    X:
      (2,c), c=3,5,...,a+3;
      (3,a+4);
      (4,c), c=6,8,...,a+2;
      (b-1,6),(b-1,8).
    Q:
      (b+2,c), c=3,5,7,9,11;
      (b-5,c), c=7,9,11;
      (b+1,2),(b-4,6),(b-3,8).

Every point has exactly its original endpoint anchor and no other occupied
neighbor, by these intervals and parities. The only closest upper-region
interaction is b=10: X's row4 selected columns are even and Q's row5
selected columns odd, so none are adjacent. For larger b the separation
increases. In the lower region the displayed surviving supports are two
rows apart or in columns two apart; the three exceptional Q supports
have only their listed incident endpoint. These statements also follow
directly from the complete endpoint and selected predicates in the formal
source. Every original endpoint had at least three occupied neighbors
within its source; the union loses no occupied point when a support is
consumed, so this remains true. Original matching edges stay disjoint.
This verifies all completeness conditions, with

    endpoints=2b+a+22, matching_edges=b+a/2+11, selected=a+14.

An even ambient rectangle of size (b+4) x max(a+6,12) contains the family.
The construction proves that k6 cannot be ruled out merely from X/Q.
The realizability of j>=8 north escapes and compatibility with the actual
A/B/C premises remain open.

## 5. Verification status

The proofs are general; finite controls only check them.

- [Independent checker](../develop/check_incident_six_north_escape.py), run
  with `python3 develop/check_incident_six_north_escape.py`, passes72
  endpoint-disjoint prescribed patterns and35,840 bounded U axial roles,
  including32,256 straight-leg interiors. All2,580,480 role/pattern
  comparisons collide. Every endpoint anchor in each bounded U is tested,
  with dimensions at most18; all four rotor forms are checked too.
  It also independently reconstructs307 complete pair families, checks
  original matching, consumption and selected lists, sole original anchors,
  occupied degrees, connectivity, counts and ambient rectangles. The b8
  negative controls prevent extending the construction below its threshold.
  [Concise output](../output/incident-six-north-escape-controls.json).
- [Lean source](../formal/SubQuorum/IncidentSixNorthEscape.lean):20 scoped
  declarations pass Lean4.33.0 and an individual axiom audit, final local
  execution59211 exit0. Only propext/Classical.choice/Quot.sound occur;
  no sorry or native computation trust extension. The arbitrary normalized
  U/rotor blockers, forced-support composition with an explicit catalogue
  adapter, escape arithmetic, exact pair selected/support equivalence and
  unique occupied neighbors are formal. General orientation/ownership
  adapters, actual-demand reconstruction and joint injection, endpoint
  degree inheritance, connectivity, matching and cardinalities remain
  written arguments. [Scope receipt](../output/incident-six-north-escape-formal-check.json).
- Independent written audit0040f102-93ef-4fca-8cbe-516cc23b679b is
  **ACCEPT**. Original stream6776 exits0 with DONE/no errors; its17,087
  character response equals the completed task response exactly, observed
  model gpt_6/pro. It accepts the general obstruction, the conditional
  b12 pair corollary with the supplied accepted reconstruction/ledger
  dependencies, and the complete two-source construction. It does not
  certify code execution, Lean execution, novelty or a global target.
  The suggested distinction between a proved necessary j>=8 bound and
  unresolved longer-escape realizability is incorporated.
  [Receipt](../output/incident-six-north-escape-review.json) and
  [full response](../output/incident-six-north-escape-review-response.md).

The [short-secondary transfer](INCIDENT_EIGHT_NORTH_ESCAPE_TRANSFER.md)
now covers every actual j>=8 escape whose secondary north leg has length6;
j=8 forces this length automatically. It gives one jointly unused positive
activation per eligible residual claim. Secondary legs of length at least8
remain unresolved.

The unrestricted allocation and rectangular-grid
triple equality, actual Vcorner realizations, longer secondary escapes, other
return dimensions, nonmaximal corners and occupied adjacent bands remain OPEN.
Submitted DMGT and primary star-forming/C4-free results are preserved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
