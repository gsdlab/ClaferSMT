/*
All clafers: 2 | Abstract: 0 | Concrete: 2 | References: 0
Constraints: 1
Goals: 0
Global scope: 1..6
Can skip resolver: True
*/
open util/integer
pred show {}
run show for 1 but 1 c0_A, 1 c0_B

fact { 1 <= #c0_A and #c0_A <= 2 }
sig c0_A
{ r_c0_B : set c0_B }
{ 1 <= #r_c0_B and #r_c0_B <= 3 }

sig c0_B
{}
{ one @r_c0_B.this
  (#((this.~@r_c0_B).@r_c0_B)) = 3 }

