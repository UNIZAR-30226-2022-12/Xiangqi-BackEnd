import mysql.connector
import datetime

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()


sql =  ("INSERT INTO Usuarios (correo, pwd, salt, validacion, nick, name, birthDate, pais, fichaSkin, tableroSkin, rango, puntos, fechaRegistro) "
        "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
value = [
        #("1@gmail", "1", "", True, "a1", "alex1", '2022-01-15', "Andorra", None, None, 1, 10, '2021-03-15'),
        #("2@gmail", "12", "", True, "a2", "alex2", '2022-02-15', "Andorra", None, None, 2, 20, '2022-03-15'),
        #("3@gmail", "123", "", False, "a3", "alex3", '2022-03-15', "Andorra", None, None, 3, 30, '2023-03-15'),
        #("2@gmail", "1234", "", True, "r1", "rubius3", '2022-04-25', "Andorra", None, None, 4, 4000, '2022-04-25'),
        #("666@gmal", "hell", "", True, "satan", "Lucifer", '1999-12-31', "Andorra", None, None, 5, 6666666, '2022-04-25')
        ("grefgIsAMotherfucker@gmail", "1234567890", "", True, "---", "XokasTheBest", '1900-01-01', "Andorra", None, None, 5, 9999999, '2022-04-25')
]
#sql =  ("SELECT * FROM Usuarios")


cursor.executemany(sql, value)
#print(value[0])
cnx.commit()

cursor.close()
cnx.close()