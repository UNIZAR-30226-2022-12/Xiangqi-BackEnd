import mysql.connector

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()

#sql =  ("SELECT * FROM Usuarios")


cursor.execute("UPDATE Usuarios SET puntos=100 WHERE id = 11")

#userList = cursor.fetchall()

cnx.commit()


cursor.close()
cnx.close()