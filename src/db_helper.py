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

#---ranking query
userGamePlayed = "SELECT us.id, count(*) AS game FROM Usuarios us, Partidas p WHERE us.id = p.roja OR us.id = p.negra GROUP BY us.id"
userGameWon = "SELECT us.id, count(*) AS game FROM Usuarios us, Partidas p WHERE (us.id = p.roja AND p.estado = 1) OR (us.id = p.negra AND p.estado = 2) GROUP BY us.id"
userGameStat = "SELECT played.id, played.game AS pg, won.game AS wg FROM (" + userGamePlayed + ") played, (" + userGameWon + ") won WHERE played.id = won.id" 
rankingQuery = "SELECT us.id, us.nick, us.pais, c.code, c.bandera, us.rango, ug.pg, ug.wg FROM Usuarios us, Country c, (" + userGameStat + ") ug WHERE us.pais = c.name AND us.id = ug.id ORDER BY ug.wg DESC"




def getAllUser(cnx): 
    cursor = cnx.cursor()

    cursor.execute(getAllUserQuery)
    userList = cursor.fetchall() 

    cursor.close()
    return userList

def getUserEmail(correo, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserEmailQuery, (correo,))
    user = cursor.fetchone()

    exist = False
    if user != None :
        exist = True
        if user[Usuarios.pais] != None:
            cursor.execute(getCountryQuery, (user[Usuarios.pais],))
            pais = cursor.fetchone()
            user = list(user)
            user[Usuarios.pais] = pais
        
    cursor.close()
    return exist, user

def getUser(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserQuery, (id,))
    user = cursor.fetchone()
    exist = False
    if user != None :
        exist = True
        if user[Usuarios.pais] != None:
            cursor.execute(getCountryQuery, (user[Usuarios.pais],))
            pais = cursor.fetchone()
            user = list(user)
            user[Usuarios.pais] = pais
        
    cursor.close()
    return exist, user

def getUserGame(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserGameQuery, (id, id))
    game = cursor.fetchall()

    cursor.close()
    return game

def getUserFriends(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserFriendsQuery, (id, id))
    friends = cursor.fetchall()

    cursor.close()
    return friends

def insertUser(user, cnx):
    try:
        cursor = cnx.cursor()

        cursor.execute(insertUserQuery, user)
        cnx.commit()
        exito = True

    except mysql.connector.Error as error:
        exito = False
        print("Failed to insert record into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito

def editUser(id, data, cnx):
    try:
        cursor = cnx.cursor()

        exito = True
        cursor.execute(editUserQuery, data+[id])
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to edit record into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito
        
def deleteUser(id, cnx):
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
        print("MySQL connection is closed")
        return exito

def validateUser(correo, cnx):
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

def chageUserPwd(correo, pwd, salt, cnx):
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
        return exito

def getCountry(name, cnx):            
    cursor = cnx.cursor()

    cursor.execute(getCountryQuery, (name,))
    country = cursor.fetchone()
    
    cursor.close()
    return country

def allCountries(cnx): 
    cursor = cnx.cursor()

    cursor.execute(getAllCountryQuery)
    countryList = cursor.fetchall()
    res = list()
    for country in countryList:
        res.append({'name': country[0], 'code': country[1]})

    cursor.close()
    return res

def usersRanking(cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(rankingQuery)
        rankList = cursor.fetchall()
        print(rankList)
    except mysql.connector.Error as error:
        print("Failed to get RankingList into Laptop table {}".format(error))
    finally:
        cursor.close()     
        return rankList 
    
    

#