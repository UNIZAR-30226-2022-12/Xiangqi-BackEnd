import mysql.connector
import datetime
import json
from pathlib import Path

#datetime.datetime.now()

skinList = {
    #Se añade la info acerca de las skins (formato por definir)
}

with open("skins.json", "w") as outfile:
    json.dump(skinList, outfile)