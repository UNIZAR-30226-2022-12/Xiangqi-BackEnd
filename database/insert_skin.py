import mysql.connector
import datetime
import imageio as iio
from pathlib import Path

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()

#sql = ("INSERT INTO Tiene (skinId, usuario) " 
#       "VALUE (%s, %s);")
sql = ("INSERT INTO Skins (skinId, tipo, precio)"
       "VALUE (%s, %s, %s);")

skins = list()
for file in Path("./images/themes/boards").iterdir():
    if not file.is_file():
        continue

    skins.append(iio.imread(file))

for file in Path("./images/themes/pieces").iterdir():
    if not file.is_file():
        continue

    skins.append(iio.imread(file))

cursor.executemany(sql, skins)

cnx.commit()

cursor.close()
cnx.close()