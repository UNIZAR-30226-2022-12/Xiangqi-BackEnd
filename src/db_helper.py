#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
from curses.ascii import US
import datetime
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

insertGameQuery =  ("INSERT INTO Partidas (roja, negra, estado, movimientos, fechaInicio, lastMove) "
        "VALUE (%s, %s, %s, %s, %s, %s);")
deleteGameIdQuery = "DELETE FROM Partidas WHERE id = %s"
guardarMovQuery = ("UPDATE Partidas SET movimientos = CONCAT(movimientos, %s) WHERE id = %s")
getGameQuery = "SELECT * FROM Partidas WHERE id = %s"
buscarPartidaQuery = "SELECT id FROM Partidas WHERE negra = None"
unirPartidaQuery = "UPDATE Partidas SET negra = %s WHERE id = %s"

#---ranking query
userGamePlayed = "SELECT us.id, count(*) AS game FROM Usuarios us, Partidas p WHERE us.id = p.roja OR us.id = p.negra GROUP BY us.id"
userGameWon = "SELECT us.id, count(*) AS game FROM Usuarios us, Partidas p WHERE (us.id = p.roja AND p.estado = 1) OR (us.id = p.negra AND p.estado = 2) GROUP BY us.id"
userGameStat = "SELECT played.id, played.game AS pg, won.game AS wg FROM (" + userGamePlayed + ") played, (" + userGameWon + ") won WHERE played.id = won.id" 
rankingQuery = "SELECT us.id, us.nick, us.pais, c.code, c.bandera, us.rango, ug.pg, ug.wg FROM Usuarios us, Country c, (" + userGameStat + ") ug WHERE us.pais = c.name AND us.id = ug.id ORDER BY ug.wg DESC"

#---shopping queries
#checkStateSkinQuery = "SELECT * FROM Skins s, Tiene t, Usuarios us WHERE (s.skinId <> t.skinId) AND (us.id <> t.usuario) AND s.skinId = %s AND us.id = %s "
#Consulta 1 = Sacar todas las skins que tiene un usuario
#Consulta 2 = Diferencia <todasSkinsTienda> - <todasSkinsUsuario>
#buyBoardSkinQuery = "SELECT s.skinId FROM Skins s, Usuarios us, Tiene t WHERE (" + checkStateSkinQuery + ") AND s.tipo = 1 AND s.precio >= us.puntos" 
#buyTokenSkinQuery = "SELECT s.skinId FROM Skins s, Usuarios us, Tiene t WHERE (" + checkStateSkinQuery + ") AND s.tipo = 0 AND s.precio >= us.puntos"
showAllSkinsQuery = "SELECT * FROM Skins"
checkUserPointsQuery = "SELECT us.puntos FROM Usuarios us WHERE us.id = %d"
availableSkinsQuery = "SELECT s.skinId, s.tipo, s.precio FROM Skins s, Usuarios us WHERE s.precio <= us.puntos AND us.id = %s"
selectSkinQuery = "SELECT * FROM (" + availableSkinsQuery + ") disponible WHERE disponible.skinId = %s"
addNewUserSkinQuery = "INSERT INTO Tiene (skinId, usuario) VALUE (%s, %s);"
editUserPointsQuery = "UPDATE Usuario SET puntos = %s WHERE id = %s"



#---user skins queries
#selectBoardQuery = "SELECT t.skinId FROM Tiene t, Skins s WHERE s.tipo = 1 AND t.skinId = %s"
#selectGameTokenQuery = "SELECT t.skinId FROM Tiene t, Skins s WHERE s.tipo = 0 AND t.skinId = %s"
getUserSkinsQuery = "SELECT * FROM Tiene t WHERE t.usuario = %s"
selectUserSkinQuery = "SELECT t.skinId FROM Tiene t WHERE t.skinId = %s and t.usuario = %s"
changeUserBoardSkinQuery = "UPDATE Usuario SET tableroSkin = %s WHERE id = %s"
changeUserTGSkinQuery = "UPDATE Usuario SET fichaSkin = %s WHERE id = %s"



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
        print("Failed editUser {}".format(error))
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
        print("Failed deleteUser {}".format(error))
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
        print("Failed validateUser {}".format(error))
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
        print("Failed changeUserPwd {}".format(error))
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
        print("Failed userRanking {}".format(error))
    finally:
        cursor.close()     
        return rankList 
    

def insertNewGame(id, cnx):
    idPartida = -1
    exito = False
    try:
        exito = True
        cursor = cnx.cursor()
        
        cursor.execute(insertGameQuery, (id, 14, 0, "", datetime.datetime.now(), datetime.datetime.now()))
        print("hola")

        idPartida = cursor.lastrowid
        cnx.commit()
    except mysql.connector.Error as error:
        print("Failed insertNewGame {}".format(error))
        exito = False
    finally:
        cursor.close()     
        return exito, idPartida
    
def insertGame(id, id2, cnx):
    try:
        cursor = cnx.cursor()
        
        cursor.execute(insertGameQuery, (id, id2, 0, "", datetime.datetime.now(), None))
        cnx.commit()
        print("buenas")
        idPartida = cursor.lastrowid
    except mysql.connector.Error as error:
        print("Failed insertGame {}".format(error))
        return -1
    finally:
        cursor.close()     
        return idPartida 
    
def deleteGameId(id, cnx):
    try:
        exito = True
        cursor = cnx.cursor()
        
        cursor.execute(deleteGameIdQuery, (id,))
        cnx.commit()
    except mysql.connector.Error as error:
        print("Failed deleteGameId {}".format(error))
        exito = False
    finally:
        cursor.close()     
        return exito 
    
def getGame(id, cnx):
    try:
        cursor = cnx.cursor()
        
        cursor.execute(getGameQuery, (id,))
        game = cursor.fetchone()
    except mysql.connector.Error as error:
        print("Failed getGame {}".format(error))
    finally:
        cursor.close()     
        return game

def joinRandomGame(id, idPartida, cnx):
    try:
        cursor = cnx.cursor()
        
        cursor.execute(unirPartidaQuery, (id, idPartida))
        cnx.commit()
        
    except mysql.connector.Error as error:
        print("Failed joinRandomGame {}".format(error))
        return False
    finally:
        cursor.close()     
        return True
    
def guardarMov(id, mov, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(guardarMovQuery, (mov, id)) 
        cnx.commit()
    except mysql.connector.Error as error:
        print("Failed guardarMov {}".format(error))
        return False
    finally:
        cursor.close()     
        return True

####################################################
# Funciones relacionadas con la compra de una skin
####################################################
def getAllShopSkins(cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(showAllSkinsQuery)
        skinShopList = cursor.fetchall()
        print(skinShopList)
    except mysql.connector.Error as error:
        print("Failed to get RankingList into Laptop table {}".format(error))
    finally:
        cursor.close()     
        return skinShopList
        
def getUserPoints(id, cnx):
    cursor = cnx.cursor()
    cursor.execute(getUserPointsQuery, (id, ))
    userPoints = cursor.fetchall()
    cursor.close()
    return userPoints
       
def getSelectedShopSkin(id, skinId, cnx):
    cursor = cnx.cursor()
    cursor.execute(selectSkinQuery, (id, skinId, ))
    shopSkins = cursor.fetchAll()
    exist = (shopSkins != None)    
    cursor.close()
    return exist, shopSkins  
    
def updateUserPoints(newScore, id, cnx):
    try:
        cursor = cnx.cursor()
        exito = True
        cursor.execute(editUserPointsQuery,newScore,id)
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to edit userPoints into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito

def addBoughtSkin(skinId, userId, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(addNewUserSkinQuery,(skinId, userId, ))
        cnx.commit()
        exito = True

    except mysql.connector.Error as error:
        exito = False
        print("Failed to insert bought skin into Laptop table {}".format(error))
    finally:
        cursor.close()
        print("MySQL connection is closed")
        return exito    

##################################################################
# Funciones relacionadas con la gestión de las skins del usuario
##################################################################

def getAllUserSkins(id, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(getUserSkinsQuery, (id, ))
        userSkinsList = cursor.fetchall()
        print(userSkinsList)
    except mysql.connector.Error as error:
        print("Failed to get RankingList into Laptop table {}".format(error))
    finally:
        cursor.close()     
        return userSkinsList

def getSelectedUserSkin(skinId, id, cnx):
    cursor = cnx.cursor()
    
    cursor.execute(selectUserSkinQuery, (skinId, id, ))
    userSkin = cursor.fetchone()
    exist = userSkin != None
    cursor.close()
    return exist, skinUser

def changeUserBoardSkin(skinId, id, cnx):
    try:
        cursor = cnx.cursor()        
        cursor.execute(changeUserBoardSkinQuery,(skinId,id,))
        exito = True
        cnx.commit()
    except mysql.connector.Error as error:
        exito = False
        print("Failed to change user board skin into Laptop table {}".format(error))
    finally:
        cursor.close()
        return exito   

def changeUserTGSkin(skinId, id, cnx):
    try:
        cursor = cnx.cursor()        
        cursor.execute(changeUserTGSkinQuery,(skinId,id,))
        exito = True
        cnx.commit()
    except mysql.connector.Error as error:
        exito = False
        print("Failed to change user token game skin into Laptop table {}".format(error))
    finally:
        cursor.close()
        return exito