import mysql.connector

#datetime.datetime.now()

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
cursor = cnx.cursor()

#sql =  ("SELECT * FROM Usuarios")


cursor.execute("UPDATE Country SET name='United Republic of Tanzania' WHERE name='\"United Republic of Tanzania\"'")

#userList = cursor.fetchall()

cnx.commit()

cursor.execute("SELECT * FROM Country WHERE name='United Republic of Tanzania'")

for user in cursor.fetchall():
    print(user)


cursor.close()
cnx.close()