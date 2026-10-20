# Independent written review of the long-H channel

VERDICT: ACCEPT, under the established model, receipt rules, and  $F_0$  certificate supplied in your request. The permanence lemma, enlarged injective payment, and realization for every even  $z\ge0$  have valid mathematical proofs. The main clarification concerns final selected-point profiles versus original-support provenance; the source-specific ledger invariance also deserves an explicit justification.The reported checker runs, Lean declarations, axiom audits, and exit status remain unverified in this review.1. The enclosure and permanent pair are valid for arbitrary  $b$ Endpoint disjointness gives the claimed equality
$$e=b-2.$$
Indeed, evenness leaves  $e=b-2$  or  $e\ge b$ ; the latter places B’s far-leg endpoint at  $(3,7)$ , which belongs to H’s row- $3$  bar.After this equality, every boundary point of
$$D=[4,b+2]\times[3,7]$$
has the asserted owner:Boundary portionEndpoint supplierRow  $4$ , columns  $3,\ldots,7$ H’s original row- $1$  barRow  $b+2$ , columns  $3,\ldots,7$ B’s original row- $1$  barColumn  $3$ , rows  $5,\ldots,b+1$ H’s near legColumn  $7$ , rows  $5,\ldots,b+1$ B’s far legThe horizontal sides supply all four corners. In particular, B’s far leg begins at physical row  $5$ , and H supplies the corner  $(4,7)$ . H’s near leg ends at row  $b+1$ , immediately above the bottom boundary.The strict interior is
$$\{5,\ldots,b+1\}\times\{4,5,6\}.$$
B and H have no endpoints there. If another source had an interior endpoint and an endpoint outside the strict interior, a unit-edge path in its connected endpoint graph would encounter the occupied boundary. Endpoint disjointness therefore traps its entire endpoint graph in those three columns. The stipulated extent bounds exclude every permitted U and rotor, in every allowed orientation.For either blank candidate  $(5,4)$  or  $(5,5)$ , selection would make the H endpoint immediately above an occupied neighbor. The unique-original-anchor requirement would force H to produce that support. Their intrinsic H coordinates are  $(2,2)$  and  $(2,3)$ , whereas H’s row- $2$  supports have columns  $0$  and  $d+1$ . Thus both positions are empty.The remaining positions are H’s original matching pair
$$(4,4),(4,5),$$
corresponding to intrinsic coordinates  $(1,2),(1,3)$ . This proves the permanent  $2P0T$  profile for all parameters in (1).2. Injection and simultaneous receipt ownership holdThe pair determines its unique original owner H. Its location among H’s original lower-bar pairs then determines the relevant bar end: the opposite candidate pairs have column sets
$$\{4,5\},\qquad \{d,d+1\},$$
which are disjoint for  $d\ge6$ .That end determines  $y$ , the adjacent terminal  $t$ , and B. At  $t=(3,2)$ , the possible producer-anchor position  $(4,2)$  is already B-owned, leaving  $(3,1)$  as the positive producer’s anchor. The established endpoint ownership and canonical-gate reconstruction therefore identify the marked-side claim.The same reconstruction handles the union with old short-H claims. A shared receipt would identify the same B and its same incident leg, requiring that length to be both  $6$  and at least  $8$ .There is also a useful strengthening of the positive-gate exclusion. At each occupied position of  $Q$ , three neighbors are H endpoints and the fourth is one of the permanently blank positions. Consequently, every possible occupied anchor adjacent to that position belongs to H. This excludes a foreign original-support provenance at either occupied position. At the blank positions, any original support would have to remain selected, contradicting the permanent profile. Thus the tile has the required separation from positive-support gate receipts as well as the inherited upper-pair, cap, and triple receipts.The physical set union defining  $p$  is essential and correctly used. Multiple certificates for one pair contribute one receipt. Activation remains in its existing summand of the exact reserve identity.3. The integer bound and its claimed improvement are correctLet
$$h=s+t,\qquad K_*=n_0+p+u.$$
Using the supplied inequalities gives
$$\begin{aligned}
2\mu
&=2N+2R-2G\\
&\ge 2N+A_{\rm activation}+m_8+c+2p+2u-2G\\
&\ge 2n_0+G+q+m_8+c+2p+2u-2G\\
&=2K_*+m_8-h.
\end{aligned}$$
The second inequality uses  $2N\ge2n_0+G$  and  $A_{\rm activation}\ge q$ . Integrality yields
$$\mu\ge n_0+p+u+
\left\lceil\frac{m_8-s-t}{2}\right\rceil.$$
The threshold in (4), including its  $+1$ , follows exactly:
$$s+t\le 2K_*+m_8+1
\quad\Longrightarrow\quad
\left\lceil\frac{m_8-s-t}{2}\right\rceil\ge-K_*.$$
For a genuinely new physical pair, increasing  $p$  by one while moving its claim from  $t$  to  $s$  preserves  $s+t$ . The certified floor rises by one, and the sufficient threshold rises by two. A claim attached to an already counted pair leaves both numerical bounds unchanged.The coefficient-one conclusion follows on configurations satisfying this condition, using the established interpretation of  $\sigma$  and  $\sigma\ge\mu$ . Its improvement over  $5/6$  is exactly  $|M|/6$  on that domain.4. The insertion proof establishes every even parameterHere is an explicit formulation that makes the all-parameter support accounting transparent. Define
$$\tau_z(r,c)=
\begin{cases}
(r,c),&r\le6,\\
(r+z,c),&r\ge7,
\end{cases}$$
and put
$$I_z=\{7,\ldots,6+z\},\qquad
\mathcal C=\{-4,1,2,3,7,8,9,10\}.$$
For  $z=0$ ,  $I_z$  is empty.Writing  $V_z$  for the endpoint union, direct substitution in the source maps gives
$$V_z=\tau_z(V_0)\;\sqcup\;(I_z\times\mathcal C).$$
The inserted endpoint ownership is
$$\{-4,1\}:E,\qquad
\{2,7\}:B,\qquad
\{3,8\}:H,\qquad
\{9,10\}:C.$$
The raw original supports added in each inserted row are exactly:Row parityE supportsB supportsH supportsOdd $\{-5,2\}$  $\{1,8\}$  $\{2,9\}$ Even $\{-3,0\}$  $\{3,6\}$  $\{4,7\}$ C adds bar endpoints and contributes no supports within the slab. The other sources lie wholly in the fixed or translated regions.Subtracting the endpoint columns gives precisely
$$T_z=\tau_z(T_0)\;\sqcup\!
\bigcup_{\substack{r\in I_z\\r\text{ odd}}}
\{r\}\times\{-5\}
\;\sqcup\!
\bigcup_{\substack{r\in I_z\\r\text{ even}}}
\{r\}\times\{-3,0,4,6\}.$$
This also accounts for coincident consumed supports. For example, E and H both produce an odd-row support at column  $2$ , and B’s endpoint consumes both obligations.The retained support-to-anchor assignments are
$$-5\mapsto-4,\quad
-3\mapsto-4,\quad
0\mapsto1,\quad
4\mapsto3,\quad
6\mapsto7.$$
Each selected point has exactly that horizontal occupied neighbor. Its other horizontal neighbor and both vertical neighbors are empty.Both interfaces closeThe complete old row- $7$  pattern is
$$V_0\cap(\{7\}\times\mathbb Z)=\{7\}\times\mathcal C,
\qquad
T_0\cap(\{7\}\times\mathbb Z)=\{(7,-5)\}.$$
Thus the first inserted row reproduces the old row- $7$  pattern exactly, including endpoint owners.The old row- $6$  selected columns are  $\{4,6,21\}$ , all empty in the new row  $7$ ; the new selected point at  $(7,-5)$  also has an empty vertical neighbor in row  $6$ . This verifies the upper interface.At the lower interface, the last inserted row  $6+z$  is even, followed by translated old row  $7$ , now at  $7+z$ . These give the same even/odd compatibility as the slab interior. All subsequent adjacencies are translated old adjacencies.Connectedness has a direct path proofEvery old endpoint edge crossing the cut between rows  $6$  and  $7$  lies in a column of  $\mathcal C$ , and both ends have the same owner, with the assignments displayed above. Each such edge becomes a vertical path within that same source through the inserted rows.Every other old endpoint adjacency remains fixed or translates. Hence connectedness of  $V_0$  implies connectedness of  $V_z$ .Endpoint disjointness follows from the disjoint insertion decomposition and the distinct column ownership. Each displayed U retains the canonical original matching for its new dimensions, so the resulting source matchings are disjoint unit-edge perfect matchings.One distinction should be explicit: the matching itself undergoes canonical re-pairing across the cut. For example, C’s old matching edge in column  $10$  between rows  $6$  and  $7$  acquires the new consecutive pairing along the longer bar. The point-set insertion identity applies to endpoints and selected points; the matching justification comes from the canonical matching of each parameterized U.5. The counts and reserve increment check exactlyFor a U source,
$$|V(U(w,a,b))|=2w+a+b-2.$$
The eleven base endpoint counts sum to  $278$ . B, C, H, and E each gain  $2z$  endpoints, giving
$$|V_z|=278+8z,\qquad |M_z|=139+4z.$$
The base retained-support counts, in the displayed source order, are
$$2,1,0,1,7,10,11,10,5,6,9,$$
which sum to  $62$ . The inserted rows add five selected points per two-row period, so
$$|T_z|=62+\frac{5z}{2}.$$
The odd insertion cut gives exactly  $z/2$  new aligned blocksThe tile row  $\{6,7\}$  retains its endpoint/final-selected profile because the replacement row  $7$  reproduces the old one. The new aligned blocks are
$$\{8,9\},\{10,11\},\ldots,\{6+z,7+z\}.$$
The final odd row here is translated old row  $7$ , which has the required odd-row pattern.For each such block, the complete nonempty tile list is:Even first columnProfile $-6$  $0P1T$  $-4$  $2P1T$  $0$  $2P1T$  $2$  $4P0T$  $4$  $0P1T$  $6$  $2P1T$  $8$  $4P0T$  $10$  $2P0T$ The column- $10$  pair is C’s original bar-matching pair. For an even first row  $v$ , its intrinsic bar coordinates are  $v-1,v$ , an odd/even original matching pair. Both column- $11$  positions are empty.Under the established defect classification, this is the sole new defect contribution, equal to  $2$ . Therefore
$$\Delta(2R)=2\cdot\frac z2=z,
\qquad
R_z=26+\frac z2.$$
Source-specific counters are preserved separatelyEven  $z$  preserves every source’s aligned tile phase. Grouping by whether the intrinsic row and column pair alignments are preserved or shifted gives:PhaseOwnersBoth preservedA, F, KRow preserved, column shiftedB, J, Q0Row shifted, column preservedH, L, MBoth shiftedC, EThis preserves the inherited source classifications.More strongly, all endpoints and original supports of the three positive sources A, F, and K lie in rows at most  $5$ . Their complete radius-one neighborhoods lie in rows at most  $6$ , where the construction preserves occupancy, anchor ownership, and gate geometry. Every added support consumption has producer and consumer among B, H, E, and C.These facts supply the needed justification for retaining the base counters
$$N=3,\quad G=2,\quad
A_{\rm activation}=4,\quad U_0=2,\quad Z_0=0.$$
Consequently,
$$\mu_z=3+\left(26+\frac z2\right)-2
=27+\frac z2.$$
6. Precise manuscript clarificationsI recommend three small additions to make the proof easier to audit.Use “endpoint and final selected-point profiles.”Original-support provenance can move within the tile accounting. For example, M’s consumed terminal support at  $(7,8)$  moves to  $(7+z,8)$ , while an H endpoint still occupies  $(7,8)$ . The permanent physical occupancy statement is correct with the proposed wording.Include the explicit row- $7$  pattern and cut-edge ownership.These establish both interfaces, the count of new aligned blocks, and connectedness directly.Include the source-phase and positive-neighborhood argument.This independently establishes the invariance of  $N,G,A_{\rm activation},U_0,Z_0$ , including quantities whose definitions retain source provenance.The family realizes actual long-H occurrences for every even  $b\ge6$ , with strictly positive margin. The universal residual coverage condition, unrestricted allocation, and rectangular-grid equality retain their stated OPEN status.Retain the lemma and the all-parameter realization, incorporate these explicit interface and provenance justifications, and preserve the stated conditional scope of the coefficient-one conclusion.
