import mysql.connector

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()

#sql =  ("SELECT * FROM Usuarios")


cursor.execute("SELECT * FROM Usuarios")

userList = cursor.fetchall()
#for x in cursor.fetchall():
print(userList)

cnx.commit()

cursor.close()
cnx.close()