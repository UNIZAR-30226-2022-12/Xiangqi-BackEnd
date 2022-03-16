#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
import mysql.connector

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

getUserQuery = "SELECT * FROM Usuarios WHERE correo = %s"

def getUserList():              
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM Usuarios")

    userList = cursor.fetchall()
    
    cursor.close()

    return userList

def loginUser(correo, pwd):
    exist = False
    pwdOk = False

    cursor = cnx.cursor()

    cursor.execute(getUserQuery, (correo,))
    user = cursor.fetchone()

    if user != None :
        exist = True
        if pwd == user[1]:
            pwdOk = True

    cursor.close()

    return exist, pwdOk, user


#cnx.close()