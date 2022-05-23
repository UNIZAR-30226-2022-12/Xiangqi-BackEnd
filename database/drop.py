import sys
import mysql.connector


cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                        host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                        database='BDpsoft')
cursor = cnx.cursor()
sql = "SET FOREIGN_KEY_CHECKS = 0"
cursor.execute(sql)
sql = "DROP TABLE IF EXISTS Tiene"
cursor.execute(sql)  
sql = "SET FOREIGN_KEY_CHECKS = 1"
cursor.execute(sql)
cursor.execute("SHOW TABLES")
print("")
print("DATABASE TABLES:")   
print(cursor.fetchall())
print("")
cursor.close()
cnx.commit()
cnx.close()