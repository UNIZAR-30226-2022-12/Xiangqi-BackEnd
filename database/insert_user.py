import mysql.connector
import datetime

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()


sql =  ("INSERT INTO Usuarios (correo, pwd, nick, name, birthDate, foto, pais, fichaSkin, tableroSkin, rango, puntos, fechaRegistro) "
        "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
value = [
        ("1@gmail", "1", "a1", "alex1", '2022-01-15', "./", "CHN", None, None, 1, 10, '2021-03-15'),
        ("2@gmail", "12", "a2", "alex2", '2022-02-15', "./", "CHN", None, None, 2, 20, '2022-03-15'),
        ("3@gmail", "123", "a3", "alex3", '2022-03-15', "./", "CHN", None, None, 3, 30, '2023-03-15')
]
#sql =  ("SELECT * FROM Usuarios")


cursor.executemany(sql, value)

cnx.commit()

cursor.close()
cnx.close()