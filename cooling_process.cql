 // delete previous?
MATCH (n) DETACH DELETE n


CREATE (e1:Event {type:'start', name:'cooling error'})
CREATE (e2:Event {type:'start', name:'SI_compressor_error'})
CREATE (e3:Event {type:'start', name:'SI_missing_cooling_fluid'})
CREATE (e4:Event {type:'start', name:'SI_e-valve_defect'})
CREATE (e5:Event {type:'start', name:'SI_def_heat_defect'})
CREATE (e6:Event {type:'start', name:'SI_vaporizer_defect'})
CREATE (e7:Event {type:'catching', name:'see sensor pattern'})

CREATE (e8:Event {type:'end', name:'end_1'})
CREATE (e9:Event {type:'end', name:'error'})
CREATE (e10:Event {type:'end', name:'success'})



CREATE (g1:Gate {type:'xor'})
CREATE (g2:Gate {type:'xor'})
CREATE (g3:Gate {type:'xor'})
CREATE (g4:Gate {type:'xor'})
CREATE (g5:Gate {type:'xor'})
CREATE (g6:Gate {type:'xor'})

// if process with and comment, else uncomment
//CREATE (g7:Gate {type:'and'})
//CREATE (g8:Gate {type:'and'})


CREATE (a1:Activity {name:'check compressor', sensors:'temperature (18,25); gyroscope', progress:'0.125'})
CREATE (a2:Activity {name:'check cooling fluid', sensors:'temperature (12,20)', progress:'0.125'})
CREATE (a3:Activity {name:'refill cooling fluid', sensors:'', progress:'0.66'})
CREATE (a4:Activity {name:'open vaporizer', sensors:'', progress:'0.25'})
CREATE (a5:Activity {name:'inform customer', sensors:'', progress:'1.0'})
CREATE (a6:Activity {name:'read out sensor data', sensors:'barometer (40,60)', progress:'0.375'})
CREATE (a7:Activity {name:'close vaporizer', sensors:'', progress:'0.80'})
CREATE (a8:Activity {name:'test system function', sensors:'temperature (18,25); gyroscope; barometer (35,60); ambient_light', progress:'1.0'})
CREATE (a9:Activity {name:'analyse sensor data', sensors:'temperature (18,20); gyroscope; barometer; ambient_light', progress:'0.50'})
CREATE (a10:Activity {name:'repair e-valve', sensors:'gyroscope', progress:'0.625'})
CREATE (a11:Activity {name:'repair defrost heater', sensors:'temperature (29,43)', progress:'0.625'})
CREATE (a12:Activity {name:'repair vaporizer', sensors:'barometer', progress:'0.625'})

// Relationships

//if process with AND comment, else uncomment
//CREATE (e1)-[:SEQ]->(g7)
//CREATE (g7)-[:SEQ]->(a1)
//CREATE (g7)-[:SEQ]->(a2)
//CREATE (a1)-[:SEQ]->(g8)
//CREATE (a2)-[:SEQ]->(g8)
//CREATE (g8)-[:SEQ]->(g1)

// if process with and uncomment, else comment
CREATE (e1)-[:SEQ]->(a1)
CREATE (a1)-[:SEQ]->(a2)
CREATE (a2)-[:SEQ]->(g1)


CREATE (e2)-[:SEQ]->(a1)
CREATE (e3)-[:SEQ]->(a2)
CREATE (g1)-[:SEQ]->(g3)
CREATE (g1)-[:SEQ]->(a4)
CREATE (g3)-[:SEQ]->(a3)
CREATE (g3)-[:SEQ]->(a5)
CREATE (a3)-[:SEQ]->(a5)
CREATE (a5)-[:SEQ]->(e8)
CREATE (a4)-[:SEQ]->(a6)
CREATE (a6)-[:SEQ]->(e7)

CREATE (e7)-[:SEQ]->(g2)
CREATE (g2)-[:SEQ]->(a7)
CREATE (g2)-[:SEQ]->(a9)
CREATE (a7)-[:SEQ]->(a8)
CREATE (a8)-[:SEQ]->(g6)
CREATE (g6)-[:SEQ]->(e9)
CREATE (g6)-[:SEQ]->(e10)
CREATE (a9)-[:SEQ]->(g4)
CREATE (g4)-[:SEQ]->(a10)
CREATE (g4)-[:SEQ]->(a11)
CREATE (g4)-[:SEQ]->(a12)
CREATE (a10)-[:SEQ]->(g5)
CREATE (a11)-[:SEQ]->(g5)
CREATE (a12)-[:SEQ]->(g5)
CREATE (g5)-[:SEQ]->(a6)
CREATE (e4)-[:SEQ]->(a10)
CREATE (e5)-[:SEQ]->(a11)
CREATE (e6)-[:SEQ]->(a12)

// example commands
//CREATE (a:Activity {name:'check', sensors:'sensor'})
//CREATE (e:Event {type:'start', name:''})
//CREATE (g:Gate {type:'xor'})
