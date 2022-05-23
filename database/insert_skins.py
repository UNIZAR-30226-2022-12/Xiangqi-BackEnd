import codecs
import mysql.connector
import datetime

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft', charset="utf8")

cursor = cnx.cursor()

sql =  ("INSERT INTO Skins (skinId, tipo, name, description, category, precio) " 
        "VALUE (%s, %s, %s, %s, %s, %s);")
#sql =  ("SELECT * FROM Usuarios")
file = codecs.open('database/skins.txt', 'r', "utf-8")
file_content = file.read().splitlines()
file.close()

values = [tuple(line.split(';')) for line in file_content]

cursor.execute("set names utf8;")
print("Inserting ... ")
cursor.executemany(sql, values)
print("ok")

cnx.commit()

cursor.close()
cnx.close()