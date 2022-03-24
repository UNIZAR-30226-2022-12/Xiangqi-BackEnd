#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
from curses.ascii import US
import mysql.connector
from mysql.connector import RefreshOption

from clases import User, Usuarios

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')

getUserQuery = "SELECT * FROM Usuarios WHERE correo = %s"
getAllUserQuery = "SELECT * FROM Usuarios"
getAllCountryQuery = "SELECT name, code FROM Country"
getCountryQuery = "SELECT * FROM Country WHERE name = %s"
getUserGameQuery = "SELECT * FROM Partidas WHERE roja = %s OR negra = %s"
insertUserQuery =  ("INSERT INTO Usuarios (correo, pwd, salt, validacion, nick, name, birthDate, pais, fichaSkin, tableroSkin, rango, puntos, fechaRegistro) "
        "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
validateUserQuery = "UPDATE Usuarios SET validacion = True WHERE correo = %s"

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
        if user[Usuarios.pais] != None:
            cursor.execute(getCountryQuery, (user[Usuarios.pais],))
            pais = cursor.fetchone()
            user = list(user)
            user[Usuarios.pais] = pais
        
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
        return exito

def getAllCountry(): 
    cnx.cmd_refresh(RefreshOption.GRANT)             
    cursor = cnx.cursor()
    cursor.execute(getAllCountryQuery)

    countryList = cursor.fetchall()
    
    cursor.close()

    return countryList

#cnx.close()