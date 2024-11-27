import sqlite3
import json
import string
import marshmallow
from marshmallow import Schema, fields, post_load
import os.path
import sys


# by: Kellan Cook

# HOW TO USE ==========================
#   ensure you have all dependencies from the requirements.txt file
#   put the sqlite static data file in the same directory
#   click run
#


# schema for encoding
class eveSystemSchema(Schema):
    systemName = fields.Str()
    region = fields.Str()
    toSystem = fields.List(fields.Str())


# object for each system
class eveSystems:
    def __init__(self, systemName, region, toSystem):
        self.systemName = systemName
        self.region = region
        self.toSystem = toSystem


i = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sqlite-latest.sqlite")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("SELECT solarSystemName, solarSystemID FROM mapSolarSystems")
systemNameList = cursor.fetchall()
systemCount = len(systemNameList)
print("number of systems found: " + str(systemCount))
print("")
s1 = []
while i < systemCount - 1:

    cursor.execute(
        "SELECT toSolarSystemID FROM mapSolarSystemJumps WHERE fromSolarSystemID = '"
        + str(systemNameList[i][1])
        + "'"
    )
    systemConnections = cursor.fetchall()
    cursor.execute(
        "SELECT regionName FROM mapregions WHERE regionid = (SELECT regionid FROM mapSolarSystems WHERE solarSystemID = "
        + str(systemNameList[i][1])
        + ")"
    )
    region = cursor.fetchone()
    region = region[0]

    # print(systemConnections)
    conections = []
    for system in systemConnections:
        if system != "":
            cursor.execute(
                "SELECT solarSystemName FROM mapSolarSystems WHERE solarSystemID == "
                + str(system[0])
                + ""
            )
            sysName = cursor.fetchone()
            conections.append(sysName[0])
            sys.stdout.write("\033[F")
            print(
                "---->"
                + sysName[0]
                + str(" " * int(15 - len(sysName[0])))
                + "  --  "
                + str(i)
                + "/"
                + str(systemCount)
            )

    system_data = eveSystems(str(systemNameList[i][0]), region, conections)

    s1.append(system_data)

    i = i + 1
print("building schema")
system_schema = eveSystemSchema(many=True)
systemJson = system_schema.dumps(s1, indent=4)
print("building json file")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "systemLinks.json")
f = open(json_path, "w+")
f.write(str(systemJson))
f.close()
print("done!")
