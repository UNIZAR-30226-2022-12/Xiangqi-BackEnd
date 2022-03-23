#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
import mysql.connector
from mysql.connector import RefreshOption

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

getUserQuery = "SELECT * FROM Usuarios WHERE correo = %s"
getAllUserQuery = "SELECT * FROM Usuarios"
getUserGameQuery = "SELECT * FROM Partidas WHERE roja = %s OR negra = %s"
insertUserQuery =  ("INSERT INTO Usuarios (correo, pwd, salt, validacion, nick, name, birthDate, pais, fichaSkin, tableroSkin, rango, puntos, fechaRegistro) "
        "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
validateUserQuery = "UPDATE Usuarios SET validado = True WHERE correo = %s"

def getAllUser(): 
    cnx.cmd_refresh(RefreshOption.GRANT)             
    cursor = cnx.cursor()
    cursor.execute(getAllUserQuery)

    userList = cursor.fetchall()
    
    cursor.close()

    return userList

def getUser(correo):
    cnx.cmd_refresh(RefreshOption.GRANT)
    exist = False

    cursor = cnx.cursor()

    cursor.execute(getUserQuery, (correo,))
    user = cursor.fetchone()

    if user != None :
        exist = True

    cursor.close()

    return exist, user

def getUserGame(correo):
    cnx.cmd_refresh(RefreshOption.GRANT)

    cursor = cnx.cursor()

    cursor.execute(getUserGameQuery, (correo, correo))
    game = cursor.fetchall()

    cursor.close()

    return game

def insertUser(user):
    cnx.cmd_refresh(RefreshOption.GRANT)
    try:
        cursor = cnx.cursor()
        exito = True

        cursor.execute(insertUserQuery, user)
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to insert record into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito
        
def validateUser(correo):
    cnx.cmd_refresh(RefreshOption.GRANT)
    try:
        cursor = cnx.cursor()
        cursor.execute(validateUserQuery, (correo,))
        exito = True

        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to validate user into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito

#cnx.close()