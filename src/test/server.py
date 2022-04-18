from aiohttp import web
import socketio

from server_helper import *


## creates a new Async Socket IO Server
sio = socketio.AsyncServer()
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.on('login')
async def login(sid, data):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(data['email'])
    print(data['pwd'])
    
    returnValue = loginUser(data)

    #return returnValue
    await sio.emit('returnLogin', returnValue)
    
@sio.on('startGame')
async def startGame(sid, data):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(data)
    
    returnValue = crearTablero();
    #return returnValue
    await sio.emit('returnStartGame', returnValue)

@sio.on('register')
async def register(sid, data):
    print("LLEGA LA REQUEST DE REGISTRO de ", sid)

    returnValue = registerUser(data)

    await sio.emit('returnRegister', returnValue)

@sio.on('profile')
async def profile(sid, data):
    print("LLEGA LA REQUEST DE PERFIL de ", sid)

    returnValue = perfil(data)

    await sio.emit('returnProfile', returnValue)   

room = {}

@sio.on('sendMsg')
async def send(sid, data):
    print("sendMsg ", sid)
    await sio.emit('receiveMsg', data, room=data['id'], skip_sid=sid)
    if not data['id'] in room:
        room[data['id']] = [sio, None] 
    else: 
        print(sio)
        print(room[data['id']][0])
        if sid == room[data['id']][0]:
            await sio.emit('receiveMsg', data, to = room[data['id']][1]) 
        else:
            await sio.emit('receiveMsg', data, to = room[data['id']][0])   
    
@sio.on('connection')
async def send(sid, data):
    print("connect room ", data['id'])
    
    sio.enter_room(sid, data['id'])
    
    if data['id'] in room:
        print("existe")
        room[data['id']][1] = sid
        print(sid)
    else: 
        print("no existe")
        room[data['id']] = [sid, None] 
        print(sid)
  

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)
## We kick off our server
if __name__ == '__main__':
    web.run_app(app)

