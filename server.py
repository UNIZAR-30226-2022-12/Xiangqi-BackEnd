from aiohttp import web
import socketio
import mysql.connector

cnx = mysql.connector.connect(user='psoftDeveloper', password='psoftDeveloper',
                              host='database-1.cb2xawbk7cv6.eu-west-1.rds.amazonaws.com',
                              database='BDpsoft')



get_users = ("SELECT * from Usuario WHERE nombre = %s")

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
@sio.on('add')
async def peticion(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)
    name = message.get("name")
    print(name)
    cursor = cnx.cursor()

    cursor.execute(get_users, (name,))
    #print(cursor.fetchall())
    #print(len(cursor.fetchall()))

    if len(cursor.fetchall()) > 0: 
    ## await a successful emit of our reversed message
    ## back to the client
        print("existe")
        await sio.emit('message', True)
    else: 
        print("no existe")
        await sio.emit('message', False)

    cursor.close()

    return False

    

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)

cnx.close()
