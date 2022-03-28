#--------------------------------------------------------------------------
#
#Comunica con db_helper para obtener toda informacion a devolver al cliente
#
#--------------------------------------------------------------------------
import datetime
import hashlib
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db_helper import *
from clases import *
import base64
from fastapi.responses import FileResponse
import json
import random

PATH = "profiles/"


#------------------
#Usuarios: 0:correo, 1:pwd, 2:salt, 3:validacion, 3:nick, 4:name, 5:birthDate, 6:pais, 7:fichaSkin, 8:tableroSkin, 8:rango, 10:puntos, 11:fechaRegistro, 12: cuentaValida
#Partidas: 0:id, 1:roja, 2:negra, 3:estado, 4:movimientos, 5:fechaInicio, 6:lastMove
#------------------

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

def userProfile(correo):
    _, user = getUser(correo)
    file_path = os.path.join(PATH, correo+".png")
    if os.path.exists(file_path):
        image = FileResponse(file_path)
    else:
        file_path = os.path.join(PATH, "img_placeholder.svg")
        image = FileResponse(file_path)
    returnValue = { #obtener informacion del usuario
        'foto':  image,
        'correo': user[Usuarios.correo],
        'nick': user[Usuarios.nick],
        'name': user[Usuarios.name],
        'birthDate': user[Usuarios.birthDate],
        'pais': {
                "name" : user[Usuarios.pais][Pais.name],
                "code" : user[Usuarios.pais][Pais.code],
                "bandera" : user[Usuarios.pais][Pais.bandera]
                },
        'rango': user[Usuarios.rango],
        'puntos': user[Usuarios.puntos],
        'registerDate': user[Usuarios.fechaRegistro]
    }
    return returnValue

def userGames(correo):
    returnValue = []
    userGames = getUserGame(correo)
    for game in userGames: #todas las partidas
        gana = False
        if game[Partidas.negra] == correo: #soy la negra
            _, oponente = getUser(game[Partidas.roja])
            tocaMover = not turnoRoja(game[Partidas.movimientos])
            if game[Partidas.estado] == 2: #gana negra
                gana = True
        else: #soy la roja
            _, oponente = getUser(game[Partidas.negra])
            tocaMover = turnoRoja(game[Partidas.movimientos])
            if game[Partidas.estado] == 1: #gana roja
                gana = True
        file_path = os.path.join(PATH, oponente[Usuarios.correo]+".png")
        if os.path.exists(file_path):
            image = FileResponse(file_path)
        else:
            file_path = os.path.join(PATH, "img_placeholder.svg")
            image = FileResponse(file_path)
        gameData = {
            'foto': image,
            'oponente': oponente[Usuarios.nick],
            'fechaInicio': game[Partidas.fechaInicio],
            'lastMove': game[Partidas.lastMove],
            'tocaMover': tocaMover,
            'gana': gana
        }
        returnValue.append(gameData)
    return image

def profileStatistics(correo):
    userGames = getUserGame(correo)
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
        if game[Partidas.roja] == correo and game[Partidas.estado] == 1: #soy roja y gana roja
            winGames.append(game)
            if latest:
                latestWin.append(game)
        elif game[Partidas.negra] == correo and game[Partidas.estado] == 2: #soy negra y gana negra
            winGames.append(game)
            if latest:
                latestWin.append(game)

    returnValue = { #obtener informacion del usuario
        'totalJugadas': len(userGames),
        'totalGanadas': len(winGames),
        'ultimasJugadas': len(latestGames),
        'ultimasGanadas': len(latestWin)
    }
    returnValue['dia'] = [0, 0, 0, 0, 0, 0, 0]
    for game in latestWin:
        gameDate = datetime.datetime.strptime(game[Partidas.fechaInicio], '%Y-%m-%d').date()
        days = (today - gameDate).days
        if days >= 0 and days < 7:
            returnValue['dia'][days] += 1
    return returnValue

def loginUser(data : LoginData):
    
    exist, user = getUser(data.email)

    returnValue = { 'exist': exist, 'ok': False, 'validacion': False}
    if exist: #si existe el usuario
        returnValue['ok'] = checkPwd(data.pwd, user[Usuarios.salt], user[Usuarios.pwd])
        print(user[Usuarios.validacion])
        if user[Usuarios.validacion] :
            returnValue['validacion'] = True
        else:
            returnValue['validacion'] = False
    return returnValue

def registerUser(data : User):

    exist, _ = getUser(data.email)

    returnValue = False
    if not exist: #si no existe el usuario
        print("No existe")
        #Guardar foto
        with open("" + str(data.email) + ".png", "wb") as f:
        #with open("/home/ubuntu/pythonSRVR/profiles/" + str(data.email) + ".png", 'wb') as f:
            f.write(base64.urlsafe_b64encode(data.image))
        f.close()
        #Crear contraseña hasheada
        salt = os.urandom(32).hex()
        hash = hashlib.sha512()
        hash.update(('%s%s' % (salt, data.pwd)).encode('utf-8'))
        password_hash = hash.hexdigest()

        user = [data.email, password_hash, salt, False, data.nickname, data.name, (data.date).date(), data.country.name, None, None, 0, 0, str(datetime.date.today())]
        returnValue = insertUser(user)
        sendEmail(data.email)
    return returnValue

def perfil(correo : str):

    exist, _ = getUser(correo)

    returnValue = { 'exist': exist } 
    file_path = os.path.join(PATH, correo+".png")
    if os.path.exists(file_path):
        image = FileResponse(file_path)
    else:
        file_path = os.path.join(PATH, "img_placeholder.svg")
        image = FileResponse(file_path)
        if exist: #si existe el usuario
            returnValue['perfil'] = userProfile(correo)
            returnValue['partidas'] = userGames(correo)
            returnValue['estadisticas'] = profileStatistics(correo)

    return {"ok": False, "hola": "hola", "imagen": image}

def validate(data : EmailData):
    
    returnValue = validateUser(data.email)

    return returnValue

def allCountry():
    
    returnValue = getAllCountry()

    return returnValue

def changePwd(data : LoginData):
    exist, _ = getUser(data.email)
    if exist: #si
        salt = os.urandom(32).hex()
        hash = hashlib.sha512()
        hash.update(('%s%s' % (salt, data.pwd)).encode('utf-8'))
        password_hash = hash.hexdigest()
        chageUserPwd(data.email, password_hash, salt)
    return exist

def forgotPwd(correo):
    exist, _ = getUser(correo)
    if exist:
        print("Enviamos correo")
        sender_email = "xiangqips@gmail.com"
        receiver_email = correo
        password = "Xiangqi2022" 
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Confirmación de la cuenta de usuario"
        message["From"] = sender_email
        message["To"] = receiver_email
        
        # Mensaje que contiene el link a la página de login (falta poner enlace a la página de login)
        html = """\
        <html>
            <body>
                <p><b>Recuperacion de la contraseña</b>
                    Haz click en el enlace <a href="http://localhost:8080/#/itsukieslamejorquintilliza?email=""" + correo + """">Recuperar contraseña</a> 
                </p>
            </body>
        </html>
        """

    
        contenido = MIMEText(html,"html")
        
        message.attach(contenido)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            print("MAIL GUAY")
            server.sendmail(
                sender_email, receiver_email, message.as_string()
                
            )
    return exist

def sendEmail(correo):
    print("Enviamos correo")
    sender_email = "xiangqips@gmail.com"
    receiver_email = correo
    password = "Xiangqi2022" 
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmación de la cuenta de usuario"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Mensaje que contiene el link a la página de login (falta poner enlace a la página de login)
    html = """\
    <html>
        <body>
            <p><b>Validación de la cuenta de usuario</b>
                Haz click en el enlace <a href="http://localhost:8080/#/itsukieslamejorquintilliza?email=""" + correo + """">Validar Cuenta</a> 
                para validar tu cuenta de usuario.
            </p>
        </body>
    </html>
    """
    
    contenido = MIMEText(html,"html")
    
    message.attach(contenido)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        print("MAIL GUAY")
        server.sendmail(
            sender_email, receiver_email, message.as_string()
            
        )