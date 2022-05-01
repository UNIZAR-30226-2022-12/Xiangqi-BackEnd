import socketio
from server_helper import *

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

app = socketio.WSGIApp(sio)

mov = {}
wait = {}

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('returnConnect', {'exito': True})
    
@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    
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

@sio.event
def doMov(sid, data):
    print(data)
    print("do mov on game ", data['id'])
    #guardar movimiento
    mov = ""
    if data['color'] == 'rojo':
        mov = data['mov']
        saveMov(data['id'], mov)
        #mov[str(data['id'])] += data["mov"]
        mov = str(9 - data['mov'][0])
        mov += str(8 - data['mov'][1])
        mov += str(9 - data['mov'][2])
        mov += str(8 - data['mov'][3])
    else:
        mov = str(9 - data['mov'][0])
        mov += str(8 - data['mov'][1])
        mov += str(9 - data['mov'][2])
        mov += str(8 - data['mov'][3])
        saveMov(data['id'], mov)
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
    sio.emit('my msg', data["msg"], skip_sid=sid)

