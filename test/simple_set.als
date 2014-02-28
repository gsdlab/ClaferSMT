/*
All clafers: 4 | Abstract: 0 | Concrete: 3 | References: 1
Constraints: 1
Goals: 0
Global scope: 3..18
Can skip resolver: False

B 3..3
  C 1..2
    D 1..3
A -> B 3..3

*/

pred show {}
run show for 1 but 3 c0_A, 3 c0_B, 3 c0_C, 3 c0_D

fact { 3 <= #c0_B and #c0_B <= 3 }
sig c0_B
{ r_c0_C : set c0_C }
{ 1 <= #r_c0_C and #r_c0_C <= 2 }

sig c0_C
{ r_c0_D : set c0_D }
{ one @r_c0_C.this
  1 <= #r_c0_D and #r_c0_D <= 3 }

sig c0_D
{}
{ one @r_c0_D.this }

fact { 3 <= #c0_A and #c0_A <= 3 }
sig c0_A
{ ref : one c0_B }

fact { all disj x, y : c0_A | (x.@ref) != (y.@ref) }
