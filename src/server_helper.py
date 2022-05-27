#--------------------------------------------------------------------------
#
#Comunica con db_helper para obtener toda informacion a devolver al cliente
#
#--------------------------------------------------------------------------
from datetime import datetime
from email.message import EmailMessage
import hashlib
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db_helper import *
from clases import *
import base64
from fastapi.responses import FileResponse
import jwt
import json
import random
import mysql.connector
from mysql.connector import RefreshOption
from textwrap import wrap

PATH = "../profiles/"
SECRET_KEY = "dvk-.klzdzgf6ff<1_:s"

usuarios = {}
#------------------
#Usuarios: 0:correo, 1:pwd, 2:salt, 3:validacion, 3:nick, 4:name, 5:birthDate, 6:pais, 7:fichaSkin, 8:tableroSkin, 8:rango, 10:puntos, 11:fechaRegistro, 12: cuentaValida
#Partidas: 0:id, 1:roja, 2:negra, 3:estado, 4:movimientos, 5:fechaInicio, 6:lastMove
#------------------

#------------------metodos de apoyo-----------------------------------------------------------------
def turnoRoja(move):
    if move == None:
        return True
    else:
        return (len(move) / 4) % 2 == 0

def checkPwd(pwd, salt, password):
    hash = hashlib.sha512()
    hash.update(('%s%s' % (salt, pwd)).encode('utf-8'))
    pwd_hash = hash.hexdigest()
    if pwd_hash == password:
        return True
    else:
        return False

def userProfile(id, cnx):
    _, user = getUser(id, cnx)
    friends = getUserFriends(id, cnx)
    hasImage, _ = getUserImage(id)
    returnValue = { #obtener informacion del usuario
        'email': user[Usuarios.correo],
        'nickname': user[Usuarios.nick],
        'name': user[Usuarios.name],
        'birthday': user[Usuarios.birthDate].strftime('%d/%m/%Y'),
        'country': {
                "name" : user[Usuarios.pais][Pais.name],
                "code" : user[Usuarios.pais][Pais.code],
                "flag" : user[Usuarios.pais][Pais.flag]
                },
        'range': userPosition(id, cnx),
        'points': user[Usuarios.puntos],
        'registerDate': user[Usuarios.fechaRegistro].strftime('%d/%m/%Y'),
        'nFriends': len(friends),
        'hasImage': hasImage
    }
    return returnValue

def userGames(id, cnx):
    returnValue = []
    userGames = getUserGame(id, cnx)
    for game in userGames: #todas las partidas
        gana = False
        if game[Partidas.negra] == id: #soy la negra
            if game[Partidas.roja] not in usuarios:
                _, oponente = getUser(game[Partidas.roja], cnx)
                usuarios[game[Partidas.roja]] = oponente
            else:
                oponente = usuarios[game[Partidas.roja]]
            tocaMover = not turnoRoja(game[Partidas.movimientos])

        else: #soy la roja
            if game[Partidas.negra] not in usuarios:
                _, oponente = getUser(game[Partidas.negra], cnx)
                usuarios[game[Partidas.negra]] = oponente
            else:
                oponente = usuarios[game[Partidas.negra]]
            tocaMover = turnoRoja(game[Partidas.movimientos])
            
        hasImage, _ = getUserImage(oponente[Usuarios.id])
        gameData = {
            'id': oponente[Usuarios.id],
            'nickname': oponente[Usuarios.nick],
            'flag': oponente[Usuarios.pais][Pais.flag],
            'country': oponente[Usuarios.pais][Pais.name],
            'startDate': game[Partidas.fechaInicio].strftime('%d/%m/%Y'),
            'lastMovDate': game[Partidas.lastMove].strftime('%d/%m/%Y'),
            'myTurn': tocaMover,
            'hasImage': hasImage,
            'idSala': game[Partidas.id],
            'estado': game[Partidas.estado]
        }
        returnValue.append(gameData)
    return returnValue

def profileStatistics(id, cnx):
    userGames = getUserGame(id, cnx)
    winGames = []
    latestGames = []
    latestWin = []
    
    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)

    for game in userGames:
        latest = False
        gameDate = game[Partidas.fechaInicio].date()
        if gameDate > one_week_ago:
            latestGames.append(game)
            latest = True
        if game[Partidas.roja] == id and game[Partidas.estado] == 1: #soy roja y gana roja
            winGames.append(game)
            if latest:
                latestWin.append(game)
        elif game[Partidas.negra] == id and game[Partidas.estado] == 2: #soy negra y gana negra
            winGames.append(game)
            if latest:
                latestWin.append(game)

    returnValue = { #obtener informacion del usuario
        'totalJugadas': len(userGames),
        'totalGanadas': len(winGames)
    #    'ultimasJugadas': len(latestGames),
    #    'ultimasGanadas': len(latestWin)
    }
    returnValue['diaGanadas'] = [0, 0, 0, 0, 0, 0, 0]
    returnValue['diaJugadas'] = [0, 0, 0, 0, 0, 0, 0]
    for game in latestWin:
        gameDate = game[Partidas.fechaInicio].date()
        days = (today - gameDate).days
        if days >= 0 and days < 7:
            returnValue['diaGanadas'][days] += 1
    for game in latestGames:
        gameDate = game[Partidas.fechaInicio].date()
        days = (today - gameDate).days
        if days >= 0 and days < 7:
            returnValue['diaJugadas'][days] += 1
    return returnValue

#no usar
def calcMovepieza(tablero, pieza, f, c):
    #if pieza >= Piezas.pr1 and pieza <= Piezas.pr4:
        if f >= 5:
            return [(f-1, c)]
        else:
            return [(f-1, c), (f, c-1), (f, c+1)] 
    #elif pieza >= Piezas.pn1 and pieza <= Piezas.pn4:
        if f <= 4:
            return [(f+1, c)]
        else:
            return [(f+1, c), (f, c-1), (f, c+1)] 

#no usar
def calcMove(tablero, equipo):
    move = []
    f = 0
    c = 0
    for fila in tablero:
        for pieza in fila:
            #if pieza in equipoRojo and equipo == 0:
                move[abs(pieza)-1] = calcMovepieza(tablero, pieza, f, c)
            #elif pieza in equipoNegro and equipo == 1:
                move[abs(pieza)-1] = calcMovepieza(tablero, pieza, f, c)
            #c+=1
        f+=1    
        
    

#--------------------------------------------------------------------------------------------------
#            Peticiones
#--------------------------------------------------------------------------------------------------

def loginUser(data : LoginData):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    exist, user = getUserEmail(data.email, cnx)
    returnValue = { 'exist': exist, 'ok': False, 'validacion': False}
    if exist: #si existe el usuario
        returnValue['ok'] = checkPwd(data.pwd, user[Usuarios.salt], user[Usuarios.pwd])
        if user[Usuarios.validacion] : #usuario validado
            returnValue['validacion'] = True
            #crear token de acceso
            if returnValue['ok']:
                token = jwt.encode({'id': user[Usuarios.id], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, SECRET_KEY, algorithm="HS256")  
                returnValue['token'] = token
                returnValue['id'] = user[Usuarios.id]
        else:
            returnValue['validacion'] = False
    cnx.close()
    return returnValue

def registerUser(data : User):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    exist, _ = getUserEmail(data.email, cnx)
    returnValue = False
    if not exist: #si no existe el usuario
        print("No existe")
        #Crear contraseña hasheada
        salt = os.urandom(32).hex()
        hash = hashlib.sha512()
        hash.update(('%s%s' % (salt, data.pwd)).encode('utf-8'))
        password_hash = hash.hexdigest()
        user = [data.email, password_hash, salt, False, data.nickname, data.name, (data.date), data.country.name, None, None, 0, 30, str(datetime.date.today())]
        returnValue = insertUser(user, cnx)
        if returnValue:
            sendEmail(data.email)
            #Guardar foto
            _, user = getUserEmail(data.email, cnx)
            imageLength = len(data.image)
            if imageLength > 0:
                with open(PATH + str(user[Usuarios.id]) + ".png", "wb") as f:
                    image_64_decode = base64.decodestring(data.image)
                    f.write(image_64_decode)
                f.close()
    cnx.close()
    return returnValue

def perfil(id : str):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = {} 
    returnValue['perfil'] = userProfile(id, cnx)
    returnValue['partidas'] = userGames(id, cnx)
    returnValue['estadisticas'] = profileStatistics(id, cnx)
    cnx.close()
    return returnValue

def getProfileInfo(id : str):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = userProfile(id, cnx)
    cnx.close()
    return returnValue

def getNickname(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = userNickname(id, cnx)
    cnx.close()
    return returnValue

def userPoints(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = (getUserPoints(id, cnx))[0]
    cnx.close()
    return returnValue

def validate(data : EmailData):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = validateUser(data.email, cnx)
    cnx.close()
    return returnValue

def getUsers(nick: str):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = []
    users = getUsersNick(nick, cnx)
    for user in users:
        userData = {
            'id': user[Usuarios.id],
            'nickname': user[Usuarios.nick],
            'name': user[Usuarios.name],
            'flag': user[Usuarios.pais][Pais.flag],
            'country': user[Usuarios.pais][Pais.name],
            'birthday': user[Usuarios.birthDate]
        }
        returnValue.append(userData)
    cnx.close()
    return returnValue

def getFriendsRequest(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    remitentes = getUserFriendRequest(id, cnx)
    returnValue = []
    for user in remitentes:
        hasImage, _ = getUserImage(user[Usuarios.id])
        remitente = {
            'id': user[Usuarios.id], 
            'nickname': user[Usuarios.nick], 
            'name': user[Usuarios.name], 
            'flag': user[Usuarios.pais][Pais.flag], 
            'country': user[Usuarios.pais][Pais.name],
            'birthday': user[Usuarios.birthDate],
            'hasImage': hasImage
            }
        returnValue.append(remitente)
    cnx.close()
    return returnValue

def getFriends(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    friends = getUserFriends(id, cnx)
    returnValue = []    
    for user in friends:
        hasImage, _ = getUserImage(user[Usuarios.id])
        friend = {
            'id': user[Usuarios.id], 
            'nickname': user[Usuarios.nick], 
            'name': user[Usuarios.name], 
            'flag': user[Usuarios.pais][Pais.flag], 
            'country': user[Usuarios.pais][Pais.name],
            'hasImage': hasImage
            }
        returnValue.append(friend)
    cnx.close()
    return returnValue

def getUserNoFriends(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = getNotUserFriends(id, cnx)
    cnx.close()
    return returnValue

def getSearchNoFriends(nick, id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    users = searchNotUserFriends(nick, id, cnx)
    returnValue = []
    for user in users:
        hasImage, _ = getUserImage(user[Usuarios.id])
        aux = {
            'id': user[Usuarios.id],
            'nickname': user[Usuarios.nick],
            'name': user[Usuarios.name],
            'flag': user[Usuarios.pais][Pais.flag],
            'country': user[Usuarios.pais][Pais.name],
            'birthday': user[Usuarios.birthDate],
            'sended': user[-1],
            'hasImage': hasImage
            }
        returnValue.append(aux)
    cnx.close()
    return returnValue

def getAllCountries():
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = allCountries(cnx)
    cnx.close()
    return returnValue

def changePwd(data : LoginData):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    salt = os.urandom(32).hex()
    hash = hashlib.sha512()
    hash.update(('%s%s' % (salt, data.pwd)).encode('utf-8'))
    password_hash = hash.hexdigest()
    chageUserPwd(data.email, password_hash, salt, cnx)
    cnx.close()
    return True

def editProfile(id : int, data, image):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    exist, user = getUser(id, cnx)

    returnValue = False
    if exist: #si no existe el usuario
        #Crear contraseña hasheada
        if data['pwd'] != 'a':
            salt = os.urandom(32).hex()
            hash = hashlib.sha512()
            hash.update(('%s%s' % (salt, data['pwd'])).encode('utf-8'))
            password_hash = hash.hexdigest()
        else:
            salt = user[Usuarios.salt]
            password_hash = user[Usuarios.pwd]
        print("cambio")
        date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
        data = [password_hash, salt, data['nickname'], data['name'], date, data['country']]
        
        returnValue = editUser(id, data, cnx)

        if id in usuarios:
            _, user = getUser(id, cnx)
            usuarios[id] = user
        
        imageLength = len(image)
        if imageLength > 0:
            with open(PATH + str(id) + ".png", "wb") as f:
                image_64_decode = base64.decodestring(image)
                f.write(image_64_decode)
            f.close()
    cnx.close()
    return returnValue

def deleteAccount(id : int):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)  
    returnValue = deleteUser(id, cnx)
    file_path = os.path.join(PATH, str(id)+".png")
    if os.path.exists(file_path):
        os.remove(file_path)
    cnx.close()
    return returnValue

def forgotPwd(correo):
    
    sender_email = 'xiangqips@gmail.com'
    email_password = 'Xiangqi2022'

    #contacts = ['741278@unizar.es', 'test@example.com']

    msg = EmailMessage()
    msg['Subject'] = 'Solicitud de cambio de contraseña de la cuenta'
    msg['From'] = sender_email
    msg['To'] = correo

    msg.set_content('Solicitud de cambio de contraseña de la cuenta')

    msg.add_alternative("""\
        <html>
            <body>
                <p><b>Recuperacion de la contraseña</b>
                    Haz click en el enlace <a href="http://psoftbucket.s3-website-eu-west-1.amazonaws.com/#/recPwd?email=""" + correo + """">Recuperar contraseña</a>
                </p>
            </body>
        </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, email_password)
        smtp.send_message(msg)
    return True

def sendEmail(correo):

    sender_email = 'xiangqips@gmail.com'
    email_password = 'Xiangqi2022'

    #contacts = ['741278@unizar.es', 'test@example.com']

    msg = EmailMessage()
    msg['Subject'] = 'Comprobación de cuenta de usuario'
    msg['From'] = sender_email
    msg['To'] = correo

    msg.set_content('Comprobación de la cuenta de usuario')

    msg.add_alternative("""\
        <html>
            <body>
                <p><b>Validación de la cuenta de usuario</b>
                    Haz click en el enlace <a href="http://psoftbucket.s3-website-eu-west-1.amazonaws.com/#/itsukieslamejorquintilliza?email=""" + correo + """">Validar Cuenta</a> 
                    para validar tu cuenta de usuario.
                </p>
            </body>
        </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, email_password)
        smtp.send_message(msg)
        print("enivado")
    return True

def getUserImage(id):
    #print(id)
    file_path = os.path.join(PATH, str(id)+".png")
    if os.path.exists(file_path):
        return True, FileResponse(file_path)
    return False, None

def getRanking():
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)  
    returnValue = []
    ranking = usersRanking(cnx)
    rango = 0
    for rank in ranking:
        hasImage, _ = getUserImage(rank[0])
        user = {
            'id': rank[0],
            'position': rango,
            'nickname': rank[2],
            'flag': rank[3],
            'country': rank[4],
            'winnedGames': rank[5],
            'playedGames': rank[6],
            'hasImage': hasImage
        }
        returnValue.append(user)
        rango += 1
    cnx.close()
    return returnValue

def userHistorial(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    returnValue = []
    historial = getUserHistorial(id, cnx)
    _, me = getUser(id, cnx)
    i = 0
    for game in historial:
        idMov = 0
        if id == game[Partidas.roja]:
            _, opponent = getUser(game[Partidas.negra], cnx)
        else:
            _, opponent = getUser(game[Partidas.roja], cnx)
        movs = []
        tocaRoja = True
        for mov in wrap(game[Partidas.movimientos], 4):
            if tocaRoja:
                idPlayer = game[Partidas.roja]
                tocaRoja = False
                turno = "rojo"
            else:
                idPlayer = game[Partidas.negra]
                tocaRoja = True
                turno = "negro"
                
            if id == idPlayer:
                nickPlayer = me[Usuarios.nick]
                flag = me[Usuarios.pais][Pais.flag]
            else:
                nickPlayer = opponent[Usuarios.nick]
                flag = opponent[Usuarios.pais][Pais.flag]
                
            if game[Partidas.estado] == 3:
                ganador = "empate"
            elif game[Partidas.estado] == 1: #gana roja
                if me[Usuarios.id] == game[Partidas.roja]:
                    ganador = me[Usuarios.nick]
                else:
                    ganador = opponent[Usuarios.nick]
            elif game[Partidas.estado] == 2: #gana negra
                if me[Usuarios.id] == game[Partidas.roja]:
                    ganador = opponent[Usuarios.nick]
                else:
                    ganador = me[Usuarios.nick]  
            else:
                  ganador = "none"
                    
            movAux = {
                'id': idMov, 
                'nickname': nickPlayer, 
                'flag': flag, 
                'color': turno, 
                'origin': "["+ mov[0] + "-" + mov[1] + "]", 
                'destination': "["+ mov[2] + "-" + mov[3] + "]"
            }
            data = {
                'data': movAux
            }
            movs.append(data)
            idMov += 1
        aux = {
            'key': i,
            'data': {
                'date': game[Partidas.fechaInicio].strftime('%d/%m/%Y'),
                'hour': game[Partidas.fechaInicio].strftime('%H:%M'),
                'winnerNickname': ganador
            }, 
            'children': movs
        }
        i += 1
        
        returnValue.append(aux)
    cnx.close()
    return returnValue

###############################
#Funciones Solicitudes
###############################
def rejectRequest(id, idOther):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    exito = rejectFriendRequest(id, idOther, cnx)
    cnx.close()
    return exito

def acceptRequest(id, idOther):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    exito = acceptFriendRequest(id, idOther, cnx)
    cnx.close()
    return exito

###############################
#Funciones partida
###############################

def createGame(id, data):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    exito, idPartida = insertNewGame(id, cnx)
    cnx.close()
    return exito, idPartida

def createNewGame(id, id2, data):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = insertGame(id, id2, cnx)
    cnx.close()
    return returnValue

def deleteGame(id, data):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = deleteGameId(id, cnx)
    cnx.close()
    return returnValue

def loadGame(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    game = getGame(id, cnx)
    cnx.close()
    returnValue = {
                "game": game,
                }
    
    return returnValue

def searchRandomOpponent(id, data):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = joinRandomGame(id, cnx)
    cnx.close()
    
    return returnValue

def joinGame(id, idPartida, data):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = joinRandomGame(id, idPartida, cnx)
    cnx.close()
    return returnValue

def saveMov(id, mov):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = guardarMov(id, mov, cnx)
    print("exito: ", returnValue)
    cnx.close()
    return returnValue

def insertFriendRequest(remitente, destinatario):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = insertSolicitud(remitente, destinatario, cnx)
    cnx.close()
    return returnValue

def finishGame(idSala, idGanador):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    winGame(idSala, idGanador, cnx)
    cnx.close()
    return True

###############################
#Funciones skins tienda
###############################  

def getStoreItems(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)  
    shopItem = getAllShopSkins(cnx)
    userItem = getAllUserSkins(id, cnx)
    
    shop = {
        'setsBoards': [],
        'setsPieces': []
    }
    for item in shopItem:
        have = False
        for userskin in userItem:
            if userskin[0] == item[0] and userskin[1] == item[1]:
                have = True
        
        aux = {
            'id': item[Skins.skinId],
            'tipo': item[Skins.tipo],
            'name': item[Skins.name],
            'desc': item[Skins.description],
            'category': item[Skins.category],
            'price': item[Skins.precio],
            'purchased': have
        }
        if item[Skins.tipo] == 0:    
            shop['setsPieces'].append(aux)
        else:
            shop['setsBoards'].append(aux)
    return shop

def getShopSkinsList():
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)  
    skinsShopList = getAllShopSkins(cnx)
    cnx.close()
    return skinsShopList

def buySkin(id,skinId):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    
    existSkin, skin = getSelectedShopSkin(skinId, cnx)
    returnValue = False
    
    if existSkin:
        _, user = getUser(id, cnx)
        userPoints = user[Usuarios.puntos]
        skinPrice = skin[Skins.precio]
        payOK = updateUserPoints(id, (userPoints-skinPrice), cnx)
        returnValue = addBoughtSkin(user, skin, cnx)    
        
    cnx.close()
    return returnValue

def buySkin(id, skinId, tipo, price):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    
    updateUserPoints(price, id, cnx)
    addBoughtSkin(skinId, tipo, id, cnx)    
        
    cnx.close()
    return True

###############################
#Funciones skins usuario
###############################

def getUserSkinsList(id):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    userSkinsList = getAllUserSkins(id,cnx)
    cnx.close()
    return userSkinsList

# Modificación de la skin de usuario a utilizar para las partidas (provisional)   
def editUserSkin(id,skinId):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT)
    
    exist, skin = getSelectedUserSkin(skinId,id,cnx)
    returnValue = False
    
    if exist:
        _, user = getUser(id,cnx)
        if skin[Skins.tipo] == 0:
            user[Usuarios.fichaSkin] = skinId
            returnValue = changeUserTGSkin(skinId, id, cnx)
        if skin[Skins.tipo] == 1:
            user[Usuarios.tableroSkin] = skinId
            returnValue = changeUserBoardSkin(skinId, id, cnx)
        
    cnx.close()
    return returnValue
    
