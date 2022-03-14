import mysql.connector

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()


sql =  ("INSERT INTO Usuarios (nick, nombre, correo) "
        "VALUE (Hanser, Alex, alex@gmail.com);")
sql =  ("SELECT * FROM Usuarios")


cursor.execute(sql)

cnx.commit()

cursor.close()
cnx.close()