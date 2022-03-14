import sys
import mysql.connector

if len(sys.argv) < 2:
    print("invoca con drop_table.py table1 table2 .. tableN")
else:
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cursor = cnx.cursor()
    for i in range(1,len(sys.argv)): 
        print("DROP TABLE \'" + sys.argv[i] + "\'... ")
        sql = "DROP TABLE IF EXISTS " + sys.argv[i]
        cursor.execute(sql)  

    cursor.execute("SHOW TABLES")
    print("")
    print("DATABASE TABLES:")   
    print(cursor.fetchall())
    print("")
    cursor.close()
    cnx.close()