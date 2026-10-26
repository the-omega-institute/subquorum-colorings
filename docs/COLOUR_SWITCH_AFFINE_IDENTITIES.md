# Exact nonnegative affine identities for the colour-switch theorem

All symbols and hypotheses are defined in [the proof](ARBITRARY_SELECTION_COLOUR_SWITCH.md). A site rk means (r,k). Retained sites have t=h=0. The expressions below use only integer coefficients. For each case the displayed polynomial identity holds after substituting its fixed indicators. Every term on its right is nonnegative under the written geometric/actual-mate premises. Thus k−d·objective≥0, with k<d, and the integer objective is at most zero.

The identities were reconstructed separately from proof assistance, then expanded with exact arithmetic. Their validity is independent of the optimizer used for discovery.

## Black local budget, objective Δ=δB−h54

### Case 1: t44=1

The identity is

    7 − 9·Δ =
      + 2·(h01+h10-t00)  # degree_t00_h01_h10
      + 2·(h03+h12-t02)  # degree_t02_h03_h12
      + 3·(h03+h05-t04)  # degree_t04_h03_h05
      + 3·(h03+h05+h14-2·t04)  # degree_t04_h03_h05_h14
      + 3·(h07-t06)  # degree_t06_h07
      + 3·(h05+h07-2·t06)  # degree_t06_h05_h07
      + 1·(h03+h14+h23-2·t13)  # degree_t13_h03_h14_h23
      + 2·(h30-t20)  # degree_t20_h30
      + 2·(h23-t22)  # degree_t22_h23
      + 1·(h14-t24)  # degree_t24_h14
      + 4·(h14+h23-2·t24)  # degree_t24_h14_h23
      + 2·(h41-t31)  # degree_t31_h41
      + 2·(h23+h32-t33)  # degree_t33_h23_h32
      + 9·(-3+h34+h43+h54)  # degree_t44_h34_h43_h54
      + 2·(2+h50+h52-t40-t42-t51-t53)  # capacity2
      + 7·(3+h01+h10+h12+h30+h32+h41+h50+h52-t00-t02-t13-t20-t22-t31-t33-t40-t42-t51-t53)  # capacity4
      + 3·(h07)  # nonnegative_h07

Hence the objective is at most 7/9<1, and integrality gives the required nonpositive bound.

### Case 2: t44=0, t33=0, h41=0

The identity is

    1 − 2·Δ =
      + 1·(1-t00)  # bound_t00
      + 1·(h01+h10-t00)  # degree_t00_h01_h10
      + 1·(h01+h03+h12-2·t02)  # degree_t02_h01_h03_h12
      + 1·(h03+h05+h14-2·t04)  # degree_t04_h03_h05_h14
      + 1·(h05+h07-2·t06)  # degree_t06_h05_h07
      + 1·(h12+h14+h23-2·t13)  # degree_t13_h12_h14_h23
      + 1·(h10-t20)  # degree_t20_h10
      + 1·(h30-t20)  # degree_t20_h30
      + 1·(h23+h32-2·t22)  # degree_t22_h23_h32
      + 2·(h34-t24)  # degree_t24_h34
      + 2·(-t31)  # degree_t31_h41
      + 1·(h30+h50-2·t40)  # degree_t40_h30_h41_h50
      + 1·(h32+h43-2·t42)  # degree_t42_h32_h41_h43
      + 1·(h50+h52-2·t51)  # degree_t51_h41_h50_h52
      + 1·(h43+h52+h54-2·t53)  # degree_t53_h43_h52_h54
      + 1·(h07)  # nonnegative_h07
      + 1·(h54)  # nonnegative_h54

Hence the objective is at most 1/2<1, and integrality gives the required nonpositive bound.

### Case 3: t44=0, t33=0, h41=1

The identity is

    3 − 4·Δ =
      + 2·(1-t00)  # bound_t00
      + 2·(h01+h10-t00)  # degree_t00_h01_h10
      + 2·(h01+h03+h12-2·t02)  # degree_t02_h01_h03_h12
      + 2·(h05+h14-t04)  # degree_t04_h05_h14
      + 1·(h03+h05+h14-2·t04)  # degree_t04_h03_h05_h14
      + 2·(h07-t06)  # degree_t06_h07
      + 1·(h05+h07-2·t06)  # degree_t06_h05_h07
      + 1·(1-t13)  # bound_t13
      + 1·(h03+h12+h14+h23-3·t13)  # degree_t13_h03_h12_h14_h23
      + 2·(h10-t20)  # degree_t20_h10
      + 2·(h30-t20)  # degree_t20_h30
      + 2·(h23-t22)  # degree_t22_h23
      + 1·(h12+h23-2·t22)  # degree_t22_h12_h23
      + 4·(h34-t24)  # degree_t24_h34
      + 2·(h30+h32-2·t31)  # degree_t31_h30_h32
      + 2·(h32+h43+h52-2·t42)  # degree_t42_h32_h43_h52
      + 2·(h43+h52+h54-2·t53)  # degree_t53_h43_h52_h54
      + 4·(1+h50-t40-t51)  # capacity3
      + 1·(h07)  # nonnegative_h07
      + 2·(h54)  # nonnegative_h54

Hence the objective is at most 3/4<1, and integrality gives the required nonpositive bound.

### Case 4: t44=0, t33=1, t24=0

The identity is

    8 − 9·Δ =
      + 3·(1-t00)  # bound_t00
      + 3·(h01+h03-t02)  # degree_t02_h01_h03
      + 3·(h05+h14-t04)  # degree_t04_h05_h14
      + 3·(h03+h05+h14-2·t04)  # degree_t04_h03_h05_h14
      + 3·(h07-t06)  # degree_t06_h07
      + 3·(h05+h07-2·t06)  # degree_t06_h05_h07
      + 3·(h03+h14-t13)  # degree_t13_h03_h14
      + 3·(h10-t20)  # degree_t20_h10
      + 3·(h12-t22)  # degree_t22_h12
      + 1·(h30-t31)  # degree_t31_h30
      + 1·(h30+h41-2·t31)  # degree_t31_h30_h41
      + 9·(-3+h23+h32+h34+h43)  # degree_t33_h23_h32_h34_h43
      + 1·(h30+h41-t40)  # degree_t40_h30_h41
      + 1·(1-t42)  # bound_t42
      + 1·(h41+h50-t51)  # degree_t51_h41_h50
      + 1·(h52+h54-t53)  # degree_t53_h52_h54
      + 2·(2+h50+h52-t40-t42-t51-t53)  # capacity2
      + 6·(2+h01+h10+h12+h30+h32+h41+h50+h52-t00-t02-t13-t20-t22-t31-t40-t42-t51-t53)  # capacity4
      + 6·(1-h32)  # bound_h32
      + 3·(h07)  # nonnegative_h07
      + 8·(h54)  # nonnegative_h54

Hence the objective is at most 8/9<1, and integrality gives the required nonpositive bound.

### Case 5: t44=0, t33=1, t24=1, h41=0

The identity is

    2 − 3·Δ =
      + 1·(h01+h10-t00)  # degree_t00_h01_h10
      + 1·(1-t02)  # bound_t02
      + 3·(h03+h05-t04)  # degree_t04_h03_h05
      + 3·(h07-t06)  # degree_t06_h07
      + 1·(1-t13)  # bound_t13
      + 1·(h30-t20)  # degree_t20_h30
      + 1·(h12-t22)  # degree_t22_h12
      + 3·(-3+h14+h23+h34)  # degree_t24_h14_h23_h34
      + 1·(-t31)  # degree_t31_h41
      + 1·(-3+h23+h32+h34+h43)  # degree_t33_h23_h32_h34_h43
      + 1·(h50-t40)  # degree_t40_h41_h50
      + 1·(h43-t42)  # degree_t42_h41_h43
      + 1·(h52-t51)  # degree_t51_h41_h52
      + 1·(h43+h54-t53)  # degree_t53_h43_h54
      + 2·(2+h01+h10+h12+h30+h32+h50+h52-t00-t02-t13-t20-t22-t31-t40-t42-t51-t53)  # capacity4
      + 1·(1-h23)  # bound_h23
      + 1·(1-h34)  # bound_h34
      + 2·(h54)  # nonnegative_h54

Hence the objective is at most 2/3<1, and integrality gives the required nonpositive bound.

### Case 6: t44=0, t33=1, t24=1, h41=1

The identity is

    11 − 12·Δ =
      + 1·(1-t00)  # bound_t00
      + 2·(h01+h10-t00)  # degree_t00_h01_h10
      + 2·(1-t02)  # bound_t02
      + 1·(h01+h12-t02)  # degree_t02_h01_h12
      + 12·(h03+h05-t04)  # degree_t04_h03_h05
      + 12·(h07-t06)  # degree_t06_h07
      + 4·(1-t13)  # bound_t13
      + 1·(h10-t20)  # degree_t20_h10
      + 1·(h10+h30-2·t20)  # degree_t20_h10_h30
      + 3·(h12-t22)  # degree_t22_h12
      + 12·(-3+h14+h23+h34)  # degree_t24_h14_h23_h34
      + 3·(h30-t31)  # degree_t31_h30
      + 4·(-3+h23+h32+h34+h43)  # degree_t33_h23_h32_h34_h43
      + 4·(h43+h52-t42)  # degree_t42_h43_h52
      + 4·(h43+h54-t53)  # degree_t53_h43_h54
      + 1·(4+h01-t00-t02-t20-t22-t31)  # capacity1
      + 4·(1+h50-t40-t51)  # capacity3
      + 8·(3+h01+h10+h12+h30+h32+h50+h52-t00-t02-t13-t20-t22-t31-t40-t42-t51-t53)  # capacity4
      + 4·(1-h23)  # bound_h23
      + 4·(1-h34)  # bound_h34
      + 8·(h54)  # nonnegative_h54

Hence the objective is at most 11/12<1, and integrality gives the required nonpositive bound.

## Colour switch, objective δW under δB≥1

### Case 1: t32=0, t41=0, h00=0

The identity is

    74 − 84·δW =
      + 12·(h01+h10-t00)  # degree_t00_h01_h10
      + 84·(-t01)  # forced_t01_h00
      + 10·(h03+h12-t02)  # degree_t02_h03_h12
      + 15·(1-h03-t03)  # occupancy_(0, 3)
      + 17·(1-t03)  # bound_t03
      + 50·(h02+h13-t03)  # degree_t03_h02_h13
      + 12·(h03+h05-t04)  # degree_t04_h03_h05
      + 12·(h07-t06)  # forced_t06_h07
      + 84·(-t10)  # forced_t10_h00
      + 34·(h02-t12)  # forced_t12_h02
      + 48·(h22-t12)  # forced_t12_h22
      + 5·(h03+h14+h23-2·t13)  # degree_t13_h03_h14_h23
      + 34·(h13+h24-2·t14)  # degree_t14_h13_h15_h24
      + 16·(h24-t14)  # forced_t14_h24
      + 12·(h30-t20)  # forced_t20_h30
      + 12·(h20)  # forced_t21_h20
      + 2·(h12-t22)  # forced_t22_h12
      + 10·(h23-t22)  # forced_t22_h23
      + 14·(1-h23-t23)  # occupancy_(2, 3)
      + 2·(h22+h33-t23)  # degree_t23_h22_h33
      + 34·(h22+h24+h33-2·t23)  # degree_t23_h22_h24_h33
      + 5·(h14+h23-2·t24)  # degree_t24_h14_h23_h25
      + 2·(h14-t24)  # forced_t24_h14
      + 60·(h20+h31-t30)  # degree_t30_h20_h31
      + 12·(h20+h31+h40-2·t30)  # degree_t30_h20_h31_h40
      + 12·(h31)  # nonnegative_h31
      + 12·(h32-t31)  # forced_t31_h32
      + 6·(h23+h34+h43-2·t33)  # degree_t33_h23_h34_h43
      + 24·(h33+h44-2·t34)  # degree_t34_h33_h35_h44
      + 36·(h44-t34)  # forced_t34_h44
      + 12·(h41+h50-t40)  # degree_t40_h41_h50
      + 24·(h33+h42+h44+h53-3·t43)  # degree_t43_h33_h42_h44_h53
      + 6·(h34+h43-2·t44)  # degree_t44_h34_h43_h45
      + 12·(1-h50-t50)  # occupancy_(5, 0)
      + 72·(h40+h51-t50)  # degree_t50_h40_h51
      + 12·(h50+h52-t51)  # degree_t51_h50_h52
      + 48·(h42+h53-t52)  # degree_t52_h42_h53
      + 12·(h42+h51+h53-2·t52)  # degree_t52_h42_h51_h53
      + 2·(2-t02-t03-t12-t13)  # square_0_2
      + 12·(2-t42-t43-t52-t53)  # square_4_2
      + 12·(-1-h01-h03-h05-h07-h10-h12-h14-h23-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 74/84<1, and integrality gives the required nonpositive bound.

### Case 2: t32=0, t41=0, h00=1

The identity is

    25 − 27·δW =
      + 18·(-t00)  # occupancy_(0, 0)
      + 27·(h02-t01)  # forced_t01_h02
      + 18·(h01+h03-t02)  # degree_t02_h01_h03
      + 24·(1-h03-t03)  # occupancy_(0, 3)
      + 3·(1-t03)  # bound_t03
      + 18·(h03+h05-t04)  # degree_t04_h03_h05
      + 18·(h07-t06)  # forced_t06_h07
      + 27·(h20-t10)  # forced_t10_h20
      + 9·(h13+h22-2·t12)  # degree_t12_h11_h13_h22
      + 9·(h22-t12)  # forced_t12_h22
      + 6·(h03+h12+h14+h23-3·t13)  # degree_t13_h03_h12_h14_h23
      + 9·(h13+h24-2·t14)  # degree_t14_h13_h15_h24
      + 9·(h24-t14)  # forced_t14_h24
      + 18·(h10-t20)  # forced_t20_h10
      + 6·(h12+h32-2·t22)  # degree_t22_h12_h21_h32
      + 6·(h12-t22)  # forced_t22_h12
      + 9·(h13+h22+h24+h33-3·t23)  # degree_t23_h13_h22_h24_h33
      + 6·(h14+h23-2·t24)  # degree_t24_h14_h23_h25
      + 6·(h14-t24)  # forced_t24_h14
      + 27·(h31+h40-t30)  # degree_t30_h31_h40
      + 18·(h30-t31)  # forced_t31_h30
      + 6·(h23+h32+h34+h43-3·t33)  # degree_t33_h23_h32_h34_h43
      + 9·(h33+h44-2·t34)  # degree_t34_h33_h35_h44
      + 9·(h44-t34)  # forced_t34_h44
      + 18·(1-h40-t40)  # occupancy_(4, 0)
      + 4·(h32+h41+h52-2·t42)  # degree_t42_h32_h41_h52
      + 2·(h41+h43+h52-2·t42)  # degree_t42_h41_h43_h52
      + 2·(h32+h41+h43+h52-3·t42)  # degree_t42_h32_h41_h43_h52
      + 9·(h33+h42+h44+h53-3·t43)  # degree_t43_h33_h42_h44_h53
      + 6·(h34+h43-2·t44)  # degree_t44_h34_h43_h45
      + 6·(h34-t44)  # forced_t44_h34
      + 9·(1-t50)  # bound_t50
      + 18·(h40+h51-t50)  # degree_t50_h40_h51
      + 10·(h41+h50-t51)  # degree_t51_h41_h50
      + 8·(h50+h52-t51)  # degree_t51_h50_h52
      + 9·(h42+h53-t52)  # degree_t52_h42_h53
      + 9·(h42+h51+h53-2·t52)  # degree_t52_h42_h51_h53
      + 14·(1-t53)  # bound_t53
      + 2·(h43+h52+h54-2·t53)  # degree_t53_h43_h52_h54
      + 2·(1-h54-t54)  # occupancy_(5, 4)
      + 2·(t54)  # nonnegative_t54
      + 18·(-1-h01-h03-h05-h07-h10-h12-h14-h23-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 25/27<1, and integrality gives the required nonpositive bound.

### Case 3: t32=0, t41=1, h23=0

The identity is

    1 − 2·δW =
      + 6·(h01+h10-t00)  # degree_t00_h01_h10
      + 2·(h00-t01)  # forced_t01_h00
      + 2·(1-h02-t02)  # occupancy_(0, 2)
      + 1·(1-t02)  # bound_t02
      + 3·(h03+h12-t02)  # degree_t02_h03_h12
      + 2·(h02+h13-t03)  # degree_t03_h02_h13
      + 3·(h03+h05+h14-2·t04)  # degree_t04_h03_h05_h14
      + 3·(h05+h07-t06)  # degree_t06_h05_h07
      + 3·(h07-t06)  # forced_t06_h07
      + 2·(h20-t10)  # forced_t10_h20
      + 2·(h02-t12)  # forced_t12_h02
      + 3·(h12+h14-2·t13)  # degree_t13_h12_h14_h23
      + 2·(h24-t14)  # forced_t14_h24
      + 6·(h30-t20)  # forced_t20_h30
      + 6·(-t22)  # forced_t22_h23
      + 2·(h22+h33-t23)  # degree_t23_h22_h33
      + 6·(-t24)  # forced_t24_h23
      + 4·(h41-t31)  # forced_t31_h41
      + 2·(h32-t33)  # degree_t33_h23_h32
      + 2·(h32+h34-2·t33)  # degree_t33_h23_h32_h34
      + 2·(h44-t34)  # forced_t34_h44
      + 2·(h41+h50-t40)  # degree_t40_h41_h50
      + 6·(-h41)  # occupancy_(4, 1)
      + 2·(-3+h31+h40+h42+h51)  # degree_t41_h31_h40_h42_h51
      + 2·(h32+h41+h52-2·t42)  # degree_t42_h32_h41_h52
      + 2·(h34+h43-2·t44)  # degree_t44_h34_h43_h45
      + 2·(h34-t44)  # forced_t44_h34
      + 4·(h41+h50-t51)  # degree_t51_h41_h50
      + 2·(h53)  # nonnegative_h53
      + 4·(h43+h52-t53)  # degree_t53_h43_h52
      + 2·(1-t30-t31-t40)  # square_3_0
      + 2·(1-t40-t50-t51)  # square_4_0
      + 2·(2-t42-t43-t52-t53)  # square_4_2
      + 6·(-1-h01-h03-h05-h07-h10-h12-h14-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 1/2<1, and integrality gives the required nonpositive bound.

### Case 4: t32=0, t41=1, h23=1

The identity is

    4 − 5·δW =
      + 1·(h01+h10-t00)  # degree_t00_h01_h10
      + 3·(h00-t01)  # forced_t01_h00
      + 2·(h02-t01)  # forced_t01_h02
      + 1·(1-h02-t02)  # occupancy_(0, 2)
      + 3·(h02+h13-t03)  # degree_t03_h02_h13
      + 1·(h02+h04+h13-2·t03)  # degree_t03_h02_h04_h13
      + 1·(1-h04-t04)  # occupancy_(0, 4)
      + 1·(h05+h07-t06)  # degree_t06_h05_h07
      + 2·(h00+h20-2·t10)  # degree_t10_h00_h11_h20
      + 1·(h20-t10)  # forced_t10_h20
      + 5·(h22-t12)  # forced_t12_h22
      + 1·(h03+h12-t13)  # degree_t13_h03_h12
      + 1·(h13+h24-2·t14)  # degree_t14_h13_h15_h24
      + 3·(h24-t14)  # forced_t14_h24
      + 1·(h30-t20)  # forced_t20_h30
      + 1·(h32-t22)  # forced_t22_h32
      + 5·(-t23)  # occupancy_(2, 3)
      + 1·(h14-t24)  # forced_t24_h14
      + 1·(1-t30)  # bound_t30
      + 2·(h20+h31+h40-2·t30)  # degree_t30_h20_h31_h40
      + 1·(h41-t31)  # forced_t31_h41
      + 1·(1-h33-t33)  # occupancy_(3, 3)
      + 1·(h24+h33-t34)  # degree_t34_h24_h33
      + 2·(h33+h44-2·t34)  # degree_t34_h33_h35_h44
      + 1·(h41+h50-t40)  # degree_t40_h41_h50
      + 1·(-h41)  # occupancy_(4, 1)
      + 3·(-3+h31+h40+h42+h51)  # degree_t41_h31_h40_h42_h51
      + 1·(h33+h44-t43)  # degree_t43_h33_h44
      + 2·(h33+h44+h53-2·t43)  # degree_t43_h33_h44_h53
      + 1·(h34-t44)  # forced_t44_h34
      + 5·(1-t50)  # bound_t50
      + 2·(h42+h51+h53-2·t52)  # degree_t52_h42_h51_h53
      + 1·(h53)  # nonnegative_h53
      + 1·(h43+h52-t53)  # degree_t53_h43_h52
      + 1·(1-t42-t51-t52)  # square_4_1
      + 1·(-2-h01-h03-h05-h07-h10-h12-h14-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 4/5<1, and integrality gives the required nonpositive bound.

### Case 5: t32=1, h13=0, h03=0

The identity is

    0 − 1·δW =
      + 1·(1-h00-t00)  # occupancy_(0, 0)
      + 1·(h01+h10-t00)  # degree_t00_h01_h10
      + 1·(h00-t01)  # forced_t01_h00
      + 1·(h01-t02)  # degree_t02_h01_h03
      + 1·(h12-t02)  # degree_t02_h03_h12
      + 1·(h02-t03)  # degree_t03_h02_h13
      + 2·(h05-t04)  # degree_t04_h03_h05
      + 2·(h07-t06)  # forced_t06_h07
      + 1·(h00-t10)  # forced_t10_h00
      + 1·(-t12)  # forced_t12_h13
      + 1·(h12+h14-2·t13)  # degree_t13_h03_h12_h14
      + 1·(-t14)  # forced_t14_h13
      + 1·(h10+h30-2·t20)  # degree_t20_h10_h21_h30
      + 2·(h32-t22)  # forced_t22_h32
      + 1·(h24-t23)  # degree_t23_h13_h24
      + 1·(h14-t24)  # forced_t24_h14
      + 1·(h23-t24)  # forced_t24_h23
      + 1·(h20+h40-t30)  # degree_t30_h20_h40
      + 2·(h32-t31)  # forced_t31_h32
      + 4·(-h32)  # occupancy_(3, 2)
      + 1·(-3+h22+h31+h33+h42)  # degree_t32_h22_h31_h33_h42
      + 1·(h23+h32-t33)  # degree_t33_h23_h32
      + 1·(h44-t34)  # forced_t34_h44
      + 1·(h30+h50-t40)  # degree_t40_h30_h50
      + 1·(h32+h41-t42)  # degree_t42_h32_h41
      + 2·(h34-t44)  # forced_t44_h34
      + 1·(h41+h50-t51)  # degree_t51_h41_h50
      + 1·(h51+h53-t52)  # degree_t52_h51_h53
      + 2·(h43+h52-t53)  # degree_t53_h43_h52
      + 1·(1-t33-t42-t43)  # square_3_2
      + 1·(2-t40-t41-t50-t51)  # square_4_0
      + 2·(-1-h01-h05-h07-h10-h12-h14-h23-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 0/1<1 (indeed at most zero already), and integrality gives the required nonpositive bound.

### Case 6: t32=1, h13=0, h03=1

The identity is

    2 − 4·δW =
      + 2·(h01+h10-t00)  # degree_t00_h01_h10
      + 4·(h02-t01)  # forced_t01_h02
      + 2·(1-t02)  # bound_t02
      + 4·(-t03)  # occupancy_(0, 3)
      + 2·(h05+h14-t04)  # degree_t04_h05_h14
      + 2·(h07-t06)  # forced_t06_h07
      + 4·(h00-t10)  # forced_t10_h00
      + 4·(-t12)  # forced_t12_h13
      + 2·(h12+h23-t13)  # degree_t13_h12_h23
      + 4·(-t14)  # forced_t14_h13
      + 2·(h30-t20)  # forced_t20_h30
      + 2·(h32-t22)  # forced_t22_h32
      + 4·(h24-t23)  # degree_t23_h13_h24
      + 2·(h34-t24)  # forced_t24_h34
      + 4·(h20+h40-t30)  # degree_t30_h20_h40
      + 2·(h32-t31)  # forced_t31_h32
      + 2·(-h32)  # occupancy_(3, 2)
      + 4·(-3+h22+h31+h33+h42)  # degree_t32_h22_h31_h33_h42
      + 4·(h44-t34)  # forced_t34_h44
      + 1·(h41+h50-t40)  # degree_t40_h41_h50
      + 3·(1-t41)  # bound_t41
      + 2·(1-h43-t43)  # occupancy_(4, 3)
      + 2·(h43-t44)  # forced_t44_h43
      + 3·(1-t50)  # bound_t50
      + 1·(h41+h50-t51)  # degree_t51_h41_h50
      + 4·(h51+h53-t52)  # degree_t52_h51_h53
      + 2·(h43+h52-t53)  # degree_t53_h43_h52
      + 2·(1-t33-t42-t43)  # square_3_2
      + 1·(2-t40-t41-t50-t51)  # square_4_0
      + 2·(-2-h01-h05-h07-h10-h12-h14-h23-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 2/4<1, and integrality gives the required nonpositive bound.

### Case 7: t32=1, h13=1

The identity is

    9 − 15·δW =
      + 3·(1-h00-t00)  # occupancy_(0, 0)
      + 33·(h01+h10-t00)  # degree_t00_h01_h10
      + 15·(h00-t01)  # forced_t01_h00
      + 3·(h01+h12-t02)  # degree_t02_h01_h12
      + 33·(h03+h12-t02)  # degree_t02_h03_h12
      + 15·(1-h03-t03)  # occupancy_(0, 3)
      + 18·(h03+h05-t04)  # degree_t04_h03_h05
      + 18·(h05+h14-t04)  # degree_t04_h05_h14
      + 36·(h07-t06)  # forced_t06_h07
      + 3·(h00+h20-2·t10)  # degree_t10_h00_h11_h20
      + 9·(h20-t10)  # forced_t10_h20
      + 15·(h02-t12)  # forced_t12_h02
      + 36·(-t13)  # occupancy_(1, 3)
      + 15·(h24-t14)  # forced_t14_h24
      + 3·(h10+h30-2·t20)  # degree_t20_h10_h21_h30
      + 30·(h30-t20)  # forced_t20_h30
      + 21·(h32-t22)  # forced_t22_h32
      + 18·(h14+h23-2·t24)  # degree_t24_h14_h23_h25
      + 12·(1-h30-t30)  # occupancy_(3, 0)
      + 3·(h20+h40-t30)  # degree_t30_h20_h40
      + 36·(h32-t31)  # forced_t31_h32
      + 56·(-h32)  # occupancy_(3, 2)
      + 15·(-3+h22+h31+h33+h42)  # degree_t32_h22_h31_h33_h42
      + 18·(h23+h32-t33)  # degree_t33_h23_h32
      + 15·(h44-t34)  # forced_t34_h44
      + 5·(h30+h50-t40)  # degree_t40_h30_h50
      + 4·(h41+h50-t40)  # degree_t40_h41_h50
      + 10·(h30+h41+h50-2·t40)  # degree_t40_h30_h41_h50
      + 4·(h40+h42+h51-2·t41)  # degree_t41_h40_h42_h51
      + 4·(1-h42-t42)  # occupancy_(4, 2)
      + 5·(h32+h41-t42)  # degree_t42_h32_h41
      + 12·(h32+h43-t42)  # degree_t42_h32_h43
      + 36·(h34-t44)  # forced_t44_h34
      + 8·(h40+h51-t50)  # degree_t50_h40_h51
      + 5·(h41+h50-t51)  # degree_t51_h41_h50
      + 12·(h41+h50+h52-2·t51)  # degree_t51_h41_h50_h52
      + 3·(h51+h53-t52)  # degree_t52_h51_h53
      + 12·(h53)  # nonnegative_h53
      + 24·(h43+h52-t53)  # degree_t53_h43_h52
      + 15·(1-t22-t23-t33)  # square_2_2
      + 3·(1-t33-t42-t43)  # square_3_2
      + 7·(2-t40-t41-t50-t51)  # square_4_0
      + 12·(2-t42-t43-t52-t53)  # square_4_2
      + 36·(-1-h01-h03-h05-h07-h10-h12-h14-h23-h30-h32-h34-h41-h43-h50-h52+t00+t02+t04+t06+t13+t20+t22+t24+t31+t33+t40+t42+t44+t51+t53)  # positive_black_deficit

Hence the objective is at most 9/15<1, and integrality gives the required nonpositive bound.
