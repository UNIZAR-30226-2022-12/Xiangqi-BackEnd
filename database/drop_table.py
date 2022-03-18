import sys
import mysql.connector


cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                        host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                        database='BDpsoft')
cursor = cnx.cursor()
sql = "SET FOREIGN_KEY_CHECKS = 0"
cursor.execute(sql)
if len(sys.argv) == 1:
    table = ["Usuarios", "Skins", "Tiene", "Amigos", "Partidas", "Solicitudes"]
    for i in table:
        print("DROP TABLE \'" + i + "\'... ")
        sql = "DROP TABLE IF EXISTS " + i
        cursor.execute(sql) 
else:
    for i in range(1,len(sys.argv)): 
        print("DROP TABLE \'" + sys.argv[i] + "\'... ")
        sql = "DROP TABLE IF EXISTS " + sys.argv[i]
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