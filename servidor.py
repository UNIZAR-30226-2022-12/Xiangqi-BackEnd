import socketio

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

static_files = {
    '/': 'latency.html',
    '/static/socket.io.js': 'static/socket.io.js',
    '/static/style.css': 'static/style.css',
}