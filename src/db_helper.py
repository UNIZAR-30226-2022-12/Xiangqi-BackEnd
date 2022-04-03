#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
from curses.ascii import US
import mysql.connector
from mysql.connector import RefreshOption

from clases import User, Usuarios

#cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
#                             host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
#                             database='BDpsoft')

getUserQuery = "SELECT * FROM Usuarios WHERE id = %s"
getUserEmailQuery = "SELECT * FROM Usuarios WHERE correo = %s"
getUserFriendsQuery = "SELECT * FROM Amigos WHERE usuario1 = %s OR usuario2 = %s"
getAllUserQuery = "SELECT * FROM Usuarios"
getAllCountryQuery = "SELECT name, code FROM Country"
getCountryQuery = "SELECT * FROM Country WHERE name = %s"
getUserGameQuery = "SELECT * FROM Partidas WHERE roja = %s OR negra = %s"
insertUserQuery =  ("INSERT INTO Usuarios (correo, pwd, salt, validacion, nick, name, birthDate, pais, fichaSkin, tableroSkin, rango, puntos, fechaRegistro) "
        "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
validateUserQuery = "UPDATE Usuarios SET validacion = True WHERE correo = %s"
changePwdQuery = "UPDATE Usuarios SET pwd = %s, salt = %s WHERE correo = %s"
editUserQuery = "UPDATE Usuarios SET pwd = %s, salt = %s, nick = %s, name = %s, birthDate = %s, pais = %s WHERE id = %s"
deleteUserQuery = "DELETE FROM Usuarios WHERE id = %s"



def getAllUser(): 
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)             
    cursor = cnx.cursor()
    cursor.execute(getAllUserQuery)

    userList = cursor.fetchall()
    
    cursor.close()
    cnx.close()

    return userList

def getUserEmail(correo):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    exist = False

    cursor = cnx.cursor()

    cursor.execute(getUserEmailQuery, (correo,))
    user = cursor.fetchone()

    if user != None :
        exist = True
        if user[Usuarios.pais] != None:
            cursor.execute(getCountryQuery, (user[Usuarios.pais],))
            pais = cursor.fetchone()
            user = list(user)
            user[Usuarios.pais] = pais
        
    cursor.close()
    cnx.close()

    return exist, user

def getUser(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    exist = False

    cursor = cnx.cursor()

    cursor.execute(getUserQuery, (id,))
    user = cursor.fetchone()

    if user != None :
        exist = True
        if user[Usuarios.pais] != None:
            cursor.execute(getCountryQuery, (user[Usuarios.pais],))
            pais = cursor.fetchone()
            user = list(user)
            user[Usuarios.pais] = pais
        
    cursor.close()
    cnx.close()

    return exist, user

def getUserGame(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)

    cursor = cnx.cursor()

    cursor.execute(getUserGameQuery, (id, id))
    game = cursor.fetchall()

    cursor.close()
    cnx.close()

    return game

def getUserFriends(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)

    cursor = cnx.cursor()

    cursor.execute(getUserFriendsQuery, (id, id))
    friends = cursor.fetchall()

    cursor.close()
    cnx.close()

    return friends

def insertUser(user):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
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
        cnx.close()
        print("MySQL connection is closed")
        return exito

def editUser(id, data):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    try:
        cursor = cnx.cursor()
        exito = True
        print(id)
        cursor.execute(editUserQuery, data+[id])
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to edit record into Laptop table {}".format(error))
    finally:
        cursor.close()
        cnx.close()
        print("MySQL connection is closed")
        return exito
        
def deleteUser(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    try:
        cursor = cnx.cursor()
        exito = True

        cursor.execute(deleteUserQuery, (id, ))
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to edit record into Laptop table {}".format(error))
    finally:
        cursor.close()
        cnx.close()
        print("MySQL connection is closed")
        return exito

def validateUser(correo):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
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
        cnx.close()
        return exito

def chageUserPwd(correo, pwd, salt):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    try:
        cursor = cnx.cursor()
        cursor.execute(changePwdQuery, (pwd, salt, correo))
        exito = True

        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to change user password into Laptop table {}".format(error))
    finally:
        cursor.close()
        cnx.close()
        return exito

def getCountry(name): 
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)             
    cursor = cnx.cursor()

    print(name)
    cursor.execute(getCountryQuery, (name,))

    country = cursor.fetchone()
    
    cursor.close()
    cnx.close()

    return country

def allCountries(): 
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)             
    cursor = cnx.cursor()
    cursor.execute(getAllCountryQuery)

    countryList = cursor.fetchall()
    res = list()
    for country in countryList:
        res.append({'name': country[0], 'code': country[1]})
    cursor.close()
    cnx.close()

    return res

#cnx.close()