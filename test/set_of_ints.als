/*
All clafers: 1 | Abstract: 0 | Concrete: 1 | References: 0
Constraints: 2
Goals: 0
Global scope: 2..4
Can skip resolver: True
*/
open util/integer
pred show {}
run show for 1 but 2 c0_A

fact { 2 <= #c0_A and #c0_A <= 4 }
sig c0_A
{ ref : one Int }

fact { all disj x, y : c0_A | (x.@ref) != (y.@ref) }
fact { (#(c0_A.@ref)) = 3 }
