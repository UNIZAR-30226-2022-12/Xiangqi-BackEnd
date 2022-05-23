import mysql.connector
import datetime

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()


sql =  ("INSERT INTO Solicitudes (remitente, destinatario) "
        "VALUE (%s, %s);")
value = [
        (31, 11),
]
#sql =  ("SELECT * FROM Usuarios")


cursor.executemany(sql, value)
#print(value[0])
cnx.commit()

cursor.close()
cnx.close()