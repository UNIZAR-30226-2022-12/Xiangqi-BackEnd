import mysql.connector

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

cursor = cnx.cursor()

cursor.execute("SHOW TABLES")

print("")
print("DATABASE TABLES:")
print(cursor.fetchall())

cursor.close()
cnx.close()