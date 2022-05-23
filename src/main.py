from datetime import timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from server_helper import *
from clases import *

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

@app.post("/do-create")
def do_create(data: User):
    returnValue = registerUser(data)
    return returnValue

@app.post("/do-login")
def do_login(data: LoginData):
    returnValue = loginUser(data)
    return returnValue

@app.get("/do-getNickname/{id}")
def do_getNickname(id: int):
    nick = getNickname(id)
    return nick

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
#def do_getRanking(id: int = Depends(verify_token)):
def do_getRanking(id: int = Depends(verify_token)):
    ranking = getRanking()
    return ranking

@app.get("/do-getPoints")
#def do_getRanking(id: int = Depends(verify_token)):
def do_getPoints(id: int = Depends(verify_token)):
    ranking = userPoints(id)
    return ranking

@app.get("/do-getStoreItems")
def do_getStoreItems(id: int = Depends(verify_token)):
    shop = getStoreItems(id)
    return shop

@app.post("/do-purchaseItem")
#def do_buySkin(skinId: int, id: int):
def do_purchaseItem(data: PurchaseData, id: int = Depends(verify_token)):
    exito = buySkin(id, data.id, data.tipo, data.price)
    return exito
    
@app.get("/do-getUserSkinList")
def do_getUserSkinList(id: int = Depends(verify_token)):
    skinList = getUserSkinsList(id)
    return skinList

@app.post("/do-editUserSkin/{skinId}/{id}")
def do_editUserSkin(skinId: int, id: int = Depends(verify_token)):
    exito = editUserSkin(id,skinId)
    return exito
    
@app.post("/do-loadGame")
def do_loadGame(data: IdPartida):
#def do_createGame(id: int = Depends(verify_token)):
    print("LLega: ", data.id)
    returnValue = loadGame(data.id)
    return returnValue

#busca usuarios
@app.post("/do-searchUsers")
def do_getSearchUsers(data: Nickname, id: int = Depends(verify_token)):
    #users = getUsers(data.nickname)
    users = getSearchNoFriends(data.nickname, id)
    return users

@app.get("/do-getSearchNoFriends")
def do_getSearchNoFriends(data):
    users = getUserNoFriends(data["id"])
    return users

@app.get("/do-getFriends")
def do_getFriends(id: int = Depends(verify_token)):
    users = getFriends(id)
    return users

@app.get("/do-getFriendRequests")
def do_getFriendRequests(id: int = Depends(verify_token)):
    users = getFriendsRequest(id)
    return users

@app.get("/do-getHistorial")
def do_getHistorial(id: int = Depends(verify_token)):
    returnValue = userHistorial(id)
    return returnValue

#busca usuarios
@app.post("/do-rejectRequest")
def do_rejectRequest(idOther: Id, id: int = Depends(verify_token)):

    rejectRequest(id, idOther.id)
    
    return True

#busca usuarios
@app.post("/do-acceptRequest")
def do_acceptRequest(idOther: Id, id: int = Depends(verify_token)):
    
    acceptRequest(id, idOther.id)
    
    return True

#perfil sin game ni staat
@app.get("/do-getProfileInfo/{id}")
def do_getProfileInfo(id, id2: int = Depends(verify_token)):
    
    return getProfileInfo(id)




