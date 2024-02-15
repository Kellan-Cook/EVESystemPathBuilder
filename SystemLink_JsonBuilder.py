import sqlite3
import json
import string
import marshmallow
from marshmallow import Schema, fields, post_load


#by: Gnomagin
#HOW TO USE ==========================
#   ensure you have all dependencies from the requirements.txt file
#   put the sqlite static data file in the same directory
#   click run
#

#schema for encoding
class eveSystemSchema(Schema):
    systemName = fields.Str()
    toSystem = fields.List(fields.Str())

#object for each system
class eveSystems:
    def __init__(self, systemName, toSystem):
        self.systemName = systemName
        self.toSystem = toSystem


i = 0
connection = sqlite3.connect('sqlite-latest.sqlite')
cursor = connection.cursor()
cursor.execute("SELECT solarSystemName, solarSystemID FROM mapSolarSystems")
systemNameList = cursor.fetchall()
systemCount = len(systemNameList)
print ("number of systems found: " + str(systemCount))
s1 = []
while(i < systemCount - 1):

    print(systemNameList[i][0])

    cursor.execute("SELECT toSolarSystemID FROM mapSolarSystemJumps WHERE fromSolarSystemID = '"+ str(systemNameList[i][1]) + "'")
    systemConnections = cursor.fetchall() 

    

    
    #print(systemConnections)
    conections = []
    for system in systemConnections:
        if(system != ""):
            cursor.execute("SELECT solarSystemName FROM mapSolarSystems WHERE solarSystemID == " + str(system[0]) + "")
            sysName = cursor.fetchone()
            conections.append(sysName[0])
            
            print("---->" + sysName[0])


    system_data = eveSystems(str(systemNameList[i][0]), conections)
    
    s1.append(system_data)

    i = i + 1
system_schema = eveSystemSchema(many=True)
systemJson = system_schema.dumps(s1, indent=4)
print(systemJson)

f = open("systemLinks.json", "w+")
f.write(str(systemJson))
f.close()