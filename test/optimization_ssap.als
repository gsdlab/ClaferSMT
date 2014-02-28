/*
All clafers: 21 | Abstract: 5 | Concrete: 14 | References: 2
Constraints: 15
Goals: 1
Global scope: 1..*
Can skip resolver: False
*/

pred show {}
run show for 1 but 3 c0_Machine, 10 c0_Requirements, 4 c0_Service, 1 c0_Task, 10 c0_cpu, 4 c0_machine, 1 c0_total_free

abstract sig c0_Service
{ r_c0_requirements : one c0_requirements
, r_c0_machine : one c0_machine }
{ all disj x, y : this.@r_c0_machine | (x.@ref) != (y.@ref)
  this in ((this.@r_c0_machine).(@ref.(@r_c0_services.@ref))) }

sig c0_requirements extends c0_Requirements
{}
{ one @r_c0_requirements.this }

sig c0_machine
{ ref : one c0_Machine }
{ one @r_c0_machine.this }

abstract sig c0_Requirements
{ r_c0_cpu : one c0_cpu }

sig c0_cpu
{ ref : one Int }
{ one @r_c0_cpu.this }

abstract sig c0_Resources extends c0_Requirements
{}

abstract sig c0_Machine
{ r_c0_services : set c0_services
, r_c0_isFree : lone c0_isFree
, r_c0_limits : one c0_limits
, r_c0_utilization : one c0_utilization }
{ all disj x, y : this.@r_c0_services | (x.@ref) != (y.@ref)
  (some this.@r_c0_isFree) <=> (no this.@r_c0_services) }

sig c0_services
{ ref : one c0_Service }
{ one @r_c0_services.this
  (this.(@ref.(@r_c0_machine.@ref))) = (this.~@r_c0_services) }

sig c0_isFree
{}
{ one @r_c0_isFree.this }

sig c0_limits extends c0_Resources
{}
{ one @r_c0_limits.this }

sig c0_utilization extends c0_Resources
{}
{ one @r_c0_utilization.this
  (this.(@r_c0_cpu.@ref)) = (sum temp : ((((this.~@r_c0_utilization).@r_c0_services).(@ref.@r_c0_requirements)).@r_c0_cpu) | temp.@ref)
  (this.(@r_c0_cpu.@ref)) < (((this.~@r_c0_utilization).@r_c0_limits).(@r_c0_cpu.@ref)) }

abstract sig c0_Task
{ r_c0_total_free : one c0_total_free }
{ (this.(@r_c0_total_free.@ref)) = (#(c0_Machine.@r_c0_isFree)) }

sig c0_total_free
{ ref : one Int }
{ one @r_c0_total_free.this }

one sig c0_MyTask extends c0_Task
{}

one sig c0_GoogleCA extends c0_Machine
{}
{ ((this.@r_c0_limits).(@r_c0_cpu.@ref)) = 10 }

one sig c0_GoogleNY extends c0_Machine
{}
{ ((this.@r_c0_limits).(@r_c0_cpu.@ref)) = 16 }

one sig c0_GoogleTX extends c0_Machine
{}
{ ((this.@r_c0_limits).(@r_c0_cpu.@ref)) = 14 }

one sig c0_MailService extends c0_Service
{}
{ ((this.@r_c0_requirements).(@r_c0_cpu.@ref)) = 4 }

one sig c0_SearchService extends c0_Service
{}
{ ((this.@r_c0_requirements).(@r_c0_cpu.@ref)) = 3 }

one sig c0_CalendarService extends c0_Service
{}
{ ((this.@r_c0_requirements).(@r_c0_cpu.@ref)) = 1 }

one sig c0_DriveService extends c0_Service
{}
{ ((this.@r_c0_requirements).(@r_c0_cpu.@ref)) = 2 }

objectives o_global {
maximize c0_MyTask.(@r_c0_total_free.@ref) 
}