#--------------------------------------------------------------------------
#
#Comunica con db_helper para obtener toda informacion a devolver al cliente
#
#--------------------------------------------------------------------------
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


def loginUser(correo, pwd):
    
    exist, user = getUser(correo)

    returnValue = { 'exist': exist }
    if exist:
        pwdOk = pwd == user[1]
        returnValue['ok'] = pwdOk
        if pwdOk:
            returnValue['user'] = { 
                'correo': user[0],
                'nick': user[2],
                'name': user[3],
                'birthDate': user[4],
                'pais': user[6],
                'rango': user[9],
                'puntos': user[10],
                'registerDate': user[11]
            }
            userGames = getUserGame(correo)
            returnValue['user']['totalPartidas'] = 0
            returnValue['user']['partidasGanadas'] =0
            returnValue['game'] = []
            for game in userGames: #todas las partidas
                gana = False
                if game[1] != correo: #soy la negra
                    _, oponente = getUser(game[1])
                    tocaMover = not turnoRoja(game[4])
                    if game[3] == 2:
                        gana = True
                else: #soy la roja
                    _, oponente = getUser(game[2])
                    tocaMover = turnoRoja(game[4])
                    if game[3] == 1:
                        gana = True
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