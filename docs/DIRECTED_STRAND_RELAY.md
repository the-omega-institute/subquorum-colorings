# An SS donor can relay along ordered neutral strands

7 October 2026. This extends the [local strand switch](STRAND_SWITCH_NORMAL_FORM.md).
Auxiliary pairings change; the physical feasible pair T,M stays fixed.
The relay uses one donor throughout, not one new budget per visited tile.

## 1. The direction of a neutral-strand switch

At a capacity-two tile of residual degree four, suppose an SS strand Y and
a distinct LS or PS strand Z use the two different auxiliary pairs. Change
to the other perfect adjacent pairing. The new strands still consist of
one SS and one strand of Z's former type. In particular SS+LS gives SS+LS,
and SS+PS gives SS+PS, with the identities of the strands changed.

Cut both old pairs into four arms. The new SS consists of Z's arm ending
at its unique S end joined to one of Y's S arms. The other new strand joins
Z's L/P arm to the other arm of Y. Thus the donor is transported into the
S side of Z. It is not guaranteed to reach a location on the L/P side.
This proves the switch statement and its direction, with all terminal-type
counts, slot reserves and signed shortage fixed.

## 2. An arbitrary-length relay lemma

Consider a fixed initial strand decomposition in a deficient region D.
Choose distinct strands Y_0,Y_1,...,Y_k,X, where Y_0 is SS, each Y_i for
1<=i<=k is LS or PS, and X is LL, LP or PP. Choose distinct tiles
Q_1,...,Q_(k+1), subject to the following explicit incidence conditions:

1. Q_i has r=2,d=4. For 1<=i<=k its two auxiliary pairs belong respectively
   to Y_(i-1) and Y_i. At Q_(k+1) they belong to Y_k and X. No other visit
   of either named strand occurs in that tile.
2. For 1<=i<=k, remove the auxiliary pair of Y_i in Q_i. Its Q_(i+1)
   passage lies on the arm ending at the unique S end of Y_i.

The incidence conditions refer to actual physical endpoint strands, so
they allow bends, long arms, occupied neighboring tiles and other unrelated
strands. They do not infer reachability from an undirected component graph.
The case k=0 is direct debt/SS cancellation at Q_1.

**Theorem 1 (directed donor relay).** Switching pairings successively at
Q_1,...,Q_k transports one SS donor to Q_(k+1). The final switch there
cancels it against X, yielding

    LL+SS -> 2LS,  LP+SS -> LS+PS,  PP+SS -> 2PS.

All intermediate LS/PS type counts are preserved. Total debt and SS counts
each decrease by exactly one, and each local S-end count/color, reserve,
tile charge, physical matching, occupied vertex and boundary edge is fixed.

**Proof.** At the first tile use Section 1. The resulting SS contains the
S arm of Y_1, hence contains its passage at Q_2 by condition 2. No other
initial strand changes, since only Y_0 and Y_1 were reconnected. Inductively,
the active SS contains the S arm of Y_i and its passage at Q_(i+1). The next
Y_(i+1) is an unchanged distinct initial strand, so the same switch applies.
At each stage the active SS replaces its identity; the old one is not kept
in the budget ledger. After k relays it meets X at the last tile. Apply the
local debt-donor switch there. Intermediate counts are unchanged and the
last switch removes exactly one debt and one SS. All changes affect only
auxiliary pairs. QED.

Several relays with disjoint participating initial strands and distinct
switch tiles can pay several distinct debts simultaneously, using one
different initial SS donor per relay. No such disjoint relay packing is
asserted for arbitrary configurations. When all debts are covered by these
relays or the previously assigned distinct reserves, the remaining regional
shortage is nonpositive. Combining that verified allocation with the prior
source-patch hypotheses gives the existing conditional coefficient-one
conclusion. The global source lemma still retains its width-six dependency;
the standalone relay proof is elementary and has no strip dependency.

## 3. What this does and does not resolve

The direct-switch normal form can leave debt and SS strands on different
tiles while neutral LS/PS strands mediate their compensation. The relay
lemma proves that an ordered chain of degree-four passages pays such a debt
without a direct shared tile in the initial decomposition. Donor count never
increases along the chain. The direction condition is essential to this
particular sequential proof: after the first switch, the SS follows the S
arm, not the other arm. No claim excludes other sequences when it fails.

This is an explicit arbitrary-length sufficient geometric class. It does
not prove that every unpaid source admits such a relay, that all relays
can be packed disjointly, or that the unrestricted grid target holds.
Saturated exports, inter-patch edges and genuinely disconnected reserve
budgets remain separate cases. The oracle audit of the earlier terminal
note is still tracked independently; this lemma was developed while that
request ran. The focused manuscript is unchanged.

`develop/check_directed_strand_relay.py` checks the endpoint reconnections
for all debt types, neutral-type words through six relay stages, arbitrary
selected arm subdivisions, and lengths through forty. These are abstract
strand-graph controls, not claims that every word is realized by a feasible
physical grid. The all-size implication for actual feasible configurations
is proved from the explicit incidence assumptions above.
