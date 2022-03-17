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
        ("1@gmail", "2@gmail", 0, None, '2022-01-15', "2022-01-15"),
        ("2@gmail", "3@gmail", 1, "1234", '2022-02-15', "2022-01-15"),
        ("3@gmail", "1@gmail", 3, "34215432", '2022-03-15', "2022-01-15")
]
#sql =  ("SELECT * FROM Usuarios")


cursor.executemany(sql, value)

cnx.commit()

cursor.close()
cnx.close()