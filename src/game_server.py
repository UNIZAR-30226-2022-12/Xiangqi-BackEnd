import socketio
from server_helper import *

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

app = socketio.WSGIApp(sio)

mov = {}
wait = {}
friendWaiting = []

connected = {}

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('returnConnect', {'exito': True})
    
@sio.event
def disconnect(sid):
    x = connected.items()
    for id in x:
        if id[1] == sid:
            connected.pop(id[0])
            break
    print('disconnect ', sid, connected)

@sio.event
def enter(sid, data):
    connected[data['id']] = sid
    print('enter ', sid, data, connected)

@sio.event
def getOnlineFriends(sid, data):
    print("Me piden amigos: ", data['id'])
    friends = getFriends(data['id'])
    #friends = [{"id": 15, "nickname": "Shiki"}]
    print("friends:", friends)
    aux = []
    for friend in friends:
        print(friend['id'], connected.get(str(friend['id'])))
        if connected.get(str(friend['id'])) != None: # Esta conectado
            aux.append(friend)
    sio.emit('onlineFriends',aux, to=connected[data['id']])
    print("EMITED: ", aux, "TO: ", connected[data['id']])

@sio.event
def sendGameRequest(sid, data):
    print(data)
    print(connected.get(str(data['idFriend'])))
    if connected.get(str(data['idFriend'])) != None: # Esta conectado
        print("Esta conectado", data)
        friendWaiting.append(data['id'])
        exito, idSala = createGame(data['id'], data)
        if exito:
            print(idSala)
            sio.enter_room(sid, str(idSala))
        sio.emit("gameRequest", {"id":data["id"], "idSala": str(idSala)},  to=connected[str(data['idFriend'])])

@sio.event
def rejectReq(sid, data):
    print("REJEC: ",data, connected[str(data['id'])])

    exito = deleteGame(data['id'], data)
    sio.emit("rejectReq",(),  to=connected[str(data['id'])])

@sio.event
def cancelGameRequest(sid, data):
    print("cancel: ",data)
    print(friendWaiting, data['id'])
    friendWaiting.remove(data['id'])
    exito = deleteGame(data['id'], data)

@sio.event
def cancelGameRandom(sid, data):
    print("cancelRandom: ",data)
    print(wait)
    del(wait[str(data['id'])])
    print(wait)
    exito = deleteGame(data['id'], data)

@sio.event
def acceptReq(sid, data):
    print("ACCEPT: ",data, connected[str(data['idFriend'])])
    idOpponent = data['idFriend']
    idSala = data['idSala']
    print(data['idFriend'], friendWaiting)
    if data['idFriend'] in friendWaiting:
        exito = joinGame(data['id'], idSala, data)
        if exito:
            print("empareja ", data['id'], idOpponent, idSala)
            sio.enter_room(sid, str(idSala))
            #sio.emit('startGame', {'idOponent': id
            # Opponent, 'idSala': idSala, 'rojo': False}, room=sid)
            sio.emit('startGame', {'idOponent': data['id'], 'idSala': idSala, 'rojo': True}, to=str(idSala), skip_sid = sid)
            sio.emit('startGame', {'idOponent': idOpponent, 'idSala': idSala, 'rojo': False}, to=sid)
            print("EMITED TO", str(idSala))
    else:
        print("noGame")
        sio.emit('noGame', (), to=sid)
    

@sio.event
def sendFriendRequest(sid, data):
    print(connected.get(str(data['idFriend'])))
    if connected.get(str(data['idFriend'])) != None: # Esta conectado
        print("Esta conectado", data)
        sio.emit("friendRequest", data["id"],  to=connected[str(data['idFriend'])])
    insertFriendRequest(data["id"], data['idFriend'])

@sio.event
def searchRandomOpponent(sid, data):
    print(data)
    if len(wait) > 0:
        #emit
        for idOpponent in wait:
            if idOpponent != data['id']:
                idSala = wait[idOpponent]
                exito = joinGame(data['id'], idSala, data)
                if exito:
                    print("empareja ", data['id'], idOpponent, idSala)
                    sio.enter_room(sid, str(idSala))
                    #sio.emit('startGame', {'idOponent': id
                    # Opponent, 'idSala': idSala, 'rojo': False}, room=sid)
                    sio.emit('startGame', {'idOponent': data['id'], 'idSala': idSala, 'rojo': True}, to=str(idSala), skip_sid = sid)
                    sio.emit('startGame', {'idOponent': idOpponent, 'idSala': idSala, 'rojo': False}, to=sid)
                    print("EMITED TO", str(idSala))
            else:
                sio.emit('returnSearch', {'exito': False})
        del(wait[idOpponent])
    else:
        exito, idSala = createGame(data['id'], data)
        if exito:
            wait[data['id']] = idSala
            print(idSala)
            sio.enter_room(sid, str(idSala))
    sio.emit('returnSearch', {'exito': False})
    
@sio.event
def cancelSearch(sid, data):
    if data['id'] in wait:
        exito = deleteGame(data['id'], data)
        if exito:
            idSala = wait['id']
            wait.remove(data['id'])
            sio.leave_room(sid, str(idSala))
        return True
    else:
        return False

@sio.event
def doMov(sid, data):
    print(data)
    print("do mov on game ", data['id'])
    #guardar movimiento
    mov = ""
    if data['color'] == 'rojo':
        mov = str(int(data['mov'][0]))
        mov += str(int(data['mov'][1]))
        mov += str(int(data['mov'][2]))
        mov += str(int(data['mov'][3]))
        saveMov(data['id'], mov)
        print("guardado")
        mov = str(9 - int(data['mov'][0]))
        mov += str(8 - int(data['mov'][1]))
        mov += str(9 - int(data['mov'][2]))
        mov += str(8 - int(data['mov'][3]))
    else:
        mov = str(9 - int(data['mov'][0]))
        mov += str(8 - int(data['mov'][1]))
        mov += str(9 - int(data['mov'][2]))
        mov += str(8 - int(data['mov'][3]))
        saveMov(data['id'], mov)
        print("guardado")
    sio.emit('opMov', {'mov': mov}, to=str(data['id']), skip_sid=sid)
    print("EMITED TO", str(data['id']))

@sio.event
def enterRoom(sid, data):
    print(sid, "HAS ENTERED")
    sio.enter_room(sid, str(data['id']))

@sio.event
def leaveRoom(sid, data):
    print(sid, "HAS LEAVED")
    sio.leave_room(sid, str(data['id']))
    
@sio.event
def sendMsg(sid, data):
    print("send message to room ", data['id'])
    #guardar mensaje si es necesario
    sio.emit('my msg', data["msg"], to=str(data['id']), skip_sid=sid)

# TE lo envia el jugador que pierde con idSala(idPartida) y el id del perdedor y del ganador
@sio.event
def lose(sid, data):
    print("send win to room ", data['idSala'])
    #HACER CAMBIOS EN LA BD
    finishGame(data['idSala'], data['idGanador'])
    
    sio.emit('win',(), to=str(data['idSala']), skip_sid=sid)

