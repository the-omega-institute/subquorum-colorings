# Actual irregular demand uses half-slots, with one exceptional contact

20 October 2026. We prove a demand bound for the complete fixed-source
U/rotor model of ALL_PHASE_JOINT_COMPENSATION_SLOTS.md. It applies to all
source phases, widths, independent even leg heights, isometries and
feasible complete retained-support fusions, without receiver separation.
The result isolates actual zero-rotor contacts as the event-only residual.
It does not pay marked positive sides automatically in the full class.

## 1. Local theorem

Retain ORIGINAL endpoint ownership. Let k_Q be the irregular event count,
c_Q=2J_Q-Kregular(Q)>=0, and i_Q the number of original irregular-capable
endpoints in Q, including those with no event. A1P1T owner contributes one
to i_Q; a2P0T owner contributes two. Let b_Q indicate a new mixed full
tile with original endpoint-owner partition3+1 and a1P1T singleton.
Then every physical tile satisfies

    2(k_Q-c_Q) <= i_Q+b_Q.                            (1)

The original signed profiles are exactly those displayed in
SINGLETON_NEGATIVE_DEFECT_COMPENSATION.md. A regular event forces a new
mixed full tile, so a nonfull tile has Kregular(Q)=J_Q=c_Q=0.

If a nonfull tile has two final endpoints and an event p->q, these are
adjacent. Let r be p's other intratile neighbor and s the fourth corner.
Since p has only one original blank neighbor, r was occupied originally.
It is not a final endpoint, so it remains selected with anchor p.
Feasibility makes s finally blank. For q's original owner, s was therefore
blank originally; its other intratile neighbor p was occupied originally
and, having a different endpoint owner, was a selection. Both profiles
are1P1T. Only p fires: the blank neighbor of q is s. Hence i_Q=2,k_Q=1,
and (1) is an equality.

If a nonfull tile has three endpoints, its missing corner is finally
blank: any retained selection there would see two endpoints. Each leaf
of this L has that corner as its unique original blank neighbor, so only
the elbow can fire. If it does, a2+1 owner partition has an irregular
2P0T pair and a1P1T singleton; a three-singleton partition has three1P1T
owners. Thus i_Q=3,k_Q=1. A single3P0T owner has no foreign endpoint
inside Q and cannot fire. Tiles without an event satisfy (1) immediately.

An originally full single-owner tile has k_Q=c_Q=i_Q=b_Q=0. For a new
mixed full tile all possible partitions are as follows. Here a counts
irregular pairs and q counts irregular singletons.

| Owner partition | Kregular | k_Q | i_Q | c_Q | b_Q |
|---|---:|---:|---:|---:|---:|
|3+1, regular singleton |2|0|0|0|0|
|3+1, irregular singleton |2|1|1|0|1|
|2+2, a irregular pairs |2-a|2a|2a|a|0|
|2+1+1, a in{0,1}, q in{0,1,2} |1-a|2a+q|2a+q|1+a|0|
|four singletons, q in{0,1,2,3,4} |0|q|q|2|0|

The difference i_Q+b_Q-2(k_Q-c_Q) is respectively0,0,0,2-q and4-q.
It is nonnegative in every row. This proves (1) by a general local
classification, with no inference from a bounded set of source fusions.

## 2. Global budget and automatic subclasses

Let B11 count phase-(1,1) negative U sources. The established exhaustive
source catalogue gives the exact identity

    sum_Q i_Q = 2S-2B11.

Set Bstar=sum_Q b_Q. Split Bstar=BU+BR according to whether the3P0T
owner is a U source or a zero-charge rotor. No other source can have
that profile. Each phase11 U has exactly two such tiles, so BU<=2B11.
Each physical tile has only one three-endpoint owner. Sum (1), then use
integrality and the source bound to obtain

    Kirregular <= S-B11+C+floor(Bstar/2)
               <= S+C+floor(BR/2).                  (2)

There is no double use of credit: c_Q is the remainder AFTER paying all
regular events, and each local inequality uses it only in its own tile.
The original irregular-capable slots likewise occur in one tile each.
The BR count equals the zero-rotor3+1 contact term H of the preceding
notes: the fourth corner is a negative singleton and is the sole negative
owner of that tile. Both notation systems count the same actual contacts.

Together with the ledger sigma>=N+S+C-Kirregular-G, (2) gives

    sigma >= N-G-floor(BR/2).                        (3)

In particular reserve Kirregular+G<=S+C holds whenever G=0 and BR<=1.
Two useful all-contact subclasses follow.

* With no positive U source and with all zero rotors in effective
  phase11, every negative U phase and negative rotor is allowed.
  Here N=G=BR=0, giving sigma>=0 without any receiver-separation or
  density condition.
* With every U source positive and all zero rotors in effective phase11,
  negative rotors are unrestricted. The established rotor barrier gives
  G=0 and there are no3P0T source groups, so BR=0 and sigma>=N.
  This removes the earlier sufficient condition N>=2Rminus for this class.

Both conclusions give |T|+|M|<=mn/2, improving the5/6 matching
coefficient by |M|/6 in their stated classes. The second has additional
slack N. Neither proves a decomposition of arbitrary grid configurations
into the permitted sources or the unrestricted triple equality.

## 3. Exact remaining joint obligation

Define Lambda_Q=i_Q+b_Q-2(k_Q-c_Q)>=0 and Lambda=sum_Q Lambda_Q.
The source identity yields the exact equality

    2(S+C-Kirregular-G)=2B11-BU-BR+Lambda-2G.          (4)

Thus the remaining reserve question is precisely the joint allocation

    2G+BU+BR <= 2B11+Lambda.                         (5)

For the weaker coefficient-one target it suffices to add2N to the right
side. Neither assertion is proved here. In particular a proof cannot
pay G from the same c_Q that already paid the irregular events.

## 4. Verification and provenance

The complete42-profile local relaxation has660 endpoint-disjoint
packings,434 with feasible retained intratile selections. The Python
checker and Lean kernel reduction both verify (1) on this full local
catalogue. Seventeen declarations and individual axiom audits pass in
formal/SubQuorum/SingletonNegativeDefects.lean, including the four exact
rotor phase catalogues and conditional floor/global arithmetic. No
sorryAx/native_decide is used. The geometric catalogue adapter, source
slot identity, marked-side injection and ledger remain written inputs.
Physical fixture checks are recorded in
output/separated-negative-compensation-controls.json; they are controls,
not a substitute for Sections1-2.
All640 complete physical images pass (1)-(4), including the exact source
slot identity and exceptional-owner split. The scalar bound (3) is
nonnegative in592 images and strictly improves the earlier D+H bound in264.
The singleton-defect bound is stronger on other images; neither bound
is claimed to dominate the other in the full source class.

The argument was proposed in Oracle research taskf629ba4e and reconstructed
and independently checked here. Its completed response is archived in
output/actual-joint-reserve-research.json. The separate rotor-only
propagation theorem has now been reconstructed in
ROTOR_ONLY_RESERVE_AND_RECTANGULAR_COMPONENTS.md, with exact owner/support
checks and19scoped Lean declarations. Its separate written-proof review
d8ed1445 completed ACCEPT; that scope is distinct from this note. No manuscript,
email or draft is changed by this research update.

Review5005a44b completed ACCEPT for this note's written half-slot proof,
both automatic subclasses and exact remaining joint identity, with the
original ledger, U catalogue, marked-side injection and rotor barrier as
established inputs. Original stream23629 matches all18005 terminal response
characters exactly, observed gpt_6/pro. It excludes the later rotor-only
propagation theorem and is separate from execution evidence.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
