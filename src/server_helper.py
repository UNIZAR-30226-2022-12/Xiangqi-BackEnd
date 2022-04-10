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

PATH = "../profiles/"
SECRET_KEY = "dvk-.klzdzgf6ff<1_:s"

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
        'range': user[Usuarios.rango],
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
            _, oponente = getUser(game[Partidas.roja], cnx)
            tocaMover = not turnoRoja(game[Partidas.movimientos])
            if game[Partidas.estado] == 2: #gana negra
                gana = True
        else: #soy la roja
            _, oponente = getUser(game[Partidas.negra], cnx)
            tocaMover = turnoRoja(game[Partidas.movimientos])
            if game[Partidas.estado] == 1: #gana roja
                gana = True
        gameData = {
            'id': oponente[Usuarios.id],
            'nickaname': oponente[Usuarios.nick],
            'flag': oponente[Usuarios.pais][Pais.flag],
            'country': oponente[Usuarios.pais][Pais.name],
            'startDate': game[Partidas.fechaInicio].strftime('%d/%m/%Y'),
            'lastMovDate': game[Partidas.lastMove].strftime('%d/%m/%Y'),
            'myTurn': tocaMover,
            #'gana': gana
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
        gameDate = datetime.datetime.strptime(game[Partidas.fechaInicio], '%Y-%m-%d').date()
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
    returnValue['diaGanadas'] = [1, 0, 0, 0, 0, 0, 0]
    returnValue['diaJugadas'] = [1, 0, 0, 0, 0, 0, 0]
    for game in latestWin:
        gameDate = datetime.datetime.strptime(game[Partidas.fechaInicio], '%Y-%m-%d').date()
        days = (today - gameDate).days
        if days >= 0 and days < 7:
            returnValue['diaGanadas'][days] += 1
    for game in latestGames:
        gameDate = datetime.datetime.strptime(game[Partidas.fechaInicio], '%Y-%m-%d').date()
        days = (today - gameDate).days
        if days >= 0 and days < 7:
            returnValue['diaJugadas'][days] += 1
    return returnValue

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
                token = jwt.encode({'id': user[Usuarios.id], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY, algorithm="HS256")  
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
        user = [data.email, password_hash, salt, False, data.nickname, data.name, (data.date), data.country.name, None, None, 0, 0, str(datetime.date.today())]
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

def validate(data : EmailData):
    cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')
    cnx.cmd_refresh(RefreshOption.GRANT) 
    returnValue = validateUser(data.email, cnx)
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
                    Haz click en el enlace <a href="http://localhost:8080/#/itsukieslamejorquintilliza?email=""" + correo + """">Recuperar contraseña</a>
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
                    Haz click en el enlace <a href="http://localhost:8080/#/itsukieslamejorquintilliza?email=""" + correo + """">Validar Cuenta</a> 
                    para validar tu cuenta de usuario.
                </p>
            </body>
        </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, email_password)
        smtp.send_message(msg)
    return True

def getUserImage(id):
    print(id)
    file_path = os.path.join(PATH, str(id)+".png")
    if os.path.exists(file_path):
        return True, FileResponse(file_path)
    return False, None
    
