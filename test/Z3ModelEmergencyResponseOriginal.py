from z3 import *
from consts import  METRICS_MAXIMIZE, METRICS_MINIMIZE

FeatureIndexMap = {}
FeatureVariable = []
FeatureIndexMap['searchandrescuefm'] = 0
searchandrescuefm = Bool('searchandrescuefm')
FeatureVariable.append(searchandrescuefm) 
FeatureIndexMap['locationfinding'] = 1
locationfinding = Bool('locationfinding')
FeatureVariable.append(locationfinding) 
FeatureIndexMap['gps'] = 2
gps = Bool('gps')
FeatureVariable.append(gps) 
FeatureIndexMap['radiotriangulation'] = 3
radiotriangulation = Bool('radiotriangulation')
FeatureVariable.append(radiotriangulation) 
FeatureIndexMap['hardwareplatform'] = 4
hardwareplatform = Bool('hardwareplatform')
FeatureVariable.append(hardwareplatform) 
FeatureIndexMap['nexusonehtc'] = 5
nexusonehtc = Bool('nexusonehtc')
FeatureVariable.append(nexusonehtc) 
FeatureIndexMap['droidmotoroal'] = 6
droidmotoroal = Bool('droidmotoroal')
FeatureVariable.append(droidmotoroal) 
FeatureIndexMap['filesharing'] = 7
filesharing = Bool('filesharing')
FeatureVariable.append(filesharing) 
FeatureIndexMap['filemanageropentintents'] = 8
filemanageropentintents = Bool('filemanageropentintents')
FeatureVariable.append(filemanageropentintents) 
FeatureIndexMap['inhousefilemanager'] = 9
inhousefilemanager = Bool('inhousefilemanager')
FeatureVariable.append(inhousefilemanager) 
FeatureIndexMap['reportsynchronization'] = 10
reportsynchronization = Bool('reportsynchronization')
FeatureVariable.append(reportsynchronization) 
FeatureIndexMap['explicitreportssync'] = 11
explicitreportssync = Bool('explicitreportssync')
FeatureVariable.append(explicitreportssync) 
FeatureIndexMap['implicitreportssync'] = 12
implicitreportssync = Bool('implicitreportssync')
FeatureVariable.append(implicitreportssync) 
FeatureIndexMap['chatprotocol'] = 13
chatprotocol = Bool('chatprotocol')
FeatureVariable.append(chatprotocol) 
FeatureIndexMap['openfire'] = 14
openfire = Bool('openfire')
FeatureVariable.append(openfire) 
FeatureIndexMap['inhousechatprotocol'] = 15
inhousechatprotocol = Bool('inhousechatprotocol')
FeatureVariable.append(inhousechatprotocol) 
FeatureIndexMap['mapaccess'] = 16
mapaccess = Bool('mapaccess')
FeatureVariable.append(mapaccess) 
FeatureIndexMap['ondemandgooglesite'] = 17
ondemandgooglesite = Bool('ondemandgooglesite')
FeatureVariable.append(ondemandgooglesite) 
FeatureIndexMap['cachedgoogleserver'] = 18
cachedgoogleserver = Bool('cachedgoogleserver')
FeatureVariable.append(cachedgoogleserver) 
FeatureIndexMap['preloadedesri'] = 19
preloadedesri = Bool('preloadedesri')
FeatureVariable.append(preloadedesri) 
FeatureIndexMap['connectivity'] = 20
connectivity = Bool('connectivity')
FeatureVariable.append(connectivity) 
FeatureIndexMap['wifi'] = 21
wifi = Bool('wifi')
FeatureVariable.append(wifi) 
FeatureIndexMap['threegnexusone'] = 22
threegnexusone = Bool('threegnexusone')
FeatureVariable.append(threegnexusone) 
FeatureIndexMap['threedroid'] = 23
threedroid = Bool('threedroid')
FeatureVariable.append(threedroid) 
FeatureIndexMap['bluetooth'] = 24
bluetooth = Bool('bluetooth')
FeatureVariable.append(bluetooth) 
FeatureIndexMap['database'] = 25
database = Bool('database')
FeatureVariable.append(database) 
FeatureIndexMap['mysql'] = 26
mysql = Bool('mysql')
FeatureVariable.append(mysql) 
FeatureIndexMap['sqlite'] = 27
sqlite = Bool('sqlite')
FeatureVariable.append(sqlite) 
FeatureIndexMap['architecturalstyle'] = 28
architecturalstyle = Bool('architecturalstyle')
FeatureVariable.append(architecturalstyle) 
FeatureIndexMap['peertopeer'] = 29
peertopeer = Bool('peertopeer')
FeatureVariable.append(peertopeer) 
FeatureIndexMap['clientserver'] = 30
clientserver = Bool('clientserver')
FeatureVariable.append(clientserver) 
FeatureIndexMap['pushbased'] = 31
pushbased = Bool('pushbased')
FeatureVariable.append(pushbased) 
FeatureIndexMap['dataexchangeformat'] = 32
dataexchangeformat = Bool('dataexchangeformat')
FeatureVariable.append(dataexchangeformat) 
FeatureIndexMap['xml'] = 33
xml = Bool('xml')
FeatureVariable.append(xml) 
FeatureIndexMap['compressedxml'] = 34
compressedxml = Bool('compressedxml')
FeatureVariable.append(compressedxml) 
FeatureIndexMap['unformatteddata'] = 35
unformatteddata = Bool('unformatteddata')
FeatureVariable.append(unformatteddata) 
s = Solver()


#Parent-Children
s.add(Implies(locationfinding, searchandrescuefm))
s.add(Implies(hardwareplatform, searchandrescuefm))
s.add(Implies(filesharing, searchandrescuefm))
s.add(Implies(reportsynchronization, searchandrescuefm))
s.add(Implies(chatprotocol, searchandrescuefm))
s.add(Implies(mapaccess, searchandrescuefm))
s.add(Implies(connectivity, searchandrescuefm))
s.add(Implies(database, searchandrescuefm))
s.add(Implies(architecturalstyle, searchandrescuefm))
s.add(Implies(dataexchangeformat, searchandrescuefm))
s.add(Implies(gps, locationfinding))
s.add(Implies(radiotriangulation, locationfinding))
s.add(Implies(nexusonehtc, hardwareplatform))
s.add(Implies(droidmotoroal, hardwareplatform))
s.add(Implies(filemanageropentintents, filesharing))
s.add(Implies(inhousefilemanager, filesharing))
s.add(Implies(explicitreportssync, reportsynchronization))
s.add(Implies(implicitreportssync, reportsynchronization))
s.add(Implies(openfire, chatprotocol))
s.add(Implies(inhousechatprotocol, chatprotocol))
s.add(Implies(ondemandgooglesite, mapaccess))
s.add(Implies(cachedgoogleserver, mapaccess))
s.add(Implies(preloadedesri, mapaccess))
s.add(Implies(wifi, connectivity))
s.add(Implies(threegnexusone, connectivity))
s.add(Implies(threedroid, connectivity))
s.add(Implies(bluetooth, connectivity))
s.add(Implies(mysql, database))
s.add(Implies(sqlite, database))
s.add(Implies(peertopeer, architecturalstyle))
s.add(Implies(clientserver, architecturalstyle))
s.add(Implies(pushbased, architecturalstyle))
s.add(Implies(xml, dataexchangeformat))
s.add(Implies(compressedxml, dataexchangeformat))
s.add(Implies(unformatteddata, dataexchangeformat))


#Mandatory-Children
s.add(locationfinding == searchandrescuefm)
s.add(hardwareplatform == searchandrescuefm)
s.add(filesharing == searchandrescuefm)
s.add(reportsynchronization == searchandrescuefm)
s.add(chatprotocol == searchandrescuefm)
s.add(mapaccess == searchandrescuefm)
s.add(connectivity == searchandrescuefm)
s.add(database == searchandrescuefm)
s.add(architecturalstyle == searchandrescuefm)
s.add(dataexchangeformat == searchandrescuefm)


#Exclusive-Or Constraints
s.add(gps==And(Not(radiotriangulation),locationfinding))
s.add(radiotriangulation==And(Not(gps),locationfinding))
s.add(nexusonehtc==And(Not(droidmotoroal),hardwareplatform))
s.add(droidmotoroal==And(Not(nexusonehtc),hardwareplatform))
s.add(filemanageropentintents==And(Not(inhousefilemanager),filesharing))
s.add(inhousefilemanager==And(Not(filemanageropentintents),filesharing))
s.add(explicitreportssync==And(Not(implicitreportssync),reportsynchronization))
s.add(implicitreportssync==And(Not(explicitreportssync),reportsynchronization))
s.add(openfire==And(Not(inhousechatprotocol),chatprotocol))
s.add(inhousechatprotocol==And(Not(openfire),chatprotocol))
s.add(ondemandgooglesite==And(Not(cachedgoogleserver),Not(preloadedesri),mapaccess))
s.add(cachedgoogleserver==And(Not(ondemandgooglesite),Not(preloadedesri),mapaccess))
s.add(preloadedesri==And(Not(ondemandgooglesite),Not(cachedgoogleserver),mapaccess))
s.add(wifi==And(Not(threegnexusone),Not(threedroid),Not(bluetooth),connectivity))
s.add(threegnexusone==And(Not(wifi),Not(threedroid),Not(bluetooth),connectivity))
s.add(threedroid==And(Not(wifi),Not(threegnexusone),Not(bluetooth),connectivity))
s.add(bluetooth==And(Not(wifi),Not(threegnexusone),Not(threedroid),connectivity))
s.add(mysql==And(Not(sqlite),database))
s.add(sqlite==And(Not(mysql),database))
s.add(peertopeer==And(Not(clientserver),Not(pushbased),architecturalstyle))
s.add(clientserver==And(Not(peertopeer),Not(pushbased),architecturalstyle))
s.add(pushbased==And(Not(peertopeer),Not(clientserver),architecturalstyle))
s.add(xml==And(Not(compressedxml),Not(unformatteddata),dataexchangeformat))
s.add(compressedxml==And(Not(xml),Not(unformatteddata),dataexchangeformat))
s.add(unformatteddata==And(Not(xml),Not(compressedxml),dataexchangeformat))


#Or Constraints


#Requires Constraints
s.add(Implies(threegnexusone, nexusonehtc))
s.add(Implies(threedroid, droidmotoroal))   

#Excludes Constraints


#Attributes
total_rampuptime = Int('total_rampuptime')
total_responsetime = Int('total_responsetime')
total_developmenttime = Int('total_developmenttime')
total_deploymenttime = Int('total_deploymenttime')
total_reliability = Real('total_reliability')
total_cost = Int('total_cost')
total_batteryusage = Int('total_batteryusage')


#Sums for Attributes
s.add(total_rampuptime== 6*If(gps, 1, 0 ) \
+ 8*If(radiotriangulation, 1, 0 ) \
+ 0*If(hardwareplatform, 1, 0 ) \
+ 0*If(nexusonehtc, 1, 0 ) \
+ 0*If(droidmotoroal, 1, 0 ) \
+ 0*If(filesharing, 1, 0 ) \
+ 9*If(filemanageropentintents, 1, 0 ) \
+ 8*If(inhousefilemanager, 1, 0 ) \
+ 0*If(reportsynchronization, 1, 0 ) \
+ 2*If(explicitreportssync, 1, 0 ) \
+ 2*If(implicitreportssync, 1, 0 ) \
+ 0*If(chatprotocol, 1, 0 ) \
+ 6*If(openfire, 1, 0 ) \
+ 4*If(inhousechatprotocol, 1, 0 ) \
+ 0*If(mapaccess, 1, 0 ) \
+ 9*If(ondemandgooglesite, 1, 0 ) \
+ 9*If(cachedgoogleserver, 1, 0 ) \
+ 13*If(preloadedesri, 1, 0 ) \
+ 0*If(connectivity, 1, 0 ) \
+ 3*If(wifi, 1, 0 ) \
+ 2*If(threegnexusone, 1, 0 ) \
+ 2*If(threedroid, 1, 0 ) \
+ 2*If(bluetooth, 1, 0 ) \
+ 0*If(database, 1, 0 ) \
+ 2*If(mysql, 1, 0 ) \
+ 4*If(sqlite, 1, 0 ) \
+ 0*If(architecturalstyle, 1, 0 ) \
+ 11*If(peertopeer, 1, 0 ) \
+ 8*If(clientserver, 1, 0 ) \
+ 10*If(pushbased, 1, 0 ) \
+ 0*If(dataexchangeformat, 1, 0 ) \
+ 3*If(xml, 1, 0 ) \
+ 5*If(compressedxml, 1, 0 ) \
+ 2*If(unformatteddata, 1, 0 ) \
)
s.add(total_responsetime== 0*If(locationfinding, 1, 0 ) \
+ 500*If(gps, 1, 0 ) \
+ 100*If(radiotriangulation, 1, 0 ) \
+ 0*If(hardwareplatform, 1, 0 ) \
+ 60*If(nexusonehtc, 1, 0 ) \
+ 55*If(droidmotoroal, 1, 0 ) \
+ 0*If(filesharing, 1, 0 ) \
+ 65*If(filemanageropentintents, 1, 0 ) \
+ 60*If(inhousefilemanager, 1, 0 ) \
+ 0*If(reportsynchronization, 1, 0 ) \
+ 30*If(explicitreportssync, 1, 0 ) \
+ 4*If(implicitreportssync, 1, 0 ) \
+ 0*If(chatprotocol, 1, 0 ) \
+ 60*If(openfire, 1, 0 ) \
+ 40*If(inhousechatprotocol, 1, 0 ) \
+ 0*If(mapaccess, 1, 0 ) \
+ 800*If(ondemandgooglesite, 1, 0 ) \
+ 4*If(cachedgoogleserver, 1, 0 ) \
+ 2*If(preloadedesri, 1, 0 ) \
+ 0*If(connectivity, 1, 0 ) \
+ 35*If(wifi, 1, 0 ) \
+ 25*If(threegnexusone, 1, 0 ) \
+ 25*If(threedroid, 1, 0 ) \
+ 30*If(bluetooth, 1, 0 ) \
+ 0*If(database, 1, 0 ) \
+ 25*If(mysql, 1, 0 ) \
+ 10*If(sqlite, 1, 0 ) \
+ 0*If(architecturalstyle, 1, 0 ) \
+ 20*If(peertopeer, 1, 0 ) \
+ 30*If(clientserver, 1, 0 ) \
+ 25*If(pushbased, 1, 0 ) \
+ 0*If(dataexchangeformat, 1, 0 ) \
+ 35*If(xml, 1, 0 ) \
+ 20*If(compressedxml, 1, 0 ) \
+ 10*If(unformatteddata, 1, 0 ) \
)
s.add(total_developmenttime== 0*If(locationfinding, 1, 0 ) \
+ 4*If(gps, 1, 0 ) \
+ 14*If(radiotriangulation, 1, 0 ) \
+ 0*If(hardwareplatform, 1, 0 ) \
+ 0*If(nexusonehtc, 1, 0 ) \
+ 0*If(droidmotoroal, 1, 0 ) \
+ 0*If(filesharing, 1, 0 ) \
+ 4*If(filemanageropentintents, 1, 0 ) \
+ 6*If(inhousefilemanager, 1, 0 ) \
+ 0*If(reportsynchronization, 1, 0 ) \
+ 6*If(explicitreportssync, 1, 0 ) \
+ 4*If(implicitreportssync, 1, 0 ) \
+ 0*If(chatprotocol, 1, 0 ) \
+ 6*If(openfire, 1, 0 ) \
+ 8*If(inhousechatprotocol, 1, 0 ) \
+ 0*If(mapaccess, 1, 0 ) \
+ 18*If(ondemandgooglesite, 1, 0 ) \
+ 18*If(cachedgoogleserver, 1, 0 ) \
+ 27*If(preloadedesri, 1, 0 ) \
+ 0*If(connectivity, 1, 0 ) \
+ 0*If(wifi, 1, 0 ) \
+ 0*If(threegnexusone, 1, 0 ) \
+ 0*If(threedroid, 1, 0 ) \
+ 0*If(bluetooth, 1, 0 ) \
+ 0*If(database, 1, 0 ) \
+ 17*If(mysql, 1, 0 ) \
+ 16*If(sqlite, 1, 0 ) \
+ 0*If(architecturalstyle, 1, 0 ) \
+ 26*If(peertopeer, 1, 0 ) \
+ 16*If(clientserver, 1, 0 ) \
+ 24*If(pushbased, 1, 0 ) \
+ 0*If(dataexchangeformat, 1, 0 ) \
+ 7*If(xml, 1, 0 ) \
+ 9*If(compressedxml, 1, 0 ) \
+ 4*If(unformatteddata, 1, 0 ) \
)
s.add(total_deploymenttime== 0*If(locationfinding, 1, 0 ) \
+ 3*If(gps, 1, 0 ) \
+ 1*If(radiotriangulation, 1, 0 ) \
+ 0*If(hardwareplatform, 1, 0 ) \
+ 0*If(nexusonehtc, 1, 0 ) \
+ 0*If(droidmotoroal, 1, 0 ) \
+ 0*If(filesharing, 1, 0 ) \
+ 1*If(filemanageropentintents, 1, 0 ) \
+ 0*If(inhousefilemanager, 1, 0 ) \
+ 0*If(reportsynchronization, 1, 0 ) \
+ 2*If(explicitreportssync, 1, 0 ) \
+ 1*If(implicitreportssync, 1, 0 ) \
+ 0*If(chatprotocol, 1, 0 ) \
+ 1*If(openfire, 1, 0 ) \
+ 0*If(inhousechatprotocol, 1, 0 ) \
+ 0*If(mapaccess, 1, 0 ) \
+ 0*If(ondemandgooglesite, 1, 0 ) \
+ 4*If(cachedgoogleserver, 1, 0 ) \
+ 4*If(preloadedesri, 1, 0 ) \
+ 0*If(connectivity, 1, 0 ) \
+ 6*If(wifi, 1, 0 ) \
+ 3*If(threegnexusone, 1, 0 ) \
+ 3*If(threedroid, 1, 0 ) \
+ 5*If(bluetooth, 1, 0 ) \
+ 0*If(database, 1, 0 ) \
+ 15*If(mysql, 1, 0 ) \
+ 14*If(sqlite, 1, 0 ) \
+ 0*If(architecturalstyle, 1, 0 ) \
+ 18*If(peertopeer, 1, 0 ) \
+ 9*If(clientserver, 1, 0 ) \
+ 9*If(pushbased, 1, 0 ) \
+ 0*If(dataexchangeformat, 1, 0 ) \
+ 0*If(xml, 1, 0 ) \
+ 0*If(compressedxml, 1, 0 ) \
+ 0*If(unformatteddata, 1, 0 ) \
)
s.add(total_reliability== If(gps, 0.75, 1.0 ) \
* If(radiotriangulation, 0.92, 1.0) \
* If(filemanageropentintents, 0.95, 1.0) \
* If(inhousefilemanager, 0.92 , 1.0) \
* If(explicitreportssync, 0.88 , 1.0) \
* If(implicitreportssync,0.97 , 1.0) \
* If(openfire, 0.95 , 1.0) \
* If(inhousechatprotocol, 0.96 , 1.0) \
* If(ondemandgooglesite, 0.91 , 1.0) \
* If(cachedgoogleserver, 0.97 , 1.0) \
* If(preloadedesri, 0.90 , 1.0) \
* If(wifi, 0.85 , 1.0) \
* If(threegnexusone, 0.88 , 1.0) \
* If(threedroid, 0.88 , 1.0) \
* If(bluetooth, 0.85 , 1.0) \
* If(mysql, 0.90 , 1.0) \
* If(sqlite, 0.90 , 1.0) \
* If(peertopeer, 0.66 , 1.0) \
* If(clientserver, 0.95 , 1.0) \
* If(pushbased, 0.94 , 1.0) 
)
s.add(total_cost== 0*If(locationfinding, 1, 0 ) \
+ 80*If(gps, 1, 0 ) \
+ 0*If(radiotriangulation, 1, 0 ) \
+ 0*If(hardwareplatform, 1, 0 ) \
+ 525*If(nexusonehtc, 1, 0 ) \
+ 520*If(droidmotoroal, 1, 0 ) \
+ 0*If(filesharing, 1, 0 ) \
+ 0*If(filemanageropentintents, 1, 0 ) \
+ 0*If(inhousefilemanager, 1, 0 ) \
+ 0*If(reportsynchronization, 1, 0 ) \
+ 0*If(explicitreportssync, 1, 0 ) \
+ 0*If(implicitreportssync, 1, 0 ) \
+ 0*If(chatprotocol, 1, 0 ) \
+ 0*If(openfire, 1, 0 ) \
+ 0*If(inhousechatprotocol, 1, 0 ) \
+ 0*If(mapaccess, 1, 0 ) \
+ 0*If(ondemandgooglesite, 1, 0 ) \
+ 900*If(cachedgoogleserver, 1, 0 ) \
+ 170*If(preloadedesri, 1, 0 ) \
+ 0*If(connectivity, 1, 0 ) \
+ 80*If(wifi, 1, 0 ) \
+ 400*If(threegnexusone, 1, 0 ) \
+ 400*If(threedroid, 1, 0 ) \
+ 70*If(bluetooth, 1, 0 ) \
+ 0*If(database, 1, 0 ) \
+ 0*If(mysql, 1, 0 ) \
+ 0*If(sqlite, 1, 0 ) \
+ 0*If(architecturalstyle, 1, 0 ) \
+ 0*If(peertopeer, 1, 0 ) \
+ 0*If(clientserver, 1, 0 ) \
+ 0*If(pushbased, 1, 0 ) \
+ 0*If(dataexchangeformat, 1, 0 ) \
+ 0*If(xml, 1, 0 ) \
+ 0*If(compressedxml, 1, 0 ) \
+ 0*If(unformatteddata, 1, 0 ) \
)
s.add(total_batteryusage== 0*If(locationfinding, 1, 0 ) \
+ 10*If(gps, 1, 0 ) \
+ 5*If(radiotriangulation, 1, 0 ) \
+ 0*If(hardwareplatform, 1, 0 ) \
+ 5*If(nexusonehtc, 1, 0 ) \
+ 5*If(droidmotoroal, 1, 0 ) \
+ 0*If(filesharing, 1, 0 ) \
+ 5*If(filemanageropentintents, 1, 0 ) \
+ 4*If(inhousefilemanager, 1, 0 ) \
+ 0*If(reportsynchronization, 1, 0 ) \
+ 3*If(explicitreportssync, 1, 0 ) \
+ 8*If(implicitreportssync, 1, 0 ) \
+ 0*If(chatprotocol, 1, 0 ) \
+ 5*If(openfire, 1, 0 ) \
+ 3*If(inhousechatprotocol, 1, 0 ) \
+ 0*If(mapaccess, 1, 0 ) \
+ 4*If(ondemandgooglesite, 1, 0 ) \
+ 5*If(cachedgoogleserver, 1, 0 ) \
+ 7*If(preloadedesri, 1, 0 ) \
+ 0*If(connectivity, 1, 0 ) \
+ 4*If(wifi, 1, 0 ) \
+ 2*If(threegnexusone, 1, 0 ) \
+ 4*If(threedroid, 1, 0 ) \
+ 3*If(bluetooth, 1, 0 ) \
+ 0*If(database, 1, 0 ) \
+ 6*If(mysql, 1, 0 ) \
+ 5*If(sqlite, 1, 0 ) \
+ 0*If(architecturalstyle, 1, 0 ) \
+ 8*If(peertopeer, 1, 0 ) \
+ 6*If(clientserver, 1, 0 ) \
+ 4*If(pushbased, 1, 0 ) \
+ 0*If(dataexchangeformat, 1, 0 ) \
+ 4*If(xml, 1, 0 ) \
+ 5*If(compressedxml, 1, 0 ) \
+ 1*If(unformatteddata, 1, 0 ) \
)

s.add(searchandrescuefm==True)

# s.add(1000 * total_responsetime < 1000 * total_cost)
# s.add(1000 * total_responsetime >= 1000 * total_cost)
    
metrics_variables = [total_batteryusage, total_cost, total_deploymenttime, \
                     total_developmenttime, total_rampuptime, \
                     total_reliability,
                     total_responsetime]
metrics_objective_direction = [METRICS_MINIMIZE, METRICS_MINIMIZE, \
    METRICS_MINIMIZE, METRICS_MINIMIZE, METRICS_MINIMIZE, \
    METRICS_MAXIMIZE, METRICS_MINIMIZE, ]

