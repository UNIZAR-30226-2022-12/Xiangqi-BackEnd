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

#------------------
#Usuarios: 0:correo, 1:pwd, 2:salt, 3:nick, 4:name, 5:birthDate, 6:pais, 7:fichaSkin, 8:tableroSkin, 8:rango, 10:puntos, 11:fechaRegistro, 12: cuentaValida
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
    foto = open("/home/ubuntu/pythonSRVR/profiles/" + str(user[0]) + ".jpg", 'r')
    #foto = open("" + str(user[0]) + ".jpg", 'r')
    returnValue = { #obtener informacion del usuario
        'foto': foto.read(),
        'correo': user[0],
        'nick': user[3],
        'name': user[4],
        'birthDate': user[5],
        'pais': user[6],
        'rango': user[9],
        'puntos': user[10],
        'registerDate': user[11]
    }
    return returnValue

def userGames(correo):
    returnValue = []
    userGames = getUserGame(correo)
    for game in userGames: #todas las partidas
        gana = False
        if game[1] != correo: #soy la negra
            _, oponente = getUser(game[1])
            tocaMover = not turnoRoja(game[4])
            if game[3] == 2: #gana negra
                gana = True
        else: #soy la roja
            _, oponente = getUser(game[2])
            tocaMover = turnoRoja(game[4])
            if game[3] == 1: #gana roja
                gana = True
        foto = open("/home/ubuntu/pythonSRVR/profiles/" + str(oponente[0]) + ".jpg", 'r')
        #foto = open("" + str(oponente[0]) + ".jpg", 'r')
        gameData = {
            'foto': foto.read(),
            'oponente': oponente[3],
            'fechaInicio': game[5],
            'lastMove': game[6],
            'tocaMover': tocaMover,
            'gana': gana
        }
        returnValue.append(gameData)
    return returnValue

def profileStatistics(correo):
    userGames = getUserGame(correo)
    winGames = []
    latestGames = []
    latestWin = []
    
    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)

    for game in userGames:
        latest = False
        gameDate = datetime.datetime.strptime(game[5], '%Y-%m-%d').date()
        if gameDate > one_week_ago:
            latestGames.append(game)
            latest = True
        if game[1] == correo and game[3] == 1: #soy roja y gana roja
            winGames.append(game)
            if latest:
                latestWin.append(game)
        elif game[2] == correo and game[3] == 2: #soy negra y gana negra
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
        gameDate = datetime.datetime.strptime(game[5], '%Y-%m-%d').date()
        days = (today - gameDate).days
        if days >= 0 and days < 7:
            returnValue['dia'][days] += 1
    return returnValue

def loginUser(data):
    
    exist, user = getUser(data.email)

    returnValue = { 'exist': exist, 'ok': False, 'cuentaValida': False}
    if exist: #si existe el usuario
        returnValue['ok'] = checkPwd(data.pwd, user[2], user[1])
        #!!
        returnValue['cuentaValida'] = checkAccount(data.cuentaValida,user[12])
    return returnValue

def registerUser(data : User):

    exist, _ = getUser(data.email)

    returnValue = False
    if not exist: #si no existe el usuario
        #Guardar foto
        f = open("/home/ubuntu/pythonSRVR/profiles/" + str(data.email) + ".jpg", 'wb')
        f.write(data['image'])
        #f = open("" + str(data['email']) + ".jpg", 'wb')
        #f.write(data['image'].encode())
        f.close()
        #Crear contraseña hasheada
        salt = os.urandom(32).hex()
        hash = hashlib.sha512()
        hash.update(('%s%s' % (salt, data.pwd)).encode('utf-8'))
        password_hash = hash.hexdigest()

        user = [data.email, password_hash, salt, data.nickname, data.name, data.date, data.country, None, None, 0, 0, str(datetime.date.today())]
        returnValue = insertUser(user)

    return returnValue

def perfil(data):
    
    exist, user = getUser(data)

    returnValue = { 'exist': exist } 
    if exist: #si existe el usuario
        returnValue['perfil'] = userProfile(user[0])
        returnValue['partidas'] = userGames(data)
        returnValue['estadisticas'] = profileStatistics(data)

    return returnValue

def validate(data):
    
    returnValue = validateUser(data.email)

    return returnValue

#!!
def checkAccount(acc, userAccount):
    if acc == userAccount: 
        return True
    else:
        return False


def validateUser(email):

    sender_email = "xiangqips@gmail.com"
    receiver_email = email
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
                Haz click en el enlace <a href="">Validar Cuenta</a> 
                para validar tu cuenta de usuario.
            </p>
        </body>
    </html>
    """
    
    contenido = MIMEText(html,"html")
    
    message.attach(contenido)
    
    context = ssl.create_default_context
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    returnValue = {'cuentaValida'}
    returnValue['cuentaValida'] = True
    return returnValue