/*
All clafers: 10 | Abstract: 0 | Concrete: 10 | References: 0
Constraints: 8
Goals: 0
Global scope: 1..1
Can skip resolver: True
*/
open util/integer
pred show {}
run show for 1 but 1 c0_g, 1 c0_p, 1 c0_price, 1 c0_r, 1 c0_role, 1 c0_ship, 1 c0_taxrate, 1 c0_total, 1 c0_usergroup

one sig c0_g
{ ref : one Int }

one sig c0_usergroup
{ ref : one Int }

one sig c0_role
{ ref : one Int }

one sig c0_r
{ ref : one Int }

fact { (c0_g.@ref) = (c0_usergroup.@ref) }
fact { (((c0_g.@ref) < 3) && ((c0_g.@ref) = 0)) => ((c0_role.@ref) = 0) }
fact { (((c0_g.@ref) < 3) && ((c0_g.@ref) != 0)) => ((c0_role.@ref) = 1) }
fact { (((c0_g.@ref) > 3) && ((c0_g.@ref) = 9)) => ((c0_role.@ref) = 2) }
fact { (((c0_g.@ref) > 3) && ((c0_g.@ref) != 9)) => ((c0_role.@ref) = (c0_r.@ref)) }
one sig c0_p
{ ref : one Int }

one sig c0_price
{ ref : one Int }

fact { (c0_p.@ref) = (c0_price.@ref) }
one sig c0_total
{ ref : one Int }

one sig c0_taxrate
{ ref : one Int }

one sig c0_ship
{ ref : one Int }

fact { (c0_total.@ref) = (((1.add[(c0_taxrate.@ref)]).mul[(c0_p.@ref)]).add[(c0_ship.@ref)]) }
lone sig c0_notifyAdmin
{}

fact { ((c0_total.@ref) > 500) <=> (some c0_notifyAdmin) }
