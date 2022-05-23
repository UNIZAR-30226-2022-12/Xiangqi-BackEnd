#----------------------------------------------------------------
#
#Modulo de acceso al base de datos
#
#----------------------------------------------------------------
#from curses.ascii import US
import datetime
import mysql.connector
from mysql.connector import RefreshOption

from clases import User, Usuarios

#cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
#                             host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
#                             database='BDpsoft')

getUserQuery = "SELECT * FROM Usuarios WHERE id = %s"
getUsersNickQuery = "SELECT * FROM Usuarios WHERE nick LIKE %s"
getUserEmailQuery = "SELECT * FROM Usuarios WHERE correo = %s"
getUserNicknameQuery = "SELECT nick FROM Usuarios WHERE id = %s"
getUserFriendsQuery = "SELECT * FROM Amigos WHERE usuario1 = %s OR usuario2 = %s"
getUserPointsQuery = "SELECT puntos FROM Usuarios WHERE id = %s"

getFriendRequestQuery = "SELECT remitente FROM Solicitudes WHERE destinatario = %s"
getUserRequestQuery = "SELECT destinatario FROM Solicitudes WHERE remitente = %s"

getFriendsQuery = "SELECT IF(usuario1 = %s, usuario2, usuario1) AS friends FROM Amigos WHERE usuario1 = %s OR usuario2 = %s"
getNotUserFriendsQuery = "SELECT DISTINCT * FROM Usuarios us WHERE us.id NOT IN (" + getFriendsQuery + ") AND us.id != %s"

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

rejectFriendRequestQuery = "DELETE FROM Solicitudes WHERE destinatario = %s and remitente = %s"
acceptFriendRequestQuery = "INSERT INTO Amigos (usuario1, usuario2) VALUE (%s, %s);"

insertGameQuery =  ("INSERT INTO Partidas (roja, negra, estado, movimientos, fechaInicio, lastMove) "
        "VALUE (%s, %s, %s, %s, %s, %s);")
deleteGameIdQuery = "DELETE FROM Partidas WHERE id = %s"
guardarMovQuery = ("UPDATE Partidas SET movimientos = CONCAT(movimientos, %s) WHERE id = %s")
insertSolicitudQuery = ("INSERT INTO Solicitudes (remitente, destinatario) "
        "VALUE (%s, %s);")

getGameQuery = "SELECT * FROM Partidas WHERE id = %s"
getUserHistorialQuery = "SELECT * FROM Partidas WHERE (estado = 1 OR estado = 2 OR estado = 3) AND (roja = %s OR negra = %s)"
buscarPartidaQuery = "SELECT id FROM Partidas WHERE negra = None"
unirPartidaQuery = "UPDATE Partidas SET negra = %s WHERE id = %s"

finishGameQuery = "UPDATE Partidas SET estado = IF(roja = %s, 1, 2) WHERE id = %s"
#---ranking query
userGamePlayed = "SELECT us.id, count(*) AS game FROM Usuarios us, Partidas p WHERE us.id = p.roja OR us.id = p.negra GROUP BY us.id"
userGameWon = "SELECT us.id, count(*) AS game FROM Usuarios us, Partidas p WHERE (us.id = p.roja AND p.estado = 1) OR (us.id = p.negra AND p.estado = 2) GROUP BY us.id"
userGameStat = "SELECT played.id, played.game AS pg, won.game AS wg FROM (" + userGamePlayed + ") played, (" + userGameWon + ") won WHERE played.id = won.id" 
rankingQuery = "SELECT us.id, us.rango, us.nick, c.bandera, us.pais, ug.wg, ug.pg FROM Usuarios us, Country c, (" + userGameStat + ") ug WHERE us.pais = c.name AND us.id = ug.id ORDER BY ug.wg DESC, ug.wg/ug.pg DESC"
#---shopping queries
#checkStateSkinQuery = "SELECT * FROM Skins s, Tiene t, Usuarios us WHERE (s.skinId <> t.skinId) AND (us.id <> t.usuario) AND s.skinId = %s AND us.id = %s "
#Consulta 1 = Sacar todas las skins que tiene un usuario
#Consulta 2 = Diferencia <todasSkinsTienda> - <todasSkinsUsuario>
#buyBoardSkinQuery = "SELECT s.skinId FROM Skins s, Usuarios us, Tiene t WHERE (" + checkStateSkinQuery + ") AND s.tipo = 1 AND s.precio >= us.puntos" 
#buyTokenSkinQuery = "SELECT s.skinId FROM Skins s, Usuarios us, Tiene t WHERE (" + checkStateSkinQuery + ") AND s.tipo = 0 AND s.precio >= us.puntos"
showAllSkinsQuery = "SELECT * FROM Skins"
selectSkinQuery = "SELECT s.skinId FROM Skins s, Usuarios us WHERE s.precio <= us.puntos AND s.skinId = %s"
addNewUserSkinQuery = "INSERT INTO Tiene (skinId, tipo, usuario) VALUE (%s, %s, %s);"
editUserPointsQuery = "UPDATE Usuarios SET puntos = puntos + %s WHERE id = %s"

#---user skins queries
#selectBoardQuery = "SELECT t.skinId FROM Tiene t, Skins s WHERE s.tipo = 1 AND t.skinId = %s"
#selectGameTokenQuery = "SELECT t.skinId FROM Tiene t, Skins s WHERE s.tipo = 0 AND t.skinId = %s"
getUserSkinsQuery = "SELECT * FROM Tiene t WHERE t.usuario = %s"
selectUserSkinQuery = "SELECT t.skinId FROM Tiene t WHERE t.skinId = %s and t.usuario = %s"
changeUserBoardSkinQuery = "UPDATE Usuario SET tableroSkin = %s WHERE id = %s"
changeUserTGSkinQuery = "UPDATE Usuario SET fichaSkin = %s WHERE id = %s"

DEFAULT_USER = 14

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

def getUsersNick(nick, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUsersNickQuery, ("%" + nick + "%",))
    usersData = cursor.fetchall()
    users = []
    if len(usersData) != 0:
        for user in usersData:
            aux = user
            if user[Usuarios.pais] != None:
                cursor.execute(getCountryQuery, (user[Usuarios.pais],))
                pais = cursor.fetchone()
                aux = list(user)
                aux[Usuarios.pais] = pais
            users.append(aux)
    return users

def userNickname(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserNicknameQuery, (id,))
    nick = (cursor.fetchone())[0]
    
    cursor.close()
    return nick

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

def getUserPoints(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserPointsQuery, (id,))
    points = cursor.fetchone()

    cursor.close()
    return points

def getUserGame(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getUserGameQuery, (id, id))
    game = cursor.fetchall()

    cursor.close()
    return game

def getUserFriendRequest(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getFriendRequestQuery, (id,))
    idRemitentes = cursor.fetchall()
    remitentes = []
    for ids in idRemitentes:
        _, user = getUser(ids[0], cnx)
        remitentes.append(user)
    #print(friends)
    cursor.close()
    return remitentes

def getUserFriends(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getFriendsQuery, (id, id, id))
    idFriends = cursor.fetchall()
    friends = []
    for ids in idFriends:
        _, user = getUser(ids[0], cnx)
        friends.append(user)
    #print(friends)
    cursor.close()
    return friends

def getNotUserFriends(id, cnx):
    cursor = cnx.cursor()

    cursor.execute(getNotUserFriendsQuery, (id, id, id, id))
    friends = cursor.fetchall()

    cursor.close()
    return friends

def searchNotUserFriends(nick, id, cnx):
    cursor = cnx.cursor()
    
    cursor.execute(getUsersNickQuery, ("%" + nick + "%",))
    users = cursor.fetchall()
    cursor.execute(getFriendsQuery, (id, id, id))
    friend = cursor.fetchall()
    cursor.execute(getUserRequestQuery, (id, ))
    requestSended = cursor.fetchall()
    friendId = [(a) for (a, ) in friend]
    request = [(a) for (a, ) in requestSended]
    
    result = []
    for user in users:
        if user[Usuarios.id] not in friendId + [id]:
            if user[Usuarios.pais] != None:
                cursor.execute(getCountryQuery, (user[Usuarios.pais],))
                pais = cursor.fetchone()
                user = list(user)
                user[Usuarios.pais] = pais
            aux = user 
            if user[Usuarios.id] not in request:
                aux += (False,)
            else:
                aux += (True,)
            result.append(aux)
    cursor.close()
    return result

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
    
def rejectFriendRequest(id, idOther, cnx):
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
        #print(rankList)
    except mysql.connector.Error as error:
        print("Failed userRanking {}".format(error))
    finally:
        cursor.close()     
        return rankList 
    
def userPosition(id, cnx):
    pos = -1
    try:
        cursor = cnx.cursor()
        cursor.execute(rankingQuery)
        ranking = cursor.fetchall()
        pos = 0
        for user in ranking:
            if user[0] == id: 
                break
            pos += 1
    except mysql.connector.Error as error:
        print("Failed userRanking {}".format(error))
    finally:
        cursor.close()     
        return pos    

def insertNewGame(id, cnx):
    idPartida = -1
    exito = False
    try:
        exito = True
        cursor = cnx.cursor()
        
        cursor.execute(insertGameQuery, (id, DEFAULT_USER, 0, "", datetime.datetime.now(), datetime.datetime.now()))
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
    
def insertSolicitud(remitente, destinatario, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(insertSolicitudQuery, (remitente, destinatario)) 
        cnx.commit()
    except mysql.connector.Error as error:
        print("Failed insertSolicitud {}".format(error))
        return False
    finally:
        cursor.close()     
        return True
    
def getUserHistorial(id, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(getUserHistorialQuery, (id, id)) 
        historial = cursor.fetchall()
        cnx.commit()
    except mysql.connector.Error as error:
        print("Failed getUserHistorial {}".format(error))
        return []
    finally:
        cursor.close()     
        return historial 

def winGame(idSala, idGanador, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(finishGameQuery, (idGanador, idSala)) 
        cursor.execute(editUserPointsQuery, (10, idGanador)) 
        cnx.commit()
    except mysql.connector.Error as error:
        print("Failed winGame {}".format(error))
        return False
    finally:
        cursor.close()     
        return True

####################################################
# Funciones relacionadas con la gestión de los skins
####################################################
def addBoughtSkin(skinId, tipo, userId, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(addNewUserSkinQuery,(skinId, tipo, userId))
        cnx.commit()
        exito = True

    except mysql.connector.Error as error:
        exito = False
        print("Failed to insert bought skin into Laptop table {}".format(error))
    finally:
        cursor.close()
        return exito  

def getAllShopSkins(cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(showAllSkinsQuery)
        skinShopList = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to get RankingList into Laptop table {}".format(error))
    finally:
        cursor.close()     
        return skinShopList 
    
def updateUserPoints(price, id, cnx):
    try:
        cursor = cnx.cursor()
        exito = True
        cursor.execute(editUserPointsQuery,(price, id))
        cnx.commit()

    except mysql.connector.Error as error:
        exito = False
        print("Failed to edit userPoints into Laptop table {}".format(error))
    finally:
        cursor.close()
        return exito  

def getAllUserSkins(id, cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute(getUserSkinsQuery, (id,))
        userSkinsList = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to get RankingList into Laptop table {}".format(error))
    finally:
        cursor.close()     
        return userSkinsList

def getSelectedUserSkin(skinId, id, cnx):
    cursor = cnx.cursor()
    
    cursor.execute(selectUserSkinQuery, (skinId,id,))
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
    
###############################
#Funciones Solicitudes
###############################
def rejectFriendRequest(id, idOther, cnx):
    try:
        cursor = cnx.cursor()

        cursor.execute(rejectFriendRequestQuery, (id, idOther))
        cnx.commit()

    except mysql.connector.Error as error:
        print("Failed rejectFriendRequest {}".format(error))
    finally:
        cursor.close()
        return True
    
def acceptFriendRequest(id, idOther, cnx):
    try:
        cursor = cnx.cursor()

        cursor.execute(rejectFriendRequestQuery, (id, idOther))
        cursor.execute(acceptFriendRequestQuery, (id, idOther))
        cnx.commit()

    except mysql.connector.Error as error:

        print("Failed acceptFriendRequest {}".format(error))
    finally:
        cursor.close()
        return True