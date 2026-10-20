# A strict phase10 height descent and a complete full-pair exit

20 October2026. A forced endpoint need not reserve an original U singleton
slot, even when its receiver is full. This note gives a complete feasible
three-source family witnessing that obstruction and proves the universal
incident-height restriction on its phase10 branch. The unrestricted finite
allocation and rectangular-grid triple equality remain OPEN.

## 1. Universal role and height restriction

Use the complete-source hypotheses of
[the support-injection theorem](DISTINCT_NEUTRAL_SUPPORTS_AND_ANY_PAIR_BUDGET.md).
At an actual neutral01-to-01 contact normalize the forced point to z=(0,0),
the active terminal to p=(1,-1), its predecessor direction to N=(-1,0), and
the passive terminal to q=(1,0), with predecessor direction E=(0,1).
Transport the physical partition: the forced receiver is {-1,0}x{-1,0}.

The active original owner has endpoints (1,-1),(0,-1),(-1,-1); the passive
one has endpoints (1,0),(1,1). The forced point belongs to neither owner.
Suppose its original owner F is a phase10 U. Then F must have z as its
terminal, with predecessor north and the other leg to the east. In particular
F also owns w=(-1,0), so the forced receiver is already full2+2.

Here is an exhaustive dimension-independent role proof. Pull z back to an
endpoint (r,c) of the canonical U(v,h,k), allowing all eight signed coordinate
permutations. A canonical endpoint is either in its two-row bar, on column1
at height2..h, or on columnv at height2..k. The four foreign endpoints west,
south, northwest and southeast cannot belong to F. The transported partition
gives the phase10 parity conditions

    r mod2 = 1 if the row pullback is reflected, otherwise0;
    c mod2 = 0 if the column pullback is reflected, otherwise1.

Splitting the three endpoint roles and eight orientations leaves only the
unreflected vertical pullback with z=(h,1), or its column-reflected analogue
z=(k,v). Both describe a north-directed terminal with the other leg east.
The Lean theorem checks this implication with arbitrary integer dimensions
and the exact original endpoint predicate; it does not assume the desired
role as an arithmetic premise. The minimum widths and heights and their
evenness are explicit hypotheses.

Let a be the active source's incident leg height and h the incident height
of F. The active source's outer bar row is1-a and its inner row is2-a. Its
bar contains column0 because its near stem is in column-1 and its other leg
is to the east, with width at least six. F's near stem contains every point
(t,0) with -h<=t<=0. Since a>=4, the active inner bar point (2-a,0) has row
at most0. Endpoint disjointness therefore requires2-a<-h. Both heights are
even, so

    h+4 <= a.                                                     (1)

Consequently active incident height4 or6 excludes EVERY phase10 owner of z,
not just phase10 singletons or owners on the same port component. The rule
does not exclude phase11, positive, other phase01 or rotor owners.

Equation(1) is a local descent. A phase10 owner has corner ports rather than
the phase01 terminal ports used to generate this contact. There is no proof
that a subsequent continuation repeats this role or preserves its height
parameter. The conditional iterated arithmetic lemma must not be read as a
global termination argument for mixed U/rotor chains.

## 2. A complete feasible two-parameter family

For arbitrary EVEN h>=6 and a>=h+4, take the following THREE original sources:

    O_a = U(14,a,4), (r,c) -> (r+2-a,c-1);
    B   = U(6,4,4),  (r,c) -> (c+1,5-r);
    F_h = U(6,h,4),  (r,c) -> (r+1-h,c).

These displayed coordinates use the ordinary aligned partition. The phases
are01,01,10. Keep their original matchings, take P as their endpoint union,
retain the union of their original supports outside P, and take no optional
selections. Translate by an even vector to fit a finite rectangular grid.

For clarity, subtract(1,1) from every displayed coordinate during the following
geometric verification, transporting the tile partition with it. The contact
has p=(1,-1),q=(1,0),forced z=(0,0), and full receiving tile {-1,0}x{-1,0}.

The original endpoint sets are disjoint. O's bar rows1-a,2-a are strictly
above F's bar rows-h,1-h, since a>=h+4. O's near stem is in column-1, F's
near stem in column0, and their far stems are in columns12 and5. B's bar
occupies columns3,4 in rows1..6; its two stems occupy rows1,6, columns0..4.
F's far terminal has row4-h<=-2, and O's far terminal row5-a<=-5. These
intervals exclude all remaining pairwise endpoint intersections.

Mandatory support retention is feasible. Each source separately has exactly
one own endpoint neighbor at every support. The possible new cross-source
interactions can be checked by the same coordinate intervals, as follows:

| Support group | Cross-source behavior |
|---|---|
| O's inward near-stem supports, column0 and even rows | Those in rows-h..0 are consumed by F; all earlier ones are separated from F's bar by at least two rows. |
| F's exterior near-stem supports, column-1, including its bar-end support | All are consumed by O's near stem. |
| F's near terminal support (1,0) | Consumed by B. |
| B's supports (1,-1) and (0,0) | Consumed by O and F respectively. |
| F's retained inward near-stem supports, column1 and odd rows<=-1 | Their one endpoint anchor is in F's column0; the nearest unconsumed O inward supports have even row, so there is no selected-selected edge. |
| F's far-side retained supports, columns4..6 | Their rows and h>=6 separate them from B's endpoints and supports. |
| O's outer near-stem and far-side supports | Their columns-2 and11..13 separate them from foreign occupied points; each retains only its own anchor. |
| The other eight B supports | The listed endpoint intervals and h>=6,a>=10 leave only their own anchors. |

These classes exhaust the original support lists. Every support outside P
therefore has exactly one occupied neighbor, and the source matching union
is still a matching by endpoint disjointness. This proves complete feasibility
for all parameters, rather than inferring it from finite controls.

## 3. The exact rule this family refutes

In the displayed aligned coordinates p=(2,0) is O's active terminal and
q=(2,1) is B's passive terminal. Their actual receiver has exactly those two
endpoints and retained support(3,0). The forced point z=(1,1) is F's terminal;
F also owns w=(0,1). Its exact original profile in the forced receiver is
regular2P1T, opposite O's regular2P1T pair {(1,0),(0,0)}.

Thus z is NOT an original phase01 terminal singleton or phase10 outer-corner
singleton. It is outside the U-only Pneg pool, and contributes no forced-point
reservation to E1reg. There is no nonfull stop J01 at that forced receiver.
This gives a complete counterexample to the candidate implication

    full forced receiver => its forced point reserves a Pneg slot.

It does not refute the already proved implication z in Pneg => z in E1reg.
It also does not refute coefficient-one allocation or grid equality.

At the explicit parameters a=10,h=6, an even translation fits the construction
in18x18. Independent reconstruction gives78 endpoints,39 matching edges and
27 retained supports, one full endpoint component, and all78 endpoints frozen.
There is one neutral01 contact and no closed specified port component. Its
forced receiver is full with phase10 pair ownership, J01=0 and forced Pneg
reservations0. The actual counts give A=U0=Z0=0,H=12,R=6,mu=6; actual ambient
slack is96. These numerical counts are certified for the explicit instance,
not asserted here as an all-parameter formula.

The family attains a-h=4, proving sharpness of the local height gap. It gives
nonzero complete full-forced-receiver coverage, previously absent from the
support-injection controls. It gives ZERO complete closed01 or AA coverage.

## 4. Verification and remaining finite closure

The Lean source proves the arbitrary-dimension phase10 role classification,
the next-corner endpoint, height descent, short-leg exclusion and conditional
sequence arithmetic. Its geometric transport and active-bar collision adapter
are written above. The complete feasible family is proved by coordinate
intervals and support classes; finite parameter and isometry controls check
these claims but do not replace the general argument.

The new rank excludes phase10 filling of short active01 legs. For long legs,
the complete family shows that a full2+2 exit can genuinely evade the singleton
reservation pool. Continuing the unrestricted proof requires a ledger that
handles these pair exits together with phase11, positive and rotor owners,
without assuming fresh owners or iterating an inapplicable descent parameter.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
