ACCEPTThe terminal-rigidity theorem  $h=m$  is valid in the stated complete original U/rotor model, including the two original rotor support–anchor identities explicitly supplied in §3. Both forcing stages close, horizontal straight U interiors are covered, and no same-owner loophole remains.The separate width generalization is also correct within the accepted bar window: if  $g+7-B\le v$ , then  $\omega\le w-2$ .The essential source dependency is the original-support status of the two rotor sites. I verify below their coordinates, anchors, ownership exclusions, and use in the proof. The endpoint footprints alone would not establish original-support membership; your explicit original-support assertions must remain part of the model data. I am not certifying the claimed constructor checks or any execution.1. The top-row no-consumer lemma is validLet
$$s=(b-9,c),\qquad 7\le c\le m+3.$$
Its north neighbor is
$$(b-10,c)=D(1,c-5),$$
an endpoint on  $D$ 's lower bar. If the proposed consumer differs from both that owner and the owner of the occupied south neighbor, its own endpoint neighbors at  $s$  can only be west/east.U roles, including straight interiorsThe complete U degree classification leaves precisely horizontal terminals and horizontal straight leg interiors:A straight leg interior has two opposite own neighbors.A terminal has one own neighbor.An outer bar corner has two perpendicular own neighbors.Every other bar or junction role has degree three.Thus no corner or bar role is omitted.At row  $b-9$ , the prescribed wall endpoints are
$$(b-9,6)=D(2,1),\qquad
(b-9,m+5)=D(2,m).$$
The consumer’s incident horizontal leg is a contiguous endpoint interval containing  $s$ , extending all the way to its outer bar. Because it cannot contain either wall, that entire interval lies in
$$7,\ldots,m+4.$$
Both incident bar columns belong to this interval. This remains true when  $s$  is a straight interior rather than a terminal.The two possible bar directions are then blocked:An upward bar reaches row  $b-10$  immediately and meets  $D$ 's lower bar.A downward bar of width at least six reaches row  $b-5$ , four steps below  $s$ . Both bar columns lie in  $E$ 's incident-row interval
$$7,\ldots,m+9.$$
This excludes every U possibility without any additional enclosure or minimum-extent assumption.All four horizontal rotor tipsThe stated endpoint memberships can be checked directly by rotating the supplied north footprints. Define
$$\rho_W(r,c)=(-c,r),\qquad
\rho_E(r,c)=(c,-r).$$
These send a north-pointing tip to a west-pointing or east-pointing tip, respectively. The four forms are  $\rho_W R_A,\rho_W R_B,\rho_E R_A,\rho_E R_B$ , with the following blockers:FormEndpoint offset from  $s$ Prescribed collisionEast A $(-2,1)$  $D$ 's upper bar at  $(b-11,c+1)$ East B $(-1,2)$  $D$ 's lower bar at  $(b-10,c+2)$ West B $(-2,-1)$  $D$ 's upper bar at  $(b-11,c-1)$ West A,  $c\ge8$  $(-1,-2)$  $D$ 's lower bar at  $(b-10,c-2)$ West A,  $c=7$  $(0,-1)$  $D$ 's near stem at  $(b-9,6)$ The respective column ranges are
$$[8,m+4],\quad [9,m+5],\quad [6,m+2],\quad [6,m+1],$$
so every claimed bar collision is valid. The exceptional  $c=7$  argument correctly uses an actual rotor endpoint—its immediate west neighbor.Vertically directed tips would use a forbidden north or south own neighbor. All nontips have degree three and are excluded already.No hidden  $E$ -self-owner exceptionAlthough the lemma explicitly assumes distinctness only from the north and south owners, its use of  $E$  as a blocker is legitimate. At row  $b-9$ ,  $E$ 's only endpoints are its bar points at columns  $m+8,m+9$ :its incident row is  $b-5$ ;its far row is  $b-4-w\le b-10$ .Hence  $E$  cannot own  $s\in\{b-9\}\times[7,m+3]$ . Likewise,  $D$  cannot own  $s$ , since its only endpoints on that row have columns  $6,m+5$ .The top-row lemma therefore holds with exactly the stated application-specific distinctness requirement.2. The first forcing stage correctly leaves only the two north rotor formsAssume  $h<m$ . Since  $h,m$  are even,
$$h\le m-2.$$
Thus
$$T=m+7-h$$
is odd and satisfies
$$9\le T\le m+3.$$
The point
$$a=(b-6,T-1)=C(h+1,1)$$
is  $C$ 's original beyond-tip support. Its original anchor is east:
$$C(h,1)=(b-6,T).$$
Its south neighbor belongs to  $E$ , because
$$T-1\in[8,m+2]\subseteq[7,m+9].$$
The prescribed-owner exclusions are valid: $Q$  has no endpoint on row  $b-6$ .At that row,  $D$  has only its near-stem endpoint at column  $6$ . $E$  has only its bar endpoints at columns  $m+8,m+9$ . $C$ 's incident leg ends at column  $T$ , so  $a$ , one step farther west, is absent from  $C$ .The other horizontal legs of  $C,E$  are on different rows. Therefore retention forces a consumer distinct from  $Q,D,E,C$ , with own neighbors restricted to north/west.Every U orientation is excludedStraight interiors require opposite own-neighbor directions and cannot fit into  $\{\mathrm N,\mathrm W\}$ . Degree-three roles are also impossible. The remaining possibilities are a north terminal, a west terminal, or a north–west outer corner.A north terminal contains
$$a+(-4,0)=(b-10,T-1),$$
because its incident leg has length at least four.Both outer-corner orientations contain this same point:If the bar runs north, its extent is at least five.If the bar runs west and the incident leg runs north, that leg has length at least four.This explicitly covers the potentially troublesome west-bar/north-leg corner. In every case the point lies on  $D$ 's lower bar, since
$$8\le T-1\le m+2.$$
For a west terminal, let  $J$  be its outer bar column.If  $J\le6$ , its continuous horizontal endpoint segment reaches  $(b-6,6)\in D$ .Otherwise  $J\ge7$ . Both bar columns  $J,J+1$  lie between columns  $7$  and  $T-1$ . An upward bar reaches  $D$ 's lower bar at row  $b-10$ ; a downward bar reaches  $E$ 's incident row at  $b-5$ .Thus every U is excluded. Your phrase “either north-bearing corner” is mathematically sufficient when read this way; explicitly mentioning the west-bar/north-leg case would make the exhaustion easier to audit.Both west rotor chiralities are blockedThe west-form blockers are actual endpoints of the rotated footprints:
$$a+(1,-1)=(b-5,T-2)\in E$$
for West A, since  $T-2\ge7$ ; and
$$a+(1,-2)=(b-5,T-3)$$
for West B.For the latter:If  $T=9$ , this is  $(b-5,6)=D(6,1)$ .If  $T\ge11$ , its column is at least eight and it belongs to  $E$ 's incident row.Consequently, only the two stated north-tip footprints can remain. Any immediate collision of those footprints with prescribed endpoints simply excludes that case earlier. For example, at  $T=9$ ,  $R_A$ 's endpoint
$$a+(-1,-2)=(b-7,6)$$
already meets  $D$ . Your subsequent conditional treatment of nonintersecting footprints is valid.3. The second forcing stage closes both north rotor casesThe required original-support data are:RotorOriginal support relative to  $a$ Original anchor relative to  $a$  $R_A$  $(-3,1)$  $(-2,1)$  $R_B$  $(-3,-1)$  $(-2,-1)$ The coordinate and anchor checks are correct. In each footprint, the support is absent and its only rotor endpoint neighbor is the displayed south anchor.Their physical locations are
$$s_A=(b-9,T),\qquad s_B=(b-9,T-2).$$
Their north neighbors are the distinct  $D$  endpoints
$$(b-10,T)=D(1,T-5),$$
and
$$(b-10,T-2)=D(1,T-7),$$
respectively. These intrinsic column indices are legal throughout the allowed range of  $T$ .The support status is the essential model inputThe retention argument requires these points to be original supports. Having exactly one neighbor in the endpoint footprint would not alone establish that status.Your §3 explicitly supplies the stronger support–anchor identities, so the proof has the needed input. Those identities should remain explicit, or be tied to an exact original-source catalogue statement. The phrase about an independent constructor check is not itself needed for the ordinary proof once these identities are supplied as model data.Every necessary owner exclusion is establishedThe support columns satisfy
$$T\in[9,m+3],\qquad T-2\in[7,m+1],$$
so both lie in the top-row lemma’s interval  $[7,m+3]$ .At row  $b-9$ , the prescribed sources have the following endpoint columns:SourceEndpoint columns at row  $b-9$  $Q$ None $D$  $6,m+5$  $E$  $m+8,m+9$  $C$  $m+6,m+7$ The far legs cannot create additional endpoints on this row:
$$b-4-w\le b-10,\qquad b-5-\omega\le b-11.$$
Thus neither support belongs to  $Q,D,E,C$ . Neither belongs to its respective rotor footprint either.Each original support now has two occupied neighbors:its south rotor anchor;its north  $D$  neighbor.It cannot remain unconsumed. Its consumer must differ from the rotor and from  $D$ , so its own endpoint neighbors can only be west/east. The top-row lemma excludes it.This proves a contradiction for each surviving north rotor case.Same-owner loopholes are closed locallyThe distinctness arguments do not rely on calling a source “new”:The first consumer cannot be  $C$ , because  $a$  is absent from  $C$ 's fixed endpoint set.The second consumer cannot be the first rotor, because its forced site is absent from that rotor’s fixed endpoint set.It cannot be  $D$ ,  $E$ ,  $C$ , or  $Q$ , by the explicit row exclusions.It may in principle be an already encountered, otherwise unmentioned owner. The top-row lemma excludes that owner by its U/rotor geometry just as it excludes any other candidate.No acyclicity or global freshness assumption is being smuggled into either forcing step.4. The terminal and support identities follow exactlyThe contradiction excludes  $h<m$ . Combined with the inherited  $h\le m$ , it gives
$$\boxed{h=m}.$$
Substituting into the original  $C$  coordinates yields
$$z=C(m,1)=(b-6,7),$$

$$C(m+1,1)=(b-6,6)=D(5,1),$$
and
$$C(m,0)=(b-5,7)=E(m+2,1).$$
The consumer roles are exactly as claimed: $D(5,1)$  is a straight near-leg interior, with own endpoint neighbors  $D(4,1)$  and  $D(6,1)$ . $E(m+2,1)$  is  $E$ 's near terminal, since its incident height is  $m+2$ .Because  $D,E$  are prescribed distinct original owners, the two supports have identified, distinct consumers. This is stronger information than merely knowing that both supports are consumed.There is also a useful consistency identity:
$$D(5,2)=(b-6,7)=z.$$
Thus  $z$  consumes  $D$ 's original odd-row lateral support, while  $D(5,1)$  consumes  $C$ 's axial terminal support. This respects the fixed original endpoint and matching model.Finally,  $m+7$  is odd, so the accepted phase calculation makes  $C$  positive and  $z$  its positive near-terminal singleton occurrence. Its activation location is therefore fixed independently of  $\omega,\xi$ .The rigidity proof uses only the legal width lower bounds; it does not need the later sharpening  $\omega\ge8,w\ge10$ .5. The separate width generalization is correctFor the general accepted bar window, put
$$r_0=g+7-B.$$
The existing bound  $B\le g+5$  supplies
$$r_0\ge2.$$
If additionally  $r_0\le v$ , then
$$E(r_0,w)=(b-4-w,B).$$
If  $\omega\ge w$ , the same point is
$$C(0,w-1),$$
a valid outer-bar endpoint of  $C$ . Endpoint disjointness gives
$$\omega<w,$$
and evenness gives
$$\boxed{\omega\le w-2}.$$
The qualification “within the accepted bar window” matters: the condition  $g+7-B\le v$  alone, with unrestricted  $B$ , would not ensure a legal nonnegative intrinsic row. In your intended scope, the inherited upper bound on  $B$  already supplies the required lower bound.Accepted scopeThe theorem proves a necessary terminal location in every complete extension:
$$h=m,\qquad z=(b-6,7),$$
together with the exact consumers and roles of its two original supports.It supplies no existence theorem for such an extension. Fixing this local target also does not prove that different labelled claims select different targets, or that this occurrence avoids all previous reservations. Your decision to make no global injection, reserve, or integer-ledger claim is therefore correct.
