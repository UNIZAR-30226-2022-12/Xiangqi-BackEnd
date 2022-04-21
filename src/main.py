from datetime import timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import socketio
from server_helper import *
from clases import *

sio = socketio.Server()
app = FastAPI()

def verify_token(request: Request):
    if 'x-access-token' not in request.headers: #busca la cabecera x-access-token en el request
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    token = request.headers['x-access-token']
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        #current_user = crud.get_user_by_uuid(db, data['public_id']) #obtener el usuario de la DB y devolverlo
        return data['id']
    except:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )   

# Esto es porque el back corre en una URL distinta que el front en las pruebas y 
# el navegador se queja sino de que las urls no corresponden
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mov = {}
room = {}

@app.post("/do-test")
def do_test():
#def do_createGame(id: int = Depends(verify_token)):
    t = cargarTablero("0020907021229274")
    return t

@app.post("/do-create")
def do_create(data: User):
    returnValue = registerUser(data)
    return returnValue

@app.post("/do-login")
def do_login(data: LoginData):
    returnValue = loginUser(data)
    return returnValue

@app.get("/do-getProfile/{id}")
#def do_getProfile(id: int, id2: int):
def do_getProfile(id: int, id2: int = Depends(verify_token)):
    returnValue = perfil(id)
    return returnValue

@app.post("/do-validate")
def do_validate(data: EmailData):
    exist = validate(data)
    return exist

@app.post("/do-forgotPwd")
def do_forgotPwd(data: EmailData):   
    exist = forgotPwd(data.email)
    return exist

@app.post("/do-changePwd")
def do_changePwd(data : LoginData):  
    returnValue = changePwd(data)
    return returnValue

@app.get("/do-getCountries")
def do_getCountries():
    returnValue = getAllCountries()
    return returnValue

@app.get("/do-getProfileImage/{id}")
#def do_getProfileImage(id: int ,id2: int):
def do_getProfileImage(id: int, id2: int = Depends(verify_token)):
    exito, image = getUserImage(id)
    if exito: 
        return image
    else:
        return {"error": False}

@app.post("/do-changeProfile/{nickname}/{name}/{date}/{country}/{pwd}")
#def do_changeProfile(nickname: str, name: str, date: str, country: str, pwd: str, image: Image, id: int):
def do_changeProfile(nickname: str, name: str, date: str, country: str, pwd: str, image: Image, id: int = Depends(verify_token)):
    user = {'nickname': nickname, 
            'name': name, 
            'date': date, 
            'country': country, 
            'pwd': pwd}
    exito = editProfile(id, user, image.image)
    return exito

@app.get("/do-deleteAccount")
#def do_deleteAccount(id: int):
def do_deleteAccount(id: int = Depends(verify_token)):
    exito = deleteAccount(id)
    return exito

@app.get("/do-getRanking")
def do_getRanking(id: int):
#def do_getRanking(id: int = Depends(verify_token)):
    ranking = getRanking()
    return ranking

@app.get("/do-getShopSkinList")
def do_getShopSkinList():
    skinList = getShopSkinList()
    return skinList

@app.get("/do-buySkin/{id},{skinId}")
def do_buySkin(id, skinId:int):
    exito = buySkin(id,skinId)
    return exito
    
@app.get("/do-getUserSkinList/{id}")
def do_getUserSkinList(id: int):
    skinList = getUserSkinList(id)
    return skinList

@app.get("/do-editUserSkin/{id},{skinId}")
def do_editUserSkin(id, skinId: int):
    exito = editUserSkin(id,skinId)
    return exito

@app.post("/do-loadGame")
def do_loadGame(data, id: int):
#def do_createGame(id: int = Depends(verify_token)):
    returnValue = loadGame(id, data)
    return returnValue

@app.post("/do-searchRandomOpponent")
def do_searchRandomOpponent(data, id: int):
#def do_createGame(id: int = Depends(verify_token)):
    #idPartida, id = searchRandomOpponent(id, data)
    if len(room) > 0:
        #emit
        idOpponent = next(iter(room))
        idSala = room[idOpponent]
        del(room[idOpponent])
        exito, id = joinGame(id, idSala, data)
        if exito:
            return {'exito': True, 'idPartida': id, 'idOpponent': idOpponent}
    return {'exito': False}

@sio.on('connection')
async def connect(sid, data):
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
    
@sio.on('disconnection')
async def disconnect(sid, data):
    print("disconnect room ", data['id'])
    
    sio.leave_room(sid, data['id'])
    saveMov(data['id'], mov[str(data['id'])])
    mov[str(data['id'])] = ""
    if data['id'] in room:
        del room[data['id']]
        
@sio.on("createGame")
async def do_createGame(sid, data, id: int):
#def do_createGame(id: int = Depends(verify_token)):
    if id not in room:
        exito, idSala = createGame(id, data)
        if exito:
            room[id] = idSala
            sio.enter_room(sid, idSala)
        return True
    else: 
        return False
    
@sio.on("cancelcCreateGame")
async def do_cancelCreateGame(sid, data, id: int):
#def do_createGame(id: int = Depends(verify_token)):
    if id in room:
        exito = deleteGame(id, data)
        if exito:
            idSala = room[id]
            room.remove(id)
            sio.leave_room(sid, idSala)
        return True
    else: 
        return False
        
@sio.on('sendMsg')
async def sendMsg(sid, data):
    print("send message to room ", data['id'])
    #guardar mensaje si es necesario
    sio.emit('my msg', data["msg"], room=data['id'], skip_sid=sid)
    
@sio.on('doMov')
async def doMov(sid, data):
    print("do mov on game ", data['id'])
    #guardar movimiento
    mov[str(data['id'])] += data["mov"]
    sio.emit('my mov', data["mov"], room=data['id'], skip_sid=sid)

