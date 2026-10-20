# Gap-eight east terminals: adjacent bands force further endpoint consumers

21 October 2026. This is a propagation lemma for the surviving east-terminal
branch, not an activation injection or a new allocation bound. The unrestricted
mixed allocation and rectangular-grid triple equality remain OPEN.

## 1. Model and branch

Use the complete original U/rotor model of
[the near-tight theorem](NEAR_TIGHT_VCORNER_DOUBLE_ACTIVATION.md): original
endpoints have unique owners, and every original support not consumed by an
endpoint is retained with its original anchor as its sole occupied neighbor.
All widths are even and at least six; both independently chosen leg lengths
are even and at least four. Transport the entire source and its supports.

In the gap-eight normalization, let

    C=U(V,h,f), C(r,c)=(c+1,h+2-r),
    X=U(d,h-8,k), X(r,c)=(c+2,r+3), h>=12.

The X beyond-tip support x=(3,h-4) has its X anchor at (3,h-5) and a
C endpoint at (2,h-4). It must therefore be consumed in any complete
extension. Here we condition on its actual consumer being a U terminal
whose sole own endpoint neighbor is EAST. Other U roles and rotors are
outside this lemma.

**East-terminal rigidity.** After naming the incident leg near, its whole
source necessarily has the frame

    E=U(omega,4,nu), E(r,c)=(c+2,h-r).

Indeed, an incident length at least six would reach the C endpoint
(3,h+1), five steps east of x. The incident length is even and at least
four, so it is four. Its bar has columns h-1,h. An upward bar would meet
C at (2,h), so the bar points down. Its width omega and other leg nu
remain independent. In particular this branch cannot be discarded by the
gap-six eastward-collision argument.

## 2. Adjacent-band propagation lemma

Suppose the endpoint-disjoint C and E above occur in a complete family.
Then omega<=V-2. Moreover exactly one of the following geometric cases holds:

| Case | Mandatory support | Fixed occupied neighbors | Consequence |
|---|---|---|---|
| omega<=V-4 | y=(omega+3,h), an E bar-end support | E at (omega+2,h), C at (omega+3,h+1) | y has an owner other than C,E |
| omega=V-2, f>=nu+4 | zE=(V,h-nu-1), E far beyond-tip support | E at (V,h-nu), C at (V+1,h-nu-1) | zE has an owner other than C,E |
| omega=V-2, f<=nu | zC=(V+1,h+1-f), C far beyond-tip support | C at (V+1,h+2-f), E at (V,h+1-f) | zC has an owner other than C,E |
| omega=V-2, f=nu+2 | zE=(V,h-nu-1), zC=(V+1,h-nu-1) | Each has its own eastern anchor and the other mandatory support | BOTH zE and zC have owners other than C,E |

In every case there is a further endpoint consumer outside C,E. In the last
case the two consumers may be the SAME owner. Nothing asserts a complete
realization of these patterns or validity of their other supports.

**Proof.** C has a far-leg endpoint at (V+1,h), using only f>=4. If
omega>=V, E's bar also contains this point. Disjointness and evenness give
omega<=V-2.

The original E support y=(omega+3,h) is one step beyond the outer bottom
bar corner. Its north neighbor is that E corner, and its east neighbor is
on C's bar because omega+3<=V+1. For omega<=V-4, its row lies strictly
between C's near and far legs; its column is outside C's bar, and its row
exceeds E's last row. Thus neither source owns y, and support retention
forces another original endpoint owner there. That owner may be an already
present source in the complete family; it need not be a newly introduced one.

If omega=V-2, then y=(V+1,h) is itself C's far-leg endpoint, so this
argument gives no additional owner. E's far terminal is e=(V,h-nu),
and C's far terminal is c=(V+1,h+2-f). If f>=nu+4, C contains the
point south of zE: its intrinsic coordinates are (nu+3,V), within the
far leg. If f<=nu, E contains the point north of zC: its intrinsic
coordinates are (f-1,omega), within the far leg. In either case the
listed support is outside both endpoint sets and has its own anchor plus
the other source's endpoint as two distinct neighbors. It must be consumed
by another owner. Evenness leaves only f=nu+2 between these cases.

In that remaining case, put q=h-nu. The terminals are (V,q) and
(V+1,q). E's lateral terminal support is C's terminal; C's lateral
terminal support lies below its own terminal, not above it. Their beyond-tip
supports are zE=(V,q-1) and zC=(V+1,q-1). Each has exactly its own
anchor as endpoint neighbor in C union E: the other terminal is diagonal,
and both legs stop at column q. But BOTH supports remain occupied in every
complete extension, whether selected or consumed. They are adjacent. If either
were selected, it would see its own anchor AND the other occupied support,
contradicting feasibility. Thus BOTH must be endpoints. Neither belongs to
C or E. This is an application of the existing
[source-retention Horn principle](SOURCE_RETENTION_HORN_CLOSURE.md), not a
choice between consuming one support or the other. QED.

## 3. Counting consequence and limits

The single-site inference "the E bottom bar-end support y always has a
consumer outside C,E" fails in the saturated case, where C already owns y.
Nevertheless the matched-return case does NOT stop propagation: checking
only endpoint neighbors would miss the adjacent-support conflict. The table
repairs this local continuation rule using the correct retained occupied set.
Endpoint-disjoint PARTIAL C/E examples test each branch; no complete extension
with the original A/B/X normalization is claimed. There is no counterexample
here to double activation or mu>=0.

No exit above is counted as a positive activation, permanent pair, cap or
m8 receipt. A forced endpoint alone gives none of those conclusions. No
new term is added to the allocation ledger. The next task is to classify
the actual consumers at the three exposed exits, permit recurring owners,
including the simultaneous matched-return pair, without reusing old targets.
The independent far length f is never assumed to reach column h-4; that
stronger condition would require f>=6 and is unavailable in general.

The executable control reconstructs canonical endpoints, supports and
matching independently and checks the four branches, the simultaneous pair's
four selected/endpoint status assignments, and the east-terminal
length/orientation reduction. These finite controls supplement the direct
all-dimensional proof; no complete witness, Lean verification or separate
review is asserted for this new note.

Run `python3 develop/check_gap_eight_adjacent_bands.py`. The control passes
864 anchored terminal roles, of which 84 survive, and 975 endpoint-disjoint
PARTIAL C/E patterns: 675 unsaturated exits, 96 saturated E exits, 180
saturated C exits and 24 matched returns. Each matched return checks all four
selected/endpoint assignments; only simultaneous consumption survives this
two-support test. The receipt is
[gap-eight-adjacent-band-controls.json](../output/gap-eight-adjacent-band-controls.json).

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
