import mysql.connector
import datetime

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()


sql =  ("INSERT INTO Partidas (roja, negra, estado, movimientos, fechaInicio, lastMove) "
        "VALUE (%s, %s, %s, %s, %s, %s);")
value = [
        ("3", "4", 1, None, '2022-03-15', "2022-01-15"),
        ("3", "4", 2, "1234", '2022-03-16', "2022-01-15"),
        ("4", "3", 1, "34215432", '2022-03-10', "2022-01-15"),
        ("4", "3", 1, "34215432", '2022-03-10', "2022-01-15")
]
#sql =  ("SELECT * FROM Usuarios")


cursor.executemany(sql, value)

cnx.commit()

cursor.close()
cnx.close()