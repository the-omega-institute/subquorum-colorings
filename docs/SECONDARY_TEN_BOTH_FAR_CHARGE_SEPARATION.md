# Exact source charges and separation of earlier originals

22 October 2026. This addresses the REVISE verdict in audit780b9242
of the both-far selected-pair theorem. Its geometric assessment supports
the gain identity, nonstacking, triple-owner correction and automatic
pair-footprint separation. Its proposed charge correction is false
for the supplied original-source constructor. The proof-text objection
about earlier blocks is valid and has been repaired in the E-frontier
note. No independent acceptance is inferred from this response.

Follow-up dd9cdf7b explicitly withdrew the earlier R charge objection
and confirmed the exhaustive earlier-original separation. It found one
local error in this supplement's original T support partition, with
the correct total unchanged. The partition below is corrected and the
verifier now checks the entire inside-support set. Final confirmation
has been requested in the same conversation; no final ACCEPT is claimed.

## Direct source counts

For R=U(L,10,f) at chart(a-11+r,C+1-c), a and C are odd and all
dimensions even. Its first bar row and leftmost endpoint column are
even. The full two-row bar therefore consists of L/2 physical tiles.
Each leg contributes depth/2 further endpoint tiles, giving

    matching = L+4+f/2,
    endpointTiles = L/2+5+f/2.

The original supports at intrinsic coordinates (0,0) and (0,L+1)
have absolute columns C+1 and C-L. These are respectively in the
next tile to the right and the previous tile to the left of the bar.
Neither far stem nor near stem occupies their tile columns. They are
therefore outside the ENTIRE endpoint tile footprint, not just the bar.
At depth10 the four odd lateral rows3,5,7,9 lie in endpoint tiles;
at depth f the f/2-1 odd lateral rows3,...,f-1 do likewise. Both
axial terminal supports lie in the terminal endpoint tile. Thus

    originalSupportsInside = 4+(f/2-1)+2 = 5+f/2,
    charge(R) = (L+4+f/2)+(5+f/2)-2(L/2+5+f/2) = -1.

For T=U(M,4,g) at chart(a-8+r,s+1-c), the offset is odd/odd.
Its corresponding counts are

    matching = M+1+g/2,
    endpointTiles = M+2+g/2,
    originalSupportsInside = 4+g/2,
    charge(T) = 1-M.

The bar occupies M/2+1 physical tile columns and two physical tile
rows; its leg additions give the displayed endpoint-tile count.
Both original bar-end supports are now inside. The near lateral
supports at intrinsic even rows2,4 contribute2; the far lateral
supports at even rows2,4,...,g contribute g/2. Both axial supports
at intrinsic rows5 and g+1 lie in the next physical tile row beyond
their stem terminals and OUTSIDE the entire endpoint tile footprint.
Hence the inside count is2+2+g/2=4+g/2. The companion verifier
compares the complete predicted inside-support SET in both phases,
including every axial and bar-end inclusion or exclusion.

Both charges are negative. One pair contributes negative mass
1+(M-1)=M and no positive-owner count. The exact selected-pair
Phi identity is unchanged. These counts use immutable original supports,
regardless of which other owners later occupy their locations.

In the audit's concrete triple-owner example, R=U(54,10,26) at
offset(38,2) has matching71, endpointTiles45, insideSupports18:
charge71+18-90=-1. The claimed inside count20 includes the two
outside bar-end supports. T=U(28,4,24) at offset(41,-23) has
matching41, endpointTiles42, insideSupports16 and charge-27.
The pair mass is28, exactly as asserted by the original verifier.
The sharp E witness U(50,10,22) has counts65,41,16 and charge-1.

## Uniform separation from every earlier original

Use the H3 notation and even dimensions of the both-far theorem.
At internal index i, C_i=s_i+w_i+13=s_(i-1)+1 is odd. Partition
the earlier records into the nine base originals B_j, added repair
P_j, west rotor Z_j, south U X_j and the root K.

For every j<i, all B_j endpoints have column at least s_j+2,
including their unbounded long stem. Since offsets decrease, this
is at least s_(i-1)+2=C_i+1. All R endpoints have column at most
C_i. Odd C_i and even C_i+1 lie in different physical tile columns,
so there is no common endpoint tile, mixed full tile or intratile event.
The root has minimum column s_0+w_0+14>=C_i+1 and is separated
by the same argument for arbitrary root breadth.

Earlier P_j,Z_j,X_j may occupy columns at or left of C_i. Their
maximum rows are respectively a_j+2,a_j-1,a_j+2. Since each
anchor gap is at least18, every such endpoint has row at most
a_i-16. R's minimum endpoint row is the even number a_i-11.
Their physical tile rows are therefore strictly smaller than those
of R. This exhausts all earlier originals without any far-leg cutoff.

For R's far strip, the simpler minimum-column bound s_j-4 still
applies. The distinctions above repair the overbroad claim that all
earlier blocks lie to the right. Own-block and first-later-frontier
receipts retain their original proofs and exact sets.

The companion verifier checks the closed-form counts, the exclusion of
both R bar-end supports and inclusion of both T bar-end supports,
and every earlier-owner separation in nonuniform chains. These finite
checks supplement the all-dimension proof. Scoped Lean establishes the
conditional count algebra and the integer physical-row/column bounds;
the source-set counts and chart exhaustion are written arguments.
