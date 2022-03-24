import mysql.connector
import datetime

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()


sql =  ("INSERT INTO Country (name, code, bandera) "
        "VALUE (%s, %s, %s);")
#sql =  ("SELECT * FROM Usuarios")
file = open('database/paises.txt', 'r')
file_content = file.read().splitlines()
file.close()

values = [tuple(line.split(';')) for line in file_content]

print("Inserting ... ")
cursor.executemany(sql, values)
print("ok")

cnx.commit()

cursor.close()
cnx.close()