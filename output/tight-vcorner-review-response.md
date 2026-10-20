Verdict: ACCEPTThe geometric forcing, the bounds  $6\le \ell\le V-4$ , reconstruction of the original labelled side, and nonreuse against every supplied old target type are correct. The proof covers arbitrary permitted widths and independent leg lengths. It does not require a complete witness or a bounded search.The ledger calculation is also correct, using the existing balance
$$\mu=N+R-G$$
and §6’s stated reclassification of tight-Vcorner demands from the former uncertified class. One distinction should be explicit in the accounting argument: negative-singleton status alone does not distinguish these demands from E/S companions. That distinction also uses the actual Vcorner role at the uniquely normalized companion  $y$ . This is separate from—and does not replace—the target nonreuse proof.I find no additional geometric hypothesis needed. My acceptance concerns the written mathematical argument under the established dependencies authorized in the question; it does not certify finite controls or Lean execution.1. Forcing the consumer of  $x$ The tightness assumption and the original lower bound on the incident leg give
$$a=h-4\ge4,\qquad h\ge8.$$
Together with  $h\le w-4$ , this gives  $w\ge12$ , as stated.The prescribed X terminal and its mandatory beyond-tip support are
$$X(a,1)=(3,a+3)=(3,h-1),
\qquad
X(a+1,1)=(3,a+4)=(3,h)=x.$$
The other two fixed endpoint neighbors are
$$C(2,1)=(2,h),\qquad C(1,2)=(3,h+1).$$
Thus  $x$  has fixed endpoint neighbors west, north and east, belonging to the prescribed distinct original owners  $X,C$ .Neither prescribed source already owns  $x$ :At physical row  $3$ , C’s endpoints are its two bar points in columns  $h+1,h+2$ . Its incident leg lies in row  $2$ , and its other leg lies in row  $V+1\ge7$ .At physical row  $3$ , X occupies columns  $3,\ldots,a+3=h-1$ .Consequently, completeness forces an original endpoint to consume  $x$ . Retaining it as X’s support would violate the requirement that its original anchor be its sole occupied neighbor. Optional selections cannot remedy this.The consuming source is different from C and X. Its original endpoint graph is connected and contains more than one point, so its endpoint at  $x$  has an own endpoint neighbor. Unique endpoint ownership excludes north, east and west as own-neighbor directions. Its only possible own endpoint neighbor is therefore south.In the original U, the only own-degree-one endpoints are its two leg terminals. In the supplied rotor, they are precisely its four tips. These are exhaustive alternatives.The rotor exclusion covers all isometriesLet  $\mathcal R$  be the supplied rotor endpoint set. It is invariant under
$$(r,c)\longmapsto(c,5-r),$$
which cycles its four tips. After placing a tip at  $x$  with its own neighbor south, all isometric endpoint footprints therefore reduce to the two reflected placements displayed in the note.Their blocking endpoints are:Rotor placementA rotor endpointThe same point in C $(r,c)\mapsto(r+2,c+h-2)$  $(4,h+1)$  $C(1,3)$  $(r,c)\mapsto(r+2,h+2-c)$  $(5,h+1)$  $C(1,4)$ Both C endpoints exist for every permitted  $V\ge6$ . Each placement violates original endpoint disjointness.This argument excludes every rotor orientation at  $x$ , regardless of transported support-anchor assignments: an endpoint collision already suffices. It does not depend on any finite enumeration of source sizes.2. The forced U frame, upper bound and activationThe consumer must be a U terminal with southward stem. Reindex its intrinsic legs, if necessary, so that the actual target terminal is the incident terminal of length  $\ell$ . This relabelling does not identify the two leg lengths.The incident endpoint column contains every point
$$(r,h),\qquad 3\le r\le\ell+3,$$
including its two bar points at the upper end of this interval.C’s independent far leg contains
$$C(2,V)=(V+1,h).$$
Only the existence of its intrinsic row  $2$  is used; the stipulated  $f\ge4$  supplies it. Avoiding this endpoint forces
$$\ell+3<V+1.$$
Since  $\ell,V$  are even,
$$\boxed{\ell\le V-4.}$$
There are two possible bar directions for a U with this terminal and stem. A right-pointing bar would contain
$$(\ell+2,h+1).$$
This is a C bar endpoint: its column is  $h+1$ , while
$$6\le\ell+2\le V-2$$
places its row inside C’s bar interval  $2,\ldots,V+1$ . Thus the bar must point left, and its placement is exactly
$$\boxed{Q(r,c)=(\ell+3-r,h+1-c).}$$
Both reflection constants are odd. The placement consequently preserves the fixed aligned physical tiles, giving the asserted positive sign.Because  $\ell$  is even, the incident terminal’s two original supports are the beyond-tip support and its even-row lateral support:
$$Q(\ell+1,1)=(2,h),\qquad
Q(\ell,0)=(3,h+1).$$
Both are C-owned endpoints. Hence the original positive terminal at  $x$  is actually activated.The physical tile is
$$\{2,3\}\times\{h,h+1\}.$$
Its four endpoints are
$$Q(\ell,1)=(3,h)$$
and
$$C(2,1)=(2,h),\quad
C(1,1)=(2,h+1),\quad
C(1,2)=(3,h+1).$$
This establishes one activated terminal occurrence, indexed by the original Q owner and its actual terminal index. Consuming both supports does not create two activations, and the proof correctly claims no further reserve at this full tile.3. All dimension branches and both small-width obstructionsWrite
$$j=h+1-\omega$$
for the physical column of Q’s independent far leg. Since  $\omega,h$  are even, the two branches
$$\omega\le h-4
\qquad\text{and}\qquad
\omega\ge h-2$$
are exhaustive.Branch I:  $\omega\le h-4$ The width lower bound  $\omega\ge6$  gives
$$5\le j\le h-5.$$
X occupies physical row  $3$  throughout columns
$$3,\ldots,h-1.$$
If  $\nu\ge\ell$ , the original Q endpoint  $(\ell,\omega)$  exists on its far leg and maps to
$$Q(\ell,\omega)=(3,j).$$
That is an X endpoint, contradicting disjointness. Therefore
$$\nu<\ell.$$
Evenness gives
$$\nu\le\ell-2.$$
Since  $\nu\ge4$ ,
$$\boxed{\ell\ge6.}$$
This is a valid use of the independent far-leg length  $\nu$ . It derives an inequality between  $\nu$  and  $\ell$ ; it never assumes they are equal.Branch II:  $\omega\ge h-2$ Now  $j\le3$ , so Q’s bar contains column  $4$ . In particular,
$$(\ell+2,4)$$
is a Q endpoint.X’s vertical bar occupies column  $4$  in rows  $3,\ldots,d+2$ . If  $\ell\le d$ , the displayed Q endpoint lies on that bar. Hence
$$\ell>d,$$
and evenness yields
$$\boxed{\ell\ge d+2\ge8.}$$
This branch does not use  $\nu$  at all.ConsequencesBoth branches give  $\ell\ge6$ , so the combined interval is
$$\boxed{6\le\ell\le V-4.}$$
Therefore  $V\ge10$ .The two excluded widths are covered separately and correctly: $V=6$ : the upper bound already gives  $\ell\le2$ , contradicting the original  $\ell\ge4$ . $V=8$ : the upper bound gives  $\ell\le4$ , contradicting the strengthened  $\ell\ge6$ .At  $h=8$ , the short-width branch would require  $\omega\le4$ , contrary to  $\omega\ge6$ . Thus only Branch II remains, giving
$$\boxed{\ell\ge d+2,\qquad V\ge d+6.}$$
These are necessary conditions. They do not assert that the remaining dimensions admit a complete extension.The independence of the other legs is preserved throughout:  $f$  is used only to supply  $C(2,V)$ ;  $k$  is not identified with  $a$  or another length; and  $\nu$  enters only the short-width branch. Additional sources cannot remove any of the fixed endpoint collisions used here.4. Reconstruction proves injectivity on labelled claimsThe target is an original terminal occurrence, not an unlabelled grid point. It determines its actual incident leg, its stem direction, and its two original supports, including which support is the outward endcap support.In the recovered normalization these are the ordered supports
$$n=(2,h),\qquad e=(3,h+1).$$
Unique endpoint ownership identifies the same original owner C at both.Their actual C roles are
$$n=C(2,1),\qquad e=C(1,2).$$
These fix the incident bar end and the incident leg. The incident length  $h$ , its original terminal
$$p=C(h,1)=(2,2),$$
and the normalized chart are consequently recoverable.There is no unresolved reflection here. The ordered supports and transported original roles fix the directed axes. The opposite bar end also cannot supply the same tile: the relevant end uses physical rows  $2,3$ , whereas the opposite end uses rows  $V,V+1$ , with  $V\ge6$ . Equal leg lengths would not erase the actual terminal labels or original source roles.The reconstructed chart determines  $t=(3,2)$ , whose actual owner is B. Moreover,
$$B(b-1,1)=(4,2),$$
and this is an original endpoint since  $b\ge6$ .Of the stipulated external producer-anchor possibilities
$$(3,1),\qquad(4,2),$$
the latter is therefore B-owned. The positive producer owns  $(3,1)$ . Unique ownership and the granted canonical gate/producer uniqueness recover the original labelled side of A.Thus two tight-Vcorner claims using the same activated terminal occurrence reconstruct the same original labelled demand. This proves the required injection.5. Nonreuse against every supplied old target typeThe frame comparisons correctly use the incident length of the same actual target terminal. If an old statement names that leg differently, both descriptions can be reindexed by the actual target leg. No equality with Q’s other leg length is needed.Old S targetsLet
$$S(r,c)=(\ell+3-r,3-c).$$
If the target were an old S target, its old producer chart  $F_S$  would satisfy
$$F_S\circ S=Q.$$
Solving gives
$$F_S(r,c)=(r,c+h-2).$$
Its original endpoint  $(0,1)$  would occupy
$$F_S(0,1)=(0,h-1).$$
This is an A endpoint, since  $h\ge8$  and  $h\le w-4$ .The self-owner exclusion is valid. Every endpoint of the hypothetical old producer has physical column at least  $h-1>1$ , whereas A has endpoints in column  $1$ . The hypothetical producer therefore cannot be A under another description. The collision is between distinct original owners.This excludes old S targets for arbitrary permitted producer widths and far-leg lengths.Old P targetsFor the established recipient frame
$$T(r,c)=(c+2,r+2),$$
the equation  $F_P\circ T=Q$  gives
$$F_P(r,c)=(\ell+5-c,h+3-r).$$
The supplied arbitrary-length bound
$$\ell\le w_{\rm old}-4$$
ensures that  $(1,\ell+2)$  is an original bar endpoint of the hypothetical producer. Its image is
$$F_P(1,\ell+2)=(3,h+2)=C(0,2).$$
Again the self-owner exclusion is sound. The hypothetical producer has row-zero bar endpoints on physical column  $h+3$ . Every C endpoint has column at most  $h+2$ , because
$$C(r,c)=(c+1,h+2-r),\qquad r\ge0.$$
The hypothetical producer cannot be C.The P exclusion therefore holds at arbitrary  $\ell$ ; it does not specialize the producer to width six.Old R targetsAn old R target requires one terminal support to be owned by its preceding original rotor. Both supports here are owned by the original U owner C. Unique endpoint ownership excludes an R collision.All-length E/S targetsAn old E/S target requires its two terminal supports to have distinct original U owners. Here both supports have the same original owner C. These ownership profiles are incompatible.Together with the granted joint injectivity of the old transfers, these exclusions establish a single global injection for all old and new demands into actual terminal activations. Repeated owner appearances elsewhere in the family and multiple family components do not affect the argument.6. Demand accounting and the precise ledger effectDemand classification and target nonreuse are different obligations.For the demand classification, the relevant facts are:The new claim has the stipulated negative-singleton gate consumer.Its uniquely normalized companion satisfies
$$y=X(0,1)$$
in the negative Vcorner role.The new class is the tight subclass of those Vcorner demands in the former uncertified remainder, as specified in §6.The first fact distinguishes the gate class from the old alternatives. The actual Vcorner companion role distinguishes it from the catalogue’s E/S companion classes. The phrase “negative singletons, so disjoint” compresses these two distinctions; singleton status by itself would not suffice against E/S.With that stated reclassification,
$$q_{\rm old}=q_0+q_T,\qquad
q=q_{\rm old}+\kappa,\qquad
t=t_{\rm old}-\kappa.$$
Thus
$$G=q+c+s+t$$
is unchanged.The physical injection proves
$$q\le A_{\rm activation}.$$
Using the inherited balance  $\mu=N+R-G$ , the permitted simultaneous inequalities give
$$\begin{aligned}
2\mu
&=(2N-G)+(2R-G)\\
&\ge 2n_0+
 A_{\rm activation}+m_8+c+2p+2u-(q+c+s+t)\\
&=2n_0+2p+2u+m_8-s-t
  +(A_{\rm activation}-q)\\
&\ge 2n_0+2p+2u+m_8-s-t.
\end{aligned}$$
Hence
$$\boxed{
\mu\ge n_0+u+p+
\left\lceil\frac{m_8-s-t}{2}\right\rceil .
}$$
The retained assumption  $s\le p$  is consistent with this substitution; it is not needed to derive this particular displayed bound.There is no new receipt counted here. The established inventory already bounds the full actual activation count together with  $m_8,c,p,u$  in the same family. The new result strengthens the demand-to-activation injection. It does not enlarge  $R$ , change the actual number of activations, or create an additional receipt at the full Q/C tile.Exact improvement and parityLet
$$D=m_8-s-t_{\rm old}.$$
Replacing  $t_{\rm old}$  by  $t_{\rm old}-\kappa$  increases the certified real lower bound for  $2\mu$  by exactly  $\kappa$ . The integer lower-bound improvement is exactly
$$\boxed{
\left\lceil\frac{D+\kappa}{2}\right\rceil
-\left\lceil\frac D2\right\rceil .
}$$
Its parity behavior is:New claimsParity of  $D$ Integer lower-bound improvement $\kappa=2j$ Either $j$  $\kappa=2j+1$ Even $j+1$  $\kappa=2j+1$ Odd $j$ Thus one new claim can produce zero improvement in the integer lower bound, exactly as stated. This remains true for negative  $D$ .Allocation thresholdPut  $B=n_0+u+p$ . The displayed lower bound certifies  $\mu\ge0$  precisely when
$$B+\left\lceil
\frac{m_8-s-t_{\rm old}+\kappa}{2}
\right\rceil\ge0.$$
For integer counts this is equivalent to
$$\boxed{
s+t_{\rm old}
\le 2n_0+2u+2p+m_8+1+\kappa .
}$$
The  $+1$  is correct.This is an equivalent form of the sufficient certificate supplied by the lower bound; it is not asserted to be a necessary condition for actual allocation.Under the stated existing implication through  $\sigma\ge\mu$ , the conditional coefficient-one conclusion follows, with gain
$$\left(1-\frac56\right)|M|=\frac{|M|}{6}.$$
The note correctly stops short of a universal improvement: residual coverage and the arbitrary-grid source decomposition remain separate obligations.7. Accepted scopeThe written proof establishes:arbitrary-extension forcing of an actual positive Q terminal;the full interval  $6\le\ell\le V-4$ ;the  $V=6,8$  no-extension obstructions and the stronger  $h=8$  restriction;injectivity on original labelled claims;nonreuse against every supplied old S/P/R and E/S target type;the stated conditional improvement to the same global ledger.It establishes no complete-extension existence theorem, no universal residual coverage, and no full-grid triple-equality theorem. The note’s limits on those claims are accurate.
