import mysql.connector
import datetime

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()

sql =  ("INSERT INTO Tiene (skinId, tipo, usuario) "
        "VALUE (%s, %s, %s);")
value = [
        (1, 0, 11),
        (2, 0, 11),
        (1, 1, 11),
        (2, 1, 11)
        #("3", "4", 2, "1234", '2022-03-16', "2022-01-15"),
        #("4", "3", 1, "34215432", '2022-03-10', "2022-01-15"),
        #("4", "3", 1, "34215432", '2022-03-10', "2022-01-15")
]
#sql =  ("SELECT * FROM Usuarios")


cursor.executemany(sql, value)

id = cursor.lastrowid
print(id)

cnx.commit()

cursor.close()
cnx.close()