#--------------------------------------------------------------------------
#
#Comunica con db_helper para obtener toda informacion a devolver al cliente
#
#--------------------------------------------------------------------------
import datetime
from db_helper import *

#------------------
#Usuarios: 0:correo, 1:pwd, 2:nick, 3:name, 4:birthDate, 5:foto, 6:pais, 7:fichaSkin, 8:tableroSkin, 9:rango, 10:puntos, 11:fechaRegistro
#Partidas: 0:id, 1:roja, 2:negra, 3:estado, 4:movimientos, 5:fechaInicio, 6:lastMove

#------------------

def turnoRoja(move):
    if move == None:
        return True
    else:
        return (len(move) / 4) % 2 == 0


def loginUser(data):
    
    exist, user = getUser(data['email'])

    returnValue = { 'exist': exist }
    if exist: #si existe el usuario
        pwdOk = data['pwd'] == user[1]
        returnValue['ok'] = pwdOk
        if pwdOk: #si la contraseña empareja
            returnValue['user'] = { #obtener informacion del usuario
                'correo': user[0],
                'nick': user[2],
                'name': user[3],
                'birthDate': user[4],
                'foro': user[5],
                'pais': user[6],
                'rango': user[9],
                'puntos': user[10],
                'registerDate': user[11]
            }
            userGames = getUserGame(data['email'])
            returnValue['user']['totalPartidas'] = len(userGames)
            returnValue['user']['partidasGanadas'] = 0
            returnValue['game'] = []
            for game in userGames: #todas las partidas
                gana = False
                if game[1] != data['email']: #soy la negra
                    _, oponente = getUser(game[1])
                    tocaMover = not turnoRoja(game[4])
                    if game[3] == 2: #gana negra
                        gana = True
                        returnValue['user']['partidasGanadas'] += 1
                else: #soy la roja
                    _, oponente = getUser(game[2])
                    tocaMover = turnoRoja(game[4])
                    if game[3] == 1: #gana roja
                        gana = True
                        returnValue['user']['partidasGanadas'] += 1
                gameData = {
                    'oponente': oponente[2],
                    'foto': oponente[5],
                    'fechaInicio': game[5],
                    'lastMove': game[6],
                    'tocaMover': tocaMover,
                    'gana': gana
                }
                returnValue['game'].append(gameData)

    return returnValue

def registerUser(data):

    exist, _ = getUser(data['email'])

    returnValue = { 'exito': not exist }

    if not exist: #si existe el usuario
        f = open("/home/ubuntu/pythonSRVR/profiles/" + str(data['email']) + ".jpg", 'wb')
        f.write(data['image'])
        #f = open("" + str(data['email']) + ".jpg", 'wb')
        #f.write(data['image'].encode())
        f.close()
        
        user = [data['email'], data['password'], data['nickname'], data['name'], data['date'], data['image'], data['country'], None, None, 0, 0, str(datetime.datetime.now())]
        print(user)
        exito = insertUser(user)
        returnValue['exito'] = exito

    return returnValue