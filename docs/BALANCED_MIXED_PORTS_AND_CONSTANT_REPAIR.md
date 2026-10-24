# Balanced mixed-port activation preserves payments and restores constant repair

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The prescribed-port obstruction identifies a domain restriction as well as
a cost phenomenon: all original mixed free ends were required to remain
free. We now allow both ends of selected original mixed paths to become
auxiliary-covered. Their opposite physical labels balance exactly. This
extends full-domain payment transfer without spending a beta or interval
on a mixed relay. In the same frozen physical family, activating two such
mixed paths gives a seven-edge repair from the prescribed lower alpha end,
uniformly in W,H,d. The actual matching and candidate edge relation do not
change.

## 1. General balanced-port transfer theorem

Let M be a perfect actual matching on finite P, A the original PP auxiliary
matching, and I the original interval units. Write the original open-strand
counts as k alphas, b betas and g mixed paths, with exact packet ledger

    S_J-B=|I|+b-k.

Suppose f original alphas have distinct old interval payments, each witnessed
at a specified TP free endpoint whose access certificate depends only on
that surviving endpoint, unchanged physical data and the original unit.
Put delta_old=k-f. Choose:

- r distinct unpaid alphas, one free end each;
- r distinct original betas, one free end each;
- t distinct original mixed paths, BOTH free ends of each.

Require 0<=r<=min(delta_old,b), 0<=t<=g. Let U be all these chosen ends,
and F the remaining original free ends. Let N be one matching on declared
permitted auxiliary edges with

    dom(N)=dom(A) disjoint-union U=P setminus F.           (1)

M is fixed. Internal changes may enter any original component. Paid alpha
witnesses remain in F, since the selected alphas are unpaid. An activated
mixed path is not a resource and its two ends are not two beta credits.

Assign physical terminal signs TP minus, BP plus on U, and reversed signs
on F. Selected alpha/beta paths alternate throughout. An activated mixed
path also alternates throughout: its two assigned end signs are opposite.
An inactive mixed path alternates with both end signs reversed. Thus changing
the state of a whole original mixed path just flips its old alternating
signing. Every unselected alpha has one positive actual marker, placed at
its paid end when backed and at a designated end otherwise. Every unselected
beta has one negative actual marker. Original cycles may be flipped.

**Theorem.** For every such N and signing, the numbers of positive and negative
same-sign N edges agree, h_plus=h_minus=h. Transport one different old payment
to every final alpha containing a backed marker. If f_N is the size of this
specific assignment and delta_N=alpha_N-f_N, then

    delta_N <= delta_old-r+h.                            (2)

There is no t loss in (2). The exact inventories are

    2 alpha_N + mixed_N = 2k+g-r-t,
    2 beta_N  + mixed_N = 2b+g-r-t,
    beta_N-alpha_N=b-k,
    alpha_N+beta_N+mixed_N=k+b+g-r-t.                    (3)

Also alpha_N<=k-r+h and beta_N<=b-r+h. If N is coherent, there is
0<=d<=min(k-r,b-r) with

    alpha_N=k-r-d, beta_N=b-r-d,
    mixed_N=g+r-t+2d.                                   (4)

The old interval assignment is replaced, not charged a second time. With
Q_N=|I|-f_N+beta_N the unchanged scalar ledger is S_J-B=Q_N-delta_N.
The grounded-cycle forest certificate still gives
delta_N<=delta_old-r+floor(q/2), with q its number of nonforest constraints.

### Proof

Signs exist on every original strand by the odd alternating M/A edge count.
Both end signs of a mixed path are opposite in either state, so no marker
is introduced when the mixed path is activated. All old A edges cross signs.
The A-covered vertices have sign sum zero. U contains r+t endpoints of each
sign, so the sign sum on dom(N) is zero. Since N is a matching, h_plus=h_minus.

For each final component D the full, uncontracted incidence identity remains

    ends(N|D) disjoint-union (F intersect D)=ends(M|D).

All chosen ends, including the two ends of an activated mixed path, have
both M and N incidences. There is no extra U boundary term. For a final
alpha, signed incidence therefore gives exactly

    M_positive(D)+N_negative(D)
        =M_negative(D)+N_positive(D)+1.                  (5)

A backed positive marker remains incident to its original paid endpoint
in F, which is a degree-one endpoint of the same final component. Hence
its old access certificate transfers. Distinct final components select
distinct markers and therefore distinct original interval units.

There are k-r-f=delta_old-r unbacked positive markers. An alpha with no
backed marker contains an unbacked marker, or, by (5), a negative N edge.
Choose one witness in each such component. The choices are injective into
the tagged disjoint union of unbacked markers and negative N edges. These
witnesses are demands or errors, not resource units. This proves (2).

Exactly r+t original TP ends and r+t original BP ends become covered.
The surviving free-end count proves (3). The same component identity
bounds alphas by all k-r positive markers and h negative N edges; the
beta counterpart uses b-r negative actual markers and h positive N edges.
For h=0 put d=k-r-alpha_N. Equation (3) and these two bounds give (4).
The forest proof is unchanged because active and inactive open-strand
signs are fixed before cycle flips. Finally substitute beta_N-alpha_N=b-k
into the original scalar ledger. QED.

### Correct edge-replacement cost

Equation (1) now implies |N|=|A|+r+t. Thus, with C=|N setminus A| and
q_cut=|A setminus N|,

    C=q_cut+r+t.                                        (6)

The old formula C=q_cut+r applies only when no mixed pair is activated.
The two new mixed ends have balanced charge, but they do require one
additional auxiliary edge per active pair. Their contribution must not
be silently omitted from the repair cost.

## 2. Seven new edges repair the formerly expensive prescribed end

Use the exact frozen three-parameter family and the SAME candidate relation
E of PORT_CHOICE_AND_UNBOUNDED_REMATCHING_COST.md. All coordinates below
are raw. Let W>=6,H>=4 be even, d>=1, and put

    r_0=W+4, R=W+5, a=2d+8.

Keep the lower source fixed at s=(r_0,3). In the central copy, two original
mixed paths are the actual one-edge paths

    BP(r_0,4)--TP(r_0,5),
    BP(r_0,6)--TP(r_0,7).

Activate both of these paths. Choose the RIGHT original beta and its lower
free end t_beta=(R,a+4). Add the two ordinary occupied grid edges

    (r_0,3)--(r_0,4),
    (r_0,5)--(r_0,6).                                   (7)

For the remaining TP tip (r_0,7), use the right lower all-BT portal and
the following A-alternating path:

    (r_0,7), (R,a), (r_0,a), (r_0,a+1), (R,a+1),
    (R,a+2), (r_0,a+2), (r_0,a+3), (R,a+3), (R,a+4).     (8)

It alternates five new edges and four old A edges. Its first edge is a
declared all-BT corridor edge; all other new edges are occupied horizontal
grid edges. All four removed A edges are the old vertical pairs in columns
a,a+1,a+2,a+3 of the lower band. These columns are PP; the last endpoint
(R,a+4) is the original lower BP end of the right beta.

The two edges (7) and path (8) have disjoint auxiliary incidences. After
flipping (8), every old PP vertex remains covered, and the newly covered
original free ends are exactly

    s, t_beta,
    (r_0,4), (r_0,5), (r_0,6), (r_0,7).

Consequently r=1,t=2 in the theorem, and C=7,q_cut=4 as required by (6).
There is no selection, actual-matching, or candidate-edge change.

For coherence, the selected alpha end and both active mixed TP ends are
minus; both active mixed BP ends and the selected right beta end are plus.
Both edges (7) therefore cross. The first PP pair in (8) is an original
two-edge cycle. Give (R,a) plus and (r_0,a) minus. The beta entry
(r_0,a+1) is plus because its A-first M/A continuation to t_beta has even
length. The portal, the next horizontal link and all subsequent M edges
of that continuation cross. Every retained A edge crosses as well.

Thus the complete N is coherent. With original (k,b,g)=(1,2,7), formula
(4) gives

    (alpha_N,beta_N,mixed_N)=(0,1,6).

Exactly one original beta supplies the credit. The two mixed paths and
opened cycle supply no extra resource; no interval unit is used. All old
interval identities remain available once, and the original strictly
positive packet margin is unchanged.

## 3. Relation to the accepted cost obstruction

The earlier theorem fixes all original mixed ends as N-free. Its exact
lower-source cost is min(H+1,W/2+3), unbounded on W=4q,H=2q. That theorem
has independently received ACCEPT, and remains correct on its stated domain.

Here the geometric candidate edges E are unchanged, but the covered domain
is enlarged by two complete original mixed pairs. Its cost from the SAME
lower alpha end is at most seven for every W,H,d. The old isolation proof
deleted precisely these mixed free ends; it cannot be reused after they
become auxiliary-covered. For q>=4, seven is strictly below the old optimum
2q+1. No optimality claim for the new seven-edge repair is made.

This supplies a concrete positive response to the obstruction: balanced
mixed-port activation must be included in joint endpoint/resource search.
It does not prove that every grid has such a continuation or enough different
resources. General grid compensation, universal 5/6 improvement and triple
equality remain open. Outside-overlap correction is still counted once.

## 4. Validation scope

The companion checker passes 334,698 abstract complete replacements and 127
real frozen uniquely matched seven-edge repairs. Combined controls include
1,215,666 backing/sign cases and 2,431,332 exact residual ledgers. It tests
the general signed incidence and partial-payment injection with activated
mixed pairs, and the explicit physical construction.
The all-size result follows from the proof and coordinates above. Earlier
full-domain Lean incidence lemmas apply to the same supplied endpoint
permutation; no full graph or global payment formalization is claimed here.
The record is `output/balanced-mixed-port-compensation-validation.json`.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_balanced_mixed_port_compensation.py --output output/balanced-mixed-port-compensation-validation.json

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
